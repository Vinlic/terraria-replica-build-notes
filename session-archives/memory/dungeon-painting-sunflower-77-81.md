# PPPPP 批（2026-08-20）：#77 墙画帧+#81 向日葵三连根因清零——9293480 首差 #77→#83

- **#77 墙画帧债**（DungeonPass 帧级解冻）：Place3x3Wall/4x3Wall/6x4Wall 三族
  帧公式互异（3x3=style 双基分解 X=余*54/Y=商*54；**4x3=style 只进 Y**、X 纯列
  偏移；6x4=27 进制 X=⌊s/27⌋*108/Y=s%27*72）；paintingEntry 返 {tile,style}
  掷序不变；PlaceTile 尾 SquareTileFrame 对画族=no-op（画块全 frameImportant，
  Check*Wall 一致即返）勿镜像。JS 杀除逻辑（check3x3WallSweep）本就忠实。
- **#81 向日葵三连根因**（SurfaceDecorPasses）：①cs:53683 先掷后覆盖——
  l<=-2 每格 Next(3) 照耗（**9 颗非 5**）；②**列扫上界独占** `j<num3`（JS 曾
  j<=hi 多扫末列→band 末列多放整株→流错位→末带两株全丢）；③趟数 double 语义
  `(double)i<8.4`=9 趟（Math.floor=8 错）；④PlaceTile 前奏液体门+锚格清位。
  连带 #82 Planting_Trees 3028 格级联全愈（上游流归位即自愈）。
- **#83 草药海滩门**（撞 StructuresPass 并行域止·移交）：PlaceSuitableHerbHere
  style-4 沙族支 `x∈[beachDistance,w-beachDistance]` 门（cs:45971）JS 缺——
  4 株全在海滩沙上；修=plantAlch 分发循环 style===4 支补 beach 门一行。
- **TileRunner SaveSlopes** pristine 三族差并集（平台/192/481-483）补齐=本
  种子零触发口径债清偿。
- **方法论新资产：金标基座参数化模拟**——dump(N-1) 六通道直装 sheet 空间 +
  pass 流重放（RNG(seed).reseed 同 RunPass）+ 参数面暴力扫描（掷数×趟数×ws）
  → 复现 vanilla(N) 写集全等即定谳；全程零金标写入。genRand=>Main.rand（
  WorldGen.cs:4391 属性别名——RunPass 的 Main.rand=new(_seed) 即 genRand 重播）。
- 四链与 OOOOO 批共树终态逐值一致（三链首差 #73/#63/#69 全=OOOOO 报告值，
  本批零扰动）；9293480 逐槽对比 NNNNN 终态零劣化。#84 H0>1×13（active
  dirt/stone 地下格 DyePlants 期 vanilla 清 half JS 未清）为下批独立小债。
