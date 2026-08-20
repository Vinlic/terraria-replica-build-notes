---
name: fog-entry-multiband-stale
description: 入场迷雾视野未开根因=分带整幅重建跨帧+带间标记+完成盲盖版本;修=完成时补扫dirty盒并消费
metadata: 
  node_type: memory
  type: project
  originSessionId: ec878731-1c65-4b4c-9a3b-c8009ce5461a
  modified: 2026-08-19T10:37:19.531Z
---

# 入场迷雾视野未开（要走动才更新）——分带重建版本盲盖竞态（2026-08-19）

症状：刚进世界出生点雾不开，走动（bump exploredVersion）才更新。
根因（Renderer.ensureFogData）：整幅重建按 120 行/带摊帧（真实世界 fogH≥600=5+ 带），
进图 tick0 的 markExplored 落在【已扫过的早行带】→ 早带按旧数据写 FOG 不回头，
完成时却 `fogVersion = world.exploredVersion`（当前版本）→ fv===v 早退把陈旧雾焊死，
直到玩家移动 bump 版本走增量分支才修。**小世界（fogH≤120 单带）永不复现**——
单测用 200×200 世界全绿的假阴性陷阱。

修：① 抽 `applyDirty()`（幂等双向重扫，纯 ex 现值函数）；增量路径与**整幅完成时**
都补扫 dirty 盒再落版本；② 两处消费 `world.exploredDirty = null`（防盒随探索无限
增长；dirty 语义从"历次并集永存"改"未消费标记"——消费点唯一=渲染端）。

验证三链：tests/fog-entry-seq.test.ts 多带回归（800×300 两带+带间标记，修前 FOG/
修后 0）；探针 _fogentry3 包裹 mmHudBlit 逐帧 fogv（修前 40/40 帧 FOG→修后 1/19
仅首帧）；_fogentry2 HUD 合成中心像素 [5,5,8]雾→[88,61,46]地形。

★方法论：
- **入场类 bug 复现要跨帧序**（重建跨帧 vs 同步标记），单帧单调用测试造不出竞态；
- **世界尺寸是复现变量**（带数=fogH/120），测试用大尺寸（>240 高）才踩多带；
- **版本号早退模式**（cache===version 即 return）+ 多帧生产者 = 经典焊死竞态：
  完成时必须对"生产期间变化"补账，不能盲盖当前版本；
- worldgen 被并行会话挂死时，**页内合成存档走 `__swFlow.loadJson`** 可绕开
  worldgen 做全链 e2e（buildSaveParts+serializeSave 造档）。

关联：[[fog-flicker-f4-latetex-fix]]（同文件前轮三修，本轮是其下游竞态）
