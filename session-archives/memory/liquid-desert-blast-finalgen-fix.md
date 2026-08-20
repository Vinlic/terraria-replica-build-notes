# QQQQ 批：#49 Lt=1 清零——finalGenMergeCheck 误带 LavaCheck 沙漠 blast 前导（12345 链 0-53 全绿）

- **症状**：12345 链 #49 Settle_Liquids 单格差 (1982,661)：JS 把密闭水袋转岩浆，
  vanilla 恒水（golden 48→49 逐位同）。
- **取证**：水袋四邻全活石；(1981,660) 对角密闭岩浆+向上密闭岩浆斜梯
  (1978,657)…(1981,660)；区域密布 187 沙岩墙。密闭格不满足 WaterCheck 入列
  任何条件→update/DelWater 的 LavaCheck 不达；settleWaterAt 无下落、
  AttemptToMoveLava 四邻无液→不火。vanilla 全程无人对斜梯调 LavaCheck→
  7×7 沙漠 blast（Liquid.cs:1457-1465）不火。
- **根因**：JS finalGenMergeCheck 岩浆分派走 lavaCheck（=blast 前导+LiquidCheck(1)）；
  原版生成收尾全图检查（WorldGen.cs:22639-22650）**直接调 Liquid.LiquidCheck(
  x,y,type,createMergeTilesDuringGen:true) 不经 LavaCheck 包装**。全图扫把密闭
  斜梯岩浆格当 blast 源→(1979,658) 首个覆盖水袋→水→岩浆。
- **修**（LiquidSim.ts 两处）：`lavaCheck(x,y,desertBlast=true)` 参化 blast 门；
  finalGenMergeCheck 传 false。update/DelWater/attemptToMove 三原版调用点不动。
- **★方法论**：①"finalGenMergeCheck 0 块一致"验证只覆盖落块通道，blast 的
  **类型平写**副作用当时不在验证半径——补验证须同时看 Lt 通道；②Tile.lava(true)
  =平写类型位（(b&0x9F)|0x20），非 OR 位或——JS 平写 liquidType=2 本正确；
  ③密闭液体格（四邻实心）的唯一可达写者=blast/strip 类区域写，排查先列
  liquidType 全部写入者再逐一问"vanilla 谁会调到它"；④mile8 第二种子须
  `SW_M8_G2=/tmp/sw-slp/g12345`（缺省 g=9293480 会全图假红）。
- **验证**：12345 链 0-53 全绿（双链里程碑）+9293480 零回退+液体 4 套件 60/60
  （A/B 冻结哈希不变——夹具无沙漠墙 blast 本死）+caves 首差 underworld 原位
  +全量 31 红=KKKK 在案带+并行在途（vanity-equip×4/hive 满载 flaky 隔离绿），
  worldgen 域真回归零；tsc src/ 零错。
