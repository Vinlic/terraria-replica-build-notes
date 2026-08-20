# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-13T00:39:32.724Z

```
只读任务,不要改任何文件。在离线 wiki 镜像目录 ~/Project/GLM/SandboxWorld/terraria-wiki-md/ 里提取以下页面的**数值与规则**(文件名即页面标题;页面很长,先用 grep -n 定位关键词再读上下文,注意区分正文与导航/分类噪音):

1. Explosives.md —— Explosives(爆炸物方块)的伤害、半径。
2. Bomb.md —— 伤害、爆炸半径(tile 数)、能否摧毁某些方块。
3. Dynamite.md —— 伤害、爆炸半径。
4. Explosive_Bunny.md / Sticky_Bomb.md / Bouncy_Bomb.md / Dirt_Bomb.md / Bomb_Fish.md / Dynamite_Fish.md / Scarab_Bomb.md —— 半径与伤害(如有)。
5. Magic_Mirrors.md —— Magic Mirror / Ice Mirror 使用时间(use time)、冷却、有无 Chaos State。
6. Rod_of_Discord.md —— 使用时间、传送规则、Chaos State 数值(持续多少秒,多少秒内再次使用才触发,伤害多少)、专家/大师是否变化、是否被 Chaos State 阻止。
7. Cell_Phone.md —— 合成链之外:使用效果(传送回重生点?)、使用时间。
8. Spawn.md / Beds.md / Dungeon_spawn_point.md —— 床设重生点的条件(单向、需要墙/门?、地形要求)、重生逻辑(死后回重生点)。
9. Dart_Trap.md / Super_Dart_Trap.md / Flame_Trap.md / Spiked_Ball_Trap.md —— 飞镖机关伤害数值、发射周期(cooldown tick)、喷火机关伤害/持续时间、毒镖/超级飞镖版本差异;周期是否随机械装置变化。
10. Explosion-proof_objects.md —— 不可被爆炸摧毁的方块清单要点。

输出格式:每个页面一条,标注 文件名 + grep -n 记录的行号,引出原文句子(英文原句)。若页面没有该数值,明确说明。不要臆测。
```

---

## 📎 Attachment · skill_listing · 2026-08-13T00:39:32.726Z

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

## 🤖 Assistant · 2026-08-13T00:39:36.232Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The user wants me to extract numeric data and rules from specific wiki pages in an offline mirror directory. This is a read-only task. Let me start by verifying the files exist, then grep for keywords.

Let me plan the searches:
1. Explosives.md — damage, radius
2. Bomb.md — damage, radius (tiles), block destruction
3. Dynamite.md — damage, radius
4. Explosive_Bunny.md / Sticky_Bomb.md / Bouncy_Bomb.md / Dirt_Bomb.md / Bomb_Fish.md / Dynamite_Fish.md / Scarab_Bomb.md — radius and damage
5. Magic_Mirrors.md — use time, cooldown, Chaos State
6. Rod_of_Discord.md — use time, teleport rules, Chaos State values
7. Cell_Phone.md — use effect, use time
8. Spawn.md / Beds.md / Dungeon_spawn_point.md — bed spawn conditions, respawn logic
9. Dart_Trap.md / Super_Dart_Trap.md / Flame_Trap.md / Spiked_Ball_Trap.md — dart trap damage, cooldown, flame trap damage/duration
10. Explosion-proof_objects.md — explosion-proof blocks

Let me run parallel greps. I'll use absolute paths and grep -n. Let me be efficient with multi-tool parallel calls.
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:39:36.426Z · glm-x-preview-260804

```
我先确认文件存在并并行定位关键词。
```


---

## 🤖 Assistant · 2026-08-13T00:39:39.496Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/terraria-wiki-md/Explosives.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Bomb.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Dynamite.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Explosive_Bunny.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Sticky_Bomb.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Bouncy_Bomb.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Dirt_Bomb.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Bomb_Fish.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Dynamite_Fish.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Scarab_Bomb.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Magic_Mirrors.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Rod_of_Discord.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Cell_Phone.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Spawn.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Beds.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Dungeon_spawn_point.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Dart_Trap.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Super_Dart_Trap.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Flame_Trap.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Spiked_Ball_Trap.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Explosion-proof_objects.md",
 "description": "Verify all target wiki files exist"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:39.521Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/terraria-wiki-md/Beds.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Bomb_Fish.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Bomb.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Bouncy_Bomb.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Cell_Phone.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Dart_Trap.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Dirt_Bomb.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Dungeon_spawn_point.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Dynamite_Fish.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Dynamite.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Explosion-proof_objects.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Explosive_Bunny.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Explosives.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Flame_Trap.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Magic_Mirrors.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Rod_of_Discord.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Scarab_Bomb.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Spawn.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Spiked_Ball_Trap.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Sticky_Bomb.md
~/Project/GLM/SandboxWorld/terraria-wiki-md/Super_Dart_Trap.md

```


---

## 🤖 Assistant · 2026-08-13T00:39:40.051Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'damage|radius|tile' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Explosives.md | head -40",
 "description": "Grep Explosives.md for damage and radius"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:40.070Z

**📎 ToolResult**

```
24:Projectile created
34:  * Internal [Tile ID](Tile_IDs.md "Tile IDs"): **141**
35:  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **108**
43:Triggering Explosives cause a large explosion. The explosion destroys most placed blocks and items (except for [explosion-proof items](Explosion-proof_items "Explosion-proof items")) within a radius of 10 tiles[1], and deals damage within a 16.25×16.25-tile area[2]. The explosion inflicts a knockback of 10 (Extremely strong), deals 1000 / [2000](Expert_Mode.md "Expert Mode") / [3000](Master_Mode.md "Master Mode") base [damage](Damage.md "Damage") to players and 500 base damage to non-player entities.[3]
63:  * Explosives deal 10 ticks[4] of [global invincibility frames](Global_invincibility_frame.md "Global invincibility frame"), so multiple Explosives triggered at once can only deal damage to the same enemy once.
64:  * An Explosives block within the blast radius of another will not be activated, therefore chain reactions cannot be created with Explosives. Rather, the second Explosives will simply drop, as with other blocks.
67:  * ****__(Old-gen console and 3DS versions) Explosives' damage is considered as [PvP](PvP.md "PvP") damage, so the player will not drop any items when killed by Explosives.
79:  * [Desktop 1.4.5.0](Desktop_1.4.5.0 "Desktop 1.4.5.0"): Explosives' damage to players is now scaled with [difficulty](Difficulty.md "Difficulty"). Previously, they dealt 500 base damage to players.
85:  * [Desktop 1.4.0.4](Desktop_1.4.0.4 "Desktop 1.4.0.4"): Fixed a bug where Explosives counted as [PvP](PvP.md "PvP") damage, resulting in [coins](Coins.md "Coins") not dropping when the player was killed by them.
115:  1. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.5.6](1.4.5.6.md "1.4.5.6") source code, methods `Kill()` in `Terraria.Projectile.cs` and `ExplodeTiles()` in `Terraria.Projectile.cs`.
116:  2. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.5.6](1.4.5.6.md "1.4.5.6") source code, method `SetDefaults()` in `Terraria.Projectile.cs`.
117:  3. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.5.6](1.4.5.6.md "1.4.5.6") source code, methods `HitWireSingle()` in `Terraria.Wiring.cs` and `BombsHurtPlayers()` in `Terraria.Projectile.cs`.
1347:  *[DPS]: Damage per second
1356:enemies]: Maximum number of enemies Abigail can damage at once
1369:  *[0.05 mph]: 0.05 miles per hour (as measured by the Stopwatch item) or 0.04 tiles per second
1384:  *[15 mph]: 15 miles per hour (as measured by the Stopwatch item) or 11.25 tiles per second
1397:  *[34 mph]: 34 miles per hour (as measured by the Stopwatch item) or 24.93 tiles per second
1398:  *[30 mph]: 30 miles per hour (as measured by the Stopwatch item) or 22 tiles per second
1402:  *[41 mph]: 41 miles per hour (as measured by the Stopwatch item) or 30.07 tiles per second
1403:  *[21 mph]: 21 miles per hour (as measured by the Stopwatch item) or 15.4 tiles per second
1419:  *[17 mph]: 17 miles per hour (as measured by the Stopwatch item) or 12.47 tiles per second
1456:  *[53 mph]: 53 miles per hour (as measured by the Stopwatch item) or 38.87 tiles per second
1457:  *[88.6 mph]: 88.6 miles per hour (as measured by the Stopwatch item) or 64.97 tiles per second
1465:  *[102 mph]: 102 miles per hour (as measured by the Stopwatch item) or 75 tiles per second
1472:  *[184 mph]: 184 miles per hour (as measured by the Stopwatch item) or 135 tiles per second
1473:  *[72 mph]: 72 miles per hour (as measured by the Stopwatch item) or 52.5 tiles per second
1474:  *[82 mph]: 82 miles per hour (as measured by the Stopwatch item) or 60.13 tiles per second
1476:  *[51 mph]: 51 miles per hour (as measured by the Stopwatch item) or 37.4 tiles per second
1477:  *[66 mph]: 66 miles per hour (as measured by the Stopwatch item) or 48.4 tiles per second
1478:  *[77 mph]: 77 miles per hour (as measured by the Stopwatch item) or 56.25 tiles per second
1479:  *[100 mph]: 100 miles per hour (as measured by the Stopwatch item) or 73.125 tiles per second
1518:  *[35 mph]: 35 miles per hour (as measured by the Stopwatch item) or 25.31 tiles per second
1519:  *[43 mph]: 43 miles per hour (as measured by the Stopwatch item) or 31.5 tiles per second
1564:  *[61 mph]: 61 miles per hour (as measured by the Stopwatch item) or 45 tiles per second
1565:  *[80 mph]: 80 miles per hour (as measured by the Stopwatch item) or 58.67 tiles per second
1566:  *[64 mph]: 64 miles per hour (as measured by the Stopwatch item) or 46.93 tiles per second
1577:  *[4 mph]: 4 miles per hour (as measured by the Stopwatch item) or 3 tiles per second
1578:  *[6 mph]: 6 miles per hour (as measured by the Stopwatch item) or 4.5 tiles per second
1579:  *[10 mph]: 10 miles per hour (as measured by the Stopwatch item) or 7.5 tiles per second
1580:  *[12 mph]: 12 miles per hour (as measured by the Stopwatch item) or 9 tiles per second

```


---

## 🤖 Assistant · 2026-08-13T00:39:40.474Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'damage|radius|tile|destroy' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Bomb.md | head -60",
 "description": "Grep Bomb.md for damage and radius"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:40.494Z

**📎 ToolResult**

```
20:Damage| 100  
25:[Tooltip](Tooltips.md "Tooltips")|  _A small explosion that will destroy most tiles_  
31:Projectile created
42:  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **28**
66:A Bomb being thrown, damaging [Target Dummies](Target_Dummy.md "Target Dummy") and destroying tiles and walls.
68:The **Bomb** is an [explosive](Explosive "Explosive") that explodes 3 seconds after being thrown. The explosion breaks nearly all [blocks](Blocks.md "Blocks"), [background walls](Background_walls.md "Background walls"), and [furniture](Furniture.md "Furniture") within a 4-tile radius, except [explosion-proof objects](Explosion-proof_objects.md "Explosion-proof objects"). The explosion also deals 100 damage to all [enemies](Enemies.md "Enemies"), [critters](Critters.md "Critters"), and players (but not [NPCs](NPCs.md "NPCs")). Bombs work in [liquids](Liquids.md "Liquids"). 
72:The [Hardmode](Hardmode.md "Hardmode") variant of the Bomb is the [Power Bomb](Power_Bomb.md "Power Bomb"). Power Bombs have a greater radius and can explode [early Hardmode ores](Hardmode_ores.md "Hardmode ores"), unlike the Bomb. 
115:  * Like [Dynamite](Dynamite.md "Dynamite"), the Bomb's blast power is not affected by intervening material: for instance, if the Bomb is surrounded by [Dungeon Bricks](Dungeon_Bricks.md "Dungeon Bricks") (which are immune to explosions), it will still destroy other destructible blocks and damage entities outside of the Dungeon Bricks but inside the blast radius.
157:    * Now can destroy anything that [Dynamite](Dynamite.md "Dynamite") can, including some blocks it couldn't before, like [Spikes](Spike.md "Spike"), [Ebonstone](Ebonstone "Ebonstone") and [Obsidian](Obsidian.md "Obsidian").
158:    * After the [Wall of Flesh](Wall_of_Flesh.md "Wall of Flesh") has been defeated, it can also destroy [Hellstone](Hellstone.md "Hellstone").
1001:  * [Damage Booster](Damage_Booster.md "Damage Booster")
1701:  *[DPS]: Damage per second
1710:enemies]: Maximum number of enemies Abigail can damage at once
1723:  *[0.05 mph]: 0.05 miles per hour (as measured by the Stopwatch item) or 0.04 tiles per second
1738:  *[15 mph]: 15 miles per hour (as measured by the Stopwatch item) or 11 tiles per second
1746:  *[Critter]: May spawn a Worm, Gold Worm, or Maggot when destroyed, as described at the top of this article
1750:  *[31 mph]: 31 miles per hour (as measured by the Stopwatch item) or 22.5 tiles per second
1751:  *[34 mph]: 34 miles per hour (as measured by the Stopwatch item) or 24.93 tiles per second
1752:  *[30 mph]: 30 miles per hour (as measured by the Stopwatch item) or 22 tiles per second
1756:  *[41 mph]: 41 miles per hour (as measured by the Stopwatch item) or 30.07 tiles per second
1757:  *[21 mph]: 21 miles per hour (as measured by the Stopwatch item) or 15.4 tiles per second
1773:  *[17 mph]: 17 miles per hour (as measured by the Stopwatch item) or 12.47 tiles per second
1810:  *[53 mph]: 53 miles per hour (as measured by the Stopwatch item) or 38.87 tiles per second
1811:  *[88.6 mph]: 88.6 miles per hour (as measured by the Stopwatch item) or 64.97 tiles per second
1819:  *[102 mph]: 102 miles per hour (as measured by the Stopwatch item) or 75 tiles per second
1826:  *[184 mph]: 184 miles per hour (as measured by the Stopwatch item) or 135 tiles per second
1827:  *[72 mph]: 72 miles per hour (as measured by the Stopwatch item) or 52.5 tiles per second
1828:  *[82 mph]: 82 miles per hour (as measured by the Stopwatch item) or 60 tiles per second
1830:  *[51 mph]: 51 miles per hour (as measured by the Stopwatch item) or 37.5 tiles per second
1831:  *[66 mph]: 66 miles per hour (as measured by the Stopwatch item) or 48.75 tiles per second
1832:  *[77 mph]: 77 miles per hour (as measured by the Stopwatch item) or 56.25 tiles per second
1833:  *[100 mph]: 100 miles per hour (as measured by the Stopwatch item) or 73.125 tiles per second
1872:  *[35 mph]: 35 miles per hour (as measured by the Stopwatch item) or 25.5 tiles per second
1873:  *[43 mph]: 43 miles per hour (as measured by the Stopwatch item) or 31.5 tiles per second
1918:  *[61 mph]: 61 miles per hour (as measured by the Stopwatch item) or 45 tiles per second
1919:  *[80 mph]: 80 miles per hour (as measured by the Stopwatch item) or 58.67 tiles per second
1920:  *[64 mph]: 64 miles per hour (as measured by the Stopwatch item) or 46.93 tiles per second
1931:  *[4 mph]: 4 miles per hour (as measured by the Stopwatch item) or 3 tiles per second
1932:  *[6 mph]: 6 miles per hour (as measured by the Stopwatch item) or 4.5 tiles per second
1933:  *[10 mph]: 10 miles per hour (as measured by the Stopwatch item) or 7.5 tiles per second
1934:  *[12 mph]: 12 miles per hour (as measured by the Stopwatch item) or 9 tiles per second

```


---

## 🤖 Assistant · 2026-08-13T00:39:40.700Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'damage|radius|tile' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Dynamite.md | head -40",
 "description": "Grep Dynamite.md for damage and radius"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:40.718Z

**📎 ToolResult**

```
20:Damage| 250  
25:[Tooltip](Tooltips.md "Tooltips")|  _A large explosion that will destroy most tiles_  
31:Projectile created
42:  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **29**
54:**Dynamite** is an [explosive](Explosive "Explosive") that explodes 5 seconds after being thrown. The explosion breaks nearly all [blocks](Blocks.md "Blocks"), [background walls](Background_walls.md "Background walls"), and [furniture](Furniture.md "Furniture") within a radius of 7 tiles, except [explosion-proof objects](Explosion-proof_objects.md "Explosion-proof objects"). The explosion also deals 250 damage to all [enemies](Enemies.md "Enemies"), [critters](Critters.md "Critters"), and players (but not [NPCs](NPCs.md "NPCs")) within 7.8 tiles horizontally and vertically of the Dynamite.[1] Dynamite works in [liquids](Liquids.md "Liquids"). 
97:  * Like the [Bomb](Bomb.md "Bomb"), Dynamite's blast power is not affected by intervening material: for instance, if Dynamite is surrounded by [Dungeon Bricks](Dungeon_Bricks.md "Dungeon Bricks") (which are immune to explosions), it will still destroy other destructible blocks and damage entities outside of the Dungeon Bricks but inside the blast radius.
99:    * Damaging entities: The explosion covers a 15.625×15.625-tile square centered on the Dynamite, i.e. 7.8125 tiles in the four directions.
100:    * Destroying tiles: The explosion covers a circle with a diameter of 14 tiles centered on the Dynamite, i.e. 7 tiles in all directions.
102:    As a result, entities at the edge of the explosion may take damage even though the tiles there remain intact.
154:  1. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, method `PrepareBombToBlow()` in `Terraria.Projectile.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
977:  * [Damage Booster](Damage_Booster.md "Damage Booster")
1674:  *[DPS]: Damage per second
1683:enemies]: Maximum number of enemies Abigail can damage at once
1696:  *[0.05 mph]: 0.05 miles per hour (as measured by the Stopwatch item) or 0.04 tiles per second
1711:  *[15 mph]: 15 miles per hour (as measured by the Stopwatch item) or 11.25 tiles per second
1724:  *[34 mph]: 34 miles per hour (as measured by the Stopwatch item) or 24.93 tiles per second
1725:  *[30 mph]: 30 miles per hour (as measured by the Stopwatch item) or 22 tiles per second
1729:  *[41 mph]: 41 miles per hour (as measured by the Stopwatch item) or 30.07 tiles per second
1730:  *[21 mph]: 21 miles per hour (as measured by the Stopwatch item) or 15.4 tiles per second
1746:  *[17 mph]: 17 miles per hour (as measured by the Stopwatch item) or 12.47 tiles per second
1783:  *[53 mph]: 53 miles per hour (as measured by the Stopwatch item) or 38.87 tiles per second
1784:  *[88.6 mph]: 88.6 miles per hour (as measured by the Stopwatch item) or 64.97 tiles per second
1792:  *[102 mph]: 102 miles per hour (as measured by the Stopwatch item) or 75 tiles per second
1799:  *[184 mph]: 184 miles per hour (as measured by the Stopwatch item) or 135 tiles per second
1800:  *[72 mph]: 72 miles per hour (as measured by the Stopwatch item) or 52.5 tiles per second
1801:  *[82 mph]: 82 miles per hour (as measured by the Stopwatch item) or 60 tiles per second
1803:  *[51 mph]: 51 miles per hour (as measured by the Stopwatch item) or 37.4 tiles per second
1804:  *[66 mph]: 66 miles per hour (as measured by the Stopwatch item) or 48.4 tiles per second
1805:  *[77 mph]: 77 miles per hour (as measured by the Stopwatch item) or 56.25 tiles per second
1806:  *[100 mph]: 100 miles per hour (as measured by the Stopwatch item) or 73.125 tiles per second
1845:  *[35 mph]: 35 miles per hour (as measured by the Stopwatch item) or 25.31 tiles per second
1846:  *[43 mph]: 43 miles per hour (as measured by the Stopwatch item) or 31.5 tiles per second
1891:  *[61 mph]: 61 miles per hour (as measured by the Stopwatch item) or 45 tiles per second
1892:  *[80 mph]: 80 miles per hour (as measured by the Stopwatch item) or 58.67 tiles per second
1893:  *[64 mph]: 64 miles per hour (as measured by the Stopwatch item) or 46.93 tiles per second
1904:  *[4 mph]: 4 miles per hour (as measured by the Stopwatch item) or 3 tiles per second
1905:  *[6 mph]: 6 miles per hour (as measured by the Stopwatch item) or 4.5 tiles per second
1906:  *[10 mph]: 10 miles per hour (as measured by the Stopwatch item) or 7.5 tiles per second
1907:  *[12 mph]: 12 miles per hour (as measured by the Stopwatch item) or 9 tiles per second
1913:  *[18 mph]: 18 miles per hour (as measured by the Stopwatch item) or 13.125 tiles per second

```


---

## 🤖 Assistant · 2026-08-13T00:39:42.271Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good progress. Now the bomb variants, magic mirrors, rod of discord, cell phone.
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:39:42.471Z · glm-x-preview-260804

```
继续并行查第 4–7 组。
```


---

## 🤖 Assistant · 2026-08-13T00:39:43.117Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'damage|radius|tile|explo' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Explosive_Bunny.md | grep -v 'mph\\]:\\|DPS\\]' | head -30",
 "description": "Grep Explosive_Bunny.md for radius and damage"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:43.143Z

**📎 ToolResult**

```
1:# Explosive Bunny
3:> 原页面: `Explosive_Bunny`
5:# Explosive Bunny
7:Explosive Bunny
24:Projectile created
26:  * Explosive Bunny
29:  * Internal [Tile ID](Tile_IDs.md "Tile IDs"): **724**
30:  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **281**
32:Explosive Bunny
39:Damage| 0  
44:Projectile created
46:  * Explosive Bunny
54:  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **281**
56:The **Explosive Bunny** is an item that serves as ammunition for the [Bunny Cannon](Bunny_Cannon.md "Bunny Cannon"). Crafting it requires a [Bunny](Bunny.md "Bunny"), which must be caught with any [Bug Net](Bug_Net.md "Bug Net"). ****__(Desktop, Console and Mobile versions) It can also be released as a [critter](Critter "Critter"), and will wander around like other critters. It will always be placed at the player's feet when released, instead of at the cursor like with most other critters. 
58:If an Explosive Bunny critter is killed, it will explode, dealing 350 / [700](Expert_Mode.md "Expert Mode") / [1050](Master_Mode.md "Master Mode") damage to the player (175 damage to friendly [NPCs](NPCs.md "NPCs"), [critters](Critters.md "Critters"), and [enemies](Enemies.md "Enemies")) within a 8×8-tile area centered on it, but not destroying tiles.[1] Explosive Bunny projectiles and critters launched from the Bunny Cannon does not damage the player when it explodes. 
66:[](Explosive_Bunny.md "Explosive Bunny")Explosive Bunny| 
75:  * The explosion of the Explosive Bunny applies 10 ticks of [static invincibility frames](Static_invincibility_frame.md "Static invincibility frame") to enemies.[2]
76:    * This means if an enemy or boss is lured into a group of stacked Explosive Bunnies, only one of the explosions will deal damage.
77:  * Unlike other critters, the [Guide to Critter Companionship](Guide_to_Critter_Companionship.md "Guide to Critter Companionship")**** __(Desktop, Console and Mobile versions) does not render it immune to damage inflicted by the player.
78:  * When the [For the Worthy](For_the_Worthy.md "For the Worthy")**** __(Desktop, Console and Mobile versions) [special seed](Special_seed "Special seed") is active, any Bunny (except the [Gold](Gold_Bunny.md "Gold Bunny") or [Gem](Gem_Bunnies.md "Gem Bunnies") variants) spawned naturally, released by the player, or spawned by the [Bunny Statue](Bunny_Statue.md "Bunny Statue") has a 2/3 (66.67%) chance of being replaced by an Explosive Bunny.[3] Explosive Bunnies spawned via the Bunny Statue do not inflict damage when killed.
82:The [Eye of Cthulhu](Eye_of_Cthulhu.md "Eye of Cthulhu") being instantaneously killed with 50 Explosive Bunnies in version [1.4.1.2](1.4.1.2.md "1.4.1.2").
84:  * When fired from the [Bunny Cannon](Bunny_Cannon.md "Bunny Cannon"), the Explosive Bunny has the highest base damage of any weapon on the [ Desktop version](Desktop_version_history.md "Desktop version history"), [ Console version](Console_version.md "Console version"), [ Old-gen console version](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version"), and [ Mobile version](Mobile_version.md "Mobile version"). It is beaten only by the [3DS](Legacy%3A3DS_version "Legacy:3DS version")[](Legacy%3A3DS_version "3DS")-exclusive [Holy Hand Grenade](Holy_Hand_Grenade "Holy Hand Grenade"), which deals 600 damage.
85:  * Prior to version [1.4.4](1.4.4.md "1.4.4"), Explosive Bunnies did not cause [invincibility frames](Invincibility_frames "Invincibility frames"), so it was possible to one-shot bosses by luring them near a small cage with many Explosive Bunnies. This was a viable [Journey Mode](Journey_Mode.md "Journey Mode") speedrun tactic.
87:  * The [Bestiary](Bestiary.md "Bestiary") entry for the Explosive Bunny: _" Not the typical garden-variety bunny. This one has been tampered with, and has an explosive temper as a result."_
99:    * The explosion now has infinite pierce count. Previously, it cannot pierce.
100:    * The explosion now applies 10 ticks of [static invincibility frames](Static_invincibility_frame.md "Static invincibility frame") to enemies.
104:    * Can now be released as a critter, and will explode and deal damage upon death.
140:  1. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.5.5](1.4.5.5.md "1.4.5.5") source code, methods `DoDeathEvents()` in `Terraria.NPC.cs` and `Kill()` in `Terraria.Projectile.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
141:  2. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.5.5](1.4.5.5.md "1.4.5.5") source code, method `SetDefaults()` in `Terraria.Projectile.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
393:[Explosives](Explosives_\(class\) "Explosives \(class\)")

```


---

## 🤖 Assistant · 2026-08-13T00:39:43.613Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'damage|radius|tile|explo' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Sticky_Bomb.md | grep -v 'mph\\]:\\|DPS\\]' | head -30",
 "description": "Grep Sticky_Bomb.md for radius and damage"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:43.640Z

**📎 ToolResult**

```
20:Damage| 100  
25:[Tooltip](Tooltips.md "Tooltips")|  _A small explosion that will destroy most tiles  
31:Projectile created
39:Explosion|   
42:  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **37**
46:The **Sticky Bomb** is an [explosive](Explosive "Explosive") that functions like the [Bomb](Bomb.md "Bomb"), but sticks onto any [block](Block "Block") on contact. If the block it sticks to is removed by some means, it will fall until it hits another. 
126:[Explosives](Explosives_\(class\) "Explosives \(class\)")
178:  * [](Explosive_Jack_'O_Lantern "Explosive Jack 'O Lantern")[Explosive Jack 'O Lantern](Explosive_Jack_'O_Lantern "Explosive Jack 'O Lantern")
179:  * [](Exploding_Bullet.md "Exploding Bullet")[Exploding Bullet](Exploding_Bullet.md "Exploding Bullet")
181:  * [](Explosive_Bunny.md "Explosive Bunny")[Explosive Bunny](Explosive_Bunny.md "Explosive Bunny")
186:  * [](Explosives.md "Explosives")[Explosives](Explosives.md "Explosives")
435:[Explosives](Explosives_\(class\) "Explosives \(class\)")
497:  * [Exploding](Exploding_Bullet.md "Exploding Bullet")
528:  * [Explosive Jack 'O Lantern](Explosive_Jack_'O_Lantern "Explosive Jack 'O Lantern")
564:  * [Explosive Bunny](Explosive_Bunny.md "Explosive Bunny")
631:  * [Explosive Powder](Explosive_Powder.md "Explosive Powder")
945:  * [Damage Booster](Damage_Booster.md "Damage Booster")
1542:  * [Explosive Trap Cane/Rod/Staff](Explosive_Trap_sentry_summons.md "Explosive Trap sentry summons")
1569:[Explosive](Explosives_\(class\) "Explosives \(class\)")
1607:  * [Explosives](Category%3AExplosives "Category:Explosives")
1651:enemies]: Maximum number of enemies Abigail can damage at once
2057:  *[Radius]: Explosion radius in tiles
2097:  *[1.98]: Melee damage multiplier
2102:  *[2.26]: Ranged damage multiplier
2106:  *[11]: Ammo damage
2197:dmg]: Attack damage
2207:  *[Výbušniny v dnešní době letí. Kup je ještě teď!]: Explosives are da' bomb these days. Buy some now!
2214:  *[Koukni na mé zboží; mají výbušné ceny!]: Check out my goods; they have explosive prices!
2229:  *[Contact]: The damage without modifier and summon damage bonuses
2230:  *[Pounce]: The damage without modifier and summon damage bonuses

```


---

## 🤖 Assistant · 2026-08-13T00:39:44.138Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'damage|radius|tile|explo' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Bouncy_Bomb.md | grep -v 'mph\\]:\\|DPS\\]' | head -30",
 "description": "Grep Bouncy_Bomb.md for radius and damage"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:44.167Z

**📎 ToolResult**

```
19:Damage| 100  
24:[Tooltip](Tooltips.md "Tooltips")|  _A small explosion that will destroy most tiles  
30:Projectile created
38:Explosion|   
41:  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **516**
45:The **Bouncy Bomb** is an [explosive](Explosive "Explosive") that functions like the [Bomb](Bomb.md "Bomb"), but bounces off [blocks](Blocks.md "Blocks") more intensely. 
92:[Explosives](Explosives_\(class\) "Explosives \(class\)")
144:  * [](Explosive_Jack_'O_Lantern "Explosive Jack 'O Lantern")[Explosive Jack 'O Lantern](Explosive_Jack_'O_Lantern "Explosive Jack 'O Lantern")
145:  * [](Exploding_Bullet.md "Exploding Bullet")[Exploding Bullet](Exploding_Bullet.md "Exploding Bullet")
147:  * [](Explosive_Bunny.md "Explosive Bunny")[Explosive Bunny](Explosive_Bunny.md "Explosive Bunny")
152:  * [](Explosives.md "Explosives")[Explosives](Explosives.md "Explosives")
401:[Explosives](Explosives_\(class\) "Explosives \(class\)")
463:  * [Exploding](Exploding_Bullet.md "Exploding Bullet")
494:  * [Explosive Jack 'O Lantern](Explosive_Jack_'O_Lantern "Explosive Jack 'O Lantern")
530:  * [Explosive Bunny](Explosive_Bunny.md "Explosive Bunny")
597:  * [Explosive Powder](Explosive_Powder.md "Explosive Powder")
911:  * [Damage Booster](Damage_Booster.md "Damage Booster")
1508:  * [Explosive Trap Cane/Rod/Staff](Explosive_Trap_sentry_summons.md "Explosive Trap sentry summons")
1535:[Explosive](Explosives_\(class\) "Explosives \(class\)")
1576:  * [Explosives](Category%3AExplosives "Category:Explosives")
1608:enemies]: Maximum number of enemies Abigail can damage at once

```


---

## 🤖 Assistant · 2026-08-13T00:39:44.586Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'damage|radius|tile|explo' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Dirt_Bomb.md | grep -v 'mph\\]:\\|DPS\\]' | head -30",
 "description": "Grep Dirt_Bomb.md for radius and damage"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:44.605Z

**📎 ToolResult**

```
19:Damage| 100  
24:[Tooltip](Tooltips.md "Tooltips")|  _A small explosion that will spread dirt_  
29:Projectile created
37:Explosion|   
40:  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **910**
42:A Dirt Bomb exploding.
44:The **Dirt Bomb** is an [explosive](Explosive "Explosive") that functions like the [Bomb](Bomb.md "Bomb"), but its explosion will place [Dirt Blocks](Dirt_Block.md "Dirt Block") in open spaces, instead of destroying blocks. Existing blocks within the explosion radius will remain unaffected. 
73:  * If the player is standing directly on the Dirt Bomb upon exploding, it will deal regular Bomb damage and not create dirt.
75:  * The dirt generated by the bomb will not replace liquids. If the explosion occurs in a pool of water, the resulting dirt will "hold" the water; mining the dirt will again free the water.
79:  * The Dirt Bomb is useful for quickly filling in holes left by explosions or mining, as well as creating hills or filling in a large area quickly. This is especially noteworthy with [Meteorite](Meteorite_\(biome\) "Meteorite \(biome\)") crash sites – depending on the size of the meteorite, one can remove all of the ore and 40–60 bombs will be enough to completely repair the impact damage. 
81:  * The bomb can yield more dirt than the 25 required to craft it, up to 57 blocks if it explodes in midair, or 56 if it is suspended off the ground by only a single block. This can be used to create an infinite supply of dirt, which can be crafted into [Mud](Mud "Mud"), which can then be used to create infinite [Chlorophyte Ore](Chlorophyte_Ore.md "Chlorophyte Ore").
89:  * [Desktop 1.4.0.5](Desktop_1.4.0.5 "Desktop 1.4.0.5"): Fixed a bug where it would not produce dirt when exploding on half-slabs.
107:[Explosives](Explosives_\(class\) "Explosives \(class\)")
159:  * [](Explosive_Jack_'O_Lantern "Explosive Jack 'O Lantern")[Explosive Jack 'O Lantern](Explosive_Jack_'O_Lantern "Explosive Jack 'O Lantern")
160:  * [](Exploding_Bullet.md "Exploding Bullet")[Exploding Bullet](Exploding_Bullet.md "Exploding Bullet")
162:  * [](Explosive_Bunny.md "Explosive Bunny")[Explosive Bunny](Explosive_Bunny.md "Explosive Bunny")
167:  * [](Explosives.md "Explosives")[Explosives](Explosives.md "Explosives")
513:Exploration
609:  * [Explosives](Category%3AExplosives "Category:Explosives")
641:enemies]: Maximum number of enemies Abigail can damage at once
1047:  *[Radius]: Explosion radius in tiles
1087:  *[1.98]: Melee damage multiplier
1092:  *[2.26]: Ranged damage multiplier
1095:  *[105]: Final weapon damage
1096:  *[11]: Ammo damage
1187:dmg]: Attack damage
1197:  *[Výbušniny v dnešní době letí. Kup je ještě teď!]: Explosives are da' bomb these days. Buy some now!
1204:  *[Koukni na mé zboží; mají výbušné ceny!]: Check out my goods; they have explosive prices!
1219:  *[Contact]: The damage without modifier and summon damage bonuses
1220:  *[Pounce]: The damage without modifier and summon damage bonuses

```


---

## 🤖 Assistant · 2026-08-13T00:39:45.048Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'damage|radius|tile|explo' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Bomb_Fish.md | grep -v 'mph\\]:\\|DPS\\]' | head -30",
 "description": "Grep Bomb_Fish.md for radius and damage"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:45.071Z

**📎 ToolResult**

```
19:Damage| 100  
24:[Tooltip](Tooltips.md "Tooltips")|  _A small explosion that will destroy most tiles_  
29:Projectile created
37:Explosion|   
40:  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **519**
42:A Bomb Fish exploding, destroying blocks and damaging a [Target Dummy](Target_Dummy.md "Target Dummy"). Note how the Bomb Fish arcs instead of heading directly for the cursor.
44:The **Bomb Fish** is an [explosive](Explosive "Explosive") that functions identically to the [Sticky Bomb](Sticky_Bomb.md "Sticky Bomb"), but does not slow down in [water](Water.md "Water"). It is obtained through fishing, with the number obtained depending on the player's [Fishing Power](Fishing_Power.md "Fishing Power"). 
88:  1. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.5.5](1.4.5.5.md "1.4.5.5") source code, method `AI_061_FishingBobber_GiveItemToPlayer()` in `Terraria.Projectile.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
92:[Explosives](Explosives_\(class\) "Explosives \(class\)")
144:  * [](Explosive_Jack_'O_Lantern "Explosive Jack 'O Lantern")[Explosive Jack 'O Lantern](Explosive_Jack_'O_Lantern "Explosive Jack 'O Lantern")
145:  * [](Exploding_Bullet.md "Exploding Bullet")[Exploding Bullet](Exploding_Bullet.md "Exploding Bullet")
147:  * [](Explosive_Bunny.md "Explosive Bunny")[Explosive Bunny](Explosive_Bunny.md "Explosive Bunny")
152:  * [](Explosives.md "Explosives")[Explosives](Explosives.md "Explosives")
401:[Explosives](Explosives_\(class\) "Explosives \(class\)")
463:  * [Exploding](Exploding_Bullet.md "Exploding Bullet")
494:  * [Explosive Jack 'O Lantern](Explosive_Jack_'O_Lantern "Explosive Jack 'O Lantern")
530:  * [Explosive Bunny](Explosive_Bunny.md "Explosive Bunny")
597:  * [Explosive Powder](Explosive_Powder.md "Explosive Powder")
911:  * [Damage Booster](Damage_Booster.md "Damage Booster")
1508:  * [Explosive Trap Cane/Rod/Staff](Explosive_Trap_sentry_summons.md "Explosive Trap sentry summons")
1535:[Explosive](Explosives_\(class\) "Explosives \(class\)")
1576:  * [Explosives](Category%3AExplosives "Category:Explosives")
1608:enemies]: Maximum number of enemies Abigail can damage at once

```


---

## 🤖 Assistant · 2026-08-13T00:39:45.513Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'damage|radius|tile|explo' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Dynamite_Fish.md | grep -v 'mph\\]:\\|DPS\\]' | head -30",
 "description": "Grep Dynamite_Fish.md for radius and damage"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:45.539Z

**📎 ToolResult**

```
18:enemies]: Maximum number of enemies Abigail can damage at once
424:  *[Radius]: Explosion radius in tiles
464:  *[1.98]: Melee damage multiplier
469:  *[2.26]: Ranged damage multiplier
472:  *[105]: Final weapon damage
473:  *[11]: Ammo damage
564:dmg]: Attack damage
574:  *[Výbušniny v dnešní době letí. Kup je ještě teď!]: Explosives are da' bomb these days. Buy some now!
581:  *[Koukni na mé zboží; mají výbušné ceny!]: Check out my goods; they have explosive prices!
596:  *[Contact]: The damage without modifier and summon damage bonuses
597:  *[Pounce]: The damage without modifier and summon damage bonuses
598:  *[Threshold]: If the player's summon damage bonuses reach it, Ruthless will become the best modifier

```


---

## 🤖 Assistant · 2026-08-13T00:39:45.975Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'damage|radius|tile|explo' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Scarab_Bomb.md | grep -v 'mph\\]:\\|DPS\\]' | head -30",
 "description": "Grep Scarab_Bomb.md for radius and damage"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:45.996Z

**📎 ToolResult**

```
19:Damage| 100  
24:[Tooltip](Tooltips.md "Tooltips")|  _A narrow explosion that will destroy most tiles  
25:Explosion aims away from your position_  
30:Projectile created
38:Explosion|   
41:  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **773**
56:A player using Scarab Bombs. Note how the explosion aims away from the player.
58:The **Scarab Bomb** is an [explosive](Explosive "Explosive") that functions like the [Sticky Bomb](Sticky_Bomb.md "Sticky Bomb"), but instead creates a 21-tile long and 3-tile wide shaft. The explosion will always aim away from the player's position, even after being thrown. 
77:  * Even though the explosion aims away from the player, it can damage a player if they are too close.
81:  * The characteristic, linear shaft created by a Scarab Bomb's explosion makes the bombs useful for several different situations: 
85:    * In the [Dungeon](Dungeon.md "Dungeon"), they are useful for clearing the [Spikes](Spike.md "Spike") lining covered pits. In this context, the [explosion-proof](Explosion-proof_objects.md "Explosion-proof objects") nature of [Dungeon Bricks](Dungeon_Bricks.md "Dungeon Bricks") becomes an advantage.
119:[Explosives](Explosives_\(class\) "Explosives \(class\)")
171:  * [](Explosive_Jack_'O_Lantern "Explosive Jack 'O Lantern")[Explosive Jack 'O Lantern](Explosive_Jack_'O_Lantern "Explosive Jack 'O Lantern")
172:  * [](Exploding_Bullet.md "Exploding Bullet")[Exploding Bullet](Exploding_Bullet.md "Exploding Bullet")
174:  * [](Explosive_Bunny.md "Explosive Bunny")[Explosive Bunny](Explosive_Bunny.md "Explosive Bunny")
179:  * [](Explosives.md "Explosives")[Explosives](Explosives.md "Explosives")
428:[Explosives](Explosives_\(class\) "Explosives \(class\)")
490:  * [Exploding](Exploding_Bullet.md "Exploding Bullet")
521:  * [Explosive Jack 'O Lantern](Explosive_Jack_'O_Lantern "Explosive Jack 'O Lantern")
557:  * [Explosive Bunny](Explosive_Bunny.md "Explosive Bunny")
624:  * [Explosive Powder](Explosive_Powder.md "Explosive Powder")
938:  * [Damage Booster](Damage_Booster.md "Damage Booster")
1535:  * [Explosive Trap Cane/Rod/Staff](Explosive_Trap_sentry_summons.md "Explosive Trap sentry summons")
1562:[Explosive](Explosives_\(class\) "Explosives \(class\)")
1603:  * [Explosives](Category%3AExplosives "Category:Explosives")
1636:enemies]: Maximum number of enemies Abigail can damage at once
2042:  *[Radius]: Explosion radius in tiles
2082:  *[1.98]: Melee damage multiplier
2087:  *[2.26]: Ranged damage multiplier
2091:  *[11]: Ammo damage

```


---

## 🤖 Assistant · 2026-08-13T00:39:46.634Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'use time|cooldown|chaos|spell|teleport|mirror' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Magic_Mirrors.md | grep -v 'mph\\]:\\|DPS\\]' | head -30",
 "description": "Grep Magic_Mirrors.md for use time and cooldown"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:46.665Z

**📎 ToolResult**

```
1:# Magic Mirrors
3:> 原页面: `Magic_Mirrors`
5:# Magic Mirrors
7:Magic Mirror
15:[Use time](Use_time.md "Use time")| 90 (Snail)  
16:[Tooltip](Tooltips.md "Tooltips")|  _Gaze in the mirror to return home_  
29:Ice Mirror
37:[Use time](Use_time.md "Use time")| 90 (Snail)  
38:[Tooltip](Tooltips.md "Tooltips")|  _Gaze in the mirror to return home_  
78:The Magic Mirror's animation.
80:The **Magic Mirror** is a [pre-Hardmode](Pre-Hardmode.md "Pre-Hardmode") [tool](Tool "Tool"). When used, it plays an animation before teleporting the player to their [spawn point](Spawn_point "Spawn point"). Compared to the [Recall Potion](Recall_Potion.md "Recall Potion"), the Magic Mirror has unlimited uses, but a delay of 0.75 seconds (45 ticks),[1] which is longer than the Recall Potion's 0.167 seconds (10 ticks)[1] before teleporting.[2]
82:The **Ice Mirror**** __(Desktop, Console and Mobile versions)** is a functionally identical alternative to the Magic Mirror. 
84:Magic Mirrors can be found in [Chests](Chests.md "Chests") generated in the [Underground](Underground.md "Underground") and [Cavern](Cavern.md "Cavern") layers. Ice Mirrors can be found in [Frozen Chests](Frozen_Chest.md "Frozen Chest") generated in the [Ice biome](Ice_biome.md "Ice biome"). Newly created [characters](Characters "Characters") in [Journey Mode](Journey_Mode.md "Journey Mode")**** __(Desktop, Console and Mobile versions) spawn with a Magic Mirror. 
92:[](Desktop_version_history.md "Desktop version") [](Console_version.md "Console version") [](Mobile_version.md "Mobile version") only:[](Magic_Mirror "Magic Mirror")[Magic Mirror](Magic_Mirror "Magic Mirror")| 
113:  * [](Magic_Mirror "Magic Mirror")[Magic Mirror](Magic_Mirror "Magic Mirror")
118:  * [](Ice_Mirror "Ice Mirror")[Ice Mirror](Ice_Mirror "Ice Mirror")**** __(Desktop, Console and Mobile versions)
123:  * [](Any_Magic_Mirror.md "Any Magic Mirror")[Any Magic Mirror](Any_Magic_Mirror.md "Any Magic Mirror")
131:  * Teleporting will reset the player's [fall damage](Fall_damage.md "Fall damage").
132:  * On the [ Old-gen console version](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version"), opening a storage item such as a [Chest](Chest "Chest") or a [Piggy Bank](Piggy_Bank.md "Piggy Bank") while the Magic Mirror animation plays will crash the game upon arrival.
136:  * Due to having a longer delay when teleporting compared to [Recall Potions](Recall_Potion.md "Recall Potion"), the player may find decrafting Magic Mirrors via [Shimmer](Shimmer.md "Shimmer") more valuable (given they have a steady supply of Recall Potions).
140:  * Due to their reflective properties, [mirrors](https://en.wikipedia.org/wiki/en:Mirror#Literature "wikipedia:en:Mirror") play a powerful role in cultural literature and are often depicted as magical in nature. In video games, it is common for them to be used as a magical means of transportation between distant locations, into secret spaces, or even into other dimensions.
141:  * Magic Mirrors have one of the slowest [use times](Use_time.md "Use time") in the game, tied with the [Magic Conch](Magic_Conch.md "Magic Conch"), [Demon Conch](Demon_Conch.md "Demon Conch"), [Cell Phone](Cell_Phone.md "Cell Phone"), [Shellphone](Shellphone.md "Shellphone"), and [Snake Charmer's Flute](Snake_Charmer's_Flute.md "Snake Charmer's Flute").
142:  * On earlier versions of [ Old-gen console](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version"), it was possible to use the Magic Mirror to gain permanent invincibility by using it before invincibility ran out. This has since been patched out.
143:  * Magic Mirrors release light emitting particles while teleporting the player. They release an increased volume of them when the player arrives at their destination.
151:  * [Desktop 1.4.4](Desktop_1.4.4 "Desktop 1.4.4"): Magic Mirror can now be crafted.
153:  * [Desktop 1.4.0.4](Desktop_1.4.0.4 "Desktop 1.4.0.4"): Fixed Collector's Edition [Carrot](Carrot.md "Carrot") overriding the Magic Mirror in a [Journey Mode](Journey_Mode.md "Journey Mode") character's inventory.
155:  * [Desktop 1.4.0.1](Desktop_1.4.0.1 "Desktop 1.4.0.1"): The Magic Mirror is now a starting item for Journey Mode characters.
157:  * [Desktop 1.3.1](Desktop_1.3.1 "Desktop 1.3.1"): Magic Mirror sprite updated. Old sprite was .
160:    * Added the Ice Mirror.
167:  * [Desktop-Release](Desktop-Release.md "Desktop-Release"): Introduced the Magic Mirror.

```


---

## 🤖 Assistant · 2026-08-13T00:39:47.231Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'use time|chaos|teleport|second|damage|expert|master' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Rod_of_Discord.md | grep -v 'mph\\]:\\|DPS\\]' | head -40",
 "description": "Grep Rod_of_Discord.md for use time and Chaos State"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:47.254Z

**📎 ToolResult**

```
20:[Use time](Use_time.md "Use time")| 20 (Very fast)  
21:[Tooltip](Tooltips.md "Tooltips")|  _Teleports you to the position of the cursor  
22:Causes the chaos state ([](Desktop_version_history.md "Desktop version"))  
23:Teleports you to the position of the cursor ([](Mobile_version.md "Mobile version"))_  
30:Debuff| [](Rod_of_Discord.md "Chaos State")Chaos State  
34:Duration| 6 seconds  
49:Expert
51:Master
55:~~[Chaos Elemental](Chaos_Elemental.md "Chaos Elemental")~~ [Chaos Elemental](Chaos_Elemental.md "Chaos Elemental")| 1| 0.2%[0.25%](Expert_Mode.md "Expert Mode")  
61:The **Rod of Discord** is a [Hardmode](Hardmode.md "Hardmode") [tool](Tool "Tool") that has a 1/500 (0.2%) / [1/400 (0.25%)](Expert_Mode.md "Expert Mode") chance of being dropped by [Chaos Elementals](Chaos_Elemental.md "Chaos Elemental"). When used, it instantly teleports the player to the location of the cursor and inflicts the **Chaos State** [debuff](Debuff "Debuff") on the player for 6 seconds. Using the Rod of Discord while this debuff is active causes the player to lose health equal to 1/7 (14.29%) of their maximum [health](Health.md "Health"). 
79:[](Achievements#Organized_Chaos "Achievements")
81:**[Organized Chaos](Achievements#Organized_Chaos "Achievements")**  • _“Find the ultra rare Rod of Discord.”_
90:  * The Rod of Discord cannot be used to teleport into the [Jungle Temple](Jungle_Temple.md "Jungle Temple") prior to defeating [Plantera](Plantera.md "Plantera"). 
91:    * More precisely,[1] the player will not be teleported pre-Plantera to any location that is below the [surface](Surface.md "Surface") and has an [unsafe](Unsafe_wall.md "Unsafe wall") [Lihzahrd Brick Wall](Lihzahrd_Brick_Wall.md "Lihzahrd Brick Wall") as [background wall](Background_wall "Background wall"). In worlds with the [Remix](Remix.md "Remix") seed enabled, this restriction extends above the surface.
92:  * The health loss inflicted by Chaos State cannot be reduced in any way or negated through [dodge](Dodge.md "Dodge") effects. It also bypasses and does not trigger [invincibility frames](Invincibility_frame.md "Invincibility frame"). It does not bypass invincibility from [Godmode](Godmode.md "Godmode"), however.
93:  * The Rod of Discord's teleport range is limited to 60 tiles horizontally and 37.5 tiles vertically from the player's center[2].
94:  * The target location must be at least 3 tiles high and 2 tiles wide. Pressing the [`⚒ Use / Attack`](Game_controls.md "Game controls") button will always place the player's feet at the cursor position. Thus, in order to teleport into a 3-tile-high opening, the player must aim at the floor. Unsuccessful teleports play the same sound, but do not inflict the debuff. 
96:  * Teleporting resets [fall damage](Fall_damage.md "Fall damage") to begin at the height at which the player teleported to.
99:  * If the player only taps the [`⚒ Use / Attack`](Game_controls.md "Game controls") button with the Rod of Discord on the [ Mobile version](Mobile_version.md "Mobile version"), they will be teleported slightly to the right (and above if blocks or furniture are obstructing the path). Using the thumbpad can yield mixed results if the aim mode is set to "Aim & Use" rather than "Aim Only".
100:  * The Rod of Discord cannot be used to teleport past [Unbreakable Walls](Unbreakable_Wall.md "Unbreakable Wall") (generated naturally in [Dual Dungeons](Dual_Dungeons "Dual Dungeons") worlds).[3]
104:  * The Rod of Discord is arguably the most powerful movement tool in the game; besides being an obvious boon to traversing terrain, it allows the player to dodge high-damage or difficult to avoid attacks, including the [Moon Lord](Moon_Lord.md "Moon Lord")'s Phantasmal Deathray, contact damage from the [Dungeon Guardian](Dungeon_Guardian.md "Dungeon Guardian"), and several of the [Empress of Light](Empress_of_Light.md "Empress of Light")'s attacks. It is also very useful in helping to catch [Truffle Worms](Truffle_Worm.md "Truffle Worm").
106:  * Since this item is one of the few ways to deal self-damage on command, it can be used with the [Shrimpy Truffle](Shrimpy_Truffle.md "Shrimpy Truffle") or the [Panic Necklace](Panic_Necklace.md "Panic Necklace") to activate the speed boost. Furthermore, it allows easy obtainment of the [The Frequent Flyer](The_Frequent_Flyer.md "The Frequent Flyer") [achievement](Achievement "Achievement").
110:  * Dying from teleporting during the Chaos State will display unique [death messages](Death_message.md "Death message"): 
117:  * Successfully using the Rod of Discord leaves behind pink glowing particles at the location of the player, as well as produces those particles at the teleport location. It also coats the player with glowing particles which gradually lose their glow as they disappear.
127:  * [Desktop 1.4.1](Desktop_1.4.1 "Desktop 1.4.1"): Teleport range is now limited to 960 pixels (60 tiles) horizontally and 600 pixels (37.5 tiles) vertically from the player's center.
130:    * Now has an increased drop rate of 1/400 (0.25%) in Expert Mode.
131:    * Now leaves a trail when teleporting.
133:  * [Desktop 1.3.0.4](Desktop_1.3.0.4 "Desktop 1.3.0.4"): Teleporting now quickly shifts the viewpoint instead of instantly setting it to the destination point.
135:  * [Desktop 1.3.0.1](Desktop_1.3.0.1 "Desktop 1.3.0.1"): Chaos State damage reduced from one sixth to one seventh of user's total health, and duration decreased from 8 to 6 seconds.
140:    * Chaos State damage reduced from one fifth to one sixth of user's total health, and duration decreased from 10 to 8 seconds.
145:    * Inflicts [Chaos State](Chaos_State "Chaos State") upon use to deter teleport spamming.
171:  1. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, method `ItemCheck_UseTeleportRod()` in `Terraria.Player.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
173:  3. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.5.3](1.4.5.3.md "1.4.5.3") source code, method `ItemCheck_UseTeleportRod()` in `Terraria.Player.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
640:  * [](Damage_Booster.md "Damage Nebula")[Damage Nebula](Damage_Booster.md "Damage Booster")
933:  * [](Rod_of_Discord.md "Chaos State")Chaos State
995:  *[100%]: Master Mode
998:  *[300]: Expert Mode
999:  *[400]: Expert Mode
1000:  *[160]: Expert Mode
1001:  *[240]: Master Mode

```


---

## 🤖 Assistant · 2026-08-13T00:39:47.821Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'use time|spawn|teleport|effect|info' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Cell_Phone.md | grep -v 'mph\\]:\\|DPS\\]' | head -40",
 "description": "Grep Cell_Phone.md for use time and effect"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:47.847Z

**📎 ToolResult**

```
9:**[Desktop](Category%3ADesktop_content "Category:Desktop content")/[Console](Category%3AConsole_content "Category:Console content")/[Mobile](Category%3AMobile_content "Category:Mobile content")-Only Content**: This information applies _only_ to the **[Desktop](Desktop_version_history.md "Desktop version history")** , **[Console](Console_version.md "Console version")** , and **[Mobile](Mobile_version.md "Mobile version")** versions of _[Terraria](Terraria.md "Terraria")_.
19:[Use time](Use_time.md "Use time")| 90 (Snail)  
38:The **Cell Phone** is a post-[Skeletron](Skeletron.md "Skeletron") [informational item](Informational_item "Informational item") and [tool](Tool "Tool") that combines the functions of the [PDA](PDA.md "PDA") and the [Magic Mirrors](Magic_Mirrors.md "Magic Mirrors"), displaying all information and allowing the player to teleport to their [spawn point](Spawn_point "Spawn point"). Unlike most informational items, the Cell Phone does not double as an [accessory](Accessory "Accessory"). It instead functions solely from the player's main [inventory](Inventory.md "Inventory"). 
135:Example information displayed by a Cell Phone.
138:  * The info it provides will be shared with players of the same team in [multiplayer](Multiplayer.md "Multiplayer") that are within 50 tiles.
157:  * It has one of the slowest [use times](Use_time.md "Use time") in the game, tied with the [Magic Conch](Magic_Conch.md "Magic Conch"), [Demon Conch](Demon_Conch.md "Demon Conch"), [Magic Mirrors](Magic_Mirrors.md "Magic Mirrors"), [Shellphone](Shellphone.md "Shellphone"), and [Snake Charmer's Flute](Snake_Charmer's_Flute.md "Snake Charmer's Flute").
621:  * [Informational items](Category%3AInformational_items "Category:Informational items")
689:  *[Critter]: May spawn a Worm, Gold Worm, or Maggot when destroyed, as described at the top of this article

```


---

## 🤖 Assistant · 2026-08-13T00:39:52.338Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Dynamite_Fish.md didn't get good content — the grep didn't show lines near the top. Let me check the top of Dynamite_Fish.md directly. Also need: Spawn.md / Beds.md / Dungeon_spawn_point.md, traps, Explosion-proof_objects.md, and verify Chaos State / Mirror cooldown details, Rod_of_Discord expert/master variation (drop rate differs in expert). Also need to check Magic Mirror cooldown.

Let me read Dynamite_Fish.md head, and grep beds/spawn/dungeon/traps/explosion-proof.
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:39:52.467Z · glm-x-preview-260804

```
查 Dynamite_Fish.md 头部及第 8–10 组。
```


---

## 🤖 Assistant · 2026-08-13T00:39:52.779Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "head -50 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Dynamite_Fish.md",
 "description": "Read Dynamite_Fish.md header section"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:52.797Z

**📎 ToolResult**

```
# Dynamite Fish

> 原页面: `Dynamite_Fish`

[Dynamite Fish](./Angler/Quests#Dynamite_Fish)
  *[1 required]: Journey Mode
  *[Qty.]: Quantity
  *[100%]: Mode Expert
  *[DPS]: Damage per second
  *[sic]: sīc erat scriptum (Latin: “thus it was written”) – any typographical or other errors in this quote are intentionally reproduced, exactly as they appear in the source.
  *[300]: Mode Master
  *[400]: Legendary Mode
  *[160]: Expert Mode
  *[240]: Master Mode
  *[3 required]: Journey Mode
  *[#]: Number of summons, i.e. times that the Desert Tiger Staff was used
  *[Max.  
enemies]: Maximum number of enemies Abigail can damage at once
  *[HM]: Hardmode
  *[**Click/tap here** to reveal this content. _(there may be a slight delay)_]: This content exists externally. Once you click, there may be a small delay while it is downloaded.
  *[**Klik/tap disini** untuk melihat isi konten. _(mungkin akan sedikit delay)_]: Konten ini tersedia secara eksternal. Ketika di klik, mungkin akan ada sedikit delay ketika melihat isi konten.
  *[**Bấm/Chạm vào đây** để hiển thị nội dung này. _(có thể sẽ bị delay một chút)_]: Nội dung này được lấy từ các nguồn bên ngoài. Khi bấm vào, có thể sẽ bị delay một chút trong khi nó tải.
  *[8]: Expert Mode
  *[10]: Master Mode
  *[120]: Expert Mode
  *[150]: Mode Expert
  *[13]: Chế độ Master
  *[195]: Master Mode
  *[Verify]: Contradicts with [[NPC spawning#Choosing a spot to spawn the NPC]]
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
  *[199/10000 (1.99%)]: Expert Mode
  *[membutuhkan 1]: Mode Journey
  *[1,99%]: Expert Mode
  *[1/50 (2%)]: Mode Expert
  *[200 required]: Journey Mode
  *[15 mph]: 15 miles per hour (as measured by the Stopwatch item) or 11.25 tiles per second
  *[16 mph]: 16 mil per jam (diukur dengan item Stopwatch) atau 11.73 blok per detik
  *[20 required]: Journey Mode
  *[180]: Expert Mode
  *[270]: Master Mode

```


---

## 🤖 Assistant · 2026-08-13T00:39:53.403Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'spawn point|respawn|set.*spawn|wall|door|background|valid|one.?way' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Beds.md | head -50",
 "description": "Grep Beds.md for spawn conditions"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:53.427Z

**📎 ToolResult**

```
28:**Beds** are [furniture](Furniture.md "Furniture") items which allow the player to set a new [spawn](Spawn.md "Spawn") point by pressing the [`⚷ Open / Activate`](Game_controls.md "Game controls") button on the foot half of the Bed, if the Bed is placed in a valid bedroom (see details below). On the [ Desktop version](Desktop_version_history.md "Desktop version history"), [ Console version](Console_version.md "Console version"), and [ Mobile version](Mobile_version.md "Mobile version"), Beds also allow the player to sleep in them by pressing the [`⚷ Open / Activate`](Game_controls.md "Game controls") button on the head half of the Bed. This makes time pass five times faster and, similar to [Chairs](Chairs.md "Chairs") and [Sofas](Sofas.md "Sofas"), gives a boost to [health regeneration](Health_regeneration.md "Health regeneration"). 
34:## Setting player spawn point
36:Pressing [`⚷ Open / Activate`](Game_controls.md "Game controls") on the foot of a Bed, when it is placed in a valid bedroom, sets the player's spawn point to that Bed. This is signified by the [status message](Status_message "Status message") _“ Spawn point set!”_. When the same is done on a Bed that has already been set as the player's spawn point, the status message _“ Spawn point removed!”_ is shown, and the player's spawn point is set back to the world's default. 
38:****__(Desktop, Console and Mobile versions) The Bed set as the player's current spawn point will be indicated with a  bed icon on the player's [minimap](Minimap.md "Minimap"). 
40:A valid bedroom for spawning, although not for sleeping due to the block above the foot of the Bed.
42:The requirements for a valid bedroom are: 
44:  * A frame of the same area as a [valid house](House#Minimal_house_sizes "House").
45:  * No area greater than 4 tiles wide or tall without [safe walls](Safe_wall.md "Safe wall") (or [fences](Fences.md "Fences")).
50:Since the first two are the same as a valid house, they can also meet the requirements for a bedroom, however, other than the Bed itself, no other furniture or lighting is required. 
52:Messages that can be appear when trying to set a spawn point are: 
56:  * If the frame has a gap: _“ Your bedroom is missing a wall!”_
57:    * This is also the message displayed when there is too large an area without any walls.
58:  * If there are only unsafe walls: _“ Natural walls in this bedroom need replacing!”_
61:  * The room is otherwise invalid: _“ This is not a valid room for a bed.”_
63:Unlike with the housing menu, there is no visual indication of bedroom validity. 
73:A valid bedroom is not needed for sleeping. Hovering the cursor over the head of a Bed will produce a Sleeping Icon. Pressing [`⚷ Open / Activate`](Game_controls.md "Game controls") on the head of a Bed causes the player to lie down and sleep (indicated by their eyes closing), which accelerates game time by five times its normal rate (1 hour of in-game time, which would normally take 1 minute of real-life time, takes only 12 seconds while sleeping. A full day and night cycle takes 288 seconds or 4 minutes and 48 seconds). 
523:  * It is advisable to place and activate a Bed in the same [house](House.md "House") the [Nurse](Nurse.md "Nurse") is living in, so immediate healing is available after recalling or respawning. ****__(Desktop, Console and Mobile versions) Be careful not to reset the spawn point by accidentally hitting the Bed upon pressing the Nurse's "heal" button, in case she is standing in front of the Bed.
524:  * There are many naturally-generated structures which can serve as suitable locations for a bedroom, such as [Underground Cabins](Underground_Cabin.md "Underground Cabin") or the houses on [Floating Islands](Floating_Island.md "Floating Island"). Some might require minor modifications, e.g. to fill background wall holes.
525:  * ****__(Desktop, Console and Mobile versions) Upon obtaining the [Shellphone](Shellphone.md "Shellphone"), the player can teleport selectively to the Bed spawn point or the world spawn point at any time. One may thus find it useful to move their home spawn point away from the world spawn, so that they can have two home bases.
540:    * When assigning a [spawn point](Spawn_point "Spawn point") at a bed fails, the reason will be provided.
558:    * Now able to remove spawn point by right-clicking on the bed again.
564:  * [Desktop 1.2.0.2](Desktop_1.2.0.2 "Desktop 1.2.0.2"): If a bed is placed somewhere that would cause the player to not spawn without breaking through blocks, the player will now get a message when trying to set their spawn point letting them know the bed is not in a suitable position.
570:  * [Desktop 1.0.2](Desktop_1.0.2 "Desktop 1.0.2"): Placing a bed far from the spawn no longer causes a player who has set their spawn there to crash on join.
912:[Wall](Wall "Wall")
930:  * [Wall Anchor](Wall_Anchor.md "Wall Anchor")
931:  * [Wall Skeleton](Wall_Skeleton.md "Wall Skeleton")
989:  * [Doors](Doors.md "Doors")
991:  * [Trap Door](Trap_Door.md "Trap Door")**** __(Desktop, Console and Mobile versions)

```


---

## 🤖 Assistant · 2026-08-13T00:39:53.800Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'spawn point|respawn|bed|wall|door' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Spawn.md | head -50",
 "description": "Grep Spawn.md for respawn logic"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:53.828Z

**📎 ToolResult**

```
12:This article is about the player's spawn location. For details about respawn timers of players after dying, see [Death § Respawn](Death#Respawn "Death"). For the spawning mechanics of other entities, see [NPC spawning](NPC_spawning.md "NPC spawning"). 
14:The **world spawn point** is where players appear in a newly created [world](World.md "World") or when joining a [multiplayer](Multiplayer.md "Multiplayer") [server](Server.md "Server"). It is defined during [world generation](World_generation.md "World generation") and is usually within a few tiles of the horizontal center of the world, in the [surface](Surface.md "Surface") layer. It is almost always located in the [Forest](Forest.md "Forest") biome as more hazardous biomes cannot appear at the world's center. 
16:A player's **spawn point** is initially the world spawn point, but can be changed by crafting a [Bed](Bed "Bed"), placing it in a [house](House.md "House") and pressing the [`⚷ Open / Activate`](Game_controls.md "Game controls") button on it. The spawn point is where players respawn after [dying](Death.md "Death"), where a [Magic/Ice Mirror](Magic_Mirrors.md "Magic Mirrors") (or its upgrades) or [Recall Potion](Recall_Potion.md "Recall Potion") will teleport them, and where they appear when entering the world. Once the house the Bed is in is broken or [`⚷ Open / Activate`](Game_controls.md "Game controls") is pressed on the Bed a second time, the player's spawn point reverts back to the world's initial spawn point. 
20:World spawn point
22:Player's spawn point
24:The world spawn point is marked by a green arrow icon on the [minimap](Minimap.md "Minimap"), and the player's spawn point is marked by a bed icon. 
26:## World spawn point
30:During [world generation](World_generation.md "World generation"), the game selects one of the [blocks](Blocks.md "Blocks") it has generated as the world spawn point.[1]
32:The world always has an even number of tiles horizontally – 4200, 6400, or 8400, depending on [world size](World_size.md "World size"). Therefore, the horizontal center of the world is a line between two tiles. When selecting the world spawn point, the game picks a random vertical tile column that is up to five tiles to the left of this central line and up to six tiles to the right of it. The block with the highest altitude in this vertical column is designated as the world spawn point. 
34:However, if the block is below the [surface](Surface.md "Surface") layer or if the tile above it contains any [liquid](Liquid "Liquid"), then it is discarded. In that case, the game again picks a random tile column, though it now increases the possible range by 1 – so now any vertical tile column that is up to _six_ tiles to the left of the horizontally central line and up to _seven_ tiles to the right of it can be randomly selected. Again, the topmost block in the selected vertical column is designated as the world spawn point, and if that block does not meet the conditions either, it is discarded as well. The process is repeated until a valid block is found, with the possible horizontal range (i.e. how far the random selection can possibly stray from the horizontal world center) being increased by 1 tile every time. 
36:As a result, the world spawn point will always be in the surface layer or higher and will never be covered by liquids. It will usually be located within a few tiles from the world's horizontal center, but can potentially end up further away from it. 
42:In [Remix](Remix.md "Remix") worlds, the game selects the world spawn point as normal and then moves it down to the lowest tile of open air, which means on the island of [Ash Blocks](Ash_Block.md "Ash Block") in those worlds. 
44:### Teleporting to the world spawn point
46:When the player enters the world, respawns after [dying](Death.md "Death"), or uses a [Recall Potion](Recall_Potion.md "Recall Potion"), [Magic/Ice Mirror](Magic_Mirrors.md "Magic Mirrors"), [Cell Phone](Cell_Phone.md "Cell Phone"), or [Shellphone (Home)](Shellphone_\(Home\) "Shellphone \(Home\)"), they will be teleported to (or appear at, in the case of entering the world) the world spawn point – so long as they currently have no manually set spawn point at a [Bed](Bed "Bed"). If the player has obstructed the world spawn point (e.g. by placing blocks in the area) or has mined the world spawn point block (leaving the spawn point in midair), the game will attempt to teleport the player to a different location nearby. 
48:The process for determining the teleportation target is described below. The tiles in the world are modeled as a [Cartesian coordinate system](https://en.wikipedia.org/wiki/en:Cartesian_coordinate_system "wikipedia:en:Cartesian coordinate system"), with the y-axis oriented downwards and the origin `(0, 0)` being the top-left tile. In this model, the world spawn point is assumed to be located at coordinates `(x, y)`. 
50:  * First, the game checks the 3×3-tile square above the world spawn point, i.e. from `(x-1, y-3)` to `(x+1, y-1)`. If this area contains any solid blocks or liquids, the teleportation target is considered obstructed.[2]
51:    * If the world spawn point is obstructed, the game checks the 30 tiles directly above it (moving upwards from `(x, y)` to `(x, y-29)`) for an unobstructed location, i.e. a block where there are no solid blocks or liquids in the 3×3-tile square above it.[3]
53:      * Otherwise, the obstructed world spawn point will be used as the teleportation target, placing the player inside of solid blocks.
54:    * If the world spawn point is not obstructed but is in midair, the game will search a 3×50-tile rectangular area below the world spawn point (from `(x-1, y)` to `(x+1, y+49)`, moving downwards, checking each row from left to right) for a solid block. The first block found will be used as the teleportation target.[4]
55:      * If no solid block is found in this area, then the world spawn point will be used as the teleportation target, placing the player in midair.
59:The [Shellphone (Spawn)](Shellphone_\(Spawn\) "Shellphone \(Spawn\)") also teleports the player to the world spawn point. The game follows the same process outlined above, with one exception: If the world spawn point is obstructed and no eligible block is found in the 30 tiles above it, then the game clears the world spawn point. With the other teleportation methods, the player would be placed inside the obstructing blocks at the world spawn point, but when using the Shellphone (Spawn), the obstruction is cleared by the game first.[5]
61:All solid blocks within the 3×3-tile square above the world spawn point will be destroyed and dropped as items. Liquids will be removed as well, but filled [storage items](Storage_items.md "Storage items") and their supporting blocks will remain intact.[6] The player might still end up inside of solid blocks this way. 
65:  * It might be useful to build a shelter over the world spawn point so that the player is provided some amount of safety if they happen to respawn at the world spawn point, like when their manually set spawn point is inadvertently reverted back to the initial world spawn point. Similarly, it should be avoided to dig directly underneath the world spawn point, as players respawning there will inevitably fall down.
66:  * It is possible, albeit extremely rare, for the world spawn point where the player first spawns to be located on a [Floating Island](Floating_Island.md "Floating Island"). In this case, it is highly advisable to use the available blocks to create a staircase to the ground. If there happens to be a [Lucky Horseshoe](Lucky_Horseshoe.md "Lucky Horseshoe") or [Fledgling Wings](Fledgling_Wings.md "Fledgling Wings") in the [Skyware Chest](Skyware_Chest.md "Skyware Chest"), then equipping that item allows jumping down without taking [fall damage](Fall_damage.md "Fall damage"). 
74:    * Added icons for the world spawn point and bed spawn point on the minimap.
75:    * Players can now spawn up to 30 tiles above their spawn point if the location is covered by blocks, rather than destroying those blocks.
80:  * [Desktop 1.2.0.2](Desktop_1.2.0.2 "Desktop 1.2.0.2"): If a [Bed](Bed "Bed") is placed somewhere that would cause the player not to spawn without breaking through blocks, they will now get a message when trying to set the spawn point letting them know the Bed is not in a suitable position.
82:  * [Desktop 1.0.1](Desktop_1.0.1 "Desktop 1.0.1"): Spawning no longer destroys [Chests](Chests.md "Chests") that are placed on ground that is removed due to spawn point clearing.
104:  1. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, method `GenerateWorld()` in `Terraria.WorldGen.cs`. The related world generation pass is called "`Spawn Point`". There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
341:  *[Critter]: May spawn a Worm, Gold Worm, or Maggot when destroyed, as described at the top of this article
1181:  *[Měl bys zůstat v době během noci. Je velmi nebezpečné toulat se v noci.]: You should stay indoors at night. It is very dangerous to be wandering around in the dark.
1434:  *[WoF]: Wall

```


---

## 🤖 Assistant · 2026-08-13T00:39:54.250Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'spawn|bed|wall|one.?way|teleport' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Dungeon_spawn_point.md | head -40",
 "description": "Grep Dungeon_spawn_point.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:54.270Z

**📎 ToolResult**

```
1:# Dungeon spawn point
3:> 原页面: `Dungeon_spawn_point`
5:[Dungeon spawn point](./Dungeon#Dungeon_point)
29:  *[Verify]: Contradicts with [[NPC spawning#Choosing a spot to spawn the NPC]]
54:  *[Critter]: May spawn a Worm, Gold Worm, or Maggot when destroyed, as described at the top of this article

```


---

## 🤖 Assistant · 2026-08-13T00:39:54.660Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'damage|cooldown|period|second|tick|wire' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Dart_Trap.md | head -30",
 "description": "Grep Dart_Trap.md for damage and cooldown"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:54.680Z

**📎 ToolResult**

```
29:Duration| 10 / [20](Expert_Mode.md "Expert Mode") / [25](Master_Mode.md "Master Mode") seconds  
45:A Dart Trap dealing damage and inflicting [Poisoned](Poisoned.md "Poisoned") to a player.
47:The **Dart Trap** is a [trap](Trap "Trap") that can be found naturally placed in [Cavern](Cavern.md "Cavern") layer and [Dungeon](Dungeon.md "Dungeon"). It fires a dart when triggered via [wire](Wire.md "Wire") which does not consume any [ammunition](Ammunition "Ammunition"). It has a cooldown of ****__(Desktop, Console and Mobile versions) 3 1/3 seconds / ****__(Old-gen console and 3DS versions) 3 seconds between firing. The darts deal 40 / [80](Expert_Mode.md "Expert Mode") / [120](Master_Mode.md "Master Mode") damage[1] and inflict [Poisoned](Poisoned.md "Poisoned") for 10 / [20](Expert_Mode.md "Expert Mode") / [25](Master_Mode.md "Master Mode") seconds to players (20 damage and 10 seconds of Poisoned to [NPCs](NPCs.md "NPCs"), [enemies](Enemies.md "Enemies"), and [critters](Critters.md "Critters")).[2]
68:  * Darts from Dart Traps do piercing damage, triggering [invincibility frames](Invincibility_frame.md "Invincibility frame") for 1/6th second (10 ticks[3]) on enemies. If an enemy is hit by more than one dart in that time frame, it will only take damage from one dart. Keeping 8 tiles of space between Dart Traps should guarantee that each dart deals damage. 
70:  * ****__(Desktop, Console and Mobile versions) Due to the cooldown period of Dart Traps being 200 ticks[4] (3.33 seconds, or 3 1/3 seconds), a [1 Second Timer](1_Second_Timer.md "1 Second Timer") can only trigger a shot once every 4 seconds. 
71:    * ****__(Old-gen console and 3DS versions) Due to the 3-second cooldown period, a 1 Second Timer will trigger a shot once every 3 seconds.
72:  * Darts travel at 45 tiles per second (60 mph) and fly for up to 60 seconds, at which point they will break as if they had struck a block. This gives the Dart Trap a maximum range of 2,700 tiles.
75:  * In order to use harvested Dart Traps, players must wire them to a triggering [mechanism](Mechanism "Mechanism") that sends a signal to the trap.
80:  * New characters can easily die to Dart Traps on higher difficulties due to the increased damage and debuff duration.
82:  * A wiring-related item, such as a Dart Trap, [Pressure Plate](Pressure_Plate "Pressure Plate"), or [Wrench](Wrench "Wrench"), can be switched to in the [Hotbar](Hotbar.md "Hotbar") or held in the opened [inventory](Inventory.md "Inventory") to reveal any [wire](Wire.md "Wire") on screen. This is useful for avoiding [traps](Traps.md "Traps") in early game. 
83:    * Alternatively, having the [Mechanical Lens](Mechanical_Lens.md "Mechanical Lens") or [the Grand Design](The_Grand_Design.md "The Grand Design") will reveal wires without switching to a wire-related item, as well as highlight wires in dark places.
86:  * If two Dart Traps are placed 180 tiles apart with a 1 Second Timer, the darts will overlap, allowing for a continuous Dart Trap.
89:  * Seven [1/2 Second Timers](1/2_Second_Timer.md "1/2 Second Timer")**** __(Desktop, Console and Mobile versions) strung together will give a 3.5 second delay between firings, which roughly matches the 3.33 second maximum.
139:  1. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, methods `HitWireSingle()` in `Terraria.Wiring.cs` and `Damage()` in `Terraria.Projectile.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
141:  3. ↑ A tick is a time unit countable by the software. Most of _[Terraria](Terraria.md "Terraria")'s_ updating logic happens every tick. A tick has the length of 1/60th of a second, hence there are 60 ticks in a second and 3600 ticks in a minute.
142:  4. ↑ 1 tick = 1/60th of a second
191:  * [](Wire.md "Wire")[Wire](Wire.md "Wire")
193:  * [](Wire_Cutter.md "Wire Cutter")[Wire Cutter](Wire_Cutter.md "Wire Cutter")
845:  *[DPS]: Damage per second
854:enemies]: Maximum number of enemies Abigail can damage at once
867:  *[0.05 mph]: 0.05 miles per hour (as measured by the Stopwatch item) or 0.04 tiles per second
882:  *[15 mph]: 15 miles per hour (as measured by the Stopwatch item) or 11.25 tiles per second
887:  *[5–9 seconds]: Expert Mode
894:  *[31 mph]: 31 miles per hour (as measured by the Stopwatch item) or 22.5 tiles per second
895:  *[34 mph]: 34 miles per hour (as measured by the Stopwatch item) or 24.93 tiles per second
896:  *[30 mph]: 30 miles per hour (as measured by the Stopwatch item) or 22 tiles per second
900:  *[41 mph]: 41 miles per hour (as measured by the Stopwatch item) or 30 tiles per second
901:  *[21 mph]: 21 miles per hour (as measured by the Stopwatch item) or 15.4 tiles per second
907:  *[1 minute 30 seconds]: Expert Mode
908:  *[1 minute 52.5 seconds]: Master Mode

```


---

## 🤖 Assistant · 2026-08-13T00:39:55.097Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'damage|cooldown|period|second|tick|wire' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Super_Dart_Trap.md | head -30",
 "description": "Grep Super_Dart_Trap.md for damage and cooldown"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:55.121Z

**📎 ToolResult**

```
31:Duration| 10 / [20](Expert_Mode.md "Expert Mode") / [25](Master_Mode.md "Master Mode") seconds  
42:The **Super Dart Trap** is a [trap](Trap "Trap") found inside the [Jungle Temple](Jungle_Temple.md "Jungle Temple") and, rarely, outside the Temple's door. It fires a dart when activated via [Wire](Wire.md "Wire"), which costs no [ammunition](Ammunition "Ammunition"), but has a cooldown period of ****__(Desktop, Console and Mobile versions) 3.33 seconds / ****__(Old-gen console and 3DS versions) 3 seconds between firings. The darts deal 80 / [160](Expert_Mode.md "Expert Mode") / [240](Master_Mode.md "Master Mode") damage[1] and inflict [Poisoned](Poisoned.md "Poisoned") for 15 / [30](Expert_Mode.md "Expert Mode") / [37.5](Master_Mode.md "Master Mode") seconds to players (40 damage and 15 seconds of Poisoned to [NPCs](NPCs.md "NPCs"), [enemies](Enemies.md "Enemies"), and [critters](Critters.md "Critters")).[2]
67:  * As with Dart Traps, darts deal piercing damage and will inflict [invincibility frames](Invincibility_frame.md "Invincibility frame"), making only one of a vertical column of darts hit.
69:  * The projectile's speed and duration are identical to those of the normal Dart Trap projectile's – it travels at exactly 45 tiles per second, and will break after 60 seconds if it does not strike a block first, giving it a maximum range of 2,700 tiles.
115:  1. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, methods `HitWireSingle()` in `Terraria.Wiring.cs` and `Damage()` in `Terraria.Projectile.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
165:  * [](Wire.md "Wire")[Wire](Wire.md "Wire")
167:  * [](Wire_Cutter.md "Wire Cutter")[Wire Cutter](Wire_Cutter.md "Wire Cutter")
823:  *[DPS]: Damage per second
832:enemies]: Maximum number of enemies Abigail can damage at once
845:  *[0.05 mph]: 0.05 miles per hour (as measured by the Stopwatch item) or 0.04 tiles per second
860:  *[15 mph]: 15 miles per hour (as measured by the Stopwatch item) or 11.25 tiles per second
861:  *[16 mph]: 16 miles per hour (as measured by the Stopwatch item) or 11.9390625 tiles per second
865:  *[5–9 seconds]: Master Mode
872:  *[31 mph]: 31 miles per hour (as measured by the Stopwatch item) or 22.5 tiles per second
873:  *[34 mph]: 34 miles per hour (as measured by the Stopwatch item) or 24.93 tiles per second
874:  *[30 mph]: 30 miles per hour (as measured by the Stopwatch item) or 22 tiles per second
878:  *[41 mph]: 41 miles per hour (as measured by the Stopwatch item) or 30.07 tiles per second
879:  *[21 mph]: 21 miles per hour (as measured by the Stopwatch item) or 15.4 tiles per second
885:  *[1 minute 30 seconds]: Expert Mode
886:  *[1 minute 52.5 seconds]: Master Mode
895:  *[17 mph]: 17 miles per hour (as measured by the Stopwatch item) or 12.47 tiles per second
932:  *[53 mph]: 53 miles per hour (as measured by the Stopwatch item) or 38.87 tiles per second
933:  *[88.6 mph]: 88.6 miles per hour (as measured by the Stopwatch item) or 64.97 tiles per second
941:  *[102 mph]: 102 miles per hour (as measured by the Stopwatch item) or 75 tiles per second
948:  *[184 mph]: 184 miles per hour (as measured by the Stopwatch item) or 135 tiles per second
949:  *[72 mph]: 72 miles per hour (as measured by the Stopwatch item) or 52.5 tiles per second
950:  *[82 mph]: 82 miles per hour (as measured by the Stopwatch item) or 60.13 tiles per second
952:  *[51 mph]: 51 miles per hour (as measured by the Stopwatch item) or 37.4 tiles per second
953:  *[66 mph]: 66 miles per hour (as measured by the Stopwatch item) or 48.75 tiles per second
954:  *[77 mph]: 77 miles per hour (as measured by the Stopwatch item) or 56.47 tiles per second

```


---

## 🤖 Assistant · 2026-08-13T00:39:55.499Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'damage|duration|second|tick|on fire|burn' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Flame_Trap.md | head -30",
 "description": "Grep Flame_Trap.md for damage and duration"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:55.525Z

**📎 ToolResult**

```
32:Duration| 20 / [40](Expert_Mode.md "Expert Mode") / [50](Master_Mode.md "Master Mode") seconds  
45:The **Flame Trap** is a [trap](Trap "Trap") found naturally in the [Jungle Temple](Jungle_Temple.md "Jungle Temple"). When activated, it fires a jet of fire, which has a maximum range of 20 ([](Legacy%3A3DS_version "Nintendo 3DS version") 47) tiles, and can pierce an infinite number of targets. It has a cooldown of ****__(Desktop, Console and Mobile versions) 3.33 seconds / ****__(Old-gen console and 3DS versions) 3 seconds between firings. The fire deals 80 / [160](Expert_Mode.md "Expert Mode") / [240](Master_Mode.md "Master Mode") damage to players (40 damage to [NPCs](NPCs.md "NPCs"), [enemies](Enemies.md "Enemies"), and [critters](Critters.md "Critters")),[1] and inflicts the [Hellfire](Hellfire.md "Hellfire") debuff for 20 / [40](Expert_Mode.md "Expert Mode") / [50](Master_Mode.md "Master Mode") seconds on players (20 seconds on NPCs, enemies, and critters).[2]
68:  * The Flame Trap fires 10 times per activation, and fires once every 6 ticks[3]. Therefore it takes a full second (60 ticks) to go through all 10 firings.[4]
115:  1. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.5.6](1.4.5.6.md "1.4.5.6") source code, methods `HitWireSingle()` in `Terraria.Wiring.cs` and `Damage()` in `Terraria.Projectile.cs`.
117:  3. ↑ A tick is a time unit countable by the software. Most of _[Terraria](Terraria.md "Terraria")'s_ updating logic happens every tick. A tick has the length of 1/60th of a second, hence there are 60 ticks in a second and 3600 ticks in a minute.
823:  *[DPS]: Damage per second
832:enemies]: Maximum number of enemies Abigail can damage at once
845:  *[0.05 mph]: 0.05 miles per hour (as measured by the Stopwatch item) or 0.04 tiles per second
860:  *[15 mph]: 15 miles per hour (as measured by the Stopwatch item) or 11.25 tiles per second
865:  *[5–9 seconds]: Master Mode
873:  *[34 mph]: 34 miles per hour (as measured by the Stopwatch item) or 24.93 tiles per second
874:  *[30 mph]: 30 miles per hour (as measured by the Stopwatch item) or 22 tiles per second
878:  *[41 mph]: 41 miles per hour (as measured by the Stopwatch item) or 30 tiles per second
879:  *[21 mph]: 21 miles per hour (as measured by the Stopwatch item) or 15.4 tiles per second
885:  *[1 minute 30 seconds]: Expert Mode
886:  *[1 minute 52.5 seconds]: Master Mode
895:  *[17 mph]: 17 miles per hour (as measured by the Stopwatch item) or 12.47 tiles per second
932:  *[53 mph]: 53 miles per hour (as measured by the Stopwatch item) or 38.87 tiles per second
933:  *[88.6 mph]: 88.6 miles per hour (as measured by the Stopwatch item) or 64.97 tiles per second
941:  *[102 mph]: 102 miles per hour (as measured by the Stopwatch item) or 75 tiles per second
948:  *[184 mph]: 184 miles per hour (as measured by the Stopwatch item) or 135 tiles per second
949:  *[72 mph]: 72 miles per hour (as measured by the Stopwatch item) or 52.5 tiles per second
950:  *[82 mph]: 82 miles per hour (as measured by the Stopwatch item) or 60.13 tiles per second
952:  *[51 mph]: 51 miles per hour (as measured by the Stopwatch item) or 37.4 tiles per second
953:  *[66 mph]: 66 miles per hour (as measured by the Stopwatch item) or 48.4 tiles per second
954:  *[77 mph]: 77 miles per hour (as measured by the Stopwatch item) or 56.25 tiles per second
955:  *[100 mph]: 100 miles per hour (as measured by the Stopwatch item) or 73.125 tiles per second
991:  *[2–6 seconds]: Expert Mode
992:  *[2.5–7.5 seconds]: Master Mode
994:  *[35 mph]: 35 miles per hour (as measured by the Stopwatch item) or 25.31 tiles per second

```


---

## 🤖 Assistant · 2026-08-13T00:39:55.928Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'damage|cooldown|period|second|tick' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Spiked_Ball_Trap.md | head -30",
 "description": "Grep Spiked_Ball_Trap.md for damage"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:55.946Z

**📎 ToolResult**

```
9:  *[DPS]: Damage per second
18:enemies]: Maximum number of enemies Abigail can damage at once
31:  *[0.05 mph]: 0.05 miles per hour (as measured by the Stopwatch item) or 0.04 tiles per second
46:  *[15 mph]: 15 miles per hour (as measured by the Stopwatch item) or 11 tiles per second
47:  *[16 mph]: 16 miles per hour (as measured by the Stopwatch item) or 11.9390625 tiles per second
51:  *[5–9 seconds]: Master Mode
59:  *[34 mph]: 34 miles per hour (as measured by the Stopwatch item) or 24.93 tiles per second
60:  *[30 mph]: 30 miles per hour (as measured by the Stopwatch item) or 22 tiles per second
64:  *[41 mph]: 41 miles per hour (as measured by the Stopwatch item) or 30.07 tiles per second
65:  *[21 mph]: 21 miles per hour (as measured by the Stopwatch item) or 15.4 tiles per second
71:  *[1 minute 30 seconds]: Expert Mode
72:  *[1 minute 52.5 seconds]: Master Mode
81:  *[17 mph]: 17 miles per hour (as measured by the Stopwatch item) or 12.47 tiles per second
118:  *[53 mph]: 53 miles per hour (as measured by the Stopwatch item) or 38.87 tiles per second
119:  *[88.6 mph]: 88.6 miles per hour (as measured by the Stopwatch item) or 64.97 tiles per second
127:  *[102 mph]: 102 miles per hour (as measured by the Stopwatch item) or 75 tiles per second
134:  *[184 mph]: 184 miles per hour (as measured by the Stopwatch item) or 135 tiles per second
135:  *[72 mph]: 72 miles per hour (as measured by the Stopwatch item) or 52.5 tiles per second
136:  *[82 mph]: 82 miles per hour (as measured by the Stopwatch item) or 60.13 tiles per second
138:  *[51 mph]: 51 miles per hour (as measured by the Stopwatch item) or 37.5 tiles per second
139:  *[66 mph]: 66 miles per hour (as measured by the Stopwatch item) or 48.75 tiles per second
140:  *[77 mph]: 77 miles per hour (as measured by the Stopwatch item) or 56.47 tiles per second
141:  *[100 mph]: 100 miles per hour (as measured by the Stopwatch item) or 73.33 tiles per second
177:  *[2–6 seconds]: Expert Mode
178:  *[2.5–7.5 seconds]: Master Mode
181:  *[43 mph]: 43 miles per hour (as measured by the Stopwatch item) or 31.5 tiles per second
188:  *[14–20 seconds]: Expert Mode
189:  *[17.5-25 seconds]: Master Mode
196:  *[ 8 seconds]: Expert Mode
197:  *[10 seconds]: Master Mode

```


---

## 🤖 Assistant · 2026-08-13T00:39:56.459Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE '^[^ ]|blocks|objects|immune' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Explosion-proof_objects.md | head -60",
 "description": "Grep Explosion-proof_objects.md for block list"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:56.527Z

**📎 ToolResult**

```
1:# Explosion-proof objects
3:> 原页面: `Explosion-proof_objects`
5:# Explosion-proof objects
7:[](Desktop_version_history.md "Desktop version") [](Console_version.md "Console version") [](Mobile_version.md "Mobile version")
9:This is the **main** page whose information applies to the **[Desktop](Desktop_version_history.md "Desktop version history")** , **[Console](Console_version.md "Console version")** , and **[Mobile](Mobile_version.md "Mobile version")** versions of _[Terraria](Terraria.md "Terraria")_.  
10:For the differences of this information on [Old-gen console](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [3DS](Legacy%3A3DS_version "Legacy:3DS version"), see **[Legacy:Explosion-proof objects](Legacy%3AExplosion-proof_objects "Legacy:Explosion-proof objects")**.
12:Several [explosives](Explosives_\(class\) "Explosives \(class\)"), like [Dynamite](Dynamite.md "Dynamite") and [Bombs](Bomb.md "Bomb"), break placed objects when they explode. This page lists **explosion-proof objects** , i.e., objects that will remain placed when an explosion occurs.[1]
14:Although these objects are themselves impervious to explosions, they will not _shield_ other objects from explosions. Explosions will destroy any vulnerable objects within their radius, even if explosion-proof blocks are in the way. 
16:## List of explosion-proof objects
18:Always
50:Only for explosives that are not [Power Bomb](Power_Bomb.md "Power Bomb") or [Sticky Power Bomb](Sticky_Power_Bomb.md "Sticky Power Bomb")
59:In [pre-Hardmode](Pre-Hardmode.md "Pre-Hardmode") only
65:Pre-[Golem](Golem.md "Golem") only
72:In [For the Worthy](For_the_Worthy.md "For the Worthy") and [Zenith](Zenith_\(seed\) "Zenith \(seed\)") only
77:## Notes
81:    * [Cursed Dungeon Walls](Dungeon_Wall "Dungeon Wall") are immune to explosions before defeating [Skeletron](Skeletron.md "Skeletron").
82:    * [Forbidden Lihzahrd Brick Walls](Forbidden_Lihzahrd_Brick_Wall "Forbidden Lihzahrd Brick Wall") are immune to explosions before defeating [Golem](Golem.md "Golem").
83:    * [Unbreakable Walls](Unbreakable_Wall.md "Unbreakable Wall") and the blocks in front of them are completely immune to explosions.
85:## History
87:[ Desktop version](Desktop_version_history.md "Desktop version history")
111:## References
117:View or edit this template
119:Game mechanics
121:Combat
132:Environment
134:  * [Ambient objects](Ambient_objects.md "Ambient objects")
149:Interface
164:Items
173:  * Explosion-proof objects
188:Game
205:Multiplayer
211:Player
243:Settings
252:Technical
264:World
276:Categories: 
282:Hidden categories: 
297:This page is issued from [Terraria Wiki](https://terraria.wiki.gg/wiki/?title=Explosion-proof_objects&oldid=1007516 "Last edited on 2026-07-19"). The text is available under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-nc-sa/4.0) unless otherwise noted. Additional terms may apply for the media files. 
310:enemies]: Maximum number of enemies Abigail can damage at once
856:dmg]: Attack damage

```


---

## 🤖 Assistant · 2026-08-13T00:40:03.596Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Some gaps to fill:
1. Dynamite_Fish.md — the page is essentially empty (just a redirect to Angler/Quests). Confirm no stats.
2. Explosion-proof_objects.md — need to read the list section (lines 16-76) to get the block list.
3. Magic_Mirrors.md — need to check if there's Chaos State mention; grep showed no "chaos" hits. Confirm absence. Also cooldown — the 0.75s delay is the use animation. No separate cooldown mentioned.
4. Rod_of_Discord.md — need expert/master variation for Chaos State. Line 61 gives duration 6s and damage 1/7. Check if there's variation by difficulty. Grep showed line 135/140 history. Need to check whether Chaos State differs in expert/master. Let me grep for "expert" context near Chaos State. Also whether Chaos State blocks usage — the page says using while debuff active causes health loss (not blocked). Need the "不" verification.
5. Spiked_Ball_Trap.md — grep found nothing at top; the file seems to be mostly footnote junk at the beginning. Let me read the top of Spiked_Ball_Trap.md.
6. Cell_Phone.md — need use time line 19 (90 Snail) and effect line 38. Good. Maybe check teleport delay mention.
7. Beds.md requirements — need lines 42-61 details; I have most. Maybe read 42-50 for the full requirements list (frame, walls, light? no—line 50 says no other furniture or lighting required). Also "单向" (one-way?) — the user asks about one-way/wall/door requirements. Actually "单向" might mean "single-press toggle" — pressing again removes. Line 36 covers that.
8. Dungeon_spawn_point.md — it's a redirect stub to Dungeon page. Confirm.

Let me read these sections.
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:40:04.333Z · glm-x-preview-260804

```
补齐剩余细节:爆炸物免疫清单、Spiked Ball Trap 页首、Dungeon_spawn_point 与 Dynamite_Fish 的实际内容。
```


---

## 🤖 Assistant · 2026-08-13T00:40:04.342Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Explosion-proof_objects.md",
 "limit": 72,
 "offset": 16
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:04.351Z

**📎 ToolResult**

```
16	## List of explosion-proof objects
17	
18	Always
19	
20	  * [](Blue_Brick "Blue Brick")[Blue Brick](Blue_Brick "Blue Brick")
21	  * [](Green_Brick "Green Brick")[Green Brick](Green_Brick "Green Brick")
22	  * [](Pink_Brick "Pink Brick")[Pink Brick](Pink_Brick "Pink Brick")
23	  * [](Ancient_Blue_Brick "Ancient Blue Brick")[Ancient Blue Brick](Ancient_Blue_Brick "Ancient Blue Brick")
24	  * [](Ancient_Green_Brick "Ancient Green Brick")[Ancient Green Brick](Ancient_Green_Brick "Ancient Green Brick")
25	  * [](Ancient_Pink_Brick "Ancient Pink Brick")[Ancient Pink Brick](Ancient_Pink_Brick "Ancient Pink Brick")
26	  * [](Cobalt_Brick.md "Cobalt Brick")[Cobalt Brick](Cobalt_Brick.md "Cobalt Brick")
27	  * [](Ancient_Cobalt_Brick.md "Ancient Cobalt Brick")[Ancient Cobalt Brick](Ancient_Cobalt_Brick.md "Ancient Cobalt Brick")
28	  * [](Palladium_Column.md "Palladium Column")[Palladium Column](Palladium_Column.md "Palladium Column")
29	  * [](Mythril_Brick.md "Mythril Brick")[Mythril Brick](Mythril_Brick.md "Mythril Brick")
30	  * [](Ancient_Mythril_Brick.md "Ancient Mythril Brick")[Ancient Mythril Brick](Ancient_Mythril_Brick.md "Ancient Mythril Brick")
31	  * [](Bubblegum_Block.md "Bubblegum Block")[Bubblegum Block](Bubblegum_Block.md "Bubblegum Block")
32	  * [](Adamantite_Beam.md "Adamantite Beam")[Adamantite Beam](Adamantite_Beam.md "Adamantite Beam")
33	  * [](Titanstone_Block.md "Titanstone Block")[Titanstone Block](Titanstone_Block.md "Titanstone Block")
34	  * [](Chlorophyte_Ore.md "Chlorophyte Ore")[Chlorophyte Ore](Chlorophyte_Ore.md "Chlorophyte Ore")
35	  * [](Chlorophyte_Brick.md "Chlorophyte Brick")[Chlorophyte Brick](Chlorophyte_Brick.md "Chlorophyte Brick")
36	  * [](Lihzahrd_Brick.md "Lihzahrd Brick")[Lihzahrd Brick](Lihzahrd_Brick.md "Lihzahrd Brick")
37	  * [](Altars.md "Demon Altar")[Demon Altar](Altars.md "Altars")
38	  * [](Altars.md "Crimson Altar")[Crimson Altar](Altars.md "Altars")
39	  * [](Lihzahrd_Altar.md "Lihzahrd Altar")[Lihzahrd Altar](Lihzahrd_Altar.md "Lihzahrd Altar")
40	  * [](Chests.md "Chest")[Chests](Chests.md "Chests")
41	  * [](Barrel.md "Barrel")[Barrel](Barrel.md "Barrel")
42	  * [](Trash_Can.md "Trash Can")[Trash Can](Trash_Can.md "Trash Can")
43	  * [](Dressers.md "Dresser")[Dressers](Dressers.md "Dressers")
44	  * [](Mannequin.md "Mannequin")[Mannequin](Mannequin.md "Mannequin")
45	  * [](Womannequin.md "Womannequin")[Womannequin](Womannequin.md "Womannequin")
46	  * [](Hat_Rack.md "Hat Rack")[Hat Rack](Hat_Rack.md "Hat Rack")
47	  * [](Mystic_Snake_Coil "Mystic Snake Coil")[Mystic Snake Coil](Mystic_Snake_Coil "Mystic Snake Coil")
48	  * [](Doors.md "Lihzahrd Door")[Lihzahrd Door](Doors.md "Doors")(while locked)
49	
50	Only for explosives that are not [Power Bomb](Power_Bomb.md "Power Bomb") or [Sticky Power Bomb](Sticky_Power_Bomb.md "Sticky Power Bomb")
51	
52	  * [](Cobalt_Ore.md "Cobalt Ore")[Cobalt Ore](Cobalt_Ore.md "Cobalt Ore")
53	  * [](Palladium_Ore.md "Palladium Ore")[Palladium Ore](Palladium_Ore.md "Palladium Ore")
54	  * [](Mythril_Ore.md "Mythril Ore")[Mythril Ore](Mythril_Ore.md "Mythril Ore")
55	  * [](Orichalcum_Ore.md "Orichalcum Ore")[Orichalcum Ore](Orichalcum_Ore.md "Orichalcum Ore")
56	  * [](Adamantite_Ore.md "Adamantite Ore")[Adamantite Ore](Adamantite_Ore.md "Adamantite Ore")
57	  * [](Titanium_Ore.md "Titanium Ore")[Titanium Ore](Titanium_Ore.md "Titanium Ore")
58	
59	In [pre-Hardmode](Pre-Hardmode.md "Pre-Hardmode") only
60	
61	  * [](Meteorite.md "Meteorite")[Meteorite](Meteorite.md "Meteorite")
62	  * [](Hellstone.md "Hellstone")[Hellstone](Hellstone.md "Hellstone")
63	  * [](Hellforge.md "Hellforge")[Hellforge](Hellforge.md "Hellforge")(in the Underworld)
64	
65	Pre-[Golem](Golem.md "Golem") only
66	
67	  * [](Spiky_Ball_Trap.md "Spiky Ball Trap")[Spiky Ball Trap](Spiky_Ball_Trap.md "Spiky Ball Trap")
68	  * [](Spear_Trap.md "Spear Trap")[Spear Trap](Spear_Trap.md "Spear Trap")
69	  * [](Super_Dart_Trap.md "Super Dart Trap")[Super Dart Trap](Super_Dart_Trap.md "Super Dart Trap")
70	  * [](Flame_Trap.md "Flame Trap")[Flame Trap](Flame_Trap.md "Flame Trap")
71	
72	In [For the Worthy](For_the_Worthy.md "For the Worthy") and [Zenith](Zenith_\(seed\) "Zenith \(seed\)") only
73	
74	  * [](Spike.md "Spike")[Spike](Spike.md "Spike")
75	  * [](Wooden_Spike.md "Wooden Spike")[Wooden Spike](Wooden_Spike.md "Wooden Spike")
76	
77	## Notes
78	
79	  * In addition, any block directly beneath a [Hellforge](Hellforge.md "Hellforge") (pre-Hardmode only), [Demon/Crimson Altar](Altars.md "Altars"), [Lihzahrd Altar](Lihzahrd_Altar.md "Lihzahrd Altar"), or one of the [storage items](Storage_item "Storage item") listed above will withstand explosions. This also applies to the block below a locked [Lihzahrd Door](Doors.md "Doors"), as well as the one above it.[2]
80	  * All background walls can be only removed by explosives if their edge (i.e., adjacent space with no wall) is within the radius of the explosion.[3]
81	    * [Cursed Dungeon Walls](Dungeon_Wall "Dungeon Wall") are immune to explosions before defeating [Skeletron](Skeletron.md "Skeletron").
82	    * [Forbidden Lihzahrd Brick Walls](Forbidden_Lihzahrd_Brick_Wall "Forbidden Lihzahrd Brick Wall") are immune to explosions before defeating [Golem](Golem.md "Golem").
83	    * [Unbreakable Walls](Unbreakable_Wall.md "Unbreakable Wall") and the blocks in front of them are completely immune to explosions.
84	
85	## History
86	
87	[ Desktop version](Desktop_version_history.md "Desktop version history")

```


---

## 🤖 Assistant · 2026-08-13T00:40:04.623Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "head -60 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Spiked_Ball_Trap.md",
 "description": "Read Spiked_Ball_Trap.md top section"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:04.645Z

**📎 ToolResult**

```
# Spiked Ball Trap

> 原页面: `Spiked_Ball_Trap`

[Spiked Ball Trap](./Traps#Spiky_Ball_Traps)
  *[1 required]: Journey Mode
  *[Qty.]: Quantity
  *[100%]: Master Mode
  *[DPS]: Damage per second
  *[sic]: sīc erat scriptum (Latin: “thus it was written”) – any typographical or other errors in this quote are intentionally reproduced, exactly as they appear in the source.
  *[300]: Master Mode
  *[400]: Expert Mode
  *[160]: Expert Mode
  *[240]: Expert Mode
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
  *[Verify]: Source code ref needed
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
  *[199/10000 (1.99%)]: Expert Mode
  *[membutuhkan 1]: Mode Journey
  *[1,99%]: Expert Mode
  *[1/50 (2%)]: Mode Expert
  *[200 required]: Journey Mode
  *[15 mph]: 15 miles per hour (as measured by the Stopwatch item) or 11 tiles per second
  *[16 mph]: 16 miles per hour (as measured by the Stopwatch item) or 11.9390625 tiles per second
  *[20 required]: Journey Mode
  *[180]: Master Mode
  *[270]: Master Mode
  *[5–9 seconds]: Master Mode
  *[5–9]: Expert Mode
  *[15 required]: Journey Mode
  *[Critter]: May spawn a Worm, Gold Worm, or Maggot when destroyed, as described at the top of this article
  *[Power]: Bait power
  *[5 required]: Journey Mode
  *[cần có {{{research}}}]: Chế độ Journey
  *[31 mph]: 31 miles per hour (as measured by the Stopwatch item)
  *[34 mph]: 34 miles per hour (as measured by the Stopwatch item) or 24.93 tiles per second
  *[30 mph]: 30 miles per hour (as measured by the Stopwatch item) or 22 tiles per second

```


---

## 🤖 Assistant · 2026-08-13T00:40:05.174Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "head -30 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Dungeon_spawn_point.md; echo '---DYNA---'; wc -l ~/Project/GLM/SandboxWorld/terraria-wiki-md/Dynamite_Fish.md",
 "description": "Check Dungeon_spawn_point and Dynamite_Fish length"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:05.208Z

**📎 ToolResult**

```
# Dungeon spawn point

> 原页面: `Dungeon_spawn_point`

[Dungeon spawn point](./Dungeon#Dungeon_point)
  *[1 required]: Journey Mode
  *[Qty.]: Quantity
  *[100%]: Mode Expert
  *[DPS]: Damage per second
  *[sic]: sīc erat scriptum (Latin: “thus it was written”) – any typographical or other errors in this quote are intentionally reproduced, exactly as they appear in the source.
  *[300]: Mode Master
  *[400]: Legendary Mode
  *[160]: Expert Mode
  *[240]: Master Mode
  *[3 required]: Journey Mode
  *[#]: Number of summons, i.e. times that the Desert Tiger Staff was used
  *[Max.  
enemies]: Maximum number of enemies Abigail can damage at once
  *[HM]: Hardmode
  *[**Click/tap here** to reveal this content. _(there may be a slight delay)_]: This content exists externally. Once you click, there may be a small delay while it is downloaded.
  *[**Klik/tap disini** untuk melihat isi konten. _(mungkin akan sedikit delay)_]: Konten ini tersedia secara eksternal. Ketika di klik, mungkin akan ada sedikit delay ketika melihat isi konten.
  *[**Bấm/Chạm vào đây** để hiển thị nội dung này. _(có thể sẽ bị delay một chút)_]: Nội dung này được lấy từ các nguồn bên ngoài. Khi bấm vào, có thể sẽ bị delay một chút trong khi nó tải.
  *[8]: Expert Mode
  *[10]: Master Mode
  *[120]: Expert Mode
  *[150]: Mode Expert
  *[13]: Chế độ Master
  *[195]: Master Mode
  *[Verify]: Contradicts with [[NPC spawning#Choosing a spot to spawn the NPC]]
  *[50 required]: Journey Mode
---DYNA---
     674 ~/Project/GLM/SandboxWorld/terraria-wiki-md/Dynamite_Fish.md

```


---

## 🤖 Assistant · 2026-08-13T00:40:05.792Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'chaos|state' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Magic_Mirrors.md ~/Project/GLM/SandboxWorld/terraria-wiki-md/Cell_Phone.md | grep -v 'mph\\]' | head",
 "description": "Check Chaos State mentions in mirror pages"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:05.822Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-13T00:40:06.489Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'expert|master|1/7|sixth|seventh|block|prevent|cannot be used' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Rod_of_Discord.md | sed -n '1,20p'",
 "description": "Check Rod_of_Discord difficulty variations"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:06.517Z

**📎 ToolResult**

```
49:Expert
51:Master
55:~~[Chaos Elemental](Chaos_Elemental.md "Chaos Elemental")~~ [Chaos Elemental](Chaos_Elemental.md "Chaos Elemental")| 1| 0.2%[0.25%](Expert_Mode.md "Expert Mode")  
61:The **Rod of Discord** is a [Hardmode](Hardmode.md "Hardmode") [tool](Tool "Tool") that has a 1/500 (0.2%) / [1/400 (0.25%)](Expert_Mode.md "Expert Mode") chance of being dropped by [Chaos Elementals](Chaos_Elemental.md "Chaos Elemental"). When used, it instantly teleports the player to the location of the cursor and inflicts the **Chaos State** [debuff](Debuff "Debuff") on the player for 6 seconds. Using the Rod of Discord while this debuff is active causes the player to lose health equal to 1/7 (14.29%) of their maximum [health](Health.md "Health"). 
90:  * The Rod of Discord cannot be used to teleport into the [Jungle Temple](Jungle_Temple.md "Jungle Temple") prior to defeating [Plantera](Plantera.md "Plantera"). 
99:  * If the player only taps the [`⚒ Use / Attack`](Game_controls.md "Game controls") button with the Rod of Discord on the [ Mobile version](Mobile_version.md "Mobile version"), they will be teleported slightly to the right (and above if blocks or furniture are obstructing the path). Using the thumbpad can yield mixed results if the aim mode is set to "Aim & Use" rather than "Aim Only".
100:  * The Rod of Discord cannot be used to teleport past [Unbreakable Walls](Unbreakable_Wall.md "Unbreakable Wall") (generated naturally in [Dual Dungeons](Dual_Dungeons "Dual Dungeons") worlds).[3]
130:    * Now has an increased drop rate of 1/400 (0.25%) in Expert Mode.
135:  * [Desktop 1.3.0.1](Desktop_1.3.0.1 "Desktop 1.3.0.1"): Chaos State damage reduced from one sixth to one seventh of user's total health, and duration decreased from 8 to 6 seconds.
140:    * Chaos State damage reduced from one fifth to one sixth of user's total health, and duration decreased from 10 to 8 seconds.
424:  * [The Dirtiest Block](The_Dirtiest_Block.md "The Dirtiest Block")
536:  * [Wands](Block-placing_wands.md "Block-placing wands")
746:  * [](The_Dirtiest_Block.md "The Dirtiest Block")[The Dirtiest Block](The_Dirtiest_Block.md "The Dirtiest Block")
995:  *[100%]: Master Mode
998:  *[300]: Expert Mode
999:  *[400]: Expert Mode
1000:  *[160]: Expert Mode
1001:  *[240]: Master Mode
1010:  *[8]: Expert Mode
1011:  *[10]: Expert Mode

```


---

## 🤖 Assistant · 2026-08-13T00:40:11.055Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Almost done. Remaining checks:

1. Beds.md — need to see lines 42-50 fully (the requirements list). I have 44, 45, 50. There's probably a line 46-49 that got filtered out (maybe about lighting/door?). Let me read lines 40-62.

2. Sticky_Bomb/Bouncy_Bomb/Dirt_Bomb/Bomb_Fish radius — these say "functions like the Bomb". Damage 100 in infobox. Radius not explicitly stated on those pages except via "functions like the Bomb". Need to check infobox for radius in those pages? The infobox has "Explosion" row. Let me check the infobox rows around line 39 in Sticky_Bomb. Actually there might be a "Radius" value in the infobox. Let me check lines 14-45 of Sticky_Bomb.md.

3. Cell_Phone teleport delay — check if there's a mention of 0.75s delay like Magic Mirror. grep for "0.75\|45 ticks\|delay" in Cell_Phone.md.

4. Dungeon spawn point — actual content lives in Dungeon.md. Let me check if Dungeon.md has a "Dungeon point"/spawn section. The user asked for Dungeon_spawn_point.md specifically; it's a redirect. I should check the Dungeon.md section quickly for usefulness. Let me grep Dungeon.md for spawn point near "Dungeon point".

Let me do these in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:40:11.409Z · glm-x-preview-260804

```
补最后一组:Sticky_Bomb 等的 infobox、Beds 条件全文、Cell Phone 延迟、Dungeon.md 中对应章节。
```


---

## 🤖 Assistant · 2026-08-13T00:40:11.684Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '14,46p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Sticky_Bomb.md",
 "description": "Read Sticky_Bomb infobox rows"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:11.704Z

**📎 ToolResult**

```
  * 

Statistics

Type| [Weapon](Weapon "Weapon")[Crafting material](Crafting_material "Crafting material")  
---|---  
Damage| 100  
[Knockback](Knockback.md "Knockback")| 8 (Very strong)  
Consumable| ✔️  
[Use time](Use_time.md "Use time")| 25 (Fast)  
[Velocity](Velocity.md "Velocity")| 5  
[Tooltip](Tooltips.md "Tooltips")|  _A small explosion that will destroy most tiles  
'Tossing may be difficult.'_  
[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_0 "White \(Rarity level: 0\)")  
[Sell](Value.md "Value")| 1 _SC_  
[Research](Journey_Mode#Research "Journey Mode")| 99 required  
  
Projectile created

  * Sticky Bomb

Sounds

Use|   
---|---  
Explosion|   
  
  * Internal [Item ID](Item_IDs.md "Item IDs"): **235**
  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **37**

The player throwing a Sticky Bomb.

The **Sticky Bomb** is an [explosive](Explosive "Explosive") that functions like the [Bomb](Bomb.md "Bomb"), but sticks onto any [block](Block "Block") on contact. If the block it sticks to is removed by some means, it will fall until it hits another.

```


---

## 🤖 Assistant · 2026-08-13T00:40:12.273Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '14,44p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Bouncy_Bomb.md; echo '---DIRT---'; sed -n '13,44p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Dirt_Bomb.md",
 "description": "Read Bouncy and Dirt Bomb infobox rows"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:12.299Z

**📎 ToolResult**

```
Statistics

Type| [Weapon](Weapon "Weapon")  
---|---  
Damage| 100  
[Knockback](Knockback.md "Knockback")| 8 (Very strong)  
Consumable| ✔️  
[Use time](Use_time.md "Use time")| 25 (Fast)  
[Velocity](Velocity.md "Velocity")| 5  
[Tooltip](Tooltips.md "Tooltips")|  _A small explosion that will destroy most tiles  
Very bouncy_  
[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_0 "White \(Rarity level: 0\)")  
[Sell](Value.md "Value")| 80 _CC_  
[Research](Journey_Mode#Research "Journey Mode")| 99 required  
  
Projectile created

  * Bouncy Bomb

Sounds

Use|   
---|---  
Explosion|   
  
  * Internal [Item ID](Item_IDs.md "Item IDs"): **3115**
  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **516**

The Bouncy Bomb in use.

---DIRT---
  * 

Statistics

Type| [Weapon](Weapon "Weapon")[Crafting material](Crafting_material "Crafting material")  
---|---  
Damage| 100  
[Knockback](Knockback.md "Knockback")| 12 (Insane)  
Consumable| ✔️  
[Use time](Use_time.md "Use time")| 25 (Fast)  
[Velocity](Velocity.md "Velocity")| 5  
[Tooltip](Tooltips.md "Tooltips")|  _A small explosion that will spread dirt_  
[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_1 "Blue \(Rarity level: 1\)")  
[Sell](Value.md "Value")| 1 _SC_  
[Research](Journey_Mode#Research "Journey Mode")| 99 required  
  
Projectile created

  * Dirt Bomb

Sounds

Use|   
---|---  
Explosion|   
  
  * Internal [Item ID](Item_IDs.md "Item IDs"): **4908**
  * Internal [Projectile ID](Projectile_IDs.md "Projectile IDs"): **910**

A Dirt Bomb exploding.

The **Dirt Bomb** is an [explosive](Explosive "Explosive") that functions like the [Bomb](Bomb.md "Bomb"), but its explosion will place [Dirt Blocks](Dirt_Block.md "Dirt Block") in open spaces, instead of destroying blocks. Existing blocks within the explosion radius will remain unaffected.

```


---

## 🤖 Assistant · 2026-08-13T00:40:12.525Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '40,62p' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Beds.md",
 "description": "Read Beds.md bedroom requirements"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:12.543Z

**📎 ToolResult**

```
A valid bedroom for spawning, although not for sleeping due to the block above the foot of the Bed.

The requirements for a valid bedroom are: 

  * A frame of the same area as a [valid house](House#Minimal_house_sizes "House").
  * No area greater than 4 tiles wide or tall without [safe walls](Safe_wall.md "Safe wall") (or [fences](Fences.md "Fences")).
  * A placed Bed.
  * No solid [blocks](Blocks.md "Blocks") above the 3 tiles at the head of the Bed ([platforms](Platforms.md "Platforms") are fine). 
    * For the Bed to be used for sleeping, all 4 tiles must not be solid (platforms are fine).

Since the first two are the same as a valid house, they can also meet the requirements for a bedroom, however, other than the Bed itself, no other furniture or lighting is required. 

Messages that can be appear when trying to set a spawn point are: 

  * If the frame is too small: _“ Your bedroom is too small!”_
  * If the frame is too big: _“ Your bedroom is too big!”_
  * If the frame has a gap: _“ Your bedroom is missing a wall!”_
    * This is also the message displayed when there is too large an area without any walls.
  * If there are only unsafe walls: _“ Natural walls in this bedroom need replacing!”_
  * If there are solid blocks directly above the Bed: _“ Your bed is obstructed.”_
  * If too close to world edge: _“ Your bed is too close to the world's edge.”_
  * The room is otherwise invalid: _“ This is not a valid room for a bed.”_

```


---

## 🤖 Assistant · 2026-08-13T00:40:12.964Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE '0\\.75|45 ticks|delay|Recall' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Cell_Phone.md | head",
 "description": "Check Cell_Phone teleport delay"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:12.984Z

**📎 ToolResult**

```
173:  * [Console 1.0.750.0](Console_1.0.750.0.md "Console 1.0.750.0"): Introduced. ([](Console_version.md "PlayStation 4"))
634:  * Entities introduced in Console 1.0.750.0
655:  *[**Click/tap here** to reveal this content. _(there may be a slight delay)_]: This content exists externally. Once you click, there may be a small delay while it is downloaded.
656:  *[**Klik/tap disini** untuk melihat isi konten. _(mungkin akan sedikit delay)_]: Konten ini tersedia secara eksternal. Ketika di klik, mungkin akan ada sedikit delay ketika melihat isi konten.
657:  *[**Bấm/Chạm vào đây** để hiển thị nội dung này. _(có thể sẽ bị delay một chút)_]: Nội dung này được lấy từ các nguồn bên ngoài. Khi bấm vào, có thể sẽ bị delay một chút trong khi nó tải.

```


---

## 🤖 Assistant · 2026-08-13T00:40:13.503Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'spawn|respawn|bed|guardian|entrance' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Dungeon.md | head -20",
 "description": "Grep Dungeon.md for spawn point section"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:13.525Z

**📎 ToolResult**

```
16:A variant of the Dungeon entrance.
18:The **Dungeon** is a vast underground labyrinth made up of [Dungeon Bricks](Dungeon_Bricks.md "Dungeon Bricks") that is generated on world creation, being located on either the far right or left of the map, and contains unique, mostly skeletal [enemies](Enemies.md "Enemies") whose spawn rates increase the deeper a player travels. It begins at an above-ground entrance structure resembling a castle, and extends down to near-[Underworld](Underworld "Underworld") depths. One Dungeon is generated in each world. Accessing the Dungeon requires first defeating [Skeletron](Skeletron.md "Skeletron") _(seeAccess below)_. The bound [Mechanic](Mechanic.md "Mechanic") is also found in the depths, and is freed when spoken to. The Dungeon can appear in one of three Dungeon Brick colors, and with one or more [Dungeon Brick Wall](Dungeon_Brick_Wall "Dungeon Brick Wall") patterns, which is randomly generated at world creation. Additionally, the Dungeon's entrance itself also can vary from world to world, coming in three different variants, each containing different details. 
22:After [Plantera](Plantera.md "Plantera") is defeated, the Dungeon spawns new, more powerful enemies, which offer access to new items. Not all enemies spawn in all Dungeons: the particular background wall type generated for a particular Dungeon determine which post-Plantera enemies spawn there (_seebelow_). 
24:After a player defeats [Golem](Golem.md "Golem") and Skeletron in a world, a group of 4 [Cultists](Cultists.md "Cultists") will spawn at the entrance of the Dungeon. Killing them will summon the [Lunatic Cultist](Lunatic_Cultist.md "Lunatic Cultist"), and killing the Lunatic Cultist will initiate the [Lunar Events](Lunar_Events.md "Lunar Events"), an end-game [event](Event "Event"). 
28:To gain unrestricted access to the Dungeon, [Skeletron](Skeletron.md "Skeletron") must first be defeated. Skeletron is summoned by speaking to the [Old Man](Old_Man.md "Old Man"), who guards the Dungeon entrance. At [night](Night "Night"), a “Curse” option will be displayed, which will turn the Old Man into Skeletron when chosen. Speaking to the Old Man during the [day](Day "Day") will not allow the player to fight Skeletron. By defeating Skeletron, the [Clothier](Clothier.md "Clothier") [NPC](NPC "NPC") becomes available, and will spawn when a suitable vacant [house](House.md "House") is available. 
30:The Dungeon can be entered but not fully explored before Skeletron is defeated. Traveling to −3 [depth](Depth "Depth") in the Dungeon before it has been defeated will summon [Dungeon Guardians](Dungeon_Guardian.md "Dungeon Guardian") which will generally kill most players with a single hit. The Dungeon Guardians are almost invincible, and killing them will _not_ grant access to the Dungeon — the only item gained from defeating a Dungeon Guardian is the [Bone Key](Bone_Key.md "Bone Key"). 
32:The player can tell if the requirements to spawn Dungeon Guardians are met if the music changes to the Dungeon track, or if they have a [Depth Meter](Depth_Meter.md "Depth Meter") equipped that reads “Level” or "X' Underground". Dungeon entrances are located at varying heights, but are always some distance above zero depths, making their entrance structures and 1–2 screens of depth generally safe from Dungeon Guardians. 
40:The Dungeon contains a dense assortment of unique [furniture](Dungeon_furniture.md "Dungeon furniture") and [mechanisms](Mechanisms.md "Mechanisms") that can be retrieved by the player for later use. Several [Dart Traps](Dart_Trap.md "Dart Trap") are [wired](Wire.md "Wire") to [Pressure Plates](Pressure_Plate "Pressure Plate"), providing an extra hazard to players. Traps like these can also sometimes be found above-ground at the Dungeon's entrance. [Chain Lanterns](Chain_Lantern "Chain Lantern") are wired to [Switches](Switch.md "Switch"), which the player can toggle on and off. 
42:There are many shelves in the Dungeon, on which are [Books](Book.md "Book"), [Lesser Healing Potions](Lesser_Healing_Potion.md "Lesser Healing Potion"), [Lesser Mana Potions](Lesser_Mana_Potion.md "Lesser Mana Potion"), and occasionally [Water Bolts](Water_Bolt.md "Water Bolt"), which appear as a blue book with a yellow stripe in placed form. [Life Crystals](Life_Crystal.md "Life Crystal") cannot spawn in the Dungeon. 
61:  * [](Dungeon_Guardian.md "Dungeon Guardian")[Dungeon Guardian](Dungeon_Guardian.md "Dungeon Guardian")(Only accessible before defeating [Skeletron](Skeletron.md "Skeletron"))
189:The particular post-Plantera enemies that [spawn](NPC_spawning.md "NPC spawning") in the Dungeon area are based off of the [background walls](Background_walls.md "Background walls"), present, which also correspond to the [Faction Flags](Faction_Flag.md "Faction Flag") found naturally placed in the area. A single Dungeon can contain multiple background wall types in different sections, or just one type. Whether a Dungeon contains different types can only be determined by exploring the Dungeon. Each wall type has "usual" enemies to spawn, but there is always a small chance of other Dungeon enemies spawning, and this chance is increased if a [lucky](Luck.md "Luck") player is present. For example, Skeleton Snipers can still rarely spawn in areas with Dungeon Brick Walls, even if no Slab Walls are nearby. 
289:## Entrance Variants
291:The entrance to the Dungeon can come in several different variants, each with different designs and details.[1]
311:  * Internally, one tile at the Dungeon entrance ("Dungeon point") is chosen as the spawning tile of the [Old Man](Old_Man.md "Old Man") and the [Mysterious Tablet](Mysterious_Tablet.md "Mysterious Tablet") (as well as the [Cultists](Cultists.md "Cultists")). This tile is the left of the two blocks on which the Old Man stands during the night.
313:  * A player is considered to be in the Dungeon if they are at or below the depth of −3 feet (1.5 tiles below surface), standing in front of any [unsafe](Unsafe_wall.md "Unsafe wall") [Dungeon Brick Walls](Dungeon_Brick_Walls.md "Dungeon Brick Walls"), and there are at least 250 [Dungeon Bricks](Dungeon_Brick "Dungeon Brick") within the [biome existence requirement](Biome_existence_requirement.md "Biome existence requirement") area.[3] This knowledge can be useful if one wants to lure out a Dungeon Guardian, or to avoid encountering one.
314:  * Most Dungeons, regardless of their visible background walls, have Brick walls behind their foreground blocks. If these blocks are mined out and Plantera has been defeated, enemies associated with Brick walls can potentially spawn.
315:  * The unique loot of the first few chests of the Dungeon (starting from the entrance) can be easily guessed without unlocking. If the first chest is located above the depth of −100 feet, it will be wooden and contain a [Golden Key](Golden_Key.md "Golden Key"), otherwise it will contain a [Muramasa](Muramasa.md "Muramasa"). The following chest will contain a [Cobalt Shield](Cobalt_Shield.md "Cobalt Shield"), and so on. 
316:    * This is because of the way Dungeon chest loot is generated; the unique item of each chest follows a predetermined order. In practice, this becomes impossible to follow because of how the Dungeon splits off into multiple branching paths; however, the entrance is predictable because it is a single linear path. The order is as follows: Muramasa, Cobalt Shield, [Aqua Scepter](Aqua_Scepter.md "Aqua Scepter"), [Blue Moon](Blue_Moon.md "Blue Moon"), [Magic Missile](Magic_Missile.md "Magic Missile"), [Valor](Valor.md "Valor"), Golden Key, [Handgun](Handgun.md "Handgun").[4]
319:  * It is possible, though highly unlikely, for a [Dungeon Guardian](Dungeon_Guardian.md "Dungeon Guardian") to spawn if the player is below −3 depth and _outside_ of the Dungeon. This will only happen if the player is extremely close to the Dungeon, by touching or standing on the outside wall.
320:  * It is possible that one or more [Chests](Chest "Chest") spawn above the surface, allowing to be looted without triggering the spawn of Dungeon Guardians. However, these do not contain the unique, valuable Dungeon-specific items.

```


---

## 🤖 Assistant · 2026-08-13T00:40:30.713Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have everything. Now I need exact line numbers for some quotes I want to use. Let me collect line numbers I know:

Explosives.md: line 43 (main stats), 63 (invincibility frames), 79 (1.4.5.0 damage scaling).
Bomb.md: line 20 (Damage 100 infobox), 68 (main), 72 (Power Bomb hardmode variant), 115 (blast power not affected), 157-158 (history: can destroy dynamite-able; Hellstone after WoF).
Dynamite.md: line 20 (250), 54 (main), 97-102 (notes detail).
Explosive_Bunny.md: 39 (Damage 0 item infobox), 58 (main 350/700/1050), 75 (10 ticks static i-frames), 84 (Bunny Cannon highest base damage).
Sticky_Bomb.md: line 20 (Damage 100), 46 (functions like Bomb). Radius not stated explicitly — same as Bomb by "functions like the Bomb". Note infobox has no radius field.
Bouncy_Bomb.md: 19 (Damage 100), 45 (functions like Bomb, bounces more intensely).
Dirt_Bomb.md: 19 (Damage 100), 44 (functions like Bomb but places dirt), 73 (regular bomb damage if standing on it), 81 (dirt yield up to 57/56).
Bomb_Fish.md: 19 (Damage 100), 44 (functions identically to Sticky Bomb, doesn't slow in water).
Dynamite_Fish.md: empty page — only redirect to Angler/Quests#Dynamite_Fish; no stats present. Line 5.
Scarab_Bomb.md: 19 (Damage 100), 58 (21-tile long, 3-tile wide shaft), 77 (can damage player if too close).
Magic_Mirrors.md: 15 (use time 90 Snail), 37 (Ice Mirror use time 90), 80 (main: delay 0.75s/45 ticks), 82 (Ice Mirror functionally identical), 141 (slowest use times). No Chaos State mention — grep returned nothing.
Rod_of_Discord.md: 20 (use time 20 Very fast), 34 (Duration 6 seconds debuff box), 61 (main: 6s, 1/7 = 14.29%), 90-91 (Jungle Temple restriction), 92 (health loss cannot be reduced, bypasses i-frames), 93 (range 60 tiles horiz/37.5 vert), 94 (target must be 3 high 2 wide; unsuccessful teleports don't inflict debuff), 96 (resets fall damage), 100 (Unbreakable Walls), 135 (history damage/duration). Expert/master: no variation for Chaos State — only drop rate 1/400 in Expert (line 61). Not blocked by Chaos State — using during debuff causes damage, not prevention (line 61).
Cell_Phone.md: 19 (use time 90 Snail), 38 (main: teleport to spawn point), 138 (info shared with teammates within 50 tiles), 157 (slowest use time).
Spawn.md: 16 (spawn point logic), 44-55, 59, 61 (teleport process).
Beds.md: 28 (intro), 36 (set/remove), 38 (bed icon), 42-50 (requirements), 52-61 (messages), 63, 525 (Shellphone).
Dungeon_spawn_point.md: stub redirect line 5 → Dungeon.md. Dungeon.md line 311 (Dungeon point spawn tile for Old Man), 313 (in-Dungeon definition).
Dart_Trap.md: 29 (Duration debuff 10/20/25), 47 (main: cooldown 3 1/3s, damage 40/80/120, Poisoned 10/20/25), 68 (piercing, 1/6s i-frames, 8 tiles spacing), 70 (200 ticks → 1 Second Timer once every 4 seconds), 71 (old-gen 3s → every 3s), 72 (45 tiles/s, 60s, 2700 tiles range).
Super_Dart_Trap.md: 31 (Duration 15/30/37.5), 42 (cooldown 3.33s, damage 80/160/240, Poisoned 15/30/37.5), 69 (same speed/range).
Flame_Trap.md: 32 (Duration 20/40/50), 45 (range 20 tiles (3DS 47), cooldown 3.33s, damage 80/160/240, Hellfire 20/40/50), 68 (fires 10 times per activation, once every 6 ticks, full second).
Spiked_Ball_Trap.md: empty stub, redirect to Traps#Spiky_Ball_Traps. No damage/cooldown in this page. Note the explosion-proof list references "Spiky Ball Trap" (Spiked_Ball_Trap.md line 67 in explosion-proof page). I should note the actual content is in Traps.md. Should I check Traps.md for spiky ball trap damage? The user asked for Spiked_Ball_Trap.md. I could quickly grep Traps.md for the numbers to be helpful, noting they come from Traps.md. Let me do that quickly — it adds value without speculation.

Also the user asked "周期是否随机械装置变化" (whether the period changes with the mechanism) — Dart_Trap.md lines 70-71 and 89 address that: cooldown is fixed 200 ticks; timer choice affects effective firing rate (1 Second Timer → once per 4s; seven 1/2-second timers → 3.5s).

Let me grep Traps.md for spiky ball numbers quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:40:31.095Z · glm-x-preview-260804

```
最后确认 Traps.md 里的 Spiky Ball Trap 数据(因 Spiked_Ball_Trap.md 为空壳重定向)。
```


---

## 🤖 Assistant · 2026-08-13T00:40:31.643Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE 'spiky|damage|cooldown|roll|second|trap' ~/Project/GLM/SandboxWorld/terraria-wiki-md/Traps.md | head -30",
 "description": "Grep Traps.md for Spiky Ball Trap stats"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:31.666Z

**📎 ToolResult**

```
1:# Traps
3:> 原页面: `Traps`
5:# Traps
7:**Traps** are placed items that cause harm to [players](Player "Player") and [enemies](Enemies.md "Enemies"). Most are [mechanisms](Mechanisms.md "Mechanisms") that are naturally generated [underground](Underground.md "Underground") and below. When found initially, they are [wired](Wired "Wired") to triggers, such as [Pressure Plates](Pressure_Plate "Pressure Plate"), intended to harm players who inadvertently activate them. Traps can be collected by players and utilized in [arenas](Arena "Arena"), and are useful for battling events like the [Pumpkin Moon](Pumpkin_Moon.md "Pumpkin Moon") and [Frost Moon](Frost_Moon.md "Frost Moon"). 
9:The [Spike](Spike.md "Spike") and [Wooden Spike](Wooden_Spike.md "Wooden Spike") are exceptions, as they are not mechanisms, but static placed items that simply cause damage on contact. The [Land Mine](Land_Mine.md "Land Mine") is a trap-like item, though never generates naturally, and is instead purchasable during [Hardmode](Hardmode.md "Hardmode"). 
11:All traps, including their triggers, are illuminated by the [Dangersense](Dangersense_Potion.md "Dangersense Potion") buff, allowing the player to avoid and collect them. Their wiring can also be seen if the player holds a [mechanism](Mechanism "Mechanism")-related item in their hand, for instance a pressure plate. The player can also see wires even in darkness if they have a [Mechanical Lens](Mechanical_Lens.md "Mechanical Lens")**** __(Desktop, Console and Mobile versions) or [Grand Design](The_Grand_Design.md "The Grand Design")**** __(Desktop, Console and Mobile versions) in their inventory. 
13:All damaging traps (except the [Land Mine](Land_Mine.md "Land Mine")) can only deal 50% base damage to enemies from the [Old One's Army](Old_One's_Army.md "Old One's Army")**** __(Desktop, Console and Mobile versions) [event](Event "Event").[1]
15:## Reusable Traps
17:Reusable traps generally fire sharp projectiles. They can be activated infinitely with a few seconds delay. 
19:### [](Statue#Enemy_statues "Skeleton Statue")[Statue Traps](Statue#Enemy_statues "Statue")
21:These traps consist of enemy [statues](Statues.md "Statues") wired to a [Red](Red_Pressure_Plate.md "Red Pressure Plate") or [Green Pressure Plate](Green_Pressure_Plate.md "Green Pressure Plate"). Because these kinds of pressure plates can be triggered by enemies, it is possible for enemies spawned from the statue to trigger the trap again, spawning additional enemies until the [statue spawn limit](Statue#Spawn_limits "Statue") is reached. The included statue can be a [Slime Statue](Slime_Statue.md "Slime Statue"), [Bat Statue](Bat_Statue.md "Bat Statue"), [Skeleton Statue](Skeleton_Statue.md "Skeleton Statue") or [Crab Statue](Crab_Statue.md "Crab Statue").[2]
23:On rare occasions, naturally generated statues can overlap with wires from other traps, incidentally forming a statue trap. 
25:### [](Dart_Trap.md "Dart Trap")[Dart Traps](Dart_Trap.md "Dart Trap")
27:Dart Traps fire a [poisoned](Poisoned.md "Poisoned") dart which resembles a [Wooden Arrow](Wooden_Arrow.md "Wooden Arrow") when activated. When found naturally, they are always wired to [Pressure Plates](Pressure_Plate "Pressure Plate") in their line of sight. The Pressure Plate can sometimes be very far away from the Dart Trap. 
29:Dart Traps are the most commonly encountered trap, found throughout the [Underground](Underground.md "Underground") and [Cavern](Cavern.md "Cavern") layers, and are the only variety not found in the Jungle Temple. Many can also be found in the [Dungeon](Dungeon.md "Dungeon"). 
43:### [](Super_Dart_Trap.md "Super Dart Trap")[Super Dart Traps](Super_Dart_Trap.md "Super Dart Trap")
45:Super Dart Traps function like ordinary Dart Traps, but do almost double the damage. They shoot what appears to resemble a [Poison Dart](Poison_Dart.md "Poison Dart"), as opposed to an arrow. They are only found in the [Jungle Temple](Jungle_Temple.md "Jungle Temple"), and are the second most common trap found there. On the [ Desktop version](Desktop_version_history.md "Desktop version history"), [ Console version](Console_version.md "Console version"), and [ Mobile version](Mobile_version.md "Mobile version"), mining them requires a [Picksaw](Picksaw.md "Picksaw") or better pickaxe. 
47:### [](Spiky_Ball_Trap.md "Spiky Ball Trap")[Spiky Ball Traps](Spiky_Ball_Trap.md "Spiky Ball Trap")
49:Spiky Ball Traps drop a single spiky ball that bounces and persists for a long time before despawning. The projectile's prolonged lifetime allows it to do significant damage to anything in its path, which may be useful for terrain often traversed by enemies. Spiky Ball Traps are found in the [Jungle Temple](Jungle_Temple.md "Jungle Temple") only, and are the most common trap there. On the [ Desktop version](Desktop_version_history.md "Desktop version history"), [ Console version](Console_version.md "Console version"), and [ Mobile version](Mobile_version.md "Mobile version"), mining them requires a Picksaw or better pickaxe. 
51:### [](Spear_Trap.md "Spear Trap")[Spear Traps](Spear_Trap.md "Spear Trap")
53:Spear Traps deploy a long spear down from the block, which can reach surprisingly far lengths if not obstructed. They have a shorter activation period than other traps. They are found in the [Jungle Temple](Jungle_Temple.md "Jungle Temple") only, and are the second most rare trap there (only succeeded by [Flame Traps](Flame_Trap.md "Flame Trap")). On the [ Desktop version](Desktop_version_history.md "Desktop version history"), [ Console version](Console_version.md "Console version"), and [ Mobile version](Mobile_version.md "Mobile version"), mining them requires a Picksaw or better pickaxe. 
55:### [](Flame_Trap.md "Flame Trap")[Flame Traps](Flame_Trap.md "Flame Trap")
57:Flame Traps act like horizontal [Geysers](Geyser.md "Geyser"), and spew flames similar to those of the [Flamethrower](Flamethrower.md "Flamethrower"). The flames extend 20 blocks horizontally, and 3 blocks vertically. They are found in the [Jungle Temple](Jungle_Temple.md "Jungle Temple") only, and are the rarest traps there. Often, they do not even spawn in a world at all. On the [ Desktop version](Desktop_version_history.md "Desktop version history"), [ Console version](Console_version.md "Console version"), and [ Mobile version](Mobile_version.md "Mobile version"), mining them requires a Picksaw or better pickaxe. 
61:[Spikes](Spike.md "Spike") and [Wooden Spikes](Wooden_Spike.md "Wooden Spike") are not mechanisms, instead dealing damage on contact with a player. They are found commonly in the [Dungeon](Dungeon.md "Dungeon") and [Jungle Temple](Jungle_Temple.md "Jungle Temple"), respectively. 
65:Structures are traps which consist of ordinary [Blocks](Blocks.md "Blocks") that are arranged in a specific way to kill the [Player](Player "Player"). 
67:### [](Boulder.md "Boulder")[Boulder traps](Boulder.md "Boulder")
71:Boulder traps feature a Pressure Plate wired to a 2×3 arrangement of [Stone Blocks](Stone_Block.md "Stone Block") with [Actuators](Actuator.md "Actuator") above it, with a Boulder resting on top. When the Pressure Plate is triggered, the blocks become inactive and the Boulder drops on the area below. They are dangerous in dark areas as players will not be able to see the Boulder or the pressure plate. They affect all entities, so when used properly can be used to defeat enemies and bosses. 
73:Boulder traps appearing as a part of a Dead Man's Chest setup use blocks with [Actuators](Actuator.md "Actuator") instead of Active Stone Blocks.Verify
80:1/1 (100%) (In [No Traps](No_Traps.md "No Traps"))  
82:1/4 (25%) (In [No Traps](No_Traps.md "No Traps"))

```


---

## 🤖 Assistant · 2026-08-13T00:40:33.306Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Traps.md line 49 describes Spiky Ball Traps qualitatively, no damage numbers. So no damage number for Spiky Ball Trap anywhere in these pages. I'll report that honestly.

Now let me compose the final report with file names, line numbers, and English quotes.
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:41:04.666Z · glm-x-preview-260804

```
所有数据已定位完毕。以下按页面汇报(全部为 grep/read 定位的行号,英文原句为页面原文)。

---

**1. Explosives.md**(爆炸物方块)
- L43:`Triggering Explosives cause a large explosion. The explosion destroys most placed blocks and items ... within a radius of 10 tiles[1], and deals damage within a 16.25×16.25-tile area[2]. The explosion inflicts a knockback of 10 (Extremely strong), deals 1000 / 2000 / 3000 base damage to players and 500 base damage to non-player entities.`
  → 破坏半径 10 tiles;伤害判定区 16.25×16.25 tiles;击退 10;对玩家 1000(专家 2000/大师 3000),对非玩家实体 500。
- L63:`Explosives deal 10 ticks[4] of global invincibility frames ... multiple Explosives triggered at once can only deal damage to the same enemy once.`
- L79:`Desktop 1.4.5.0: Explosives' damage to players is now scaled with difficulty. Previously, they dealt 500 base damage to players.`

**2. Bomb.md**
- L20(infobox):`Damage| 100`
- L68:`The **Bomb** is an explosive that explodes 3 seconds after being thrown. The explosion breaks nearly all blocks, background walls, and furniture within a 4-tile radius, except explosion-proof objects. The explosion also deals 100 damage to all enemies, critters, and players (but not NPCs). Bombs work in liquids.`
  → 引信 3 秒;半径 4 tiles;伤害 100;不伤 NPC;水下可用。
- L72:`The Hardmode variant of the Bomb is the Power Bomb. Power Bombs have a greater radius and can explode early Hardmode ores, unlike the Bomb.`
- L115:`...the Bomb's blast power is not affected by intervening material: for instance, if the Bomb is surrounded by Dungeon Bricks (which are immune to explosions), it will still destroy other destructible blocks and damage entities outside of the Dungeon Bricks but inside the blast radius.`
- L157–158(History):`Now can destroy anything that Dynamite can, including some blocks it couldn't before, like Spikes, Ebonstone and Obsidian.` / `After the Wall of Flesh has been defeated, it can also destroy Hellstone.`

**3. Dynamite.md**
- L20(infobox):`Damage| 250`
- L54:`**Dynamite** is an explosive that explodes 5 seconds after being thrown. The explosion breaks nearly all blocks, background walls, and furniture within a radius of 7 tiles, except explosion-proof objects. The explosion also deals 250 damage to all enemies, critters, and players (but not NPCs) within 7.8 tiles horizontally and vertically of the Dynamite.`
  → 引信 5 秒;破坏半径 7 tiles;伤害 250;伤害判定 7.8 tiles。
- L99–102(精确几何):`Damaging entities: The explosion covers a 15.625×15.625-tile square centered on the Dynamite, i.e. 7.8125 tiles in the four directions.` / `Destroying tiles: The explosion covers a circle with a diameter of 14 tiles centered on the Dynamite, i.e. 7 tiles in all directions.` / `As a result, entities at the edge of the explosion may take damage even though the tiles there remain intact.`

**4. 炸弹变体**
- **Explosive_Bunny.md** — L58:`If an Explosive Bunny critter is killed, it will explode, dealing 350 / 700 / 1050 damage to the player (175 damage to friendly NPCs, critters, and enemies) within a 8×8-tile area centered on it, but not destroying tiles.` → 半径即 8×8-tile 判定区,不毁块;伤害 350(专家 700/大师 1050),对 NPC/生物/敌怪 175。L75:`The explosion of the Explosive Bunny applies 10 ticks of static invincibility frames to enemies.`
- **Sticky_Bomb.md** — L20:`Damage| 100`;L46:`The **Sticky Bomb** is an explosive that functions like the **Bomb**, but sticks onto any block on contact.` 半径未在本页直接给出,由 "functions like the Bomb" 继承 Bomb 的 4-tile radius(见 Bomb.md L68)。本页 infobox 无 Radius 字段。
- **Bouncy_Bomb.md** — L19:`Damage| 100`;L45:`The **Bouncy Bomb** is an explosive that functions like the **Bomb**, but bounces off blocks more intensely.` 半径同上继承,未直接给出。
- **Dirt_Bomb.md** — L19:`Damage| 100`;L44:`The **Dirt Bomb** is an explosive that functions like the **Bomb**, but its explosion will place Dirt Blocks in open spaces, instead of destroying blocks. Existing blocks within the explosion radius will remain unaffected.` L73:`If the player is standing directly on the Dirt Bomb upon exploding, it will deal regular Bomb damage and not create dirt.`
- **Bomb_Fish.md** — L19:`Damage| 100`;L44:`The **Bomb Fish** is an explosive that functions identically to the **Sticky Bomb**, but does not slow down in water.` → 数值等同 Sticky Bomb(即 Bomb)。
- **Dynamite_Fish.md** — **无任何数值**。L5 仅为重定向:`[Dynamite Fish](./Angler/Quests#Dynamite_Fish)`,全文只有页面骨架和导航噪音。
- **Scarab_Bomb.md** — L19:`Damage| 100`;L58:`The **Scarab Bomb** is an explosive that functions like the **Sticky Bomb**, but instead creates a 21-tile long and 3-tile wide shaft. The explosion will always aim away from the player's position, even after being thrown.` L77:`Even though the explosion aims away from the player, it can damage a player if they are too close.`

**5. Magic_Mirrors.md**
- L15:`[Use time](Use_time.md "Use time")| 90 (Snail)`(Magic Mirror)
- L37:`[Use time](Use_time.md "Use time")| 90 (Snail)`(Ice Mirror)
- L80:`Compared to the Recall Potion, the Magic Mirror has unlimited uses, but a delay of 0.75 seconds (45 ticks),[1] which is longer than the Recall Potion's 0.167 seconds (10 ticks) before teleporting.` → 冷却即使用延迟 0.75 秒(45 ticks),无次数限制。
- L82:`The **Ice Mirror** ... is a functionally identical alternative to the Magic Mirror.`
- **Chaos State:本页无任何提及**(grep 'chaos|state' 零命中)。
- L141:`Magic Mirrors have one of the slowest use times in the game, tied with the Magic Conch, Demon Conch, Cell Phone, Shellphone, and Snake Charmer's Flute.`

**6. Rod_of_Discord.md**
- L20:`[Use time](Use_time.md "Use time")| 20 (Very fast)`
- L34(debuff box):`Duration| 6 seconds`
- L61:`When used, it instantly teleports the player to the location of the cursor and inflicts the **Chaos State** debuff on the player for 6 seconds. Using the Rod of Discord while this debuff is active causes the player to lose health equal to 1/7 (14.29%) of their maximum health.`
  → Chaos State 持续 6 秒;期间再用(6 秒内)损失最大生命 1/7;**不被阻止使用,而是扣血惩罚**。
- 专家/大师差异:L61 仅掉率不同(`1/500 (0.2%) / 1/400 (0.25%) in Expert Mode`);**Chaos State 数值本身无难度缩放**。
- 传送规则:L93 `The Rod of Discord's teleport range is limited to 60 tiles horizontally and 37.5 tiles vertically from the player's center`;L94 `The target location must be at least 3 tiles high and 2 tiles wide... Unsuccessful teleports play the same sound, but do not inflict the debuff.`;L90–91 不能进神庙(Plantera 前,unsafe Lihzahrd Brick Wall);L100 `The Rod of Discord cannot be used to teleport past Unbreakable Walls`。
- L92:`The health loss inflicted by Chaos State cannot be reduced in any way or negated through dodge effects. It also bypasses and does not trigger invincibility frames.`

**7. Cell_Phone.md**
- L19:`[Use time](Use_time.md "Use time")| 90 (Snail)`
- L38:`...combines the functions of the PDA and the Magic Mirrors, displaying all information and allowing the player to teleport to their **spawn point**.` → 是,传送回重生点(spawn point,非世界出生点)。
- L138:`The info it provides will be shared with players of the same team in multiplayer that are within 50 tiles.`
- L157:`It has one of the slowest use times in the game, tied with ... Magic Mirrors ...`(即同为 90)。本页未单独给出 0.75 秒延迟数值(该数值在 Magic_Mirrors.md L80)。

**8. Spawn / Beds / Dungeon spawn point**
- **Spawn.md** L16:`The spawn point is where players respawn after dying, where a Magic/Ice Mirror (or its upgrades) or Recall Potion will teleport them, and where they appear when entering the world. Once the house the Bed is in is broken or Open / Activate is pressed on the Bed a second time, the player's spawn point reverts back to the world's initial spawn point.`
- **Spawn.md** L44–61:传送目标判定流程(无床重生点时回 world spawn point):L50 检查出生点上方 3×3 区域是否被实心块/液体阻挡;L51 若阻挡则向上检查 30 tiles;L54 若悬空则向下 3×50 区域找实心块;L59 Shellphone (Spawn) 的例外;L61 会摧毁出生点上方 3×3 的实心块并移除液体。
- **Beds.md** L36:`Pressing Open / Activate on the foot of a Bed, when it is placed in a valid bedroom, sets the player's spawn point to that Bed... When the same is done on a Bed that has already been set as the player's spawn point, the status message "Spawn point removed!" is shown, and the player's spawn point is set back to the world's default.` → **单向开关:再按一次取消并回到世界默认出生点**。
- **Beds.md** L42–50 有效卧室条件:`A frame of the same area as a valid house.` / `No area greater than 4 tiles wide or tall without safe walls (or fences).` / `A placed Bed.` / `No solid blocks above the 3 tiles at the head of the Bed (platforms are fine).` 及 L50:`...other than the Bed itself, no other furniture or lighting is required.` → **需要框架+墙,不需要门、光源或其他家具**。
- **Beds.md** L52–61:各失败提示("Your bedroom is missing a wall!" / "Natural walls in this bedroom need replacing!" / "Your bed is obstructed." 等)。
- **Dungeon_spawn_point.md** — **无实质内容**,L5 仅重定向 `[Dungeon spawn point](./Dungeon#Dungeon_point)`。实际内容在 **Dungeon.md**:L311 `one tile at the Dungeon entrance ("Dungeon point") is chosen as the spawning tile of the Old Man and the Mysterious Tablet (as well as the Cultists)`;L313 `A player is considered to be in the Dungeon if they are at or below the depth of −3 feet (1.5 tiles below surface), standing in front of any unsafe Dungeon Brick Walls, and there are at least 250 Dungeon Bricks within the biome existence requirement area.`(这是 Old Man 刷出点,与床重生点无关。)

**9. 机关**
- **Dart_Trap.md** L47:`It has a cooldown of (Desktop...) 3 1/3 seconds / (Old-gen console and 3DS) 3 seconds between firing. The darts deal 40 / 80 / 120 damage[1] and inflict Poisoned for 10 / 20 / 25 seconds to players (20 damage and 10 seconds of Poisoned to NPCs, enemies, and critters).`
- L70–71(机械装置影响):`Due to the cooldown period of Dart Traps being 200 ticks (3.33 seconds, or 3 1/3 seconds), a 1 Second Timer can only trigger a shot once every 4 seconds.` / `Due to the 3-second cooldown period, a 1 Second Timer will trigger a shot once every 3 seconds.` → 冷却固定,定时器频率受其约束。
- L68:`Darts from Dart Traps do piercing damage, triggering invincibility frames for 1/6th second (10 ticks) on enemies... Keeping 8 tiles of space between Dart Traps should guarantee that each dart deals damage.` L72:`Darts travel at 45 tiles per second (60 mph) and fly for up to 60 seconds... maximum range of 2,700 tiles.`
- **Super_Dart_Trap.md** L42:`cooldown period of ... 3.33 seconds / ... 3 seconds ... The darts deal 80 / 160 / 240 damage and inflict Poisoned for 15 / 30 / 37.5 seconds to players (40 damage and 15 seconds of Poisoned to NPCs...)` → 与普通飞镖机关相比伤害×2、中毒时间 15/30/37.5s,冷却相同。L69:`The projectile's speed and duration are identical to those of the normal Dart Trap projectile's`(45 tiles/s,射程上限 2700 tiles)。
- **Flame_Trap.md** L45:`it fires a jet of fire, which has a maximum range of 20 (47) tiles, and can pierce an infinite number of targets. It has a cooldown of ... 3.33 seconds / ... 3 seconds ... The fire deals 80 / 160 / 240 damage to players (40 damage to NPCs...), and inflicts the Hellfire debuff for 20 / 40 / 50 seconds on players (20 seconds on NPCs, enemies, and critters).`
- L68(持续时间):`The Flame Trap fires 10 times per activation, and fires once every 6 ticks. Therefore it takes a full second (60 ticks) to go through all 10 firings.` → 每次激活喷火 1 秒(10 次、每 6 ticks 一次)。
- **Spiked_Ball_Trap.md** — **无任何数值**。L5 仅重定向 `[Spiked Ball Trap](./Traps#Spiky_Ball_Traps)`。Traps.md L49 也只有定性描述:`Spiky Ball Traps drop a single spiky ball that bounces and persists for a long time before despawning`,未给伤害/冷却数值。

**10. Explosion-proof_objects.md**
- L12 引言:`This page lists **explosion-proof objects**, i.e., objects that will remain placed when an explosion occurs.`
- L14 关键规则:`Although these objects are themselves impervious to explosions, they will not _shield_ other objects from explosions. Explosions will destroy any vulnerable objects within their radius, even if explosion-proof blocks are in the way.`
- 清单(L18–75):
  - **Always**(L20–48):Blue/Green/Pink Brick 及 Ancient 版本、Cobalt Brick(+Ancient)、Palladium Column、Mythril Brick(+Ancient)、Bubblegum Block、Adamantite Beam、Titanstone Block、Chlorophyte Ore/Brick、Lihzahrd Brick、Demon/Crimson Altar、Lihzahrd Altar、Chests、Barrel、Trash Can、Dressers、Mannequin、Womannequin、Hat Rack、Mystic Snake Coil、Lihzahrd Door(锁定时)。
  - **仅对非 Power Bomb/Sticky Power Bomb**(L50–57):Cobalt/Palladium/Mythril/Orichalcum/Adamantite/Titanium Ore。
  - **仅 pre-Hardmode**(L59–63):Meteorite、Hellstone、Hellforge(地狱中)。
  - **仅 Pre-Golem**(L65–70):Spiky Ball Trap、Spear Trap、Super Dart Trap、Flame Trap。
  - **仅 For the Worthy / Zenith 种子**(L72–75):Spike、Wooden Spike。
- L79:`any block directly beneath a Hellforge (pre-Hardmode only), Demon/Crimson Altar, Lihzahrd Altar, or one of the storage items listed above will withstand explosions. This also applies to the block below a locked Lihzahrd Door, as well as the one above it.`
- L80–83(墙):`All background walls can be only removed by explosives if their edge (i.e., adjacent space with no wall) is within the radius of the explosion.` 及 Cursed Dungeon Walls(杀骷髅王前免疫)、Forbidden Lihzahrd Brick Wall(杀 Golem 前免疫)、Unbreakable Wall 及其前方方块完全免疫。

---

**无数据页面汇总**(已明确定位确认,非遗漏):`Dynamite_Fish.md`(纯重定向空页)、`Spiked_Ball_Trap.md`(纯重定向空页)、`Dungeon_spawn_point.md`(纯重定向空页,内容在 Dungeon.md)、`Magic_Mirrors.md`(无 Chaos State 相关内容)、`Sticky_Bomb.md` / `Bouncy_Bomb.md`(半径未直接写出,靠 "functions like the Bomb" 继承)。
```
