---
name: event-system-port
description: 事件系统三件套落地（2026-08-11）——日食/南瓜月霜月/星璇四塔，架构约定与二期清单
metadata: 
  node_type: memory
  type: project
  originSessionId: 372ae608-2da7-4502-87f6-cedcc2af7bb7
  modified: 2026-08-11T10:13:23.056Z
---

事件系统三件套已全部落地（2026-08-11，多代理实施，设计文档在 game/docs/event-*.md）：

- **日食**：`Clock.eclipse` 运行时态（不进 flags/存档——原版 Main.eclipse 不落盘）；黎明 roll（hardMode+机械任一击杀+1/20，NPC.cs:64898-64920）；日耀碑牌 vi_2767 召唤；刷怪池 14 id（3459-3525 全表非旧 45-48 表）；血红暮色压暗（Main.cs:63282）+BGM 27；`(!eclipse||!dayTime)` 门关闭白天小动物段。
- **南瓜月/霜月**（`src/world/MoonEvent.ts`）：独立事件状态**勿塞 invasionType**（原版正交建模：负组号-1/-2+bool）；20 波分数表共用、计分进波清零不结转、addMoonEventKill 在掉落结算后同帧（NPCLoot→CheckProgress 顺序）；霜月 wave14/南瓜 wave19 空刷是原版行为勿加兜底；血月互斥（start 清 bloodMoon）；选怪段在日食段之前（原版 2714/3134/3459 序）；moonMusic 在 pickMusic 链首（原版链尾=最高优先级覆盖 Boss 曲）。
- **星璇四塔**（`src/world/LunarEvent.ts`）：塔=纯 NPC aiStyle 94（无需 tile 基建）；教徒 439 死触发（downed_439 通用置位链追加）；四等距列±100 抖动；盾满 100（杀月总后 50）盾在=iframes 每 tick 刷新；扣盾归属表见 docs §3（伴生怪 406/408/410/413/414/416/428 不扣盾）；塔死 180t 演出后真死；四塔全灭→3600 倒计时→月总 398；lunarMusic=34 排 bossMusic 之后（**源码纠偏：文档"与 moonMusic 同层"不对**，Main.cs:12479 月总 38 先于塔曲）。
- **掉落数据修复**：extract-npcdrops.mjs 三缺陷（parseAtom 贪婪吞链名/emit 后挂链宿主错/多级链平铺）已修；六个月事件 Boss gate 链体补齐（纪念碑/1914/1871 等）；求值器补 oneOfRules kind。

**Why:** 事件代码的触发/结算/选曲接线点分散在 Game.ts 多处，二期改动前先读 docs/event-*.md 对应章节与代码注释锚点。
**How to apply:** 二期清单：①Boss AI 家族（月事件 57/58/60/61/62/63 + 四塔 74/75/85/95/96/97/99，现用近似家族）；②629 追踪弹/MoonLordShake/护盾着色器；③月亮贴图（南瓜/雪月）；④进度条 wave20 显示语义；⑤590/591 火把照明 AI；⑥微光 sparkle 视效。**caves-checkpoint 'beaches'/'mcopenings' 分歧属用户并行 worldgen 开发线（dfc2eb8），勿当本线 bug 修**。相关：[[spawner-vanilla-alignment]] [[multiplayer-room-system]]
