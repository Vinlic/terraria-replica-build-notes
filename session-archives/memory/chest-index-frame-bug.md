---
name: chest-index-frame-bug
description: 宝箱四格同贴图根因——legacy structurePass 的 placeChest 写格索引(0/1)而非像素(0/18)，生成端+读档双修复
metadata:
  type: project
---

2026-08-11 宝箱"每个格子一模一样"根因（用户两个新存档都中招）：

- **现行 bug**（非历史遗留）：`WorldGen.ts placeChest`（legacy structurePass 的 2×2 宝箱）写入帧 (0,0)/(1,0)/(0,1)/(1,1)——**格索引当像素**。渲染 ofx=1 只偏 1px → 四格显示同一锚点贴图。BuriedChestsPass 的 placeBuriedChest 是对的（style*36+dx*18）——只有 legacy structurePass 错。
- **修复**：①placeChest 改 0/18 像素；②`Game.repairIndexFrames()`（afterWorldLoad）——已存坏档的兜底：扫全图 vanilla framed style 且 fw≥2 物体块，若全格帧 <18 且非全 0 → ×18 修帧 + 全 chunk 标脏。特征依据：合法多格块必有一格 ≥18（全 0 由渲染端锚点扫描重建）。
- **同种子复现测试**：tests/chest-frames.test.ts（种子 9293480 = 用户地图 seed，生成端扫坏块）。
- **marks 文件**（用户导出的标注 json）是定位利器——直接给出坏格坐标+帧值+邻居帧，省掉浏览器探针。

**Why:** 两套帧写入并存（vanilla pass 正确 / legacy structurePass 错误），同 seed 生成测试一步定位。**How to apply:** 凡多格家具渲染异常先 dump 四格原始帧（frameX/frameY），看是像素(18 的倍数)还是索引(0/fw-1)。关联 [[vanilla-door-frames]]（同类帧单位坑）。
