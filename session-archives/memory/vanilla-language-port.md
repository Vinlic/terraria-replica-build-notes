---
name: vanilla-language-port
description: "原版语言系统移植完成 — 12语言/默认zh-Hans/设置切换、扁平语言包构建管线、{$}构建期展开、flattenDeep陷阱"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-11T09:18:59.143Z
---

# 原版语言系统移植(2026-08-10 完成)

12 种语言全部支持,默认 zh-Hans,设置面板"界面"栏语言网格可切换(显示名=当前语言渲染 `Language.*` 键,原版语义)。E2E:`game/scripts/l10n-smoke.mjs`(切英文→面板/菜单刷新→持久化→重启仍英文→单包无双 fetch)。

**架构**(对照 Terarria1456):
- `src/i18n/GameCulture.ts`:12 culture(LegacyId 1-12,zh-Hans=7)、`fromLegacyId`(id<1钳1)、`normalizeLang`(兼容旧数字)
- `src/i18n/LanguageManager.ts`:全键 Map + category 索引 + `$` 变体表;`setLanguage` fetch `l10n/<name>.json` + pack LRU≤2;`randomFromCategory`/`indexedFromCategory` 取模;`sw:langchange` window 事件
- `src/i18n/Lang.ts`:门面保持旧签名(`load/text/has/worldgenText`)+ 便捷方法 `itemName/itemNameByKey(vi_前缀或ITEM_KEY_TO_ID)/npcName(负netId近似)/buffName/buffDesc/projectileName/tileName/menu/misc/inter/gen`
- `idNames.generated.ts` 由构建生成(id→常量名,id-maps internal),**键一律引号化**(projectiles 有负数 id -65)

**与原版差异(构建期承担)**:`scripts/build-l10n.mjs` 产出扁平 `{[category]:{[key]:value}}` 单文件/语言(默认合并 en 基线做英文兜底 overlay)+ `index.json`;**`{$Key}` 复制构建期展开**(未命中保留原样,原版 L171 行为,如 `{$NPCName.None}` 残留是预期);`{?Cond}` 剥标记保留正文(chatter 未来用);`{Var}` 命名模板全库 0 键不做。纯函数在 `scripts/l10n-merge.mjs`(+ .d.mts 供 tsc)。

**★flattenDeep 陷阱**:`Object.assign(out, sub)` 合并递归结果会整体替换 `out[cat]`,同类别多组嵌套只剩最后一组(曾致自定义文案丢 9/10 组);必须逐类别 `Object.assign(out[cat], entries)`。已加回归测试。

**自有文案** `tools/l10n-custom/{en-US,zh-Hans}.json`(深层嵌套,Mods.SandboxWorld.* 键空间;纯 JSON 无注释);原版没有的标签全走这里(UI面板/设置/世界创建/角色创建/Buff描述),能对上原版的用原版键(LegacyMenu.14=设置/47=创建世界/16=创建人物/102=选择语言/98,99=音效音乐/UI.Normal/GameUI.Expert/UI.Master/UI.Creative=难度/UI.PlayerCreateCategory*=颜色标签)。

**启动时序**:`main.ts` 先 `await options.load()` 再 `Lang.init(options.data.lang)`(mainFlow 的 options.load 幂等);OptionsData.lang 默认 'zh-Hans'。语言切换刷新:SettingsPanel 重建保 cat、TitleMenu.renderTexts、WorldCreation 整面板重建(static lastSel 记忆)、CharCreation.refreshTexts、WorldSelect/CharSelect reload,**常量数组必须改键引用否则重建也拿旧文案**。

**遗留**:legacy showMainMenu 垫片与 F5 标注/贴图纠错/兼容报告(dev 面板)保留中文;`GetPrefixedItemName` Gender 变体未接线(无 prefix 系统);负 netID 65 条硬表(Lang.cs:522-527)待 NPC 变种;非中文语言落系统字体(像素感丢失,仅提示);测试 tests/pot-break.test.ts 曾闪败(与 l10n 无关)。

**全量键审计（2026-08-11，用户报"Mods.SandboxWorld.NPC.Rescued"裸键显示）**：`tools/_audit-l10n.mjs`——提取 src 全部 `Lang.text/has('字面键')` 对 zh-Hans 合并包解析（点路径逐段下行+整段键兜底，与 LanguageManager 同语义）。发现 5 键代码在用包里缺：NPC.Rescued/TaxCollected/TaxEmpty/Progress.Connecting/Toast.Need200Hp → 补 tools/l10n-custom 两包+rebuild。数值索引键（inter/misc/gen/menu）与 chatter 类目另扫——全在。**注意**：新增自有键必须进 l10n-custom（en+zh 两包都要），只改代码不补包=运行时裸键显示；zh-Hant 等其余 10 语言经 en 兜底 merge 自动获得。

**构建期自动检查（2026-08-11 二轮，用户令"build 时自动检查"）**：①核心 `tools/l10n-audit.mjs`（auditL10n/resolvePackKey 导出，CLI=vite 插件=vitest 三方共用）。**三轮扩展**：除 Lang.text/has 直调外，全量扫 `'Mods.SandboxWorld.*'` 字面串（labelKey/descKey 间接传递键也覆盖，216 键）——**模板串键（\`...\${var}\`）抓不到，自定义键必须全字面**。②vite 插件 `l10nAuditAuto()`（vite.config.ts）：**先查语言包过期**（l10n-custom/构建脚本 mtime > 产物 → 自动重跑 build-l10n.mjs）再审计——`vite build` 缺键即 throw 中断（实测注入裸键 exit=1+键名/位置清单）；dev 仅 warn。③回归锁 tests/l10n-audit.test.ts（基数护栏 + resolvePackKey 三语义）。

关联 [[vanilla-ui-port]] [[terraria-assets-pipeline]]
