---
name: palm-chop-tileaxe-parity
description: 树族砍伐+生命周期全对齐:v_323缺axe根因;★gemcorn门在树顶标记格(一审误修干基);砍伐=切口及以上树桩保留;木材按基座草族;仙人掌CheckCactus三规则+vi_276;橡实11档锚点表/再生之斧补种/Lucy全消息机/苗成长分发(frameX/54档)
metadata: 
  node_type: memory
  type: project
  originSessionId: ec878731-1c65-4b4c-9a3b-c8009ce5461a
  modified: 2026-08-17T08:44:20.306Z
---

# 树族砍伐 tileAxe 全对齐（2026-08-17 一审棕榈 + 二审全树族）

**一审根因**：`v_323_palm_trees` def 缺 `axe`（def() 缺省 -1）→ toolCanBreak
斧档恒 false。tileAxe 16 件（Main.cs:7157-7172）：5,72,80,488,704,323,596,
616,634,583-589。连带修：镐排除门（Player.cs:45039 `pick>0 && !tileAxe[·]`，
pick 档加 `&& d.axe < 0`）——v_5/v_80 的 pick:0 此前允许镐挖树。

**二审（KillTile_GetTreeDrops :66245-66309 权威核对）五修**：
1. **★宝石树 gemcorn 门在树顶标记格**（`frameX≥22 && frameY≥198`，
   SetGemTreeDrops :66149）——growTreeWithSettings 树顶覆写冠帧
   （cs:30932-30967）；干底格实际是 132-176 基座帧。**一审误当"干基门"
   修到干底格 → 真树仍永假**（测试种了假帧才绿）。教训：帧语义条件先到
   worldgen 种植端核对帧落位，勿按直觉命名。
2. **砍伐范围 = 切口及以上**（Player.cs:45120 单格 KillTile → SquareTileFrame
   3×3 → CheckTree :54598 上行级联，树族全 frameImportant），**切口以下树桩
   保留**（其下方仍是干/草 → CheckTree 存活门通过）。旧实现整列连桩清除非
   原版。蘑菇树 72 级联在 TileFrameImportant case 72（:86582-86606）。
3. **木材按基座草族**（GetTreeType :63106）：2/477→木9、23/661→乌木619、
   199/662→阴森911、60→红木620、70→每格50%发光蘑菇183或无、147→针叶2503、
   109/492→珍珠621、633→灰烬5215。每格1木+bonusWood（:66306 Next(35)<=
   手持斧力 || 1/3 → 该格2）。基座溯源 GetTreeBottom :63519 **穿透空格**到
   首个活性格（砍侧枝也溯源对）。
4. **橡实 = 树冠标记格 50% ×1**（TreeTypeDropsAcorns :63140：None/Mushroom/
   Jungle 不掉）——旧 75%×2-3 是自创。普通树 5/596/616/634 与自有 'tree'
   （worldgen/橡实生长主路径）共用 dropVanillaTreeLoot。
5. **仙人掌（CheckCactus :54132 三规则）**：①根列溯源（断干处经斜叠臂平移
   列）到底无沙族(53/112/116/234)整砖→死；②臂格 below/left/right 全非80→死；
   ③干格正下方非80且非沙族→死。不动点迭代（干/臂互撑单遍扫描会死锁——
   曾用臂规则套干格）。每格掉 vi_276（GetItemDrops case 80 :64767，无bonus）；
   挖脚下沙也级联整株倒。斧伤害 ×3 再 ×1.2（:45098-45100 已对）。

**三批（"不允许遗漏"指令全量收口，2026-08-17 同日三审）**：
6. **CanKillTile 上方保护族**（:62276-62315）：干族（枝 66@0-44/88@66-110/
   冠 Y≥198 例外）/棕榈干基 66,220/箱柜 21,26,77,88,467/蘑菇树 72/倒木 488/
   仙人掌底帽帧（frameX/18∈{0,1,4,5}）→ 本格不可破坏。双门：tryMine 伤害归零
   （:45108）+ breakTile 早退（CheckTileBreakability 同语义，爆炸同门）。
   ★挖仙人掌脚下沙在原版是被拦的（保护帧）——CheckCactus 沙支撑级联只在
   非底帽帧/沙流走后触发。
7. **橡实放置全锚点**（TileObjectData tile20 :4858-4900）：11 类地面 → 交替档
   0/3/6/9/12/15/18/21/24/27/30，帧=(档+Next(3))×18（RandomStyleRange=3）；
   成长分发读 frameX/54=档/3。旧"仅 T.GRASS+toast"自创。placeAcornSapling
   同时供再生之斧 5295 补种（IsBottomOfTreeTrunkNoRoots 破坏前捕获）。
8. **Lucy 全消息机**（items/LucyAxe.ts）：七源 IndexedFromCategory 取模循环，
   variation byte；弹字=dmgNumbers label（420t 色 RGB(184,96,98)×1.15=#D46E71
   + vx 漂移——label 路径补了 vx）；音 lucyaxe_talk 5 变体 0.4；表情 149；
   hasLucy=背包任意格（:12213）；Idle 7200-14400t；cactus/Storage/PickedUp
   420t 冷却；砍树源无冷却。UI placeHeld 存取态翻转+throwHeldToWorld 接钩。
   MP msg141 未接（记档）。
9. **苗成长 faithful 分发**（AttemptToGrowTreeFromSapling :72849）：tile20 档
   10→灰烬（★ASH_PROFILE.sapling 曾误 590：growTreeWithSettings 苗越格走查
   消费该字段→运行期灰烬苗永不成树，改 acorn_sapling）/6-9→棕榈/其余→
   growTree 全套（枝/根/冠+高度 5-16，旧自造光杆柱退役）；595/615→观赏树
   （1/5 采样=4×）；地下区仅档 10。成树 FX=视野内叶爆近似。
10. **toolCanBreak→toolMatchesTile 撞车**：并行会话同日重构（sheet 口径+
    平台镐可拆修正），测试随之迁单源——以对方为准合并。
11. **探针方法论（_treelifecycle.mjs 全绿 10 断言）**：物品注入必须走
    `spawnDrop(key)+fixedUpdate×40 自动拾取+按 drop.itemId 找槽选中`——动态
    `import('/src/data/items.ts')` 在并行会话热编辑期与游戏实例**分叉**
    （双 ITEM_DEFS → 假 id 炸 Player fixedUpdate:1792 unguarded `.key`）。
    vanilla.json 键推导：`/sprites/vanilla.json` items 段以数字 vid 为键、
    内含权威 PascalKey → `vi_<vid>_<PascalKey>`。tryMine 连击须手动
    `g.tickCount += 60` 跳冷却；放置/挖掘前传送玩家（inTileRange 射程门）；
    沙地苗要找干平沙（液体/半砖门拒绝）。
12. **定责实验**：全量回归的 worldgen 金标失败（caves-oracle/shimmer/
    final-hash/spawn-tree-clear 同树 (2958,538)）= 并行 worldgen 会话在途
    状态——回退我方 ASH_PROFILE.sapling 后**同树同断言仍败**即排除；还原。
    ASH_PROFILE.sapling 对 worldgen 无行为差（调用点 y=草地行，苗越格走查
    两值都立即停）。

**How to apply**：
- 帧捕获必须先于 `setTile(x,y,0)`（双轴清零）；帧语义条件先查种植端帧落位。
- 棕榈掉落：每干格棕榈木 2504（无 bonus 掷）+ 树冠格（X 88-132）橡实 +
  邪恶沙变体（234→911/116→621/112→619，下扫跳过非实心活性格 cs:65298）。
- 倒木 488/704：无掉落（GetItemDrops 无掉落表），object 锚点路径 drop:null ✓。
- 测试：palm-chop 15 条 + tree-lifecycle 7 条（锚点表/补种门/Lucy 冷却机/
  苗分发三族）。原型壳 `Object.create(Game.prototype)` 直调 private。

关联 [[mining-model-port]]（挖掘模型）/ [[gem-anchor-gate-port]]（宝石 178
放置锚定——与宝石树掉落无关）。
