---
name: guide-query-parity-batch
description: "攻略查询原版水位结论(图鉴唯一百科+向导反查,无wiki链接)+图鉴免门UNLOCK_ALL+ItemTooltip说明行接入"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1fc2b821-952a-4ed1-9b75-6e99198205af
  modified: 2026-08-13T07:17:44.034Z
---

2026-08-13 攻略查询系统调研+落地（用户拍板：只对齐原版水位、不自研面板、图鉴完全免门）。

**原版结论**：唯一百科=图鉴（掉落+掉率+条件/环境标签/数值/风味/击杀解锁门，`UIBestiaryTest`）；向导 NPC"制作"=唯一配方反查（`Recipe.CollectGuideRecipes` Recipe.cs:439，我们有 `UI.openGuideSearch` UI.ts:1435）；tooltip 渲染 item.ToolTip（Main.cs:20783-20798）；**无全配方浏览器、无游戏内 wiki 链接**（LinkButtonsInitializer 仅标题画面）。磁盘有 655MB 英文 wiki markdown + 中文 mirror 工具（tools/wiki-mirror.mjs 未跑）——v2 若做正文检索再用。

**改动**：①`Bestiary.ts` 加 `bestiaryGating = { unlockAll: true }`（holder 供单测注入），`unlockState()` 开闸恒 `DropsWithRates`——**刻意偏离原版**（原版 5 档击杀门+金宠门），图鉴作参考书；击杀数/完成度条仍真实统计。②`UI.showTooltipFor` 补 ItemTooltip.* 说明行（vi_→ITEM_NAME_BY_ID→`Lang.text('ItemTooltip.'+name)`，缺键跳过，\n 分行；l10n 是**嵌套**结构 `ItemTooltip` 对象 2664 键非平铺——zh 包路径 `public/l10n/zh-Hans.json`）。③搜索别名（eoc/eow，Populator.cs:643）登记 docs/spawn-parity-gaps.md 不实现。

**坑**：①单测要真实语言包须 `languageManager.loadPackJson(JSON.parse(readFileSync('public/l10n/zh-Hans.json')))`（bestiary-ui.test.ts 先例）；②门控单测统一 `beforeEach{unlockAll=false}/afterEach{true}` 注入，另加免门默认断言；③高负载（load≈19）时 puppeteer 页面引导 240s 超时——同路径已有单测覆盖则跳过探针。tests/bestiary-ungated-tooltip.test.ts 4 条 + bestiary 两套 51 条全绿。相关 [[bestiary-data-layer]]
