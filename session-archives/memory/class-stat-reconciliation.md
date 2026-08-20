---
name: class-stat-reconciliation
description: 职业数值全对账：minionDamage 独立第四链拆分/魔力眩晕94/投掷并入近战/Rage115 Wrath117 名实对调坑/对账表
metadata: 
  node_type: memory
  type: project
  originSessionId: 4a66e745-9d91-4188-8ade-1e2b7775e8b4
  modified: 2026-08-13T02:57:58.845Z
---

职业数值全对账（2026-08-12，代理提取 Player.cs 全源 + 逐条核对落地，whip6 探针隔离验证）：

**四链拆分**（Player.damageMult 加 'summon' 第四 kind）：minionDamage 独立链 = 1 + SUMMON_GEAR/SET + 四系通用（Wrath 药水 117 伤害/食物三档）；MagicPower/Archery 等 class 来源不进召唤。召唤暴击恒 0（GetWeaponCrit summon=0），鞭 Crit 走 TagCrit——本来就对。

**ID 陷阱（反编译表与 1.4.4 wiki 错位）**：
- **Rage=115（暴击药水，三系+10暴、召唤不吃）/ Wrath=117（伤害药水，四系+10%伤）**——名字反直觉！本仓枚举 `Wrath=39→vanillaBuff115`（效果=暴击）、`Rage=40→vanillaBuff117`（效果=伤害）：效果 1:1 但**枚举名与原版互换**，注释/fallbackName 已标正（怒气=115 暴怒=117）
- ManaSickness=**94**（magic 乘区 ×(1-0.25×剩余/300) 满档 -25% 线性恢复，Player.cs:10003/:25616）；**33 是 Weak**（近战-5.1%伤/速，防-4，移-10%——勿混！我第一版就错按 33 写成近战减益）
- Archery=**16**（arrowDamage ×1.1 非 20%，还有箭速×1.2 未接）
- 本反编译无 Clarity 药水/Ocram；野性咬噬=148 四系+20%；BOC 321=三系+10暴+召唤+10%伤

**落地项**：①魔力眩晕 buff 69（喝蓝手动桥接+魔力花自动都挂 5s/max 合并，l10n 键补在 ../tools/l10n-custom/）②投掷武器并入 melee（1.4.4+ 手里剑 277 melee=true；此前 thrownCombat 裸 damage 无乘区无词缀无穿透——已补）

**对账表确认已正确**：Tipsy(25 近战+10%伤/速+2暴/防-4)、食物三档（四系伤+三系暴+meleeSpeed）、MagicPower(7 magic+20%)、水晶球预见(29)、ranged/magic 无攻速乘区、鞭攻速=summonerWeaponSpeedBonus(311/308/314)+meleeSpeed 耦合+whipUseTimeMultiplier。

**记录未实装（对账清单遗留）**：Shroomite 箭/弹/箭头分道乘区(bowEffectiveDamage 拆分)、磨刀 159 meleeArmorPen+12、Werewolf 28、BOC 321、星云 179-181 四系+15%/层、潜行系（Shroomite/Vortex/Psycho Knife）、Beetle 攻击球、毁灭/复仇者/天界石四系段（accfx 部分覆盖 dmgAll）、Weak 33 减益（敌方施加源）。

**实装批（同日，whip7-class-probe.mjs 八项全绿）**：
① **远程分道**（Player.cs:3820 bowEffectiveDamage 拆分）：`rangedDamageMult('arrow'|'bullet'|'rocket'|'other')`——箭=(rangedDamage+箭袋stack)×Archery×蘑菇矿箭头1.12×潜行；弹/火箭=base×对应蘑菇矿头1.12。弓族按 `bowC.useAmmo`(40箭/97弹/771火箭/283镖) 分类。**箭袋 arrowDmg 从 dmgRanged 拆出（原来误伤枪械）**。蘑菇矿头 1546/1547/1548 还给远程暴+5。
② **磨刀 159**：BuffType 24 已在册，效果新接——`player.meleeArmorPen`（仅近战挥击+投掷路径加，召唤/鞭不吃）；磨刀站 tile=**377**（3198 是物品！）就近 60t 扫描常驻。
③ **狼人 28**（BuffType 71）：月亮符 485 accfx{nightWolf}+夜间 → 近战+5.1%伤/+2暴/×1.051速。★Clock.isDay 是派生 getter（timeOfDay 0.25-0.75），探针只能改 timeOfDay。
④ **BOC 321**（BuffType 72）：混乱之脑 3223 accfx，受击 1/6 → **bocPulse 延迟脉冲**（damage() 无 game 参）→ fixedUpdate 消费：三系暴+10+召唤伤+10%+困惑近敌 300px。
⑤ **星云**：套装 2760/2761/2762，耗魔 15% 叠层≤3（近似原版击杀掉 booster），每层四系+15%，8s 全层刷新。
⑥ **甲虫进攻套** 2199+2200+2202：近战命中 45 次/球 ≤3 球，每球近战+10%伤/速；受击掉球。
⑦ **潜行**：蘑菇矿全套/星璇全套+按住↓静立蓄 1/60t——远程伤×(1+(1-stealth)×0.6/0.8)、暴+10/20×(1-stealth)；探针实测满潜行箭伤×1.6。
⑧ **Weak 33**（BuffType 73）：狼人敌 155 命中施加 30s（damagePlayer attacker 钩子）——近战-5.1%伤/速、防-4、移-10%。

**坑**：l10n 键加在 `../tools/l10n-custom/` 后必须手动 `node scripts/build-l10n.mjs`（vite 自动重建不触发审计缓存）；BuffType.Sharpened=24 已存在勿重复注册。

**Review 批修正（同日二审）**：①弓公式精确化——bowEffectiveDamage :3820 = (rangedDamage + stack×arrowMult)×arrowMult（stack 段吃 arrowMult²，首版漏平方）；②**潜行机制首版写反**——蘑菇矿=**移动**蓄 (|vx|+|vy|)×0.0075/t、静止散 0.015/t、攻击暂停（无按↓！）；星璇=**双击↓开关**（15t 窗口自实现 downTapT）开时 stealth 满起每 t -0.04 且**移速×0.3**（:25563）。③Clock.isDay 是派生 getter 探针只能改 timeOfDay。

**Review 后仍留（有意/低价值）**：Archery 箭速×1.2、箭袋箭速/击退×1.1 与熔箭袋木箭→火矢+2（quiver accfx 占位未消费）、潜行 aggro 降低（-750/-1200 需 spawner 联动）、甲虫壳 2201 防御版、变态刀 3106 单件潜行、狼人视觉变身、星云=耗魔近似（原版击杀掉 booster）、甲虫=命中计数近似（原版时间蓄能）。

**专项清单进度2（08-13 续3）**：悠悠球 lerp 已被并行会话完整落地（msRange 缩放/inertia num7/deadZone num9/flag3 超程/flag4 1.3× 强收/回收态 ×0.8 惯性——全 1:1 销项）；**连枷 case 3 垂链态**（:41288-41330 1:1）已插：持按悬垂（超链长段 ×0.98 朝手 MoveTowards(14,1)、链内近停段 X×0.96/Y+0.2/玩家静止再 ×0.96）、松手→回收、进入口=回拉态再按改 st=3。剩余：配重球环绕（Pr:64472-64516）、Molotov 爆裂、狙击镜 zoom、单品省弹表。

**击退管线完整版（08-13 续2）**：`kby===0`=武器路径信号——hurt 内走原版应用语义（N:82204-82236：X 朝 ±num3 收敛设置=同向不足才推/反向×2步/钳目标；Y=-num3×0.75×resist 且若 vy 已更低则不动=原版"只上抛不压制"）；kby≠0=爆炸/光环加法（登记）。**0.65 自造系数全摘**（近战挥击/WeaponProj 四族/随从 ×0.5 亦摘）→ 四调用点改裸 kb+kby=0（glove×2/Titan×1.5 保留=真原版 P:52477；minionKB 加法保留）。Arrow 本就裸 kb+kby=0 自动进入原版路径。构建绿+单测4/4。

**专项清单落地（08-13 续）**：**击退五段软封顶管线**（N:82144-82236 1:1：>8/10/12/14 段 ×0.9/0.8/0.7/0.6、钳 16、地狱火 onFireT 代 ×1.1、暴击×1.4（hurt 加第 6 参 crit，Arrow/WeaponProj/近战挥击三热路径传入）、小丑 185×1.5）已进 Enemy.hurt。**遗留**：调用侧 0.65 自造系数待清扫（清扫后管线即完整 num3 语义）；悠悠球 lerp/连枷垂链/配重球环绕/Molotov/狙击镜/省弹表待批。

**全接入收尾批（08-13）**：审计残留四项全接——①词缀**tagdmg**（I:567 bonusTagDmg：WhipProj.bonusTagDmg 字段+Game 注入+命中并进 whipTagDmg）②词缀**size**（P:46431 num13=shootSpeed×scale：矛 ctor spd 乘 ps.size）③**击退抗性方向修正**（N:82144 vx=num3×dir×resist——resist 是"接受比例"非"抵抗比例"，曾 (1-resist) 反向致 Boss 被推飞）④**MagicProj 暴击**（P:52512——曾恒 false）。构建绿+单测4/4。**仍登记未接**（需专项）：击退软封顶五段+crit×1.4（N:82144-82239 全段移植）、悠悠球 lerp 追踪曲线（Pr:65071）、连枷 case 3 垂链态（Pr:41288）、配重球环绕（Pr:64472）、Molotov 爆裂、狙击镜 zoom、单品省弹表。

**全流派武器审计批完结（08-13，任务#72 13/13）**：投掷乘区ranged(42/279/287非277矛)/Arrow暴击链(critBonus三spawn注入系crit+item.crit+词缀crt)/近战reuseSpd裸useTime/弹药过玩家乘区/霰弹多弹丸(534 rand4-5/964 rand3-4/4703 8发)/悠悠球三型号表(射程130-400顶速9-17.5寿命LT×60/(1+meleeSpeed)/2)/剑族弹速÷meleeSpeed/autoReuse全kind门(maneed click edge)/manaCost截断/回旋镖(BOOMERANG_RETURN+命中盒20型表22-46px)/**armorPen减防语义全路径**(Enemy.hurt第5参 min(pen,def),N:81913——曾加伤害上2倍过强;摘6处加算→Arrow/WeaponProj四族/grenade explodeAt/鞭:12068/随从/挥击全hit时传参)/**武器词缀10乘区**(crt四链/mcst=round接CheckMana/shtspd+spd在wrapper出口统一折算/arpen并入全部pen注入点;size纯视觉未接)/矛SPEAR_PARAMS(并行会话已1:1)。**协作坑**：并行会话会写回覆盖我的编辑(投掷修复被覆盖一次,重套加固注释)；我加的SPEAR_OFF与并行SPEAR_PARAMS撞车=立即删重复。

**终审补接（08-13）**：minionKB 半接线已补——MinionProj.contact 击退处 `+ equipStats.minionKB`（:52477-52482）；node 单测（tests/minion-kb.test.ts：0/2/4 三档）通过。★WhipProj 内联鞭表已被并行会话重构收敛进 `src/entities/WhipTag.ts` 单源（TagEffectState 全状态机），无死代码双源。E2E 环境注记：并行会话 WorldGen worker 现报 `SOLID_LUT is not defined`（他们的重构回归，世界生不出→页面无限重载→探针 nav-destroyed），浏览器 E2E 须待其修复。

**清零批完结（08-13，19/19 全清）**：Archery 箭速/箭袋速击/熔箭袋/甲虫壳/变态刀/狼人视觉(38/21/20槽位)/DD2音效(素材在Sounds/Custom!)/Foxparks喷火/床睡(脚侧判定,受伤不醒,全员睡熟×5)/**星云booster全链**(魔法命中1/3非击杀!CD30+物品实体3453-55抓取42吸附12+Levelup逐级cap3/480t+逐级衰减)/**⑫-2 aggro消费端**(Enemy.seekDirX中央不转身门 NC:78447-78452——单人下TargetClosest多玩家选距退化,此门即全部消费位;四态探针绿)全部落地。**探针三坑**：①updateUse头部门禁`uiBlocking||dead||fullMap.open||timeUiHover||weatherUiHover`(Game.ts:3518)——fullMap.open全库无=true写点但HMR分叉会怪态为真,探针须每帧强关;②靶60ms钉靶间隔会坠落脱靶(flaky根因),要16ms;③vi_64紫杖射线=屏幕角非世界角,靶须放玩家同行。

相关：[[summoner-full-parity-batch]]
