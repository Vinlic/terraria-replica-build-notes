---
name: vanilla-npc-drops-port
description: 击杀掉落系统 1:1 重做——结构化规则提取器+求值运行时+钱币心星管线，旧 regex 掉落表已退役
metadata: 
  node_type: memory
  type: project
  originSessionId: af6cf2c7-84f1-4f59-9d74-9dc27cdc059e
  modified: 2026-08-11T05:54:03.832Z
---

# 原版掉落系统移植（1.4.5.6 ItemDropDatabase 1:1，2026-08-11 完成）

**旧链路全坏已退役**：extract-npcloot.mjs regex 提取（分母取错列/NPCLootOld 死代码混入/RollLuck(变量)识别不到致史莱姆法杖 100%/伪条目）+ vanillaNpcDrops() 已删除（vanillaNpcs.ts 只留 vanillaItemKey）。

**新链路**：
- `tools/extract-npcdrops.mjs`：C# 迷你表达式解析器（parsePostfix/parseAtom/泛型 `List<T>`/多行数组/链式 .OnXxx/.OnXxx 尾巴变量 emittedRefs/RemoveFromMultipleNPCs/条件变量 `__cond` 解引用）→ `src/data/vanilla-npcdrops.json`（626 条目/385 NPC/条目内 0 unknown）+ `vanilla-npcvalue.json`（393 NPC value）+ slimeBody 表。
- `src/drops/NpcDrops.ts`：resolveDrops 按 netID（回退 type）+全局规则注册序独立求值；链门控 success/failedRoll/failedConditions；expert/master/bossBag(掉袋+清 value)/local/perPlayer(单人化+清 value)/mechSpawn(1/2500×3)；条件求值器 ~40 个（未知→false+warnOnce）；rollCoins=NPCLoot_DropMoney 1:1（均值 ≈1.47×value）；rollHeartsAndStars；rollBossPotionsAndHearts；dropVelocity vx∈[-3,3] vy∈[-4,-1.5]。
- 接线：Enemy.hurt 死亡分支（game.dropContext() 补 zone/季节/血月/风）；`NATIVE_DROP_KEY` 表（71-74 钱币/gel/torch/lens/wood 等走原生 def——vi_ 占位键会让钱币无法计数）。

**Why**: 用户发现掉落与原版差距是结构性的（物品映射 8.3%、概率翻倍、法杖必掉、不掉钱），regex 修补不可救药。

**How to apply**: 改掉落先查 `ItemDropDatabase.cs` + `Conditions.cs`（1456 反编译）；求值语义以 ItemDropResolver.cs:23-58 为准（CanDrop 失败=DoesntFillConditions 不进 failedRoll 链）；expert 在 master 也为 true。验证：tests/npc-drops.test.ts（12 例）+ probe-npcdrops.mjs（PROBE OK）。1456 :1087 晶状体 1/100、黑晶状状体失败后 1/3（与 wiki 旧说相反，以源码为准）。见 [[reference-vanilla-source-of-truth]] [[vanilla-npc-port]]。

**review 补丁（2026-08-11 第二轮）**：① DropNothing 状态=DoesntFillConditions → bossBag/masterCommon/masterAll/nothing 非触发分支改 failedCond；② masterAll(master) 恒 Success（掷骰在 DropItemForEachInteractingPlayer 内）；③ 双子 BeforeLoot（:79761 另一眼存活→value=0+无 Boss 药水/心）；④ 变体 value 表（SetDefaultsFromNetId case -N，-1=100/-4=10000/-5=10）；⑤ **Enemy.vanillaNetId 默认 0 非 null**——netId/value 查表须 `!==0 ? : type` 归一（否则全怪不掉钱）；⑥ 对账闭合：629 调用−5 方法定义−3 变体拷贝=626 条目；⑦ 旧 extract-npcloot.mjs→.retired、vanilla-npcloot.json 已删。遗留：-11 等缩放型变体 value 未提取（非字面量）。

**心/星 pickup 化（2026-08-11 第三轮）**：心(58)/星(184) 是 `ItemID.Sets.IsAPickup`（ItemID.cs:248）——碰触即 `Heal(20)`/`statMana+=100`（clamp 上限）+SoundID 7+ClearOut，**永不进背包**（Player.PickupItem :34594-34630，满血照样消耗——"血不满"门只在生成端 NPCLoot_DropCommonLifeAndMana）。实装：ItemDrop.pickup='heart'|'star' 标记（Enemy spawn 闭包按 id 58/184 打标），触碰分支先于 inv.add 处理；绿色+20/蓝色+100 飘字沿用 addDamageNumber。probe-heart.mjs 验证 healed=20/不进包。

**pickup 全量排查（同日）**：IsAPickup 集合=58/184/1734/1735/1867/1868/3453-3455/4143——ItemDropDatabase 规则表内**零** pickup 类物品（只走怪掉心星+Boss 死亡两条管线，已全覆盖）；星(184)已 pickup 化。雕像产怪/心星雕像未实现（无泄漏）。
**瓦罐掉心纠错**：potLoot `num10==0&&受伤` 分支掉的是 **58 心 pickup**（WorldGen.cs:57511-57531，1颗+1/2，专家再1/2×2）——旧代码误标"蘑菇"(蘑菇= item 5)且 override 58→mushroom_item 收集物。已改 dropHeart+专家分支。
**★ vanillaItemKey(vanillaNpcs) 退役潮**：该函数只认 snake_case 显式注册（vi 表是 PascalCase）→ 大多数 id 返回 null 且**调用方静默跳过**。已换 VANILLA_ITEM_KEY_BY_ID 的三处：potLoot.drop（瓦罐战利品曾整条静默丢失——药水/箭/手里剑/绳全不出）、BuriedChestsPass.vid（宝箱战利品同病）、openNpcShop/npcShopBuy（未映射物品扣钱不给货）。新代码一律用 VANILLA_ITEM_KEY_BY_ID。

**兔子掉珍珠石砖（2026-08-19 修）**：slimeBody 是全局规则（:684），原版 CanDrop 首判 SlimeCanContainItems[type]；本仓曾把类型门外包给"只有史莱姆掷 ai1"——但 **ai[1] 是全 NPC 共享计时槽**（兔子行走计时 120-898/战士/蝙蝠都写），任何怪死时 ai1 恰落 1..6146 都被当物品 id 掉出（兔子 ai1=412 → 珍珠石砖 412）。修 = NpcDrops slimeBody 首行加 SLIME_CAN_CONTAIN 类型门（{1,59,147,184,537}），tests/slimebody-typegate 3 绿（含"非史莱姆全档×6 ai1 档不掉"+"五史莱姆不误伤"）。★铁律：**全局掉落规则的 CanDrop 类型门必须规则内本判**，不能外包给"上游只有 X 会写该字段"——共享槽字段的语义按 NPC 类型分叉。
