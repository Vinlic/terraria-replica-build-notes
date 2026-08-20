---
name: plantera-parity-audit
description: 世纪之花262全链1:1对齐批:召唤SpawnOnPlayer化/灯泡爆发接通/弹幕物理/毒buff/专家分支/商店门/Wiring死门/测试13条
metadata: 
  node_type: memory
  type: project
  originSessionId: 1fc2b821-952a-4ed1-9b75-6e99198205af
  modified: 2026-08-13T00:58:43.032Z
---

2026-08-13 世纪之花全链复核+对齐。**ID 修正(勿再用旧表)**：1456 里 Plantera=262/Hook=263/Tentacle=264/Spore=265(非 265/260/261/259),灯泡 tile=238(非 2383),弹幕 Seed=275/PoisonSeed=276/ThornBall=277,宝袋=3328(3331 是邪教徒袋)。

**修复清单**（均有 1456 行号注）：
1. 灯泡召唤改走 `Game.spawnBossOnPlayer(262)`（NPC.cs:81273-81506：玩家屏幕外 500 次尝试+末次强制、timeLeft×20=15000）；旧路径地表±55 列顶部扫描是错的。物品召唤(summonBoss)路径暂保留原样（后续统一迁移）。
2. 三机械全灭保底灯泡 `WorldEvolution.planteraBulbBurst()`（cs:74180-74329：丛林侧框[0.15/0.35 或 0.65/0.85]×[worldSurface,h-200]、2500 次、<500 forceBulb(泥59+4×4计分≥12+外环转草)、<200 允非活动格、恰好生成一个）；Game.ts Boss 死亡 ev16/17/18+hardMode+三旗门触发。EvolutionHost 加 dungeonX 字段。
3. 弹幕物理：Arrow 新 opts `gravDelay`(275/276 35t 后 g=0.025)/`thornBounce`(277 vx恒反×0.9,vy>3 才竖弹)/`homing{speed,weight,floor|cap}`(专家追踪 275/276 18/70/14、277 12/200/16)；bossAI.shoot 加 arrowOpts 透传。
4. 玩家中毒 BuffType.Poisoned=78(vanillaBuff 20,BuffDescription.Poisoned 原版键免 l10n)+ENV_DOTS -2HP/s；statusPlayer case 276（专家必中 120-540t/经典 50% 180-420t,Projectile.cs:11527-11535）。
5. planteraAI 补专家/ftw 分支（速度 (v+1)×1.1/(a+0.01)×1.1、钳+150、弹速17、骰4→2/8→6、蓄力+1、触须 8+3/钩 ai3 锚定+1/60 补充、触手动态半径+300×(1-血比)+加速度+0.3、钩收线+1）；激怒下界修为 **UnderworldLayer=h-200**（Main.cs:2863，曾误用 lavaLine 差近 200 格，双处）；despawn 4800px 语义接入；孢子 EncourageDespawn(5)+专家追踪×2。
6. 钩蔓 263 `dontTakeDamage=true`（NPC.cs:12331；自毁走直改 hp 不受阻）。
7. `Wiring.planteraDowned` 死门接活（读档注入+262 死亡置位）→ 蜥蜴砖致动/神庙传送器限制按原版解除。**1456 无 TempleDoor tile**——神庙门禁就是祭坛+致动+传送器+蜥蜴砖 pick210 四道,勿再造门 tile。
8. 地牢之魂 288 死亡刷出（cs:79863-79878：非288+lifeMax>100+value>0+hasPlayerTarget+hardMode+downed_262+玩家ZoneDungeon,1/13 专家1/9）——Enemy 掉落段 spawnPart。
9. 宝袋 3328 开包（Player.cs:7077-7135：面具1/7+神庙钥匙恒+**孢子囊3336恒**+苗苗1/15+斧1/20+俾格米1/2+荆棘钩1/10+rand(8)八选一）——Game 物品使用链新分支。
10. 商店门：extract-shops.mjs 补 downedPlantBoss/downedPirates 并重提（地雷937/自动锤1551/画家5344/巫医1159-1162/1167/1339/泥芽4701 全部带门）；shopCondOk 加两 case。旅行商人首件改原版显式清单单次随机（Player.cs:55747-55785,含世花+4染料 2878/2879/2884/2885）——旧实现误用 GetItem 池+重试环。

**已核对无需改**：掉落规则全量(vanilla-npcdrops.json 5 组)、BGM 24(262/263/264)、Boss 头像/血条/藤蔓渲染、蜥蜴砖 pick210 挖掘门、Lacewing 661 门(19:30-24:00+1/10+唯一)、hardDungeon/日食 477 门、Cyborg/进化减半。**登记未实装**：expert justHit 越视线骰、ftw 钩蔓落地生刺(tile 655 未查)、宝袋 TryGettingDevArmor、其余 Boss 宝袋开包(仅 3328)、钩蔓 value=15金字段。

**测试**：tests/bossAI-plantera.test.ts 13 条（相位常数/激怒界 h-200 陷阱回归/despawn/弹幕 opts/延迟重力/追踪/荆棘弹跳/上毒/爆发恰好一个+无草 false/263 无敌）全绿；boss 族 83+npc-drops 22+buff/scale 63 回归全绿。world-final-hash 两个种子当前红=并行"世界生成零风险优化批"改了生成输出,**非本批**(本批不触生成确定性),金标归该会话闸门管。相关 [[boss-summon-announce]] [[mechanics-audit-2026-08-12]]
