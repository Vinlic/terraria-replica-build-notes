---
name: boss-summon-announce
description: Boss 召唤的公告文本/音效/BGM 原版语义——统一格式+双子/月总例外、Roar 唯蜂后例外、每 Boss 专属 BGM 表
metadata:
  type: project
---

2026-08-10 Boss 召唤三件套按 1.4.5.6 校对（Game.announceBossSummon + Music.ts BOSS_MUSIC）：

- **公告**（SpawnOnPlayer 末尾 switch NPC.cs:81495-81511 + NewNPC:81548）：default → `Announcement.HasAwoken`（"{名}已苏醒！"，名字走 Lang.npcName）；**双子 125 专项 `Lang.misc[48]`"双子魔眼已苏醒！"**；126/398（部件/第二只）不播；**月总 398 特判 `Enemies.MoonLord`**（"月亮领主"，不取 MoonLordCore 名）。颜色 ChatColors.BossOrEvent = (175,75,255)，走 onChat（未接线回退 toast）。旧实现统一播 misc[9]"你感到有个邪恶的东西在看着你……"是错的（那是 EoC 自然生成预警文本）。
- **音效**（Player.ItemCheck_UseBossSpawners:43083+）：**全部 SoundID 15 Roar**——用户以为每个 Boss 不同，源码事实是统一的；**唯一例外 Abeemination(蜂后) → SoundID.Item173**（已用 xnb-unpack 提取 Item_173.xnb → public/sounds/，Sfx 名 'beeSummon'）。
- **BGM**（Music.ts BOSS_MUSIC，Main.cs:12162-12280 type→槽位 + :12474-12535 槽位→MusicID）：EoW 99/骷髅王 104/史莱姆王 93/血肉墙 12/双子 97/Prime 98/毁灭者 92/蜂后 96/石巨人 17/世花 24/克脑 13(Boss3)/猪鲨 58/月总 38/异教徒 94/光皇 57/史莱姆皇后 56/鹿角怪 90；**未列入表 boss → Boss1(5)**。pickMusic 的 bossMusic 参数先于全部群系分支；Boss 盒 = 屏幕±5000px（异教徒/光皇相位 1600px 暂按 5000 近似）。MusicInput.bossNearby(boolean) 已废弃为 bossMusic(number)。
- 测试：tests/boss-summon.test.ts（映射表逐项 + 优先级压过地狱曲）。

**Why:** 用户要求"每个 boss 召唤文本/音效/BGM 各不同"——对照源码后：文本和 BGM 确实各不同（按名/按表），音效原版就是统一的（唯蜂后例外），不能臆造差异。
**How to apply:** 加新 Boss：BOSS_MUSIC 补映射 + 公告默认自动走 HasAwoken（Lang.npcName 有名即可）。关联 [[music-extraction-off-by-one]]（BGM 文件映射曾错位）。

## 2026-08-14 全量审计终态(26 Boss×3 列,tests/boss-music-parity.test.ts 冻结表)
- **史后=657/光女=636**(勿混);火把神 664 小游戏曲 101 优先于一切 Boss;Mechdusa(remix+getGood 机械族)曲 25 覆写。
- 公告/音效**解耦**:原版物品召唤多数带 Roar、生成路径多数无声——曾捆绑"公告+Roar"致 7 处自然路径多吼(自然EoC/机械自然/鹿角怪雨/世花灯泡/蜂后幼虫/暗影珠/老人诅咒);静默生成集{50,82,126,316,551,662}∪{68,395,439,396,397,664};**骷髅王召唤物无吼**、史王/Betsy/邪教徒/月总无苏醒公告、双子只 125 公告(126 静默)、月总公告带 Enemies.MoonLord 前缀。
- 死亡音=本体 DeathSound(曾统一咆哮吞掉);唯一额外死亡咆哮=EoC gore 双吼;月总核心无声;双子先死一只不公告,末死播 Plural。
- 蜂后物品吼=Item_173(唯一);地牢守卫=全游戏唯一非物品生成 Roar(aiStyle11 首帧)。
- 火星入侵曲=37 非 39;入侵走精确 type 表(492/394 只计分不切曲);DD2 闪电甲虫 578 勿入 VANILLA_BOSS_IDS 音乐位。
- 补链:鹿角怪召唤物 5120 整链(ZoneSnow 门)、虹萤 661 踩死→光女生成链、天印 3601 Roar+misc[52]。
- 备案:机械自然 roll downed 键名内部不一致(4078 行)/月总合体 AI/lunar 与 Boss 同屏单值近似。

## 2026-08-14 近似转正批(选曲 flag 链/downed 家族键/虹萤门)
- **选曲链 flag 化**(Main.cs:12150-12566 全 1:1):type→num3 槽位(MUSIC_SLOT 全表含入侵/塔/仪式/雪人)→ 各置**独立 flag**(多 Boss 并存非首/末取一,曾 break 首个=近似已废)→ SLOT_MUSIC_CHAIN 24 槽固定序裁决(月总38>Mechdusa25>火星37>塔34>世花24>光女57>猪鲨58>毁灭者92>双子97>Prime98>史王93>邪教徒94>血肉墙12>Boss1兜底5>克脑/雪人13>石巨人17>骷髅王104>蜂后96>史后56>EoW99>鹿角怪90>海盗35>哥布林39>OOA41)。OOA 成员覆写槽12(isOldOnesArmy);Boss1 兜底槽1(578 排除);Mechdusa 覆写槽17。Game.ts 单扫描→resolveEventMusic→pickMusic(eventMusic 单字段)。
- **downed 家族键**:双子 125/126 共写 downed_125(vanilla case 125: case 126: 同写 downedMechBoss2,NPC.cs:80223);mech1=134/mech2=125/mech3=127(曾 125/126/127 顺位错指);自然 roll 门+flag 映射修正;downed_126 旧档兼容读保留。
- **虹萤 661 门**:GetWereThereAnyInteractions(:80616-8025)→ 本体 playerInteraction 位(玩家伤害置位)——接 Enemy.playerInteracted(死因不限玩家击杀,环境死同触发,曾近似为击杀链)。

## 2026-08-14 Mechdusa 合体落地(近似转正第④项)
- `src/entities/mechQueen.ts`:mechQueen 静态登记(registerMechQueen/markMechQueen/mechQueenUp/getMechQueenCenter=Center+(0,-14) :51348),对应 NPC.mechQueen(:6502)+IsMechQueenUp(:6784)。
- 召唤链 `spawnMechQueenEnsemble`(:19739-19748):queen ai3 标记+同点 125/126/134+2×139 探针;`Game.summonMechdusa` 接 5334 剃刀(门=无四机械+mechdusaWorld),公告 misc[107](非 HasAwoken)。
- 双子蛇发锚:`mechQueenAnchor`=GetMechQueenCenter+(-150,-250)×0.75 RotatedBy(queen.vx×0.025);Prime queen 攻相分支(:27135-27291);Enemy :3530 探针 ai0 计 360 门。
- 渲染:127 合体帧 3-5 状态机接活、drawMechdusaHair(蛇头链 Main.cs:25075+)、134 画 136 尾、双子常规链绘制跳过(:22180 门)。
- 测试 bossAI-mechdusa.test.ts 18 条;回归 bossAI 全套+music 71/71 绿。

## Mechdusa 代理终报补遗(接管复核后)
- **再修正一处**:Prime 非合体态悬浮旋转=裸 vx/15(:27803),AngleLerp 阻尼倾转只属 mech 分支(:27797)——早前我把 mech 分支当通用实现,代理已分轴。骷髅王 35 无此问题(其悬浮恒 vx/15)。
- 139 探针引用参数是 **ai2**(第 7 参)非 ai0;合体离场级联=双子 EncourageDespawn(5)→尽→134 Transform(136) 静默消散(bossFled 防误记)。
- 登记缺口(原版有,随各自机制批补):毁灭者身段受击出探针 1/50(mech) vs 1/25(常规,NPC.cs:90266,常规态也未实装)、双子 timeLeft 互保(:26548-26563)、125/139 激光/探针发光叠层(Main.cs:25119-25133)、蛇发链光照着色。
- 终验:bossAI-mechdusa+dd2+summon+music-parity 41/41 绿。

## 2026-08-14 Mech 族缺口全量补齐(目标"缺口全量补齐")
- ①135 受击出探针:Enemy.hurt 内(:90265-90281)——135 身段存活+ai2==0 掷 1/25(Mechdusa 1/50)→ ai2=1+段底 fromVanilla(139)+addEnemy。每段至多一只。
- ②双子互保:twinsAI(:26548-26563)——夜晚 despawnTimer<10 → 借另一眼 despawnTimer-1(DiscourageDespawn=max 抬升,NPC.cs:7237);两只眼离屏同步消散。
- ③发光叠层第五批 NPC_GLOW:125 Eye_Laser(a:1)/139 Probe(cond ai3==0——新增 cond 字段)/131 Bone_Laser(200/255)/134-136 Dest1-3('opacity');XNA Color(...,0)+(One,InvSrcAlpha)=全强度加色,A=0 不参与源贡献。134-136 的 npcColor!=Black 光照门无逐实体光染管线(差异登记,与全 Glow 表同口径)。
- ③ Mech 拖尾:generic 路径 drawNpcGlow 后——125-131 全族+139 自由态+140,oldPos 9→1 间隔 2 共 5 份,α=(10-i)/20,当前帧当前旋转,压本体之上(Enemy.histXAt 历史缓冲)。
- ④蛇发链光照:**compositeLight 全屏合成**(Renderer:1525)已架构级覆盖链段(原版逐链段 GetColor 的近似,注释 :2774 在案)——非缺口,登记解除。
- 测试 tests/mech-gaps.test.ts 5 条 + boss 五套 42/42 + pass-hash/lunar 绿。
