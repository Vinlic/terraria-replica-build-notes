---
name: npc-frame-ironclad-audit
description: "全NPC帧数石锤复核:json×Main.npcFrameCount[697]×贴图高三方零差;修4错帧+补13缺失(589被困高尔夫球手spawner静默丢弃);帧数唯一权威=json frames勿高/56反推"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1fc2b821-952a-4ed1-9b75-6e99198205af
  modified: 2026-08-13T08:16:57.705Z
---

2026-08-13 全量 NPC 帧渲染 1:1 石锤复核（用户要求"完全石锤"）。

**方法**：机械提取 `Main.npcFrameCount[697]`（Main.cs:65994 初始化数组,去注释后按序）× `vanilla-npcs.json` 全量对账 × 全贴图 `file` 尺寸帧高合理性带（16-220px,微型小动物 8-14px 另列合理）三方交叉。

**结论**：修复后 **json 与 Main.npcFrameCount 零差异**；全 689 条贴图帧高全部自洽。

**修复数据**：①4 条帧数错：129/130 PrimeSaw/Vice 1→2、408 StardustJellyfishSmall 5→4、**668 鹿角怪 25→8**（曾误填 25）；②13 条 json 缺失整补（SetDefaults 提取）：**589 GolferRescue（13 帧,spawner :1483 spawnBound(589) 此前 fromVanilla null 静默丢弃——被困高尔夫球手从未出现过）**、255 僵尸蘑菇帽/614 爆炸兔/624 地精(11)/662 海盗幽灵(4)/664 火把之神/667 金史莱姆/676 微光史莱姆/693/694(30)/695/76/146。

**铁律（两轮教训）**：①NPC 帧数唯一权威 = `vanilla-npcs.json frames`（=Main.npcFrameCount）,**勿用 高/56 反推**（城镇史莱姆 670 表 476px/14 帧=34px 帧高,反推 8 必错）；②`atlas.vnpcMeta` 只覆盖 vanilla.json npcs 的 20 条特殊条目,取帧数必须 `?? VANILLA_NPCS[id].frames ?? 1`；③写测试锚点别凭记忆——先跑三方对账脚本再填期望值（僵尸=3 非 4、WoF 113=2 非 4,两次锚点翻车）。tests/town-sheet-frames.test.ts 7 条含权威锚点。相关 [[vanilla-npc-json-gaps]] [[deerclops-port]] [[guide-query-parity-batch]]

## 2026-08-14 附:Prime 头帧混播(用户报"一/二阶段动画一起播")
- 根因:vanillaFrameIdx(Renderer.ts)无 127 分支 → 落通用 6t 档全 6 帧循环(正常脸 0-1+旋冲脸 2+MechQueen 3-5 连播)。
- 原版权威 FindFrame case 127(NPC.cs:75196-75231):ai[1]==0=帧{0,1} 12t 眨眼;ai[1]≠0=恒帧 2;3-5=MechQueen 合体专属。锯 129=2t/激光 130=8t 越帧回卷;钳 128/炮 131 无 case=恒帧 0(均单帧无需特判)。
- 验证法(可复用):hook `renderer.atlas.vnpc` 录特定 npc 取帧序列+真实时间驱动(fixedUpdate 不触发渲染);Clock.isDay 是 getter,改夜须写 timeOfDay=0;spawnNpcByVanilla 是小动物桶专用入口(头会进 critters 臂找不到头自杀),Boss 生成用 debugSpawnNpc(F6)。
