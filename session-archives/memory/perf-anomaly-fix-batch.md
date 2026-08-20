---
name: perf-anomaly-fix-batch
description: 性能异常扫描修复批:ChunkCache 三漏释放+Audio LRU+invalidateAll 去抖+三微改;30/36 扫描项处置结论
metadata:
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-13T06:26:28.006Z
---

2026-08-13 全系统异常扫描(36 点)修复批。用户拒绝了主循环 worker 化(余量 5-7×,无单项超 3ms/tick,收益不足)。

**确认异常 10 条中修了 7**:
1. **ChunkCache 三漏释放**(慢性显存劣化主通道,与 contextlost 风暴同机制):markDirty/invalidateAll 置哨兵前、LRU 淘汰 delete 前,统一走新 `releasePair`(width=0,height=0;复用 dispose 语义)。行为零变化——哨兵原子替换旧 pair,渲染走 get() 惰性重建,直读 map 的只有 DebugReport 统计哨兵数(只读)
2. dirtyQueue 去重 `includes` O(n) → 伴生 dirtySet(消灭 invalidateAll O(n²));flushDirty shift 后同步删 Set,dispose 清两者
3. **Audio buffers LRU**:上限 3(每首解码 PCM 30-45MB,104 首 GB 级);`evictOld` 一轮全扫收集可淘汰者再删(跳过失败哨兵 null 与 pool 播放中)——**refresh-continue 式淘汰会死循环,扫描式才安全**(第一版翻车当场重写)
4. **invalidateAll 去抖合批**:Game.ts onVImageLoaded 挂 500ms setTimeout,765 Tiles_+368 Wall_ 风暴期 N 张表只触发一次。精确化(sheet→chunks 反查)登记待办
5. 粒子循环 st/solidAt 闭包外提(每粒子重建 → 循环级一次)
6. HitTile.update 去 `[...this.data]` 拷贝(Map 迭代中删当前项安全)
7. geyserTiles 增量维护补 443 分支+scan 时 clear(顺带修正确性:放置的间歇泉永不喷发)

**未做**:lightAtInto(雨滴池仅 ~50/帧,nursery 级小分配,改 5 文件收益不匹配);疑似 6 条(tintCache 惊群/动画重烘焙税/Minimap fillRect 等)留观察;误报 16 条不动。

**测试**:tests/chunk-canvas-release.test.ts(4 例,stub pair 直驱,不经过 renderChunk——node 无 DOM)、tests/audio-buffer-lru.test.ts(4 例,桩 rAF/window+私有字段直驱)。

**教训**:①vitest node 环境测 DOM 类,用 stub 对象绕构造依赖,别硬起 canvas;②AudioSystem 构造器立即 startLoop→rAF,测试前必须桩 requestAnimationFrame;③tsc 基线已有并行会话错误时,只 grep 自己触碰的文件判断。

相关:[[perf-audit-2026-08]] [[multiplayer-capacity-opt-batch]]
