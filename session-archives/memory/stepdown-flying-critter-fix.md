---
name: stepdown-flying-critter-fix
description: "萤火虫/蝴蝶\"怪力按压闪现\"根因=StepDown宽门vy>=0;修复=NPC族wasGround门/玩家vy===GRAVITY字面门"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1fc2b821-952a-4ed1-9b75-6e99198205af
  modified: 2026-08-13T04:54:34.657Z
---

2026-08-13 修复：低空飞行小动物（萤火虫/蝴蝶）周期性"被怪力按到地上+闪现+恢复+再按压"。

**根因**：`TileCollision.moveAndCollide` 的 StepDown（Collision.StepDown 移植，贴地下台阶 7~17px 瞬移吸附）触发门写成 **`vy >= 0` 宽门**——低空平飞的小动物（vx≠0、vy≥0、脚下 7~17px 有落面）每 tick 被瞬移按压到地面；飞行 AI 抬升后再次进入窗口 → 周期循环。症状精确匹配"矮飞行生物"。

**原版门（均为 == 精确等值）**：NPC.cs:54374 `velocity.Y == 0f`（该时点=贴地语义——原版重力加在碰撞后）；Player.cs:23252 `velocity.Y == gravity`。

**修复**（TileCollision.ts）：Body 加 `stepDownGate?: 'grounded' | 'gravity'`；门 = 玩家 `vy===GRAVITY`（字面）/ NPC 族（Enemy/Critter/TownNPC 缺省）`wasGround`（**入口重置 onGround 前捕获**——本仓重力在碰撞前累加,贴地时 vy=GRAVITY≠0,原版 ==0 在我方恒假,取语义等价门）。StepUp 不动。

**测试**：tests/stepdown-gate.test.ts 3 条（贴地吸附保留/空中不吸附/玩家双门）+ 回归 93 条（conveyor/grapple/thrown/a-batch2/npc-drops）全绿。

**排查弯路**：浏览器探针全程超时（机器 load≈19 + 每次超时连带 SIGKILL 掉自己的 5201 vite 实例,需重启）——高负载期改走静态分析更快;`debugSpawnNpc` 后 in-page 长循环 bench 在该负载下不可行。相关 [[vulture-firefly-ai-fix]] [[vanilla-solid-audit]]
