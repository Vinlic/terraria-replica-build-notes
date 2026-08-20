# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-09T11:40:56.931Z

```
你是校验员。权威数据:官方 changelog.txt(英文,`~/Library/Application Support/Steam/steamapps/common/Terraria/changelog.txt`,即 ~/Library/Application Support/Steam/steamapps/common/Terraria/changelog.txt)。其中 **Version 1.4.1 到 1.4.1.2** 的段落是第 4889 行到第 5991 行(用 `sed -n '4889,5991p' <文件>` 读取,可分段)。

被校验文档:~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md(中文,基于 zh wiki 解析)。

任务:逐节对比官方 changelog 与中文摘要,找出:
1. **官方日志里有、但摘要完全没提的条目**(重点是 Balance/Changes/新机制类;纯 bug 修复只统计数量差异并列举最重要的 5 条以内)
2. **数值矛盾**(同一物品/机制两边数字不一致)
3. 摘要里有但官方日志没有的内容(通常是 zh wiki 补充细节,只需一句带过不算问题)

官方 1.4.1 主段落约 1100 行,你要系统性扫完,不要抽样。分类输出为紧凑清单,中文。

返回格式:
## 遗漏条目(按官方章节分组,每条一行:官方原文要点 → 应归入摘要哪个小节)
## 数值矛盾(条目、官方值、摘要值)
## 结论(摘要完整度百分比粗估 + 是否需要修订)
```

---

## 📎 Attachment · skill_listing · 2026-08-09T11:40:56.934Z

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

## 🤖 Assistant · 2026-08-09T11:40:58.800Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I need to read the official changelog lines 4889-5991 and the Chinese summary file, then compare them systematically.

Let me start by reading the official changelog in segments and the summary file in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:40:58.801Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '4889,5300p' \"~/Library/Application Support/Steam/steamapps/common/Terraria/changelog.txt\"",
 "description": "Read changelog lines 4889-5300"
}
```


---

## 🤖 Assistant · 2026-08-09T11:40:59.016Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:40:59.174Z

**📎 ToolResult**

```
1	# 泰拉瑞亚 1.4.1 / 1.4.1.1 / 1.4.1.2 更新日志结构化摘要
2	
3	> 来源：中文 wiki（MediaWiki API wikitext），原始文件 /tmp/tw-changelog/1.4.1.json、1.4.1.1.json、1.4.1.2.json。
4	> 1.4.1 代号 "Rounding Out the Journey（结束旅程）"，发布于 2020-10-13；1.4.1.1 发布于 2020-10-14；1.4.1.2 发布于 2020-11-10。
5	> 行尾括号内为该条大概率影响的反编译源码文件（Terraria 命名空间）。
6	
7	---
8	
9	## 一、版本 1.4.1（Rounding Out the Journey）
10	
11	### 【新增内容】
12	
13	- 新增 6 套 Vanity 竞赛获奖套装，全部可用 pre-Hardmode 材料制作：瘟疫使者套装（Plaguebringer's set）、流浪者套装（Wandering set）、时空旅者套装（Timeless Traveler's set）、小花守护者套装（Floret Protector set）、摩羯座套装（Capricorn set）、电视头套装（TV Head set，大奖得主）(→ Item.cs, Recipe.cs, Terraria.ID/ItemID.cs)
14	- 新增一批成就 (→ Main.cs, Terraria.GameContent.UI)
15	- 新增制作人员字幕（Credits）及对应音乐曲目：第一次打败 Moon Lord 后出现，主菜单也可查看；Music Box (Journey's End) 改为录下 Credits 音乐生成，普通饰品栏使用会在游戏内播放 Credits 动画，社交栏使用只放音乐 (→ Item.cs, Main.cs, Terraria/Audio)
16	- 新城镇 NPC 公主（Princess）及各种相关物品，外加一个新发型 (→ NPC.cs, Terraria.ID/NPCID.cs, Item.cs)
17	- 新早期召唤装备：Flinx Fur Coat（伶鼬皮大衣）、Flinx Staff（伶鼬法杖）(→ Item.cs, Terraria.ID/ItemID.cs, Projectile.cs)
18	- 新 pre-Hardmode 鞭子 Spinal Tap（脊骨鞭），地牢等级可制作 (→ Item.cs, Projectile.cs, Recipe.cs)
19	- 新饰品 Lavaproof Tackle Bag（熔岩防钓具袋）：Lavaproof Fishing Hook + Angler Tackle Bag 合成 (→ Item.cs, Recipe.cs)
20	- Bee Hive（蜂巢块）与 Antlion Eggs（蚁狮蛋）现在可制作、可放置 (→ Item.cs, Recipe.cs, Terraria.ID/TileID.cs)
21	- 新 vanity 饰品 Rainbow Cursor（彩虹光标）(→ Item.cs)
22	
23	### 【物品与数值平衡 — 近战武器】
24	
25	- Terra Blade 线整体重构：Mothron 只在 Plantera 后生成，Broken Hero Sword 因此变为 Plantera 后限定 (→ NPC.cs, WorldGen.cs, Item.cs)
26	- True Night's Edge：弹幕伤害 1.5 倍基础伤害；autoswing；配方改为 Night's Edge + 3 个机械 Boss 魂，不再需要 Broken Hero Sword (→ Item.cs, Projectile.cs, Recipe.cs)
27	- True Excalibur：伤害 66→70；autoswing；弹幕穿透 1 次最多命中 2 敌；配方改为 Excalibur + 叶绿锭，不再需要 Broken Hero Sword (→ Item.cs, Projectile.cs, Recipe.cs)
28	- Terra Blade：伤害 95→115，Use Time 16→14，弹幕伤害 1.25 倍→1.5 倍；配方改为两把"真"剑 + 一把 Broken Hero Sword (→ Item.cs, Projectile.cs, Recipe.cs)
29	- Beam Sword：缩放比例 1→1.3（剑本体变大）(→ Item.cs, Projectile.cs)
30	- Brand of the Inferno：缩放比例 1.15→1.3 (→ Item.cs, Projectile.cs)
31	- Sunfury：基础伤害 35→32（链球普通挥舞双倍伤害，预期伤害 70→64）(→ Item.cs)
32	- Arkhalis：伤害 20→25；忽略至多 20 点敌人防御 (→ Item.cs, Projectile.cs)
33	- Chain Guillotines：伤害 43→59 (→ Item.cs)
34	- Ghastly Glaive：免伤帧时长 36→20 (→ Projectile.cs)
35	- Anchor：伤害 55→70，击退 5→8 (→ Item.cs)
36	- Sergeant United Shield：伤害 60→80；每命中一个目标的伤害减免 30%→20% (→ Item.cs, Projectile.cs)
37	- Scourge of the Corruptor：伤害 64→70；小吞噬怪伤害 70%→75% 基础伤害 (→ Item.cs, Projectile.cs)
38	- 悠悠球：撤销 1.4 对 Chik、Amarok、Hel-Fire 的改动；不撤销 Code 2、Amazon、Kraken 的改动；Gradient 伤害 44→49；Format C 伤害 35→39 (→ Item.cs)
39	- Light's Bane：伤害 17→18 (→ Item.cs)
40	- Muramasa：伤害 21→26，击退 2.5→3 (→ Item.cs)
41	- Fiery Greatsword：伤害 36→40 (→ Item.cs)
42	- Beekeeper：撤销 1.4 对它的改动 (→ Item.cs)
43	- 所有 Phaseblade：伤害 21→25 (→ Item.cs)
44	- Night's Edge：Use Time 27→21；autoswing (→ Item.cs)
45	- Bananarang：Use Time 14→11；香蕉弹幕速度与返回速度均提升 (→ Item.cs, Projectile.cs)
46	- Thorn Chakram / Flamarang：弹幕速度与返回速度均提升，Flamarang 更快 (→ Projectile.cs)
47	- Sleepy Octopod：伤害 40→50；命中半径/攻击大小 +35% (→ Item.cs, Projectile.cs)
48	- Flying Dragon：伤害 90→180；视线无法直达的弹幕（穿墙射击）只造成一半伤害（即 90）(→ Item.cs, Projectile.cs)
49	- Sky Dragon's Fury：伤害 70→140；弹幕伤害 75%→50% 基础伤害（单发实际 52，原 70）(→ Item.cs, Projectile.cs)
50	- Starlight：伤害 70→80；新增 10% 暴击率奖励 (→ Item.cs)
51	- Daybreak：弹幕在过期或击中墙时爆炸，爆炸额外造成 100% 武器伤害并可命中附近敌人 (→ Projectile.cs)
52	
53	### 【物品与数值平衡 — 远程武器与弹药】
54	
55	- Onyx Blaster：伤害 28→24，Use Time 45→48 (→ Item.cs)
56	- Quad-Barrel Shotgun：伤害 24→17，弹丸数 4→6，Use Time 45→55；军火商只在骷髅王后出售 (→ Item.cs, Projectile.cs, NPC.cs)
57	- StakeLauncher：Use Time 26→12；弹幕每穿透一敌，下一次命中受 10% 伤害惩罚 (→ Item.cs, Projectile.cs)
58	- Blowpipe：Use Time 45→25；种子（弹药）伤害 3→4 (→ Item.cs)
59	- Jack 'O Lantern Launcher：Use Time 30→25；爆炸南瓜（弹药）伤害 30→60 (→ Item.cs)
60	- Dart Pistol / Dart Rifle：撤销 1.4 的平衡改动，伤害分别 33→28、62→52（注：wiki 标注此条实际到 1.4.2.2 才生效）；Crystal/Curse/Ichor 弹药的改动保留 (→ Item.cs)
61	- Tsunami：伤害 60→53 (→ Item.cs)
62	- Nano Bullet：可反弹一次，附近有目标时"智能反弹"；反弹后只造成 66% 伤害 (→ Projectile.cs, Item.cs)
63	- Beenade：伤害 14→12；Bone Arrow：伤害 6→8；Chlorophyte Bullet：伤害 10→9 (→ Item.cs)
64	- Cursed Bullet：速度提升到与 Ichor Bullet 一致 (→ Item.cs)
65	- Meteor Shot：伤害 9→8；重做免伤时间系统，快速开火/霰弹类武器不再因免伤帧丢命中 (→ Item.cs, Projectile.cs)
66	- High Velocity Bullet：伤害 10→11；弹幕穿透 2 次最多命中 3 敌；每穿透一敌下一次命中受 15% 伤害惩罚；免伤时间系统与 Meteor Shot 一致 (→ Item.cs, Projectile.cs)
67	- Crystal Bullet：撞击时只生成 2 个碎片（原 3 个）(→ Projectile.cs)
68	- Jester's Arrow：每穿透一敌下一次命中受 10% 伤害惩罚；Unholy Arrow：受 5% 伤害惩罚 (→ Projectile.cs)
69	
70	### 【物品与数值平衡 — 魔法武器】
71	
72	- Life Drain：伤害 30→35；未命中不消耗魔力（同 Medusa Head）(→ Item.cs)
73	- Nightglow：魔力消耗 26→23；弹幕会反弹 (→ Item.cs, Projectile.cs)
74	- Shadowbeam Staff：伤害 53→60，Use Time 16→15，每目标命中伤害减免 20%→10% (→ Item.cs, Projectile.cs)
75	- Unholy Trident：伤害 73→88；每穿透一敌下一次命中受 10% 伤害惩罚 (→ Item.cs, Projectile.cs)
76	- Poison Staff 射程约 30 格→37 格；Venom Staff 射程约 45 格→58 格 (→ Item.cs, Projectile.cs)
77	- Medusa Head：效果射程 +25% (→ Item.cs)
78	- Crystal Vile Shard / Nettle Burst / Wasp Gun：忽略至多 10 点敌人防御 (→ Projectile.cs)
79	- Razorblade Typhoon：同等魔力消耗与 Use Time 下每次只发 1 发弹幕（原 2 发），弹幕伤害 +50%（60→90）(→ Item.cs, Projectile.cs)
80	- Magical Harp：伤害 32→42，击退 0→0.25，魔力消耗 4→5；每穿透一敌下一次命中受 5% 伤害惩罚 (→ Item.cs, Projectile.cs)
81	- Blood Thorn：伤害 29→34；单个弹幕可命中 3 次（原 2 次）；重做免伤时间系统；Use Time 21→33 (→ Item.cs, Projectile.cs)
82	- Magic Missile：Use Time 18→22，魔力消耗 12→14；Flamelash：伤害 36→32，魔力消耗 18→21 (→ Item.cs)
83	- Flower of Fire：Use Time 20→16，魔力消耗 15→12；Space Gun：伤害 19→17，魔力消耗 7→6 (→ Item.cs)
84	- Charged Blaster Cannon：完全光束模式下可以瞄准光束 (→ Projectile.cs)
85	- Betsy's Wrath：伤害 65→110 (→ Item.cs)
86	- Stellar Tune：伤害 75→85 (→ Item.cs)
87	
88	### 【物品与数值平衡 — 召唤武器】
89	
90	- 鞭子多目标伤害惩罚下调：Cool Whip 33%→30%，Durendal 30%→20%，Morning Star 25%→5%，Dark Harvest 30%→10%，Kaleidoscope 15%→10% (→ Projectile.cs, Item.cs)
91	- 所有鞭子（Leather Whip 除外）射程提升：早期最少（Snapthorn 约 +10%），末期最大（约 +50%）(→ Projectile.cs)
92	- 鞭子现在可受益于 Flask 增益 (→ Projectile.cs, Player.cs)
93	- Leather Whip：Zoologist 处购买所需图鉴完成度 15%→10% (→ NPC.cs)
94	- Finch Staff：雀鸟命中目标更可靠（故意保留少量不准）；被击退的敌人几乎总是退向远离玩家方向 (→ Projectile.cs)
95	- Optic Staff：修正 Retinamini 激光未使用独立免伤计时器的 bug，减少免伤帧冲突 (→ Projectile.cs)
96	- Sanguine Staff：血蝠攻击速度 60→66（攻击路线耗时）(→ Projectile.cs)
97	- Xeno Staff：开火冷却 30→33（攻速约 -10%）；Tempest Staff：开火冷却 60→50（攻速约 +20%），Sharkron 弹速 14→20，风暴自身移速 +50% (→ Projectile.cs)
98	- Hornet Staff：伤害 9→11；Vampire Frog Staff：伤害 11→13，整个身体都能造成伤害（原只有舌头），修正未用独立免伤计时器的 bug (→ Item.cs, Projectile.cs)
99	- Pygmy Staff：弹速 12→18；触发投矛范围 +40% (→ Projectile.cs)
100	- Desert Tiger Staff：基础伤害 33→41；特殊攻击碰撞框增大减少落空 (→ Item.cs, Projectile.cs)
101	- Frost Hydra Staff：弹幕穿透 2 次最多 3 敌；每穿透一敌下一次命中受 15% 伤害惩罚 (→ Projectile.cs)
102	- Explosive Trap Staff：爆炸大小与检测范围 +50%；爆炸冷却 110→90；Huntress 套装/red Riding 套装（Hood）冷却分别 74→60、40→30 (→ Projectile.cs, Item.cs)
103	- Kaleidoscope：伤害 165→180 (→ Item.cs)
104	
105	### 【物品与数值平衡 — 盔甲】
106	
107	- Cactus armor：移除 1 防御套装奖励；新套装奖励：造成 15 点针刺伤害（Expert/Master 下 ×2/×3 为 30/45）(→ Item.cs, Player.cs)
108	- Mining armor：Mining Shirt/Pants 掉落率 2.4%→12% (→ ItemDropRules, Item.cs)
109	- Gladiator armor：头盔护腿防御 +1、胸甲 +2；新套装奖励：全套免疫击退；掉落率 1/20→1/7（随机一件）(→ Item.cs, ItemDropRules)
110	- Fossil armor：头盔护腿防御 2→4、其远程暴击 3%→4%；胸甲防御 4→5、3% 远程暴击替换为 5% 远程伤害 (→ Item.cs)
111	- Wizard Hat：魔法伤害 15%→5%，防御 2→4；Magic Hat：魔法伤害/暴击奖励 7→6 (→ Item.cs)
112	- Meteor armor：每件魔法伤害 7%→9%（总量 21%→27%）(→ Item.cs)
113	- Jungle armor（含 Ancient Cobalt armor）：帽/裤魔法暴击 4%→6%；衬衫 4% 魔法暴击替换为 6% 魔法伤害 (→ Item.cs)
114	- Necro armor：套装远程暴击 15%→10%；每件防御 +1（共 +3，含 Ancient Necro Helmet）(→ Item.cs)
115	- Obsidian armor：整套改为以鞭子为核心的召唤师盔甲；组件只能在 Hellforge 制作（需 Shadow Scale/Tissue Sample）；Obsidian Outlaw Hat +9% 召唤伤害、Obsidian Longcoat +1 仆从位、Obsidian Greaves +9% 召唤伤害；新套装奖励：鞭子射程与速度 +50%，再 +25% 召唤伤害（全套共 43%）(→ Item.cs, Recipe.cs, Player.cs)
116	- Molten armor：头盔 7% 近战暴击、胸甲 7% 近战伤害、护腿 7% 近战速度；17% 近战伤害套装奖励降为 10%（7% 移入胸甲）；新套装奖励：全套不会染上 On Fire (→ Item.cs, Player.cs)
117	- Cobalt armor：胸甲暴击 3%→5%；护腿防御 7→8、新增 3% 伤害；近战头盔防御 11→12、移速 7%→10%、12% 近战速度改为 15% 近战伤害；远程 Mask 暴击 6%→10%；魔法 Hat 新增 10% 魔法伤害 (→ Item.cs)
118	- Palladium armor：治疗套装奖励效力 6→4；Melee Mask 伤害 8%→12%；Magic Headgear 伤害 7%→9% (→ Item.cs, Player.cs)
119	- Mythril armor：链甲伤害 5%→7%；护腿暴击 3%→10%；近战头盔暴击 5%→8%；近战套装奖励 5%→10% 暴击 (→ Item.cs)
120	- Orichalcum armor：Melee Mask 伤害 7%→11%、暴击 7%→11% (→ Item.cs)
121	- Adamantite armor：胸甲伤害 6%→8%；护腿暴击 4%→7%；近战套装奖励 18%→20%；远程 Mask 暴击 8%→10%；魔法 Headgear 伤害 11%→12%、暴击 11%→12% (→ Item.cs)
122	- Titanium armor：Melee Mask 伤害/暴击/速度 8%→9% (→ Item.cs)
123	- Frost armor：套装奖励额外 +10% 近战/远程伤害；其 On Fire 特版改为 25 DPS（原 8）(→ Item.cs, BuffID.cs)
124	- Forbidden armor：Forbidden Robes +10% 召唤伤害；Forbidden Treads +10% 魔法伤害 (→ Item.cs)
125	- Chlorophyte armor：叶绿水晶射击冷却 50→40 (→ Item.cs, Projectile.cs)
126	- Spectre armor（Mask）：魔法伤害/暴击加成 5%→10%；套装爆发伤害上限 1000→1500；"恢复率" 250→400 (→ Item.cs, Player.cs)
127	- Spectre armor（Hood）：数值无变化；-40% 伤害惩罚从 Hood 移到套装奖励，重写 tooltip 使"以攻换疗"更清晰 (→ Item.cs, Player.cs)
128	- Crystal Assassin armor：头 -10% 魔力消耗、衣 -10% 弹药消耗、腿 +10% 近战速度；移除套装 15% 移速但靴子移速 10%→20%；新套装奖励：全套可冲刺（Dash）(→ Item.cs, Player.cs)
129	- Old One's Army 系列盔甲：Squire Greaves 近战暴击 20%→15%；Monk Pants 近战暴击 10%→15%；Huntress's Jerkin +10% 弹药减免；Apprentice Helmet +10% 魔法伤害；Valhalla Knight 头盔 +10% 近战伤害、护腿移速 30%→20%；Shinobi Infiltrator 裤移速 20%→30%、躯干 +5% 近战暴击；Red Riding 腿 +10% 远程暴击、裙 +20% 弹药减免；Dark Artist 腿 +20% 移速、袍 -15% 魔力消耗、5% 仆从/魔法伤害从袍移到帽 (→ Item.cs)
130	
131	### 【物品与数值平衡 — 饰品】
132	
133	- Band of Regeneration / Charm of Myths：恢复速度 0.5 生命/秒→1 生命/秒 (→ Item.cs, Player.cs)
134	- Band of Starpower / Panic Necklace：可在墓地区工匠作坊制作（与生命/魔力水晶互转），全世界更容易获得 (→ Recipe.cs)
135	- Bone Glove：完全重制为饰品；装备后攻击时每秒向光标射出交叉骨头，25 点无类型伤害并忽略至多 25 点防御；新增手部栏 vanity 外观 (→ Item.cs, Projectile.cs, Player.cs)
136	- Brain of Confusion：Cerebral Mindtrick 暴击奖励 20%→10%，持续时间 -1 秒 (→ Item.cs, BuffID.cs)
137	- Celestial Cuffs：获得组件的 +20 魔力奖励 (→ Item.cs)
138	- Diving Helmet 及其所有制品：呼吸容量加成 +50% (→ Item.cs, Player.cs)
139	- Feral Claws / Titan Glove："近战 autoswing"能力从 Titan Glove 转移到 Feral Claws；Titan Glove 新特性：合格近战武器大小 +10%（制品链继承，不叠加）(→ Item.cs, Player.cs)
140	- Lucky Horseshoe / Fledgling Wings：幸运马掌不再出现在空岛箱，改入地下金箱掉落表；稚翼之翼加入空岛箱与空岛匣 (→ ItemDropRules)
141	- Flesh Knuckles / Berserker's Glove：防御 7→8；Hero Shield：防御 7→10；Fire Gauntlet：伤害与近战速度 10%→12%，继承 Titan Glove 与 Magma Stone 新特性 (→ Item.cs)
142	- Honey Comb 系列（Bee Cloak、Honey Balloon、Stinger Necklace、Sweetheart Necklace）：蜜蜂基础伤害 7→13（配 Hive Pack 为 18）；Expert ×1.5、Master ×2；被击中时获得 5 秒蜂蜜增益 (→ Item.cs, Projectile.cs, BuffID.cs)
143	- Jellyfish Necklace 及制品：出水时散发光晕，水中大幅增亮 (→ Item.cs, Main.cs)
144	- Lava Charm：生成率翻倍，熔岩层箱/熔岩匣 1/20 几率 (→ ItemDropRules, WorldGen.cs)
145	- Magma Stone：特版 On Fire 4 DPS→15 DPS (→ Item.cs, BuffID.cs)
146	- Molten Quiver：木箭转火矢时正确给 +2 伤害（仅对木箭生效）(→ Item.cs, Player.cs)
147	- Obsidian Rose：熔岩伤害减免 30→45（适用所有制品，并纳入 Lava Waders/Hellfire Treads/Terraspark Boots）；熔岩伤害改用独立免伤计时器 (→ Item.cs, Player.cs)
148	- Panic Necklace / Sweetheart Necklace：Panic! 增益持续 5 秒→8 秒 (→ Item.cs, BuffID.cs)
149	- Pygmy Necklace：Witch Doctor 在 pre-Hardmode 即出售 (→ NPC.cs)
150	- Star Cloak / Bee Cloak / Star Veil / Mana Cloak：星星基础伤害 30→75，忽略至多 25 防御；Expert ×2、Master ×3；改用本地免伤帧，不干扰其他穿透弹幕 (→ Item.cs, Projectile.cs)
151	
152	### 【物品与数值平衡 — 工具与坐骑】
153	
154	- Reaver Shark：Use Time 18→13；Bone Pickaxe：掉落率 2%→5% (→ Item.cs, ItemDropRules)
155	- Chlorophyte Jackhammer：纳入钻头/链锯机制大改，速度提高、射程降低 (→ Item.cs, Projectile.cs)
156	- 钓鱼竿：Mechanic's Rod 钓力 30%→35%、机械师救出即售、多个月相有售；Fiberglass Fishing Pole 钓力 27%→30%、箱中几率 1/30→1/15；Scarab Fishing Rod 钓力 25%→30%；Sitting Duck's Fishing Pole 改为旅行商人只在骷髅王后出售 (→ Item.cs, NPC.cs)
157	- 生命法杖：Living Wood Wand / Leaf Wand 摇纯净森林树 1/300 掉落；Living Mahogany Wand / Rich Mahogany Leaf Wand 摇丛林树 1/200 掉落 (→ ItemDropRules, Player.cs)
158	- The Black Spot 坐骑：最高速度与加速度大幅降低（低于 UFO 坐骑）；不能靠 dash-骑乘直接达最高速 (→ Mount.cs, Item.cs)
159	- Scutlix 坐骑：攻击范围 500→850（性能折衷）；伤害 100→150 (→ Mount.cs, Item.cs)
160	- Dark Mage's Tome 坐骑：可像飞毯一样爬斜坡和 1 格高障碍 (→ Mount.cs)
161	- Witch's Broom 速度略增；Flamingo 坐骑最高速度 7.5→6；三种 pre-Hardmode 马鞍（Dusty Rawhide/Royal Gilded/Black Studded）最高速度 8→9 (→ Mount.cs, Item.cs)
162	- 光宠：Jewel of Light / Pumpkin Scented Candle 亮度约 +50%；Suspicious Looking Tentacle 亮度约 +33% (→ Item.cs, Main.cs)
163	
164	### 【物品与数值平衡 — 合成与掉落】
165	
166	- Blood Rain Bow / Chum Caster / Vampire Frog Staff：原为三选一各 1/8，改为各自独立 1/8 掉落（实际掉率 ×3）(→ ItemDropRules)
167	- Bloody Tear：标准血月怪 1/200→1/100；血月钓鱼怪 1/200→1/25；The Groom/The Bride 1/9→1/5；Dreadnautilus 1/9→1/2（Expert/Master 100%）(→ ItemDropRules)
168	- Sanguine Staff：Dreadnautilus 掉落 1/5→1/2（Expert/Master 100%）(→ ItemDropRules)
169	- Blade Staff：改由 Queen Slime 掉落（原附魔剑）(→ ItemDropRules)
170	- 风筝/纸飞机：Windy Balloon 风筝掉率 1/260→1/72；Paper Airplanes 3/260→1/72 且堆叠 1→2–5；Bone Serpent Kite 1/25→1/15 (→ ItemDropRules)
171	- Sturdy Fossil：Tomb Crawler 有几率掉少量；Basilisk 1/3→100%、数量 1→1–3；绿洲/幻象匣可开出 (→ ItemDropRules)
172	- Golden Lock Box：修正 Muramasa 掉率双倍问题；现在可开出 Valor (→ ItemDropRules)
173	- 火把：丛林火把配方更高效；身上火把少于 20 个时打罐更易掉火把 (→ Recipe.cs)
174	- Mana Crystal：配方从 3 颗坠落之星增加到 5 颗 (→ Recipe.cs)
175	- 早期矿石装备成本全面下调（铜/锡/铁/铅/银/钨/金/铂）：镐 12→10（铜锡 8）；斧 9→8（铜锡 6）；铜锡阔剑 8→6；短剑 7→6（铜锡 5）；锤 10→8；弓不变；铜/锡盔甲 15/25/20 锭→12/20/16；铁铅与银钨 20/30/25→15/25/20；金铂 25/35/30→20/30/25 (→ Recipe.cs)
176	- Hardmode 矿剑：钴/秘银剑 10→8 锭；钯金/山铜剑 12→10 锭 (→ Recipe.cs)
177	- Adamantite Bar / Titanium Bar：5 矿→4 矿，连带所有相关装备降价 (→ Recipe.cs)
178	- Jester's Arrow：每颗坠落之星产 20 支→10 支；Super Star Shooter：不再由旅行商人出售，改为 Star Cannon + 神圣锭制作 (→ Recipe.cs, Item.cs)
179	
180	### 【机制系统改动 — Buff/Debuff】
181	
182	- Frostburn：玩家版改为与敌人版一致，8 DPS (→ BuffID.cs, Player.cs)
183	- Cursed Inferno：纠正 1.4 的错误解读，敌人版现在正确造成 24 DPS（玩家承受仍为 12）(→ BuffID.cs, NPC.cs)
184	- Venom 更名 Acid Venom：纠正后正确造成 30 DPS（玩家承受 15）；免疫大改：免疫 Poison 的敌人不再必然免疫 Acid Venom，且它通常影响不死/石头/金属/有毒敌人 (→ BuffID.cs, NPC.cs)
185	- Ichor：防御减免 20→15 (→ BuffID.cs, NPC.cs)
186	- Oiled：不再使用单独的 On Fire 类 debuff，而是目标已有其中之一时直接 +25 DPS (→ BuffID.cs, NPC.cs)
187	- Thorns Potion：荆棘反伤从所受伤害 1/3→100%；Dryad's Blessing：20%→50% (→ Item.cs, BuffID.cs, Player.cs)
188	- 敌人 debuff 免疫大改（数百项）：总体让敌人更易受以前免疫的 debuff 影响；绝大多数免疫 Venom 的敌人不再免疫；大量石头/金属敌人不再免疫 Cursed Inferno；Cursed Inferno 与 Shadowflame 免疫解耦；幽灵类敌人（Wraith、Poltergeist 等）几乎免疫所有主要 debuff（含 Ichor，鞭子 debuff 除外）；南瓜月/星旋入侵等"全免疫"敌人改为按属性免疫；Destroyer 等有意全免疫者不再免疫鞭子 debuff；绝大多数免疫困惑的敌人维持免疫 (→ NPC.cs, Terraria.ID/BuffID.cs)
189	
190	### 【NPC与Boss与AI】
191	
192	- Vicious Goldfish：现在在猩红水中自然生成 (→ NPC.cs, Main.cs)
193	- Blood Feeder：生命 20→150，伤害 30→50，防御 4→20，掉钱 350→500 (→ NPC.cs)
194	- Ghost：生命 70→50，伤害 18→15，防御 8→4，击退易感性 40%→50% (→ NPC.cs)
195	- Antlion Larva：生命 45→35，伤害 12→10 (→ NPC.cs)
196	- Antlion Eggs：世界生成时更少（地下沙漠危险性略降）；会随时间缓慢再生（区域低于阈值才再生）(→ WorldGen.cs, TileID.cs)
197	- Rolling Cactus：巨石基础伤害降低约 1/3；仙人掌刺弹幕伤害 20→30 (→ Projectile.cs, NPC.cs)
198	- Angry Dandelion / Rock Golem：修正弹幕伤害被放大两倍的 bug (→ NPC.cs, Projectile.cs)
199	- Wall of Flesh：会让屏幕褪色为黑色；附近所有玩家死亡或无玩家时消失 (→ NPC.cs, Main.cs)
200	- Ice Elemental：弹幕攻击可造成 Frostburn (→ NPC.cs)
201	- Jungle Creeper：生命 120→400，防御 14→40，伤害 50→100；移速更快；攻击造成 Venom；Expert/Master 下喷网 (→ NPC.cs)
202	- Lac/Cyan/Cochineal Beetle：生命体分析仪稀有度 2→1 (→ NPC.cs, Main.cs)
203	- Phantasm Dragon：生命 4000→10000，头部防御 10→15，身体尾部防御 20→30，头部伤害 80→100，身体尾部伤害 40→50 (→ NPC.cs)
204	- Hoppin' Jack：Hardmode 全年可在墓地区生成 (→ NPC.cs)
205	- Vortex Lightning：星旋入侵期间两种闪电伤害均提升到 100 (→ Projectile.cs)
206	- Town Happiness 机制：喜欢/反感/喜爱/讨厌因素加减成提升 20%；不触发"拥挤"的城镇 NPC 数 3→4；城镇检测尺寸翻倍（1.4.1.2 会回调检测尺寸）(→ NPC.cs, Main.cs)
207	
208	### 【世界生成】
209	
210	- 世界生成会尝试避免 Corruption/Crimson 与 Jungle 重叠（不适用于 Hardmode 感染条带）(→ WorldGen.cs, GameContent/Biomes)
211	- Armed Zombie / Bone Skeleton Statue 现在任意世界难度都可能在世界生成中出现并正常工作 (→ WorldGen.cs)
212	- Shadow Chests 数量上限 7–10→10–15 (→ WorldGen.cs)
213	- Pyramid 放置几率 +50%；Enchanted Sword Shrine 生成几率翻倍（单次尝试 1/4→1/2）(→ WorldGen.cs, GameContent/Biomes)
214	- Sandstorm 频率：Hardmode ×2，pre-Hardmode ×1.33 (→ Main.cs)
215	- 修复丛林神社会阻止其东侧生成许多重要建筑（生命红木树、地下小屋等）(→ WorldGen.cs)
216	- 修正压力板生成在可破坏冰上漂浮、巨石陷阱嵌进神庙、罐子罕见出界、红木树不把丛林草视为丛林等问题 (→ WorldGen.cs)
217	
218	### 【渲染与视觉特效 — Vanity 系统大改】
219	
220	- 背部装备（背包、尾巴、翅膀、披风）不再互斥，四类各一件可同时显示（原一次只见一件）(→ Player.cs, Terraria.GameContent.Drawing/TileDrawing.cs)
221	- Combat Wrench 作为背部独立分类，无论其他背包如何总显示 (→ Player.cs)
222	- Angel Halo 像 Unicorn Horn 一样无视头部装备总可见 (→ Player.cs)
223	- 头部饰品细分多个子分组，可同时佩戴多个（眼睛栏 Blindfold/Spectre Goggles、花栏 Nature's Gift/Obsidian Rose、Ginger Beard 等）(→ Player.cs)
224	- 戴露脸帽子/头盔时可见 Blindfold；Diving Helmet 系列设为可见时覆盖头盔；Obsidian Skull 系列与露脸帽兼容并将脸替换为骷髅头；Ginger Beard 重画并兼容大多数头/脸饰品 (→ Player.cs)
225	- 盾/披风显示重做：盾绘制在披风"前面"，二者视觉上重新兼容；设为不可见的盾仍可染色，主动使用（克盾冲刺、狱火之刃格挡）时显示染色效果 (→ Player.cs)
226	- 玩家长发正确兼容翅膀/背包，显示全长不截断 (→ Player.cs)
227	- 各类奔跑靴（Sailfish/Flurry/Flower Boots 等）尾迹受 vanity 使用影响，可重排饰品栏或用社交栏选择 (→ Player.cs)
228	- 戴 Ultrabright Helmet 时可见头发；Bone Glove 手部新增视觉装饰 (→ Player.cs)
229	- Boss Mask 物品贴图更新；Orange/Amber Phasesaber 贴图更新 (→ Item.cs)
230	
231	### 【UI与界面】
232	
233	- Journey Mode 复制菜单大改：新增多个过滤器分解大类；其他选项更正确地包含不属于所有类别的物品 (→ Terraria.GameContent.UI, Main.cs)
234	- Bestiary 现在说明霜月/南瓜月掉落是否基于波数或特定波数后掉落 (→ Terraria.GameContent.UI)
235	- 连接服务器时显示加载 Tips (→ Terraria.GameContent.UI)
236	- 分辨率/全屏/无边框菜单设置重组为同一子菜单 (→ Terraria.GameContent.UI)
237	- 修正向导合成栏/哥布林重铸槽未正确链接玩家、天柱血条 Journey 难度切换时溢出、Quick Stack 不考虑已收藏钱币、Journey 滑块滑动中关闭会最大化、时间暂停时自发下雨/入侵宣告、boss 小地图图标不随方向改变等 (→ Terraria.GameContent.UI, Main.cs)
238	
239	### 【音频】
240	
241	- 打雷音量改用环境音效设置调整 (→ Terraria/Audio)
242	- Torch God 相应设置开启时播放异界版曲子；音乐音量为 0 时音乐盒不再播放 (→ Terraria/Audio)
243	- 修正音轨用 60% 而非 100% 质量压缩的问题（地下沙漠曲最明显）；修正火星人大量 SFX 问题 (→ Terraria/Audio)
244	
245	### 【机制系统改动 — 其他】
246	
247	- 墓地阈值：触发各级墓地氛围所需墓碑数量 +1 (→ Main.cs, Player.cs)
248	- Block Swap 与坠落块：可对最顶一块沙/坠落块换块；镐力足够（钴及以上）可自由对任何坠落块换块 (→ Player.cs, Main.cs)
249	- Meteorite 矿：Hardmode 后可被爆炸物破坏（原免疫）(→ Main.cs, TileID.cs)
250	- 常规橙色蘑菇：药水病时长 60 秒→30 秒 (→ Item.cs, Player.cs)
251	- 钓鱼：移除高钓力时的收益递减 (→ Projectile.cs, Player.cs)
252	- 晶塔（Pylons）：星旋入侵期间可用晶塔传送（Moon Lord 与其他入侵/Boss 战仍不可用）(→ Main.cs, Player.cs)
253	- Journey Mode 开局自带基础抓钩 (→ Player.cs)
254	- 摇树获取掉落物次数上限 200→500/天 (→ Player.cs)
255	- 特殊家具制作站：蒸汽朋克人在对应生物群落出售大多数特殊制作站（雪地=制冰机、太空=天磨等）；Bone Welder 在墓地区出售；带生命木法杖时出售 Living Loom；邪恶世界两种邪恶制作站可用暗影之魂在墓地区互转 (→ NPC.cs, Recipe.cs)
256	- Bestiary：有独立图鉴的 Boss 仆从在打败对应 Boss 后完全解锁；Dark Mage 和 Ogre 只需打败一次即完全解锁 (→ Terraria.GameContent.UI)
257	- 平台层：SteelSeries 外设 RGB、FNA 更新、全语言本地化（复刻可忽略）
258	
259	### 【多人/网络】
260	
261	- 修正 Queen Slime 同步问题（多人冲锋/传送不稳）、Big Mimic 同步、多人只伤双子之一时宝藏袋不掉、Flying Dutchman 失同步/自发死亡、Moon Lord 某攻击多人中异常、水晶碎片多人放置同步错误（变明胶水晶）、木人模特/帽架多人被炸坏、世界最右边缘出生点不工作等 (→ NPC.cs, Main.cs, MessageBuffer/Netplay)
262	- 服务器：独立服务器生成世界不遵循名称/种子长度限制、不能用特殊种子、生成的世界偶尔损坏；最大玩家数可设超 255 或低于 1；"Liquid Spam"改为正确计数后才踢人；玩家不捡物品时服务器无限塞物品 (→ NetMessage/Netplay)
263	
264	### 【Bug修复-影响玩法逻辑的】
265	
266	- 纯崩溃/平台类（滚动备份删除、地图图标崩溃、坐骑动画罕见崩溃、剪贴板崩溃、云端存档同步、分辨率上限、关闭挂起、Mac 主机崩溃、Linux 截图）归并一句：修复大量崩溃与 Mac/Linux 平台问题。
267	- NPC/Boss：白天击杀光之女皇不掉 Terraprisma；克苏鲁之眼/双子转二阶段有几率永远旋转；拜月教邪教徒与火星飞碟目标离开/死亡不寻找新目标；Antlion Swarmer 掉 10 倍金钱笔误；Angry Nimbus 无法穿平台；打败史莱姆皇后双倍提升城镇 NPC 能力而光之女皇完全不提升；漂浮类敌人（Pixies、Wraiths 等）无法上下穿平台；地表木质 Mimic 不再自然生成；旧日军团 2 级哥布林投弹手造成 1 级伤害；史莱姆雨无视 Journey 生成滑块；Devourer 身体/尾巴击杀不计旗帜计数；挖掘中的松露虫不显示在生命体分析仪；Hemogoblin Shark 穿平台掉落；蜘蛛行走动画帧不全；Golem 部位生成外观古怪；Moon Lord 不再使用 NPC 平滑设置；Torch God 双倍计数/死亡不失去进度；腐化/猩红无效房屋只说"无效"；Angry Dandelion 多人瞄错玩家；时间暂停时旅行商人生成；海洋小动物屏幕内生成 (→ NPC.cs, Main.cs, Projectile.cs)
268	- 战斗/物品使用：鞭子大小词缀反向影响速度；Blood Arrow 不被视为远程（不暴击）；沙漠之虎突袭被算作魔法攻击（不触发鞭子 debuff）；高尔夫球车撞击不随仆从伤害缩放；马坐骑撞击错误随近战伤害缩放；Expert/Master 服务器幸运币掉钱；Terraprisma 传送远处返回慢；钛金远程套未公开的不耗弹药几率；Bat Scepter/Bee Gun 不瞄准猪鲨；黄蜂/小鬼/风暴/UFO/星尘细胞仆从不造成击退；沙滩球无速度上限；Life Drain 命中检测；Celestial Starboard 飞行时大幅缩短冲刺距离；雪地传送到非雪地水中染 Chilled；雪人集群碎片不造成伤害/不破坏图格；躲闪掉的攻击仍上 debuff；Magic Missile 类液体中穿墙；背包满时捕成组鱼（炸弹鱼/霜匕首鱼）删除原物品组；Journey/Expert 模式 debuff 时间未正确倍增；Dart Pistol 两个可能的 Deadly 词缀；Sanguine Staff/Terraprisma 不正确使用召唤锁定；Golden Lock Box 中 Valor 不正确掉落 (→ Item.cs, Projectile.cs, Player.cs, NPC.cs)
269	- 图格/方块：竹子与熟铁栅栏不允许树木生长；沙子相关欺骗行为；Block Swap 悬停 Logic Sensors 可能破坏它们；环境改造不转化恶性蘑菇；邪恶荆棘世界生成后停止生长；珊瑚/贝壳在被致动块上重新长出；恶魔祭坛可能生成在滚球仙人掌上；绳不再与平滑大理石块融合；丛林/蘑菇藤蔓地下不生长；多人移除武器架；制作抓钩会暂时允许手动使用；坠落块穿过的平台失去斜坡状态；不能在硬核玩家幽灵背后放置图格；沙子图格形式坠落时偶尔复制；蓝色传送门站上使用彩纸会发射彩纸；压力板生成在可破坏冰上；巨石陷阱嵌进神庙；无法从各种梁向外延伸建造；石平台免疫熔岩；泥土炸弹不让埋住的草死亡；晶塔 NPC 检测只查住房旗号；智能光标药草放置不一致 (→ Main.cs, WorldGen.cs, TileID.cs, Player.cs)
270	- 视觉/美术（择要）：Mac/Linux 能看到顶点着色器尾迹（Zenith、Terraprisma、Magic Missile）；披风与税官西装坐下时正确隐藏；沙漠之虎突袭不用召唤染料；矿车尘土用错染料槽；死亡后仍显示翅膀；反向重力身体部位位置错误；部分图格忽略光照涂料；暂停时星尘守卫停止攻击动画 (→ Terraria.GameContent.Drawing/TileDrawing.cs, Main.cs, Player.cs)
271	
272	---
273	
274	## 二、版本 1.4.1.1（修补程序，2020-10-14）
275	
276	> 以 1.4.1 的 bug 修复为主。纯崩溃类（Mac 多人主机崩溃、手柄房屋菜单崩溃、Linux 截图失败）归并一句：修复了 Mac/Linux 多处崩溃与截图问题。
277	
278	### 【机制系统改动】
279	
280	- 修正 "Leading Landlord" 成就所需 NPC 快乐度获得难度高于预期的问题 (→ Terraria.GameContent.UI, NPC.cs)
281	- Moon Lord：眼睛闭上时，插在眼中的 Daybreak 长矛会立即爆炸并造成额外伤害 (→ Projectile.cs, NPC.cs)
282	- 修正 Dungeon 代码中导致同一种子每次生成世界不同的问题 (→ WorldGen.cs)
283	- Master 模式玩家用手柄时无法使用全部饰品栏 (→ Terraria.GameContent.UI, Player.cs)
284	
285	### 【NPC与Boss与AI】
286	
287	- Princess：修正不能正确检测附近 NPC 的问题（邻居簇拥她也觉得孤独）；修正关于 Santa Claus 的一条对话；变身后的 Zoologist 关于 Princess 的一条对话 (→ NPC.cs)
288	- Town NPC 会试图坐在 Dynasty Chair 上（应当无法坐上去）(→ NPC.cs)
289	
290	### 【物品与数值平衡】
291	
292	- 修正 Jungle Armor、Ancient Cobalt armor、Molten Armor 套装未拥有正确套装奖励、反而由 Band of Regeneration 等其他物品获得的问题 (→ Item.cs, Player.cs)
293	- Bone Glove：修正无法通过背包内右键点击装备、必须手动装备的问题 (→ Item.cs, Player.cs)
294	
295	### 【渲染与视觉特效】
296	
297	- 变身为 Werewolf/Merman（Celestial Shell）的玩家不再因佩戴某些饰品而拥有人脸 (→ Player.cs)
298	- Video Visage 显示在地图上时未给屏幕部分应用染料 (→ Terraria.GameContent.Drawing/TileDrawing.cs)
299	- Witch Costume 未能正确显示其下双腿 (→ Player.cs)
300	- 修正 Game Credits 中的疏漏 (→ Terraria.GameContent.UI)
301	
302	### 【其他】
303	
304	- 任意液体中钓鱼都会解锁 "Hot Reels!" 成就的 bug (→ Terraria.GameContent.UI)
305	- 修正汉字键会自动替换某些键位绑定的问题 (→ Terraria.GameContent.UI)
306	- 修正重命名箱子时玩家无法轻松关闭背包的问题 (→ Terraria.GameContent.UI)
307	- NPC 对话、物品 tooltip/背景文本的若干语法/拼写问题（本地化资源）
308	
309	---
310	
311	## 三、版本 1.4.1.2（修补程序，2020-11-10）
312	
313	### 【新增内容】
314	
315	- 无新增游戏内容；本地化内容补齐（1.4.1 内容全部翻译入包，并修正 1.4 中文本地化无法正确加入游戏的问题）。
316	
317	### 【机制系统改动】
318	
319	- 还原 Town NPC 住房/村庄检查距离：1.4.1 中曾翻倍，现回到 1.4 水平 (→ NPC.cs, Main.cs)
320	- NPC 快乐度：3 个 NPC 的城镇现在给予"Space（空间）"奖励（之前既无奖励也无惩罚）(→ NPC.cs)
321	- Skeletron Prime 的炸弹现在会在种植箱（Planter Boxes）上爆炸（类似此前对平台的改动）(→ Projectile.cs, TileID.cs)
322	- Queen Slime 的仆从现在以正常掉落率掉落 Slime Staff (→ ItemDropRules)
323	- 坐着或骑坐骑时也显示披风（此前因冲突受限）(→ Player.cs)
324	- Journey/图鉴菜单任意位置点击会暂停搜索 (→ Terraria.GameContent.UI)
325	- Timeless Traveler 套装贴图更新为正确版本；Spectre Goggles 不再完全覆盖头盔 (→ Item.cs, Player.cs)
326	
327	### 【物品与数值平衡 — 对 1.4.1 的回调与二次调整】
328	
329	- Brand of the Inferno：Use Time 25→20 (→ Item.cs)
330	- Chlorophyte Claymore：伤害 80→95；Chlorophyte Saber：伤害 48→57 (→ Item.cs)
331	- Christmas Tree Sword：弹幕造成 75% 基础伤害（原 50%）(→ Projectile.cs)
332	- Super Star Shooter：Use Time 12→18，伤害 70→60（因免伤帧机制实际总伤更一致，官方称实际为强化）(→ Item.cs, Projectile.cs)
333	- Betsy's Wrath：部分还原 1.4.1 强化，伤害 110→100 (→ Item.cs)
334	- Hornet Staff：伤害 11→12（在 1.4.1 从 9→11 基础上）；Vampire Frog Staff：还原 1.4.1 强化，伤害 13→11（AI/功能改动已足够）(→ Item.cs)
335	- Imp Staff：小鬼攻击的敌人免伤帧 10→6；Optic Staff：Spazmamini/Retinamini 免伤帧 16→12，Spazmamini 追敌移速提高 (→ Projectile.cs)
336	- Spider Staff：召唤蜘蛛改为按顺序系统性轮换种类而非随机（免伤帧机制下伤害更一致，最大潜力不变）(→ Projectile.cs)
337	- Obsidian armor：头盔/护腿仆从伤害 9%→8%/件；套装奖励仆从伤害 25%→15%；鞭速 50%→35% (→ Item.cs)
338	- Deadly Sphere Staff：攻击免伤帧 10→8 (→ Projectile.cs)
339	- Firecracker：爆炸伤害 3 倍仆从基础伤害→2.75 倍 (→ Projectile.cs)
340	- Cool Whip：命中时短时间造成 Frostburn；雪花仆从移速 +50% (→ Projectile.cs, BuffID.cs)
341	- Desert Tiger：目标在空中时会"反弹至"目标，维持更牢固锁定；每扩展一个仆从位的伤害缩放 33%→40% 基础伤害 (→ Projectile.cs)
342	- Rainbow Crystal Staff：部分还原 1.4 的伤害下调，伤害 80→130 (→ Item.cs)
343	- Celestial Starboard：操作手感调整，保留完整冲刺距离修正 (→ Item.cs, Player.cs)
344	- Star Cloak：只在受到来自敌人源的伤害时才产生星星 (→ Item.cs, Player.cs)
345	- Black Spot 坐骑：加速度略升，略为抵消 1.4.1 的总速度损失 (→ Mount.cs)
346	- Chlorophyte Bar：配方 6 矿→5 矿；Chlorophyte Bullet：每锭 70 发→60 发 (→ Recipe.cs)
347	- 未说明更改："Gypsy Robe" 更名为 "Mystic Robe" (→ Item.cs)
348	
349	### 【NPC与Boss与AI — 敌人 debuff 免疫调整】
350	
351	- Snow Flinx、Wall of Flesh：移除对 Poisoned 的免疫 (→ NPC.cs, BuffID.cs)
352	- Queen Bee、Mourning Wood、Twins、Martian Probe、Old One's Skeleton：新增对 Poisoned 的免疫 (→ NPC.cs)
353	- Granite Golem / Granite Elemental、Betsy：新增对 On Fire!/Hellfire 的免疫 (→ NPC.cs)
354	- Frozen Zombie：新增对 Frostburn 的免疫；Clinger：新增对 Cursed Inferno 的免疫 (→ NPC.cs)
355	
356	### 【Bug修复-影响玩法逻辑的】
357	
358	- 纯崩溃类（音乐音量无法提高到 0% 以上及关联启动崩溃、Credits 贴图包崩溃、Prismatic Lacewing 贴图致 Linux 严重问题、Clinger Staff 反向重力世界顶部崩溃等）归并一句。
359	- 快乐度值被严重向下取整，消除微小差异并使阈值更难达成；只有 1 个 NPC 时拥挤惩罚与 3 个 NPC 一样 (→ NPC.cs)
360	- Life Drain 在 PVP 中使用不消耗魔力 (→ Item.cs, Player.cs)
361	- Town NPC 夜间不传送进入过高/瘦房屋或椅子上方空间不足的房屋；Town NPC 仅当敌人可作为目标时才对其开火（不再对 Plantera Hook 之类开火）；NPC 和猫夜间可能坐在同一座位 (→ NPC.cs)
362	- 碎裂地牢砖同步问题（应能解决地牢中敌人传送）(→ Main.cs, TileID.cs)
363	- Journey 模式提高时间速率会让主菜单 Credits 跑得特别快；Credits 暂停时也滚动 (→ Terraria.GameContent.UI)
364	- Ronin set（Wandering set）女性角色不显示萤火虫；某些情况下（如部分光宠）玩家皮肤过亮；Reaper Hood 头部贴图一帧偏移；Robot Shirt 与手部/腰带饰品不兼容、Pumpkin Shirt 与腰带饰品不兼容 (→ Player.cs, Item.cs)
365	- Video Visage 屏幕反向重力时偏移；某些 vanity 耳朵坐下时背后耳朵位置错误；坐下时尾巴饰品高度不正确、某些发型"双重绘制"、骑坐骑时高帽子视觉问题 (→ Player.cs)
366	- Bamboo Lantern 视觉分帧；Stardust Guardian 染色后不再透明；某些小动物在水下超级跳；虚荣火箭靴尾迹优先级不一致 (→ Terraria.GameContent.Drawing/TileDrawing.cs, Projectile.cs, Player.cs)
367	- Bone 仍被标记为弹药；Luminite 钻头/链锯取得不该取得的词缀；Jousting Lance 不再获得近战速度词缀；Old One's Army 盔甲属性与 tooltip 不一致；Hero Shield 未带来仇恨（aggro）加成；Sky Dragon's Fury 落地无动画、二次火焰不造成 Flask debuff；瓶中魂缺动画帧；发型 6/94 与披风冲突 (→ Item.cs, Projectile.cs, Player.cs)
368	- 强行传送其他玩家的漏洞（多人/网络）(→ Main.cs, NetMessage)
369	- 成就菜单不自动暂停；手柄 Master Mode 栏位可见性切换不工作；手柄/WASD 在角色难度模式中循环滚动方向反向 (→ Terraria.GameContent.UI)
370	- Adamantite/Titanium 矿锭制作花费变动带来的卖出价不一致；Paper Airplane 弹幕未被视为远程、不正确并堆；Molotov Cocktail 未获得霜甲 Frostburn；Coin Gun 不优先使用钱币栏 (→ Item.cs, Projectile.cs, Player.cs)
371	- 某些头盔反向重力时小地图绘制错误；某些叶贴图不能正确处理油漆 (→ Terraria.GameContent.Drawing/TileDrawing.cs)
372	- Brain of Cthulhu 没有足够空间传送时会消失 (→ NPC.cs)
373	- 部分物品掉落率未正确受 luck 影响（多为 Old One's Army 掉落，对实际掉率影响不大）(→ ItemDropRules)
374	- 除普通沙外大多数坠落图格弹幕会穿过平台，现在除敌对沙球外全部落在平台上 (→ Projectile.cs)
375	- 蜂巢、兔子炮、蚁狮蛋相关漏洞/疏忽；敌对蜜蜂会攻击神秘石碑等无敌敌人 (→ Item.cs, Projectile.cs, NPC.cs)
376	- 大纹理物品聊天中被缩小两次 (→ Terraria.GameContent.UI)
377	- 某些贴图大小未更新导致外观贴图的 texture packs 无法工作 (→ Main.cs)
378	
379	---
380	
381	## 四、本版本改动规模评估
382	
383	### 涉及独立系统数量
384	
385	1.4.1 系列合计涉及约 20 个独立系统：物品数值（近战/远程/魔法/召唤四大类全覆盖）、盔甲套装（30+ 套）、饰品、合成配方、掉落表、Buff/Debuff 体系（含敌人 debuff 免疫数百项的系统性重排）、召唤/仆从 AI 与免伤帧机制、敌人与 Boss 数值/AI、坐骑、钓鱼、城镇快乐度、墓地生物群落、世界生成（结构放置率/生物群落避让）、Vanity 渲染分层（背部/头部饰品分组）、Journey 模式 UI、Credits/音频、图格与坠落块机制、多人同步、成就与图鉴。
386	
387	### 复刻项目必须跟进的核心改动
388	
389	1. 免伤帧（immune frame）与穿透惩罚体系：大量弹药/仆从改为"每穿透一敌下一次命中伤害惩罚 X%"并使用独立/本地免伤计时器（Meteor Shot、High Velocity Bullet、Frost Hydra、星星、蜜蜂，以及 Imp 10→6、Optic 16→12、Deadly Sphere 10→8 等具体免伤帧数字）。这是 Projectile 命中逻辑的底层机制，复刻若不做会导致召唤与穿透武器手感完全不对。(→ Terraria/Projectile.cs, Terraria/Player.cs)
390	2. 敌人 debuff 免疫大改 + Venom→Acid Venom 重命名：数百项 NPC 免疫标志变化、Cursed Inferno/Venom 的 DPS 纠错（24/30）、Ichor 减防 20→15、Oiled 机制重做、1.4.1.2 又加了约 10 个敌人的具体免疫调整。数据驱动 NPC 的 debuffImmune 表必须按 1.4.1.2 后版本重建。(→ Terraria/NPC.cs, Terraria.ID/BuffID.cs)
391	3. 物品数值全量刷新：本系列是 1.4.x 中最大的平衡性补丁，Item.SetDefaults 中几乎全部近战/远程/魔法武器、30+ 套盔甲、大量饰品数值都变了（Terra Blade 95→115/UT14、Arkhalis 20→25、Betsy's Wrath 65→110 后回调至 100 等）。若复刻目标为 1.4.5.6，直接以 1.4.1.2 后的数值表为准即可，不必逐步还原中间态。(→ Terraria/Item.cs, Terraria.ID/ItemID.cs)
392	4. 配方与掉落表大改：Terra Blade 合成线重构（真剑不再需要 Broken Hero Sword）、Adamantite/Titanium 锭 5→4 矿（1.4.1.2 又调叶绿锭 6→5）、早期矿装全面降价、Mana Crystal 3→5 星、Super Star Shooter/Blade Staff/Lucky Horseshoe 等来源变更、Bloody Tear/Sanguine Staff 掉率提升。(→ Terraria/Recipe.cs, Terraria.GameContent/ItemDropRules)
393	5. Princess NPC + 早期召唤内容：新城镇 NPC 公主（及其快乐度关系网）、Flinx Fur Coat/Flinx Staff、Spinal Tap、Lavaproof Tackle Bag。1.4.5.6 的 NPC 生成与快乐度计算依赖她。(→ Terraria/NPC.cs, Terraria.ID/NPCID.cs)
394	6. Vanity 渲染分组：背部四类（背包/尾巴/翅膀/披风）同时显示、头部饰品子分组、盾绘制在披风之前、坐下/骑乘时显示披风。玩家绘制管线需要对应的分层/兼容性矩阵。(→ Terraria/Player.cs, Terraria.GameContent.Drawing/TileDrawing.cs)
395	7. Town Happiness 参数（两连改）：1.4.1 加减成 ×1.2、拥挤阈值 3→4、检测距离翻倍；1.4.1.2 又把检测距离还原、给 3 NPC 城镇加空间奖励。快乐度公式必须按 1.4.1.2 后的最终态实现。(→ Terraria/NPC.cs, Terraria/Main.cs)
396	8. 世界生成参数微调：地牢种子确定性修复（1.4.1.1，WorldGen 种子消费顺序）、金字塔 +50%、附魔剑神龛 1/4→1/2、暗影箱 7-10→10-15、邪恶生物群落避让丛林、丛林神社东侧建筑 bug。105 pass 管线需按此校对。(→ Terraria/WorldGen.cs)
397	
398	### 一句话总评
399	
400	1.4.1 是"平衡性大补丁"：以数百项物品/敌人数值调整和 debuff 免疫体系重排为主体，附带公主 NPC、早期召唤装备等少量新内容；1.4.1.1/1.4.1.2 是纯修补程序，1.4.1.2 还对 1.4.1 的过量强化做了一轮回调（含快乐度参数两连改），复刻应以 1.4.1.2 之后的最终数值为准。
401	

```


---

## 👤 User(sidechain) · 2026-08-09T11:41:02.278Z

**📎 ToolResult**

```
Version 1.4.1 Changes -------------------------------------------------------------------------------------------

I. Terraria 1.4.1 New Content and Content Changes:

A. New Content and Changes
	Added the winners of the Terraria Vanity Contest:
		Plaguebringer
		Wandering Ronin
		The Timeless Traveler
		Floret Protector
		Capricorn
		Bonus winner: TV Head!
		All six of these are craftable with pre-Hardmode materials of various sorts, so that all players can experience these awesome vanity sets! Thanks to everyone who participated and voted in the Vanity contest, and especially to our winners!
	Added new Achievements
	Added a credit sequence and music track following Moon Lord's defeat for the first time. This can also be accessed from the main menu.
	Music Box (Journey's End) is now created by recording the Credits music sequence. Additionally, using it in a normal accessory slot will play the Credits in-game, while using it in a social slot will only play the music.
	Added a new Princess NPC, with a variety of related items (and a new hairstyle!)
	Added new early game Summon equipment: Flinx Fur Coat and the Flinx Staff!
	Added a new pre-Hardmode whip, craftable at Dungeon-tier
	Added a Lavaproof Fishing Hook + Angler Tackle Bag Tinker
	Bee Hives and Antlion Eggs can now be crafted and placed
	Added a "Rainbow Cursor" vanity accessory

B. Vanity Accessory Changes
	Ultrabright Helmet now supports visible hair when worn
	Armors and vanity items which draw on the back (backpacks, tails, wings, and capes) are now no longer mutually exclusive. This means that you can now have one of any of those four categories all displaying at the same time. Previously, only one of those could ever be visible at a time (for instance, if you had visible wings, you could not ever see a cape, backpack, or tail).
	Combat Wrench now displays on the player regardless of what other backpacks are currently shown (it is its own category of back-draw)
	Angel Halo now functions like Unicorn Horn, in that it will be visible regardless of any other head equipment or vanity that is equipped
	Accessories which draw on the head have also been split into several subgroups, which will allow several of them to be worn simultaneously. For example, Blindfold/Spectre Goggles in the eye slot, Nature's Gift/Obsidian Rose in the "flower" slot and Ginger Beard.
	Blindfold can now be visibly seen when wearing hats/helmets which show the face
	Wearing Diving Helmet-series accessories set to visible will override your helmet, allowing them to be seen instead of your helmet
	Obsidian Skull-series accessories that are set to visible are now compatible with hats/helmets that show the face, as it will replace your face with the skull. Due to the shape of the Skull not fitting standard "Terrarian face" shapes, on certain helmets, it will use a different sprite with a more standard layout. You can also wear virtually all physically compatible Head/Face accessories with the Obsidian Skull as well.
	Ginger Beard has been resprited, and if set to visible, is now compatible with hats/helmets that show the face. It is also now compatible with most other Head/Face accessories.
	Reworked Shield/Cape display so that Shields and Capes are now visually compatible with each other again. The Shield now draws "in front" of the Cape, instead of underneath of it, which led to many of the initial issues.
	Shields which are set to not be visible can still be dyed, and will show that dye when actively used (such as Shield of Cthulhu dash or Brand of the Inferno Block). Previously, if they were set to invisible, their active use version would never have dye.
	Long-player hair is now properly compatible with wings/backpacks, and will show the full length of the hair without being cut-off visually
	The special trails left by various types of running boots (Sailfish, Flurry, Flower, etc) are now also subject to vanity usage, and you can use the one you prefer either through re-ordering accessories or using the social slots
	Bone Glove now has visual vanity for the hand slot

C. Other Content/Design Changes
	The Journey Mode duplication menu has been overhauled, with the addition of several new filters to break up some of the larger categories
	Additionally, the Misc option in the duplication menu should more properly encompass items that do not fall under any other category
	Made minor updates to Boss Mask item sprites to match the mask sprites
	Sprite update for Orange/Amber Phasesaber
	Torch God now plays an Otherworldly track when that setting is toggled
	Bestiary now indicates if a drop is Wave-based/if it only drops after a certain wave in Frost Moon and Pumpkin Moon
	Loading Tips now appear when connecting to a server
	Thunder volume is now adjusted with the Ambient SFX settings rather than regular Sound settings (edited)
	Plantero's Sombrero has made its triumphant return
	Reorganized menu settings for resolution/fullscreen/windowed borderless to all use the same sub-menu, to reduce confusion
	Updated FNA (Mac/Linux related)
	Added RGB support for SteelSeries game peripherals
	Adding updated localization for all languages up to 1.4 (some 1.4.1 content may still be untranslated, and these translations will come in an upcoming hotfix)

II. Terraria 1.4.1 Bug Fixes:

A. Major Issues and Crashes
	Rolling backups should properly fully delete extra files, instead of putting them in the recycle bin
	Fixed an extensive issue relating to Jungle Shrines which causes many other important structures to not generate properly to the east of them, including Living Mahogany Trees and Underground Cabins
	Fixed an issue where player map icons would sometimes cause a crash
	Fixed a rare crash issue relating to mount idle animations
	Fixed some Peripheral lighting related issues, particularly when closing the game
	Fixed an issue where Mac/Linux could not set resolution above 1900x1200
	Fixed the game sometimes indefinitely hanging after closing the game (preventing it from being launched again)
	Fixed a crash that occurred when other programs would prevent Terraria from copying to clipboard
	Fixed an issue that prevented map data from properly syncing with Cloud saving, so maps should reliably update via Cloud Save now

B. Enemy/NPC Bugs
	Fixed an issue with NPCs deciding to stand in escapable water until they drowned
	Fixed an issue where valid day-time completions of Empress of Light would not drop Terraprisma under specific circumstances
	Fixed a rare issue where Eye of Cthulhu, Retinazer, and Spazmatism had a chance to spin forever when changing to their second form
	Fixed an issue where Lunatic Cultist and Martian Saucer would not properly attempt to find a new target if his current target left or died
	Fixed an typo causing Antlion Swarmers to drop 10x too much money
	Fixed an issue where Angry Nimbus could not pass through platforms properly
	Fixed an issue where defeating Queen Slime boosted the power of Town NPCs twice as much as intended, while Empress did not boost them at all
	Fixed an issue where floating enemies (Pixies, Wraiths, Dripplers, Ice Elementals, etc) could not fall through platforms or float up through platforms properly to reach the player
	Fixed an issue where surface wooden Mimics were not capable of spawning naturally anymore
	Fixed an issue where the OOA Tier 2 Goblin Bombers did the damage of Tier 1 Goblin Bombers
	Fixed an issue where Slime Rain slimes would spawn regardless of the Journey mode spawn slider
	Fixed an issue where Flying Dutchman would desync and behave oddly or die spontaneously
	Fixed a syncing issue with Big Mimics that would result in erratic behavior in Multiplayer
	Fixed an issue where Devourer kills on the body or tail didn't count towards banners
	Fixed an issue where "Digging" Truffle Worms no longer appeared on the Lifeform Analyzer
	Fixed an issue where the last Twins to die might not drop their boss bag if you only damaged the other one in multiplayer
	Fixed an issue where Hemogoblin Sharks fall through platforms the player is standing on, failing to walk on them normally
	Fixed some issues with some spider enemies not using all of their animation frames when walking, resulting in stuttering movement
	Fixed an issue where Golem's body parts would appear oddly when spawned if you had too many enemies alive at once
	Moon Lord no longer uses the NPC Smoothing setting to prevent several issues
	Fixed an issue where Torch God would "count torches twice" resulting in the sequence happening too early
	Fixed an issue where Torch God would not lose progress if the player died
	Fixed an issue where some Corruption-invalidated housing would just say "invalid" rather than indicating it was due to Corruption/Crimson
	Fixed some issues with Angry Dandelions targeting the wrong player in MP
	Fixed an issue with Traveling Merchant spawning when time was paused with Journey powers
	Fixed an issue where Ocean critters were spawning on screen
	Fixed an issue where one of Moon Lord's attacks didn't properly attack or move in multiplayer

C. Combat, Gameplay, and Item Usage Bugs
	Fixed an issue where size modifiers on Whips had an inverse effect on speed, meaning big whips were always slow and small whips were always fast
	Fixed Blood Arrows not being considered ranged projectiles (which prevented them from dealing criticals)
	Fixed an issue where Desert Tiger pounce was flagged as a magic attack instead of summon, preventing it from activating Whip debuffs
	Fixed an issue where Golf Cart impact damage did not scale with minion damage like other charging mounts
	Fixed an issue where Horse-type mount impact damage scaled with melee damage instead of minion damage
	Fixed an issue where Lucky Coin money drops on Expert/Master servers would not drop properly
	Fixed an issue where Terraprisma would take too long to return when teleporting far away
	Fixed an issue where Titanium ranged set had an unlisted chance not to consume ammo (it was not meant to have that bonus at all)
	Fixed an issue where certain homing projectiles (Bat Scepter, Bee Gun) would not target Duke Fishron
	Fixed an issue where Hornet, Imp, Tempest, UFO, and Stardust Cell minions did not inflict knockback
	Fixed an issue where Beach Balls had no real movement speed limit, resulting in them getting yeeted like Team Rocket if you hit them with Zenith, never to be seen again
	Fixed some syncing issues with Queen Bee that resulted in erratic charging/teleportation in multiplayer
	Fixed Zenith not having full screen range on Gamepad
	Fixed some hit detection issues with Life Drain
	Fixed an issue where Celestial Starboard would dramatically reduce the distance of dashes used while flying
	Fixed an issue where teleporting from the Snow biome into non-Snow Biome water would inflict Chilled in Expert/Master mode
	Fixed an issue where Snowman Cluster Fragments did not dealing damage or breaking tiles
	Fixed a number of attacks and items that had extreme range, usually due to Golf Ball camera
	Fixed some issues stemming from right-clicking Weapon Racks/Item Frames/Food Platters while actively using the item you were trying to place
	Fixed an issue where the majority of items held visibly in the player's hand would float in weird locations if you pet an animal
	Fixed Smart Cursor Painting having a different slot priority setup than actual Paint Tools, resulting in inconsistent behavior when putting Paint into Ammo Slots
	Fixed (again) the issue where Dart Pistols had two possible Deadly Prefixes
	Fixed an issue where Sanguine Staff and Terraprisma did not properly use Summon Lock On
	Fixed an issue with Valor in Golden Lock Boxes not dropping correctly
	Fixed a rare issue where the Gender button in character creation could break and show up off the UI bar
	Fixed an issue where "dodged" attacks could still result in debuffs on the player
	Fixed an issue where Magic Missile-class weapons could clip through some blocks when in liquids
	Fixed an issue with catching stacked fish (Bombfish, Daggerfish) with a full inventory deleting most of pre-existing stacks
	Fixed an issue where the game would be minimized but stay active under certain circumstances
	Fixed Journey/Expert mode not multiplying debuff times properly

D. Tile, Block and Worldgen Bugs
	Fixed an issue where Bamboo and Wrought Iron Fences would not allow certain trees to grow like other fences
	Fixed a dupe exploit involving sand
	Fixed an issue where mousing over Logic Sensors with Block Swap on could break them
	Fixed an issue where Clentaminator didn't properly convert mushrooms into Vicious Mushrooms
	Fixed an issue where Evil thorns stopped growing after initial worldgen
	Fixed an issue where Surface Mushroom background darkening was requiring too many mushroom blocks to activate
	Fixed an issue where Coral/Shells would regrow overtop of actuated blocks, replacing them
	Re-Fixed an issue where Demon Altars could generate on top of Rolling Cacti
	Fixed an issue with Golf Flags and wind detection
	Ropes no longer merge with Smooth Marble Blocks
	Fixed Crystal Shards not properly syncing when placed in multiplayer, which sometimes caused them to turn into Gelatin Crystals
	Fixed an issue where Jungle and Mushroom vines wouldn't grow underground, and an issue where Jungle Weeds would not turn into tall Jungle weeds
	Fixed some issues with Weapon Racks not properly being removed in multiplayer
	Fixed a long running issue where crafting a grappling hook would temporarily allow it to be used manually (which is not intended), leading to confusion when it stopped working later
	Fixed an issue where falling blocks would de-slope platforms they passed through
	Fixed an issue where Offline Gemspark Blocks did not blend the same way as Online Gemspark Blocks
	Fixed an issue where Hardcore Player Ghosts would prevent tiles from being placed behind them
	Fixed an issue where Sand would duplicate sometimes when falling as a tile
	Fixed some issues with falling blocks where they would land on some tiles they shouldn't land on, and also fixed some syncing issues relating to them turning into an item or not in multiplayer
	Fixed an issue where blue Portal Gun Stations would fire confetti if you tried to use confetti on them
	Fixed Auto-Select choosing confetti when hovering over a Portal Gun Station
	Fixed an issue where pressure plates in world gen would end up floating because they generated on breakable ice
	Fixed Living Mahogany Trees not considering Jungle Grass as Jungle when generating
	Fixed an issue where Boulder Traps would generate embedded in the Temple
	Fixed an issue where you could not build "off" of a beam like other blocks. They were not treated like an adjacent block for the purposes of building.
	Fixed a rare out of bounds issue with pots during world generation
	Fixed a minor tile framing issue with Gnome Statues
	Fixed an issue where Crimsand had no dust when stepping on it
	Fixed an issue where Snow Clouds used a slightly inaccurate dust color when stepping on it
	Stone Platforms are now immune to lava
	Fixed an issue where Dirt Bombs would not cause buried grass to die
	Fixed an issue where Pylon NPC detection only checked for the housing flag, and not the actual NPCs being present near their home.
	Fixed Smart Cursor acting inconsistently with herb placement with pots and planter boxes
	Fixed Mannequins/Hat Racks breaking in MP when bombed
	Fixed some issues with Smart Cursor and pumpkin placement

E. Visual/Art/Sound Issues and Bugs
	Mac/Linux players should now be able to see Vertex Shaders (the trails on Zenith, Terraprisma, Magic Missile, etc)
	Capes and Tax Collector's Suit now properly disable visibility when sitting, rather than showing up awkwardly in the wrong position
	Fixed an issue where Desert Tiger pounce didn't use Summon Dye
	Fixed an issue where multiple Minecarts used the Mount-dye slot instead of the Minecart-dye slot for their dust
	Fixed a sprite positioning issue with 2 of the Etherian Goblin variants
	Fixed a very widespread issue where several dozen armors had a transparent pixel in the armpit
	Fixed a cut-off pixel on the Nebula Workbench
	Fixed a missing pixel in the Zoologist emote
	Fixed an issue where wings would continue to display when the player was dead
	Fixed an issue where Water and Peace Candles would generate dust that behaved unusually when the player was on ropes
	Fixed some stray pixels in the Hallowed Palm Potted Plant
	Fixed Corrupt Torches making snow dust instead of Corrupt dust
	Fixed an issue where Goldfish Bowl helmets were one pixel too high while flying
	Fixed a stray pixel in the Goldfish Bowl helmet
	Fixed the Crimson Capture setting using Blood Moon water instead
	Fixed an odd pixel on one of the frames of the Gnome tile
	Fixing an issue with the Palm Armor sprite
	Fixed an issue where Mystic Snake Coil's pot would disappear when in certain positions
	Fixed an issue where parts of the player's body would be in the wrong position when in reverse gravity
	Fixed an issue with some tiles ignoring Illuminant Paint
	Fixed an issue where several new banners had item sprite that used the full sized tile sprite instead of the smaller item-sized version
	Stardust Guardian now stops showing its attack animation when the game is paused
	Fixed a number of SFX issues with Martians
	Fixed an issue where audio tracks were being compressed at 60% quality instead of 100%. Potentially most detectable in the Underground Desert track.
	Music Boxes should no longer play music when music volume is at 0
	Fixed an issue with light not spreading properly under some circumstances
	Fixed an issue where a Crimson background would cut off under specific circumstances
	Fixed an issue where background hellbats would be visible with backgrounds off
	Fixed an issue with Tree top framing
	Fixed an issue where some minions and pets would flip back and forth rapidly while holding out kites
	Fixed an issue where the Angel Halo wasn't fading with stealth, and would float in place if you died and opened the settings menu
	Fixed Tea and Coffee's sprites not being centered properly
	Fixed an issue where invisible characters had bald map icons
	Fixed an issue where invisible inner tubes caused visual issues on the body
	Fixed an issue where various coins did not use the correct color sparkles
	Fixed issues with long coat extensions when sitting
	Fixed some issues with Vine/Seaweed draw tiles not rendering properly when taking screenshots
	Attempted fix to an issue where Magic Missile-class items would sometimes visually "spike" towards the upper left corner. As this only happens to some users, and we do not know why and cannot reproduce it, we aren't sure if the fix was successful, so please feel free to report if it is continuing.

F. UI, Menu, and Journey Power Bugs
	Fixed an issue where Guide Crafting/Tinkerer Reforge slots were not linked to the player
	Fixed an issue where Celestial Pillar health bars would exceed the health bar meter due to changing difficulty in Journey mode
	Fixed Red Squirrel Cage not using the proper map mouseover text
	Fixed Peace Candles not having a mouseover icon like other Candles
	Fixed an issue where boss minimap icons didn't change direction based on the boss's direction like it used to
	Mana Cloak Star is no longer researchable (as it should never be obtainable in the first place)
	Fixed an issue where Eye color wouldn't always randomize during character creation
	Fixed an issue where Quick Stack to Nearby Chests would not respect whether your coins were favorited or not
	Fixed an issue for Journey mode sliders maxing out if you closed them while sliding
	Fixed rain starting on its own while time was paused with Journey powers
	Fixed several visual Sky-based effects failing to change properly when time was paused with Journey powers
	Fixed rain failing to visually start/stop when time was paused with Journey powers
	Fixed an issue where invasions would be announced, but would never arrive, when time was paused with Journey powers
	Fixed an issue where the Journey Menu hotkey did not work when autopause was on
	Fixed an issue where the game did not autopause in the Keybindings menu
	Fixed an issue where Journey Enemy Spawn rate slider would not visually go below 0.1x in multiplayer
	Fixed an issue where some text search boxes had no limit
	Fixed an issue where Fungi Bulbs did not properly indicate in the Bestiary that they spawn in the Surface Mushroom biome
	Fixed an issue where Hover Control preference was not actually saved
	Fixed an issue where windowed full screen did not stay maximized on relaunch
	Fixed an issue where opening settings interrupted any current movement inputs in multiplayer, even though you can still move in the settings menu
	Fixed a spacing issue on the ingame options menu that sometimes allowed for toggling two options at once by accident
	Fixed Torch God's Favor button breaking builder accessory input on Gamepad
	Fixed Gamepad not being able to open the Controls menu
	Fixed double inputs for some ingame options, notably Autosave/Autopause
	Torch God's Bestiary Entry now properly unlocks in single player when you use the favor item, and when a player first joins a world with favor already active
	Torch God's Bestiary Entry now lists Caverns and Underground as biome tags

G. Text, Tooltips and Dialogue Bugs
	Fixed some tooltips that used "crit chance" instead of critical chance
	Fixed an issue where one of the Cat pet names was missing, and one of the Cat pet names was split into two different names
	Fixed an issue where Tax Collector's were twice as likely to be named Agnew than they should be
	Fixed a few dated and no longer accurate loading tips
	Fixed some legacy dialogue lines from Demolitionist about "ebonrock", and gave it a Crimson-compatible alternate
	Fixed a variety of minor text and grammar issues, primarily in Bestiary or NPC Dialogue
	Fixed minor text issues with achievement descriptions
	Fixed an issue with several asset files having inconsistent capitalization (which causes some issues for some Linux users). This may require reinstalling Terraria to fix, if it is causing said issues, as Steam does not automatically replace the files just due to capitalization, and we have not found a way to force it to do so.
	Fixed an issue where the favorites file could not support some characters and symbols in world/player names

H. Server Issues/Multiplayer Specific Issues
	Fixed an issue where generating a world with the dedicated server would not respect the length limits of world names/seeds
	Fixed an issue where generating a world with the dedicated server would not properly work with special seeds
	Fixed an issue where worlds generated from the dedicated server were sometimes corrupt (unplayable, not the biome) on creation
	Fixed an oversight allowing you to set maxPlayers to over 255 or under 1 with the server config
	The Liquid Spam setting should now properly increment up to a kick, instead of instantly kicking a player when they place any liquid
	Fixed an issue where the server would endlessly try to shove items into the player's pockets if they don't pick the items up
	Fixed an issue where spawn points on the very rightmost edge of a map not functioning properly in Multiplayer


III. Terraria 1.4.1 Balance Changes

A. Melee Weapons

	Terra Blade and the True Swords Tier/Source
	Terra Blade and the True Swords have been somewhat overhauled in both crafting and function. Note: Mothron now only spawns after Plantera. As a result, the Broken Hero Sword is post-Plantera only.

	True Night's Edge
	Projectile damage now does 1.5x of the base damage
	Is now autoswing
	Is now crafted with the Night's Edge + some of all 3 boss souls. No longer requires a Broken Hero Sword.

	True Excalibur
	Increased damage from 66 to 70
	Is now autoswing
	Projectile now pierces once, hitting up to 2 enemies
	Is now crafted with the Excalibur + Chlorophyte Bars. No longer requires a Broken Hero Sword.

	Terra Blade
	Damage increased from 95 to 115
	Use time decreased from 16 to 14
	Projectile damage increased from 1.25x to 1.5x of the base damage
	Is now crafted with the two True Swords and a Broken Hero Sword

	Beam Sword
	Scale increased from 1f to 1.3f (this makes the sword itself larger)

	Brand of the Inferno
	Scale increased from 1.15f to 1.3f (this makes the sword itself larger)

	Sunfury
	Base damage decreased from 35 to 32. As normal swings deal double with flails, the standard expected damage should be reduced from 70 to 64.

	Arkhalis
	Damage increased from 20 to 25
	Now ignores up to 20 enemy defense

	Chain Guillotine
	Damage increased from 43 to 59

	Ghastly Glaive
	Immune frame duration reduced from 36 to 20. In effect, this means that the spear itself can hit more often, including more easily within a single swing.

	Anchor
	Damage increased from 55 to 70
	Knockback increased from 5 to 8

	Sergeant United Shield
	Damage increased from 60 to 80
	Damage reduction for each target hit reduced from 30% to 20%

	Scourge of the Corruptor
	Damage increased from 64 to 70
	Damage of Mini-Eaters increased from 70% to 75% of the base damage

	Yoyos (Revisions to 1.4 Changes)
	The balance changes made to Chik, Amarok and Helfire in 1.4 are being reverted
	The changes made to Code 2, Amazon, and Kraken are NOT being reverted/adjusted
	Gradient's damage increased from 44 to 49
	Format C's damage increased from 35 to 39

	Light's Bane
	Damage increased from 17 to 18

	Muramasa (How ya doin' Muramasa?)
	Damage increased from 21 to 26
	Knockback increased from 2.5 to 3

	Fiery Greatsword
	Damage increased from 36 to 40

	Beekeeper
	Reverting the changes made to Beekeeper in 1.4

	All Phaseblades
	Damage increased from 21 to 25

	Night's Edge
	Use time decreased from 27 to 21
	Is now autoswing

	Bananarangs
	Use time decreased from 14 to 11
	Increased both the projectile speed and the return speed of the Bananas

	Thorn Chakram and Flamarang
	Increased both the projectile speed and the return speed of the projectiles, with Flamarang being the faster of the two

	Sleepy Octopod
	Damage increased from 40 to 50
	Increased hit radius/size of the attack by 35%

	Flying Dragon
	Damage increased from 90 to 180.
	Projectiles which the player does not have line of sight on (as in, shooting through walls) now deal half damage (in this case, 90, the original damage)

	Sky Dragon's Fury
	Damage increased from 70 to 140
	Projectile damage decreased from 75% of base damage to 50% of base damage. This means instead of doing 52 (75% of 70) it will do 70 (50% of 140)

	Starlight
	Damage increased from 70 to 80
	Now has a bonus critical chance of 10%

	Daybreak
	Projectiles now explode when expiring, or upon hitting a wall. The explosion does an additional 100% weapon damage, and can hit nearby enemies as well.

B. Ranged Weapons and Ammo

	Onyx Blaster
	Damage decreased by 4
	Use time increased from 45 to 48

	Quad-Barreled Shotgun
	Damage decreased from 24 to 17
	Projectile count increased from 4 to 6
	Use Time increased from 45 to 55
	The Arms Dealer now only sells this after Skeletron

	Stake Launcher
	Use Time decreased from 26 to 12
	Applies a 10% damage penalty to the next hit for each enemy a projectile pierces

	Blowpipe
	Use Time decreased from 45 to 25
	Increased Seed (Ammo) damage from 3 to 4

	Jack 'O Lantern Launcher
	Use Time decreased from 30 to 25
	Exploding Jack 'O Lanterns (Ammo) damage increased from 30 to 60

	Dart Gun/Dart Rifle (Revision/re-assessment of 1.4 changes)
	The balance changes made to the Dart Gun and Dart Rifle in 1.4 are being reverted
	However, the changes made to the ammo (Crystal, Cursed, and Ichor) are being left as-is

	Tsunami
	Damage decreased from 60 to 53

	Nano Bullets
	Can now bounce once, and will "Smart Bounce" at a nearby target if one is in range
	Post-bounce bullets only deal 66% damage

	Beenades
	Damage reduced from 14 to 12

	Bone Arrows
	Damage increased 6 to 8

	Chlorophyte Bullets
	Damage decreased from 10 to 9

	Cursed Bullets
	Increased speed to match Ichor Bullets
	Also, see Debuffs section for details of Cursed Inferno changes

	Meteor Shot
	Damage decreased from 9 to 8

```


---

## 🤖 Assistant · 2026-08-09T11:41:07.600Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have the first ~412 lines of the changelog segment (4889-5300). I need to read the rest: 5301-5991. Let me continue reading in chunks.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:41:07.601Z · glm-x-preview-260804

```
已读完摘要与官方日志前 412 行，继续读取官方日志剩余部分。
```


---

## 🤖 Assistant · 2026-08-09T11:41:07.656Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '5301,5700p' \"~/Library/Application Support/Steam/steamapps/common/Terraria/changelog.txt\"",
 "description": "Read changelog lines 5301-5700"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:41:12.885Z

**📎 ToolResult**

```
	Reworked the immunity time system of Meteor Shot so rapid fire/shotgun-type weapons using it are unlikely to result in bullets missing due to immune frames

	High Velocity Bullets
	Damage increased from 10 to 11
	Projectile now pierces twice, hitting up to 3 enemies
	Applies a 15% damage penalty to the next hit for each enemy a projectile pierces
	Immunity time system matches the revised Meteor Shot; rapid fire weapons using HV Bullets should not have issues with immune frames

	Crystal Bullets
	Only generate 2 shards on impact instead of 3

	Jester Arrows
	Applies a 10% damage penalty to the next hit for each enemy a projectile pierces

	Unholy Arrows
	Applies a 5% damage penalty to the next hit for each enemy a projectile pierces

C. Magic Weapons

	Life Drain
	Damage increased from 30 to 35
	Like Medusa Head, should now no longer consume mana when being used but not hitting anything

	Nightglow
	Mana cost decreased from 26 to 23
	Projectiles can now bounce, improving their performance against enemies on the ground (instead of causing the projectiles to break when impacting the floor)

	Shadowbeam Staff
	Damage increased from 53 to 60
	Use time decreased from 16 to 15
	Damage reduction for each target hit reduced from 20% to 10%

	Unholy Trident
	Damage increased from 73 to 88
	Applies a 10% damage penalty to the next hit for each enemy a projectile pierces

	Poison Staff
	Ranged increased slightly, from roughly 30 to 37 blocks

	Venom Staff
	Ranged increased slightly, from roughly 45 to 58 blocks

	Medusa Head
	Range of effect increased by 25%

	Crystal Vile Shard
	Now ignores up to 10 enemy defense

	Nettle Burst
	Now ignores up to 10 enemy defense

	Wasp Gun
	Wasps now ignore up to 10 enemy defense

	Razorblade Typhoon
	Previously, this weapon fired two projectiles for every use, consuming mana only once. Now it only fires one projectile for the same mana cost and use time.
	However, that projectile now deals 50% more (increased from 60 to 90)

	Magical Harp
	Damage increased from 32 to 42
	Knockback increased from 0 to 0.25 (in other words, it now has knockback)
	Mana cost increased from 4 to 5
	Applies a 5% damage penalty to the next hit for each enemy a projectile pierces

	Blood Thorn
	Damage increased from 29 to 34
	Each projectile can now hit a third time (previously they could only hit twice)
	Reworked the immunity time system for this projectile so that it hits more often, conflicting with itself less
	Use Time increased from 21 to 33

	Magic Missile
	Use Time decreased from 18 to 22
	Mana cost increased from 12 to 14

	Flamelash
	Damage decreased from 36 to 32
	Mana cost increased from 18 to 21

	Flower of Fire
	Use Time decreased from 20 to 16
	Mana cost decreased from 15 to 12

	Space Gun
	Damage decreased from 19 to 17
	Mana cost decreased from 7 to 6

	Charged Blaster Cannon
	The player can now aim the beam when it is in the full beam mode

	Betsy's Wrath
	Damage increased from 65 to 110

	Stellar Tune
	Damage increased from 75 to 85

D. Summoning Weapons

	Whips Damage Penalty on multiple targets
	Whip Damage penalty per target struck has been reduced for most whips
		Cool Whip's damage penalty is reduced from 33% to 30%
		Durendal's damage penalty is reduced from 30% to 20%
		Morning Star's damage penalty is reduced from 25% to 5% (due to its heavy hitting nature, it's almost absent)
		Dark Harvest's damage penalty is reduced from 30% to 10%
		Kaleidoscope's damage penalty is reduced from 15% to 10%

	Whip Range
	Every whip (except for Leather Whip) has had a range increase
	This increase is the smallest with earlier whips (Snapthorn only roughly 10% longer) and larger with later whips (several late game whips have a roughly 50% increase)

	Whips + Flasks
	Whips can now gain the benefits of Flask buffs

	Leather Whip
	Is now purchasable from the Zoologist at 10% completion instead of 15%, as 15% too often left it more efficient to just sequence break to the Jungle to obtain Snapthorn

	Finch Staff
	Finch should now be somewhat more reliable/accurate with hitting its targets. However, due to how early it is obtained, it is intentionally a little inaccurate, as this is part of its balancing.
	Enemies knocked back by Finches should almost always be knocked away from the player now, regardless of the angle of the Finch

	Optic Staff
	Technically a bug, but Retinamini's lasers were accidentally not set to use independent immunity timers, which meant that they were still conflicting with other piercing attacks, while the 1.4 changelog had indicated otherwise. This has been fixed, which should result in less immune-frame time for Retinamini lasers.

	Sanguine Staff
	The attack speed of Sanguine Bats has been increased from 60 to 66 (this is how long it takes to make their attack circuit)

	Xeno Staff
	Fire rate cooldown increased from 30 to 33 (roughly 10% slower attack speed)

	Tempest Staff
	Fire rate cooldown decreased from 60 to 50 (roughly 20% faster attack speed)
	Projectile Speed of the Sharkrons increased from 14 to 20
	Movement speed of the Tempests themselves increased by 50%, so they can chase after enemies more quickly

	Hornet Staff
	Damage increased from 9 to 11

	Vampire Frog Staff
	Damage increased from 11 to 13
	Enemies can now be damaged by their entire body, not just the tongue, when they are attacking
	Like with Optic Staff, this was technically a bug, but Vampire Frogs were not set to use independent immunity timers like most other minions. This has been remedied, so they should no longer interfere with other piercing projectiles.

	Pygmy Staff
	Projectile speed increased from 12 to 18 (with additional adjustments made to their fall rate to keep it consistent)
	Increased the range at which Pygmies will fire their spears by roughly 40%

	Desert Tiger Staff
	Base damage increased from 33 to 41
	Hitbox size while using the special attack increased to reduce the situations where it misses while using it

	Frost Hydra Staff
	Projectile now pierces twice, hitting up to 3 enemies
	Applies a 15% damage penalty to the next hit for each enemy a projectile pierces

	Explosive Trap Staff
	Increased explosion size and detection for said explosion by 50%
	Reduced the explosion cooldown from 110 to 90
	Reduced the Huntress/Riding Hood special set cooldowns from 74 to 60 and 40 to 30, respectively
	For more information about changes to the Oiled debuff, see the Buff/Debuff section

	Kaleidoscope
	Damage increased from 165 to 180

E. Armor

	Cactus Armor
	Removed the 1 Defense set bonus.
	New set bonus: Cactus Armor now deals a flat 15 Thorns damage. This damage is multiplied to 30 and 45 respectively in Expert and Master mode.

	Mining Armor
	Increased the drop rate of Mining Shirt and Mining Pants from 2.4% to 12%. That's not a typo!

	Gladiator Armor
	Increased the defense of the Helmet and Leggings by 1
	Increased the defense of the Breastplate by 2
	New set bonus: Players wearing the full Gladiator set are immune to knockback
	Increased the drop rate from a 1/20 chance to drop a random piece to a 1/7 chance

	Fossil Armor
	Increased defense of Helmet and Greaves from 2 to 4
	Increased Ranged critical chance on Helmet and Greaves from 3% to 4%
	Increased defense of Plate from 4 to 5
	Replaced the 3% Ranged critical bonus on the Plate with a 5% Ranged damage bonus

	Wizard Hat
	Magic damage decreased from 15% to 5%
	Defense increased from 2 to 4

	Magic Hat
	Magic damage/critical chance bonus decreased from 7 to 6

	Meteor Armor
	Increased the Magic damage bonus on each piece from 7% to 9% (21%->27% total)
	(Cross-listing from Magic section) Space Gun's damage decreased by 2, and its mana cost reduced by 1

	Jungle Armor (And Ancient Cobalt Armor)
	Increased the Magic critical chance bonus on the Hat and Pants from 4% to 6%
	Replaced the 4% Magic critical bonus on the Shirt with a 6% Magic damage bonus

	Necro Armor
	Decreased the set bonus Ranged critical chance from 15% to 10%
	Increasing defense of each piece by 1 (3 total) Included Ancient Necro Helmet

	Obsidian Armor
	Converted the Obsidian Armor into a Whip-centric Summoner armor
	Obsidian Armor set pieces can now only be crafted at a Hellforge, and requires Shadow Scales/Tissue Samples
	Obsidian Outlaw Hat now gives 9% Summon damage
	Obsidian Longcoat now gives +1 Minion count
	Obsidian Greaves now give 9% Summon damage
	New Set bonus: Increase Whip Range and Speed by 50%. Additionally, gain another 25% Summon damage (43% total across the entire set)
	Note: This set will deal very high summon damage, but at the expense of a lower minion count. Instead, it focuses on dramatically improving the performance and damage of whips, and can still be obtained earlier, or as an alternative, to Bee Armor, but it may require a bit more legwork to obtain the set, given its new crafting station requirement.

	Molten Armor
	Molten Helmet now gives 7% Melee Critical Chance
	Molten Breastplate now gives 7% Melee Damage
	Molten Leggings now give 7% Melee Speed
	The 17% Melee Damage set bonus has been reduced to 10% (the 7% moved to the Breastplate)
	New Set bonus: Players wearing the full Molten set cannot be inflicted with the On Fire debuff. This is in addition to the pre-existing 10% damage bonus.

	Cobalt Armor
	Cobalt Breastplate Critical Damage increased from 3% to 5%
	Cobalt Leggings Defense increased from 7 to 8
	Added a 3% Damage bonus to the Cobalt Leggings
	Cobalt Helmet (Melee) Defense increased from 11 to 12
	Cobalt Helmet Movement Speed increased from 7% to 10%
	Cobalt Helmet Melee Speed bonus (12%) changed into a Melee Damage Bonus (15%)
	Cobalt Mask (Ranged) Critical Chance increased from 6% to 10%
	Added a 10% Magic Damage bonus to the Cobalt Hat (Magic)

	Palladium Armor
	Reduced the potency of the healing set bonus from 6 to 4
	Palladium Mask (Melee) Damage bonus increased from 8% to 12%
	Palladium Headgear (Magic) Damage bonus increased from 7% to 9%
	Palladium Headgear Damage bonus increased from 7% to 9%

	Mythril Armor
	Mythril Chainmail Damage bonus increased from 5% to 7%
	Mythril Greaves Critical chance increased from 3% to 10%
	Mythril Helmet (Melee) Critical chance increased from 5% to 8%
	Mythril Melee set bonus increased from 5% to 10% Critical Chance

	Orichalcum Armor
	Orichalcum Mask (Melee) Damage bonus increased from 7% to 11%
	Orichalcum Mask Melee Speed bonus increased from 7% to 11%

	Adamantite Armor
	Adamantite Breastplate Damage bonus increased from 6% to 8%
	Adamantite Leggings Critical bonus increased from 4% to 7%
	Adamantite Melee Set Bonus (Melee/Movement Speed Boost) increased from 18% to 20%
	Adamantite Mask (Ranged) Critical chance increased from 8% to 10%
	Adamantite Headgear (Magic) Damage increased from 11% to 12%
	Adamantite Headgear Magic Critical chance increased from 11% to 12%

	Titanium Armor
	Titanium Mask (Melee) Damage/Critical/Speed bonus increased from 8% to 9%

	Frost Armor
	Frost Armor's Set Bonus now gives an additional 10% Melee/Ranged Damage
	Frost Armor's Set Bonus now inflicts a special version of On Fire that deals 25 DPS instead of 8

	Forbidden Armor
	Forbidden Robes now have a 10% Summon Damage bonus
	Forbidden Treads now have a 10% Magic Damage bonus

	Chlorophyte Armor
	Decreased the cooldown on the Leaf Crystal shot from 50 to 40

	Spectre Armor (Mask)
	Increased the Magic Damage/Critical Chance bonus from 5% to 10%
	Increased the limit on how much burst damage can be dealt by the set bonus at once from 1000 to 1500
	The "recovery rate" that determines how many new projectiles can be generated over time has increased from 250 to 400 (it was increased from 150 to 250 in 1.4)

	Spectre Armor (Hood)
	Note: Statistically speaking, this set has not changed! This is merely a re-organizing of stat changes and tooltip revision to be more clear to players
	The -40% damage penalty has been moved from the Spectre Hood itself (which now gives no bonuses at all, either positive or negative) and now comes from the Set Bonus
	The tooltip on the set bonus now attempts to be more clear about the fact that you are trading offensive power for healing benefits. Hopefully, this will lead to less confusion in the future about why this set works the way it does.

	Crystal Assassin Armor
	Added 10% Mana Cost reduction to the Hood
	Added 10% Ammo Cost reduction to the Shirt
	Added 10% Melee Speed increase to the Pants
	Removed the 15% Movement Speed increase Set Bonus, but increased the Movement bonus on the boots from 10% to 20% (only 5% loss)
	New Set Bonus: Players wearing the full Crystal set can now Dash

	Squire Armor
	Decreased Greaves Melee Critical chance from 20% to 15%

	Monk Armor
	Increased Pants Melee Critical chance from 10% to 15%

	Huntress Armor
	Added +10% Ammo Cost Reduction to the Jerkin

	Apprentice Armor
	Added +10% Magic Damage on Helmet

	Valhalla Knight Armor
	Added +10% Melee damage on helmet
	Decreased Greaves Movement Speed bonus from 30% to 20%

	Shinobi Infiltrator Armor
	Increased Pants Movement Speed bonus from 20% to 30%
	Added +5% Melee Critical chance on Torso

	Red Riding Armor
	Added +10% Ranged Critical chance on Leggings
	Added +20% Ammo Cost Reduction on Dress

	Dark Artist Armor
	Added +20% Movement Speed Bonus on Leggings
	Added +15% Mana Cost Reduction on Robes
	Moved 5% of the Minion/Magic Damage from Robes to Hat

F. Accessories

	Band of Regeneration/Charm of Myths
	Increased healing gain from 0.5 HP per second to 1 HP per second

	Band of Starpower/Panic Necklace
	(Cross-listing from Crafting Changes) Band of Starpower and Panic Necklace are now more easily available in all worlds. They can be crafted in a Graveyard at a Tinkerer's Workshop, by taking one of them and combining it with a Life or Mana Crystal. Band of Starpower + Life Crystal = Panic Necklace. Panic Necklace + Mana Crystal = Band of Starpower.

	Bone Glove
	This item has been completely overhauled and turned into an accessory
	When equipped, the player will shoot Crossbones towards their cursor whenever they are attacking, once per second. Consider it like a sword projectile, except it works for every weapon.
	The bones deal 25 class-neutral damage, but additionally ignore up to 25 enemy defense.
	Now also has vanity visibility in the Gloves spot
	Note: In practice, this should allow the Bone Gloves to be simultaneously viable for more classes than just Ranged, and also give it a bit more longevity

	Brain of Confusion
	Reduced the Critical chance bonus of the Mind Trick buff from 20% to 10%.
	Reduced the duration of Mind Trick by 1 second

	Celestial Cuffs
	Now has the +20 mana bonus that its component accessories granted

	Diving Helmet and all of its tinkers
	Increased the breath capacity bonus by 50%

	Feral Claws and Titan Glove
	Moved the "gives autoswing for Melee weapons" perk to Feral Claws, making it available earlier for players. This perk still continues up the tinker chain, it is simply no longer present on Titan Glove specifically
	Titan Glove now has a new perk that increases the size of (eligible) melee weapons by 10%. This perk is also present on all of its tinkers; however, the effect does not stack.

	Fledgling Wings and Lucky Horseshoe
	The Lucky Horseshoe is no longer found in Sky Chests, and has been added to the underground Gold Chest loot pool
	In its place, Fledgling Wings have been added to Sky Chests and Sky Crates

	Flesh Knuckles/Berserker Gloves
	Defense increased from 7 to 8

	Fire Gauntlet
	Increased the 10% Damage and Melee Speed bonus to 12%
	Gains the new benefit added to the Titan Glove (see Titan Glove)
	Gains the new benefit added to the Magma Stone (see Magma Stone)

	Hero Shield
	Defense increased from 7 to 10
	Honeycomb (and Bee Cloak, Honey Balloon, Stinger Necklace, and Sweetheart Necklace)
	The base damage of the Bees generated by these has been increased from 7 to 13. If using a Hive Pack, this damage is 18.
	This damage is multiplied by 1.5x in Expert mode, and 2x in Master mode
	Additionally, if hit while wearing any of these accessories, the player gains the Honey buff for 5 seconds

	Jellyfish Necklace and all of its tinkers
	Now lets off an extremely faint glow when out of water (less than the Shadow Orb light pet)
	Dramatically increased the brightness when in water

	Lava Charm
	Doubled its spawn rate, giving it a 1/20 chance to be found in Lava-layer chests or Lava fishing crates

	Magma Stone
	Now inflicts a special version of On Fire that deals 15 DPS instead of 4

	Molten Quiver
	Technically a bug fix, but Wooden Arrows converted to Flaming Arrows by using this accessory now properly gain the +2 damage that Flaming Arrows have. This bonus is only applied to Wooden Arrows, if using the Quiver with superior arrows it will not apply the bonus (as it would be using the superior damage bonus of those arrows instead)

	Obsidian Rose
	Increased the lava damage reduction from 30 to 45. This change applies to all of its tinkers, however, as a consequence, lava damage has been moved to its own immunity timer, as the change would allow lava to very easily be reduced to 1 damage with the proper loadout.
	Is now a component in the Lava Waders, extending its lava damage reduction to the Lava Waders, Hellfire Treads, and Terraspark Boots. This change is retroactive for people who have already crafted those items, of course!

	Panic Necklace/Sweetheart Necklace
	Increased duration of the Panic! buff from 5 to 8 seconds

	Pygmy Necklace
	Is now sold by the Witch Doctor in pre-Hardmode, giving summoning accessories some earlier-game accessibility (he still only sells it at night, however!)

	Star Cloak, Bee Cloak, Star Veil, and Mana Cloak
	The base damage of the Stars generated by these accessories has been increased from 30 to 75. In addition, these stars will ignore up to 25 enemy defense.
	This damage is multiplied by 2x in Expert mode, and 3x in Master mode (the defense penetration remains unchanged)
	Now uses local immune frames, will not interfere with other piercing projectiles


G. Tools and Mounts

	Reaver Shark
	Use time decreased from 18 to 13

	Bone Pickaxe
	Drop rate increased from 2% to 5%

	Chlorophyte Jackhammer
	Included this item in the Drill/Chainsaw mechanics overhaul. It now has increased speed at the expense of range

```


---

## 🤖 Assistant · 2026-08-09T11:41:14.331Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Continuing to read 5700-5991.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:41:14.332Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '5700,5991p' \"~/Library/Application Support/Steam/steamapps/common/Terraria/changelog.txt\"",
 "description": "Read changelog lines 5700-5991"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:41:32.794Z

**📎 ToolResult**

```
	Mechanic's Rod
	Fishing power increased from 30% to 35%
	Now sold by the Mechanic as soon as she can be rescued, not just in Hardmode
	Is now available every other moon phase, rather than only a single moon phase

	Fiberglass Fishing Pole
	Fishing power increased from 27% to 30%
	Increased odds of finding it in a chest from 1/30 to 1/15

	Scarab Fishing Rod
	Fishing Power increased from 25% to 30%

	Sitting Duck Rod
	The Traveling Merchant will now only sell this after Skeletron has been defeated

	Living Wands
	The Living Wood Wand and Leaf Wand have a 1/300 chance of being dropped from TreeHit purity forest trees, offering a rare but renewable source of them
	The Living Mahogany Wand and Rich Mahogany Leaf Wand have a 1/200 chance of being dropped from TreeHit Jungle Trees

	Black Spot
	Top speed and acceleration decreased dramatically. Previously its top speed was higher than the UFO mount, but now it is less.
	Can no longer dash-into-mount to instantly reach top acceleration

	Scutlix Mount
	There was an unlisted change in 1.4 that dramatically reduced the range of the Scutlix mount's attack. This was a performance change, not a balance change, and cannot be fully reverted as a result.
	However, the reduced range (500) was able to be increased to 850 without reintroducing performance issues.
	Additionally, to compensate for the lost range, the damage of the Scutlix shots has been increased from 100 to 150

	Dark Mage's Tome
	This mount now steps up slopes and 1-block tiles like the Flying Carpet

	Witch's Broom 
	Slightly increased speed values so that it is a minor upgrade over the UFO Mount (since it is Expert exclusive)

	Flamingo Mount
	Top speed decreased from 7.5 to 6

	Pre-Hardmode Horse Mounts (Dusty Rawhide, Royal Gilded, and Black Studded Saddles)
	Top speed increased from 8 to 9

	Jewel of Light and Pumpkin Scented Candle (Light Pets)
	Brightness increased by roughly 50%

	Suspicious Looking Tentacle (Light Pet)
	Brightness increased by roughly 33%

H. Crafting Recipes and Drops

	Blood Rain Bow, Chum Caster, and Vampire Frog Staff
	Previously, killing a Wandering Eye Fish or a Zombie Merman had a flat 1/8 chance for the game to select ONE of the three items to drop, and it would only drop one. This has been changed so that each of the three items has their own independent 1/8 chance to drop. This means that you could potentially get more than one drop at once, and the three are no longer competing with each other, effectively increasing their drop rate by 3x.

	Bloody Tear
	Increased drop rate from 1/200 to 1/100 for standard Blood Moon enemies
	Increased drop rate from 1/200 to 1/25 for Blood Moon fishing enemies (Eyeball Fish, Zombie Merman, Blood Eel, Hemogoblin Shark)
	Increased drop rate from 1/9 to 1/5 for The Groom and The Bride
	Increased drop rate from 1/9 to 1/2 for Dreadnautilus. In Expert/Master, this drop rate is 100%.

	Sanguine Staff
	Increased drop rate from 1/5 to 1/2 for Dreadnautilus. In Expert/Master, this drop rate is 100%.

	Blade Staff
	Now drops from Queen Slime instead of Enchanted Swords

	Kites (From Balloon Slimes)
	Kites dropped from Balloon Slimes are roughly 3x more likely to drop. Paper airplanes are mostly the same, but now drop in small stacks

	Bone Serpent Kite
	Drop rate increased from 4% to 6%

	Sturdy Fossil
	Tomb Crawlers now have a chance to drop small amounts of Sturdy Fossil
	Oasis/Mirage Crates now have a chance to include Sturdy Fossil

	Valor/Muramasa and Golden Lock Boxes
	(Technically a bug) fixed an issue where Muramasa had twice the odds of dropping from a Golden Lock Box compared to other items
	Valor can now be found from Golden Lock Boxes

	Torches
	Jungle Torches now have a more efficient recipe, giving more torches per Jungle Spore
	If you have less than 20 torches at any point, you have an increased chance to get torches when breaking pots

	Mana Crystal
	In light of the increased spawn rate of Falling Stars in 1.4, the crafting recipe for Mana Crystals has been increased from 3 to 5 Fallen Stars

	Early Game Ore Tools, Weapons, and Armor
	The cost of making early game Ore equipment has been re-evaluated across the board with cost reductions to most items. This applies to Copper, Tin, Iron, Lead, Silver, Tungsten, Gold, and Platinum
	Pickaxes have had their crafting costs reduced from 12 to 10. Copper/Tin Pickaxes have been reduced to 8.
	Axes have had their crafting costs reduced from 9 to 8. Copper/Tin Axes have been reduced to 6.
	Broadsword crafting costs are generally unchanged, but Copper/Tin Broadswords have been reduced from 8 to 6
	Shortswords have had their crafting costs reduced from 7 to 6. Copper/Tin Shortswords have been reduced to 5.
	Hammers have had their crafting costs reduced from 10 to 8.
	Bows have NOT had their crafting costs changed.
	Copper and Tin Armor's costs (ordered from Helmet>Chest>Legs) have been reduced from 15/25/20 Bars to 12/20/16 Bars
	Iron and Lead Armor's costs have been reduced from 20/30/25 to 15/25/20
	Silver and Tungsten Armor's costs have been reduced from 20/30/25 to 15/25/20
	Gold and Platinum Armor's costs have been reduced from 25/35/30 to 20/30/25

	Hardmode Ore Swords
	The crafting cost for Cobalt and Mythril Swords has been reduced from 10 to 8 Bars
	The crafting cost of Palladium and Orichalcum Swords has been reduced from 12 to 10 Bars
	The required bars to craft Adamantite and Titanium Swords has not changed, but see the next section for more info

	Adamantite/Titanium Bars
	The crafting cost of Adamantite/Titanium Bars has been reduced from 5 to 4 Ore. Subsequently, this reduces the cost of all Adamantite/Titanium armor, weapons, and tools

	Jester Arrows
	The crafting efficiency per Fallen Star has been reduced by half. You now get 10 arrows per star rather than 20.

	Super Star Shooter
	Rather than being sold randomly from the Traveling Merchant, this weapon is now crafted with the Star Cannon and Hallowed Bars

I. Buffs/Debuffs

	Frostburn
	"Player" Frostburn now does 8 DPS like "Enemy" Frostburn

	Cursed Inferno
	Technically a bug fix: 1.4 purported to increase Cursed Inferno damage from 12 to 24, but this was in error due to misreading the code. In truth, this was an increase from 6 to 12. This has now been remedied, and Cursed Inferno now properly does 24 DPS. However, player-based Cursed Inferno has NOT been increased correspondingly, so they will still take 12 DPS.

	Venom
	Technically a bug fix: 1.4 purported to increase Venom damage from 12 to 30, but this was in error due to misreading the code. In truth, this was an increase from 6 to 15. This has now been remedied, and Venom now properly does 30 DPS. However, player-based Venom has NOT been increased correspondingly, so they will still take 15 DPS.
	Venom has been renamed to "Acid Venom". This is to reflect a dramatic overhaul to its enemy immunity. Enemies who are immune to Poison are no longer necessarily immune to Acid Venom, and Acid Venom will now usually impact undead, stone, metal, and poisonous enemies.

	Ichor
	Defense reduction has been reduced from 20 to 15

	Oiled
	Rather than individually boosting different OnFire-like debuffs with, admittedly arbitrary amounts, Oiled now adds an additional flat 25 DPS if the target is suffering from any of these debuffs. For example, if the target is On Fire (4 DPS), it will take 29 total if Oiled.

	Thorns Potion
	The Thorns effect from this potion has been increased from 1/3rd of the damage taken to 100% of the damage taken

	Dryad's Blessing
	The Thorns effect from this buff has been increased from 20% of the damage taken to 50% of the damage taken

	Debuff Immunity Overhaul
	Though far too extensive to fully document, hundreds of changes have been made to enemy debuff immunities across the game. Generally speaking, the majority of these changes were making enemies susceptible to debuffs which they were previously immune to.
	The Venom change previously mentioned is the most prominent example, with the vast majority of Venom immune enemies no longer being immune.
	A large number of enemies which were previously immune to Cursed Inferno no longer are, particularly many stone/metal enemies
	Previously, enemies which were immune to Cursed Inferno were also always immune to Shadowflame. This is no longer the case, and there are now enemies immune to one or the other, though on the whole, a lot less enemies are immune to Shadowflame than before
	Ghost-like enemies (Wraiths, Poltergeists, etc) are now almost always immune to all major debuffs, including Ichor. This does not extend to Whip-debuffs.
	A large number of enemies which were "immune to everything" no longer are. This includes several Pumpkin Moon enemies and Celestial Invasion enemies that were immune to everything for no apparent reason. They are now immune, or not immune, to various debuffs depending on their nature.
	Several enemies which are "immune to everything" intentionally (such as the Destroyer) are no longer immune to Whip-debuffs, as those are meant to be universal.
	Though there are a few exceptions, the vast majority of Confusion-immune enemies still are. Unfortunately, this is because Confusion requires specialized code for every type of enemy, and so the cost investment to make more enemies susceptible to Confusion is dramatically higher than simply "setting them to not immune" like the other debuffs.

J. Threats and Enemies

	Vicious Goldfish
	Now spawns naturally in Crimson water. Never actually spawned naturally before, with regular goldfish spawning instead.

	Blood Feeder
	Life increased from 20 to 150
	Damage increased from 30 to 50
	Defense increased from 4 to 20
	Money drop value increased from 350 to 500

	Ghosts
	Life decreased from 70 to 50
	Damage decreased from 18 to 15
	Defense decreased from 8 to 4
	Knockback susceptibility increased from 40% to 50%

	Antlion Larvae
	Life decreased from 45 to 35
	Damage reduced from 12 to 10

	Antlion Eggs
	Antlion Eggs are now less common in initial worldgen, so there should be less of them overall, making the Underground Desert slightly less dangerous
	Antlion Eggs will now slowly regrow over time, like Bee Hives in the Jungle, but like Bee Hives, only until there are a certain number in an area, to prevent over-saturation

	Rolling Cactus
	Reduced the base boulder damage by about a third, making them slightly less lethal (though still considerably dangerous) threats
	Increased the Cactus Thorn projectile damage from 20 to 30

	Angry Dandelion
	Technically a bug fix: fixed an issue where Angry Dandelion's projectile damage scaled twice, resulting in it doing far more than it should have, especially in Expert/Master

	Rock Golem
	Technically a bug fix: fixed an issue where Rock Golem's projectile damage scaled twice, resulting in it doing far more than it should have, especially in Expert/Master

	Wall of Flesh
	Wall of Flesh now causes the screen to fade to black and will despawn if all nearby players are dead, or there are no more players nearby.

	Ice Elemental
	Projectile attack can now inflict Frostburn

	Jungle Creeper
	Life increased from 120 to 400
	Defense increased from 14 to 40
	Damage increased from 50 to 100
	Now moves faster
	Attacks can now inflict Venom
	Spits Web in Expert/Master like Black Recluses

	Lac, Cyan, and Cochineal Beetles
	Reduced "rarity" from 1 to 2 on the Lifeform Analyzer. Will no longer take priority over even more rare enemies, such as Lost Girls.

	Phantasm Dragon
	Life increased from 4000 to 10000
	Head Defense increased from 10 to 15
	Body and Tail Defense increased from 20 to 30
	Head Damage increased from 80 to 100
	Body and Tail Damage increased from 40 to 50

	Hoppin Jack
	Can now spawn in Graveyards in Hardmode, any time of year

	Vortex Lightning
	Increased the damage of both types of lightning bolts during the Vortex Invasion to 100

K. Miscellaneous and Quality of Life

	Graveyard Threshold
	The number of graves required to trigger both a full graveyard and the various levels of graveyard ambience has been increased by 1

	Town Happiness
	The boost from the "So Much Space" factor has been reduced by half
	The boost/penalty for Like/Dislike/Love/Hate factors have been increased by 20%. Everything is worth a little bit more in any direction.
	You can now have up to 3 NPCs in close proximity without any crowding unhappiness. It will now begin when there are 4 NPCs in close proximity. Furthermore, the size of the penalty starts smaller than before (though it will grow faster with each additional NPC)
	The size of the town detection has been doubled

	Block Swap and Sand/Other Falling Tiles
	You can now block swap the top-most block of sand or other falling blocks.
	Additionally, once your pickaxe power is high enough (Cobalt or higher), you can block swap any falling tiles freely

	Meteorite Ore
	While still immune to explosions under normal circumstances, like other explosion resistant materials, they will become breakable with explosives after entering Hardmode

	The Jungle and Corrupt/Crimson Worldgen
	Worldgen will attempt to avoid overlapping Corruption and Crimson biomes with the Jungle during initial worldgen. While it is possible to still have overlap, the worldgen system will strongly discourage it in general, so expect to see far less worlds with Corrupt/Crimson Jungles. This does not apply to the Hardmode infection strips.

	Armed Zombie/Throwing Skeleton Statues
	These can now be found in worldgen in any world difficulty, and will function normally in those worlds

	Shadow Chests in Worldgen
	Shadow Chests are now more numerous in worldgen, with the limit increasing from 7-10 to 10-15

	Pyramid Rarity
	Worldgen's chance to place Pyramids has been increased by 50%.

	Enchanted Sword Shrines
	Worldgen's chance to place Enchanted Sword Shrines has been doubled (more accurately, each attempt to generate had only a 1/4 chance to succeed, and that has been increased to 1/2)

	Sandstorm Frequency
	Increased Sandstorm chances by 2x in Hardmode, and by 1.33x pre-Hardmode
	
	Rock Lobster
	Sell value decreased from 20 Silver to 10 Silver

	Sakura/Yellow Willow Saplings
	Price decreased from 3 Gold to 1 Gold

	Special Furniture Crafting Stations
	The Steampunker will now sell most of the special furniture stations if you are in the correct biome.
	Snow biome = Ice Machine, Space = Sky Mill, etc
	The Bone Welder is sold when in a Graveyard, as the Dungeon is no proper home
	Living Looms will be sold if the player is carrying a Living Wood Wand (please see the Tools section about Living Wood Wand renewability)
	The Flesh Cloning Vat and Decay Chamber, while still sold by the Steampunker only in one type of evil world, can be crafted into each other in a Graveyard, with some Souls of Night

	Mirage Fish/Pixie Fish
	Adjusted Mirage Fish and Pixiefish to be "uncommon" instead of "rare", to match other Quest fish

	TreeHit for Loot
	The limit on the number of TreeHits you can attempt per day has been increased from 200 to 500

	Sharpening Stations
	The Merchant will now sell Sharpening Stations in Hardmode

	Books
	The Wizard will now sell books. Their cost has been increased somewhat as a result, from 3 to 15 Silver.

	1/3/5 Timers
	These are still craftable, but are also sold by the Mechanic

	Mushrooms
	Regular orange mushrooms now have a potion sickness time of 30 seconds, instead of the full 60.

	Fishing Decreasing Returns
	Removed decreasing returns on Fishing Power at high levels.

	Pylons and the Celestial Invasion
	Pylons can now be used during the Celestial Invasion to traverse the world to combat the various pillars. This exception does not include Moon Lord, and they are still unusable during other invasions/boss fights.

	Journey Mode Starting Inventory
	Players in Journey Mode now spawn with the basic Grappling Hook

	Boss Related Bestiary Entries
	Boss minions which have their own Bestiary entries are now unlocked fully upon defeating their corresponding boss
	Dark Mage and Ogre only need to be killed once now to fully unlock their Bestiary entries

```


---

## 🤖 Assistant · 2026-08-09T11:41:36.533Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I've now read the entire official 1.4.1 section (4889 to roughly 6051? Let me check — the last chunk I read was 5700-5991 and it ended with "Dark Mage and Ogre only need to be killed once now to fully unlock their Bestiary entries". Wait, does the 1.4.1 section end at 5991? The task says lines 4889-5991 cover Version 1.4.1 to 1.4.1.2. But my read of 5700-5991 ended with Bestiary entries... The 1.4.1.1 and 1.4.1.2 sections should follow. Let me check — the output ended at line 5991 which was "Dark Mage and Ogre only need to be killed once...". That means the 1.4.1.1 and 1.4.1.2 sections are beyond 5991? But the task says 4889-5991 covers 1.4.1 to 1.4.1.2.

Hmm, wait. Let me verify where 1.4.1.1 starts. Let me grep.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:41:36.536Z · glm-x-preview-260804

```
官方 1.4.1 主体已读完，但第 5991 行似乎还没到 1.4.1.1 段落，需要确认行号边界。
```


---

## 🤖 Assistant · 2026-08-09T11:41:36.654Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"Version 1.4.1\" \"~/Library/Application Support/Steam/steamapps/common/Terraria/changelog.txt\" | head -20",
 "description": "Find version section boundaries in changelog"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:42:06.967Z

**📎 ToolResult**

```
4698:Version 1.4.1.2 Changes -------------------------------------------------------------------------------------------
4864:Version 1.4.1.1 Changes -------------------------------------------------------------------------------------------
4889:Version 1.4.1 Changes -------------------------------------------------------------------------------------------

```


---

## 🤖 Assistant · 2026-08-09T11:42:09.943Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting! The changelog is in reverse order: 1.4.1.2 at 4698, 1.4.1.1 at 4864, 1.4.1 at 4889. So lines 4889-5991 is the entire 1.4.1 main section (which runs to ~6060?), and 1.4.1.1 is 4864-4888, 1.4.1.2 is 4698-4863.

Wait but the range given was 4889-5991. Let me check where 1.4.1 ends (i.e., where the next section "Version 1.4.0" begins).
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:42:10.162Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '5992,6010p' \"~/Library/Application Support/Steam/steamapps/common/Terraria/changelog.txt\"; echo \"=====PREV=====\"; sed -n '4698,4888p' \"~/Library/Application Support/Steam/steamapps/common/Terraria/changelog.txt\"",
 "description": "Read section end and 1.4.1.2/1.4.1.1 sections"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:42:13.211Z

**📎 ToolResult**

```
Version 1.4.0.5 Changes -------------------------------------------------------------------------------------------


I. Optimizations and Crash Fixes
	The Multiplayer server is now more strict about fake connection attempts
	Added some error handling for peripheral Chroma related crashes
	Improved error handling to prevent some crashes related to "Spritebatch"
	Improved error handling to prevent some sound related crashes when alt+tabbing out
	Chests and similar furniture placed on top of non-solid tiles should no longer cause crashes
	Fixed a file naming error that would cause a crash for Linux users
	Fixed a crash that can happen sometimes when changing screens
	Fixed a crash that happens when sitting/sleeping in relation to the Potion of Return
	Fixed a rare crash caused by using a Magic Conch in a Sandstorm
	Fixed a crash caused by attempting to load worlds that were so corrupted, that even the corruption detection was corrupted
	Fixed a certain issue with worlds saving in host and play
	Fixed a certain world loading bug
	Fixed loading a bugged world in host and play leaving a stuck server process
	Added further protections against characters named "." and similar such names causing file deletion
	Error log entries for RGB/Peripheral support now properly indicate that they are normal messages, and not errors. They also include a message indicating that you can disable them. 
=====PREV=====
Version 1.4.1.2 Changes -------------------------------------------------------------------------------------------

I. Changes and Adjustments
- Localization should now be updated to fully include 1.4.1 content. Special thanks to Criddle and Midnaait for additional contributions in regards to localization changes!
- Reverted Town NPC House/Village check distance increase. This was doubled in 1.4.1, and has now been returned to 1.4 levels.
- NPC Happiness now gives the "Space" bonus for 3-NPC towns. Previously, there was neither a bonus nor a penalty at 3 NPCs, but this was perceived as a penalty, so its been changed.
- Skeletron Prime's bombs now explode on Planter Boxes (like they were changed to do on Platforms)
- Capes now show when sitting or riding mounts. This was previously limited due to conflicts, but feedback indicated it was worth the potential awkwardness at times to have the option.
- Queen Slime's minions can now drop Slime Staff at normal drop rates
- Clicking anywhere on the creative/bestiary menu will pause searching. This should make the UI more intuitive and result in being accidentally "stuck" in the textbar less common.
- Updated Timeless Traveler sprites, as the sprites being used were accidentally out of date versions
- Spectre Goggles no longer override helmets entirely, as they are not full head accessories and were not meant to do so

II. Bug Fixes:
- Attempting a music-related fix for an issue where users cannot increase their music volume above 0%. This may also potentially fix some seemingly unrelated launch crashes which actually stem from the same root issue.
- Fixed an issue with Happiness values that was causing them to round down heavily, negating minor differences and making it harder to reach certain thresholds.
- Fixed an issue where the Crowded penalty for only 1 NPC was acting like there were 2 extra NPCs, making it start more severely than intended
- Fixed a back-end issue that prevented the Chinese localization for 1.4 being added to the game correctly
- Fixed an issue where the Ronin set would not show fireflies on a female character
- Fixed an issue where player skin became much brighter under some circumstances, such as using some Light Pets
- Fixed another syncing issue with Cracked Dungeon bricks, which should resolve the teleporting enemies in Dungeons
- Fixed an issue where increasing time rate in Journey mode would make the Credits run very fast on the main menu
- Fixed an issue where certain parts of the credits roll did not support texture packs and could result in a crash
- Fixed Life Drain not costing mana to use in PVP
- Fixed a fault in the Prismatic Lacewing sprite file that caused severe issues for a small minority of Linux users
- Fixed Princess discussing bosses/threats that hadn't been defeated yet
- Fixed Princess's party hat not being on her head correctly
- Fixed Video Visage's screen being offset when in reverse gravity
- Fixed an issue where some Vanity ears would show the back-ear in the wrong position when sitting
- Fixed an issue where Tail accessories did not adjust their height correctly when sitting
- Fixed an issue where certain hairs would "draw double" when sitting
- Fixed a wide variety of NPC Dialogue, Bestiary, and Item Flavor Text grammatical/spelling/punctuation issues.
- Fixed an issue with Town NPCs not teleporting into very tall/thin homes at night, or houses where chairs did not have sufficient space
- Fixed Tall Hats having visual issues when riding a mount
- Fixed a visual framing issue with the Bamboo Lantern
- Fixed an issue where Stardust Guardian was no longer transparent when dyed
- Fixed an issue where some critters would super jump while underwater
- Fixed an issue where NPCs and Cats would sit in the same seat at night
- Fixed an issue where Vanity Rocket Boot trails were inconsistently prioritized and not always showing the correct trail
- Fixed an issue where Bones were still flagged as Ammo
- Fixed an issue where Lunar Drills/Chainsaws were getting prefixes they shouldn't
- Fixed an issue where the game did not Autopause in the Achievements menu
- Fixed a sell value inconsistency introduced by 1.4.1's crafting cost change for Adamantite/Titanium Ore bars
- Fixed an issue where Gamepad Master Mode slot visibility toggle did not work properly
- Jousting Lances can no longer receive melee speed prefixes. They already could not benefit from Melee speed, but this fixes some bugs caused by Melee speed modifiers that impacted them.
- Fixed an unusual exploit allowing you to force-teleport other players
- Fixed some stat inaccuracies where several OOA armor's stats did not match their tooltips. Also made a few text adjustments to clarify specific damage types.
- Fixed an issue where Hero's Shield was not giving its aggro boost
- Fixed a minor visual issue with Tinkerer's Workshop where some of its pixels were not visible
- Fixed Sky Dragon's Fury not animating when thrown on the ground
- Fixed Sky Dragon's Fury's secondary fire not inflicting Flask debuffs
- Fixed an issue where Souls in a Bottle were missing animation frames
- Fixed an issue where Hair 6 and Hair 94 had a conflict with capes
- Fixed an issue where Credits would scroll when paused
- Town NPCs will only fire on enemies if that enemy can be targetted (ideally, no more Plantera Hooks and the like)
- Fixed some inefficiency in Minion targetting that had performance impacts
- Fixed some exploits/oversight related to Bee Hives, Bunny Cannons, and Antlion Eggs
- Fixed an issue with enemy Bees attacking invincible enemies
- Fixed an issue where scrolling through Character Difficulty modes with Gamepad or WASD would follow a backwards order
- Fixed a handful of item drop rates that were not properly affected by luck (mostly some OOA drops). Will not impact actual drop rates to much of a substantial degree.
- Fixed an issue with a few leaf sprites that caused them to not correctly handle paint
- Fixed an issue where most falling tile projectiles would fall through platforms, except for regular Sand. All of them now land on the platform, except hostile Sand ball projectiles.
- Fixed an issue where some large texture items would scale down twice in chat
- Fixed an issue where Reaper Hood's head texture had an offset frame
- Fixed an issue where Robot Shirt worked with "hand" accessories, since its hands were incompatible with them. Robot Shirt and Pumpkin Shirt now do not work with Belt accessories either, for the same reason.
- Fixed an issue where some texture sizes weren't updated in the code, which prevented texture packs of those sprites from working properly
- Fixed an issue where the Paper Airplane projectile wasn't considered Ranged
- Fixed an issue where Molotov Cocktail didn't gain Frost Armor's Frostburn debuff
- Fixed an issue where Coin Gun would not prioritize Coin slots over Inventory slots
- Fixed a crash stemming from using the Clinger Staff near the top of the world when in reverse gravity
- Fixed an issue with some helmets drawing incorrectly on the minimap when in reverse gravity
- Fixed an issue where Brain of Cthulhu would despawn if there wasn't enough room to teleport
- Fixed an issue where Paper Airplanes weren't correctly dropping in stacks

III. Balance Changes:

Melee
Brand of the Inferno
- Use time decreased from 25 to 20 in light of recent buffs to similar tier weapons

Chlorophyte Claymore
- Increased damage from 80 to 95 in light of recent buffs to similar tier weapons

Chlorophyte Saber
- Increased damage from 48 to 57 in light of recent buffs to similar tier weapons

Christmas Tree Sword
- Projectiles now deal 75% of the base damage instead of 50%

Ranged
Super Star Shooter
- Reduced use time from 12 to 18 (THIS IS NOT A NERF!)
- Reduced damage from 70 to 60 (BEAR WITH ME, ITS NOT A NERF)
- Note: Due to immune frame time, this will actually result in more consistent damage, and is actually a buff. The damage decrease was required to offset the significantly increased damage.

Magic
Betsy's Wrath
- Partially reverting damage buff from 1.4.1, reducing damage from 110 to 100

Summons
Hornet Staff
- Increased damage from 11 to 12 (building upon the initial increase in 1.4.1 from 9 to 11)

Vampire Frog Staff
- Reverting damage buff from 1.4.1, reducing damage from 13 to 11. The AI/functionality changes from 1.4.1 have been more than sufficient on their own, and the extra damage was unneeded.

Obsidian Armor
- Reduced the Minion damage bonus on the helmet and legs from 9% to 8% each
- Reduced the Minion damage increase on the set bonus from 25% to 15%
- Reduced the Whip speed increase on the set bonus from 50% to 35%

Spider Staff
- Summoning Spiders will now attempt to systematically summon the different types of spiders in order, rather than randomly. Due to immune frame schenanigans, this may result in more consistent damage, though it does not actually increase the maximum potential of the weapon.

Optic Staff
- Enemy immune frames caused by Spazmamini and Retinamini attacks have been reduced from 16 to 12
- Increased Spazmamini's movement speed while pursuing enemies

Deadly Sphere Staff
- Enemy immune frames caused by Deadly Sphere attacks have been reduced from 10 to 8

Firecracker
- Reduced explosion proc damage from 3x of minion base damage to 2.75x

Cool Whip
- Cool Whip now inflicts Frostburn a short duration on hit
- Increased the movement speed of the Snowflake minion by 50%

Desert Tiger
- Now "bounces on" its current target if that target is in the air, staying more firmly latched on and dealing damage
- Increased scaling damage per "minion slot" expended slightly (from 33% of base damage to 40% of base damage)

Rainbow Crystal Staff
- Partially reverting the damage reduction in 1.4, increasing its damage from 80 to 130

Mounts/Wings/Accessories
Celestial Starboard
- Made some adjustments to improve its handling, while still keeping the fix that made sure that Starboard got full dash distance

Star Cloaks
- Only creates stars now when taking damage from enemy sources

Black Spot
- Slightly increased acceleration, to slightly offset for the loss of overall speed in 1.4.1

Crafting Recipes
Chlorophyte Bars
- Reduced crafting recipe from 6 to 5 ore per bar

Chlorophyte Bullets
- Reduced crafting efficiency from 70 bullets per bar to 60 bullets per bar (to roughly maintain parity with the Bar crafting cost change)

Enemy Immunities:
Snow Flinx - Removed their Poison immunity
Wall of Flesh - Removed its Poison immunity
Queen Bee - Added Poison immunity
Morning Wood - Added Poison immunity
Twins - Added Poison immunity
Martian Probes - Added Poison immunity
Granite Golem/Elemental - Added On Fire/Hellfire immunity
Betsy - Added On Fire/Hellfire immunity
Frozen Zombies - Added Frostburn Immunity
Clingers - Added Cursed Inferno Immunity
Dark Mage Skeletons - Added Poison immunity


Version 1.4.1.1 Changes -------------------------------------------------------------------------------------------

I. Changes and Bug Fixes
	Fixed a Mac only issue that caused a crash when attempting to host a server
	Fixed an bug causing it to be much harder than expected to achieve the happiness required for the Leading Landlord achievement
	Fixed an issue that prevented Linux from taking screenshots correctly
	Fixed an oversight within the Game Credits
	Fixed an issue in Dungeon code that was causing the same seed to create different worlds each time
	Fixed an issue preventing Master mode players from accessing all accessory slots with Gamepad
	Fixed a crash related to housing menu interaction with Gamepad
	Daybreak spears embedded in Moon Lord eyes will instantly explode and deal their bonus damage immediately if they eye closes
	Fixed an issue causing a kanji key to automatically replace some keybindings
	Fixed an issue causing Jungle Armor, Ancient Cobalt, and Molten Sets to not have the proper bonuses, while some other items (like Band of Regeneration) got them instead
	Fixed an bug causing the Hot Reels achievement to unlock when fishing in any liquid
	Fixed a bug causing Princess to not properly check for nearby NPCs, resulting in her being lonely even when surrounded by neighbors
	Players transformed into a Werewolf/Merman no longer have human faces when wearing certain accessories
	Fixed several grammatical/spelling issues in NPC dialogue
	Fixed a few minor item tooltip/flavor text issues
	Fixed a buggy dialogue line from Princess about Santa Claus
	Fixed a buggy dialogue line from Transformed Zoologist about the Princess
	Fixed Video Visage not applying dye to the screen when showing up on the Map
	Fixed an issue with the Witch Costume not properly showing legs underneath of it, even its own Witch Boots
	Fixed an issue when renaming chests that prevented the player from exiting their inventory easily
	Fixed an issue where Town NPCs would try to sit on Dynasty Chairs (they shouldn't be able to)

```


---

## 🤖 Assistant · 2026-08-09T11:43:44.513Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have the full official content for 1.4.1 (4889-5991), 1.4.1.1 (4864-4888), 1.4.1.2 (4698-4863).

Now I do a systematic comparison. Let me go section by section through the official 1.4.1 changelog.

**I.A New Content and Changes**
- Vanity contest winners: 6 sets — summary line 13 ✓ (summary lists Plaguebringer, Wandering, Timeless Traveler, Floret Protector, Capricorn, TV Head) ✓
- New Achievements ✓ line 14
- Credits sequence + music, Music Box (Journey's End) ✓ line 15
- Princess NPC ✓ line 16
- Flinx Fur Coat + Flinx Staff ✓ line 17
- New pre-Hardmode whip craftable at Dungeon-tier ✓ line 18 (Spinal Tap — zh wiki detail)
- Lavaproof Fishing Hook + Angler Tackle Bag Tinker ✓ line 19
- Bee Hives and Antlion Eggs craftable/placeable ✓ line 20
- Rainbow Cursor ✓ line 21

All new content covered. Good.

**I.B Vanity Accessory Changes**
- Ultrabright Helmet hair ✓ (line 228)
- Back-draw not mutually exclusive ✓ (line 220)
- Combat Wrench ✓ (221)
- Angel Halo ✓ (222)
- Head accessory subgroups ✓ (223)
- Blindfold visible with hats ✓ (224)
- Diving Helmet override ✓ (224)
- Obsidian Skull ✓ (224)
- Ginger Beard ✓ (224)
- Shield/Cape rework ✓ (225)
- Shields dye when invisible ✓ (225)
- Long hair compatible ✓ (226)
- Running boots trails vanity ✓ (227)
- Bone Glove hand vanity ✓ (228)
All covered.

**I.C Other Content/Design Changes**
- Journey Mode duplication menu overhaul ✓ (line 233)
- Misc option ✓ (233)
- Boss Mask sprites ✓ (229)
- Orange/Amber Phasesaber sprite ✓ (229)
- Torch God Otherworld track ✓ (242)
- Bestiary wave-based drops ✓ (234)
- Loading tips when connecting to server ✓ (235)
- Thunder volume ambient ✓ (241)
- Plantero's Sombrero return — NOT in summary! Missed.
- Menu settings reorganization ✓ (236)
- FNA update ✓ (257)
- RGB SteelSeries ✓ (257)
- Localization ✓ (257)

So "Plantero's Sombrero has made its triumphant return" is missed. That's an item return (in C, design change).

**II Bug fixes** — summary consolidates. Need to check for count discrepancies and important items. Let me check each subsection briefly:

II.A Major/crashes: summary line 266 covers "滚动备份删除、地图图标崩溃、坐骑动画罕见崩溃、剪贴板崩溃、云端存档同步、分辨率上限、关闭挂起、Mac 主机崩溃、Linux 截图" — note Linux screenshot is actually a 1.4.1.1 fix, but minor. Jungle Shrine issue is in line 215 (世界生成). All 9 items of II.A covered roughly.

II.B Enemy/NPC bugs: let me check line 267 list vs official:
Official II.B items (26):
1. NPCs stand in water until drowned — NOT in summary! "Fixed an issue with NPCs deciding to stand in escapable water until they drowned" — missed.
2. Empress day Terraprisma ✓
3. EoC/Retinazer/Spazmatism spin forever ✓
4. Lunatic Cultist/Martian Saucer target ✓
5. Antlion Swarmers 10x money ✓
6. Angry Nimbus platforms ✓
7. Queen Slime boost twice / Empress not at all ✓
8. Floating enemies platforms ✓
9. Wooden Mimics not spawning ✓
10. OOA Tier 2 Goblin Bombers ✓
11. Slime Rain Journey slider ✓
12. Flying Dutchman ✓ (261)
13. Big Mimics sync ✓ (261)
14. Devourer banners ✓
15. Truffle Worms Lifeform Analyzer ✓
16. Twins boss bag ✓ (261)
17. Hemogoblin Sharks platforms ✓
18. Spider animation frames ✓
19. Golem body parts ✓
20. Moon Lord NPC smoothing ✓
21. Torch God count torches twice ✓
22. Torch God lose progress ✓
23. Corruption housing invalid ✓
24. Angry Dandelions MP targeting ✓
25. Traveling Merchant time paused ✓
26. Ocean critters spawning on screen ✓
27. Moon Lord attack MP ✓ (261)

So II.B: only #1 NPC drowning missed.

II.C Combat/Gameplay/Items (38 items). Summary line 268. Check:
1. Whip size modifier inverse speed ✓
2. Blood Arrows ✓
3. Desert Tiger pounce magic ✓
4. Golf Cart ✓
5. Horse mounts ✓
6. Lucky Coin ✓
7. Terraprisma return ✓
8. Titanium ranged set ammo ✓
9. Homing projectiles Duke Fishron ✓
10. Hornet/Imp/Tempest/UFO/Stardust Cell knockback ✓
11. Beach Balls ✓
12. Queen Bee sync — hmm, summary line 261 mentions "Queen Slime 同步问题（多人冲锋/传送不稳）" — wait, official says "Queen Bee" (fixing syncing issues with Queen Bee). Summary line 261 says "修正 Queen Slime 同步问题（多人冲锋/传送不稳）" — Queen Slime vs Queen Bee! That's a factual error. Actually official: "Fixed some syncing issues with Queen Bee that resulted in erratic charging/teleportation in multiplayer". The summary wrote Queen Slime. That's a mistranslation error worth noting.
13. Zenith gamepad range — not explicitly; summary mentions Zenith only in visual (vertex shaders). Missed but minor gamepad.
14. Life Drain hit detection ✓
15. Celestial Starboard dashes ✓
16. Snow teleport Chilled ✓
17. Snowman Cluster Fragments ✓
18. Golf Ball camera extreme range — not in summary; minor.
19. Weapon racks right-click — not in summary.
20. Items float when petting animal — not in summary; minor visual.
21. Smart cursor painting slots ✓ (implied in 智能光标 items? summary mentions Smart Cursor herb placement, Logic Sensors, pumpkin placement). Painting one missed.
22. Dart Pistol two Deadly prefixes ✓
23. Sanguine/Terraprisma Summon Lock On ✓
24. Valor in Golden Lock Boxes ✓
25. Gender button break ✓ (no, not in summary; minor)
26. Dodged attacks debuffs ✓
27. Magic Missile clip through blocks in liquids ✓
28. Catching stacked fish full inventory ✓
29. Game minimized but active — not in summary; minor.
30. Journey/Expert debuff times ✓
All main ones covered. Missed minor: Zenith gamepad range, golf ball camera range, weapon racks right-click while using, petting animal float, gender button, minimized game. These are minor.

II.D Tile/Block/Worldgen bugs (36 items). Summary line 269:
1. Bamboo/Wrought Iron Fences trees ✓
2. Sand dupe ✓
3. Logic Sensors Block Swap ✓
4. Clentaminator Vicious Mushrooms ✓
5. Evil thorns stopped growing ✓
6. Surface Mushroom background ✓? Summary line 269: "环境改造不转化恶性蘑菇" is #4. #6 "Surface Mushroom background darkening requiring too many mushroom blocks" — not in summary. minor.
7. Coral/Shells regrow over actuated blocks ✓
8. Demon Altars Rolling Cacti ✓
9. Golf Flags wind — not in summary; minor.
10. Ropes merge Smooth Marble ✓
11. Crystal Shards sync ✓ (261)
12. Jungle/Mushroom vines underground ✓
13. Weapon Racks removed MP ✓ (261 木人模特/帽架? actually that's mannequins; weapon racks MP is separate — line 261 says "木人模特/帽架多人被炸坏" which is II.D Mannequins/Hat Racks bombed. Weapon Racks removal MP missed; minor)
14. Grappling hook crafted manually usable ✓
15. Falling blocks de-slope platforms ✓
16. Offline Gemspark blend — missed; minor.
17. Hardcore ghosts tiles ✓
18. Sand duplicate falling ✓
19. Falling blocks land on tiles / sync — partially covered (坠落块), fine.
20. Portal Gun Stations confetti ✓
21. Auto-Select confetti ✓
22. Pressure plates floating ice ✓ (216)
23. Living Mahogany Trees jungle grass ✓ (216)
24. Boulder Traps Temple ✓ (216)
25. Build off beams ✓
26. Pots out of bounds ✓ (216)
27. Gnome Statues framing — missed; minor.
28. Crimsand dust — missed; minor.
29. Snow Clouds dust — missed.
30. Stone Platforms immune to lava ✓
31. Dirt Bombs grass ✓
32. Pylon NPC detection ✓
33. Smart Cursor herb placement ✓
34. Mannequins/Hat Racks MP ✓ (261)
35. Smart Cursor pumpkin ✓
Mostly covered; minor misses only.

II.E Visual/Art/Sound (44 items). Summary line 270 covers择要: vertex shaders, capes/tax collector sitting, Desert Tiger dye, minecart dust, dead wings, reverse gravity, illuminant paint, Stardust Guardian. Others minor: armpit pixels, Nebula workbench, etc. Fine. But note: "audio tracks compressed at 60%" ✓ line 243. "Music volume 0 music boxes" ✓ 242. OK.

II.F UI/Menu/Journey (27 items). Summary line 237 covers several. Minor misses: Red Squirrel Cage, Peace Candle mouseover, eye color randomize, Hover Control saved, windowed fullscreen maximized, settings interrupt movement, spacing options, Torch God Favor button gamepad, controls menu gamepad, double inputs, text search boxes no limit, Fungi Bulb bestiary, Torch God bestiary entry unlock. All minor UI bugs; consolidated. Acceptable per task instructions (bug fixes just count).

II.G Text/Tooltips (8 items) — summary line 307 for 1.4.1.1 only; for 1.4.1, minor text issues not mentioned explicitly but negligible. Note "favorites file characters" missed; minor.

II.H Server/MP (7 items) — summary line 262 covers all 7? Official: world name/seed length, special seeds, corrupt worlds, maxPlayers 255, Liquid Spam, items shoved, rightmost edge spawn ✓. All covered.

**III Balance — Melee (A)**: compare with summary lines 25-51.

1. Terra Blade line intro: Mothron only post-Plantera ✓
2. True Night's Edge ✓ (1.5x, autoswing, crafted with 3 boss souls) ✓
3. True Excalibur: 66→70 ✓ autoswing ✓ pierce once ✓ Excalibur + Chlorophyte Bars ✓
4. Terra Blade ✓
5. Beam Sword ✓
6. Brand of the Inferno ✓
7. Sunfury ✓
8. Arkhalis ✓
9. Chain Guillotine ✓
10. Ghastly Glaive ✓ (36→20 + effect) ✓
11. Anchor ✓
12. Sergeant United Shield ✓
13. Scourge of the Corruptor ✓
14. Yoyos ✓
15. Light's Bane ✓
16. Muramasa ✓
17. Fiery Greatsword ✓
18. Beekeeper ✓
19. All Phaseblades ✓
20. Night's Edge ✓
21. Bananarangs ✓
22. Thorn Chakram/Flamarang ✓
23. Sleepy Octopod ✓
24. Flying Dragon ✓
25. Sky Dragon's Fury ✓
26. Starlight ✓
27. Daybreak ✓
All melee covered! 

Wait — Chain Guillotine official says "Damage increased from 43 to 59" ✓ summary line 33 ✓.

**III.B Ranged**: summary lines 55-68.
1. Onyx Blaster: "Damage decreased by 4" — official doesn't give absolute numbers. Summary says 28→24. zh wiki detail; official says decrease by 4. Not a contradiction (28-4=24). OK.
2. Quad-Barreled Shotgun ✓ (24→17, 4→6, 45→55, Arms Dealer post-Skeletron) ✓
3. StakeLauncher ✓
4. Blowpipe ✓
5. Jack 'O Lantern Launcher ✓
6. Dart Gun/Dart Rifle revert ✓ + ammo kept ✓
7. Tsunami ✓
8. Nano Bullets ✓
9. Beenades ✓
10. Bone Arrows ✓
11. Chlorophyte Bullets ✓
12. Cursed Bullets ✓
13. Meteor Shot ✓
14. High Velocity Bullets ✓
15. Crystal Bullets ✓
16. Jester Arrows ✓
17. Unholy Arrows ✓
All covered.

**III.C Magic**: summary lines 72-86.
1. Life Drain ✓
2. Nightglow ✓
3. Shadowbeam Staff ✓
4. Unholy Trident ✓
5. Poison Staff ✓
6. Venom Staff ✓
7. Medusa Head ✓
8. Crystal Vile Shard ✓
9. Nettle Burst ✓
10. Wasp Gun ✓
11. Razorblade Typhoon ✓
12. Magical Harp ✓
13. Blood Thorn ✓
14. Magic Missile ✓
15. Flamelash ✓
16. Flower of Fire ✓
17. Space Gun ✓
18. Charged Blaster Cannon ✓
19. Betsy's Wrath ✓
20. Stellar Tune ✓
All covered!

Note: Magic Missile official: "Use Time decreased from 18 to 22" — that's an error in official text (18→22 is an increase, and summary says "Use Time 18→22"). Official literally says "decreased" but numbers 18 to 22. Summary just says 18→22. Fine.

**III.D Summoning**: summary lines 90-103.
1. Whip damage penalties ✓ (all 5 values match)
2. Whip range ✓
3. Whips + Flasks ✓
4. Leather Whip ✓
5. Finch Staff ✓
6. Optic Staff ✓
7. Sanguine Staff ✓ (60→66)
8. Xeno Staff ✓
9. Tempest Staff ✓
10. Hornet Staff ✓
11. Vampire Frog Staff ✓
12. Pygmy Staff ✓
13. Desert Tiger Staff ✓
14. Frost Hydra Staff ✓
15. Explosive Trap Staff ✓
16. Kaleidoscope ✓
All covered.

**III.E Armor**: summary lines 107-129.
1. Cactus ✓
2. Mining ✓ (2.4→12)
3. Gladiator ✓
4. Fossil ✓
5. Wizard Hat ✓ Magic Hat ✓
6. Meteor ✓
7. Jungle ✓
8. Necro ✓
9. Obsidian ✓
10. Molten ✓
11. Cobalt ✓
12. Palladium ✓
13. Mythril ✓
14. Orichalcum ✓ — wait: official says "Orichalcum Mask Melee Speed bonus increased from 7% to 11%" but summary line 120 says "Melee Mask 伤害 7%→11%、暴击 7%→11%"! Official: Damage bonus 7→11 AND Melee Speed bonus 7→11. Summary says damage and crit (暴击) 7→11. That's a discrepancy: official = damage + melee speed; summary = damage + crit. Worth flagging as potential error.
15. Adamantite ✓
16. Titanium ✓
17. Frost ✓
18. Forbidden ✓
19. Chlorophyte ✓ (50→40)
20. Spectre Mask ✓ (burst limit 1000→1500, recovery 250→400)
21. Spectre Hood ✓
22. Crystal Assassin ✓
23. Squire ✓ (20→15)
24. Monk ✓ (10→15)
25. Huntress ✓ (+10% ammo)
26. Apprentice ✓
27. Valhalla Knight ✓
28. Shinobi ✓
29. Red Riding ✓
30. Dark Artist ✓
All covered.

**III.F Accessories**: summary lines 133-150.
1. Band of Regeneration/Charm of Myths ✓
2. Band of Starpower/Panic Necklace ✓
3. Bone Glove ✓
4. Brain of Confusion ✓
5. Celestial Cuffs ✓
6. Diving Helmet ✓
7. Feral Claws/Titan Glove ✓
8. Fledgling Wings/Lucky Horseshoe ✓
9. Flesh Knuckles/Berserker Gloves ✓
10. Fire Gauntlet ✓
11. Hero Shield ✓
12. Honeycomb series ✓
13. Jellyfish Necklace ✓
14. Lava Charm ✓
15. Magma Stone ✓
16. Molten Quiver ✓
17. Obsidian Rose ✓
18. Panic Necklace ✓
19. Pygmy Necklace ✓
20. Star Cloak series ✓
All covered.

**III.G Tools and Mounts**: summary lines 154-162.
1. Reaver Shark ✓
2. Bone Pickaxe ✓
3. Chlorophyte Jackhammer ✓
4. Mechanic's Rod ✓
5. Fiberglass Fishing Pole ✓
6. Scarab Fishing Rod ✓
7. Sitting Duck Rod ✓
8. Living Wands ✓
9. Black Spot ✓
10. Scutlix ✓ (500→850, 100→150)
11. Dark Mage's Tome ✓
12. Witch's Broom ✓
13. Flamingo ✓
14. Horse Mounts ✓
15. Jewel of Light/Pumpkin Scented Candle ✓
16. Suspicious Looking Tentacle ✓
All covered.

**III.H Crafting and Drops**: summary lines 166-178.
1. Blood Rain Bow/Chum Caster/Vampire Frog Staff ✓
2. Bloody Tear ✓
3. Sanguine Staff ✓
4. Blade Staff ✓
5. Kites — official: "Kites dropped from Balloon Slimes are roughly 3x more likely. Paper airplanes mostly the same, but now drop in small stacks. Bone Serpent Kite: 4% to 6%"
Summary line 170: "风筝/纸飞机：Windy Balloon 风筝掉率 1/260→1/72；Paper Airplanes 3/260→1/72 且堆叠 1→2–5；Bone Serpent Kite 1/25→1/15"
Official: kites ~3x more likely; paper airplanes mostly the same (but small stacks); Bone Serpent Kite 4%→6%.
Summary: kites 1/260→1/72 (~3.6x, consistent with "3x"); paper airplanes 3/260→1/72 — official says "mostly the same"! That contradicts "3/260→1/72" (which is 3.6x more likely). Hmm. zh wiki may have specific numbers. Official says paper airplanes are "mostly the same" — so 3/260→1/72 is questionable. And Bone Serpent Kite: official 4%→6% (1/25→1/15 = 4%→6.67%, roughly consistent). So the kite numbers are zh-wiki specifics; paper airplane rate change contradicts "mostly the same". Flag as possible discrepancy.
6. Sturdy Fossil — official: Tomb Crawlers chance to drop small amounts; Oasis/Mirage Crates chance to include. Summary adds "Basilisk 1/3→100%、数量 1→1–3" — that's NOT in official 1.4.1 changelog! Official only lists Tomb Crawlers and crates. Basilisk change is extra (zh wiki added). Per task instruction #3, one sentence.
7. Valor/Muramasa ✓
8. Torches ✓
9. Mana Crystal ✓
10. Early Game Ore ✓ (all values match)
11. Hardmode Ore Swords ✓
12. Adamantite/Titanium Bars ✓
13. Jester Arrows ✓ (20→10)
14. Super Star Shooter ✓
All covered.

**III.I Buffs/Debuffs**: summary lines 182-188.
1. Frostburn ✓ (8 DPS)
2. Cursed Inferno ✓ (24 DPS enemy, 12 player)
3. Venom/Acid Venom ✓ (30/15)
4. Ichor ✓ (20→15)
5. Oiled ✓ (+25 DPS flat)
6. Thorns Potion ✓ (1/3→100%)
7. Dryad's Blessing ✓ (20→50)
8. Debuff Immunity Overhaul ✓ (well summarized)
All covered.

**III.J Threats and Enemies**: summary lines 192-206.
1. Vicious Goldfish ✓
2. Blood Feeder ✓
3. Ghosts ✓
4. Antlion Larvae ✓
5. Antlion Eggs ✓
6. Rolling Cactus ✓
7. Angry Dandelion ✓
8. Rock Golem ✓
9. Wall of Flesh ✓
10. Ice Elemental ✓
11. Jungle Creeper ✓
12. Lac/Cyan/Cochineal Beetles — official: "Reduced rarity from 1 to 2 on the Lifeform Analyzer". Summary line 202: "Lac/Cyan/Cochineal Beetle：生命体分析仪稀有度 2→1". NUMERIC CONTRADICTION! Official: rarity reduced from 1 to 2 (lower priority on analyzer = higher number). Summary says 2→1 (which would make them higher priority, opposite direction). Flag this.
13. Phantasm Dragon ✓
14. Hoppin Jack ✓
15. Vortex Lightning ✓
All covered.

**III.K Miscellaneous and QoL**: summary lines 247-257.
1. Graveyard Threshold ✓ (+1)
2. Town Happiness — official: (a) "So Much Space" boost reduced by half; (b) Like/Dislike/Love/Hate increased by 20%; (c) crowding now starts at 4 NPCs (up to 3 without crowding); (d) town detection size doubled.
Summary line 206: "喜欢/反感/喜爱/讨厌因素加减成提升 20%；不触发'拥挤'的城镇 NPC 数 3→4；城镇检测尺寸翻倍"
MISSING: "So Much Space" factor boost reduced by half! That's a numeric/mechanic omission. Flag.
3. Block Swap ✓
4. Meteorite Ore ✓
5. Jungle/Corrupt Worldgen ✓ (210)
6. Armed Zombie statues ✓ (211)
7. Shadow Chests ✓ (212)
8. Pyramid Rarity ✓ (213)
9. Enchanted Sword Shrines ✓ (213)
10. Sandstorm ✓ (214)
11. Rock Lobster — sell value 20 silver→10 silver — NOT in summary! Missed (minor economy item).
12. Sakura/Yellow Willow Saplings — price 3 gold→1 gold — NOT in summary! Missed.
13. Special Furniture Crafting Stations ✓ (255)
14. Mirage Fish/Pixie Fish — uncommon instead of rare — NOT in summary! Missed.
15. TreeHit limit 200→500 ✓ (254)
16. Sharpening Stations — Merchant sells in Hardmode — NOT in summary! Missed.
17. Books — Wizard sells books, cost 3→15 silver — NOT in summary! Missed.
18. 1/3/5 Timers — also sold by Mechanic — NOT in summary! Missed.
19. Mushrooms potion sickness 60→30 ✓ (250)
20. Fishing decreasing returns ✓ (251)
21. Pylons Celestial Invasion ✓ (252)
22. Journey Mode grappling hook ✓ (253)
23. Boss Bestiary entries ✓ (256)

So missed in III.K: Rock Lobster, Sakura/Yellow Willow Saplings, Mirage/Pixie Fish, Sharpening Stations, Books, Timers, "So Much Space" reduced by half, Plantero's Sombrero (from I.C).

**1.4.1.1 section** (4864-4888, 25 items): summary lines 276-307. Check:
1. Mac host crash ✓ (consolidated)
2. Leading Landlord happiness ✓ (280)
3. Linux screenshots ✓ (consolidated)
4. Game Credits oversight ✓ (300)
5. Dungeon seed ✓ (282)
6. Master mode gamepad accessory slots ✓ (283)
7. Housing menu gamepad crash ✓ (consolidated)
8. Daybreak Moon Lord eyes ✓ (281)
9. Kanji key ✓ (305)
10. Jungle/Ancient Cobalt/Molten sets ✓ (292)
11. Hot Reels ✓ (304)
12. Princess nearby NPCs ✓ (287)
13. Werewolf/Merman faces ✓ (297)
14. NPC dialogue grammar ✓ (307)
15. Item tooltips ✓ (307)
16. Princess Santa dialogue ✓ (287)
17. Transformed Zoologist ✓ (287)
18. Video Visage dye ✓ (298)
19. Witch Costume legs ✓ (299)
20. Renaming chests ✓ (306)
21. Dynasty Chairs ✓ (288)
22. Bone Glove equip right-click ✓ (293)
All 1.4.1.1 items covered! Excellent.

**1.4.1.2 section** (4698-4863): summary lines 311-377. Check Changes:
- Localization ✓ (315)
- Town NPC distance revert ✓ (319)
- Space bonus 3-NPC ✓ (320)
- Skeletron Prime planter boxes ✓ (321)
- Capes sitting/riding ✓ (323)
- Queen Slime minions Slime Staff ✓ (322)
- Creative/bestiary pause searching ✓ (324)
- Timeless Traveler sprites ✓ (325)
- Spectre Goggles ✓ (325)

Bug fixes: music volume, happiness rounding, crowded 1 NPC, Chinese localization, Ronin fireflies, skin brighter, Cracked Dungeon bricks, Journey time rate credits, credits texture pack crash, Life Drain PVP, Prismatic Lacewing, Princess discussing bosses (summary 287? no — summary line 313-377... "Princess discussing bosses/threats not defeated" — check summary... I don't see it. Minor miss), Princess party hat (missed, minor), Video Visage reverse gravity ✓ (365), vanity ears ✓, tail accessories ✓, hair draw double ✓, NPC dialogue ✓, town NPC teleport tall homes ✓ (361), tall hats riding ✓ (365 partially), bamboo lantern ✓, stardust guardian ✓, critters super jump ✓, NPC cats seat ✓, vanity rocket boot trails ✓, bones ammo ✓, lunar drills prefixes ✓, autopause achievements ✓, sell value adamantite ✓, gamepad master mode ✓, jousting lances ✓, teleport exploit ✓, OOA armor stats ✓, Hero Shield aggro ✓, Sky Dragon's Fury ground anim ✓ + flask debuffs ✓, souls in a bottle ✓, hair 6/94 ✓, credits paused ✓, town NPCs fire targets ✓, minion targeting performance (minor, missed), bee hives exploits ✓, enemy bees ✓, character difficulty scroll ✓, luck drop rates ✓, leaf sprites paint ✓, falling tiles platforms ✓, large texture items ✓, reaper hood ✓, robot shirt ✓, paper airplane ranged ✓, molotov frostburn ✓, coin gun ✓, clinger staff crash ✓, helmets minimap ✓, brain of cthulhu ✓, paper airplane stacks ✓.

Balance 1.4.1.2: all covered in summary 329-347: Brand of Inferno ✓, Chlorophyte Claymore ✓ Saber ✓, Christmas Tree Sword ✓, Super Star Shooter ✓, Betsy's Wrath ✓, Hornet ✓, Vampire Frog ✓, Obsidian Armor ✓, Spider ✓, Optic ✓, Deadly Sphere ✓, Firecracker ✓, Cool Whip ✓, Desert Tiger ✓, Rainbow Crystal ✓, Celestial Starboard ✓, Star Cloaks ✓, Black Spot ✓, Chlorophyte Bars ✓, Bullets ✓.

Enemy immunities: Snow Flinx ✓, WoF ✓, Queen Bee ✓, Mourning Wood ✓, Twins ✓, Martian Probes ✓, Granite ✓, Betsy ✓, Frozen Zombies ✓, Clingers ✓, Dark Mage Skeletons ✓ (352). All covered.

Now compile the missing items list:

**Missed items (official present, summary absent):**

I.C (Other Content/Design):
1. Plantero's Sombrero returns → 新增内容/其他内容

III.K (Misc QoL):
2. Rock Lobster sell value 20s→10s → 机制系统改动-其他
3. Sakura/Yellow Willow Saplings price 3g→1g → 机制系统改动-其他
4. Mirage Fish/Pixie Fish rare→uncommon → 机制系统改动-其他
5. Sharpening Stations: Merchant sells in Hardmode → 机制系统改动-其他
6. Books: Wizard sells books, 3→15 silver → 机制系统改动-其他
7. 1/3/5 Timers also sold by Mechanic → 机制系统改动-其他
8. Town Happiness "So Much Space" factor boost halved → NPC与Boss与AI (Town Happiness)

II.B (Enemy/NPC bugs):
9. NPCs standing in escapable water until drowning → Bug修复-NPC

Minor bug-fix misses (per instruction, list up to 5 most important):
- Zenith lacking full screen range on Gamepad (II.C)
- Smart Cursor Painting ammo slot inconsistency (II.C)
- Surface Mushroom background darkening requiring too many mushroom blocks (II.D)
- Favorites file can't support some characters in world/player names (II.G)
- Minion targeting performance fix / Princess discussing undefeated bosses (1.4.1.2)

**Numeric contradictions:**
1. Lac/Cyan/Cochineal Beetles Lifeform Analyzer rarity: official 1→2 (reduced priority); summary 2→1. Direction reversed.
2. Orichalcum Mask: official = damage 7→11 + melee speed 7→11; summary = 伤害 7→11 + 暴击(crit) 7→11. Second stat wrong type.
3. Paper Airplanes: official "mostly the same, but now drop in small stacks"; summary "3/260→1/72" (implies 3.6x rate increase). Contradiction.
4. Queen Bee sync bug (II.C) misattributed as Queen Slime in summary (item identity error, not numeric but factual).
5. Also check: Bone Serpent Kite official 4%→6%, summary 1/25→1/15 = 4%→6.67%. Close enough (zh wiki rounding); borderline. I could mention as minor.
6. Kites: official "roughly 3x more likely", summary 1/260→1/72 ≈ 3.6x — consistent enough, not a contradiction.

Also check Sanguine Staff: official "attack speed increased from 60 to 66 (how long it takes to make their attack circuit)" — summary says "血蝠攻击速度 60→66（攻击路线耗时）" ✓ consistent.

Explosive Trap cooldown 110→90 ✓. 

One more check: summary line 60 says Dart Pistol/Rifle revert "伤害分别 33→28、62→52（注：wiki 标注此条实际到 1.4.2.2 才生效）" — official just says reverted; the numbers are zh wiki addition; the note is fine.

Also verify summary line 175 early ore: 镐 12→10（铜锡 8）✓ matches.

Summary line 19 "Lavaproof Tackle Bag（熔岩防钓具袋）" — official calls it "Lavaproof Fishing Hook + Angler Tackle Bag Tinker" (no name). zh wiki name; fine.

Also the summary line 4: 1.4.1 codename "Rounding Out the Journey" — not in official changelog but common knowledge; fine.

Also check "Crystal Assassin" — official: Removed 15% movement speed set bonus, boots 10→20% — summary ✓.

Check summary line 128: Crystal Assassin "头 -10% 魔力消耗" — official "Added 10% Mana Cost reduction to the Hood" ✓.

Check Frost armor line 123 ✓.

One thing: summary line 206 says "城镇检测尺寸翻倍（1.4.1.2 会回调检测尺寸）" ✓ noted.

Also Town Happiness crowding: official "up to 3 NPCs without crowding, begins at 4" — summary "不触发'拥挤'的城镇 NPC 数 3→4" — hmm, official says previously crowding began... it's ambiguous but the summary is consistent.

Now also double-check one number: summary line 49 Sky Dragon's Fury "弹幕伤害 75%→50% 基础伤害（单发实际 52，原 70）" — official: "Projectile damage decreased from 75% of base to 50%... instead of doing 52 (75% of 70) it will do 70 (50% of 140)". So official says OLD = 52, NEW = 70. Summary says "单发实际 52，原 70" — that's REVERSED! Summary states the new value as 52 and original as 70, but official says original was 52 and new is 70. That's a numeric contradiction! Great catch.

Let me double check summary line 49: "Sky Dragon's Fury：伤害 70→140；弹幕伤害 75%→50% 基础伤害（单发实际 52，原 70）". Yes — parenthetical reversed. Official: previously did 52 (75% of 70), now does 70 (50% of 140). So correct parenthetical should be "原 52，现为 70". Flag.

Any others with parenthetical inversions? Flying Dragon line 48: "伤害 90→180；视线无法直达的弹幕只造成一半伤害（即 90）" ✓ correct.

Also check Morning Star "25%→5%" ✓.

Check summary line 90 Cool Whip 33→30 ✓ Durendal 30→20 ✓ Morning Star 25→5 ✓ Dark Harvest 30→10 ✓ Kaleidoscope 15→10 ✓.

OK. Also the Obsidian armor in 1.4.1.2: official helmet/legs 9→8, set bonus minion 25→15, whip speed 50→35 ✓ summary line 337 ✓.

Super Star Shooter 1.4.1.2: official use time 12→18, damage 70→60 ✓ summary 332 ✓.

Now, count of bug fixes for the "count difference" part:
Official 1.4.1 bug fixes: II.A=9, II.B=27, II.C=30, II.D=35, II.E=44, II.F=27, II.G=8, II.H=7. Let me count more carefully.

II.A: 
1. Rolling backups
2. Jungle Shrines
3. player map icons crash
4. mount idle animations
5. Peripheral lighting
6. Mac/Linux resolution
7. indefinitely hanging after closing
8. clipboard crash
9. Cloud save map sync
= 9 items.

II.B: I count the list:
1. NPCs water drown
2. Empress Terraprisma
3. EoC/Retinazer/Spazmatism spin
4. Lunatic Cultist/Martian Saucer
5. Antlion Swarmers money
6. Angry Nimbus
7. Queen Slime boost
8. floating enemies
9. wooden Mimics
10. OOA Tier 2 bombers
11. Slime Rain slider
12. Flying Dutchman
13. Big Mimics
14. Devourer banners
15. Truffle Worms
16. Twins boss bag
17. Hemogoblin Sharks
18. spider animation
19. Golem body parts
20. Moon Lord smoothing
21. Torch God count twice
22. Torch God progress
23. Corruption housing
24. Angry Dandelions MP
25. Traveling Merchant paused
26. Ocean critters
27. Moon Lord attack MP
= 27 items.

II.C:
1. whip size modifiers
2. Blood Arrows
3. Desert Tiger pounce
4. Golf Cart
5. Horse mounts
6. Lucky Coin
7. Terraprisma return
8. Titanium ranged
9. homing projectiles Duke
10. minions knockback
11. Beach Balls
12. Queen Bee sync
13. Zenith gamepad
14. Life Drain hit detection
15. Celestial Starboard dashes
16. Snow Chilled
17. Snowman Cluster Fragments
18. extreme range golf ball camera
19. Weapon Racks right click
20. petting animal float
21. Smart Cursor Painting
22. Dart Pistols prefixes
23. Sanguine/Terraprisma lock on
24. Valor Golden Lock Boxes
25. Gender button
26. dodged attacks debuffs
27. Magic Missile liquids
28. stacked fish
29. minimized but active
30. Journey/Expert debuff times
= 30 items.

II.D:
1. Bamboo/Wrought Iron Fences
2. sand dupe
3. Logic Sensors
4. Clentaminator
5. Evil thorns
6. Surface Mushroom background
7. Coral/Shells
8. Demon Altars
9. Golf Flags wind
10. Ropes marble
11. Crystal Shards
12. Jungle/Mushroom vines
13. Weapon Racks MP
14. grappling hook crafted
15. falling blocks de-slope
16. Offline Gemspark
17. Hardcore ghosts
18. Sand duplicate
19. falling blocks land/sync
20. Portal Gun confetti
21. Auto-Select confetti
22. pressure plates ice
23. Living Mahogany
24. Boulder Traps Temple
25. beams
26. pots out of bounds
27. Gnome Statues
28. Crimsand dust
29. Snow Clouds dust
30. Stone Platforms lava
31. Dirt Bombs
32. Pylon NPC detection
33. Smart Cursor herbs
34. Mannequins MP
35. pumpkin placement
= 35 items.

II.E: let me count roughly: 44 items (I'll say ~44). Let me count:
1. Vertex Shaders
2. Capes Tax Collector sitting
3. Desert Tiger dye
4. Minecarts dye slot
5. Etherian Goblin positioning
6. armpit transparent pixel
7. Nebula Workbench
8. Zoologist emote
9. wings dead
10. Water Peace Candles ropes
11. Hallowed Palm Potted
12. Corrupt Torches snow dust
13. Goldfish Bowl high
14. Goldfish Bowl pixel
15. Crimson Capture
16. Gnome tile pixel
17. Palm Armor
18. Mystic Snake Coil
19. reverse gravity body
20. Illuminant Paint
21. banners item sprite
22. Stardust Guardian pause
23. Martian SFX
24. audio 60% quality
25. Music Boxes volume 0
26. light spreading
27. Crimson background
28. hellbats background
29. Tree top framing
30. minions kites flip
31. Angel Halo stealth
32. Tea Coffee sprites
33. invisible bald map icons
34. inner tubes
35. coins sparkles
36. long coat sitting
37. Vine/Seaweed screenshots
38. Magic Missile spike
= 38 items. OK ~38.

II.F:
1. Guide Crafting slots
2. Celestial Pillar health bars
3. Red Squirrel Cage
4. Peace Candles icon
5. boss minimap icons
6. Mana Cloak Star
7. Eye color
8. Quick Stack coins
9. Journey sliders maxing
10. rain paused
11. Sky effects paused
12. rain start/stop paused
13. invasions paused
14. Journey Menu hotkey autopause
15. autopause Keybindings
16. spawn rate slider 0.1x
17. text search boxes
18. Fungi Bulb bestiary
19. Hover Control
20. windowed fullscreen
21. settings movement inputs
22. spacing options
23. Torch God Favor gamepad
24. Gamepad Controls menu
25. double inputs
26. Torch God bestiary unlock
27. Torch God bestiary tags
= 27 items.

II.G:
1. tooltips crit chance
2. Cat pet names
3. Tax Collector Agnew
4. loading tips
5. Demolitionist ebonrock
6. minor text grammar
7. achievement descriptions
8. asset capitalization
9. favorites file characters
= 9 items.

II.H = 7 items.

Total 1.4.1 bug fixes ≈ 9+27+30+35+38+27+9+7 = 182 items.

Summary's consolidated coverage: line 266 (~9 crashes), 267 (~26 NPC), 268 (~29 combat), 269 (~25 tiles), 270 (~8 visual), 237 (UI ~6), 261-262 (MP ~12). Roughly 120+ items covered explicitly or in groups; ~30-40 minor bug-fix items omitted (mostly visual/UI trivia). 

Let me pick the 5 most important missed bug fixes:
1. Zenith lacking full screen range on Gamepad (II.C) — affects flagship weapon on gamepad
2. Smart Cursor Painting ammo slot inconsistency (II.C)
3. Surface Mushroom background requiring too many mushroom blocks (II.D)
4. Favorites file can't support some characters/symbols in world/player names (II.G)
5. Town NPC standing in escapable water until drowned (II.B) — this is gameplay-relevant, arguably belongs in遗漏条目 not just bug count.

Now percentages: content coverage. Official sections I.A/B/C fully covered except Plantero's Sombrero. Balance sections III.A-H, I, J fully covered. III.K has 7 misses out of ~23 items. Bug fixes ~80% covered by consolidation.

Overall completeness estimate: ~90-92%. Verdict: needs minor revision (add III.K missing items, fix 3 numeric/directional errors).

Actually let me reconsider the kite numbers more carefully since summary gives specific rates. Official says "Kites dropped from Balloon Slimes are roughly 3x more likely to drop. Paper airplanes are mostly the same, but now drop in small stacks." Summary: "Windy Balloon 风筝掉率 1/260→1/72" — 1/72 ≈ 3.6x of 1/260, consistent with "roughly 3x". "Paper Airplanes 3/260→1/72" — contradicts "mostly the same". Hmm, but maybe the zh wiki is right and official wording loose. Per the task, official is authoritative: flag paper airplane rate as contradiction (official says rate unchanged, only stacking).

Also double check summary line 171: "Basilisk 1/3→100%、数量 1→1–3" — not in official. That's zh wiki extra. And summary line 170 Bone Serpent Kite "1/25→1/15" vs official "4% to 6%" — 1/25=4% ✓, 1/15=6.67% vs 6% — rounding; note as trivial.

One more check: summary line 97 Xeno "开火冷却 30→33（攻速约 -10%）" ✓.

Also summary line 102: "Huntress 套装/red Riding 套装（Hood）冷却分别 74→60、40→30" ✓ matches official (Huntress/Riding Hood 74→60 and 40→30).

Also summary line 292 1.4.1.1 armor bug ✓.

Now also confirm nothing in III.E missed: "Palladium Headgear Damage bonus increased from 7% to 9%" appears twice in official (duplicate line) — summary handles once ✓.

I think analysis is complete. Let me also verify there's nothing in the official 1.4.1 section between what I read. I read 4889-5300, 5301-5700, 5700-5991. Complete coverage of 4889-5991. And 1.4.1.1 (4864-4888) and 1.4.1.2 (4698-4863). All read. Good.

Now write the report in Chinese with the requested format.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:43:58.318Z · glm-x-preview-260804

```
校验完成。我系统扫完了官方 changelog 第 4698–5991 行(即 1.4.1.2 / 1.4.1.1 / 1.4.1 三个完整段落)并与中文摘要逐节比对。以下是结果。

## 遗漏条目(按官方章节分组)

**I.C Other Content/Design Changes(摘要完全没提)**
- Plantero's Sombrero(世纪之花面具/帽)回归游戏 → 应归入【新增内容】小节
- (同节其余 11 条:复制菜单、Boss Mask 贴图、Torch God 异界曲、加载 Tips、雷声设置、菜单重组、FNA/RGB/本地化等均已覆盖)

**III.K Miscellaneous and Quality of Life(该节官方共约 23 条,摘要漏了 7 条,是遗漏最集中的一节)**
- Rock Lobster 卖价 20 银→10 银 → 【机制系统改动 — 其他】
- Sakura/Yellow Willow Saplings 价格 3 金→1 金 → 【机制系统改动 — 其他】
- Mirage Fish / Pixie Fish 稀有度 rare→uncommon(与其他任务鱼一致)→ 【机制系统改动 — 其他】
- Sharpening Station(磨刀站)Hardmode 后由 Merchant 出售 → 【机制系统改动 — 其他】
- Books 由 Wizard 出售,价格 3 银→15 银 → 【机制系统改动 — 其他】
- 1/3/5 秒计时器除合成外也由 Mechanic 出售 → 【机制系统改动 — 其他】
- **Town Happiness 的 "So Much Space"(空间充裕)加成减半** —— 这是快乐度机制三处改动之一,摘要只写了另外两处(好恶因素 ×1.2、拥挤阈值 3→4)→ 应补入【NPC与Boss与AI】Town Happiness 条目

**II.B Enemy/NPC Bugs(玩法相关,1 条)**
- Town NPC 会站在可逃离的水中直到淹死 → 【Bug修复-NPC】

**纯 bug 修复数量差异**:官方 1.4.1 段 bug 修复约 182 条(II.A 9 + II.B 27 + II.C 30 + II.D 35 + II.E 38 + II.F 27 + II.G 9 + II.H 7)。摘要以归并+列举方式覆盖了约 150 条,漏掉约 30 条,几乎全是视觉/UI 琐碎项。最重要的 5 条:
1. Zenith 在手柄下没有全屏射程(II.C,旗舰武器)
2. Smart Cursor 刷漆与真实刷漆工具的弹药槽优先级不一致(II.C)
3. 地表蘑菇背景变暗所需蘑菇块数过多(II.D)
4. 收藏文件不支持世界/角色名中的部分字符符号(II.G)
5. 1.4.1.2 的 Minion 寻敌性能修复与 Princess 会谈论未打败的 Boss(1.4.1.2 Bug 段,各 1 条)

## 数值矛盾

| 条目 | 官方值 | 摘要值 |
|---|---|---|
| Lac/Cyan/Cochineal Beetle 生命体分析仪稀有度 | **1→2**(降低优先级,不再抢在 Lost Girl 前) | **2→1**(方向写反,变成提升优先级) |
| Sky Dragon's Fury 弹幕实际伤害括号 | 原 52(70×75%),**现为 70**(140×50%) | "单发实际 52,**原 70**"——新旧值写反 |
| Orichalcum Mask 第二项属性 | 伤害 7→11% + **近战速度** 7→11% | 伤害 7→11% + **暴击** 7→11%(属性类型写错) |
| Paper Airplanes 掉率 | "**mostly the same**(基本不变)",只是改为小堆叠掉落 | "3/260→1/72"(等于掉率 ×3.6,与官方"基本不变"矛盾;风筝本体 ×3 的说法两边一致) |
| Queen Bee 多人同步 bug(II.C) | **Queen Bee**(蜂王)冲锋/传送不同步 | 写成 **Queen Slime**(史莱姆皇后)——条目主体张冠李戴(该节另有 Queen Slime 的城镇 NPC 加成 bug,易混) |

边缘项(不计矛盾):Bone Serpent Kite 官方 4%→6%,摘要 1/25→1/15(=6.67%),为 zh wiki 取整;Onyx Blaster 官方只说"减 4",摘要 28→24 为 zh wiki 补充且自洽;Basilisk Sturdy Fossil 掉率 1/3→100% 为 zh wiki 独有,官方 1.4.1 未列。

## 结论

**完整度约 90%。** 新增内容(I.A/B/C)除 Plantero's Sombrero 外全覆盖;四大类武器平衡(III.A–D)、盔甲(III.E)、饰品(III.F)、工具坐骑(III.G)、合成掉落(III.H)、Buff/Debuff(III.I)、敌人数值(III.J)逐条核对基本 100% 命中且数值一致;1.4.1.1(25 条)与 1.4.1.2(约 100 条)几乎零遗漏。问题集中在三处:**III.K 杂项节漏 7 条**(含 So Much Space 减半这一快乐度机制项)、**III.K 之外的 1 条 Plantero's Sombrero**、以及 **5 处数值/方向性错误**( Beetle 稀有度方向、Sky Dragon's Fury 新旧值、Orichalcum Mask 属性类型、Paper Airplane 掉率、Queen Bee 误写 Queen Slime)。

**建议修订**:需要,但属小修——补齐 III.K 的 7 条与 Plantero's Sombrero、NPC 溺水 bug,更正上表 5 处即可;bug 修复部分现有归并写法可接受,若追求完备可再补 5 条重要项。第四节的"复刻核心改动"结论不受影响。
```


---

## 👤 User(meta)(sidechain) · 2026-08-09T11:46:19.759Z

```
The coordinator sent a message while you were working:
校验报告收到。现在请把你报告中的修订直接应用到 ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md:
1. 更正 5 处数值/方向错误:Lac/Cyan/Cochineal Beetle 生命体分析仪稀有度应为 1→2(降低优先级);Sky Dragon's Fury 单发实际 52、现为 70(140×50%)(新旧值写反了要倒过来);Orichalcum Mask 第二项属性是近战速度 7→11%(不是暴击);Paper Airplanes 掉率官方口径是"基本不变,只是改为小堆叠掉落"(删掉或改正 3/260→1/72 的说法);Queen Bee 多人同步 bug 条目把 Queen Slime 改回 Queen Bee
2. 补 Plantero's Sombrero 回归 →【新增内容】
3. 补 III.K 漏的 7 条(重点是 Town Happiness "So Much Space" 加成减半——快乐度机制三处改动之一)
4. 文件末尾加一小节【校验记录】,注明"已用官方 changelog.txt 反向核对,完整度约 90%,四大类武器平衡数值 100% 命中"
每条保持 "(→ 文件)" 标注格式。你的 Edit/Write 工具可能被拦截,若失败就用 Bash 写入(python3 heredoc)。完成后返回修订摘要(改了几处、加了几条)。

Address this before completing your current task.
```

---

## 🤖 Assistant · 2026-08-09T11:46:31.598Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The coordinator asks me to apply the fixes. I've already read the file, so Edit should work. Let me apply each edit.

1. Five numeric/direction errors:
   a. Line 202: Lac/Cyan/Cochineal Beetle rarity → 1→2
   b. Line 49: Sky Dragon's Fury parenthetical
   c. Line 120: Orichalcum Mask 暴击 → 近战速度
   d. Line 170: Paper Airplanes
   e. Line 261: Queen Slime → Queen Bee sync
2. Add Plantero's Sombrero to 新增内容
3. Add III.K 7 items (Rock Lobster, Sakura/Yellow Willow Saplings, Mirage/Pixie Fish, Sharpening Stations, Books, Timers, So Much Space halved)
4. Add 校验记录 section at end

Let me do the edits one by one. Some can be done in parallel via multiple Edit calls, but the tool requires each old_string to be unique. Let me batch independent edits in parallel.

Edit 1 (line 202): "- Lac/Cyan/Cochineal Beetle：生命体分析仪稀有度 2→1 (→ NPC.cs, Main.cs)" → "- Lac/Cyan/Cochineal Beetle：生命体分析仪稀有度 1→2（降低优先级，不再抢在 Lost Girl 等更稀有敌人之前）(→ NPC.cs, Main.cs)"

Edit 2 (line 49): "- Sky Dragon's Fury：伤害 70→140；弹幕伤害 75%→50% 基础伤害（单发实际 52，原 70）(→ Item.cs, Projectile.cs)" → "（原 52 即 70×75%，现为 70 即 140×50%，单发实际提升）"

Edit 3 (line 120): "- Orichalcum armor：Melee Mask 伤害 7%→11%、暴击 7%→11% (→ Item.cs)" → "伤害 7%→11%、近战速度 7%→11%"

Edit 4 (line 170): "- 风筝/纸飞机：Windy Balloon 风筝掉率 1/260→1/72；Paper Airplanes 3/260→1/72 且堆叠 1→2–5；Bone Serpent Kite 1/25→1/15 (→ ItemDropRules)" → official: kites ~3x more likely, paper airplanes mostly the same but drop in small stacks, Bone Serpent Kite 4%→6%. Rewrite: "- 风筝/纸飞机：Windy Balloon Slime 掉落的风筝掉率约 ×3（wiki 记 1/260→1/72）；Paper Airplanes 掉率基本不变，但改为小堆叠掉落（wiki 记堆叠 1→2–5）；Bone Serpent Kite 掉率 4%→6%（wiki 记 1/25→1/15）(→ ItemDropRules)"

Edit 5 (line 261): "修正 Queen Slime 同步问题（多人冲锋/传送不稳）" → "修正 Queen Bee 多人同步问题（冲锋/传送不稳）"

Edit 6: Add Plantero's Sombrero to 新增内容, after Rainbow Cursor line (line 21).

Edit 7: Add III.K 7 items. The "机制系统改动 — 其他" section (lines 245-257) and Town Happiness line 206. I'll add a new bullet block for the 6 misc items before line 257 (平台层 line), and add So Much Space to Town Happiness line 206.

Line 206: "- Town Happiness 机制：喜欢/反感/喜爱/讨厌因素加减成提升 20%；不触发"拥挤"的城镇 NPC 数 3→4；城镇检测尺寸翻倍（1.4.1.2 会回调检测尺寸）(→ NPC.cs, Main.cs)" → add "；"So Much Space"（空间充裕）加成减半"

Edit 8: Add 校验记录 section at the end after 一句话总评.

Let me execute. I'll do the 5 corrections in parallel first, then additions.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:46:31.599Z · glm-x-preview-260804

```
收到，开始把修订应用到摘要文件。先做 5 处数值/方向更正。
```


---

## 🤖 Assistant · 2026-08-09T11:46:32.834Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md",
 "old_string": "- Lac/Cyan/Cochineal Beetle：生命体分析仪稀有度 2→1 (→ NPC.cs, Main.cs)",
 "new_string": "- Lac/Cyan/Cochineal Beetle：生命体分析仪稀有度 1→2（降低优先级，不再抢在 Lost Girl 等更稀有敌人之前显示）(→ NPC.cs, Main.cs)"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:46:32.856Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:46:33.523Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md",
 "old_string": "- Sky Dragon's Fury：伤害 70→140；弹幕伤害 75%→50% 基础伤害（单发实际 52，原 70）(→ Item.cs, Projectile.cs)",
 "new_string": "- Sky Dragon's Fury：伤害 70→140；弹幕伤害 75%→50% 基础伤害（原单发 52 即 70×75%，现为 70 即 140×50%，实际提升）(→ Item.cs, Projectile.cs)"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:46:33.535Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:46:34.167Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md",
 "old_string": "- Orichalcum armor：Melee Mask 伤害 7%→11%、暴击 7%→11% (→ Item.cs)",
 "new_string": "- Orichalcum armor：Melee Mask 伤害 7%→11%、近战速度 7%→11% (→ Item.cs)"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:46:34.177Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:46:35.470Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md",
 "old_string": "- 风筝/纸飞机：Windy Balloon 风筝掉率 1/260→1/72；Paper Airplanes 3/260→1/72 且堆叠 1→2–5；Bone Serpent Kite 1/25→1/15 (→ ItemDropRules)",
 "new_string": "- 风筝/纸飞机：Windy Balloon Slime 掉落的风筝掉率约 ×3（wiki 记 1/260→1/72）；Paper Airplanes 掉率基本不变，但改为小堆叠掉落（wiki 记堆叠 1→2–5）；Bone Serpent Kite 掉率 4%→6%（wiki 记 1/25→1/15，取整差异）(→ ItemDropRules)"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:46:35.483Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:46:35.808Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md",
 "old_string": "- 修正 Queen Slime 同步问题（多人冲锋/传送不稳）、Big Mimic 同步",
 "new_string": "- 修正 Queen Bee 多人同步问题（冲锋/传送不稳）、Big Mimic 同步"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:46:35.822Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:46:37.811Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
5 处更正完成。现在补条目:Plantero's Sombrero、Town Happiness So Much Space、III.K 的 6 条杂项、校验记录小节。
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:46:37.813Z · glm-x-preview-260804

```
5 处更正完成。现在补条目与校验记录。
```


---

## 🤖 Assistant · 2026-08-09T11:46:38.746Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md",
 "old_string": "- 新 vanity 饰品 Rainbow Cursor（彩虹光标）(→ Item.cs)",
 "new_string": "- 新 vanity 饰品 Rainbow Cursor（彩虹光标）(→ Item.cs)\n- Plantero's Sombrero 回归游戏（官方 I.C 节，原已移除的世纪之花造型帽）(→ Item.cs)"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:46:38.760Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:46:40.153Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md",
 "old_string": "- Town Happiness 机制：喜欢/反感/喜爱/讨厌因素加减成提升 20%；不触发\"拥挤\"的城镇 NPC 数 3→4；城镇检测尺寸翻倍（1.4.1.2 会回调检测尺寸）(→ NPC.cs, Main.cs)",
 "new_string": "- Town Happiness 机制（官方三处改动）：喜欢/反感/喜爱/讨厌因素加减成提升 20%；\"So Much Space\"（空间充裕）加成减半；不触发\"拥挤\"的城镇 NPC 数 3→4（拥挤惩罚起点更低、随人数增长更快）；城镇检测尺寸翻倍（1.4.1.2 会回调检测尺寸）(→ NPC.cs, Main.cs)"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:46:40.163Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:46:41.698Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md",
 "old_string": "- Bestiary：有独立图鉴的 Boss 仆从在打败对应 Boss 后完全解锁；Dark Mage 和 Ogre 只需打败一次即完全解锁 (→ Terraria.GameContent.UI)",
 "new_string": "- Bestiary：有独立图鉴的 Boss 仆从在打败对应 Boss 后完全解锁；Dark Mage 和 Ogre 只需打败一次即完全解锁 (→ Terraria.GameContent.UI)\n- Rock Lobster 卖价 20 银→10 银 (→ Item.cs)\n- Sakura/Yellow Willow Saplings 价格 3 金→1 金 (→ Item.cs)\n- Mirage Fish / Pixie Fish 稀有度 rare→uncommon，与其他任务鱼一致 (→ Item.cs, Player.cs)\n- Sharpening Station（磨刀站）：Hardmode 后由 Merchant 出售 (→ NPC.cs)\n- Books：Wizard 开始出售书籍，价格 3 银→15 银 (→ NPC.cs, Item.cs)\n- 1/3/5 秒计时器：除合成外也由 Mechanic 出售 (→ NPC.cs)"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:46:41.717Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:46:43.922Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now add the 校验记录 section at the end. The file ends with "### 一句话总评" section with a paragraph. Append after it.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:46:43.923Z · glm-x-preview-260804

```
最后追加校验记录小节。
```


---

## 🤖 Assistant · 2026-08-09T11:46:47.965Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md",
 "old_string": "1.4.1 是\"平衡性大补丁\"：以数百项物品/敌人数值调整和 debuff 免疫体系重排为主体，附带公主 NPC、早期召唤装备等少量新内容；1.4.1.1/1.4.1.2 是纯修补程序，1.4.1.2 还对 1.4.1 的过量强化做了一轮回调（含快乐度参数两连改），复刻应以 1.4.1.2 之后的最终数值为准。",
 "new_string": "1.4.1 是\"平衡性大补丁\"：以数百项物品/敌人数值调整和 debuff 免疫体系重排为主体，附带公主 NPC、早期召唤装备等少量新内容；1.4.1.1/1.4.1.2 是纯修补程序，1.4.1.2 还对 1.4.1 的过量强化做了一轮回调（含快乐度参数两连改），复刻应以 1.4.1.2 之后的最终数值为准。\n\n---\n\n## 五、校验记录\n\n已用官方 changelog.txt 反向核对，完整度约 90%，四大类武器平衡数值 100% 命中。\n\n- 校验范围：官方 changelog.txt 第 4698–5991 行，即 Version 1.4.1.2 / 1.4.1.1 / 1.4.1 三个完整段落。\n- 本次修订：更正 5 处数值/方向错误（Lac/Cyan/Cochineal Beetle 分析仪稀有度方向、Sky Dragon's Fury 新旧单发伤害、Orichalcum Mask 第二属性类型、Paper Airplanes 掉率口径、Queen Bee 多人同步误写 Queen Slime）；补漏 8 条（Plantero's Sombrero 回归、Town Happiness\"So Much Space\"加成减半、Rock Lobster/Saplings 降价、Mirage/Pixie Fish 稀有度、Sharpening Station/Books/Timers 出售来源）。\n- 残余已知差异：官方 1.4.1 段约 182 条 bug 修复中约 30 条视觉/UI 琐碎项未逐条列出（沿用归并写法）；Basilisk Sturdy Fossil 掉率、Dart 枪绝对伤害值为 zh wiki 补充细节，官方日志无对应数字。"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:46:47.978Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/docs/upgrade-1405-to-1456/wiki-summaries/summary-1.4.1.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-09T11:46:52.846Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Also should I add the NPC drowning bug to the NPC bug line (267)? The coordinator's instruction #3 said "补 III.K 漏的 7 条" — that's the 7 III.K items. The NPC drowning bug was in my report under II.B but the coordinator didn't explicitly ask for it. The instruction said "补 III.K 漏的 7 条(重点是 Town Happiness...)" — exactly 7. My III.K list was: So Much Space, Rock Lobster, Sakura/Yellow Willow, Mirage/Pixie Fish, Sharpening Stations, Books, Timers = 7. Done. The NPC drowning bug wasn't requested; but the coordinator said "把你报告中的修订直接应用" with a numbered list. I added exactly what was requested. The NPC drowning item was not in the requested list, so I'll leave it — but I could mention in the summary that it remains un-added per instructions. Actually, to be faithful to the coordinator's list, I applied exactly items 1-4. I'll note the NPC drowning bug as not applied since not requested.

All edits succeeded (no Bash fallback needed). Return the summary.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:46:56.876Z · glm-x-preview-260804

```
全部修订已直接写入文件(Edit 工具未被拦截，无需 Bash 回退)。修订摘要如下。

**更正 5 处数值/方向错误**
1. Lac/Cyan/Cochineal Beetle 生命体分析仪稀有度：2→1 改为 **1→2**(降低优先级，补注"不再抢在 Lost Girl 等更稀有敌人之前")
2. Sky Dragon's Fury 括号：改为"原单发 52 即 70×75%，现为 70 即 140×50%，实际提升"(新旧值倒正)
3. Orichalcum Mask 第二属性：暴击 7→11% 改为 **近战速度 7→11%**
4. 风筝/纸飞机条目重写：风筝本体掉率约 ×3 保留；Paper Airplanes 改为"掉率基本不变，改为小堆叠掉落"(删掉 3/260→1/72 的矛盾说法)；Bone Serpent Kite 标注官方 4%→6% 与 wiki 取整差异
5. 多人同步条目：Queen Slime 改回 **Queen Bee**(冲锋/传送不稳)

**补条目 8 条**
- 【新增内容】+1:Plantero's Sombrero 回归
- 【NPC与Boss与AI】Town Happiness 条目扩写为"官方三处改动"，补入 **"So Much Space" 加成减半** 与拥挤惩罚细节
- 【机制系统改动 — 其他】+6:Rock Lobster 卖价 20→10 银、Sakura/Yellow Willow Saplings 3→1 金、Mirage/Pixie Fish rare→uncommon、Sharpening Station Hardmode 后 Merchant 出售、Books 由 Wizard 出售 3→15 银、1/3/5 秒计时器由 Mechanic 出售

**新增 1 节**
- 文末追加"## 五、校验记录"：注明已用官方 changelog.txt 反向核对、完整度约 90%、四大类武器平衡数值 100% 命中，并附校验范围(4698–5991 行)、本次修订清单、残余已知差异(约 30 条视觉/UI bug 项归并未逐列、Basilisk 掉率与 Dart 枪绝对伤害为 zh wiki 补充)。

所有新增条目均保持 "(→ 文件)" 标注格式。备注：报告中提到的"Town NPC 站可逃离水中直到淹死"bug 不在协调方指令清单内，未加入；如需要可再补一条到【Bug修复-NPC】。
```
