---
name: ocean-sand-hellfort-parity
description: 海里单体沙三根因修复(ShellPiles 锚点自创/顺序反/引力沙缺失)+地狱建筑只在中部50%是原版行为非bug
metadata: 
  node_type: memory
  type: project
  originSessionId: cb3a4729-b2a0-4330-a696-da1975f3392a
  modified: 2026-08-12T09:47:13.795Z
---

2026-08-12 用户报"海里单体沙"+“地狱建筑只在中间”。结论：

- **地狱废墟只在中部 50%(x∈[25%,75%])是原版行为**(1456 WorldGen.cs:32301-32304 普通世界跳过外侧 25%;drunk/remix 种子才反转)。三张原版真机 .wld 金标实测地狱砖 x 全落 1019..3091(4200 宽),两侧 1/4 区为 0。勿当 bug 修。已知小偏差:HellFortPass.ts 步长推进应只在成功放塔时跳(原版 32330),扫描上界 hellTop 原版无上界——未修。
- **海里单体沙已修三处**:① runBeachDecorPass 曾自创锚点+深度门放宽 worldSurface+120(原版 cs:16404 盒扫描找水线接触点+ShellPile cs:10338 下探>worldSurface 即弃),含原版右侧误写 shellStartXLeft 的复制粘贴怪癖(16468/16472,保留掷骰);② 海滩装饰从管线末尾归位到"水体沉降"后"半砖平滑"前(cs:16385<16507);③ 新增 GravitatingSandCleanup(cs:15198-15226,零掷骰,GravitatingSandPass.ts,Lakes 后 Shimmer 前)——ResetToType 不清 wall(wall 是独立 ushort 字段,Tile.cs:279)。
- shellStart 四变量由 runBeachesPass 记录(cs:14996/15025/15060/15090,水线分支首列),GenState 已加字段。
- 验证:seed 123456 孤立沙 5→0(剩 1 颗是沙-泥土交界贴水坑的正常地表);贝壳堆 36 格落水线;caves-checkpoint 首分歧 corruption 是并行会话在改 CorruptionPass(17:34 mtime),与本次无关;gem/loot/sky 9 测全绿。探针 scripts/_ocean-hell-audit.mjs + _shell-debug.mjs(注意探针里 world.worldSurface 不存在,要用 groundLevel 或 lastGenState)。
- 关联 [[vanilla-worldgen-passes]] [[vanilla-beach-plants-fix]]
