---
name: item-audit-port
description: 道具功能全量审计管线+vi_工具/药水桥接——清单表生成脚本、逐类覆盖判定、引擎级缺口清单
metadata: 
  node_type: memory
  type: project
  originSessionId: d6caec24-1cc3-4182-bea5-29046ee459cf
  modified: 2026-08-11T11:24:55.251Z
---

# 道具功能全量审计（2026-08-11，用户令"导清单→逐项核对→复验打勾"）

**管线**（可复跑）：①`tools/extract-itemfunc.mjs` → `src/data/vanilla-itemfunc.json` **2141 件功能画像**（Item.cs SetDefaults1-5 最近一层 switch(type) 归属扫描；字段=melee/ranged/magic/summon/pick/axe/hammer/createTile/createWall/healLife/healMana/buffType/buffTime/ammo/shoot/holdStyle/torch 等）。②`scripts/item-audit.ts`（vite-node 跑，导 src 数据）→ **`docs/item-audit.md` 清单表**（逐项 id/名称/状态/备注+分类汇总）。

**审计终态（打勾基线）**：工具 95✅ / 放置物 1038✅（place_v_ 全量自动生成=tile def 存在即覆盖）/ 铺墙 124✅（wallitems 循环补 wallId，**审计坑：墙物品是 snake_case 第二注册键 vi_26_stone_wall ≠ vanilla.json PascalCase 键 vi_26_StoneWall——查 wallId 集合而非按 key 反查**）/ 治疗魔力药 16✅ / Buff 药水 13✅ 97⚠️ / 武器 442✅ / 盔甲配饰 870✅ / 杂项装备 274✅ / 火把 ✅ / 材料 3125✅ / **召唤武器 31❌（召唤物系统未移植）**。

**vi_ 桥接（本轮修复三件）**：①**工具**（60 件 vi_ 镐/斧/锤此前不挖矿！）——`Game.itemFuncTool(id)`：vi_ key 反解 vid → itemfunc pick/axe/hammer → tool def（power=原值/damage·useTime·kb 取 combat 表），updateUse:1961 + updateSwingHits + 挥速三处 `def.tool ?? itemFuncTool`；双工具 Hamaxe 取主类型。②**药水/食物**——updateUse 新 vi_ consumable 分支（门=consumable 且无 createTile/shoot/工具）：healLife 治疗+耐药 60s、healMana 回魔、buffType→BuffType 经 **BUFF_DEFS.vanillaBuff 反查**（用户同日已扩 8 个新 Buff：ObsidianSkin=1/Gills=4/ManaRegen=6/MagicPower=7/Featherfall=8/WaterWalking=15/Archery=16/NightOwl=12，编号与原版一致）、buffTime tick→秒 /60（铁皮药水 28800t=480s ✓）、buffType 21（耐药）不主动施加。③审计器判定规则同步（桥接即 ✅）。

**测试**：tests/item-bridge.test.ts 7 条（画像数值/Buff 反查链/派生公式）。**坑**：Buff 药水 id 易猜错（铁皮药水=292 非 1161；TEdit key IronskinPotion 反查为准）；Chrome 拉不起时（launch unsettled await）浏览器冒烟降级为单测+审计复跑。

**引擎级缺口（97⚠️+31❌）**：召唤武器 31 件（需召唤物 AI/跟随/伤害系统）；Buff 97 种未实现（食物 WellFed/锻造/战斗/钓鱼等小众 Buff——逐个要 BuffState 扩展）；审计后新增功能类时记得扩 extract-itemfunc 字段表。

**R1-R3 执行（2026-08-11 晚，按 ~/.claude/plans/magical-cooking-squid.md 迭代计划）**：审计 Buff 药水 13✅→**40✅/70⚠️**。**R1 数值批**（13 Buff）：Lifeforce113(maxHp+20% floor(base/5/20)*20)/Endurance114(受伤×0.9 在 damage 内乘)/Wrath115(全系暴+10)/Rage117(全系伤+10)/Tipsy25(近战伤+10%暴+2速×1.1防-4)/Titan108(**近战击退×1.5 非 减伤——kbBuff :20812 勘误**)/AmmoReservation112/Mining104(冷却×0.75)/Builder107(放置铺墙射程+1)/Heartreach105(heartGrabBonus+60 ItemDrop 心分支)/FlipperPotion109/Battle13+Calming106（**Spawner 钳制 maxSpawns≤15 作用在战斗药水加成后**——测试断言要 min(15,...)）。**R2 浸剂**（9 Buff）：8 药剂经 BUFF_BY_VANILLA 反查→近战命中 updateSwingHits 施加敌 debuff（venom30/cursed24/poison6 HP/s onFire 同构滴血、ichor hurt 内 def-15、midas rollCoins 第 4 参 ×1.10-1.51、nano confused 每秒翻 vx 近似、party 彩带）+Inferno116 光环（200px 每 60t 20 伤+灼烧 2s+heldLight 0.65/0.4/0.1）。**R3 视觉批**（5 Buff）：Shine11 heldLight 1.3 常亮；Spelunker9/Dangersense111/BiomeSight343=Renderer.drawBuffHighlights 全屏 tile 扫描叠层（TILE_DEFS key 启发式集合/呼吸 alpha）；Hunter17 登记未画框；counterWeight=yoyo spawnWeight 回调落 556+ 配重弹；desertBoots=zoneDesert 每帧同步+0.25 移速。**教训**：①updateWeather 作用域无 p 变量——狱火块写 p.* 运行时崩（stale dist 报 ReferenceError），加块前查作用域变量；②User WIP 智能光标 7 键没进 l10n-custom 时我方 vitest l10n-audit 门会拦全量测试（占位键先补）；③Enemy ctor 签名 (key,x,y)。

**R4-R5 执行（2026-08-11 深夜）**：**R4 魔力星+套装**：accfx 加 manaMagnet/magicCuffs/manaFlower；魔力星吸附（Player.manaMagnetBonus+80 → ItemDrop star 分支，Player.cs:34495 专属通道）；魔力手铐=受伤回蓝 raw 1:1（:37678）；魔力花=耗魔×0.92+不足自动喝蓝（Game.tryAutoManaPotion 扫 vi_ healMana，**switch case 内 break 跨函数编译错→改 if(mana>=cost) 结构**）；**盔甲套装加成** `vanillaArmorSets.ts`：键=`hs|bs|ls` **槽序号非物品 id**（提取器存 slot 数值；铁=2|2|2/熔岩=9|9|9/**铜=1|1|1——1.4.5 木套迁至 52|32|31 且木无套装加成**）；肉前 14 条+通配 `h|b|*` 兜底；equipStats.setBonus/manaCostMul 接入（丛林 0.84 两魔法门）。**R5 幸运**：Player.luck（clamp[-0.7,1]，药水 257 三档 buffTime>600s=3 ×0.1——AddBuff max=续高档，测试分实例）；NpcDropCtx.luck → rollLuck 双层掷骰（Luck.cs:6）+ rollCoins |luck| 重掷（:80414）。测试 equip-r4 7+luck-r5 2；全量 75/76（仅用户洞穴 oracle）；build ✓。剩 R6 召唤物 31 件/R7 钓鱼+重力。

**R6 召唤系统（2026-08-12）✅ 31/31——道具功能审计 6059 件 ❌ 归零**：①combatWeapon 加 kind:'summon'（哨兵分流=投射物 aiStyle 53/54/123 共 6 件；其余 25 随从）。②实体 MinionProj：飞行=环形槽位悬停→锁敌≤700px 俯冲→>1300px 瞬移回收；地面形参已留暂统一飞行；哨兵=定点 60t 一发 Arrow+10 分钟；接触伤害同敌 20t 冷却吃 damageMult('magic')；贴图 projSprite 懒加载。③上限链（maxMinions :9855）：随从=1+附魔台+召唤药水 110（新 BuffType.Summoning），超限驱逐最旧；哨兵独立 cap=1。④★Game.useItem 通用分支陷阱："其它物品"（!heldDef.tool）在 cw 分发之前——召唤法杖被它吞掉，gate 补 cw?.kind!=='summon' 才落 useCombatWeapon case。⑤测试 summon-r6 4 条；全量 76/77（仅用户洞穴 oracle）；build 被用户并行 WIP 挡住（Sfx.ts 语法错+Game.ts 'sh' 未定义）。调试：召唤链"0 只"假阴性=上限驱逐净计数不变，用 delta 或先清场。R7 钓鱼+重力未做。

****总体 review（2026-08-12，用户令"总体 review 确认真校对了"）**：Explore 代理对七轮 12 项核心数值回 C# 源码逐条核验——9 一致 / 2 近似 / 1 真 bug，全部当场修：①**midas off-by-one**（rng.int(10,51)=Next(10,52)≠原版 Next(10,51)=[10,50] → int(10,50)；RNG 约定 int(a,b)=Next(a,b+1)）②**ichor 语义纠正**：非"防御-15"，是 NPC.checkArmorPenetration（NPC.cs:81913）armorPenetration+=15 折半=+7 直伤+超防钳制（旧注释引 :92096 是染色代码）③spawner 链序 calmed→sunflower→battle→蜡烛（整数截断 ±1）④丛林套补齐 8 种槽序组合+删 ShadowScale 虚构数值（C# 只置旗标）⑤审计分类修：Buff 药水门加 consumable&&!summon——62⚠️ 实为 59 件宠物/召唤武器（buffType 是随从 buff）误入，真缺口仅 3 件（隐身10/保暖124/火把神376）→ **48✅/3⚠️**。终态：tsc 0 错、build ✓、全量 77/80（3 失败=用户 JunglePass 在途：oracle×2+草稿_jt；dungeon-spawn 计数 45→12 漂移系其 RNG 位移，测试注释已预告该语义）。**RNG off-by-one 高危区：rng.int(a,b)=Next(a,b+1)——凡对照 Next(a,b) 必须 int(a,b-1)，midas 是首例实锤**。

**R7（2026-08-12）✅ 迭代计划七轮全部完成****：**钓鱼**：extract-itemfunc 加 fishingPole/bait（**9 支竿中 2291-2296 族在 case 段外区间块——最近 switch 归属扫不到，输出端补丁表**：2291:15/2293:20/2292:30/2295:35/2296:40/2294:50）；鱼饵 29 种。`vanillaFishing.ts` 渔获池（液体优先 lava/honey > 海洋 > 群系 corrupt/crimson/hallow/jungle/snow > 深度 surface/cavern；id 全 l10n 实名核对）+ rollCatch（crate 10%+药水/垃圾 35%-power×0.4%）。`Bobber.ts` 状态机：抛物线→落水漂浮→等待(300-210 缩 power)→咬钩 60t 窗口→收竿 rollCatch+掉落；**错过窗口重置等待 90-210t**（否则 --waitT<=0 每帧连咬——测试抓到）；鱼饵消耗 1/(1+bait/6)（钓具箱 +1 分母 ：51640）；岩浆需熔线钓钩（equipStats.lavaFishing 未提取→浮标烧毁）。Game.useItem 端：fishingPole>0 分支（有浮标=收竿/无=抛竿+扫鱼饵）。三药水 BuffType：Fishing121(+15)/Sonar122(预展示待接画字)/Crate123(+10%箱率)。**重力**：Player.gravDir(1|-1)——重力/跳跃/松键截断/摔伤起点四点镜像（:3207 vy×gravDir）；倒置 onGround=hitHead（天花板当地板，TileCollision 已有该旗）；Game Up 键边沿切换（gravLatch）+BuffType.Gravitation(18)；**渲染翻转未做**（纸娃娃/动画镜像待后续）。测试 fishing-r7 6 条（数据/池/状态机两段/空竿）；全量 77/78（仅用户洞穴 oracle）；**build 被用户新 WIP bossAI_martian 挡住（3 错）**。

关联 [[vanilla-ui-port]] [[vanilla-npc-port]]

**R8(2026-08-12)提取器双缺口:链锤射锤根因**:用户报"链锤(Mace 5011)射出一把锤子"。
链路:projectile 947/948 **不在 vanilla-projectiles.json** → 分类器 ai=-1 → 落 shot 直射兜底
(原版 useStyle5+channel 连枷 aiStyle15)。根因=extract-projectiles.mjs 只认单值/区间条件,
**复合 OR 条件 `type == 947 || type == 948`(共用 DefaultToFlail 块)整块漏提**——修后
934→1029 条(补 95,含 167-171/723-752/940-965 等空档)。同轮第二缺口:extract-itemcombat.mjs
不认**嵌套 `if (type == K)` 单守卫覆盖**(5012 组共享 shoot=947,内层 if 覆盖 948)——修后
5012 shoot→948、3021 shootSpeed 15→16(源 :27955)。经验:1456 SetDefaults 三种惯用法=
单值/区间/**复合 OR** + 共享体/**嵌套 switch(type)**/**嵌套 if(type==K)** 覆盖,提取器全要认;
"武器行为像发射器"优先查 projectileData(shoot) 是否 undefined。回归 tests/mace-flail.test.ts。

**R8 续:同类错配全面 review(2026-08-12)**:通配化 extract-projectiles 条件解析——
平衡括号取条件+纯 type 布尔式逐 id Function 求值,【顶层 else-if 链先匹配者生效】+
块内嵌套纯 type if 递归求值(裸 else 分支行泄漏靠 find 首现顺序无害)。覆盖
单值/区间/复合 OR/括号混排(`(type>=360&&type<=366)||type==381||type==760`),
934→**1105 条**,再补 76(含嵌套分支 width/height,76-78 三分支验证)。审计结论:
shoot 目标缺失=0;**aiStyle13 锚定链族(鱼叉160/Golem拳1297/KO加农1314/链刀1325/
链斩3012)曾落入 shot=子弹射飞,已归 spear 前刺族**(AI_ANCHORED=13 常量);
钻头/电锯 shot 分类是死代码(itemfunc pick/axe 力在,挖掘路径先拦截);已知缺口
不修:aiStyle7 抓钩 28 件/aiStyle26+67+90+124 宠物约 30 件/aiStyle75 特殊件
(Arkhalis 冲刺剑/SolarEruption/PortalGun)=系统未移植;items.ts 3 个同键重复
(122/217/1507,生成器冗余,无害)。普查 tests/weapon-census.test.ts(归族分布断言)。
