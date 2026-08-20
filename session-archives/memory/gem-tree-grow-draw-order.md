---
name: gem-tree-grow-draw-order
description: GrowTreeWithSettings 两处掷骰偏差(基座帧骰无条件/帧变体先于枝型)——shimmer 金标 2026-08-14 暴露并修复;GrowTree 与 GrowTreeWithSettings 掷序相反勿互搬
metadata:
  node_type: memory
  type: project
  originSessionId: 04569a63-44aa-4669-98a3-b777d15e98f8
  modified: 2026-08-13T16:34:02.398Z
---

2026-08-14 微光链 C# oracle 金标(tools/golden/caves-oracle.cs Shimmer 段 + tests/shimmer-checkpoint.test.ts)暴露 TreePass.growTreeWithSettings 两处掷骰偏差,已 1:1 修复:

1. **cs:30906 基座干身帧骰无条件掷**:`num5 = genRand.Next(3)` 在 vanilla 是无条件掷,帧写才受 flag4/flag5(tL/tR)门控(cs:30907-30959)。旧实现把掷骰内嵌 `if (tL || tR)`——两侧 tuft 全 false 时每棵成树**少掷 1 骰**(以太腔石地恒如此;灰烬草基座也常发生),500 采样流整体漂移。修法:骰子出 if,帧写按 tL&&tR→fx88 / tL→fx0 / tR→fx66 三分支。
2. **cs:30595-30596 干身掷序:先帧变体 Next(3) 再枝型 Next(10)**。旧实现枝型先掷——两骰都无条件(总数同)但枝型取自不同流位 → 枝型/重投序列漂移(同高同枝数的成树 reroll 计数对不上,流随后分叉)。**GrowTree(growTrunk cs:14213 起)顺序相反(枝型先)**——两个函数语义不同源,勿互搬。

**连带**:caves-oracle.cs 的 GrowAshTree/GrowGemTreeFn 转录同两处同步修正(oracle 与 JS 必须同态,否则 caves-chain underworld 检查点假红);修复落地后 **caves-chain-*.json 金标必须重生成**(underworld 起全部哈希变,2026-08-14 已重生成)。

**教训**:「两骰都无条件掷」不等于掷序无关——骰值进分支判定(枝型/重投)时,序即语义。对账工具:RNG 流位置指纹(UnifiedRandom SeedArray[56]+inext 的 FNV,oracle StreamHash/JS streamHash 同算法)比网格哈希更早定位分叉点;oracle SW_DUMP_SHIMMER 状态恢复通道可把单个 pass 从全链隔离裁决。

相关:[[shimmer-audit-status]] [[vanilla-worldgen-passes]] [[seed-equivalence-plan]]
