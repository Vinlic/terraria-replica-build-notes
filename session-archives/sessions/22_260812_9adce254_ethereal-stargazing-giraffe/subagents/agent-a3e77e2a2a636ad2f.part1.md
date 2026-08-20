# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-13T02:12:13.686Z

```
Read-only extraction task. From the offline Terraria wiki mirror at ~/Project/GLM/SandboxWorld/terraria-wiki-md/, extract the infobox/stat numbers for these boss pages: Wall_of_Flesh.md, Retinazer.md, Spazmatism.md, Skeletron_Prime.md, The_Destroyer.md, Plantera.md.

For EACH page report exactly what the wiki states (verbatim numbers, noting Classic / Expert / Master columns where present):
1. Max life / HP (all three difficulty values). For multi-part bosses (Wall of Flesh + eyes + The Hungry, Skeletron Prime + Prime Cannon/Saw/Vice/Laser, The Destroyer head/body/tail, Plantera second phase) give per-part values as the wiki lists them.
2. Defense (three values) per part.
3. Contact damage (three values) per part.
4. KB resistance if stated.
5. Number of body segments for The Destroyer if stated.
6. Any stated phase-2/phase-3 thresholds (e.g. Twins transform below 40% HP; Plantera second phase at 50% HP; Wall of Flesh behavior) and what stats change in later phases (damage/defense values).
7. Any stated despawn behavior (fleeing at dawn, when player dies, enrage conditions like Plantera outside jungle).

The pages are long; use grep/sed to find the infobox (search for "Max life", "Defense", "KB", "AI", "Type") rather than reading whole files. Do NOT create or modify any files. Return a compact per-boss report with exact wiki numbers, clearly labeling which value belongs to which part and which difficulty.
```

---

## 📎 Attachment · skill_listing · 2026-08-13T02:12:13.689Z

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

## 🤖 Assistant · 2026-08-13T02:12:15.539Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I need to extract infobox data from six Terraria wiki markdown files. Let me start by locating the infobox sections in each file. I'll run parallel greps to find where "Max life", "Defense", "KB", "Type" appear in each file, then read those specific regions.

Let me first check that the files exist and get their sizes, plus grep for the key infobox markers in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-13T02:12:15.699Z · glm-x-preview-260804

```
I'll locate the infobox sections in each file first, then read the relevant ranges.
```


---

## 🤖 Assistant · 2026-08-13T02:12:16.862Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls -la ~/Project/GLM/SandboxWorld/terraria-wiki-md/Wall_of_Flesh.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Retinazer.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Spazmatism.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Skeletron_Prime.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Destroyer.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Plantera.md",
 "description": "List the six boss wiki files"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:16.904Z

**📎 ToolResult**

```
-rw-r--r--@ 1 user  staff  133927  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Plantera.md
-rw-r--r--@ 1 user  staff   68874  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Retinazer.md
-rw-r--r--@ 1 user  staff  123458  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Skeletron_Prime.md
-rw-r--r--@ 1 user  staff   71167  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Spazmatism.md
-rw-r--r--@ 1 user  staff  124625  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Destroyer.md
-rw-r--r--@ 1 user  staff  166202  8月  6 21:57 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Wall_of_Flesh.md

```


---

## 🤖 Assistant · 2026-08-13T02:12:17.138Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"Max life|Defense|KB resist|AI|Environment|Type\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Wall_of_Flesh.md | head -60",
 "description": "Find infobox markers in Wall_of_Flesh.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:17.173Z

**📎 ToolResult**

```
9:This is the **main** page whose information applies to the **[Desktop](Desktop_version_history.md "Desktop version history")** , **[Console](Console_version.md "Console version")** , and **[Mobile](Mobile_version.md "Mobile version")** versions of _[Terraria](Terraria.md "Terraria")_.  
24:Type| [Boss](Boss "Boss")  
26:[Environment](Environment "Environment")| [ The Underworld ](The_Underworld.md "The Underworld")  
27:[AI Type](AI.md "AI")| Wall of Flesh AI  
28:Max Life| 8000/11200/14280  
194:To defeat the Wall of Flesh, the player must attack either its eyes or its mouth. They all share the same health counter, so attacking any of the three will deplete the total health of the boss. However, the eyes have less [defense](Defense.md "Defense") (thus take more damage) than the mouth. No other parts of the Wall of Flesh can be damaged. 
202:The Wall of Flesh can be summoned by dropping a [Guide Voodoo Doll](Guide_Voodoo_Doll.md "Guide Voodoo Doll") into [lava](Lava.md "Lava") in [The Underworld](The_Underworld.md "The Underworld") while the [Guide](Guide.md "Guide") is alive, which destroys the Guide Voodoo Doll and kills the Guide in the process. Alternatively, the boss can also be summoned by letting the Guide die within lava in The Underworld. He can die by any means (the player, an enemy, or the environment), as long as he is touching lava when he dies.[2]
206:### Technical details
208:When the Guide Voodoo Doll is destroyed or the Guide is killed in lava, the game checks whether all players are horizontally at least 75 tiles away from the location of the doll/Guide. If they are, then the Wall of Flesh is spawned at that horizontal position. Otherwise, the game moves one tile towards the closest lateral [world border](World_border.md "World border") and checks again, repeating this until it encounters a tile that is horizontally at least 75 tiles away from any player. It stops 20 tiles before the true world border (i.e. 21/22 tiles away from the visible world border), even if a player is still within 75 tiles at that point (e.g. standing directly against the visible world border). 
210:After locating the horizontal spawn position, the game determines a valid vertical position. The spawning tile must not be occupied by a solid block and its liquid level must not exceed 100 (i.e. at most approx. 39% of the tile can contain liquid). Again, the game begins at the vertical position of the doll/Guide and checks if that location is valid. Then it checks one tile above that spot and one tile below it, then two tiles above and two tiles below, and so on, until finding a valid spot. If the game finds no valid spot after 1000 attempts (i.e. 1000 tiles above and below), then it reverts to the initial vertical position. Finally, the vertical limits are enforced: If the vertical position that was encountered is higher than 10 tiles below the [Cavern](Cavern.md "Cavern")–Underworld border, it is forcibly moved down to that position (even though the tile there was not considered valid before), and if it is lower than 80 tiles below that border (roughly the vertical center of the Underworld), it is forcibly moved up to that position (again, even though the tile at that position was not considered valid before). 
220:While this debuff is active, if the player collides with the "wall" part of the Wall of Flesh, they will take 50 / [100](Expert_Mode.md "Expert Mode") / [150](Master_Mode.md "Master Mode") damage and be [knocked back](Knockback.md "Knockback") in the direction the Wall of Flesh is facing. This damage does not have the usual ±15% random variance, and ignores the player's knockback immunity (e.g. from the [Cobalt Shield](Cobalt_Shield.md "Cobalt Shield") and its upgrades). If the player is killed by this damage, the [death message](Death.md "Death") _“ <Player name> was slain...”_[3] is displayed. 
226:The Wall of Flesh moves faster as its health depletes; see below for details. It can reach up to 17 mph / [41 mph](Expert_Mode.md "Expert Mode") at very low health levels. Due to the Wall of Flesh's higher movement speed in Expert Mode, the speed at which it draws players via the Tongue debuff in Expert also increases as its health decreases. 
230:  * The Wall of Flesh has small mouths called The Hungry, each attached by a long vein, which move towards and damage players. As the Wall of Flesh's main body takes damage, they deal more damage and become more resistant to attacks. When sufficiently damaged, they detach and fly towards players at high speed. 
232:    * In Expert Mode, the Hungry gain extra [knockback](Knockback.md "Knockback") resistance with each additional player in [multiplayer](Multiplayer.md "Multiplayer"), and become immune to knockback when there are at least 5 players.[4]
274:Type| [Boss](Boss "Boss")  
276:[Environment](Environment "Environment")| [ The Underworld ](The_Underworld.md "The Underworld")  
277:[AI Type](AI.md "AI")| Wall of Flesh AI  
279:Max Life| 8000/11200/14280  
280:[Defense](Defense.md "Defense")| 12/18  
309:Type| [Boss](Boss "Boss")  
311:[Environment](Environment "Environment")| [ The Underworld ](The_Underworld.md "The Underworld")  
312:[AI Type](AI.md "AI")| Wall of Flesh Eye AI  
315:Max Life| 8000/11200/14280  
316:[Defense](Defense.md "Defense")| 0/6  
353:Type| [Enemy](Enemy "Enemy")  
355:[Environment](Environment "Environment")| [ The Underworld ](The_Underworld.md "The Underworld")  
356:[AI Type](AI.md "AI")| The Hungry AI  
361:Max Life| 240/336/504  
362:[Defense](Defense.md "Defense")| 10/16 (WoF health >75%)  
397:Type| [Flying Enemy](Flying_Enemy "Flying Enemy")  
399:[Environment](Environment "Environment")| [ The Underworld ](The_Underworld.md "The Underworld")  
400:[AI Type](AI.md "AI")| Demon Eye AI  
402:Max Life| 80/112/168  
403:[Defense](Defense.md "Defense")| 6  
434:When the Wall of Flesh is killed, it leaves its [drops](Drops "Drops") in a midair 9×9-tile frame of [Demonite Bricks](Demonite_Brick.md "Demonite Brick") (in [Corruption](Corruption "Corruption") worlds) or [Crimtane Bricks](Crimtane_Brick.md "Crimtane Brick") (in [Crimson](Crimson "Crimson") worlds). It will also always drop the [Pwnhammer](Pwnhammer.md "Pwnhammer"), which is required to generate [Hardmode](Hardmode.md "Hardmode") ores in the world (through breaking [Demon](Demon_Altar "Demon Altar") or [Crimson Altars](Crimson_Altar "Crimson Altar") with a hammer of 80% hammer power or higher, of which the Pwnhammer is the first obtained). 
443:Main article: [Hardmode](Hardmode.md "Hardmode")
451:  * Being able to summon the Wall of Flesh depends on the [Guide](Guide.md "Guide") being alive. He cannot respawn if it is [nighttime](Night "Night") or there is an [event](Event "Event") in progress. Due to this, the waiting time between multiple fights is often much greater than with other bosses. Timing the fight to finish just before dawn has a chance to allow two or even more fights, especially if the Guide already has an assigned [house](House.md "House").
456:  * In a world where the [special world seed](Special_world_seed "Special world seed") [For the Worthy](For_the_Worthy.md "For the Worthy") is active, the Wall of Flesh's eyes and mouth are much smaller, while The Hungry are much larger. [Fire Imps](Fire_Imp.md "Fire Imp") with higher defense and faster [Burning Spheres](Burning_Sphere.md "Burning Sphere") also constantly spawn throughout the fight.
457:  * As a result of the spawning mechanics, the Wall of Flesh can move towards the side of world which is laterally shorter. For example, when a Guide Voodoo Doll is dropped into lava more than 75 tiles away from the player in the right half of the world, and the player is on the right side of the location of said doll, the Wall of Flesh will be summoned on the left side of the player and move rightwards.
471:**[It's Hard!](Achievements#It's_Hard! "Achievements")**  • _“Unleash the ancient spirits of light and darkness across your world, enabling much stronger foes and showering the world with dazzling treasures (and rainbows!).”_
490:  * If the Wall of Flesh was recently summoned, make sure the Guide has respawned before attempting to summon the Wall of Flesh again to avoid the unnecessary loss of [Voodoo Dolls](Voodoo_Doll "Voodoo Doll").
493:    * The two main types of Wall of Flesh arenas are solid bridges and platform bridges, each with their own pros and cons. 
494:      * Solid bridges are made out of solid blocks, blocking lasers from the bottom eye and allowing bouncing projectiles to rebound against it, but come at the cost of blocking most of the player's own projectiles and not allowing dropping down through to evade attacks.
495:      * Platform bridges allow projectiles to pass through them, allowing the user to damage all parts of the boss more often and drop down from them if needed to dodge lasers. However, it does not block the bottom eye's lasers, and certain projectiles like [Beenades](Beenade.md "Beenade") do not work well unless they hit solid blocks. In [Expert Mode](Expert_Mode.md "Expert Mode") and higher, it is recommended to build these out of [Stone Platforms](Stone_Platform "Stone Platform"), [Ash Wood Platforms](Ash_Wood_Platform "Ash Wood Platform") or [Obsidian Platforms](Obsidian_Platform "Obsidian Platform") which will not be destroyed by dying [Lava Slimes](Lava_Slime.md "Lava Slime").
498:  * Focus on The Hungry first before damaging the wall itself. The Hungry's damage and defense are boosted as the body takes damage, which will make them more difficult to kill if left for later.
505:  * The lead developer of _[Terraria](Terraria.md "Terraria")_ , [Redigit](Redigit.md "Redigit"), has confirmed that the [Guide](Guide.md "Guide") is the Wall of Flesh on the official _Terraria_ Discord.[7] This explains the relevancy of his death to the appearance of the boss. 
514:  * The veining at the back of both eye and mouth is identical to the veins trailing the [Eye of Cthulhu](Eye_of_Cthulhu.md "Eye of Cthulhu").
530:    * The Hungry no longer gain a 3rd stat bonus after 25% Wall of Flesh health. They will continue to use the 2nd stat bonus from 50% WoF health for the remainder of the fight.
584:  5. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, method `AI()` in `Terraria.NPC.cs`. The relevant part is the `aiStyle == 27` block. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
686:  * [Sea Snail](Sea_Snail.md "Sea Snail")
722:  * [Arapaima](Arapaima.md "Arapaima")
769:  * [Wraith](Wraith.md "Wraith")
800:    * [Tainted](Tainted_Ghoul "Tainted Ghoul")
847:[Rain](Rain.md "Rain")
852:  * [Raincoat Zombie](Raincoat_Zombie.md "Raincoat Zombie")
854:    * [Rainbow](Rainbow_Slime.md "Rainbow Slime")
899:  * [Nailhead](Nailhead.md "Nailhead")
945:  * [Captain](Pirate_Captain.md "Pirate Captain")
947:  * [Corsair](Pirate_Corsair.md "Pirate Corsair")
954:  * [Brain Scrambler](Brain_Scrambler.md "Brain Scrambler")

```


---

## 🤖 Assistant · 2026-08-13T02:12:17.540Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"Max life|Defense|KB resist|AI|Environment|Type\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Retinazer.md | head -60",
 "description": "Find infobox markers in Retinazer.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:17.583Z

**📎 ToolResult**

```
18:enemies]: Maximum number of enemies Abigail can damage at once
55:  *[Power]: Bait power
102:  *[Hej, tady nejsme ve filmu, kámo. Náboje něco stojí.]: Hey, this ain't a movie, pal. Ammo costs extra.
565:  *[Def.]: Defense
573:  *[Dynamit. Můj speciální lík na všechno, co tě trápí.]: Dynamite, my own special cure-all for what ails ya.
585:  *[Podepsal bys mi tento griefovací dokument?]: Hey, could you sign this Griefing Waiver?
599:  *[N/A]: Not available in vanilla game
744:  *[Chain charge]: Expert Mode
893:  *[Říká se, že existuje člověk, který ti poradí, jak máš přežít v této krajině… ale počkat. To jsem přeci já.]: They say there is a person who will tell you how to survive in this land... oh wait. That's me.
1008:  *[defense]: Expert Mode
1016:  *[The [](Shield_of_Cthulhu.md "Shield of Cthulhu")[Shield of Cthulhu](Shield_of_Cthulhu.md "Shield of Cthulhu") can greatly increase your mobility as well as provide some extra defense.]: Expert Mode
1018:  *[The [](Brain_of_Confusion.md "Brain of Confusion")[Brain of Confusion](Brain_of_Confusion.md "Brain of Confusion") has a chance to dodge an attack, providing the player with a useful [](Cerebral_Mindtrick "Cerebral Mindtrick")[Cerebral Mindtrick](Cerebral_Mindtrick "Cerebral Mindtrick") buff.]: Expert Mode
1039:  *[The [](Brain_of_Confusion.md "Brain of Confusion")[Brain of Confusion](Brain_of_Confusion.md "Brain of Confusion") is very useful for players as it provides a chance to dodge an attack, but is exclusive to Crimson worlds. It doesn't prevent getting inflicted with the [](Cursed_Inferno.md "Cursed Inferno")[Cursed Inferno](Cursed_Inferno.md "Cursed Inferno") debuff, however.]: Expert Mode
1337:  *[Zase trable s těmi tyrany?]: Trouble with those bullies again?
1339:  *[vypadáš, jako kdybys byl napůl strávený. Zase jsi honil slizy?]: You look half digested. Have you been chasing slimes again?

```


---

## 🤖 Assistant · 2026-08-13T02:12:17.974Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"Max life|Defense|KB resist|AI|Environment|Type\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Spazmatism.md | head -60",
 "description": "Find infobox markers in Spazmatism.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:18.009Z

**📎 ToolResult**

```
18:enemies]: Maximum number of enemies Abigail can damage at once
55:  *[Power]: Bait power
102:  *[Hej, tady nejsme ve filmu, kámo. Náboje něco stojí.]: Hey, this ain't a movie, pal. Ammo costs extra.
565:  *[Def.]: Defense
573:  *[Dynamit. Můj speciální lík na všechno, co tě trápí.]: Dynamite, my own special cure-all for what ails ya.
585:  *[Podepsal bys mi tento griefovací dokument?]: Hey, could you sign this Griefing Waiver?
599:  *[N/A]: Not available in vanilla game
744:  *[Chain charge]: Expert Mode
893:  *[Říká se, že existuje člověk, který ti poradí, jak máš přežít v této krajině… ale počkat. To jsem přeci já.]: They say there is a person who will tell you how to survive in this land... oh wait. That's me.
1008:  *[defense]: Expert Mode
1016:  *[The [](Shield_of_Cthulhu.md "Shield of Cthulhu")[Shield of Cthulhu](Shield_of_Cthulhu.md "Shield of Cthulhu") can greatly increase your mobility as well as provide some extra defense.]: Expert Mode
1018:  *[The [](Brain_of_Confusion.md "Brain of Confusion")[Brain of Confusion](Brain_of_Confusion.md "Brain of Confusion") has a chance to dodge an attack, providing the player with a useful [](Cerebral_Mindtrick "Cerebral Mindtrick")[Cerebral Mindtrick](Cerebral_Mindtrick "Cerebral Mindtrick") buff.]: Expert Mode
1039:  *[The [](Brain_of_Confusion.md "Brain of Confusion")[Brain of Confusion](Brain_of_Confusion.md "Brain of Confusion") is very useful for players as it provides a chance to dodge an attack, but is exclusive to Crimson worlds. It doesn't prevent getting inflicted with the [](Cursed_Inferno.md "Cursed Inferno")[Cursed Inferno](Cursed_Inferno.md "Cursed Inferno") debuff, however.]: Expert Mode
1337:  *[Zase trable s těmi tyrany?]: Trouble with those bullies again?
1339:  *[vypadáš, jako kdybys byl napůl strávený. Zase jsi honil slizy?]: You look half digested. Have you been chasing slimes again?

```


---

## 🤖 Assistant · 2026-08-13T02:12:18.378Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"Max life|Defense|KB resist|AI|Environment|Type\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Skeletron_Prime.md | head -60",
 "description": "Find infobox markers in Skeletron_Prime.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:18.506Z

**📎 ToolResult**

```
9:This is the **main** page whose information applies to the **[Desktop](Desktop_version_history.md "Desktop version history")** , **[Console](Console_version.md "Console version")** , and **[Mobile](Mobile_version.md "Mobile version")** versions of _[Terraria](Terraria.md "Terraria")_.  
24:Type| [Boss](Boss "Boss")  
26:[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
27:[AI Type](AI.md "AI")| Skeletron Prime Head AI  
31:Max Life| 28000/42000/53550  
32:[Defense](Defense.md "Defense")| 24  
107: _“ The air is getting colder around you...”_
119:It also has a 1/10 (10%) chance to spawn naturally at dusk (7:30 PM) during Hardmode once a [Demon or Crimson Altar](Altars.md "Altars") has been destroyed, as long as it has not yet been defeated at least once in the current world. When spawning naturally, its arrival is announced by the [status message](Status_message "Status message") _" The air is getting colder around you..."_. 
135:Type| Boss Part  
137:[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
138:[AI Type](AI.md "AI")| Prime Cannon AI  
141:Max Life| 7000/10500/13387  
142:[Defense](Defense.md "Defense")| 23  
175:Type| Boss Part  
177:[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
178:[AI Type](AI.md "AI")| Prime Saw AI  
180:Max Life| 9000/13500/17212  
181:[Defense](Defense.md "Defense")| 38  
203:Type| Boss Part  
205:[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
206:[AI Type](AI.md "AI")| Prime Vice AI  
208:Max Life| 9000/13500/17212  
209:[Defense](Defense.md "Defense")| 34  
231:Type| Boss Part  
233:[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
234:[AI Type](AI.md "AI")| Prime Laser AI  
237:Max Life| 6000/9000/11475  
238:[Defense](Defense.md "Defense")| 20  
264:Skeletron Prime's head constantly endeavors to remain between 31.5 and 12.5 tiles above the player and within 6.25 tiles of either side of the player. It can accelerate infinitely in order to move back into this area. The head does not actively attempt to make contact with the player.[1]
268:  * Prime Cannon fires bombs every 2.33 seconds that do not destroy tiles[5], usually up into the air rather than directly at the player. It usually stays above the player.
269:  * Prime Saw usually remains under the player, moving up and down.
270:  * Prime Vice will swipe around wildly, making occasional lunges at the player. It usually remains diagonal to the player.
275:  * Skeletron Prime's head will grow spikes and start spinning towards the player at 10 mph, exactly like how its pre-Hardmode counterpart [Skeletron](Skeletron.md "Skeletron") does. Damage and defense are doubled to 94 / [160](Expert_Mode.md "Expert Mode") / [240](Master_Mode.md "Master Mode") damage and 48 defense.[1] In [Expert Mode](Expert_Mode.md "Expert Mode"), the base spinning speed is 31 mph and is increased the further the player is away, up to a maximum of 76 mph at a distance of 37.5 tiles.
276:  * Prime Cannon will aim at the player directly and decrease its cooldown between firing to 0.67 seconds.
282:If Skeletron Prime is not killed before [dawn](Dawn "Dawn") (4:30 AM), it will enrage and permanently behave like a faster Dungeon Guardian, increasing its velocity[6] and usually killing the player instantly upon contact: its damage and defense is increased to 9,999.[1] It will remain in this state until defeated, even if it becomes night again. Killing Skeletron Prime in this form still counts as defeating it and it will drop its items normally. 
291:  * With the 1/10 (10%) chance of spawning naturally at dusk, the resulting chance for each mechanical boss is initially 1/30 (3.33%). Once one of them has been defeated, the remaining two have a resulting 1/20 (5%) chance of spawning naturally, and after defeating the second one, the last one has the full chance of 1/10 (10%).
311:**[Mecha Mayhem](Achievements#Mecha_Mayhem "Achievements")**  • _“Do battle against the Twins, the Destroyer, and Skeletron Prime simultaneously and emerge victorious.”_
329:  * Unhindered movement is crucial when Skeletron Prime's head starts spinning, as it deals double the regular damage. [Wings](Wings.md "Wings") greatly aid in moving vertically, and flattened terrain or a [sky bridge](Sky_bridge.md "Sky bridge") are convenient for horizontal movement.
332:  * Due to Skeletron Prime's overall high defense, inflicting it with [Ichor](Ichor_\(debuff\) "Ichor \(debuff\)") is effective, as it is not immune to it. Note that most Ichor weapons lack in damage compared to other weapons, so they should only be used periodically for inflicting the debuff.
340:  * It is the only mechanical boss whose name contains the [pre-Hardmode](Pre-Hardmode.md "Pre-Hardmode") boss's name. Furthermore, it used to be the only mechanical boss that shared boss music with its pre-Hardmode variant. Additionally, its name does not begin with the word _The_ , unlike the other two mechanical bosses.
341:  * Unlike [Skeletron](Skeletron.md "Skeletron"), Skeletron Prime's defense doubles when its head is spinning.
370:    * Skeletron Prime AI overhaul: will now act similar to Skeletron and spin faster in [Expert Mode](Expert_Mode.md "Expert Mode").
379:    * Increased health, damage and defense of most parts.
384:    * Now has a chance to spawn naturally at dusk with the message: "The air is getting colder around you...".
387:    * Reduced health, damage and defense of all parts and head.
409:  1. ↑ 1.0 1.1 1.2 1.3 1.4 1.5 1.6 1.7 Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.5.5](1.4.5.5.md "1.4.5.5") source code, method `AI()` in `Terraria.NPC.cs`. The relevant part is the `aiStyle == 32` block. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
411:  3. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.0.5](1.4.0.5.md "1.4.0.5") source code, methods `AI_106()` in `Terraria.Projectile.cs` and `Kill()` in `Terraria.Projectile.cs`. The relevant parts are under `type == 102`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
412:  4. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.3](1.4.3.md "1.4.3") source code, method `AI()` in `Terraria.NPC.cs`. The relevant part is the `aiStyle == 36` block. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
414:  6. ↑ Skeletron Prime's velocity is based on its distance to the player, following this formula: [math]\displaystyle{ \text{velocity}_{\text{mph}} = \frac{9}{11} * \text{distance}_{\text{tiles}} + \frac{1125}{22} }[/math] It ranges from 51 mph at a distance of zero tiles to 164 mph at a distance of 137.5 tiles, where it is capped. Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.1.2](1.4.1.2.md "1.4.1.2") source code, method `AI()` in `Terraria.NPC.cs`. The relevant part is the `aiStyle == 32` block. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
415:  7. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.5.5](1.4.5.5.md "1.4.5.5") source code, method `UpdateTime()` in `Terraria.Main.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
416:  8. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.5.5](1.4.5.5.md "1.4.5.5") source code, method `UpdateTime_StartNight()` in `Terraria.Main.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
514:  * [Sea Snail](Sea_Snail.md "Sea Snail")
550:  * [Arapaima](Arapaima.md "Arapaima")
597:  * [Wraith](Wraith.md "Wraith")
628:    * [Tainted](Tainted_Ghoul "Tainted Ghoul")
675:[Rain](Rain.md "Rain")
680:  * [Raincoat Zombie](Raincoat_Zombie.md "Raincoat Zombie")
682:    * [Rainbow](Rainbow_Slime.md "Rainbow Slime")
727:  * [Nailhead](Nailhead.md "Nailhead")
773:  * [Captain](Pirate_Captain.md "Pirate Captain")

```


---

## 🤖 Assistant · 2026-08-13T02:12:18.808Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"Max life|Defense|KB resist|AI|Environment|Type\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Destroyer.md | head -60",
 "description": "Find infobox markers in The_Destroyer.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:18.864Z

**📎 ToolResult**

```
9:This is the **main** page whose information applies to the **[Desktop](Desktop_version_history.md "Desktop version history")** , **[Console](Console_version.md "Console version")** , and **[Mobile](Mobile_version.md "Mobile version")** versions of _[Terraria](Terraria.md "Terraria")_.  
24:Type| [Boss](Boss "Boss")[Burrowing Enemy](Burrowing_Enemy "Burrowing Enemy")  
26:[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
27:[AI Type](AI.md "AI")| The Destroyer AI  
28:Max Life| 80000/120000/153000  
137:[NPC ID](NPC_IDs.md "NPC IDs") | Type  | Damage  | Defense   
142:136  |  | The Destroyer Tail | 40/68/102 | 35  
146:The Destroyer spawns coiled up, like most worm enemies, and immediately starts uncoiling and following the player. It has limited mobility when fully in the air, requiring [blocks](Blocks.md "Blocks") or [platforms](Platforms.md "Platforms") to "burrow" through. However, it is able to move freely while off-screen. It follows the player from any distance and will only despawn if the player dies or if dawn comes (4:30 AM). It despawns by quickly traveling underground until off-screen. 
155:Each body segment has a 1/25 (4%) chance to release a Probe whenever it is damaged. This only happens once per segment and is signified by the red light on the segment turning off.[4] Probes will fly towards the player, attempting to maintain a distance while occasionally moving into melee range. They fire lasers with moderate accuracy. 
157:  * Probes never return to the main body, and will not despawn as long as The Destroyer is alive, even if the player goes too far away.[5]
158:  * Killing the boss itself does not destroy the remaining Probes, and they will still continue to attack the player afterwards.
167:  * With the 1/10 (10%) chance of spawning naturally at dusk, the resulting chance for each mechanical boss is initially 1/30 (3.33%). Once one of them has been defeated, the remaining two have a resulting 1/20 (5%) chance of spawning naturally, and after defeating the second one, the last one has the full chance of 1/10 (10%).
187:**[Mecha Mayhem](Achievements#Mecha_Mayhem "Achievements")**  • _“Do battle against the Twins, the Destroyer, and Skeletron Prime simultaneously and emerge victorious.”_
207:  * As with the Eater of Worlds, weapons that can hit several enemies are highly effective against The Destroyer. 
208:    * For extra risk and reward, line up with the head (which has no defense) and fire down the length of its body.
217:  * The Destroyer is extremely long, measuring 82 segments including head and tail, or 239 tiles in length.[9]
244:    * Health returned to 80,000 (from 60,000). Damage and defense increased: 
246:      * Body damage increased from 35 to 55. Defense returned to 30 (from 26).
247:      * Tail damage increased from 20 to 40. Defense returned to 35 (from 30).
254:    * Health reduced from 80,000 to 60,000. Damage and defense reduced: 
256:      * Body damage reduced from 40 to 35. Defense reduced from 30 to 26.
257:      * Tail defense reduced from 35 to 30.
274:    * Health returned to 80,000 (from 60,000). Damage and defense increased: 
276:      * Body damage increased from 35 to 55. Defense returned to 30 (from 26).
277:      * Tail damage increased from 20 to 40. Defense returned to 35 (from 30).
282:    * Health reduced from 80,000 to 60,000. Damage and defense reduced: 
284:      * Body damage reduced from 40 to 35. Defense reduced from 30 to 26.
285:      * Tail defense reduced from 35 to 30.
319:  2. ↑ 2.0 2.1 2.2 2.3 Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.1.2](1.4.1.2.md "1.4.1.2") source code, method `AI_037_Destroyer()` in `Terraria.NPC.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
320:  3. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.5.6](1.4.5.6.md "1.4.5.6") source code, method `AI_005_EaterOfSouls()` in `Terraria.NPC.cs`.
321:  4. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.5.6](1.4.5.6.md "1.4.5.6") source code, methods `HitEffect()` in `Terraria.NPC.cs` and `AI_037_Destroyer()` in `Terraria.NPC.cs`.
323:  6. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.5.5](1.4.5.5.md "1.4.5.5") source code, method `UpdateTime()` in `Terraria.Main.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
324:  7. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.5.5](1.4.5.5.md "1.4.5.5") source code, method `UpdateTime_StartNight()` in `Terraria.Main.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
445:  * [Sea Snail](Sea_Snail.md "Sea Snail")
481:  * [Arapaima](Arapaima.md "Arapaima")
528:  * [Wraith](Wraith.md "Wraith")
559:    * [Tainted](Tainted_Ghoul "Tainted Ghoul")
606:[Rain](Rain.md "Rain")
611:  * [Raincoat Zombie](Raincoat_Zombie.md "Raincoat Zombie")
613:    * [Rainbow](Rainbow_Slime.md "Rainbow Slime")
658:  * [Nailhead](Nailhead.md "Nailhead")
704:  * [Captain](Pirate_Captain.md "Pirate Captain")
706:  * [Corsair](Pirate_Corsair.md "Pirate Corsair")
713:  * [Brain Scrambler](Brain_Scrambler.md "Brain Scrambler")
769:  * [Brain Suckler](Brain_Suckler.md "Brain Suckler")
793:  * [](Brain_of_Cthulhu.md "Brain of Cthulhu")[Brain of Cthulhu](Brain_of_Cthulhu.md "Brain of Cthulhu")
873:  * [Snail](Snail.md "Snail")
874:    * [Glowing](Glowing_Snail.md "Glowing Snail")
875:    * [Magma](Magma_Snail.md "Magma Snail")
913:  * [Fairies](Fairies.md "Fairies")
937:  * [Zebra Swallowtail](Zebra_Swallowtail_Butterfly.md "Zebra Swallowtail Butterfly")
951:  * [](Painter.md "Painter")[Painter](Painter.md "Painter")
995:waiting for rescue](NPCs.md "NPCs")
1023:  * [The Destroyer AI NPCs](Category%3AThe_Destroyer_AI_NPCs "Category:The Destroyer AI NPCs")
1035:  * Mainspace pages with a corresponding Legacy page
1057:This page is issued from [Terraria Wiki](https://terraria.wiki.gg/wiki/?title=The_Destroyer&oldid=1003547 "Last edited on 2026-07-15"). The text is available under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-nc-sa/4.0) unless otherwise noted. Additional terms may apply for the media files. 
1070:enemies]: Maximum number of enemies Abigail can damage at once
1107:  *[Power]: Bait power
1154:  *[Hej, tady nejsme ve filmu, kámo. Náboje něco stojí.]: Hey, this ain't a movie, pal. Ammo costs extra.
1617:  *[Def.]: Defense

```


---

## 🤖 Assistant · 2026-08-13T02:12:19.180Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"Max life|Defense|KB resist|AI|Environment|Type\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Plantera.md | head -60",
 "description": "Find infobox markers in Plantera.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:19.230Z

**📎 ToolResult**

```
9:This is the **main** page whose information applies to the **[Desktop](Desktop_version_history.md "Desktop version history")** , **[Console](Console_version.md "Console version")** , and **[Mobile](Mobile_version.md "Mobile version")** versions of _[Terraria](Terraria.md "Terraria")_.  
24:Type| [Boss](Boss "Boss")  
26:[Environment](Environment "Environment")| [ Underground Jungle ](Underground_Jungle.md "Underground Jungle")  
27:[AI Type](AI.md "AI")| Plantera AI  
32:Max Life| 30000[42000](Expert_Mode.md "Expert Mode")[53550](Master_Mode.md "Master Mode")  
33:[Defense](Defense.md "Defense")| 36 [1]  
84:Type| [Boss](Boss "Boss")  
86:[Environment](Environment "Environment")| [ Underground Jungle ](Underground_Jungle.md "Underground Jungle")  
87:[AI Type](AI.md "AI")| Plantera AI  
89:Max Life| 15000/30000[21000/42000](Expert_Mode.md "Expert Mode")[26775/53550](Master_Mode.md "Master Mode")  
90:[Defense](Defense.md "Defense")| 10 [1]  
286:Type| Boss PartInvincible  
288:[Environment](Environment "Environment")| [ Underground Jungle ](Underground_Jungle.md "Underground Jungle")  
289:[AI Type](AI.md "AI")| Plantera's Hook AI  
291:Max Life| 4000/8000/12000  
292:[Defense](Defense.md "Defense")| 24  
313:Type| Boss Part  
315:[Environment](Environment "Environment")| [ Underground Jungle ](Underground_Jungle.md "Underground Jungle")  
316:[AI Type](AI.md "AI")| Plantera's Tentacle AI  
318:Max Life| 1000/2000/2550  
319:[Defense](Defense.md "Defense")| 20  
341:Type| [Projectile NPC](Projectile_NPC "Projectile NPC")  
343:[Environment](Environment "Environment")| [ Underground Jungle ](Underground_Jungle.md "Underground Jungle")  
344:[AI Type](AI.md "AI")| Spore AI  
346:Max Life| 1  
347:[Defense](Defense.md "Defense")| 0  
369:After all three mechanical bosses have been defeated, [Plantera's Bulbs](Plantera's_Bulb.md "Plantera's Bulb") will randomly spawn in the Underground Jungle (indicated by the [status message](Status_message "Status message") _" The jungle grows restless..."_). These bulbs emit a faint pink light in dark areas and immediately summon Plantera nearby upon being destroyed, usually a fair distance off-screen. 
379:Plantera travels slowly through blocks using three long vines to grapple onto solid foreground blocks, similarly to [multi-hooks](Hooks.md "Hooks"). In the second phase, Plantera gains the ability to grapple onto [background walls](Background_walls.md "Background walls"). The ends of her vines, called Plantera's Hooks, are completely invincible and deal contact damage. 
393:Poison Seeds and Thorn Balls are only used when Plantera's health is below 80% (24,000 / [33,600](Expert_Mode.md "Expert Mode") / [42,840](Master_Mode.md "Master Mode")). There is a short cooldown after a projectile has been fired, which depends on Plantera's current health as well as the type of projectile: 
409:Once Plantera is brought down to half of her maximum health (15,000 / [21,000](Expert_Mode.md "Expert Mode") / [26,775](Master_Mode.md "Master Mode")), she changes into her second form as her pink petals fall away to reveal a thorn-filled mouth. In this form, Plantera ceases to fire the same projectiles from before and instead moves much more quickly and aggressively in an attempt to inflict contact damage. Her contact damage is greater than in the first form, but her defense decreases significantly to 10. 
422:Plantera becomes "enraged" if she follows the player out of the [Underground Jungle](Underground_Jungle.md "Underground Jungle"), whether it be to the surface, to the [Underworld](Underworld "Underworld"), or to a completely different biome. She does not enrage in [Hallowed](Hallowed "Hallowed"), [Corrupted](Corrupted "Corrupted") or [Crimson](Crimson "Crimson") parts of the Underground Jungle as long as there are at least 140 [Jungle grass](Jungle_grass.md "Jungle grass") / [Hive](Hive.md "Hive") / [Lihzahrd Brick](Lihzahrd_Brick.md "Lihzahrd Brick") blocks nearby. Being enraged causes Plantera to gain double damage, double defense (quadruple defense in the second form), and increased movement speed, as well as changing her attack patterns and directly rushing toward the player. Her projectiles also deal double damage and have reduced cooldowns. Plantera's behavior returns to normal upon reentering the Underground Jungle biome. 
437:In her second form, Plantera and Plantera's Tentacles move faster than normal. In addition, there are nine more Plantera's Tentacles, attached to Plantera's Hooks in groups of three. Furthermore, the eight tentacles that are attached to Plantera's body can respawn after they have been killed (this does not apply to the tentacles on the hooks). The rate is randomized, but it depends on the number of tentacles that are alive – if all tentacles are destroyed, a new tentacle spawns after 5 seconds, on average. This is increased by 5 seconds per living tentacle, hence it takes an average of 180 seconds for all eight tentacles to fully respawn. A single defeated tentacle will take 40 seconds to respawn, on average, assuming the other seven tentacles remain alive for the duration.[1]
443:A [status message](Status_message "Status message") saying _" Screams are echoing from the dungeon..."_ will appear upon Plantera's defeat, signaling that new, more difficult types of [enemies](Enemies.md "Enemies") will begin spawning in the [Dungeon](Dungeon.md "Dungeon") ([see details](Dungeon#Hardmode_post-Plantera_Dungeon "Dungeon")). These enemies drop powerful new weapons, accessories, and other items. [Dungeon Spirits](Dungeon_Spirit.md "Dungeon Spirit") will begin to appear when Dungeon enemies with more than 100 health are slain, which drop [Ectoplasm](Ectoplasm.md "Ectoplasm"), a new [crafting material](Crafting_material "Crafting material") that offers access to the [Pumpkin Moon](Pumpkin_Moon.md "Pumpkin Moon") and [Frost Moon](Frost_Moon.md "Frost Moon") [events](Event "Event"), as well as [Spectre Bars](Spectre_Bar.md "Spectre Bar"). 
455:  * [Butchers](Butcher.md "Butcher"), [Psychos](Psycho.md "Psycho"), [Nailheads](Nailhead.md "Nailhead"), [Deadly Spheres](Deadly_Sphere.md "Deadly Sphere"), [Dr. Man Flies](Dr._Man_Fly.md "Dr. Man Fly"), and [Mothrons](Mothron.md "Mothron") will start spawning during the [Solar Eclipse](Solar_Eclipse.md "Solar Eclipse") event.
460:  * The conditions of whether [Jungle Temple](Jungle_Temple.md "Jungle Temple") building supplies can be dropped is checked upon entering the world, or occasionally during gameplay.[a] If no [Lihzahrd Bricks](Lihzahrd_Brick.md "Lihzahrd Brick") and no unsafe [Lihzahrd Brick Walls](Lihzahrd_Brick_Wall.md "Lihzahrd Brick Wall") were found (i.e. no tiles with [ID](Tile_IDs.md "Tile IDs") 226 and no walls with [ID](Wall_IDs.md "Wall IDs") 87 exist in world), Plantera will drop Jungle Temple building materials upon its defeat and reset the drop condition (i.e. it cannot drop them again until another check is performed and passed). [7] This means that, should the player lose their world's Lihzahrd Altar, it is possible to obtain another without switching worlds by removing the entirety of the Jungle Temple.
462:  * If Plantera has no surfaces to latch onto, she will slowly float upward, eventually going up into [Space](Space.md "Space"), or until she hits a space where she can latch onto again. Plantera's Hooks pass through blocks, so trying to trap her will be unsuccessful; she will simply latch out.
493:  * Narrow passages slow Plantera as it takes more time for her to grip the surrounding terrain.
586:  1. ↑ 1.0 1.1 1.2 1.3 1.4 1.5 1.6 Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.1.2](1.4.1.2.md "1.4.1.2") source code, method `AI()` in `Terraria.NPC.cs`. The relevant part is in the `aiStyle == 51` block. Note that several of Plantera's stats, including damage and defense, are hard-coded there. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
590:  5. ↑ 5.0 5.1 Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, method `AI()` in `Terraria.NPC.cs`. The relevant part is the `aiStyle == 51` block. Internally, a counter which starts at 0 is used to determine whether the Plantera can shoot a projectile. Each tick, the counter is increased by 1; this increment will be further increased in these conditions: +1 when Plantera's health is under 90%, 80%, 70%, and 60%, respectively; +1 in [Expert Mode](Expert_Mode.md "Expert Mode"); +1 in [For the Worthy](For_the_Worthy.md "For the Worthy") or [Zenith](Zenith_\(seed\) "Zenith \(seed\)") world; +3 when enraged. When the counter reaches more than 80, a projectile is fired, then the counter is reset to different values based on the projectile fired: 0 for regular Seed, -30 for Poison Seed, -120 for Thorn Ball. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
591:  6. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, method `AI()` in `Terraria.NPC.cs`. The relevant part is the `aiStyle == 51` block. Internally, a counter which starts at 0 is used to determine whether the Plantera can spawn a Spore. Each tick, the counter is increased by 1; this increment will be further increased by 1 when Plantera's health is under 40%, 30%, 20%, and 10%, respectively. When the counter reaches more than 350, a Spore is spawned, then the counter is reset to 0. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
725:  * [Sea Snail](Sea_Snail.md "Sea Snail")
761:  * [Arapaima](Arapaima.md "Arapaima")
808:  * [Wraith](Wraith.md "Wraith")
839:    * [Tainted](Tainted_Ghoul "Tainted Ghoul")
886:[Rain](Rain.md "Rain")
891:  * [Raincoat Zombie](Raincoat_Zombie.md "Raincoat Zombie")
893:    * [Rainbow](Rainbow_Slime.md "Rainbow Slime")
938:  * [Nailhead](Nailhead.md "Nailhead")
984:  * [Captain](Pirate_Captain.md "Pirate Captain")
986:  * [Corsair](Pirate_Corsair.md "Pirate Corsair")
993:  * [Brain Scrambler](Brain_Scrambler.md "Brain Scrambler")
1049:  * [Brain Suckler](Brain_Suckler.md "Brain Suckler")
1073:  * [](Brain_of_Cthulhu.md "Brain of Cthulhu")[Brain of Cthulhu](Brain_of_Cthulhu.md "Brain of Cthulhu")
1153:  * [Snail](Snail.md "Snail")
1154:    * [Glowing](Glowing_Snail.md "Glowing Snail")
1155:    * [Magma](Magma_Snail.md "Magma Snail")
1193:  * [Fairies](Fairies.md "Fairies")
1217:  * [Zebra Swallowtail](Zebra_Swallowtail_Butterfly.md "Zebra Swallowtail Butterfly")
1231:  * [](Painter.md "Painter")[Painter](Painter.md "Painter")
1275:waiting for rescue](NPCs.md "NPCs")

```


---

## 🤖 Assistant · 2026-08-13T02:12:23.986Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting: the Retinazer.md and Spazmatism.md greps found no infobox — those files appear to be redirects or just different. Let me check the top of those files.

Also I need full infoboxes. Let me read the infobox ranges:
- Wall_of_Flesh.md: lines 20-70 (main), 270-430 (mouth, eyes, hungry, hungry2)
- Skeletron_Prime.md: lines 20-260
- The_Destroyer.md: lines 20-145
- Plantera.md: lines 20-350

For Retinazer and Spazmatism, check the head of the files.
```

</details>


---

## 🤖 Assistant · 2026-08-13T02:12:23.993Z · glm-x-preview-260804

```
Retinazer and Spazmatism don't seem to have infoboxes at the top. Let me inspect those files and read the infobox ranges for the others.
```


---

## 🤖 Assistant · 2026-08-13T02:12:24.135Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "head -40 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Retinazer.md",
 "description": "Show top of Retinazer.md"
}
```


---

## 🤖 Assistant · 2026-08-13T02:12:24.182Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "head -40 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Spazmatism.md",
 "description": "Show top of Spazmatism.md"
}
```


---

## 🤖 Assistant · 2026-08-13T02:12:24.235Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -E \"redirect|Redirect|Twins\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Retinazer.md | head -20",
 "description": "Check if Retinazer.md is a redirect"
}
```


---

## 🤖 Assistant · 2026-08-13T02:12:24.240Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '20,60p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Wall_of_Flesh.md",
 "description": "Read WoF main infobox"
}
```


---

## 🤖 Assistant · 2026-08-13T02:12:24.245Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '270,410p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Wall_of_Flesh.md",
 "description": "Read WoF part infoboxes"
}
```


---

## 🤖 Assistant · 2026-08-13T02:12:24.398Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '20,60p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Skeletron_Prime.md",
 "description": "Read Skeletron Prime head infobox"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:24.502Z

**📎 ToolResult**

```
# Retinazer

> 原页面: `Retinazer`

[Retinazer](./The_Twins#Eyes)
  *[1 required]: Journey Mode
  *[Qty.]: Quantity
  *[100%]: Master Mode
  *[DPS]: Damage per second
  *[sic]: sīc erat scriptum (Latin: “thus it was written”) – any typographical or other errors in this quote are intentionally reproduced, exactly as they appear in the source.
  *[300]: Expert Mode
  *[400]: Expert Mode
  *[160]: Expert Mode
  *[240]: Master Mode
  *[3 required]: Journey Mode
  *[#]: Number
  *[Max.  
enemies]: Maximum number of enemies Abigail can damage at once
  *[HM]: Hardmode
  *[**Click/tap here** to reveal this content. _(there may be a slight delay)_]: This content exists externally. Once you click, there may be a small delay while it is downloaded.
  *[**Klik/tap disini** untuk melihat isi konten. _(mungkin akan sedikit delay)_]: Konten ini tersedia secara eksternal. Ketika di klik, mungkin akan ada sedikit delay ketika melihat isi konten.
  *[**Bấm/Chạm vào đây** để hiển thị nội dung này. _(có thể sẽ bị delay một chút)_]: Nội dung này được lấy từ các nguồn bên ngoài. Khi bấm vào, có thể sẽ bị delay một chút trong khi nó tải.
  *[8]: Expert Mode
  *[10]: Expert Mode
  *[120]: Expert Mode
  *[150]: Expert Mode
  *[13]: Chế độ Master
  *[195]: Master Mode
  *[Verify]: Talk:Re-Logic
  *[50 required]: Journey Mode
  *[0.05 mph]: 0.05 miles per hour (as measured by the Stopwatch item) or 0.04 tiles per second
  *[100 required]: Journey Mode
  *[cần có 1]: Chế độ Journey
  *[25 required]: Journey Mode
  *[cần có 25]: Chế độ Journey
  *[400 required]: Journey Mode
  *[membutuhkan 100]: Mode Journey
  *[cần có 100]: Chế độ Journey
  *[Slg.]: Số lượng
  *[1.99%]: Expert Mode

```


---

## 👤 User(sidechain) · 2026-08-13T02:12:24.504Z

**📎 ToolResult**

```
# Spazmatism

> 原页面: `Spazmatism`

[Spazmatism](./The_Twins#Eyes)
  *[1 required]: Journey Mode
  *[Qty.]: Quantity
  *[100%]: Master Mode
  *[DPS]: Damage per second
  *[sic]: sīc erat scriptum (Latin: “thus it was written”) – any typographical or other errors in this quote are intentionally reproduced, exactly as they appear in the source.
  *[300]: Master Mode
  *[400]: Expert Mode
  *[160]: Expert Mode
  *[240]: Master Mode
  *[3 required]: Journey Mode
  *[#]: Number
  *[Max.  
enemies]: Maximum number of enemies Abigail can damage at once
  *[HM]: Hardmode
  *[**Click/tap here** to reveal this content. _(there may be a slight delay)_]: This content exists externally. Once you click, there may be a small delay while it is downloaded.
  *[**Klik/tap disini** untuk melihat isi konten. _(mungkin akan sedikit delay)_]: Konten ini tersedia secara eksternal. Ketika di klik, mungkin akan ada sedikit delay ketika melihat isi konten.
  *[**Bấm/Chạm vào đây** để hiển thị nội dung này. _(có thể sẽ bị delay một chút)_]: Nội dung này được lấy từ các nguồn bên ngoài. Khi bấm vào, có thể sẽ bị delay một chút trong khi nó tải.
  *[8]: Expert Mode
  *[10]: Expert Mode
  *[120]: Master Mode
  *[150]: Master Mode
  *[13]: Chế độ Master
  *[195]: Master Mode
  *[Verify]: Talk:Social slots
  *[50 required]: Journey Mode
  *[0.05 mph]: 0.05 miles per hour (as measured by the Stopwatch item) or 0.04 tiles per second
  *[100 required]: Journey Mode
  *[cần có 1]: Chế độ Journey
  *[25 required]: Journey Mode
  *[cần có 25]: Chế độ Journey
  *[400 required]: Journey Mode
  *[membutuhkan 100]: Mode Journey
  *[cần có 100]: Chế độ Journey
  *[Slg.]: Số lượng
  *[1.99%]: Expert Mode

```


---

## 👤 User(sidechain) · 2026-08-13T02:12:24.612Z

**📎 ToolResult**

```
5:[Retinazer](./The_Twins#Eyes)

```


---

## 👤 User(sidechain) · 2026-08-13T02:12:24.635Z

**📎 ToolResult**

```
Master

Statistics

Type| [Boss](Boss "Boss")  
---|---  
[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
[AI Type](AI.md "AI")| Skeletron Prime Head AI  
Damage| 47/80/120 (contact)   
94[160](Expert_Mode.md "Expert Mode")[240](Master_Mode.md "Master Mode") (while spinning)[1]  
9999 (during [day](Day "Day"))[1]  
Max Life| 28000/42000/53550  
[Defense](Defense.md "Defense")| 24  
48 (while spinning)[1]  
9999 (during [day](Day "Day"))[1]  
[KB](Knockback.md "Knockback") Resist| 100%  
Immune to| [](Poisoned.md "Poisoned")[](Confused.md "Confused")[](Bone_Javelin.md "Penetrated")[](Blood_Butcherer.md "Blood Butchered")[](Tentacle_Spike.md "Tentacle Spike")[](Bleeding.md "Bleeding")[](Hemorrhage.md "Hemorrhage")  
  
Drops

[Coins](NPC_drops#Coin_drops "NPC drops")| 12 _GC_(Dropped by Treasure Bag[2])  
---|---  
  
  * **Item(Quantity)****Rate**
  * [](Soul_of_Fright.md "Soul of Fright")[Soul of Fright](Soul_of_Fright.md "Soul of Fright") (25–40)

100%

  * [](Hallowed_Bar.md "Hallowed Bar")[Hallowed Bar](Hallowed_Bar.md "Hallowed Bar") (15–30)

100%

  * [](Greater_Healing_Potion.md "Greater Healing Potion")[Greater Healing Potion](Greater_Healing_Potion.md "Greater Healing Potion") (5–15)

100%

  * [](Skeletron_Prime_Mask.md "Skeletron Prime Mask")[Skeletron Prime Mask](Skeletron_Prime_Mask.md "Skeletron Prime Mask")

14.29%

  * [](Skeletron_Prime_Trophy "Skeletron Prime Trophy")[Skeletron Prime Trophy](Skeletron_Prime_Trophy "Skeletron Prime Trophy")

```


---

## 👤 User(sidechain) · 2026-08-13T02:12:24.639Z

**📎 ToolResult**

```
Master

Statistics

Type| [Boss](Boss "Boss")  
---|---  
[Environment](Environment "Environment")| [ The Underworld ](The_Underworld.md "The Underworld")  
[AI Type](AI.md "AI")| Wall of Flesh AI  
Damage| 50/150/225  
Max Life| 8000/11200/14280  
[Defense](Defense.md "Defense")| 12/18  
[KB](Knockback.md "Knockback") Resist| 100%  
Immune to| [](On_Fire!.md "On Fire!")[](Confused.md "Confused")[](Hellfire.md "Hellfire")  
  
Drops

[Coins](NPC_drops#Coin_drops "NPC drops")| 8 _GC_ 20 _GC_  
---|---  
  
Sounds

Hurt|   
---|---  
Killed|   
Summon   
Leech|   
  
  * Internal [NPC ID](NPC_IDs.md "NPC IDs"): **113**

Wall of FleshWall of Flesh Eye

Classic

Expert

Master

Statistics

Type| [Boss](Boss "Boss")  
---|---  
[Environment](Environment "Environment")| [ The Underworld ](The_Underworld.md "The Underworld")  
[AI Type](AI.md "AI")| Wall of Flesh Eye AI  
Damage| 50/150/225 (contact)  
22–30[44–60](Expert_Mode.md "Expert Mode")[66–90](Master_Mode.md "Master Mode") (Eye Laser; depending on health)  
Max Life| 8000/11200/14280  
[Defense](Defense.md "Defense")| 0/6  
[KB](Knockback.md "Knockback") Resist| 100%  
Immune to| [](On_Fire!.md "On Fire!")[](Confused.md "Confused")[](Hellfire.md "Hellfire")  
  
Drops

[Coins](NPC_drops#Coin_drops "NPC drops")| 8 _GC_ 20 _GC_  
---|---  
  
Projectile created

Projectile created

Projectile created

  * Eye Laser

Sounds

Hurt|   
---|---  
Killed|   
Eye Laser|   
  
  * Internal [NPC ID](NPC_IDs.md "NPC IDs"): **114**
  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **83**

The Hungry

Classic

Expert

Master

Statistics

Type| [Enemy](Enemy "Enemy")  
---|---  
[Environment](Environment "Environment")| [ The Underworld ](The_Underworld.md "The Underworld")  
[AI Type](AI.md "AI")| The Hungry AI  
Damage| 30/60/90 (WoF health >75%)  
45[90](Expert_Mode.md "Expert Mode")[135](Master_Mode.md "Master Mode") (WoF health 75–50%)  
60[120](Expert_Mode.md "Expert Mode")[180](Master_Mode.md "Master Mode") (WoF health <50%)  
  
Max Life| 240/336/504  
[Defense](Defense.md "Defense")| 10/16 (WoF health >75%)  
20 (WoF health 75–50%)  
30 (WoF health <50%)  
  
[KB](Knockback.md "Knockback") Resist| −10%/1%/12%[ (1 player)  
57% (2 players)  
71% (3 players)  
81% (4 players)  
100% (5 players or more)  
](Expert_Mode.md "Expert Mode")[ (1 player)  
62% (2 players)  
75% (3 players)  
83% (4 players)  
100% (5 players or more)  
](Master_Mode.md "Master Mode")  
Immune to| [](Confused.md "Confused")[](Shimmering.md "Shimmering")  
  
Sounds

Hurt|   
---|---  
Killed|   
  
  * Internal [NPC ID](NPC_IDs.md "NPC IDs"): **115**

The HungryThe Hungry II

Classic

Expert

Master

Statistics

Type| [Flying Enemy](Flying_Enemy "Flying Enemy")  
---|---  
[Environment](Environment "Environment")| [ The Underworld ](The_Underworld.md "The Underworld")  
[AI Type](AI.md "AI")| Demon Eye AI  
Damage| 30/60/90  
Max Life| 80/112/168  
[Defense](Defense.md "Defense")| 6  
[KB](Knockback.md "Knockback") Resist| 20%/28%/36%[ (1 player)  
69% (2 players)  
79% (3 players)  
86% (4 players)  
100% (5 players or more)  
](Expert_Mode.md "Expert Mode")[ (1 player)  
72% (2 players)

```


---

## 👤 User(sidechain) · 2026-08-13T02:12:24.640Z

**📎 ToolResult**

```
Master

Statistics

Type| [Boss](Boss "Boss")  
---|---  
[Environment](Environment "Environment")| [ The Underworld ](The_Underworld.md "The Underworld")  
[AI Type](AI.md "AI")| Wall of Flesh AI  
Max Life| 8000/11200/14280  
[KB](Knockback.md "Knockback") Resist| 100%  
Immune to| [](On_Fire!.md "On Fire!")[](Confused.md "Confused")[](Hellfire.md "Hellfire")  
  
Inflicts [ debuffs ](Debuffs.md "Debuffs")

Inflicts [ debuffs ](Debuffs.md "Debuffs")

Inflicts [ debuffs ](Debuffs.md "Debuffs")

Debuff| [](Wall_of_Flesh.md "Horrified")Horrified  
---|---  
Debuff tooltip|  _You have seen something nasty, there is no escape._  
Duration| While the player is within 120 tiles from the boss.  
  
Debuff| [](The_Tongue.md "The Tongue")[The Tongue](The_Tongue.md "The Tongue")  
---|---  
Debuff tooltip|  _You are being sucked into the mouth_  
Duration| While the player is inflicted with Horrified: when the player leaves The Underworld, or is more than 2.5 tiles behind the boss.  
  
Drops

[Coins](NPC_drops#Coin_drops "NPC drops")| 8 _GC_(Dropped by Treasure Bag[1])  
---|---  
  
  * **Item(Quantity)****Rate**
  * [](Pwnhammer.md "Pwnhammer")[Pwnhammer](Pwnhammer.md "Pwnhammer")

100%

  * Two (see the notes below) of the following 8 items will always be dropped
  * One of the following 4 weapons will always be dropped

```


---

## 🤖 Assistant · 2026-08-13T02:12:24.675Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '130,260p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Skeletron_Prime.md",
 "description": "Read Skeletron Prime part infoboxes"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:24.725Z

**📎 ToolResult**

```
Master

Statistics

Type| Boss Part  
---|---  
[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
[AI Type](AI.md "AI")| Prime Cannon AI  
Damage| 30/51/76 (contact)  
80[160](Expert_Mode.md "Expert Mode")[240](Master_Mode.md "Master Mode") (Bomb)[3]  
Max Life| 7000/10500/13387  
[Defense](Defense.md "Defense")| 23  
[KB](Knockback.md "Knockback") Resist| 100%  
Immune to| [](Bleeding.md "Bleeding")[](Confused.md "Confused")[](Poisoned.md "Poisoned")[](Hemorrhage.md "Hemorrhage")  
  
Projectile created

Projectile created

Projectile created

  * Skeletron Prime Bomb

Sounds

Hurt|   
---|---  
Killed|   
Bomb launch|   
Bomb explosion|   
  
  * Internal [NPC ID](NPC_IDs.md "NPC IDs"): **128**
  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **102**

Prime Saw

Classic

Expert

Master

Statistics

Type| Boss Part  
---|---  
[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
[AI Type](AI.md "AI")| Prime Saw AI  
Damage| 56/95/143  
Max Life| 9000/13500/17212  
[Defense](Defense.md "Defense")| 38  
[KB](Knockback.md "Knockback") Resist| 100%  
Immune to| [](Bleeding.md "Bleeding")[](Confused.md "Confused")[](Poisoned.md "Poisoned")[](Hemorrhage.md "Hemorrhage")  
  
Sounds

Hurt|   
---|---  
Killed|   
  
  * Internal [NPC ID](NPC_IDs.md "NPC IDs"): **129**

Prime Vice

Classic

Expert

Master

Statistics

Type| Boss Part  
---|---  
[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
[AI Type](AI.md "AI")| Prime Vice AI  
Damage| 52/88/133  
Max Life| 9000/13500/17212  
[Defense](Defense.md "Defense")| 34  
[KB](Knockback.md "Knockback") Resist| 100%  
Immune to| [](Bleeding.md "Bleeding")[](Confused.md "Confused")[](Poisoned.md "Poisoned")[](Hemorrhage.md "Hemorrhage")  
  
Sounds

Hurt|   
---|---  
Killed|   
  
  * Internal [NPC ID](NPC_IDs.md "NPC IDs"): **130**

Prime Laser

Classic

Expert

Master

Statistics

Type| Boss Part  
---|---  
[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
[AI Type](AI.md "AI")| Prime Laser AI  
Damage| 29/49/74 (contact)  
50[100](Expert_Mode.md "Expert Mode")[150](Master_Mode.md "Master Mode") (Death Laser)[4]  
Max Life| 6000/9000/11475  
[Defense](Defense.md "Defense")| 20  
[KB](Knockback.md "Knockback") Resist| 100%  
Immune to| [](Bleeding.md "Bleeding")[](Confused.md "Confused")[](Poisoned.md "Poisoned")[](Hemorrhage.md "Hemorrhage")  
  
Projectile created

Projectile created

Projectile created

  * Death Laser

Sounds

Hurt|   
---|---  
Killed|   
Attack|   
  
  * Internal [NPC ID](NPC_IDs.md "NPC IDs"): **131**
  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **100**

## Behavior

```


---

## 🤖 Assistant · 2026-08-13T02:12:25.042Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '20,160p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Destroyer.md",
 "description": "Read Destroyer infobox and stat table"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:25.087Z

**📎 ToolResult**

```
Master

Statistics

Type| [Boss](Boss "Boss")[Burrowing Enemy](Burrowing_Enemy "Burrowing Enemy")  
---|---  
[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
[AI Type](AI.md "AI")| The Destroyer AI  
Max Life| 80000/120000/153000  
[KB](Knockback.md "Knockback") Resist| 100%  
Immune to| **All[debuffs](Debuffs.md "Debuffs") except [whip debuffs](Whip_debuffs.md "Whip debuffs")**  
  
Drops

[Coins](NPC_drops#Coin_drops "NPC drops")| 12 _GC_(Dropped by Treasure Bag[1])  
---|---  
  
  * **Item(Quantity)****Rate**
  * [](Soul_of_Might.md "Soul of Might")[Soul of Might](Soul_of_Might.md "Soul of Might") (25–40)

100%

  * [](Hallowed_Bar.md "Hallowed Bar")[Hallowed Bar](Hallowed_Bar.md "Hallowed Bar") (15–30)

100%

  * [](Greater_Healing_Potion.md "Greater Healing Potion")[Greater Healing Potion](Greater_Healing_Potion.md "Greater Healing Potion") (5–15)

100%

  * [](Destroyer_Mask.md "Destroyer Mask")[Destroyer Mask](Destroyer_Mask.md "Destroyer Mask")

14.29%

  * [](Destroyer_Trophy "Destroyer Trophy")[Destroyer Trophy](Destroyer_Trophy "Destroyer Trophy")

10%

  * [](Treasure_Bag_\(The_Destroyer\) "Treasure Bag \(The Destroyer\)")[Treasure Bag](Treasure_Bag_\(The_Destroyer\) "Treasure Bag \(The Destroyer\)")(The Destroyer)

[100%](Expert_Mode.md "Expert Mode")

  *   * [](Mechanical_Wagon_Piece.md "Mechanical Wagon Piece")[Mechanical Wagon Piece](Mechanical_Wagon_Piece.md "Mechanical Wagon Piece")

100%

  * [](Destroyer_Mask.md "Destroyer Mask")[Destroyer Mask](Destroyer_Mask.md "Destroyer Mask")

14.29%

  * [](Soul_of_Might.md "Soul of Might")[Soul of Might](Soul_of_Might.md "Soul of Might") (25–40)

100%

  * [](Hallowed_Bar.md "Hallowed Bar")[Hallowed Bar](Hallowed_Bar.md "Hallowed Bar") (20–35)

100%

  * [Coins](Coins.md "Coins") ([30 _GC_](NPC_drops#Coin_drops "NPC drops"))

100%

  *   * [](Deactivated_Probe.md "Deactivated Probe")[Deactivated Probe](Deactivated_Probe.md "Deactivated Probe")

[25%](Master_Mode.md "Master Mode")

  * [](Destroyer_Relic "Destroyer Relic")[Destroyer Relic](Destroyer_Relic "Destroyer Relic")

[100%](Master_Mode.md "Master Mode")

Projectile created

Projectile created

Projectile created

  * Death Laser

Sounds

Hurt|   
---|---  
Killed|   
Spawn|   
Death Laser|   
  
  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **100**

 _“ You feel vibrations from deep below...”_

"Destroyer" redirects here. For other uses, see [Destroyer (disambiguation)](Destroyer_\(disambiguation\) "Destroyer \(disambiguation\)").

**The Destroyer** is a [Hardmode](Hardmode.md "Hardmode") [mechanical boss](Mechanical_boss "Mechanical boss") that is essentially a more difficult version of the [Eater of Worlds](Eater_of_Worlds.md "Eater of Worlds"). Its segments share a single health pool, meaning individual segments cannot die. Each of The Destroyer's segments fires lasers at the player, and as they take damage, they launch [](Probe.md "Probe")[Probes](Probe.md "Probe"), independent [flying enemies](Flying_enemies.md "Flying enemies") that fire lasers and can be killed individually. 

While The Destroyer is alive, its exclusive music [The Destroyer](Music#The_Destroyer "Music") will play. When [Otherworldly music](Party_Girl#Music_toggle "Party Girl") is enabled, the track [Boss 2 (Otherworldly)](Music#Boss_2_\(Otherworldly\) "Music") will play instead. 

## Summoning and spawning

The Destroyer can be summoned manually using a [Mechanical Worm](Mechanical_Worm.md "Mechanical Worm") at [night](Night "Night") (7:30 PM to 4:30 AM). 

It also has a 1/10 (10%) chance to spawn naturally at dusk (7:30 PM) during Hardmode once a [Demon or Crimson Altar](Altars.md "Altars") has been destroyed, as long as it has not been defeated. When spawning naturally, its arrival is announced by the [status message](Status_message "Status message") _" You feel vibrations from deep below..."_. 

The Destroyer must be killed before dawn (4:30 AM), otherwise it flees and despawns. 

## Segments

See also: [Probe](Probe.md "Probe")

Classic

Expert

Master

2 values: Pre-Hardmode › Hardmode  
3 values: Pre-Hardmode › Hardmode › Post-Plantera

[NPC ID](NPC_IDs.md "NPC IDs") | Type  | Damage  | Defense   
---|---|---|---  
134  |  | The Destroyer Head | 70/280/420 | 0  
135  |  | The Destroyer Body | 55/94/140 (contact)  
44[72](Expert_Mode.md "Expert Mode")[108](Master_Mode.md "Master Mode") (Death Laser [2]) | 30  
136  |  | The Destroyer Tail | 40/68/102 | 35  
  
## Behavior

The Destroyer spawns coiled up, like most worm enemies, and immediately starts uncoiling and following the player. It has limited mobility when fully in the air, requiring [blocks](Blocks.md "Blocks") or [platforms](Platforms.md "Platforms") to "burrow" through. However, it is able to move freely while off-screen. It follows the player from any distance and will only despawn if the player dies or if dawn comes (4:30 AM). It despawns by quickly traveling underground until off-screen. 

The Destroyer performs the following attacks: 

  * It leaps from the ground and attempts to ram the player.
  * It attempts to surround the player with its segments.
  * It fires red Death Lasers from its segments which deal 44 / [72](Expert_Mode.md "Expert Mode") / [108](Master_Mode.md "Master Mode") damage.[2]
  * It releases flying [](Probe.md "Probe")[Probes](Probe.md "Probe") from its body that fire Pink Lasers which deal 50 / [88](Expert_Mode.md "Expert Mode") / [132](Master_Mode.md "Master Mode") damage.[3]

Each body segment has a 1/25 (4%) chance to release a Probe whenever it is damaged. This only happens once per segment and is signified by the red light on the segment turning off.[4] Probes will fly towards the player, attempting to maintain a distance while occasionally moving into melee range. They fire lasers with moderate accuracy. 

  * Probes never return to the main body, and will not despawn as long as The Destroyer is alive, even if the player goes too far away.[5]
  * Killing the boss itself does not destroy the remaining Probes, and they will still continue to attack the player afterwards.
  * Since each body segment can only spawn one Probe, The Destroyer will eventually run out of Probes to spawn.[2]
  * Dim segments still fire lasers like normal.[2]

```


---

## 🤖 Assistant · 2026-08-13T02:12:25.345Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '20,110p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Plantera.md",
 "description": "Read Plantera infoboxes"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:25.389Z

**📎 ToolResult**

```
Master

Statistics

Type| [Boss](Boss "Boss")  
---|---  
[Environment](Environment "Environment")| [ Underground Jungle ](Underground_Jungle.md "Underground Jungle")  
[AI Type](AI.md "AI")| Plantera AI  
Damage| 50[100](Expert_Mode.md "Expert Mode")[150](Master_Mode.md "Master Mode") (contact) [1]  
44[76](Expert_Mode.md "Expert Mode")[114](Master_Mode.md "Master Mode") (Seed)  
54[96](Expert_Mode.md "Expert Mode")[144](Master_Mode.md "Master Mode") (Poison Seed)  
62[108](Expert_Mode.md "Expert Mode")[162](Master_Mode.md "Master Mode") (Thorn Ball)  
Max Life| 30000[42000](Expert_Mode.md "Expert Mode")[53550](Master_Mode.md "Master Mode")  
[Defense](Defense.md "Defense")| 36 [1]  
[KB](Knockback.md "Knockback") Resist| 100%  
Immune to| [](Bleeding.md "Bleeding")[](Confused.md "Confused")[](Poisoned.md "Poisoned")[](Hemorrhage.md "Hemorrhage")  
  
Inflicts [ debuff ](Debuffs.md "Debuffs")

Inflicts [ debuff ](Debuffs.md "Debuffs")

Inflicts [ debuff ](Debuffs.md "Debuffs")

Debuff| [](Poisoned.md "Poisoned")[Poisoned](Poisoned.md "Poisoned")  
---|---  
Debuff tooltip|  _Slowly losing life_  
Chance| 50%[100%](Expert_Mode.md "Expert Mode") (Poison Seed)  
Duration| 3–7 seconds[4–18 seconds](Expert_Mode.md "Expert Mode")[5–22.5 seconds](Master_Mode.md "Master Mode")  
  
Projectiles created

Projectiles created

Projectiles created

  * Seed

  * Poison Seed

  * Thorn Ball

Sounds

Hurt|   
---|---  
Killed|   
Fires projectile|   
  
  * Internal [NPC ID](NPC_IDs.md "NPC IDs"): **262**
  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **20**
  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **275** , **276** , **277**

PlanteraSecond FormHardmode exclusive

** _Map icon_**

Classic

Expert

Master

Statistics

Type| [Boss](Boss "Boss")  
---|---  
[Environment](Environment "Environment")| [ Underground Jungle ](Underground_Jungle.md "Underground Jungle")  
[AI Type](AI.md "AI")| Plantera AI  
Damage| 70[140](Expert_Mode.md "Expert Mode")[210](Master_Mode.md "Master Mode") [1]  
Max Life| 15000/30000[21000/42000](Expert_Mode.md "Expert Mode")[26775/53550](Master_Mode.md "Master Mode")  
[Defense](Defense.md "Defense")| 10 [1]  
[KB](Knockback.md "Knockback") Resist| 100%  
Immune to| [](Confused.md "Confused")[](Poisoned.md "Poisoned")  
  
Drops

[Coins](NPC_drops#Coin_drops "NPC drops")| 15 _GC_(Dropped by Treasure Bag[2])  
---|---  
  
  * **Item(Quantity)****Rate**
  * [](Temple_Key.md "Temple Key")[Temple Key](Temple_Key.md "Temple Key")

100%

  * One of the following 8 items will always be dropped [3][4]
  * [](Grenade_Launcher.md "Grenade Launcher")[Grenade Launcher](Grenade_Launcher.md "Grenade Launcher")

    \+ [](Rocket_I "Rocket I")[Rocket I](Rocket_I "Rocket I") (50–149)

(will always drop the first time Plantera is defeated in a world that is neither in Expert nor Master Mode)

```


---

## 🤖 Assistant · 2026-08-13T02:12:25.710Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '280,350p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Plantera.md",
 "description": "Read Plantera hook and tentacle infoboxes"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:25.771Z

**📎 ToolResult**

```
Expert

Master

Statistics

Type| Boss PartInvincible  
---|---  
[Environment](Environment "Environment")| [ Underground Jungle ](Underground_Jungle.md "Underground Jungle")  
[AI Type](AI.md "AI")| Plantera's Hook AI  
Damage| 60/120/180  
Max Life| 4000/8000/12000  
[Defense](Defense.md "Defense")| 24  
[KB](Knockback.md "Knockback") Resist| 0%/10%/20%  
  
Sounds

Hurt|   
---|---  
Killed|   
  
  * Internal [NPC ID](NPC_IDs.md "NPC IDs"): **263**

Plantera's Tentacle

Classic

Expert

Master

Statistics

Type| Boss Part  
---|---  
[Environment](Environment "Environment")| [ Underground Jungle ](Underground_Jungle.md "Underground Jungle")  
[AI Type](AI.md "AI")| Plantera's Tentacle AI  
Damage| 60/138/207  
Max Life| 1000/2000/2550  
[Defense](Defense.md "Defense")| 20  
[KB](Knockback.md "Knockback") Resist| 0%/10%/20%  
Immune to| [](Bleeding.md "Bleeding")[](Confused.md "Confused")[](Poisoned.md "Poisoned")[](Hemorrhage.md "Hemorrhage")  
  
Sounds

Hurt|   
---|---  
Killed|   
  
  * Internal [NPC ID](NPC_IDs.md "NPC IDs"): **264**

Spore

Classic

Expert

Master

Statistics

Type| [Projectile NPC](Projectile_NPC "Projectile NPC")  
---|---  
[Environment](Environment "Environment")| [ Underground Jungle ](Underground_Jungle.md "Underground Jungle")  
[AI Type](AI.md "AI")| Spore AI  
Damage| 70/140›126/210›189  
Max Life| 1  
[Defense](Defense.md "Defense")| 0  
[KB](Knockback.md "Knockback") Resist| 100%  
Immune to| [](Confused.md "Confused")

```


---

## 🤖 Assistant · 2026-08-13T02:12:29.812Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Retinazer.md and Spazmatism.md are stub redirect pages pointing to ./The_Twins#Eyes. I need to get the eye data from The_Twins.md. Let me check that file.

Also I still need:
- Wall of Flesh: Hungry II remaining KB lines, behavior details (speed phases, despawn behavior). Also the main body damage line wasn't in the first sed (it was lines 20-60, the "Damage" row for main body appears between Max Life... actually main infobox at line 274-280 in second sed shows Damage| 50/150/225. Wait the first sed output shows the first infobox which lacks Damage and Defense rows — it seems the page has two infobox variants (one collapsed). Fine.
- WoF behavior section: lines 206-260 for phase/despawn behavior.
- Twins page for Retinazer/Spazmatism infoboxes and 40% threshold.

Let me grep The_Twins.md.
```

</details>


---

## 🤖 Assistant · 2026-08-13T02:12:30.316Z · glm-x-preview-260804

```
Retinazer and Spazmatism are redirect stubs pointing to The_Twins. Let me get the eye data from The_Twins.md and the behavior sections for WoF, Skeletron Prime, Destroyer, Plantera.
```


---

## 🤖 Assistant · 2026-08-13T02:12:31.036Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"Max Life|KB.*Resist|AI Type|^Type\\||Damage\\|\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Twins.md | head -50",
 "description": "Find infobox markers in The_Twins.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:31.246Z

**📎 ToolResult**

```
22:Type| [Boss](Boss "Boss")  
25:Max Life| 43000[64500](Expert_Mode.md "Expert Mode")[82238](Master_Mode.md "Master Mode") (total)  
27:[KB](Knockback.md "Knockback") Resist| 100%  
122:Type| [Boss](Boss "Boss")  
125:[AI Type](AI.md "AI")| Retinazer AI  
126:Damage| 45/76/115 (contact)  
128:Max Life| 20000/30000/38250  
130:[KB](Knockback.md "Knockback") Resist| 100%  
169:Type| [Boss](Boss "Boss")  
172:[AI Type](AI.md "AI")| Spazmatism AI  
173:Damage| 50/85/128 (contact)  
175:Max Life| 23000/34500/43988  
177:[KB](Knockback.md "Knockback") Resist| 100%  
229:Type| [Boss](Boss "Boss")  
232:[AI Type](AI.md "AI")| Retinazer AI  
233:Damage| 67[114](Expert_Mode.md "Expert Mode")[172](Master_Mode.md "Master Mode") (contact)  
236:Max Life| 8000/20000[12000/30000](Expert_Mode.md "Expert Mode")[15300/38250](Master_Mode.md "Master Mode") [4]  
238:[KB](Knockback.md "Knockback") Resist| 100%  
281:Type| [Boss](Boss "Boss")  
284:[AI Type](AI.md "AI")| Spazmatism AI  
285:Damage| 75[127](Expert_Mode.md "Expert Mode")[192](Master_Mode.md "Master Mode") (contact)  
287:Max Life| 9200/23000[13800/34500](Expert_Mode.md "Expert Mode")[17595/43988](Master_Mode.md "Master Mode") [2]  
289:[KB](Knockback.md "Knockback") Resist| 100%

```


---

## 🤖 Assistant · 2026-08-13T02:12:31.739Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"40%|transform|second form|Spazmatism|Retinazer|dawn|despawn|flee\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Twins.md | head -40",
 "description": "Find phase and despawn info in The_Twins.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:31.867Z

**📎 ToolResult**

```
94:**The Twins** are a [Hardmode](Hardmode.md "Hardmode") [mechanical boss](Mechanical_bosses.md "Mechanical bosses") which are essentially a more difficult version of the [Eye of Cthulhu](Eye_of_Cthulhu.md "Eye of Cthulhu"). The Twins are two separate flying entities, **Retinazer** and **Spazmatism** , connected by a tendril, each with its own attack pattern and health. Both must be killed in order to defeat the boss. 
104:The Twins must be killed before dawn (4:30 AM), otherwise they flee and despawn. 
108:There are two eyes: Retinazer and Spazmatism. Retinazer is a laser-shooting eye with a red iris, while Spazmatism is an eye with a green iris that shoots Cursed Flames. 
110:RetinazerFirst Form
125:[AI Type](AI.md "AI")| Retinazer AI  
157:SpazmatismFirst Form
172:[AI Type](AI.md "AI")| Spazmatism AI  
217:RetinazerSecond Form
232:[AI Type](AI.md "AI")| Retinazer AI  
247:  * [](Retinazer_Trophy "Retinazer Trophy")[Retinazer Trophy](Retinazer_Trophy "Retinazer Trophy")
269:SpazmatismSecond Form
284:[AI Type](AI.md "AI")| Spazmatism AI  
310:  * [](Spazmatism_Trophy "Spazmatism Trophy")[Spazmatism Trophy](Spazmatism_Trophy "Spazmatism Trophy")
338:  * The eyeball with the red iris, Retinazer, fires purple, high-velocity Eye Lasers at low accuracy when close enough to the player. It will usually attempt to remain diagonally above the player, but moves slower compared to Spazmatism.
339:  * The eyeball with the green iris, Spazmatism, fires green balls of Cursed Flames, which have a 11/16 (68.75%) chance of inflicting the [Cursed Inferno](Cursed_Inferno.md "Cursed Inferno") [debuff](Debuff "Debuff") for 2–3 / [4–6](Expert_Mode.md "Expert Mode") / [5–7.5](Master_Mode.md "Master Mode") seconds. It will usually attempt to remain horizontally in line with the player.
341:Both eyes alternate between their signature ranged attacks and charging attacks, much like the [Eye of Cthulhu](Eye_of_Cthulhu.md "Eye of Cthulhu"). Retinazer charges four times while traveling much greater distances than Spazmatism at the expense of longer periods in between charges, while Spazmatism charges ten times within quick, high-velocity bursts that cover shorter distances. 
345:When one of the eyes' health dips below 40%, it spins before transitioning into its second form, casting off its retina to reveal its true mechanical appearance before beginning to attack the player after a few seconds. Retinazer transforms at 8,000 / [12,000](Expert_Mode.md "Expert Mode") / [15,300](Master_Mode.md "Master Mode") health while Spazmatism transforms at 9,200 / [13,800](Expert_Mode.md "Expert Mode") / [17,595](Master_Mode.md "Master Mode") health. During their second phase, the defense of each eye is also increased to 20 and 28 for Retinazer and Spazmatism respectively. 
347:  * Retinazer becomes a mechanical eye with a laser cannon in its pupil and now only fires red Death Lasers, ceasing its attempts to ram the player (or align with the player diagonally). It fires at a higher rate, with more damage, and at pinpoint accuracy, periodically switching to a quick barrage with considerably less damage. Both normal and burst lasers are fired more quickly as its health is depleted, leading to a near-constant stream of them near the end. 
348:    * Retinazer _will_ , however, align horizontally with the player when firing barrages, though not as tightly as first-phase Spazmatism does. When not barraging, Retinazer will usually align itself vertically with the player from above.
349:  * Spazmatism becomes a mechanical mouth (similar to the Eye of Cthulhu's second phase) that continuously pursues the player. It alternates between charging at the player six times with increased speed and range, and spewing Eye Fire from its mouth in the form of a continuous stream of Cursed Flames while slowly approaching the player for approximately seven seconds, in a manner similar to the [Flamethrower](Flamethrower.md "Flamethrower"). The stream of Cursed Flames also has a 11/16 (68.75%) chance of inflicting the [Cursed Inferno](Cursed_Inferno.md "Cursed Inferno") [debuff](Debuffs.md "Debuffs") for 2–3 / [4–6](Expert_Mode.md "Expert Mode") / [5–7.5](Master_Mode.md "Master Mode") seconds. Spazmatism no longer attempts to align itself horizontally with the player.
351:In [Expert Mode](Expert_Mode.md "Expert Mode"), both eyes fire faster and charge greater distances in their first phases as their health is depleted, and their Cursed Flame and Eye Laser projectiles have a 16.67% higher velocity. In their second phases, Retinazer's barrages scale much more aggressively with health and its slower Death Laser barrages have a 17.65% higher velocity, and Spazmatism has a much shorter delay between individual charges. 
369:  * In single player The Twins can only despawn if both of their despawn timers reach 0 at the same time, which causes them to despawn together. In multiplayer, however, it is possible for them to despawn separately. 
370:    * This can be exploited by timing 2 players' deaths such that one twin despawns, then a player respawns, allowing for an easier battle with only one twin.
402:  * Focus on defeating one eye completely first without inflicting too much damage on the other one. Battling The Twins while both are in their second form makes the battle much more difficult, especially in [Expert Mode](Expert_Mode.md "Expert Mode"). 
403:    * Spazmatism may be a better choice for defeating first, since its Cursed Flames are difficult to avoid without proper mobility equipment and [buffs](Buffs.md "Buffs") in its second phase. Retinazer is less deadly, as it cannot inflict [debuffs](Debuffs.md "Debuffs") and will not charge in its second phase, which helps the player attack it from a safe distance with ranged attacks.
404:    * In its first phase, Retinazer's accuracy is low enough that it will simply miss most shots against a stationary player. If Spazmatism is already defeated, even moderately tanky builds can maximize DPS for less effort by staying put, except to dodge charges.
407:  * In its second phase, Retinazer can only attack the player if it has an unobstructed line of sight. Hiding in a box prevents it from dealing any damage.
412:  * Retinazer's name is a [portmanteau](https://en.wikipedia.org/wiki/en:portmanteau "wikipedia:en:portmanteau") of _[retina](https://en.wikipedia.org/wiki/en:retina "wikipedia:en:retina")_ , a part of the eye, and _[laser](https://en.wikipedia.org/wiki/en:laser "wikipedia:en:laser")_. Spazmatism's name is a portmanteau of _[spasm](https://en.wikipedia.org/wiki/en:spasm "wikipedia:en:spasm")_ , meaning to twitch uncontrollably, and _[astigmatism](https://en.wikipedia.org/wiki/en:astigmatism "wikipedia:en:astigmatism")_ , an eye disorder that creates blurry or distorted vision.
413:  * Spazmatism's second form has visible bolts along either side, whereas Retinazer's second form only has them along one side.
416:  * Despite inflicting it, Spazmatism is not immune to Cursed Inferno.
419:  * The Twins seem to be bio-mechanical hybrids since they are not immune to debuffs like [On Fire!](On_Fire!.md "On Fire!"), [Cursed Inferno](Cursed_Inferno.md "Cursed Inferno"), or [Acid Venom](Acid_Venom.md "Acid Venom"), even when transformed.
420:  * The Twins make an appearance in _[Don't Starve Together](Don't_Starve_Together.md "Don't Starve Together")_ as the [Twins of Terror](https://dontstarve.wiki.gg/wiki/Eye_of_Terror#Twins_of_Terror "dts:Eye of Terror"), the harder version of the original Eye of Terror. However, unlike in _[Terraria](Terraria.md "Terraria")_ , Retinazer is known as "Retinazor," they can both spawn minions, do not fire any projectiles, and can charge towards players in both phases.
424:  * Retinazer: _" Belonging to a pair of mechanically recreated Eyes of Cthulhu, this one focuses its energy into firing powerful lasers."_
425:  * Spazmatism: _" Belonging to a pair of mechanically recreated Eyes of Cthulhu, this one chases at high speed, exhaling cursed flames."_
442:    * The Twins now use their map icons correctly. Before this, Retinazer used both first phase icons while Spazmatism used both second phase icons.
443:    * Decreased Spazmatism's Cursed Inferno duration to compensate for increased Cursed Inferno DPS. The debuff can now last for 3 / [6](Expert_Mode.md "Expert Mode") / [7.5](Master_Mode.md "Master Mode") seconds (chance of 6/16 (37.5%)), 2 / [4](Expert_Mode.md "Expert Mode") / [5](Master_Mode.md "Master Mode") seconds (5/16 (31.25%)), or not be inflicted at all (5/16 (31.25%)). Previous durations were 8 / [16](Expert_Mode.md "Expert Mode") seconds (chance of 8/48 (16.67%)), 5 / [10](Expert_Mode.md "Expert Mode") seconds (10/48 (20.83%)), 3 / [6](Expert_Mode.md "Expert Mode") seconds (15/48 (31.25%)), or not being inflicted at all (15/48 (31.25%)).
447:    * Old sprites for Retinazer were:  .
448:    * Old sprites for Spazmatism were:  .
453:    * Increased Spazmatism's health to 23,000, decreased damage for both.
454:    * The Twins now transform at 2/5th HP, instead of at half HP.

```


---

## 🤖 Assistant · 2026-08-13T02:12:31.991Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '206,262p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Wall_of_Flesh.md",
 "description": "Read WoF behavior section"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:32.053Z

**📎 ToolResult**

```
### Technical details

When the Guide Voodoo Doll is destroyed or the Guide is killed in lava, the game checks whether all players are horizontally at least 75 tiles away from the location of the doll/Guide. If they are, then the Wall of Flesh is spawned at that horizontal position. Otherwise, the game moves one tile towards the closest lateral [world border](World_border.md "World border") and checks again, repeating this until it encounters a tile that is horizontally at least 75 tiles away from any player. It stops 20 tiles before the true world border (i.e. 21/22 tiles away from the visible world border), even if a player is still within 75 tiles at that point (e.g. standing directly against the visible world border). 

After locating the horizontal spawn position, the game determines a valid vertical position. The spawning tile must not be occupied by a solid block and its liquid level must not exceed 100 (i.e. at most approx. 39% of the tile can contain liquid). Again, the game begins at the vertical position of the doll/Guide and checks if that location is valid. Then it checks one tile above that spot and one tile below it, then two tiles above and two tiles below, and so on, until finding a valid spot. If the game finds no valid spot after 1000 attempts (i.e. 1000 tiles above and below), then it reverts to the initial vertical position. Finally, the vertical limits are enforced: If the vertical position that was encountered is higher than 10 tiles below the [Cavern](Cavern.md "Cavern")–Underworld border, it is forcibly moved down to that position (even though the tile there was not considered valid before), and if it is lower than 80 tiles below that border (roughly the vertical center of the Underworld), it is forcibly moved up to that position (again, even though the tile at that position was not considered valid before). 

The center of the Wall of Flesh's mouth appears at the determined location, and the eyes are spawned relative to it. The boss quickly aligns itself vertically with the player after spawning. 

## Behavior

The Wall of Flesh is very tall, occupying the entire screen vertically. It slowly sweeps across the Underworld in a single direction, forcing the player to constantly move away for the duration of the fight while also contending with the Underworld's usual hazards. 

When the Wall of Flesh is alive, all players near the Underworld[a] and less than 120 tiles from the Wall of Flesh are inflicted with the **Horrified** [debuff](Debuffs.md "Debuffs"). The debuff is constantly inflicted as long as the Wall of Flesh exists. Once inflicted, it lasts until either the player or the Wall of Flesh dies. This debuff is mostly used for determining whether The Tongue debuff can be inflicted. 

While this debuff is active, if the player collides with the "wall" part of the Wall of Flesh, they will take 50 / [100](Expert_Mode.md "Expert Mode") / [150](Master_Mode.md "Master Mode") damage and be [knocked back](Knockback.md "Knockback") in the direction the Wall of Flesh is facing. This damage does not have the usual ±15% random variance, and ignores the player's knockback immunity (e.g. from the [Cobalt Shield](Cobalt_Shield.md "Cobalt Shield") and its upgrades). If the player is killed by this damage, the [death message](Death.md "Death") _“ <Player name> was slain...”_[3] is displayed. 

If the Wall of Flesh reaches the edge of the world, it despawns, and all players inflicted with Horrified will die instantly (with the unique death message _“ <Player name> was licked.”_ or _“ <Player name> got to 1st base with the Wall of Flesh!”_).

When the Horrified debuff is active, attempting to leave the Underworld or getting behind the Wall of Flesh inflicts [The Tongue](The_Tongue.md "The Tongue") debuff. When it is activated, a tendril snatches the player and draws them into the Wall of Flesh's mouth at a speed of up to 56 mph, ignoring [blocks](Blocks.md "Blocks") in the way. In [Expert Mode](Expert_Mode.md "Expert Mode"), the debuff also causes the player to take 50 damage per second. The player is unable to move or use items while the debuff is active. If the player dies to the debuff, the unique death message _“ <Player name> was licked.”_ or _“ <Player name> got to 1st base with the Wall of Flesh!”_ will be displayed. When The Tongue debuff is active, if the [Euclidean distance](https://en.wikipedia.org/wiki/en:Euclidean_distance "wikipedia:en:Euclidean distance") between the player and Wall of Flesh is more than 187.5 tiles, the player will die instantly instead of being drawn to the Wall of Flesh, with the unique death message _“ <Player name> tried to escape.”_[3] This effectively prevents the player from escaping the fight or teleporting behind the boss (including with [Magic Mirrors](Magic_Mirrors.md "Magic Mirrors"), [Teleporters](Teleporter.md "Teleporter"), [Demon Conch](Demon_Conch.md "Demon Conch"), etc.). Quitting and re-entering the world allows for escape, but causes the Wall of Flesh to despawn.

The Wall of Flesh moves faster as its health depletes; see below for details. It can reach up to 17 mph / [41 mph](Expert_Mode.md "Expert Mode") at very low health levels. Due to the Wall of Flesh's higher movement speed in Expert Mode, the speed at which it draws players via the Tongue debuff in Expert also increases as its health decreases. 

Additionally: 

  * The Wall of Flesh has small mouths called The Hungry, each attached by a long vein, which move towards and damage players. As the Wall of Flesh's main body takes damage, they deal more damage and become more resistant to attacks. When sufficiently damaged, they detach and fly towards players at high speed. 
    * The Hungry will always drop a [Heart](Heart.md "Heart") when killed. In Expert Mode, they only have a 1/5 (20%) chance to do so, and they respawn as long as the Wall of Flesh is alive.
    * In Expert Mode, the Hungry gain extra [knockback](Knockback.md "Knockback") resistance with each additional player in [multiplayer](Multiplayer.md "Multiplayer"), and become immune to knockback when there are at least 5 players.[4]
  * The Wall of Flesh's eyes fire purple Eye Lasers. As its health depletes, the lasers increase in damage, frequency, and velocity.
  * The Wall of Flesh "burps" [Leeches](Leech.md "Leech") from its mouth that chase players. These will also always / [with a 1/5 (20%) chance](Expert_Mode.md "Expert Mode") drop a [Heart](Heart.md "Heart") when killed.
  * It randomly lets out a roar.

### Movement speed

The movement speed of the Wall of Flesh depends on its health as follows:[5]

Classic Mode  Health | Speed   
---|---  
≥75%  | 8 mph  
<75%6000 HP | 9 mph  
<50%4000 HP | 11 mph  
<25%2000 HP | 14 mph  
<10%800 HP | 17 mph  
  
Expert Mode  Health | Speed   
---|---  
≥75%  | 12 mph  
<75%[8400](Expert_Mode.md "Expert Mode") / [10710](Master_Mode.md "Master Mode") HP | 14 mph  
<66%[7392](Expert_Mode.md "Expert Mode") / [9424](Master_Mode.md "Master Mode") HP | 16 mph  
<50%[5600](Expert_Mode.md "Expert Mode") / [7140](Master_Mode.md "Master Mode") HP | 19 mph  
<33%[3696](Expert_Mode.md "Expert Mode") / [4712](Master_Mode.md "Master Mode") HP | 21 mph  
<25%[2800](Expert_Mode.md "Expert Mode") / [3570](Master_Mode.md "Master Mode") HP | 24 mph  
<10%[1120](Expert_Mode.md "Expert Mode") / [1428](Master_Mode.md "Master Mode") HP | 28 mph  
<5%[560](Expert_Mode.md "Expert Mode") / [714](Master_Mode.md "Master Mode") HP | 33 mph  
<3.5%[392](Expert_Mode.md "Expert Mode") / [499](Master_Mode.md "Master Mode") HP | 37 mph  
<2.5%[280](Expert_Mode.md "Expert Mode") / [357](Master_Mode.md "Master Mode") HP | 41 mph  
  
## Parts

```


---

## 🤖 Assistant · 2026-08-13T02:12:32.314Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '260,300p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Skeletron_Prime.md",
 "description": "Read Skeletron Prime behavior section"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:32.423Z

**📎 ToolResult**

```
## Behavior

Skeletron Prime's appearance during the spinning phase.

Skeletron Prime's head constantly endeavors to remain between 31.5 and 12.5 tiles above the player and within 6.25 tiles of either side of the player. It can accelerate infinitely in order to move back into this area. The head does not actively attempt to make contact with the player.[1]

Skeletron Prime's four limbs all have unique attacks: 

  * Prime Cannon fires bombs every 2.33 seconds that do not destroy tiles[5], usually up into the air rather than directly at the player. It usually stays above the player.
  * Prime Saw usually remains under the player, moving up and down.
  * Prime Vice will swipe around wildly, making occasional lunges at the player. It usually remains diagonal to the player.
  * Prime Laser shoots red Death Lasers every 3.33 seconds, similar to those of [Retinazer](Retinazer.md "Retinazer") and [The Destroyer](The_Destroyer.md "The Destroyer"), and is always pointed at a player. It usually stays horizontal to the player.

Every 10 seconds, Skeletron Prime will enter a spinning phase for 6.67 seconds, in which its attacks become more aggressive: 

  * Skeletron Prime's head will grow spikes and start spinning towards the player at 10 mph, exactly like how its pre-Hardmode counterpart [Skeletron](Skeletron.md "Skeletron") does. Damage and defense are doubled to 94 / [160](Expert_Mode.md "Expert Mode") / [240](Master_Mode.md "Master Mode") damage and 48 defense.[1] In [Expert Mode](Expert_Mode.md "Expert Mode"), the base spinning speed is 31 mph and is increased the further the player is away, up to a maximum of 76 mph at a distance of 37.5 tiles.
  * Prime Cannon will aim at the player directly and decrease its cooldown between firing to 0.67 seconds.
  * Prime Saw will begin homing directly towards the player's location.
  * Prime Vice becomes more aggressive and frequently lunges towards the player.
  * Prime Laser will fire lasers every 1.33 seconds.
  * Skeletron Prime lets out a roar every time it enters the spinning phase.

If Skeletron Prime is not killed before [dawn](Dawn "Dawn") (4:30 AM), it will enrage and permanently behave like a faster Dungeon Guardian, increasing its velocity[6] and usually killing the player instantly upon contact: its damage and defense is increased to 9,999.[1] It will remain in this state until defeated, even if it becomes night again. Killing Skeletron Prime in this form still counts as defeating it and it will drop its items normally. 

If the player is more than 375 tiles away, Skeletron Prime will start moving downwards and will quickly despawn.[1]

## Notes

This content is transcluded from [Mechanical bosses § Notes](Mechanical_bosses#Notes "Mechanical bosses").

  * When spawning naturally, a mechanical boss spawns exactly 81 in-game minutes (at 8:51 PM) after the status message has appeared. Being in a layer lower than the [Surface](Surface.md "Surface") at that moment, or, in singleplayer, exiting the world during that timespan, will prevent the boss from spawning naturally. Also, if any boss is already active at 8:51 PM, the spawn will not take place.
  * With the 1/10 (10%) chance of spawning naturally at dusk, the resulting chance for each mechanical boss is initially 1/30 (3.33%). Once one of them has been defeated, the remaining two have a resulting 1/20 (5%) chance of spawning naturally, and after defeating the second one, the last one has the full chance of 1/10 (10%).
  * An [Eye of Cthulhu](Eye_of_Cthulhu.md "Eye of Cthulhu") naturally spawning will take precedence over a mechanical boss naturally spawning.[7]
  * If the [Old One's Army](Old_One's_Army.md "Old One's Army") or another [boss](Boss "Boss") is active at 7:30 PM, a natural mechanical boss spawn will not occur that night.[8]
  * A [Lantern Night](Lantern_Night.md "Lantern Night") occurring will prevent a mechanical boss from naturally spawning. However, summoning a mechanical boss using one of the summon items will cancel out the Lantern Night, just like any other boss summon.
  * In worlds that combine the [For the Worthy](For_the_Worthy.md "For the Worthy") and [Remix](Remix.md "Remix") seeds, the player cannot summon the mechanical bosses separately, they have to summon [Mechdusa](Mechdusa.md "Mechdusa") instead.
  * It is possible to summon a mechanical boss in [pre-Hardmode](Pre-Hardmode.md "Pre-Hardmode") if the summoning item is brought in from another world. However, if the Wall of Flesh has not been defeated, [Plantera's Bulbs](Plantera's_Bulb.md "Plantera's Bulb") will not start spawning.
  * The Bombs fired by the Prime Cannon explode upon contact with [platforms](Platforms.md "Platforms") as well as [Planter Boxes](Planter_Boxes.md "Planter Boxes").

## Achievements

```


---

## 🤖 Assistant · 2026-08-13T02:12:32.639Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '375,445p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Plantera.md",
 "description": "Read Plantera behavior sections"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:32.760Z

**📎 ToolResult**

```
Plantera's second form.

Plantera travels slowly through blocks using three long vines to grapple onto solid foreground blocks, similarly to [multi-hooks](Hooks.md "Hooks"). In the second phase, Plantera gains the ability to grapple onto [background walls](Background_walls.md "Background walls"). The ends of her vines, called Plantera's Hooks, are completely invincible and deal contact damage. 

### First form

Plantera slowly creeps after the player, deals contact damage, and fires the projectiles listed in the following table at them. She generally keeps her distance from the player, instead focusing on rapidly bombarding them with high-velocity projectile attacks. She will only fire projectiles when she has a clear line of sight to the player. 

Projectile | Damage[1] | Chance to be fired[1]  
---|---|---  
| Seed | 44 / [76](Expert_Mode.md "Expert Mode") / [114](Master_Mode.md "Master Mode") | 21/32 (65.63%) / [5/12 (41.67%)](Expert_Mode.md "Expert Mode")(100% while Plantera has ≥80% health)  
| Poison Seed | 54 / [96](Expert_Mode.md "Expert Mode") / [144](Master_Mode.md "Master Mode") | 8/32 (25%) / [6/12 (50%)](Expert_Mode.md "Expert Mode")  
| Thorn Ball | 62 / [108](Expert_Mode.md "Expert Mode") / [162](Master_Mode.md "Master Mode") | 3/32 (9.38%) / [1/12 (8.33%)](Expert_Mode.md "Expert Mode")  
  
Seeds and Poison Seeds function similarly to the stingers of [Hornets](Hornet.md "Hornet"), the [Queen Bee](Queen_Bee.md "Queen Bee"), and the petals of the [Flower Pow](Flower_Pow.md "Flower Pow"). In Expert mode, they can travel through blocks, but not in Classic mode. The green Poison Seeds have a 1/2 (50%) / [100%](Expert_Mode.md "Expert Mode") chance to inflict the [Poisoned](Poisoned.md "Poisoned") [debuff](Debuff "Debuff") for 3–7 / [4–9](Expert_Mode.md "Expert Mode") seconds. Thorn Balls are similar to the projectiles released by [Spiky Ball Traps](Spiky_Ball_Trap.md "Spiky Ball Trap") but ricochet off solid blocks much more quickly and erratically. They will try to follow the player horizontally, potentially overwhelming the player if they stay within the same area for extended periods of time. 

Poison Seeds and Thorn Balls are only used when Plantera's health is below 80% (24,000 / [33,600](Expert_Mode.md "Expert Mode") / [42,840](Master_Mode.md "Master Mode")). There is a short cooldown after a projectile has been fired, which depends on Plantera's current health as well as the type of projectile: 

Projectile | Cooldown, based on Plantera's health[5]  
---|---  
≥ 90%  
[hp 1] | 89%–80%  
[hp 2] | 79%–70%  
[hp 3] | 69%–60%  
[hp 4] | 59%–50%  
[hp 5]  
| Seed | 1.35 seconds  | 0.68 seconds  | 0.45 seconds  | 0.35 seconds  | 0.28 seconds   
| Poison Seed | n/a | n/a | 0.62 seconds  | 0.47 seconds  | 0.38 seconds   
| Thorn Ball | n/a | n/a | 1.12 seconds  | 0.85 seconds  | 0.68 seconds   
  
### Second form

Once Plantera is brought down to half of her maximum health (15,000 / [21,000](Expert_Mode.md "Expert Mode") / [26,775](Master_Mode.md "Master Mode")), she changes into her second form as her pink petals fall away to reveal a thorn-filled mouth. In this form, Plantera ceases to fire the same projectiles from before and instead moves much more quickly and aggressively in an attempt to inflict contact damage. Her contact damage is greater than in the first form, but her defense decreases significantly to 10. 

Upon transformation, Plantera sprouts eight additional mouths, called Plantera's Tentacles, that are attached via vines to her body. Plantera's tentacles deal contact damage and get in the way of the player's attacks, but have comparatively little health. Defeated tentacles will not regrow, making Plantera much easier to fight once all are killed. 

Plantera now occasionally releases floating pink Spore [projectile enemies](Projectile_NPC "Projectile NPC") that drift toward the player, similar to the spores released by the [Giant Fungi Bulb](Giant_Fungi_Bulb.md "Giant Fungi Bulb"). They can be destroyed in a single hit with any [weapon](Weapon "Weapon") or [tool](Tool "Tool"), but travel through blocks and deal high contact damage. Similarly to the first phase, the cooldown between the release of Spores depends on Plantera's health: 

[Projectile enemy](Projectile_NPC "Projectile NPC") | Cooldown, based on Plantera's health[6]  
---|---  
50%–40%[hp 6] | 39%–30%[hp 7] | 29%–20%[hp 8] | 19%–10%[hp 9] | ≤10%[hp 10]  
| Spore | 5.85 seconds  | 2.93 seconds  | 1.95 seconds  | 1.47 seconds  | 1.18 seconds   
  
### Enraged behavior

Plantera becomes "enraged" if she follows the player out of the [Underground Jungle](Underground_Jungle.md "Underground Jungle"), whether it be to the surface, to the [Underworld](Underworld "Underworld"), or to a completely different biome. She does not enrage in [Hallowed](Hallowed "Hallowed"), [Corrupted](Corrupted "Corrupted") or [Crimson](Crimson "Crimson") parts of the Underground Jungle as long as there are at least 140 [Jungle grass](Jungle_grass.md "Jungle grass") / [Hive](Hive.md "Hive") / [Lihzahrd Brick](Lihzahrd_Brick.md "Lihzahrd Brick") blocks nearby. Being enraged causes Plantera to gain double damage, double defense (quadruple defense in the second form), and increased movement speed, as well as changing her attack patterns and directly rushing toward the player. Her projectiles also deal double damage and have reduced cooldowns. Plantera's behavior returns to normal upon reentering the Underground Jungle biome. 

### Expert Mode

In [Expert Mode](Expert_Mode.md "Expert Mode"), there are a few significant differences in Plantera's attacks, aside from the default increased health and damage. 

In the first form, her pink Seeds can travel through blocks, and all projectiles have limited homing capabilities. The cooldowns are also decreased: 

Projectile | Cooldown, based on Plantera's health[5]  
---|---  
≥ 90%[hp 1] | 89%–80%[hp 2] | 79%–70%[hp 3] | 69%–60%[hp 4] | 59%–50%[hp 5]  
| Seed | 0.68 seconds  | 0.45 seconds  | 0.35 seconds  | 0.28 seconds  | 0.23 seconds   
| Poison Seed | n/a | n/a | 0.47 seconds  | 0.38 seconds  | 0.32 seconds   
| Thorn Ball | n/a | n/a | 0.85 seconds  | 0.68 seconds  | 0.57 seconds   
  
In her second form, Plantera and Plantera's Tentacles move faster than normal. In addition, there are nine more Plantera's Tentacles, attached to Plantera's Hooks in groups of three. Furthermore, the eight tentacles that are attached to Plantera's body can respawn after they have been killed (this does not apply to the tentacles on the hooks). The rate is randomized, but it depends on the number of tentacles that are alive – if all tentacles are destroyed, a new tentacle spawns after 5 seconds, on average. This is increased by 5 seconds per living tentacle, hence it takes an average of 180 seconds for all eight tentacles to fully respawn. A single defeated tentacle will take 40 seconds to respawn, on average, assuming the other seven tentacles remain alive for the duration.[1]

## Aftermath

Plantera always drops a [Temple Key](Temple_Key.md "Temple Key"), which grants access to the [Jungle Temple](Jungle_Temple.md "Jungle Temple") and the [Golem](Golem.md "Golem") [boss](Boss "Boss"). 

A [status message](Status_message "Status message") saying _" Screams are echoing from the dungeon..."_ will appear upon Plantera's defeat, signaling that new, more difficult types of [enemies](Enemies.md "Enemies") will begin spawning in the [Dungeon](Dungeon.md "Dungeon") ([see details](Dungeon#Hardmode_post-Plantera_Dungeon "Dungeon")). These enemies drop powerful new weapons, accessories, and other items. [Dungeon Spirits](Dungeon_Spirit.md "Dungeon Spirit") will begin to appear when Dungeon enemies with more than 100 health are slain, which drop [Ectoplasm](Ectoplasm.md "Ectoplasm"), a new [crafting material](Crafting_material "Crafting material") that offers access to the [Pumpkin Moon](Pumpkin_Moon.md "Pumpkin Moon") and [Frost Moon](Frost_Moon.md "Frost Moon") [events](Event "Event"), as well as [Spectre Bars](Spectre_Bar.md "Spectre Bar"). 

Additionally:

```


---

## 🤖 Assistant · 2026-08-13T02:12:33.031Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '396,410p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Wall_of_Flesh.md",
 "description": "Read Hungry II KB resistance lines"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:33.085Z

**📎 ToolResult**

```
Type| [Flying Enemy](Flying_Enemy "Flying Enemy")  
---|---  
[Environment](Environment "Environment")| [ The Underworld ](The_Underworld.md "The Underworld")  
[AI Type](AI.md "AI")| Demon Eye AI  
Damage| 30/60/90  
Max Life| 80/112/168  
[Defense](Defense.md "Defense")| 6  
[KB](Knockback.md "Knockback") Resist| 20%/28%/36%[ (1 player)  
69% (2 players)  
79% (3 players)  
86% (4 players)  
100% (5 players or more)  
](Expert_Mode.md "Expert Mode")[ (1 player)  
72% (2 players)

```


---

## 🤖 Assistant · 2026-08-13T02:12:34.072Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"despawn|flee|dawn|player dies|unspawn\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Plantera.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Destroyer.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Skeletron_Prime.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Wall_of_Flesh.md | head -30",
 "description": "Find despawn statements across pages"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:34.157Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/terraria-wiki-md/Skeletron_Prime.md:121:If Skeletron Prime is not defeated by dawn (4:30 AM), it will enrage and permanently behave much like a [Dungeon Guardian](Dungeon_Guardian.md "Dungeon Guardian"). It will cease using its limbs and instead charge at the player at extremely high speeds, dealing usually lethal damage upon contact. 
~/Project/GLM/SandboxWorld/terraria-wiki-md/Skeletron_Prime.md:282:If Skeletron Prime is not killed before [dawn](Dawn "Dawn") (4:30 AM), it will enrage and permanently behave like a faster Dungeon Guardian, increasing its velocity[6] and usually killing the player instantly upon contact: its damage and defense is increased to 9,999.[1] It will remain in this state until defeated, even if it becomes night again. Killing Skeletron Prime in this form still counts as defeating it and it will drop its items normally. 
~/Project/GLM/SandboxWorld/terraria-wiki-md/Skeletron_Prime.md:284:If the player is more than 375 tiles away, Skeletron Prime will start moving downwards and will quickly despawn.[1]
~/Project/GLM/SandboxWorld/terraria-wiki-md/Skeletron_Prime.md:2421:  *[dawn]: 4:30 AM
~/Project/GLM/SandboxWorld/terraria-wiki-md/Plantera.md:524:  * [Desktop 1.4.4](Desktop_1.4.4 "Desktop 1.4.4"): Increased distance before despawn timer begins ticking down dramatically.
~/Project/GLM/SandboxWorld/terraria-wiki-md/Plantera.md:546:    * Now despawns when all players have been killed.
~/Project/GLM/SandboxWorld/terraria-wiki-md/Plantera.md:2635:  *[dawn]: 4:30 AM
~/Project/GLM/SandboxWorld/terraria-wiki-md/Wall_of_Flesh.md:222:If the Wall of Flesh reaches the edge of the world, it despawns, and all players inflicted with Horrified will die instantly (with the unique death message _“ <Player name> was licked.”_ or _“ <Player name> got to 1st base with the Wall of Flesh!”_).
~/Project/GLM/SandboxWorld/terraria-wiki-md/Wall_of_Flesh.md:224:When the Horrified debuff is active, attempting to leave the Underworld or getting behind the Wall of Flesh inflicts [The Tongue](The_Tongue.md "The Tongue") debuff. When it is activated, a tendril snatches the player and draws them into the Wall of Flesh's mouth at a speed of up to 56 mph, ignoring [blocks](Blocks.md "Blocks") in the way. In [Expert Mode](Expert_Mode.md "Expert Mode"), the debuff also causes the player to take 50 damage per second. The player is unable to move or use items while the debuff is active. If the player dies to the debuff, the unique death message _“ <Player name> was licked.”_ or _“ <Player name> got to 1st base with the Wall of Flesh!”_ will be displayed. When The Tongue debuff is active, if the [Euclidean distance](https://en.wikipedia.org/wiki/en:Euclidean_distance "wikipedia:en:Euclidean distance") between the player and Wall of Flesh is more than 187.5 tiles, the player will die instantly instead of being drawn to the Wall of Flesh, with the unique death message _“ <Player name> tried to escape.”_[3] This effectively prevents the player from escaping the fight or teleporting behind the boss (including with [Magic Mirrors](Magic_Mirrors.md "Magic Mirrors"), [Teleporters](Teleporter.md "Teleporter"), [Demon Conch](Demon_Conch.md "Demon Conch"), etc.). Quitting and re-entering the world allows for escape, but causes the Wall of Flesh to despawn.
~/Project/GLM/SandboxWorld/terraria-wiki-md/Wall_of_Flesh.md:451:  * Being able to summon the Wall of Flesh depends on the [Guide](Guide.md "Guide") being alive. He cannot respawn if it is [nighttime](Night "Night") or there is an [event](Event "Event") in progress. Due to this, the waiting time between multiple fights is often much greater than with other bosses. Timing the fight to finish just before dawn has a chance to allow two or even more fights, especially if the Guide already has an assigned [house](House.md "House").
~/Project/GLM/SandboxWorld/terraria-wiki-md/Wall_of_Flesh.md:453:  * When the Wall of Flesh is alive and all players in the Underworld have been killed, the screen gradually fades to black over the course of 4 seconds, after which the Wall of Flesh will despawn and the screen will return to normal visibility.
~/Project/GLM/SandboxWorld/terraria-wiki-md/Wall_of_Flesh.md:489:  * If the Wall of Flesh is accidentally summoned, the player can quit and re-enter the world to despawn it. Note that doing so will also remove any dropped items and teleport the player back to their [spawn point](Spawn_point "Spawn point").
~/Project/GLM/SandboxWorld/terraria-wiki-md/Wall_of_Flesh.md:539:  * [Desktop 1.4.1](Desktop_1.4.1 "Desktop 1.4.1"): Now causes the screen to fade to black and despawns if all nearby players are dead, or there are no players nearby.
~/Project/GLM/SandboxWorld/terraria-wiki-md/Wall_of_Flesh.md:2943:  *[dawn]: 4:30 AM
~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Destroyer.md:122:The Destroyer must be killed before dawn (4:30 AM), otherwise it flees and despawns. 
~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Destroyer.md:146:The Destroyer spawns coiled up, like most worm enemies, and immediately starts uncoiling and following the player. It has limited mobility when fully in the air, requiring [blocks](Blocks.md "Blocks") or [platforms](Platforms.md "Platforms") to "burrow" through. However, it is able to move freely while off-screen. It follows the player from any distance and will only despawn if the player dies or if dawn comes (4:30 AM). It despawns by quickly traveling underground until off-screen. 
~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Destroyer.md:157:  * Probes never return to the main body, and will not despawn as long as The Destroyer is alive, even if the player goes too far away.[5]
~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Destroyer.md:205:  * Since The Destroyer follows the player instead of despawning, one can use any means of teleportation ([Magic Mirrors](Magic_Mirrors.md "Magic Mirrors"), [Teleporters](Teleporter.md "Teleporter"), etc.) to easily avoid it during the fight. 
~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Destroyer.md:322:  5. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.5.6](1.4.5.6.md "1.4.5.6") source code, method `DoesntDespawnToInactivity()` in `Terraria.NPC.cs`.
~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Destroyer.md:2354:  *[dawn]: 4:30 AM

```


---

## 🤖 Assistant · 2026-08-13T02:12:40.425Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I need the full Twins eye infoboxes (Retinazer first form lines 122-155, Spazmatism first form 169-215, Retinazer second form 229-265, Spazmatism second form 281-315). Let me read those to get exact Damage/Defense rows.

Also need WoF mouth infobox full (already have from second sed, lines 274-290: Damage 50/150/225, Defense 12/18). Wait — the second sed output shows the first block "Wall of Flesh" with Damage| 50/150/225 and Defense 12/18. Note Defense is "12/18" only two values — Classic 12, Expert/Master 18 presumably. I'll note as stated.

Note: the first sed (lines 20-60) showed the main infobox without Damage/Defense rows — likely a collapsed variant. Fine.

Also, WoF "wall" damage: 50/100/150 from behavior section.

Hungry II KB: 20%/28%/36% with Expert scaling lines. Let me get the remaining lines of Hungry II KB (lines 410-425).

Also check Plantera despawn — does the page state despawn when player dies? Line 546 is a history entry. Let me check for despawn behavior of Plantera — grep "despawn" only found history lines. The question asks for stated despawn behavior; for Plantera, enrage is the notable one. Maybe there's something in notes about her despawning when player dies. Let me grep more broadly in Plantera for "dies|death|far away|375".

Also The Twins despawn details around line 365-372 (despawn timers). Let me read that too.

Let me run these in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-13T02:12:40.671Z · glm-x-preview-260804

```
Now let me read the Twins' eye infoboxes in full and a few remaining details.
```


---

## 🤖 Assistant · 2026-08-13T02:12:41.055Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '110,215p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Twins.md",
 "description": "Read Retinazer and Spazmatism first-form infoboxes"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:41.187Z

**📎 ToolResult**

```
RetinazerFirst Form

** _Map icon_**

Classic

Expert

Master

Statistics

Type| [Boss](Boss "Boss")  
---|---  
[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
[AI Type](AI.md "AI")| Retinazer AI  
Damage| 45/76/115 (contact)  
40[76](Expert_Mode.md "Expert Mode")[114](Master_Mode.md "Master Mode") (Eye Laser) [4]  
Max Life| 20000/30000/38250  
[Defense](Defense.md "Defense")| 10  
[KB](Knockback.md "Knockback") Resist| 100%  
Immune to| [](Bleeding.md "Bleeding")[](Confused.md "Confused")[](Poisoned.md "Poisoned")[](Hemorrhage.md "Hemorrhage")  
  
Drops

[Coins](NPC_drops#Coin_drops "NPC drops")| 12 _GC_ 30 _GC_  
---|---  
  
Projectile created

Projectile created

Projectile created

  * Eye Laser

Sounds

Hurt|   
---|---  
Killed|   
Eye Laser|   
Entering second phase|   
  
  * Internal [NPC ID](NPC_IDs.md "NPC IDs"): **125**
  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **83**

SpazmatismFirst Form

** _Map icon_**

Classic

Expert

Master

Statistics

Type| [Boss](Boss "Boss")  
---|---  
[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
[AI Type](AI.md "AI")| Spazmatism AI  
Damage| 50/85/128 (contact)  
50[88](Expert_Mode.md "Expert Mode")[132](Master_Mode.md "Master Mode") (Cursed Flame) [2]  
Max Life| 23000/34500/43988  
[Defense](Defense.md "Defense")| 10  
[KB](Knockback.md "Knockback") Resist| 100%  
Immune to| [](Bleeding.md "Bleeding")[](Confused.md "Confused")[](Poisoned.md "Poisoned")[](Hemorrhage.md "Hemorrhage")  
  
Inflicts [ debuff ](Debuffs.md "Debuffs")

Inflicts [ debuff ](Debuffs.md "Debuffs")

Inflicts [ debuff ](Debuffs.md "Debuffs")

Debuff| [](Cursed_Inferno.md "Cursed Inferno")[Cursed Inferno](Cursed_Inferno.md "Cursed Inferno")  
---|---  
Debuff tooltip|  _Losing life_  
Chance| 68.75% [3]  
Duration| 2–3 seconds [3][4–6 seconds](Expert_Mode.md "Expert Mode") [3][5–7.5 seconds](Master_Mode.md "Master Mode") [3]  
  
Drops

[Coins](NPC_drops#Coin_drops "NPC drops")| 12 _GC_ 30 _GC_  
---|---  
  
Projectile created

Projectile created

Projectile created

  * Cursed Flame (hostile)

Sounds

Hurt|   
---|---  
Killed|   
Cursed Flame|   
Entering second phase|   
  
  * Internal [NPC ID](NPC_IDs.md "NPC IDs"): **126**
  * Internal [Buff ID](Buff_IDs.md "Buff IDs"): **39**
  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **96**

```


---

## 🤖 Assistant · 2026-08-13T02:12:41.516Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '217,320p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Twins.md",
 "description": "Read Retinazer and Spazmatism second-form infoboxes"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:41.615Z

**📎 ToolResult**

```
RetinazerSecond Form

** _Map icon_**

Classic

Expert

Master

Statistics

Type| [Boss](Boss "Boss")  
---|---  
[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
[AI Type](AI.md "AI")| Retinazer AI  
Damage| 67[114](Expert_Mode.md "Expert Mode")[172](Master_Mode.md "Master Mode") (contact)  
50[92](Expert_Mode.md "Expert Mode")[138](Master_Mode.md "Master Mode") (Death Laser)  
36[68](Expert_Mode.md "Expert Mode")[102](Master_Mode.md "Master Mode") (Death Laser rapid fire) [4]  
Max Life| 8000/20000[12000/30000](Expert_Mode.md "Expert Mode")[15300/38250](Master_Mode.md "Master Mode") [4]  
[Defense](Defense.md "Defense")| 20 [4]  
[KB](Knockback.md "Knockback") Resist| 100%  
Immune to| [](Bleeding.md "Bleeding")[](Confused.md "Confused")[](Poisoned.md "Poisoned")[](Hemorrhage.md "Hemorrhage")  
  
Drops

[Coins](NPC_drops#Coin_drops "NPC drops")| 12 _GC_ 30 _GC_  
---|---  
  
  * **Item(Quantity)****Rate**
  * [](Retinazer_Trophy "Retinazer Trophy")[Retinazer Trophy](Retinazer_Trophy "Retinazer Trophy")

10%

Projectile created

Projectile created

Projectile created

  * Death Laser

Sounds

Hurt|   
---|---  
Killed|   
Death Laser|   
  
  * Internal [NPC ID](NPC_IDs.md "NPC IDs"): **125**
  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **100**

SpazmatismSecond Form

** _Map icon_**

Classic

Expert

Master

Statistics

Type| [Boss](Boss "Boss")  
---|---  
[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
[AI Type](AI.md "AI")| Spazmatism AI  
Damage| 75[127](Expert_Mode.md "Expert Mode")[192](Master_Mode.md "Master Mode") (contact)  
60[108](Expert_Mode.md "Expert Mode")[162](Master_Mode.md "Master Mode") (Eye Fire) [2]  
Max Life| 9200/23000[13800/34500](Expert_Mode.md "Expert Mode")[17595/43988](Master_Mode.md "Master Mode") [2]  
[Defense](Defense.md "Defense")| 28 [2]  
[KB](Knockback.md "Knockback") Resist| 100%  
Immune to| [](Bleeding.md "Bleeding")[](Confused.md "Confused")[](Poisoned.md "Poisoned")[](Hemorrhage.md "Hemorrhage")  
  
Inflicts [ debuff ](Debuffs.md "Debuffs")

Inflicts [ debuff ](Debuffs.md "Debuffs")

Inflicts [ debuff ](Debuffs.md "Debuffs")

Debuff| [](Cursed_Inferno.md "Cursed Inferno")[Cursed Inferno](Cursed_Inferno.md "Cursed Inferno")  
---|---  
Debuff tooltip|  _Losing life_  
Chance| 68.75% [3]  
Duration| 2–3 seconds [3][4–6 seconds](Expert_Mode.md "Expert Mode") [3][5–7.5 seconds](Master_Mode.md "Master Mode") [3]  
  
Drops

[Coins](NPC_drops#Coin_drops "NPC drops")| 12 _GC_ 30 _GC_  
---|---  
  
  * **Item(Quantity)****Rate**
  * [](Spazmatism_Trophy "Spazmatism Trophy")[Spazmatism Trophy](Spazmatism_Trophy "Spazmatism Trophy")

10%

Projectile created

Projectile created

Projectile created

  * Eye Fire

```


---

## 🤖 Assistant · 2026-08-13T02:12:41.777Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '355,375p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Twins.md",
 "description": "Read Twins despawn notes"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:41.935Z

**📎 ToolResult**

```
This content is transcluded from [Mechanical bosses § Notes](Mechanical_bosses#Notes "Mechanical bosses").

  * When spawning naturally, a mechanical boss spawns exactly 81 in-game minutes (at 8:51 PM) after the status message has appeared. Being in a layer lower than the [Surface](Surface.md "Surface") at that moment, or, in singleplayer, exiting the world during that timespan, will prevent the boss from spawning naturally. Also, if any boss is already active at 8:51 PM, the spawn will not take place.
  * With the 1/10 (10%) chance of spawning naturally at dusk, the resulting chance for each mechanical boss is initially 1/30 (3.33%). Once one of them has been defeated, the remaining two have a resulting 1/20 (5%) chance of spawning naturally, and after defeating the second one, the last one has the full chance of 1/10 (10%).
  * An [Eye of Cthulhu](Eye_of_Cthulhu.md "Eye of Cthulhu") naturally spawning will take precedence over a mechanical boss naturally spawning.[5]
  * If the [Old One's Army](Old_One's_Army.md "Old One's Army") or another [boss](Boss "Boss") is active at 7:30 PM, a natural mechanical boss spawn will not occur that night.[6]
  * A [Lantern Night](Lantern_Night.md "Lantern Night") occurring will prevent a mechanical boss from naturally spawning. However, summoning a mechanical boss using one of the summon items will cancel out the Lantern Night, just like any other boss summon.
  * In worlds that combine the [For the Worthy](For_the_Worthy.md "For the Worthy") and [Remix](Remix.md "Remix") seeds, the player cannot summon the mechanical bosses separately, they have to summon [Mechdusa](Mechdusa.md "Mechdusa") instead.
  * It is possible to summon a mechanical boss in [pre-Hardmode](Pre-Hardmode.md "Pre-Hardmode") if the summoning item is brought in from another world. However, if the Wall of Flesh has not been defeated, [Plantera's Bulbs](Plantera's_Bulb.md "Plantera's Bulb") will not start spawning.
  * Killing both eyes is required for the boss to collectively drop all of its loot, including dropped [Hearts](Heart.md "Heart"). Thus, killing one of the eyes will not drop any Hearts.
  * Both eyes can drop their respective [trophy](Trophy "Trophy") when killed, regardless of which is killed first. It is also possible (1/100 (1%) chance) for both trophies to drop in one battle.

Two pairs of The Twins that spawned.

  * In single player The Twins can only despawn if both of their despawn timers reach 0 at the same time, which causes them to despawn together. In multiplayer, however, it is possible for them to despawn separately. 
    * This can be exploited by timing 2 players' deaths such that one twin despawns, then a player respawns, allowing for an easier battle with only one twin.

## Achievements

[](Achievements#Buckets_of_Bolts "Achievements")

```


---

## 🤖 Assistant · 2026-08-13T02:12:42.159Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '405,425p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Wall_of_Flesh.md",
 "description": "Read Hungry II remaining KB lines"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:42.259Z

**📎 ToolResult**

```
69% (2 players)  
79% (3 players)  
86% (4 players)  
100% (5 players or more)  
](Expert_Mode.md "Expert Mode")[ (1 player)  
72% (2 players)  
82% (3 players)  
88% (4 players)  
100% (5 players or more)  
](Master_Mode.md "Master Mode")  
Immune to| [](Confused.md "Confused")[](Shimmering.md "Shimmering")  
  
Drops

  * **Item(Quantity)****Rate**
  * [](Heart.md "Heart")[Heart](Heart.md "Heart")

100%[20%](Expert_Mode.md "Expert Mode")

Sounds

```


---

## 🤖 Assistant · 2026-08-13T02:12:43.210Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i -E \"despawn|dies|killed,|far away|away from|375 tiles|timer\" ~/Project/GLM/SandboxWorld/terraria-wiki-md/Plantera.md | grep -v -i \"history\\|1\\.4\\.\\|Desktop\\|Console\\|Mobile\\|Legacy\" | head -20",
 "description": "Search Plantera despawn statements"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:43.623Z

**📎 ToolResult**

```
546:    * Now despawns when all players have been killed.
1758:  *[13 mph]: 13 miles per hour (as measured by the Stopwatch item) or 9.375 tiles per second
2119:  *[32 mph]: 32 miles per hour (as measured by the Stopwatch item) or 23.63343375 tiles per second
2131:  *[63 mph]: 63 miles per hour (as measured by the Stopwatch item) or 45.9375 tiles per second
2222:  *[1 mph]: 1 mile per hour (as measured by the Stopwatch item) or 0.375 tiles per second

```


---

## 🤖 Assistant · 2026-08-13T02:12:44.177Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '24,32p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Twins.md; echo ---; sed -n '122,133p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Twins.md; echo ---; sed -n '169,180p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Twins.md",
 "description": "Read Twins total and eye stat rows"
}
```


---

## 👤 User(sidechain) · 2026-08-13T02:12:44.516Z

**📎 ToolResult**

```
[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
Max Life| 43000[64500](Expert_Mode.md "Expert Mode")[82238](Master_Mode.md "Master Mode") (total)  
[Defense](Defense.md "Defense")| 10  
[KB](Knockback.md "Knockback") Resist| 100%  
Immune to| [](Bleeding.md "Bleeding")[](Confused.md "Confused")[](Poisoned.md "Poisoned")[](Hemorrhage.md "Hemorrhage")  
  
Drops

[Coins](NPC_drops#Coin_drops "NPC drops")| 12 _GC_(Dropped by Treasure Bag[1])  
---
Type| [Boss](Boss "Boss")  
---|---  
[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
[AI Type](AI.md "AI")| Retinazer AI  
Damage| 45/76/115 (contact)  
40[76](Expert_Mode.md "Expert Mode")[114](Master_Mode.md "Master Mode") (Eye Laser) [4]  
Max Life| 20000/30000/38250  
[Defense](Defense.md "Defense")| 10  
[KB](Knockback.md "Knockback") Resist| 100%  
Immune to| [](Bleeding.md "Bleeding")[](Confused.md "Confused")[](Poisoned.md "Poisoned")[](Hemorrhage.md "Hemorrhage")  
  
Drops
---
Type| [Boss](Boss "Boss")  
---|---  
[Environment](Environment "Environment")| [ Surface ](Surface.md "Surface") \+ [ Night ](Night "Night")[ Space ](Space.md "Space") \+ [ Night ](Night "Night")  
[AI Type](AI.md "AI")| Spazmatism AI  
Damage| 50/85/128 (contact)  
50[88](Expert_Mode.md "Expert Mode")[132](Master_Mode.md "Master Mode") (Cursed Flame) [2]  
Max Life| 23000/34500/43988  
[Defense](Defense.md "Defense")| 10  
[KB](Knockback.md "Knockback") Resist| 100%  
Immune to| [](Bleeding.md "Bleeding")[](Confused.md "Confused")[](Poisoned.md "Poisoned")[](Hemorrhage.md "Hemorrhage")  
  
Inflicts [ debuff ](Debuffs.md "Debuffs")

```


---

## 🤖 Assistant · 2026-08-13T02:13:01.788Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I now have everything needed. Let me also double check the Destroyer "82 segments" statement and the WoF Hungry count (how many Hungry). And whether Destroyer page states number of body segments — line 217: "The Destroyer is extremely long, measuring 82 segments including head and tail, or 239 tiles in length." That's in trivia though. Good enough — I'll report it as stated.

Also Plantera despawn: the page doesn't state a current despawn rule except enrage. I'll note that.

Let me compile the report. Note formatting conventions: "a/b/c" = Classic/Expert/Master; "a[ b ][ c ]" same thing with linked text.

Wall of Flesh:
- Main body: Max Life 8000/11200/14280; Damage 50/150/225; Defense 12/18 (two values listed); KB Resist 100%.
- "Wall" part damage: 50/100/150 (behavior section).
- Eyes: Max Life 8000/11200/14280 (shared), Damage 50/150/225 contact, plus Eye Laser 22–30/44–60/66–90 depending on health; Defense 0/6; KB 100%.
- The Hungry: Max Life 240/336/504; Damage 30/60/90 (>75%), 45/90/135 (75–50%), 60/120/180 (<50%); Defense 10/16 (>75%), 20 (75–50%), 30 (<50%); KB Resist −10%/1%/12% (1 player) with Expert multiplayer scaling 57/71/81/100% at 2/3/4/5+ players, and Master 62/75/83/100%.
- The Hungry II: Max Life 80/112/168; Damage 30/60/90; Defense 6; KB 20%/28%/36% (1 player) with Expert scaling 69/79/86/100% (2/3/4/5+), Master 72/82/88/100%.
- Movement speed phase table (Classic and Expert/Master thresholds).
- Despawn: reaches edge of world → despawns and all Horrified players die; if all players in Underworld killed → screen fades to black over 4 seconds then despawns; quitting and re-entering world despawns it.

Skeletron Prime head: Max Life 28000/42000/53550; Damage 47/80/120 contact, 94/160/240 spinning, 9999 during day; Defense 24, 48 while spinning, 9999 during day; KB 100%.
- Prime Cannon: 7000/10500/13387 HP; contact 30/51/76, bomb 80/160/240; def 23; KB 100%.
- Prime Saw: 9000/13500/17212; 56/95/143; def 38; KB 100%.
- Prime Vice: 9000/13500/17212; 52/88/133; def 34; KB 100%.
- Prime Laser: 6000/9000/11475; contact 29/49/74, death laser 50/100/150; def 20; KB 100%.
- Phase: spinning phase every 10 seconds for 6.67 seconds (head damage/defense doubled). Not HP-threshold based.
- Despawn: dawn (4:30 AM) → enrage permanently, behaves like faster Dungeon Guardian, damage and defense increased to 9,999. More than 375 tiles away → moves downward and quickly despawns.

The Destroyer: main Max Life 80000/120000/153000, KB 100%, no defense row in main infobox.
Segments table: Head (NPC 134): damage 70/280/420, defense 0. Body (135): contact 55/94/140, Death Laser 44/72/108, defense 30. Tail (136): 40/68/102, defense 35.
Probe lasers 50/88/132.
Segments: 82 segments including head and tail, 239 tiles (trivia).
Despawn: only if player dies or dawn (4:30 AM); flees and despawns at dawn.

Twins total: 43000/64500/82238 total, Defense 10, KB 100%.
Retinazer 1st: 20000/30000/38250; contact 45/76/115; Eye Laser 40/76/114; def 10; KB 100%.
Retinazer 2nd: HP 8000/20000 [12000/30000] [15300/38250]; contact 67/114/172; Death Laser 50/92/138; rapid fire 36/68/102; def 20; KB 100%.
Spazmatism 1st: 23000/34500/43988; contact 50/85/128; Cursed Flame 50/88/132; def 10; KB 100%.
Spazmatism 2nd: HP 9200/23000 [13800/34500] [17595/43988]; contact 75/127/192; Eye Fire 60/108/162; def 28; KB 100%.
Threshold: below 40% → transforms. Retinazer transforms at 8,000/12,000/15,300; Spazmatism at 9,200/13,800/17,595. Defense increased to 20 and 28 respectively.
Despawn: must be killed before dawn (4:30 AM) otherwise flee and despawn; singleplayer both despawn timers must reach 0 at same time.

Plantera: Max Life 30000/42000/53550; contact 50/100/150; Seed 44/76/114; Poison Seed 54/96/144; Thorn Ball 62/108/162; Defense 36; KB 100%.
Second form: Max Life 15000/30000 [21000/42000] [26775/53550]; Damage 70/140/210; Defense 10; KB 100%.
Hooks: 4000/8000/12000; damage 60/120/180; def 24; KB 0%/10%/20%; invincible boss part.
Tentacles: 1000/2000/2550; damage 60/138/207; def 20; KB 0%/10%/20%.
Spore: HP 1, def 0, damage 70/140→126/210→189, KB 100%.
Phase 2 at 50% (15,000/21,000/26,775). Poison Seeds and Thorn Balls only below 80% (24,000/33,600/42,840).
Enrage: out of Underground Jungle → double damage, double defense (quadruple in second form), increased movement speed; no enrage in Hallowed/Corrupt/Crimson parts of Underground Jungle with ≥140 Jungle grass/Hive/Lihzahrd Brick blocks nearby.
Despawn: current page only notes enrage; no dawn despawn (Plantera can be fought any time). History line: "Now despawns when all players have been killed" (1.4.0.5? it's a history entry). I'll mention only if useful — the task says "any stated despawn behavior". For Plantera, the page's despawn-related statements are the enrage and that history entry. I'll note enrage as the main one.

Also note Plantera KB resist for main is 100%; hooks/tentacles have 0%/10%/20%.

WoF Hungry count: the page doesn't state a number in what I read; not asked. Skip.

Defense values: note that only some have three values — WoF 12/18 (two values), Hungry defense 10/16 then flat 20/30; Twins eyes def 10 (single) etc. I'll present verbatim.

Now write the compact report.
```

</details>


---

## 🤖 Assistant · 2026-08-13T02:13:22.811Z · glm-x-preview-260804

```
All data extracted. Here is the per-boss report.

Important note: `Retinazer.md` and `Spazmatism.md` are redirect stubs containing only `[Retinazer](./The_Twins#Eyes)` / `[Spazmatism](./The_Twins#Eyes)` plus glossary boilerplate. All eye stats come from `~/Project/GLM/SandboxWorld/terraria-wiki-md/The_Twins.md`.

Notation below: `a/b/c` = Classic/Expert/Master (wiki's own slash format). Where the wiki wrote linked-bracket values I keep them inline.

---

## Wall of Flesh (`Wall_of_Flesh.md`)

All parts share one health counter.

**Wall of Flesh (main body)**
- Max Life: `8000/11200/14280`
- Contact damage: `50/150/225`
- Defense: `12/18` (only two values listed on the page)
- KB Resist: `100%`
- The undamageable "wall" part deals `50 / 100 / 150` damage (behavior section)

**Wall of Flesh Eye** (NPC 114)
- Max Life: `8000/11200/14280`
- Damage: `50/150/225` (contact); `22–30 / 44–60 / 66–90` (Eye Laser; depending on health)
- Defense: `0/6`
- KB Resist: `100%`

**The Hungry** (NPC 115) — stats scale with WoF health
- Max Life: `240/336/504`
- Damage: `30/60/90` (WoF health >75%); `45/90/135` (75–50%); `60/120/180` (<50%)
- Defense: `10/16` (>75%); `20` (75–50%); `30` (<50%)
- KB Resist (1 player): `−10%/1%/12%`; Expert/Master scale with player count — Expert: 57% (2p), 71% (3p), 81% (4p), 100% (5p+); Master: 62% (2p), 75% (3p), 83% (4p), 100% (5p+)

**The Hungry II** (NPC 116, detached form)
- Max Life: `80/112/168`
- Damage: `30/60/90`
- Defense: `6`
- KB Resist: `20%/28%/36%` (1p); Expert: 69/79/86/100% (2/3/4/5+p); Master: 72/82/88/100%

**Phase / behavior (no HP-form change; speed ramps)**
- Classic speed: ≥75% = 8 mph; <75% (6000 HP) = 9; <50% (4000) = 11; <25% (2000) = 14; <10% (800) = 17 mph
- Expert/Master speed: ≥75% = 12 mph; <75% (8400/10710) = 14; <66% (7392/9424) = 16; <50% (5600/7140) = 19; <33% (3696/4712) = 21; <25% (2800/3570) = 24; <10% (1120/1428) = 28; <5% (560/714) = 33; <3.5% (392/499) = 37; <2.5% (280/357) = 41 mph
- The Hungry deal more damage / gain defense as the body is damaged, and detach when sufficiently damaged. 1.4.4 change: Hungry no longer gain a 3rd stat bonus after 25% WoF health (they keep the 2nd bonus from 50%)

**Despawn**
- Reaches edge of world: despawns, and all players with Horrified die instantly ("was licked" / "got to 1st base...")
- If all players in the Underworld are killed: screen fades to black over 4 seconds, then it despawns
- Quitting and re-entering the world makes it despawn
- Escape-blocking: Horrified/The Tongue debuffs; Tongue kills instantly beyond 187.5 tiles ("tried to escape")

---

## Retinazer (via `The_Twins.md`)

**First form** (NPC 125)
- Max Life: `20000/30000/38250`
- Contact damage: `45/76/115`; Eye Laser `40/76/114`
- Defense: `10` (single value)
- KB Resist: `100%`

**Second form**
- Max Life: `8000/20000 [12000/30000] [15300/38250]`
- Contact damage: `67/114/172`; Death Laser `50/92/138`; Death Laser rapid fire `36/68/102`
- Defense: `20`
- KB Resist: `100%`

**Phase threshold**: transforms below 40% HP — Retinazer transforms at `8,000 / 12,000 / 15,300` health; defense increases to 20.

**Despawn**: The Twins must be killed before dawn (4:30 AM), otherwise they flee and despawn. In singleplayer both despawn timers must hit 0 simultaneously.

---

## Spazmatism (via `The_Twins.md`)

**First form** (NPC 126)
- Max Life: `23000/34500/43988`
- Contact damage: `50/85/128`; Cursed Flame `50/88/132` (Cursed Inferno 68.75% chance, 2–3/4–6/5–7.5 s)
- Defense: `10`
- KB Resist: `100%`

**Second form**
- Max Life: `9200/23000 [13800/34500] [17595/43988]`
- Contact damage: `75/127/192`; Eye Fire `60/108/162`
- Defense: `28`
- KB Resist: `100%`

**Phase threshold**: transforms below 40% HP — Spazmatism transforms at `9,200 / 13,800 / 17,595` health; defense increases to 28.

**Despawn**: same as above (flees at dawn 4:30 AM).

**The Twins combined infobox** (top of page): Max Life `43000 [64500] [82238]` (total), Defense `10`, KB Resist `100%`.

---

## Skeletron Prime (`Skeletron_Prime.md`)

**Head** (Skeletron Prime Head AI)
- Max Life: `28000/42000/53550`
- Damage: `47/80/120` (contact); `94/160/240` (while spinning); `9999` (during day)
- Defense: `24`; `48` (while spinning); `9999` (during day)
- KB Resist: `100%`

**Prime Cannon** (NPC 128)
- Max Life: `7000/10500/13387`
- Damage: `30/51/76` (contact); Bomb `80/160/240`
- Defense: `23`; KB `100%`

**Prime Saw** (NPC 129)
- Max Life: `9000/13500/17212`
- Damage: `56/95/143`; Defense: `38`; KB `100%`

**Prime Vice** (NPC 130)
- Max Life: `9000/13500/17212`
- Damage: `52/88/133`; Defense: `34`; KB `100%`

**Prime Laser** (NPC 131)
- Max Life: `6000/9000/11475`
- Damage: `29/49/74` (contact); Death Laser `50/100/150`
- Defense: `20`; KB `100%`

**Phase**: not HP-gated — every 10 seconds it enters a spinning phase for 6.67 seconds; head damage and defense double (94/160/240 damage, 48 defense); Expert spin speed 31 mph up to 76 mph at 37.5 tiles.

**Despawn/enrage**: if not killed before dawn (4:30 AM) it enrages permanently, behaving like a faster Dungeon Guardian — damage and defense increase to `9,999` (persists even after nightfall; killing it still counts). If the player is more than 375 tiles away, it moves downward and quickly despawns.

---

## The Destroyer (`The_Destroyer.md`)

**Whole boss infobox**
- Max Life: `80000/120000/153000`
- KB Resist: `100%`; no Defense row (single shared health pool)

**Segments table** (per-segment; NPC IDs 134/135/136)
| Part | Damage | Defense |
|---|---|---|
| Head (134) | `70/280/420` | `0` |
| Body (135) | `55/94/140` (contact); Death Laser `44/72/108` | `30` |
| Tail (136) | `40/68/102` | `35` |

- Probe Pink Lasers: `50/88/132` damage

**Body segment count**: the page states (Trivia) "The Destroyer is extremely long, measuring **82 segments including head and tail**, or 239 tiles in length." (No count given in the infobox itself.)

**Despawn**: only if the player dies or at dawn (4:30 AM) — "must be killed before dawn (4:30 AM), otherwise it flees and despawns"; despawns by traveling underground until off-screen. Probes never despawn while The Destroyer is alive.

---

## Plantera (`Plantera.md`)

**Plantera (first form, NPC 262)**
- Max Life: `30000 [42000] [53550]`
- Damage: `50/100/150` (contact); Seed `44/76/114`; Poison Seed `54/96/144`; Thorn Ball `62/108/162`
- Defense: `36`; KB Resist: `100%`

**Plantera (second form)**
- Max Life: `15000/30000 [21000/42000] [26775/53550]`
- Damage: `70/140/210`
- Defense: `10` ("her defense decreases significantly to 10"); KB Resist: `100%`

**Plantera's Hook** (NPC 263, Boss Part, Invincible)
- Max Life: `4000/8000/12000`; Damage `60/120/180`; Defense `24`; KB `0%/10%/20%`

**Plantera's Tentacle** (NPC 264)
- Max Life: `1000/2000/2550`; Damage `60/138/207`; Defense `20`; KB `0%/10%/20%`

**Spore** (projectile NPC)
- Max Life: `1`; Damage `70/140→126/210→189`; Defense `0`; KB `100%`

**Phase thresholds**
- Second form at **50% HP**: `15,000 / 21,000 / 26,775` — contact damage rises, defense drops to 10
- Poison Seeds and Thorn Balls only used below **80% HP**: `24,000 / 33,600 / 42,840`
- Expert Mode second form: 9 extra tentacles (3 per hook); body tentacles respawn (~5 s if all dead, scaling +5 s per living tentacle)

**Enrage / despawn behavior**
- Enraged when she leaves the Underground Jungle (surface, Underworld, or another biome): gains **double damage, double defense (quadruple defense in second form)**, increased movement speed, rushes the player; projectiles deal double damage with reduced cooldowns. No enrage in Hallowed/Corrupted/Crimson parts of the Underground Jungle if ≥140 Jungle grass/Hive/Lihzahrd Brick blocks are nearby. Behavior returns to normal on re-entering the biome.
- No dawn despawn is stated. The only despawn-related line is a history entry: "Now despawns when all players have been killed."
```
