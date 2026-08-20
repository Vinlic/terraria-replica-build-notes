---
name: cracked-brick-chain-port
description: 地牢裂砖481-483全功能对齐:生成端16.6%走廊+坑陷阱+noFail秒挖+爆炸可毁已有;破坏后果五链补齐(掉同色砖/连锁崩塌上1/3侧1/6/Debris弹片736-738伤20/跑落撞碎/弹幕扫掠碎);钩爪抓碎早已实现
metadata: 
  node_type: memory
  type: project
  originSessionId: c44574b3-7d4d-403b-8e39-61a13d11a1c6
  modified: 2026-08-14T02:39:32.711Z
---

地牢裂砖族（481-483，随地牢主题蓝/绿/粉）功能全链对齐（2026-08-14，用户："检查我们的实现是否完全一致对齐了？感觉是不是不太对"——审计证明确有缺口）。

**原版功能定性**：肉前合法"挖穿地牢"的薄弱墙+塌陷陷阱。普通地牢砖 41/43/44 需 65 镐力，
裂砖 minPick=0+tileNoFail=铜镐秒挖。生成端：每条走廊 16.6% 整条用裂砖
（DungeonHallSettings.cs:15）+ 坑陷阱盖板（DungeonPitTrap，isPitTrapTile）。
Zenith 种子全隐形（:1224）；醉世界与地牢砖同组染色。

**审计前已有**：实心通行（[[tile-passability-audit]]）/16.6% 裂砖走廊（DungeonPass:409）/
坑陷阱 dgPitTrap/noFail 秒挖（TILE_NO_FAIL_SHEETS）/爆炸可毁（EXPLODE_NEVER 无 481-483）/
腐化不可替换（CorruptionPass:49）/钩爪 1/16 抓碎（GrappleProj:130 已 1:1 :49666——审计时
grep "CrackedBrick" 未中因其命名 CRACKED_BRICK_SHEETS）。

**本批补齐五链**（原版有我们没有）：
1. **掉落**：碎裂砖掉同色普通地牢砖（:67003：481→275/482→276/483→277）——breakCrackedBrick
   内做（tiles.ts drop 保持 null 防通用路径幽灵掉落）。
2. **连锁崩塌**（KillTile :63837-63883）：8 邻掷签——正上 1/3（num17/2）、其余 1/6，
   KillTile(noItem) 递归链；纯函数 `src/world/CrackedBricks.ts` crackedChainKill
   （被杀格 type=0 天然防重入；连锁格不掉落防雪崩刷物资）。
3. **Debris 弹片**（:63887-63895+7466+Kill :75336-75360）：每块碎砖喷 proj 736-738
   （伤 20、v=(0,0.41)、10×10、击退 6）；`src/entities/DebrisProj.ts`——落地 Kill：
   Item_127+3 尘+中心下格裂砖 1/2 掷 KillTile（掉落）。
4. **跑/落撞碎**（Player.cs:23040-23110 CheckCrackedBrickBreak 1:1，Player.ts
   checkCrackedBrickBreak 挂 fixedUpdate 尾）：速度门 |vx| 或 vy > rand(2,12)；
   **vy<1 时脚底三点任一"实心非裂砖"→不触发**（站普通地跑不算，须跳/落撞）；
   num3=**当前**脚行（position.Y 非 y+vy）+Inflate(1,1) 盒相交才命中；命中压 vy→1；
   破坏区=预测位横 ±24px、脚行至 +2 行。
5. **弹幕扫掠碎**（HandleMovement :16630-16655，Game.crushCrackedBricksSweptByProjectiles
   挂 entities.update 后）：移动扫掠盒内裂砖 KillTile——**所有弹幕**飞行路径切碎裂砖；
   CanCutTile 门（墙 350/正下 78·380·579 豁免）；DebrisProj 自身豁免（快照长度迭代）。
6. 专属音 Item_127（:66551 每块碎都播）。

**测试**：tests/cracked-brick-chain.test.ts 10 条（连锁全中/全不中/非裂砖不传染/映射/弹片
构造+落地两掷/撞碎砸穿+普通地不触发）+ cracked-brick-solid 3/3。撞碎用例坑：玩家须贴
平台 ≤2px（Inflate 后盒底才与行顶相交）。

**未做（备案）**：Zenith 隐形彩蛋（种子系统未引入）；ExplodeCrackedTiles 与我们 explodeAt
毁环的形状差异（圆形 vs 方形，语义等价面已覆盖）；DebrisProj 重力 0.3 为 aiStyle 10 近似。
