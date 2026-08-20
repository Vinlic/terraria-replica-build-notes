---
name: vanilla-door-frames
description: 原版门帧竖排布局算法 + 各 gen pass 放门要 -2 的坑，Door.ts 助手与回归测试位置
metadata: 
  node_type: memory
  type: project
  originSessionId: 8f9c7b63-58b1-49de-a435-85fe12e156d6
  modified: 2026-08-09T10:39:50.185Z
---

原版 Tiles_10/11（关/开门）贴图表是**竖排**布局（2026-08-09 修复"门贴图不可见/开门错位"时确认）：

- 关门 style = `36*(frameX/54) + frameY/54`；frameX = 变体(0/18/36 三张纹理)+54*列（仅 0/54 两列），frameY = 54*(style%36) + 行内偏移。曾误用 `frameX = style*54`（横排）导致越界不可见。
- 开门 frameX = `72*列 + (direction==-1 ? 36 : 0)`，锚点在 direction==-1 时左移一格（WorldGen.OpenDoor L22384 / CloseDoor L15901；CloseDoor 关门只挡实体不挡图格 = Collision.EmptyTile(ignoreTiles:true)，且不重写 frameY、frameX 随机三变体）。
- **放门 y 偏移坑**：原版 `PlaceTile(x, j, 10)` → `PlaceDoor(x, j-1)` → 门顶格在 **j-2**。各 gen pass 持有的 vanilla j（地牢走廊 j2、入口 floor(cy)+1 是底格、浮空岛 floorY、神庙 jy、地狱堡 rowB-1）放整门时一律 `placeDoorClosed(st, x, j-2, style)`。
- 助手全在 `game/src/world/Door.ts`（doorClosedFrame/doorStyleOf/placeDoorClosed/openDoor/closeDoor/clearDoorAt）；玩家交互在 Game.ts toggleDoor（按 facing 开门、失败换向，原版 Player.cs L20965）。
- 回归测试：`node_modules/.bin/vite-node scripts/door-test.mjs`（帧数学+开关门往返+阻挡回退）。
- E2E 验证法：浏览器内 `import('/src/data/tiles.ts')` 拿 TILE_BY_KEY，扫 st.type 找门；chunk 画布像素要先把 camera.follow 覆盖为空函数冻结相机才会惰性渲染（`g.chunks.chunks` Map，key=(cx&0xffff)|(cy<<16)，CHUNK=16）。

关联 [[vanilla-worldgen-port-status]]、[[terraria-assets-pipeline]]。

## 高门 Tall Gate 开态错位修复（2026-08-10，用户标注 Starter_World (3263,394) 报"通过时贴图不对"）
- **它算门**：Tall Gate = 门族 1×5 物体（388 关 / 389 开，ShiftTallGate 保帧换型，玩家触碰自动开/离开自动关，原版 DoorOpeningHelper 语义）。
- **根因**：DRAW_Y_OFFSET 有 `388: -2` 而 **389 缺条目**（回退 0）→ 开门换型后整张贴图下移 2px、5 格栅板逐行重叠。原版实证 `addTile(388); newTile.FullCopyFrom(388); addTile(389)`（TileObjectData.cs:2325）——389 完整继承 DrawYOffset。修复=补 `389: -2`。**教训：开/关两态是两个 tile id，ObjectData 类偏移表必须成对登记**。
- 顺带核实：高门 CoordinateHeights=[18,16,16,16,18]+2pad → 帧距不均（94→114 是 +20，其余 +18），原版 wld 里 style1 帧就是 94/114/132/150/168（非常规 18 倍数，勿当坏数据"修"掉）；shiftTallGate 的 %90 锚点回溯对这些值恰好全对。
- 验证：浏览器并排放关/开两态，顶格内容起点均为 -4（对齐 ✓）；180/180。

## 放置朝向族：椅子/陷阱（2026-08-11，用户问"桌椅怎么转向"+实测"换朝向摆椅子还是同向"）
- **原版机制**（Player.cs PlaceThing_Tiles_PlaceIt_ 系列，放置后处理钩子）：
  - **椅子 15**（:40193 SpinChairs）：`direction==1 → 上下两格 frameX 各 +18`——面朝左放=朝左(frameX 0)，面朝右放=朝右(+18)。1×2 两行都要。
  - **陷阱 137**（:40209 SpinTraps）：同款单格 +18。
  - **床 79/浴缸 90**（:40185 SpinBedsAndBaths）：仅联机重同步，单机无逻辑。
  - **桌子 14 不在列**——原版桌子对称、**不可转向**（用户问"桌椅"，实际只有椅子转）。
  - 锤子砸家具 = 破坏（tileHammer 走伤害），**不旋转**——朝向只在放置瞬间定。
- **修复**：tryPlace 加 sheet===15 钩子（137 上轮已加）。探针：左向放 fx=[0,0]、右向放 fx=[18,18] ✓。探针坑：tryPlace 有 5.5 格距离限制，直接调内部函数要把 player 挪到放置点旁。
- **朝向排查 review 收口（2026-08-11）**：原版方向机制两条线：① PlaceIt_ 帧补丁（椅子15 +18 两行/陷阱137 +18 单格——已修）；② TileObjectData Direction=PlaceLeft/Right 备选锚点族。②全量提取后**仅浴缸 90 在我们注册表且可放置**：方向存 frameX+72 带（Tiles_90 每样式带 144px=双向并排；GetTileDrawData addFrX+=144*styleBand；wld 实测 frameX 双组 0-54/72-126）——tryPlace 补 sheet===90 钩子，右向 8 格 +72 ✓左向 0-54 ✓。其余 ②族：火烈鸟 579=渲染期动态面向玩家（TileDrawing case 579 frameY+22，非放置朝向）、餐盘 520/453/720/721 未注册、高门 388/389 仅锚侧无视觉、门 10/11 走门系统。马桶 497 wld 无样本未证实（表 72 宽疑 4 样式），留观察。桌 14/床 79 无方向（wld 帧分布=样式列）。
- **朝向排查终轮收口（2026-08-11 晚，用户令"继续验证其他，确认全部检查完毕"）**：
  - **马桶 497 有方向**（TileObjectData :4189 StyleHorizontal+WrapLimit2+Direction=PlaceLeft——**方向占样式列**：变体步长 36、方向位 +18；素材 72px=2变体×2方向吻合；本地 4 个 wld 无样本，源码实证）。tryPlace 加 sheet===497 重写帧（placeStyle*36 + facing?18 + 列偏移）——通用 *18 步长对它是错的。
  - **大炮 209 wire=旋转+开火复合状态机**（Wiring.cs:1237-1346）：块内列 0/3=旋转态（列0 frameY+54 抬仰角带0-8、列3 -54，两端钳位）、列1/2=待发；水平带 3/4（左向）+行0/1 → frameX±72 翻朝向；开火条件 flag2=!(左向&&行<2)，伤害 普通300/兔兔350、CheckMech 480/3600。devices.ts 此前只做开火半边且**角度解码用错**（把旋转状态列当仰角）——已整段 1:1 重写（弹药未接入，弹体仍以巨石近似）。
  - **大炮放置朝向**：TileObjectData 209 无 Direction（StyleHorizontal 而已）——放置即默认态，朝向调整全靠 wire 触发旋转 ✓ 无需放置钩子。
  - 其余终验：长椅 89=纯样式列（3 个 wld 帧分布证实无方向）、告示牌 55 同、火烈鸟 579=渲染期面向玩家。**朝向 review 全部闭环**：注册表内可放置物 = 椅15/陷阱137/浴缸90/马桶497（四个钩子全实证+探针过）、门/高门/火把走各自系统、其余无方向。
  - 并行会话在途回归：原版配方提取计数断言 2688→2786 漂移（其配方数据在变），非本轮改动。
