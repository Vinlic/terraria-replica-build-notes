---
name: kkkkk-campsite-mahogany-engine
description: "#101槽全零批：引擎solidAllowSide左右坡各漏一项(L排{1,3}/R排{2,4})+check2x1Sweep补185六带掉落掷+尾双SquareTileFrame；campsite四根因(Place3x2中心锚/篝火+36帧/倒木地面门错行/金币堆无门覆盖写)+mahogany三链漏wall清(W2178)；moss184帧写侧查证已收敛(FRAMES解析双布局坑)；新派发CheckAlch/CheckJunglePlant/Check2xX三击杀族"
metadata: 
  node_type: memory
  type: project
  modified: 2026-08-19T11:28:11.922Z
  originSessionId: 0650e0c7-c14a-4b14-b89b-73780115946c
---

KKKKK 批（2026-08-19，接 FFFFF 备案）：#101 Micro_Biomes 槽八通道 A 67→0/T 69→0/W 2178→0/Sl 1→0 全零。

- **引擎 solidAllowSide**（cs:70345/65+Tile.cs:340-355）：LeftTileAllowLeftSlope 排 rightSlope()={1,3}、Right 排 leftSlope()={2,4}——曾各漏一项（L 仅排 2/R 仅排 1）。影响 frame178/129 全消费端。
- **check2x1Sweep**：杀后补 185 六带内容掉落掷（cs:47137-232：576-610 明胶 12 掷族/612-46 银/648-82 金/684-898 六带 Next(1,4)——noItem 无产物但 genRand 堆叠实参先求值必耗掷）+尾双 SquareTileFrame(cs:47366-68)。TrackPass 本地表同源收编。
- **campsite 四根因**（CampsiteBiome.cs）：①PlaceTile(215/186)→Place3x2 **中心锚 [i-1..i+1]×[j-1..j]**（cs:52097），曾左锚 +1 位移；②篝火 Place3x2 后六格 **frameY+=36**（未点燃行 36/54——旧批修"行反"时误删）；③倒木地面门曾错查对象自身底行（应 y+1 行 SolidTile2+Boulders 排除）；④金币堆 PlaceTile(332) default 支**无任何门覆盖写**（只写 active+type 帧墙液保留，曾自造 !active+实心下门）+尾 SquareTileFrame+生成期 488 早退。
- **mahogany W2178**：Actions.SetTile 默认 clearTile=true=tile.Clear(~(Wiring|Actuator)) **连墙清**——branchCell/叶球/rootCell 三处漏 wall=0（干身本有）；带=基座预置墙 64×1150/花岗岩 180×1385 golden 清 JS 残留。
- **新派发三击杀族**（文件头"零击杀证据"备案陈旧作废）：CheckAlch 82/83/84（frameY 无条件复位+列 0-6 地基表+列 5 岩浆成熟 82/83↔84）/CheckJunglePlant 233/236/238/702（2×2 mod2 锚+3×2 mod3 锚，**3×2 杀循环行数 3 原文如此**）/Check2xX 26 id（465/531/591/592 顶锚族+余底锚）。尘掷零（num 择取全确定性）。frameSparse 跳过表同列扩充（C3X2 同款防嵌合伪杀）。
- **方法论坑**：①FRDUMP .fr 是 u32×3 布局、金标 .fr 是 u32+u16×2——混用解析出"13k 帧差"假象（FFFFF moss 184 帧写备案即此伪影，实际 pass 内重写 8 格全=golden 演化值）；②mile8 s22222 金标是猩红世界须 SW_M8_EVIL=1（evil=0 首现 #26 Shinies 邪矿石带≠回归）；③残差归因先查"基座在、金标杀"（=击杀级联缺口）vs"基座在、金标无"（=放置位移）。
- 验证：#105 基线 A=215/T=260 逐字同；mile8 四链零回退（9293480 #65 基线原样/12345 全绿/s22222 #61/m #62 前进）；48/48+40/40+全量 worldgen 域零真回归（tests/boulder-trap.test.ts 并行 WIP 语法错曾炸全量 transform）。
