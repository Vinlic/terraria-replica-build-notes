---
name: dungeon-entrance-sand-seal-fix
description: 地牢入口走廊被沙封死根因=legacy 入口误用 Dome/Tower 专属 ±300 预计算漂移;入口类型门 DungeonCrawler.cs:275/818-849
metadata: 
  node_type: memory
  type: project
  originSessionId: 1fc2b821-952a-4ed1-9b75-6e99198205af
  modified: 2026-08-12T17:32:50.260Z
---

2026-08-13 修复:地牢入口走廊(老头游走的院子)常被沙丘封死。

**根因**:DungeonPass 曾把 DungeonCrawler.cs:280-318 的入口预计算(±300 拒绝采样 + 锚点迁移)无条件套在 legacy 入口上。原版该块被 `preGenDungeonEntranceSettings.PrecalculateEntrancePosition` 门住(DungeonCrawler.cs:275),而 `MakeDungeon_GetEntranceSettings`(:818-849)只给 Dome/Tower 设 true,**legacy(普通世界默认)为 false → 整段不执行**,dungeonLocation 保持 Reset 值,入口由爬升大厅盲爬出地表决定(MakeDungeon_GenerateNextEntranceHall_Legacy,:443)。预计算的接受条件只挡云与净空——沙丘顶越高越空几乎必过 → 入口被系统性吸到沙丘顶,东侧开口被沙墙封死。顺带该循环多消耗 0~6000 颗共享流样本(legacy 不该耗)。

**原版防沙机制全景**(核对结论,勿再疑):所有放沙 pass(Dunes/OceanSand/SandPatches/Desert)都在 Dungeon 之前;之后只有 BeachesAndOceanCleanup(x 钳死在 leftBeachEnd-50 外)、GravitatingSandCleanup(cs:15198,填"落沙与上方实心间"空腔,无地牢门禁)、FinalCleanup ③ 落沙柱(cs:22312-22385,同样无门禁)。原版走廊不被封纯靠"入口顶上是砖、上方无悬空沙"(LegacyDungeonEntrance.cs:213-251 Block B:[入口顶,worldSurface) 内活动非样式方块全覆写为砖+门口强清)。我们 dungeonEnt(1405 DungeonEnt 移植)等价步骤齐全;GravitatingSand/FinalCleanup 与原版逐门一致,无需加门禁。

**遗留对账项**(本次未做,做完整地牢流对齐时处理):①vanilla 在 Dunes pass 头(cs:11542)消耗主题 Next(3)+入口类型 2 掷+RandomSeed=Next()(int32)共 4 颗;我们主题在 DunesPass、入口类型 2 掷在 DungeonPass 头、RandomSeed 整颗缺失 → 净差 1 颗。②vanilla LegacyEntrance 用 RandomSeed 播种的**私有** UnifiedRandom 掷结构骰(LegacyDungeonEntrance.cs:96),我们用共享流。修复后 Dungeon pass 消耗=shelf/lantern/useSkewed+y0 一颗,与 vanilla legacy 完全一致。

**回归**:world-final-hash 与 /tmp/gen-pass-hash 基线已重生成(UPDATE_GOLDEN=1 / GENHASH_DUMP=1)。caves-checkpoint 'lakes' 分歧为既有问题(链上无 DungeonPass 依赖,系并行 LiquidSim 未提交),勿误算本次。复现脚本 tests/_dg-sand-dump.test.ts(多种子计数,DG_DUMP=1 出 ASCII 图):修复前用户种子 1831 沙块封院,修复后 321(仅地形残沙,院口开放);9293480=260、SandboxWorld=87、12345=0,均视觉确认不封路。相关 [[ocean-sand-hellfort-parity]] [[vanilla-worldgen-port-status]]
