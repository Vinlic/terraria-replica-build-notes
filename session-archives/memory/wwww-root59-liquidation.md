# WWWW 批：#59 百格级根清偿（193→0）+ 帧杀级联引擎 + #89 藤归零 + 9293480 首差 #59→#63

接 YYYY 归因（装饰位漂 4.3M 脊柱）。docs/worldgen/content-parity-vs-vanilla-2026-08-16.md WWWW 章。

## 根清偿四修（全部 CaveHousePass 域，golden 实证）
1. **HouseBuilder FillRooms 陷阱雕像 = 无条件调**（HouseBuilder.cs:483-491：
   PlaceTile(105) 失败也调 PlaceStatueTrap；Statues pass cs:17045 相反=成功门内
   才调——两处语义相反勿互搬）。曾关进成功分支 → 4 屋漏陷阱+45 格漏线 → ±25
   红线扫描翻转全链。golden wire 对拍定位（TTTT 060 wire 快照 45 格 js=0）。
2. **AgeRoom 钟乳石 = 全族**：沙漠 396/397→378 列/花岗岩 368/大理石 367 都放
   （曾"仅冰族"局部近似漏 135 格）；用 ShimmerPass 全量 placeUncheckedStalactite
   替换局部副本。
3. **梁写 SetTileKeepWall=Clear(~(Wiring|Actuator))**：清液体/坡/半砖+梁底格
   slope/half 复位（78 格梁带水 L/Y 差根因）。
4. **跨物件帧杀级联引擎 frameKillSweep**（54 格终清）：vanilla 带帧写（PlaceTile
   尾 SquareTileFrame 九宫/SetFrames(frameNeighbors)）触发 Check2xX/Check3x2/
   CheckPile/Check2x2/CheckOrb/CheckStalactite 整盒击杀；**触发面=带帧写阶段**，
   蚀变裸 SetTile 不触发（(2634,479) 三格残破仙人掌存活实证）；杀=KillTile 生成
   期（noItem 零掷+type=0+清 half/slope）。**杀全族零掷的铁证：#60-62 全绿（流
   对齐）**。修后小屋序列 42/42 与 van_houses.json 对齐。
- 金标反事实方法论：SW_WWW_59G 注入 fr/wire/chest 全不动 → 输入债排除，定罪
  写侧（TTTT 织入产物是 pass 头快照三通道，可复用）。

## 放大器裁决
- #71 罐 golden 基座重放**零自因**（勿修）；#89 藤 6 格自差两修归零（putVine 的
  ClearSlope=清 slope+half 双轴；蜂巢凹龛 KillTile→九宫 CheckVines 级联——失锚
  整列下杀 cs:85599-85698）。

## 小项与移交
- 12345 #54 Hf=1 单差 (3845,1045)：golden53 基座重放精确复现；修两处幽灵半砖
  保真（loop1/loop2 active()&&halfBrick 双门）但单差仍在——vanilla 侧掷流织入
  才能定位（YYYY 金字塔同类阻塞）。湖体±255=维持 m 链 #32 地牢债级联定谳，
  移交 XXXX。

## 战果与陷阱
- 9293480 全管线首差 #59→#63（2 格=XXXX placeTightWebs 域）；12345 #59 128→12；
  m2222 矩阵 typ-11.6%/wal-44.7%（装饰漂塌缩实证）；**s12345/l9293480 矩阵恶化
  ≠本批**——panorama 定位在 #100-105 段（XXXX MicroBiomes/DungeonPass 在途编辑
  窗口），本批域 ≤#99 全改善。矩阵横比必须记录并行会话 mtime 窗口，否则误归因。
- mile8 尾段红集：#63=2+漂移带（GemPasses/Piles/FinalCleanup 等 mtime 实证）。
- worldgen 域真回归零（3817 例 35 败全 KKKK 在案带；隔离复核 npc-liquid/paint/
  hive 绿=他批探针 import 副作用）。液体 60/60。
