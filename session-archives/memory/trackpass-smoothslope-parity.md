# 矿轨 TrackPass 全链终清（FFFFF 批 2026-08-19）

- **#101 轨道 314 全图 3991/3991 逐位全同**（CCCCC 移交 2397 差+golden 独有对角段全清）;A 8272→67/T 9157→69/L·Hf·Lt→0/Sl 1296→1;掷流首差 166921→223943（轨段全等）;残差=campsite 族+W 2178（CCCCC 域）。
- **定罪方法论**:自织金标副本（tttt-app 拷贝+Cecil 头钩:ND 栈迹/NB 定界栈迹/KT·SM 目标格观察）复跑 span 字节级相同;span 'd' 通道是 UnifiedRandom 类级钩——SoundStyle._random（独立实例）的音高掷会入流但零 genRand 消耗（plate 轨 PlaceTile(314,mute:false)→LegacySoundStyle 重载实参求值先于 dedServ 门）。'a N'≡'b 0 N' 同耗一样本必须归一比对。
- **根因链**:①AAAAA 省略的 Tile.SmoothSlope(cs:124/127)写坡状态——轨自身帧链立刻读它(ice sl3→gem 178 锚败杀,掷侧零差;JS 未写坡→gem 存活→多掷 Next(3)=首差真根);②KillTile.CheckTileBreakability 门(实心格上 PreventsTileRemovalIfOnTopOfIt 族整跳;树干本身非实心恒可杀=轨巷杀穿树干是原版行为,spawn-tree 测试加轨道巷豁免);③404 化石连锁可达(3×3 Next(15)/Next(4) 掷+递归);④Check2x1 内容掉落掷(185 frameX 带 Next(1,4)/Next(10,100) 条件族);⑤岩浆陷阱压板 PlaceTile(135) 尾 SquareTileFrame。
- **引擎缺口备案**(FinalCleanup 域,TrackPass 已本地规避):solidAllowSide 左右坡排除项各漏一项('L'应排{1,3}现仅2;'R'应排{2,4}现仅1);check2x1Sweep 185 掉落掷缺失;moss 184 frameY 写侧未写(掷侧已镜像)。
- **潜伏债**:TrackGenerator.TryRewriteHistoryToAvoidTiles 终评段——C# 第二 for 复用 num 终值=_length-num2(段 [_length-num2+1,_length-1]),JS 曾用第一 while 残留值多评一格。
- **Cecil 织入坑**:InsertBefore 缓存锚必须每条重取 Instructions[0](否则 call 排 ldarg 前=InvalidProgramException);TileFrame/Tile.slope 头钩在 Mono x86 卡死 hellforges(KillTile/Next 头钩无害);织入探针资产 /tmp/fffff-app+/tmp/fffff-patch。
- mile8 9293480 首差 #63→#64=并行会话清掉 (495,748) spider 债(两槽均在 pass 101 前,本批不可达)。
