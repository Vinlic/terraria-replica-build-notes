---
name: music-extraction-off-by-one
description: BGM 提取两代错位的根因与修复——定位必须用 XWB 内嵌流名，vgmstream -s 是 1 基
metadata: 
  node_type: memory
  type: project
  originSessionId: 0650e0c7-c14a-4b14-b89b-73780115946c
  modified: 2026-08-10T03:13:44.040Z
---

游戏 BGM（`game/public/audios/music/Music_<id>.mp3`）由 `tools/xwb-extract.mjs` 从原版 `Wave Bank.xwb` 提取。2026-08-10 修复了两代错位 bug（症状：玩家在腐化之地听到丛林 BGM，全表 id≥5 每首装的是前一首）：

1. 第一代：按"wave 条目号=MusicID"提取，全表错位；
2. 第二代：改用 Sound Bank.xsb cue 名配对，但 ① vgmstream `-s` 是 **1 基**而 xsb 的 wave 索引是 **0 基**，整体前移一格；② xsb 前三条 cue 配对本身也错（M1/M3 对调）。

**Why:** 症状是"BGM 与地点不符"，很容易误判成群系判定（SceneMetrics/pickMusic）的 bug——实际上选曲链 1:1 正确、场景计数也正确，错的是音频文件内容。
**How to apply:**
- MusicID 定位的唯一权威 = XWB 内嵌流名（`vgmstream-cli -m -s <slot>` 输出 `stream name: Music_N`），不要再用 xsb 配对；
- vgmstream `-s` 一律 1 基（slot = wave+1）；
- XWB 的时长格式是 `M:SS.mmm`，parseFloat 会只取到分钟位；
- 修完映射必须 `--force` 全量重提（脚本对已存在文件默认跳过）；
- 时长自检（mp3 vs XWB play duration ±1.5s）是验证提取正确性的最快手段，当前 104/104 一致。
