# 尾段五连根因 #69→#77 清零（NNNNN 批 2026-08-19/20）

9293480 链 0..65→0..76 全绿（+11 槽），首差 #77 撞 DungeonPass 帧债域移交止。
方法论新资产：tttt-app 织入服务器双侧 span 对拍（SW_TT_SPAN_PASSES=<pass 显示名>
× SW_WWW_SPAN_OUT；服务器须带 -world 参否则 -autocreate 不触发；滤 d/n 规范化，
`a N`≡`b 0 N`）——Next 流首差行号即掷流分叉点，配决策点探针落位。

## 五根因

1. **岛屋壳/柱半砖坡位**（IslandHousePass）：cs:79903-79908/79969-79974 落日光板
   显式 halfBrick(false)+slope(0)；JS 不清。室内挖空支只 active(false)——0 位靠
   壳填先行清位继承（勿在挖空支单独补）。
2. **SaveSlopes 静态快照**（QuickCleanupPass）：TileID.PostSetupContent（TileID.cs:425-429）
   一次性从 pristine Main.tileSolid 拷贝，生成期翻转（137/130/225/192 窗口）不回写。
   live 读法把窗口期非实心族误入 ClearSlope 支保活性（vanilla 走 else 支清除浮空
   坡/半砖格）。pristine 三族差=sheet{19,239,380,427,435-439}+192+481-483。
   连带：vanilla 清除=active(false) 只清活性位（type/half/slope 保留），勿用
   setTileSilent(0) 连带清。#71 Pots(17079)/#72 级联归零。
3. **SpreadGrass 转化后级联**（Spread.ts）：cs:75286-75288 SquareTileFrame(i,j)——
   TileFrame 头清位+186/187 Check3x2（六格一致性/支撑行/样式组门/187→186 转化）
   +生成期 KillTile（**cs:63965 type=0**；尘掷全走 Main.rand 零 genRand 影响）
   +杀后 5×5 复扫。触发例：活树房间石堆第 6 格被活木 191 同帧覆写→残件 5 格。
4. **SurfaceOreAndStone y 掷上界**（SurfaceDecorPasses）：GenVars.worldSurface
   （Terrain 游走终值=274，TerrainPass.cs:235）≠Main.worldSurface（≈337=wsHigh+25）。
   GenState.genWorldSurface 是正确对应字段。连带五处 Next 边界值错（int(1,1) 恒+1
   ≠Next(2)∈{0,1}；int(1,2)∈{1,2}≠Next(3)∈{0,1,2}）——掷数同/值错更隐蔽。
5. **SolidTile2 严口径**（SurfaceDecorPasses 本地）：cs:70186 要求 slope==0 &&
   !halfBrick——坡面草上的倒木/堆放置 vanilla 拒（(405,230) s2 草实锤）。PilesPass
   自有严格版不受影响（SurfaceDecorPasses 曾"半砖/坡面放行"近似）。

## 移交与遗留

- #77：DungeonPass 墙画 240 帧 9 格全 f0,0（应逐格 +18 步进）→ Piles pass
  Check3x3Wall 首消费者杀除。修复属 LLLLL 域。
- wwwrep boundary（/tmp/www-b）帧通道对槽 74+ 已陈旧（修前管线捕获），尾段槽
  重放需重采或以全链 mile8 为准。
- TileRunner 内部 SAVE_SLOPES LUT 无 pristine 修正（理论隐患，本种子零触发）。

四链终态：9293480 0..76 绿；12345 首差 #62（基线同值）；s22222 #61（基线恢复，
JJJJ 在途落定）；m20260811 #62（最新态）——零劣化，尾段普降。
