---
name: npc-ambient-sound-audit
description: 怪物音效全量审计:HitSound/DeathSound已数据驱动;AI内嵌周期音缺口大(idle表32类/小动物/critter/闲话表全缺);蠕虫roar已修
metadata: 
  node_type: memory
  type: project
  originSessionId: 1fc2b821-952a-4ed1-9b75-6e99198205af
  modified: 2026-08-18T11:42:55.814Z
---

2026-08-18 用户报"地狱骨龙(骨蛇39)接近有音效"——**骨蛇掘地音 = AI_006 :52375-52395
周期性 SoundID 15 Roar**(间隔=玩家格距/40 钳10-20,排除 621/87/117/454/412)。

**修复**:eowAI 分支(13-15)原已有(曾误播 dig 近似→改 eowDig 真轨,
Sfx.ts 加 'eowDig' → eow_dig.wav);**通用 wormAI(39 等)整段缺失**——
在朝向段前补 1:1 周期 roar。测试 tests/worm-roar-sound.test.ts 3 条
(39 roar≥3次/EoW 13 eowDig 双段链/排除表 412 静默)。EoW 断链自查
(:51886 头无下段即灭)=原版语义,测试须手工 wormNext/wormFollow 建链。

**全量审计要点**(232 处 PlaySound 归类):
- HitSound/DeathSound = 数据驱动已全(vanilla-npcs.json 字段→wav 组)
- AI 内嵌**周期/事件音**是缺口重灾区:AI_003 闲话表(:57731 僵尸14/木乃伊26/
  吸血鬼29,7 等 1/N 掷骰)、IdleSounds 表(:91119 32 类环境声)、
  小动物声(:93415 鸭蛙鸟鸥枭)、AI_005 黄蜂 Item17、AI_009 秃鹫(4,9)、
  AI_103 沙鲨(15,4)+(14,542)、宠物受击表(:82259 15 款 player_hit_*)
- 佛系验尸法:grep 'PlaySound' NPC.cs 剔 HitSound/DeathSound 后按 AI 函数归属归类

**全量落地批(2026-08-18 用户令"全部做掉")**:
- 新建 `src/data/vanillaNpcAmbience.ts` 三表(IdleSounds 47条/CHATTER 47type/CRITTER 23type 全量转录)
- Enemy.ambientSoundTick(fixedUpdate 尾):critter 段互斥 else-if 链 1:1;闲话仅 aiStyle3;
  IdleSounds wet 门查液体格;Game.playSfxWav→Sfx.playWavFile 直 wav(FILE_CASE_VOL 自带音量档)
- GameHooks.playSfxWav 可选(?.)=测试 mock 兼容(6 个 mock 无此键的旧测试零改)
- 事件音 12 落点:黄蜂 Item17(ai1==101 清零帧)/猪龙 Zombie_9 1/1000(floatEyeAI 头)/
  秃鹫沙球 ai0==200 Item5+弹31(AI_017 :24475-24506 曾整段缺失,顺带补攻击本体)/
  沙鲨 Roar_1 游弋+Zombie_7 出沙(bossAI_dd2)/蚁狮 Item_5/怒滚虫546 NPC_Hit_11 追击跳
  (chargerAI 整段补)/海豚 Zombie_109(ai3 计数器整段补 :23726-23741)/小精灵 Pixie 1/40/
  幽灵316 NPC_Killed_55/水蛭117 NPC_Killed_13+20尘(_wormSpawnFx 哨兵)/幻影龙454 Item_119/
  仙灵三处 roar 近似→Pixie 真轨(状态3@15t/状态5@15t/召唤脉冲1/30)/
  火星骑手 Item_39(438弹)+部件 Item_12(449激光)/星云脑消散 menuOpen→Item_8(审计#22 错音)
- 自制僵尸呻吟退役(Game.ts 只认 legacy key 全不命中,被 1:1 表取代)
- 测试 tests/npc-ambience-sounds.test.ts 6 条:三表锚点+wav 全在库(fs 直查防键拼错)+
  水蛭/幻影龙出生音触发;33 测试绿,tsc 0
- ~~遗留 6 项~~ → 子代理"补齐 6 项音效缺口"全落地(2026-08-18 续):
  宠物语音表(vanillaNpcAmbience:143-167+projTargets/GGame 接线)/TransformVisuals
  (Enemy.tryTransformTo 加 game 参,:81742-81749 gore99 三锚点核对✓)/老人自灭咆哮
  (Game.ts Roar_0,考古=骷髅王后 ai3==1 自灭非微光)/229 微光变体死亡 NPC_Killed_6/
  378 牙齿炸弹状态机(:30082/:30204 结构核对✓)/水花分液体 splashWavFile(顺带修
  honeyWet/shimmerWet 覆写 bug)

**★Roar 键误轨大修(2026-08-18 用户报"地底蠕虫音全变 boss 唤醒咆哮")**:
- 根因三连:①WAV_MAP['roar']=['Roar_0','Roar_1'] 随机双轨——原版 boss 吼=PlaySound
  (15,x,y,**0**)=Roar_0(NPC.cs 16 处全显式 style0),蠕虫掘地=PlaySound(15,x,y)
  无 style=**Roar_1**(LegacySoundPlayer :366 签名 **Style=1 缺省**!)——一半概率播
  2 秒 boss 巨吼;②FILE_CASE_VOL['Roar_1']=0.25 是 case15 style4(沙鲨)调用点专属
  误登成文件档→真蠕虫轨被压 1/4 几不可闻;③缺 case15 **单实例互斥**(:825-841
  State==Playing 跳过)→多蠕虫 10-20t/tick 满响叠成音墙
- 修:WAV_MAP['roar']=['Roar_0'];wormAI(Enemy.ts:416)/destroyerAI(bossAI.ts,
  :50459-50473 补齐——原 AI_037 段缺掘地音)→playSfxWav('Roar_1',1);沙鲨游弋
  显式 0.25;Sfx 加 SINGLE_INSTANCE{Roar_0,Roar_1}互斥(onended 清槽,分槽独立)
- ★单实例语义全表(LegacySoundPlayer):case15 Roar=播着跳过/ case3 NPC_Hit=
  **Stop-重播**(未移植,连击打断重播语义)/ case4 NPC_Killed=每次都播(仅 style10
  互斥)/ case14·26·29 僵尸族=每次都播——勿一刀切互斥!
- ★PlaySound 签名陷阱:第 4 参 Style **缺省 1 不是 0/−1**——所有无 style 调用都是
  变体 1(Roar_1/Zombie_1 等),对轨时必须先查缺省值
- 连带蝙蝠死亡音疑案(用户报"洞穴蝙蝠死亡没声"):hurt→killedSound 链路进程内
  复现正常(NPC_Killed_4 播出);真根因=①蠕虫音墙掩盖 ②首播懒加载静默(NPC_Killed_4
  未缓存→playWavFile false→Game.playSfxFiles 回退 hit 合成音=死亡音"消失",第二只
  起才响)——修=怪池 Hit/Death wav 进世界定向预热(Game.ts preload 块 VANILLA_
  SPAWN_POOLS 全池)
- worm-roar 测试更新:骨蛇断言 Roar_1 非 roar 键+单实例互斥四断言(stub window
  AudioContext 喂 buffer 法,vi.stubGlobal 可测 Sfx 全链)

**★roar 全调用点对齐批(2026-08-18 子代理穷尽对账,54 测试绿)**:
- SoundID.Roar 是 const int 15 非音轨对象,全树零 WithVolume;case36 ForceRoar
  style0=Roar_0/style-1=Roar_0+pitch0.6/缺省1=Roar_1;所有 case-15 调用零第 5 参
- 音量错档 6 处全改满响+坐标:双子变身(bossAI 0.7)/Prime 白天(0.8)/Prime 旋冲
  (0.6)/石巨人头自由(0.8)/EoC 冲刺预备(0.7)/EoC 连冲(0.7→playSfxWav
  'Roar_0'+pitch0.6,GameHooks.playSfxWav 补第 5 参 pitch)
- 漏吼 2 处补:骷髅王 35 旋冲 ai[2]==2(:22155)/魔眼 126 二阶段冲刺启动帧
  (:27674,雷眼无;twinsAI ai1===1 的 spaz 分支——注意 ai1===1 在 ai0===0 与
  ai0===3 两处各有分支,别放错宿主!)
- 借轨 10 处改直文件:duke 7 处+大龙卷→Zombie_20/小龙卷 Zombie_9/月总核心
  Zombie_92(×0.5 自动)/幻影矢前摇×2→NPC_Hit_6(PlaySound 4,6)/月总眼
  Zombie_100(:38227 Next(100,101)=恒100!)/幻龙 Zombie_102(×0.4 自动)/
  教徒显形 Zombie_89(×0.7 自动)/光女 Item_163/160/史后落地 Item_167/
  石巨人落地+冲拳 Item_14
- 自加音 9 处删(原版零声):教徒冰雾/闪电/仪式圈/火球、史后蓄冲/凝胶环、
  石巨人本体死吼+自由头死吼(头自由 :32587 一声保留满响)、月总头死光、
  四塔破盾、火山拉杆(Wiring.cs:1697-1741 仅动画)
- 遗留登记:魔眼二阶段冲 14+专家2.5 速(我们 13)速度档缺口与吼无关,另行修
- ★顺修:音效批新增的 game.playSfxFiles 非可选调用炸旧 mock(蚁狮 69 测试
  "playSfxFiles is not a function")——Enemy.ts 16 处+martian 2 处统一 `?.`;
  铁律:GameHooks 上的音效新调用一律可选链(旧 mock 不含键)

**★终审清零批(2026-08-18 review 抓出)**:
- case36 ForceRoar 是**覆盖槽**语义(直接 CreateInstance,旧实例 _trackedInstances
  续播)=每次都播——case15 互斥会误吞 EoC 连冲高频吼!修=playWavFile 第 6 参
  replace(豁免互斥+槽位换绑,旧 onended 因 identity 检查不误删);EoC 冲刺预备
  (style0)/连冲(style-1+pitch0.6)两处传 true。★四 case 语义全表:15=播着跳过/
  3=Stop-重播/4·14·26·29=每次都播/36=覆盖+续播
- EoC 段一→段二变身(:20329)/FTW 重启(:20685)补坐标(原版带坐标衰减,曾无参)
- 史后蓄冲死变量清理(prev 只剩空块消费→整段删净)

**★遗留清零批(2026-08-18 用户令"全部对齐",音效台账归零)**:
- ★BellHurt 5484 真相:=LegacySoundStyle(2,**35**)→**Item_35.wav**(case2 音库,
  ×0.75 自动档)——"素材缺"是当年 wav 名想成 Player_Hit_35 的误判,文件一直在!
  PET 表补齐全 14 键零缺;★全表 WithPitchVariance(0.4)=调用方掷 ±0.4 音高
  (Game 近战+projTargets 两处直调点带 pitch 参)
- 城镇宠物 637/638/656 json 补 HitSound/DeathSound(提取器漏;637/656 死音
  NPCDeath6、638 NPCDeath1);TownNPC 受击/死亡音硬编码(NPC_Hit_1×0.6/
  NPC_Killed_1×0.8)→vanillaSoundFiles 数据驱动+满响(原版 StrikeNPC/checkDead
  无音量参=1);229 微光变体特判保留
- 双子二阶段行为对齐:魔眼冲刺 14→expert **16.5**(:27674 段仅 expert 无 FTW)/
  减速计时 expert **×1.5**(:27696-27700);雷眼自造"侧移 seek8+射击180t"整段
  替换为原版**直冲 12/expert15/getGood+2**(:26746-26763;雷眼减速无 expert=一致);
  雷眼变身完成双声 NPCHit1+Roar(:26844——魔眼 :27478 只吼无前置声,双门分流)
