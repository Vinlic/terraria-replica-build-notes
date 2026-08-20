---
name: dungeon-spawn-port
description: 地牢刷怪系统移植要点——SpawnAnNPC 地牢分支/ZoneDungeon 墙集/dungeonY 链/AI 族 10-21
metadata: 
  node_type: memory
  type: project
  originSessionId: 0650e0c7-c14a-4b14-b89b-73780115946c
  modified: 2026-08-10T05:35:20.122Z
---

2026-08-10 地牢刷怪移植完成（用户报告"地牢怪不生成"，根因是 VanillaSpawner 完全没有地牢分支 + zoneDungeon 墙集写错）：

- **SpawnAnNPC 地牢分支**（NPC.cs L2536-2706）：未杀骷髅王（`world.flags.downedSkeletron`）只出守卫 68；杀过后出 294/295/296/31/-13/-14（愤怒骨族）、32 黑魔法师、34 诅咒头骨、71 地牢史莱姆、70 火轮、72 刺球。`CheckToSpawnDungeonEnemies` 门槛 = 玩家 y ≥ dungeonY+40。
- **ZoneDungeon 三处来源**：①玩家 SceneMetrics（`Game.trySpawnEnemy` 每帧 `setPlayerFlags(scene.zoneDungeon, downedSkeletron)`）；②`Main.wallDungeon` 全表 = **{7,8,9,94-99}**——曾误写成 [7,8,9,41,43,44]（tile id 混入）+漏 94-99，而地牢管线恰恰大量铺 98/99 变体墙；③刷怪率修正 ×0.3/×1.8、未杀骷髅王 spawnRate=10（clamp 后赋值不受 ≥60 下限影响）。
- **dungeonY 链路**：DungeonPass 回填 `gs.dungeonY`（入口地表 Y）→ World.dungeonY → 存档 header round-trip → wld 导入（WldParser 捕获 dungeonX/Y，此前直接丢弃）。缺省回退 groundLevel。
- **`world.dungeonX` 曾是过期值**：WorldGen 在 DungeonPass 前写死 `gs.dungeonLocation`，而 pass 内预计算会重掷（锚点 ±300 拒绝采样迁移）——必须在 pass 后回写。地牢主链随机游走还会从 x0 再漂移数百格，dungeonX 只作粗略参考。
- **AI 族**：10 诅咒头骨（距离分档 5/3/1.5/1 + <250 环绕摆动，Enemy.cursedSkullAI）、20 火轮（ai3=1+Next(15)*0.1 ∈ [1.0,2.4]，逐轴限速）、21 刺球（对角 6 弹跳）在 Enemy.ts；**11 拆分**：68 守卫走 `dungeonGuardianAI`（恒速 8/伤 9999），35 骷髅王走用户 bossAI.ts 的 `skeletronBossAI`——其注释"守卫分支已在 skeletronHeadAI"即指此拆分。
- **Enemy.aiInit 标记**：原版 `ai[0]==0` 初始化门在我们的 ai0 初值 -1120（史莱姆语义）下不可用，新 AI 族一律用 `aiInit` 布尔。
- 测试：`tests/dungeon-spawn.test.ts`（刷怪链+速率）、`tests/dungeon-ai.test.ts`（四族行为）、`tests/dungeon-walls.test.ts`（管线后墙存活）。浏览器 E2E 探针（scripts/_dungeonprobe.mjs）对地牢深处选点受 headless 小视口影响大，Node 直测更稳。

**Why:** 三层错误叠加（无分支/墙集错/坐标过期）才表现为"完全不刷"，逐层对照 [[reference-vanilla-source-of-truth]] 排查。
**How to apply:** 地牢相关问题先查这三处；加新 AI 族记得用 aiInit；SpawnAnNPC 加新分支注意在原版链中的位置（地牢在 crimson/corrupt 之前）。
