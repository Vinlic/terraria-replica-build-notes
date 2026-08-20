---
name: dungeon-entrance-plug-fix
description: "地牢塔→地下通道被砖堵死根因:塔挂载点自制gY地表扫描+7×7兜底竖井,1456实为挂hall出口位;附带4处对齐修复与BFS探针方法论"
metadata: 
  node_type: memory
  type: project
  originSessionId: d76053b3-a9fb-4d75-a43d-41f181c7cab5
  modified: 2026-08-13T08:47:47.155Z
---

# 地牢入口堵塔修复(2026-08-13)

用户报:地牢塔楼通到地下地牢的通道被地牢砖堵死(种子12345,52行实心段)。

## 根因(与原版机制差异,1456 权威链:DungeonCrawler.cs + LegacyEntranceDungeonHall.cs + LegacyDungeonEntrance.cs + DungeonUtils.cs)

1. **塔挂载点(根因)**:原版 `GenerateEntrance(data, generatingDungeonPositionX/Y)` 直取爬升 hall 末尾写的出口位置;塔底(num6≈j+10..18)构造性压住末段挖空框(val±num2*0.5,竖向重叠≥3行)→ 连通是构造保证。我们曾自制"首实心列扫描 gY 吸附地表 + 扫不到则 7×7 直挖竖井兜底":山丘地形下塔吸到山顶、楼梯口还在山下,塔体下延整段刷砖把塔底与竖井口间岩层灌死 → 堵塔。修复=删 gY/兜底,塔挂 (dx,dy)=hall 出口(DungeonPass.ts 爬升循环)。
2. 楼梯中线钳制:1456 非 skew=左 `vx<-0.5→-0.5`、右 `vx>0.5→翻-0.5`;skew(Next(4)==0,1/4 世界)=左翻+0.5。1405 同处是冗余反编译条件,以 1456 为准。删自制 dungeonLocation±60 回拉。补 InWorld(余量35)步内断。循环上限 99(num3=100 先减后断)。
3. 塔强度须复用 dc.dxS1/dyS1/dxS2/dyS2(LegacyDungeonEntrance 读 data.dungeonEntranceStrengthX/Y,MakeDungeon 掷一次与 hall 探测偏移同源);曾重掷。外门厅段同。
4. 塔下延起点=塔顶 t1(非塔底 b1);1456 无塔底井口刻槽(自加的 3×4 已删)。
5. `Main.dungeonX/Y` 生成期唯一写入端=DungeonUtils.cs:1665 SetOldManSpawn(外前厅0.5框底部);WorldGen.cs:72510 是运行时兜底 setter 勿引。我们 world.dungeonX/Y=entStand(老人位)语义一致。

## 探针方法论(scripts/_dungeonconn.mjs,保留)

- **列扫描最长实心段会误判斜井**;连通性证明用 BFS:从 world.dungeonX/Y(老人位)4向灌水,门 tile 可通行(内部 id **17关/18开**,tiles.ts:34,非原版10/388/389),断言=最深"地牢墙开放格"(墙7-9/94-99,天然洞穴没有)≥rockLevel-80。
- 种子控制走 `window.__swFlow.newWorld(seed,4200,1200)`(旧 select+button 垫片是空种子随机)。worldgen 跑在 worker,`globalThis` 调试 trace 要从 `page.workers()` 逐个 evaluate 取。
- 修复后 4 种子(12345/9293480/20260811/2147483647)9 PASS/0 FAIL。

关联:[[vanilla-worldgen-port-status]] [[parallel-vite-sessions]]
