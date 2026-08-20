---
name: blockframes-lookup-rebuild
description: 标准实心块auto帧表(LOOKUP)2026-08-12按原版判定链机械重建;旧表仅47/256掩码且L角坐标错位=木材衔接异常根因
metadata: 
  node_type: memory
  type: project
  originSessionId: ec878731-1c65-4b4c-9a3b-c8009ce5461a
  modified: 2026-08-12T15:35:54.103Z
---

VanillaTiler.ts 的 `LOOKUP`(8 向掩码→候选帧)2026-08-12 按**原版判定链机械重生成**(256 全掩码)。血案:旧手写表仅覆盖 47/256 掩码(209 个回落 DEFAULT=[1,1] 平帧),且 L 角坐标错指 13-17 列(原版实际 0-5 列×3-4 行;16/17 列越 16 列表宽被 frameHasContent 兜底)——密集木结构衔接无边缘、无端点、无圆角,表现为"木材衔接贴图和原版不一样"。

**原版机制(WorldGen.TileFrameCosmetic,WorldGen.cs:85144-85506)**:放置/破坏时运行时重算,帧落 tile.frameX/frameY(本仓库为渲染时查表,语义等价):
- **正交四向决定基础帧**(对角只在全连时参与);**3 变体**(frameNumber,放置时 genRand);
- 表布局(Tiles_30 等 16 列×15 行,18px 网格):col1-3×row1 内部 | col0/col4 竖左右缘 | row0/2×col1-3 横上下缘 | col6-8 端点+圆角 | col9 右端 col12 左端 | col9-11×row3 孤立 | **col0-5×row3-4 L 角(带变体)** | col10-12 全连圆角(缺两对角);
- :84986-85129 坡面圆角带((18+n)*18 列)超 16 列表宽,未移植(平块不受影响,已注释)。

**How to apply**:
- 修改 LOOKUP 必须回到 WorldGen.cs:85144-85506 逐条对照,勿凭视觉猜坐标;重建器语义见表头注释(每族带锚点行号)。
- 验证法:`tsx -e` + 假 store(type/flags/half/slope + idx/inBounds)调 autoFrameAt,21 形态期望值见当次会话(孤立/端点×4/条带×2/L角×4/T×4/全连圆角×5)。
- frameHasContent 兜底会**静默**吞掉越界帧(表现为平帧)——排查"某形态贴图不对"时先查 atlas src 是否 oob(F5 报告 focus.atlas.oob 字段)。
- 相关 [[vanilla-ui-port]](素材表布局惯例)、[[waterfall-anim-frames]](另一类帧表坑)
