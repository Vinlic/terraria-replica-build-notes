---
name: enemy-teleport-port
description: 敌怪传送/闪现全族审计+1:1 修复（caster 12ids 重做/混沌元素/星云脑/King/Queen/Empress）+出怪范围结论
metadata: 
  node_type: memory
  type: project
  originSessionId: d6caec24-1cc3-4182-bea5-29046ee459cf
  modified: 2026-08-13T03:45:00.528Z
---

# 敌怪传送 1:1 审计与修复（2026-08-13，用户令"检查出怪范围+闪现怪特效音效全量"）

## 出怪范围结论（用户 Q1）
原版 GetSpawnArea（NPC.cs:841-876）：生成区半径=屏宽/高×**0.7** 格、safe 拒绝=×0.52——**全部怪统一**。仓库 `rangeX=viewHalf×1.4`（=0.7 全屏）+`safe=viewHalf×1.04`（=0.52）**已 1:1** ✓。例外仅：skyMob 天空层（0.35/0.45 门）、waterTile 水生成、地牢砖墙门、房屋墙——均已在库。登记未移植差异：狙击镜扩圈（:848-862）、双地牢种子 safeArea 减半、高尔夫草地 1/10 拒绝、海盗船 Y 覆写、SpawnOnPlayer 专属落点（245/370/398/316/82/50）、史莱姆雨独立流程。

## 传送族全表（原版四元组 对拍源）
- **共享采样器 AI_AttemptToFindTeleportSpot :18876-18946**（fighterFamilies.attemptToFindTeleportSpot，本批扩 opts：centered/inAir/dungeonWallGate）：100 次 ±range 采样、列下扫、自身 3×3 排除、岩浆门、!inAir 须实心、telefrag 外扩格+玩家 20t 速度外推、**>2000px 曼哈顿直接放弃**。调用参数：caster(20,5)、混沌元素(20,9)、星云脑(20,12,centered,inAir)、MysticFrog(15,8)。
- **Caster aiStyle8 12ids**（Enemy.ts casterAI 本批重做）：ai0 初值 **500**；攻击蓄力点各族表→ai1=30 倒数 **==25 发射**（Imp 24 专属 **==10** 发焰球 25；533 特殊 ai1=181 每 30t×5 发）；提前传送表 283/284≥450→700、281/282≥540→700、285/286>400→650、533≥360→650；**ai0≥650 触发**（失败=整轮 650t 重来）；次帧执行=旧位 Item8+50尘→改写(x*16-w/2+8, y*16-h)→新位 Item8+50尘；ai1=20（Imp 5）压掉发射门；尘色表 CASTeR_TP_DUST（29/45/533→dust27 紫、32→172、693→269 白、283/284→173 绿、285/286→174 红、281/282→175 青、172→106 金、默认 24→dust6 橙）；地牢族门 dungeonWallGate（32/281-286 须地牢砖墙 7-9/94-99——**无墙测试世界会正确拒绝**）。172 符文法师原版=传近身+快离场+受击 alpha 归零（仓库走通用支=登记近似）；533 的 596 弹落点采样未 1:1（用直射 Dart 近似=登记）。
- **混沌元素 120**：ai3 卡死计数≥180（受击/贴身清零）；触发后 **次帧** 到达 FX（ai3==-120→0）：Item8 **仅新位一次** + 新位 20 尘 71 + 旧位（oldPos[2]=两帧前）20 尘相向速度（pos1/pos2 WeakMap 历史）。本批修掉 menuTick 错键。
- **星云脑 420**：480t 周期+受击 1/6 提前；双端 Item8+尘 242 各 20；落点 Center 锚。本批补双端音+修 menu_open 键名 bug（恒静音）。
- **BoC 266**：两相淡入淡出传送**已 1:1 含 Item8**（bossAI.ts:339 新位/:388 旧位）——无需动。
- **King Slime 50**：despawn 传世界右下角（localAI=maxTiles*16）**是原版行为**；本批补**常规周期传送**（ai2 无视线||高差>160 累计≥300+落地 → 传送循环；antiCheese la0≥360||>2000px→玩家脚底；FindTeleportSpot 外环±10/内环±7 带环带排除+视线门，退 (±6,±2) 再退脚底）；执行段补 Gore734 王冠粒子+缩身/淡入两态**每帧 10 尘 4 蓝 (78,136,255)**（dest 存 WeakMap 像素 Bottom 锚）。**无传送音**（原版即无）。
- **Queen 657**：触发已对（ai3≥300 无视线||高差>320 ×1.5）；本批修尘节律=消散/显形两态**每帧 10 尘** GetDustColor 粉蓝 lerp（近似双色抽样）；**无音效**（原版即无）。
- **Empress 636**：半血变身传送=**纯 position 改写无 dust 无传送音**——本批删掉错加的 roar+黄尘；**Item161 状态开始一次**（:47036，wav 已拷入 public/sounds）。
- **月亮领主 398**：>2400px 归位=纯改写无 FX（与原版 ML 行为一致，未动）。
- **雕像宝箱怪 690**：屏外伪装传送无 FX（玩家不可见，未动）。

## 出生时刻特效（对照结论）
普通怪出生**全部静默**（NewNPC :81524-81576 无 FX 分支）——仓库一致 ✓。例外四族：DD2 fighter 出怪门淡入+DD2_EtherianPortalSpawnEnemy 音（部分在库，音素材缺=登记）；aiStyle86 472/521 出生 Item8+螺旋尘（521 有 Item_8 在 lunar_misc）；172 淡入。

## 依赖缺口登记
- **捕虫网/捕捉子系统不存在** → Mystic Frog 687 捕获传送（Teleport style13：每侧 Item8+21 尘 27）依赖它，未做。
- 出怪范围五项小差异（见上）。
- 172 近身单传/离场、533 弹 596 落点采样：近似登记。

## 坑
- caster 单测断言：落点可能距原位<8 格→用 Item8 音判传送勿用位移阈值；283 地牢族须测试世界补墙 7-9。
- 测试 dayTime 字段默认 true（直调 spawnAnNPC 须手工置位——同雪原审计坑）。
- 音效：`game.playSfxFiles(['Item_8'], 1, x, y)` 直播原版 wav；SfxName 键名 bug 恒静音（menu_open→menuOpen 已修）。

关联 [[spawner-vanilla-alignment]] [[approx-zero-project]]


## review+下一步批（同日）
- 广域回归绿（32+31+11+13+6 批次）；caster 语义逐条对拍 vanilla ✓（顺序：dest执行→ai0+1→蓄力点→触发→弹幕；Imp==10/533 %30 表达式照抄；533 实发 4 发：120/90/60/30——150/30==5 不满足 <5）。多文件一次跑崩"no tests"=瞬时 collect 崩溃，单跑即绿。
- PostCheckChosenSpawnTile 补两门：落脚上两格液体非岩浆→微光(4)/蜂蜜(3)拒绝（:931-940，liquidType 编码 水1/岩浆2/蜜3/微光4）；高尔夫草地 477/492 非事件态 1/10 整帧拒绝（:943-947，invasion 用 invaders 近前线代理，moonEvent null 须判空）。
- 月总 SpawnOnPlayer 160→150px 对齐（case 398）。
- 不可独立做（依赖登记）：狙击镜扩圈=物品 1254/1299 不在库；海盗船 491=多部件飞行体缺；Duke 钓饵链=松露虫 2671 未接进 fishing；533 弹 596=投射物数据表无此 id。幽灵 316 已在墓地池（:81314 收紧属 SpawnOnPlayer 通用链，本仓少消费方）；史莱姆雨流程已在库 ✓。

## 缺口全量补齐批（同日第二轮，用户令"缺口全量补齐"）
- **捕虫网捕捉**（Game.netCatchCritter）：1991/3183/4821 网特判过 melee 门（:42962）；CRITTER_CATCH_BY_NPC 18 条表（46→2019…447→2894，螃蟹 67 无 catchItem=不可捕）；捕获物 spawnDrop 玩家中心秒拾（noGrabDelay 语义，**冒烟须等 2s**）+critter dead；687 神秘青蛙=attemptToFindTeleportSpot(15,8)+Teleport style13 双侧 Item8+21 尘、失败 Poof 消散（**687 未注册小动物=休眠待接**）。释放=CRITTER_RELEASE_BY_ITEM 反查+鼠标格非实心放出（:43377/:80900）。坑：VANILLA_ITEM_KEY_BY_ID 是驼峰键且双注册（ITEM_BY_KEY 查得到）。
- **Duke 松露虫链**（Bobber.ts）：2673 fishingCheck 特判=两侧海洋 X<380/>w-380 && 池液>1000 && 无 370 → 咬钩窗（-280..-160）truffleBite 标记、**永不出鱼**；窗口逃脱清标记；reel 返 -1 哨兵→Game 落浮标+100px 召 370+公告；consumeBait 2673 必耗。坑：biteT getter=ai1<0。
- **海盗船 491**：AI/分发/掉落/数据早已 1:1（flyingDutchmanAI+dutchmanCannonAI）——补三件：①VanillaSpawner 生成分支（进度>50%+1/20+!any(491)+41×30 净空+(spawnTileY-10)*16 Bottom 锚）；②Extra_40..45 六张贴图入库（whitelist MISC）+Renderer.drawDutchman 独占分支（OriginFlip(208,460) 锚/旗 4f/桨 8f×5/四帆/4 炮代画 NPC_492 九帧=ai2 行；flip=facing===-1）+492 船在世时跳过独立绘制（hide 语义）；③聚合血条（PirateShipBigProgressBar：总 8000 恒定=Σ炮 hp，boss 槽空且 491 在屏时画）。坑：dd2LocalAI 是模块私有 WeakMap→导出 dutchmanAnim 给渲染。
- **弹 596/129**：DART_STYLE[596]（8×8 aiStyle107 homing range2400 spd5 lerp40 拖尾紫）+533 volley 落点采样（玩家±6 格排除双邻域+非激活+非岩浆+±2 无实心，50 次，>2000px 直发）；[129] 符文爆弹（速 10 伤 40 ±10 抖动）172 专属分支。**596 其实在 vanilla-projectiles.json（此前 node 查法坏误报缺）**。
- **狙击镜扩圈**：spawner.scopeNum3 字段（Game 每帧求值：手持 1254/1299 或装备 1299 → 1.25/1.5/2.0 档）→ range/safe 各加 viewHalf/num3。**vi_ 物品运行时全量自动注册（items.ts 静态 grep 查不到=误报缺）**。
- **DD2 出怪门音**：`playSfx('spawn')` 键不存在=三处恒静音 bug——素材**在 Sounds/Custom/ 且提取管线已拍平到 public/sounds/ 根**（此前查错目录误报缺）→ playSfxFiles 变体随机 ×3 修复。
- **472 出生音**：phantomAI roar→Item_8 修正。**172 符文法师**：volley 点表已对+无音门已有，补 129 单发分支。
- **城镇 NPC 回家传送**（TownNPC）：flag=雨天/夜间/日食/史莱姆雨 && 家±4 格外 && 玩家屏 42 格外（NPC 与家双矩形门）→ 静默传回（三列落位头顶净空）。
- 验证：gaps-smoke 全绿（兔子捕获入包/491+4 炮/贴图 590/56/60/142/零 pageerror）+129 测试绿（唯 kb 语义=并行 WIP）+build ✓。**残留真缺**：687 神秘青蛙未注册小动物（净化粉变 683 链一并缺）；金/防火网 cutExtraTiles；491 血条 expertscale 基线差。

## review+终批（同日第三轮，"缺口也不要遗留"）
- **review 发现真 bug**：普通虫网 1991 也在砍草（原版 :42972 仅金/防火网调 CutTiles）——已修（swingVid!==1991 门）。史莱姆雨 KS 生成核实在库（netId -4 1/200）；Golem 祭坛±20 搜索在库；DD2 玩家塔音效已接（旧记忆"无素材"过期——素材在 Sounds/Custom/ 拍平根目录）。
- **172 符文法师淡入**：spawnAlpha 255 起步 -1/t（:20797-20810），justHit 重置重淡。
- **神秘青蛙 687 全链落地**：critters.ts 注册（weight 0 不入常规池）；spawnFrog 三门（!unlockedSlimeYellowSpawn && rollLuck(luck,30)==0 && !activeIds 687）→ pendingCritterKey 交付（**687 无 vanilla-npcs.json 条目→Game 侧 null 拾取转 Critter，仿 453 转桶模式**；dupe 判定补 critters 桶）；applyPowder 命中→Poof+dead+flag 持久化+TownNPC town_slime_yellow（683 注册 TOWN_NPC_IDS，仿 682 先例）+toast。live 冒烟全绿（转化/旗/网捕传送）。
- **491 血条基线核实**：总量 8000 恒定 vs 炮 hp 缩放和 = **就是原版 PirateShipBigProgressBar 语义**（reference dummy 用未缩放 SetDefaults(492).lifeMax×4）——已忠实，关闭登记。
- **新登记**：686 绑缚紫史莱姆→684 解放链（TOWN_NPC_IDS 无 684/676-681 城镇史莱姆家族，UNLOCKED_SLIME_PURPLE_SPAWN 仍恒 false 占位）；双地牢种子=remix 专属 N/A；316/82 SpawnOnPlayer 收紧=本仓无消费方 N/A。

## 城镇史莱姆家族全链（2026-08-13 终轮，"继续处理遗留"）
**家族勘误**：成员=670（书呆子/蓝）+678-684 七只，非 676-688（676=微光史莱姆敌怪/677=Faeling/688=河豚均无关）；NPCID 字段名与显示名无错位（字段名按"绑着谁"、显示名按"长什么样"）。TOWN_NPC_HEAD_INDEX 已全 8 只（670→46…684→53）。
**八只获取链全落地**：
- 670 蓝=史莱姆王死亡砸出（onEnemyKilled case 50 → flag+TownNPC 上抛）
- 678 绿=入驻轮真派对门（genuineParty 或旗；到访置 unlockedSlimeGreenSpawn WorldGen.cs:5543）
- 679 金=685 抖箱右键/触碰+**金钥匙 327 消耗门**（freeBoundNpc 补，无钥匙 toast 拒绝）
- 680 紫=686 气球绑缚（绑缚触碰解救；原版=戳爆，语义可达近似）
- 681 彩虹=4986 凝胶气球入微光——**断链修复**：spawnNpcByVanilla 对 670-684 转 TownNPC 落 npcs 桶（原先 fromVanilla(681) json 缺条目返 null 只置旗不出怪）
- 682 红=血月钓鱼（已在）✓ 683 黄=净化粉 687（已在）✓
- 684 铜=**ItemDrop 铜盔 89/铜短剑 3507 落可转化史莱姆{1,302,333-336}变身**（GetPickedUpByMonsters_Special :1160-1191）
- 687 地表覆盖补 case-60 落脚开关（:2249-2270 友好轮丛林草：白天 2/3 鹦鹉/其余 SpawnFrog，zone 边缘带）
**渲染/数据修复**：BOUND_NPC_SHEET 补 685/686（绑缚史莱姆此前不渲染！）；json 手补 670/678-681/683-685（extract-npcs 两根因：读 1405 旧源+多 || 条件正则截断——**修提取器重跑有漂移风险，手补为准**）；8 只 extra 0→6（ExtraFramesCount NPCID.cs:4831，行走循环 2..7）。
**入驻轮第二轮**：prio 链尾补 8 条史莱姆（旗门；678 真派对门 genuineParty 非手动派对）。
**l10n 零新增**：SlimeNames_*/Slime*Chatter 在包**顶层**（此前误查 d.Town 子节）+RandomText 已映射全 8 只。
**触碰解救**：boundTouchCheck（%15tick，玩家 AABB 相交→freeBoundNpc；534 税务官除外）——右键保留兜底。
验证：44 测试绿+build ✓+冒烟（684 变身/铜旗/670 构造/extra=6+前批全部）fails:[]。残留登记：史莱姆对话应走 Chatter（CanTalk=false）现为'……'占位=装饰性；686 戳爆变体差异（触碰解救近似）已注。