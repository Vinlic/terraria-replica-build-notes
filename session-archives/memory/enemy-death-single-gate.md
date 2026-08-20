---
name: enemy-death-single-gate
description: 多弹头同帧致死后二次死亡管线bug(双份碎块);hurt入口dead门;hurt返回值契约=仅致死true
metadata: 
  node_type: memory
  type: project
  originSessionId: c212e38d-8db4-446d-b3da-4e20d707caf7
  modified: 2026-08-13T16:04:34.078Z
---

2026-08-14 用户报"多弹头武器(食人鱼/霰弹)打死僵尸出现两份碎块":

**根因链**:2026-08-13"单发弹豁免免疫帧"修复(pierce=1 无视 iframes,霰弹多弹头同 tick 全生效——正确修复)打开了新窗口:同 tick 后续弹头对"首发已致死、尚未出列"的敌怪**再次进入 hurt** → hp 再减 → `hp<=0` 死亡分支**二次执行**(碎块/掉落/音效翻倍)。原版由 Damage_PVE 的 `npc.active` 前置门(Projectile.cs:11869)天然防重,本仓 hurt 缺等价入口门。

**修复**:Enemy.hurt 入口 `if (this.dead) return false;`(死亡分支内 dead=true 置位本就够早,纯入口缺失)。tests/enemy-death-single.test.ts 3 条(双发/八发霰弹 killed 恰好 1/未致死不吞伤)。

**两个踩坑**:
1. **hurt() 返回值契约 = 仅致死(或特殊分支)返回 true,非致死恒 false**——写测试勿假设"受击成功=true"。
2. 测试 mock 死亡管线最少要给:world.flags/isExpert、player.hp/luck/buffs.has/addDPS(掉落链层层读)。

**关联**:此 bug 是免疫帧豁免修复的**二阶效应**——改判定门后要重扫"同帧多事件"路径的幂等性。
