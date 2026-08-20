---
name: enemy-ranged-transform-audit
description: 敌怪弹幕+形态互转全量审计（2026-08-11）：已移植清单、ai 字段初值陷阱、原版反直觉门、遗留未移植项
metadata: 
  node_type: memory
  type: project
  originSessionId: 04569a63-44aa-4669-98a3-b777d15e98f8
  modified: 2026-08-13T02:45:09.904Z
---

# 敌怪弹幕与形态互转审计（2026-08-11）

双代理对照审计（原版 NPC.cs 全发射点 vs 我方实现），修复后 263 测试全绿。

**Why**: 用户问"还有没有类似爬墙蜘蛛的问题 + 弹幕怪是否移植正确"。系统性差集如下。

## 形态互转（Transform 全表，grep ".Transform(" NPC.cs）

已移植：蜘蛛 164↔165 族、**158↔159 VampireBat↔Vampire**（cs:23393 玩家下方 200px+视线→落地化人形；59236 距>300 化回）、
**195 LostGirl→196 Nymph**（aiStyle 42，cs:30281：靠近 200px+视线/被推动/受伤任一 → ai0=1 → 21t 变身；AI_042 无移动代码纯站立）、
**198 Lihzahrd→199**（HP≤55% 激怒，cs:57422）。
有意不做：城镇史莱姆解锁 685→679/684、微光 92524、兔子/金鱼腐化 93124、鸭子网捕 362↔363、
松露虫 374→375（受惊钻地）、Nutcracker 348→349（霜月）、EoW 分段 14→13/15（断链分裂，wormAI 未支持）、
OwlMimic 689→317、Mechdusa 134→136。
`tryTransformTo` 是通用机制，后续新转换对直接复用。

## 弹幕（对照表要点）

已补：黄蜂 42/176/231-235 毒刺（**反直觉门 cs:51161：玩家待机未挥动 → 计数清零，只有挥动/潜行才射**！
itemAnimation 用 player.useTime>0 近似）、腐化者 94 唾液、哈比 48 三连羽、恶魔 62/66 飞镰、红恶魔 156 三叉戟、
蜗牛怪 122/冰元素 169（充能机 localAI>120+视线→充能、122@32/169@16 发射、出 700px 取消、受击清）、
脓水粘怪 268 金雨、爬行者 101 诅咒焰（**回退 ai3=100 重试语义**）、巨型诅咒颅 289（500px 内 0→1 冲刺状态机、段内 t20 发射）、
尖刺史莱姆 184/535/204（单发抛物线；专家五连未启用）、战士射击表扩展 110/206/290/291/292(burst×4)/293/449-452/481/498-506
（参数全在 RANGED_TABLE，含 drop 系数/spread/枪口偏移/burst）、冰雪巨人 243（HP 比缩放阈值）、岩石巨人 631（100t 前摇 t68 发射）。

**五类"假弹幕"是 NewNPC 不是 Projectile**：FireImp→NPC25 球、Tim→665、DarkCaster→33、GoblinSorcerer→30、
Corruptor→112（aiStyle 9 追踪球速 5/7）——只 grep Projectile.NewProjectile 会整族漏。

Boss 侧审计结论：弹幕全覆盖（bossAI.shoot→Arrow 贴图弹），无缺漏；仅 bossAI.ts 里 Prime 四臂三处中文注释
id 标反（行为正确）。bossAI.ts 顶部 addProj(MagicProj) 是死代码。

## 陷阱（本轮实踩）

1. **ai0 字段默认 -1120 是史莱姆跳周期专用初值**——新 AI 用 ai0 计数前必须 `if (ai0 < 0) ai0 = 0`
   （lostGirlAI/batAI 射击块都踩过：计数从 -1120 爬起 1000+ tick 不触发）。
   ★EoC 也踩（2026-08-13）：eocAI 状态机只认 ai0∈{0,1,2,3}，-1120 无分支 → 夜晚整段空转
   = 眼悬停不动（F6 面板/自然刷怪两路都触发）——已补入口归一（Enemy.ts eocAI 头）。
   ★全仓清查（2026-08-13 双代理）：**Enemy.ts 修 7 处**——dandelionAI/birdAI（等值门空转：
   蒲公英永不喷籽/鸟永久滞空）、swarmerAI/cursedSkullAI/wallCreeperAI（振荡器钳
   `ai0<-200→0`，原相位漂移 ~20s）、seahorseAI（角度 -1120rad=朝向固化 92°）、plantAI
   （`ai0===-1120` 自愈锚点=当前格，防绕过 spawner 的路径即死）。**bossAI 修 3 处 P1**
   ——moonLordHeadAI（`ai0<-3→0` 放行 -2/-3 运行态）/ancientLightAI（bInit 补归一）/
   dukeBubbleAI（ai0/ai1 复位移出 player 门）。确认安全：入口归一族 11 处+bInit 族 40+
   处+不读 ai0 族 25+ 处。**P2 备案不改**：moonLordHand/moonLeech/ancientDoom/pumpkingBlade/
   skeletronHand/primePart/wofEye/moonLordFreeEye 靠父体 spawnPart 预置+孤儿自毁双保险；
   `(e.ai0||1)` 写法对负值无防护，勿复用。史后仆从 ai0=-500×Next(3) 是合法负预置。
   修后 134 AI 测试全绿（critter-ai/enemy-ai-families/dungeon-ai/enemy-shooters/
   bossAI-×3/boss-summon/boss-hostile-proj-sim）。
2. onGround 未建立前 vy===0 不能当"落地"（出生首 tick 误触发）——尖刺史莱姆第一 tick 就射的根因。
3. 全量套件偶发 1-4 个随机测试失败而单跑全过 = 并行负载抖动（p5/npc-drops 史料同款），重跑即绿；
   随机型测试留大余量（黄蜂毒刺 400→1200 tick）。

## 遗留未移植（有意/待办）

- 专家模式限定弹：蜘蛛 WebSpit（163/236/237/238）、尖刺史莱姆五连、哥布林 666 自爆（getGoodWorld）
- casterAI 细节对表：原版三连在 ai[0]==100/200/300 上膛、倒数 10 生成（我们 15/40/65 tick 近似）、
  弹是 NPC 球非 Dart；hardmode 三法师各有专属弹（293/290/291 proj）
- aiStyle 家族未实现（落 zombieAI 兜底）：19 蚁狮（沙球）、49 雨云（下雨）、102 沙元素（龙卷印记召唤）、
  9 弹幕球本体族、事件军团（DD2 108-112/南瓜霜月 57-62/火星 72-76/星柱 83-97/日食）
- Nailhead 463（受击爆钉）、GiantFungiBulb 260（NewNPC 孢子）、AngryNimbus 250、Mothron 族、
  DesertDjinn 533（印记 596）、LibrarianSkeleton 693（1.4.4 飞书）
- Dart 敌对弹幕是色块渲染（无原版弹贴图）；bossAI.shoot 的 Arrow 才带 Projectile_N 贴图

## 二轮（同日）：AI 家族错误回退消除

全量路由审计（vanilla-npcs.json aiStyle → dispatch）结论：aiStyle 7/24 正确走 TownNPC/critterWander/birdAI；
**9 个家族落 zombieAI 兜底是错的，已 1:1 移植**（tests/enemy-ai-families.test.ts 9 例）：
0 被缚NPC（cs:19774 站立/376/579 水漂；TownNPC.bound 是主路径，Enemy 侧防御）+
**fromVanilla 修 friendly 旗零伤害**（此前被缚NPC contact 10 伤害是 bug）；
17 秃鹫（cs:24079 栖息→200px盒/受击起飞单向，Raven 301 同块）；
19 蚁狮（cs:24465 扎地不动+沙球冷却200；**探脚行必须取盒内最底行(y+h-1)，+2 偏移会把站地误判成扎根**）；
23 飞行武器（cs:25316 冲9/漂100/转120 三态，块内强制穿墙；受击回蓄转——用新增 justHitT/get justHit）；
25 宝箱怪（cs:25621 伪装200px盒→小小小大跳循环 3.5/-4、2.5/-8）；
39 陆龟（cs:29257 待机蓄力>200px+4/t→蓄势30→旋冲10/6→下落→复位；417 Sroller 骨架；496/497 半值）；
41 赫柏林（cs:30017 负倒计时 ai0，+5/t+400/dist 截断加速，小-5/大-9 第3跳；Derpling 177 独立参数）；
44 飞鱼/蚁狮蜂（cs:30999 分轴限速追+失视垂直逃逸；xGate 悬停；同型分离/穿平台未移植）；
56 地牢之魂（cs:32915 (v*100+期望)/101 惯性追踪，穿墙）。

**通用陷阱**：唤醒判定（17/25 的"有速度"门）必须用重力前速度——我们 AI 内先加重力再判会把站立态
每帧误判 vy>0.3 直接唤醒（原版 AI 读速度在重力施放之前）。
渲染补：aiStyle 23/56 rotation；17/25 FindFrame 静止帧0/激活帧1+循环。

仍未移植（落兜底但当前不可达/事件系）：9 弹幕球本体、38 雪人、44 之 587、48 自由头、49 雨云、
57-63 南瓜霜月、71 猪鲨龙卷产物、72-97 火星/星柱/日蚀、99、102-106 沙漠族、108-112 DD2。
critter 游荡仍是通用近似（birdAI 已按 aiStyle 24 接入）。

**蛛网撕破扫描顺序（用户反馈"掉落集中头部"核查，同日）**：触发阻尼本来就是全身碰撞盒
（探针证实脚部网同样生效）；撕网目标格=StickyTiles 返回的第一个重叠网——原版**列优先**
（Collision.cs:3399 外层 X 左→右、内层 Y 顶→下），且 KillTile **直接破坏检测格**（Player.cs:22676）。
我们原为行优先+重扫，已改 1:1：垂直蛛网串从身体最上方（头）开始自上而下撕是**原版行为**
（头先进网）；差异场景是横向蛛网层（原版撕最左列、非最上行）。测试 tests/cobweb.test.ts 第 4 例。

**黄蜂毒刺"已移植却永不发射"根因（同日三修，用户报"黄蜂不射毒针"）**：毒刺代码本身
（swarmerAI Enemy.ts:1738，42/176/231-235）正确，坏在"itemAnimation 用 player.useTime>0 近似"
这一层——**挥击重启门 `!this.swing && useTime===0` 使每个挥击周期漏出恰好 1 帧 useTime==0**
（swing.t 在 tick 末 updateSwingHits 才清，useTime 在 player.fixedUpdate 先归零，重启要等下一帧
updateUse）→ AI 在那一帧看到"待机"→ ai1 清零 → 每周期最多攒 ~spd×1.25（15-50），永不到 130。
原版时序：itemAnimation 在 Player.Update 内归零**同帧**被 ItemCheck 重启，NPC AI（同帧后段）
永远看不到 0 帧。修复：Game.ts 两处挥击门改 `useTime===0 && (!swing || swing.t<=1)`（剑 1875/
镐斧 1892，同帧重启、挥击时长不变）。注意 1934 通用物品分支本就无 !swing 门，无需动。
验证 scripts/_hornet-stinger-probe.mjs 三组：A 直驱+useTime 恒 5 → 3 发 ✓；B useTime=0 → 0 发
（待机门语义保持）✓；C 真实循环持剑按鼠标 → entities.update 时刻 useTime 最小值=1（门闭合）
且真黄蜂端到端射 2 发 ✓。**教训：把原版 player 字段映射到自家近似时，必须核对"AI 每帧可见值
的时序"，不是只对齐数值语义**。

**同类问题全量清扫（同日四修，用户问"检查是否其他有类似问题"）**：把"AI 每帧可见的玩家
状态信号时序/语义"当一类 bug 扫全量——grep 原版 NPC.cs 全部 `itemAnimation`/`stealth` 门只有
两处：黄蜂 cs:51164（已修）+ **战士族远程表 cs:60036-60039（当时漏移植！）**：目标玩家待机
（stealth==0 && itemAnimation==0）→ 视线判 false → 永不开瞄（对 110/111/206/214-216/290-293/
350/379-382/409/411/424/426/449-452/468/481/498-506/520 全表生效）。已补 Enemy.ts fighterAI
开瞄分支 `los = player.useTime > 0`（中途瞄准不受门影响,与原版同）。**清扫确认无恙的**：
哈比 48（cs:23462 只 CanHit 无 idle 门）、蜗牛怪/爬行者/诅咒颅/腐化者/冰雪巨人/岩石巨人各发射块
均无此门；NPC.cs 其余 itemAnimation 读点（78335+/78448/78552 多人 aggo、91965 SoulDrain 武器）
与敌怪 AI 无关；useTime 的运行时读取方全工程只有黄蜂一处+本次新增；`!this.swing` 消费方只有
改掉的两处门+updateSwingHits 早退。测试 tests/enemy-shooters.test.ts 补 110 两例（挥动中射/
待机 -1）。**残余注意**：player.useTime>0 近似 itemAnimation>0 在"喝药/使用物品"期间也成立
（原版喝药同样 itemAnimation>0,语义恰好一致,无需修）。

相关：[[wall-creeper-ai40-port]] [[vanilla-npc-port]] [[mining-model-port]]
