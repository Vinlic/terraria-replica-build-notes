---
name: recipe-engine-port
description: 配方引擎 1:1 完成态(2026-08-13):3173配方+decraft全链+RecipeGroup双侧语义+value=0真相;提取器与测试索引
metadata: 
  node_type: memory
  type: project
  originSessionId: ec878731-1c65-4b4c-9a3b-c8009ce5461a
  modified: 2026-08-12T16:27:34.356Z
---

配方引擎(Recipe.cs + ShimmerTransforms)2026-08-13 按"全面补齐 1:1"目标完成。**原版 SetupRecipes 无 AddCondition(进度锁只在 decraft 侧 RecipeSets)**,引擎面即全部。

**数据**:tools/extract-recipes.mjs 从 Recipe.cs SetupRecipes 折叠注册序 → vanilla-recipes.json(3173 条:create/createStack/tile 36 站点/items/groups 31 组/water·honey·lava·snow·graveyard·alchemy(站点13自动)/**notDecraftable 119/crimson 15/corruption 15/shimmer(CustomShimmerResults) 5**,2026-08-13 补提三标志+shimmer)。组序=注册序(last-wins 的基础)。

**运行时**:
- craft 侧:collectOwnedItems(含组假 id 1000000+gid 聚合)/craftableCount/envOk(站点继承+环境)/consumeMaterials(炼金台 1/3 折扣 :213-227)。**RecipeGroup 双侧语义修复(:15043-15056)**:材料槽 id ∈ 组 ValidItems → 该槽=组——craft 判定/扣料均按"组内任一物品"(持 Boreal 木 5215 可造火把/被扣);提取器数据的哨兵 id ≥1000000 与占位真实 id 两种形态都由 groupOf() 归一。
- decraft 侧(Shimmer.ts + ItemDrop.tryDecraft):UpdateWhichItemsAreCrafted(:15110 last-wins,notDecraftable 跳过)→ GetDecraftingRecipeIndex(:15 猩红/腐化分支)→ IsRecipeIndexDecraftLocked(:47 含 154 骨→骷髅王/1101→石巨人)→ GetShimmered 分支序 **:1786 钱币→:1809 转化→:1878 decraft(勿改序!)** → decraftOutcome(customShimmerResults 覆盖/组代表替换/炼金 rand3=Main.rand.Next(3) 逐单位 1/3 蒸发/逐产物 9999 拆垛)→ spawn(shimmered 上浮+≥2 材料按序号交替散射)。canShimmerItem 补 :49056 decraft 位(decraftCtx 四参)。

**两个易错真相**:
1. **vanilla-itemvalue.json 只存 SetDefaults case 内显式赋值;缺表 = 原版 value 0(Item.ResetStats :48596)绝非"未知"**。DecraftItemId(RecipeGroup.cs:59 OrderBy(value).First() 稳定)曾误用 MAX 回退 → Wood 组被 5215 抢位;`?? 0` 后组代表=9(木配方 decraft 返还普通木材,原版已知行为)。
2. 木剑(24)=7 木头(item id 别背错);火把 createStack=3(findDecraftAmount 按它除)。

**测试**:tests/decraft.test.ts(16,rand3 注入确定性)+tests/shimmer.test.ts(18)+liquid-shimmer-render(5)全绿。调试:getDecraftingRecipeIndex 在 vanillaRecipes.ts(Shimmer.ts 只 re-import 非导出)。

**LiquidSim 环形缓冲重写审查(2026-08-13 已通过)**:LiquidBuffer.cs 权威语义三条——①满(49998)丢新 ✓;②**入队即置 checkingLiquid(:115)**——曾漏,同 tick 同格二次 AddWater 会重复入队(已补一行修复);③DelBuffer(0) 是交换删除=首元素后接倒序,**非 FIFO**(我们的 FIFO 与旧 Array 行为一致、checkpoint 双种子实测不可观测,留档不改)。复验:caves-checkpoint 3/3(含 SandboxWorld corruption)+liquid/shimmer/decraft/terrain 49/49。**坑:并行会话实时重构测试基建时跑 vitest 会撞中间态(__crDump is not a function 之类),重跑即好**。相关 [[liquidtype-plus-one-encoding]] [[blockframes-lookup-rebuild]]
