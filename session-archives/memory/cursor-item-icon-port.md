---
name: cursor-item-icon-port
description: 指针物品/交互图标系统全量移植+收口批——余辉/群系覆写/悬停表提取器(穿透公式对象回填)/油漆子图标/住房携带头像;收口:temple·remix旗接通+孤儿箱文本支(MouseText无面板带影文字)+FakeContainers 441/468+放置建记录88族
metadata: 
  node_type: memory
  type: project
  originSessionId: c212e38d-8db4-446d-b3da-4e20d707caf7
  modified: 2026-08-15T17:06:34.118Z
---

2026-08-15 DrawInterface_40(:44474-44562)+DrawInterface_38(:44622-44688)全量移植;08-16 收口批清遗留。

**结构**(三层):
- 数据层 `Player` 五字段(cursorItemIconEnabled/ID/Push/Text/Reversed,每帧 tickCursorIcon 头重置)+ `Game.itemIconCache`(余辉:time=10/移动>4px 清/换物品清/移动时每帧-1 :45922-45945)+ 4 使用路径触发(放置/通用桶族/电路工具,射程门内)
- 悬停表 `Game.tileInteractionsMouseOver`:轨道314→2343/床79(bottomSideOfBed 翻转)/梳妆台88三态/织布机621/茶壶464/699→5482/礼盒335/高门386-389/椅子15/蜡烛33/宝箱21·467(Containers 记录感知)/虚假箱441·468(纯图标)/传送塔597——表在 vanilla-hovericons.json
- 绘制层 `Renderer.drawCursorItemIcon`(智能光标后):门→住房携带头像独占→id 解析序(held→群系覆写→悬停 ID)→乘光→reversed→油漆子图标(刷22/滚28×0.8)→**MouseText 文本支**

**群系覆写**(else-if 序 1:1):火把 8 = 微光5353>地牢3004>神庙4388>地狱433>蘑菇5293>神圣4387>腐化4385>猩红4386>冰雪974>丛林4388>沙漠4383(表面/地下/remix 三支);营火 966 另一套(神庙在**地牢前**!)。收口批接通两旗:`temple=SceneMetrics.zoneTemple`(wall==87≡ZoneLihzhardTemple,并行会话后补的)、`desertRemix=zoneDesert && world.seedFlags.remix`(预与,原版:39661 第三沙漠兜底支)。

**收口批(08-16)**:
- 宝箱/二类箱悬停走 Containers(:34301-34367):**记录感知**——有记录→样式图标;孤儿(FindChest<0)→默认类型名文本+图标抑制(cursorItemIconID=**-1**,压掉手持物图标!)。键=LegacyChestType.0/chestType2.0(嵌套 l10n 对象,12语全有)
- 梳妆台三态(:33278-33315):锚=tx-floor(fx%54/18)/fy%36!=0上移;**下半格(fy>0)恒 icon 269**;上半孤儿→'梳妆台'文本
- MouseText 文本支(Main.cs:20032-20175 rare=0):**无面板**带影文字@mouse+14,屏幕右/下缘 40px 收边,白×mouseTextColor 脉动(FlickerClock;canvas 字+四向描边同 InfoAccsLayer 偏差登记)
- 放置建记录行重构:`tileId===T.CHEST` → `def.vanilla.sheet∈{21,467,88}`(PlaceChest:57840 CreateChest/PlaceDresserDirect:57899 同锚左上格)——vi_48_Chest 探针实证 +1
- 提取器核心陷阱:C# case 穿透共享公式段必须回填**公式对象**各自代入(床644/645/646);chairs return/result 双写法混排单函数

**遗留登记**:FlexibleTileWand 悬停弹药子图标(TryGetAmmo 第二支,offset 28)——Rubblemaker 5324/5329/5330 放置系统引擎级缺口;命名箱支(chest.name 文本)——ChestData 无 name 字段+无重命名链;vi_334 dresser 物品无 tile 字段不可放置(88 放置建记录支暂不可达,代码已预置)。

tests/cursor-item-icon.test.ts 11 条(余辉/群系序含 temple·remix/解析序/表抽查/油漆偏移/containerHover·dresserHover)。探针 scripts/_cursoricontext-probe.mjs 7 断言全绿(含真实世界宝箱 style23→1533)。**探针坑:?play=small 直载引导;玩家悬空下坠→相机漂移→悬停格滑走,须垫地板+预热 hover;protocolTimeout 600s**。收口批顺手修 StructuresPass.ts:16 顶层裸 process.env 炸浏览器加载(typeof 守卫,同 DungeonPass)。
