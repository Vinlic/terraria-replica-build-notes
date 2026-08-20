---
name: vine-cascade-port
description: 藤蔓支撑级联CheckVines移植:打中间节下方整段消失;IsVine八族同构;亲代面变型+支撑白名单
metadata: 
  node_type: memory
  type: project
  originSessionId: d76053b3-a9fb-4d75-a43d-41f181c7cab5
  modified: 2026-08-18T04:43:25.099Z
---

# 藤蔓支撑级联 CheckVines 移植(2026-08-18)

用户问"打掉藤中间一节,下方会不会消失"——**原版会**:CheckVines
(WorldGen.cs:85599-85700,TileFrame 入口 :82114 对 IsVine 全族逐格):
- 上方非同型藤且非亲代面 → `KillTile(i,j)` 整格消;KillTile 尾部 SquareTileFrame
  3×3 → 下方藤再查 → **级联到藤底**。
- 上方是异族亲代面 → **变型**成对应藤(52 挂丛林草→62)。

## IsVine 八族(TileID.cs:237)与亲代/支撑表

| sheet | 藤 | 变型亲代面(:85630-85655) | 支撑白名单(:85661+) |
|---|---|---|---|
| 52 | 普通藤 | {2,52,477}(type≠382) | {2,477,192} |
| 62 | 丛林藤 | {60,226,62} | {60,**384 活红木叶**,226} |
| 115 | 神圣藤 | {109,115,492} | {109,492} |
| 205 | 猩红藤 | {199,205,662} | {199,662} |
| 636 | 腐化藤 | {23,636,661} | {23,661} |
| 382 | 神圣花藤 | {382} | {2,477,192} |
| 528 | 蘑菇藤 | {70,528} | {70} |
| 638 | 1.4.5 新藤 | {633,638} | {633} |

上方格取型条件:nactive && !bottomSlope(slope 3/4 排除)+同型续接先于一切。
num==-1(上方非活)恒死。变型集与支撑集**不同**(62 的 384 在支撑不在变型)。

## 本仓实现

- `Game.checkVineAt(i,j)`(CheckVines 1:1)+ 监听
  `onTileChanged((x,y) => checkVineAt(x, y+1))`(下落沙同款);级联靠
  breakTile→setTile(0) 再触发监听逐节向下,天然递归。
- 变型走 `VINE_INTERNAL_BY_SHEET` 反查内部 id + setTile(触发下方再查,
  等价原版 3×3 帧化)。
- 生成/导入期 setTileSilent 不触发 → 生成端挂藤零扰动。
- 测试 tests/vine-cascade.test.ts 五例(中间级联/顶草全灭/52→62 变型/
  蘑菇藤白名单/384 支撑);端到端探针:9 节丛林藤打第 2 节 → 下方 7 节全灭顶节留。

## 教训

- "水草"类垂挂物(蘑菇藤 528 发光藤)与丛林藤同构——查机制先找 TileID.Sets
  家族集,不逐个猜 tile。
- onTileChanged 事件驱动级联是本仓先例模式(火把掉落/下落沙/藤三级);
  新"支撑类"tile 语义照此接。
