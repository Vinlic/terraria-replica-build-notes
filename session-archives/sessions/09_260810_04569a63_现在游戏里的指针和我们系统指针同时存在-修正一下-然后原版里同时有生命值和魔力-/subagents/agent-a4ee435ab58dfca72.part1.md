# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-11T04:52:15.514Z

```
你在 ~/Project/GLM/SandboxWorld/ 工作。权威源码：~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs（1.4.5.6 反编译），名字对照 Terraria.ID/NPCID.cs。

任务：提取以下**小动物（critter）AI 家族**的可照抄移植规格。先 `grep -n "else if (aiStyle == N)" NPC.cs` 定位块起始行再完整读。每个家族输出：状态字段含义、运动学（速度/加速度/重力/碰撞/穿墙标志）、行为触发条件、关键数值、行号。控制 30 次工具调用内。

1. **aiStyle 7 的小动物分支**（46 兔/299 松鼠/300 老鼠/361 青蛙/366 蝎/148 企鹅/616/617/625 龟/610 鼠/593/602 海鸥/608 鷿鷈/687 等——AI_007 巨块里 critter 走的部分）：游走节奏（走多久停多久）、跳跃（撞1格墙跳？随机跳?）、受击反应（是否 AI_007 内处理还是外层）、水中的行为。注意区分城镇 NPC 逻辑与小动物逻辑（如 CountsAsCritter/stoneDefense 分支）。
2. **aiStyle 64 萤火虫族**（355 Firefly/358 LightningBug/654 Lavafly/677 Faeling）：昼夜行为（白天消失?）、飞行漂移模式、光照。
3. **aiStyle 65 蝴蝶族**（356/444/653/661）：飞行模式、昼夜、与 64 的差异。
4. **aiStyle 66 蠕虫族**（357 Worm/448 GoldWorm/606 Maggot/484-487?/374 TruffleWorm 特殊处）：地表蠕动方式（速度/方向翻转）、雨后出现？、374 松露虫的静止/受惊差异。
5. **aiStyle 67 蜗牛族**（359/360/655）：爬行速度、贴地方式、发光蜗牛/岩浆蜗牛差异。
6. **aiStyle 68 鸭族**（363/365/603/609 = Duck 变体）：陆地走/水中游/偶尔短飞 的状态机与触发。
7. **aiStyle 112 仙女族**（583/584/585 粉绿蓝仙灵）：环绕玩家? 漂移模式、光照、昼夜。
8. **aiStyle 114**（595-601，含 599/601 蜻蜓）：这一族都是什么怪（NPCID.cs 查名）？运动模式（蜻蜓悬停突进?）。
9. **aiStyle 115 瓢虫/椿象**（604/605/669）：慢飞、着陆、幸运机制钩子（只提一句）。
10. **aiStyle 116 水黾**（612/613）：水面行走判定（如何贴水面）、移动节奏。
11. **aiStyle 118 海马**（626/627）：水下游动模式。
12. **aiStyle 1 的蚱蜢**（377/446）在 AI_001 里的差异项（ai0 +3 已知，还有别的吗——比如跳跃强度/受击反应）。
13. **aiStyle 16 的鱼类小动物**（55 金鱼/592/607 Pupfish/615 Dolphin/688 Pufferfish）在 AI_016 里的差异项（金鱼离水拍打? 海豚跳跃? 河鲀膨胀?）。

输出：13 节紧凑规格 + 共同陷阱（如各家族白天消失条件 Main.dayTime 处理、Catchable 机制是否在 AI 内、wet 分支等）。
```

---

## 📎 Attachment · skill_listing · 2026-08-11T04:52:15.517Z

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

## 🤖 Assistant · 2026-08-11T04:52:17.081Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by locating the AI blocks in NPC.cs. I'll grep for the aiStyle blocks first.

I have 30 tool calls budget. Let me be efficient with big reads.

Let me first grep for the block starts.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:52:17.148Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"else if (aiStyle == \" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -80",
 "description": "List aiStyle block start lines in NPC.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:52:17.197Z

**📎 ToolResult**

```
24674:		else if (aiStyle == 21)
24726:		else if (aiStyle == 22)
25316:		else if (aiStyle == 23)
25396:		else if (aiStyle == 24)
25621:		else if (aiStyle == 25)
25714:		else if (aiStyle == 26)
25718:		else if (aiStyle == 27)
26141:		else if (aiStyle == 28)
26299:		else if (aiStyle == 29)
26497:		else if (aiStyle == 30)
27116:		else if (aiStyle == 31)
27736:		else if (aiStyle == 32)
28055:		else if (aiStyle == 33)
28360:		else if (aiStyle == 34)
28640:		else if (aiStyle == 35)
28876:		else if (aiStyle == 36)
29111:		else if (aiStyle == 37)
29115:		else if (aiStyle == 38)
29257:		else if (aiStyle == 39)
29784:		else if (aiStyle == 40)
30017:		else if (aiStyle == 41)
30281:		else if (aiStyle == 42)
30312:		else if (aiStyle == 43)
30999:		else if (aiStyle == 44)
31269:		else if (aiStyle == 45)
31273:		else if (aiStyle == 46)
31496:		else if (aiStyle == 47)
31500:		else if (aiStyle == 48)
31742:		else if (aiStyle == 49)
31807:		else if (aiStyle == 50)
31873:		else if (aiStyle == 51)
32238:		else if (aiStyle == 52)
32406:		else if (aiStyle == 53)
32537:		else if (aiStyle == 54)
32828:		else if (aiStyle == 55)
32915:		else if (aiStyle == 56)
32937:		else if (aiStyle == 57)
33246:		else if (aiStyle == 58)
33405:		else if (aiStyle == 59)
33588:		else if (aiStyle == 60)
33902:		else if (aiStyle == 61)
34155:		else if (aiStyle == 62)
34208:		else if (aiStyle == 63)
34256:		else if (aiStyle == 64)
34486:		else if (aiStyle == 65)
34490:		else if (aiStyle == 66)
34586:		else if (aiStyle == 67)
34861:		else if (aiStyle == 68)
35118:		else if (aiStyle == 69)
35122:		else if (aiStyle == 70)
35196:		else if (aiStyle == 71)
35318:		else if (aiStyle == 72)
35340:		else if (aiStyle == 73)
35452:		else if (aiStyle == 74)
35745:		else if (aiStyle == 75)
36322:		else if (aiStyle == 76)
36774:		else if (aiStyle == 77)
37199:		else if (aiStyle == 78)
37712:		else if (aiStyle == 79)
38129:		else if (aiStyle == 80)
38224:		else if (aiStyle == 81)
38668:		else if (aiStyle == 82)
38793:		else if (aiStyle == 83)
38963:		else if (aiStyle == 84)
38967:		else if (aiStyle == 85)
39261:		else if (aiStyle == 86)
39520:		else if (aiStyle == 87)
39876:		else if (aiStyle == 88)
40407:		else if (aiStyle == 89)
40450:		else if (aiStyle == 90)
40686:		else if (aiStyle == 91)
40871:		else if (aiStyle == 92)
40918:		else if (aiStyle == 93)
41029:		else if (aiStyle == 94)
41445:		else if (aiStyle == 95)
41493:		else if (aiStyle == 96)
41536:		else if (aiStyle == 97)
41686:		else if (aiStyle == 98)
41997:		else if (aiStyle == 99)
42064:		else if (aiStyle == 100)

```


---

## 🤖 Assistant · 2026-08-11T04:52:18.051Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"aiStyle == 7\\b\\|aiStyle == 7)\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; grep -n \"private void AI_007\\|private void AI_001\\b\\|private void AI_016\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Locate AI_007/001/016 methods"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:52:18.082Z

**📎 ToolResult**

```
6567:			if (isLikeATownNPC && aiStyle == 7 && velocity.Y == 0f)
6579:			if (isLikeATownNPC && aiStyle == 7)
20769:		if (aiStyle == 7)
53255:			if (Main.npc[j].active && Main.npc[j].aiStyle == 7 && Main.npc[j].townNPC && Main.npc[j].ai[0] == 5f && (Main.npc[j].Bottom + Vector2.UnitY * -2f).ToTileCoordinates() == point2)
53285:				if (Main.npc[i].active && Main.npc[i].aiStyle == 7 && Main.npc[i].townNPC && Main.npc[i].ai[0] == 5f && (Main.npc[i].Bottom + Vector2.UnitY * -2f).ToTileCoordinates() == point)
55782:						if (Main.npc[num119].active && Main.npc[num119].aiStyle == 7 && Main.npc[num119].townNPC && Main.npc[num119].ai[0] == 5f && (Main.npc[num119].Bottom + Vector2.UnitY * -2f).ToTileCoordinates() == point)
82035:				if (aiStyle == 7 && (ai[0] == 3f || ai[0] == 4f || ai[0] == 16f || ai[0] == 17f))
91374:		if (aiStyle == 7 && position.Y > Main.bottomWorld - 640f + (float)height && Main.netMode != 1)
91920:		else if (aiStyle == 7 && ai[0] == 25f)
93841:		if (aiStyle == 7)
94225:		if (aiStyle == 7)
94256:		if ((type == 690 && ai[0] == 0f) || type == 72 || aiStyle == 21 || aiStyle == 67 || type == 376 || type == 579 || type == 541 || (aiStyle == 7 && ai[0] == 25f))
53195:	private void AI_007_FindGoodRestingSpot(int myTileX, int myTileY, out int floorX, out int floorY)
53264:	private void AI_007_TryForcingSitting(int homeFloorX, int homeFloorY)
53335:	private void AI_007_TownEntities_UpdateSavedStates()
53366:	private void AI_007_TownEntities()
55982:	private void AI_007_TownEntities_Shimmer_TeleportToLandingSpot()
56063:	private void AI_007_TownEntities_TeleportToHome(int homeFloorX, int homeFloorY)
56093:	private void AI_007_TownEntities_GetWalkPrediction(int myTileX, int homeFloorX, bool canBreathUnderWater, bool currentlyDrowning, int tileX, int tileY, out bool keepwalking, out bool avoidFalling)
56172:	private void AI_007_AttemptToPlayIdleAnimationsForPets(int petIdleChance)

```


---

## 🤖 Assistant · 2026-08-11T04:52:19.675Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The aiStyle blocks: 7 at 20769, 64 at 34256, 65 at 34486, 66 at 34490, 67 at 34586, 68 at 34861, and I need 112, 114, 115, 116, 118. Let me grep the later range.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:52:20.301Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"else if (aiStyle == \" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | awk -F: '$1>42064 && $1<54000' | head -40",
 "description": "List aiStyle blocks 100+ start lines"
}
```


---

## 🤖 Assistant · 2026-08-11T04:52:21.754Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"= 595,\\|= 596,\\|= 597,\\|= 598,\\|= 599,\\|= 600,\\|= 601,\\|= 583,\\|= 584,\\|= 585,\\|= 357,\\|= 448,\\|= 606,\\|= 374,\\|= 484,\\|= 485,\\|= 486,\\|= 487,\\|= 359,\\|= 360,\\|= 655,\\|= 626,\\|= 627,\\|= 612,\\|= 613,\\|= 615,\\|= 688,\\|= 592,\\|= 607,\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ID/NPCID.cs",
 "description": "Look up NPC names in NPCID.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:52:23.806Z

**📎 ToolResult**

```
42143:		else if (aiStyle == 101)
42224:		else if (aiStyle == 102)
42621:		else if (aiStyle == 103)
42807:		else if (aiStyle == 104)
42811:		else if (aiStyle == 105)
43063:		else if (aiStyle == 106)
43153:		else if (aiStyle == 107)
43157:		else if (aiStyle == 108)
43161:		else if (aiStyle == 109)
43165:		else if (aiStyle == 110)
43169:		else if (aiStyle == 111)
43173:		else if (aiStyle == 112)
43177:		else if (aiStyle == 113)
43181:		else if (aiStyle == 114)
43185:		else if (aiStyle == 115)
43189:		else if (aiStyle == 116)
43193:		else if (aiStyle == 117)
43197:		else if (aiStyle == 118)
43201:		else if (aiStyle == 119)
43205:		else if (aiStyle == 120)
43209:		else if (aiStyle == 121)
43213:		else if (aiStyle == 122)
43217:		else if (aiStyle == 123)
43221:		else if (aiStyle == 124)
43225:		else if (aiStyle == 125)
43229:		else if (aiStyle == 126)
43233:		else if (aiStyle == 127)

```


---

## 👤 User(sidechain) · 2026-08-11T04:52:23.832Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 2
ugrep: warning: ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ID/NPCID.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-11T04:52:25.003Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/Terarria1456/; find ~/Project/GLM/SandboxWorld/Terarria1456 -name \"NPCID.cs\" 2>/dev/null",
 "description": "Find NPCID.cs location"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:52:25.037Z

**📎 ToolResult**

```
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
Terraria.GameContent.Generation.Dungeon
Terraria.GameContent.Generation.Dungeon.Entrances
Terraria.GameContent.Generation.Dungeon.Features
Terraria.GameContent.Generation.Dungeon.Halls
Terraria.GameContent.Generation.Dungeon.LayoutProviders
Terraria.GameContent.Generation.Dungeon.Rooms
Terraria.GameContent.Golf
Terraria.GameContent.ItemDropRules
Terraria.GameContent.Items
Terraria.GameContent.LeashedEntities
Terraria.GameContent.Liquid
Terraria.GameContent.LootSimulation
Terraria.GameContent.LootSimulation.LootSimulatorConditionSetterTypes
Terraria.GameContent.Metadata
Terraria.GameContent.Metadata.MaterialData.Materials.json
Terraria.GameContent.Metadata.MaterialData.Tiles.json
Terraria.GameContent.NetModules
Terraria.GameContent.ObjectInteractions
Terraria.GameContent.Personalities
Terraria.GameContent.Prefixes
Terraria.GameContent.RGB
Terraria.GameContent.Shaders
Terraria.GameContent.Skies
Terraria.GameContent.Skies.CreditsRoll
Terraria.GameContent.Tile_Entities
Terraria.GameContent.UI
Terraria.GameContent.UI.BigProgressBar
Terraria.GameContent.UI.Chat
Terraria.GameContent.UI.Elements
Terraria.GameContent.UI.Minimap
Terraria.GameContent.UI.ResourceSets
Terraria.GameContent.UI.States
Terraria.GameContent.WorldBuilding.Configuration.json
Terraria.GameInput
Terraria.Graphics
Terraria.Graphics.CameraModifiers
Terraria.Graphics.Capture
Terraria.Graphics.Effects
Terraria.Graphics.Light
Terraria.Graphics.Renderers
Terraria.Graphics.Shaders
Terraria.ID
Terraria.Initializers
Terraria.IO
Terraria.IO.Data.ResourcePacksDefaultInfo.tsv
Terraria.Libraries.CsvHelper.CsvHelper.dll
Terraria.Libraries.DotNetZip.Ionic.Zip.CF.dll
Terraria.Libraries.JSON.NET.Newtonsoft.Json.dll
Terraria.Libraries.MP3Sharp.MP3Sharp.dll
Terraria.Libraries.NVorbis.NVorbis.dll
Terraria.Libraries.NVorbis.System.ValueTuple.dll
Terraria.Libraries.RailSDK.OSX.RailSDK.Net.dll
Terraria.Libraries.ReLogic.ReLogic.dll
Terraria.Libraries.Steamworks.NET.OSX.Steamworks.NET.dll
Terraria.Libraries.SteelSeries.SteelSeriesEngineWrapper.dll
Terraria.Localization
Terraria.Localization.Content.de-DE.Game.json
Terraria.Localization.Content.de-DE.Items.json
Terraria.Localization.Content.de-DE.json
Terraria.Localization.Content.de-DE.Legacy.json
Terraria.Localization.Content.de-DE.NPCs.json
Terraria.Localization.Content.de-DE.Projectiles.json
Terraria.Localization.Content.de-DE.Town.json
Terraria.Localization.Content.en-US.Game.json
Terraria.Localization.Content.en-US.Items.json
Terraria.Localization.Content.en-US.json
Terraria.Localization.Content.en-US.Legacy.json
Terraria.Localization.Content.en-US.NPCs.json
Terraria.Localization.Content.en-US.Projectiles.json
Terraria.Localization.Content.en-US.Town.json
Terraria.Localization.Content.es-ES.Game.json
Terraria.Localization.Content.es-ES.Items.json
Terraria.Localization.Content.es-ES.json
Terraria.Localization.Content.es-ES.Legacy.json
Terraria.Localization.Content.es-ES.NPCs.json
Terraria.Localization.Content.es-ES.Projectiles.json
Terraria.Localization.Content.es-ES.Town.json
Terraria.Localization.Content.fr-FR.Game.json
Terraria.Localization.Content.fr-FR.Items.json
Terraria.Localization.Content.fr-FR.json
Terraria.Localization.Content.fr-FR.Legacy.json
Terraria.Localization.Content.fr-FR.NPCs.json
Terraria.Localization.Content.fr-FR.Projectiles.json
Terraria.Localization.Content.fr-FR.Town.json
Terraria.Localization.Content.it-IT.Game.json
Terraria.Localization.Content.it-IT.Items.json
Terraria.Localization.Content.it-IT.json
Terraria.Localization.Content.it-IT.Legacy.json
Terraria.Localization.Content.it-IT.NPCs.json
Terraria.Localization.Content.it-IT.Projectiles.json
Terraria.Localization.Content.it-IT.Town.json
Terraria.Localization.Content.ja-JP.Game.json
Terraria.Localization.Content.ja-JP.Items.json
Terraria.Localization.Content.ja-JP.json
Terraria.Localization.Content.ja-JP.Legacy.json
Terraria.Localization.Content.ja-JP.NPCs.json
Terraria.Localization.Content.ja-JP.Projectiles.json
Terraria.Localization.Content.ja-JP.Town.json
Terraria.Localization.Content.ko-KR.Game.json
Terraria.Localization.Content.ko-KR.Items.json
Terraria.Localization.Content.ko-KR.json
Terraria.Localization.Content.ko-KR.Legacy.json
Terraria.Localization.Content.ko-KR.NPCs.json
Terraria.Localization.Content.ko-KR.Projectiles.json
Terraria.Localization.Content.ko-KR.Town.json
Terraria.Localization.Content.pl-PL.Game.json
Terraria.Localization.Content.pl-PL.Items.json
Terraria.Localization.Content.pl-PL.json
Terraria.Localization.Content.pl-PL.Legacy.json
Terraria.Localization.Content.pl-PL.NPCs.json
Terraria.Localization.Content.pl-PL.Projectiles.json
Terraria.Localization.Content.pl-PL.Town.json
Terraria.Localization.Content.pt-BR.Game.json
Terraria.Localization.Content.pt-BR.Items.json
Terraria.Localization.Content.pt-BR.json
Terraria.Localization.Content.pt-BR.Legacy.json
Terraria.Localization.Content.pt-BR.NPCs.json
Terraria.Localization.Content.pt-BR.Projectiles.json
Terraria.Localization.Content.pt-BR.Town.json
Terraria.Localization.Content.ru-RU.Game.json
Terraria.Localization.Content.ru-RU.Items.json
Terraria.Localization.Content.ru-RU.json
Terraria.Localization.Content.ru-RU.Legacy.json
Terraria.Localization.Content.ru-RU.NPCs.json
Terraria.Localization.Content.ru-RU.Projectiles.json
Terraria.Localization.Content.ru-RU.Town.json
Terraria.Localization.Content.zh-Hans.Game.json
Terraria.Localization.Content.zh-Hans.Items.json
Terraria.Localization.Content.zh-Hans.json
Terraria.Localization.Content.zh-Hans.Legacy.json
Terraria.Localization.Content.zh-Hans.NPCs.json
Terraria.Localization.Content.zh-Hans.Projectiles.json
Terraria.Localization.Content.zh-Hans.Town.json
Terraria.Localization.Content.zh-Hant.Game.json
Terraria.Localization.Content.zh-Hant.Items.json
Terraria.Localization.Content.zh-Hant.json
Terraria.Localization.Content.zh-Hant.Legacy.json
Terraria.Localization.Content.zh-Hant.NPCs.json
Terraria.Localization.Content.zh-Hant.Projectiles.json
Terraria.Localization.Content.zh-Hant.Town.json
Terraria.Map
Terraria.Modules
Terraria.Net
Terraria.Net.Sockets
Terraria.ObjectData
Terraria.Physics
Terraria.Server
Terraria.Social
Terraria.Social.Base
Terraria.Social.Steam
Terraria.Social.WeGame
Terraria.Testing
Terraria.Testing.ChatCommands
Terraria.UI
Terraria.UI.Chat
Terraria.UI.Gamepad
Terraria.Utilities
Terraria.Utilities.FileBrowser
Terraria.Utilities.Terraria.Utilities
Terraria.WorldBuilding
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/NPCID.cs

```


---

## 🤖 Assistant · 2026-08-11T04:52:25.665Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"AI_112\\|AI_113\\|AI_114\\|AI_115\\|AI_116\\|AI_117\\|AI_118\\|AI_119\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -30",
 "description": "Find AI_112-119 method locations"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:52:25.692Z

**📎 ToolResult**

```
43175:			AI_112_FairyCritter();
43179:			AI_113_WindyBalloon();
43183:			AI_114_Dragonflies();
43187:			AI_115_LadyBugs();
43191:			AI_116_WaterStriders();
43195:			AI_117_BloodNautilus();
43199:			AI_118_Seahorses();
43203:			AI_119_Dandelion();
47344:	private void AI_119_Dandelion()
47432:	private void AI_118_Seahorses()
47488:	private void AI_117_BloodNautilus()
47882:	private void AI_116_WaterStriders()
47944:	private void AI_115_LadyBugs()
48080:	private void AI_114_Dragonflies()
48253:	private void AI_113_WindyBalloon()
48283:		NPC nPC = AI_113_WindyBalloon_GetSlaveNPC();
48432:	public NPC AI_113_WindyBalloon_GetSlaveNPC()
48453:	private void AI_112_FairyCritter()
82587:			NPC nPC2 = AI_113_WindyBalloon_GetSlaveNPC();

```


---

## 🤖 Assistant · 2026-08-11T04:52:27.874Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read the key AI methods. First, the critter part of AI_007 (20769 onwards). AI_007 block spans from 20769 to 24674 (aiStyle 21)? That's huge — that's ~3900 lines. The town NPC logic dominates. I need the critter part. Let me grep within AI_007 for critter-related things: CountsAsCritter, stoneDefense, townNPC checks.

Let me grep for "CountsAsCritter" in NPC.cs to understand.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:52:28.200Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"CountsAsCritter\\|stoneDefense\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -40",
 "description": "Find CountsAsCritter and stoneDefense usages"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:52:28.225Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-11T04:52:28.678Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"townNPC\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | awk -F: '$1>=20769 && $1<=24674' | head -60",
 "description": "Find townNPC branches inside AI_007 block"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:52:34.008Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-11T04:52:35.868Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Empty output? Odd. Maybe grep tool is ugrep and fails? The first grep for "else if (aiStyle == " worked. Let me retry with plain grep -F.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:52:36.345Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"CountsAsCritter\" NPC.cs | head -20; echo ---; grep -n \"private bool CountsAsCritter\\|public bool CountsAsCritter\" NPC.cs",
 "description": "Grep CountsAsCritter in NPC.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:52:36.377Z

**📎 ToolResult**

```
---

```


---

## 🤖 Assistant · 2026-08-11T04:52:37.846Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
CountsAsCritter doesn't exist in NPC.cs. Maybe it's in a different file, or in this decompiled version the name differs. Let me search the whole decompiled tree.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:52:38.210Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456 && grep -rn \"CountsAsCritter\" --include=*.cs . | head -20",
 "description": "Search CountsAsCritter across decompiled tree"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:52:38.237Z

**📎 ToolResult**

```
(eval):1: no matches found: --include=*.cs

```


---

## 🤖 Assistant · 2026-08-11T04:52:38.584Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '20769,20830p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read start of aiStyle 7 block"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:52:38.617Z

**📎 ToolResult**

```
		if (aiStyle == 7)
		{
			AI_007_TownEntities();
			return;
		}
		if (aiStyle == 8)
		{
			bool flag4 = RedHatSkeletronAdjustmentsEnabled();
			if (type == 32)
			{
				int num70 = FindFirstNPC(35);
				if (num70 >= 0 && Main.npc[num70].ai[3] == 1f)
				{
					localAI[3] = 1f;
					flag4 = true;
				}
			}
			TargetClosest();
			velocity.X *= 0.93f;
			if (velocity.X > -0.1f && velocity.X < 0.1f)
			{
				velocity.X = 0f;
			}
			if (this.ai[0] == 0f)
			{
				this.ai[0] = 500f;
				if (type == 693)
				{
					localAI[1] = 150f;
				}
			}
			if (type == 172)
			{
				if (alpha < 255)
				{
					alpha++;
				}
				if (justHit)
				{
					alpha = 0;
				}
			}
			if (this.ai[2] != 0f && this.ai[3] != 0f)
			{
				position += netOffset;
				if (type == 172)
				{
					alpha = 255;
				}
				SoundEngine.PlaySound(SoundID.Item8, position);
				for (int num71 = 0; num71 < 50; num71++)
				{
					if (type == 29 || type == 45)
					{
						int num72 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 27, 0f, 0f, 100, default(Color), Main.rand.Next(1, 3));
						Dust dust = Main.dust[num72];
						dust.velocity *= 3f;
						if (Main.dust[num72].scale > 1f)
						{
							Main.dust[num72].noGravity = true;
						}
					}

```


---

## 🤖 Assistant · 2026-08-11T04:52:41.926Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
AI_007 = AI_007_TownEntities() (line 53366). But critters with aiStyle 7 also go there. Critters (rabbit etc.) are aiStyle 7 too. AI_007_TownEntities handles both town NPC and critters. Let me read AI_007_TownEntities. It spans 53366 to ~55982 (AI_007_TownEntities_Shimmer_TeleportToLandingSpot). That's ~2600 lines. I need to find critter-specific parts within.

Let me grep within that range for type numbers like 46 (Bunny), 299 (Squirrel), 366 (Scorpion), 361 (Frog), 148 (Penguin), 616/617 (turtle), 610, 593, 602 (seagull), 608, 687, 657 (Owl?). Actually let me grep for "type == 46" etc within that range.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:52:43.056Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '53366,55982p' NPC.cs > /tmp/ai7.txt && wc -l /tmp/ai7.txt && grep -n \"type == 46\\|type == 299\\|type == 300\\|type == 361\\|type == 366\\|type == 148\\|type == 616\\|type == 617\\|type == 625\\|type == 610\\|type == 593\\|type == 602\\|type == 608\\|type == 687\\|type == 657\" /tmp/ai7.txt",
 "description": "Extract AI_007 body and grep critter type branches"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:52:52.037Z

**📎 ToolResult**

```
    2617 /tmp/ai7.txt
202:		if ((type == 148 || type == 149) && localAI[0] == 0f)
220:		if ((type == 362 || type == 364 || type == 602 || type == 608) && Main.netMode != 1 && (velocity.Y > 4f || velocity.Y < -4f || wet))
491:		bool flag7 = type == 300 || type == 447 || type == 610;
492:		bool flag8 = type == 616 || type == 617 || type == 625;
493:		bool flag9 = type == 361 || type == 445 || type == 687;
922:				else if (type == 299 || type == 539 || type == 538 || (type >= 639 && type <= 645))
939:				if (type == 625)
2610:		if (type == 683 || type == 687)

```


---

## 🤖 Assistant · 2026-08-11T04:52:53.079Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "/tmp/ai7.txt",
 "offset": 180,
 "limit": 330
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:52:53.094Z

**📎 ToolResult**

```
180					}
181					num2 += 0.5f;
182				}
183				if (type == 209)
184				{
185					num3 /= 3f;
186				}
187				if (tipsy)
188				{
189					defense = (int)((double)defense * 1.1);
190					num2 *= 1.1f;
191					num3 *= 0.9f;
192				}
193			}
194			if (type == 142 && Main.netMode != 1 && !Main.xMas)
195			{
196				StrikeNPCNoInteraction(9999, 0f, 0);
197				if (Main.netMode == 2)
198				{
199					NetMessage.SendData(28, -1, -1, null, whoAmI, 9999f);
200				}
201			}
202			if ((type == 148 || type == 149) && localAI[0] == 0f)
203			{
204				localAI[0] = Main.rand.Next(1, 5);
205			}
206			if (type == 124)
207			{
208				int num4 = lazyNPCOwnedProjectileSearchArray[whoAmI];
209				bool flag4 = false;
210				if (Main.projectile.IndexInRange(num4))
211				{
212					Projectile projectile = Main.projectile[num4];
213					if (projectile.active && projectile.type == 582 && projectile.ai[1] == (float)whoAmI)
214					{
215						flag4 = true;
216					}
217				}
218				localAI[0] = flag4.ToInt();
219			}
220			if ((type == 362 || type == 364 || type == 602 || type == 608) && Main.netMode != 1 && (velocity.Y > 4f || velocity.Y < -4f || wet))
221			{
222				Transform(type + 1);
223				return;
224			}
225			AI_007_TownEntities_UpdateSavedStates();
226			dontTakeDamage = false;
227			if (ai[0] == 25f)
228			{
229				dontTakeDamage = true;
230				if (ai[1] == 0f)
231				{
232					velocity.X = 0f;
233				}
234				shimmerWet = false;
235				wet = false;
236				lavaWet = false;
237				honeyWet = false;
238				if (ai[1] == 0f && Main.netMode == 1)
239				{
240					return;
241				}
242				if (ai[1] == 0f && ai[2] < 1f)
243				{
244					AI_007_TownEntities_Shimmer_TeleportToLandingSpot();
245				}
246				if (ai[2] > 0f)
247				{
248					ai[2] -= 1f;
249					if (ai[2] <= 0f)
250					{
251						ai[1] = 1f;
252					}
253					return;
254				}
255				ai[1] += 1f;
256				if (ai[1] >= 30f)
257				{
258					if (!Collision.WetCollision(position, width, height))
259					{
260						shimmerTransparency = MathHelper.Clamp(shimmerTransparency - 1f / 60f, 0f, 1f);
261					}
262					else
263					{
264						ai[1] = 30f;
265					}
266					velocity = new Vector2(0f, -4f * shimmerTransparency);
267				}
268				Rectangle hitbox = base.Hitbox;
269				hitbox.Y += 20;
270				hitbox.Height -= 20;
271				float num5 = Main.rand.NextFloatDirection();
272				Lighting.AddLight(base.Center, Main.hslToRgb((float)Main.timeForVisualEffects / 360f % 1f, 0.6f, 0.65f).ToVector3() * Utils.Remap(ai[1], 30f, 90f, 0f, 0.7f));
273				if (Main.rand.NextFloat() > Utils.Remap(ai[1], 30f, 60f, 1f, 0.5f))
274				{
275					Dust.NewDustPerfect(Main.rand.NextVector2FromRectangle(hitbox) + Main.rand.NextVector2Circular(8f, 0f) + new Vector2(0f, 4f), 309, new Vector2(0f, -2f).RotatedBy(num5 * (MathF.PI * 2f) * 0.11f), 0, default(Color), 1.7f - Math.Abs(num5) * 1.3f);
276				}
277				if (ai[1] > 60f && Main.rand.Next(15) == 0)
278				{
279					for (int i = 0; i < 3; i++)
280					{
281						Vector2 vector = Main.rand.NextVector2FromRectangle(base.Hitbox);
282						ParticleOrchestrator.RequestParticleSpawn(clientOnly: true, ParticleOrchestraType.ShimmerBlock, new ParticleOrchestraSettings
283						{
284							PositionInWorld = vector,
285							MovementVector = DirectionTo(vector).RotatedBy(MathF.PI * 9f / 20f * (float)(Main.rand.Next(2) * 2 - 1)) * Main.rand.NextFloat()
286						});
287					}
288				}
289				TargetClosest();
290				NPCAimedTarget targetData = GetTargetData();
291				if (ai[1] >= 75f && shimmerTransparency <= 0f && Main.netMode != 1)
292				{
293					ai[0] = 0f;
294					ai[1] = 0f;
295					ai[2] = 0f;
296					ai[3] = 0f;
297					Math.Sign(targetData.Center.X - base.Center.X);
298					velocity = new Vector2(0f, -4f);
299					localAI[0] = 0f;
300					localAI[1] = 0f;
301					localAI[2] = 0f;
302					localAI[3] = 0f;
303					netUpdate = true;
304					townNpcVariationIndex = ((townNpcVariationIndex != 1) ? 1 : 0);
305					NetMessage.SendData(56, -1, -1, null, whoAmI);
306					Teleport(position, 12);
307					ParticleOrchestrator.BroadcastParticleSpawn(ParticleOrchestraType.ShimmerTownNPC, new ParticleOrchestraSettings
308					{
309						PositionInWorld = base.Center
310					});
311					if (townNpcVariationIndex == 1)
312					{
313						AchievementsHelper.NotifyProgressionEvent(43);
314					}
315				}
316				return;
317			}
318			if (type >= 0 && type < NPCID.Count && NPCID.Sets.TownCritter[type] && target == 255)
319			{
320				TargetClosest();
321				if (position.X < Main.player[target].position.X)
322				{
323					direction = 1;
324					spriteDirection = direction;
325				}
326				if (position.X > Main.player[target].position.X)
327				{
328					direction = -1;
329					spriteDirection = direction;
330				}
331				if (homeTileX == -1)
332				{
333					UpdateHomeTileState(homeless, (int)((position.X + (float)(width / 2)) / 16f), homeTileY);
334				}
335			}
336			else if (homeTileX == -1 && homeTileY == -1 && velocity.Y == 0f && !shimmering)
337			{
338				UpdateHomeTileState(homeless, (int)base.Center.X / 16, (int)(position.Y + (float)height + 4f) / 16);
339			}
340			bool flag5 = false;
341			int num6 = (int)(position.X + (float)(width / 2)) / 16;
342			int num7 = (int)(position.Y + (float)height + 1f) / 16;
343			AI_007_FindGoodRestingSpot(num6, num7, out var floorX, out var floorY);
344			if (type == 441)
345			{
346				taxCollector = true;
347			}
348			directionY = -1;
349			if (direction == 0)
350			{
351				direction = 1;
352			}
353			bool num8 = ai[0] == 24f;
354			int num9 = 0;
355			if (!num8)
356			{
357				for (int j = 0; j < 255; j++)
358				{
359					if (!Main.player[j].active || Main.player[j].talkNPC != whoAmI)
360					{
361						continue;
362					}
363					flag5 = true;
364					if (ai[0] != 10f && ai[0] != 12f && ai[0] != 14f && ai[0] != 15f)
365					{
366						if (ai[0] != 0f)
367						{
368							netUpdate = true;
369						}
370						ai[0] = 0f;
371						ai[1] = 300f;
372						localAI[3] = 100f;
373						num9 = ((!(Main.player[j].position.X + (float)(Main.player[j].width / 2) < position.X + (float)(width / 2))) ? 1 : (-1));
374					}
375				}
376			}
377			if (ai[3] == 1f)
378			{
379				life = -1;
380				HitEffect();
381				active = false;
382				netUpdate = true;
383				if (type == 37 || type == 54)
384				{
385					SoundEngine.PlaySound(15, (int)position.X, (int)position.Y, 0);
386				}
387				return;
388			}
389			if (type == 37 && Main.netMode != 1)
390			{
391				UpdateHomeTileState(homeless: false, Main.dungeonX, Main.dungeonY);
392				if (downedBoss3)
393				{
394					ai[3] = 1f;
395					netUpdate = true;
396				}
397			}
398			if (type == 368)
399			{
400				homeless = true;
401				if (!Main.dayTime)
402				{
403					if (!shimmering)
404					{
405						UpdateHomeTileState(homeless, (int)(base.Center.X / 16f), (int)(position.Y + (float)height + 2f) / 16);
406					}
407					if (!flag5 && ai[0] == 0f)
408					{
409						ai[0] = 1f;
410						ai[1] = 200f;
411					}
412					flag = false;
413				}
414			}
415			if (type == 369 && homeless && wet)
416			{
417				if (base.Center.X / 16f < 380f || base.Center.X / 16f > (float)(Main.maxTilesX - 380))
418				{
419					UpdateHomeTileState(homeless, Main.spawnTileX, Main.spawnTileY);
420					ai[0] = 1f;
421					ai[1] = 200f;
422				}
423				if (position.X / 16f < 300f)
424				{
425					direction = 1;
426				}
427				else if (position.X / 16f > (float)(Main.maxTilesX - 300))
428				{
429					direction = -1;
430				}
431			}
432			if (NPCID.Sets.CritterThatCanTurnOnPlayers[type])
433			{
434				if (Main.netMode != 1)
435				{
436					int num10 = Player.FindClosest(position, width, height);
437					if (Collision.CanHit(this, Main.player[num10]) && (Main.player[num10].RollOnlyBadLuckExtreme(3000) == 0 || Main.player[num10].IsThisCenx()))
438					{
439						ai[3] = 2f;
440						netUpdate = true;
441					}
442				}
443				if (ai[3] != 0f)
444				{
445					if (lifeMax == 5)
446					{
447						lifeMax = 25;
448						life = 25;
449						defense = defDefense + 6;
450						damage = 20;
451					}
452					aiStyle = 3;
453				}
454			}
455			if (!WorldGen.InWorld(num6, num7) || Main.tile[num6, num7] == null)
456			{
457				return;
458			}
459			if (Main.tile[num6, num7].type == 666 && Main.netMode != 1)
460			{
461				TryAddingRepeatedBuff(120, 180);
462			}
463			if (!homeless && Main.netMode != 1 && townNPC && (flag || (type == 37 && Main.tileDungeon[Main.tile[num6, num7].type])) && !AI_007_TownEntities_IsInAGoodRestingSpot(num6, num7, floorX, floorY))
464			{
465				bool flag6 = true;
466				for (int k = 0; k < 2; k++)
467				{
468					if (!flag6)
469					{
470						break;
471					}
472					Rectangle rectangle = new Rectangle((int)(position.X + (float)(width / 2) - (float)(sWidth / 2) - (float)safeRangeX), (int)(position.Y + (float)(height / 2) - (float)(sHeight / 2) - (float)safeRangeY), sWidth + safeRangeX * 2, sHeight + safeRangeY * 2);
473					if (k == 1)
474					{
475						rectangle = new Rectangle(floorX * 16 + 8 - sWidth / 2 - safeRangeX, floorY * 16 + 8 - sHeight / 2 - safeRangeY, sWidth + safeRangeX * 2, sHeight + safeRangeY * 2);
476					}
477					for (int l = 0; l < 255; l++)
478					{
479						if (Main.player[l].active && new Rectangle((int)Main.player[l].position.X, (int)Main.player[l].position.Y, Main.player[l].width, Main.player[l].height).Intersects(rectangle))
480						{
481							flag6 = false;
482							break;
483						}
484					}
485				}
486				if (flag6)
487				{
488					AI_007_TownEntities_TeleportToHome(floorX, floorY);
489				}
490			}
491			bool flag7 = type == 300 || type == 447 || type == 610;
492			bool flag8 = type == 616 || type == 617 || type == 625;
493			bool flag9 = type == 361 || type == 445 || type == 687;
494			bool flag10 = NPCID.Sets.IsTownSlime[type];
495			_ = NPCID.Sets.IsTownPet[type];
496			bool flag11 = flag8 || flag9;
497			bool flag12 = flag8 || flag9;
498			bool flag13 = flag10;
499			bool flag14 = flag10;
500			float num11 = 200f;
501			if (NPCID.Sets.DangerDetectRange[type] != -1)
502			{
503				num11 = NPCID.Sets.DangerDetectRange[type];
504			}
505			float num12 = num11;
506			if (flag5 && NPCID.Sets.AttackType[type] == 3 && num12 < 250f)
507			{
508				num12 = 250f;
509			}

```


---

## 🤖 Assistant · 2026-08-11T04:52:54.605Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me continue reading the walk/jump state machine. This is a big file. Let me read further, focusing on ai[0] states (0=idle/wander, 1=walk, etc.) and jumps.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:52:54.802Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "/tmp/ai7.txt",
 "limit": 440,
 "offset": 509
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:52:54.809Z

**📎 ToolResult**

```
509			}
510			bool flag15 = false;
511			bool flag16 = false;
512			bool flag17 = false;
513			bool flag18 = false;
514			float num13 = -1f;
515			float num14 = -1f;
516			int num15 = 0;
517			int num16 = -1;
518			int num17 = -1;
519			if (!flag8 && Main.netMode != 1)
520			{
521				for (int m = 0; m < Main.maxNPCs; m++)
522				{
523					if (!Main.npc[m].active || NPCID.Sets.CritterThatCanTurnOnPlayers[Main.npc[m].type] || Main.npc[m].type == 690 || ((Main.npc[m].friendly || Main.npc[m].damage <= 0) && !Main.npc[m].stinky) || m == whoAmI || !(Main.npc[m].Distance(base.Center) < num12) || (type == 453 && NPCID.Sets.Skeletons[Main.npc[m].type]) || (!Main.npc[m].noTileCollide && !Collision.CanHit(base.Center, 0, 0, Main.npc[m].Center, 0, 0)))
524					{
525						continue;
526					}
527					flag15 = true;
528					if (Main.npc[m].Distance(base.Center) >= num11)
529					{
530						continue;
531					}
532					bool flag19 = Main.npc[m].CanBeChasedBy(this);
533					flag16 = true;
534					if (Main.npc[m].stinky)
535					{
536						flag17 = true;
537					}
538					float num18 = Main.npc[m].Center.X - base.Center.X;
539					if (type == 614)
540					{
541						if (num18 < 0f && (num13 == -1f || num18 > num13))
542						{
543							num14 = num18;
544							num17 = m;
545						}
546						if (num18 > 0f && (num14 == -1f || num18 < num14))
547						{
548							num13 = num18;
549							num16 = m;
550						}
551						continue;
552					}
553					if (num18 < 0f && (num13 == -1f || num18 > num13))
554					{
555						num13 = num18;
556						if (flag19)
557						{
558							num16 = m;
559						}
560					}
561					if (num18 > 0f && (num14 == -1f || num18 < num14))
562					{
563						num14 = num18;
564						if (flag19)
565						{
566							num17 = m;
567						}
568					}
569				}
570				if (!flag16 && !flag5)
571				{
572					for (int n = 0; n < 255; n++)
573					{
574						if (Main.player[n].active && !Main.player[n].dead && Main.player[n].stinky && Main.player[n].Distance(base.Center) < num11 && (Main.player[n].stinky || (type != 633 && type != 37 && type != 441 && type != 228 && type != 107 && type != 453)))
575						{
576							flag16 = true;
577							flag17 = true;
578							float num19 = Main.player[n].Center.X - base.Center.X;
579							if (num19 < 0f && (num13 == -1f || num19 > num13))
580							{
581								num13 = num19;
582								num16 = n;
583							}
584							if (num19 > 0f && (num14 == -1f || num19 < num14))
585							{
586								num14 = num19;
587								num17 = n;
588							}
589						}
590					}
591				}
592				if (flag16 && !flag5)
593				{
594					num15 = ((num13 == -1f) ? 1 : ((num14 != -1f) ? (num14 < 0f - num13).ToDirectionInt() : (-1)));
595					float num20 = 0f;
596					if (num13 != -1f)
597					{
598						num20 = 0f - num13;
599					}
600					if (num20 == 0f || (num14 < num20 && num14 > 0f))
601					{
602						num20 = num14;
603					}
604					if (ai[0] == 8f)
605					{
606						if (direction == -num15)
607						{
608							ai[0] = 1f;
609							ai[1] = 300 + Main.rand.Next(300);
610							ai[2] = 0f;
611							localAI[3] = 0f;
612							netUpdate = true;
613						}
614					}
615					else if (ai[0] != 10f && ai[0] != 12f && ai[0] != 13f && ai[0] != 14f && ai[0] != 15f)
616					{
617						if (NPCID.Sets.PrettySafe[type] != -1 && (float)NPCID.Sets.PrettySafe[type] < num20)
618						{
619							flag16 = false;
620						}
621						else if (ai[0] != 1f)
622						{
623							int tileX = (int)((position.X + (float)(width / 2) + (float)(15 * direction)) / 16f);
624							int tileY = (int)((position.Y + (float)height - 16f) / 16f);
625							bool currentlyDrowning = wet && !flag11;
626							AI_007_TownEntities_GetWalkPrediction(num6, floorX, flag11, currentlyDrowning, tileX, tileY, out var _, out var avoidFalling);
627							if (!avoidFalling)
628							{
629								if (ai[0] == 3f || ai[0] == 4f || ai[0] == 16f || ai[0] == 17f)
630								{
631									NPC nPC = Main.npc[(int)ai[2]];
632									if (nPC.active)
633									{
634										nPC.ai[0] = 1f;
635										nPC.ai[1] = 120 + Main.rand.Next(120);
636										nPC.ai[2] = 0f;
637										nPC.localAI[3] = 0f;
638										nPC.direction = -num15;
639										nPC.netUpdate = true;
640									}
641								}
642								ai[0] = 1f;
643								ai[1] = 120 + Main.rand.Next(120);
644								ai[2] = 0f;
645								localAI[3] = 0f;
646								if (flag2)
647								{
648									direction = num15;
649								}
650								else
651								{
652									direction = -num15;
653								}
654								netUpdate = true;
655							}
656						}
657						else if (!flag2 && ai[0] == 1f && direction != -num15)
658						{
659							direction = -num15;
660							netUpdate = true;
661						}
662					}
663				}
664			}
665			if (ai[0] == 0f)
666			{
667				if (flag5 && num9 != 0 && !flag16 && !flag15)
668				{
669					direction = num9;
670				}
671				if (stinky)
672				{
673					ai[0] = 1f;
674				}
675				if (localAI[3] > 0f)
676				{
677					localAI[3] -= 1f;
678				}
679				int num21 = 120;
680				if (type == 638)
681				{
682					num21 = 60;
683				}
684				if ((flag9 || flag10) && wet)
685				{
686					ai[0] = 1f;
687					ai[1] = 200 + Main.rand.Next(500, 700);
688					ai[2] = 0f;
689					localAI[3] = 0f;
690					netUpdate = true;
691				}
692				else if (flag && !flag5 && !NPCID.Sets.TownCritter[type])
693				{
694					if (Main.netMode != 1)
695					{
696						if (num6 == floorX && num7 == floorY)
697						{
698							if (velocity.X != 0f)
699							{
700								netUpdate = true;
701							}
702							if (velocity.X > 0.1f)
703							{
704								velocity.X -= 0.1f;
705							}
706							else if (velocity.X < -0.1f)
707							{
708								velocity.X += 0.1f;
709							}
710							else
711							{
712								velocity.X = 0f;
713								AI_007_TryForcingSitting(floorX, floorY);
714							}
715							if (NPCID.Sets.IsTownPet[type])
716							{
717								AI_007_AttemptToPlayIdleAnimationsForPets(num21 * 4);
718							}
719						}
720						else
721						{
722							if (num6 > floorX)
723							{
724								direction = -1;
725							}
726							else
727							{
728								direction = 1;
729							}
730							ai[0] = 1f;
731							ai[1] = 200 + Main.rand.Next(200);
732							ai[2] = 0f;
733							localAI[3] = 0f;
734							netUpdate = true;
735						}
736					}
737				}
738				else
739				{
740					if (flag7)
741					{
742						velocity.X *= 0.5f;
743					}
744					if (velocity.X > 0.1f)
745					{
746						velocity.X -= 0.1f;
747					}
748					else if (velocity.X < -0.1f)
749					{
750						velocity.X += 0.1f;
751					}
752					else
753					{
754						velocity.X = 0f;
755					}
756					if (Main.netMode != 1)
757					{
758						if (!flag5 && NPCID.Sets.IsTownPet[type] && ai[1] >= 100f && ai[1] <= 150f)
759						{
760							AI_007_AttemptToPlayIdleAnimationsForPets(num21);
761						}
762						if (ai[1] > 0f)
763						{
764							ai[1] -= 1f;
765						}
766						bool flag20 = true;
767						int tileX2 = (int)((position.X + (float)(width / 2) + (float)(15 * direction)) / 16f);
768						int tileY2 = (int)((position.Y + (float)height - 16f) / 16f);
769						bool currentlyDrowning2 = wet && !flag11;
770						AI_007_TownEntities_GetWalkPrediction(num6, floorX, flag11, currentlyDrowning2, tileX2, tileY2, out var _, out var avoidFalling2);
771						if (wet && !flag11)
772						{
773							bool currentlyDrowning3 = Collision.DrownCollision(position, width, height, 1f, includeSlopes: true);
774							if (AI_007_TownEntities_CheckIfWillDrown(currentlyDrowning3))
775							{
776								ai[0] = 1f;
777								ai[1] = 200 + Main.rand.Next(300);
778								ai[2] = 0f;
779								if (NPCID.Sets.TownCritter[type])
780								{
781									ai[1] += Main.rand.Next(200, 400);
782								}
783								localAI[3] = 0f;
784								netUpdate = true;
785							}
786						}
787						if (avoidFalling2)
788						{
789							flag20 = false;
790						}
791						if (ai[1] <= 0f)
792						{
793							if (flag20 && !avoidFalling2)
794							{
795								ai[0] = 1f;
796								ai[1] = 200 + Main.rand.Next(300);
797								ai[2] = 0f;
798								if (NPCID.Sets.TownCritter[type])
799								{
800									ai[1] += Main.rand.Next(200, 400);
801								}
802								localAI[3] = 0f;
803								netUpdate = true;
804							}
805							else
806							{
807								direction *= -1;
808								ai[1] = 60 + Main.rand.Next(120);
809								netUpdate = true;
810							}
811						}
812					}
813				}
814				if (Main.netMode != 1 && (!flag || AI_007_TownEntities_IsInAGoodRestingSpot(num6, num7, floorX, floorY)))
815				{
816					if (num6 < floorX - 25 || num6 > floorX + 25)
817					{
818						if (localAI[3] == 0f)
819						{
820							if (num6 < floorX - 50 && direction == -1)
821							{
822								direction = 1;
823								netUpdate = true;
824							}
825							else if (num6 > floorX + 50 && direction == 1)
826							{
827								direction = -1;
828								netUpdate = true;
829							}
830						}
831					}
832					else if (Main.rand.Next(80) == 0 && localAI[3] == 0f)
833					{
834						localAI[3] = 200f;
835						direction *= -1;
836						netUpdate = true;
837					}
838				}
839			}
840			else if (ai[0] == 1f)
841			{
842				if (Main.netMode != 1 && flag && AI_007_TownEntities_IsInAGoodRestingSpot(num6, num7, floorX, floorY) && !NPCID.Sets.TownCritter[type])
843				{
844					ai[0] = 0f;
845					ai[1] = 200 + Main.rand.Next(200);
846					localAI[3] = 60f;
847					netUpdate = true;
848				}
849				else
850				{
851					bool flag21 = !flag11 && Collision.DrownCollision(position, width, height, 1f, includeSlopes: true);
852					if (!flag21)
853					{
854						if (Main.netMode != 1 && !homeless && !Main.tileDungeon[Main.tile[num6, num7].type] && (num6 < floorX - 35 || num6 > floorX + 35))
855						{
856							if (position.X < (float)(floorX * 16) && direction == -1)
857							{
858								ai[1] -= 5f;
859							}
860							else if (position.X > (float)(floorX * 16) && direction == 1)
861							{
862								ai[1] -= 5f;
863							}
864						}
865						ai[1] -= 1f;
866					}
867					if (ai[1] <= 0f)
868					{
869						ai[0] = 0f;
870						ai[1] = 300 + Main.rand.Next(300);
871						ai[2] = 0f;
872						if (NPCID.Sets.TownCritter[type])
873						{
874							ai[1] -= Main.rand.Next(100);
875						}
876						else
877						{
878							ai[1] += Main.rand.Next(900);
879						}
880						localAI[3] = 60f;
881						netUpdate = true;
882					}
883					if (closeDoor && ((position.X + (float)(width / 2)) / 16f > (float)(doorX + 2) || (position.X + (float)(width / 2)) / 16f < (float)(doorX - 2)))
884					{
885						Tile tileSafely = Framing.GetTileSafely(doorX, doorY);
886						if (tileSafely.type == 11)
887						{
888							if (WorldGen.CloseDoor(doorX, doorY))
889							{
890								closeDoor = false;
891								NetMessage.SendData(19, -1, -1, null, 1, doorX, doorY, direction);
892							}
893							if ((position.X + (float)(width / 2)) / 16f > (float)(doorX + 4) || (position.X + (float)(width / 2)) / 16f < (float)(doorX - 4) || (position.Y + (float)(height / 2)) / 16f > (float)(doorY + 4) || (position.Y + (float)(height / 2)) / 16f < (float)(doorY - 4))
894							{
895								closeDoor = false;
896							}
897						}
898						else if (tileSafely.type == 389)
899						{
900							if (WorldGen.ShiftTallGate(doorX, doorY, closing: true))
901							{
902								closeDoor = false;
903								NetMessage.SendData(19, -1, -1, null, 5, doorX, doorY);
904							}
905							if ((position.X + (float)(width / 2)) / 16f > (float)(doorX + 4) || (position.X + (float)(width / 2)) / 16f < (float)(doorX - 4) || (position.Y + (float)(height / 2)) / 16f > (float)(doorY + 4) || (position.Y + (float)(height / 2)) / 16f < (float)(doorY - 4))
906							{
907								closeDoor = false;
908							}
909						}
910						else
911						{
912							closeDoor = false;
913						}
914					}
915					float num22 = 1f;
916					float num23 = 0.07f;
917					if (type == 614 && flag16)
918					{
919						num22 = 1.5f;
920						num23 = 0.1f;
921					}
922					else if (type == 299 || type == 539 || type == 538 || (type >= 639 && type <= 645))
923					{
924						num22 = 1.5f;
925					}
926					else if (flag8)
927					{
928						if (wet)
929						{
930							num23 = 1f;
931							num22 = 2f;
932						}
933						else
934						{
935							num23 = 0.07f;
936							num22 = 0.5f;
937						}
938					}
939					if (type == 625)
940					{
941						if (wet)
942						{
943							num23 = 1f;
944							num22 = 2.5f;
945						}
946						else
947						{
948							num23 = 0.07f;

```


---

## 🤖 Assistant · 2026-08-11T04:52:55.960Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Continue reading — need jump logic. Let me read further lines ~950-1400.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:52:56.083Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "/tmp/ai7.txt",
 "limit": 420,
 "offset": 949
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:52:56.090Z

**📎 ToolResult**

```
949							num22 = 0.2f;
950						}
951					}
952					if (flag7)
953					{
954						num22 = 2f;
955						num23 = 1f;
956					}
957					if (friendly && (flag16 || flag21))
958					{
959						num22 = 1.5f;
960						float num24 = 1f - (float)life / (float)lifeMax;
961						num22 += num24 * 0.9f;
962						num23 = 0.1f;
963					}
964					if (flag13 && wet)
965					{
966						num22 = 2f;
967						num23 = 0.2f;
968					}
969					if (flag9 && wet)
970					{
971						if (Math.Abs(velocity.X) < 0.05f && Math.Abs(velocity.Y) < 0.05f)
972						{
973							velocity.X += num22 * 10f * (float)direction;
974						}
975						else
976						{
977							velocity.X *= 0.9f;
978						}
979					}
980					else if (velocity.X < 0f - num22 || velocity.X > num22)
981					{
982						if (velocity.Y == 0f)
983						{
984							velocity *= 0.8f;
985						}
986					}
987					else if (velocity.X < num22 && direction == 1)
988					{
989						velocity.X += num23;
990						if (velocity.X > num22)
991						{
992							velocity.X = num22;
993						}
994					}
995					else if (velocity.X > 0f - num22 && direction == -1)
996					{
997						velocity.X -= num23;
998						if (velocity.X > num22)
999						{
1000							velocity.X = num22;
1001						}
1002					}
1003					bool flag22 = true;
1004					if ((float)(homeTileY * 16 - 32) > position.Y)
1005					{
1006						flag22 = false;
1007					}
1008					if (!flag22 && velocity.Y == 0f)
1009					{
1010						Collision.StepDown(ref position, ref velocity, width, height, ref stepSpeed, ref gfxOffY);
1011					}
1012					if (velocity.Y >= 0f)
1013					{
1014						float num25 = gfxOffY;
1015						Vector2 vector2 = position;
1016						Vector2 vector3 = velocity;
1017						Collision.StepUp(ref position, ref velocity, width, height, ref stepSpeed, ref gfxOffY, 1, flag22, 1);
1018						if (num25 == gfxOffY && vector2 == position && vector3 == velocity && ai[1] < 100f && ai[1] % 10f == 0f && Main.netMode != 1)
1019						{
1020							ai[0] = 1f;
1021							ai[1] = 200 + Main.rand.Next(300);
1022							ai[2] = 0f;
1023							if (NPCID.Sets.TownCritter[type])
1024							{
1025								ai[1] += Main.rand.Next(200, 400);
1026							}
1027							direction *= -1;
1028							velocity.X *= -1f;
1029							netUpdate = true;
1030							return;
1031						}
1032					}
1033					if (velocity.Y == 0f)
1034					{
1035						int num26 = (int)((position.X + (float)(width / 2) + (float)(15 * direction)) / 16f);
1036						int num27 = (int)((position.Y + (float)height - 16f) / 16f);
1037						int num28 = 180;
1038						AI_007_TownEntities_GetWalkPrediction(num6, floorX, flag11, flag21, num26, num27, out var keepwalking3, out var avoidFalling3);
1039						bool flag23 = false;
1040						bool flag24 = false;
1041						if (wet && !flag11 && isLikeATownNPC && (flag24 = AI_007_TownEntities_CheckIfWillDrown(flag21)) && localAI[3] <= 0f)
1042						{
1043							avoidFalling3 = true;
1044							localAI[3] = num28;
1045							int num29 = 0;
1046							for (int num30 = 0; num30 <= 10 && Framing.GetTileSafely(num26 - direction, num27 - num30).liquid != 0; num30++)
1047							{
1048								num29++;
1049							}
1050							float num31 = 0.3f;
1051							float num32 = (float)Math.Sqrt((float)(num29 * 16 + 16) * 2f * num31);
1052							if (num32 > 26f)
1053							{
1054								num32 = 26f;
1055							}
1056							velocity.Y = 0f - num32;
1057							localAI[3] = position.X;
1058							flag23 = true;
1059						}
1060						if (avoidFalling3 && !flag23)
1061						{
1062							int num33 = (int)((position.X + (float)(width / 2)) / 16f);
1063							int num34 = 0;
1064							for (int num35 = -1; num35 <= 1; num35++)
1065							{
1066								Tile tileSafely2 = Framing.GetTileSafely(num33 + num35, num27 + 1);
1067								if (tileSafely2.nactive() && Main.tileSolid[tileSafely2.type])
1068								{
1069									num34++;
1070								}
1071							}
1072							if (num34 <= 2)
1073							{
1074								if (velocity.X != 0f)
1075								{
1076									netUpdate = true;
1077								}
1078								keepwalking3 = (avoidFalling3 = false);
1079								ai[0] = 0f;
1080								ai[1] = 50 + Main.rand.Next(50);
1081								ai[2] = 0f;
1082								localAI[3] = 40f;
1083							}
1084						}
1085						if (position.X == localAI[3] && !flag23)
1086						{
1087							direction *= -1;
1088							netUpdate = true;
1089							localAI[3] = num28;
1090						}
1091						if (flag21 && !flag23)
1092						{
1093							if (localAI[3] > (float)num28)
1094							{
1095								localAI[3] = num28;
1096							}
1097							if (localAI[3] > 0f)
1098							{
1099								localAI[3] -= 1f;
1100							}
1101						}
1102						else
1103						{
1104							localAI[3] = -1f;
1105						}
1106						Tile tileSafely3 = Framing.GetTileSafely(num26, num27);
1107						Tile tileSafely4 = Framing.GetTileSafely(num26, num27 - 1);
1108						Tile tileSafely5 = Framing.GetTileSafely(num26, num27 - 2);
1109						bool flag25 = height / 16 < 3;
1110						if (townNPC && tileSafely5.nactive() && (tileSafely5.type == 10 || tileSafely5.type == 388) && (Main.rand.Next(10) == 0 || flag))
1111						{
1112							if (Main.netMode != 1)
1113							{
1114								if (WorldGen.OpenDoor(num26, num27 - 2, direction))
1115								{
1116									closeDoor = true;
1117									doorX = num26;
1118									doorY = num27 - 2;
1119									NetMessage.SendData(19, -1, -1, null, 0, num26, num27 - 2, direction);
1120									netUpdate = true;
1121									ai[1] += 80f;
1122								}
1123								else if (WorldGen.OpenDoor(num26, num27 - 2, -direction))
1124								{
1125									closeDoor = true;
1126									doorX = num26;
1127									doorY = num27 - 2;
1128									NetMessage.SendData(19, -1, -1, null, 0, num26, num27 - 2, -direction);
1129									netUpdate = true;
1130									ai[1] += 80f;
1131								}
1132								else if (WorldGen.ShiftTallGate(num26, num27 - 2, closing: false))
1133								{
1134									closeDoor = true;
1135									doorX = num26;
1136									doorY = num27 - 2;
1137									NetMessage.SendData(19, -1, -1, null, 4, num26, num27 - 2);
1138									netUpdate = true;
1139									ai[1] += 80f;
1140								}
1141								else
1142								{
1143									direction *= -1;
1144									netUpdate = true;
1145								}
1146							}
1147						}
1148						else
1149						{
1150							if ((velocity.X < 0f && direction == -1) || (velocity.X > 0f && direction == 1))
1151							{
1152								bool flag26 = false;
1153								bool flag27 = false;
1154								if (tileSafely5.nactive() && Main.tileSolid[tileSafely5.type] && !Main.tileSolidTop[tileSafely5.type] && (!flag25 || (tileSafely4.nactive() && Main.tileSolid[tileSafely4.type] && !Main.tileSolidTop[tileSafely4.type])))
1155								{
1156									if (!Collision.SolidTilesVersatile(num26 - direction * 2, num26 - direction, num27 - 5, num27 - 1) && !Collision.SolidTiles(num26, num26, num27 - 5, num27 - 3))
1157									{
1158										velocity.Y = -6f;
1159										netUpdate = true;
1160									}
1161									else if (flag7)
1162									{
1163										if (WorldGen.SolidTile((int)(base.Center.X / 16f) + direction, (int)(base.Center.Y / 16f)))
1164										{
1165											direction *= -1;
1166											velocity.X *= 0f;
1167											netUpdate = true;
1168										}
1169									}
1170									else if (flag16)
1171									{
1172										flag27 = true;
1173										flag26 = true;
1174									}
1175									else if (!flag24)
1176									{
1177										flag26 = true;
1178									}
1179								}
1180								else if (tileSafely4.nactive() && Main.tileSolid[tileSafely4.type] && !Main.tileSolidTop[tileSafely4.type])
1181								{
1182									if (!Collision.SolidTilesVersatile(num26 - direction * 2, num26 - direction, num27 - 4, num27 - 1) && !Collision.SolidTiles(num26, num26, num27 - 4, num27 - 2))
1183									{
1184										velocity.Y = -5f;
1185										netUpdate = true;
1186									}
1187									else if (flag16)
1188									{
1189										flag27 = true;
1190										flag26 = true;
1191									}
1192									else
1193									{
1194										flag26 = true;
1195									}
1196								}
1197								else if (position.Y + (float)height - (float)(num27 * 16) > 20f && tileSafely3.nactive() && Main.tileSolid[tileSafely3.type] && !tileSafely3.topSlope())
1198								{
1199									if (!Collision.SolidTilesVersatile(num26 - direction * 2, num26, num27 - 3, num27 - 1))
1200									{
1201										velocity.Y = -4.4f;
1202										netUpdate = true;
1203									}
1204									else if (flag16)
1205									{
1206										flag27 = true;
1207										flag26 = true;
1208									}
1209									else
1210									{
1211										flag26 = true;
1212									}
1213								}
1214								else if (avoidFalling3)
1215								{
1216									if (!flag24)
1217									{
1218										flag26 = true;
1219									}
1220									if (flag16)
1221									{
1222										flag27 = true;
1223									}
1224								}
1225								else if (flag14 && !Collision.SolidTilesVersatile(num26 - direction * 2, num26 - direction, num27 - 2, num27 - 1))
1226								{
1227									velocity.Y = -5f;
1228									netUpdate = true;
1229								}
1230								if (flag27)
1231								{
1232									keepwalking3 = false;
1233									velocity.X = 0f;
1234									ai[0] = 8f;
1235									ai[1] = 240f;
1236									netUpdate = true;
1237								}
1238								if (flag26)
1239								{
1240									direction *= -1;
1241									velocity.X *= -1f;
1242									netUpdate = true;
1243								}
1244								if (keepwalking3)
1245								{
1246									ai[1] = 90f;
1247									netUpdate = true;
1248								}
1249								if (velocity.Y < 0f)
1250								{
1251									localAI[3] = position.X;
1252								}
1253							}
1254							if (velocity.Y < 0f && wet)
1255							{
1256								velocity.Y *= 1.2f;
1257							}
1258							if (velocity.Y < 0f && NPCID.Sets.TownCritter[type] && !flag7)
1259							{
1260								velocity.Y *= 1.2f;
1261							}
1262						}
1263					}
1264					else if (flag14 && !wet)
1265					{
1266						int num36 = (int)(base.Center.X / 16f);
1267						int num37 = (int)((position.Y + (float)height - 16f) / 16f);
1268						int num38 = 0;
1269						for (int num39 = -1; num39 <= 1; num39++)
1270						{
1271							for (int num40 = 1; num40 <= 6; num40++)
1272							{
1273								Tile tileSafely6 = Framing.GetTileSafely(num36 + num39, num37 + num40);
1274								if (tileSafely6.liquid > 0 || (tileSafely6.nactive() && Main.tileSolid[tileSafely6.type]))
1275								{
1276									num38++;
1277								}
1278							}
1279						}
1280						if (num38 <= 2)
1281						{
1282							if (velocity.X != 0f)
1283							{
1284								netUpdate = true;
1285							}
1286							velocity.X *= 0.2f;
1287							ai[0] = 0f;
1288							ai[1] = 50 + Main.rand.Next(50);
1289							ai[2] = 0f;
1290							localAI[3] = 40f;
1291						}
1292					}
1293				}
1294			}
1295			else if (ai[0] == 2f || ai[0] == 11f)
1296			{
1297				if (Main.netMode != 1)
1298				{
1299					localAI[3] -= 1f;
1300					if (Main.rand.Next(60) == 0 && localAI[3] == 0f)
1301					{
1302						localAI[3] = 60f;
1303						direction *= -1;
1304						netUpdate = true;
1305					}
1306				}
1307				ai[1] -= 1f;
1308				velocity.X *= 0.8f;
1309				if (ai[1] <= 0f)
1310				{
1311					localAI[3] = 40f;
1312					ai[0] = 0f;
1313					ai[1] = 60 + Main.rand.Next(60);
1314					netUpdate = true;
1315				}
1316			}
1317			else if (ai[0] == 3f || ai[0] == 4f || ai[0] == 5f || ai[0] == 8f || ai[0] == 9f || ai[0] == 16f || ai[0] == 17f || ai[0] == 20f || ai[0] == 21f || ai[0] == 22f || ai[0] == 23f)
1318			{
1319				velocity.X *= 0.8f;
1320				ai[1] -= 1f;
1321				if (ai[0] == 8f && ai[1] < 60f && flag16)
1322				{
1323					ai[1] = 180f;
1324					netUpdate = true;
1325				}
1326				if (ai[0] == 5f)
1327				{
1328					Point coords = (base.Bottom + Vector2.UnitY * -2f).ToTileCoordinates();
1329					Tile tile = Main.tile[coords.X, coords.Y];
1330					if (tile != null && tile.type != 15 && tile.type != 497)
1331					{
1332						ai[1] = 0f;
1333					}
1334					else
1335					{
1336						Main.sittingManager.AddNPC(whoAmI, coords);
1337					}
1338				}
1339				if (ai[1] <= 0f)
1340				{
1341					ai[0] = 0f;
1342					ai[1] = 60 + Main.rand.Next(60);
1343					ai[2] = 0f;
1344					localAI[3] = 30 + Main.rand.Next(60);
1345					netUpdate = true;
1346				}
1347			}
1348			else if (ai[0] == 6f || ai[0] == 7f || ai[0] == 18f || ai[0] == 19f)
1349			{
1350				if (ai[0] == 18f && (localAI[3] < 1f || localAI[3] > 2f))
1351				{
1352					localAI[3] = 2f;
1353				}
1354				velocity.X *= 0.8f;
1355				ai[1] -= 1f;
1356				int num41 = (int)ai[2];
1357				if (num41 < 0 || num41 > 255 || !Main.player[num41].CanBeTalkedTo || Main.player[num41].Distance(base.Center) > 200f || !Collision.CanHitLine(base.Top, 0, 0, Main.player[num41].Top, 0, 0))
1358				{
1359					ai[1] = 0f;
1360				}
1361				if (ai[1] > 0f)
1362				{
1363					int num42 = ((base.Center.X < Main.player[num41].Center.X) ? 1 : (-1));
1364					if (num42 != direction)
1365					{
1366						netUpdate = true;
1367					}
1368					direction = num42;

```


---

## 🤖 Assistant · 2026-08-11T04:52:59.235Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I now have a good grasp of AI_007's walk/jump state machine. Now let me look at the shared "out of AI" critter handling — e.g. StrikeNPC catch handling, wet handling, and the common AI section for critters (e.g., `townNPC == false && CountsAsCritter`?). Since CountsAsCritter doesn't exist, critter handling in vanilla is via NPCID.Sets.

Now let me read aiStyle 64, 65, 66, 67, 68 blocks in NPC.cs. Block ranges:
- 64: 34256–34486 (230 lines)
- 65: 34486–34490 (4 lines? probably delegates)
- 66: 34490–34586
- 67: 34586–34861
- 68: 34861–35118

Let me read 34256–35118 in one go (862 lines).
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:52:59.440Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "offset": 34256,
 "limit": 862
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:52:59.453Z

**📎 ToolResult**

```
34256			else if (aiStyle == 64)
34257			{
34258				float num1022 = this.ai[0];
34259				float num1023 = this.ai[1];
34260				if (Main.netMode != 1)
34261				{
34262					localAI[0] -= 1f;
34263					if (this.ai[3] == 0f)
34264					{
34265						this.ai[3] = (float)Main.rand.Next(75, 111) * 0.01f;
34266					}
34267					if (localAI[0] <= 0f)
34268					{
34269						TargetClosest();
34270						localAI[0] = Main.rand.Next(60, 180);
34271						float num1024 = Math.Abs(base.Center.X - Main.player[target].Center.X);
34272						if (num1024 > 700f && localAI[3] == 0f)
34273						{
34274							float num1025 = (float)Main.rand.Next(50, 151) * 0.01f;
34275							if (num1024 > 1000f)
34276							{
34277								num1025 = (float)Main.rand.Next(150, 201) * 0.01f;
34278							}
34279							else if (num1024 > 850f)
34280							{
34281								num1025 = (float)Main.rand.Next(100, 151) * 0.01f;
34282							}
34283							int num1026 = direction * Main.rand.Next(100, 251);
34284							int num1027 = Main.rand.Next(-50, 51);
34285							if (position.Y > Main.player[target].position.Y - 100f)
34286							{
34287								num1027 -= Main.rand.Next(100, 251);
34288							}
34289							float num1028 = num1025 / (float)Math.Sqrt(num1026 * num1026 + num1027 * num1027);
34290							num1022 = (float)num1026 * num1028;
34291							num1023 = (float)num1027 * num1028;
34292						}
34293						else
34294						{
34295							localAI[3] = 1f;
34296							float num1029 = (float)Main.rand.Next(5, 151) * 0.01f;
34297							int num1030 = Main.rand.Next(-100, 101);
34298							int num1031 = Main.rand.Next(-100, 101);
34299							float num1032 = num1029 / (float)Math.Sqrt(num1030 * num1030 + num1031 * num1031);
34300							num1022 = (float)num1030 * num1032;
34301							num1023 = (float)num1031 * num1032;
34302						}
34303						netUpdate = true;
34304					}
34305				}
34306				scale = this.ai[3];
34307				if (type == 677)
34308				{
34309					bool flag61 = true;
34310					Point point4 = base.Center.ToTileCoordinates();
34311					int num1033 = 40;
34312					if (point4.X < num1033)
34313					{
34314						num1022 += 0.5f;
34315						if (num1022 > 3f)
34316						{
34317							num1022 = 3f;
34318						}
34319						flag61 = false;
34320					}
34321					else if (point4.X > Main.maxTilesX - num1033)
34322					{
34323						num1022 -= 0.5f;
34324						if (num1022 < -3f)
34325						{
34326							num1022 = -3f;
34327						}
34328						flag61 = false;
34329					}
34330					if (point4.Y < num1033)
34331					{
34332						num1023 += 0.5f;
34333						if (num1023 > 3f)
34334						{
34335							velocity.Y = 3f;
34336						}
34337						flag61 = false;
34338					}
34339					else if (point4.Y > Main.maxTilesY - num1033)
34340					{
34341						num1023 -= 0.5f;
34342						if (num1023 < -3f)
34343						{
34344							num1023 = -3f;
34345						}
34346						flag61 = false;
34347					}
34348					if (localAI[1] > 0f)
34349					{
34350						localAI[1]--;
34351					}
34352					else if (flag61)
34353					{
34354						localAI[1] = 15f;
34355						float num1034 = 0f;
34356						Vector2 zero = Vector2.Zero;
34357						for (int num1035 = 0; num1035 < Main.maxNPCs; num1035++)
34358						{
34359							NPC nPC5 = Main.npc[num1035];
34360							if (nPC5.active && nPC5.damage > 0 && !nPC5.friendly && nPC5.Hitbox.Distance(base.Center) <= 100f)
34361							{
34362								num1034++;
34363								zero += DirectionFrom(nPC5.Center);
34364							}
34365						}
34366						for (int num1036 = 0; num1036 < 255; num1036++)
34367						{
34368							Player player9 = Main.player[num1036];
34369							if (player9.active && player9.Hitbox.Distance(base.Center) <= 150f)
34370							{
34371								num1034++;
34372								zero += DirectionFrom(player9.Center);
34373							}
34374						}
34375						if (num1034 > 0f)
34376						{
34377							float num1037 = 2f;
34378							zero /= num1034;
34379							zero *= num1037;
34380							velocity += zero;
34381							if (velocity.Length() > 8f)
34382							{
34383								velocity = velocity.SafeNormalize(Vector2.Zero) * 8f;
34384							}
34385							Vector2 vector123 = base.Center + zero * 10f;
34386							localAI[0] = 10f;
34387							netUpdate = true;
34388						}
34389					}
34390				}
34391				else if (localAI[2] > 0f)
34392				{
34393					int i3 = (int)base.Center.X / 16;
34394					int j3 = (int)base.Center.Y / 16;
34395					if (localAI[2] > 3f)
34396					{
34397						if (type == 358)
34398						{
34399							Lighting.AddLight(i3, j3, 0.10124999f * scale, 0.21374999f * scale, 0.225f * scale);
34400						}
34401						else if (type == 654)
34402						{
34403							Lighting.AddLight(i3, j3, 0.225f * scale, 0.105000004f * scale, 0.060000002f * scale);
34404						}
34405						else
34406						{
34407							Lighting.AddLight(i3, j3, 0.109500006f * scale, 0.15f * scale, 0.0615f * scale);
34408						}
34409					}
34410					localAI[2] -= 1f;
34411				}
34412				else if (localAI[1] > 0f)
34413				{
34414					localAI[1] -= 1f;
34415				}
34416				else
34417				{
34418					localAI[1] = Main.rand.Next(30, 180);
34419					if (!Main.dayTime || (double)(position.Y / 16f) > Main.worldSurface + 10.0)
34420					{
34421						localAI[2] = Main.rand.Next(10, 30);
34422					}
34423				}
34424				int num1038 = 80;
34425				velocity.X = (velocity.X * (float)(num1038 - 1) + num1022) / (float)num1038;
34426				velocity.Y = (velocity.Y * (float)(num1038 - 1) + num1023) / (float)num1038;
34427				if (velocity.Y > 0f)
34428				{
34429					int num1039 = 4;
34430					int num1040 = (int)base.Center.X / 16;
34431					int num1041 = (int)base.Center.Y / 16;
34432					for (int num1042 = num1041; num1042 < num1041 + num1039; num1042++)
34433					{
34434						if (WorldGen.InWorld(num1040, num1042, 2) && Main.tile[num1040, num1042] != null && ((Main.tile[num1040, num1042].nactive() && Main.tileSolid[Main.tile[num1040, num1042].type]) || Main.tile[num1040, num1042].liquid > 0))
34435						{
34436							num1023 *= -1f;
34437							if (velocity.Y > 0f)
34438							{
34439								velocity.Y *= 0.9f;
34440							}
34441						}
34442					}
34443				}
34444				if (velocity.Y < 0f)
34445				{
34446					int num1043 = 30;
34447					bool flag62 = false;
34448					int num1044 = (int)base.Center.X / 16;
34449					int num1045 = (int)base.Center.Y / 16;
34450					for (int num1046 = num1045; num1046 < num1045 + num1043; num1046++)
34451					{
34452						if (WorldGen.InWorld(num1044, num1046, 2) && Main.tile[num1044, num1046] != null && Main.tile[num1044, num1046].nactive() && Main.tileSolid[Main.tile[num1044, num1046].type])
34453						{
34454							flag62 = true;
34455						}
34456					}
34457					if (!flag62)
34458					{
34459						num1023 *= -1f;
34460						if (velocity.Y < 0f)
34461						{
34462							velocity.Y *= 0.9f;
34463						}
34464					}
34465				}
34466				if (collideX)
34467				{
34468					num1022 = ((!(velocity.X < 0f)) ? (0f - Math.Abs(num1022)) : Math.Abs(num1022));
34469					velocity.X *= -0.2f;
34470				}
34471				if (type == 677)
34472				{
34473					rotation = velocity.X * 0.3f;
34474				}
34475				if (velocity.X < 0f)
34476				{
34477					direction = -1;
34478				}
34479				if (velocity.X > 0f)
34480				{
34481					direction = 1;
34482				}
34483				this.ai[0] = num1022;
34484				this.ai[1] = num1023;
34485			}
34486			else if (aiStyle == 65)
34487			{
34488				AI_065_Butterflies();
34489			}
34490			else if (aiStyle == 66)
34491			{
34492				if (type == 484)
34493				{
34494					float num1047 = (float)Main.rand.Next(90, 111) * 0.01f;
34495					num1047 *= (Main.essScale + 0.5f) / 2f;
34496					Lighting.AddLight((int)((position.X + (float)(width / 2)) / 16f), (int)((position.Y + (float)(height / 2)) / 16f), 0.3f * num1047, 0.1f * num1047, 0.25f * num1047);
34497				}
34498				if (velocity.Y == 0f)
34499				{
34500					if (this.ai[0] == 1f)
34501					{
34502						if (direction == 0)
34503						{
34504							TargetClosest();
34505						}
34506						if (collideX)
34507						{
34508							direction *= -1;
34509						}
34510						float num1048 = 0.2f;
34511						if (type == 485)
34512						{
34513							num1048 = 0.25f;
34514						}
34515						if (type == 486)
34516						{
34517							num1048 = 0.325f;
34518						}
34519						if (type == 487)
34520						{
34521							num1048 = 0.4f;
34522						}
34523						velocity.X = num1048 * (float)direction;
34524						if (type == 374)
34525						{
34526							velocity.X *= 3f;
34527						}
34528					}
34529					else
34530					{
34531						velocity.X = 0f;
34532					}
34533					if (Main.netMode != 1)
34534					{
34535						localAI[1] -= 1f;
34536						if (localAI[1] <= 0f)
34537						{
34538							if (this.ai[0] == 1f)
34539							{
34540								this.ai[0] = 0f;
34541								localAI[1] = Main.rand.Next(300, 900);
34542							}
34543							else
34544							{
34545								this.ai[0] = 1f;
34546								localAI[1] = Main.rand.Next(600, 1800);
34547							}
34548							netUpdate = true;
34549						}
34550					}
34551				}
34552				else if (direction == 0)
34553				{
34554					direction = 1;
34555					if (velocity.X < 0f)
34556					{
34557						direction = -1;
34558					}
34559				}
34560				if (type != 374)
34561				{
34562					return;
34563				}
34564				spriteDirection = direction;
34565				bool flag63 = false;
34566				for (int num1049 = 0; num1049 < 255; num1049++)
34567				{
34568					Player player10 = Main.player[num1049];
34569					if (player10.active && !player10.dead && !(Vector2.Distance(player10.Center, base.Center) > 160f))
34570					{
34571						flag63 = true;
34572						break;
34573					}
34574				}
34575				int num1050 = 90;
34576				if (flag63 && this.ai[1] < (float)num1050)
34577				{
34578					this.ai[1]++;
34579				}
34580				if (this.ai[1] == (float)num1050 && Main.netMode != 1)
34581				{
34582					position.Y += 16f;
34583					Transform(375);
34584				}
34585			}
34586			else if (aiStyle == 67)
34587			{
34588				if (Main.netMode != 1)
34589				{
34590					int num1051 = (int)MathHelper.Clamp((int)(base.Center.X / 16f), 0f, Main.maxTilesX);
34591					int num1052 = (int)MathHelper.Clamp((int)(base.Center.Y / 16f), 0f, Main.maxTilesY);
34592					Tile tile = Main.tile[num1051, num1052];
34593					if (tile != null && tile.shimmer() && tile.liquid > 30)
34594					{
34595						GetShimmered();
34596						return;
34597					}
34598				}
34599				if (type == 359)
34600				{
34601					if (this.ai[3] != 0f)
34602					{
34603						scale = this.ai[3];
34604						int num1053 = (int)(12f * scale);
34605						int num1054 = (int)(12f * scale);
34606						if (num1053 != width)
34607						{
34608							position.X = position.X + (float)(width / 2) - (float)num1053 - 2f;
34609							width = num1053;
34610						}
34611						if (num1054 != height)
34612						{
34613							position.Y = position.Y + (float)height - (float)num1054;
34614							height = num1054;
34615						}
34616					}
34617					if (this.ai[3] == 0f && Main.netMode != 1)
34618					{
34619						this.ai[3] = (float)Main.rand.Next(80, 111) * 0.01f;
34620						netUpdate = true;
34621					}
34622				}
34623				if (type == 360)
34624				{
34625					Lighting.AddLight((int)base.Center.X / 16, (int)base.Center.Y / 16, 0.1f, 0.2f, 0.7f);
34626				}
34627				if (type == 655)
34628				{
34629					Lighting.AddLight((int)base.Center.X / 16, (int)base.Center.Y / 16, 0.6f, 0.3f, 0.1f);
34630				}
34631				float num1055 = 0.3f;
34632				if (type == 360 || type == 655)
34633				{
34634					num1055 = 0.6f;
34635				}
34636				if (this.ai[0] == 0f)
34637				{
34638					TargetClosest();
34639					directionY = 1;
34640					this.ai[0] = 1f;
34641					if (direction > 0)
34642					{
34643						spriteDirection = 1;
34644					}
34645				}
34646				bool flag64 = false;
34647				if (Main.netMode != 1)
34648				{
34649					if (this.ai[2] == 0f && Main.rand.Next(7200) == 0)
34650					{
34651						this.ai[2] = 2f;
34652						netUpdate = true;
34653					}
34654					if (!collideX && !collideY)
34655					{
34656						localAI[3] += 1f;
34657						if (localAI[3] > 5f)
34658						{
34659							this.ai[2] = 2f;
34660							netUpdate = true;
34661						}
34662					}
34663					else
34664					{
34665						localAI[3] = 0f;
34666					}
34667				}
34668				if (this.ai[2] > 0f)
34669				{
34670					this.ai[1] = 0f;
34671					this.ai[0] = 1f;
34672					directionY = 1;
34673					if (velocity.Y > num1055)
34674					{
34675						rotation += (float)direction * 0.1f;
34676					}
34677					else
34678					{
34679						rotation = 0f;
34680					}
34681					spriteDirection = direction;
34682					velocity.X = num1055 * (float)direction;
34683					noGravity = false;
34684					int num1056 = (int)(base.Center.X + (float)(width / 2 * -direction)) / 16;
34685					int num1057 = (int)(position.Y + (float)height + 8f) / 16;
34686					if (Main.tile[num1056, num1057] != null && !Main.tile[num1056, num1057].topSlope() && collideY)
34687					{
34688						this.ai[2] -= 1f;
34689					}
34690					num1057 = (int)(position.Y + (float)height - 4f) / 16;
34691					num1056 = (int)(base.Center.X + (float)(width / 2 * direction)) / 16;
34692					if (Main.tile[num1056, num1057] != null && Main.tile[num1056, num1057].bottomSlope())
34693					{
34694						direction *= -1;
34695					}
34696					if (collideX && velocity.Y == 0f)
34697					{
34698						flag64 = true;
34699						this.ai[2] = 0f;
34700						directionY = -1;
34701						this.ai[1] = 1f;
34702					}
34703					if (velocity.Y == 0f)
34704					{
34705						if (localAI[1] == position.X)
34706						{
34707							localAI[2] += 1f;
34708							if (localAI[2] > 10f)
34709							{
34710								direction = 1;
34711								velocity.X = (float)direction * num1055;
34712								localAI[2] = 0f;
34713							}
34714						}
34715						else
34716						{
34717							localAI[2] = 0f;
34718							localAI[1] = position.X;
34719						}
34720					}
34721				}
34722				if (this.ai[2] != 0f)
34723				{
34724					return;
34725				}
34726				noGravity = true;
34727				if (this.ai[1] == 0f)
34728				{
34729					if (collideY)
34730					{
34731						this.ai[0] = 2f;
34732					}
34733					if (!collideY && this.ai[0] == 2f)
34734					{
34735						direction = -direction;
34736						this.ai[1] = 1f;
34737						this.ai[0] = 1f;
34738					}
34739					if (collideX)
34740					{
34741						directionY = -directionY;
34742						this.ai[1] = 1f;
34743					}
34744				}
34745				else
34746				{
34747					if (collideX)
34748					{
34749						this.ai[0] = 2f;
34750					}
34751					if (!collideX && this.ai[0] == 2f)
34752					{
34753						directionY = -directionY;
34754						this.ai[1] = 0f;
34755						this.ai[0] = 1f;
34756					}
34757					if (collideY)
34758					{
34759						direction = -direction;
34760						this.ai[1] = 0f;
34761					}
34762				}
34763				if (!flag64)
34764				{
34765					float num1058 = rotation;
34766					if (directionY < 0)
34767					{
34768						if (direction < 0)
34769						{
34770							if (collideX)
34771							{
34772								rotation = 1.57f;
34773								spriteDirection = -1;
34774							}
34775							else if (collideY)
34776							{
34777								rotation = 3.14f;
34778								spriteDirection = 1;
34779							}
34780						}
34781						else if (collideY)
34782						{
34783							rotation = 3.14f;
34784							spriteDirection = -1;
34785						}
34786						else if (collideX)
34787						{
34788							rotation = 4.71f;
34789							spriteDirection = 1;
34790						}
34791					}
34792					else if (direction < 0)
34793					{
34794						if (collideY)
34795						{
34796							rotation = 0f;
34797							spriteDirection = -1;
34798						}
34799						else if (collideX)
34800						{
34801							rotation = 1.57f;
34802							spriteDirection = 1;
34803						}
34804					}
34805					else if (collideX)
34806					{
34807						rotation = 4.71f;
34808						spriteDirection = -1;
34809					}
34810					else if (collideY)
34811					{
34812						rotation = 0f;
34813						spriteDirection = 1;
34814					}
34815					float num1059 = rotation;
34816					rotation = num1058;
34817					if ((double)rotation > 6.28)
34818					{
34819						rotation -= 6.28f;
34820					}
34821					if (rotation < 0f)
34822					{
34823						rotation += 6.28f;
34824					}
34825					float num1060 = Math.Abs(rotation - num1059);
34826					float num1061 = 0.1f;
34827					if (rotation > num1059)
34828					{
34829						if ((double)num1060 > 3.14)
34830						{
34831							rotation += num1061;
34832						}
34833						else
34834						{
34835							rotation -= num1061;
34836							if (rotation < num1059)
34837							{
34838								rotation = num1059;
34839							}
34840						}
34841					}
34842					if (rotation < num1059)
34843					{
34844						if ((double)num1060 > 3.14)
34845						{
34846							rotation -= num1061;
34847						}
34848						else
34849						{
34850							rotation += num1061;
34851							if (rotation > num1059)
34852							{
34853								rotation = num1059;
34854							}
34855						}
34856					}
34857				}
34858				velocity.X = num1055 * (float)direction;
34859				velocity.Y = num1055 * (float)directionY;
34860			}
34861			else if (aiStyle == 68)
34862			{
34863				if (Main.netMode != 1 && this.ai[0] == 1f && NPCID.Sets.BirdThatCanPoop[type] && localAI[3] == 0f)
34864				{
34865					int num1062 = Player.FindClosest(position, width, height);
34866					float x3 = base.Center.X;
34867					if (x3 >= Main.player[num1062].Left.X && x3 <= Main.player[num1062].Right.X && Main.player[num1062].Top.Y > base.Bottom.Y && Collision.CanHit(this, Main.player[num1062]) && (Main.player[num1062].RollOnlyBadLuckExtreme(50) == 0 || Main.player[num1062].IsThisCenx()))
34868					{
34869						localAI[3] = 1f;
34870						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), Main.player[num1062].Center.X, base.Center.Y, 0f, 0f, 1080, 0, 0f);
34871					}
34872				}
34873				noGravity = true;
34874				if (this.ai[0] == 0f)
34875				{
34876					noGravity = false;
34877					int num1063 = direction;
34878					int num1064 = target;
34879					TargetClosest();
34880					if (num1064 >= 0 && num1063 != 0)
34881					{
34882						direction = num1063;
34883					}
34884					if (wet && WorldGen.InWorld((int)(base.Center.X + (float)((width / 2 + 8) * direction)) / 16, (int)(base.Center.Y / 16f), 5))
34885					{
34886						float num1065 = 2f;
34887						velocity.X = (velocity.X * 19f + num1065 * (float)direction) / 20f;
34888						int num1066 = (int)(base.Center.X + (float)((width / 2 + 8) * direction)) / 16;
34889						int num1067 = (int)(base.Center.Y / 16f);
34890						int j4 = (int)(position.Y / 16f);
34891						int num1068 = (int)((position.Y + (float)height) / 16f);
34892						if (Main.tile[num1066, num1067] == null)
34893						{
34894							Main.tile[num1066, num1067] = new Tile();
34895						}
34896						if (Main.tile[num1066, num1068] == null)
34897						{
34898							Main.tile[num1066, num1068] = new Tile();
34899						}
34900						if (num1066 < 5 || num1066 > Main.maxTilesX - 5 || WorldGen.SolidTile(num1066, num1067) || WorldGen.SolidTile(num1066, j4) || WorldGen.SolidTile(num1066, num1068) || Main.tile[num1066, num1068].liquid == 0)
34901						{
34902							direction *= -1;
34903						}
34904						spriteDirection = direction;
34905						if (velocity.Y > 0f)
34906						{
34907							velocity.Y *= 0.5f;
34908						}
34909						noGravity = true;
34910						num1066 = (int)(base.Center.X / 16f);
34911						num1067 = (int)(base.Center.Y / 16f);
34912						float num1069 = position.Y + (float)height;
34913						if (Main.tile[num1066, num1067 - 1] == null)
34914						{
34915							Main.tile[num1066, num1067 - 1] = new Tile();
34916						}
34917						if (Main.tile[num1066, num1067] == null)
34918						{
34919							Main.tile[num1066, num1067] = new Tile();
34920						}
34921						if (Main.tile[num1066, num1067 + 1] == null)
34922						{
34923							Main.tile[num1066, num1067 + 1] = new Tile();
34924						}
34925						if (Main.tile[num1066, num1067 - 1].liquid > 0)
34926						{
34927							num1069 = num1067 * 16;
34928							num1069 -= (float)(Main.tile[num1066, num1067 - 1].liquid / 16);
34929						}
34930						else if (Main.tile[num1066, num1067].liquid > 0)
34931						{
34932							num1069 = (num1067 + 1) * 16;
34933							num1069 -= (float)(Main.tile[num1066, num1067].liquid / 16);
34934						}
34935						else if (Main.tile[num1066, num1067 + 1].liquid > 0)
34936						{
34937							num1069 = (num1067 + 2) * 16;
34938							num1069 -= (float)(Main.tile[num1066, num1067 + 1].liquid / 16);
34939						}
34940						num1069 -= 6f;
34941						if (base.Center.Y > num1069)
34942						{
34943							velocity.Y -= 0.1f;
34944							if (velocity.Y < -8f)
34945							{
34946								velocity.Y = -8f;
34947							}
34948							if (base.Center.Y + velocity.Y < num1069)
34949							{
34950								velocity.Y = num1069 - base.Center.Y;
34951							}
34952						}
34953						else
34954						{
34955							velocity.Y = num1069 - base.Center.Y;
34956						}
34957					}
34958					if (Main.netMode == 1)
34959					{
34960						return;
34961					}
34962					if (!wet)
34963					{
34964						this.ai[0] = 1f;
34965						netUpdate = true;
34966						direction = -direction;
34967						return;
34968					}
34969					Rectangle rectangle4 = new Rectangle((int)Main.player[target].position.X, (int)Main.player[target].position.Y, Main.player[target].width, Main.player[target].height);
34970					if (new Rectangle((int)position.X - 100, (int)position.Y - 100, width + 200, height + 200).Intersects(rectangle4) || life < lifeMax)
34971					{
34972						this.ai[0] = 1f;
34973						velocity.Y -= 6f;
34974						netUpdate = true;
34975						direction = -direction;
34976					}
34977				}
34978				else
34979				{
34980					if (Main.player[target].dead)
34981					{
34982						return;
34983					}
34984					bool flag65 = false;
34985					this.ai[1] += 1f;
34986					if (this.ai[1] >= 300f)
34987					{
34988						flag65 = true;
34989					}
34990					if (flag65)
34991					{
34992						if (velocity.Y == 0f || collideY || wet)
34993						{
34994							velocity.X = 0f;
34995							velocity.Y = 0f;
34996							this.ai[0] = 0f;
34997							this.ai[1] = 0f;
34998							if (Main.netMode != 1)
34999							{
35000								if ((type == 363 || type == 365 || type == 603 || type == 609) && !wet)
35001								{
35002									Transform(type - 1, 0f, 200 + Main.rand.Next(200));
35003								}
35004								netUpdate = true;
35005							}
35006						}
35007						else
35008						{
35009							velocity.X *= 0.98f;
35010							velocity.Y += 0.1f;
35011							if (velocity.Y > 2f)
35012							{
35013								velocity.Y = 2f;
35014							}
35015						}
35016						return;
35017					}
35018					if (collideX)
35019					{
35020						direction *= -1;
35021						velocity.X = oldVelocity.X * -0.5f;
35022						if (direction == -1 && velocity.X > 0f && velocity.X < 2f)
35023						{
35024							velocity.X = 2f;
35025						}
35026						if (direction == 1 && velocity.X < 0f && velocity.X > -2f)
35027						{
35028							velocity.X = -2f;
35029						}
35030					}
35031					if (collideY)
35032					{
35033						velocity.Y = oldVelocity.Y * -0.5f;
35034						if (velocity.Y > 0f && velocity.Y < 1f)
35035						{
35036							velocity.Y = 1f;
35037						}
35038						if (velocity.Y < 0f && velocity.Y > -1f)
35039						{
35040							velocity.Y = -1f;
35041						}
35042					}
35043					if (direction == -1 && velocity.X > -3f)
35044					{
35045						velocity.X -= 0.1f;
35046						if (velocity.X > 3f)
35047						{
35048							velocity.X -= 0.1f;
35049						}
35050						else if (velocity.X > 0f)
35051						{
35052							velocity.X -= 0.05f;
35053						}
35054						if (velocity.X < -3f)
35055						{
35056							velocity.X = -3f;
35057						}
35058					}
35059					else if (direction == 1 && velocity.X < 3f)
35060					{
35061						velocity.X += 0.1f;
35062						if (velocity.X < -3f)
35063						{
35064							velocity.X += 0.1f;
35065						}
35066						else if (velocity.X < 0f)
35067						{
35068							velocity.X += 0.05f;
35069						}
35070						if (velocity.X > 3f)
35071						{
35072							velocity.X = 3f;
35073						}
35074					}
35075					int num1070 = (int)((position.X + (float)(width / 2)) / 16f) + direction;
35076					int num1071 = (int)((position.Y + (float)height) / 16f);
35077					bool flag66 = true;
35078					int num1072 = 15;
35079					bool flag67 = false;
35080					for (int num1073 = num1071; num1073 < num1071 + num1072; num1073++)
35081					{
35082						if (Main.tile[num1070, num1073] == null)
35083						{
35084							Main.tile[num1070, num1073] = new Tile();
35085						}
35086						if ((Main.tile[num1070, num1073].nactive() && Main.tileSolid[Main.tile[num1070, num1073].type]) || Main.tile[num1070, num1073].liquid > 0)
35087						{
35088							if (num1073 < num1071 + 5)
35089							{
35090								flag67 = true;
35091							}
35092							flag66 = false;
35093							break;
35094						}
35095					}
35096					if (flag66)
35097					{
35098						velocity.Y += 0.1f;
35099					}
35100					else
35101					{
35102						velocity.Y -= 0.1f;
35103					}
35104					if (flag67)
35105					{
35106						velocity.Y -= 0.2f;
35107					}
35108					if (velocity.Y > 3f)
35109					{
35110						velocity.Y = 3f;
35111					}
35112					if (velocity.Y < -4f)
35113					{
35114						velocity.Y = -4f;
35115					}
35116				}
35117			}

```


---

## 🤖 Assistant · 2026-08-11T04:53:01.758Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Excellent. That covers 64, 66, 67, 68. Now 65 = AI_065_Butterflies(). Find it. Also 112 (AI_112_FairyCritter 48453), 114 (AI_114_Dragonflies 48080), 115 (AI_115_LadyBugs 47944), 116 (AI_116_WaterStriders 47882), 118 (AI_118_Seahorses 47432). And AI_001 grasshopper, AI_016 fish.

Let me find AI_065_Butterflies.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:53:02.257Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"private void AI_065_Butterflies\\|private void AI_001(\\|private void AI_016\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Locate AI_065, AI_001, AI_016 method lines"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:53:02.295Z

**📎 ToolResult**

```
45231:	private void AI_065_Butterflies()

```


---

## 🤖 Assistant · 2026-08-11T04:53:08.215Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 215,
 "offset": 45231
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:53:08.223Z

**📎 ToolResult**

```
45231		private void AI_065_Butterflies()
45232		{
45233			float num = ai[0];
45234			float num2 = ai[1];
45235			if (type == 661)
45236			{
45237				Vector3 rgb = Main.hslToRgb(Main.GlobalTimeWrappedHourly * 0.33f % 1f, 1f, 0.5f).ToVector3() * 0.3f;
45238				rgb += Vector3.One * 0.1f;
45239				Lighting.AddLight(base.Center, rgb);
45240				int num3 = 60;
45241				bool flag = false;
45242				int num4 = 50;
45243				NPCAimedTarget targetData = GetTargetData();
45244				if (targetData.Invalid || targetData.Center.Distance(base.Center) >= 300f)
45245				{
45246					flag = true;
45247				}
45248				if (!Main.remixWorld && !targetData.Invalid && targetData.Type == NPCTargetType.Player && !Main.player[target].ZoneHallow)
45249				{
45250					num4 = num3;
45251					flag = true;
45252				}
45253				ai[2] = MathHelper.Clamp(ai[2] + (float)flag.ToDirectionInt(), 0f, num4);
45254				if (ai[2] >= (float)num3)
45255				{
45256					active = false;
45257					if (Main.netMode != 1)
45258					{
45259						NetMessage.SendData(23, -1, -1, null, whoAmI);
45260					}
45261					return;
45262				}
45263				Opacity = Utils.GetLerpValue(num3, (float)num4 / 2f, ai[2], clamped: true);
45264				if (ai[2] > 0f)
45265				{
45266					int num5 = 1;
45267					for (int i = 0; i < num5; i++)
45268					{
45269						if (Main.rand.Next(5) == 0)
45270						{
45271							float num6 = MathHelper.Lerp(0.9f, 0.6f, Opacity);
45272							Color newColor = Main.hslToRgb(Main.GlobalTimeWrappedHourly * 0.3f % 1f, 1f, 0.5f) * 0.5f;
45273							int num7 = Dust.NewDust(position, width, height, 267, 0f, 0f, 0, newColor);
45274							Main.dust[num7].position = base.Center + Main.rand.NextVector2Circular(width, height);
45275							Main.dust[num7].velocity *= Main.rand.NextFloat() * 0.8f;
45276							Main.dust[num7].velocity += velocity * 0.6f;
45277							Main.dust[num7].noGravity = true;
45278							Main.dust[num7].fadeIn = 0.6f + Main.rand.NextFloat() * 0.7f * num6;
45279							Main.dust[num7].scale = 0.35f;
45280							if (num7 != 6000)
45281							{
45282								Dust dust = Dust.CloneDust(num7);
45283								dust.scale /= 2f;
45284								dust.fadeIn *= 0.85f;
45285								dust.color = new Color(255, 255, 255, 255) * 0.5f;
45286							}
45287						}
45288					}
45289				}
45290				dontTakeDamage = ai[2] >= (float)(num4 / 2);
45291			}
45292			if (Main.netMode != 1)
45293			{
45294				if (ai[2] == 0f && type != 661)
45295				{
45296					int num8 = 0;
45297					int num9 = 4;
45298					int num10 = 6;
45299					int num11 = 3;
45300					int num12 = 7;
45301					int num13 = 2;
45302					int num14 = 1;
45303					int num15 = 5;
45304					int num16 = Main.rand.Next(100);
45305					num16 = ((num16 == 0) ? num15 : ((num16 < 3) ? num14 : ((num16 < 9) ? num13 : ((num16 < 19) ? num12 : ((num16 < 34) ? num11 : ((num16 < 53) ? num10 : ((num16 >= 75) ? num8 : num9)))))));
45306					ai[2] = 1 + num16;
45307				}
45308				if (ai[3] == 0f)
45309				{
45310					ai[3] = (float)Main.rand.Next(75, 111) * 0.01f;
45311				}
45312				localAI[0] -= 1f;
45313				if (localAI[0] <= 0f)
45314				{
45315					localAI[0] = Main.rand.Next(90, 240);
45316					TargetClosest();
45317					float num17 = Math.Abs(base.Center.X - Main.player[target].Center.X);
45318					if (num17 > 700f && localAI[3] == 0f)
45319					{
45320						float num18 = (float)Main.rand.Next(50, 151) * 0.01f;
45321						if (num17 > 1000f)
45322						{
45323							num18 = (float)Main.rand.Next(150, 201) * 0.01f;
45324						}
45325						else if (num17 > 850f)
45326						{
45327							num18 = (float)Main.rand.Next(100, 151) * 0.01f;
45328						}
45329						int num19 = direction * Main.rand.Next(100, 251);
45330						int num20 = Main.rand.Next(-50, 51);
45331						if (position.Y > Main.player[target].position.Y - 100f)
45332						{
45333							num20 -= Main.rand.Next(100, 251);
45334						}
45335						float num21 = num18 / (float)Math.Sqrt(num19 * num19 + num20 * num20);
45336						num = (float)num19 * num21;
45337						num2 = (float)num20 * num21;
45338					}
45339					else
45340					{
45341						localAI[3] = 1f;
45342						float num22 = (float)Main.rand.Next(26, 301) * 0.01f;
45343						int num23 = Main.rand.Next(-100, 101);
45344						int num24 = Main.rand.Next(-100, 101);
45345						float num25 = num22 / (float)Math.Sqrt(num23 * num23 + num24 * num24);
45346						num = (float)num23 * num25;
45347						num2 = (float)num24 * num25;
45348					}
45349					netUpdate = true;
45350				}
45351			}
45352			scale = ai[3];
45353			int num26 = 60;
45354			velocity.X = (velocity.X * (float)(num26 - 1) + num) / (float)num26;
45355			velocity.Y = (velocity.Y * (float)(num26 - 1) + num2) / (float)num26;
45356			if (velocity.Y > 0f)
45357			{
45358				int num27 = 3;
45359				int num28 = (int)base.Center.X / 16;
45360				int num29 = (int)base.Center.Y / 16;
45361				for (int j = num29; j < num29 + num27; j++)
45362				{
45363					if (Main.tile[num28, j] != null && ((Main.tile[num28, j].nactive() && Main.tileSolid[Main.tile[num28, j].type]) || Main.tile[num28, j].liquid > 0))
45364					{
45365						num2 *= -1f;
45366						if (velocity.Y > 0f)
45367						{
45368							velocity.Y *= 0.9f;
45369						}
45370					}
45371				}
45372			}
45373			if (velocity.Y < 0f)
45374			{
45375				int num30 = 30;
45376				bool flag2 = false;
45377				int num31 = (int)base.Center.X / 16;
45378				int num32 = (int)base.Center.Y / 16;
45379				for (int k = num32; k < num32 + num30; k++)
45380				{
45381					if (Main.tile[num31, k] != null && Main.tile[num31, k].nactive() && Main.tileSolid[Main.tile[num31, k].type])
45382					{
45383						flag2 = true;
45384					}
45385				}
45386				if (!flag2)
45387				{
45388					num2 *= -1f;
45389					if (velocity.Y < 0f)
45390					{
45391						velocity.Y *= 0.9f;
45392					}
45393				}
45394			}
45395			if (localAI[1] > 0f)
45396			{
45397				localAI[1] -= 1f;
45398			}
45399			else
45400			{
45401				localAI[1] = 15f;
45402				if (type == 661)
45403				{
45404					localAI[1] = 10f;
45405				}
45406				float num33 = 0f;
45407				Vector2 zero = Vector2.Zero;
45408				for (int l = 0; l < Main.maxNPCs; l++)
45409				{
45410					NPC nPC = Main.npc[l];
45411					if (nPC.active && nPC.damage > 0 && !nPC.friendly && nPC.Hitbox.Distance(base.Center) <= 100f)
45412					{
45413						num33 += 1f;
45414						zero += DirectionFrom(nPC.Center);
45415					}
45416				}
45417				if (num33 > 0f)
45418				{
45419					zero /= num33;
45420					zero *= 2f;
45421					velocity += zero;
45422					if (velocity.Length() > 16f)
45423					{
45424						velocity = velocity.SafeNormalize(Vector2.Zero) * 16f;
45425					}
45426				}
45427			}
45428			if (collideX)
45429			{
45430				num = ((!(velocity.X < 0f)) ? (0f - Math.Abs(num)) : Math.Abs(num));
45431				velocity.X *= -0.2f;
45432			}
45433			if (velocity.X < 0f)
45434			{
45435				direction = -1;
45436			}
45437			if (velocity.X > 0f)
45438			{
45439				direction = 1;
45440			}
45441			ai[0] = num;
45442			ai[1] = num2;
45443			if (type == 356)
45444			{
45445				catchItem = (short)(1994f + ai[2] - 1f);

```


---

## 🤖 Assistant · 2026-08-11T04:53:11.147Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. Now the type 661 = Hallowed butterfly? Actually 661 is "Hell Butterfly"? Let me check names later. 356 is Monarch Butterfly; ai[2] is color variant 1..7 which maps to catch item 1994+variant-1.

Now let me read 112, 114, 115, 116, 118 methods: lines 47882 (116) to 48253, plus 47432-47488 (118), plus AI_112 48453 onwards. Let me read 47432-48253 in one read (820 lines) and then AI_112 (48453 to ~48700).
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:53:11.360Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 62,
 "offset": 47432
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:53:11.372Z

**📎 ToolResult**

```
47432		private void AI_118_Seahorses()
47433		{
47434			noGravity = wet;
47435			Collision.GetWaterLineIterate(base.Center.ToTileCoordinates(), out var waterLineHeight);
47436			bool flag = waterLineHeight > 0f && base.Top.Y - waterLineHeight < 20f;
47437			if (!wet)
47438			{
47439				if (velocity.Y == 0f)
47440				{
47441					velocity.X *= 0.95f;
47442				}
47443				rotation += (velocity.X + velocity.Y) / 2f * 0.05f;
47444			}
47445			else
47446			{
47447				ai[1] -= 1f;
47448				if (ai[1] <= 0f)
47449				{
47450					velocity += ai[0].ToRotationVector2() * 0.06f;
47451					float num = velocity.Length();
47452					if (num > 3f || num < -3f)
47453					{
47454						velocity.X = Math.Min(3f, Math.Max(-3f, velocity.X));
47455						ai[1] = Main.rand.Next(450, 600);
47456						ai[0] = Main.rand.NextFloat() * (MathF.PI * 2f);
47457						if (flag && ai[0] > MathF.PI)
47458						{
47459							ai[0] -= MathF.PI;
47460						}
47461						netUpdate = true;
47462					}
47463				}
47464				else
47465				{
47466					velocity *= 0.95f;
47467				}
47468				rotation = velocity.X * 0.1f;
47469			}
47470			bool flag2 = collideY && wet && (!flag || velocity.Y < 0f);
47471			if (collideX || flag2)
47472			{
47473				Vector2 v = ai[0].ToRotationVector2();
47474				if (collideX)
47475				{
47476					v.X *= -1f;
47477				}
47478				if (flag2)
47479				{
47480					v.Y *= -1f;
47481				}
47482				ai[0] = v.ToRotation();
47483				velocity = ai[0].ToRotationVector2() * velocity.Length();
47484				netUpdate = true;
47485			}
47486		}
47487	
47488		private void AI_117_BloodNautilus()
47489		{
47490			float moveSpeed = 0.15f;
47491			float num = 7.5f;
47492			float num2 = 60f;
47493			float num3 = 90f;

```


---

## 🤖 Assistant · 2026-08-11T04:53:11.640Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 371,
 "offset": 47882
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:53:11.646Z

**📎 ToolResult**

```
47882		private void AI_116_WaterStriders()
47883		{
47884			bool flag = false;
47885			if (Collision.GetWaterLine(base.Center.ToTileCoordinates(), out var waterLineHeight))
47886			{
47887				float num = base.Bottom.Y - 1f;
47888				if (base.Center.Y > waterLineHeight)
47889				{
47890					velocity.Y -= 0.8f;
47891					if (velocity.Y < -4f)
47892					{
47893						velocity.Y = -4f;
47894					}
47895					if (num + velocity.Y < waterLineHeight)
47896					{
47897						velocity.Y = waterLineHeight - num;
47898					}
47899				}
47900				else
47901				{
47902					velocity.Y = MathHelper.Min(velocity.Y, waterLineHeight - num);
47903					flag = true;
47904				}
47905			}
47906			else if (wet)
47907			{
47908				velocity.Y -= 0.2f;
47909			}
47910			if ((int)ai[0] != 0)
47911			{
47912				return;
47913			}
47914			ai[1] += 1f;
47915			velocity.X *= 0.9f;
47916			if (velocity.Y == 0f)
47917			{
47918				velocity.X *= 0.6f;
47919			}
47920			bool flag2 = wet || flag;
47921			bool flag3 = flag2 || velocity.Y == 0f;
47922			int num2 = Main.rand.Next(120, 241);
47923			if (!flag2)
47924			{
47925				num2 = Main.rand.Next(60, 241);
47926			}
47927			if (!flag3 || !(ai[1] >= (float)num2))
47928			{
47929				return;
47930			}
47931			ai[1] = 0f;
47932			velocity.X = Main.rand.NextFloatDirection() * 5f;
47933			netUpdate = true;
47934			if (!flag2)
47935			{
47936				if (velocity.Y == 0f)
47937				{
47938					velocity.Y = -2f;
47939				}
47940				ai[1] = 60f;
47941			}
47942		}
47943	
47944		private void AI_115_LadyBugs()
47945		{
47946			if (Main.netMode != 1)
47947			{
47948				if (ai[1] == 0f)
47949				{
47950					ai[1] = Main.rand.NextFloat() * 0.2f + 0.7f;
47951					netUpdate = true;
47952				}
47953				if ((localAI[0] -= 1f) <= 0f)
47954				{
47955					localAI[0] = Main.rand.Next(60, 181);
47956					if (Main.rand.Next(5) == 0)
47957					{
47958						if (ai[2] == 0f)
47959						{
47960							ai[2] = 1f;
47961							ai[0] = 0f;
47962							netUpdate = true;
47963						}
47964						else if (ai[2] == 1f)
47965						{
47966							TargetClosest();
47967							ai[2] = 0f;
47968							ai[0] = Main.rand.NextFloat() * (MathF.PI * 2f);
47969							if (Distance(Main.player[target].Center) > 700f)
47970							{
47971								ai[0] = AngleTo(Main.player[target].Center) + Main.rand.NextFloatDirection() * 0.3f;
47972							}
47973							netUpdate = true;
47974						}
47975					}
47976					TargetClosest();
47977					ai[0] = Main.rand.NextFloat() * (MathF.PI * 2f);
47978					if (Distance(Main.player[target].Center) > 700f)
47979					{
47980						ai[0] = AngleTo(Main.player[target].Center) + Main.rand.NextFloatDirection() * 0.3f;
47981					}
47982					netUpdate = true;
47983				}
47984			}
47985			scale = ai[1];
47986			if (ai[2] == 0f)
47987			{
47988				Vector2 value = ai[0].ToRotationVector2() * 1f;
47989				value.X += Main.windSpeedTarget * 0.8f;
47990				velocity = Vector2.Lerp(velocity, value, 0.0125f);
47991				if (velocity.Y > 0f)
47992				{
47993					int num = 4;
47994					int num2 = (int)base.Center.X / 16;
47995					int num3 = (int)base.Center.Y / 16;
47996					for (int i = num3; i < num3 + num; i++)
47997					{
47998						if (Main.tile[num2, i] != null && ((Main.tile[num2, i].nactive() && Main.tileSolid[Main.tile[num2, i].type]) || Main.tile[num2, i].liquid > 0))
47999						{
48000							ai[0] = 0f - ai[0];
48001							if (velocity.Y > 0f)
48002							{
48003								velocity.Y *= 0.9f;
48004							}
48005						}
48006					}
48007				}
48008				if (velocity.Y < 0f)
48009				{
48010					int num4 = 30;
48011					bool flag = false;
48012					int num5 = (int)base.Center.X / 16;
48013					int num6 = (int)base.Center.Y / 16;
48014					for (int j = num6; j < num6 + num4; j++)
48015					{
48016						if (Main.tile[num5, j] != null && ((Main.tile[num5, j].nactive() && Main.tileSolid[Main.tile[num5, j].type]) || Main.tile[num5, j].liquid > 0))
48017						{
48018							flag = true;
48019						}
48020					}
48021					if (!flag)
48022					{
48023						ai[0] = 0f - ai[0];
48024						if (velocity.Y < 0f)
48025						{
48026							velocity.Y *= 0.9f;
48027						}
48028					}
48029				}
48030				if (collideX)
48031				{
48032					ai[0] = 0f - ai[0] + MathF.PI;
48033					velocity.X *= -0.2f;
48034				}
48035			}
48036			else
48037			{
48038				if (velocity.Y > 0f)
48039				{
48040					int num7 = 4;
48041					int num8 = (int)base.Center.X / 16 + direction;
48042					int num9 = (int)base.Center.Y / 16;
48043					for (int k = num9; k < num9 + num7; k++)
48044					{
48045						if (Main.tile[num8, k] != null && Main.tile[num8, k].liquid > 0)
48046						{
48047							TargetClosest();
48048							velocity.Y = -1f;
48049							ai[2] = 0f;
48050							ai[0] = Main.rand.NextFloat() * (MathF.PI / 4f) - MathF.PI / 2f;
48051							if (Distance(Main.player[target].Center) > 700f)
48052							{
48053								ai[0] = AngleTo(Main.player[target].Center) + Main.rand.NextFloatDirection() * 0.3f;
48054							}
48055							netUpdate = true;
48056							return;
48057						}
48058					}
48059				}
48060				if (velocity.Y != 0f)
48061				{
48062					velocity.X *= 0.98f;
48063					velocity.Y = MathHelper.Lerp(velocity.Y, 2f, 0.005f);
48064				}
48065				else
48066				{
48067					velocity = Vector2.Lerp(velocity, Vector2.UnitX * direction, 0.05f);
48068					velocity.Y += 0.2f;
48069					if (collideX)
48070					{
48071						direction *= -1;
48072						velocity.X *= -0.2f;
48073						netUpdate = true;
48074					}
48075				}
48076			}
48077			direction = ((velocity.X > 0f) ? 1 : (-1));
48078		}
48079	
48080		private void AI_114_Dragonflies()
48081		{
48082			if (localAI[0] == 0f && Main.netMode != 1)
48083			{
48084				localAI[0] = 1f;
48085				Vector2 center = base.Center;
48086				ai[2] = center.X;
48087				ai[3] = center.Y;
48088				velocity = (Main.rand.NextVector2Circular(5f, 3f) + Main.rand.NextVector2CircularEdge(5f, 3f)) * 0.4f;
48089				ai[1] = 0f;
48090				ai[0] = 1f;
48091				netUpdate = true;
48092			}
48093			switch ((int)ai[0])
48094			{
48095			case 0:
48096				velocity *= 0.94f;
48097				if (Main.netMode != 1 && (ai[1] += 1f) >= (float)(60 + Main.rand.Next(60)))
48098				{
48099					Vector2 vector = new Vector2(ai[2], ai[3]);
48100					if (Distance(vector) > 96f)
48101					{
48102						velocity = DirectionTo(vector) * 3f;
48103					}
48104					else if (Distance(vector) > 16f)
48105					{
48106						velocity = DirectionTo(vector) * 1f + Main.rand.NextVector2Circular(1f, 0.5f);
48107					}
48108					else
48109					{
48110						velocity = (Main.rand.NextVector2Circular(5f, 3f) + Main.rand.NextVector2CircularEdge(5f, 3f)) * 0.4f;
48111					}
48112					ai[1] = 0f;
48113					ai[0] = 1f;
48114					netUpdate = true;
48115				}
48116				break;
48117			case 1:
48118			{
48119				int num = 4;
48120				Vector2 other = new Vector2(ai[2], ai[3]);
48121				if (Distance(other) > 112f)
48122				{
48123					num = 200;
48124				}
48125				if ((ai[1] += 1f) >= (float)num)
48126				{
48127					ai[1] = 0f;
48128					ai[0] = 0f;
48129					netUpdate = true;
48130				}
48131				int num2 = (int)base.Center.X / 16;
48132				int num3 = (int)base.Center.Y / 16;
48133				int num4 = 3;
48134				for (int i = num3; i < num3 + num4; i++)
48135				{
48136					if (Main.tile[num2, i] != null && ((Main.tile[num2, i].nactive() && Main.tileSolid[Main.tile[num2, i].type]) || Main.tile[num2, i].liquid > 0))
48137					{
48138						if (velocity.Y > 0f)
48139						{
48140							velocity.Y *= 0.9f;
48141						}
48142						velocity.Y -= 0.2f;
48143					}
48144				}
48145				if (!(velocity.Y < 0f))
48146				{
48147					break;
48148				}
48149				int num5 = 30;
48150				bool flag = false;
48151				for (int j = num3; j < num3 + num5; j++)
48152				{
48153					if (Main.tile[num2, j] != null && Main.tile[num2, j].nactive() && Main.tileSolid[Main.tile[num2, j].type])
48154					{
48155						flag = true;
48156						break;
48157					}
48158				}
48159				if (!flag && velocity.Y < 0f)
48160				{
48161					velocity.Y *= 0.9f;
48162				}
48163				break;
48164			}
48165			}
48166			if (velocity.X != 0f)
48167			{
48168				direction = ((velocity.X > 0f) ? 1 : (-1));
48169			}
48170			if (wet)
48171			{
48172				velocity.Y = -3f;
48173			}
48174			if (localAI[1] > 0f)
48175			{
48176				localAI[1] -= 1f;
48177				return;
48178			}
48179			localAI[1] = 15f;
48180			float num6 = 0f;
48181			Vector2 zero = Vector2.Zero;
48182			for (int k = 0; k < Main.maxNPCs; k++)
48183			{
48184				NPC nPC = Main.npc[k];
48185				if (nPC.active && nPC.damage > 0 && !nPC.friendly && nPC.Hitbox.Distance(base.Center) <= 100f)
48186				{
48187					num6 += 1f;
48188					zero += DirectionFrom(nPC.Center);
48189				}
48190			}
48191			for (int l = 0; l < 255; l++)
48192			{
48193				Player player = Main.player[l];
48194				if (player.active && player.Hitbox.Distance(base.Center) <= 150f)
48195				{
48196					num6 += 1f;
48197					zero += DirectionFrom(player.Center);
48198				}
48199			}
48200			if (num6 > 0f)
48201			{
48202				float num7 = 2f;
48203				zero /= num6;
48204				zero *= num7;
48205				velocity += zero;
48206				if (velocity.Length() > 16f)
48207				{
48208					velocity = velocity.SafeNormalize(Vector2.Zero) * 16f;
48209				}
48210				Vector2 vector2 = base.Center + zero * 10f;
48211				ai[1] = -10f;
48212				ai[0] = 1f;
48213				ai[2] = vector2.X;
48214				ai[3] = vector2.Y;
48215				netUpdate = true;
48216			}
48217			else
48218			{
48219				if (Main.netMode == 1 || !((new Vector2(ai[2], ai[3]) - base.Center).Length() < 16f))
48220				{
48221					return;
48222				}
48223				int maxValue = 30;
48224				if (Main.tile[(int)ai[2] / 16, (int)ai[3] / 16].type != 519)
48225				{
48226					maxValue = 4;
48227				}
48228				if (Main.rand.Next(maxValue) != 0)
48229				{
48230					return;
48231				}
48232				int cattailX = (int)ai[2];
48233				int cattailY = (int)ai[2];
48234				if (FindCattailTop((int)ai[2] / 16, (int)ai[3] / 16, out cattailX, out cattailY))
48235				{
48236					ai[2] = cattailX * 16;
48237					ai[3] = cattailY * 16;
48238					netUpdate = true;
48239					return;
48240				}
48241				int num8 = (int)(base.Center.X / 16f);
48242				int m;
48243				for (m = (int)(base.Center.Y / 16f); !WorldGen.SolidTile(num8, m) && (double)m < Main.worldSurface; m++)
48244				{
48245				}
48246				m -= Main.rand.Next(3, 6);
48247				ai[2] = num8 * 16;
48248				ai[3] = m * 16;
48249				netUpdate = true;
48250			}
48251		}
48252	

```


---

## 🤖 Assistant · 2026-08-11T04:53:14.160Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now AI_112_FairyCritter at 48453. Read until ~48650.

Also I need AI_001 (grasshopper) and AI_016 (fish). These are inline in the big AI method (aiStyle == 1 at ~?), not separate methods. Let me grep for "aiStyle == 1)" and "aiStyle == 16)". Actually the big dispatch: aiStyle 1 is inside the same giant method. Let me find lines.

Also NPCID names for 595-601 etc.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:53:14.353Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 200,
 "offset": 48453
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:53:14.365Z

**📎 ToolResult**

```
48453		private void AI_112_FairyCritter()
48454		{
48455			bool flag = false;
48456			lavaImmune = true;
48457			if (Main.netMode != 1 && ai[2] > 1f)
48458			{
48459				int num = 18000;
48460				localAI[1] += 1f;
48461				if (localAI[1] >= (float)num)
48462				{
48463					ai[2] = 7f;
48464					if (Main.player[target].Center.X < base.Center.X)
48465					{
48466						direction = 1;
48467					}
48468					else
48469					{
48470						direction = -1;
48471					}
48472					netUpdate = true;
48473				}
48474			}
48475			switch ((int)ai[2])
48476			{
48477			case 0:
48478			{
48479				lavaImmune = false;
48480				noTileCollide = false;
48481				if (ai[0] == 0f && ai[1] == 0f)
48482				{
48483					ai[0] = base.Center.X;
48484					ai[1] = base.Center.Y;
48485				}
48486				if (localAI[0] == 0f)
48487				{
48488					localAI[0] = 1f;
48489					velocity = new Vector2(MathHelper.Lerp(2f, 4f, Main.rand.NextFloat()) * (float)(Main.rand.Next(2) * 2 - 1), MathHelper.Lerp(1f, 2f, Main.rand.NextFloat()) * (float)(Main.rand.Next(2) * 2 - 1));
48490					velocity *= 0.7f;
48491					netUpdate = true;
48492				}
48493				Vector2 vector4 = new Vector2(ai[0], ai[1]) - base.Center;
48494				if (vector4.Length() > 20f)
48495				{
48496					Vector2 vector5 = new Vector2((vector4.X > 0f) ? 1 : (-1), (vector4.Y > 0f) ? 1 : (-1));
48497					velocity += vector5 * 0.04f;
48498					if (Math.Abs(velocity.Y) > 2f)
48499					{
48500						velocity.Y *= 0.95f;
48501					}
48502				}
48503				TargetClosest();
48504				Player player = Main.player[target];
48505				if (!player.dead && player.Distance(base.Center) < 250f)
48506				{
48507					ai[2] = 1f;
48508					direction = ((!(player.Center.X > base.Center.X)) ? 1 : (-1));
48509					if (velocity.X * (float)direction < 0f)
48510					{
48511						velocity.X = direction * 2;
48512					}
48513					ai[3] = 0f;
48514					netUpdate = true;
48515				}
48516				break;
48517			}
48518			case 1:
48519			{
48520				lavaImmune = false;
48521				noTileCollide = false;
48522				if (collideX)
48523				{
48524					direction *= -1;
48525					velocity.X = direction * 2;
48526				}
48527				if (collideY)
48528				{
48529					velocity.Y = ((oldVelocity.Y > 0f) ? 1 : (-1));
48530				}
48531				float num12 = 4.5f;
48532				if (Math.Sign(velocity.X) != direction || Math.Abs(velocity.X) < num12)
48533				{
48534					velocity.X += (float)direction * 0.04f;
48535					if (velocity.X * (float)direction < 0f)
48536					{
48537						if (Math.Abs(velocity.X) > num12)
48538						{
48539							velocity.X += (float)direction * 0.4f;
48540						}
48541						else
48542						{
48543							velocity.X += (float)direction * 0.2f;
48544						}
48545					}
48546					else if (Math.Abs(velocity.X) > num12)
48547					{
48548						velocity.X = (float)direction * num12;
48549					}
48550				}
48551				int num13 = (int)((position.X + (float)(width / 2)) / 16f);
48552				int num14 = 20;
48553				if (direction < 0)
48554				{
48555					num13 -= num14;
48556				}
48557				int num15 = (int)((position.Y + (float)height) / 16f);
48558				bool flag5 = true;
48559				int num16 = 8;
48560				bool flag6 = false;
48561				for (int i = num13; i <= num13 + num14; i++)
48562				{
48563					for (int j = num15; j < num15 + num16; j++)
48564					{
48565						if (Main.tile[i, j] == null)
48566						{
48567							Main.tile[i, j] = new Tile();
48568						}
48569						if ((Main.tile[i, j].nactive() && Main.tileSolid[Main.tile[i, j].type]) || Main.tile[i, j].liquid > 0)
48570						{
48571							if (j < num15 + 5)
48572							{
48573								flag6 = true;
48574							}
48575							flag5 = false;
48576							break;
48577						}
48578					}
48579				}
48580				if (flag5)
48581				{
48582					velocity.Y += 0.05f;
48583				}
48584				else
48585				{
48586					velocity.Y -= 0.2f;
48587				}
48588				if (flag6)
48589				{
48590					velocity.Y -= 0.3f;
48591				}
48592				if (velocity.Y > 3f)
48593				{
48594					velocity.Y = 3f;
48595				}
48596				if (velocity.Y < -5f)
48597				{
48598					velocity.Y = -5f;
48599				}
48600				break;
48601			}
48602			case 2:
48603			{
48604				noTileCollide = true;
48605				NPCAimedTarget targetData = GetTargetData();
48606				bool flag3 = false;
48607				if (targetData.Type == NPCTargetType.Player)
48608				{
48609					flag3 = Main.player[target].dead;
48610				}
48611				if (flag3)
48612				{
48613					ai[2] = 1f;
48614					direction = ((!(targetData.Center.X > base.Center.X)) ? 1 : (-1));
48615					if (velocity.X * (float)direction < 0f)
48616					{
48617						velocity.X = direction * 2;
48618					}
48619					ai[3] = 0f;
48620					netUpdate = true;
48621					break;
48622				}
48623				Rectangle r = Utils.CenteredRectangle(targetData.Center, new Vector2(targetData.Width + 60, targetData.Height / 2));
48624				if (Main.netMode != 1 && base.Hitbox.Intersects(r))
48625				{
48626					if (GetFairyTreasureCoords(out var treasureCoords2))
48627					{
48628						ai[0] = treasureCoords2.X;
48629						ai[1] = treasureCoords2.Y;
48630						ai[2] = 3f;
48631						ai[3] = 0f;
48632						netUpdate = true;
48633					}
48634					else
48635					{
48636						ai[2] = 6f;
48637						ai[3] = 0f;
48638						netUpdate = true;
48639					}
48640					break;
48641				}
48642				Vector2 vector3 = r.ClosestPointInRect(base.Center);
48643				Vector2 value = DirectionTo(vector3) * 2f;
48644				float num8 = Distance(vector3);
48645				if (num8 > 150f)
48646				{
48647					value *= 2f;
48648				}
48649				else if (num8 > 80f)
48650				{
48651					value *= 1.5f;
48652				}

```


---

## 🤖 Assistant · 2026-08-11T04:53:14.845Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"aiStyle == 1$\\|aiStyle == 1)\\|aiStyle == 16$\\|aiStyle == 16)\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head",
 "description": "Find aiStyle 1 and 16 block lines"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:53:19.498Z

**📎 ToolResult**

```
19894:		if (aiStyle == 1)
23549:		if (aiStyle == 16)

```


---

## 🤖 Assistant · 2026-08-11T04:53:23.535Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
AI_112 case 2 continues — fairy leads player to treasure. That's a long state machine (states 0-7). I have enough for the summary: fairy critter wanders (case 0), notices player within 250px (case 1 flies), leads player (case 2, noTileCollide), state 3 fly to treasure, etc., despawns after 18000 ticks (5 min) with ai[2]=7 (leave).

Let me read a bit more of AI_112 (48653-48830) to get the remaining states briefly, plus the fairy light emission. Then read aiStyle 1 (19894+) for grasshopper and aiStyle 16 (23549+).

Actually, to conserve calls, let me grep for key things in AI_112 remaining (light emission) and read it quickly with limited lines.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:53:23.733Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 180,
 "offset": 48653
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:53:23.744Z

**📎 ToolResult**

```
48653				velocity = Vector2.Lerp(velocity, value, 0.07f);
48654				Point point = base.Center.ToTileCoordinates();
48655				if (ai[3] < 300f)
48656				{
48657					GetBirdFlightRecommendation(6, 3, point, out var goDownwards, out var goUpwards);
48658					if (goDownwards)
48659					{
48660						velocity.Y += 0.05f;
48661					}
48662					if (goUpwards)
48663					{
48664						velocity.Y -= 0.02f;
48665					}
48666					if (velocity.Y > 2f)
48667					{
48668						velocity.Y = 2f;
48669					}
48670					if (velocity.Y < -4f)
48671					{
48672						velocity.Y = -4f;
48673					}
48674				}
48675				if (WorldGen.InWorld(point.X, point.Y))
48676				{
48677					if (WorldGen.SolidTile(point))
48678					{
48679						ai[3] = Math.Min(ai[3] + 2f, 400f);
48680					}
48681					else
48682					{
48683						ai[3] = Math.Max(ai[3] - 1f, 0f);
48684					}
48685				}
48686				break;
48687			}
48688			case 3:
48689				noTileCollide = true;
48690				if (ai[3] == 15f)
48691				{
48692					SoundEngine.PlaySound(27, (int)position.X, (int)position.Y);
48693				}
48694				if (ai[3] <= 15f)
48695				{
48696					velocity *= 0.9f;
48697				}
48698				else
48699				{
48700					if (Main.player[target].Center.X > base.Center.X)
48701					{
48702						spriteDirection = -1;
48703					}
48704					else
48705					{
48706						spriteDirection = 1;
48707					}
48708					flag = true;
48709					float num6 = 0f;
48710					float num7 = ai[3] - 15f;
48711					float circleHeight = 22f;
48712					if (num7 <= 65f)
48713					{
48714						num6 = MathF.PI / 8f;
48715						circleHeight = 14f;
48716					}
48717					else if (num7 <= 130f)
48718					{
48719						num6 = -MathF.PI / 8f;
48720						circleHeight = 18f;
48721					}
48722					num6 *= (float)direction;
48723					Vector2 fairyCircleOffset3 = GetFairyCircleOffset(num7 / 65f, num6, circleHeight);
48724					Vector2 fairyCircleOffset4 = GetFairyCircleOffset(num7 / 65f + 1f / 65f, num6, circleHeight);
48725					velocity = fairyCircleOffset4 - fairyCircleOffset3;
48726				}
48727				ai[3] += 1f;
48728				if (ai[3] >= 210f)
48729				{
48730					ai[2] = 4f;
48731					TargetClosest();
48732					ai[3] = 0f;
48733					netUpdate = true;
48734				}
48735				break;
48736			case 6:
48737			{
48738				noTileCollide = true;
48739				Vector2 vector = Main.player[target].Center - base.Center;
48740				if (vector.Length() > 100f)
48741				{
48742					ai[2] = 2f;
48743					TargetClosest();
48744					ai[3] = 0f;
48745					netUpdate = true;
48746					break;
48747				}
48748				if (!Collision.SolidCollision(position, width, height))
48749				{
48750					noTileCollide = false;
48751					if (collideX)
48752					{
48753						velocity.X *= -1f;
48754					}
48755					if (collideY)
48756					{
48757						velocity.Y *= -1f;
48758					}
48759				}
48760				if (vector.Length() > 20f)
48761				{
48762					Vector2 vector2 = new Vector2((vector.X > 0f) ? 1 : (-1), (vector.Y > 0f) ? 1 : (-1));
48763					velocity += vector2 * 0.04f;
48764					if (Math.Abs(velocity.Y) > 2f)
48765					{
48766						velocity.Y *= 0.95f;
48767					}
48768				}
48769				if (Main.netMode != 1 && GetFairyTreasureCoords(out var treasureCoords))
48770				{
48771					ai[0] = treasureCoords.X;
48772					ai[1] = treasureCoords.Y;
48773					ai[2] = 3f;
48774					ai[3] = 0f;
48775					netUpdate = true;
48776				}
48777				break;
48778			}
48779			case 4:
48780			{
48781				noTileCollide = true;
48782				NPCAimedTarget targetData2 = GetTargetData();
48783				bool flag4 = false;
48784				if (targetData2.Type == NPCTargetType.Player)
48785				{
48786					flag4 = Main.player[target].dead;
48787				}
48788				if (flag4)
48789				{
48790					ai[2] = 1f;
48791					direction = ((!(targetData2.Center.X > base.Center.X)) ? 1 : (-1));
48792					if (velocity.X * (float)direction < 0f)
48793					{
48794						velocity.X = direction * 2;
48795					}
48796					ai[3] = 0f;
48797					netUpdate = true;
48798					break;
48799				}
48800				Rectangle r2 = Utils.CenteredRectangle(new Vector2(ai[0] * 16f + 8f, ai[1] * 16f + 8f), Vector2.One * 5f);
48801				if (base.Hitbox.Intersects(r2))
48802				{
48803					ai[2] = 5f;
48804					ai[3] = 0f;
48805					netUpdate = true;
48806					break;
48807				}
48808				float num9 = Distance(targetData2.Center);
48809				float num10 = 300f;
48810				if (num9 > num10)
48811				{
48812					if (num9 < num10 + 100f && !Collision.SolidCollision(position, width, height))
48813					{
48814						noTileCollide = false;
48815						if (collideX)
48816						{
48817							velocity.X *= -1f;
48818						}
48819						if (collideY)
48820						{
48821							velocity.Y *= -1f;
48822						}
48823					}
48824					flag = true;
48825					if (Main.player[target].Center.X > base.Center.X)
48826					{
48827						spriteDirection = -1;
48828					}
48829					else
48830					{
48831						spriteDirection = 1;
48832					}

```


---

## 🤖 Assistant · 2026-08-11T04:53:25.812Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
OK, enough for fairy. Now aiStyle 1 at 19894 (grasshopper) and aiStyle 16 at 23549. Let me read relevant portions. aiStyle 1 block is from 19894 to ... probably 20769. That's huge (~900 lines) — includes slimes etc. Grasshopper: type 377 (Grasshopper), 446 (Gold Grasshopper). Search within for type 377.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:53:26.912Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '19894,20769p' NPC.cs > /tmp/ai1.txt; grep -n \"type == 377\\|type == 446\\|type == 446\\b\" /tmp/ai1.txt; echo ---16---; sed -n '23549,24674p' NPC.cs > /tmp/ai16.txt; grep -n \"type == 55\\b\\|type == 592\\|type == 607\\|type == 615\\|type == 688\" /tmp/ai16.txt",
 "description": "Find grasshopper branches in AI_001 and fish in AI_016"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:53:37.623Z

**📎 ToolResult**

```
sed: NPC.cs: No such file or directory
---16---
sed: NPC.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-11T04:53:39.913Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '19894,20769p' NPC.cs > /tmp/ai1.txt && sed -n '23549,24674p' NPC.cs > /tmp/ai16.txt && grep -n \"type == 377\\|type == 446\" /tmp/ai1.txt; echo ---16---; grep -n \"type == 55 \\|type == 55)\\|(type == 55\\b\" /tmp/ai16.txt | head; grep -n \"592\\|607\\|615\\|688\" /tmp/ai16.txt | head -20",
 "description": "Extract AI_001 and AI_016, grep critter types"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:53:50.223Z

**📎 ToolResult**

```
---16---
7:			if (type == 688)
81:			if (type == 615)
210:				if (type != 55 && type != 592 && type != 607 && type != 615 && type != 688)
416:						if (type == 615)

```


---

## 🤖 Assistant · 2026-08-11T04:53:54.779Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
type == 377 not found in AI_001? Grasshopper aiStyle... Let me check. In 1.4.4+, grasshopper might use aiStyle 1 but handled via a separate path. Let me grep NPCID for Grasshopper aiStyle. Actually maybe AI_001 is not the block 19894; maybe aiStyle 1 block ends earlier. Wait — the dispatch: `if (aiStyle == 1)` at 19894. The block ends at `else if (aiStyle == 2)`? Let me check where. Also grasshopper in 1.4.5 might have been moved to AI_007? Actually no — grasshopper is aiStyle 1 in older versions... Hmm, in 1.4.4 Grasshopper still aiStyle 1? Let me check the npc json or NPCID.Sets.

Let me grep for "Grasshopper" in NPCID.cs and check aiStyle in the project's npc data.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:53:55.098Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456 && grep -n \"Grasshopper\\|GoldGrasshopper\" Terraria.ID/NPCID.cs | head; echo ---; grep -n \"aiStyle == 2)\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -3; echo ---; head -60 /tmp/ai1.txt",
 "description": "Check grasshopper NPCID and AI_001 block extent"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:54:09.869Z

**📎 ToolResult**

```
10790:		{ "Grasshopper", 377 },
10842:		{ "Gold Grasshopper", 446 },
11819:	public const short Grasshopper = 377;
11953:	public const short GoldGrasshopper = 446;
---
19899:		if (aiStyle == 2)
---
		if (aiStyle == 1)
		{
			AI_001_Slimes();
			return;
		}
		if (aiStyle == 2)
		{
			AI_002_FloatingEye();
			return;
		}
		if (aiStyle == 3)
		{
			AI_003_Fighters();
			return;
		}
		if (aiStyle == 4)
		{
			bool flag2 = false;
			if (Main.expertMode && (double)life < (double)lifeMax * 0.12)
			{
				flag2 = true;
			}
			bool flag3 = false;
			if (Main.expertMode && (double)life < (double)lifeMax * 0.04)
			{
				flag3 = true;
			}
			float num4 = 20f;
			if (flag3)
			{
				num4 = 10f;
			}
			if (target < 0 || target == 255 || Main.player[target].dead || !Main.player[target].active)
			{
				TargetClosest();
			}
			bool dead = Main.player[target].dead;
			float num5 = position.X + (float)(width / 2) - Main.player[target].position.X - (float)(Main.player[target].width / 2);
			float num6 = position.Y + (float)height - 59f - Main.player[target].position.Y - (float)(Main.player[target].height / 2);
			float num7 = (float)Math.Atan2(num6, num5) + 1.57f;
			if (num7 < 0f)
			{
				num7 += 6.283f;
			}
			else if ((double)num7 > 6.283)
			{
				num7 -= 6.283f;
			}
			float num8 = 0f;
			if (this.ai[0] == 0f && this.ai[1] == 0f)
			{
				num8 = 0.02f;
			}
			if (this.ai[0] == 0f && this.ai[1] == 2f && this.ai[2] > 40f)
			{
				num8 = 0.05f;
			}
			if (this.ai[0] == 3f && this.ai[1] == 0f)
			{
				num8 = 0.05f;

```


---

## 🤖 Assistant · 2026-08-11T04:54:12.282Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
aiStyle 1 = AI_001_Slimes(). Grasshopper is aiStyle 1 — it goes through AI_001_Slimes with special handling. Let me find AI_001_Slimes method and grep type 377.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:54:13.145Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"private void AI_001_Slimes()\" NPC.cs && awk '/private void AI_001_Slimes\\(\\)/{f=1} f{print NR\": \"$0}' NPC.cs | grep -n \"type == 377\\|type == 446\" | head",
 "description": "Locate AI_001_Slimes and grasshopper branches"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:54:16.037Z

**📎 ToolResult**

```
60735:	private void AI_001_Slimes()
745:61479: 		if ((type == 377 || type == 446) && target != 255 && !Main.player[target].dead && Vector2.Distance(base.Center, Main.player[target].Center) <= 200f && !wet)
1120:61854: 		if (type == 377 || type == 446)
1268:62002: 			if (type == 377 || type == 446)
1364:62098: 				if (type == 377 || type == 446)
25384:86118: 		if (type == 377 && life <= 0)

```


---

## 🤖 Assistant · 2026-08-11T04:54:17.499Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '61440,61560p' NPC.cs",
 "description": "Read grasshopper flee branch in AI_001_Slimes"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:54:17.539Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
sed: NPC.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-11T04:54:18.873Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '61440,61560p' NPC.cs",
 "description": "Read grasshopper flee branch in AI_001_Slimes"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:54:18.914Z

**📎 ToolResult**

```
		}
		if (ai[0] == -999f)
		{
			frame.Y = 0;
			frameCounter = 0.0;
			rotation = 0f;
			return;
		}
		if (type == 244)
		{
			float num24 = (float)Main.DiscoR / 255f;
			float num25 = (float)Main.DiscoG / 255f;
			float num26 = (float)Main.DiscoB / 255f;
			num24 *= 1f;
			num25 *= 1f;
			num26 *= 1f;
			Lighting.AddLight((int)((position.X + (float)(width / 2)) / 16f), (int)((position.Y + (float)(height / 2)) / 16f), num24, num25, num26);
			AI_001_SetRainbowSlimeColor();
		}
		bool flag3 = false;
		if (!Main.dayTime || life != lifeMax || (double)position.Y > Main.worldSurface * 16.0 || Main.slimeRain)
		{
			flag3 = true;
		}
		if (Main.remixWorld && type == 59 && life == lifeMax)
		{
			flag3 = false;
		}
		if (type == 81)
		{
			flag3 = true;
			if (Main.rand.Next(30) == 0)
			{
				position += netOffset;
				int num27 = Dust.NewDust(position, width, height, 14, 0f, 0f, alpha, this.color);
				Main.dust[num27].velocity *= 0.3f;
				position -= netOffset;
			}
		}
		if ((type == 377 || type == 446) && target != 255 && !Main.player[target].dead && Vector2.Distance(base.Center, Main.player[target].Center) <= 200f && !wet)
		{
			flag3 = true;
		}
		if (type == 183)
		{
			flag3 = true;
		}
		if (type == 304)
		{
			flag3 = true;
		}
		if (type == 667)
		{
			flag3 = true;
		}
		if (type == 244)
		{
			flag3 = true;
			ai[0] += 2f;
		}
		if (type == 147 && Main.rand.Next(10) == 0)
		{
			position += netOffset;
			int num28 = Dust.NewDust(position, width, height, 76);
			Main.dust[num28].noGravity = true;
			Main.dust[num28].velocity *= 0.1f;
			position -= netOffset;
		}
		if (type == 667)
		{
			Color color2 = new Color(204, 181, 72, 255);
			Lighting.AddLight((int)(base.Center.X / 16f), (int)(base.Center.Y / 16f), (float)(int)color2.R / 255f * 1.1f, (float)(int)color2.G / 255f * 1.1f, (float)(int)color2.B / 255f * 1.1f);
			if (velocity.Length() > 1f || Main.rand.Next(4) != 0)
			{
				int num29 = 8;
				Vector2 vector2 = position + new Vector2(-num29, -num29);
				int num30 = width + num29 * 2;
				int num31 = height + num29 * 2;
				position += netOffset;
				int num32 = Dust.NewDust(vector2, num30, num31, 246);
				Main.dust[num32].noGravity = true;
				Main.dust[num32].noLightEmittance = true;
				Main.dust[num32].velocity *= 0.2f;
				Main.dust[num32].scale = 1.5f;
				position -= netOffset;
			}
		}
		if (type == 676)
		{
			Lighting.AddLight(base.Center, 23);
			if ((velocity.Length() > 1f && Main.rand.Next(3) == 0) || Main.rand.Next(5) == 0)
			{
				Dust dust4 = Dust.NewDustPerfect(Main.rand.NextVector2FromRectangle(base.Hitbox), 306);
				dust4.noGravity = true;
				dust4.noLightEmittance = true;
				dust4.alpha = 127;
				dust4.color = Main.hslToRgb(((float)Main.timeForVisualEffects / 300f + Main.rand.NextFloat() * 0.1f) % 1f, 1f, 0.65f);
				dust4.color.A = 0;
				dust4.velocity = dust4.position - base.Center;
				dust4.velocity *= 0.1f;
				dust4.velocity.X *= 0.25f;
				if (dust4.velocity.Y > 0f)
				{
					dust4.velocity.Y *= -1f;
				}
				dust4.scale = Main.rand.NextFloat() * 0.3f + 0.5f;
				dust4.fadeIn = 0.9f;
				dust4.position += netOffset;
			}
		}
		if (type == 184)
		{
			if (Main.rand.Next(8) == 0)
			{
				position += netOffset;
				int num33 = Dust.NewDust(position - velocity, width, height, 76);
				Main.dust[num33].noGravity = true;
				Main.dust[num33].velocity *= 0.15f;
				position -= netOffset;
			}
			flag3 = true;

```


---

## 🤖 Assistant · 2026-08-11T04:54:20.859Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
flag3 = "always jump" flag for slimes. For grasshopper: flag3=true when player within 200px and not wet. Then the jump logic around 61854-62100. Let me read those parts.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:54:21.315Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '61830,61900p' NPC.cs; echo =====; sed -n '61985,62140p' NPC.cs",
 "description": "Read grasshopper jump logic in AI_001_Slimes"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:54:21.345Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
sed: NPC.cs: No such file or directory
(eval):1: ==== not found

```


---

## 🤖 Assistant · 2026-08-11T04:54:23.978Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '61830,61900p' NPC.cs",
 "description": "Read AI_001_Slimes lines 61830-61900"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:54:24.008Z

**📎 ToolResult**

```
					}
				}
				if (num51 < 400f && Collision.CanHit(new Vector2(position.X, position.Y - 20f), width, height + 20, Main.player[target].position, Main.player[target].width, Main.player[target].height) && velocity.Y == 0f)
				{
					ai[0] = -80f;
					if (velocity.Y == 0f)
					{
						velocity.X *= 0.9f;
					}
					if (Main.netMode != 1 && localAI[0] == 0f)
					{
						num50 = Main.player[target].position.Y - vector8.Y - (float)Main.rand.Next(-30, 20);
						num50 -= num51 * 0.05f;
						num49 = Main.player[target].position.X - vector8.X - (float)Main.rand.Next(-20, 20);
						num51 = (float)Math.Sqrt(num49 * num49 + num50 * num50);
						num51 = 7f / num51;
						num49 *= num51;
						num50 *= num51;
						localAI[0] = 65f;
						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector8.X, vector8.Y, num49, num50, 176, 13, 0f, Main.myPlayer);
					}
				}
			}
		}
		if (type == 377 || type == 446)
		{
			if (localAI[2] < 90f)
			{
				localAI[2] += 1f;
			}
			else
			{
				friendly = false;
			}
		}
		if (type == 59)
		{
			position += netOffset;
			Lighting.AddLight((int)((position.X + (float)(width / 2)) / 16f), (int)((position.Y + (float)(height / 2)) / 16f), 1f, 0.3f, 0.1f);
			int num52 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 6, velocity.X * 0.2f, velocity.Y * 0.2f, 100, default(Color), 1.7f);
			Main.dust[num52].noGravity = true;
			position -= netOffset;
		}
		if (ai[2] > 1f)
		{
			ai[2] -= 1f;
		}
		if (wet)
		{
			if (collideY)
			{
				velocity.Y = -2f;
			}
			if (velocity.Y < 0f && ai[3] == position.X)
			{
				direction *= -1;
				ai[2] = 200f;
			}
			if (velocity.Y > 0f)
			{
				ai[3] = position.X;
			}
			if (type == 59 && !Main.remixWorld)
			{
				if (velocity.Y > 2f)
				{
					velocity.Y *= 0.9f;
				}
				else if (directionY < 0)
				{
					velocity.Y -= 0.8f;

```


---

## 🤖 Assistant · 2026-08-11T04:54:26.371Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '62055,62220p' NPC.cs",
 "description": "Read AI_001_Slimes jump state machine"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:54:26.395Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
sed: NPC.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-11T04:54:27.949Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Annoying — cwd resets. Use absolute path.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:54:28.089Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '62055,62220p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_001_Slimes jump state machine"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:54:28.121Z

**📎 ToolResult**

```
					{
						velocity.X += 0.5f * (float)direction;
					}
					ai[0] = -200f;
					ai[3] = position.X;
				}
				else
				{
					velocity.Y = -6f;
					velocity.X += 2 * direction;
					if (type == 59 && !Main.remixWorld)
					{
						velocity.X += 2 * direction;
					}
					ai[0] = -120f;
					if (num55 == 1)
					{
						ai[0] += num54;
					}
					else
					{
						ai[0] += num54 * 2f;
					}
				}
				if (type == 659)
				{
					velocity.Y *= 1.6f;
					velocity.X *= 1.2f;
				}
				if (type == 685)
				{
					velocity.Y *= 0.5f;
					velocity.X *= 0.2f;
					if (Main.rand.Next(2) == 0)
					{
						direction *= -1;
					}
				}
				if (type == 141)
				{
					velocity.Y *= 1.3f;
					velocity.X *= 1.2f;
				}
				if (type == 377 || type == 446)
				{
					velocity.Y *= 0.9f;
					velocity.X *= 0.6f;
					if (flag3)
					{
						direction = -direction;
						velocity.X *= -1f;
					}
					int i2 = (int)(base.Center.X / 16f);
					int j2 = (int)(base.Center.Y / 16f) - 1;
					if (WorldGen.SolidTile(i2, j2) && 0f - velocity.Y + (float)height > 16f)
					{
						velocity.Y = -(16 - height);
					}
				}
			}
			else if (ai[0] >= -30f)
			{
				aiAction = 1;
			}
		}
		else if (target < 255 && ((direction == 1 && velocity.X < 3f) || (direction == -1 && velocity.X > -3f)))
		{
			if (collideX && Math.Abs(velocity.X) == 0.2f)
			{
				position.X -= 1.4f * (float)direction;
			}
			if (collideY && oldVelocity.Y != 0f && Collision.SolidCollision(position, width, height))
			{
				position.X -= velocity.X + (float)direction;
			}
			if ((direction == -1 && (double)velocity.X < 0.01) || (direction == 1 && (double)velocity.X > -0.01))
			{
				velocity.X += 0.2f * (float)direction;
			}
			else
			{
				velocity.X *= 0.93f;
			}
		}
	}

	public void AI_001_SetRainbowSlimeColor()
	{
		color.R = (byte)Main.DiscoR;
		color.G = (byte)Main.DiscoG;
		color.B = (byte)Main.DiscoB;
		color.A = 100;
		alpha = 175;
	}

	private int AI_001_Slimes_GenerateItemInsideBody(bool isBallooned)
	{
		int num = Main.rand.Next(4);
		bool flag = isBallooned;
		if (WorldGen.Skyblock.lowTiles)
		{
			if (Main.rand.Next(3) != 0)
			{
				num = Main.rand.Next(1, 3);
			}
			if (Main.rand.Next(3) != 0)
			{
				flag = false;
			}
		}
		if (flag)
		{
			switch (Main.rand.Next(13))
			{
			default:
				return 4367;
			case 1:
				return 4368;
			case 2:
				return 4369;
			case 3:
				return 4370;
			case 4:
				return 4371;
			case 5:
				return 4612;
			case 6:
				return 4674;
			case 7:
			case 8:
			case 9:
				return 4343;
			case 10:
			case 11:
			case 12:
				return 4344;
			}
		}
		switch (num)
		{
		case 0:
			switch (Main.rand.Next(7))
			{
			case 0:
				return 290;
			case 1:
				return 292;
			case 2:
				return 296;
			case 3:
				return 2322;
			default:
				if (Main.netMode != 0 && Main.rand.Next(2) == 0)
				{
					return 2997;
				}
				return 2350;
			}
		case 1:
			num = Main.rand.Next(4);
			if (WorldGen.Skyblock.lowTiles)
			{
				if (Main.moonPhase == 0)
				{
					num = Main.rand.Next(2);
				}

```


---

## 🤖 Assistant · 2026-08-11T04:54:29.996Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Need to see the part just above 62055 — the jump trigger (ai[0] <= 0 and velocity.Y == 0). Let me read 61990-62060.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:54:30.359Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '61990,62060p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read jump trigger in AI_001_Slimes"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:54:30.389Z

**📎 ToolResult**

```
			{
				ai[0] += 5f;
			}
			if (type == 659)
			{
				ai[0] += 3f;
			}
			if (type == 304)
			{
				float num53 = (1 - life / lifeMax) * 10;
				ai[0] += num53;
			}
			if (type == 377 || type == 446)
			{
				ai[0] += 3f;
			}
			if (type == 81)
			{
				if (scale >= 0f)
				{
					ai[0] += 4f;
				}
				else
				{
					ai[0] += 1f;
				}
			}
			float num54 = -1000f;
			if (type == 659)
			{
				num54 = -500f;
			}
			if (type == 667)
			{
				num54 = -400f;
			}
			int num55 = 0;
			if (ai[0] >= 0f)
			{
				num55 = 1;
			}
			if (ai[0] >= num54 && ai[0] <= num54 * 0.5f)
			{
				num55 = 2;
			}
			if (ai[0] >= num54 * 2f && ai[0] <= num54 * 1.5f)
			{
				num55 = 3;
			}
			if (num55 > 0)
			{
				netUpdate = true;
				if (flag3 && ai[2] == 1f)
				{
					TargetClosest();
				}
				if (num55 == 3)
				{
					velocity.Y = -8f;
					if (type == 59 && !Main.remixWorld)
					{
						velocity.Y -= 2f;
					}
					velocity.X += 3 * direction;
					if (type == 59 && !Main.remixWorld)
					{
						velocity.X += 0.5f * (float)direction;
					}
					ai[0] = -200f;
					ai[3] = position.X;
				}

```


---

## 🤖 Assistant · 2026-08-11T04:54:33.825Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now AI_016 fish. Let me read the relevant chunk of /tmp/ai16.txt (which I created with absolute path — check it exists). It was created in an earlier call with absolute path: `sed -n '23549,24674p' NPC.cs > /tmp/ai16.txt` — that was the one that failed? No, the failed one was `sed -n '19894,20769p' NPC.cs > /tmp/ai1.txt` in the cd-less call. The successful one had `cd ... &&`. Wait, second attempt: `cd /Users/.../Terraria && sed -n '19894,20769p' NPC.cs > /tmp/ai1.txt && sed -n '23549,24674p' NPC.cs > /tmp/ai16.txt` — succeeded. Good, both files exist.

grep results in ai16: line 7 type==688, 81 type==615, 210 "type != 55 && type != 592 && type != 607 && type != 615 && type != 688", 416 type==615. Let me view those regions.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:54:34.191Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1,60p' /tmp/ai16.txt; echo =====; sed -n '70,120p' /tmp/ai16.txt",
 "description": "Read start of AI_016 fish block"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:54:39.107Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
		if (aiStyle == 16)
		{
			if (direction == 0)
			{
				TargetClosest();
			}
			if (type == 688)
			{
				if (Main.netMode != 1)
				{
					if (justHit && this.ai[2] == 0f)
					{
						this.ai[2] = 1f;
						localAI[0] = 180f;
						netUpdate = true;
					}
					else
					{
						localAI[0]--;
						if (localAI[0] <= 0f)
						{
							localAI[0] = 120f;
							if (this.ai[2] == 1f)
							{
								this.ai[2] = 0f;
							}
							if (justHit)
							{
								this.ai[2] = 1f;
							}
							netUpdate = true;
						}
					}
				}
				if (this.ai[2] == 1f)
				{
					velocity *= 0.98f;
					if (Collision.GetWaterLine(base.Top.ToTileCoordinates(), out var waterLineHeight))
					{
						float num263 = base.Top.Y - 5f;
						if (base.Center.Y > waterLineHeight)
						{
							velocity.Y -= 0.4f;
							if (velocity.Y < -2f)
							{
								velocity.Y = -2f;
							}
							if (num263 + velocity.Y < waterLineHeight)
							{
								velocity.Y = waterLineHeight - num263;
							}
						}
						else
						{
							velocity.Y = MathHelper.Min(velocity.Y, waterLineHeight - num263);
							if (Math.Abs(num263 - waterLineHeight) < 2f)
							{
								velocity.Y = 0f;
							}
						}
(eval):1: ==== not found

```


---

## 🤖 Assistant · 2026-08-11T04:54:40.476Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '60,130p' /tmp/ai16.txt",
 "description": "Continue AI_016 pufferfish/dolphin part"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:54:47.145Z

**📎 ToolResult**

```
						}
					}
					else if (wet)
					{
						velocity.Y -= 0.3f;
						if (velocity.Y < -10f)
						{
							velocity.Y = -10f;
						}
					}
					else
					{
						velocity.Y += 0.3f;
						if (velocity.Y > 10f)
						{
							velocity.Y = 10f;
						}
					}
					return;
				}
			}
			if (type == 615)
			{
				if (this.ai[2] == 0f)
				{
					int num264 = Main.rand.Next(300, 1200);
					if ((this.ai[3] += 1f) >= (float)num264)
					{
						this.ai[2] = Main.rand.Next(1, 3);
						if (this.ai[2] == 1f && !Collision.CanHitLine(position, width, height, new Vector2(position.X, position.Y - 128f), width, height))
						{
							this.ai[2] = 2f;
						}
						if (this.ai[2] == 2f)
						{
							TargetClosest();
						}
						this.ai[3] = 0f;
						netUpdate = true;
					}
				}
				if (this.ai[2] == 1f)
				{
					if (collideY || collideX)
					{
						this.ai[2] = 0f;
						this.ai[3] = 0f;
						netUpdate = true;
					}
					else if (wet)
					{
						velocity.Y -= 0.4f;
						if (velocity.Y < -6f)
						{
							velocity.Y = -6f;
						}
						rotation = velocity.Y * (float)direction * 0.3f;
						if (rotation < MathF.PI * -2f / 5f)
						{
							rotation = MathF.PI * -2f / 5f;
						}
						if (rotation > MathF.PI * 2f / 5f)
						{
							rotation = MathF.PI * 2f / 5f;
						}
						if (this.ai[3] == 1f)
						{
							this.ai[2] = 0f;
							this.ai[3] = 0f;
							netUpdate = true;
						}

```


---

## 🤖 Assistant · 2026-08-11T04:54:49.912Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '130,240p' /tmp/ai16.txt; echo END; sed -n '400,470p' /tmp/ai16.txt",
 "description": "Read dolphin jump and generic fish swim part"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:54:53.159Z

**📎 ToolResult**

```
						}
					}
					else
					{
						rotation += (float)direction * 0.2f;
						this.ai[3] = 1f;
						velocity.Y += 0.3f;
						if (velocity.Y > 10f)
						{
							velocity.Y = 10f;
						}
					}
					return;
				}
				if (this.ai[2] == 2f)
				{
					if (collideY || collideX)
					{
						this.ai[2] = 0f;
						this.ai[3] = 0f;
						netUpdate = true;
					}
					else if (wet)
					{
						velocity.Y -= 0.4f;
						if (velocity.Y < -6f)
						{
							velocity.Y = -6f;
						}
						rotation = velocity.Y * (float)direction * 0.3f;
						if (rotation < MathF.PI * -2f / 5f)
						{
							rotation = MathF.PI * -2f / 5f;
						}
						if (rotation > MathF.PI * 2f / 5f)
						{
							rotation = MathF.PI * 2f / 5f;
						}
						if (Collision.GetWaterLine(base.Top.ToTileCoordinates(), out var waterLineHeight2))
						{
							float y = waterLineHeight2 + 0f - position.Y;
							velocity.Y = y;
							velocity.Y = MathHelper.Clamp(velocity.Y, -2f, 0.5f);
							rotation = -MathF.PI / 5f * (float)direction;
							velocity.X *= 0.95f;
							if (this.ai[3] == 0f)
							{
								netUpdate = true;
							}
							this.ai[3]++;
							if (this.ai[3] >= 300f)
							{
								this.ai[2] = 0f;
								this.ai[3] = 0f;
								netUpdate = true;
								velocity.Y = 4f;
							}
							if (this.ai[3] == 60f && Main.rand.Next(2) == 0)
							{
								SoundEngine.PlaySound(45, (int)position.X, (int)position.Y);
							}
						}
					}
					else
					{
						this.ai[2] = 0f;
						this.ai[3] = 0f;
						netUpdate = true;
						velocity.Y += 0.3f;
						if (velocity.Y > 10f)
						{
							velocity.Y = 10f;
						}
					}
					return;
				}
			}
			if (wet)
			{
				bool flag22 = false;
				if (type != 55 && type != 592 && type != 607 && type != 615 && type != 688)
				{
					TargetClosest(faceTarget: false);
					if (Main.player[target].wet && !Main.player[target].dead && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
					{
						flag22 = true;
					}
				}
				int num265 = (int)base.Center.X / 16;
				int num266 = (int)(position.Y + (float)height) / 16;
				if (Main.tile[num265, num266].topSlope())
				{
					if (Main.tile[num265, num266].leftSlope())
					{
						direction = -1;
						velocity.X = Math.Abs(velocity.X) * -1f;
					}
					else
					{
						direction = 1;
						velocity.X = Math.Abs(velocity.X);
					}
				}
				else if (Main.tile[num265, num266 + 1].topSlope())
				{
					if (Main.tile[num265, num266 + 1].leftSlope())
					{
						direction = -1;
						velocity.X = Math.Abs(velocity.X) * -1f;
					}
					else
END
							}
							if (directionY > 0)
							{
								num268 = 1f;
							}
							velocity.Y += 0.02f;
							if (velocity.Y > num268)
							{
								this.ai[0] = -1f;
							}
						}
					}
					else
					{
						velocity.X += (float)direction * 0.1f;
						float num269 = 1f;
						if (type == 615)
						{
							num269 = 3f;
						}
						if (velocity.X < 0f - num269 || velocity.X > num269)
						{
							velocity.X *= 0.95f;
						}
						if (this.ai[0] == -1f)
						{
							velocity.Y -= 0.01f;
							if (velocity.Y < -0.3f)
							{
								this.ai[0] = 1f;
							}
						}
						else
						{
							velocity.Y += 0.01f;
							if (velocity.Y > 0.3f)
							{
								this.ai[0] = -1f;
							}
						}
					}
					int num270 = (int)(position.X + (float)(width / 2)) / 16;
					int num271 = (int)(position.Y + (float)(height / 2)) / 16;
					if (Main.tile[num270, num271 - 1] == null)
					{
						Main.tile[num270, num271 - 1] = new Tile();
					}
					if (Main.tile[num270, num271 + 1] == null)
					{
						Main.tile[num270, num271 + 1] = new Tile();
					}
					if (Main.tile[num270, num271 + 2] == null)
					{
						Main.tile[num270, num271 + 2] = new Tile();
					}
					if (Main.tile[num270, num271 - 1].liquid > 128)
					{
						if (Main.tile[num270, num271 + 1].active())
						{
							this.ai[0] = -1f;
						}
						else if (Main.tile[num270, num271 + 2].active())
						{
							this.ai[0] = -1f;
						}
					}
					if (type != 157 && (velocity.Y > 0.4f || velocity.Y < -0.4f))
					{
						velocity.Y *= 0.95f;
					}
				}

```


---

## 🤖 Assistant · 2026-08-11T04:54:54.839Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now the non-wet (out of water) part for goldfish etc. Let me grep for "justHit" / "out of water" flap in ai16. Let me look at lines 240-400.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:54:55.148Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '240,400p' /tmp/ai16.txt",
 "description": "Read AI_016 water/out-of-water movement"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:55:05.215Z

**📎 ToolResult**

```
					else
					{
						direction = 1;
						velocity.X = Math.Abs(velocity.X);
					}
				}
				if (!flag22)
				{
					if (collideX)
					{
						velocity.X *= -1f;
						direction *= -1;
						netUpdate = true;
					}
					if (collideY)
					{
						netUpdate = true;
						if (velocity.Y > 0f)
						{
							velocity.Y = Math.Abs(velocity.Y) * -1f;
							directionY = -1;
							this.ai[0] = -1f;
						}
						else if (velocity.Y < 0f)
						{
							velocity.Y = Math.Abs(velocity.Y);
							directionY = 1;
							this.ai[0] = 1f;
						}
					}
				}
				if (type == 102)
				{
					Lighting.AddLight((int)(position.X + (float)(width / 2) + (float)(direction * (width + 8))) / 16, (int)(position.Y + 2f) / 16, 0.07f, 0.04f, 0.025f);
				}
				if (flag22)
				{
					if (this.ai[0] != 0f)
					{
						this.ai[0] = 0f;
						netUpdate = true;
					}
					TargetClosest();
					if (type == 157)
					{
						if (velocity.X > 0f && direction < 0)
						{
							velocity.X *= 0.95f;
						}
						if (velocity.X < 0f && direction > 0)
						{
							velocity.X *= 0.95f;
						}
						velocity.X += (float)direction * 0.25f;
						velocity.Y += (float)directionY * 0.2f;
						if (velocity.X > 8f)
						{
							velocity.X = 7f;
						}
						if (velocity.X < -8f)
						{
							velocity.X = -7f;
						}
						if (velocity.Y > 5f)
						{
							velocity.Y = 4f;
						}
						if (velocity.Y < -5f)
						{
							velocity.Y = -4f;
						}
					}
					else if (type == 65 || type == 102 || type == 692)
					{
						velocity.X += (float)direction * 0.15f;
						velocity.Y += (float)directionY * 0.15f;
						if (velocity.X > 5f)
						{
							velocity.X = 5f;
						}
						if (velocity.X < -5f)
						{
							velocity.X = -5f;
						}
						if (velocity.Y > 3f)
						{
							velocity.Y = 3f;
						}
						if (velocity.Y < -3f)
						{
							velocity.Y = -3f;
						}
					}
					else
					{
						velocity.X += (float)direction * 0.1f;
						velocity.Y += (float)directionY * 0.1f;
						if (velocity.X > 3f)
						{
							velocity.X = 3f;
						}
						if (velocity.X < -3f)
						{
							velocity.X = -3f;
						}
						if (velocity.Y > 2f)
						{
							velocity.Y = 2f;
						}
						if (velocity.Y < -2f)
						{
							velocity.Y = -2f;
						}
					}
				}
				else
				{
					if (this.ai[0] == 0f)
					{
						this.ai[0] = 1f;
						netUpdate = true;
					}
					if (type == 157)
					{
						if (Main.player[target].position.Y > position.Y)
						{
							directionY = 1;
						}
						else
						{
							directionY = -1;
						}
						velocity.X += (float)direction * 0.2f;
						if (velocity.X < -2f || velocity.X > 2f)
						{
							velocity.X *= 0.95f;
						}
						if (this.ai[0] == -1f)
						{
							float num267 = -0.6f;
							if (directionY < 0)
							{
								num267 = -1f;
							}
							if (directionY > 0)
							{
								num267 = -0.2f;
							}
							velocity.Y -= 0.02f;
							if (velocity.Y < num267)
							{
								this.ai[0] = 1f;
							}
						}
						else
						{
							float num268 = 0.6f;
							if (directionY < 0)
							{
								num268 = 0.2f;
							}

```


---

## 🤖 Assistant · 2026-08-11T04:55:07.991Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now the out-of-water part (after the `if (wet)` block, `else` branch) for goldfish flapping. Let me grep for the else after the wet block — probably around line 470+ in ai16. Also check for goldfish out of water behavior (velocity.Y = -5 etc.) and GoldfishWalker type 362? Let me look at 470-560.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:55:08.383Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"else\" /tmp/ai16.txt | awk -F: '$1>470 && $1<700' | head; echo ===; sed -n '470,600p' /tmp/ai16.txt",
 "description": "Read AI_016 out-of-water branch"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:55:14.574Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
472:			else
484:					else if (Main.netMode != 1)
517:			else
545:					else
557:			else if (!Main.player[target].dead)
591:					else if (velocity.X > 0f)
600:				else if (direction == 1 && velocity.X < 3f)
607:					else if (velocity.X < 0f)
630:				else
669:			else
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-11T04:55:16.281Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '470,680p' /tmp/ai16.txt",
 "description": "Read AI_016 out-of-water fish flap logic"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:55:21.034Z

**📎 ToolResult**

```
				}
			}
			else
			{
				if (velocity.Y == 0f)
				{
					if (type == 65 || type == 692)
					{
						velocity.X *= 0.94f;
						if (velocity.X > -0.2f && velocity.X < 0.2f)
						{
							velocity.X = 0f;
						}
					}
					else if (Main.netMode != 1)
					{
						velocity.Y = (float)Main.rand.Next(-50, -20) * 0.1f;
						velocity.X = (float)Main.rand.Next(-20, 20) * 0.1f;
						direction = ((Main.rand.Next(2) == 0) ? 1 : (-1));
						NetUpdateIgnoreSpamLimit();
					}
				}
				velocity.Y += 0.3f;
				if (velocity.Y > 10f)
				{
					velocity.Y = 10f;
				}
				this.ai[0] = 1f;
			}
			if (type == 692 && this.ai[0] == 0f)
			{
				Player player2 = Main.player[target];
				rotation = (base.Center - player2.Center).SafeNormalize(Vector2.Zero).ToRotation();
				if (spriteDirection == -1)
				{
					rotation += MathF.PI;
				}
				rotation = MathHelper.WrapAngle(rotation);
				if (rotation < -0.3f)
				{
					rotation = -0.3f;
				}
				if (rotation > 0.3f)
				{
					rotation = 0.3f;
				}
			}
			else
			{
				rotation = velocity.Y * (float)direction * 0.1f;
				if (rotation < -0.2f)
				{
					rotation = -0.2f;
				}
				if (rotation > 0.2f)
				{
					rotation = 0.2f;
				}
			}
			return;
		}
		if (aiStyle == 17)
		{
			noGravity = true;
			if (this.ai[0] == 0f)
			{
				noGravity = false;
				TargetClosest();
				if (Main.netMode != 1)
				{
					if (velocity.X != 0f || velocity.Y < 0f || (double)velocity.Y > 0.3)
					{
						this.ai[0] = 1f;
						netUpdate = true;
					}
					else
					{
						Rectangle rectangle = new Rectangle((int)Main.player[target].position.X, (int)Main.player[target].position.Y, Main.player[target].width, Main.player[target].height);
						if (new Rectangle((int)position.X - 100, (int)position.Y - 100, width + 200, height + 200).Intersects(rectangle) || life < lifeMax)
						{
							this.ai[0] = 1f;
							velocity.Y -= 6f;
							netUpdate = true;
						}
					}
				}
			}
			else if (!Main.player[target].dead)
			{
				if (collideX)
				{
					velocity.X = oldVelocity.X * -0.5f;
					if (direction == -1 && velocity.X > 0f && velocity.X < 2f)
					{
						velocity.X = 2f;
					}
					if (direction == 1 && velocity.X < 0f && velocity.X > -2f)
					{
						velocity.X = -2f;
					}
				}
				if (collideY)
				{
					velocity.Y = oldVelocity.Y * -0.5f;
					if (velocity.Y > 0f && velocity.Y < 1f)
					{
						velocity.Y = 1f;
					}
					if (velocity.Y < 0f && velocity.Y > -1f)
					{
						velocity.Y = -1f;
					}
				}
				TargetClosest();
				if (direction == -1 && velocity.X > -3f)
				{
					velocity.X -= 0.1f;
					if (velocity.X > 3f)
					{
						velocity.X -= 0.1f;
					}
					else if (velocity.X > 0f)
					{
						velocity.X -= 0.05f;
					}
					if (velocity.X < -3f)
					{
						velocity.X = -3f;
					}
				}
				else if (direction == 1 && velocity.X < 3f)
				{
					velocity.X += 0.1f;
					if (velocity.X < -3f)
					{
						velocity.X += 0.1f;
					}
					else if (velocity.X < 0f)
					{
						velocity.X += 0.05f;
					}
					if (velocity.X > 3f)
					{
						velocity.X = 3f;
					}
				}
				float num272 = Math.Abs(position.X + (float)(width / 2) - (Main.player[target].position.X + (float)(Main.player[target].width / 2)));
				float num273 = Main.player[target].position.Y - (float)(height / 2);
				if (num272 > 50f)
				{
					num273 -= 100f;
				}
				if (position.Y < num273)
				{
					velocity.Y += 0.05f;
					if (velocity.Y < 0f)
					{
						velocity.Y += 0.01f;
					}
				}
				else
				{
					velocity.Y -= 0.05f;
					if (velocity.Y > 0f)
					{
						velocity.Y -= 0.01f;
					}
				}
				if (velocity.Y < -3f)
				{
					velocity.Y = -3f;
				}
				if (velocity.Y > 3f)
				{
					velocity.Y = 3f;
				}
			}
			if (wet)
			{
				if (velocity.Y > 0f)
				{
					velocity.Y *= 0.95f;
				}
				velocity.Y -= 0.5f;
				if (velocity.Y < -4f)
				{
					velocity.Y = -4f;
				}
				TargetClosest();
			}
			return;
		}
		if (aiStyle == 18)
		{
			bool flag23 = false;
			if (wet && this.ai[1] == 1f)
			{
				flag23 = true;
			}
			else
			{
				dontTakeDamage = false;
			}
			if (Main.expertMode && (type == 63 || type == 64 || type == 103 || type == 242))
			{
				if (wet)
				{
					if (target >= 0 && Main.player[target].wet && !Main.player[target].dead && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height) && (Main.player[target].Center - base.Center).Length() < 150f)
					{
						if (this.ai[1] == 0f)
						{

```


---

## 🤖 Assistant · 2026-08-11T04:55:31.714Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I now have AI_016 fully. Note: goldfish flap — actually the "out of water" behavior: velocity.Y random -5..-2, X -2..2, direction random, then gravity +0.3 capped 10. Type 65/692 (crimson goldfish?) don't hop (velocity.X *= 0.94).

Also note aiStyle 16 wet branch: fish flee from player in water (flag22 for non-55/592/607/615/688... wait flag22 is set when player is wet and CanHit — for types NOT in that exclusion list; so those types DO flee; the excluded ones (goldfish, pupfish, dolphin, pufferfish) don't flee).

Now I need:
- NPC names for 595-601, 583-585, 687, 610, 593, 616/617/625, 661, 653, 444, 604/605/669, 612/613, 626/627, 592, 607, 608, 603, 609, 363/365.
- Common traps: dayTime despawn, catchable handling. Critters despawn during day — that's not in AI; it's in NPC.UpdateNPC or SpawnRate? Actually critters "vanish during day" is handled per-AI (butterflies/fireflies: the AI_064 localAI[2] light blink). The actual despawn of butterflies at dawn is in... hmm. In vanilla, butterflies and fireflies despawn at daybreak — I recall `NPC.life = ...`? Actually critters don't despawn; they just stop spawning. Wait — no, vanilla butterflies/fireflies DO die at dawn. Let me check: In Terraria, butterflies spawn during day and are gone at night? Actually butterflies remain. Fireflies spawn at night, remain during day (they blink their light). Hmm. Let me check the UpdateAI / AI section for dayTime checks per critter. Let me grep "Main.dayTime" near critter handling, particularly a generic one.

Let me check the AI_007 critter relevant parts: line 91374 "if (aiStyle == 7 && position.Y > Main.bottomWorld...)". And line 82035, 91920, 93841, 94225 — these are in other methods (StrikeNPC? HitEffect?). Let me look at those quickly since they matter for "受击反应" (hit reaction) — e.g., type 362/364/602/608 transform to type+1 when falling fast or wet (that's the seagull/frog -> bugged form?). Actually 362 is "Frog" (jumps) and 363 "Duck"? Let me check names.

Also stoneDefense: grep found nothing; user mentioned "stoneDefense 分支" — probably they misremember; the equivalent is `npc.dontTakeDamage`/`defense`. Skip.

Let me get names quickly and check a few cross-references. I'll grep NPCID for the list of IDs.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:55:32.740Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"public const short\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/NPCID.cs | awk -F'[,= ]+' '{print $NF, $0}' | awk '$1>=355 && $1<=692' | awk '{print $2\" \"$3\" \"$4\" \"$5\" = \"$1}' | head -60",
 "description": "List NPCID names for critter ID range"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:55:39.228Z

**📎 ToolResult**

```
11073: public const short = 4;
11075: public const short = 5;
11077: public const short = 6;
11137: public const short = 36;
11139: public const short = 37;
11141: public const short = 38;
11143: public const short = 39;
11145: public const short = 40;
11147: public const short = 41;
11149: public const short = 42;
11151: public const short = 43;
11153: public const short = 44;
11155: public const short = 45;
11157: public const short = 46;
11159: public const short = 47;
11161: public const short = 48;
11163: public const short = 49;
11165: public const short = 50;
11167: public const short = 51;
11169: public const short = 52;
11171: public const short = 53;
11173: public const short = 54;
11175: public const short = 55;
11177: public const short = 56;
11179: public const short = 57;
11181: public const short = 58;
11183: public const short = 59;
11185: public const short = 60;
11187: public const short = 61;
11189: public const short = 62;
11191: public const short = 63;
11193: public const short = 64;
11195: public const short = 65;
11197: public const short = 66;
11199: public const short = 67;
11201: public const short = 68;
11203: public const short = 69;
11775: public const short = 355;
11777: public const short = 356;
11779: public const short = 357;
11781: public const short = 358;
11783: public const short = 359;
11785: public const short = 360;
11787: public const short = 361;
11789: public const short = 362;
11791: public const short = 363;
11793: public const short = 364;
11795: public const short = 365;
11797: public const short = 366;
11799: public const short = 367;
11801: public const short = 368;
11803: public const short = 369;
11805: public const short = 370;
11807: public const short = 371;
11809: public const short = 372;
11811: public const short = 373;
11813: public const short = 374;
11815: public const short = 375;
11817: public const short = 376;
11819: public const short = 377;

```


---

## 🤖 Assistant · 2026-08-11T04:55:42.642Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"public const short.*= \\(355\\|356\\|357\\|358\\|359\\|360\\|361\\|362\\|363\\|364\\|365\\|366\\|374\\|375\\|377\\|445\\|446\\|447\\|448\\|444\\|484\\|485\\|486\\|487\\|55\\|583\\|584\\|585\\|592\\|593\\|595\\|596\\|597\\|598\\|599\\|600\\|601\\|602\\|603\\|604\\|605\\|606\\|607\\|608\\|609\\|610\\|612\\|613\\|615\\|616\\|617\\|625\\|626\\|627\\|653\\|654\\|655\\|661\\|669\\|677\\|687\\|688\\|606\\|299\\|300\\|148\\|361\\),\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/NPCID.cs",
 "description": "Get exact const names for critter IDs"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:55:42.667Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-11T04:55:46.748Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '11775,11796p;11819,11820p;11950,11955p;12090,12100p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/NPCID.cs; echo ---; grep -n \"= 583,\\|= 584,\\|= 585,\\|= 592,\\|= 593,\\|= 595,\\|= 596,\\|= 597,\\|= 598,\\|= 599,\\|= 600,\\|= 601,\\|= 602,\\|= 603,\\|= 604,\\|= 605,\\|= 606,\\|= 607,\\|= 608,\\|= 609,\\|= 610,\\|= 612,\\|= 613,\\|= 615,\\|= 616,\\|= 617,\\|= 625,\\|= 626,\\|= 627,\\|= 653,\\|= 654,\\|= 655,\\|= 661,\\|= 669,\\|= 677,\\|= 687,\\|= 688,\\|= 299,\\|= 300,\\|= 366,\\|= 148,\\|= 357,\\|= 374,\\|= 359,\\|= 360,\\|= 448,\\|= 444,\\|= 55,\\|= 362,\\|= 363,\\|= 364,\\|= 365\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/NPCID.cs",
 "description": "Extract critter ID to name mapping"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:55:46.785Z

**📎 ToolResult**

```
	public const short Firefly = 355;

	public const short Butterfly = 356;

	public const short Worm = 357;

	public const short LightningBug = 358;

	public const short Snail = 359;

	public const short GlowingSnail = 360;

	public const short Frog = 361;

	public const short Duck = 362;

	public const short Duck2 = 363;

	public const short DuckWhite = 364;

	public const short DuckWhite2 = 365;

	public const short Grasshopper = 377;


	public const short GoldFrog = 445;

	public const short GoldGrasshopper = 446;

	public const short GoldMouse = 447;

	public const short TombCrawlerHead = 513;

	public const short TombCrawlerBody = 514;

	public const short TombCrawlerTail = 515;

	public const short SolarFlare = 516;

	public const short LunarTowerSolar = 517;

---
11795:	public const short DuckWhite2 = 365;

```


---

## 🤖 Assistant · 2026-08-11T04:55:48.836Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The `= 583,` grep failed because declarations are multi-line? No — they're on one line like `public const short Firefly = 355;`. The grep pattern with `= 583,` should match `= 583;`. Ah, I used comma instead of semicolon. Let me redo with `= 583;`.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:55:50.342Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"= 58[345];\\|= 59[2-9];\\|= 60[0-9];\\|= 61[0-7];\\|= 625;\\|= 626;\\|= 627;\\|= 65[34];\\|= 655;\\|= 661;\\|= 669;\\|= 677;\\|= 687;\\|= 688;\\|= 299;\\|= 300;\\|= 366;\\|= 148;\\|= 374;\\|= 357;\\|= 359;\\|= 360;\\|= 448;\\|= 444;\\|= 55;\\|= 36[1-5];\\|= 48[4-7];\\|= 606;\\|= 615;\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/NPCID.cs",
 "description": "Map critter IDs to names"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:55:50.365Z

**📎 ToolResult**

```
11175:	public const short Goldfish = 55;
11361:	public const short Penguin = 148;
11663:	public const short Squirrel = 299;
11665:	public const short Mouse = 300;
11779:	public const short Worm = 357;
11783:	public const short Snail = 359;
11785:	public const short GlowingSnail = 360;
11787:	public const short Frog = 361;
11789:	public const short Duck = 362;
11791:	public const short Duck2 = 363;
11793:	public const short DuckWhite = 364;
11795:	public const short DuckWhite2 = 365;
11797:	public const short ScorpionBlack = 366;
11813:	public const short TruffleWorm = 374;
11949:	public const short GoldButterfly = 444;
11957:	public const short GoldWorm = 448;
12029:	public const short EnchantedNightcrawler = 484;
12031:	public const short Grubby = 485;
12033:	public const short Sluggy = 486;
12035:	public const short Buggy = 487;
12231:	public const short FairyCritterPink = 583;
12233:	public const short FairyCritterGreen = 584;
12235:	public const short FairyCritterBlue = 585;
12249:	public const short GoldGoldfish = 592;
12251:	public const short GoldGoldfishWalker = 593;
12253:	public const short WindyBalloon = 594;
12255:	public const short BlackDragonfly = 595;
12257:	public const short BlueDragonfly = 596;
12259:	public const short GreenDragonfly = 597;
12261:	public const short OrangeDragonfly = 598;
12263:	public const short RedDragonfly = 599;
12265:	public const short YellowDragonfly = 600;
12267:	public const short GoldDragonfly = 601;
12269:	public const short Seagull = 602;
12271:	public const short Seagull2 = 603;
12273:	public const short LadyBug = 604;
12275:	public const short GoldLadyBug = 605;
12277:	public const short Maggot = 606;
12279:	public const short Pupfish = 607;
12281:	public const short Grebe = 608;
12283:	public const short Grebe2 = 609;
12285:	public const short Rat = 610;
12287:	public const short Owl = 611;
12289:	public const short WaterStrider = 612;
12291:	public const short GoldWaterStrider = 613;
12293:	public const short ExplosiveBunny = 614;
12295:	public const short Dolphin = 615;
12297:	public const short Turtle = 616;
12299:	public const short TurtleJungle = 617;
12315:	public const short SeaTurtle = 625;
12317:	public const short Seahorse = 626;
12319:	public const short GoldSeahorse = 627;
12371:	public const short HellButterfly = 653;
12373:	public const short Lavafly = 654;
12375:	public const short MagmaSnail = 655;
12387:	public const short EmpressButterfly = 661;
12403:	public const short Stinkbug = 669;
12419:	public const short Shimmerfly = 677;
12439:	public const short BoundTownSlimeYellow = 687;
12441:	public const short Pufferfish = 688;

```


---

## 🤖 Assistant · 2026-08-11T04:55:53.424Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Wait, 687 is BoundTownSlimeYellow? But flag9 = type==361||445||687 — frogs... 687? Hmm flag9 (frog-like water burst). Let me check: flag9 = type == 361 || type == 445 || type == 687. 687 = BoundTownSlimeYellow?? That seems wrong. Maybe grep ordering issue: "= 687;" matched BoundTownSlimeYellow = 687. Hmm, could be. Let me check nearby lines 12435-12441.

Also 46 = Bunny? Check. And 610 Rat, 687... let me verify 46 and 687 and 148/149.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:55:54.177Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '11155,11160p;12435,12442p;11360,11365p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/NPCID.cs; grep -n \"BoundTownSlimeYellow\\|= 46;\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/NPCID.cs",
 "description": "Verify IDs 46, 687, 149"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:55:54.209Z

**📎 ToolResult**

```
	public const short Tim = 45;

	public const short Bunny = 46;

	public const short CorruptBunny = 47;


	public const short Penguin = 148;

	public const short PenguinBlack = 149;

	public const short IceBat = 150;
	public const short BoundTownSlimeOld = 685;

	public const short BoundTownSlimePurple = 686;

	public const short BoundTownSlimeYellow = 687;

	public const short Pufferfish = 688;

11157:	public const short Bunny = 46;
12439:	public const short BoundTownSlimeYellow = 687;

```


---

## 🤖 Assistant · 2026-08-11T04:56:02.310Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting: flag9 = 361(Frog)/445(GoldFrog)/687(BoundTownSlimeYellow — that's a town slime which is also in flag10 = IsTownSlime, so it can burst in water). OK.

Now let me quickly check a couple of remaining things:
1. AI_007 critter water-related and penguin localAI[0] random 1-4 (line 202: penguin localAI[0] = Next(1,5) — probably penguin variation... used elsewhere).
2. The "受击反应" for critters — line 91920 "else if (aiStyle == 7 && ai[0] == 25f)" is shimmer. Line 82035 relates to FindFrame. Where's "flee when hit"? In AI_007 flag16 includes justHit? Let me check: In AI_007, the danger detection loop covers hostile NPCs (not friendly). For critters being hit: StrikeNPC sets ai[0]? Actually the flee-on-hit for critters — in vanilla, hitting a critter makes it run (ai[0]=1, direction away). Let me grep "justHit" inside /tmp/ai7.txt.

3. Day despawn for fireflies/butterflies: grep "Main.dayTime" in relevant places. Actually for critters, daytime disappearance: In NPC.cs there might be a check in AI for butterflies... I didn't see dayTime in AI_064/065 except the light blink condition. So critters do NOT despawn at dawn — they only stop spawning. That's the trap: user assumed "白天消失?" — answer: no, fireflies/butterflies don't despawn; their lights blink off during day (localAI[2] only set when !dayTime or underground).

Wait, but fireflies famously despawn at dawn? Let me check... In Terraria, fireflies caught and released persist. Actually the AI_064 code I read shows nothing about despawn. So no despawn. Good — but let me double check by grepping "active = false" in AI_064 region — I read the whole block 34256-34486; only ai[2]>=60 despawn is in AI_065 for Empress (661). Correct.

4. Catchable mechanism: `Catchable` — is it in AI? Let me grep "catchItem" and "Catchable" in NPC.cs to note.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:56:03.182Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"justHit\" /tmp/ai7.txt | head; echo ===CATCH===; grep -n \"Catchable\\b\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -10; echo ===catchItem===; grep -n \"catchItem = \" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head",
 "description": "Check justHit flee and catchable handling"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:56:09.947Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
(eval):1: ==CATCH=== not found

```


---

## 🤖 Assistant · 2026-08-11T04:56:17.488Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"justHit\" /tmp/ai7.txt | head -5; grep -cn \"Catchable\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; grep -n \"Catchable\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -5; grep -n \"catchItem = \" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -8",
 "description": "Check justHit flee, Catchable, catchItem"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:56:22.290Z

**📎 ToolResult**

```
5
17786:		if (type >= 0 && type < NPCID.Count && Main.npcCatchable[type])
80907:		else if (Type >= 0 && Type < NPCID.Count && (Main.npcCatchable[Type] || who == Main.myPlayer) && CanReleaseNPCs(who))
91473:		SubAI_HandleTemporaryCatchableNPCPlayerInvulnerability();
91588:	private void SubAI_HandleTemporaryCatchableNPCPlayerInvulnerability()
91590:		if (type >= 0 && type < NPCID.Count && Main.npcCatchable[type])
8381:		catchItem = 0;
9278:			catchItem = 2019;
9404:			catchItem = 261;
9692:				catchItem = 2015;
9696:				catchItem = 2016;
9700:				catchItem = 2017;
10803:			catchItem = 2205;
10815:			catchItem = 2205;

```


---

## 🤖 Assistant · 2026-08-11T04:56:31.998Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Catchable: `Main.npcCatchable[type]` set in SetDefaults (line 17786 block). Catching is via projectile (bug net) checking catchItem — not in AI. And SubAI_HandleTemporaryCatchableNPCPlayerInvulnerability at 91588 gives player invuln briefly after releasing? Fine, one line note.

justHit in ai7.txt: grep printed nothing for first (no output before 5? Actually output shows "5" which is count? confusing). The first grep returned nothing visible. Let me check justHit handling for critters — probably in AI_007 via flag16 (danger) only, and life<lifeMax flee. Actually for critters, flee on hit: at line 970 of ai16 (fish) uses life<lifeMax. In AI_007, the ai[0]==0 idle block has "if (stinky) ai[0]=1". Hmm. Where do critters flee when hit? In AI_007: for town NPC, `if (friendly && (flag16 || flag21))` — flag21 is drowning. For critters: nothing about justHit directly; but there is the danger loop which scans hostile NPCs. And also `life < lifeMax` — check. Let me grep "life < lifeMax\|life != lifeMax" in ai7.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:56:32.896Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"life < lifeMax\\|life != lifeMax\\|justHit\" /tmp/ai7.txt; echo ===; sed -n '5326,53270p' /dev/null 2>/dev/null; grep -n \"GetWalkPrediction\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -3",
 "description": "Check flee-on-hit and walk prediction helper"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:56:39.442Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-11T04:56:41.372Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"life < lifeMax\\|life != lifeMax\\|justHit\" /tmp/ai7.txt",
 "description": "Grep life/justHit in AI_007 body"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:56:51.540Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-11T04:56:56.718Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So AI_007 has no justHit flee — critters flee based on: hostile NPC within DangerDetectRange (default 200), or stinky. Actually wait, `NPCID.Sets.DangerDetectRange` default 200. Hmm, but hitting a critter — in vanilla, hitting a critter with a net catches it; hitting with a sword kills it (5 HP). There's no flee-on-hit in AI_007. Good to note.

Hmm, but wait: line 82035 in NPC.cs: `if (aiStyle == 7 && (ai[0] == 3f || ai[0] == 4f || ai[0] == 16f || ai[0] == 17f))` — that's in AI for... let me not bother.

Also check the penguin localAI[0] = Next(1,5) usage — probably FindFrame. Not needed.

Now remaining details to verify:
- AI_007 flag2: what is flag2? It was referenced (if flag2 direction = num15 else -num15). Need to know flag2 definition. Let me grep the top of AI_007_TownEntities for "flag2 =" / "bool flag2".
- Also "flag" variable (talked-to / at home?).

Let me check the head of AI_007_TownEntities (lines 1-180 of /tmp/ai7.txt).
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:56:56.719Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "/tmp/ai7.txt",
 "limit": 180
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:56:56.725Z

**📎 ToolResult**

```
1		private void AI_007_TownEntities()
2		{
3			ShimmeredTownNPCs[type] = IsShimmerVariant;
4			if (type == 441 && GivenName == "Andrew")
5			{
6				defDefense = 200;
7			}
8			if (Main.onlyShimmerOceanWorlds && type == 680 && GivenName == "Slimefors")
9			{
10				life = lifeMax;
11				defDefense = 99999;
12			}
13			int num = 300;
14			if (type == 638 || type == 656 || NPCID.Sets.IsTownSlime[type])
15			{
16				num = 0;
17			}
18			bool flag = Main.raining;
19			if (!Main.dayTime)
20			{
21				flag = true;
22			}
23			if (Main.eclipse)
24			{
25				flag = true;
26			}
27			if (Main.slimeRain)
28			{
29				flag = true;
30			}
31			if (Main.IsItStorming && (double)(position.Y / 16f) < Main.worldSurface)
32			{
33				flag = true;
34			}
35			float num2 = 1f;
36			if (Main.masterMode)
37			{
38				defense = (dryadWard ? (defDefense + 20) : defDefense);
39			}
40			else if (Main.expertMode)
41			{
42				defense = (dryadWard ? (defDefense + 15) : defDefense);
43			}
44			else
45			{
46				defense = (dryadWard ? (defDefense + 10) : defDefense);
47			}
48			float num3 = 2f;
49			bool flag2 = false;
50			if (isLikeATownNPC)
51			{
52				bool flag3 = life == lifeMax;
53				lifeMax = defLifeMax;
54				if (combatBookWasUsed)
55				{
56					lifeMax += 250;
57					num3 *= 0.8f;
58					num2 += 0.25f;
59					defense += 8;
60				}
61				if (combatBookVolumeTwoWasUsed)
62				{
63					lifeMax += 250;
64					num3 *= 0.8f;
65					num2 += 0.25f;
66					defense += 8;
67				}
68				if (lifeMax > defLifeMax && flag3)
69				{
70					life = lifeMax;
71				}
72				if (downedSlimeKing)
73				{
74					num3 *= 0.985f;
75					num2 += 0.05f;
76					defense += 2;
77				}
78				if (downedBoss1)
79				{
80					num3 *= 0.985f;
81					num2 += 0.05f;
82					defense += 2;
83				}
84				if (downedDeerclops)
85				{
86					num3 *= 0.985f;
87					num2 += 0.1f;
88					defense += 3;
89				}
90				if (downedBoss2)
91				{
92					num3 *= 0.985f;
93					num2 += 0.1f;
94					defense += 3;
95				}
96				if (downedBoss3)
97				{
98					num3 *= 0.985f;
99					num2 += 0.1f;
100					defense += 3;
101				}
102				if (downedQueenBee)
103				{
104					num3 *= 0.985f;
105					num2 += 0.1f;
106					defense += 3;
107				}
108				if (Main.hardMode)
109				{
110					num3 *= 0.985f;
111					num2 += 0.4f;
112					defense += 12;
113				}
114				if (downedQueenSlime)
115				{
116					num3 *= 0.985f;
117					num2 += 0.15f;
118					defense += 6;
119				}
120				if (downedMechBoss1)
121				{
122					num3 *= 0.985f;
123					num2 += 0.15f;
124					defense += 6;
125				}
126				if (downedMechBoss2)
127				{
128					num3 *= 0.985f;
129					num2 += 0.15f;
130					defense += 6;
131				}
132				if (downedMechBoss3)
133				{
134					num3 *= 0.985f;
135					num2 += 0.15f;
136					defense += 6;
137				}
138				if (downedPlantBoss)
139				{
140					num3 *= 0.985f;
141					num2 += 0.15f;
142					defense += 8;
143				}
144				if (downedEmpressOfLight)
145				{
146					num3 *= 0.985f;
147					num2 += 0.15f;
148					defense += 8;
149				}
150				if (downedFishron)
151				{
152					num3 *= 0.985f;
153					num2 += 0.15f;
154					defense += 8;
155				}
156				if (downedGolemBoss)
157				{
158					num3 *= 0.985f;
159					num2 += 0.15f;
160					defense += 8;
161				}
162				if (downedAncientCultist)
163				{
164					num3 *= 0.985f;
165					num2 += 0.15f;
166					defense += 20;
167				}
168				if (Main.infectedSeed && type == 20)
169				{
170					flag2 = true;
171					life = lifeMax;
172					defDefense = 99999;
173					immortal = true;
174				}
175				if (Main.netMode != 1 && WorldGen.Skyblock.lowTiles)
176				{
177					if (num3 > 1f)
178					{
179						num3 = (num3 + 1f) / 2f;
180					}

```


---

## 🤖 Assistant · 2026-08-11T04:57:06.339Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
flag = "should stay home indoors" (raining/night/eclipse/slimeRain/storm). flag2 = infected seed guide special.

Now I have enough for AI_007. A few more quick greps:
1. AI_007_GetWalkPrediction (56093) — brief semantics: keepwalking/avoidFalling. I have enough: it checks ahead tiles for cliff.
2. Check the aiStyle 7 critter-specific: 593 (GoldGoldfishWalker), 602/608 transform when falling fast or wet -> type+1 (Seagull602->603 flying form, Grebe608->609). Note this is the inverse of ducks: 363/365/603/609 (Duck2/DuckWhite2/Seagull2/Grebe2, aiStyle 68 flying forms) transform to type-1 when landing and not wet.
3. type 46 bunny — where's bunny jump? Bunny is aiStyle 7 and jumps using the generic "jump over 1-block obstacle" logic + TownCritter ai[1] extras. Also note NPCID.Sets.TownCritter set for these critters.

Check what NPCID.Sets.TownCritter includes to identify which aiStyle-7 types are critters: grep in NPCID.cs Sets.

Let me also verify AI_016's fish despawn/`hitEffect`... not needed.

One more: for aiStyle 64, the "scared" logic localAI[1] in firefly family? In AI_064, `else if (localAI[1] > 0f) localAI[1]--` and the blink logic. Fine.

Also need AI_065 vs 064 differences: 064 velocity smoothing 80 vs 065 60; flee from enemies: 065 flees NPCs within 100f every 15 ticks (localAI[1] interval), max speed 16; 064 only Faeling 677 flees NPCs and players. 065 idle wander speed 0.26-3.0 vs 064 0.05-1.5.

Now check TownCritter sets quickly and also "DangerDetectRange" values for critters? Probably -1 default -> 200.

Let me do one final grep for TownCritter list and be done.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:57:06.346Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"TownCritter\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/NPCID.cs | head -5; grep -n \"TownCritter\\[\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ID/NPCID.cs | head",
 "description": "Find TownCritter set definition"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:57:06.389Z

**📎 ToolResult**

```
4821:		public static bool[] TownCritter = Factory.CreateBoolSet(46, 148, 149, 230, 299, 300, 303, 337, 361, 362, 364, 366, 367, 443, 445, 447, 538, 539, 540, 583, 584, 585, 592, 593, 602, 607, 608, 610, 616, 617, 625, 626, 627, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 687, 688);
ugrep: warning: ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ID/NPCID.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-11T04:57:29.103Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Note: TownCritter includes 687 (BoundTownSlimeYellow) and 688 (Pufferfish) — interesting, 688 pufferfish is TownCritter? That's for AI_007 purposes? Actually 688 is aiStyle 16. TownCritter[688]=true used in... hmm AI_007 only for aiStyle 7. Also used in AI_007_GetWalkPrediction? Whatever — worth a note.

Wait, 688 in that list might actually be for a slime. Anyway.

Also DangerDetectRange — default -1 => num11 = 200.

I have all 13 sections. Let me also double-check the aiStyle 66 worm "雨后出现" — spawning is outside AI; note briefly. And the worm velocity when ai[0]!=1: stationary. Truffle worm 374: ai[1] charges up to 90 when player within 160f, then Y+=16 and Transform(375) = TruffleWormDigger.

Also 484 EnchantedNightcrawler glows (light 0.3,0.1,0.25 * essScale blend).

One more check for AI_116: ai[0] != 0 return — meaning when caught/dying? Fine.

I'm at ~25 tool calls. Time to write the final report.

Let me compile the compact spec.

Line numbers (NPC.cs):
1. aiStyle 7 → dispatch 20769-20773, method AI_007_TownEntities 53366 (tmp offsets: +53365).
   - Penguin localAI[0]=Next(1,5): 53567 (202+53365=53567)
   - Transform for 362/364/602/608: 53585 (220)
   - TownCritter branch: 53683 (318)
   - Danger loop (hostile NPC scan, DangerDetectRange default 200): 53884 (519)
   - idle ai[0]==0: 54030 (665); wet→walk for frog/turtle/townslime: 54049 (684)
   - walk ai[0]==1: 54205 (840); speed table 54280-54326 (915-961)
   - jump block 54315-54417 (950-1052): StepUp retry, jump -6/-5/-4.4, rabbit/mouse? flag7 (300/447/610) turn around instead
   - gravity: handled globally (npcGravity 0.3); velocity.Y<0 && wet => *1.2; TownCritter && !flag7 => *1.2 (bunny hop boost)
   - flee states ai[0]==8 (scared standing), ai[0]==2/11 sit, 3/4/5/8/9/16/17/20-23 idle anims.
   - Note flag8/flag9 water burst: frogs (361/445/687) in water get instant X push num22*10.
   - Note: no justHit-based flee in AI_007; danger detection is enemy-based; `friendly` types speed up when danger (num22=1.5 + up to 0.9 by missing life).

Hmm wait, flag7 = type 300/447/610 (Mouse/GoldMouse/Rat): num22=2, num23=1 — they dart fast, and when blocked by 2-high wall they turn around instead of jumping (else-if flag7 branch at 1150-1169 → direction*=-1 and velocity.X=0).

flag8 = 616/617/625 turtles: on land num22=0.5,num23=0.07; in water num22=2,num23=1 (625 seaturtle 2.5/1).
flag9 = 361/445/687 frogs.
299 squirrel & 538/539 & 639-645 (squirrel variants): num22=1.5.
614 ExplosiveBunny: 1.5/0.1 with danger.
Bunny 46 and others: 1.0/0.07.

2. aiStyle 64 block: 34256-34486. Details captured.
3. aiStyle 65: dispatch 34486-34489; method AI_065_Butterflies 45231-45447 (I read to 45445; catchItem at 45443).
4. aiStyle 66: 34490-34586.
5. aiStyle 67: 34586-34861.
6. aiStyle 68: 34861-35117.
7. aiStyle 112: dispatch 43173-43176; method 48453-~48900.
8. aiStyle 114: 43181-43184; method 48080-48251.
9. aiStyle 115: 43185-43188; method 47944-48078.
10. aiStyle 116: 43189-43192; method 47882-47942.
11. aiStyle 118: 43197-43200; method 47432-47486.
12. aiStyle 1: dispatch 19894-19897; AI_001_Slimes 60735. Grasshopper bits: flag3 (flee) 61479-61483; localAI[2] 90 ticks friendly timer 61854-61864; ai[0]+=3 61994-61997; jump modification 62088-62102.
13. aiStyle 16: 23549-24021ish. pufferfish 688: 23555-23620 (tmp 7-72 → +23548). dolphin 615: 23629-23746. generic: 23758+. out-of-water: 24018-24045ish (tmp 471-498 → +23547... let me compute: tmp line 471 corresponds to 23549+471-1=24019). flap random velocity at tmp 484 → 24032.

Common traps:
- Catchable: Main.npcCatchable[type] set in SetDefaults 17786; catch via net (projectile), catchItem set in SetDefaults; NOT in AI. SubAI_HandleTemporaryCatchableNPCPlayerInvulnerability 91588.
- Daytime despawn: no critter despawns at dawn inside these AI. Fireflies/butterflies only blink light (AI_064 localAI[2]) when !Main.dayTime || underground (position.Y/16 > worldSurface+10). Empress butterfly (661) fades out when player leaves hallow (ai[2] timer) — actual despawn active=false.
- wet flag: computed by Collision each tick (NPC.wet); some families check it.
- Many critters rely on gravity default 0.3 & tile collision (noTileCollide=false default); flight families set noGravity implicitly by just not applying gravity? Actually no — noGravity is set... in AI_064 there's no noGravity set. Hmm — for fireflies noGravity must be set elsewhere: NPC.SetDefaults sets noGravity via aiStyle? There's `if (NPCID.Sets.NPCBestiaryDrawOffset...)`. Actually there's a generic section in AI: let me recall — in AI_016? For flying critters, vanilla sets `npc.noGravity = true` in... AI_017 (birds) sets noGravity=true explicitly (we saw in aiStyle 17). AI_064 doesn't set noGravity — so it must be set from NPC default by aiStyle: In SetDefaults there is `noGravity = ...`? There's `if (aiStyle == 64...)`? Hmm. There is a known: `npc.noGravity = true` set in NPC.SetDefaults based on aiStyle via `NPCAIStyleSnapChecks`? Let me quickly grep "noGravity = true" near SetDefaults... Budget: I have ~4 calls left. One grep to resolve this, since it's a porting trap.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:57:29.656Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"noGravity\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | awk -F: '$1<21000' | head -20",
 "description": "Find where noGravity defaults are set for critter aiStyles"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:57:34.520Z

**📎 ToolResult**

```
6420:	public bool noGravity;
8467:		noGravity = false;
8646:			noGravity = true;
8662:			noGravity = true;
8676:			noGravity = true;
8706:			noGravity = true;
8735:			noGravity = true;
8764:			noGravity = true;
8793:			noGravity = true;
8810:			noGravity = true;
8828:			noGravity = true;
8847:			noGravity = true;
8866:			noGravity = true;
8886:			noGravity = true;
9005:			noGravity = true;
9035:			noGravity = true;
9077:			noGravity = true;
9092:			noGravity = true;
9108:			noGravity = true;
9125:			noGravity = true;

```


---

## 🤖 Assistant · 2026-08-11T04:57:37.576Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '8640,8665p;9000,9010p;9070,9080p;9120,9130p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read noGravity per-type defaults context"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:57:37.605Z

**📎 ToolResult**

```
			damage = 15;
			defense = 12;
			lifeMax = 2800;
			HitSound = SoundID.NPCHit1;
			DeathSound = SoundID.NPCDeath1;
			knockBackResist = 0f;
			noGravity = true;
			noTileCollide = true;
			boss = true;
			value = 30000f;
			npcSlots = 5f;
		}
		else if (type == 5)
		{
			width = 20;
			height = 20;
			aiStyle = 5;
			damage = 12;
			defense = 0;
			lifeMax = 8;
			HitSound = SoundID.NPCHit1;
			DeathSound = SoundID.NPCDeath1;
			noGravity = true;
			noTileCollide = true;
		}
		else if (type == 6)
			damage = 40;
			defense = 6;
			lifeMax = 26;
			HitSound = SoundID.NPCHit3;
			DeathSound = SoundID.NPCDeath3;
			noGravity = true;
			noTileCollide = true;
			value = 80f;
			knockBackResist = 0.4f;
		}
		else if (type == 24)
			height = 16;
			aiStyle = 9;
			damage = 20;
			defense = 0;
			lifeMax = 1;
			HitSound = SoundID.NPCHit3;
			DeathSound = SoundID.NPCDeath3;
			noGravity = true;
			noTileCollide = true;
			alpha = 255;
			knockBackResist = 0f;
			damage = 20;
			defense = 14;
			lifeMax = 600;
			HitSound = SoundID.NPCHit2;
			DeathSound = SoundID.NPCDeath2;
			noGravity = true;
			noTileCollide = true;
			knockBackResist = 0f;
		}
		else if (type == 37)
		{

```


---

## 🤖 Assistant · 2026-08-11T04:57:40.865Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So noGravity is per-NPC-type in SetDefaults (each critter like Firefly has noGravity=true declared in its own branch). For porting: our project has an npc json with per-type flags presumably. Good enough: note that noGravity/noTileCollide are per-type defaults in SetDefaults, not in AI (except AI_008-ish explicit overrides).

Now write the final compact report. I have 13 sections + common traps. Keep it dense with line numbers.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:58:58.944Z · glm-x-preview-260804

```
13 节小动物 AI 移植规格(行号均为 `Terraria/NPC.cs` 1.4.5.6 反编译,除非另注明)。整体结构:大 dispatch 在 `AI()` 内(`if (aiStyle == 7)` 20769 直接调 `AI_007_TownEntities()` 20773;64/65/66/67/68 内联于 34256/34486/34490/34586/34861;112-118 内联壳在 43173-43200,实体方法在后部)。

## 1. aiStyle 7 小动物(AI_007_TownEntities,53366 起,~2600 行)
城镇 NPC 与小动物同走一个方法,靠 `NPCID.Sets.TownCritter[type]`(NPCID.cs:4821 列表:`46,148,149,230,299,300,303,337,361,362,364,366,367,443,445,447,538,539,540,583-585,592,593,602,607,608,610,616,617,625,626,627,639-652,687,688`)区分。**没有 CountsAsCritter/stoneDefense 字段——这个 1456 版里不存在,别移植**。
- 状态字段:`ai[0]`=行为态(0 站立/1 行走/2、11 坐/3、4、16、17 与伙伴坐/5 坐椅子/8 受惊僵立/9-23 杂项),`ai[1]`=当前态倒计时,`ai[2]`=伙伴 whoAmI(3/4/16/17),`ai[3]`=0;`ai[0]==25` 为微光传送态(53592-53681,小动物可忽略)。`localAI[1]` 走廊往返锚点 X,`localAI[2]` 卡位计数,`localAI[3]` 多用途计时。
- 游走节奏(54030 起):站→走 在 `ai[1]` 归零且前方无悬崖时触发,`ai[1]=200+Next(300)`,**TownCritter 额外 +Next(200,400)**;走→站 `ai[1]=300+Next(300)`,TownCritter 反而 -Next(100)、城镇 NPC +Next(900)。站定时 `Main.rand.Next(80)==0` 有 1/80 概率原地转身(200 帧冷静期 localAI[3],54197-54202)。企鹅(148/149)进 AI 先 `localAI[0]=Next(1,5)`(53567,FindFrame 用)。
- 速度表(54280-54326):默认 `maxX(num22)=1f, acc(num23)=0.07f`;松鼠族 299/538/539/639-645 → maxX=1.5;乌龟 flag8(616/617/625):陆地 0.5/0.07,水中 2/1(625 海龟 2.5/1);鼠类 flag7(300 鼠/447 金鼠/610 鼠)=2/1(疾冲);614 爆炸兔 1.5/0.1;受威胁(friendly 且 flag16)→ maxX=1.5 + 失血比例×0.9,acc=0.1。青蛙 flag9(361/445/687)在水中:速度近零时直接 `velocity.X += num22*10*direction`,否则 velocity.X*=0.9(54333-54342)。
- 跳跃(54315-54417,`velocity.Y==0` 时):前方 1 格实心且上方净空 → `velocity.Y=-5f`;2 格 → `-6f`;脚下踩进半格(tileSafely3 情形)→ `-4.4f`;**不满足时:危险中(flag16)进入 ai[0]=8 受惊僵立 240 帧,否则掉头**。flag7(鼠类)不跳:撞墙直接 `direction*=-1; velocity.X=0`(54312-54319)。跳跃上升补偿:`velocity.Y<0 && wet → *=1.2`;`velocity.Y<0 && TownCritter && !flag7 → *=1.2`(兔/松鼠跳得更飘)(54398-54405)。1 格台阶 `Collision.StepUp` 若失败且 `ai[1]<100 && ai[1]%10==0` → 掉头(54246-54259)。悬崖回避用 `AI_007_TownEntities_GetWalkPrediction`(56093)。
- 受击反应:**AI_007 内无 justHit 逻辑**——受惊只来自危险扫描(53884-54028:对每个非友方 NPC 检查 `Distance<200`(或 `NPCID.Sets.DangerDetectRange[type]`)+`Collision.CanHit`);stinky 玩家也算危险。受惊 → `ai[0]=1, ai[1]=120+Next(120), direction=逃离方向`(`NPCID.Sets.PrettySafe` 可豁免)。挨打本身不触发逃跑。
- 水中:flag8/flag9 在水(53649-53655)直接进入行走态(200+Next(500,700));溺水预判 `AI_007_TownEntities_CheckIfWillDrown`(54142-54157)会按水体深度算跳出速度(0.3 重力公式,上限 26)。城镇 slime(flag10/13)水中 2/0.2。
- 形态切换(53585-53589):`362/364/602/608`(**Duck/DuckWhite/Seagull/Grebe**,行走形)当 `|velocity.Y|>4 或 wet` → `Transform(type+1)`(进入 68 飞形)。

## 2. aiStyle 64 萤火虫族(355 Firefly/358 LightningBug/654 Lavafly/677 Faeling,34256-34486)
- `ai[0]/ai[1]`=目标速度分量,`ai[3]`=随机 scale(0.75-1.11),`localAI[0]`=漂移重选计时,`localAI[1]`=闪烁间隔计时,`localAI[2]`=发光剩余帧,`localAI[3]`=是否已"近距漂移"标记。
- 漂移:每 `60-179` 帧(TargetClosest 后)若玩家 X 距离 >700 且 `localAI[3]==0` → 朝随机方向 `0.5-1.5px/f`(>1000 用 1.5-2.0,>850 用 1.0-1.5),Y 偏 -100~+250(偏向上);否则近距小漂移 0.05-1.5。速度平滑:`v = (v*79 + target)/80`。
- 垂直避障:向下 4 格内有实心/液体 → 反向;向上 30 格无实心 → 反向(34427-34465)。collideX → `velocity.X*=-0.2` 并翻转 ai[0]。
- 光照(34391-34409,仅 `localAI[2]>3` 时):358 紫蓝 (0.10125,0.21375,0.225)×scale;654 橙红 (0.225,0.105,0.06)×scale;其余萤火虫绿黄 (0.1095,0.15,0.0615)×scale。
- **昼夜:白天不消失**,只是不亮——`localAI[2]=Next(10,30)` 仅当 `!Main.dayTime || position.Y/16 > worldSurface+10`(34416-34423)。
- 677 Faeling(微光仙尘):世界边缘 40 格内回推;每 15 帧扫描 100px 内敌怪 + 150px 内玩家,逃逸速度叠加,上限 8;`rotation = velocity.X*0.3`(34307-34390)。

## 3. aiStyle 65 蝴蝶族(356 Butterfly/444 Gold/653 Hell/661 Empress,AI_065_Butterflies 45231)
与 64 骨架相同,差异:
- 平滑系数 60(vs 64 的 80),漂移速度 0.26-3.0(vs 0.05-1.5),近距漂移重选间隔 90-239 帧。
- 主动避敌(每 15 帧,45395-45427):100px 内敌怪叠加反方向速度,上限 **16px/f**(64 只有 Faeling 有这逻辑)。
- 661 EmpressButterfly(45235-45291):彩虹光 `hslToRgb(time*0.33%1,1,0.5)*0.3 + 0.1`;玩家离开神圣 300px 外 → `ai[2]` 计数涨到 60 → **`active=false` 真消失**(唯一的"离开环境即死"),`Opacity` 渐隐 + 彩尘;`dontTakeDamage = ai[2]>=25`。
- 356 君主蝶 `ai[2]`=1-7 花色变体(SetDefaults 时按 1%/2%/6%/10%/15%/19%/25% 反向权重),`catchItem = 1994 + ai[2] - 1`(45443)。

## 4. aiStyle 66 蠕虫族(357 Worm/448 GoldWorm/606 Maggot/374 TruffleWorm/484 EnchantedNightcrawler/485 Grubby/486 Sluggy/487 Buggy,34490-34586)
- `ai[0]`=0 静止 / 1 蠕动;`localAI[1]`=切换计时。静止 300-899 帧 → 蠕动 600-1799 帧(34533-34549)。蠕动速度 = 方向×`0.2`(485=0.25,486=0.325,487=0.4;374 再×3);`collideX → direction*=-1`(34506)。重力正常,`velocity.Y==0` 才有上述逻辑。
- 484 EnchantedNightcrawler 发光:`(0.3,0.1,0.25)×Next(90,111)%×(essScale+0.5)/2`(34492-34497)。
- 374 松露虫(34560-34584):额外段——160px 内有存活玩家则 `ai[1]` 每帧+1,到 90 → `position.Y+=16; Transform(375)`(TruffleWormDigger 钻地逃走)。**静止期速度为 0 且不会被随机蠕动惊扰**(受惊只由玩家接近触发)。
- "雨后出现"是 spawner 侧(`Main.raining` 刷怪条件),AI 内无雨逻辑。

## 5. aiStyle 67 蜗牛族(359 Snail/360 GlowingSnail/655 MagmaSnail,34586-34861)
- 359 用 `ai[3]` 存随机 scale(0.8-1.11),并同步把 width/height 缩到 `12*scale`(34600-34621)。
- 光照:360 (0.1,0.2,0.7),655 (0.6,0.3,0.1)(34623-34630)。
- 速度 `num1055`:普通蜗牛 0.3,发光/岩浆蜗牛 **0.6**(34631-34635)。
- 模式:`ai[2]>0` = "被惊扰逃跑"(1/7200 随机触发,或腾空超 5 帧触发,34646-34666)——正常重力,朝 direction 爬;`ai[2]==0` = **贴墙爬**:`noGravity=true`,`velocity = (num1055*direction, num1055*directionY)`,撞墙/撞地翻 direction 或 directionY,四象限旋转朝向(rotation 目标 0/1.57/3.14/4.71,以 0.1/帧 插值,34763-34856)。bottomSlope 检测(34690-34695)会掉头。33-38 行为镜面:撞墙瞬间先切 `ai[2]=0` 沉降一帧再转爬壁方向。
- 微光水(liquid>30 && tile.shimmer)→ `GetShimmered()`(34588-34597)。

## 6. aiStyle 68 鸭族(363 Duck2/365 DuckWhite2/603 Seagull2/609 Grebe2 飞形;34861-35117)
两态:`ai[0]=0` 游泳/陆行,`ai[0]=1` 飞行;`ai[1]`=飞行计时。整族 `noGravity=true`(飞形默认),仅 `ai[0]==0` 且非 wet 时 `noGravity=false`(34873-34876)。
- 水中(34884-34957):X 朝 direction 平滑到 2;前方 8+width/2 像素 tile 实心或无水 → `direction*=-1`;贴水面:由上/中/下 tile.liquid 反推水面 Y,-6px 偏移,`Center.Y > 水面` 时 `velocity.Y-=0.1`(下限 -8),否则 `velocity.Y=水面-Center.Y` 钉住。脱离水 → `ai[0]=1; direction*=-1`(34962-34967)。玩家进 200px 扩展盒或 `life<lifeMax` → 起飞:`ai[0]=1; velocity.Y-=6; direction*=-1`(34969-34976)。
- 飞行(34978-35115):`ai[1]>=300` 且 `velocity.Y==0 || collideY || wet` → 落回 `ai[0]=0` 并 `Transform(type-1, 0, 200+Next(200))`(35000-35003,回到行走形);否则 X 渐近 ±3(0.1/帧),前方 15 格向下扫描:5 格内有障碍 → `velocity.Y-=0.2` 额外抬升,有障碍 → `velocity.Y-=0.1`,无 → `velocity.Y+=0.1`;Y 限 [-4,3]。collideX/collideY 反弹 ×-0.5 保底 ±1~2。玩家 dead → 直接 return。
- Seagull2(603)是 `NPCID.Sets.BirdThatCanPoop` 候选,飞行中玩家正下方 50 次失败抽奖+CanHit 才投弹(34863-34871)。

## 7. aiStyle 112 仙女族(583 粉/584 绿/585 蓝,AI_112_FairyCritter 48453)
`ai[2]`=状态(0 游荡/1 追随飞/2 引导玩家/3 转圈/4 飞向宝箱/5 挖宝/6 等待/7 离场),`ai[0]/ai[1]`=锚点(状态 0 为出生点,2+ 为宝箱 tile),`ai[3]`=阶段计时,`localAI[1]`=存在计时。`lavaImmune=true`(除非状态 0/1)。
- 状态 0:绕出生点 20px 外微加速 0.04,Y 限 ±2;玩家 250px 内 → 状态 1。
- 状态 1:平飞,`velocity.X` 渐近 `direction×4.5`(0.04-0.4 分档),前方 20×8 tile 扫描决定 Y(净空 +0.05/有障碍 -0.2/5 格内有障碍再 -0.3),Y 限 [-5,3]。
- 状态 2(引导,`noTileCollide=true`):飞向玩家头顶矩形(`Width+60, Height/2`)最近点,速度 2(>150px ×2,>80px ×1.5);`GetBirdFlightRecommendation(6,3,...)` 微调 Y;穿墙计时 `ai[3]`(实心 +2、空 -1,封顶 400)。玩家碰到仙女命中盒 → 找宝箱(`GetFairyTreasureCoords`)→ 状态 3,找不到 → 状态 6。
- 状态 3:在玩家头顶按 `GetFairyCircleOffset` 做圆周舞(22px 高,65 帧一弧),210 帧后 → 状态 4 飞向宝箱;状态 4 抵达 → 状态 5;状态 6 贴玩家等待并反复重找宝箱;**存在满 18000 帧(5 分钟)强制 `ai[2]=7` 离场**(48457-48473)。
- 光照在各 FindFrame/Draw 侧;不绕玩家环飞——是引导寻宝宠物,不是装饰飘浮。

## 8. aiStyle 114 蜻蜓族(AI_114_Dragonflies 48080)
名字:595 Black/596 Blue/597 Green/598 Orange/599 Red/600 Yellow/601 **GoldDragonfly**——全是蜻蜓 7 色变体。
- `ai[0]`=0 悬停 / 1 突进;`ai[1]`=计时;`ai[2]/ai[3]`=驻留锚点(初始出生点);`localAI[0]`=初始化标记,`localAI[1]`=避敌扫描计时。
- 初始化:`velocity=(随机圆(5,3)+随机圆边(5,3))×0.4`,状态 1(48082-48092)。
- 悬停(0):`velocity*=0.94`,每 60-119 帧结束;离锚点 >96px → `velocity=方向×3`(突进),16-96px → ×1+抖动,<16px → 再随机。
- 突进(1):持续 4 帧(离锚点 >112px 时 200 帧,防丢锚);向下 3 格有实心/液体 → `velocity.Y-=0.2` 且 `*=0.9`;向上 30 格无实心 → `*=0.9`。wet → `velocity.Y=-3`(弹出水)。
- 避敌(每 15 帧):100px 敌怪 + 150px 玩家叠加逃逸 ×2,上限 16,并把锚点挪到逃逸方向 10 倍处(48174-48216)。
- 落锚迁移:闲时离锚 <16px,若锚 tile 是 519(cattail 香蒲)1/30、否则 1/4 概率重选锚:`FindCattailTop` 找香蒲顶,否则从脚下向下找地表再上抬 3-5 格(48217-48250)。

## 9. aiStyle 115 瓢虫/椿象(604 LadyBug/605 GoldLadyBug/669 Stinkbug,AI_115_LadyBugs 47944)
- `ai[0]`=飞行方向角(弧度),`ai[1]`=随机 scale(0.7-0.9),`ai[2]`=0 飞 / 1 陆行,`localAI[0]`=重选计时。**幸运机制钩子只提一句:杀瓢虫影响幸运,在 NPC 掉落/幸运系统(Player.Luck)侧,不在本 AI**。
- 飞行(47986-48034):`velocity = Lerp(velocity, ai[0].方向×1 + (windSpeedTarget×0.8, 0), 0.0125)`——慢飞且受风;向下 4 格实心/液体 → 角度取反;向上 30 格无实心 → 取反;collideX → `ai[0] = -ai[0]+π; velocity.X*=-0.2`。
- 陆行(48036-48075):先查前方 1 格向下 4 格有水 → 起飞回 ai[2]=0;`velocity.Y!=0` 时 X 衰减 0.98、Y Lerp 到 2;落地后 `velocity → Lerp(UnitX×direction, 0.05)` + `velocity.Y+=0.2`(一跳一跳),collideX → `direction*=-1; velocity.X*=-0.2`。
- 状态切换:每 60-180 帧 1/5 概率切换飞/陆;落陆时 `ai[0]=随机全角`,玩家 700px 外时改为朝玩家角 ±0.3(漂向玩家)。

## 10. aiStyle 116 水黾(612 WaterStrider/613 Gold,AI_116_WaterStriders 47882)
- 贴水面:`Collision.GetWaterLine` 取本 tile 列水面 Y;`Center.Y > 水面` → `velocity.Y-=0.8`(下限 -4),越界钳制 `velocity.Y = 水面-(Bottom-1)`;`Center.Y <= 水面` → `velocity.Y = min(velocity.Y, 水面-(Bottom-1))` 并置 flag(在水面)。无水线但 wet → `velocity.Y-=0.2`(47884-47909)。
- 移动(47910-47941):`ai[0]!=0` 直接 return(其余态不在此);`ai[1]+=1` 计时,`velocity.X*=0.9`,着地再 ×0.6。每 120-240 帧(不在水面/未 wet 时 60-240)触发一次:`velocity.X = 随机方向×5`;若当时不在水面上且着地 → 顺带 `velocity.Y=-2` 起跳,并重置 `ai[1]=60`。

## 11. aiStyle 118 海马(626 Seahorse/627 Gold,AI_118_Seahorses 47432)
- `ai[0]`=游动方向角,`ai[1]`=冲刺冷却;`noGravity = wet`(离水才受重力)。
- 离水:`velocity.Y==0` 时 `velocity.X*=0.95`,`rotation += (vx+vy)/2×0.05`(瘫软扭动)。
- 水中:`ai[1]--`;归零时沿 `ai[0]` 方向 `velocity += 方向×0.06`,若合速度超 ±3 → 重新随机 `ai[0]=NextFloat×2π`、`ai[1]=Next(450,600)`;接近水面(`Top.Y-水线<20`)时新角度若朝下(>π)减 π 折回(47456-47459)。非冲刺帧 `velocity*=0.95`,`rotation=velocity.X×0.1`。
- 碰撞(47470-47485):collideX → 反射 ai[0] 的 X;着水底且(远离水面或正在下潜)→ 反射 Y;`velocity = 新方向×原速度`,netUpdate。

## 12. aiStyle 1 蚱蜢(377 Grasshopper/446 GoldGrasshopper,在 AI_001_Slimes 60735 内)
- 已知 ai[0]+3 之外还有 4 处差异:
  1. **受惊激活**(61479-61483):`flag3`(强制跳)在 `target 有效且玩家距离 ≤200px 且 !wet` 时置真——蚱蜢看到人才蹦,平时走路档(走路档速度 0.2/帧)。
  2. **friendly 窗口**(61854-61864):`localAI[2]<90` 时递增,满 90 帧 → `friendly=false`。即刚被放出/出生 1.5 秒内不与玩家敌对(蚱蜢 damage>0,会咬人)。
  3. **跳跃力衰减**(62088-62102):跳起时(`velocity.Y*=-1` 那支为 -6/-8 档)蚱蜢 `velocity.Y*=0.9; velocity.X*=0.6`,且若 flag3(受惊)则 `direction=-direction; velocity.X*=-1` 反向逃;头上 1 格实心且 `-velocity.Y+height>16` → `velocity.Y=-(16-height)` 防卡顶。
  4. **冷却加速**(61994-61997):落地后 `ai[0]+=3`(比普通史莱姆 +5 慢,蹦得更稀)。
- 受击反应:无专属;与其他 slime 一样共用通用 StrikeNPC 流程。

## 13. aiStyle 16 鱼类小动物(55 Goldfish/592 GoldGoldfish/607 Pupfish/615 Dolphin/688 Pufferfish,23549 起)
- **688 河鲀膨胀**(23555-23620):`justHit && ai[2]==0` → `ai[2]=1`(膨胀),`localAI[0]=180` 倒计时;每 120 帧复查,挨打期间保持膨胀。膨胀态:`velocity*=0.98`,贴水面悬浮(同 116 的 GetWaterLine 钉法,Y 上限 -2/0);wet 无水线 → `velocity.Y-=0.3`(限 -10);离水 → `+0.3`(限 10)。膨胀态 `return`,不吃后面的通用鱼逻辑。
- **615 海豚**(23629-23747):`ai[2]`=0 巡游 / 1 跃出 / 2 潜游贴面;`ai[3]`=阶段计时。每 300-1199 帧(`ai[3]` 累计)触发:1/2 概率跃出(若头顶 128px 内被挡改潜游)。跃出态:湿 → `velocity.Y-=0.4`(限 -6),`rotation=velocity.Y×direction×0.3` 钳 ±2π/5,出水后 `rotation+=direction×0.2; velocity.Y+=0.3`(限 10)即抛物线跳;撞墙撞地立即回 0。潜游态:湿 → 贴水线(`GetWaterLine`,`velocity.Y=钳(水线-position.Y, -2, 0.5)`,`rotation=-π/5×direction`,`velocity.X*=0.95`),ai[3]>=300 → 收尾 `velocity.Y=4` 沉回;ai[3]==60 时 1/2 播 SoundID 45。
- **通用水中游**(23758 起):55/592/607/615/688 **不参与**"玩家同水则逃离"检测(flag22 排除,23758-23768),其他鱼(65/102/157/692 等)玩家 wet 且 CanHit 时朝反方向游。坡面强制顺坡(direction 由 topSlope 决定)。collideX → `velocity.X*=-1; direction*=-1`;collideY → Y 反弹并翻 directionY、`ai[0]=±1`。慢速游:`velocity.X+=direction×0.1`(钳 ±3),`ai[0]` 在 ±0.3 之间摆动做 Y 浮沉;dolphin X 上限 3。liquid>128 且下方 1-2 格 active → `ai[0]=-1` 上浮。`rotation=velocity.Y×direction×0.1` 钳 ±0.2。
- **离水拍打**(24019-24039):`velocity.Y==0` 时 65/692 只 `velocity.X*=0.94`;**其余(含 55 金鱼)随机 `velocity.Y=Next(-50,-20)×0.1, velocity.X=Next(-20,20)×0.1`,随机 direction**(拍打乱跳),然后 `velocity.Y+=0.3`(限 10),`ai[0]=1`。金鱼没有专属"拍打动画"AI,就是这个随机弹跳。

## 共同陷阱
- **Catchable 不在 AI 内**:`Main.npcCatchable[type]` 与 `catchItem` 都在 `SetDefaults` 设置(NPC.cs 17786 一带);捕捉判定走虫网投射物与 `CanReleaseNPCs`(80907);放生短暂无敌在 `SubAI_HandleTemporaryCatchableNPCPlayerInvulnerability`(91588)。AI 层只读不写。
- **白天消失是伪命题**:这 13 族没有任何一处在 `Main.dayTime` 时 `active=false`。萤火虫族只是白天停止发光(AI_064 34419 条件);唯一环境消失的是 661 EmpressButterfly(离开神圣渐隐,且逻辑是"距玩家/非神圣区"而非昼夜)。"白天/夜晚刷什么"完全在 spawner 侧。
- **wet 是每帧由 Collision 算出的标志**,不是存档字段;多族用 `wet` 做分支(7 青蛙/乌龟、16 全族、66、68、112),移植时必须先跑 wet/碰撞更新再进 AI。
- **noGravity/noTileCollide 是 per-type 默认**(SetDefaults 各分支,如 8646/8662/…),不是按 aiStyle 批量设置;只有 67(爬壁时 true/逃跑时 false)、68(状态切换)、118(`noGravity=wet`)在 AI 内动态改。漏了 per-type 默认会导致萤火虫直接坠落。
- **随机 scale 存在 ai[3] 并写回 `npc.scale`**(64/65/115/67 的 359),且 65 用 `ai[2]` 存蝴蝶花色(影响 catchItem),存档必须持久化 ai/localAI,否则重进世界变体丢失。
- **Transform 成对链**:7 族 362↔363、364↔365、602↔603、608↔609(wet/落速触发去 68 飞形,68 落地 `Transform(type-1, 0, ai[1]=200+Next(200))` 回来);66 族 374→375。Transform 会重置 ai,注意保留 netUpdate 与 ai[1] 初值。
- **多人语义**:几乎所有重选/状态切换都包 `Main.netMode != 1`,客户端只做插值;写 JS 版时要区分"权威帧逻辑"与"纯视觉逻辑",否则会出现双端各自随机漂移。
- 危险感知半径:`NPCID.Sets.DangerDetectRange[type]`,默认 -1 → 取 200;`PrettySafe` 阈值可豁免远处威胁(AI_007 内 flag16 派生逃跑)。
- 反编译里不存在 `CountsAsCritter`/`stoneDefense`(任务书提到的名字),对应物分别是 `NPCID.Sets.TownCritter` 与 per-type `defense`/`dontTakeDamage`;别按 1.4.0 旧字段名移植。
```
