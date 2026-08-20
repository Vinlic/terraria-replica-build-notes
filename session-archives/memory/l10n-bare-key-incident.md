---
name: l10n-bare-key-incident
description: "NeedTempleKey裸键事故全链——顶层点分键被整键当类别成{\"键\":{\"\":\"文本\"}};审计整段键兜底放行非字符串;三闸门+运行时自愈"
metadata: 
  node_type: memory
  type: project
  originSessionId: c212e38d-8db4-446d-b3da-4e20d707caf7
  modified: 2026-08-13T16:27:02.034Z
---

2026-08-14 用户报 Toast 直显 `Mods.SandboxWorld.Toast.NeedTempleKey` 裸键。

**根因链(三层叠加)**:
1. **build 侧**:custom 文件(仓库根 tools/l10n-custom,非 game/tools!)混用两种写法——头部嵌套 `{Mods:{SandboxWorld:{...}}}` + 尾部多代理追加的**顶层平铺点分键** `"Mods.SandboxWorld.Toast.X": "文案"`。`flattenDeep` 顶层键=类别的约定下,平铺点分键被**整键当类别** → 产物 `{"Mods.SandboxWorld.Toast.NeedTempleKey":{"":"文案"}}` 假类别。原版 84 分片顶层类别均不含点,首段拆分安全。
2. **审计侧盲区**:resolvePackKey 的"逐段下行+**整段键兜底**"把假类别当命中(返回对象非字符串)→"390 键全部命中"假绿。
3. **运行时**:texts map 查不到 → getText 回退键本身。

**修复(四层)**:
- flattenDeep:顶层点分键按**首段拆** = 类别+条目键(存量坏键全量自愈)
- build-l10n:产物形状闸门 validateTable(类别含点/空条目键/非字符串值 → throw)
- l10n-audit:命中 = **typeof string**(非仅 defined)+ 全表形状扫描;vite 插件 dev 警告/build 阻断双档
- LanguageManager.buildTables 运行时自愈:对象值含 '' 字符串 → 按类别名登记(旧坏包不裸键)

**验证**:重建后 NeedTempleKey="需要一把神庙钥匙!";zh 包 0 形状违例;Toast 键 46→52(找回 6 个同批丢失键:JojaCola/AchievementUnlocked/ChaosState/NightHallowOnly 等);审计 390/0/0;l10n 测试 26/26。

**教训**:①"键存在"≠"键可用",值类型是审计契约的一部分;②custom 文件双写法混用是事故温床(现在两种写法都正确支持);③**custom 路径在仓库根 tools/,不在 game/tools/**(TOOLS=here/../..)。


## 三件：InputTrigger 全局替换（2026-08-18，"蠕虫罐头说明有问题"）

用户报蠕虫罐头 tooltip 裸显 `{InputTrigger_ToggleOrOpen} to open打开`——根因是
**Lang.cs:86-160 RegisterGlobalSubstitution 未移植**：原版 GetTextValue →
LocalizedText.Format 会把 {Token} 查全局替换表（键位名+NPC 名），我们只做了
{0}/{1} 位置参数，171 条 ItemTooltip+GameUI/LoadingTips 全部裸显 token。
**修复**=LanguageManager.getTextValue 尾接 applyGlobalSubstitutions（惰性建表
一次缓存；{字母开头} 正则不碰 {0}；未注册 token 原样保留=原版语义）：
- 键位（键盘档，PlayerInput.cs:1880+ 默认绑定）：MouseRight→Controls.RightClick
  （ToggleOrOpen/InteractWithTile(UI) 三 token 同源）、MouseLeft→Controls.LeftClick
  （UseOrAttack）、SmartCursor→Controls.Control、SmartSelect→Controls.Shift、
  Grapple/QuickEquip=E、QuickMount=R（UI.BuildFromInventory）、FavoriteItem=Alt、
  Trash=Controls.Shift；**键盘未绑（LockOn/Radial*/Hotbar±）=空串**（GenerateRawInputList
  空列表语义）。
- NPC 名（:102-110 {Nurse}/{Merchant}/等九 token）→ setNpcNameResolver 注入
  （Game.afterWorldLoad 闭包查 TownNPC.vanillaId+givenName；缺位保留 token=null 语义）。
- ★"to open打开"是 **1.4.5.6 官中数据终态**（Terraria.Localization.Content.zh-Hans.Items.json
  原文如此——替换后= "右键点击 to open打开"，与真实游戏一致，勿"修"数据）。
- 教训：**菜单期探针查 Lang 必须先轮询 Lang.loaded**（语言包异步拉取，2s 定时
  等不稳）；puppeteer waitForFunction 内嵌 async import 不可靠，Node 侧手动轮询。
测试 lang.test.ts +4 例；探针 _l10n-subst-probe（run-probes 注册，3 断言）。


## 四件：同类问题全量审计（2026-08-18"检查是否还有类似问题"）

枚举构建包全部 {Token} 分类对账,发现**替换表只接了 61 注册中的 23 个**+一处
构建期语义误读：
- **补全 38 注册**：14 个 NPC 名(Mechanic/Truffle/Steampunker/DyeTrader/PartyGirl/
  Cyborg/Painter/WitchDoctor/Pirate/Stylist/TravelingMerchant/Angler/Bartender/
  GolfGuy/TaxCollector)+动态值 WorldName/PlayerName/InventoryKey/
  AnglerCompletedQuestsCount/TotalDeathsCount/WorldEvilStone(黑檀|猩红按 crimson)/
  ToggleArmorSetBonusKey(Key.DOWN 默认)——setGlobalSubstitutionContext 注入
  (Game.afterWorldLoad 闭包活取;缺位保留 token=null 语义)。
- **{$未命中语义纠偏**:l10n-merge expandCopyCommands 曾"保留 {$ 原样"并注释
  "原版 L171 行为"——**误读**,原文 `: text2` 是替换成裸键名。修复后 5 条旗帜
  tooltip 的 {$NPCName.None} → "NPCName.None"(构建重建),再由 **UI 层**
  bannerNpcOfItem(vanilla-banners npcToBanner 反查,共享旗取家族最小 npc id)
  换成 NPC 显示名(原版旗帜 tooltip 动态注入语义)。
- **无问题确认**：{NPCName}/{BiomeName}(TownNPCMood)与 {Adjective}/{Noun}/
  {Location}(世界名)消费端已自替换 ✓;{Day}/{BloodMoon} 等 bool 族全在 {?}
  标记内构建期剥离 ✓ 零裸露;{0:+0;-#}(PrefixArmorPenetration 正负格式串)
  无消费路径(词缀 UI 走自算行)暂不可见;{Armsdealer}(GolferChatter)是官方
  typo(注册表键 ArmsDealer 大写 D,原版同样不替换裸显)——最终态保留。
- resetForTest 现清注入器+替换表缓存(模块级状态泄漏曾致跨测试污染)。
测试 lang.test.ts 19 例/l10n 全家 57 例;探针 l10n-subst 扩到 4 断言(8 键
抽查零裸 token)。


## 终审（2026-08-18"最终 review"）

回读全批改动对源码逐项复核——**零真偏差,一处防御性加固**：
- 12 语言全包 `{$` 残留=0（重建后全扫）；custom 双文件无 {$。
- 递归安全：l() 闭包取 Controls.*/Misc.*/Key.* 均无嵌套 token（快路径）。
- 循环引用终止：A↔B 互拷 → 裸键替换后不动点收束,循环对落 unresolved 报告
  （与原版 100 次迭代上限同语义）。
- 旗帜家族反查核验：共享旗取最小 npc id（如 104 族=7 僵尸）与旗帜物品名
  家族代表一致；邪教徒旗 216-220 → npc 402+ 全在 npcToBanner。
- 键名跨语言正确（en Right Click/ja 右クリック/ko 우클릭;Key.DOWN 同）。
- **加固**：idNames 兜底表携带 2 条官方 {$ItemName.*Altar} 复制原文（6135/6136
  图标祭坛——主路径 ItemName.*Icon 12 语言全在=死数据）→ Lang.itemNameByKey
  兜底门追加 `!fb.startsWith('{$')` 按缺失处理走英文名,防未来键缺失时裸显。
- 测试终态：l10n 全家 45 例+相邻 63 例全绿；tsc 零错。
