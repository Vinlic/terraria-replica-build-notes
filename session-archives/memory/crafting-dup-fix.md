---
name: crafting-dup-fix
description: 合成重复配方根因(自制表内部重复+vi_跨表双显)+合成音SoundID7+输入框键盘穿透修复+本地材料未桥接原版id空间缺口
metadata: 
  node_type: memory
  type: project
  originSessionId: d76053b3-a9fb-4d75-a43d-41f181c7cab5
  modified: 2026-08-12T15:41:09.670Z
---

2026-08-12 背包合成对齐检查结论与修复:

- **重复配方根因**(木锤双显):自制表 `data/recipes.ts` 内部就写了两遍(行 21/38,批次追加没查重);钨锭/铂锭同款两遍。已删,单测锁(vanilla-recipes.test.ts 新增 describe:内部去重+产物禁 vi_ 前缀)。
- **跨表双显**:自制表 vi_ 产物(93 木墙/26 石墙/109 魔力水晶)与原版段(vanilla-recipes.json 3173 条,内部零重复)双显;魔力水晶自制数值还是错的(3 坠星,原版 1456 徒手 5 坠星)。已删自制三条,vi_ 一律走原版表。
- **两表设计**:原版段只认 vid≥0 的物品(VID_TO_KEY 首个注册者胜);自制表 local 键(wood/copper_bar 等)与原版空间**故意隔离**——若给 local 物品挂 vid 会造出新双显(workbench 等)。材料桥接必须走"仅材料侧别名表"路线。
- **已知缺口(待做)**:本地材料(wood=9/stone=3/gel=23/矿/锭)无 vid → collectOwnedItems 不可见 → 原版段凡用这些材料的配方(木墙 93 等)合成不可用。修法:vanillaRecipes.ts 加 MATERIAL_ALIASES(仅材料计数/扣料/显示,不碰产物)。
- **合成音效**:原版 = SoundID 7 物品抓取(成品上鼠标 grab 声,ItemSlot PlaySound(7));三处已改 'pickup'(craft/vanillaCraft/vanillaCraftOutput,原 tink 是错的)。
- **键盘穿透**:main.ts window keydown(KeyE/Escape/F3-F12)与 Input keydown(快捷栏数字/缩放/Space preventDefault)都不查 e.target——搜索框打字会关背包/吞空格/切快捷栏。两处都加了 INPUT/TEXTAREA/contentEditable 早退(仅 Escape 放行);背包打开时数字键不切快捷栏(uiBlocking 门,原版语义)。
