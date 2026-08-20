---
name: town-npc-attack-port
description: 城镇NPC自卫攻击(AI_007四态)+头顶表情气泡移植;NaN判距门教训;Extra_48是表情总表
metadata: 
  node_type: memory
  type: project
  originSessionId: c212e38d-8db4-446d-b3da-4e20d707caf7
  modified: 2026-08-12T16:49:49.117Z
---

2026-08-13 用户报"原版向导会射箭没对齐"+"NPC头上的气泡没了"。两项均未移植,本轮落地:

**自卫攻击**(原版 AI_007_TownEntities 攻击态,NPC.cs:54747-55538;触发门 :55621-55966):
- 数据 `src/data/vanillaTownAttack.ts`:NPCID.Sets 四表(DangerDetectRange/AttackTime/
  AttackAverageChance/AttackType,NPCID.cs:4835-4851)+四态逐类型参数(10 近战弹/12 弓/
  14 魔法/15 挥击)。**向导=22:AttackType 1,肉前木箭 proj1 伤12、肉后火焰箭 proj2 伤+6,
  速10/散布±0.7/aimLift 4**;209 三选一弹;229 PrettySafe 近距换 162 炮弹。
- 运行时 TownNPC.attackUpdate:站地+冷却(localAI[1]=cdBase/2+rand(cdRand))+探测范围
  (默认200)内 LOS 敌(canHit)→掷骰 1/max(1,chance×2)(209 ÷3)→入态;态内 ai[1]--/
  tick++/vx×0.8,发射档=shootTick+burst 连发链(`localAI[3]>档→推下一档`);退出回冷却。
- 友方弹 `TownShot.ts`(箭族重力 0.3,只伤敌)。GameHooks 新增 spawnTownShot。
- 难度伤害缩放 townNpcDamageMult 恒 Classic=1(Expert 1.5 未接难度系统);挥击态中段单 hit
  近似(原版逐 tick 弧形);15 态换侧重挥未接。
- **教训:判距门 NaN 恒假**——敌 mock 无 cx 字段,`NaN >= range` 恒 false 距离门形同虚设
  (测试抓到);敌中心必须由 x/y/w/h 推导,勿依赖实体 getter。
- 回归 tests/town-npc-attack.test.ts(4 断言)。

**表情气泡**(EmoteBubble.Draw :201-224):
- **真身贴图 = Extra_48.png(272×1092,8 列×32 行、34px/格)**——Images/UI/Emotes.png 是
  64×32 空壳勿用;EmoteBubbleBorder.png 是遗留。图集 MISC 已收 Extra_48。
- 绘制:头顶底锚;首尾 6t 边框帧 (1,0) 否则 (0,0);图标格 = (emote*2%8+anim, 1+emote/4)。
- 触发:空闲随机冒泡(1/3600/t,240t,emote 均匀 0..120)——原版情境驱动(NewBubble 散落
  多处+NPC 互聊 16/17 态)未移植,属可见子集近似。

**受击链全量补齐(2026-08-13 追问"npc受击可以正常掉血吗")**:此前仅陷阱弹命中城镇 NPC。本轮按原版三源补齐:
- **玩家弹幕/近战 = 巫毒窄门**(Projectile.Damage_PVE_Inner :11970-11976 + ApplyItemToNPC):仅向导 22
  (装备向导巫毒娃娃 267→equipStats.killGuide)/裁缝师 54(裁缝娃 1307→killClothier)可伤——
  **其余城镇 NPC 玩家武器一律无效**(曾险些全族误开,测试前查源拦下);Player 装备聚合新增两旗标;
  projTargets.hitTownNpcs(source: 'playerProj'|'hostile')统一门禁,WeaponProj/Arrow/MagicProj/
  FallingBlock/WhipProj/挥砍全走此 helper
- **hostile 弹(敌怪弹/陷阱)恒命中**(:11975 flag2 = hostile && victim.friendly)——Arrow hostile 分支已补
- **敌怪接触**:GetHurtByOtherNPCs(:93605-93690)移植进 TownNPC.envHurtUpdate——任一 damage>0 敌接触
  → hurt(def.damage, dir*6),专属 30t 冷却(immune[255]);dryadWard 荆棘反伤/HurtingBees 未接
- **岩浆**(:94511-94530):50 直伤/30t;**溺水**(CheckDrowning :96118):breath 200/水内 7t -1,
  尽后每 7t life-=2(不过防御),归零 StrikeNPC(2) 致死一击
- 教训:①敌 mock 无 cx/cy getter 时 NaN 比较恒 false(判距/重叠全部用 x/y/w/h 推);
  ②专属冷却初值勿写死(immune[255] 起始 0,我误初始化 30 白锁半秒,测试抓到)
- 回归 tests/town-npc-hurt.test.ts(6 断言);并行会话在途 test 改用 VANILLA_ITEM_KEY_BY_ID 漏 import
  已代补(tests/projectile-reflect.test.ts)

**地图头像层+Boss指针考古(2026-08-13)**:
- 地图画像原版三件套(Main.DrawMap :55546-55700):玩家头(MapPlayerRenderer=角色头层含发型/
  头盔)/城镇 NPC 头(NPC_Head_{TOWN_NPC_HEAD_INDEX},恒显 CanBeSeen_Townie=true :55756,
  朝向翻转)/**Boss 头(NPC_Head_Boss_{BossHeadTextures 表 NPCID.cs:4861,68/262 带
  npc.rotation,世吞 134 多段质心平均)**——Boss 也在地图上,用户疑问已证
- headScale:小地图 min(1,(1×0.4+1)/3)≈0.47 / 全图 min(1,(zoom×0.5+1)/3)(Main.cs:55059/:55140)
- **"Boss 屏外边缘指针"原版 PC 不存在**(全反编译树零命中;屏外反馈=顶部 BigProgressBar
  血条+头像恒显)——用户记忆疑来自 tMod 模组,未移植
- 实现 Renderer.drawMapHeads:纸娃娃 0 帧顶 24×22 裁头(黑描边四向暗影近似
  OutlinedTextureRenderer)+NPC/Boss 头贴图;小地图旧 Player_0 帧、全图脉冲环+箭头标记
  全部退役(原版只画头);数据 BOSS_HEAD_INDEX/bossHeadRotation 入 vanillaNpcs.ts
- 未接:Plantera 266 隐藏/世吞质心/35·127·345 ai 门旋转/262 半血换头(GetBossHeadTextureIndex 特判)

**地图头像三轮修正(2026-08-13 用户反馈三项)**:
- **裁剪**:头像层必须 clip 到小地图框(窗口外 NPC 头像外溢 bug)——小地图支包
  ctx.clip(rect);全图天然出画布裁剪无需处理
- **玩家头裁带**:原版=PlayerHeadDrawRenderTargetContent(发型/头盔全层组合头,中心锚);
  纸娃娃裁 24×22 会削发型 → 改帧 0 顶部【40×32】整宽带(drawHead 加 sw/sh 参数)
- **缩放公式两支曾安反**:小地图(mapStyle1)=min(1,(mapMinimapScale×0.25×2+1)/3)×UIScale
  (:55140/:890,1.05);全图(overlay mapStyle2)=min(1,(mapOverlayScale×0.2×2+1)/3)×UIScale
  (:55059/:894,2.5)——另漏乘 UIScale≈1.1(displayHeight/1080×1.1 :4281)。
  注意:我们全图默认 zoom=0.5(fit 全世界)≠原版 overlay 默认 2.5,头像小属该设计差,
  放大后随公式长到 cap 1

**成就弹窗原版化(2026-08-13,用户问"位置一样吗")**:此前成就解锁走顶部通用 toast——错。
原版 = InGameNotificationsTracker(Main.cs:45542→Tracker :38-52)+ InGamePopups.AchievementUnlockedPopup:
**底部居中、距底 40px(手柄 65px)、多条 50px×opacity 向上堆叠**;300t 寿命(前 30t 淡入/末 15t 淡出);
库存蓝底 Color(64,109,164)×0.5(hover ×0.75);64px 成就图标(Achievements.png 8/行 66 栅格)+
Achievement_Borders 边框(scale×0.3);标题右对齐图标左;点击开成就页并移除。**不是左下消息栏**。
实现:UI.achievementPopup(CSS 底锚 40px/5s/蓝底/图标 clipPath 栅格裁切+边框),GameCallbacks.
onAchievementPopup 优先、缺省回退旧 toast;点击=关闭(成就页 UI 未接,GAP)。
l10n 键 Toast.AchievementUnlocked 保留作 toast 兜底文案。顺带补齐并行会话 prefix 类型链三处
(slotContent/paintSlot/ChestData.items)。

**成就弹窗 review 修正(2026-08-13 自审)**:初版三处偏差已修——
①图标 64px→**21px**(原版 num3=num×0.3≈0.33,整表 ×21/64 缩放后按 66px 栅格偏移定位);
②direction:rtl 把标题/图标放反→原版【图标在右距条右缘 33px(=12+num3×64 :107)、标题右对齐
其左 10px(anchorx=1 :110)】;③堆叠 gap 6→19px(PushAnchor 50px音高 :89)。
实测探针(_achprobe):卡片底缘=屏高-40 ✓ 中心=屏宽/2 ✓ 条高 33≈原版(标题高+10)×1.1 ✓
图标 21×21 ✓ bg=rgba(64,109,164,.5) 逐位 ✓ 右内边距 33px ✓。

**同类问题 sweep(2026-08-13 review)**:HUD 锚点逐项对账原版——
- Buff 行:32/76/38列宽/50行距(Main.cs :42636-42645)✓ 早已对齐
- Boss 血条:456×22、水平居中、距底 50(BigProgressBarHelper :51 CenteredRectangle
  ScreenSize×(0.5,1)+(0,-50))✓ 我们 rect y=viewH-50-BH/2 等价
- 快捷栏:原版左上角 ✓(我们 top:0 left:0)
- **表情气泡=双实现实锤**(与双血条同病):并行会话的 render/EmoteBubble.ts 模块
  (spawnEmote/tickEmotes/drawEmotes 1:1,GetPosition 头顶锚+开合帧)在本会话内联
  drawTownNPC 气泡版共存 → 双画。合并:内联版+TownNPC emote 字段/掷骰全部退役,
  空闲随机冒泡改由 Game.tickNpcEmotes 窗口(600t)喂 spawnEmote(npc, rand 0..120, 240t)
- 教训:并行会话新增模块时先 grep 全文同名系统再动手(双血条/双气泡两案皆然)

**信息饰品系统移植(2026-08-13,/goal 四任务)**:原版=Main.DrawInfoAccs(Main.cs:46142-46665)
12 行右侧列(非 tMod 的 InfoDisplay 类——1456 无此类)。落地:
- **P0 阻塞点**:extract-equip-prefix.mjs:111 只认字面 `accessory = true;`,22 件信息饰品走
  DefaultToInfoAccessory(Item.cs:48234→:48229 accessory=true)全漏 → statOfInternal null →
  armorAccepts 拒收。修=scanCaseFields 支持存在性模式(无捕获组恒记 1)+ACCESSORY 并入
  DefaultToInfoAccessory/DefaultToAccessory + 手补 3124/5358-5361(反编译伪影缺辅助调用,
  Player.cs:12353-12394 列为 OR 源)。重跑 +61 条 acc==1(总 345)
- **数据**:src/stats/InfoAccs.ts(纯函数:gates 12 字段/refresh 1:1 :12319-12400/换算器
  formatWatch|Weather|MoonPhase|Compass|Depth/mphOf/buildInfoAccRows 分支序)。
  Player.equipStats.infoAccs 聚合(vid 直查先例 killGuide)+运行态 hideInfo[13](:776)/
  lastCreatureHit/speedSlice[60]/DPS 五态(addDPS 门禁 accDreamCatcher,Projectile.cs:12817)。
  Enemy.hurt 尾参 fromPlayer(Game 挥砍+Arrow/WeaponProj/MagicProj/WhipProj/Dart 传 true;
  TownShot false——npcProj 不计)。SceneMetrics 补 bestOreSheet/X/Y+34 条优先级表+frameX 变体门
- **绘制**:render/InfoAccsLayer.ts(几何 X=W-280/行距22/矮屏20/背包横排图标/悬停+13 框);
  InfoIcon_0-13 已入 vanilla-ui 白名单。**小地图常显时间/天气文本已门禁化**
  (accWatch/accWeatherRadio,无饰品消失——原版语义);调试面板保留
- **开关+存档**:背包内点图标切 hideInfo(吞点击复用 timeUiHover 槽);serialize/SaveFile/
  mainFlow 三处 hideInfo?: boolean[](旧档缺省 false;worker 走 serialize 纯函数自动覆盖)
- **获取**:掉落 18/393/3095/3102(npcdrops✓)/六表+雷达秒表分析仪 DPS 计(商店✓)/
  工匠组合 395,3036,3121,3122,3123,3124+5437 贝壳手机(=3124+4263+4819,✓全在 recipes)
- **遗留 GAP**:渔夫任务奖励池(Player.cs:55351 GetAnglerReward 池
  {2373-2375,3120,3037,3096,5139}+DropAnglerAccByMissing 持有剔除)未建;5437 使用变身
  5358-5361 未接;accWatchTime(床冻结)未跟踪;金色生物染 OurFavoriteColor 未接
- **三套索引必须分开**:行序(分支序)/图标序(hideInfo 下标,8 归并 7)/物品 id——
  Explore 阶段的"12 项固定链序"表述不准确,Plan 代理已纠

**持械视觉(AttackType1,2026-08-13 用户报"没拿武器效果"补)**:原版=DrawNPCExtras(Main.cs:27121-27195),**不在 DrawNPCDirect 主体**(全区域搜 townNPC 零命中,别再找错地方):
- 触发=AttackType==1 且 ai[0]==12 攻击态全程,beforeDraw=false(本体前层)
- **228/229/209 提前 return 无持械**(:27124-27126);持械仅 5 NPC:19(枪 HM98/前95)、**22(木弓39,grip18,aim>-0.1 锚Y+4)**、178(434)、227(3350,scale.85)、368(HM2223/前2269 scale.75)
- 锚=Bottom−OffsetsNPCOffhand[2](14,26),spriteDirection==1 偏移X取负;旋转=ai[2]×90°×朝向
- **ai[2]**=:55191-55197 发射档取【目标中心】方向Y钳±0.5(非 aimLift!),态尽归零(:55203)
- 握位 num12=floor(W/2)−grip(DrawPlayerItemPos.X恒W/2,Y表全是死码);右向 dx=num12、左向 scale(-1,1) 镜像=原版 origin=(W+num12,H/2)+Flip 等价几何
- 实现:TOWN_HOLDOUT 表(vanillaTownAttack.ts)+TownNPC holdoutAim/hardMode getter+Renderer.drawTownHoldout(atlas.vicon 取真图标)
- 探针 _townholdout-probe.mjs 7断言全过(**命中瞬间同步 toDataURL+像素断言**——态窗仅0.5s,异步截图必错过;手部区域113木弓调色板像素);私有 vite 5202 已清
- 未接 GAP:AttackType2 魔法光环(Extra_51,:27216)/AttackType3 GetSwingStats 挥弧(:27235)/向导 Extra_52 扶弓手(frame≥21)
