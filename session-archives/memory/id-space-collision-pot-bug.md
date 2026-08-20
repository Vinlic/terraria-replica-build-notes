---
name: id-space-collision-pot-bug
description: 陶罐错位 bug 根因=物品id错抄进tile sheet表(drawAdjust case 28)+完整排查方法论
metadata: 
  node_type: memory
  type: project
  originSessionId: d6caec24-1cc3-4182-bea5-29046ee459cf
  modified: 2026-08-17T08:24:01.534Z
---

# 陶罐错位 bug(2026-08-12):id 空间碰撞 + 排查方法论

## 第二案:地牢裂砖掉珊瑚(2026-08-17,用户报)
碎裂砖 481-483「会自己破裂的方块」碎裂后掉珊瑚。根因=Game.ts breakCrackedBrick 按
`sheet-481+275` 掉物品 275/276/277——275=**Coral 珊瑚**(ItemID.cs:2089)、277=三叉戟。
错读源头:WorldGen.cs:67003 的 `case 41/481/677→275` 属 **KillTile_MakeTileDust(:66744)
的碎屑 gore 槽位表**(裂砖与同色普通砖共用碎屑),被当成物品掉落表搬用。真掉落表=
KillTile_GetItemDrops(:64012,dropItem=0 起步):481-483 落 :65970-66148 无赋值 break 块
→**原版裂砖碎裂无任何掉落**。修=删掉落分支+测试改负断言(275 是 coral/277 是 trident
防再犯)。教训:同函数族里 MakeTileDust(gore槽位)/GetItemDrops(物品)/PlaySounds(音效id)
三张表挨着且 case 键同为 tile id——搬运前必须确认返回值喂给哪个空间。

触发语义复核(同日用户追问):①三点支撑门=每走廊掷一次 CrackedBrickChance=0.166
(DungeonHallSettings.cs:15)整段全裂砖(RegularDungeonHall.cs:107)——「大部分连片踩得碎
vs 孤立陷阱盖板(PitTrapTileType=裂砖)只能弹幕砸」正是原版设计;②检测窗=判定盒仅外扩
1px(num3+1 行被 Intersects 判死,只可能命中脚行);③★调用位序:原版 :27733 在
StepUp/TileCollision【前】——本仓曾挂 fixedUpdate 尾(碰撞后),空中横移(vy<1 脚底悬空)
以 vx 撞脚行裂砖场景 vx 已被碰撞清零永不触发,已迁回碰撞前+真跑 fixedUpdate 的位序
回归测试。检查类钩子挂错 Update 段位=读到的速度是"碰撞残值"而非"帧初速度"。

## 根因
`VanillaTiler.drawAdjust` 的 switch 以 **tile sheet id** 为键,我却把 **Player.cs 手持物品贴图的 14 相位动画组**(case 28/105/470/719,sy+=270×(t%4)、sx+=288×(t/4),t=(x+y+tick/4)%14)错抄了进去。**sheet 28 = 陶罐(Pots)**,被劫持后:
- 源 Y 加 0/270/540/810 随位置+时间变化 → 错位
- sx+288 超出 108px 表宽 → 边界检查 return → 随机空格
- 开门关门触发 chunk 重建,tick 相位不同 → 错位形态变化("变化后仍错误")

**Why**: 三个 id 空间共用 0-753 的数字:tile sheet id / item id / NPC id。从反编译源码搬 case 组时必须先确认它属于哪个 id 空间。见 [[js-bitwise-int32-traps]] 同类的"数字撞车"教训。

**How to apply**:
1. 搬运原版 switch case 前,先看该 switch 的 dispatch 变量是什么(GetTileDrawData→tile sheet;DrawItem→item id;DrawNPC→NPC id)
2. drawAdjust/vectorOffset/tileTopCond 三个表都按 sheet id 键,case 值必须逐一回源码核对"这是 tile 吗"
3. 用户报"错位且随交互变化"= 源矩形被运行态变量污染(tick/位置/风),优先查帧源调整函数

## 排查方法论(此案实证有效的顺序)
1. **先离线验证数据层**:解码存档 RLE 检查帧是否规整(本案 15984 格全对,排除数据层)
2. **算出期望像素基线**:从素材 PNG 离线算期望帧的不透明像素数(本案 [112,48,172,140]),没有基线就无法判定"错"的程度
3. **E2E 互相关测位移**:chunk 像素 vs 期望帧 ±6px 平移搜索,量化"错位"
4. **同一会话多次重建对比**:证明烘焙非确定性(排除静态管线 bug,锁定运行态变量)
5. **逐层打桩二分**:vframeAt 调用与返回 → drawImage 实参 → 画后回读;发现"取帧正确但最终绘制参数错"= 中间层污染
6. **中间层二分收网**:在取帧后/重排前/绘制前三点各埋一行探针,一次同场捕获 → 一次定位到 drawAdjust

## 排查中的弯路(避免重蹈)
- 过滤正则写错(空格分隔 vs 逗号)导致"0 命中"误判为"没烘焙"——探针过滤条件要先用已知会命中的样本验证
- 探针盯旧 canvas(invalidateAll 换新画布后补丁失明)——重建型目标要记录 canvas 标签而非引用
- HMR 整页重载杀探针状态——探测脚本要有重试循环 + 稳定窗口等待(__swGame.renderer && chunks 都在)
- monkey-patch import 的模块可能拿到 HMR 双实例——验证同一性(cc.autotiler.atlas === renderer.atlas)或直接源码埋探针(最快)
- 高负载下浏览器世界生成 >10min——用 __swLoadJson 加载现成存档(秒级)替代生成新世界

## 调试桥(本次新增,保留)
- `__swTileByKey(key)` / `__swTileDefById(id)` / `__swLoadJson(text)`(mainFlow,菜单阶段可用)
