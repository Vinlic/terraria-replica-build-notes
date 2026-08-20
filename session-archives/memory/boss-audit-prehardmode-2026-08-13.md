---
name: boss-audit-prehardmode-2026-08-13
description: 肉前三王+肉山1:1审计与全量修复:EoC专家状态机/世噬分体语义/肉山困难模式转化链+舌头机制
metadata: 
  node_type: memory
  type: project
  originSessionId: 8f9c7b63-58b1-49de-a435-85fe12e156d6
  modified: 2026-08-13T16:41:39.370Z
---

2026-08-13 肉前三王(克眼4/世噬13-15/克脑266-267)+肉山(113+眼114+饿鬼115/116+水蛭117-119)三线逐行审计+修复收官。审计还勘误了我方任务书三处(部件 id 114/115/116 非 88/110/121;266 帧是 7t 非 6t;闲置豁免集 117 不在原版列表)。

**核心修复**:
- **肉山 P0×2**:困难模式世界转化链(HardmodePass.ts:GERunner 三套转化表 1:1+V 带位置+洞穴墙回填+砖盒 140/347;Game 击杀流原序接线:brickbox→捕获旧 hardMode→startHardmode→!wasHard 灯笼夜19→misc[15]+成就9 迁移;**RNG 备案:原版 genRand 流中段不可复现,用 new RNG(seed) 结构性等价**);巫毒娃娃岩浆召唤链(ItemDrop.checkLavaDeath+spawnWOF 全门禁 1:1)
- **肉山 P1/P2**:舌头机制(Player.wofTongue:Horrified79/TheTongue80 双 buff+140px 带 50 伤+专家 50HP/s DoT+3000px/到边即死+updateUse 禁道具门;原版**无拖回**,3000px 是击杀线);bossFled×2(到边/玩家死≠击杀);Hungry→116 转化;激光 83 extraUpdates=2(Arrow.subStep 拆分);专家 Hungry 重生;水蛭体节链;Zombie_10 尖啸
- **克眼**:专家/大师参数+P2 状态机 state 3/4/5 全段重写(:19967-20756);P2 伤害/防御覆写(23/36/54+def 0/-15/-30;**legacy 路径 ENEMY_DEFS 共享引用,直写 def 会污染全表——恒等判断后拷贝**);变身两段 200t;残影真门;仆从朝向 −π/2(pngjs 实测瞳孔朝帧底)
- **世噬**:分体语义全量重构(杀中段=拆两条独立虫/杀头=下段晋升新头/仅最后一段置 boss 位走全套掉落 DropEoWLoot);65/70 体节;掘地/空中双模;专家毒唾 666;离开腐化下潜消散
  ★**离屏消散 bug(用户实测"打两下自动战败",2026-08-13 晚修)**:体节 14/15
  SetDefaults boss=false(仅头 13 是 boss)→ 不在旧豁免名单 → 离屏 750t(12.5s)
  消散 → 蠕虫级联整链同灭(含头)→ Game 误判击败公告+downed。修复 = 原版
  DoesntDespawnToInactivity 全量名单(NPC.cs:78584-78679,含 14/15/113-115/118/
  119/134-136 等 59 id)+ CheckActive flag2 强真名单(:78735-78758,13/35/39/127-131/
  392-394/491/492)+ 条件豁免(139 需 134 在场,552-578 需 548 在场)。
  ★**VANILLA_BOSS_IDS 全量对账**(NPC.cs 逐 case 提取 boss=true):曾缺
  **396/397(月总头/手,原版 boss=true!)**、578(DD2 闪电甲虫 T3)、664(火把神)
  ——补入;68 地牢守卫/325/327/345/346(月事件)原版无 boss 位,不入。boss 槽
  接管点已审(仅联机傀儡/F6/显式召唤),事件怪补入无副作用。
  ★**EoW 聚合血条**(EaterOfWorldsProgressBar.cs:18-46):原版=全场 13-15 段
  HP 之和 ÷ **恒定分母**(链段数+2)×150,杀段缩分子不缩分母,锚死自动换段
  续显(TryFindingAnotherEOWPiece)。我们旧实现=单锚 hp(打身体段血条不动)。
  修复:Enemy.eowChainMax(spawnWormChain 写全链)+ Game.render 参数构造处
  13-15 族聚合求和。
  ★**毁灭者共享生命(realLife,与 EoW 完全相反的模型)**:NPC.realLife :6086;
  头 134 首帧建链时全链 ai[3]=头(:50206-50227)→ **段 135/136 受击伤害传导扣
  头 80000 总血、段 hp/maxHp 镜像**(StrikeNPC :82132-82137)——节不可单独打死,
  血条=CommonBossBigProgressBar 单锚头自动正确;防御按【本段】结算(135 def=30)。
  实现:Enemy.realLifeHost(null=独立,EoW 恒 null :51524)+ hurt 分流传导 +
  destroyerAI 建链赋值。测试坑:Clock 默认 8:15AM 白天——destroyerAI 白天钻地
  撤离会整链 dead 测试必设夜晚。tests/destroyer-reallife.test.ts 3 条,
  6 套件 54 绿
- **克脑**:专家四镜像幻影(以玩家中心镜像,alpha=(1-life/max)²×2);FindFrame 0-3/4-7 双相;266 JSON 修正 1456 值(1250/0.45,原 JSON 系 1405 提取)

**How to apply:**
- 遗留备案:WoF 墙身大贴图平铺渲染(WallOfFlesh.png 未入库)+肌腱链+舌头视觉;hurt() 负防御钳制会吞 P2 专家 -15/-30 增伤(独立审计线);毁灭者链 spawnWormChain 差一体节;getGoodWorld 分支按仓内惯例留注释
- knockBackResist 缺省已修 ?? 1(原 0.5,影响 137 只)
- 同日世界生成金标(terrain/caves/world-final)被并发会话在途编辑打红(TerrainPass 08:41 改动致 rockLevel 475→463)——非本批,勿抢修
- 教训:大任务代理易被 API 流看门狗打断——拆小批+「收尾模式」唤醒(完成在途项+报告,不开新项)最有效

**2026-08-14 追记:EoC 二阶段冲刺"体感速度差"结案(非 AI bug)**
- 数值链逐行复核 NPC.cs:20452-20756 全 1:1(单冲 6.8/专家 ×1.15×1.3/摩擦
  0.97+0.98/冲程 130/专家 90/连冲 20/悬下方 ×1.3),探针 7 断言全绿(首速恰 6.8、
  前 40t 零摩擦、130t 一冲、3 连 262t、悬浮 200t 出冲)
- ★**eocAI 尾部 x+=vx 是唯一积分点**——Enemy.ts :5717 的 noTileCollide 分支属
  flyAI 内部非通用物理段;曾误判"双积分"删除致 EoC 定格,tests/eoc-dash-speed.test.ts
  就是防再删的回归(删→0,双→13.6)
- **真根因 = 渲染层有效缩放**:canvas 背板是 CSS px(无 devicePixelRatio 适配,
  Renderer.resize)+ 默认 zoom 1.25 → retina(DPR2)上等效原版 250% 缩放:同屏
  世界视野仅原版全屏 40%,屏上读出速度 ≈2.5×。已把 Camera.ZOOM_MIN 0.75→0.5
  (retina 上 0.5×2=1.0 恰等效原版 100%,滚轮/± 可达)。**遗留决策**:canvas 走
  DPR 背板可根治(锐度+原版真视野)但 4× 填充成本+UI 全链路要动——需用户拍板

## 2026-08-14 附:骷髅王/机械骷髅王旋冲"只摆不转"根因
- 根因:两 Boss(35 AI_011/127 AI_032)旋冲/狂暴段 `spin += facing*0.3`,而 facing=每帧 sign(vx)——冲过玩家贴脸时 vx 反复换号 → spin ±0.3 震荡=肉眼"两边摇动"。原版 rotation += **direction**×0.3 的 direction 是 TargetClosest 的持久字段(目标侧),旋冲全程不换号。
- 修复:进旋冲/狂暴段时把目标侧冻结进 ai3(两 Boss 头 ai3 均未占用),段内 spin += ai3*0.3;顺带 35 hover 补 rotation=vx/15 倾转、127 hover 改原版 AngleLerp(vx/15*0.5, 0.75) 阻尼。
- 验证法:采样 e.spin 时序断言单调 +0.3/t(44t 全绿);贴脸过冲点(t≈22 dist≈5)是翻号高发处,回归探针必测。
