---
name: env-hazards-port
description: 环境接触伤害 1:1(尖刺/岩浆+着火/窒息/灼烧/流血/蛛网)——TouchDamage 表行号/数值/Buff DoT 语义
metadata: 
  node_type: memory
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-11T06:51:25.896Z
---

2026-08-11 移植环境接触伤害全链(用户报:地牢尖刺无伤害/岩浆无着火粒子):

**TouchDamage.ts**(新):TileID.Sets 表(cs:381-389)+ HurtTiles(Collision.cs:3128 盒扩1/半砖下移8/窒息族缩盒2/坡面 num7)+ CanTileHurt(230 仅ftw/80 仙人掌仅饥荒种子→本作恒无效)+ liquidCollision(盒判定)+ stickyTiles(51/229)。数值:**尖刺48=60 木尖刺232=80 荆棘32=10 丛刺69=17 滚球仙人掌484=25 世纪之花刺655=100 尖刺块750=70**;灼烧族{37陨石,58狱石,76,684,230}→Burning 20t(fireWalk 豁免);流血族{48,232,750};窒息族{53,112,116,123,224,234};毁块族{32,69,352,655}。
**ApplyTouchDamage**(Player.cs:28507):伤害全抵消(含无敌帧)时跳过 buff 授予;suffocateDelay<5 递增否则每 tick Suffocation 1t。
**Buffs.ts**:新增 OnFire(24,-4HP/s=lifeRegen-8)/Burning(67,-30HP/s+移速×0.5)/Bleeding(30,仅阻断自然恢复 lifeRegenTime=0)/Suffocation(68,-20HP/s);tick 返回有符号(rateAccum 支持负速率);UI buffBar+图标(torch/meteorite/药水/沙块);l10n 自有键 4 条。
**岩浆**:Player.cs:27350——盒判定;护身符 lavaTime 宽限;**单发 80(吃防御/无敌帧)+OnFire 7s**(旧实现每半秒15是错的);入水熄灭 OnFire(:27426);火粒子(dust6 #FF9A3C 上浮,0.8/tick)。
**Enemy**:NPC.cs:94520——30t 冷却(lavaCd,非 hurt 的 8t iframes!)onFire 7s+50 直伤;onFire DoT 4HP/s 直扣 hp(lifeRegen 路径无防御)+火粒子;死亡走 hurt(9999) 管线。**NPC_LAVA_IMMUNE 表**(data/npcLavaImmune.ts,SetDefaults else-if 链提取 48 种:24老人/59恶魔/60巫毒恶魔/62火小鬼/66蜥蜴人/655 世纪之花等)。
**蛛网 StickyMovement**(Player.cs:22630)已在既有实现覆盖(含蜂蜜块 229/挣断掉落 cobweb)——本轮发现已存在勿重复。
回归:tests/env-hazards.test.ts(表对账/HurtTiles/液体盒/免疫表/窒息族实心);dungeon-spawn 阈值 50→25(生成端 RNG 位移致地牢采样密度 45,池断言全过)。

**Review 补修四项(2026-08-11 二次核对)**:
- Enemy 岩浆冷却是**独立 30t**(immune[255]),不受普通受击 iframes 影响——去掉误加的 iframes 门禁
- 玩家离浆 lavaTime **逐步 +1/tick 恢复**(Player.cs:27405),非立即回满(护身符宽限需等时回充)
- 敌怪入水熄灭 onFire(NPC.cs:94284 TryRemovingWaterPerishableEffects:水湿非岩浆→DelBuff 24)
- waterWalk 装备时岩浆判定缩高 6px(原版 num80)
**Buff 全量审计(2026-08-11 三轮)**:
- 药水时长修正(items.ts,Item.cs case 289-292/301):恢复/敏捷/铁皮/荆棘 **全部 480s(28800t)**——旧值 120-300s 全错;恢复药水 isHealType true→**false**(原版 buff 药水不触发 PotionSickness);desc 文案同步(铁皮 +8 非旧 +6;荆棘全额反伤非"反弹 2")
- Honey 对冲分支补齐(Player.cs:18934:DoT 时 honey 额外 lifeRegen+4 = +2HP/s;rateAccum 加 separate 键分账)
- 新增 7 药水 buff(效果行号):ObsidianSkin(1,360s,lavaImmune+fireWalk+着火免疫:9573)/Gills(4,240s:9656)/ManaRegen(6,480s,≈2.3×:19238)/MagicPower(7,240s,+20%:9669)/Featherfall(8,600s,重力/3+免摔:9671/21367)/WaterWalking(15,600s:9706)/Archery(16,480s,×1.1:9710);Game buffTypeMap+UI 图标(=对应药水)+l10n+stable-id 10494-10500
- **缺失清单(后续轮)**:渲染/光照系 Spelunker(9)/Shine(11)/NightOwl(12)/Hunter(17);刷怪系 Invisibility(10)/Battle(13);机制系 Gravitation(18 重力反转)/Warmth/Tipsy/食物系 Well Fed——待渲染/spawner/食物系统专项

**已知边界(非本轮范围)**:武器/弹幕授予 onFire(火焰箭等)待武器系统;Burning 的原版专属 buff 贴图以近义物品图标近似;lavaRose(黑曜石玫瑰 -45 伤)/灰烬木套装减伤未接(物品未实装)。
