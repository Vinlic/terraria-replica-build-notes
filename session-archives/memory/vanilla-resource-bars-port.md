---
name: vanilla-resource-bars-port
description: 资源条双样式：Classic 朴素心星 + Fancy 华丽金框（1.4.4+ 原版默认"New"样式）+ 光标原版化
metadata: 
  node_type: memory
  type: project
  originSessionId: 04569a63-44aa-4669-98a3-b777d15e98f8
  modified: 2026-08-13T02:06:16.528Z
---

# 原版资源条（生命心/魔力星）双样式

**根因背景（2026-08-13 用户报"心和星没金边"）**：此前只移植了 **Classic**（"Default" 旧样式——红心暗红描边、蓝星朴素）。原版 1.4.4+ 默认是 **"New"=FancyClassic**（金框分格面板）——用户看到的金边就是它。两者都对，是样式选项不是贴图错误（实测：Heart.png 边缘纯暗红 (57,4,5) 零金色像素；FancyClassic/Heart_Single_Fancy 36×38 有 212 金像素、青铜框 (185,151,59)）。

**Classic（已有 ResourceBars.ts）**：ClassicPlayerResourcesDisplaySet 1:1；金心=生命果 Heart2 **从首颗起消耗**（420 上限=前 4 金、500 全金）勿"纠正"成尾部金；星列 x=775+anchorX 竖排 28px；亮度 30+225×fill。

**Fancy（2026-08-13 新增 `src/render/FancyResourceBars.ts`）** 1:1（FancyClassicPlayerResourcesDisplaySet.cs :118-290 + PlayerStatsSnapshot.cs:21-47 + ResourceDrawSettings.cs:26-55）：
- 心条锚点 **(sw-296, 15)**（NewWithText 时 y+6）；面板层两行（行距 28；行 2 元素索引偏移 10）——HeartPanelDrawer :236-253：首格 Heart_Left(28×30)/中间 Heart_Middle(24×30)/行末 Heart_Right(26×30)、**总末格（==lastHeartPanel）Heart_Right_Fancy(36×38) 华丽帽偏移 (-8,-4)**、单心 Heart_Single_Fancy(-4,-4)；推进=贴图宽。
- 填充层（HeartFillingDrawer :255-270）：锚点 +(15,15)、推进 **2+22px**、**缩放=GetLerpValue 填充比例从中心生长**。★锚点语义=**精灵中心**（ResourceDrawSettings.Draw :26-55：OffsetSpriteAnchorByTexturePercentile=(0.5,0.5) → spriteBatch origin 中心，position 即中心）——曾误当格子左上再加 +11/+12 → 填充整体偏右下 ~11px="心/星与边框错位"（2026-08-13 用户报，已修，实测心填充质心=格中心 998.0/998.0 分毫不差）；生命果格（fruit=(baseMaxHp-400)/5）用 **Heart_Fill_B 金填充**；回满那格叠加 cursorScale-1。
- 星列锚点 **(sw-40, 22)**：Star_A(顶)/Star_B(中)/Star_C(底)/Star_Single；填充 Star_Fill(22×24) 锚点 +(15,16)、推进 **-2+24px**、中心缩放。
- "New" 默认无文字；NewWithText 才画生命文本。

**素材管线两坑**：①vanilla-ui-whitelist.json 是纯 JSON **不能插 // 注释**（JSON.parse 挂、atlas 崩）；②手工 cp 到 public/sprites/vanilla-ui/ 的散文件会被 `vite build` 的 vanillaAtlasAuto 冲掉——**白名单才是持久权威入口**。12 张 FancyClassic 入白名单，展平键 `UI_PlayerResourceSets_FancyClassic_*`（源 terraria-assets/Images/UI/PlayerResourceSets/FancyClassic/）。

**接线**：Options.resourceBarStyle `'fancy'|'classic'`（**默认 fancy**=原版默认），Settings 界面页"生命和魔力样式"切换（Lang 键 `UI.SelectHealthStyle`）；Renderer 分流。探针 `_fancy-bars-probe.mjs`：12 贴图全载/心区金 68/星区 64/fancyDefault ✓。

（历史）光标原版化：`#sw-cursor-style` 全屏 cursor:none、ui-canvas z300、VUI 自愈循环画 Cursor_0。小地图 (屏宽-292,90) 让位；MinimapFrame/Default 皮肤 1:1（黑垫 244²/框 256×264 @(-8,-15)/正方 240²/三按钮 18px 悬停）。扩容三件套：生命水晶/生命果 vi_1291/魔力水晶 vi_109 入存档。遗留：TryToHover tooltip、其余 8 款小地图皮肤。

关联 [[vanilla-ui-port]] [[sandboxworld-project-setup]]
