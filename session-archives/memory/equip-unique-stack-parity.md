---
name: equip-unique-stack-parity
description: 装备唯一性(同款/双翅膀/DualEquipArmor)+maxStack 1456改制(默认9999仅11例外!1405的1844处已废弃);vi_堆叠表权威化
metadata: 
  node_type: memory
  type: project
  originSessionId: 413208b1-378e-40ae-a408-9ae931eb30dd
  modified: 2026-08-13T05:02:14.526Z
---

2026-08-13 装备唯一性 + 堆叠上限对账(用户点名项):

**配饰栏位置**:背包面板(Esc)→顶栏"装备"页签→左侧三列竖排(染料|时装|装备),
装备列两段式=盔甲 armor[0-2] + 4px 组距 + 配饰段 armor[3-7](8 恶魔之心/9 大师解锁),
染料/时装镜像 10-19(UI.ts buildInventoryPanel vcol2)。

**maxStack 1456 最终态(★重大口径)**:1.4.4 改制把逐物品堆叠全废——
`Item.CommonMaxStack=9999`(Item.cs:66)为 ResetStats 默认(:48615),全 SetDefaults
链仅 **11 处覆盖**:{71,72,73}=100(铜银金;**铂 74=9999**!DoCoins :38570 只对
71-73 恰 100 进位)、{58,184,1734,1735,1867,1868,1922,3388}=1。1405 有 1844 处
逐物品赋值(30/99/999)已全部废弃——**武器/药水/材料一律 9999**。实现:data/items.ts
`VANILLA_MAX_STACK` 表 + item() 对 vi_ 键**一律表权威**(手写 maxStack 忽略);
曾错:vi_ 默认 999/唱片=1/喷泉=99/铂币=100 全部纠正。

**装备唯一性(Inventory.armorAccepts 扩展,原版 ItemSlot.cs)**:
- 配饰功能段 3-9/社交段 13-19:**段内同 type 唯一**(冲突槽=自身槽放行 :3242)、
  **双翅膀互斥**(CanEquipBothAccessories :3202,不同款翅膀也不行)、
  **跨段同 type 互斥**(:1313/:1322)——按内部 id 比=原版按 type(词缀不同也算同款!)
- 盔甲 0-2↔10-12 同款互斥,`DualEquipArmor{205,5004,4955}`(ItemID.cs:54)白名单例外(:1251/:1260)
- 拖放(placeHeld)与一键装备(swapEquipItem)都汇到 armorAccepts 单点门
- miscEquips 五类各一槽,唯一性天然成立

测试 tests/inventory-equip-rules.test.ts 8 条(堆叠表/合并上限/同款/跨段/双翅/
Dual 白名单/槽位范围)。坑:测试取样勿硬编码 vid(itemstats 覆盖面为准,40 号
赫尔墨斯靴不在表);并行会话同期重写 items.ts(本地物品退役),vi_ 批量注册循环
(vanilla.json :745)也传过 maxStack:999 须一并拔除。

相关:[[local-item-retirement]] [[use-path-final-audit]]

**凝胶弹药栏（2026-08-19 修）**：用户报"没到获得枪的阶段凝胶就归入弹药栏"。原版拾取路由两趟（Player.cs FillAmmo :38591-38655）：①合并弹药栏 54-57 已有堆（全部 FitsAmmoSlot 物，凝胶亦然）；②填空格仅 CanFillEmptyAmmoSlot（Item.cs:1360-1369）——八种特殊弹药 {23 凝胶/169 沙/75 坠星/370 黑檀沙/408 珍珠沙/1246 猩红沙/353 麦酒/849 致动器} 不自动入栏落背包。曾 fillRange 无差别合并+填空 = 根因。修 = Inventory.add 弹药段拆两趟（fillRange 加 mergeOnly 档）+ canFillEmptyAmmoSlot 助手。★42 是弓非箭（useAmmo=40 消耗 40 木箭——itemcombat 42 无 ammo 字段是正确数据非缺失）；★Inventory 空槽 = null 非 undefined。tests/gel-ammo-slot 6 绿。
