---
name: worldgen-perf-batch
description: 世界生成零风险优化批:TileRunner/MudCaves/GemCaves 热循环(重复idx/属性链/元组洪泛);逐pass哈希自洽闸门法;总-24%
metadata: 
  node_type: memory
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-12T18:32:01.489Z
---

2026-08-13 用户问"其他世界生成流程是否也零风险有优化"。逐 pass 耗时排行(用现成 `onWorldPartial` 回调记录时间戳,零产品代码改动):基线 15.7s/4200×1200,大头=生物群系 4.5s/宝石系统 3.3s/栽树 1.4s/洞穴 0.7s。实施四批,总 **10.2s(-35%)**,闸门全程零漂移。

**已实施(全部过"逐 pass 哈希自洽"闸门)**:
1. **TileRunner.ts A 批**:①`ci0`+`ti` 重复 `st.idx(x,y)` 同值合并为一;②内层 typed array 引用与 `st.w` 提为局部(热循环局部化);③framed 跳过判定 `TILE_DEFS[t]?.framed&&!decor` → 模块级 `FRAMED_SKIP` Uint8Array(定义同源)。TileRunner 是沙漠/丛林/大理石/矿石全家族共用 runner。
2. **TileRunner.ts D 批(续)**:mudWall 分支每格 5-8 次 `st.wall[st.idx(...)]` 跳读 → `twall[ti±stW]` 内联(负索引语义两版一致:typed array 越界=undefined);挖空/铺设分支的 st.type/flags/liquid/liquidType/wall 读写全部换 ty/tf/tliq/tltype/twall 局部。子级计时实证:jungle 1893→629ms、desert 1953→729、mushroom 1208→407、marble 1072→452(同负载窗口)。
3. **Spread.ts(MudCaves 全图洪水)B 批**:3×3 窗 solid 判定属性链 → 函数级 `SOLID` LUT;`st.idx` 内联 `l*w+k`;typed array 局部化。
4. **GemPasses.ts(GemCaves countTiles 洪水)C 批**:`Set<number>` seen + 每格 4 元组数组 push → 平坦 Int32Array 栈(同序入栈/pop 取尾=DFS 下邻优先保持)+ Uint8Array seen(visited 列表局部清除;栈深上界 4×300+1<4096 无需增长)。**踩坑:第一版留了"栈增长"半成品(typed array 定长不可增长)——必须当场接 tsc/测试,半成品不许过夜**。

**闸门方法论(可复用,12 行测试即可重建)**:`onWorldPartial` 钩子逐 pass 记录 `type/flags/wall/liquid/liquidType/half/slope` 七数组 fnv1a → `GENHASH_DUMP=1` 落盘基线 → 改后跑比对 `diff=0/47` 即逐字节等价。**关键教训:并行会话实时编辑 worldgen,基线保质期只有分钟级**——每批改动前重落基线、改后立即比对(短窗口);跨小时比对必被搅旧误报。负载也会污染耗时(并行 vite build 满载时耗时×2.7,等 load<15 再测)。

**候选未实施**(性价比/风险权衡后放弃):DesertHive 蚁狮巢(独立 FastRandom 流+DFS,定制深、风险>收益);栽树 1.0s(同款内联可再-10%,边际);子级计时探针方法论=BIOME_TIMER env 门包裹 vanillaBiomes 各 run* 调用(测完必须撤——**并行会话 git commit -a 会把工作区探针扫进提交**,本次 HEAD 即被扫入;撤除后工作区为净版,diff 恰为探针移除)。

**失败归属**(勿重复排查):caves-checkpoint/弹幕三件套(projectile-reflect/arrow-tree-pass/proj-critter-hit)/debug-report/world-final-hash@1511931452 均经 git stash A/B 证实为并行会话在途,与本批无关。

相关:[[liquid-settle-perf]] [[vanilla-worldgen-passes]] [[perf-audit-2026-08]]
