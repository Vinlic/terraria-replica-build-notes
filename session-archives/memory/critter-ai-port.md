---
name: critter-ai-port
description: 小动物AI全家族1:1移植（2026-08-11）+Critter类退役（08-17）：环境生成/释放/687全走Enemy aiStyle路由，兔子hop=弹跳族误配根因
metadata: 
  node_type: memory
  type: project
  originSessionId: 04569a63-44aa-4669-98a3-b777d15e98f8
  modified: 2026-08-17T08:42:41.133Z
---

# 四轮 review 自审（2026-08-17 夜,5 处真偏差）

**教训:重构后必须回读源码逐门核对,本轮五处全是"门"错**——①企鹅/蝎被
surfaceSpawn 门误拦(原版 case 147/161/53 **无 flag10 深度门**,地下雪/沙照出);
②外门漏 HALLOW_GRASS/HALLOW_MOWED(case 2 四草族=神圣草此前整族不出小动物)+
多出 DIRT(原版泥土 default 空过);③critter npcSlots 兜底 0.1→1(NPC 类默认 1f,
json 无显式值的兔/企鹅各占 1 槽);④洞穴段补金兔 443 无门掷+摘 dayTime——且
纠正自审时的**二次误读**:flag11 宝石未中=空过,无兔兜底(else 46 只属地表支;
判 else 归属时须看整条 if-else-if 链的 flag 分层);⑤DropBait cap 按基型数
(CountNPCS(357|606)金蚯蚓不计/蚱蜢只数 377,grubby+地狱饵才族合计)。另:香蒲
蜻蜓是独立块(tile{2,477,53}+day+!windy+Next(2)==0),与雨替换块(无昼夜风门)
两套门——曾合并共用。深度出生测试两例+双探针复验全绿。

# 三轮收尾（2026-08-17，"禁止登记不修"批——遗留全清零）

**五项全修**：①松鼠黑化 Enemy 实装(CRITTER_TURN_ON_PLAYERS 集,townCritterWalkAI
头部;★RollOnlyBadLuckExtreme **非负运恒 -1 不触发**——须负运才反咬,luck=0 测试
翻车教训)→ai3=2 永久转 fighterAI(25HP/防+6/伤20)。②蝴蝶物种全链:ai2=物种槽
(出生加权 25/22/19/15/10/6/2/1%)+释放 Style 直存(spawnNpcByVanilla 第4参)+
渲染带 (ai2-1)×3+拍翅[0,1,2,1]——修了 24 帧连播跨物种变脸;漂移计时挪 lai0
(原版 localAI[0],曾误写 ai2 覆写物种)。③Flower Boots 全链:accfx 提取器六轮
flowerBoots 模式(3017/3993)+equipStats+DoBootsEffect(每2t/落地/无钩爪/
|vx|+|vy|>1)+四草族帧带(森林 NextFromList 22 值等权/神圣≠90 重掷)+DropBait
×10000。④刷怪帽 nearby 并入 critters 桶 slot 和(NPC.cs:78709 **无 Boss 豁免**/
史莱姆雨蓝史莱姆×0.65/释放 releaseOwner 不计=Enemy.releasedFromItem);594 留
enemies 桶=与原版一体计数同义,偏差消解。⑤DropBait 提为纯函数 src/world/DropBait.
ts(单测锁定:185 帧带 1/6/花靴 1/400→1/4e6 阈值验证/grubby 序贯 1/4→486 再
1/12→487/墓地覆金)+挂 **breakTile 顶部**(一切破坏路径——★185-187 非 tileCut
38 项表核查,原版走镐破坏;tileCut 表提取勿混相邻表!)+noItem(裂砖连锁)不掷。

**Critter 类终删**:687 发光先迁 Enemy(townCritterWalkAI WrappedLerp 光)→
Renderer instanceof/drawCritter 删→Game as Critter 全改 as Enemy→
netCatchCritter 签名 Enemy→critters.ts 只剩捕获 98/释放 93 两表(CRITTER_DEFS/
kind 族死表删)。E2E:_cutbait-probe(镐破坏 40 次→蚯蚓出生/姿势 vy∈[-5,-2.1]/
cap≤5)+_bunny-ai 双探针全绿。

# 全动物 99 只四维审查（2026-08-17 二轮，docs/critter-audit-2026-08-17.md）

**捕获/释放表对账方法论**:提取器三坑——①复合条件 `type==A||B` 只抓首号;②内层
`if(type==C) catchItem=D` 覆写(鸟 74/297/298 三值各异/海马/仙灵三色**独立物品**
4068/4069/4070);③公式族 `catchItem=(short)(base+type-off)` 与 range 条件
(`type>=484&&<=487`)整族漏。**释放表不能由捕获表逆推**——共享物品族原版一律释
基础/走形(261→55 非 230/2019→46 非节日变体/2121→361 非 687[其 catchItem 是死
数据,网捕走传送特例]/2122→362);真值源=Item.cs DefaultToCapturedCritter(金系
case 堆在**四层缩进**,提取须放宽 `\t+case`)。终态:捕获 98/释放 93 双全等。

**出生可达性审查**:蚱蜢/蚯蚓/蛆/魔夜爬虫/地狱饵**不走刷怪链**——真源是
WorldGen.cs:66304 KillTile_DropBait 割植物掷骰(分母表+caps5/5/8/8+金 1/400+
墓地 worm→蛆+背玩家弹跳 vy=Next(-50,-21)×0.1;grubby 序贯两掷 1/4→486 再
1/12→487,**非加法**)。spawner 侧修 4 族:夜猫头鹰 611/689、晨鸟表 297/298/442
(<9:30 且 2/3)、鸟表二(1/2 **无昼夜门**)、沙地蝎 case53 落脚即出;**旧"森林
概率表"(蚯蚓/蚱蜢/鼠混编)+N(15) 包裹+dayTime 外门全是自创近似**——原版尾部表
=金兔→金松鼠→节日→1/3 松鼠→兜底兔,链无昼夜门(夜间兔/松鼠/鸟照出)。已按真
序重构。**教训:spawnTileType 是内部 tile id(T.GRASS=3 非 2)**,测试 setTile
勿用原版 id;昼夜须改 clock.timeOfDay(spawn() 内会用 isDay 覆写字段)。

**遗留全清零**(三轮见上节):黑化/placeStyle/花靴/帽计数/DropBait 挂点全实装。

# Critter 类退役收尾（2026-08-17，"兔子像蚱蜢"修复）

用户报兔子 AI 像蚱蜢——根因是**双系统并存**：Enemy.critterWanderAI（08-11 的
1:1 路由）之外，旧自研 `Critter` 类（entities/Critter.ts，kind=hop/walk/fly）
还在三个出生点活跳：①spawnCritter() 池尾环境生成（每 120t，critters<8）；
②捕获物释放；③spawner pendingCritterKey→687 神秘青蛙。hop kind 把 aiStyle 7
行走族（兔 46/松鼠 299/鼠 300/蛙 361/鸭 362/金兔 443/687——NPCID.Sets.
TownCritter 全家）全套成史莱姆式周期跳（vy=-3.2~-4，50-110t 一跳）；原版它们
**平地恒速行走**（accel 0.07 cap 1），仅越障三档跳（-6/-5/-4.4 ×1.2 上升补），
且**玩家邻近不触发逃离/起跳**（危险扫描只认敌怪+stinky 玩家，NPC.cs:53887）。
蚱蜢 377/446 才是 aiStyle 1 弹跳族。**处置**：三出生点全改 Enemy（释放走
spawnNpcByVanilla 中心锚=ReleaseNPC NewNPC 语义；687 直接 spawnNPC(687)，
json+贴图在位，pendingCritterKey 侧信道已删）；池尾整段退役（环境小动物唯一
来源=spawner friendly 链，向导在镇即 townNPCs=1 门开）。**同修**：
townCritterWalkAI 尾部自创 `onGround && vx*=0.85` 摩擦删（稳态 0.397px/t≈原版
一半；原版行走态零衰减）——测试 critter-walker-parity.test.ts 5 例锁定
（平地 minVy=0/巡航=1.0/玩家贴身不起跳/687 Enemy 化/释放表）。**双类兼容**：
critters 桶消费者四处的 `CRITTER_BY_KEY[c.key]` 对 Enemy 实例静默 undefined
（网捕恒不可捕=真 bug）→ Game.critterVid() vanillaId 优先解析；activeIds 并入
critters 桶（AnyNPCs(687) 门对桶可见）。**遗留**：Critter 类零构造但未删
（Renderer instanceof/drawCritter + EntityManager 桶类型牵连，并行会话活跃期
不扩大爆炸半径）；Enemy.hurt 有 object-dmg 兼容 shim（critters 桶单参调用→5
伤害）。探针 _bunny-ai-probe.mjs（run-probes 注册 6 断言，含确定性
spawnNpcByVanilla(46) 行走采样）。

# 小动物 AI 全量去近似（2026-08-11）

用户拍板"小动物游荡也要完整移植原版，不要用近似"。`critterWanderAI` 的通用近似
（随机踱步+受击窜）已废除，改为 aiStyle 精确路由（Enemy.ts `critterWanderAI` switch）。

## 路由表（99 只小动物 / 13 个 aiStyle）

- 24 鸟 → birdAI（原有）｜1 蚱蜢 → slimeAI（**补走路档**：cs:61479 无玩家 200px 内激愤时
  0.2 慢爬不进跳循环；跳力衰减 vy×0.9/vx×0.6 cs:62088；落地 ai0+3）｜
  16 鱼类小动物 → swimAI（**补 688 河鲀膨胀**（受击 180t 阻尼悬浮）+**615 海豚周期跃出**）
- 新移植：7 → townCritterWalkAI（站/走循环+速度表+台阶跳-5/-6/-4.4+危险逃离+鸭族湿水变形）、
  64 fireflyAI、65 butterflyAI（重写）、66 wormCritterAI、67 snailAI、68 duckFlyAI、
  112 fairyAI、114 dragonflyAI、115 ladybugAI、116 waterStriderAI、118 seahorseAI
- 测试 tests/critter-ai.test.ts 13 例

## 关键语义（易忘）

- **路由双门坑（2026-08-13 线上报障修复）**：AI 家族路由有**两个 switch**——主 switch
  （fixedUpdate，`vanilla.critter` 门后的 else 分支）和 `critterWanderAI` 内部 switch。
  AI_113 风气球 594 只登记在后者，但 594 json **无 critter 字段** → 落主 switch
  `default: zombieAI` 在地上走、aiInit 恒 false → 渲染 ai2=0 画帧 0 灰壳 + 无 slave =
  用户看到"灰色吊起史莱姆无气球"。教训：**新增 aiStyle 路由必须两头都登记**（或只
  登记主 switch——vanilla NPC.AI 无 critter 门，按 aiStyle 单路由才是原版语义）。
  回归测试：a-batch4 A4-7 第 3 例（fixedUpdate 端到端断言 aiInit/ai2/slave ai0=-999/吊篮坐标）。
- AI_113 风气球 594：json frames=1 但贴图 NPC_594.png 是 **8 列横条**——帧 0=灰史莱姆
  壳（吊篮里的史莱姆剪影，被 slave 颜色两遍染色 Main.cs:23380-23406），帧 1-7=气球
  顶盖变体+吊绳；FindFrame frame.Y=ai[2]=Next(7)+1（NPC.cs:68652）。slave 变体
  SetDefaults 负数分支精确值：-4 scale0.6/hp150/dmg5/def5/kb×1.4/色(250,30,90,90)（:7668）、
  -7 scale**1.2**/hp40/dmg12/def6/kb×0.9/色(200,0,255,150)（:7699，曾误 1.05 纯缩放）、
  -3 scale0.9/hp14/dmg6/def0/kb×1.2/色(0,220,40,100)（:7658）。
- **AI_007 小动物与城镇 NPC 同方法**（cs:53366，TownCritter 区分）——速度表：
  松鼠族 1.5、龟陆 0.5/水 2（625 2.5）、鼠类 2 且不跳改转身、青蛙水中窜 maxX×10；
  跳跃上升 ×1.2；鸭/海鸥/鷿鷈行走形(362/364/602/608) wet 或 |vy|>4 → Transform(+1)
- **68 飞形落地 Transform(type-1) 无条件**（363→362 等）——曾写 `if(ground>363)` 漏了 363 自身
- **374 松露虫**：玩家 160px 内 90t → y+=16 Transform(375)，375 是**穿墙逃离**蠕虫
  （wormAI 反向）——tryTransformTo 加 allowEmbedded 参数跳过实心适配检查
- 蝴蝶/萤火虫垂直避障（下4实心/上30全空反向）每帧钉扎会与开阔天空互搏 →
  惯性过冲可能触地；测试用洞穴顶棚消除上方规则干扰
- ai0 默认 -1120（史莱姆初值）坑了所有新 AI：每个用 ai0 当状态/计时的入口都要
  `if (ai0 < 0) ai0 = 初始态`
- 白天消失是伪命题：无一小动物 AI 内按 dayTime 消失（萤火虫白天只不发光）；刷怪昼夜在 spawner 侧

## 未移植备案（小动物侧）

- ~~萤火虫/发光蜗牛动态光照~~ **已补齐（同日二轮）**：Enemy 新增 `lightRGB` 字段（AI 每 tick 重写、
  fixedUpdate 头清 null），Game 渲染前扫 enemies+critters 两桶落入 lighting.addLight——
  萤火虫族闪烁（cs:34412：间隔 30-180、发光 10-30 帧、**昼地表不亮**（!dayTime||y>worldSurface+10 门）、
  色表 358 紫蓝/654 橙红/其余绿黄 ×随机 scale 0.75-1.11（ai3，同时写 vanillaScale 影响渲染））；
  发光蜗牛 360 (0.1,0.2,0.7)/熔岩蜗牛 655 (0.6,0.3,0.1) 恒定；魔化夜 crawler 484 每帧 90-111% 抖动紫光。
  **测试坑：测试用 World 的 groundLevel 默认 0（真实世界由生成期赋值），不设会让"地下"判定恒真**
- 蜗牛四象限 rotation 视觉、仙灵状态 2-7 宝箱引导链（需宝箱搜索基建）、661 帝皇蝶离神圣渐隐、
  瓢虫幸运钩子（Player.Luck 侧）、114 蜻蜓香蒲锚点迁移、蚱蜢出生 90t friendly 窗口、企鹅 localAI[0] 帧参数

## 浮空岛深空不变量（sky-invariant，同日顺手修）

岛放置下限 90（原版字面）时：列顶游走再上漂最多 13 格 + 岛树最高 29 格 → 树冠探进 y<60 深空，
`tests/sky-invariant.test.ts` 稳定红。补偿下限到 **102**（StructuresPass，注释说明原版岛树是
随机游走找点种植不贴最高凸起故 90 即可）。定位法：vitest 临时探针 dump 岛列（grass 在 86、树到 57）。

相关：[[enemy-ranged-transform-audit]] [[vanilla-npc-port]] [[wall-creeper-ai40-port]]
