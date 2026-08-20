---
name: housing-b-vanilla-ui
description: 住房B方案落地:锚点两轮偏离全摘(锚池空=原版return);queryRoom/assignRoom/住房面板(查询器+NPC头像分配);inter39-42键权威修正
metadata: 
  node_type: memory
  type: project
  originSessionId: c212e38d-8db4-446d-b3da-4e20d707caf7
  modified: 2026-08-15T13:39:43.620Z
---

2026-08-15 用户定案"百分百对齐原版,按 B 执行"——远程基地自动入驻的两轮兜底(出生点/玩家位)**全摘**,入驻轮回归 :5035-5037(锚池空=整轮不跑,含新 NPC 生成);远程基地唯一正路 = **住房查询/分配 UI**(原版玩家侧另一半,已实装):

**原版机制全链(回源实证)**:
- SpawnHomelessNPC 仅在 `num10>=1`(至少一名已安家城镇 NPC)时跑(Main.cs:64530-64537 白天晨间随机门);锚池空直接 return(:5035-5037)
- 手动分配:`PerformHousingCheck(x,y)`(查询器"?"→MoveTownNPC(x,y,-1,Rich feedback),成功播 inter[39]) / `TryMovingNPC(x,y,n)`(选中 NPC 头像→MoveTownNPC(x,y,n) 过→moveRoom+Sound12;Main.cs:44602-44620)
- 失败文案链:inter[40] 无效/[41] 已占/[42] 腐化 + Game.HouseMissing_n(门/光源/桌/椅序,:4680-4700;**原版无 _0**)
- queryRoom 种子 = 任意点(StartRoomCheck 泛洪,实心起点=StartedInASolidTile)

**落地件**:Housing.queryRoom/housingCheckAt(floodRoom 加 needsOut 旗标 flush);Game.housingMode(updateUse 首拍拦截+吞点击)/housingQuery/housingAssign;ui/HousingPanel(查询器+NPC 头像行+家坐标);背包"住房"按钮;mainFlow openHousing;**inter39-42 权威值修正**(shard 原为标题误植:39=此房屋符合要求/40=这不是有效的房屋/41=此房屋已被占据/42=此房屋已腐化,decompile en-US.Legacy.json 核对)

**坑**:动态拼串 `Lang.text('Game.HouseMissing_' + n)` 会被 l10n-audit 扫成裸键 MISSIG——用 const 数组静态 4 键;custom json 嵌套注入用正则锚 `"SandboxWorld": {` 后插子对象;HousingPanel 引 TownNPC 类型走 `import('./entities/TownNPC').TownNPC` 类型位(动态 import 无值)。

tests/housing-ui.test.ts 5 条(任意点查询/缺椅旗标/实心起点/占用·宠物同房/远程基地契约)。housing-remote-anchor.test.ts(偏离期产物)已删。

**review 补(同日)**:①HousingPanel 根必须带 `sw-panel` 类——Input 窗口级 mousedown 的 UI 过滤器(closest '.sw-panel,.sw-slot,...')认这个类,否则面板上的点击穿透成游戏输入(挖矿/挥砍);②住房拦截必须在 updateUse **最前**(:5385),早于 uiBlocking 早退(:5457)——原版背包开着也能点世界分配(mouseInterface 分支优先),我们同序。

**全量对齐版(用户"不能近似"定案,同日二轮)**:DOM 面板退役,改 **Canvas 像素级 1:1**(DrawNPCHousesInUI :41433-41607):右侧竖列 x=screenW-64-28、行高 56×inventoryScale、列满(>screenH-80)换列左移 48、上限 4 列;槽底 Inventory_Back11(悬停 Back14);**行序=HeadListOrder 81 项**(0 号=查询器 NpcHead[0],tooltip=inter[8]"房屋询问";其余=在场城镇 NPC 按 TOWN_NPC_HEAD_INDEX 头索引持有表,CannotBeDrawnInHousingUI{21,80} 剔除);头像 36px 上限缩放居中;左键选中 Sound12(:41506)、右键取消 Sound12 自毁(:44666);携带 NPC 离场自动降级查询器(:44649);悬停 tooltip=FullName/inter[8](:41498)。**查询器贴图即 NPC_Head_0(原版同槽逻辑),勿自造放大镜图标**。
