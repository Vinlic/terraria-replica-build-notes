---
name: vanilla-random-text-death-tombstone
description: 随机文本体系（世界名/NPC名/死亡文本/墓志铭）+ 死亡文本 + 墓碑 DropTombstone/aiStyle17 移植完成
metadata: 
  node_type: memory
  type: project
  originSessionId: 04569a63-44aa-4669-98a3-b777d15e98f8
  modified: 2026-08-10T05:48:18.575Z
---

2026-08-10 三件套移植完成（标杆 Terarria1456，见 [[reference-vanilla-source-of-truth]]）：

1. **随机文本** `src/i18n/RandomText.ts`，数据全部走 l10n zh-Hans.json 分节（零硬编码）：
   - 世界名 = UIWorldCreation.AssignRandomWorldName 1:1（RandomWorldName_Composition 模板
     {Adjective}/{Noun}/{Location} + 1/10000 永恒领域 + >27 字重掷）。旧的 SeedEasterEggs
     小样本 randomWorldName 已删；tests/world-store.test.ts 的 import 已改指向新模块。
   - NPC 名 = getNewNPCNameInner 类型→名字池表（Merchant/Nurse/Guide…，37 守卫老人无池→空串，正确）。
   - 玩家随机名 = 人类 NPC 池并集（★原版无玩家名字池，记录为偏差）。
   - 死亡文本 = Lang.CreateDeathMessage 1:1（DeathTextGeneric + DeathSource.NPC + DeathText.*）。
   - Epitaph 墓志铭数据就绪但未接线（原版只用于 worldgen 墓地 pass，我们没生成墓地）。
   - 入口：Lang.randomFrom(path) → languageManager.randomFromCategory（用户重构的 Lang 门面）。
2. **死因追踪**：Player.lastDamageCause（npc/fell/drowned/lava/default），设点=damagePlayer/
   岩浆 tick/溺水 tick/摔落结算；handlePlayerDeath 生成死亡文本 toast + 传给墓碑。
3. **墓碑** Tombstone.ts 重写为 DropTombstone+aiStyle17：款式按身家（≤10万铜→43/200-204，
   >10万→金 527-531；style 0-10 → Tiles_85 偶数列）；抛射速度/重力 0.2/翻滚 rotation+=vx*0.1/
   落地摩擦 0.98/无弹跳；底缘中心可放 2×2 → 放 tile85(style*36 帧锚) + world.signs + dig 声。
   **落点不佳（树/水上）会原地等待可放点——原版投射物同语义，勿"修"成弹跳**。
   渲染旋转原点改中心（投射物语义）；碑文=死亡文本+\n+zh 长日期。
   world.signs 已入存档；右键墓碑（interactAt tombstone_v 分支）→ UI.showSign 弹窗
   （GameCallbacks.onReadSign → mainFlow 接 ui）。
   TownNPC.givenName = newNpcName(vanillaId)，对话气泡带名字前缀；NPC 不入存档（saveGame npcs 恒空），名不持久。

验证：tests/random-text.test.ts（真实 l10n 包注入 loadPackJson）+ save signs roundtrip + E2E
（scripts/_death-probe.mjs：NPC 名 Gus/Claire、死亡→墓碑 1s 落格 signs:1）。
坑：tests/*.js 与 src/**/*.js 同为 tsc 陈旧产物会遮蔽 .ts（已清 tests 侧；src 侧部分残留，
vite.config .ts-first 兜底）；E2E 期间用户并发编辑触发 HMR reload 会打断探针（轮询重试模式）。


## 死亡画面移植（2026-08-12，用户令"移植原版死亡效果：中央文字+倒计时+画面渐灰"）
原版 = **DrawInterface_35_YouDied**（Main.cs:44765-44801）+ **GetDeathAlpha**（Player.cs:53284）+ **immuneAlpha ramp**（Player.cs:16873：dead 时 +2/tick 钳 255）：
- 「你被杀死了……」Lang.inter[38] @ 屏中-60（DeathText 大字号）；lostCoins>0 时下移 50 写「掉了{0}」（Game.DroppedCoins）；再 -26 → 重生倒计时「{0}」Game.RespawnInSuffix（数值=1+respawnTimer/60 秒，**zh 值是裸 {0} 无"秒"字**）scale 0.7 @ 屏中+10。
- 文字色 = GetDeathAlpha(Transparent)：r=0.9α g=0.5α b=0.5α a=0.4α——红黑渐显（immunAlpha 0→255 约 2.1s 走满）。
- **原版无全局去饱和**（"Death" shader 是 Chroma RGB 键盘灯）——灰化遮罩是我们对用户记忆的视觉近似：rgba(46,40,46, α×0.55) 全屏罩。
- 实现：Player.immuneAlpha 字段+Game fixedUpdate ramp+respawnPlayer 重置；Game.lostCoins（**掉钱计算要含 vi_71-74**——wld 存档的钱币是 vi_ 键，只算 coin_* 会恒 0，冒烟实证 lost 0→5000）；Renderer.drawDeathScreen（HUD 12 步，画在最上层）+deathLostCoins 每帧注入。我们重生计时 180t（3s，自有节奏非原版 3600）——倒计时格式照原版秒数式。冒烟 _death-smoke（已删）：dead/ramp/lost 5000/重生重置全✓。

## 增补(2026-08-13):死因全表移植
- CreateDeathMessage(Lang.cs:1010-1132)共 22 死因分支,原实现仅 5 类且 default 全走 Slain。
- **用户实证场景:站炽热狱石/陨石上烧死**——原版 DoT 致死(:19142-19156) suffocating→ByOther(7),其余(灼烧/着火/流血等)一律 **ByOther(8) Burned_1..4**(else 分支不区分火/毒)——已接。地块接触(尖刺:28514)=other3 DefaultWrap;掉出世界底=21 Underground;WoF 舌锁 DoT=12 WasLicked、舌距>3000=11 TriedToEscape。
- 死因映射号权威:Player.cs PlayerDeathReason.ByOther 调用点(19146-19201/22050-54/22989/23799/23831/24929/25085/27392/28514/37751/9938)。
- generic 两个占位符 {0}=玩家 {1}=世界名(Removed/Space_5 等条目用 {1});createDeathText(player,cause,worldName)。
- vitest node 环境拉不到 vanilla 语言包(fetch 无服务)→Lang.text 回落键名是环境假象,校验必须走浏览器探针(scripts/_death-text-browser.mjs,22 分支全✓)。


## /goal 终审(2026-08-13):"暂不可达"逐项核实
**已补齐(常规世界可达,原先缺失):**
- **petrified(5) 全链**:美杜莎 480 蓄力 AI(fighterAI 内 medusaChargeStep,cs:56751-56889 1:1——ai2 状态机/低血四参/45°锥/三路视线/双向对视)+ Stoned buff 156(封输入=Player.ts:1063 frozen 同段)+ 变身瞬间 Hurt(20×敌伤倍率,cause petrified)(:24924-24931)。美杜莎大理石房困难模式会刷(VanillaSpawner:2360)。
- **teleportFail 13/14/15**:混沌杖 1326 混沌期内再传送**允许传送+扣 max/7 可致死**(原 :44904-44913,此前实现为拒绝——语义偏差已对齐);性别分支 14/15(FEMALE_VARIANTS 判 skinVariant)。teleportFailMale/Female kind 新增(zh 文案同为 Teleport_2_*)。
**确认属实不可达(原版单人同,非缺失):** inferno(16)=PvP 光环专属;diedInTheDark(17)/starved(18)/vampire(22)=The Constant 秘密种子;space(19)=remix/ftw(forcedGravity 仅 getGoodWorld 克脑设置 cs:32573,重力药水不设);teamTank(20)=多人圣骑士盾转移。
**stabbed(6) 已补齐(2026-08-13 继续):** 同伴方块全链落地——BuffType.CompanionCube(84/vanillaBuff 191)+ item 3628 已在 vi_ 自动注册表(vi_3628_CompanionCube),Game.updateUse case 3628(UseSound Item_8+AddBuff 3600t+BuffHandle_SpawnPetIfNeeded 等价)+ MinionProj 653 家族(companionCubeStep,AI_067 light-pet 路径 1:1:buff 续命/岩浆尖叫 NPCDeath59|61+3600t 冷却/黑暗 lai1 -3600..120 计数/静止+无无敌→1/5 尖叫 Item_16 否则 Hurt(3,ByOther(6))+immune 清零/跟随 300px 切悬浮态/地面态 150px 摩停+jumpGate |vx|>3+距离表起跳/视觉 34×34 scale 0.8+cubeRot)。E2E:暗室静置 0.5-1s 被捅 3 伤,cause=stabbed,Buff_191 栏图标✓。_CompanionCubeScreamCooldown 静态 float[256]→单人模块级静态等价(备案)。
回归:enemy-ai-families/registry-clear/bossAI-lategame/gem 71 过;fullgen 双种子 21-26s。


## 二次 review 修正(2026-08-13,"无近似"复查)
- **混沌杖 1:1 重写**:原版首次传送**无 /6 代价**(旧实现自造);ChaosState 真 buff 88(360t 每次使用刷新,:44913)替代 chaosStateT(400≠360);混沌期再传 max/7+lifeRegenTime 清零+死因 13/50%性别 14/15;teleport 落点门(LimitPoint/墙线密度350/蜥蜴墙87)未移植=teleportToMouse 既有 BFS 近似(传送药水等共用,备案)。
- **美杜莎补全**:蓄力点光 0.9/0.75/0.1(两段,:56816/:56820);尘边界 num26<num25/num29<180 含 0 tick。netOffset 为联网位修跳过。
- **石化/冰冻禁用物品**:updateUse 头部补 Stoned∪Frozen 门(:24942-24950 controlUseItem 清零段——Frozen 此前只封移动不封使用,一并修);GrappleProj Frozen 门同侧补 Stoned。
- E2E(夜/平地/互视):蓄力完成→Stoned 上身(Buff_156 栏图标)→hp100→80→lastCause=petrified ✓;30 AI 回归全绿。
- Stoned 变身伤害走 damage():防御按难度系数结算(与原版 Hurt 同构)✓。

- 天花板提醒: stabbed 死因依赖的物品使用链已通,22+2 死因分支全部端到端可达或证实种子/多人门禁,无遗留。
