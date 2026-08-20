# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-20T02:56:11.145Z

```
任务代号 RECON-CONST（秘密种子只读侦察④——**全程零 src 改动**）。目标：为 The Constant（dontstarve 联动）种子的位级移植铺全图景。

## 四阶段
1. **Wiki 情报**：WebFetch https://terraria.wiki.gg/wiki/Secret_world_seeds ——触发文本全集+worldgen 特性清单（永夜/黑暗机制、墓地群系、独特地形——worldgen 域部分）。
2. **原版源码映射**：Terarria1456/ grep theConstant/WorldSeedOption_*——特性→flag→pass 分支（cs 行号）；已知线索：墓园 spawnGraveyardBiomesEverywhere 门（WorldGen.ts graveyardSeedGate 在案：theConstant&&(drunk||getGood)&&!tenth）、WavyCaves 仅饥荒世界（WorldGen 注释）、HHHH"AddSpikeCaves 系秘种子门"。
3. **JS 现状审计**：SeedEasterEggs 解析正则 vs vanilla；全管线消费点三列清单；UI 可达性。
4. **债规模定量**：干净基线（gen86.sh 模式，**专用端口 7904**，先 pgrep）产 .wld；JS 对拍→四通道+对象计数+头锚首图景与规模估计（不产槽链）。

## 纪律
零 src/tests 改动；金标零写入；既有 /tmp 资产只读；★>60s 命令 nohup+轮询；与其他在途批错峰；探针用完删；单命令 <8min；禁 kill 5199；不动 vite.config.ts。
交付：报告章「RECON-CONST」+memory 账本一行。
```

---

## 📎 Attachment · skill_listing · 2026-08-20T02:56:11.161Z

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

## 🤖 Assistant · 2026-08-20T02:57:34.390Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by understanding the task. This is RECON-CONST, a read-only reconnaissance of The Constant (dontstarve) secret world seed for the SandboxWorld project (a Terraria 1.4.5.6 clone in TypeScript).

Four phases:
1. Wiki intelligence: WebFetch https://terraria.wiki.gg/wiki/Secret_world_seeds — trigger text set + worldgen features list (eternal night/darkness mechanics, graveyard biome, unique terrain — worldgen domain parts)
2. Vanilla source mapping: Terarria1456/ grep theConstant/WorldSeedOption_* — feature→flag→pass branches (cs line numbers); known leads: graveyard spawnGraveyardBiomesEverywhere gate, WavyCaves only famine world, AddSpikeCaves secret seed gate
3. JS current state audit: SeedEasterEggs parsing regex vs vanilla; full pipeline consumption points three-column list; UI accessibility
4. Debt scale quantification: clean baseline (gen86.sh pattern, dedicated port 7904, pgrep first) produce .wld; JS comparison → four channels + object counts + header anchor first image and scale estimate (no slot chain production)

Disciplines:
- Zero src/tests changes
- Gold standard zero writes
- Existing /tmp assets read-only
- >60s commands use nohup+polling
- Stagger with other in-flight batches
- Delete probes after use
- Single command <8min
- No kill 5199
- Don't touch vite.config.ts

Deliverable: report chapter "RECON-CONST" + memory ledger line.

Let me start with parallel work: WebFetch the wiki, and grep the vanilla source. Let me first explore the directory structure to understand the codebase.

Let me kick off:
1. WebFetch wiki
2. Bash: find Terarria1456 directory location

Let me do these in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-20T02:57:34.972Z · glm-x-preview-260804

```
收到 RECON-CONST 任务。零改动侦察，四阶段推进。先并行启动 Wiki 情报与原版源码定位。
```


---

## 🤖 Assistant · 2026-08-20T02:57:37.661Z · glm-x-preview-260804

**🔧 ToolUse: `WebFetch`**

```json
{
 "url": "https://terraria.wiki.gg/wiki/Secret_world_seeds",
 "prompt": "Extract everything about \"The Constant\" (dontstarve / hunger / famine) secret world seed: (1) all seed trigger text strings that activate it, (2) all world generation features and terrain changes (darkness/eternal night mechanics, graveyard biome, unique terrain features, caves, structures), (3) any gameplay mechanics tied to it (light, hunger, darkness). Quote exact trigger strings and feature lists."
}
```


---

## 🤖 Assistant · 2026-08-20T02:57:38.452Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/ && ls ~/Project/GLM/SandboxWorld/Terarria1456/ | head -30",
 "description": "List project root and vanilla decompiled source directories"
}
```


---

## 👤 User(sidechain) · 2026-08-20T02:57:38.610Z

**📎 ToolResult**

```
annotations.json
backups
check-size.mjs
CLAUDE.md
docs
game
node_modules
server
session-archives
src
Terarria1405
Terarria1456
Terarria1456Server
Terraia_Maples
terraria-assets
Terraria-Map-Editor
terraria-wiki-md
terraria.wiki.gg_en_all_2026-07a.zim
tModLoader
tools
verify-bleed2.mjs
verify-dev.mjs
verify-quickload.mjs
verify-stable.mjs
verify-swing.mjs
verify-torch.mjs
verify-wld-persist.mjs
verify-wld2.mjs
开服.sh
app.ico
app.manifest
BCrypt.Net
Microsoft.Xna.Framework.RuntimeProfile
nativefiledialog.cs
Properties
Terraria
Terraria.Achievements
Terraria.Audio
Terraria.Chat
Terraria.Chat.Commands
Terraria.Cinematics
Terraria.csproj
Terraria.DataStructures
Terraria.Enums
Terraria.GameContent
Terraria.GameContent.Achievements
Terraria.GameContent.Ambience
Terraria.GameContent.Animations
Terraria.GameContent.Bestiary
Terraria.GameContent.Biomes
Terraria.GameContent.Biomes.CaveHouse
Terraria.GameContent.Biomes.Desert
Terraria.GameContent.Creative
Terraria.GameContent.Creative.Content.Sacrifices.tsv
Terraria.GameContent.Drawing
Terraria.GameContent.Dyes
Terraria.GameContent.Events
Terraria.GameContent.FishDropRules
Terraria.GameContent.Generation

```


---

## 👤 User(sidechain) · 2026-08-20T02:57:47.773Z

**📎 ToolResult ⚠️ERROR**

```
Unable to verify if domain terraria.wiki.gg is safe to fetch. This may be due to network restrictions or enterprise security policies blocking claude.ai.

```


---

## 🤖 Assistant · 2026-08-20T02:58:03.614Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
WebFetch failed on the domain. There's a local ZIM file `terraria.wiki.gg_en_all_2026-07a.zim` in the project root — I can extract the wiki article from there. Also there's a `terraria-wiki-md` directory which may have markdown versions of the wiki. Let me check both.

Also, let me start the vanilla source grep in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-20T02:58:04.426Z · glm-x-preview-260804

```
Wiki 直接抓取被拦，但项目根有 `terraria.wiki.gg_en_all_2026-07a.zim` 与 `terraria-wiki-md/` 本地资产，可离线提取。并行启动原版源码 grep。
```


---

## 🤖 Assistant · 2026-08-20T02:58:05.941Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/terraria-wiki-md/ 2>/dev/null | head -20; find ~/Project/GLM/SandboxWorld/terraria-wiki-md -iname \"*secret*world*\" -o -iname \"*constant*\" 2>/dev/null | head",
 "description": "Check local wiki markdown mirror for secret seeds article"
}
```


---

## 👤 User(sidechain) · 2026-08-20T02:58:06.200Z

**📎 ToolResult**

```
_categories_partials_Category_3DS_content_pages_1.md
_categories_partials_Category_3DS_content_pages_2.md
_categories_partials_Category_3DS_content_pages_3.md
_categories_partials_Category_3DS_content_pages_4.md
_categories_partials_Category_3DS_content_pages_5.md
_categories_partials_Category_3DS_content_pages_6.md
_categories_partials_Category_3DS_content_pages_7.md
_categories_partials_Category_3DS_content_pages_8.md
_categories_partials_Category_Accessory_items_pages_1.md
_categories_partials_Category_Accessory_items_pages_2.md
_categories_partials_Category_Achievement-related_elements_pages_1.md
_categories_partials_Category_Achievement-related_elements_pages_2.md
_categories_partials_Category_Autoswing_items_pages_1.md
_categories_partials_Category_Autoswing_items_pages_2.md
_categories_partials_Category_Bag_loot_items_pages_1.md
_categories_partials_Category_Bag_loot_items_pages_2.md
_categories_partials_Category_Buffs_pages_1.md
_categories_partials_Category_Buffs_pages_2.md
_categories_partials_Category_By_Hand_pages_1.md
_categories_partials_Category_By_Hand_pages_2.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Secret_world_seeds
~/Project/GLM/SandboxWorld/terraria-wiki-md/Category_Secret_world_seeds.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Constant.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Secret_world_seeds.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Guide_The_Constant.md

```


---

## 🤖 Assistant · 2026-08-20T02:58:06.720Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456 && grep -rn \"theConstant\\|TheConstant\" --include=\"*.cs\" -l | head -30",
 "description": "Find files referencing theConstant in vanilla source"
}
```


---

## 👤 User(sidechain) · 2026-08-20T02:58:06.970Z

**📎 ToolResult**

```
Terraria.WorldBuilding/WorldSeedOption_DontStarve.cs
Terraria.GameContent.UI.States/UIWorldCreation.cs

```


---

## 🤖 Assistant · 2026-08-20T02:58:40.342Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Found the wiki markdown files locally. Let me read them. Also there are two cs files referencing theConstant. Let me read those and grep for the seed options in WorldGen.cs etc.
```

</details>


---

## 🤖 Assistant · 2026-08-20T02:58:40.675Z · glm-x-preview-260804

```
本地 wiki 镜像齐全。并行读取 Wiki 文章与原版源码。
```


---

## 🤖 Assistant · 2026-08-20T02:58:42.194Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/terraria-wiki-md/Secret_world_seeds.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Constant.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Guide_The_Constant.md; ls ~/Project/GLM/SandboxWorld/terraria-wiki-md/Secret_world_seeds/ 2>/dev/null",
 "description": "Check wiki article sizes and subdirectory"
}
```


---

## 👤 User(sidechain) · 2026-08-20T02:58:42.311Z

**📎 ToolResult**

```
    1941 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Secret_world_seeds.md
    1928 ~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Constant.md
    1278 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Guide_The_Constant.md
    5147 total
row.md
section.md

```


---

## 🤖 Assistant · 2026-08-20T02:58:42.644Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.WorldBuilding/WorldSeedOption_DontStarve.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-20T02:58:42.700Z

**📎 ToolResult**

```
1	namespace Terraria.WorldBuilding;
2	
3	public class WorldSeedOption_DontStarve : AWorldGenerationOption
4	{
5		protected override string KeyName => "Seed_TheConstant";
6	
7		public override string ServerConfigName => "theconstant";
8	
9		public WorldSeedOption_DontStarve()
10		{
11			base.SpecialSeedNames = new string[4] { "constant", "theconstant", "eye4aneye", "eyeforaneye" };
12			base.SpecialSeedValues = new int[0];
13		}
14	}
15	

```


---

## 🤖 Assistant · 2026-08-20T02:59:08.516Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The vanilla source confirms 4 special seed names: "constant", "theconstant", "eye4aneye", "eyeforaneye". Now let me read the wiki articles. The Constant.md is the dedicated article. Let me read it, focusing on worldgen features. Also grep more broadly in vanilla source for how theConstant flag is used — it might be accessed via `WorldGen.TheConstant` or similar property. Let me grep for "TheConstant" usage (capital T) and "Seed_TheConstant".
```

</details>


---

## 🤖 Assistant · 2026-08-20T02:59:09.580Z · glm-x-preview-260804

```
触发词已定：`constant` / `theconstant` / `eye4aneye` / `eyeforaneye`。现在读 Wiki 主文并扩大源码 grep 范围。
```


---

## 🤖 Assistant · 2026-08-20T02:59:09.814Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Constant.md"
}
```


---

## 👤 User(sidechain) · 2026-08-20T02:59:10.045Z

**📎 ToolResult**

```
1	# The Constant
2	
3	> 原页面: `The_Constant`
4	
5	# The Constant
6	
7	[](Desktop_version_history.md "Desktop version") [](Console_version.md "Console version") [](Mobile_version.md "Mobile version")
8	
9	**[Desktop](Category%3ADesktop_content "Category:Desktop content")/[Console](Category%3AConsole_content "Category:Console content")/[Mobile](Category%3AMobile_content "Category:Mobile content")-Only Content**: This information applies _only_ to the **[Desktop](Desktop_version_history.md "Desktop version history")** , **[Console](Console_version.md "Console version")** , and **[Mobile](Mobile_version.md "Mobile version")** versions of _[Terraria](Terraria.md "Terraria")_.
10	
11	"Eyeforaneye" redirects here. For the patch named "An Eye For An Eye", see [1.4.3](1.4.3.md "1.4.3"). 
12	
13	The Constant
14	
15	Seed Information
16	
17	Codes| `constant``the constant``eye 4 an eye``eye for an eye`  
18	---|---  
19	Description|  _Bringing the Don’t Starve Together adventure into Terraria, can you survive persistent hunger as you seek to save Terraria? Oh, and don’t forget to stay in the light!_  
20	Type| [Special world seed](Special_world_seed "Special world seed")  
21	  
22	Image
23	
24	  * Map view of a [medium](World_size.md "World size") Constant world. Note the difference in cave generation.
25	
26	World Icons
27	
28	  * Corruption Pre‑Hardmode
29	
30	  * Crimson Pre‑Hardmode
31	
32	  * Corruption Hardmode
33	
34	  * Crimson Hardmode
35	
36	Shows an [Evergreen](https://dontstarve.wiki.gg/wiki/Evergreen "dts:Evergreen") from _Don't Starve_
37	
38	  * Internal Name: TheConstant
39	
40	**The Constant** is a [special world seed](Special_world_seeds.md "Special world seeds"). It is a [crossover](Crossover_content#Don't_Starve_Together "Crossover content") with Klei Entertainment's _[Don't Starve Together](https://dontstarve.wiki.gg/wiki/Don%27t_Starve_Together "dts:Don't Starve Together")_. 
41	
42	## World generation changes
43	
44	### Surface
45	
46	  * Marble patches occasionally spawn throughout the world on the surface with a few white-painted statues.
47	  * [Spider Nests](Spider_Nest.md "Spider Nest") or small patches of [Spider Walls](Spider_Wall.md "Spider Wall") often generate at or near the surface.
48	
49	### Underground
50	
51	  * The world generates with "wavy caves", which travel up and down in sharp zig-zag patterns, or travel diagonally downwards.
52	  * [Lead Ore](Lead_Ore.md "Lead Ore") and [Platinum Ore](Platinum_Ore.md "Platinum Ore") will never generate (i.e. only [Iron](Iron_Ore.md "Iron Ore") and [Gold Ore](Gold_Ore.md "Gold Ore") will appear in Constant worlds).
53	
54	## Player
55	
56	  * The player has a [hunger](Hunger.md "Hunger") system, which goes down over time and can be increased by consuming [food](Food.md "Food") items. When the player's current hunger level decreases, they will [emote](Emotes#General "Emotes"). 
57	    * The player's initial hunger starts at [Peckish](Peckish "Peckish"), which lasts 5 minutes. After that, the player becomes [Hungry](Hungry "Hungry"), which lasts 5 minutes and lowers the player's stats to be similar to [Weak](Weak.md "Weak").
58	    * Finally, the player starts [Starving](Starving "Starving"), which further lowers the player's stats and makes the player lose health equal to 2% of their max health per second indefinitely.
59	    * Consuming any food immediately replaces the hunger debuffs with the respective [Well Fed](Well_Fed.md "Well Fed") buff. After the buff ends, the player gets the Peckish debuff, and the cycle continues.
60	  * The player gains a custom hurt sound based on _Don't Starve_ -related characters. 
61	    * Male characters' hurt sound is the same as [Wilson](https://dontstarve.wiki.gg/wiki/Wilson "dts:Wilson")'s: 
62	    * Female characters' hurt sound is the same as [Willow](https://dontstarve.wiki.gg/wiki/Willow "dts:Willow")'s: 
63	
64	## Other changes
65	
66	The Constant's shader effect being shown right after loading into a world.
67	
68	  * The world has a constant sepia screen shader which significantly darkens the world. This effect can also be seen when generating the world. 
69	    * The shader will be disabled if the player equips the [Radio Thing](Radio_Thing "Radio Thing").
70	    * The shader will also not work under the Retro or Trippy [lighting modes](Lighting_mode.md "Lighting mode").
71	  * It will be pitch dark on the surface during normal nights. When a [New Moon](New_Moon "New Moon"), a [Full Moon](Full_Moon "Full Moon"), or a [Blood Moon](Blood_Moon.md "Blood Moon") occurs, the player will be able to see things normally on the surface.
72	  * When the player enters completely dark areas, the [status message](Status_message "Status message") _" It is very dark...you feel in danger..."_ will be displayed after three seconds, and after two more seconds (five seconds in total after entering the dark area), the player will take 250 base damage per second. This continuous damage will last until the player is illuminated by any type of light or dies. When the player gets illuminated, they will stop receiving damage from darkness, the 5-second damage timer will be reset, and the status message _" The danger of the dark has passed."_ will be displayed.[1] Dying from darkness will display the following unique [death message](Death_message.md "Death message"): _" <Player name> was killed by something in the dark!"_
73	  * [Cacti](Cactus.md "Cactus") will hurt the player when touched or chopped, with a base damage of 6.[2]
74	  * [Torches](Torches.md "Torches"), [Campfires](Campfires.md "Campfires"), [Tiki Torches](Tiki_Torch.md "Tiki Torch"), and [Lamps](Lamps.md "Lamps") exposed to the sky will be "extinguished" when it [rains](Rain.md "Rain"). 
75	    * Torch and Campfire variants which can be placed in water (i.e., the Coral, Cursed Flame, and Ichor varieties) will never be extinguished.
76	    * Other pieces of furniture that produce light and/or seem to be fire-based, like [Candles](Candles.md "Candles"), [Candelabras](Candelabras.md "Candelabras"), [Furnaces](Furnace.md "Furnace"), [Fireplaces](Fireplace.md "Fireplace"), [Lamp Posts](Lamp_Post.md "Lamp Post"), etc., will also remain lit.
77	  * _Don't Starve_ items will have their drop rate increased, these being the [Ham Bat](Ham_Bat.md "Ham Bat"), the [Bat Bat](Bat_Bat.md "Bat Bat"), [Monster Meat](Monster_Meat.md "Monster Meat"), the [Tentacle Spike](Tentacle_Spike.md "Tentacle Spike"), and the [Glommer's Flower](Glommer's_Flower.md "Glommer's Flower"). [Abigail's Flower](Abigail's_Flower.md "Abigail's Flower") has a higher spawn chance as well.
78	  * The [paintings](Paintings#From_Traveling_Merchant "Paintings") related to _Don't Starve_ that are sold by the [Traveling Merchant](Traveling_Merchant.md "Traveling Merchant") will be more common.
79	  * In [Expert](Expert "Expert") worlds, [Wall Creepers](Wall_Creeper.md "Wall Creeper") and [Black Recluses](Black_Recluse.md "Black Recluse") [saved](Coin_pickup_in_Expert_Mode.md "Coin pickup in Expert Mode") on the [minimap](Minimap.md "Minimap") can always respawn.[3]
80	  * [Rare clouds](Ambient_entities#Rare_clouds "Ambient entities") in the background are more common. 
81	    * Of these rare clouds, _Don't Starve_ -related clouds are more common.
82	
83	## Tips
84	
85	Main article: [Guide:The Constant](Guide%3AThe_Constant "Guide:The Constant")
86	
87	  * Early options for food include regular [Mushrooms](Mushroom.md "Mushroom"), [shaking trees](Trees#Shaking "Trees"), converting [Vertebrae](Vertebra.md "Vertebra") or [Rotten Chunks](Rotten_Chunk.md "Rotten Chunk") into [Monster Lasagna](Monster_Lasagna.md "Monster Lasagna"), and getting the [Merchant](Merchant.md "Merchant") to move in to buy a [Bug Net](Bug_Net.md "Bug Net") (or to buy [Marshmallows](Marshmallow.md "Marshmallow") if he is in a [Snow biome](Snow_biome.md "Snow biome")).
88	  * The [Mining Helmet](Mining_armor.md "Mining armor"), [Jellyfish Necklace](Jellyfish_Necklace.md "Jellyfish Necklace") and [Magiluminescence](Magiluminescence.md "Magiluminescence") can help keep the darkness away before [light pets](Pets#Light_Pets "Pets") are found.
89	  * By using [explosives](Explosives_\(class\) "Explosives \(class\)"), the player can harvest Cacti without taking damage.
90	  * To avoid damage from cacti while retaining Desert enemy spawns, place [platforms](Platforms.md "Platforms") 2 tiles above the Sand. This will prevent cacti from growing, but still allow enemies to spawn.
91	
92	## Trivia
93	
94	  * "The Constant" directly references [the world with the same name](https://dontstarve.wiki.gg/wiki/The_Constant "dts:The Constant") in _Don't Starve_.
95	  * Several world generation changes in the Constant seed recreate specific [Set Pieces](https://dontstarve.wiki.gg/wiki/Set_Piece "dts:Set Piece") or items in _Don't Starve_ : 
96	    * The Marble patches recreate the [Marble Sculptures](https://dontstarve.wiki.gg/wiki/Set_Piece#Marble_Sculptures_Set_Piece "dts:Set Piece") set piece.
97	    * The Spider Caves on the surface recreate [Spider Dens](https://dontstarve.wiki.gg/wiki/Spider_Den "dts:Spider Den").
98	  * Several game mechanics in The Constant seed are based on mechanics in _Don't Starve_ , these include: 
99	    * The shader is based on the shader effect in _Don't Starve_.
100	    * A world can only have [Iron](Iron_Ore.md "Iron Ore") and [Gold Ores](Gold_Ore.md "Gold Ore") due to the fact that only [Iron Ore](https://dontstarve.wiki.gg/wiki/Iron_Ore "dts:Iron Ore") and [Gold Nuggets](https://dontstarve.wiki.gg/wiki/Gold_Nugget "dts:Gold Nugget") exist in _Don't Starve_.
101	    * The [hunger](Hunger.md "Hunger") mechanic is directly based on _Don't Starve's_ [Hunger](https://dontstarve.wiki.gg/wiki/Hunger "dts:Hunger") mechanic.
102	    * In _Don't Starve_ , the player is also able to see things normally during [Full Moon](https://dontstarve.wiki.gg/wiki/Moon_Cycle "dts:Moon Cycle") nights. 
103	      * However, the player cannot see things during [New Moons](https://dontstarve.wiki.gg/wiki/Moon_Cycle "dts:Moon Cycle") in _Don't Starve_ , which is not the case in _Terraria_.
104	    * The mechanic of players getting damaged in completely dark areas is based on a similar mechanic of survivors being attacked by [Charlie](https://dontstarve.wiki.gg/wiki/Charlie "dts:Charlie") in complete darkness.
105	    * The player getting damaged by [Cacti](Cactus.md "Cactus") is based on _Don't Starve's_ [Cactus](https://dontstarve.wiki.gg/wiki/Cactus "dts:Cactus"), which damages the player by 6 health when harvesting it.
106	    * Exposed [Torches](Torches.md "Torches") and [Campfires](Campfires.md "Campfires") extinguish when Rain starts, as in _Don't Starve_ , [Rain](https://dontstarve.wiki.gg/wiki/Rain "dts:Rain") will make [Torches](https://dontstarve.wiki.gg/wiki/Torch "dts:Torch") and [Campfires](https://dontstarve.wiki.gg/wiki/Campfire "dts:Campfire") burn out faster.
107	
108	## History
109	
110	[ Desktop version](Desktop_version_history.md "Desktop version history")
111	
112	  * [Desktop 1.4.5.4](Desktop_1.4.5.4 "Desktop 1.4.5.4"): The Constant's filter is now correctly hidden when combined with [Skyblock](Skyblock.md "Skyblock").
113	
114	  * [Desktop 1.4.5.0](Desktop_1.4.5.0 "Desktop 1.4.5.0"): 
115	    * The Constant's filter is now hidden when mixed with other world seeds.
116	    * Added a sound effect for when the player is starving on The Constant worlds.
117	
118	  * [Desktop 1.4.4.6](Desktop_1.4.4.6 "Desktop 1.4.4.6"): [Cacti](Cacti.md "Cacti") are now highlighted by [Dangersense Potions](Dangersense_Potion.md "Dangersense Potion") on Constant Seeds.
119	
120	  * [Desktop 1.4.4](Desktop_1.4.4 "Desktop 1.4.4"): 
121	    * Darkness damage increased from 50 to 250, and the time before being hurt decreased from 8 to 4 seconds.
122	    * Eating regular [Mushrooms](Mushroom.md "Mushroom") will reset [hunger](Hunger.md "Hunger") back to full duration Peckish if the player is Peckish, Hungry, or Starving.
123	
124	  * [Desktop 1.4.3](Desktop_1.4.3 "Desktop 1.4.3"): Introduced.
125	
126	## References
127	
128	  1. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.3.6](1.4.3.6.md "1.4.3.6") source code, methods `UpdateDarknessState()` in `Terraria.GameContent.DontStarveDarknessDamageDealer.cs` and `Update()` in `Terraria.GameContent.DontStarveDarknessDamageDealer.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
129	  2. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.3.6](1.4.3.6.md "1.4.3.6") source code, methods `ItemCheck_UseMiningTools_ActuallyUseMiningTool()` in `Terraria.Player.cs`, `HurtTiles()` in `Terraria.Collision.cs`, and `Update()` in `Terraria.Player.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
130	  3. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, methods `WouldNPCBeDiscouraged()` in `Terraria.GameContent.CoinLossRevengeSystem.RevengeMarker.cs` and `DespawnEncouragement_AIStyle3_Fighters_NotDiscouraged()` in `Terraria.NPC.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
131	
132	View or edit this template
133	
134	[Special world seeds](Special_world_seeds.md "Special world seeds")
135	
136	  * [](Not_the_Bees.md "Not the Bees")[Not the Bees](Not_the_Bees.md "Not the Bees")
137	  * [](Drunk.md "Drunk")[Drunk](Drunk.md "Drunk")
138	  * [](Celebration_Mk_10.md "Celebration Mk 10")[Celebration Mk 10](Celebration_Mk_10.md "Celebration Mk 10")
139	  * [](The_Constant.md "The Constant")The Constant
140	  * [](For_the_Worthy.md "For the Worthy")[For the Worthy](For_the_Worthy.md "For the Worthy")
141	  * [](No_Traps.md "No Traps")[No Traps](No_Traps.md "No Traps")
142	  * [](Remix.md "Remix")[Remix](Remix.md "Remix")
143	  * [](Zenith_\(seed\) "Zenith \(seed\)")[Zenith](Zenith_\(seed\) "Zenith \(seed\)")
144	  * [](Skyblock.md "Skyblock")[Skyblock](Skyblock.md "Skyblock")
145	
146	View or edit this template
147	
148	Game mechanics
149	
150	Combat
151	
152	  * [Attack speed](Attack_speed.md "Attack speed")
153	  * [Autoswing](Autoswing.md "Autoswing")
154	  * [Critical hit](Critical_hit.md "Critical hit")
155	  * [Damage](Damage.md "Damage")
156	    * [Invincibility frame](Invincibility_frame.md "Invincibility frame")
157	  * [Knockback](Knockback.md "Knockback")
158	  * [Lock on](Lock_on.md "Lock on")**** __(Desktop, Console, Mobile and 3DS versions)
159	  * [Velocity](Velocity.md "Velocity")
160	
161	Environment
162	
163	  * [Ambient objects](Ambient_objects.md "Ambient objects")
164	  * [Ambient entities](Ambient_entities.md "Ambient entities")**** __(Desktop, Console and Mobile versions)
165	  * [Biome backgrounds](Biome_backgrounds.md "Biome backgrounds")
166	  * [Biomes](Biomes.md "Biomes")
167	    * [Spread](Biome_spread.md "Biome spread")
168	  * [Day and night cycle](Day_and_night_cycle.md "Day and night cycle")
169	  * [Events](Events.md "Events")
170	  * [Gravity](Gravity.md "Gravity")
171	  * [Liquids](Liquids.md "Liquids")
172	  * [Moon phase](Moon_phase.md "Moon phase")
173	  * [Music](Music.md "Music")
174	  * [NPC spawning](NPC_spawning.md "NPC spawning")
175	  * [Status messages](Status_messages.md "Status messages")
176	  * [Wind](Wind.md "Wind")
177	
178	Interface
179	
180	  * [Boss health bar](Boss_health_bar.md "Boss health bar")**** __(Desktop, Console and Mobile versions)
181	  * [Camera Mode](Camera_Mode.md "Camera Mode")**** __(Desktop version)
182	  * [Credits](Credits.md "Credits")**** __(Desktop, Console and Mobile versions)
183	  * [Emotes](Emotes.md "Emotes")**** __(Desktop, Console and Mobile versions)
184	  * [Minimap](Minimap.md "Minimap")
185	  * [Logo](Logo.md "Logo")
186	  * [NPC flag](NPC_flag.md "NPC flag")
187	  * [Title messages](Title_messages.md "Title messages")**** __(Desktop version)
188	  * [Tips](Tips.md "Tips")
189	  * [Resource Packs](Resource_Pack.md "Resource Pack")**** __(Desktop version)
190	  * [RGB](RGB.md "RGB")**** __(Desktop version)
191	  * [Workshop Hub](Workshop_Hub.md "Workshop Hub")**** __(Desktop version)
192	
193	Items
194	
195	  * [Alternative crafting ingredients](Alternative_crafting_ingredients.md "Alternative crafting ingredients")
196	  * [Ammo conversion](Ammo_conversion.md "Ammo conversion")
197	  * [Block Swap](Block_Swap.md "Block Swap")**** __(Desktop, Console and Mobile versions)
198	  * [Consumables](Consumables.md "Consumables")
199	  * [Crafting stations](Crafting_stations.md "Crafting stations")
200	    * [By Hand](By_Hand.md "By Hand")
201	  * [Crossover content](Crossover_content.md "Crossover content")
202	  * [Explosion-proof objects](Explosion-proof_objects.md "Explosion-proof objects")
203	  * [Flat-surface items](Flat-surface_items.md "Flat-surface items")
204	  * [Highlight](Highlight.md "Highlight")
205	  * [Mining speed](Mining_speed "Mining speed")
206	  * [Modifiers](Modifiers.md "Modifiers")
207	  * [NPC drops](NPC_drops.md "NPC drops")
208	  * [Placement](Placement.md "Placement")
209	  * [Pickaxe power](Pickaxe_power.md "Pickaxe power")
210	  * [Rarity](Rarity.md "Rarity")
211	  * [Recipes](Recipes.md "Recipes")
212	  * [Storage](Storage_items.md "Storage items")
213	  * [Tooltips](Tooltips.md "Tooltips")
214	  * [Use time](Use_time.md "Use time")
215	  * [Value](Value.md "Value")
216	
217	Game
218	
219	  * [Achievements](Achievements.md "Achievements")**** __(Desktop, Console, Old-gen console and Mobile versions)
220	  * [Difficulty](Difficulty.md "Difficulty")
221	    * [Journey](Journey_Mode.md "Journey Mode")**** __(Desktop, Console and Mobile versions)
222	    * [Classic](Classic_Mode.md "Classic Mode")
223	    * [Expert](Expert_Mode.md "Expert Mode")**** __(Desktop, Console and Mobile versions)
224	      * [Coin pickup](Coin_pickup_in_Expert_Mode.md "Coin pickup in Expert Mode")**** __(Desktop, Console and Mobile versions)
225	    * [Master](Master_Mode.md "Master Mode")**** __(Desktop, Console and Mobile versions)
226	  * [Fishing](Fishing.md "Fishing")
227	  * [Golf](Golf.md "Golf")**** __(Desktop, Console and Mobile versions)
228	  * [Hoik](Hoik.md "Hoik")
229	  * [Music](Music.md "Music")
230	  * [Teleportation](Teleportation.md "Teleportation")
231	    * [Pylons](Pylons.md "Pylons")**** __(Desktop, Console and Mobile versions)
232	  * [Town](Town.md "Town")**** __(Desktop, Console and Mobile versions)
233	
234	Multiplayer
235	
236	  * [Server](Server.md "Server")
237	  * [Chat](Chat.md "Chat")
238	  * [Multiplayer](Multiplayer.md "Multiplayer")
239	
240	Player
241	
242	  * [Aggro](Aggro.md "Aggro")
243	  * [Ammo conservation](Ammo_conservation.md "Ammo conservation")
244	  * [Breath meter](Breath_meter.md "Breath meter")
245	  * [Buffs](Buffs.md "Buffs")
246	    * [Debuffs](Debuffs.md "Debuffs")
247	  * [Character](Character.md "Character")
248	  * [Character styles](Character_styles.md "Character styles")**** __(Desktop, Console and Mobile versions)
249	  * [Damage reduction](Damage_reduction.md "Damage reduction")
250	  * [Dash](Dash.md "Dash")
251	  * [Death](Death.md "Death")
252	  * [Defense](Defense.md "Defense")
253	  * [Dodge](Dodge.md "Dodge")
254	  * [Drowning](Drowning.md "Drowning")
255	  * [Extra jump](Extra_jump.md "Extra jump")
256	  * [Fall damage](Fall_damage.md "Fall damage")
257	  * [Flight](Flight.md "Flight")
258	  * [Ghost](Ghost.md "Ghost")**** __(Desktop, Console, Old-gen console and Mobile versions)
259	  * [Hairstyles](Hairstyles.md "Hairstyles")
260	  * [Health](Health.md "Health")
261	  * [Health regeneration](Health_regeneration.md "Health regeneration")
262	  * [Inventory](Inventory.md "Inventory")
263	  * [Lifesteal](Lifesteal.md "Lifesteal")
264	  * [Loadouts](Loadouts.md "Loadouts")**** __(Desktop, Console and Mobile versions)
265	  * [Luck](Luck.md "Luck")**** __(Desktop, Console and Mobile versions)
266	  * [Mana](Mana.md "Mana")
267	  * [Movement speed](Movement_speed.md "Movement speed")
268	  * [Social slots](Social_slots.md "Social slots")
269	  * [Spawn](Spawn.md "Spawn")
270	  * [Stealth](Stealth.md "Stealth")
271	
272	Settings
273	
274	  * [Cursor modes](Cursor_modes.md "Cursor modes")
275	  * [Game controls](Game_controls.md "Game controls")
276	  * [Lighting mode](Lighting_mode.md "Lighting mode")**** __(Desktop, Console and Mobile versions)
277	  * [Parallax](Parallax.md "Parallax")**** __(Desktop, Console and Mobile versions)
278	  * [Settings](Settings.md "Settings")**** __(Desktop, Console, Mobile and 3DS versions)
279	  * [Toggles](Toggles.md "Toggles")
280	
281	Technical
282	
283	  * [AI](AI.md "AI")
284	  * [Chat commands](Commands.md "Commands")
285	  * [Command-line parameters](Command-line_parameters.md "Command-line parameters")**** __(Desktop version)
286	  * [Config.json](Config.json_settings.md "Config.json settings")**** __(Desktop and Mobile versions)
287	  * [Data IDs](Data_IDs.md "Data IDs")
288	  * [Debug commands](Debug_commands.md "Debug commands")**** __(Desktop version)
289	  * [Game platform](Game_platform.md "Game platform")
290	  * [NPC names](NPC_names.md "NPC names")
291	  * [Projectiles](Projectiles.md "Projectiles")
292	
293	World
294	
295	  * [Pre-Hardmode](Pre-Hardmode.md "Pre-Hardmode")
296	  * [Hardmode](Hardmode.md "Hardmode")
297	    * [Conversion](Hardmode_conversion.md "Hardmode conversion")
298	  * [Special world seeds](Special_world_seeds.md "Special world seeds")**** __(Desktop, Console and Mobile versions)
299	  * [Secret world seeds](Secret_world_seeds.md "Secret world seeds")**** __(Desktop, Console and Mobile versions)
300	  * [World](World.md "World")
301	    * [Generation](World_generation.md "World generation")
302	  * [World Seed](World_Seed.md "World Seed")**** __(Desktop, Console and Mobile versions)
303	  * [World size](World_size.md "World size")
304	
305	Categories: 
306	
307	  * [Exclusive content](Category%3AExclusive_content "Category:Exclusive content")
308	  * [Desktop content](Category%3ADesktop_content "Category:Desktop content")
309	  * [Console content](Category%3AConsole_content "Category:Console content")
310	  * [Mobile content](Category%3AMobile_content "Category:Mobile content")
311	  * [Pages with information based on outdated versions of Terraria's source code](Category%3APages_with_information_based_on_outdated_versions_of_Terraria's_source_code "Category:Pages with information based on outdated versions of Terraria's source code")
312	  * [Game mechanics](Category%3AGame_mechanics "Category:Game mechanics")
313	  * [Special world seeds](Category%3ASpecial_world_seeds "Category:Special world seeds")
314	
315	Hidden categories: 
316	
317	  * Pages using DynamicPageList3 dplvar parser function
318	  * Pages using DynamicPageList3 parser function
319	  * Entities patched in Desktop 1.4.5.4
320	  * Entities patched in Desktop 1.4.5.0
321	  * Entities patched in Desktop 1.4.4.6
322	  * Entities patched in Desktop 1.4.4
323	  * Entities introduced in Desktop 1.4.3
324	  * Pages with navboxes
325	  * Random
326	
327	This page is issued from [Terraria Wiki](https://terraria.wiki.gg/wiki/?title=The_Constant&oldid=998790 "Last edited on 2026-06-16"). The text is available under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-nc-sa/4.0) unless otherwise noted. Additional terms may apply for the media files. 
328	  *[1 required]: Journey Mode
329	  *[Qty.]: Quantity
330	  *[100%]: Expert Mode
331	  *[DPS]: Damage per second
332	  *[sic]: sīc erat scriptum (Latin: “thus it was written”) – any typographical or other errors in this quote are intentionally reproduced, exactly as they appear in the source.
333	  *[300]: Master Mode
334	  *[400]: Expert Mode
335	  *[160]: Expert Mode
336	  *[240]: Master Mode
337	  *[3 required]: Journey Mode
338	  *[#]: Number of summons, i.e. times that the Stardust Dragon Staff was used
339	  *[Max.  
340	enemies]: Maximum number of enemies Abigail can damage at once
341	  *[HM]: Hardmode
342	  *[**Click/tap here** to reveal this content. _(there may be a slight delay)_]: This content exists externally. Once you click, there may be a small delay while it is downloaded.
343	  *[**Klik/tap disini** untuk melihat isi konten. _(mungkin akan sedikit delay)_]: Konten ini tersedia secara eksternal. Ketika di klik, mungkin akan ada sedikit delay ketika melihat isi konten.
344	  *[**Bấm/Chạm vào đây** để hiển thị nội dung này. _(có thể sẽ bị delay một chút)_]: Nội dung này được lấy từ các nguồn bên ngoài. Khi bấm vào, có thể sẽ bị delay một chút trong khi nó tải.
345	  *[8]: Expert Mode
346	  *[10]: Expert Mode
347	  *[120]: Master Mode
348	  *[150]: Expert Mode
349	  *[13]: Chế độ Master
350	  *[195]: Master Mode
351	  *[Verify]: Talk:Tesla Turret (page does not exist)
352	  *[50 required]: Journey Mode
353	  *[0.05 mph]: 0.05 miles per hour (as measured by the Stopwatch item) or 0.04 tiles per second
354	  *[100 required]: Journey Mode
355	  *[cần có 1]: Chế độ Journey
356	  *[25 required]: Journey Mode
357	  *[cần có 25]: Chế độ Journey
358	  *[400 required]: Journey Mode
359	  *[membutuhkan 100]: Mode Journey
360	  *[cần có 100]: Chế độ Journey
361	  *[Slg.]: Số lượng
362	  *[1.99%]: Expert Mode
363	  *[199/10000 (1.99%)]: Expert Mode
364	  *[membutuhkan 1]: Mode Journey
365	  *[1,99%]: Expert Mode
366	  *[1/50 (2%)]: Mode Expert
367	  *[200 required]: Journey Mode
368	  *[15 mph]: 15 miles per hour (as measured by the Stopwatch item) or 11.25 tiles per second
369	  *[16 mph]: 16 miles per hour (as measured by the Stopwatch item) or 11.9390625 tiles per second
370	  *[20 required]: Journey Mode
371	  *[180]: Expert Mode
372	  *[270]: Master Mode
373	  *[5–9 seconds]: Master Mode
374	  *[5–9]: Expert Mode
375	  *[15 required]: Journey Mode
376	  *[Critter]: May spawn a Worm, Gold Worm, or Maggot when destroyed, as described at the top of this article
377	  *[Power]: Bait power
378	  *[5 required]: Journey Mode
379	  *[cần có {{{research}}}]: Chế độ Journey
380	  *[31 mph]: 31 miles per hour (as measured by the Stopwatch item) or 22.5 tiles per second
381	  *[34 mph]: 34 miles per hour (as measured by the Stopwatch item) or 24.93 tiles per second
382	  *[30 mph]: 30 miles per hour (as measured by the Stopwatch item) or 22 tiles per second
383	  *[Expert Mode exclusive]: Expert Mode
384	  *[402]: Master Mode
385	  *[523]: Expert Mode
386	  *[41 mph]: 41 miles per hour (as measured by the Stopwatch item) or 30.07 tiles per second
387	  *[21 mph]: 21 miles per hour (as measured by the Stopwatch item) or 15.4 tiles per second
388	  *[800]: Expert Mode
389	  *[1200]: Master Mode
390	  *[15]: Expert Mode
391	  *[17]: Master Mode
392	  *[O. v. odražení]: Odolnost vůči odražení
393	  *[1 minute 30 seconds]: Expert Mode
394	  *[1 minute 52.5 seconds]: Master Mode
395	  *[90]: Master Mode
396	  *[112.5]: Master Mode
397	  *[2–6]: Chế độ Expert
398	  *[2-6]: Expert Mode
399	  *[%100]: Expert Mode
400	  *[28]: Expert Mode
401	  *[42]: Master Mode
402	  *[80]: Expert Mode
403	  *[17 mph]: 17 miles per hour (as measured by the Stopwatch item) or 12.47 tiles per second
404	  *[ Minor improvements to all stats and increased life regeneration]: Expert Mode
405	  *[ Major improvements to all stats and increased life regeneration]: Expert Mode
406	  *[50%]: Expert Mode
407	  *[1/2 (50%)]: Expert Mode
408	  *[30]: Expert Mode
409	  *[45]: Expert Mode
410	  *[3/4]: Chế độ Expert
411	  *[5]: Master Mode
412	  *[75%]: Chế độ Expert
413	  *[semua]: Mode Master
414	  *[6]: Expert Mode
415	  *[toàn bộ]: Chế độ Master
416	  *[199/10000 (1,99%)]: Mode Expert
417	  *[4 minutes]: Expert Mode
418	  *[5 minutes]: Master Mode
419	  *[4]: Expert Mode
420	  *[36]: Expert Mode
421	  *[22]: Expert Mode
422	  *[26]: Master Mode
423	  *[Ruce pryč od mé zbraně, kámo!]: Keep your hands off my gun, buddy!
424	  *[Hej, tady nejsme ve filmu, kámo. Náboje něco stojí.]: Hey, this ain't a movie, pal. Ammo costs extra.
425	  *[Koukám, že házíš očkem po žraločkovi. Opravdu nechceš vědět, jak byl vyroben.]: I see you're eyeballing the Minishark. You really don't want to know how it was made.
426	  *[Neobtěžuj se s [jméno demoličního experta], vše, co potřebuješ, je přímo tady.]: Don't bother with [Name of Demolitionist], I've got all you need right here.
427	  *[Jaký má [jméno demoličního experta] problém? Uvědomuje si vůbec, že oba prodáváme naprosto rozdílné zboží?]: What's [Name of Demolitionist]'s problem? Does he even realize we sell completely different stuff?
428	  *[Pohni zadkem! Za hodinu mám rande s [jméno sestřičky].]: Make it quick! I've got a date with [Name of Nurse] in a hour.
429	  *[Chci to, co [jméno sestřičky] prodává. Co myslíš tím, že neprodává ani ň?]: I want what [Name of Nurse] is sellin'. What do you mean, she doesn't sell anything?
430	  *[Na [jméno dryády] bych mohl oči nechat. Škoda, že je to taková prudařka.]: [Name of Dryad] is a looker. Too bad she's such a prude.
431	  *[Slyšel jsem, že se ve světě nachází panenka vypadající skoro jako [jméno průvodce]. Mile rád bych do ní vpálil pár kulek.]: I heard there is a doll that looks very similar to [Name of Guide] somewhere in the underworld. I'd like to put a few rounds in it.
432	  *[Miluji noci jako je tahle. Vždy se najde něco na zabití.]: I love nights like tonight, there is never a shortage of things to kill.
433	  *[Chlape, tohle je noc přímo stvořená, abys s nikým nemusel mluvit, nemyslíš [jméno hráče]?]: Man, it's a good night not to talk to anybody, don't you think, [Name of Player]?
434	  *[14]: Expert Mode
435	  *[17.5]: Master Mode
436	  *[7]: Expert Mode
437	  *[8.75]: Master Mode
438	  *[21]: Expert Mode
439	  *[26.25]: Master Mode
440	  *[53 mph]: 53 miles per hour (as measured by the Stopwatch item) or 38.87 tiles per second
441	  *[88.6 mph]: 88.6 miles per hour (as measured by the Stopwatch item) or 64.97 tiles per second
442	  *[3.33–6.67%]: Expert Mode
443	  *[3.33%–6.67%]: Expert Mode
444	  *[W]: Wave
445	  *[3.33%]: Expert Mode
446	  *[6.67%]: Expert Mode
447	  *[0.014%]: Expert Mode
448	  *[ Medium improvements to all stats and increased life regeneration]: Expert Mode
449	  *[102 mph]: 102 miles per hour (as measured by the Stopwatch item) or 75 tiles per second
450	  *[+100%]: Expert Mode
451	  *[−50%]: Expert Mode
452	  *[+20%]: Expert Mode
453	  *[−16.67%]: Expert Mode
454	  *[200]: Expert Mode
455	  *[225]: Master Mode
456	  *[184 mph]: 184 miles per hour (as measured by the Stopwatch item) or 135 tiles per second
457	  *[72 mph]: 72 miles per hour (as measured by the Stopwatch item) or 52.5 tiles per second
458	  *[82 mph]: 82 miles per hour (as measured by the Stopwatch item) or 60.13 tiles per second
459	  *[6.25–12.5%]: Expert Mode
460	  *[51 mph]: 51 miles per hour (as measured by the Stopwatch item) or 37.4 tiles per second
461	  *[66 mph]: 66 miles per hour (as measured by the Stopwatch item) or 48.75 tiles per second
462	  *[77 mph]: 77 miles per hour (as measured by the Stopwatch item) or 56.47 tiles per second
463	  *[100 mph]: 100 miles per hour (as measured by the Stopwatch item) or 73.33 tiles per second
464	  *[6.25%]: Expert Mode
465	  *[12.5%]: Expert Mode
466	  *[32›140›176]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
467	  *[48›210›264]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
468	  *[26›92›116]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
469	  *[39›138›174]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
470	  *[2›8›10]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
471	  *[68›148›224]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
472	  *[102›222›336]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
473	  *[40›72›108]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
474	  *[60›108›162]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
475	  *[4›8›12]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
476	  *[92›100]: Expertní mód : Pre-hardmode › Těžký mód
477	  *[138›150]: Master Mode : Pre-Hardmode › Hardmode
478	  *[70›62]: Expertní mód : Pre-hardmode › Těžký mód
479	  *[105›93]: Master Mode : Pre-Hardmode › Hardmode
480	  *[60›132›198]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
481	  *[90›198›297]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
482	  *[36›64›96]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
483	  *[54›96›144]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
484	  *[6›12›18]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
485	  *[200›200›220]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
486	  *[300›300›330]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
487	  *[90›90›80]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
488	  *[135›135›120]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
489	  *[600]: Master Mode
490	  *[320]: Expert Mode
491	  *[480]: Master Mode
492	  *[100]: Expert Mode
493	  *[120›120›132]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
494	  *[180›180›198]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
495	  *[440]: Expert Mode
496	  *[660]: Master Mode
497	  *[1500]: Master Mode
498	  *[2250]: Master Mode
499	  *[2–6 seconds]: Expert Mode
500	  *[2.5–7.5 seconds]: Master Mode
501	  *[2.5–7.5]: Master Mode
502	  *[35 mph]: 35 miles per hour (as measured by the Stopwatch item) or 25.5 tiles per second
503	  *[43 mph]: 43 miles per hour (as measured by the Stopwatch item) or 31.5 tiles per second
504	  *[ 17–30]: Expert Mode
505	  *[99 required]: Journey Mode
506	  *[10–29]: Expert Mode
507	  *[1 time]: Expert Mode
508	  *[140]: Expert Mode
509	  *[210]: Master Mode
510	  *[14–20 seconds]: Expert Mode
511	  *[17.5-25 seconds]: Master Mode
512	  *[25%]: Master Mode
513	  *[14–20]: Expert Mode
514	  *[17.5–25]: Master Mode
515	  *[1/30 (3.33%)]: Expert Mode
516	  *[15.97%]: Expert Mode
517	  *[23/144 (15.97%)]: Expert Mode
518	  *[ 8 seconds]: Expert Mode
519	  *[10 seconds]: Master Mode
520	  *[0.5–2.5 seconds]: Master Mode
521	  *[90%]: Expert Mode
522	  *[Web Spit]: Expert Mode
523	  *[30 seconds]: Expert Mode
524	  *[37.5 seconds]: Master Mode
525	  *[4–12]: Expert Mode
526	  *[5–15]: Master Mode
527	  *[33.33%]: Expert Mode
528	  *[1/3 (33.33%)]: Expert Mode
529	  *[20-40]: Expert Mode
530	  *[25-40]: Expert Mode
531	  *[10-14]: Mode Expert
532	  *[12.5-17.5]: Master Mode
533	  *[20]: Expert Mode
534	  *[25]: Master Mode
535	  *[6-10]: Expert Mode
536	  *[7.5-12.5]: Master Mode
537	  *[1/1 (100%)]: Expert Mode
538	  *[6-20]: Expert Mode
539	  *[7.5-25]: Master Mode
540	  *[7.5-15]: Expert Mode
541	  *[9.37-18.75]: Master Mode
542	  *[11/243 (4.53%)]: Expert Mode
543	  *[11/81 (13.58%)]: Expert Mode
544	  *[2 hours]: Expert Mode
545	  *[3 hours]: Master Mode
546	  *[20–40]: Expert Mode
547	  *[25–50]: Master Mode
548	  *[61 mph]: 61 miles per hour (as measured by the Stopwatch item) or 45 tiles per second
549	  *[80 mph]: 80 miles per hour (as measured by the Stopwatch item) or 58.67 tiles per second
550	  *[64 mph]: 64 miles per hour (as measured by the Stopwatch item) or 46.93 tiles per second
551	  *[1/150]: Expert Mode
552	  *[1/30]: Expert Mode
553	  *[15.56–31.11%]: Expert Mode
554	  *[15.56%–31.11%]: Expert Mode
555	  *[15.56%]: Expert Mode
556	  *[31.11%]: Expert Mode
557	  *[ 12 _SC_ 50 _CC_]: Expert Mode
558	  *[dusk]: 7:30 PM
559	  *[1.33%]: Expert Mode
560	  *[1%]: Expert Mode
561	  *[4 mph]: 4 miles per hour (as measured by the Stopwatch item) or 3 tiles per second
562	  *[6 mph]: 6 miles per hour (as measured by the Stopwatch item) or 4.5 tiles per second
563	  *[10 mph]: 10 miles per hour (as measured by the Stopwatch item) or 7.5 tiles per second
564	  *[12 mph]: 12 miles per hour (as measured by the Stopwatch item) or 9 tiles per second
565	  *[20 seconds]: Expert Mode
566	  *[25 seconds]: Master Mode
567	  *[0.5%]: Expert Mode
568	  *[0.67%]: Expert Mode
569	  *[1-3]: エキスパートモード
570	  *[18 mph]: 18 miles per hour (as measured by the Stopwatch item) or 12.94 tiles per second
571	  *[Crit]: Critical strike chance
572	  *[20 mph]: 20 miles per hour (as measured by the Stopwatch item) or 14.67 tiles per second
573	  *[54 mph]: 54 miles per hour (as measured by the Stopwatch item) or 39.6 tiles per second
574	  *[and the core]: Expert Mode
575	  *[2,800]: Chế độ Expert
576	  *[3,570]: Chế độ Master
577	  *[3,640]: Chế độ Expert
578	  *[4,641]: Chế độ Master
579	  *[15,120]: Chế độ Expert
580	  *[19,296]: Chế độ Master
581	  *[2,125]: Chế độ Expert
582	  *[2,709]: Chế độ Master
583	  *[4,760]: Chế độ Expert
584	  *[6,069]: Chế độ Master
585	  *[11,900]: Mode Expert
586	  *[15,172]: Mode Master
587	  *[8,800]: Chế độ Expert
588	  *[11,220]: Master Mode
589	  *[11,200]: Chế độ Expert
590	  *[14,280]: Chế độ Master
591	  *[28,800]: Chế độ Expert
592	  *[36,720]: Chế độ Master
593	  *[30,000]: Chế độ Expert
594	  *[38,250]: Chế độ Master
595	  *[34,500]: Chế độ Expert
596	  *[43,988]: Chế độ Master
597	  *[120,000]: Chế độ Expert
598	  *[153,000]: Chế độ Master
599	  *[280]: Expert Mode
600	  *[420]: Master Mode
601	  *[42,000]: Chế độ Expert
602	  *[53,550]: Chế độ Master
603	  *[88,500]: Chế độ Expert
604	  *[112,836]: Chế độ Master
605	  *[90,000]: Chế độ Expert
606	  *[114,749]: Chế độ Master
607	  *[78,000]: Expert Mode
608	  *[99,450]: Chế độ Master
609	  *[11700]: Mode Expert
610	  *[14917]: Mode Master
611	  *[98,000]: Chế độ Expert
612	  *[124,950]: Chế độ Master
613	  *[48,000]: Chế độ Expert
614	  *[61,200]: Master Mode
615	  *[217,500]: Expert Mode
616	  *[277,311]: Chế độ Master
617	  *[dua]: Mode Expert
618	  *[10,500]: Mode Expert
619	  *[24 detik]: Mode Expert
620	  *[30 detik]: Mode Expert
621	  *[30 required]: Journey Mode
622	  *[mph]: miles per hour
623	  *[70]: Expert Mode
624	  *[36 mph]: 36 miles per hour (as measured by the Stopwatch item) or 26.4 tiles per second
625	  *[315]: Expert Mode
626	  *[68]: Expert Mode
627	  *[0.5]: Expert Mode
628	  *[96]: Expert Mode
629	  *[144]: Expert Mode
630	  *[12.5]: Master Mode
631	  *[143 mph]: 143 miles per hour (as measured by the Stopwatch item) or 105 tiles per second
632	  *[5525]: Expert Mode
633	  *[7049]: Master Mode
634	  *[60%]: Expert Mode
635	  *[64%]: Expert Mode
636	  *[65%]: Master Mode
637	  *[110–135]: Master Mode
638	  *[30–50]: Master Mode
639	  *[5.23–10.5 sec]: Expert Mode
640	  *[6.53–13.12 sec]: Master Mode
641	  *[3–6 sec]: Expert Mode
642	  *[3.75–7.5 sec]: Master Mode
643	  *[0.73–1.5 sec]: Expert Mode
644	  *[0.92–1.87 sec]: Master Mode
645	  *[7.5–15 sec]: Expert Mode
646	  *[9.37–18.75 sec]: Master Mode
647	  *[1.5–3 sec]: Expert Mode
648	  *[1.87–3.75 sec]: Master Mode
649	  *[11.23–22.5 sec]: Expert Mode
650	  *[14.03–28.12 sec]: Master Mode
651	  *[9.73–19.5 sec]: Expert Mode
652	  *[12.17–24.37 sec]: Master Mode
653	  *[ 60%]: Mode Expert
654	  *[ 25%]: Chế độ Master
655	  *[ 100%]: Expert Mode
656	  *[5700-7700]: Expert Mode
657	  *[ %100]: Master Mode
658	  *[0-200]: Chế độ Expert
659	  *[0-500]: Chế độ Expert
660	  *[2125]: Expert Mode
661	  *[170]: Expert Mode
662	  *[2709]: Master Mode
663	  *[217]: Chế độ Master
664	  *[20%]: Expert Mode
665	  *[1/5 (20%)]: Expert Mode
666	  *[9.73-19.5]: Expert Mode
667	  *[12.17-24.37]: Master Mode
668	  *[2]: Expert Mode
669	  *[3]: Master Mode
670	  *[43.75%]: Expert Mode
671	  *[7/16 (43.75%)]: Expert Mode
672	  *[Third]: Expert Mode
673	  *[Major improvements to all stats and increased life regeneration]: 達人模式
674	  *[Medium improvements to all stats and increased life regeneration]: 達人模式
675	  *[Minor improvements to all stats and increased life regeneration]: 達人模式
676	  *[13 seconds]: Master Mode
677	  *[Zabíjení zajíčků je bezcitné. Tečka.]: Killing bunnies is cruel. Period.
678	  *[14 seconds]: Expert Mode
679	  *[17.5 seconds]: Master Mode
680	  *[26 mph]: 26 miles per hour (as measured by the Stopwatch item) or 18.75 tiles per second
681	  *[189]: Expert Mode
682	  *[283]: Master Mode
683	  *[4.94%]: Expert Mode
684	  *[3.96%]: Expert Mode
685	  *[700]: Expert Mode
686	  *[1,050]: Master Mode
687	  *[23 mph]: 23 miles per hour (as measured by the Stopwatch item) or 16.87 tiles per second
688	  *[2 mph]: 2 miles per hour (as measured by the Stopwatch item) or 1.6875 tiles per second
689	  *[79/1600 (4.94%)]: Expert Mode
690	  *[4,94%]: Expert Mode
691	  *[3/80 (3,75%)]: Mode Expert
692	  *[12.5 seconds]: Master Mode
693	  *[2 required]: Journey Mode
694	  *[24–100]: Expert Mode
695	  *[12–20]: Expert Mode
696	  *[360]: Master Mode
697	  *[[]: Western world border
698	  *[C]: World center
699	  *[]]: Eastern world border
700	  *[60]: Master Mode
701	  *[18–30]: Expert Mode
702	  *[18–90]: Expert Mode
703	  *[115 mph]: 115 miles per hour (as measured by the Stopwatch item) or 84.33 tiles per second
704	  *[382 mph]: 382 miles per hour (as measured by the Stopwatch item) or 280.13 tiles per second
705	  *[721 mph]: 721 miles per hour (as measured by the Stopwatch item) or 528.73 tiles per second
706	  *[12.5–50%]: Expert Mode
707	  *[12.5%–50%]: Expert Mode
708	  *[16.67%]: Expert Mode
709	  *[0.25%]: Expert Mode
710	  *[0.26 mph]: 0.26 miles per hour (as measured by the Stopwatch item)
711	  *[40]: Expert Mode
712	  *[50]: Master Mode
713	  *[37.5]: Master Mode
714	  *[62.5]: Master Mode
715	  *[6.25]: Master Mode
716	  *[46 mph]: 46 miles per hour (as measured by the Stopwatch item) or 33.73 tiles per second
717	  *[membutuhkan 25]: Mode Journey
718	  *[6.22–31.11%]: Expert Mode
719	  *[6.22%–31.11%]: Expert Mode
720	  *[6.22%]: Expert Mode
721	  *[7.78%]: Expert Mode
722	  *[10.37%]: Expert Mode
723	  *[6,22–31,11%]: Expert Mode
724	  *[102]: Master Mode
725	  *[ 4–6 seconds]: Expert Mode
726	  *[5–7.5 seconds]: Master Mode
727	  *[7.5]: Master Mode
728	  *[16]: Expert Mode
729	  *[24]: Expert Mode
730	  *[12 _GC_ 50 _SC_]: Expert Mode
731	  *[8 _GC_]: Expert Mode
732	  *[10 _GC_]: Master Mode
733	  *[tida perempat]: Mode Expert
734	  *[ Verifikasi]: Talk:Coins/id (halaman belum tersedia)
735	  *[Verifikasi]: in Xbox and Mobile
736	  *[ Verify]: Talk:Coins/vi (page does not exist)
737	  *[92 mph]: 92 miles per hour (as measured by the Stopwatch item) or 67.5 tiles per second
738	  *[1.5–3]: Expert Mode
739	  *[1.87–3.75]: Master Mode
740	  *[2/243 (0.82%)]: Expert Mode
741	  *[2/81 (2.47%)]: Expert Mode
742	  *[35]: Master Mode
743	  *[1.8–3]: Expert Mode
744	  *[2.25–3.75]: Master Mode
745	  *[1/6 (16.67%)]: Expert Mode
746	  *[Radius]: Explosion radius in tiles
747	  *[13 mph]: 13 miles per hour (as measured by the Stopwatch item) or 9.375 tiles per second
748	  *[7.76%]: Expert Mode
749	  *[2%]: Expertní mód
750	  *[10 minutes]: Expert Mode
751	  *[12 minutes 30 seconds]: Master Mode
752	  *[105›93›187]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
753	  *[157›140›281]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
754	  *[1–3]: Expert Mode
755	  *[1–2]: Expert Mode
756	  *[5–7]: Expert Mode
757	  *[2–4]: Master Mode
758	  *[1/4 (25%)]: Expert Mode
759	  *[8 seconds]: Expert Mode
760	  *[67%]: Expert Mode
761	  *[two pieces]: Expert Mode
762	  *[dua bagian]: Mode Expert
763	  *[2-10]: Expert Mode
764	  *[2-12]: Master Mode
765	  *[0.73–1.5]: Expert Mode
766	  *[0.92–1.87]: Master Mode
767	  *[0.9–1.13]: Expert Mode
768	  *[1.5–1.88]: Master Mode
769	  *[1/6 (16.7%)]: Expert Mode
770	  *[4-6]: Expert Mode
771	  *[5-7.5]: Master Mode
772	  *[48-72]: Expert Mode
773	  *[60-90]: Master Mode
774	  *[168]: Master Mode
775	  *[5–20%]: Expert Mode
776	  *[5%]: Expert Mode
777	  *[10%]: Expert Mode
778	  *[1]: Base value
779	  *[0.14]: Turtle armor
780	  *[0.2]: 5 Menacing modifiers
781	  *[0.15]: Shroomite bonus
782	  *[0.12]: Avenger Emblem
783	  *[0.1]: Quiver bonus
784	  *[0.05]: Well Fed
785	  *[230]: Godly Meowmere
786	  *[1.98]: Melee damage multiplier
787	  *[0.13]: Shroomite armor
788	  *[0.6]: Shroomite armor stealth effect
789	  *[0.16]: 4 Menacing modifiers
790	  *[39]: Godly Chlorophyte Shotbow
791	  *[2.26]: Ranged damage multiplier
792	  *[1.15]: Shroomite bonus
793	  *[1.1]: Archery buff
794	  *[105]: Master Mode
795	  *[11]: Ammo damage
796	  *[3–6]: Expert Mode
797	  *[3.75–7.5]: Master Mode
798	  *[3.6–6]: Expert Mode
799	  *[4.5–7.5]: Master Mode
800	  *[6.56%]: Expert Mode
801	  *[59/900 (6.56%)]: Expert Mode
802	  *[15 seconds]: Master Mode
803	  *[1 minute]: Expert Mode
804	  *[three-quarters]: Expert Mode
805	  *[all]: Master Mode
806	  *[a [Jellyfish](Jellyfish.md "Jellyfish")'s shock attack]: Expert Mode
807	  *[30 _CC_]: Expert Mode
808	  *[ 4.94%]: Expert Mode
809	  *[1 _SC_ 50 _CC_]: Expert Mode
810	  *[6 _GC_]: Expert Mode
811	  *[6–90 seconds]: Expert Mode
812	  *[7.5–112.5 seconds]: Master Mode
813	  *[2–40 seconds]: Expert Mode
814	  *[2.5–50 seconds]: Master Mode
815	  *[1–30 seconds]: Expert Mode
816	  *[1.25–37.5 seconds]: Master Mode
817	  *[4–14 seconds]: Expert Mode
818	  *[5–17.5 seconds]: Master Mode
819	  *[12 seconds]: Expert Mode
820	  *[14–30 seconds]: Expert Mode
821	  *[17.5–37.5 seconds]: Master Mode
822	  *[4–20 seconds]: Expert Mode
823	  *[5–25 seconds]: Master Mode
824	  *[1.5–28 seconds]: Expert Mode
825	  *[1.87–35 seconds]: Master Mode
826	  *[3–30 seconds]: Expert Mode
827	  *[3.75–37.5 seconds]: Master Mode
828	  *[4–12 seconds]: Expert Mode
829	  *[5–15 seconds]: Master Mode
830	  *[1.5–14 seconds]: Expert Mode
831	  *[1.87–17.5 seconds]: Master Mode
832	  *[0.73–8 seconds]: Expert Mode
833	  *[0.92–10 seconds]: Master Mode
834	  *[10–90 seconds]: Expert Mode
835	  *[12.5–112.5 seconds]: Master Mode
836	  *[0.5–32 seconds]: Expert Mode
837	  *[0.63–40 seconds]: Master Mode
838	  *[5 mph]: 5 miles per hour (as measured by the Stopwatch item) or 3.75 tiles per second
839	  *[0.67–4 seconds]: Expert Mode
840	  *[0.83–5 seconds]: Master Mode
841	  *[1–4 seconds]: Expert Mode
842	  *[4–8 seconds]: Expert Mode
843	  *[5 seconds]: Master Mode
844	  *[11.23–600 seconds]: Expert Mode
845	  *[14.03–750 seconds]: Master Mode
846	  *[3–90 seconds]: Master Mode
847	  *[16 seconds]: Expert Mode
848	  *[ 6]: Expert Mode
849	  *[ 18]: Expert Mode
850	  *[ 6-90 detik]: Mode Expert
851	  *[2-20 detik]: Mode Expert
852	  *[14-20 detik]: Mode Expert
853	  *[16 detik]: Mode Expert
854	  *[5-30 detik]: Mode Expert
855	  *[6 detik]: Mode Expert
856	  *[2.5-14 detik]: Mode Expert
857	  *[1.25-8 detik]: Mode Expert
858	  *[0.5-32 detik]: Mode Expert
859	  *[18.75 detik - 10 menit]: Mode Expert
860	  *[16.25 detik - 4 menit]: Mode Expert
861	  *[10 detik]: Mode Expert
862	  *[14-16 detik]: Mode Expert
863	  *[20 detik-90 detik]: Mode Expert
864	  *[2-3 detik]: Mode Expert
865	  *[ 1 detik]: Mode Expert
866	  *[5-9 detik]: Mode Expert
867	  *[3-90 detik]: Mode Expert
868	  *[16 detik]: Mode Expert
869	  *[52]: Expert Mode
870	  *[78]: Master Mode
871	  *[72]: Expert Mode
872	  *[108]: Expert Mode
873	  *[24 seconds]: Expert Mode
874	  *[0.67 seconds]: Expert Mode
875	  *[0.83 seconds]: Master Mode
876	  *[midnight]: 12:00 AM
877	  *[five]: Expert Mode
878	  *[0.67]: Expert Mode
879	  *[0.83]: Master Mode
880	  *[14000]: Expert Mode
881	  *[21000]: Master Mode
882	  *[11900]: Expert Mode
883	  *[15172]: Master Mode
884	  *[0.75]: Expert Mode
885	  *[Atk.  
886	dmg]: Attack damage
887	  *[Def.]: Defense
888	  *[AP]: Armor penetration
889	  *[77]: Master Mode
890	  *[81]: Master Mode
891	  *[27]: Expert Mode
892	  *[31]: Master Mode
893	  *[208]: Master Mode
894	  *[69]: Expert Mode
895	  *[Dynamit. Můj speciální lík na všechno, co tě trápí.]: Dynamite, my own special cure-all for what ails ya.
896	  *[Výbušniny v dnešní době letí. Kup je ještě teď!]: Explosives are da' bomb these days. Buy some now!
897	  *[Proč očisťovat svět, když jej můžeš vyhodit do povětří?]: Why purify the world when you can just blow it up?
898	  *[Dnes se bude dobře umírat!]: It's a good day to die!
899	  *[Jsem si docela jistý, že ti [jméno sestřičky] pomůže přišít zpět všechny tvé končetiny.]: 
900	  *[Zajímalo by mě, co se stane, pokud… (BUM!)… Oh, omlouvám se, potřeboval jsi tu nohu?]: I wonder what happens if I... (BOOM!)... Oh, sorry, did you need that leg?
901	  *[Dokonce i [jméno prodejce zbraní] by chtěl to, co já prodávám!]: Even [Name of Arms Dealer] wants what I'm selling!
902	  *[Byl bys radši s dírou po kulce, nebo dírou po granátu? Myslel jsem si to.]: Would you rather have a bullet hole or a grenade hole? That's what I thought.
903	  *[Koukni na mé zboží; mají výbušné ceny!]: Check out my goods; they have explosive prices!
904	  *[ZÁKAZ KOUŘENÍ!]: NO SMOKING IN HERE!!
905	  *[Pokud hodíš tenhle do vany a zavřeš všechna okna, pročistí to všechny tvé dutiny a urve uši!]: If you throw this one in the bathtub and close all the windows, it'll clear your sinuses and pop your ears!
906	  *[Chceš si hrát na kuře Pojistku?]: Wanna play Fuse Chicken?
907	  *[Podepsal bys mi tento griefovací dokument?]: Hey, could you sign this Griefing Waiver?
908	  *[Něco jsem si od těch zombie odnesl!]: I've got something for them zombies alright!
909	  *[Hej, neviděl jsi někde klauna?]: Hey, have you seen a clown around?
910	  *[Ještě před chvílí tady seděla bomba, teď ji nemůžu najít…]: There was a bomb sitting right here, and now I can't seem to find it...
911	  *[84]: Expert Mode
912	  *[126]: Master Mode
913	  *[30 seconds]: Expertní mód
914	  *[60 mph]: 60 miles per hour (as measured by the Stopwatch item) or 44 tiles per second
915	  *[33,33%]: Master Mode
916	  *[88]: Expert Mode
917	  *[132]: Master Mode
918	  *[Contact]: The damage without modifier and summon damage bonuses
919	  *[Pounce]: The damage without modifier and summon damage bonuses
920	  *[Threshold]: If the player's summon damage bonuses reach it, Ruthless will become the best modifier
921	  *[N/A]: Not available in vanilla game
922	  *[16−30 seconds]: Expert Mode
923	  *[20−37.5 seconds]: Master Mode
924	  *[ 9.75%]: Expert Mode
925	  *[16–30]: Expert Mode
926	  *[20–37.5]: Master Mode
927	  *[128]: Expert Mode
928	  *[192]: Master Mode
929	  *[15–60]: Expert Mode
930	  *[0.5×]: Journey Mode
931	  *[2×]: Expert Mode
932	  *[3×]: Master Mode
933	  *[4×]: Expert Mode
934	  *[5.33×]: Legendary Mode
935	  *[2.5×]: Master Mode
936	  *[3.5×]: Legendary Mode
937	  *[0.9×]: Expert Mode
938	  *[0.8×]: Master Mode
939	  *[1.5×]: Expert Mode
940	  *[1.75×]: Master Mode
941	  *[May increase both during [Hardmode](Hardmode.md "Hardmode") and [Post-Plantera](Post-Plantera.md "Post-Plantera")]: Expert Mode
942	  *[May increase]: Expert Mode
943	  *[15 / 30]: Expert Mode
944	  *[ 4%]: Expert Mode
945	  *[+15]: Expert Mode
946	  *[+20]: Master Mode
947	  *[ 16]: Expert Mode
948	  *[18]: Master Mode
949	  *[Opatruj se! Terraria tě potřebuje!]: Be safe; Terraria needs you!
950	  *[Musíš očistit svět od této nákazy.]: You must cleanse the world of this corruption.
951	  *[Musíš očistit svět od tohoto karmínu.]: You must cleanse the world of this crimson.
952	  *[Písky času se přesýpají. A upřímně, nemládneš a nekrásníš.]: The sands of time are flowing. And well, you are not aging very gracefully.
953	  *[Co je to s tím, že více ‚štěkám‘ než koušu?]: What's this about me having more 'bark' than bite?
954	  *[Dva goblini tahle přijdou do baru a jeden říká tomu druhému: ‚Dáš si goblet piva?!‘]: So two goblins walk into a bar, and one says to the other, 'Want to get a Goblet of beer?!'
955	  *[Proč se mi [Jméno obchodníka] snaží prodat sochy andělů? Všichni přeci ví, že nic nedělají.]: Why does [Name of Merchant] keep trying to sell me an angel statues? Everyone knows that they don't do anything.
956	  *[Kéž by se mnou [jméno prodejce zbraní] přestal flirtovat. Copak si neuvědomuje, že jsem více než 500 let stará?]: I wish [Name of Arms Dealer] would stop flirting with me. Doesn't he realize I'm 500 years old?
957	  *[Už jsi v nákaze zkoušel použít očistný prášek na ebenokámen?]: Have you tried using purification powder on the ebonstone of The Corruption?
958	  *[Už jsi v karmínu zkoušel použít očistný prášek na karmínokámen?]: Have you tried using purification powder on the Crimstone of the Crimson?
959	  *[Viděl jsi starce procházejícího se kolem podzemní kobky? Vůbec nevypadá dobře…]: Have you seen the old man walking around the dungeon? He doesn't look well at all...
960	  *[Myslím si, že je [jméno lanýže] nepochopený ostatními. Je to velmi vtipný chlapík.]: I feel like [Name of Truffle] is a bit misunderstood, he really is a fun guy.
961	  *[Prodávám co se mi zlíbí! Pokud se ti to nelíbí, tak máš smůlu.]: I sell what I want! If you don't like it, too bad.
962	  *[Kámo, je to mnou, nebo je venku tak milion zombie?]: Dude, is it just me or are there a million [[zombies]] out tonight?
963	  *[Nechci aby sis kupoval mé věci. Já chci abys chtěl si mé věci kupovat, jasné?]: I don't want you to buy my stuff. I want you to want to buy my stuff, ok?
964	  *[Proč musíš být ve chvílích jako je tato tak konfrontační?]: Why do you have to be so confrontational during a time like this?
965	  *[[jméno světa] je z [procenta posvátnosti] % posvátný a [procenta nákazy/karmínu] % [nakažen/karmínový]. [Dryádin komentář (viz výše)].]: [Name of world] is [hallow percentage]% hallow and [crimson/corruption percentage]% [crimson/corruption]. [Dryad's comment, see above].
966	  *[[jméno světa] je kompletně očištěn. Odvedl jsi úžasnou práci!]: [Name of World] is completely pure. You have done an amazing job!
967	  *[+10]: Expert Mode
968	  *[+14]: Master Mode
969	  *[6–20 seconds]: Expert Mode
970	  *[7.5–25 seconds]: Master Mode
971	  *[3–10 seconds]: Expert Mode
972	  *[201]: Expert Mode
973	  *[302]: Expert Mode
974	  *[184]: Expert Mode
975	  *[277]: Master Mode
976	  *[39000/78000]: Expert Mode
977	  *[49725/99450]: Master Mode
978	  *[0]: Expert Mode
979	  *[39,000]: Expert Mode
980	  *[49,725]: Master Mode
981	  *[11,700]: Expert Mode
982	  *[14,917]: Master Mode
983	  *[60,000]: Expert Mode
984	  *[76,500]: Master Mode
985	  *[99,000]: Master Mode
986	  *[ 78000]: Expert Mode
987	  *[99450]: Master Mode
988	  *[ ]: Master Mode
989	  *[ 62 _GC_ 50 _SC_]: Expert Mode
990	  *[ 2 _GC_ 50 _SC_]: Mode Expert
991	  *[39000]: Mode Expert
992	  *[49725]: Mode Master
993	  *[double]: Expert Mode
994	  *[triple]: Master Mode
995	  *[1/9 (11.11%)]: Expert Mode
996	  *[1/8 (12.5%)]: Expert Mode
997	  *[19]: Master Mode
998	  *[15120]: Expert Mode
999	  *[19296]: Master Mode
1000	  *[356]: Mode Expert
1001	  *[209]: Mode Expert
1002	  *[139.33 yards (152.38 m)]: Expert Mode
1003	  *[10479]: Expert Mode
1004	  *[1/20 (5%)]: Expert Mode
1005	  *[10 minutes]: Expert Mode
1006	  *[100-150]: Expert Mode
1007	  *[2-3]: Chế độ Expert
1008	  *[ 15120]: Chế độ Expert
1009	  *[ 19296]: Chế độ Master
1010	  *[ 10500]: Chế độ Expert
1011	  *[10 menit]: Mode Expert
1012	  *[12 menit 30 detik]: Mode Master
1013	  *[2–3]: Chế độ Expert
1014	  *[1/20 (%5)]: Expert Mode
1015	  *[10 phút]: Chế độ Expert
1016	  *[12 phút 30 giây]: Chế độ Master
1017	  *[10500]: Expert Mode
1018	  *[Total damage]: Stationary / Moving
1019	  *[110]: Expert Mode
1020	  *[248]: Master Mode
1021	  *[165]: Expert Mode
1022	  *[372]: Master Mode
1023	  *[49000/98000]: Expert Mode
1024	  *[62475/124950]: Master Mode
1025	  *[12]: Expert Mode
1026	  *[Ethereal Lance 3]: Expert Mode
1027	  *[49,000]: Expert Mode
1028	  *[62,475]: Master Mode
1029	  *[59,994]: Master Mode
1030	  *[39,996]: Expert Mode
1031	  *[24 mph]: 24 miles per hour (as measured by the Stopwatch item) or 17.6 tiles per second
1032	  *[33 mph]: 33 miles per hour (as measured by the Stopwatch item) or 24.2 tiles per second
1033	  *[2000]: Expert Mode
1034	  *[3000]: Master Mode
1035	  *[6000]: Expert Mode
1036	  *[9000]: Master Mode
1037	  *[10000]: Expert Mode
1038	  *[15000]: Master Mode
1039	  *[48›86]: Expert Mode : Pre-Hardmode › Hardmode
1040	  *[72›129]: Master Mode : Pre-Hardmode › Hardmode
1041	  *[124]: Expert Mode
1042	  *[186]: Master Mode
1043	  *[37%]: Expert Mode
1044	  *[44%]: Master Mode
1045	  *[55%]: Expert Mode
1046	  *[82%]: Expert Mode
1047	  *[84%]: Master Mode
1048	  *[172]: Expert Mode
1049	  *[258]: Master Mode
1050	  *[228]: Expert Mode
1051	  *[342]: Master Mode
1052	  *[1.33–6.67%]: Expert Mode
1053	  *[27.27–60%]: Expert Mode
1054	  *[5–25%]: Master Mode
1055	  *[20–100%]: Master Mode
1056	  *[125]: Master Mode
1057	  *[9/25 (36%)]: Expert Mode
1058	  *[9/25]: Expert Mode
1059	  *[1050]: Master Mode
1060	  *[1/10 (10%)]: Expert Mode
1061	  *[54]: Master Mode
1062	  *[2366/3640]: Expert Mode
1063	  *[3016/4641]: Master Mode
1064	  *[−15]: Expert Mode
1065	  *[−30]: Expert Mode
1066	  *[Chain charge]: Expert Mode
1067	  *[2,366]: Chế độ Expert
1068	  *[3,016]: Mode Master
1069	  *[436]: Expert Mode
1070	  *[556]: Master Mode
1071	  *[145]: Expert Mode
1072	  *[185]: Master Mode
1073	  *[7 _GC_ 50 _SC_]: Expert Mode
1074	  *[36  
1075	40 when below 145 health]: Expert Mode
1076	  *[54  
1077	60 when below 185 health]: Master Mode
1078	  *[2365/3640]: Chế độ Expert
1079	  *[ 7 _GC_ 50 _SC_]: Chế độ Expert
1080	  *[ %25]: Master Mode
1081	  *[36  
1082	40 khi dưới 145 máu]: Chế độ Expert
1083	  *[54  
1084	60 khi dưới 185 máu]: Chế độ Master
1085	  *[3017/4641]: Chế độ Master
1086	  *[Liên hoàn lướt]: Chế độ Expert
1087	  *[4641]: Chế độ Master
1088	  *[3016]: Chế độ Master
1089	  *[1,000]: Expert Mode
1090	  *[1,500]: Master Mode
1091	  *[8 mph]: 8 miles per hour (as measured by the Stopwatch item) or 5.625 tiles per second
1092	  *[19 mph]: 19 miles per hour (as measured by the Stopwatch item) or 14.0625 tiles per second
1093	  *[4.2–7]: Expert Mode
1094	  *[5.25–8.75]: Master Mode
1095	  *[6–10]: Expert Mode
1096	  *[7.5–12.5]: Master Mode
1097	  *[1.2–2]: Expert Mode
1098	  *[1.5–2.5]: Master Mode
1099	  *[FP]: Fishing Power
1100	  *[cần có 5]: Chế độ Journey
1101	  *[cần có 3]: Chế độ Journey
1102	  *[membutuhkan 99]: Mode Journey
1103	  *[22 mph]: 22 miles per hour (as measured by the Stopwatch item) or 15.8371875 tiles per second
1104	  *[113 mph]: 113 miles per hour (as measured by the Stopwatch item) or 82.5 tiles per second
1105	  *[116 mph]: 116 miles per hour (as measured by the Stopwatch item) or 85.07 tiles per second
1106	  *[13600]: Expert Mode
1107	  *[20400]: Master Mode
1108	  *[32 mph]: 32 miles per hour (as measured by the Stopwatch item) or 23.63343375 tiles per second
1109	  *[81 mph]: 81 miles per hour (as measured by the Stopwatch item) or 59.4 tiles per second
1110	  *[71 mph]: 71 miles per hour (as measured by the Stopwatch item) or 52.07 tiles per second
1111	  *[14 mph]: 14 miles per hour (as measured by the Stopwatch item) or 10.546875 tiles per second
1112	  *[28 mph]: 28 miles per hour (as measured by the Stopwatch item) or 20.53 tiles per second
1113	  *[37 mph]: 37 miles per hour (as measured by the Stopwatch item) or 27 tiles per second
1114	  *[42 mph]: 42 miles per hour (as measured by the Stopwatch item) or 30.8 tiles per second
1115	  *[48 mph]: 48 miles per hour (as measured by the Stopwatch item) or 35.2 tiles per second
1116	  *[49 mph]: 49 miles per hour (as measured by the Stopwatch item) or 36 tiles per second
1117	  *[56 mph]: 56 miles per hour (as measured by the Stopwatch item) or 41.25 tiles per second
1118	  *[47 mph]: 47 miles per hour (as measured by the Stopwatch item) or 34.47 tiles per second
1119	  *[7.7 mph]: 7.7 miles per hour (as measured by the Stopwatch item) or 5.65 tiles per second
1120	  *[63 mph]: 63 miles per hour (as measured by the Stopwatch item) or 45.9375 tiles per second
1121	  *[2.5]: Master Mode
1122	  *[250]: Master Mode
1123	  *[375]: Master Mode
1124	  *[100% by wave 14]: Expert Mode
1125	  *[3/11 (27.27%)]: Expert Mode
1126	  *[3/8 (37.5%)]: Expert Mode
1127	  *[3/5 (60%)]: Expert Mode
1128	  *[Base]: Base drop rate without the factor
1129	  *[1.67%]: Expert Mode
1130	  *[2.22%]: Expert Mode
1131	  *[8.33%]: Master Mode
1132	  *[27.27%]: Expert Mode
1133	  *[37.5%]: Expert Mode
1134	  *[6-12]: Expert Mode
1135	  *[7-15]: Master Mode
1136	  *[48-96]: Expert Mode
1137	  *[56-120]: Master Mode
1138	  *[3.75]: Master Mode
1139	  *[13/125 (10.4%)]: Expert Mode
1140	  *[39/400 (9.75%)]: Expert Mode
1141	  *[69/1225 (5.63%)]: Expert Mode
1142	  *[1–4]: Expert Mode
1143	  *[1.25–5]: Master Mode
1144	  *[0.67–2]: Expert Mode
1145	  *[0.83–2.5]: Master Mode
1146	  *[12.5–25%]: Master Mode
1147	  *[(Expert Mode exclusive)]: Expertní mód
1148	  *[40 mph]: 40 miles per hour (as measured by the Stopwatch item) or 29.33 tiles per second
1149	  *[1 minute 38 seconds]: Expert Mode
1150	  *[2 minutes 3 seconds]: Master Mode
1151	  *[Ukořisti drahokam]: Capture the Gem
1152	  *[membutuhkan 15]: Mode Journey
1153	  *[cần có 15]: Chế độ Journey
1154	  *[membutuhkan 5]: Mode Journey
1155	  *[28 seconds]: Expert Mode
1156	  *[35 seconds]: Master Mode
1157	  *[30–90 seconds]: Expert Mode
1158	  *[7.84%]: Expert Mode
1159	  *[7,84%]: Mode Expert
1160	  *[43]: Expert Mode
1161	  *[64]: Expert Mode
1162	  *[288]: Expert Mode
1163	  *[432]: Master Mode
1164	  *[4%]: Expert Mode
1165	  *[44]: Chế độ Expert
1166	  *[66]: Chế độ Master
1167	  *[33.3%]: Expert Mode
1168	  *[10 required]: Journey Mode
1169	  *[90000]: Expert Mode
1170	  *[114749]: Master Mode
1171	  *[37500]: Expert Mode
1172	  *[47812]: Master Mode
1173	  *[22500]: Expert Mode
1174	  *[28687]: Master Mode
1175	  *[19125]: Master Mode
1176	  *[10–14 seconds]: Expert Mode
1177	  *[15–21 seconds]: Master Mode
1178	  *[10–14]: Expert Mode
1179	  *[15–21]: Master Mode
1180	  *[18,750]: Expert Mode
1181	  *[23,906]: Master Mode
1182	  *[58 mph]: 58 miles per hour (as measured by the Stopwatch item) or 42.75 tiles per second
1183	  *[104]: Expert Mode
1184	  *[156]: Master Mode
1185	  *[59 mph]: 59 miles per hour (as measured by the Stopwatch item) or 43.125 tiles per second
1186	  *[162]: Master Mode
1187	  *[112]: Expert Mode
1188	  *[116]: Expert Mode
1189	  *[174]: Master Mode
1190	  *[96–116]: Expert Mode
1191	  *[144–174]: Master Mode
1192	  *[15,000]: Expert Mode
1193	  *[19,124]: Master Mode
1194	  *[7,500]: Expert Mode
1195	  *[9,562]: Master Mode
1196	  *[18,000]: Expert Mode
1197	  *[22,949]: Master Mode
1198	  *[13,500]: Expert Mode
1199	  *[17,212]: Master Mode
1200	  *[4,500]: Expert Mode
1201	  *[5,737]: Master Mode
1202	  *[2,250]: Expert Mode
1203	  *[2,868]: Master Mode
1204	  *[11,250]: Expert Mode
1205	  *[14,343]: Master Mode
1206	  *[9,000]: Expert Mode
1207	  *[11,474]: Master Mode
1208	  *[6,750]: Expert Mode
1209	  *[8,606]: Master Mode
1210	  *[123 mph]: 123 miles per hour (as measured by the Stopwatch item) or 90 tiles per second
1211	  *[1 mph]: 1 mile per hour (as measured by the Stopwatch item) or 0.73 tiles per second
1212	  *[AMA]: Ask Me Anything
1213	  *[Zdravím [jméno hráče]. Je zde něco, s čím bych mohl pomoci?]: Greetings, [Name of Player]. Is there something I can help you with?
1214	  *[Jsem zde proto, abych ti dával rady co máš dělat. Doporučuji ti si se mnou přijít promluvit, kdykoliv si nebudeš vědět rady.]: I am here to give you advice on what to do next. It is recommended that you talk with me anytime you get stuck.
1215	  *[Říká se, že existuje člověk, který ti poradí, jak máš přežít v této krajině… ale počkat. To jsem přeci já.]: They say there is a person who will tell you how to survive in this land... oh wait. That's me.
1216	  *[Měl bys zůstat v době během noci. Je velmi nebezpečné toulat se v noci.]: You should stay indoors at night. It is very dangerous to be wandering around in the dark.
1217	  *[Hej kamaráde, nevíš, kde se nachází nějaký smrtirost? Jen tak, přemýšlím nahlas.]: Hey, buddy, do you know where any deathweed is? Oh, no reason; Just wondering, is all.
1218	  *[Pokud se podíváš na oblohu, uvidíš, že je měsíc krvavý.]: If you were to look up, you'd see the moon is red right now.
1219	  *[S jistotou můžeš říct, že nastal krvavý měsíc, jakmile se barva oblohy promění v červenou. Něho během této doby způsobuje, že se objevuje více nepřátel.]: You can tell a Blood Moon is out when the sky turns red. There is something about it that causes monsters to swarm.
1220	  *[Oktoberfest je tady! [Jméno obchodníka] uvařil kvůli této události své proslulé pivo a [jméno oděvníka] prodává tradiční oblečení spojené s festivalem.]: The Oktober festival is here! [Name of Merchant] has brewed up some of his famous ale especially for the occasion and [Name of Clothier] is selling traditional festival clothes.
1221	  *[Nový rok je tady! [Jméno demoličního experta] prodává speciální zbraně, které rozzáří oblohu a [jméno oděvníka] prodává tradiční sváteční oděv.]: New Year is here! [Name of Demolitionist] is selling special weaponry to light up the skies, and [Name of Clothier] is selling traditional festive attire.
1222	  *[75]: Expert Mode
1223	  *[Expert-exclusive]: Expert Mode
1224	  *[Master-exclusive]: Master Mode
1225	  *[Hive Pack]: Expert Mode
1226	  *[and third]: Expert Mode
1227	  *[0.9›0.4]: Pre-Hardmode › Hardmode
1228	  *[0.5›0.45]: Pre-Hardmode › Hardmode
1229	  *[216]: Master Mode
1230	  *[252]: Master Mode
1231	  *[6.25–25%]: Master Mode
1232	  *[25–100%]: Master Mode
1233	  *[140–148]: Expert Mode
1234	  *[210–222]: Master Mode
1235	  *[10–20 seconds]: Expert Mode
1236	  *[12.5–25 seconds]: Master Mode
1237	  *[≤ 2 seconds]: Expert Mode
1238	  *[≤ 2.5 seconds]: Master Mode
1239	  *[50–100%]: Master Mode
1240	  *[nebo 3/4]: Expertní mód
1241	  *[tümü]: Master Mode
1242	  *[18750]: Expert Mode
1243	  *[67]: Expert Mode
1244	  *[1–5 seconds]: Expert Mode
1245	  *[1.25–6.25 seconds]: Master Mode
1246	  *[ 17 _CC_ ]: Expert Mode
1247	  *[ 49 _CC_ ]: Expert Mode
1248	  *[ 1 _SC_ 30 _CC_ ]: Expert Mode
1249	  *[ 20 _CC_ ]: Expert Mode
1250	  *[14 _GC_ 81 _SC_]: Expert Mode
1251	  *[16 _GC_ 6 _SC_]: Master Mode
1252	  *[2 _PC_ 67 _GC_]: Expert Mode
1253	  *[2 _PC_ 89 _GC_]: Master Mode
1254	  *[81 _SC_ 20 _CC_]: Expert Mode
1255	  *[3 _SC_ 72 _CC_]: Expert Mode
1256	  *[1 _SC_ 69 _CC_]: Expert Mode
1257	  *[9 _SC_ 20 _CC_]: Expert Mode
1258	  *[8 _SC_ 6 _CC_]: Expert Mode
1259	  *[7 _SC_ 44 _CC_]: Expert Mode
1260	  *[4 _SC_ 92 _CC_]: Expert Mode
1261	  *[2 _SC_ 61 _CC_]: Expert Mode
1262	  *[3 _SC_ 31 _CC_]: Expert Mode
1263	  *[5 _SC_ 26 _CC_]: Expert Mode
1264	  *[3 _SC_ 17 _CC_]: Expert Mode
1265	  *[11 _SC_ 73 _CC_]: Expert Mode
1266	  *[4 _SC_ 32 _CC_]: Expert Mode
1267	  *[16 _SC_ 91 _CC_]: Expert Mode
1268	  *[54 _SC_ 67 _CC_]: Expert Mode
1269	  *[72 _SC_ 68 _CC_]: Expert Mode
1270	  *[44 _SC_ 90 _CC_]: Expert Mode
1271	  *[2 _GC_ 46 _SC_ 61 _CC_]: Expert Mode
1272	  *[45 _SC_ 93 _CC_]: Expert Mode
1273	  *[65 _SC_ 1 _CC_]: Expert Mode
1274	  *[12 _SC_ 81 _CC_]: Expert Mode
1275	  *[1 _GC_ 83 _SC_ 35 _CC_]: Expert Mode
1276	  *[2 _GC_ 65 _SC_]: Expert Mode
1277	  *[7 _GC_ 71 _SC_]: Expert Mode
1278	  *[7 _GC_ 95 _SC_]: Expert Mode
1279	  *[8 _GC_ 71 _SC_]: Expert Mode
1280	  *[21 _GC_ 9 _SC_]: Expert Mode
1281	  *[19 _GC_ 70 _SC_]: Expert Mode
1282	  *[13 _GC_ 25 _SC_]: Expert Mode
1283	  *[26 _GC_ 17 _SC_]: Expert Mode
1284	  *[9 _GC_ 44 _SC_]: Expert Mode
1285	  *[5 _GC_ 31 _SC_]: Expert Mode
1286	  *[3 _GC_ 68 _SC_]: Expert Mode
1287	  *[21 _GC_ 20 _SC_]: Expert Mode
1288	  *[15 _GC_ 90 _SC_]: Expert Mode
1289	  *[15 _GC_ 60 _SC_]: Expert Mode
1290	  *[31 _GC_ 80 _SC_]: Expert Mode
1291	  *[37 _GC_ 71 _SC_]: Expert Mode
1292	  *[39 _GC_ 75 _SC_]: Expert Mode
1293	  *[17 _GC_ 92 _SC_]: Expert Mode
1294	  *[35 _GC_ 51 _SC_]: Expert Mode
1295	  *[66 _GC_ 25 _SC_]: Expert Mode
1296	  *[11 _GC_ 92 _SC_]: Expert Mode
1297	  *[19 _GC_ 73 _SC_]: Expert Mode
1298	  *[26 _GC_ 50 _SC_]: Expert Mode
1299	  *[2 _PC_ 65 _GC_]: Expert Mode
1300	  *[1 _PC_ 18 _GC_]: Expert Mode
1301	  *[45900]: Expert Mode
1302	  *[68850]: Master Mode
1303	  *[327,420]: Expert Mode
1304	  *[436,560]: Master Mode
1305	  *[217500]: Expertní mód
1306	  *[277311]: Master Mode
1307	  *[450]: Master Mode
1308	  *[Master Mode]: Master Mode
1309	  *[245]: Expert Mode
1310	  *[367]: Master Mode
1311	  *[76]: Expert Mode
1312	  *[114]: Master Mode
1313	  *[42000]: Expert Mode
1314	  *[53550]: Master Mode
1315	  *[4–18 seconds]: Expert Mode
1316	  *[5–22.5 seconds]: Master Mode
1317	  *[21000/42000]: Expert Mode
1318	  *[26775/53550]: Master Mode
1319	  *[5›6]: Expert Mode : Pre-Hardmode › Hardmode
1320	  *[6›7]: Master Mode : Pre-Hardmode › Hardmode
1321	  *[1/100 (1%)]: Expert Mode
1322	  *[1/2000 (0.05%)]: Expert Mode
1323	  *[25–40]: Expert Mode
1324	  *[8–28]: Expert Mode
1325	  *[2–20 seconds]: Expert Mode
1326	  *[2.5–25 seconds]: Master Mode
1327	  *[2–8 seconds]: Expert Mode
1328	  *[2.5–10 seconds]: Master Mode
1329	  *[17–30]: Expert Mode
1330	  *[defense]: Expert Mode
1331	  *[14400/28800]: Expert Mode
1332	  *[18360/36720]: Master Mode
1333	  *[25–74]: Expert Mode
1334	  *[13500]: Expert Mode
1335	  *[17212]: Master Mode
1336	  *[11475]: Master Mode
1337	  *[13387]: Master Mode
1338	  *[The [](Shield_of_Cthulhu.md "Shield of Cthulhu")[Shield of Cthulhu](Shield_of_Cthulhu.md "Shield of Cthulhu") can greatly increase your mobility as well as provide some extra defense.]: Expert Mode
1339	  *[The [](Worm_Scarf.md "Worm Scarf")[Worm Scarf](Worm_Scarf.md "Worm Scarf") will reduce damage taken, making it a powerful choice.]: Expert Mode
1340	  *[The [](Brain_of_Confusion.md "Brain of Confusion")[Brain of Confusion](Brain_of_Confusion.md "Brain of Confusion") has a chance to dodge an attack, providing the player with a useful [](Cerebral_Mindtrick "Cerebral Mindtrick")[Cerebral Mindtrick](Cerebral_Mindtrick "Cerebral Mindtrick") buff.]: Expert Mode
1341	  *[91]: Expert Mode
1342	  *[137]: Master Mode
1343	  *[10+25 per hand alive]: Expert Mode
1344	  *[0+25 per hand alive]: Expert Mode
1345	  *[6–10 seconds]: Expert Mode
1346	  *[7.5–12.5 seconds]: Master Mode
1347	  *[1−2 seconds]: Expert Mode
1348	  *[1.5–2.5 seconds]: Master Mode
1349	  *[9.75%]: Expert Mode
1350	  *[55.56%]: Expert Mode
1351	  *[64500]: Expert Mode
1352	  *[82238]: Master Mode
1353	  *[64,500]: Expert Mode
1354	  *[82,238]: Master Mode
1355	  *[12,000]: Expert Mode
1356	  *[15,300]: Master Mode
1357	  *[13,800]: Expert Mode
1358	  *[17,595.2]: Master Mode
1359	  *[[](Shield_of_Cthulhu.md "Shield of Cthulhu")[Shield of Cthulhu](Shield_of_Cthulhu.md "Shield of Cthulhu")'s dash is essential throughout the fight.]: Expert Mode
1360	  *[[](Worm_Scarf.md "Worm Scarf")[Worm Scarf](Worm_Scarf.md "Worm Scarf") greatly decreases damage, but is exclusive to Corruption worlds.]: Expert Mode
1361	  *[The [](Brain_of_Confusion.md "Brain of Confusion")[Brain of Confusion](Brain_of_Confusion.md "Brain of Confusion") is very useful for players as it provides a chance to dodge an attack, but is exclusive to Crimson worlds. It doesn't prevent getting inflicted with the [](Cursed_Inferno.md "Cursed Inferno")[Cursed Inferno](Cursed_Inferno.md "Cursed Inferno") debuff, however.]: Expert Mode
1362	  *[24%]: Expert Mode
1363	  *[28%]: Master Mode
1364	  *[11,920]: Expert Mode
1365	  *[15,198]: Master Mode
1366	  *[1560]: Expert Mode
1367	  *[1989]: Master Mode
1368	  *[3120]: Expert Mode
1369	  *[3978]: Master Mode
1370	  *[8800]: Expert Mode
1371	  *[7.2-12.5]: Master Mode
1372	  *[ Expert-exclusive]: Expert Mode
1373	  *[ Master-exclusive]: Master Mode
1374	  *[(expert)]: Expert Mode
1375	  *[12000]: Expert Mode
1376	  *[13800]: Expert Mode
1377	  *[18-90]: Expert Mode
1378	  *[67,500]: Expert Mode
1379	  *[37,500]: Expert Mode
1380	  *[75,000]: Expert Mode
1381	  *[with a 1/5 (20%) chance]: Expert Mode
1382	  *[41]: Expert Mode
1383	  *[0 mph]: 0 miles per hour (as measured by the Stopwatch item) or 0 tiles per second
1384	  *[150 mph]: 150 miles per hour (as measured by the Stopwatch item) or 110 tiles per second
1385	  *[179 mph]: 179 miles per hour (as measured by the Stopwatch item) or 131.27 tiles per second
1386	  *[ 6500]: Expert Mode
1387	  *[8287]: Master Mode
1388	  *[1.25%–5%]: Expert Mode
1389	  *[32]: Expert Mode
1390	  *[0.25 mph]: 0.25 miles per hour (as measured by the Stopwatch item) or 0.18 tiles per second
1391	  *[ 2700]: Expert Mode
1392	  *[4050]: Master Mode
1393	  *[96 mph]: 96 miles per hour (as measured by the Stopwatch item) or 70.4 tiles per second
1394	  *[164 mph]: 164 miles per hour (as measured by the Stopwatch item) or 120 tiles per second
1395	  *[245 mph]: 245 miles per hour (as measured by the Stopwatch item)
1396	  *[11/100 (11%)]: Expert Mode
1397	  *[5% – 20%]: Expert Mode
1398	  *[6.22% – 31.11%]: Expert Mode
1399	  *[50 mph]: 50 miles per hour (as measured by the Stopwatch item) or 36.67 tiles per second
1400	  *[2–10 or 20 seconds]: Expert Mode
1401	  *[2.5–12.5 or 25 seconds]: Master Mode
1402	  *[2–10 or 20 secondi]: Expert Mode
1403	  *[2.5–12.5 or 25 secondi]: Master Mode
1404	  *[52 mph]: 52 miles per hour (as measured by the Stopwatch item) or 38.13 tiles per second
1405	  *[5.63%]: Expert Mode
1406	  *[2 seconds]: Expert Mode
1407	  *[2.5 seconds]: Master Mode
1408	  *[4,000]: Expert Mode
1409	  *[6,000]: Master Mode
1410	  *[148]: Expert Mode
1411	  *[222]: Master Mode
1412	  *[1.33 seconds]: Expert Mode
1413	  *[1.67 seconds]: Master Mode
1414	  *[33,150]: Expert Mode
1415	  *[42,266]: Master Mode
1416	  *[22,100]: Expert Mode
1417	  *[28,177]: Master Mode
1418	  *[11,050]: Expert Mode
1419	  *[14,088]: Master Mode
1420	  *[4,420]: Expert Mode
1421	  *[5,635]: Master Mode
1422	  *[198]: Master Mode
1423	  *[297]: Master Mode
1424	  *[50 seconds]: Master Mode
1425	  *[1 minute 2.5 seconds]: Master Mode
1426	  *[1.25–5 seconds]: Master Mode
1427	  *[six]: Master Mode
1428	  *[additional accessory slot]: Master Mode
1429	  *[1.25%]: Expert Mode
1430	  *[2.5%]: Expert Mode
1431	  *[38 mph]: 38 miles per hour (as measured by the Stopwatch item) or 28.125 tiles per second
1432	  *[ 36]: Expert Mode
1433	  *[399/40,000 (0.9975%)]: Expert Mode
1434	  *[178]: Master Mode
1435	  *[2,659]: Expert Mode
1436	  *[3,390]: Master Mode
1437	  *[2,519]: Expert Mode
1438	  *[3,212]: Master Mode
1439	  *[2,800–2,240]: Expert Mode
1440	  *[3,570–2,856]: Master Mode
1441	  *[2,239–1,680]: Expert Mode
1442	  *[2,855–2,142]: Master Mode
1443	  *[1,679–1,120]: Expert Mode
1444	  *[2,141–1,428]: Master Mode
1445	  *[1,119–560]: Expert Mode
1446	  *[1,427–714]: Master Mode
1447	  *[559–280]: Expert Mode
1448	  *[713–357]: Master Mode
1449	  *[279–0]: Expert Mode
1450	  *[356–0]: Master Mode
1451	  *[2800]: Expert Mode
1452	  *[3570]: Master Mode
1453	  *[1/15th]: Expert Mode
1454	  *[15%]: Mode Expert
1455	  *[46%]: Expert Mode
1456	  *[52%]: Master Mode
1457	  *[68%]: Master Mode
1458	  *[1000]: Expert Mode
1459	  *[sometimes]: Expert Mode
1460	  *[1.2]: Archery buff
1461	  *[9]: Master Mode
1462	  *[O3DS]: Original Nintendo 3DS
1463	  *[Number]: Number of Tiny Eaters
1464	  *[Average]: Average number of Tiny Eaters
1465	  *[102×102]: Expert Mode
1466	  *[1/25 (4%)]: Expert Mode
1467	  *[44–60]: Expert Mode
1468	  *[66–90]: Master Mode
1469	  *[WoF]: Wall
1470	  *[135]: Master Mode
1471	  *[ (1 player)  
1472	57% (2 players)  
1473	71% (3 players)  
1474	81%  (4 players)  
1475	100% (5 players or more)  
1476	]: Expert Mode
1477	  *[ (1 player)  
1478	62% (2 players)  
1479	75% (3 players)  
1480	83% (4 players)  
1481	100% (5 players or more)  
1482	]: Master Mode
1483	  *[ (1 player)  
1484	69% (2 players)  
1485	79% (3 players)  
1486	86%  (4 players)  
1487	100% (5 players or more)  
1488	]: Expert Mode
1489	  *[ (1 player)  
1490	72% (2 players)  
1491	82% (3 players)  
1492	88% (4 players)  
1493	100% (5 players or more)  
1494	]: Master Mode
1495	  *[1485]: Expert Mode
1496	  *[2227]: Master Mode
1497	  *[2700]: Expert Mode
1498	  *[220]: At least one Ogre has to be killed
1499	  *[330]: Master Mode
1500	  *[224]: Expert Mode
1501	  *[336]: Master Mode
1502	  *[454]: Master Mode
1503	  *[52›93›138]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1504	  *[78›140›208]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1505	  *[60›105›105]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1506	  *[90›157›157]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1507	  *[48›86›131]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1508	  *[73›129›196]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1509	  *[60›105›161]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1510	  *[90›157›241]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1511	  *[45›120›161]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1512	  *[67›180›241]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1513	  *[472]: Master Mode
1514	  *[18–23]: Expert Mode
1515	  *[1/4]: Master Mode
1516	  *[4.94 (79/1600)]: Expert Mode
1517	  *[30–49]: Expert Mode
1518	  *[1/2]: Expert Mode
1519	  *[20–35]: Expert Mode
1520	  *[90–110]: Chế độ Expert
1521	  *[49/625 (7.84%)]: Expert Mode
1522	  *[99/2500 (3.96%)]: Expert Mode
1523	  *[1/15 (6.67%)]: Expert Mode
1524	  *[1/75 (1.33%)]: Expert Mode
1525	  *[1/20 (5%) ****__(Desktop, Console and Mobile versions)]: Expert Mode
1526	  *[5/9 (55.56%)]: Expert Mode
1527	  *[H]: Height (tiles)
1528	  *[14–17]: Expert Mode
1529	  *[3–4]: Expert Mode
1530	  *[12–15]: Chế độ Expert
1531	  *[21-27]: Chế độ Expert
1532	  *[four]: Expert Mode
1533	  *[1–5]: Expert Mode
1534	  *[1.25–6.25]: Master Mode
1535	  *[almost opaque]: Expert Mode
1536	  *[three]: Expert Mode
1537	  *[24,000]: Expert Mode
1538	  *[30,600]: Master Mode
1539	  *[1,200]: Master Mode
1540	  *[16,000]: Expert Mode
1541	  *[20,400]: Master Mode
1542	  *[40000]: Expert Mode
1543	  *[51000]: Master Mode
1544	  *[48000]: Expert Mode
1545	  *[61000]: Master Mode
1546	  *[39 mph]: 39 miles per hour (as measured by the Stopwatch item) or 28.6 tiles per second
1547	  *[599/90,000 (0.6656%)]: Expert Mode
1548	  *[395]: Expert Mode
1549	  *[second phase]: Expert Mode
1550	  *[54000]: Expert Mode
1551	  *[全て]: Master Mode
1552	  *[75 HP]: Chế độ Master
1553	  *[21 Sát thương]: Chế độ Master
1554	  *[20% KB]: Chế độ Master
1555	  *[411 HP]: Chế độ Master
1556	  *[93 Sát thương]: Chế độ Master
1557	  *[Vždy kupuj více drátů, než potřebuješ.]: Always buy more wire than you need!
1558	  *[Je to určitě zapojené do proudu?]: Did you make sure your device was plugged in?
1559	  *[Oh, víš co tento dům opravdu potřebuje? Více blikajících světélek.]: Oh, you know what this house needs? More blinking lights.
1560	  *[Hej [jméno hráče], nevrátil jsi se právě od [jméno gobliního kutila]? Neříkal ti náhodou něco o mně?]: Hey, [Name of Player], did you just come from [Name of Goblin Tinkerer]'s? Did he say anything about me by chance?
1561	  *[Hej, dávej si bacha, kam jdeš! Já jsem tam ještě nedávno byla!]: Hey, watch where you're going! I was over there a little while ago!
1562	  *[[Jméno prodejce zbraní] pořád říká, že stiskne mou tlakovou desku. Já jsem mu ale říkala, že na ni se má šlapat.]: [Name of Arms Dealer] keeps talking about pressing my pressure plate. I told him it was for stepping on.
1563	  *[Oh, nech mě hádat. Zapomněl jsi koupit dostatek drátů. Hlupáku.]: Oh, let me guess. Forgot to buy enough wire. Idiot.
1564	  *[Mohl… Mohl bys… Prosím? Ok? Ok. Ugh.]: Just-could you just...Please? Ok? Ok. Ugh.
1565	  *[Nelíbí se mi, jak se na mě díváš. Já právě PRACUJI.]: I don't appreciate the way you're looking at me. I am WORKING right now.
1566	  *[Všechno co bych pro vypínač chtěla je… Cože?!]: All I want is for the switch to make the... What?!
1567	  *[NEHÝBAT! SPADLA MI KONTAKTNÍ ČOČKA.]: DON'T MOVE. I DROPPED MY CONTACT.
1568	  *[Už jsme byla skoro hotová s věšením blikajících světélek!]: But I was almost done putting blinking lights up here!
1569	  *[Zadrž, už jsem tady dole skoro chytala WiFi signál.]: Hold on, I've almost got wifi going down here.
1570	  *[Děkuji. Trvat to o něco déle, tak skončím jako většina těch kostlivců, co tady dole žije.]: Thanks! It was only a matter of time before I ended up like the rest of the skeletons down here.
1571	  *[Kosh, kapleck Mog. Oh sorry, that's Klingon for 'Buy something or die.']: Kosh, kapleck Mog. Oh promiň, to je klingonsky výraz pro: ‚Něco si kup, nebo zemři.‘
1572	  *[Meč poráží papír! Získej jeden ještě dnes.]: Sword beats paper! Get one today.
1573	  *[Krásné ráno, co myslíš? Nechtěl jsi něco?]: Lovely morning, wouldn't you say? Was there something you needed?
1574	  *[Chceš jablka? Chceš mrkve? Chceš ananasy? Máme pro tebe pochodně!]: You want apples? You want carrots? You want pineapples? We got torches.
1575	  *[Slunce je vysoko, ale mé ceny jsou nízké.]: 
1576	  *[Chlape, to slunce ale pálí! Náhodou mám jedno úžasně ventilované brnění.]: Boy, that sun is hot! I do have some perfectly ventilated armor.
1577	  *[Koukni na moje hliněné bloky, jsou extra hliněné.]: Check out my dirt blocks, they are extra dirty.
1578	  *[Ah, jednoho dnes se budou vyprávět pověsti o [jméno hráče]… jen ty dobré, tím jsem si jist.]: Ah, they will tell tales of [Name of Player] some day... good ones I'm sure.
1579	  *[Brzy nastane noc můj příteli. Rozhodni se dokud ještě můžeš.]: Night be upon us soon, friend. Make your choices while you can.
1580	  *[Nemáš ani ponětí, jakou cenou se v zámoří platí za hliněné bloky.]: You have no idea how much Dirt Blocks sell for overseas.
1581	  *[Kosh, kapleck Mog. Oh promiň, to je [klingonsky](https://en.wikipedia.org/wiki/cs:Klingon "wikipedia:cs:Klingon") výraz pro: ‚Něco si kup, nebo zemři.‘]: Kosh, kapleck Mog. Oh sorry, that's klingon for 'Buy something or die.'
1582	  *[[Jméno hráče], je to tak? Slyšel jsem jen dobré zprávy příteli!]: [Name of Player] is it? I've heard good things, friend!
1583	  *[Občas přemýšlím, jestli je měsíc ze sýra… huh, co? Oh ano, kup něco!]: I wonder if the moon is made of cheese... huh, what? Oh yes, buy something!
1584	  *[Chlápek co teď odcházel mi tady nechal nějaký bordel… uhm chtěl jsem říct… poklady!]: The last guy who was here left some junk... er I mean... treasures!
1585	  *[Řekl jsi zlato? To od tebe klidně odkoupím.]: Did you say gold? I'll take that off of ya.
1586	  *[Slyšel jsem o ukrytém pokladu… oh zapomeň na to.]: I hear there's a secret treasure... oh never mind.
1587	  *[Socha anděla povídáš? Promiň, ale já neprodávám žádné harampádí.]: Angel statue you say? I'm sorry, I'm not a junk dealer.
1588	  *[Viděl jsi už Chith… Shith… Chat… Obří oko?]: Have you seen Chith...Shith.. Chat... The big eye?
1589	  *[Občas hoď okem po ceně, kup čočky!]: Keep your eye on the prize, buy a lens!
1590	  *[Oh výtečně. Už zase slyším [jméno mechaničky] a [jméno sestřičky], jak se hádají.]: Oh, great. I can hear [Name of Mechanic] and [Name of Nurse] arguing from here.
1591	  *[Ani krvavý měsíc nezastaví kapitalismus. Pojďme uzavřít nějaký obchod.]: Not even a Blood Moon can stop capitalism. Let's do some business.
1592	  *[Hej, tento dům je zabezpečený, je to tak? [Jméno hráče], je to tak?!]: Hey, this house is secure, right? Right? [Name of Player]?
1593	  *[Doufám, že takový vychrtlý klučina jako ty není to, co nás má ochránit před okem Cthulu.]: I hope a scrawny kid like you isn't all that's standing between us and Cthulu's Eye.
1594	  *[Cítím, jako kdyby mě sledovala přítomnost zla.]: I feel like an evil presence is watching me.
1595	  *[Když se tak koukám na to ošuntělé brnění, co nosíš, mám chuť ti prodat ještě pár léčivých lektvarů.]: Look at that shoddy armor you're wearing. Better buy some more healing potions.
1596	  *[10–20]: Expert Mode
1597	  *[12–25]: Master Mode
1598	  *[900]: Master Mode
1599	  *[ 5 _GC_]: Expert Mode
1600	  *[25 _GC_]: Expert Mode
1601	  *[11 mph]: 11 miles per hour (as measured by the Stopwatch item) or 8.07 tiles per second
1602	  *[9 mph]: 9 miles per hour (as measured by the Stopwatch item) or 6.6 tiles per second
1603	  *[49]: Expert Mode
1604	  *[Pre-HM]: Pre-Hardmode
1605	  *[101]: Expert Mode
1606	  *[337]: Expert Mode
1607	  *[Enemies that have [picked up coins](Coin_pickup_in_Expert_Mode.md "Coin pickup in Expert Mode")]: Expert Mode
1608	  *[2.67]: Expert Mode
1609	  *[2.25]: Master Mode
1610	  *[16 sekund]: Expertní mód
1611	  *[ 2 _PC_ 50 _GC_]: Expertní mód
1612	  *[40–45]: Expert Mode
1613	  *[187.5]: Master Mode
1614	  *[+24%]: Expert Mode
1615	  *[+28%]: Master Mode
1616	  *[305 mph]: 305 miles per hour (as measured by the Stopwatch item) or 223.67 tiles per second
1617	  *[255 mph]: 255 miles per hour (as measured by the Stopwatch item) or 187 tiles per second
1618	  *[720 mph]: 720 miles per hour (as measured by the Stopwatch item) or 528 tiles per second
1619	  *[0.0396%]: Expert Mode
1620	  *[10,149/1,000,000 (1.01%)]: Expert Mode
1621	  *[199/10,000 (1.99%)]: Expert Mode
1622	  *[36%]: Expert Mode
1623	  *[night]: 7:30 PM – 4:30 AM
1624	  *[dawn]: 4:30 AM
1625	  *[2–8]: Expert Mode
1626	  *[10–30 seconds]: Expert Mode
1627	  *[12.5–37.5 seconds]: Master Mode
1628	  *[10–30]: Expert Mode
1629	  *[12.5–37.5]: Master Mode
1630	  *[3 _SC_]: Expert Mode
1631	  *[3 _GC_]: Expert Mode
1632	  *[6 _SC_]: Expert Mode
1633	  *[4 _SC_ 50 _CC_]: Expert Mode
1634	  *[9 _SC_]: Expert Mode
1635	  *[20 _SC_]: Expert Mode
1636	  *[15 _SC_]: Expert Mode
1637	  *[30 _SC_]: Expert Mode
1638	  *[50 _SC_]: Expert Mode
1639	  *[37 _SC_ 50 _CC_]: Expert Mode
1640	  *[75 _SC_]: Expert Mode
1641	  *[1 _GC_ 20 _SC_]: Expert Mode
1642	  *[90 _SC_]: Expert Mode
1643	  *[1 _GC_ 80 _SC_]: Expert Mode
1644	  *[2 _GC_]: Expert Mode
1645	  *[1 _GC_ 50 _SC_]: Expert Mode
1646	  *[2 _GC_ 25 _SC_]: Expert Mode
1647	  *[4 _GC_ 50 _SC_]: Expert Mode
1648	  *[4 _GC_]: Expert Mode
1649	  *[Hej, nezmiňoval se [jméno prodejce zbraní] o tom, že by potřeboval vyšetřit? Ptám se jen tak.]: Hey, has [Name of Arms Dealer] mentioned needing to go to the doctor for any reason? Just wondering.
1650	  *[Bolí to, když uděláš tohle? Pak tohle nedělej.]: Does it hurt when you do that? Don't do that.
1651	  *[Ukaž mi, co tě bolí.]: Show me where it hurts.
1652	  *[Tohle není to největší, co jsem za svůj život viděla… Ano, už jsem viděla větší rány.]: That's not the biggest I've ever seen... Yes, I've seen bigger wounds for sure.
1653	  *[Otoč hlavu a zakašlej.]: Turn your head and cough.
1654	  *[Někdy si přeji, aby byl [jméno demoličního experta] více opatrný. Už mě unavuje to každodenní přišívání jeho končetin zpět k tělu.]: I wish [Name of Demolitionist] would be more careful. I'm getting tired of having to sew his limbs back on every day.
1655	  *[Lízátko by sis nedal?]: Would you like a lollipop?
1656	  *[Asi si budu muset promluvit s [jméno průvodce]. Jak často si musíš ošetřovat tak těžké popáleniny?]: I need to have a serious talk with [Name of Guide]. How many times a week can you come in with severe lava burns?
1657	  *[Už jsi viděl starce, jak se potuluje kolem podzemní kobky? Vypadá utrápeně.]: Have you seen that Old Man pacing around the dungeon? He looks troubled.
1658	  *[Nedělej ze sebe takové dítě. Už jsem viděla horší.]: Quit being such a baby! I've seen worse.
1659	  *[Zase trable s těmi tyrany?]: Trouble with those bullies again?
1660	  *[To bude potřebovat pár stehu!]: That's gonna need stitches!
1661	  *[vypadáš, jako kdybys byl napůl strávený. Zase jsi honil slizy?]: You look half digested. Have you been chasing slimes again?
1662	  *[Počkej chvíli, mám tady někde nějaké náplasti se zvířátky.]: Hold on, I've got some cartoon bandages around here somewhere.
1663	  *[[Jméno hráče], to rozchodíš a budeš v pořádku. Šmárja.]: Walk it off, (Name of Player), you'll be fine. Sheesh.
1664	  *[Drazí přátelé, sešli jsme se zde, abychom vzdali poslední úctu… ále, budeš v pořádku.]: Dear friends we are gathered here today to bid farewell... oh, you'll be fine.
1665	  *[Myslím si, že toto ti sluší víc.]: I think you look better this way.
1666	  *[Eww… Co se stalo s tvým obličejem?]: Eww.. what happened to your face?
1667	  *[Támhle jsi nechal svoje rameno. Dojdu pro něj.]: You left your arm over there. Let me get that for you.
1668	  *[MŮJ BOŽE. Dobrá jsem, ale TAKHLE zase ne.]: MY GOODNESS. I'm good but I'm not THAT good.
1669	  *[Co má tohle znamenat?]: What is that supposed to mean!?
1670	  *[Nemyslím si, že se mi líbí tvůj tón v hlase.]: I don't think I like your tone.
1671	  *[Co tady děláš? Pokud nekrvácíš, tak tě tady nechci. Běž pryč.]: Why are you even here? If you aren't bleeding, you don't need to be here. Get out.
1672	  *[COŽE?!]: WHAT?!
1673	  *[Pokud plánuješ zemřít, učiň tak venku.]: If you're going to die, do it outside.
1674	  *[Pospěš si a přestaň krvácet.]: Hurry up and stop bleeding.
1675	  *[Běda, jestli se mi tvá krev dostane na sukni.]: You better not get blood on me.
1676	  *[Ani to nebolelo, že ne?]: That didn't hurt too bad, now did it?
1677	  *[Všechno v pořádku. A ne abych se zase načapala, jak skáčeš z dalších útesů.]: All better. I don't want to see you jumping off any more cliffs.
1678	  *[Tohle asi zanechá jizvu.]: That's probably going to leave a scar.
1679	  *[Podařilo se mi tvůj obličej sešít. Příště si dávej větší pozor.]: I managed to sew your face back on. Be more careful next time.
1680	  *[Přestaň plýtvat mým časem.]: Quit wasting my time.
1681	  *[Žádné šťastné konce ode mě nečekej.]: I don't give happy endings.
1682	  *[Pokud nechceš plastickou operaci, tak ti toho víc nenabídnu.]: I can't do anymore for you without plastic surgery.
1683	  *[Omlouvám se, ale mé služby si nemůžeš momentálně dovolit.]: I'm sorry, but you can't afford me.
1684	  *[Budeš potřebovat více zlata, než je tohle.]: I'm gonna need more gold than that.
1685	  *[Jen abys věděl – nepracuji zadarmo.]: I don't work for free you know.
1686	  *[1,485]: Expert Mode
1687	  *[2,227]: Master Mode
1688	  *[500]: Expert Mode
1689	  *[%55]: Expert Mode
1690	  *[%64]: Expert Mode
1691	  *[Vrať se zpět za noci, pokud si přeješ vstoupit.]: Come back at night if you wish to enter.
1692	  *[Nemůžu tě pustit dále, pokud mě neosvobodíš od mé kletby.]: I cannot let you enter until you free me of my curse.
1693	  *[Můj pán nemůže být vyvolán pod záštitou denního světla.]: My master cannot be summoned under the light of day.
1694	  *[Jsi příliš slabý na zlomení mé kletby. Vrať se zpět, až nebudeš taková nicka.]: You are far too weak to defeat my curse. Come back when you aren't so worthless.
1695	  *[Ubohý hlupáku. Nemůžeš si myslet, že bys mohl porazit mého pána ve stavu, v jakém se nacházíš.]: You pathetic fool. You cannot hope to face my master as you are now.
1696	  *[Doufám, že máš tak šest přátel stojících po tvém boku.]: I hope you have like six friends standing around behind you.
1697	  *[Prosím ne, cizinče. Jen bys marnil svůj drahocenný život.]: Please, no, stranger. You'll only get yourself killed.
1698	  *[Cizinče. Budeš dostatečně silný, abys porazil mého pána?]: Stranger, do you possess the strength to defeat my master?
1699	  *[Ty bys mohl být dostatečně silný na osvobození mě od mé kletby…]: You just might be strong enough to free me from my curse...
1700	  *[Prosím! Poraz mého věznitele a osvoboď mne! Zapřísahám tě!]: Please! Battle my captor and free me! I beg you!
1701	  *[Poraz mého pána a já ti zajistím průchod do podzemní kobky.]: Defeat my master, and I will grant you passage into the Dungeon.
1702	  *[Pokud porazíš mého pána, splním ti jedno přání.]: If you beat my master I will grant you one wish.
1703	  *[∞]: Must defeat Betsy
1704	  *[56]: Mode Expert
1705	  *[7–12]: Master Mode
1706	  *[24–40]: Expert Mode
1707	  *[28–48]: Master Mode
1708	  *[20-37.5]: Master Mode
1709	  *[64–120]: Expert Mode
1710	  *[80-150]: Master Mode
1711	  *[56–80]: Expert Mode
1712	  *[70–100]: Master Mode
1713	  *[40–56]: Expert Mode
1714	  *[60-84]: Master Mode
1715	  *[4–20]: Expert Mode
1716	  *[5–25]: Master Mode
1717	  *[28800]: Mode Expert
1718	  *[43200]: Mode Master
1719	  *[16-30]: Mode Expert
1720	  *[64-120]: Mode Expert
1721	  *[40-56]: Mode Expert
1722	  *[要100次]: Journey Mode
1723	  *[1/150 (0.67%)]: Expert Mode
1724	  *[12.89%]: Expert Mode
1725	  *[19%]: Expert Mode
1726	  *[9.78%]: Expert Mode
1727	  *[13.56%]: Expert Mode
1728	  *[29/225 (12.89%)]: Expert Mode
1729	  *[230 mph]: 230 miles per hour (as measured by the Stopwatch item) or 168.75 tiles per second
1730	  *[22/225 (9.78%)]: Expert Mode
1731	  *[19/100 (19%)]: Expert Mode
1732	  *[Expert Mode:]: Expert Mode
1733	  *[1.4%]: Expert Mode
1734	  *[1/70 (1.43%)]: Expert Mode
1735	  *[10›8]: Expert Mode : Pre-Hardmode › Hardmode
1736	  *[300›330]: Expert Mode : Pre-Hardmode › Hardmode
1737	  *[%-13]: Expert Mode
1738	  *[%1,4]: Expert Mode
1739	  *[5/12 (41.67%)]: Expert Mode
1740	  *[6/12 (50%)]: Expert Mode
1741	  *[1/12 (8.33%)]: Expert Mode
1742	  *[4–9]: Expert Mode
1743	  *[33,600]: Expert Mode
1744	  *[42,840]: Master Mode
1745	  *[21,000]: Expert Mode
1746	  *[26,775]: Master Mode
1747	  *[42,000–37,800]: Expert Mode
1748	  *[53,550–48,195]: Master Mode
1749	  *[37,799–33,600]: Expert Mode
1750	  *[48,194–42,840]: Master Mode
1751	  *[33,599–29,400]: Expert Mode
1752	  *[42,839–37,485]: Master Mode
1753	  *[29,399–25,200]: Expert Mode
1754	  *[37,484–32,130]: Master Mode
1755	  *[25,199–21,001]: Expert Mode
1756	  *[32,129–26,776]: Master Mode
1757	  *[21,000–16,800]: Expert Mode
1758	  *[26,775–21,420]: Master Mode
1759	  *[16,799–12,600]: Expert Mode
1760	  *[21,419–16,065]: Master Mode
1761	  *[12,599–8,400]: Expert Mode
1762	  *[16,064–10,710]: Master Mode
1763	  *[8,399–4,200]: Expert Mode
1764	  *[10,709–5,355]: Master Mode
1765	  *[4,199–0]: Expert Mode
1766	  *[5,354–0]: Master Mode
1767	  *[101×101]: Expert Mode
1768	  *[3/2500 (0.12%)]: Expert Mode
1769	  *[2–10 or 20]: Expert Mode
1770	  *[2.5–12.5 or 25]: Master Mode
1771	  *[4–20 or 40]: Expert Mode
1772	  *[5-12.5 or 50]: Master Mode
1773	  *[2.5-10]: Master Mode
1774	  *[4–16]: Expert Mode
1775	  *[5-20]: Master Mode
1776	  *[2.5-7.5]: Master Mode
1777	  *[5-15]: Master Mode
1778	  *[10 or 40]: Expert Mode
1779	  *[12.5 or 50]: Master Mode
1780	  *[20 or 80]: Expert Mode
1781	  *[25 or 100]: Master Mode
1782	  *[5-10]: Chế độ Expert
1783	  *[6-12.5]: Master Mode
1784	  *[10-20]: Expert Mode
1785	  *[12-25]: Master Mode
1786	  *[4–18]: Chế độ Expert
1787	  *[7.5-17.5]: Master Mode
1788	  *[8–36]: Expert Mode
1789	  *[15-35]: Master Mode
1790	  *[4–8]: Expert Mode
1791	  *[8–16]: Expert Mode
1792	  *[5.23-10.5]: Expert Mode
1793	  *[6.53-13.12]: Master Mode
1794	  *[10-21]: Expert Mode
1795	  *[13-26]: Master Mode
1796	  *[14400]: Chế độ Expert
1797	  *[21600]: Chế độ Master
1798	  *[98]: Expert Mode
1799	  *[123]: Master Mode
1800	  *[196]: Expert Mode
1801	  *[246]: Master Mode
1802	  *[2–10 hoặc 20]: Chế độ Expert
1803	  *[4-20 hoặc 40]: Chế độ Expert
1804	  *[4-16]: Chế độ Expert
1805	  *[4-12]: Chế độ Expert
1806	  *[10 hoặc 40]: Chế độ Expert
1807	  *[20 hoặc 80]: Chế độ Expert
1808	  *[8-36]: Chế độ Expert
1809	  *[8-16]: Chế độ Expert
1810	  *[2.625–5.25]: Chế độ Expert
1811	  *[514 mph]: 514 miles per hour (as measured by the Stopwatch item) or 376.93 tiles per second
1812	  *[2/45]: Expert Mode
1813	  *[5–18]: Expert Mode
1814	  *[7–24]: Expert Mode
1815	  *[7–27]: Expert Mode
1816	  *[10–36]: Expert Mode
1817	  *[3–12]: Expert Mode
1818	  *[3–7]: Expert Mode
1819	  *[95 mph]: 95 miles per hour (as measured by the Stopwatch item) or 69.67 tiles per second
1820	  *[membutuhkan 3]: Mode Journey
1821	  *[6×]: Master Mode
1822	  *[3 mph]: 3 miles per hour (as measured by the Stopwatch item) or 1.875 tiles per second
1823	  *[by wave 12]: Expert Mode
1824	  *[0.56%]: Expert Mode
1825	  *[0.83%]: Expert Mode
1826	  *[1.11%]: Expert Mode
1827	  *[2–20]: Expert Mode
1828	  *[2.5–25]: Master Mode
1829	  *[2.5–10]: Master Mode
1830	  *[8-28 (depending on health)]: Chế độ Expert
1831	  *[2-20 seconds]: Chế độ Expert
1832	  *[2.5-25 seconds]: Chế độ Master
1833	  *[2-8 seconds (melee)]: Chế độ Expert
1834	  *[2.5-10 seconds (melee)]: Chế độ Master
1835	  *[14,400]: Expert Mode
1836	  *[18,360]: Master Mode
1837	  *[0.42 seconds]: Expert Mode
1838	  *[0.5 seconds]: Expert Mode
1839	  *[Descrizione]: General description of items in these tiers. Some exceptions will apply.
1840	  *[Mô tả]: Mô tả vật phẩm của bậc này. Một số ngoại lệ sẽ được áp dụng.
1841	  *[**撳呢度** 嚟載入內容。 _（可能會有些微延遲）_]: 呢個內容係喺外部儲存，所以你撳咗之後，喺佢未下載完之前會有延遲。
1842	  *[2.5 hours]: Master Mode
1843	  *[First part]: At 1/7 of the world
1844	  *[Combined]: Both parts (at 3/14 of the world)
1845	  *[1/5600 (0.02%)]: Expert Mode
1846	  *[Laju]: Laju Anak Panah
1847	  *[Krit]: Peluang Kritikal
1848	  *[382]: Master Mode
1849	  *[10.8%]: Expert Mode
1850	  *[35/324 (10.8%)]: Expert Mode
1851	  *[1/400 (0.25%)]: Expert Mode
1852	  *[27 mph]: 27 miles per hour (as measured by the Stopwatch item) or 19.8 tiles per second
1853	  *[5–10 seconds]: Master Mode
1854	  *[5–10]: Master Mode
1855	  *[0.018%]: Expert Mode
1856	  *[17,550]: Expert Mode
1857	  *[22,376]: Master Mode
1858	  *[5,850]: Expert Mode
1859	  *[7,458]: Master Mode
1860	  *[2 minutes]: Expert Mode
1861	  *[2 minutes 30 seconds]: Master Mode
1862	  *[0.56%–3.33%]: Expert Mode
1863	  *[2 minutes]: Expert Mode
1864	  *[2 minutes and 30 seconds]: Master Mode
1865	  *[107 mph]: 107 miles per hour (as measured by the Stopwatch item) or 78.75 tiles per second
1866	  *[cần có 99]: Chế độ Journey
1867	  *[3,099 mph]: 3,099 miles per hour (as measured by the Stopwatch item) or 2,272.5 tiles per second
1868	  *[20–40 seconds]: Expert Mode
1869	  *[25–50 seconds]: Master Mode
1870	  *[two]: Expert Mode
1871	  *[one]: Master Mode
1872	  *[6,600]: Expert Mode
1873	  *[8,415]: Master Mode
1874	  *[118]: Expert Mode
1875	  *[179]: Master Mode
1876	  *[57]: Expert Mode
1877	  *[85]: Master Mode
1878	  *[100 (if hands aren't killed)]: Expert Mode
1879	  *[6-10 seconds]: Expert Mode
1880	  *[0.5-1 seconds]: Expert Mode
1881	  *[76 mph]: 76 miles per hour (as measured by the Stopwatch item) or 55.7065 tiles per second
1882	  *[158]: Expert Mode
1883	  *[20-35]: Expert Mode
1884	  *[criteria met]: Expert Mode
1885	  *[Criteria not met]: Expert Mode
1886	  *[3/125 (2.4%)]: Expert Mode
1887	  *[3/250 (1.2%)]: Expert Mode
1888	  *[2/125 (1.6%)]: Expert Mode
1889	  *[1/125 (0.8%)]: Expert Mode
1890	  *[0.0143%]: Expert Mode
1891	  *[1/7000 (0.0143%)]: Expert Mode
1892	  *[1/70 (1.4286%)]: Expert Mode
1893	  *[1/5600 (0.0179%)]: Expert Mode
1894	  *[1.43%]: Expert Mode
1895	  *[6–12]: Expert Mode
1896	  *[7–15]: Master Mode
1897	  *[2–10]: Expert Mode
1898	  *[2–12]: Master Mode
1899	  *[10–32]: Expert Mode
1900	  *[12.5–40]: Master Mode
1901	  *[0.5–1]: Expert Mode
1902	  *[0.63–1.25]: Master Mode
1903	  *[5.23–10.5]: Expert Mode
1904	  *[6.53–13.12]: Master Mode
1905	  *[membutuhkan 400]: Mode Journey
1906	  *[90 giây]: Chế độ Expert
1907	  *[2 giây]: Chế độ Expert
1908	  *[84 mph]: 84 miles per hour (as measured by the Stopwatch item) or 61.6 tiles per second
1909	  *[Convertable]: Prone to being converted by Corruption, Crimson, or Hallow
1910	  *[Biến đổi được]: Dễ bị biến đổi bởi Corruption, Crimson, hoặc Hallow
1911	  *[15–30]: Expert Mode
1912	  *[No.]: Number
1913	  *[9/10 (90%)]: Expert Mode
1914	  *[40 seconds]: Expert Mode
1915	  *[10.4%]: Expert Mode
1916	  *[2 or 3 seconds]: Expert Mode
1917	  *[2.5 or 3.75 seconds]: Master Mode
1918	  *[10 or 40 seconds]: Expert Mode
1919	  *[12.5 or 50 seconds]: Master Mode
1920	  *[535]: Expert Mode
1921	  *[ 1–4]: Expert Mode
1922	  *[0.1 mph]: 0.1 miles per hour (as measured by the Stopwatch item) or 0.075 tiles per second
1923	  *[Damage]: The damage without modifier and summon damage bonuses
1924	  *[73 mph]: 73 miles per hour (as measured by the Stopwatch item) or 53.53 tiles per second
1925	  *[1600]: Expert Mode
1926	  *[2400]: Master Mode
1927	  *[15,97%]: Expert Mode
1928	  *[23/144 (15,97%)]: Mode Expert
1929	  *[91 mph]: 91 miles per hour (as measured by the Stopwatch item) or 66.73 tiles per second

```


---

## 🤖 Assistant · 2026-08-20T02:59:10.870Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456 && grep -rn \"TheConstant\\|Seed_TheConstant\" --include=\"*.cs\" | grep -v \"UIWorldCreation\" | head -60",
 "description": "Grep all TheConstant flag usages in vanilla source"
}
```


---

## 👤 User(sidechain) · 2026-08-20T02:59:11.064Z

**📎 ToolResult**

```
Terraria.WorldBuilding/WorldSeedOption_DontStarve.cs:5:	protected override string KeyName => "Seed_TheConstant";

```
