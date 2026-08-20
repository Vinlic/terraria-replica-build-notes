---
name: town-npc-persistence
description: 城镇 NPC 存档/wld 导入持久化 + bound NPC 被入驻轮塞进同一空房叠加的修复
metadata:
  type: project
---

2026-08-10 城镇 NPC 三连修（用户报"存档多个 NPC 叠在出生房、点击出现已获救"）：

- **缺口一（saveGame 写死 npcs:[]）**：城镇 NPC 从不保存——saveGame/serializeSave 加第 4 参 `townNpcs`（Game.townNpcsForSave() 快照：key/位置/home/bound/givenName），链路 mainFlow.doSave → saveClient.save → worker postMessage（SaveRequest 加 townNpcs）→ serializeSave；回退同步路径同参。
- **缺口二（load 不消费 + wld 导入丢弃）**：SaveData.npcs 读出后挂 `world.pendingTownNpcs`；Game.afterWorldLoad 有列表则**原位生成**（TownNPC+home+bound+givenName）、无向导条目才补向导、跳过 placeBoundRescueNpcs；空列表走原新世界逻辑。wld 导入（WldImport）：WldWorld.npcs（x/y=像素、home=tile、-1=homeless）→ SaveData.npcs，spriteId 反查 TOWN_NPC_IDS；**bound 型 id 映射**（id-maps 核实）：105 BoundGoblin→goblin_tinkerer、106 BoundWizard→wizard、123 BoundMechanic→mechanic、354 WebbedStylist→stylist、**589 GolferRescue→golfer**、534 DemonTaxCollector→tax_collector。
- **缺口三（叠加根因）**：updateTownNpcArrival 的 QuickFindHome 对未安家 NPC 找空房入住——**没排除 bound**，五个救援 NPC（homeless by design）被依次塞进同一间出生房同一点 (3202,405)。修：`if (n.home || n.bound || ...) continue`。原版 AI_007 bound 态原地待救。
- "点击出现已获救"= freeBoundNpc 正常语义（wld 里他们就是未解救态）；修完叠加后体验正常（各自原地，走到跟前才解救）。
- 探针：scripts/_mapbug.mjs（__swFlow.loadJson 桥 + bound NPC 时序 trace + tick 循环后全量 dump）。修复验证：tick 循环后 bound 全部留在原生位置（地牢/蜘蛛巢/沙漠/洞穴），guide 正常入住出生房。

**Why:** 原版 WorldFile 的 town NPC 段是读档必经路径；缺它=每次读档 NPC 清零重生成，入驻系统再把 homeless 全搬进空房。**How to apply:** 改 SaveData 字段时 SaveFile.ts 与 serialize.ts 是**双胞胎**（worker 共用 serialize），两处必须同步改；wld NPC spriteId 查 id-maps/npcs.json 的 internal 名区分正常态/救援态。关联 [[vanilla-npc-json-gaps]]。
