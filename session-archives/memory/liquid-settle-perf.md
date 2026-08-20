---
name: liquid-settle-perf
description: 液体沉降 12-20× 零风险提速:buffer 头指针队列(曾 O(n²) 主热点)+实心 LUT;冻结快照 A/B 逐字节闸门法
metadata: 
  node_type: memory
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-12T16:41:07.980Z
---

2026-08-13 用户报"正在安置液体"耗时过长(settleWorldLiquids 单次 22-56s,种子敏感)。零风险约束下完成 ①② 两项,单次沉降 10.2s→0.5-0.9s(冻结快照口径)/用户体感全程大幅缩短。

**①buffer 头指针队列(LiquidSim.ts)——主热点**:`Array<{x,y}>.shift()` O(n) × 万次回灌 = O(n²)。改定长 Int32Array 对+head/tail。**踩坑:初次实现漏了 compact——定长到顶后越界写被 typed array 静默丢弃,与原版"shift 后可重新装满"容量语义不等价**,A/B 哈希当场报警;补 `if (bufTail===CAP && bufHead>0) copyWithin 前移` 后逐字节一致。
**②实心 LUT**:构造时用原判定式逐 id 预计算 `solidNP`(solid&&!platform),blocksLiquid/solidTileFull(后者叠加格级 half/slope,不可整体预计算)/addWater/waterCheck 四处换表。TILE_DEFS 构造后不变,定义同源零风险。
**跳过**(无 measurable 收益,不强推):③liquids SoA ④热循环局部化——阶段剖析(quickWater 94ms/waterCheck 21ms/rounds 563ms@1022iters/finalCheck 53ms)显示剩余成本在 updateLiquid 单格逻辑,改动面大收益边际;⑤sqrt→整数平方(shimmerRemoveWater 仅 2 次调用)⑥yield 32→64ms(总量已 <1s)。

**验收方法论(可复用)**:
- **冻结快照 A/B 闸门**:生成一次世界→type/flags/wall/liquid/liquidType/half/slope 落盘 /tmp→分别跑优化前/后代码的 settle→四数组 fnv1a 必须一致。**为什么必须**:并行会话实时编辑 worldgen,跨运行整管线哈希连 type/flags 都漂,无法直接比对;冻结输入把变量隔离到 LiquidSim 单文件。
- 永久回归:tests/liquid-settle-golden.test.ts(自包含合成夹具:水/岩浆/蜂蜜/微光四腔+脱水路径,golden `f4f6614e d6806ecf b6f70ec5 e84ee6b5`)——此后 LiquidSim 任何改动破坏该哈希即被拦截。
- 旁证:pass-hash/world-final-hash(9293480)绿;caves-checkpoint 10 失败与 world-final-hash 1511931452 失败均经 **git stash A/B 证实为并行会话 WIP**,与本轮无关。

**教训**:① typed array 定长队列必须处理 compact,越界写静默丢弃不报错——A/B 字节闸门是唯一可靠防线;② 阶段计时先行,避免对 SoA/局部化类大改动面优化做无用功。

相关:[[vanilla-liquid-port]] [[perf-audit-2026-08]] [[diag-script-orphan-prevention]]
