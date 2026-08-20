---
name: visual-defects-corruption-fix
description: 腐化区三缺陷定案:石锥风格=原版无腐化变体(非bug);黄玉悬空=TileFrame178方向基带缺失已修;暗影球缝=DRAW_Y_OFFSET 31:4无据已摘;冰锥=DesertPass placeDeco误用已改placeTight
metadata: 
  node_type: memory
  type: project
  originSessionId: 4a66e745-9d91-4188-8ade-1e2b7775e8b4
  modified: 2026-08-13T06:11:01.650Z
---

腐化区视觉三缺陷 + 冰锥定案（08-13，两代理取证 + 修复，构建绿+单测4/4）：

**A 石锥风格（用户翻案成功，已修）**：代理首判"原版无腐化变体"是**错的**——它只看了 PlaceUncheckedStalactite（:38352 生成时表：25/203 并入灰柱 54）。但 1.4.5.6 有**第二套重定型系统**：PlaceTight :38346 放完即调 CheckStalactite（:39022）→ UpdateStalagtiteStyle（:38690）→ GetDesiredStalagtiteStyle（:38746）按锚定材质映射专属列——**25 黑檀→style2→fx270 腐化款、203 猩红→style3→fx324 猩红款**（用户人工核对素材发现）。完整映射（合并两表）：1/苔→54（挂藤墙62→108）｜117→216｜25→270｜203→324｜396/397→378｜368→432｜367→486｜147/161→0｜163→594｜164→540｜200→648｜225→162（仅单格）。修：ShimmerPass placeUncheckedStalactite 重写为 BASE() 查表（垂挂+地面两路），死代码 ICEY/STONY/逐族 if 链移除。**教训：审计代理只读生成端函数就下"原版没有"结论不可靠——用户看素材/玩原版的直觉优先**。

**B 黄玉悬空（真 bug 已修）**：根因≠锚定门失效（黑檀石是合法锚，这颗以**左锚**通过）——是**TileFrame case 178（:85844-85882）方向基带缺失**：原版 PlaceTile 178 丢方向后紧跟 SquareTileFrame 重写 `frameY = 基带{下0/上54/左108/右162} + 变体`；本仓只写了变体 → 全部 178 永远落地帧，侧锚/顶锚宝石渲染成悬空。修：GemPasses checkMultiDirAnchor 返回方向（0下/1上/2左/3右）、placeExposed 写 `GEM_DIR_BASE[dir]+Next(3)*18`。

**C 暗影球缝（真 bug 已修）**：世界数据完美（连续 2×2 @3262-3263,511-512；我早前"水平错3列"是 token 索引被 RLE 干扰的误读）。根因 = VanillaTiler `DRAW_Y_OFFSET 31:4`（连同 12:4）**无原版依据**（36px 动画组 TileDrawing.cs:5524-5529 只设 addFrY、tileTop=0）+ ChunkCache tile 层 256 严格无外扩：+4 遇球骑 chunk 行边界 → 上半底 4px 被裁、下半再 +4 → 中线 4px 暗缝（像素实测 107→46→102）。修：摘 12:4/31:4 两项。防御项登记：tile 层 EXT 外扩、其余正值偏移（428:4 等）同型风险。

**冰锥（真 bug 已修）**：v_165_cave_decos 是**误标**（vanilla 165 = Icicles 冰凌）。根因 DesertPass AddTileVariance 误用 placeDeco（底锚上行帧分配器）：①倒挂形帧行颠倒（fy=18 锥尖在上、fy=0 基座在下 +4px 断缝）②冰列 fx=0 画进地下沙漠（蓝冰锥挂沙岩）。修：改走 `placeTight`（ShimmerPass 1:1 完整移植：邻接材质分派 396/397→沙岩列 378+var*18、帧序 0/18 倒挂/36/54 地面/72/90 单格），锚点 `py+(flag?-1:+1)`（DesertHive.cs:491）。死代码 T165 摘除。遗留：placeTight 后的 CheckStalactite（:38346）未实现（风格一致性，不影响错位）。

**Review 全仓扫描（08-13 收尾）**：165 写入方全量盘点六处——ShimmerPass placeTight（主 1:1 ✓）、DesertPass（已改走 placeTight ✓）、GemPasses 4 调用（走 placeTight ✓）、HiveSpiderPass placeTightWebs fx108（=原版 `spiders:true` 分支逐字 ✓）+ 蜂巢腔 fx162 蛛网（225→style12 ✓）、**MarbleGranitePass 本地版只写 type/flags 不写帧（大理石/花岗岩洞全渲染 fx0 冰柱底座）→ 摘本地实现委托 ShimmerPass（导出 placeUncheckedStalactite 供私有流调用点）**、CaveHousePass 冰族与 WorldEvolution SNOW_FAMILY 两处把 163/164/200 全写 fx0 列 → 按重定型表改 594/540/648 专属列。审计豁免表（audit/exemptions）一处登记无需动。构建绿+单测4/4。

**教训**：①debug rows 的 token 索引≠真实列（RLE `*N` 压缩），跨行对位必须逐 token 展开累计；②贴图帧 bug 先像素级测量定位（截图内嵌 PNG 解码 + 亮度剖线）再下结论。

相关：[[loot-parity-audit]]、[[gem-anchor-gate-port]]
