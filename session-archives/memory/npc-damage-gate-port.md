---
name: npc-damage-gate-port
description: 玩家弹/爆炸对城镇NPC伤害门(Damage_PVE_Inner三例外:臭鸡蛋318无条件/巫毒22·54装备门/explodeAt同门);hitTownNpcs已有projId参;Arrow友方支曾整缺
metadata: 
  node_type: memory
  type: project
  originSessionId: ec878731-1c65-4b4c-9a3b-c8009ce5461a
  modified: 2026-08-18T04:48:26.040Z
---

# 玩家弹/爆炸 → 城镇 NPC 伤害门补齐（2026-08-18，"原版 NPC 受爆炸物伤害吗"追问）

**原版语义**（Projectile.Damage_PVE_Inner :11895-11925）：
- 玩家方弹（friendly）：`flag = !npc.friendly` → 城镇 NPC 恒 false → 免疫。
  三例外：**臭鸡蛋 318 无条件**（:11971 `flag |= type==318`——全游戏唯一
  可无条件砸 friendly NPC 的玩家弹，物品 1809 consumable 投掷→Arrow projId 318）；
  **向导 22** 需玩家装备向导巫毒娃娃 267（killGuide）；**裁缝 54** 需裁缝娃
  1307（killClothier）——任意玩家弹（弓/回旋镖/魔法弹/炸弹）都可走此门。
- 敌方弹：hostile && friendly && !dontTakeDamageFromHostiles 恒命中。

**本仓盘点**（比初判好：hitTownNpcs/projTargets 已有且覆盖广）：
- 已有：Whip 巫毒门 ✓；Dart 陷阱弹内联 npc 循环（hostile）✓；Arrow hostile
  支 ✓；WeaponProj/MagicProj 调 hitTownNpcs 但 projId 没传（318 例外出不来）。
- 曾缺四件（本批补）：
  1. **hitTownNpcs 加 projId 参**：playerProj 门 `!doll && projId !== 318` 拒。
  2. **Arrow 友方支**（曾整缺——玩家弓/投掷弹对城镇 NPC 完全跳过）：
     `else if (!reflected && hitTownNpcs(..., 'playerProj', this.projId))`；
     318 命中即碎（penetrate 1 语义 killNow）。
  3. WeaponProj/MagicProj 调用点补传 projId。
  4. **explodeAt 城镇 NPC 门**（炸弹+向导巫毒=经典杀向导链）：同巫毒门
     （318 非爆炸物实际不达此路径），victim-settles 同盒（hurtBox 半宽判交）。

**二审补（2026-08-18 review 批）**：
- explodeAt 门表达式与 hitTownNpcs 对齐（`!doll && projId!==318` 拒——曾写成
  `!doll || projId===318`，语义反转但 318 非爆炸物不可达=无害，仍对齐消歧）。
- **SkyDragonFury（Spin.applyHits 线段盒 + Swing 三段敌循环）与 FirstFractal
  补巫毒门**（projId 0=纯巫毒、无娃娃 no-op 零风险）；Celeb2Rocket 直击无门
  但命中即 explode→explodeAt 门已覆盖（结果等价，直击 vs 附近爆的形态差异
  记档）。Dart 内联 NPC 循环复核为【仅敌对弹可达】（`!hostile||reflected`
  提前 return）=flag2 正确，友方炮弹/雪球不经此 ✓（一审误判）。
- GrenadeProj 接触引爆仅查 enemies=faithful（原版 friendly 弹对城镇 NPC 无
  命中不触发引信）。

**How to apply**：
- 测试 tests/npc-damage-gate.test.ts 7 条。★TownNPC 构造器 (key,x,y) 的 y 是
  **脚底**锚——盒顶 = y−h+2，测试弹/爆心必须按 `n.x/n.y` 实际盒算重叠
  （按传入 y 算 = 恒不重叠假阴性）。explodeAt 原型壳须 stub
  addDamageNumber/playSfxFiles（真方法碰未初始化 dmgNumbers → 'push' of undefined）。
- 反射弹（reflected→hostile）对城镇 NPC 走 hostile 支=原版 flag2 语义 ✓。
- Cannonball blastDamage（Dart 162/281）只伤敌怪 = faithful（friendly 弹）。

关联 [[pvp-system-port]]（victim-settles 模型）/ [[town-npc-attack-port]]。
