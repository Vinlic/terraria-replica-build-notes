# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-09T11:40:17.815Z

```
你是校验员。权威数据:官方 changelog.txt(英文,`~/Library/Application Support/Steam/steamapps/common/Terraria/changelog.txt`,即 ~/Library/Application Support/Steam/steamapps/common/Terraria/changelog.txt)。其中 **Version 1.4.4 到 1.4.4.9(含 1.4.4.8.1)** 的段落是第 2374 行到第 4368 行(用 `sed -n '2374,4368p' <文件>` 读取,可分段)。

被校验文档:~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md(中文,基于 zh wiki 解析)。注意:该摘要目前**缺 1.4.4.8.1**(官方第 1995-2003 行,内容已知:海洋晶塔修复、Guide/Goblin 菜单物品管理修复、多人哨兵移除修复、Bone Helm 小地图标识修复、绞肉机方块外观位置调整、North Pole 伤害 73→80)——这条不用报,我已知。

任务:逐节对比官方 changelog 与中文摘要,找出:
1. **官方日志里有、但摘要完全没提的条目**(重点是 Content/Additions、Balance、新机制类;纯 bug 修复只统计数量差异并列举最重要的 5 条以内)
2. **数值矛盾**(同一物品/机制两边数字不一致)
3. 摘要里有但官方日志没有的内容(通常是 zh wiki 补充细节,只需一句带过不算问题)

官方 1.4.4 主段落约 2000 行,你要系统性扫完,不要抽样。分类输出为紧凑清单,中文。

返回格式:
## 遗漏条目(按官方章节分组,每条一行:官方原文要点 → 应归入摘要哪个小节)
## 数值矛盾(条目、官方值、摘要值)
## 结论(摘要完整度百分比粗估 + 是否需要修订)
```

---

## 📎 Attachment · skill_listing · 2026-08-09T11:40:17.816Z

```
- dataviz: Use this skill whenever you are about to create ANY chart, graph, plot, dashboard, or data visualization, in ANY output medium — an HTML or React artifact, inline SVG, plotting code in any library (matplotlib, plotly, d3, Recharts, …), an image/PNG you will render and upload, or a chart shared into Slack. Read it BEFORE writing the first line of chart code, choosing chart colors, building a stat tile / meter / KPI row, or laying out a dashboard. Produces visualizations that read as one system — elegant, accessible, consistent in light and dark — using a brand-neutral placeholder palette you swap for your own. Teaches a design-system-agnostic method: a form heuristic, a color formula with a runnable validator, mark specs, and interaction rules. A validated default palette is documented in `references/palette.md` — swap that file's values for your brand's. Triggers on: "chart", "graph", "plot", "data viz", "visualization", "dashboard", "analytics", "visualize data", "categorical colors", "sequential / diverging palette", "stat tile", "sparkline", "heatmap", "legend", "axis", "tooltip", "chart colors", "color by series".
- update-config: Use this skill to configure the Claude Code harness via settings.json. Automated behaviors ("from now on when X", "each time X", "whenever X", "before/after X") require hooks configured in settings.json - the harness executes these, not Claude, so memory/preferences cannot fulfill them. Also use for: permissions ("allow X", "add permission", "move permission to"), env vars ("set X=Y"), hook troubleshooting, or any changes to settings.json/settings.local.json files. Examples: "allow npm commands", "add bq permission to global settings", "move permission to user settings", "set DEBUG=true", "when claude stops show X". For simple settings like theme/model, suggest the /config command.
- keybindings-help: Use when the user wants to customize keyboard shortcuts, rebind keys, add chord bindings, or modify ~/.claude/keybindings.json. Examples: "rebind ctrl+s", "add a chord shortcut", "change the submit key", "customize keybindings".
- simplify: Review the changed code for reuse, simplification, efficiency, and altitude cleanups, then apply the fixes. Quality only — it does not hunt for bugs; use /code-review for that.
- fewer-permission-prompts: Scan your transcripts for common read-only Bash and MCP tool calls, then add a prioritized allowlist to project .claude/settings.json to reduce permission prompts.
- loop: Run a prompt or slash command on a recurring interval (e.g. /loop 5m /foo, defaults to 10m) - When the user wants to set up a recurring task, poll for status, or run something repeatedly on an interval (e.g. "check the deploy every 5 minutes", "keep running /babysit-prs"). Do NOT invoke for one-off tasks.
- claude-api: Reference for the Claude API / Anthropic SDK — model ids, pricing, params, streaming, tool use, MCP, agents, caching, token counting, model migration.
TRIGGER — read BEFORE opening the target file; don't skip because it "looks like a one-liner" — whenever: the prompt names Claude/Anthropic in any form (Claude, Anthropic, Fable, Opus, Sonnet, Haiku, `anthropic`, `@anthropic-ai`, `claude-*`, `us.anthropic.*`, `[1m]`); the user asks about an LLM (pricing/model choice/limits/caching) — never answer from memory; OR the task is LLM-shaped with provider unstated (agent/MCP/tool-definition/multi-agent/RAG/LLM-judge/computer-use; generate/summarize/extract/classify/rewrite/converse over NL; debugging refusals/cutoffs/streaming/tool-calls/tokens).
SKIP only when another provider is being worked on (overrides all triggers): OpenAI/GPT/Gemini/Llama/Mistral/Cohere/Ollama named in the query; OR `grep -rE 'openai|langchain_openai|google.generativeai|genai|mistralai|cohere|ollama'` over the project hits (run this grep FIRST if no provider named — don't Read the file).
- run: Launch and drive this project's app to see a change working. Use when asked to run, start, or screenshot the app, or to confirm a change works in the real app (not just tests). First looks for a project skill that already covers launching the app; otherwise falls back to built-in patterns per project type (CLI, server, TUI, Electron, browser-driven, library).
- init: Initialize a new CLAUDE.md file with codebase documentation
- review: Review a GitHub pull request; for your working diff use /code-review
- security-review: Complete a security review of the pending changes on the current branch
```


---

## 🤖 Assistant · 2026-08-09T11:40:19.784Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by reading both files. The official changelog section is lines 2374-4368 (~2000 lines), and the Chinese summary. Let me read them in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:40:19.786Z · glm-x-preview-260804

```
我先读取官方 changelog 的指定段落和中文摘要文件。
```


---

## 🤖 Assistant · 2026-08-09T11:40:20.024Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '2374,2900p' \"~/Library/Application Support/Steam/steamapps/common/Terraria/changelog.txt\"",
 "description": "Read official changelog lines 2374-2900"
}
```


---

## 🤖 Assistant · 2026-08-09T11:40:20.030Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:40:20.238Z

**📎 ToolResult**

```
1	# Terraria 1.4.4「爱的劳动 Labor of Love」更新日志结构化摘要
2	
3	> 数据来源:中文 wiki MediaWiki wikitext(/tmp/tw-changelog/1.4.4.json 及 1.4.4.1~1.4.4.9.json)。
4	> 发布日期:1.4.4 于 2022-09-28;热修至 1.4.4.9(2022-11-17)。
5	> 注:官方 1.4.4 日志对微光 Shimmer / Aether 生态几乎未着墨(仅在热修 1.4.4.3 起大量出现 Shimmer 相关修正,以及 Terraformer、Aether Torch 等间接条目),本摘要忠实于原文,不额外编造;该体系规模评估见文末。
6	> 行尾 (→ 文件) 为该条目大概率影响的反编译源码文件(ShortName)。
7	
8	---
9	
10	# 一、主版本 1.4.4
11	
12	## 【新增内容-物品】
13	
14	- 添加 8 种史莱姆城镇宠物(Town pets),可集齐(→ NPC.cs, Item.cs, ItemID.cs)
15	- 添加超过 300 种新物品(官方原话"超过 300 种")(→ ItemID.cs, Item.cs)
16	- 添加超过 25 种新方块和墙(→ TileID.cs, WallID.cs)
17	- 添加超过 55 幅新绘画(paintings)(→ ItemID.cs, WorldGen.cs)
18	- 添加一些新的虚荣配饰和物品(→ ItemID.cs)
19	- 添加 3 套新家具系列(→ TileID.cs, ItemID.cs)
20	- 添加 Rubblemaker(碎块制造器,可放置 rubble 装饰)(→ Item.cs, TileID.cs)
21	- 添加 Shellphone(贝壳手机,魔法海螺+恶魔海螺+手机合成链)(→ Item.cs, Recipe.cs)
22	- 添加 Hand of Creation(创造之手,建筑配饰合集)(→ Item.cs, Recipe.cs)
23	- 添加 Echo Coating(回声涂层),并将 Illuminant Paint 改为 Illuminant Coating;涂层与涂料可互相叠加(→ Item.cs, TileID.cs, Player.cs)
24	- 添加 Lilith's Necklace(莉莉丝项链,狼变身配饰)(→ Item.cs)
25	- 添加 Poo(便便)及便便相关内容(→ Item.cs, TileID.cs)
26	- 添加 Terraformer(地形改造器,Clentaminator 升级)(→ Item.cs, ShimmerTransforms.cs)
27	- 添加 Biome Sight Potion(生物群落视域药水)(→ Item.cs, BuffID.cs)
28	- 添加 Flymeal(蝇食,可激怒城镇 NPC)(→ Item.cs, NPC.cs)
29	- 添加若干 pre-Hardmode 武器(→ ItemID.cs, Item.cs)
30	- 添加 Bottomless Honey Bucket(无尽蜂蜜桶)和 Honey Absorbant Sponge(蜂蜜超强吸收海绵)(→ Item.cs)
31	- 添加 Fart Kart(屁屁卡丁车矿车)(→ Item.cs, Projectile.cs)
32	- 添加 Resplendent Dessert(华丽甜点,史莱姆王子+史莱姆皇后双宠物)(→ Item.cs)
33	- 重新实现 Pixel Boxes(像素盒),由机械师出售,像素显示功能改善(→ Item.cs, TileID.cs)
34	- 重新实现被弃用的 Mini Star Cell Banner,由对应敌人掉落并提供增益;普通 Star Cell Banner 不再对 Mini Star Cell 生效(→ Item.cs, ItemDropRules)
35	- Mechanical Cart 条目隐含新物品 Minecart Upgrade Kit(机械矿车升级包,承接原机械矿车激光效果)(→ Item.cs, Projectile.cs)
36	- 添加 Jungle Birds(丛林鸟类生物)(→ NPCID.cs, NPC.cs)
37	- 添加 1 种新树(Ash Wood 树,配合 Ash Wood 家具/工具链)(→ TileID.cs, WorldGen.cs)
38	
39	## 【新增内容-NPC/Boss】
40	
41	- 8 种城镇史莱姆(Town Slimes;1.4.4.1 提到"第 8 个 Town Slime"对应成就 The Great Slime Mitosis,热修中出现 Squire/Diva/Surly/Cool/Mystic 等变体与变形来源)(→ NPCID.cs, NPC.cs)
42	- 传送敌怪 AI 引入"玩家移动预测"传送避让系统(详见机制系统改动)(→ NPC.cs, Player.cs)
43	- Nurse 评论玩家近期死亡频率;Painter 拆分两个商店菜单;NPC 死亡后无条件重生(详见 NPC 与 UI 节)(→ NPC.cs, Main.cs)
44	- Lifeform Analyzer 稀有度体系重排,新增 Voodoo Demon 展示(→ NPC.cs, Player.cs)
45	
46	## 【新增内容-方块/世界内容】
47	
48	- 添加 Crimson Jungle Grass(血腥丛林草)与 Corrupt Jungle Grass(腐化丛林草);腐化/血腥化丛林草不再退化为泥土,只蔓延草(→ TileID.cs, WorldGen.cs)
49	- 添加 25+ 新方块与墙(含 3 套新家具、Ash Wood 系列等)(→ TileID.cs, WallID.cs)
50	- 新特殊种子:Remix(Don't dig up,地狱出生向上探索)、No Traps(无陷阱)、Everything(Get fixed boi,合集)(→ WorldGen.cs, Main.cs)
51	- For the Worthy 大改:经典自动按专家、专家自动按大师处理;可 100% 完成图鉴(→ NPC.cs, WorldGen.cs)
52	- Not the Bees:补入蜘蛛洞生成、全鱼类可捕、可 100% 完成图鉴(→ WorldGen.cs)
53	- The Constant:黑暗伤害 50→250,受伤等待 8 秒→4 秒;饥饿状态吃蘑菇重置为完整持续时间 Peckish(→ Player.cs, BuffID.cs)
54	- Celebrationmk10:一系列喜庆化改动(→ WorldGen.cs, Main.cs)
55	- 地下沙漠最小尺寸由最大尺寸的 50% 提高到 75%(→ WorldGen.cs)
56	
57	## 【物品与数值平衡】
58	
59	### 近战武器
60	
61	- 全部阔剑类(含镐/斧/锤/锤斧):击中改用局部无敌帧,发射弹幕的剑不再阻止其穿透弹幕贴脸命中(→ Item.cs, Player.cs, Projectile.cs)
62	- 全部链枷:旋转击退由正常击退的 25% 提至 35%;旋转命中频率 3 次/秒→4 次/秒(原本 4 次/秒者→5 次/秒)(→ Item.cs, Projectile.cs)
63	- 7 种金属阔剑全面加强:Copper(伤害 8→9、使用 23→21、尺寸 1→1.1)、Tin(9→10、22→20、1→1.1)、Iron(10→12、22→20、1→1.15、击退 5→5.5)、Lead(11→13、21→20、1→1.15、5→5.5)、Silver(11→14、21→20、1→1.2、5→6)、Tungsten(12→14、20→19、1.025→1.2、5→6)、Gold(13→15、20→18、1.05→1.25、5→6.5)、Platinum(15→16、19→17、1.075→1.25、5→6.5)(→ Item.cs)
64	- 木质剑系:Wooden(使用 25→20、尺寸 0.95→1.0、击退 4→5)、Boreal(使用 23→20、击退 5→6)、Palm/Rich Mahogany(使用 23→19、击退 5→6)、Ebonwood/Shadewood(伤害 10→11、使用 21→19、击退 5→6)、Pearlwood(伤害 11→30、使用 21→15、可自动挥舞)(→ Item.cs)
65	- Cactus Sword:伤害 8→10,使用 32→30(→ Item.cs)
66	- 回旋镖系(短距 DPS 削弱、伤害上调):Wooden Boomerang 伤害 8→10、使用 16→20;Enchanted 13→17、15→20;Shroomerang 14→23、15→20、掉落 1/100→1/40;Ice Boomerang 16→21、15→20、新增几率 Frostburn;Flamarang 32→49、On Fire! 几率 20%→50%、15→20(→ Item.cs)
67	- Zombie Arm(12→15、23→22、1→1.2、4.25→5.5)、Bone Sword(16→19、1.05→1.2、4.5→5.5)、Bat Bat(31→36)、Katana(16→18、22→20、1→1.1)、Candy Cane Sword(16→19)、Fruitcake Chakram(14→19)、Bladed Glove(12→14)、Bloody Machete(15→20)、Mandible Blade(14→16、1→1.1)、Falcon Blade(尺寸 1.05→1.175)(→ Item.cs)
68	- Gladius:击退 0.5→3,掉落 1/40→1/20;Purple Clubberfish:伤害 24→35、击退 7→8;Tentacle Spike:19→20、使用 23→21(→ Item.cs)
69	- Storm Spear:伤害 12→14,弹幕伤害由 1.25 倍基础→1.5 倍;Trident 水下挥舞发光(→ Item.cs, Projectile.cs)
70	- Light's Bane:重做为斜向短程斩切弹幕(造成基础伤害一半),伤害 18→16(→ Item.cs, Projectile.cs)
71	- Blood Butcherer:重做为叠层流血(Blood Butchered,最多 5 层、每层 4 DPS、持续 9 秒)(→ Item.cs, Projectile.cs, BuffID.cs)
72	- The Rotted Fork:伤害 14→17,矛尖新增随近战速度变化的震波(→ Item.cs, Projectile.cs)
73	- Phaseblades(全色):伤害 25→26,使用 25→18;Phasesabers(全色):伤害 42→48,使用 20→16,合成水晶碎块 50→25(→ Item.cs, Recipe.cs)
74	- Starfury:星星下落加速 25%,可穿墙落到光标位置(→ Item.cs, Projectile.cs)
75	- Blade of Grass:新增上旋叶刃弹幕(低伤高破防),伤害 28→18,使用 30→20,击退 3→4.5;配方改为 3 Vine、Jungle Spore 12→15(→ Item.cs, Recipe.cs, Projectile.cs)
76	- Thorn Chakram:中毒几率 20%→50%(→ Item.cs)
77	- Bee Keeper:伤害 26→30,贴图加大(→ Item.cs)
78	- Lucy the Axe:伤害 26→27,使用 17→15,移除 useTurn,闲聊频率降低(→ Item.cs)
79	- Muramasa:命中后追加半伤斩切,伤害 26→24(→ Item.cs, Projectile.cs)
80	- Valor:伤害 22→28(→ Item.cs)
81	- Fiery Greatsword 更名 Volcano:命中触发烈焰爆炸 AOE,使用 30→40(→ Item.cs, Projectile.cs)
82	- Night's Edge:剑刃周围新增伤害能量环,能量环朝瞄准方向二次旋转(→ Item.cs, Projectile.cs)
83	- Dark Lance:伤害 29→34,新增矛尖震波,改造成 Shadowflame(→ Item.cs, Projectile.cs)
84	- Breaker Blade:伤害 43→70,使用 29→35,尺寸 1.05→1.15,对满血目标特效倍率 +100%→+150%(→ Item.cs)
85	- 6 种 Hardmode 金属剑上调:Cobalt(39→40、23→19、1.1→1.2、3.85→5)、Palladium(45→49、25→22、1.125→1.2、4.75→5.5)、Mythril(49→50、26→20)、Orichalcum(50→59、25→22、1.17→1.22)、Adamantite(56→61、26→21、1.2→1.25)、Titanium(58→61、25→20、1.2→1.25)(→ Item.cs)
86	- 6 种 Hardmode 金属长柄武器上调:Cobalt Naginata 29→44、Palladium Pike 32→44、Mythril Halberd 35→45、Orichalcum Halberd 36→46、Adamantite Glaive 38→49、Titanium Trident 40→48(→ Item.cs)
87	- Cutlass:伤害 49→53,使用 17→16(→ Item.cs)
88	- Frostbrand:弹幕冷却 55 帧→30 帧,弹幕改造成 Frostbite,穿透 2→3,改独立无敌帧(→ Item.cs, Projectile.cs)
89	- Ice Sickle:伤害 42→50,弹幕范围 +50%,弹幕伤害 100%→50% 基础,改独立无敌帧,穿透 5→3(→ Item.cs, Projectile.cs)
90	- Bladetongue:Ichor 弹幕穿透无限→5,改独立无敌帧(→ Item.cs, Projectile.cs)
91	- Slap Hand:伤害 35→55,使用 21→20(→ Item.cs)
92	- Hel-Fire:改造成 Hellfire(原 On Fire!)(→ Item.cs, BuffID.cs)
93	- Amarok:改造成 Frostbite(原 Frostburn)(→ Item.cs, BuffID.cs)
94	- Chain Guillotines:链条提速约 25%、飞行距离 +50%(→ Projectile.cs)
95	- Bananarang:由可堆叠 10 个改为单体(可获得词缀),伤害 55→45,售价上调,小丑掉落 10%(→ Item.cs, ItemDropRules)
96	- Sergeant United Shield:击退 0→2(→ Item.cs)
97	- Beam Sword:弹幕冷却 60 帧→35 帧,可自动挥舞,移除 useTurn 与强制转向(→ Item.cs)
98	- Excalibur:新增剑刃能量环,伤害 66→72(→ Item.cs, Projectile.cs)
99	- Gungnir:伤害 42→61,新增矛尖震波(→ Item.cs, Projectile.cs)
100	- Light Disc:由可堆叠 5 个改为单体(可获词缀),配方×5、售价×5,伤害 57→60,使用 15→14,同时上限 5→6,弹速/距离 13→16(→ Item.cs, Recipe.cs, Projectile.cs)
101	- True Night's Edge:新增能量环,改发射大旋转能量圈(长距多段命中),伤害 105→70,使用 26→32(→ Item.cs, Projectile.cs)
102	- True Excalibur:新增大能量环,不再发射弹幕,伤害 70→72,使用 16→18(→ Item.cs)
103	- Brand of the Inferno:贴图加大,改造成 Hellfire(→ Item.cs)
104	- Chlorophyte Saber:弹幕冷却 42 帧→28 帧,弹幕伤害 100%→70% 基础,持续 +50%,改独立无敌帧;Claymore/Partisan 同改独立无敌帧(→ Item.cs, Projectile.cs)
105	- Ghastly Glaive:降低矛本体无敌帧(更频繁命中)(→ Projectile.cs)
106	- Death Sickle:降低击退防止击出镰刀范围(→ Item.cs)
107	- Butcher's Chainsaw:链条与火花改独立无敌帧(单体伤害大增),火花改 Hellfire(→ Item.cs, Projectile.cs)
108	- Terra Blade(重做):伤害 115→85,使用 14→18,新增剑刃能量环,每次挥舞发射中远程快速绿色能量斩(替代按冷却剑气)(→ Item.cs, Projectile.cs)
109	- Scourge of the Corruptor:小吞噬者提速增追踪,均产 2.67→3 个(范围 2-4)(→ Projectile.cs)
110	- Paladin's Hammer:可自动挥舞(→ Item.cs)
111	- Keybrand:伤害 85→105,额外暴击 14%→17%,伤害缩放上限降低(高血量敌人受更高伤害)(→ Item.cs)
112	- The Horseman's Blade:新增能量环,伤害 75→150,南瓜伤害 100% 基础(原 150%),雕像怪不再产南瓜(→ Item.cs, Projectile.cs)
113	- North Pole:使用 25→30,生成弹幕减半,矛弹全额基础伤害、雪花 70%(原 80%/63%),移除风影响、落点半随机,存在时间缩短(→ Item.cs, Projectile.cs)
114	- Christmas Tree Sword:弹幕伤害 75%→100% 基础(→ Item.cs, Projectile.cs)
115	- Flairon:泡泡破裂前持续 +33%,锁定距离 +30%(→ Projectile.cs)
116	- Starlight:范围受 Titan Glove 与尺寸词缀影响(→ Item.cs, Player.cs)
117	- Influx Waver:伤害 110→100,二段弹幕跟随目标移动(→ Item.cs, Projectile.cs)
118	- Flying Dragon:使用 25→20,无视线时不再有伤害惩罚(→ Item.cs, Projectile.cs)
119	- Star Wrath:伤害 110→170,落星伤害 2 倍→1 倍基础,落星改局部无敌帧(→ Item.cs, Projectile.cs)
120	- Meowmere:使用 16→14,弹幕 1.25 倍基础伤害,改局部无敌帧(→ Item.cs, Projectile.cs)
121	- Terrarian:悠悠球与球体弹幕改独立无敌帧(→ Projectile.cs)
122	- 三种骑枪:Jousting Lance 56→60、Hallowed 78→90、Shadow 108→130(→ Item.cs)
123	
124	### 远程武器与弹药
125	
126	- Flintlock Pistol:伤害 10→13,击退 0→1;Musket:使用 36→32,不再自动开火;Undertaker:伤害 15→22,使用 23→20,击退 1→2(→ Item.cs)
127	- Blood Rain Bow:弹幕发光;Harpoon:弹幕改局部无敌帧(→ Projectile.cs)
128	- Spiky Ball:伤害 15→16,穿透 6→7;Star Cannon:击退 0→3(→ Item.cs)
129	- The Bee's Knees:等效使用时间 24→23(修代码不一致)(→ Item.cs)
130	- Quad-Barrel Shotgun:伤害 17→14,弹数 6→8,其一必定精准(→ Item.cs, Projectile.cs)
131	- Handgun:伤害 17→26,使用 10→15;Phoenix Blaster:伤害 24→33,使用 11→17(→ Item.cs)
132	- 6 种 Hardmode 连弩上调:Cobalt(32→35、24→23)、Palladium(34→37、23→22)、Mythril(36→39、22→20)、Orichalcum(38→40、21→19)、Adamantite(40→42、19→18)、Titanium(41→43、18→17)(→ Item.cs)
133	- Marrow:伤害 50→53,可自动开火;Ice Bow:使用 16→14(→ Item.cs)
134	- Hallowed Repeater:伤害 53→50,使用 16→17(→ Item.cs)
135	- Flamethrower:弹幕改局部无敌帧,伤害计算前无视 15 防御,视觉与碰撞箱重做,改 Hellfire(→ Item.cs, Projectile.cs)
136	- Super Star Shooter:星斩改独立无敌帧,星斩伤害 50%→75% 基础(→ Item.cs, Projectile.cs)
137	- Pulse Bow:伤害 85→80,改为三机械 Boss 后出售(原 Plantera 后)(→ Item.cs, NPC.cs)
138	- Phantom Phoenix:凤凰弹幕改 Hellfire(转化出的火箭仍 On Fire!)(→ Item.cs, Projectile.cs)
139	- Venus Magnum:使用 8→9,可自动开火(→ Item.cs)
140	- Rocket Launcher:伤害 45→55(→ Item.cs)
141	- Elf Melter:伤害 60→53,喷焰次数 6→5,改局部无敌帧,无视 15 防御,穿透 3→4,改 Frostbite,视觉重做(→ Item.cs, Projectile.cs)
142	- Electrosphere Launcher:电球导弹不再造成直接伤害(仅转电球)(→ Projectile.cs)
143	- Aerial Bane:仅 tooltip 显示方式改动(基础伤害改显示地面伤害)(→ Item.cs)
144	- Celebration MK2:伤害 40→50,修复红色导弹每帧多段命中(→ Item.cs, Projectile.cs)
145	- Archery Potion:弓伤害加成 1.2 倍→1.1 倍(→ Item.cs, BuffID.cs)
146	- Ichor Dart 伤害 12→10;Cursed Dart 伤害 10→9;修复 Ichor Dart 近距每帧命中(→ Item.cs, Projectile.cs)
147	- Exploding Bullet:不再对自己造成伤害(→ Projectile.cs)
148	- Frostburn Arrow:弹药伤害 9→7(→ Item.cs)
149	- Holy Arrow:星伤 50%→33% 基础(→ Item.cs)
150	- 集束火箭(全变体):破片伤害 33%→50%(→ Item.cs, Projectile.cs)
151	
152	### 魔法武器
153	
154	- 基础魔力再生重做:移动基础再生翻倍以上;静止/药水加成降 1/3(总量持平,最低再生率大幅提高)(→ Player.cs, Main.cs)
155	- Amethyst Staff:魔耗 3→5、伤害 14→15、使用 40→37;Topaz Staff:魔耗 4→5、15→16、38→36;Sapphire Staff:魔耗 5→6、17→18,可自动开火(→ Item.cs)
156	- Thunder Zapper:伤害 12→20,魔耗 5→7,击退 2→3(→ Item.cs)
157	- Crimson Rod:云持续 5 分钟,改独立无敌帧,魔耗 10→30;Nimbus Rod:云持续 5 分钟,伤害 36→30,改独立无敌帧,魔耗 10→30,穿透无限→5;Clinger Staff:持续 5 分钟,改独立无敌帧(→ Item.cs, Projectile.cs)
158	- Weather Pain:穿透 12→15,命中间隔 20→25 帧,持续 +2 秒(→ Projectile.cs)
159	- Bee Gun/Wasp Gun/Last Prism:获得占位击退值以拿词缀(→ Item.cs)
160	- Magic Missile:伤害 27→35;Aqua Scepter:伤害 16→27、击退 5→7、魔耗 6→7、范围大增(→ Item.cs)
161	- Flower of Fire:弹速/距离 6→7.5,额外弹射 1 次(→ Item.cs)
162	- Zapinators(灰/橙):使用 37→36(→ Item.cs)
163	- Magic Dagger:伤害 40→35,可自动开火,改局部无敌帧,平飞距离 +50%(→ Item.cs, Projectile.cs)
164	- Cursed Flames:伤害 50→55;Golden Shower:伤害 21→30(→ Item.cs)
165	- Flower of Frost:弹速/距离 7→9,改 Frostbite(→ Item.cs)
166	- Blood Thorn:荆棘加大、持续 +40%、可自平台生成、穿透 3→4,移除 1.4 遗留的每次命中掉伤系统(→ Item.cs, Projectile.cs)
167	- Meteor Staff:魔耗 13→9;Frost Staff:使用 16→12,改 Frostbite(→ Item.cs)
168	- Shadowflame Hex Doll:伤害 40→32,改局部无敌帧,必有一触手朝光标(→ Item.cs, Projectile.cs)
169	- Spirit Flame:AOE 范围翻倍,持续 +25%(→ Projectile.cs)
170	- Magical Harp:击退 0.25→2(→ Item.cs)
171	- Tome of Infinite Wisdom:伤害 32→36,龙卷 2 倍→1.75 倍基础(→ Item.cs)
172	- Wasp Gun:蜂速约 +25%,独立无敌帧,占位击退(→ Item.cs, Projectile.cs)
173	- Leaf Blower:魔耗 4→5(→ Item.cs)
174	- Inferno Fork:伤害 65→70,AOE 75% 基础(原 65%),爆炸持续加长,击退 8→5,改 Hellfire(→ Item.cs, Projectile.cs)
175	- Shadowbeam Staff:伤害 60→80;Spectre Staff:改独立无敌帧(→ Item.cs, Projectile.cs)
176	- Magnet Sphere:持续 11→15 秒,球体改为撞墙反弹(→ Projectile.cs)
177	- Rainbow Gun:持续 20→40 秒,改独立无敌帧(→ Item.cs, Projectile.cs)
178	- Toxic Flask:伤害 46→52,使用 28→45,弹速/距离 9→14,气体云视觉大改、持续更长、不穿墙改为区域扩散(→ Item.cs, Projectile.cs)
179	- Heat Ray:伤害 80→90;Bat Scepter:蝙蝠追踪速度约 +30%(→ Item.cs, Projectile.cs)
180	- Stellar Tune:击退 0→1.5(→ Item.cs)
181	- Nightglow:未追踪弹幕持续约 +50%,开始追踪时重置持续(→ Projectile.cs)
182	- Bubble Gun:弹速/距离 11→15,泡泡持续翻倍,魔耗 4→5(→ Item.cs)
183	- Razorblade Typhoon:伤害 90→85,魔耗 16→20,持续 3→2.5 秒(→ Item.cs, Projectile.cs)
184	- Nebula Blaze:击退 0→3(→ Item.cs)
185	- Lunar Flare:魔耗 13→9(→ Item.cs)
186	
187	### 召唤武器
188	
189	- Leather Whip:击退 0.5→1,价格 15 金→10 金(→ Item.cs, NPC.cs)
190	- Snapthorn:伤害 18→19(注:1.4.4.8 勘误实际仍为 18),击退 1→1.5,Whip Speed buff(Jungle's Fury)20%→12%;配方 Stinger 12→15、Jungle Spore 3→12(→ Item.cs, Recipe.cs)
191	- Spinal Tap:伤害 29→27;Firecracker:伤害 40→37,改 Hellfire(→ Item.cs)
192	- Cool Whip:伤害 50→45,标记伤害 6,雪花伤害 10→15 且速度 +50%,改 Frostbite(→ Item.cs, Projectile.cs)
193	- Durendal:使用 30→28,buff 35%→25%;Dark Harvest:使用 30→27,buff(Harvest Time)50%→35%,Reaping 标记等效 10 伤害并扩散到邻近目标(→ Item.cs, Projectile.cs)
194	- 修复鞭攻速 buff 错误作用于近战武器(→ Player.cs, Projectile.cs)
195	- Blade Staff:因高频+破防,仅获 75% 鞭标记加成(→ Item.cs, Projectile.cs)
196	- Sanguine Staff:击退 8→3,修复贴脸多段命中(→ Item.cs, Projectile.cs)
197	- 全部召唤法杖:可自动开火,但召唤物不再无视攻击冷却(→ Item.cs, Projectile.cs)
198	- Optic Staff:Retinamini 激光不再穿透,Retinamini 伤害 24→26,Spazmatism 30→21,冲刺更灵活,返回更快(→ Item.cs, Projectile.cs)
199	- Deadly Sphere:伤害 50→40,改局部无敌帧,仇恨范围增大、冲刺改善,修复脱仇,返回更快(→ Item.cs, Projectile.cs)
200	- Pygmy Staff:Pygmy 伤害 34→40,矛提速,预判瞄准,矛必带 Acid Venom(原 Poisoned),返回更快(→ Item.cs, Projectile.cs)
201	- Desert Tiger Staff:步行追击 +25%;Raven Staff:返回速度随玩家移速(→ Projectile.cs)
202	- Tempest Staff:返回途中持续射击,返回速度随玩家移速,龙卷改 10 帧独立无敌帧(原 20 帧全局)(→ Projectile.cs)
203	- Xeno Staff:开火间隔 33→36,UFO 不必完全返回即可传送攻击新目标,返回速度随玩家移速(→ Item.cs, Projectile.cs)
204	- 全部哨兵:鞭标记与效果适用于哨兵伤害;持续时间 2 分钟→10 分钟(→ Projectile.cs, Player.cs)
205	- Houndius Shootius/Explosive Trap/Flameburst 哨兵:召唤后开火有短暂延迟;Ballista:伤害 27/67/140→30/74/156,攻击延迟 180→160,击退 4.5→4.7(→ Item.cs, Projectile.cs)
206	- Lightning Aura:因高频+无视防御,仅获 50% 鞭标记加成,新增占位击退(→ Item.cs, Projectile.cs)
207	- Frost Hydra Staff:弹幕改 Frostbite,弹速 +50%(→ Item.cs, Projectile.cs)
208	- Rainbow Crystal Staff:改独立无敌帧(→ Projectile.cs)
209	- Lunar Portal Staff:伤害 50→100,光束冷却 90→30(可叠光束),激光转速加快(→ Item.cs, Projectile.cs)
210	
211	### 盔甲
212	
213	- Snow armor(蓝/粉):部件防御 1/2/1→3/3/3(共 9),新增免疫 Chilled/Frozen 套装奖励,部件掉落 1/150→1/30(→ Item.cs, Player.cs)
214	- Mining armor:头盔防御 1→2,30% 采矿速度拆分为三件+套装奖励各 10%(→ Item.cs)
215	- Angler armor:tooltip 显示钓鱼力,新增降低敌怪生成率套装奖励(→ Item.cs, NPC.cs)
216	- Shadow armor:套装奖励重做(灵活速度加成,空中也有效),部件 +7% 近战速度替换为 +5% 暴击(→ Item.cs, Player.cs)
217	- Crimson armor:部件伤害加成 2%→3%(→ Item.cs)
218	- Obsidian armor:鞭范围 50%→30%,鞭速度 35%→15%(→ Item.cs)
219	- Cobalt armor:Hat 防御 2→3、Helmet 12→14、Mask 4→5、Breastplate 8→10(→ Item.cs)
220	- Orichalcum armor:Boots 新增 8% 伤害加成(→ Item.cs)
221	- Titanium armor:碎片每 10 ticks 最多 1 个(上限 6/秒),雕像怪不产碎片(→ Player.cs, Projectile.cs)
222	- Hallowed armor:Holy Protection 改为闪避后 30 秒冷却(不再 25% 几率由攻击触发)(→ Player.cs)
223	- Chlorophyte armor:叶水晶改为即时命中能量束,开火有距离限制(→ Player.cs, Projectile.cs)
224	- Tiki armor:Mask 新增 10% 鞭范围,套装奖励新增 20% 鞭范围(→ Item.cs)
225	- Shroomite armor:火箭头盔新增"特种武器"类别(镖枪/火焰喷射器/星星炮等),修复 tooltip 伤害显示多 1(→ Item.cs, Player.cs)
226	- Spectre armor:Hood 队友治疗范围 1200→3000,形状改圆形(→ Item.cs, Projectile.cs)
227	- Beetle armor(Scale Mail):Beetle's Might 充能时长 +33%,升 3 级更快(→ Item.cs, Player.cs)
228	- Solar armor:日耀冲锋/爆炸伤害受近战伤害加成(→ Player.cs)
229	- Stardust armor:Helmet +1 哨兵数,Chestplate/Leggings 各 +15% 鞭范围(→ Item.cs)
230	
231	### 配饰、坐骑、工具、图格
232	
233	- Frog Leg 系:同源配饰可叠加(相加),跳跃速度加成 48%→32%,摔落保护等比下调(→ Item.cs, Player.cs)
234	- Squire's Shield/Apprentice's Scarf:改由 T1/T3 Dark Mage 掉落(pre-Hardmode 可得),Classic 50% / Expert+ 100%,移出 Ogre 掉落池(→ ItemDropRules)
235	- Hive Pack:大黄蜂开火频率约 +30%,Wasp Gun 伤害 31→36、蜂破防 10→15(→ Item.cs, Projectile.cs)
236	- Magiluminescence/Soaring Insignia:移动力属性奖励各降 25%(无限飞行不变)(→ Item.cs)
237	- Spore Sac:孢子大幅提速,侦测范围 +20%(→ Projectile.cs)
238	- Lucky Horseshoe 回退到天空箱(Skyware Chest);Fledgling Wings 改为 1/40 次要物品;天空箱(Sky Crate)同步更新(→ WorldGen.cs, ItemDropRules)
239	- Leaf Wings:改为击败 Plantera 后巫医出售,属性对齐罕见 Plantera 前翅膀(Flame/Butterfly/Bee/Bat),售价 1.5 铂金(→ NPC.cs, Item.cs)
240	- Magic Quiver 系:伤害加成改相加(原相乘),弹速加成同时作用于弹药速度(→ Item.cs, Player.cs)
241	- Philosopher's Stone/Charm of Myths:药水病冷却改为按装备时刻动态等比缩放(穿戴半分钟再卸下仅减 10 秒而非 15 秒)(→ Item.cs, Player.cs)
242	- Volatile Gelatin:弹道更远更平,开火 50 帧→40 帧(每秒 1.2 次→1.5 次)(→ Projectile.cs)
243	- Magma Skull/Molten Skull Rose:配方改用 Lava Charm(原 Magma Stone),改为提供临时熔岩免疫(原攻击加 Hellfire)(→ Item.cs, Recipe.cs)
244	- Hellfire Treads:改由 Flame Waker Boots+Spectre Boots 合成(原 Flame Waker Boots+Lava Waders),失去岩浆行走,获得 Hermes 奔跑+Rocket 飞行,跑动产生火花(→ Item.cs, Recipe.cs)
245	- Lava Waders:可用 Molten Skull Rose+水上行走靴合成(→ Recipe.cs)
246	- Fairy Bell:妖精移速 3.5→6(→ Projectile.cs)
247	- Turtle Mount:速度 +150%,游泳 +66%,跳跃 +20%,水下提供呼吸(→ Item.cs, Player.cs)
248	- Gelatinous Pillion:水平飞行速度约 -30%,行走约 -10%(→ Item.cs)
249	- 全部矿车:更高难度下更高伤害与击退,更容易撞飞敌人(→ Projectile.cs, Player.cs)
250	- Drill Mount:右键可拆墙,挖掘速度约 3 倍(→ Player.cs)
251	- Spectre Pickaxe:采矿速度 10→8;全部无击退钻头获得占位击退以拿词缀(→ Item.cs)
252	- The Grand Design:配方改用 Mechanical Ruler(自带网格显示)(→ Recipe.cs, Item.cs)
253	- Magic Conch/Demon Conch:动画速度对齐 Magic Mirror(→ Item.cs)
254	- Bottomless Water Bucket/Super Absorbant Sponge:完成 10 个渔夫任务即可 pre-Hardmode 获得(BWB 第 25 个任务必得)(→ ItemDropRules)
255	- Enchanted Sundial:充能时发光,自然血月/日食开始时立即充能,可被电线触发(→ Item.cs, TileID.cs)
256	- Pylons:可用最大距离增大(消除"能开启却不能用"的情况);月总召唤期间可用(→ Item.cs, Main.cs)
257	- Snowball Launcher:无需弹药,冷却 10 帧→7 帧,弹道更远下坠更少(→ Item.cs, Projectile.cs)
258	- Star in a Bottle:魔力再生 1/秒→5/秒,并缩短施法后再生延迟(→ TileID.cs, Player.cs)
259	- 职业 Buff 站(Sharpening Station/Crystal Ball/Ammo Box/Bewitching Table):增益持续到死亡/取消/退出(无时限)(→ Player.cs, TileID.cs)
260	- Ammo Box:Hardmode 军火商出售(移出旅行商人),15 金→10 金;War Table 改为 Buff 站(+1 哨兵,无限时)(→ NPC.cs, TileID.cs, Player.cs)
261	
262	### 增益、减益、食物、药水
263	
264	- Poisoned(对敌):DPS 2→6(对玩家不变)(→ BuffID.cs, NPC.cs)
265	- Hardmode 火/霜来源大批改 Hellfire/Frostbite:Flamethrower、Elf Melter、Hel-Fire、Inferno Fork(弹幕+爆炸)、Phantom Phoenix(仅凤凰弹)、Flameburst Cane/Staff、Butcher's Chainsaw 火花、Brand of the Inferno、Amarok、Flower of Frost、Firecracker、Cool Whip(→ Item.cs, Projectile.cs, BuffID.cs)
266	- Crate Potion:持续 3→4 分钟,对板条箱几率效果 +50%(总体多 25%)(→ Item.cs, BuffID.cs)
267	- Warmth Potion:新增对 Ice Bat/Ice Tortoise/Ice Mimic/Yeti 的接触伤害保护(→ Item.cs, BuffID.cs)
268	- Calming Potion:降生成效果 +33%,持续 8→12 分钟(→ Item.cs)
269	- Inferno Potion:伤害 10→20,改 Hellfire(→ Item.cs)
270	- Luck Potion:持续/阈值 3/5/10→5/10/15 分钟(→ Item.cs)
271	- Spelunker Potion:激活时雕像与绘画发光(→ Item.cs, TileDrawing.cs)
272	- Bottled Honey:额外提供 15 秒 Honey buff(→ Item.cs)
273	- Strange Brew:随机回 70-120 血,药水病 40-70 秒随机,几率性无敌(时间越长几率越低),不再回蓝(→ Item.cs)
274	- 食物调整:Froggle Bunwich(2 级)8→6 分钟;Seafood Dinner 由 4 分钟 3 级改 14 分钟 2 级;Grub Soup(2 级)10→14 分钟;Potato Chips(1 级)18→25 分钟;Carton of Milk(1 级)15→20 分钟;Hotdog 由 20 分钟 2 级改 12 分钟 3 级(→ Item.cs)
275	
276	### 掉落几率与获取来源
277	
278	- 旅行商人:Hardmode 必多 1 稀有物品栏(仅含四类少见物品池);任何时期必多 1 绘画栏(绘画移出其它栏);Celestial Magnet、Ammo Box 移出其商店;Pad Thai 1 级→2 级、Pho 1 级→3 级、Zapinators 5 级→3 级;圣诞节绘画改为击败雪霜军团后全年售卖(→ NPC.cs)
279	- Celestial Magnet:改在 Skyware Chest/Sky Crate 作为主要物品(→ WorldGen.cs, ItemDropRules)
280	- Waldo 等罕见地下小屋绘画生成频率大增(仍为该尺寸组最罕见);其它"较罕见"地下小屋绘画稀有度统一(→ WorldGen.cs)
281	- 宝箱主要物品池 12→10(Throwing Knife/Glowstick 降为次要);骷髅商人按月相售卖木箱主要战利品(→ WorldGen.cs, NPC.cs)
282	- Living Wood Chest 含矿车几率 1/10→1/6(向日葵/瓢虫矿车各半);Mushroom Chest 必含独特物品之一(蘑菇矿车/蘑菇虚荣各 50%)(→ WorldGen.cs)
283	- Treasure Magnet:Shadow Chest/Obsidian Lock Box 改 1/5 次要物品;Demonic Hellcart 可于 Obsidian/Hellstone Crate 额外掉落;Shark Bait 改 1/10 次要物品(→ WorldGen.cs, ItemDropRules)
284	- 摇树掉水果几率 1/15→1/12(→ WorldGen.cs)
285	- 掉落率上调:Diving Helmet 1/50→1/20、Pocket Mirror 1/100→1/40(专家翻倍 1/50→1/20)、Medusa Head 1/50→1/25、Turtle Shell 1/17→1/12、Brain Scrambler 1/100→1/30、Deadly Sphere Staff 1/40→1/30、Fire Feather 1/75→1/50、Bone Feather 1/450→1/300、Giant Harpy Feather 1/200→1/150、Tattered Bee Wing 1/150→1/100、Obsidian Rose 1/50→1/20、Frozen Turtle Shell 1/100→1/50、Ice Sickle 1/180→1/100(→ ItemDropRules)
286	- Monster Meat:1/1000→1/1500(The Constant 1/200→1/500)(→ ItemDropRules)
287	- Flinx Fur:50% 掉 1-3 个→100% 掉 1-2 个(总体 +50%);专家 90%→100% 掉 1-3 个(→ ItemDropRules)
288	- EoW/BoC 掉落重构:BoC 专家/大师 Crimtane+Tissue Sample 总量约砍半(原本近两倍);击杀/宝袋比例:专家 50/50,大师 25/75;经典不变(→ ItemDropRules, NPC.cs)
289	- 极罕见海盗掉落:全部翻倍(Pirate Captain 的更高几率也翻倍);Flying Dutchman 额外 1/15 掉其一(Coin Gun 1/50);Flying Dutchman 必掉一件黄金家具,黄金平台每叠数量提高(→ ItemDropRules)
290	- Reindeer Bells:Ice Queen 掉率翻倍(→ ItemDropRules)
291	- 岩浆箱(Obsidian/Hellstone Crate)略少见:1/5→1/6(→ ItemDropRules)
292	- 生物群落箱优先于 Gold Crate(两者实际几率不变)(→ ItemDropRules)
293	- Wooden Crate:木箱主要战利品 1/45→1/20,Umbrella 替换为 Step Stool(→ ItemDropRules)
294	- 钓鱼箱矿石下调:Wooden 约 -40%、Iron 与生物群落箱约 -30%、Gold 约 -20%(→ ItemDropRules)
295	- Gold/Titanium Crate:Life Crystal 1/15→1/8;Enchanted Sword 1/50→1/30(Titanium 1/15)(→ ItemDropRules)
296	- Oasis/Mirage Crate:极低几率额外掉 Sandstorm in a Bottle(→ ItemDropRules)
297	- Pharaoh's set 在金字塔箱中变稀有(相对提高其它物品频率)(→ WorldGen.cs)
298	- Gold Worm 用作鱼饵时消耗仅 1/20(→ Item.cs)
299	- OOA Ogre 武器:T2 掉率 33%→50%(专家/大师 50%→100%),T3 1/6→1/4(→ ItemDropRules)
300	- 宝袋开发者套装:1/20→1/16(→ ItemDropRules)
301	- Frost Daggerfish 单次钓获数量提高(→ ItemDropRules)
302	- Seahorse 在更多海洋类型/形状/状态生成;Gem Critter 按宝石稀有度生成;Water Strider 生成率增加且风速上限 10→20 mph;蝴蝶日几率提高;宝藏仙灵 Hardmode 生成率降 2/3;松露虫/彩虹蜉蝣生成受 Luck 影响;丛林小动物在丛林城镇生成率降低(→ NPC.cs, Main.cs)
303	- The Bride/The Groom(墓地生成)非血月也掉 Bloody Tear(→ ItemDropRules)
304	- Teleporter 改为机械师 pre-Hardmode 出售(原蒸汽朋克人)(→ NPC.cs)
305	- Digging Molecart:动物学家图鉴 35% 即售(原 60%)(→ NPC.cs)
306	- Bast Statue 可在地下沙漠小屋作为家具生成(→ WorldGen.cs)
307	
308	### 配方与价格
309	
310	- Celestial Sigil:每类月亮碎片 20→12(→ Recipe.cs)
311	- 新增:Cloud in a Bottle+Frost Core/Forbidden Fragment @水晶球 → Sandstorm/Blizzard in a Bottle(→ Recipe.cs)
312	- Molotov Cocktail 改用普通凝胶(原粉凝胶);Unholy Arrow 可用 Vertebrae 替代 Worm Teeth;Thorns Potion 不再需要 Worm Teeth/Stinger(→ Recipe.cs)
313	- Angel/Demon Wings 灵魂消耗 25→15;Empty Bucket 铁锭/铅锭 3→2(→ Recipe.cs)
314	- 全部矿物砖改为 1:5 比例(1 矿+5 块=5 砖,原 1:1);Shroomite Plating 1:15→1:25;Pearlstone Brick 对齐 Ebonstone Brick(2 珍珠岩)(→ Recipe.cs)
315	- Coral Torch:每珊瑚产 3 个(原 1);Chain 配方产出 10→15(→ Recipe.cs)
316	- 蝾螈/大壳蟹/喇蛄三种旗帜任意两种可合成第三种;Wormhole Potion 配方 3 瓶水→3 瓶药水(→ Recipe.cs)
317	- 首次对话酒保给 10 Defender Medal(可买 2 杖,原 1);T2 盔甲 25→15、T3 盔甲 75→50、T2 哨兵 25→15、T3 哨兵 100→60、Defender's Forge 75→50(均 Defender Medal)(→ NPC.cs, Recipe.cs)
318	- Pad Thai/Pho 购买价提高;彩色玻璃售价下调;Sailor set、Eye Patch、Mummy set、Pharaoh's set、Baby Grinch's Mischief Whistle、Mana Crystal、Ancient Manipulator、Shell Pile 新增售价;1.4 高售价配饰与升级品售价下调(降重铸费)(→ Item.cs)
319	- 壁纸 1 银→75 铜;环境改造溶液 25 银→15 银;税官存钱上限 10→25 金(可被好感度进一步提高);青蛙售价 15→10 银(食物配方等比);渔夫任务 Hardmode 给 2 倍钱;Red Potion 研究数 10→3(→ Item.cs, NPC.cs)
320	- 新增配方:9 种安全地牢墙、全部世界生成地牢平台、Magic Mirror(→ Recipe.cs)
321	- 合成表检查代码高度优化(大量动态配方时大幅减少/消除掉帧)(→ Recipe.cs, Main.cs)
322	
323	## 【NPC与Boss与AI】
324	
325	### Boss
326	
327	- King Slime/Deerclops/Queen Slime/Golem/Empress of Light:占用更多敌怪槽(甚至非常多)以抑制战斗中杂兵生成(不影响史莱姆雨生成)(→ NPC.cs, Main.cs)
328	- Brain of Cthulhu:生命 1000→1250;全难度击退抗性 50/55/60%→55/60/65%;专家/大师幻象更快变不透明;第一阶段玩家周围新增传送安全范围;二阶段不再有地图图标(→ NPC.cs)
329	- Wall of Flesh:The Hungry 不再在 WoF 生命低于 25% 时获第三次加成(仅保留低于 50% 的第二次,直到战斗结束);The Tongue 拉扯速度匹配专家/大师 Boss 移速(→ NPC.cs, Projectile.cs)
330	- Queen Slime:二阶段最大飞行速度与加速度各降约 15%;仆从弹幕伤害 30/80/150→30/68/120,弹幕发光(→ NPC.cs, Projectile.cs)
331	- Plantera:消失计时器快速衰减前的最大玩家距离提高(→ NPC.cs)
332	- Golem:身体生命 9000→15000,头部 16000→25000,拳头 7000→10000;发拳前有约半秒充能视觉;拳头不再可被弹回(→ NPC.cs, Projectile.cs)
333	- Duke Fishron:生命 50000→60000,专家/大师缩放 1.6→1.65,最终 50000/60000/76500→60000/78000/99000;召唤与变形时无敌;激怒后移动快得多、更频繁发射更快 Cthulhunado(→ NPC.cs, Projectile.cs)
334	- 白天 Empress of Light/Skeletron/Skeletron Prime/Dungeon Guardian:一击必杀不再能被神圣护甲/忍者大师装备等闪避配饰躲过(→ Player.cs, NPC.cs)
335	- Lunatic Cultist:专家/大师生命缩放 1.25→1.5,最终 32000/40000/51000→32000/48000/61000;Ancient Light 弹幕不再可被一击杀死(承受一定伤害才死),会被制导弹幕追踪而吸收伤害(→ NPC.cs, Projectile.cs)
336	- Moon Lord:Phantasmal Sphere 伤害 -20%,碰撞箱略减;必掉两件不同武器(→ NPC.cs, Projectile.cs, ItemDropRules)
337	
338	### 敌怪、威胁与入侵
339	
340	- 反弹弹幕敌怪(Biome Mimics、Selenians):反弹弹幕仅对玩家造成一半伤害,且专家/大师不再缩放增伤(→ NPC.cs, Projectile.cs)
341	- 传送敌怪(法师 AI、Chaos Elemental、Nebula Floater):玩家周身保护半径大幅增加;系统考虑玩家速度与方向预测传送避让(仍非绝对);Chaos Elemental/Nebula Floater 保护半径更大(→ NPC.cs, Player.cs)
342	- Lifeform Analyzer 稀有度按共栖敌怪类型重排(如 Dye Beetle 降为 Rarity 1);Voodoo Demon 也展示(→ NPC.cs, Player.cs)
343	- Pumpkin Moon:波次上限提至 20 波(15-20 波分数需求对齐 Frost Moon);波次组成彻底重制;Boss 设数量上限;Mourning Wood/Pumpking 敌怪槽上调(大幅减少同时生成);多人专家/大师常见敌人引入按人数生命倍率;奖杯改用 Frost Moon 掉率(原 15 波后必掉);Boss 按波掉率略降(仍比 Frost Moon 常见)(→ NPC.cs, Main.cs)
344	- Frost Moon:多人专家/大师常见敌人同样加入生命倍率;两月事件"专家掉落奖励"修正系数略降、基础掉率同量上调(经典略多、专家持平);大师难度均获 2.5 倍得分倍率(原仅专家 2 倍、大师无加成)(→ NPC.cs, Main.cs)
345	- Poltergeist:可自由飞行(原仅地面),生命 2000→1250,波次分数 8→10,旗帜击杀需求上调(→ NPC.cs)
346	- Splinterling:生命 900→1200,旗帜击杀上调;Spooky Wood 基础掉量下调(专家/大师反而更高)(→ NPC.cs, ItemDropRules)
347	- Hellhound:生命 1200→1800,波次分数 4→5,旗帜击杀上调(→ NPC.cs)
348	- Headless Horseman:生命 10000→5000,可朝玩家发射南瓜弹幕,波次分数 25→50,多人专家/大师获与 Pumpking/Mourning Wood 相同生命缩放(→ NPC.cs, Projectile.cs)
349	- Mourning Wood:生命 12000→14000,防御 28→34,敌怪槽上调,Spooky Wood 基础掉量下调;Pumpking:生命 22000→26000,防御 36→40,敌怪槽上调(→ NPC.cs)
350	- Old One's Army:T3 第 6 波 Etherian Wyvern 改为 Etherian Lightning Bug;永恒水晶专家 2 倍/大师 3 倍生命;波间等待可右键水晶座跳过(→ NPC.cs, Main.cs)
351	- Martian Saucer:二阶段核心碰撞箱增大(→ NPC.cs)
352	- Dreadnautilus:冲撞追踪性减弱、转向半径增大;弹幕不再被图格阻挡;夜间更亮(→ NPC.cs, Projectile.cs)
353	- Blood Squid:生命 1000→750,弹幕伤害 100→70,弹幕夜间更亮;Hemogoblin Shark 弹幕夜间更亮(→ NPC.cs, Projectile.cs)
354	- Clown:Chattering Teeth Bomb 伤害 200→120,Happy Bombs 160→120 且发光;牙齿炸弹新增生成/随机被动音效;掉落池大改:成为 KO Cannon 唯一来源(1/5),Bananarang 1/30→1/10,Bloody Tear 1/100→1/10(→ NPC.cs, ItemDropRules)
355	- 蚁狮类:Antlion Larva 防御 4→2、生命 35→30、最大速度略降(尤其跳跃);Giant Antlion Charger 防御 22→16;Swarmer 18→12(→ NPC.cs)
356	- Tomb Crawler:身体防御 16→12、尾 20→14;Tomb Crawler/Dune Splicer 生成率下调(沙漠上层更低)(→ NPC.cs)
357	- Rolling Cactus:伤害 90→70(→ NPC.cs)
358	- Jellyfish:专家电击对接触型武器生效(矛、短剑、日耀喷发、催眠章鱼、天龙怒、鞭)(→ NPC.cs, Player.cs)
359	- Snow Flinx:在冰块/雪块上生成几率一致化(→ NPC.cs)
360	- Lost Girl:Hardmode 不再降生成率(1/200→1/80,全程一致),基础掉钱 5 金→2 金(→ NPC.cs)
361	- Bone Serpent:头/身/尾伤害 30/15/10→36/20/16,头/身防御 10/12→12/18(尾不变),生命 250→300,移速提升,FTW/Everything 有专属数据强化(→ NPC.cs)
362	- Rune Wizard:生成 1/300→1/200(→ NPC.cs)
363	- Rock Golem:投石频率降低、石块减速,生成率降低,掉钱 5 金→2.5 金,头掉率翻倍(→ NPC.cs)
364	- Giant Fungi Bulb:无视线不再开火,弹幕不再穿墙(击中图格即毁)(→ NPC.cs, Projectile.cs)
365	- Gastropod:开火带内置不精确度(→ NPC.cs)
366	- Cursed Hammer/Crimson Axe:修复生成代码长期不一致(原远比附魔剑稀有,现对齐,尤其 Crimson Axe)(→ NPC.cs, Main.cs)
367	- Desert Spirit:弹幕伤害 80/120/180→60/88/132(→ Projectile.cs)
368	- Jungle Creeper:防御 40→28;Moss Hornet:几率掉 Stinger(→ NPC.cs)
369	- Necromancer/Ragged Caster:传送后发射前有超过 1 秒停止期(对齐 Diabolist)(→ NPC.cs)
370	- 天柱:专家/大师不再提高击杀需求(统一 100);击败月总后全难度只需 50(→ Main.cs)
371	- Solar Crawltipede:头伤 150→120,身体伤害 100→80(→ NPC.cs)
372	- Solar Corite:生成率减半,不再屏幕外远距冲刺,冲锋前有充能动画,冲锋速度略降(→ NPC.cs)
373	- Nebula Floater:传送后 0.5 秒不可开火,反传送几率 1/4→1/6,同时上限 2→3,生成率翻倍(不超上限)(→ NPC.cs)
374	- Nebula Predictor:同时上限 2→3;Brain Suckler:生成率降 40%(→ NPC.cs)
375	- Vortex Alien Queen:行走/追击显著加速,弹幕减速;Alien Larva 纳入 Alien Hornet/Queen 家族上限(防止数量失控)(→ NPC.cs)
376	- Vortex Portals:生成与开火音效更明显;Storm Diver:空中机动改善、开火角度增大、频率大幅提高、首射延迟降低、弹速增加、其一必定精准、开火前有视觉警告(→ NPC.cs, Projectile.cs)
377	- Stargazer:光束新增半秒"充能"光束效果(伤害光束实际持续不变)(→ NPC.cs)
378	- 大 Star Cell:击退抗性 50%→70%,追击更快;Milkyway Weaver:移速 +50%,追逐数秒后周期性停止并生成星尘敌怪(→ NPC.cs)
379	
380	## 【世界生成】
381	
382	- 新种子 Remix/No Traps/Everything(详见新增内容节)(→ WorldGen.cs)
383	- 敲祭坛不再在世界中生成随机侵染方块(→ WorldGen.cs)
384	- 地下沙漠最小尺寸 50%→75%(最大不变)(→ WorldGen.cs)
385	- 地牢裂砖(Cracked Dungeon Bricks)数量略降(→ WorldGen.cs)
386	- 首次击败全部三王后立即尝试在丛林生成 Plantera's Bulb(→ WorldGen.cs, Main.cs)
387	- Crystal Shard 可在珍珠沙/硬化珍珠沙/珍珠砂岩上生长(→ WorldGen.cs)
388	- 修复:中世界部分生成物大小/数量未正确考量(丛林、发光蘑菇生物群落偏少)(→ WorldGen.cs)
389	- 修复:恶魔/血腥祭坛无法在深层地下生成(开局即存在的 bug,现在深层更多)(→ WorldGen.cs)
390	- 修复:薄冰覆盖宝箱、圆石陷阱与宝箱重叠、过高位置 Sandstone Chest 变金箱、活体桃花心木树压箱/压神庙、营地小生物群落错误生成、世界各处零散沙块伴随地下沙漠墙刷怪(→ WorldGen.cs)
391	- 修复:Windows 与 Mac/Linux 种子世界生成差异(底层 OS 差异可能无法完全消除)(→ WorldGen.cs)
392	- Not the Bees 世界补生成蜘蛛洞(→ WorldGen.cs)
393	
394	## 【渲染与视觉特效】
395	
396	- 重绘若干核心进程剑,更大更新(→ Item.cs, Main.cs)
397	- Starfury 星星视觉大幅改动(→ Projectile.cs)
398	- Zenith 挥舞音效更频繁以匹配挥速(→ Item.cs, Projectile.cs)
399	- Rod of Discord 物品贴图更亮并发光(→ Item.cs)
400	- Rainbow Brick 地图色调改善(→ TileDrawing.cs, Main.cs)
401	- 海洋水更透明易看穿(→ Main.cs)
402	- 传送器不再持续闪烁发光(→ TileDrawing.cs)
403	- 发光蘑菇草/巨型发光蘑菇涂漆后发不同颜色的光(→ TileDrawing.cs)
404	- 快速堆叠至附近宝箱新增物品飞入动画(→ Main.cs)
405	- 击败月总的世界在世界菜单图标加特殊边框(→ Main.cs)
406	- 信息配饰未激活/无信息时灰显;金色小动物在生命体分析机金色显示(→ Player.cs, Main.cs)
407	- 传送门枪风味文本与信息文本;演奏乐器时显示音符;配饰栏装备石碑仅自己可见效果(→ Main.cs)
408	- Boss 血条数值显示选项;生命/魔力数值显示选项(→ Main.cs)
409	- 一批视觉修复:血月海洋非血红、同种墙安全/不安全版本未正确合并、手持弹幕上下半格抖动、间歇泉陷阱偏移、血污高速穿世界、侵染仙人掌/绿洲植物/海燕麦地图仅显示绿色、落雪块无声无尘、多数栅栏漂浮底部贴图、地下背景层最上排不透光、水晶碎片在斜坡上浮空、石堆破坏尘埃颜色、Money Hair Dye 高额钱币彩虹循环、冰冻吊灯光色错误、Hardmode 矿石替换带漆图格时继承漆、Silly Sunflower Bottoms+Frog Leg 腿消失、水下坐椅+游泳圈腿部绘制、Kimono 坐姿与女性跳跃贴图等(→ Main.cs, TileDrawing.cs, Player.cs)
410	
411	## 【UI与界面/生活质量】
412	
413	- 新增装备配装(Loadouts):F1-F3 切换配装,相机模式改绑 F4(→ Player.cs, Main.cs)
414	- 社交栏可再次放置任意配饰;移除社交栏兼容性 tooltip(→ Player.cs)
415	- 几乎全部可堆叠物品堆叠上限提升至 9999;向导巫毒娃娃可堆叠(>1 个叠丢岩浆可能带来不必要的后果)(→ Item.cs, Main.cs)
416	- Void Bag 右键开关:关闭时类似钱槽(不再拾取溢出物品);开启时保留拾取并新增——快速使用其中增益/食物/药水(含魔力花自动用魔力药水、虫洞药水自动生效)、直接用内容物合成、收藏、快速堆叠至附近宝箱、用其中钥匙开箱、信息配饰/导线视野配饰/机械标尺生效、取空箱时收集溢出(→ Player.cs, Item.cs, Main.cs)
417	- 图鉴显示敌怪击杀数;按当前游玩情况(难度、种子等)显示属性(→ Main.cs, NPC.cs)
418	- 新增"全部武器自动挥舞"可选选项(→ Item.cs, Main.cs)
419	- 画家拆两个商店菜单(防止商品过多无法购买)(→ NPC.cs)
420	- 聊天框可发送渔夫任务鱼;全部任务鱼带捕获地 tooltip(便于分享)(→ Item.cs, Main.cs)
421	- 画刷/钓竿/环境改造器在光标旁显示所选"弹药";环境改造器可用步枪/狙击镜缩放(→ Item.cs, Player.cs)
422	- 钓鱼配饰/渔夫盔甲/钓鱼药水显示具体钓鱼力(→ Item.cs)
423	- +/* 缩放速度翻倍(→ Main.cs)
424	- 更新过时加载提示与向导文本(幸运马蹄铁、陨石等)(→ Main.cs)
425	- 旅途模式制作菜单悬停显示研究所需数量(向导/哥布林界面同样适用)(→ Main.cs)
426	- 游戏 /death、/pvpdeath、/alldeath、/allpvpdeath 命令查看个人与全服死亡统计(→ Main.cs)
427	- 部分信息配饰灰显机制;生命体分析机金色显示金色小动物(→ Player.cs, Main.cs)
428	- 主菜单新增禁用快速丢弃选项;随机角色可选发型增多、女性更常见;发型师大半发型创角可用(→ Main.cs)
429	- 旅途模式放置范围增加同时增加拾取范围;滑条带可交互按键(→ Player.cs, Main.cs)
430	- 右键 Encumbering Stone 可切换为 Uncumbering Stone 以控制阻止拾取(→ Item.cs)
431	- 装备的宠物显示在角色选择菜单(→ Main.cs)
432	- Shift 点击物品到研究栏自动研究(→ Main.cs)
433	- 角色创建默认经典模式(原旅途)(→ Main.cs)
434	- Capricorn Hooves/Tail 立即互相变形并保留收藏(→ Item.cs)
435	- 大部分 Boss 面具可与胡须配饰组合(→ Player.cs)
436	- Hardcore 幽灵移速提高(→ Player.cs)
437	- Balla Hat/Gangsta Hat 分昼夜售卖(→ NPC.cs)
438	- 小动物笼可堆叠放置且生物可站立(类似平台)(→ TileID.cs)
439	- 摇树必出叶片视觉提示;每日摇树计数按世界独立(→ WorldGen.cs, Main.cs)
440	- 大部分图格/树木生成的小动物获得短暂保护(与来自图格的蠕虫同机制)(→ NPC.cs)
441	- 史莱姆雨只在早 6 点至中午开始,但几率 ×4(总量不变)(→ Main.cs)
442	- 提取机可将钓鱼垃圾转为低级鱼饵(→ Item.cs)
443	- 高尔夫一杆进洞直接提示(→ Main.cs)
444	- Cracked Dungeon Bricks 可被弹幕打破(→ Projectile.cs, TileID.cs)
445	- 绳与矿车轨道/平台可相交;绳上滑动不与平台碰撞;一侧已有平台/轨道的绳可方块替换(→ Player.cs, TileID.cs)
446	- 火炬与营火可方块替换;Torch God's Favor 也能转换营火;全部可上锁宝箱可用 Chest Lock 重新上锁(→ Player.cs, TileID.cs)
447	- 旗帜/吊瓶/灯笼可挂于未锤击平台及锤击平台任意位置下(→ TileID.cs)
448	- 回退 Frozen Slime Block 连接样式改动(有意与史莱姆块不一致,供建筑用)(→ TileID.cs)
449	- 部分浸水即可钓鱼(手臂在浮标上方即可,含携带游泳圈)(→ Player.cs)
450	- 死亡的 NPC 无条件重生(无视首次入住条件;派对女孩正常几率重生、军火商/爆破专家不需持有对应物品)(→ NPC.cs)
451	- 击败 Golem 前神庙内导线不可见/不可放置/不可剪除(→ Player.cs, Main.cs)
452	- 全部矿车轨道物品与锁链不被岩浆摧毁(→ TileID.cs)
453	- 天空箱/天箱可找到一叠云块;神圣绿洲钓鱼可同时获得神圣或绿洲鱼(腐化/血腥不适用)(→ WorldGen.cs, Player.cs)
454	- Fairy Glowstick 更亮;Mystic Snake Coil 生长更快、最大高度 80→100 格;向日葵放置可自动挥舞(→ Item.cs)
455	- 稀有敌怪旗帜需求 50 次降为 10/25 次(图鉴同步)(→ NPC.cs)
456	- OOA 旗帜提供较弱对应 Banner buff(→ NPC.cs, Player.cs)
457	- 提交奇异植物给 6 份染料(原 3)(→ NPC.cs)
458	- 商人/骷髅商人 Hardmode 除弱效药水外还售常规药水(→ NPC.cs)
459	- Town pets 可用另一张宠物许可证更换(许可证可从动物学家处无限购买)(→ NPC.cs)
460	- Angler 常见任务奖励不再含家具,改为随任务完成数递增的几率额外掉家具(→ ItemDropRules, NPC.cs)
461	- 天气电台在沙尘暴激活时切换显示沙尘暴(→ Item.cs, Main.cs)
462	- 召唤物品 tooltip 改称"召唤"伤害(原"仆从"伤害)(→ Item.cs)
463	- 部分上下键 tooltip 文本一致性调整(→ Main.cs)
464	
465	## 【音频】
466	
467	- 为若干武器和敌怪新增音效(→ Main.cs, Projectile.cs)
468	- Chattering Teeth Bomb 新增生成时音效与随机被动音效(→ Projectile.cs)
469	- Zenith 挥舞音效更频繁(→ Item.cs)
470	- 冷却完成的"滴答"音效从 Frostbrand/Beam Sword/Chlorophyte Saber 移除(太频繁)(→ Item.cs, Main.cs)
471	- Vortex Portal 生成/开火音效更明显(→ NPC.cs, Projectile.cs)
472	- 修复:Resource Pack OGG 循环检测、多人特定枪械音频不同步、Don't Starve 死亡音效在 Constant 种子不播放、较新环境生物音量不受环境音量设置控制(1.4.4.8)、Kwad Racer Drone 音量降低(1.4.4.4)、Volcano 爆炸声远距播放(1.4.4.3)(→ Main.cs, NPC.cs)
473	
474	## 【机制系统改动(微光/转化/新机制)】
475	
476	- 独立无敌帧统一规则:有限击中次数、使用独立免疫帧的穿透弹幕,其"最后一击"不再给予免疫帧(为由全局转独立的弹幕兜底)(→ Projectile.cs, NPC.cs)
477	- 玩家 Buff/Debuff 上限 22→44(覆盖前可达双倍);敌怪 Debuff 上限 5→20(→ Player.cs, NPC.cs)
478	- 死亡后无敌时长 1 秒→3 秒(→ Player.cs, Main.cs)
479	- 局部无敌帧大规模推广:全阔剑类(含镐斧锤)、Flamethrower/Elf Melter、Magic Dagger、Shadowflame Hex Doll、Harpoon、Death Sickle(1.4.4.8)等(→ Item.cs, Projectile.cs)
480	- 独立无敌帧大规模推广:Crimson/Nimbus/Clinger、Spectre Staff、Rainbow Gun、Rainbow Crystal、Chlorophyte Saber、Frostbrand、Ice Sickle、Bladetongue、Wasp Gun、Tempest 龙卷、Frost Hydra(1.4.4.8)、Death Sickle(1.4.4.8)、Lunar Portal 等数十处(→ Projectile.cs)
481	- 涂层(Coating)系统:Echo Coating、Illuminant Coating,可与涂料及彼此叠加(→ TileID.cs, Player.cs)
482	- 魔力再生公式重做(详见魔法节)(→ Player.cs)
483	- 鞭标记系统:标记伤害概念(Cool Whip 6、Morning Star 8、Dark Harvest Reaping 等效 10)、Blade Staff 75% 系数、Lightning Aura 50% 系数、哨兵同样适用鞭标记(→ Player.cs, Projectile.cs)
484	- 鞭攻速 buff 修复为仅作用于鞭(→ Player.cs, Projectile.cs)
485	- 矿车/钻头坐骑/机械矿车升级包机制调整(详见配饰节)(→ Item.cs, Projectile.cs)
486	- Shimmer(微光)体系:1.4.4 正文仅以 Terraformer、Aether Torch、Shimmer decraft 相关热修条目间接出现;行为细节集中于热修:物品/装备 decraft 回材料、生物入微光转化(Faeling、Gummy Worm、Town Slime 变形:Sparkle Slime Balloon→Diva Slime、圣诞/万圣节史莱姆→Squire Slime)、玩家浸入获得 Shimmering 增益(1.4.4.4 起不再对 Boss 无敌)、已录音音乐盒转空白、特定转化(Lava Charm→Magma Stone、Sandstorm in a Bottle/Flying Carpet→Pharaoh's set、全部火炬→Aether Torch)、进度门控(骷髅王前不得 decraft 出 bone、Golem 前不得出蜥蜴砖)、部分物品禁 decraft(→ ShimmerTransforms.cs, Main.cs, NPC.cs, Item.cs)
487	- 氯光法杖(Terraformer)喷射微光转化生物群落(→ Item.cs, ShimmerTransforms.cs)
488	- 氯光矿石净化能力增强(可净化沙块、砂岩等更多侵染图格)(→ WorldGen.cs, TileID.cs)
489	- Philosopher's Stone 动态冷却缩放机制(详见配饰节)(→ Player.cs)
490	- NPC 重生规则:死亡 NPC 无条件重生(→ NPC.cs)
491	- 击杀三王立即尝试生成 Plantera 球茎(→ WorldGen.cs, Main.cs)
492	- 首次对话酒保赠送 10 Defender Medal(→ NPC.cs)
493	
494	## 【多人/网络】
495	
496	- Pumpkin/Frost Moon:多人专家/大师常见敌怪加入按人数生命倍率(原仅 Boss 有);修复南瓜月倍率过高与霜月倍率未生效(1.4.4.6)(→ NPC.cs, NetMessage)
497	- Headless Horseman 多人专家/大师生命缩放对齐 Pumpking/Mourning Wood(→ NPC.cs)
498	- 服务器 /death /pvpdeath /alldeath /allpvpdeath 命令(→ Main.cs)
499	- 修复多人崩溃:沙块掉落、Companion Cube、Ice Rod(→ Main.cs)
500	- 修复服务器问题:无效火炬帧、无效世界文件路径启动失败、服务器漏洞(→ Main.cs)
501	- 修复不同步:墓碑落地、苔藓地表生长、Nimbus/Crimson Rod、鞭与矛、Flying Knife 挥舞动画、服务器旗帜掉落归属、Keybrand 粒子、水桶除水、PVP 减益、Tesla Turret 弹幕、蹦跳的鱼类生物、Dry Bomb 液体、Rainbow Gun 弯曲绘制、斜坡沙块、多人调整生命的 Boss 血条中途加入显示、配装饰品同步(1.4.4.4/1.4.4.9)、多人岩浆从服务器未生成图格出现(1.4.4.1)(→ NetMessage, Projectile.cs, Main.cs)
502	- 修复:多人 Lucky Coin 在专家/大师不正常工作(→ ItemDropRules)
503	
504	## 【Bug修复-仅列影响玩法逻辑的】
505	
506	- Duke Fishron Cthulhunado 直接生成在玩家身上、Empress of Light 攻击后直接传送到玩家身上(→ NPC.cs)
507	- 鞭攻速 buff 错误作用于近战武器(→ Player.cs, Projectile.cs)
508	- 特定方式放置的平台站姿导致传送敌怪直接传到玩家身上(→ NPC.cs, Player.cs)
509	- 叠加多来源破防导致武器伤害高于基础伤害(→ Player.cs, NPC.cs)
510	- Sanguine Staff/Terraprisma 单次攻击多段命中;Blood Thorn 每次穿透掉伤;Deadly Sphere 脱仇;Imp Staff 异常高频开火;Bee/Explosive Bunny 无无敌帧高频命中(→ Projectile.cs)
511	- 无限飞行坐骑上魔力不按正常速率再生;无限飞行坐骑挂机不阻止蠕虫 AI(→ Player.cs, NPC.cs)
512	- Ichor Dart/Celebration MK2 每帧高频命中(→ Projectile.cs)
513	- Frost Moon:Flocko/Krampus 不给波次分数;第 2/3/4 波所需分数过少(→ Main.cs)
514	- Flamethrower/Elf Melter 弹药消耗问题;Rocket Launcher 无法获得远程词缀;Beam Sword 自动挥舞发射时强制玩家转向(→ Item.cs, Player.cs)
515	- Mothron 地下不检查实心图格/在岩浆中产卵;四足敌怪无法穿平台落下;The Horseman's Blade 无法处理月总眼/自然生物;特殊种子缩小 Boss 碰撞箱不准;OOA 飞行敌怪钻地逃避防御;部分雪霜军团敌怪移速错误;背靠墙时 Super Star Shooter 弹幕无法产生;Corruptor/Giant Fungi Bulb 向硬核幽灵开火(→ NPC.cs, Projectile.cs, Player.cs)
516	- 每日摇树计数跨世界累积;祭坛无法深层生成;部分被侵染图格不被树妖检测(沙/植物/藤/荆棘);OOA 后保留 Etherian Mana;沙块伴随地下沙漠墙刷怪;击败骷髅王前可钓鱼获得地牢物品;NPC 站地牢砖任何时间立即传送回家;染料植物在蜂蜜中生长;神庙内 Torch God's Favor 不用丛林火把;部分石堆在侵染/环境改造后存活;南瓜下方图格变质不自毁;水下活树隧道无法生成金色金鱼;Lucky Coin 多人专家/大师不工作(→ WorldGen.cs, Main.cs, NPC.cs, Player.cs, ItemDropRules)
517	- 高草无法在大部分栅栏前生长;蘑菇草/灰烬草墓铲无法一击破坏;Smart Cursor 种草药/南瓜选错目标;Dirt Rod 泥球摧毁装饰图格;Life Fruit/Plantera's Bulb/丛林植物错误破坏被替换植物图格;南瓜 Smart Cursor 无效位置(→ TileID.cs, WorldGen.cs, Player.cs)
518	- 其余 gameplay 修复见下文各热修小节(→ 多文件)
519	
520	---
521	
522	# 二、子版本热修(1.4.4.1 ~ 1.4.4.9)
523	
524	## 1.4.4.1(2022-09-28,desktop)
525	- 新增:击败月总的世界在选择菜单有金色边框;新增 1 个成就(→ Main.cs)
526	- 修复:服务器配置选项被完全忽略;旅途模式敌怪属性普遍增加的重大缩放错误;玩家无限使用某些物品无法停止;第 8 个 Town Slime 不解锁 The Great Slime Mitosis 成就(→ Main.cs, NPC.cs)
527	- 修复世界生成:树损坏(加防错机制)、生成特定物体时无限挂起、Trapped Chests 生成问题(缓解 Get fixed boi 生成滞缓)(→ WorldGen.cs)
528	- 修复:Chain 配方更改失效(应出 15 条而非 10 条)、Magic Quiver 击退加成向下取整(实际削弱大部分击退值)、Chains 免疫岩浆却不能延伸进岩浆(→ Recipe.cs, Item.cs, TileID.cs)
529	- 修复:多人岩浆从服务器未生成的图格出现("幽灵岩藻")、被水母放电杀死时错误死亡信息(→ NetMessage, NPC.cs)
530	- 修正:Monolith 被压入地面、反向重力液体渲染、Jungle 小动物在腐化/血腥丛林 Hive 附近生成、月相 Phantasmal Sphere 调整只应用于一个版本、悬挂家具随风摆动(→ TileID.cs, Main.cs, NPC.cs, Projectile.cs)
531	
532	## 1.4.4.2(2022-09-29,desktop)
533	- 修复 1.4.4.1 导致 Mac/Linux 无法启动、手柄/主机/移动/Steam Deck 物品复制、手柄物品无法正确分配到 D-Pad 快捷栏(→ Main.cs)
534	- 修复:Aether Campfire 缺一条 tooltip、上锁盒子不能用钥匙打开、多人 Solar Tablet 不成功仍被消耗、泵将岩浆/蜂蜜转成水、重力反转长矛视觉问题(→ Item.cs, Main.cs, TileID.cs)
535	- 修复:Clentaminator 溶液快速消耗、泥土图格合并、Smart Cursor 将圆石放到晶塔上、两个物品近战速度 tooltip 不一致(→ Item.cs, TileID.cs, Player.cs)
536	- 修复:FTW/Get fixed boi 中 Brain of Cthulhu 传送离玩家过近(仍不会躲避玩家,高速移动仍可能撞上)(→ NPC.cs)
537	
538	## 1.4.4.3(2022-10-03)
539	- 平衡:部分物品因可被利用而禁用 Shimmer decraft;Light Disc/Bananarang/Fairy Boots/Hellfire Treads 售价下调;修复剑范围效果无法正确打到身后并整体改善区域命中检测;Blade of Grass 叶刃不造成中毒(→ ShimmerTransforms.cs, Item.cs, Projectile.cs)
540	- 修复:快速堆叠对部分宝箱无效、Void Bag 收藏物品被"拿取全部"取到背包(→ Main.cs, Player.cs)
541	- 修复:Clentaminator 溶液摧毁树木并掉错木材、Royal Gel 不保护 Shimmer Slime、长矛范围在高近战速度下命中检测不稳、快速治疗用瓶装蜂蜜不给 Honey buff(→ Item.cs, NPC.cs, Projectile.cs, Player.cs)
542	- 修复:NPC 商店打开后不再动态更新价格折扣(重新允许商店开着换 Greedy Ring/Discount Card)(→ NPC.cs)
543	- 修复:Enchanted Sundial 不在自然血月/日食重充能、Shimmer 转化出的坠落之星白天立即消失(拾取中的也不再消失)、珍珠沙未被标为合成材料、Volcano 爆炸声远距播放(→ Item.cs, ShimmerTransforms.cs, Projectile.cs)
544	- 修复:死亡/冰冻/蛛网/石化时可切换配装、薄冰覆盖宝箱的世界生成问题、Barrel smart cursor 边框不匹配(→ Player.cs, WorldGen.cs, Main.cs)
545	- 修复:Abigail's Flower 在部分图格生长并破坏本不应破坏的图格;手柄"快速使用"导致物品无限使用;Tortured Soul 能捡钱(→ WorldGen.cs, NPC.cs, Main.cs)
546	
547	## 1.4.4.4(2022-10-04)
548	- Shimmering 增益不再对 Boss 提供无敌(入侵类在下一补丁处理)(→ Player.cs, NPC.cs)
549	- 图格/弹幕类便携存储拥有快速堆叠动画;漂浮容器弹幕(钱槽/Void Bag)拥有更远的快速堆叠范围(→ Main.cs, Projectile.cs)
550	- Ghost set 衬衫可见下层裤子(配 Familiar Pants 仍光腿);Kwad Racer Drone 音量降低(→ Item.cs)
551	- 修复:更多 Shimmer decraft 利用、Shimmer 世界生成位置过高(现正常形成视觉效果)、无效配装栏导致全部配装功能失效、多人配装饰品不同步、NPC 战斗动画中被 Shimmer 转化的手臂外观(→ ShimmerTransforms.cs, WorldGen.cs, Player.cs, NetMessage)
552	- 修复:Terra Blade 调试尘埃、加速游戏时间后雷电过快导致掉帧与频闪危害、复古/迷幻光照下水帘不一致、手持部分物品时热键被错误屏蔽、保存时部分玩家崩溃、名称被翻译的 NPC 不掉基于名称的特殊掉落(→ Projectile.cs, Main.cs, ItemDropRules)
553	
554	## 1.4.4.5(2022-10-07)
555	- 三本 Guide(动物伙伴/环境保护/和平共处)可在物品栏/快捷栏按 open 键切换开关(→ Item.cs, Player.cs)
556	- 全部火炬在微光转化为 Aether Torch;不再能通过 Shimmer decraft 在骷髅王前获得 bone、在 Golem 前获得蜥蜴砖(→ ShimmerTransforms.cs, TileID.cs)
557	- 防玩家过久停留 Shimmering 状态的保险机制;修复 Shimmer+弹性方块软锁(→ Player.cs)
558	- 修复:WoF 掉落在世界转 Hardmode 时消失(Remix/Everything 外罕见)、Shellphone 无法 decraft、黄金马桶不产便便、更多 decraft 利用物品(→ ItemDropRules, ShimmerTransforms.cs, Item.cs)
559	- 修复:图格致动保护向下延伸过远、海洋游玩中被反复吸干、Remix/Everything 丛林神庙罕见不生成、安全沙漠墙处刷敌、FTW/Everything 爆炸物多次命中、Abigail's Flower 无法在蘑菇草/灰烬草生长、镰刀无法从灰烬草/海燕麦收干草、Constant 黑暗讯息预警不足(→ WorldGen.cs, NPC.cs, Projectile.cs, Player.cs)
560	
561	## 1.4.4.6(2022-10-21)
562	- Angler 配饰重复保护重构:扩展到全部 7 种配饰(含钓鱼浮标,含升级形态如 Shellphone),集齐 7 种才开始掉重复;总体提升配饰掉量;Mermaid set/Fish set 优先级高于配饰(→ ItemDropRules)
563	- 从堆叠分出物品几秒后加速更快(应对 9999 堆叠)(→ Main.cs)
564	- 不安全地牢砖墙/地下沙漠墙反直觉生成条件修正(原要求敌怪图格后方有墙,现为上方)(→ NPC.cs, Main.cs)
565	- "Goblin Summoner"名称降级为"Goblin Warlock"(仅名称变更)(→ NPCID.cs)
566	- Master+FTW/Everything 菜单显示"Legendary"难度;臭虫(Stinkbug)日更常见(→ Main.cs, NPC.cs)
567	- 新增 Solidifier 处合成沙岩块/硬化沙块;圣诞/万圣节史莱姆可变形为 Squire Slime(无蓝史莱姆季节时);Sandstorm in a Bottle/Flying Carpet 可 transmute 为 Pharaoh's set;Lava Charm 可 transmute 为 Magma Stone(→ Recipe.cs, ShimmerTransforms.cs)
568	- 银子弹/钨子弹 Shimmer 分解产出 1 矿石(原 1 锭);铜短剑/铜斧/铜镐可分解为 1 铜矿+1 木头(原不可分解);玻璃窑售价下调(→ ShimmerTransforms.cs, Item.cs)
569	- Oiled 减益可见性提高;FTW 中 Crispy Honey Block、Constant 中仙人掌被危险感知高亮;FTW 随机天使雕像替换不再影响地牢箱(含 Hardmode 生物群落箱)(→ BuffID.cs, Player.cs, WorldGen.cs)
570	- 修复:Remix 中 Ice Golem/Angry Nimbus/Rainbow Slime 雨/暴风雪生成不可靠;Digging Molecart 可 pre-Hardmode 挖祭坛及有物品的宝箱;南瓜月多人倍率过高/错误伤害倍率、霜月倍率未按预期调整(→ NPC.cs, Item.cs)
571	- (再次)修复 Brain of Cthulhu 传送到玩家面前;可重复来源生成的 NPC/生物(雕像等)被标记并在达上限时被普通生成替换(含蜂王的蜜蜂);落微光的生物生成更多 Faeling(→ NPC.cs, ShimmerTransforms.cs)
572	- 修复:Guide to Peaceful Coexistence 被误标 material、Hand of Creation 稀有度低于 Architect Gizmo Pack、世界名称撇号不一致、Inner Tube 不能在蜂蜜漂浮、Chromatic Cloak 对微光生效、宝石树无下方图格不显示树叶、Celebrationmk10 沙块方块替换不变青色、地下沙漠宝箱生成错误类型(通常金箱)且战利品错误、右键可在装备栏装"空气"、万圣节/圣诞节兔子不变 Faeling、环境保护指南阻止陷阱摧毁图格、Deerclops 敌怪槽不生效、The Horseman's Blade 弹幕选生物为目标、FTW/Everything 中 Boss 弹幕 NPC 击杀判定单多人不一致、Remix/Everything 化肥对特定地下层树无效、飞镖陷阱碰撞大小不一、世界边缘外生物群落/草蔓延缓冲区(防蔓延到不可净化位置)(→ 多文件)
573	
574	## 1.4.4.7(2022-10-24,desktop)
575	- 修复:白天不断自行设为夜晚;每次启动后首次生成蜂王/Golem 失败(多人更频繁);图鉴排序不先更新调整后属性(→ Main.cs, NPC.cs)
576	- 修复:上/下切换 Rubblemaker 图格会改变其他玩家的图格选择(多人);Dead Man's Chest 陷阱生成在其它存储物品上并损坏(→ NetMessage, WorldGen.cs)
577	- 修复:Remix/Everything 中未经玩家交互被岩浆杀死的史莱姆也能召唤 King Slime(先击中后岩浆击杀仍有效);Slimer 无意中双倍几率掉 Monster Meat;回退 1.4.4.6 IPv6 修改(→ Main.cs, ItemDropRules)
578	
579	## 1.4.4.8(2022-11-09)
580	- Mac 性能优化(角色创建菜单、人体模型旁等)(→ Main.cs)
581	- 平衡:可击中身后敌人的光环剑(Excalibur、The Horseman's Blade 等)现在将敌人击离而非击向玩家(→ Projectile.cs, Player.cs)
582	- Trimarang:击退 3→4.5、使用 22→20、弹速与返回速度微增(比合成素材全部更快);Starfury:基础伤害 22→25、弹幕 2 倍→1.5 倍基础(44→37);Bee Keeper/Hive-Five 蜜蜂基于近战暴击造成暴击(→ Item.cs, Projectile.cs)
583	- Night's Edge:伤害 42→40、使用 21→25、穿透 3→2(单次挥舞最大命中 6→4)、挥舞范围扩大略降;Ice Sickle:弹幕伤害 50%→67% 基础、穿透 3→4;Death Sickle 镰刀弹幕改独立无敌帧;Terra Blade 从近战速度获得的收益降低 25%;North Pole 相近雪花互相略推开(→ Item.cs, Projectile.cs)
584	- Undertaker 伤害 22→19(部分回退 1.4.4 增强);Phoenix Blaster 伤害 33→30、使用 17→14;Aqua Scepter 穿透无限→5(类似 Golden Shower)(→ Item.cs)
585	- Snapthorn:中毒持续 4→3 秒、几率 100%→20%;勘误:1.4.4 日志称其伤害 18→19 有误,实际仍为 18(→ Item.cs)
586	- Optic Staff:基础伤害 21→24(Spazmamini 为 100% 基础)、Retinamini 倍率 1.25→1.15;Houndius Shootius 弹幕碰撞框增大;Frost Hydra 弹幕改独立无敌帧;Magic Quiver 掉率 1/80→1/40(→ Item.cs, Projectile.cs, ItemDropRules)
587	- War Table/War Table Banner:掉率分离并提高——T1 Dark Mage Classic 各独立 50%/Expert+ 100%,T3 各 1/8 / 1/4(→ ItemDropRules)
588	- 坐下/入睡:大幅降低生命再生加成;受伤打断入睡与坐下状态(→ Player.cs)
589	- Mystic Frog:生成率提高、不再在捕捉时消失(传送到屏幕内附近)、图鉴条目更新;Don't dig up 的 pre-Hardmode Mimic:生命 270→300、防御 16→12;Don't dig up 的 King Slime 生成加进度检测(对齐普通世界史莱姆雨条件)(→ NPC.cs)
590	- 其它更改:Gold Worm 生物形式入微光也变 Gummy Worm;Sparkle Slime Balloon 物品形式入微光也生成 Diva Slime;Pressure Plate Track 被危险感知高亮;Lava Charm/Molten Charm 有虚荣配饰外观;War Table Banner/悬挂草药/悬挂火盆可挂于锤击平台下;神圣甲与远古神圣甲不再互相转化(改 decraft 为神圣锭)(→ ShimmerTransforms.cs, Player.cs, Item.cs)
591	- 修复(玩法类节选):地牢小房间隔断上方入口、蜥蜴门生成在不可达位置、圆石陷阱生成在宝箱上、Royal Gel 对 Golden Slime 无效、人体模型/帽架移除配饰放置距离、蜗牛生物无视微光、按上键反转重力不解除坐骑、鞭上药瓶微粒缺失、Deadly Sphere 窄封闭区 DPS 恶意利用、Grand Design/传送门枪阻断抓钩热键(仅鼠标)、食人鱼枪一发未命中即全部回收、Don't dig up 地狱 1 格厚层生成错误敌人、城镇 NPC 频繁往返传送、Cascade 意外由部分敌人掉落、解除/覆盖 Abigail 删除玩家"拥有"的其它仆从弹幕与 buff、反转重力下短剑/Starlight 手臂方向、多人钻头坐骑采矿光束不可见、Sky Dragon's Fury/Ghastly Glaive 与微光相关问题及弹幕异常、叶绿套开火冷却切甲被重置、Fireblossom Seeds+Smart Cursor 无法在灰烬草工作、Holy Protection 移除圣甲后残留、深池钓鱼钓不上任何东西、多人 Truffle 无法分配地下蘑菇住所、Don't dig up 海洋晶塔不生效、Meowmere 矿车轨迹与特定护甲异常、草籽 Smart Cursor 异常、光之女皇无敌阶段仍能伤害玩家、宝石果在高苔藓旁无法生长/放置、音乐盒与词缀不一致、石碑可堆叠导致可获词缀、泥土炸弹不替换高草等图格、Like A Boss 成就不适用于较新 Boss 召唤物、Real Estate Agent 成就不需要酒保、虫洞药水使用后的微光状态问题(→ 多文件)
592	
593	## 1.4.4.9(2022-11-17,desktop)
594	- 已录音音乐盒入微光 transmute 为空白音乐盒(→ ShimmerTransforms.cs)
595	- 更新超过 100 个外观图(老旧资源现代化);90 种剑与工具的尺寸乘数重置为 1(贴图放大体现实际尺寸;hitbox 影响极小,通常使武器范围增加 1-2 像素);附完整 Item ID 尺寸对照表(例:Iron Broadsword 32×32→36×36、Breaker Blade 70×80→80×92、Keybrand 45×50→58×62、Beam Sword 40×40→52×52、Death Sickle 60×56→70×64、全部 Phasesaber 48×48→56×56 等);企鹅宠物弹幕(Projectile ID 112)22×102→32×216;注意:资源包中对应替换贴图失效(→ Item.cs, Main.cs)
596	- 平衡:Scarecrow 旗帜/图鉴需求 200→150(对应南瓜月中较少数量),全部 Scarecrow 共享击杀计数并同时解锁;Morning Star 伤害 180→165;Xeno Staff 开火间隔 36→40(对应其 AI 改动后超预期表现);Bee Wax 及其制品售价一致性调整;Imp Staff 售价提高(匹配其它狱岩锭装备)(→ Item.cs, NPC.cs, ItemDropRules)
597	- 修复(玩法类节选):多人配装外观同步、Echo Coating 墙体在地下显示纯黑、多人喷漆器对可掉落图格无效、Don't dig up 城镇 NPC 在有效海洋区域不出售海洋晶塔、Truffle 在 Don't dig up 仍售深蓝溶液、回归药水传送门按当前高度(骑坐骑传送)定位、Toxic Flask 弹幕把平台当实心方块、1.4.4.3 起生成的世界缺少发光郁金香(不回填)、开启 Void Bag 中信息配饰在多人不提供附近玩家显示、Shadow Scale/Tissue Sample 无法在叶绿提取机互转、Shift 放配饰到人体模型可致无效状态、多人右键切换类物品(Void Bag/Shellphone)音效反复播放(→ 多文件)
598	
599	---
600	
601	# 三、【本版本改动规模评估】
602	
603	## 系统覆盖面
604	约涉及 **18~20 个独立系统**:物品数值(Item.SetDefaults)、弹幕与无敌帧体系、Boss/敌怪 AI 与数值、鞭与召唤标记系统、盔甲套装奖励、配饰叠加与升级链、坐骑与矿车、钓鱼与渔夫奖励、宝箱/世界生成战利品池、掉落规则(ItemDropRules)、配方(Recipe)与合成性能优化、增益/减益(含 Hellfire/Frostbite 全系替换)、魔力再生公式、微光/转化(Shimmer/Aether,新文件 ShimmerTransforms.cs)、特殊种子(4 新种子+4 旧种子更新)、涂层/涂装系统、装备配装 Loadouts、Void Bag 重做、UI/生活质量(约 50 条)、多人同步。
605	
606	## 新增 ID 段估算(相对 1.4.3)
607	- ItemID:新增约 300+(官方口径"超过 300 种新物品");1.4.4.9 尺寸表中 Axe of Regrowth 已到 ID 5295,可作上限锚点(→ ItemID.cs)
608	- TileID/WallID:新增约 25+ 方块与墙(含 Ash Wood 全套、涂层图格状态、3 套家具)(→ TileID.cs, WallID.cs)
609	- NPCID:新增 8 个城镇史莱姆 + 若干新生物(Jungle Birds、Faeling、Gummy Worm 等)(→ NPCID.cs)
610	- BuffID:新增/强化 Hellfire、Frostbite、Blood Butchered、Shimmering、Oiled、鞭速系列(Jungle's Fury/Durendal's Blessing/Harvest Time)等(→ BuffID.cs)
611	- 新文件:ShimmerTransforms.cs(微光转化表)、Aether 生物群落生成(GameContent/Biomes)(→ ShimmerTransforms.cs, GameContent/Biomes)
612	
613	## 复刻项目必须跟进的核心改动(按优先级)
614	
615	1. **P0 微光/Aether 体系**:新液体微光 + Aether 生物群落生成 + ShimmerTransforms 转化表(物品 decraft、生物转化、Town Slime 变形、玩家 Shimmering 状态)。官方 1.4.4 正文对此几乎零记录,必须直接参照反编译 ShimmerTransforms.cs 与 WorldGen 的 Aether 生成;1.4.4.3~1.4.4.9 热修提供了大量行为细节(禁 decraft 名单、火炬转 Aether Torch、进度门控、Boss 无敌豁免)。(→ ShimmerTransforms.cs, WorldGen.cs, Main.cs, 液体系统)
616	2. **P0 无敌帧体系重构**:全局/局部/独立三套规则的全面重分配——全阔剑改局部、数十件武器改独立/局部。这是战斗手感的底层改动,必须先在弹幕命中判定层统一实现,否则后续所有武器手感都错。(→ Projectile.cs, NPC.cs, Player.cs)
617	3. **P0 数值大改(数百条)**:近战全系加强(早期金属阔剑、6 种 Hardmode 金属剑/长柄)、Terra Blade/Volcano/True Night's Edge/True Excalibur/Excalibur/Horseman's Blade/Night's Edge 重做为能量环系、手炮系、魔法(魔力再生公式、三朵云 5 分钟)、召唤(鞭标记伤害系统+哨兵 10 分钟+哨兵适用鞭标记)。SetDefaults 需逐条对表。(→ Item.cs, Recipe.cs, Projectile.cs, Player.cs)
618	4. **P1 Boss/敌怪数值与 AI**:Golem 三段生命大改(15000/25000/10000)、Duke Fishron 60000/缩放 1.65、BoC 1250、邪教徒 1.5 倍缩放、南瓜月 20 波重构+全部南瓜月敌人重排、传送敌怪预测避让系统、Boss 占用敌怪槽机制。(→ NPC.cs, Main.cs)
619	5. **P1 Buff/Debuff 上限与替换**:玩家 buff 上限 22→44、敌怪 debuff 5→20、死亡无敌 1→3 秒、Hardmode 火系 On Fire!→Hellfire、Frostburn→Frostbite、Poisoned 对敌 2→6 DPS。(→ Player.cs, NPC.cs, BuffID.cs)
620	6. **P1 装备配装 Loadouts + Void Bag 重做**:F1-F3 三套配装(饰品/时装/染料独立)、Void Bag 双态与全套新功能,Player 数据结构需新增字段。(→ Player.cs, Main.cs, Item.cs)
621	7. **P2 掉落与战利品池重构**:旅行商人双新栏位、EoW/BoC 掉落重构(击杀/宝袋比例)、大批掉率调整、宝箱主要物品池 12→10、天箱战利品调整、钓鱼箱矿石下调。(→ ItemDropRules, WorldGen.cs, NPC.cs)
622	8. **P2 世界生成**:4 个新特殊种子(Remix/No Traps/Everything 为重头)、FTW 难度自动升级、祭坛不再散播腐化、地下沙漠最小尺寸 75%、深层祭坛生成修复。(→ WorldGen.cs, Main.cs)
623	9. **P2 涂层系统 + 方块交互**:Echo/Illuminant Coating 与涂料可叠加、绳/轨道/平台相交、火炬与营火方块替换、旗帜悬挂规则、堆叠上限 9999。(→ TileID.cs, Player.cs, Item.cs)
624	10. **P3 渲染/UI/音频**:100+ 贴图更新与 90 种武器尺寸乘数归一(1.4.4.9)、Boss 血条数值、快速堆叠动画、/death 命令、图鉴击杀数。可延后,但尺寸归一影响 hitbox,应与 P0 数值对表时一并处理。(→ TileDrawing.cs, Main.cs)
625	
626	## 风险提示
627	- 1.4.4 正式日志遗漏微光/Aether 的正向描述(仅在热修中以修复口吻出现),复刻不能只靠 changelog,必须直接读取 ShimmerTransforms.cs 与相关生成代码。
628	- 1.4.4.8/1.4.4.9 对 1.4.4 数值有**二次修正**(Undertaker 回退、Night's Edge 再削、Snapthorn 勘误、Xeno Staff 再削、Starfury 再调),最终数值以 1.4.4.9 之后为准,只抄 1.4.4 会抄错。
629	- 免疫帧规则改动横跨 Item/Projectile/NPC/Player 四个文件,是本版本最容易引入手感偏差的部分。
630	

```


---

## 👤 User(sidechain) · 2026-08-09T11:40:30.129Z

**📎 ToolResult**

```
<persisted-output>
Output too large (38.5KB). Full output saved to: ~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/e65c4575-731a-43e0-a377-ccf50cc42db3/tool-results/bwhh9lvf0.txt

Preview (first 2KB):
Version 1.4.4 Changes -------------------------------------------------------------------------------------------

I. Labor of Love Content Changes and Additions:
A. New Special Seeds and Updates to Special Seeds
- Added the "Remix" World Seed, where the player spawns in the Underworld and makes their way up. Worldgen is heavily overhauled, and enemy spawns and item drops are changed
- Added the "No Traps" World Seed, for those players who just totally hate dying to traps during their Terraria adventures.
- Added the "Everything" World Seed, a combination of all of the major seed features from every other special seed.

For the Worthy Updates
- Numerous changes and threats have made their way to the FTW seed, to demand even more worthiness from players
- Classic difficulty FTW worlds automatically behave as Expert. Expert FTW worlds are automatically Master.
- Should now be possible to 100% complete the Bestiary

Not the Bees Updates
- Spider Caves now generate in Not The Bees worldgen
- All fish should be catchable now
- Should now be possible to 100% complete the Bestiary

Don't Starve Seed Updates
- Don't Starve Darkness damage increased from 50 to 250, and the time before being hurt decreased from 8 to 4 seconds
- Eating regular mushrooms will reset hunger back to full duration Peckish if you are Peckish, Hungry, or Starving

Celebration Seed Updates
- A number of changes have been made to Celebration worlds to make them even more fancy and festive!

B. New Items and Content
- Added 8 Slime Town Pets! Collect em all!
- Added over 300 new items
- Added over 25 new blocks and walls
- Added over 55 new paintings
- Added a few new vanity accessories and items
- Added a new tree type
- Added 3 new furniture sets
- Added Crimson and Corrupt Mud Grass. Corruption and Crimson no longer dry out Jungle Grass into dirt when corrupting it, but instead simply spread to the grass portion.
- Added Rubblemaker
- Added Shellphone
...
</persisted-output>

```


---

## 🤖 Assistant · 2026-08-09T11:40:34.197Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I need to read the full official changelog section 2374-4368 systematically. The first bash output was saved to a file. Let me read the persisted output and continue reading the rest of the changelog sections. I'll read the changelog in chunks directly.

Let me plan: the official section spans lines 2374-4368 (~2000 lines). I need to scan it all systematically. Let me read it in chunks via sed, but outputs get truncated at 38KB. ~2000 lines will be maybe 200KB. So I need to read in pieces of ~500 lines each, and outputs may still be too large (38KB for 526 lines). Let me use smaller chunks, ~400 lines each, which is ~30KB. That's 5 chunks. I'll read the persisted file too.

Actually let me just read the persisted output file with the Read tool, and then get subsequent chunks.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:40:34.502Z · glm-x-preview-260804

```
我需要系统性读取官方日志全段(2374-4368)。先读取已保存的第一段输出,再分块读取剩余部分。
```


---

## 🤖 Assistant · 2026-08-09T11:40:34.505Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/e65c4575-731a-43e0-a377-ccf50cc42db3/tool-results/bwhh9lvf0.txt"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:40:34.640Z

**📎 ToolResult**

```
1	Version 1.4.4 Changes -------------------------------------------------------------------------------------------
2	
3	I. Labor of Love Content Changes and Additions:
4	A. New Special Seeds and Updates to Special Seeds
5	- Added the "Remix" World Seed, where the player spawns in the Underworld and makes their way up. Worldgen is heavily overhauled, and enemy spawns and item drops are changed
6	- Added the "No Traps" World Seed, for those players who just totally hate dying to traps during their Terraria adventures.
7	- Added the "Everything" World Seed, a combination of all of the major seed features from every other special seed.
8	
9	For the Worthy Updates
10	- Numerous changes and threats have made their way to the FTW seed, to demand even more worthiness from players
11	- Classic difficulty FTW worlds automatically behave as Expert. Expert FTW worlds are automatically Master.
12	- Should now be possible to 100% complete the Bestiary
13	
14	Not the Bees Updates
15	- Spider Caves now generate in Not The Bees worldgen
16	- All fish should be catchable now
17	- Should now be possible to 100% complete the Bestiary
18	
19	Don't Starve Seed Updates
20	- Don't Starve Darkness damage increased from 50 to 250, and the time before being hurt decreased from 8 to 4 seconds
21	- Eating regular mushrooms will reset hunger back to full duration Peckish if you are Peckish, Hungry, or Starving
22	
23	Celebration Seed Updates
24	- A number of changes have been made to Celebration worlds to make them even more fancy and festive!
25	
26	B. New Items and Content
27	- Added 8 Slime Town Pets! Collect em all!
28	- Added over 300 new items
29	- Added over 25 new blocks and walls
30	- Added over 55 new paintings
31	- Added a few new vanity accessories and items
32	- Added a new tree type
33	- Added 3 new furniture sets
34	- Added Crimson and Corrupt Mud Grass. Corruption and Crimson no longer dry out Jungle Grass into dirt when corrupting it, but instead simply spread to the grass portion.
35	- Added Rubblemaker
36	- Added Shellphone
37	- Added Hand of Creation
38	- Added Echo Coating and changed Illuminant Paint to be Illuminant Coating. Coatings function exactly like paint, except they can be stacked with any other paint and each other.
39	- Added Lilith's Necklace
40	- Added Poo
41	- Added Terraformer
42	- Added a Biome Sight Potion
43	- Added Jungle Birds
44	- Added Flymeal, bane of Townsfolk everywhere
45	- Added a few more pre-Hardmode weapons
46	- Added Bottomless Honey Bucket and Honey Absorbent Sponge
47	- Added Fart Kart
48	- Added Resplendent Dessert
49	- Re-implemented Pixel Boxes to be sold by the Mechanic, which have been updated to have improved functionality for pixel displays.
50	- Re-implemented the deprecated Mini Star Cell Banner. It drops and buffs its respective enemy. Regular Star Cell banner no longer gives a buff against Mini Cells.
51	
52	C. UI and Menu QoL Changes
53	- Added Equipment Loadouts. Changed F1-F3 keys to be the default bindings for Loadout Swapping, and F4 was changed to be the keybind for Camera mode.
54	- You can now place any accessory in social slots again. Social slot eligibility tooltip removed.
55	- Increased the max stack size of nearly all stackable items to 9999.
56	- You can now stack Guide Voodoo Dolls! But . . . with great stacking comes great responsibility. Throwing a stack of more than one into lava may have unwanted consequences.
57	- Void Bag now can be opened/closed with right click. A closed Void Bag will no longer pick up overflow items, and functions more like a Money Trough. An open Void Bag still picks up overflow items, and gains a number of new features, including:
58	- Using Quick Buff, Food, and Potions from its Storage. This includes Mana Flower Mana Potions. Wormhole Potions will also work automatically from within it.
59	- Allow crafting directly from Void Bag Contents
60	- Favoriting items inside of it
61	- Quick Stack to Nearby Chests from its contents
62	- Keys within it can be used to unlock chests
63	- Info accessories, Wire vision accessories, and Mechanical ruler all work from within it
64	- Void Bag will now also collect overflow items when looting chests
65	- Bestiary now shows kill count for that enemy
66	- Bestiary now shows stats based on the current gameplay session (based on things like difficulty, seed, etc)
67	- Added an accessibility option which will allow all weapons to be autofired
68	- Painter now has two shops menus. Wares are split between them to prevent his wares from being locked out of purchase due to too many items being in one shop.
69	- You can now link Angler quest fish in the player chat box
70	- All Quest Fish items now have tooltips saying where to catch them (useful for sharing in chat message)
71	- Paintbrushes, Fishing Rods, and Clentaminator now show the currently selected "ammo" by the cursor
72	- Clentaminator now works with Rifle/Sniper Scope functionality
73	- Angler Set, Fishing Accessories, and the Fishing Potion now all indicate how much Fishing Power increase they grant
74	- The +/- options to change Zoom now zoom twice as fast
75	- Updated some outdated loading and Guide text about things such as Lucky Horseshoe and Meteorites
76	- When in Journey mode, mousing over items in the crafting menu will show how many are needed to Research. This also applies to Guide and Tinkerer UI slots.
77	- Some info accessory tabs are grayed out when inactive or display N/A, and will light back up when active again. Gold Critters will appear in gold on the Lifeform Analyzer.
78	- Changed the Quest info for Pengfish and Pixiefish to be more consistent with similar fish
79	- Quick Stack to Nearby Chests now has a visual effect, showing the items which are being quick stacked moving towards the chests they go into
80	- Added flavor text and info text for Portal Gun
81	- Equipping any of the Monoliths in accessory slots will create a player-side shader effect in the same way that Radio Thing does
82	- Playing musical instruments now shows the note on the cursor
83	- Significantly increasing the range of quick stack to nearby chests
84	- Pumpkin and Frost Moon will now display the total score when the event is over.
85	- Flower Accessory's social display visual now draws over helmets/face accessories, to allow combining. Additionally, Jungle Rose has been changed from a Head Vanity to a Vanity Accessory.
86	- Worlds in the World Menu where Moon Lord have been defeated now have a special border around their icon
87	- Added an option to show health/mana display numbers on Health/Mana UI settings
88	- Added an option to display numbers on boss health bars
89	- When a Sandstorm is active, the Weather Radio info accessory will display it, alternating between it and the standard weather display
90	- Character creation now defaults to Classic mode instead of Journey mode
91	- Summoning tooltips now say they deal "Summon" damage instead of "Minion" damage
92	- The game now tracks deaths, and they can be viewed with the /death and /pvpdeath commands. Additionally includes the /alldeath and /allpvpdeath for server-wide numbers.
93	- Made some consistency improvements to tooltip text displaying Up/Down messages
94	- Capricorn Legs/Tail now instant-transform into each other, and maintain favorite status, rather than simply spawning a new item in a different inventory location
95	- Shift-clicking items to the research slot automatically researches the item.
96	- When randomizing a character, more hairstyles are available to be rolled
97	- When randomizing a character, the game will pick female characters more often than before (which previously was actually quite uncommon)
98	- Most of the Stylist haircuts are now available when creating your character
99	- Added an option to disable quick trash in the main menu
100	- When using Journey mode's reach booster, it also increases item pickup range
101	- Encumbering Stone can be right clicked from the inventory or hotbar to make it Uncumbering, allowing more controllable use of its pickup blocking function
102	- Your equipped pet can now be seen on the player selection menu with your character
103	- Journey sliders now have interactible buttons which allow you to snap to specific points
104	
105	D. Content Changes and Feature Expansions
106	- Added new achievements
107	- Added new Death Messages
108	- Added several new title texts
109	- Added many new words to the random world name list
110	- Added new sounds to several weapons and enemies
111	- Ropes and Minecart tracks can now intersect, allowing you to use a rope and a minecart in the same spot without having to break one
112	- Similarly, Ropes and Platforms can also now intersect.
113	- The player no longer collides with platforms when on a rope pulley, to allow for ropes which go through platforms
114	- You can now exchange your Town pet by using another Pet License (They can now be purchased infinitely from the Zoologist)
115	- Smashing altars no longer generates random blocks of infection in the world
116	- Traveling Merchant now has an extra guaranteed item slot in his inventory in Hardmode. This slot can only contain items from the 4 less common item pools, with the most common items being excluded.
117	- Traveling Merchant now has an extra guaranteed item slot in his inventory at all times. This slot will ALWAYS contain a painting. Paintings have been removed from all of his other inventory slots, which will slightly increase the odds of obtaining the rest of his wares.
118	- Angler no longer drops furniture items as part of his regular drop pool. Instead, he now has a chance to give a bonus Furniture drop when completing quests. The odds of getting a bonus furniture drop increase as your Quests completed increases.
119	- Right clicking the Eternia Crystal Stand during the cooldown between OOA waves will allow you to skip the delay and immediately start the next wave. The Eternia Crystal stand and the first wave completed message also indicate this fact.
120	- Upon defeating all 3 mechs for the first time, the game will now attempt to immediately spawn a Plantera Bulb in the Jungle
121	- Glowing Mushroom grass and trees now glow different colors when painted
122	- Critter Cages can now be stacked and stood on like platforms
123	- Increased the minimum size of Underground Deserts from 50% of the maximum size to 75% of the maximum. The maximum size has not increased.
124	- The player can now have double the number of active buffs/debuffs (44 total) before they start overriding each other
125	- Torch God's Blessing can now convert Campfires as well
126	- You can now block swap torches and campfires
127	- Players can now blockswap ropes out for platforms or minecart tracks if there is already a platform/minecart track to the side of the rope
128	- All Lockable Chests can now be re-locked using Chest Locks
129	- The Extractinator can now be used to turn fishing trash into low level bait
130	- When getting a hole in one in golf, it now says so instead of saying 1 stroke
131	- Slime Rain can now only begin from 6 AM to Noon, but the odds of it happening are now 4x as high. This will result in the same number of Slime Rains overall, but they simply start in the morning.
132	- Most critters which spawn from tiles or trees now have a brief delay before they can be killed (the same as how Worms from tiles are protected)
133	- When hitting trees, the tree will now always show a visual puff of leaves, even if nothing is dropped, to indicate that a successful tree hit has been performed
134	- Banners, Hanging Bottles, and Lanterns can now be placed on unhammered platforms and all other platform hammer configurations
135	- Reverting a previous change that altered how Frozen Slime Blocks merged with regular Slime Blocks and other blocks. They are now intentionally inconsistent with regular Slime Blocks for building purposes.
136	- Crystal Shards can now grow on Pearlsand, Hardened Pearlsand, and Pearlsandstone
137	- Rainbow Bricks now use an improved map color gradient
138	- Abigail's Flower now breaks in one hit when mined and makes a grassy sound when doing so
139	- Zenith's swing SFX now plays more often to more appropriately match its swing speed
140	- Rod of Discord's item sprite is now bright and generates some light, making it easier to see if it drops
141	- Resprited several of the core progression swords to be bigger and more up to date
142	- Starfury's star has been given a visual overhaul
143	- You can now fish while partially submerged in water, as long as the player's arms are above the bobber. This includes fishing in an Inner Tube!
144	- Cracked Dungeon Bricks can now be broken by projectiles
145	- Added recipes for all 9 safe versions of Dungeon Walls
146	- Added recipes for all of the Dungeon worldgen platforms
147	- Added a recipe for Magic Mirror
148	- Heavily optimized recipe checking code. This should result in dramatically reduced/eliminated FPS drops when large numbers of recipes are calculated on the fly (such as when opening a chest that contains large numbers of crafting materials when near crafting stations)
149	- Balla Hat and Gangsta Hat are now sold during day and night respectively, instead of 24/7
150	- Ocean water is now slightly more transparent and easier to see in
151	- The Nurse can now comment on how often you have been dying in her random dialogue
152	- Some Boss Masks can now be combined with Beard Accessories
153	- Increased movement speed of Hardcore Ghosts
154	- Teleporters no longer produce flickering light passively
155	
156	
157	II. Labor of Love Bug Fixes:
158	A. Crashes and Major Issues
159	- Fixing an issue which prevented Terraria from working on some Mac OSX 12 installations
160	- Fixed a crash that could happen if various critters went outside of the world's boundary
161	- Fixed a crash relating to Sand falling in multiplayer
162	- Fixed a rare crash with Companion Cube in multiplayer
163	- Fixed a crash caused by Lightning Aura Sentries dropping through the bottom of the world
164	- Fixed a crash issue related to Ice Rod in multiplayer
165	- Fixed a crash relating to loading and unloading resource packs
166	- Fixed an issue where invalid Torch frames would cause problems on servers
167	- Fixed an issue when attempting to verify integrity of game files, a single file would always fail to validate
168	
169	B. Combat, Enemy, and Weapon Issues
170	- Fixed a quirk of Duke Fishron's Cthulhunado that would sometimes instantly spawn it on the player and hurt them unavoidably. It should now spawn a certain distance below the player if there is no floor nearby, allowing the player time to avoid it
171	- Fixed an issue where Whips that gave Attack Speed buffs would incorrectly apply the buff to Melee weapons. Their tooltips have been updated to emphasize this fix.
172	- Fixed a bug where standing on certain configurations of platforms would allow teleporting enemies to teleport directly on top of you and cause damage
173	- Fixed a bug where, if stacking multiple sources of defense penetration, it would allow weapons to deal extra phantom damage above base damage
174	- Fixed a bug where Sanguine Staff and Terraprisma could hit a single enemy more than once per swing
175	- Fixed a bug with Blood Thorn causing its thorns to unintentionally lose damage on every pierce
176	- Fixed a bug where Deadly Spheres minions would spontaneously de-aggro from enemies in the middle of combat
177	- Fixed a issue where Empress of Light would sometimes teleport directly on top of the player
178	- Fixed a bug that caused mana to not regenerate at normal speeds when on infinite flight mounts
179	- Fixed an issue where Ichor Dart and Celebration MK2 would sometimes rapidly hit more than intended
180	- Fixed Flocko and Krampus not giving wave progression points during Frost Moon
181	- Fixed a bug where Frost Moon's Waves 2, 3, and 4 required way too few points to progress
182	- Fixed an issue with ammo consumption for Flamethrower and Elf Melter
183	- Fixed a bug where Chain Knife and Flairon had a strange damage hitbox in the upper corner of the player
184	- Fixed a bug where Rocket Launcher could not received Ranged prefixes such as Unreal
185	- Fixed a bug where Beam Sword forced you to turn to face the direction it is firing its projectile when autoswinging
186	- Fixed a bug where Imp Staff would randomly rapidly fire at enemies under specific circumstances. It can still fire at an above average speed in these circumstances, but it isn't as extremely fast now.
187	- Fixed an issue where underground Mothrons did not check to make sure they were laying eggs on solid tiles, including laying eggs in lava like a terrible parent
188	- Fixed an issue where quadruped enemies would not fall through platforms
189	- Fixed an issue that prevented Horseman's Blade from proccing on certain targets, such as Moon Lord's eyes or naturally spawned critters
190	- Fixed some issues where size downscaled bosses in Special Seeds had inaccurate hitboxes
191	- Fixed Bee enemies and Explosive Bunnies being able to rapidly hit enemies with no iframe cooldown
192	- Fixed being idle on infinite flight mounts not protecting from Worm spawns
193	- Fixed Old One's Army Flyer behavior where they would fly under the ground and not come back up, thus avoiding defenses
194	- Fixed an issue where some Frost Legion enemies didn't have the correct movement speed
195	- Fixed a bug causing Super Star Shooter's projectile to die when having your back to a wall
196	- Fixed a bug where Corruptors and Giant Fungi Bulbs would fire at Hardcore ghosts
197	
198	C. Gameplay Functionality Issues
199	- Fixed some long running issues where the size or quantity of some worldgen features were not properly accounted for in Medium worlds, resulting less of some things like the Jungle or Mushroom biomes
200	- Fixed a bug that caused daily Tree Shake count to be cumulative across all worlds
201	- Fixed a worldgen bug that has existed since the beginning of the game that prevented Demon/Crimson Altars from spawning deep underground. You will now find many more of them much deeper Underground.
202	- Fixed an issue where some infected tiles were not being detected by the Dryad, including some sand types, plants, vines, and thorns
203	- Fixed an exploit allowing conservation of Etherian Mana after Old One's Army ends
204	- Fixing more inconsistencies between seeded PC and Mac/Linux worldgen, though ultimately it may be impossible to completely eliminate all variation due to fundamental OS differences at a basic level
205	- Fixed the player taking damage from Don't Starve darkness when in well lit areas due to being in another window
206	- Fixed an issue where joining into a world where the Real Estate Agent achievement was "valid" for unlock would not unlock it until the next time an NPC moved in. It should now unlock immediately upon joining.
207	- Fixed an issue where small patches of sand around the world would generate with Underground Desert backwalls, allowing those enemies to spawn
208	- Fixed an issue where Sandstone Chests that generated too high in the world would turn into Gold Chests instead
209	- Fixed another issue with Giant Mahogany Trees generating over chests or the Temple
210	- Fixed Lavafly Jar not counting as a light source for housing
211	- Fixed a bug with Boulder traps causing overlap issues with chests if they generated too close
212	- Fixed NPCs standing in front of each other too often, and Town Pets standing over chairs and blocking Town NPCs
213	- Fixed a bug where Life Fruit, Plantera Bulbs, and Jungle Plants would not properly break the plant tiles they replaced
214	- Fixed Campfire Minibiomes sometimes generating incorrectly
215	- Fixed Dirt Rod's Dirt Ball projectiles destroying some decorative tiles
216	- Fixed an issue where Smart Cursor would sometimes target solid blocks when trying to place Herb Seeds
217	- Fixed a similar issue where Smart Cursor would try to plant Pumpkins in non-valid locations
218	- Fixed a long running inconsistency where Tall Grass couldn't grow in front of most fences
219	- Fixed Mushroom/Ash Grass not breaking in one hit when using Gravedigger's Shovel
220	- Fixed the player being able to fish up Dungeon items before Skeletron is defeated
221	- Fixed an issue where NPCs could teleport home instantly at any time when standing on Dungeon Brick
222	- Fixed Dye Plants growing in Honey
223	- Fixed Jungle Torches not being used by Torch God's Favor when inside of the Temple
224	- Fixed some Rubble types "surviving" tile change via infection/Clentaminator when they should not.
225	- Fixed Pumpkins not breaking themselves when the tile beneath them was changed to be non-valid for plant growth
226	- Fixed a bug where Gold Goldfish could not spawn in underwater living tree tunnels
227	- Fixed Lucky Coin not working properly in Multiplayer on Expert and Master mode
228	
229	D. Visual / Audio Issues
230	- Fixed an issue where unsafe and safe versions of the same Wall type did not properly merge together
231	- Fixed an issue with OGG resource pack tracks not detecting loops properly
232	- Fixed an issue with some held projectiles (Spears, Flails) jittering a bit when the player goes up and down half-blocks
233	- Fixed the offset on Geyser trap tiles so that they merge more seamlessly with blocks they are placed on
234	- Fixed an issue with some gore moving at extremely high speeds through the entire world
235	- Fixed an issue with infected Cacti, Oasis plants, and Sea Oats only showing as green on the map
236	- Fixed an issue with falling Slush Blocks not having a sound or dust when Slush Balls break
237	- Fixed a sprite issue where most fences that were "floating" were visually cut-off at the bottom
238	- Fixed the top row of the underground background layer not allowing light, causing visual artifacts
239	- Fixed an issue where Crystal Shards could grow on sloped blocks, resulting in them floating
240	- Fixed an audio desync with certain guns in multiplayer
241	- Fixed a number of Rubble piles creating the wrong dust color when broken
242	- Fixed a minor visual offset with Video Visage's screen sprite when facing different directions
243	- Fixed a positioning issue with Furnace and Hellforge to resolve some tile sheet issues in texture packs
244	- Fixed cattails and vines not maintaining paint when growing
245	- Fixed King Slime's crown not properly adjusting its size under some circumstances
246	- Fixed an issue where Money Hair Dye's color system would break and cycle through colors of the rainbow when reaching particularly large quantities of money
247	- Fixed Frozen Chandelier's light being the wrong color
248	- Fixed Hardmode ores generating with paint when replacing a painted tile
249	- Fixed an issue where Silly Sunflower Bottoms and Frog Legs, when worn together, would show the player with no legs at all
250	- Fixed some spriting issues in the Minotaur pet's animation
251	- Fixed an issue where sitting in a chair while underwater and while also wearing an Inner Tube would make the player's legs draw incorrectly
252	- Fixed the Ocean not being bloody during a Blood Moon
253	- Fixed Kimono pants being treated like a robe, breaking sitting frames, as well as an issue with the female Kimono "jumping" sprite
254	
255	E. UI, Input, Text and Tooltip Issues
256	- Gamepad now tries matching Button Instructions to the inventory slot your cursor is on immediately. Hovering over a button or item with the cursor will show the relevant Gamepad instructions.
257	- Fixed an issue where exiting the research menu mid-animation would result in the animation resuming when you opened it back up later
258	- Fixed Info Accessories not properly updating their display when the game is paused
259	- Fixed an issue allowing Armor Swapping with sold items
260	- Fixed Moon Lord's health bar flickering when he spawns
261	- Fixed Gravedigger Shovel using two different recipes for Iron and Lead. It now just uses a single AnyIron recipe
262	- Fixed world names/seeds being able to exceed the size limit of the text box under certain conditions
263	- Fixed an issue where sorting Chests and then changing directly from that Chest to another Chest (without closing) would maintain the color highlight of the sorted slots
264	- Fixed an issue where Boss health bars that have scaled health due to multiplayer would have an incorrect display for players joining the server mid fight
265	- Fixed link buttons on main menu not working on Mac/Linux
266	- Fixed a bug where the Tongued debuff did not actually give its unique death message if it killed you
267	- Fixed a minor capitalization issue in the "Web Spit" projectile
268	- Wasp Gun's tooltip now properly indicates that it penetrates defense (Wasp Gun Wasp Gun)
269	- Fixed an issue where all of the 3 Shroomite Helmets caused the tooltip damage of weapons they boosted to be slightly inaccurate. It would make the tooltip damage round up by 1 extra, making for a displayed damage that was incorrect compared to the actual amount of damage done. The actual damage done has not changed.
270	- Fixed a bug where player kills by self-destructing enemies might give a death message for the wrong enemy
271	- Fixed an issue where the game would not display your dropped coin count if you dropped an inordinately large amount of platinum on death
272	- Fixed a text inconsistency in the Venom Flask tooltip
273	- Fixed an issue where NPCs would refer to the Underground as "NormalUnderground"
274	- Fixed some text menus in the game not being compatible with the virtual keyboard when using Gamepad
275	- Fixed Lava Moss' tooltip and rarity color not matching the other glowing moss
276	- Fixed a number of other inconsistencies with item rarity colors and sell values
277	- Fixed Djinn's Curse having "vanity" tooltip line, as it does actually confer mechanical benefits
278	
279	F. Multiplayer Syncing and Functionality Issues
280	- Fixed Tombstones desyncing when landing in multiplayer
281	- Fixed an issue with Moss growth not syncing in multiplayer when the moss was above ground
282	- Fixed some syncing issues with Nimbus Rod and Crimson Rod
283	- Fixed a certain server exploit
284	- Fixed a desync with Whips and Spears in multiplayer
285	- Fixed a server launch failure caused when providing an invalid world file pathway via the server config file
286	- Fixed a visual swing animation issue with Flying Knife when using Feral Claw-type accessories in multiplayer
287	- Fixed an issue causing Banner drops to be attributed to an uninvolved player on servers
288	- Fixed an issue where Keybrand's particle effects didn't show up for the user in multiplayer
289	- Fixed bucket-removed water not syncing properly sometimes in multiplayer
290	- Fixed a number of PVP debuffs not syncing properly in multiplayer
291	- Fixed a syncing issue with Tesla Turret projectiles in multiplayer
292	- Fixed a visual desync with flopping fish critters in multiplayer
293	- Fixed an issue where Dry Bombs and similar items would not sync fluid properly on servers
294	- Fixed an issue where Rainbow Gun could arc down and draw across the entire world for some people in multiplayer
295	- Fixed an issue with sloped blocks not syncing their slope changes when sand fell on them in multiplayer
296	
297	III. Labor of Love: Balance Changes:
298	
299	A. Global Mechanics Changes
300	Static Immunity Frames Last Hit
301	- All piercing projectiles that use static immunity no longer apply immunity on their "final hit", if they are a projectile which expires after enough pierces. This has very little impact on 	previously existing static immunity projectiles, but is important for several projectiles which are being changed to use static instead of global. Global Immunity projectiles already do 		this, so this change was made to account for some projectiles which were being changed from global to static, so that they did not receive an accidental damage nerf.
302	
303	Buff/Debuff Caps
304	- Player buff/debuff maximum increased from 22 to 44.
305	- Enemy debuff maximum increased from 5 to 20
306	
307	Post-Death Invincibility
308	- Duration increased from 1 to 3 seconds
309	
310	
311	B. Bosses
312	King Slime
313	- Now takes up more enemy slots, reducing or outright eliminating additional enemy spawns during his fight. This does not impact Slime Rain spawns.
314	
315	Brain of Cthulhu 
316	- Health increased from 1000 to 1250
317	- 5% Knockback resistance added across all difficulties (50/55/60% to 55/60/65%)
318	- Expert/Master illusions now become opaque much faster
319	- There is now a safe range around the player during Phase 1 to prevent BoC from teleporting directly on top of you (though it can still be extremely close)
320	- No longer has a map icon during Phase 2
321	
322	Deerclops
323	- Now takes up more enemy slots, reducing or outright eliminating enemy spawns during his fight
324	
325	Wall of Flesh
326	- Hungries no longer gain a 3rd stat bonus after 25% Wall of Flesh health. They will continue to use the 2nd stat bonus from 50% WoF health for the remainder of the fight.
327	- Wall of Flesh's tongued debuff pull speed now scales with the boss's speed in Expert/Master, to prevent the Wall from moving faster than it pulls you in at the end of the fight
328	
329	Queen Slime
330	- Maximum flight speed and acceleration in Phase 2 have been reduced by about 15%
331	- Queen Slime's minion projectile damage reduced from 30/80/150 to 30/68/120
332	- These same projectiles now generate some light to be more visible at night
333	- Now takes up more enemy slots, reducing or outright eliminating additional enemy spawns during his fight
334	
335	Plantera
336	- Increased distance before despawn timer begins ticking down dramatically.
337	
338	Golem
339	- Golem Body health increased from 9000 to 15000
340	- Golem Head health increased from 16000 to 25000
341	- Golem Fists health increased from 7000 to 10000
342	- Now charges its punches with a visual effect for half a second before firing them.
343	- Golem's Fists can no longer be deflected.
344	- Now takes up more enemy slots, reducing or outright eliminating enemy spawns during his fight
345	
346	Duke Fishron
347	- Health increased from 50,000 to 60,000
348	- Health scaling factor in Expert/Master increased from 1.6x to 1.65x
349	- Final Health values have increased from 50k/60k/76.5k to 60k/78k/99k
350	- Now invincible immediately after being summoned, and during his phase transitions
351	- Fixed an issue where Duke Fishron's Cthulhunado would sometimes instantly spawn on the player and hurt them, unavoidably. It should now spawn a certain distance below the player if there is no floor or platforms directly below, allowing the player time to avoid it
352	- When Enraged, Duke Fishron is much faster, and fires more frequent and faster Cthulhunados
353	
354	Empress of Light
355	- Fixed a issue where Empress of Light would sometimes teleport directly on top of the player after an attack
356	- Now takes up more MANY more enemy slots, reducing or outright eliminating enemy spawns during her fight. 
357	
358	Daytime Empress of Light, Skeletron, Skeletron Prime, and Dungeon Guardian
359	- "Instant kill" attacks will no longer be avoided by Dodge procs such as Hallowed Armor or Master Ninja Gear
360	
361	Lunatic Cultist
362	- Health scaling factor in Expert/Master increased from 1.25 to 1.5
363	- Final Health values have increased from 32k/40k/51k to 32k/48k/61k
364	- Ancient Light projectiles are no longer instantly killed, but actually take some damage to kill, and will be targetted by homing projectiles, soaking up some of your damage.
365	
366	Moon Lord
367	- Phantasmal Sphere damage reduced by 20%
368	- Phantasmal Sphere hitbox size reduced slightly
369	- Will now always drop 2 non-identical weapons
370	
371	C. Enemies, Threats and Invasions
372	Projectile Reflecting Enemies (Large Mimics, Selenians) (Nerf)
373	- Reflected Projectiles now only deal half-damage to the player
374	- Reflected Projectiles no longer scale and deal extra damage in Expert/Master mode.
375	
376	Teleporting Enemies (Teleporting Casters, Chaos Elementals, and Nebula Floaters)
377	- The protection radius around the player preventing them from teleporting directly onto you has been increased substantially
378	- The game will now also take your speed and direction into account when you are moving, and will further attempt to prevent these enemies from spawning directly in your path without time to react. However, this system is not absolute and only gives some extra distance, so it is still possible to crash into a recently teleported enemy if you do not alter course or are moving very fast.
379	- The protection radius around the player is even higher for Chaos Elementals and Nebula Floaters due to their not being stationary
380	
381	Lifeform Analyzer Rarities
382	- A number of enemies rare enough to show up on the Lifeform Analyzer have had their rarity levels changed to give proper priority based on enemies which they co-exist with. For example, Dye Beetles have been reduced to Rarity 1, so that any higher Rarity enemy will take priority on the display.
383	- Voodoo Demons are now also listed on the Lifeform Analyzer
384	
385	Pumpkin Moon and Frost Moon
386	- Pumpkin Moon can now go up to Wave 20. Wave point requirements for Waves 15-20 match Frost Moon.
387	- Pumpkin Moon's wave composition has been completely rearranged to account for this.
388	- Pumpkin Moon bosses are now capped in number, more closely resembling the behavior of Frost Moon bosses
389	- Increased the number of enemy slots taken up by Mourning Wood and Pumpking, to be more in line with Frost Moon bosses, dramatically reducing how many can spawn at a time
390	- All regular enemies in Pumpkin/Frost Moon now have low per-player Health scaling in Expert/Master multiplayer. The boss units already had scaling.
391	- Pumpkin Moon trophies now drop using Frost Moon drop rates, instead of dropping from 100% of Wave 15 kills.
392	- Pumpkin Moon boss drop-rate-by-wave multiplier has been reduced, though drops are still more common than Frost Moon levels. This is partly to account for having a higher wave cap, though drops are still slightly less common than before.
393	- Both Pumpkin Moon and Frost Moon's "expert drop bonus" modifier has been reduced slightly, with the base drop rates being increased by the same amount. The end result is that Classic mode drops are slightly more generous, while Expert drop rates stay the same. (This is after taking Pumpkin Moon's previous change into account)
394	- Both Pumpkin Moon and Frost Moon now receive a 2.5x point multiplier when playing in Master mode. Previously, they received a 2x multiplier in Expert, but no additional gain in Master.
395	
396	Poltergeist
397	- Can now fly freely into the air, not just on the ground
398	- Health reduced from 2000 to 1250
399	- Pumpkin Moon wave progression points increased from 8 to 10
400	- Due to increased number present in the event, increased the kill count needed for a banner
401	
402	Splinterling
403	- Health increased from 900 to 1200
404	- Due to increased number present in the event, increased the kill count needed for a banner
405	- Reduced base Spooky Wood drop count due to increased numbers of Splinterlings killed per Pumpkin Moon. However, due to the faster point gain in Expert/Master, they now have bonus drop quantities in Expert and Master.
406	
407	Hellhound
408	- Health increased from 1200 to 1800
409	- Pumpkin Moon wave progression points increased from 4 to 5
410	- Due to increased number present in the event, increased the kill count needed for a banner
411	
412	Headless Horseman
413	- Health reduced from 10000 to 5000.
414	- Can now fire a pumpkin projectile at the player
415	- Pumpkin Moon wave progression points increased from 25 to 50
416	- Now has the same Health scaling as Pumpking and Mourning Wood in Expert/Master multiplayer
417	
418	Mourning Wood
419	- Health increased from 12000 to 14000
420	- Defense increased from 28 to 34
421	- Increased the number of enemy slots taken, to be more in line with Frost Moon bosses, dramatically reducing how many can spawn at a time
422	- Reduced base Spooky Wood drop count. However, due to the faster point gain in Expert/Master, they now have bonus drop quantities in Expert and Master.
423	
424	Pumpking
425	- Health increased from 22000 to 26000
426	- Defense increased from 36 to 40
427	- Increased the number of enemy slots taken, to be more in line with Frost Moon bosses, dramatically reducing how many can spawn at a time
428	
429	Old One's Army
430	- Etherian Lightning Bugs now spawn in OOA Tier 3 Wave 6 instead of Wyverns
431	- The Eternia Crystal now has 2x as much health on Expert and 3x as much health on Master.
432	
433	Martian Saucer
434	- Increased the hitbox size of the core in Phase 2
435	
436	Dreadnautilus
437	- Charge attack has less tracking and a wider turning radius, meaning it is easier to avoid
438	- Projectiles are now no longer blocked by tiles
439	- Projectiles are more lit up/visible at night
440	
441	Blood Squid
442	- Health reduced from 1000 to 750
443	- Projectile damage reduced from 100 to 70
444	- Projectiles are more lit up/visible at night
445	
446	Hemogoblin Shark
447	- Projectiles are more lit up/visible at night
448	
449	Clowns
450	- Damage of Chattering Teeth Bomb reduced from 200 to 120
451	- Damage of Happy Bombs reduced from 160 to 120
452	- Happy Bombs now glow, making them easier to see
453	- Chattering Teeth Bombs now have a sound effect when spawned and occasionally played passively, helping the player to be aware of them
454	- Clown's drop pool has also been overhauled:
455	- Is now the sole source of KO Cannon, having a 1/5 chance to drop it
456	- Bananarang drop rate has been increased from 1/30 to 1/10 (See Bananarang for other changes to this item)
457	- Bloody Tear drop rate increased from 1/100 to 1/10 (like other uncommon Blood Moon enemies)
458	
459	Antlion Larvae
460	- Defense reduced from 4 to 2
461	- Health reduced from 35 to 30
462	- Maximum speed slightly reduced, particularly when jumping
463	
464	Giant Antlion Chargers
465	- Defense reduced from 22 to 16
466	
467	Giant Antlion Swarmers
468	- Defense reduced from 18 to 12
469	
470	Tomb Crawlers
471	- Defense of body segments reduced from 16 to 12
472	- Defense of tail segment reduced from 20 to 14
473	
474	Tomb Crawlers and Dune Splicers
475	- Spawn rates reduced
476	- In the upper levels of the Desert, there is a further reduction in spawn rates
477	
478	Rolling Cacti
479	- Damage reduced from 90 to 70
480	
481	Jellyfish
482	- Expert Electric Shock attack now applies to projectile contact weapons (Spears, Shortswords, Solar Eruption, Sleepy Octopod, Sky Dragon's Fury, and Whips)
483	
484	Snow Flinx
485	- Snow Flinxes now have a more consistent spawn rate on Ice/Snow. Previously, was incapable of spawning on Snow or Ice under most conditions.
486	
487	Lost Girl
488	- Instead of their spawn rate decreasing in Hardmode, it stays the same the entire game. This means that their Hardmode spawn rate has changed from 1/200 to 1/80
489	- Base money drop value reduced from 5 to 2 Gold
490	
491	Bone Serpents
492	- Head/Body/Tail Damage increased from 30/15/10 to 36/20/16
493	- Head/Body Defense increased from 10/12 to 12/18. Tail unchanged.
494	- Health increased from 250 to 300
495	- Movement speed increased
496	- Further stat bonuses specifically on FTW and Everything Seed
497	
498	Rune Wizard
499	- Spawn rate increased from 1/300 to 1/200
500	
501	Rock Golems
502	- Now throw rocks less frequently and the rocks move a little slower as well
503	- Spawn rate reduced
504	- Base money drop value reduced from 5 to 2.5 Gold
505	- Rock Golem Head drops twice as often to account for the rarity change
506	
507	Giant Fungi Bulbs
508	- Will no longer fire at you if they do not have line of sight
509	- Projectiles can no longer move through walls, and will break on impact with blocks
510	
511	Gastropods
512	- Now have some built in inaccuracy when firing, reducing their likelihood of hitting the player from long distances
513	
514	Cursed Hammer and Crimson Axe
515	- Fixing a long standing inconsistency in their spawn code, that resulted in them being dramatically rarer than Enchanted Swords. They should be about as common as Enchanted Swords now, particularly notably with Crimson Axes, which were impacted more severely by the inconsistency.
516	
517	Desert Spirits
518	- Projectile damage reduced from 80/120/180 to 60/88/132
519	
520	Jungle Creeper
521	- Defense reduced from 40 to 28
522	
523	Moss Hornets
524	- Now has a chance to drop Stingers
525	
526	Necromancers and Ragged Casters
527	- Now has a grace period of over a second after teleportation before they begin firing. (This is the same as what Diabolists always had)
528	

```


---

## 🤖 Assistant · 2026-08-09T11:40:36.873Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I've now read lines 2374-2901 (the persisted file covers up to about line 2901 of the changelog, since sed printed 2374-2900). Actually the persisted file has 528 lines, corresponding to changelog lines 2374-2901.

Now let me continue reading lines 2901-4368. That's ~1470 lines. I'll read in chunks of ~400 lines to keep outputs manageable.

Let me proceed.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:40:37.374Z · glm-x-preview-260804

```
第一段已读完(对应官方 2374-2901 行)。继续读取后续段落。
```


---

## 🤖 Assistant · 2026-08-09T11:40:37.377Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '2902,3300p' \"~/Library/Application Support/Steam/steamapps/common/Terraria/changelog.txt\"",
 "description": "Read official changelog lines 2902-3300"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:40:43.035Z

**📎 ToolResult**

```
All Celestial Pillars
- Expert/Master worlds no longer have an increased Celestial Pillar kill requirement. They need 100 now like Classic Difficulty Worlds.
- Upon defeating Moon Lord, Lunar Pillars now require only 50 kills to lower the Pillar shields (applies in all difficulties)

Solar Crawltipedes
- Head damage reduced from 150 to 120
- Body damage reduced from 100 to 80

Solar Corites
- Spawn rate reduced by half
- Should no longer charge at the player from significantly off screen
- Now have a brief wind up animation before their charge, giving more notice
- Charge speed is slightly slower

Nebula Floaters
- Now have a 0.5 second delay after teleportation during which they cannot fire
- Counter-teleportation chance reduced from 1/4 to 1/6
- The maximum number of active Nebula Floaters at any one time increased from 2 to 3
- The spawn rate of Nebula Floaters has been doubled, though they cannot exceed their unit cap

Nebula Predictors
- The maximum number of active Nebula Predictors at any one time increased from 2 to 3

Nebula Brain Sucklers
- Spawn rate has been reduced by 40%

Vortex Alien Queens
- Walk and chasing speed increased significantly
- Projectile speed reduced

Vortex Alien Larvae
- Now included in the Alien Queen family "cap". For context: the game has a cap on how many Alien Hornets and Alien Queens could be in play, to prevent evolving Queens from becoming too numerous. However, Larvae were not part of that cap, and so could spawn and evolve up into Hornets/Queens normally, eventually creating overwhelming numbers. After this change, Alien Larvae simply won't spawn on Queen death once this internal limit is reached.

Vortex Portals (Both Hornet Portals and Vortexian Portals)
- Now makes a more distinct sound when spawning, giving the player notice that it is present
- Vortexian Portals make a more pronounced sound when firing, again, to give audio feedback about the threat

Storm Diver
- Improved its air mobility, to better keep up with the player
- Widened its firing angle
- Firing rate dramatically increased
- Minimum delay before first shot reduced
- Projectile speed increased
- One of its projectiles is always accurate
- Added a visual effect just prior to firing to give advanced warning to the player

Stargazers
- Beam now has a half second "charge up" beam effect, giving players a chance to react and avoid the incoming beam of damage. The actual duration of the damage period remains the same.

Large Stardust Cells
- Knockback resistance increased from 50% to 70%
- Are now faster when chasing the player

Milkyway Weavers
- Movement speed increased by 50%
- Periodically stops chasing to spawn a new Stardust enemy after a few seconds of charging


D. Melee Weapons
All "Broadswords"
- All broadsword-class melee weapons (this also includes pickaxes, axes, hammers, and hamaxes) now use local immunity frames on hit. Very notably, this means that projectile swords will no longer block their own piercing projectiles from hitting a target at point blank range. It will also result in more consistent hitting when mixing multiple sources of damage (Piercing minions and swords, for example)

All Flails
- Knockback when spinning flails has been increased from 25% to 35% of normal knockback
- Spinning flails now hit up to 4 times a second instead of 3 times a second. Flails which already hit 4 times a second have been increased to 5 times a second.

Copper Broadsword
- Damage increased from 8 to 9
- Usetime reduced from 23 to 21
- Size Scale increased from 1x to 1.1x (As a reminder, scale dictates the size of the weapon; this makes the sword's size and reach 10% larger)

Tin Broadsword
- Damage increased from 9 to 10
- Usetime reduced from 22 to 20
- Size Scale increased from 1x to 1.1x

Iron Broadsword
- Damage increased from 10 to 12
- Usetime reduced from 22 to 20
- Size Scale increased from 1x to 1.15x
- Knockback increased from 5 to 5.5

Lead Broadsword
- Damage increased from 11 to 13
- Usetime reduced from 21 to 20
- Size Scale increased from 1x to 1.15x
- Knockback increased from 5 to 5.5

Silver Broadsword
- Damage increased from 11 to 14
- Usetime reduced from 21 to 20
- Size Scale increased from 1x to 1.2x
- Knockback increased from 5 to 6

Tungsten Broadsword
- Damage increased from 12 to 14
- Usetime reduced from 20 to 19
- Size Scale increased from 1.025x to 1.2x
- Knockback increased from 5 to 6

Gold Broadsword
- Damage increased from 13 to 15
- Usetime reduced from 20 to 18
- Size Scale increased from 1.05x to 1.25x
- Knockback increased from 5 to 6.5

Platinum Broadsword
- Damage increased from 15 to 16
- Usetime reduced from 19 to 17
- Size Scale increased from 1.075x to 1.25x
- Knockback increased from 5 to 6.5

Cactus Sword
- Damage increased from 8 to 10
- Usetime reduced from 32 to 30

Wooden Sword
- Usetime reduced from 25 to 20
- Size Scale increased from 0.95 to 1.0
- Knockback increased from 4 to 5

Boreal Sword
- Usetime reduced from 23 to 20
- Knockback increased from 5 to 6

Palm/Mahogany Sword
- Usetime reduced from 23 to 19
- Knockback increased from 5 to 6

Ebonwood/Shadewood Sword
- Damage increased from 10 to 11
- Usetime reduced from 21 to 19
- Knockback increased from 5 to 6

Wooden Boomerang
- Damage increased from 8 to 10
- UseTime increased from 16 to 20 (decreases short range DPS but does not impact long distance DPS)

Enchanted Boomerang
- Damage increased from 13 to 17
- UseTime increased from 15 to 20 (decreases short range DPS but does not impact long distance DPS)

Zombie Arm
- Damage increased from 12 to 15
- Usetime reduced from 23 to 22
- Size Scale increased from 1x to 1.2x
- Knockback increased from 4.25 to 5.5

Bone Sword
- Damage increased from 16 to 19
- Size Scale increased from 1.05x to 1.2x
- Knockback increased from 4.5 to 5.5

Bat Bat
- Damage increased from 31 to 36

Shroomerang
- Increased damage from 14 to 23
- UseTime increased from 15 to 20 (decreases short range DPS but does not impact long distance DPS)
- Increase drop rate from 1/100 to 1/40

Ice Boomerang
- Increased damage from 16 to 21
- Now has a chance to inflict Frostburn
- UseTime increased from 15 to 20 (decreases short range DPS but does not impact long distance DPS)

Gladius
- Knockback increased from 0.5 to 3
- Drop rate increased from 1/40 to 1/20

Purple Clubberfish
- Damage increased from 24 to 35
- Knockback increased from 7 to 8

Tentacle Spike
- Damage increased from 19 to 20
- Usetime reduced from 23 to 21

Falcon Blade
- Size scale increased from 1.05x to 1.175x

Mandible Blade
- Damage increased from 14 to 16
- Size scale increased from 1x to 1.1x

Storm Spear
- Damage increased from 12 to 14
- Projectile damage increased from 1.25x to 1.5x of base damage

Trident
- Now generates light when swung underwater

Katana
- Damage increased from 16 to 18
- Usetime reduced from 22 to 20
- Size Scale increased from 1 to 1.1

Candy Cane Sword
- Damage increased from 16 to 19
- Usetime reduced from 27 to 25

Fruitcake Chakram
- Damage increased from 14 to 19

Bladed Glove
- Damage increased from 12 to 14

Bloody Machete
- Damage increased from 15 to 20

Light's Bane
- Now also generates a short range diagonal slash of darkness every time the sword is swungt, dealing half of the base damage of Light's Bane
- Damage reduced from 18 to 16

Blood Butcherer
- Now uses a system very similar to Tentacle Spike. Every successful strike on an enemy applies a stack of "Blood Butchered", a short lived damage over time effect. Each of these stacks are signified by a gout of blood spouting forth from the enemy.
- Blood Butchered can stack up to 5 times, and each stack deals 4 damage over time, allowing for a maximum of 20 damage over time.
- Stacks of Blood Butchered last for 9 seconds before expiring

Rotted Fork
- Damage increased from 14 to 17
- Now generates a shockwave at the end of the spear, which increases its effective range. This shockwave also scales in size with melee speed, so you can now expect more pronounced Melee Speed benefits for Rotted Fork.

Phaseblades (all colors)
- Damage increased from 25 to 26
- Usetime reduced from 25 to 18

Starfury
- Stars now fall 25% faster
- Starfury will now fall through blocks until reaching the player's cursor, unless the cursor is pointing into solid block, in which case it will fall to the nearest open air block. It should generally fall more often and more reliably through blocks compared to before.

Blade of Grass
- Now fires an upward spiraling razor leaf from the sword with every swing. This projectile has a short-to-medium range
- This projectile does low damage, but ignores a substantial amount of defense, ensuring that it inflicts damage reliably
- Damage reduced from 28 to 18
- Usetime reduced from 30 to 20
- Increased knockback from 3 to 4.5
- Crafting recipe now requires 3 Vines, and the Jungle Spore cost has been increased from 12 to 15
- Note: Poison has been buffed in 1.4.4, and Blade of Grass and its Razor Leaf both benefit from this buff

Thorn Chakram
- Poison chance increased from 20% to 50%
- Note: Poison has been buffed in 1.4.4

Bee Keeper
- Damage increased from 26 to 30
- Resprited and size increased

Lucy
- Damage increased from 26 to 27
- Usetime reduced from 17 to 15
- Lucy no longer uses useTurn; this means that if you are currently swinging, changing your walking direction will not change the direction you are swinging her
- Lucy's idle chatter messages are now less frequent

Muramasa
- Upon striking an enemy, Muramasa will generate an additional slashing cut over the affected target, dealing half of the base damage of Muramasa
- Damage reduced from 26 to 24

Valor
- Damage increased from 22 to 28

Flamarang
- Damage increased from 32 to 49
- On Fire chance increased from 20% to 50%
- UseTime increased from 15 to 20 (decreases short range DPS but does not impact long distance DPS)

Fiery Greatsword -> Volcano
- Fiery Greatsword's name has been changed to Volcano
- Upon striking an enemy, Volcano will now generate an fiery explosive area of effect, dealing additional damage to the original target and nearby enemies!
- Usetime reduced from 30 to 40

Night's Edge
- Night's Edge now has an area of damaging energy around the blade, dealing damage in a larger, wider area of effect, including better coverage behind the player.
- Additionally, this swing radius will spin around a second time in the direction of the player's aim, increasing the range of the weapon's forward reach to short-to-medium range

Dark Lance
- Damage increased from 29 to 34
- Now generates a shockwave at the end of the spear, which increases its effective range. This shockwave also scales in size with melee speed, so you can now expect more pronounced Melee Speed benefits for Dark Lance.
- Now inflicts Shadowflame

Breaker Blade
- Damage increased from 43 to 70
- Usetime increased from 29 to 35
- Size Scale increased from 1.05x to 1.15x
- Breaking effect damage multiplier increased from +100% to +150%

Cobalt Sword
- Damage increased from 39 to 40
- Usetime reduced from 23 to 19
- Size Scale increased from 1.1x to 1.2x
- Knockback increased from 3.85 to 5

Palladium Sword
- Damage increased from 45 to 49
- Usetime reduced from 25 to 22
- Size Scale increased from 1.125x to 1.2x
- Knockback increased from 4.75 to 5.5

Mythril Sword
- Damage increased from 49 to 50
- Usetime reduced from 26 to 20
- Size Scale increased from 1.15x to 1.2x

Orichalcum Sword
- Damage increased from 50 to 59
- Usetime reduced from 25 to 22
- Size Scale increased from 1.17x to 1.22x

Adamantite Sword
- Damage increased from 56 to 61
- Usetime reduced from 26 to 21
- Size Scale increased from 1.2x to 1.25x

Titanium Sword
- Damage increased from 58 to 61
- Usetime reduced from 25 to 20
- Size Scale increased from 1.2x to 1.25x

Pearlwood Sword
- Damage increased from 11 to 30
- Usetime reduced from 21 to 15
- Is now autoswing

Cobalt Naginata
- Damage increased from 29 to 44

Palladium Pike
- Damage increased from 32 to 44

Mythril Halberd
- Damage increased from 35 to 45

Orichalcum Halberd
- Damage increased from 36 to 46

Adamantite Glaive
- Damage increased from 38 to 49

Titanium Trident
- Damage increased from 40 to 48

Phasesabers (all colors)
- Damage increased from 42 to 48
- Usetime reduced from 20 to 16
- Crystal Shard crafting cost reduced from 50 to 25

Cutlass
- Damage increased from 49 to 53
- Use Time reduced from 17 to 16

Frostbrand
- Projectile cooldown reduced from 55 frames to 30 frames.
- No longer uses the "chirp" sound when the cooldown is ready, as it would be too often.
- Projectile now inflicts Frostbite
- Pierce Count increased from 2 to 3
- Projectile now inflicts static immunity, meaning it will no longer interfere with other sources of piercing damage

Ice Sickle
- Damage increased from 42 to 50
- Range of Ice Sickle projectiles increased by 50%
- Projectile damage reduced from 100% of base damage to 50% of base damage
- Projectile changed to use static frames, and reduced the immune time between hits (deals damage slightly more often)
- Projectile pierce count reduced from 5 to 3

Bladetongue
- Ichor Shot pierce count reduced from unlimited to 5 hits
- Projectile now inflicts static immunity, meaning it will no longer interfere with other sources of piercing damage

Slap Hand
- Damage increased from 35 to 55
- Usetime reduced from 21 to 20

Hel-Fire
- Now inflicts Hellfire instead of On Fire

Amarok
- Now inflicts Frostbite instead of Frostburn

Chain Guillotine
- Chains now move roughly 25% faster and fly 50% further

Bananarang
- Is now a single item, not 10 stacked items. As a result, can now have prefixes.
- Damage reduced from 55 to 45
- Sell price of a single Bananarang increased accordingly
- Now has a 10% chance to drop from Clowns

Sergeant United Shield
- Knockback increased from 0 to 2, also allowing it access to better reforge modifiers

Beam Sword
- Projectile cooldown reduced from 60 frames to 35 frames.
- No longer uses the mana chirp system to indicate projectile is ready to fire
- Is now autoswing
- No longer uses useTurn; this means that if you are currently swinging, changing your walking direction will not change the direction you are swinging it
- No longer forces you to turn to face the direction the projectile is being fired in while swinging

Excalibur
- Excalibur now has an area of damaging energy around the blade, dealing damage in a larger, wider area of effect, including better coverage behind the player.

```


---

## 🤖 Assistant · 2026-08-09T11:40:44.438Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Continuing. Read 3301-3700.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:40:44.439Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '3301,3700p' \"~/Library/Application Support/Steam/steamapps/common/Terraria/changelog.txt\"",
 "description": "Read official changelog lines 3301-3700"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:40:50.804Z

**📎 ToolResult**

```
- Damage increased from 66 to 72

Gungnir
- Damage increased from 42 to 61
- Now generates a shockwave at the end of the spear, which increases its effective range. This shockwave also scales in size with melee speed, so you can now expect more pronounced Melee Speed benefits for Gungnir.

Light Disc
- Is now a single item, not 5 stacked items. As a result, can now have prefixes.
- Recipe cost has been multiplied by 5 (since you now only need to make 1). Similarly, it now sells for 5x as much.
- Damage increased from 57 to 60
- UseTime reduced from 15 to 14
- Can now shoot up to 6 Discs at once instead of 5.
- Projectile speed/distance increased from 13 to 16

True Night's Edge
- True Night's Edge now has an area of damaging energy around the blade, dealing damage in a larger, wider area of effect, including better coverage behind the player.
- Instead of a sword projectile, it now fires a large, spinning disc of energy which travels a medium-long distance, striking multiple times
- Damage reduced from 105 to 70
- Use Time increased from 26 to 32

True Excalibur
- True Excalibur now has a very large area of damaging energy around the blade, dealing damage in a dramatically wider area of effect, including better coverage behind the player.
- It no longer fires a projectile sword beam
- Damage increased from 70 to 72
- Usetime increased from 16 to 18

Brand of the Inferno
- Resprited and slightly increased in size
- Now inflicts Hellfire instead of On Fire

Chlorophyte Saber
- Projectile cooldown reduced from 42 to 28 frames
- No longer uses the mana chirp system to indicate projectile is ready to fire
- Projectile damage reduced from 100% of base damage to 70%
- Projectiles linger 50% longer
- Projectiles now use static immune frames

Chlorophyte Claymore/Partisan
- Projectiles now use static immune frames

Ghastly Glaive
- Reduced the immunity frames applied by the spear itself, allowing it to hit a single target more often when swung

Death Sickle
- Knockback decreased to prevent enemies from being knocked out of the spinning blades

Butcher's Chainsaw
- Both the Chainsaw and its Sparks now use static immune frames. As a direct consequence of this, the sparks are now able to hit the same target that they are being spawned off of when hitting with the chainsaw. This results in a notable increase in single target damage when hitting an enemy with the chainsaw.
- Spark projectiles now inflicts Hellfire instead of On Fire

Terra Blade
- Damage reduced from 115 to 85
- Usetime increased from 14 to 18
- Terra Blade now has an area of damaging energy around the blade, dealing damage in a larger, wider area of effect, including better coverage behind the player.
- Instead of a projectile sword beam fired on a cooldown, Terra Blade now fires a medium-long range, rapidly moving slash of green energy with every swing

Scourge of the Corruptor
- Minieaters now move and track enemies faster
- The average number of minieaters has been increased from 2.67 to 3, and the number is a much simpler 2-4 range

Paladin's Hammer
- Is now autoswing

Keybrand
- Damage increased from 85 to 105
- Bonus critical chance increased from 14% to 17%
- Reduced the maximum power of the scaling damage effect. This is canceled out by the damage buff, so that low-health damage is the same as it was before. At higher health, enemies will take more damage than before.

Horseman's Blade
- Horseman's Blade now has an area of damaging energy around the blade, dealing damage in a larger, wider area of effect, including better coverage behind the player.
- Damage increased from 75 to 150
- The pumpkins now deal 100% of the base damage of the sword instead of 150% (this is still more than they did before)
- Pumpkins will no longer be generated from statue spawned enemies.

North Pole
- UseTime increased from 25 to 30
- Now spawns half as many projectiles, but the damage of the spear projectile now deals base damage and the flakes deal 70% base, compared to the previous 80% for the spear projectile and 63% for the snowflakes
- Removed the impact of wind on flakes. Their spawning position is now semi-randomized, so that they don't all fall in the exact location.
- Spear projectiles and flakes now have a much shorter projectile lifetime

Christmas Tree Sword
- Projectile damage increased from 75% of base damage to 100%

Flairon
- Bubbles now last 33% longer before popping
- The range at which the bubbles will lock on and chase a target has been increased by 30%

Starlight
- Range now increases with Titan Glove and prefix size modifiers

Influx Waver
- Damage reduced from 110 to 100
- The secondary projectiles spawned after a successfully landed projectile hit will now move with their target, significantly reducing the chance of missing

Flying Dragon
- Usetime reduced from 25 to 20
- No longer has a damage penalty when it it has no line of sight with targets

Star Wrath
- Damage increased from 110 to 170
- Projectile damage reduced from 2x base damage to 1x base damage
- Falling stars now use local immunity, so each star will be able to hit a target for damage.

Meowmere
- Usetime reduced from 16 to 14
- Projectiles now deal 1.25x of the base sword damage
- Projectiles now use local immunity. Each individual bouncing cat has its own damage timer, so they will never conflict with each other.

Terrarian
- Both the Yoyo and the Orbs now use static immunity. Because the Yoyo and Orbs now each do damage without being blocked by the other, this results in a substantial increase to Terrarian's potential damage

Jousting Lance
- Damage increased from 56 to 60

Hallowed Jousting Lance
- Damage increased from 78 to 90

Shadow Jousting Lance
- Damage increased from 108 to 130


E. Ranged Weapons and Ammo
Flintlock Pistol
- Damage increased from 10 to 13
- Knockback increased from 0 to 1, allowing access to better modifiers

Musket
- Usetime reduced from 36 to 32
- No longer autofire

Undertaker
- Damage increased from 15 to 22
- Usetime reduced from 23 to 20
- Knockback increased from 1 to 2

Blood Rain Bow
- Projectiles now generate a little bit of light and can be seen better at night

Harpoon
- Projectile now uses local immunity. In practice, this means that no matter how close/rapidly you fire at the target, you will never miss due to immune frames from the previous shot

Spiky Balls
- Damage increased from 15 to 16
- Pierce Count increased from 6 to 7

Star Cannon
- Knockback increased from 0 to 3, allowing access to better modifiers

Bee's Knees
- To correct a code inconsistency issue, effective useTime reduced from 24 to 23

Quad Barreled Shotgun
- Damage reduced from 17 to 14
- Pellet count increased from 6 to 8
- One pellet is now always aimed towards the cursor accurately

Handgun
- Damage increased from 17 to 26
- Usetime increased from 10 to 15

Phoenix Blaster
- Damage increased from 24 to 33
- Usetime increased from 11 to 17

Cobalt Repeater
- Damage increased from 32 to 35.
- UseTime reduced from 24 to 23.

Palladium Repeater
- Damage increased from 34 to 37.
- UseTime reduced from 23 to 22.

Mythril Repeater
- Damage increased from 36 to 39.
- UseTime reduced from 22 to 20.

Orichalcum Repeater
- Damage increased from 38 to 40.
- UseTime reduced from 21 to 19.

Adamantite Repeater
- Damage increased from 40 to 42.
- UseTime reduced from 19 to 18

Titanium Repeater
- Damage increased from 41 to 43.
- UseTime reduced from 18 to 17.

Marrow
- Damage from 50 to 53
- Is now autofire

Ice Bow
- Usetime reduced from 16 to 14

Hallowed Repeater
- Damage reduced from 53 to 50
- Usetime increased from 16 to 17

Flamethrower
- Now uses local immunity frames on its projectiles
- Now ignores up to 15 points of enemy defense before losing damage
- Pierce count increased from 3 to 4
- Reworked visuals and hitbox size
- Now inflicts Hellfire instead of On Fire

Super Star Shooter
- The Star Slash now uses static immunity, so its immune frames will no longer block subsequent Star Shots from hitting
- The Star Slash now inflicts 75% of base damage instead of 50%

Pulse Bow
- Damage reduced from 85 to 80
- Now sold after defeating all 3 Mechs, instead of after Plantera

Phantom Phoenix
- The Phoenix projectile now inflicts Hellfire instead of On Fire. The converted Fire Arrows still inflict On Fire, as they are just normal Fire Arrows

Venus Magnum
- Usetime increased from 8 to 9
- Is now autofire

Rocket Launcher
- Damage increased from 45 to 55

Elf Melter
- Damage reduced from 60 to 53
- Bursts of flames per shot reduced from 6 to 5
- Now uses local immunity frames on its projectiles
- Now ignores up to 15 points of enemy defense before losing damage
- Pierce count increased from 3 to 4
- Now inflicts Frostbite instead of On Fire
- Reworked visuals and hitbox size

Electrosphere Launcher
- Electrosphere Missiles no longer deal direct damage, but still impact and turn into the Electrospheres which will then hurt the target normally

Aerial Bane:
- Note: No actual change has been made to its functionality, only the way its damage is displayed on the tooltip
- The tooltip base damage now shows ground damage done, and not the air damage done, to more accurately match the tooltip

Celebration MK2
- Damage increased from 40 to 50
- Fixed a bug that caused red missiles to rapidly hit every frame, doing more damage than expected

Archery Potion
- Bow damage bonus reduced from 1.2x to 1.1x

Ichor/Cursed Darts
- Ichor Dart damage reduced from 12 to 10
- Cursed Dart damage reduced from 10 to 9
- Fixed a bug that allowed Ichor Dart to hit rapidly every frame when used at very close range, dealing much more damage than expected

Exploding Bullets
- No longer inflicts self-damage

Frostburn Arrows
- Ammo damage reduced from 9 to 7

Holy Arrows
- Star damage reduced from 50% to 33%

Cluster Rockets (all variants) 
- Fragment damage increased from 33% to 50%


F. Magic Weapons
Base Mana Regeneration
- The base mana regen rate (the amount regenerated when moving and not using Mana Regen Potion) has been more than doubled
- The mana regen bonus when stationary and/or using Mana Regen Potion has been cut by 1/3rd. This reduction is the exact size of the amount added to the base regen rate, so there is no net gain in the total amount of regen possible.
- A player using Mana Regen Potion/Stationary should have the same mana regen speed as before, but the minimum mana regeneration rate has been increased substantially, making Mana Regen Potion/being stationary less mandatory for playability

Wand of Sparking
- Average duration of On Fire slightly increased

Amethyst Staff
- Mana cost increased from 3 to 5, allowing it to obtain better prefixes
- Damage increased from 14 to 15
- Usetime reduced from 40 to 37

Topaz Staff
- Mana cost increased from 4 to 5, allowing it to obtain better prefixes
- Damage increased from 15 to 16
- Usetime reduced from 38 to 36

Sapphire Staff
- Mana cost increased from 5 to 6
- Damage increased from 17 to 18
- Is now autofire

Thunder Zapper
- Damage increased from 12 to 20
- Mana cost increased from 5 to 7
- Knockback increased from 2 to 3

Crimson Rod
- Duration of clouds increased to 5 minutes
- Now uses static frames, so immune frames will no longer interfere with non-Crimson Rod sources of damage
- Mana cost increased from 10 to 30

Weather Pain
- Pierce count from 12 to 15
- Time between hits increased from 20 frames to 25 frames
- Duration of projectile increased by 2 seconds

Bee Gun
- Now has a token knockback value, allowing access to better modifiers

Magic Missile
- Damage increased from 27 to 35

Aqua Scepter
- Damage increased from 16 to 27
- Knockback increased from 5 to 7
- Mana Cost increased from 6 to 7
- Range increased substantially and its angle of descent is more gradual

Flower of Fire
- Projectile speed/distance increased from 6 to 7.5
- Now bounces 1 additional time

Zapinators (Grey and Orange)
- Usetime reduced from 37 to 36

Magic Dagger
- Damage reduced from 40 to 35
- Is now autofire
- Now uses local immune frames, as the fire rate was so fast that they conflicted with themselves
- Distance before daggers begin to fall has been increased by 50%

Cursed Flames
- Damage increased from 50 to 55

Flower of Frost
- Projectile speed/distance increased from 7 to 9
- Now inflicts Frostbite instead of Frostburn

Golden Shower
- Damage increased from 21 to 30

Blood Thorn
- Slightly increased the size of the thorns
- Thorns now last 40% longer
- Thorns can now sprout from platforms if they are in-range.
- Increased pierce count per thorn from 3 to 4
- Removed a system accidentally left on Blood Thorn since 1.4, that caused it to have unintended damage loss every time a thorn hit a target. Should immediately result in much higher damage when a target it being hit repeatedly by the same cast.

Meteor Staff
- Mana cost reduced from 13 to 9

Frost Staff
- UseTime reduced from 16 to 12
- Now inflicts Frostbite

Shadowflame Hex Doll
- Damage reduced from 40 to 32
- Now uses local immunity, meaning each of its tendrils can hit on their own immunity timer
- Now always fires one tendril directly towards the cursor, though the others will continue to vary wildly beyond close range

Spirit Flame
- Doubled the size of its AoE damage. Note: this AoE was so small before that it was nearly incapable at hitting multiple targets. This is still a very small AoE effect, but should now be able to hit two targets directly next to each other.
- Projectile duration increased by 25%

Nimbus Rod
- Duration of clouds increased to 5 minutes
- Damage reduced from 36 to 30
- Now uses static frames, so immune frames will no longer interfere with non-Nimbus Rod sources of damage
- Mana cost increased from 10 to 30
- Pierce Count reduced from infinite to 5

Clinger Staff
- Duration increased to 5 minutes
- Now uses static frames, so immune frames will no longer interfere with non-Clinger Staff sources of damage

Magical Harp
- Knockback increased from 0.25 to 2

Tome of Infinite Wisdom
- Damage increased from 32 to 36
- Tornado damage reduced from 2x base damage to 1.75x base damage

Wasp Gun
- Wasps move roughly 25% faster
- Wasps now inflict static immunity, meaning they will no longer interfere with other sources of piercing damage
- Now has a token knockback value, allowing access to better modifiers

Leaf Blower
- Mana Cost increased from 4 to 5, allowing access to better modifiers

Inferno Fork
- Damage increased from 65 to 70
- AoE damage now does 75% of the base damage instead of 65%
- Blast effect now lasts longer
- Knockback reduced from 8 to 5, to limit how far enemies are knocked out of the blast radius
- Now inflicts Hellfire instead of On Fire

Shadowbeam Staff
- Damage increased from 60 to 80

Spectre Staff
- Now uses static immune frames, so its immune frames will no longer conflict with other attacks

```


---

## 🤖 Assistant · 2026-08-09T11:40:54.858Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Continuing 3701-4100.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:40:54.861Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '3701,4100p' \"~/Library/Application Support/Steam/steamapps/common/Terraria/changelog.txt\"",
 "description": "Read official changelog lines 3701-4100"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:41:00.224Z

**📎 ToolResult**

```
Magnet Sphere
- Duration increased from 11 to 15 seconds
- Now bounces off of walls instead of the sphere vanishing

Rainbow Gun
- Duration increased from 20 to 40 seconds
- Now uses static immune frames, so its immune frames will no longer conflict with other attacks

Toxic Flask 
- Damage increased from 46 to 52
- Usetime increased from 28 to 45
- Flask projectile speed/distance increased from 9 to 14
- Received a visual overhaul to make the gas clouds more "gassy"
- Projectiles now linger substantially longer than before
- Projectiles no longer penetrate walls, but will now "spread out" around a region, slightly pushing away from each other to fill a small area of space. This results in a more concentrated area of gas clouds, with less wasted to being stuck in walls or the floor.

Heat Ray
- Damage increased from 80 to 90

Bat Scepter
- Bats now move roughly 30% faster when tracking a target (though they remain normal speed when not tracking)

Stellar Tune
- Knockback increased from 0 to 1.5, allowing access to better modifiers

Nightglow
- Projectiles that are not currently tracking a target linger roughly 50% longer before disappearing
- Projectiles will have their duration reset to full upon beginning to track a target

Bubble Gun
- Projectile speed/distance increased from 11 to 15
- The bubbles now last twice as long before popping, meaning that more bubbles reach their full range, and they linger longer before disappearing
- Mana cost increased from 4 to 5, allowing access to better modifiers

Razorblade Typhoon
- Damage reduced from 90 to 85
- Mana cost increased from 16 to 20
- Duration of projectiles reduced from 3 seconds to 2.5 seconds

Nebula Blaze
- Knockback increased from 0 to 3, allowing access to better modifiers

Lunar Flare
- Mana cost reduced from 13 to 9

Last Prism
- Now has a token knockback value, allowing access to better modifiers


G. Summoning Weapons
Leather Whip
- Knockback increased from 0.5 to 1
- Purchase value reduced from 15 Gold to 10 Gold

Snapthorn
- Damage increased from 18 to 19
- Knockback increased from 1 to 1.5
- Jungle's Fury (Snapthorn's Whip Speed buff) has been reduced from 20% to 12%
- Stinger crafting cost increased from 12 to 15, and Jungle Spore crafting cost increased from 3 to 12

Spinal Tap
- Damage reduced from 29 to 27

Firecracker
- Damage reduced from 40 to 37
- Now inflicts Hellfire instead of On Fire

Cool Whip
- Damage reduced from 50 to 45
- Now inflicts 6 Tag Damage
- Snowflake damage increased from 10 to 15, and now moves 50% faster
- Now inflicts Frostbite instead of Frostburn

Durendal
- Usetime reduced from 30 to 28
- Durendal's Blessing (Durendal's Whip Speed buff) has been reduced from 35% to 25%

Morning Star
- Usetime reduced from 45 to 35
- Tag damage increased from 5 to 8
- Minion critical bonus increased from 5 to 12
- Visual Change: Morning Star now has many more segments on its chain, which results in a much more visible white-grey swing profile. This will increase its visibility somewhat when swung in dark/night environments.

Dark Harvest 
- Usetime reduced from 30 to 27
- Harvest Time (Dark Harvest's Whip Speed buff) has been reduced from 50% to 35%
- Reaping, Dark Harvest's special tag debuff, will now proc damage on the affected target as well as nearby targets. This acts as an effective 10 tag damage.

Snapthorn, Durendal, and Dark Harvest
- Fixed an issue where Whip speed buffs from Whips would incorrectly apply the buff to Melee weapons. Their tooltips have been updated to emphasize this fix.

Blade Staff
- Now only gains 75% of the damage from whip tags, due to its high hit rate and armor piercing capabilities

Sanguine Staff
- Knockback reduced from 8 to 3
- Fixed a bug where Sanguine Bats could hit a single target more than one time if the player was very close to the target.

All Minion Staves
- Minion summoning staves are now auto-fire, but minions which bypassed their attack cooldown immediately upon summoning no longer do so

Optic Staff
- Retinamini's lasers no longer pierce. As a result, they are no longer impacted by immune frames.
- Retinamini damage increased from 24 to 26.
- Spazmatism damage reduced from 30 to 21.
- Spazmatism now has more flexible charging range when pursuing targets
- Twin minions now return to the player more quickly

Deadly Sphere
- Damage reduced from 50 to 40
- Now uses local immune frames. At higher Summon counts, the damage dealt by Deadly Spheres should be significantly higher
- Aggro range has been increased, so it will attempt to engage enemies from further distances. Additionally, improved how its "dash" movement is able to engage enemies at a distance.
- Fixed a bug that caused Deadly Spheres to spontaneously de-aggro from enemies in the middle of combat
- Sphere minions now return to the player more quickly

Pygmy Staff
- Pygmy damage increased from 34 to 40
- Pygmy spears are now a little bit faster
- Pygmies will now attempt to predictively aim at moving targets (though of course, enemies can change course)
- Pygmy spears now always inflict Venom, and no longer inflict Poison
- Pygmies now move faster when returning to the player

Desert Tiger 
- Now runs 25% faster when chasing enemies on foot

Raven Staff
- Ravens will now attempt to return to the player faster depending on how fast the player is moving

Tempest Staff
- Tempests will now continue to fire at enemies when returning to the player
- Tempests will now return to the player faster depending on how fast the player is moving
- Tempest Staff's tornados (not the shark projectiles) have been changed from using a global immunity system with 20 frames of immune time, to using static immunity with only 10 frames

Xeno Staff
- Fire rate reduced (33 to 36)
- UFOs no longer need to fully return to the player before they can teleport and re-engage with a new enemy
- UFOs will now attempt to return to the player faster depending on how fast the player is moving

All Sentries
- Whip tags and effects now apply to Sentry damage (the same way they apply to minions)
- The duration of all sentries has been increased from 2 to 10 minutes

Houndius Shootius
- Now has a short delay on firing after being summoned

Explosive Traps
- Now has a token knockback value, allowing access to better modifiers
- Now has a short delay on firing after being summoned

Flameburst Sentries
- Now inflicts Hellfire instead of On Fire (Only applies to the Cane and Sentry)
- Now has a short delay on firing after being summoned

Ballista Towers
- Damage increased from 27/67/140 to 30/74/156
- Attack delay reduced from 180 to 160
- Knockback increased from 4.5 to 4.7
- Now has a short delay on firing after being summoned

Lightning Aura
- Only gains 50% of the damage from whip tags, due to its high hit rate and armor piercing capabilities
- Now has a token knockback value, allowing access to better modifiers
- Staves now have a more informative tooltip explaining how their damage works (it basically ignores defense)

Frost Hydra Staff
- Projectile now inflicts Frostbite
- Projectile speed increased by 50%
- Now has a short delay on firing after being summoned

Rainbow Crystal Staff
- Projectiles now use static immune frames

Lunar Portal Staff
- Damage increased from 50 to 100.
- Cooldown between beams reduced from 90 to 30; this is fast enough to allow a second beam to begin while the first one is still active.
- Lasers swing faster and cover a wider arc


H. Armor
Snow Armor (Blue and Pink)
- Increased the defense of the pieces from 1/2/1 to 3/3/3, for a total of 9 defense
- Now has a set bonus which grants immunity to Chilled/Frozen. Note: you can mix and match Blue and Pink pieces and still get the set bonus.
- The effective drop rate for each piece has been increased from 1/150 to 1/30

Mining Set
- Mining Helmet defense increased from 1 to 2
- The Mining Set's 30% mining speed is now split evenly between the Mining Shirt, Mining Pants, and the set bonus, with each giving 10%.

Angler Set
- Tooltips now show how much fishing power they grant
- Now has a set bonus which reduces enemy spawn rates

Shadow Armor
- Set bonus reworked to provide a more flexible speed increase system, similar to Magiluminescence. Unlike Magiluminescence, this works while in the air.
- +7% Melee speed on each piece has been removed, and replaced with +5% universal Critical chance

Crimson Armor 
- Damage bonus on each piece increased from 2% to +3%

Obsidian Armor
- Whip range bonus reduced from 50% to 30%
- Whip Speed bonus reduced from 35% to 15%

Cobalt Armor
- Defense of Cobalt Hat increased from 2 to 3
- Defense of Cobalt Helmet increased from 12 to 14
- Defense of Cobalt Mask increased from 4 to 5
- Defense of Cobalt Breastplate increased from 8 to 10

Orichalcum Armor
- Orichalcum Boots now give an 8% damage bonus

Titanium Armor
- Shards can now only generate once every 10 ticks (1/6th of a second), for a maximum of 6 shards a second
- Titanium Armor no longer spawns shards from statue spawned enemies.

Hallowed Armor 
- Holy Protection buff no longer starts its cooldown immediately at the time the buff starts, but instead begins the 30 second cooldown when you activate the dodge. If you never use the dodge, you can re-activate it immediately after the buff expires.
- Previously, the Holy Protection buff was activated by attacking an enemy, but it only had a 25% chance to activate. This did not really have any true impact on its functionality at all except to make it slightly inconsistent, so this has been removed. The buff will now be activated 100% of the time as long as you are not on cooldown.

Chlorophyte Armor
- Leaf Crystal's projectile is now an instantaneous bolt of energy, dramatically reducing its likelihood of missing.
- Now has a distance limit for how far it will fire when triggered by hitting an NPC (previously it could be significantly off screen)

Tiki Armor
- Tiki Mask now gives 10% Whip Range
- Tiki Armor Set Bonus now gives an additional 20% Whip Range

Shroomite Armor
- Shroomite Helmet (the Rocket Helmet) now also applies its bonus to any Ranged projectile shooting weapon which is not otherwise included by the Gun or Bow helmets. This includes such weapons as Dart Guns, Flamethrowers, and Star Cannons. This category of weapons is being referred to as "Specialist" weapons.
- Fixed a tooltip display bug that caused any weapons buffed by Shroomite Headpieces to display their damage 1 higher than it should have been. This was purely a tooltip calculation issue, and no change has been made to the actual potency of Shroomite's damage bonus

Spectre Armor
- Spectre Hood's teammate healing range increased from 1200 to 3000. Furthermore, it is now a circular shape instead of a diamond, further increasing its effective coverage area.

Beetle Scale Armor
- Beetle's Might charges last about 33% longer, and it now takes slightly less time/damage to charge up to Beetle's Might Tier 3

Solar Armor 
- Solar Dash/Explosion damage now scales with melee damage bonus

Stardust Armor
- Stardust Helmet now gives +1 Sentry count
- Stardust Chestplate and Leggings now give +15% whip range each


I. Accessories, Mounts, Tools and Tiles
Frog Legs and all Tinkers
- Players can now stack any Frog Leg-derived tinker to gain additive benefits
- Jump Speed Bonus reduced from 48% to 32%
- Fall damage protection reduced roughly proportionally to the Jump Speed bonus

Squire's Shield and Apprentice's Scarf
- Dark Mages in Tier 1 and Tier 3 Old One's Army now drop Squire's Shield and Apprentices Scarf, allowing access to +Sentry accessories pre-Hardmode. The drop rate is 50% to drop one of them in Classic, and 100% in Expert/Master. These two items have been removed from the Ogre's drop pool.

Hive Pack 
- Now increases the firing rate of Hornet Summons by about 30%
- Increases the damage of Wasp Gun by from 31 to 36, and increases the defense penetration of wasps from 10 to 15

Magiluminescence
- All Mobility enhancing stat bonuses reduced by 25%.

Spore Sac
- Movement speed of the spores has been dramatically increased
- Range at which spores will begin chasing targets increased by 20%

Lucky Horseshoe and Fledgling Wings 
- Reverted the change that put Lucky Horseshoe in Gold Chests, and put them back into Sky Chests on worldgen
- Fledgling Wing has been removed as primary drop from Sky Chests, and has a 1/40 chance of being secondary loot
- Sky Crates have been updated to account for the above changes.

Leaf Wings
- Now sold by Witch Doctor after Plantera has been defeated, but otherwise under the same conditions.
- Wing Power has been increased to be the same as uncommon pre-Plantera Wings (Flame, Butterfly, Bee and Bat)
- Cost has been increased to 1.5 Platinum

Magic Quiver, Molten Quiver, and Stalker's Quiver
- Damage bonus is now additive with other ranged damage bonuses, instead of multiplicative. This will generally result in slightly lower overall damage, especially when you have high quantities of Ranged damage bonus.
- Projectile speed bonus now also increases speed gained from ammo. Previously, it only increased the bow's projectile speed value.

Philosopher's Stone and Charm of Myths
- Potion Sickness reduction is no longer "front-loaded" at the time of using the potion. Instead, the cooldown is dynamically updated whenever the accessory is equipped. Equipping it will reduce the remaining cooldown proportionally, and removing it will increase the remaining cooldown proportionally. As long as you are wearing it, your effective remaining cooldown is reduced. This means that it you wear it for half of a minute and then remove it, you will only reduce 7.5 seconds from the total cooldown instead of 15. It also means that if you forget to equip it when using a potion, you can still equip it after to reduce the remaining cooldown.

Volatile Gel
- Projectiles now fire farther and with a flatter arc
- Fire rate increased from every 50 frames to every 40 frames (1.2 per second -> 1.5 per second)

Soaring Insignia
- All Mobility enhancing stat bonuses reduced by 25%. The infinite flight has not been changed.

Magma Skull and Molten Skull Rose
- The recipe for both of these items now takes a Lava Charm instead of a Magma Stone
- Both of these accessories now give temporary Lava Immunity, instead of adding Hellfire to attacks

Hellfire Treads
- Is no longer crafted by combining Flame Waker and Lava Waders. Instead, is crafted from Flame Waker and Spectre Boots
- Loses its Lava Wading benefits, but now has Hermes Running and Rocket Booting
- Generates fire sparks on running and uses the classic flame Rocket Boot trail

Lava Waders
- Can now be crafted with a Molten Skull Rose and Water Walking Boots/Obsidian Water Walking Boots

Fairy Bell
- Fairy Light Pet movement speed increased from 3.5 to 6

Turtle Mount
- Speed increased by 150%
- Swim Speed increased by 66%
- Jump Height increased by 20%
- Now gives water breathing when underwater

Gelatinous Pillion
- Horizontal flight speed reduced by roughly 30%
- Walking speed reduced by roughly 10%

All Minecarts
- Minecarts now hit harder in higher difficulties, deal more knockback, and are generally better at hitting enemies without letting the player be hurt when colliding with enemies

Mech Cart
- Now has the same speed and stats as other minecarts, and does not generate lasers (This will be addressed by a new item, the Minecart Upgrade Kit)

Drill Mount
- Can now break walls with right click
- Dig speed is roughly 3x faster

Spectre Pickaxe
- Mining speed reduced from 10 to 8 

Drills
- All drills that already had no knockback now have a token amount of knockback to obtain better modifiers

The Grand Design
- Now takes the Mechanical Ruler in its recipe instead of the Ruler. This also means that having the Grand Design in the inventory enables the Laser Grid UI option.

Magic Conch and Demon Conch
- Their animation sequence is now as fast as Magic Mirror, instead of being slower

Bottomless Waterbucket/Super Absorbant Sponge
- Can now be obtained in pre-Hardmode from Angler Quests, as soon as you have completed 10 Quests.
- Bottomless Water Bucket specifically is a guaranteed drop at 25 Quests

Enchanted Sundial
- Now glows when it is charged
- Will instantly become charged if a natural Blood Moon or Eclipse begins
- Can now be triggered via wire

Pylons
- Increased the maximum range where Pylons are usable from (it should be impossible to be in range of opening a Pylon and not be able to teleport with it)
- You can now use Pylons during Moon Lord's summoning sequence

Snowball Launcher
- No longer requires ammo
- Firing cooldown reduced from 10 to 7 frames
- Better projectile range and arc

Star in a Bottle
- Star in a Bottle's mana regeneration bonus increased from 1 mana per second to 5 mana per second. Additionally, it now also reduces the cooldown before mana begins regenerating after using magic weapons slightly.

Class Buff Stations
- Sharpening Station, Crystal Ball, Ammo Box, and Bewitching Table now last until death/being canceled or quitting out, rather than having a time limit

Ammo Box
- Is now sold by the Arms Dealer in Hardmode. Is no longer sold by the Traveling Merchant.
- Cost reduced from 15 Gold to 10 Gold to match other buff stations

War Table
- Is now a buff station that grants a +1 Summon Sentry cap buff


J. Buffs, Debuffs, Food and Potions
Poison
- The version of Poison inflicted on enemies now does 6 DPS instead of 2. This does not impact the Player version of Poison.

On Fire! and Frostburn 
The majority of Hardmode obtained items which inflict On Fire! or Frostburn have been changed to inflict Hellfire and Frostbite respectively.
This applies to:
- Flamethrower
- Elf Melter
- Hel-Fire
- Inferno Fork (Both Bolt and Blast)
- Phantom Phoenix (only applies to the Phoenix Shot, as the converted arrows are the Flaming Arrow projectile type)
- Flameburst Cane and Flameburst Staff
- Butcher's Chainsaw Sparks
- Brand of the Inferno
- Amarok
- Flower of Frost
- Firecracker
- Cool Whip

Crate Potions
- Duration increased from 3 minutes to 4 minutes
- Potency of Crate fishing chance increased by 50% (This is an overall increase of 25% more crates when fishing with a Crate Potion active)

Warmth Potion 
- Now include contact damage protection against Ice Bat, Ice Tortoise, Ice Mimic, and Yeti

Calming Potion 
- Potency of spawn reduction effect increased by 33%
- Duration increased from 8 to 12 minutes

```


---

## 🤖 Assistant · 2026-08-09T11:41:02.934Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Continuing 4101-4368.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:41:02.937Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '4101,4368p' \"~/Library/Application Support/Steam/steamapps/common/Terraria/changelog.txt\"",
 "description": "Read official changelog lines 4101-4368"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:41:08.514Z

**📎 ToolResult**

```
Inferno Potion 
- Damage increased from 10 to 20
- Now inflicts Hellfire instead of On Fire

Luck Potions 
- Duration and potency thresholds of all Luck Potions increased from 3/5/10 to 5/10/15.

Spelunker Potions 
- Statues and Paintings now glow when this potion is active

Bottled Honey 
- In addition to healing, now also grants 15 seconds of the Honey buff

Strange Brew
- Now heals randomly between 70 and 120 health
- Potion Sickness is now variable, between 40 and 70 seconds
- May randomly give a period of damage invulnerability, with longer durations being possible rarely
- No longer heals mana at all

Froggle Bunwich 
- Duration reduced from 8 to 6 minutes (Tier 2)

Seafood Dinner 
- Reduced from Tier 3 with a 4 minute duration to Tier 2 with a 14 minute duration

Grub Soup 
- Duration increased from 10 to 14 minutes (Tier 2)

Potato Chips 
- Duration increased from 18 to 25 minutes (Tier 1)

Carton of Milk
- Duration increased from 15 to 20 minutes (Tier 1)

Hot Dog 
- Changed from Tier 2 with a 20 minute duration to Tier 3 with a 12 minute duration


K. Drop Rates, Obtainment Sources and Other Probabilities
Traveling Merchant Shop
- Now has an extra guaranteed item slot in his inventory in Hardmode. This slot can only contain items from the 4 less common item pools, with the most common items being excluded.
- Traveling Merchant now has an extra guaranteed item slot in his inventory at all times. This slot will ALWAYS contain a painting. Paintings have been removed from all of his other inventory slots, which will slightly increase the odds of obtaining the rest of his wares.
- Celestial Magnet and Ammo Box are no longer sold by Traveling Merchant.
- Pad Thai has been increased from Tier 1 to Tier 2, making it less common
- Pho has been increased from Tier 1 to Tier 3, making it less common
- Christmas paintings will now be sold any time after Frost Legion has been defeated, rather than only when Christmas season is active
- Both Zapinators have been reduced from Tier 5 to Tier 3, making them more common

Celestial Magnet
- Is now found in the primary random loot pool of Sky Chests and Sky Crates

Waldo Painting and other "Rare" Underground Cabin Paintings
- Increased frequency of Waldo spawning in worldgen dramatically, though it is still the rarest painting of its size group
- All other "extra rare" Underground Cabin Paintings (American Explosive, Rare Enchantment, etc) are now of equal rarity within their size group

Wooden Chest Primary Loot
- Throwing Daggers/Glowsticks no longer act as primary loot, changing the primary loot pool size from 12 to 10. These items are now secondary loot.
- Skeleton Merchant can now sell most of the remaining Wooden Chest primary loot on a rotating Moon Cycle schedule. Every day of the Lunar Cycle, he will have a new item.

Living Tree Chests 
- Odds of containing a minecart increased from 1/10 to 1/6. If it does contain one, it is still a 50/50 chance to be a Sunflower or Ladybug Minecart.

Mushroom Biome Chests
- Mushroom Chests are now guaranteed to have one of their exclusive drops, with the Shroom Minecart and Mushroom Vanity each having a 50% chance.

Treasure Magnet 
- Instead of being primary loot, is now a 1/5 chance secondary loot in Shadow Chests and Obsidian Lock Boxes

Demonic Hellcart
- Can now be found in Lava Crates as uncommon bonus loot

Shark Bait
- Instead of being primary loot, is now a 1/10 chance secondary loot in Water Chests and Ocean Crates

Tree Fruit 
- Chance for tree fruit when hitting a tree from increased from 1/15 to 1/12

Diving Helmet 
- Drop rate increased from 1/50 to 1/20

Pocket Mirror
- Drop rate increased from 1/100 to 1/40. Expert drop rates (which doubled the odds of getting Pocket Mirror) are increased from 1/50 to 1/20

Medusa Head 
- Drop rate increased from 1/50 to 1/25

Turtle Shells 
- Drop rate increased from 1/17 to 1/12

Brain Scrambler 
- Drop rate increased from 1/100 to 1/30

Deadly Sphere Staff 
- Drop rate increased from 1/40 to 1/30

Fire Feather 
- Drop rate increased from 1/75 to 1/50

Bone Feather 
- Drop rate increased from 1/450 to 1/300

Giant Harpy Feather
- Drop rate increased from 1/200 to 1/150

Tattered Bee Wing 
- Drop rate increased from 1/150 to 1/100

Obsidian Rose 
- Drop rate increased from 1/50 to 1/20

Frozen Turtle Shell
- Drop rate increased from 1/100 to 1/50

Ice Sickle
- Drop rate increased from 1/180 to 1/100

Monster Meat
- Drop rate reduced from 1/1000 to 1/1500. In Don't Starve seeds, changed from 1/200 to 1/500.

Flinx Fur
- Changed the drop rate of Flinx Fur, from 50% chance to drop 1-3, to 100% chance to drop 1-2 (a 50% overall increase). The Expert drop rate has changed from 90% to 100% to drop 1-3.

Eater of Worlds/Brain of Cthulhu
- Brain of Cthulhu's overall drop rate of Crimtane Ore and Tissue Samples in Expert/Master has been reduced significantly, as it was dropping almost twice as much as it should have been. It now drops roughly as much as Eater of Worlds drops.
- Restructured how Ore/Tissue Sample/Shadow Scale drops are handled in Expert and Master. Overall, the quantity of drops from Creepers/Segment kills has been reduced, while the amount of drops from Treasure Bags has been increased.
- In Expert mode, the total quantity of drops is split roughly evenly, with 50% of the Ore/Samples/Scales coming from the partial kills and 50% coming from Treasure Bags
- In Master mode, the total quantity of drops is weighted heavily toward the Treasure Bag, with only 25% of the rewards coming from partial kills, and 75% coming from the Treasure Bags
- Normal mode drop rates and weighting has been left entirely untouched by all of these changes.

Very Rare Pirate Drops 
- All of these have had their drop rates doubled outright. Their increased drop rate from Pirate Captains has also been doubled.
- Flying Dutchman now have a substantially increased chance of dropping these items, with a 1/15 chance to drop any of them except Coin Gun, which has a 1/50 chance

Golden Furniture
- Flying Dutchman is now guaranteed to drop 1 piece of Golden Furniture
- The stack size of dropped Golden Platforms has been increased as well

Reindeer Bells
- Drop rate from Ice Queens has been doubled

Lava Crates
- Lava Crates are now slightly less common (1/5 chance reduced to 1/6 chance). However, with the buff to Crate Potions, they will be roughly the same as before when using a Crate Potion.

Biome Crates
- When fishing in an area where Biome Crates can be caught, the game will now prioritize getting a Biome Crate instead of a Gold Crate, when in the (relatively rare) circumstance that you were eligible for both. Actual odds of getting either are unchanged by this.

Wooden Crates
- Drop rate for Wooden Chest primary loot increased from 1/45 to 1/20
- Umbrella replaced with Step Stool in the Wooden Chest loot pool

Fishing Crate Ore
- The drop rate of ore and ore bars from fishing crates has been reduced.
- Wooden Crates have roughly 40% less ore
- Iron and Biome Crates have roughly 30% less ore
- Gold Crates have roughly 20% less ore

Gold/Titanium Crates 
- Drop rate of Life Crystals increased from 1/15 to 1/8
- Drop rate of Enchanted Swords from Gold Crates increased from 1 in 50 to 30. In Titanium Crates, this drop rate has been further increased to 1 in 15.

Oasis/Mirage Crates 
- Now have a very rare chance to drop a Sandstorm in a Bottle as bonus loot

Pharoah Vanity Set 
- Pharaoh set is now less common from Pyramid Chests, increasing relative frequency of the other drops

Gold Worms 
- When used for fishing, has a particularly low chance of being consumed (only 1/20 chance)

Old One's Army Ogre Weapons
- Increased the odds that the Tier 2 Ogre will drop a weapon from 33% to 50%. In Expert/Master mode, this has been increased from 50% to 100%
- Tier 3 Ogres also have a higher chance of dropping a weapon, up from 1/6 to 1/4 chance.

Dev Armors from Treasure Bags
- Chance of getting a dev armor increased from 1/20 to 1/16

Frost Daggerfish 
- Maximum amount of Frost Daggerfish you can get per pull increased

Seahorses
- Can now spawn in a wider variety of Ocean shapes and conditions, which will result in more consistent spawning

Gem Bunnies and Squirrels
- Gem Critter spawns now have a rarity system based on their gem

Water Striders
- Spawn rate increased
- Increased the maximum level of windiness that will allow Water Striders to spawn from 10 MPH to 20 MPH

Butterfly Days
- Increased the odds of having a Butterfly day

Treasure Fairies
- Spawn rate reduced by 2/3rds in Hardmode

Truffle Worm and Prismatic Lacewing
- Spawn rates are now impacted by Luck

Jungle Critters
- Overall spawnrate of Jungle critters in Jungle towns reduced

Bloody Tears
- Brides and Grooms that spawn in Graveyards can now drop Bloody Tears even if it isn't a Blood Moon

Teleporters 
- Now sold by the Mechanic pre-Hardmode, instead of being sold by the Steampunker

Digging Mole Cart 
- Will now be sold by the Zoologist at 35% Bestiary completion instead of 60%

Bast Statue
- Can now generate as furniture in Underground Desert Cabins (in addition to being found in chests)


L. Recipes and Prices
- Crafting cost of Celestial Sigil reduced from 20 of each fragment to 12
- You can now craft Sandstorm and Blizzard in a Bottle using a Cloud in a Bottle + Frost Core/Forbidden Fragment at a Crystal Ball
- Molotov Cocktail now takes regular Gel instead of Pink Gel
- You can now use Vertebrae instead of Worm Teeth to craft Unholy Arrows
- Thorns Potions no longer require Worm Teeth or Stingers to craft
- Angel & Demon Wing Souls of Light/Night cost reduced from 25 to 15
- Empty Bucket Iron/Lead Bar cost reduced from 3 to 2
- Changed the recipes of all ore-based bricks to have a 1:5 crafting ratio (1 ore + 5 blocks = 5 bricks). Previously, they had a 1:1 ratio.
- Shroomite Plating's recipe changed from a 1:15 to a 1:25 crafting ratio, costing 1 Shroomite Bar for every 25 Shroomite Plating
- Pearlstone Brick's recipe changed to be consistent with Ebonstone Brick, using 2 Pearlstone Blocks instead of 1 Pearlstone Block and 1 Pearlsand
- Coral Torch's recipe now takes 3 Torches and gives 3 Coral Torches per Coral, instead of 1 Torch
- Chain's recipe now gives 15 Chain instead of 10
- Any 2 of Salamander/Shelly/Crawdad Trio's banners can be used to craft the banner of the missing member of the trio
- Wormhole Potion recipe now takes 3 Bottled Waters, and gives 3 Wormhole Potions
- The Tavernkeep now gives 10 Medals when initially spoken to, allowing players to purchase 2 Tier 1 staves instead of 1
- Tier 2 OOA Armor piece cost reduced from 25 to 15 Medals
- Tier 3 OOA Armor piece cost reduced from 75 to 50 Medals
- Tier 2 OOA Sentries cost reduced from 25 to 15 Medals
- Tier 3 OOA Sentries cost reduced from 100 to 60 Medals
- Defenders Forge cost reduced from 75 to 50 Medals
- Purchase cost of Pad Thai and Pho increased
- Reduced the sell values of Stained Glass types to more accurately reflect the cost of the specific gems used to make it
- Sailor Vanity, Eyepatch, Mummy Vanity, Pharaoh Vanity, Grinch Whistle, Mana Crystals, Ancient Manipulator, and Shell Piles all now have a sell value
- Reducing the sell value (and subsequently, the reforge cost) of a number of 1.4 tinkers and accessories which had higher than typical sell values
- Cost of Wallpapers reduced from 1 Silver to 75 Copper
- Cost of Clentaminator Solutions have been reduced from 25 Silver to 15 Silver
- Tax Collector can now hold up to a base 25 Gold instead of 10 (this can further be boosted by happiness)
- Sell value of Frogs reduced from 15 to 10 Silver. Their food recipe sell values have also been reduced proportionally.
- Angler Quests now give 2x as much money in Hardmode
- Research cost of Red Potion reduced from 10 to 3


M. Miscellaneous
- Summoning Moon Lord with Celestial Sigil will only have a 12 second summoning time instead of 60 second
- Old One's Army Banners now apply Banner buff to their respective enemies, though it is much weaker than the normal Banner buff
- Banners from particularly rare enemies may now drop at 10 or 25 kills instead of 50. This same value will apply to how many kills it takes to complete their Bestiary page.
- Wire in the Temple cannot be cut by the player until Golem is defeated
- The player cannot see wires within the Temple until Golem is defeated
- NPCs who die will now respawn freely, ignoring the original unique conditions which were required to spawn in the first place. For example, Party Girl will have "normal" respawn odds instead of her rare spawn chance, and NPCs with a required item like Arms Dealer and Demolitionist will no longer require a player to be holding that item to respawn.
- Life Crystals are now lower priority on the Metal Detector than Hardmode Ores
- Chlorophyte Ore infection protection is now slightly stronger. It can also purify a wider selection of infected tiles, such as Sand and Sandstone.
- Strange Plants now give 6x dye when turned in instead of 3x
- Slightly reduced the quantity of cracked bricks in the Dungeon
- Merchant and Skeletron Merchant now both sell "regular" Potions in Hardmode, in addition to their Lesser Potions.
- All Minecart Track items are now immune to lava destruction
- Chain tiles are now immune to lava destruction
- Stacks of Cloud blocks can now be found in Skyware Chests and Sky Crates
- When fishing in a Hallowed Oasis, you can now obtain both Hallowed or Oasis fish. This same rule does not apply to the more invasive Corruption/Crimson.
- Fairy Glowstick now has stronger light, closer to regular glowsticks
- Snake Coil grows substantially faster than before, and maximum height increased from 80 to 100 blocks
- Placing Sunflowers is now auto-swing

```


---

## 🤖 Assistant · 2026-08-09T11:41:12.802Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I've now read lines 2374-4368 of the changelog. Wait — the official said 2374-4368 covers 1.4.4 through 1.4.4.9 including 1.4.4.8.1. But my reading of 4101-4368 ends at "Placing Sunflowers is now auto-swing" — that seems to be the end of section M. But where are the hotfixes 1.4.4.1-1.4.4.9? Let me check what comes after line 4368. Actually the user said 2374-4368 covers 1.4.4 to 1.4.4.9. Let me verify by checking what's at the end and whether hotfix sections are within that range. Section M ends around line 4368. Hmm, but the user said the range includes 1.4.4.1~1.4.4.9. Let me check what's beyond 4368 to see the structure. Actually the user's claim may be wrong, or hotfixes might come before 1.4.4 (changelog is usually newest first). Let me check the surrounding lines to find where 1.4.4.1-1.4.4.9 hotfix sections are.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:41:12.803Z · glm-x-preview-260804

```
我已读完 2374-4368 全段。让我确认热修小节(1.4.4.1~1.4.4.9)在文件中的位置,以核对摘要的热修部分。
```


---

## 🤖 Assistant · 2026-08-09T11:41:13.399Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"^Version 1.4.4\" \"~/Library/Application Support/Steam/steamapps/common/Terraria/changelog.txt\" | head -30; echo \"---\"; sed -n '4360,4380p' \"~/Library/Application Support/Steam/steamapps/common/Terraria/changelog.txt\"",
 "description": "Locate hotfix section line numbers and check section end"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:41:18.557Z

**📎 ToolResult**

```
1951:Version 1.4.4.9 Changes -------------------------------------------------------------------------------------------
1995:Version 1.4.4.8.1 Changes -------------------------------------------------------------------------------------------
2004:Version 1.4.4.8 Changes -------------------------------------------------------------------------------------------
2169:Version 1.4.4.7 Changes -------------------------------------------------------------------------------------------
2182:Version 1.4.4.6 Changes -------------------------------------------------------------------------------------------
2236:Version 1.4.4.5 Changes -------------------------------------------------------------------------------------------
2264:Version 1.4.4.4 Changes -------------------------------------------------------------------------------------------
2287:Version 1.4.4.3 Changes -------------------------------------------------------------------------------------------
2320:Version 1.4.4.2 Changes -------------------------------------------------------------------------------------------
2343:Version 1.4.4.1 Changes -------------------------------------------------------------------------------------------
2374:Version 1.4.4 Changes -------------------------------------------------------------------------------------------
---
- Merchant and Skeletron Merchant now both sell "regular" Potions in Hardmode, in addition to their Lesser Potions.
- All Minecart Track items are now immune to lava destruction
- Chain tiles are now immune to lava destruction
- Stacks of Cloud blocks can now be found in Skyware Chests and Sky Crates
- When fishing in a Hallowed Oasis, you can now obtain both Hallowed or Oasis fish. This same rule does not apply to the more invasive Corruption/Crimson.
- Fairy Glowstick now has stronger light, closer to regular glowsticks
- Snake Coil grows substantially faster than before, and maximum height increased from 80 to 100 blocks
- Placing Sunflowers is now auto-swing

Version 1.4.3.6 Changes ------------------------------------------------------------------------------------------

I. Bug Fixes:
- Fixed numerous issues that caused the game to hang indefinitely when you quit it, on Mac & Linux.
- Fixed steam overlay issues on Linux.
- Updated FNA. (Mac/Linux related)


Version 1.4.3.5 Changes ------------------------------------------------------------------------------------------

I. Bug Fixes:
- Fixed certain inputs failing, acting weird, when using frameskip off setting

```


---

## 🤖 Assistant · 2026-08-09T11:41:24.679Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good — so the 1.4.4 main section is 2374-4368, and hotfixes 1.4.4.1-1.4.4.9 are lines 1951-2373. The user said the range 2374-4368 is "Version 1.4.4 到 1.4.4.9" — slightly misleading, but they gave the range explicitly so I read it all. The summary covers hotfixes too, so I should also verify the hotfix sections (1951-2373) against the summary's hotfix subsections. The user's main focus is the 1.4.4 main section (they said "官方 1.4.4 主段落约 2000 行,你要系统性扫完"). But the summary also has hotfix sections — a thorough check should include them since they're part of the comparison. Let me read 1951-2373 too.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:41:25.227Z · glm-x-preview-260804

```
主段落已扫完。摘要还包含热修小节,官方热修位于 1951-2373 行,我一并读取以便完整对比。
```


---

## 🤖 Assistant · 2026-08-09T11:41:25.230Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1951,2373p' \"~/Library/Application Support/Steam/steamapps/common/Terraria/changelog.txt\"",
 "description": "Read official hotfix sections lines 1951-2373"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:41:43.740Z

**📎 ToolResult**

```
<persisted-output>
Output too large (33.8KB). Full output saved to: ~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/e65c4575-731a-43e0-a377-ccf50cc42db3/tool-results/bumtd3049.txt

Preview (first 2KB):
Version 1.4.4.9 Changes -------------------------------------------------------------------------------------------

I. Changes:
- Updated localization of non-English languages to include all of the post-1.4.4 hotfix content and text adjustments & changes
- Recorded Music Boxes thrown into Shimmer will now be transmuted back into blank Music Boxes
- Updated over one hundred sprites to modernize some older and dated assets. 
- In tandem with the above, reset the scale stat on about 90 swords and tools back to 1. Over time and various updates, many of these weapons had their "scale" multiplier increased, a balancing stat that increases their size to give them a bigger hitbox. Unfortunately, this results in increasingly distorted and inconsistent pixel size across our weapons. All of the affected weapons/tools have had their sprite increased in size to reflect their actual in-game size, and then the scaling factor reduced back down to 1. This will result in both modernized versions of some old sprites, but less stretched, size appropriate weapon sprites to match their intended size. In practice, this will result in minimal actual impact on their in-game hitbox size, but when there is a change, it is almost always a difference of a pixel or two, and usually in favor of making the weapon slightly bigger.
- An important note for Resource Pack makers: any sprite replacements in resource packs for any of these updated Swords/Tools will no longer function, because the old sprites are not the same size as they are now. To update resource packs which change the appearance of these weapons, the replacement sprites will need to be resized to match the new expected sprite size.


II. Bug Fixes:
- Fixed further issues with loadouts not syncing their visuals in multiplayer to other players
- Fixed an issue where some settings would reset after updates/hotfixes, most notably, currently active Resource Packs
...
</persisted-output>

```


---

## 🤖 Assistant · 2026-08-09T11:41:46.492Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/e65c4575-731a-43e0-a377-ccf50cc42db3/tool-results/bumtd3049.txt"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:41:46.632Z

**📎 ToolResult**

```
1	Version 1.4.4.9 Changes -------------------------------------------------------------------------------------------
2	
3	I. Changes:
4	- Updated localization of non-English languages to include all of the post-1.4.4 hotfix content and text adjustments & changes
5	- Recorded Music Boxes thrown into Shimmer will now be transmuted back into blank Music Boxes
6	- Updated over one hundred sprites to modernize some older and dated assets. 
7	- In tandem with the above, reset the scale stat on about 90 swords and tools back to 1. Over time and various updates, many of these weapons had their "scale" multiplier increased, a balancing stat that increases their size to give them a bigger hitbox. Unfortunately, this results in increasingly distorted and inconsistent pixel size across our weapons. All of the affected weapons/tools have had their sprite increased in size to reflect their actual in-game size, and then the scaling factor reduced back down to 1. This will result in both modernized versions of some old sprites, but less stretched, size appropriate weapon sprites to match their intended size. In practice, this will result in minimal actual impact on their in-game hitbox size, but when there is a change, it is almost always a difference of a pixel or two, and usually in favor of making the weapon slightly bigger.
8	- An important note for Resource Pack makers: any sprite replacements in resource packs for any of these updated Swords/Tools will no longer function, because the old sprites are not the same size as they are now. To update resource packs which change the appearance of these weapons, the replacement sprites will need to be resized to match the new expected sprite size.
9	
10	
11	II. Bug Fixes:
12	- Fixed further issues with loadouts not syncing their visuals in multiplayer to other players
13	- Fixed an issue where some settings would reset after updates/hotfixes, most notably, currently active Resource Packs
14	- Fixed an issue where Echo Painted walls Underground would show up as solid black
15	- Fixed an issue where Paint Sprayer did not work in multiplayer on tiles that could fall
16	- Fixed Town NPCs not selling Ocean Pylons in valid Ocean Pylon regions on Remix/Everything seeds
17	- Fixed Truffle still selling Dark Blue Solution in Remix/Everything seeds
18	- Fixed Potion of Return's portal using the player's current height to determine its location, such as changing position when being on a mount or not
19	- Fixed an issue where Toxic Flask projectiles perceived platforms as solid blocks and would not pass through them
20	- Fixing a typo on Shroomite Helm tooltips that said they gave less damage than they did
21	- Fixed an issue where Shift-Clicking accessories into a Mannequin could result in invalid states such as having duplicate redundant accessories
22	- Fixed an issue where some Right-Click-to-Transform Items (Void Bag, Shellphone, etc) could result in sound effect spam playing rapidly for other players in multiplayer
23	- Fixed an issue where most worlds generated in or after 1.4.4.3 would not have Glow Tulips. Unfortunately, this will not retroactively generate Glow Tulips for those worlds
24	- Fixed an issue where info accessories stored in Open Void Bags did not apply their info benefit to nearby players in multiplayer
25	- Fixed an issue where the player preview draws behind the Dresser UI instead of infront of it
26	- Fixed a visual issue with the Witch's Broom mount's lantern when combined with certain armor effects
27	- Fixed an issue that prevented Shadow Scales and Tissue Samples from being swapped in the Chlorophyte Extractinator
28	- Fixed an issue where Flamewaker/Hellfire flame trail would be dyed by the dye on a different pair of boots in the accessory order
29	- Fixed an issue where inventory hotbar slots would highlight in gold when in the inventory incorrectly
30	- Fixed an issue that prevents the player from throwing items from inventory when using a Gamepad and autopaused
31	- Followup fix for a recurring issue that locks players into reusing an item repeatedly when on Gamepad
32	- Fixed an issue where some tile's glowing would not function properly when in a hammered state
33	- Fixed Aether effect not working in screenshots/snapshots taken in Camera mode
34	
35	
36	III. Balance:
37	- Scarecrows Banner/Bestiary Unlock Count Requirement reduced from 200 to 150 to reflect lower numbers in Pumpkin Moons
38	- All Scarecrow Bestiary Entries now share one kill count, rather than 10 independent kill counts, and will be unlocked simultaneously
39	- Morning Star damage reduced from 180 to 165
40	- Xeno Staff's fire rate further reduced from 36 to 40, in light of its AI changes resulting in much better performance than anticipated
41	- Made adjustments to the sell value of Bee Wax and Bee Wax-derived crafting items to result in a more consistent sell value across the set
42	- Increased the sell value of Imp Staff to match other Hellstone Bar gear
43	
44	
45	Version 1.4.4.8.1 Changes -------------------------------------------------------------------------------------------
46	
47	- Fixed an issue introduced in 1.4.4.8 that prevented Ocean Pylons from working on Remix/Everything worlds
48	- Fixed an issue introduced in 1.4.4.8 that prevented inventory management when using Guide/Goblin Tinkerer special menus
49	- Fixed a multiplayer issue where losing a sentry due to changing gear could remove someone else's sentry
50	- Fixed Bone Helm having an incorrect offset on the minimap in reverse gravity
51	- Adjusted Meat Grinder's tile position to be more evenly positioned and have less dead space
52	- North Pole base damage increased from 73 to 80 in light of the previous adjustments in 1.4.4.8
53	
54	Version 1.4.4.8 Changes -------------------------------------------------------------------------------------------
55	
56	I. Changes:
57	- Made some optimizations to Mac performance. We are interested in feedback on how successful this is, and if possible, will try to follow up on other areas that also need improvement. For the time being, the most notable examples to test out are on the player creation menu and around mannequins (especially with large numbers of mannequins), but other general performance improvements may be expected. Please let us know if there are any improvements or issues as a result of the optimizations!
58	- Biome Style buttons on the Camera Mode biome interface now have mouseover text showing what biome they represent
59	- Right clicking out of search bars in the Bestiary and Research menus will now also exit the search, just like Left Clicking previously did
60	- Lava Charm and Molten Charm now have vanity accessory visuals
61	- War Table Banners and Hanging Pots/Hanging Brazier can now be hung from platforms in both the up and down hammered position
62	- Adding flavor text to Bone Pickaxe
63	- Added a loading tip and Guide help text indicating the ability to assign/unassign NPC housing
64	- Reducing the duration that loading tips are present on screen during worldgen/load before scrolling to the next
65	- Gold Worms, when thrown into Shimmer in critter form, also turn into Gummy Worms, instead of Faelings, the same as if they were thrown in as an item
66	- Dropping a Sparkle Slime Balloon into Shimmer in item form will now also spawn Diva Slime, instead of it only working when you throw it as a projectile
67	- Pressure Plate Minecart Tracks are now shown with Dangersense Potion
68	- Hallowed and Ancient Hallowed Armor no longer transmute into each other in Shimmer. Instead, they decraft into Hallowed Bars
69	
70	
71	II. Bug Fixes:
72	- Fixed an issue that allows lava kills on Blue Slimes to count as valid for spawning King Slime in Remix/Everything seed. They will still count as valid, however, if the player hurts them first.
73	- Fixed Steam deck users being unable to use smart cursor when using precise aim methods (trackpad, attached mouse)
74	- Fixed a Dungeon issue where closet and hallways might sometimes cut-off the entrance from above it, resulting in being unable to progress. This should result in, at minumum, less examples of inaccessible Dungeons.
75	- Fixed a rare issue where the Temple door can rarely generate in a position that is entirely inaccessible from the entrance
76	- Fixed an issue causing Boulder Traps to generate over chests
77	- Fixed Royal Gel not working on Golden Slime
78	- Fixed an issue where Mannequins and Hatracks even remotely near the player would remove your bonus tile placement range from Accessories
79	- Fixed an issue where Snail-type critters ignored Shimmer entirely
80	- Re-fixed a change that prevented anti-gravity shifting from kicking you off of mounts when pressing Up
81	- Fixed Flask particles not appearing on whips
82	- Fixed an issue where Deadly Spheres could be put into tightly enclosed spaces to dramatically increase their DPS
83	- Partially fixed an issue preventing the Grappling Hook hotkey when using Grand Design/Portal Gun, but only when using a mouse for now
84	- Fixed an issue where Piranha Gun would sometimes recall all of the Piranhas if even one of them missed
85	- Fixed a number of minor issues with sprites such as the Hardcore Ghost, Chaos Elemental's Glowmask, Research Menu UI Slot, Iron Fence, and Shimmered+Transformed Zoologist
86	- Fixed some sprite issues that resulted in a number of Food item sprites being partially cut-off. While doing so, also made some fixes to a few Food items showing up on plates incorrectly
87	- Fixed Skyware Toilet's item not using the updated color scheme shown in the furniture tile
88	- Fixed a single 1-block layer in the underworld of the Remix/Everything seed that spawned the wrong enemies
89	- Fixed an issue where Town NPCs would rapidly teleport back and forth between housing locations
90	- Fixed Cascade dropping from some unintended enemies (like Old One's Army)
91	- Fixed Phasesabers and Orange Phaseblade not glowing like the other Phaseblades
92	- Fixed newer ambient critter sounds not scaling with the Ambient volume setting like other critters
93	- Fixed an issue where dispelling or overriding Abigail would delete any projectiles "owned" by the player, including other summon and their buffs
94	- Fixed the Skeleton Merchant showing up in the bestiary with out of date sprites. 
95	- Fixed an issue with the player's arm rotating the wrong way when in reverse gravity and swinging Shortswords or Starlight
96	- Fixed a multiplayer issue where Drill Mount's mining beams were not visible to other players when mining walls
97	- Fixed Sofas having a mouseover text that said "Benches". Chippy's Couch is also now properly labeled a Couch. This might end up in a Youtube video.
98	- Fixed an issue with Slimer's drops in the bestiary being listed unusually/duplicated
99	- Fixing grammatical issue with mana cost tooltips
100	- Fixed newest three workbenches not unlocking the Benched achievement
101	- Fixed Halloween Skeletons not counting towards Skeleton kills
102	- Fixed an issue with Sky Dragon's Fury and Ghastly Glaive relating to Shimmer and some odd projectile behavior
103	- Fixed an issue where Chlorophyte Armor's set bonus fire cooldown time was inadvertently reset when swapping between armor
104	- Fixed an issue where Fireblossom seeds wouldn't work properly with Smart Cursor with Ash Grass
105	- Fixed an issue where dead players would not show their vanity equipment on the player select menu
106	- Fixed an issue where Holy Protection would persist on the player after removing Hallowed Armor
107	- Fixed an issue where Fertilizer didn't work in the Underworld in Remix/Everything seeds
108	- Fixed a crash issue that could happen when editing a sign and quitting out of the game
109	- Fixed Wave 20 Pumpkin Moon's announcement text not including Headless Horsemen
110	- Fixed an issue where Gamepad placement range did not account for Builder Potion's bonus
111	- Fixed the cancel button when renaming chests overlapping with other UI buttons
112	- Fixed rope coils not extending rope when the rope in question intersected platforms/rails
113	- Fixed Red Pigrons dropping more money than other Pigrons for no apparent reason
114	- Fixed an issue where fishing very deep ponds would sometimes not allow fishing up anything at all
115	- Fixed an issue where Gamepad/Steamdeck controls would auto-craft an item when accessing the Guide or Tinkerer's special menus
116	- Fixed Truffle not being able to be assigned to underground mushroom biomes in Multiplayer
117	- Fixed the /alldeath commands giving an incorrect output when the player only had one death
118	- Fixed an issue where Ocean Pylons wouldn't work in some Ocean-areas in Remix/Everything seed
119	- Fixed an issue where Meowmere Minecart's trail behaved oddly with certain armor
120	- Fixed an issue where Grass Seeds were not properly supported by Smart Cursor and so behaved oddly
121	- Fixed an issue where Empress of Light could hit players during her invulnerable phase transitions
122	- Fixed Gemcorns not growing or being Smart Cursor placeable when near tall moss
123	- Fixed an inconsistency with music boxes and prefixes
124	- Fixed monoliths being able to have prefixes, due to being able to stack
125	- Fixed Dirt Bombs not replacing tiles such as tall grass
126	- Fixed Life Drain's projectile being named Soul Drain
127	- Fixed the Like A Boss achievement not working on some newer boss summoner items
128	- Fixed the Real Estate Agent achievement not requiring Tavernkeep
129	- Fixed an issue leading to town NPCs bouncing back and forth between different locations
130	- Fixed an issue with Shimmer status after using a Wormhole Potion to teleport
131	
132	
133	III. Balance:
134	
135	Swords with Range Boosting Auras (Excalibur, Horseman's Blade, etc)
136	- Swords with boosted range auras that hit enemies behind the player will now knock enemies away, rather than into the player
137	
138	Trimarang:
139	- Knockback increased from 3 to 4.5.
140	- Projectile speed and return speed (very) slightly increased. It is now faster than all of the boomerangs that go into it
141	- Usetime decreased from 22 to 20
142	
143	Starfury
144	- Base damage increased from 22 to 25
145	- Reduce projectile damage from 2x to 1.5x (from 44 to 37)
146	
147	Bee Keeper and Hive-Five
148	- Spawned bees can now crit based on Melee critical chance
149	
150	Night's Edge
151	- Damage reduced from 42 to 40
152	- Usetime increased from 21 to 25
153	- Reduce pierce count from 3 to 2. As the swing actually has 2 projectiles (each of which have their own pierce counter), this is a reduction from 6 to 4 maximum possible hits per swing
154	- Range of the extended portion of the swing has been slightly reduced
155	
156	Ice Sickle
157	- Projectile damage increased from 50% of base to 67%
158	- Pierce count on projectile increased from 3 to 4
159	
160	Death Sickle:
161	- Sickle projectiles changed to use static immune frames instead of global
162	
163	Terra Blade
164	- Reduced the benefits from Melee Speed stat bonuses by 25%
165	
166	North Pole
167	- Flakes that are very close to each other will now slightly push away from each other, resulting in flake spread when falling
168	
169	Undertaker
170	- Damage reduced from 22 to 19 (partially undoing the 1.4.4 buff)
171	
172	Phoenix Blaster
173	- Damage reduced from 33 to 30
174	- UseTime reduced from 17 to 14
175	
176	Aqua Scepter
177	- Piercing count reduced from unlimited to 5, like Golden Shower
178	
179	Snapthorn
180	- Poison duration reduced from 4 to 3 seconds
181	- Chance to inflict Poison reduced from 100% to 20%
182	- Correction: In 1.4.4, the changelog listed that Snapthorn's damage was increased from 18 to 19. This was in error. It remains at 18 damage.
183	
184	Houndious Shootius
185	- Increased hitbox size of the projectile
186	
187	Optic Staff
188	- Base damage increased from 21 to 24 (Spazmamini's damage is 100% of base damage)
189	- Retinamini's damage scaling reduced from 1.25x to 1.15x of base damage (still a slight increase due to the increased base)
190	
191	Frost Hydra
192	- Projectiles set changed to use static immune frames instead of global
193	
194	Magic Quiver
195	- Drop rate increased from 1/80 to 1/40
196	
197	War Table (and by default, War Banners)
198	- Increasing drop rate and splitting its drop chance away from War Banners
199	- T1 Dark Mage now has a 50% chance to drop each of them independently in Classic, and a 100% to drop each in Expert+. 
200	- T3 Dark Mage has a 1/8 chance to drop either independently in Classic, and a 1/4 chance in Expert+.
201	
202	Sleeping/Sitting in Chairs
203	- Dramatically reduced the health regen buff when sitting or sleeping
204	- Sleeping and Sitting are now interrupted by taking damage
205	
206	Mystic Frog:
207	- Spawn rate increased
208	- No longer despawns when attempting to catch it with a net; it instead teleports to a nearby onscreen location
209	- Bestiary entry changed to more subtly imply how to obtain it
210	
211	Remix World pre-Hardmode Mimics
212	- Health increased from 270 to 300
213	- Defense reduced from 16 to 12
214	
215	Remix World King Slime Spawns
216	- Put a stat progression check on King Slime spawns to prevent Day 1 spawns on unprepared players. Will be identical to Slime Rain conditions from normal worlds.
217	
218	
219	Version 1.4.4.7 Changes -------------------------------------------------------------------------------------------
220	
221	I. Bug Fixes:
222	
223	- Fixed an issue with day spontaneously setting itself to night
224	- Fixed an issue where Queen Bee and Golem would fail to spawn the first time every launch session, and possibly more often in multiplayer in some cases
225	- Fixed bestiary entries not updating their adjusted stats first for the purposes of sorting
226	- Fixed an issue where pressing UP/DOWN to toggle Rubblemaker tiles changing the selection of other players as well
227	- Fixed a worldgen issue where Dead Man's Chest minibiome traps could generate over other containers and break them
228	- Fixed an issue where King Slime could be summoned on Remix/Everything seeds by Slimes being killed in lava without player interaction. Hurting the slime first will still allow King Slime's spawn to happen if the lava delivers the killing blow, however.
229	- Fixed Slimers having an inadvertent double chance to drop Monster Meat
230	- Reverting a change in 1.4.4.6 relating to ipv6 IPs to resolve a bug; will be re-evaluated in a future hotfix
231	
232	Version 1.4.4.6 Changes -------------------------------------------------------------------------------------------
233	
234	I. Content Changes and Balance Changes
235	- The Angler's Accessory Drop Duplicate Protection has been adjusted to make it more flexible and player friendly. Instead of only selectively applying duplicate protection to the 2 triple sets of accessories independently, he now applies the duplicate protection to all 7 accessories, including the Fishing Bobber. If the player has any of the 7 accessories (either in their individual form or their tinkered forms, such as Shellphone) in their inventory, the Angler will always give a non-duplicate accessory whenever he rolls to drop an accessory at all. He will only begin dropping duplicates again once the player has all 7 in their inventory. This will also result in a general increase in the number of accessories he drops.
236	- As a follow-up change to the above, the Mermaid and Fish Costume have been moved to be before Accessories in priority order since Accessories will be more common.
237	- Pulling items out of stacks now speeds up faster after a few seconds to account for the larger stack size
238	- Adjusted some unintuitive spawning conditions with unsafe Dungeon and Underground Desert Backwalls, where they required a wall to be placed behind the block where the enemies would be spawning instead of just above it. This is no longer the case.
239	- It has come to our attention that the Goblin Summoner does not, in fact, drop any Summoner items. This is an unacceptable discrepancy, so the Goblin Summoner has been demoted to Goblin Warlock.
240	- Master For the Worthy and Everything Seeds now show their difficulty as "Legendary" on the main menu
241	- Stinkbugs are now more common on days where Stinkbugs can spawn
242	- Added recipes to craft Sandstone and Hardened Sand Blocks at a Solidifier
243	- Christmas and Halloween Slimes can now be transformed into the Squire Slime if no Blue Slimes are available due to seasonal spawns
244	- Sandstorm in a Bottle and Flying Carpet can now be transmuted into Pharaoh Vanities
245	- Lava Charm can now be transmuted into Magma Stone
246	- Increased the visibility of the Oiled debuff to make it more clear when it is active
247	- Silver and Tungsten Bullets will now give 1 ore when decrafted in Shimmer, instead of 1 bar
248	- Copper Shortsword, Copper Axe, and Copper Pickaxe will now give 1 Copper Ore and 1 Wood when decrafted in Shimmer (instead of not being decraftable at all)
249	- Reduced the sell value of the Glass Kiln
250	- Crispy Honey Blocks are now highlighted by Dangersense Potions on FTW Seeds
251	- Cacti are now highlighted by Dangersense Potions on Constant Seeds
252	- FTW Random Angel Statue replacement should no longer impact Dungeon Chests, including the HM Biome Chests
253	
254	II. Bug Fixes:
255	- Fixed an issue where Ice Golems, Angry Nimbi, and Rainbow Slimes wouldn't spawn reliably on Remix seed. They should now properly spawn during rain/blizzards.
256	- Fixed Molecart being able to dig through Demon Altars pre-Hardmode, and also being able to dig through chests with items in them
257	- Fixed an issue where Pumpkin Moon enemies were scaling way too much in multiplayer, including an entirely unintended damage scaling
258	- Fixed an issue where Frost Moon enemies were NOT scaling in multiplayer as intended (they should behave the same as the now fixed Pumpkin Moon scaling)
259	- Fixing (again) Brain of Cthulhu telefragging players
260	- Fixed the Guide to Peaceful Coexistence being flagged as a material when it was not a material
261	- Fixed an issue where ipv6 addresses were not functioning correctly for multiplayer servers
262	- NPCs or Critters spawned via spammable sources (by placing them, by statues, etc) are now flagged as such, and will be automatically replaced by regular spawns if they reach the spawn limit. This also applies to Queen Bee's Bees.
263	- Related fix to the above, the game will now spawn more faelings at once from critters dropped into Shimmer, as they will no longer interfere with natural spawns
264	- Fixed Hand of Creation having a lower rarity than Architekt Gizmo Pack
265	- Fixed several world name generator words that used an inconsistent apostrophe
266	- Revised a number of tooltips relating to Ammo and Mana Consumption to be more consistent
267	- Revised Celestial Shell accessory line's tooltips to be on more lines so that the text didn't scroll off the screen on small resolutions.
268	- Revised tooltips for a few other armor pieces to have more consistent order/phrasing
269	- Fixed some minor grammatical issues in some bestiary entries
270	(Note: Localization/tooltip adjustments in 1.4.4.5 and 1.4.4.6 are only to English at this time, and will be added in other languages in a subsequent hotfix)
271	- Fixed an issue causing players in Everything seed to get boosted boss death timers when in single player
272	- Fixed the Inner Tube being able to float in Honey, and it will now also work in Shimmer if you have the Chromatic Cloak equipped
273	- Fixed an issue where Gem Trees would not draw their foliage if there was no block below the block they grew out of
274	- Fixed Block Swapping Sand in the Celebration seed not painting it cyan
275	- Fixed an issue that would sometimes result in Underground Desert chests generating as the wrong type of chest, usually Gold Chests (and with the wrong type of loot)
276	- Fixed an issue where some equipment slots could have "nothing" right clicked into them
277	- Fixed Halloween and Christmas Bunnies not transforming into Faelings in Shimmer
278	- Fixed an issue where the Environmental Preservation Guide effect would prevent traps from breaking tiles
279	- Fixed an issue that prevented Deerclop's enemy slot count from properly reducing spawns like other enemies and bosses
280	- Fixed an issue where Horseman's Blade projectiles would sometimes decide to target critters, even though they aren't meant to target critters
281	- Fixed an issue with boss projectile NPCs being inconsistently killable in Single vs Multiplayer on FTW/Everything seeds
282	- Fixed an issue where Fertilizer wouldn't work on trees in certain Underground layers of Remix/Everything seed
283	- Fixed an inconsistency with the collision size of some dart trap darts
284	- Added a buffer zone to infection and grass spread outside the edge of the world to prevent scenarios where infection could reach places where it couldn't be purified 
285	
286	Version 1.4.4.5 Changes -------------------------------------------------------------------------------------------
287	
288	I. Additions/Changes:
289	- Guides to Critter Companionship, Environmental Preservation, and Peaceful Coexistence can now be toggled on and off via Right Click, either in the inventory or from hotbar
290	- All Torches are now transmuted in Shimmer to Aether Torches
291	- You can no longer obtain bones via Shimmer decrafting before Skeletron
292	- You can no longer obtain Lihzahrd Bricks via Shimmer decrafting before Golem
293	
294	II. Bug Fixes:
295	- Fixed an issue that caused Wall of Flesh's drops to sometimes vanish when the world was converted to Hardmode. Very rare outside of Remix/Everything worlds. 
296	- Adding a failsafe that will protect players who get stuck in an excessively long Shimmer state
297	- Fixed a potential softlock caused by Shimmer and bouncy blocks
298	- Fixed some issues with Golf and Drone cameras being stuck panning to the player too long
299	- Fixed Golden Toilets not facilitating proper Poo creation
300	- Fixed Shellphones being unable to be decrafted in Shimmer
301	- Fixed another exploitable item with Shimmer decrafting
302	- Fixed an issue with tile actuation protection extending too far below the tile
303	- Fixed an issue with Oceans being drained repeatedly during gameplay
304	- Fixed an extremely rare issue with the Jungle Temple not generating on Remix/Everything Seed
305	- Fixed an issue allowing enemies to spawn on safe Desert walls
306	- Fixed a minor sprite issue with Town Slimes
307	- Fixed a punctuation issue with Russian Hotdog tooltips
308	- Fixed an issue preventing the Escape key from functioning on menus
309	- Fixed explosives on FTW/Everything Seeds hitting multiple times
310	- Fixed Abigail's Flower not being able to grow on Mushroom or Ash Grass
311	- Fixed the Sickle not being able to get Hay from Ash Grass and Sea Oats 
312	- Fixed an issue with the delay on Darkness messages on the Constant seed not giving enough warning time
313	
314	Version 1.4.4.4 Changes -------------------------------------------------------------------------------------------
315	
316	I. Additions/Changes:
317	- Both tile and projectile versions of personal storage items now have the Quick Stack to Nearby Chests animation
318	- Changed Ghost Costume's Shirt so that you can see your worn pants beneath it. Using it with Familiar Legs will show the bare legs again.
319	- Floating container projectiles (Money Trough, Void Bag) now have an increased Quick Stack to Nearby Chests range just like chests do
320	- Reduced volume on the Kwad Racer Drone
321	- Shimmered debuff state no longer grants invincibility against bosses (invasion will be in a subsequent hotfix)
322	
323	II. Bug Fixes:
324	- Fixed a crash that happened to some players whenever the game tried to save
325	- Fixed an issue where NPCs who's names were translated would not drop name-based special drops
326	- Fixed some debug dust on Terra Blade
327	- Fixed issues where thunder/lightning became very fast when the game's time was sped up, resulting in FPS drops and potentially damaging flashing lights
328	- Fixed an issue where holding certain items inhibited the use of some hotkeys when it shouldn't have
329	- Fixed some inconsistencies with waterfalls in Retro/Trippy lighting
330	- Fixed a few more items being exploitable via Shimmer decrafting
331	- Fixed it being possible for Shimmer to spawn too high up in worldgen to properly form its visual effects
332	- Fixed an issue where it was possible to have an invalid loadout slot, breaking all loadout functionality
333	- Fixed an issue with loadout vanities in multiplayer not syncing to other players
334	- Fixed a visual issue with NPC arm sprites during combat animations when Shimmered
335	- Fixed a few minor tooltip and item name inconsistencies
336	
337	Version 1.4.4.3 Changes -------------------------------------------------------------------------------------------
338	
339	I. Bug Fixes:
340	- Fixed an issue preventing Quick Stack to Nearby Chests from working with some chests
341	- Fixed an issue where Favorited items in Void Bag would be placed into the player's inventory when Looting the Void Bag
342	- Fixed an issue when Clentaminator solutions would break trees and cause them to drop the wrong wood
343	- Fixed a typo in Ash Wood Breastplate's name
344	- Fixed Royal Gel not protecting against Shimmer Slimes
345	- Fixed an issue where Spear Range Boost Effects would have unreliable hit detection at high melee speeds
346	- Fixed Bottled Honey not giving the Honey buff when used with Quick Heal
347	- NPC Shops no longer update their discount price at all once the shop is open. Reenabled moving Greedy Ring/Discount Card in the accessory slots when the shop is open (since the price will no longer change dynamically)
348	- Fixed Enchanted Moondial not recharging when Blood Moon/Eclipse occur naturally
349	- Fixed an issue where Shimmered items that create Falling Stars would have the Falling Stars vanish instantly during day. Additionally, Falling Stars which are currently in the process of being "picked up" by a player will not vanish during day
350	- Fixed an issue where Pearlsand was not properly flagged as a Material for some crafting recipes which took any Sand
351	- Fixed Volcano's detonation sound playing for players very far away
352	- Fixed Don't Starve death sounds not playing on Constant Seeds
353	- Fixed an issue allowing you to switch loadouts while dead, frozen, webbed or stoned
354	- Fixed text issue with Fallen Starfish tooltip and Quest text giving the wrong location for fishing
355	- Fixed a worldgen issue that would allow thin ice chasms to override Chests
356	- Fixed the smart cursor outline of the Barrel not matching its shape
357	- Minor updates to other language localization
358	- Fixed a line of stray pixels on the Wand of Frosting sprite
359	- Fixed an issue with Spear Range Boost Effects looking odd on Minecarts in some scenarios
360	- Fixed Abigail's Flower being able to grow over and break a bunch of tiles it shouldn't be able to break
361	- Fixed Gamepad Fast Use causing some items to be used indefinitely
362	- Fixed Tortured Souls being able to pick up coins (who would want to give even MORE money to the tax man?)
363	
364	II. Balance
365	- A few items were set to be non-decraftable in Shimmer due to exploits
366	- Reduced the sell value of Light Disc, Bananarang, Fairy Boots, and Hellfire Treads to be more reasonable
367	- Fixed an issue with Sword Range Boost Effects not properly hitting behind the player, and generally improved their hit detection accuracy across the board
368	- Fixed Blade of Grass Razor Leaves not inflicting Poison
369	
370	Version 1.4.4.2 Changes -------------------------------------------------------------------------------------------
371	
372	I. Additions/Changes:
373	- Updating non-English localization files to account for some last minute changes and adjustments
374	
375	II. Bug Fixes:
376	- Fixed an issue introduced in 1.4.4.1 that prevented Mac/Linux from launching properly
377	- Fixed some additional Mac/Linux related launching and server issues
378	- Fixed an issue causing certain usable items to be duplicated on Gamepad/Console/Mobile/Steam Deck
379	- Fixed a Gamepad issue preventing items from being assigned to the D-Pad Hotbar properly
380	- Fixed a missing tooltip on Aether Campfire
381	- Fixed Lock Boxes not being openable with keys
382	- Fixed Solar Tablets not working in multiplayer but still consuming the tablet
383	- Fixed Pumps turning Lava and Honey into Water
384	- Fixed a softlock caused by leaving worlds in certain ways when using Drones or Golf
385	- Fixed Brain of Cthulhu teleporting too close to the player in FTW/Everything Seeds. It should no longer be able to directly telefrag the player, but the Brain is not avoiding you, so a rapidly moving player may still find themselves in its new teleport position.
386	- Fixed a visual issue caused by using some spears in reverse gravity
387	- Fixed some tile merging issues with dirt
388	- Fixed an issue causing some Clentaminator Solutions to consume far too much ammo per shot
389	- Fixed some Melee Speed tooltip inconsistencies on 2 items
390	- Fixed Smart Cursor trying to place Boulders on Pylons
391	
392	
393	Version 1.4.4.1 Changes -------------------------------------------------------------------------------------------
394	
395	I. Additions/Changes:
396	- Worlds where Moon Lord has been defeated now show a golden border on the world selection menu
397	- Added one new achievement
398	
399	II. Bug Fixes:
400	- Fixed some serverconfig options being completely ignored when running servers
401	- Fixed a major scaling issue with Journey mode universally having increased stats on enemies
402	- Fixed an issue causing players to infinitely use some items without being able to stop
403	- Fixed an issue where rescuing certain slimes as the 8th would not unlock The Great Slime Mitosis achievement
404	- Fixed character selection not properly applying dyes to players who had dyed pets
405	- Fixed a bug that gave an incorrect death message when killed by Jellyfish Shock Attacks
406	- Added a failsafe so that broken trees in worldgen will be fixed
407	- Fixed Paint Scraper not working with Smart Cursor when removing coatings
408	- Fixed some monoliths not properly being "pushed down" into the ground
409	- Fixed some liquid rendering issues when in reverse gravity
410	- Fixed the change to Chain's recipe from 10->15 not working. It should now properly give 15.
411	- Fixed an issue where Magic Quiver's knockback bonus rounded down, which actually nerfed most Knockback values
412	- Fixed an issue where Chains were lava immune, but could NOT be "extended" into lava
413	- Fixed hanging furniture swinging indoors with the wind
414	- Fixed an issue where Jungle critters could spawn in a Corrupt/Crimson Jungle when near Hive blocks
415	- Fixed an issue during worldgen where the game hangs indefinitely trying to spawn some objects
416	- Fixed an issue with Escape not working properly on the Virtual Keyboard
417	- Fixed an issue where the change Moon Lord's Phantasmal Sphere damage was only applied to one of the two versions
418	- Fixed a few bugs relating to new content that hasn't been spoiled yet
419	- Fixed an issue preventing 2 of the game title texts from showing, but they are still not properly translated in non-English languages for now
420	- Fixed an issue with lava spawns from tiles not spawning serverside in multiplayer, resulting in ghost lava
421	- Fixing a worldgen issue with trapped chests, which should alleviate at least one possible cause of worldgen freezing on the Everything seed
422	
423	
424	

```


---

## 🤖 Assistant · 2026-08-09T11:43:27.913Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have the full official text. Let me systematically compare with the summary.

Let me organize by official sections and check each entry against the summary.

**Section A. Special Seeds** — summary has Remix/No Traps/Everything, FTW (Classic→Expert, Expert→Master, bestiary 100%), Not the Bees (spider caves, all fish, bestiary), Don't Starve (darkness 250, 4s, mushrooms), Celebration. Summary covers all. ✓

**Section B. New Items and Content** — check items:
- 8 Slime Town Pets ✓
- 300+ items ✓
- 25+ blocks and walls ✓
- 55+ paintings ✓
- few new vanity accessories ✓
- new tree type ✓
- 3 furniture sets ✓
- Crimson and Corrupt Mud Grass ✓ — wait official says "Crimson and Corrupt Mud Grass" — hmm, actually official text: "Added Crimson and Corrupt Mud Grass. Corruption and Crimson no longer dry out Jungle Grass into dirt when corrupting it". Summary says "Crimson Jungle Grass 与 Corrupt Jungle Grass;腐化/血腥化丛林草不再退化为泥土". Close enough (official: Mud Grass; summary: Jungle Grass). Minor naming difference. Hmm — official calls it "Mud Grass" but the description mentions Jungle Grass drying out. zh wiki probably says 丛林草. Not a numeric conflict; skip or one-liner.
- Rubblemaker ✓
- Shellphone ✓
- Hand of Creation ✓
- Echo Coating/Illuminant Coating ✓
- Lilith's Necklace ✓
- Poo ✓
- Terraformer ✓
- Biome Sight Potion ✓
- Jungle Birds ✓
- Flymeal ✓
- few more pre-Hardmode weapons ✓
- Bottomless Honey Bucket and Honey Absorbent Sponge ✓
- Fart Kart ✓
- Resplendent Dessert ✓
- Pixel Boxes ✓
- Mini Star Cell Banner ✓
- Minecart Upgrade Kit — summary mentions under Mechanical Cart ✓ (via "Minecart Upgrade Kit" line 35)

Wait — summary doesn't mention Mechanical Cart change explicitly! Official section I (Accessories/Mounts/Tools/Tiles): "Mech Cart - Now has the same speed and stats as other minecarts, and does not generate lasers (This will be addressed by a new item, the Minecart Upgrade Kit)". Summary line 35: "Mechanical Cart 条目隐含新物品 Minecart Upgrade Kit(机械矿车升级包,承接原机械矿车激光效果)" — it says the entry implies the new item, but the summary misses the actual nerf: Mech Cart now has same speed/stats as other minecarts and doesn't generate lasers. That's a balance change (nerf to Mech Cart speed). The summary only mentions the upgrade kit. This is a partial omission — the Mech Cart stat normalization is missing. Worth listing.

**Section C. UI and Menu QoL** — check each:
- Loadouts F1-F3, F4 camera ✓ (line 413)
- any accessory in social slots ✓
- max stack 9999 ✓
- Guide Voodoo Dolls stack ✓
- Void Bag ✓ (comprehensive)
- Bestiary kill count ✓
- Bestiary stats based on session ✓
- accessibility option autofire ✓
- Painter two shops ✓
- link Angler quest fish in chat ✓
- Quest fish tooltips ✓
- Paintbrushes/Fishing Rods/Clentaminator show ammo ✓
- Clentaminator Rifle/Sniper Scope ✓
- Angler set/fishing accessories/potion indicate fishing power ✓
- +/- zoom 2x fast ✓
- outdated loading/Guide text ✓
- Journey mode research tooltip ✓
- info accessory tabs grayed out, gold critters ✓
- **Changed the Quest info for Pengfish and Pixiefish** — summary? I don't see it. Minor text change; count as small omission.
- Quick Stack visual effect ✓ (line 404 快速堆叠动画)
- Portal Gun flavor text ✓
- **Equipping any of the Monoliths in accessory slots will create a player-side shader effect** — summary? Line 407: "传送门枪风味文本与信息文本;演奏乐器时显示音符;配饰栏装备石碑(Monolith)仅自己可见效果" — yes ✓ ("配饰栏装备石碑仅自己可见效果" — that's the Monolith shader effect).
- musical instruments note ✓
- **Significantly increasing the range of quick stack to nearby chests** — summary line 416 mentions quick stack features in Void Bag, line 404 animation. But "increased range of quick stack to nearby chests" — summary doesn't explicitly mention. Check line 549: "漂浮容器弹幕(钱槽/Void Bag)拥有更远的快速堆叠范围" — that's the 1.4.4.4 change for floating containers. The main 1.4.4 change "significantly increased quick stack range" — I don't see in summary. Small omission (QoL).
- **Pumpkin and Frost Moon will now display the total score when the event is over** — summary? I don't see. Check Pumpkin Moon section (line 343-344) — no mention of score display. Small omission.
- **Flower Accessory's social display visual now draws over helmets/face accessories... Jungle Rose changed from Head Vanity to Vanity Accessory** — summary? Not present. Omission (vanity, minor).
- Worlds Moon Lord defeated special border ✓ (line 405)
- health/mana numbers option ✓
- boss health bar numbers ✓
- Weather Radio sandstorm ✓ (line 461)
- Character creation default Classic ✓
- Summon tooltips "Summon" ✓
- /death commands ✓
- tooltip Up/Down consistency ✓
- Capricorn ✓
- Shift-click research ✓
- randomize character hairstyles/female ✓
- Stylist haircuts at creation ✓
- disable quick trash option ✓
- Journey reach booster pickup range ✓ (line 429)
- Encumbering Stone ✓
- equipped pet on selection menu ✓
- Journey sliders buttons ✓

**Section D. Content Changes and Feature Expansions**:
- new achievements ✓ (1.4.4.1 mentions)
- new Death Messages — summary? Not explicitly. Minor.
- new title texts — not in summary. Minor.
- new words to random world name list — not in summary. Minor.
- new sounds to weapons/enemies ✓ (音频节)
- Ropes and Minecart tracks intersect ✓ (line 445)
- Ropes and Platforms intersect ✓
- no collide with platforms on rope pulley ✓ ("绳上滑动不与平台碰撞")
- Town pet exchange Pet License ✓ (line 459)
- Smashing altars no infection ✓ (line 383)
- Traveling Merchant extra slot Hardmode ✓ / extra painting slot ✓ (line 278)
- Angler no furniture drops ✓ (line 460)
- Right click Eternia Crystal Stand skip ✓ (line 350 "波间等待可右键水晶座跳过")
- 3 mechs → Plantera Bulb ✓
- Glowing Mushroom grass/trees glow different colors painted ✓ (line 403)
- Critter Cages stack ✓ (line 438)
- Underground Desert min size 50%→75% ✓
- double buffs/debuffs 44 ✓
- Torch God's Blessing convert Campfires ✓ (line 446)
- block swap torches and campfires ✓
- blockswap ropes out for platforms/tracks ✓
- Lockable Chests re-locked ✓
- Extractinator fishing trash → bait ✓ (line 442)
- golf hole in one ✓
- Slime Rain 6AM-Noon 4x ✓
- critters from tiles brief delay ✓
- tree hit visual puff ✓
- Banners/Hanging Bottles/Lanterns on unhammered platforms ✓
- Frozen Slime Blocks revert ✓
- Crystal Shards on Pearlsand ✓
- Rainbow Bricks map color ✓
- **Abigail's Flower now breaks in one hit when mined and makes a grassy sound** — summary? Not present (1.4.4.3 has Abigail fixes, but the 1-hit-break main change is missing). Minor omission.
- Zenith SFX ✓
- Rod of Discord sprite ✓
- Resprited core progression swords ✓
- Starfury star visual ✓
- fish partially submerged ✓
- Cracked Dungeon Bricks projectiles ✓
- recipes 9 safe dungeon walls ✓
- recipes dungeon worldgen platforms ✓
- Magic Mirror recipe ✓
- recipe checking optimized ✓
- Balla Hat/Gangsta Hat day/night ✓
- Ocean water transparent ✓
- Nurse comments on dying ✓
- Boss Masks + Beard ✓
- Hardcore Ghosts speed ✓
- Teleporters no flickering ✓

**Section II Bug fixes A-F** — the summary lists bug fixes selectively; task says count differences and list ≤5 most important. The summary's bug section covers most major ones. Let me check a few possibly missing important ones:
- "Fixed a crash caused by Lightning Aura Sentries dropping through the bottom of the world" — not in summary; minor.
- "Fixed Chain Knife and Flairon had a strange damage hitbox in the upper corner" — summary? Line 510 lists Terraprisma etc but not Chain Knife/Flairon hitbox. Minor.
- "Fixed Lavafly Jar not counting as a light source for housing" — not in summary. Minor.
- "Fixed NPCs standing in front of each other too often, and Town Pets standing over chairs and blocking Town NPCs" — not in summary. Minor.
- "Fixed an issue where sorting Chests..." minor.
- "Fixed player taking damage from Don't Starve darkness when in well lit areas due to being in another window" — summary? Not present. Minor.
- "Fixed Real Estate Agent achievement unlock on join" — not present; minor (1.4.4.8 mentions Real Estate Agent requiring Tavernkeep, summary covers that).
- Most bug fixes in summary look covered. I'll count: official has ~110 bug-fix bullets across A–F; summary lists maybe ~60 (concentrated). I'll estimate.

**Section III Balance**:

A. Global mechanics:
- Static immunity final hit ✓ (line 476)
- Buff caps 22→44, 5→20 ✓
- Post-death invincibility 1→3 ✓

B. Bosses:
- King Slime slots ✓
- BoC: 1000→1250 ✓; knockback 50/55/60→55/60/65 ✓; illusions ✓; safe range ✓; no map icon ✓
- Deerclops slots ✓
- WoF Hungry ✓; tongue pull ✓
- Queen Slime 15% ✓; 30/80/150→30/68/120 ✓; light ✓; slots ✓
- Plantera despawn ✓
- Golem 9000→15000, 16000→25000, 7000→10000 ✓; charge visual ✓; fists deflect ✓; slots ✓
- Duke 50000→60000, 1.6→1.65, 50k/60k/76.5k→60k/78k/99k ✓; invincible ✓; enraged ✓; Cthulhunado fix ✓
- Empress: teleport fix ✓; MANY slots ✓
- Daytime Empress/Skeletron/Prime/Dungeon Guardian dodge ✓
- Cultist 1.25→1.5, 32k/40k/51k→32k/48k/61k ✓; Ancient Light ✓
- Moon Lord Phantasmal Sphere -20% ✓, hitbox ✓, 2 non-identical weapons ✓

C. Enemies:
- Reflecting enemies half damage ✓
- Teleporting enemies ✓
- Lifeform Analyzer ✓
- Pumpkin/Frost Moon: all points covered ✓ (wave 20, rearranged, boss caps, slots, per-player scaling, trophies Frost Moon rates, boss drop-rate-by-wave reduced, expert drop bonus, Master 2.5x)
- Poltergeist ✓ (fly, 2000→1250, 8→10, banner)
- Splinterling ✓ (900→1200, banner, Spooky Wood)
- Hellhound ✓ (1200→1800, 4→5, banner)
- Headless Horseman ✓ (10000→5000, pumpkin projectile, 25→50, scaling)
- Mourning Wood ✓ (12000→14000, 28→34, slots, spooky wood)
- Pumpking ✓ (22000→26000, 36→40, slots)
- OOA: Lightning Bugs T3 Wave 6 ✓; Eternia Crystal 2x/3x ✓
- Martian Saucer core hitbox ✓
- Dreadnautilus ✓
- Blood Squid ✓
- Hemogoblin ✓
- Clowns ✓ (200→120, 160→120, glow, sound, KO Cannon 1/5, Bananarang 1/30→1/10, Bloody Tear 1/100→1/10)
- Antlion Larvae ✓ (4→2, 35→30, speed)
- Giant Antlion Chargers 22→16 ✓; Swarmers 18→12 ✓
- Tomb Crawlers ✓ (16→12, 20→14); spawn rates ✓
- Rolling Cacti 90→70 ✓
- Jellyfish electric shock ✓
- Snow Flinx ✓
- Lost Girl ✓ (1/200→1/80, 5→2 gold)
- Bone Serpents ✓ (30/15/10→36/20/16, 10/12→12/18, 250→300, speed, FTW)
- Rune Wizard 1/300→1/200 ✓
- Rock Golems ✓ (rocks, spawn, 5→2.5, head drops 2x)
- Giant Fungi Bulbs ✓
- Gastropods ✓
- Cursed Hammer/Crimson Axe ✓
- Desert Spirits ✓
- Jungle Creeper 40→28 ✓
- Moss Hornets Stingers ✓
- Necromancers/Ragged Casters ✓
- Celestial Pillars ✓ (100, 50 after ML)
- Solar Crawltipede ✓ (150→120, 100→80)
- Solar Corites ✓
- Nebula Floaters ✓ (0.5s, 1/4→1/6, 2→3, doubled)
- Nebula Predictors 2→3 ✓
- Brain Sucklers -40% ✓
- Vortex Alien Queens ✓; Larvae cap ✓
- Vortex Portals ✓
- Storm Diver ✓
- Stargazers ✓
- Large Stardust Cells ✓; Milkyway Weavers ✓

D. Melee:
- All broadswords local iframes ✓
- All flails 25%→35%, 3→4/sec ✓
- Metal broadswords: check numbers:
  - Copper 8→9, 23→21, 1→1.1 ✓
  - Tin 9→10, 22→20, 1→1.1 ✓
  - Iron 10→12, 22→20, 1→1.15, 5→5.5 ✓
  - Lead 11→13, 21→20, 1→1.15, 5→5.5 ✓
  - Silver 11→14, 21→20, 1→1.2, 5→6 ✓
  - Tungsten 12→14, 20→19, 1.025→1.2, 5→6 ✓
  - Gold 13→15, 20→18, 1.05→1.25, 5→6.5 ✓
  - Platinum 15→16, 19→17, 1.075→1.25, 5→6.5 ✓
  Summary says "7 种金属阔剑" but lists 8 (Copper, Tin, Iron, Lead, Silver, Tungsten, Gold, Platinum)! Official lists 8 (Copper, Tin, Iron, Lead, Silver, Tungsten, Gold, Platinum). So summary count "7 种" is wrong — should be 8. That's a minor numeric/count discrepancy. Worth noting.
- Cactus 8→10, 32→30 ✓
- Wooden 25→20, 0.95→1.0, 4→5 ✓
- Boreal 23→20, 5→6 ✓
- Palm/Mahogany 23→19, 5→6 ✓
- Ebonwood/Shadewood 10→11, 21→19, 5→6 ✓
- Wooden Boomerang 8→10, 16→20 ✓
- Enchanted Boomerang 13→17, 15→20 ✓
- Zombie Arm ✓
- Bone Sword ✓
- Bat Bat 31→36 ✓
- Shroomerang ✓ (14→23, 15→20, 1/100→1/40)
- Ice Boomerang ✓ (16→21, Frostburn chance, 15→20)
- Gladius ✓ (0.5→3, 1/40→1/20)
- Purple Clubberfish ✓ (24→35, 7→8)
- Tentacle Spike ✓ (19→20, 23→21)
- Falcon Blade 1.05→1.175 ✓
- Mandible Blade ✓ (14→16, 1→1.1)
- Storm Spear ✓ (12→14, 1.25→1.5)
- Trident underwater light ✓
- Katana ✓
- Candy Cane Sword: official 16→19 AND usetime 27→25. Summary only says "Candy Cane Sword(16→19)" — misses 27→25. Minor numeric omission.
- Fruitcake Chakram 14→19 ✓
- Bladed Glove 12→14 ✓
- Bloody Machete 15→20 ✓
- Light's Bane ✓
- Blood Butcherer ✓ (5 stacks, 4 each, 9 sec)
- Rotted Fork ✓
- Phaseblades 25→26, 25→18 ✓
- Starfury ✓
- Blade of Grass ✓ (28→18, 30→20, 3→4.5, 3 vines, 12→15 spores)
- Thorn Chakram 20%→50% ✓
- Bee Keeper 26→30 ✓
- Lucy ✓
- Muramasa ✓
- Valor 22→28 ✓
- Flamarang ✓ (32→49, 20%→50%, 15→20)
- Volcano ✓ (rename, AOE, 30→40)

Wait — official: "Usetime reduced from 30 to 40"? No — "Usetime reduced from 30 to 40" — that's weird wording, it says reduced but 30→40 is an increase. Official text: "Usetime reduced from 30 to 40". Hmm, that's what the official says (a typo in official, but the numbers are 30→40). Summary says "使用 30→40" ✓ — matches numbers.
- Night's Edge ✓
- Dark Lance ✓
- Breaker Blade ✓ (43→70, 29→35, 1.05→1.15, +100%→+150%)
- Cobalt Sword ✓ 39→40, 23→19, 1.1→1.2, 3.85→5
- Palladium ✓ 45→49, 25→22, 1.125→1.2, 4.75→5.5
- Mythril ✓ 49→50, 26→20 — official also has Size Scale 1.15x→1.2x; summary omits size for Mythril. Minor.
- Orichalcum ✓
- Adamantite ✓
- Titanium ✓
- Pearlwood ✓ (11→30, 21→15, autoswing)
- Cobalt Naginata 29→44 ✓ etc.
- Phasesabers ✓ (42→48, 20→16, 50→25)
- Cutlass ✓ (49→53, 17→16)
- Frostbrand ✓ (55→30 frames, Frostbite, 2→3, static)
- Ice Sickle ✓ (42→50, +50% range, 100%→50%, static, 5→3)
- Bladetongue ✓
- Slap Hand ✓ (35→55, 21→20)
- Hel-Fire ✓
- Amarok ✓
- Chain Guillotine ✓
- Bananarang ✓ (single, 55→45, sell price, 10% Clowns)
- Sergeant United Shield ✓ (0→2)
- Beam Sword ✓ (60→35, no chirp, autoswing, no useTurn, no forced turn)
- Excalibur ✓ (66→72)
- Gungnir ✓ (42→61)
- Light Disc ✓ (single, recipe x5, 57→60, 15→14, 5→6 discs, 13→16)
- True Night's Edge ✓ (105→70, 26→32)
- True Excalibur ✓ (70→72, 16→18)
- Brand of the Inferno ✓
- Chlorophyte Saber ✓ (42→28, no chirp, 100%→70%, 50% linger, static)
- Claymore/Partisan ✓
- Ghastly Glaive ✓
- Death Sickle ✓
- Butcher's Chainsaw ✓
- Terra Blade ✓ (115→85, 14→18, aura, slash)
- Scourge of the Corruptor ✓ (2.67→3, 2-4)
- Paladin's Hammer ✓
- Keybrand ✓ (85→105, 14%→17%, scaling)
- Horseman's Blade ✓ (75→150, 100% instead of 150%, statue)
- North Pole ✓ (25→30, half projectiles, base damage spear, 70% flakes vs 80%/63%, wind, lifetime)
- Christmas Tree Sword ✓ (75%→100%)
- Flairon ✓ (33% longer, 30% lock range)
- Starlight ✓
- Influx Waver ✓ (110→100)
- Flying Dragon ✓ (25→20, no LoS penalty)
- Star Wrath ✓ (110→170, 2x→1x, local)
- Meowmere ✓ (16→14, 1.25x, local)
- Terrarian ✓
- Jousting Lances ✓ (56→60, 78→90, 108→130)

E. Ranged:
- Flintlock ✓ (10→13, 0→1)
- Musket ✓ (36→32, no autofire)
- Undertaker ✓ (15→22, 23→20, 1→2)
- Blood Rain Bow ✓
- Harpoon ✓
- Spiky Balls ✓ (15→16, 6→7)
- Star Cannon ✓ (0→3)
- Bee's Knees ✓ (24→23)
- Quad-Barrel ✓ (17→14, 6→8)
- Handgun ✓ (17→26, 10→15)
- Phoenix Blaster ✓ (24→33, 11→17)
- Repeaters ✓ all six
- Marrow ✓ (50→53, autofire); Ice Bow ✓ (16→14)
- Hallowed Repeater ✓ (53→50, 16→17)
- Flamethrower ✓ (local, 15 defense, visuals, Hellfire) — summary ✓. Official also has "Pierce count increased from 3 to 4" for Flamethrower — check summary line 135: "Flamethrower:弹幕改局部无敌帧,伤害计算前无视 15 防御,视觉与碰撞箱重做,改 Hellfire" — missing pierce 3→4. Elf Melter line has 穿透 3→4. So Flamethrower pierce 3→4 missing. Minor numeric omission.
- Super Star Shooter ✓ (static, 50%→75%)
- Pulse Bow ✓ (85→80, 3 mechs)
- Phantom Phoenix ✓
- Venus Magnum ✓ (8→9, autofire)
- Rocket Launcher ✓ (45→55)
- Elf Melter ✓ (60→53, 6→5, local, 15 defense, 3→4 pierce, Frostbite, visuals)
- Electrosphere ✓
- Aerial Bane ✓
- Celebration MK2 ✓ (40→50, red missile fix)
- Archery Potion ✓ (1.2→1.1)
- Ichor/Cursed Darts ✓ (12→10, 10→9, fix)
- Exploding Bullets ✓
- Frostburn Arrows 9→7 ✓
- Holy Arrows 50%→33% ✓
- Cluster Rockets 33%→50% ✓

F. Magic:
- Mana regen ✓
- **Wand of Sparking: Average duration of On Fire slightly increased** — summary? Not present. Omission (minor buff).
- Amethyst Staff ✓ (3→5, 14→15, 40→37)
- Topaz ✓ (4→5, 15→16, 38→36)
- Sapphire ✓ (5→6, 17→18, autofire)
- Thunder Zapper ✓ (12→20, 5→7, 2→3)
- Crimson Rod ✓ (5 min, static, 10→30)
- Weather Pain ✓ (12→15, 20→25, +2s)
- Bee Gun token knockback ✓
- Magic Missile ✓ (27→35)
- Aqua Scepter ✓ (16→27, 5→7, 6→7, range)
- Flower of Fire ✓ (6→7.5, +1 bounce)
- Zapinators ✓ (37→36)
- Magic Dagger ✓ (40→35, autofire, local, +50%)
- Cursed Flames ✓ (50→55)
- Flower of Frost ✓ (7→9, Frostbite)
- Golden Shower ✓ (21→30)
- Blood Thorn ✓
- Meteor Staff ✓ (13→9)
- Frost Staff ✓ (16→12, Frostbite)
- Shadowflame Hex Doll ✓ (40→32, local, tendril)
- Spirit Flame ✓ (double AoE, +25%)
- Nimbus Rod ✓ (5 min, 36→30, static, 10→30, inf→5)
- Clinger Staff ✓ (5 min, static)
- Magical Harp ✓ (0.25→2)
- Tome of Infinite Wisdom ✓ (32→36, 2x→1.75x)
- Wasp Gun ✓ (25% faster, static, token)
- Leaf Blower ✓ (4→5)
- Inferno Fork ✓ (65→70, 75% vs 65%, longer, 8→5, Hellfire)
- Shadowbeam ✓ (60→80)
- Spectre Staff ✓ static
- Magnet Sphere ✓ (11→15, bounce)
- Rainbow Gun ✓ (20→40, static)
- Toxic Flask ✓ (46→52, 28→45, 9→14, visuals)
- Heat Ray ✓ (80→90)
- Bat Scepter ✓ (30% faster)
- Stellar Tune ✓ (0→1.5)
- Nightglow ✓
- Bubble Gun ✓ (11→15, 2x, 4→5)
- Razorblade Typhoon ✓ (90→85, 16→20, 3→2.5)
- Nebula Blaze ✓ (0→3)
- Lunar Flare ✓ (13→9)
- Last Prism token knockback ✓ (summary line 159 "Bee Gun/Wasp Gun/Last Prism:获得占位击退值" ✓)

G. Summoning:
- Leather Whip ✓ (0.5→1, 15→10 gold)
- Snapthorn ✓ (18→19 [with 1.4.4.8 erratum noted], 1→1.5, 20%→12%, 12→15 stinger, 3→12 spore)
- Spinal Tap ✓ (29→27)
- Firecracker ✓ (40→37, Hellfire)
- Cool Whip ✓ (50→45, 6 tag, 10→15 snowflake +50% speed, Frostbite)
- Durendal ✓ (30→28, 35%→25%)
- **Morning Star: Usetime reduced 45→35; Tag damage 5→8; Minion crit bonus 5→12; visual segments** — summary? Line 483 mentions "Morning Star 8" tag damage in the whip tag system section. But the full Morning Star entry (45→35 usetime, tag 5→8, minion crit 5→12) is NOT in the 召唤武器 section! Check summary lines 189-209... I don't see Morning Star entry. Line 483 in 机制系统 mentions "Morning Star 8" only as tag damage example. So Morning Star's balance entry (usetime 45→35, crit 5→12) is missing. Also 1.4.4.9 Morning Star 180→165 damage is present (line 596) ✓. This is a real omission — balance entry missing. Important since it's a Balance item.
- Dark Harvest ✓ (30→27, 50%→35%, Reaping 10)
- Snapthorn/Durendal/Dark Harvest fix ✓
- Blade Staff ✓ 75%
- Sanguine Staff ✓ (8→3, fix)
- All Minion Staves ✓
- Optic Staff ✓ (lasers no pierce, 24→26, 30→21, flexible charge, return)
- Deadly Sphere ✓ (50→40, local, aggro, dash, de-aggro fix, return)
- Pygmy ✓ (34→40, spears faster, predictive, Venom, return)
- Desert Tiger ✓ (+25% run)
- Raven ✓
- Tempest ✓
- Xeno ✓ (33→36, teleport, return)
- All Sentries ✓ (whip tags, 2→10 min)
- Houndius ✓ delay
- **Explosive Traps: token knockback + short delay** — summary line 205: "Houndius Shootius/Explosive Trap/Flameburst 哨兵:召唤后开火有短暂延迟" ✓ (delay covered; token knockback not mentioned — trivial)
- Flameburst ✓ (Hellfire for Cane and Sentry, delay)
- Ballista ✓ (27/67/140→30/74/156, 180→160, 4.5→4.7, delay)
- Lightning Aura ✓ (50%, token, tooltip)
- Frost Hydra ✓ (Frostbite, +50% speed, delay)
- Rainbow Crystal ✓ static
- Lunar Portal ✓ (50→100, 90→30, lasers faster/wider)

H. Armor:
- Snow ✓ (1/2/1→3/3/3, 9 total, Chilled/Frozen, mix sets, 1/150→1/30)
- Mining ✓
- Angler ✓
- Shadow ✓
- Crimson ✓ (2%→3%)
- Obsidian ✓ (50%→30%, 35%→15%)
- Cobalt ✓ (2→3, 12→14, 4→5, 8→10)
- Orichalcum Boots 8% ✓
- Titanium ✓ (10 ticks, 6/sec, statue)
- Hallowed ✓ (30 sec cooldown on dodge, 25% removed)
- Chlorophyte ✓
- Tiki ✓
- Shroomite ✓ (specialist, tooltip fix)
- Spectre ✓ (1200→3000, circular)
- Beetle ✓ (33% longer, Tier 3)
- Solar ✓
- Stardust ✓ (+1 sentry, +15% each)

I. Accessories/Mounts/Tools/Tiles:
- Frog Legs ✓ (48%→32%, fall)
- Squire's Shield/Apprentice's Scarf ✓ (T1/T3 Dark Mages, 50%/100%, removed from Ogre)
- Hive Pack ✓ (30% firing, 31→36, 10→15)
- Magiluminescence ✓ (-25%)
- Spore Sac ✓
- Lucky Horseshoe/Fledgling ✓ (Sky Chests, 1/40 secondary, Sky Crates)
- Leaf Wings ✓ (Plantera, uncommon wings, 1.5 plat)
- Magic Quiver ✓ (additive, ammo speed)
- Philosopher's Stone ✓ (dynamic; summary says "穿戴半分钟再卸下仅减 10 秒而非 15 秒" — official says "you will only reduce 7.5 seconds from the total cooldown instead of 15". NUMERIC CONFLICT! Official: 7.5 seconds; summary: 10 seconds. Let me double check official text: "This means that it you wear it for half of a minute and then remove it, you will only reduce 7.5 seconds from the total cooldown instead of 15." Yes 7.5. Summary says 10 秒. That's a numeric discrepancy!
- Volatile Gel ✓ (farther/flatter, 50→40 frames, 1.2→1.5/sec)
- Soaring Insignia ✓
- Magma Skull/Molten Skull Rose ✓ (Lava Charm recipe, temp lava immunity)
- Hellfire Treads ✓ (Spectre Boots, loses lava wading, Hermes+Rocket, sparks)
- Lava Waders ✓ (Molten Skull Rose + Water Walking Boots)
- Fairy Bell ✓ (3.5→6)
- Turtle Mount ✓ (150%, 66%, 20%, breathing)
- Gelatinous Pillion ✓ (-30%, -10%)
- All Minecarts ✓ (harder, knockback)
- **Mech Cart — same speed/stats as other minecarts, no lasers** — summary missing the nerf (only mentions upgrade kit). OMISSION (balance).
- Drill Mount ✓ (right click walls, 3x)
- Spectre Pickaxe ✓ (10→8)
- Drills token knockback ✓
- Grand Design ✓ (Mechanical Ruler, laser grid)
- Magic Conch/Demon Conch ✓
- BWB/Sponge ✓ (10 quests, BWB 25)
- Enchanted Sundial ✓ (glow, blood moon/eclipse, wire)
- Pylons ✓ (range, Moon Lord)
- Snowball Launcher ✓ (no ammo, 10→7, range)
- Star in a Bottle ✓ (1→5 mana/sec, cooldown)
- Class Buff Stations ✓
- Ammo Box ✓ (Arms Dealer, 15→10)
- War Table ✓ (+1 sentry buff station)

J. Buffs/Debuffs/Food/Potions:
- Poison 2→6 ✓
- Hellfire/Frostbite list ✓
- Crate Potions ✓ (3→4 min, 50% potency, 25% overall)
- Warmth ✓
- Calming ✓ (33%, 8→12)
- Inferno ✓ (10→20, Hellfire)
- Luck ✓ (3/5/10→5/10/15)
- Spelunker ✓ (statues, paintings)
- Bottled Honey ✓ (15s)
- Strange Brew ✓ (70-120, 40-70, invuln, no mana)
- Foods ✓ (Froggle 8→6 T2; Seafood T3 4min→T2 14min; Grub 10→14; Potato 18→25; Milk 15→20; Hotdog T2 20→T3 12)

K. Drop rates:
- Traveling Merchant ✓ (extra hardmode slot, painting slot, Celestial Magnet/Ammo Box removed, Pad Thai T1→T2, Pho T1→T3, Christmas paintings Frost Legion, Zapinators T5→T3)
- Celestial Magnet ✓ (Sky Chests primary)
- Waldo ✓
- Wooden Chest Primary Loot ✓ (12→10, Skeleton Merchant moon cycle)
- Living Tree Chests ✓ (1/10→1/6, 50/50)
- Mushroom Chests ✓
- Treasure Magnet ✓ (1/5 secondary Shadow Chests/Lock Boxes)
- Demonic Hellcart ✓ (Lava Crates uncommon)
- Shark Bait ✓ (1/10 secondary Water Chests/Ocean Crates)
- TreeFruit 1/15→1/12 ✓
- Diving Helmet 1/50→1/20 ✓
- Pocket Mirror ✓ (1/100→1/40, expert 1/50→1/20)
- Medusa Head ✓
- Turtle Shells ✓
- Brain Scrambler ✓
- Deadly Sphere Staff ✓
- Fire Feather ✓
- Bone Feather ✓
- Giant Harpy Feather ✓
- Tattered Bee Wing ✓
- Obsidian Rose ✓
- Frozen Turtle Shell ✓
- Ice Sickle ✓
- Monster Meat ✓ (1/1000→1/1500, DS 1/200→1/500)
- Flinx Fur ✓
- EoW/BoC ✓
- Pirate drops ✓ (doubled, Captain doubled, Dutchman 1/15, Coin Gun 1/50)
- Golden Furniture ✓ (guaranteed 1, platforms stack)
- Reindeer Bells ✓
- Lava Crates 1/5→1/6 ✓
- Biome Crates priority ✓
- Wooden Crates ✓ (1/45→1/20, Umbrella→Step Stool)
- Fishing Crate Ore ✓ (-40%, -30%, -20%)
- Gold/Titanium ✓ (1/15→1/8, 1/50→30, Titanium 1/15)
- Oasis/Mirage ✓
- Pharaoh ✓
- Gold Worms ✓ (1/20)
- OOA Ogre ✓ (33→50, 50→100, 1/6→1/4)
- Dev Armors ✓ (1/20→1/16)
- Frost Daggerfish ✓
- Seahorses ✓
- Gem Bunnies/Squirrels ✓
- Water Striders ✓ (+10→20 MPH)
- Butterfly Days ✓
- Treasure Fairies ✓ (-2/3)
- Truffle Worm/Prismatic Lacewing luck ✓
- Jungle Critters ✓
- Bloody Tears ✓ (Brides/Grooms graveyards)
- Teleporters ✓ (Mechanic)
- Digging Mole Cart ✓ (35%)
- Bast Statue ✓

L. Recipes/Prices: all seem covered:
- Celestial Sigil 20→12 ✓
- Sandstorm/Blizzard bottles ✓
- Molotov ✓
- Vertebrae ✓
- Thorns ✓
- Wings 25→15 ✓
- Empty Bucket 3→2 ✓
- ore bricks 1:5 ✓
- Shroomite Plating 1:15→1:25 ✓
- Pearlstone Brick ✓ (2 Pearlstone)
- Coral Torch ✓ (3 torches → 3 coral torches per coral) — summary: "每珊瑚产 3 个(原 1)" ✓ close enough
- Chain 15 ✓
- Trio banners ✓
- Wormhole 3 waters → 3 potions ✓
- Tavernkeep 10 medals ✓
- T2 armor 25→15 ✓, T3 75→50 ✓, T2 sentries 25→15 ✓, T3 sentries 100→60 ✓, Defenders Forge 75→50 ✓
- Pad Thai/Pho cost ✓
- Stained Glass ✓
- sell values added ✓
- reduced sell values tinkers ✓
- Wallpapers 1s→75c ✓
- Solutions 25s→15s ✓
- Tax Collector 10→25 ✓
- Frogs 15→10 ✓
- Angler 2x Hardmode ✓
- Red Potion 10→3 ✓

M. Miscellaneous:
- **Celestial Sigil summoning time 60s→12s** — summary? NOT present! Check... summary line 310: "Celestial Sigil:每类月亮碎片 20→12" (recipe). But the 12-second summoning time change is missing. That's an omission (gameplay-relevant!). Important.
- OOA Banners ✓
- Rare enemy banners 10/25 ✓
- Wire temple cut/see ✓ (line 451 "击败 Golem 前神庙内导线不可见/不可放置/不可剪除" ✓)
- NPC respawn ✓
- **Life Crystals lower priority on Metal Detector than Hardmode Ores** — summary? Not present. Omission (minor but gameplay).
- Chlorophyte Ore infection protection stronger + purify sand/sandstone ✓ (line 488 "氯光矿石净化能力增强(可净化沙块、砂岩等更多侵染图格)" ✓)
- Strange Plants 6x dye ✓
- Cracked bricks reduced ✓
- Merchant potions ✓
- Minecart Track lava immune ✓
- Chain lava immune ✓
- Cloud blocks Skyware ✓
- Hallowed Oasis fish ✓
- Fairy Glowstick ✓
- Snake Coil ✓ (80→100)
- Sunflowers autoswing ✓

Hotfixes 1.4.4.1–1.4.4.9 comparison (summary section 二):

1.4.4.9:
- localization update — summary doesn't mention (trivial)
- Music boxes ✓
- 100+ sprites ✓
- 90 swords scale reset ✓ (summary adds the ID table from zh wiki — that's the wiki supplement, fine)
- resource pack note ✓
- Bug fixes: summary lists loadouts sync ✓, settings reset? Summary line 597 lists many. Check: "Echo Coating 墙体在地下显示纯黑" ✓, paint sprayer ✓, Ocean Pylons ✓, Truffle ✓, Potion of Return ✓, Toxic Flask ✓, Shift-click mannequin ✓, right-click transform sounds ✓, Glow Tulips ✓, info accessories Void Bag ✓. Others minor (dresser UI, witch's broom, Shadow Scales Chlorophyte Extractinator — summary has "Shadow Scale/Tissue Sample 无法在叶绿提取机互转" ✓, Flamewaker dye, hotbar gold highlight, gamepad throw, item reuse, hammered glow, Aether screenshots). Fine.
- Balance: Scarecrow 200→150 ✓ shared kill count ✓, Morning Star 180→165 ✓, Xeno 36→40 ✓, Bee Wax ✓, Imp Staff ✓.

1.4.4.8.1: user said skip (known missing).

1.4.4.8:
- Mac performance ✓
- **Biome Style buttons mouseover text (Camera Mode)** — not in summary; trivial
- **Right clicking out of search bars (Bestiary/Research)** — not in summary; trivial
- Lava Charm vanity ✓ (line 590)
- War Table Banner/Hanging Pots hung from platforms ✓
- **Bone Pickaxe flavor text** — trivial
- **Loading tip NPC housing assign** — trivial
- **Reducing loading tip duration** — trivial
- Gold Worms → Gummy Worms ✓
- Sparkle Slime Balloon → Diva ✓
- Pressure Plate Tracks Dangersense ✓
- Hallowed/Ancient Hallowed decraft ✓
- Bug fixes — summary covers the gameplay ones. A few not: Phasesabers/Orange Phaseblade not glowing (minor), Halloween Skeletons not counting towards Skeleton kills (minor), rope coils not extending through platforms (minor, actually gameplay-ish), /alldeath one death output (trivial), Red Pigrons money (trivial), Life Drain named Soul Drain (trivial). Fine.
- Balance: aura swords knock away ✓, Trimarang ✓, Starfury ✓, Bee Keeper crits ✓, Night's Edge ✓, Ice Sickle ✓, Death Sickle ✓, Terra Blade melee speed ✓, North Pole flakes ✓, Undertaker ✓, Phoenix Blaster ✓, Aqua Scepter ✓, Snapthorn ✓, Houndius ✓, Optic ✓, Frost Hydra ✓, Magic Quiver 1/80→1/40 ✓, War Table ✓, Sleeping/Sitting ✓, Mystic Frog ✓, Remix Mimics ✓, Remix King Slime ✓.

1.4.4.7: all covered ✓ (day/night, Queen Bee/Golem spawn, bestiary sorting, Rubblemaker multiplayer, Dead Man's Chest, King Slime lava, Slimer Monster Meat, ipv6 revert).

1.4.4.6: covered — Angler duplicate protection ✓, Mermaid/Fish priority ✓, pulling items speed ✓, backwall spawn ✓, Goblin Warlock ✓, Legendary difficulty ✓, Stinkbugs ✓, Solidifier recipes ✓, Christmas/Halloween slimes Squire ✓, Sandstorm/Flying Carpet transmute ✓, Lava Charm→Magma Stone ✓, Oiled ✓, Silver/Tungsten bullets ✓, copper tools ✓, Glass Kiln ✓, Crispy Honey ✓, Cacti ✓, FTW angel statue ✓. Bug fixes covered. One note: "Fixed an issue causing players in Everything seed to get boosted boss death timers when in single player" — not in summary; minor.

1.4.4.5: covered ✓ (Guides toggle, torches→Aether, bones/Lihzahrd gating, WoF drops, failsafe, softlock, golden toilets, Shellphone decraft, actuation, oceans drained, temple, safe desert walls, explosives FTW, Abigail, sickle, darkness).

1.4.4.4: covered ✓ (tile/projectile storage quick stack, ghost shirt, floating containers range, Kwad volume, Shimmered no boss invincibility, save crash, translated names, Terra Blade dust, thunder, hotkeys, waterfalls, decraft exploits, shimmer spawn height, invalid loadout, vanity sync, NPC arms).

1.4.4.3: covered ✓ (quick stack chests, Void Bag favorites, Clentaminator trees, Royal Gel, spear range, Bottled Honey, shops discount, Moondial, falling stars, pearlsand, Volcano sound, DS death sounds, loadout switching, thin ice, barrel, Abigail, gamepad fast use, Tortured Soul). Balance ✓ (non-decraftable, sell values, sword range fix, Blade of Grass poison).

1.4.4.2: covered ✓ (Mac/Linux launch, duplication, D-Pad, Aether Campfire tooltip, Lock Boxes, Solar Tablets, Pumps, BoC FTW, spears reverse gravity, dirt merging, Clentaminator ammo, melee speed tooltips, boulder on pylons).

1.4.4.1: covered ✓ (golden border, achievement, serverconfig, Journey scaling, infinite use, Great Slime Mitosis, tree failsafe, Chain 15, Magic Quiver knockback, Chains lava, hanging furniture, jungle critters, worldgen hang, trapped chests, ghost lava, monolith pushed, liquid rendering).

Now compile findings.

**遗漏条目(官方有、摘要没有)** — prioritized:

Content/Additions & Balance:
1. Mech Cart 削弱:速度/属性与普通矿车相同,不再产生激光(由 Minecart Upgrade Kit 承接)→ 应归入【配饰、坐骑、工具、图格】(摘要只提了 Upgrade Kit,漏了机械矿车本身被削)
2. Morning Star(晨星锤鞭)完整平衡条目:使用 45→35、标记伤害 5→8、仆从暴击 5→12、视觉链段增加 → 应归入【召唤武器】(摘要仅在机制节提"Morning Star 8")
3. Celestial Sigil 召唤月总时间 60 秒→12 秒 → 应归入【配方与价格】或 Boss 节(摘要只记了碎片 20→12)
4. Wand of Sparking:On Fire 平均持续时间略增 → 【魔法武器】
5. Flamethrower 穿透 3→4 → 【远程武器】
6. Candy Cane Sword 使用 27→25(摘要只记伤害 16→19)→ 【近战武器】
7. Mythril Sword 尺寸 1.15→1.2(摘要漏)→ 【近战武器】
8. Life Crystals 在 Metal Detector 中优先级低于 Hardmode 矿石 → 【掉落几率与获取来源】或机制节
9. Abigail's Flower 一击挖断+草声 → 【UI/生活质量】或方块节
10. Pumpkin/Frost Moon 结束时显示总分 → 【UI/生活质量】
11. 显著增加快速堆叠至附近宝箱的范围 → 【UI/生活质量】
12. Flower Accessory 社交栏绘制在头盔之上;Jungle Rose 由头部虚荣改为虚荣配饰 → 【新增内容-物品/虚荣】
13. Pengfish/Pixiefish 任务信息一致性 → UI(小)
14. 新成就/新死亡信息/新标题文本/世界名随机词库扩充 → 【新增内容】(摘要仅在 1.4.4.1 提 1 个成就)

Bug fixes count difference: official ~110 bullets in sections II.A-F; summary gameplay-bug section lists ~45 condensed + more spread in hotfixes. I'll note the most important missing ones (≤5):
- Lightning Aura Sentry 坠出世界底部崩溃
- Chain Knife/Flairon 上角伤害判定异常
- Lavafly Jar 不算住房光源
- NPC 互相挡站位/城镇宠物占椅阻挡 NPC
- 切窗时 Constant 黑暗仍造成伤害
Also "sorting chest highlight", "Moon Lord health bar flicker", "Gravedigger Shovel 双配方改 AnyIron" (this one is gameplay-recipe: Gravedigger's Shovel now single AnyIron recipe — actually that's a recipe change, arguably belonging to 配方 section! Official lists under UI/Text fixes. Summary doesn't mention. Could note.)

**数值矛盾**:
1. Philosopher's Stone:官方 7.5 秒 vs 摘要 10 秒(穿戴半分钟卸下的冷却缩减)
2. 金属阔剑数量:官方 8 把 vs 摘要"7 种"(但列了 8 把)— 措辞错误
3. Crimson/Corrupt "Mud Grass":官方写 Mud Grass,摘要写 Jungle Grass — 名称口径,不算数值。

Anything else numeric? Let me double-check a few summary numbers against official:
- Candy Cane: official 16→19 + usetime 27→25. Summary 16→19 only. Omission not conflict.
- Ice Boomerang useTime 15→20 ✓.
- Quad-Barrel 17→14, 6→8 ✓.
- Snapthorn erratum handled ✓.
- Optic Staff 1.4.4.8: base 21→24, Retinamini 1.25→1.15 ✓.
- Warmth potion ✓.
- North Pole 1.4.4.8.1: 73→80 — user said skip.
- Starfury 1.4.4.8: 22→25, 2x→1.5x (44→37) ✓.
- Terra Blade melee speed -25% ✓.
- Hallowed: 30s cooldown ✓.

Also check summary line 64: "Pearlwood(伤害 11→30、使用 21→15、可自动挥舞)" ✓.

Check summary line 63 lists 8 swords but says 7 — noted.

Check Boss "Queen Slime 弹幕 30/80/150→30/68/120" ✓.

Check "Titanium armor:碎片每 10 ticks 最多 1 个(上限 6/秒)" ✓.

Check Frost Moon master 2.5x ✓.

Check "Squire's Shield/Apprentice's Scarf:改由 T1/T3 Dark Mage 掉落" ✓.

Check Leaf Wings "售价 1.5 铂金" ✓.

Check summary line 213 Snow armor "1/2/1→3/3/3(共 9)" ✓.

Check "Mechanical Cart 条目隐含新物品" — noted as omission of the nerf.

Check Pylons ✓.

Check Star in a Bottle 1→5 ✓.

Check recipe ratios ✓.

Check "税官存钱上限 10→25 金" ✓.

So numeric conflicts: really only the 7.5 vs 10 seconds one, plus the "7 种/8 把" count. Both worth reporting.

**Summary has but official doesn't**: mostly zh wiki supplements — e.g., 1.4.4.9 的完整 Item ID 尺寸对照表, Hive-Five 蜜蜂暴击(official says "Bee Keeper and Hive-Five" — actually official mentions Hive-Five ✓), Jellyfish weapon list details, 大量 (→ 文件) 标注, 规模评估章节. Also summary's "Snapthorn 配方 Stinger 12→15、Jungle Spore 3→12" ✓ official. "Scarecrow 旗帜/图鉴需求 200→150" ✓. Fine — one line.

Now estimate completeness. Coverage is very high. Missing items: ~14 content/balance/QoL entries + 1 numeric conflict + Mech Cart nerf + Morning Star + Celestial Sigil summon time + Wand of Sparking. Out of ~600+ content/balance lines, missing ~15 substantive entries → ~97% for balance/content; bug fixes condensed but deliberately. Overall ~95%.

Let me verify a couple of uncertain greps in the summary to make sure I'm not falsely reporting omissions: search for "Celestial Sigil", "Morning Star", "Mech", "Wand of Sparking", "快速堆叠", "总分", "7 种".
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:43:27.920Z · glm-x-preview-260804

```
官方全段(2374-4368)及热修段(1951-2373)均已逐条扫完。最后核实几处疑似遗漏,确认摘要中确实没有对应内容。
```


---

## 🤖 Assistant · 2026-08-09T11:43:28.671Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries && for k in \"Celestial Sigil\" \"Morning Star\" \"Mechanical Cart\" \"Minecart Upgrade\" \"Wand of Sparking\" \"Metal Detector\" \"总分\" \"Abigail\" \"Jungle Rose\" \"Flower Accessory\" \"7.5\" \"10 秒而非\" \"Pengfish\" \"火花点燃\" \"Chain Knife\"; do echo \"== $k ==\"; grep -n \"$k\" summary-1.4.4.md || echo \"(无)\"; done",
 "description": "Grep summary for suspected omissions"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:43:33.354Z

**📎 ToolResult**

```
== Celestial Sigil ==
310:- Celestial Sigil:每类月亮碎片 20→12(→ Recipe.cs)
== Morning Star ==
483:- 鞭标记系统:标记伤害概念(Cool Whip 6、Morning Star 8、Dark Harvest Reaping 等效 10)、Blade Staff 75% 系数、Lightning Aura 50% 系数、哨兵同样适用鞭标记(→ Player.cs, Projectile.cs)
604:- 平衡:Scarecrow 旗帜/图鉴需求 200→150(对应南瓜月中较少数量),全部 Scarecrow 共享击杀计数并同时解锁;Morning Star 伤害 180→165;Xeno Staff 开火间隔 36→40(对应其 AI 改动后超预期表现);Bee Wax 及其制品售价一致性调整;Imp Staff 售价提高(匹配其它狱岩锭装备)(→ Item.cs, NPC.cs, ItemDropRules)
== Mechanical Cart ==
35:- Mechanical Cart 条目隐含新物品 Minecart Upgrade Kit(机械矿车升级包,承接原机械矿车激光效果)(→ Item.cs, Projectile.cs)
== Minecart Upgrade ==
35:- Mechanical Cart 条目隐含新物品 Minecart Upgrade Kit(机械矿车升级包,承接原机械矿车激光效果)(→ Item.cs, Projectile.cs)
== Wand of Sparking ==
(无)
== Metal Detector ==
(无)
== 总分 ==
(无)
== Abigail ==
545:- 修复:Abigail's Flower 在部分图格生长并破坏本不应破坏的图格;手柄"快速使用"导致物品无限使用;Tortured Soul 能捡钱(→ WorldGen.cs, NPC.cs, Main.cs)
559:- 修复:图格致动保护向下延伸过远、海洋游玩中被反复吸干、Remix/Everything 丛林神庙罕见不生成、安全沙漠墙处刷敌、FTW/Everything 爆炸物多次命中、Abigail's Flower 无法在蘑菇草/灰烬草生长、镰刀无法从灰烬草/海燕麦收干草、Constant 黑暗讯息预警不足(→ WorldGen.cs, NPC.cs, Projectile.cs, Player.cs)
591:- 修复(玩法类节选):地牢小房间隔断上方入口、蜥蜴门生成在不可达位置、圆石陷阱生成在宝箱上、Royal Gel 对 Golden Slime 无效、人体模型/帽架移除配饰放置距离、蜗牛生物无视微光、按上键反转重力不解除坐骑、鞭上药瓶微粒缺失、Deadly Sphere 窄封闭区 DPS 恶意利用、Grand Design/传送门枪阻断抓钩热键(仅鼠标)、食人鱼枪一发未命中即全部回收、Don't dig up 地狱 1 格厚层生成错误敌人、城镇 NPC 频繁往返传送、Cascade 意外由部分敌人掉落、解除/覆盖 Abigail 删除玩家"拥有"的其它仆从弹幕与 buff、反转重力下短剑/Starlight 手臂方向、多人钻头坐骑采矿光束不可见、Sky Dragon's Fury/Ghastly Glaive 与微光相关问题及弹幕异常、叶绿套开火冷却切甲被重置、Fireblossom Seeds+Smart Cursor 无法在灰烬草工作、Holy Protection 移除圣甲后残留、深池钓鱼钓不上任何东西、多人 Truffle 无法分配地下蘑菇住所、Don't dig up 海洋晶塔不生效、Meowmere 矿车轨迹与特定护甲异常、草籽 Smart Cursor 异常、光之女皇无敌阶段仍能伤害玩家、宝石果在高苔藓旁无法生长/放置、音乐盒与词缀不一致、石碑可堆叠导致可获词缀、泥土炸弹不替换高草等图格、Like A Boss 成就不适用于较新 Boss 召唤物、Real Estate Agent 成就不需要酒保、虫洞药水使用后的微光状态问题(→ 多文件)
== Jungle Rose ==
(无)
== Flower Accessory ==
(无)
== 7.5 ==
161:- Flower of Fire:弹速/距离 6→7.5,额外弹射 1 次(→ Item.cs)
333:- Duke Fishron:生命 50000→60000,专家/大师缩放 1.6→1.65,最终 50000/60000/76500→60000/78000/99000;召唤与变形时无敌;激怒后移动快得多、更频繁发射更快 Cthulhunado(→ NPC.cs, Projectile.cs)
== 10 秒而非 ==
241:- Philosopher's Stone/Charm of Myths:药水病冷却改为按装备时刻动态等比缩放(穿戴半分钟再卸下仅减 10 秒而非 15 秒)(→ Item.cs, Player.cs)
== Pengfish ==
(无)
== 火花点燃 ==
(无)
== Chain Knife ==
(无)

```


---

## 🤖 Assistant · 2026-08-09T11:43:45.695Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed. All the suspected omissions are real. Now compile the final report.

Summary of findings:

## 遗漏条目

**Balance/Content(重要)**:
1. Mech Cart 被削(速度/属性对齐普通矿车、不产激光)→ 配饰坐骑节
2. Morning Star 1.4.4 平衡条目(使用 45→35、标记 5→8、仆从暴击 5→12、链段视觉)→ 召唤武器节
3. Celestial Sigil 召唤月总时间 60s→12s → 配方/Boss 节
4. Wand of Sparking On Fire 时长略增 → 魔法武器节
5. Life Crystal 在 Metal Detector 优先级降于 Hardmode 矿石 → 掉落/机制节

**数值子项漏记(同一武器漏一条子数值)**:
6. Flamethrower 穿透 3→4(Elf Melter 记了,Flamethrower 漏)→ 远程节
7. Candy Cane Sword 使用 27→25(只记了伤害)→ 近战节
8. Mythril Sword 尺寸 1.15→1.2(其余 5 把都记了尺寸)→ 近战节
9. Explosive Trap 哨兵占位击退(可拿词缀)→ 召唤节(小)

**QoL/其他**:
10. 快速堆叠至附近宝箱的范围显著增加 → UI 节
11. 南瓜/霜月事件结束显示总分 → UI 节
12. Abigail's Flower 一击挖断+草声 → 方块/UI 节
13. Flower Accessory 社交栏绘制于头盔之上、Jungle Rose 改虚荣配饰 → 虚荣
14. Pengfish/Pixiefish 任务描述一致性 → UI(小)
15. 新成就/新死亡信息/新标题文本/随机世界名词库扩充 → 新增内容(1.4.4.1 成就已记,正文"D. Content Changes"的成就/死亡信息/标题/词库没记)
16. Gravedigger's Shovel 配方改为单一 AnyIron 配方(官方列在 UI/文本修复)→ 配方节

**纯 bug 修复数量差异**:官方 II.A-F 约 110 条;摘要按"影响玩法逻辑"筛选约 45 条。最重要的漏报 5 条以内:
- Lightning Aura Sentry 坠出世界底部导致崩溃
- Chain Knife/Flairon 玩家上角伤害判定异常
- Lavafly Jar 不计为住房光源
- NPC 频繁互相遮挡站位、城镇宠物站椅阻挡 NPC
- 切出窗口时 Constant 种子光照充足区域仍受黑暗伤害

热修 1.4.4.1~1.4.4.9(除 8.1 已知)核对:基本全覆盖,仅漏 trivial 项(1.4.4.8 相机生物群落样式按钮提示/搜索栏右键退出/加载提示时长、1.4.4.9 非英语本地化更新、1.4.4.6 Everything 单人 Boss 死亡计时器偏长)。不算问题。

## 数值矛盾
1. Philosopher's Stone:官方 7.5 秒 vs 摘要 10 秒
2. 金属阔剑:官方 8 把 vs 摘要写"7 种"(实际列了 8 把,仅计数措辞错)
3. (口径非数值)官方称新草为 "Crimson and Corrupt Mud Grass",摘要译作"血腥/腐化丛林草"——描述句一致,仅名称口径不同,一句带过。

## 结论
完整度粗估:内容/平衡条目约 97%(约 600 条中漏 15 条左右);含 bug 修复整体约 95%。需要小幅修订:补 5 条重要遗漏(Mech Cart 削弱、Morning Star、Celestial Sigil 召唤时间、Wand of Sparking、Metal Detector 优先级)、修 1 处数值(7.5 秒)、修"7 种"计数。1.4.4.8.1 已知缺失按计划补。
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:43:56.455Z · glm-x-preview-260804

```
校验完成。官方 1.4.4 主段落(2374-4368 行,约 1995 行)已全量逐条扫完,热修段(1951-2373 行)也一并核对(1.4.4.8.1 按约定跳过)。以下为结果。

## 遗漏条目(按官方章节分组,每条一行:官方原文要点 → 应归入摘要哪个小节)

**III. Balance(最重要,共 5 条)**
- I 章 Mech Cart:速度与属性对齐普通矿车、不再产生激光(仅由 Minecart Upgrade Kit 承接)→【配饰、坐骑、工具、图格】(摘要 line 35 只提了 Upgrade Kit,漏了机械矿车本身被削)
- G 章 Morning Star:使用 45→35、标记伤害 5→8、仆从暴击加成 5→12、链段视觉加多 →【召唤武器】(摘要仅在机制节 line 483 提"Morning Star 8"标记值,1.4.4 平衡条目整条缺失;1.4.4.9 的 180→165 已记)
- M 章 Celestial Sigil:召唤月总时间 60 秒→12 秒 →【配方与价格】或 Boss 节(摘要 line 310 只记了碎片 20→12)
- F 章 Wand of Sparking:On Fire 平均持续时间略增 →【魔法武器】
- M 章 Life Crystals:在 Metal Detector 中优先级降为低于 Hardmode 矿石 →【掉落几率与获取来源】或机制系统节

**III. Balance 同武器漏子数值(3 条)**
- E 章 Flamethrower:穿透 3→4(Elf Melter 的 3→4 记了,Flamethrower 漏)→【远程武器与弹药】
- D 章 Candy Cane Sword:使用 27→25(只记了伤害 16→19)→【近战武器】
- D 章 Mythril Sword:尺寸 1.15→1.2(其余 5 把 Hardmode 金属剑都记了尺寸)→【近战武器】

**I 章 Content / C 章 UI QoL(共 7 条)**
- 快速堆叠至附近宝箱的范围显著增加 →【UI与界面/生活质量】
- 南瓜月/霜月事件结束时显示总分 →【UI】(或南瓜月节)
- Abigail's Flower 一击挖断并发出草声 →【方块/UI 节】
- Flower Accessory 社交栏显示绘制于头盔/面部配饰之上;Jungle Rose 由头部虚荣改为虚荣配饰 →【新增内容-物品】
- Pengfish/Pixiefish 任务鱼描述一致性调整 →【UI】(小)
- D 章四条宏观新增:新成就、新死亡信息、新标题文本、随机世界名词库扩充 →【新增内容】(1.4.4.1 的 1 个成就已记,正文这四条没记)
- Gravedigger's Shovel 铁铅双配方合并为单一 AnyIron 配方(官方列在 UI/文本修复)→【配方与价格】

**II 章 Bug 修复数量差异**:官方 A-F 六节约 110 条;摘要按"影响玩法逻辑"筛选取舍合理,实收约 45 条。最重要的漏报 5 条以内:① Lightning Aura Sentry 坠出世界底部崩溃;② Chain Knife/Flairon 玩家上角伤害判定异常;③ Lavafly Jar 不计为住房光源;④ NPC 频繁互相遮挡站位、城镇宠物站椅阻挡 NPC;⑤ 切出窗口时 Constant 种子在光照充足区仍受黑暗伤害。

**热修小节**:1.4.4.1~1.4.4.9(除 8.1)逐条核对基本全覆盖,仅漏纯琐碎项(1.4.4.8 相机生物群落按钮提示、搜索栏右键退出、加载提示停留时长、Bone Pickaxe 风味文本;1.4.4.9 非英语本地化更新;1.4.4.6 Everything 单人 Boss 死亡计时器偏长),不构成问题。

## 数值矛盾

| 条目 | 官方值 | 摘要值 |
|---|---|---|
| Philosopher's Stone 动态冷却示例(穿半分钟卸下) | 仅减 **7.5** 秒(而非 15) | 减 **10** 秒(line 241) |
| 早期金属阔剑计数 | **8** 把(Copper/Tin/Iron/Lead/Silver/Tungsten/Gold/Platinum) | 写"**7** 种"(line 63,但实际列了 8 把,仅措辞错) |

另有一处名称口径(非数值):官方称新草为 "Crimson and Corrupt **Mud Grass**",摘要译作"血腥/腐化**丛林草**";描述句(不再退化为泥土)两边一致,仅命名口径不同。

## 结论

**完整度粗估 95%**:内容/平衡条目约 97%(约 600 条中漏 15 条上下,其中真正影响复刻对表的 5 条:Mech Cart 削弱、Morning Star、Celestial Sigil 召唤时间、Wand of Sparking、Metal Detector 优先级);bug 修复为有意筛选,方向正确。**需要修订,但属小幅**:补上述 5 条重点遗漏 + 3 条子数值、修正 7.5 秒与"7 种"计数,再按计划补 1.4.4.8.1 即可。摘要中的 Item ID 尺寸对照表、(→ 文件)标注、规模评估等为 zh wiki 补充内容,官方日志没有,属正常增补不计为问题。
```


---

## 👤 User(meta)(sidechain) · 2026-08-09T11:46:17.165Z

```
The coordinator sent a message while you were working:
校验报告收到。现在请把你报告中的修订直接应用到 ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md:
1. 补 5 条重点遗漏平衡条目(Mech Cart 削弱、Morning Star 平衡条目 45→35/标记 5→8/暴击加成 5→12、Celestial Sigil 60→12s、Wand of Sparking、Metal Detector Life Crystal 优先级)
2. 补 3 条子数值(Flamethrower 穿透 3→4、Candy Cane Sword 使用 27→25、Mythril Sword 尺寸 1.15→1.2)
3. 修正 Philosopher's Stone 冷却示例为 7.5 秒、"7 种"金属阔剑计数改为 8 把
4. 顺手补几条你列的 I/C 章遗漏条目(快速堆叠范围、南瓜月/霜月总分、四条宏观新增等),每条保持 "(→ 文件)" 标注格式
5. 文件末尾加一小节【校验记录】,注明"已用官方 changelog.txt 反向核对,完整度约 95%"
注意:1.4.4.8.1 小节我已手动补过,不要动它。你的 Edit/Write 工具可能被拦截,若失败就用 Bash 写入(python3 heredoc)。完成后返回修订摘要(改了几处、加了几条)。

Address this before completing your current task.
```

---

## 🤖 Assistant · 2026-08-09T11:46:45.605Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I need to apply the revisions. Let me plan the edits:

1. Five balance entries:
   - Mech Cart nerf → line 35 area (Accessories, Mounts, Tools, Tiles section, or amend line 35). Line 35 is in 【New Content - Items】: "Mechanical Cart entry implies new item Minecart Upgrade Kit...". Better to add the Mech Cart nerf to the 【Accessories, Mounts, Tools, Tiles】 section near the minecart entries (line 249 "All minecarts..."). I'll add a new line after line 249 or amend line 35. I think adding a proper entry in the accessories section is right, and maybe also fix line 35 to be clearer. I'll amend line 35 to include the nerf, and/or add to accessories. Simplest: add a new bullet in accessories section after line 249 (all minecarts): "Mechanical Cart: speed/stats aligned with regular minecarts, no longer fires lasers (laser effects taken over by new item Minecart Upgrade Kit) (→ Item.cs, Projectile.cs)".
   
   - Morning Star balance entry → summon weapons section. Insert after Dark Harvest (line 193) or before. Add: "Morning Star: use 45→35, tag damage 5→8, minion crit bonus 5→12, chain segments increased for better visibility (→ Item.cs)"
   
   - Celestial Sigil 60→12s → 【Recipes and Prices】 near line 310. Amend line 310: "- Celestial Sigil: 20 of each type of lunar fragment→12; summoning Moon Lord time 60 seconds→12 seconds (→ Recipe.cs, NPC.cs)"
   
   - Wand of Sparking → magic weapons section, near mana regen (line 154). Add: "- Wand of Sparking: On Fire! average duration slightly increased (→ Item.cs)"
   
   - Metal Detector Life Crystal priority → 【Drop Rates and Acquisition Sources】 or mechanics. I'll put in drop rates section, maybe near end (line 306 area). Add: "- Life Crystals now have lower priority than Hardmode ores on the Metal Detector (→ Item.cs, Player.cs)"

2. Three sub-values:
   - Flamethrower pierce 3→4: line 135 "- Flamethrower: projectiles changed to local invincibility frames, ignores 15 defense before damage calculation, visuals and hitbox reworked, changed to Hellfire" → add "pierce 3→4".
   - Candy Cane Sword use 27→25: line 67 contains "Candy Cane Sword(16→19)" → change to "Candy Cane Sword(16→19, use 27→25)".
   - Mythril Sword size 1.15→1.2: line 85 "Mythril(49→50、26→20)" → "Mythril(49→50、26→20、1.15→1.2)".

3. Philosopher's Stone: line 241 "reduces by only 10 seconds instead of 15" → "reduces by only 7.5 seconds instead of 15". And line 63 "7 metal broadswords" → "8 metal broadswords (early metals)".

4. I/C chapter additions:
   - Quick stack range: UI section, near line 404 (quick stack animation). Add bullet.
   - Pumpkin/Frost Moon total score: could add to UI section or pumpkin moon. Add to UI: "- Pumpkin Moon/Frost Moon display total score when event ends (→ Main.cs)". Or add to the Pumpkin Moon line 343. I'll add to UI section.
   - Abigail's Flower one-hit break: add.
   - Flower Accessory/Jungle Rose: add.
   - Pengfish/Pixiefish: add (small).
   - Four macro additions (new achievements/new death messages/new title texts/world name lexicon): add to 【New Content - Items】 section.
   - Gravedigger's Shovel AnyIron recipe: add to 【Recipes and Prices】.

5. Add 【Verification Record】 at end.

Don't touch 1.4.4.8.1.

Let me do the edits with the Edit tool. I've already read the file. Let me make each edit.

Edit 1: line 63 "7 metal broadswords fully buffed" → "8 metal broadswords fully buffed". Actually the text: "- 7 metal broadswords fully buffed: Copper(..." — change "7" to "8".

Edit 2: line 85 Mythril: "- 6 Hardmode metal swords buffed: Cobalt(39→40、23→19、1.1→1.2、3.85→5)、Palladium(45→49、25→22、1.125→1.2、4.75→5.5)、Mythril(49→50、26→20)、Orichalcum..." → "Mythril(49→50、26→20、1.15→1.2)".

Edit 3: line 67 Candy Cane Sword: "Candy Cane Sword(16→19)" → "Candy Cane Sword(16→19、use 27→25)".

Edit 4: line 135 Flamethrower: "- Flamethrower: projectiles changed to local invincibility frames, ignores 15 defense before damage calculation, visuals and hitbox reworked, changed to Hellfire(→ Item.cs, Projectile.cs)" → insert "pierce 3→4、". 

Edit 5: line 154 area — add Wand of Sparking after mana regen line. Insert new line after line 154.

Edit 6: Morning Star in summon section. Insert after line 193 (Dark Harvest) — actually order: official order is Cool Whip, Durendal, Morning Star, Dark Harvest. Summary has Cool Whip (192), Durendal/Dark Harvest (193). Insert Morning Star as new line after 192? Let me insert after line 192 (Cool Whip) and before 193: "- Morning Star: use 45→35, tag damage 5→8, minion critical bonus 5→12, chain segments greatly increased for more visible swing arc (→ Item.cs)".

Edit 7: Mech Cart — add to accessories section. After line 249 "All minecarts: ..." add "- Mechanical Cart: speed and attributes aligned with regular minecarts, no longer fires lasers (laser effects taken over by new item Minecart Upgrade Kit) (→ Item.cs, Projectile.cs)".

Also line 35 mentions "Mechanical Cart entry implies new item Minecart Upgrade Kit" — keep as is, or amend. I'll leave it; the new bullet in accessories covers it. Actually to avoid duplication confusion, maybe amend line 35 slightly? The coordinator said "Mech Cart nerf" as one of the 5. I'll add the accessories bullet which contains the nerf. That's sufficient. But line 35 says "entry implies new item" which now is redundant-ish but harmless. I'll leave it.

Edit 8: Metal Detector — drop rates section. Add after line 306 (Bast Statue) or near line 285 drop rate increases. I'll add at end of drop rates section after line 306: "- Life Crystals now have lower priority than Hardmode ores on the Metal Detector (→ Item.cs, Player.cs)".

Edit 9: Celestial Sigil line 310: "- Celestial Sigil: 20 of each type of lunar fragment→12(→ Recipe.cs)" → "- Celestial Sigil: 20 of each type of lunar fragment→12; Celestial Sigil summons Moon Lord with only 12 seconds of summoning time (originally 60 seconds) (→ Recipe.cs, NPC.cs)".

Edit 10: Philosopher's Stone line 241: "10 seconds" → "7.5 seconds".

Edit 11: I/C additions in UI section. Add several bullets. Where? UI section lines 411-463. Add after line 404 (quick stack animation) — but that's rendering section. Quick stack animation is in 【Rendering and Visual Effects】 line 404. The quick stack range increase fits UI. Let me add a small cluster of new bullets at the end of the UI section (after line 463 "consistency adjustments for some Up/Down key tooltip text") — before 【Audio】:

"- Quick Stack to Nearby Chests range significantly increased (→ Main.cs)
- Pumpkin Moon/Frost Moon display total score when event ends (→ Main.cs)
- Pengfish/Pixiefish quest info description aligned with similar fish (→ Item.cs, Main.cs)
- Flower Accessory social slot display drawn over helmets/face accessories for combining; Jungle Rose changed from head vanity to vanity accessory (→ Item.cs, Player.cs)
- Abigail's Flower now breaks in one hit when mined and plays a grass sound (→ Item.cs, TileID.cs)"

Edit 12: four macro additions → 【New Content - Items】 section. Add at end of that section (after line 37, before ## 【New Content - NPC/Boss】):
"- New achievements, new death messages, new title texts, random world name lexicon expanded with many new words (→ Main.cs, Lang.cs)"

Edit 13: Gravedigger's Shovel AnyIron → 【Recipes and Prices】. Add after line 316 or near 320. Add after line 313: "- Gravedigger's Shovel iron/lead double recipe merged into a single AnyIron recipe (→ Recipe.cs)".

Edit 14: 【Verification Record】 at end of file, after the risk notes section (line 629). Append:

"---

# Four, 【Verification Record】

- This summary was reverse-verified line by line against the official changelog.txt (1.4.4 main section lines 2374-4368, hotfixes 1.4.4.1~1.4.4.9 lines 1951-2373); completeness about 95%.
- Missing balance/QoL entries and sub-values have been filled in per verification findings: Mechanical Cart nerf, Morning Star balance entry, Celestial Sigil summoning time, Wand of Sparking, Metal Detector priority, Flamethrower pierce, Candy Cane Sword use time, Mythril Sword size, quick stack range, event total score, and others.
- Philosopher's Stone cooldown example corrected to 7.5 seconds (official original), early metal broadsword count corrected to 8.
- 1.4.4.8.1 subsection filled in separately.
- Reference for final values: post-1.4.4.9 (including hotfix secondary corrections)."

Let me now make these edits. I'll use Edit tool calls. Many are independent edits to different strings — but they're all in the same file; parallel Edit calls to the same file might conflict? The instructions say independent calls can be parallel. Edits to the same file with unique old_strings should be fine, but to be safe with file-state tracking, I'll batch a few at a time. Actually, editing the same file in parallel could cause race issues. I'll do them sequentially in small batches — actually each Edit is applied in order if in the same block? Risky. Let me do them one per message but that's many round trips. I'll try batching multiple Edit calls in one block; the harness applies them sequentially. It's generally supported. I'll batch them.

Let me be careful with exact strings from the Read output (strip line numbers).
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:46:45.606Z · glm-x-preview-260804

```
收到,我直接把修订应用到摘要文件。先做数值修正与子数值补录。
```


---

## 🤖 Assistant · 2026-08-09T11:46:46.309Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md",
 "old_string": "- 7 种金属阔剑全面加强:",
 "new_string": "- 8 种金属阔剑全面加强:"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:46:46.321Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:46:47.037Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md",
 "old_string": "Mythril(49→50、26→20)、Orichalcum",
 "new_string": "Mythril(49→50、26→20、1.15→1.2)、Orichalcum"
}
```


---

## 🤖 Assistant · 2026-08-09T11:46:47.039Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md",
 "old_string": "Candy Cane Sword(16→19)",
 "new_string": "Candy Cane Sword(16→19、使用 27→25)"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:46:47.049Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 👤 User(sidechain) · 2026-08-09T11:46:47.056Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:46:48.367Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md",
 "old_string": "- Flamethrower:弹幕改局部无敌帧,伤害计算前无视 15 防御,视觉与碰撞箱重做,改 Hellfire(→ Item.cs, Projectile.cs)",
 "new_string": "- Flamethrower:弹幕改局部无敌帧,伤害计算前无视 15 防御,穿透 3→4,视觉与碰撞箱重做,改 Hellfire(→ Item.cs, Projectile.cs)"
}
```


---

## 🤖 Assistant · 2026-08-09T11:46:48.372Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md",
 "old_string": "(穿戴半分钟再卸下仅减 10 秒而非 15 秒)",
 "new_string": "(穿戴半分钟再卸下仅减 7.5 秒而非 15 秒)"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:46:48.380Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 👤 User(sidechain) · 2026-08-09T11:46:48.387Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:46:53.441Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Five edits applied. Now add the new entries (5 balance + I/C additions + verification record).
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:46:53.444Z · glm-x-preview-260804

```
5 处修正已应用。接着补 5 条重点平衡条目与 I/C 章遗漏条目。
```


---

## 🤖 Assistant · 2026-08-09T11:46:54.053Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md",
 "old_string": "- 基础魔力再生重做:移动基础再生翻倍以上;静止/药水加成降 1/3(总量持平,最低再生率大幅提高)(→ Player.cs, Main.cs)",
 "new_string": "- 基础魔力再生重做:移动基础再生翻倍以上;静止/药水加成降 1/3(总量持平,最低再生率大幅提高)(→ Player.cs, Main.cs)\n- Wand of Sparking:On Fire! 平均持续时间略微增加(→ Item.cs)"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:46:54.062Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:46:55.295Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md",
 "old_string": "- Cool Whip:伤害 50→45,标记伤害 6,雪花伤害 10→15 且速度 +50%,改 Frostbite(→ Item.cs, Projectile.cs)",
 "new_string": "- Cool Whip:伤害 50→45,标记伤害 6,雪花伤害 10→15 且速度 +50%,改 Frostbite(→ Item.cs, Projectile.cs)\n- Morning Star:使用 45→35,标记伤害 5→8,仆从暴击加成 5→12,链条段数大幅增加(挥舞弧光更清晰可见)(→ Item.cs)"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:46:55.318Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:46:55.932Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md",
 "old_string": "- 全部矿车:更高难度下更高伤害与击退,更容易撞飞敌人(→ Projectile.cs, Player.cs)",
 "new_string": "- 全部矿车:更高难度下更高伤害与击退,更容易撞飞敌人(→ Projectile.cs, Player.cs)\n- Mechanical Cart(削弱):速度与属性对齐普通矿车,不再发射激光(激光效果由新物品 Minecart Upgrade Kit 承接)(→ Item.cs, Projectile.cs)"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:46:55.963Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:46:56.542Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md",
 "old_string": "- Bast Statue 可在地下沙漠小屋作为家具生成(→ WorldGen.cs)",
 "new_string": "- Bast Statue 可在地下沙漠小屋作为家具生成(→ WorldGen.cs)\n- Life Crystal 在 Metal Detector 上优先级降低,低于 Hardmode 矿石(→ Item.cs, Player.cs)"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:46:56.556Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:46:57.184Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md",
 "old_string": "- Celestial Sigil:每类月亮碎片 20→12(→ Recipe.cs)",
 "new_string": "- Celestial Sigil:每类月亮碎片 20→12;且以 Celestial Sigil 召唤月总的召唤时间由 60 秒缩短至 12 秒(→ Recipe.cs, NPC.cs)"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:46:57.203Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:47:02.164Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now: I/C additions — UI section additions (quick stack range, event total score, Pengfish, Flower Accessory/Jungle Rose, Abigail's Flower), 四条宏观新增 (content additions), Gravedigger's Shovel recipe, and 校验记录 at end.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:47:02.167Z · glm-x-preview-260804

```
平衡条目补录完成。现在补 I/C 章遗漏条目、Gravedigger's Shovel 配方与文末校验记录。
```


---

## 🤖 Assistant · 2026-08-09T11:47:03.473Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md",
 "old_string": "- 添加 Jungle Birds(丛林鸟类生物)(→ NPCID.cs, NPC.cs)\n- 添加 1 种新树(Ash Wood 树,配合 Ash Wood 家具/工具链)(→ TileID.cs, WorldGen.cs)",
 "new_string": "- 添加 Jungle Birds(丛林鸟类生物)(→ NPCID.cs, NPC.cs)\n- 添加 1 种新树(Ash Wood 树,配合 Ash Wood 家具/工具链)(→ TileID.cs, WorldGen.cs)\n- 宏观新增:新成就、新死亡信息、新标题文本、随机世界名词库新增大量词汇(→ Main.cs, Lang.cs)"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:47:03.485Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:47:04.811Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md",
 "old_string": "- 部分上下键 tooltip 文本一致性调整(→ Main.cs)",
 "new_string": "- 部分上下键 tooltip 文本一致性调整(→ Main.cs)\n- 快速堆叠至附近宝箱的范围显著增加(→ Main.cs)\n- 南瓜月/霜月事件结束时显示本次事件总分(→ Main.cs)\n- Pengfish/Pixiefish 任务信息描述与同类鱼保持一致(→ Item.cs, Main.cs)\n- Flower Accessory 社交栏显示绘制于头盔/面部配饰之上(便于组合);Jungle Rose 由头部虚荣改为虚荣配饰(→ Item.cs, Player.cs)\n- Abigail's Flower 挖掘时一击破坏并播放草声(→ Item.cs, TileID.cs)"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:47:04.821Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:47:05.344Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md",
 "old_string": "- Angel/Demon Wings 灵魂消耗 25→15;Empty Bucket 铁锭/铅锭 3→2(→ Recipe.cs)",
 "new_string": "- Angel/Demon Wings 灵魂消耗 25→15;Empty Bucket 铁锭/铅锭 3→2(→ Recipe.cs)\n- Gravedigger's Shovel 铁锭/铅锭双配方合并为单一 AnyIron 配方(→ Recipe.cs)"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:47:05.353Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:47:07.244Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now append the 校验记录 section at the end of the file. The file ends with the 风险提示 section (line 629 originally: "- 免疫帧规则改动横跨 Item/Projectile/NPC/Player 四个文件,是本版本最容易引入手感偏差的部分。"). I'll append after that.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:47:07.245Z · glm-x-preview-260804

```
最后在文件末尾追加【校验记录】小节。
```


---

## 🤖 Assistant · 2026-08-09T11:47:10.173Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md",
 "old_string": "- 免疫帧规则改动横跨 Item/Projectile/NPC/Player 四个文件,是本版本最容易引入手感偏差的部分。",
 "new_string": "- 免疫帧规则改动横跨 Item/Projectile/NPC/Player 四个文件,是本版本最容易引入手感偏差的部分。\n\n---\n\n# 四、【校验记录】\n\n- 本摘要已用官方 changelog.txt 反向逐条核对(1.4.4 主段落第 2374-4368 行;热修 1.4.4.1~1.4.4.9 第 1951-2373 行),完整度约 95%。\n- 依据校验结论已补录遗漏条目:Mechanical Cart 削弱、Morning Star 平衡条目(45→35/标记 5→8/暴击 5→12)、Celestial Sigil 召唤时间 60→12 秒、Wand of Sparking、Metal Detector 的 Life Crystal 优先级;以及快速堆叠范围、事件总分显示、Flower Accessory/Jungle Rose、Abigail's Flower、宏观新增(成就/死亡信息/标题/词库)、Gravedigger's Shovel 配方等。\n- 已修正数值:Philosopher's Stone 动态冷却示例改为 7.5 秒(以官方原文为准);早期金属阔剑计数改为 8 把;补 Flamethrower 穿透 3→4、Candy Cane Sword 使用 27→25、Mythril Sword 尺寸 1.15→1.2。\n- 1.4.4.8.1 小节另行补录;最终数值以 1.4.4.9(含全部热修二次修正)为准。"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:47:10.195Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.4.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:47:15.300Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Verify the changes landed and that 1.4.4.8.1 wasn't touched. Let me grep quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:47:15.301Z · glm-x-preview-260804

```
校验改动是否全部落盘,并确认 1.4.4.8.1 小节未被触碰。
```


---

## 🤖 Assistant · 2026-08-09T11:47:16.988Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries && echo \"== 8 种阔剑 ==\" && grep -c \"8 种金属阔剑\" summary-1.4.4.md && echo \"== 7.5 秒 ==\" && grep -n \"7.5 秒\" summary-1.4.4.md | head -3 && echo \"== 新增条目抽查 ==\" && grep -n \"Wand of Sparking\\|Morning Star:使用\\|Mechanical Cart(削弱)\\|Life Crystal 在 Metal\\|60 秒缩短至 12\\|快速堆叠至附近宝箱的范围显著\\|总分\\|宏观新增\\|Gravedigger\\|校验记录\" summary-1.4.4.md && echo \"== 1.4.4.8.1 小节(应保持不动)== \" && grep -n -A 8 \"^## 1.4.4.8.1\" summary-1.4.4.md && wc -l summary-1.4.4.md",
 "description": "Verify all edits landed and 1.4.4.8.1 untouched"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:47:17.036Z

**📎 ToolResult**

```
== 8 种阔剑 ==
1
== 7.5 秒 ==
244:- Philosopher's Stone/Charm of Myths:药水病冷却改为按装备时刻动态等比缩放(穿戴半分钟再卸下仅减 7.5 秒而非 15 秒)(→ Item.cs, Player.cs)
656:- 已修正数值:Philosopher's Stone 动态冷却示例改为 7.5 秒(以官方原文为准);早期金属阔剑计数改为 8 把;补 Flamethrower 穿透 3→4、Candy Cane Sword 使用 27→25、Mythril Sword 尺寸 1.15→1.2。
== 新增条目抽查 ==
38:- 宏观新增:新成就、新死亡信息、新标题文本、随机世界名词库新增大量词汇(→ Main.cs, Lang.cs)
156:- Wand of Sparking:On Fire! 平均持续时间略微增加(→ Item.cs)
195:- Morning Star:使用 45→35,标记伤害 5→8,仆从暴击加成 5→12,链条段数大幅增加(挥舞弧光更清晰可见)(→ Item.cs)
253:- Mechanical Cart(削弱):速度与属性对齐普通矿车,不再发射激光(激光效果由新物品 Minecart Upgrade Kit 承接)(→ Item.cs, Projectile.cs)
311:- Life Crystal 在 Metal Detector 上优先级降低,低于 Hardmode 矿石(→ Item.cs, Player.cs)
315:- Celestial Sigil:每类月亮碎片 20→12;且以 Celestial Sigil 召唤月总的召唤时间由 60 秒缩短至 12 秒(→ Recipe.cs, NPC.cs)
319:- Gravedigger's Shovel 铁锭/铅锭双配方合并为单一 AnyIron 配方(→ Recipe.cs)
470:- 快速堆叠至附近宝箱的范围显著增加(→ Main.cs)
471:- 南瓜月/霜月事件结束时显示本次事件总分(→ Main.cs)
652:# 四、【校验记录】
655:- 依据校验结论已补录遗漏条目:Mechanical Cart 削弱、Morning Star 平衡条目(45→35/标记 5→8/暴击 5→12)、Celestial Sigil 召唤时间 60→12 秒、Wand of Sparking、Metal Detector 的 Life Crystal 优先级;以及快速堆叠范围、事件总分显示、Flower Accessory/Jungle Rose、Abigail's Flower、宏观新增(成就/死亡信息/标题/词库)、Gravedigger's Shovel 配方等。
== 1.4.4.8.1 小节(应保持不动)== 
604:## 1.4.4.8.1(2022-11-10,desktop)
605-- 修复 1.4.4.8 引入的问题:海洋晶塔在 Don't dig up/Get fixed boi 种子中无法使用 (→ PylonSystem, WorldGen.cs)
606-- 修复 1.4.4.8 引入的问题:使用向导/哥布林工匠的特殊菜单时无法整理背包 (→ Player.cs, Terraria.GameContent.UI)
607-- 修复多人下因更换装备导致己方哨兵被移除时,可能连带移除其他玩家哨兵的问题 (→ Player.cs, Terraria.NetMessage)
608-- 修复 Bone Helm 在重力反转时小地图上人物标识显示不正确 (→ Main.cs, Terraria.Map)
609-- 调整绞肉机(Meat Grinder)方块外观位置,更均匀、少占无效空间 (→ TileDrawing.cs)
610-- **平衡:North Pole 伤害在 1.4.4.8 调整基础上 73→80** (→ Item.cs)
611-
612-## 1.4.4.9(2022-11-17,desktop)
     657 summary-1.4.4.md

```


---

## 🤖 Assistant · 2026-08-09T11:47:23.135Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All edits landed, 1.4.4.8.1 intact (manually added by coordinator, untouched). File went from 629 lines to 657 lines. All 13 edits applied.

Summary of changes:
- 修正 2 处数值/计数:Philosopher's Stone 10→7.5 秒;"7 种"→"8 种"金属阔剑
- 补 3 条子数值:Flamethrower 穿透 3→4、Candy Cane Sword 使用 27→25、Mythril Sword 尺寸 1.15→1.2(内嵌于既有条目)
- 新增 11 条条目(每条带 (→ 文件) 标注):
  1. Wand of Sparking(魔法节)
  2. Morning Star(召唤节)
  3. Mechanical Cart 削弱(配饰坐骑节)
  4. Life Crystal Metal Detector 优先级(掉落节)
  5. Celestial Sigil 召唤时间(扩写既有条目)
  6. 宏观新增(新增内容-物品节)
  7. 快速堆叠范围(UI 节)
  8. 南瓜月/霜月总分(UI 节)
  9. Pengfish/Pixiefish(UI 节)
  10. Flower Accessory/Jungle Rose(UI 节)
  11. Abigail's Flower(UI 节)
  12. Gravedigger's Shovel 配方(配方节)
  Actually that's 12 new bullets (Celestial Sigil was an amend, not new bullet). New bullets: Wand of Sparking, Morning Star, Mechanical Cart, Life Crystal, 宏观新增, 快速堆叠范围, 总分, Pengfish, Flower Accessory, Abigail's, Gravedigger's = 11 new bullets + 1 amended (Celestial Sigil).
- 新增文末【校验记录】小节(4 行)
- 总计 13 处编辑,文件 629→657 行
- 1.4.4.8.1 未动
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:47:27.495Z · glm-x-preview-260804

```
修订已全部应用完成。

## 修订摘要

**共 14 处编辑,文件 629 → 657 行;1.4.4.8.1 小节已确认原样保留(你手动补的 6 条均在)。**

**修正(4 处,内嵌于既有条目)**
1. Philosopher's Stone 冷却示例:10 秒 → **7.5 秒**(line 244,以官方原文为准)
2. 早期金属阔剑计数:"7 种" → **"8 种"**(line 64)
3. Flamethrower 补穿透 **3→4**(line 138,Elf Melter 原有、Flamethrower 之前漏)
4. Candy Cane Sword 补使用 **27→25**(line 68);Mythril Sword 补尺寸 **1.15→1.2**(line 86)——合并计为 2 处

**新增条目(11 条,全部带 "(→ 文件)" 标注)**
| 条目 | 归入小节 | 行号 |
|---|---|---|
| Mechanical Cart 削弱(对齐普通矿车、失去激光,由 Minecart Upgrade Kit 承接) | 配饰、坐骑、工具、图格 | 253 |
| Morning Star:使用 45→35、标记 5→8、仆从暴击 5→12、链段视觉 | 召唤武器 | 195 |
| Celestial Sigil 召唤月总时间 60s→12s(扩写原配方条目) | 配方与价格 | 315 |
| Wand of Sparking:On Fire! 时长略增 | 魔法武器 | 156 |
| Life Crystal 在 Metal Detector 优先级低于 Hardmode 矿石 | 掉落几率与获取来源 | 311 |
| 宏观新增(成就/死亡信息/标题文本/世界名词库) | 新增内容-物品 | 38 |
| 快速堆叠至附近宝箱范围显著增加 | UI与界面/生活质量 | 470 |
| 南瓜月/霜月结束显示总分 | 同上 | 471 |
| Pengfish/Pixiefish 任务描述一致性 | 同上 | 472 |
| Flower Accessory 社交栏绘制层级 + Jungle Rose 改虚荣配饰 | 同上 | 473 |
| Abigail's Flower 一击挖断+草声 | 同上 | 474 |
| Gravedigger's Shovel 合并为单一 AnyIron 配方 | 配方与价格 | 319 |

**新增文末小节**【校验记录】(line 652-657):注明已用官方 changelog.txt 反向核对(主段落 2374-4368 行、热修 1951-2373 行)、完整度约 95%,并列明本次补录与修正清单。

官方 I/C 章其余更琐碎的遗漏(如 Phasesaber 发光修复、搜索栏右键退出等纯文本/视觉项)按此前校验结论未逐条补入,摘要的 bug 修复筛选口径保持不变。
```
