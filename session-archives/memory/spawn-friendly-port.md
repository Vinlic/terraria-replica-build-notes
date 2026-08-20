---
name: spawn-friendly-port
description: 兔鼠刷到浮空岛的根因=spawnFriendly 掷骰未移植(NPC.cs:711-832);townNPCs 门/概率表/敌怪链守卫
metadata: 
  node_type: memory
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-11T16:15:31.310Z
---

2026-08-11 用户报"松鼠兔子刷到空中岛"。根因:**spawnFriendly 掷骰整段未移植**(旧备忘标"恒 false 门恒放行")——原版小动物链在 SpawnAnNPC `else if (spawnFriendly)`(:2006)内,**只有掷中友好轮才可能出小动物**;而友好轮掷骰由 **townNPCs(玩家附近城镇 NPC 数)** 门控:

- 外层门(:710):!invaders && 非血月(或白天) && !腐化/猩红(日食/陨石/旧军缺席恒 false)
- **地狱侧**(player.Y/16 > UnderworldLayer=h-200,:713-759):townNPCs 1→1/10、2→1/5、≥3→1/3;未中 spawnRate×1.25/×1.5/×2
- **地表/洞穴侧**(:760-831):townNPCs==0 → **永不友好**(浮空岛/荒野无 NPC → 原版从不出兔鼠!);1→1/3(未中×2)、2→2/3(未中×3)、≥3→恒友好(:824 专家 1/30 例外);友好命中 maxSpawns×0.5(地狱)/×0.6(地表)
- 友好轮 = SpawnAnNPC 的 else-if 链分支:**整轮只出小动物,落点 tile 不合就空过,绝不落入敌怪链**(守卫在 VanillaSpawner 敌怪段前 return null)

落地:VanillaSpawner.getSpawnRate 尾部掷骰(新增 townNPCs/dayTime/zoneEvil/bloodMoon 四参)+ 四段友好门(水池 A/B :1839/:1895、雨天宝石鼠兔、地表小动物、洞穴宝石鼠兔)+ 友好轮敌怪链守卫;Game.trySpawnEnemy 统计玩家 ±(85×60) 格内存活 TownNPC 数传入(≈SceneMetrics.TownNPCCount)。回归 tests/spawn-friendly-cycle.test.ts(0 NPC 恒 false/≥3 恒友好/血月夜与邪恶区关门/友好轮不出敌怪)。墓地/Skyblock/infectedSeed 变体未实装。

**全面 review(2026-08-12,防止同类"登记了却没人补"再发)**:
- 又修 3 处:①困难丛林水 157 巨骨舌鱼/猩红水 241/242(:1673-1683,此前困难丛林湖只有食人鱼兜底) ②龟甲虫 219(丛林草 1/60)/骨头博士 52(夜 1/500)(:3681/3688,此前"登记跳过"与 jungle 测试冲突——测试断言已更新放行 219) ③UnderworldLayer=h-200 注释纠正(是精确值 Main.cs:2863,非近似)
- **新纪律**:docs/spawn-parity-gaps.md 台账——所有"未移植/近似/恒X"必须登记(原版行号+可见影响+依赖);VanillaSpawner.ts 文件头加了指引注释
- 链结构核对结论:友好轮守卫位置正确(skyMob:1290/救援段:1565-1703 在友好分支**之前**,原版即不挡);蚁狮 SandstoneCheck 并行会话已补
- 遗留(台账"待补"区):友好轮水中小动物、恶地沙漠食尸鬼变体池、沙虫 513、TownNPC 救援四件(渔夫/高尔夫球手/造型师/酒保,需 spawner→TownNPC 管线扩展,453 模式可复用)
- 并行会话在途(非本批):critter-ai 萤火虫/living-tree/bossAI-lategame/caves-checkpoint 四处红

## 2026-08-13 附:spawnFrog 裸传 rng.next 崩溃(用户报"进丛林炸")
- 根因:VanillaSpawner.spawnFrog 把 `rng.next` 当**裸函数引用**传给 Luck.rollLuck(第三参是 `() => number`)→ 方法与实例分离,`this.ur` undefined。同文件其余三处(:442/:1520/:1529)都是 `() => rng.next()`,此处笔误。
- 修复=箭头包裹;全库扫 `[(, ]\w+\.next[,)]` 无其他裸传。
- 验证:1500/8000 帧丛林 fixedUpdate 探针零 pageerror(修前进丛林必炸)。探针坑:g.enemies 是方法要用 g.entities.enemies;fixedUpdate 需传 dt 否则静默不刷怪。
