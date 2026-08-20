# A 级近似清零 第三批（a-batch3）

日期：2026-08-12。四项全部落地，测试 tests/a-batch3.test.ts（36 例）。

## 1. DD2 T2/T3 出怪概率表 1:1
src/world/OldOnesArmy.ts：`spawnMonsterD2`（DD2Event.cs:1240-1442）/ `spawnMonsterD3`
（:1545-1766）逐行转录；旧"等波表等权出怪"档删除。要点：
- 配额 T2 num=50/num2(562)=5→8→10→12/num3(559)=5→7/num4(568)=2/num5(572)=8→12/num6(570)=3→5；
  T3 num=60/num2(563)=7→9→12→15/num3(560)=7→10/num4(569)=2→3/num5(573)=12→18/num6(571)=4→6/num7(578)=4。
- 多人缩放 :1267-1275/:1578-1586：`for i=1..ActivePlayersCount-1`，且原版笔误照录——
  num5/num6 引用的是基线 num（`num*1.3`/`num*1.35`）而非自身。host 新增 `activePlayersCount()`
  （Game 接 `1 + net.players.size`）。
- T3 波 6 是两条独立 if 链（:1699-1710 与 :1711-1731，中间无 else）→ 一拍可双组。
- 基线档"双出"语义（556 可选 + 553 必出 等）在 T2 波 3/6/7、T3 波 1/2/5/6/7。

## 2. 钓鱼咬钩（Bobber.ts 重写）
- 等待 = localAI[1] 累积器（Projectile.cs:50897-50915）：每 tick `+⌊力/30⌋ + Next(1,3)
  + (Next(300)<力 ? Next(1,3) : 0) + (Next(60)==0 ? 60 : 0)`，>660 → FishingCheck。
- 咬钩门（FishingCheck :19179-19184）：`Next(100) <= ⌊(力+75)/2⌋` 才真咬，否则空拍重来。
- 窗口（SetFishingCheckResults :19334/:19344）：`ai[1] = Next(-240,-90) - 力`，每 tick
  `+= Next(1,5)`，归零即逃脱（渔获作废，:50918-50934）。biteT getter = ceil(-ai1)。
- 水体段（TryBuildFishingContext :19208-19249 + GetFishingPondState :20170-20201 1:1）：
  池宽横向扩张（边界 10/W-10）× 逐列下数（H-10 截断），蜂蜜 ×1.5；<75 不咬；
  atmo = ⌊(Y-(60+10(W/4200)²))/(地表/6)⌋ 截 [0.25,1] → waterNeeded=300×atmo，
  quality<1 时力按比例缩。
- 浮标入液后中心对齐液行中部（原版 GetWaterLine 沉到液面下、Center/16 落液格内）。
- 海洋判定（:19886 1:1）：`Y<worldSurface && (X<380 || X>W-380) && 水体>1000` 三条件。
- 旧固定档（90-300t 等待 / 60t 窗口）已废；fishing-r7 两例同步改语义。

## 3. 攻速配饰
- Player.attackSpeedMult = CapAttackSpeeds 倒数档（Player.cs:28555-28574）：
  `raw = (1+装备meleeSpeed)×醉酒1.1×狼人1.051×虚弱0.949×甲虫球×食物档`，
  返回 `raw>3 ? 1/3 : 1/raw`。**原"猛爪手套 ×2"档删除**——原版 211 只给
  meleeSpeed+=0.12（:14559-14562）+ autoReuseGlove，0.12 已在 vanilla-accfx.json。
- `meleeDamageBonus`（猛爪 +5）删除：原版 211/897 无近战伤害加成（1343/936 的 +12% 走 accfx）。
- 力量手套族 autoReuseGlove（BEHAVIOR_FX 211/897/1343/936/3992）：近战自动连挥，
  Game.useItem 近战分支 `cwMelee.autoReuse || gloveReuse`，唯 type 3030 除外
  （TryAllowingItemReuse :52036-52053）。
- 远端挥舞时长改用代理自身 attackSpeedMult（msg5 已同步远端盔甲）——
  "攻速配饰远端不可见取基础值"档退役。
- buff-r1/equip-stats/food-chain 三处旧语义断言（1.1/1.12/1.05）改为倒数。

## 4. AI_003 逐族切片（新文件 src/entities/fighterFamilies.ts）
aiStyle 分布扫描（public/sprites/vanilla-npcs.json，658 型）：3=186 / 7=71 / 6=43 /
1=25 / 107=20 / 5=17 / 14=17 / 2=13 / 16=13 / 8=12 …；Enemy.ts:585/591（case 74/75 的
else 兜底）经查为死分支——aiStyle 74 全部两型（388/418）与 75 全部六型
（390/392/393/394/416/492）均已被 dispatch 条件覆盖。真正的兜底是 fighterAI 的
固定移动档（加速 0.1/限速 ±1）。
本批按"频率×影响面"Top5 落地 NPC.cs:57799-58800 横向移动 else-if 链全表
（fighterMoveSpec，逐分支行号注释）：
1. 僵尸族 default 档 num108（132→0.95/186→1.1/189→0.8 …）+ scaleBoost 族
2. 骷髅族 num84（21→1.5/201→1.1/202→0.9/342 scale 档）
3. 骨甲三族 269-280 num85（1.0-3.25，恒 scaleBoost）
4. 稻草人 305-314 num86（1.0-2.25）
5. 混沌元素 120（3 档+逆行 0.99）+ 3 档组 166/213/258/528/529
另有 159/349、199、二速族（104/77/197/163…）、小丑 109、木乃伊族（半血激怒 1→2）、
骨李 287、冰雪巨人 243 / 独眼僵尸 251（HP 动态档）、美杜莎 480/僵尸人鱼 586（越伤越快）、
火星工程师 386、屠夫 460（分段加速）、391/427/415/419/518/532、蚁狮冲锋兽 508/580/582
（平滑逼近式 :58526-58612）、血僵尸 489（距离减速）、螃蟹/海螺/幼虫 0.5 档。
行为型：混沌元素 ai[3] 卡死计数（:57504-57545）+ 传送（:57431-57460 演出 / :60679-60696
触发 / AI_AttemptToFindTeleportSpot :18876-18946 1:1，telefrag 预防含 20t 速度外推）；
沼泽怪 166 伏击（:56327-56360）。
射击族排除表（:58719）返回 null——原版这些型横向移动链上无分支（弓手不走路）。

## AI_002/AI_003 待移植精确清单（只登记，不许近似）
AI_002（:52673-53150）：170/171/180 Pigron（:52675/:52725）、116 The Hungry（:52824）、
133 Wandering Eye（:52901，半血激怒已有简化）、2/133/190-194 振翅音（:53109）。
AI_003：624 地精石化+游走（:56252/:57711-57720）、466（:56290）、461 深海怪游泳形态
（:56361-56444）、586 僵尸人鱼形态（:56445）、111 哥布林弓手伏击 ai[3]<0（:57367-57417，
需出生侧注入）、482 花岗岩傀儡（:56646）、480 美杜莎石化凝视（:56751-56886，buff 156）、
471 哥布林术士（:56886）、415 Drakomire 骑乘（:57181）、427/428 外星幼虫/蜂
（:57250/:57281）、463 钉头受击放钉（:57547-57590）、469 The Possessed（:57626）、
462 Fritz 冲刺（:57678）、305-309 稻草人扑跳（:58231-58242）、
430-436/494/495/591 扑咬突进（:58669-58718，**本批暂走 legacy 通用档**）、
425 冲刺（:58910+）、525-527 光源（渲染层）、flag8 开门白名单（:57468/:60383——
本作战士开门未按此表过滤，僵尸能开门、弓手不能）。
射击族（:59464-60120）走一期 RANGED_TABLE（Enemy.ts）+ 本批排除表；逐 type 弹道
微差（散布/drop/弹速表内已录，MultiShot 292/424、GetChaseResults 426 预判未接）。

## 回归
- tsc 零新增（仅他人 WIP：_gem-dist-audit/_ghost 两文件既有错）。
- 全量 vitest：本批相关 8 文件全绿；剩余失败均为他人 WIP（worldgen TrackGenerator
  ReferenceError 链 caves-checkpoint/world-final-hash/hive、debug-report hoverRing、
  luck/shimmer 链），已隔离确认与本批无关。
- enemy-shooters 弓手例出生行 59→57（身高 40px 嵌地板；弓手不再走路后无跳脱出）。
