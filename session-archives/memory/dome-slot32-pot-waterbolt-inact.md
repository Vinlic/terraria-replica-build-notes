# MMMM 批：12345 #32 Dome 残余三根因（瓦罐支撑门/水书掷位/致动柱链）

- **主根因=PlacePot 支撑门语义**：`dgDungeonPot` 曾用碰撞语义 `genSolidType`（平台
  false）——vanilla `WorldGen.PlacePot`（cs:54082，:54099-54102）= **nactive()+
  Main.tileSolid**，平台 19 生成期 tileSolid=true（GenSolid `vanGenSolidType` 差集
  9 类）。Dome 平台罐全数失败 → 每罐漏掷 Next(3)（:54113 成功才掷）→ Platforms
  起全链掷位漂移（旗/挂毯/钟/画全错位）。Legacy 房/廊候选 IsAShelf=false 无罐
  路径 → 单种子绿掩盖。**教训：凡读 Main.tileSolid 的调用方必须走 vanGenSolidType**。
- **次根因=水书掷位**：`d.nowb === false` 对缺省字段（undefined）不成立——Dome
  下对平台候选无 NoWaterbolt 字段 → 整族漏掷 Next(50)（GenerateDungeonBook 默认
  重载参数位 DU:426-429）。JS 布尔字段判别禁用 `=== false`，用 `!== true`。
- **致动柱链**（与 LLLL HalfBrickPass 侧互证）：DungeonPillar.GenerateTileStrip
  :151-154/:200-203 `flag4→inActive(true)`（平滑后置）——JS dgPillarStrip 加 inact
  参（ClearTile 先清 bit5）；SolidOrSlopedTile/!inActive（WG:70046）→ solidOrSlopedD；
  SpreadWallDungeon 走 SolidTile（WG:70155 !inActive）→ dgSolid（W 776→0 即此：
  致动格非实心可传播）；灯笼/吊灯/桌面锚 nactive（cs:46705/:52769/:45360）。
  结果 Ia 234→0、Sl 8→0。
- **Dome/Tower 入口盒特性门**：DomeDungeonEntrance.cs:31-38≡Tower:31-38 拒
  Bookshelves/Paintings/Spikes（hitbox 内；基类另拒 BiomeChests=任何入口）——
  JS 补 `entNoFeat`（entKind!==0）于 spikeRun/书架门槛/featArea3 三点。
- **验证**：12345 #32 八通道全零、#33-46 连带绿、#53 塌缩 93%（余项=上游祭坛
  6 格级联，LLLL 反事实证净输入下=0）；9293480 0..53 全绿（Legacy 结构性无操作）。
  Tower 支同修未验（双链无 Tower 种子，矩阵 s33333 复扫）。
