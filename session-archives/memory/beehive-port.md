---
name: beehive-port
description: 蜂巢链路移植要点——KillTile case 225/231、蜂 AI 分支、Larva tile 是 231 不是 220、蜂蜜流动唤醒时序
metadata: 
  node_type: memory
  type: project
  originSessionId: 0650e0c7-c14a-4b14-b89b-73780115946c
  modified: 2026-08-10T05:58:36.583Z
---

2026-08-10 蜂巢链路按 1.4.5.6 校对移植完成：

- **KillTile case 225（Hive 块）**：1/3 → 本格满蜂蜜液体（`st.setLiquid(x,y,255,3)`——打破蜂巢块"流蜜"的出处）；否则掉 item 1124 + 1/2 概率出蜂（Next(3)==0 → 2 只否则 1 只，type=210/211，初速 ±0.4）。实现在 `src/world/hive.ts`（可测纯函数+hooks），Game.breakTile 接线。
- **KillTile case 231（Larva 幼虫）**：无掉落；最近玩家与破坏点曼哈顿距离 <4800px → 蜂后 222。**Larva 是 tile 231，220 是 Solidifier**（TEdit 权威核对，反编译里 L23660 的 PlaceTile 220 与蜂巢无关）。
- **蜂 AI（AI_005 L50768+）**：速度档 5 / 加速 0.1×(ai1-60)/60 爬坡、暖机期逐轴钳 ±6、flag4 双步加速、**flag3 摆动**（蜜蜂在 flag3 集 42/94/619/176/210/211/231-235 内——无条件摆动，无 dist 门槛）、撞墙反弹 ×0.7（6/173 是 ×0.4）。
- **幼虫生成**：HiveSpiderPass 托台代码与原版 AddBeeLarva（WorldGen.cs:32215+）逐行对应但**漏了最后 PlaceTile(231)**，已补 3×3 放置（顶行帧 (0,0)，底行贴蜂巢地板）。
- **蜂后召唤**：summonBoss 已加 'queen_bee'→222；但 **AI 43 未移植**（落 default zombieAI 会地上走）——等 bossAI 批次。
- **蜂蜜流动**：`setLiquid` 触发 onLiquidChanged → LiquidSim.addWater 唤醒。测试陷阱：LiquidSim 必须**先构造再写液体**，否则钩子未注册、液体永远不动。

**Why:** 蜜蜂自然刷新只来自打破蜂巢块（SpawnAnNPC 无 wall 108 分支——蜂巢墙不刷蜂，网上说法有误，以源码为准）；蜂蜜块 229/脆蜜 230 是 Liquid 交互产物（LiquidSim 已有）。
**How to apply:** 测试在 tests/hive.test.ts（破坏语义/分布/4800px 门槛/流动/幼虫生成/蜂 AI，7 用例）。改动 LiquidSim/Game 时留意用户在并行编辑这些文件（曾遇到半保存的重复 `const t` 语法错阻塞全测试）。
