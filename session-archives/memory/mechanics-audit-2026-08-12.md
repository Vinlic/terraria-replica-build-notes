---
name: mechanics-audit-2026-08-12
description: 26 机制集成审计结论+难度错接高危 bug 修复（世界难度与角色难度拆轴）
metadata: 
  node_type: memory
  type: project
  originSessionId: 04569a63-44aa-4669-98a3-b777d15e98f8
  modified: 2026-08-18T06:45:45.565Z
---

# 26 机制审计（2026-08-12）

齐全 13：暴击/防御/掉落/攻速/合成(3173 配方)/音乐/重铸/稀有度/伤害/刷怪率/日夜/幸运/状态讯息。
部分 12（缺口要点）：①仇恨 aggro 已算未消费（索敌固定 18 格）②buff 350+ 全表⑤钓鱼渔获 400+ 条精简+渔夫任务缺⑥月相个别掉落未核⑭生命果未验⑯恢复公式两处简化⑲玩家击退不按武器 kb⑳减益主干缺（Poisoned/Cursed/Ichor/Venom/Electrified/Stoned）㉒中硬核死亡规则（已随难度批补）。缺失：⑬高尔夫全无。

# ★难度错接修复（同日，最高危）

根因：expert/master 全部误读 player.appearance.difficulty（**角色**难度 0软/1中/2硬/3旅），世界难度从未被读取。
修复：world.difficulty（GameMode 0-3）+ isExpert/isMaster/isJourney getter + 存档/wld(gameMode 位)回填 + 旧档槽位回填防降级。
8 处消费点改读 world：Enemy.ts:4178 掉落 ctx、吸血预算 70/80、瓦罐心、旅行商店、掉钱 deathCoinKeepFraction、月事件计分、旧日军团、史莱姆雨触发。
**角色难度回归死亡惩罚**（原版语义）：软核/旅程才 DropCoins；中核/硬核 dropInventoryOnDeath 全掉+铜三件返还；硬核 hardcoreDead 标记不可重生+CharSelect 灰显。**注意：原版硬核不走 DropCoins**（钱随物品全掉，:53398-53470）。
Journey 最小集：T 键循环时间倍率 [1,2,4,8,16,24]+冻结，journeyTimeScale() 乘 clock。
**陷阱**：Journey(3) 不算专家（Main.Difficulty 无 GameMode==3 分支 Main.cs:2696）。
遗留：专家/大师玩家受伤倍率 2×/3× 未接；Journey 研究/力量菜单未做。
测试 tests/world-difficulty.test.ts 15 例。

**Why**: 双难度轴混读会让"硬核角色误触专家掉落、专家世界完全不生效"——数值面最广的隐性 bug。
相关：[[explosion-family-port]]（NpcDrops ctx 入参）

## Review 补修（同日，4 CONFIRMED）
1. **deathCoinKeepFraction 曾整个反了**——原版 num2=保留份额（经典 1/2、专家 **1/4**、大师 0），
   曾误当掉出份额（专家 0.75/大师 1）→ 专家只掉 1/4、大师不掉。已修+测试同步。
2. 瓦罐心 expert `num10--` 偏移（WorldGen.cs:57482-57486）曾注释写了没实现 → 补。
3. 史莱姆雨 SlimeRainSpawns 的 expert 参数曾硬编码 false（NPC.cs:5829）→ 传 w.isExpert。
4. 天气 dayRate 曾写死 1（Main.cs:64320-64409 全链吃 dayRate）→ 传 journeyTimeScale()。
PLAUSIBLE 遗留：NPC ScaleStats 专家/大师怪强度倍率（NPC.cs:18081/18106）全缺（最大消费面）；
旅程倍率不作用世界演化(evolution)；铜三件 3507/3506/3509 原版 TurnToAir 不落地；wld gameMode 无钳制。
教训：**"留/掉"份额语义必须回调用点核对 num3=stack-num2 的流向**。

## 近似清零工程（2026-08-12 晚）
全库盘点：561 处标记（A 级数值 60 点/B 级系统缺失 36/C 级视觉 165/D 级等价声明 130）。
**A 批 1 已完成（7 项，tests/a-batch1.test.ts 24 例）**：
魔力回复整模型 1:1（:19214-19302，含 manaRegenDelay 惩罚/存量系数/帽 20；瓶中星/斗篷 982 真值）；
冲刺 16.9/14.5 单帧+撞墙减半+dashDelay 三态（:20769-21323）；沙丘靴=**×1.75 乘区+runningOnSand 门**（:26225，非"+3/段"——源码纠错）；
友好轮削减假合规修复（地狱×0.5/地表×0.6/town≥3 无条件削 :723-830）；旅行商人 5000 次+4200-4700 阈值降档（Chest.cs:919-947）；
植物生长全图轮转等价采样（:71549-71631 密度等价式）；吸血/鬼疗 HealProj aiStyle52 飞行结算（:27114-27165）。
**教训**：①沙丘靴注释说"+3/段"源码实为×1.75——盘点的"近似描述"本身也要回源码验；
②VanillaSpawner:687 假合规（注释声称乘了实际没乘）——近似审计必须看代码不只看注释。
**A 批 2 待做**：召唤链（鞭 Bezier/哨兵 60t 兜底/月主弹 3连→1发/MinionShot tag）、DD2 T2/T3 逐怪概率表(:1240-1442)、
钓鱼咬钩窗口、攻速配饰差异(Game.ts:9982)、floatEye/fighter 一期档、星光斗篷/蜂巢 SpawnStar。
B 级最大项：专家/大师 ScaleStats(:18081/18106) 仍未接。

## A 批 2 完成（召唤链 1:1，tests/a-batch2.test.ts 23 例）
鞭 Bezier 控制点链（Projectile.cs:45618-45761 逐式：GetWhipSettings case 848 是**赋值**坑）+AI_165+曲线分段命中；
哨兵"60t 兜底"已不可达（门禁=aiStyle{53,123,130,134,137,138} 全有专属分支）；5480 三连真源=case1045 ai[1]链
（**1456 原版强制 num=1 单发** :13832-13866）；5479=命中伤×0.33；MinionShot 吃 tag（WhipTag.ts）；
沙漠虎 818/AI_120/hitCooldown 全对表；修星座星方向翻转（:13877 facing 门）。
**A 批 3 待做**：DD2 T2/T3 逐怪概率表(:1240-1442)、钓鱼咬钩窗口(Bobber:51)、攻速配饰差异(Game.ts:9982)、
floatEye/fighter 一期档(Enemy.ts:585,591)、星光斗篷/蜂巢 SpawnStar(Game.ts:8217)。

## A 批 3 完成（tests/a-batch3.test.ts 36 例）
DD2 T2/T3 逐怪概率链全量转录（DD2Event.cs:1240-1442/:1545-1766，多人缩放原版笔误照录）；钓鱼咬钩
AI_061 localAI 累积器模型 1:1（:50762-50937/:19327 窗口=Next(-240,-90)-力）；攻速改 CapAttackSpeeds
倒数档（:28555-28574）——**删除"猛爪手套×2"无据档**；Top5 战士族表移植（fighterFamilies.ts，
僵尸/骷髅/骨甲/稻草人/混沌元素+十余族；Enemy.ts:585/591 兜底实为死分支，真兜底=fighterAI 固定档）。
剩余精确待移植清单在 memory a-batch3-approx-zero.md。
**A 批 4 待做**：星光斗篷/蜂巢 SpawnStar(Game.ts:8217)、Boss AI 残余（克脑幻影/爬行者 267/WoF justHit/
毁灭者出怪概率 2/6850）、floatEye 全族覆盖核对、其余 A 级散点（DarkBlurItem 411 阶化/水槽 sheet 判/神圣火把 0.5 中值）。

## A 批 4 完成（收尾，tests/a-batch4.test.ts 24 例）——A级数值近似清零基本收官
克脑 AI_054 全文重写（**考古：原版无幻影分身=alpha 渐隐瞬移循环**；20 爬行者/1 速缓追/瞬移外推
16×speed/dontTakeDamage 解锁/二阶段 justHit 抵扣）；爬行者 AI_055；Hungry justHit；毁灭者激光真值
公式（Next(4) 累积+阈值每 tick 重掷 Next(1400,26000)）；猪鲨泡泡 StrikeNPC 真身；星光斗篷/蜂巢全值
（override 723-726 优先级/HivePack 公式）；**demonTorch 考古：非计数器是全局三角波**（Main.cs:18089）；
TargetClosest/风气球 num3 实装；DarkBlurItem 411=不存在（盘点讹误）。
**A 级 60 点已消灭绝大部分（批1-4 共 ~26 组）**；仍存活=专家/大师档（等 ScaleStats 批）与未建系统依赖。
**下一批（B 级最大项）**：NPC ScaleStats 专家/大师强度轴（NPC.cs:18081/18106/18448）+玩家受伤倍率 2×/3×。

## B 级最大项完成：ScaleStats 难度强度轴（tests/scale-stats.test.ts 41 例）
新 src/stats/ScaleStats.ts（五件套 1:1 :18081-18659+六曲线+C# 银行家舍入/f32 对齐）；Enemy.fromVanilla
造怪即缩放（hp/damage/defense/kb抗性/value）；玩家受伤 2×/3×=生成端 EnemyDamageMultiplier+
弹幕命中端 hostileDamageScaling（:13770）双路；**Boss 不豁免**（EoC 专家 3640=2800×2×0.65，唯一豁免=
expertHardmode 提前 return :18471）；GetAIOverride_SubstituteSpawn **不存在**（真实=spawner 三处
spawnArmedZombies&&expert 门 :4565/:4624/:4644 已实装）；FTW 种子=Main.Difficulty+1（getGoodWorld）；
存档不持久化缩放值（原版同，天然一致）。专家 Boss 分支一并清（FTW40 爬行者/!ZoneCrimson/饥饿者
专家段/激光 lerp 22→18/星光蜂倍率）。
遗留：旅程强度滑杆(:17245)/gore 392-395 无管线/Boss 硬编码 damagePlayer 未加乘区。
== 近似清零总进度 ==：A 级数值 60 点清完（批1-4）；B 级最大消费面（ScaleStats）已接；
剩余 B 级=未建系统依赖（油漆/钩爪/高尔夫/渔夫任务等 36 项清单在盘点报告）。

## B 批渔获全量化收尾（tests/fishing-full 34 例 + a-batch3 对齐）
渔获 158 条 FishDropRule 全量表（src/data/vanilla-fishing.json，tools/extract-fishing.mjs）+
渔夫任务链（rollAnglerQuest 门禁表/rollAnglerRewards Main→Decoration→Money→Bait 四段 1:1）。
**关键原版语义（测试踩坑）**：①Populate 注册序 RareDrops(:194)在 OceanDrops 之前——
全稀有档开时 Legendary 2423(1/5 无条件)先命中是原版行为；②Ocean stopper(:108)只在本组
命中时挡后续——掷空则 Surface 组照样落地；③2485 是腐化限定（Main.cs:3862 crimson 才拒）。

## B 批高尔夫全量（tests/golf.test.ts 38 例）——26 机制唯一全缺项补齐
src/world/golf/{golfPhysics(BallCollision.cs 逐行+14材质/133tile表),GolfState,golferShop}+GolfBall 重写
（7×7/aiStyle149/球色 GetGolfTrailColor）；Game 接线（进洞 HitSwitch/球座放取/哨子回退罚杆/>10 驱逐/
Golfer 商店五档门槛与台词四档）。**真 bug**：材质表键是原版 tile id，TileStore 是内部 id——
golfVanillaTileId 归一（否则材质阻尼全退化 Default）。等价边界：单人计分/无排行榜 UI/球车未实装。
B 级剩余：钩爪、油漆、TileEntity 框架化、墓园 pass、事件系统段（南瓜霜月日食）等。


## 增补(2026-08-13):boss 击退+头顶血条
- **boss 击退**:原版 SetDefaults 全 boss knockBackResist=0(EoC :8645 证据),JSON 数据全对。事故=当日 fromVanilla 曾把"比例"换算成"抗性=1-比例+0.89 钳"而 hurt() 仍按比例消费 → 语义倒挂(boss 吃 89% 击退/普怪零击退);已回滚为比例直存。**铁律:def.knockbackResist 全链=原版承受比例(0=免疫),hurt/bossAI.ts:528/bossAI_dd2.ts:640 三消费方同语义,勿再换算**。运行时验证:kb=0 受击 vx 不动。
- **头顶血条 boss 不豁免**:DrawInterface_14_EntityHealthBars(Main.cs:45203)对一切 life!=lifeMax 且非 dontTakeDamage 的 NPC 画条,**boss 专门 ×1.5**(45230-45315 type 表),与底部 Boss 大条共存、无时间衰减(打到没满血就一直显示)。Renderer.drawHealthBar 已 1:1(专家克脑 266 豁免/蠕虫段豁免也在)。用户若嫌 boss 头顶条可开设置项,但改默认=偏离原版。

## B 批钩爪全量（tests/grapple.test.ts 28 例）——智能光标"等价空集"最大遗留闭环
32 弹体型号/26 物品全表（射程/回收/锚上限/牵引逐项抄，无折算）；AI_007 三态 1:1（列优先锚盒/
上限杀最旧/黑名单/935 瞬移）；GrappleMovement+GetGrapplingForces（446 反重力/652 静态/865 垂吊/
牵引上限族）；QuickGrapple 双钩交替/月亮轮换；SmartCursor 钩爪锚点集实装。
**纠偏**：原版无"落地自动释放"（RemoveAllGhooks 全调用点=坐骑/床/传送/死亡）；钩中敌人无效果
（蝙蝠钩=牵引14 非自动瞄准）——任务书预期与原版不符已按源码实现。
B 级剩余：油漆、TileEntity 框架化、墓园 pass、南瓜霜月/日食事件段、宇宙四塔事件。


## 增补(2026-08-13):头顶血条锚定修复
- **原版通用 NPC 绘制锚 = 底锚**(Main.cs:24758 真通用分支:`Y=盒底-帧高*scale/2+4+halfH*scale+NPCAddHeight`,origin=帧中心旋转 → 贴图底=盒底+4)。cs:23635 是 371 族特例(中心锚),勿再当通用引用。
- 我们飞行族=中心锚+EoC 显式 +23/+30 下移(2026-08-11 用户拍板,眼球主体居中于盒)——贴图底超盒底 ~57px,血条若按原版"盒底+10"就扎进球内(用户报)。
- 修法:drawEnemy 回填 `Enemy.spriteBottomWorld`(实际贴图底,世界 y,渲染 scratch),drawHealthBar 取 `max(盒底+10+AddH, 贴图底+6)`——保持原版"条悬贴图底下方 6px"的相对关系。实测:box 3142/spriteBottom 3199/barY 3205,像素级确认条在眼球下方。

## B 批油漆系统全量（tests/paint.test.ts 41 例）
Paint.ts（paintColor :77 1:1/MapColor 乘最大通道/暗影中位×0.3/负相反转）+TileStore paint/
paintWall Uint8+独立 RLE 存档通道+.wld 导入落盘（此前读到即丢）+三件套交互（刷=tile 滚=wall，
**通道由工具决定**，同色不扣）+SmartCursor 三策略激活+ChunkCache 乘色 pass+小地图 ABGR 直算
+史莱姆踩漆（并修原误挂 zombieAI→slimeAI 空转 bug）+商店 for 循环段。
**等价边界**：tile 渲染乘色系数在编译 shader 内不可见（Canvas 乘色近似，深层 13-24 渲染=浅层）；
涂层 4668/5344 系统未建恒惰性。**修误挂教训**：slimeColorTick 曾挂 zombieAI 且守卫使空转——
激活遗留近似前先确认挂点。
B 级剩余：TileEntity 框架化、墓园 pass、南瓜霜月/日食事件段、宇宙四塔事件、矿车完整链。

## B 批南瓜月+霜月事件（tests/pumpkin-frost.test.ts 36 例）
**1.4.5.6 已无独立 PumpkinMoon/FrostMoon 类**——逻辑在 NPC.cs（CheckProgress :79243-79518/
出怪表 :2714-3457/分值阈值 :6534）。触发物核对：1844 勋章→南瓜月、**1958 顽皮礼物→霜月**
（"顽皮礼物召南瓜月"是错的）。权威出怪表逐行转录（含三处原版怪癖照抄：南瓜月 14/15/17/18 波
327 独立 if 双刷/wave4 判 325 刷 330 复制粘贴笔误/霜月 14 波可空刷）。修复合并分值表保真度缺陷
（异事件怪计分）。Boss AI_057-063 已在 bossAI_moon_events.ts（前几轮就位，本次对账）。
遗留：pickPumpkinMoonSpawn 双刷需 caller 多产出（Game.ts 并发占用未动，权威表已落地）。
B 级剩余：TileEntity 框架化、墓园 pass、日食事件、宇宙四塔事件、矿车完整链。

## B 批日食+四塔（tests/eclipse-lunar.test.ts 34 例）
**审计先行**：日食主链 95% 已就位（出怪表/掉落/存档/BGM 全对），缺 sundial 冷却清零→模块化 Eclipse.ts；
四塔 LunarEvent.ts 覆盖 ~95%，缺口=updateLunarApocalypse 只挂击杀链（原版 WorldGen.cs:71523 每帧）。
**挖出真 bug**：starCellAI(AI_085) 吸附门写成 !is405——原版是 type==421（cs:39052），致命球 467
（日食怪同 aiStyle）会钉玩家头顶灌 Obstructed(163)；421 瞄 Top 分支也错位。先复现后修。
遗留：日食怪战士族专属行为分支 8 条精确清单（Psycho 潜伏/Nailhead 散射/Eyezor 激光等）。
**B 级剩余**：墓园 pass、TileEntity 框架化、矿车完整链、星璇四塔星柱怪 AI 族细节。

## B 批墓园+日食怪8分支（tests/graveyard-eclipse.test.ts 25 例）
**考古**：墓园不是常规 pass 是 tile 计数群系（SceneMetrics cs:622-635 计数=tile85−向日葵/2、阈值28）；
生成 pass 仅秘密种子专属（getfixedboi 因 !tenthAnniversary 被否决）；Ecto Mist/幽灵外观**原版不存在**。
效果链审计全就位（刷怪变体/BGM13/视觉 lerp/商店门/配方门/成就），唯一缺口=生成 pass+墓志铭
（唯一消费端 WorldGen.cs:25161——玩家墓碑用死亡文本不用墓志铭）。
日食怪 8 分支全移植（Psycho 潜伏/逆向刹车、Nailhead 散射、Eyezor 死光独立段非射击族、Butcher
空免击退、Possessed 爬墙冲刺、Fritz **目标在上跳更高**、DrManFly 射速 7.5/射程 400）；
**日食豁免白天驱散 cs:60694 此前缺失**（日食怪白天刷的一出生就离场）；flag8 不攻门表考古
（460/462/463 **不在**表内原版会攻门）。
**B 级剩余**：TileEntity 框架化、矿车完整链、墓碑 Sign.ReadSign 锚左上格。

## B 批矿车完整链（tests/minecart.test.ts 29 例 + track 35 例 = 64 例）
**审计先行**：MinecartTrack.cs 全量（36 帧表/TrackCollision/FrameTrack/FlipSwitchTrack）已就位——
缺口 11 项全在 Player 侧：脱轨无碰撞穿全图/runSlowdown 错值（反推刹车强 6 倍）/onWrongGround 全链缺/
无输入三分支缺/斜坡重力停摆缺/**默认木质车上不了车**（原版无物品 num4=13 照上车）/27 型坐骑参数
只映射 9 型/撞敌三处偏差（盒错/expert×1.5/击退预除）/**frameTrack 污染非轨道邻格**（家具帧清 0）。
**考古**：36 帧无垂直/电梯段（上下行=TOP/BOTTOM 逐格±1）；压板 2492/增压 2739 非 tile 428。
遗留：鼹鼠车钻掘铺轨/SuperCart 防御+激光（Mount.cs:4794-4800）/轮火花视觉。
B 级核心仅剩 TileEntity 框架化（挂物族已最小等价，框架化属重构非缺功能）。

## 26 机制遗留五项补齐（tests/mechanics-leftovers.test.ts 19 例）
**#1 仇恨**：TryTrackingTarget cs:78485 **曼哈顿距离−aggro**（非欧氏）；旧实现误取 Upgraded 距离门
（**本体源码零调用**是 mod API）；不转身门三条件（itemAnim==0&&aggro<0&&oldTarget）——effectiveTargetDist
+canTargetPlayerAt 统一入口，flyAI 18 格门接线。**#19 击退考古纠错**：Hurt 击退是**固定 4.5/-3.5**
（cs:37908，不按武器 kb 缩放——任务前提不成立已按原版修）。**#20 减益**：DoT 原版序表+感电(144)
双档（静-4/动-16 extra）；**顺带修硬 bug：BUFF_TYPE_BY_VANILLA 用 Object.keys 字符串键，数值枚举
has()/get() 全落空**——读档 buff 恢复链整个坏死，补 Number(t) 复活。#14 生命果审计已存在正确；
#6 考古结论：**月相不影响任何 NPC 掉落**（loot 段零 moonPhase 读点），消费面=钓鱼/商店/刷怪三处已接。
精确遗留：npcTypeNoAggro+1000/动物学家月相轮换货 4430-4441/骷髅商人月相定价。

## 遗留三项清尾（tests/moon-shop-aggro.test.ts 11 例）
**考古纠错**：4430-4441 月相轮换货是**树妖(20)**的（NPCInteractions.cs:491 Shop(20,3)），不是动物学家
（633 是 Shop(633,23)，兽耳尾四相位已接）；动物学家的月相段只有兽耳尾套装。GetSkeletonMerchantPrices
在 1456 是**死代码**（ShopHelper.cs:64 定义零调用，ProcessMood :107 提前 return）——骷髅月相定价
按任务接线但注明"删一行即回退 1456 死码语义"。npcTypeNoAggro 23 类表+1000 罚项（单人 direction
恒 ±1 → 罚项恒生效=表内怪索敌 +1000 曼哈顿）。顺带补 seekDirX 不面向门（cs:78543）。
卖出链（sellValue）确认本仓无消费链，既有缺口未动。

## 卖出链移植（tests/sell-chain.test.ts 18 例）
交互=**Shift+左键**（非拖拽，ItemSlot.cs:185-196）；卖价=value÷5（cs:34732）最小 1 铜；钱币 71-74
豁免；value=0 白送入店；快乐度对卖是 **÷** 且仅商店条目吃 0.8（双向不对称 cs:34935-34936）；
**回购记账全额退**（刚买的按买价原额，卖超量只剩 value/5）；关店清记账。币装不下整体回滚。
遗留：卖出不回落货架（本仓货架无状态）/光标持有物点格出售未接/买入侧既有取整近似登记。

## 微光 oracle 金标对账闭环（tests/shimmer-checkpoint.test.ts 双通道）
扩展 caves-oracle.cs 尾段 7 checkpoint + **RNG 流位置指纹**（StreamHash，正交网格哈希：指纹分叉=掷骰
数分叉）+ 状态恢复通道（oracle 态直跑 runShimmerPass，不受上游 WIP 影响）。**金标抓出两处真偏差**
（都在 TreePass 非微光本体）：①基座帧骰被内嵌 if——原版 Next(3) 无条件掷（cs:30906），以太腔 tuft
恒 false 每树少 1 骰流漂移；②growTreeWithSettings 干身**掷序颠倒**（帧变体先于枝型 cs:30595，注意
GrowTree 是枝型先，两函数不同源勿互搬）→ 修后 ShimmerPass 四段落逐位全等（本体零偏差）。
**连带**：oracle 同步修正 → caves-chain 金标已重生成（underworld 起哈希变）。
备案：真实管线执行序 lakes/slush 位置与原版注册序有偏差（"液体"槽注释认知错，属 pass 数组代理域）。

## 双键清理第1步+备案四项（2026-08-14）
**批次A字段搬移**：基数重测=1227 对/81 驼峰独有字段（tool×35/axePower×7/value×2/wireTool×1/
tile×22/placeStyle×14，远超旧快照 39）全部并入蛇形，tests/dual-key-fields.test.ts 锁定清零+基数
防假绿；遗留 10 值冲突（蛇形=手工修正值保留）+14 重复键。**批次B**：FTW sizeScaleOverride
netIdSpawnScale 膨胀(o+o²)/2+首盒替换+种子二盒；图鉴假人 488 不入图鉴锁死；canDisplayBuffs
仅 FTW 245-248 置 false 且 NPC 侧两消费者未移植（精确登记）；十周年 netID 二次盒=rawW×o×o
怪癖照抄（旧实现只改渲染乘区碰撞盒恒基底=真偏差已修）。

## 矿车尾巴+环境音轨+invalidateAll（2026-08-14）
SuperCart 防御 (int)(2×(1+|vx|/Run×2.5)) + 激光（mech 点 GetMinecartMechPoint/±π4 锥/591 无
type-tag 永不暴击）；鼹鼠车挖掘全链（MinecartDiggerHelper 1:1，2340 轨道消耗+五列 KillTile+
速度钳±1）；轮火花五尘型委派+三档速度门。**Ambient 环境音轨**：AMBIENT_FILES 40 成员（14 个
legacy SoundID 的 wav 全映射）×ambientVol **替换** master 非叠加（:420-429）；Settings 第三滑杆
+持久化。invalidateAll 精确失效已由并行会话落地（chunkSheets 反查+500ms 合批），本批清残留死
兜底。测试 minecart 44/sfx-ambient 6/chunk-cache-precise-invalidate 5。

## 卖出链收尾+四例嫌疑归因（2026-08-14）
光标持有物点空商店格=整叠卖出（ItemSlot case15→4）+buyOnce 货架（Chest.AddItemToShop :651-670，
**卖出确实回货架**——任务前提"不回落货架"被源码推翻）+词缀 value 平方乘区（Item.cs:596-597
`num2*=num2` 曾按白板价收）+买入价链去近似（:34921 折扣 (int) 先截后乘/:34935 银行家舍入/
**收费无 min-1 钳**）。四例嫌疑全测试侧：fishing-r7=漏关 legendary 池（Legendary 1/3 注册序在
VeryRare 前）；map-skins=400ms 防抖 vs 旧测试（fake timers）；draw-side-leftovers=断言钉死旧形态
（54da8bb4 帽位 ai0/微光 alpha 衰减都是更贴原版）；npc-liquid 食人鱼=2.6% 尾部概率（岸加宽 352px
> 物理上限）。**新风险点**：金标冻结可能盖到旧代码（caves-chain 00:23 冻结保留无 bug dungeon 行
但 DungeonPass mtime 00:00——陈旧 watch 实例嫌疑）。**邻接缺口登记**：Shift+点商店行批量买 10
（CanBulkBuy ItemSlot.cs:2874-2881）未实装。

## DungeonPass 入口门骰偏差+Journey 力量菜单+TownNPC 曲线（2026-08-14）
**入口门骰**（金标会话按协议拒绝盖章揪出）：DungeonPass.ts:968 曾误植 `rn(3)==0?doorStyle:13`——
原版入口门 LegacyDungeonEntrance.cs:616 硬编码 13 零掷骰，主题掷骰属 dungeonD 门特征段
（DungeonGlobalDoors.cs:46-53）。多余 Next(3) 使掷骰流 4201 笔起全错位。修复由并行会话落地。
**Journey 力量菜单 15 power 全实现**（JourneyPowers.ts+UI；CreativePowers.cs 逐 power）。
**重大语义纠错：旅程世界缺省 Difficulty=0.5**（此前按经典 1.0 跑是错的）；isExpert/isMaster 改
Difficulty 轴 getter（掉落/掉钱/血月门随滑杆翻转）。上帝模式 damage 早退/血蓝回满/底缘钳位。
刷怪率 0.1×~10× 双段 Remap 进 getSpawnRate；==0 禁刷。存档世界段/玩家段拆分。
**TownNPC 伤害考古翻案**：原版有缩放——GetAttackDamage_ForTownNPC（NPC.cs:7041）×
TownNPCDamageMultiplier 曲线（Journey 2/Classic 1/Expert 1.5/Legendary 2，**无 Master 键→
插值 1.75**，(int) 向零截断）。旧"恒 1"注释错误；自制 townNpcDamageMult 三处偏差已废。
遗留：num2 Boss 击杀进度强化链（大项登记 TownNPC.ts:809）。

## A 批减益/穿甲/DoT/DD2/短剑/luck（2026-08-14，tests armorpen-dot-parity 18+bossAI-dd2 22+weapons-entities 51+luck-drop-chain 6）
**Ichor 考古翻案**：NPC 侧不是防-15 也不是平推——NPC.checkArmorPenetration（NPC.cs:81913）
单池 `armorPen+ichor15+brokenArmor20+betsy40+(int)(def×pct)`，早退 pool≤0，超防钳 def/2，否则
**pool/2 加进伤害**（Projectile.cs:12808），之后才 dmg-def/2。玩家侧才是 def-15。提取器补
armorPenetration 字段恰 25 款入表（85=15/916=50/917·1036=30/1045=50）。**Bleeding 无 DoT**：
仅 bleed→lifeRegenTime=0（:18998），":386 sinceHurt 近似"注释过时销项。vampireSeed=
Main.vampireSeed 门 lifeRegen-=100（种子世界 50HP/s，休眠分支）。**鞭 debuff 全表**
ApplyWhipDebuffs（:11067）913→323/912→324/914→1/1033→362/849→310；"午夜鞭5320"是误记
（5320=治疗药水放置物），849=镰刀鞭 Dark Harvest；310 纯视觉/362 链电标记（TagEffectState 依赖
登记 GAP）。**DD2 疗效**：主语=黑暗魔法师 564/565 三拍下探 50 格出弹 674，**第 40 AI 步**以弹体
中心 1000px 扫描 +min(500,lifeMax−life)——旧近似三偏差（拍点即刻/圆心错/无地面也出）。
**短剑 161**：1.4.5.6 无掷出态（DefaultToShortsword :10158，★extraUpdates=1 每帧 2 子步 8 帧
跑完），938-945 绘制角独享 -π/4×dir，802/842 出膛 ±π/8 抖动。**luck 链已全线接通**——"恒 0"
是 NpcDrops.ts:10 过时注释；真缺口=四叶草族 5574-5576 未入表/多人 closestPlayer 近似本地/
瓢虫 releaseOwner 门恒满足。Enemy.hurt:6557 ichorT 池外平推残差=drop-in 补丁已写注释等窗口。

## Game.ts 残差批（2026-08-15 午夜，tests/game-residuals-b 4 例）
**圣骑士盾两处**：持有侧转移伤走 damagePreview 完整减伤链（原版 :37751 是真 Hurt 调用——
持有者自己的难度防系数+endurance 再结算；dodgeable:false 不吃黑带闪避）；受害实扣改
floor(ok×0.75)（原版 :37746-37747 **前置** ×0.75——两截断之和可比 num2 少 1，整除吞伤
是原版行为，"全额-退25%"会多扣 1）。TeamDamageShare={General,BossNoCheese}（熔岩/尖刺
槽不共享）本仓天然正确（环境伤直调 p.damage 绕过转移块）。**waterWalk 钓鱼加成考古**：
原版 :41546 是 canFloatInWater&&wet（装备4404族**或药水265**，:9595/:12845 每帧重扫；
wet=水/蜂蜜）——原"有资格就+5"过宽已修；**坐椅钓鱼+5**(:41549)依赖玩家坐椅系统=引擎级
缺口。**gore 两处接线**：克脑二阶段 392-395（position 左上角出/初速 Next(-30,31)*0.2）+
碎镜 1085 完整 Kill 链（Item106 音+oldVelocity×0.2 阻尼回退+10×尘330+四片 gore，钩子签名
加 oldVx/oldVy）。**★AmmoID 提取器假数据大事故**：AMMO_ID 表缺 9 枚举名（Flare=931/
Snowball/StyngerBolt/CandyCorn/JackOLantern/Stake/NailFriendly/FallenStar/Acorn）→
**7 件武器 useAmmo=-1、14 件弹药 ammo=-1**（信号枪/星星炮/吹叶机/毒镖枪全族弹药链静默
坏死）——"930 useAmmo=-1 原版语义不接"是错误考古（原版无 -1 语义，纯提取器 bug），全表
补齐重生成后零 -1。**useTime/useAnimation 缺省统一 100**（ResetStats Item.cs:48626-48627，
曾 20/25/30 中位无据；武器 case 必设字段=近死代码兜底）。**gemsOnly 考古翻案**：软核死亡
掉的是**大宝石 1522-1527+3643 大琥珀（夺旗 CTF 旗物）非普通宝石**——"本仓无背包宝石"
前提错，真缺口=CTF 物品族未注册；顺带修起始三件 TurnToAir 不掉落（:53414-53418，曾会把
铜三件也撒出去再发新的）。
**Shift 批量买 10**（卖出批的邻接缺口）：CanBulkBuy（ItemSlot.cs:2874-2881，Shift 按住）
+GetBulkBuyAmount（:2861-2870 常规 10/buyOnce min(10,stack)）→ npcShopBuy 循环化（首件音
i==0/币尽 break/满叠 break/buyOnce 逐次减库存），纯函数 bulkBuyAmount 导出+测试；UI 行
click 透传 shiftKey。
**同日二轮（21:00 窗口）陈旧断言清障 7 例**：①起始三件门收窄——原版 :53414-53418 的
TurnToAir **只在 inventory 主循环**，armor/dye/misc/loadouts 无条件掉（我的首轮实现外扩
到全槽组=真偏差，被 world-difficulty 测试抓住，starterGate 参数化修正）；②projstatus-g7/
buff-r2 断言过时（贴附族 DoT 改层数池驱动——dotLoss 布景须 addStickerStack 一层；ichor
received 100 才是原版真值：pool=15>def → 钳 floor(def/2) **恰抵消半防**，旧"+7 平推"模型废）；
③debug-report maxChunks 复原 384（6db8ae90：contextlost 自适应就位后提回，224 断言过时）；
④l10n 只剩双语=半截构建，build-l10n 重建 12 语言；⑤wiring-devices bossMusic→eventMusic
（4fbe8e22 BGM 链重构改名）；⑥hell-background stub 只给 naturalWidth 而 ImageBitmap 迁移后
读 width/height——stub 补双属性。**教训：并行批次提交时最容易漏的是配套测试的"消费形态"
更新（字段改名/属性形态迁移/布景函数新依赖），收尾清单应含 grep 全仓旧字段名。**

## A 级近似清零收尾批（2026-08-15 深夜：法师 693 书弹/地牢之魂双门/ChaosState 销项）
**693 图书管理员骷髅书弹**（原"通用法师 Dart 兜底"仅剩此消费者）：新 src/entities/BookProj.ts
（Projectile.cs:23742-23809 三态：出生 vy=-3 小跳+6×尘269 → 悬停 45t（vy×0.95/rot 朝玩家
+π/2 每步 0.25 贴近，**后减门 ai1--<=0=第 46 tick 才转化**）→ 冲撞速 9+滚转 |v|×sign×0.03+
纸屑 gore 1007/1008 权 1:2（初速 vx×1.5 后置 +vx 合计 2.5×）+常驻光 (0.3,0.25,0.1)+1/15 尘
269）。dmg13 原值（NPC.cs:21215 无难度包装）；fireCasterVolley 693 分支书锚=tile 50 扫描（20×30
窗随机一本，**本仓放书系统未建恒走兜底** Center+NextVector2Circular(30,15)=单位角×(30,15)×
NextFloat）；通用 Dart 兜底删除（原版 if 链外零弹）。测试 tests/caster-book 4 例。
**地牢之魂双门**：均匀掷→rollLuck(luck, 13/专家9)==0 + **新增 NPC 中心格地牢墙门**
（wallDungeon 7/8/9/94-99，原版 :79875 双门，此前缺墙门=砖外误刷魂）。**ChaosState 销项**：
buff 88 早已真实装（Game case1326 has/apply），audit"独立冷却字段"过时，仅清孤儿注释。
**万圣/圣诞小动物销项**：原版就是均匀 Next(3)!=0（NPC.cs:1544），luck 只在金小动物/侏儒支——
审计描述本身错。**A 级 60 点至此全清**（批1-4+残差+本轮）；剩余=引擎级依赖（坐椅/CTF/tile50
放书）。

## 玩家坐椅系统落地（2026-08-16 凌晨，tests/player-sitting 6 例）——最大引擎级缺口闭环
src/player/PlayerSitting.ts（PlayerSittingHelper.cs 1:1）：GetSittingTargetInfo 逐型
帧偏移全量（椅 15/497 朝向随 frameX+马桶档 frameY/40∈{1,20}+王座 27 档下沉4；梳妆台
102 三列三行让位±1/±2；摇篮 487 frameX%72 局部列；长凳 89 款式 42 档三座位下沉表+端座
±4）；SitDown（CanSnapToPosition 实心门+同位重坐起身+摘钩/下车+锚点+velocity 清零）；
UpdateSitting（椅失效/移动输入/滑轮/坐骑/朝向变 → 起身）。Player 侧：isLockedToATile
物理锁（矿车同款早退段，velocity 恒0）+回血 ×1.3+lifeRegenTime +3（坐/睡同档——顺带
补了睡的 ×1.3）+马桶 TryToPoop（1/600·醉1/200 食tier递降，屎堆 5395 未注册登记）。
Game 接线：interactAt 坐椅分支（SITTABLE_SHEETS×withinSnapRange 40px）+每帧
updateSitting+**钓鱼坐椅+5（:41549）接通**（此前登记的引擎级缺口销项）。
遗留登记：红帽骷髅夜间长凳触发（killClothier 旗标未持久化）；渲染坐姿偏移已接
（drawPlayer 头部 translate facing×offsetForSeat.X / −4+trunc(offsetForSeat.Y)），**坐姿
腿帧=DrawSittingLegs 专属例程未画**（PlayerDrawLayers.cs ~100 行逐腿甲变体旋转四边形，
纯 C 级视觉债）；屎堆 5395 未注册。
**书链（tile 50 Books）调研定案**：StyleOnTable1x1+StyleHorizontal（TileObjectData
addTile(50)），放置帧随机 frameX=18×Next(5)（WorldGen.cs:45379）；物品 149 书 createTile=50
未注册+地牢陈设放书属 worldgen 域（并行会话活跃）——**整链 deferred 到 worldgen 窗口**
（否则注册了也没有获取途径：书只从打掉放置书获得）。CTF 大宝石 1522-1527/3643 为
**vanilla 不可获取内容**（无官方夺旗模式）——有意跳过销项。

## 水中跳跃原版化（2026-08-16，tests/water-jump 6 例）——用户问"水中跳是否对齐"揪出 4 偏差
**考古**（JumpMovement :20384-20510 + 重力链 :24111-24156）：①起跳门=vy==0（踩底/水行
站立）或脚蹼族湿态任意时刻（flag2&&flag3 :20407），均须 releaseJump 边沿——**头露出水面
不是起跳条件**（原版踩水悬停 vy≠0 跳不出水面）；②水中跳=-6.01+jumpHeight 30 平台段
（湿/干同链 sustain 钉速，起跳帧与 sustain **同帧互斥**——平台段全长=起跳帧+30 帧）；
③液体参数档：水 0.2/5.01/30/6.01｜蜂蜜 honeyWet 0.1/3 **跳参数保持干燥档**｜人鱼 merman
0.3/7+sustain 不减计数（:20392-20400 无限游泳）｜手持三叉戟 277（UpdateEquips :12487
**手持即生效**）0.25/6/25/5.51+↑键 0.1/2｜微光 0.15/23/5.51｜岩浆 wet 同链走水档。
**修掉的 4 偏差**：旧"头露水面即可跳+24t 冷却"自制门（水过强）；旧 accel 0.62/4.4 游泳
上浮（原版无脚蹼【完全没有】上浮输入，脚蹼=水中任意重触发完整跳+swimTime 30）；jumpHold
sustain 在干燥分支内（水下跳丢平台段=跳高减半）；蜂蜜走水档（应 0.1/3+干燥跳参）。
**基建**：跳键边沿需 tick 尾快照（jumpEdgePrev——prevInputJump 在 tick 头快照恒同值不可用，
prevInputX 同款尾快照模式）；effJumpSpd 当帧档位传递（湿态液体档，出水瞬间切回——原版
jumpSpeed 字段语义天然结果）。sustain 公共段+人鱼/液体档/trident/lava wet 全接入；
swimTime 字段（动画计时，渲染未消费登记）。
**城镇史莱姆不攻击定案**（2026-08-17 用户问"侍卫史莱姆为何不攻击"，wiki 复核后用户确认）：原版设计如此——
NPCID.Sets.AttackType 全 8 只城镇史莱姆（670/678-684）显式 **-1**（NPCID.cs:4849）→ AI_007
攻击态入口链（NPC.cs:55864 族按 AttackType==0/1/2/3 分流）无匹配永不进攻击态；
AttackTime 同 -1；AttackAverageChance 的 670:1 是无攻击型下的无效残留。本仓一致：
TOWN_ATTACK_TYPE/TIME 表无 670 族条目→attackUpdate 直接 return false ✓。
**"被动攻击"疑云销案**（用户曾据 wiki 措辞质疑，终由本人确认无攻击）：①wiki（中/英+1.4.5 全补丁
日志）无任何"被动攻击"记载——"被动 AI"+信息栏"伤害 10"是误读源；②NPC↔NPC 伤害全路径枚举
（1.4.5.6）仅三条：GetHurtByOtherNPCs(:93605，方向恒敌怪→friendly，攻击方过滤 !friendly)
+ dryadWard/HurtingBees 两个反击分支 + AI_007 攻击态——friendly 史莱姆零命中，damage=10 是
SetDefaults(:17416) 残留死值；③英文 wiki Town NPC 页明文 "town pets have no means of
self-defense"（城镇宠物无自卫手段）——"不主动攻击但有自卫攻击"是普通城镇 NPC 行为。
**顺带登记缺口（未实装）**：城镇 NPC 危险逃离反应（NPC.cs:53884-54023 扫描+触发：
DangerDetectRange（史莱姆 250）+LOS 门 → ai[0]=1 背向逃跑 120+rand(120)；PrettySafe
NPCID.cs:4851 阈外当没看见；逃跑态 :54205-54662 panic 档 1.5+(1-hp/max)×0.9/加速 0.1/
撞深墙转 ai[0]=8 恐慌 240t/悬崖止步；史莱姆湿态强制逃水 :54049）。

## 增补(2026-08-17):全员贴地 +4 统一（用户报"角色/NPC/怪物悬空1-2px"）
**考古定案**：原版绘制全局约定=可见贴图底**恒=盒底+4**（Main.cs:24741 NPC 通用
分支 `Y=盒底−帧高×scale/2+4+半帧高×scale`；PlayerDrawLayers :109/:203/:343 头/
身/腿全层同款 `Position.Y+height−frameH+4f`）——帧底透明边距（~2px）**一并沉入
地面**，原版脚部本就压住地表 ~2px。此前自制的 spriteBottomPad（逐帧测透明行
"贴地"补偿）数学上把可见脚底钉在盒底=视觉恒高 2-4px=悬空感根因。已全家族六处
替换为恒 +4（怪物主路径/legacy 缩放怪/小动物/城镇NPC/纸娃娃活/纸娃娃死亡帧/
Maples），spriteBottomPad+bottomPadCache 删除。spriteBottomWorld 血条回填链随
anchorY 自洽（=盒底+4+eocOff）。教训：**自制"视觉修正"必须先查原版公式——
原版常故意沉入而非贴线**。

## 增补(2026-08-17):睡床锚点 1:1（用户报"睡觉渲染不对"）
床偏移表（BED_VISUAL_OFFSET×frameY/36）与旋转变换原本就对——错在**入住锚点**是
简化版：曾 x=(tx+1)·16/y=(ty−1)·16 硬编码。原版 StartSleeping（SH:156-191）+
GetSleepingTargetInfo（:193-224）：床段左列=点击列−frameX%72/18；**frameY%36≠0
（下半行）行上修−1**；frameX/72 列位 0=朝左床(+1列/方向−1)/1=朝右床(+2列/方向+1)；
anchor=Point(col,row+1)·ToWorld(8,16)，玩家 **Bottom=anchor**（曾按左上角硬置→
水平差 10-16px/垂直差 6-10px/下半行不修=躺姿贴床错位三合一）。测试 2 例锁锚点
数学（player-sitting.test.ts 扩 8 例）。**登记缺口**：移动/跳跃/坐骑输入起床
（SH:103-105 controlLeft..Jump→StopSleeping）未接——本仓仅床格失效与再点起床。

## 增补(2026-08-17 深夜):短剑左刺剑柄朝前修复
用户报"铜短剑右刺正常/左刺剑柄戳"（下午引入）。考古：938-945/802/842 在 Main.cs
:32360 **专属绘制组**——锚=碰撞盒中心+gfxOffY、**origin=贴图中心**、rotation−π/4×sd
（仅 938-945）、dir=spriteDirection<0→FlipHorizontally（:32427 的 FlipVertically 只属
761/762 勿张冠李戴）。我们曾复用通用路径 num145 偏置锚（枢轴≈贴图右缘=剑尖附近）——
右刺角度巧合正常，左刺 −π/4×sd 与镜像叠加后枢轴错位=剑柄朝前。修=drawProj 增
centerAnchor 档（:32361-32367 逐式）。教训：**弹幕绘制不止一个"通用公式"——
:32360 组/num145 组/DrawProj_Spear 三套锚并存，移植先认组**。

## 增补(2026-08-17 深夜二批)::32360 组全排查 + 工具使用转身
**组排查法**：:32360 中心锚组 ∩ 武器可达集 → 逐型对我们绘制路径。命中三修：
①链球族（25 痛球/26 蓝月/35 日怒/63 道/154 肉球/247 花锤/757 血泵链球）也在组内——
FlailProj 曾走 num145 偏置锚（球心枢轴偏移+链条连接点错位）→ centerAnchor；
②79 彩虹光弹原版 num327=0 强制直立（:32420-32423，另带 12 帧前位移 scale 渐缩——
scale 通道 C 级登记）→ 入 PROJ_NO_ROT；③drawProj 其余消费者（回旋镖/长矛/莫洛托夫/
配重/悠悠球/猪鲨刺球）均不在组内无恙。**登记 C 级**：617 星云奥秘 rotation=ai[1]
轨道角（需 AI 态通道，非集合可解）。
**工具使用转身（用户问"原版是否这样"——不是，是缺口）**：ItemCheck :46561-46589
的 ChangeDir 门 flag 对【全物品】默认 true（仅 723/3611 例外）——镐/斧/锤使用同样
转向使用方向；我们工具分支（Game 镐/斧/锤 case）从未更新 facing → 补目标格侧转身。

## 增补(2026-08-18 凌晨):今日全批复查
复查法：逐改动列风险面→深查两高点→大回归。**抓到 1 真隐患**：睡眠物理锁
（Player :1769）注释写"坐/睡态"但条件只判 sitting——sleeping 玩家重力/移动链照跑
（按方向键"边睡边走"+睡中新锚点下重力微坠）。修=锁条件补 sleeping + 原版移动
输入起床（SH:103-105 inputX/inputJump/inputUp/inputDown/ridingMount，判在锁前）。
双光源复查零风险（六发光随从 SetDefaults.light 全无=无双发）。热点状态复查：
spawnVanilla 定义唯一、minionSlotsOf 三消费点齐。280 例大回归全绿。

## 增补(2026-08-18 凌晨):worldgen 21% 栈溢出排查（并行会话中间态）
用户报 worker "Maximum call stack size exceeded"@21%。**先装定位基建**：generateWorld
每 pass run 包 try/catch 重抛 `[pass i/59 名]`（保留 cause 原栈）——用户第二次报错
即自带定位：**19/59 雕像宝箱**。复现法在档：tests/_worldgen-crash.test.ts（SW_GEN_REPRO=1
+ SW_SEED/SW_SIZE 环境变量，默认 skip）。当前树 11 种子×medium+large 全绿——
判定为并行 worldgen 会话中间构建态（CaveHousePass/DungeonPass 当晚正被改，均在
雕像宝箱槽内）。教训：**worker 最小化栈先装 pass 名定位层再排查，别猜 pass**。

## 增补(2026-08-18):worker 21% 栈溢出真根因（两案连环）
**案一（真根因）**：HiveSpiderPass/CaveWallsPass 的 countTiles 是真递归 DFS（帽
3500/1500）——**Chrome worker 栈只有主线程一半**（实测空帧 4544 vs 8840），3500 层
真实帧必爆（主线程测试全绿是假阴性！）。修=显式栈化：逆序压栈出序=递归 pre-order
逐帧等价（封顶/只登记非实心/重复访问计数全保）。金标验证：caves 链 dungeonL 前
全等（dungeonL 分歧=并行会话 DungeonPass WIP 已知项）；hive 8/8 绿。
**案二（探针大坑）**：vite preview 对重建后的【新 hash 文件】做 SPA fallback 回
index.html（1009B text/html）——worker 加载 HTML 解析炸、onerror 空栈，形似"dist
仍崩"！**preview 复测前必须重启**（清单启动时快照）。两案合计排查时长≈2h，教训：
①worker 内装 unhandledrejection/error 自报回传（已落 worldGen.worker.ts，主线程
onerror 拿不到 worker 栈）；②主线程绿≠worker 绿——栈敏感代码必须 worker 实测；
③**生成期递归一律显式栈化**（新铁律：深度>500 的递归禁止进 worker 管线）。
终验：重启 preview 后 dist worker 11 种子（含崩溃种子 363737517/1795905044）全 PASS。

## 增补(2026-08-17/18 五批并档——原为索引五条散行,细节归档于此)

1. **全量未完成审计 0818 批处理**：docs/incomplete-work-audit-2026-08-18.md 200 条
   （35A/110B/36C/19D）；**审计半数为陈注释**（buff 三件/食人鱼枪/许可证链均早已全接）；
   真修=护士×0.8+快乐度链(:39506)、镜头 pan 全档（scope 0.5/1254 2-3·0.8/1299 免右键,
   :62216-62231）；并行会话 tsc 错误清单在案（WATER_TORCH/QUICK_BUFF 族/spawnEmote 重复）。
2. **缺口补齐二批+构建修复**：构建三修复（DungeonPass node:fs 动态化/UI 撞字段合并/
   pass 包 Error cause 兼容）；魂镰 3006 全链（Game 扫描 1100px+清零计数/Buffs SoulDrain
   枚举 v151/Player 回复加成 num5 加算/敌 soulDrainActive 镜像）；对谈表情 70/100/90 是
   id 非时长（并行会话纠错）；并行会话错误快速修法（静态 this. 前缀/CritterLike 单参/
   boss2Already 提升）。
3. **测试套件陈断言清理**：food-chain"多档并存"期望过时（IsFedState 互斥:高档顶掉低档,
   remove 无回落——按原版语义重写）；bg 两套件 recorder 缺 BGBlit 接口（img/fill）——
   GLBgBlit 重构后 drawUnderground 直调 b.fill 炸；并行会话改造会被我的 git stash/checkout
   误伤（stash 前必查 git log 该会话是否刚提交）。
4. **缺口补齐二批收尾**：vanity 3863/3864/3865 DD2 面具 van=1 曾全量重生成覆盖丢失
   （3865 头槽 207 误→209 修正）；终态：tsc 0 错+vite build 绿+全量 vitest 31 失败全属
   并行会话（worldgen 金标 7 套件+town-sitting 危险逃离 2+dungeonL）。
5. **A 批三缺口**：655 摇树蜂巢（GrenadeProj AI_025 落地 vy>5 反弹×0.2/撞墙 killBeehive
   裂 2+Next(3)³蜂/Game.beehive 接线）+608 日曜爆闪（kb15+pierce-1+尘 31×4+6×30×3.7+
   Item14）+447 火星死光（MartianDeathray AI_079 束高逐 tick 扫实心/锚 392|395 窗口门/
   240t）；测试 martian-deathray 4 例。
