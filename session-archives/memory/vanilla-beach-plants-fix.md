---
name: vanilla-beach-plants-fix
description: 杂草草族门禁+贝壳堆/海藻 pass+螃蟹确认+蘑菇采集掉落（双地图对账驱动）
metadata:
  type: project
---

2026-08-10 海滩/植物系统性对齐（用户给原版导入图 vs 自产图 JSON 对账驱动；对账脚本
思路存 [[vanilla-names-i18n]] 审计模式——vitest 临时测试 import TILE_DEFS 全图扫描）：

- **杂草规则**（WorldGen.ts surfacePass 内）：1:1 原版 pass GrassPlantsEvilPlantsAndPumpkinsOnSurface
  （WorldGen.cs:20201）+PlaceTile 液体拒绝（59477）。门禁=草族限定：普通草 2→tile3 变体
  （草6/花9/蘑菇144）、腐化草 23→24（13%荆棘32）、猩红草 199→201（13%荆棘352）、
  丛林草 60→73、蘑菇草 70→71（**发光蘑菇株 v_71×~1000 与原版 ×1085 规模吻合**）。
  沙滩/海水自然无杂草（此前任意实心块上方都长）。
- **贝壳堆**（BeachPass.ts runBeachDecorPass）：ShellPile 1:1（L10307：椭圆随机漂移填
  v_495+下探补沙/硬化沙）；锚点须全列扫沙面（固定窗口会漏真实海盆深度——E2E shell=0 的根因）。
  **海藻 v_549**：沙面+上方 4 格全满水才放（GrowCheckSeaweed 深水条件），2/3 门。
  pass 注册名'海滩装饰'（vanillaBeachDecor 桥接 ctxGs）。
- **螃蟹**：原版 Crab 67 是敌怪（伤20）——VanillaSpawner 海洋段早已 1:1（N(3)→67），
  E2E 数 0 是因为只数了 critters 桶。补海鸥 602（L1767 水面干格 1/10，critter:true）。
  CRITTER_DEFS 里另加了 crab/seagull（spawnCritter 兜底路径，oceanOnly 门防进沙漠）。
- **蘑菇采集**（Game tileCut 分支）：KillTile_GetItemDrops（65041）：tile3 帧144→item5
  mushroom_item、tile24 帧144→vi_60、tile201 帧270→vi_2887。
- 帧表：NPC_67 螃蟹 8 帧@34px、NPC_602 海鸥 15 帧@36px（透明带探测法）。
- 遗留：水中仍有少量杂草（草地被水淹，原版 12200 我们 ~100-250，合法）；滴水石 373/374
  与蘑菇藤 528 未生成；贝壳堆掉落（5490/5491）未接。

**雪原植物门禁(2026-08-13,用户报"杂草花长在冰雪环境")**:原版
GrassPlantsEvilPlantsAndPumpkinsOnSurface(WorldGen.cs:20209-20260)只认 草2→杂草3/
腐化草23→24/猩红草199→201,**雪 147 无任何植物分支**;Flowers(:20592)也只转草上的草。
根因=runSurfaceDecorPass 门禁误含 SNOW;已移除。验证陷阱:雪面上 1.1 万格"异物"
直方图实为【冰块(雪原合法叠层)/泥浆块】——排查时先按内部 id 直方图归因再断言
(泛化断言"雪上非雪活性块"会误报地形叠层)。回归 tests/snow-biome-plants.test.ts
(同种子 12345 实跑断言 19/20/21 内部 id 零命中)。

**全群系体检(2026-08-13,/goal)**:方法论=全图"地面sheet→上方块"直方图归因(排除同 sheet 叠层与
地形噪音),逐群系对照原版 pass 语义。结论(修复 SNOW 门后全绿):
- 雪147/冰161:无草花菇;185/186/187 堆饰**合法**(原版 Piles :19099 雪/冰/薄冰→style26-31 冰样式)
- 沙53:滚动仙人掌484/海藻549/燕麦529/贝壳堆495/沙岩族 ✓;无草花菇
- 丛林草60:短植物61/藤62 ✓;蘑菇草70→蘑菇植物71 ✓;地狱灰烬草633→637/638/灰烬树634 ✓
- 邪恶:猩红199→201 ✓;腐化(强制 evil:0)23→24 ✓(其余=堆饰/香蒲/荆棘/腐化藤/树,全合法)
- 草2:短植物3/花73/蘑菇/香蒲519/树 ✓;dirt 裸露属地形
回归 tests/snow-biome-plants.test.ts 扩两断言(雪沙冰禁植物+两邪恶侧必生邪恶植物,三世界实跑)。
临时直方图脚本已清;需要复查时按"ground sheet→above 直方图+内部 id 归名"重建。
