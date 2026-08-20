---
name: vanilla-npc-json-gaps
description: vanilla-npcs.json 缺 588/633/663 三个城镇 NPC 导致"整张贴图条当一帧画"——补数据与帧数权威来源
metadata:
  type: project
---

2026-08-10 修"高尔夫球手完整贴图条"渲染 bug（用户报 Starter World 存档进图右侧出现竖条全帧贴图）：

- **根因**：`public/sprites/vanilla-npcs.json` 缺 **588 Golfer / 633 Zoologist / 663 Princess** 三个城镇 NPC（extract-npcs.mjs 的 SetDefaults 块链没覆盖到它们的共享块）。SpriteAtlas.vnpc 懒加载 `frames = vanillaNpcFrames[id] ?? 1` → **frames=1 → fh=整张贴图高** → drawTownNPC 把 NPC_588.png（42×1400，25 帧）整条当一帧画。bound 高尔夫球手（placeBoundRescueNpcs 放置在地下沙漠）由 placeBoundRescueNpcs 生成正好撞上。已补三条（frames 权威来自 **Main.cs npcFrameCount 数组**：588=25、633=23、663=23；其余字段城镇共享段标准 250HP/防御15/aiStyle7）。**TownNPC 构造的 lifeMax/defense 有 ?? 兜底所以只坏渲染，不坏数值**。
- **教训**：凡"某 NPC 显示为竖条/整图" = frames 数据缺失或帧高非整除，先查 `vanilla-npcs.json` 有无该 id。帧数权威 = Terarria1456/Terraria/Main.cs 的 `npcFrameCount = new int[697]{...}` 数组（idx=id）。
- **同图另两症状**：①"突然卡一下"= 11.5MB json 载入 1.3s（parse+世界构建+液体沉降）一次性 + 载入后首帧初始化尖峰 41ms；②"向导瞬移到出生房下方"静止探针未复现（向导生成在 spawn-2 格），疑似卡顿跳帧视觉误判或沉降改变地形——待用户复测。
- 探针：scripts/_mapbug.mjs（经 __swFlow.loadJson 桥载入自有 json 存档；分段计时+tick 尖峰记录+bound NPC 清单）。

**Why:** 数据提取器的块链解析对"多 case 共享块"（城镇族一长串 case 共用一段默认值）覆盖不全，缺的恰好是渲染必需的 frames。
**How to apply:** 新 NPC 渲染异常先查 json 有无 id+frames；补数据时帧数一律查 npcFrameCount 数组。关联 [[vanilla-npc-port]]。
