---
name: vanilla-npc-port
description: 怪物移植完成度高：数据+掉落+12 族 AI+群系/水域/小动物(CountsAsCritter)生成全落地；余 Boss 专属 AI/HProjectile 弹幕
metadata: 
  node_type: memory
  type: project
  originSessionId: af6cf2c7-84f1-4f59-9d74-9dc27cdc059e
  modified: 2026-08-10T08:18:20.304Z
---

2026-08-09 原版全量 NPC 移植（用户要求：贴图/行为AI/音效/交互/属性全量）：

- **数据**：`tools/extract-npcs.mjs` → `vanilla-npcs.json` **561/586 种**（lifeMax/damage/defense/knockBackResist/aiStyle/尺寸/音效/帧数/名字；SetDefaults 是 if-else-if 区间链非 switch；`== N` 必须返回 [n,n]）。
- **贴图**：838 张 NPC_*.png 入 public/sprites/vanilla/；`SpriteAtlas.vnpc` 懒加载（竖条帧 frameH=img.height/frames）。
- **音效**：NPC_Hit_1..58 / NPC_Killed_1..27 入 public/sounds；`vanillaSoundName` 映射。
- **掉落**：`tools/extract-npcloot.mjs` 双源（ItemDropDatabase.cs RegisterToNPC/MultipleNPCs+规则变量+数组变量 + NPC.cs NPCLootOld if 块 NewItem 配平解析）→ `vanilla-npcloot.json` **261 怪/1266 条**；`vanillaNpcDrops(id)` 原版物品 id→ITEM_BY_KEY（PascalCase→snake_case）接入 fromVanilla。大坑：Multiple 的 id 段截到闭括号否则链尾数字变 NPC id；NPCLootOld 在 NPC.cs；无块语句跳转只前进不跳块。
- **★ 反编译补全（重要转折）**：Terarria1405（1.4.0.5，curRelease 230）的 `NPC.AI()`/`HitEffect()`/`Projectile.AI()`/`Projectile.Draw()`/`Recipe` 是空壳（"too long to display"——dnSpy 放弃 12 万指令级超长方法，全仓库仅 5 处）。**已用 ilspycmd 9.1 反编译本机 Steam 1.4.5.6 exe** → `Terarria1405/NPC.145.cs`（96371 行，AI() 完整）。重跑：`bash game/tools/decompile-npc.sh`（前置：~/.dotnet .NET8 运行时 + /tmp/ilspy/pkg；**-t 必须全限定名 Terraria.NPC**）。补 Projectile/Recipe：`ilspycmd -t Terraria.Projectile` / `-t Terraria.Recipe.Recipe`。**AI 行为以 1.4.5.6 源为准**（旧编号 aiStyle 两版未变），属性数据仍用 1.4.0.5（与帧数/贴图表对齐）。
- **已移植 AI 家族（12 族全原版核）**：001 史莱姆 / 002 飘浮眼（X±4/Y±2.5、133 激怒 ±6/±4）/ 003 战士（四级跳+台阶步升）/ 005 蜂群（网格量化+摆动+制导）/ 006 蠕虫多段体 / 008 法师（传送+弹幕）/ 014 蝙蝠（撞墙反弹、X 0.1/±4 Y 0.04/±1.5、158/660 特化档）/ **016 游泳（水中 accel 0.1、X±3/Y±2、Arapaima157 0.25/±7、离水上浮；鲨鱼实测水中追击 176px）** / **018 水母（0.98 阻尼漂移+90tick 周期脉冲 7 速游向目标+无目标缓沉）** / **022 幽灵（noTileCollide、目标速 7 Lerp 0.0125 飘忽逼近）** / 026 冲锋（0.07/±6、卡墙折返、跳梯 5×vx 提前量；**chargerAI(maxSpd) 已参数化**）/ **107 ImprovedWalkers（→chargerAI(…,1)：0.07/±1.0 walker 档）**。
- **生成池修正（重要）**：underground 移除 **33**（aiStyle 9、1 血 = 法师弹幕怪，不该自然生成）；hell 移除 **68**（Dungeon Guardian Boss）；nightSurface 移除 **396**（月亮领主手 45000 血）。修后池内 aiStyle 全部被已移植家族覆盖（day[1]/night[2,3,5]/under[2,3,6,8,14]/hell[3,8,14]）。
- **Enemy 数据驱动**：`fromVanilla(id)` 合成 def（knockbackResist 换算 `1-比例` 钳 0.89）；fixedUpdate aiStyle 分发后落入共享尾段（接触伤害/入水声/夜间烧除）；Boss id 集 VANILLA_BOSS_IDS（用户并行加的）。渲染 alpha/scale/facing。
- **生成池**：`poolFor` 四池（白天/夜间地表/洞穴/地狱）+ `window.__swSetPool([id])` 探针确定性开关（main.ts setDebugPool）。
- **探针**（全需确定性池 + 怪传进观测台）：`_npcprobe/_batprobe/_eyeprobe/_swarmprobe/_fighterprobe/_casterprobe(主角回血)/_wormprobe/_chargerprobe(|moved|)/_lootprobe`。教训：到达类断言按速度×距离算窗口；facing 断言用采样时刻相对方位；多法师集火会打死主角致挂机误报。
- **review 修复史**：early-return 跳接触伤害（严重）；击退映射反向；alpha/scale 渲染；noTileCollide 穿墙；P2 类型优先级；背景水层序；岩浆底部变蓝（visTypeA 预填）；战士卡墙谜案=观测窗口不足。
- **★ 群系/水域/小动物生成已落地（2026-08-09 深夜，探针 `_biomeprobe.mjs` 3/3）**：
  - **小动物**：`tools/extract-critters.mjs` 从 Terarria1456 的 `Terraria.ID/NPCID.cs` **CountsAsCritter 表（99 id）**+ SetDefaults 提取 → vanilla-npcs.json 补 64/更 35 条（兔子46/鸟74/松鼠299/鼠300/蚯蚓357/蚱蜢377 带全数据）。原版小动物 = `Enemy.fromVanilla` 进 **critters 桶**（spawnCritter 里白天 45% 分支），`critterWanderAI` 被动游荡+受击逃跑；**Enemy.hurt 兼容 shim**（critters 桶调用方按 Critter.hurt(game) 单参调用 → 对象重映射）。
  - **群系池**：`biomeAt()`（生成列首个实心 tile 的 key 判定：corrupt→corruption/crimson→crimson/mud→jungle/ice+snow→snow/sand 族→desert），poolFor 第五参；新增 corruption[6,7,32]/crimson[173,223,224]/jungle[51,158,258]/snow[147,152,184,185]/desert[61,73,335] 池。
  - **水域**：trySpawnEnemy 深水列（**向下扫 100 格**）→ water 池[63,64,65,58,67,102,221]；aiStyle 16/18 走**水下落点搜索（-8..100 窗口）**；原"海洋排除 return"改为 deepWaterCol 标记（水生可入海、legacy 怪仍拦）。坑：环带点常在水面/水池上方，列扫描与落点窗口都必须够深（40 不够）。
  - 实测：腐化出噬魂怪/吞噬怪、水池出水母/蟹/琵琶鱼、白天出兔/蚯蚓/蚱蜢。
- **行为修正批（2026-08-09 深夜2，用户报告五连问题）**：
  - **鱼/水母飞天**：swimAI 离水分支误写 `vy -= 0.3`（=持续向上）→ 改重力下坠+落地拍打；jellyfishAI 原本无水检测（空气里脉冲追人）→ 加水检测，离水受重力。
  - **友好生物有攻击性**：共享尾段接触伤害对 damage=0 也调 damagePlayer(0)（仍有击退/闪红感）→ `def.damage > 0` 才触发。
  - **鲨鱼生成在陆地小水洼**：水生落点要求下方连续 5 格液体（真水体）。
  - **白天史莱姆追杀主角**：slimeAI 索敌改为 受击(iframes)或玩家<6格 才追，否则随机游荡跳。
  - **贴图帧错乱**：根因非帧数表（两版帧数表仅差 4 条、PNG 高度÷frames 除 10 个困难模式 id 外全整除）——是**动画循环跑遍全部帧**（骷髅 15 帧只有 0-2 是行走，其余攻击/死亡姿势）→ 临时钳制 ≤4 帧后已在深夜3批次替换为原版 FindFrame 分族引擎（见上）。
- **★ 原版 FindFrame 分族帧引擎（2026-08-09 深夜3，替换 ≤4 帧临时钳制）**：Renderer.vanillaFrameIdx(e, frames) 按 Terarria1456 NPC.cs FindFrame 逐族规则——僵尸族(ZOMBIE_FRAME_TYPES 22 个 id, L77026)：腾空2/站定0/行走按 walkCycleT%32 的 8/16/24 阈值 → 0,1,2,1 往复；蝙蝠(ai14, L75585)：每 6tick 推进、BAT_SKIP_LAST(49/51/60/634) 不含末帧；史莱姆(ai1, L71506)：每 8tick 全循环；战士/107(L70155+)：站定0/腾空末帧/行走从帧2起按 |vx|*2+1 累加>6 推进循环回2；鲨鱼(ai16, L75386)：frame=(t/4)%4；水母(ai18, L74621)：脉冲期 [4..6] 循环、漂移 [0..3]。Enemy.walkCycleT 每 tick += |vx|（≈原版 frameCounter 驱动源 L77072/L70216）。其余族（眼/蜂群/幽灵）6tick 全循环。
- **★ VanillaSpawner 1:1 落地（2026-08-10，用户令"全量 1:1 不做临时方案"）**：`src/world/spawn/VanillaSpawner.ts` 移植 Spawner 内嵌类——SetSpawnFlagsForChosenTile(L950: waterTile/nearMarble/nearGranite/surfaceSpawn/underGround/isOcean/isBeach/Zone*) + FindSpawnTile(L879: 50 次随机取点±viewHalf+11..44、向下扫实心) + **SpawnAnNPC 链**（蜘蛛巢墙62→地下沙漠墙216/217/187→海洋→水池→小动物 Next(15) 门→蘑菇地70→丛林草60→沙漠沙→猩红→腐化→地表(白天 GetBasicSlimeToSpawn/夜晚 Next(6) 门+僵尸 switch Next(5)+-38..-42 小变种/-43 小眼)→underGround(N50 蠕虫/雪147/slime)→地狱(y>h-190: 骨蛇/火妖/恶魔)→洞穴(N60 蝾螈/蠕虫 N100/slime/骷髅 switch Next(4)/兜底蝙蝠)）。**负 netID 全量**：NET_ID_MAP 按 SetDefaultsFromNetId(L7633) 基底+scale+属性+color 覆盖（-1..-15 史莱姆系/-11/-12 噬魂怪/-38..-42 僵尸/-43 小眼/-46..-53 骷髅）。Game.trySpawnEnemy 薄壳化（spawner.spawn → 按 aiStyle 分放：蠕虫链/水生水下格/critter 桶/普通落脚位）。Enemy 新增 vanillaScale/tint/spawnAlpha（出生淡隐-8/tick，**替换永久 alpha**——修复半透明怪物）；渲染 multiply 着色 tint（绿史莱姆等）、scale=SetDefaults×netID、flying 判定统一用 noGravity。**验证分布**：白天=史莱姆、夜晚=史莱姆+水母+蠕虫、洞穴=蝙蝠+骷髅+水母（全部符合原版链）。world.flags.hardMode 已加（默认 false）。**注意**：world.timeOfDay 与 world.clock.timeOfDay 是两个字段，探针要设 clock.timeOfDay。
- **★ 城镇 NPC 贴图修正（2026-08-09，用户报"向导/护士/商人全是史莱姆贴图"）**：根因 `drawTownNPC` 曾把全部城镇 NPC 画成 Maples 图集 `角色/NPC_1.png`——Maples 沿用原版命名，NPC_1 **就是绿史莱姆**。修复：`TownNPC.vanillaId`（`TOWN_NPC_IDS` key→id+ExtraFramesCount，vanillaNpcs.ts；24 城镇 NPC，Zoologist=BestiaryGirl 633）+ `atlas.vnpc` 原版贴图条（40×56 帧）；帧语义按 FindFrame 城镇分支（NPC.cs:70172-70262）：腾空=1/站定=0/行走 2..frames-extra-1 循环（counter += |vx|*2+1、>6 推进、越界回卷帧2；extra 来自 NPCID.Sets.ExtraFramesCount NPCID.cs:4831）。`vanillaFrameIdx` 加 aiStyle 7 分支覆盖雕像 spawnNpc 走 Enemy.fromVanilla 的城镇 NPC。验证 `_townnpc.mjs`（3/3）+ `_townnpc-pix.mjs`（像素级：chromaDiff=0 精确吻合，史莱姆对照 33；注意光照合成压暗 RGB，绝对色差不可用，用色度 r-g/g-b）。npcFrameCount（Main.cs:65994）与 vanilla-npcs.json frames 已核对一致。
- **★ TownNPC 生命系统 + 小动物提取修复（2026-08-09 夜）**：TownNPC 新增 hp/maxHp（vanilla-npcs.json lifeMax/defense：250/15）/iframes/hurt()——陷阱弹幕可误伤城镇 NPC（见 [[vanilla-wiring-port]]），死亡即移除（原版次日重生未移植）。**extract-critters.mjs 大坑**：曾把 SetDefaults 源码 `.replace(/\n\s*/g,' ')` 压平成单行，parseBlock 的 `^` 行锚点导致每块只捕获第一个赋值→**64 条小动物缺 height/aiStyle/defense**（bunny 只有 width=18，height=undefined→fromVanilla NaN 碰撞盒）。修复=去压平重跑，99 条小动物数据全量补齐（bunny 18×20/aiStyle 7/defense 0）。
- **1:1③ 完成（2026-08-10 深夜）**：
  - **史莱姆 AI_001 原版核重写**：ai0 计数器跳跳节奏（站定 vx*=0.8；阶段判定 num54=-1000：ai0>=0→小跳 vy=-6/vx+=2*dir/ai0=-1120；-1000..-500→小跳 ai0=-2120；-2000..-1500→大跳 vy=-8/vx+=3*dir/ai0=-200——即小跳→小跳→大跳循环）；flag3 激愤=夜晚||受伤||地下（白天满血地表**不追**——用户要求的行为）；卡墙检测落地X==起跳X→反转+ai2=200 冷却不索敌；蚱蜢 377/446 复用（ai0 额外+3）。
  - **birdAI（aiStyle 24）**：三态 ai0=0 地面踱步/1 飞行/2 降落；飞行 X 轴同飘浮眼 0.1 步进 ±4；Y 轴前方 15 格下探（全空 vy+=0.05 缓沉、受阻 -0.1、近障 5 格内再 -0.2）；撞墙反转旧速×-0.5 最小 ±3/±1；玩家贴近/受击起飞（远离方向）。
  - **butterflyAI（64/65）**：正弦漂移 + 遇墙反弹。
  - **critter 分发**：鸟 24→birdAI、蝶萤 64/65→butterflyAI、蚱蜢 1→slimeAI、其余地面→critterWanderAI。
  - **探针启动路径统一修复**：用户并行 vui 菜单改版后 querySelector('button') 命中标题页"单人模式"而非垫片"创建新世界"——全部探针改为 `select.parentElement.querySelector('button').click()`。
  - **VanillaSpawner debugPoolOverride 钩子**：非空时绕过原版链直接池选（确定性验证探针兼容）。
  - 回归：NPC 5/5、蝙蝠 4/4、战士 4/4、蜂群 4/4、法师 3/3、蠕虫 5/5、掉落 2/2、smoke PASS。
- **1:1④ 完成（2026-08-10 凌晨）**：
  - **蠕虫段链→原版方向向量收缩**（L52271-52308）：shrink=(dist-linkDist)/dist、position += dxC*shrink 维持 linkDist=width 间距（替代贪吃蛇链）；spriteDirection 按 dxC 符号（L52305）。
  - **蜂群真实振荡**（L17742-17752）：ai0 逐 tick 递增、>200 翻回 -200（替代 aiT 取模）；>0 加 vy、|ai0|>100 加 vx；近距清零。
  - **Despawn 系统**（L7228-7241）：despawnTimer=7500（原版 timeLeft）；飘浮眼白天 DespawnEncouraged(10)→离屏 90 格清；夜行怪白天离屏清；其余离屏 120 格 timer 递减到 0 清、回屏重置——替代"白天烧除/90 格硬清"。
  - 回归全绿（蠕虫 5/5 蜂群 4/4 眼 4/4 NPC 5/5 蝙蝠 4/4 战士 4/4 法师 3/3 smoke PASS；charger 位移断言对振荡采样天然不稳，改以速度档+折返判定 4/4）。
- **待办**：①Boss 专属 AI（~~EoC 4~~已完成见下/史莱姆王 15/WoF 27/骷髅头 11/地牢守卫 68，全有 1.4.5.6 源）；②HitEffect 死亡粒子表；③Projectile.AI 弹幕；④critter 各家族原版行为逐族 1:1（现统一 critterWanderAI：蚱蜢跳 1/鸟飞 24/蝶 64/虫爬 66）；⑤SpawnNPC 权重；⑥25 种缺失属性。

- **★ EoC(克苏鲁之眼) AI_004 1:1 完成（2026-08-10）**：Enemy.eocAI 全量（NPC.cs:19909-20757 普通档）——P1 悬浮玩家上方 200px 伺服 5/0.04（600t）→ 3 连冲 6.0 速/150t（40t 后 0.98 摩擦）；悬浮在玩家上方且<500px 累计 110t 召仆从 5（vel=dir*5）；HP≤50% → 自旋变身（0.005→0.5 rad/tick ×100t 加速 + 减速 100t + gore/吼声）→ P2 悬浮 120px/6/0.07（200t）→ 3 连冲 6.8/130t（0.97）；白天/目标死亡 → vy-=0.04 漂离+despawn。旋转：悬浮追 atan2(dy,dx)+π/2（0.02/40t 后 0.05），冲刺锁 atan2(v)-π/2（Renderer ctx.rotate(visAngle)）。FindFrame case 4：0/1/2 三帧眨眼各 7t，ai[0]>1（P2）+3 偏移。召唤走 Enemy.fromVanilla(4)（可疑眼球）。
  - **三个时序陷阱（探针逐 tick 采样定位）**：①per-AI `++aiT` 叠加 fixedUpdate 头部全局 `aiT++` → 全部计时减半；②**分发层 `hasPlayer=!player.dead` 把死亡玩家传成 null → eocAI 的 dead 分支永远进不去**——原版语义是 TargetClosest 后照常拿 player 对象判 `player[target].dead`（cs:19931），死亡走逃离分支在状态机前 return；修为 case 4 传原始 player；③逃离分支要 `this.aiT--` 抵消头部自增 = 原版 ai[2] 冻结语义（死亡期冲刺/悬浮计时暂停，复活从冻结处继续）——否则死亡期 aiT 照走、复活即提前退出冲刺（曾致"首冲 279t"谜案）。**教训：凡原版 AI 有 dead-target 分支的，分发必须传 player 原对象而非 null；全局计时器与原版 ai[n] 字段语义差一个"分支内是否推进"**。
  - 验证探针 `game/probe-eoc-trace.mjs`（monkey-patch fixedUpdate 逐 tick 记 state/aiT/chargesLeft）：悬浮 600t、3 连冲各 150t、退出回悬浮全对齐；`probe-eoc-dead.mjs`（死亡期 aiT 冻结+vy -0.04/tick+复活续冲）。


- **★ Boss 全量移植（2026-08-10,B1-B5 五批;B4 9/10 组完成）**：**B1 数据/显形**（VANILLA_BOSS_IDS 头主体集+JSON 补 127/636/657/128-131+downed_<id> 记账通用化）✅；**B2 肉前三王**✅（EoC 另一会话负责、用户明令跳过）——骷髅王 AI_011+手 12、史莱姆王 AI_015、克脑 AI_054+爬行者 55,探针 `_bossprobe.mts` 11/11。**B3 机械三王**✅——双子 AI_030/031、Prime AI_032+部件 AI_033-036、毁灭者 AI_037(80 段链),`_mechprobe.mts` 27/27。**B4**✅(石巨人组在途):WoF 族 bossAI_wof.ts(ai27/28/29,空腔扫描/眼激光 83/饥饿者挂墙脱落,33/33)、蜂后+世花 bossAI_queenbee_plantera.ts(ai43/50/51/52/53——**勘误:261/265 是孢子,263 才是钩蔓,264 触须 53 主会话补**,25/25)、猪鲨+月总 bossAI_duke_moonlord.ts(ai69/70/77/78/79,**月总 396/397/398 血尽不直死:Enemy.hurt 放行由 AI 转 ai0=-2/2 残肢/演出**,30/30)、邪教徒+光女+史后 bossAI_lategame.ts(ai84/120/121+主会话补 ai100/101 远古之光/末日,25/25)。渲染 Renderer.ts ROTATION_NPC 旋转集(35/68/113-115/125-131/134-136/261-265/370/396/397/657);召唤 key:Game.ts summonBossAtTx 映射 wall_of_flesh 113/queen_bee 222/plantera 262/duke 370/moon_lord 398/lunatic_cultist 439/empress 636/queen_slime 657+mechanical_worm/eye/skull 物品(556/544/557,夜+hardMode);JSON 补 658/659/660(史后仆从:1 史后数据 24×18/14 40×30)。弹幕贴图 atlas 白名单补 42 张(83/96/100-102/183/275-277/407-408/410/441-442/464-468/490/522/526/527/545/612/719/754-756/836-840/872-874/919/922/923/926/950)。**坑**:Enemy.ai0 默认 -1120(史莱姆语义),凡原版 ai[] 从 0 起的 AI 必须 bInit 复位;伤害/防御状态修正必须 WeakMap 基值缓存防每 tick 重乘膨胀(骷髅王 1.3^400 事故);探针 fake game 必须有 entities{nextId,add} 包装器(bossAI.addEnemy 读 game.entities.add 不是顶层 add);探针落位要贴地板(底边在实心行下=坠穿);史莱姆王小史莱姆断言天然概率性(30%/落地);**E2E 被另一会话在途 Lang.ts 运行时错误挡住(暂 defer)**;E2E Chrome 路径改用 ~/.cache/puppeteer 测试版(/Applications 对 node stat ENOENT——macOS TCC);g.summonBoss 要 bind(g) 否则 this undefined;并行子代理任务可能被分类器故障静默吞掉(石巨人组首发丢失,二次重发)。

- **Zone 判定修正(2026-08-09,用户报"腐化之地不刷噬魂怪")**:VanillaSpawner 原 ZoneCorrupt 只看落脚格类型且漏黑檀石 25(腐化地表实测 238 格黑檀石 vs 草仅 310 格且分布散),玩家站腐化里选点几乎踩不中 → 噬魂怪永不触发。已改为原版 SceneMetrics 语义(cs:16/613-615/678):以玩家为中心 **169×123 窗口**计数,EvilTileCount(23/24/25/32/112/163/398/400/661 计1,向日葵27 −10/株)≥300 = ZoneCorrupt;BloodTileCount(199/201/203/200/234/352/399/401/662)同阈值 = ZoneCrimson。400/401/661/662 引擎无 def 计 0 不影响。countTiles 每次生成尝试扫 ~2 万格(~0.1ms,spawnTimer 节流下可接受)。E2E:站黑檀石地表驱 Spawner 300 次 → 噬魂怪 6 占 152 次 + Devourer 101 占 72 次,与原版权重一致。**"腐化偏小/草浮空"系误判已澄清(2026-08-09 追问核实)**:CorruptionPass 与原版 WorldGen.cs:6059-6460 逐项一致——组数 w*0.00045(4200 宽小世界=1 组)、组宽 cx±(100..299)、主裂隙 300-450 步/支裂隙 1/35·50-100 步、cooldown 20/30、转换带 surface+30..50 游走、草铺"每列第一个暴露格"(`worldSurfaceLow`=全图最高地表≈山巅起扫,山区列草比 worldSurface 高百余格**是原版同款**,worldSurface 只是平均线);补齐了雪砖 161→腐化冰 163 的转换(v_163 早已注册,注释占位过时)。仍缺:沙岩 397→400/401(v_400/v_401 无 def)。

- **攀爬者(Clinger 101)修复(2026-08-10,用户报"大号噬魂怪只有头部+地上挪动+腐化底下不刷噬魂怪")**:用户看到的"大号噬魂怪"实为攀爬者 101。三处修复:①腐化分支按 1.4.5.6 一比一重写(NPC.cs:4032-4074)——门禁从 ZoneCorrupt 改为**落脚面 tile**(23腐化草/25黑檀石/112黑沙/163腐化冰/661,或 22&&ZoneCorrupt),攀爬者 101 仅**困难模式+岩石层下 1/3**且带锚点格参数(SpawnNPC 第6/7参→ai0/ai1),困难模式另有 83 世界吞噬兽(1/40)/121/81/94 史莱姆族;**肉前任意深度落脚面为腐化系即刷 -11/-12/6 噬魂怪(修复"腐化底下不刷")**;②AI_013 plantAI 一比一(NPC.cs:22604-22700)——锚点格固定悬停+朝玩家伸展(range 175/食人花 250,300-450tick 周期×1.3)+逆向 accel×1.5+**锚点格被挖即死**+noTileCollide 幽灵位移;③spawnNPC 增加 ai0/ai1 参数传递。验证:地下腐化实测出 {6,-11} 噬魂怪;攀爬者离线单测(悬停不落地/朝上方玩家伸展 189px/锚点破坏即死)。攀爬者贴图"只有头部"是其原版设计(浮头+下垂内脏,62×42×5帧),全帧行分布正常——此前因 zombieAI 落地才显得只有头。

- **守卫老人(NPC 37)落地(2026-08-10,用户令"白天只对话/夜晚诅咒唤 BOSS")**:①TOWN_NPC_IDS 加 old_man {id:37,extra:2}(21 帧原版贴图条);②afterWorldLoad 生成 TownNPC('old_man'),home 锚定门口+leashHome 栓绳游走;③talkToNearbyNpc old_man 分支——白天/hardMode 只出 6 句原版闲聊气泡(走开/诅咒/可怜的骨头等),夜晚 Boss 在场时拒绝,否则**二次对话确认**(oldManCurseArm 600 tick 窗)→老人 dead 消失 + summonBossAtTx('skeletron_head', 老人所在列)召唤骷髅王 35(skeletronHeadAI 已有);④summonBoss 拆出 summonBossAtTx(key, tx) 位置化变体(诅咒在地牢上空召唤,非玩家侧 55 格)。E2E:白天气泡✓、夜晚二次确认→骷髅王 35 生成+老人消失✓。**注意**:talkToNearbyNpc 要求玩家 3.5 格内且光标命中老人±8px(探针需先传送玩家);骷髅王手 NPC 36(aiStyle 12)未移植,暂只召唤头。
  - **★ 门口落位三连坑(2026-08-10,用户报"门口看不到老人")**:探针定位三层根因——①旧扫描从 groundLevel-30(平均地表)起,地牢在山坡时入口(dungeonY)比平均地表高上百格→老人落到门口地底;②dungeonEnt 塔心(cy±1)是 3 宽竖井口(通楼梯),落塔心=坠井;③外廊门可能在与"背离地图中心"相反的一侧,单侧扫门找不到。修复=standSpot 候选链(门内/门外±3/6/10 格,验证=向下≤10 找地面+头顶 3 格净空+**3 宽地板**防井口/崖边)+双侧由外向内扫门+两级兜底(门高平面±70 列→塔外 20-70 列天空扫描站山坡)。验证探针 `game/probe-oldman.mjs` 8/8 种子:dist≤2、落地实心、头顶露天。**教训:出生点放置必须验证"脚下实心+头顶净空+左右有地板",塔/井类结构的锚点(dungeonX/Y)是塔心不是门口平地**。
- **★ Boss 全量移植收官(2026-08-10,B1-B5 全部完成)**:石巨人组 bossAI_golem.ts(agent 死前已落盘 30/30,只是没来得及汇报;主会话接线 case 45/46/47+hurt 豁免 245-248+旋转 246-249+召唤 key golem 245)——本体蓄力跳(挂头无敌 iframes=2/缺臂加速/血尽 60t 演出)、挂载头锚本体+嘴火弹 258+眼激光 259(半血二阶段)、拳肩锚归位→蓄力 30t→直线冲拳→过玩家主轴关穿墙、头血尽原体变身自由头 249(满血+249 属性)。**最终回归:9 探针 189 断言全绿**(golem30/boss11/mech27/wof33/qb25/dukeml30/lategame25/spider4/biomeflag4)+wiring31+lighting51+door0 失败。Enemy.hurt 血尽豁免表现合计:396/397/398 月总+245/246/247/248 石巨人(AI 首行转换)。Boss 分发全集:1/2/3/4(EoC 另会话)/5/6/8/10-18/20-22/24-29/30-37/43/45-47/50-55/69/70/77-79/84/100/101/107/120/121。召唤 key 全集:eater13/king50/brain266/skeletron35/queen_bee222/wall_of_flesh113/prime127/destroyer134/twins125/lunatic439/empress636/queen_slime657/plantera262/duke370/moon_lord398/golem245+物品 mechanical_worm/eye/skull。**遗留**:EoC 由另一会话负责;E2E(e2e-mechboss.mjs)被 Lang.ts 运行时错误挡住待跑;造型师354/机械师124/哥布林45 解绑 NPC 救援链路未做;专家模式分支全量注释保留;光女白天暴怒/邪教徒克隆体/世花离丛暴怒/史后离神圣暴怒未做。

相关：[[reference-vanilla-source-of-truth]]、[[vanilla-liquid-port]]

- **★ 天亮驱散夜怪 1:1（2026-08-10，用户报"僵尸等夜怪天亮不死"）**：原版语义是**游荡/上飞 + 离屏即逝**，不是原地蒸发。三处落地：
  - **CheckActive 移植**（NPC.cs:78669-78798）：timeLeft=**activeTime=750**（非 7500，旧记忆有误）；屏内矩形（rectangle2=sWidth/sHeight+2w ≈ 半轴 62×35 格）每 tick 重置 750+清 encouraged 旗；离屏从当前值倒数归零即 dead。执行顺序=AI 先 EncourageDespawn → 尾段 CheckActive（屏内重置会**撤销** encourage——采样 encouraged 旗在屏内恒 false 是正常的，cap 只在离屏后可见）。
  - **AI_003 战士白天驱散**（cs:57732/57773 + NotDiscouraged :60694）：白天 && y<worldSurface && 类型不在 FIGHTER_DAY_ACTIVE 豁免表（腐化/猩红战士/秃鹫/鸟妖等 59 个 id）→ 停止索敌 + EncourageDespawn(10) + 站定 2t 转向游荡（state 复用作转向计数）。僵尸 3 不在表 → 天亮驱散 ✓。
  - **AI_002 飘浮眼昼散表**（cs:52707/53152）：白天 && y≤worldSurface && id∈{2,133,190-194,317,318} → EncourageDespawn(10) + **保持水平方向**（direction=vx>0?1:-1，旧实现反了）+ directionY=-1 上飞。
  - **AI_005 噬魂怪无白天处理**（cs:50639 仅 type 619 特判）——噬魂怪白天照常追、只受通用 750t 离屏倒计时，这是原版行为非遗漏。
  - 旧 despawn 尾段（nightOnly 90 格硬清/120 格 7500t）整体废弃；nightOnly 仍用于生成门禁。验证探针 `game/probe-day-despawn.mjs`：夜追 ✓/白天屏内存活+游荡不追 ✓/离屏僵尸+眼 ~10t 消 ✓/噬魂怪 60t 仍活 ✓。

- **★ 生成条件审计批(2026-08-10,用户问"其它怪生成条件是否也有问题")——又抓 4 个**：
  ①**大理石/花岗岩邻近扫描缺失**(NPC.cs:960-1046):原版落点格/玩家格都不中时还有两轮大范围扫描(落点±Next(20,30) 步长 1-3 + 玩家±Next(30,60) 步长 3-6 抽样),只查两格则小矿洞永远探测不到→蛇发女妖 481/花岗岩傀儡 482 不出;②**地下沙漠旗标同蜘蛛巢病**(L1078-1100):1/3 扫落点±Next(5,15) 墙集{216,217,187}+2/3 查玩家格墙,此前只查落点一格;③**邻近旗标跨次泄漏**:nearMarble/nearGranite/spawnUndergroundDesert 从不复位,碰一次大理石后全图永远出 481(原版每尝试全新置旗)→spawn() 开头统一复位;④**T 表 8 个 key 拼错静默归零**(get() ?? 0):v_367_marble→v_367_marble_block、v_368_smooth_granite→v_368_granite_block、v_60_jungle_grass→…_block、v_70_mushroom_grass→…_block、v_116_pearlsand→…_block、v_161_snow_brick→snow_brick、v_163_corrupt_ice→v_163_purple_ice_block、v_200_frozen_crimson→v_200_red_ice_block;**T.MARBLE=0 还会误匹配空气格**(tile 0)——扫描若用错 key 会全图误报。164 粉冰引擎未注册保持 0(注释)。**探针教训**:生成点必须在屏幕外(玩家±41×26 格)——生物群系腔要伸进屏幕外带,否则 findSpawnTile 全拒;深度带互斥(沙漠旗标带 200..rockLevel,大理石洞穴池在 rockLayer 以下,地狱带 h-190)——单隧道测不了全部,`_spiderprobe.mts`(巢内 75% 主力/巢外/远离三场景)+`_biomeflagprobe.mts`(沙漠/大理石/花岗岩/对照 4 场景,600 高世界双隧道)。其余链段(蘑菇地/丛林/沙漠 tile/猩红/腐化/地牢/地表昼夜/underGround/地狱/洞穴池)与反编译逐段比对无同类缺失。

- **丛林刷怪测试修正+e2e（2026-08-10）**：tests/jungle-spawn.test.ts 浅层用例原白名单写死 {51,56,1,-3,-7} 失败——原版 else-if 链语义里浅层丛林 5/8 **落穿通用地表池**（僵尸/眼/史莱姆/鸟等 16 种 id 合法）；断言改为「51/56 必出、158/204/43/黄蜂族必不出现」。新增端到端用例（真实世界 jungleX 附近找深层丛林草落脚 → 3000 次 spawner.spawn 全链路）：tally 命中 204×283/43×226/黄蜂族×720/51×112。**注意 51=丛林蝙蝠非黄蜂；56 抓人草只在浅层带(y≤(surface+rock)/2)、43 食人怪只在深层**（原版 L3839-3856 分带）。world-store「删除后 id 不复用」全量跑偶发失败=测试间状态污染 flake,单跑恒过。

- **★ 城镇 NPC 入驻系统 1:1（2026-08-10，用户报"初始应只有向导，商人护士开局就在"+令移植原版入驻/房屋逻辑）**：
  - **初始态**：向导(NPC 22)随世界出生于出生点（WorldGen.cs:20036），homeless；商人/护士开局直刷已删。
  - **Housing.ts**（新）：房屋判定=门内侧泛洪填充（≤1200 格、≥60 格），纯空气格必须有**房墙**（Main.wallHouse 全表 267 id 提取——木墙=93；自然泥土/石墙不合格），门/平台算边界，需求=门+桌(含工作台,sheet 14/18)+椅(15/21)+光源(TileDef.light)。旧 isValidHouse 启发式已删。checkRoom(st,doorX,doorY) 单房判定 / findFreeHouse 全图扫空闲房（按到出生点距离取最近，房间 tile 集含任一已入住 home 即视为占用）。
  - **入驻轮**（Game.updateTownNpcArrival，tick%7200==600 首查后每 2 分钟=Main.cs:65021 UpdateTime_SpawnTownNPCs 语义）：①QuickFindHome——无家 NPC 见空房入住（leashHome=true）；②优先级链（num42 顺序子集：向导>商人>护士>军火商>树妖>爆破手；护士/爆破手要求商人在场）；③有房入住房内(Announcement.HasArrived)，无房但有入住者→白天且当前无流浪者时在其家附近流浪生成（SpawnHomelessNPC :4992，HomelessArrived_N），无任何入住者不生成。
  - **条件（NPC.cs:7046-7170 SpawnAllowed_*）**：商人=硬币≥5000 铜（coin_copper/silver/gold 权 1/100/10000）；护士=maxHp/20>5（生命水晶）；军火商=背包有 ammo/useAmmo==AmmoID.Bullet(14)；爆破手=炸弹系物品键集；树妖=downed_4(EoC)/downed_13(世吞)/downed_266(克脑)/downed_35(骷髅王)。Boss 击杀写 flags[`downed_${vanillaId}`]（Game.ts:927 通用记账）。
  - 验证 probe `game/probe-town-arrival.mjs` 4/4。注意：裁缝/哥布林/机械师/巫师等依赖未移植的"救援(savedNPC)"系统，暂不入驻。

- **★ NPC 对话文本全量对齐 GetChat（2026-08-10，用户报"向导说出地牢守卫(老人)文本"）**：根因=townNpcChat 只写了商人 17/护士 18，**其余类型全部落入守卫老人自建文案池**(Mods OldMan1-6 诅咒主题)——向导说"解除诅咒"。已按 NPC.cs:94974+ GetChat 分支 1:1 补齐：向导 22(cs:95473 夜 173/昼 174-176)、守卫老人 37(cs:95224 昼 82-84；夜 生命<300||防御<10 → 85-88 否则 89-92，**替换自建池**)、军火商 19(95195 互cue 58-63+常规 66-68)、树妖 20(95204 69/332+互cue 70-72+77-81/333)、爆破手 38(95246 93+互cue 97-100+夜 101-104+昼 105-109)。在场旗标 present(id)+downedBoss1/2/3(downed_4/13|266/35)。未实现事件段(血月/灯笼夜/日食/史莱姆雨/DD2)跳过走常规池。**命名占位符**(原版显示期 Format)：{PlayerName}=appearance.name 兜底'泰拉瑞亚'、{Guide} 等=在场实例随机名否则类型名、{WorldEvilStone}=Lang.itemName(**61** Ebonstone/**836** Crimstone——**物品 id 非 tile id**！曾误用 tile id 25/203 得到"黄陨石光剑")。formatDialogTags 在 openNpcDialog 出口统一替换。验证 probe `game/probe-npc-chat.mjs` 10/10 池内采样。

- **★ 城镇 NPC 全量补齐（2026-08-10，用户令"全量移植包括交互"）**：
  - **GetChat 全部 24 分支**（NPC.cs:94974+）：裁缝54/哥布林107(流浪121-125+Chatter池)/巫师108(按角色性别分档互cue 142-147)/机械师124/圣诞142/松露160/蒸汽朋克178/染料商207/派对女孩208/电子人209/油漆工227/巫医228/海盗229/造型师353(月相池,moonPhase≈(dayCount-1)%8)/税务员441/高尔夫球手588(GolferChatter+QuestsChatter)/动物学家633(满月变身 LycantropeChatter)/公主663(PrincessChatter)。**Chatter 池**=Lang.chatter()→languageManager.randomFromCategory（l10n 各 XxxChatter 类目）。{Bartender} 标签→Lang.npcName(550)。
  - **入驻条件全链**（Main.cs num42 完整顺序 24 项）：裁缝=downed_35；松露=hardMode；蒸汽朋克=任一机械王(125/126/127/134)；巫医=downed_222；电子人=hardMode+downed_262；海盗=xMas 外 downedPirates(未实现恒假)；圣诞=xMas(恒假)；动物学家=图鉴10%(恒假)；派对女孩=每轮1/40重掷+≥20人；染料商=背包染料(vid 1107-1120/3385-3388)+≥4人；油漆工=≥8人；公主=22 种全在场；**救援系**(savedGoblin/Wizard/Mech/Stylist/TaxCollector/Golfer 旗标)。
  - **救援系统**：TownNPC.bound（原地不动）+placeBoundRescueNpcs（载入放置：机械师=地牢墙内/造型师=蜘蛛巢墙62/高尔夫球手=地下沙漠墙216-217-187/哥布林=洞穴层/税务员=地狱层/巫师=hardMode 后入驻轮补放）；右键→freeBoundNpc（bound 解除+saved 旗标+Rescued 公告）。原版为独立类型 105/106/122/123（捆绑贴图），本作用 bound 近似。
  - **商店全量**：tools/extract-shops.mjs（Item.cs SetDefaults1-5 提 value——**buyPrice(plat,gold,silver,copper) 左锚,值=Σ arg·100^(3-i),reduce 后补 ×100^(4-N)**；Chest.SetupShop 顶层 case 提商品表——**嵌套 switch 的 case 靠 depth==2 过滤**；NPCInteractions.cs:489-513 的 NPC→shop 槽映射）→ src/data/vanilla-shopstock.json（21 店 426 条，含 if 门标记）。Game.SHOPSTOCK 数据驱动+shopCondOk 门映射（hardMode/downedBoss1-3/downedMechBossAny/night/day/zoneSnow/Jungle/Graveyard/Meteor/Underworld/crimson；moonPhase 近似恒真；xMas/bloodMoon/eclipse/party 不上架）；shopStockFor 替换 MERCHANT_BASE 硬编码；全部商店 NPC 出"商店"按钮。缺价条目兜底 100 铜（dryad 40 条/golfer 25 条用了 DefaultTo* 助手设价）。
  - 验证 probe `game/probe-npc-full.mjs`：初始=向导+老人+5 bound ✓/解救旗标+正式对话池 ✓/商人 13 基础款+夜晚荧光棒 ✓/6 NPC 对话池采样 ✓/裁缝条件 ✓（每轮一名：downed_35 先到树妖）。
  - **未移植交互**（依赖缺失子系统，NPCInteractions.cs:514-531）：重铸(TinkererReforge 需词缀系统)/理发窗口(StylistHairWindow)/收税(TaxCollectorCollectTaxes)/树妖净化粉(DryadPurification)/染料商稀有植物/向导提示/住房查询(RequestHome)/幸福感(ReportHappiness)/旅行商人368(移动商店)/骷髅商453/钓鱼娃369/酒馆老板550(酒馆事件)。bound NPC 渲染为站立姿态(原版有捆绑贴图)。

- **★ 整体 review + 税务员收税补齐（2026-08-10）**：Player.taxMoney/taxTimer（Player.cs:792-793）；Game.fixedUpdate 累积（Main.cs:64462：税务员在场时每 3600 tick +50 铜×已入住城镇 NPC 数，上限 250000=25 金）；对话「收集」按钮(inter 89)→taxCollect+gainCopper（spendCopper 镜像）。NpcButtonId 加 'collect'。验证 probe-tax.mjs：1 游戏小时=150 铜(3 入住)→收集+150 ✓。**review 确认**：城镇 NPC 死亡"重生"由入驻轮自然承担（UpdateTime_SpawnTownNPCs 同款语义），无需独立系统。**探针教训再确认**：页面内 `import('/src/entities/xxx.ts')` 与游戏模块是**不同实例**（vite ?t= 分叉），探针造的实体过不了游戏侧 instanceof——必须用游戏侧已有实体/游戏侧构造器。

- **★ 事件旗标 + 旅行商人 + 骷髅商（2026-08-10 "全量补齐"第二轮）**：
  - **Clock 事件字段**：moonPhase(每黎明+1 mod8, Main.cs:64877)/bloodMoon(黄昏 roll：moonPhase!=4 && 1/9 && maxHp>120, :64813-64831, 公告 LegacyMisc.8)/xMas(现实 12/15+)/halloween(10/10-11/1)。Game fixedUpdate 跨越检测（_lastClockT 快照，crossed(0.25)=黎明/crossed(0.75)=黄昏）+checkSeasonal()。
  - **血月接线**：对话段 guide 170-172/arms 64-65/dryad 73-76/demo 94-96/mechanic 161-164/stylist 304-306/clothier 111（插在原版链对应位置）；shopCondOk bloodMoon/xMas → clock；santa 条件改 clock.xMas；spawner 夜晚再 ×0.3/×1.8（L447-450）。造型师月相池/动物学家变身改用真 moonPhase。
  - **旅行商人 368**：TOWN_NPC_IDS(travelling_merchant, extra=10)。updateTravellingMerchant 每 tick：上午(昼进度<0.5) 1/108000、城镇 NPC≥2(除 37/453)→随机入住者家旁生成+HasArrived；白天过 0.65 或入夜+离屏→misc[35] 告别。**动态商店**：tools/extract-travelshop.mjs 提 GetItem/GetPainting 池（65+31 条 {id,tier,cond}）→ vanilla-travelshop.json；buildTravelStock=4-6 件(首件 minRarity=2 渐放宽)+1 画，按原版 if 链顺序后命中覆盖、RollLuck(N)=1/N（无运气系统）；shopStockFor 特例走 travelStock。对话 319-331。
  - **骷髅商 453**：TOWN_NPC_IDS(skeleton_merchant, extra=9)。VanillaSpawner 洞穴主池 1/2 桶→1/35（原误标 Creeper Egg）；Game.trySpawnEnemy 把 picked.vanillaId===453 转 TownNPC 进 npcs（CountNPCS==0 去重）；离屏 750t 消散（CheckActive 语义）；商店 case 20（33 件提取）；对话 356-363+Chatter。
  - 验证 probe `game/probe-events.mjs` 全绿。**探针双实例坑第二次踩实：改模块级导出(debugPoolOverride)必须走 window.__swSetPool（游戏侧 setter），动态 import 的 setDebugPool 是另一实例**。
  - 仍缺（子系统依赖）：词缀+重铸/理发窗口/净化粉/住房查询+幸福感 UI/GuideHelpText 条件文本(被 l10n 管线剔除)/海盗·哥布林入侵/钓鱼娃/酒馆老板/图鉴(动物学家)。

- **★ Boss 结束语义修正(2026-08-10,用户报"天亮离开却显示被打败+错误记账+守卫诅咒 Boss 杀主角显示打败")**:单点根因=另一会话的 despawn 系统(EncourageDespawn 语义,Enemy.ts:327-347)让 Boss 离场时 `dead=true`,直接流入 Game 记账块 → 全部按"击败"处理(播 HasBeenDefeated + downed 标志)。修复:①Enemy 加 `bossFled` 字段,despawn 倒数归零的 Boss 死亡打标;②bossAI 三处 flee 补 `encourageDespawn(10)`(双子天亮/玩家死、Prime ai1=3 离场;骷髅王离场另一会话已修)+毁灭者钻地链消散直接打 bossFled;③Game 记账分支:fled→灰字「逃走了…」不播击败不写 downed,kill→蓝字击败公告+downed;骷髅王两种结局都走 maybeRespawnOldMan(!downedSkeletron 条件天然区分)。**原版语义对照:双子/毁灭者天亮 EncourageDespawn 逃离不记账;Prime/骷髅王白天狂暴(ai1=2, 9999 伤防)不逃——AI_032 源码 :27782-27800 证实 Prime 是狂暴不是逃跑**。E2E 11/11(双子/毁灭者天亮=逃走+不记账+结算;骷髅王杀主角后未死→离场结算+不记账)。boss 回归 11+27+30 全绿。

- **★ 入侵系统移植（2026-08-10，哥布林/雪人/海盗 1:1；火星后移）**：调研报告两份（原版语义+仓库挂点）已并入本条与计划文件 splendid-gliding-lighthouse.md。
  - **Invasion.ts**（新）：INVASION_GROUP（组1=26-29/111/471/472，组2=143-145，组3=212-216/252/491/492/662）、KILL_WEIGHT（216=5/471=10）、canStartInvasion（:63863 maxHp≥200）、startInvasion（:63884：80+40n，海盗+40+20n；invasionX=左右边缘 50/50）、tickInvasion（:63775：胜利→type 清零返回 won 类型；前线 1 tile/帧向 spawnX；warn 3600 周期公告）、invasionWarningMisc（misc 0-7/24-27）、shouldSpawnInvasionEnemies（:352 地表+前线 ±3000px）。
  - **World 五元组持久化**：invasionType/Size/SizeStart/X/Delay → serialize.ts（SaveData+SaveMeta+写出）、SaveFile.ts（saveGame meta+load 回填）、SaveClient.ts、protocol.ts（可选字段）。**invasionWarn 不存档**（Game.invasionWarn 运行时）。
  - **刷怪管线**：VanillaSpawner.invaders+activeIds（setPlayerFlags 扩参）；getSpawnRate 头部覆盖 rate=20/max=11；spawnAnNPC 最前 invaders 互斥分支（哥布林 471→29→26→111→27→28；雪人 145→143→144；海盗 216→215→252→214→213→212，491 飞船暂缺）；Game.onEnemyKilled(key,enemy) 组号匹配扣分（types.ts 签名扩参）。
  - **触发**：黎明 crossed(0.25)——invasionDelay--、哥布林（shadowOrbSmashed+未击败1/3/已击败1/30|1/60）、海盗（hardMode+1/30|1/60，altarCount 门以 hardMode 替代）；物品 goblin_battle_standard(361)/snow_globe(602)/pirate_map(1301) 注册+使用分支（ignoreDelay）；入侵中 updateTownNpcArrival/updateTravellingMerchant 压制。startInvasionAndAnnounce 公共入口（maxHp<200 toast Need200Hp）。
  - **表现**：公告 Lang.misc 紫(175,75,255)；Renderer.render 第14参 invasion{name,pct}（nearInvasion=屏内±5000px 本组 NPC 门；drawInvasionBar 在 Boss 条下 30px 黄条，布局偏差已注明）；MusicInput.invasionMusic（pickMusic 链 bossMusic 之后；海盗35/哥布林39/雪人13）。
  - **敌人侧**：FIGHTER_DAY_ACTIVE 加入侵 14 id；fighterAI 尾部入侵远程段（RANGED_TABLE 111/214/215/216：ai0=瞄准冷却半程发射、ai3=姿态、LOS 步进扫描、预判点+散布±40、Dart 敌我对全敌对弹体）。
  - 验证 probe-invasion.mjs 9/9：启动/低血拒绝/边缘生成/海盗池生成无泄漏/扣分/胜利→downedPirates→海盗NPC解锁/哥布林黎明 roll/压制/物品/音乐/存档往返。回归 probe-events/probe-npc-full 不破。
  - **未做**：火星入侵 type=4（探测器399+飞碟395 后续单独一期）、491 海盗飞船多部件、祭坛计数门、灯笼夜奖励。
  - **review 补漏（同轮）**：①warn 冻结——原版 invasionWarn-- 只在推进分支内（cs:63819/63833），抵达 spawnX 后 warn 冻结不再周期重播（曾每帧递减致无限重播公告）；②ShouldSpawnInvasionEnemies 次级条件（cs:366-375）：前线达中线 ±5 格 && 玩家 ±3000px 有城镇 NPC → 2/3 概率判 invaders（城镇被袭）——shouldSpawnInvasionEnemies 加 townNpcXs 参数。核对无误项：200 生命门是 StartInvasion 自身强制（:63896 num>0）故物品/自然 roll 等价；invaders 分支在 else-if 链中先于全部群系分支（我方放 spawnAnNPC 最前正确）；skyMob 分支（哈比/飞龙）本就未移植属既存缺口非入侵引入。

- **★ 篝火胶片滚动修复（2026-08-11，用户标注 v_215_campfires 报"动画像滚动胶片"）**：根因=TileAnim 把 215 按默认 pitch 38 加偏移，而 Tiles_215.png 帧块是 **36px 无缝排布**（像素自相关+ASCII 行剖面实证：火焰16+隙2+木柴16，帧起点 0/36/72/...）→ 每帧 +2px 漂移=胶片滚动。**原版 GetTileDrawData 在大 switch 之后有 Campfires 专属覆盖（TileDrawing.cs:6124-6133）：`frameY<36 → addFrY=tileFrame×36；frameY≥36（熄灭/灰烬行）→ 恒 252`**——不在任何 case 里，极易漏读。修复：TileAnim.campfireYOffset(frameY)（36 节距+熄灭行静止）+ ChunkCache 215 专分支。**同轮核对其余表项全部正确**：17/377 默认 38（furnace case 只设 tileHeight=18）、106/220/247/228/231/243/300-308/354/355/499/592=54（5374/5388/5580/5586 各 case 显式）。验证 probe-campfire.mjs：8 帧偏移 0..252 步进 36 ✓ 熄灭行 252 ✓ 渲染覆盖率 0.44 ✓。**教训：GetTileDrawData 的 addFrY 语义 = 初始化默认 38 + switch 内 case 覆盖 + switch 后 Sets 族覆盖（Campfires）三层，移植 pitch 必须三层都查**。

- **蠕虫族段旋转修复（2026-08-11，用户报"地下蠕虫/骨龙每段错转 90°"）**：原版 AI_006_Worms（1456 全量 51357-52672，前 644 行无 rotation、**函数长 ~1300 行，dump 要 dump 全**）：段 `rotation = atan2(vy,vx) + π/2`（:51500）、头朝目标角 +1.57（:52591）——贴图正面朝上(NPC_10 18×30 竖构图)。我们 wormAI 段只位移不转角 → 段全部竖立 90° 错位。修复：wormAI 每段 `visAngle = atan2(指向链前段) + π/2`（段速度角等价——我们的段无 velocity，用指向 leader 的方向=行进切向）；头用速度角。渲染 drawEnemy 加 `aiStyle===6 → rotate(visAngle)` 且旋转态不叠 facing 镜像（与 ROTATION_NPC 同策略）。全族生效：Devourer 7/Giant Worm 10/EoW 13-15/Bone Serpent 39-41（=用户"骨龙"）；Destroyer 134-136 走既有 ROTATION_NPC。浏览器探针：每段 visAngle 实时更新≠初值 ✓。教训：**1456 重构后 AI 函数超长，grep 前 644 行无果≠无逻辑**（1405 的 L17547 也有同款 `+1.57f` 可交叉验证）。
- ★蚁狮/黄蜂排查(2026-08-12,用户报"沙漠无蚁狮/丛林无黄蜂,疑缺发射粒子生物"):**端到端全部正常**——刷怪层实测沙漠(蚁狮69×214/秃鹫61×1163/幼虫580/581)、深层丛林(黄蜂42×297+231-235族);AI(antlionAI 沙球/swarmerAI 毒刺 L51125-51213 已移植含 ai1≥130 爬坡/玩家待机清零门/朝向一致门/101余音帧);渲染(vnpc 懒加载, NPC_42/69 贴图在 public)。**用户没见到的真实原因**:①黄蜂只在深层丛林 y>(ws+rock)/2,地表丛林=蝙蝠/抓人草(原版同分带);②地表 spawnRate=600(原版值),30s 仅~5次尝试;③沙漠带窄,刷怪环(±36-69格)半数落在带外。**小偏差修**:沙漠分支漏 tile 404 化石(原版 L3859 全集 53/112/116/234/397/396/404)——补 T.FOSSIL。npcs 白名单仅19项(城镇/小动物)不影响战斗怪(vnpc 懒加载兜底)。

## 蜂后死后不消散+血条残留（2026-08-11）
用户报"被蜂后杀死→重生后蜂后不追不消失、血条一直在"。两根因：
1. **queenBeeAI ai0===5 离场分支只写了注释没调 `e.encourageDespawn(10)`**（原版 :30390 每tick调）——Boss 豁免 despawn 永不消散。"没追杀"本身是原版正确行为（玩家死→ai[0]=5 飞离；远距>3000→ai[0]=4 追赶态）。已补调用→离屏~10t 消散+bossFled→game.boss 清空。
2. **Boss 血条显示门**：原版 BigProgressBarSystem.TryFindingNPCToTrack 只跟踪"屏幕矩形 Inflate(5000,5000) 内的 boss"——我们的 renderer `if(boss)` 无条件画。已加距离门（|dx|<半屏/z+5000 && |dy|<…）。Renderer boss 参数类型扩了 cx/cy（Game 投影处同步）。
教训：**"共享系统兜底"注释≠已接线**——bossAI 移植时 EncourageDespawn 有三处真调用（bossAI.ts:63/314/556），蜂后这处只有注释；review AI 分支要 grep 实际调用。probe-bee-despawn.mjs 验证（登记 boss→玩家死→蜂后消散→boss 清→重生）。

## 蜜蜂/黄蜂动画翻转修复（2026-08-13，用户报"蜜蜂和黄蜂动画贴图有翻转错误"）
- **根因**：AI_005 旋转按族分流（cs:51045-51054），我们全族统一"朝速度方向转头"——
  黄蜂 42/231-235、孢子蝠 176、205 原版**只倾斜 rotation=vx×0.1**（+spriteDirection=vx 符号），
  蜜蜂 210/211 倾斜 vx×0.2（FindFrame L75553 覆盖）；仅噬魂怪族 6/94/173/619 走 atan2(朝目标)-1.57、
  其余默认 atan2(速度)-1.57。全向转头+facing 镜像叠加 → 飞行中整只倒转=翻转观感。
- **修复**：drawEnemy aiStyle5 分支按 id 分流（黄蜂系/蜜蜂系只倾斜）；帧引擎补黄蜂族
  拍翼循环 0→1→2→1 每 2 tick（cs:75607-75633,8t 循环）；蜜蜂 t/6%4 全循环原已对。
- 教训：**aiStyle 同族的旋转/翻转规则未必统一**——逐 case 查原版分支，勿族级一刀切。

## 全 Boss 玩家死亡处置对齐（2026-08-11，真值表来自子代理全面提取 NPC.cs）
四类处置模式：(a) EncourageDespawn+上飞/下落 (b) 瞬时 active=false (c) 状态机逃跑 (d) 特殊计时。
**通用大坑：despawn 系统屏内判定此前用原始 player（尸体位置也算屏内）→ 死亡玩家期间一切鼓励消散失效**。已修（dead 玩家视为离屏，同原版 CheckActive 只认 active 玩家）。
逐 Boss 修复（均为 NPC.cs 实证行号）：
- EoC4 :20020 flee 补 encourage(10)（原只有 120 格兜底剔除）
- 双子125/126 :26585 player=null 也进上飞离场（原仅漂移不消散）
- KS50 :43466-43575 死亡/远距3000 → encourage(10)+背对+ai1=5 缩身60t→传送到世界右下角→ai1=6 淡入回归（anti-cheese 传送）
- EoW13-15 :51532 wormAI 无 dead 处理 → 补 encourage(300) 缓消（EoW flag=false 不加速下钻）
- BoC266 :32810-32822 死亡→ai3 计数120、>60 后 vy+=(n-60)*0.25 钻地下坠（**Y+= 是向下**，代理表曾写反）；曼哈顿>6000 瞬消（:32560）
- Prime臂 :28067 头 ai1!=0 且玩家死 → 下坠（vy+=0.1 上限16）替代悬停
- 石巨人245 :19469 死亡仅 noTileCollide（**不瞬消不切状态**——原实现死亡也瞬消）；活人>3000 曼哈顿才瞬消
- 猪鲨370 :49234 补 encourage(10)；皇后657 :45574 补 encourage(10)+背对（又一处"注释有调用无"）
已对齐无需改：骷髅王35/守卫68（ai1=3 下落+50）、WoF113（3 秒 localAI 自毁）、世花262（反向逃跑4800px 续命）、鹿角怪未实装、Cultist/Empress/MoonLord 自带瞬消/渐隐、Golem 部件 golemBoss<0 自毁。
验证 probe-boss-dead.mjs 12/12（EoC/KS/EoW/BoC/双子/Prime/毁灭者/世花/猪鲨/邪教徒/光皇/皇后）。

## 天气生怪事件对齐（2026-08-11，用户问"飞鱼/金鱼上岸"）
原版天气生成规则（NPC.cs SpawnAnNPC 内嵌链）：
- **已有**：雨天白天地表 1/4 飞鱼 224（aiStyle 44 ✓）/1/2 雨伞史莱姆 225；雨夜 1/2 雨衣僵尸 223（1/3 出 -54/-55 缩放变体——NetIdMap（NPCID.cs:10445）-54/-55→type 223，**不是**腐化金鱼）；雨天水黾/萤火虫不出。
- **补齐**：雨天小动物块（L2288-2311 friendly 段）= 金鱼上岸 230 主导 + 2/3 蚯蚓 357 + 1/400 金蚯蚓 448/金金鱼 593；雨天香蒲蜻蜓（L2107+FindCattailTop :80977 ±30×±20 reservoir 找 tile519 顶段 → 601 金蜻蜓 1/400 / 池 596-600 按 tile）。**实装在 Game.spawnCritter（我们的 friendly 通道）——不能放 VanillaSpawner 敌怪链**（原版 friendly/enemy 两套点位搜索，放敌怪链会抢占敌怪配额）。
- **缺口**：风日生物 594 WindyBalloon（AI_113 双部件气球+史莱姆）/628 Dandelion（AI_119）——json 有数据、AI 未移植；gem 松鼠/兔（世界宝石档位表）略。
- 验证 probe-rain-spawn.mjs：224/225/230×1180/357 2:1/448。367/367 全绿。

## 风日生物补齐（2026-08-11 续）
- **AI_113 风气球 594**（cs:43036-43175）：首帧挂史莱姆（1/180 金-4/1/10 母-7/1/3 绿-3 手动变体覆盖，ai0=-999 冻结——slimeAI 首行放行 :61441）；横速朝向加速至 2+|wind|×2；前方 8 格探测升降；玩家 400px 跟随 Y；爆=湿/自格实心（hurt 死亡分支解冻 slave ai0=0+上移10，对照 HitEffect :82590——**解冻必须在 hurt 而非 AI 内**，AI 死后不跑）；自然 despawn 消散时 slave 一并 dead（防 -999 悬空）。
- **AI_119 蒲公英 628**（cs:43254-43318）：非风日 encourageDespawn(10)；玩家下风 600px 且 |dy|<100 → 喷籽态计数 40 发 1-3 枚种子（proj 836 伤7→Dart 近似），80 回待机。本体无位移。
- **生成接入**（spawner 白天地表链，L4426/4431）：594 2/3 → 628 草地 9/10；门=!waterTile && 落点上格无墙（L1188 num=wall）&& IsItAHappyWindyDay(=shouldUseWindyDayMusic) && 下风侧（L1101 (pX-spawnTileX)*wind>0）。
- 验证：probe-wind-spawn.mjs（挂载/解冻/喷籽）+ 下风侧采样 594×7:628×2。374/374。

## 宝石系统全量接入（2026-08-11 晚，真值表来自子代理提取）
原版结构：宝石矿 tile 63-68（Gems pass 密度 0.5/0.45/0.3/0.25/0.1/0.05×w×0.2——**我们已有**）；琥珀无矿脉（提炼机+沙漠暴露晶簇 style6）。
新实装（src/world/gen/vanilla/GemPasses.ts，注册管线'宝石系统'位=地表装饰后）：
1. **GemCaves**（:17528）：countTiles 是**洪泛连通空气计数**（非窗口！曾实现错）50-300、无岩浆/冰、有岩石；Spread.Gem 形态近似=随机游走 200 步×5 格，实心 Gemmable 19:1 石:宝（**gemTileId 必须用内部 id 非 sheet 号**——sheet 63-68 vs 内部 ~7xx 曾错），空气格墙=48+序、1/2 暴露晶簇。
2. **ExposedGems**（冰 :20842 雪/冰上 1-3×1-3 权重紫3黄3蓝2翠2红1钻1 / 地下 :20874 单格 / 琥珀 :20891 墙 187/216 → 3×3 style6，原版不查实心直接 PlaceTile）。
3. **宝石树 pass**（:22196）：全列 j∈[ws,h-20) 上无液体 1/5 → 7 选 1 → growGemTree（TreePass 已有全套墙/基座/净空门）。
4. **暴露晶簇掉落**（KillTile :65545）：frameX/18 style → 181/180/177/179/178/182/999（清格前捕帧）。
5. **宝石树砍伐**（fellImportedTree sheet 583-589 特化）：每格 1/10 宝石×1 / 9/10 石×1-2；干基帧（fx≥22&&fy≥198）50% gemcorn 4851-4857（:65754+66149）。
6. **宝石小动物**：GetGemSquirrel/Bunny 加权表（:5587，Diamond5%/Amber8%/Ruby10%/Emerald12%/Sapphire16%/Topaz21%/Amethyst28%，**与就近宝石无关**）；洞穴层昼夜 1/3×1/5 松鼠+2/3×1/5 兔子（:2466 尾段）；雨天块补 gem 分支。挂 spawnCritter friendly 通道。
7. **gemcorn 4851-4857**（tile 590 fw3=带宽54px frameX/54 序号；placeStyle 0-6）；growSaplings 支持 590（必须 underground，growGemTree 全套判定）。
8. **提炼机**（tile 219 interactAt）：mode0 沙泥 424/淤泥 1103、mode1 沙漠化石 3347；链=1/10 坚固化石(mode1)→1/2 钱币大表（白1/12000/金1/800/银1/60/铜10-100）→蚊 1242（5000/1667）→宝石 1/25（mode1 50）→琥珀 1/50（mode1 20）→1/2 钱币小表→兜底 8 矿石（:511 12/11/14/13/699-702）。Toast.NeedExtractMaterial 入 zh-Hans/en-US。
验证：tests/gem-passes.test.ts **4/4**（含神庙免疫断言）。

## 宝石洞 review 纠偏（2026-08-11 深夜，用户报"神庙里看到宝石"）
**根因：GemCaves 漫洞实现是随机游走且空气分支无墙门** → 游走可溜进神庙把内部空气刷成宝石墙+晶簇。原版 Spread.Gem（:3565-3651）是 BFS 且**有墙格（wall≠0）一律不扩散、空气分支只在无墙格处理**——神庙（墙 87）/房屋天然免疫。全部重写对齐：
1. **GemCaves**：随机游走 → 原版 BFS（实心 Gemmable 自身+四邻转 randGemTile 19:1；无墙空气刷墙+1:2 晶簇+四邻入队；有墙格不扩散）。
2. **冰系晶簇**：目标格**自身**为冰块 147/161/162/224（此前错写"下方格为冰"）；逐行雪界 snowMinX/MaxX[y]（此前用常量左右界）；不对称窗口四向各 1-3（此前对称 1-3×1-3）；InWorld(,40)。
3. **地下晶簇**：x∈[20,w-20]（此前 4）；anyLava 精确（liquid>0&&type==2）。
4. **琥珀晶簇**：不对称窗口（各向 Next(1,4)，左闭右开）——此前对称 3×3。
5. 原版天然洞穴 wall=0（我们引擎 CavesPass 一致，天然 unsafe 墙是渲染期绘制非数据）——BFS 的"无墙空气"门即天然洞穴腔。
**注意：修复前生成的旧世界仍带神庙宝石，需重生成世界**。

## StepUp/StepDown 全体共享移植（2026-08-12，用户报"敌人卡半砖上不去"+彻查令）
**根因**：原版 `Collision.StepUp`（:3641-3770）是玩家（Player.cs:23258/:27753）与**全部 NPC**（NPC.cs:54382，AI 意图速度先于 TileCollision 调用）共用的自动上台阶——半砖 8px/整砖 16px/净空门齐全；我们只有 Player 自研版，敌人/小动物/城镇NPC 全卡死。
**实施**（src/physics/TileCollision.ts）：
- `applyStepUp` 1:1（gravDir=1/holdsMatching=false）：意图速度探柱 num2=⌊(x+vx+w/2+(w/2+1)dir)/16⌋、脚行 num3=⌊(y+h-1)/16⌋；净空门 flag(上方 j=2..num4)/flag2(后上对角)/flag3(脚上一格或面朝坡或半砖)/flag4(落脚实心或上半砖)+X重叠门；抬升目标=行顶（上半砖-8/本格半砖+8），上限 16.1px。
- `applyStepDown`（:3577-3638）1:1：贴地行走脚下 7~17px 内有落面（含半砖顶+8/平台）→ 吸附下去，消除下楼梯腾空帧（onGround 连续）。
- moveAndCollide 头部：`b.stepUp` 时 vy≥0 先 StepDown 再 StepUp——掉落物/弹幕/墓碑不置旗（原版它们不调）。Player/Enemy/Critter/TownNPC 四类置 stepUp=true；Player 自研上台阶删除（抬升检测改 gfxOffY 等价的 stepRenderY 补偿）。
**同类彻查结论**：SlopeCollision/坡面速度辅助（走 moveAndCollide 已全体共享✓）、传送带（Conveyor.ts conveyorCarriesEnemy 已有敌人门✓）、尖刺 HurtTiles（原版本就只伤玩家 Player.cs:28486，对齐✓）、平台（NPC 不下落穿透同原版✓）。Boss noTileCollide 族原版也跳过 StepUp✓。
验证：probe-stepup.mjs（僵尸上半砖+整砖台阶 PROBE OK）+ 34 定向测试全绿。注意：世界生成 worker 被并行会话在途改动间歇弄挂（runLivingTreesPass 等），探针需等其落盘。

## 受伤实体血条（2026-08-12，用户报"掉血不显示生命值"）
**根因**：Enemy.hpBarT 计时一直在维护但 Renderer 从未画过——血条渲染整个缺失。
**原版语义**（DrawInterface_14_EntityHealthBars Main.cs:45203 + DrawHealthBar :21748）：
- **无时间衰减**：`life != lifeMax && !dontTakeDamage` 即显示（我们旧的 hpBarT=240t 方案与原版不符，hpBarT 保留但不再作门）。
- 位置：脚底 +10 + NPCAddHeight（:21852-21977 全表已入 Renderer.HB_ADD_H）；Boss/大型怪 scale 1.5（:45228-45298 表）。
- 36px 宽、填充=36×hp%；**绿→黄→红渐变**（:21766-21778：n=hp%-0.1，n>0.5 绿满红减/否则红满绿增）；alpha=中心格光照亮度×0.95（8 档量化控 tintedSprite 缓存）。
- 贴图 HealthBar1/2.png（36×12，从 terraria-assets 补拷）；fill<34 四段绘制（背景帽+余量+填充主体+末帽 :21814-21828）。
- 蠕虫段不画（头部血条代表全链，DrawInterface_Healthbar_Worm :45527 头尾中点语义→近似画头下）；毁灭者 134 原版全链共享一条（destroyerHB 平滑），近似同上。
- Critter 无 hp 字段（一击死）暂不画；TownNPC 有 hp/maxHp ✓ 画。
验证：探针 hurt 僵尸 15 → drawHealthBar 执行 OK + 截图目检渐变条；回归 25/25。

## 召唤物色块+多帧胶片修复（2026-08-12，用户报"爆炸烈焰魔杖召唤 #FFD060 色块"）
**根因双层**：①public/sprites/vanilla 只有 374 张 Projectile 贴图——42 件召唤武器 40 件的投射物全无贴图 → MinionProj.draw 兜底色块（随从金 #FFD060/哨兵紫 #B080FF）。②原版投射物贴图是**竖向多帧行**，draw 整图压 32px → 多帧压成胶片条。
**修复**：
1. terraria-assets 全量补拷 Projectile_*.png（374→1109，全投射物兜底色块一并消灭；**无需图集**——projSprite 按需懒加载+缓存，同 id 全程一张，同时在场类型 <20，与 item atlas 的成片渲染场景不同）。
2. Main.projFrames 全 275 条非 1 帧赋值提取 → src/data/vanilla-projframes.json（663=7 帧/266=12 帧/191=18 帧…未列入恒 1）。
3. Arrow.ts 新增 projFrameCount/projFrameImg（帧高=图高/帧数切片+canvas 缓存 2048 上限）；MinionProj.draw 改单帧 1:1 绘制 + age/8 tick 动画循环，MinionProj 加 age 字段。
验证：探针 p663 帧裁 74×66、p266 第 3 帧 50×26、五贴图全可载 + 截图目检哨兵塔/史莱姆随从形象正常；回归 25/25。
遗留：召唤物 AI 仍是飞行/地面/哨兵三态近似（原版各 aiStyle 定制行为）；哨兵 Arrow 弹近似（爆炸烈焰塔原版发射火球 proj）；鞭子系统未实装。

## 召唤物攻击帧状态机（2026-08-12，用户报"攻击时应该有攻击帧"）
**原版语义**（AI_130_FlameBurstTower，Projectile.cs:65194-65450）：
- 帧布局：**帧 0 = 待机**；帧 1-6 = 开火动画（num5=1 起，每 num7=4t 一帧，共 num6×num7=24t）；
  **第 12t（num3）从炮口 Bottom+(dir*6,-46) 发火球 668**；结束回待机并冷却 num8=60t（T1）。
- 锁定目标（900px 内）转向 direction=Sign(指向)；AI 尾部 tileCollide=true + velocity.Y+=0.2 落地。
**实施**（MinionProj）：sFire/sFireT/sCool 状态机 + facing 翻转（draw ctx.scale(-1,1)）+ 哨兵重力落地；火球=Arrow(projId 668, grav 0.2)。仅 663/665/667（爆炸烈焰三档）——弩车/闪电光环/爆炸机关塔帧语义未逐个核对，保持 60t 一发近似+age 匀速循环（记录缺口）。随从（非哨兵）仍 age/8 匀速循环（各 aiStyle 定制动画未移植）。
验证 sentry-probe.mjs：待机帧0→开火进入→facing=-1→第12t火球668→帧4/6推进→24t回待机+冷却60t→落地 ✓。

## 召唤师三缺口全部落地（2026-08-12，"继续全部落地"）
**① OOA 六塔 AI 1:1**（MinionProj，对照 Projectile.cs）：
- 弩车 677-679（AI_134 :65584）：帧 0 待机/1-5 每 5t；第 12t 弩箭 680（速16）；25t 结束；冷却 160（GetBallistraShotDelay）
- 闪电光环 688-690（AI_137）：非射击——每 3t 塔周 4 格盒场伤（localNPCHitCooldown=3；原版 999 宽扫描增长近似）
- 爆炸机关 691-693（AI_138 :66059）：帧 4 张每 12t 连续循环；每 3t 探测中心上方 48px 的 144×144 盒→AoE+粒子+冷却 90
**② 鞭子系统**（全 18 把 DefaultToWhip 提取→src/data/vanilla-whips.json；combatWeapon kind:'whip'）：
- WhipProj（ProjectileAI_Whip :45600 主干简化）：根部钉玩家、飞出/收回包络、长度=shootSpeed×useAnimation×2、弧线下垂、分段命中
- tag：ItemID.UniqueTagEffects TagDamage 表（皮鞭+4~火鞭+15）；Enemy.whipTagT=240t/whipTagDmg；随从命中吃 +tag 加伤；随从锁定目标优先 tag 敌（ApplyTag 语义）
- 探针 whip-probe：武器语义 14 伤/甩出完成/敌人受伤/tag 4/随从加伤 ✓
**③ AI_062 族随从帧语义**（:62868-62971）：373 黄蜂 2t/帧 0-2；375 小鬼 5t/帧 0-3 **+攻击中帧偏移 4**（attackFlash=24t，命中点亮——真攻击帧）；407 蜘蛛 2t/帧 0-5；423/613 3t/帧 0-3
遗留：其余随从家族（星尘龙/沙漠虎等 ~15 族）定制帧与 AI 仍为三态近似；鞭的玩家 buff（荆棘鞭 summoner 怒等 PlayerBuffId）未接。

## 召唤师剩余两缺口落地（2026-08-12 第二轮，"继续全部落地"）
**① 其余随从家族帧表**（Projectile.cs 各 AI 内 frameCounter 规则提取 → MinionProj.MINION_FRAMES）：
266 史莱姆 5t/8 帧、317 乌鸦 5t/4、387 魔眼 4t/3、533 致命球 2t/3、755 血红 6t/5、
759 雀 6t/4、831 沙漠虎 4t/6、970 阿比盖尔 4t/6、1025 藤壶 8t/4（+此前的 373/375/407/423/613）。
未列入（758 吸血蛙 24 帧/951 雪怪 12 帧/1022 蘑菇 16 帧/1093 猫 28 帧/191 矮人 18 帧/393 海盗 15 帧/864 刃 2 帧/946 棱镜 1 帧）帧语义复杂或单帧，走 age/8 兜底（已注释声明）。
**② 鞭玩家 buff**（WhipTagEffect.PlayerBuffId 全表核对 ItemID.cs:1303-1414）：
- WHIP_TAG 修正为原版真值：5473:3/4911:6(非 8)/5478:12(非 10)/5479:15/4914:20/5480:25；4912 火鞭无 flat tag（专属爆炸 proc 未实装）；6143 妖精鞭 +4
- WHIP_PLAYER_BUFF：4913 荆棘鞭→314、4911→312、4678→308、4680→311、5473→365；命中授予 180t
- Player.whipBuffs 倒计时；**314 效果实装**：随从/哨兵 dmgOf ×1.1（MinionProj 两处）；其余 buff 登记持续期（效果端未接）
- 探针：荆棘鞭命中 → whipBuffs[314]=180(衰减至 130≈180-50t ✓)、tag 6/190t ✓
**遗留（记录）**：随从 AI 行为本体（黄蜂悬停/蜘蛛爬墙/星尘龙穿墙等 ~15 族 bespoke AI）仍三态近似；火鞭爆炸 proc/星璇星坠落/万花筒 possession 等专属 tag 特效未实装；308/311/312/365 buff 的效果端未接（仅登记）。

## NPC 网格贴图系统性排查(2026-08-12,594 事件驱动)
**方法论**:vnpc 纵切假设的地雷 = 原版用 2D 网格取帧的 NPC。权威信号两个:①FindFrame 写 frame.X/frame.Width(纯竖条只写 frame.Y);②Main.cs DrawNPC 的 `Frame(列,行)` 专属调用。宽度比扫描(脚本 scripts/_npcgridscan.mjs)噪点大,只作辅助。
**全量命中清单与处置**:
- 594 风气球 Frame(8,1) ✅ 已修(drawWindyBalloon)
- **657 史莱姆皇后 Frame(2,16)** Main:23134/FindFrame:67503——vy/ai0/ai1 状态机,索引=frame.Y/122
- **576/577 气球机器/食人魔 Frame(5,10)** Main:23301/FindFrame:68241——frame.Y 存索引(走路 11-20/攻击 37-47 各帧持时)
- **696 Frame(6,27,fy/9,fy%9)** Main:23349
- **564/565 等离子灯/雾机 Frame(5,9)** Main:23413(600×972=120×108 格)
- **668 鹿角怪 Frame(5,5,…,2,2) 2px padding** Main:26211 DrawNPCDirect_Deerclops(1090×1200),ai0 序列表 GetAttack1/2Frame
- 396-398 月总 Frame(3,3) ✅ 已有专属三分支
- 551 贝琪 ✅ 纵条正确(302 宽=龙本体);缺 Extra_82 喷火覆盖层(备案)
- :26839 Frame(20,1) = 派对帽子纹理,非 NPC 表,排除
**7 个网格 NPC 的移植由实现代理执行中**(drawNpcGrid 统一助手+各 FindFrame 状态机+tests/npc-grid-draw.test.ts)。

## 网格 NPC 移植完成(2026-08-12,实现代理交付)
**7 个网格 NPC 全部落地**(Renderer.ts:1424-1436 五分支 + drawNpcGrid:1832 切格助手 + WeakMap 帧态;帧状态机纯函数 :199-378 导出供测):
- 657 皇后 Frame(2,16):vy/half/ai0/ai1 全状态机,Inflate(0,-2)+Bottom(0,2)+贴图朝右
- 576/577 食人魔 Frame(5,10):走 11-20/攻 37-47(38起手与46腾空冻结!)/施法 21-38/漂浮 |vx|
- 696 Frame(6,27,**每 9 折行**)+同列 row+18 半透明投影层
- 564/565 暗黑魔法师 Frame(5,9):阈值链还原为定长序列(98/128/184t 对齐施法时长),Glow_225 叠画并入 alpha 分支
- 668 鹿角怪 Frame(5,5)pad2:三攻击序列表(:6516-6534),入段范围用原版显式常量(12..17/12..18/19..24,非表尾——代理测试抓到的真 bug)
镜像统一:canvas scale(-1,1)+originX ≡ XNA FlipHorizontally+origin(翻转绕 origin 点)。
**测试**:tests/npc-grid-draw.test.ts 22 项序列断言全绿+cactus 5=27/27;全量 802/805(3 失败皆并发区:caves×2+sky-invariant rain_cloud 深空)。
**未实装**(注释标注):657 shader 残影/Extra_186 水晶/Extra_177 王冠/二段翅膀、出生特效、696 表情泡、668 红雾/紫电重影。
**dist 阻塞**:并发会话在途编辑(WorldGen.ts vanilla.json import 路径已代修 ../../../;MushroomPass.ts 误引 writeFileSync 进浏览器包未修——等其落地)。

### 网格 NPC 移植 review(2026-08-12,源码逐项核对)
**核对结论:整体可靠**。逐项验证:网格数学(XNA Frame cols/rows 整除/668 的 pad2)、657 Inflate(0,-2)(:23142 实证)、696 perRow=9 折行、668 锚点方向(spriteDirection==1→106,:26219-26226 实证)、镜像等价性(canvas scale(-1,1)+originX ≡ XNA Flip 绕 origin)、食人魔默认段(:68340-68366 逐行一致)。
**Review 修两处**:
① 657 flying 判定——渲染原用 `ai0===0`,AI 侧权威是 `ai0===5||(ai0===4&&ai2===0)||(phase2&&ai0===0)`(bossAI_lategame:949);半血 ai0∈{4,5} 飞行时帧段会走错,已同式对齐(渲染/AI flying 必须一致,注释已标)。
② 696 投影层——原版画两遍(:23360-23367:第一遍精确+第二遍 ±1 抖动),我们只画一遍抖动,已补齐。
**保留的已注明近似**:564/565 阈值链→定长序列循环(循环长与施法时长对齐)、657/668 出生特效用 spawnAlpha 替代、shader 残影/Extra 叠层未实装(素材白名单缺)。
回归:27/27 定向 + 全量 814/817(3 失败皆并发会话 worldgen: caves marble/jungle + sky 深空雨云)。
