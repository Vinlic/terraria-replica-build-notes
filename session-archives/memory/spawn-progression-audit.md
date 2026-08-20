---
name: spawn-progression-audit
description: 肉后出怪池/数值强化对账终审:隔离已1:1;数值=换池+ExpertHardmode兜底(花后80→100);月后原版无影响;四缺口已修
metadata: 
  node_type: memory
  type: project
  originSessionId: 1fc2b821-952a-4ed1-9b75-6e99198205af
  modified: 2026-08-13T06:18:40.307Z
---

2026-08-13 肉后怪物强化+出怪池隔离（肉前/肉后/机械/花后/月后）双代理全量对账终审。

**结论：隔离机制已 1:1；"肉后变强"原版语义=换怪池（60+ 分支全挂 hardMode 门）+ 专家弱怪归一兜底，经典模式无全表数值膨胀。**

**原版权威要点**（NPC.cs:1186-5144 SpawnAnNPC / 18081-18673 scaleStats）：
- downedMechBossAny 全 spawner 仅 2 处：红恶魔 156/岩浆蝙蝠 151（:4799/:4812）——我方 L2321/2327 一致。
- downedPlantBoss：hardDungeon 池（:291 须 hardMode∧Plantera 双门）+日食蛾怪族+月光蝶 661——我方全挂 downed_262 ✓。
- **月后（downedMoonlord）对出怪池/数值零影响**（1.4.5.6）——仅星璇塔盾 100→50（我方 LunarEvent 已接）。cultist 同零。
- 数值：ScaleStats 结构逐行同构（NeedsExpertScaling 门/ByDifficulty 曲线+Tweaks 表/ByPlayerCount/ExpertHardmode 兜底）；两集合 NEEDS_EXPERT_SCALING 与 DONT_DO_HARDSMODE_SCALING 与 NPCID.cs:4799/:4440 逐 id 零差；Mimic 85/629 肉前降档仅 remix/skyblock 用（我方无该种子,豁免）。
- 日食分支本身无 hardMode 门（:3459）——原版靠事件入口门（黎明 roll hardMode∧mechAny / 日耀碑牌困难物品）保证隔离。

**本轮修复四项**：①**630 血木乃伊**补 vanilla-npcs.json（1456 cs:17042-17054：180/60/18/kb0.5/aiStyle3/16帧,贴图已在）——此前 fromVanilla null 静默丢弃；②F6 调试日食补 hardMode 门（自然入口原则）；③**townNoWorms 并入 noWorms**（原版同字段只写真值→OR 即终态;此前闩后不读=城镇旁蠕虫抑制失效）；④getGoodWorld 刷怪率 ×0.8/×1.2（:654-656）。WoF 战地狱压制（:668 ×3/×0.3）不移植：我方 trySpawnEnemy 在 Boss 在场整体 return,强度已覆盖。

**登记未修**：仙女 583-585 整链未移植（×1.66 HM 跟随,在 spawn-parity-gaps）；僵尸抗性测试期望 0.55 过时（并行会话改曲线为原版两键后真值 0.45,归其修）；681 行 Blood Feeder 241 反编译双 ZoneCrimson 疑云（241/242 均猩红水体,行为疑正确）。tests/spawn-progression-gates.test.ts 3 条。相关 [[spawner-vanilla-alignment]] [[mechanics-audit-2026-08-12]]
