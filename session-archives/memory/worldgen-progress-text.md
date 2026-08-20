---
name: worldgen-progress-text
description: 创建世界进度文案原版化:worldgenKeys 全量重写(54槽全覆盖+5错值修正);权威=awk配对AddGenerationPass↔progress.Message
metadata: 
  node_type: memory
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-13T05:20:41.168Z
---

2026-08-13 用户问"创建世界的文本是否对齐原版"。发现机制早已存在(UIWorldLoadState.setProgress:54 → Lang.worldgenText → worldgenKeys 数字表),但映射表只覆盖 20 槽且 **5 处错值**,30+ 槽显示自造中文。

**权威提取法(可复用)**:`awk '/AddGenerationPass\(GenPassNameID/{name=$0} /progress.Message = Lang.gen/{match($0,/gen\[[0-9]+\]/); print name " => " substr($0,RSTART,RLENGTH)}' WorldGen.cs` — 全量 pass↔gen 键配对,勿凭记忆/语义猜(TerrainPass 的文本在 TerrainPass.cs:59 而非 WorldGen.cs)。

**5 处错值修正**(语义猜错的教训):
- '液体' 27→**19**(Lakes=正在添加水体;27 是沉降)
- '地狱屋' 36→**30**(36=地狱熔炉;UndergroundHouses=30 隐藏宝藏)
- '表面' 89→**37**(89=放置物体;SpreadingGrass=37 铺草)
- '地表装饰' 37→**34**(Traps=34 放置机关)
- '清浮空'→'瓦片清理'(槽改名)

**新表结构**(worldgenKeys.ts):数字表(43 槽,每条带 cs 行号注释)+ 字符串键表(1.4 新增 pass:绿洲/长苔藓/钟乳石宝石树=WorldGeneration.*;微光/沙上清水原版无文本借位)。Lang.worldgenText 先查字符串表再查数字表,无映射回退 pass 名。

**双入口接线**:创建世界主路径 UIWorldLoadState 已走 worldgenText(原有);旧调试入口 mainFlow.ts:180 也包了一层。settle 两路文案统一 `LegacyWorldGen.27`(Game.ts settleLabel)。

**54 槽全覆盖验证**:tests/worldgen-progress-text.test.ts(影子槽名清单 vs 两表全查)+ 5 错值断言 + 字符串键断言 + l10n 存在性(数字键 0-91 全在 zh-Hans)。槽改名时测试的 SLOTS 影子清单需同步(单一事实源风险,测试头注释已标)。

**生物群系合并槽限制**:该槽合并 16-34 号 15+ 个原版 pass,单槽只显示代表文本(丛林 11);原版每个子 pass 有独立文本轮播——子级切换未做(需 GenCtx 子标签机制),登记待办。

相关:[[load-progress-vanilla]] [[vanilla-worldgen-passes]] [[worldgen-perf-batch]]
