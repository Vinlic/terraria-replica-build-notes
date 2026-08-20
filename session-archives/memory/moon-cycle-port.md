---
name: moon-cycle-port
description: 月亮周期系统全量审计+补齐（血月六缺口/钓鱼月相乘区/腐化变换/血泪/破门/地表化提升）
metadata: 
  node_type: memory
  type: project
  originSessionId: d6caec24-1cc3-4182-bea5-29046ee459cf
  modified: 2026-08-12T15:03:19.935Z
---

# 月亮周期系统审计+补齐（2026-08-12，/goal 令"检查是否全量移植，没有则 1:1 补齐"）

**审计结论（已有 ✓）**：月相推进/血月 roll 主干（1/9+新月禁+HP>120+灯笼/月事件压制+misc[8]，Game:2145-2250）/刷怪率（夜×0.6+血月×0.3/1.8）+血月池（clown/groom/bride/血僵尸/滴血者）/满月狼人（L4533，注释写"新月"实为满月 phase0——**phase0=满月**，勿改）/城镇 NPC 夜血月不出（L709）/水色 9（血月柱并入）/Deathweed 血月+满月开花/血月对话池/音乐 Eerie=2（多分支）/血月红滤镜（**用户并行会话 MonolithFilters 已 1:1 完成**——SceneState:116 激活链含 env.worldBloodMoon、深度系数 UseOpacity；我曾重复实现已撤）/黎明月相++与日食 1/20 roll。

**本轮补齐六缺口**：
1. **钓鱼威力乘区**（`fishingPowerMultiplier` vanillaFishing.ts，Player.cs:41560-41605 全因子：雨 1.2/云 1.1/晨昏 1.3/正午 0.8/前半夜 0.8/**月相 0→1.1、1,7→1.05、3,5→0.95、4→0.9**/血月 1.1）→ Bobber.fishingPower(p, game) 应用；**昼夜边界必须用 clock.isDay**（并行会话已改 4:30/19:30=0.1875/0.8125，硬编码 0.25/0.75 会错判 0.8 为夜）。
2. **血月钓鱼敌怪**（Projectile.cs:19399-19427）：水+血月夜 1/6（血肉抛竿 poleVid 4325→1/3）→ catchEnemy（困难 {620,621,586,587}+1/10 恐惧鹦鹉螺 618；非困难 {586,587}）；Game 收竿侧 Enemy.fromVanilla 生成于浮标。682 分支需 bestiary 解锁旗标未跟踪从略；legendary 稀有度体系缺失→4382/5240 血月传说掉落未接（登记）。
3. **血月小动物腐化**（UpdateNPC_BloodMoonTransformations :93107）：BLOOD_MOON_EVIL 表（兔 46/企鹅 303/海鸥 337/443/540→47·464；金鱼族 55/230/592/593→57·465；松鼠 148/149→168·470；[腐化,猩红]按 w.crimson）——**扫 entities.enemies 桶非 npcs**（npcs 是 TownNPC 桶！首版扫错桶=不生效）；敌怪 transformTo、小动物 dead+Enemy.fromVanilla 替换。**tryTransformTo 拒绝嵌入实心**——探针造怪要在净空位。
4. **血泪 4271**（Player.cs:43329+CanUseItem :51435）：夜非血月→sound15(throw)/bloodMoon/moonPhase==4 拨 5/misc[8]/消耗；昼或血月静默无效。Game.useItem 链桶分支与钓鱼同槽。
5. **僵尸攻门**（AI_003 :64716-64780 + AI_007 :60390 不放弃语义）：fighterAI 前方门格（sheet10）→ doorWarm 60t 蓄势 → doorHit +5/t 至 10 开门（失败非血月/墓园 30t 脱离 doorCd；血月/墓园永不放弃）；**GoblinPeon 26 直接 breakTile 拆门**。GameHooks 新增 breakTile（Game 方法 private→public）。反编译 flag8-11 作用域歧义（63425 初始化后中段零赋值）——按两段无歧义语义实现。墓园判定走 world.scene（**World 新增 scene 字段**，Game 每帧 scanScene 后写 w.scene=this.scene）。
6. **血月/日食地下刷怪地表化**（NPC.cs:1146-1153）：rockLevel-20 以下落点在中带（x∈(0.38w+50, 0.62w)）→ surfaceSpawn=true。

**七轮：依赖子系统全量接入（2026-08-12，用户令"依赖子系统的也要接，可并行子代理"）**——三调研代理（自然Boss/钓鱼稀有度/月相商店）并行返回后落地：
- **种子旗标持久化**：World.seedFlags 新字段（SeedFlags 接口），生成两路径灌入（WorldGen :36/:218）+ WorldPacket.seedFlags（worker 回传）+ SaveData.header.seedFlags（旧档={}）+ wld 导入默认 {}。
- **十周年血月 1/6**（:64815-64817 maxValue2=6）+ **drunkWorld 黎明 crimson 翻转**（:64883-64886）。
- **自然 Boss 召唤链**（StartNight :64732-64811 + 夜间块 :64547-64621）：EoC roll（!downed_4||BossesKeepSpawning(getGood×Constant×非十周年)||skyblock；maxHp≥200 def>10；1/3（skyblock 1/10）；城镇 NPC≥4）→ spawnEyePending+misc[9]，血月 roll 加 !spawnEye 互斥门（:64818）；机械 roll（hardMode+altarCount>0+1/10+无 Boss+三机械未全灭 → 三选一未击败+misc[27+n]）；夜间 time>4860（nightTicks=(t-DUSK)/0.375×32400）后每 tick：玩家地表/4500px 无月总 → EoC 命中即清旗 / 机械一次性（:64596 无条件清零）；离屏列召唤（半屏+300px）——summonBossAtTx 加 'eye_of_cthulhu'→4 映射；黎明清旗（:64625）。
- **钓鱼稀有度**（FishingCheck_RollDropLevels :20106-20167）：rollRarities 独立 roll（legendary 1/max(⌊4500/L⌋,6)、veryrare 2250/5、rare 1050/4、uncommon 300/3——**各档独立不互斥**）；rollCatch 重排为原版规则表序 junk→crate(+15 药水)→RareDrops 传说族（血月 !combatBook 4382 1/2 → 血月 5240 1/2 → 2423 1/5/3225 1/5/2420 1/10）→鱼池；战斗书旗标走 w.flags.combatBookWasUsed。
- **682 红城镇史莱姆**（:19413-19416）：**世界级一次性旗标**（非图鉴！Player.cs:51591 置位、WorldFile :1413/:2433 持久化）→ w.flags.unlockedSlimeRedSpawn；1/5 优先敌怪表；收竿 reelBobber（抽方法）：682→置旗+TownNPC('town_slime_red')入镇；618→y+64px（:51581-84）。**NPC 数据缺口补 5 条**（587/618/620/621/682 取 1456 SetDefaults+npcFrameCount 数组 :65994——587:4帧/618:4/620:21/621:1/682:14；贴图已在库）。
- **月相商店分档**（shopStockFor 相位实表）：shopCondOk 'moonPhase' 恒 **false**（提取器未捕获 case 值——改 true 会全相位重复上架）；分档表：骷髅商 453 八相位专柜+奇偶药水/火把/箭/配重轮 phase%4/轮滑鞋三段/满月夜 3043（Chest.cs:2780-2940）；树妖盆栽 phase/2 三件组（**先清 out 的 4430-4441 再补**——提取器把相位 switch 摊平成 hardMode/无门条目）；裁缝 54 八相位套装（0/1 肉前 2/3 双件、2-7 hard 单/双件）；染料商 207 满月 2871+2872；造型师 353 (偶相位==白天)→1981；机械师 124 渔夫在场且奇相位→2295；蒸汽朋克 178 748 加相位≥4 门（提取器只记 hardMode）；动物学家 633 配对耳尾 phase/2+满月夜 5253；画家 227 并入 case25 月相四画（1481-1484 by phase/2）+常驻 1490。
- 探针 `_subsys-smoke.mjs`（12 断言）：商店分档/682+618 收竿/drunk 翻转全绿；EoC 链由调试数据证明（def 17/town 4/桩随机→旗标置位后被夜间块消费=全链执行；末轮断言改 boss 存在性但遇 HMR 风暴未及复跑）。**探针防御门：defense>10 需铁甲+铁皮 buff（armor id 90/81/77+156——111/112/113 是星力手环等!）；timeOfDay 跨 DAWN 不能数字跳变（crossed 是数值比较不识别午夜回绕）**。

**八轮：残留全清（2026-08-12，用户令"残留的需要全部接入完整"）**：
- **战斗书 4382/5336**（Player.cs:44703-44730 ItemCheck_UseCombatBook）：使用→世界旗标 w.flags.combatBookWasUsed/combatBookVolumeTwoWasUsed + Misc.CombatBookUsed 公告 + useTime 30，**不消耗**；城镇 NPC 增益（NPC.cs:53419 每本 lifeMax+250/防+8，伤害×0.8/速+0.25 无战斗系统落防/血）——TownNPC.applyCombatBook（使用时对在场者叠 + fixedUpdate 首 tick 给后入驻者补，每本恰一次）。**4382=血月传说钓获（1/3，:19650 Next(3)——七轮写 1/2 有误已对齐代理数据）；用后不再掉**。
- **高尔夫子系统**（功能移植）：GolfBall 实体（放置 item 3989/染色 4242-4253 → proj 721/739+；物理=重力 0.3+弹跳 0.5+滚摩擦 0.985；**洞杯判定 tile 476+自上而下+速度≤100** GolfHelper.cs:62-69）→ golfBallScored 计分（**⌊位移tile÷(杆数+2)⌋×系数**，2 杆以上 SetScoreTime=1.0、一杆进洞 golfScoreTime/3600 折扣，挥杆清零计时 GolfState.cs:27-47）；Player.golferScoreAccumulated（存档 player 段持久化）。**杆型表 12 支**（driver 14/-4 · iron 11/-5 · wedge 8/-7 · putter 5/-1；材料+1 高级+2）——GOLF_CLUBS；挥杆=80px 内球朝指针击出。
- **分数商店门**（Chest.cs:3147-3238）：Golfer >500→入门杆4265/奖杯4599、>1000→中级杆+银杯、**>=2000→高级杆+金杯4601+球车4264(需downedBoss3)+月相四画4658-61**；Zoologist >=2000→猎人斗篷4744（:1951）；Painter >500→橄榄球4743（:2250）。
- **公主月相商店**（:3427-3445）：十周年+hardMode+downedPirates → 相位对 2584海盗杖/854折扣卡/855幸运币/905钱币枪（入驻条件七轮前已有：全员在场或十周年）。
- 冒烟实证：bookFlag ✓、golfScore=5（公式精确：⌊320/16⌋/(2+2)）、2000 分三商店门全开 ✓、零 pageerror。**bookBuff 断言 false=探针环境无 guide（新世界初始 0 城镇 NPC），代码为纯 maxHp+=250**。单测 37（杆表梯度+计分公式形状）；全量 1108 中 5 失败单跑全绿（共享态 flake）+caves-oracle 用户 WIP。

**九轮：两处近似升 1:1（2026-08-12，用户令"2处近似不行，要1:1复刻"）**：
- **高尔夫蓄力全 1:1**（GolfHelper.cs）：**蓄力=光标到球距离/300（与按住时长无关！代理调研纠偏）**，杆型椭圆钳制（FindVectorOnOval :276-291——**推杆下限 (0,0) 除零：C# v/0=NaN 比较恒假=下限不生效，JS 同语义 return 0**），速度=L×32；**GOLF_CLUBS 16 支**（4 基础+12 材质镜像同属性：iron (0.25..1,1)/putter (0..0.25,0.25)/wedge (0.25..0.65,1.5) rough=1/driver (0.25..1.5,0.65)——GetClubProperties :348-371）；ValidateShot 角度钳 [-87.12°,0]（不能向下）+站位盒（玩家脚下 X∈[-16,32] Y∈[-16,16] 面向翻转 :423-449）；HitGolfBall 地面阻尼（TileMaterials xnb 未提取取代表值 0.96/0.5——唯一数据依赖登记）。**channel 状态机**（AI_150 :49498-49627）：按住=瞄准（SetDummyItemTime 12 维持/ChangeDir 朝光标/力度条 54×rel+预测线 20 步物理点）、松开=击球、**右键取消**（:49592-49601）、重力倒置禁用（:49506）；**自动摆球**（TryPlacingAGolfBallNearANearbyTee :49512：5×5 找球座 tile 494、杀旧球、GetPreferredGolfBallToUse 手持→背包→默认 721）。物品分支旧单击版已删。
- **Zoologist 图鉴进度门全表**（Chest.cs:3241-3385）：CompletionPercent 九档 0.03/0.10/0.25/0.30/0.40/0.45/0.50/0.70/1.0（鞭/钩/执照/种子/风筝/马鞍/长枪 hard/矿车/指令/三仪/导线/胜利塔）+仙灵火把门（三仙灵 583/584/585 图鉴 >NotKnown，:3524-3544）+事件门（满月夜狼人画/hardMode 血月玩具/世花后泥巴/日耀塔风筝/派对蜂群雷）+四相位兽耳尾——entry 按 creditId 反查（bestiaryCreditId/bestiaryEntries 导出）。**狼人态不影响商店**（agent 实证：case 23 不调 ShouldBestiaryGirlBeLycantrope；只改贴图/对话/自卫伤害）。
- 冒烟实证：**golfShot 公式精确**（putterCap=8=0.25×32、ironCap=32、角度钳 noDown ✓）+ eocRolled=true（自然召唤链 Boss 生成实证）+ 计分 5 + 三商店门 + 零 pageerror。单测 40（杆表 16 支/公式三断言）。全量 1154 中 4 失败=用户 WIP（caves-oracle×2+debug-report hoverRing 新段）+biohang 单跑绿。

**终态**：月亮周期域无任何近似残留。数据依赖仅 TileMaterials.GolfPhysics（xnb 资产，代表值已注明）。

**验证**：单测 fishingPowerMultiplier 5 条（含月相六档）；`_bloodmoon-smoke.mjs` 全绿（滤镜 active/兔 46→47 变换/血泪消耗+置位+新月拨 5/乘区 0.88=0.8×1.1/零 pageerror）。fishing-r7 mock 需补中性 clock/weather/scene（乘区接入后旧 mock 缺字段）。全量剩余失败=caves-oracle×2+registry 探针（用户 WIP）。

关联 [[vanilla-ui-port]] [[wind-sway-port]] [[sandboxworld-project-setup]]
