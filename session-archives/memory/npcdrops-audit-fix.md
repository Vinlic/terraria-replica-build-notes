---
name: npcdrops-audit-fix
description: 掉落系统1:1审计修复——slimeBody堆叠case提取器bug/初速度vy差0.1/心星luck/雕像AnyInteractions；钱币乘子链·bossBag族·value表·EoC规则逐项核对通过
metadata: 
  node_type: memory
  type: project
  originSessionId: c44574b3-7d4d-403b-8e39-61a13d11a1c6
  modified: 2026-08-13T06:52:06.260Z
---

掉落系统 1:1 审计（2026-08-13，/goal 检查所有掉落）。[[vanilla-npc-drops-port]] 续。

**审计方法**：①提取器重跑对账（0 漂移 = 表与当前源码一致）；②棘手规则抽样逐项对 C#（EoC 12 条/trophies/双矿/晶状体全对）；③管线逐行对源码。

**修复 4 处**：
1. ★ **slimeBody 提取器堆叠 case bug**：`case (\d+):` 逐 case 切段把多 case 分组成员丢了（只留组内最后一个 case，如 3-13 组只存 3347）——改 token 流前向合并（连续 case 归组、组内首个 min/max 归属全组），10→**44 键全组 1:1**（vs SlimeBodyItemDropRule.cs:39-115 逐组核对）。
2. **掉落初速度**：vy 原 [-40,-15]（差 0.1，原版 `Next(-40,-15)`=[-40,-16]）；补 859/4743 恒零速、520/521/NebulaPickup{3453-3455} 双向 Next(-30,31)（Item.cs:49328-49337）；dropVelocity 加 id 参。
3. **心/星 luck**：RollLuck(6/2) 原为裸随机（丢幸运双掷语义）→ 换 rollLuck(ctx,denom,1)（:80334/:80345）。
4. **雕像门 AnyInteractions**：:79651 `rand>=rarity || !AnyInteractions()`——补 Enemy.playerInteracted（hurt fromPlayer 生效置位，:5802 fromPlayer 块），rarity 掷中还需玩家曾交互（岩浆/陷阱杀的雕像怪不出）。

**核对通过（零修改）**：
- 钱币管线：8 层乘子链逐项（midas Next(10,51)/基线 Next(-20,76)/1-2-4-8-16-32-64 层/bloodMoon Next(101)）+ luck 双掷取极值 + 贪心拆币（:80412-80540）✓
- 心星（:80332-80348 门/顺序 ✓）、Boss 药水分支表 13 项全对（:79746-79803）+ 獾帽 5004 已在 Game 层接（EoC+WoF 同日双杀，:79804-79815）✓
- 雕像门数据：STATUE_NO_EARLYMODE_LOOT{480,82,86,170,180,171} + STATUE_DROP_RARITY 全表 vs NPCID.cs:4795-4797 **逐值一致** ✓
- evalRule 规则族：bossBag（expert 才掉+清 value）、masterCommon、masterAll（perPlayer+恒清钱）、local/perPlayer、gate(LeadingConditionRule)、mechSpawn(1/2500)、oneOf、expert/master/masterExpert 委托 ✓
- value 表抽查（EoC 30000/WoF 80000/slime 0/zombie 60/DEye 75/moon 0）✓
- NpcDrops.ts 头注"NotFromStatue 恒 true"为**陈旧注释**（雕像门实际在 Enemy 死亡段整单跳过 :79647 语义，更准）。

**遗留偏差（记录）**：NotFromStatue 类规则内条件与 Enemy 整单门并存（双保险无害）；luck 来源未移植部分恒 0；天空盒/DST/Mechdusa/NamedNPC 条件恒 false。