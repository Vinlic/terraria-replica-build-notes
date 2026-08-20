---
name: local-item-retirement
description: 184本地物品退役vi_单空间:迁移锚快照/v4存档armor稳定id/createTile回填/钱币单轨/v3裸下标vi_分支禁走稳定表
metadata: 
  node_type: memory
  type: project
  originSessionId: d76053b3-a9fb-4d75-a43d-41f181c7cab5
  modified: 2026-08-18T06:42:59.275Z
---

2026-08-13 本地自制物品全量退役(184 键:170 迁移 vi_ + 12 盔甲循环 + 2 删除 wood_pickaxe/wood_axe),只剩原版 1:1。

- **基建**:`data/itemKeys.ts`(VI/VI_ID/VI_KEY——全库唯一物品字面量源,后续 dual-key 清理只动此文件)+ `data/itemMigration.ts`(RETIRED_KEY_TO_VID=ITEM_KEY_TO_ID 派生+补 15 条[coin_platinum:74/mana_regen:293/12盔甲/grand_design:3611 覆盖撞号];读档 remap 漏斗)。**VANILLA_ITEM_KEY_BY_ID 归一驼峰键,严禁手拼蛇形 vi_ 键**。
- **迁移锚**:`src/data/legacyItemIndex.generated.json`=删除前构建的 index→key 快照(v3 存档 armor/dye/trash/misc 段裸下标解码表)。★删后绝不能重跑生成器(会把本地键抹掉);items.ts 注册顺序再变也需以"含本地键的旧构建"重生成——生成器测试已删,快照即终态。
- **存档 v4**:serialize armor/dye/trash/miscEquips/miscDyes/loadouts 全走稳定 id(v3 是裸下标,曾对注册顺序脆弱);版本分派:≥4 稳定 id、==3 armor 段走快照反查、v2 接受破损。**v3 裸下标的 vi_ 分支必须 `ITEM_BY_KEY[快照key]` 直查——经 ITEM_STABLE_OF_INTERNAL[裸下标] 在删除后整体错位(踩过:解析成 vi_453_bomb_statue)**。
- **放置回填**:items.ts 注册尾循环 itemfunc.createTile(1040 条全可解析)→TILE_KEY_BY_SHEET→def.tile/placeStyle(蛇形+驼峰双 def 都刷,仅填 undefined);钱币四 def maxStack=100。本地放置物继任全部核验(torch=4/door=10/workbench=18/furnace=17/anvil=16/chest=21/platform=19)。
- **钱币单轨**:COIN_KEYS=vi_71-74;晋升仅在钱币区放不下时触发(DoCoins 逐格判同面额,一次只升一级);spendCopper/gainCopper(补铂档)/商人门槛(coinIndexOf+COIN_VALUES,顺修漏铂)/死亡掉钱/coinsOwned 全单轨;4 张 vid→本地 override 表拆除(NATIVE_DROP_KEY/COIN_KEY_BY_VID/potLoot/WldImport ITEM_MAP——后两者曾把金/银币折成铜币,10^6 缩水 bug)。
- **RECIPES 自制表整体退役**(recipes.ts 已删):合成只留原版段 3173 条;"本地材料对原版配方不可见"缺口随退役自然消失(vi_ 材料自带 vid)。
- **开局语义修正**:copper_sword(3508 Broadsword)→3507 Shortsword(原版新玩家=镐3509/短剑3507/斧3506)。
- tiles.ts drop 字段全量改存 **vid 数字**,读取端(Game cutTile/World.breakTileAt)typeof number→VI() 解析。
- 死代码清理:VANILLA_ITEM_ICON_MAP 本地段 169 条/ItemIconGen 本地 switch/LEGACY_USE_STYLE/NATIVE_ITEM_VID/SmartCursor·Torch·Renderer 本地 'torch' 特判(vi_8 经 viIdFromKey 自动解析)。
- 测试:item-retirement(迁移表健全+PRIV 漏斗落点)/place-backfill(1040 全落+10 继任核验)/save-migration-v4(v3 armor 三分支+删除键归0)/coin-single-track;14 个既有测试同步 vi_ 化(mining 改 itemfunc+combat 桥断言)。
- 遗留:v2 存档与跨版本联机接受破损(政策);place_v_* 族未收敛(独立决策);dual-key 蛇形/驼峰清理仍延期(docs/dual-key-cleanup-plan.md,现在只需动 itemKeys.ts)。
- **退役后回归(2026-08-18 修)**:vi_ def 的 `vid` 字段注册循环**不落**(全库仅 2 条手写例外)、`name` 恒 ''——凡裸读 `def.vid`/`def.name` 的消费点在退役后级联落空。快捷栏选中名(UI.refreshHotbar)曾裸取 `ITEM_DEFS[id]?.vid ?? -1` → 恒显 inter(37)"物品"(旧本地物品有实 name 兜底所以退役前正常)。修=走 `Lang.itemNameByKey(key)` 全链(vi_ 前缀→官方 l10n→zh/en id-maps→place_v_ 方块名→Mods→name)。约定:要 vid 用 `def.vid ?? viIdFromKey(key)`(Game.ts 全线如此);要显示名一律 itemNameByKey。
