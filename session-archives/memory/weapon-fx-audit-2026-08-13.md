---
name: weapon-fx-audit-2026-08-13
description: "武器特效音效全量审计:喵刀502全链1:1(喵叫/彩虹拖尾/迪斯科光/弹跳)+UseSound582件数据驱动+221独占绘制清单(仅502覆盖,清单在docs)"
metadata: 
  node_type: memory
  type: project
  originSessionId: ec878731-1c65-4b4c-9a3b-c8009ce5461a
  modified: 2026-08-14T00:12:56.344Z
---

# 武器特效/音效审计（2026-08-13，喵刀报障触发）

**架构事实**：全原版武器（melee-shoot/投掷/弓枪/magic/shot 兜底）汇入 **Arrow** 类，
弹体贴图 `Projectile_{id}.png` 数据驱动——贴图层全绿；projframes 帧表与原版
`projFrames[]`（Main.cs 散点赋值 275 条）零差异。缺口在特效绘制层与音效层。

**喵刀 3063→弹 502 全链 1:1**（tests/meowmere.test.ts 4 例）：
- 1.4.5.6 喵刀射 **502**（旧版 998 已废弃——勿"修正"成 998）
- 弹跳（HandleMovement :16794 专支，先于通用 aiStyle-8 tink 链 :18165 命中——502 不播 tink）：
  ai[0] 计数 ≥5 消亡、全速翻面、前 20t 平飞后 g=0.2
- **喵叫只在撞块弹跳**（HandleMovement :16794-16812——全库唯一 PlaySound(37)；
  曾误接命中链+弹跳播 tink，2026-08-13 实测复核修正）：style 5+ai0 =
  **Item_57/58.wav**（音量×0.5×style×0.05）；命中怪物【无音无计数】；第 5 弹消亡。
  发射时只有 UseSound Item1 挥击 whoosh（「发射就有喵叫」体感=猫落地弹跳极快）
- 拖尾=Projectile_250.png 沿 oldPos（Main.cs:32495）；点光=迪斯科六段（:19441）
- localNPCHitCooldown 10t 同敌再咬（非 hitSet 永久免疫）
- melee-shoot 穿透已去 min-3 钳（数据驱动，-1→3 近似保留）

**细剑/短剑戳击绘制修正**（铜短剑 3507→弹 938，aiStyle 161）：贴图 RT→LB 对角线剑。
DrawProjDirect 专支（Main.cs:32444）rotation=atan2+π/2 **−π/4×spriteDirection**（:44997 sd=sign(dot(v,X))）
+ dir 规则 sd==-1→FlipHorizontally（:29827）——曾漏 π/4 修正（右刺剑尖扎向右下 45°）与左刺镜像。
XNA flip 先于旋转（绕 origin）↔ canvas rotate 后 scale(-1,1) 等价。像素验证：水平刺=水平剑体。
短剑全部走 SpearProj（kind spear——AI_SHORTSWORD 归 spear），spear kind 不加 swing 无双图。

**第二批（2026-08-13 下午）**：彩虹枪 250/251 专用弹链（RainbowProj.ts——隐形头
每 2t 铺段/段 40s 持续/**全段共享静态免疫共享钟**（每段自衰减塌缩踩坑）/淡入淡出）
+ 泰拉刃 985 Arrow terra 模式（25t 消亡非 timeLeft 90/>8 ×0.94 减速/扇形探墙双阻尼/
分层绘制）。**审计口径修正**：DrawProjDirect 还有 case N→DrawProj_XXX 独占方法
分派（真刃系 972-976/982-985 等 ~30 族）首批 `proj.type ==` 扫描漏了——续批重扫。

**第三批**：星怒 3065→503（Arrow star 模式：天降三剑/线上穿墙越线撞块/alpha 钳 150）。
**勘误**：星怒是 3065 射 503——曾误记 3062→500（3062=猩红之心宠物、500=海盗船员弹），
旗舰表 itemCombat 数据为准。UseSound 命名轨（DD2 等）已被并行会话经
soundtracks.json 接通（我方备份已过期）。下一旗舰：Last Prism 3541→633（充能聚束，channel 语义）。

**第四批**：Last Prism 3541→633/632（PrismProj.ts：channel 晶体+6 光棱/充能三段
散开收敛/满充 180t ×3/LaserScan 截断/线碰撞 5t 免疫/彩虹双 pass）。四大旗舰
（喵刀/彩虹枪/泰拉刃/星怒/棱镜）全部完成。遗留：真刃系 DrawProj_* 方法分派
族（case N 口径 ~30 族）；GetLastPrismHue 玩家名彩蛋不移植。**测试坑**：PrismProj
依赖 game.player 挂手——mock 必须注入 player 否则晶体首帧即死。

**复查批（近似清查）**：① 泰拉刃 985 三错修（ai[1]=18 出生注入→寿命 43t 非 25t/
初速×5 非 shootSpeed——>8 减速段恒不触发属 973 共用段/ai0±1+ai2scale 漏传）；补齐
伴生 **984 旋斩弧**（TerraArc.ts——曾整件漏）。② 棱镜 632 轨道相位两处错修 +
633 aim 先归一。③ 彩虹 251 绘制锚 (−10,−18)。④ 星怒严格 > 边界。
**教训：ai[] 参数全在 Player.ItemCheck 出生注入（48xxx 段）——先查出生再定 AI 常量，勿假设 0。**

**报障批（短剑戳击）**：① 细剑 CutTiles 整段漏接（Projectile.cs:14151：Center 起
10px×scale 线扫草/瓦罐——戳击可清障的机制本体）。② **发射型武器使用期间面向鼠标**
（ItemCheck_Shoot :46578-46590：num=Dot(朝向轴,瞄准向)>0→1 否则 −1，全 itemAnimation
每 useTime tick 重评；723/3611 豁免）——useCombatWeapon/melee-shoot/弓/投掷 四入口
统一补 `facing = cos(ang)>0?1:−1`。**纯近战阔剑不转向**（:19546-19556 useTurn 门——
挥砍期间方向锁定，我方现状恰好一致勿"修"）。

**review 批（短剑修复后自查）**：移动改向门落地——① useTurn 提取入
vanilla-itemcombat.json（1141 件 true，Item.cs 1421 处）；② Player 行走/滑行/钩爪
三处朝向翻转加 itemAnimation 窗门（窗代理=itemAnimTicks>0||useTime>0；useTurn 豁免）；
③ **自查纠偏：门只锁朝向不锁移动**（首版误把整段加速块套进门内=挥砍中不能跑，
原版 :19546 仅 direction）。另：发射型武器转向四处入口的 cos(ang) 以屏幕中心为
原点（缩放/相机前瞻下仍方向正确，与全引擎 px/py 约定一致）。沙丘靴测试红=并行
会话在途 ramp 改动（非本批，改前已红）。

**第五批 真刃系六剑**（SwingArc.ts 配置表驱动）：972/982/983/997/984 旋斩弧
+ 973 伸长斩（锚定 vel×num6²×77/寿命 ai1+65/t≥80 清伤/近墙阻尼）+ 972 飞斩变体
（|ai0|<0.2 分支）+ 五剑出生链（273 双发/675 半伤 973/674 982 伤害 0 视觉弧——
**368/1826 无 shootSpeed 被通用门饿死**，拦截要放在 cwMelee shootSpeed 门之前）。
备案：DrawPrettyStarSparkle 未移植；997 南瓜 321 暂缓。剑弧类命中用
85×scale 旋转盒近似（CanHitWithOwnBody 190/191 扇形）。

**第六批 Zenith 4956→933**（SwingArc.ts 内）：每挥 3 剑/档案=首 4956 后 19 表随机/
vel=(目标−心)/2 非归一=轨道半径/锚点随玩家/椭圆轨道+反旋/本体=【物品贴图
LoadItem(ai[1])】/彩带 polyline。备案：ReachableArea 未接。**坑：GetLerpValue
(from>to) 递减区间必须线性后钳——min/max 早退会写反（测试盯住）。七剑全齐
（泰拉/永夜/真永夜/圣剑/真断钢/无头骑士/Zenith）。**

**翅膀对账（2026-08-13 报障"搜索看不到翅膀"）**：数据层本就 1:1 全齐（WingStats
51 槽全字段含悬浮族四槽 + itemstats wing 槽 47 只；**29-32 槽是原版死槽无物品勿补**）。
缺口=目录注册：只注册了 5 只开发者翅膀（4730/4750/4754/4954/4978）——补注册 42 只
（items.ts，vi_ key 即自动解析图标）。悬浮持有者：1866→22 / 3883→37 / 4954→45。
测试 tests/wing-catalog.test.ts 3 例（47 只全注册/属性抽检/死槽断言）。

**枪族对账（2026-08-13"子弹过大"报障）**：尺寸根因=Arrow 曾硬编码 10×10 盒+
w×w 绘制（原版子弹全族 4×4 盒 + 2×20 曳光贴图×1.2）——并行会话落"构造期按弹型
取 pd0 width/height/scale/extraUpdates + 绘制原生尺寸×scale"修复，我方复核数据
层全对（16 子弹/15 箭/12 火箭/5 飞镖的盒/scale/eu 提取齐）+ 补**目录层**：useAmmo
武器 68 把（枪 21 缺/弓弩 37 缺/发射器 7 全缺/吹箭 3 缺——原仅注册 6 把）+ 弹药
41 件。回归 tests/ranged-catalog.test.ts（子弹 4×4/scale1.2/eu1、207=eu2、
242=eu7 穿 3、箭 10×10）。**注意 503 extraUpdates=1 → 星怒剑每 tick 双子步
（alpha −30/tick 是原版语义——测试已同步 225 断言）**。

**翅膀飞不高报障（根因修复）**：重力段无条件 +GRAVITY——原版重力在 :26545 火箭靴
if 的【else-if 链】上（!flag19→滑翔→飞毯→常规重力 :27033），**扇动 flag19 时整链
跳过 = 飞行期零重力**（WingMovement 0.1/0.5 档独立驱动）。修：`if (flying)
{ grav=0; fallStartY=null; }`。仿真 6.2 格→57.4 格（tests/wing-flight.test.ts
3 例：爬升/wingTime 全耗/滑翔终端 maxFall/3）。**测试坑：手搓世界高 ≤120+出生
点 y>80 会踩世界下 40 格 KillMe 边框死区（cause underground，hp=0 恒冻结）——
世界加高 300。**

**第七批 DrawProj_* 尾件**：974 魔光剑（AI_188：出生在瞄准搜索点非玩家锚——
ZenithTarget 50px→敌人/±20 散布；ai0=1 暴击折进=2 且 dmg×2；36t 消亡；Frame(1,13)
辉光帧 12 双 pass）+ 976 草剑（AI_152 976 分支：弧线 vel.RotatedBy(ai0)；**速度恒 16
——num6 公式按 timeLeft=60 写但默认 3600 恒负钳 0，是 1.4.5.6 实际行为勿"修"**；
穿墙岩浆亡 life 3600 远射）。**测试坑：测试岩浆池勿放飞行路径上（飞叶会撞进自建池）。**

**第八批 内联头部**：充能爆破炮 2882→460/461/459（PrismProj.ts 追加：AI_075 460 分支
channel 蓄力——459 小弹节奏 ai0==1/≤50%10/80-180%30 速度 10、180t 满蓄发 461（×1.5
伤）光束灭即亡、Item15 蓄力音 (5−档)×2 间隔；461=AI_84 锚定线碰撞 22/LaserScan 2400）
+ **5669 真铜短剑→1100**（与 Zenith 同 AI_182 出生链，档案恒 3507——拦截表扩 1100 一行
级接线）。测试 rainbow.test.ts 扩 11 例。伤害榜 top10 现仅剩 857(4722 无名)/684(3827
飞龙 ai1 直射)/1254 狙击枪/261 大地法杖 四件。

**第九批 3827 飞龙剑气 684**：Arrow dragonFade 模式（SetDefaults alpha=255 :7021 →
AI −40/t 渐显 + 尘 60 拖尾 + spriteDirection=direction）+ **垂直线命中盒**（CanHitWithOwnBody
:14693-14701：perp±40px 厚 16 四采样——非通用 16×16 盒）+ 出生垂直偏移（Player.cs:46612：
归一vel.RotatedBy(direction×−π/2)×24 侧向出鞘）。剩 top：857(4722 ai168)/1254(狙击枪
通用路径)/261(1296 大地法杖 ai14)。**坑：spawnAlpha 是 Enemy 专属字段——Arrow 要自立
dragonAlpha（曾借用报 TS2339）。**

**第十批 大地法杖 1296→261**：Arrow boulder 模式（AI_014 弹跳族复用 bounce 衰减 +
重力 0.3 + extraUpdates 1（pd）；慢速消亡 |v|<1.5；墙撞高速 → dig 音+尘爆岩视觉
（:18235-18244）；慢速半伤 :12745 已由 hurt 侧通用链覆盖近似）。1296 目录补注册。
**伤害榜 125+ 全清**；剩 857(4722 ai168 无名)/1254(通用)/及 100 以下内联清单。

**第十一批 日耀喷发 3473→611/612**（SolarEruption.ts）：611 链鞭（AI_075 共享壳
611 专属段 :63918——首帧 Item116/alpha−42 渐显/旋进 spinningpoint=(num50×(ai0/30×2π−π/2))
Y×sin(ai[1]) 双翻转/velocity+=48×spin 30t Kill/命中 Daybreak 189 300t+每 4t 出 612；
绘制=链条拼装帧头(0,2,30,40)rot+π+身段(0,68,30,18)沿 vel 平铺 spd+16−40，第二层
(0,46)单层近似备案）+ 612 爆焰（AI_117：scale=ai1 0.85+rand×1.15 每 tick+0.01/帧
3t×5/15t Kill/Daybreak）。3473 目录补注册。**测试坑：链鞭 vy 抖动大——敌盒 24×18
会被甩飞 miss，测试用 40×40。**

**第十二批 波涌之刃 2880→451**（TideSlash.ts）：aiStyle 81 内联段三阶段
（-1 掷出：alpha +5×spdN 钳 75 → 0 折返：+75 钳 255 → ≥1 瞬击：+15×spdN、
vel ×0.98/spdN、250px 最近敌 alpha≥255 时 100px 随机环落+朝敌 15、ai0+=penetrate
==1 末段 Kill、无敌 Kill、骑乘目标速度）；spdN=max(1,|v|/11)；rotation=vel角+π/4；
tileCollide 仅 -1/0 开。2880 目录补注册。**测试坑：611 链鞭 ai[1] 随机抖动会随机
甩偏 flaky——测试构造后 pin ai1。**

**第十三批 轻量双件**：初代分形剑 4722→857（FirstFractal.ts：AI_168——60t 消亡/
帧 rand15/vel.RotatedBy(ai0±π/120)/Opacity 淡入12末12/rotation=π/4×sd+vel 角；出生链
:47400 随机可追敌+20t 预测或鼠标钳 700、速度 12+rand×2、出生点=目标−30 步旋转弧）+
3870 双足翼龙之怒→711×3（Arrow 711 模式：alpha255 渐显+命中 Betsy's Curse 203 600t
计时直写/30×30 scale0.7 eu1；出生 :48156 出膛 40px+三连扇形各旋 −π/60×dir）。两件
目录补注册。**测试坑：vitest 文件合并跑时 fishing 海洋判定例偶发红（单跑恒绿=
合跑时序抖动，非代码回归）。idempotent 检查用 from '...' 路径串勿用类名（类名在
用例里已出现会跳过 import）。**

**第十四批 屠夫链锯 3098→509**（ChainsawProj.ts）：AI_020 channel 持械（挂手
MountedCenter−size/2、vel=瞄准向每帧直写、断链 Kill、2 帧 2t 交替、Item189 每 20t、
尘 31 火花、rotation=atan2+π/2+1.57 链锯修正）。3098 目录补注册。**测试坑：命中
冷却计法——hitCd 10 在次 tick 才开始减，实际再击窗口≈11t，断言窗要留 5t 余量；
Bash 分类器间歇不可用时用 Write/Edit/Read 工具继续（Python/幂等脚本全废）。**
**伤害榜 100+ 档全清零**（200/190×5/180/170/156/150×2/140/130×2/126/125/120 全 1:1）。

**第十五批 天龙之怒 3858 全链**（SkyDragonFury.ts 四类）：707 左键旋剑
（AI_140：50t 两整圈 Δrot=4π/半程 t=25 松手收/持按重瞄 rot−=π/线盒 ±110 厚 23/
6t 冷却/CutTiles±60/4 股尘 226）+708 右键椭圆弧（AI_142：随 itemAnimation 代理
swing.t、anim2/6/10 出 709±0.384 扇形、半伤 kb+4、ai0∈[12.6,42]×dir）+709 天龙弹
（30 AI 次=15t 寿命/重力 0.3/3 帧/亡爆尘+消费旧圈+新星圈）+1110 星圈（aiStyle77
脉动 [62,80] floor/8t 免疫/4 帧/consume 渐隐）。**右键 alt 接线 = 传送门枪同位
（Game.ts 右键分派 useTime===0 门）；707 useTime=52 近似 SetDummyItemTime 冻结、
onEnd 钳 2=reuseDelay。dmgKind 修正：'shot' 兜底里的 melee 件（636/707）原版走
meleeDamage 乘区勿笼统归 ranged（itemCombat(vid).melee 门）。1110 脉动下界 =
max(0.75+0.25v,0.8−0.2v) 交点 v=1/9 → floor(62.2)=62 非 64。**
**伤害榜 120+ 档 DD2 法杖族核销**：3826 弩车/3834 爆炸机关 = 既有 MinionProj
哨兵路径（BALLISTA/TRAP_TOWER 表已含 679/693）、3543 Daybreak=DaybreakFlare 已在。

**第十六批 月总双魔法**（LunarNebula.ts）：星云烈焰 3542→634/635（20% 强发
Damage×3 else 速−1 :46489；ai1 状态机 0初始化Item34→1搜敌 250/500+视线→6追踪
lerp(vel,朝向×6,1/30)；无重力（:54638 排除表）；Kill=50×50 AoE+Item14+尘爆）+
月耀 3570→645×3 天降（:47072 X 双重散布/Y−600−100i/|dy|钳20 恒下/速÷2/ai1=鼠标Y线
——过线才开 tileCollide=穿墙到线；飞行相 alpha 恒255=不可见（GetAlpha :76171），
视觉全靠尘 229 尾；60px 搜敌→爆炸相 140 盒 126update；命中转爆 :16706 非 Kill）。
**教训：Kill 内二次 Damage() 与首击同帧双记——原版靠 npc.immune 挡，本仓 burst
带 skipId 显式跳过。uncovered json 是陈旧扫描件——伤害榜前列大多已移植/已路由
（946/301/262/641/643 走既有 kind 分发），真缺口要逐件查 aiStyle 路由再定。**
伏笔已销：aiStyle1 重力链对账 2026-08-14 完成——见 [[arrow-gravity-chain-parity]]
（projGravSpec 数据驱动 + Arrow 构造缺省吃规格：箭 0.1@15 缓坠/子弹 flag3 直线/
711 两段式/终端 16；测试 11 条全量回归零破坏）。

**音效数据驱动**：`vanilla-itemusesound.json`（Item.cs SetDefaults 显式 UseSound
582 件/74 个 Item_N）+ `Game.playUseSound(vid, fallback)` 接 5 发射点——
**magic 路径此前恒播 tink**（所有法杖敲石头声）已修。copy-sfx 白名单 +135。
备案：7 命名轨（DD2/DeadCells/LeafBlower/Pal/Abigail）需 Trackable 变体解析。

**220 未覆盖独占绘制**（DrawProjDirect 特例 ∩ 486 射击弹型）：清单固化
`game/docs/weapon-fx-uncovered-2026-08-13.json`，方法论文档
`game/docs/weapon-fx-audit-2026-08-13.md`。旗舰优先序：彩虹枪 1260→弹 250
（aiStyle46，Projectile_250=彩虹条素材）→ Last Prism 633 → 泰拉刃 985 → 星怒 500。
**坑**：喷火器 85 的 98×686 七帧火焰帧数在 Draw 函数里硬编码（非 projFrames）——
帧表审计抓不到，须 Draw 源码级对账；特效修复必须 AI+绘制成对（单接绘制有皮无骨）。

相关：[[dart-proj-visual-port]]（DART_STYLE 敌弹侧）、[[sfx-distance-attenuation]]

**2026-08-19 天顶剑三修**（用户"效果完全不对"）：①**cycle 方向反**——原版 num164=(itemAnimationMax−itemAnimation)/itemTime 动画进度递增（首剑=4956 档案+鼠标直指；第2/3剑=400 内敌锁+±150 散射），我们误用 swing.t/useTime（t 递减=方向反：首剑吃散射、末剑才 4956）→ 改 (dur−t)/useTime；②**extraUpdates=1 漏**——933 AI 每 tick 跑两遍（120 计数 60 tick 耗尽），单跑=轨道慢一倍滞空过久 → fixedUpdate 内 step()×2；③**LimitPointToPlayerReachableArea 漏**（:44828 鼠标目标钳玩家中心 1920×1200 矩形）。proj933=32×32/穿透-1/tileCollide false/ignoreWater ✓。
