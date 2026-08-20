---
name: wall-creeper-ai40-port
description: "AI_040 爬墙蜘蛛 1:1 移植要点——164/165 是\"同一种怪的两个形态\"靠 Transform 互转，不是两种怪"
metadata: 
  node_type: memory
  type: project
  originSessionId: 04569a63-44aa-4669-98a3-b777d15e98f8
  modified: 2026-08-11T03:15:58.579Z
---

# AI_040 爬墙蜘蛛族移植（2026-08-11）

用户问"爬墙蜘蛛是不是应该能爬墙" → 结论：**原版 164（Wall Creeper）地面行走是正确的**；
能爬墙的是 Transform 出来的 165（Wall Creeper Wall）。同族还有 163/236/239/530（地面）
↔ 238/237/240/531（爬墙），六对全是"同一怪物两形态"。

**关键机制（NPC.cs）**：
- AI_003 内 ：59273-59293：地面蜘蛛 `velocity.Y==0 && NPCCanStickToWalls()` →
  `Transform(墙形态)`（TryChangingSizeFromBottomCenter 底边中心锚定改尺寸）
- AI_040（:29784-30022）：无重力贴墙爬；有视线伺服追击/无视线 ai[0]±200 振荡漂移；
  碰撞旧速×-0.5 反弹（X 朝 direction 保底 ±2、Y 保底 ±2）；`!NPCCanStickToWalls()`
  → Transform 回地面形态（:29991）
- NPCCanStickToWalls（:56209）：身体中心 3×3 内"非实心且有背景墙"格数 >4 ——
  蜘蛛洞天然满足，地表不满足（所以地表蜘蛛只走路）
- 原版生成只 SpawnNPC(164)（蜘蛛洞分支 :1586）；165 永不直接生成，全靠 Transform

**Why**: 没看 Transform 机制会误判"165 缺生成"或"164 该爬墙"，两头都错。

**How to apply**: 实现=Enemy.ts `wallCreeperAI`(case 40) + `tryTransformTo` + fighterAI
内互转 + Renderer aiStyle40 旋转/不镜像/帧表（crawlT 累加器，cs:73795 FindFrame）。
测到 tests/wall-creeper.test.ts 4 例。专家模式毒液弹（:29960 type 472）未移植（无专家模式）。

相关：[[vanilla-npc-port]]

## 渲染旋转族镜像守卫（2026-08-11 二轮，噬魂怪屁股朝前实踩）

**Bug 类**：旋转驱动族（npc.rotation 决定朝向）若再叠 `facing>0 → scale(-1,1)` 镜像 → 二次翻转"屁股朝前"
（噬魂怪 6 向右飞时实踩）。原版这些家族**从不写 spriteDirection**（默认 -1）→ 原版不镜像。

**修复**：Renderer.drawEnemy 集中判定 `rotationDriven`（旋转分发与镜像排除共用同一谓词，防复发）：
id 4（EoC）/ ROTATION_NPC 集 / aiStyle 5（全转头成员）/ 6 / 23 / 40 / 56。
**例外**：aiStyle 5 内"仅倾斜"成员（黄蜂 42/231-235、孢子蝠 176/205、蜜蜂 210/211）贴图横画只 tilt
不转头——仍需镜像。同轮顺手修掉 23 飞行武器（facing 恒 1 被永久镜像）与 56 地牢之魂（facing 随玩家
→ 追人时骷髅头反）。**新增旋转族 AI 必须登记 rotationDriven**，否则必然屁股朝前。

## AI_005 swarmer 二轮对表（2026-08-11 三轮，噬魂怪"AI 不对"反馈）

实踩 4 处偏差（Enemy.ts swarmerAI）：
1. **旋转角来源**（观感最大）：cs:51022 原版 6/94/173/619 的 rotation=atan2(**指向目标的期望速度**)−π/2
   ——噬魂怪永远盯着目标转头，惯性环绕时头不摆；我们误用当前速度角。其余全转头成员（仆从 5）
   原版才用速度角。已分族修（faceTarget 门）。
2. **碰撞反弹最小弹速**（cs:51041）：collideX 朝 direction 保底 ±2、collideY |vy|<1.5 保底 ±2——
   曾注释"最小值暂略"直接没做，撞墙后贴墙蠕动。
3. **wet 浮力**（cs:51106）：6/94/173 入水 vy−0.3 钳 −2（上浮不沉）；黄蜂族 −0.5 钳 −4。全缺。
4. **紫尘拖尾**（cs:51083）：非蜂族 1/20 下半身 dust 18（173 红 5）。
已核对无偏差：速度表(6/173=4/0.02、94=4.2/0.022、仆从5=5/0.03、默认6/0.05)、8px量化、
摆振门控(>100/恒开)、<150px 近距制导、flag4 双步、蜜蜂 ramp、仆从穿墙直移。
cs:50809 flag2(dist>600) 是原版死变量，忽略正确。
