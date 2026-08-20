---
name: platform-standable-framey-fix
description: 平台站立穿透根因=把家具 frameY==0 门错套到平台族;原版 tileSolid∩tileSolidTop 四件套 frameY=材质行与站立无关
metadata: 
  node_type: memory
  type: project
  originSessionId: d76053b3-a9fb-4d75-a43d-41f181c7cab5
  modified: 2026-08-17T07:15:40.951Z
---

# 平台站立穿透修复(2026-08-17)

用户报"很多平台角色站上去只会往下掉(木平台)"。根因:`TileStore.isPlatform` 的
`d.platform && frameY===0` 把**家具族的底行门**(Collision.cs:2331 的
`tileSolidTop && frameY==0` 补门,家具 tileSolid=false 靠它接落)错套到**平台行为族**。

## 原版权威语义(1456=1405 一致)

- `tileSolid[19]=true` **且** `tileSolidTop[19]=true`(Main.cs:7841-7842)。
  TileCollision :2330-2333:`flag = tileSolid[type]` → 平台恒真,frameY 无关;
  `if (tileSolidTop && frameY==0) flag=true` 是给家具的补门。
- 平台**材质在 frameY**(`PlaceTile case 19/380: frameY = 18*style`,
  WorldGen.cs:60245),**连接形态在 frameX**(TileFrameImportant :86232 重写,
  27 变体列:0两连/18左连/36右连/…/斜坡族)。Tiles_19 486×1260=27列×70行实证。
- 平台行为族 = tileSolid∩tileSolidTop = **{19 平台, 239 矿锭, 380 花盆箱, 427 团队平台}**
  (Main.cs 实测提取)。恒可站、可 fallThrough 下穿;X 轴/上顶不拦(消费端豁免)。
- 单向豁免在原版靠 X 轴 :2425/:2444 与上顶 :2449 的 `!tileSolidTop` 门,不是 isPlatform。
- 各消费点门不同:StepUp holdsMatching(:3713)=`(solidTop&&frameY==0)||Platforms(19/427/
  435-439)||380`(**不含 239 矿锭**);StepDown 落面(:3614)=solidTop 不查帧;
  SolidCollision acceptTopSurfaces(:2771) 平台族走 PlatformProperTopFrame(frameX)。

## 修复落点

- `TileStore.isPlatform`:sheet∈{19,239,380,427} 恒真(忽略 frameY);家具族保留 frameY===0。
- `TileCollision.applyStepUp` platAt 排除 sheet 239(原版 StepUp 门不含矿锭)。
- `FurnitureStyle.furnitureStyleBase` 补 case 19/380 `[0, style*18]`——玩家放置端曾落
  default 把材质误写进 frameX(木平台 style 0 碰巧无症状,非 0 材质贴图错位)。
- 测试钉死:tests/tile-passability.test.ts"平台材质行可站/矿锭花盆箱恒可站/家具上排仍不可站"。

## 教训

- 世界里 platform fy 分布探针(_platscan)是定位关键:2002 块只有 159 块 fy0 可站,
  fy234×1009(洞穴小屋随机材质)全穿透——现象与"很多平台掉下去"完全对应。
- 探针放置玩家须留足高度:玩家 h=42px,放平台上 2 格脚会嵌进平台行 10px,
  单向平台门(上一位置在平台之上)天然不满足,是假穿透。必须 ≥3 格。
- 页面 evaluate 里模块级表(TILE_DEFS/TILE_BY_KEY)不可达,用
  `await import('/src/data/tiles.ts')`(vite 直接伺服 TS)——_cactus3 等探针同款。
