# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-12T18:25:16.980Z

```
Read-only research in ~/Project/GLM/SandboxWorld/terraria-wiki-md/ (offline Terraria wiki mirror; filenames = page titles with underscores; use `ls | grep -i <name>` to find, then Read the .md files).

Task: extract the WIKI-STATED numeric values (damage per second / duration / stat modifiers / sources) for the following buffs and debuffs. For each, quote the exact wiki numbers and the file it came from.

DEBUFFS: Poisoned, Acid Venom (Venom), On Fire!, Cursed Inferno, Ichor, Frostburn, Bleeding, Darkness, Silenced, Slow, Weak, Confused, Broken Armor, Suffocation, Chilled, Frozen, Stunned, Electrified, Moon Leech, Betsy's Curse, Ogre Sped, Lovestruck, Stinky, Burning, Mana Sickness, Obstructed, Midas, Daybroken.

BUFFS: Regeneration, Swiftness, Ironskin, Endurance, Wrath, Rage, Lifeforce, Well Fed (Exquisitely Stuffed/Plenty Satisfied tiers), Clairvoyance, Magic Power, Mana Regeneration, Summoning, Bewitched, Sharpened, Ammo Box, Ammo Reservation, Warmth, Gills, Flipper, Featherfall, Gravitation, Obsidian Skin, Invisibility, Hunter, Spelunker, Dangersense, Shine, Night Owl, Battle, Calming, Tipsy, Fishing/Sonar/Crate potions, Mining, Builder, Heartreach, Titan, Inferno, Well Fed.

Also read the buff-station pages: Campfires (campfire buff), Heart Lantern, Star in a Bottle, Sunflower, Peace Candle, Water Candle, Bast Statue (Cat set), Garden Gnome, Slice of Cake, Torch God / Torch-related luck, War Table, Bewitching Table, Sharpening Station, Ammo Box (station), Crystal Ball, Ammo Reservation potion.

Also Buffs.md (the index page) — report what it says about buff duration merge/refresh rules and debuff immunity accessories (e.g. Bezoar, Medicated Bandage, Adhesive Bandage list which debuffs they grant immunity to).

Report as a compact list: `Name — wiki value (file:section)`. Note where the wiki explicitly states a value that changed between versions. Do NOT summarize; give the raw numbers. Search breadth: very thorough.
```

---

## 📎 Attachment · skill_listing · 2026-08-12T18:25:16.988Z

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

## 🤖 Assistant · 2026-08-12T18:25:18.649Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The user wants me to research a large set of Terraria wiki buff/debuff pages in the offline mirror at ~/Project/GLM/SandboxWorld/terraria-wiki-md/. I need to find files by name, read them, extract numeric values, and report.

Let me start by listing the directory and finding relevant files. This is a big task with ~100 pages. Let me be efficient with parallel bash calls.

Let me first check the directory structure.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:25:18.818Z · glm-x-preview-260804

```
I'll research this systematically. Let me start by locating the relevant files.
```


---

## 🤖 Assistant · 2026-08-12T18:25:19.331Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/terraria-wiki-md/ | head -50; echo \"---COUNT---\"; ls ~/Project/GLM/SandboxWorld/terraria-wiki-md/ | wc -l",
 "description": "List wiki mirror directory"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:25:19.684Z

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
_categories_partials_Category_Console_content_pages_1.md
_categories_partials_Category_Console_content_pages_10.md
_categories_partials_Category_Console_content_pages_11.md
_categories_partials_Category_Console_content_pages_12.md
_categories_partials_Category_Console_content_pages_13.md
_categories_partials_Category_Console_content_pages_14.md
_categories_partials_Category_Console_content_pages_15.md
_categories_partials_Category_Console_content_pages_16.md
_categories_partials_Category_Console_content_pages_17.md
_categories_partials_Category_Console_content_pages_2.md
_categories_partials_Category_Console_content_pages_3.md
_categories_partials_Category_Console_content_pages_4.md
_categories_partials_Category_Console_content_pages_5.md
_categories_partials_Category_Console_content_pages_6.md
_categories_partials_Category_Console_content_pages_7.md
_categories_partials_Category_Console_content_pages_8.md
_categories_partials_Category_Console_content_pages_9.md
_categories_partials_Category_Consumable_items_pages_1.md
_categories_partials_Category_Consumable_items_pages_2.md
_categories_partials_Category_Consumable_items_pages_3.md
_categories_partials_Category_Consumable_items_pages_4.md
_categories_partials_Category_Consumable_items_pages_5.md
_categories_partials_Category_Consumable_items_pages_6.md
_categories_partials_Category_Craftable_items_pages_1.md
_categories_partials_Category_Craftable_items_pages_2.md
_categories_partials_Category_Craftable_items_pages_3.md
_categories_partials_Category_Craftable_items_pages_4.md
_categories_partials_Category_Craftable_items_pages_5.md
_categories_partials_Category_Craftable_items_pages_6.md
_categories_partials_Category_Craftable_items_pages_7.md
---COUNT---
    9163

```


---

## 🤖 Assistant · 2026-08-12T18:25:20.633Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && ls | grep -iE '^(Poisoned|Acid_Venom|Venom|On_Fire|Cursed_Inferno|Ichor|Frostburn|Bleeding|Darkness|Silenced|Slow|Weak|Confused|Broken_Armor|Suffocation|Chilled|Frozen|Stunned|Electrified|Moon_Leech|Betsys_Curse|Betsy|Ogre_Sped|Lovestruck|Stinky|Burning|Mana_Sickness|Obstructed|Midas|Daybroken|Webbed)\\.md$'",
 "description": "Find debuff pages"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:25:24.408Z

**📎 ToolResult**

```
Acid_Venom.md
Betsy.md
Bleeding.md
Broken_Armor.md
Burning.md
Chilled.md
Confused.md
Cursed_Inferno.md
Darkness.md
Daybroken.md
Electrified.md
Frostburn.md
Frozen.md
Ichor.md
Mana_Sickness.md
Midas.md
Poisoned.md
Silenced.md
Slow.md
Stinky.md
Suffocation.md
Weak.md
Webbed.md

```


---

## 🤖 Assistant · 2026-08-12T18:25:25.625Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Found most debuff pages. Missing: On Fire!, Moon Leech, Betsy's Curse, Ogre Sped, Lovestruck, Stunned, Obstructed, Venom (probably Acid_Venom covers it). Let me search for those.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:25:26.150Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && ls | grep -iE 'On_Fire|Moon_Leech|Ogre_Sped|Lovestruck|Stunned|Obstructed|Betsys_Curse|Betsy'",
 "description": "Find missing debuff pages"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:25:26.286Z

**📎 ToolResult**

```
Betsy_Mask.md
Betsy_Trophy.md
Betsy.md
Betsy's_Egg.md
Betsy's_Wings
Betsy's_Wings.md
Betsy's_Wrath.md
Category_Betsy_AI_NPCs.md
Category_Moon_Leech_Clot_AI_NPCs.md
Moon_Leech_Clot.md
On_Fire!
On_Fire!.md
Treasure_Bag_(Betsy).md

```


---

## 🤖 Assistant · 2026-08-12T18:25:27.696Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && ls | grep -iE '^(Regeneration|Swiftness|Ironskin|Endurance|Wrath|Range|Rage|Lifeforce|Well_Fed|Exquisitely_Stuffed|Plenty_Satisfied|Clairvoyance|Magic_Power|Mana_Regeneration|Summoning|Bewitched|Sharpened|Ammo_Box|Ammo_Reservation|Warmth|Gills|Flipper|Featherfall|Gravitation|Obsidian_Skin|Invisibility|Hunter|Spelunker|Dangersense|Shine|Night_Owl|Battle|Calm|Calmness|Tipsy|Fishing|Sonar|Crate|Mining|Builder|Heartreach|Titan|Inferno|Buffs?)\\.md$'",
 "description": "Find buff pages"
}
```


---

## 🤖 Assistant · 2026-08-12T18:25:28.596Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && ls | grep -iE 'Campfire|Heart_Lantern|Star_in_a_Bottle|Sunflower|Peace_Candle|Water_Candle|Bast_Statue|Garden_Gnome|Slice_of_Cake|Torch_God|War_Table|Bewitching_Table|Sharpening_Station|Crystal_Ball|Candle'",
 "description": "Find buff station pages"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:25:32.488Z

**📎 ToolResult**

```
Ammo_Box.md
Buffs.md
Exquisitely_Stuffed.md
Fishing.md
Flipper.md
Mana_regeneration.md
Tipsy.md
Well_Fed.md

```


---

## 👤 User(sidechain) · 2026-08-12T18:25:32.621Z

**📎 ToolResult**

```
Bast_Statue.md
Bewitching_Table.md
Campfires
Campfires.md
Candles
Candles.md
Category_Campfire.md
Category_Crystal_Ball_and_Honey.md
Category_Crystal_Ball_and_Lava.md
Category_Crystal_Ball_and_Water,_Sink,_or_Water_fountain.md
Category_Crystal_Ball.md
Crystal_Ball.md
Garden_Gnome
Garden_Gnome.md
Guide_The_Torch_God_strategies.md
Heart_Lantern.md
Legacy_Campfires.md
Legacy_Crystal_Ball.md
Legacy_Roman_candle.md
Legacy_Star_in_a_Bottle.md
Legacy_Sunflower.md
Legacy_Water_Candle.md
Music_Box_(Alt_Torch_God).md
Music_Box_(Torch_God).md
Peace_Candle.md
Pumpkin_Scented_Candle.md
Shadow_Candle.md
Sharpening_Station.md
Silly_Sunflower_set.md
Slice_of_Cake
Slice_of_Cake.md
Star_in_a_Bottle.md
Sunflower_Minecart.md
Sunflower_Statue.md
Sunflower.md
Sunflowers.md
The_Torch_God_(NPC).md
The_Torch_God.md
Torch_God_(achievement).md
Torch_God's_Favor
Torch_God's_Favor.md
Torch_God's_Flavor.md
War_Table_Banner.md
War_Table.md
Water_Candle
Water_Candle.md

```


---

## 🤖 Assistant · 2026-08-12T18:25:36.673Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Many buff pages don't exist as separate .md files — they may be inside `On_Fire!` (a directory?) and potion pages. Let me check: potion buffs like Regeneration, Swiftness, Ironskin, Endurance, Wrath, Rage, Lifeforce, Clairvoyance, Magic Power, Mana Regeneration, Summoning, Bewitched, Sharpened, Ammo Reservation, Warmth, Gills, Featherfall, Gravitation, Obsidian Skin, Invisibility, Hunter, Spelunker, Dangersense, Shine, Night Owl, Battle, Calming, Fishing, Sonar, Crate, Mining, Builder, Heartreach, Titan, Inferno are probably on their potion pages (Regeneration_Potion.md, etc.).

Also "On_Fire!" is a directory (no .md listed for it? Actually `On_Fire!` and `On_Fire!.md` both exist). Let me check the directories.

Also missing: Stunned, Obstructed, Moon Leech (debuff - only Moon_Leech_Clot NPC exists; the Moon Leech buff may be on Buffs.md or Moon_Lord page), Ogre Sped, Lovestruck, Betsy's Curse. These console/old-gen debuffs may be described in Buffs.md or Debuffs.md. Let me search for them via grep.

Let me find potion pages.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:25:37.908Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && ls | grep -iE 'Potion' | grep -iE 'Regeneration|Swiftness|Ironskin|Endurance|Wrath|Rage|Lifeforce|Clairvoyance|Magic_Power|Mana_Regeneration|Summoning|Ammo_Reservation|Warmth|Gills|Featherfall|Gravitation|Obsidian_Skin|Invisibility|Hunter|Spelunker|Dangersense|Spelunker|Shine|Night_Owl|Battle|Calm|Fishing|Sonar|Crate|Mining|Builder|Heartreach|Titan|Inferno|Teleportation|Love|Stinky|Lovestruck'",
 "description": "Find potion pages"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:25:38.089Z

**📎 ToolResult**

```
Ammo_Reservation_Potion.md
Battle_Potion.md
Builder_Potion.md
Calming_Potion.md
Crate_Potion.md
Dangersense_Potion.md
Endurance_Potion.md
Featherfall_Potion.md
Fishing_Potion.md
Gills_Potion.md
Gravitation_Potion.md
Heartreach_Potion.md
Hunter_Potion.md
Inferno_Potion.md
Invisibility_Potion.md
Ironskin_Potion.md
Legacy_Ammo_Reservation_Potion.md
Legacy_Battle_Potion.md
Legacy_Builder_Potion.md
Legacy_Calming_Potion.md
Legacy_Crate_Potion.md
Legacy_Dangersense_Potion.md
Legacy_Endurance_Potion.md
Legacy_Featherfall_Potion.md
Legacy_Fishing_Potion.md
Legacy_Gills_Potion.md
Legacy_Gravitation_Potion.md
Legacy_Heartreach_Potion.md
Legacy_Hunter_Potion.md
Legacy_Inferno_Potion.md
Legacy_Invisibility_Potion.md
Legacy_Ironskin_Potion.md
Legacy_Lifeforce_Potion.md
Legacy_Magic_Power_Potion.md
Legacy_Mana_Regeneration_Potion.md
Legacy_Mining_Potion.md
Legacy_Night_Owl_Potion.md
Legacy_Obsidian_Skin_Potion.md
Legacy_Rage_Potion.md
Legacy_Regeneration_Potion.md
Legacy_Shine_Potion.md
Legacy_Sonar_Potion.md
Legacy_Spelunker_Potion.md
Legacy_Summoning_Potion.md
Legacy_Swiftness_Potion.md
Legacy_Titan_Potion.md
Legacy_Warmth_Potion.md
Legacy_Wrath_Potion.md
Lifeforce_Potion
Lifeforce_Potion.md
Love_Potion.md
Magic_Power_Potion.md
Mana_Regeneration_Potion.md
Mining_Potion.md
Night_Owl_Potion.md
Obsidian_Skin_Potion.md
Rage_Potion.md
Regeneration_Potion.md
Shine_Potion.md
Sonar_Potion.md
Spelunker_Potion.md
Summoning_Potion.md
Swiftness_Potion.md
Teleportation_Potion.md
Titan_Potion.md
Warmth_Potion.md
Wrath_Potion.md

```


---

## 🤖 Assistant · 2026-08-12T18:25:38.822Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && ls | grep -iE 'Debuff|Buffs?\\.(md|$)|On_Fire|Stunned|Obstructed|Moon_Leech|Ogre|Lovestruck|Stinky' ; echo \"---DIRS---\"; ls -d */ 2>/dev/null | head -30",
 "description": "Find debuff index pages and dirs"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:25:43.200Z

**📎 ToolResult**

```
Buffs.md
Category_Buffs.md
Category_Debuffs
Category_Debuffs.md
Category_In-Progress_projects.md
Category_Moon_Leech_Clot_AI_NPCs.md
Debuffs
Debuffs.md
Guide_Armor_progression
Guide_Armor_progression.md
Guide_Game_progression_graph.md
Guide_Game_progression.md
Guide_Ranged_Progression.md
Ichor_(debuff).md
Legacy_Buffs.md
Legacy_Ichor_(debuff).md
Legacy_Slime_(debuff).md
Moon_Leech_Clot.md
Ogre_Mask_(unobtainable).md
Ogre_Mask.md
Ogre_Spit.md
Ogre_Trophy.md
Ogre.md
Ogre's_Club.md
On_Fire!
On_Fire!.md
Permanent_buffs.md
Quick_Buff.md
Slime_(debuff).md
Stinky.md
Treasure_Bag_(Ogre).md
Weapon_progression_switch.md
Whip_debuff.md
Whip_debuffs.md
---DIRS---
'0'_Statue/
'1'_Statue/
'2'_Statue/
'3'_Statue/
'4'_Statue/
'5'_Statue/
'6'_Statue/
'7'_Statue/
'8'_Statue/
'9'_Statue/
'A'_Statue/
'B'_Statue/
'C'_Statue/
'D'_Statue/
'E'_Statue/
'F'_Statue/
'G'_Statue/
'H'_Statue/
'I'_Statue/
'J'_Statue/
'K'_Statue/
'L'_Statue/
'M'_Statue/
'N'_Statue/
'O'_Statue/
'P'_Statue/
'Q'_Statue/
'R'_Statue/
'S'_Statue/
'T'_Statue/

```


---

## 🤖 Assistant · 2026-08-12T18:25:46.594Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. Now I have a picture. Missing pages: Stunned, Obstructed, Moon Leech (buff), Ogre Sped, Lovestruck, Betsy's Curse — these are likely console/old-gen only debuffs described in Debuffs.md index or Buffs.md. Let me grep for them.

Let me now read the main debuff files in parallel. There are many. Let me start with the index pages first (Buffs.md, Debuffs.md) since they contain duration merge/refresh rules and immunity accessories, and also mention console debuffs.

Let me check file sizes first to know how to read.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:25:47.603Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && wc -l Buffs.md Debuffs.md On_Fire\\!.md Poisoned.md Acid_Venom.md Cursed_Inferno.md Frostburn.md Mana_Sickness.md Daybroken.md Electrified.md Midas.md Ichor.md Well_Fed.md Tipsy.md Exquisitely_Stuffed.md Fishing.md Ammo_Box.md Mana_regeneration.md Flipper.md",
 "description": "Check file sizes"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:25:47.644Z

**📎 ToolResult**

```
    1242 Buffs.md
    1456 Debuffs.md
    2006 On_Fire!.md
    2143 Poisoned.md
     539 Acid_Venom.md
     963 Cursed_Inferno.md
    1346 Frostburn.md
    1697 Mana_Sickness.md
     957 Daybroken.md
    1152 Electrified.md
    1728 Midas.md
    2070 Ichor.md
    2277 Well_Fed.md
    2114 Tipsy.md
     736 Exquisitely_Stuffed.md
    1696 Fishing.md
     990 Ammo_Box.md
    1224 Mana_regeneration.md
    1850 Flipper.md
   28186 total

```


---

## 🤖 Assistant · 2026-08-12T18:25:48.298Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && grep -rliE 'Ogre Sped|Lovestruck|Betsy.?s Curse|Stunned|Obstructed' --include='*.md' . 2>/dev/null | head -30",
 "description": "Grep for console-only debuffs"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:25:48.405Z

**📎 ToolResult**

```
Pork_of_the_Sea.md
Dog_Whistle.md
Lightning_Carrot.md
Kites.md
Spawn.md
Saddles.md
Dungeon_Spirit.md
Suspicious_Looking_Tentacle.md
Probe.md
Deactivated_Probe.md
Eye_Bone.md
Mana_Booster.md
Gills_Potion.md
Foxparks.md
Mighty_Wind.md
Dark_Harvest.md
Moon_Charm.md
Toy_Tank.md
Daybroken.md
Slime_Staff.md
Swiftness_Potion.md
Blessed_Apple.md
Stoned.md
Featherfall_Potion.md
Reaper.md
Ghost_(enemy).md
Swarm_Grenade.md
Ham_Bat.md
Faecorn.md
Damage_Booster.md

```


---

## 🤖 Assistant · 2026-08-12T18:25:50.871Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me search more specifically for the debuff names in Debuffs.md and Buffs.md indexes. First, read Debuffs.md — it likely has a table of all debuffs including console-only ones with descriptions.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:25:51.971Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && grep -n -iE 'Ogre Sped|Lovestruck|Betsy|Stunned|Obstructed|Moon Leech' Debuffs.md | head -20",
 "description": "Search Debuffs.md index"
}
```


---

## 🤖 Assistant · 2026-08-12T18:25:51.993Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && grep -rn -iE \"'''Ogre Sped|'''Lovestruck|'''Betsy|'''Stunned|'''Obstructed|'''Moon Leech\" --include='*.md' . 2>/dev/null | head -20",
 "description": "Grep for page-title patterns"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:25:52.014Z

**📎 ToolResult**

```
48:[](Love_Potion.md "Lovestruck") | [Lovestruck](Love_Potion.md "Love Potion")**** __(Desktop, Console, Old-gen console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 119 | Target emits cosmetic red hearts. Increases [happiness](Happiness.md "Happiness") of affected [Town NPCs](Town_NPC.md "Town NPC") by 10%.  | _You are in love!_ | 30 seconds   
73:[](Betsy's_Wrath.md "Betsy's Curse") | [Betsy's Curse](Betsy's_Wrath.md "Betsy's Wrath")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 203 | Target turns purple and emits miasma particles. Adds **40** [armor penetration](Armor_penetration.md "Armor penetration") against the afflicted target.  | _Defense is lowered_ | 5 seconds   
81:[](Legacy%3AHeart_Arrow "Stunned") | [Stunned](Legacy%3AHeart_Arrow "Legacy:Heart Arrow")**** __(3DS version) Internal [Buff ID](Buff_IDs.md "Buff IDs"): m200 | Completely immobilizes the affected target.  | _Paralyzed by love_ | 5–7 seconds   
93:[](Brain_Suckler.md "Obstructed") | [Obstructed](Brain_Suckler.md "Brain Suckler")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 163 | Light brightness is severely lowered and the screen is darkened except for a small area around the player. Also stops natural [health regeneration](Health_regeneration.md "Health regeneration") of the player similar to the [Bleeding](Bleeding.md "Bleeding") debuff.  | _You can't see!_ | While being attacked by a [Brain Suckler](Brain_Suckler.md "Brain Suckler")  
191:  * Players can inflict the [ Acid Venom](Acid_Venom.md "Acid Venom"), [ Betsy's Curse](Betsy's_Wrath.md "Betsy's Wrath"), [ Bleeding](Bleeding.md "Bleeding"), [ Blood Butchered](Blood_Butcherer.md "Blood Butcherer"), [ Broken Armor](Broken_Armor.md "Broken Armor"), [ Celled](Stardust_Cell_Staff.md "Stardust Cell Staff"), [ Confused](Confused.md "Confused"), [ Cursed Inferno](Cursed_Inferno.md "Cursed Inferno"), [ Daybroken](Daybroken.md "Daybroken"), [ Frostbite](Frostbite.md "Frostbite"), [ Frostburn](Frostburn.md "Frostburn"), [ Hellfire](Hellfire.md "Hellfire"), [ Hemorrhage](Hemorrhage.md "Hemorrhage"), [ Ichor](Ichor_\(debuff\) "Ichor \(debuff\)"), [ Lovestruck](Love_Potion.md "Love Potion"), [ Midas](Midas.md "Midas"), [ Oiled](Oiled.md "Oiled"), [ On Fire!](On_Fire!.md "On Fire!"), [ Penetrated](Bone_Javelin.md "Bone Javelin"), [ Poisoned](Poisoned.md "Poisoned"), [ Shadowflame](Shadowflame.md "Shadowflame"), [ Shimmering](Shimmering.md "Shimmering"), [ Slime](Slime_\(debuff\) "Slime \(debuff\)"), [ Sparkle Slime](Sparkle_Slime_Balloon.md "Sparkle Slime Balloon"), [ Stinky](Stinky.md "Stinky"), and [ Wet](Wet.md "Wet") debuffs on most enemies. The following items inflict these debuffs:
202:[](Betsy's_Wrath.md "Betsy's Wrath")[Betsy's Wrath](Betsy's_Wrath.md "Betsy's Wrath")**** __(Desktop, Console and Mobile versions) | [](Betsy's_Wrath.md "Betsy's Curse")[Betsy's Curse](Betsy's_Wrath.md "Betsy's Wrath")**** __(Desktop, Console and Mobile versions)  
260:[](Love_Potion.md "Love Potion")[Love Potion](Love_Potion.md "Love Potion")**** __(Desktop, Console, Old-gen console and Mobile versions) | [](Love_Potion.md "Lovestruck")[Lovestruck](Love_Potion.md "Love Potion")**** __(Desktop, Console, Old-gen console and Mobile versions)  
334:  * [Desktop 1.3.4](Desktop_1.3.4 "Desktop 1.3.4"): [Betsy's Curse](Betsy's_Curse "Betsy's Curse"), [Creative Shock](Creative_Shock.md "Creative Shock"), [Withered Weapon](Withered_Weapon "Withered Weapon"), and [Withered Armor](Withered_Armor "Withered Armor") added.
681:  * [](Betsy's_Egg.md "Itsy Betsy")[Itsy Betsy](Betsy's_Egg.md "Betsy's Egg")**** __(Desktop, Console and Mobile versions)
846:  * [](Betsy's_Wrath.md "Betsy's Curse")[Betsy's Curse](Betsy's_Wrath.md "Betsy's Wrath")**** __(Desktop, Console and Mobile versions)
879:  * [](Brain_Suckler.md "Obstructed")[Obstructed](Brain_Suckler.md "Brain Suckler")**** __(Desktop, Console and Mobile versions)
885:  * [](Love_Potion.md "Lovestruck")[Lovestruck](Love_Potion.md "Love Potion")**** __(Desktop, Console, Old-gen console and Mobile versions)

```


---

## 👤 User(sidechain) · 2026-08-12T18:25:52.712Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-12T18:25:57.516Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Debuffs.md is the index. Note line 48, 73, 81, 93 give values for Lovestruck (+10% happiness, 30s), Betsy's Curse (40 armor pen, 5s), Stunned (5-7s), Obstructed. Need Ogre Sped and Moon Leech. Let me grep Debuffs.md for "Ogre".

Now the strategy: these debuff pages (Poisoned.md etc.) are big (2000+ lines) mostly nav boilerplate. The actual content is near the top. Let me read the top ~150 lines of each page.

Let me read Debuffs.md relevant table rows first, plus grep for Ogre Sped and Moon Leech.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:25:58.091Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && grep -n -iE 'Ogre|Moon Leech|Electrified|Daybroken|Midas' Debuffs.md | head -10",
 "description": "Search for Ogre/Moon Leech in index"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:25:58.121Z

**📎 ToolResult**

```
72:[](Midas.md "Midas") | [Midas](Midas.md "Midas")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 72 | Target glows yellow. Causes afflicted target to drop 10-50% more coins than usual on death.  | _Drop more money on death_ | 2 seconds   
78:[](Daybroken.md "Daybroken") | [Daybroken](Daybroken.md "Daybroken")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 189 | Target is engulfed in solar flames. Deals **100** damage per second to the afflicted target. Can be stacked for up to 8 times by using [Daybreak](Daybreak.md "Daybreak"), resulting in **800** DPS.  | _Incinerated by solar rays_ | 5 seconds   
108:[](Ogre.md "Oozed") | [Oozed](Ogre.md "Ogre")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 197 | Player turns green and drips green goo. Divides the player's horizontal [movement speed](Movement_speed.md "Movement speed") by 3. If after this the player's horizontal speed is greater than 5 mph and the player has no vertical momentum, their horizontal speed will be further halved.  | _Movement is significantly reduced_ | 15 seconds  
123:[](Electrified.md "Electrified") | [Electrified](Electrified.md "Electrified")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 144 | Player is engulfed in electricity and emits sparks. Players take **20** damage per second when pressing [`◀ Left`](Game_controls.md "Game controls") or [`▶ Right`](Game_controls.md "Game controls"), or **4** DPS otherwise.  | _Moving hurts!_ | 4–8 seconds  
191:  * Players can inflict the [ Acid Venom](Acid_Venom.md "Acid Venom"), [ Betsy's Curse](Betsy's_Wrath.md "Betsy's Wrath"), [ Bleeding](Bleeding.md "Bleeding"), [ Blood Butchered](Blood_Butcherer.md "Blood Butcherer"), [ Broken Armor](Broken_Armor.md "Broken Armor"), [ Celled](Stardust_Cell_Staff.md "Stardust Cell Staff"), [ Confused](Confused.md "Confused"), [ Cursed Inferno](Cursed_Inferno.md "Cursed Inferno"), [ Daybroken](Daybroken.md "Daybroken"), [ Frostbite](Frostbite.md "Frostbite"), [ Frostburn](Frostburn.md "Frostburn"), [ Hellfire](Hellfire.md "Hellfire"), [ Hemorrhage](Hemorrhage.md "Hemorrhage"), [ Ichor](Ichor_\(debuff\) "Ichor \(debuff\)"), [ Lovestruck](Love_Potion.md "Love Potion"), [ Midas](Midas.md "Midas"), [ Oiled](Oiled.md "Oiled"), [ On Fire!](On_Fire!.md "On Fire!"), [ Penetrated](Bone_Javelin.md "Bone Javelin"), [ Poisoned](Poisoned.md "Poisoned"), [ Shadowflame](Shadowflame.md "Shadowflame"), [ Shimmering](Shimmering.md "Shimmering"), [ Slime](Slime_\(debuff\) "Slime \(debuff\)"), [ Sparkle Slime](Sparkle_Slime_Balloon.md "Sparkle Slime Balloon"), [ Stinky](Stinky.md "Stinky"), and [ Wet](Wet.md "Wet") debuffs on most enemies. The following items inflict these debuffs:
225:[](Daybreak.md "Daybreak")[Daybreak](Daybreak.md "Daybreak")**** __(Desktop, Console and Mobile versions) | [](Daybroken.md "Daybroken")[Daybroken](Daybroken.md "Daybroken")**** __(Desktop, Console and Mobile versions)  
226:[](Solar_Eruption.md "Solar Eruption")[Solar Eruption](Solar_Eruption.md "Solar Eruption")**** __(Desktop, Console and Mobile versions) | [](Daybroken.md "Daybroken")[Daybroken](Daybroken.md "Daybroken")**** __(Desktop, Console and Mobile versions)  
261:[](Flask_of_Gold.md "Flask of Gold")[Flask of Gold](Flask_of_Gold.md "Flask of Gold") | [](Midas.md "Midas")[Midas](Midas.md "Midas")  
262:[](Golden_Bullet.md "Golden Bullet")[Golden Bullet](Golden_Bullet.md "Golden Bullet") | [](Midas.md "Midas")[Midas](Midas.md "Midas")  
377:  3. ↑ Total DPS calculation includes 48 from Cursed Inferno, 30 from Hellfire, 30 from Acid Venom, 800 from Daybroken, 30 from Shadowflame, 20 from Blood Butchered, 16 from Frostburn, 18 from Penetrated, 15 from Tentacle Spiked, 12 from Bleeding, 100 from Hemorrhage, 200 from Electric Eel's debuff with three other marked enemies nearby, 8 from On Fire!, 6 from Poisoned, 200 from Celled, 50 from Frostbite, 25 from Oiled, and 44 from Dryad's Bane.

```


---

## 🤖 Assistant · 2026-08-12T18:25:58.321Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Debuffs.md",
 "limit": 120
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:25:58.327Z

**📎 ToolResult**

```
1	# Debuffs
2	
3	> 原页面: `Debuffs`
4	
5	# Debuffs
6	
7	**Debuffs** are negative status effects inflicted on a player, [enemy](Enemy "Enemy") or [NPC](NPC "NPC") during combat or through various items or the environment. Active debuffs are shown as icons below the [hotbar](Hotbar.md "Hotbar"), along with their remaining duration. Debuffs are almost universally negative or at least malign effects, in contrast with [buffs](Buffs.md "Buffs"), over which the player has much more control. 
8	
9	In general, damaging debuffs will stack: If a target is both [Poisoned](Poisoned.md "Poisoned") and [On Fire!](On_Fire!.md "On Fire!"), they will take damage from both debuffs (see Notes for more details). [Death](Death.md "Death") always cancels any active debuffs. 
10	
11	Unlike buffs, debuffs cannot be canceled by right-clicking their icons. The [Nurse](Nurse.md "Nurse") can cancel debuffs at a cost that varies from 75 _CC_ / [1 _SC_ 50 _CC_](Expert_Mode.md "Expert Mode") to 3 _GC_ / [6 _GC_](Expert_Mode.md "Expert Mode") per active debuff, depending on some factors (see _[Nurse § Price increases](Nurse#Price_increases "Nurse")_ for more details). This does not apply to [Potion Sickness](Potion_Sickness.md "Potion Sickness") or [Cerebral Mindtrick](Cerebral_Mindtrick "Cerebral Mindtrick"), which cannot be canceled. 
12	
13	## Applicable to players, enemies and NPCs
14	
15	Icon | Name | Effect | Tooltip | Duration   
16	---|---|---|---|---  
17	[](Bleeding.md "Bleeding") | [Bleeding](Bleeding.md "Bleeding")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 30 | Target drips blood Stops natural [health regeneration](Health_regeneration.md "Health regeneration") of the players (items like the [Band of Regeneration](Band_of_Regeneration.md "Band of Regeneration") or the set bonus of the [Palladium armor](Palladium_armor.md "Palladium armor") bypass this effect, as they provide additional regeneration instead of boosting natural regeneration), and deals **12** damage per second to enemies and NPCs.  | _Cannot regenerate life_ | 5–45 seconds  
18	[6–90 seconds](Expert_Mode.md "Expert Mode")  
19	[7.5–112.5 seconds](Master_Mode.md "Master Mode")  
20	[](Poisoned.md "Poisoned") | [Poisoned](Poisoned.md "Poisoned")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 20 | Target turns green and cannot regenerate life. Also causes afflicted players' eyes to appear half-closed. Players take **2** damage per second, while enemies and NPCs take **6** DPS.  | _Slowly losing life_ | 2–20 seconds  
21	[2–40 seconds](Expert_Mode.md "Expert Mode")  
22	[2.5–50 seconds](Master_Mode.md "Master Mode")  
23	[](Acid_Venom.md "Acid Venom") | [Acid Venom](Acid_Venom.md "Acid Venom")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 70 | Target turns purple and cannot regenerate life. Players take **15** damage per second, while enemies and NPCs take **30** DPS.  | _Losing life_ | 4 seconds  
24	[8 seconds](Expert_Mode.md "Expert Mode")  
25	[10 seconds](Master_Mode.md "Master Mode")  
26	[](On_Fire!.md "On Fire!") | [On Fire!](On_Fire!.md "On Fire!")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 24 | Target is engulfed in flames and cannot regenerate life. All entities take **4** damage per second. DPS against players is increased to **50** if [Vampirism](Vampirism "Vampirism") seed is enabled. Coming in contact with [water](Water.md "Water"), [honey](Honey.md "Honey") or [Shimmer](Shimmer.md "Shimmer") removes the debuff.  | _Slowly losing life_ | 0.5–15 seconds  
27	[1–30 seconds](Expert_Mode.md "Expert Mode")  
28	[1.25–37.5 seconds](Master_Mode.md "Master Mode")  
29	[](Hellfire.md "Hellfire") | [Hellfire](Hellfire.md "Hellfire")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 323 | Target is engulfed in flames and cannot regenerate life. Players take **4** damage per second, while enemies and NPCs take **15** DPS. Coming in contact with [water](Water.md "Water"), [honey](Honey.md "Honey") or [Shimmer](Shimmer.md "Shimmer") removes the debuff.  | _Slowly losing life_ | 1–20 seconds   
30	[](Cursed_Inferno.md "Cursed Inferno") | [Cursed Inferno](Cursed_Inferno.md "Cursed Inferno")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 39 | Target is engulfed in cursed flames and cannot regenerate life. Players take **12** damage per second, while enemies and NPCs take **24** DPS and receive **10%** extra knockback.  | _Losing life_ | 2–7 seconds  
31	[4–14 seconds](Expert_Mode.md "Expert Mode")  
32	[5–17.5 seconds](Master_Mode.md "Master Mode")  
33	[](Frostburn.md "Frostburn") | [Frostburn](Frostburn.md "Frostburn")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 44 | Target is engulfed in frost flames and cannot regenerate life. All entities take **8** damage per second.  | _It's either really hot or really cold. Either way it REALLY hurts_ | 6 seconds  
34	[12 seconds](Expert_Mode.md "Expert Mode")  
35	[15 seconds](Master_Mode.md "Master Mode")  
36	[](Frostbite.md "Frostbite") | [Frostbite](Frostbite.md "Frostbite")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 324 | Target is engulfed in frost flames and cannot regenerate life. Players take **8** damage per second, while enemies and NPCs take **25** DPS.  | _It's either really hot or really cold. Either way it REALLY hurts_ | 2–20 seconds   
37	[](Ichor_\(debuff\) "Ichor") | [Ichor](Ichor_\(debuff\) "Ichor \(debuff\)")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 69 | Target glows yellow. Reduces **15** [defense](Defense.md "Defense") from afflicted players, and adds **15** [armor penetration](Armor_penetration.md "Armor penetration") against afflicted enemies and NPCs.  | _Reduced defense_ | 7–15 seconds  
38	[14–30 seconds](Expert_Mode.md "Expert Mode")  
39	[17.5–37.5 seconds](Master_Mode.md "Master Mode")  
40	[](Broken_Armor.md "Broken Armor") | [Broken Armor](Broken_Armor.md "Broken Armor")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 36 | Causes afflicted enemies to turn blue. Halves [defense](Defense.md "Defense") of the afflicted players, and adds **20** [armor penetration](Armor_penetration.md "Armor penetration") against afflicted enemies and NPCs.  | _Defense is cut in half_ | 2–10 seconds  
41	[4–20 seconds](Expert_Mode.md "Expert Mode")  
42	[5–25 seconds](Master_Mode.md "Master Mode")  
43	[](Shimmering.md "Shimmering") | [Shimmering](Shimmering.md "Shimmering")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 353 | Causes the player to phase through all blocks until they reach an opening, and become immune to all damage (except from [bosses](Bosses.md "Bosses") and their minions).   
44	  
45	Causes [Town NPCs](Town_NPCs.md "Town NPCs") to transform into their [shimmered form](Shimmer#NPC_transmutations "Shimmer").   
46	  
47	Causes enemies to gradually turn invisible, and makes certain enemies [transform into other enemies](Shimmer#Critter_and_enemy_transmutations "Shimmer").  | _You've gone insubstantial!_ | Lasts until the player has reached an opening or [the Underworld](The_Underworld.md "The Underworld"), or when [`▲ Up`](Game_controls.md "Game controls"), [`◀ Left`](Game_controls.md "Game controls"), [`▼ Down`](Game_controls.md "Game controls"), or [`▶ Right`](Game_controls.md "Game controls") is pressed after 20 seconds have passed.   
48	[](Love_Potion.md "Lovestruck") | [Lovestruck](Love_Potion.md "Love Potion")**** __(Desktop, Console, Old-gen console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 119 | Target emits cosmetic red hearts. Increases [happiness](Happiness.md "Happiness") of affected [Town NPCs](Town_NPC.md "Town NPC") by 10%.  | _You are in love!_ | 30 seconds   
49	[](Stinky.md "Stinky") | [Stinky](Stinky.md "Stinky")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 120 | Target emites cosmetic green fumes. Decreases [Luck](Luck.md "Luck") of affected by players by 0.25 and makes [Town NPCs](Town_NPC.md "Town NPC") flee from them.  | _You smell terrible_ | 30 seconds   
50	[](Wet.md "Wet") | [Wet](Wet.md "Wet")**** __(Desktop, Console, Old-gen console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 103 | Target drips water. Clears any existing [On Fire!](On_Fire!.md "On Fire!"), [Hellfire](Hellfire.md "Hellfire"), and [Burning](Burning.md "Burning") debuffs and grants an immunity to them. Also grants immunity to [Stinky](Stinky.md "Stinky") debuff on enemies and NPCs.  | _You are dripping water_ | 30 seconds   
51	[](Slime_\(debuff\) "Slime") | [Slime](Slime_\(debuff\) "Slime \(debuff\)")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 137 | Target drips blue goo. Damage from [On Fire!](On_Fire!.md "On Fire!"), [Hellfire](Hellfire.md "Hellfire"), [Cursed Inferno](Cursed_Inferno.md "Cursed Inferno"), [Frostburn](Frostburn.md "Frostburn"), [Frostbite](Frostbite.md "Frostbite"), and [Shadowflame](Shadowflame.md "Shadowflame") debuffs is doubled.  | _You are slimy and sticky_ | 3 seconds   
52	[](Sparkle_Slime_Balloon.md "Sparkle Slime") | [Sparkle Slime](Sparkle_Slime_Balloon.md "Sparkle Slime Balloon")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 320 | Target drips pink goo and sparkles, a purely visual effect.  | _You are slimy and sparkly_ | 30 seconds   
53	  
54	## Applicable to players and enemies only
55	
56	Icon | Name | Effect | Tooltip | Duration   
57	---|---|---|---|---  
58	[](Confused.md "Confused") | [Confused](Confused.md "Confused")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 31 | A purple question mark appears above afflicted enemies. Causes player's [game controls](Game_controls.md "Game controls") to be switched ([`◀ Left`](Game_controls.md "Game controls") with [`▶ Right`](Game_controls.md "Game controls"), and [`▲ Up`](Game_controls.md "Game controls") with [`▼ Down`](Game_controls.md "Game controls")), and reverses enemy's movement directions. Also prevents most enemies from firing projectiles.  | _Movement is reversed_ | 5–14 seconds  
59	[1.5–28 seconds](Expert_Mode.md "Expert Mode")  
60	[1.87–35 seconds](Master_Mode.md "Master Mode")  
61	  
62	## Applicable to players and NPCs only
63	
64	Icon | Name | Effect | Tooltip | Duration   
65	---|---|---|---|---  
66	[](Tipsy.md "Tipsy") | [Tipsy](Tipsy.md "Tipsy")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 25 | Causes affected Player's eyes to appear half-closed, and affected NPCs to drip green goo. Players lose **4** [defense](Defense.md "Defense") in exchange for **+10%** [melee damage](Melee_damage.md "Melee damage"), **+10%** [melee speed](Melee_speed "Melee speed"), **+2%** melee [critical strike chance](Critical_strike_chance "Critical strike chance"), and **+5** [Fishing Power](Fishing_Power.md "Fishing Power"). [Town NPCs](Town_NPC.md "Town NPC") gain **1.1×** defense, **1.1×** damage and **1.11×** attack speed.  | _Increased melee abilities, lowered defense_ | 2 minutes   
67	  
68	## Applicable to enemies and NPCs only
69	
70	Icon | Name | Effect | Tooltip | Duration   
71	---|---|---|---|---  
72	[](Midas.md "Midas") | [Midas](Midas.md "Midas")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 72 | Target glows yellow. Causes afflicted target to drop 10-50% more coins than usual on death.  | _Drop more money on death_ | 2 seconds   
73	[](Betsy's_Wrath.md "Betsy's Curse") | [Betsy's Curse](Betsy's_Wrath.md "Betsy's Wrath")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 203 | Target turns purple and emits miasma particles. Adds **40** [armor penetration](Armor_penetration.md "Armor penetration") against the afflicted target.  | _Defense is lowered_ | 5 seconds   
74	[](Shadowflame.md "Shadowflame") | [Shadowflame](Shadowflame.md "Shadowflame")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 153 | Target is engulfed in shadowflames. Deals **15** damage per second to the afflicted target.  | _Losing life_ | 5–8 seconds   
75	[](Hemorrhage.md "Hemorrhage") | [Hemorrhage](Hemorrhage.md "Hemorrhage")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 375 | Target drips blood. Deals **100** damage per second to the afflicted target.  | _Bleeding profusely_ | 4–12 seconds   
76	[](Oiled.md "Oiled") | [Oiled](Oiled.md "Oiled")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 204 | Target turns gray and drips oil. Deals **25** extra damage per second to targets inflicted with any of [On Fire!](On_Fire!.md "On Fire!"), [Hellfire](Hellfire.md "Hellfire"), [Cursed Inferno](Cursed_Inferno.md "Cursed Inferno"), [Frostburn](Frostburn.md "Frostburn"), [Frostbite](Frostbite.md "Frostbite"), or [Shadowflame](Shadowflame.md "Shadowflame") debuffs.  | _Taking more damage from being on fire_ | 4–9 seconds   
77	[](Bone_Javelin.md "Penetrated") | [Penetrated](Bone_Javelin.md "Bone Javelin")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 169 | Deals **3** damage per second to the afflicted target. Can be stacked for up to 6 times, resulting in **18** DPS.  | _Bleeding Out_ | 15 seconds   
78	[](Daybroken.md "Daybroken") | [Daybroken](Daybroken.md "Daybroken")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 189 | Target is engulfed in solar flames. Deals **100** damage per second to the afflicted target. Can be stacked for up to 8 times by using [Daybreak](Daybreak.md "Daybreak"), resulting in **800** DPS.  | _Incinerated by solar rays_ | 5 seconds   
79	[](Stardust_Cell_Staff.md "Celled") | [Celled](Stardust_Cell_Staff.md "Stardust Cell Staff")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 183 | Deals **20** damage per second to the afflicted target. Can be stacked for up to 10 times, resulting in **200** DPS.  | _being eaten by cells_ | 6–9 seconds   
80	[](Blood_Butcherer.md "Blood Butchered") | [Blood Butchered](Blood_Butcherer.md "Blood Butcherer")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 344 | Deals **4** damage per second to the afflicted target. Can be stacked for up to 5 times, resulting in **20** DPS.  | _Bleeding out rapidly_ | 9 seconds   
81	[](Legacy%3AHeart_Arrow "Stunned") | [Stunned](Legacy%3AHeart_Arrow "Legacy:Heart Arrow")**** __(3DS version) Internal [Buff ID](Buff_IDs.md "Buff IDs"): m200 | Completely immobilizes the affected target.  | _Paralyzed by love_ | 5–7 seconds   
82	  
83	## Applicable to players only
84	
85	Icon | Name | Effect | Tooltip | Duration   
86	---|---|---|---|---  
87	[](Darkness.md "Darkness") | [Darkness](Darkness.md "Darkness")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 22 | Player turns blue and their eyes close. Light brightness is lowered.  | _Decreased light vision_ | 15 seconds  
88	[3–30 seconds](Expert_Mode.md "Expert Mode")  
89	[3.75–37.5 seconds](Master_Mode.md "Master Mode")  
90	[](Blackout.md "Blackout") | [Blackout](Blackout.md "Blackout")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 80 | Player's eyes close. Light brightness is severely lowered.  | _Light vision severely reduced_ | 2–6 seconds  
91	[4–12 seconds](Expert_Mode.md "Expert Mode")  
92	[5–15 seconds](Master_Mode.md "Master Mode")  
93	[](Brain_Suckler.md "Obstructed") | [Obstructed](Brain_Suckler.md "Brain Suckler")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 163 | Light brightness is severely lowered and the screen is darkened except for a small area around the player. Also stops natural [health regeneration](Health_regeneration.md "Health regeneration") of the player similar to the [Bleeding](Bleeding.md "Bleeding") debuff.  | _You can't see!_ | While being attacked by a [Brain Suckler](Brain_Suckler.md "Brain Suckler")  
94	[](Silenced.md "Silenced") | [Silenced](Silenced.md "Silenced")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 35 | Prevents the player from using anything via [`⚒ Use / Attack`](Game_controls.md "Game controls") that requires mana.  | _Cannot use items that require mana_ | 7 seconds  
95	[1.5–14 seconds](Expert_Mode.md "Expert Mode")  
96	[1.87–17.5 seconds](Master_Mode.md "Master Mode")  
97	[](Cursed.md "Cursed") | [Cursed](Cursed.md "Cursed")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 23 | Prevents the player from using any item activated via [`⚒ Use / Attack`](Game_controls.md "Game controls"), [`⚷ Open / Activate`](Game_controls.md "Game controls"), [`Quick Heal`](Game_controls.md "Game controls"), [`Quick Mana`](Game_controls.md "Game controls"), [`Quick Buff`](Game_controls.md "Game controls"), [`Grapple`](Game_controls.md "Game controls"), and [`Quick Mount`](Game_controls.md "Game controls").  | _Cannot use any items_ | 4 seconds  
98	[0.73–8 seconds](Expert_Mode.md "Expert Mode")  
99	[0.92–10 seconds](Master_Mode.md "Master Mode")  
100	[](Creative_Shock.md "Creative Shock") | [Creative Shock](Creative_Shock.md "Creative Shock")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 199 | Cannot place or break blocks.  | _You have lost the power of creation!_ | Infinite during the [Old One's Army](Old_One's_Army.md "Old One's Army") event   
101	[](Chilled.md "Chilled") | [Chilled](Chilled.md "Chilled")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 46 | Multiplies the player's horizontal [movement speed](Movement_speed.md "Movement speed") by 0.75×. Also prevents the player from sprinting with [Boots](Boots.md "Boots") or reaching the unique horizontal speed of [wings](Wings.md "Wings"), instead forcing the player to use their own horizontal movement speed.  | _Your movement speed has been reduced_ | 5–45 seconds  
102	[10–90 seconds](Expert_Mode.md "Expert Mode")  
103	[12.5–112.5 seconds](Master_Mode.md "Master Mode")  
104	[](Slow.md "Slow") | [Slow](Slow.md "Slow")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 32 | Multiplies the player's horizontal [movement speed](Movement_speed.md "Movement speed") by 0.5×. Also prevents the player from sprinting with [Boots](Boots.md "Boots") or reaching the unique horizontal speed of [wings](Wings.md "Wings"), instead forcing the player to use their own horizontal movement speed.  | _Movement speed is reduced_ | 5–16 seconds  
105	[0.5–32 seconds](Expert_Mode.md "Expert Mode")  
106	[0.63–40 seconds](Master_Mode.md "Master Mode")  
107	[](Burning.md "Burning") | [Burning](Burning.md "Burning")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 67 | Players are engulfed in flames and cannot regenerate life. Players take **30** damage per second and their horizontal [movement speed](Movement_speed.md "Movement speed") is multiplied by 0.5×. Also prevents the player from sprinting with [Boots](Boots.md "Boots") or reaching the unique horizontal speed of [wings](Wings.md "Wings"), instead forcing the player to use their own horizontal movement speed.  | _Losing life and slowed movement_ | While in contact with [Meteorite](Meteorite.md "Meteorite"), [Hellstone](Hellstone.md "Hellstone"), or [Hellstone Brick](Hellstone_Brick.md "Hellstone Brick")  
108	[](Ogre.md "Oozed") | [Oozed](Ogre.md "Ogre")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 197 | Player turns green and drips green goo. Divides the player's horizontal [movement speed](Movement_speed.md "Movement speed") by 3. If after this the player's horizontal speed is greater than 5 mph and the player has no vertical momentum, their horizontal speed will be further halved.  | _Movement is significantly reduced_ | 15 seconds  
109	[15 seconds](Expert_Mode.md "Expert Mode")  
110	[15 seconds](Master_Mode.md "Master Mode")  
111	[](Frozen.md "Frozen") | [Frozen](Frozen.md "Frozen")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 47 | Player is encased in ice. Prevents the player from moving or using any item activated via [`⚒ Use / Attack`](Game_controls.md "Game controls"), [`⚷ Open / Activate`](Game_controls.md "Game controls"), [`Quick Heal`](Game_controls.md "Game controls"), [`Quick Mana`](Game_controls.md "Game controls"), [`Quick Buff`](Game_controls.md "Game controls"), [`Grapple`](Game_controls.md "Game controls"), and [`Quick Mount`](Game_controls.md "Game controls").  | _You can't move!_ | 0.33–2 seconds  
112	[0.67–4 seconds](Expert_Mode.md "Expert Mode")  
113	[0.83–5 seconds](Master_Mode.md "Master Mode")  
114	[](Webbed.md "Webbed") | [Webbed](Webbed.md "Webbed")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 149 | Player is trapped in web. Causes the player to be stuck in the spot where they were hit, even ignoring gravity. Also prevents the player from using any item activated via [`⚒ Use / Attack`](Game_controls.md "Game controls"), [`⚷ Open / Activate`](Game_controls.md "Game controls"), [`Quick Heal`](Game_controls.md "Game controls"), [`Quick Mana`](Game_controls.md "Game controls"), [`Quick Buff`](Game_controls.md "Game controls"), [`Grapple`](Game_controls.md "Game controls"), and [`Quick Mount`](Game_controls.md "Game controls").  | _You are stuck_ | [0.5–2.5 seconds](Expert_Mode.md "Expert Mode")  
115	[0.5–2.5 seconds](Master_Mode.md "Master Mode")  
116	[](Stoned.md "Stoned") | [Stoned](Stoned.md "Stoned")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 156 | Player petrifies into a stone statue. Prevents the player from moving or using any item activated via [`⚒ Use / Attack`](Game_controls.md "Game controls"), [`⚷ Open / Activate`](Game_controls.md "Game controls"), [`Quick Heal`](Game_controls.md "Game controls"), [`Quick Mana`](Game_controls.md "Game controls"), [`Quick Buff`](Game_controls.md "Game controls"), [`Grapple`](Game_controls.md "Game controls"), and [`Quick Mount`](Game_controls.md "Game controls"). Also causes the player to take increased fall damage and reduces the distance before fall damage can occur, which will not be negated by any accessories, with the exception of [Djinn's Curse](Djinn's_Curse.md "Djinn's Curse"), or if the player is under the effects of a [Featherfall Potion](Featherfall_Potion.md "Featherfall Potion").  | _You are completely petrified!_ | 1–4 seconds  
117	[1–4 seconds](Expert_Mode.md "Expert Mode")  
118	[1–4 seconds](Master_Mode.md "Master Mode")  
119	[](Mighty_Wind.md "Mighty Wind") | [Mighty Wind](Mighty_Wind.md "Mighty Wind")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 194 | Pushes the player based on direction and speed of the [wind](Wind.md "Wind").  | _The wind moves you around!_ | Infinite while in a [Sandstorm](Sandstorm.md "Sandstorm") and not in front of [Background walls](Background_walls.md "Background walls")  
120	[](Alien_Queen.md "Distorted") | [Distorted](Alien_Queen.md "Alien Queen")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 164 | Causes the player to continually rise and fall in a short wave-like motion, and mostly disables the player's manual vertical movement.  | _Gravity around you is distorted_ | 6–12 seconds  

```


---

## 🤖 Assistant · 2026-08-12T18:26:04.452Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Excellent! The Debuffs.md index is a goldmine. It gives concise numeric values for nearly all debuffs. I still need:
- Moon Leech (not in this index apparently — it's a buff? "Moon Leech" is buff ID 195 inflicted by Moon Lord's Moon Leech Clot on player; it's listed as a debuff on the Moon Lord page maybe). Let me grep.
- Ogre Sped — console/old-gen debuff, may be on Ogre.md (Desktop Ogre has Oozed; Old-gen Ogre has Ogre Sped?). Let me check Ogre.md.
- Suffocation, Weak, Mana Sickness, Frozen, Electrified, Daybroken, Stinky, Lovestruck, Burning, Midas — need remaining ones from this index (lines 120+). Let me read the rest of the index table.

Let me read lines 120-200 of Debuffs.md.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:26:04.464Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Debuffs.md",
 "offset": 120,
 "limit": 70
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:26:04.469Z

**📎 ToolResult**

```
120	[](Alien_Queen.md "Distorted") | [Distorted](Alien_Queen.md "Alien Queen")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 164 | Causes the player to continually rise and fall in a short wave-like motion, and mostly disables the player's manual vertical movement.  | _Gravity around you is distorted_ | 6–12 seconds  
121	[5–9 seconds](Expert_Mode.md "Expert Mode")  
122	[5–9 seconds](Master_Mode.md "Master Mode")  
123	[](Electrified.md "Electrified") | [Electrified](Electrified.md "Electrified")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 144 | Player is engulfed in electricity and emits sparks. Players take **20** damage per second when pressing [`◀ Left`](Game_controls.md "Game controls") or [`▶ Right`](Game_controls.md "Game controls"), or **4** DPS otherwise.  | _Moving hurts!_ | 4–8 seconds  
124	[4–8 seconds](Expert_Mode.md "Expert Mode")  
125	[4–8 seconds](Master_Mode.md "Master Mode")  
126	[](Suffocation.md "Suffocation") | [Suffocation](Suffocation.md "Suffocation")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 68 | Players take **20** damage per second and cannot regenerate life.  | _Losing life_ | While buried under fallen [Silt](Silt "Silt"), [Sand](Sand "Sand"), and [Slush](Slush "Slush").   
127	[](Wither_Beast.md "Withered Armor") | [Withered Armor](Wither_Beast.md "Wither Beast")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 195 | Player turns blue. Halves the player's [defense](Defense.md "Defense").  | _Your armor is lowered!_ | While within 25 tiles of a [Wither Beast](Wither_Beast.md "Wither Beast")  
128	[](Etherian_Lightning_Bug.md "Withered Weapon") | [Withered Weapon](Etherian_Lightning_Bug.md "Etherian Lightning Bug")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 196 | Player emits sparks when attacking. Halves all player–inflicted damage, except for classless damage.  | _Your attacks are weaker!_ | 5 seconds  
129	[5 seconds](Expert_Mode.md "Expert Mode")  
130	[5 seconds](Master_Mode.md "Master Mode")  
131	[](Weak.md "Weak") | [Weak](Weak.md "Weak")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 33 | Decreases the player's physical stats (-4 [defense](Defense.md "Defense"), -5.1% [melee damage](Melee_damage.md "Melee damage"), -5.1% [melee speed](Melee_speed "Melee speed"), -10% [movement speed](Movement_speed.md "Movement speed")).  | _Physical abilities are decreased_ | 60–300 seconds  
132	[11.23–600 seconds](Expert_Mode.md "Expert Mode")  
133	[14.03–750 seconds](Master_Mode.md "Master Mode")  
134	[](Hunger.md "Peckish") | [Peckish](Hunger.md "Hunger")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 332 | No actual effect.  | _You could eat, but it's not so bad._ | While in the first stage of [Hunger](Hunger.md "Hunger"), for 5 minutes (8 minutes with [Remix](Remix.md "Remix") seed enabled).   
135	[](Hunger.md "Hungry") | [Hungry](Hunger.md "Hunger")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 333 | Decreases the player's stats (-2 [defense](Defense.md "Defense"), -5% [damage](Damage.md "Damage"), -5% [melee speed](Melee_speed "Melee speed"), -2% [critical strike chance](Critical_strike_chance "Critical strike chance"), -0.5 Minion and Sentry [knockback](Knockback.md "Knockback"), -5% [mining speed](Mining_speed "Mining speed")).  | _You are quite hungry and feeling weak._ | While in the second stage of Hunger, for 5 minutes (8 minutes with [Remix](Remix.md "Remix") seed enabled).   
136	[](Hunger.md "Starving") | [Starving](Hunger.md "Hunger")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 334 | Nullifies all [health regeneration](Health_regeneration.md "Health regeneration"), deals damage to the player equal to 2% of their maximum health every second, and decreases the player's stats (-4 [defense](Defense.md "Defense"), -10% [damage](Damage.md "Damage"), -10% [melee speed](Melee_speed "Melee speed"), -4% [critical strike chance](Critical_strike_chance "Critical strike chance"), -1 Minion and Sentry [knockback](Knockback.md "Knockback"), -15% [mining speed](Mining_speed "Mining speed"))..  | _You are starving to death! Eat immediately!_ | While in the third stage of Hunger, until food is eaten or the player dies.   
137	[](Feral_Bite.md "Feral Bite") | [Feral Bite](Feral_Bite.md "Feral Bite")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 148 | Increases player's damage by 20% (not including classless damage), but halves effectiveness of their natural [health regeneration](Health_regeneration.md "Health regeneration") and can randomly apply the following debuffs: [Darkness](Darkness.md "Darkness"), [Cursed](Cursed.md "Cursed"), [Confused](Confused.md "Confused"), [Slow](Slow.md "Slow"), [Weak](Weak.md "Weak"), and [Silenced](Silenced.md "Silenced").  | _Increased damage, Decreased life regen, Causes status effects_ | [3–90 seconds](Expert_Mode.md "Expert Mode")  
138	[3–90 seconds](Master_Mode.md "Master Mode")  
139	[](Brain_of_Confusion.md "Cerebral Mindtrick") | [Cerebral Mindtrick](Brain_of_Confusion.md "Brain of Confusion")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 321 | Increases the player's [critical strike chance](Critical_strike_chance "Critical strike chance") and [summon damage](Summon_damage.md "Summon damage") by 10%. Cannot use [Brain of Confusion](Brain_of_Confusion.md "Brain of Confusion") to dodge.  | _Increased critical chance and minion damage_ | 4 seconds   
140	[](Rod_of_Discord.md "Chaos State") | [Chaos State](Rod_of_Discord.md "Rod of Discord")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 88 | Causes the player to lose health equal to ****__(Desktop, Console and Mobile versions) 1/7th / ****__(Old-gen console and 3DS versions) 1/6th of their maximum health if they use the [Rod of Discord](Rod_of_Discord.md "Rod of Discord") again while the debuff is active.  | _Using the Rod of Discord will take life_ | 6 seconds   
141	[](Wall_of_Flesh.md "Horrified") | [Horrified](Wall_of_Flesh.md "Wall of Flesh")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 37 | Causes the player to die if they are more than 187.5 tiles away from the [Wall of Flesh](Wall_of_Flesh.md "Wall of Flesh").  | _You have seen something nasty, there is no escape._ | While fighting Wall of Flesh   
142	[](The_Tongue.md "The Tongue") | [The Tongue](The_Tongue.md "The Tongue")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 38 | Pulls the player through tiles, directly in front of the [Wall of Flesh](Wall_of_Flesh.md "Wall of Flesh"). In [Expert Mode](Expert_Mode.md "Expert Mode"), Deals **50** damage per second to the player.  | _You are being sucked into the mouth_ | While in contact with [The Tongue](The_Tongue.md "The Tongue")  
143	[](Moon_Bite.md "Moon Bite") | [Moon Bite](Moon_Bite.md "Moon Bite")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 145 | Prevents the player from healing via [Vampire Knives](Vampire_Knives.md "Vampire Knives") or [Spectre Hood](Spectre_armor.md "Spectre armor").  | _You are unable to absorb healing effects_ | 14 seconds  
144	[16 seconds](Expert_Mode.md "Expert Mode")  
145	[16 seconds](Master_Mode.md "Master Mode")  
146	[](Potion_Sickness.md "Potion Sickness") | [Potion Sickness](Potion_Sickness.md "Potion Sickness")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 21 | Prevents the player from drinking [healing potions](Healing_potions "Healing potions").  | _Cannot consume anymore healing items_ | 70–30 seconds (52.5−22.5 seconds with a [Philosopher's Stone](Philosopher's_Stone.md "Philosopher's Stone") or [Charm of Myths](Charm_of_Myths.md "Charm of Myths"))   
147	[](Mana_Sickness.md "Mana Sickness") | [Mana Sickness](Mana_Sickness.md "Mana Sickness")**** __(Desktop, Console, Old-gen console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 94 | Player's magic damage is multiplicatively reduced by 25%, with the amount of damage reduction being lowered by 1% every 0.2 seconds.  | _Magic damage reduced by_ | 5–10 seconds   
148	[](Water_Candle.md "Water Candle") | [Water Candle](Water_Candle.md "Water Candle")Internal [Buff ID](Buff_IDs.md "Buff IDs"): 86 | Causes enemies to spawn 1.33× faster and multiplies max number of enemies on screen by 1.5×.  | _Increased monster spawn rate_ | When holding a [water Candle](Water_Candle.md "Water Candle") or near a placed Water Candle   
149	[](Shadow_Candle.md "Shadow Candle") | [Shadow Candle](Shadow_Candle.md "Shadow Candle")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 350 | Nullifies the enemy spawn reduction benefits of [Town NPCs](Town_NPC.md "Town NPC") in the area, and negates [unique spawning requirement of certain enemies](Guide%3AEnemy_farming#Shadow_Candle "Guide:Enemy farming").  | _Dispels the peace of towns_ | When holding a [Shadow Candle](Shadow_Candle.md "Shadow Candle") or near a placed Shadow Candle   
150	  
151	## Applicable to enemies only
152	
153	Icon | Name | Effect | Tooltip | Duration   
154	---|---|---|---|---  
155	[](Dryad's_Blessing.md "Dryad's Bane") | [Dryad's Bane](Dryad's_Blessing.md "Dryad's Blessing")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 186 | Target emits golden particles. Deals between **4 /[ 6](Expert_Mode.md "Expert Mode") / [7](Master_Mode.md "Master Mode")** to **12 /[ 18](Expert_Mode.md "Expert Mode") / [22](Master_Mode.md "Master Mode")** damage per second to afflicted enemies, depending on how many [bosses](Bosses.md "Bosses") are defeated. DPS is doubled if [Purify this](Purify_this.md "Purify this") seed is enabled.  | _The power of nature compells you_ | While inside [Dryad](Dryad.md "Dryad")'s leaf shield.   
156	  
157	## Unobtainable debuffs
158	
159	Icon | Name | Effect | Tooltip | Notes   
160	---|---|---|---|---  
161	[](Dazed.md "Dazed") | [Dazed](Dazed.md "Dazed")**** __(Desktop, Console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 160 | Divides the player's horizontal [movement speed](Movement_speed.md "Movement speed") by 3, [jump speed](Jump_speed.md "Jump speed") by 2, and [jump duration](Jump_duration.md "Jump duration") by 5.  | _Movement is greatly slowed_ | Unobtainable during normal gameplay   
162	  
163	## Notes
164	
165	  * When an entity is inflicted with multiple damage-over-time debuffs, only the damage numbers from the strongest debuff will appear on it, but the damage ticks will happen faster to account for all the inflicted debuffs, ensuring that all of them deal their full DPS.[1]
166	    * For example, an enemy inflicted with the [Acid Venom](Acid_Venom.md "Acid Venom") debuff takes 15 damage every 0.5 seconds (resulting in 30 DPS), while an enemy inflicted with the [Shadowflame](Shadowflame.md "Shadowflame") debuff takes 5 damage every 0.33 seconds (resulting in 15 DPS). Enemies that are inflicted with both Acid Venom and Shadowflame will take 15 damage every 0.33 seconds (resulting in 45 DPS, which is equal to the DPS of Acid Venom and Shadowflame added together).
167	  * The duration of the following debuffs, if inflicted on players, is increased by 100% in [Expert Mode](Expert_Mode.md "Expert Mode")**** __(Desktop, Console and Mobile versions) (i.e. doubled) and by 150% in [Master Mode](Master_Mode.md "Master Mode")**** __(Desktop, Console and Mobile versions) :[2]
168	
169	    * [](Acid_Venom.md "Acid Venom")[Acid Venom](Acid_Venom.md "Acid Venom")
170	    * [](Blackout.md "Blackout")[Blackout](Blackout.md "Blackout")
171	    * [](Bleeding.md "Bleeding")[Bleeding](Bleeding.md "Bleeding")
172	    * [](Broken_Armor.md "Broken Armor")[Broken Armor](Broken_Armor.md "Broken Armor")
173	    * [](Chilled.md "Chilled")[Chilled](Chilled.md "Chilled")
174	    * [](Confused.md "Confused")[Confused](Confused.md "Confused")
175	    * [](Cursed.md "Cursed")[Cursed](Cursed.md "Cursed")
176	    * [](Cursed_Inferno.md "Cursed Inferno")[Cursed Inferno](Cursed_Inferno.md "Cursed Inferno")
177	    * [](Darkness.md "Darkness")[Darkness](Darkness.md "Darkness")
178	    * [](Frostbite.md "Frostbite")[Frostbite](Frostbite.md "Frostbite")**** __(Desktop, Console and Mobile versions)
179	    * [](Frostburn.md "Frostburn")[Frostburn](Frostburn.md "Frostburn")
180	    * [](Frozen.md "Frozen")[Frozen](Frozen.md "Frozen")
181	    * [](Hellfire.md "Hellfire")[Hellfire](Hellfire.md "Hellfire")**** __(Desktop, Console and Mobile versions)
182	    * [](Ichor_\(debuff\) "Ichor")[Ichor](Ichor_\(debuff\) "Ichor \(debuff\)")
183	    * [](On_Fire!.md "On Fire!")[On Fire!](On_Fire!.md "On Fire!")
184	    * [](Poisoned.md "Poisoned")[Poisoned](Poisoned.md "Poisoned")
185	    * [](Silenced.md "Silenced")[Silenced](Silenced.md "Silenced")
186	    * [](Slow.md "Slow")[Slow](Slow.md "Slow")
187	    * [](Weak.md "Weak")[Weak](Weak.md "Weak")
188	
189	    * Furthermore, players in Expert worlds are inflicted with the Chilled debuff when they enter [water](Water.md "Water") or [Shimmer](Shimmer.md "Shimmer") in a [Snow biome](Snow_biome.md "Snow biome"). The Chilled debuff lasts for as long as the player is in the liquid plus [5](Expert_Mode.md "Expert Mode") / [6.25](Master_Mode.md "Master Mode") seconds after getting out.

```


---

## 🤖 Assistant · 2026-08-12T18:26:04.486Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && grep -n -iE 'Moon Leech|Ogre Sped' Ogre.md Buffs.md Moon_Leech_Clot.md 2>/dev/null | head -20",
 "description": "Find Moon Leech and Ogre Sped"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:26:04.513Z

**📎 ToolResult**

```
Moon_Leech_Clot.md:1:# Moon Leech Clot
Moon_Leech_Clot.md:5:# Moon Leech Clot
Moon_Leech_Clot.md:11:Moon Leech ClotHardmode exclusive
Moon_Leech_Clot.md:18:[AI Type](AI.md "AI")| Moon Leech Clot AI  
Moon_Leech_Clot.md:33:The **Moon Leech Clot** is a [Hardmode](Hardmode.md "Hardmode"), post-[Lunatic Cultist](Lunatic_Cultist.md "Lunatic Cultist") [projectile NPC](Projectile_NPC "Projectile NPC") which is spawned at the player's position when the [Moon Lord](Moon_Lord.md "Moon Lord")'s tongue grabs hold of the player. Moon Leech Clots do not deal any damage, but if a Moon Leech Clot manages to reach the Moon Lord's mouth before it is killed, a part of the Moon Lord that is currently alive regains 1,000 health. 
Moon_Leech_Clot.md:37:  * Moon Leech Clots take 1.5 seconds to reach the Moon Lord's mouth.
Moon_Leech_Clot.md:41:  * Moon Leech Clots will always reach the Moon Lord's mouth in the same amount of time. They travel toward it at a variable rate, remaining almost stationary if the Moon Lord is in its default position behind the player. As a result of this, though it may seem counterintuitive, it is actually beneficial to be closer to the mouth to destroy Moon Leech Clots, as they will not move away as quickly.
Moon_Leech_Clot.md:42:  * Due to their low health and 0 [defense](Defense.md "Defense"), Moon Leech Clots can be easily taken out with most [Hardmode](Hardmode.md "Hardmode") weapons, but due to their fast speed, they should be targeted as soon as they appear.
Moon_Leech_Clot.md:547:    * Moon Leech Clot
Moon_Leech_Clot.md:738:  * [Moon Leech Clot AI NPCs](Category%3AMoon_Leech_Clot_AI_NPCs "Category:Moon Leech Clot AI NPCs")
Ogre.md:709:    * [Moon Leech Clot](Moon_Leech_Clot.md "Moon Leech Clot")

```


---

## 🤖 Assistant · 2026-08-12T18:26:07.123Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Moon Leech isn't on those pages. Let me search Buffs.md for Moon Leech (it's buff ID 195? Actually "Moon Leech" is a buff on the Moon Lord — Moon Leech debuff on player prevents life regen? Actually "Moon Leech" (buff ID 195) is applied to Moon Lord while leeching). Let me grep the whole wiki for "Moon Leech" as a buff name. Also Ogre Sped — likely in Debuffs.md console section? Let me grep whole tree.

Actually "Ogre Sped" was the Old-gen console Ogre debuff. Let me search the whole tree for both.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:26:07.911Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && grep -rln 'Ogre Sped' . 2>/dev/null | head; echo '---MOONLEECH---'; grep -rln 'Moon Leech' --include='*.md' . 2>/dev/null | grep -v Clot | head",
 "description": "Search tree for Ogre Sped and Moon Leech buff"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:26:08.217Z

**📎 ToolResult**

```
---MOONLEECH---
Anomura_Fungus.md
Goblin_Warrior.md
Spore_Zombie.md
Cochineal_Beetle.md
Parrot.md
Sea_Turtle.md
Dungeon_Spirit.md
Cyborg.md
Krampus.md
Probe.md

```


---

## 🤖 Assistant · 2026-08-12T18:26:08.613Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && grep -n -iE 'leech' Buffs.md | head -10; echo '---'; grep -n -iE 'merge|refresh|stack' Buffs.md | head -20",
 "description": "Search Buffs.md index for leech/merge rules"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:26:08.642Z

**📎 ToolResult**

```
---

```


---

## 🤖 Assistant · 2026-08-12T18:26:11.441Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
No "Ogre Sped" anywhere, and "Moon Leech" only appears as "Moon Leech Clot" references. So the wiki mirror doesn't have pages for Ogre Sped or Moon Leech as buffs. Good to note in report.

Wait, "Moon Leech" grep matched pages like Anomura_Fungus — those are probably "The Leech" (devourer?) or nav. Anyway, no dedicated page.

Now, Buffs.md grep for 'merge|refresh|stack' returned nothing — maybe the wording is different. Let me read Buffs.md.

Let me now read Buffs.md in full-ish (1242 lines, but mostly nav). Let me read the first ~120 lines to see the buff table.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:26:11.642Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Buffs.md",
 "limit": 150
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:26:11.844Z

**📎 ToolResult**

```
1	# Buffs
2	
3	> 原页面: `Buffs`
4	
5	# Buffs
6	
7	[](Desktop_version_history.md "Desktop version") [](Console_version.md "Console version") [](Mobile_version.md "Mobile version")
8	
9	This is the **main** page whose information applies to the **[Desktop](Desktop_version_history.md "Desktop version history")** , **[Console](Console_version.md "Console version")** , and **[Mobile](Mobile_version.md "Mobile version")** versions of _[Terraria](Terraria.md "Terraria")_.  
10	For the differences of this information on [Old-gen console](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [3DS](Legacy%3A3DS_version "Legacy:3DS version"), see **[Legacy:Buffs](Legacy%3ABuffs "Legacy:Buffs")**.
11	
12	**Buffs** are positive status effects granted to a player upon consuming, equipping, or otherwise activating various items. Active buffs are shown as icons below the [hotbar](Hotbar.md "Hotbar"), along with their remaining duration. Buffs are almost universally positive or at least benign effects, in contrast with [debuffs](Debuffs.md "Debuffs"), over which the player has much less control. [Pets](Pets.md "Pets"), [light pets](Light_pets.md "Light pets"), [minions](Minion "Minion"), and [mounts](Mounts.md "Mounts") also have their own associated buffs while they are activated. 
13	
14	Buffs can be easily activated with the buff [hotkey](Hotkey "Hotkey") ([](Desktop_version_history.md "Desktop version") default [`B`](Game_controls.md "Game controls")), which activates all the buff-granting consumables in the player's inventory (starting from the top-left) that are not currently activated. A player is limited to 44 active buffs and debuffs at any one point, and the leftmost buff in the bar will be deactivated if another is applied after this limit is reached. Most buffs can be deactivated prematurely by right-clicking the icon ([](Desktop_version_history.md "Desktop version")), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff ([](Console_version.md "Console version")), or by double-tapping the buff icon ([](Mobile_version.md "Mobile version")). However, buffs that are granted by proximity to an entity will only deactivate when the player is no longer in range _(seeEnvironmental below)_. 
15	
16	Most activated buffs are bound to a character, and persist as that character moves from server to server and from world to world, with the exception of buffs granted from equipments, which disappear when they leave the world. Buffs are always deactivated on the player's [death](Death.md "Death"), with the exception of those granted by [flasks](Flasks.md "Flasks"). 
17	
18	## Consumables
19	
20	These buffs are provided from sources that are consumed upon use, such as [potions](Potions.md "Potions"), flasks, and [food](Food.md "Food"). 
21	
22	Icon  | Name  | Source  | Effect  | Tooltip  | Duration   
23	---|---|---|---|---|---  
24	[](Ammo_Reservation_Potion.md "Ammo Reservation") | [Ammo Reservation](Ammo_Reservation_Potion.md "Ammo Reservation Potion") | [](Ammo_Reservation_Potion.md "Ammo Reservation Potion")[Ammo Reservation Potion](Ammo_Reservation_Potion.md "Ammo Reservation Potion") | Reduces the chance of consuming any [ammunition](Ammunition "Ammunition") by 20%.  | 20% chance to save ammo  | 8 minutes   
25	[](Archery_Potion.md "Archery") | [Archery](Archery_Potion.md "Archery Potion") | [](Archery_Potion.md "Archery Potion")[Archery Potion](Archery_Potion.md "Archery Potion") | Increases [arrow](Arrow "Arrow") damage and firing speed by 20%.  | 10% increased bow damage and 20% increased arrow speed  | 8 minutes   
26	[](Battle_Potion.md "Battle") | [Battle](Battle_Potion.md "Battle Potion") | [](Battle_Potion.md "Battle Potion")[Battle Potion](Battle_Potion.md "Battle Potion") | Doubles the spawn rate of enemies and [critters](Critters.md "Critters") and maximum amount of enemies on-screen.  | Increased enemy spawn rate  | 7 minutes   
27	[](Builder_Potion.md "Builder") | [Builder](Builder_Potion.md "Builder Potion") | [](Builder_Potion.md "Builder Potion")[Builder Potion](Builder_Potion.md "Builder Potion") | Increases placement speed by 25% and extends placement range by one tile.  | Increased placement speed and range  | 45 minutes   
28	[](Biome_Sight_Potion.md "Biome Sight") | [Biome Sight](Biome_Sight_Potion.md "Biome Sight Potion") | [](Biome_Sight_Potion.md "Biome Sight Potion")[Biome Sight Potion](Biome_Sight_Potion.md "Biome Sight Potion") | Highlights all tiles that are [Corrupted](The_Corruption.md "The Corruption"), [Crimson](Crimson "Crimson"), or [Hallowed](The_Hallow.md "The Hallow") in purple, red, and pink respectively.  | Shows the location of infected blocks  | 5 minutes   
29	[](Calming_Potion.md "Calm") | [Calm](Calming_Potion.md "Calming Potion") | [](Calming_Potion.md "Calming Potion")[Calming Potion](Calming_Potion.md "Calming Potion") | Reduces enemy spawn rate by 17%.  | Decreased enemy spawn rate  | 12 minutes   
30	[](Crate_Potion.md "Crate") | [Crate](Crate_Potion.md "Crate Potion") | [](Crate_Potion.md "Crate Potion")[Crate Potion](Crate_Potion.md "Crate Potion") | Doubles the chance of catching a [crate](Crate "Crate").  | Greater chance of fishing up a crate  | 4 minutes   
31	[](Dangersense_Potion.md "Dangersense") | [Dangersense](Dangersense_Potion.md "Dangersense Potion") | [](Dangersense_Potion.md "Dangersense Potion")[Dangersense Potion](Dangersense_Potion.md "Dangersense Potion") | Highlights hazardous [blocks](Blocks.md "Blocks") and objects like [traps](Traps.md "Traps").  | You can see nearby hazards  | 10 minutes   
32	[](Endurance_Potion.md "Endurance") | [Endurance](Endurance_Potion.md "Endurance Potion") | [](Endurance_Potion.md "Endurance Potion")[Endurance Potion](Endurance_Potion.md "Endurance Potion") | Reduces all damage taken by 10%.  | 10% reduced damage  | 4 minutes   
33	[](Well_Fed.md "Exquisitely Stuffed") | [Exquisitely Stuffed](Well_Fed.md "Well Fed") | Numerous [food](Food.md "Food") items  | Grants several major improvements of base stats, e.g. damage, defense. etc.  | Major improvements to all stats  
34	[Major improvements to all stats and increased life regeneration](Expert_Mode.md "Expert Mode") | 4–48 minutes (depending on the food item)  
35	[](Featherfall_Potion.md "Featherfall") | [Featherfall](Featherfall_Potion.md "Featherfall Potion") | [](Featherfall_Potion.md "Featherfall Potion")[Featherfall Potion](Featherfall_Potion.md "Featherfall Potion") | Grants control over the player's falling speed and negates [fall damage](Fall_damage.md "Fall damage").  | Press UP or DOWN to control speed of descent  | 10 minutes   
36	[](Fishing_Potion.md "Fishing") | [Fishing](Fishing_Potion.md "Fishing Potion") | [](Fishing_Potion.md "Fishing Potion")[Fishing Potion](Fishing_Potion.md "Fishing Potion") | Increases [Fishing Power](Fishing_Power.md "Fishing Power") by 15.  | Increased fishing power  | 8 minutes   
37	[](Flipper_Potion.md "Flipper") | [Flipper](Flipper_Potion.md "Flipper Potion") | [](Flipper_Potion.md "Flipper Potion")[Flipper Potion](Flipper_Potion.md "Flipper Potion") | [Liquids](Liquids.md "Liquids") do not impede movement speed, and allows the player to swim.  | Move like normal in water  | 8 minutes   
38	[](Gills_Potion.md "Gills") | [Gills](Gills_Potion.md "Gills Potion") | [](Gills_Potion.md "Gills Potion")[Gills Potion](Gills_Potion.md "Gills Potion") | Allows the player to breathe underwater, preventing [drowning](Drowning.md "Drowning").  | Allows you to breathe in liquids  | 4 minutes   
39	[](Gravitation_Potion.md "Gravitation") | [Gravitation](Gravitation_Potion.md "Gravitation Potion") | [](Gravitation_Potion.md "Gravitation Potion")[Gravitation Potion](Gravitation_Potion.md "Gravitation Potion") | Allows the player to invert gravity with [`▲ Up`](Game_controls.md "Game controls").  | Press UP to reverse gravity  | 3 minutes   
40	[](Heartreach_Potion.md "Heartreach") | [Heartreach](Heartreach_Potion.md "Heartreach Potion") | [](Heartreach_Potion.md "Heartreach Potion")[Heartreach Potion](Heartreach_Potion.md "Heartreach Potion") | Increases [heart](Heart.md "Heart") pickup range.  | Increased heart pickup range  | 8 minutes   
41	[](Hunter_Potion.md "Hunter") | [Hunter](Hunter_Potion.md "Hunter Potion") | [](Hunter_Potion.md "Hunter Potion")[Hunter Potion](Hunter_Potion.md "Hunter Potion") | Highlights all enemies on-screen.  | Shows the location of enemies  | 8 minutes   
42	[](Inferno_Potion.md "Inferno") | [Inferno](Inferno_Potion.md "Inferno Potion") | [](Inferno_Potion.md "Inferno Potion")[Inferno Potion](Inferno_Potion.md "Inferno Potion") | Casts a damaging ring of fire around the player.  | Nearby enemies are ignited  | 4 minutes   
43	[](Invisibility_Potion.md "Invisibility") | [Invisibility](Invisibility_Potion.md "Invisibility Potion") | [](Invisibility_Potion.md "Invisibility Potion")[Invisibility Potion](Invisibility_Potion.md "Invisibility Potion") | Turns the player invisible.  | Grants invisibility  | 3 minutes   
44	[](Ironskin_Potion.md "Ironskin") | [Ironskin](Ironskin_Potion.md "Ironskin Potion") | [](Ironskin_Potion.md "Ironskin Potion")[Ironskin Potion](Ironskin_Potion.md "Ironskin Potion") | Increases [defense](Defense.md "Defense") by 8.  | Increase defense by 8  | 8 minutes   
45	[](Lifeforce_Potion.md "Lifeforce") | [Lifeforce](Lifeforce_Potion.md "Lifeforce Potion") | [](Lifeforce_Potion.md "Lifeforce Potion")[Lifeforce Potion](Lifeforce_Potion.md "Lifeforce Potion") | Increases max health by 20%.  | 20% increased max life  | 8 minutes   
46	[](Lucky_\(buff\) "Lucky") | [Lucky](Lucky_\(buff\) "Lucky \(buff\)") | [](Lesser_Luck_Potion "Lesser Luck Potion")[Lesser Luck Potion](Lesser_Luck_Potion "Lesser Luck Potion")   
47	[](Luck_Potion "Luck Potion")[Luck Potion](Luck_Potion "Luck Potion")   
48	[](Greater_Luck_Potion "Greater Luck Potion")[Greater Luck Potion](Greater_Luck_Potion "Greater Luck Potion") | Increases [luck](Luck.md "Luck").  | You are feeling pretty lucky  | 5 minutes   
49	10 minutes   
50	15 minutes   
51	[](Magic_Power_Potion.md "Magic Power") | [Magic Power](Magic_Power_Potion.md "Magic Power Potion") | [](Magic_Power_Potion.md "Magic Power Potion")[Magic Power Potion](Magic_Power_Potion.md "Magic Power Potion") | Increases Magic damage by 20%.  | 20% increased magic damage  | 4 minutes   
52	[](Mana_Regeneration_Potion.md "Mana Regeneration") | [Mana Regeneration](Mana_Regeneration_Potion.md "Mana Regeneration Potion") | [](Mana_Regeneration_Potion.md "Mana Regeneration Potion")[Mana Regeneration Potion](Mana_Regeneration_Potion.md "Mana Regeneration Potion") | Increases mana regeneration.  | Increased mana regeneration  | 8 minutes   
53	[](Mining_Potion.md "Mining") | [Mining](Mining_Potion.md "Mining Potion") | [](Mining_Potion.md "Mining Potion")[Mining Potion](Mining_Potion.md "Mining Potion") | Increases mining speed.  | 25% increased mining speed  | 10 minutes   
54	[](Night_Owl_Potion.md "Night Owl") | [Night Owl](Night_Owl_Potion.md "Night Owl Potion") | [](Night_Owl_Potion.md "Night Owl Potion")[Night Owl Potion](Night_Owl_Potion.md "Night Owl Potion") | Improves the player's night vision and increases the radius of any available [light source](Light_source "Light source").  | Increased night vision  | 10 minutes   
55	[](Obsidian_Skin_Potion.md "Obsidian Skin") | [Obsidian Skin](Obsidian_Skin_Potion.md "Obsidian Skin Potion") | [](Obsidian_Skin_Potion.md "Obsidian Skin Potion")[Obsidian Skin Potion](Obsidian_Skin_Potion.md "Obsidian Skin Potion") | Grants invulnerability to damage from lava.  | Immune to lava  | 6 minutes   
56	[](Well_Fed.md "Plenty Satisfied") | [Plenty Satisfied](Well_Fed.md "Well Fed") | Numerous [food](Food.md "Food") items  | Grants several medium improvements of base stats, e.g. damage, defense. etc.  | Medium improvements to all stats  
57	[Medium improvements to all stats and increased life regeneration](Expert_Mode.md "Expert Mode") | 5–20 minutes (depending on the food item)  
58	[](Rage_Potion.md "Rage") | [Rage](Rage_Potion.md "Rage Potion") | [](Rage_Potion.md "Rage Potion")[Rage Potion](Rage_Potion.md "Rage Potion") | Increases critical strike chance by 10%.  | 10% increased critical chance  | 4 minutes   
59	[](Regeneration_Potion.md "Regeneration") | [Regeneration](Regeneration_Potion.md "Regeneration Potion") | [](Regeneration_Potion.md "Regeneration Potion")[Regeneration Potion](Regeneration_Potion.md "Regeneration Potion") | Increases life regeneration by 2 health per second.  | Provides life regeneration  | 8 minutes   
60	[](Shine_Potion.md "Shine") | [Shine](Shine_Potion.md "Shine Potion") | [](Shine_Potion.md "Shine Potion")[Shine Potion](Shine_Potion.md "Shine Potion") | Causes the player to glow brightly.  | Emitting light  | 10 minutes   
61	[](Sonar_Potion.md "Sonar") | [Sonar](Sonar_Potion.md "Sonar Potion") | [](Sonar_Potion.md "Sonar Potion")[Sonar Potion](Sonar_Potion.md "Sonar Potion") | Reveals the name of the catch while fishing.  | You can see what's biting your hook  | 8 minutes   
62	[](Spelunker_Potion.md "Spelunker") | [Spelunker](Spelunker_Potion.md "Spelunker Potion") | [](Spelunker_Potion.md "Spelunker Potion")[Spelunker Potion](Spelunker_Potion.md "Spelunker Potion") | Highlights [ore](Ore "Ore"), [chests](Chests.md "Chests"), and other treasure.  | Shows the location of treasure and ore  | 5 minutes   
63	[](Summoning_Potion.md "Summoning") | [Summoning](Summoning_Potion.md "Summoning Potion") | [](Summoning_Potion.md "Summoning Potion")[Summoning Potion](Summoning_Potion.md "Summoning Potion") | Increases number of maximum minions by 1.  | Increased your max number of minions by 1  | 8 minutes   
64	[](Swiftness_Potion.md "Swiftness") | [Swiftness](Swiftness_Potion.md "Swiftness Potion") | [](Swiftness_Potion.md "Swiftness Potion")[Swiftness Potion](Swiftness_Potion.md "Swiftness Potion") | Increases movement speed by 25%.  | 25% increased movement speed  | 8 minutes   
65	[](Thorns_Potion.md "Thorns") | [Thorns](Thorns_Potion.md "Thorns Potion") | [](Thorns_Potion.md "Thorns Potion")[Thorns Potion](Thorns_Potion.md "Thorns Potion") | Melee attackers take a small amount of damage upon harming the player.  | Attackers also take damage  | 8 minutes   
66	[](Titan_Potion.md "Titan") | [Titan](Titan_Potion.md "Titan Potion") | [](Titan_Potion.md "Titan Potion")[Titan Potion](Titan_Potion.md "Titan Potion") | Increases knockback of all weapons.  | Increased knockback  | 8 minutes   
67	[](Torch_God's_Flavor.md "Torch Blessing") | [Torch Blessing](Torch_God's_Flavor.md "Torch God's Flavor") | [](Torch_God's_Flavor.md "Torch God's Flavor")[Torch God's Flavor](Torch_God's_Flavor.md "Torch God's Flavor") | Converts nearby torches to match the biome.  | Nearby torches will be converted to match the biome  | 8 minutes   
68	[](Warmth_Potion.md "Warmth") | [Warmth](Warmth_Potion.md "Warmth Potion") | [](Warmth_Potion.md "Warmth Potion")[Warmth Potion](Warmth_Potion.md "Warmth Potion") | Reduces damage from cold-themed enemies.  | Reduced damage from cold sources  | 15 minutes   
69	[](Water_Walking_Potion.md "Water Walking") | [Water Walking](Water_Walking_Potion.md "Water Walking Potion") | [](Water_Walking_Potion.md "Water Walking Potion")[Water Walking Potion](Water_Walking_Potion.md "Water Walking Potion") | Allows the player to walk on [liquids](Liquids.md "Liquids").  | Press DOWN to enter water  | 10 minutes   
70	[](Wrath_Potion.md "Wrath") | [Wrath](Wrath_Potion.md "Wrath Potion") | [](Wrath_Potion.md "Wrath Potion")[Wrath Potion](Wrath_Potion.md "Wrath Potion") | Increases damage dealt with weapons by 10%.  | 10% increased damage  | 4 minutes   
71	[](Well_Fed.md "Well Fed") | [Well Fed](Well_Fed.md "Well Fed") | Numerous [food](Food.md "Food") items  | Grants several minor improvements of base stats, e.g. damage, defense. etc.  | Minor improvements to all stats  
72	[Minor improvements to all stats and increased life regeneration](Expert_Mode.md "Expert Mode") | 10–45 minutes(depending on the food item)  
73	[](Flask_of_Party.md "Weapon Imbue: Confetti") | [Weapon Imbue: Confetti](Flask_of_Party.md "Flask of Party") | [](Flask_of_Party.md "Flask of Party")[Flask of Party](Flask_of_Party.md "Flask of Party") | Melee and [whip](Whips.md "Whips") attacks cause bursts of confetti.  | Melee attacks cause confetti to appear  | 20 minutes   
74	[](Flask_of_Cursed_Flames.md "Weapon Imbue: Cursed Flames") | [Weapon Imbue: Cursed Flames](Flask_of_Cursed_Flames.md "Flask of Cursed Flames") | [](Flask_of_Cursed_Flames.md "Flask of Cursed Flames")[Flask of Cursed Flames](Flask_of_Cursed_Flames.md "Flask of Cursed Flames") | Melee and [whip](Whips.md "Whips") attacks inflict the [Cursed Inferno](Cursed_Inferno.md "Cursed Inferno") debuff on enemies.  | Melee attacks inflict enemies with cursed flames  | 20 minutes   
75	[](Flask_of_Fire.md "Weapon Imbue: Fire") | [Weapon Imbue: Fire](Flask_of_Fire.md "Flask of Fire") | [](Flask_of_Fire.md "Flask of Fire")[Flask of Fire](Flask_of_Fire.md "Flask of Fire") | Melee and [whip](Whips.md "Whips") attacks inflict the [On Fire!](On_Fire!.md "On Fire!") debuff on enemies.  | Melee attacks set enemies on fire  | 20 minutes   
76	[](Flask_of_Gold.md "Weapon Imbue: Gold") | [Weapon Imbue: Gold](Flask_of_Gold.md "Flask of Gold") | [](Flask_of_Gold.md "Flask of Gold")[Flask of Gold](Flask_of_Gold.md "Flask of Gold") | Melee and [whip](Whips.md "Whips") attacks inflict the [Midas](Midas.md "Midas") debuff on enemies.  | Melee attacks make enemies drop more gold  | 20 minutes   
77	[](Flask_of_Ichor.md "Weapon Imbue: Ichor") | [Weapon Imbue: Ichor](Flask_of_Ichor.md "Flask of Ichor") | [](Flask_of_Ichor.md "Flask of Ichor")[Flask of Ichor](Flask_of_Ichor.md "Flask of Ichor") | Melee and [whip](Whips.md "Whips") attacks inflict the [Ichor debuff](Ichor_debuff "Ichor debuff") on enemies.  | Melee attacks decrease enemies defense  | 20 minutes   
78	[](Flask_of_Nanites.md "Weapon Imbue: Nanites") | [Weapon Imbue: Nanites](Flask_of_Nanites.md "Flask of Nanites") | [](Flask_of_Nanites.md "Flask of Nanites")[Flask of Nanites](Flask_of_Nanites.md "Flask of Nanites") | Melee and [whip](Whips.md "Whips") attacks inflict the [Confused](Confused.md "Confused") debuff on enemies.  | Melee attacks confuse enemies  | 20 minutes   
79	[](Flask_of_Poison.md "Weapon Imbue: Poison") | [Weapon Imbue: Poison](Flask_of_Poison.md "Flask of Poison") | [](Flask_of_Poison.md "Flask of Poison")[Flask of Poison](Flask_of_Poison.md "Flask of Poison") | Melee and [whip](Whips.md "Whips") attacks inflict the [Poisoned](Poisoned.md "Poisoned") debuff on enemies.  | Melee attacks poison enemies  | 20 minutes   
80	[](Flask_of_Venom.md "Weapon Imbue: Acid Venom") | [Weapon Imbue: Acid Venom](Flask_of_Venom.md "Flask of Venom") | [](Flask_of_Venom.md "Flask of Venom")[Flask of Venom](Flask_of_Venom.md "Flask of Venom") | Melee and [whip](Whips.md "Whips") attacks inflict the [Acid Venom](Acid_Venom.md "Acid Venom") debuff on enemies.  | Melee attacks inflict acid venom on your targets  | 20 minutes   
81	  
82	## Equipment
83	
84	These buffs are provided naturally by equipment, either permanently or under certain circumstances. 
85	
86	Icon  | Name  | Source  | Effect  | Tooltip  | Duration   
87	---|---|---|---|---|---  
88	[](Cool_Whip.md "A Nice Buff") | [A Nice Buff](Cool_Whip.md "Cool Whip") | Striking an enemy with [](Cool_Whip.md "Cool Whip")[Cool Whip](Cool_Whip.md "Cool Whip") | Summons a temporary flying snowflake minion that attacks nearby enemies  | Summons a snowflake to fight for you  | 3 seconds   
89	[](Ballista_Panic!.md "Ballista Panic!") | [Ballista Panic!](Ballista_Panic!.md "Ballista Panic!") | When hit while wearing full [Squire armor](Squire_armor.md "Squire armor") or full [Valhalla Knight armor](Valhalla_Knight_armor.md "Valhalla Knight armor") | Reduces attack cooldown of [Ballista sentry summons](Ballista_sentry_summons.md "Ballista sentry summons") to 1/0.5 seconds  | Your ballistas rapidly shoot in panic!  | 5 seconds   
90	[](Beetle_Endurance.md "Beetle Endurance") | [Beetle Endurance](Beetle_Endurance.md "Beetle Endurance") | When hit while wearing full [Beetle armor](Beetle_armor.md "Beetle armor") with [](Beetle_Shell "Beetle Shell")[Beetle Shell](Beetle_Shell "Beetle Shell") | Reduces all damage taken by 15%/30%/45%.  | Absorbs 15% of damage taken  
91	Absorbs 30% of damage taken  
92	Absorbs 45% of damage taken  | While not receiving damage   
93	[](Beetle_Might.md "Beetle Might") | [Beetle Might](Beetle_Might.md "Beetle Might") | Damaging an enemy while wearing [Beetle armor](Beetle_armor.md "Beetle armor") with [](Beetle_Scale_Mail "Beetle Scale Mail")[Beetle Scale Mail](Beetle_Scale_Mail "Beetle Scale Mail") | 10%/20%/30% increased melee damage and speed.  | Melee damage and speed increase by 10%  
94	Melee damage and speed increase by 20%  
95	Melee damage and speed increase by 30%  | While in combat   
96	[](Damage_Booster.md "Damage Nebula") | [Damage Nebula](Damage_Booster.md "Damage Booster") | Striking an enemy while wearing full [Nebula armor](Nebula_armor.md "Nebula armor") | Increases damage by 15%/30%/45%.  | 15% increased damage  
97	30% increased damage  
98	45% increased damage  | 8 seconds   
99	[](Durendal.md "Durendal's Blessing") | [Durendal's Blessing](Durendal.md "Durendal") | Striking an enemy with [](Durendal.md "Durendal")[Durendal](Durendal.md "Durendal") | Increases whip speed by 25%.  | Whip speed is increased  | 3 seconds   
100	[](Dark_Harvest.md "Harvest Time") | [Harvest Time](Dark_Harvest.md "Dark Harvest") | Striking an enemy with [](Dark_Harvest.md "Dark Harvest")[Dark Harvest](Dark_Harvest.md "Dark Harvest") | Increases whip speed by 35%.  | Whip speed is increased  | 3 seconds   
101	[](Kites.md "High Spirits") | [High Spirits](Kites.md "Kites") | Flying a [](Kites.md "Kites")[Kites](Kites.md "Kites") | Slightly increases Movement Speed, Mining Speed and Placement Speed.  | Slightly increased movement speed, mining speed, and placement speed  | 10 Seconds for every Second flying a [](Kites.md "Kites")[Kites](Kites.md "Kites") (Max 12 Minutes 1 Second)   
102	[](Hallowed_armor.md "Holy Protection") | [Holy Protection](Hallowed_armor.md "Hallowed armor") | Striking an enemy while wearing full [Hallowed armor](Hallowed_armor.md "Hallowed armor") | Allows the player to dodge the next attack dealt by an enemy.  | You will dodge the next attack  | 30 seconds (or until dodge effect is triggered)   
103	[](Frozen_Turtle_Shell.md "Ice Barrier") | [Ice Barrier](Frozen_Turtle_Shell.md "Frozen Turtle Shell") | [](Frozen_Turtle_Shell.md "Frozen Turtle Shell")[Frozen Turtle Shell](Frozen_Turtle_Shell.md "Frozen Turtle Shell") / [](Frozen_Shield.md "Frozen Shield")[Frozen Shield](Frozen_Shield.md "Frozen Shield") | Grants 25% damage reduction.[1] | Damage taken is reduced by 25%  | While below 50% health   
104	[](Snapthorn.md "Jungle's Fury") | [Jungle's Fury](Snapthorn.md "Snapthorn") | Striking an enemy with the [](Snapthorn.md "Snapthorn")[Snapthorn](Snapthorn.md "Snapthorn") | Increases whip speed by 12%.  | Whip speed is increased  | 3 seconds   
105	[](Chlorophyte_armor.md "Leaf Crystal") | [Leaf Crystal](Chlorophyte_armor.md "Chlorophyte armor") | Wearing full [Chlorophyte armor](Chlorophyte_armor.md "Chlorophyte armor") | Summons a leaf crystal above the player that shoots at enemies.  | Shoots crystal leaves at nearby enemies  | Infinite   
106	[](Life_Drain.md "Life Drain") | [Life Drain](Life_Drain.md "Life Drain") | [](Life_Drain.md "Life Drain")[Life Drain](Life_Drain.md "Life Drain") | Increases life regeneration.  | Increased life regeneration  | While attacking an enemy that is not immune to its debuff   
107	[](Life_Booster.md "Life Nebula") | [Life Nebula](Life_Booster.md "Life Booster") | Striking an enemy while wearing full [Nebula armor](Nebula_armor.md "Nebula armor") | Increases health regeneration by 5/10/15 per second.  | Increased life regeneration  | 8 seconds   
108	[](Mana_Booster.md "Mana Nebula") | [Mana Nebula](Mana_Booster.md "Mana Booster") | Striking an enemy while wearing full [Nebula armor](Nebula_armor.md "Nebula armor") | Increases mana regeneration by 10/20/30 per second.  | Increased mana regeneration  | 8 seconds   
109	[](Neptune's_Shell.md "Merfolk") | [Merfolk](Neptune's_Shell.md "Neptune's Shell") | [](Neptune's_Shell.md "Neptune's Shell")[Neptune's Shell](Neptune's_Shell.md "Neptune's Shell") / [](Moon_Shell.md "Moon Shell")[Moon Shell](Moon_Shell.md "Moon Shell") / [](Celestial_Shell.md "Celestial Shell")[Celestial Shell](Celestial_Shell.md "Celestial Shell") | Turns the player into a merfolk upon entering water, allowing infinite breathing and improved swimming.  | Can breathe and move easily underwater  | While underwater   
110	[](Panic_Necklace.md "Panic!") | [Panic!](Panic_Necklace.md "Panic Necklace") | When hit while having [](Panic_Necklace.md "Panic Necklace")[Panic Necklace](Panic_Necklace.md "Panic Necklace") / [](Sweetheart_Necklace.md "Sweetheart Necklace")[Sweetheart Necklace](Sweetheart_Necklace.md "Sweetheart Necklace") equipped.  | Increases movement speed by 100%.  | Movement speed is increased  | 5 seconds   
111	[](Palladium_armor.md "Rapid Healing") | [Rapid Healing](Palladium_armor.md "Palladium armor") | After striking an enemy while wearing full [Palladium armor](Palladium_armor.md "Palladium armor") | Heals 15 health over time.  | Life regeneration is greatly increased  | 5 seconds   
112	[](Titanium_armor.md "Titanium Barrier") | [Titanium Barrier](Titanium_armor.md "Titanium armor") | After striking an enemy while wearing full [Titanium armor](Titanium_armor.md "Titanium armor").  | Titanium shards spawn and rotate around the player, dealing damage to enemies that come into contact with them.  | Defensive shards surround you  | 10 seconds   
113	[](Solar_Flare_armor.md "Solar Blaze")[](Solar_Flare_armor.md "Solar Blaze")[](Solar_Flare_armor.md "Solar Blaze") | [Solar Blaze](Solar_Flare_armor.md "Solar Flare armor") | Not taking damage while wearing full [Solar Flare armor](Solar_Flare_armor.md "Solar Flare armor"), up to 3 "charges"  | Reduces all damage taken by 20%. Grants the ability to dash for consuming a charge. Taking damage depletes one charge.  | Absorbs 20% of damage taken, repel enemies when taking damage  | Infinite, until damaged 3 times   
114	[](Stardust_armor.md "Stardust Guardian") | [Stardust Guardian](Stardust_armor.md "Stardust armor") | Wearing full [Stardust armor](Stardust_armor.md "Stardust armor") | Causes a unique Stardust Guardian minion to follow the player.  | The stardust guardian will protect you  | Infinite   
115	[](Striking_Moment.md "Striking Moment") | [Striking Moment](Striking_Moment.md "Striking Moment") | Using [](Brand_of_the_Inferno.md "Brand of the Inferno")[Brand of the Inferno](Brand_of_the_Inferno.md "Brand of the Inferno") with a shield or using [](Sergeant_United_Shield.md "Sergeant United Shield")[Sergeant United Shield](Sergeant_United_Shield.md "Sergeant United Shield") | Damage multiplied by 5 for next melee attack landed.  | 400% increased damage for next melee strike  | 5 seconds (or until melee strike hits target)   
116	[](Moon_Charm.md "Werewolf") | [Werewolf](Moon_Charm.md "Moon Charm") | [](Moon_Charm.md "Moon Charm")[Moon Charm](Moon_Charm.md "Moon Charm") / [](Moon_Shell.md "Moon Shell")[Moon Shell](Moon_Shell.md "Moon Shell") / [](Celestial_Shell.md "Celestial Shell")[Celestial Shell](Celestial_Shell.md "Celestial Shell") | Gives improvements to physical abilities, as well as giving the player a cosmetic werewolf skin.  | Physical abilities are increased  | During the [night](Night "Night")  
117	  
118	## Activated furniture
119	
120	These buffs are provided upon right-clicking particular placed furniture. 
121	
122	Icon  | Name  | Source  | Effect  | Tooltip  | Duration   
123	---|---|---|---|---|---  
124	[](Alchemy_Flask.md "Alchemic Enhancement") | [Alchemic Enhancement](Alchemy_Flask.md "Alchemy Flask") | [](Alchemy_Flask.md "Alchemy Flask")[Alchemy Flask](Alchemy_Flask.md "Alchemy Flask") | Increases newly received buff potion durations by 20%.  | Fresh buffs last longer  | Infinite   
125	[](Ammo_Box.md "Ammo Box") | [Ammo Box](Ammo_Box.md "Ammo Box") | [](Ammo_Box.md "Ammo Box")[Ammo Box](Ammo_Box.md "Ammo Box") | Grants a 20% chance [not to consume ammo](Ammo_conservation.md "Ammo conservation").  | 20% chance to save ammo  | Infinite   
126	[](Bewitching_Table.md "Bewitched") | [Bewitched](Bewitching_Table.md "Bewitching Table") | [](Bewitching_Table.md "Bewitching Table")[Bewitching Table](Bewitching_Table.md "Bewitching Table") | Increases number of maximum minions by 1.  | Increased your max number of minions by 1  | Infinite   
127	[](Crystal_Ball.md "Clairvoyance") | [Clairvoyance](Crystal_Ball.md "Crystal Ball") | [](Crystal_Ball.md "Crystal Ball")[Crystal Ball](Crystal_Ball.md "Crystal Ball") | Grants +20 maximum mana, +5% magic damage, +2% magic critical strike chance, and −2% mana usage.  | Magic powers are increased  | Infinite   
128	[](Sharpening_Station.md "Sharpened") | [Sharpened](Sharpening_Station.md "Sharpening Station") | [](Sharpening_Station.md "Sharpening Station")[Sharpening Station](Sharpening_Station.md "Sharpening Station") | Increases melee weapons armor penetration by 12.  | Melee weapons have armor penetration  | Infinite   
129	[](War_Table.md "Strategist") | [Strategist](War_Table.md "War Table") | [](War_Table.md "War Table")[War Table](War_Table.md "War Table") | Increases number of maximum sentries by 1.  | Increased your max number of sentries by 1  | Infinite   
130	[](Slice_of_Cake.md "Sugar Rush") | [Sugar Rush](Slice_of_Cake.md "Slice of Cake") | [](Slice_of_Cake.md "Slice of Cake")[Slice of Cake](Slice_of_Cake.md "Slice of Cake") | Increases the player's movement and mining speed by 20%.  | 20% increased movement and mining speed  | 2 minutes   
131	  
132	## Environmental
133	
134	These buffs are provided by being in range of particular placed furniture, blocks, or NPCs. [Banners](Banners_\(enemy\) "Banners \(enemy\)"), as well as static effects from objects like Peace Candle and Happy!, affect all players within a rectangular area of 170×125[2] tiles centered on the object. Since they cannot be canceled by right-clicking them, the only way to remove the buff is to leave the area (with the exception of honey). 
135	
136	Icon  | Name  | Source  | Effect  | Tooltip  | Duration   
137	---|---|---|---|---|---  
138	[](Campfires.md "Cozy Fire") | [Cozy Fire](Campfires.md "Campfires") | [](Campfire "Campfire")[Campfire](Campfire "Campfire")  
139	[](Fireplace.md "Fireplace")[Fireplace](Fireplace.md "Fireplace") | Increases life regeneration by 0.5 HP/s, and multiplies current healing rate by 1.1.  | Life regen is slightly increased  | Infinite while in the vicinity of a Campfire or Fireplace   
140	[](Dryad's_Blessing.md "Dryad's Blessing") | [Dryad's Blessing](Dryad's_Blessing.md "Dryad's Blessing") | [](Dryad.md "Dryad")[Dryad](Dryad.md "Dryad") | Increases the player's defense by 8 and increases life regeneration by 3 HP/s.  | The power of nature protects you  | Infinite while inside the Dryad's leaf barrier   
141	[](Sunflower.md "Happy!") | [Happy!](Sunflower.md "Sunflower") | [](Sunflower.md "Sunflower")[Sunflower](Sunflower.md "Sunflower") | Increases movement speed by 10% and reduces enemy spawns by 17%.  | Movement speed increased and monster spawns reduced  | Infinite while in the vicinity of a Sunflower   
142	[](Heart_Lantern.md "Heart Lamp") | [Heart Lamp](Heart_Lantern.md "Heart Lantern") | [](Heart_Lantern.md "Heart Lantern")[Heart Lantern](Heart_Lantern.md "Heart Lantern") | Increases life regeneration by 1 HP/s.  | Life regen is increased  | Infinite while in the vicinity of a Heart Lantern   
143	[](Honey_\(buff\) "Honey") | [Honey](Honey_\(buff\) "Honey \(buff\)") | [](Honey.md "Honey")[Honey](Honey.md "Honey") | Increases life regeneration by 1 HP/s and multiplies natural regeneration by 3.  | Life regeneration is increased  | Infinite while in honey, 30 seconds after stepping out of the honey   
144	[](Peace_Candle.md "Peace Candle") | [Peace Candle](Peace_Candle.md "Peace Candle") | [](Peace_Candle.md "Peace Candle")[Peace Candle](Peace_Candle.md "Peace Candle") | Decreases enemy spawn rate by 23%, and maximum enemies on-screen by 30%.  | Decreased monster spawn rate  | Infinite while in the vicinity of a Peace Candle   
145	[](Star_in_a_Bottle.md "Star in a Bottle") | [Star in a Bottle](Star_in_a_Bottle.md "Star in a Bottle") | [](Star_in_a_Bottle.md "Star in a Bottle")[Star in a Bottle](Star_in_a_Bottle.md "Star in a Bottle") | Increases mana regeneration by about 2 MP/s.  | Increased mana regeneration  | Infinite while in the vicinity of a Star in a Bottle   
146	[](Bast_Statue.md "The Bast Defense") | [The Bast Defense](Bast_Statue.md "Bast Statue") | [](Bast_Statue.md "Bast Statue")[Bast Statue](Bast_Statue.md "Bast Statue") | Increases defense by 5.  | Defense is increased by 5  | Infinite while in the vicinity of a Bast Statue   
147	  
148	## Summons
149	
150	Aside from the normal buffs, some buffs provide the player with a [minion](Minion "Minion"). Unlike other buffs, they last until the player dies, cancels the buff, or leaves the current world. 

```


---

## 🤖 Assistant · 2026-08-12T18:26:14.680Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This index is extremely valuable. Now I need:
1. Buff duration merge/refresh rules in Buffs.md — the section after the tables (Notes). Let me grep for it.
2. Debuff immunity accessories (Bezoar, Medicated Bandage, Adhesive Bandage) — those are on their item pages. The task says "Buffs.md — report what it says about ... debuff immunity accessories". Hmm, but Bezoar etc. are item pages. Let me check Buffs.md notes section and also read Bezoar.md, Medicated_Bandage.md, Adhesive_Bandage.md, Armor_Polish, Vitamins, Nazar etc.

Let me read Buffs.md notes section.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:26:15.117Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && grep -n '^## \\|^### ' Buffs.md | head -40",
 "description": "List Buffs.md section headers"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:26:15.146Z

**📎 ToolResult**

```
18:## Consumables
82:## Equipment
118:## Activated furniture
132:## Environmental
148:## Summons
189:## Mounts
253:## Notes
257:## Achievements
275:## See also
280:## History
347:## Footnotes

```


---

## 🤖 Assistant · 2026-08-12T18:26:16.597Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Buffs.md",
 "limit": 60,
 "offset": 253
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:26:16.601Z

**📎 ToolResult**

```
253	## Notes
254	
255	  * [](Switch_version.md "Nintendo Switch") The player can also double tap a buff on the touch screen to deactivate it early, but only in handheld mode.
256	
257	## Achievements
258	
259	[](Achievements#The_Cavalry "Achievements")
260	
261	**[The Cavalry](Achievements#The_Cavalry "Achievements")**  • _“Equip a mount.”_
262	
263	Equip your first [mount](Mount "Mount").
264	
265	Category:  Collector
266	
267	[](Achievements#You_and_What_Army? "Achievements")
268	
269	**[You and What Army?](Achievements#You_and_What_Army? "Achievements")**  • _“Command nine summoned minions simultaneously.”_
270	
271	Have nine [minions](Minion "Minion") summoned at the same time.
272	
273	Category:  Challenger
274	
275	## See also
276	
277	  * [Pets](Pets.md "Pets")
278	  * [Permanent boosters](Permanent_boosters.md "Permanent boosters")
279	
280	## History
281	
282	[ Desktop version](Desktop_version_history.md "Desktop version history")
283	
284	  * [Desktop 1.4.5.0](Desktop_1.4.5.0 "Desktop 1.4.5.0"): [Alchemic Enhancement](Alchemic_Enhancement "Alchemic Enhancement"), [Torch Blessing](Torch_Blessing "Torch Blessing"), and [High Spirits](High_Spirits "High Spirits") buffs introduced.
285	
286	  * [Desktop 1.4.4](Desktop_1.4.4 "Desktop 1.4.4"): 
287	    * [Biome Sight](Biome_Sight "Biome Sight") buff added.
288	    * Player buff/debuff maximum increased from 22 to 44.
289	
290	  * [Desktop 1.4.0.5](Desktop_1.4.0.5 "Desktop 1.4.0.5"): 
291	    * Buff effects should now properly follow enemies affected by [NPC](NPC "NPC") smoothing.
292	    * Fixed a bug where buff order was not recalculated properly under certain circumstances, leaving empty spaces.
293	    * Fixed some buff icons having white space on them instead of transparency.
294	
295	  * [Desktop 1.4.0.1](Desktop_1.4.0.1 "Desktop 1.4.0.1"): 
296	    * [Sugar Rush](Sugar_Rush "Sugar Rush") buff added.
297	    * Buff durations timer display now rounds up instead of down.
298	
299	  * [Desktop 1.3.2](Desktop_1.3.2 "Desktop 1.3.2"): Fixed extremely long-timed buffs not updating properly in [Multiplayer](Multiplayer.md "Multiplayer").
300	
301	  * [Desktop 1.3.0.1](Desktop_1.3.0.1 "Desktop 1.3.0.1"): 
302	    * [Happy!](Happy! "Happy!"), [Star in a Bottle](Star_in_a_Bottle.md "Star in a Bottle"), [Peace Candle](Peace_Candle.md "Peace Candle") buffs introduced.
303	    * The [Dryad](Dryad.md "Dryad") can now cast a defensive buff.
304	    * Weapon Imbues now last 20 minutes and persist through death.
305	
306	  * [Desktop 1.2.4.1](Desktop_1.2.4.1 "Desktop 1.2.4.1"): Fixed bug where upon loading the player might sometimes have empty spaces between their buffs.
307	
308	  * [Desktop 1.2.2](Desktop_1.2.2 "Desktop 1.2.2"): Player buff/debuff maximum increased from 10 to 22.
309	
310	  * [Desktop 1.2.1.2](Desktop_1.2.1.2 "Desktop 1.2.1.2"): [Heart Lamp (buff)](Heart_Lamp_\(buff\) "Heart Lamp \(buff\)") and [Campfire (buff)](Campfire_\(buff\) "Campfire \(buff\)") introduced.
311	
312	  * [Desktop 1.2.1](Desktop_1.2.1 "Desktop 1.2.1"): [Pumpkin Pie](Pumpkin_Pie.md "Pumpkin Pie") also grants [Well Fed](Well_Fed.md "Well Fed").

```


---

## 🤖 Assistant · 2026-08-12T18:26:19.710Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Buffs.md does NOT contain buff duration merge/refresh rules explicitly. The merge/refresh rule ("re-applying a buff while active does not stack, only refreshes duration"; also "buffs with different names from same item don't stack") is probably on individual potion pages or on "Buffs" notes... Actually the buff stacking rules are on the Potions page or on "Buffs" — let me search for "re-applied" / "refreshed" / "does not stack" across the wiki.

Also immunity accessories: Bezoar etc. Let me search.

Let me do parallel greps.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:26:20.321Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && grep -rn -iE 're-appl|reappl|refresh' --include='*.md' Buffs.md Debuffs.md Potions.md Quick_Buff.md Permanent_buffs.md 2>/dev/null | head -20",
 "description": "Search for buff refresh rules"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:26:20.349Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-12T18:26:21.188Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && ls | grep -iE 'Bezoar|Medicated_Bandage|Adhesive_Bandage|Armor_Polish|Vitamins|Nazar|Megaphone|Fast_Clock|Trifold_Map|Blindfold|Hand_Warm|Pocket_Mirror|Ankh'",
 "description": "Find immunity accessory pages"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:26:21.241Z

**📎 ToolResult**

```
Adhesive_Bandage
Adhesive_Bandage.md
Ankh_Banner.md
Ankh_Charm
Ankh_Charm.md
Ankh_Shield
Ankh_Shield.md
Ankh.md
Ankhumulation_Complete.md
Armor_Polish
Armor_Polish.md
Bezoar
Bezoar.md
Blindfold
Blindfold.md
Fast_Clock
Fast_Clock.md
Guide_Crafting_an_Ankh_Shield.md
Hand_Warmer.md
Legacy_Ankh_Charm
Legacy_Ankh_Charm.md
Legacy_Ankh_Shield
Legacy_Ankh_Shield.md
Legacy_Blindfold.md
Legacy_Megaphone.md
Legacy_Nazar.md
Legacy_Trifold_Map.md
Medicated_Bandage
Medicated_Bandage.md
Megaphone
Megaphone.md
Nazar
Nazar.md
Pocket_Mirror.md
Trifold_Map
Trifold_Map.md
Vitamins
Vitamins.md

```


---

## 🤖 Assistant · 2026-08-12T18:26:26.298Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
No refresh/merge rules found on Buffs.md. The merge/stacking rule is probably on potion pages: "Using another ... Potion while the buff is active will not stack the effect, but will refresh the duration" — hmm, actually I recall the wiki's Potion pages don't say that. Actually the rule about buffs not stacking and only the longest-duration instance applying might be described in "Buffs" page in the original wiki... The mirror's Buffs.md notes only has the Switch note. So I should report that Buffs.md does NOT state merge/refresh rules, but I can check individual potion pages for such statements.

Let me grep potion pages for "stack".

Also need to read immunity accessory pages. Let me grep the relevant sections from Bezoar.md, Medicated_Bandage.md, Adhesive_Bandage.md, Armor_Polish.md, Vitamins.md, Nazar.md, Megaphone.md, Fast_Clock.md, Trifold_Map.md, Blindfold.md, Hand_Warmer.md, Ankh_Charm.md, Pocket_Mirror.md.

These files are big (nav boilerplate). Let me read the top ~40 lines of each — the info box lists "Grants immunity to X".

Let me do it in parallel batches with grep for the immunity lines instead.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:26:27.129Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && for f in Bezoar Medicated_Bandage Adhesive_Bandage Armor_Polish Vitamins Nazar Megaphone Fast_Clock Trifold_Map Blindfold Hand_Warmer Pocket_Mirror Ankh_Charm Ankh_Shield; do echo \"=== $f ===\"; grep -n -iE 'Grants immunity|immunity to' \"$f.md\" | head -4; done",
 "description": "Extract immunity lines from accessories"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:26:31.081Z

**📎 ToolResult**

```
=== Bezoar ===
15:[Tooltip](Tooltips.md "Tooltips")|  _Grants immunity to Poisoned_  
36:The **Bezoar** is a [pre-Hardmode](Pre-Hardmode.md "Pre-Hardmode") [immunity accessory](Immunity_accessory "Immunity accessory") that grants the player immunity to the [Poisoned](Poisoned.md "Poisoned") [debuff](Debuff "Debuff"). It has a 1/100 (1%) / [199/10000 (1.99%)](Expert_Mode.md "Expert Mode") chance to drop from [Hornets](Hornet.md "Hornet"), [Moss Hornets](Moss_Hornet.md "Moss Hornet"), and [Toxic Sludges](Toxic_Sludge.md "Toxic Sludge"). 
68:  * It does not grant immunity to [Acid Venom](Acid_Venom.md "Acid Venom"), the stronger version of Poisoned.
=== Medicated_Bandage ===
15:[Tooltip](Tooltips.md "Tooltips")|  _Grants immunity to Poisoned and Bleeding_  
22:The **Medicated Bandage** is an [immunity accessory](Immunity_accessories.md "Immunity accessories") that combines the functions of the [Adhesive Bandage](Adhesive_Bandage.md "Adhesive Bandage") and the [Bezoar](Bezoar.md "Bezoar"). This item grants immunity to any [Bleeding](Bleeding.md "Bleeding") and [Poison](Poisoned.md "Poisoned") [debuffs](Debuff "Debuff"). 
=== Adhesive_Bandage ===
15:[Tooltip](Tooltips.md "Tooltips")|  _Grants immunity to Bleeding_  
36:The **Adhesive Bandage** is an [immunity accessory](Immunity_accessory "Immunity accessory") that grants the player immunity to the [Bleeding](Bleeding.md "Bleeding") [debuff](Debuff "Debuff"). It has a 1/100 (1%) / [199/10000 (1.99%)](Expert_Mode.md "Expert Mode") chance to drop from [Rusty Armored Bones](Rusty_Armored_Bones.md "Rusty Armored Bones"), [Werewolves](Werewolves "Werewolves"), and [Angler Fish](Angler_Fish.md "Angler Fish"). 
=== Armor_Polish ===
15:[Tooltip](Tooltips.md "Tooltips")|  _Grants immunity to Broken Armor_  
35:The **Armor Polish** is a [Hardmode](Hardmode.md "Hardmode") [immunity accessory](Immunity_accessory "Immunity accessory") that grants the player immunity to the [Broken Armor](Broken_Armor.md "Broken Armor") [debuff](Debuff "Debuff"). It has a 1/100 (1%) / [199/10000 (1.99%)](Expert_Mode.md "Expert Mode") chance to drop from [Armored Skeletons](Armored_Skeleton.md "Armored Skeleton") and [Blue Armored Bones](Blue_Armored_Bones.md "Blue Armored Bones"). 
=== Vitamins ===
15:[Tooltip](Tooltips.md "Tooltips")|  _Grants immunity to Weakness_  
35:**Vitamins** are a [Hardmode](Hardmode.md "Hardmode") [immunity accessory](Immunity_accessory "Immunity accessory") that grants the player immunity to the [Weak](Weak.md "Weak") [debuff](Debuff "Debuff"). It has a 1/100 (1%) / [199/10000 (1.99%)](Expert_Mode.md "Expert Mode") chance to drop from [Corruptors](Corruptor.md "Corruptor") and [Floaty Grosses](Floaty_Gross.md "Floaty Gross"). 
=== Nazar ===
20:[Tooltip](Tooltips.md "Tooltips")|  _Grants immunity to Cursed_  
43:The **Nazar** is a [pre-Hardmode](Pre-Hardmode.md "Pre-Hardmode"), post-[Skeletron](Skeletron.md "Skeletron") [immunity accessory](Immunity_accessory "Immunity accessory") that grants the player immunity to the [Cursed](Cursed.md "Cursed") [debuff](Debuff "Debuff"). It has a 1/100 (1%) / [199/10000 (1.99%)](Expert_Mode.md "Expert Mode") chance to drop from [Cursed Skulls](Cursed_Skull.md "Cursed Skull"), [Giant Cursed Skulls](Giant_Cursed_Skull.md "Giant Cursed Skull"), [Cursed Hammers](Cursed_Hammer.md "Cursed Hammer"), [Crimson Axes](Crimson_Axe.md "Crimson Axe"), and [Enchanted Swords](Enchanted_Sword_\(NPC\) "Enchanted Sword \(NPC\)"). 
=== Megaphone ===
20:[Tooltip](Tooltips.md "Tooltips")|  _Grants immunity to Silenced_  
42:The **Megaphone** is an [immunity accessory](Immunity_accessory "Immunity accessory") that grants the player immunity to the [Silenced](Silenced.md "Silenced") [debuff](Debuff "Debuff"). It has a 1/100 (1%) / [199/10000 (1.99%)](Expert_Mode.md "Expert Mode") chance to drop from [Pixies](Pixie.md "Pixie"), [Green Jellyfish](Green_Jellyfish "Green Jellyfish"), [Dark Mummies](Dark_Mummy.md "Dark Mummy"), and [Blood Mummies](Blood_Mummy.md "Blood Mummy"). 
=== Fast_Clock ===
15:[Tooltip](Tooltips.md "Tooltips")|  _Grants immunity to Slow_  
36:The **Fast Clock** is a [Hardmode](Hardmode.md "Hardmode") [immunity accessory](Immunity_accessory "Immunity accessory") that grants the player immunity to the [Slow](Slow.md "Slow") [debuff](Debuff "Debuff"). It has a 1/100 (1%) / [199/10000 (1.99%)](Expert_Mode.md "Expert Mode") chance to drop from [Pixies](Pixie.md "Pixie"), regular [Mummies](Mummies.md "Mummies"), and [Wraiths](Wraith.md "Wraith"). 
=== Trifold_Map ===
20:[Tooltip](Tooltips.md "Tooltips")|  _Grants immunity to Confusion_  
41:The **Trifold Map** is a [Hardmode](Hardmode.md "Hardmode") [immunity accessory](Immunity_accessory "Immunity accessory") that grants the player immunity to the [Confused](Confused.md "Confused") [debuff](Debuff "Debuff"). It has a 1/100 (1%) / [199/10000 (1.99%)](Expert_Mode.md "Expert Mode") chance to drop from [Clowns](Clown.md "Clown"), [Giant Bats](Giant_Bat.md "Giant Bat"), and [Light Mummies](Light_Mummy.md "Light Mummy"). 
=== Blindfold ===
20:[Tooltip](Tooltips.md "Tooltips")|  _Grants immunity to Darkness_  
44:The **Blindfold** is a [Hardmode](Hardmode.md "Hardmode") [immunity accessory](Immunity_accessory "Immunity accessory") that grants the player immunity to the [Darkness](Darkness.md "Darkness") [debuff](Debuff "Debuff"). It has a 1/100 (1%) / [199/10000 (1.99%)](Expert_Mode.md "Expert Mode") chance to drop from [Corrupt Slimes](Corrupt_Slime.md "Corrupt Slime"), [Slimelings](Slimeling.md "Slimeling"), [Crimslimes](Crimslime.md "Crimslime"), [Dark Mummies](Dark_Mummy.md "Dark Mummy"), and [Blood Mummies](Blood_Mummies.md "Blood Mummies"). 
=== Hand_Warmer ===
22:[Tooltip](Tooltips.md "Tooltips")|  _Grants immunity to Chilled and Frozen_  
42:The **Hand Warmer** is a [pre-Hardmode](Pre-Hardmode.md "Pre-Hardmode") [immunity accessory](Immunity_accessory "Immunity accessory") that grants the player immunity to the [Chilled](Chilled.md "Chilled") and [Frozen](Frozen.md "Frozen") [debuffs](Debuffs.md "Debuffs"). It is obtained from [Presents](Presents "Presents"), with a chance of about 0.622% in pre-Hardmode and about 0.580% in [Hardmode](Hardmode.md "Hardmode").[1]
47:    * Despite this, the Ankh Shield still provides immunity to Chilled, but not Frozen.
=== Pocket_Mirror ===
19:[Tooltip](Tooltips.md "Tooltips")|  _Grants immunity to Stoned_  
38:The **Pocket Mirror** is a [Hardmode](Hardmode.md "Hardmode") [immunity accessory](Immunity_accessory "Immunity accessory") that grants the player immunity to the [Stoned](Stoned.md "Stoned") [debuff](Debuff "Debuff"). It has a 1/40 (2.5%) / [1/20 (5%)](Expert_Mode.md "Expert Mode") chance of being dropped by naturally spawned [Medusas](Medusa.md "Medusa"). 
=== Ankh_Charm ===
20:[Tooltip](Tooltips.md "Tooltips")|  _Grants immunity to most debuffs_  
27:The **Ankh Charm** is a [Hardmode](Hardmode.md "Hardmode") [immunity accessory](Immunity_accessory "Immunity accessory") that grants the player immunity to the following [debuffs](Debuffs.md "Debuffs"): 
115:    * Now provides immunity to the [Stoned](Stoned.md "Stoned") debuff.
=== Ankh_Shield ===
21:[Tooltip](Tooltips.md "Tooltips")|  _Grants immunity to knockback and fire blocks  
22:Grants immunity to most debuffs_  
36:  * Immunity to [knockback](Knockback.md "Knockback")
37:  * Immunity to the following debuffs:

```


---

## 🤖 Assistant · 2026-08-12T18:26:36.261Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. Let me get the Ankh_Charm list (lines 27-40) and Ankh_Shield list (36-50).

Then I need to read the individual debuff pages for their specific values (DPS, duration ranges, sources, version changes). The index gives most, but the task asks for per-file values and "sources" and version changes. I should at least check each debuff page's top section for notes about version changes (e.g., On Fire! DPS changed, Frostburn, Cursed Inferno values, Ichor defense values, etc.).

Given the large number of pages, I'll read the top ~60 lines of each debuff page, which contains the infobox and the description. The History section at the bottom may note value changes, but that's lines ~700+. Let me grep each file for "History" section with numbers — better: grep for lines containing "Desktop 1\." plus numbers is noisy.

Efficient approach: for each debuff page, read lines 1-70 (infobox + lead) and grep the History section lines that mention numbers. Let me start reading the top of each page in parallel batches.

Let me batch: read On_Fire!.md, Poisoned.md, Acid_Venom.md, Cursed_Inferno.md tops.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:26:36.487Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Ankh_Charm.md",
 "limit": 18,
 "offset": 27
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:26:36.496Z

**📎 ToolResult**

```
27	The **Ankh Charm** is a [Hardmode](Hardmode.md "Hardmode") [immunity accessory](Immunity_accessory "Immunity accessory") that grants the player immunity to the following [debuffs](Debuffs.md "Debuffs"): 
28	
29	  * [](Bleeding.md "Bleeding")[Bleeding](Bleeding.md "Bleeding")
30	  * [](Broken_Armor.md "Broken Armor")[Broken Armor](Broken_Armor.md "Broken Armor")
31	  * [](Confused.md "Confused")[Confused](Confused.md "Confused")
32	  * [](Cursed.md "Cursed")[Cursed](Cursed.md "Cursed")
33	  * [](Darkness.md "Darkness")[Darkness](Darkness.md "Darkness")
34	  * [](Poisoned.md "Poisoned")[Poisoned](Poisoned.md "Poisoned")
35	  * [](Silenced.md "Silenced")[Silenced](Silenced.md "Silenced")
36	  * [](Slow.md "Slow")[Slow](Slow.md "Slow")
37	  * [](Stoned.md "Stoned")[Stoned](Stoned.md "Stoned")
38	  * [](Weak.md "Weak")[Weak](Weak.md "Weak")
39	
40	## Crafting
41	
42	### Recipes
43	
44	Result| Ingredients| [Crafting station](Crafting_station "Crafting station")  

```


---

## 🤖 Assistant · 2026-08-12T18:26:36.750Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Ankh_Shield.md",
 "limit": 22,
 "offset": 34
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:26:36.754Z

**📎 ToolResult**

```
34	
35	  * +4 [defense](Defense.md "Defense")
36	  * Immunity to [knockback](Knockback.md "Knockback")
37	  * Immunity to the following debuffs:
38	
39	    
40	
41	  * [](Bleeding.md "Bleeding")[Bleeding](Bleeding.md "Bleeding")
42	  * [](Broken_Armor.md "Broken Armor")[Broken Armor](Broken_Armor.md "Broken Armor")
43	  * [](Burning.md "Burning")[Burning](Burning.md "Burning")
44	  * [](Chilled.md "Chilled")[Chilled](Chilled.md "Chilled")
45	  * [](Confused.md "Confused")[Confused](Confused.md "Confused")
46	  * [](Cursed.md "Cursed")[Cursed](Cursed.md "Cursed")
47	  * [](Darkness.md "Darkness")[Darkness](Darkness.md "Darkness")
48	  * [](Poisoned.md "Poisoned")[Poisoned](Poisoned.md "Poisoned")
49	  * [](Silenced.md "Silenced")[Silenced](Silenced.md "Silenced")
50	  * [](Slow.md "Slow")[Slow](Slow.md "Slow")
51	  * [](Stoned.md "Stoned")[Stoned](Stoned.md "Stoned")
52	  * [](Weak.md "Weak")[Weak](Weak.md "Weak")
53	
54	## Crafting
55	

```


---

## 🤖 Assistant · 2026-08-12T18:26:38.786Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read the debuff pages. I'll batch-read tops of multiple pages. Use Read with limit ~70 each, in parallel.

Batch 1: On_Fire!.md, Poisoned.md, Acid_Venom.md, Cursed_Inferno.md, Ichor_(debuff).md (note: there's Ichor.md (item) and Ichor_(debuff).md), Frostburn.md.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:26:38.982Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/On_Fire!.md",
 "limit": 60,
 "offset": 9
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:26:38.993Z

**📎 ToolResult**

```
9	## Statistics
10	
11	### Type
12	
13	[Debuff](Debuff "Debuff")
14	
15	### Effects
16	
17	−4 health per second  
18	No health regeneration
19	
20	### Tooltip
21	
22	_Slowly losing life_
23	
24	## Items to prevent
25	
26	  * [](Obsidian_Skin "Obsidian Skin")[Obsidian Skin](Obsidian_Skin "Obsidian Skin")
27	  * [](Water.md "Water")[Water](Water.md "Water")
28	  * [](Honey.md "Honey")[Honey](Honey.md "Honey")
29	  * [](Shimmer.md "Shimmer")[Shimmer](Shimmer.md "Shimmer")**** __(Desktop, Console and Mobile versions)
30	  * [](Molten_armor.md "Molten armor")[Molten armor](Molten_armor.md "Molten armor")
31	
32	## Internal IDs
33	
34	### [Buff ID](Buff_IDs.md "Buff IDs")
35	
36	24
37	
38	### Internal name
39	
40	`OnFire`
41	
42	Not to be confused with [Burning](Burning.md "Burning").
43	
44	**On Fire!** is a [debuff](Debuffs.md "Debuffs") that prevents [health regeneration](Health_regeneration.md "Health regeneration") and causes the afflicted entity or player to lose 4 health per second. When an enemy is [Oiled](Oiled.md "Oiled")**** __(Desktop, Console and Mobile versions) , it will lose an additional 25 health per second, totaling to a loss of 29 [health](Health.md "Health") per second. 
45	
46	The debuff can be negated by submerging in any [liquid](Liquid "Liquid") except [lava](Lava.md "Lava"), having the [Obsidian Skin](Obsidian_Skin "Obsidian Skin") [buff](Buff "Buff"), ****__(Desktop, Console and Mobile versions) or equipping a full set of [Molten armor](Molten_armor.md "Molten armor"). 
47	
48	## Causes
49	
50	### From environment
51	
52	From  | Duration  | Chance  | Total damage   
53	---|---|---|---  
54	[](Lava.md "Lava")[Lava](Lava.md "Lava") | 7 / [14](Expert_Mode.md "Expert Mode") / [17.5](Master_Mode.md "Master Mode") seconds  | 100%  | 28 / [56](Expert_Mode.md "Expert Mode") / [70](Master_Mode.md "Master Mode")  
55	  
56	### From player
57	
58	From  | Duration  | Chance  | Total damage   
59	---|---|---|---  
60	[](Wand_of_Sparking.md "Wand of Sparking") | [Wand of Sparking](Wand_of_Sparking.md "Wand of Sparking")**** __(Desktop, Console and Mobile versions) | 1−4 seconds  | 50% | 4–16   
61	[](Volcano.md "Volcano") | [Volcano](Volcano.md "Volcano") | 3 seconds  | 50% | 12   
62	[](Molotov_Cocktail.md "Molotov Cocktail") | [Molotov Cocktail](Molotov_Cocktail.md "Molotov Cocktail")**** __(Desktop, Console, Old-gen console and Mobile versions) | 3–6 seconds  | 100% | 12–24   
63	[](Imp_Staff.md "Imp Staff") | [Imp Staff](Imp_Staff.md "Imp Staff")**** __(Desktop, Console, Old-gen console and Mobile versions) | 3–6 seconds  | 100%  | 12–24   
64	[](Foxparks.md "Foxparks") | [Foxparks](Foxparks.md "Foxparks")**** __(Desktop, Console and Mobile versions) | 5−10 seconds (Fireball) 5 seconds (Flamethrower)  | 100% | 20-40   
65	[](Molten_Pickaxe.md "Molten Pickaxe") | [Molten Pickaxe](Molten_Pickaxe.md "Molten Pickaxe") | 3 seconds  | 10% | 12   
66	[](Molten_Hamaxe.md "Molten Hamaxe") | [Molten Hamaxe](Molten_Hamaxe.md "Molten Hamaxe") | 3 seconds  | 20% | 12   
67	[](Flaming_Arrow.md "Flaming Arrow") | [Flaming Arrow](Flaming_Arrow.md "Flaming Arrow") | 3 seconds  | 33.3% | 12   
68	[](Flare "Flare") | [Flare](Flare "Flare") | 5–10 seconds  | 100% | 20–40   

```


---

## 🤖 Assistant · 2026-08-12T18:26:39.264Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Acid_Venom.md",
 "limit": 55,
 "offset": 9
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:26:39.273Z

**📎 ToolResult**

```
9	This is the **main** page whose information applies to the **[Desktop](Desktop_version_history.md "Desktop version history")** , **[Console](Console_version.md "Console version")** , and **[Mobile](Mobile_version.md "Mobile version")** versions of _[Terraria](Terraria.md "Terraria")_.  
10	For the differences of this information on [Old-gen console](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [3DS](Legacy%3A3DS_version "Legacy:3DS version"), see **[Legacy:Venom](Legacy%3AVenom "Legacy:Venom")**.
11	
12	## Acid Venom
13	
14	## Statistics
15	
16	### Type
17	
18	[Debuff](Debuff "Debuff")
19	
20	### Effects
21	
22	−30 health per second (on enemies)  
23	−15 health per second (on players)  
24	No health regeneration
25	
26	### Tooltip
27	
28	_Losing life_
29	
30	## Internal IDs
31	
32	### [Buff ID](Buff_IDs.md "Buff IDs")
33	
34	70
35	
36	### Internal name
37	
38	`Venom`
39	
40	Not to be confused with [Vial of Venom](Vial_of_Venom.md "Vial of Venom").
41	
42	**Acid Venom** is a [Hardmode](Hardmode.md "Hardmode") [debuff](Debuffs.md "Debuffs") that prevents health regeneration and causes the afflicted NPC or player to take damage each second for the duration of the debuff. It deals 30 damage per second when inflicted to enemies, and 15 damage per second when inflicted to players. 
43	
44	## Causes
45	
46	### From player
47	
48	From  | Duration  | Chance  | Total damage   
49	---|---|---|---  
50	[](Venom_Bullet.md "Venom Bullet") | [Venom Bullet](Venom_Bullet.md "Venom Bullet") | 10 seconds  | 1/1 (100%) | 300   
51	[](Venom_Arrow.md "Venom Arrow") | [Venom Arrow](Venom_Arrow.md "Venom Arrow") | 10 seconds  | 1/1 (100%) | 300   
52	[](Venom_Staff.md "Venom Staff") | [Venom Staff](Venom_Staff.md "Venom Staff") | 30 seconds  | 1/1 (100%) | 900   
53	[](Spider_Staff.md "Spider Staff") | [Spider Staff](Spider_Staff.md "Spider Staff") | 2–4 seconds  | 1/1 (100%) | 60–120   
54	[](Queen_Spider_Staff.md "Queen Spider Staff") | [Queen Spider Staff](Queen_Spider_Staff.md "Queen Spider Staff") | 2–4 seconds  | 1/1 (100%) | 60–120   
55	[](Flask_of_Venom.md "Flask of Venom") | [Flask of Venom](Flask_of_Venom.md "Flask of Venom") | 5–9 seconds  | 1/1 (100%) | 150–270   
56	[](Pygmy_Staff.md "Pygmy Staff") | [Pygmy Staff](Pygmy_Staff.md "Pygmy Staff") | 5–10 seconds  | 1/1 (100%) | 150–300   
57	  
58	### From enemy
59	
60	From  | Duration  | Chance  | Total damage   
61	---|---|---|---  
62	[](Black_Recluse.md "Black Recluse") | [Black Recluse](Black_Recluse.md "Black Recluse") | 4 / [8](Expert_Mode.md "Expert Mode") / [10](Master_Mode.md "Master Mode") seconds  | 1/10 (10%) | 60 / [120](Expert_Mode.md "Expert Mode") / [150](Master_Mode.md "Master Mode")  
63	[](Jungle_Creeper.md "Jungle Creeper") | [Jungle Creeper](Jungle_Creeper.md "Jungle Creeper") | 4 / [8](Expert_Mode.md "Expert Mode") / [10](Master_Mode.md "Master Mode") seconds  | 1/10 (10%) | 60 / [120](Expert_Mode.md "Expert Mode") / [150](Master_Mode.md "Master Mode")  

```


---

## 🤖 Assistant · 2026-08-12T18:26:43.943Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. Now I have On Fire! (4 DPS; oiled total 29/s) and Acid Venom (30 enemy / 15 player DPS; 4s base duration).

Let me check the On_Fire! history for version changes and notes about DPS. Also check Acid Venom version note (Venom was 1.2 "Venom" naming? The Legacy page). Let me grep the History sections of these debuff pages for numeric changes. Actually the important thing the task asks: "Note where the wiki explicitly states a value that changed between versions." Examples I know: Frostburn used to be 8 DPS both; Cursed Inferno 24/12; Ichor 15 def; Poisoned 2/6; On Fire! 4; Bleeding 12. In 1.4 many enemy DPS values were raised. Let me grep history sections for keywords like "damage per second" or "DPS" or numbers.

Let me grep each debuff page's History for lines containing digits and "Desktop".

Simpler: grep -n "Desktop 1" in each file, and look for lines mentioning numbers. But that's a lot of output. Let me be targeted: search for lines in History sections that mention "per second" or "damage" or "seconds".
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:26:45.207Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && for f in Poisoned Cursed_Inferno Frostburn Ichor_(debuff) Bleeding Darkness Silenced Slow Weak Confused Broken_Armor Suffocation Chilled Frozen Electrified Midas Daybroken Mana_Sickness Burning Stinky; do echo \"=== $f ===\"; grep -n -E 'Desktop 1\\.[0-9].*(per second|DPS|damage|second|defense|speed|mana|health)' \"$f.md\" | head -6; done 2>/dev/null",
 "description": "Grep history sections for value changes"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:26:48.595Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1

```


---

## 🤖 Assistant · 2026-08-12T18:26:49.954Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The parentheses in Ichor_(debuff) break globbing/quoting. Let me handle it by listing files explicitly with proper quoting.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:26:51.310Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && for f in \"Poisoned\" \"Cursed_Inferno\" \"Frostburn\" \"Ichor_(debuff)\" \"Bleeding\" \"Darkness\" \"Silenced\" \"Slow\" \"Weak\" \"Confused\" \"Broken_Armor\" \"Suffocation\" \"Chilled\" \"Frozen\" \"Electrified\" \"Midas\" \"Daybroken\" \"Mana_Sickness\" \"Burning\" \"Stinky\" \"On_Fire!\"; do echo \"=== $f ===\"; grep -n -E 'Desktop 1\\.[0-9]' \"$f.md\" | grep -E 'per second|DPS|damage|second|defense|speed|mana|health|coin' | head -5; done",
 "description": "Grep history for numeric changes per debuff"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:26:56.393Z

**📎 ToolResult**

```
=== Poisoned ===
271:  * [Desktop 1.4.4](Desktop_1.4.4 "Desktop 1.4.4"): When inflicted on enemies, now does 6 DPS instead of 2.
=== Cursed_Inferno ===
=== Frostburn ===
133:  * [Desktop 1.4.1](Desktop_1.4.1 "Desktop 1.4.1"): Players inflicted with this effect now lose 8 health per second, up from 6.
137:  * [Desktop 1.2.3](Desktop_1.2.3 "Desktop 1.2.3"): Damage doubled, but damage is done at half the rate. Wearing [Frost armor](Frost_armor.md "Frost armor") no longer makes [Spiky Ball Traps](Spiky_Ball_Trap.md "Spiky Ball Trap") inflict the Frostburn debuff.
=== Ichor_(debuff) ===
121:  * [Desktop 1.4.4](Desktop_1.4.4 "Desktop 1.4.4"): Mechanic changed from lowering [defense](Defense.md "Defense") to adding [armor penetration](Armor_penetration.md "Armor penetration") when applied to enemies.
=== Bleeding ===
=== Darkness ===
=== Silenced ===
=== Slow ===
=== Weak ===
=== Confused ===
=== Broken_Armor ===
=== Suffocation ===
=== Chilled ===
=== Frozen ===
=== Electrified ===
=== Midas ===
=== Daybroken ===
=== Mana_Sickness ===
66:  * [Desktop 1.3.0.1](Desktop_1.3.0.1 "Desktop 1.3.0.1"): Now the duration stacks and damage-reducing effect increases if mana-restoring items are consumed while the debuff is active, up to 10 seconds and 50% lowered magic damage.
=== Burning ===
=== Stinky ===
=== On_Fire! ===

```


---

## 🤖 Assistant · 2026-08-12T18:26:59.380Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Some history hits. Let me also grep for "1.4.4" and "1.4.0.1" lines generally in these pages with any wording, since damage changes might be worded differently. Let me get all History bullets for key pages — that could be a lot but pages are manageable if I extract only lines starting with "* [Desktop".

Let me grep for all Desktop lines in the specific pages (no filter) for the ones with no hits so far: Cursed_Inferno, Bleeding, Midas, Frozen, Electrified, etc.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:27:00.610Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && for f in \"Cursed_Inferno\" \"Bleeding\" \"Midas\" \"Frozen\" \"Electrified\" \"Ichor_(debuff)\" \"Confused\" \"Slow\" \"Weak\" \"Broken_Armor\" \"Suffocation\" \"Chilled\" \"Darkness\" \"Silenced\" \"Burning\" \"Daybroken\" \"Stinky\" \"Mana_Sickness\"; do echo \"=== $f ===\"; grep -n -E '\\* \\[(Desktop|Console) 1' \"$f.md\" | head -8; done",
 "description": "List history bullets for each debuff page"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:27:09.867Z

**📎 ToolResult**

```
=== Cursed_Inferno ===
112:  * [Desktop 1.4.1](Desktop_1.4.1 "Desktop 1.4.1"): 
116:  * [Desktop 1.4.0.1](Desktop_1.4.0.1 "Desktop 1.4.0.1"): 
121:  * [Desktop 1.1](Desktop_1.1 "Desktop 1.1"): Introduced.
=== Bleeding ===
251:  * [Desktop 1.4.5.0](Desktop_1.4.5.0 "Desktop 1.4.5.0"): 
257:  * [Desktop 1.1](Desktop_1.1 "Desktop 1.1"): Introduced.
=== Midas ===
53:  * [Desktop 1.2](Desktop_1.2 "Desktop 1.2"): Introduced.
57:  * [Console 1.02](Console_1.02.md "Console 1.02"): Introduced.
=== Frozen ===
78:  * [Desktop 1.3.0.1](Desktop_1.3.0.1 "Desktop 1.3.0.1"): The player can no longer use [grappling hooks](Hooks.md "Hooks") while Frozen.
80:  * [Desktop 1.2.3](Desktop_1.2.3 "Desktop 1.2.3"): No longer causes the player to appear [vanity](Vanity "Vanity")-less.
82:  * [Desktop 1.2.2](Desktop_1.2.2 "Desktop 1.2.2"): 
86:  * [Desktop 1.2](Desktop_1.2 "Desktop 1.2"): Introduced.
90:  * [Console 1.0.933.1](Console_1.0.933.1.md "Console 1.0.933.1"): Made corresponding update from [](Console_version.md "PlayStation 4")'s 1.0.750.0 update. ([](Console_version.md "Xbox One"))
92:  * [Console 1.0.750.0](Console_1.0.750.0.md "Console 1.0.750.0"): The player can no longer use grappling hooks while Frozen. ([](Console_version.md "PlayStation 4"))
94:  * [Console 1.05](Console_1.05.md "Console 1.05"): Can now be inflicted by the Ice Queen miniboss which shows up in the new Frost Moon event.
96:  * [Console 1.04](Console_1.04.md "Console 1.04"): Can now be prevented by the new Hand Warmer accessory, which has a very small chance to be dropped from Presents.
=== Electrified ===
67:  * [Desktop 1.4.4](Desktop_1.4.4 "Desktop 1.4.4"): Added 3 new death messages.
69:  * [Desktop 1.4.3.3](Desktop_1.4.3.3 "Desktop 1.4.3.3"): Tooltip changed from "You cannot move" to "Moving hurts!".
71:  * [Desktop 1.3.0.4](Desktop_1.3.0.4 "Desktop 1.3.0.4"): Can no longer be canceled by right-clicking the buff icon.
73:  * [Desktop 1.3.0.1](Desktop_1.3.0.1 "Desktop 1.3.0.1"): Introduced.
77:  * [Console 1.0.933.1](Console_1.0.933.1.md "Console 1.0.933.1"): Introduced. ([](Console_version.md "Xbox One"))
79:  * [Console 1.0.750.0](Console_1.0.750.0.md "Console 1.0.750.0"): Introduced. ([](Console_version.md "PlayStation 4"))
=== Ichor_(debuff) ===
121:  * [Desktop 1.4.4](Desktop_1.4.4 "Desktop 1.4.4"): Mechanic changed from lowering [defense](Defense.md "Defense") to adding [armor penetration](Armor_penetration.md "Armor penetration") when applied to enemies.
123:  * [Desktop 1.4.1](Desktop_1.4.1 "Desktop 1.4.1"): Defense reduction has been decreased by 25% from 20 to 15.
125:  * [Desktop 1.2.4](Desktop_1.2.4 "Desktop 1.2.4"): Fixed bug where [Flask of Gold](Flask_of_Gold.md "Flask of Gold") would apply Ichor debuff on enemies rather than Midas debuff.
127:  * [Desktop 1.2](Desktop_1.2 "Desktop 1.2"): Introduced.
131:  * [Console 1.02](Console_1.02.md "Console 1.02"): Introduced.
=== Confused ===
507:  * [Desktop 1.4.5.0](Desktop_1.4.5.0 "Desktop 1.4.5.0"): 
511:  * [Desktop 1.1](Desktop_1.1 "Desktop 1.1"): Introduced.
=== Slow ===
84:  * [Desktop 1.4.3](Desktop_1.4.3 "Desktop 1.4.3"): Can now be inflicted by Deerclops as well.
86:  * [Desktop 1.3.0.1](Desktop_1.3.0.1 "Desktop 1.3.0.1"): Now has a chance to be inflicted by [Expert Mode](Expert_Mode.md "Expert Mode") Brain of Cthulhu and Creepers, as well as Skeletron's Hands.
88:  * [Desktop 1.2](Desktop_1.2 "Desktop 1.2"): Now inflicted by the Necromancer's beams, and Rusty Armored Bones as well.
90:  * [Desktop 1.1](Desktop_1.1 "Desktop 1.1"): Introduced.
=== Weak ===
83:  * [Desktop 1.4.2](Desktop_1.4.2 "Desktop 1.4.2"): Can no longer be inflicted by [Vile Spit](Vile_Spit.md "Vile Spit") fired by the [Eater of Worlds](Eater_of_Worlds.md "Eater of Worlds") in [Expert Mode](Expert_Mode.md "Expert Mode").
85:  * [Desktop 1.3.0.1](Desktop_1.3.0.1 "Desktop 1.3.0.1"): 
91:  * [Desktop 1.2.2](Desktop_1.2.2 "Desktop 1.2.2"): Can now be inflicted for one hour by the [Red Potion](Red_Potion.md "Red Potion").
93:  * [Desktop 1.2.1](Desktop_1.2.1 "Desktop 1.2.1"): The [Floaty Gross](Floaty_Gross.md "Floaty Gross") and [Scarecrow](Scarecrow.md "Scarecrow") enemies can now inflict this debuff for 2 minutes and 1 minute respectively.
95:  * [Desktop 1.2](Desktop_1.2 "Desktop 1.2"): Can now be prevented by the new [Vitamins](Vitamins.md "Vitamins"), [Armor Bracing](Armor_Bracing.md "Armor Bracing"), [Ankh Charm](Ankh_Charm.md "Ankh Charm"), and [Ankh Shield](Ankh_Shield.md "Ankh Shield") accessories.
97:  * [Desktop 1.1](Desktop_1.1 "Desktop 1.1"): Introduced.
101:  * [Console 1.0.933.1](Console_1.0.933.1.md "Console 1.0.933.1"): Updated to match [](Console_version.md "PlayStation 4")'s 1.0.750.0 update.
103:  * [Console 1.0.750.0](Console_1.0.750.0.md "Console 1.0.750.0"): 
=== Broken_Armor ===
109:  * [Desktop 1.4.5.0](Desktop_1.4.5.0 "Desktop 1.4.5.0"): 
113:  * [Desktop 1.3.0.1](Desktop_1.3.0.1 "Desktop 1.3.0.1"): Duration from Armored Skeletons reduced from 5 to 2 minutes.
115:  * [Desktop 1.1](Desktop_1.1 "Desktop 1.1"): Introduced.
=== Suffocation ===
74:  * [Desktop 1.2.3](Desktop_1.2.3 "Desktop 1.2.3"): Running underwater no longer causes flashes of the Suffocation debuff.
76:  * [Desktop 1.2](Desktop_1.2 "Desktop 1.2"): Introduced.
80:  * [Console 1.02](Console_1.02.md "Console 1.02"): Introduced.
=== Chilled ===
81:  * [Desktop 1.2](Desktop_1.2 "Desktop 1.2"): Introduced.
85:  * [Console 1.02](Console_1.02.md "Console 1.02"): Introduced.
=== Darkness ===
79:  * [Desktop 1.4.0.1](Desktop_1.4.0.1 "Desktop 1.4.0.1"): 
84:  * [Desktop 1.3.0.1](Desktop_1.3.0.1 "Desktop 1.3.0.1"): 
89:  * [Desktop 1.2.2](Desktop_1.2.2 "Desktop 1.2.2"): Can now be inflicted for one hour by the [Red Potion](Red_Potion.md "Red Potion").
91:  * [Desktop 1.1](Desktop_1.1 "Desktop 1.1"): Can now be inflicted by the new [Corrupt Slime](Corrupt_Slime.md "Corrupt Slime") and [Dark Mummy](Mummies#Variants "Mummies") enemies.
93:  * [Desktop 1.0.6](Desktop_1.0.6 "Desktop 1.0.6"): Introduced.
97:  * [Console 1.0.933.1](Console_1.0.933.1.md "Console 1.0.933.1"): Made corresponding updates from [](Console_version.md "PlayStation 4")'s 1.0.750.0 update. ([](Console_version.md "Xbox One"))
99:  * [Console 1.0.750.0](Console_1.0.750.0.md "Console 1.0.750.0"): 
=== Silenced ===
84:  * [Desktop 1.4.5.0](Desktop_1.4.5.0 "Desktop 1.4.5.0"): No longer affects summon weapons.
86:  * [Desktop 1.1](Desktop_1.1 "Desktop 1.1"): Introduced.
=== Burning ===
97:  * [Desktop 1.4.5.0](Desktop_1.4.5.0 "Desktop 1.4.5.0"): 
101:  * [Desktop 1.3.0.2](Desktop_1.3.0.2 "Desktop 1.3.0.2"): No longer caused by developer items in Classic Mode.
103:  * [Desktop 1.3.0.1](Desktop_1.3.0.1 "Desktop 1.3.0.1"): 
107:  * [Desktop 1.2](Desktop_1.2 "Desktop 1.2"): Introduced.
111:  * [Console 1.02](Console_1.02.md "Console 1.02"): Introduced.
=== Daybroken ===
89:  * [Desktop 1.4.3](Desktop_1.4.3 "Desktop 1.4.3"): Fixed a typo in the tooltip ("Incenerated" to "Incinerated").
91:  * [Desktop 1.3.0.4](Desktop_1.3.0.4 "Desktop 1.3.0.4"): Fixed Daybroken debuff spreading to friendly NPCs, killing them.
93:  * [Desktop 1.3.0.1](Desktop_1.3.0.1 "Desktop 1.3.0.1"): Introduced.
97:  * [Console 1.0.933.1](Console_1.0.933.1.md "Console 1.0.933.1"): Introduced. ([](Console_version.md "Xbox One"))
99:  * [Console 1.0.750.0](Console_1.0.750.0.md "Console 1.0.750.0"): Introduced. ([](Console_version.md "PlayStation 4"))
=== Stinky ===
70:  * [Desktop 1.4.5.0](Desktop_1.4.5.0 "Desktop 1.4.5.0"): 
77:  * [Desktop 1.4.4](Desktop_1.4.4 "Desktop 1.4.4"): Can now be inflicted by Poo and the [Flymeal](Flymeal.md "Flymeal").
79:  * [Desktop 1.4.0.3](Desktop_1.4.0.3 "Desktop 1.4.0.3"): Sprite updated. Old sprite was 
81:  * [Desktop 1.3.4.3](Desktop_1.3.4.3 "Desktop 1.3.4.3"): Fixed not properly applying to other players in [Multiplayer](Multiplayer.md "Multiplayer").
83:  * [Desktop 1.2.4](Desktop_1.2.4 "Desktop 1.2.4"): Introduced.
87:  * [Console 1.4.4](Console_1.4.4.md "Console 1.4.4"): Can now be inflicted by Poo.
89:  * [Console 1.07](Console_1.07.md "Console 1.07"): Introduced.
=== Mana_Sickness ===
66:  * [Desktop 1.3.0.1](Desktop_1.3.0.1 "Desktop 1.3.0.1"): Now the duration stacks and damage-reducing effect increases if mana-restoring items are consumed while the debuff is active, up to 10 seconds and 50% lowered magic damage.
68:  * [Desktop 1.2.3](Desktop_1.2.3 "Desktop 1.2.3"): Introduced.
72:  * [Console 1.06](Console_1.06.md "Console 1.06"): Introduced.

```


---

## 🤖 Assistant · 2026-08-12T18:27:14.652Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have version-change info for: Poisoned (1.4.4: 2→6 DPS on enemies), Frostburn (1.4.1: 6→8 on players; 1.2.3 damage doubled), Ichor (1.4.1: 20→15; 1.4.4 mechanic change to armor pen), Broken Armor (1.3.0.1: Armored Skeleton duration 5→2 min), Mana Sickness (1.3.0.1 stacking up to 10s/50%).

Also Cursed_Inferno 1.4.1 and 1.4.0.1 bullets (lines 112-120) — need content. And Bleeding 1.4.5.0, Burning 1.4.5.0, Confused 1.4.5.0, Darkness 1.4.0.1/1.3.0.1, Stinky 1.4.5.0. Let me read those specific line ranges.

Also I need per-page infobox values for each debuff (top ~30 lines). Let me batch read them.

Plan:
Batch A (reads): Cursed_Inferno lines 110-122; Bleeding 245-260; Burning 90-110; Confused 500-515; Darkness 75-95; Stinky 65-80.
Batch B (reads of tops): Poisoned, Cursed_Inferno, Frostburn, Ichor_(debuff), Bleeding, Darkness, Silenced, Slow, Weak, Confused, Broken_Armor, Suffocation, Chilled, Frozen, Electrified, Midas, Daybroken, Mana_Sickness, Burning, Stinky.

That's a lot of Read calls but they're cheap. Let me use a bash grep to extract infobox "Effects" sections more efficiently — grep -A4 "### Effects".
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:27:15.622Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && for f in \"Poisoned\" \"Cursed_Inferno\" \"Frostburn\" \"Ichor_(debuff)\" \"Bleeding\" \"Darkness\" \"Silenced\" \"Slow\" \"Weak\" \"Confused\" \"Broken_Armor\" \"Suffocation\" \"Chilled\" \"Frozen\" \"Electrified\" \"Midas\" \"Daybroken\" \"Mana_Sickness\" \"Burning\" \"Stinky\"; do echo \"=== $f ===\"; grep -n -A5 '^### Effects' \"$f.md\" | head -8; done",
 "description": "Extract infobox effects for all debuffs"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:27:23.390Z

**📎 ToolResult**

```
=== Poisoned ===
20:### Effects
21-
22-−6 health per second (on enemies)  
23-−2 health per second (on players)  
24-No health regeneration
25-
=== Cursed_Inferno ===
20:### Effects
21-
22-−24 health per second (on enemies)  
23-+10% knockback taken (on enemies)  
24-−12 health per second (on players)  
25-No health regeneration
=== Frostburn ===
20:### Effects
21-
22-−8 health per second  
23-No health regeneration
24-
25-### Tooltip
=== Ichor_(debuff) ===
20:### Effects
21-
22-+15 armor penetration against target (on enemies)  
23-−15 defense (on players)
24-
25-### Tooltip
=== Bleeding ===
15:### Effects
16-
17-−12 health per second (on enemies)  
18-No health regeneration (on players)
19-
20-### Tooltip
=== Darkness ===
=== Silenced ===
15:### Effects
16-
17-Unable to use any item that consumes mana
18-
19-### Tooltip
20-
=== Slow ===
15:### Effects
16-
17-Horizontal movement speed is halved
18-
19-### Tooltip
20-
=== Weak ===
15:### Effects
16-
17-Multiple stat decreases
18-
19-### Tooltip
20-
=== Confused ===
15:### Effects
16-
17-Player's controls are reversed
18-
19-### Tooltip
20-
=== Broken_Armor ===
15:### Effects
16-
17-+20 armor penetration against target (on enemies)  
18-Halves defense (on players)
19-
20-### Tooltip
=== Suffocation ===
15:### Effects
16-
17-−20 health per second
18-
19-### Tooltip
20-
=== Chilled ===
15:### Effects
16-
17-Reduced movement speed
18-
19-### Tooltip
20-
=== Frozen ===
15:### Effects
16-
17-Unable to move or use items
18-
19-### Tooltip
20-
=== Electrified ===
19:### Effects
20-
21-−4 health per second (when stationary)  
22-−20 health per second (when moving left/right)  
23-No health regeneration
24-
=== Midas ===
15:### Effects
16-
17-Affected enemy drops more coins upon death
18-
19-### Tooltip
20-
=== Daybroken ===
19:### Effects
20-
21-−25 health per quarter second  
22-No health regeneration
23-
24-### Tooltip
=== Mana_Sickness ===
=== Burning ===
20:### Effects
21-
22-−30 health per second  
23-Reduced movement speed
24-
25-### Tooltip
=== Stinky ===
15:### Effects
16-
17-Decreased luck, entity emits green fumes
18-
19-### Tooltip
20-

```


---

## 🤖 Assistant · 2026-08-12T18:27:27.000Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. Now, durations per debuff page: The individual pages have "Causes" tables with durations. The index already gave base duration ranges. I should also grab the durations from each page's infobox if present. Some infoboxes have "Duration" field. Let me grep for "Duration" in infobox (line ~25-30). Actually the infobox of buff pages typically has "Duration" row. Let me grep -n -A2 '### Duration' or "Duration" rows.

Let me check the structure of one page, e.g., Silenced.md lines 10-50.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:27:27.254Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Silenced.md",
 "limit": 45,
 "offset": 8
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:27:27.258Z

**📎 ToolResult**

```
8	
9	## Statistics
10	
11	### Type
12	
13	[Debuff](Debuff "Debuff")
14	
15	### Effects
16	
17	Unable to use any item that consumes mana
18	
19	### Tooltip
20	
21	_Cannot use items that require mana_
22	
23	## Items to prevent
24	
25	  * [](Megaphone.md "Megaphone")[Megaphone](Megaphone.md "Megaphone")
26	  * [](Countercurse_Mantra.md "Countercurse Mantra")[Countercurse Mantra](Countercurse_Mantra.md "Countercurse Mantra")
27	  * [](Ankh_Charm.md "Ankh Charm")[Ankh Charm](Ankh_Charm.md "Ankh Charm")
28	  * [](Ankh_Shield.md "Ankh Shield")[Ankh Shield](Ankh_Shield.md "Ankh Shield")
29	
30	## Internal IDs
31	
32	### [Buff ID](Buff_IDs.md "Buff IDs")
33	
34	35
35	
36	### Internal name
37	
38	`Silenced`
39	
40	**Silenced** is a [debuff](Debuffs.md "Debuffs") that prevents the player from using any item which uses [mana](Mana.md "Mana"), stopping them from using [magic weapons](Magic_weapons.md "Magic weapons") and [summon weapons](Summon_weapons.md "Summon weapons"). On the [ Desktop version](Desktop_version_history.md "Desktop version history"), [ Console version](Console_version.md "Console version"), and [ Mobile version](Mobile_version.md "Mobile version"), it does not affect summon weapons. 
41	
42	The debuff can be prevented from afflicting the player by equipping the [Megaphone](Megaphone.md "Megaphone") or its derivatives. 
43	
44	## Causes
45	
46	### From enemy
47	
48	From  | Duration  | Chance   
49	---|---|---  
50	[](Pixie.md "Pixie") | [Pixie](Pixie.md "Pixie") | 7 / [14](Expert_Mode.md "Expert Mode") / [17.5](Master_Mode.md "Master Mode") seconds  | 1/10 (10%)  
51	[](Dark_Mummy.md "Dark Mummy") | [Dark Mummy](Dark_Mummy.md "Dark Mummy") | 7 / [14](Expert_Mode.md "Expert Mode") / [17.5](Master_Mode.md "Master Mode") seconds  | 1/5 (20%)  
52	[](Blood_Mummy.md "Blood Mummy") | [Blood Mummy](Blood_Mummy.md "Blood Mummy")**** __(Desktop, Console and Mobile versions) | 7 / [14](Expert_Mode.md "Expert Mode") / [17.5](Master_Mode.md "Master Mode") seconds  | 1/5 (20%)  

```


---

## 🤖 Assistant · 2026-08-12T18:27:28.525Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && for f in \"Poisoned\" \"Cursed_Inferno\" \"Frostburn\" \"Ichor_(debuff)\" \"Bleeding\" \"Darkness\" \"Slow\" \"Weak\" \"Confused\" \"Broken_Armor\" \"Chilled\" \"Frozen\" \"Electrified\" \"Mana_Sickness\" \"Suffocation\" \"Midas\" \"Daybroken\" \"Burning\" \"Stinky\"; do echo \"=== $f ===\"; grep -n -E '^\\s*(Duration|Type)\\|' \"$f.md\" | head -3; done",
 "description": "Check infobox duration rows"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:27:32.269Z

**📎 ToolResult**

```
=== Poisoned ===
=== Cursed_Inferno ===
=== Frostburn ===
=== Ichor_(debuff) ===
=== Bleeding ===
=== Darkness ===
=== Slow ===
=== Weak ===
=== Confused ===
=== Broken_Armor ===
=== Chilled ===
=== Frozen ===
=== Electrified ===
=== Mana_Sickness ===
=== Suffocation ===
=== Midas ===
=== Daybroken ===
=== Burning ===
=== Stinky ===

```


---

## 🤖 Assistant · 2026-08-12T18:27:38.587Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
No duration rows in infobox; durations are in the Causes tables and the index. That's fine — I'll use index durations and add key cause durations from individual pages where notable (e.g., Broken Armor from Armored Skeleton = 2 minutes / 5 min expert; Weak from Red Potion 1 hour; Darkness from Red Potion 1 hour; Frozen durations; Cursed Inferno from sources).

The task wants "sources" too. Providing all sources per debuff would be huge. I'll give the main inflicting sources with durations for key ones, focusing on numbers. To keep it compact but thorough, I'll extract the "Causes" table rows for each debuff — but that's a LOT. Let me extract them efficiently with grep for table rows in each debuff page (lines starting with "[]( ) | [Name]"). Actually the tables include both player and enemy causes with durations and chances. I'll grab the first ~15 rows per page.

Hmm, the task says "extract the WIKI-STATED numeric values (damage per second / duration / stat modifiers / sources)". So sources matter. I'll include the notable ones (with durations/chances) but keep compact — maybe list top sources per debuff.

Given time constraints, I'll extract the Causes tables for the requested debuffs via grep and report them in condensed form. Let me pull the Causes sections for each debuff page.

Let me write a loop that prints lines from "## Causes" to the next "## " header for each debuff file, but limited to first 25 lines. That gives sources with durations.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:27:39.572Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && for f in \"Poisoned\" \"Cursed_Inferno\" \"Frostburn\" \"Ichor_(debuff)\"; do echo \"##### $f #####\"; awk '/^## Causes/{flag=1} flag&&/^## /&&!/^## Causes/{exit} flag' \"$f.md\" | grep -E '\\|' | head -22; done",
 "description": "Extract causes tables for 4 debuffs"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:28:06.262Z

**📎 ToolResult**

```
##### Poisoned #####
From  | Duration  | Chance  | Total damage   
---|---|---|---  
[](Blade_of_Grass.md "Blade of Grass") | [Blade of Grass](Blade_of_Grass.md "Blade of Grass") | 7 seconds  | 25% | 42   
[](Hornet_Staff.md "Hornet Staff") | [Hornet Staff](Hornet_Staff.md "Hornet Staff") | 4–7 seconds  | 100% | 24–42   
[](Thorn_Chakram.md "Thorn Chakram") | [Thorn Chakram](Thorn_Chakram.md "Thorn Chakram") | 7 seconds  | 50% | 42   
[](Snapthorn.md "Snapthorn") | [Snapthorn](Snapthorn.md "Snapthorn") | 3 seconds  | 20% | 18   
[](Toxikarp.md "Toxikarp") | [Toxikarp](Toxikarp.md "Toxikarp") | 10–29 seconds  | 100% | 60–174   
[](Barnacle_Staff.md "Barnacle Staff") | [Barnacle Staff](Barnacle_Staff.md "Barnacle Staff") | 5–10 seconds  | 100% | 30-60   
[](Poison_Dart.md "Poison Dart") | [Poison Dart](Poison_Dart.md "Poison Dart") | 30–60 seconds  | 100% | 180–360   
[](Poisoned_Knife.md "Poisoned Knife") | [Poisoned Knife](Poisoned_Knife.md "Poisoned Knife") | 10 seconds  | 50% | 60   
[](Poison_Staff.md "Poison Staff") | [Poison Staff](Poison_Staff.md "Poison Staff") | 30 seconds  | 100% | 180   
[](Flask_of_Poison.md "Flask of Poison") | [Flask of Poison](Flask_of_Poison.md "Flask of Poison") | 5–10 seconds  | 100% | 30–60   
[](Spore_Sac.md "Spore Sac") | [Spore Sac](Spore_Sac.md "Spore Sac") | 5–10 seconds  | 100% | 30–60   
From  | Duration  | Chance  | Total damage   
---|---|---|---  
[](Hornet.md "Hornet") | [Hornet](Hornet.md "Hornet")(Stinger attack) | 10 / [2–10 or 20](Expert_Mode.md "Expert Mode") / [2.5–12.5 or 25](Master_Mode.md "Master Mode") seconds  | 1/3 (33.33%) / [1/1 (100%)](Expert_Mode.md "Expert Mode") | 20 / [4–20 or 40](Expert_Mode.md "Expert Mode") / [5-12.5 or 50](Master_Mode.md "Master Mode")  
[](Moss_Hornet.md "Moss Hornet") | [Moss Hornet](Moss_Hornet.md "Moss Hornet")(Stinger attack) | 10 / [2–10 or 20](Expert_Mode.md "Expert Mode") / [2.5–12.5 or 25](Master_Mode.md "Master Mode") seconds  | 1/3 (33.33%) / [1/1 (100%)](Expert_Mode.md "Expert Mode") | 20 / [4–20 or 40](Expert_Mode.md "Expert Mode") / [5-12.5 or 50](Master_Mode.md "Master Mode")  
[](Toxic_Sludge.md "Toxic Sludge") | [Toxic Sludge](Toxic_Sludge.md "Toxic Sludge") | 10 / [20](Expert_Mode.md "Expert Mode") / [25](Master_Mode.md "Master Mode") seconds  | 1/2 (50%) | 20 / [40](Expert_Mode.md "Expert Mode") / [50](Master_Mode.md "Master Mode")  
[](Queen_Bee.md "Queen Bee") | [Queen Bee](Queen_Bee.md "Queen Bee")(Stinger attack) | 10 / [2–10 or 20](Expert_Mode.md "Expert Mode") / [2.5–12.5 or 25](Master_Mode.md "Master Mode") seconds  | 1/3 (33.33%) / [1/1 (100%)](Expert_Mode.md "Expert Mode") | 20 / [4–20 or 40](Expert_Mode.md "Expert Mode") / [5-12.5 or 50](Master_Mode.md "Master Mode")  
[Queen Bee](Queen_Bee.md "Queen Bee")(melee) | [2–8](Expert_Mode.md "Expert Mode") / [2.5-10](Master_Mode.md "Master Mode") seconds  | [1/1 (100%)](Expert_Mode.md "Expert Mode") | [4–16](Expert_Mode.md "Expert Mode") / [5-20](Master_Mode.md "Master Mode")  
[](Bee.md "Bee") | [Bee](Bee.md "Bee") | [2–6](Expert_Mode.md "Expert Mode") / [2.5-7.5](Master_Mode.md "Master Mode") seconds  | [1/1 (100%)](Expert_Mode.md "Expert Mode") | [4–12](Expert_Mode.md "Expert Mode") / [5-15](Master_Mode.md "Master Mode")  
[](Spiked_Jungle_Slime.md "Spiked Jungle Slime") | [Spiked Jungle Slime](Spiked_Jungle_Slime.md "Spiked Jungle Slime")(Stinger attack) | 5 or 20 / [10 or 40](Expert_Mode.md "Expert Mode") / [12.5 or 50](Master_Mode.md "Master Mode") seconds  | 5/8 (62.5%) | 10 or 40 / [20 or 80](Expert_Mode.md "Expert Mode") / [25 or 100](Master_Mode.md "Master Mode")  
##### Cursed_Inferno #####
From  | Duration  | Chance  | Total damage   
---|---|---|---  
[](Cursed_Arrow.md "Cursed Arrow") | [Cursed Arrow](Cursed_Arrow.md "Cursed Arrow") | 7 seconds  | 100% | 168   
[](Cursed_Bullet.md "Cursed Bullet") | [Cursed Bullet](Cursed_Bullet.md "Cursed Bullet") | 7 seconds  | 100% | 168   
[](Cursed_Dart.md "Cursed Dart") | [Cursed Dart](Cursed_Dart.md "Cursed Dart") | 3–6 seconds  | 100% | 72–144   
[](Cursed_Flames.md "Cursed Flames") | [Cursed Flames](Cursed_Flames.md "Cursed Flames") | 7 seconds  | 100% | 168   
[](Cursed_Flare "Cursed Flare") | [Cursed Flare](Cursed_Flare "Cursed Flare") | 10 seconds  | 100% | 240   
[](Clinger_Staff.md "Clinger Staff") | [Clinger Staff](Clinger_Staff.md "Clinger Staff") | 7 seconds  | 100% | 168   
[](Flask_of_Cursed_Flames.md "Flask of Cursed Flames") | [Flask of Cursed Flames](Flask_of_Cursed_Flames.md "Flask of Cursed Flames") | 3–6 seconds  | 100% | 72–144   
From  | Duration  | Chance  | Total damage   
---|---|---|---  
[](Clinger.md "Clinger") | [Clinger](Clinger.md "Clinger") (Cursed Flame)  | 2-3 / [4-6](Expert_Mode.md "Expert Mode") / [5-7.5](Master_Mode.md "Master Mode") seconds  | 1/3 (33.33%) | 24-36 / [48-72](Expert_Mode.md "Expert Mode") / [60-90](Master_Mode.md "Master Mode")  
[](Vile_Ghoul "Vile Ghoul") | [Vile Ghoul](Vile_Ghoul "Vile Ghoul") | 7 / [14](Expert_Mode.md "Expert Mode") / [17.5](Master_Mode.md "Master Mode") seconds  | 1/1 (100%) | 84 / [168](Expert_Mode.md "Expert Mode") / [210](Master_Mode.md "Master Mode")  
[](Spazmatism.md "Spazmatism") | [Spazmatism](Spazmatism.md "Spazmatism") (Cursed Flames Attack)  | 2-3 / [4-6](Expert_Mode.md "Expert Mode") / [5-7.5](Master_Mode.md "Master Mode") seconds  | 1/3 (33.33%) | 24-36 / [48-72](Expert_Mode.md "Expert Mode") / [60-90](Master_Mode.md "Master Mode")  
##### Frostburn #####
From  | Duration  | Chance  | Total damage   
---|---|---|---  
[](Wand_of_Frosting.md "Wand of Frosting") | [Wand of Frosting](Wand_of_Frosting.md "Wand of Frosting") | 2–3 seconds  | 50% | 16–24   
[](Frostburn_Arrow.md "Frostburn Arrow") | [Frostburn Arrow](Frostburn_Arrow.md "Frostburn Arrow") | 3 seconds  | 33.3% | 24   
[](Ice_Boomerang.md "Ice Boomerang") | [Ice Boomerang](Ice_Boomerang.md "Ice Boomerang") | 3 seconds  | 50% | 24   
From  | Duration  | Chance  | Total damage   
---|---|---|---  
[](Ice_Elemental.md "Ice Elemental")[Ice Elemental](Ice_Elemental.md "Ice Elemental")(Frost Blast) | 6 / [12](Expert_Mode.md "Expert Mode") / [15](Master_Mode.md "Master Mode") seconds  | 1/3 (33.33%) | 48 / [96](Expert_Mode.md "Expert Mode") / [120](Master_Mode.md "Master Mode")  
[](Slush_Slime.md "Slush Slime")[Slush Slime](Slush_Slime.md "Slush Slime") | 3-6 / [6-12](Expert_Mode.md "Expert Mode") / [7-15](Master_Mode.md "Master Mode") seconds  | 1/1 (100%) | 24-48 / [48-96](Expert_Mode.md "Expert Mode") / [56-120](Master_Mode.md "Master Mode")  
[](Snow_Slime.md "Snow Slime")[Snow Slime](Snow_Slime.md "Snow Slime") | 3-6 / [6-12](Expert_Mode.md "Expert Mode") / [7-15](Master_Mode.md "Master Mode") seconds  | 1/1 (100%) | 24-48 / [48-96](Expert_Mode.md "Expert Mode") / [56-120](Master_Mode.md "Master Mode")  
##### Ichor_(debuff) #####
From  | Duration  | Chance   
---|---|---  
[](Golden_Shower.md "Golden Shower") | [Golden Shower](Golden_Shower.md "Golden Shower") | 10 seconds  | 100%   
[](Ichor_Bullet.md "Ichor Bullet") | [Ichor Bullet](Ichor_Bullet.md "Ichor Bullet") | 10 seconds  | 100%   
[](Ichor_Arrow.md "Ichor Arrow") | [Ichor Arrow](Ichor_Arrow.md "Ichor Arrow") | 10 seconds  | 100%   
[](Flask_of_Ichor.md "Flask of Ichor") | [Flask of Ichor](Flask_of_Ichor.md "Flask of Ichor") | 10–19 seconds  | 100%   
[](Ichor_Dart.md "Ichor Dart") | [Ichor Dart](Ichor_Dart.md "Ichor Dart") | 7–14 seconds  | 100%   
[](Bladetongue.md "Bladetongue") | [Bladetongue](Bladetongue.md "Bladetongue") | 5–9 seconds (sword)  
3–7 seconds (projectile) | 100%   
From  | Duration  | Chance   
---|---|---  
[](Ichor_Sticker.md "Ichor Sticker")[Ichor Sticker](Ichor_Sticker.md "Ichor Sticker") | 15 / [30](Expert_Mode.md "Expert Mode") / [37.5](Master_Mode.md "Master Mode") seconds  | 1/1 (100%)  
[](Tainted_Ghoul "Tainted Ghoul")[Tainted Ghoul](Tainted_Ghoul "Tainted Ghoul") | 7 / [14](Expert_Mode.md "Expert Mode") / [17.5](Master_Mode.md "Master Mode") seconds  | 1/1 (100%)

```


---

## 🤖 Assistant · 2026-08-12T18:28:11.429Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
These are long. For the report, I'll summarize key sources with durations. The task wants compact list format `Name — wiki value (file:section)`. I'll include main numbers plus a few notable sources. I shouldn't dump every source row; but "sources" is requested. I'll give the notable numeric source durations per debuff in compact form (e.g., "sources: Lava 7s/14/17.5 @100%; Wand of Sparking 1–4s @50%").

Given the volume, I'll extract sources for the remaining debuffs too but keep the report condensed. Let me grab causes for the rest of debuffs quickly (Bleeding, Darkness, Slow, Weak, Confused, Broken Armor, Chilled, Frozen, Electrified, Mana Sickness, Suffocation, Burning, Midas, Daybroken, Stinky, Poisoned done, Cursed done, Frostburn done, Ichor done, On Fire partially done).

Actually, I already have On Fire causes partially. Let me get the rest.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:28:12.816Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && for f in \"Bleeding\" \"Darkness\" \"Slow\" \"Weak\" \"Confused\" \"Broken_Armor\" \"Chilled\" \"Frozen\" \"Electrified\" \"Mana_Sickness\" \"Burning\" \"Midas\" \"Daybroken\" \"Stinky\"; do echo \"##### $f #####\"; awk '/^## Causes/{flag=1} flag&&/^## /&&!/^## Causes/{exit} flag' \"$f.md\" | grep -E '\\|' | sed -E 's/\\[\\]\\([^)]*\\) ?//g; s/\\[([^]|]*)\\]\\(([^)]*)\\)/\\1/g' | head -14; done",
 "description": "Extract condensed causes for remaining debuffs"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:28:37.059Z

**📎 ToolResult**

```
##### Bleeding #####
From  | Duration  | Chance   
---|---|---  
| Spike Slime**** __(Desktop, Console and Mobile versions) | 10-20 / 20-40 / 25-40 seconds  | 1/1 (100%)  
| Werewolf | 45 / 90 / 112.5 seconds  | 1/8 (12.5%)  
| Vampire | 5-7/ 10-14 / 12.5-17.5 seconds  | 1/1 (100%)  
| Angler Fish | 45 / 90 / 112.5 seconds  | 1/8 (12.5%)  
| Rusty Armored Bones | 10 / 20 / 25 seconds  | 1/8 (12.5%)  
| Skeletron Head | 6-10 / 7.5-12.5 seconds  | 1/1 (100%)  
| Duke Fishron | 6-20 / 7.5-25 seconds  | 1/3 (33.33%)  
| Brain of Cthulhu | 7.5-15 / 9.37-18.75 seconds  | 11/243 (4.53%)  
| Creeper | 7.5-15 / 9.37-18.75 seconds  | 11/81 (13.58%)  
From  | Duration  | Chance   
---|---|---  
| Tizona**** __(Old-gen console and 3DS versions) | 10 seconds  | ?   
##### Darkness #####
From  | Duration  | Chance   
---|---|---  
| Black Slime | 15 / 30 / 37.5 seconds  | 1/4 (25%)  
| Corrupt Slime | 15 / 30 / 37.5 seconds  | 1/4 (25%)  
| Slimer(without wings) | 15 / 30 / 37.5 seconds  | 1/4 (25%)  
| Slimeling | 15 / 30 / 37.5 seconds  | 1/4 (25%)  
| Crimslime | 15 / 30 / 37.5 seconds  | 1/4 (25%) ****__(Desktop, Console and Mobile versions)  
| Dark Mummy | 15 / 30 / 37.5 seconds  | 1/4 (25%)  
| Blood Mummy**** __(Desktop, Console and Mobile versions) | 15 / 30 / 37.5 seconds  | 1/4 (25%)  
| Demon | 15 / 30 / 37.5 seconds  | 1/3 (33.33%) (Scythe attack)  
| Voodoo Demon | 15 / 30 / 37.5 seconds  | 1/3 (33.33%) (Scythe attack)  
| Arch Demon**** __(Old-gen console and 3DS versions) | 15 seconds  | 1/3 (33.33%) (Scythe attack)  
| Brain of Cthulhu | 3–6 / 3.75–7.5 seconds  | 11/243 (4.53%)  
| Creeper | 3–6 / 3.75–7.5 seconds  | 11/81 (13.58%)  
##### Slow #####
From  | Duration  | Chance   
---|---|---  
| Pixie | 15 / 30 / 37.5 seconds  | 1/8 (12.5%)  
| Wraith | 15 / 30 / 37.5 seconds  | 1/8 (12.5%)  
| Mummy | 15 / 30 / 37.5 seconds  | 1/8 (12.5%)  
| Rusty Armored Bones | 5 / 10 / 12.5 seconds  | 2/9 (22.22%)  
| Necromancer | 5–16 / 10–32 / 12.5–40 seconds  | 1/1 (100%)  
"Skeletron Hand \(NPC\)") | Skeletron Hand "Skeletron Hand \(NPC\)") | 0.5–1 / 0.63–1.25 seconds  | 1/2 (50%)  
| Brain of Cthulhu | 5.23–10.5 / 6.53–13.12 seconds  | 11/243 (4.53%)  
| Creeper | 5.23–10.5 / 6.53–13.12 seconds  | 11/81 (13.58%)  
| Deerclops**** __(Desktop, Console and Mobile versions)(Roar) | 12 / 24 / 30 seconds  | 1/1 (100%)  
From  | Duration  | Chance   
---|---|---  
| Feral Bite**** __(Desktop, Console and Mobile versions) | 2.1–3.5 / 4.2–7 / 5.25–8.75 seconds  | 1/6 (16.67%), 1/20 (5%) every second  
##### Weak #####
From  | Duration  | Chance   
---|---|---  
| Corruptor(Vile Spit) | 5 / 10 / 12.5 minutes  | 1/20 (5%)  
| Floaty Gross | 2 / 4 / 5 minutes  | 1/25 (4%)  
| Scarecrow | 1 / 2 / 2.5 minute(s)  | 1/10 (10%)  
| Brain of Cthulhu | 11.23–22.5 / 14.03–28.12 seconds  | 11/243 (4.53%)  
| Creeper | 11.23–22.5 / 14.03–28.12 seconds  | 11/81 (13.58%)  
From  | Duration  | Chance   
---|---|---  
| Feral Bite**** __(Desktop, Console and Mobile versions) | 3–5 / 6–10 / 7.5–12.5 seconds  | 1/6 (16.67%), 1/20 (5%) every second  
From  | Duration  | Chance   
---|---|---  
| Red Potion**** __(Desktop, Console and Mobile versions)(except For the Worthy and Zenith "Zenith \(seed\)") worlds) | 1 / 2 / 3 hours  | 1/1 (100%)  
##### Confused #####
From  | Duration  | Chance   
---|---|---  
| Brain of Confusion**** __(Desktop, Console and Mobile versions) | 1.5 seconds at minimum;  
depends on damage taken, see notes | 60%–100%   
| Dao of Pow | 2–4 seconds  | 80%   
| Bee Keeper | 2 seconds  | 100%   
| Purple Clubberfish | 1–3  | 50%   
| Ale Tosser**** __(Desktop, Console and Mobile versions) | 2–5 seconds  | 5%   
| Anchor | 1-2 seconds  | 33%   
| Golem Fist | 2 seconds  | 33%   
| Nano Bullet | 1–3 seconds  | 100%   
| Flask of Nanites | 1–3 seconds  | 100%   
From  | Duration  | Chance   
---|---|---  
##### Broken_Armor #####
From  | Duration  | Chance   
---|---|---  
| Paladin's Hammer | 10–20 seconds  | 100%   
From  | Duration  | Chance   
---|---|---  
| Armored Skeleton | 2 / 4 / 5 minutes  | 1/6 (16.67%)  
| Blue Armored Bones | 10 / 20 / 25 seconds  | 1/2 (50%)  
| Brain of Cthulhu | 9.73-19.5 / 12.17-24.37 seconds  | 11/243 (4.53%)  
| Creeper | 9.73-19.5 / 12.17-24.37 seconds  | 11/81 (13.58%)  
From  | Duration  | Chance   
---|---|---  
| Red Potion**** __(Desktop, Console and Mobile versions)(except For the Worthy and Zenith "Zenith \(seed\)") worlds) | 1 / 2 / 3 / hours  | 1/1 (100%)  
##### Chilled #####
From  | Duration  | Chance   
---|---|---  
| Ice Slime | 10 / 20 / 25 seconds  | 1/12 (8.33%)  
| Spiked Ice Slime | 20 / 40 / 50 seconds  | 1/1 (100%) (both contact and Ice Spike)   
| Ice Bat | 15 / 30 / 37.5 seconds  | 1/15 (6.67%)  
| Ice Golem | 45 / 90 / 112.5 seconds  | 1/1 (100%) (Frost Beam)   
| Icy Merman | 25 / 50 / 62.5 seconds  | 1/1 (100%) (Icewater Spit)   
| Ice Queen | 5 / 10 / 12.5 seconds  | 1/2 (50%) (Frost Wave)   
10 / 20 / 25 seconds  | 1/2 (50%) (Frost Wave)   
5 / 10 / 12.5 seconds  | 1/3 (33.33%) (Frost Shard)   
10 / 20 / 25 seconds  | 1/3 (33.33%) (Frost Shard)   
From  | Duration  | Chance   
---|---|---  
| Waterin Snow biome | 5 / 6.25 seconds  | 1/1 (100%)  
##### Frozen #####
From  | Duration  | Chance   
---|---|---  
| Spiked Ice Slime | 1 / 2 / 2.5 second(s)  
1.5 / 3 / 3.75 seconds  | 1/15 (6.67%) / 13/125 (10.4%)  
| Deerclops**** __(Desktop, Console and Mobile versions) | 0.33 / 0.67 / 0.83 seconds  | 1/1 (100%) (Ice Spike attack)   
| Ice Bat | 1 / 2 / 2.5 second(s)  | 1/35 (2.86%) / 69/1225 (5.63%)  
| Ice Golem | 1 / 2 / 2.5 second(s)  | 1/5 (20%) (Beam attack)   
| Icy Merman | 0.5–2 / 1–4 / 1.25–5 second(s)  | 1/10 (10%) (Spit attack)   
| Ice Queen | 0.33–1 / 0.67–2 / 0.83–2.5 second(s)  | 127/768 (16.54%), see Ice Queen § Notes  
##### Electrified #####
From | Duration | Chance | Total damage  
---|---|---|---  
Tesla Turret | 5 seconds  | 2/3 (66.67%) | 20 / 100   
Gigazapper | 4-8 seconds  | 1/1 (100%) | 16-32 / 80-160   
##### Mana_Sickness #####
From | Duration   
---|---  
Lesser Mana Potion | 5 seconds   
##### Burning #####
From  | Duration   
---|---  
Meteorite | While in contact   
From  | Duration  | Chance   
---|---|---  
| Hell Slime | 1-3 seconds  | 1/1 (100%)  
##### Midas #####
From  | Duration  | Chance   
---|---|---  
| Flask of Gold | 2 seconds  | 100%   
| Golden Bullet | 2 seconds  | 100%   
##### Daybroken #####
From  | Duration  | Chance   
---|---|---  
| Daybreak | 5 seconds  | 100%   
| Solar Eruption | 5 seconds  | 100%   
##### Stinky #####
From  | Duration  | Chance   
---|---|---  
| Poo**** __(Desktop, Console and Mobile versions) | 3 seconds  | 100%   
| Poo Boulder**** __(Desktop, Console and Mobile versions) | 10 seconds (on contact when rolling)  
3 seconds (standing atop it) | 100%   
From  | Duration  | Chance   
---|---|---  
| Flymeal**** __(Desktop, Console and Mobile versions) | 5 seconds  | 100%   
| Stink Potion | 30 seconds  | 100%   
From  | Duration  | Chance   
---|---|---  
| Poo Slime**** __(Desktop, Console and Mobile versions) | 5-10 / 10-20 / 12-25 seconds  | 1/1 (100%)

```


---

## 🤖 Assistant · 2026-08-12T18:29:11.966Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Excellent, very rich. Now I need the remaining details:
- On Fire! full causes (I have partial) and notes about Oiled.
- Cursed Inferno history 1.4.1/1.4.0.1 content.
- Bleeding 1.4.5.0, Burning 1.4.5.0, Confused 1.4.5.0, Darkness 1.4.0.1/1.3.0.1, Stinky 1.4.5.0 content.
- Mana Sickness page details (the −25% × mechanic and notes).
- Suffocation page (20 DPS, sources: sand/silt/slush).
- Chilled page (0.75×; also from water in snow biome 5s/6.25s).
- Midas page (10–50% more coins; 2s).
- Electrified notes (DPS 20 moving / 4 idle; durations 4–8).
- Frozen (0.33–2s).
- Poisoned page notes (2 vs 6).
- Acid Venom (legacy Venom 1.2: Venom used to deal 25? Let me check Legacy_Venom page existence).

Also buffs. Big set. Buff index in Buffs.md gave many values: Ammo Reservation 20%/8min, Battle 2× spawn/7min, Builder 25% placement speed +1 tile range/45min, Calm −17%/12min, Crate doubles/4min, Dangersense/10min, Endurance −10%/4min, Featherfall/10min, Fishing +15/8min, Flipper/8min, Gills/4min, Gravitation/3min, Heartreach/8min, Hunter/8min, Inferno/4min, Invisibility/3min, Ironskin +8 def/8min, Lifeforce +20% max life/8min, Magic Power +20% magic dmg/4min, Mana Regen/8min, Mining +25%/10min, Night Owl/10min, Obsidian Skin/6min, Rage +10% crit/4min, Regeneration +2 HP/s/8min, Shine/10min, Sonar/8min, Spelunker/5min, Summoning +1 minion/8min, Swiftness +25%/8min, Titan/8min, Warmth/15min, Wrath +10% dmg/4min.

I still need per-potion page details: Clairvoyance (Crystal Ball: +20 max mana, +5% magic damage, +2% magic crit, −2% mana usage), Sharpened (armor penetration +12? — the index says 12; individual page may say "increases armor penetration of melee weapons by 12"... hmm I recall it's 12? Actually Sharpening Station grants "Sharpened" = +12 armor penetration? I thought it was 8 in old gen and 12 in 1.4? Let me verify), Bewitched (+1 minion), Ammo Box (20% chance), Strategist/War Table (+1 sentry), Warmth potion details, Titan details, Heartreach details, Inferno details, Tipsy details, Well Fed tiers details (stats per tier), Fishing/Sonar/Crate numbers, Mining/Builder numbers.

Also potion durations: the index gave them. Potion pages may also state "duration increased by Alchemy Flask +20%".

Buff-station pages: Campfires (Cozy Fire +0.5 HP/s, ×1.1 healing), Heart Lantern (+1 HP/s), Star in a Bottle (+2 MP/s... "about 2 MP/s"), Sunflower (+10% move speed, −17% spawns), Peace Candle (−23% spawn rate, −30% max on-screen), Water Candle (1.33× spawn, 1.5× max), Bast Statue (+5 def; also "Bast set"? The task said "Bast Statue (Cat set)" — probably refers to Cat set vanity granting... no. Actually there's "Bast Statue" giving +5 defense), Garden Gnome (+0.4 luck? "increases luck by 0.2"? Let me check), Slice of Cake (Sugar Rush +20% move & mining speed, 2 min), Torch God luck (torch luck up to +0.2; "torch god's favor"? Torch God page has luck numbers), War Table (Strategist +1 sentry), Bewitching Table (Bewitched +1 minion), Sharpening Station (Sharpened +12 armor pen), Crystal Ball (Clairvoyance), Ammo Box station (20% ammo save, infinite while... actually "10 minutes"? The index said Infinite — need to check the Ammo_Box.md page: the buff lasts 10 minutes I believe. Let me read), Ammo Reservation potion (20%, 8 min).

Let me now read the buff-station pages and potion pages. I'll do targeted greps for the effect statements.

First batch: Ammo_Box.md, Sharpening_Station.md, Bewitching_Table.md, War_Table.md, Crystal_Ball.md, Slice_of_Cake.md, Bast_Statue.md, Garden_Gnome.md.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:29:11.970Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && for f in \"Ammo_Box\" \"Sharpening_Station\" \"Bewitching_Table\" \"War_Table\" \"Crystal_Ball\" \"Slice_of_Cake\" \"Bast_Statue\" \"Garden_Gnome\"; do echo \"##### $f #####\"; grep -n -E '20% chance|armor penetration|minion|sentry|maximum mana|magic damage|critical strike|mana usage|mining speed|movement|defense|luck|HP/s|health per second|mana per second|10 minutes|8 minutes|2 minutes|infinite|Infinite' \"$f.md\" | head -8; done",
 "description": "Extract effects from buff-station pages"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:29:21.644Z

**📎 ToolResult**

```
##### Ammo_Box #####
25:20% chance to save ammo_  
35:Buff tooltip|  _20% chance to save ammo_  
36:Duration| Infinite  
71:    * Buff duration of 10 minutes removed. The buff now lasts until the player dies or leaves the world.
696:  * [](Unlucky_Yarn.md "Black Cat")[Black Cat](Unlucky_Yarn.md "Unlucky Yarn")
##### Sharpening_Station #####
24:Melee weapons have armor penetration_  
34:Buff tooltip|  _Melee weapons have armor penetration_  
35:Duration| Infinite  
49:Placing and pressing [`⚷ Open / Activate`](Game_controls.md "Game controls") on the Sharpening Station grants the **Sharpened** [buff](Buff "Buff"), which increases [armor penetration](Armor_penetration.md "Armor penetration") of [melee weapons](Melee_weapons.md "Melee weapons") and melee projectiles by 12. This lasts until the player [dies](Death.md "Death") or leaves the world, but can be canceled at any time by right-clicking the icon ([](Desktop_version_history.md "Desktop version")), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff ([](Console_version.md "Console version")), or by double-tapping the buff icon ([](Mobile_version.md "Mobile version")). 
69:    * Buff duration of 10 minutes removed. The buff now lasts until the player dies or leaves the world.
694:  * [](Unlucky_Yarn.md "Black Cat")[Black Cat](Unlucky_Yarn.md "Unlucky Yarn")
1361:  *[10 minutes]: Expert Mode
1362:  *[12 minutes 30 seconds]: Master Mode
##### Bewitching_Table #####
24:Increased your max number of minions by 1_  
34:Buff tooltip|  _Increased your max number of minions by 1_  
35:Duration| Infinite  
49:Pressing [`⚷ Open / Activate`](Game_controls.md "Game controls") on a placed Bewitching Table grants the **Bewitched** [buff](Buff "Buff"), which increases the player's [minion](Minion "Minion") capacity by 1. This lasts until the player [dies](Death.md "Death") or leaves the world, but can be canceled at any time by right-clicking the icon ([](Desktop_version_history.md "Desktop version")), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff ([](Console_version.md "Console version")), or by double-tapping the buff icon ([](Mobile_version.md "Mobile version")). 
74:  * The Bewitching Table does not have an effect on [sentry](Sentry "Sentry") capacity. The latter can be increased by the [War Table](War_Table.md "War Table").
92:    * Buff duration of 10 minutes removed. The buff now lasts until the player dies or leaves the world.
714:  * [](Unlucky_Yarn.md "Black Cat")[Black Cat](Unlucky_Yarn.md "Unlucky Yarn")
##### War_Table #####
34:Duration| Infinite  
63:Placing and pressing [`⚷ Open / Activate`](Game_controls.md "Game controls") on the War Table grants the **Strategist** [buff](Buff "Buff"), which increases the player's [sentry](Sentry "Sentry") capacity by 1. This lasts until the player [dies](Death.md "Death") or leaves the world, but can be canceled at any time by right-clicking the icon ([](Desktop_version_history.md "Desktop version")), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff ([](Console_version.md "Console version")), or by double-tapping the buff icon ([](Mobile_version.md "Mobile version")). 
71:  * The War Table can be used outside of the Old One's Army event, and it increases the summoning cap of any sentry.
708:  * [](Unlucky_Yarn.md "Black Cat")[Black Cat](Unlucky_Yarn.md "Unlucky Yarn")
1372:  *[10 minutes]: Expert Mode
1373:  *[12 minutes 30 seconds]: Master Mode
1627:  *[10 minutes]: Expert Mode
1772:  *[2 minutes 3 seconds]: Master Mode
##### Crystal_Ball #####
36:Duration| Infinite  
59:  * +5% magic damage
60:  * +2% magic [critical strike chance](Critical_strike_chance "Critical strike chance")
61:  * −2% mana usage
235:    * Buff duration of 10 minutes removed. The buff now lasts until the player dies or leaves the world.
867:  * [](Unlucky_Yarn.md "Black Cat")[Black Cat](Unlucky_Yarn.md "Unlucky Yarn")
1544:  *[10 minutes]: Expert Mode
1545:  *[12 minutes 30 seconds]: Master Mode
##### Slice_of_Cake #####
33:Buff tooltip|  _20% increased movement and mining speed_  
34:Duration| 2 minutes  
54:Placing and pressing [`⚷ Open / Activate`](Game_controls.md "Game controls") on the Slice of Cake grants the **Sugar Rush** [buff](Buff "Buff"), which grants +20% [movement speed](Movement_speed.md "Movement speed") and +20% [mining speed](Mining_speed "Mining speed"). This lasts for 2 minutes, but can be canceled at any time by right-clicking the icon ([](Desktop_version_history.md "Desktop version")), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff ([](Console_version.md "Console version")), or by double-tapping the buff icon ([](Mobile_version.md "Mobile version")). 
694:  * [](Unlucky_Yarn.md "Black Cat")[Black Cat](Unlucky_Yarn.md "Unlucky Yarn")
1356:  *[10 minutes]: Expert Mode
1357:  *[12 minutes 30 seconds]: Master Mode
1611:  *[10 minutes]: Expert Mode
1756:  *[2 minutes 3 seconds]: Master Mode
##### Bast_Statue #####
23:[Tooltip](Tooltips.md "Tooltips")|  _Increases defense by 5 when placed nearby_  
33:Duration| Infinite while in vicinity  
53:The **Bast Statue** is a [furniture](Furniture.md "Furniture") item that grants **The Bast Defense** [buff](Buff "Buff") to players in its vicinity, increasing their [defense](Defense.md "Defense") by 5. The buff effect can be toggled via [wire](Wire.md "Wire"). The Bast Statue can be found in [Sandstone Chests](Sandstone_Chest.md "Sandstone Chest") in the lower 3/7ths of the [Underground Desert](Underground_Desert.md "Underground Desert") and in [Oasis Crates](Oasis_Crate.md "Oasis Crate") and [Mirage Crates](Mirage_Crate.md "Mirage Crate") obtained from [fishing](Fishing.md "Fishing") in the [Oasis](Oasis.md "Oasis"). It can also be found as a furniture in [Underground Desert Cabins](Underground_Cabin.md "Underground Cabin"). 
59:  * Multiple statues will not stack their effects. Two Bast Statues in a player's vicinity will still only grant +5 defense.
64:  * The buff name "The Bast Defense" is a pun on the phrase "[the best defense is a good offense](https://en.wikipedia.org/wiki/en:the_best_defense_is_a_good_offense "wikipedia:en:the best defense is a good offense")", a proverb commonly used as the prime strategic principle of war.
693:  * [](Unlucky_Yarn.md "Black Cat")[Black Cat](Unlucky_Yarn.md "Unlucky Yarn")
##### Garden_Gnome #####
32:The **Garden Gnome** is a small [furniture](Furniture.md "Furniture") item formed when a [Gnome](Gnome.md "Gnome") touches sunlight. A placed Garden Gnome positively influences the player's [Luck](Luck#Garden_Gnomes "Luck") stat by 0.2. The buff is applied to any players standing within a rectangular area of 170×125[1] tiles centered on the Garden Gnome, similar to the [Heart Lantern](Heart_Lantern.md "Heart Lantern"). Additional Garden Gnomes do not increase luck further. 
69:  * Unlike other buff furniture, the Garden Gnome does not apply a visible [buff](Buff "Buff") to the player to show that its effect is active. One can improvise by placing another area-effect object (such as a [Campfire](Campfire "Campfire") or [Sunflower](Sunflower.md "Sunflower")) next to the Garden Gnome and looking for that buff icon to estimate whether the luck bonus is being applied.
75:  * The following are the amount of Garden Gnomes needed for making its luck increase available everywhere for each [world size](World_size.md "World size"). 
592:  *[10 minutes]: Expert Mode
593:  *[12 minutes 30 seconds]: Master Mode
847:  *[10 minutes]: Expert Mode

```


---

## 🤖 Assistant · 2026-08-12T18:29:30.599Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Excellent. Now Crystal Ball details (lines 55-62) — I have partial; need "+20 maximum mana". Let me read lines 52-64 of Crystal_Ball.md.

Also Campfires.md, Heart_Lantern.md, Star_in_a_Bottle.md, Sunflower.md, Peace_Candle.md, Water_Candle.md, The_Torch_God.md (luck), and potions.

Let me batch: read Crystal_Ball lines 50-64; grep the environmental pages.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:29:30.819Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Crystal_Ball.md",
 "limit": 14,
 "offset": 50
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:29:30.823Z

**📎 ToolResult**

```
50	> Are you here for a peek at my crystal ball?
51	> 
52	> —  The [Wizard](Wizard.md "Wizard")
53	
54	The **Crystal Ball** is a [Hardmode](Hardmode.md "Hardmode") [furniture](Furniture.md "Furniture") item which functions as a [crafting station](Crafting_station "Crafting station"). It is purchased from the [Wizard](Wizard.md "Wizard") for 10 _GC_. Pressing [`⚷ Open / Activate`](Game_controls.md "Game controls") on a placed Crystal Ball grants the **Clairvoyance** [buff](Buff "Buff") and opens its crafting menu. 
55	
56	The Clairvoyance buff boosts the following magic-related stats: 
57	
58	  * +20 maximum [mana](Mana.md "Mana")
59	  * +5% magic damage
60	  * +2% magic [critical strike chance](Critical_strike_chance "Critical strike chance")
61	  * −2% mana usage
62	
63	The Clairvoyance buff lasts until the player [dies](Death.md "Death") or leaves the world. The buff can be canceled at any time by right-clicking the icon ([](Desktop_version_history.md "Desktop version")), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff ([](Console_version.md "Console version")), or by double-tapping the buff icon ([](Mobile_version.md "Mobile version")). 

```


---

## 🤖 Assistant · 2026-08-12T18:29:31.952Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && for f in \"Campfires\" \"Heart_Lantern\" \"Star_in_a_Bottle\" \"Sunflower\" \"Peace_Candle\" \"Water_Candle\"; do echo \"##### $f #####\"; grep -n -E '0\\.5|1\\.1|HP/s|health per second|mana per second|MP/s|1\\.33|1\\.5|17%|23%|30%|10%|170.125|170×125|range' \"$f.md\" | head -8; done",
 "description": "Extract environmental buff numbers"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:29:59.958Z

**📎 ToolResult ⚠️ERROR**

```
glm-x-preview-260804[1m] is temporarily unavailable, so auto mode cannot determine the safety of Bash right now. Wait briefly and then try this action again. If it keeps failing, continue with other tasks that don't require this action and come back to it later. Note: reading files, searching code, and other read-only operations do not require the classifier and can still be used.

```


---

## 🤖 Assistant · 2026-08-12T18:30:01.962Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The Bash classifier is temporarily unavailable. I can still use Read. Let me use Read for the environmental pages. I'll read the relevant portions. These files are long (nav boilerplate), but the content is near the top (~lines 30-80). Let me read tops of Campfires.md, Heart_Lantern.md, Star_in_a_Bottle.md, Sunflower.md, Peace_Candle.md, Water_Candle.md.

Read tool with limit ~60 each, in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:30:02.220Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Campfires.md",
 "limit": 45,
 "offset": 40
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:30:02.228Z

**📎 ToolResult**

```
40	
41	The **Campfire** is a type of [furniture](Furniture.md "Furniture") and [crafting station](Crafting_station "Crafting station") that emits light and provides the **Cozy Fire** [buff](Buff "Buff") to players in its vicinity. A Campfire can be turned off by pressing the [`⚷ Open / Activate`](Game_controls.md "Game controls") on the object or by sending it a [wire](Wire.md "Wire") signal, and can be toggled back on again the same way. It is also used to cook a [Marshmallow on a Stick](Marshmallow_on_a_Stick.md "Marshmallow on a Stick"). 
42	
43	The Cozy Fire buff increases the [health regeneration](Health_regeneration.md "Health regeneration") rate of nearby players by 10% and adds an additional constant 0.5 health per second. The buff is applied to all players who are within a rectangular area of 170×125[1] tiles centered on the Campfire, similar to the [Heart Lantern](Heart_Lantern.md "Heart Lantern"). The regeneration buffs from both items will stack together to provide a greater regeneration boost, and being within range of these items can also help to counteract the effects of damaging [debuffs](Debuffs.md "Debuffs") (such as [Poisoned](Poisoned.md "Poisoned") and [On Fire!](On_Fire!.md "On Fire!")). 
44	
45	The [Fireplace](Fireplace.md "Fireplace") operates similarly and provides the same Cozy Fire buff, but does not function as a crafting station and cannot cook a Marshmallow on a Stick. 
46	
47	## Crafting
48	
49	### Recipes
50	
51	Result| Ingredients| [Crafting station](Crafting_station "Crafting station")  
52	---|---|---  
53	Aether Campfire**** __(Desktop, Console and Mobile versions) Internal [Item ID](Item_IDs.md "Item IDs"): 5357| 
54	
55	  * [](Any_Wood.md "Any Wood")[Any Wood](Any_Wood.md "Any Wood")10
56	  * [](Aether_Torch.md "Aether Torch")[Aether Torch](Aether_Torch.md "Aether Torch")**** __(Desktop, Console and Mobile versions) 5
57	
58	| [By Hand](By_Hand.md "By Hand")  
59	Bone Campfire**** __(Desktop, Console and Mobile versions) Internal [Item ID](Item_IDs.md "Item IDs"): 3724| 
60	
61	  * [](Any_Wood.md "Any Wood")[Any Wood](Any_Wood.md "Any Wood")10
62	  * [](Bone_Torch.md "Bone Torch")[Bone Torch](Bone_Torch.md "Bone Torch")**** __(Desktop, Console and Mobile versions) 5
63	
64	  
65	[](Desktop_version_history.md "Desktop version") [](Console_version.md "Console version") [](Mobile_version.md "Mobile version") only:CampfireInternal [Item ID](Item_IDs.md "Item IDs"): 966| 
66	
67	  * [](Any_Wood.md "Any Wood")[Any Wood](Any_Wood.md "Any Wood")10
68	  * [](Torch.md "Torch")[Torch](Torch.md "Torch")5
69	
70	  
71	Coral Campfire**** __(Desktop, Console and Mobile versions) Internal [Item ID](Item_IDs.md "Item IDs"): 4690| 
72	
73	  * [](Any_Wood.md "Any Wood")[Any Wood](Any_Wood.md "Any Wood")10
74	  * [](Coral_Torch.md "Coral Torch")[Coral Torch](Coral_Torch.md "Coral Torch")**** __(Desktop, Console and Mobile versions) 5
75	
76	  
77	Corrupt Campfire**** __(Desktop, Console and Mobile versions) Internal [Item ID](Item_IDs.md "Item IDs"): 4691| 
78	
79	  * [](Any_Wood.md "Any Wood")[Any Wood](Any_Wood.md "Any Wood")10
80	  * [](Corrupt_Torch.md "Corrupt Torch")[Corrupt Torch](Corrupt_Torch.md "Corrupt Torch")**** __(Desktop, Console and Mobile versions) 5
81	
82	  
83	Crimson Campfire**** __(Desktop, Console and Mobile versions) Internal [Item ID](Item_IDs.md "Item IDs"): 4692| 
84	

```


---

## 🤖 Assistant · 2026-08-12T18:30:02.480Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Heart_Lantern.md",
 "limit": 45,
 "offset": 40
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:30:02.488Z

**📎 ToolResult**

```
40	## Crafting
41	
42	### Recipes
43	
44	Result| Ingredients| [Crafting station](Crafting_station "Crafting station")  
45	---|---|---  
46	[](Heart_Lantern.md "Heart Lantern")Heart Lantern| 
47	
48	  * [](Life_Crystal.md "Life Crystal")[Life Crystal](Life_Crystal.md "Life Crystal")
49	  * [](Chain.md "Chain")[Chain](Chain.md "Chain")4
50	
51	| [By Hand](By_Hand.md "By Hand")  
52	  
53	## Notes
54	
55	  * In [Celebration Mk 10](Celebration_Mk_10.md "Celebration Mk 10")**** __(Desktop, Console and Mobile versions) and [Zenith](Zenith_\(seed\) "Zenith \(seed\)")**** __(Desktop, Console and Mobile versions) worlds, the Heart Lantern can be purchased from the [Princess](Princess.md "Princess") for 7 _GC_ 50 _SC_.
56	
57	## Tips
58	
59	  * As with the Campfire, it may be useful to keep a Heart Lantern in the [hotbar](Inventory#Hotbar_\(10_slots\) "Inventory") in dangerous areas, so that it can be placed easily for quicker regeneration.
60	  * It is also useful to have one placed permanently in the player's [base](Guide%3ABases "Guide:Bases"), along with a Campfire and a [honey](Honey.md "Honey") bath.
61	  * The combined and continuous health regeneration from Heart Lanterns, Campfires, and honey can make many [boss](Boss "Boss") fights less difficult. Including one or more of these in any arena is usually a good idea.
62	
63	## History
64	
65	[ Desktop version](Desktop_version_history.md "Desktop version history")
66	
67	  * [Desktop 1.4.4](Desktop_1.4.4 "Desktop 1.4.4"): 
68	    * Stack limit increased from 999 to 9999.
69	    * Can now be placed under platforms.
70	
71	  * [Desktop 1.4.2.3](Desktop_1.4.2.3 "Desktop 1.4.2.3"): Can now be purchased from the Princess in Celebrationmk10 worlds.
72	
73	  * [Desktop 1.4.0.1](Desktop_1.4.0.1 "Desktop 1.4.0.1"): Area of effect increased.
74	
75	  * [Desktop 1.2.3](Desktop_1.2.3 "Desktop 1.2.3"): 
76	    * Reduced Heart Lantern effect.
77	    * [Nurse](Nurse.md "Nurse") no longer charges for, or removes the potion cooldown, Heart Lantern, and [Campfire buffs](Campfire "Campfire").
78	
79	  * [Desktop 1.2.1.2](Desktop_1.2.1.2 "Desktop 1.2.1.2"): Introduced.
80	
81	[ Console version](Console_version.md "Console version")
82	
83	  * [Console 1.02](Console_1.02.md "Console 1.02"): Introduced.
84	

```


---

## 🤖 Assistant · 2026-08-12T18:30:03.922Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Heart_Lantern content is earlier (before line 40). Let me read lines 30-40. Also read Star_in_a_Bottle, Sunflower, Peace_Candle, Water_Candle tops.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:30:04.185Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Heart_Lantern.md",
 "limit": 12,
 "offset": 28
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:30:04.192Z

**📎 ToolResult**

```
28	---|---  
29	Buff tooltip|  _Life regen is increased_  
30	Duration| Infinite while in vicinity  
31	  
32	  * Internal [Item ID](Item_IDs.md "Item IDs"): **1859**
33	  * Internal [Tile ID](Tile_IDs.md "Tile IDs"): **42 (9)**
34	  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **89**
35	
36	The **Heart Lantern** is a functional [lantern](Lantern "Lantern") that grants the **Heart Lamp** [buff](Buff "Buff"), providing a [health regeneration](Health_regeneration.md "Health regeneration") of 1 HP per second to all players within a rectangular area of 170×125[1] ([](Desktop_version_history.md "Desktop version") [](Console_version.md "Console version") [](Mobile_version.md "Mobile version")) / 100×84 ([](Legacy%3AOld-gen_console_version "Old-gen console version") [](Legacy%3A3DS_version "Nintendo 3DS version")) tiles. 
37	
38	Like other lanterns, the Heart Lantern is a [mechanism](Mechanism "Mechanism") that can be toggled on or off if [wired](Wire.md "Wire"), though this does not affect the buff. 
39	

```


---

## 🤖 Assistant · 2026-08-12T18:30:04.756Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Star_in_a_Bottle.md",
 "limit": 18,
 "offset": 28
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:30:04.762Z

**📎 ToolResult**

```
28	  
29	Grants [Buff](Buffs.md "Buffs")
30	
31	Buff| [](Star_in_a_Bottle.md "Star in a Bottle")Star in a Bottle  
32	---|---  
33	Buff tooltip|  _Increased mana regeneration_  
34	Duration| Infinite while in vicinity  
35	  
36	  * Internal [Item ID](Item_IDs.md "Item IDs"): **1431**
37	  * Internal [Tile ID](Tile_IDs.md "Tile IDs"): **42 (7)**
38	  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **158**
39	
40	The **Star in a Bottle** is a functional [lantern](Lantern "Lantern") that grants the **Star in a Bottle** [buff](Buff "Buff"), providing [mana](Mana.md "Mana") regeneration of 5 mana per second to all players within a rectangular area of 170×125[1] tiles. 
41	
42	Like other lanterns, the Star in a Bottle is a [mechanism](Mechanism "Mechanism") that can be toggled on or off if [wired](Wire.md "Wire"), though this does not affect the buff. 
43	
44	## Crafting
45	

```


---

## 🤖 Assistant · 2026-08-12T18:30:07.526Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting: Star in a Bottle page says 5 mana per second, while Buffs.md index says "about 2 MP/s". That's a discrepancy worth reporting! The wiki: actual effect is +2 mana/s? Hmm. In 1.4 the Star in a Bottle reduces mana regeneration delay by 10 frames? The wiki page here says 5 mana per second. I'll report both with citations.

Now Sunflower, Peace Candle, Water Candle, Torch God.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:30:07.751Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Sunflower.md",
 "limit": 16,
 "offset": 30
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:30:07.756Z

**📎 ToolResult**

```
30	
31	Buff| [](Sunflower.md "Happy!")Happy!  
32	---|---  
33	Buff tooltip|  _Movement speed increased and monster spawns reduced_  
34	Duration| Infinite while in vicinity  
35	  
36	  * Internal [Item ID](Item_IDs.md "Item IDs"): **63**
37	  * Internal [Tile ID](Tile_IDs.md "Tile IDs"): **27**
38	  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **146**
39	
40	Naturally generated Sunflowers in a [Forest](Forest.md "Forest").
41	
42	"Happy" redirects here. For the NPC attribute, see [NPC happiness](NPC_happiness.md "NPC happiness"). 
43	
44	The **Sunflower** is a large, tall [plant](Plants.md "Plants") which can be found growing naturally on [grass](Grass "Grass"), and can be broken with a [pickaxe](Pickaxe "Pickaxe") or [drill](Drill "Drill"), or by coming into contact with [water](Water.md "Water"). It cannot be grown from [seeds](Seeds.md "Seeds") like most other plants, but is instead placed fully-grown, either naturally upon world generation or by the player. It can also be purchased from the [Dryad](Dryad.md "Dryad") for 50 _SC_ each, while a [Blood Moon](Blood_Moon.md "Blood Moon") is not occurring. 
45	

```


---

## 🤖 Assistant · 2026-08-12T18:30:08.025Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Peace_Candle.md",
 "limit": 16,
 "offset": 28
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:30:08.034Z

**📎 ToolResult**

```
28	Grants [Buff](Buffs.md "Buffs")
29	
30	Buff| [](Peace_Candle.md "Peace Candle")Peace Candle  
31	---|---  
32	Buff tooltip|  _Decreased monster spawn rate_  
33	Duration| Infinite while in vicinity  
34	  
35	  * Internal [Item ID](Item_IDs.md "Item IDs"): **3117**
36	  * Internal [Tile ID](Tile_IDs.md "Tile IDs"): **372**
37	  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **157**
38	
39	For a complete list of candles, see [Candle](Candle "Candle"). 
40	
41	The **Peace Candle** is a [furniture](Furniture.md "Furniture") item that emits a low amount of light and can be placed only on [flat-surface items](Flat-surface_items.md "Flat-surface items"). When placed or held, it gives nearby players the **Peace Candle** [buff](Buff "Buff"). 
42	
43	The Peace Candle buff decreases spawn rates by 23% in the area and decreases the maximum number of simultaneous on-screen enemies by 30%. The buff is applied to any players holding a Peace Candle or standing within a rectangular area of 170×125[1] tiles centered on a Peace Candle. In order to be considered "holding" the candle, it must be in the player's [hotbar](Hotbar.md "Hotbar") and currently selected; merely being in a player's inventory will not suffice. Multiple Candles will not stack with each other, even if one is placed and the other held. Peace Candles can only be placed on [platforms](Platforms.md "Platforms") and flat [furniture](Furniture.md "Furniture") items like [Work Benches](Work_Benches.md "Work Benches") and [Tables](Tables.md "Tables"). 

```


---

## 🤖 Assistant · 2026-08-12T18:30:13.521Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Peace Candle: −23% spawn rate, −30% max on-screen. Good.

Sunflower effect (+10% move speed, −17% spawn) is stated in Buffs.md index (line 141). Let me check the Sunflower page for the numeric statement. It's probably a bit further down. Let me read lines 46-56.

Also Water Candle page. And Torch God.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:30:13.748Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Sunflower.md",
 "limit": 8,
 "offset": 46
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:30:13.756Z

**📎 ToolResult**

```
46	Sunflowers can only be placed on regular, Hallowed, Jungle, or Ash grass, at any height. They cannot be placed on Corrupt grass, Crimson grass, Mushroom grass, bare [Dirt Blocks](Dirt_Block.md "Dirt Block"), nor in [Clay Pots](Clay_Pot.md "Clay Pot") or [Planter Boxes](Planter_Boxes.md "Planter Boxes"). 
47	
48	Sunflowers grant the **Happy!** [buff](Buff "Buff") to players in their vicinity, increasing their movement speed and reducing [enemy](Enemy "Enemy") spawns. Furthermore, they serve as a small barrier against the spread of the [Corruption](Corruption "Corruption")/[Crimson](Crimson "Crimson") and [Hallow](Hallow "Hallow"), negate some of the effects of the evil biomes, and help preventing [Graveyard](Graveyard.md "Graveyard") biomes from forming. 
49	
50	## Effects
51	
52	A placed Sunflower provides the following functions: 
53	

```


---

## 🤖 Assistant · 2026-08-12T18:30:14.000Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Water_Candle.md",
 "limit": 18,
 "offset": 38
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:30:14.005Z

**📎 ToolResult**

```
38	  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **86**
39	
40	For a complete list of candles, see [Candle](Candle "Candle"). 
41	
42	The **Water Candle** is a [furniture](Furniture.md "Furniture") item that emits a low amount of light, and can be placed only on [flat-surface items](Flat-surface_items.md "Flat-surface items"). When placed or held, it gives nearby players the **Water Candle** [debuff](Debuff "Debuff"). 
43	
44	The Water Candle debuff increases all [enemy](Enemy "Enemy") and [critter](Critter "Critter") spawn rates by 33%, and increases the maximum number of simultaneous on-screen enemies by 50%. The debuff is applied to any players holding or standing within a rectangular area of 170×125[1] tiles centered on a Water Candle. In order to be considered "holding" the candle, it must be in the player's [hotbar](Hotbar.md "Hotbar") and currently selected; merely being in a player's inventory will not suffice. Multiple candles will not stack with each other, even if one is placed and the other held. 
45	
46	Several Water Candles are found commonly on the shelves of the [Dungeon](Dungeon.md "Dungeon"). They can also be crafted at a [Crystal Ball](Crystal_Ball.md "Crystal Ball"). 
47	
48	Placed Water Candles can be shut off by pressing the [`⚷ Open / Activate`](Game_controls.md "Game controls") button on them, and will toggle when activated via [wiring](Wiring "Wiring"). Water Candles that are turned off will not activate the Water Candle debuff. 
49	
50	The Water Candle's effect is the opposite of the [Peace Candle](Peace_Candle.md "Peace Candle"), which decreases enemy spawn rates. If a Peace Candle and a Water Candle are active at the same time, neither have any effect on spawn rates. Conversely, the Water Candle's effect stacks with that of the [Battle Potion](Battle_Potion.md "Battle Potion"). 
51	
52	## Crafting
53	
54	### Recipes
55	

```


---

## 🤖 Assistant · 2026-08-12T18:30:17.675Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Water Candle: +33% spawn rate, +50% max on-screen (Buffs/Debuffs index phrased as 1.33× and 1.5×). Also note: Water Candle effect stacks with Battle Potion; Peace+Water cancel.

Sunflower Effects section — read lines 53-60 for numeric values.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:30:17.930Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Sunflower.md",
 "limit": 14,
 "offset": 53
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:30:17.935Z

**📎 ToolResult**

```
53	
54	  * The two tiles directly underneath it cannot become [Corrupted](The_Corruption.md "The Corruption"), [Crimsoned](The_Crimson.md "The Crimson"), or [Hallowed](The_Hallow.md "The Hallow"), even in [Hardmode](Hardmode.md "Hardmode"). In some cases, this can prevent Corrupted and Crimson grass from spreading sideways. It also blocks other conversions in a small area around it. _See[Biome spread](Biome_spread.md "Biome spread") for details._
55	  * Each Sunflower decreases an area's evil biome [tile count](Biomes#Biome_existence_requirements "Biomes") by 80 tiles.[1] Furthermore, when determing whether [NPCs](NPCs.md "NPCs") will reject a [house](House.md "House"), each Sunflower in the area decreases the [evil score](House#Evil_score "House") by 40 points.[2] If placed in large quantities, Sunflowers can allow NPCs to live near evil biomes. For the exact size of each area, see [Biomes § Biome existence requirements](Biomes#Biome_existence_requirements "Biomes") and [House](House.md "House") respectively.
56	  * It provides the Happy! [buff](Buff "Buff") to players within a rectangular area of 170×125[3] tiles centered on the Sunflower, which grants +10% [movement speed](Movement_speed.md "Movement speed"), a ×1.1 movement speed multiplier to itself and all movement speed buffs to the left of it in the buff list (effectively making the buff granting +21% movement speed), as well as 17% reduction to [spawn rates](Spawn_rate.md "Spawn rate") and 20% reduction to max spawns. 
57	    * It does not provide the Happy! buff if there are at least 5 [Tombstones](Tombstones.md "Tombstones") in the same area.
58	  * It helps to prevent [Graveyard](Graveyard.md "Graveyard") biomes from forming by canceling out one [Tombstone](Tombstones.md "Tombstones") each.
59	
60	## Notes
61	
62	  * The Sunflower's Happy! buff stacks with the effect of the [Peace Candle](Peace_Candle.md "Peace Candle"), as well as the movement speed buff of [Asphalt Blocks](Asphalt_Block.md "Asphalt Block"). 
63	    * This does not affect top running speed when equipped with [Movement Accessories](Movement_Accessories.md "Movement Accessories") such as the [Hermes Boots](Hermes_Boots.md "Hermes Boots") or their upgrades.
64	  * The Happy! buff reduces [critter](Critter "Critter") spawns, so if the player would like to collect [bait](Bait.md "Bait"), it is wise to remove any nearby Sunflowers.
65	  * The Sunflower emits faint light but does not count as a valid [light source](Light_source "Light source") for [housing](Housing "Housing"). The petals of the Sunflower are fully bright in the dark.
66	

```


---

## 🤖 Assistant · 2026-08-12T18:30:18.263Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Torch_God.md",
 "limit": 60,
 "offset": 40
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:30:18.268Z

**📎 ToolResult**

```
40	  * Torch fireballs match the color of the Torch they are fired from. This is purely cosmetic; all fireball colors have the same behavior and stats.
41	  * If the world is left while the Torch God is still ongoing, spent Torches will not re-light. They will have to be reactivated or replaced.
42	  * Passing the event, dying, or leaving the world temporarily invalidates the existing Torches. They can re-initiate the event after a short delay if the area is re-entered.
43	  * Any combination of Torch types can be used to summon the Torch God.
44	  * Torches placed during the event can fire off at the player too.
45	  * Torch fireballs do not harm [critters](Critters.md "Critters"), enemies, or players who have already consumed the Torch God's Favor.
46	  * After the Torch God ends, there is a 60-second cooldown before the event can start again for a player.[7]
47	  * The [Bestiary](Bestiary.md "Bestiary") entry of the Torch God is unlocked once the Torch God's Favor is consumed.
48	
49	## Achievements
50	
51	[](Achievements#Torch_God "Achievements")
52	
53	**[Torch God](Achievements#Torch_God "Achievements")**  • _“Invoked the wrath of the God of Torches, and survived long enough to earn its blessing.”_
54	
55	Use the [Torch God's Favor](Torch_God's_Favor.md "Torch God's Favor").
56	
57	Category:  Slayer
58	
59	## Tips
60	
61	For more elaborate strategies on surviving The Torch God, including [arena](Arena "Arena") recommendations, see [Guide:The Torch God strategies](Guide%3AThe_Torch_God_strategies "Guide:The Torch God strategies"). 
62	
63	  * Starting the event in an open area offers the player more room to dodge.
64	  * Only proper Torches become part of the Torch God. Non-Torch [light sources](Light_sources.md "Light sources") like [lanterns](Lanterns.md "Lanterns") can provide light to the area without becoming fireballs.
65	  * Items that give the player a dodge chance, such as the [Brain of Confusion](Brain_of_Confusion.md "Brain of Confusion"), work against torch fireballs.
66	  * Taken as an agility challenge, having mobility items like [grappling hooks](Grappling_hooks.md "Grappling hooks") is preferred to help dodge the torch fireballs.
67	  * Taken as an endurance challenge, having [armor](Armor.md "Armor"), buffs, and accessories that offer high [defense](Defense.md "Defense") is preferred to reduce the damage from the torch fireballs.
68	  * The player can lessen enemy spawns using a [Calming Potion](Calming_Potion.md "Calming Potion") and [Peace Candle](Peace_Candle.md "Peace Candle") to reduce dangerous distractions from enemies, allowing the player to focus on dodging the fireballs. 
69	    * Alternatively, the player can activate the event in a [town](Town.md "Town") for a greater spawn reduction. If the player fails, however, that town may become inaccessible until the player either completes the event or removes the Torches.
70	  * Some Torches make their associated fireballs harder to see, while other Torches make it easier to see. The best, brightest Torch for dodging purposes is the [White Torch](White_Torch.md "White Torch"), but is made from [Diamonds](Diamond.md "Diamond") and thus may be resource-intensive. The second best Torch is the [Ultrabright Torch](Ultrabright_Torch.md "Ultrabright Torch"), and it is uncommonly sold from the [Traveling Merchant](Traveling_Merchant.md "Traveling Merchant"). The third best Torch is the [Ichor Torch](Ichor_Torch.md "Ichor Torch"). Depending on the environment, the [Ice Torch](Ice_Torch.md "Ice Torch"), [Hallowed Torch](Hallowed_Torch.md "Hallowed Torch"), and [Jungle Torch](Jungle_Torch.md "Jungle Torch") might be the fourth best.
71	  * The Torch God's Favor does not count as being in the inventory if it is in the [trash slot](Trash_slot.md "Trash slot"), in a [storage item](Storage_item "Storage item") like a [Chest](Chest "Chest"), or tossed to the ground. A player can use this to repeat the event.
72	
73	### Arena ideas
74	
75	A basic arena using a loop of [Minecart Tracks](Minecart_Track.md "Minecart Track").
76	
77	These are some brief ideas for creating a favorable environment to take the event in: 
78	
79	  * Create a large open area and line Torches around one edge to provide maximum dodging time.
80	  * Build a small, square arena with the Torches clustered in the center. Lay down [Ropes](Ropes.md "Ropes") and walkways to be able to circle the Torches.
81	  * Make a [hellevator](Hellevator.md "Hellevator") with a rope line and a Torch every 10 tiles, then place 101 Torches at the top and head down the rope line. By the time the player reaches the bottom, they should obtain Torch God's Favor.
82	  * Lay down a loop of [Minecart Tracks](Minecart_Track.md "Minecart Track") around a cluster of 101 Torches. [Hammer](Hammer "Hammer") the rails so that the Minecart rides in circles around the Torches, and make use of bumpers and rail intersections as necessary.
83	
84	## Trivia
85	
86	  * The Torch God, as well as its reward, was most likely introduced as a response to the controversial "[bad torch luck](Luck#Trivia "Luck")" feature introduced in [1.4.0.1](1.4.0.1.md "1.4.0.1"), which would punish players for using the wrong Torch type in a given biome (e.g. using Ice Torches in the Underground Jungle as opposed to Jungle Torches).
87	  * The Torch God was initially discussed on live stream by _[Terraria](Terraria.md "Terraria")_ streamer [Pedguin](https://www.twitch.tv/Pedguin) on May 24th, 2020, as a way for [Redigit](Redigit.md "Redigit") to punish players for placing the wrong Torch. Redigit commented in the chat that he liked the idea.
88	  * The Torch God event is called `HappyFunTorchTime` in the game's source code.
89	  * When shot, each fireball emits the sound used by several [casters](Caster "Caster") and [magic weapons](Magic_weapons.md "Magic weapons").
90	  * A Torch God NPC exists in-game, with an [NPC ID](NPC_IDs.md "NPC IDs") of `664`. It is classified as a [boss](Boss "Boss") and seems to be used for displaying the required info of the Torch God's [Bestiary](Bestiary.md "Bestiary") entry. 
91	    * If it is summoned via third-party software or [mods](Mods.md "Mods") and is killed, it would only drop 5–15 [Lesser Healing Potions](Lesser_Healing_Potion.md "Lesser Healing Potion") and some [Hearts](Heart.md "Heart"). Doing so would also unlock the Torch God's Bestiary entry.
92	    * While the "boss" is alive, the music [Boss 1](Boss_1.md "Boss 1") will play.
93	  * If the event is completed and the Torch God's Favor is consumed, it will become impossible for the player who consumed it to obtain the music box or its alternate variant alone. In that case, another character or player who has not consumed the Torch God’s Favor may complete the event and hand the Favor or music box to them.
94	  * The Torch God is one of the few entities in the Bestiary that has a 5-star rarity, making it one of the only 4 bosses with a 5-star rarity.
95	
96	  * The [Bestiary](Bestiary.md "Bestiary") entry for the The Torch God: _" An unseen deity responsible for a torch's eternal flicker, however easily angered by the unsightly, ungrateful abuse of torch placement."_
97	
98	## History
99	

```


---

## 🤖 Assistant · 2026-08-12T18:30:21.672Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Torch God page is about the event, not luck numbers. Torch-related luck numbers are on Luck.md and Torch_God's_Favor.md. Let me check Torch_God's_Favor.md and Luck.md torch section.

Then the potions. Let me now check Bash availability again — the classifier may be back. I'll try a Bash call for potion pages extraction.

Actually, let me use Read for Torch_God's_Favor.md top.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:30:21.949Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Torch_God's_Favor.md",
 "limit": 30,
 "offset": 20
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:30:21.954Z

**📎 ToolResult**

```
20	[Use time](Use_time.md "Use time")| 30 (Average)  
21	[Tooltip](Tooltips.md "Tooltips")|  _Unlocks an ability toggle to the left of the inventory  
22	When enabled normal torches change according to your biome_  
23	[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_4 "Light Red \(Rarity level: 4\)")  
24	[Sell](Value.md "Value")| 2 _GC_  
25	[Research](Journey_Mode#Research "Journey Mode")| 1 required  
26	  
27	Sounds
28	
29	Use|   
30	---|---  
31	|   
32	  
33	  * Internal [Item ID](Item_IDs.md "Item IDs"): **5043**
34	
35	Torch God's Favor [toggles](Toggles.md "Toggles")
36	
37	* * *
38	
39	[ Desktop](Desktop_version_history.md "Desktop version history") icons
40	
41	  
42	Off  
43	On
44	
45	[ Mobile](Mobile_version.md "Mobile version") icons
46	
47	  
48	Off  
49	On

```


---

## 🤖 Assistant · 2026-08-12T18:30:24.752Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Not luck numbers. Let me look at Luck.md torch section. And check Bash again.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:30:25.202Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && grep -n -iE 'torch.*luck|luck.*torch' Luck.md | head -12",
 "description": "Find torch luck numbers in Luck.md"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:30:25.225Z

**📎 ToolResult**

```
83:Only in the [Underground](Underground.md "Underground") layer and below, each type of torch present in a 81×81-tile rectangle centered on the player (and also any torch they are holding) will increase or reduce torch luck. By placing or holding [torches](Torches.md "Torches") in the correct locations, players can increase their luck.[8] Only a single torch is needed to trigger a luck bonus or penalty. Multiple torches of a given type have no increased benefit, and one or more incorrect torches will completely negate the benefits of torch luck. Torch luck can never go below 0; it either provides positive luck or none at all. 
85:Biome torches give good luck in their own biome, while giving a luck penalty in any other location (with exceptions). Ordinary torches give a penalty in most places with a corresponding biome torch, while Bone Torches give a bonus in biomes without their own biome torch (and also the [Ocean](Ocean.md "Ocean")). For [hybrid biomes](Hybrid_biome.md "Hybrid biome"), as long as all torches belong to one of the existing biomes, no penalty will be given. For example, having both Ice Torch and Hallowed Torches nearby in a Hallowed Snow biome still increases luck by 0.2. 
87:If the [Torch God's Favor](Torch_God's_Favor.md "Torch God's Favor") is toggled on, ordinary torches are automatically converted to the proper type when held and/or placed in the Hallow, Corruption, Crimson, Jungle, Desert and Snow biomes. Bone Torches, [Demon Torches](Demon_Torch.md "Demon Torch"), and [Aether Torches](Aether_Torch.md "Aether Torch") can also be automatically placed in the [Dungeon](Dungeon.md "Dungeon"), [Underworld](Underworld "Underworld"), or [Aether](Aether "Aether") respectively, but note that these torches do not affect torch luck in the respective location. 
89:Torch | Beneficial locations | Increased torch luck | Reduced torch luck   
110:  * Placed torches on the [Surface](Surface.md "Surface") and in [Space](Space.md "Space") are ignored. This means that in these layers, only held torches will affect luck.
111:  * Torch luck does not apply in the [Dungeon](Dungeon.md "Dungeon") or [Jungle Temple](Jungle_Temple.md "Jungle Temple"), or when [The Torch God](The_Torch_God.md "The Torch God") [event](Event "Event") is active.
112:  * Torches turned off (e.g. via [Wire](Wire.md "Wire")) will still affect luck.
142:  * In an [Underground Jungle](Underground_Jungle.md "Underground Jungle") biome with a single [Jungle Torch](Jungle_Torch.md "Jungle Torch"), a [Garden Gnome](Garden_Gnome.md "Garden Gnome"), with 5 minutes of the [Lucky](Lucky_\(buff\) "Lucky \(buff\)") buff remaining, on a [Lantern Night](Lantern_Night.md "Lantern Night"), one would get 28 of that drop on average. If it took an hour to farm for this drop, it now would take approximately 17 fewer minutes.
425:  * When introduced, mismatched [Torches](Torches.md "Torches") could result in a negative Torch luck value, reducing the final luck score. This was changed shortly after, in [1.4.0.3](1.4.0.3.md "1.4.0.3")**** __(Desktop, Console and Mobile versions) , after a Reddit post criticizing the mechanic garnered attention, causing a large community backlash.[27] Up until [1.4.5.0](1.4.5.0.md "1.4.5.0"), this change caused the Wizard's messages below −0.42 luck to become impossible to see in-game.
440:  * [Desktop 1.4.0.3](Desktop_1.4.0.3 "Desktop 1.4.0.3"): Negative luck influence from Torches capped at a minimum of 0. Incorrect Torches can still remove positive luck influence from Torches.
465:  8. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, methods `TryRecalculatingTorchLuck()` in `Terraria.Player.cs` and `UpdateTorchLuck_ConsumeCountersAndCalculate()` in `Terraria.Player.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.

```


---

## 🤖 Assistant · 2026-08-12T18:31:11.294Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Luck.md",
 "limit": 25,
 "offset": 89
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:31:11.302Z

**📎 ToolResult**

```
89	Torch | Beneficial locations | Increased torch luck | Reduced torch luck   
90	---|---|---|---  
91	[](Ice_Torch.md "Ice Torch")[Ice Torch](Ice_Torch.md "Ice Torch") | [Snow biome](Snow_biome.md "Snow biome"), [Underground Snow](Underground_Snow "Underground Snow") | 0.2 | 0.2   
92	[](Desert_Torch.md "Desert Torch")[Desert Torch](Desert_Torch.md "Desert Torch") | [Desert](Desert.md "Desert"), [Underground Desert](Underground_Desert.md "Underground Desert") | 0.2 | 0.2   
93	[](Jungle_Torch.md "Jungle Torch")[Jungle Torch](Jungle_Torch.md "Jungle Torch") | [Jungle](Jungle.md "Jungle"), [Underground Jungle](Underground_Jungle.md "Underground Jungle") | 0.2 | 0.2   
94	[](Hallowed_Torch.md "Hallowed Torch")[Hallowed Torch](Hallowed_Torch.md "Hallowed Torch") | [Hallow](Hallow "Hallow"), [Underground Hallow](Underground_Hallow.md "Underground Hallow") | 0.2 | 0.2   
95	[](Corrupt_Torch.md "Corrupt Torch")[Corrupt Torch](Corrupt_Torch.md "Corrupt Torch") | [Corruption](Corruption "Corruption"), [Underground Corruption](Underground_Corruption.md "Underground Corruption") | 0.2 | 0.2   
96	[](Crimson_Torch.md "Crimson Torch")[Crimson Torch](Crimson_Torch.md "Crimson Torch") | [Crimson](Crimson "Crimson"), [Underground Crimson](Underground_Crimson.md "Underground Crimson") | 0.2 | 0.2   
97	[](Cursed_Torch.md "Cursed Torch")[Cursed Torch](Cursed_Torch.md "Cursed Torch") | [Corruption](Corruption "Corruption"), [Underground Corruption](Underground_Corruption.md "Underground Corruption") | 0.2 | 0   
98	[](Ichor_Torch.md "Ichor Torch")[Ichor Torch](Ichor_Torch.md "Ichor Torch") | [Crimson](Crimson "Crimson"), [Underground Crimson](Underground_Crimson.md "Underground Crimson") | 0.2 | 0   
99	[](Coral_Torch.md "Coral Torch")[Coral Torch](Coral_Torch.md "Coral Torch") | [Oceans](Ocean.md "Ocean") | 0.2 | 0  
100	0.2 (only when both placed outside of [water](Water.md "Water") and outside an [Ocean](Ocean.md "Ocean"))   
101	[](Mushroom_Torch.md "Mushroom Torch")[Mushroom Torch](Mushroom_Torch.md "Mushroom Torch") | [Glowing Mushroom biomes](Glowing_Mushroom_biome.md "Glowing Mushroom biome") | 0.2 | 0.2   
102	[](Bone_Torch.md "Bone Torch")[Bone Torch](Bone_Torch.md "Bone Torch") | Anywhere outside the [Snow biome](Snow_biome.md "Snow biome"), [Desert](Desert.md "Desert"), [Jungle](Jungle.md "Jungle"),  
103	[Corruption](Corruption "Corruption"), [Crimson](Crimson "Crimson"), [Hallow](Hallow "Hallow"), [Dungeon](Dungeon.md "Dungeon") or [Jungle Temple](Jungle_Temple.md "Jungle Temple") | 0.1 | 0   
104	[](Torch.md "Torch")[Torch](Torch.md "Torch") | None | 0 | 0  
105	0.1 ([Desert](Desert.md "Desert"), [Corruption](Corruption "Corruption"), [Crimson](Crimson "Crimson"), and [Hallow](Hallow "Hallow") only)  
106	0.3 ([Snow biome](Snow_biome.md "Snow biome") only)   
107	  
108	#### Notes
109	
110	  * Placed torches on the [Surface](Surface.md "Surface") and in [Space](Space.md "Space") are ignored. This means that in these layers, only held torches will affect luck.
111	  * Torch luck does not apply in the [Dungeon](Dungeon.md "Dungeon") or [Jungle Temple](Jungle_Temple.md "Jungle Temple"), or when [The Torch God](The_Torch_God.md "The Torch God") [event](Event "Event") is active.
112	  * Torches turned off (e.g. via [Wire](Wire.md "Wire")) will still affect luck.
113	  * [Colored](Torch#Colored_Torch "Torch"), [Ultrabright](Torches#Ultrabright_Torch "Torches"), [Demon](Torches#Demon_Torch "Torches") and [Aether Torches](Torches#Aether_Torch "Torches"), along with other light sources such as [Candles](Candles.md "Candles"), have no effect.

```


---

## 🤖 Assistant · 2026-08-12T18:31:29.044Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Bash works again. Now the potions. Let me extract potion page effect/duration lines. I'll grep for the buff description lines. Potion pages: structure has "Grants Buff" infobox and a lead paragraph with numbers, plus Duration.

Let me grep key lines per potion page.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:31:30.222Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && for f in Regeneration_Potion Swiftness_Potion Ironskin_Potion Endurance_Potion Wrath_Potion Rage_Potion Lifeforce_Potion Magic_Power_Potion Mana_Regeneration_Potion Summoning_Potion Ammo_Reservation_Potion; do echo \"##### $f #####\"; grep -n -E 'Duration\\|' \"$f.md\" | head -2; grep -n -E 'per second|percent|%|defense|minion|damage|critical|mana|life|max health|ammo' \"$f.md\" | sed -n '1,4p'; done",
 "description": "Extract potion buff values batch 1"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:31:43.019Z

**📎 ToolResult**

```
##### Regeneration_Potion #####
32:Duration| 8 minutes  
10:For the differences of this information on [Old-gen console](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [3DS](Legacy%3A3DS_version "Legacy:3DS version"), see **[Legacy:Regeneration Potion](Legacy%3ARegeneration_Potion "Legacy:Regeneration Potion")**.
22:[Tooltip](Tooltips.md "Tooltips")|  _Provides life regeneration_  
23:[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_1 "Blue \(Rarity level: 1\)")  
31:Buff tooltip|  _Provides life regeneration_  
##### Swiftness_Potion #####
32:Duration| 8 minutes  
10:For the differences of this information on [Old-gen console](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [3DS](Legacy%3A3DS_version "Legacy:3DS version"), see **[Legacy:Swiftness Potion](Legacy%3ASwiftness_Potion "Legacy:Swiftness Potion")**.
22:[Tooltip](Tooltips.md "Tooltips")|  _25% increased movement speed_  
23:[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_1 "Blue \(Rarity level: 1\)")  
31:Buff tooltip|  _25% increased movement speed_  
##### Ironskin_Potion #####
32:Duration| 8 minutes  
10:For the differences of this information on [Old-gen console](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [3DS](Legacy%3A3DS_version "Legacy:3DS version"), see **[Legacy:Ironskin Potion](Legacy%3AIronskin_Potion "Legacy:Ironskin Potion")**.
22:[Tooltip](Tooltips.md "Tooltips")|  _Increase defense by 8_  
23:[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_1 "Blue \(Rarity level: 1\)")  
31:Buff tooltip|  _Increase defense by 8_  
##### Endurance_Potion #####
32:Duration| 4 minutes  
10:For the differences of this information on [Old-gen console](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [3DS](Legacy%3A3DS_version "Legacy:3DS version"), see **[Legacy:Endurance Potion](Legacy%3AEndurance_Potion "Legacy:Endurance Potion")**.
22:[Tooltip](Tooltips.md "Tooltips")|  _Reduces damage taken by 10%_  
23:[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_1 "Blue \(Rarity level: 1\)")  
31:Buff tooltip|  _10% reduced damage_  
##### Wrath_Potion #####
32:Duration| 4 minutes  
10:For the differences of this information on [Old-gen console](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [3DS](Legacy%3A3DS_version "Legacy:3DS version"), see **[Legacy:Wrath Potion](Legacy%3AWrath_Potion "Legacy:Wrath Potion")**.
22:[Tooltip](Tooltips.md "Tooltips")|  _Increases damage by 10%_  
23:[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_1 "Blue \(Rarity level: 1\)")  
31:Buff tooltip|  _10% increased damage_  
##### Rage_Potion #####
32:Duration| 4 minutes  
10:For the differences of this information on [Old-gen console](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [3DS](Legacy%3A3DS_version "Legacy:3DS version"), see **[Legacy:Rage Potion](Legacy%3ARage_Potion "Legacy:Rage Potion")**.
22:[Tooltip](Tooltips.md "Tooltips")|  _Increases critical chance by 10%_  
23:[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_1 "Blue \(Rarity level: 1\)")  
31:Buff tooltip|  _10% increased critical chance_  
##### Lifeforce_Potion #####
32:Duration| 8 minutes  
10:For the differences of this information on [Old-gen console](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [3DS](Legacy%3A3DS_version "Legacy:3DS version"), see **[Legacy:Lifeforce Potion](Legacy%3ALifeforce_Potion "Legacy:Lifeforce Potion")**.
22:[Tooltip](Tooltips.md "Tooltips")|  _Increases max life by 20%_  
23:[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_1 "Blue \(Rarity level: 1\)")  
31:Buff tooltip|  _20% increased max life_  
##### Magic_Power_Potion #####
32:Duration| 4 minutes  
10:For the differences of this information on [Old-gen console](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [3DS](Legacy%3A3DS_version "Legacy:3DS version"), see **[Legacy:Magic Power Potion](Legacy%3AMagic_Power_Potion "Legacy:Magic Power Potion")**.
22:[Tooltip](Tooltips.md "Tooltips")|  _20% increased magic damage_  
23:[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_1 "Blue \(Rarity level: 1\)")  
31:Buff tooltip|  _20% increased magic damage_  
##### Mana_Regeneration_Potion #####
32:Duration| 8 minutes  
10:For the differences of this information on [Old-gen console](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [3DS](Legacy%3A3DS_version "Legacy:3DS version"), see **[Legacy:Mana Regeneration Potion](Legacy%3AMana_Regeneration_Potion "Legacy:Mana Regeneration Potion")**.
22:[Tooltip](Tooltips.md "Tooltips")|  _Increased mana regeneration_  
23:[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_1 "Blue \(Rarity level: 1\)")  
31:Buff tooltip|  _Increased mana regeneration_  
##### Summoning_Potion #####
32:Duration| 8 minutes  
10:For the differences of this information on [Old-gen console](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [3DS](Legacy%3A3DS_version "Legacy:3DS version"), see **[Legacy:Summoning Potion](Legacy%3ASummoning_Potion "Legacy:Summoning Potion")**.
22:[Tooltip](Tooltips.md "Tooltips")|  _Increases your max number of minions by 1_  
23:[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_1 "Blue \(Rarity level: 1\)")  
31:Buff tooltip|  _Increased your max number of minions by 1_  
##### Ammo_Reservation_Potion #####
32:Duration| 8 minutes  
10:For the differences of this information on [Old-gen console](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [3DS](Legacy%3A3DS_version "Legacy:3DS version"), see **[Legacy:Ammo Reservation Potion](Legacy%3AAmmo_Reservation_Potion "Legacy:Ammo Reservation Potion")**.
22:[Tooltip](Tooltips.md "Tooltips")|  _20% chance to save ammo_  
23:[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_1 "Blue \(Rarity level: 1\)")  
31:Buff tooltip|  _20% chance to save ammo_

```


---

## 🤖 Assistant · 2026-08-12T18:31:54.379Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. Potion pages confirm tooltips and durations. Now batch 2 of potions: Warmth, Gills, Featherfall, Gravitation, Obsidian_Skin, Invisibility, Hunter, Spelunker, Dangersense, Shine, Night_Owl, Battle, Calming, Fishing, Sonar, Crate, Mining, Builder, Heartreach, Titan, Inferno.

I mainly need durations and any extra numeric detail (e.g., Warmth −? damage from cold sources; Heartreach range increase; Titan knockback +70%?; Inferno 15-base damage ring?; Mining +25%; Fishing +15; Crate doubles; Sonar; Battle 2×).

The Buffs.md index already gave: Warmth 15 min, Gills 4 min, Featherfall 10, Gravitation 3, Obsidian Skin 6, Invisibility 3, Hunter 8, Spelunker 5, Dangersense 10, Shine 10, Night Owl 10, Battle 7, Calm 12, Fishing 8 (+15 FP), Sonar 8, Crate 4 (doubles), Mining 10 (+25%), Builder 45 min (25% placement + 1 tile range), Heartreach 8, Titan 8, Inferno 4.

Let me extract Duration lines from these potion pages and any extra numeric info (Warmth, Titan, Heartreach, Inferno).
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:31:55.612Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && for f in Warmth_Potion Gills_Potion Featherfall_Potion Gravitation_Potion Obsidian_Skin_Potion Invisibility_Potion Hunter_Potion Spelunker_Potion Dangersense_Potion Shine_Potion Night_Owl_Potion Battle_Potion Calming_Potion Fishing_Potion Sonar_Potion Crate_Potion Mining_Potion Builder_Potion Heartreach_Potion Titan_Potion Inferno_Potion; do printf \"%-24s \" \"$f\"; grep -m1 -E '^\\s*Duration\\|' \"$f.md\" | sed -E 's/\\[[^]]*\\]\\([^)]*\\)/ /g'; done",
 "description": "Extract durations for remaining potions"
}
```


---

## 🤖 Assistant · 2026-08-12T18:31:56.755Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && for f in Warmth_Potion Titan_Potion Heartreach_Potion Inferno_Potion Fishing_Potion Crate_Potion Mining_Potion Battle_Potion Calming_Potion Builder_Potion; do echo \"##### $f #####\"; sed -n '40,60p' \"$f.md\" | grep -E '\\*\\*|increase|reduc|chance|damage|range|speed|power|doub' | head -4; done",
 "description": "Extract detail text for selected potions"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:32:03.764Z

**📎 ToolResult**

```
Warmth_Potion            Duration| 15 minutes  
Gills_Potion             Duration| 4 minutes  
Featherfall_Potion       Duration| 10 minutes  
Gravitation_Potion       Duration| 3 minutes  
Obsidian_Skin_Potion     Duration| 6 minutes  
Invisibility_Potion      Duration| 3 minutes  
Hunter_Potion            Duration| 8 minutes  
Spelunker_Potion         Duration| 5 minutes  
Dangersense_Potion       Duration| 10 minutes  
Shine_Potion             Duration| 10 minutes  
Night_Owl_Potion         Duration| 10 minutes  
Battle_Potion            Duration| 7 minutes  
Calming_Potion           Duration| 12 minutes  
Fishing_Potion           Duration| 8 minutes  
Sonar_Potion             Duration| 8 minutes  
Crate_Potion             Duration| 4 minutes  
Mining_Potion            Duration| 10 minutes  
Builder_Potion           Duration| 45 minutes  
Heartreach_Potion        Duration| 8 minutes  
Titan_Potion             Duration| 8 minutes  
Inferno_Potion           Duration| 4 minutes

```


---

## 👤 User(sidechain) · 2026-08-12T18:32:30.559Z

**📎 ToolResult**

```
##### Warmth_Potion #####
  * Internal [Item ID](Item_IDs.md "Item IDs"): **2359**
  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **124**
The **Warmth Potion** is a [buff potion](Buff_potions.md "Buff potions") that grants the **Warmth** [buff](Buffs.md "Buffs") when consumed, which provides +30% [damage reduction](Damage_reduction.md "Damage reduction") from cold-themed [enemies](Enemies.md "Enemies") _(seebelow)_. This lasts for 15 minutes, but can be canceled at any time by right-clicking the icon ([](Desktop_version_history.md "Desktop version")), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff ([](Console_version.md "Console version")), or by double-tapping the buff icon ([](Mobile_version.md "Mobile version")). 
[](Warmth_Potion.md "Warmth Potion")Warmth Potion**** __(Desktop, Console, Old-gen console and Mobile versions)| 
##### Titan_Potion #####
  * Internal [Item ID](Item_IDs.md "Item IDs"): **2326**
  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **108**
The **Titan Potion** is a [buff potion](Buff_potions.md "Buff potions") which grants the **Titan** [buff](Buffs.md "Buffs") when consumed. The buff increases the amount of [knockback](Knockback.md "Knockback") the player inflicts on [enemies](Enemies.md "Enemies") by 50%. This lasts for 8 minutes, but can be canceled at any time by right-clicking the icon ([](Desktop_version_history.md "Desktop version")), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff ([](Console_version.md "Console version")), or by double-tapping the buff icon ([](Mobile_version.md "Mobile version")). 
##### Heartreach_Potion #####
  * Internal [Item ID](Item_IDs.md "Item IDs"): **2323**
  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **105**
~~[Boreal Crate](Boreal_Crate.md "Boreal Crate")**** __(Desktop, Console and Mobile versions)~~[](Boreal_Crate.md "Boreal Crate")[Boreal Crate](Boreal_Crate.md "Boreal Crate")| 2–4| 1/24 (4.17%)  
~~[Bramble Crate](Bramble_Crate.md "Bramble Crate")**** __(Desktop, Console and Mobile versions)~~[](Bramble_Crate.md "Bramble Crate")[Bramble Crate](Bramble_Crate.md "Bramble Crate")| 2–4| 1/24 (4.17%)  
##### Inferno_Potion #####
  * Internal [Item ID](Item_IDs.md "Item IDs"): **2348**
  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **116**
The **Inferno Potion** is a [buff potion](Buff_potions.md "Buff potions") that grants the **Inferno** [buff](Buffs.md "Buffs") when consumed. The buff casts a spinning ring of fire around the player that deals 20 damage per second and inflicts the [Hellfire](Hellfire.md "Hellfire") [debuff](Debuffs.md "Debuffs") for 2 seconds to all [enemies](Enemies.md "Enemies") inside of it while also giving off light. [Critters](Critters.md "Critters") and other passive [NPCs](NPCs.md "NPCs") are unaffected. This lasts for 4 minutes, but can be canceled at any time by right-clicking the icon ([](Desktop_version_history.md "Desktop version")), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff ([](Console_version.md "Console version")), or by double-tapping the buff icon ([](Mobile_version.md "Mobile version")). 
##### Fishing_Potion #####
  * Internal [Item ID](Item_IDs.md "Item IDs"): **2354**
  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **121**
The **Fishing Potion** is a [buff potion](Buff_potion "Buff potion") which grants the **Fishing** [buff](Buff "Buff") when consumed. The buff increases [Fishing Power](Fishing_Power.md "Fishing Power") by 15. This lasts for 8 minutes, but can be canceled at any time by right-clicking the icon ([](Desktop_version_history.md "Desktop version")), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff ([](Console_version.md "Console version")), or by double-tapping the buff icon ([](Mobile_version.md "Mobile version")). 
 _**or**_  
##### Crate_Potion #####
  * Internal [Item ID](Item_IDs.md "Item IDs"): **2356**
  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **123**
The **Crate Potion** is a [buff potion](Buff_potion "Buff potion") which grants the **Crate** [buff](Buff "Buff") when consumed. The buff increases the chance of getting a [crate](Crate "Crate") from 1/10 (10%) to 1/4 (25%) when [fishing](Fishing.md "Fishing"). This lasts for 4 minutes, but can be canceled at any time by right-clicking the icon ([](Desktop_version_history.md "Desktop version")), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff ([](Console_version.md "Console version")), or by double-tapping the buff icon ([](Mobile_version.md "Mobile version")). 
  * [](Shiverthorn.md "Shiverthorn")[Shiverthorn](Shiverthorn.md "Shiverthorn")**** __(Desktop, Console, Old-gen console and Mobile versions)
##### Mining_Potion #####
  * Internal [Item ID](Item_IDs.md "Item IDs"): **2322**
  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **104**
~~[Boreal Crate](Boreal_Crate.md "Boreal Crate")**** __(Desktop, Console and Mobile versions)~~[](Boreal_Crate.md "Boreal Crate")[Boreal Crate](Boreal_Crate.md "Boreal Crate")| 2–4| 1/24 (4.17%)  
~~[Bramble Crate](Bramble_Crate.md "Bramble Crate")**** __(Desktop, Console and Mobile versions)~~[](Bramble_Crate.md "Bramble Crate")[Bramble Crate](Bramble_Crate.md "Bramble Crate")| 2–4| 1/24 (4.17%)  
##### Battle_Potion #####
  * Internal [Item ID](Item_IDs.md "Item IDs"): **300**
  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **13**
The **Battle Potion** is a [buff potion](Buff_potions.md "Buff potions") which grants the **Battle** [buff](Buffs.md "Buffs") when consumed. The buff increases the [spawn rate](NPC_spawning.md "NPC spawning") and maximum number of [enemies](Enemies.md "Enemies") and [critters](Critters.md "Critters") that can be on-screen at once by 100%, effectively doubling these rates. This lasts for 7 minutes, but can be canceled at any time by right-clicking the icon ([](Desktop_version_history.md "Desktop version")), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff ([](Console_version.md "Console version")), or by double-tapping the buff icon ([](Mobile_version.md "Mobile version")). 
 _**or**_  
##### Calming_Potion #####
  * Internal [Item ID](Item_IDs.md "Item IDs"): **2324**
  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **106**
~~[Mythril Crate](Mythril_Crate.md "Mythril Crate")**** __(Desktop, Console and Mobile versions)~~[](Mythril_Crate.md "Mythril Crate")[Mythril Crate](Mythril_Crate.md "Mythril Crate")| 2–4| 1/32 (3.13%)  
The **Calming Potion** is a [buff potion](Buff_potions.md "Buff potions") which grants the **Calm** [buff](Buffs.md "Buffs") when consumed. The buff reduces the [enemy](Enemies.md "Enemies") [spawn rate](Spawn_rate.md "Spawn rate") by 39%, and the maximum number of enemies on-screen is reduced by 40%. This lasts for 12 minutes, but can be canceled at any time by right-clicking the icon ([](Desktop_version_history.md "Desktop version")), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff ([](Console_version.md "Console version")), or by double-tapping the buff icon ([](Mobile_version.md "Mobile version")). 
##### Builder_Potion #####
  * Internal [Item ID](Item_IDs.md "Item IDs"): **2325**
  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **107**
The **Builder Potion** is a [buff potion](Buff_potion "Buff potion") that grants the **Builder** [buff](Buff "Buff") when consumed. It grants the following effects: 
  * +1 [placement range](Placement_range.md "Placement range")

```


---

## 🤖 Assistant · 2026-08-12T18:32:39.389Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting discrepancies:
- Calming Potion page: −39% spawn rate, −40% max on-screen, whereas Buffs.md index says 17% spawn reduction. Both wiki-stated; I'll report both and note the conflict.
- Crate Potion: 1/10 → 1/4 chance (index says "doubles the chance" — 10%→25% isn't doubling; index wording). Report both.
- Warmth: +30% damage reduction from cold-themed enemies (index says "Reduces damage from cold-themed enemies").
- Titan: +50% knockback.
- Inferno: 20 damage per second ring, inflicts Hellfire 2 s.
- Battle: +100% spawn rate and max enemies (doubling).
- Builder: +1 placement range, +25% placement speed (need to confirm the 25%).

Let me get the Builder bullet list and Mining, Heartreach, Swiftness, Night Owl, Hunter, Spelunker details (range numbers), and Featherfall/Gills etc.

Also Well Fed tiers (Well_Fed.md): stats. Exquisitely_Stuffed.md and Plenty Satisfied. Let me extract those numbers.

Also Tipsy.md (from index: −4 def, +10% melee damage, +10% melee speed, +2% melee crit, +5 fishing power, 2 minutes; NPCs 1.1× def, 1.1× damage, 1.11× attack speed).

Let me batch.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:32:39.478Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && sed -n '44,58p' Builder_Potion.md; echo \"=====MINING=====\"; sed -n '44,52p' Mining_Potion.md | grep -E '\\*\\*|increase|%'; echo \"=====HEARTREACH=====\"; sed -n '44,52p' Heartreach_Potion.md | grep -E '\\*\\*|increase|range|%|pickup'; echo \"=====SWIFTNESS=====\"; sed -n '44,52p' Swiftness_Potion.md | grep -E '\\*\\*|increase|speed|%'; echo \"=====NIGHTOWL=====\"; sed -n '44,52p' Night_Owl_Potion.md | grep -E '\\*\\*|increase|vision|light|%'; echo \"=====HUNTER=====\"; sed -n '44,52p' Hunter_Potion.md | grep -E '\\*\\*|highlight|screen|%'; echo \"=====SPELUNKER=====\"; sed -n '44,52p' Spelunker_Potion.md | grep -E '\\*\\*|highlight|block|%|tile'",
 "description": "Extract detail text for utility potions"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:32:39.533Z

**📎 ToolResult**

```
Classic

Expert

Master

Entity| Qty.| Rate  
---|---|---  
~~[Chest](Chest "Chest")~~[](Chest "Chest")[Chest](Chest "Chest")| 1–2| 1/9 (11.11%)  
  
The **Builder Potion** is a [buff potion](Buff_potion "Buff potion") that grants the **Builder** [buff](Buff "Buff") when consumed. It grants the following effects: 

  * +1 [placement range](Placement_range.md "Placement range")
  * +25% [placement speed](Placement_speed.md "Placement speed") when placing [blocks](Blocks.md "Blocks") and [walls](Walls "Walls")
=====MINING=====
=====HEARTREACH=====
=====SWIFTNESS=====
=====NIGHTOWL=====
=====HUNTER=====
=====SPELUNKER=====

```


---

## 🤖 Assistant · 2026-08-12T18:32:44.940Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The other potions' lead paragraphs are at different line numbers. Let me grep for the lead sentence pattern "**...** is a buff potion" with the number following. I'll grep -A2 'is a .*potion' lines.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:32:46.324Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && for f in Mining_Potion Heartreach_Potion Swiftness_Potion Night_Owl_Potion Hunter_Potion Spelunker_Potion Shine_Potion Sonar_Potion Dangersense_Potion Gills_Potion Featherfall_Potion Gravitation_Potion Obsidian_Skin_Potion Invisibility_Potion Regeneration_Potion Endurance_Potion; do echo \"##### $f #####\"; grep -m1 -E 'is a .*potion.*' \"$f.md\" | sed -E 's/\\[\\]\\([^)]*\\)//g; s/\\[([^]]*)\\]\\([^)]*\\)/\\1/g' | head -c 700; echo; done",
 "description": "Extract lead sentences from utility potions"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:32:54.031Z

**📎 ToolResult**

```
##### Mining_Potion #####
The **Mining Potion** is a buff potion which grants the **Mining** buff when consumed. The buff increases mining speed by 25%. This lasts for 10 minutes, but can be canceled at any time by right-clicking the icon (), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff (), or by double-tapping the buff icon (). 

##### Heartreach_Potion #####
The **Heartreach Potion** is a buff potion which grants the **Heartreach** buff when consumed. The buff increases the pickup range of life recovery Hearts by 15.625 tiles, from 2.625 tiles to a total of 18.25 tiles. This lasts for 8 minutes, but can be canceled at any time by right-clicking the icon (), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff (), or by double-tapping the buff icon (). 

##### Swiftness_Potion #####
The **Swiftness Potion** is a buff potion which grants the **Swiftness** buff when consumed. The buff increases the player's maximum movement speed by 25%, but does not stack with sprinting accessories (such as Hermes Boots), nor does it affect the speed of mounts. This lasts for 8 minutes, but can be canceled at any time by right-clicking the icon (), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff (), or by double-tapping the buff icon (). 

##### Night_Owl_Potion #####
The **Night Owl Potion** is a buff potion that grants the **Night Owl** buff when consumed. The buff improves the player's night vision, and sharply increases the radius of any available light source. The buff itself has no effect in total darkness. This lasts for 10 minutes, but can be canceled at any time by right-clicking the icon (), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff (), or by double-tapping the buff icon (). 

##### Hunter_Potion #####
The **Hunter Potion** is a buff potion which grants the **Hunter** buff when consumed. The buff shows the location of enemies, critters, and undiscovered NPCs on the screen by highlighting them in red (enemies) or green (critters and NPCs). Although these affected entities glow, they do not emit any light to the surrounding area. This lasts for 8 minutes, but can be canceled at any time by right-clicking the icon (), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff (), or by double-tapping the buff icon (). 

##### Spelunker_Potion #####
The **Spelunker Potion** is a buff potion which grants the **Spelunker** buff when consumed. The buff illuminates valuable nearby objects and highlights them with a yellow tint. This lasts for 5 minutes, but can be canceled at any time by right-clicking the icon (), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff (), or by double-tapping the buff icon (). 

##### Shine_Potion #####
The **Shine Potion** is a buff potion which grants the **Shine** buff when consumed. The buff makes the player glow brightly, which is useful for exploring caves or while exploring underwater. This lasts for 10 minutes, but can be canceled at any time by right-clicking the icon (), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff (), or by double-tapping the buff icon (). 

##### Sonar_Potion #####
The **Sonar Potion** is a buff potion which grants the **Sonar** buff when consumed. The buff displays the name of a fishing catch above a fishing pole's bobber when it receives a bite while fishing, along with a sound effect. This lasts for 8 minutes, but can be canceled at any time by right-clicking the icon (), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff (), or by double-tapping the buff icon (). 

##### Dangersense_Potion #####
The **Dangersense Potion** is a buff potion which grants the **Dangersense** buff when consumed. The buff reveals hazardous traps, blocks, and objects that can potentially harm or impede the player by highlighting them in red, even in complete darkness. This lasts for 10 minutes, but can be canceled at any time by right-clicking the icon (), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff (), or by double-tapping the buff icon (). 

##### Gills_Potion #####
The **Gills Potion** is a buff potion which grants the **Gills** buff when consumed. The buff prevents the player's breath meter from depleting and thus prevents drowning. This lasts for 4 minutes, but can be canceled at any time by right-clicking the icon (), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff (), or by double-tapping the buff icon (). 

##### Featherfall_Potion #####
The **Featherfall Potion** is a buff potion which grants the **Featherfall** buff when consumed. The buff negates fall damage, and reduces the player's fall speed and gravity to 1/3 (33.33%)[1] of normal, allowing them to jump higher and fall slower. This lasts for 10 minutes, but can be canceled at any time by right-clicking the icon (), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff (), or by double-tapping the buff icon (). 

##### Gravitation_Potion #####
The **Gravitation Potion** is a buff potion which grants the **Gravitation** buff when consumed. The buff allows the player to invert gravity with `▲ Up`, making the screen appear upside-down and causing the player to fall upwards and walk on top of ceilings. The effect can be toggled while in midair. This lasts for 3 minutes, but can be canceled at any time by right-clicking the icon (), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff (), or by double-tapping the buff icon (). 

##### Obsidian_Skin_Potion #####
The **Obsidian Skin Potion** is a buff potion which grants the **Obsidian Skin** buff when consumed. The buff makes the player immune to lava and the On Fire! debuff. It also grants immunity to the Burning debuff from touching Meteorite, Hellstone, Hellstone Bricks, and Ancient Hellstone Bricks for its duration. This lasts for 6 minutes, but can be canceled at any time by right-clicking the icon (), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff (), or by double-tapping the buff icon (). 

##### Invisibility_Potion #####
The **Invisibility Potion** is a buff potion that grants the **Invisibility** buff when consumed. This lasts for 3 minutes, but can be canceled at any time by right-clicking the icon (), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff (), or by double-tapping the buff icon (). The buff is furthermore immediately canceled if the player takes damage of any kind. 

##### Regeneration_Potion #####
The **Regeneration Potion** is a buff potion which grants the **Regeneration** buff when consumed. The buff provides health regeneration by restoring an additional 2 health per second, for a total of 960 health. This lasts for 8 minutes, but can be canceled at any time by right-clicking the icon (), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff (), or by double-tapping the buff icon (). 

##### Endurance_Potion #####
The **Endurance Potion** is a buff potion that grants the **Endurance** buff when consumed, which provides +10% damage reduction. This lasts for 4 minutes, but can be canceled at any time by right-clicking the icon (), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff (), or by double-tapping the buff icon ().

```


---

## 🤖 Assistant · 2026-08-12T18:32:56.998Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Excellent. Now Well Fed tiers and Tipsy, Exquisitely Stuffed. Let me extract Well_Fed.md stats table (the three tiers: Well Fed, Plenty Satisfied, Exquisitely Stuffed with their stat bonuses).
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:32:57.844Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && grep -n -E '^## |^### ' Well_Fed.md | head -20; echo \"===TABLE===\"; sed -n '/Effect table\\|Effects\\|grants the following/,/^## /p' Well_Fed.md | grep -E '\\|' | head -30",
 "description": "Find Well Fed stat tiers"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:33:05.205Z

**📎 ToolResult**

```
12:## Well Fed
14:## Statistics
16:### Type
20:### Cause
24:### Effects
28:### Duration
32:### Tooltip
37:## Internal IDs
39:### [Buff ID](Buff_IDs.md "Buff IDs")
43:### Internal name
47:## Plenty Satisfied
49:## Statistics
51:### Type
55:### Cause
59:### Effects
63:### Duration
67:### Tooltip
72:## Internal IDs
74:### [Buff ID](Buff_IDs.md "Buff IDs")
78:### Internal name
===TABLE===

```


---

## 🤖 Assistant · 2026-08-12T18:33:13.387Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Well_Fed.md",
 "limit": 85,
 "offset": 12
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:33:13.390Z

**📎 ToolResult**

```
12	## Well Fed
13	
14	## Statistics
15	
16	### Type
17	
18	[Buff](Buff "Buff")
19	
20	### Cause
21	
22	[](Food.md "Food")[Food items](Food.md "Food")
23	
24	### Effects
25	
26	Minor improvements to all stats
27	
28	### Duration
29	
30	Varies
31	
32	### Tooltip
33	
34	_Minor improvements to all stats  
35	[ Minor improvements to all stats and increased life regeneration](Expert_Mode.md "Expert Mode")_
36	
37	## Internal IDs
38	
39	### [Buff ID](Buff_IDs.md "Buff IDs")
40	
41	26
42	
43	### Internal name
44	
45	`WellFed`
46	
47	## Plenty Satisfied
48	
49	## Statistics
50	
51	### Type
52	
53	[Buff](Buff "Buff")
54	
55	### Cause
56	
57	[](Food.md "Food")[Food items](Food.md "Food")
58	
59	### Effects
60	
61	Medium improvements to all stats
62	
63	### Duration
64	
65	Varies
66	
67	### Tooltip
68	
69	_Medium improvements to all stats  
70	[ Medium improvements to all stats and increased life regeneration](Expert_Mode.md "Expert Mode")_
71	
72	## Internal IDs
73	
74	### [Buff ID](Buff_IDs.md "Buff IDs")
75	
76	206
77	
78	### Internal name
79	
80	`WellFed2`
81	
82	## Exquisitely Stuffed
83	
84	## Statistics
85	
86	### Type
87	
88	[Buff](Buff "Buff")
89	
90	### Cause
91	
92	[](Food.md "Food")[Food items](Food.md "Food")
93	
94	### Effects
95	
96	Major improvements to all stats

```


---

## 🤖 Assistant · 2026-08-12T18:33:16.224Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The numeric per-tier stats aren't in Well_Fed.md infoboxes. They may be in a "Effects" section further down or in the Food page. Let me grep Well_Fed.md for percentage/number lines describing the tiers (e.g., "+2% damage, +2 defense").
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:33:16.890Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && grep -n -E '\\+?[0-9]+%|\\+[0-9]+ ' Well_Fed.md | head -25",
 "description": "Find Well Fed tier stat numbers"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:33:16.910Z

**📎 ToolResult**

```
127:[Defense](Defense.md "Defense") | +2 | +3 | +4   
128:[Damage](Damage.md "Damage") | +5% | +7.5% | +10%   
129:[Critical strike chance](Critical_strike_chance "Critical strike chance") | +2% | +3% | +4%   
130:[Melee speed](Melee_speed "Melee speed") | +5% | +7.5% | +10%   
131:[Minion](Minion "Minion") [knockback](Knockback.md "Knockback") | +0.5 | +0.75 | +1   
132:[Movement speed](Movement_speed.md "Movement speed") | +20% | +30% | +40%   
133:[Mining speed](Mining_speed "Mining speed") | +5% | +10% | +15%   
216:    * Fixed bug that made Well Fed give 10% magic damage and no ranged damage instead of each having a 5% damage increase.
610:  *[100%]: Expert Mode
642:  *[1.99%]: Expert Mode
643:  *[199/10000 (1.99%)]: Expert Mode
645:  *[1,99%]: Expert Mode
646:  *[1/50 (2%)]: Mode Expert
686:  *[50%]: Expert Mode
687:  *[1/2 (50%)]: Expert Mode
692:  *[75%]: Chế độ Expert
696:  *[199/10000 (1,99%)]: Mode Expert
722:  *[3.33–6.67%]: Expert Mode
723:  *[3.33%–6.67%]: Expert Mode
725:  *[3.33%]: Expertní mód
726:  *[6.67%]: Expert Mode
727:  *[0.014%]: Expert Mode
730:  *[+100%]: Expert Mode
731:  *[−50%]: Expert Mode
732:  *[+20%]: Expert Mode

```


---

## 🤖 Assistant · 2026-08-12T18:33:23.806Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Well_Fed.md",
 "limit": 30,
 "offset": 112
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:33:23.810Z

**📎 ToolResult**

```
112	
113	### Internal name
114	
115	`WellFed3`
116	
117	**Well Fed** , **Plenty Satisfied** , and **Exquisitely Stuffed** are [buffs](Buffs.md "Buffs") granted to the player when they consume [food](Food.md "Food"), which provide general stat bonuses that vary in potency and duration depending on the food item consumed. In [Expert Mode](Expert_Mode.md "Expert Mode"), [health regeneration](Health_regeneration.md "Health regeneration") will only be fully effective while the player is under the effects of one of these buffs. While one of these buffs is active in a [The Constant](The_Constant.md "The Constant") or [Zenith](Zenith_\(seed\) "Zenith \(seed\)") [special world seed](Special_world_seed "Special world seed"), the player will also be temporarily immune to [hunger](Hunger.md "Hunger") for the buff's duration. 
118	
119	This lasts for 1 to 48 minutes (depending on the item used), but can be canceled at any time by right-clicking the icon ([](Desktop_version_history.md "Desktop version")), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff ([](Console_version.md "Console version")), or by double-tapping the buff icon ([](Mobile_version.md "Mobile version")). 
120	
121	Only one of these buffs may be active at a time and therefore do not stack. The buff that was most recently applied takes priority. 
122	
123	## Effects
124	
125	Stat | Well Fed | Plenty Satisfied | Exquisitely Stuffed   
126	---|---|---|---  
127	[Defense](Defense.md "Defense") | +2 | +3 | +4   
128	[Damage](Damage.md "Damage") | +5% | +7.5% | +10%   
129	[Critical strike chance](Critical_strike_chance "Critical strike chance") | +2% | +3% | +4%   
130	[Melee speed](Melee_speed "Melee speed") | +5% | +7.5% | +10%   
131	[Minion](Minion "Minion") [knockback](Knockback.md "Knockback") | +0.5 | +0.75 | +1   
132	[Movement speed](Movement_speed.md "Movement speed") | +20% | +30% | +40%   
133	[Mining speed](Mining_speed "Mining speed") | +5% | +10% | +15%   
134	  
135	Well Fed and its variants also allow the player to produce [Poo](Poo.md "Poo") by sitting on a [Toilet](Toilet "Toilet") for a short duration, after which the buff is removed. 
136	
137	## Causes
138	
139	See [Food](Food.md "Food") for the complete list of food items that grant these buffs.
140	
141	## Tips

```


---

## 🤖 Assistant · 2026-08-12T18:33:30.226Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Excellent — Well Fed tiers table with all stats. Note the rule "Only one of these buffs may be active at a time and therefore do not stack. The buff that was most recently applied takes priority." That's a merge/refresh-relevant rule on Well_Fed.md.

Now Tipsy (Sake/Ale) numbers and durations. Let me extract Tipsy.md. Also the remaining debuff page details: Suffocation, Chilled, Frozen, Darkness, Mana Sickness notes, Burning, Midas notes (10-50% coins), Stinky (luck −0.25), and the Cursed Inferno history bullets, Bleeding 1.4.5.0, Burning 1.4.5.0, Confused 1.4.5.0, Darkness 1.4.0.1/1.3.0.1.

Let me batch with sed for specific line ranges.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:33:31.976Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && echo \"===TIPSY===\"; grep -n -E 'Duration\\||defense|melee damage|melee speed|critical|Fishing Power|1\\.1|1\\.11|2 minutes' Tipsy.md | head -10; echo; echo \"===CURSEDINFERNO 1.4.1/1.4.0.1===\"; sed -n '110,121p' Cursed_Inferno.md; echo \"===BLEEDING 1.4.5===\"; sed -n '249,258p' Bleeding.md; echo \"===BURNING 1.4.5/1.3.0.1===\"; sed -n '95,108p' Burning.md",
 "description": "Extract Tipsy and debuff version-change notes"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:33:32.008Z

**📎 ToolResult**

```
===TIPSY===
24:+ melee stats, - defense
32:_Increased melee abilities, lowered defense_
48:  * -4 [defense](Defense.md "Defense")
49:  * +10% [melee damage](Melee_damage.md "Melee damage")
50:  * +2% melee [critical strike chance](Critical_strike_chance "Critical strike chance")
51:  * +10% [melee speed](Melee_speed "Melee speed")
52:  * +5 [Fishing Power](Fishing_Power.md "Fishing Power")
59:  * 1.1× defense
60:  * 1.1× [damage](Damage.md "Damage")
71:[](Ale.md "Ale")[Ale](Ale.md "Ale") | 2 minutes   

===CURSEDINFERNO 1.4.1/1.4.0.1===
[ Desktop version](Desktop_version_history.md "Desktop version history")

  * [Desktop 1.4.1](Desktop_1.4.1 "Desktop 1.4.1"): 
    * Damage per second to enemies doubled from 12 to 24.
    * Significantly more enemies are now susceptible to Cursed Inferno.

  * [Desktop 1.4.0.1](Desktop_1.4.0.1 "Desktop 1.4.0.1"): 
    * Damage per second to both players and enemies doubled from 6 to 12.
    * Affected enemies now take 10% more [knockback](Knockback.md "Knockback").
    * Cursed Inferno duration from [Ghoul](Ghoul "Ghoul"), [Clinger](Clinger.md "Clinger"), and [Spazmatism](The_Twins.md "The Twins") decreased somewhat to mitigate the increased damage to the player.

  * [Desktop 1.1](Desktop_1.1 "Desktop 1.1"): Introduced.
===BLEEDING 1.4.5===
[ Desktop version](Desktop_version_history.md "Desktop version history")

  * [Desktop 1.4.5.0](Desktop_1.4.5.0 "Desktop 1.4.5.0"): 
    * Enemies inflicted with Bleeding now lose 12 health per second.
    * Now inflicted by the [Harpoon](Harpoon.md "Harpoon"), the [Stylish Scissors](Stylish_Scissors.md "Stylish Scissors") and the [Bloody Machete](Bloody_Machete.md "Bloody Machete").
    * Can now be inflicted by a slime [variant](Slimes#Special_variants "Slimes") carrying [Spikes](Spike.md "Spike").
    * Now inflicted by [Sharp Spike Blocks](Sharp_Spike_Block.md "Sharp Spike Block").

  * [Desktop 1.1](Desktop_1.1 "Desktop 1.1"): Introduced.

===BURNING 1.4.5/1.3.0.1===
[ Desktop version](Desktop_version_history.md "Desktop version history")

  * [Desktop 1.4.5.0](Desktop_1.4.5.0 "Desktop 1.4.5.0"): 
    * [Molten armor](Molten_armor.md "Molten armor") set bonus and [Superheated Blood](Superheated_Blood.md "Superheated Blood") (Lava Shark) now grant immunity to burning blocks.
    * Can now be inflicted by a slime [variant](Slimes#Special_variants "Slimes") carrying [Hellstone](Hellstone.md "Hellstone").

  * [Desktop 1.3.0.2](Desktop_1.3.0.2 "Desktop 1.3.0.2"): No longer caused by developer items in Classic Mode.

  * [Desktop 1.3.0.1](Desktop_1.3.0.1 "Desktop 1.3.0.1"): 
    * No longer caused by developer items when worn in [Expert Mode](Expert_Mode.md "Expert Mode").
    * Sloping Meteorite, Hellstone, and Hellstone Brick no longer prevents this debuff.

  * [Desktop 1.2](Desktop_1.2 "Desktop 1.2"): Introduced.

```


---

## 🤖 Assistant · 2026-08-12T18:33:37.500Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Great. Tipsy page has more detail: let me get the Tipsy NPC attack speed line and duration. Also get Darkness 1.4.0.1/1.3.0.1 and Confused 1.4.5.0 and Stinky 1.4.5.0, Suffocation details, Chilled notes, Frozen notes, Midas notes, Mana Sickness notes, Electrified notes.

Let me batch.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:33:38.695Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && echo \"===TIPSY NPC===\"; sed -n '54,70p' Tipsy.md; echo \"===DARKNESS 1.4.0.1===\"; sed -n '77,90p' Darkness.md; echo \"===CONFUSED 1.4.5===\"; sed -n '505,512p' Confused.md; echo \"===STINKY 1.4.5===\"; sed -n '68,76p' Stinky.md",
 "description": "Extract Tipsy NPC stats and remaining history notes"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:33:38.725Z

**📎 ToolResult**

```
===TIPSY NPC===

While the effects are mostly beneficial, it is still a debuff and therefore cannot be removed manually like [buffs](Buffs.md "Buffs").[a] Instead, it can be removed by healing at the [Nurse](Nurse.md "Nurse"). 

Tipsy can also be applied to NPCs (by using the [Ale Tosser](Ale_Tosser.md "Ale Tosser")). This makes NPCs produce Ale particle effect, and grants affected NPCs:[1]

  * 1.1× defense
  * 1.1× [damage](Damage.md "Damage")
  * 0.9× attack interval (about +11% [attack speed](Attack_speed.md "Attack speed"))

These increases is calculated multiplicatively after all other [NPC stat boosts](NPC_stat_boosts.md "NPC stat boosts") have been calculated. 

## Causes

### From item

From  | Duration   
---|---  
===DARKNESS 1.4.0.1===
[ Desktop version](Desktop_version_history.md "Desktop version history")

  * [Desktop 1.4.0.1](Desktop_1.4.0.1 "Desktop 1.4.0.1"): 
    * Now causes the player's eyes to close while active.
    * Now lasts for 3 hours in [Master Mode](Master_Mode.md "Master Mode") if inflicted by the [Red Potion](Red_Potion.md "Red Potion").
    * Can now be inflicted by the [Crimslime](Crimslime.md "Crimslime") and the new [Blood Mummy](Blood_Mummy.md "Blood Mummy") enemy.

  * [Desktop 1.3.0.1](Desktop_1.3.0.1 "Desktop 1.3.0.1"): 
    * Can now be inflicted by the [Brain of Cthulhu](Brain_of_Cthulhu.md "Brain of Cthulhu") and its [Creeper](Creeper.md "Creeper") minions in [Expert Mode](Expert_Mode.md "Expert Mode") for 5 to 10 seconds at a 1/8 and 1/24 chance, respectively.
    * Now has a 1/6 (16.67%) chance of being inflicted each second by the new [Feral Bite](Feral_Bite.md "Feral Bite") debuff, which is inflicted by [Bats](Bats.md "Bats") in Expert Mode.
    * Now lasts for 30 seconds in Expert Mode (and for 2 hours if inflicted by the [Red Potion](Red_Potion.md "Red Potion")).

  * [Desktop 1.2.2](Desktop_1.2.2 "Desktop 1.2.2"): Can now be inflicted for one hour by the [Red Potion](Red_Potion.md "Red Potion").

===CONFUSED 1.4.5===
[ Desktop version](Desktop_version_history.md "Desktop version history")

  * [Desktop 1.4.5.0](Desktop_1.4.5.0 "Desktop 1.4.5.0"): 
    * [Purple Clubberfish](Purple_Clubberfish.md "Purple Clubberfish"), [Ale Tosser](Ale_Tosser.md "Ale Tosser"), [Anchor](Anchor.md "Anchor") and [Golem Fist](Golem_Fist.md "Golem Fist") now have a chance to inflict Confused.
    * [Bee Keeper](Bee_Keeper.md "Bee Keeper")'s Confused debuff chance increased from 90% to 100%.

  * [Desktop 1.1](Desktop_1.1 "Desktop 1.1"): Introduced.

===STINKY 1.4.5===
[ Desktop version](Desktop_version_history.md "Desktop version history")

  * [Desktop 1.4.5.0](Desktop_1.4.5.0 "Desktop 1.4.5.0"): 
    * Now decreases the player's luck by 0.25.
    * Can now be inflicted by [Poo Boulders](Poo_Boulder.md "Poo Boulder"), as well as a slime [variant](Slimes#Special_variants "Slimes") carrying [Poo](Poo.md "Poo").
    * Can now be removed by [water](Water.md "Water").
    * Can now be removed from enemies and NPCs via the [Wet](Wet.md "Wet") debuff.
    * Now causes NPCs to flee.

```


---

## 🤖 Assistant · 2026-08-12T18:37:01.626Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now remaining debuff page specifics:
- Suffocation page: 20 DPS and causes (sand/silt/slush while buried).
- Chilled page: 0.75× note, water in snow biome.
- Frozen: durations 0.33–2 s.
- Midas notes: 10–50% more coins; on players? "afflicted target drops 10-50% more coins".
- Mana Sickness: mechanics (25% reduction, decays 1% per 0.2 s = 5%/s, 5–10 s duration, stacking to 50%).
- Electrified notes: DPS when moving.
- Poisoned notes: player 2, enemy 6, 1.4.4 change.
- On Fire notes: Oiled interaction.
- Ichor page: durations 7–15 s (index). The Ichor_(debuff) page: causes list. Also note Ichor debuff on enemies: armor penetration +15.
- Frostburn: 8 DPS, 6 s, 1.4.1 change.
- Frozen: 0.33–2 s.
- Weak: stat mods −4 def, −5.1% melee dmg, −5.1% melee speed, −10% move speed; 60–300 s.
- Slow: 0.5× movement.

Let me grab the lead paragraphs of these pages for exact wording.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:37:03.454Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && for f in \"Suffocation\" \"Chilled\" \"Frozen\" \"Midas\" \"Mana_Sickness\" \"Electrified\" \"Weak\" \"Slow\" \"Darkness\" \"Bleeding\" \"Stinky\" \"Daybroken\" \"Burning\"; do echo \"##### $f #####\"; grep -m1 -E '\\*\\*[A-Za-z !]+(\\*\\*)? is a (debuff|Hardmode)' \"$f.md\" | sed -E 's/\\[\\]\\([^)]*\\)//g; s/\\[([^]]*)\\]\\([^)]*\\)/\\1/g' | head -c 620; echo; done",
 "description": "Extract lead paragraphs for debuffs"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:37:10.592Z

**📎 ToolResult**

```
##### Suffocation #####

##### Chilled #####

##### Frozen #####

##### Midas #####

##### Mana_Sickness #####

##### Electrified #####

##### Weak #####

##### Slow #####

##### Darkness #####

##### Bleeding #####

##### Stinky #####

##### Daybroken #####

##### Burning #####

```


---

## 🤖 Assistant · 2026-08-12T18:37:12.926Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The regex didn't match. The lead sentence format may be "**Suffocation** is a debuff" but with a bold-marker issue. Let me just grep for "is a" lines.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:37:13.812Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && for f in \"Suffocation\" \"Chilled\" \"Frozen\" \"Midas\" \"Mana_Sickness\" \"Electrified\" \"Weak\"; do echo \"##### $f #####\"; grep -m1 -n 'is a debuff' \"$f.md\" | sed -E 's/\\[\\]\\([^)]*\\)//g; s/\\[([^]]*)\\]\\([^)]*\\)/\\1/g' | head -c 600; echo; done",
 "description": "Extract debuff lead sentences"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:37:19.000Z

**📎 ToolResult**

```
##### Suffocation #####

##### Chilled #####

##### Frozen #####

##### Midas #####

##### Mana_Sickness #####

##### Electrified #####

##### Weak #####

```


---

## 🤖 Assistant · 2026-08-12T18:37:21.449Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
grep -m1 -n returns a line number prefix but no content? That means lines exist but sed output truncated to 600 chars starting with line number... no, output is empty entirely. Maybe the pattern 'is a debuff' doesn't appear. Let me check the structure of Suffocation.md directly with Read.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:37:22.167Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Suffocation.md",
 "limit": 40,
 "offset": 38
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:37:22.172Z

**📎 ToolResult**

```
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
48	[](Crimsand_Block "Crimsand Block") | [Crimsand Block](Crimsand_Block "Crimsand Block") | Until the player gets out from under the Crimsand Blocks   
49	[](Silt_Block.md "Silt Block") | [Silt Block](Silt_Block.md "Silt Block") | Until the player gets out from under the Silt Blocks   
50	[](Slush_Block.md "Slush Block") | [Slush Block](Slush_Block.md "Slush Block") | Until the player gets out from under the Slush Blocks   
51	  
52	### Self-induced
53	
54	From  | Duration  | Chance   
55	---|---|---  
56	[](Red_Potion.md "Red Potion") | [Red Potion](Red_Potion.md "Red Potion")**** __(Desktop, Console and Mobile versions)(except [For the Worthy](For_the_Worthy.md "For the Worthy") and [Zenith](Zenith_\(seed\) "Zenith \(seed\)") worlds) | 1 / [2](Expert_Mode.md "Expert Mode") / [3](Master_Mode.md "Master Mode") hours  | 1/1 (100%)   
57	  
58	## Notes
59	
60	  * Suffocation will be caused only be the blocks listed above, and not by any other blocks the player may get clipped inside of. For example, [Obsidian](Obsidian.md "Obsidian") forming over the player or being [hoiked](Hoik.md "Hoik") into other blocks will not cause Suffocation damage.
61	
62	## Trivia
63	
64	  * The Suffocation debuff icon features a blue face, which is a common symptom of [asphyxiation](https://en.wikipedia.org/wiki/en:asphyxia "wikipedia:en:asphyxia"). 
65	    * It also shows two open palms crossed over the throat, which is the universal sign of choking.
66	  * Dying from suffocation will display one of the following unique [death messages](Death_message.md "Death message"): 
67	    * _“ <Player name> couldn't breathe.”_
68	    * _“ <Player name> was buried alive.”_
69	
70	## History
71	
72	[ Desktop version](Desktop_version_history.md "Desktop version history")
73	
74	  * [Desktop 1.2.3](Desktop_1.2.3 "Desktop 1.2.3"): Running underwater no longer causes flashes of the Suffocation debuff.
75	
76	  * [Desktop 1.2](Desktop_1.2 "Desktop 1.2"): Introduced.
77	

```


---

## 🤖 Assistant · 2026-08-12T18:37:32.699Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good — Suffocation sources. The infobox says −20 health per second, no regen.

Let me check Chilled.md notes and Frozen.md lead for the movement multiplier statement and water-in-snow info, and Mana_Sickness.md lead.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:37:32.920Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Chilled.md",
 "limit": 45,
 "offset": 36
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:37:32.928Z

**📎 ToolResult**

```
36	
37	### Internal name
38	
39	`Chilled`
40	
41	**Chilled** is a [debuff](Debuffs.md "Debuffs") which moderately reduces the player's [movement speed](Movement_speed.md "Movement speed"), similar to [Slow](Slow.md "Slow"). It is usually inflicted by enemies found in the [Snow](Snow_biome.md "Snow biome") or [Ice](Ice_biome.md "Ice biome") [biomes](Biomes.md "Biomes"). In [Expert Mode](Expert_Mode.md "Expert Mode")**** __(Desktop, Console and Mobile versions) , it is also caused by touching [water](Water.md "Water") or [Shimmer](Shimmer.md "Shimmer")**** __(Desktop, Console and Mobile versions) in a Snow biome, and for five seconds after getting out. 
42	
43	Most enemies that can inflict Chilled can also inflict the [Frozen](Frozen.md "Frozen") debuff. 
44	
45	The debuff can be negated by equipping the [Hand Warmer](Hand_Warmer.md "Hand Warmer"), [Ankh Shield](Ankh_Shield.md "Ankh Shield"), ****__(Desktop, Console and Mobile versions) or a full set of [Snow armor](Snow_armor.md "Snow armor"). Additionally, [Arctic Diving Gear](Arctic_Diving_Gear.md "Arctic Diving Gear") will protect the player from Chilled afflicted by submerging in liquids, but not other sources of Chilled. 
46	
47	## Causes
48	
49	### From enemy
50	
51	From  | Duration  | Chance   
52	---|---|---  
53	[](Ice_Slime.md "Ice Slime") | [Ice Slime](Ice_Slime.md "Ice Slime") | 10 / [20](Expert_Mode.md "Expert Mode") / [25](Master_Mode.md "Master Mode") seconds  | 1/12 (8.33%)  
54	[](Spiked_Ice_Slime.md "Spiked Ice Slime") | [Spiked Ice Slime](Spiked_Ice_Slime.md "Spiked Ice Slime") | 20 / [40](Expert_Mode.md "Expert Mode") / [50](Master_Mode.md "Master Mode") seconds  | 1/1 (100%) (both contact and Ice Spike)   
55	[](Ice_Bat.md "Ice Bat") | [Ice Bat](Ice_Bat.md "Ice Bat") | 15 / [30](Expert_Mode.md "Expert Mode") / [37.5](Master_Mode.md "Master Mode") seconds  | 1/15 (6.67%)  
56	[](Ice_Golem.md "Ice Golem") | [Ice Golem](Ice_Golem.md "Ice Golem") | 45 / [90](Expert_Mode.md "Expert Mode") / [112.5](Master_Mode.md "Master Mode") seconds  | 1/1 (100%) (Frost Beam)   
57	[](Icy_Merman.md "Icy Merman") | [Icy Merman](Icy_Merman.md "Icy Merman") | 25 / [50](Expert_Mode.md "Expert Mode") / [62.5](Master_Mode.md "Master Mode") seconds  | 1/1 (100%) (Icewater Spit)   
58	[](Ice_Queen.md "Ice Queen") | [Ice Queen](Ice_Queen.md "Ice Queen") | 5 / [10](Expert_Mode.md "Expert Mode") / [12.5](Master_Mode.md "Master Mode") seconds  | 1/2 (50%) (Frost Wave)   
59	10 / [20](Expert_Mode.md "Expert Mode") / [25](Master_Mode.md "Master Mode") seconds  | 1/2 (50%) (Frost Wave)   
60	5 / [10](Expert_Mode.md "Expert Mode") / [12.5](Master_Mode.md "Master Mode") seconds  | 1/3 (33.33%) (Frost Shard)   
61	10 / [20](Expert_Mode.md "Expert Mode") / [25](Master_Mode.md "Master Mode") seconds  | 1/3 (33.33%) (Frost Shard)   
62	  
63	### From environment
64	
65	From  | Duration  | Chance   
66	---|---|---  
67	[](Water.md "Water") | [Water](Water.md "Water")in [Snow biome](Snow_biome.md "Snow biome") | [5](Expert_Mode.md "Expert Mode") / [6.25](Master_Mode.md "Master Mode") seconds  | [1/1 (100%)](Expert_Mode.md "Expert Mode")  
68	[](Shimmer.md "Shimmer") | [Shimmer](Shimmer.md "Shimmer")**** __(Desktop, Console and Mobile versions) in [Snow biome](Snow_biome.md "Snow biome")  
69	  
70	## Notes
71	
72	  * While this debuff is active, moving causes sounds and dust effects similar to those of the [Hermes Boots](Hermes_Boots.md "Hermes Boots").
73	  * Chilled even affects movement on certain [mounts](Mounts.md "Mounts"). [Saddles](Saddles.md "Saddles"), [Blessed Apple](Blessed_Apple.md "Blessed Apple"), [Fuzzy Carrot](Fuzzy_Carrot.md "Fuzzy Carrot"), [Goat Skull](Goat_Skull.md "Goat Skull"), [Hardy Saddle](Hardy_Saddle.md "Hardy Saddle"), [Hexxed Branch](Hexxed_Branch.md "Hexxed Branch"), [Reindeer Bells](Reindeer_Bells.md "Reindeer Bells"), and [Scaly Truffle](Scaly_Truffle.md "Scaly Truffle") are all slowed down under the effect of this debuff.
74	  * When entering [water](Water.md "Water") while this debuff is active, the timer on the debuff will be invisible. 
75	    * This does not apply when player has the debuff longer than 5 seconds inside the [Tundra](Ice_biome.md "Ice biome") biome.
76	
77	## History
78	
79	[ Desktop version](Desktop_version_history.md "Desktop version history")
80	

```


---

## 🤖 Assistant · 2026-08-12T18:37:40.730Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. Now Mana_Sickness.md and Midas.md and Frozen.md lead/notes. And Weak.md, Slow.md movement multipliers (from index: Chilled 0.75×, Slow 0.5×, Burning 0.5×). Also Electrified notes. Let me read Mana_Sickness.md around the top.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:37:40.970Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Mana_Sickness.md",
 "limit": 45,
 "offset": 36
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:37:40.977Z

**📎 ToolResult**

```
36	
37	The magic damage reduction is multiplicative rather than additive, and is applied after all damage multipliers. For example, if the player has +100% damage from buffs and items, the total damage with the debuff at 5 seconds left comes to 150% (200% × (1 - 25%); -25% comes from Mana Sickness). 
38	
39	## Causes
40	
41	### From item
42	
43	From | Duration   
44	---|---  
45	[](Lesser_Mana_Potion.md "Lesser Mana Potion")[Lesser Mana Potion](Lesser_Mana_Potion.md "Lesser Mana Potion") | 5 seconds   
46	[](Mana_Potion.md "Mana Potion")[Mana Potion](Mana_Potion.md "Mana Potion")  
47	[](Lesser_Restoration_Potion "Lesser Restoration Potion")[Lesser Restoration Potion](Lesser_Restoration_Potion "Lesser Restoration Potion")**** __(Old-gen console and 3DS versions)  
48	[](Greater_Mana_Potion.md "Greater Mana Potion")[Greater Mana Potion](Greater_Mana_Potion.md "Greater Mana Potion")  
49	[](Super_Mana_Potion.md "Super Mana Potion")[Super Mana Potion](Super_Mana_Potion.md "Super Mana Potion")**** __(Desktop, Console, Old-gen console and Mobile versions)  
50	[](Restoration_Potion.md "Restoration Potion")[Restoration Potion](Restoration_Potion.md "Restoration Potion")(****__(Old-gen console and 3DS versions) only)  
51	  
52	## Notes
53	
54	  * The magic damage reduction is calculated by the following formula, with the remaining debuff duration measured in ticks.[3][4]
55	
56	    [math]\displaystyle{ \text{Reduction multiplier}=0.25\times\frac{\text{Debuff duration}}{300} }[/math]
57	
58	## See also
59	
60	  * [Potion Sickness](Potion_Sickness.md "Potion Sickness")
61	
62	## History
63	
64	[ Desktop version](Desktop_version_history.md "Desktop version history")
65	
66	  * [Desktop 1.3.0.1](Desktop_1.3.0.1 "Desktop 1.3.0.1"): Now the duration stacks and damage-reducing effect increases if mana-restoring items are consumed while the debuff is active, up to 10 seconds and 50% lowered magic damage.
67	
68	  * [Desktop 1.2.3](Desktop_1.2.3 "Desktop 1.2.3"): Introduced.
69	
70	[ Console version](Console_version.md "Console version")
71	
72	  * [Console 1.06](Console_1.06.md "Console 1.06"): Introduced.
73	
74	[ Nintendo Switch version](Switch_version.md "Switch version")
75	
76	  * [Switch 1.0.711.6](Switch_1.0.711.6.md "Switch 1.0.711.6"): Introduced.
77	
78	[ Mobile version](Mobile_version.md "Mobile version")
79	
80	  * [Mobile 1.2.11212](Mobile_1.2.11212.md "Mobile 1.2.11212"): Introduced.

```


---

## 🤖 Assistant · 2026-08-12T18:37:47.733Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Mana Sickness: formula Reduction = 0.25 × duration/300 (ticks). Need the lead sentence (lines 30-36). Let me read lines 28-37.

Also Midas and Frozen leads. Let me batch read.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:37:47.956Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Mana_Sickness.md",
 "limit": 10,
 "offset": 28
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:37:47.960Z

**📎 ToolResult**

```
28	
29	### Internal name
30	
31	`ManaSickness`
32	
33	**Mana Sickness** is a [debuff](Debuff "Debuff") that reduces the player's [magic damage](Magic_damage.md "Magic damage") after they consume any [mana](Mana.md "Mana")-restoring item. Automatically drinking Mana Potions with the [Mana Flower](Mana_Flower.md "Mana Flower") will also cause the debuff. Whenever a mana-restoring item is consumed, the player is inflicted with 5 seconds of Mana Sickness.[1] The percentage of magic damage reduction is proportional to the remaining debuff duration (see Notes for formula), reducing by 1% every 1/5 second; at 5 seconds remaining, the damage reduction is 25%. All mana-restoring items inflict the same length of the debuff; for example, a [Lesser Mana Potion](Lesser_Mana_Potion.md "Lesser Mana Potion") induces the same duration of Mana Sickness as a [Greater Mana Potion](Greater_Mana_Potion.md "Greater Mana Potion"). 
34	
35	****__(Desktop, Console and Mobile versions) If the player consumes additional mana-restoring items while the debuff is active, the duration will be increased by 5 seconds for each item consumed, up to a maximum of 10 seconds (50% damage reduction).[2]
36	
37	The magic damage reduction is multiplicative rather than additive, and is applied after all damage multipliers. For example, if the player has +100% damage from buffs and items, the total damage with the debuff at 5 seconds left comes to 150% (200% × (1 - 25%); -25% comes from Mana Sickness). 

```


---

## 🤖 Assistant · 2026-08-12T18:37:48.170Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Midas.md",
 "limit": 14,
 "offset": 36
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:37:48.177Z

**📎 ToolResult**

```
36	
37	### From player
38	
39	From  | Duration  | Chance   
40	---|---|---  
41	[](Flask_of_Gold.md "Flask of Gold") | [Flask of Gold](Flask_of_Gold.md "Flask of Gold") | 2 seconds  | 100%   
42	[](Golden_Bullet.md "Golden Bullet") | [Golden Bullet](Golden_Bullet.md "Golden Bullet") | 2 seconds  | 100%   
43	  
44	## Trivia
45	
46	  * [Midas](https://en.wikipedia.org/wiki/en:Midas "wikipedia:en:Midas") is the name of a king in Greek mythology who was rewarded by [Dionysus](https://en.wikipedia.org/wiki/en:Dionysus "wikipedia:en:Dionysus") with the ability to turn anything that he touched into gold.
47	  * The debuff icon displays an item that looks similar to the [Lucky Coin](Lucky_Coin.md "Lucky Coin"), which functions in a similar manner to the debuff when equipped. The main difference is that the Lucky Coin gives a _chance_ for enemies to drop extra coins when _damaged_ , not when slain.
48	
49	## History

```


---

## 🤖 Assistant · 2026-08-12T18:37:57.955Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Midas lead is above line 36 (lines 28-35). Let me read Midas.md lines 20-36. Actually I have enough from the index: "Causes afflicted target to drop 10-50% more coins than usual on death. Duration 2 seconds." But let me confirm the lead sentence for the exact 10-50% claim.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:37:58.167Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Midas.md",
 "limit": 10,
 "offset": 28
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:37:58.174Z

**📎 ToolResult**

```
28	
29	### Internal name
30	
31	`Midas`
32	
33	**Midas** is a [Hardmode](Hardmode.md "Hardmode") [debuff](Debuff "Debuff") that causes affected [enemies](Enemies.md "Enemies") to drop 10-49% more [coins](Coins.md "Coins") than usual on death. Affected enemies glow golden, much like enemies afflicted with the [Ichor debuff](Ichor_\(debuff\) "Ichor \(debuff\)"). 
34	
35	## Causes
36	
37	### From player

```


---

## 🤖 Assistant · 2026-08-12T18:38:07.349Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Midas: 10-49% more coins on the page vs 10-50% in the index — discrepancy to note.

Now let me get a few remaining things:
1. Frozen.md lead (durations 0.33–2 s and what prevents it).
2. Electrified lead (DPS).
3. Weak.md stat list.
4. Acid Venom history/Legacy Venom (Venom name change / old values).
5. Love_Potion (Lovestruck): +10% happiness, 30 s — check page.
6. Betsy's_Wrath.md (Betsy's Curse): 40 armor pen, 5 s; verify page.
7. Brain_Suckler.md (Obstructed) — verify duration.
8. Ogre.md — "Ogre Sped" not present; Ogre has Oozed (÷3 horizontal speed, 15 s). Confirm.
9. Star in a Bottle discrepancy noted.
10. Warmth potion: +30% damage reduction from cold enemies — check the "see below" list maybe.

Also the buff duration merge/refresh rules: not in Buffs.md. Maybe in "Buff_potions.md" or "Potions.md". Let me grep for "duration" stacking statements, e.g., "Using the potion again while the buff is active will refresh its duration" — I recall the wiki has a note on buff potions: "Buff durations do not stack; drinking another potion while the buff is active only resets the timer". Let me search.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:38:08.419Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && grep -rn -iE 'duration (will )?not stack|does not stack.*duration|reset.{0,20}timer|refresh.{0,30}duration|duration.{0,30}refresh|timer.{0,30}reset' --include='*.md' Buff_potions.md Potions.md Quick_Buff.md Buffs.md 2>/dev/null | head -10; echo \"===BUFFPOTIONS EXISTS?===\"; ls | grep -iE '^Buff_potions|^Potions\\.md|^Quick_Buff'",
 "description": "Search for buff duration stacking rules"
}
```


---

## 🤖 Assistant · 2026-08-12T18:38:08.648Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Love_Potion.md",
 "limit": 14,
 "offset": 40
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:38:19.971Z

**📎 ToolResult**

```
===BUFFPOTIONS EXISTS?===
Buff_potions
Buff_potions.md
Potions.md
Quick_Buff.md

```


---

## 👤 User(sidechain) · 2026-08-12T18:38:19.974Z

**📎 ToolResult**

```
40	Use|   
41	---|---  
42	Impact|   
43	  
44	  * Internal [Item ID](Item_IDs.md "Item IDs"): **2352** ****__(Desktop, Console, Old-gen console and Mobile versions)
45	  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **119**** __(Desktop, Console, Old-gen console and Mobile versions)**
46	  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **370**
47	
48	The Love Potion in action.
49	
50	The **Love Potion** is a [Hardmode](Hardmode.md "Hardmode") thrown [potion](Potion "Potion") that functions similarly to [Thrown Water](Thrown_Water.md "Thrown Water"). Upon colliding with solid [blocks](Blocks.md "Blocks"), it inflicts the **Lovestruck** [debuff](Debuff "Debuff") on players (including the user), [enemies](Enemies.md "Enemies"), [critters](Critters.md "Critters"), and [NPCs](NPCs.md "NPCs") within a radius of 9 tiles, causing them to emit red hearts for 30 seconds, similar to the [Water Gun](Water_Gun.md "Water Gun")'s dripping effect. It also increases affected NPCs' happiness by 10% for the duration of the effect. 
51	
52	## Crafting
53	

```


---

## 🤖 Assistant · 2026-08-12T18:38:23.474Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Lovestruck: 30 seconds, +10% NPC happiness, radius 9 tiles. Good.

Now Buff_potions.md — check for duration merge rules.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:38:23.959Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && grep -n -iE 'stack|duration|refresh|reset' Buff_potions.md | head -20",
 "description": "Search Buff_potions for duration rules"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:38:23.979Z

**📎 ToolResult**

```
18:Potion| Ingredients| Tooltip| Duration| Icon| Type

```


---

## 🤖 Assistant · 2026-08-12T18:38:30.805Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Buff_potions.md",
 "limit": 20,
 "offset": 10
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:38:30.810Z

**📎 ToolResult**

```
10	For the differences of this information on [Old-gen console](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [3DS](Legacy%3A3DS_version "Legacy:3DS version"), see **[Legacy:Buff potions](Legacy%3ABuff_potions "Legacy:Buff potions")**.
11	
12	Main article: [Potions](Potions.md "Potions")
13	
14	See also: [Flasks](Flasks.md "Flasks")
15	
16	**Buff potions** grant the character a temporary, usually short-lived [buff](Buff "Buff") when consumed. 
17	
18	Potion| Ingredients| Tooltip| Duration| Icon| Type  
19	---|---|---|---|---|---  
20	[](Ammo_Reservation_Potion.md "Ammo Reservation Potion")[Ammo Reservation Potion](Ammo_Reservation_Potion.md "Ammo Reservation Potion")| 
21	
22	  * [](Bottled_Water.md "Bottled Water")[Bottled Water](Bottled_Water.md "Bottled Water")
23	  * [](Double_Cod.md "Double Cod")[Double Cod](Double_Cod.md "Double Cod")
24	  * [](Moonglow.md "Moonglow")[Moonglow](Moonglow.md "Moonglow")
25	
26	| 20% chance to save ammo| 8 minutes| | Battle  
27	[](Archery_Potion.md "Archery Potion")[Archery Potion](Archery_Potion.md "Archery Potion")| 
28	
29	  * [](Bottled_Water.md "Bottled Water")[Bottled Water](Bottled_Water.md "Bottled Water")

```


---

## 🤖 Assistant · 2026-08-12T18:38:34.892Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Buff_potions.md is just a table. No merge/refresh rule.

Where does the wiki state buff duration merging? I recall on individual potion pages under "Notes": "Like all buffs, the duration ... does not stack". Let me grep a couple of potion pages for "Notes" mentioning stack. E.g., Regeneration_Potion.md Notes. Let me grep for "stack" in Regeneration_Potion.md and Ironskin_Potion.md.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:38:36.428Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && grep -n -iE 'stack|multipl|additive|duration' Regeneration_Potion.md Ironskin_Potion.md Swiftness_Potion.md Battle_Potion.md | grep -v -E 'Bottled|Ingredient|Moonglow|Daybloom|Blinkroot|Deathweed|Fireblossom|Shiverthorn|Waterleaf|Crate|ratio|Rarity|Tooltip' | head -20",
 "description": "Search potion notes for stacking rules"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:38:36.448Z

**📎 ToolResult**

```
Swiftness_Potion.md:67:The **Swiftness Potion** is a [buff potion](Buff_potion "Buff potion") which grants the **Swiftness** [buff](Buff "Buff") when consumed. The buff increases the player's maximum [movement speed](Movement_speed.md "Movement speed") by 25%, but does not stack with [sprinting accessories](Sprinting_accessories.md "Sprinting accessories") (such as [Hermes Boots](Hermes_Boots.md "Hermes Boots")), nor does it affect the speed of [mounts](Mounts.md "Mounts"). This lasts for 8 minutes, but can be canceled at any time by right-clicking the icon ([](Desktop_version_history.md "Desktop version")), by selecting the icon using Cycle Next/Previous Buff and then pressing Remove Buff ([](Console_version.md "Console version")), or by double-tapping the buff icon ([](Mobile_version.md "Mobile version")). 
Swiftness_Potion.md:92:  * The Swiftness buff stacks with the effects of the [Slice of Cake](Slice_of_Cake.md "Slice of Cake").
Swiftness_Potion.md:103:  * [Desktop 1.4.4](Desktop_1.4.4 "Desktop 1.4.4"): Stack limit increased from 30 to 9999.
Swiftness_Potion.md:1784:  *[1.98]: Melee damage multiplier
Swiftness_Potion.md:1789:  *[2.26]: Ranged damage multiplier
Battle_Potion.md:78:  * The effect stacks between players because each player spawns their own NPCs. It also increases the maximum amount of enemies that can be spawned, allowing multiple players to drink them and spawn enemies at a much faster than intended rate.
Battle_Potion.md:93:  * [Desktop 1.4.4](Desktop_1.4.4 "Desktop 1.4.4"): Stack limit increased from 30 to 9999.
Ironskin_Potion.md:108:  * [Desktop 1.4.4](Desktop_1.4.4 "Desktop 1.4.4"): Stack limit increased from 30 to 9999.
Ironskin_Potion.md:1782:  *[1.98]: Melee damage multiplier
Ironskin_Potion.md:1787:  *[2.26]: Ranged damage multiplier

```


---

## 🤖 Assistant · 2026-08-12T18:38:43.227Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
No explicit general "buff duration merge/refresh" rule on Buffs.md or potion pages. I'll report that Buffs.md contains no such rule; the only related statements found are: 44-buff cap (Buffs.md intro), buffs persist through world/server changes, death clears buffs except flasks (Buffs.md intro), Well_Fed.md "Only one of these buffs may be active at a time... most recently applied takes priority", Sunflower Happy! stacking with Peace Candle, Battle/Water Candle stacking, Calming/Battle stacking notes, Heart Lantern + Campfire stacking ("regeneration buffs from both items will stack"), Bast Statue non-stacking, Peace Candle non-stacking multiples, Garden Gnome non-stacking.

Also Alchemy Flask: "Increases newly received buff potion durations by 20%" (Buffs.md).

Now remaining debuff checks:
- Frozen.md lead + notes.
- Electrified lead.
- Weak lead.
- Acid Venom history / Legacy Venom differences.
- Betsy's_Wrath.md (Betsy's Curse).
- Ogre.md Oozed details (and confirm no "Ogre Sped").
- Brain_Suckler.md Obstructed.
- On Fire! full causes + notes (Oiled).
- Poisoned notes.
- Ichor_(debuff) lead + notes.
- Frostburn lead.
- Burning lead (0.5× movement).

Let me batch these greps/reads.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:38:43.458Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Frozen.md",
 "limit": 16,
 "offset": 36
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:38:43.461Z

**📎 ToolResult**

```
36	
37	`Frozen`
38	
39	A player inflicted with Frozen.
40	
41	This article is about the debuff. For the furniture set, see [Frozen furniture](Frozen_furniture.md "Frozen furniture"). 
42	
43	**Frozen** is a [debuff](Debuffs.md "Debuffs") that causes the player to briefly freeze in place, being completely unable to move or use any [weapons](Weapons.md "Weapons") or [items](Items.md "Items"), rendering the player completely vulnerable to most attacks. 
44	
45	The debuff can be negated by equipping the [Hand Warmer](Hand_Warmer.md "Hand Warmer") or ****__(Desktop, Console and Mobile versions) a full set of [Snow armor](Snow_armor.md "Snow armor"). 
46	
47	All enemies that can inflict Frozen can inflict the [Chilled](Chilled.md "Chilled") debuff as well (with the exception of [Deerclops](Deerclops.md "Deerclops")**** __(Desktop, Console and Mobile versions)). 
48	
49	## Causes
50	
51	### From enemy

```


---

## 🤖 Assistant · 2026-08-12T18:38:43.731Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Electrified.md",
 "limit": 20,
 "offset": 36
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:38:43.735Z

**📎 ToolResult**

```
36	
37	`Electrified`
38	
39	**Electrified** is a [Hardmode](Hardmode.md "Hardmode"), post-[Golem](Golem.md "Golem") [debuff](Debuff "Debuff") that causes the player to lose 4 health per second. If the player is moving left/right, they will lose an additional 16 health per second, totaling to a loss of 20 health per second. The damage inflicted by this debuff is capable of killing or severely weakening players relying on constant movement to avoid damage from [enemies](Enemies.md "Enemies"). Using a [hook](Hooks.md "Hooks") or teleporting with a [Rod of Discord](Rod_of_Discord.md "Rod of Discord") will not increase damage. Pressing [`◀ Left`](Game_controls.md "Game controls") or [`▶ Right`](Game_controls.md "Game controls") when unable to move (hooks, [blocks](Blocks.md "Blocks"), other debuffs, etc.) will also increase damage. 
40	
41	## Causes
42	
43	### From enemy
44	
45	From | Duration | Chance | Total damage  
46	---|---|---|---  
47	[](Tesla_Turret.md "Tesla Turret")[Tesla Turret](Tesla_Turret.md "Tesla Turret") | 5 seconds  | 2/3 (66.67%) | 20 / 100   
48	[](Gigazapper.md "Gigazapper")[Gigazapper](Gigazapper.md "Gigazapper") | 4-8 seconds  | 1/1 (100%) | 16-32 / 80-160   
49	  
50	## Notes
51	
52	  * Technically, the additional -16 HP/s life draining only happens if player presses [`◀ Left`](Game_controls.md "Game controls") or [`▶ Right`](Game_controls.md "Game controls") controls, whether player is actually moving is not the reason for it happening.
53	
54	## Trivia
55	

```


---

## 🤖 Assistant · 2026-08-12T18:38:45.622Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. Now Weak.md, Burning.md leads; Acid Venom history; Betsy's_Wrath.md; Ogre.md (Oozed); Brain_Suckler.md (Obstructed); On Fire! notes.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:38:45.855Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Weak.md",
 "limit": 22,
 "offset": 36
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:38:45.858Z

**📎 ToolResult**

```
36	### Internal name
37	
38	`Weak`
39	
40	This article is about the debuff that decreases player stats. For the modifier, see [Modifiers § Universal](Modifiers#Universal "Modifiers"). 
41	
42	**Weak** is a [debuff](Debuffs.md "Debuffs") that decreases the player's stats as follows: 
43	
44	  * −4 [defense](Defense.md "Defense")
45	  * −5.1% [melee damage](Melee_damage.md "Melee damage")
46	  * −5.1% [melee speed](Melee_speed "Melee speed")
47	  * −10% [movement speed](Movement_speed.md "Movement speed")
48	
49	The debuff can be negated by equipping [Vitamins](Vitamins.md "Vitamins") or its derivatives. 
50	
51	## Causes
52	
53	### From enemy
54	
55	From  | Duration  | Chance   
56	---|---|---  
57	[](Corruptor.md "Corruptor") | [Corruptor](Corruptor.md "Corruptor")([Vile Spit](Vile_Spit.md "Vile Spit")) | 5 / [10](Expert_Mode.md "Expert Mode") / [12.5](Master_Mode.md "Master Mode") minutes  | 1/20 (5%)  

```


---

## 🤖 Assistant · 2026-08-12T18:38:46.162Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Betsy's_Wrath.md",
 "limit": 20,
 "offset": 36
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:38:46.166Z

**📎 ToolResult**

```
36	Debuff tooltip|  _Defense is lowered_  
37	Duration| 10 seconds  
38	  
39	Projectile created
40	
41	  * Betsy's Wrath
42	
43	Sounds
44	
45	Use|   
46	---|---  
47	Impact|   
48	  
49	  * Internal [Item ID](Item_IDs.md "Item IDs"): **3870**
50	  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **203**
51	  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **711**
52	
53	Obtained from
54	
55	Classic

```


---

## 🤖 Assistant · 2026-08-12T18:38:47.973Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Betsy's Wrath infobox says Duration 10 seconds, while Debuffs.md index says 5 seconds for Betsy's Curse! Let me check the Betsy's_Wrath.md page text about the debuff (armor penetration). Let me read further.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:38:48.518Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && grep -n -iE 'armor penetration|Betsy.s Curse|40' \"Betsy's_Wrath.md\" | head -10",
 "description": "Find Betsy's Curse armor penetration"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:38:48.536Z

**📎 ToolResult**

```
34:Debuff| [](Betsy's_Wrath.md "Betsy's Curse")Betsy's Curse  
68:**Betsy's Wrath** is a [Hardmode](Hardmode.md "Hardmode"), post-[Golem](Golem.md "Golem") [wand](Wand "Wand") that has a 1/4 (25%) chance of being dropped by [Betsy](Betsy.md "Betsy") during Tier 3 of the [Old One's Army](Old_One's_Army.md "Old One's Army") [event](Event "Event"). When used, it fires three fireballs that travel in arcs. The fireballs explode upon impact with an [enemy](Enemy "Enemy") or a [block](Block "Block") and inflict the **Betsy's Curse** [debuff](Debuff "Debuff"), which adds 40 [armor penetration](Armor_penetration.md "Armor penetration") against affected entities for 10 seconds. 
74:  * The Betsy's Curse debuff cannot be inflicted against other players in [PvP](PvP.md "PvP").
75:  * Betsy's Wrath can be considered an upgrade to the [Golden Shower](Golden_Shower.md "Golden Shower"). Ichor also stacks with Betsy's Curse, for a total of 55 armor penetration.
84:Enemies immune to Betsy's Curse
124:  * [Desktop 1.4.4](Desktop_1.4.4 "Desktop 1.4.4"): Debuff's mechanic changed from lowering [defense](Defense.md "Defense") to adding [armor penetration](Armor_penetration.md "Armor penetration").
1069:  * [](Betsy's_Wrath.md "Betsy's Curse")Betsy's Curse
1167:  *[400]: Expertní mód
1169:  *[240]: Master Mode
1191:  *[400 required]: Journey Mode

```


---

## 🤖 Assistant · 2026-08-12T18:38:51.475Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Betsy's Curse: +40 armor penetration for 10 seconds (Betsy's_Wrath.md page). The Debuffs.md index says 5 seconds. Discrepancy noted. Also 1.4.4 changed mechanic from lowering defense to armor penetration. Also stacks with Ichor = 55 armor penetration.

Now Ogre.md (Oozed) and Brain_Suckler.md (Obstructed), and Burning lead, and Acid Venom history/Legacy, and On Fire notes.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:38:52.640Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && echo \"===OGRE Oozed===\"; grep -n -iE 'Oozed|Ogre Sped|movement' Ogre.md | head -8; echo \"===BRAINSUCKLER Obstructed===\"; grep -n -iE 'Obstructed|light|seconds' Brain_Suckler.md | head -8; echo \"===BURNING lead===\"; sed -n '42,56p' Burning.md",
 "description": "Extract Oozed, Obstructed, Burning details"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:38:52.673Z

**📎 ToolResult**

```
===OGRE Oozed===
30:Debuff| [](Ogre.md "Oozed")Oozed  
32:Debuff tooltip|  _Movement is significantly reduced_  
67:  * The Ogre will hurl out a ball of Ogre Spit into his hand before tossing it at the player. This attack is used when the Ogre is farther away from the player, and, while it only damages targets struck by the ball itself, it inflicts the [Oozed](Oozed "Oozed") [debuff](Debuff "Debuff") onto any nearby player for 15 seconds upon contact with tiles, slowing them down significantly.[1]
141:  * The Oozed [debuff](Debuff "Debuff") does not affect the speed of flying mounts that are not in contact with the ground, making them quite useful while fighting Ogres.
965:and Movement
1202:Movement
1210:  * [](Ogre.md "Oozed")Oozed
===BRAINSUCKLER Obstructed===
38:Debuff| [](Brain_Suckler.md "Obstructed")Obstructed  
53:The Obstructed debuff's screen effect.
55:The effects of the Obstructed debuff.
57:The **Brain Suckler** is a [Hardmode](Hardmode.md "Hardmode"), post-[Lunatic Cultist](Lunatic_Cultist.md "Lunatic Cultist") flying [enemy](Enemies.md "Enemies") that spawns in the area of the [Nebula Pillar](Nebula_Pillar.md "Nebula Pillar") during the [Lunar Events](Lunar_Events.md "Lunar Events"). It latches onto the player's head, dealing large amounts of damage at a steady rate, while also inflicting the **Obstructed** [debuff](Debuffs.md "Debuffs") for the remainder of the time it is on the player. The debuff causes the player's screen to darken significantly, except for a small area around the player, similar to the [Blackout](Blackout.md "Blackout") debuff. It additionally has the effect of [Bleeding](Bleeding.md "Bleeding"), preventing natural [health regeneration](Health_regeneration.md "Health regeneration").[1]
62:  * Unlike the Blackout and [Darkness](Darkness.md "Darkness") debuffs, Obstructed darkens the screen evenly, without factoring in light levels.
315:    * [Light](Light_Mummy.md "Light Mummy")
445:  * [Etherian Lightning Bug](Etherian_Lightning_Bug.md "Etherian Lightning Bug")
568:  * [](Empress_of_Light.md "Empress of Light")[Empress of Light](Empress_of_Light.md "Empress of Light")
===BURNING lead===
  * [](Hellfire_Treads.md "Hellfire Treads")[Hellfire Treads](Hellfire_Treads.md "Hellfire Treads")**** __(Desktop, Console and Mobile versions)
  * [](Terraspark_Boots.md "Terraspark Boots")[Terraspark Boots](Terraspark_Boots.md "Terraspark Boots")**** __(Desktop, Console and Mobile versions)
  * [](Obsidian_Horseshoe.md "Obsidian Horseshoe")[Obsidian Horseshoe](Obsidian_Horseshoe.md "Obsidian Horseshoe")
  * [](Obsidian_Skin_Potion.md "Obsidian Skin Potion")[Obsidian Skin Potion](Obsidian_Skin_Potion.md "Obsidian Skin Potion")

## Internal IDs

### [Buff ID](Buff_IDs.md "Buff IDs")

67

### Internal name

`Burning`

```


---

## 🤖 Assistant · 2026-08-12T18:38:54.097Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Burning.md",
 "limit": 12,
 "offset": 56
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:38:54.105Z

**📎 ToolResult**

```
56	
57	The effect when walking over [Hellstone Bricks](Hellstone_Brick.md "Hellstone Brick") and other burning blocks.
58	
59	Not to be confused with [On Fire!](On_Fire!.md "On Fire!").
60	
61	**Burning** is a [debuff](Debuffs.md "Debuffs") inflicted when the player comes in contact with [Hellstone](Hellstone.md "Hellstone"), [Hellstone Bricks](Hellstone_Brick.md "Hellstone Brick"), [Ancient Hellstone Bricks](Ancient_Hellstone_Brick.md "Ancient Hellstone Brick"), or [Meteorite](Meteorite.md "Meteorite"). The player continuously takes 30 damage per second and has their movement speed reduced until they are no longer in contact with the block. 
62	
63	The debuff can be negated by equipping the [Obsidian Skull](Obsidian_Skull.md "Obsidian Skull") or its derivatives, by drinking an [Obsidian Skin Potion](Obsidian_Skin_Potion.md "Obsidian Skin Potion"), or by equipping a full set of [Molten armor](Molten_armor.md "Molten armor"). 
64	
65	## Causes
66	
67	### From environment

```


---

## 🤖 Assistant · 2026-08-12T18:38:54.816Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && ls | grep -iE 'Legacy_Venom|Legacy_Acid'; echo \"===AV HISTORY===\"; grep -n -E '\\* \\[Desktop' Acid_Venom.md | head -8",
 "description": "Read Burning lead and check Acid Venom history"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:38:54.874Z

**📎 ToolResult**

```
Legacy_Venom_Arrow.md
Legacy_Venom_Bullet.md
Legacy_Venom_Staff.md
Legacy_Venom.md
===AV HISTORY===
111:  * [Desktop 1.4.1](Desktop_1.4.1 "Desktop 1.4.1"): 
115:  * [Desktop 1.4.0.1](Desktop_1.4.0.1 "Desktop 1.4.0.1"): 
120:  * [Desktop 1.2](Desktop_1.2 "Desktop 1.2"): Introduced.
493:  * [Desktop content](Category%3ADesktop_content "Category:Desktop content")

```


---

## 🤖 Assistant · 2026-08-12T18:38:56.490Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Acid_Venom.md",
 "limit": 14,
 "offset": 109
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:38:56.495Z

**📎 ToolResult**

```
109	[ Desktop version](Desktop_version_history.md "Desktop version history")
110	
111	  * [Desktop 1.4.1](Desktop_1.4.1 "Desktop 1.4.1"): 
112	    * Damage per second doubled from 15 to 30 on the enemy version of the debuff.
113	    * Venom was renamed to Acid Venom and now affects several metal, stone, undead, and poisonous enemies.
114	
115	  * [Desktop 1.4.0.1](Desktop_1.4.0.1 "Desktop 1.4.0.1"): 
116	    * Damage per second increased from 6 to 15 on both player and enemy versions of the debuff.
117	    * [Pygmy](Pygmy_Staff.md "Pygmy Staff") and [Queen Spider Staff](Queen_Spider_Staff.md "Queen Spider Staff") Venom duration decreased to mitigate the increased potency.
118	    * [Black Recluse](Black_Recluse.md "Black Recluse") and [Sand Poacher](Sand_Poacher.md "Sand Poacher") Venom duration decreased somewhat to mitigate the increased danger to the player.
119	
120	  * [Desktop 1.2](Desktop_1.2 "Desktop 1.2"): Introduced.
121	
122	[ Console version](Console_version.md "Console version")

```


---

## 🤖 Assistant · 2026-08-12T18:38:56.976Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && grep -n -E 'damage per second|health per second|duration|seconds' Legacy_Venom.md | head -8",
 "description": "Read Acid Venom history and Legacy Venom"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:38:56.997Z

**📎 ToolResult**

```
18:−6 health per second  
21:On the [ Old-gen console version](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [Nintendo 3DS](Legacy%3A3DS_version "Legacy:3DS version")[](Legacy%3A3DS_version "3DS")[ version](Legacy%3A3DS_version "Legacy:3DS version"), Acid Venom is called _Venom_ , and inflicts 6 damage per second to the inflicted target. Enemies immune to [Poison](Poison "Poison") are also immune to Venom. 
77:  *[5–9 seconds]: Master Mode
97:  *[1 minute 30 seconds]: Expert Mode
98:  *[1 minute 52.5 seconds]: Master Mode
203:  *[2–6 seconds]: Expert Mode
204:  *[2.5–7.5 seconds]: Master Mode
214:  *[14–20 seconds]: Expert Mode

```


---

## 🤖 Assistant · 2026-08-12T18:39:01.661Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Acid Venom history: 1.4.0.1: 6→15 DPS; 1.4.1: enemy 15→30, renamed. Legacy Venom: 6 DPS.

Now remaining: On Fire! notes (Oiled), Poisoned notes, Ichor lead, Frostburn lead, Cursed Inferno lead, Frozen durations (already), Silenced (done), Darkness (done: 15 s base), Stinky (done), Daybroken (done: 25 per quarter second = 100 DPS), Heart Lantern etc done.

Let me also check the Warmth potion "see below" list and its 30% damage reduction note, plus Warmth's cold enemy list. And Tipsy duration from Ale = 2 minutes (already).

Also "Heartreach" numbers (done: +15.625 tiles → 18.25 total).

Also "Crate Potion" done. "Fishing Potion" +15 FP done. "Sonar" done.

Also "Inferno" 20 DPS ring done.

Also need: Poisoned notes; Ichor_(debuff) lead; Frostburn lead; Cursed_Inferno lead; On Fire! full notes.

Let me batch.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:39:01.904Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Poisoned.md",
 "limit": 20,
 "offset": 40
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:39:01.909Z

**📎 ToolResult**

```
40	
41	20
42	
43	### Internal name
44	
45	`Poisoned`
46	
47	Poisoned as inflicted by a [Dart Trap](Dart_Trap.md "Dart Trap").
48	
49	**Poisoned** is a [debuff](Debuffs.md "Debuffs") that prevents [health regeneration](Health_regeneration.md "Health regeneration") and causes the afflicted entity to take damage every second for the duration of the debuff. Players are dealt 2 damage per second, whereas enemies are dealt 6 damage per second. 
50	
51	Visually, the debuff causes afflicted entities to gain a green tint, and the player's eyes will squint while they are afflicted. 
52	
53	The debuff can be negated by equipping the [Bezoar](Bezoar.md "Bezoar") or its derivatives, or eating/diving into [Honey](Honey.md "Honey") for its regenerative [buff](Honey_\(buff\) "Honey \(buff\)"). 
54	
55	## Causes
56	
57	### From player
58	
59	From  | Duration  | Chance  | Total damage   

```


---

## 🤖 Assistant · 2026-08-12T18:39:02.223Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Ichor_(debuff).md",
 "limit": 14,
 "offset": 38
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:39:02.231Z

**📎 ToolResult**

```
38	
39	This article is about the debuff. For the crafting material, see [Ichor](Ichor.md "Ichor"). 
40	
41	**Ichor** is a [Hardmode](Hardmode.md "Hardmode") [debuff](Debuffs.md "Debuffs") that lowers the afflicted player's [defense](Defense.md "Defense") by 15, or adds 15 [armor penetration](Armor_penetration.md "Armor penetration") when calculating damage against afflicted enemies. It is inflicted by the ranged attacks of [Ichor Stickers](Ichor_Sticker.md "Ichor Sticker") in the [Underground Crimson](Underground_Crimson.md "Underground Crimson") or by [Tainted Ghouls](Tainted_Ghoul "Tainted Ghoul") found in [Crimson](The_Crimson.md "The Crimson") [Underground Deserts](Underground_Desert.md "Underground Desert"). It can also be inflicted by [weapons](Weapons.md "Weapons") and [ammo](Ammo "Ammo") crafted with [Ichor](Ichor.md "Ichor"). 
42	
43	## Causes
44	
45	### From player
46	
47	From  | Duration  | Chance   
48	---|---|---  
49	[](Golden_Shower.md "Golden Shower") | [Golden Shower](Golden_Shower.md "Golden Shower") | 10 seconds  | 100%   
50	[](Ichor_Bullet.md "Ichor Bullet") | [Ichor Bullet](Ichor_Bullet.md "Ichor Bullet") | 10 seconds  | 100%   
51	[](Ichor_Arrow.md "Ichor Arrow") | [Ichor Arrow](Ichor_Arrow.md "Ichor Arrow") | 10 seconds  | 100%   

```


---

## 🤖 Assistant · 2026-08-12T18:39:06.183Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. Now Frostburn and Cursed Inferno leads, and On Fire! notes (Oiled).
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:39:06.397Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Frostburn.md",
 "limit": 12,
 "offset": 38
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:39:06.401Z

**📎 ToolResult**

```
38	
39	**Frostburn** is a [debuff](Debuff "Debuff") that prevents [health regeneration](Health_regeneration.md "Health regeneration") and causes the afflicted entity to take 8 damage each second for the duration of the debuff. 
40	
41	If the afflicted target is [Oiled](Oiled.md "Oiled"), they will take 25 additional damage per second, totaling 33 damage per second. 
42	
43	## Causes
44	
45	### From player
46	
47	From  | Duration  | Chance  | Total damage   
48	---|---|---|---  
49	[](Wand_of_Frosting.md "Wand of Frosting") | [Wand of Frosting](Wand_of_Frosting.md "Wand of Frosting") | 2–3 seconds  | 50% | 16–24   

```


---

## 🤖 Assistant · 2026-08-12T18:39:06.653Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Cursed_Inferno.md",
 "limit": 12,
 "offset": 38
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:39:06.658Z

**📎 ToolResult**

```
38	
39	`CursedInferno`
40	
41	**Cursed Inferno** is a [Hardmode](Hardmode.md "Hardmode") [debuff](Debuff "Debuff") that prevents [health regeneration](Health_regeneration.md "Health regeneration") and causes the afflicted entity to take damage each second for the duration of the debuff. Players are dealt 12 damage per second, while enemies are dealt 24 damage per second. Additionally, affected enemies also take 10% more knockback _(see[Knockback § Formula](Knockback#Formula "Knockback") for details)_. 
42	
43	If the afflicted target is [Oiled](Oiled.md "Oiled"), they will take 25 additional damage per second, totaling 49 damage per second to enemies or 37 damage per second to players. 
44	
45	## Causes
46	
47	### From player
48	
49	From  | Duration  | Chance  | Total damage   

```


---

## 🤖 Assistant · 2026-08-12T18:39:09.397Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now On Fire! notes section and Warmth list. Let me check On Fire!'s notes about Oiled and durations, plus the remaining causes.

Also need: Darkness lead (15 seconds?), Silenced durations (done: 7 s base; Pixie etc.), Confused durations (5–14 s), Frozen (0.33–2 s).

Let me read On_Fire! notes.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:39:10.787Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && awk '/^## Notes/{flag=1} flag&&/^## /&&!/^## Notes/{exit} flag' On_Fire\\!.md | sed -E 's/\\[\\]\\([^)]*\\)//g; s/\\[([^]]*)\\]\\([^)]*\\)/\\1/g' | head -20; echo \"===WARMTH LIST===\"; awk '/^## Notes|^## Tips/{flag=1} flag&&/^## /&&!/Notes|Tips/{exit} flag' Warmth_Potion.md | sed -E 's/\\[\\]\\([^)]*\\)//g; s/\\[([^]]*)\\]\\([^)]*\\)/\\1/g' | grep -E 'enemies|damage|list|cold' | head -12",
 "description": "Extract On Fire notes and Warmth cold enemy list"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:39:28.865Z

**📎 ToolResult**

```
## Notes

  * Entities afflicted with the debuff emit a small amount of light.

===WARMTH LIST===
  * The Warmth buff does not affect the ice-themed weapons' damage in PvP.
  * Its damage reduction can be combined with similar effects from other items, such as the Endurance Potion. _SeeDamage reduction for details._
  * The Warmth buff does not reduce the damage of the Frozen Zombie, despite it being a cold-themed enemy.
  * The Warmth Potion is highly advantageous during the Frost Legion and Frost Moon events, as many of their enemies are affected by the Warmth buff. Additionally, it will last the full duration of the Frost Moon.
  * The potion is helpful during the fight against Deerclops, even though it does not reduce the damage of its Shadow Hand projectiles.

```


---

## 🤖 Assistant · 2026-08-12T18:39:38.039Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Warmth: +30% damage reduction from cold-themed enemies (lead), doesn't affect PvP, doesn't reduce Frozen Zombie damage.

Now I have nearly everything. Remaining small items:
1. Frozen causes durations (I have from index: 0.33–2 s base; Deerclops 0.33 s; Ice Queen 0.33–1 s etc.)
2. On Fire! full causes (I have the first ~10 rows).
3. Silenced causes: Pixie 7 s @1/10 etc. (have).
4. Confused: Brain of Confusion 1.5 s min @60–100%; Dao of Pow 2–4 s @80%; Bee Keeper 2 s @100%.
5. Debuffs.md notes on DPS stacking (line 165-166, 377) — got.
6. Expert/Master duration multipliers (line 167-187) — got: +100% Expert, +150% Master for listed debuffs. Note: for some debuffs (Electrified, Moon Bite, Oozed, Withered Weapon) duration unchanged in Expert.

Wait — interesting: the index table lists "1.5–28 seconds" for Confused in Expert — that seems like a typo on the wiki (should be 10–28?). I'll report as stated.

7. The task also asked about "Ogre Sped" and "Moon Leech" — neither exists as a page; note that. Also check Legacy pages for these (Legacy_Buffs.md may list Ogre Sped). Let me grep Legacy_Buffs.md for Ogre/Moon Leech/Stunned.

8. Ammo Box station: buff "Infinite" duration (since 1.4.4; previously 10 minutes).

9. Sharpening Station: armor penetration +12 (and history: previously +8? let me check history of Sharpening_Station for value changes).

10. Check Tipsy duration "2 minutes" from Ale — yes.

Let me do a final batch: grep Legacy_Buffs.md for Ogre Sped/Stunned/Moon Leech; grep Sharpening_Station history; grep Crystal_Ball history for Clairvoyance values changes (e.g., mana usage −2%? earlier −5%?). Also check War_Table/Bewitching_Table 1.4.4 duration change (already: 10 min → infinite).
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:39:39.076Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && echo \"===LEGACY BUFFS: Ogre Sped / Stunned / Moon Leech===\"; grep -n -iE 'Ogre Sped|Stunned|Moon Leech|Lovestruck' Legacy_Buffs.md | head -8; echo \"===SHARPEN HISTORY===\"; grep -n -E '\\* \\[Desktop' Sharpening_Station.md | head -8; echo \"===CRYSTALBALL HISTORY===\"; grep -n -A3 'Desktop 1.4.4' Crystal_Ball.md | head -8",
 "description": "Check legacy buffs and station history"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:39:39.110Z

**📎 ToolResult**

```
===LEGACY BUFFS: Ogre Sped / Stunned / Moon Leech===
===SHARPEN HISTORY===
65:  * [Desktop 1.4.5.0](Desktop_1.4.5.0 "Desktop 1.4.5.0"): Buff now only applies to [melee](Melee "Melee") items and projectiles as intended.
67:  * [Desktop 1.4.4](Desktop_1.4.4 "Desktop 1.4.4"): 
71:  * [Desktop 1.4.1](Desktop_1.4.1 "Desktop 1.4.1"): Can now be purchased from the [Merchant](Merchant.md "Merchant") during [Hardmode](Hardmode.md "Hardmode").
73:  * [Desktop 1.4.0.1](Desktop_1.4.0.1 "Desktop 1.4.0.1"): [Armor penetration](Armor_penetration.md "Armor penetration") buff tripled from 4 to 12.
75:  * [Desktop 1.3.0.1](Desktop_1.3.0.1 "Desktop 1.3.0.1"): Introduced.
912:  * [Desktop content](Category%3ADesktop_content "Category:Desktop content")
===CRYSTALBALL HISTORY===
233:  * [Desktop 1.4.4](Desktop_1.4.4 "Desktop 1.4.4"): 
234-    * Stack limit increased from 999 to 9999.
235-    * Buff duration of 10 minutes removed. The buff now lasts until the player dies or leaves the world.
236-    * Now used to make the Blizzard in a Bottle and the Sandstorm in a Bottle.
--
1108:  * Entities patched in Desktop 1.4.4
1109-  * Entities patched in Desktop 1.3.0.1
1110-  * Entities patched in Desktop 1.2.4

```


---

## 🤖 Assistant · 2026-08-12T18:39:41.604Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Sharpened: 1.4.0.1 armor penetration tripled from 4 to 12. Great version change note.

Legacy_Buffs.md has no Ogre Sped/Stunned/Moon Leech. Let me quickly verify Legacy_Buffs.md has a table with debuffs? Let me check whether Legacy:Debuffs exists.

Actually let me check Legacy_Debuffs.md exists.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:39:42.918Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && ls | grep -iE 'Legacy_Debuffs|Legacy_On_Fire|Legacy_Stunned|Legacy_Ogre'; echo \"---\"; grep -rn 'Ogre Sped' Legacy_Buffs.md Legacy_Debuffs.md 2>/dev/null | head -3; echo \"===legacy buffs debuff rows===\"; grep -n -iE 'Sped|Leech|Lovestruck|Stunned' Legacy_Buffs.md | head",
 "description": "Check legacy debuff pages"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:39:42.979Z

**📎 ToolResult**

```
---
===legacy buffs debuff rows===

```


---

## 🤖 Assistant · 2026-08-12T18:39:58.755Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
No legacy debuffs page; no Ogre Sped anywhere in the mirror. Confirmed.

Now let me double-check a few remaining buff pages requested:
- "Fishing/Sonar/Crate potions" — done (Fishing +15 FP/8 min; Sonar 8 min; Crate 1/10→1/4, 4 min).
- "Mining, Builder, Heartreach, Titan, Inferno" — done.
- "Well Fed" — done.
- "Warmth, Gills, Flipper, Featherfall, Gravitation, Obsidian Skin, Invisibility, Hunter, Spelunker, Dangersense, Shine, Night Owl, Battle, Calming, Tipsy" — done.
- "Clairvoyance, Magic Power, Mana Regeneration, Summoning, Bewitched, Sharpened, Ammo Box, Ammo Reservation" — done.
- "Regeneration, Swiftness, Ironskin, Endurance, Wrath, Rage, Lifeforce" — done.

Buff stations: Campfires ✓, Heart Lantern ✓, Star in a Bottle ✓ (discrepancy 5 MP/s page vs 2 MP/s index), Sunflower ✓ (+10% move, ×1.1 multiplier → +21% effective, −17% spawn, −20% max spawns; note Buffs.md index says −17% only), Peace Candle ✓ (−23%, −30%), Water Candle ✓ (+33%, +50%; 1.33×, 1.5×), Bast Statue ✓ (+5 def, no stacking), Garden Gnome ✓ (+0.2 luck), Slice of Cake ✓ (+20% move & mining, 2 min), Torch God / torch luck ✓ (±0.2, Bone +0.1, torch 0/0.1/0.3; negative capped at 0 since 1.4.0.3), War Table ✓ (+1 sentry), Bewitching Table ✓ (+1 minion), Sharpening Station ✓ (+12 armor pen, 1.4.0.1 4→12), Crystal Ball ✓, Ammo Box station ✓ (20% save, infinite since 1.4.4, previously 10 min), Ammo Reservation potion ✓ (20%, 8 min).

One more check: the Debuffs.md "Duration" for Acid Venom is 4 seconds (base). And Poisoned 2–20 s. Bleeding 5–45 s. On Fire 0.5–15 s. Cursed Inferno 2–7 s. Frostburn 6 s. Ichor 7–15 s. Broken Armor 2–10 s. Confused 5–14 s. Darkness 15 s. Silenced 7 s. Chilled 5–45 s. Slow 5–16 s. Weak 60–300 s. Frozen 0.33–2 s. Electrified 4–8 s. Suffocation while buried. Burning while in contact. Mana Sickness 5–10 s. Lovestruck 30 s. Stinky 30 s. Betsy's Curse 5 s (index) / 10 s (page). Daybroken 5 s. Midas 2 s. Obstructed while latched.

Also the Debuffs.md note 377: total DPS list for all debuffs — useful to quote as cross-check (48 Cursed Inferno? wait "48 from Cursed Inferno" — hmm that says 48? Let me re-read: "Total DPS calculation includes 48 from Cursed Inferno, 30 from Hellfire, 30 from Acid Venom, 800 from Daybroken..." Interesting: Cursed Inferno 48? That's 24 × 2? It's a footnote on some page about maximum DPS. I'll quote as-is.

Also, "Moon Leech": the buff applied to Moon Lord is "Moon Leech" — hmm. Actually in-game buff ID 195 is "Withered Armor"... The Moon Lord's tongue debuff on the player is "Moon Bite" (prevents lifesteal) and the buff on Moon Lord is "Moon Leech" (ID 195?). In this wiki, Withered Armor = 195. So "Moon Leech" doesn't exist here. I'll report: no page; the only related page is Moon_Leech_Clot.md (regains 1,000 HP per clot reaching the mouth; clots take 1.5 s to reach the mouth).

Also, note the "Daybroken" infobox says "−25 health per quarter second" (= 100/s).

Also, "Obstructed" — I should note the Brain Suckler's damage? Not needed.

Also, "Campfires.md" also mentions the buff name "Cozy Fire" and area 170×125.

Also the task asked about Buffs.md debuff immunity accessories — but Buffs.md itself doesn't list them; the immunity info is on Debuffs.md? Let me check Debuffs.md for an immunity accessory section (there's "Items to prevent" maybe in the page). Let me grep Debuffs.md for Bezoar/Medicated.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:39:58.788Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && grep -n -iE 'Bezoar|Medicated|Adhesive|Ankh|Immunity accessory|immunity to' Debuffs.md | head -10",
 "description": "Check Debuffs.md immunity accessories"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:39:58.831Z

**📎 ToolResult**

```
50:[](Wet.md "Wet") | [Wet](Wet.md "Wet")**** __(Desktop, Console, Old-gen console and Mobile versions) Internal [Buff ID](Buff_IDs.md "Buff IDs"): 103 | Target drips water. Clears any existing [On Fire!](On_Fire!.md "On Fire!"), [Hellfire](Hellfire.md "Hellfire"), and [Burning](Burning.md "Burning") debuffs and grants an immunity to them. Also grants immunity to [Stinky](Stinky.md "Stinky") debuff on enemies and NPCs.  | _You are dripping water_ | 30 seconds

```


---

## 🤖 Assistant · 2026-08-12T18:40:05.992Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Debuffs.md doesn't list immunity accessories either (each debuff page has "Items to prevent"). So the immunity accessory list comes from the accessory item pages themselves (Bezoar, Adhesive Bandage, Medicated Bandage, Armor Polish, Vitamins, Nazar, Megaphone, Fast Clock, Trifold Map, Blindfold, Hand Warmer, Pocket Mirror, Ankh Charm/Shield), which I've gathered.

Also, Adhesive Bandage drop chance 1/100 (1%) / 1.99% expert; Bezoar 1/100; Medicated Bandage = Adhesive + Bezoar.

Also there are combined accessories: Countercurse Mantra (Nazar+Megaphone: Cursed+Silenced), Armor Bracing (Armor Polish+Vitamins: Broken Armor+Weak), Medicated Bandage (Bleeding+Poisoned), The Plan (Fast Clock+Trifold Map: Slow+Confused), Blindfold→Obsidian Shield? Let me quickly verify Countercurse Mantra, Armor Bracing, The Plan tooltips for completeness — these are relevant to the immunity question.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:40:06.799Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md/ && for f in Countercurse_Mantra Armor_Bracing The_Plan Medicated_Bandage; do printf \"%-20s \" \"$f\"; grep -m1 -E 'Grants immunity' \"$f.md\" | sed -E 's/\\[\\]\\([^)]*\\) ?//g'; echo; done",
 "description": "Check combined immunity accessory tooltips"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:40:19.611Z

**📎 ToolResult**

```
Countercurse_Mantra  [Tooltip](Tooltips.md "Tooltips")|  _Grants immunity to Silenced and Cursed_  

Armor_Bracing        [Tooltip](Tooltips.md "Tooltips")|  _Grants immunity to Weakness and Broken Armor_  

The_Plan             [Tooltip](Tooltips.md "Tooltips")|  _Grants immunity to Slow and Confusion_  

Medicated_Bandage    [Tooltip](Tooltips.md "Tooltips")|  _Grants immunity to Poisoned and Bleeding_

```


---

## 🤖 Assistant · 2026-08-12T18:40:39.760Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I now have everything I need. Let me also quickly verify the "Bewitched" and "Strategist" durations were "10 minutes" pre-1.4.4 (already noted) and get the Ammo Box page's pre-1.4.4 duration (10 minutes, noted at line 71).

One more: the "On Fire!" full causes and "Vampirism seed 50 DPS" note from the index — got it.

Also "Frozen" base duration range from index: 0.33–2 s (base) / 0.67–4 (Expert) / 0.83–5 (Master).

Also "Slow" 0.5× movement; "Chilled" 0.75× movement; Burning 0.5× movement.

Also I should double check "Silenced" base duration 7 s (index) and note Silenced no longer affects summon weapons in 1.4.5.

Also Darkness: base 15 s.

Also Weak: 60–300 s base (index) with sources 1–5 min; Red Potion 1–3 h.

Also Confused base 5–14 s; the expert value "1.5–28" is likely a wiki typo; I'll flag it as written.

Let me also confirm Debuffs.md line 20-22 Poisoned duration 2–20 s and check the On Fire! causes remaining rows quickly to give good sources. I have enough (Lava 7 s, Wand of Sparking, Molotov, Imp Staff, Flare, Molten pickaxe/hamaxe, Flaming Arrow, Volcano).

I think I'm ready to write the report. Format: `Name — wiki value (file:section)`. Compact but with raw numbers. I'll organize by DEBUFFS, BUFFS, STATIONS, INDEX/MECHANICS. Use absolute file paths once and then short names to keep it readable — but instructions say share absolute paths. I'll give the absolute directory once and use file names; better: use full paths in the key header line, then `file.md` references. To be safe I'll write the absolute path for each file at least once. That's heavy but acceptable — I'll list them compactly.

Let me compose the final answer.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:41:41.579Z · glm-x-preview-260804

```
All research complete. Below is the raw wiki-stated data.

Base directory for every path below: `~/Project/GLM/SandboxWorld/terraria-wiki-md/`

---

## DEBUFFS

Two files carry most values: `Debuffs.md` (index tables) and each debuff's own page. Where they disagree, both are quoted.

- **Poisoned** — players **2 DPS**, enemies/NPCs **6 DPS**, no regen; duration **2–20 s** (Expert 2–40 s, Master 2.5–50 s). `Debuffs.md` ("Applicable to players, enemies and NPCs" table) and `Poisoned.md` § lead ("Players are dealt 2 damage per second, whereas enemies are dealt 6 damage per second") + § Statistics ("−6 health per second (on enemies) / −2 (on players)"). Version change: `Poisoned.md` § History — "Desktop 1.4.4: When inflicted on enemies, now does 6 DPS instead of 2."
- **Acid Venom (Venom)** — enemies **30 DPS**, players **15 DPS**; base duration **4 s** (Expert 8 s, Master 10 s). `Acid_Venom.md` § Statistics + lead; durations in `Debuffs.md` table. Sources (`Acid_Venom.md` § Causes): Venom Bullet/Arrow 10 s 100% (300 total dmg), Venom Staff 30 s (900), Spider/Queen Spider Staff 2–4 s (60–120), Flask of Venom 5–9 s (150–270), Pygmy Staff 5–10 s (150–300); Black Recluse/Jungle Creeper 4/8/10 s @1/10. Version changes (`Acid_Venom.md` § History): 1.4.0.1 "Damage per second increased from 6 to 15"; 1.4.1 "doubled from 15 to 30 on the enemy version... renamed to Acid Venom". Old value: `Legacy_Venom.md` — "Venom... inflicts **6 damage per second**".
- **On Fire!** — **−4 HP/s** all entities (index: "increased to **50** DPS against players if Vampirism seed is enabled"); base duration **0.5–15 s** (Expert 1–30 s, Master 1.25–37.5 s); removed by water/honey/Shimmer. `On_Fire!.md` § Statistics ("−4 health per second") + lead; `Debuffs.md` table. Sources (`On_Fire!.md` § Causes): Lava 7 / 14 / 17.5 s @100% (28/56/70 total), Wand of Sparking 1–4 s @50%, Volcano 3 s @50%, Molotov Cocktail 3–6 s @100%, Imp Staff 3–6 s @100%, Flare 5–10 s @100%, Flaming Arrow 3 s @33.3%, Molten Pickaxe 3 s @10%, Molten Hamaxe 3 s @20%, Foxparks 5–10 s (fireball) / 5 s (flamethrower). With Oiled: **29 HP/s total** (4 + 25).
- **Cursed Inferno** — players **12 DPS**, enemies **24 DPS** + **+10% knockback taken**; base duration **2–7 s** (Expert 4–14 s, Master 5–17.5 s). `Cursed_Inferno.md` § Statistics + lead; `Debuffs.md` table. Oiled interaction: **49 DPS to enemies / 37 DPS to players** (`Cursed_Inferno.md` lead). Sources: Cursed Arrow/Bullet/Cursed Flames/Clinger Staff 7 s @100% (168 total), Cursed Dart/Flask of Cursed Flames 3–6 s (72–144), Cursed Flare 10 s (240); Clinger/Spazmatism 2–3 / 4–6 / 5–7.5 s @1/3. Version changes (`Cursed_Inferno.md` § History): 1.4.0.1 "DPS to both players and enemies doubled from **6 to 12**... enemies now take 10% more knockback"; 1.4.1 "Damage per second to enemies doubled from **12 to 24**".
- **Ichor** — **−15 defense** on players / **+15 armor penetration** vs enemies; base duration **7–15 s** (Expert 14–30 s, Master 17.5–37.5 s). `Ichor_(debuff).md` § Statistics + lead; `Debuffs.md` table. Sources: Golden Shower/Ichor Bullet/Ichor Arrow 10 s @100%, Flask of Ichor 10–19 s, Ichor Dart 7–14 s, Bladetongue 5–9 s (sword) / 3–7 s (projectile); Ichor Sticker 15/30/37.5 s @100%, Tainted Ghoul 7/14/17.5 s. Version changes (`Ichor_(debuff).md` § History): 1.4.1 "Defense reduction has been decreased by 25% from **20 to 15**"; 1.4.4 "Mechanic changed from lowering defense to adding armor penetration when applied to enemies."
- **Frostburn** — **8 DPS** all entities; base duration **6 s** (Expert 12 s, Master 15 s). `Frostburn.md` § Statistics + lead; `Debuffs.md` table. Oiled: **33 DPS total** (8 + 25). Sources: Wand of Frosting 2–3 s @50%, Frostburn Arrow 3 s @33.3%, Ice Boomerang 3 s @50%; Ice Elemental 6/12/15 s @1/3. Version changes (`Frostburn.md` § History): 1.2.3 "Damage doubled, but damage is done at half the rate"; 1.4.1 "Players... now lose 8 health per second, up from **6**."
- **Bleeding** — no regen for players; **12 DPS to enemies/NPCs**; base duration **5–45 s** (Expert 6–90 s, Master 7.5–112.5 s). `Bleeding.md` § Statistics ("−12 health per second (on enemies) / No health regeneration (on players)"); `Debuffs.md` table. Sources (`Bleeding.md` § Causes): Spike Slime 10–20 / 20–40 / 25–40 s @100%, Werewolf 45/90/112.5 s @1/8, Vampire 5–7 / 10–14 / 12.5–17.5 s @100%, Angler Fish 45 s @1/8, Rusty Armored Bones 10 s @1/8, Skeletron Head 6–10 s @100%, Duke Fishron 6–20 s @1/3. Version change (`Bleeding.md` § History): 1.4.5.0 "Enemies inflicted with Bleeding now lose **12 health per second**."
- **Darkness** — light brightness lowered; base duration **15 s** (Expert 3–30 s, Master 3.75–37.5 s). `Debuffs.md` table; `Darkness.md` § Statistics. Sources (`Darkness.md` § Causes): Black/Corrupt Slime, Slimeling, Crimslime, Dark Mummy, Blood Mummy 15 / 30 / 37.5 s @1/4; Demon/Voodoo Demon (scythe) 15 s @1/3; Brain of Cthulhu 3–6 s @11/243, Creeper @11/81; Red Potion 1 / 2 / 3 hours @100%.
- **Silenced** — blocks all mana-using items (summon weapons unaffected on Desktop/Console/Mobile); base duration **7 s** (Expert 1.5–14 s, Master 1.87–17.5 s). `Debuffs.md` table; `Silenced.md` lead. Sources (`Silenced.md` § Causes): Pixie 7 / 14 / 17.5 s @1/10, Dark/Blood Mummy 7 s @1/5. Prevented by Megaphone/Countercurse Mantra/Ankh. Version change (`Silenced.md` § History): 1.4.5.0 "No longer affects summon weapons."
- **Slow** — horizontal movement **×0.5**; blocks sprinting/wing speed; base duration **5–16 s** (Expert 0.5–32 s, Master 0.63–40 s). `Debuffs.md` table; `Slow.md` § Statistics ("Horizontal movement speed is halved"). Sources (`Slow.md` § Causes): Pixie/Wraith/Mummy 15 / 30 / 37.5 s @1/8, Rusty Armored Bones 5 s @2/9, Necromancer 5–16 s @100%, Skeletron Hand 0.5–1 s @1/2, Deerclops (roar) 12 / 24 / 30 s @100%, Feral Bite 2.1–3.5 s @1/6 per second.
- **Weak** — **−4 defense, −5.1% melee damage, −5.1% melee speed, −10% movement speed**; base duration **60–300 s** (Expert 11.23–600 s, Master 14.03–750 s). `Debuffs.md` table; `Weak.md` lead. Sources (`Weak.md` § Causes): Corruptor (Vile Spit) 5 / 10 / 12.5 **minutes** @1/20, Floaty Gross 2 / 4 / 5 min @1/25, Scarecrow 1 min @1/10, Red Potion 1 / 2 / 3 hours @100%.
- **Confused** — controls reversed, enemy movement reversed; base duration **5–14 s** (Expert "**1.5**–28 s" as written, Master 1.87–35 s). `Debuffs.md` table; `Confused.md` § Statistics. Sources (`Confused.md` § Causes): Brain of Confusion 1.5 s minimum @60–100%, Dao of Pow 2–4 s @80%, Bee Keeper 2 s @100% (raised from 90% in 1.4.5.0), Nano Bullet / Flask of Nanites 1–3 s @100%, Ale Tosser 2–5 s @5%.
- **Broken Armor** — halves player defense / **+20 armor penetration** vs enemies; base duration **2–10 s** (Expert 4–20 s, Master 5–25 s). `Debuffs.md` table; `Broken_Armor.md` § Statistics. Sources (`Broken_Armor.md` § Causes): Paladin's Hammer 10–20 s @100%; Armored Skeleton **2 / 4 / 5 minutes** @1/6, Blue Armored Bones 10 s @1/2, Red Potion 1 / 2 / 3 hours. Version change (`Broken_Armor.md` § History): 1.3.0.1 "Duration from Armored Skeletons reduced from **5 to 2 minutes**."
- **Suffocation** — **20 DPS**, no regen; lasts while buried under Sand/Silt/Slush-family blocks (or 1 / 2 / 3 hours via Red Potion). `Suffocation.md` § Statistics ("−20 health per second") + § Causes; `Debuffs.md` table.
- **Chilled** — horizontal movement **×0.75**, blocks sprinting/wings; base duration **5–45 s** (Expert 10–90 s, Master 12.5–112.5 s); in Expert, water/Shimmer in Snow biome inflicts it for time in liquid **+5 s** (Expert) / **+6.25 s** (Master) after exiting. `Debuffs.md` table; `Chilled.md` lead + § Causes (Ice Slime 10/20/25 s @1/12; Spiked Ice Slime 20/40/50 s @100%; Ice Golem 45/90/112.5 s @100% beam; Ice Queen 5–25 s @1/2–1/3).
- **Frozen** — fully immobilized; base duration **0.33–2 s** (Expert 0.67–4 s, Master 0.83–5 s). `Debuffs.md` table; `Frozen.md` lead. Sources (`Frozen.md` § Causes): Deerclops 0.33 / 0.67 / 0.83 s @100%, Spiked Ice Slime 1 / 1.5 s, Ice Bat 1 s @1/35, Ice Golem 1 s @1/5, Icy Merman 0.5–2 s @1/10, Ice Queen 0.33–1 s.
- **Stunned** (3DS, Heart Arrow) — "Completely immobilizes the affected target", duration **5–7 seconds**. `Debuffs.md` table row "Stunned" (3DS version, Buff ID m200, tooltip "Paralyzed by love"). No dedicated page in the mirror.
- **Electrified** — **4 DPS stationary / 20 DPS while moving** (lead: "lose 4 health per second... additional 16 health per second, totaling to a loss of 20"); duration **4–8 s** (unchanged in Expert/Master). `Electrified.md` § Statistics + lead; `Debuffs.md` table. Sources: Tesla Turret 5 s @2/3 (20/100 total), Gigazapper 4–8 s @100% (16–32 / 80–160).
- **Moon Leech** — no page/row exists in the mirror (searched `Buffs.md`, `Debuffs.md`, `Legacy_Buffs.md`, whole tree). Closest data: `Moon_Leech_Clot.md` — each clot that reaches the Moon Lord's mouth heals a living part **1,000 HP**; clots take **1.5 seconds** to reach the mouth; 0 defense.
- **Betsy's Curse** — **+40 armor penetration**; duration **5 seconds** per `Debuffs.md` table, but **10 seconds** per `Betsy's_Wrath.md` § lead and § infobox ("Duration| 10 seconds"). Stacks with Ichor for **55 armor penetration total** (`Betsy's_Wrath.md` § Notes). Version change: 1.4.4 "Debuff's mechanic changed from lowering defense to adding armor penetration."
- **Ogre Sped** — does not exist anywhere in the mirror (grep across all 9,163 files = no hits). The current Ogre debuff is **Oozed**: divides horizontal movement speed by **3**, further halved if >5 mph with no vertical momentum; **15 seconds** (same in Expert/Master). `Debuffs.md` table + `Ogre.md` ("inflicts the Oozed debuff... for 15 seconds").
- **Lovestruck** — cosmetic hearts; **+10% happiness** for affected Town NPCs; **30 seconds**. `Debuffs.md` table; `Love_Potion.md` § lead ("within a radius of **9 tiles**... for 30 seconds... increases affected NPCs' happiness by 10%").
- **Stinky** — **−0.25 luck** (added 1.4.5.0), NPCs flee; **30 seconds**. `Debuffs.md` table; `Stinky.md` § History (1.4.5.0). Sources (`Stinky.md` § Causes): Poo 3 s, Poo Boulder 10 s (rolling) / 3 s (standing), Flymeal 5 s, Stink Potion 30 s, Poo Slime 5–10 / 10–20 / 12–25 s. Removed by water.
- **Burning** — **30 DPS** + movement reduced (index: **×0.5** horizontal speed, no sprint/wing speed); lasts while touching Meteorite/Hellstone/Hellstone Brick (Hell Slime: 1–3 s @100%). `Burning.md` § Statistics ("−30 health per second") + lead; `Debuffs.md` table.
- **Mana Sickness** — 5 s per mana item consumed; damage reduction **25%** at 5 s remaining, decaying **−1% per 1/5 second**; stacking consumption adds 5 s each up to **10 s / 50% reduction**; reduction is **multiplicative**. Formula: `Reduction multiplier = 0.25 × (Debuff duration in ticks) / 300`. `Mana_Sickness.md` § lead + § Notes; `Debuffs.md` table ("5–10 seconds"). Version change: 1.3.0.1 stacking introduced.
- **Obstructed** — screen darkened except small area around player; also stops natural regen (like Bleeding); lasts "while being attacked by a Brain Suckler". `Debuffs.md` table; `Brain_Suckler.md` § lead.
- **Midas** — enemies drop **10–49%** more coins on death (`Midas.md` § lead) / **"10-50%"** as written in `Debuffs.md` table; duration **2 s**. Sources: Flask of Gold 2 s @100%, Golden Bullet 2 s @100%.
- **Daybroken** — **100 DPS** ("−25 health per quarter second", `Daybroken.md` § Statistics); stacks to **8** via Daybreak = **800 DPS**; **5 seconds**. `Debuffs.md` table. Sources: Daybreak 5 s @100%, Solar Eruption 5 s @100%.

Stacking note (`Debuffs.md` § Notes): "only the damage numbers from the strongest debuff will appear... but the damage ticks will happen faster to account for all of the inflicted debuffs" (worked example: Acid Venom 15 dmg per 0.5 s; Shadowflame 5 dmg per 0.33 s; both together 15 dmg per 0.33 s = 45 DPS). Footnote 3 lists total combined DPS: 48 Cursed Inferno, 30 Hellfire, 30 Acid Venom, 800 Daybroken, 30 Shadowflame, 20 Blood Butchered, 16 Frostburn, 18 Penetrated, 15 Tentacle Spiked, 12 Bleeding, 100 Hemorrhage, 200 Electric Eel debuff, 8 On Fire!, 6 Poisoned, 200 Celled, 50 Frostbite, 25 Oiled, 44 Dryad's Bane.

Duration scaling (`Debuffs.md` § Notes): durations of Acid Venom, Blackout, Bleeding, Broken Armor, Chilled, Confused, Cursed, Cursed Inferno, Darkness, Frostbite, Frostburn, Frozen, Hellfire, Ichor, On Fire!, Poisoned, Silenced, Slow, Weak are **+100% (doubled) in Expert and +150% in Master** when inflicted on players.

---

## BUFFS (potions)

- **Regeneration** — **+2 HP/s** ("total of 960 health"), **8 minutes**. `Regeneration_Potion.md` § lead + § infobox.
- **Swiftness** — **+25% movement speed** (does not stack with sprinting accessories/mounts), **8 minutes**. `Swiftness_Potion.md` § lead.
- **Ironskin** — **+8 defense**, **8 minutes**. `Ironskin_Potion.md` § tooltip.
- **Endurance** — **+10% damage reduction** (i.e. −10% damage taken), **4 minutes**. `Endurance_Potion.md` § lead + tooltip.
- **Wrath** — **+10% damage**, **4 minutes**. `Wrath_Potion.md` § tooltip.
- **Rage** — **+10% critical strike chance**, **4 minutes**. `Rage_Potion.md` § tooltip.
- **Lifeforce** — **+20% max life**, **8 minutes**. `Lifeforce_Potion.md` § tooltip.
- **Well Fed / Plenty Satisfied / Exquisitely Stuffed** (`Well_Fed.md` § Effects table) —
  - Defense: **+2 / +3 / +4**
  - Damage: **+5% / +7.5% / +10%**
  - Crit chance: **+2% / +3% / +4%**
  - Melee speed: **+5% / +7.5% / +10%**
  - Minion knockback: **+0.5 / +0.75 / +1**
  - Movement speed: **+20% / +30% / +40%**
  - Mining speed: **+5% / +10% / +15%**
  - Durations: Well Fed **10–45 min**, Plenty Satisfied **5–20 min**, Exquisitely Stuffed **4–48 min** (`Buffs.md` Consumables table); `Well_Fed.md` lead says "1 to 48 minutes". Expert Mode: health regeneration only fully effective with one of these active. Rule: "Only one of these buffs may be active at a time... The buff that was most recently applied takes priority." (`Well_Fed.md` lead). Also see `Exquisitely_Stuffed.md`.
- **Clairvoyance** — **+20 max mana, +5% magic damage, +2% magic crit, −2% mana usage**; lasts until death/world exit (10-minute duration removed in 1.4.4). `Crystal_Ball.md` § lead/bullets.
- **Magic Power** — **+20% magic damage**, **4 minutes**. `Magic_Power_Potion.md` § tooltip.
- **Mana Regeneration** — "Increases mana regeneration", **8 minutes**. `Mana_Regeneration_Potion.md` + `Buffs.md` Consumables table.
- **Summoning** — **+1 max minion**, **8 minutes**. `Summoning_Potion.md` § tooltip.
- **Bewitched** — **+1 max minion**; infinite (10-minute duration removed in 1.4.4). `Bewitching_Table.md` § lead + § History.
- **Sharpened** — **+12 armor penetration** for melee weapons and melee projectiles; infinite (was 10 minutes). Version change (`Sharpening_Station.md` § History): 1.4.0.1 "Armor penetration buff tripled from **4 to 12**"; 1.4.5.0 melee-only.
- **Ammo Box (station buff)** — **20% chance not to consume ammo**; duration Infinite (1.4.4 removed a **10-minute** duration). `Ammo_Box.md` § infobox + § History.
- **Ammo Reservation (potion)** — **20% chance to save ammo**, **8 minutes**. `Ammo_Reservation_Potion.md` § tooltip/infobox.
- **Warmth** — **+30% damage reduction from cold-themed enemies**, **15 minutes**. `Warmth_Potion.md` § lead. Notes: no effect in PvP; does not reduce Frozen Zombie damage.
- **Gills** — breathe underwater/no drowning, **4 minutes**. `Gills_Potion.md` § lead.
- **Flipper** — liquids don't impede movement + swim, **8 minutes**. `Buffs.md` Consumables table (`Flipper.md` in this mirror is the enemy/fish page).
- **Featherfall** — fall speed and gravity **reduced to 1/3 (33.33%)** of normal, negates fall damage, **10 minutes**. `Featherfall_Potion.md` § lead.
- **Gravitation** — invert gravity with Up, **3 minutes**. `Gravitation_Potion.md` § lead.
- **Obsidian Skin** — immune to lava and On Fire! (and Burning from blocks), **6 minutes**. `Obsidian_Skin_Potion.md` § lead.
- **Invisibility** — invisible; **3 minutes**; canceled on taking any damage. `Invisibility_Potion.md` § lead.
- **Hunter** — highlights enemies/critters/NPCs, **8 minutes**. `Hunter_Potion.md` § lead.
- **Spelunker** — highlights ores/treasure, **5 minutes**. `Spelunker_Potion.md` § lead.
- **Dangersense** — highlights hazards, **10 minutes**. `Dangersense_Potion.md` § lead.
- **Shine** — player glows, **10 minutes**. `Shine_Potion.md` § lead.
- **Night Owl** — night vision + light-source radius, **10 minutes**. `Night_Owl_Potion.md` § lead.
- **Battle** — spawn rate and max on-screen enemies/critters **+100% (doubled)**, **7 minutes**. `Battle_Potion.md` § lead.
- **Calm (Calming Potion)** — page says **−39% spawn rate, −40% max on-screen enemies**, **12 minutes** (`Calming_Potion.md` § lead), while `Buffs.md` index says "Reduces enemy spawn rate by **17%**". Both are wiki-stated; note the conflict.
- **Tipsy** (Ale/Sake) — **−4 defense, +10% melee damage, +10% melee speed, +2% melee crit, +5 Fishing Power**; **2 minutes**; NPCs get **1.1× defense, 1.1× damage, 0.9× attack interval (~+11% attack speed)**. `Tipsy.md` § Effects bullets + § NPC section; `Debuffs.md` table.
- **Fishing** — **+15 Fishing Power**, **8 minutes**. `Fishing_Potion.md` § lead.
- **Sonar** — reveals catch name, **8 minutes**. `Sonar_Potion.md` § lead.
- **Crate** — crate chance **1/10 (10%) → 1/4 (25%)**, **4 minutes** (`Crate_Potion.md` § lead; `Buffs.md` index phrases it as "Doubles the chance of catching a crate").
- **Mining** — **+25% mining speed**, **10 minutes**. `Mining_Potion.md` § lead.
- **Builder** — **+1 placement range, +25% placement speed** (blocks and walls), **45 minutes**. `Builder_Potion.md` § bullets.
- **Heartreach** — heart pickup range **+15.625 tiles, from 2.625 to 18.25 tiles**, **8 minutes**. `Heartreach_Potion.md` § lead.
- **Titan** — **+50% knockback inflicted**, **8 minutes**. `Titan_Potion.md` § lead.
- **Inferno** — fire ring dealing **20 damage per second**, inflicting **Hellfire for 2 seconds**, **4 minutes**. `Inferno_Potion.md` § lead.

---

## BUFF STATIONS / ENVIRONMENTAL

- **Campfire (Cozy Fire)** — health regen **+10%** and **+0.5 HP/s** constant; 170×125-tile area; stacks with Heart Lantern. `Campfires.md` § lead.
- **Heart Lantern (Heart Lamp)** — **+1 HP/s**; area 170×125 (Desktop/Console/Mobile) / 100×84 (Old-gen & 3DS). `Heart_Lantern.md` § lead.
- **Star in a Bottle** — page: "**5 mana per second**", 170×125 area (`Star_in_a_Bottle.md` § lead) vs. `Buffs.md` index: "**about 2 MP/s**". Conflict noted.
- **Sunflower (Happy!)** — **+10% movement speed** plus a **×1.1 multiplier** to itself and all movement buffs left of it ("effectively... **+21% movement speed**"), **−17% spawn rate**, **−20% max spawns**; 170×125 area; suppressed by ≥5 Tombstones. `Sunflower.md` § Effects. `Buffs.md` index lists only "+10% movement speed, −17% spawns".
- **Peace Candle** — **−23% spawn rate, −30% max on-screen enemies**; 170×125; multiple candles don't stack; Peace + Water Candle cancel each other. `Peace_Candle.md` § lead.
- **Water Candle** — **+33% enemy/critter spawn rate, +50% max on-screen enemies** (index: "1.33×" and "1.5×"); stacks with Battle Potion. `Water_Candle.md` § lead; `Debuffs.md` table.
- **Bast Statue (The Bast Defense)** — **+5 defense**; does not stack with multiple statues. `Bast_Statue.md` § lead + § Notes.
- **Garden Gnome** — **+0.2 luck** within 170×125 tiles; additional gnomes don't stack; no visible buff icon. `Garden_Gnome.md` § lead.
- **Slice of Cake (Sugar Rush)** — **+20% movement speed, +20% mining speed**, **2 minutes**. `Slice_of_Cake.md` § lead.
- **Torch luck** (`Luck.md` § Torches) — Underground only, 81×81-tile area; biome torches (Ice/Desert/Jungle/Hallowed/Corrupt/Crimson/Mushroom) each **+0.2** in their biome; Cursed/Ichor/Coral/Bone torches **+0.2 / +0.1**; plain Torch **0**, **−0.1** in Desert/Corruption/Crimson/Hallow, **−0.3** in Snow; one wrong torch negates torch luck entirely; torch luck floored at 0 since 1.4.0.3 (previously could go negative). Torch Blessing (`Torch_God's_Flavor.md`): auto-converts torches, 8 minutes (`Buffs.md` Consumables).
- **War Table (Strategist)** — **+1 max sentry**; infinite (10-minute duration removed in 1.4.4). `War_Table.md` § lead.
- **Bewitching Table** — **+1 max minion**; infinite (was 10 minutes). `Bewitching_Table.md` § lead + § History.
- **Sharpening Station** — **+12 armor penetration**; infinite (was 10 minutes). `Sharpening_Station.md` § lead.
- **Crystal Ball** — Clairvoyance, see above. `Crystal_Ball.md`.
- **Dryad's Blessing** (bonus context) — **+8 defense, +3 HP/s**. `Buffs.md` Environmental table.

---

## Buffs.md INDEX PAGE — mechanics & immunity

`Buffs.md` contains **no buff duration merge/refresh rule**. Its Notes section holds only a Nintendo Switch touch-screen note. What it *does* state (§ intro):
- Player limited to **44 active buffs and debuffs** (raised from 22 in 1.4.4; from 10 in 1.2.2); leftmost buff is dropped when exceeded.
- Buffs persist across servers/worlds except equipment-granted ones; all buffs cleared on death **except flasks**.
- **Alchemic Enhancement** (Alchemy Flask): "Increases newly received buff potion durations by **20%**" (`Buffs.md` Activated furniture table).

The only merge/precedence statements found elsewhere: `Well_Fed.md` lead ("Only one of these buffs may be active at a time... most recently applied takes priority"); stacking statements in `Campfires.md` (Heart Lantern + Campfire regen stack), `Sunflower.md` § Notes (Happy! stacks with Peace Candle/Asphalt), `Battle_Potion.md` § Notes (stacks across players; stacks with Water Candle), `Bast_Statue.md`, `Peace_Candle.md`, `Garden_Gnome.md` (each non-stacking with itself).

Debuff immunity accessories are **not** listed in `Buffs.md`; they are on the accessory pages (tooltips and leads), all 1/100 (1%) / 1.99% Expert drops unless noted:
- `Bezoar.md` — "Grants immunity to Poisoned" (note: does **not** cover Acid Venom).
- `Adhesive_Bandage.md` — "Grants immunity to Bleeding".
- `Medicated_Bandage.md` — "Grants immunity to Poisoned and Bleeding" (Adhesive Bandage + Bezoar).
- `Armor_Polish.md` — Broken Armor. `Vitamins.md` — Weak. `Armor_Bracing.md` — "Grants immunity to Weakness and Broken Armor".
- `Nazar.md` — Cursed. `Megaphone.md` — Silenced. `Countercurse_Mantra.md` — "Grants immunity to Silenced and Cursed".
- `Fast_Clock.md` — Slow. `Trifold_Map.md` — Confused. `The_Plan.md` — "Grants immunity to Slow and Confusion".
- `Blindfold.md` — Darkness. `Hand_Warmer.md` — "Grants immunity to Chilled and Frozen" (Ankh Shield keeps Chilled immunity but not Frozen, per its Notes). `Pocket_Mirror.md` — Stoned (1/40 / 1/20 drop from Medusa).
- `Ankh_Charm.md` — Bleeding, Broken Armor, Confused, Cursed, Darkness, Poisoned, Silenced, Slow, Stoned, Weak.
- `Ankh_Shield.md` — the Ankh Charm list **plus Burning and Chilled**, plus **+4 defense** and knockback immunity.
```
