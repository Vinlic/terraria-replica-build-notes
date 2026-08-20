---
name: yoyo-bag-family
description: 悠悠球袋装备族全链——counterWeight int 化/双球/配重球 AI_099_1 重写/魔法线幽灵克隆/meleeSpeed 倒数坑
metadata: 
  node_type: memory
  type: project
  originSessionId: cb3a4729-b2a0-4330-a696-da1975f3392a
  modified: 2026-08-19T09:47:19.036Z
---

悠悠球袋族(3366/3334/3309-3314/5540/5541/5547)装备效果 + 配重球/双球/魔法线全链
(2026-08-19 子代理建成):equipStats.counterWeight **int 物品id**(0=无;556-561 彩色/
1079 黑)+ yoyoGlove + magicString + vanityCounterWeight(社交槽彩色配重优先)。

**Why:** 曾 counterWeight 降级 bool + Game 侧"命中落配重"近似;CounterweightProj 18×18
盒/无 ai0 状态机/切向增速块恒跑(原版仅超径分支内)。

**How to apply:**
- Player.Counterweight(Player.cs:11946-12004):计数门(手套→同型二号球 16 速朝命中点;
  配重数<球数→掷配重,vanity 优先,kb=(kb+6)/2)——本仓 `counterweightDecision` 纯函数导出。
- ★counterWeight **每帧清零重掷**(ResetEffects :18288 + UpdateEquips 每帧)——袋装期间
  颜色每帧变,命中采样当帧值(勿按"首次装备定死"实现,曾被简报误导)。
- ai0 状态机(YoyoProj=AI_099_2/CounterweightProj=AI_099_1):-1 回收(×0.8 惯性穿墙)、
  -2 脱离坠落(重力 0.3 帽 16/穿透 Next(3,7)/撞墙亡)、-3 魔法线幽灵(隐身零伤)、
  正值追标。**-2 免画线**(Main.cs:27799)。
- magicString(:64727/:65110):松手→原球转 -3 幽灵飞回(线仍画)+ 掷 75% 伤/击退 -2
  克隆自由坠落;配重球同款转移。
- ★meleeSpeed 缩放:原版基 1(Player.cs:2328),本仓 attackSpeedMult=**倒数**——
  悠悠球射程/寿命链须取倒数还原,曾方向全反。
- 测试 tests/yoyo-bag(38);遗留:603 专属副弹/heldProj 朝向为引擎级缺口;-2 穿透
  不消耗于小动物支路。关联 [[string-accessory-system]]。
