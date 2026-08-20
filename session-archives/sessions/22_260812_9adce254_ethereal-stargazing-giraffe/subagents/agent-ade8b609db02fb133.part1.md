# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-13T02:11:55.293Z

```
Read-only extraction task. From the offline Terraria wiki mirror at ~/Project/GLM/SandboxWorld/terraria-wiki-md/, extract the infobox/stat numbers for these boss pages: King_Slime.md, Eye_of_Cthulhu.md, Eater_of_Worlds.md, Brain_of_Cthulhu.md, Skeletron.md, Queen_Bee.md.

For EACH page report exactly what the wiki states (verbatim numbers, noting Classic / Expert / Master columns where present):
1. Max life / HP (all three difficulty values, e.g. "2,800 / 3,640 / 4,641"). For multi-part bosses (Eater of Worlds head/body/tail, Brain + Creepers, Skeletron head/hand) give per-part values as the wiki lists them, and any stated total.
2. Defense (three values).
3. Contact damage (three values) — per part where applicable.
4. KB (knockback) resistance if stated.
5. Number of segments (Eater of Worlds) / number of Creepers (Brain) if stated.
6. Any stated phase-2 threshold (e.g. "transforms below 65% HP" for Eye of Cthulhu) and what changes (defense/damage values in phase 2).
7. Any stated despawn behavior (fleeing at dawn, when player dies, etc.).

The pages are long; use grep/sed to find the infobox section (search for "Max life", "Environment", "Type", "KB", "Defense", "AI") rather than reading whole files. Do NOT create or modify any files. Return a compact per-boss report with exact wiki numbers. If a page has separate tables per difficulty or per boss part, note which value belongs to which part.
```

---

## 📎 Attachment · skill_listing · 2026-08-13T02:11:55.297Z

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

## 🤖 Assistant · 2026-08-13T02:11:58.310Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I need to extract infobox/stat data from six boss pages in the offline Terraria wiki mirror. Let me start by confirming the files exist and finding the infobox sections. I'll use grep to locate relevant lines in parallel.

Let me first list the files to confirm they exist.
```

</details>


---

## 🤖 Assistant · 2026-08-13T02:11:58.311Z · glm-x-preview-260804

```
I'll start by confirming the files exist and locating their infobox sections.
```


---

## 🤖 Assistant · 2026-08-13T02:11:59.258Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls -la ~/Project/GLM/SandboxWorld/terraria-wiki-md/King_Slime.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Eye_of_Cthulhu.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Eater_of_Worlds.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Brain_of_Cthulhu.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Skeletron.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Queen_Bee.md",
 "description": "Check the six boss wiki files exist"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:11:59.304Z

**📎 ToolResult**

```
-rw-r--r--@ 1 user  staff   74557  8月  6 21:56 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Brain_of_Cthulhu.md
-rw-r--r--@ 1 user  staff   92741  8月  6 21:56 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Eater_of_Worlds.md
-rw-r--r--@ 1 user  staff   88482  8月  6 21:56 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Eye_of_Cthulhu.md
-rw-r--r--@ 1 user  staff  109270  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/King_Slime.md
-rw-r--r--@ 1 user  staff  117707  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Queen_Bee.md
-rw-r--r--@ 1 user  staff  130179  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Skeletron.md

```


---

## 🤖 Assistant · 2026-08-13T02:11:59.845Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"Max life\\|Environment\\|^Type\\|KB\\|Defense\\|^AI\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/King_Slime.md | head -50",
 "description": "Locate infobox markers in King_Slime.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:11:59.898Z

**📎 ToolResult**

```
24:Type| [Boss](Boss "Boss")[Slime](Slime "Slime")  
26:[Environment](Environment "Environment")| [ Forest ](Forest.md "Forest")[ Slime Rain ](Slime_Rain.md "Slime Rain")  
30:[Defense](Defense.md "Defense")| 10  
31:[KB](Knockback.md "Knockback") Resist| 100%  
187:In Remix worlds, killing a slime has a 1/200 (0.5%) chance of spawning King Slime, provided the boss has not yet been defeated, is not already alive, and at least one player has more than 140 maximum [health](Health.md "Health") and more than 8 [defense](Defense.md "Defense").[4] Only the death of certain types of slime can trigger this: [Baby Slime](Baby_Slime.md "Baby Slime"), [Black Slime](Black_Slime.md "Black Slime"), [Blue Slime](Blue_Slime.md "Blue Slime"), [Green Slime](Green_Slime.md "Green Slime"), [Jungle Slime](Jungle_Slime.md "Jungle Slime"), [Pinky](Pinky.md "Pinky"), [Purple Slime](Purple_Slime.md "Purple Slime"), [Red Slime](Red_Slime.md "Red Slime"), and [Yellow Slime](Yellow_Slime.md "Yellow Slime"). [Statue](Slime_Statue.md "Slime Statue")-spawned slimes are eligible as well. Slimes killed without the player dealing damage to them will not spawn King Slime. 
1738:  *[Def.]: Defense

```


---

## 🤖 Assistant · 2026-08-13T02:12:01.158Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
King Slime's infobox seems small. Let me look at the infobox region of King_Slime.md (lines ~15-45). Also grep the other files in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-13T02:12:01.406Z · glm-x-preview-260804

```
All six files exist. Now let me locate infobox markers in the remaining files in parallel.
```


---

## 🤖 Assistant · 2026-08-13T02:12:01.999Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"Max life\\|Environment\\|^Type\\|KB Resist\\|Defense.md\\|^AI\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Eye_of_Cthulhu.md | head -50",
 "description": "Locate infobox markers in Eye_of_Cthulhu.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:02.072Z

**📎 ToolResult**

```
24:Type| [Boss](Boss "Boss")  
26:[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
30:[Defense](Defense.md "Defense")| 12  
59:Type| [Boss](Boss "Boss")  
61:[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
67:[Defense](Defense.md "Defense")| 00  
219:  * At least one player in the world has at least 200 maximum [health](Health.md "Health") and more than 10 [defense](Defense.md "Defense").
228:When the Eye of Cthulhu falls below 50% / [65%](Expert_Mode.md "Expert Mode") health (1,400 / [2,366](Expert_Mode.md "Expert Mode") / [3,016](Master_Mode.md "Master Mode")), it spins in place and transforms into its second form (shedding its iris into a mouth), which rams the player more aggressively three times, then hangs in the air for a period. The Eye of Cthulhu no longer spawns Servants of Cthulhu and has no [defense](Defense.md "Defense"), but now has increased contact damage. It also now lets out a roar every time it charges.

```


---

## 🤖 Assistant · 2026-08-13T02:12:02.527Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"Max life\\|Environment\\|^Type\\|KB Resist\\|Defense.md\\|^AI\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Eater_of_Worlds.md | head -60",
 "description": "Locate infobox markers in Eater_of_Worlds.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:02.572Z

**📎 ToolResult**

```
24:Type| [Boss](Boss "Boss")[Burrowing Enemy](Burrowing_Enemy "Burrowing Enemy")  
26:[Environment](Environment "Environment")| [ The Corruption ](The_Corruption.md "The Corruption")[ Underground Corruption ](Underground_Corruption.md "Underground Corruption")  
207:  * The different segments of the Eater of Worlds are not equivalent in stats: the head segment will deal significantly more damage than the body or tail, but also has the least [defense](Defense.md "Defense").

```


---

## 🤖 Assistant · 2026-08-13T02:12:02.998Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"Max life\\|Environment\\|^Type\\|KB Resist\\|Defense.md\\|^AI\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Brain_of_Cthulhu.md | head -60",
 "description": "Locate infobox markers in Brain_of_Cthulhu.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:03.032Z

**📎 ToolResult**

```
24:Type| [Boss](Boss "Boss")  
26:[Environment](Environment "Environment")| [ The Crimson ](The_Crimson.md "The Crimson")[ Underground Crimson ](Underground_Crimson.md "Underground Crimson")  
31:[Defense](Defense.md "Defense")| 14  
59:Type| [Boss](Boss "Boss")  
61:[Environment](Environment "Environment")| [ The Crimson ](The_Crimson.md "The Crimson")  
65:[Defense](Defense.md "Defense")| 14

```


---

## 🤖 Assistant · 2026-08-13T02:12:03.431Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"Max life\\|Environment\\|^Type\\|KB Resist\\|Defense.md\\|^AI\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Skeletron.md | head -60",
 "description": "Locate infobox markers in Skeletron.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:03.470Z

**📎 ToolResult**

```
24:Type| [Boss](Boss "Boss")  
26:[Environment](Environment "Environment")| [ Dungeon entrance ](Dungeon_entrance "Dungeon entrance") \+ [ Night ](Night "Night")  
35:[Defense](Defense.md "Defense")| 10[10+25 per hand alive](Expert_Mode.md "Expert Mode")  
151:Type| Boss Part  
153:[Environment](Environment "Environment")| [ Dungeon entrance ](Dungeon_entrance "Dungeon entrance") \+ [ Night ](Night "Night")  
157:[Defense](Defense.md "Defense")| 14

```


---

## 🤖 Assistant · 2026-08-13T02:12:04.017Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"Max life\\|Environment\\|^Type\\|KB Resist\\|Defense.md\\|^AI\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Queen_Bee.md | head -50",
 "description": "Locate infobox markers in Queen_Bee.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:04.055Z

**📎 ToolResult**

```
24:Type| [Boss](Boss "Boss")  
26:[Environment](Environment "Environment")| [ Bee Hive ](Bee_Hive_\(biome\) "Bee Hive \(biome\)")[ Jungle ](Jungle.md "Jungle")[ Underground Jungle ](Underground_Jungle.md "Underground Jungle")  
31:[Defense](Defense.md "Defense")| 8[8–28](Expert_Mode.md "Expert Mode") (depending on health)[1]  
257:    * Larvae are unaffected by the [Guide to Environmental Preservation](Guide_to_Environmental_Preservation.md "Guide to Environmental Preservation") and its upgrades.

```


---

## 🤖 Assistant · 2026-08-13T02:12:05.748Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read the infobox regions of each file. King Slime lines 20-45, Eye of Cthulhu 20-80, Eater of Worlds 20-100, Brain 20-80, Skeletron 20-165, Queen Bee 20-45.
```

</details>


---

## 🤖 Assistant · 2026-08-13T02:12:05.986Z · glm-x-preview-260804

```
Infoboxes located. Let me read each infobox region in full.
```


---

## 🤖 Assistant · 2026-08-13T02:12:06.228Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/King_Slime.md",
 "offset": 15,
 "limit": 40
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:06.235Z

**📎 ToolResult**

```
15	
16	Classic
17	
18	Expert
19	
20	Master
21	
22	Statistics
23	
24	Type| [Boss](Boss "Boss")[Slime](Slime "Slime")  
25	---|---  
26	[Environment](Environment "Environment")| [ Forest ](Forest.md "Forest")[ Slime Rain ](Slime_Rain.md "Slime Rain")  
27	[AI Type](AI.md "AI")| King Slime AI  
28	Damage| 40/64/96  
29	Max Life| 2000/2800/3570  
30	[Defense](Defense.md "Defense")| 10  
31	[KB](Knockback.md "Knockback") Resist| 100%  
32	Immune to| [](Poisoned.md "Poisoned")[](Hemorrhage.md "Hemorrhage")[](Confused.md "Confused")[](Bleeding.md "Bleeding")[](Shimmering.md "Shimmering")  
33	  
34	Drops
35	
36	[Coins](NPC_drops#Coin_drops "NPC drops")| 1 _GC_(Dropped by Treasure Bag[1])  
37	---|---  
38	  
39	  * **Item(Quantity)****Rate**
40	  * [](Solidifier.md "Solidifier")[Solidifier](Solidifier.md "Solidifier")
41	
42	100%
43	
44	  * [](Slimy_Saddle.md "Slimy Saddle")[Slimy Saddle](Slimy_Saddle.md "Slimy Saddle")
45	
46	25%
47	
48	  * One of the following 3 items will be dropped [2]
49	  * [](Ninja_Hood "Ninja Hood")[Ninja Hood](Ninja_Hood "Ninja Hood")
50	
51	33.33%
52	
53	  * [](Ninja_Shirt "Ninja Shirt")[Ninja Shirt](Ninja_Shirt "Ninja Shirt")
54	

```


---

## 🤖 Assistant · 2026-08-13T02:12:06.535Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Eye_of_Cthulhu.md",
 "offset": 18,
 "limit": 75
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:06.543Z

**📎 ToolResult**

```
18	Expert
19	
20	Master
21	
22	Statistics
23	
24	Type| [Boss](Boss "Boss")  
25	---|---  
26	[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
27	[AI Type](AI.md "AI")| Eye of Cthulhu AI  
28	Damage| 15/30/45  
29	Max Life| 2800/3640/4641  
30	[Defense](Defense.md "Defense")| 12  
31	[KB](Knockback.md "Knockback") Resist| 100%  
32	Immune to| [](Confused.md "Confused")  
33	  
34	Sounds
35	
36	Hurt|   
37	---|---  
38	Killed|   
39	Spawn  
40	 _or_  
41	Entering second phase|   
42	Summon   
43	Servant of Cthulhu|   
44	  
45	  * Internal [NPC ID](NPC_IDs.md "NPC IDs"): **4**
46	
47	Eye of CthulhuSecond Form
48	
49	** _Map icon_**
50	
51	Classic
52	
53	Expert
54	
55	Master
56	
57	Statistics
58	
59	Type| [Boss](Boss "Boss")  
60	---|---  
61	[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
62	[AI Type](AI.md "AI")| Eye of Cthulhu AI  
63	Damage| 23[36](Expert_Mode.md "Expert Mode")  
64	[40](Expert_Mode.md "Expert Mode") (when below 145 health)[54](Master_Mode.md "Master Mode")  
65	[60](Master_Mode.md "Master Mode") (when below 185 health)[1]  
66	Max Life| 1400/2800[2366/3640](Expert_Mode.md "Expert Mode")[3016/4641](Master_Mode.md "Master Mode")  
67	[Defense](Defense.md "Defense")| 00  
68	[−15](Expert_Mode.md "Expert Mode") (when below 436 health)  
69	[−30](Expert_Mode.md "Expert Mode") (when below 145 health)0  
70	[−15](Expert_Mode.md "Expert Mode") (when below 556 health)  
71	[−30](Expert_Mode.md "Expert Mode") (when below 185 health)[1]  
72	[KB](Knockback.md "Knockback") Resist| 100%  
73	Immune to| [](Confused.md "Confused")  
74	  
75	Drops
76	
77	[Coins](NPC_drops#Coin_drops "NPC drops")| 3 _GC_(Dropped by Treasure Bag[2])  
78	---|---  
79	  
80	  * **Item(Quantity)****Rate**
81	  * [](Badger's_Hat.md "Badger's Hat")[Badger's Hat](Badger's_Hat.md "Badger's Hat")(when defeated on the same day  
82	as the [Wall of Flesh](Wall_of_Flesh.md "Wall of Flesh")) [3]
83	
84	100%
85	
86	  * [](Binoculars.md "Binoculars")[Binoculars](Binoculars.md "Binoculars")
87	
88	2.5%
89	
90	  * [](Unholy_Arrow.md "Unholy Arrow")[Unholy Arrow](Unholy_Arrow.md "Unholy Arrow") (20–50)
91	
92	100%

```


---

## 🤖 Assistant · 2026-08-13T02:12:06.810Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Eater_of_Worlds.md",
 "offset": 18,
 "limit": 100
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:06.822Z

**📎 ToolResult**

```
18	Expert
19	
20	Master
21	
22	Statistics
23	
24	Type| [Boss](Boss "Boss")[Burrowing Enemy](Burrowing_Enemy "Burrowing Enemy")  
25	---|---  
26	[Environment](Environment "Environment")| [ The Corruption ](The_Corruption.md "The Corruption")[ Underground Corruption ](Underground_Corruption.md "Underground Corruption")  
27	[AI Type](AI.md "AI")| Worm AI  
28	Max Life| 10050[15120](Expert_Mode.md "Expert Mode")[19296](Master_Mode.md "Master Mode")  
29	[KB](Knockback.md "Knockback") Resist| 100%  
30	Immune to| [](Bleeding.md "Bleeding")[](Confused.md "Confused")[](Hemorrhage.md "Hemorrhage")  
31	  
32	Drops
33	
34	[Coins](NPC_drops#Coin_drops "NPC drops")| 8 _SC_ 20 _SC_  
35	---|---  
36	  
37	  * **Item(Quantity)****Rate**
38	  * [](Shadow_Scale.md "Shadow Scale")[Shadow Scale](Shadow_Scale.md "Shadow Scale") (0–134)
39	
40	100%
41	
42	  * [](Demonite_Ore.md "Demonite Ore")[Demonite Ore](Demonite_Ore.md "Demonite Ore") (20–395)
43	
44	100%
45	
46	  * [](Eater's_Bone.md "Eater's Bone")[Eater's Bone](Eater's_Bone.md "Eater's Bone")
47	
48	5%
49	
50	  * [](Lesser_Healing_Potion.md "Lesser Healing Potion")[Lesser Healing Potion](Lesser_Healing_Potion.md "Lesser Healing Potion") (5–15)
51	
52	100%
53	
54	  * [](Eater_of_Worlds_Mask.md "Eater of Worlds Mask")[Eater of Worlds Mask](Eater_of_Worlds_Mask.md "Eater of Worlds Mask")
55	
56	14.29%
57	
58	  * [](Eater_of_Worlds_Trophy "Eater of Worlds Trophy")[Eater of Worlds Trophy](Eater_of_Worlds_Trophy "Eater of Worlds Trophy")
59	
60	10%
61	
62	  * [](Treasure_Bag_\(Eater_of_Worlds\) "Treasure Bag \(Eater of Worlds\)")[Treasure Bag](Treasure_Bag_\(Eater_of_Worlds\) "Treasure Bag \(Eater of Worlds\)")(Eater of Worlds)
63	
64	[100%](Expert_Mode.md "Expert Mode")
65	
66	  *   * [](Worm_Scarf.md "Worm Scarf")[Worm Scarf](Worm_Scarf.md "Worm Scarf")
67	
68	100%
69	
70	  * [](Eater_of_Worlds_Mask.md "Eater of Worlds Mask")[Eater of Worlds Mask](Eater_of_Worlds_Mask.md "Eater of Worlds Mask")
71	
72	14.29%
73	
74	  * [](Demonite_Ore.md "Demonite Ore")[Demonite Ore](Demonite_Ore.md "Demonite Ore") (80–110[110–135](Master_Mode.md "Master Mode"))
75	
76	100%
77	
78	  * [](Shadow_Scale.md "Shadow Scale")[Shadow Scale](Shadow_Scale.md "Shadow Scale") (20–40[30–50](Master_Mode.md "Master Mode"))
79	
80	100%
81	
82	  * [](Eater's_Bone.md "Eater's Bone")[Eater's Bone](Eater's_Bone.md "Eater's Bone")
83	
84	5%
85	
86	  * [Coins](Coins.md "Coins") ([20 _SC_](NPC_drops#Coin_drops "NPC drops"))
87	
88	100%
89	
90	  *   * [](Writhing_Remains.md "Writhing Remains")[Writhing Remains](Writhing_Remains.md "Writhing Remains")
91	
92	[25%](Master_Mode.md "Master Mode")
93	
94	  * [](Eater_of_Worlds_Relic "Eater of Worlds Relic")[Eater of Worlds Relic](Eater_of_Worlds_Relic "Eater of Worlds Relic")
95	
96	[100%](Master_Mode.md "Master Mode")
97	
98	  * When Dungeon is not present, one of the following combinations will be dropped
99	  * [](Blue_Brick "Blue Brick")[Blue Brick](Blue_Brick "Blue Brick") (500-600)
100	
101	33%
102	
103	  *   * All of the following three items will drop with Blue Brick
104	  * [](Cursed_Blue_Tiled_Wall "Cursed Blue Tiled Wall")[Cursed Blue Tiled Wall](Cursed_Blue_Tiled_Wall "Cursed Blue Tiled Wall") (400-500)
105	
106	  * [](Cursed_Blue_Slab_Wall "Cursed Blue Slab Wall")[Cursed Blue Slab Wall](Cursed_Blue_Slab_Wall "Cursed Blue Slab Wall") (400-500)
107	
108	  * [](Cursed_Blue_Brick_Wall "Cursed Blue Brick Wall")[Cursed Blue Brick Wall](Cursed_Blue_Brick_Wall "Cursed Blue Brick Wall") (400-500)
109	
110	  *   *   * [](Green_Brick "Green Brick")[Green Brick](Green_Brick "Green Brick") (500-600)
111	
112	33%
113	
114	  *   * All of the following three items will drop with Green Brick
115	  * [](Cursed_Green_Tiled_Wall "Cursed Green Tiled Wall")[Cursed Green Tiled Wall](Cursed_Green_Tiled_Wall "Cursed Green Tiled Wall") (400-500)
116	
117	  * [](Cursed_Green_Slab_Wall "Cursed Green Slab Wall")[Cursed Green Slab Wall](Cursed_Green_Slab_Wall "Cursed Green Slab Wall") (400-500)

```


---

## 🤖 Assistant · 2026-08-13T02:12:07.084Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Brain_of_Cthulhu.md",
 "offset": 18,
 "limit": 70
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:07.096Z

**📎 ToolResult**

```
18	Expert
19	
20	Master
21	
22	Statistics
23	
24	Type| [Boss](Boss "Boss")  
25	---|---  
26	[Environment](Environment "Environment")| [ The Crimson ](The_Crimson.md "The Crimson")[ Underground Crimson ](Underground_Crimson.md "Underground Crimson")  
27	[AI Type](AI.md "AI")| Brain of Cthulhu AI  
28	Damage| 30/54/81  
29	Max Life| 1250/2125/2709  
30	3250[5525](Expert_Mode.md "Expert Mode")[7049](Master_Mode.md "Master Mode") (with Creepers)[2][3]  
31	[Defense](Defense.md "Defense")| 14  
32	[KB](Knockback.md "Knockback") Resist| 55%[60%](Expert_Mode.md "Expert Mode")[64%](Master_Mode.md "Master Mode")  
33	Immune to| [](Confused.md "Confused")  
34	  
35	Sounds
36	
37	Hurt|   
38	---|---  
39	Killed|   
40	Spawn  
41	 _or_  
42	Entering second phase|   
43	Teleport|   
44	  
45	  * Internal [NPC ID](NPC_IDs.md "NPC IDs"): **266**
46	
47	Brain of CthulhuSecond Form
48	
49	** _Map icon_**
50	
51	Classic
52	
53	Expert
54	
55	Master
56	
57	Statistics
58	
59	Type| [Boss](Boss "Boss")  
60	---|---  
61	[Environment](Environment "Environment")| [ The Crimson ](The_Crimson.md "The Crimson")  
62	[AI Type](AI.md "AI")| Brain of Cthulhu AI  
63	Damage| 30/54/81  
64	Max Life| 1250/2125/2709  
65	[Defense](Defense.md "Defense")| 14  
66	[KB](Knockback.md "Knockback") Resist| 55%[60%](Expert_Mode.md "Expert Mode")[65%](Master_Mode.md "Master Mode")  
67	Immune to| [](Confused.md "Confused")  
68	  
69	Drops
70	
71	[Coins](NPC_drops#Coin_drops "NPC drops")| 5 _GC_(Dropped by Treasure Bag[1])  
72	---|---  
73	  
74	  * **Item(Quantity)****Rate**
75	  * [](Crimtane_Ore.md "Crimtane Ore")[Crimtane Ore](Crimtane_Ore.md "Crimtane Ore") (40–90)
76	
77	100%
78	
79	  * [](Bone_Rattle.md "Bone Rattle")[Bone Rattle](Bone_Rattle.md "Bone Rattle")
80	
81	5%
82	
83	  * [](Lesser_Healing_Potion.md "Lesser Healing Potion")[Lesser Healing Potion](Lesser_Healing_Potion.md "Lesser Healing Potion") (5–15)
84	
85	100%
86	
87	  * [](Brain_of_Cthulhu_Mask.md "Brain of Cthulhu Mask")[Brain of Cthulhu Mask](Brain_of_Cthulhu_Mask.md "Brain of Cthulhu Mask")

```


---

## 🤖 Assistant · 2026-08-13T02:12:07.358Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Skeletron.md",
 "offset": 18,
 "limit": 155
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:07.381Z

**📎 ToolResult**

```
18	Expert
19	
20	Master
21	
22	Statistics
23	
24	Type| [Boss](Boss "Boss")  
25	---|---  
26	[Environment](Environment "Environment")| [ Dungeon entrance ](Dungeon_entrance "Dungeon entrance") \+ [ Night ](Night "Night")  
27	[AI Type](AI.md "AI")| Head AI  
28	Damage| 32/70/106(contact)  
29	[68](Expert_Mode.md "Expert Mode") (Skull)[1]  
30	[91](Expert_Mode.md "Expert Mode") (while spinning)[1]  
31	[102](Master_Mode.md "Master Mode") (Skull)[1]  
32	[137](Master_Mode.md "Master Mode") (while spinning)[1]  
33	9999 (during [day](Day "Day"))  
34	Max Life| 4400/8800/11220  
35	[Defense](Defense.md "Defense")| 10[10+25 per hand alive](Expert_Mode.md "Expert Mode")  
36	0[0+25 per hand alive](Expert_Mode.md "Expert Mode") (while spinning)  
37	9999 (during day)  
38	[KB](Knockback.md "Knockback") Resist| 100%  
39	Immune to| [](Poisoned.md "Poisoned")[](Confused.md "Confused")[](Bone_Javelin.md "Penetrated")[](Blood_Butcherer.md "Blood Butchered")[](Tentacle_Spike.md "Tentacle Spike")[](Bleeding.md "Bleeding")[](Hemorrhage.md "Hemorrhage")  
40	  
41	Inflicts [ debuff ](Debuffs.md "Debuffs")
42	
43	Inflicts [ debuff ](Debuffs.md "Debuffs")
44	
45	Debuff| [](Bleeding.md "Bleeding")[Bleeding](Bleeding.md "Bleeding")  
46	---|---  
47	Debuff tooltip|  _Cannot regenerate life_  
48	Chance| 100%  
49	Duration| [6–10 seconds](Expert_Mode.md "Expert Mode")[7.5–12.5 seconds](Master_Mode.md "Master Mode")  
50	  
51	Drops
52	
53	[Coins](NPC_drops#Coin_drops "NPC drops")| 5 _GC_(Dropped by Treasure Bag[2])  
54	---|---  
55	  
56	  * **Item(Quantity)****Rate**
57	  * [](Healing_Potion.md "Healing Potion")[Healing Potion](Healing_Potion.md "Healing Potion") (5–15)
58	
59	100%
60	
61	  * One of the following 3 items may be dropped
62	  * [](Skeletron_Mask.md "Skeletron Mask")[Skeletron Mask](Skeletron_Mask.md "Skeletron Mask")
63	
64	14.29%
65	
66	  * [](Skeletron_Hand.md "Skeletron Hand")[Skeletron Hand](Skeletron_Hand.md "Skeletron Hand")
67	
68	12.24%
69	
70	  * [](Book_of_Skulls.md "Book of Skulls")[Book of Skulls](Book_of_Skulls.md "Book of Skulls")
71	
72	10.5%
73	
74	  *   * [](Skeletron_Trophy "Skeletron Trophy")[Skeletron Trophy](Skeletron_Trophy "Skeletron Trophy")
75	
76	10%
77	
78	  * [](Chippy's_Couch.md "Chippy's Couch")[Chippy's Couch](Chippy's_Couch.md "Chippy's Couch")
79	
80	14.29%
81	
82	  * [](Treasure_Bag_\(Skeletron\) "Treasure Bag \(Skeletron\)")[Treasure Bag](Treasure_Bag_\(Skeletron\) "Treasure Bag \(Skeletron\)")(Skeletron)
83	
84	[100%](Expert_Mode.md "Expert Mode")
85	
86	  *   * [](Bone_Glove.md "Bone Glove")[Bone Glove](Bone_Glove.md "Bone Glove")
87	
88	100%
89	
90	  * One of the following three items will be dropped
91	  * [](Skeletron_Mask.md "Skeletron Mask")[Skeletron Mask](Skeletron_Mask.md "Skeletron Mask")
92	
93	33%
94	
95	  * [](Skeletron_Hand.md "Skeletron Hand")[Skeletron Hand](Skeletron_Hand.md "Skeletron Hand")
96	
97	33%
98	
99	  * [](Book_of_Skulls.md "Book of Skulls")[Book of Skulls](Book_of_Skulls.md "Book of Skulls")
100	
101	33%
102	
103	  *   * [Coins](Coins.md "Coins") ([12 _GC_ 50 _SC_](NPC_drops#Coin_drops "NPC drops"))
104	
105	100%
106	
107	  *   * [](Possessed_Skull.md "Possessed Skull")[Possessed Skull](Possessed_Skull.md "Possessed Skull")
108	
109	[25%](Master_Mode.md "Master Mode")
110	
111	  * [](Skeletron_Relic "Skeletron Relic")[Skeletron Relic](Skeletron_Relic "Skeletron Relic")
112	
113	[100%](Master_Mode.md "Master Mode")
114	
115	  * When Hellforge is not present
116	  * [](Hellforge.md "Hellforge")[Hellforge](Hellforge.md "Hellforge")
117	
118	100%
119	
120	  * 
121	
122	Projectile created
123	
124	Projectile created
125	
126	  * Skull
127	
128	Sounds
129	
130	Hurt|   
131	---|---  
132	Killed|   
133	Spawn  
134	 _or_  
135	Entering spinning phase|   
136	  
137	  * Internal [NPC ID](NPC_IDs.md "NPC IDs"): **35**
138	  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **30**
139	  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **270**
140	
141	SkeletronSkeletron Hand
142	
143	Classic
144	
145	Expert
146	
147	Master
148	
149	Statistics
150	
151	Type| Boss Part  
152	---|---  
153	[Environment](Environment "Environment")| [ Dungeon entrance ](Dungeon_entrance "Dungeon entrance") \+ [ Night ](Night "Night")  
154	[AI Type](AI.md "AI")| Skeletron Hand AI  
155	Damage| 20/44/66  
156	Max Life| 600/1560/1989  
157	[Defense](Defense.md "Defense")| 14  
158	[KB](Knockback.md "Knockback") Resist| 100%  
159	Immune to| [](Bleeding.md "Bleeding")[](Confused.md "Confused")[](Poisoned.md "Poisoned")[](Hemorrhage.md "Hemorrhage")  
160	  
161	Inflicts [ debuff ](Debuffs.md "Debuffs")
162	
163	Inflicts [ debuff ](Debuffs.md "Debuffs")
164	
165	Debuff| [](Slow.md "Slow")[Slow](Slow.md "Slow")  
166	---|---  
167	Debuff tooltip|  _Movement speed is reduced_  
168	Chance| 50%  
169	Duration| [1−2 seconds](Expert_Mode.md "Expert Mode")[1.5–2.5 seconds](Master_Mode.md "Master Mode")  
170	  
171	Sounds
172	

```


---

## 🤖 Assistant · 2026-08-13T02:12:07.637Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Queen_Bee.md",
 "offset": 18,
 "limit": 30
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:07.652Z

**📎 ToolResult**

```
18	Expert
19	
20	Master
21	
22	Statistics
23	
24	Type| [Boss](Boss "Boss")  
25	---|---  
26	[Environment](Environment "Environment")| [ Bee Hive ](Bee_Hive_\(biome\) "Bee Hive \(biome\)")[ Jungle ](Jungle.md "Jungle")[ Underground Jungle ](Underground_Jungle.md "Underground Jungle")  
27	[AI Type](AI.md "AI")| Queen Bee AI  
28	Damage| 30/54/81 (contact)  
29	22[44](Expert_Mode.md "Expert Mode")[66](Master_Mode.md "Master Mode") (Queen Bee's Stinger)[1]  
30	Max Life| 3400/4760/6069  
31	[Defense](Defense.md "Defense")| 8[8–28](Expert_Mode.md "Expert Mode") (depending on health)[1]  
32	[KB](Knockback.md "Knockback") Resist| 100%  
33	Immune to| [](Bleeding.md "Bleeding")[](Confused.md "Confused")[](Poisoned.md "Poisoned")[](Hemorrhage.md "Hemorrhage")  
34	  
35	Inflicts [ debuff ](Debuffs.md "Debuffs")
36	
37	Inflicts [ debuff ](Debuffs.md "Debuffs")
38	
39	Inflicts [ debuff ](Debuffs.md "Debuffs")
40	
41	Debuff| [](Poisoned.md "Poisoned")[Poisoned](Poisoned.md "Poisoned")  
42	---|---  
43	Debuff tooltip|  _Slowly losing life_  
44	Chance| 33.33%[100%](Expert_Mode.md "Expert Mode")  
45	Duration| 10 seconds[2–20 seconds](Expert_Mode.md "Expert Mode")[2.5–25 seconds](Master_Mode.md "Master Mode") (Queen Bee's Stinger)  
46	[2–8 seconds](Expert_Mode.md "Expert Mode") (contact)[2.5–10 seconds](Master_Mode.md "Master Mode") (contact)  
47	  

```


---

## 🤖 Assistant · 2026-08-13T02:12:10.220Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have the infobox data for most. Missing pieces:

1. Eater of Worlds — the main infobox doesn't show per-segment stats. There must be separate sections or tables per segment (head/body/tail). Let me search for those in Eater_of_Worlds.md. Also segment count.
2. Phase-2 thresholds and despawn behavior for each boss.

Let me search:
- Eater of Worlds: per-segment stats — grep for "head", "body", "tail", "segments" in the file.
- Phase 2 / despawn: grep "dawn", "sunrise", "flee", "despawn", "morning", "daybreak", "dies" in each file.

Let me run these in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-13T02:12:10.505Z · glm-x-preview-260804

```
Infoboxes captured. Now I need Eater of Worlds' per-segment stats and the phase-2/despawn details for all bosses.
```


---

## 🤖 Assistant · 2026-08-13T02:12:10.966Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"segment\\|Segment\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Eater_of_Worlds.md | head -40",
 "description": "Find segment info in Eater_of_Worlds.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:11.005Z

**📎 ToolResult**

```
144:The **Eater of Worlds** is a [pre-Hardmode](Pre-Hardmode.md "Pre-Hardmode") [Corruption](The_Corruption.md "The Corruption")-themed [worm](Worm_AI.md "Worm AI") [boss](Bosses.md "Bosses"). It is not a single target, but a string of segments with individual health. It has a total of 67 / [72](Expert_Mode.md "Expert Mode") segments.[1] When any inner body segment is destroyed, it splits into multiple smaller worms, each with their own head and tail. Each section of the Eater of Worlds must be killed in order to defeat the entire boss. The Eater of Worlds, like all worms, is immune to [lava](Lava.md "Lava"). 
146:Fighting the Eater of Worlds is the only way to obtain [Shadow Scales](Shadow_Scale.md "Shadow Scale"), and it is one of the only ways to obtain usable quantities of [Demonite Ore](Demonite_Ore.md "Demonite Ore"). Individual segments drop some of these when killed, with a larger amount of them being dropped upon defeating the entire boss.[2]
158:## Segments
205:  * Note that actually _defeating_ the Eater of Worlds is not completely necessary to progress, as a certain amount of segments may drop the needed amount of materials. 
207:  * The different segments of the Eater of Worlds are not equivalent in stats: the head segment will deal significantly more damage than the body or tail, but also has the least [defense](Defense.md "Defense"). 
209:  * Individual segments cannot survive on their own. Killing one segment of a part consisting of two segments will kill both segments and drop their loot.
211:  * The Eater of Worlds spawns in a coiled state and gradually unravels before attacking the player. Attacking it with piercing weapons in this state will damage all of its segments, which can kill it in seconds.
218:  * The Eater of Worlds will randomly shoot [Vile Spit](Vile_Spit.md "Vile Spit") from its head and body segments. The Vile Spit projectiles can be destroyed in a single hit from any attack or projectile. 
219:    * Head segments will shoot more frequently at low health.[10]
220:    * Body segments can only shoot when they are above [surface](Surface.md "Surface") and are not in front of a background wall.[10]
268:  * Like other worm-types, once the Eater's head passes a given point, every body segment must follow. This allows the player to stand next to the body, attacking every segment as it goes by. The player should be wary of the head looping back around.
276:  * Since each segment can drop loot when killed, it can be a good source of [Presents](Presents "Presents") during [Christmas](Christmas.md "Christmas"), and [Goodie Bags](Goodie_Bag.md "Goodie Bag"), [Bloody Machetes](Bloody_Machete.md "Bloody Machete"), and [Bladed Gloves](Bladed_Glove.md "Bladed Glove") during [Halloween](Halloween.md "Halloween").
278:    * It is a good way to farm for a [Corruption Key](Corruption_Key "Corruption Key"), as every segment has a chance of dropping one.
292:  * With five eyes on the body segments and three eyes on the head and tail segments each, the Eater of Worlds has 331 / [356](Expert_Mode.md "Expert Mode") eyes in total.
296:  * Oddly enough, but most likely intentionally, it is not required to actually completely defeat the Eater of Worlds to get progression-locked items such as the [Nightmare Pickaxe](Nightmare_Pickaxe.md "Nightmare Pickaxe") or [Shadow armor](Shadow_armor.md "Shadow armor"), since each separate segment drops [Shadow Scales](Shadow_Scale.md "Shadow Scale"). 
317:    * Restructured how [Demonite Ore](Demonite_Ore.md "Demonite Ore")/[Shadow Scale](Shadow_Scale.md "Shadow Scale") drops are handled in [Expert](Expert "Expert") and [Master](Master "Master"). Overall, the quantity of drops from segment kills has been reduced, while the amount of drops from Treasure Bags has been increased.
329:    * Now has more segments, even more so in Expert Mode.
386:  1. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, methods `GetEaterOfWorldsSegmentsCount()` in `Terraria.NPC.cs` and `AI_006_Worms()` in `Terraria.NPC.cs`. Note that the worm-type segment counts in the code are only for the _body_ segments, and do not include the head or tail; hence 65/70 becomes 67/72 There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
395:  10. ↑ 10.0 10.1 Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, method `AI_006_Worms()` in `Terraria.NPC.cs`. Head segments initially have a [math]\displaystyle{ \frac{1}{90+\frac{\text{Current health}}{\text{Max health}}\times300} }[/math] chance every tick[9] to shoot (1/390 (0.26%) chance at full health, with the chance getting higher as the segment's health decreases). Body segments simply have a 1/900 (0.11%) chance every tick. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.

```


---

## 🤖 Assistant · 2026-08-13T02:12:11.336Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"Head\\|Body\\|Tail\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Eater_of_Worlds.md | head -40",
 "description": "Find head/body/tail references in Eater_of_Worlds.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:11.377Z

**📎 ToolResult**

```
171:13  |  | Eater of Worlds Head | 150/210/268 | 22/48/73 | 2/4 | 
177:14  |  | Eater of Worlds Body | 150/210/268 | 13/21/31 | 4/6 | 
183:15  |  | Eater of Worlds Tail | 150/210/268 | 11/18/26 | 8/10 | 
219:    * Head segments will shoot more frequently at low health.[10]
220:    * Body segments can only shoot when they are above [surface](Surface.md "Surface") and are not in front of a background wall.[10]
353:    * Head health reduced from 80 to 65, damage reduced from 43 to 22.
354:    * Body health reduced from 210 to 150, damage reduced from 18 to 13, defense reduced from 7 to 4.
355:    * Tail health reduced from 300 to 220, damage reduced from 15 to 11, defense reduced from 10 to 8.
360:    * Head health reduced from 140 to 80, damage reduced from 50 to 43.
361:    * Body health reduced from 230 to 210, damage reduced from 25 to 18.
362:    * Tail health reduced from 350 to 300.
366:    * Head health increased from 120 to 140, damage increased from 40 to 50, defense increased from 0 to 2.
367:    * Body health increased from 200 to 230, damage increased from 10 to 25, defense increased from 4 to 7.
368:    * Tail health increased from 300 to 350, damage increased from 10 to 15, defense increased from 8 to 10.
395:  10. ↑ 10.0 10.1 Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, method `AI_006_Worms()` in `Terraria.NPC.cs`. Head segments initially have a [math]\displaystyle{ \frac{1}{90+\frac{\text{Current health}}{\text{Max health}}\times300} }[/math] chance every tick[9] to shoot (1/390 (0.26%) chance at full health, with the chance getting higher as the segment's health decreases). Body segments simply have a 1/900 (0.11%) chance every tick. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
466:  * [Meteor Head](Meteor_Head.md "Meteor Head")
798:  * [Headless Horseman](Headless_Horseman.md "Headless Horseman")

```


---

## 🤖 Assistant · 2026-08-13T02:12:11.840Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"dawn\\|sunrise\\|morning\\|daybreak\\|flee\\|despawn\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Eye_of_Cthulhu.md | head -20",
 "description": "Find despawn behavior in Eye_of_Cthulhu.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:11.885Z

**📎 ToolResult**

```
230:If the Eye of Cthulhu is not defeated by dawn (4:30 AM), if all players die, or if it goes too far off-screen, it will despawn. 
252:    * Additionally, if a player in [Journey Mode](Journey_Mode.md "Journey Mode") rapidly switches between [dawn](Dawn "Dawn") and [dusk](Dusk "Dusk"), preventing the eye from despawning, more naturally spawned eyes can appear.

```


---

## 🤖 Assistant · 2026-08-13T02:12:12.411Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"dawn\\|sunrise\\|morning\\|daybreak\\|flee\\|despawn\\|Creepers\\|creepers\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Brain_of_Cthulhu.md | head -30",
 "description": "Find despawn and creeper info in Brain_of_Cthulhu.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:12.450Z

**📎 ToolResult**

```
30:3250[5525](Expert_Mode.md "Expert Mode")[7049](Master_Mode.md "Master Mode") (with Creepers)[2][3]  
180:The **Brain of Cthulhu** is a [pre-Hardmode](Pre-Hardmode.md "Pre-Hardmode"), [Crimson](The_Crimson.md "The Crimson")-themed [boss](Bosses.md "Bosses"). Fighting the boss and its attendant [Creepers](Creeper.md "Creeper") is the only way to obtain [Tissue Samples](Tissue_Sample.md "Tissue Sample"), and is one of the ways to obtain usable quantities of [Crimtane Ore](Crimtane_Ore.md "Crimtane Ore"). Defeating the Brain of Cthulhu for the first time also allows the [Tavernkeep](Tavernkeep.md "Tavernkeep") [NPC](NPCs.md "NPCs") to spawn as the Unconscious Man, and allows [meteorites](Meteorite_\(biome\) "Meteorite \(biome\)") to land. 
194:The Brain of Cthulhu's battle is composed of two phases. In the first, the Brain is immune to [damage](Damage.md "Damage") and teleports randomly around the player. Twenty [Creepers](Creeper.md "Creeper") spawn along with the Brain and orbit the boss at high speed. Creepers cannot respawn once they are killed, and all twenty Creepers must be defeated before the Brain of Cthulhu enters its second phase, where it becomes vulnerable to attack and can be directly killed. 
198:The Brain of Cthulhu is initially invincible and appears translucent upon being spawned. It teleports around the player, slowly approaching them before teleporting away again in a random direction while its Creeper minions attack the player. While the Brain of Cthulhu is not teleporting, the Creepers travel in irregular circles around the Brain before hurling themselves toward the player and pulling themselves toward the Brain again afterward. The Creepers do not teleport along with the Brain but are instead pulled between the player and the Brain in large, sweeping orbits, forming groups and allowing the player to deal damage to all the Creepers simultaneously. Once all twenty of its Creepers are defeated, the Brain of Cthulhu enters its second phase. 
206:In [Expert Mode](Expert_Mode.md "Expert Mode"), the second phase has three mirror images of the Brain appear around the player, mirroring the Brain's movements and becoming more opaque as the boss loses health. The Creepers also behave much more aggressively and gain increased movement speed. 
208:Furthermore, both the Creepers (in the first phase) and the Brain (in the second phase) inflict a random [debuff](Debuffs.md "Debuffs") upon contact. The probabilities of applying each debuff are listed in the following table; note that the Creepers always inflict a debuff while the Brain only has a 1/3 (33.33%) chance to do so.[4]
213:Brain | Creepers   
245:  * [Creepers](Creeper.md "Creeper") drop [Hearts](Heart.md "Heart") at a higher rate than most [enemies](Enemies.md "Enemies"), at a 1/2 (50%) chance.
246:  * Creepers do not drop [Souls of Night](Souls_of_Night "Souls of Night") or [Biome Keys](Biome_Keys.md "Biome Keys").
247:  * If the player leaves the Crimson, the Brain of Cthulhu will move downwards and despawn. 
248:    * However, if the player returns to the Crimson before the Brain of Cthulhu despawns, the battle will continue as normal.
249:  * Two Brains can be summoned at once by smashing [Crimson Hearts](Crimson_Heart.md "Crimson Heart"). They seem to share their Creepers and go into their second phases simultaneously.
250:  * Note that actually _defeating_ the Brain of Cthulhu is not completely necessary to progress, as the Creepers may drop the needed amount of materials. 
258:    * Spawns with 40 Creepers, twice as many as normal.
259:    * When Creepers are charging at the player, their acceleration is about 2.67 times compared to Expert Mode. Creeper charging frequency is about 1.63 times compared to Expert Mode.
287:  * Creepers have low individual health and are especially susceptible to the [On Fire!](On_Fire!.md "On Fire!") and [Frostburn](Frostburn.md "Frostburn") [debuffs](Debuffs.md "Debuffs"). Weapons that inflict these debuffs can make quick work of them.
288:  * [Grenades](Grenades "Grenades") and other splash damage weapons can kill the Creepers very quickly, as they will bunch up often.
289:  * Since the Brain of Cthulhu is susceptible to knockback, weapons with high knockback such as [The Rotted Fork](The_Rotted_Fork.md "The Rotted Fork") can keep both Creepers and the Brain from closing distance between teleports. It is also possible to use early-game melee weapons such as the [Katana](Katana.md "Katana") or the [Zombie Arm](Zombie_Arm.md "Zombie Arm") as long as they do not have disadvantageous [modifiers](Modifiers.md "Modifiers"). It is preferable to use spears for this fight since they deal more knockback, however, so the [Trident](Trident.md "Trident") or [The Rotted Fork](The_Rotted_Fork.md "The Rotted Fork") is recommended. 
291:  * [Jester's Arrows](Jester's_Arrow.md "Jester's Arrow") or other piercing weapons can be immensely helpful while fighting the first stage, since Creepers often group up in a clustered formation, effectively allowing the player to hit most if not all of the Creepers in one well-aimed shot.
309:  * Unlike the correlation between the [Eater of Worlds](Eater_of_Worlds.md "Eater of Worlds") and [The Destroyer](The_Destroyer.md "The Destroyer"), the Brain of Cthulhu does not have a [Hardmode](Hardmode.md "Hardmode") counterpart, although The Destroyer's [Probes](Probe.md "Probe") are similar in function to its [Creepers](Creeper.md "Creeper"). 
312:  * Because the [Compass](Compass.md "Compass") and [Depth Meter](Depth_Meter.md "Depth Meter") reveal each tile to be 2 feet in length, the Brain of Cthulhu would be about 13′ 9″ (5.01 m) tall and 20′ (7.29 m) wide. The Creepers would be about 3′ 9″ (1.37 m) tall and wide.
313:  * The Brain of Cthulhu has the least health out of all the bosses, with even less than the [Eye of Cthulhu](Eye_of_Cthulhu.md "Eye of Cthulhu") in its second form. However, when adding in the health of the Creepers, it has more health than [King Slime](King_Slime.md "King Slime").
318:  * The list of debuffs inflicted by the Brain and Creepers in Expert Mode just so happens to be exactly the same as the list of debuff immunities granted by the [Ankh Charm](Ankh_Charm.md "Ankh Charm"). The [Ankh Shield](Ankh_Shield.md "Ankh Shield") also gives these immunities, with the addition of [Burning](Burning.md "Burning") and [Chilled](Chilled.md "Chilled"). Of course, it is fairly trivial to defeat the Brain of Cthulhu at the point in the game that the Ankh Charm can be obtained.
338:      * Restructured how Ore/Tissue Sample drops are handled in Expert and Master. Overall, the quantity of drops from Creepers kills has been reduced, while the amount of drops from Treasure Bags has been increased.
385:  3. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.0.5](1.4.0.5.md "1.4.0.5") source code, method `GetBrainOfCthuluCreepersCount()` in `Terraria.NPC.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.

```


---

## 🤖 Assistant · 2026-08-13T02:12:18.162Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Excellent. Now let me get the Eater of Worlds Segments section (around line 158-200) to see the full per-segment table. Also I need:

- Brain Creeper stats (Creeper.md maybe, or within the Brain page). The Brain page shows "Brain | Creepers" at line 213. Let me read lines 155-230 of Eater_of_Worlds.md and 208-245 of Brain_of_Cthulhu.md.
- Despawn behavior for King Slime, Eater of Worlds, Skeletron, Queen Bee.
- Phase 2 for Skeletron (spinning phase / below 50%?), Queen Bee (enrage behavior?), King Slime (teleport + spawning slimes at low health?).

Let me read Eater of Worlds segments section and Brain's creeper table region, and grep despawn in King Slime, Eater of Worlds, Skeletron, Queen Bee.
```

</details>


---

## 🤖 Assistant · 2026-08-13T02:12:18.164Z · glm-x-preview-260804

```
Let me read the Eater of Worlds segment table and Brain's Creeper table, plus search despawn behavior in the remaining bosses.
```


---

## 🤖 Assistant · 2026-08-13T02:12:18.165Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Eater_of_Worlds.md",
 "limit": 55,
 "offset": 155
}
```


---

## 🤖 Assistant · 2026-08-13T02:12:18.168Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Brain_of_Cthulhu.md",
 "limit": 40,
 "offset": 205
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:18.175Z

**📎 ToolResult**

```
205	
206	In [Expert Mode](Expert_Mode.md "Expert Mode"), the second phase has three mirror images of the Brain appear around the player, mirroring the Brain's movements and becoming more opaque as the boss loses health. The Creepers also behave much more aggressively and gain increased movement speed. 
207	
208	Furthermore, both the Creepers (in the first phase) and the Brain (in the second phase) inflict a random [debuff](Debuffs.md "Debuffs") upon contact. The probabilities of applying each debuff are listed in the following table; note that the Creepers always inflict a debuff while the Brain only has a 1/3 (33.33%) chance to do so.[4]
209	
210	Debuff | Duration[4]  
211	(seconds) | Chance   
212	---|---|---  
213	Brain | Creepers   
214	[](Poisoned.md "Poisoned")[Poisoned](Poisoned.md "Poisoned") | [5.23–10.5 sec](Expert_Mode.md "Expert Mode")  
215	[6.53–13.12 sec](Master_Mode.md "Master Mode") | 11/243 (4.53%) | 11/81 (13.58%)  
216	[](Darkness.md "Darkness")[Darkness](Darkness.md "Darkness") | [3–6 sec](Expert_Mode.md "Expert Mode")  
217	[3.75–7.5 sec](Master_Mode.md "Master Mode") | 11/243 (4.53%) | 11/81 (13.58%)  
218	[](Cursed.md "Cursed")[Cursed](Cursed.md "Cursed") | [0.73–1.5 sec](Expert_Mode.md "Expert Mode")  
219	[0.92–1.87 sec](Master_Mode.md "Master Mode") | 2/243 (0.82%) | 2/81 (2.47%)  
220	[](Bleeding.md "Bleeding")[Bleeding](Bleeding.md "Bleeding") | [7.5–15 sec](Expert_Mode.md "Expert Mode")  
221	[9.37–18.75 sec](Master_Mode.md "Master Mode") | 11/243 (4.53%) | 11/81 (13.58%)  
222	[](Confused.md "Confused")[Confused](Confused.md "Confused") | [1.5–3 sec](Expert_Mode.md "Expert Mode")  
223	[1.87–3.75 sec](Master_Mode.md "Master Mode") | 2/243 (0.82%) | 2/81 (2.47%)  
224	[](Slow.md "Slow")[Slow](Slow.md "Slow") | [5.23–10.5 sec](Expert_Mode.md "Expert Mode")  
225	[6.53–13.12 sec](Master_Mode.md "Master Mode") | 11/243 (4.53%) | 11/81 (13.58%)  
226	[](Weak.md "Weak")[Weak](Weak.md "Weak") | [11.23–22.5 sec](Expert_Mode.md "Expert Mode")  
227	[14.03–28.12 sec](Master_Mode.md "Master Mode") | 11/243 (4.53%) | 11/81 (13.58%)  
228	[](Silenced.md "Silenced")[Silenced](Silenced.md "Silenced") | [1.5–3 sec](Expert_Mode.md "Expert Mode")  
229	[1.87–3.75 sec](Master_Mode.md "Master Mode") | 11/243 (4.53%) | 11/81 (13.58%)  
230	[](Broken_Armor.md "Broken Armor")[Broken Armor](Broken_Armor.md "Broken Armor") | [9.73–19.5 sec](Expert_Mode.md "Expert Mode")  
231	[12.17–24.37 sec](Master_Mode.md "Master Mode") | 11/243 (4.53%) | 11/81 (13.58%)  
232	  
233	## Aftermath
234	
235	  * The [Tavernkeep](Tavernkeep.md "Tavernkeep") will begin to spawn as the Unconscious Man.
236	  * [Meteorites](Meteorite_\(biome\) "Meteorite \(biome\)") will now be able to land.
237	  * The [Dryad](Dryad.md "Dryad") will be able to move in if she could not already.
238	  * The [Merchant](Merchant.md "Merchant") will begin selling the [Drum Set](Drum_Set.md "Drum Set") and [Drumstick](Drumstick "Drumstick") if he was not already.
239	  * The [Arms Dealer](Arms_Dealer.md "Arms Dealer") will begin selling [Unholy Arrows](Unholy_Arrow.md "Unholy Arrow") at night if he was not already.
240	  * The [Angler](Angler.md "Angler") will be able to ask for [Angelfish](Angelfish.md "Angelfish") and [Cloudfish](Cloudfish.md "Cloudfish") if he could not already.
241	  * The [Traveling Merchant](Traveling_Merchant.md "Traveling Merchant") will begin selling the [Gray Zapinator](Gray_Zapinator.md "Gray Zapinator") if he was not already.
242	
243	## Notes
244	

```


---

## 👤 User(sidechain) · 2026-08-13T02:12:18.176Z

**📎 ToolResult**

```
155	
156	It can also be summoned manually by using a [Worm Food](Worm_Food.md "Worm Food") in [The Corruption](The_Corruption.md "The Corruption") or [Underground Corruption](Underground_Corruption.md "Underground Corruption"), at any time. 
157	
158	## Segments
159	
160	Classic
161	
162	Expert
163	
164	Master
165	
166	2 values: Pre-Hardmode › Hardmode  
167	3 values: Pre-Hardmode › Hardmode › Post-Plantera
168	
169	[NPC ID](NPC_IDs.md "NPC IDs") | Type  | Health  | Damage  | Defense  | Extra Drops   
170	---|---|---|---|---|---  
171	13  |  | Eater of Worlds Head | 150/210/268 | 22/48/73 | 2/4 | 
172	
173	  * [](Demonite_Ore.md "Demonite Ore")[Demonite Ore](Demonite_Ore.md "Demonite Ore") (2–5[1–3](Expert_Mode.md "Expert Mode")[1–2](Master_Mode.md "Master Mode"))50%50%[33.33%](Master_Mode.md "Master Mode")
174	  * [](Shadow_Scale.md "Shadow Scale")[Shadow Scale](Shadow_Scale.md "Shadow Scale") (1–2)50%[20%](Expert_Mode.md "Expert Mode")[10%](Master_Mode.md "Master Mode")
175	
176	  
177	14  |  | Eater of Worlds Body | 150/210/268 | 13/21/31 | 4/6 | 
178	
179	  * [](Demonite_Ore.md "Demonite Ore")[Demonite Ore](Demonite_Ore.md "Demonite Ore") (2–5[1–3](Expert_Mode.md "Expert Mode")[1–2](Master_Mode.md "Master Mode"))50%50%[33.33%](Master_Mode.md "Master Mode")
180	  * [](Shadow_Scale.md "Shadow Scale")[Shadow Scale](Shadow_Scale.md "Shadow Scale") (1–2)50%[20%](Expert_Mode.md "Expert Mode")[10%](Master_Mode.md "Master Mode")
181	
182	  
183	15  |  | Eater of Worlds Tail | 150/210/268 | 11/18/26 | 8/10 | 
184	
185	  * [](Demonite_Ore.md "Demonite Ore")[Demonite Ore](Demonite_Ore.md "Demonite Ore") (2–5[1–3](Expert_Mode.md "Expert Mode")[1–2](Master_Mode.md "Master Mode"))50%50%[33.33%](Master_Mode.md "Master Mode")
186	  * [](Shadow_Scale.md "Shadow Scale")[Shadow Scale](Shadow_Scale.md "Shadow Scale") (1–2)50%[20%](Expert_Mode.md "Expert Mode")[10%](Master_Mode.md "Master Mode")
187	
188	  
189	  
190	## Aftermath
191	
192	  * The [Tavernkeep](Tavernkeep.md "Tavernkeep") will begin to spawn as the Unconscious Man.
193	  * The [meteorites](Meteorite_\(biome\) "Meteorite \(biome\)") will now be able to land.
194	  * The [Dryad](Dryad.md "Dryad") will be able to move in if she could not already.
195	  * The [Merchant](Merchant.md "Merchant") will begin selling the [Drum Set](Drum_Set.md "Drum Set") and [Drumstick](Drumstick "Drumstick") if he was not already.
196	  * The [Arms Dealer](Arms_Dealer.md "Arms Dealer") will begin selling [Unholy Arrows](Unholy_Arrow.md "Unholy Arrow") at night if he was not already.
197	  * The [Angler](Angler.md "Angler") will be able to ask for [Angelfish](Angelfish.md "Angelfish") and [Cloudfish](Cloudfish.md "Cloudfish") if he could not already.
198	  * The [Traveling Merchant](Traveling_Merchant.md "Traveling Merchant") will be able to sell the [Gray Zapinator](Gray_Zapinator.md "Gray Zapinator") if he could not already.
199	
200	## Notes
201	
202	  * If the player dies or leaves [the Corruption](The_Corruption.md "The Corruption"), the Eater of Worlds will stop following the player and quickly go off-screen until it [despawns](NPC_despawning.md "NPC despawning"). 
203	    * The Eater of Worlds will not despawn while the player is in the [Crimson](Crimson "Crimson") biome.
204	  * Trying to summon the Eater of Worlds with [Worm Food](Worm_Food.md "Worm Food") while another is still alive will not work and the item will not be consumed.
205	  * Note that actually _defeating_ the Eater of Worlds is not completely necessary to progress, as a certain amount of segments may drop the needed amount of materials. 
206	    * However, defeating the Eater of Worlds is the only way to gain access to the [Tavernkeep](Tavernkeep.md "Tavernkeep") and [Meteorites](Meteorite_\(biome\) "Meteorite \(biome\)").
207	  * The different segments of the Eater of Worlds are not equivalent in stats: the head segment will deal significantly more damage than the body or tail, but also has the least [defense](Defense.md "Defense"). 
208	    * The reverse is true for its tail; it has more defense than the body or head, but also deals the least damage.
209	  * Individual segments cannot survive on their own. Killing one segment of a part consisting of two segments will kill both segments and drop their loot.

```


---

## 🤖 Assistant · 2026-08-13T02:12:18.177Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"dawn\\|sunrise\\|morning\\|daybreak\\|flee\\|despawn\\|all players\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/King_Slime.md | head -20",
 "description": "Find despawn behavior in King_Slime.md"
}
```


---

## 🤖 Assistant · 2026-08-13T02:12:18.197Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"dawn\\|sunrise\\|morning\\|daybreak\\|flee\\|despawn\\|all players\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Skeletron.md | head -20",
 "description": "Find despawn behavior in Skeletron.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:18.219Z

**📎 ToolResult**

```
181:If 150 [slimes](Slimes.md "Slimes") are killed by players, [NPCs](NPCs.md "NPCs"), [traps](Traps.md "Traps"), [lava](Lava.md "Lava"), and/or summoned [minions](Minions "Minions") during the Slime Rain event, King Slime spawns. The following slimes will count toward this total as long as they are killed during the event: [Baby Slime](Baby_Slime.md "Baby Slime"), [Black Slime](Black_Slime.md "Black Slime"), [Blue Slime](Blue_Slime.md "Blue Slime"), [Green Slime](Green_Slime.md "Green Slime"), [Jungle Slime](Jungle_Slime.md "Jungle Slime"), [Pinky](Pinky.md "Pinky"), [Purple Slime](Purple_Slime.md "Purple Slime"), [Red Slime](Red_Slime.md "Red Slime"), and [Yellow Slime](Yellow_Slime.md "Yellow Slime"). [Statue](Slime_Statue.md "Slime Statue")-spawned slimes are counted as well. Defeating King Slime ends the event shortly after. If all players die, King Slime despawns, and the event continues for some time before ending on its own (between 9 and 15 in-game hours). If King Slime has already been defeated in a world, it only takes 75 slime kills to spawn him. If King Slime is summoned manually with the Slime Crown and then subsequently killed, while the Slime Rain is active, the event ends in the same way as if the player killed the King Slime that naturally spawns at the end of the event. This can be quite helpful for players in later stages of the game who want to get the Slime Rain event over with as quickly as possible. 
193:If the player dies or gets more than 187.5 tiles away from King Slime, he will teleport to the bottom-right corner of the world and despawn in 0.17 seconds.[5]

```


---

## 👤 User(sidechain) · 2026-08-13T02:12:18.245Z

**📎 ToolResult**

```
192:Summoning Skeletron requires the player to speak to the [Old Man](Old_Man.md "Old Man") at the Dungeon's entrance at [night](Night "Night"). Upon selecting the _" Curse"_ option, he will turn into Skeletron. Skeletron can only be summoned once per night, as the Old Man will not respawn until dawn. 
209:If the player takes too long to kill Skeletron and [dawn](Dawn "Dawn") (4:30 AM) arrives, it will enrage and begin acting exactly as a faster [Dungeon Guardian](Dungeon_Guardian.md "Dungeon Guardian"), permanently performing its spinning attack as well increasing its damage and defense to 9,999, usually killing any players remaining in the vicinity quickly upon contact. Skeletron remains in this form until it dies or despawns, even if players manage to avoid dying until the following dusk. Killing Skeletron in this form still counts as defeating it and it will drop its items normally. 
225:  * Once either of the hands are destroyed or the head's health is reduced to below 75% ([6,600](Expert_Mode.md "Expert Mode") / [8,415](Master_Mode.md "Master Mode")), the head begins to shoot homing skulls at the player that despawn on contact with a solid block. It shoots one skull roughly every 1.33 seconds, and doubles the frequency to one skull roughly every 0.67 seconds once both hands are defeated. It pauses firing during its spin attack.
329:  * The Old Man will respawn at the following dawn if the player fails to defeat Skeletron.
363:    * Moving quickly enough on a [minecart](Minecarts.md "Minecarts") can cause the hands to despawn.
2421:  *[Krásné ráno, co myslíš? Nechtěl jsi něco?]: Lovely morning, wouldn't you say? Was there something you needed?
2472:  *[dawn]: 4:30 AM

```


---

## 🤖 Assistant · 2026-08-13T02:12:18.284Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"dawn\\|sunrise\\|morning\\|daybreak\\|flee\\|despawn\\|all players\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Queen_Bee.md | head -20",
 "description": "Find despawn behavior in Queen_Bee.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:18.488Z

**📎 ToolResult**

```
251:  * Unlike most other bosses, the Queen Bee does not despawn when far away from the player and charges towards the player instead. 
253:    * In multiplayer, if all players fighting the Queen Bee die at the same time and any other players are alive at the time, the Queen Bee pursues the other players regardless of distance and will only swap aggro to a different player on the death of her current target. 
254:      * The only way to properly despawn the Queen Bee outside of killing her is for all players in the world to die at once.
2311:  *[Krásné ráno, co myslíš? Nechtěl jsi něco?]: Lovely morning, wouldn't you say? Was there something you needed?
2362:  *[dawn]: 4:30 AM

```


---

## 🤖 Assistant · 2026-08-13T02:12:18.925Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"dawn\\|sunrise\\|morning\\|daybreak\\|flee\\|despawn\\|all players\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Eater_of_Worlds.md | head -20",
 "description": "Find despawn behavior in Eater_of_Worlds.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:19.007Z

**📎 ToolResult**

```
202:  * If the player dies or leaves [the Corruption](The_Corruption.md "The Corruption"), the Eater of Worlds will stop following the player and quickly go off-screen until it [despawns](NPC_despawning.md "NPC despawning"). 
203:    * The Eater of Worlds will not despawn while the player is in the [Crimson](Crimson "Crimson") biome.
281:  * The Eater of Worlds will start to flee underground if the player leaves the Corruption biome, but will not immediately despawn. Players can utilize this mechanic to keep the Eater of Worlds away from themselves without despawning it by moving in and out of the Corruption, watching for the boss's icon on the [minimap](Minimap.md "Minimap") to make sure it does not leave.
331:  * [Desktop 1.3.5.3](Desktop_1.3.5.3 "Desktop 1.3.5.3"): Fixed despawning at rare situations in [multiplayer](Multiplayer.md "Multiplayer").
349:  * [Desktop 1.1.2](Desktop_1.1.2 "Desktop 1.1.2"): The Eater of Worlds can now spawn when a third Shadow Orb is broken within the Hallow, but will still flee due to not being in the Corruption.
352:    * No longer defeated when it flees.

```


---

## 🤖 Assistant · 2026-08-13T02:12:26.534Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have most data. Remaining:

1. Creeper stats (Brain of Cthulhu's Creepers) — the Brain page infobox gives "(with Creepers)" totals: 3250/5525/7049. Individual Creeper stats might be in Creeper.md. The task says "number of Creepers (Brain) if stated" — the Brain page states 20 Creepers (Expert note says "Spawns with 40 Creepers, twice as many as normal" at line 258 — wait, that's odd. Let me check line 258 context — it might be a "For the raw damage" or a bug note. Actually line 258 says "Spawns with 40 Creepers, twice as many as normal" — hmm, this might be in a "getfixedboi" / Remix / secret world seed section. Let me check the context around 255-260.

2. Phase 2 thresholds:
- Eye of Cthulhu: below 50% / 65% health (1,400 / 2,366 / 3,016). ✓ (line 228)
- King Slime: any phase? King Slime doesn't have a phase 2 but has behavior changes (teleports when low, spawns slimes). Let me check for that.
- Queen Bee: enrage behavior (in surface during day?) — let me grep "enrage" in Queen_Bee.md.
- Skeletron: spins below 50% health? Let me grep "spin" / "below" in Skeletron.md around line 209-225.
- Eater of Worlds: no phase 2.
- Brain: phase 2 after all Creepers killed (not HP threshold). ✓

3. Creeper stats: I should check Creeper.md for Creeper's own stats (HP/defense/damage/KB). The task asks "number of Creepers (Brain) if stated" — the Brain page says 20. But maybe include Creeper stats too since the task says "Brain + Creepers" per-part values. Let me check Creeper.md exists.

Let me run these greps in parallel:
- grep -n "spin\|below\|75%\|50%" Skeletron.md around behavior section
- grep -n "enrage\|angry\|faster" Queen_Bee.md
- King Slime behavior changes: grep "teleport\|low health\|spawns" King_Slime.md
- Brain context lines 252-262
- Creeper.md infobox.
```

</details>


---

## 🤖 Assistant · 2026-08-13T02:12:26.936Z · glm-x-preview-260804

```
Now let me capture phase-2 thresholds for Skeletron/Queen Bee/King Slime, and check the Creeper stats page and the Brain "40 Creepers" note context.
```


---

## 🤖 Assistant · 2026-08-13T02:12:29.445Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"spinning\\|spins\\|50%\\|75%\\|below\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Skeletron.md | head -25",
 "description": "Find spinning phase threshold in Skeletron.md"
}
```


---

## 🤖 Assistant · 2026-08-13T02:12:29.537Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"enrage\\|Enrage\\|angrier\\|faster\\|25%\\|50%\\|below\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Queen_Bee.md | head -25",
 "description": "Find enrage behavior in Queen_Bee.md"
}
```


---

## 🤖 Assistant · 2026-08-13T02:12:29.582Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"teleport\\|low health\\|half\\|50%\\|spawns\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/King_Slime.md | head -25",
 "description": "Find behavior changes in King_Slime.md"
}
```


---

## 🤖 Assistant · 2026-08-13T02:12:29.623Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Brain_of_Cthulhu.md",
 "limit": 14,
 "offset": 252
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:29.664Z

**📎 ToolResult**

```
252	    * In Expert Mode, defeating the actual Brain is the only way to get access to the [Brain of Confusion](Brain_of_Confusion.md "Brain of Confusion"), a powerful accessory that can benefit the player well late into the game.
253	    * This trait of being able to gain the progression-based items of a boss simply by damaging it instead of defeating it is shared with its Corruption counterpart, [Eater of Worlds](Eater_of_Worlds.md "Eater of Worlds").
254	  * Since [Hellstone](Hellstone.md "Hellstone") can be destroyed with [explosives](Explosives_\(class\) "Explosives \(class\)") in Hardmode, and Hardmode ores can be obtained from [fishing](Fishing.md "Fishing"), defeating the Brain of Cthulhu is not necessary to obtain those items.
255	  * In [For the Worthy](For_the_Worthy.md "For the Worthy") and [Zenith](Zenith_\(seed\) "Zenith \(seed\)") special worlds, the Brain of Cthulhu receives the following changes: 
256	    * Has +20% damage (applied before any Expert/Master difficulty bonuses)
257	    * Has +7 defense for a total of 21 defense, making the second phase rather difficult when using most pre-BoC weapons (damage of those weapons is typically lower than 25).
258	    * Spawns with 40 Creepers, twice as many as normal.
259	    * When Creepers are charging at the player, their acceleration is about 2.67 times compared to Expert Mode. Creeper charging frequency is about 1.63 times compared to Expert Mode.
260	    * The Brain of Cthulhu itself moves 3 times as fast in its first phase.
261	    * The Brain of Cthulhu has fully opaque illusions for the entirety of its second phase after taking its first damage, regardless of difficulty.
262	    * [Gravity](Gravity.md "Gravity") is reversed once the Brain of Cthulhu enters its second phase, and cannot be reversed by gravity-reversing items (e.g. [Gravitation Potions](Gravitation_Potion.md "Gravitation Potion") or the [Gravity Globe](Gravity_Globe.md "Gravity Globe")).
263	  * The conditions of whether [Dungeon Bricks](Dungeon_Bricks.md "Dungeon Bricks") and [Dungeon Brick Walls](Dungeon_Brick_Walls.md "Dungeon Brick Walls") (in a set of bricks and all three variations of walls with matching color. The color of both are chosen randomly)[5] can be dropped is checked upon entering the world, or occasionally during gameplay.[6] If no Dungeon Bricks and no Dungeon Brick Walls of any kind were found (i.e. no walls with [ID](Wall_IDs.md "Wall IDs") 7, 8, 9, 94, 95, 96, 97, 98 nor 99 and no tiles with [ID](Tile_IDs.md "Tile IDs") 41, 43, nor 44), Brain of Cthulhu will drop [Dungeon](Dungeon.md "Dungeon") building materials upon its defeat and reset the drop condition (i.e. it cannot drop them again until another check is performed and passed).[7]
264	
265	## Achievements

```


---

## 🤖 Assistant · 2026-08-13T02:12:29.740Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/terraria-wiki-md/Creeper.md 2>/dev/null && grep -n \"Max Life\\|Damage|\\|Defense\\|KB Resist\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Creeper.md | head -10",
 "description": "Check Creeper stats page if present"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:29.858Z

**📎 ToolResult**

```
30:[91](Expert_Mode.md "Expert Mode") (while spinning)[1]  
32:[137](Master_Mode.md "Master Mode") (while spinning)[1]  
36:0[0+25 per hand alive](Expert_Mode.md "Expert Mode") (while spinning)  
135:Entering spinning phase|   
168:Chance| 50%  
196:A special variant of Skeletron can be summoned via [Chippy's Couch](Chippy's_Couch.md "Chippy's Couch"). _SeeRed Hat variant below._
205:  2. The head spins and begins chasing the player, dealing significant damage if touched, but dropping its defense by 10 (to 0 in Classic Mode) for the duration of the attack.
209:If the player takes too long to kill Skeletron and [dawn](Dawn "Dawn") (4:30 AM) arrives, it will enrage and begin acting exactly as a faster [Dungeon Guardian](Dungeon_Guardian.md "Dungeon Guardian"), permanently performing its spinning attack as well increasing its damage and defense to 9,999, usually killing any players remaining in the vicinity quickly upon contact. Skeletron remains in this form until it dies or despawns, even if players manage to avoid dying until the following dusk. Killing Skeletron in this form still counts as defeating it and it will drop its items normally. 
216:    * During the spinning attack, Skeletron's defense is therefore also only reduced to 50 / 25. Only when both hands are defeated, it will be reduced to 0 like in Classic Mode.
217:  * While spinning, the head gets a 30% damage boost, making it deal [91](Expert_Mode.md "Expert Mode") / [137](Master_Mode.md "Master Mode") damage.
219:  * Hand slashes are 50% more frequent and receive a 16% speed increase. 
221:  * The head accelerates and moves faster when not spinning.
225:  * Once either of the hands are destroyed or the head's health is reduced to below 75% ([6,600](Expert_Mode.md "Expert Mode") / [8,415](Master_Mode.md "Master Mode")), the head begins to shoot homing skulls at the player that despawn on contact with a solid block. It shoots one skull roughly every 1.33 seconds, and doubles the frequency to one skull roughly every 0.67 seconds once both hands are defeated. It pauses firing during its spin attack.
226:  * Skeletron moves faster and has better [AI](AI.md "AI") when targeting multiple players. With this, it is able to "stun-lock" the player while spinning, able to almost instantly kill them if they are not able to escape (e.g. by using a [hook](Hooks.md "Hooks")).
241:[118](Expert_Mode.md "Expert Mode") (while spinning)[1]  
242:[179](Master_Mode.md "Master Mode") (while spinning)[1]  
290:  * Time between spinning phase decreased by 1/3 (33.33%).
291:  * Acceleration increased by 35% when not spinning.
292:  * Speed increased by 40% when spinning.
293:  * Can reflect player's [projectiles](Projectiles.md "Projectiles") when spinning if any Skeletron Hand is alive.
294:  * When spinning, it occasionally spawns 1–2 Red Hat variant of [Dark Casters](Dark_Caster.md "Dark Caster"). 
299:One of the following [status messages](Status_messages.md "Status messages") will be displayed when the Red Hat Skeletron begins spinning: 
461:  3. ↑ Note that the player's center needs to be below 0 depth. The player's center is determined by the center of their hitbox, which is 42 pixels high and 20 pixels wide. If we consider the player takes up a 2-tile-wide×3-tile-high area, the player's center will be located at the middle tile in the left column of the 2×3 area when the player is standing exactly at the center of 2 tiles. Since the [Depth Meter](Depth_Meter.md "Depth Meter") measures depth at the level of the player's feet, Dungeon Guardians will only start spawning once the Depth Meter displays "3' Underground" or more.
1254:  *[50%]: Expert Mode
1255:  *[1/2 (50%)]: Expert Mode

```


---

## 👤 User(sidechain) · 2026-08-13T02:12:29.922Z

**📎 ToolResult**

```
192:[25%](Master_Mode.md "Master Mode")
241:When fought outside of the [Underground Jungle](Underground_Jungle.md "Underground Jungle"), the Queen Bee enrages, causing her movements to become more aggressive and firing stingers at a much faster rate. When fought in the surface [Jungle](Jungle.md "Jungle") or a different [Underground](Underground.md "Underground") biome, the Queen Bee still enrages, but this state is less aggressive than if the player were to fight her in any other surface biome. 
252:    * This means if a player teleports, such as by using a [Magic Mirror](Magic_Mirror "Magic Mirror"), the Queen Bee chases them across the map no matter the distance. If the player teleports outside of the Jungle, she will enrage and may kill the player.
331:    * Now enrages when out of the Underground Jungle.
1144:  *[50%]: Master Mode
1145:  *[1/2 (50%)]: Expert Mode
1189:  *[−50%]: Expert Mode
1202:  *[6.25%]: Expert Mode
1250:  *[25%]: Master Mode
1392:  *[ 25%]: Chế độ Master
1444:  *[12.5–50%]: Expert Mode
1445:  *[12.5%–50%]: Expert Mode
1447:  *[0.25%]: Expert Mode
1496:  *[1/4 (25%)]: Expert Mode
1792:  *[5–25%]: Master Mode
1813:40 when below 145 health]: Expert Mode
1815:60 when below 185 health]: Master Mode
1884:  *[12.5–25%]: Master Mode
1969:  *[6.25–25%]: Master Mode
2126:  *[1.25%–5%]: Expert Mode
2167:  *[1.25%]: Expert Mode
2478:  *[6/12 (50%)]: Expert Mode

```


---

## 👤 User(sidechain) · 2026-08-13T02:12:29.924Z

**📎 ToolResult**

```
100:50%
117:50%
121:50%
181:If 150 [slimes](Slimes.md "Slimes") are killed by players, [NPCs](NPCs.md "NPCs"), [traps](Traps.md "Traps"), [lava](Lava.md "Lava"), and/or summoned [minions](Minions "Minions") during the Slime Rain event, King Slime spawns. The following slimes will count toward this total as long as they are killed during the event: [Baby Slime](Baby_Slime.md "Baby Slime"), [Black Slime](Black_Slime.md "Black Slime"), [Blue Slime](Blue_Slime.md "Blue Slime"), [Green Slime](Green_Slime.md "Green Slime"), [Jungle Slime](Jungle_Slime.md "Jungle Slime"), [Pinky](Pinky.md "Pinky"), [Purple Slime](Purple_Slime.md "Purple Slime"), [Red Slime](Red_Slime.md "Red Slime"), and [Yellow Slime](Yellow_Slime.md "Yellow Slime"). [Statue](Slime_Statue.md "Slime Statue")-spawned slimes are counted as well. Defeating King Slime ends the event shortly after. If all players die, King Slime despawns, and the event continues for some time before ending on its own (between 9 and 15 in-game hours). If King Slime has already been defeated in a world, it only takes 75 slime kills to spawn him. If King Slime is summoned manually with the Slime Crown and then subsequently killed, while the Slime Rain is active, the event ends in the same way as if the player killed the King Slime that naturally spawns at the end of the event. This can be quite helpful for players in later stages of the game who want to get the Slime Rain event over with as quickly as possible. 
191:King Slime attempts to deal contact damage to the player by hopping towards them, and additionally summons slimes to aid him in the fight. When unable to reach the player, he may teleport to their location. 
193:If the player dies or gets more than 187.5 tiles away from King Slime, he will teleport to the bottom-right corner of the world and despawn in 0.17 seconds.[5]
220:King Slime can teleport to the player under the following two circumstances: 
225:As soon as either of these conditions is met, a timer of 5 seconds starts ticking down. When it reaches 0, King Slime teleports to the player's location. If it reaches 0 while King Slime is jumping, the teleportation is delayed until he lands on the ground. Afterwards, the timer resets back to 5 seconds. The timer pauses when neither of the two conditions is met, but it is not reset, meaning it continues where it left off once either condition is met again. 
227:In order to teleport to the player, King Slime tries to find a suitable target location with the following steps:[6]
229:  1. If the total distance between King Slime and the player is greater than 125 tiles, he will teleport directly on top of the player, even if they are midair.
230:  2. Otherwise, he tries to find a valid block to teleport on that is 7–10 tiles ([Chebyshev distance](https://en.wikipedia.org/wiki/en:Chebyshev_distance "wikipedia:en:Chebyshev distance")) away from the player's center.[7]
231:     * A block is considered valid for teleporting if it is an [unactuated](Actuator.md "Actuator") solid block (including [platforms](Platforms.md "Platforms"), but not [planter boxes](Planter_boxes.md "Planter boxes")), does not contain [lava](Lava.md "Lava"), and if the tile above it is not occupied by any unactuated, [unsloped](Slope.md "Slope") solid blocks (including platforms and planter boxes). Additionally, King Slime is required to have an unobstructed line of sight to the player after teleporting there.[8]
232:  3. If the previous step fails, then he tries to find a valid block to teleport on that is 2–6 tiles (Chebyshev distance) away from the player's center.
233:  4. If all of the previous steps fail, then he will teleport directly on top of the player, even if they are midair.
235:Once the target location is chosen, King Slime stays still, disappears over the course of 1 second, and then reappears at the target location over the course of 0.5 seconds. His jump attack cycle is reset from the beginning after teleporting.[5]
243:Finally, King Slime additionally always spawns 4–7 Blue Slimes upon his defeat. These slimes will never be replaced by Spiked Slimes in Expert Mode.[9]
247:  * Defeating King Slime for the first time spawns [Nerdy Slime](Nerdy_Slime "Nerdy Slime").
259:  * King Slime can spawn inside of blocks, making him unable to move unless through teleporting.
260:  * It is possible for King Slime to teleport to the player after they died fighting in the outer layers of the world.
303:  * Piercing weapons can not only damage King Slime, but also kill the additional slimes he spawns.
304:  * When King Slime is about to teleport, he shrinks and his map icon will get closer towards the ground. The latter can be used to know when he is about to return if he goes offscreen.
307:  * King Slime himself does not drop any [Gel](Gel.md "Gel"), but the Blue Slimes he spawns do. This makes fighting him a good way to farm Gel, e.g. for [Flamethrower](Flamethrower.md "Flamethrower") ammo or [Asphalt Blocks](Asphalt_Block.md "Asphalt Block").
309:  * When King Slime teleports, he can become stuck inside the blocks around him, preventing his movement for a while.
323:  * When teleporting, King Slime drops his current crown and seemingly generates a new one upon completing the teleport.
347:    * Can now teleport to [platforms](Platforms.md "Platforms").

```


---

## 👤 User(sidechain) · 2026-08-13T02:12:29.928Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/terraria-wiki-md/Creeper.md
21:Damage| 20/36/54  
22:Max Life| 100/170/217  
23:[Defense](Defense.md "Defense")| 10

```


---

## 🤖 Assistant · 2026-08-13T02:12:37.413Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have nearly everything. A few remaining details to verify:

1. Skeletron behavior section — read lines 195-226 to get the behavior description (spinning, hands, etc.) to confirm the phase details.
2. King Slime behavior — any phase change at low health? Line 191-193 covers hopping/teleport. Let me check if there's a "loses his crown" / spawns more slimes at low health. Actually I saw line 243: spawns 4-7 Blue Slimes upon defeat. Also, King Slime spawns Spiked Slimes in Expert Mode. Let me check around lines 237-246.
3. Creeper KB resist: Creeper.md line 23 defense 10; check KB line.
4. Eater of Worlds despawn: got it.
5. Queen Bee: no phase 2 but enrage outside Underground Jungle. Also Queen Bee spawns bees at 50% health? Let me grep for "50% health" or "summons" in Queen_Bee.md.

Let me read Creeper.md infobox fully (lines 15-30), Skeletron behavior (lines 195-226), King Slime behavior (lines 236-246), and grep Queen Bee for "summons\|spawns\|health".
```

</details>


---

## 🤖 Assistant · 2026-08-13T02:12:37.792Z · glm-x-preview-260804

```
Almost complete. Let me verify the Creeper infobox, Skeletron behavior text, King Slime's slime spawning, and Queen Bee's summoning behavior.
```


---

## 🤖 Assistant · 2026-08-13T02:12:38.014Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Creeper.md",
 "limit": 18,
 "offset": 15
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:38.025Z

**📎 ToolResult**

```
15	Statistics
16	
17	Type| [Flying Enemy](Flying_Enemy "Flying Enemy")  
18	---|---  
19	[Environment](Environment "Environment")| [ The Crimson ](The_Crimson.md "The Crimson")  
20	[AI Type](AI.md "AI")| Creeper AI  
21	Damage| 20/36/54  
22	Max Life| 100/170/217  
23	[Defense](Defense.md "Defense")| 10  
24	[KB](Knockback.md "Knockback") Resist| 20%/28%/36%  
25	Immune to| [](Confused.md "Confused")  
26	  
27	Drops
28	
29	  * **Item(Quantity)****Rate**
30	  * [](Tissue_Sample.md "Tissue Sample")[Tissue Sample](Tissue_Sample.md "Tissue Sample") (2–5[1–3](Expert_Mode.md "Expert Mode")[1–2](Master_Mode.md "Master Mode"))
31	
32	66.67%66.67%[50%](Master_Mode.md "Master Mode")

```


---

## 🤖 Assistant · 2026-08-13T02:12:38.272Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Skeletron.md",
 "limit": 20,
 "offset": 200
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:38.299Z

**📎 ToolResult**

```
200	Skeletron is a large floating skull with two independent floating hands. All parts can travel through [blocks](Blocks.md "Blocks"), and will attempt to make contact with the player to inflict damage. Each part can be killed independently, but killing the head is all that is required to defeat Skeletron. 
201	
202	Skeletron alternates between two attack phases: 
203	
204	  1. The head remains above while the hands slash at the player.
205	  2. The head spins and begins chasing the player, dealing significant damage if touched, but dropping its defense by 10 (to 0 in Classic Mode) for the duration of the attack.
206	
207	Skeletron switches between these two phases in a regular cycle during the entire fight, with the first phase lasting for roughly 13.33 seconds and the second phase lasting for roughly 6.67 seconds. It lets out a roar every time it enters the second phase. 
208	
209	If the player takes too long to kill Skeletron and [dawn](Dawn "Dawn") (4:30 AM) arrives, it will enrage and begin acting exactly as a faster [Dungeon Guardian](Dungeon_Guardian.md "Dungeon Guardian"), permanently performing its spinning attack as well increasing its damage and defense to 9,999, usually killing any players remaining in the vicinity quickly upon contact. Skeletron remains in this form until it dies or despawns, even if players manage to avoid dying until the following dusk. Killing Skeletron in this form still counts as defeating it and it will drop its items normally. 
210	
211	### Expert Mode
212	
213	Skeletron has additional properties in [Expert Mode](Expert_Mode.md "Expert Mode"): 
214	
215	  * The defense of its head is increased by 25 for each of its hands, resulting in a total defense of 60, initially. Once one hand is defeated, it drops to 35 and finally to 10 when both hands are defeated. 
216	    * During the spinning attack, Skeletron's defense is therefore also only reduced to 50 / 25. Only when both hands are defeated, it will be reduced to 0 like in Classic Mode.
217	  * While spinning, the head gets a 30% damage boost, making it deal [91](Expert_Mode.md "Expert Mode") / [137](Master_Mode.md "Master Mode") damage.
218	  * Skeletron will inflict [debuffs](Debuffs.md "Debuffs") upon contact with the player: its hands are able to inflict [Slow](Slow.md "Slow") for [1–2](Expert_Mode.md "Expert Mode") / [1.5–2.5](Master_Mode.md "Master Mode") seconds, and the head is able to inflict [Bleeding](Bleeding.md "Bleeding") for [6–10](Expert_Mode.md "Expert Mode") / [7.5–12.5](Master_Mode.md "Master Mode") seconds.
219	  * Hand slashes are 50% more frequent and receive a 16% speed increase. 

```


---

## 🤖 Assistant · 2026-08-13T02:12:38.493Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/King_Slime.md",
 "limit": 14,
 "offset": 236
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:38.522Z

**📎 ToolResult**

```
236	
237	### Spawning slimes
238	
239	King Slime can spawn 1–3 [Blue Slimes](Blue_Slime.md "Blue Slime") from his body upon taking damage, with each of these Blue Slimes having a 1/4 (25%) chance to be replaced by a [Spiked Slime](Spiked_Slime.md "Spiked Slime") in [Expert Mode](Expert_Mode.md "Expert Mode"). At the beginning of the fight, King Slime can spawn slimes upon taking any hit that brings him below 95% health. Afterwards, he needs to lose at least 5% of his maximum health (100 / [140](Expert_Mode.md "Expert Mode") / [178](Master_Mode.md "Master Mode") health) compared to his health at the last time he spawned slimes before he can spawn them again, with this process repeating until he dies.[5] For example, bringing him to exactly 1,899 / [2,659](Expert_Mode.md "Expert Mode") / [3,390](Master_Mode.md "Master Mode") (95%) health causes him to spawn slimes for the first time, after which he will not spawn new slimes until brought to below 1,799 / [2,519](Expert_Mode.md "Expert Mode") / [3,212](Master_Mode.md "Master Mode") (90%) health. 
240	
241	As a result, King Slime has a maximum of 19 opportunities to spawn slimes, meaning 19–57 slimes in total, or 38 slimes on average. This number will be lower if any of King Slime's slime-spawning opportunities is skipped by reducing his health by more than 5% of his maximum health in a single hit. 
242	
243	Finally, King Slime additionally always spawns 4–7 Blue Slimes upon his defeat. These slimes will never be replaced by Spiked Slimes in Expert Mode.[9]
244	
245	## Aftermath
246	
247	  * Defeating King Slime for the first time spawns [Nerdy Slime](Nerdy_Slime "Nerdy Slime").
248	  * The [Angler](Angler.md "Angler") will be able to ask for [Angelfish](Angelfish.md "Angelfish") and [Cloudfish](Cloudfish.md "Cloudfish") if he could not already.
249	  * If [Queen Slime](Queen_Slime.md "Queen Slime") has already been defeated, the [Princess](Princess.md "Princess") will begin selling [Royal Romance](Royal_Romance.md "Royal Romance").

```


---

## 🤖 Assistant · 2026-08-13T02:12:39.103Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"summons\\|spawns bees\\|at 50%\\|below half\\|health falls\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Queen_Bee.md | head -15",
 "description": "Find bee summoning behavior in Queen_Bee.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:39.221Z

**📎 ToolResult**

```
291:    * The [Lightning Aura sentry summons](Lightning_Aura_sentry_summons.md "Lightning Aura sentry summons") and the [Explosive Trap sentry summons](Explosive_Trap_sentry_summons.md "Explosive Trap sentry summons") can easily kill the bees if the player is near them.

```


---

## 🤖 Assistant · 2026-08-13T02:12:43.982Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Queen Bee doesn't seem to summon bees based on the grep. Let me check Queen Bee's behavior section quickly to check for any phase/summon info. Grep "Behavior" heading in Queen_Bee.md, and also grep "Bee$" spawning. Actually, let me grep "spawns.*bees\|attacks" in Queen_Bee.md. Also I should double-check the Eye of Cthulhu line 228 region — I already have it: below 50% / 65% health (1,400 / 2,366 / 3,016).

One more check for Queen Bee behavior — read the Behavior section briefly.
```

</details>


---

## 🤖 Assistant · 2026-08-13T02:12:44.110Z · glm-x-preview-260804

```
One last check on Queen Bee's behavior section.
```


---

## 🤖 Assistant · 2026-08-13T02:12:44.355Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"^## \\|^### \" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Queen_Bee.md | head -20",
 "description": "List section headings in Queen_Bee.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:44.633Z

**📎 ToolResult**

```
225:## Summoning and spawning
231:## Behavior
243:## Aftermath
249:## Notes
263:## Achievements
281:## Tips
297:## Trivia
308:## Gallery
316:## History
360:## References

```


---

## 🤖 Assistant · 2026-08-13T02:12:44.634Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Queen_Bee.md",
 "limit": 18,
 "offset": 228
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:44.715Z

**📎 ToolResult**

```
228	
229	She can also be summoned manually by using an [Abeemination](Abeemination.md "Abeemination") in the [Jungle](Jungle.md "Jungle") or Underground Jungle, at any time. 
230	
231	## Behavior
232	
233	The Queen Bee has three distinct attack patterns: 
234	
235	  * The Queen Bee levels herself horizontally with the player before charging back and forth three times in an attempt to ram the player. Upon being summoned, she will always use this attack first.
236	  * The Queen Bee spawns [Bees](Bee.md "Bee") while hovering (which includes larger ones in [Expert Mode](Expert_Mode.md "Expert Mode")), which pursue and attack the player. During this attack, she may spawn 6, 12, or 18 Bees.
237	  * The Queen Bee rapidly fires large yellow stingers at the player which visibly pulsate to indicate their location, similarly to [Hornets](Hornet.md "Hornet"). The stingers have a 1/3 (33.33%) / [100%](Expert_Mode.md "Expert Mode") chance of inflicting the [Poisoned](Poisoned.md "Poisoned") [debuff](Debuff "Debuff") for 10 / [2–20](Expert_Mode.md "Expert Mode") / [2.5–25](Master_Mode.md "Master Mode") seconds. During this attack, the Queen Bee alternates between hovering above the player and positioning herself to swoop in at the player from above.
238	
239	In [Expert Mode](Expert_Mode.md "Expert Mode"), the speed of these attacks increases as the Queen Bee's health lowers and her charges increase both in speed and number. At low enough health, the Queen Bee can perform up to six charges in a row before switching to a different attack. The Queen Bee's defense also increases up to a maximum of 28 depending on how much of her health has been depleted.[1] Additionally, she will inflict the [Poisoned](Poisoned.md "Poisoned") [debuff](Debuff "Debuff") upon direct contact with the player for [2–8](Expert_Mode.md "Expert Mode") / [2.5–10](Master_Mode.md "Master Mode") seconds. 
240	
241	When fought outside of the [Underground Jungle](Underground_Jungle.md "Underground Jungle"), the Queen Bee enrages, causing her movements to become more aggressive and firing stingers at a much faster rate. When fought in the surface [Jungle](Jungle.md "Jungle") or a different [Underground](Underground.md "Underground") biome, the Queen Bee still enrages, but this state is less aggressive than if the player were to fight her in any other surface biome. 
242	
243	## Aftermath
244	
245	  * The [Witch Doctor](Witch_Doctor.md "Witch Doctor") will be able to move in.

```


---

## 🤖 Assistant · 2026-08-13T02:13:03.659Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I now have everything needed. Let me compile the report.

Summary of extracted data (verbatim from wiki):

**King Slime** (King_Slime.md lines 22-32)
- Damage: 40/64/96
- Max Life: 2000/2800/3570
- Defense: 10 (single value, no difficulty variance)
- KB Resist: 100%
- No phase 2. Spawns slimes: 1-3 Blue Slimes upon taking damage; first spawn below 95% health; thereafter needs to lose ≥5% max HP (100/140/178) since last spawn; max 19 opportunities (19-57 slimes, 38 avg). On defeat always spawns 4-7 Blue Slimes.
- Despawn: if player dies or gets more than 187.5 tiles away → teleports to bottom-right corner of world and despawns in 0.17 seconds. Also: if all players die, King Slime despawns (Slime Rain continues).

**Eye of Cthulhu** (Eye_of_Cthulhu.md lines 22-32)
- Damage: 15/30/45 (phase 1 contact)
- Max Life: 2800/3640/4641
- Defense: 12
- KB Resist: 100%
- Second form infobox (lines 57-72):
  - Damage: 23 [36 Expert] [54 Master]; 40 (Expert, when below 145 health) / 60 (Master, when below 185 health)
  - Max Life: 1400/2800 [2366/3640 Expert] [3016/4641 Master]
  - Defense: 0 0 [−15 Expert when below 436 health] [−30 Expert when below 145 health]; 0 [−15 Master when below 556 health] [−30 Master when below 185 health]
  - KB Resist: 100%
- Phase 2 threshold: below 50% / 65% health (1,400 / 2,366 / 3,016) — spins in place, transforms into second form, rams 3 times, no Servants of Cthulhu, no defense, increased contact damage.
- Despawn: if not defeated by dawn (4:30 AM), if all players die, or if it goes too far off-screen → despawns.

**Eater of Worlds** (Eater_of_Worlds.md)
- Main infobox (lines 22-30): Max Life: 10050 [15120 Expert] [19296 Master]; KB Resist 100%. No Damage/Defense in main infobox (it's per-segment). No Defense line at all in the main infobox.
- Segments section (lines 158-186): table with columns NPC ID | Type | Health | Damage | Defense:
  - Head (ID 13): Health 150/210/268, Damage 22/48/73, Defense 2/4
  - Body (ID 14): Health 150/210/268, Damage 13/21/31, Defense 4/6
  - Tail (ID 15): Health 150/210/268, Damage 11/18/26, Defense 8/10
  - Note above the table: "2 values: Pre-Hardmode › Hardmode / 3 values: Pre-Hardmode › Hardmode › Post-Plantera" — so the slash values are difficulty? Wait, this header says Classic/Expert/Master (lines 160-164), then the "2 values / 3 values" note refers to defense scaling in progression (pre-hardmode/hardmode/post-Plantera). So Health 150/210/268 = Classic/Expert/Master. Damage 22/48/73 = Classic/Expert/Master. Defense 2/4 = Pre-Hardmode/Hardmode (2 values). Hmm, that's how the wiki formats it. I should note this.
- Total segments: 67 / 72 (Expert)
- Splitting: when any inner body segment destroyed, splits into multiple smaller worms.
- Despawn: if player dies or leaves the Corruption, stops following and goes off-screen until despawns; will not despawn while the player is in the Crimson biome. Also flees underground if player leaves Corruption but not immediately despawn.
- No phase 2.

**Brain of Cthulhu** (Brain_of_Cthulhu.md)
- First form infobox (lines 22-33): Damage 30/54/81; Max Life 1250/2125/2709, and "3250 [5525 Expert] [7049 Master] (with Creepers)"; Defense 14; KB Resist 55% [60% Expert] [64% Master]
- Second form infobox (lines 57-67): Damage 30/54/81; Max Life 1250/2125/2709; Defense 14; KB Resist 55% [60% Expert] [65% Master] (note: 65% Master here vs 64% in first form — I must report verbatim)
- Creeper stats (Creeper.md lines 20-24): Damage 20/36/54; Max Life 100/170/217; Defense 10; KB Resist 20%/28%/36%
- Number of Creepers: Twenty (20) spawn; all 20 must be defeated before second phase.
- Phase 2: not an HP threshold — triggered when all 20 Creepers defeated; Brain becomes vulnerable/attackable. Expert: 3 mirror images; Creepers more aggressive. In Expert/Master both Creepers (phase 1) and Brain (phase 2) inflict random debuffs.
- Despawn: if the player leaves the Crimson, Brain moves downwards and despawns (battle resumes if player returns before despawn).
- Trivia: "least health out of all bosses... when adding in the health of the Creepers, it has more health than King Slime."

**Skeletron** (Skeletron.md)
- Head infobox (lines 22-39): Damage 32/70/106 (contact); 68 (Expert, Skull projectile); 91 (Expert, while spinning); 102 (Master, Skull); 137 (Master, while spinning); 9999 (during day). Max Life 4400/8800/11220. Defense 10 [10+25 per hand alive Expert]; 0 [0+25 per hand alive Expert] (while spinning); 9999 (during day). KB Resist 100%.
- Hand infobox (lines 149-158): Type Boss Part; Damage 20/44/66; Max Life 600/1560/1989; Defense 14; KB Resist 100%.
- Two attack phases cycle: head above + hands slash (~13.33 s), then head spins chasing (~6.67 s); spinning drops defense by 10 (to 0 in Classic).
- Expert Mode: head defense +25 per hand alive → total 60 initially, 35 after one hand, 10 after both. During spinning: 50/25, then 0 when both hands defeated. Spinning damage +30% → 91 (Expert) / 137 (Master).
- Skull firing threshold: once either hand destroyed OR head below 75% health (6,600 / 8,415) → shoots homing skulls ~every 1.33 s; doubles to ~0.67 s once both hands defeated.
- Despawn/enrage: at dawn (4:30 AM) enrage — acts as faster Dungeon Guardian, permanently spinning, damage and defense 9,999; remains until it dies or despawns, even past following dusk.
- Total HP: not stated as a combined total in the infobox; head 4400/8800/11220 + 2 hands 600/1560/1989 each. I'll note per-part.

**Queen Bee** (Queen_Bee.md lines 22-32)
- Damage: 30/54/81 (contact); 22 [44 Expert] [66 Master] (Queen Bee's Stinger)
- Max Life: 3400/4760/6069
- Defense: 8 [8–28 Expert] (depending on health)
- KB Resist: 100%
- No phase 2 per se; attack speed increases as health lowers (Expert), up to 6 charges at low health; defense increases up to max 28 depending on health depleted (Expert).
- Enrage when fought outside Underground Jungle (less aggressive in surface Jungle or different Underground biome).
- Despawn: unlike most bosses, does NOT despawn when far away — charges toward player instead; only despawns if all players in world die at once.

Now write the compact per-boss report. Include file paths (absolute). Note the Eater of Worlds defense 2-value note and the trivia total. Report verbatim numbers.
```

</details>


---

## 🤖 Assistant · 2026-08-13T02:13:28.081Z · glm-x-preview-260804

```
All data extracted. Here is the per-boss report with verbatim wiki numbers.

---

## 1. King Slime — `~/Project/GLM/SandboxWorld/terraria-wiki-md/King_Slime.md` (infobox lines 22–32)

- **Max Life:** `2000/2800/3570`
- **Defense:** `10` (single value; no per-difficulty column)
- **Contact damage:** `40/64/96`
- **KB Resist:** `100%`
- **Immune to:** Poisoned, Hemorrhage, Confused, Bleeding, Shimmering
- **Phase 2:** none stated. Behavior notes: hops at the player, summons slimes, teleports when unable to reach the player. Slime spawning is threshold-based: 1–3 Blue Slimes per trigger; first trigger below **95%** health (exactly 1,899 / 2,659 / 3,390), then requires losing ≥5% max HP (**100 / 140 / 178**) since last spawn; max **19 opportunities → 19–57 slimes (38 avg)**. Always spawns **4–7 Blue Slimes** on defeat.
- **Despawn:** if the player dies or gets **more than 187.5 tiles away**, he teleports to the bottom-right corner of the world and despawns in **0.17 seconds**. Also despawns if **all players die** (Slime Rain event continues 9–15 in-game hours).

## 2. Eye of Cthulhu — `~/Project/GLM/SandboxWorld/terraria-wiki-md/Eye_of_Cthulhu.md`

**First form infobox (lines 22–32):**
- **Max Life:** `2800/3640/4641`
- **Defense:** `12`
- **Contact damage:** `15/30/45`
- **KB Resist:** `100%`

**Second form infobox (lines 57–72) — separate table:**
- **Max Life:** `1400/2800` + `[2366/3640]` (Expert) + `[3016/4641]` (Master)
- **Damage:** `23` + `[36]` (Expert) + `[54]` (Master); plus `[40]` (Expert, "when below 145 health") and `[60]` (Master, "when below 185 health")
- **Defense:** `0` / `0` + `[−15]` (Expert, "when below 436 health") + `[−30]` (Expert, "when below 145 health") / `0` + `[−15]` (Master, "when below 556 health") + `[−30]` (Master, "when below 185 health") — i.e. 0 in Classic, negative-scaling in Expert/Master
- **KB Resist:** `100%`

- **Phase-2 threshold (line 228, verbatim):** "falls below **50% / 65%** health (**1,400 / 2,366 / 3,016**)" — spins in place, transforms (sheds iris into a mouth), rams more aggressively **three times**, stops spawning Servants of Cthulhu, **has no defense**, has **increased contact damage**, roars every charge.
- **Despawn (line 230, verbatim):** "not defeated by dawn (**4:30 AM**), if **all players die**, or if it goes **too far off-screen**, it will despawn."

## 3. Eater of Worlds — `~/Project/GLM/SandboxWorld/terraria-wiki-md/Eater_of_Worlds.md`

**Main infobox (lines 22–30)** — no Damage or Defense rows, worm is per-segment:
- **Max Life (total):** `10050` + `[15120]` (Expert) + `[19296]` (Master)
- **KB Resist:** `100%`

**Segments table (lines 158–186)**, columns `Health | Damage | Defense`:

| Segment (NPC ID) | Health | Damage | Defense |
|---|---|---|---|
| Head (13) | `150/210/268` | `22/48/73` | `2/4` |
| Body (14) | `150/210/268` | `13/21/31` | `4/6` |
| Tail (15) | `150/210/268` | `11/18/26` | `8/10` |

Table header caveat (verbatim, lines 166–167): "2 values: Pre-Hardmode › Hardmode / 3 values: Pre-Hardmode › Hardmode › Post-Plantera" — i.e. Health and Damage are Classic/Expert/Master, while the two Defense values are Pre-Hardmode/Hardmode (not difficulty-scaled).

- **Segments count (line 144, verbatim):** "It has a total of **67 / 72** segments" (Classic / Expert).
- **KB Resist:** `100%` (infobox, worm-wide).
- **Phase 2:** none. Splitting instead: destroying any inner body segment splits it into multiple smaller worms, each with own head and tail; every section must be killed.
- **Despawn (lines 202–203, 281):** if the player **dies or leaves the Corruption**, it stops following and goes off-screen until it despawns; it will **not despawn while the player is in the Crimson**. Also "will start to flee underground if the player leaves the Corruption biome, but will not immediately despawn."

## 4. Brain of Cthulhu — `~/Project/GLM/SandboxWorld/terraria-wiki-md/Brain_of_Cthulhu.md`

**First form infobox (lines 22–33):**
- **Max Life:** `1250/2125/2709`, plus stated combined total `3250` + `[5525]` (Expert) + `[7049]` (Master) "(with Creepers)"
- **Defense:** `14`
- **Contact damage:** `30/54/81`
- **KB Resist:** `55%` + `[60%]` (Expert) + `[64%]` (Master)

**Second form infobox (lines 57–67):**
- **Max Life:** `1250/2125/2709`
- **Defense:** `14`
- **Damage:** `30/54/81`
- **KB Resist:** `55%` + `[60%]` (Expert) + `[65%]` (Master) — note the Master value is **65%** here vs **64%** in the first-form box (verbatim discrepancy on the wiki)

**Creepers** (separate page `~/Project/GLM/SandboxWorld/terraria-wiki-md/Creeper.md`, lines 20–24):
- **Max Life:** `100/170/217`; **Damage:** `20/36/54`; **Defense:** `10`; **KB Resist:** `20%/28%/36%`

- **Creeper count (line 194, verbatim):** "**Twenty** Creepers spawn along with the Brain"; Creepers cannot respawn, and **all twenty** must be defeated before phase 2.
- **Phase 2:** not HP-based — triggered when all 20 Creepers are killed; Brain becomes vulnerable and can be directly killed. Expert: three mirror images appear, becoming more opaque as health drops; Creepers more aggressive with increased movement speed. Expert/Master: Creepers (phase 1) and Brain (phase 2) inflict a random debuff on contact (Brain only 1/3 = 33.33% chance; Creepers always).
- **Despawn (line 247, verbatim):** "If the player **leaves the Crimson**, the Brain of Cthulhu will move downwards and despawn." If the player returns before despawn, battle resumes.
- Trivia (line 313): "least health out of all the bosses"; with Creepers' health included it has **more health than King Slime**.

## 5. Skeletron — `~/Project/GLM/SandboxWorld/terraria-wiki-md/Skeletron.md`

**Head infobox (lines 22–39):**
- **Max Life:** `4400/8800/11220`
- **Defense:** `10` + `[10+25 per hand alive]` (Expert); `0` + `[0+25 per hand alive]` (Expert, while spinning); `9999` (during day)
- **Damage:** `32/70/106` (contact); `[68]` (Expert, Skull projectile); `[91]` (Expert, while spinning); `[102]` (Master, Skull); `[137]` (Master, while spinning); `9999` (during day)
- **KB Resist:** `100%`
- Inflicts Bleeding, 100% chance, duration `[6–10 seconds]` (Expert) `[7.5–12.5 seconds]` (Master)

**Hand infobox — separate "Boss Part" table (lines 149–158):**
- **Max Life:** `600/1560/1989` (per hand)
- **Defense:** `14`
- **Damage:** `20/44/66`
- **KB Resist:** `100%`

No combined head+hands total is stated in the infobox; values are per-part as above.

- **Phase cycle (lines 202–207):** alternates between (1) head above while hands slash (~13.33 s) and (2) head spins and chases (~6.67 s); spinning drops defense by 10 (to **0 in Classic Mode**).
- **Expert (lines 215–217):** head defense `+25 per hand alive` → **60 initially, 35 after one hand, 10 after both**; while spinning only reduced to **50 / 25**, then **0** when both hands defeated; spinning damage gets a **30% boost** → `91` (Expert) / `137` (Master).
- **Threshold (line 225, verbatim):** "Once either of the hands are destroyed or the head's health is reduced to **below 75% (6,600 / 8,415)**" — fires homing skulls (~every 1.33 s, doubling to ~0.67 s once both hands are defeated; pauses while spinning).
- **Despawn/enrage (line 209, verbatim):** at "**dawn (4:30 AM)**" it enrages, acts as "exactly as a faster Dungeon Guardian, permanently performing its spinning attack as well increasing its **damage and defense to 9,999**"; stays in this form "until it dies or despawns, even if players manage to avoid dying until the following dusk." Killing it in this form still counts.

## 6. Queen Bee — `~/Project/GLM/SandboxWorld/terraria-wiki-md/Queen_Bee.md` (infobox lines 22–32)

- **Max Life:** `3400/4760/6069`
- **Defense:** `8` + `[8–28]` (Expert) "(depending on health)"
- **Contact damage:** `30/54/81`; Stinger: `22` + `[44]` (Expert) + `[66]` (Master)
- **KB Resist:** `100%`
- Inflicts Poisoned: 33.33% chance / 100% (Expert); 10 s duration / 2–20 s (Expert) / 2.5–25 s (Master) (stinger), 2–8 s (Expert, contact) / 2.5–10 s (Master, contact)

- **Phase 2:** none stated; instead gradual escalation (line 239, Expert): attack **speed increases as health lowers**, at low enough health up to **six charges** in a row, and **defense increases up to a maximum of 28** depending on health depleted.
- **Enrage (line 241):** when fought **outside the Underground Jungle**, movements more aggressive and stingers fire much faster; still enrages in surface Jungle or a different Underground biome, but less aggressively.
- **Despawn (lines 251–254, verbatim):** "Unlike most other bosses, the Queen Bee **does not despawn when far away** from the player and charges towards the player instead"; "The only way to properly despawn the Queen Bee outside of killing her is for **all players in the world to die at once**."

---

### Cross-page notes
- Column conventions differ between pages: most infoboxes use Classic/Expert/Master with brackets marking Expert/Master values; Skeletron's and Eye of Cthulhu's second-form boxes interleave condition qualifiers ("while spinning", "when below 145 health", "during day"); Eater of Worlds' segment table uses 3 difficulty values for Health/Damage but only 2 progression values (Pre-Hardmode/Hardmode) for Defense.
- All six bosses state **KB Resist 100%** except Brain of Cthulhu (55%/60%/64–65%) and its Creepers (20%/28%/36%).
- No file was created or modified; all values above were read directly from the mirror with grep/Read.
```
