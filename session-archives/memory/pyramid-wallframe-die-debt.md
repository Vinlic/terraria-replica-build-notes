# 金字塔走廊 26v24 = 刷墙段 SquareWallFrame 掷债（ZZZZ 批定谳）

YYYY 阻塞项"golden 二进制 vs 反编译行为差"终审（2026-08-19，报告 ZZZZ 批章）：
s22222 金字塔走廊直段 vanilla 26 带 vs JS 24 带，根因**不是** Next(20,30) 骰本身。

## 根因链
- WorldGen.Pyramid 主体刷墙段（cs:27870-27888）每写一墙 34 调
  `SquareWallFrame(m,n)` → Framing.WallFrame(resetFrame:true) 在
  wallLargeFrames[wall]==0 时掷 **1×Next(0,3)**（wall==21 另有第二掷；墙 34
  非大帧墙≠21 ⇒ 恰 1 掷/墙）。s22222 计 **11025 掷**。
- JS 金字塔（StructuresPass.ts）镜像了写墙但**没镜像掷** → num8 之后全部骰序
  位移：num12（Next(20,30)）取流位 #6=23 而非 #11029=25 → 走廊峰值列
  2677+25=2702 vs JS 2700 → 出口隧道错路（y 496 vs 461）→ pre-temple 债 6154
  → 神庙锚 iter2 → ~100k 格级联。
- 三方证据逐位一致：①金标 dump 几何拟合骰向量 (d4..d9)=(1,5,25,16,8,25)；
  ②fresh(22222) 样本流 K-约束解命中 11025 且几何墙写独立重放=11025；
  ③双参 Next(int,int) 织入实测（/tmp/zzzz-span.txt）：PYRHDR 2686,228 →
  0,9,108 → **11025×Next(0,3)** → a2=1 → 5,8=5 → **20,30=25** → 16/8/25。

## 方法论要点（复用价值）
- **RunPass 每 pass 头 `Main.rand = new UnifiedRandom(_seed)`**（genRand=>Main.rand
  属性）——骰是 pass 局部的，跨 pass 流位移不可能；排查找 pass 体内。
- IL 直读两把快刀先行（Pyramid 骰序/边界 + UnifiedRandom.Next 数学），再织入。
- 织入 ret 钩：**先插 dup 再插 call**（后插者离锚近；反序=[call,dup,ret] 炸
  InvalidProgramException）；头钩 InsertBefore 每条重取 Instructions[0]（LIFO）。
- 0817 地牢/装饰同族教训重演：SquareWallFrame 掷语义 DesertPass.wallFrameDraw
  早有先例——**凡 PlaceWall/刷墙调用链都要查 Framing.WallFrame 的掷**。
- 勘误：PYR_TRACE 打印 k-- 前值（"k=229"非锚差，锚两侧同为 j=228）；mile8
  slot json 是对拍基线，复跑会覆盖（先备份）。

## 修复（移交协调者——StructuresPass.ts 并行禁区）
金字塔刷墙段写墙后补 `rng.int(0, 2);`（精确 diff 见报告 ZZZZ 批 ⑤）。
验证（/tmp 副本施加）：#40 金字塔 3269/6089→176/178（纯 #32 地牢债基线）、
#46 神庙 35639/62947/67415→176/178/0 级联全消、#105 终态 −28/−34/−70/−50%；
9293480 A/B 全等（无金字塔链零影响；四链中唯 s22222 建金字塔）。
