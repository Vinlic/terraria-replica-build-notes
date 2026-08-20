---
name: summoner-ranged-minions
description: 射击型召唤物全量落地：AI_062 五族/AI_026 俾格米掷矛/aiStyle66 双子激光/aiStyle53+123 五哨兵——表驱动 MINION_SHOOT+SENTRY_SHOOT
metadata: 
  node_type: memory
  type: project
  originSessionId: 4a66e745-9d91-4188-8ade-1e2b7775e8b4
  modified: 2026-08-12T03:27:42.091Z
---

射击型召唤物落地（2026-08-12，MinionProj.ts 两张表驱动，探针 whip4-shoot.mjs 六族全绿）：

**MINION_SHOOT（随从，Projectile.cs 源码行号）**
- 373 黄蜂→374 sp10 CD36（:63116，ai[1] rand(1,4)/t>90 折算）；375 小鬼→376 sp11 CD68
- 407 风暴(鲨鱼龙卷！item 2621 Tempest→407，不是蜘蛛)→408 sp20 CD30；423 Xeno UFO(item 2749)→433 sp4 CD24 **射程门 400**；613 星尘细胞→614 sp14 CD36 门 500
- 191-194 俾格米→195 掷矛 sp11 CD30 射程800 **±20px 抖动**（AI_026 :58795）
- 387 双子激光眼→389 sp8 **×1.15 伤** CD45 需视线（:28982）；388/533 是冲刺非射击
- 1094 Foxparks→1097 CD42（还有手持通道模式 proj 1106 未实现=遗留）
- 近战族确认：蜘蛛 390-392(AI_026 flag7)/海盗 393/吸血蛙 758/Flinx 951 全是接触，AI_067 无射击

**SENTRY_SHOOT（aiStyle 53 :27300 / 123 :33990，射程门 1000）**
- 308 冰九头蛇→309 sp9 CD60 炮口+24*facing；377 蜘蛛皇后→378；966 猎犬→967 sp12.5 CD90 Center-16Y
- 641 月门→642 CD30；643 彩虹水晶→**644×3 目标区随机落点 AoE**（直接 hurt，散布随距离 0.5-1.25×）

**坑**：①通用哨兵兜底原本射 projId=self（贴图错）已废；②随从射击与接触伤害并存（原版语义）；③探针坑——靶子打死会从 entities 移除，reset dead 标志不回列，用 1e9 血靶；弹幕生成即死要 hook entities.add 计数不能事后采样。

**近似遗留**：小鬼火球 life 1200t vs 原版 100t；Foxparks 手持喷火(1106)未实现；387 视线门未做(穿墙射)。

相关：[[summoner-whip-sfx-facing]]
