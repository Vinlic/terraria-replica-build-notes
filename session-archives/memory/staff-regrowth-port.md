---
name: staff-regrowth-port
description: 再生法杖没效果三根因:近战/工具分支return截胡放置链(213=melee+createTile2)+草族转化放置语义缺失+药草采收链近似;AccFx.flowerBoots类型补法=BEHAVIOR_FX表
metadata: 
  node_type: memory
  type: project
  originSessionId: ec878731-1c65-4b4c-9a3b-c8009ce5461a
  modified: 2026-08-17T10:09:29.428Z
---

# 再生法杖 213 全链（2026-08-17 用户报障"再生法杖没效果"）

**三根因**（按权重）：
1. **使用流截胡**：213 = melee 武器（damage 7）**且** createTile=2（Item.cs
   :4003-4016）——近战分支（`cwMelee && !tool`）与工具分支（5295 再生之斧）
   的 `return` 把放置分支（:6396）整个饿死。修：分支前并行钩
   `tryGrassConvert(tx,ty,heldDef,{noCooldown:true})`（原版 TryUsingItem 里
   melee 挥击与 PlaceThing **并行**；noCooldown=冷却由分支统一设置，同按键
   挥击+放置）。
2. **草族转化语义缺失**：`BlockPlacementForAssortedThings`（:40379-40440）——
   种子/法杖的放置目标是【已有可转化块】非空格：草种/圣种→泥土(0)、腐化/
   猩红种→泥或泥土、丛林/蘑菇/661/662 种→泥(59)、灰烬草种→灰烬(57)；
   法杖/斧额外可转**石头(1)/灰砖(38)**（建党冷知识）。八向暴露门；转化走
   setTile(active→active) 保半砖/坡面/漆。
3. **药草采收链近似**：右键采收曾"仅掉 1 种子"（且 style3/4 种子序互换）；
   砍取（TILE_CUT）曾零掉落。修全 1:1：case 83/84（:65726-65750）草药
   313+style ×1 + 开花种子 307+style ×Next(1,4)；83 时辰门
   `IsAlchemyPlantHarvestable`（:66203-66227：0昼/1夜/3血月·满月夜/4雨/
   5 15:45后且雨中须地下→timeOfDay>15.75/24）；法杖加成（staffOfRegrowthBonus
   :65740-65746）草 ×Next(1,3)+种子 ×Next(1,6)；盆栽自动补种
   （TryReplantingHerbs：below ∈ {78 陶盆,380 种植箱,579}→回种 82 苗）；
   挥割加成（cutTile 对 83/84 时手持 213/5295 置 `_staffHarvestBonus`，
   breakTile 消费）。

**Why（连带两存量 bug）**：
- **NO_SWAP_PLACE 口径错**：原表是 DoesntPlace 的 **createTile（tile sheet）**
  {2,60,70,109,199,23,661,662,633}，曾误拿**物品 vid** 比对——草种子族
  （62/59…）从没被排除方块交换：指向实心块先敲掉再放置。改比
  `TILE_DEFS[TILE_BY_KEY[itemDef.tile]].sheet`。
- tryGrassConvert 必须放 tryPlace **最前**（方块交换段在距离门之前，会把
  可转化目标先敲掉）。

**AccFx.flowerBoots 类型错（同日连带）**：Player.ts 消费 `fx.flowerBoots` 但
vanillaAccFx.ts 的 AccFx 接口没有——行为型旗标走 **BEHAVIOR_FX 补充表**
（interface 加 `flowerBoots?: number` + `'3017'/'3993': { flowerBoots: 1 }`，
GrantArmorBenefits :12682-12688）。

**How to apply**：
- 测试 tests/staff-regrowth.test.ts 8 条（转化四例/采收四例）。
  ★原型壳坑：ITEM_DEFS 的 id=**数组索引**（item() 不写 id 字段，`d.id`
  undefined）；interactAt 射程用 `p.x/y/w/h`（只给 cx/cy → NaN 恒 false）。
- python 搬移代码块务必校验区间方向（i1>i2 切片=空串静默无操作曾致交换段
  双份+ReferenceError）。
- 右键采收本身是 QoL 快捷（原版无右键采收=砍取），掉落语义已 1:1 备案。

关联 [[palm-chop-tileaxe-parity]]（树生命周期批）/ [[mining-model-port]]。
