# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-13T00:39:22.220Z

```
只读任务,不要改任何文件。在离线 wiki 镜像目录 ~/Project/GLM/SandboxWorld/terraria-wiki-md/ 里提取以下页面的**数值与规则**(文件名即页面标题;页面很长,先用 grep 定位关键词再读上下文,注意区分正文与导航/分类噪音):

1. Spiked.md 与 Spike.md、Wooden_Spike.md、Spike_pit.md —— 地刺(Spike)接触伤害数值;木刺(Wooden Spike)数值;专家/大师难度是否有倍率;触发方式。
2. Lava.md —— 岩浆接触伤害(普通/专家/大师),着火(On Fire!)持续时间,免疫规则概述。
3. Lava_immunity.md / Lava_Charm.md / Lava_Waders.md / Obsidian_Rose.md / Obsidian_Skin_Potion.md —— 各自防护规则:Lava Charm 免疫秒数(7秒?)、Lava Waders 规则(7秒岩浆免疫+其他)、Obsidian Rose 减伤数值(从多少减到多少)、Obsidian Skin Potion 免疫时长(完全免疫岩浆?秒数)、叠加上限。
4. Cactus.md / Cactus_plant.md —— 仙人掌接触伤害数值。
5. Suffocation.md —— Suffocation debuff 数值(每秒扣多少 HP)。
6. Rolling_Cactus.md(顺手)—— 滚动仙人掌伤害。

输出格式:每个页面一条,标注 文件名 + 页面中该数值所在的大致行号(用 grep -n 记录),引出原文句子(英文原句即可)。若页面没有该数值(比如 wiki 说 unknown),明确说明。不要臆测。
```

---

## 📎 Attachment · skill_listing · 2026-08-13T00:39:22.223Z

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

## 🤖 Assistant · 2026-08-13T00:39:27.891Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The user wants me to extract numeric values and rules from several wiki markdown pages in ~/Project/GLM/SandboxWorld/terraria-wiki-md/. This is a read-only task. Let me first verify the files exist, then use grep to locate keywords, then read context.

Let me start by checking the directory and finding the files.
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:39:32.737Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls -la ~/Project/GLM/SandboxWorld/terraria-wiki-md/ | head -50",
 "description": "List wiki mirror directory contents"
}
```


---

## 🤖 Assistant · 2026-08-13T00:39:32.831Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls -la ~/Project/GLM/SandboxWorld/terraria-wiki-md/Spiked.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Spike.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Wooden_Spike.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Spike_pit.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Lava.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Lava_immunity.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Lava_Charm.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Lava_Waders.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Obsidian_Rose.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Obsidian_Skin_Potion.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Cactus.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Cactus_plant.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Suffocation.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Rolling_Cactus.md 2>&1",
 "description": "Check existence and sizes of target wiki files"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:32.877Z

**📎 ToolResult**

```
-rw-r--r--@ 1 user  staff   16538  8月  6 21:52 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Cactus_plant.md
-rw-r--r--@ 1 user  staff   96517  8月  6 21:56 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Cactus.md
-rw-r--r--@ 1 user  staff  124938  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Lava_Charm.md
-rw-r--r--@ 1 user  staff   48080  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Lava_immunity.md
-rw-r--r--@ 1 user  staff  129675  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Lava_Waders.md
-rw-r--r--@ 1 user  staff   84254  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Lava.md
-rw-r--r--@ 1 user  staff  137666  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Obsidian_Rose.md
-rw-r--r--@ 1 user  staff  132642  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Obsidian_Skin_Potion.md
-rw-r--r--@ 1 user  staff  101489  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Rolling_Cactus.md
-rw-r--r--@ 1 user  staff   71151  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Spike_pit.md
-rw-r--r--@ 1 user  staff  106427  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Spike.md
-rw-r--r--@ 1 user  staff   71155  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Spiked.md
-rw-r--r--@ 1 user  staff  110467  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Suffocation.md
-rw-r--r--@ 1 user  staff  113153  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Wooden_Spike.md

```


---

## 👤 User(sidechain) · 2026-08-13T00:39:32.931Z

**📎 ToolResult**

```
total 1117784
-rw-r--r--@    1 user  staff    88650  8月  6 21:57 _categories_partials_Category_3DS_content_pages_1.md
-rw-r--r--@    1 user  staff    89161  8月  6 21:57 _categories_partials_Category_3DS_content_pages_2.md
-rw-r--r--@    1 user  staff    89097  8月  6 21:57 _categories_partials_Category_3DS_content_pages_3.md
-rw-r--r--@    1 user  staff    88897  8月  6 21:57 _categories_partials_Category_3DS_content_pages_4.md
-rw-r--r--@    1 user  staff    89367  8月  6 21:57 _categories_partials_Category_3DS_content_pages_5.md
-rw-r--r--@    1 user  staff    89014  8月  6 21:57 _categories_partials_Category_3DS_content_pages_6.md
-rw-r--r--@    1 user  staff    88959  8月  6 21:57 _categories_partials_Category_3DS_content_pages_7.md
-rw-r--r--@    1 user  staff    86145  8月  6 21:57 _categories_partials_Category_3DS_content_pages_8.md
-rw-r--r--@    1 user  staff    90679  8月  6 21:57 _categories_partials_Category_Accessory_items_pages_1.md
-rw-r--r--@    1 user  staff    83274  8月  6 21:57 _categories_partials_Category_Accessory_items_pages_2.md
-rw-r--r--@    1 user  staff    89013  8月  6 21:57 _categories_partials_Category_Achievement-related_elements_pages_1.md
-rw-r--r--@    1 user  staff    87728  8月  6 21:57 _categories_partials_Category_Achievement-related_elements_pages_2.md
-rw-r--r--@    1 user  staff    89677  8月  6 21:57 _categories_partials_Category_Autoswing_items_pages_1.md
-rw-r--r--@    1 user  staff    85226  8月  6 21:57 _categories_partials_Category_Autoswing_items_pages_2.md
-rw-r--r--@    1 user  staff    89516  8月  6 21:57 _categories_partials_Category_Bag_loot_items_pages_1.md
-rw-r--r--@    1 user  staff    87664  8月  6 21:57 _categories_partials_Category_Bag_loot_items_pages_2.md
-rw-r--r--@    1 user  staff    90311  8月  6 21:57 _categories_partials_Category_Buffs_pages_1.md
-rw-r--r--@    1 user  staff    81006  8月  6 21:57 _categories_partials_Category_Buffs_pages_2.md
-rw-r--r--@    1 user  staff    90570  8月  6 21:57 _categories_partials_Category_By_Hand_pages_1.md
-rw-r--r--@    1 user  staff    79054  8月  6 21:57 _categories_partials_Category_By_Hand_pages_2.md
-rw-r--r--@    1 user  staff    89089  8月  6 21:57 _categories_partials_Category_Console_content_pages_1.md
-rw-r--r--@    1 user  staff    89185  8月  6 21:57 _categories_partials_Category_Console_content_pages_10.md
-rw-r--r--@    1 user  staff    89051  8月  6 21:57 _categories_partials_Category_Console_content_pages_11.md
-rw-r--r--@    1 user  staff    88882  8月  6 21:57 _categories_partials_Category_Console_content_pages_12.md
-rw-r--r--@    1 user  staff    89070  8月  6 21:57 _categories_partials_Category_Console_content_pages_13.md
-rw-r--r--@    1 user  staff    89590  8月  6 21:57 _categories_partials_Category_Console_content_pages_14.md
-rw-r--r--@    1 user  staff    88818  8月  6 21:57 _categories_partials_Category_Console_content_pages_15.md
-rw-r--r--@    1 user  staff    89043  8月  6 21:57 _categories_partials_Category_Console_content_pages_16.md
-rw-r--r--@    1 user  staff    80236  8月  6 21:57 _categories_partials_Category_Console_content_pages_17.md
-rw-r--r--@    1 user  staff    90114  8月  6 21:57 _categories_partials_Category_Console_content_pages_2.md
-rw-r--r--@    1 user  staff    90162  8月  6 21:57 _categories_partials_Category_Console_content_pages_3.md
-rw-r--r--@    1 user  staff    89558  8月  6 21:57 _categories_partials_Category_Console_content_pages_4.md
-rw-r--r--@    1 user  staff    90002  8月  6 21:57 _categories_partials_Category_Console_content_pages_5.md
-rw-r--r--@    1 user  staff    89446  8月  6 21:57 _categories_partials_Category_Console_content_pages_6.md
-rw-r--r--@    1 user  staff    90017  8月  6 21:57 _categories_partials_Category_Console_content_pages_7.md
-rw-r--r--@    1 user  staff    89991  8月  6 21:57 _categories_partials_Category_Console_content_pages_8.md
-rw-r--r--@    1 user  staff    89040  8月  6 21:57 _categories_partials_Category_Console_content_pages_9.md
-rw-r--r--@    1 user  staff    89590  8月  6 21:57 _categories_partials_Category_Consumable_items_pages_1.md
-rw-r--r--@    1 user  staff    89736  8月  6 21:57 _categories_partials_Category_Consumable_items_pages_2.md
-rw-r--r--@    1 user  staff    89516  8月  6 21:57 _categories_partials_Category_Consumable_items_pages_3.md
-rw-r--r--@    1 user  staff    89587  8月  6 21:57 _categories_partials_Category_Consumable_items_pages_4.md
-rw-r--r--@    1 user  staff    89668  8月  6 21:57 _categories_partials_Category_Consumable_items_pages_5.md
-rw-r--r--@    1 user  staff    84416  8月  6 21:57 _categories_partials_Category_Consumable_items_pages_6.md
-rw-r--r--@    1 user  staff    91989  8月  6 21:57 _categories_partials_Category_Craftable_items_pages_1.md
-rw-r--r--@    1 user  staff    90460  8月  6 21:57 _categories_partials_Category_Craftable_items_pages_2.md
-rw-r--r--@    1 user  staff    90353  8月  6 21:57 _categories_partials_Category_Craftable_items_pages_3.md
-rw-r--r--@    1 user  staff    90724  8月  6 21:57 _categories_partials_Category_Craftable_items_pages_4.md
-rw-r--r--@    1 user  staff    90822  8月  6 21:57 _categories_partials_Category_Craftable_items_pages_5.md
-rw-r--r--@    1 user  staff    90613  8月  6 21:57 _categories_partials_Category_Craftable_items_pages_6.md

```


---

## 🤖 Assistant · 2026-08-13T00:39:34.084Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All files exist. Now let me grep for keywords in parallel. Start with the Spike family.
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:39:34.466Z · glm-x-preview-260804

```
所有文件均存在。现在我将使用 grep 并行检索每个页面中的关键词。
```


---

## 🤖 Assistant · 2026-08-13T00:39:34.940Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"damage|expert|master\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Spike.md | head -40",
 "description": "Locate damage and difficulty keywords in Spike.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:34.957Z

**📎 ToolResult**

```
34:Duration| 10 / [20](Expert_Mode.md "Expert Mode") / [25](Master_Mode.md "Master Mode") seconds  
40:The **Spike** is a [trap](Trap "Trap") that can be found in the [Dungeon](Dungeon.md "Dungeon"). Upon contact, it deals 60 damage to the player, on all [difficulties](Difficulties "Difficulties"), and inflicts the [Bleeding](Bleeding.md "Bleeding") [debuff](Debuff "Debuff") for 10 / [20](Expert_Mode.md "Expert Mode") / [25](Master_Mode.md "Master Mode") seconds. It can be broken with a [pickaxe](Pickaxe "Pickaxe"), [drill](Drill "Drill"), or [explosives](Explosives_\(class\) "Explosives \(class\)"). 
60:  * Spike damage can be [dodged](Dodge.md "Dodge"), but not the Bleeding debuff.
61:  * Spikes only damage players.
81:    * Damage increased from 40 to 60, and now inflicts the Bleeding debuff.
83:  * [Desktop 1.3.0.5](Desktop_1.3.0.5 "Desktop 1.3.0.5"): Spike damage is kept separate from other damage when factoring immunity, preventing abuse of invincibility frames.
749:  *[100%]: Master Mode
750:  *[DPS]: Damage per second
752:  *[300]: Master Mode
753:  *[400]: Expert Mode
754:  *[160]: Expert Mode
755:  *[240]: Expert Mode
759:enemies]: Maximum number of enemies Abigail can damage at once
764:  *[8]: Expert Mode
765:  *[10]: Expert Mode
766:  *[120]: Master Mode
767:  *[150]: Master Mode
768:  *[13]: Chế độ Master
769:  *[195]: Master Mode
781:  *[1.99%]: Expert Mode
782:  *[199/10000 (1.99%)]: Expert Mode
784:  *[1,99%]: Expert Mode
785:  *[1/50 (2%)]: Mode Expert
790:  *[180]: Master Mode
791:  *[270]: Master Mode
792:  *[5–9 seconds]: Master Mode
793:  *[5–9]: Expert Mode
802:  *[Expert Mode exclusive]: Expert Mode
803:  *[402]: Master Mode
804:  *[523]: Expert Mode
807:  *[800]: Expert Mode
808:  *[1200]: Master Mode
809:  *[15]: Expert Mode
810:  *[17]: Master Mode
812:  *[1 minute 30 seconds]: Expert Mode
813:  *[1 minute 52.5 seconds]: Master Mode
814:  *[90]: Master Mode
815:  *[112.5]: Master Mode
816:  *[2–6]: Chế độ Expert
817:  *[2-6]: Expert Mode

```


---

## 🤖 Assistant · 2026-08-13T00:39:35.299Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"damage|expert|master|redirect\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Spiked.md | head -40",
 "description": "Locate damage keywords in Spiked.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:35.320Z

**📎 ToolResult**

```
8:  *[100%]: Master Mode
9:  *[DPS]: Damage per second
11:  *[300]: Master Mode
12:  *[400]: Expert Mode
13:  *[160]: Expert Mode
14:  *[240]: Expert Mode
18:enemies]: Maximum number of enemies Abigail can damage at once
23:  *[8]: Expert Mode
24:  *[10]: Expert Mode
25:  *[120]: Master Mode
26:  *[150]: Master Mode
27:  *[13]: Chế độ Master
28:  *[195]: Master Mode
40:  *[1.99%]: Expert Mode
41:  *[199/10000 (1.99%)]: Expert Mode
43:  *[1,99%]: Expert Mode
44:  *[1/50 (2%)]: Mode Expert
49:  *[180]: Master Mode
50:  *[270]: Master Mode
51:  *[5–9 seconds]: Master Mode
52:  *[5–9]: Expert Mode
61:  *[Expert Mode exclusive]: Expert Mode
62:  *[402]: Master Mode
63:  *[523]: Expert Mode
66:  *[800]: Expert Mode
67:  *[1200]: Master Mode
68:  *[15]: Expert Mode
69:  *[17]: Master Mode
71:  *[1 minute 30 seconds]: Expert Mode
72:  *[1 minute 52.5 seconds]: Master Mode
73:  *[90]: Master Mode
74:  *[112.5]: Master Mode
75:  *[2–6]: Chế độ Expert
76:  *[2-6]: Expert Mode
77:  *[%100]: Expert Mode
78:  *[28]: Expert Mode
79:  *[42]: Master Mode
80:  *[80]: Expert Mode
82:  *[ Minor improvements to all stats and increased life regeneration]: Expert Mode
83:  *[ Major improvements to all stats and increased life regeneration]: Expert Mode

```


---

## 🤖 Assistant · 2026-08-13T00:39:36.930Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"damage|expert|master\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Wooden_Spike.md | head -40",
 "description": "Locate damage keywords in Wooden_Spike.md"
}
```


---

## 🤖 Assistant · 2026-08-13T00:39:36.946Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"damage|expert|master\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Spike_pit.md | head -40",
 "description": "Locate damage keywords in Spike_pit.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:36.953Z

**📎 ToolResult**

```
34:Duration| 10 / [20](Expert_Mode.md "Expert Mode") / [25](Master_Mode.md "Master Mode") seconds  
40:The **Wooden Spike** is a type of [trap](Trap "Trap") [block](Block "Block") that damages players who come in contact with it. The Wooden Spike deals 80 damage on contact and inflicts the [Bleeding](Bleeding.md "Bleeding") [debuff](Debuff "Debuff") for 10 / [20](Expert_Mode.md "Expert Mode") / [25](Master_Mode.md "Master Mode") seconds. Wooden Spikes are exclusively obtainable in limited quantities from the [Jungle Temple](Jungle_Temple.md "Jungle Temple"), and can be broken with any [drill](Drill "Drill"), [pickaxe](Pickaxe "Pickaxe"), or [explosive](Explosives_\(class\) "Explosives \(class\)"), unlike the [Lihzahrd Bricks](Lihzahrd_Brick.md "Lihzahrd Brick") found around them, which require a [Picksaw](Picksaw.md "Picksaw") or stronger mining tool to break. 
46:  * Wooden Spikes will deal damage to a player if any part of the player is in contact with them.
47:  * Just like Spikes, Wooden Spikes only damage players. They do not damage [NPCs](NPCs.md "NPCs"), [critters](Critters.md "Critters"), or [enemies](Enemies.md "Enemies"), and as such are unsuitable for [base defense](Guide%3ABases "Guide:Bases") outside of [PvP](PvP.md "PvP").
48:  * Wooden Spikes deal the same base amount of damage in all [difficulties](Difficulty.md "Difficulty"). Since [defense](Defense.md "Defense") is more efficient in [Expert](Expert_Mode.md "Expert Mode") and [Master Mode](Master_Mode.md "Master Mode"), the player will almost always receive less damage from Wooden Spikes than in Classic Mode.
54:  * Despite its name and appearance suggesting that it is made of a weaker material, the Wooden Spike deals more damage than the metal [Spike](Spike.md "Spike").
69:    * Damage increased from 60 to 80.
74:  * [Desktop 1.3.0.5](Desktop_1.3.0.5 "Desktop 1.3.0.5"): Spike damage is kept separate from other damage when factoring immunity, preventing abuse of invincibility frames.
731:  *[100%]: Expert Mode
732:  *[DPS]: Damage per second
734:  *[300]: Expert Mode
735:  *[400]: Master Mode
736:  *[160]: Expert Mode
737:  *[240]: Master Mode
741:enemies]: Maximum number of enemies Abigail can damage at once
746:  *[8]: Expert Mode
747:  *[10]: Expert Mode
748:  *[120]: Expert Mode
749:  *[150]: Master Mode
750:  *[13]: Chế độ Master
751:  *[195]: Master Mode
763:  *[1.99%]: Expert Mode
764:  *[199/10000 (1.99%)]: Expert Mode
766:  *[1,99%]: Expert Mode
767:  *[1/50 (2%)]: Mode Expert
772:  *[180]: Master Mode
773:  *[270]: Master Mode
774:  *[5–9 seconds]: Master Mode
775:  *[5–9]: Expert Mode
784:  *[Expert Mode exclusive]: Expert Mode
785:  *[402]: Master Mode
786:  *[523]: Expert Mode
789:  *[800]: Expert Mode
790:  *[1200]: Master Mode
791:  *[15]: Expert Mode
792:  *[17]: Master Mode
794:  *[1 minute 30 seconds]: Expert Mode
795:  *[1 minute 52.5 seconds]: Master Mode
796:  *[90]: Expert Mode
797:  *[112.5]: Master Mode

```


---

## 👤 User(sidechain) · 2026-08-13T00:39:36.964Z

**📎 ToolResult**

```
8:  *[100%]: Master Mode
9:  *[DPS]: Damage per second
11:  *[300]: Master Mode
12:  *[400]: Expert Mode
13:  *[160]: Expert Mode
14:  *[240]: Expert Mode
18:enemies]: Maximum number of enemies Abigail can damage at once
23:  *[8]: Expert Mode
24:  *[10]: Expert Mode
25:  *[120]: Master Mode
26:  *[150]: Master Mode
27:  *[13]: Chế độ Master
28:  *[195]: Master Mode
40:  *[1.99%]: Expert Mode
41:  *[199/10000 (1.99%)]: Expert Mode
43:  *[1,99%]: Expert Mode
44:  *[1/50 (2%)]: Mode Expert
49:  *[180]: Master Mode
50:  *[270]: Master Mode
51:  *[5–9 seconds]: Master Mode
52:  *[5–9]: Expert Mode
61:  *[Expert Mode exclusive]: Expert Mode
62:  *[402]: Master Mode
63:  *[523]: Expert Mode
66:  *[800]: Expert Mode
67:  *[1200]: Master Mode
68:  *[15]: Expert Mode
69:  *[17]: Master Mode
71:  *[1 minute 30 seconds]: Expert Mode
72:  *[1 minute 52.5 seconds]: Master Mode
73:  *[90]: Master Mode
74:  *[112.5]: Master Mode
75:  *[2–6]: Chế độ Expert
76:  *[2-6]: Expert Mode
77:  *[%100]: Expert Mode
78:  *[28]: Expert Mode
79:  *[42]: Master Mode
80:  *[80]: Expert Mode
82:  *[ Minor improvements to all stats and increased life regeneration]: Expert Mode
83:  *[ Major improvements to all stats and increased life regeneration]: Expert Mode

```


---

## 🤖 Assistant · 2026-08-13T00:39:39.547Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Spike.md line 40: deals 60 damage on all difficulties, Bleeding 10/20/25s. Lines 60-61: notes.
Wooden_Spike.md line 40: deals 80 damage, Bleeding 10/20/25s. Line 48: same base damage in all difficulties. Line 46: trigger — damage if any part of player is in contact.

Spiked.md and Spike_pit.md — they appear to have only navigation noise; the "damage" matches at the top are from a navigation legend block. Let me look at their heads to determine content. Also check if Spiked.md is a redirect to Spike.md.
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:39:40.023Z · glm-x-preview-260804

```
Spike.md 和 Wooden_Spike.md 包含核心数据。Spiked.md 和 Spike_pit.md 的匹配项看起来像是导航噪音——让我检查一下它们的实际内容结构。
```


---

## 🤖 Assistant · 2026-08-13T00:39:40.215Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Spiked.md",
 "limit": 45
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:40.220Z

**📎 ToolResult**

```
1	# Spiked
2	
3	> 原页面: `Spiked`
4	
5	[Spiked](./Modifiers#Accessory_modifiers)
6	  *[1 required]: Journey Mode
7	  *[Qty.]: Quantity
8	  *[100%]: Master Mode
9	  *[DPS]: Damage per second
10	  *[sic]: sīc erat scriptum (Latin: “thus it was written”) – any typographical or other errors in this quote are intentionally reproduced, exactly as they appear in the source.
11	  *[300]: Master Mode
12	  *[400]: Expert Mode
13	  *[160]: Expert Mode
14	  *[240]: Expert Mode
15	  *[3 required]: Journey Mode
16	  *[#]: Number
17	  *[Max.  
18	enemies]: Maximum number of enemies Abigail can damage at once
19	  *[HM]: Hardmode
20	  *[**Click/tap here** to reveal this content. _(there may be a slight delay)_]: This content exists externally. Once you click, there may be a small delay while it is downloaded.
21	  *[**Klik/tap disini** untuk melihat isi konten. _(mungkin akan sedikit delay)_]: Konten ini tersedia secara eksternal. Ketika di klik, mungkin akan ada sedikit delay ketika melihat isi konten.
22	  *[**Bấm/Chạm vào đây** để hiển thị nội dung này. _(có thể sẽ bị delay một chút)_]: Nội dung này được lấy từ các nguồn bên ngoài. Khi bấm vào, có thể sẽ bị delay một chút trong khi nó tải.
23	  *[8]: Expert Mode
24	  *[10]: Expert Mode
25	  *[120]: Master Mode
26	  *[150]: Master Mode
27	  *[13]: Chế độ Master
28	  *[195]: Master Mode
29	  *[Verify]: Source code ref needed
30	  *[50 required]: Journey Mode
31	  *[0.05 mph]: 0.05 miles per hour (as measured by the Stopwatch item) or 0.04 tiles per second
32	  *[100 required]: Journey Mode
33	  *[cần có 1]: Chế độ Journey
34	  *[25 required]: Journey Mode
35	  *[cần có 25]: Chế độ Journey
36	  *[400 required]: Journey Mode
37	  *[membutuhkan 100]: Mode Journey
38	  *[cần có 100]: Chế độ Journey
39	  *[Slg.]: Số lượng
40	  *[1.99%]: Expert Mode
41	  *[199/10000 (1.99%)]: Expert Mode
42	  *[membutuhkan 1]: Mode Journey
43	  *[1,99%]: Expert Mode
44	  *[1/50 (2%)]: Mode Expert
45	  *[200 required]: Journey Mode

```


---

## 🤖 Assistant · 2026-08-13T00:39:40.418Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Spike_pit.md",
 "limit": 45
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:40.423Z

**📎 ToolResult**

```
1	# Spike pit
2	
3	> 原页面: `Spike_pit`
4	
5	[Spike pit](./Traps#Spike_Pits)
6	  *[1 required]: Journey Mode
7	  *[Qty.]: Quantity
8	  *[100%]: Master Mode
9	  *[DPS]: Damage per second
10	  *[sic]: sīc erat scriptum (Latin: “thus it was written”) – any typographical or other errors in this quote are intentionally reproduced, exactly as they appear in the source.
11	  *[300]: Master Mode
12	  *[400]: Expert Mode
13	  *[160]: Expert Mode
14	  *[240]: Expert Mode
15	  *[3 required]: Journey Mode
16	  *[#]: Number
17	  *[Max.  
18	enemies]: Maximum number of enemies Abigail can damage at once
19	  *[HM]: Hardmode
20	  *[**Click/tap here** to reveal this content. _(there may be a slight delay)_]: This content exists externally. Once you click, there may be a small delay while it is downloaded.
21	  *[**Klik/tap disini** untuk melihat isi konten. _(mungkin akan sedikit delay)_]: Konten ini tersedia secara eksternal. Ketika di klik, mungkin akan ada sedikit delay ketika melihat isi konten.
22	  *[**Bấm/Chạm vào đây** để hiển thị nội dung này. _(có thể sẽ bị delay một chút)_]: Nội dung này được lấy từ các nguồn bên ngoài. Khi bấm vào, có thể sẽ bị delay một chút trong khi nó tải.
23	  *[8]: Expert Mode
24	  *[10]: Expert Mode
25	  *[120]: Master Mode
26	  *[150]: Master Mode
27	  *[13]: Chế độ Master
28	  *[195]: Master Mode
29	  *[Verify]: Source code ref needed
30	  *[50 required]: Journey Mode
31	  *[0.05 mph]: 0.05 miles per hour (as measured by the Stopwatch item) or 0.04 tiles per second
32	  *[100 required]: Journey Mode
33	  *[cần có 1]: Chế độ Journey
34	  *[25 required]: Journey Mode
35	  *[cần có 25]: Chế độ Journey
36	  *[400 required]: Journey Mode
37	  *[membutuhkan 100]: Mode Journey
38	  *[cần có 100]: Chế độ Journey
39	  *[Slg.]: Số lượng
40	  *[1.99%]: Expert Mode
41	  *[199/10000 (1.99%)]: Expert Mode
42	  *[membutuhkan 1]: Mode Journey
43	  *[1,99%]: Expert Mode
44	  *[1/50 (2%)]: Mode Expert
45	  *[200 required]: Journey Mode

```


---

## 🤖 Assistant · 2026-08-13T00:39:41.119Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -v -E \"^\\s*\\*\\[|^  \\*\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Spiked.md | grep -n -v \"^$\" | head -30",
 "description": "Filter out legend noise lines from Spiked.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:44.280Z

**📎 ToolResult**

```
1:1:# Spiked
2:2:
3:3:> 原页面: `Spiked`
4:4:
5:5:[Spiked](./Modifiers#Accessory_modifiers)
6:18:enemies]: Maximum number of enemies Abigail can damage at once
7:564:dmg]: Attack damage
8:753:40 when below 145 health]: Expert Mode
9:755:60 when below 185 health]: Master Mode
10:760:40 khi dưới 145 máu]: Chế độ Expert
11:762:60 khi dưới 185 máu]: Chế độ Master
12:1150:57% (2 players)  
13:1151:71% (3 players)  
14:1152:81%  (4 players)  
15:1153:100% (5 players or more)  
16:1154:]: Expert Mode
17:1156:62% (2 players)  
18:1157:75% (3 players)  
19:1158:83% (4 players)  
20:1159:100% (5 players or more)  
21:1160:]: Master Mode
22:1162:69% (2 players)  
23:1163:79% (3 players)  
24:1164:86%  (4 players)  
25:1165:100% (5 players or more)  
26:1166:]: Expert Mode
27:1168:72% (2 players)  
28:1169:82% (3 players)  
29:1170:88% (4 players)  
30:1171:100% (5 players or more)

```


---

## 🤖 Assistant · 2026-08-13T00:39:46.656Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Spiked.md is a redirect page: "[Spiked](./Modifiers#Accessory_modifiers)" — it redirects to Modifiers#Accessory_modifiers. So "Spiked" refers to an accessory modifier, NOT the trap. No damage value in this page.

Spike_pit.md redirects to "./Traps#Spike_Pits". No damage value in this page itself. I should note that the actual content is in Traps.md. Let me check Traps.md for the Spike Pit section since the user wants the numbers — worth a bonus note.

Now let's read the Spike.md and Wooden_Spike.md relevant sections more fully, and check Traps.md for Spike Pits.
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:39:47.253Z · glm-x-preview-260804

```
Spiked.md 和 Spike_pit.md 都是重定向存根。让我确认它们的目标，并阅读核心地刺（Spike）页面章节，以及 Traps.md 中的 Spike Pit 章节。
```


---

## 🤖 Assistant · 2026-08-13T00:39:48.205Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -A 3 -i \"spike pit\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Traps.md | grep -v \"^\\s*\\*\\[\" | head -30",
 "description": "Find Spike Pit section in Traps.md"
}
```


---

## 🤖 Assistant · 2026-08-13T00:39:48.217Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Spike.md",
 "limit": 65,
 "offset": 28
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:48.222Z

**📎 ToolResult**

```
28	Inflicts [Debuff](Debuffs.md "Debuffs")
29	
30	Debuff| [](Bleeding.md "Bleeding")[Bleeding](Bleeding.md "Bleeding")  
31	---|---  
32	Debuff tooltip|  _Cannot regenerate life_  
33	Chance| 100%  
34	Duration| 10 / [20](Expert_Mode.md "Expert Mode") / [25](Master_Mode.md "Master Mode") seconds  
35	  
36	  * Internal [Item ID](Item_IDs.md "Item IDs"): **147**
37	  * Internal [Tile ID](Tile_IDs.md "Tile IDs"): **48**
38	  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **30**
39	
40	The **Spike** is a [trap](Trap "Trap") that can be found in the [Dungeon](Dungeon.md "Dungeon"). Upon contact, it deals 60 damage to the player, on all [difficulties](Difficulties "Difficulties"), and inflicts the [Bleeding](Bleeding.md "Bleeding") [debuff](Debuff "Debuff") for 10 / [20](Expert_Mode.md "Expert Mode") / [25](Master_Mode.md "Master Mode") seconds. It can be broken with a [pickaxe](Pickaxe "Pickaxe"), [drill](Drill "Drill"), or [explosives](Explosives_\(class\) "Explosives \(class\)"). 
41	
42	Spikes cannot be destroyed by explosives when the [For the Worthy](For_the_Worthy.md "For the Worthy") seed is active.[1]
43	
44	## Crafting
45	
46	### Used in
47	
48	Result| Ingredients| [Crafting station](Crafting_station "Crafting station")  
49	---|---|---  
50	[](Spike_Block.md "Spike Block")[Spike Block](Spike_Block.md "Spike Block")**** __(Desktop, Console and Mobile versions) 5| 
51	
52	  * [](Stone_Block.md "Stone Block")[Stone Block](Stone_Block.md "Stone Block")5
53	  * [](Spike.md "Spike")Spike
54	
55	| [](Work_Bench "Work Bench")[Work Bench](Work_Bench "Work Bench")  
56	  
57	## Notes
58	
59	  * Spikes turn bright red when the [Dangersense](Dangersense "Dangersense") [buff](Buff "Buff") is active.
60	  * Spike damage can be [dodged](Dodge.md "Dodge"), but not the Bleeding debuff.
61	  * Spikes only damage players.
62	  * Spikes are valid walls for [NPC housing](House.md "House").
63	
64	## See also
65	
66	  * [Wooden Spike](Wooden_Spike.md "Wooden Spike")
67	  * [Sharp Spike Block](Sharp_Spike_Block.md "Sharp Spike Block")
68	
69	## History
70	
71	[ Desktop version](Desktop_version_history.md "Desktop version history")
72	
73	  * [Desktop 1.4.5.0](Desktop_1.4.5.0 "Desktop 1.4.5.0"): Can now be used to craft [Spike Blocks](Spike_Block.md "Spike Block").
74	
75	  * [Desktop 1.4.4](Desktop_1.4.4 "Desktop 1.4.4"): Stack limit increased from 999 to 9999.
76	
77	  * [Desktop 1.4.2](Desktop_1.4.2 "Desktop 1.4.2"): Fixed an issue where Spikes would not hurt the player from some angles at certain elevations.
78	
79	  * [Desktop 1.4.0.1](Desktop_1.4.0.1 "Desktop 1.4.0.1"): 
80	    * Sprites updated. Old sprites were:  and .
81	    * Damage increased from 40 to 60, and now inflicts the Bleeding debuff.
82	
83	  * [Desktop 1.3.0.5](Desktop_1.3.0.5 "Desktop 1.3.0.5"): Spike damage is kept separate from other damage when factoring immunity, preventing abuse of invincibility frames.
84	
85	  * [Desktop 1.2](Desktop_1.2 "Desktop 1.2"): Stack limit increased from 250 to 999.
86	
87	  * [Desktop 1.1](Desktop_1.1 "Desktop 1.1"): Can now be destroyed by [explosives](Explosives_\(class\) "Explosives \(class\)").
88	
89	  * [Desktop-Release](Desktop-Release.md "Desktop-Release"): Introduced.
90	
91	[ Console version](Console_version.md "Console version")
92	

```


---

## 👤 User(sidechain) · 2026-08-13T00:39:48.233Z

**📎 ToolResult**

```
131:### [](Spike.md "Spike") Spike Pits
132-
133-[](Desktop_version_history.md "Desktop version") [](Console_version.md "Console version") [](Mobile_version.md "Mobile version")
134-
--
137:Spike Pits can be found throughout the [Dungeon](Dungeon.md "Dungeon"), and consist of a thick row of [Cracked Dungeon Bricks](Cracked_Dungeon_Bricks.md "Cracked Dungeon Bricks") above a large rectangular pit. Surrounding the pit on all sides are [spikes](Spikes "Spikes"), which can quickly deal large amounts of damage. Some of these pits are filled with water, which can make them even more deadly at first, but can later be used for [Fishing](Fishing.md "Fishing"). 
138-
139-### [](Dead_Man's_Chest.md "Dead Man's Chest")[Dead Man's Chests](Dead_Man's_Chest.md "Dead Man's Chest")
140-
--
183:  * A Spike Pit with [Dangersense](Dangersense "Dangersense") [buff](Buff "Buff") active. The [torches](Torches.md "Torches") are placed by a player.
184-
185-  * A Dead Man's Chest and its surrounding traps.
186-
--
350:    * Added Dead Man's Chest traps, Spike Pits, Sand Traps, Lava Traps, Pressure Plate Track Traps and [Rolling Cactus](Rolling_Cactus.md "Rolling Cactus").
351-    * Geyser trap are now set off just by stepping on them.
352-    * Temple traps now require the [Picksaw](Picksaw.md "Picksaw") or higher to mine.
353-

```


---

## 🤖 Assistant · 2026-08-13T00:39:48.255Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Wooden_Spike.md",
 "limit": 35,
 "offset": 28
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:48.259Z

**📎 ToolResult**

```
28	Inflicts [Debuff](Debuffs.md "Debuffs")
29	
30	Debuff| [](Bleeding.md "Bleeding")[Bleeding](Bleeding.md "Bleeding")  
31	---|---  
32	Debuff tooltip|  _Cannot regenerate life_  
33	Chance| 100%  
34	Duration| 10 / [20](Expert_Mode.md "Expert Mode") / [25](Master_Mode.md "Master Mode") seconds  
35	  
36	  * Internal [Item ID](Item_IDs.md "Item IDs"): **1150**
37	  * Internal [Tile ID](Tile_IDs.md "Tile IDs"): **232**
38	  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **30**
39	
40	The **Wooden Spike** is a type of [trap](Trap "Trap") [block](Block "Block") that damages players who come in contact with it. The Wooden Spike deals 80 damage on contact and inflicts the [Bleeding](Bleeding.md "Bleeding") [debuff](Debuff "Debuff") for 10 / [20](Expert_Mode.md "Expert Mode") / [25](Master_Mode.md "Master Mode") seconds. Wooden Spikes are exclusively obtainable in limited quantities from the [Jungle Temple](Jungle_Temple.md "Jungle Temple"), and can be broken with any [drill](Drill "Drill"), [pickaxe](Pickaxe "Pickaxe"), or [explosive](Explosives_\(class\) "Explosives \(class\)"), unlike the [Lihzahrd Bricks](Lihzahrd_Brick.md "Lihzahrd Brick") found around them, which require a [Picksaw](Picksaw.md "Picksaw") or stronger mining tool to break. 
41	
42	## Notes
43	
44	  * The [Lihzahrd Altar](Lihzahrd_Altar.md "Lihzahrd Altar") can spawn on top of Wooden Spikes.
45	  * Wooden Spikes turn bright red when the [Dangersense](Dangersense "Dangersense") [buff](Buff "Buff") is active.
46	  * Wooden Spikes will deal damage to a player if any part of the player is in contact with them.
47	  * Just like Spikes, Wooden Spikes only damage players. They do not damage [NPCs](NPCs.md "NPCs"), [critters](Critters.md "Critters"), or [enemies](Enemies.md "Enemies"), and as such are unsuitable for [base defense](Guide%3ABases "Guide:Bases") outside of [PvP](PvP.md "PvP").
48	  * Wooden Spikes deal the same base amount of damage in all [difficulties](Difficulty.md "Difficulty"). Since [defense](Defense.md "Defense") is more efficient in [Expert](Expert_Mode.md "Expert Mode") and [Master Mode](Master_Mode.md "Master Mode"), the player will almost always receive less damage from Wooden Spikes than in Classic Mode.
49	  * Wooden Spikes are valid frame tiles for [NPC housing](House.md "House").
50	  * Wooden Spikes cannot be destroyed by [explosives](Explosives_\(class\) "Explosives \(class\)") when the [For the Worthy](For_the_Worthy.md "For the Worthy") seed is enabled.[1]
51	
52	## Trivia
53	
54	  * Despite its name and appearance suggesting that it is made of a weaker material, the Wooden Spike deals more damage than the metal [Spike](Spike.md "Spike").
55	
56	## See also
57	
58	  * [Sharp Spike Block](Sharp_Spike_Block.md "Sharp Spike Block")
59	
60	## History
61	
62	[ Desktop version](Desktop_version_history.md "Desktop version history")

```


---

## 🤖 Assistant · 2026-08-13T00:39:51.199Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Spike family done. Now Lava.md.
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:39:51.213Z · glm-x-preview-260804

```
尖刺系列已完成。现在开始处理 Lava.md。
```


---

## 🤖 Assistant · 2026-08-13T00:39:51.226Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"80|damage|On Fire|second|immune|immunity\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Lava.md | grep -v \"^\\s*[0-9]*:\\s*\\*\\[\" | head -40",
 "description": "Locate damage and fire keywords in Lava.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:51.248Z

**📎 ToolResult**

```
9:The icon displayed when immune to lava.
13:Contact with lava deals [damage](Damage.md "Damage") (which is not affected by damage variance) and inflicts the [On Fire!](On_Fire!.md "On Fire!") [debuff](Debuff "Debuff"). [Players](Player "Player") take 80 damage and the debuff lasts for 7 / [14](Expert_Mode.md "Expert Mode") / [17.5](Master_Mode.md "Master Mode") seconds[2], whereas [enemies](Enemies.md "Enemies"), [NPCs](NPCs.md "NPCs"), and [critters](Critters.md "Critters") take 50 damage and the debuff lasts for 7 seconds.[3] Various items make the player immune to this damage, such as the [Lava Charm](Lava_Charm.md "Lava Charm") and its derivatives. Lava also [slows movement](Movement_speed#Medium_movement "Movement speed") of entities submerged in it, similarly to water. 
88:By default, players are dealt 80 damage and set on fire by lava.
147:  * The damage from lava can be reduced by [defense](Defense.md "Defense") and [damage reduction](Damage_reduction.md "Damage reduction"). Apart from that, the following items allow for reducing or eliminating lava damage: 
148:    * [](Obsidian_Skin_Potion.md "Obsidian Skin Potion")[Obsidian Skin Potion](Obsidian_Skin_Potion.md "Obsidian Skin Potion"): Grants a buff when consumed which provides lava immunity for its entire duration.
149:    * [](Superheated_Blood.md "Superheated Blood")[Superheated Blood](Superheated_Blood.md "Superheated Blood")**** __(Desktop, Console and Mobile versions) : Summons a Lava Shark Mount, which provides unlimited lava immunity, as well as fast movement in liquids.
150:    * [](Obsidian_Rose.md "Obsidian Rose")[Obsidian Rose](Obsidian_Rose.md "Obsidian Rose")and its upgrades: Reduces the base damage taken from lava from 80 to ****__(Desktop, Console and Mobile versions) 35 / ****__(Old-gen console and 3DS versions) 50 and halves the duration of the inflicted [On Fire!](On_Fire!.md "On Fire!") [debuff](Debuff "Debuff") from 7 / [14](Expert_Mode.md "Expert Mode") / [17.5](Master_Mode.md "Master Mode") seconds to 3.5 / [7](Expert_Mode.md "Expert Mode") / [8.75](Master_Mode.md "Master Mode") seconds.
151:    * [](Ash_Wood_armor.md "Ash Wood armor")[Ash Wood armor](Ash_Wood_armor.md "Ash Wood armor")(set bonus)****__(Desktop, Console and Mobile versions) : Halves the base damage taken from lava from 80 to 40 and halves the duration of the inflicted On Fire! debuff from 7 / [14](Expert_Mode.md "Expert Mode") / [17.5](Master_Mode.md "Master Mode") seconds to 3.5 / [7](Expert_Mode.md "Expert Mode") / [8.75](Master_Mode.md "Master Mode") seconds.
152:    * Equipping both Ash Wood armor and the Obsidian Rose (or its upgrades) provides unlimited lava immunity. 
153:      * In this case, lava immunity time from the following items will still be consumed.
154:  * Various [accessories](Accessories.md "Accessories") and one type of [minecart](Minecarts.md "Minecarts") allow the player to be submerged in lava for some time without taking damage. This immunity is similar to the [breath meter](Breath_meter.md "Breath meter") while underwater, but it has its own separate bar, is immediately activated upon touching lava, and takes much longer to refill than the breath meter after exiting lava. Each of these items grants 7 seconds of immunity. If multiple of these items are equipped/used simultaneously, the duration of immunity will be stacked, up to a maximum of ****__(Desktop, Console and Mobile versions) 49 / ****__(Old-gen console and 3DS versions) 14 seconds if all of them are used.
171:  * Occasional lava "drips" from the ceiling are a special effect, which cause no damage. The player can create them with a [Magic Lava Dropper](Magic_Lava_Dropper "Magic Lava Dropper")**** __(Desktop, Console and Mobile versions). 
173:  * Some entities will not take any damage from contact with lava, including: 
186:  * A shallow lava pit underneath a structure will damage all walking [enemies](Enemies.md "Enemies") as they attempt to jump towards the player in the structure, and, if shallow enough, will gather their drops in one location for easy collection later. One can also use this technique to upgrade regular pits. Standing underneath the pit will lure most enemies toward the player, with even some flying enemies diving into the lava.
228:    * Touching lava while in water will now properly put the On Fire! debuff out when leaving lava.
234:  * [Desktop 1.1](Desktop_1.1 "Desktop 1.1"): Now exists as a secondary "layer" behind the placed blocks. Therefore can no longer be removed by dropping [sand](Sand "Sand")-like block in it. "Blocked" liquids now disappear only after restart of world.
241:    * Now causes the [On Fire!](On_Fire!.md "On Fire!") [debuff](Debuff "Debuff").
271:  4. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, method `CheckLavaDeath()` in `Terraria.Item.cs` and field `IsLavaImmuneRegardlessOfRarity` in `Terraria.ID.ItemID.Sets.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
387:enemies]: Maximum number of enemies Abigail can damage at once
933:dmg]: Attack damage

```


---

## 🤖 Assistant · 2026-08-13T00:39:55.271Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Lava.md line 13 is the core: players take 80 damage, On Fire! lasts 7/14/17.5 s; enemies/NPCs/critters take 50 damage, 7 s. Line 150: Obsidian Rose reduces base damage from 80 to 35 (Desktop/Console/Mobile) or 50 (Old-gen console and 3DS), halves On Fire! duration from 7/14/17.5 to 3.5/7/8.75. Line 154: 7 seconds each; stacked up to 49 (Desktop, Console, Mobile) / 14 (Old-gen console and 3DS). Line 148: Obsidian Skin Potion — grants buff providing lava immunity for its entire duration.

Let me also read the head of Lava.md to check for expert/master multipliers on lava contact damage — actually, the wiki text says players take 80 damage, with On Fire! debuff lasting 7/14/17.5s. There's no expert/master multiplier on the contact damage itself. Let me read lines 1-20 to be thorough.
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:39:55.728Z · glm-x-preview-260804

```
Lava.md 已包含核心数据。让我读取一下它的开头以了解上下文，并开始检索防护物品页面。
```


---

## 🤖 Assistant · 2026-08-13T00:39:55.893Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Lava.md",
 "limit": 20
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:55.898Z

**📎 ToolResult**

```
1	# Lava
2	
3	> 原页面: `Lava`
4	
5	# Lava
6	
7	Some lava in a cave.
8	
9	The icon displayed when immune to lava.
10	
11	**Lava** is a glowing red-orange [liquid](Liquid "Liquid") found deep in the [Cavern](Cavern.md "Cavern") layer and throughout [The Underworld](The_Underworld.md "The Underworld"), appearing instead of [water](Water.md "Water") at [depths](Layers.md "Layers") below approximately 950 feet (475 tiles) in a [small world](World_size.md "World size"), 1,450 feet (725 tiles) in a medium world, or 1,950 feet (975 tiles) in a large world (on average).[1] Tiny pools can frequently be found on the outskirts of the [Underground Desert](Underground_Desert.md "Underground Desert")**** __(Desktop, Console and Mobile versions) as well, even as high as 200 feet below the surface. 
12	
13	Contact with lava deals [damage](Damage.md "Damage") (which is not affected by damage variance) and inflicts the [On Fire!](On_Fire!.md "On Fire!") [debuff](Debuff "Debuff"). [Players](Player "Player") take 80 damage and the debuff lasts for 7 / [14](Expert_Mode.md "Expert Mode") / [17.5](Master_Mode.md "Master Mode") seconds[2], whereas [enemies](Enemies.md "Enemies"), [NPCs](NPCs.md "NPCs"), and [critters](Critters.md "Critters") take 50 damage and the debuff lasts for 7 seconds.[3] Various items make the player immune to this damage, such as the [Lava Charm](Lava_Charm.md "Lava Charm") and its derivatives. Lava also [slows movement](Movement_speed#Medium_movement "Movement speed") of entities submerged in it, similarly to water. 
14	
15	Lava flows downwards and horizontally, settling and taking the shape of any block formations below and beside it, the way water does. Lava flows slower than water. After flowing 50 tiles in a direction, lava will begin to evaporate, causing the source to be lost. Unlike water, the color of lava does not depend on the biome the player is in. It also emits a medium amount of flickering light. Lava is opaque, hiding [objects](Objects.md "Objects"), [drops](Drops "Drops"), enemies, and players. 
16	
17	Most dropped items of [](Rarity.md "White \(Rarity level: 0\)") [rarity](Rarity.md "Rarity") (which includes all [coins](Coins.md "Coins")) and all of [](Rarity.md "Gray \(Rarity level: −1\)") rarity will be destroyed when submerged in lava past their vertical midpoint. Furthermore, most [trees](Trees.md "Trees") and most types of placed [furniture](Furniture.md "Furniture") and [platforms](Platforms.md "Platforms") are destroyed upon contact with lava (with exceptions). [Blocks](Blocks.md "Blocks") cannot be placed directly within lava, but falling blocks like [silt](Silt "Silt") and [sand](Sand "Sand") can fall into it, resulting in placement at its bottom. Lava can be moved by the player via a [bucket](Bucket "Bucket") or [pump](Pump "Pump"). 
18	
19	In addition to naturally generated lava, it may be produced in a few other ways. [Hellstone](Hellstone.md "Hellstone") produces half a block's volume of lava when mined in the Underworld (a full block's volume in [Expert Mode](Expert_Mode.md "Expert Mode")**** __(Desktop, Console and Mobile versions)). [Lava Slimes](Lava_Slime.md "Lava Slime") create a small amount of lava when slain in Expert Mode (except in worlds with the [Remix](Remix.md "Remix")**** __(Desktop, Console and Mobile versions) [special world seed](Special_world_seed "Special world seed") active). [Hellbats](Hellbat.md "Hellbat") and [Lava Bats](Lava_Bat.md "Lava Bat") create a small amount of lava when slain in [Zenith](Zenith_\(seed\) "Zenith \(seed\)") worlds. 
20	

```


---

## 🤖 Assistant · 2026-08-13T00:39:56.462Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"7 second|seven second|grants\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Lava_Charm.md | grep -v \"^\\s*[0-9]*:\\s*\\*\\[\" | head -15",
 "description": "Find immunity duration in Lava_Charm.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:56.488Z

**📎 ToolResult**

```
20:[Tooltip](Tooltips.md "Tooltips")|  _Provides 7 seconds of immunity to lava_  
43:The **Lava Charm** is an [accessory](Accessory "Accessory") that grants immunity to [lava](Lava.md "Lava") for 7 seconds. It is found in [Chests](Chests.md "Chests") located in the [cavern](Cavern.md "Cavern") layer as well as obtained from [Hellstone Crates](Hellstone_Crate.md "Hellstone Crate") and [Obsidian Crates](Obsidian_Crate.md "Obsidian Crate") with a 1/20 (5%) chance. It can only be found in Chests in the lower portion of the Caverns where [lava](Lava.md "Lava") pools can naturally spawn, as opposed to Chests throughout the entirety of the Caverns. 
97:  * The [Molten Charm](Molten_Charm.md "Molten Charm"), [Magma Skull](Magma_Skull.md "Magma Skull"), [Molten Skull Rose](Molten_Skull_Rose.md "Molten Skull Rose"), [Lava Waders](Lava_Waders.md "Lava Waders"), and [Terraspark Boots](Terraspark_Boots.md "Terraspark Boots") all stack with the Lava Charm to increase lava immunity by 7 seconds each. The [Demonic Hellcart](Demonic_Hellcart.md "Demonic Hellcart") also gives an additional 7 seconds. Of these, only the Demonic Hellcart is not itself a Lava Charm upgrade.

```


---

## 🤖 Assistant · 2026-08-13T00:39:57.173Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"7 second|seven second|grant|lava immunity|water walking|obsidian\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Lava_Waders.md | grep -v \"^\\s*[0-9]*:\\s*\\*\\[\" | head -20",
 "description": "Find protection rules in Lava_Waders.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:57.200Z

**📎 ToolResult**

```
21:Grants immunity to fire blocks and 7 seconds of immunity to lava  
29:The **Lava Waders** are a [pre-Hardmode](Pre-Hardmode.md "Pre-Hardmode") [immunity accessory](Immunity_accessory "Immunity accessory"). They grant the following effects while equipped: 
35:  * Immunity to [lava](Lava.md "Lava") for 7 seconds.
47:  * [](Obsidian_Water_Walking_Boots.md "Obsidian Water Walking Boots")[Obsidian Water Walking Boots](Obsidian_Water_Walking_Boots.md "Obsidian Water Walking Boots")
49:  * [](Obsidian_Rose.md "Obsidian Rose")[Obsidian Rose](Obsidian_Rose.md "Obsidian Rose")
54:  * [](Obsidian_Water_Walking_Boots.md "Obsidian Water Walking Boots")[Obsidian Water Walking Boots](Obsidian_Water_Walking_Boots.md "Obsidian Water Walking Boots")
59:  * [](Obsidian_Water_Walking_Boots.md "Obsidian Water Walking Boots")[Obsidian Water Walking Boots](Obsidian_Water_Walking_Boots.md "Obsidian Water Walking Boots")
60:  * [](Obsidian_Rose.md "Obsidian Rose")[Obsidian Rose](Obsidian_Rose.md "Obsidian Rose")
65:  * [](Water_Walking_Boots.md "Water Walking Boots")[Water Walking Boots](Water_Walking_Boots.md "Water Walking Boots")
66:  * [](Obsidian_Rose.md "Obsidian Rose")[Obsidian Rose](Obsidian_Rose.md "Obsidian Rose")
71:  * [](Water_Walking_Boots.md "Water Walking Boots")[Water Walking Boots](Water_Walking_Boots.md "Water Walking Boots")
77:[](Obsidian.md "Obsidian")[Obsidian](Obsidian.md "Obsidian") × 20  
78:( [](Water.md "Water") \+ [](Lava.md "Lava") )| | | | | | | | | | | | | | | | [](Obsidian.md "Obsidian")[Obsidian](Obsidian.md "Obsidian") × 20  
79:( [](Water.md "Water") \+ [](Lava.md "Lava") )| | | | | | | | | | | | | | | | | | | | | [](Obsidian.md "Obsidian")[Obsidian](Obsidian.md "Obsidian") × 20  
88:[](Obsidian_Skull.md "Obsidian Skull")[Obsidian Skull](Obsidian_Skull.md "Obsidian Skull")| | | [](Lava_Charm.md "Lava Charm")[Lava Charm](Lava_Charm.md "Lava Charm")  
89:( [](Gold_Chest.md "Gold Chest") [](Obsidian_Crate.md "Obsidian Crate") [](Hellstone_Crate.md "Hellstone Crate") )| | | | | | | | | | | [](Obsidian_Skull.md "Obsidian Skull")[Obsidian Skull](Obsidian_Skull.md "Obsidian Skull")| | | [](Water_Walking_Boots.md "Water Walking Boots")[Water Walking Boots](Water_Walking_Boots.md "Water Walking Boots")  
91:( [](Gold_Chest.md "Gold Chest") [](Obsidian_Crate.md "Obsidian Crate") [](Hellstone_Crate.md "Hellstone Crate") )| | | [](Obsidian_Skull.md "Obsidian Skull")[Obsidian Skull](Obsidian_Skull.md "Obsidian Skull")| |   
96:( [](Gold_Chest.md "Gold Chest") [](Obsidian_Crate.md "Obsidian Crate") [](Hellstone_Crate.md "Hellstone Crate") )| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |   
102:[](Molten_Charm.md "Molten Charm")[Molten Charm](Molten_Charm.md "Molten Charm")| | | [](Obsidian_Rose.md "Obsidian Rose")[Obsidian Rose](Obsidian_Rose.md "Obsidian Rose")  
103:( [](Fire_Imp.md "Fire Imp") )| | | [](Water_Walking_Boots.md "Water Walking Boots")[Water Walking Boots](Water_Walking_Boots.md "Water Walking Boots")

```


---

## 🤖 Assistant · 2026-08-13T00:39:57.787Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"80|50|35|halves|damage\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Obsidian_Rose.md | grep -v \"^\\s*[0-9]*:\\s*\\*\\[\" | head -20",
 "description": "Find damage reduction values in Obsidian_Rose.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:57.810Z

**📎 ToolResult**

```
20:[Tooltip](Tooltips.md "Tooltips")|  _Reduces damage from touching lava_  
39:The **Obsidian Rose** is an [accessory](Accessory "Accessory") that reduces the base [damage](Damage.md "Damage") taken from [lava](Lava.md "Lava") from 80 to 35 and halves the duration of the [On Fire!](On_Fire!.md "On Fire!") [debuff](Debuff "Debuff") inflicted by it from 7 / [14](Expert_Mode.md "Expert Mode") / [17.5](Master_Mode.md "Master Mode") seconds to 3.5 / [7](Expert_Mode.md "Expert Mode") / [8.75](Master_Mode.md "Master Mode") seconds.[1]
41:Additionally, equipping both [Ash Wood armor](Ash_Wood_armor.md "Ash Wood armor") and the Obsidian Rose (or its upgrades) provides immunity to lava damage and debuff.[1]
86:  * The effects of the Obsidian Rose and the accessories crafted from it do not stack; wearing two or more does not reduce the base damage of lava below 35.
87:  * In [Remix](Remix.md "Remix") and [Zenith](Zenith_\(seed\) "Zenith \(seed\)") worlds, where lava is more hazardous, the Obsidian Rose and the accessories crafted from it decrease the damage from 200 to 155 and the duration of On Fire! from 10.5 / [21](Expert_Mode.md "Expert Mode") / [26.25](Master_Mode.md "Master Mode") seconds to 7 / [14](Expert_Mode.md "Expert Mode") / [17.5](Master_Mode.md "Master Mode") seconds.[1]
91:  * More effective and easily accessible means of surviving contact with lava, such as [Obsidian Skin Potions](Obsidian_Skin_Potion.md "Obsidian Skin Potion") and [Lava Charms](Lava_Charm.md "Lava Charm"), become available during or even before the stage of progression where a player could reasonably begin looking for an Obsidian Rose. Combined with how rarely it appears, and the fact that all its alternatives prevent lava damage outright, an Obsidian Rose has usually outlived its usefulness before it is even found. 
100:    * Drop rate increased from 1/50 to 1/20.
105:    * Lava damage reduction increased from 30 to 45.
123:  * [Mobile 1.2.6508](Mobile_1.2.6508.md "Mobile 1.2.6508"): Introduced.
1084:  * Entities introduced in Mobile 1.2.6508
1102:enemies]: Maximum number of enemies Abigail can damage at once
1648:dmg]: Attack damage

```


---

## 🤖 Assistant · 2026-08-13T00:40:00.766Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good progress. Now:
- Lava_Charm.md: line 43 "grants immunity to lava for 7 seconds". Line 97 stacking note.
- Lava_Waders.md: line 29-35 "Immunity to lava for 7 seconds", need full list of granted effects. Let me read lines 20-45.
- Obsidian_Rose.md: line 39 "reduces the base damage taken from lava from 80 to 35", halves duration. Line 86: doesn't stack below 35. Line 87: Remix/Zenith 200 → 155.
- Need Obsidian_Skin_Potion.md: duration.
- Lava_immunity.md.
- Cactus.md / Cactus_plant.md.
- Suffocation.md.
- Rolling_Cactus.md.

Note: Lava.md line 150 says Obsidian Rose reduces "from 80 to 35 (Desktop, Console and Mobile) / 50 (Old-gen console and 3DS)". Obsidian_Rose.md line 39 says 80 to 35. Both should be quoted.

Let me continue.
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:40:01.045Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Lava_Waders.md",
 "limit": 20,
 "offset": 19
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:01.053Z

**📎 ToolResult**

```
19	---|---  
20	[Tooltip](Tooltips.md "Tooltips")|  _Provides the ability to walk on water, honey & lava  
21	Grants immunity to fire blocks and 7 seconds of immunity to lava  
22	Reduces damage from touching lava_  
23	[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_7 "Lime \(Rarity level: 7\)")  
24	[Sell](Value.md "Value")| 10 _GC_  
25	[Research](Journey_Mode#Research "Journey Mode")| 1 required  
26	  
27	  * Internal [Item ID](Item_IDs.md "Item IDs"): **908**
28	
29	The **Lava Waders** are a [pre-Hardmode](Pre-Hardmode.md "Pre-Hardmode") [immunity accessory](Immunity_accessory "Immunity accessory"). They grant the following effects while equipped: 
30	
31	  * The ability to stand and walk on the surface of all [liquids](Liquids.md "Liquids"). 
32	    * When walking on liquid, press the [`▼ Down`](Game_controls.md "Game controls") key allows submerging into the liquid.
33	  * Prevents [fall damage](Fall_damage.md "Fall damage") when landing on the surface of any liquid.
34	  * Immunity to the [Burning](Burning.md "Burning") [debuff](Debuff "Debuff").
35	  * Immunity to [lava](Lava.md "Lava") for 7 seconds.
36	  * Decreases the damage taken from lava from 80 to 35, and reduces the duration of [On Fire!](On_Fire!.md "On Fire!") debuff inflicted by lava from 7 / [14](Expert_Mode.md "Expert Mode") / [17.5](Master_Mode.md "Master Mode") seconds to 3.5 / [7](Expert_Mode.md "Expert Mode") / [8.75](Master_Mode.md "Master Mode") seconds.
37	  * Equipping the [Ash Wood armor](Ash_Wood_armor.md "Ash Wood armor") at the same time provides immunity to lava damage and debuff.
38	

```


---

## 🤖 Assistant · 2026-08-13T00:40:01.732Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"duration|minute|immune|lava for|Obsidian Skin\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Obsidian_Skin_Potion.md | grep -v \"^\\s*[0-9]*:\\s*\\*\\[\" | head -20",
 "description": "Find duration and immunity in Obsidian_Skin_Potion.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:01.755Z

**📎 ToolResult**

```
1:# Obsidian Skin Potion
5:# Obsidian Skin Potion
10:For the differences of this information on [Old-gen console](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [3DS](Legacy%3A3DS_version "Legacy:3DS version"), see **[Legacy:Obsidian Skin Potion](Legacy%3AObsidian_Skin_Potion "Legacy:Obsidian Skin Potion")**.
12:Obsidian Skin Potion
29:Buff| [](Obsidian_Skin_Potion.md "Obsidian Skin")Obsidian Skin  
31:Buff tooltip|  _Immune to lava_  
32:Duration| 6 minutes  
81:The **Obsidian Skin Potion** is a [buff potion](Buff_potions.md "Buff potions") which grants the **Obsidian Skin** [buff](Buffs.md "Buffs") when consumed. The buff makes the player immune to [lava](Lava.md "Lava") and the [On Fire!](On_Fire!.md "On Fire!") [debuff](Debuffs.md "Debuffs"). It also grants immunity to the [Burning](Burning.md "Burning") debuff from touching [Meteorite](Meteorite.md "Meteorite"), [Hellstone](Hellstone.md "Hellstone"), [Hellstone Bricks](Hellstone_Brick.md "Hellstone Brick"), and [Ancient Hellstone Bricks](Ancient_Hellstone_Brick.md "Ancient Hellstone Brick") for its duration. This lasts for 6 minutes, but can be canceled at any time by right-clicking the icon ([](Desktop_version_history.md "Desktop version")), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff ([](Console_version.md "Console version")), or by double-tapping the buff icon ([](Mobile_version.md "Mobile version")). 
83:In addition to being crafted, Obsidian Skin Potions can be found in [pots](Pot.md "Pot") and [Shadow Chests](Shadow_Chest.md "Shadow Chest") in [the Underworld](The_Underworld.md "The Underworld"), as well as in [crates](Crates.md "Crates"). 
91:[](Obsidian_Skin_Potion.md "Obsidian Skin Potion")Obsidian Skin Potion| 
106:  * When the player equips an [Obsidian Skull](Obsidian_Skull.md "Obsidian Skull") (or its upgrades) or benefits from the Obsidian Skin buff, the [Dangersense](Dangersense "Dangersense") buff will no longer highlight [Hellstone](Hellstone.md "Hellstone"), [Hellstone Bricks](Hellstone_Brick.md "Hellstone Brick"), and [Meteorite](Meteorite.md "Meteorite").
115:  * The Obsidian Skin buff was the first buff ever added to the game.
123:  * [Desktop 1.4.0.1](Desktop_1.4.0.1 "Desktop 1.4.0.1"): Duration increased from 4 to 6 minutes.
127:  * [Desktop 1.0.6](Desktop_1.0.6 "Desktop 1.0.6"): Duration increased from 3 to 4 minutes.
161:  * [](Obsidian_Skin_Potion.md "Obsidian Skin Potion")Skin Potion
254:  * Obsidian Skin
1051:  * [](Obsidian_Skin_Potion.md "Obsidian Skin")Obsidian Skin

```


---

## 🤖 Assistant · 2026-08-13T00:40:02.381Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"7 second|immune|immunity|49|14 second|stack\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Lava_immunity.md | grep -v \"^\\s*[0-9]*:\\s*\\*\\[\" | head -25",
 "description": "Find immunity rules in Lava_immunity.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:02.408Z

**📎 ToolResult**

```
1:# Lava immunity
3:> 原页面: `Lava_immunity`
5:[Lava immunity](./Lava#lava_immunity)

```


---

## 🤖 Assistant · 2026-08-13T00:40:02.887Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"damage|expert|master\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Cactus_plant.md | grep -v \"^\\s*[0-9]*:\\s*\\*\\[\" | head -20",
 "description": "Find damage values in Cactus_plant.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:02.911Z

**📎 ToolResult**

```
18:enemies]: Maximum number of enemies Abigail can damage at once

```


---

## 🤖 Assistant · 2026-08-13T00:40:08.186Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
- Lava_Waders.md lines 20-22 tooltip, 29-37 effects list: 7s lava immunity, reduces damage from 80 to 35, reduces On Fire! duration.
- Obsidian_Skin_Potion.md: line 32 Duration 6 minutes, line 81 buff makes player immune to lava and On Fire! for 6 minutes.
- Lava_immunity.md: line 5 is a redirect to ./Lava#lava_immunity — so content is in Lava.md. Lava.md line 154 has the stacking max (49 / 14 s).
- Cactus_plant.md: no damage mention other than legend noise. Let me check the head of Cactus_plant.md to see what it says — probably it redirects to Cactus.md or says cacti don't deal damage? Let me read.

Now: Cactus.md, Suffocation.md, Rolling_Cactus.md.
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:40:08.291Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Cactus_plant.md",
 "limit": 30
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:08.297Z

**📎 ToolResult**

```
1	# Cactus plant
2	
3	> 原页面: `Cactus_plant`
4	
5	[Cactus plant](./Cactus#Plant)
6	  *[1 required]: Journey Mode
7	  *[Qty.]: Quantity
8	  *[100%]: Mode Expert
9	  *[DPS]: Damage per second
10	  *[sic]: sīc erat scriptum (Latin: “thus it was written”) – any typographical or other errors in this quote are intentionally reproduced, exactly as they appear in the source.
11	  *[300]: Master Mode
12	  *[400]: Expertní mód
13	  *[160]: Expertní mód
14	  *[240]: Master Mode
15	  *[3 required]: Journey Mode
16	  *[#]: Number of Bees
17	  *[Max.  
18	enemies]: Maximum number of enemies Abigail can damage at once
19	  *[HM]: Hardmode
20	  *[**Click/tap here** to reveal this content. _(there may be a slight delay)_]: This content exists externally. Once you click, there may be a small delay while it is downloaded.
21	  *[**Klik/tap disini** untuk melihat isi konten. _(mungkin akan sedikit delay)_]: Konten ini tersedia secara eksternal. Ketika di klik, mungkin akan ada sedikit delay ketika melihat isi konten.
22	  *[**Bấm/Chạm vào đây** để hiển thị nội dung này. _(có thể sẽ bị delay một chút)_]: Nội dung này được lấy từ các nguồn bên ngoài. Khi bấm vào, có thể sẽ bị delay một chút trong khi nó tải.
23	  *[8]: Expert Mode
24	  *[10]: Expert Mode
25	  *[120]: Master Mode
26	  *[150]: Master Mode
27	  *[13]: Chế độ Master
28	  *[195]: Master Mode
29	  *[Verify]: How does the remaining 1/2 behave? Are there Cacti on incomplete blocks, or is there a subsequent step to clean up those incomplete Sand Blocks?
30	  *[50 required]: Journey Mode

```


---

## 🤖 Assistant · 2026-08-13T00:40:08.825Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"10 damage|damage|contact\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Cactus.md | grep -v \"^\\s*[0-9]*:\\s*\\*\\[\" | head -20",
 "description": "Find damage values in Cactus.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:08.847Z

**📎 ToolResult**

```
301:  * Neither the plant nor the placed item deal contact damage to any entity, although it used to before [1.1](1.1.md "1.1"). 
302:    * However, the plant does deal contact damage in a [The Constant](The_Constant.md "The Constant") world.
335:  * [Desktop 1.1](Desktop_1.1 "Desktop 1.1"): No longer damages players (used to cause 10 damage).
1118:  * [Damage Booster](Damage_Booster.md "Damage Booster")
1775:enemies]: Maximum number of enemies Abigail can damage at once

```


---

## 🤖 Assistant · 2026-08-13T00:40:09.384Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"health|per second|hp|damage\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Suffocation.md | grep -v \"^\\s*[0-9]*:\\s*\\*\\[\" | head -20",
 "description": "Find HP drain values in Suffocation.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:09.407Z

**📎 ToolResult**

```
17:−20 health per second
33:**Suffocation** is a [debuff](Debuff "Debuff") that is inflicted when the player is submerged in falling [Sand](Sand "Sand"), [Silt](Silt "Silt"), or [Slush](Slush "Slush"), causing them to lose 20 health per second for as long as they are submerged. [Drowning](Drowning.md "Drowning") will not inflict this debuff. Red damage numbers appear as the player loses health, like other debuffs that inflict continuous damage. 
35:Suffocation causes the 5-damage ticks after impact.
60:  * Suffocation will be caused only be the blocks listed above, and not by any other blocks the player may get clipped inside of. For example, [Obsidian](Obsidian.md "Obsidian") forming over the player or being [hoiked](Hoik.md "Hoik") into other blocks will not cause Suffocation damage.
129:  * [](Damage_Booster.md "Damage Nebula")[Damage Nebula](Damage_Booster.md "Damage Booster")**** __(Desktop, Console and Mobile versions)
495:enemies]: Maximum number of enemies Abigail can damage at once
1041:dmg]: Attack damage
1230:40 when below 145 health]: Expert Mode
1232:60 when below 185 health]: Master Mode

```


---

## 🤖 Assistant · 2026-08-13T00:40:10.020Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"damage|knockback\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Rolling_Cactus.md | grep -v \"^\\s*[0-9]*:\\s*\\*\\[\" | head -15",
 "description": "Find damage values in Rolling_Cactus.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:10.042Z

**📎 ToolResult**

```
46:A stationary Rolling Cactus deals 25 damage when a player touches it.[1] A Rolling Cactus projectile deals 70 / [140](Expert_Mode.md "Expert Mode") / [210](Master_Mode.md "Master Mode") damage to players (35 damage to [NPCs](NPCs.md "NPCs"), [enemies](Enemies.md "Enemies"), and [critters](Critters.md "Critters")) and inflicts a [knockback](Knockback.md "Knockback") value of 10 (Extremely strong) upon contact.[2] Rolling Cactus Spikes deal 60 / [120](Expert_Mode.md "Expert Mode") / [180](Master_Mode.md "Master Mode") damage to players (30 damage to NPCs, enemies, and critters), inflict a [knockback](Knockback.md "Knockback") value of 2 (Very weak), pierce entities, and break upon contact with solid tiles.[3]
64:  * Once rolling, a Rolling Cactus always causes the same amount of damage, regardless of its speed. A player or enemy hit by a Rolling Cactus that just began rolling will take just as much damage as they would from a fast-moving Rolling Cactus.
81:    * Rolling Cactus projectile damage reduced from 90 to 70.
86:    * Reduced the base Rolling Cactus projectile damage from 140 to 90.
87:    * Increased the base Rolling Cactus Spike projectile damage from 40 to 60.
657:enemies]: Maximum number of enemies Abigail can damage at once
1203:dmg]: Attack damage

```


---

## 🤖 Assistant · 2026-08-13T00:40:13.939Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
- Cactus_plant.md: redirect to ./Cactus#Plant. No numbers.
- Cactus.md line 301-302: neither plant nor placed item deals contact damage (used to before 1.1); but plant DOES deal contact damage in The Constant world. Line 335: no longer damages players (used to cause 10 damage). Need to check if there's a number for The Constant damage. Let me grep Cactus.md for "Constant" damage value.
- Suffocation.md: line 33 "lose 20 health per second". Line 17 infobox "−20 health per second". Line 35: 5-damage ticks. Let me read around lines 30-60 for details (expert scaling? ticks).
- Rolling_Cactus.md line 46: stationary 25 damage; projectile 70/140/210; spikes 60/120/180.

Let me check Cactus.md The Constant damage value and read Suffocation.md more fully. Also confirm Lava.md line 154 context (stacking max) is the "Lava immunity" section — read around lines 140-160.
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:40:14.415Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -B 2 -A 2 \"The Constant\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Cactus.md | grep -v \"^\\s*[0-9]*[-:]\\s*\\*\\[\" | head -25",
 "description": "Check The Constant damage context in Cactus.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:14.438Z

**📎 ToolResult**

```
300-  * The Cactus plant is designed after the [saguaro](https://en.wikipedia.org/wiki/en:saguaro "wikipedia:en:saguaro"), a cactus species found in North America noted for its "arms" and exceptional overall size.
301-  * Neither the plant nor the placed item deal contact damage to any entity, although it used to before [1.1](1.1.md "1.1"). 
302:    * However, the plant does deal contact damage in a [The Constant](The_Constant.md "The Constant") world.
303-
304-## History

```


---

## 🤖 Assistant · 2026-08-13T00:40:14.679Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Suffocation.md",
 "limit": 35,
 "offset": 13
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:14.684Z

**📎 ToolResult**

```
13	[Debuff](Debuff "Debuff")
14	
15	### Effects
16	
17	−20 health per second
18	
19	### Tooltip
20	
21	_Losing life_
22	
23	## Internal IDs
24	
25	### [Buff ID](Buff_IDs.md "Buff IDs")
26	
27	68
28	
29	### Internal name
30	
31	`Suffocation`
32	
33	**Suffocation** is a [debuff](Debuff "Debuff") that is inflicted when the player is submerged in falling [Sand](Sand "Sand"), [Silt](Silt "Silt"), or [Slush](Slush "Slush"), causing them to lose 20 health per second for as long as they are submerged. [Drowning](Drowning.md "Drowning") will not inflict this debuff. Red damage numbers appear as the player loses health, like other debuffs that inflict continuous damage. 
34	
35	Suffocation causes the 5-damage ticks after impact.
36	
37	## Causes
38	
39	### From environment
40	
41	[Sand Block and variants](Sand_Blocks.md "Sand Blocks"), [Silt Blocks](Silt_Block.md "Silt Block"), and [Slush Blocks](Slush_Block.md "Slush Block") inflict suffocation for as long as they intersect the player. 
42	
43	From  | Duration   
44	---|---  
45	[](Sand_Block "Sand Block") | [Sand Block](Sand_Block "Sand Block") | Until the player gets out from under the Sand Blocks   
46	[](Ebonsand_Block "Ebonsand Block") | [Ebonsand Block](Ebonsand_Block "Ebonsand Block") | Until the player gets out from under the Ebonsand Blocks   
47	[](Pearlsand_Block "Pearlsand Block") | [Pearlsand Block](Pearlsand_Block "Pearlsand Block") | Until the player gets out from under the Pearlsand Blocks   

```


---

## 🤖 Assistant · 2026-08-13T00:40:14.896Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Lava.md",
 "limit": 16,
 "offset": 144
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:14.901Z

**📎 ToolResult**

```
144	  * [](Water_Bucket "Water Bucket")[Water Bucket](Water_Bucket "Water Bucket")
145	
146	  * The exact depth at which lava will begin replacing all water in a world is different for every world and can vary by up to several hundred feet/tiles between worlds; the approximate depths given above are _only averages_.[1]
147	  * The damage from lava can be reduced by [defense](Defense.md "Defense") and [damage reduction](Damage_reduction.md "Damage reduction"). Apart from that, the following items allow for reducing or eliminating lava damage: 
148	    * [](Obsidian_Skin_Potion.md "Obsidian Skin Potion")[Obsidian Skin Potion](Obsidian_Skin_Potion.md "Obsidian Skin Potion"): Grants a buff when consumed which provides lava immunity for its entire duration.
149	    * [](Superheated_Blood.md "Superheated Blood")[Superheated Blood](Superheated_Blood.md "Superheated Blood")**** __(Desktop, Console and Mobile versions) : Summons a Lava Shark Mount, which provides unlimited lava immunity, as well as fast movement in liquids.
150	    * [](Obsidian_Rose.md "Obsidian Rose")[Obsidian Rose](Obsidian_Rose.md "Obsidian Rose")and its upgrades: Reduces the base damage taken from lava from 80 to ****__(Desktop, Console and Mobile versions) 35 / ****__(Old-gen console and 3DS versions) 50 and halves the duration of the inflicted [On Fire!](On_Fire!.md "On Fire!") [debuff](Debuff "Debuff") from 7 / [14](Expert_Mode.md "Expert Mode") / [17.5](Master_Mode.md "Master Mode") seconds to 3.5 / [7](Expert_Mode.md "Expert Mode") / [8.75](Master_Mode.md "Master Mode") seconds.
151	    * [](Ash_Wood_armor.md "Ash Wood armor")[Ash Wood armor](Ash_Wood_armor.md "Ash Wood armor")(set bonus)****__(Desktop, Console and Mobile versions) : Halves the base damage taken from lava from 80 to 40 and halves the duration of the inflicted On Fire! debuff from 7 / [14](Expert_Mode.md "Expert Mode") / [17.5](Master_Mode.md "Master Mode") seconds to 3.5 / [7](Expert_Mode.md "Expert Mode") / [8.75](Master_Mode.md "Master Mode") seconds.
152	    * Equipping both Ash Wood armor and the Obsidian Rose (or its upgrades) provides unlimited lava immunity. 
153	      * In this case, lava immunity time from the following items will still be consumed.
154	  * Various [accessories](Accessories.md "Accessories") and one type of [minecart](Minecarts.md "Minecarts") allow the player to be submerged in lava for some time without taking damage. This immunity is similar to the [breath meter](Breath_meter.md "Breath meter") while underwater, but it has its own separate bar, is immediately activated upon touching lava, and takes much longer to refill than the breath meter after exiting lava. Each of these items grants 7 seconds of immunity. If multiple of these items are equipped/used simultaneously, the duration of immunity will be stacked, up to a maximum of ****__(Desktop, Console and Mobile versions) 49 / ****__(Old-gen console and 3DS versions) 14 seconds if all of them are used.
155	
156	    
157	
158	  * [](Lava_Charm.md "Lava Charm")[Lava Charm](Lava_Charm.md "Lava Charm")
159	  * [](Molten_Charm.md "Molten Charm")[Molten Charm](Molten_Charm.md "Molten Charm")**** __(Desktop, Console and Mobile versions)

```


---

## 🤖 Assistant · 2026-08-13T00:40:19.126Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have everything I need. A couple of remaining checks:

1. Cactus.md — the plant deals contact damage in The Constant world, but no number given. Let me quickly grep for any number near "Constant" in Cactus.md... already did — line 302 says it deals contact damage but no number. So the wiki doesn't give a value for The Constant cactus damage (only the historical 10 damage). I should state that.

2. Suffocation — no expert/master scaling mentioned? The wiki says 20 HP/s; I saw no difficulty multiplier in grep. Let me double check for "Expert" in Suffocation.md outside legend noise.

3. Lava_Charm.md line 43 confirmed 7 seconds. Also check for notes about stacking in Lava_Charm.md — line 97 already.

4. Lava_Waders.md line 36 — confirmed 80 to 35.

Also double-check whether Lava.md mentions expert/master multiplier for lava contact damage itself — line 13 says players take 80 damage (no difficulty variation), only On Fire! duration varies. Good.

Quick check on Suffocation expert mentions.
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:40:19.670Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"expert|master\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Suffocation.md | grep -v -E \"^\\s*[0-9]+:\\s*\\*\\[\" | head -10",
 "description": "Check difficulty scaling mentions in Suffocation.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:19.691Z

**📎 ToolResult**

```
56:[](Red_Potion.md "Red Potion") | [Red Potion](Red_Potion.md "Red Potion")**** __(Desktop, Console and Mobile versions)(except [For the Worthy](For_the_Worthy.md "For the Worthy") and [Zenith](Zenith_\(seed\) "Zenith \(seed\)") worlds) | 1 / [2](Expert_Mode.md "Expert Mode") / [3](Master_Mode.md "Master Mode") hours  | 1/1 (100%)   
1230:40 when below 145 health]: Expert Mode
1232:60 when below 185 health]: Master Mode
1237:40 khi dưới 145 máu]: Chế độ Expert
1239:60 khi dưới 185 máu]: Chế độ Master
1631:]: Expert Mode
1637:]: Master Mode
1643:]: Expert Mode
1649:]: Master Mode

```


---

## 🤖 Assistant · 2026-08-13T00:40:20.281Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"stack|7 seconds\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Lava_Charm.md | grep -v -E \"^\\s*[0-9]+:\\s*\\*\\[\" | head -10",
 "description": "Check stacking notes in Lava_Charm.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:20.307Z

**📎 ToolResult**

```
20:[Tooltip](Tooltips.md "Tooltips")|  _Provides 7 seconds of immunity to lava_  
43:The **Lava Charm** is an [accessory](Accessory "Accessory") that grants immunity to [lava](Lava.md "Lava") for 7 seconds. It is found in [Chests](Chests.md "Chests") located in the [cavern](Cavern.md "Cavern") layer as well as obtained from [Hellstone Crates](Hellstone_Crate.md "Hellstone Crate") and [Obsidian Crates](Obsidian_Crate.md "Obsidian Crate") with a 1/20 (5%) chance. It can only be found in Chests in the lower portion of the Caverns where [lava](Lava.md "Lava") pools can naturally spawn, as opposed to Chests throughout the entirety of the Caverns. 
97:  * The [Molten Charm](Molten_Charm.md "Molten Charm"), [Magma Skull](Magma_Skull.md "Magma Skull"), [Molten Skull Rose](Molten_Skull_Rose.md "Molten Skull Rose"), [Lava Waders](Lava_Waders.md "Lava Waders"), and [Terraspark Boots](Terraspark_Boots.md "Terraspark Boots") all stack with the Lava Charm to increase lava immunity by 7 seconds each. The [Demonic Hellcart](Demonic_Hellcart.md "Demonic Hellcart") also gives an additional 7 seconds. Of these, only the Demonic Hellcart is not itself a Lava Charm upgrade.

```


---

## 🤖 Assistant · 2026-08-13T00:40:22.469Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All data collected. Suffocation has no Expert/Master scaling on the 20 HP/s (only Red Potion duration scales with difficulty, which is a cause, not the debuff value).

Now compose the final report. Each page one entry, filename + approximate line number + original English sentence. Note redirect pages clearly. No speculation.
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:40:44.778Z · glm-x-preview-260804

```
全部提取完成。以下按页面逐条汇报(所有行号均为 `grep -n` 实测行号;`*_partial`/分类页噪音已排除)。

## 1. 地刺(Spike)系列

**~/Project/GLM/SandboxWorld/terraria-wiki-md/Spike.md**(真正的地刺页面)
- L40(核心数值):"The **Spike** is a trap that can be found in the Dungeon. Upon contact, it deals 60 damage to the player, on all difficulties, and inflicts the Bleeding debuff for 10 / 20 (Expert Mode) / 25 (Master Mode) seconds."
- L34(infobox):"Duration| 10 / 20(Expert)/ 25(Master)seconds",Chance 100%。
- 难度倍率:**接触伤害无倍率**,明确"60 damage ... on all difficulties";只有 Bleeding 持续时间随难度变长(10/20/25 秒)。
- 触发方式:L40 "Upon contact"(接触即触发);L61 "Spikes only damage players.";L60 "Spike damage can be dodged, but not the Bleeding debuff.";L83(1.3.0.5)"Spike damage is kept separate from other damage when factoring immunity, preventing abuse of invincibility frames."
- 历史变更:L81 "Damage increased from 40 to 60, and now inflicts the Bleeding debuff."(1.4.0.1)

**~/Project/GLM/SandboxWorld/terraria-wiki-md/Spiked.md**
- **重定向存根,无任何数值。** L5 仅一行:`[Spiked](./Modifiers#Accessory_modifiers)`,重定向到 Modifiers 页的 Accessory modifiers 锚点。即 wiki 上 "Spiked" 是饰品前缀名,不是陷阱。全页其余内容均为图例/导航噪音。

**~/Project/GLM/SandboxWorld/terraria-wiki-md/Wooden_Spike.md**
- L40(核心数值):"The **Wooden Spike** ... deals 80 damage on contact and inflicts the Bleeding debuff for 10 / 20(Expert)/ 25(Master)seconds."
- 难度倍率:L48 "Wooden Spikes deal the same base amount of damage in all difficulties. Since defense is more efficient in Expert and Master Mode, the player will almost always receive less damage from Wooden Spikes than in Classic Mode."(基础伤害无倍率,实际受伤因防御效率反而更低)
- 触发方式:L46 "Wooden Spikes will deal damage to a player if any part of the player is in contact with them.";L47 "they do not damage NPCs, critters, or enemies"。
- Trivia L54:"the Wooden Spike deals more damage than the metal Spike."
- 历史变更:L69 "Damage increased from 60 to 80."

**~/Project/GLM/SandboxWorld/terraria-wiki-md/Spike_pit.md**
- **重定向存根,无数值。** L5 仅:`[Spike pit](./Traps#Spike_Pits)`。实际内容在 Traps.md:Traps.md L137 "Spike Pits can be found throughout the Dungeon, and consist of a thick row of Cracked Dungeon Bricks above a large rectangular pit. Surrounding the pit on all sides are spikes, which can quickly deal large amounts of damage."(未给出独立数值,伤害即 Spike 的 60)

## 2. Lava.md

**~/Project/GLM/SandboxWorld/terraria-wiki-md/Lava.md**
- L13(核心数值):"Contact with lava deals damage (which is not affected by damage variance) and inflicts the On Fire! debuff. Players take 80 damage and the debuff lasts for 7 / 14 (Expert) / 17.5 (Master) seconds, whereas enemies, NPCs, and critters take 50 damage and the debuff lasts for 7 seconds."
- 即:**玩家 80 伤害(普通/专家/大师相同,无倍率),On Fire! 7/14/17.5 秒;敌人/NPC/小动物 50 伤害、7 秒。**
- 免疫规则概述:L147–154(Lava immunity 小节,Lava_immunity.md 即指向此处):
  - L147 "The damage from lava can be reduced by defense and damage reduction."
  - L148 "Obsidian Skin Potion: Grants a buff when consumed which provides lava immunity for its entire duration."
  - L154 "Each of these items grants 7 seconds of immunity. If multiple of these items are equipped/used simultaneously, the duration of immunity will be stacked, up to a maximum of 49 (Desktop, Console and Mobile) / 14 (Old-gen console and 3DS) seconds if all of them are used."(**叠加上限 49 秒,旧平台 14 秒**)

## 3. 防护装备

**~/Project/GLM/SandboxWorld/terraria-wiki-md/Lava_immunity.md**
- **重定向存根,无数值。** L5 仅:`[Lava immunity](./Lava#lava_immunity)`。规则见 Lava.md L147–154(上文已引)。

**~/Project/GLM/SandboxWorld/terraria-wiki-md/Lava_Charm.md**
- L43:"The **Lava Charm** is an accessory that grants immunity to lava for 7 seconds."(确认 7 秒)
- L20(tooltip):"_Provides 7 seconds of immunity to lava_"
- 叠加:L97 "The Molten Charm, Magma Skull, Molten Skull Rose, Lava Waders, and Terraspark Boots all stack with the Lava Charm to increase lava immunity by 7 seconds each. The Demonic Hellcart also gives an additional 7 seconds."

**~/Project/GLM/SandboxWorld/terraria-wiki-md/Lava_Waders.md**
- L20–22(tooltip):"Provides the ability to walk on water, honey & lava / Grants immunity to fire blocks and 7 seconds of immunity to lava / Reduces damage from touching lava"
- L29–37 完整效果列表:L31 行走于所有液体表面;L33 落在液面免摔伤;L34 "Immunity to the Burning debuff.";L35 "Immunity to lava for 7 seconds.";L36 "Decreases the damage taken from lava from 80 to 35, and reduces the duration of On Fire! debuff inflicted by lava from 7 / 14(Expert)/ 17.5(Master)seconds to 3.5 / 7(Expert)/ 8.75(Master)seconds.";L37 与 Ash Wood armor 同装备时完全免疫岩浆伤害与 debuff。

**~/Project/GLM/SandboxWorld/terraria-wiki-md/Obsidian_Rose.md**
- L39:"The **Obsidian Rose** is an accessory that reduces the base damage taken from lava from 80 to 35 and halves the duration of the On Fire! debuff inflicted by it from 7 / 14(Expert)/ 17.5(Master)seconds to 3.5 / 7(Expert)/ 8.75(Master)seconds."
- 叠加上限:L86 "The effects of the Obsidian Rose and the accessories crafted from it do not stack; wearing two or more does not reduce the base damage of lava below 35."
- 版本差异(Lava.md L150 补充):旧世代主机/3DS 是减到 50 而非 35:"Reduces the base damage taken from lava from 80 to 35 (Desktop, Console and Mobile) / 50 (Old-gen console and 3DS)"。
- 特殊种子世界 L87:"In Remix and Zenith worlds ... the Obsidian Rose ... decrease the damage from 200 to 155 and the duration of On Fire! from 10.5 / 21(Expert)/ 26.25(Master)seconds to 7 / 14(Expert)/ 17.5(Master)seconds."

**~/Project/GLM/SandboxWorld/terraria-wiki-md/Obsidian_Skin_Potion.md**
- L81:"The buff makes the player immune to lava and the On Fire! debuff. It also grants immunity to the Burning debuff from touching Meteorite, Hellstone, Hellstone Bricks, and Ancient Hellstone Bricks for its duration. This lasts for 6 minutes..."(**完全免疫岩浆,持续 6 分钟**)
- L32(infobox):"Duration| 6 minutes";L31 buff tooltip "_Immune to lava_"。
- 历史:L123 "Desktop 1.4.0.1: Duration increased from 4 to 6 minutes."

## 4. 仙人掌

**~/Project/GLM/SandboxWorld/terraria-wiki-md/Cactus.md**
- L301:"Neither the plant nor the placed item deal contact damage to any entity, although it used to before 1.1."(当前版本仙人掌植物与放置物**均不造成接触伤害**)
- L302:"However, the plant does deal contact damage in a The Constant world."(The Constant 种子世界中植物有接触伤害,但 **wiki 未给出具体数值**)
- L335(历史):"Desktop 1.1: No longer damages players (used to cause 10 damage)."(历史上的旧值是 10)

**~/Project/GLM/SandboxWorld/terraria-wiki-md/Cactus_plant.md**
- **重定向存根,无数值。** L5 仅:`[Cactus plant](./Cactus#Plant)`,内容在 Cactus.md(见上条)。

## 5. Suffocation.md

**~/Project/GLM/SandboxWorld/terraria-wiki-md/Suffocation.md**
- L33:"**Suffocation** is a debuff that is inflicted when the player is submerged in falling Sand, Silt, or Slush, causing them to lose **20 health per second** for as long as they are submerged."
- L17(infobox Effects):"−20 health per second"
- L35:"Suffocation causes the 5-damage ticks after impact."(结算表现为每跳 5 点)
- 触发方块:L41 "Sand Block and variants, Silt Blocks, and Slush Blocks inflict suffocation for as long as they intersect the player." 持续时间:直到脱离沙块(L45)。
- 难度倍率:页面正文**未提及** 20 HP/s 有专家/大师倍率(L56 的 1/2/3 hours 是 Red Potion 施加该 debuff 的持续时间随难度变化,非扣血值)。

## 6. Rolling_Cactus.md(顺手)

**~/Project/GLM/SandboxWorld/terraria-wiki-md/Rolling_Cactus.md**
- L46:"A stationary Rolling Cactus deals 25 damage when a player touches it. A Rolling Cactus projectile deals 70 / 140(Expert)/ 210(Master)damage to players (35 damage to NPCs, enemies, and critters) and inflicts a knockback value of 10 (Extremely strong) upon contact. Rolling Cactus Spikes deal 60 / 120(Expert)/ 180(Master)damage to players (30 damage to NPCs, enemies, and critters), inflict a knockback value of 2 (Very weak), pierce entities, and break upon contact with solid tiles."
- L64:"Once rolling, a Rolling Cactus always causes the same amount of damage, regardless of its speed."(滚动伤害与速度无关)

### 补充说明(避免误读)
- 镜像里每个页面尾部都有约 700–1600 行的图例噪音(`*[数值]: Expert Mode` 之类),本次所有引用行号都在正文区,已确认非导航内容。
- Spiked.md、Spike_pit.md、Lava_immunity.md、Cactus_plant.md 四个文件都是**一行重定向存根**,本身不含任何数值;真实数据分别在 Modifiers.md、Traps.md、Lava.md、Cactus.md。
```
