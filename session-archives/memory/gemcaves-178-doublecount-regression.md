---
name: gemcaves-178-doublecount-regression
description: "#64 Gem_Caves回归三日记:UUUU引擎case178上线后placeExposed手写roll2/roll3成双计(+2幽灵掷/颗)全站漂移;被'GemPasses 03:16并行在途'误归因隐匿;金标基座反事实一步翻案+手写退役归引擎"
metadata: 
  node_type: memory
  type: project
  modified: 2026-08-19T10:48:57.854Z
  originSessionId: 0650e0c7-c14a-4b14-b89b-73780115946c
---

#64 Gem_Caves 回归（OOOO 清零→UUUU 引擎上线又红→LLLLL 归因清零，2026-08-19）。

- 现象：mile8 9293480 #64 A=317（WWWW 期 319=含 2 格蜘蛛继承债）；OOOO 曾清到
  八通道零。
- 定位：`SW_WWW=rep 64..64`（golden63 基座×现网 runGemCavesPass）复现
  A=317/T=953/W=2763 → **pass 自差**，FFFFF SmoothSlope/并行 Structures/HellFort
  等输入侧候选全排除。
- 根因：UUUU ④-4 给 FinalCleanupPass 引擎 frameImportantDispatch 加了
  `case 178: frame178Sweep(...,reset)`（cs:85844-85886 字面镜像，本身正确）；而
  GemPasses.placeExposed 的 manual roll2+GEM_DIR_BASE 基带+manual roll3 是引擎
  无 178 分派时代的补偿（旧注释"中心 178 引擎无分派 case = no-op"）——上线后
  两次 genSquareTileFrame 中心访各再掷 1×Next(3) → 每颗宝石 5 掷（vanilla 3）
  = +2 幽灵掷，首颗晶簇后全 pass 流移位全站错位（T0>178/T178>0 等量互换族）。
  #92/#93（placeExposed 同族）同病连带归零。
- 隐匿机制：UUUU 尾段全扫把 #64/65/92-94/103-105 红记"并行会话在途漂移带
  （GemPasses 03:16 mtime 实证）"——03:16 实为 OOOO 清零批落盘时刻。★教训：
  **mtime 新≠肇事者；先金标基座反事实分流"输入债 vs pass 自差"再定责**。
  UUUU 补 frameSparse 跳读表只救槽 57 重放路径，生产路径双计仍在。
- 修法（GemPasses.ts 单文件，引擎零动）：手写掷/基带退役改由两次
  genSquareTileFrame 中心访产出（列主序第 5 位=vanilla cs:80924 同序）；尾帧加
  `if (st.flags[pi])` 活性门（cs:60275 `if(tile.active())`，首帧被杀跳尾帧）；
  checkMultiDirAnchor 保留为 PlaceTile 前置门。
- 验证：#64 槽重放八通道零；mile8 9293480 0..64 绿首差→#65 Moss；12345（0..61
  绿，JJJJJ 并行域前进）/s22222（0..60）/m20260811（0..58=基线）三链前缀保持、
  #63→#64 delta=0；shimmer-checkpoint 首红 'gems'=runGemsPass(dump35) 非宝石洞。
- 残余关联：引擎 solidAllowSide 坡排除偏差（SSSS 遗留①）现是 frame178Sweep
  侧锚潜在残源（本种子零命中；侧坡锚若现 T178>0 即此因，归引擎域）。
