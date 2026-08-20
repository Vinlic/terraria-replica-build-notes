---
name: lantern-style-axis
description: 灯笼不发光根因=竖排样式家族帧编码错(TileObjectData 默认 StyleHorizontal=false);placeFurn 横排假设受害清单
metadata: 
  node_type: memory
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-11T10:00:21.996Z
---

2026-08-11 用户报地牢灯笼不发光(标注 frameX=54)。

**权威语义(TileLightScanner 主 switch case 42 + TileObjectData)**:
- **TileObjectData 默认 StyleHorizontal=false → 样式竖排(frameY)**!只有显式 `= true` 的才横排
- 灯笼 42:样式在 frameY(行高 **36**,实证 frameY/36),**frameX 只有 0(亮)/18(灭)**——亮灭档在 X
- 发光门:`frameX != 0 → 不发光`;光色按样式 12 行色表(0:(.7,.65,.55)…9:(.9,.2,.4) 11:(.85,.6,1) 14:(1,.95,.65);样式 7/9 叠 demonTorch 调制,恶魔火把计数未实装取中值近似)
- 吊灯 34 门:`frameX % 108 < 54` 才发光(样式 X 每 108 + Y 每 54 双轴)

**根因**:DungeonPass.placeFurn 通用帧公式 `frameX = style×stride` 假设横排——灯笼被写 frameX=54 → 非法帧(渲染错位+光判灭)。已修:placeFurn 加第 9 参 `styleRowH?`(非空=竖排:frameY=style×rowH+dy×18、frameX=fx×18);灯笼调用传 36;lantern def 移除静态 light(改走 specialTileLight case 42 色表)。

**同族受害者修复完成(2026-08-11 第二轮,TileObjectData 模板快照解析 + Tiles_N.png 尺寸实测双重实证)**:
- 样式行高公式:`rowH = Σ(CoordinateHeights[i] + CoordinatePadding) + PaddingFix.Y`(灯笼 2 格=36 ✓ 验证)。解析器:/tmp 脚本状态机(必须处理 newTile.CopyFrom(模板) 继承——首轮解析漏模板把一批 H 误判 V)
- **真实轴表**:桌14/工作台18/铁砧16/织布机86/钢琴87/雕像105/磨刀站377/桌2(469)/Bast 506/旗帜55/书架101/浴缸90/小堆185/骨堆186 均横排 H(旧 placeFurn ✓ 不动);**竖排 V 受害**:蜡烛33(步22,亮灭 X 0/18)、吊灯34(样式 Y 行 54、wrap37 换列 108、亮灭块内 X +54)、烛台100(样式 Y 步 72=skip2×36)、灯笼42(36 已修)、酒桶94/中式灯笼95/电视126/画框173/提炼机219(步 36/54)
- **画布局(Tiles_N.png 实测)**:240 墙饰 1944×162=横排 36 列×54 **wrap36 超 36 换行 Y+54**;242 画 324×1944=竖排 27 行×72 **wrap27 换列 X+108**(旧 style*108 直接写出 3996px 越界=地牢画样 1+ 全丢);246 画 54×1332=竖排 37 行×36;245 横排 36 步(旧公式恰好对)
- 落地:DungeonPass placeWallArt 按表分派(240/241/242)、蜡烛三处(X 亮灭 0/18 + Y 样式 22)、吊灯 placeFurn styleRowH=54、烛台×2 styleRowH=72;CaveHousePass placeFurniture 画四表分派(240/242/246/245)
- **Review 第二轮补漏(2026-08-11)**:全调用对账脚本(必须提取 `...VAN(N,fw,fh)` 形式 def——`vanilla:{sheet:` 正则漏 legacy 三件套曾把灯笼误判 H)+ **PNG 行带实测**(纯 python zlib 解 IDAT+unfilter,无 PIL 环境):
  - 路灯 93:竖排步 **110**(70×2048,6 格物件+2pad),def fh 曾错写 3→修 6;亮灭 X 0/18
  - 旗帜 91:横排步 **54** wrap37 换行(1998×162=37×54);Dungeon/IslandHouse 曾写 style*18
  - CaveHouse 烛台 rng(0,5) 曾走通用横排→修
  - **统一收敛**:新建 `src/world/FurnitureStyle.ts` 权威布局表(furnitureStyleBase),DungeonPass.placeFurn / CaveHouse.placeFurniture / **Game 玩家放置**(曾同样 style*fw*18 一刀切)三端共用;心灯判定注释 frameY 324-358=样式 9 与新布局吻合
  - 对账脚本模式:placeFurn 调用 × TILE_BY_KEY 常量 → sheet → 轴表;横排传 styleRowH 或竖排漏传都会被揪出
- 语法坑:某次 python replace 在 DungeonPass 1439 产生多余顶层 `}`(esbuild Unexpected "}")——已修;**教训:多行 python replace 后必须立即 tsc,别攒批**
