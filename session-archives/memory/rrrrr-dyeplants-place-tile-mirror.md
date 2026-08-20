# RRRRR 批：#84 PlaceTile 头尾镜像 + #90 Check3x2 堆级联 + #86 掷流谜案

（2026-08-20，9293480 首差 #84→#85，详见 game/docs/worldgen/content-parity-vs-vanilla-2026-08-16.md RRRRR 章）

## #84 Dye_Plants Hf/Sl 全清 = PlaceTile(227/656/752) 头尾两段镜像

- 13 格 active 半砖 → 头段 else-if 支：`ResetsHalfBrickPlacementAttempt[num]`
  （TileID.cs:181 **默认 true**，CreateBoolSet(true, 例外表)——例外表={2,23,60,70,
  109,179-183,381,477,492,512-517,534-537,539-540,625-628,633,661,662,199}）
  && 活性非 frameImportant → halfBrick(false)+帧归零（坡保留）。StatuesPass 先例同款。
- 1 格幽灵 slope → 尾奏 SquareTileFrame（case227 恒调 cs:60068 + 活性再调
  cs:60283）→ **TileFrame 头 cs:82078-82：非活性格 half/slope/漆清、幽灵 type
  保留**（与头段 Clear 的 type 全清相区分——判定是哪段的判据）。
- 失败尝试同样清场（预清场族）；656 在液体拒置表（先于清场拒）；488 倒木守卫
  零副作用最先行。JS 落点=SurfaceDecorPasses placeTileHead+squareTileFrame 共用。

## #90 Flowers 残差 = killTileTree 杀链缺 Check3x2 堆级联

杀 3×2 堆（186/187）任一格 → 帧结构破 → 整堆六格杀。杀后 destroyObject 复位
**5×5 复扫**（cs:49856-62 连锁邻组）；底材质按样式列⌊fx/18/3⌋分档；
SolidTileAllowBottomSlope **越界=真**（cs:70214）。QQQQQ Spread.ts 有同源
check3x2PileFull（其 187→186 降帧支读中心格帧系近似——vanilla 读堆左上格）。

## #86 荆棘翻转谜案（备案移交）

JS 与独立模拟逐掷一致（3735 掷零分歧）但 golden 需 +3/+5 掷偏移注入
（roll<1404 任意点，二分界 R*=1404=check#22 Next(13)）才 8ch 全等——pass 内
全部机制+邻帧派发全族零掷已排除；嫌疑=金标 85 边界织入侧多耗掷（蜘蛛探针
时代残留）——需重产金标或织入源审读定谳。

## 教训

- 草药/染料 pass 残差先查 PlaceTile 头（半砖/幽灵）与尾帧链（TileFrame 头
  非活性清位）两段——"槽末两侧等同+pass 内消失"是这两段的指纹。
- mile8 反事实 replay 的 T 差未必真债：成熟草药 82→84 升级读 frameX（陈旧
  边界帧→伪差）——全链 delta=0 才是裁决。
- 四链回归 env：12345/s22222 须 SW_M8_EVIL=1（evil=0 误现 #26 邪矿带=
  已知非回归）；m20260811 须 SW_M8_W=6400 SW_M8_H=1800 SW_M8_NOCACHE=1。
