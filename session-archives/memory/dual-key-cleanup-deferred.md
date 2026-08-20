---
name: dual-key-cleanup-deferred
description: 双键注册清理已延期（2026-08-12）——完整方案在 game/docs/dual-key-cleanup-plan.md，恢复条件=安静窗口
metadata: 
  node_type: memory
  type: project
  originSessionId: 04569a63-44aa-4669-98a3-b777d15e98f8
  modified: 2026-08-13T17:27:39.902Z
---

# 双键注册根源清理 — 已延期待执行

**完整执行方案快照**：`game/docs/dual-key-cleanup-plan.md`（改动代价实测 + 六步方案 + 验证清单 + 延期状态）。

要点备忘：
- items.ts 有 520 对双键（蛇形显式 + 驼峰自动）+ 10 个重复键异常（vid 122/217/1507 蛇形双重、4851-4857 GemTree 驼峰双重）
- **非纯删除**：驼峰 def 独有 tool×32/axePower×5/value×2 必须先搬入蛇形，否则丢挖掘力数据
- 三处映射方向翻转（VANILLA_ITEM_KEY_BY_ID/工具力循环/音乐盒喷泉循环）；最大触点=WldImport:909 驼峰 fallback（不改则 520 物品导入静默丢弃）
- v3 存档零迁移；v2 旧档内部 id 会漂移需保留旧映射（**此项需用户拍板**）
- **恢复条件**：items.ts/Game.ts/SaveFile.ts 无人触碰的安静窗口单 commit 落地；并发窗口内曾发生多次他人编辑事故（tiles.ts 注示吞行/DungeonPass 多余大括号），勿在活跃期做跨文件重构
- ~~零冲突先行项：字段搬移~~ **已完成（2026-08-14）**：实测基数重测为 1227 对/81 驼峰独有字段
  （tool×35/axePower×7/value×2/wireTool×1/tile×22/placeStyle×14），全部并入蛇形，行尾注释
  `// ←vi_… 独有字段搬移(批次A)`；`tests/dual-key-fields.test.ts` 锁定差异清零+基数防假绿。
  **遗留**：10 处值冲突（蛇形为手工修正值，保留蛇形）+ 14 重复键异常（清理第 3 步）

相关：[[explosion-family-port]]（战利品双份入箱补丁的由来）
