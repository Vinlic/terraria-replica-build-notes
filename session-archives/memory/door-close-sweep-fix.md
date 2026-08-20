---
name: door-close-sweep-fix
description: 开关门切掉旁贴工作台/墓碑半边=closeDoor三列无差别清扫;原版只动type==11开门格;T表是legacy id空间
metadata: 
  node_type: memory
  type: project
  originSessionId: c212e38d-8db4-446d-b3da-4e20d707caf7
  modified: 2026-08-14T10:52:53.924Z
---

2026-08-14 用户报"开关门把工作台半边贴图切没/墓碑同理"(疑渲染重绘缺失——**不是**,是数据层抹格):

**根因**:`closeDoor` 清扫区 `sweepL=min(closedX,x-1)..sweepR=max(closedX+1,x+1)` 曾对区内**所有格**无条件 `setTile(0)`。场景:门朝空侧开(开门格在门柱+空侧两列)→ 关门时 sweepR=x+1 越过门自身列,把旁贴家具那列(工作台锚/墓碑半边)**直接抹掉**——渲染如实画"半边消失"。

**原版语义**(CloseDoor :32037-32057):两列循环里 **`tile2.type == 11`(开门格)才动**——关列转关门型+新 frameX(变体 rand3),其余开门格 active(false);**绝不触碰非门图格**。修=清扫加 `st.get(sx,ay+dy)===T.DOOR_OPEN` 门。

**验证**:tests/door-furniture-guard.test.ts 3 条(工作台/墓碑全周期无损+朝家具侧开门仍拒绝)。locked-door-chain 5/5 回归绿。

**三个方法论点**:
1. 用户猜"渲染重绘缺失"时先无头复现数据层——本例数据层开门方向正确、关门抹格,渲染只是忠实受害者。
2. `T` 表(tiles.ts:28)是 **legacy 本地 id 空间**(WORKBENCH:13/DOOR:17)——恰好与 vi_ 内部 id 对齐纯运气,写测试勿依赖 `T.WORKBENCH` 语义,用 `TILE_BY_KEY`。
3. 门帧行内步进 **18**(0/18/36)非 54——测试摆门用错步进会让锚点扫描行为变形(54 是样式行步进)。
