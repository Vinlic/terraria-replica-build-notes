---
name: balloon-slime-ai125-port
description: 气球史莱姆下地底/卡死根因=686被转成bound站地TownNPC(丢失AI_125漂浮语义);修=真Enemy aiStyle125悬停AI(前方列扫描/追平玩家/湿爆)+die()走死链Transform(680)
metadata: 
  node_type: memory
  type: project
  originSessionId: ec878731-1c65-4b4c-9a3b-c8009ce5461a
  modified: 2026-08-17T11:00:07.182Z
---

# 笨笨气球史莱姆 686 全链（2026-08-17 用户报障"下到地面以下/卡地底下"）

**根因**：686 生成时被 `trySpawnBoundTownNpc` 转成 **bound 站地 TownNPC**
（重力+贴地）——原版是 aiStyle 125 **漂浮体**（SetDefaults :17559-17570：
noGravity/noTileCollide/lifeMax 1/damage 0），气球悬停于地形上方、撞水/受击
爆裂解救。站地近似丢失漂浮 → 漂浮怪出生点在天空位 + 无瓦碰撞落位 → 可沉到
地表以下/嵌地形卡死。

**修法（三件）**：
1. **Enemy.balloonSlimeAI**（AI_125 :44009-44139 1:1）：
   - 水平朝 direction 0.04 加速至 3+|wind|×2（比 AI_113 风气球的 0.01 档快
     ——两气球非同参）；rotation=vx×0.05。
   - 前方一列（中心+dir）自底向下扫 8+num2 格：实心/液体 5+num2 内=近距
     → vy−0.1−0.2；有阻 −0.1；开阔 +0.05；钳 [−4,2]。
   - 玩家 400px 内且 canHit → ±0.035 追平高度（num8=2 钳内双补档）。
   - num2 = 玩家高出本体底边的格数（direction 与目标方位不符则 0）——
     ★玩家在高空时扫描加深=气球追平玩家高度，是原版行为勿当 bug 修。
   - 湿/嵌实心 → `this.die(game)`（**不能直写 dead=true**——windyBalloon 式
     直写绕过 hurt 管线 → onEnemyKilled 不触发 → Transform(680) 丢失）。
2. **撤 686 的 bound 转换**（trySpawnBoundTownNpc 表移除 686；天空怪位
   spawnTileY=空中行 ✓ 通用 flying 落位=首个非实心干格 ✓ 原生对齐）。
3. **Game.onEnemyKilled 686 支**（CheckDead :82525-82555）：气球碎粒子近似
   （Gore 1143-1145×3+1146）→ position=Bottom+(0,48) → TownNPC
   'town_slime_clumsy' + `unlockedSlimePurpleSpawn` 置旗（无公告）。

**How to apply**：
- 测试 tests/balloon-slime.test.ts 4 条：600t 悬停恒在地表上（不卡地底）/
  空域缓降 vy≤2 / 湿爆当 tick 死 / 前方近地遮挡上升。玩家须放**地面同高**
  （高空玩家→num2 加深→追平=合法上升）。
- AI 测试 harness 惯例：makeHooks（ai-side-fixes 同款）+ `Enemy.fromVanilla(
  686,x,y)` + private AI 经 bind 直调。

关联 [[critter-ai-port]]（小动物 AI 族）/ [[npc-frame-golden-gate]]
（686 json 条目曾缺=手补档）。
