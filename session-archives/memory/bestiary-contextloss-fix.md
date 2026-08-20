---
name: bestiary-contextloss-fix
description: 图鉴resize全消失=context丢失窗口期无重画;三层修=RO稳定居抖+contextrestored重画+空白自愈扫描;黑影=NotKnown原版设计;探针81/81全绿
metadata:
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-13T16:12:20.707Z
---

2026-08-14 用户报"图鉴仍有生物黑影/透明,多切几次才出现;**resize 后全部消失**"。

**分层定性**:
1. "黑影"= **原版设计**:renderInfo 对 NotKnown 条目 `filter:brightness(0)
   opacity(0.55)`(:995)——未知生物显示剪影是原版语义,非 bug
2. "透明/多切几次才出现"= 首访异步解码竞态(bstLoadSheet onload 前画布空白)
3. **"resize 全消失"= 真_bug**:拖拽窗口=每帧 RO→refresh→replaceChildren+81 张
   新 canvas=画布创建风暴→GPU 压力→**context 丢失**;canvas 2D 内容丢失后
   **不自动恢复**,而面板只在创建时画一次=永久空白。且 contextrestored 监听
   存在挂上之前的窗口期(丢失发生在风暴中、监听在重建后)——事件后补也接不到。

**三层修**:
1. **RO 稳定居抖 150ms**(尾部一次刷新;同尺寸早退;close 清 roTimer)——
   源头掐风暴;rAF 合并保留给滚轮/点击
2. **contextlost/contextrestored 监听**(网格 cell 与 96×96 大头像):lost
   preventDefault(允许恢复),restored 按原参数重画
3. **空白自愈扫描 scheduleBlankSweep**(核心,兜住一切丢失窗口):每次
   refreshNow 后 400ms 扫 `.sw-bst canvas`,getImageData alpha 全空判定空白
   →网格经 cell.dataset.credit 反查 working 行重画、大头像经 this.infoDraw
   参数重画(bstLoadSheet 缓存命中=同步,开销可忽略)

**探针 scripts/_bstresize-probe.mjs 实证**:开面板 81/81 ✓ →10 档连续
viewport 缩放风暴(80ms/档)+回原尺寸 → **81/81** ✓ →81 张合成 contextlost/
restored → **81/81** ✓。修复前:resize 风暴后 0/81(全透明),合成恢复事件后
81/81(证明机制对但接不到真实丢失窗口)——正是三层修的依据链。

**教训**:①DOM 面板画布"创建时画一次"模式在 context 丢失面前裸奔——要么
可重画(drawPortrait 纯函数化参数化),要么别用 canvas;②contextrestored
监听对"风暴中丢失"有时序盲区,自愈扫描(定时验空白补画)才是兜底;
③RO 直连 refresh 在拖拽场景=创建风暴,必须稳定居抖。

相关:[[bestiary-scroll-crash-fix]] [[leak-family-sweep]]
