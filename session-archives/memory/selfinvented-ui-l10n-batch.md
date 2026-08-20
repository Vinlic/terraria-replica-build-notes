---
name: selfinvented-ui-l10n-batch
description: 自造UI全量多语言批:8面板~90键落地+原版官译键优先原则;并行会话撞车同键不同值的合并裁决;扫描器工具留档
metadata: 
  node_type: memory
  type: project
  originSessionId: 413208b1-378e-40ae-a408-9ae931eb30dd
  modified: 2026-08-16T05:26:25.371Z
---

2026-08-14 自造 UI 多语言批(用户"自造的做一下多语言支持"):

**原版官译键优先原则**(AmbientVol 事故推广):凡原版存在的功能/文案一律用原版键
(12 语言官译自动生效),`Mods.SandboxWorld.*` 自造键只留给原版没有的东西。本批换
原版键:健康/魔力样式值 `UI.HealthManaStyle_New/Default`(经典/精致)、风摆开关
`UI.TilesSwayInWindOn/Off`(环境风效)、世界创建种子族 `UI.WorldCreationSeed/
SeedEmpty/RandomizeSeedDescription/RandomizeNameDescription/WorldCreationSize`、
怀表时间 `Game.Time`、难度名 `UI.Softcore/Expert/Master`、商店价 `Lang.valueToCoins`
(Currency.* 官译)、收纳容器名 `Lang.itemName(87/346/3813/4076)`。

**自造键落地**(zh/en 双译,其余 10 语言落 en 兜底):Bestiary.*(18)/MP.*(33)/
Mobile.*/AssetDl.*(含 Phase_* 模板键)/Tabs.*/Craft.*/Reforge.*/Party.Birthday/
Map.*(传送预选/标记)/Toast.*(NeedItem/NpcArrived/BossFled/BuffSeconds/NeedBait/
BannerReady/WorldLoadFail/ConnectTimeout/Favorited)/NPC.WorldStatus/Item.Defense/
JourneyPowers.DifficultyNote/WorldCreation.DefaultName/Research.Title。

**修掉的隐性 bug**:NPC 入驻 toast 三处写成 `Lang.npcName(id) ?? 'X加入了小镇!'`
——命中时只显示名字不显示"入驻";改为 `Toast.NpcArrived {0}`。party.ts 硬编码
NPC 中文名表退役 → TOWN_NPC_IDS+Lang.npcName(12 语言官译)。

**遗留不处理**:F6/F5/F3/DebugSummonPanel 调试面板、道具搜索 dev 面板、诊断日志、
UI.ts showMainMenu 死代码、天气无线电上的天气预设调试按钮、JourneyPowersUI 的
t() 中文 fallback(键全命中,fallback 恒不显示——已逐键验证,CreativePowers 79 键
里只有 ResearchItemsCategory/DifficultySlider_Description 不存在已改)。

**并行会话撞车**(重要教训):另一会话同刻在做同任务——custom 文件出现三套同键
不同值段(嵌套/嵌套重复/顶层点分),后写者按 Object.assign 覆盖。裁决法:以 **src
实际调用的键与参数形态**为准保留一套(我的 Craft.PutTakeHint 无参调用 vs 对方
"{0}" 占位值 → 保留无参兼容版),删重复段,重建+audit 收口。冲突时先 grep src
看代码真身再动手。

**工具留档**:`game/tools/_cjk-literal-scan.mjs`(剥注释扫玩家可见面硬编码中文,
TARGETS 清单可控)+ `game/tools/_l10n-custom-diff.mjs`(代码键↔custom 双向对账;
模板串动态键会误报死键——MP.*/DiffDesc.*/ItemName.Wood* 是活的)。审计正则只认
`Lang.text('字面')`,t() 包装与模板串键**不设防**,须人工验。

**2026-08-16 追记:SW 缓存卡死旧语言包(用户报暂停菜单裸键 Tabs.Bestiary)**
- 根因:public/sw.js 把 `/l10n/` 也走 cache-first,而缓存版本号 = vanilla.json/ui
  哈希 + CACHE_BUSTER——**l10n 重建不换版本** → 页面永远命中多语言批之前的旧包,
  新键全显示裸键(键在源/产物都验证过也在,纯缓存层事故)
- 修:sw.js 对 `/l10n/` 改**网络优先+离线回退缓存**(与壳 JS 同策略);AssetCache
  版本注释同步(l10n 豁免,sounds/fonts/audios 仍靠 CACHE_BUSTER 手动闸)
- SW 更新时序:sw.js 字节变了,首次刷新后台装新 SW+claim,**第二次刷新**才保证走
  新 handler——用户侧"刷新两次"(或清 SW 存储)立即生效
- 教训:**可变配置(l10n)绝不进 cache-first 缓存**;CACHE_BUSTER 手动闸对高频变更
  的资产族形同虚设

相关 [[l10n-bare-key-incident]] [[vanilla-language-port]] [[sw-asset-preload-port]]
