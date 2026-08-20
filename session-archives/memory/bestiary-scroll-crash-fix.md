---
name: bestiary-scroll-crash-fix
description: 图鉴滚轮翻页崩溃三根因(零缓存自取/每tick全量重建/边界空滚);修=缓存+在途去重+rAF合并+阈值门;风暴探针40/40画布堆平稳
metadata:
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-13T15:06:17.529Z
---

2026-08-13 用户报"图鉴滚动翻两页就崩,贴图像加载不过来;点击翻页正常"。

**三根因叠加(BestiaryPanel.ts)**:
1. **贴图零缓存自取**:drawPortrait 三处 `vimages.get` miss → `new Image()` 自取,
   **结果不回写任何缓存**——trackpad 滚轮一滚几十个 tick,每个 tick 全量 refresh
   重建网格,同一张多帧行大 NPC 表被**反复解码**(HTTP 缓存只去重字节不解码)
   → 渲染进程解码/内存压爆=崩溃;"加载不过来"=onload 画到上代 refresh 已销毁
   的 canvas(纯浪费堆积)。点击正常因为一次点击=一次 refresh。
2. 每个 wheel tick 直接 page()+全量 refresh(无节流)
3. 边界处滚轮 offset 不变也全量重建

**修复四件**:
1. **bstLoadSheet 模块级缓存**:命中直回/atlas.vimages 借用/**在途去重**(并发
   refresh 同表只 fetch+decode 一次)/onerror 负终结(404 也回调防队列堆积)/
   160 条 FIFO 上限(引用即成本)。drawPortrait 全部走它,文件里唯一 new Image()
2. **refresh rAF 合并**(refreshNow 内部化):风暴每帧至多重建一次
3. **wheel 阈值门**:|acc|≥40 才翻页(trackpad 惯性事件流)
4. page() offset 不变早退 + paint/paintWithBg 加 canvas.isConnected 守卫

**E2E(scripts/_bstscroll-probe.mjs,生产 preview)**:?play=small 进世界 →
__swUI.onBestiary() 开面板(★__swFlow 桥没暴露 openBestiary,走 UI 回调)→
gridWrap 两波共 80 个 deltaY=120 wheel 事件 → **PASS**:页码 1-81→466-546
(翻到末页)、40/40 头像画布绘制、**堆 133→134MB 平稳**、渲染进程存活。

**教训**:①"每帧重查自愈"模式的 DOM 面板版=必须配缓存+合并,事件风暴下
自愈变自杀;②滚轮交互永远先想 trackpad 惯性(事件数 ×10);③懒取结果不回写
=白取(本仓第四犯变体)。

相关:[[asset-lazy-loading]] [[sw-asset-preload-port]]
