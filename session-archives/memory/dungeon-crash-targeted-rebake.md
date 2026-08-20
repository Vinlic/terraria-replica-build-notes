---
name: dungeon-crash-targeted-rebake
description: 进地牢崩溃(trace 21万解码风暴)=晚到表全量invalidateAll重烘384chunk;修=chunkSheets缺表登记+onBakeAssetArrived精确打击,双路径合一;黑影修复同款解码缓存驱逐
metadata:
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-14T01:04:06.680Z
---

2026-08-14 用户报"进地牢崩溃"+Chrome trace(130MB/66万事件)。

**Trace 法医(生产构建 4173)**:JS 堆仅 47MB(非 JS OOM)·零 >500ms 长任务
(非主线程卡死)·**崩溃前 15s 恰好出现 21 万次 "Draw LazyPixelRef"(图像解码
风暴,峰值 9.9 万/5s)**。链条:进地牢=地牢墙 Wall_7/8/9+Tiles_7+背景 Background_
7x/9x 批晚到 → onVImageLoaded(Game 白名单+bakeTracker 双路径)→ invalidateAll
→ **384 chunk 全量重烘 × 每 chunk 数百次 drawImage 大表** → GPU 内存压力
(196MB chunk 画布+大表+背景)致解码缓存反复驱逐 → 每次绘制重解码 →
raster/GPU 风暴 → 渲染进程崩溃。

**修法(全量→精确打击)**:
1. ChunkCache.`chunkSheets`: Map<chunkKey, Set<file>>——renderChunk 置
   _bakingKey,bakeTracker.note(file)(=ensureVImage miss)登记进当前 chunk 的
   缺表集;markDirty/LRU 淘汰/renderChunk 重入时删条目
2. `onBakeAssetArrived(file)`(500ms 去抖合批):只 markDirty 登记过该文件的
   chunk;**零命中=no-op(绝不 invalidateAll 兜底——那正是风暴根因;
   逻辑自洽:烘焙时已就位的文件不可能在 chunk 里留过 fallback)**
3. Game.ts onVImageLoaded 白名单路径同路由 this.chunks.onBakeAssetArrived
   (scheduleChunkInvalidate/invalidateAll 调用点清零,函数留作无调用兜底)
4. F5: cc.arriveInvalidateChunks 调试计数

**探针(scripts/_dungeon-crash-probe.mjs)**:?play=small → 玩家直传 dungeonX
→ 12s 观察:**存活,arriveChunks=2(旧版=384 全量),dirtyQueue 归零,零 error**。

## 同日 trace③:死亡重生远跳 → 第三台引擎
地牢死亡→重生跳回出生点(1300+格)= 视野整批新 chunk 烘焙(~100×数百家
drawImage)+ LRU 同批淘汰地牢 chunk,在长地牢会话积累的 GPU 压力下解码缓存
已在驱逐线→烘焙全量重解码(145k/10s)→崩。**修:MAX_CHUNKS 384→224**
(画布常驻 196→112MB,给解码缓存留空间;缩放 0.5 可视 ~100 chunk 仍冗余)。
探针(远传地牢 6s→模拟重生跳回出生点→20s):存活/脏归零/零 error。
三台引擎全拆:晚到表(全量重烘→精确)/动画(不筛视野不冻暂停→双门)/
重生远跳(常驻压力→减半)。若还有第四台,F5 chunkCache 段+trace 定位。

**与图鉴黑影修复同根**:都是"解码缓存被 GPU 内存压力驱逐"的不同表象——图鉴
=canvas 内容丢,地牢=每帧重解码。教训:**onVImageLoaded 的响应范围必须与
"该表实际影响的内容"同构**(chunk 级),全局响应=风暴放大器。

## 同日 trace②:站定+暂停也崩 → 动画 tile 持续重烘引擎
第二份 trace(28k 解码/9s+1.2万任务/s churn,站定暂停态)定性:**advanceAnim**
每换帧行重烘含动画 tile 的 chunk(火把/篝火/烛台;地牢门口就有一堆)——
①暂停时渲染循环仍跑 advanceAnim ②重烘不筛视野(LRU 384 里屏外的也烘)。
**双门修**:Game.ts 调用点 `if (!this.paused)`(原版单机暂停世界全冻结=语义
对齐)+ `chunks.animView` 视野矩形过滤(±2 chunk 冗余;屏外 chunk 回视野时
渲染 get 惰性重烘,动画自然追上)。探针(放篝火+火把→传地牢→暂停站 25s):
存活、dirty=2、零 error。**风暴引擎至此两台全拆:晚到表(全量重烘)+动画
(不筛视野/不冻暂停);同构原则第二课:重烘的范围必须=可见的范围**。

相关:[[bestiary-contextloss-fix]] [[asset-lazy-loading]] [[leak-family-sweep]]
