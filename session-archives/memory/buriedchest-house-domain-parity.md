# JJJJJ 批：m/s 双链 #59 Buried_Chests 清零（屋域七件）

m20260811 A=21,792/s22222 A=19 → **双链八通道全零** + m 链掷签名流 93,918 行逐位全对齐。
方法论=金标掷签名流直注（tttt-app `SW_TT_SPAN_PASSES="Buried Chests"`——pass 名带空格，
CS 标签名不命中！）vs JS 原型包装流，规范化后逐行 diff 首差定位+roll 索引栈迹 ctx 落位。

七件根因（全 vanilla 字面对照定罪）：
1. **蘑菇 flag7 双支位形**：洞穴支 cs:37007 在主件 if/else 外（双路径共享 if/else 单掷）；金支 cs:36689 是两道独立 `flag7&&` 门（1/2 矿车+1/3 三件套可同中）——曾均错置 mainId 分支内 → 无主件蘑菇箱漏掷 1 → m 链屋链整体位移。
2. **'er' 邻帧**：PlaceEmptyRooms 壳 SetFrames(frameNeighbors:true)/腔 ClearTile(frameNeighbors:true) 都带 TileFrame 分派击杀链+尘掷——houseFrameDispatch（引擎+屋域补件）；kstage 扫与内联并存（s 链 484 对仅内联漏杀实证）。
3. **木屋 aging 邻帧**：木① SetTile(51,setSelfFrames:true)/木③ ClearTile(frameNeighbors:true) 接 frame 位（蘑菇② SetTile(71) 裸写不帧勿泛化）。
4. **屋域补件族**：105/349/12/巨石族(含 484，引擎只派 138/411)/Check3x3 族{219,220,228,231,243,247,283,300-308}(cs:86744,引擎缺；231 幼虫 !tileSolid[225] 窗口特例 cs:53158)。
5. **宝箱预清场**（TileObject.cs:79-90）：箱体 cut/Breakable 先 KillTile（尘掷表+51&墙62 补 Next(4) cs:63904）+尾九宫引擎级联。
6. **门/485 kfCheckObject 派发**：case10 CheckDoorClosed(四座门杀=木③清格邻帧击发)/case485 CheckSuper。
7. **吊灯尘掷界**：34/42 族=Next(2)（cs:69069）非 Next(3)——DDDD 只实测掷数未校界。

坑与裁定：
- s 终态 W 16k→59k = #63 蜘蛛波对 #62 水箱残带构型变化的非线性放大（新旧 #62 核心 pairs 逐对相同=既有债；m 链零 W 增量）；根因在 OceanCaves/HiveSpider 域非本批。
- tttt-app Next(0,N) 单参重载显示 'a N' ≡ JS 'b 0 N' 须规范化；d 通道 vanilla 无钩。
- 四链终态：s/m 首差 #62（水箱域）；9293480 #73；12345 #62。液体 60/60；全量新红 8 文件隔离 32/32 绿（互扰带）。
