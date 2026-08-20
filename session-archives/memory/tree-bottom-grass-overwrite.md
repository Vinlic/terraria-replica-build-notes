---
name: tree-bottom-grass-overwrite
description: 无根树终审(2026-08-18 GGGG推翻2026-08-15旧裁决):Flowers杀干基后原版经KillTile尾SquareTileFrame→TileFrame case5→CheckTree整树坍塌——原版无"断一格站立的树";旧裁决只核到KillTile漏了级联;JS已1:1补级联(killTileTree);零genRand;x86实测231/219干列地面全实心族
metadata: 
  node_type: memory
  type: project
  originSessionId: c44574b3-7d4d-403b-8e39-61a13d11a1c6
  modified: 2026-08-18T11:13:23.389Z
---

树干底格被草占/"无根树"终审（GGGG 批 2026-08-18，**推翻本文件 2026-08-15 旧裁决**）。

**旧裁决错在哪**：旧文核对了 Flowers pass 五环（pass 序/列窗/tileSolid 放行/
allowOver 怪门/KillTile+PlaceTile）——这五环本身都对，但**漏了 KillTile 的尾部
级联**：原版 `KillTile(m,n)` 尾部 `SquareTileFrame(i,j)`（cs:63947→80924）→
3×3 `TileFrame`（cs:82067）→ tileFrameImportant case 5（cs:86619）→
**CheckTree（cs:54598）**：干基被杀后上方干身"下方支撑失效"逐格上杀、侧枝/
根须按邻干判定连杀 = **整树坍塌**（与游戏内砍树同一机制）。净效果不是"树断一格
站着"，而是**整树消失 + PlaceTile(3) 在原干基位放草/花**。x86 实测铁证：
s12345.wld 逐列扫干（连续竖跑≥3）219 列，干底地面格全实心族
{2:98,60:60,70:19,147:17,199:25}，**零 73/3 垫底**——若原版留断树必有垫底列。

**JS 修复（SurfaceDecorPasses.ts，GGGG 批）**：Flowers 击杀位 `killTile` →
`killTileTree`（杀 + 3×3 列主序帧扫）；`checkTreeAt` 1:1 移植 CheckTree/
CheckTreeWithSettings(Vanity 596/616) 全规则链（R1 直干支撑杀/R2 根须贴干/
R2else 侧枝重帧/R3 基座帧/R4 侧枝贴干链/R4else2 无下杀/R4else3 孤立重帧/双帧
变尾传播）；帧读写走 cfx/cfy 虚拟值（Uint16 存不了 -1，死格重帧只影响尾部传播
判定）。★曾栽的坑：num4 忘 +1（读了本格不是下方格→R1 的 num4!==self 恒 false
级联全不触发）——单元合成树先验证再上管线。级联**零 genRand**（尘埃走
Main.rand；type 5/3/73/185-187 分支无掷点）→ 掷流不动，状态对齐 vanilla。
genTrees 登记表同步修剪（基座失活=树已亡）。

**验证口径**：seed 12345 小世界——修复前 Flowers 后 9~15 列 `87/2→86/73` 型
（干基被花草替换+整干浮空一格）；修复后 bad=0，地面直方图全实心族，
Flowers 槽干列 159→150（=被击杀树坍塌数）。M8 槽 0-53 不受影响（Flowers=
原版槽 ~90 在 M8 dump 范围外）。树列错位（JS 150 vs x86 219）是尾段上游债
级联（槽 54-105 在途批），非 Flowers 自因——清单在
game/docs/worldgen/content-parity-vs-vanilla-2026-08-16.md GGGG 章。

**残留备案**：棕榈 323（只长沙族、花圃门要求下方草）与宝石/灰烬树（地下/地狱
不可达）不派发级联——本域恒 no-op；529/530 邻接重帧为存量近似（稀有零掷骰）。
