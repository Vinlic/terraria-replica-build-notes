---
name: load-progress-vanilla
description: "读档进度对齐原版:gen51\"正在加载世界数据\"按列/gen27\"正在安置液体\"收敛比例50-100;settle p 语义从 iter 计数改收敛比例"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-13T04:55:31.338Z
---

2026-08-13 用户要求"读档进度也对齐创建世界的原版效果"。对齐 WorldFile.loadWorld 的 statusText 序列:

**原版链(WorldFile.cs)**:
1. `LoadWorldTiles` :2514-2518:每列更新 `gen[51]("正在加载世界数据:") + int(i/w*100+1)%`
2. 液体沉降 :755-762:循环内 `gen[27]("正在安置液体") + int(num7*100/2+50)%`;num7=收敛比例=(num5-活量)/num5,num5=初始活量(活量回升则抬升,:759-761)→ 显示恒在 **50-100%** 区间
3. gen[48/49/50/51/73] 其余是保存/校验/回滚路径,读档主链只有上述两段

**实施**:
- `loadSaveData` 加可选 `onTilesProgress`(SaveFile.ts):tiles RLE 段按目标索引累计=等效列进度,每 1%(nAll/100)回调一次防 postMessage 风暴;可选参零破坏(importWld/测试/fallback 直用无感)
- **settle.ts p 语义改为原版收敛比例**(原为粗糙 `0.35+min(0.6,iter/20000)`):num5/num7 同式实现——gen 路径 pass 49(:16274-16277 progress.Set(num6/3+0.33))与 load 路径(:762)同源,生成路径进度条也顺带变准。纯 UI 语义,哈希闸门不受影响
- worker(worldGen.worker.ts):saveParse 加 `phase='tiles'` 上报;settle phase p 直传(去掉 0.3+p*0.5 旧映射)
- mainFlow `loadProgressLabel(phase,p)`:tiles→`Lang.text('LegacyWorldGen.51')+' '+min(100,int(p*100+1))%`;settle→`LegacyWorldGen.27`+' '+min(100,int(50+p*50))%;其余→自定义 LoadingSave。两处 worker onProgress 消费点统一改
- Game.loadWorld 主线程 fallback(importWld/worker 挂)同款 gen[27] 文案(:1609-1618);生成路径 newWorld 的 settleLabel **不动**(pass 名显示已是原版 pass 序列)
- 原版文案键在 `LegacyWorldGen`(我们 l10n 已有 94 键,zh/en 双语)

**测试**:tests/load-progress.test.ts 4 例(回调单调/末值 100/两公式断言/占位)。注意 label 公式在 mainFlow 闭包内不可直测,测试内是**同公式复刻**——改公式需两边同步(单一事实源风险,已注释)。

相关:[[load-perf-batch]] [[liquid-settle-perf]] [[save-parity-port]]
