---
name: loot-parity-audit
description: 宝箱战利品全表对账+修复批:地牢生物群系箱写反(P0)/堆叠两处/lootSeq回卷/金箱ivy/h-250门/flag9-12-13尾段/地狱序成功才递增
metadata: 
  node_type: memory
  type: project
  originSessionId: 4a66e745-9d91-4188-8ade-1e2b7775e8b4
  modified: 2026-08-13T05:36:40.475Z
---

宝箱战利品对账批（08-13，代理全表核对 + 修复，构建绿+单测4/4）：

**P0 已修**：地牢生物群系箱**三元写反**——原版 DungeonGenerationStyles.cs :306 Corrupt块=Scourge(1571)+style24、:346 Crimson块=吸血鬼刀(1569)+style25；本仓 crimson?1571:1569 全反。→ 已正。

**P1 已修**：金箱火把/冰火把 [10,20]（cs:36820 Next(11)+10，曾 10,19）；地狱再生药水 [15,20]（cs:37290 Next(6)+15，曾 15,29）。

**P2 已修**：地牢 lootSeq 回卷——原版 = GetDungeonLootAndChestStyle(:35843) `style≥8→回0 在取件前` + DungeonUtils.cs:399 **成功才递增**；旧 seq 逻辑每循环多一件 164 手枪。

**结构修复**：
- 金箱分支摘 ivy 段（原版 flag4 附赠只在洞穴分支 cs:36864-36880）
- 洞穴/地狱**战利品**分界 = h-250（cs:36839），h-205 只是样式门（cs:36162）——曾并一道门
- 洞穴主件 num25=Next(7) 先掷恒消耗（:36911 种子对齐）
- 地狱 2350/4870 先掷堆叠再选物（:37375）
- nextHellItem 摘自增 → placeBuriedChest **成功后** hellChestIdx++（:36257 失败重试取同一件）
- 金箱 main 段补：832→933 前插（:36549）、flag12 1/40→4978 幼翼（:36568）、蘑菇 flag7（:36689 1/2 矿车+1/3 三件套）、**flag9 门**（:36597 首只暗影钥匙必给后 1/3 + Ram Rune 5465 首只必给后 1/8，GenState.generatedShadowKey/generatedRamRune）
- 洞穴 main 段补 flag7（:37007 1/2 else 三件套）+ flag9（:36892）
- 尾段补齐（:37414-37557）：flag12 天空磨坊 2197 1/3 + Next(6) 五选一画 + 751 云[50,100]；flag13 2195 恒给 + 2767 1/5 else 2766[3,7]；flag9 2192 1/8；上锁箱 flag10 → 尾段 5234 1/2（:37494）；voice 门 rng.int(0,11) 恒消耗
- 地表分支：832→933 后插（:36287）、848→866 法老袍（:36283）
- ChestFlags 扩展 mushroom/dungeon/skyTheme/temple/lockedBiome；样式派生（style 32/16/13 → flag7/13/12）
- **DungeonPass.addChest 接 rollChestLoot**（审计三.3）：地牢箱杂物表 + flag9（钥匙/RamRune）+ 上锁箱 flag10（5234 尾件、不给钥匙）——签名加 rng/gs、vidOfInternal 辅助（ITEM_DEFS 反查 vid）

**id 映射健康**：全部箱源 loot id 6059 条核对零缺失零错误（9=木材是合法地表箱物非块污染）。

**遗留登记（08-13 续2 全清）**：✅ 冰箱门三析取 1:1（cs:36107 `(tile21&&style11)||(tile467&&style24)||(无主件&&位置&&冰tile)`——显式 style 11 也进池+997/669 覆盖，旧 style===undefined 单门是误植；CaveHouse 冰屋摘显式 loot 直入新门）；✅ 沙漠门三析取（cs:36066 `(tile467&&style10)||(style42&&flag16)||(无主件&&IsUndergroundDesert)`——沙漠小屋显式 style10 自动进 desert 池）；✅ 蘑菇小屋 style32→flags.mushroom（样式派生块）；✅ 岛屿屋四件序（cs:79983 houseIdx 0-3=159/65/158/2219，>3→Next(4)——旧三件版 2219 永不出现）+ items 走 rollChestLoot（金箱杂物+flag12 尾段）。**仅剩登记**：Dead Man's Chest 5007 自认有意跳过；voice-change 物品插入（掷已保流对齐，物品未入箱）；金字塔 flag11 强制地表表（866 已补，地表深度自然走地表分支）。

**腐化石锥=原版语义（非bug）**：PlaceUncheckedStalactite :38352 材质组刻意含黑檀石25/猩红203 → 腐化洞穴灰色石锥 1:1。

**用户报告三视觉缺陷另查中**（代理进行中）：冰锥（v_165 实为冰凌，DesertPass placeDeco 底锚帧颠倒+冰帧选错沙岩区）、腐化石锥风格/黄玉悬空/暗影球缝（用户澄清：真·暗影球=v_31_orb_heart sheet31，非祭坛 sheet26；解码=两颗球残骸被裂隙挖半，水平错 3 列）。

相关：[[2026-08-10-loot-new-passes]]
