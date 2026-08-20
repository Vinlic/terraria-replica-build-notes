---
name: cloud-parity-fill-attempts
description: 云量偏多根因=resetClouds重试凑满而非恰numClouds次尝试；AABB拒绝即少一朵是原版云量调节器
metadata: 
  node_type: memory
  type: project
  originSessionId: 04569a63-44aa-4669-98a3-b777d15e98f8
  modified: 2026-08-19T10:13:23.260Z
---

云朵对齐批（2026-08-19，用户实报"云量似乎有点过多了"）：

- **主根因**：原版 `Cloud.resetClouds`（Cloud.cs:39-59）= 恰 `numClouds` 次 addCloud 尝试，
  AABB 重叠拒绝即少一朵（拒绝还消耗尝试）。本仓曾 `while (length < target && guard++ < 400)`
  重试凑满——离线模拟（真实云贴图尺寸表 + RSA 随机排布）1920×1080/目标100 档：
  原版 ~46 朵 vs 本仓 ~77 朵 = **1.7 倍偏多**；2560×1440 档达 2 倍。修=改为恰 target 次 for 循环。
- **次修三件**（Cloud.cs addCloud/Update 缺失行为）：
  1. X 锚 `num2 = windSpeedCurrent − player.velocity.X*0.1`（:96-100，!gameMenu）——
     顺风缓冲侧 ±200 随玩家速度翻转（frameCtx.player.vx 注入）。
  2. 恰界 scale 微移：1.0→0.9999、1.15→1.1499（:373-378）防跨 pass 边界（1.0 应属
     远空 pass1/1.15 应属近距 pass2）。
  3. 海洋群系前景层满档（bgAlphaFrontLayer[4]==1，=bgStyle 4 海滩）且 y>200 的低云
     kill + 0.005/帧快淡（:399-402，与通用 0.001 叠加=0.006）——海面天空更晴朗。
     读数走 BiomeBackground.frontLayer()[4]（frameCtx.oceanFrontAlpha 注入）。
- **numClouds 语义**（Main.cs:58341-58421，Weather.updateCloudCounts 已 1:1）：numCloudsTemp
  逐 tick 漂移（晴天钳 ≤100），但 numClouds **只在 weatherCounter 到期（3600-10800t）才
  赋值**——开局 rand.Next(200) 的高值可持续数分钟，是原版行为勿"修"。
- 测试 tests/cloud-parity.test.ts（8 例：恰 target 次尝试/恒同掷点 1 朵/随机档 20-75、
  X 锚 vx 修正 ±200、海洋杀云 0.006/帧、scale 微移、出界 600 回收）。

**Why**: "凑满目标"与"恰 N 次尝试"在拒绝率高时差出 1.7×——原版云量上限由 AABB
拒绝（RSA 饱和 ~45-77 朵）天然调节，不是 numClouds 本身。

**How to apply**: 数量类生成器对齐时先算"尝试次数语义"而非"结果数量语义"；
离线 RSA 模拟（贴图尺寸表 + 随机排布）是量化云量差值的廉价法。相关 [[moonlight-worldlayer-split]]。
