# AAAAA：TrackGenerator 帧链 1:1（#101 残余尾 1% 处置）

接 XXXX 移交（van TrackGenerator.cs:136/151/158 TileFrame(frameNeighbors:true) 未镜像）。
对拍发现实际是**三链**：①循环一遍 KillTile=尘掷(RRRR 表)+击杀+尾部 SquareTileFrame
（cs:63967）——XXXX 未定罪但 'a 3' 苔藓掷大半在此；②cs:136 压板支 PlaceTile=
ClearEverything(墙/液体全清!)+PlaceTrack(20,-1)+SquareTileFrame 九宫；③cs:150-160
逐列 l<8/末列 m<playerHeight 五连 TileFrame(resetFrame:true)。JS 修（TrackPass.ts）：
killTileLane(尘掷全表复刻——killTileGen 私有,FinalCleanup 禁区只 import)+squareTileFrame314
(九宫=genSquareTileFrame+314 格补 frameTrack,两子系统零交叉可换序)+wuTileFrame 五连
字面镜像(tf314:314→frameTrack[零掷],余→genTileFrame)；退役"铺完统一 frameTrack"三循环
(等价论断撤销——van 链同时帧非轨道邻格且多轮 FrameTrack 时序不可交换)。HandleRopeEndFraming
生成期可证 no-op(GetRopeEnds 只停 inactive/绳格)；ResetToType 保墙清液体、线还原四色精确赋值。

验证：掷流 firstDiff 165353→**165546**(+193 掷逐条吻合)；帧位金标 102 .fr 路径吻合段
**48/50 逐位同**(2=路径分歧边界)。★残差定源**上游**：van 轨 y=735 直穿矿爆区而 JS 绕高
——金标出口实证 JS 411 起爆器 2×2 比 van 低一格(placeMiningExplosives findDown 首实心
低一行,掷不可见[411 杀零掷])→findPath **零掷**重路由→巷杀错位首曝掷流。矿爆段非轨道段
=域外移交。另一引擎缺口:case 138 巨石 Check2x2 缺(3 格 18,18vs0,0)移交引擎批。
工具资产:_wwwrep span 增 d/n 通道+rng.vanilla 'n'(SW_WWW_SPAN_DN=0 关);
★frtyp/.fr 是稀疏 (idx,val) 对/三元组数组——按格索引读=垃圾(本批翻车两次)。
mile8 9293480 0..62 绿;world-final-hash 常量待再生窗并入重基队列。
