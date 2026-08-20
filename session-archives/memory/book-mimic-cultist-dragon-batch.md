---
name: book-mimic-cultist-dragon-batch
description: 书怪693/694全链+教徒幻影龙454召唤批：AI_010多状态机/贴书传送/书掉落vi_165链/仪式圈召唤/455-458数据补齐
metadata: 
  node_type: memory
  type: project
  originSessionId: 04569a63-44aa-4669-98a3-b777d15e98f8
  modified: 2026-08-18T10:14:07.781Z
---

B 批（2026-08-18，task #150 收官）：审计四项全落地，tests/book-mimic.test.ts 14 绿。

**694 水书宝箱怪（AI_010 :21552-21888 重写 cursedSkullAI）**：伪装态 3（静止/kb0/justHit→觉醒4）/觉醒 4（80t→活跃0）/冲刺链 flag18（d∈[100,300]，1/3 掷，蓄120t→态2 冲60t→ai2=-300 冷却，速度 14 直线）/咒球链 flag19（d≤500，态1 内 ai2==17 Center+(0,10) 出 NPC 33 水球）/逃逸 flag17（贴脸<100px ai1=-60，<-30 反向 8px/t）。★<100px 重置门是 flag10(694) 专属——曾全族误用。帧机（FindFrame :77905）在 AI 内算 customFrameIdx（Renderer.vanillaFrameIdx 顶部直读），npcFrameT=态切换清零的 frameCounter。34/289 通用档顺带 1:1：旋转=atan2(v)+<0 加 π+spriteDirection 翻转（Renderer stR===10 rotate e.visAngle）+289 justHit 清态。

**693 贴书传送**：attemptToFindTeleportSpotNearBooks（fighterFamilies.ts，:18948-19024）——地牢墙窗随机列→交替方向走到墙面→垂直扫书（玩家 80px 扩展盒拒书）→落点=(书格外侧,书y+1)；±1 盒防原地。InWorld(Point) fluff=0 非 10。casterAI 传送先贴书后落通用。

**spawner 书掷（:2655-2677）**：N(8)→最近书位生 694（ai3=3 伪装态）；else N(10)→693。AI_FindNearbyBook（spawnTile-16 起 32×32 closestBook+屏外门）；掷中无书空过落 num44 掷。findNearestBookForSpawn + tileClearOfPlayerScreens（屏外门抽成格坐标版）。

**书链数据面**：tile50 掉落 KillTile_DropItems case 50（:65709）——frameX==90→vi_165 WaterBolt、其余 vi_149 Book（Game.ts framedSheet===50 分支）；放置帧随机 18*Next(5)（:45379）；桌面 1×1 族 {13,33,49,50,174,372,646} 须 TILE_TABLE_SHEETS（tiles.ts 导出 Main.tileTable 全表）。书=世界生成放（DungeonPass placeOnTableD(x,y-1,BOOKS)——DungeonGlobalPlatforms PlaceBooksChance）；waterbolt 帧 90 在 1456 有 X/Y 互换 typo（Main.tile[placeY,placeY]）几乎不触发——waterbolt 水术主获取=694 2.5% 掉落。法师商店已含 149。

**教徒仪式圈召唤（Projectile 490 :31282-31292）**：age==300 场上无 454→幻影龙头+spawnWormChain(head,5,[455,456,457,458,459],sharedLife)；有→521（AI_086 phantomAI big 档本就齐）。454-459 渐显（:51379-51400）：头无条件 -42/t、段沿链 <85 门、渐隐期 dontTakeDamage+228 紫尘（Enemy 共享尾新块，与 EoW 位移门版并列）。spawnWormChain 扩 segIds+sharedLife 参数（realLifeHost=head 共享 10000 血池）。**455-458 原缺数据**（提取器漏 grouped SetDefaults）——vanilla-npcs.json 手补+454 对齐 1456（100伤/15防/10000HP；旧表 80/10/4000 是陈旧值）。

坑：dash 态漂移——蓄力期逼近会使 d 跌破 100 使 flag18 失效转 flag19（原版同款，测试须把玩家放 ~256px）；书屏外门查【书位】非落点位。

**C 批收尾（同日）**：vi_5395 屎堆注册（vanilla.json 有图标但 itemfunc 缺 createTile→自动注册成无 tile 摆设）+TryToPoop 1:1（**旧版"tier 递降"是自造**——原版整档移除+叠数=⌊剩余秒/3600⌋×tier 钳[3..999]+OnlyBadLuckExtreme(10)×1.2+noGrabDelay100）；{Bartender} 台词走 townName；DungeonPass 书帧 18*Next(5) 补写（掷值曾被丢=恒帧0；帧不入金标哈希安全）+waterbolt 帧按 1456 typo（tile[placeY,placeY] 对角检查）落地；687/睡渔夫两审计项实为已实现（注释过期，已勘误标记）。审计 A 级 35 条现余：坐骑槽UI/高尔夫球车3611/虚空袋/涂层/公告盒编辑/成就页UI/碎块魔杖/gravDir/事件门/RerollVariation/平台锤循环/builderAcc 开关/爬墙坐骑55。

**★金鱼掉恐惧之魂事故（同日修）**：C 批曾把 vi_5395 手写 `item()` 插在自动注册循环【前】——ITEM_DEFS id=数组下标，插入点后全部物品 id 平移+1，按内部 id 反查 vid 的掉落链全体错位。修=删手写条目、tile 走 BLOCK_TILE_BACKFILL 追加 `[5395,666]`（回填改写现成 def 零位移）。tests/item-id-stability.test.ts 钉死：连续 vid 内部 id 严格递增 + 5395 tile 回填。**铁律：自动循环前禁止插 item()；补链一律回填表**。

**createTile 双源回填+覆盖闸门（用户最佳实践质询后落地）**：手维护回填表只是折中非最佳——真实解=①createTile 双源（itemfunc 提取优先，缺时回退 vanilla.json .items.createTile【游戏数据最终态，覆盖提取器解不开的共享算式段 2189 件；双源交集 1042 中 1039 一致，3 件分歧均源码二次赋值、vanilla.json 更准：498=470/1989=470/3977=475】）②tests/item-id-stability.test.ts 覆盖闸门：vanilla.json 声明可放置且 tile 表已注册的物品 def.tile 必须非空（ALLOWLIST_NO_PLACE 登记有意豁免），静默"放置无效"从此必红。★坑：CRITTER_ANCHOR_ITEMS 循环的 `d.tile !== undefined` 跳过门在双源回填后会把锚桩 placeStyle 吞掉——改判 `d.tile !== CRITTER_ANCHOR_TILE`（只挡指向别 tile 的）。
