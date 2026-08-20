---
name: summoner-full-parity-batch
description: 召唤师全量1:1批：数值链(SUMMON_GEAR/SET)/星尘龙链体/虎阿比盖尔计数器两段式/守护者/鞭射程表+衰减+OnHit proc；instanceof HMR fork 探针坑
metadata: 
  node_type: memory
  type: project
  originSessionId: 4a66e745-9d91-4188-8ade-1e2b7775e8b4
  modified: 2026-08-12T05:09:31.763Z
---

召唤师全量对齐批（2026-08-12，三路代理提取原版规格后落地，探针 whip5-summon-full.mjs 全绿）：

**数值链**（新模块 `src/data/vanillaSummonStats.ts`；accfx 提取器不覆盖 maxMinions/minionDamage 模式→独立表）：
- SUMMON_GEAR 散件+配饰（ApplyEquipFunctional type if-chain 1:1）：俾格米项链 1158 +1槽、死灵卷轴 1845 +1槽+10%、纸莎草 1864 +1槽+15%、大力士甲虫 1167 仅+15%伤；OOA 四配饰 3809-3812 各+1哨兵+10%；星尘三件 3381(+1槽+1哨兵+22%!)/3382/3383(+2槽+22%+鞭程0.15)；诡异 1832/33/34 = +1/+2/+1 槽+11%；提基/蜘蛛/蜂/黑曜/禁戒/神圣兜帽 4873/4899/绿藻 5524/Flinx 5068 全表
- SUMMON_SET 套装（槽序键）：诡异+25%伤、黑曜 185|187|127 +15%伤+鞭程30%+鞭速1/1.15、提基 82|53|48 +1槽+鞭程20%、绿藻 283|51|47 +2槽、神圣召唤头 24|229/212 +2槽、星尘 189|190|130 = guardian 行为型
- Player 新 getter：summonDamageMult（=damageMult('magic')×(1+minionDmg)）、maxMinions、maxSentries；equipStats 加 minionSlots/minionDmg/sentrySlots/whipRange/whipSpd/summonSet
- **随从伤害 live 刷新**（Projectile.cs:15368）：Game 召唤只传武器基伤，MinionProj 每 tick 重算——换装即时生效
- 两套驱逐语义分开：召唤腾位=最旧先死；上限缩水=最后召唤先死（Game.fixedUpdate 每帧登记）

**旗舰家族**（MinionProj 分支，行号注释全）：
- 星尘龙 625+626/627/628：aiStyle 121——追敌 acc 0.4-0.8 限速 30/跟随限速 15，穿墙穿敌；链段纯跟随（父段心-方向×16px），全链共用一张 hitCd（7t/敌）；伤害×(1+0.23×段数)；extendDragon 再召唤尾前插 2 段（Game summon case 625 特例：有头不出新头）
- 沙漠虎：杖召唤的是计数器宝石 831（AI_164 头顶环绕不攻击），派生唯一本体虎 833/834/835（≤3/≤6/7+ 档位，伤害×(1+0.4×(宝石-1))，本体 noSlot），周期冲刺 360/300/240t
- 阿比盖尔：计数器 970 + 本体 963（飞行近战 50px 挥击，伤×(1+0.55×(n-1)) 肉前档）
- 星尘守护者 623：套装在身常驻（Game.fixedUpdate），站玩家侧后，500 内拳击，noSlot
- 酷鞭 917 雪花/麻线鞭 1036 蜘蛛：whip 命中生成，noSlot，生命绑 whipBuffs[312/365]

**鞭升级**（WhipProj）：per-whip 射程倍率表（皮鞭 0.75~月主鞭 2.2，晨星 848 是赋值 1.6）；多目标衰减表（同挥第 n 敌 ×falloff^(n-1)）；proc 体系（火鞭 4912 ×2.75+918 爆炸/星陨 1037/花瓣 1038×3/星座星 1039/月主 1045，enemy.whipProcT 240t 一次性）；黑收成 4680 OnTaggedHit 每跳 916；buff 311/308/314=鞭攻速+35/25/12%（**纠正：314 不是召唤伤害+10%**）

**两坑**：①EntityManager.add 解构后丢 this（nextId undefined 炸帧）——必须 `ents.add(...)` 或包 arrow；②探针 `instanceof MinionProj` 在 dev server HMR 模块分叉下恒 false——用 `constructor.name`。

**Review 批修复的 2 真bug**（2026-08-12 复审发现）：
1. **伤害双乘区**：useCombatWeapon wrapper 对 summon/whip 预乘 `damageMult('ranged')+armorPen`，随从/鞭再乘 summonDamageMult → 双乘+双穿透。修复：whip/summon case 改传 `cwIn.damage×(ps?.dmg??1)` 裸基伤（乘区由 MinionProj/WhipProj 命中侧单次结算）。验证 whip6-mult-check.mjs：游侠徽章 ranged 1.15 下随从每跳仍=基伤。
2. **守护者脱装不死**：星尘套脱下后 623 常驻。修复：Game.fixedUpdate 无 guardian 套装时 kill 现存 623。

**复审确认的近似**：仅剩 summonDamageMult 复用 damageMult('magic')（含 MagicPower 等 magic-only buff，原版 minionDamage 独立链不含）——架构级取舍：本仓 damageMult 只有 melee/ranged/magic 三链，加第四链需重铺全部 buff 来源，收益/代价不成比例。其余三条数据级近似（掷矛抛物线 grav 0.3/小鬼火球 life 100/龙链段旋转 rot 通道/虎冲刺伤 1.5+0.4n）已于复审批补齐。

**遗留**：射击随从的 Arrow 弹不吃鞭 tag（原版 MinionShot 吃）；387 视线门；鞭直伤 debuff（Hellfire/Frostburn/Poison 敌方侧未接）；Foxparks 手持喷火 1106；MinionAttackTargetNPC 右键指定；Possession 多重补鞭。

相关：[[summoner-ranged-minions]]、[[summoner-whip-sfx-facing]]

## 召唤兽朝向/旋转语义修复批（2026-08-17，用户报"魔眼法杖眼球镜像"揪出全族）
**三类朝向机制考古（Projectile.cs 真值，此前通用段一律 facing=sign(移动方向) 翻转=错）**：
- **旋转制（不翻转）**：双子 387/388（aiStyle 66）`rotation = velocity.ToRotation()+π`
  （:28859-28861/:28864-28868——贴图朝左 +π 补偿；**387 交战中朝 LOS 目标** :28867，
  388 恒速度向）；533 致命球滚动 `rotation += vx*0.04`；917 雪花 `vx*0.0125`。
- **AI_062 左贴图表**：373 黄蜂/375 小鬼/407 风暴/423 UFO/613 细胞
  （:62983-62990）`velocity.X>0 → spriteDirection=-1`——贴图朝左、右行才翻转
  → `facing = -sign(vx)`（曾整族反着画）；963 阿比盖尔特判 ×-1（:62992）贴图
  朝右，常规 facing 不变 ✓。
- **AI_026/164 零赋值恒不翻**：俾格米 191-194/宝宝史莱姆 266/蜘蛛 313·379·390·391/
  Foxparks 1094/计数器 831·970——原版从不写 spriteDirection，我们曾按 facing 翻=错。
实现：MinionProj 三表 `AI62_LEFT_ART/MINION_NO_FLIP/MINION_ROT_ONLY` + draw 重构
（rot!==0 或 ROT_ONLY → rotate；否则 facing<0 且非 NO_FLIP → scale(-1,1)——旋转与
翻转互斥，原版 dir 恒 None）+ **朝向/rot 计算必须在移动段之后**（原版 FindFrame 取
当 tick velocity；放移动前首 tick vx=0 恒不更新）。388 补 MINION_FRAMES [4,3,0]
（:28878-28888 与 387 同拍）。乌鸦 317/虎 833-835/755/759/623 核对无恙（右贴图常规）。
测试 tests/minion-orientation.test.ts 6 例（记录型 ctx 桩断言 rotate/scale 调用序）。
**未接视觉债登记**：388 拖尾 oldPos 渐隐(:33939+)/387 EyeLaserSmall 辉光叠画/755·759·
虎行走 rotation 摆动(vx*0.04-0.15)——C 级。

**续（同日二轮，用户报"激光起始位置偏移"）**：射击随从出弹锚点曾写死
`cx-5`（按 10×10 判定盒假设）——389 激光判定盒 4×4 → 弹体中心恒偏左上 3px；
修复=按 projectileData(shot) 实际判定盒取半宽（原版 NewProjectile @Center →
左上=Center−size/2，:28977-38981），全 MINION_SHOOT 族受益；387 激光 timeLeft
补 300（:28981 覆写，非 SetDefaults 600）。测试第 7 例锁锚点+弹型+寿命。

**续三轮（全召唤物出弹锚点+寿命对账，用户问"其他召唤物同类问题"）——9 处偏差全修**：
| 出弹点 | 原版锚点 | 曾错 |
|---|---|---|
| MINION_SHOOT 全族 | Center（AI_062 :63209）| ✓已修(二轮) |
| 俾格米 191-194→195 | (cx, cy-8)（AI_026 vector15 :58764）| 缺 -8 手部高度 |
| Foxparks 1094→1097 | cy-10（:58784 再 -2）| 缺偏移 |
| 哨兵53 308/377→309/378 | 炮口−弹盒/2（14/16）| 写死 -5 偏 2-3px |
| 哨兵53 **966→967 炮口** | **本体 Center**（flag24 zero 恒 (0,0) :27315-27347）| **误植 -16Y（考古纠错）** |
| 哨兵123 641→642 | Center（:33993）−9（18×18）| -2 近似+写死-5 |
| 烈焰塔 663-667→668 | 炮口−8（16×16）| 写死 -5 |
| 弩车 677-679→680 | **本体 Center**（:65590/:65693）−8 | **(cx,y+20) 左上角语义=弹心偏右下半格** |
寿命对账：AI_062 全族出生覆写 timeLeft=300（:63210，含小鬼 376——SetDefaults 100 被压过，
旧表 life:100 错）；唯 423→433 分支不覆写 → 100；哨兵弹走 projectileData(shot).timeLeft
（378 蛛卵 60）。教训：**NewProjectile(x,y,…) 是左上角语义、NewProjectile(center…) 是中心
重载——两形态混用是偏移根因；出弹锚点必须按弹型 SetDefaults 判定盒取半宽**。
测试 minion-orientation 10 例（387 激光/俾格米-8/弩车中心/九头蛇扇区炮口+14×14 居中）。

**续四轮（用户报"只召出一个激光眼"）——多生召唤杖三分支补齐**：Player.cs
召唤特殊分发段 :47840-47967 逐条对账：①**2535 魔眼法杖=成对双子**（:47872-47883
projToShoot 387 + projToShoot+1 388 双 SpawnMinionOnCursor；两型 minionSlots 各
0.5=一对 1 槽——388 noSlot 不占计数）②**2551 蜘蛛法杖=三型轮换** 390/391/392
（:47885-47888 nextCycledSpiderMinionType 先用后 ++%3，Game.spiderMinionCycle 游标）
③**2584 海盗法杖=随机三变体** 393+Next(3)（:47893；393/394 aiStyle 67 常规翻转，
392 是 aiStyle 26 → 补进 MINION_NO_FLIP）。其余分支（5664 localAI0=30/1802/2364
单发）无多生态。Game.ts 召唤 case 重构出 spawnMinion(pid,noSlot) 局部 helper；
成就 9+ 计数同步排除 noSlot 对偶件。

**续五轮（用户报"5 只眼仅 1 激光眼"）——noSlot 方案翻案**：四轮的"388 noSlot 不占
计数"是错的：不占位=【永不进驱逐池】→ 387 被逐后 388 永存，越召越多（4 痉挛+1 激光）。
正确模型=原版 Projectile.minionSlots 权重制：双子各 0.5、其余 1，**全部入池可驱逐**；
上限判定=Σslots+1(StaffMinionSlotsRequired 默认 1)≤maxMinions，驱逐循环到腾够
（:51022-51047），驱逐序=槽位升序稳定排序（:50976-50988 原版插入式升序——混编池
先杀 0.5 双子，同权重保插入序=双子对自然成对死）。maxMinions=1 恰好一对；=3 恰好
三对。成就 9+ 口径同步改权重和。**教训：noSlot 只该用于真 0 槽实体（鞭伴生 917/1036），
"半槽"必须进权重池而非排除池。**

**续六轮（用户报"又只剩一个激光眼"）——每 tick 自裁段才是真凶**：Game.fixedUpdate
里有第二处上限执法（:15370-15392 的移植，此前按【实体数】计数逐帧杀超额随从）——
一对=2 实体 > maxMinions=1 → 388 出生即被每 tick 补杀（召唤段的腾位修复没毛病，
是这里在背后清场）。原版该段真身=槽位权重制自裁：每随从按实体序累加 own
minionSlots，slotsMinions+own > maxMinions → 自己 Kill()（双子 0.5+0.5=1 恰好
成对活）。修=两处统一走模块级 minionSlotsOf()（387/388→0.5 余 1）。
**铁律：上限执法有【两处】（召唤腾位 FreeUpPetsAndMinions + 每 tick Projectile.AI
自裁），改槽位模型必须两处同步，只改一处必被另一处清场。**

**续七轮（用户报"两眼重叠"）——双子悬停/互斥原文化**：原版两眼分开的本体机制两件：
①**互斥**（AI_66 :28514-28539）：同主另一双子曼哈顿距<判定盒宽40 → 双轴速度各
互推 ±0.05/t（成对同点出生需 id 决胜破对称，原版靠浮点噪声）；②**专属悬停**
（:28790-28860）：锚点=玩家中心+(0,-60)，距锚>70px 才阻尼趋近（v=(v×15+dir×spd)/16，
spd≥15 且随玩家速度），**≤70px 零驱动力**=互斥自由区——互推累积到曼哈顿~40px 稳定。
教训：**通用槽位硬弹簧（速度∝距离）会压死 ±0.05 互斥**（实测分离仅 1.25px）——
半槽/成对随从的聚合行为必须连原版悬停物理一起移植，互斥才有效。测试第 11 例锁
90t 分离≥20px。

**续八轮（用户问"激光眼有无近身攻击"）**：有——两只双子 SetDefaults 均 friendly=
true 即带接触伤害（387 也非纯远程）；差异在同型静态免疫冷却 387=16t/388=12t
（:4436/:4451，曾通用 20t 已分型）+388 独有 25 穿甲（弹型数据通道自动带）。
激光 389 是独立弹幕命中（×1.15 伤），与接触伤并存不互斥。

**续九轮（用户报"血红法杖蝙蝠不发光"）——随从世界点光全表补齐**：随从光不在
SetDefaults.light 标量（Game 弹幕光表只扫该字段→随从全漏），在各 AI 的
AddLight/CastLightOpen：755 血蝙蝠=Crimson(220,20,60) CastLightOpen(:48604) +
绘制端 4 层红晕（α120 ±2px 十字向叠画染色本体，Main.cs:30669-30678——"发红光"
的视觉主体是晕圈）；613 细胞(0.2,0.6,0.7):62191；623 守护者(0.9,0.9,0.7):41997；
1094 狐火(0.5,0.3,0.1):55275；533 双色档（无态机取橙）；653 方块白 0.5。**双子
387/388 零自发光**（AI_66 仅 533 有 AddLight——调查中途的"蓝/橙"印象是 533 的）。
实现=MinionProj `get lightRGB()`（实体光通道直读，985 泰拉刃同链）+ tintFrameCache
染色缓存（source-atop 剪影）。测试 3 例（含双子无光反证）。
