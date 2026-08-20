# MossPass #65 四连根因清零（MMMMM 批 2026-08-19）

9293480 链 #65 Moss（T=1170/W=444）→ 八通道全零+掷流 54007=54007 逐条全等；首差 #65→#69。

## 四根因（全 pass 自差——golden64 基座反事实 100% 复现）

1. **霓虹洪水 repeat=false**（vanilla cs:9800 缺省 true）：只转单格不递归洪水；
   零 RNG 差但 countTiles rockCount 分歧滚成掷流错位（span 首差@604=patch 段
   vanilla 多一次重掷）。
2. **Spread.Moss 出列端误去重**（cs:3509-3561）：原版去重在**入队门**（hashSet=
   已出列格），出列端无跳过——同波重复入队的格处理两次，次访走 wall!=0 支把
   **坡/半砖石头换苔藓**（dump64 slope/half≠0 实证；签名=T179>1 ow=54 iw=0）；
   JS 出列端 seen.has→continue 吞次访 → 坡半砖石漏转+尾段洪水种子缩水。
3. **暴露段动态上限截断**（cs:17720-17731 原版无上限）：`iter<budget*500` 的
   budget 随命中递减→上限收缩提前出循环（实测 197/211 命中、剩 13 预算）→
   掷流滚进地狱段（T381 族×218 错位）。修=定值保险丝 1e7（真世界 ~7500 迭代；
   "命中率 1-5%"旧估值错一个量级，实际 ~1/35）。
4. **SpreadGrass enclosed/SolidTile 读静态实心表**（cs:75251/cs:70160）：tileSolid
   是生成期可变表——Moss 窗口期 **225 蜂巢块=非实心**（LifeCrystals 尾 cs:16944
   翻 false、Piles 尾 cs:19591 还原；s19 GenSolid 快照实证）→ 蜂巢贴面石头
   （ow=64 族）尾段洪水漏转。修=MossPass.isSolidTile+Spread.ts enclosed 两处走
   `vanGenSolidType`（消费端 #73/#79 零副作用实证）。

## 方法论

- 双侧 span 对拍：tttt-app 织入 `SW_TT_SPAN_PASSES=Moss`（'d' 不录）× JS
  `_wwwrep` SW_WWW_SPAN_OUT（滤 d/n）——修前@604 定位、修后 54007 全等终审。
- 残差分类画像（ow/iw/it 三元组）快指段来源：ow=54=patch BFS 空气支、ow=iw≠0=
  BFS 固体支存量墙、ow=0=scatter/exposed/hell；enclosed 格=洪水不可达=查生成期
  tileSolid 翻转。
- **W=0 但 T≠0 时查"无墙写的转换"**（scatter/BFS 固体支）；**A/T 首差格不变仅值
  变**=既有债带内值演化（非新回归）。

## 遗留

新首差 #69 Floating_Island_Houses（IslandHousePass 域）；s22222 #59 Buried_Chests
2 格=JJJJJ 并行在途（本批代码 dump 65/73/79 前零执行，mtime 19:12/19:18 实证）；
m20260811 #59→#62 改善（JJJJJ 落定）。报告：docs/worldgen/content-parity-vs-
vanilla-2026-08-16.md「MMMMM 批」章。
