---
name: dungeon-furnish-parity-batch
description: 地牢陈设四症状修复批:灯线dgSwitch走线+灭档/灯笼吊灯宝箱帧公式/isLockedDoor内部id陷阱/openDoor砍切/AreaOr语义
metadata: 
  node_type: memory
  type: project
  originSessionId: 1fc2b821-952a-4ed1-9b75-6e99198205af
  modified: 2026-08-13T15:02:42.236Z
---

2026-08-13 地牢陈设审计批(seed 12345 探针 tests/_dungeon-furnish-audit*.test.ts):

**修复**(DungeonPass.ts + Door.ts + tiles.ts):
- **dgSwitch 灯线**:原版 Lights_GenerateSwitch(DungeonGlobalLights.cs:159-194)= L形红线逐格铺(含开关格不含灯格)+2/3 灭档 frameX=18 绝对写。修前 0/16 开关有线→修后 9/9。
- **灯笼帧**:Place1x2Top(:46694) frameY=style*36(+18 下格)/frameX=0;样式按墙变体三档(wall==variants[1]/[2] 换档,lantern[] 数组 precomputed)。
- **吊灯帧**:PlaceChand(:52753) style=27+theme(Item.cs:25748 `27+type-2652`,2652/53/54 蓝绿粉);页列 num2=108*(style/36)、行基 num3=style*54。亮灭=整块 frameX±54(每页108px 前三列亮后三列灭,ToggleChandelier)。
- **宝箱帧**:PlaceChestDirect(:57864) 顶行 fy=0/底 18、列 fx=36*style/18+36*style;地牢普通箱 style2(fx=72)。
- **isLockedDoor 陷阱**:曾写 `st.type[i]===10`——10 是原版 sheet id,TileStore 存内部 id(门=17)恒 false→神庙锁门无钥匙可开。改 T.DOOR_CLOSED+tests/locked-door-chain.test.ts。
- **openDoor 砍切**:原版(cs:37698-37724)侧列允许 tileCut/165/IsADripTile(373/374/375/461/709)并 KillTile;我们曾要求全空→蛛网堵门。tiles.ts doorSmashable()。开门 11/16→13/14。

**原版行为考**(勿误修):
- 地牢门 style13=地牢门(item1138)普通门;16/17/18=蓝绿粉;锁门仅神庙 style11(fy594∈IsLockedDoor[594,646])。
- FindSideExit 的 AreaOr(4,3)=**任一格**非实心即可(GenCondition.cs:40-52)——出口检查本就弱,门侧石头是原版包络。
- Bast 雕像 x=`Next(2,W-2)+X` 且 forced:true——贴门可能原版同样存在。
- 起爆器411+炸药桶=MicroBiomesPass 爆炸物群系,可刷进地牢。

**遗留**:"诡异装饰物"已破案=**DG_ITEM_TILE id 空间碰撞**(DungeonPass 表直存 sheet id,placeSimple 裸写 st.type:落地钟104→活木/蜡烛33→猩红矿/灯93→氙苔/椅15→铁砧/烛台100→石板/书架101→熔岩苔)。修复=源头 TILE_INTERNAL_BY_SHEET 换算+place4x2 去双转换;插桩验尸法(setLivingWood trace 零命中锁定非树写入)。placeSimple 仍单格放置(原版 PlaceTile 整件)留家具重构批。TILE_CUT_SHEETS(tiles.ts)与 Game.ts TILE_CUT_VANILLA 双副本待合并。移交单 game/docs/dungeon-furnish-handoff-2026-08-13.md。

**环境坑**:vitest≥4 吞 console.log 须 --disable-console-intercept;负载130时全管线测试超时须 --testTimeout=400000;DungeonPass/WorldGen 是并行会话活跃战区,改前必 stat mtime,Edit old_string 冲突即对方在改同段。相关 [[dungeon-entrance-plug-fix]] [[chest-index-frame-bug]] [[vanilla-door-frames]]
