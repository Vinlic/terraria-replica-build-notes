---
name: statues-sweep-port
description: m/s链#58清零=PlaceTile case105尾SquareTileFrame无条件级联(惰性帧校验杀165/187/485/484)+flag2双门/幻影成功/陷阱Boulders门;484本地补件(HalfBrickPass同源惯例);零帧帧债垫片勿泛化(活树零帧/187 styleCol门);spawn-tree红=#32 Dungeon债×TrackPass放大非回归
metadata: 
  node_type: memory
  type: project
  originSessionId: ggggg-batch-2026-08-19
  modified: 2026-08-19T08:34:45.696Z
---

m20260811/s22222 链 #58 Statues 清零（GGGGG 批 2026-08-19，接 DDDDD 移交）。

**根因**：vanilla PlaceTile case 104/105/349 臂（cs:60088-60101）＝`Place2xX; SquareTileFrame;`——**尾九宫无条件跑（放置成败都跑）**→ TileFrame→frameImportant Check* 惰性帧校验：放置前从未被帧到的孤立残件（165 悬空钟乳/187 沙堆/485 蚁狮巨石/484 巨石半组）首次被雕像尝试窗口命中即整组杀。JS StatuesPass 缺整步→残件保留+后续尝试成功位翻转→尾部雕像/陷阱错位（放置集对拍 1344/1344 全同证流零漂移，残差纯杀级联）。

**修复四件**（StatuesPass.ts，引擎复用 FinalCleanupPass.genSquareTileFrame）：
①statueFrameSweep 每次 PlaceTile 等价尝试后无条件调；②flag2 双门 cs:17024-28（锚 active&&frameImportant&&!tileCut→拒；anyShimmer→拒——曾只跳过清锚还继续放）；③幻影成功 cs:17029＝PlaceTile 后回读锚格 active&&type==x（随机 y 落既有同型雕像体内也推进 num+触发陷阱）；④placeStatueTrap 补 Place1x1 Boulders 底座门（cs:45213）+尾 SquareTileFrame+回读 tile2==135 才拉线（失败续扫）。CaveHousePass placeStatue 共享（HouseBuilder→PlaceStatueTrap 同源）。

**484 本地补件**：引擎 Check2x2 只派发 138/411（CCCCC 批），484 在场（s 链 (2407,807) 半组）按 HalfBrickPass 同源副本惯例本地补 check2x2Boulder484（boulder 支/零掷/杀尾九宫走引擎/嵌套 484 四×四尾窗再扫）。

**零帧帧债垫片（{240,440,88}）**：JS DungeonPass chTile/dgWr 全陈设 type-only 写（NNN 只补过 banner 91）→ 零帧组必假杀（vanilla 有效帧保留）。垫片写自洽 style-0 帧型。★**勿泛化**：活树树干亦全零帧（改写炸 #82 栽树链——spawn-tree-regression 实锤翻车过）；186/187 地基门读 styleCol（style-0 翻判据）不垫。族域=引擎读帧完整性且 style 无关的成员。

**裁定**：237 蜥蜴祭坛杀=vanilla 真——cs:16782 FragileIce 头把 226 翻非实心（cs:17076 才回），statues 期 SolidTileAllowBottomSlope(226)=false（PRE 态逐通道取证+隔离重放双向验证）。spawn-tree-clear 测试红=非回归：为该种子现制金标 /tmp/sw-slp/g-sptree（106 槽），vanilla x=2936=[627] 全图病理 0 命中，JS 本就深偏（PRE/POST 首差均 #32 Dungeon A=2311），写者=TrackPass(FFFF 在途域)。

**战果**：m/s #58 八通道全 0；首差均→#59 Buried_Chests（m A=21.8k/s 19 格=屋域放大器债移交）；9293480 #63/12345 #54 基线逐位原样（附产 12345 #58 5→0）；液体 60/60。教训：FFFF 并行编辑窗口会撞半存态（squareFrameTrack 崩）——验证须等其 mtime 稳定后复跑。
