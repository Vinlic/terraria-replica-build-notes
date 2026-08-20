---
name: npc-frame-golden-gate
description: NPC帧数硬闸门npc-frame-golden.test.ts三层+贴图自洽;运行时直读Main.cs零快照;三破坏性自证全炸;研究UI l10n缺失归并行
metadata: 
  node_type: memory
  type: project
  originSessionId: 1fc2b821-952a-4ed1-9b75-6e99198205af
  modified: 2026-08-13T08:34:15.656Z
---

2026-08-13 应用户"强硬方案让这种过不了测试"建 **tests/npc-frame-golden.test.ts** 常驻金标闸门：

**三层 + 自洽**（运行时直读 `Terarria1456/Terraria/Main.cs` 提取 npcFrameCount[697]——2MB 文件流扫 <100ms，**零快照零腐烂**）：
1. 帧数全量对账：每条 `VANILLA_NPCS` frames === 数组值（治 668→25 类错值）；
2. 完整性：数组 frames>1 的 id 必须在 json（白名单 ALLOWED_MISSING 当前空；治 13 条缺失类）；
3. 消费端覆盖：源码扫描 VanillaSpawner/Game 的 `spawnBound(N)|spawnPart|fromVanilla(N,|D(N)` 字面量 → 必须有 json 条目（治 589 静默丢弃类）；**id>696 跳过**（界外=误匹配）；
4. 附贴图自洽：frames>1 的帧高 ∈ [8,300]（单帧不设限——荷兰人 590px）。

**自证三连（全炸后还原）**：668→9 ✓红报 `668 json=9 vanilla=8`；删 624 ✓红报缺失；spawner 塞 `D(696); // 注释` ✓红（**教训：剔整注释行会让带注释的假引用漏放，必须行内 `//.*` 剥离后再匹配**——自证③第一轮没炸暴露的）。

**测试自坑记录**：①`new URL('../../..')` 从 game/tests 多跳一层（根是 `../..`）；②PNG IHDR 高度在 bytes **20..24** 非 16..20（宽高读反致 Merchant h=40 全员误报）。当前 11/11 绿（含 town-sheet 7 条）。

**环境**：全量 `npx vitest run` 暂被并行会话 `ResearchUI.ts` 缺 4 键（Research.Empty/Progress/Sacrifice/SacrificeAll）阻断——归该会话补 tools/l10n-custom 后重建,勿代补。相关 [[npc-frame-ironclad-audit]]
