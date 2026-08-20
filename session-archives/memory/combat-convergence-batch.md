---
name: combat-convergence-batch
description: 战斗系统收敛批：配重球环绕实体/燃烧瓶MolotovProj裂开6火云/狙击镜zoom/3878补丁——专项清单全部清零
metadata: 
  node_type: memory
  type: project
  originSessionId: 4a66e745-9d91-4188-8ade-1e2b7775e8b4
  modified: 2026-08-13T03:32:15.996Z
---

战斗收敛批（08-13 续4，任务 #72 专项清单全部清零，构建绿+单测4/4）：

**配重球**（AI_099_1 :64472-64610 1:1）：`CounterweightProj` 环绕实体——轨道半径 125（yoyoString +25%+10）、超径钳回（num6=min(over,sp-1) 衰减）、切向增速 vector2=(vy,vx) 象限定号保速转朝、rotation+0.5/t、生存绑宿主 yoyo（alive()）；Game spawnWeight 回调改用它（曾直线坠落 Arrow 近似）。★判宿主死亡用 `!yoyo.dead` 双重写法（实际等价单次）。

**燃烧瓶**（2590→399 aiStyle 68；:70889-70928）：`MolotovProj` 弹跳瓶体（t≥15 重力 0.2/t），撞块/命中/超时 → 裂开 6 朵火云（散布 -vx×rand(20,50)%±8 / -|vy|×rand(30,50)%-8..+2、伤 ×0.5）→ 火云=Arrow(bounce/grav0.1/life360/pierce3) + ignite(OnFire :10850)；thrown 路径 `tc.shoot===399` 分流 return。★审计"3197=燃烧瓶"是错认：3197 是霜镖鱼(shoot 520 coldDamage)，真 Molotov=2590(shoot 399)。

**狙击镜 zoom**（Main.cs:62215）：装备 1858/4005 + 右键按住 → setZoom(×0.8) latch，松开复原（`_scopeZoomed/_scopePrevZoom`）。1858/4005 的 +10%伤/+10暴 数值已在 accfx。

**省弹表**：ammoCost80 全来源盘点=蘑菇矿胸 1549(accfx ✓)/腿 1550(**漏**:vanilla 只给 crit+7 无省弹——已核源码 :13293 只有 1549 有)/化石套 188|189|129(ArmorSetBonuses ✓)/3878 忍者大师(accfx **补了** dmgRanged0.25+ammoSave；minionDmg+25% 走 SUMMON_GEAR 补)。无尽袋 3103/3104 恒不耗已在。**审计点名的 3475/3930/3540/5134 是弹药物/武器 id 非"省弹来源"——虚警**。

**协作坑**：Enemy.ts 4497 撞上并行会话法师 Dart 编辑现场——build 炸但非我改动，sleep 30 后绿。python heredoc <<'PYEOF' 不执行（引号问题）→ 改用 Write _patch_x.py + python3 _patch_x.py 模式。

相关：[[class-stat-reconciliation]]、[[summoner-full-parity-batch]]
