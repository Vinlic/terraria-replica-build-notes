# 液体缓冲器回灌双重错位 + TileFrameImportant 165/91（DDDDD 批 2026-08-19）

- **根因一（主）**：LiquidBuffer 回灌（Liquid.cs:1134-1148，1405 双版一致）——
  回灌量 = `curMaxLiquid-(curMaxLiquid-numLiquid)` = **numLiquid**（当前活动数，
  非空余量）；`DelBuffer(0)` = **swap-remove**（尾元素补头位，出序 A,C,B… 非
  FIFO）；顺序 = 清 checking → AddWater → 后 DelBuffer（满载时同格空转）。JS 曾
  FIFO 环形 + 空余量上限 → 中世界（6400×1800）r0 唤醒链首触 24999 帽后回灌时序
  整体漂移 → 全图 475 条湖面薄膜高度全漂（#49 L=11,707）。小世界永不触帽 = 三条
  小链 #49 长绿的假象来源。修 = bufCount + 尾接 + swap-remove（O(1)）。
- **根因二**：YYY 级联 tileFrameGen 缺 165→CheckStalactite / 91→CheckBanner
  派发（蛛网水死表杀的 3×3 帧扫触发组拆）——UpdateStalagtiteStyle style≠desired
  耗 Next(3) 走 pass 链流；CheckBanner 锚门 tileSolid≈solid||platform 近似。
- **连带战果**：#53 Smooth_World 旧 Hf/Sl 半砖债全系 #49 薄膜液体差下游——液体
  对齐后整段消失；m/s 链首差 #49→#58（Statues 域新暴露）。
- **附带**：#49 pass 头 oceanDepths 归水扫（cs:16222，唯 #49 有——#97 无，
  QuickCleanup 自有窗口版）settleWorldLiquids +oceanStrip 参接线。
- **方法论**：独立重放器（golden 8 通道 + JS frame/wire/GenSolid 界 + RNG(seed)
  pass 流）复现自差 → 连通域聚类（475 条单行薄膜=全局调度差指纹）→ 阶段化重放
  （薄膜全在 r0 成形 + numLiquid 顶帽监测）→ 缓冲器介入实锤。
- **教训**：「账面 1:1」的模块在容量边界路径（curMaxLiquid 帽、49998 帽）可能藏着
  从未触发的分支——大尺寸世界是天然的压力测试；调度序差在混沌系统（薄膜圆整漂移）
  里呈现为"处处轻微不同"而非单点错位。
