---
name: perf-audit-2026-08
description: "2026-08-10 全局内存/性能审计:实测+双代理静态分析,分级风险清单与修复优先级"
metadata: 
  node_type: memory
  type: project
  originSessionId: af6cf2c7-84f1-4f59-9d74-9dc27cdc059e
  modified: 2026-08-10T10:24:52.783Z
---

# 2026-08-10 全局内存/性能审计

实测(CDP 堆指标 + 进程 RSS + saveGame 探针,中世界 6400×1800):
- 稳态 60s:JS 堆 16-22MB 振荡无单调增长(无泄漏),FPS ~115,实体稳定
- **saveGame 单次:147ms,JSON 7.2MB,JS 堆瞬时 +144MB,进程 RSS +1.5GB**(GC 后不归还)
- 中世界加载:RSS +690MB;**主菜单基线 1.4GB**(疑似图集全量解码纹理)
- 常驻世界数组:15B/tile → 76/173/302MB(4200²/6400²/8400² 三尺寸)

## 分级风险(合并双代理结论)

### 致命/高
1. **ChunkCache 无淘汰**(ChunkCache.ts:26,90-97):每 chunk 2×256² canvas=512KB,Map 只增不减,
   跑图无界(满图大世界 ~22GB 理论)。修:LRU 淘汰(保留视口±2 圈)
2. **.wld 导入 5 份全图副本并存**(mainFlow:157 JSON.stringify(save)→loadSave→JSON.parse 双拷贝;
   parser 12B/t + importer 11B/t + RLE number[] + b64):7MB wld≈370MB 峰值,8400²≈1.2GB。
   修:parseWldToSave 直接产出 SaveData 后置空 buf;跳过 stringify/parse 往返
3. **saveGame RLE number[] 峰值**(SaveFile.ts:87-104 push 裸数组 8-24M 元素 + bytesToB64
   `s+=` 逐字符 + btoa + JSON.stringify):实测堆 +144MB/RSS +1.5GB。
   修:rle 输出改 Uint32Array 分块预分配;base64 用分块 String.fromCharCode.apply;
   或直接存二进制分段
4. **主菜单基线 1.4GB**:素材图集全量解码疑似元凶,待查(懒加载/按需解码)

### GC 压力(稳态)
5. VanillaLiquidRenderer 每 pass 分配 24 个类型化数组 ×2 pass/帧 ≈ 744KB/帧≈45MB/s
   (注释自估"~15 个"少算一倍)——提为按容量复用的模块级数组即可
6. 光照合成 compositeLight 每像素 4 个 tap 元组 ≈ 5.3M 小对象/s(Renderer.ts:1204-1221)——
   内联成标量
7. LightingEngine.compute 每次重算 new Int32Array(rw*rh*4)≈259KB×5-25次/s(:115)——复用
8. LiquidSim.update 内联 [[x±1,y]...] 元组数组 ×2 循环,活跃水流 ≈2.5M 对象/s(:213-230)——展开
9. 每 tick 固定小分配:Entity 6 桶 filter(:45-50)、checkPressurePlates/updateTriggerTiles
   3×new Set+字符串键、particles/dmgNumbers filter、entities.all() 拼接——in-place 压缩

### 中
10. ItemDrop 无 merge 无上限:dev 模式一次 ~500 实体(setupDevMode 溢出逐个 spawnDrop),
    雕像农场线性堆积——加 merge 或上限
11. 迷雾 getFogCanvas 随 exploredVersion 全图重建(5MB+126 万格/次,Renderer.ts:1302)——分片
12. Wiring 大网络 BFS 每计时器周期全量重放(Wiring.ts:234-334)——电路玩法的 CPU 尖峰
13. VanillaSpawner 每次刷怪重扫 2×169×123 zone 计数(与 15tick 前 scanScene 重复)——复用 scene
14. Minimap.redrawAll 全图+parseInt/格;minimap canvas 本身 w×h×4B 常驻(大世界 46MB)

### 可忽略
- Sfx 48 个 wav 全解码 ≈8.5MB;水蜡烛/营火/树苗/迷雾扫描均千级有节流;
  WaterfallRenderer/tintCache 等有界;Enemy def 克隆每怪驻留(Boss 30 段放大,应缓存 drops)
- TileStore 监听器不可注销:临时 LiquidSim dispose 是假的(~10MB/loadWorld,换新 World 兜底)

## 2026-08-10 复测(全修复后,用户 trace 复核)
Trace-20260810T111857:渲染进程 JS 堆峰值 57MB(菜单加载)→稳态 34MB,DOM 4k 节点,
仅 6 张解码位图——trace 内页面本身极轻。用户看到的"标签页 700MB+"是 Chrome 任务
管理器的标签页合计(渲染器+GPU+共享),非 JS 占用。
三档实测(逐进程 RSS,已扣除 Chrome 空白基线 706MB):
- 菜单增量 497MB(渲染器 342MB——其中 JS 17MB,其余为 Blink/合成器/图片缓存内部)
- 进小世界增量 1449MB(渲染器 1126MB:JS 133MB[世界数组 76MB+chunk+液体] +
  vimages 6918 张解码 269MB + uiimages 253MB + 图片/GPU 缓存内部)
结论:素材分层加载已把可控部分压到位;剩余大头是 Chrome 内部位图/合成缓存,
JS 侧无可再挤的空间(133MB 全是必要数据)。

## 修复优先级建议
P0: ChunkCache LRU(真泄漏)+ saveGame 二进制化(峰值最痛)+ 导入去双拷贝
P1: 液体渲染数组复用 + tap 内联 + LiquidSim 元组展开(三处改动小收益大)
P2: ItemDrop 上限/merge、迷雾分片、VanillaSpawner 复用 scene、基线 1.4GB 排查

## 2026-08-10 晚:读档三次卡死真相(Trace-20260810T175943 分析)
**contextlost×80090 / contextrestored×69006 风暴**,从第三次读档瞬间(19.8s)开始,
每秒 2.1 万次——GPU 显存被反复丢弃↔恢复,页面假死"反复崩溃"。根因双层:
1. **window 监听钉死旧 Game**:Input(5 个 window 监听)+ Renderer(resize)每实例挂全局
   匿名监听从不移除 → window 强引用 → 退出世界后整个旧 Game 对象图(ChunkCache 数百张
   chunk 画布 + Minimap 全幅 46MB + fogCanvas 全幅)永远不可达 GC。
2. **destroy() 只 remove 主画布**:detached canvas 的 GPU 背板回收滞后,三次读档累积
   数百 MB 显存 → Chrome 开始丢上下文。
修复(已落地):Input.destroy() 移除全部监听;Renderer.dispose()(resize 移除 +
主/lightCanvas/fogCanvas 清零 + minimap dispose);ChunkCache.dispose()(chunk 画布
清零+清表);Minimap.dispose();Game.destroy() 串起整条链。
**教训:每个挂 window/document 监听或持 canvas 的 per-Game 组件,destroy 时必须显式
拆除/清零——detached canvas 与全局监听是 JS 堆指标看不见的隐性泄漏。**

## 2026-08-10 晚第二轮(Trace-20260810T181743):修复后仍爆,两个新根因
dispose 链落地后撑得更久但多次循环仍 contextlost 风暴(28252 次),且出现
**角色/装备/时装贴图消失(选人界面+游戏内都看不到角色)**:
1. **buildAssets 每 Game 重建**(AssetGen.ts):itemIcons ~6700 张 canvas(含 vi_ 全量物品)
   + 全部 tile 表 + playerSheet + enemySprites——全是确定性程序化生成,内容每次相同!
   修:AssetBundle 改全局单例(`shared ??= {...}`),一次生成全程复用。ChunkCache 的
   sheets 即 assets.tileSheets,自动共享。
2. **PaperDoll 合成/调色缓存被 contextlost 打成白板且永不失效**(PaperDoll.ts cache/tintCache
   模块级):canvas 丢上下文后内容归零,缓存命中返回空图 → 角色隐形。修:`clearPaperDollCache()`
   导出,Game.destroy 调用(画布清零防泄漏)。
**注意:assets 单例化后,若仍发生 contextlost,共享图标/角色表会永久白板(不再有
"新 Game 重建"兜底)——contextlost 必须根治而不是兜底。** AutoTiler 缓存是实例级
(随 Game 回收)无需处理;atlas vimages 是 <img> 不受 contextlost 影响。

## 2026-08-10 多核落地:存档 worker + chunk 摊销(用户令"做必要做的多核")
- **决策依据**:全 GPU 渲染评估(WebGL 移植负 ROI:帧余量 5-7×,渲染段仅 1.9ms;原版 spriteBatch 611 处但光照网格同为 CPU);多核 ROI 排序=存档(147ms 主线程阻塞)>chunk 烘焙尖峰(87ms)>光照/液体(<2ms 不值得)
- **存档 worker 化**:`src/save/serialize.ts`(纯核心,ByteWriter/RLE/serializeSave,零依赖)←主线程 SaveFile(薄壳 re-export+同步 saveGame 兼容入口)与 `src/workers/save.worker.ts` 共用,**输出逐位一致**(10 断言:tiles/walls/liquid/liquidType/wire/player/header 全等);`SaveClient`(WorldGenClient 同款握手,broken 永久回退)——**postMessage 不 transfer**(活数组 detach 会毁游戏状态),主线程只付结构化克隆 memcpy(小世界 ~15ms);幽灵净化在视图上执行=worker 路径只净化副本。mainFlow.doSave 改异步(saveClient.ensure() 懒建)
- **chunk 摊销**:flushDirty(maxN=4)→加 budgetMs=6 时间预算(单 chunk 至少完成 1 个),跑图烘焙突发不再挤占帧
- **实测**:真实游戏小世界(504 万格)快速存档**主线程 0 个 >30ms 长任务**(旧:147ms+);回归 wiring31/lighting51 ✓;save.worker bundle 2.37kB 独立产物
- **SAB(SharedArrayBuffer)零拷贝方案评估后不做**:需 COOP/COEP 跨域隔离头,部署环境不可控;结构化克隆 15-60ms 已可接受,留作部署可控时的升级项
