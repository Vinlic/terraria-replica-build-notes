# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-13T10:01:52.183Z

```
你在 ~/Project/GLM/SandboxWorld/ 项目（工作目录 game/）。Terraria 复刻，1:1 对齐 Terarria1456/。**只读调查**（禁止修改）。用户实测：**城镇 NPC 自己住进了地下世界生成时就有的房子**（地下小屋/神龛等天然结构），不是玩家建的——核实原版语义与本仓现状，判断是否 bug。

调查线：
1. **原版语义**（权威）：原版 NPC 入住（TownRoomManager.cs / WorldGen.ScoreRoom / Housing.cs）——天然地下小屋（CaveHousePass 生成的）**能否**成为合法住房？原版判定核心：房间必须有玩家放置的"房屋墙"（wallHouse 表）还是天然墙也行？**关键事实预期**：原版要求背景墙必须是"房屋墙"且很多天然墙不合格；且原版房间必须**在特定条件**（如无 boss、非地下特殊区）。查：原版 ScoreRoom 对墙的判定（WorldGen.cs ScoreRoom :5804-5940 附近，wallHouse/CanEnemyRoom）+ 是否有"房间位置"限制（如必须靠近出生点/地表？）。特别注意原版 **天然地下小屋的墙**（土墙/石墙 vs 木墙）：CaveHousePass 生成的小屋用什么墙（cs:17159 AddBuriedChest 区域附近的小屋生成），这些墙在 wallHouse 表里吗？如果原版地下小屋墙**是**房屋墙且原版 NPC **能**住进去——那用户看到的是原版正确行为；如果不能——本仓 Housing 判定比原版宽松，是 bug。
2. **本仓现状**：src/world/Housing.ts（ScoreRoom 移植——波 6b 批做过全维度 1:1：候选地板/杂物/邪恶度/占用）——查它对墙的判定与原版差异：是否漏了 wallHouse 门（grep wallHouse/HousingWalls）；town-npc 入驻轮（Game.ts updateTownNpcArrival 附近）的候选房间来源（findFreeHouse 扫描范围——是否全图扫含地下）。
3. **CaveHousePass 墙型**：src/world/gen/vanilla/CaveHousePass.ts 小屋生成的墙 id——对照 WALL_HOUSE 表（VanillaSpawner.ts:107）与原版 wallHouse。
4. 结论三选一：A=原版行为（生成房墙是合法房屋墙+原版可住）→ 如实报告无需修；B=本仓判定偏差（缺 wallHouse 门/扫描范围过宽）→ 给出精确修复点；C=需要更多事实（列出待查项）。

产出 ≤30 行：原版事实/本仓差异点（文件:行）/结论 A/B/C + 修复建议（若 B）。
```

---

## 📎 Attachment · skill_listing · 2026-08-13T10:01:52.189Z

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

## 🤖 Assistant · 2026-08-13T10:01:58.255Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me investigate this. I need to:

1. Find the original Terraria source (Terraria1456/) - check ScoreRoom in WorldGen.cs, wallHouse table, CaveHousePass generation
2. Check this repo's Housing.ts implementation
3. Check CaveHousePass.ts wall types
4. Check WALL_HOUSE table in VanillaSpawner.ts
5. Check Game.ts updateTownNpcArrival / findFreeHouse scan range

Let me start with parallel searches.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:01:58.258Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/ 2>/dev/null; echo ---; ls ~/Project/GLM/SandboxWorld/game/src/world/ 2>/dev/null; echo ---; ls ~/Project/GLM/SandboxWorld/Terarria1456/ 2>/dev/null | head -30",
 "description": "List project directories"
}
```


---

## 🤖 Assistant · 2026-08-13T10:01:58.279Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"wallHouse\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs | head -20; echo ===; grep -rn \"wallHouse\" ~/Project/GLM/SandboxWorld/game/src --include=*.ts | head -30",
 "description": "Search wallHouse in original and repo"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:01:58.360Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:5347:		if (Main.wallHouse[Main.tile[x, y].wall])
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:6154:			if (Main.wallHouse[Main.tile[x + i, y].wall])
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:6162:			if (Main.wallHouse[Main.tile[x, y + i].wall])
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:17940:						if (!Main.wallHouse[Main.tile[num11, num12].wall] && Main.tile[num11, num12].wall != 244)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:20416:										if (Main.tile[l, m].liquid > 0 || Main.wallHouse[Main.tile[l, m].wall])
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:20465:										if (Main.tile[num6, num7].liquid > 0 || Main.wallHouse[Main.tile[num6, num7].wall])
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:52298:			if (Main.tile[x, y].wall == 0 || Main.wallHouse[Main.tile[x, y].wall])
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:52302:			if (Main.tile[x - 1, y].wall == 0 || Main.wallHouse[Main.tile[x - 1, y].wall])
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:52306:			if (Main.tile[x + 1, y].wall == 0 || Main.wallHouse[Main.tile[x + 1, y].wall])
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:52310:			if (Main.tile[x, y - 1].wall == 0 || Main.wallHouse[Main.tile[x, y - 1].wall])
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:52314:			if (Main.tile[x, y + 1].wall == 0 || Main.wallHouse[Main.tile[x, y + 1].wall])
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:70860:			while (!Main.wallHouse[Main.tile[num40, num41].wall] || Main.tile[num40, num41].active())
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:70883:				while (!Main.tile[num42, num41].active() && Main.wallHouse[Main.tile[num42, num41].wall])
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:70888:				for (; !Main.tile[num43, num41].active() && Main.wallHouse[Main.tile[num43, num41].wall]; num43++)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:70895:				while (!Main.tile[num40, num44].active() && Main.wallHouse[Main.tile[num40, num44].wall])
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:70900:				for (; !Main.tile[num40, num45].active() && Main.wallHouse[Main.tile[num40, num45].wall]; num45++)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:71672:				if (Main.wallHouse[Main.tile[point.X, point.Y].wall])
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:73570:					if (Main.tile[k, num16].liquid > 0 || Main.wallHouse[Main.tile[k, num16].wall])
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:73639:					if (Main.tile[num20, num21].liquid > 0 || Main.wallHouse[Main.tile[num20, num21].wall])
(eval):1: == not found

```


---

## 👤 User(sidechain) · 2026-08-13T10:01:58.367Z

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
---
audit
Banners.ts
BossSummonStations.ts
Door.ts
Eclipse.ts
evolution
Extractinator.ts
FurnitureItems.ts
FurnitureStyle.ts
gen
golf
hive.ts
Housing.ts
Invasion.ts
LanternNight.ts
liquid
LunarEvent.ts
MeteorFall.ts
MinecartTrack.ts
MoonEvent.ts
OldOnesArmy.ts
Paint.ts
SceneMetrics.ts
spawn
TeleportPylons.ts
TileStore.ts
Torch.ts
TorchGod.ts
weather
wiring
Wiring.ts
World.ts
WorldAlignment.ts
---
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

## 🤖 Assistant · 2026-08-13T10:02:02.635Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting - line 6154/6162 in WorldGen.cs is within ScoreRoom area. Let me look at the ScoreRoom function in the original. The user said ScoreRoom :5804-5940 but the wallHouse refs are at 6154. Let me find ScoreRoom definition.

Also need Main.wallHouse initialization - where it's set (Main.cs). Let me search.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:02:03.486Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"public static.*ScoreRoom\\|bool ScoreRoom\\|ScoreRoom(\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs | head; echo ---; grep -rn \"wallHouse\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head -30",
 "description": "Find ScoreRoom and wallHouse init"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:02:03.821Z

**📎 ToolResult**

```
4749:		ScoreRoom(-1, type, feedback);
5371:		ScoreRoom(-1, num);
5701:					ScoreRoom(npc, Main.npc[npc].type);
5747:	private static bool ScoreRoom_IsThisRoomOccupiedBySomeone(int ignoreNPC = -1, int npcTypeAsking = -1)
5804:	public static void ScoreRoom(int ignoreNPC = -1, int npcTypeAskingToScoreRoom = -1, IRoomCheckFeedback feedback = null)
5967:	private static bool ScoreRoom_CanBeHomeSpot(int x, int y)
---
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:1431:	public static bool[] wallHouse = new bool[WallID.Count];
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9651:		wallHouse[224] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9653:		wallHouse[323] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9655:		wallHouse[324] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9657:		wallHouse[325] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9659:		wallHouse[326] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9661:		wallHouse[327] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9663:		wallHouse[328] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9665:		wallHouse[329] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9667:		wallHouse[330] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9669:		wallHouse[331] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9670:		wallHouse[332] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9671:		wallHouse[333] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9672:		wallHouse[334] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9673:		wallHouse[335] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9674:		wallHouse[336] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9675:		wallHouse[337] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9676:		wallHouse[338] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9677:		wallHouse[339] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9678:		wallHouse[340] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9679:		wallHouse[341] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9680:		wallHouse[342] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9681:		wallHouse[343] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9682:		wallHouse[344] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9683:		wallHouse[345] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9684:		wallHouse[346] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9685:		wallHouse[60] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9686:		wallHouse[225] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9687:		wallHouse[226] = true;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:9688:		wallHouse[227] = true;

```


---

## 🤖 Assistant · 2026-08-13T10:02:03.992Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"wallHouse\\|HOUSING_WALL\\|HousingWall\\|isHouseWall\\|wallHouse\" ~/Project/GLM/SandboxWorld/game/src --include=*.ts | head -40",
 "description": "Search wallHouse equivalent in repo"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:02:04.145Z

**📎 ToolResult**

```
(eval):1: no matches found: --include=*.ts

```


---

## 🤖 Assistant · 2026-08-13T10:02:08.486Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
zsh glob issue with `--include=*.ts`. Use quotes. Let me read ScoreRoom original 5804-5980 and Main.cs 9640-9740 for full wallHouse list.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:02:12.929Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs",
 "limit": 175,
 "offset": 5804
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:02:12.947Z

**📎 ToolResult**

```
5804		public static void ScoreRoom(int ignoreNPC = -1, int npcTypeAskingToScoreRoom = -1, IRoomCheckFeedback feedback = null)
5805		{
5806			if (feedback == null)
5807			{
5808				feedback = NoRoomCheckFeedback.WithText;
5809			}
5810			roomOccupied = false;
5811			roomHasStandingSpace = false;
5812			roomEvil = false;
5813			sharedRoomX = -1;
5814			if (ScoreRoom_IsThisRoomOccupiedBySomeone(ignoreNPC, npcTypeAskingToScoreRoom))
5815			{
5816				roomOccupied = true;
5817				hiScore = -1;
5818				return;
5819			}
5820			hiScore = 0;
5821			int num = 0;
5822			int num2 = 50;
5823			Housing_GetTestedRoomBounds(out var startX, out var endX, out var startY, out var endY);
5824			int[] tileTypeCounts = new int[TileID.Count];
5825			CountTileTypesInArea(tileTypeCounts, startX + 1, endX - 1, startY + 2, endY + 1);
5826			int num3 = -GetTileTypeCountByCategory(tileTypeCounts, TileScanGroup.TotalGoodEvil);
5827			if (num3 < 50)
5828			{
5829				num3 = 0;
5830			}
5831			num2 -= num3;
5832			if (num3 > 0)
5833			{
5834				roomEvil = true;
5835			}
5836			if (num2 <= -250)
5837			{
5838				hiScore = num2;
5839				return;
5840			}
5841			startX = roomX1;
5842			endX = roomX2;
5843			startY = roomY1;
5844			endY = roomY2;
5845			for (int i = startX + 1; i < endX; i++)
5846			{
5847				for (int j = startY + 2; j < endY + 2; j++)
5848				{
5849					if (!Main.tile[i, j].nactive() || !ScoreRoom_CanBeHomeSpot(i, j) || !Main.tileSolid[Main.tile[i, j].type] || Collision.SolidTiles(i - 1, i + 1, j - 3, j - 1) || !Main.tile[i - 1, j].nactive() || !Main.tileSolid[Main.tile[i - 1, j].type] || !Main.tile[i + 1, j].nactive() || !Main.tileSolid[Main.tile[i + 1, j].type])
5850					{
5851						continue;
5852					}
5853					num = num2;
5854					int num4 = 0;
5855					int num5 = 0;
5856					for (int k = i - 2; k < i + 3; k++)
5857					{
5858						for (int l = j - 4; l < j; l++)
5859						{
5860							Tile tile = Main.tile[k, l];
5861							if (tile.nactive() && !TileID.Sets.IgnoredInHouseScore[tile.type] && (tile.type != 11 || IsOpenDoorAnchorFrame(k, l)))
5862							{
5863								if (k == i)
5864								{
5865									num4++;
5866								}
5867								else if (TileID.Sets.BasicChest[tile.type])
5868								{
5869									num5++;
5870								}
5871								else
5872								{
5873									num = ((tile.type != 10 && tile.type != 388) ? ((!IsOpenDoorAnchorFrame(k, l) && tile.type != 389) ? ((!Main.tileSolid[tile.type]) ? (num + 5) : (num - 5)) : (num - 20)) : (num - 20));
5874								}
5875							}
5876						}
5877					}
5878					if (num > 0)
5879					{
5880						roomHasStandingSpace = true;
5881					}
5882					if (sharedRoomX >= 0 && num >= 1 && Math.Abs(sharedRoomX - i) < 3)
5883					{
5884						num = 1;
5885					}
5886					if (num > 0 && num5 > 0)
5887					{
5888						num -= 30 * num5;
5889						if (num < 1)
5890						{
5891							num = 1;
5892						}
5893					}
5894					if (num > 0 && num4 > 0)
5895					{
5896						num -= 15 * num4;
5897						if (num < 1)
5898						{
5899							num = 1;
5900						}
5901					}
5902					feedback.ReportScore(i, j, num);
5903					if (num <= hiScore)
5904					{
5905						continue;
5906					}
5907					bool flag = Housing_CheckIfInRoom(i, j);
5908					bool[] array = new bool[3];
5909					for (int m = 1; m <= 3; m++)
5910					{
5911						if (!Main.tile[i, j - m].active() || !Main.tileSolid[Main.tile[i, j - m].type])
5912						{
5913							array[m - 1] = true;
5914						}
5915						if (!Housing_CheckIfInRoom(i, j - m))
5916						{
5917							array[m - 1] = false;
5918						}
5919					}
5920					bool[] array2 = array;
5921					for (int n = 0; n < array2.Length; n++)
5922					{
5923						if (!array2[n])
5924						{
5925							flag = false;
5926							break;
5927						}
5928					}
5929					if (flag && Housing_CheckIfInRoom(i, j - 1))
5930					{
5931						feedback.SetAsHighScore(i, j, num);
5932						hiScore = num;
5933						bestX = i;
5934						bestY = j;
5935					}
5936				}
5937			}
5938		}
5939	
5940		public static void Housing_GetTestedRoomBounds(out int startX, out int endX, out int startY, out int endY)
5941		{
5942			int num = 40;
5943			int num2 = 5;
5944			int num3 = 3;
5945			startX = roomX1 - num2 - 1 - num;
5946			endX = roomX2 + num2 + 1 + num;
5947			startY = roomY1 - num3 - 1 - num;
5948			endY = roomY2 + num3 + 1 + num;
5949			if (startX < 5)
5950			{
5951				startX = 5;
5952			}
5953			if (endX >= Main.maxTilesX - 5)
5954			{
5955				endX = Main.maxTilesX - 6;
5956			}
5957			if (startY < 5)
5958			{
5959				startY = 5;
5960			}
5961			if (endY >= Main.maxTilesY - 5)
5962			{
5963				endY = Main.maxTilesY - 6;
5964			}
5965		}
5966	
5967		private static bool ScoreRoom_CanBeHomeSpot(int x, int y)
5968		{
5969			Tile tile = Main.tile[x, y];
5970			if (tile.active())
5971			{
5972				ushort type = tile.type;
5973				if (type == 379)
5974				{
5975					return false;
5976				}
5977			}
5978			return true;

```


---

## 🤖 Assistant · 2026-08-13T10:02:12.948Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "limit": 100,
 "offset": 9645
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:02:12.965Z

**📎 ToolResult**

```
9645			tileFrameImportant[296] = true;
9646			tileFrameImportant[297] = true;
9647			tileFrameImportant[316] = true;
9648			tileFrameImportant[317] = true;
9649			tileFrameImportant[318] = true;
9650			tileLargeFrames[284] = 1;
9651			wallHouse[224] = true;
9652			wallLargeFrames[224] = 2;
9653			wallHouse[323] = true;
9654			wallLargeFrames[323] = 2;
9655			wallHouse[324] = true;
9656			wallLargeFrames[324] = 2;
9657			wallHouse[325] = true;
9658			wallLargeFrames[325] = 2;
9659			wallHouse[326] = true;
9660			wallLargeFrames[326] = 2;
9661			wallHouse[327] = true;
9662			wallLargeFrames[327] = 2;
9663			wallHouse[328] = true;
9664			wallLargeFrames[328] = 2;
9665			wallHouse[329] = true;
9666			wallLargeFrames[329] = 2;
9667			wallHouse[330] = true;
9668			wallLargeFrames[330] = 2;
9669			wallHouse[331] = true;
9670			wallHouse[332] = true;
9671			wallHouse[333] = true;
9672			wallHouse[334] = true;
9673			wallHouse[335] = true;
9674			wallHouse[336] = true;
9675			wallHouse[337] = true;
9676			wallHouse[338] = true;
9677			wallHouse[339] = true;
9678			wallHouse[340] = true;
9679			wallHouse[341] = true;
9680			wallHouse[342] = true;
9681			wallHouse[343] = true;
9682			wallHouse[344] = true;
9683			wallHouse[345] = true;
9684			wallHouse[346] = true;
9685			wallHouse[60] = true;
9686			wallHouse[225] = true;
9687			wallHouse[226] = true;
9688			wallHouse[227] = true;
9689			wallHouse[231] = true;
9690			wallHouse[232] = true;
9691			wallHouse[233] = true;
9692			wallHouse[235] = true;
9693			wallHouse[234] = true;
9694			wallHouse[312] = true;
9695			wallHouse[313] = true;
9696			wallHouse[237] = true;
9697			wallHouse[238] = true;
9698			wallHouse[239] = true;
9699			wallHouse[240] = true;
9700			tileLargeFrames[409] = 2;
9701			tileLargeFrames[669] = 2;
9702			tileLargeFrames[670] = 2;
9703			tileLargeFrames[671] = 2;
9704			tileLargeFrames[672] = 2;
9705			tileLargeFrames[673] = 2;
9706			tileLargeFrames[674] = 2;
9707			tileLargeFrames[675] = 2;
9708			tileLargeFrames[676] = 2;
9709			tileFrameImportant[410] = true;
9710			tileFrameImportant[480] = true;
9711			tileFrameImportant[509] = true;
9712			tileFrameImportant[657] = true;
9713			tileFrameImportant[658] = true;
9714			tileLighted[658] = true;
9715			tileFrameImportant[720] = true;
9716			tileFrameImportant[721] = true;
9717			tileFrameImportant[725] = true;
9718			tileFrameImportant[733] = true;
9719			tileFrameImportant[751] = true;
9720			tileFrameImportant[752] = true;
9721			wallHouse[173] = true;
9722			wallHouse[183] = true;
9723			wallHouse[179] = true;
9724			wallLargeFrames[179] = 1;
9725			tileSolid[367] = true;
9726			tileBlockLight[367] = true;
9727			tileMergeDirt[367] = true;
9728			tileSolid[357] = true;
9729			tileBlockLight[357] = true;
9730			tileLargeFrames[357] = 1;
9731			tileBlendAll[357] = true;
9732			wallHouse[184] = true;
9733			wallHouse[181] = true;
9734			tileSolid[368] = true;
9735			tileBlockLight[368] = true;
9736			tileMergeDirt[368] = true;
9737			tileSolid[369] = true;
9738			tileBlockLight[369] = true;
9739			tileBrick[369] = true;
9740			tileMergeDirt[369] = true;
9741			wallHouse[186] = true;
9742			tileLargeFrames[325] = 1;
9743			tileSolid[325] = true;
9744			tileBlockLight[325] = true;

```


---

## 🤖 Assistant · 2026-08-13T10:02:18.547Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Need to see the full wallHouse list - it's spread out. Let me grep all wallHouse assignments in Main.cs. And I need Housing_CheckIfInRoom which is the key room-validity function (walls!). Let me find Housing_CheckIfInRoom in WorldGen.cs — that's where wallHouse[wall] check happens (line 5347?). Let's check line 5347 context and find where walls are validated in the room check.

Actually key: the room validity check for housing is in Housing_CheckIfInRoom (WorldGen.cs:~52100-52320 based on the wallHouse hits at 52298-52314). Let me read that.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:02:19.401Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"Housing_CheckIfInRoom\\|Housing_CheckSolidSpot\\|Housing_KickOut\\|roomClosed\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs | head -20; echo ---; grep -c \"wallHouse\\[\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "description": "Locate Housing_CheckIfInRoom"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:02:19.471Z

**📎 ToolResult**

```
5752:			if (nPC.active && nPC.townNPC && ignoreNPC != i && !nPC.homeless && Housing_CheckIfInRoom(nPC.homeTileX, nPC.homeTileY) && Housing_CheckIfInRoom(nPC.homeTileX, nPC.homeTileY - 1))
5907:				bool flag = Housing_CheckIfInRoom(i, j);
5915:					if (!Housing_CheckIfInRoom(i, j - m))
5929:				if (flag && Housing_CheckIfInRoom(i, j - 1))
5981:	private static bool Housing_CheckIfInRoom(int i, int j)
---
268

```


---

## 🤖 Assistant · 2026-08-13T10:02:19.771Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs",
 "limit": 120,
 "offset": 52240
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:02:19.781Z

**📎 ToolResult**

```
52240			}
52241			bool flag = true;
52242			for (int i = x - 1; i < x + 1; i++)
52243			{
52244				for (int j = y - 1; j < y + 1; j++)
52245				{
52246					if (Main.tile[i, j] == null)
52247					{
52248						Main.tile[i, j] = new Tile();
52249					}
52250					if (Main.tile[i, j].active())
52251					{
52252						flag = false;
52253					}
52254				}
52255				if (Main.tile[i, y + 1] == null)
52256				{
52257					Main.tile[i, y + 1] = new Tile();
52258				}
52259				if (!SolidTile(i, y + 1))
52260				{
52261					flag = false;
52262				}
52263				if (type == 254 && Main.tile[i, y + 1].type != 2 && Main.tile[i, y + 1].type != 477 && Main.tile[i, y + 1].type != 492 && Main.tile[i, y + 1].type != 109)
52264				{
52265					flag = false;
52266				}
52267			}
52268			if (flag)
52269			{
52270				short num2 = (short)(36 * style);
52271				Main.tile[x - 1, y - 1].active(active: true);
52272				Main.tile[x - 1, y - 1].frameY = num;
52273				Main.tile[x - 1, y - 1].frameX = num2;
52274				Main.tile[x - 1, y - 1].type = type;
52275				Main.tile[x, y - 1].active(active: true);
52276				Main.tile[x, y - 1].frameY = num;
52277				Main.tile[x, y - 1].frameX = (short)(num2 + 18);
52278				Main.tile[x, y - 1].type = type;
52279				Main.tile[x - 1, y].active(active: true);
52280				Main.tile[x - 1, y].frameY = (short)(num + 18);
52281				Main.tile[x - 1, y].frameX = num2;
52282				Main.tile[x - 1, y].type = type;
52283				Main.tile[x, y].active(active: true);
52284				Main.tile[x, y].frameY = (short)(num + 18);
52285				Main.tile[x, y].frameX = (short)(num2 + 18);
52286				Main.tile[x, y].type = type;
52287			}
52288		}
52289	
52290		public static bool NearFriendlyWall(int x, int y)
52291		{
52292			try
52293			{
52294				if (x < 2 || x >= Main.maxTilesX - 2 || y < 2 || y >= Main.maxTilesY - 2)
52295				{
52296					return true;
52297				}
52298				if (Main.tile[x, y].wall == 0 || Main.wallHouse[Main.tile[x, y].wall])
52299				{
52300					return true;
52301				}
52302				if (Main.tile[x - 1, y].wall == 0 || Main.wallHouse[Main.tile[x - 1, y].wall])
52303				{
52304					return true;
52305				}
52306				if (Main.tile[x + 1, y].wall == 0 || Main.wallHouse[Main.tile[x + 1, y].wall])
52307				{
52308					return true;
52309				}
52310				if (Main.tile[x, y - 1].wall == 0 || Main.wallHouse[Main.tile[x, y - 1].wall])
52311				{
52312					return true;
52313				}
52314				if (Main.tile[x, y + 1].wall == 0 || Main.wallHouse[Main.tile[x, y + 1].wall])
52315				{
52316					return true;
52317				}
52318			}
52319			catch
52320			{
52321			}
52322			return false;
52323		}
52324	
52325		public static void Check2x2Style(int i, int j, int type)
52326		{
52327			if (destroyObject)
52328			{
52329				return;
52330			}
52331			bool flag = false;
52332			int num = j;
52333			int num2;
52334			for (num2 = Main.tile[i, j].frameY / 18; num2 > 1; num2 -= 2)
52335			{
52336			}
52337			num -= num2;
52338			int num3 = Main.tile[i, j].frameX / 18;
52339			int num4 = 0;
52340			while (num3 > 1)
52341			{
52342				num3 -= 2;
52343				num4++;
52344			}
52345			num3 = i - num3;
52346			int num5 = num4 * 36;
52347			for (int k = num3; k < num3 + 2; k++)
52348			{
52349				for (int l = num; l < num + 2; l++)
52350				{
52351					if (Main.tile[k, l] == null)
52352					{
52353						Main.tile[k, l] = new Tile();
52354					}
52355					if (!Main.tile[k, l].active() || Main.tile[k, l].type != type || Main.tile[k, l].frameX != (k - num3) * 18 + num5)
52356					{
52357						flag = true;
52358					}
52359				}

```


---

## 🤖 Assistant · 2026-08-13T10:02:20.873Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now read Housing_CheckIfInRoom at 5981 — the core room enclosure check.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:02:21.140Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs",
 "limit": 115,
 "offset": 5981
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:02:21.151Z

**📎 ToolResult**

```
5981		private static bool Housing_CheckIfInRoom(int i, int j)
5982		{
5983			Point p = new Point(i, j);
5984			if (roomTiles.InBounds(p))
5985			{
5986				return roomTiles[p];
5987			}
5988			return false;
5989		}
5990	
5991		public static bool StartRoomCheck(int x, int y, IRoomCheckFeedback feedback = null)
5992		{
5993			if (feedback == null)
5994			{
5995				feedback = NoRoomCheckFeedback.WithText;
5996			}
5997			roomHasStinkbug = false;
5998			roomHasEchoStinkbug = false;
5999			roomX1 = x;
6000			roomX2 = x;
6001			roomY1 = y;
6002			roomY2 = y;
6003			roomTiles.Reset(new Point(x, y), maxRoomSize);
6004			numRoomTiles = 0;
6005			for (int i = 0; i < TileID.Count; i++)
6006			{
6007				houseTile[i] = false;
6008			}
6009			canSpawn = true;
6010			if (x < 10 || y < 10 || x >= Main.maxTilesX - 10 || y >= lastMaxTilesY - 10)
6011			{
6012				feedback.TooCloseToWorldEdge(x, y, 0);
6013				roomCheckFailureReason = TownNPCRoomCheckFailureReason.TooCloseToWorldEdge;
6014				canSpawn = false;
6015				return false;
6016			}
6017			if (Main.tile[x, y].nactive() && Main.tileSolid[Main.tile[x, y].type])
6018			{
6019				feedback.StartedInASolidTile(x, y);
6020				roomCheckFailureReason = TownNPCRoomCheckFailureReason.RoomCheckStartedInASolidTile;
6021				canSpawn = false;
6022				return false;
6023			}
6024			roomCheckFailureReason = TownNPCRoomCheckFailureReason.None;
6025			Stack<Point> roomCheckStack = _roomCheckStack;
6026			roomCheckStack.Clear();
6027			roomCheckStack.Push(new Point(x, y));
6028			while (roomCheckStack.Count > 0 && (canSpawn || !feedback.StopOnFail))
6029			{
6030				Point point = roomCheckStack.Pop();
6031				if (!CheckRoom(point.X, point.Y, roomCheckStack.Count, feedback))
6032				{
6033					continue;
6034				}
6035				for (int j = -1; j <= 1; j++)
6036				{
6037					for (int k = -1; k <= 1; k++)
6038					{
6039						if (j != 0 || k != 0)
6040						{
6041							roomCheckStack.Push(new Point(point.X + j, point.Y + k));
6042						}
6043					}
6044				}
6045			}
6046			if (!canSpawn)
6047			{
6048				return false;
6049			}
6050			if (numRoomTiles < 60)
6051			{
6052				roomCheckFailureReason = TownNPCRoomCheckFailureReason.RoomIsTooSmall;
6053				canSpawn = false;
6054				return false;
6055			}
6056			if (canSpawn)
6057			{
6058				return true;
6059			}
6060			return false;
6061		}
6062	
6063		private static bool CheckRoom(int x, int y, int iteration, IRoomCheckFeedback feedback)
6064		{
6065			bool stopOnFail = feedback.StopOnFail;
6066			if (x < 10 || y < 10 || x >= Main.maxTilesX - 10 || y >= lastMaxTilesY - 10)
6067			{
6068				feedback.TooCloseToWorldEdge(x, y, iteration);
6069				roomCheckFailureReason = TownNPCRoomCheckFailureReason.TooCloseToWorldEdge;
6070				canSpawn = false;
6071				return false;
6072			}
6073			if (!roomTiles.InBounds(new Point(x, y)))
6074			{
6075				feedback.RoomTooBig(x, y, iteration);
6076				roomCheckFailureReason = TownNPCRoomCheckFailureReason.RoomIsTooBig;
6077				canSpawn = false;
6078				return false;
6079			}
6080			if (!roomTiles.Add(new Point(x, y)))
6081			{
6082				return false;
6083			}
6084			numRoomTiles++;
6085			if (stopOnFail && numRoomTiles >= maxRoomTiles)
6086			{
6087				feedback.RoomTooBig(x, y, iteration);
6088				roomCheckFailureReason = TownNPCRoomCheckFailureReason.RoomIsTooBig;
6089				canSpawn = false;
6090				return false;
6091			}
6092			if (x < roomX1)
6093			{
6094				roomX1 = x;
6095			}

```


---

## 🤖 Assistant · 2026-08-13T10:02:23.401Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Continue reading CheckRoom - the wall check part. Lines 6095-6170 contain wallHouse checks at 6154/6162.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:02:23.645Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs",
 "limit": 120,
 "offset": 6095
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:02:23.654Z

**📎 ToolResult**

```
6095			}
6096			if (x > roomX2)
6097			{
6098				roomX2 = x;
6099			}
6100			if (y < roomY1)
6101			{
6102				roomY1 = y;
6103			}
6104			if (y > roomY2)
6105			{
6106				roomY2 = y;
6107			}
6108			if (stopOnFail && (roomX2 - roomX1 >= maxRoomSize || roomY2 - roomY1 >= maxRoomSize))
6109			{
6110				feedback.RoomTooBig(x, y, iteration);
6111				roomCheckFailureReason = TownNPCRoomCheckFailureReason.RoomIsTooBig;
6112				canSpawn = false;
6113				return false;
6114			}
6115			feedback.AnyBlockScannedHere(x, y, iteration);
6116			if (Main.tile[x, y].nactive())
6117			{
6118				houseTile[Main.tile[x, y].type] = true;
6119				if (Main.tileSolid[Main.tile[x, y].type])
6120				{
6121					feedback.BlockingWall(x, y, iteration);
6122					return false;
6123				}
6124				if (Main.tile[x, y].type == 11 && (Main.tile[x, y].frameX == 0 || Main.tile[x, y].frameX == 54 || Main.tile[x, y].frameX == 72 || Main.tile[x, y].frameX == 126))
6125				{
6126					feedback.BlockingOpenGate(x, y, iteration);
6127					return false;
6128				}
6129				if (Main.tile[x, y].type == 389)
6130				{
6131					feedback.BlockingOpenGate(x, y, iteration);
6132					return false;
6133				}
6134				if (Main.tile[x, y].type == 386 && ((Main.tile[x, y].frameX < 36 && Main.tile[x, y].frameY == 18) || (Main.tile[x, y].frameX >= 36 && Main.tile[x, y].frameY == 0)))
6135				{
6136					feedback.BlockingOpenGate(x, y, iteration);
6137					return false;
6138				}
6139				if (Main.tile[x, y].type == 630)
6140				{
6141					roomHasStinkbug = true;
6142					feedback.Stinkbug(x, y, iteration);
6143				}
6144				if (Main.tile[x, y].type == 631)
6145				{
6146					roomHasEchoStinkbug = true;
6147					feedback.EchoStinkbug(x, y, iteration);
6148				}
6149			}
6150			bool flag = false;
6151			bool flag2 = false;
6152			for (int i = -2; i < 3; i++)
6153			{
6154				if (Main.wallHouse[Main.tile[x + i, y].wall])
6155				{
6156					flag = true;
6157				}
6158				if (Main.tile[x + i, y].nactive() && (Main.tileSolid[Main.tile[x + i, y].type] || TileID.Sets.HousingWalls[Main.tile[x + i, y].type]))
6159				{
6160					flag = true;
6161				}
6162				if (Main.wallHouse[Main.tile[x, y + i].wall])
6163				{
6164					flag2 = true;
6165				}
6166				if (Main.tile[x, y + i].nactive() && (Main.tileSolid[Main.tile[x, y + i].type] || TileID.Sets.HousingWalls[Main.tile[x, y + i].type]))
6167				{
6168					flag2 = true;
6169				}
6170			}
6171			if (!flag || !flag2)
6172			{
6173				if (Main.tile[x, y].wall > 0)
6174				{
6175					feedback.UnsafeWall(x, y, iteration);
6176					roomCheckFailureReason = TownNPCRoomCheckFailureReason.TooManyUnsafeWalls;
6177				}
6178				else
6179				{
6180					feedback.MissingAWall(x, y, iteration);
6181					roomCheckFailureReason = TownNPCRoomCheckFailureReason.HoleInWallIsTooBig;
6182				}
6183				canSpawn = false;
6184				return false;
6185			}
6186			return true;
6187		}
6188	
6189		public static void StartMeteorShower()
6190		{
6191			meteorShowerCount = genRand.Next(650, 751);
6192			meteorShowerCount *= 4;
6193			ChatHelper.BroadcastChatMessage(NetworkText.FromKey(Lang.gen[92].Key), ChatColors.World);
6194		}
6195	
6196		public static bool dropMeteor(bool spawnUnderGround = false)
6197		{
6198			bool flag = true;
6199			if (!isGeneratingOrLoadingWorld)
6200			{
6201				if (Main.netMode == 1)
6202				{
6203					return false;
6204				}
6205				if (!Main.isThereAWorldSurface)
6206				{
6207					return false;
6208				}
6209				for (int i = 0; i < 255; i++)
6210				{
6211					if (Main.player[i].active)
6212					{
6213						flag = false;
6214						break;

```


---

## 🤖 Assistant · 2026-08-13T10:02:37.063Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I understand the original semantics fully:

**Original CheckRoom (WorldGen.cs:6063-6187)**: For EACH tile in the flood-filled room, it requires that within ±2 tiles horizontally there is at least one "safe" element (wallHouse wall OR solid tile OR TileID.Sets.HousingWalls tile), AND similarly within ±2 vertically. If neither, fail: "TooManyUnsafeWalls" if wall>0 (unsafe natural wall nearby) or "HoleInWallIsTooBig" if wall==0 (no wall at all).

So key fact: **natural walls are NOT automatically disqualifying**. The check is local: a tile is OK if within 2 tiles there's a house wall / solid block / housing-wall tile. So a cave house whose walls are natural dirt walls but enclosed by solid blocks would pass (because solid tiles count as "flag"). Actually wait — the important thing: if the room interior tile has natural wall (e.g., dirt wall id 27? no—cave house interiors), the check requires nearby house wall OR solid tile. In a cave house, interior is hollow; interior tiles have walls placed by gen? Let me check CaveHousePass in original: Terraria.GameContent.Biomes.CaveHouse. The house builder places walls (wood wall etc.) inside.

Let me check original CaveHouseBiome / HouseBuilder to see which wall types they place.

Actually the question of whether original NPCs move into naturally-generated underground houses: **Yes! This is well-known Terraria behavior** — NPCs can and do move into naturally generated structures (underground cabins, living trees, desert caves with walls, floating islands) as long as the room meets housing requirements (light source, comfort, flat surface, door... wait, does the housing check require furniture?).

Hmm, important: modern Terraria housing check (StartRoomCheck + ScoreRoom + houseTile scan) requires: enclosed room with walls, and then the "Housing_CheckIfValid..." Actually there's a separate check for requirements: houseTile[] records tile types in room; then `WorldGen.Housing_CheckIfValid`? Let me search. There's a function that checks for door, table, chair, light: e.g. in NPC.cs townNPC arrival they check `WorldGen.StartRoomCheck` etc. Also "HousingCategoryCheck" / RoomRequirement validation — TileID.Sets.RoomNeed.CountsAsChair etc.

Key question is about the walls, though. And also whether the room must be above ground. There is no "must be near spawn/surface" restriction in original — NPCs happily live in underground houses in vanilla. That's a known vanilla thing: "NPCs can live underground if you build them a valid house underground, and they will also claim naturally generated underground cabins if they're valid."

But are natural underground cabins valid? Their interiors are filled with wood walls? Let me check original CaveHouseBiome HouseBuilder.

Now repo side. Let me check:
- game/src/world/Housing.ts
- CaveHousePass.ts wall ids
- VanillaSpawner.ts:107 WALL_HOUSE
- Game.ts updateTownNpcArrival / findFreeHouse

Let me do these in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:02:37.743Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"class HouseBuilder\\|_wall\\|WallID\\.\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs 2>/dev/null | head -30; echo ---; ls ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/ 2>/dev/null",
 "description": "Inspect original CaveHouse HouseBuilder walls"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:02:37.838Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:12:public class HouseBuilder
---
DesertHouseBuilder.cs
GraniteHouseBuilder.cs
HouseBuilder.cs
HouseBuilderContext.cs
HouseType.cs
HouseUtils.cs
IceHouseBuilder.cs
JungleHouseBuilder.cs
MarbleHouseBuilder.cs
MushroomHouseBuilder.cs
WoodHouseBuilder.cs

```


---

## 🤖 Assistant · 2026-08-13T10:02:38.221Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/game/src/world/Housing.ts; grep -n \"wall\\|Wall\" ~/Project/GLM/SandboxWorld/game/src/world/Housing.ts | head -50",
 "description": "Check repo Housing.ts wall logic"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:02:38.279Z

**📎 ToolResult**

```
     391 ~/Project/GLM/SandboxWorld/game/src/world/Housing.ts
4://   （maxRoomSize，WorldGen.cs:4210/4214）；纯空气格必须有"房墙"（Main.wallHouse 表），
20:/** Main.wallHouse 全表（Main.cs `wallHouse[n] = true` 逐条提取；自然墙全部不在内） */
71:/** TileID.Sets.HousingWalls（TileID.cs:377）：栅栏 11 / 高门 386 / 389 */
275: *  房墙（Main.wallHouse）或 nactive 且 tileSolid/HousingWalls 的 tile。
277:function hasLooseWallEvidence(st: TileStore, x: number, y: number): boolean {
278:  // TileID.Sets.HousingWalls（TileID.cs:377）：11 栅栏 / 386 高门 / 389
279:  const wallLike = (ii: number): boolean => {
280:    if (WALL_HOUSE.has(st.wall[ii])) return true;
286:    if (st.inBounds(x + k, y) && wallLike(st.idx(x + k, y))) horiz = true;
287:    if (st.inBounds(x, y + k) && wallLike(st.idx(x, y + k))) vert = true;
309:    // 房墙或实心/HousingWalls tile（nactive）即算有墙——横竖两向须都有证据
310:    if (!st.flags[i] && !WALL_HOUSE.has(st.wall[i]) && !hasLooseWallEvidence(st, x, y)) return null;

```


---

## 🤖 Assistant · 2026-08-13T10:02:40.368Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good, repo Housing.ts does implement wallHouse gate. Now check:
1. Whether repo WALL_HOUSE table matches original (VanillaSpawner.ts:107).
2. Original CaveHouse wall types - what walls do WoodHouseBuilder etc place? Check HouseBuilder.cs / WoodHouseBuilder.cs.
3. Game.ts findFreeHouse scan range.

Let me read repo Housing.ts fully and original HouseBuilder.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:02:40.697Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/Housing.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:02:40.705Z

**📎 ToolResult**

```
1	// 原版城镇房屋判定（WorldGen.StartRoomCheck / RoomNeeds / ScoreRoom 1:1，
2	// Terarria1456 WorldGen.cs:4600-5350 + 5747-5940）：
3	//   房间 = 门内侧非实心区域泛洪填充，60 ≤ 格数 ≤ 750（maxRoomTiles），包围盒 < 100
4	//   （maxRoomSize，WorldGen.cs:4210/4214）；纯空气格必须有"房墙"（Main.wallHouse 表），
5	//   家具格（实标记非实心 tile）豁免墙判定；门/平台算边界不穿透；
6	//   需求（CountsAsDoor/Table/Chair/Light，WorldGen.RoomNeeds）：
7	//   ≥1 门（扫描锚即门）+ ≥1 桌（含工作台）+ ≥1 椅 + ≥1 光源。
8	//   站位评分 = ScoreRoom 1:1（WorldGen.cs:5804-5940）：
9	//   ① 占用：他人 home 与 home-1 同在房内 → 整房作废（hiScore=-1）；
10	//   ② 邪恶度：房间包围盒向外扩 46 格（Housing_GetTestedRoomBounds ±40+6）扫 tile 计数，
11	//     神圣 +、腐化/猩红 −、向日葵 +5/株，净值 ≥50 才计分（roomEvil），base 50 − 邪恶值；
12	//   ③ 候选地板：nactive+实心+CanBeHomeSpot(非 379 boulder)+上方 3 格无实心+左右实心；
13	//   ④ 头顶 5×4 杂物扫描：非实心 +5 / 实心 −5 / 门(10/388 与开锚 389) −20 /
14	//     基础箱每只 −30 / 正上列每格 −15（均floor到 1）；
15	//   ⑤ 落位校验：地板格与上方 1-3 格都在房内（Housing_CheckIfInRoom）；
16	//   ⑥ 取严格大于的最高分（同分先扫者胜：j 从房顶向下、i 从左向右）。
17	import { T, TILE_DEFS } from '../data/tiles';
18	import type { TileStore } from './TileStore';
19	
20	/** Main.wallHouse 全表（Main.cs `wallHouse[n] = true` 逐条提取；自然墙全部不在内） */
21	export const WALL_HOUSE = new Set([
22	  224, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339,
23	  340, 341, 342, 343, 344, 345, 346, 60, 225, 226, 227, 231, 232, 233, 235, 234, 312, 313,
24	  237, 238, 239, 240, 173, 183, 179, 184, 181, 186, 168, 169, 142, 143, 144, 149, 151, 150,
25	  152, 145, 148, 175, 176, 182, 146, 147, 167, 133, 134, 135, 136, 137, 75, 76, 78, 82, 77,
26	  1, 4, 5, 6, 10, 11, 12, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32,
27	  33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 44, 45, 46, 47, 66, 67, 68, 72, 73, 107, 106, 245,
28	  315, 316, 317, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123,
29	  124, 125, 108, 100, 101, 102, 103, 104, 105, 84, 74, 241, 85, 88, 89, 90, 91, 92, 93, 126,
30	  127, 128, 129, 130, 131, 132, 138, 139, 140, 141, 177, 172, 242, 243, 174, 230, 228, 229,
31	  236, 319, 318, 321, 322, 320, 347, 348, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360,
32	  361, 362, 363, 364, 365, 366, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 314, 256,
33	  257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274,
34	  275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292,
35	  293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310,
36	  311,
37	]);
38	
39	/** 桌家族（CountsAsTable 近似：键名 + 原版 sheet 双保险；工作台计入） */
40	function countsAsTable(key: string, sheet: number | undefined): boolean {
41	  return key.includes('table') || key === 'workbench' || sheet === 14 || sheet === 18;
42	}
43	/** 椅家族（CountsAsChair 近似：椅子/王座；sheet 15=椅 21=王座） */
44	function countsAsChair(key: string, sheet: number | undefined): boolean {
45	  return key.includes('chair') || key.includes('throne') || sheet === 15 || sheet === 21;
46	}
47	
48	const isDoorType = (t: number) => t === T.DOOR_CLOSED || t === T.DOOR_OPEN;
49	
50	/** Main.tileSolid 代理：平台族在原版 tileSolid=true（仅 tileSolidTop 另计），
51	 *  本仓库 defs 把平台记为 platform 而非 solid——ScoreRoom 杂物扫描按原版语义并入 */
52	const tileSolidLike = (t: number): boolean => {
53	  const d = t ? TILE_DEFS[t] : undefined;
54	  return !!d && (d.solid || d.platform);
55	};
56	
57	export interface Room {
58	  /** NPC 站立/安家 tile（门内地面） */
59	  standX: number;
60	  standY: number;
61	  /** 房间全部 tile idx（占用判定用）。含一圈实心边界格——原版 roomTiles 在
62	   *  CheckRoom 拒绝前先 Add（WorldGen.cs:6076-6080），ScoreRoom 的
63	   *  Housing_CheckIfInRoom 因此对地板格成立 */
64	  tiles: Set<number>;
65	}
66	
67	/** WorldGen.maxRoomTiles / maxRoomSize（WorldGen.cs:4210/4214） */
68	const MAX_TILES = 750;
69	const MAX_ROOM_SPAN = 100;
70	const MIN_TILES = 60;
71	/** TileID.Sets.HousingWalls（TileID.cs:377）：栅栏 11 / 高门 386 / 389 */
72	const HOUSING_WALL_TILES = new Set([11, 386, 389]);
73	
74	// ================= ScoreRoom 静态表（WorldGen.cs:5773-5788 GetTileTypeCountByCategory） =================
75	
76	const sheetOf = (t: number): number => TILE_DEFS[t]?.vanilla?.sheet ?? -1;
77	/** 邪恶度计数表（GetTileTypeCountByCategory TileScanGroup；sheet 即原版 tile id） */
78	const EVIL_CORRUPT = new Set([23, 24, 25, 32, 112, 163, 400, 398]);
79	const EVIL_CRIMSON = new Set([199, 203, 200, 401, 399, 234, 352]);
80	const EVIL_HALLOW = new Set([109, 110, 113, 117, 116, 164, 403, 402]);
81	const SUNFLOWER_SHEET = 27;
82	/** TileID.Sets.IgnoredInHouseScore（TileID.cs:411）：头顶扫描忽略项 */
83	const IGNORED_IN_HOUSE_SCORE = new Set([4, 3, 73, 82, 83, 84, 386]);
84	/** TileID.Sets.BasicChest（TileID.cs:315） */
85	const BASIC_CHEST = new Set([21, 467]);
86	/** ScoreRoom_CanBeHomeSpot（WorldGen.cs:5967-5978）：boulder 379 不可作家 */
87	const BOULDER_SHEET = 379;
88	
89	// ================= 同房判定（TownRoomManager.CanNPCsLiveWithEachOther） =================
90	
91	/** NPC.housingCategory=1 全表（NPC.cs SetDefaults 仅四处赋值 ：17159/:17243/:17429/:17542）：
92	 *  城镇宠物——637 城镇猫 / 638 城镇狗 / 656 城镇兔 / 670 蓝史莱姆 / 678-684 史莱姆
93	 *  变体（绿/紫/老/黄/铜/彩虹/粉）；其余全部 = 0（含所有城镇 NPC） */
94	const HOUSING_CATEGORY_PET = new Set([637, 638, 656, 670, 678, 679, 680, 681, 682, 683, 684]);
95	
96	/** NPC.housingCategory（NPC.cs:8450 重置 0；上表四块赋 1） */
97	export function npcHousingCategory(npcId: number): 0 | 1 {
98	  return HOUSING_CATEGORY_PET.has(npcId) ? 1 : 0;
99	}
100	
101	/** TownRoomManager.CanNPCsLiveWithEachOther（TownRoomManager.cs:153-155）：
102	 *  `npc1.housingCategory != npc2.housingCategory`——**同类别不可同房**：
103	 *  城镇 NPC 之间互斥、宠物之间互斥；一名城镇 NPC + 一只宠物可同房。
104	 *  （ScoreRoom/QuickFindHome 的占用豁免消费位，WorldGen.cs:5587/5737/5754） */
105	export function canNPCsLiveWithEachOther(npc1ByType: number, npc2ByType: number): boolean {
106	  return npcHousingCategory(npc1ByType) !== npcHousingCategory(npc2ByType);
107	}
108	/** 原版门/闸 tile id（ScoreRoom 杂物扫描 5873 行） */
109	const DOOR_CLOSED_SHEET = 10;
110	const DOOR_OPEN_SHEET = 11;
111	const TALL_GATE_CLOSED_SHEET = 388;
112	const TALL_GATE_OPEN_SHEET = 389;
113	
114	/** IsOpenDoorAnchorFrame（WorldGen.cs:69228-69240）：开门的顶/底锚帧（frameX%72
115	 *  落在 [0,18)∪[54,72)），中段是门洞不算门体 */
116	function isOpenDoorAnchorFrame(st: TileStore, x: number, y: number): boolean {
117	  const i = st.idx(x, y);
118	  if (!st.flags[i] || sheetOf(st.type[i]) !== DOOR_OPEN_SHEET) return false;
119	  const m = st.frameX[i] % 72;
120	  return m < 18 || m >= 54;
121	}
122	
123	/** Collision.SolidTiles（矩形内任一实心即 true）——ScoreRoom 头顶净空判定用 */
124	function solidTilesIn(st: TileStore, x0: number, x1: number, y0: number, y1: number): boolean {
125	  for (let y = y0; y <= y1; y++) {
126	    for (let x = x0; x <= x1; x++) {
127	      if (!st.inBounds(x, y)) continue;
128	      const i = st.idx(x, y);
129	      if (st.flags[i] && tileSolidLike(st.type[i])) return true;
130	    }
131	  }
132	  return false;
133	}
134	
135	export interface RoomScore {
136	  /** hiScore（WorldGen.hiScore）；-1=被占用，0=无合格站位/过于邪恶 */
137	  score: number;
138	  /** bestX/bestY（地板格；站位 = y-1） */
139	  x: number;
140	  y: number;
141	  roomEvil: boolean;
142	  hasStandingSpace: boolean;
143	}
144	
145	export interface Occupant { x: number; y: number; /** 入住者原版 NPC id（CanNPCsLiveWithEachOther 判定；缺省按 cat 0 城镇 NPC） */ npcId?: number }
146	
147	/**
148	 * ScoreRoom 1:1（WorldGen.cs:5804-5940）：对已判合格的房间打分并选家位点。
149	 * occupied = 已入住 NPC 的 home tile（home 与 home-1 同在房内视为占用者）；
150	 * askingNpcId = 申请入住的 NPC id（占用豁免用：同 housingCategory 才判占用，
151	 * WorldGen.cs:5754 CanNPCsLiveWithEachOther——城镇 NPC 与城镇宠物可同房）。
152	 */
153	export function scoreRoom(
154	  st: TileStore, room: Room,
155	  occupied: Array<{ x: number; y: number; npcId?: number }>,
156	  askingNpcId = -1,
157	): RoomScore {
158	  const fail: RoomScore = { score: 0, x: room.standX, y: room.standY, roomEvil: false, hasStandingSpace: false };
159	  // ① 占用检查（ScoreRoom_IsThisRoomOccupiedBySomeone WorldGen.cs:5750-5763）：home 与
160	  //    home-1 都在房内者视为占用者——CanNPCsLiveWithEachOther 不同类别（城镇+宠物）可
161	  //    同房：兼容者不入占用、记入 sharedX（:5758），其 home 列 ±3 格内站位评分压至 1
162	  //    （:5882-5886 避让）；同类别则整房作废（hiScore=-1）
163	  let sharedX = -1;
164	  for (const h of occupied) {
165	    if (h.x < 1 || h.y < 1 || h.x >= st.w || h.y >= st.h) continue;
166	    if (room.tiles.has(st.idx(h.x, h.y)) && room.tiles.has(st.idx(h.x, h.y - 1))) {
167	      if (!canNPCsLiveWithEachOther(askingNpcId, h.npcId ?? -1)) {
168	        return { score: -1, x: room.standX, y: room.standY, roomEvil: false, hasStandingSpace: false };
169	      }
170	      sharedX = h.x;
171	    }
172	  }
173	  // 房间包围盒（原版 roomX1..roomY2 随泛洪扩张，含边界格）
174	  let rx1 = st.w, rx2 = 0, ry1 = st.h, ry2 = 0;
175	  for (const i of room.tiles) {
176	    const x = i % st.w, y = (i / st.w) | 0;
177	    if (x < rx1) rx1 = x;
178	    if (x > rx2) rx2 = x;
179	    if (y < ry1) ry1 = y;
180	    if (y > ry2) ry2 = y;
181	  }
182	  // ② 邪恶度：包围盒外扩 46（Housing_GetTestedRoomBounds ±(40+5+1)）扫 tile 计数
183	  //    （CountTileTypesInArea startX+1..endX-1 / startY+2..endY+1）
184	  let bx1 = Math.max(5, rx1 - 46), bx2 = Math.min(st.w - 6, rx2 + 46);
185	  let by1 = Math.max(5, ry1 - 44), by2 = Math.min(st.h - 6, ry2 + 44);
186	  let corrupt = 0, crimson = 0, hallow = 0, sunflower = 0;
187	  for (let y = by1 + 2; y <= by2 + 1; y++) {
188	    for (let x = bx1 + 1; x <= bx2 - 1; x++) {
189	      if (!st.inBounds(x, y)) continue;
190	      const i = st.idx(x, y);
191	      if (!st.flags[i]) continue;
192	      const sh = sheetOf(st.type[i]);
193	      if (EVIL_CORRUPT.has(sh)) corrupt++;
194	      else if (EVIL_CRIMSON.has(sh)) crimson++;
195	      else if (EVIL_HALLOW.has(sh)) hallow++;
196	      else if (sh === SUNFLOWER_SHEET) sunflower++;
197	    }
198	  }
199	  const evilNet = corrupt + crimson - 5 * sunflower - hallow; // WorldGen.cs:5774-5794 TotalGoodEvil=腐+猩−圣−5×向日葵格(每株−40);旧符号反致种向日葵反把好房推向 corrupted
200	  let base = 50;
201	  let roomEvil = false;
202	  const evil = evilNet < 50 ? 0 : evilNet;
203	  base -= evil;
204	  if (evil > 0) roomEvil = true;
205	  if (base <= -250) return { ...fail, roomEvil }; // 过于邪恶整房作废（5831-5835）
206	  // ③-⑥ 逐候选地板打分
207	  let hiScore = 0, bestX = room.standX, bestY = room.standY, hasStandingSpace = false;
208	  for (let j = ry1 + 2; j <= ry2 + 1; j++) {
209	    for (let i = rx1 + 1; i < rx2; i++) {
210	      if (!st.inBounds(i, j)) continue;
211	      const ii = st.idx(i, j);
212	      if (!st.flags[ii] || sheetOf(st.type[ii]) === BOULDER_SHEET) continue;
213	      if (!tileSolidLike(st.type[ii])) continue;
214	      if (solidTilesIn(st, i - 1, i + 1, j - 3, j - 1)) continue; // 头顶 3 格净空
215	      const li = st.idx(i - 1, j), ri = st.idx(i + 1, j);
216	      if (!st.flags[li] || !tileSolidLike(st.type[li])) continue; // 左右须实心
217	      if (!st.flags[ri] || !tileSolidLike(st.type[ri])) continue;
218	      let num = base;
219	      let centerCol = 0, chests = 0;
220	      for (let k = i - 2; k <= i + 2; k++) {
221	        for (let l = j - 4; l < j; l++) {
222	          if (!st.inBounds(k, l)) continue;
223	          const ci = st.idx(k, l);
224	          if (!st.flags[ci]) continue;
225	          const sh = sheetOf(st.type[ci]);
226	          if (IGNORED_IN_HOUSE_SCORE.has(sh)) continue;
227	          if (sh === DOOR_OPEN_SHEET && !isOpenDoorAnchorFrame(st, k, l)) continue;
228	          if (k === i) { centerCol++; continue; }
229	          if (BASIC_CHEST.has(sh)) { chests++; continue; }
230	          if (sh === DOOR_CLOSED_SHEET || sh === TALL_GATE_CLOSED_SHEET) num -= 20;
231	          else if (!isOpenDoorAnchorFrame(st, k, l) && sh !== TALL_GATE_OPEN_SHEET) num += tileSolidLike(st.type[ci]) ? -5 : 5;
232	          else num -= 20;
233	        }
234	      }
235	      if (num > 0) hasStandingSpace = true;
236	      // 共用房避让（WorldGen.cs:5882-5886）：与同居者 home 列距离 <3 的站位评分压至 1
237	      if (sharedX >= 0 && num >= 1 && Math.abs(sharedX - i) < 3) num = 1;
238	      if (num > 0 && chests > 0) { num -= 30 * chests; if (num < 1) num = 1; }
239	      if (num > 0 && centerCol > 0) { num -= 15 * centerCol; if (num < 1) num = 1; }
240	      if (num <= hiScore) continue;
241	      // ⑤ 落位校验：地板与上方 1-3 格都在房内且上方无实心（5908-5926）
242	      let ok = room.tiles.has(ii);
243	      for (let m = 1; m <= 3; m++) {
244	        const ai = st.idx(i, j - m);
245	        if (!st.inBounds(i, j - m) || !room.tiles.has(ai)) { ok = false; break; }
246	        if (st.flags[ai] && tileSolidLike(st.type[ai])) { ok = false; break; }
247	      }
248	      if (ok && room.tiles.has(st.idx(i, j - 1))) {
249	        hiScore = num;
250	        bestX = i;
251	        bestY = j;
252	      }
253	    }
254	  }
255	  return { score: hiScore, x: bestX, y: bestY, roomEvil, hasStandingSpace };
256	}
257	
258	/**
259	 * 从一扇门向内检查房间。doorX/doorY = 门顶格；门两侧/三行逐一尝试作填充起点。
260	 * 返回 null = 不构成合格房屋（漏墙 / 太大太小 / 缺桌椅灯）。
261	 */
262	export function checkRoom(st: TileStore, doorX: number, doorY: number): Room | null {
263	  for (const side of [-1, 1]) {
264	    for (let dy = 0; dy <= 2; dy++) {
265	      const sx = doorX + side, sy = doorY + dy;
266	      if (!st.inBounds(sx, sy) || st.isSolid(sx, sy)) continue;
267	      const room = floodRoom(st, sx, sy);
268	      if (room) return room;
269	    }
270	  }
271	  return null;
272	}
273	
274	/** CheckRoom 宽松墙证据（WorldGen.cs:6150-6169）：横竖各 ±2 的 5×1 窗口内出现
275	 *  房墙（Main.wallHouse）或 nactive 且 tileSolid/HousingWalls 的 tile。
276	 *  flag=横向证据、flag2=纵向证据——两向都须命中，否则按漏墙处理（:6171-6184） */
277	function hasLooseWallEvidence(st: TileStore, x: number, y: number): boolean {
278	  // TileID.Sets.HousingWalls（TileID.cs:377）：11 栅栏 / 386 高门 / 389
279	  const wallLike = (ii: number): boolean => {
280	    if (WALL_HOUSE.has(st.wall[ii])) return true;
281	    if (!st.flags[ii]) return false;
282	    return tileSolidLike(st.type[ii]) || HOUSING_WALL_TILES.has(sheetOf(st.type[ii]));
283	  };
284	  let horiz = false, vert = false;
285	  for (let k = -2; k <= 2; k++) {
286	    if (st.inBounds(x + k, y) && wallLike(st.idx(x + k, y))) horiz = true;
287	    if (st.inBounds(x, y + k) && wallLike(st.idx(x, y + k))) vert = true;
288	  }
289	  return horiz && vert;
290	}
291	
292	/** 泛洪填充一个房间（8 向 = 原版 StartRoomCheck 邻居压栈 j,k∈-1..1，:6037-6043；
293	 *  对角穿墙连通是原版语义；门/平台/实心为边界） */
294	function floodRoom(st: TileStore, sx: number, sy: number): Room | null {
295	  const tiles = new Set<number>();
296	  let hasTable = false, hasChair = false, hasLight = false, hasDoor = false;
297	  let minX = sx, maxX = sx, minY = sy, maxY = sy;
298	  let head = 0;
299	  const queue: number[] = [st.idx(sx, sy)];
300	  tiles.add(queue[0]);
301	
302	  while (head < queue.length) {
303	    const i = queue[head++];
304	    const x = i % st.w, y = (i / st.w) | 0;
305	    const t = st.type[i];
306	    const def = t ? TILE_DEFS[t] : undefined;
307	    // 纯空气格必须背靠房墙（原版 CheckRoom 墙判定；家具格豁免）。宽松分支
308	    // （WorldGen.cs:6150-6185）：自身无房墙时，横/竖各 ±2 的 5×1 窗口内出现
309	    // 房墙或实心/HousingWalls tile（nactive）即算有墙——横竖两向须都有证据
310	    if (!st.flags[i] && !WALL_HOUSE.has(st.wall[i]) && !hasLooseWallEvidence(st, x, y)) return null;
311	    if (st.flags[i] && def) {
312	      if (isDoorType(t)) { hasDoor = true; }
313	      else if (def.light) hasLight = true;
314	      else if (countsAsTable(def.key, def.vanilla?.sheet)) hasTable = true;
315	      else if (countsAsChair(def.key, def.vanilla?.sheet)) hasChair = true;
316	    }
317	    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]] as const) {
318	      const nx = x + dx, ny = y + dy;
319	      if (nx < 1 || ny < 1 || nx >= st.w - 1 || ny >= st.h - 1) return null; // 漏到世界边
320	      const ni = st.idx(nx, ny);
321	      if (tiles.has(ni)) continue;
322	      const nt = st.type[ni];
323	      const ndef = nt ? TILE_DEFS[nt] : undefined;
324	      // 边界：实心 / 平台 / 门（门计入需求但不穿透到室外）。
325	      // 原版 CheckRoom 先 roomTiles.Add 再拒绝（6076-6080）——边界格也入集合，
326	      // ScoreRoom 的 Housing_CheckIfInRoom(地板格) 依赖这一点
327	      if (st.isSolid(nx, ny) || ndef?.platform || isDoorType(nt)) {
328	        if (isDoorType(nt)) hasDoor = true;
329	        tiles.add(ni);
330	        if (nx < minX) minX = nx;
331	        if (nx > maxX) maxX = nx;
332	        if (ny < minY) minY = ny;
333	        if (ny > maxY) maxY = ny;
334	        continue;
335	      }
336	      if (tiles.size >= MAX_TILES) return null; // ≥maxRoomTiles = 没封好（WorldGen.cs:4210）
337	      if (maxX - minX >= MAX_ROOM_SPAN || maxY - minY >= MAX_ROOM_SPAN) return null;
338	      tiles.add(ni);
339	      queue.push(ni);
340	      if (nx < minX) minX = nx;
341	      if (nx > maxX) maxX = nx;
342	      if (ny < minY) minY = ny;
343	      if (ny > maxY) maxY = ny;
344	    }
345	  }
346	  if (tiles.size < MIN_TILES || !hasDoor || !hasTable || !hasChair || !hasLight) return null;
347	  // 站立点：起点列向下找地板
348	  let fy = sy;
349	  while (fy < st.h - 2 && !st.isSolid(sx, fy)) fy++;
350	  if (st.isSolid(sx, sy) || fy >= st.h - 2) return null;
351	  return { standX: sx, standY: fy - 1, tiles };
352	}
353	
354	/**
355	 * 全图找一间无人入住的合格房屋（房间枚举为本仓库自有——原版无"全图找房"，
356	 * QuickFindHome 是对既有 home 的单房校验；房内站位选择 = ScoreRoom 1:1）。
357	 * 多房择优：取 ScoreRoom 分最高者，同分取离锚点近（原版单房无此维度）。
358	 * occupied = 已入住 NPC 的 home tile 列表（npcId 供同房豁免判定）。
359	 * askingNpcId = 申请入住者（ScoreRoom 占用豁免 + 共用房避让）。
360	 */
361	export function findFreeHouse(
362	  st: TileStore, occupied: Array<{ x: number; y: number; npcId?: number }>,
363	  nearX?: number, nearY?: number, askingNpcId = -1,
364	): Room | null {
365	  const anchorX = nearX ?? Math.floor(st.w / 2);
366	  const anchorY = nearY ?? 0;
367	  let best: Room | null = null;
368	  let bestScore = 0;
369	  let bestD = Infinity;
370	  for (let y = 3; y < st.h - 4; y++) {
371	    const row = y * st.w;
372	    for (let x = 3; x < st.w - 3; x++) {
373	      const t = st.type[row + x];
374	      if (!isDoorType(t)) continue;
375	      const room = checkRoom(st, x, y);
376	      if (!room) continue;
377	      // ScoreRoom：占用/邪恶度/站位打分一体（占用返回 -1）
378	      const s = scoreRoom(st, room, occupied, askingNpcId);
379	      if (s.score <= 0) continue;
380	      const d = Math.abs(s.x - anchorX) + Math.abs((s.y - 1) - anchorY);
381	      if (s.score > bestScore || (s.score === bestScore && d < bestD)) {
382	        bestScore = s.score;
383	        bestD = d;
384	        room.standX = s.x;
385	        room.standY = s.y - 1;
386	        best = room;
387	      }
388	    }
389	  }
390	  return best;
391	}
392	

```


---

## 🤖 Assistant · 2026-08-13T10:02:57.928Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Big finding: `findFreeHouse` scans the **whole map** (y from 3 to h-4, x from 3 to w-3) for any door, then checks the room. So generated structures with doors + table + chair + light anywhere (including deep underground) are candidates. That's repo's own extension ("原版无'全图找房'").

Now: original semantics — how do town NPCs find homes? In vanilla, NPCs move into rooms that... Let me recall: `WorldGen.QuickFindHome` and the NPC spawn/move-in logic. In vanilla, when a town NPC spawns (townNPC arrival), the code searches for a suitable home. Let me find it in NPC.cs: search "QuickFindHome" and "homeless".

Vanilla: NPC.cs — when a new town NPC arrives, `Main.npc[i].homeless` etc. There is code in NPC.UpdateTownNPC or in Main.UpdateTime / NPC.SpawnTownNPC... Let me grep for how a homeless town NPC finds a home: `homeless = false` assignments near QuickFindHome.

Also key: vanilla housing check requires the room to be reachable? Actually vanilla NPCs teleport home at night. Underground houses: vanilla NPCs CAN live in underground cabins — well-known.

But important nuance: **vanilla's home search is anchored** — new town NPCs appear near the player/spawn and search near spawn? Let me check. In NPC.cs `SpawnTownNPC`/`UpdateTownNPCs`? There's code:

```
if (!npc.homeless) ... 
```

Actually the vanilla code for a homeless NPC finding a home: `WorldGen.QuickFindHome(npc)`? Let me grep.

Also, vanilla CaveHouse walls: WoodHouseBuilder uses WoodWall? Let me check HouseBuilder.cs to see `_wall` fields. Cave houses in vanilla: the interior walls are Wood Walls (for forest), Gold Brick etc.? Actually vanilla cave cabins: interior lined with wood walls — and Wood Wall (id 21? no). WallID: WoodWall = 21? Let me check WallID.cs: 1 = Stone? Actually WallID: 1 = Stone Wall? Known: WallID.Wood = 21? Hmm: WallID.Dirt = 0? WallID: DirtWall=0... Let me grep WallID.cs for the ids used by cave house builders.

Repo WALL_HOUSE includes 21, 22, 23... many ids including 21..27 — those are wood/gray brick etc. So if cave houses place wood walls (id 21?) they'd be house walls in both.

Let me now:
1. Read original HouseBuilder.cs (CaveHouse) to find wall types.
2. Read repo CaveHousePass.ts for wall ids.
3. Check VanillaSpawner.ts:107 WALL_HOUSE (maybe a different table used by gen).
4. Check Game.ts updateTownNpcArrival.
````

</details>


---

## 🤖 Assistant · 2026-08-13T10:02:59.321Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:02:59.360Z

**📎 ToolResult**

```
1	using System;
2	using System.Collections.Generic;
3	using System.Collections.ObjectModel;
4	using System.Linq;
5	using Microsoft.Xna.Framework;
6	using Terraria.GameContent.Generation;
7	using Terraria.Utilities;
8	using Terraria.WorldBuilding;
9	
10	namespace Terraria.GameContent.Biomes.CaveHouse;
11	
12	public class HouseBuilder
13	{
14		private const int VERTICAL_EXIT_WIDTH = 3;
15	
16		public static readonly HouseBuilder Invalid = new HouseBuilder();
17	
18		public readonly HouseType Type;
19	
20		public readonly bool IsValid;
21	
22		protected ushort[] SkipTilesDuringWallAging = new ushort[5] { 245, 246, 240, 241, 242 };
23	
24		public double ChestChance { get; set; }
25	
26		public ushort TileType { get; protected set; }
27	
28		public ushort WallType { get; protected set; }
29	
30		public ushort BeamType { get; protected set; }
31	
32		public byte BeamPaint { get; protected set; }
33	
34		public int PlatformStyle { get; protected set; }
35	
36		public int DoorStyle { get; protected set; }
37	
38		public int TableStyle { get; protected set; }
39	
40		public bool UsesTables2 { get; protected set; }
41	
42		public int WorkbenchStyle { get; protected set; }
43	
44		public int PianoStyle { get; protected set; }
45	
46		public int BookcaseStyle { get; protected set; }
47	
48		public int ChairStyle { get; protected set; }
49	
50		public int ChestStyle { get; protected set; }
51	
52		public bool UsesContainers2 { get; protected set; }
53	
54		public ReadOnlyCollection<Rectangle> Rooms { get; private set; }
55	
56		public Rectangle TopRoom => Rooms.First();
57	
58		public Rectangle BottomRoom => Rooms.Last();
59	
60		private UnifiedRandom _random => WorldGen.genRand;
61	
62		private Tile[,] _tiles => Main.tile;
63	
64		private HouseBuilder()
65		{
66			IsValid = false;
67		}
68	
69		protected HouseBuilder(HouseType type, IEnumerable<Rectangle> rooms)
70		{
71			Type = type;
72			IsValid = true;
73			List<Rectangle> list = rooms.ToList();
74			list.Sort((Rectangle lhs, Rectangle rhs) => lhs.Top.CompareTo(rhs.Top));
75			Rooms = list.AsReadOnly();
76		}
77	
78		protected virtual void AgeRoom(Rectangle room)
79		{
80		}
81	
82		public void PotentiallyConvertToRainbowMossBlock()
83		{
84			if (WorldGen.SecretSeed.rainbowStuff.Enabled && WorldGen.genRand.Next(2) == 0)
85			{
86				TileType = 692;
87				WallType = 346;
88				PlatformStyle = 43;
89				DoorStyle = 44;
90			}
91		}
92	
93		public void PotentiallyConvertToRainbowBrick()
94		{
95			if (!Main.tenthAnniversaryWorld)
96			{
97				return;
98			}
99			if (Main.getGoodWorld)
100			{
101				if (WorldGen.genRand.Next(7) == 0)
102				{
103					TileType = 160;
104					WallType = 44;
105				}
106			}
107			else if (WorldGen.genRand.Next(2) == 0)
108			{
109				TileType = 160;
110				WallType = 44;
111			}
112		}
113	
114		public void RainbowifyOnTenthAnniversaryWorlds()
115		{
116			if (!Main.tenthAnniversaryWorld || (TileType == 160 && WorldGen.genRand.Next(2) == 0))
117			{
118				return;
119			}
120			foreach (Rectangle room in Rooms)
121			{
122				WorldUtils.Gen(new Point(room.X, room.Y), new Shapes.Rectangle(room.Width, room.Height), new Actions.SetTileAndWallRainbowPaint());
123			}
124		}
125	
126		public void PotentiallyConvertToSeedHouse()
127		{
128			if (WorldGen.SecretSeed.errorWorld.Enabled)
129			{
130				PlatformStyle = WorldGen.genRand.Next(49);
131				DoorStyle = WorldGen.genRand.Next(49);
132				TableStyle = WorldGen.genRand.Next(35);
133				WorkbenchStyle = WorldGen.genRand.Next(44);
134				PianoStyle = WorldGen.genRand.Next(39);
135				BookcaseStyle = WorldGen.genRand.Next(40);
136				ChairStyle = WorldGen.genRand.Next(44);
137				switch (WorldGen.genRand.Next(20))
138				{
139				default:
140					TileType = 159;
141					WallType = 43;
142					break;
143				case 1:
144					TileType = 422;
145					WallType = 225;
146					break;
147				case 2:
148					TileType = 194;
149					WallType = 75;
150					break;
151				case 3:
152					TileType = 541;
153					WallType = 318;
154					PlatformStyle = 48;
155					break;
156				case 4:
157					TileType = 137;
158					WallType = 147;
159					break;
160				case 5:
161					TileType = 48;
162					WallType = 245;
163					break;
164				case 6:
165					TileType = 370;
166					WallType = 182;
167					break;
168				case 7:
169					TileType = 140;
170					WallType = 33;
171					break;
172				case 8:
173					TileType = 347;
174					WallType = 174;
175					break;
176				case 9:
177					TileType = 508;
178					WallType = 243;
179					break;
180				case 10:
181					TileType = 507;
182					WallType = 242;
183					break;
184				case 11:
185					TileType = 546;
186					WallType = 167;
187					break;
188				case 12:
189					TileType = 329;
190					WallType = 169;
191					break;
192				case 13:
193					TileType = 326;
194					WallType = 136;
195					break;
196				case 14:
197					TileType = 327;
198					WallType = 137;
199					break;
200				case 15:
201					TileType = 345;
202					WallType = 172;
203					break;
204				case 16:
205					TileType = 708;
206					WallType = 347;
207					break;
208				case 17:
209					TileType = 501;
210					WallType = 238;
211					break;
212				case 18:
213					TileType = 272;
214					WallType = 225;
215					break;
216				case 19:
217					TileType = 421;
218					WallType = 225;
219					break;
220				}
221			}
222			else
223			{
224				if (WorldGen.genRand.NextFloat() > 0.4f)
225				{
226					return;
227				}
228				bool num = Type == HouseType.Wood;
229				bool flag = Type == HouseType.Desert;
230				bool num2 = Type == HouseType.Jungle;
231				bool flag2 = Type == HouseType.Ice;
232				List<ushort> list = new List<ushort>();
233				if (num2 && Main.notTheBeesWorld && Main.tenthAnniversaryWorld)
234				{
235					list.Add(562);
236					list.Add(563);
237					list.Add(229);
238				}
239				if ((num || flag2) && Main.drunkWorld && Main.tenthAnniversaryWorld)
240				{
241					if (flag2)
242					{
243						list.Add(197);
244					}
245					else
246					{
247						list.Add(193);
248					}
249				}
250				if (flag2 && WorldGen.SecretSeed.worldIsFrozen.Enabled && WorldGen.genRand.Next(3) == 0)
251				{
252					list.Add(145);
253					list.Add(146);
254				}
255				if (flag && Main.remixWorld && Main.getGoodWorld)
256				{
257					list.Add(188);
258				}
259				if (list.Count > 0)
260				{
261					ushort num3 = list[WorldGen.genRand.Next(list.Count)];
262					switch (num3)
263					{
264					case 562:
265						TileType = num3;
266						WallType = 312;
267						BeamType = 575;
268						BeamPaint = 16;
269						PlatformStyle = 44;
270						DoorStyle = 45;
271						TableStyle = 8;
272						UsesTables2 = true;
273						WorkbenchStyle = 40;
274						PianoStyle = 39;
275						BookcaseStyle = 40;
276						ChairStyle = 44;
277						ChestStyle = 11;
278						UsesContainers2 = true;
279						break;
280					case 563:
281						TileType = num3;
282						WallType = 313;
283						BeamType = 575;
284						BeamPaint = 16;
285						PlatformStyle = 44;
286						DoorStyle = 45;
287						TableStyle = 8;
288						UsesTables2 = true;
289						WorkbenchStyle = 40;
290						PianoStyle = 39;
291						BookcaseStyle = 40;
292						ChairStyle = 44;
293						ChestStyle = 11;
294						UsesContainers2 = true;
295						break;
296					case 229:
297						TileType = num3;
298						WallType = 86;
299						BeamType = 575;
300						BeamPaint = 15;
301						PlatformStyle = 24;
302						DoorStyle = 22;
303						TableStyle = 19;
304						UsesTables2 = false;
305						WorkbenchStyle = 19;
306						PianoStyle = 9;
307						BookcaseStyle = 9;
308						ChairStyle = 22;
309						ChestStyle = 29;
310						UsesContainers2 = false;
311						break;
312					case 188:
313						TileType = num3;
314						WallType = 72;
315						BeamType = 124;
316						BeamPaint = 17;
317						PlatformStyle = 25;
318						DoorStyle = 4;
319						TableStyle = 30;
320						UsesTables2 = false;
321						WorkbenchStyle = 5;
322						PianoStyle = 17;
323						BookcaseStyle = 6;
324						ChairStyle = 6;
325						ChestStyle = 42;
326						UsesContainers2 = false;
327						break;
328					case 193:
329						TileType = num3;
330						WallType = 76;
331						BeamType = 124;
332						BeamPaint = 19;
333						PlatformStyle = 20;
334						DoorStyle = 31;
335						TableStyle = 29;
336						UsesTables2 = false;
337						WorkbenchStyle = 8;
338						PianoStyle = 24;
339						BookcaseStyle = 26;
340						ChairStyle = 31;
341						ChestStyle = 34;
342						UsesContainers2 = false;
343						break;
344					case 197:
345						TileType = num3;
346						WallType = 76;
347						BeamType = 574;
348						BeamPaint = 26;
349						PlatformStyle = 20;
350						DoorStyle = 31;
351						TableStyle = 29;
352						UsesTables2 = false;
353						WorkbenchStyle = 8;
354						PianoStyle = 24;
355						BookcaseStyle = 26;
356						ChairStyle = 31;
357						ChestStyle = 34;
358						UsesContainers2 = false;
359						break;
360					case 145:
361						TileType = num3;
362						WallType = 29;
363						BeamType = 574;
364						BeamPaint = 26;
365						break;
366					case 146:
367						TileType = num3;
368						WallType = 30;
369						BeamType = 574;
370						BeamPaint = 26;
371						break;
372					}
373				}
374			}
375		}
376	
377		public void PaintSeedHouses()
378		{
379			if (TileType != 197 || !Main.drunkWorld || !Main.tenthAnniversaryWorld)
380			{
381				return;
382			}
383			foreach (Rectangle room in Rooms)
384			{
385				WorldUtils.Gen(new Point(room.X, room.Y), new Shapes.Rectangle(room.Width, room.Height), Actions.Chain(new Modifiers.OnlyTiles(19, 10, 11, 14, 18, 87, 101, 15, 21), new Actions.SetTilePaint(7)));
386				WorldUtils.Gen(new Point(room.X, room.Y), new Shapes.Rectangle(room.Width, room.Height), Actions.Chain(new Modifiers.OnlyWalls(WallType), new Actions.SetWallPaint(7)));
387			}
388		}
389	
390		public virtual void Place(HouseBuilderContext context, StructureMap structures)
391		{
392			PlaceEmptyRooms();
393			foreach (Rectangle room in Rooms)
394			{
395				structures.AddProtectedStructure(room, 8);
396			}
397			PlaceStairs();
398			PlaceDoors();
399			PlacePlatforms();
400			PlaceSupportBeams();
401			PlaceBiomeSpecificPriorityTool(context);
402			FillRooms();
403			foreach (Rectangle room2 in Rooms)
404			{
405				AgeRoom(room2);
406			}
407			PlaceChests();
408			PlaceBiomeSpecificTool(context);
409			PaintSeedHouses();
410		}
411	
412		private void PlaceEmptyRooms()
413		{
414			foreach (Rectangle room in Rooms)
415			{
416				WorldUtils.Gen(new Point(room.X, room.Y), new Shapes.Rectangle(room.Width, room.Height), Actions.Chain(new Actions.SetTileKeepWall(TileType), new Actions.SetFrames(frameNeighbors: true)));
417				WorldUtils.Gen(new Point(room.X + 1, room.Y + 1), new Shapes.Rectangle(room.Width - 2, room.Height - 2), Actions.Chain(new Actions.ClearTile(frameNeighbors: true), new Actions.PlaceWall(WallType)));
418			}
419		}
420	
421		private void FillRooms()
422		{
423			int x = 14;
424			if (UsesTables2)
425			{
426				x = 469;
427			}
428			Point[] choices = new Point[7]
429			{
430				new Point(x, TableStyle),
431				new Point(16, 0),
432				new Point(18, WorkbenchStyle),
433				new Point(86, 0),
434				new Point(87, PianoStyle),
435				new Point(94, 0),
436				new Point(101, BookcaseStyle)
437			};
438			foreach (Rectangle room in Rooms)
439			{
440				int num = room.Width / 8;
441				int num2 = room.Width / (num + 1);
442				int num3 = _random.Next(2);
443				for (int i = 0; i < num; i++)
444				{
445					int num4 = (i + 1) * num2 + room.X;
446					switch (i + num3 % 2)
447					{
448					case 0:
449					{
450						int num5 = room.Y + Math.Min(room.Height / 2, room.Height - 5);
451						PaintingEntry paintingEntry = ((Type == HouseType.Desert) ? WorldGen.RandHousePictureDesert() : WorldGen.RandHousePicture());
452						WorldGen.PlaceTile(num4, num5, paintingEntry.tileType, mute: true, forced: false, -1, paintingEntry.style);
453						break;
454					}
455					case 1:
456					{
457						int num5 = room.Y + 1;
458						WorldGen.PlaceTile(num4, num5, 34, mute: true, forced: false, -1, _random.Next(6));
459						for (int j = -1; j < 2; j++)
460						{
461							for (int k = 0; k < 3; k++)
462							{
463								_tiles[j + num4, k + num5].frameX += 54;
464							}
465						}
466						break;
467					}
468					}
469				}
470				int num6 = room.Width / 8 + 3;
471				WorldGen.SetupStatueList();
472				while (num6 > 0)
473				{
474					int num7 = _random.Next(room.Width - 3) + 1 + room.X;
475					int num8 = room.Y + room.Height - 2;
476					switch (_random.Next(4))
477					{
478					case 0:
479						WorldGen.PlaceSmallPile(num7, num8, _random.Next(31, 34), 1, 185);
480						break;
481					case 1:
482						WorldGen.PlaceTile(num7, num8, 186, mute: true, forced: false, -1, _random.Next(22, 26));
483						break;
484					case 2:
485					{
486						int num9 = _random.Next(2, GenVars.statueList.Length);
487						WorldGen.PlaceTile(num7, num8, GenVars.statueList[num9].X, mute: true, forced: false, -1, GenVars.statueList[num9].Y);
488						if (GenVars.StatuesWithTraps.Contains(num9))
489						{
490							WorldGen.PlaceStatueTrap(num7, num8);
491						}
492						break;
493					}
494					case 3:
495					{
496						Point point = Utils.SelectRandom(_random, choices);
497						WorldGen.PlaceTile(num7, num8, point.X, mute: true, forced: false, -1, point.Y);
498						break;
499					}
500					}
501					num6--;
502				}
503			}
504		}
505	
506		private void PlaceStairs()
507		{
508			foreach (Tuple<Point, Point> item3 in CreateStairsList())
509			{
510				Point item = item3.Item1;
511				Point item2 = item3.Item2;
512				int num = ((item2.X > item.X) ? 1 : (-1));
513				ShapeData shapeData = new ShapeData();
514				for (int i = 0; i < item2.Y - item.Y; i++)
515				{
516					shapeData.Add(num * (i + 1), i);
517				}
518				WorldUtils.Gen(item, new ModShapes.All(shapeData), Actions.Chain(new Actions.PlaceTile(19, PlatformStyle), new Actions.SetSlope((num == 1) ? 1 : 2), new Actions.SetFrames(frameNeighbors: true)));
519				WorldUtils.Gen(new Point(item.X + ((num == 1) ? 1 : (-4)), item.Y - 1), new Shapes.Rectangle(4, 1), Actions.Chain(new Actions.Clear(), new Actions.PlaceWall(WallType), new Actions.PlaceTile(19, PlatformStyle), new Actions.SetFrames(frameNeighbors: true)));
520			}
521		}
522	
523		private List<Tuple<Point, Point>> CreateStairsList()
524		{
525			List<Tuple<Point, Point>> list = new List<Tuple<Point, Point>>();
526			for (int i = 1; i < Rooms.Count; i++)
527			{
528				Rectangle rectangle = Rooms[i];
529				Rectangle rectangle2 = Rooms[i - 1];
530				int num = rectangle2.X - rectangle.X;
531				int num2 = rectangle.X + rectangle.Width - (rectangle2.X + rectangle2.Width);
532				if (num > num2)
533				{
534					list.Add(new Tuple<Point, Point>(new Point(rectangle.X + rectangle.Width - 1, rectangle.Y + 1), new Point(rectangle.X + rectangle.Width - rectangle.Height + 1, rectangle.Y + rectangle.Height - 1)));
535				}
536				else
537				{
538					list.Add(new Tuple<Point, Point>(new Point(rectangle.X, rectangle.Y + 1), new Point(rectangle.X + rectangle.Height - 1, rectangle.Y + rectangle.Height - 1)));
539				}
540			}
541			return list;
542		}
543	
544		private void PlaceDoors()
545		{
546			foreach (Point item in CreateDoorList())
547			{
548				WorldUtils.Gen(item, new Shapes.Rectangle(1, 3), new Actions.ClearTile(frameNeighbors: true));
549				WorldGen.PlaceTile(item.X, item.Y, 10, mute: true, forced: true, -1, DoorStyle);
550			}
551		}
552	
553		private List<Point> CreateDoorList()
554		{
555			List<Point> list = new List<Point>();
556			foreach (Rectangle room in Rooms)
557			{
558				if (FindSideExit(new Rectangle(room.X + room.Width, room.Y + 1, 1, room.Height - 2), isLeft: false, out var exitY))
559				{
560					list.Add(new Point(room.X + room.Width - 1, exitY));
561				}
562				if (FindSideExit(new Rectangle(room.X, room.Y + 1, 1, room.Height - 2), isLeft: true, out exitY))
563				{
564					list.Add(new Point(room.X, exitY));
565				}
566			}
567			return list;
568		}
569	
570		private void PlacePlatforms()
571		{
572			foreach (Point item in CreatePlatformsList())
573			{
574				WorldUtils.Gen(item, new Shapes.Rectangle(3, 1), Actions.Chain(new Actions.ClearMetadata(), new Actions.PlaceTile(19, PlatformStyle), new Actions.SetFrames(frameNeighbors: true)));
575			}
576		}
577	
578		private List<Point> CreatePlatformsList()
579		{
580			List<Point> list = new List<Point>();
581			Rectangle topRoom = TopRoom;
582			Rectangle bottomRoom = BottomRoom;
583			if (FindVerticalExit(new Rectangle(topRoom.X + 2, topRoom.Y, topRoom.Width - 4, 1), isUp: true, out var exitX))
584			{
585				list.Add(new Point(exitX, topRoom.Y));
586			}
587			if (FindVerticalExit(new Rectangle(bottomRoom.X + 2, bottomRoom.Y + bottomRoom.Height - 1, bottomRoom.Width - 4, 1), isUp: false, out exitX))
588			{
589				list.Add(new Point(exitX, bottomRoom.Y + bottomRoom.Height - 1));
590			}
591			return list;
592		}
593	
594		private void PlaceSupportBeams()
595		{
596			foreach (Rectangle item in CreateSupportBeamList())
597			{
598				if (item.Height > 1 && _tiles[item.X, item.Y - 1].type != 19)
599				{
600					WorldUtils.Gen(new Point(item.X, item.Y), new Shapes.Rectangle(item.Width, item.Height), Actions.Chain(new Actions.SetTileKeepWall(BeamType), new Actions.SetFrames(frameNeighbors: true), new Actions.SetTilePaint(BeamPaint)));
601					Tile tile = _tiles[item.X, item.Y + item.Height];
602					tile.slope(0);
603					tile.halfBrick(halfBrick: false);
604				}
605			}
606		}
607	
608		private List<Rectangle> CreateSupportBeamList()
609		{
610			List<Rectangle> list = new List<Rectangle>();
611			int num = Rooms.Min((Rectangle room) => room.Left);
612			int num2 = Rooms.Max((Rectangle room) => room.Right) - 1;
613			int num3 = 6;
614			while (num3 > 4 && (num2 - num) % num3 != 0)
615			{
616				num3--;
617			}
618			for (int num4 = num; num4 <= num2; num4 += num3)
619			{
620				for (int num5 = 0; num5 < Rooms.Count; num5++)
621				{
622					Rectangle rectangle = Rooms[num5];
623					if (num4 < rectangle.X || num4 >= rectangle.X + rectangle.Width)
624					{
625						continue;
626					}
627					int num6 = rectangle.Y + rectangle.Height;
628					int num7 = 50;
629					for (int num8 = num5 + 1; num8 < Rooms.Count; num8++)
630					{
631						if (num4 >= Rooms[num8].X && num4 < Rooms[num8].X + Rooms[num8].Width)
632						{
633							num7 = Math.Min(num7, Rooms[num8].Y - num6);
634						}
635					}
636					if (num7 > 0)
637					{
638						Point result;
639						bool flag = WorldUtils.Find(new Point(num4, num6), Searches.Chain(new Searches.Down(num7), new Conditions.IsSolid()), out result);
640						if (num7 < 50 && !WorldGen.SecretSeed.GenerateBiggerAbandonedHouses)
641						{
642							flag = true;
643							result = new Point(num4, num6 + num7);
644						}
645						if (flag)
646						{
647							list.Add(new Rectangle(num4, num6, 1, result.Y - num6));
648						}
649					}
650				}
651			}
652			return list;
653		}
654	
655		private static bool FindVerticalExit(Rectangle wall, bool isUp, out int exitX)
656		{
657			Point result2;
658			bool result = WorldUtils.Find(new Point(wall.X + wall.Width - 3, wall.Y + (isUp ? (-5) : 0)), Searches.Chain(new Searches.Left(wall.Width - 3), new Conditions.IsSolid().Not().AreaOr(3, 5)), out result2);
659			exitX = result2.X;
660			return result;
661		}
662	
663		private static bool FindSideExit(Rectangle wall, bool isLeft, out int exitY)
664		{
665			Point result2;
666			bool result = WorldUtils.Find(new Point(wall.X + (isLeft ? (-4) : 0), wall.Y + wall.Height - 3), Searches.Chain(new Searches.Up(wall.Height - 3), new Conditions.IsSolid().Not().AreaOr(4, 3)), out result2);
667			exitY = result2.Y;
668			return result;
669		}
670	
671		private void PlaceChests()
672		{
673			if (_random.NextDouble() > ChestChance)
674			{
675				return;
676			}
677			bool flag = false;
678			foreach (Rectangle room in Rooms)
679			{
680				int num = room.Height - 1 + room.Y;
681				bool num2 = num > (int)Main.worldSurface;
682				ushort chestTileType = (ushort)((num2 && UsesContainers2) ? 467 : 21);
683				int chestStyle = (num2 ? ChestStyle : 0);
684				for (int i = 0; i < 10; i++)
685				{
686					if (flag = WorldGen.AddBuriedChest(_random.Next(2, room.Width - 2) + room.X, num, 0, notNearOtherChests: false, chestStyle, trySlope: false, chestTileType))
687					{
688						break;
689					}
690				}
691				if (flag)
692				{
693					break;
694				}
695				for (int j = room.X + 2; j <= room.X + room.Width - 2; j++)
696				{
697					if (flag = WorldGen.AddBuriedChest(j, num, 0, notNearOtherChests: false, chestStyle, trySlope: false, chestTileType))
698					{
699						break;
700					}
701				}
702				if (flag)
703				{
704					break;
705				}
706			}
707			if (!flag)
708			{
709				foreach (Rectangle room2 in Rooms)
710				{
711					int num3 = room2.Y - 1;
712					bool num4 = num3 > (int)Main.worldSurface;
713					ushort chestTileType2 = (ushort)((num4 && UsesContainers2) ? 467 : 21);
714					int chestStyle2 = (num4 ? ChestStyle : 0);
715					for (int k = 0; k < 10; k++)
716					{
717						if (flag = WorldGen.AddBuriedChest(_random.Next(2, room2.Width - 2) + room2.X, num3, 0, notNearOtherChests: false, chestStyle2, trySlope: false, chestTileType2))
718						{
719							break;
720						}
721					}
722					if (flag)
723					{
724						break;
725					}
726					for (int l = room2.X + 2; l <= room2.X + room2.Width - 2; l++)
727					{
728						if (flag = WorldGen.AddBuriedChest(l, num3, 0, notNearOtherChests: false, chestStyle2, trySlope: false, chestTileType2))
729						{
730							break;
731						}
732					}
733					if (flag)
734					{
735						break;
736					}
737				}
738			}
739			if (flag)
740			{
741				return;
742			}
743			for (int m = 0; m < 1000; m++)
744			{
745				int i2 = _random.Next(Rooms[0].X - 30, Rooms[0].X + 30);
746				int num5 = _random.Next(Rooms[0].Y - 30, Rooms[0].Y + 30);
747				bool num6 = num5 > (int)Main.worldSurface;
748				ushort chestTileType3 = (ushort)((num6 && UsesContainers2) ? 467 : 21);
749				int chestStyle3 = (num6 ? ChestStyle : 0);
750				if (flag = WorldGen.AddBuriedChest(i2, num5, 0, notNearOtherChests: false, chestStyle3, trySlope: false, chestTileType3))
751				{
752					break;
753				}
754			}
755		}
756	
757		private void PlaceBiomeSpecificPriorityTool(HouseBuilderContext context)
758		{
759			if (Type != HouseType.Desert || GenVars.extraBastStatueCount >= GenVars.extraBastStatueCountMax)
760			{
761				return;
762			}
763			bool flag = false;
764			foreach (Rectangle room in Rooms)
765			{
766				int num = room.Height - 2 + room.Y;
767				if (WorldGen.remixWorldGen && (double)num > Main.rockLayer)
768				{
769					return;
770				}
771				for (int i = 0; i < 10; i++)
772				{
773					int num2 = _random.Next(2, room.Width - 2) + room.X;
774					WorldGen.PlaceTile(num2, num, 506, mute: true, forced: true);
775					if (flag = _tiles[num2, num].active() && _tiles[num2, num].type == 506)
776					{
777						break;
778					}
779				}
780				if (flag)
781				{
782					break;
783				}
784				for (int j = room.X + 2; j <= room.X + room.Width - 2; j++)
785				{
786					if (flag = WorldGen.PlaceTile(j, num, 506, mute: true, forced: true))
787					{
788						break;
789					}
790				}
791				if (flag)
792				{
793					break;
794				}
795			}
796			if (!flag)
797			{
798				foreach (Rectangle room2 in Rooms)
799				{
800					int num3 = room2.Y - 1;
801					for (int k = 0; k < 10; k++)
802					{
803						int num4 = _random.Next(2, room2.Width - 2) + room2.X;
804						WorldGen.PlaceTile(num4, num3, 506, mute: true, forced: true);
805						if (flag = _tiles[num4, num3].active() && _tiles[num4, num3].type == 506)
806						{
807							break;
808						}
809					}
810					if (flag)
811					{
812						break;
813					}
814					for (int l = room2.X + 2; l <= room2.X + room2.Width - 2; l++)
815					{
816						if (flag = WorldGen.PlaceTile(l, num3, 506, mute: true, forced: true))
817						{
818							break;
819						}
820					}
821					if (flag)
822					{
823						break;
824					}
825				}
826			}
827			if (flag)
828			{
829				GenVars.extraBastStatueCount++;
830			}
831		}
832	
833		private void PlaceBiomeSpecificTool(HouseBuilderContext context)
834		{
835			if (Type == HouseType.Jungle && context.SharpenerCount < _random.Next(2, 5))
836			{
837				bool flag = false;
838				foreach (Rectangle room in Rooms)
839				{
840					int num = room.Height - 2 + room.Y;
841					for (int i = 0; i < 10; i++)
842					{
843						int num2 = _random.Next(2, room.Width - 2) + room.X;
844						WorldGen.PlaceTile(num2, num, 377, mute: true, forced: true);
845						if (flag = _tiles[num2, num].active() && _tiles[num2, num].type == 377)
846						{
847							break;
848						}
849					}
850					if (flag)
851					{
852						break;
853					}
854					for (int j = room.X + 2; j <= room.X + room.Width - 2; j++)
855					{
856						if (flag = WorldGen.PlaceTile(j, num, 377, mute: true, forced: true))
857						{
858							break;
859						}
860					}
861					if (flag)
862					{
863						break;
864					}
865				}
866				if (flag)
867				{
868					context.SharpenerCount++;
869				}
870			}
871			if (Type != HouseType.Desert || context.ExtractinatorCount >= _random.Next(2, 5))
872			{
873				return;
874			}
875			ushort num3 = 219;
876			if (WorldGen.SecretSeed.errorWorld.Enabled)
877			{
878				num3 = 642;
879			}
880			bool flag2 = false;
881			foreach (Rectangle room2 in Rooms)
882			{
883				int num4 = room2.Height - 2 + room2.Y;
884				for (int k = 0; k < 10; k++)
885				{
886					int num5 = _random.Next(2, room2.Width - 2) + room2.X;
887					WorldGen.PlaceTile(num5, num4, num3, mute: true, forced: true);
888					if (flag2 = _tiles[num5, num4].active() && _tiles[num5, num4].type == num3)
889					{
890						break;
891					}
892				}
893				if (flag2)
894				{
895					break;
896				}
897				for (int l = room2.X + 2; l <= room2.X + room2.Width - 2; l++)
898				{
899					if (flag2 = WorldGen.PlaceTile(l, num4, num3, mute: true, forced: true))
900					{
901						break;
902					}
903				}
904				if (flag2)
905				{
906					break;
907				}
908			}
909			if (flag2)
910			{
911				context.ExtractinatorCount++;
912			}
913		}
914	}
915	

```


---

## 🤖 Assistant · 2026-08-13T10:02:59.490Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"wall\\|Wall\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts | head -40; echo ---; grep -n \"WALL_HOUSE\\|wallHouse\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/VanillaSpawner.ts | head -10",
 "description": "Cave house wall ids repo vs spawner table"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:02:59.563Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:24:  tile: number; wall: number; beam: number; door: number; platformStyle: number;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:36:  wood:     { tile: T.WOOD, wall: 27, beam: TILE_BY_KEY['v_124_wooden_beam']!, door: 0, platformStyle: 0, chestStyle: 1, table: 0, workbench: 0, piano: 0, bookcase: 0 },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:37:  ice:      { tile: TILE_BY_KEY['v_321_boreal_wood']!, wall: 149, beam: TILE_BY_KEY['v_574_boreal_beam']!, door: 30, platformStyle: 19, chestStyle: 11, table: 28, workbench: 23, piano: 23, bookcase: 25 },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:38:  jungle:   { tile: TILE_BY_KEY['v_158_rich_mahogany']!, wall: 42, beam: TILE_BY_KEY['v_575_rich_mahogany_beam']!, door: 2, platformStyle: 2, chestStyle: 8, table: 2, workbench: 2, piano: 2, bookcase: 12 },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:39:  desert:   { tile: TILE_BY_KEY['sandstone']!, wall: 187, beam: TILE_BY_KEY['v_577_sandstone_column']!, door: 43, platformStyle: 42, chestStyle: 10, chestTile2: true, tables2: true, table: 7, workbench: 39, piano: 38, bookcase: 39 },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:40:  granite:  { tile: TILE_BY_KEY['v_369_smooth_granite_block']!, wall: 181, beam: TILE_BY_KEY['v_576_granite_column']!, door: 34, platformStyle: 28, chestStyle: 50, table: 33, workbench: 29, piano: 28, bookcase: 30 },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:41:  marble:   { tile: TILE_BY_KEY['v_357_smooth_marble_block']!, wall: 179, beam: TILE_BY_KEY['v_561_marble_column']!, door: 35, platformStyle: 29, chestStyle: 51, table: 34, workbench: 30, piano: 29, bookcase: 31 },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:42:  mushroom: { tile: TILE_BY_KEY['v_190_glowing_mushroom_block']!, wall: 74, beam: TILE_BY_KEY['v_578_mushroom_beam']!, door: 6, platformStyle: 18, chestStyle: 32, table: 27, workbench: 7, piano: 22, bookcase: 24 },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:67:// SkipTilesDuringWallAging(HouseBuilder.cs:22 = {245,246,240,241,242} 画/挂件族)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:216:  if (n <= 1) return ['v_240_wall_hangings_3x3', PIC_240[rng.int(0, 17)]];
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:227:  if (n <= 1) return ['v_240_wall_hangings_3x3', [63, 64, 65, 66, 67, 68][rng.int(0, 5)]];
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:241://  · 链序 = 掷骰序:Dither/Blotches 永远排在 OnlyTiles/OnlyWalls 之前
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:249:  | { k: 'onlyWalls'; types: number[] }                                   // Modifiers.OnlyWalls(Modifiers.cs:216)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:253:  | { k: 'setTileKeepWall'; tile: number }                                // Actions.SetTileKeepWall(Actions.cs:272)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:256:  | { k: 'clearWall' }                                                    // Actions.ClearWall(Actions.cs:171)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:257:  | { k: 'placeWall'; wall: number }                                      // Actions.PlaceWall(Actions.cs:516)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:291:    case 'onlyWalls':
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:293:      return st.inBounds(x, y) && s.types.includes(st.wall[st.idx(x, y)])
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:303:    case 'setTileKeepWall':
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:313:    case 'clearWall':
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:314:      st.setWallSilent(x, y, 0);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:316:    case 'placeWall':
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:317:      st.setWallSilent(x, y, s.wall);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:383:  const wallTail = (surfaceWall: number): ChainStep[] => [
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:385:    r.y > gs.worldSurface ? { k: 'clearWall' } : { k: 'placeWall', wall: surfaceWall },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:397:    // ② 墙侵蚀(WoodHouseBuilder.cs:36):Dither(0.85)+Blotches()+OnlyWalls(27)+
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:400:      { k: 'dither', p: 0.85 }, B2(0.3), { k: 'onlyWalls', types: [def.wall] }, ...wallTail(2),
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:413:    //   OnlyTiles(321)+SetTileKeepWall(161)+Dither(0.8)+SetTileKeepWall(147)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:416:      { k: 'setTileKeepWall', tile: ICE161 },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:417:      { k: 'dither', p: 0.8 }, { k: 'setTileKeepWall', tile: SNOW147 },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:426:    // ③ 墙(IceHouseBuilder.cs:32,无 OnlyWalls):Dither(0.85)+Blotches(2,0.8)+
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:428:    genRect(st, rng, [{ k: 'dither', p: 0.85 }, B2(0.8), ...wallTail(40)], r.x, r.y, r.w, r.h);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:433:    //   OnlyTiles(158)+SetTileKeepWall(60)+Dither(0.8)+SetTileKeepWall(59)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:436:      { k: 'setTileKeepWall', tile: JUNGLE60 },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:437:      { k: 'dither', p: 0.8 }, { k: 'setTileKeepWall', tile: MUD59 },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:447:    // ③ 墙 64(JungleHouseBuilder.cs:32,无 OnlyWalls/SkipTiles)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:448:    genRect(st, rng, [{ k: 'dither', p: 0.85 }, B2(0.3), { k: 'placeWall', wall: 64 }], r.x, r.y, r.w, r.h);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:455:      { k: 'setTileKeepWall', tile: MUSH70 },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:466:    genRect(st, rng, [{ k: 'dither', p: 0.85 }, B2(0.3), { k: 'clearWall' }], r.x, r.y, r.w, r.h);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:471:    //   Dither(0.6)+Blotches(2,0.6)+OnlyTiles(主题块)+SetTileKeepWall(368/367)
---
ugrep: warning: ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/VanillaSpawner.ts: No such file or directory

```


---

## 🤖 Assistant · 2026-08-13T10:03:06.156Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
VanillaSpawner.ts path — user said VanillaSpawner.ts:107. Let me find it.

Also I need the WoodHouseBuilder.cs WallType for Wood (27 = wood wall, which is in WALL_HOUSE repo list). Original WoodHouseBuilder: WallType = 27 (Wood Wall). Yes repo uses 27. Ice = 149, jungle = 42, desert = 187, granite = 181, marble = 179, mushroom = 74.

Check whether those ids are in repo WALL_HOUSE: 27 ✓ (line 26 has 27), 149 ✓ (line 24), 42 ✓ (line 27), 187? Look: line 31 has 318, 319, 321, 322, 320, 347, 348, 351-366... 187 — I see "174, 230, 228, 229" hmm. Let me check: 187 not seen. Wait line 25 has "152, 145, 148, 175, 176, 182, 146, 147, 167, 133, 134, 135, 136, 137, 75, 76, 78, 82, 77". 187 missing? Let me check original wallHouse for 187. Actually original Main.cs has 268 wallHouse[ assignments. Let me extract the full list from Main.cs and compare with repo list.

Note: desert wall in original DesertHouseBuilder is WallType = 187? Let me check DesertHouseBuilder.cs. And Mushroom 74 ✓ present, granite 181 ✓ present, marble 179 ✓ present (line 24 has 179).

Let me extract all wallHouse ids from Main.cs and diff against repo's set.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:03:06.746Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -oE \"wallHouse\\[[0-9]+\\] = true\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | grep -oE \"[0-9]+\" | sort -n | tr '\\n' ' '",
 "description": "Extract full original wallHouse id list"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:03:06.816Z

**📎 ToolResult**

```
1 4 5 6 10 11 12 16 17 18 19 20 21 22 23 24 25 26 27 29 30 31 32 33 34 35 36 37 38 39 41 42 43 44 45 46 47 60 66 67 68 72 73 74 75 76 77 78 82 84 85 88 89 90 91 92 93 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 149 150 151 152 167 168 168 169 172 173 174 175 176 177 179 181 182 183 184 186 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366

```


---

## 🤖 Assistant · 2026-08-13T10:03:07.367Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"WallType = \" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/*.cs; echo ---; find ~/Project/GLM/SandboxWorld/game/src -name \"VanillaSpawner.ts\"",
 "description": "Original cave house WallType values and locate VanillaSpawner"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:03:07.443Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/DesertHouseBuilder.cs:14:		base.WallType = 187;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/GraniteHouseBuilder.cs:14:		base.WallType = 181;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:87:			WallType = 346;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:104:				WallType = 44;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:110:			WallType = 44;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:141:				WallType = 43;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:145:				WallType = 225;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:149:				WallType = 75;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:153:				WallType = 318;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:158:				WallType = 147;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:162:				WallType = 245;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:166:				WallType = 182;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:170:				WallType = 33;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:174:				WallType = 174;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:178:				WallType = 243;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:182:				WallType = 242;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:186:				WallType = 167;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:190:				WallType = 169;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:194:				WallType = 136;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:198:				WallType = 137;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:202:				WallType = 172;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:206:				WallType = 347;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:210:				WallType = 238;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:214:				WallType = 225;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:218:				WallType = 225;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:266:					WallType = 312;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:282:					WallType = 313;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:298:					WallType = 86;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:314:					WallType = 72;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:330:					WallType = 76;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:346:					WallType = 76;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:362:					WallType = 29;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:368:					WallType = 30;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/MarbleHouseBuilder.cs:14:		base.WallType = 179;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/IceHouseBuilder.cs:14:		base.WallType = 149;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/MushroomHouseBuilder.cs:13:		base.WallType = 74;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/JungleHouseBuilder.cs:14:		base.WallType = 42;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/WoodHouseBuilder.cs:13:		base.WallType = 27;
---
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts

```


---

## 🤖 Assistant · 2026-08-13T10:03:21.937Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Original wallHouse list includes 187? Looking at the extracted list: I see "181 182 183 184 186 224" — **187 is NOT in the list**! Also 185? no. 178? no. So Desert cave houses use wall 187 (sandstone brick? no — 187 = "Sandstone Brick"? Actually 187 is Natural Sandstone Wall?). Hmm, let me check WallID 187. In WallID.cs: 187 = SandstoneBrick? Let me check. Actually 216 is Sandstone Brick? Let me grep WallID.cs.

Wait — but the desert house walls get aged: DesertHouseBuilder.cs probably replaces walls (AgeRoom → SetWall 187→?). Let me read DesertHouseBuilder.cs.

Anyway, repo's WALL_HOUSE set also lacks 187 (checking repo list: 181, 182 present, 186 present... 187 absent). Consistent with original! So both exclude 187 → desert cave houses' interiors have wall 187 which is NOT a house wall in either original or repo. Interesting but consistent.

But wait — the critical question is different. Let me re-examine. The CheckRoom wall logic: for each air tile, it needs EITHER wallHouse wall on itself OR loose evidence (house wall / solid tile / housing-wall tile within ±2 in both axes). In a generated cave house: interior air tiles have wall 27 (wood, house wall) → pass. Floor tiles are solid → the check `if (!flag || !flag2)` — for the flood-fill, the original CheckRoom doesn't stop at solid tiles?? Wait, original CheckRoom: if the tile is nactive and tileSolid → "BlockingWall" feedback and return false (not added to stack). So solid tiles block. So roomTiles only contains non-solid interior. And interior walls are 27 → fine.

So **in vanilla, a naturally generated underground wood cabin (wall 27 wood wall + door + table + chair + light) IS valid housing** — and NPCs do move into underground cabins in vanilla. Yes, this is well-known vanilla behavior: town NPCs will claim underground cabins. Confirmed: vanilla wiki: "NPCs will move into any valid house, including naturally generated structures such as Underground Cabins". Also vanilla places doors+table+chair+torch? FillRooms places tables/workbenches/pianos/bookcases, and PlaceDoors places doors, and light? Torches: `PlaceSmallPile`, statue... where are torches placed? There's `PlaceChests`, plus in the gen maybe torches placed in `AgeRoom`? Hmm, vanilla cave cabins DO have torches? Actually, do they? Underground cabins in vanilla have chandeliers? Let me check WoodHouseBuilder.cs AgeRoom.

Let me read WoodHouseBuilder.cs and IceHouseBuilder.cs.

Also need to determine how vanilla decides where a new town NPC's home is: does it scan the whole world? Let me check vanilla: NPC.cs `UpdateTownNPC` / `SpawnNPC` — for homeless NPC, `WorldGen.QuickFindHome`. Actually in vanilla, when the housing query assigns a room, it's the player using the housing menu. But automatic move-in: in `NPC.AI`/`TownNPC` handling? Let me grep for "homeless" + "QuickFindHome" in NPC.cs and Main.cs.

Key vanilla code: `WorldGen.checkRoom` / `NPC.SpawnTownNPC`? The arrival of new town NPC: NPC.cs around "townNPC && homeless" -> there's `npc.homeless = true;` then in `NPC.UpdateTownNPC`, if homeless and night → teleport. Who assigns homes automatically? I recall in `Main.UpdateTime`/`WorldGen.UpdateWorld` there's code:

```
if (Main.checkForSpawns && ...) 
```

Actually the automatic home assignment is in NPC.cs `UpdateTownNPCs`? Let me search for "QuickFindHome" across the original codebase.
````

</details>


---

## 🤖 Assistant · 2026-08-13T10:03:21.955Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"QuickFindHome\" ~/Project/GLM/SandboxWorld/Terarria1456 --include=*.cs | head -20",
 "description": "Find QuickFindHome usages"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:03:22.028Z

**📎 ToolResult**

```
(eval):1: no matches found: --include=*.cs

```


---

## 🤖 Assistant · 2026-08-13T10:03:22.420Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cat ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/WoodHouseBuilder.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/DesertHouseBuilder.cs",
 "description": "Read wood and desert house builders"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:03:22.467Z

**📎 ToolResult**

```
using System.Collections.Generic;
using Microsoft.Xna.Framework;
using Terraria.WorldBuilding;

namespace Terraria.GameContent.Biomes.CaveHouse;

public class WoodHouseBuilder : HouseBuilder
{
	public WoodHouseBuilder(IEnumerable<Rectangle> rooms)
		: base(HouseType.Wood, rooms)
	{
		base.TileType = 30;
		base.WallType = 27;
		base.BeamType = 124;
		base.PlatformStyle = 0;
		base.DoorStyle = 0;
		base.TableStyle = 0;
		base.WorkbenchStyle = 0;
		base.PianoStyle = 0;
		base.BookcaseStyle = 0;
		base.ChairStyle = 0;
		base.ChestStyle = 1;
		PotentiallyConvertToSeedHouse();
		PotentiallyConvertToRainbowBrick();
		PotentiallyConvertToRainbowMossBlock();
	}

	protected override void AgeRoom(Rectangle room)
	{
		for (int i = 0; i < room.Width * room.Height / 16; i++)
		{
			int x = WorldGen.genRand.Next(1, room.Width - 1) + room.X;
			int y = WorldGen.genRand.Next(1, room.Height - 1) + room.Y;
			WorldUtils.Gen(new Point(x, y), new Shapes.Rectangle(2, 2), Actions.Chain(new Modifiers.Dither(), new Modifiers.Blotches(2, 2), new Modifiers.IsEmpty(), new Actions.SetTile(51, setSelfFrames: true)));
		}
		WorldUtils.Gen(new Point(room.X, room.Y), new Shapes.Rectangle(room.Width, room.Height), Actions.Chain(new Modifiers.Dither(0.85), new Modifiers.Blotches(), new Modifiers.OnlyWalls(base.WallType), new Modifiers.SkipTiles(SkipTilesDuringWallAging), ((double)room.Y > Main.worldSurface) ? ((GenAction)new Actions.ClearWall(frameNeighbors: true)) : ((GenAction)new Actions.PlaceWall(2))));
		WorldUtils.Gen(new Point(room.X, room.Y), new Shapes.Rectangle(room.Width, room.Height), Actions.Chain(new Modifiers.Dither(0.95), new Modifiers.OnlyTiles(30, 321, 158), new Actions.ClearTile(frameNeighbors: true)));
	}

	public override void Place(HouseBuilderContext context, StructureMap structures)
	{
		base.Place(context, structures);
		RainbowifyOnTenthAnniversaryWorlds();
	}
}
using System.Collections.Generic;
using Microsoft.Xna.Framework;
using Terraria.GameContent.Generation;
using Terraria.WorldBuilding;

namespace Terraria.GameContent.Biomes.CaveHouse;

public class DesertHouseBuilder : HouseBuilder
{
	public DesertHouseBuilder(IEnumerable<Rectangle> rooms)
		: base(HouseType.Desert, rooms)
	{
		base.TileType = 396;
		base.WallType = 187;
		base.BeamType = 577;
		base.PlatformStyle = 42;
		base.DoorStyle = 43;
		base.TableStyle = 7;
		base.UsesTables2 = true;
		base.WorkbenchStyle = 39;
		base.PianoStyle = 38;
		base.BookcaseStyle = 39;
		base.ChairStyle = 43;
		base.ChestStyle = 10;
		base.UsesContainers2 = true;
		PotentiallyConvertToSeedHouse();
	}

	protected override void AgeRoom(Rectangle room)
	{
		WorldUtils.Gen(new Point(room.X, room.Y), new Shapes.Rectangle(room.Width, room.Height), Actions.Chain(new Modifiers.Dither(0.8), new Modifiers.Blotches(2, 0.2), new Modifiers.OnlyTiles(base.TileType), new Actions.SetTileKeepWall(396, setSelfFrames: true), new Modifiers.Dither(), new Actions.SetTileKeepWall(397, setSelfFrames: true)));
		WorldUtils.Gen(new Point(room.X + 1, room.Y), new Shapes.Rectangle(room.Width - 2, 1), Actions.Chain(new Modifiers.Dither(), new Modifiers.OnlyTiles(397, 396), new Modifiers.Offset(0, 1), new ActionStalagtite()));
		WorldUtils.Gen(new Point(room.X + 1, room.Y + room.Height - 1), new Shapes.Rectangle(room.Width - 2, 1), Actions.Chain(new Modifiers.Dither(), new Modifiers.OnlyTiles(397, 396), new Modifiers.Offset(0, 1), new ActionStalagtite()));
		WorldUtils.Gen(new Point(room.X, room.Y), new Shapes.Rectangle(room.Width, room.Height), Actions.Chain(new Modifiers.Dither(0.8), new Modifiers.Blotches(), new Modifiers.OnlyWalls(base.WallType), new Actions.PlaceWall(216)));
	}
}

```


---

## 🤖 Assistant · 2026-08-13T10:03:37.397Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Key vanilla facts:

1. **Wood cave house** (WoodHouseBuilder.AgeRoom): for underground rooms (`room.Y > Main.worldSurface`), walls of type 27 are CLEARED (Actions.ClearWall) with dither 0.85 + blotches — i.e., the wood walls are mostly REMOVED underground, leaving natural wall? Wait — ClearWall sets wall = 0. Hmm, that means underground wood cabins have NO back walls (wall 0) in most of the interior! That's vanilla behavior — underground cabins often have holes in walls. But with wall 0, the CheckRoom loose-evidence rule: if wall==0, needs flag/flag2 from nearby house wall or solid tile within ±2 both axes → "HoleInWallIsTooBig" if fails. So partially cleared walls often still pass because the frame (solid tile border) provides evidence... Actually for interior tiles 2+ tiles away from any wall/solid, flag fails. Cabin interior is like 10x8; tiles in middle are >2 from border → fail. Hmm, so vanilla underground cabins often FAIL housing due to missing walls? But players report NPCs move into underground cabins — after players patch walls? Actually vanilla wiki on Underground Cabin: "Unlike most other structures, they cannot be used as housing until walls are added"? Let me check the wiki folder: terraria-wiki-md. Search for "Underground Cabin" housing.

Anyway, the repo's CaveHousePass.ts replicates this exactly: `r.y > gs.worldSurface ? { k: 'clearWall' } : { k: 'placeWall', wall: 2 }` with dither 0.85 (line 385, 400). So repo matches vanilla.

2. Desert cave house: WallType 187 aged to 216 (PlaceWall 216). Wall 216 = Sandstone Brick Wall? And 216 IS in wallHouse list? Check list: "...255 256 ... 311 312..." I don't see 216! Original list: 207-223 range: 224 appears, but 216? Looking at list: after 186 comes 224. So 216 NOT a house wall either. Hmm wait, 216 might be "Sandstone Brick Wall" which should be a valid housing wall in-game... Let me double check by grepping Main.cs for wallHouse[216].

Hmm the extraction shows no 216. Let me verify with a targeted grep. Also check WallID.cs names for 27, 187, 216, 2, 40, 64.

3. Repo CaveHousePass for desert (line ~471): let me read that region to see if it places 216. Line 471 mentions "OnlyTiles(主题块)+SetTileKeepWall(368/367)" — for granite? I saw line 466 clearWall for mushroom? Let me read lines 440-500.

Also torches/light: vanilla FillRooms doesn't place torches. Where do cabin lights come from? In vanilla cave cabins, are there torches? Hmm — underground cabins have... I believe they can contain chandeliers? Actually no. Let me check: PlaceSmallPile / statue... There's no torch placement in HouseBuilder. But wait, there's `PlaceChests` and that's it. Hmm, but housing requires a light source. Vanilla cabins: I recall they do NOT contain light sources (they're dark), so they are NOT valid housing without player adding a torch. Hmm, but wait — MushroomHouseBuilder? Let me check other builders for light placement. Actually let me grep the CaveHouse folder for "torch" / 4 / 33.

Actually — vanilla housing requirement for light comes from RoomNeeds in WorldGen: `houseTile` scan → `WorldGen.RoomNeeds`? Let me check how vanilla validates room needs: WorldGen.cs has `RoomCategoryCheck`? Search for "CountsAsTorch".

But the more important question for the user's report: NPC moved into a *generated* underground structure. In vanilla, do NPCs auto-claim generated structures? The vanilla automatic home-finding: I need to find it. In vanilla, `NPC.UpdateTownNPC` handles homeless NPCs. And there's code in NPC.cs `SpawnTownNPC`/`Main.UpdateTime`: When a town NPC spawns, `WorldGen.QuickFindHome`? The grep failed due to zsh glob. Let me redo with quotes.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:03:38.389Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"QuickFindHome\" ~/Project/GLM/SandboxWorld/Terarria1456 --include=\"*.cs\" | head -20; echo ---; grep -rn \"torch\\|Torch\\|, 4,\\|(4,\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/*.cs | grep -vi torchgod | head",
 "description": "Find QuickFindHome and cabin torch placement"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:03:38.554Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:56089:			WorldGen.QuickFindHome(whoAmI);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:65092:					WorldGen.QuickFindHome(k);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:5135:		QuickFindHome(num13);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:5665:	public static void QuickFindHome(int npc)
---
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:519:			WorldUtils.Gen(new Point(item.X + ((num == 1) ? 1 : (-4)), item.Y - 1), new Shapes.Rectangle(4, 1), Actions.Chain(new Actions.Clear(), new Actions.PlaceWall(WallType), new Actions.PlaceTile(19, PlatformStyle), new Actions.SetFrames(frameNeighbors: true)));
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:666:		bool result = WorldUtils.Find(new Point(wall.X + (isLeft ? (-4) : 0), wall.Y + wall.Height - 3), Searches.Chain(new Searches.Up(wall.Height - 3), new Conditions.IsSolid().Not().AreaOr(4, 3)), out result2);

```


---

## 🤖 Assistant · 2026-08-13T10:03:38.706Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts",
 "limit": 60,
 "offset": 440
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:03:38.750Z

**📎 ToolResult**

```
440	    //   IsEmpty+ActionVines(3, H, 62)
441	    for (const rowY of [r.y, r.y + r.h - 1]) {
442	      genRect(st, rng, [
443	        { k: 'dither', p: 0.5 }, { k: 'onlyTiles', types: [JUNGLE60] }, { k: 'offset', dx: 0, dy: 1 },
444	        { k: 'isEmpty' }, { k: 'vines', min: 3, max: r.h, vine: VINE62 },
445	      ], r.x + 1, rowY, r.w - 2, 1);
446	    }
447	    // ③ 墙 64(JungleHouseBuilder.cs:32,无 OnlyWalls/SkipTiles)
448	    genRect(st, rng, [{ k: 'dither', p: 0.85 }, B2(0.3), { k: 'placeWall', wall: 64 }], r.x, r.y, r.w, r.h);
449	    return;
450	  }
451	  if (theme === 'mushroom') {
452	    // ① 190→70(MushroomHouseBuilder.cs:27):Dither(0.7)+Blotches(2,0.5)+OnlyTiles(190)
453	    genRect(st, rng, [
454	      { k: 'dither', p: 0.7 }, B2(0.5), { k: 'onlyTiles', types: [def.tile] },
455	      { k: 'setTileKeepWall', tile: MUSH70 },
456	    ], r.x, r.y, r.w, r.h);
457	    // ② 顶/底行(MushroomHouseBuilder.cs:28-29):Dither(0.6)+OnlyTiles(70)+
458	    //   Offset(0,-1)+IsEmpty+SetTile(71)
459	    for (const rowY of [r.y, r.y + r.h - 1]) {
460	      genRect(st, rng, [
461	        { k: 'dither', p: 0.6 }, { k: 'onlyTiles', types: [MUSH70] }, { k: 'offset', dx: 0, dy: -1 },
462	        { k: 'isEmpty' }, { k: 'setTile', tile: SHROOM71 },
463	      ], r.x + 1, rowY, r.w - 2, 1);
464	    }
465	    // ③ 墙清空(MushroomHouseBuilder.cs:30)
466	    genRect(st, rng, [{ k: 'dither', p: 0.85 }, B2(0.3), { k: 'clearWall' }], r.x, r.y, r.w, r.h);
467	    return;
468	  }
469	  if (theme === 'granite' || theme === 'marble') {
470	    // ① 369→368 / 357→367(GraniteHouseBuilder.cs:28 / MarbleHouseBuilder.cs:28):
471	    //   Dither(0.6)+Blotches(2,0.6)+OnlyTiles(主题块)+SetTileKeepWall(368/367)
472	    const to = theme === 'granite' ? GRANITE368 : MARBLE367;
473	    genRect(st, rng, [
474	      { k: 'dither', p: 0.6 }, B2(0.6), { k: 'onlyTiles', types: [def.tile] },
475	      { k: 'setTileKeepWall', tile: to },
476	    ], r.x, r.y, r.w, r.h);
477	    // ② 顶/底行(GraniteHouseBuilder.cs:29-30):Dither(0.8)+OnlyTiles(368/367)+
478	    //   Offset(0,1)+ActionStalagtite(名单外 no-op,但 Dither/PlaceTight 掷骰照耗)
479	    for (const rowY of [r.y, r.y + r.h - 1]) {
480	      genRect(st, rng, [
481	        { k: 'dither', p: 0.8 }, { k: 'onlyTiles', types: [to] }, { k: 'offset', dx: 0, dy: 1 }, { k: 'stalagtite' },
482	      ], r.x + 1, rowY, r.w - 2, 1);
483	    }
484	    // ③ 墙 180/178(GraniteHouseBuilder.cs:31 / MarbleHouseBuilder.cs:31)
485	    genRect(st, rng, [
486	      { k: 'dither', p: 0.85 }, B2(0.3), { k: 'placeWall', wall: theme === 'granite' ? 180 : 178 },
487	    ], r.x, r.y, r.w, r.h);
488	    return;
489	  }
490	  // desert
491	  // ① 396→396→397(DesertHouseBuilder.cs:31):Dither(0.8)+Blotches(2,0.2)+
492	  //   OnlyTiles(396)+SetTileKeepWall(396)+Dither(0.5)+SetTileKeepWall(397)
493	  //   ——第一段写 396 是原版字面(视觉 no-op),但第二道 Dither 的掷骰位置在此
494	  genRect(st, rng, [
495	    { k: 'dither', p: 0.8 }, B2(0.2), { k: 'onlyTiles', types: [def.tile] },
496	    { k: 'setTileKeepWall', tile: def.tile },
497	    { k: 'dither', p: 0.5 }, { k: 'setTileKeepWall', tile: HARDSAND397 },
498	  ], r.x, r.y, r.w, r.h);
499	  // ② 顶/底行钟乳石(DesertHouseBuilder.cs:32-33,曾整体缺失 C5):

```


---

## 🤖 Assistant · 2026-08-13T10:03:40.418Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now check QuickFindHome in WorldGen.cs:5665 — this is the vanilla automatic home assignment. Let me read it. This determines the candidate anchor & scan range.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:03:40.663Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs",
 "limit": 85,
 "offset": 5665
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:03:40.674Z

**📎 ToolResult**

```
5665		public static void QuickFindHome(int npc)
5666		{
5667			bool flag = Main.tileSolid[379];
5668			Main.tileSolid[379] = true;
5669			if (Main.npc[npc].homeTileX > 10 && Main.npc[npc].homeTileY > 10 && Main.npc[npc].homeTileX < Main.maxTilesX - 10 && Main.npc[npc].homeTileY < Main.maxTilesY)
5670			{
5671				canSpawn = false;
5672				StartRoomCheck(Main.npc[npc].homeTileX, Main.npc[npc].homeTileY - 1);
5673				if (!canSpawn)
5674				{
5675					for (int i = Main.npc[npc].homeTileX - 1; i < Main.npc[npc].homeTileX + 2; i++)
5676					{
5677						for (int j = Main.npc[npc].homeTileY - 1; j < Main.npc[npc].homeTileY + 2 && !StartRoomCheck(i, j); j++)
5678						{
5679						}
5680					}
5681				}
5682				if (!canSpawn)
5683				{
5684					int num = 10;
5685					for (int k = Main.npc[npc].homeTileX - num; k <= Main.npc[npc].homeTileX + num; k += 2)
5686					{
5687						for (int l = Main.npc[npc].homeTileY - num; l <= Main.npc[npc].homeTileY + num && !StartRoomCheck(k, l); l += 2)
5688						{
5689						}
5690					}
5691				}
5692				if (!CheckSpecialTownNPCSpawningConditions(Main.npc[npc].type))
5693				{
5694					canSpawn = false;
5695				}
5696				if (canSpawn)
5697				{
5698					RoomNeeds();
5699					if (canSpawn)
5700					{
5701						ScoreRoom(npc, Main.npc[npc].type);
5702					}
5703					if (canSpawn && hiScore > 0)
5704					{
5705						canSpawn = IsRoomConsideredOccupiedForNPCIndex(npc);
5706					}
5707					if (canSpawn && hiScore > 0)
5708					{
5709						Main.npc[npc].homeTileX = bestX;
5710						Main.npc[npc].homeTileY = bestY;
5711						Main.npc[npc].homeless = false;
5712						Main.npc[npc].homelessDespawn = false;
5713						AchievementsHelper.NotifyProgressionEvent(8);
5714						canSpawn = false;
5715					}
5716					else
5717					{
5718						Main.npc[npc].homeless = true;
5719					}
5720				}
5721				else
5722				{
5723					Main.npc[npc].homeless = true;
5724				}
5725			}
5726			Main.tileSolid[379] = flag;
5727		}
5728	
5729		private static bool IsRoomConsideredOccupiedForNPCIndex(int npc)
5730		{
5731			bool result = true;
5732			for (int i = 0; i < Main.maxNPCs; i++)
5733			{
5734				if (i != npc)
5735				{
5736					NPC nPC = Main.npc[i];
5737					if (nPC.active && nPC.townNPC && !nPC.homeless && nPC.homeTileX == bestX && nPC.homeTileY == bestY && !TownManager.CanNPCsLiveWithEachOther(Main.npc[npc], nPC))
5738					{
5739						result = false;
5740						break;
5741					}
5742				}
5743			}
5744			return result;
5745		}
5746	
5747		private static bool ScoreRoom_IsThisRoomOccupiedBySomeone(int ignoreNPC = -1, int npcTypeAsking = -1)
5748		{
5749			for (int i = 0; i < Main.maxNPCs; i++)

```


---

## 🤖 Assistant · 2026-08-13T10:03:40.995Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "limit": 45,
 "offset": 65060
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:03:41.028Z

**📎 ToolResult**

```
65060			int num15 = 0;
65061			int num16 = 0;
65062			int num17 = 0;
65063			int num18 = 0;
65064			int num19 = 0;
65065			int num20 = 0;
65066			int num21 = 0;
65067			int num22 = 0;
65068			int num23 = 0;
65069			int num24 = 0;
65070			int num25 = 0;
65071			int num26 = 0;
65072			int num27 = 0;
65073			int num28 = 0;
65074			int num29 = 0;
65075			int num30 = 0;
65076			int num31 = 0;
65077			int num32 = 0;
65078			int num33 = 0;
65079			int num34 = 0;
65080			int num35 = 0;
65081			int num36 = 0;
65082			int num37 = 0;
65083			int num38 = 0;
65084			int num39 = 0;
65085			int num40 = 0;
65086			for (int k = 0; k < maxNPCs; k++)
65087			{
65088				if (npc[k].active && npc[k].townNPC)
65089				{
65090					if (npc[k].type != 368 && npc[k].type != 37 && npc[k].type != 453 && !npc[k].homeless)
65091					{
65092						WorldGen.QuickFindHome(k);
65093					}
65094					if (npc[k].type == 37)
65095					{
65096						num7++;
65097					}
65098					if (npc[k].type == 17)
65099					{
65100						num2++;
65101					}
65102					if (npc[k].type == 18)
65103					{
65104						num3++;

```


---

## 🤖 Assistant · 2026-08-13T10:03:45.191Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Huge finding: **vanilla QuickFindHome only re-validates the NPC's EXISTING homeTile** (home ±1, then ±10 spiral). It never searches the world for a new house. The homeTileX/homeTileY for a new town NPC comes from where the NPC spawned. Let me check where a new town NPC's homeTile is set: WorldGen.cs:5135 `QuickFindHome(num13)` — in `SpawnTownNPC`? Let me read around 5080-5140. That's the "arrival" code: NPC spawns near player, then homeTile is set near spawn point. Let me read.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:03:45.455Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs",
 "limit": 90,
 "offset": 5060
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:03:45.479Z

**📎 ToolResult**

```
5060					bestX = num6;
5061					break;
5062				}
5063			}
5064			int num7 = bestX;
5065			int num8 = bestY;
5066			bool flag2 = false;
5067			if (!flag2 && !((double)num8 > Main.worldSurface))
5068			{
5069				for (int m = 20; m < 500; m++)
5070				{
5071					for (int n = 0; n < 2; n++)
5072					{
5073						num7 = ((n != 0) ? (bestX - m * 2) : (bestX + m * 2));
5074						if (num7 > 10 && num7 < Main.maxTilesX - 10)
5075						{
5076							int num9 = bestY - m;
5077							double num10 = bestY + m;
5078							if (num9 < 10)
5079							{
5080								num9 = 10;
5081							}
5082							if (num10 > Main.worldSurface)
5083							{
5084								num10 = Main.worldSurface;
5085							}
5086							for (int num11 = num9; (double)num11 < num10; num11++)
5087							{
5088								num8 = num11;
5089								if (!Main.tile[num7, num8].nactive() || !Main.tileSolid[Main.tile[num7, num8].type])
5090								{
5091									continue;
5092								}
5093								if (Main.tile[num7, num8 - 3].liquid != 0 || Main.tile[num7, num8 - 2].liquid != 0 || Main.tile[num7, num8 - 1].liquid != 0 || Collision.SolidTiles(num7 - 1, num7 + 1, num8 - 3, num8 - 1))
5094								{
5095									break;
5096								}
5097								flag2 = true;
5098								Rectangle value = new Rectangle(num7 * 16 + 8 - NPC.sWidth / 2 - NPC.safeRangeX, num8 * 16 + 8 - NPC.sHeight / 2 - NPC.safeRangeY, NPC.sWidth + NPC.safeRangeX * 2, NPC.sHeight + NPC.safeRangeY * 2);
5099								for (int num12 = 0; num12 < 255; num12++)
5100								{
5101									if (Main.player[num12].active && new Rectangle((int)Main.player[num12].position.X, (int)Main.player[num12].position.Y, Main.player[num12].width, Main.player[num12].height).Intersects(value))
5102									{
5103										flag2 = false;
5104										break;
5105									}
5106								}
5107								break;
5108							}
5109						}
5110						if (flag2)
5111						{
5112							break;
5113						}
5114					}
5115					if (flag2)
5116					{
5117						break;
5118					}
5119				}
5120			}
5121			int num13 = NPC.NewNPC(NPC.GetSpawnSourceForTownSpawn(), num7 * 16, num8 * 16, prioritizedTownNPCType, 1);
5122			Main.npc[num13].homeTileX = bestX;
5123			Main.npc[num13].homeTileY = bestY;
5124			Main.npc[num13].homeless = true;
5125			Main.npc[num13].homelessDespawn = true;
5126			if (num7 < bestX)
5127			{
5128				Main.npc[num13].direction = 1;
5129			}
5130			else if (num7 > bestX)
5131			{
5132				Main.npc[num13].direction = -1;
5133			}
5134			Main.npc[num13].netUpdate = true;
5135			QuickFindHome(num13);
5136			int num14 = Main.rand.Next(6);
5137			_ = Main.npc[num13].FullName;
5138			string key = ((!Main.npc[num13].homeless) ? "Announcement.HasArrived" : ("Announcement.HomelessArrived_" + num14));
5139			ChatHelper.BroadcastChatMessage(NetworkText.FromKey(key, Main.npc[num13].GetFullNetName()), ChatColors.NPCTravel);
5140		}
5141	
5142		public static void UnspawnHomelessNPC()
5143		{
5144			int num = -1;
5145			for (int i = 0; i < Main.maxNPCs; i++)
5146			{
5147				if (Main.npc[i].active && Main.npc[i].homelessDespawn)
5148				{
5149					num = i;

```


---

## 🤖 Assistant · 2026-08-13T10:03:52.526Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Need the start of this function to know how bestX/bestY (home) is chosen. Let me read 4980-5060.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:03:52.543Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs",
 "limit": 85,
 "offset": 4975
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:03:52.565Z

**📎 ToolResult**

```
4975			}
4976			if (flag)
4977			{
4978				ChatHelper.BroadcastChatMessage(NetworkText.FromKey(Lang.misc[35].Key, Main.npc[num].GetFullNetName()), ChatColors.NPCTravel);
4979				Main.npc[num].active = false;
4980				Main.npc[num].life = 0;
4981				NetMessage.SendData(23, -1, -1, null, num);
4982			}
4983		}
4984	
4985		public static void SpawnHomelessNPC()
4986		{
4987			if (Main.eclipse || !Main.dayTime || (Main.invasionType > 0 && Main.invasionDelay == 0 && Main.invasionSize > 0) || prioritizedTownNPCType == 0 || FindAnyHomelessTownNPC(includeGuide: true) != -1)
4988			{
4989				return;
4990			}
4991			for (int i = 0; i < Main.maxNPCs; i++)
4992			{
4993				if (Main.npc[i].active && Main.npc[i].type == prioritizedTownNPCType)
4994				{
4995					return;
4996				}
4997			}
4998			bool flag = Main.tileSolid[379];
4999			Main.tileSolid[379] = true;
5000			try
5001			{
5002				if (SpawnTownNPC(LastFoundHouse.X, LastFoundHouse.Y) == TownNPCSpawnResult.Successful)
5003				{
5004					return;
5005				}
5006			}
5007			finally
5008			{
5009				Main.tileSolid[379] = flag;
5010			}
5011			_ = Point.Zero;
5012			int[] array = new int[Main.maxNPCs];
5013			Point[] array2 = new Point[Main.maxNPCs];
5014			int num = 0;
5015			for (int j = 0; j < Main.maxNPCs; j++)
5016			{
5017				NPC nPC = Main.npc[j];
5018				if (nPC.active && nPC.townNPC && nPC.type != 37 && !nPC.homeless)
5019				{
5020					array[num] = j;
5021					array2[num] = new Point(nPC.homeTileX, nPC.homeTileY);
5022					num++;
5023				}
5024			}
5025			if (num == 0)
5026			{
5027				return;
5028			}
5029			int num2 = Main.rand.Next(num);
5030			_ = array[num2];
5031			Point point = array2[num2];
5032			bestX = point.X;
5033			bestY = point.Y;
5034			int minValue = bestX;
5035			int num3 = bestX;
5036			int num4 = bestY;
5037			int num5 = bestX;
5038			while (num5 > bestX - 10 && (SolidTile(num5, num4) || Main.tileSolidTop[Main.tile[num5, num4].type]) && (!Main.tile[num5, num4 - 1].active() || !Main.tileSolid[Main.tile[num5, num4 - 1].type] || Main.tileSolidTop[Main.tile[num5, num4 - 1].type]) && (!Main.tile[num5, num4 - 2].active() || !Main.tileSolid[Main.tile[num5, num4 - 2].type] || Main.tileSolidTop[Main.tile[num5, num4 - 2].type]) && (!Main.tile[num5, num4 - 3].active() || !Main.tileSolid[Main.tile[num5, num4 - 3].type] || Main.tileSolidTop[Main.tile[num5, num4 - 3].type]))
5039			{
5040				minValue = num5;
5041				num5--;
5042			}
5043			for (int k = bestX; k < bestX + 10 && (SolidTile(k, num4) || Main.tileSolidTop[Main.tile[k, num4].type]) && (!Main.tile[k, num4 - 1].active() || !Main.tileSolid[Main.tile[k, num4 - 1].type] || Main.tileSolidTop[Main.tile[k, num4 - 1].type]) && (!Main.tile[k, num4 - 2].active() || !Main.tileSolid[Main.tile[k, num4 - 2].type] || Main.tileSolidTop[Main.tile[k, num4 - 2].type]) && (!Main.tile[k, num4 - 3].active() || !Main.tileSolid[Main.tile[k, num4 - 3].type] || Main.tileSolidTop[Main.tile[k, num4 - 3].type]); k++)
5044			{
5045				num3 = k;
5046			}
5047			for (int l = 0; l < 30; l++)
5048			{
5049				int num6 = Main.rand.Next(minValue, num3 + 1);
5050				if (l < 20)
5051				{
5052					if (num6 < bestX - 1 || num6 > bestX + 1)
5053					{
5054						bestX = num6;
5055						break;
5056					}
5057				}
5058				else if (num6 != bestX)
5059				{

```


---

## 🤖 Assistant · 2026-08-13T10:04:15.780Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Excellent. Vanilla semantics fully clear now:

**Vanilla**: A new town NPC's home anchor = **an existing housed NPC's homeTile** (random pick among housed NPCs, `SpawnHomelessNPC`), or `LastFoundHouse` (a house the player flagged with housing query?) via SpawnTownNPC. The home position is then validated by QuickFindHome — searching **only within ±10 tiles of that home** for a valid room. There is **no whole-world house search**. So in vanilla, an NPC will only move into an underground cabin if:
- some already-housed NPC lives right next to it (±10), or
- LastFoundHouse = that cabin (player used housing query on it).

So vanilla NPCs never spontaneously migrate into distant underground cabins. The first NPC (Guide) — homeTile initial? For the very first guide, `LastFoundHouse` initial value = spawn? Let me check LastFoundHouse default. In Main: `LastFoundHouse` default = world spawn. And Guide spawns at spawn point.

Now, additionally: **is a generated underground cabin even a valid room in vanilla?** Wood cabins underground have walls cleared (dither 0.85 → most wall 27 removed) → interior air tiles with wall 0 → CheckRoom requires loose evidence within ±2 both axes from house wall/solid/housing-wall-tile. Border tiles adjacent to the wood frame get evidence from solid tiles, but center tiles (>2 from frame) fail → room invalid. So underground wood cabins are generally NOT valid housing in vanilla (that's consistent with community knowledge: "underground cabins can't be used as housing without adding walls"). Hmm — but is that true? Let me verify: vanilla dither(0.85) means 85% chance to apply ClearWall... Actually Modifiers.Dither(0.85) means each tile has 85% chance to be processed. Plus Blotches. So ~85% of wall tiles cleared, ~15% remain wall 27. With random 15% remaining + blotch clustering, interior tiles: a tile passes if within ±2 in BOTH x and y directions there's some house-wall/solid tile. With 15% random walls remaining, the chance that a 5×1 horizontal window has at least one house wall = 1-0.85^5 ≈ 56%, and both directions ≈ 31% per tile. Many tiles fail → whole room fails (canSpawn=false → room invalid). So mostly invalid. 

Also light: vanilla cabins have NO torch (no torch placement in HouseBuilder). RoomNeeds requires light source → vanilla generated cabins FAIL the light requirement anyway! Wait, really? Let me confirm RoomNeeds requires light. WorldGen.RoomNeeds — let me check. Also does FillRooms place a light? choices = table, workbench (18), bookcase (86? no 86 is Dresser?), piano, bookcase (101)... `new Point(16, 0)` = 16 = ... hmm 16 is "Iron Anvil"? Actually tile 16 = Anvil? No. TileID 16 = "Anvil"? Let me not worry: no torch (4) or candelabra etc. Statue list includes 105 (torch statue)? GenVars.statueList includes torch statue (105) which doesn't produce light unless wired. So vanilla cave cabins lack light → not valid housing. That's consistent: in vanilla, underground cabins are NOT valid housing as generated (no light source, walls partly missing). Players must add torch + patch walls.

Hmm wait — but mushroom houses? Glowing mushroom? Not light tiles for housing (CountsAsTorch is TileID.Sets.CountsAsTorch). Anyway.

So the answer for the user: **In vanilla, generated structures cannot be claimed by NPCs spontaneously** because:
1. No whole-world house search (home anchor = existing housed NPC home or LastFoundHouse; validation radius ±10).
2. Generated underground cabins lack a light source (RoomNeeds fails) and underground wood cabins have walls cleared.

Therefore repo behavior = bug (B): `findFreeHouse` scans whole map (Housing.ts:370-372) including underground, so NPCs move into distant generated cabins. Also need to verify repo requires light — yes floodRoom requires hasLight (line 346). So how did the NPC move into a generated underground house in this repo? Because repo's CaveHousePass must place a light source? Let me check: does repo CaveHousePass place torches? Let me grep for torch/light in CaveHousePass.ts. Also VanillaSpawner.ts:107 WALL_HOUSE (spawn/VanillaSpawner.ts). Let me check both.

Also check Game.ts updateTownNpcArrival to see the call site and anchor.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:04:16.983Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"torch\\|Torch\\|light\\|Lantern\\|chandelier\\|candelabra\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts | head -20; echo ---; sed -n '95,125p' ~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts; echo ---; grep -rn \"updateTownNpcArrival\\|findFreeHouse\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | grep -v Housing.ts | head",
 "description": "Check cabin lights, spawner wall table, arrival call sites"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:04:17.078Z

**📎 ToolResult**

```
46:const CANDELABRA = TILE_BY_KEY['candelabra']!;
539:      placeFurniture(st, 'candelabra', x, y, rng.int(0, 5), 'top');
---
    LIHZAHRD_BRICK: get('v_226_lihzahrd_brick'),
    // 蘑菇族计数(SceneMetrics.cs:617)：71 植株/72 蘑菇树/528 藤（70 蘑菇草见上）
    MUSHROOM_PLANT: get('v_71_mushroom_plant'), MUSHROOM_TREE: get('v_72_mushroom_tree'),
    MUSHROOM_VINE: get('v_528_mushroom_vines'),
    // 190 发光蘑菇块（NPC.cs:5010/5109 glowshroom 出怪门 tile 70||190 之一）
    MUSHROOM_BLOCK: get('v_190_glowing_mushroom_block'),
    // Moss 族（TileID.Sets.Conversion.Moss，TileID.cs:38）：CheckToSpawnRockGolem 落脚门
    // 179 绿/180 黄/181 红/182 蓝/183 紫/381 熔岩/534 氪/536 氙/539 氩/625 氖/627 氦
    MOSS_GREEN: get('v_179_green_moss_block'), MOSS_YELLOW: get('v_180_yellow_moss_block'),
    MOSS_RED: get('v_181_red_moss_block'), MOSS_BLUE: get('v_182_blue_moss_block'),
    MOSS_PURPLE: get('v_183_purple_moss_block'), MOSS_LAVA: get('v_381_lava_moss'),
    MOSS_KRYPTON: get('v_534_krypton_moss_block'), MOSS_XENON: get('v_536_xenon_moss_block'),
    MOSS_ARGON: get('v_539_argon_moss_block'), MOSS_NEON: get('v_625_neon_moss_block'),
    MOSS_HELIUM: get('v_627_helium_moss_block'),
    // 恶地族补齐（SceneMetrics.cs:614-615）：661 腐化丛林草/400 腐化沙岩/662/401 猩红对位
    // （旧注释称引擎无 def——实际均已注册，按 0 计是漏）
    CORRUPT_JUNGLE_GRASS: get('v_661_corrupt_jungle_grass_block'),
    CORRUPT_SANDSTONE: get('v_400_corrupt_sandstone_block'),
    CRIMSON_JUNGLE_GRASS: get('v_662_crimson_jungle_grass_block'),
    CRIMSON_SANDSTONE: get('v_401_crimson_sandstone_block'),
  };
})();
/** 房屋墙表（Main.cs wallHouse[N]=true 全提取，265 项）：可由玩家放置的墙。
 *  FindSpawnTile L886：落点格带房屋墙 → 弃选（房屋内不刷怪的主守卫）；
 *  SetSpawnFlags L321：玩家所站格带房屋墙 → noWorms（房屋内不出蠕虫） */
const WALL_HOUSE = new Set([1, 4, 5, 6, 10, 11, 12, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 44, 45, 46, 47, 60, 66, 67, 68, 72, 73, 74, 75, 76, 77, 78, 82, 84, 85, 88, 89, 90, 91, 92, 93, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 167, 168, 169, 172, 173, 174, 175, 176, 177, 179, 181, 182, 183, 184, 186, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366]);

/** EvilTileCount 计数表(SceneMetrics.cs:614):23/661/24/25/32/112/163/400/398 计 1,27 向日葵 −10 */
const EVIL_LOOKUP = (() => {
  const t = new Uint8Array(TILE_DEFS.length);
  for (const id of [T.CORRUPT_GRASS, T.CORRUPT_JUNGLE_GRASS, T.EBONSTONE, T.CORRUPT_PLANT,
---
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:26:import { findFreeHouse, WALL_HOUSE } from '../world/Housing';
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2242:      // 商人/护士等由 checkTownArrival 按原版条件 + 房屋系统入住(见 updateTownNpcArrival)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3526:    if (this.tickCount % 7200 === 600) this.updateTownNpcArrival();
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10456:  private updateTownNpcArrival() {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10479:      const house = findFreeHouse(st, homes, this.world.spawnX, this.world.spawnY, n.vanillaId);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10547:    const house = findFreeHouse(st, homes, this.world.spawnX, this.world.spawnY, id);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:12147:  //  泛洪填充 + 原版 wallHouse 墙表 + 桌椅灯需求，见 checkRoom/findFreeHouse）

```


---

## 🤖 Assistant · 2026-08-13T10:04:32.341Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Important: repo CaveHousePass.ts line 539 places a CANDELABRA in cave houses! Original HouseBuilder has NO light placement. Let me verify: grep original CaveHouse for candelabra (tile 35?) or "PlaceTile(35". Candelabra is tile 35 in vanilla? Actually Candle=33, Candelabra=35, Chandelier=34? Hmm 34 = Bookcase? Let me check. Tile 33 = Candle, 35 = Candelabra? Actually: 33 Candle, 34 Bookcase?? no. Vanilla TileID: 33 = Candle? Let me check quickly: TileID.Candle = 33, TileID.Chandeliers = 34? In HouseBuilder.FillRooms there's `new Point(34, 0)` in choices — hmm, 34 with frameX += 54 (3 tiles wide) — that's a painting? Actually case 1 places tile 34 at room.Y+1 (top) and adds frameX 54 → that's a "Wall Hangings"? No wait: case 0 places RandHousePicture (paintings), case 1 places tile 34 at top row — tile 34 is "Chandelier"? Hmm: In choices: `new Point(16, 0)` (16 = ?), `new Point(86, 0)` (86 = Dresser), `new Point(94, 0)` (94 = ?), `new Point(101, BookcaseStyle)` (101 = Bookcase). 14=Table, 18=Workbench, 87=Piano. And 34 in case 1 — top placement with 3-wide → 34 = "Chandelier"! Yes! TileID 34 = Chandeliers. So vanilla cave cabins DO get chandeliers?? Hmm wait, case 1 happens for `i + num3 % 2 == 1` → alternating with paintings. So yes vanilla FillRooms places **Chandelier (tile 34)** as one of the 7 furniture choices? No wait — case 0/1 are in the first loop (num = width/8 positions): paintings or chandelier. Then second loop places statues/piles/tables/workbenches/pianos/bookcases.

So vanilla cave cabins DO contain chandeliers (light source!). OK so light requirement can be satisfied in vanilla cabins. Good — so my earlier claim was wrong; vanilla cabins have light.

So in vanilla: underground wood cabin has chandelier (light), door, table/workbench/piano/bookcase, chair (does it place chairs? ChairStyle exists... hmm `PlaceTile(..., 15, ChairStyle)`? I don't see chair placement in HouseBuilder.FillRooms! choices don't include chair (15). Hmm — ChairStyle property is set but where used? Maybe unused (dead config). Statues/piles/chests/tables/pianos/bookcases/chandeliers. Hmm, chairs? Vanilla cabins don't have chairs? The RoomNeeds requires chair. Hmm.

Let me check RoomNeeds in WorldGen.cs to see requirements, and whether chair is required. Search "CountsAsChair" in WorldGen.cs / RoomNeeds.

Anyway, the decisive difference is the **whole-map scan** in findFreeHouse. In vanilla, NPC home anchors to an existing housed NPC's home or LastFoundHouse, and QuickFindHome only validates ±10 around that anchor. Let me confirm LastFoundHouse semantics & the NPC.cs:56089 QuickFindHome call (per-frame homeless handling?). Let me check NPC.cs:56089 context.

Also repo Game.ts:10456-10550: uses spawnX/spawnY as anchor but findFreeHouse only uses anchor for tie-breaking distance, not for limiting scan range. So a generated cabin anywhere on the map (even deep underground) with door+table+chair+light wins. Also note repo's cave houses include chandeliers (light) — check whether repo places chairs/tables/doors to make them fully valid: yes it likely ports FillRooms (choices incl. table/workbench/piano/bookcase + candelabra). Chair? Let me grep for 'chair' in CaveHousePass.

Let me also check the repo call site 10456-10560 to see the homes/occupied and whether anchor restriction exists.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:04:32.648Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 60,
 "offset": 10456
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:04:32.657Z

**📎 ToolResult**

```
10456	  private updateTownNpcArrival() {
10457	    // 入侵/月事件进行中暂停城镇 NPC 入驻（SpawnHomelessNPC :4987 门；月事件原版经
10458	    // !dayTime 间接压制——本入驻轮无昼夜门，显式补 moonEventActive）
10459	    if (invasionActive(this.world) || moonEventActive(this.world)) return;
10460	    const npcs = this.entities.npcs.filter((n) => n instanceof TownNPC && !n.dead) as TownNPC[];
10461	    const has = (key: string) => npcs.some((n) => n.npcKey === key);
10462	    // npcId 随 home 携带（ScoreRoom 占用豁免 CanNPCsLiveWithEachOther 用）
10463	    const homes = npcs.filter((n) => n.home)
10464	      .map((n) => ({ x: n.home!.x, y: n.home!.y, npcId: n.vanillaId }));
10465	    const st = this.world.store;
10466	
10467	    // ①' 被绑巫师【不补放】（2026-08-13 对齐原版）：106 BoundWizard 唯一来源 =
10468	    // SpawnAnNPC 三人组链（NPC.cs:1999-2002，hardMode && 1/20 && 洞穴层深处门），
10469	    // VanillaSpawner 已 1:1——困难模式开启后由链自然掷出，入驻轮直接补放非原版
10470	    // （生成期 placeBoundRescueNpcs 同批移除，实证见 onWorldReady 注释）
10471	    // ①'' 睡渔夫补放（原版 SpawnNPC 海洋/沙滩分支每轮掷——补放近似其"未解救则持续在场"）
10472	    this.placeSleepingAngler();
10473	
10474	    // ① QuickFindHome（Main.cs:65072：每轮对未安家 NPC 找房入住）
10475	    // bound（被绑待救）不入住不搬动——原版 AI_007 bound 态原地，否则五个救援 NPC
10476	    // 会被塞进同一间空房叠在一点（读档/新世界 7200 tick 后必现）
10477	    for (const n of npcs) {
10478	      if (n.home || n.bound || n.npcKey === 'old_man') continue;
10479	      const house = findFreeHouse(st, homes, this.world.spawnX, this.world.spawnY, n.vanillaId);
10480	      if (!house) break;
10481	      n.home = { x: house.standX, y: house.standY };
10482	      n.leashHome = true; // 有家者白天在家附近游走
10483	      homes.push({ x: house.standX, y: house.standY, npcId: n.vanillaId });
10484	      n.x = house.standX * TILE + 8 - n.w / 2;
10485	      n.y = (house.standY + 1) * TILE - n.h;
10486	    }
10487	
10488	    // ② 优先级链（Main.cs num42 完整顺序；护士/爆破手要求商人在场，
10489	    //    染料商 ≥4 人、油漆工 ≥8 人、派对女孩 ≥20 人且 1/40 重掷）
10490	    const merchantHere = has('merchant');
10491	    const allow = (key: string) => this.townNpcSpawnAllowed(key);
10492	    const n = npcs.length; // num40：在场城镇 NPC 总数（含守卫老人，原版同）
10493	    // 严格按 Main.cs:65458-65570 num42 优先链原序（2026-08-13 对齐：补 angler
10494	    // 369/酒保 550、造型师归位到裁缝后、史莱姆第二轮按 :65557-65574 原序重排）
10495	    const prio: Array<[string, boolean]> = [
10496	      ['guide', !has('guide')],
10497	      ['merchant', !merchantHere && allow('merchant')],
10498	      ['nurse', !has('nurse') && merchantHere && allow('nurse')],
10499	      ['arms_dealer', !has('arms_dealer') && allow('arms_dealer')],
10500	      ['goblin_tinkerer', !has('goblin_tinkerer') && allow('goblin_tinkerer')],
10501	      ['wizard', !has('wizard') && allow('wizard')],
10502	      ['dryad', !has('dryad') && allow('dryad')],
10503	      ['demolitionist', !has('demolitionist') && merchantHere && allow('demolitionist')],
10504	      ['witch_doctor', !has('witch_doctor') && allow('witch_doctor')],
10505	      ['steampunker', !has('steampunker') && allow('steampunker')],
10506	      ['mechanic', !has('mechanic') && allow('mechanic')],
10507	      ['angler', !has('angler') && allow('angler')],            // :65489（369）
10508	      ['cyborg', !has('cyborg') && allow('cyborg')],
10509	      ['pirate', !has('pirate') && allow('pirate')],
10510	      ['clothier', !has('clothier') && allow('clothier')],
10511	      ['stylist', !has('stylist') && allow('stylist')],         // :65506（354，裁缝后）
10512	      ['dyer', !has('dyer') && n >= 4 && allow('dyer')],
10513	      ['painter', !has('painter') && n >= 8],
10514	      ['party_girl', !has('party_girl') && n >= 20 && allow('party_girl')],
10515	      ['santa_claus', !has('santa_claus') && allow('santa_claus')],

```


---

## 🤖 Assistant · 2026-08-13T10:04:33.279Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"chair\\|Chair\\|placeFurniture\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts | head -20; echo ---; grep -n \"RoomNeeds\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs | head -5",
 "description": "Cabin furniture and original RoomNeeds"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:04:33.362Z

**📎 ToolResult**

```
163:function placeFurniture(st: TileStore, key: string, x: number, y: number, style = 0, anchor: 'bottom' | 'top' = 'bottom'): boolean {
535:      placeFurniture(st, key, x, y, style);
539:      placeFurniture(st, 'candelabra', x, y, rng.int(0, 5), 'top');
552:        placeFurniture(st, 'v_186_decos_3x2', x, y, rng.int(22, 25));
559:        placeFurniture(st, key, x, y, style);
705:      if (placeFurniture(st, key, rng.int(2, r.w - 3) + r.x, y)) return true;
708:      if (placeFurniture(st, key, x, y)) return true;
---
4675:		if (!RoomNeeds())
5359:		if (!RoomNeeds())
5616:	public static bool RoomNeeds()
5622:		for (int i = 0; i < TileID.Sets.RoomNeeds.CountsAsChairTypes.Length; i++)
5624:			if (houseTile[TileID.Sets.RoomNeeds.CountsAsChairTypes[i]])

```


---

## 🤖 Assistant · 2026-08-13T10:04:36.420Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me check RoomNeeds 5616-5665 for the requirements, and check repo CaveHousePass FillRooms: what furniture keys it places (line 520-560) — do they include chair? Also check whether repo cave houses have doors placed (PlaceDoors). If repo cabins include door+table+chair+light... chair might be missing. But user observed NPC moved in, so all four requirements must have been met — or repo light detection treats something else as light. Let me read CaveHousePass 500-570 to see the FillRooms port.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:04:36.684Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts",
 "limit": 65,
 "offset": 505
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:04:36.707Z

**📎 ToolResult**

```
505	    ], r.x + 1, rowY, r.w - 2, 1);
506	  }
507	  // ③ 墙 216(DesertHouseBuilder.cs:34):Dither(0.8)+Blotches()+OnlyWalls(187)
508	  genRect(st, rng, [
509	    { k: 'dither', p: 0.8 }, B2(0.3), { k: 'onlyWalls', types: [def.wall] }, { k: 'placeWall', wall: 216 },
510	  ], r.x, r.y, r.w, r.h);
511	}
512	
513	// ---------- FillRooms(画/烛台交替 + 装饰循环) ----------
514	function fillRooms(st: TileStore, rng: RNG, r: Rect, def: ThemeDef, theme: Theme): void {
515	  // 家具七选(HouseBuilder.FillRooms choices;沙漠 Tables2 → tile 469)
516	  const choices: Array<[string, number]> = [
517	    [def.tables2 ? 'v_469_tables_group_2' : 'table', def.table],
518	    ['anvil', 0],
519	    ['workbench', def.workbench],
520	    ['v_86_loom', 0],
521	    ['piano', def.piano],
522	    ['keg', 0],
523	    ['bookcase', def.bookcase],
524	  ];
525	  // 画/烛台交替:switch(i + parity%2) 仅 0/1 两档有内容(i≥2 落空,原版同款)
526	  const n = Math.floor(r.w / 8);
527	  const step = Math.floor(r.w / (n + 1));
528	  const parity = rng.int(0, 1);
529	  for (let i = 0; i < n; i++) {
530	    const x = (i + 1) * step + r.x;
531	    if ((i + (parity % 2)) % 2 === 0) {
532	      // 画:Y + min(H/2, H-5)
533	      const y = r.y + Math.min(Math.floor(r.h / 2), r.h - 5);
534	      const [key, style] = theme === 'desert' ? randHousePictureDesert(rng) : randHousePicture(rng);
535	      placeFurniture(st, key, x, y, style);
536	    } else {
537	      // 烛台:顶行悬挂(原版 +54 点亮帧——本引擎烛台恒点亮,帧差不建模)
538	      const y = r.y + 1;
539	      placeFurniture(st, 'candelabra', x, y, rng.int(0, 5), 'top');
540	    }
541	  }
542	  // 装饰循环:W/8+3 件
543	  const decoCount = Math.floor(r.w / 8) + 3;
544	  for (let k = 0; k < decoCount; k++) {
545	    const x = rng.int(0, r.w - 4) + 1 + r.x;
546	    const y = r.y + r.h - 2;
547	    switch (rng.int(0, 3)) {
548	      case 0: // 小堆 185(PlaceSmallPile size1:style*18)
549	        if (!activeAt(st, x, y)) st.setTileSilent(x, y, SMALL_PILE, rng.int(31, 33) * 18, 0);
550	        break;
551	      case 1: // 骨堆 186
552	        placeFurniture(st, 'v_186_decos_3x2', x, y, rng.int(22, 25));
553	        break;
554	      case 2: // 雕像(statueList[Next(2, len)],陷阱雕像照接)
555	        placeStatue(st, x, y, rng.int(2, STATUE_LIST.length - 1));
556	        break;
557	      case 3: {
558	        const [key, style] = choices[rng.int(0, choices.length - 1)];
559	        placeFurniture(st, key, x, y, style);
560	        break;
561	      }
562	    }
563	  }
564	}
565	
566	// ---------- 楼梯 / 门 / 平台 / 梁 ----------
567	/** CreateStairsList + PlaceStairs:相邻房间对角平台链 + 顶步 4×1 平台 + 斜坡 */
568	function placeStairs(st: TileStore, rooms: Rect[], def: ThemeDef): void {
569	  for (let i = 1; i < rooms.length; i++) {

```


---

## 🤖 Assistant · 2026-08-13T10:04:36.944Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs",
 "limit": 50,
 "offset": 5616
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:04:36.971Z

**📎 ToolResult**

```
5616		public static bool RoomNeeds()
5617		{
5618			roomChair = false;
5619			roomDoor = false;
5620			roomTable = false;
5621			roomTorch = false;
5622			for (int i = 0; i < TileID.Sets.RoomNeeds.CountsAsChairTypes.Length; i++)
5623			{
5624				if (houseTile[TileID.Sets.RoomNeeds.CountsAsChairTypes[i]])
5625				{
5626					roomChair = true;
5627					break;
5628				}
5629			}
5630			for (int j = 0; j < TileID.Sets.RoomNeeds.CountsAsTableTypes.Length; j++)
5631			{
5632				if (houseTile[TileID.Sets.RoomNeeds.CountsAsTableTypes[j]])
5633				{
5634					roomTable = true;
5635					break;
5636				}
5637			}
5638			for (int k = 0; k < TileID.Sets.RoomNeeds.CountsAsTorchTypes.Length; k++)
5639			{
5640				if (houseTile[TileID.Sets.RoomNeeds.CountsAsTorchTypes[k]])
5641				{
5642					roomTorch = true;
5643					break;
5644				}
5645			}
5646			for (int l = 0; l < TileID.Sets.RoomNeeds.CountsAsDoorTypes.Length; l++)
5647			{
5648				if (houseTile[TileID.Sets.RoomNeeds.CountsAsDoorTypes[l]])
5649				{
5650					roomDoor = true;
5651					break;
5652				}
5653			}
5654			if (roomChair && roomTable && roomDoor && roomTorch)
5655			{
5656				canSpawn = true;
5657			}
5658			else
5659			{
5660				canSpawn = false;
5661			}
5662			return canSpawn;
5663		}
5664	
5665		public static void QuickFindHome(int npc)

```


---

## 🤖 Assistant · 2026-08-13T10:04:45.882Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Original RoomNeeds requires chair+table+door+torch(light). Vanilla cave cabins: FillRooms places chandelier (tile 34 — is 34 in CountsAsTorchTypes? Chandeliers are light sources, yes tile 34 is in the CountsAsTorch list probably) but **no chairs** (ChairStyle never used to place tile 15 in HouseBuilder). Wait — is there any chair? grep HouseBuilder for "15" — `WorldGen.PlaceTile(num4, num5, 34, ...)` and choices. No 15. So vanilla cabins lack chairs → **vanilla generated cave cabins can NEVER be valid housing** (missing chair requirement)! Interesting. Hmm, but let me double check CountsAsChairTypes includes bed (87?) and throne... Vanilla: chairs, beds, thrones count as chairs. Beds: tile 87 is Piano... TileID 87 = Piano; 88 = Bookcase? Let me check: Bookcase=101, Piano=87, Dresser=86 (dresser counts as table? no, dresser counts as... hmm), Keg=94? keg, Loom=86? Actually choices: (14 table),(16,0),(18 workbench),(86,0),(87 piano),(94,0),(101 bookcase). 16 = ? "Anvil"? no anvil=16? Hmm 16 is... TileID 16 = "Anvil"? Repo maps: 'anvil' for 16, 'v_86_loom' for 86, 'keg' for 94. OK. None are chairs.

So in vanilla, generated cabins (any type) are NOT valid housing because no chair. Wait — but desert houses: `PlaceBiomeSpecificTool` for jungle places sharpener (377), desert bast statue/extractinator. No chairs. Statue list: could include... statues are 105-family, not chairs.

Hmm, but wait: does anything else place chairs in cabins? Vanilla underground cabins sometimes have chairs in-game... Actually yes! I recall vanilla cabins DO sometimes contain chairs... Let me double check whether Chairs get placed elsewhere in the CaveHouse gen — maybe in CaveHouseBiome.cs. Let me grep CaveHouseBiome.cs and the folder for "15" chair placement.

Also, even if a cabin were valid (chair aside), the decisive point remains: vanilla NPCs never scan the world for homes.

Let me quickly grep the CaveHouse folder for PlaceTile with 15.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:04:47.368Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"PlaceTile(.*15[,)]\\|, 15,\\|ChairStyle\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/ ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes/CaveHouseBiome.cs 2>/dev/null | head; echo ---; grep -rn \"CountsAsChairTypes\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/TileID.cs | head -3; grep -n \"= 15;\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ID/TileID.cs | head -5",
 "description": "Check chair placement in vanilla cabin gen"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:04:47.451Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/WoodHouseBuilder.cs:21:		base.ChairStyle = 0;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/IceHouseBuilder.cs:22:		base.ChairStyle = 30;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseUtils.cs:136:			result3.Width = Utils.Clamp(result2.X - result.X, 15, 30);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseUtils.cs:140:			result3.Width = Utils.Clamp(result2.X - result.X, 15, 30);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/DesertHouseBuilder.cs:23:		base.ChairStyle = 43;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/MushroomHouseBuilder.cs:21:		base.ChairStyle = 9;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/JungleHouseBuilder.cs:22:		base.ChairStyle = 3;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:48:	public int ChairStyle { get; protected set; }
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:136:			ChairStyle = WorldGen.genRand.Next(44);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:276:					ChairStyle = 44;
---
ugrep: warning: ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/TileID.cs: No such file or directory
ugrep: warning: ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ID/TileID.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-13T10:05:00.060Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: `ChairStyle` is set everywhere but **never used to place a chair** in vanilla cave house generation. So vanilla generated cabins never contain chairs → RoomNeeds fails → **vanilla: generated underground cabins can never be claimed as housing by NPCs** (automatically or even via housing query, unless player adds a chair).

Wait, actually the housing query also runs RoomNeeds, so even the player can't flag a cabin without adding furniture. Right.

Plus double gate: even if a cabin had furniture, vanilla QuickFindHome never scans the world (anchor = existing housed NPC home / LastFoundHouse, ±10 validation only).

So user's observed behavior (NPC self-moves into generated underground structure) is impossible in vanilla → it's a repo deviation. Root cause candidates in repo:

1. **findFreeHouse whole-map scan** (Housing.ts:370-372): y from 3 to h-4, x from 3 to w-3 — includes deep underground. Vanilla has no whole-map search; anchor-based ±10 only (QuickFindHome, WorldGen.cs:5684-5691). Game.ts:10479/10547 pass spawn as anchor but anchor only tie-breaks distance, doesn't restrict candidates.

2. Repo cabins: do they place chairs? Repo fillRooms choices: table/anvil/workbench/loom/piano/keg/bookcase — same as vanilla, no chair. But statues: repo placeStatue uses STATUE_LIST — does that include a chair? No. So how did the NPC move in? Maybe repo's chair detection `countsAsChair` matches something else, e.g. 'bed'? Not placed in cabins. Hmm. Or maybe the structure was a different one (e.g., shrine/other gen). Or repo `countsAsChair(key)` matches "throne"... Let me check: does repo place `statue` tiles whose key contains 'chair'? Or maybe the room flood-found a nearby different area including a chair. Or maybe the light: candelabra counts as light (def.light) ✓; table ✓ (workbench/table); door ✓ (PlaceDoors); chair — hmm.

Wait — maybe repo's CaveHousePass placeStatue with STATUE_LIST that may include tile 'v_105_statues'... no chairs. Let me check whether the repo's cabin has chair via any route... Actually maybe the user's structure is a different one (e.g. `EnchantedSwordShrine` or a "living tree"?). Or maybe repo counts "keg"? 'keg' doesn't contain 'chair'. 'v_86_loom'? no. 'anvil'? no. Hmm.

Let me check whether repo has other gen structures that place chairs (e.g. Pyramid? LivingTree? FloatingIsland houses?). Also check `STATUE_LIST` contents. But maybe more relevant: check what `def.light` is for candelabra, and whether `countsAsChair` may be satisfied by the throne in... Let's search repo for structures that place door+table+chair+light. E.g. gen may port "floating island house" with full furniture. Let me grep gen dir for 'chair'.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:05:00.604Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rln \"chair\" ~/Project/GLM/SandboxWorld/game/src/world/gen/ | head -20; echo ---; grep -rn \"STATUE_LIST\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts | head -3",
 "description": "Find gen structures placing chairs"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:05:00.678Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/IslandHousePass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TemplePass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts
---
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:16:import { STATUE_LIST, STATUES_WITH_TRAPS, placeStatueTrap } from './StatuesPass';
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:188:  const [sheet, style] = STATUE_LIST[idx];
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:555:        placeStatue(st, x, y, rng.int(2, STATUE_LIST.length - 1));

```


---

## 🤖 Assistant · 2026-08-13T10:05:08.834Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So IslandHousePass (floating island house), LivingTreePass, TemplePass (lihzahrd temple?), DungeonPass place chairs. Floating islands are in the sky, not underground. Living trees — surface. So what underground structure has a full furniture set including chair?

Wait — maybe the NPC didn't need a chair because `countsAsChair` in Housing.ts matches key.includes('chair') || sheet===15||21. In cave house, statues: statueList includes... no.

Hold on: maybe the room the NPC entered isn't a CaveHouse but a **CaveHouse that also contains a "throne" from statue list**? no.

Alternatively — maybe the user's world structure is a generated "地下小屋/神龛" (shrine) from another pass, e.g. `EnchantedSwordShrinePass`, `DesertTemple`, `JungleTemple`, `PyramidPass`. Let me grep for structures placing door+chair+table+light combos underground. Let me check which passes place 'door' and 'chair'.

Actually more efficient: grep all gen files for placeFurniture/tile with 'chair'.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:05:09.495Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"'chair'\\|\\\"chair\\\"\\|chair\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/IslandHousePass.ts ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TemplePass.ts ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts | head -20; echo ---; grep -rn \"door\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts | head -10",
 "description": "Inspect chair/door placement in island/livingtree/temple passes"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:05:09.584Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TemplePass.ts:718:              : { tile: TILE_BY_KEY['chair']!, style: 12 };
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/IslandHousePass.ts:15:const CHAIR = TILE_BY_KEY['chair']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:48:const CHAIR = TILE_BY_KEY['chair']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:26:const CHAIR = TILE_BY_KEY['chair']!;
---

```


---

## 🤖 Assistant · 2026-08-13T10:05:21.925Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
LivingTreePass has CHAIR const. Let me check how it's used and whether living trees place doors/tables/lights. But living trees are surface structures. The user said "地下世界生成时就有的房子（地下小屋/神龛等天然结构）". Hmm "神龛" = shrine.

Let me check LivingTreePass usage of CHAIR and also see if there are underground structures with full furniture: check `grep -rn "DOOR\b" gen`. Alternatively, check TemplePass:718 chair — temple (jungle temple) has chairs but lihzahrd brick walls (226) IS a house wall in WALL_HOUSE? 226 is in WALL_HOUSE (yes, line: 225 226 227). Jungle temple rooms: do they have doors? Temple doors are tile 10 (closed door) with special style? Lihzahrd door (tile 385?)... Temple has furniture: chairs, tables, workbenches, torches? And doors are tile 10 (in 1.4.4 temple doors are regular doors that only open with temple key). If repo places tile 10 doors + table + chair + torch in the temple, then the temple room is a valid house in repo → NPC moves into the jungle temple deep underground! In vanilla, temple doors are tile 10 but locked doors (tile 10 with... no, temple doors are tile 10 in 1.4; they're locked until Plantera). Also vanilla NPC would still not scan there.

Let me look at TemplePass.ts:718 context and check for door/table/light placement there.

Also check LivingTreePass: living tree houses? In 1.4, living trees can have a small room inside with furniture? Hmm.

Let me check both quickly. Also there might be "ShrinePass" (Enchanted Sword Shrine) with no furniture.

Priority: the fix recommendation. The key deviation is the whole-map scan in findFreeHouse (Housing.ts:361-391) + call sites Game.ts:10479/10547. Vanilla semantics: new NPC home anchor = random housed NPC's home (or LastFoundHouse/spawn), then QuickFindHome validates only ±10 around anchor. So fix: restrict candidate scan to a radius around anchor (e.g. spawn or existing homes), or iterate anchors from existing homes.

Let me quickly check TemplePass for doors+light to explain "神龛/地下小屋" move-in.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:05:22.727Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '690,740p' ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TemplePass.ts; echo ===; grep -n \"DOOR\\|door\\|torch\\|Torch\\|table\\|workbench\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TemplePass.ts | head -25",
 "description": "Check temple furniture/doors/lights"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:05:22.795Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
      }
      if (fails > 10000) break;
    }
  }

  // ---- 4. 蜥蜴家具（cs:34585-34632）：预算 = 房数×1.35×(1+Next(-15,26)%) ----
  //  Next(3)（cs:34608-34630 原文配对，勿旋转）：0→工作台 18 style10 /
  //  1→桌 14 style9 / 2→椅 15 style12（曾把三对整体错抄一位→神庙出木椅）
  {
    let budget = tRooms * 1.35 * (1 + rng.int(-15, 25) * 0.01);
    let fails = 0;
    while (budget > 0) {
      fails++;
      const x2 = rng.int(lx, rx);
      const y2 = rng.int(ty, by);
      if (st.inBounds(x2, y2) && st.wall[st.idx(x2, y2)] === 87 && !st.flags[st.idx(x2, y2)]) {
        let fy = y2;
        while (st.inBounds(x2, fy) && !st.flags[st.idx(x2, fy)]) {
          fy++;
          if (fy > by) break;
        }
        fy--;
        if (fy <= by) {
          const kind = rng.int(0, 2);                 // Next(3)
          const spec = kind === 0
            ? { tile: TILE_BY_KEY['workbench']!, style: 10 }
            : kind === 1
              ? { tile: TILE_BY_KEY['table']!, style: 9 }
              : { tile: TILE_BY_KEY['chair']!, style: 12 };
          if (placeFurn(st, x2, fy, spec.tile, spec.style)) budget -= 1;
        }
      }
      if (fails > 10000) break;
    }
  }

  // ---- 5. 墙挂饰 240 style88（cs:34634-34682）：数量 = 1 + (w>4200) + (w>6400?Next(2):0) ----
  {
    let count = 1;
    if (st.w > 4200) count++;
    if (st.w > 6400) count += rng.int(0, 1);
    let fails = 0;
    while (count > 0) {
      fails++;
      const x2 = rng.int(lx, rx);
      const y2 = rng.int(ty, by);
      if (st.inBounds(x2, y2) && st.wall[st.idx(x2, y2)] === 87 && !st.flags[st.idx(x2, y2)]) {
        // ±70 内已有 240，或 ±4 内有蜥蜴砖 226 → 拒绝（cs:34654-34675）
        let flag = false;
        for (let dx = -70; dx <= 70 && !flag; dx++) {
          for (let dy = -70; dy <= 70; dy++) {
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-13T10:05:23.215Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"CHAIR\\|DOOR\\|TABLE\\|TORCH\\|workbench\\|table\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts | head -25",
 "description": "Check living tree furniture"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:05:23.267Z

**📎 ToolResult**

```
26:const CHAIR = TILE_BY_KEY['chair']!;
222:    if (placeFurniture(st, CHAIR, num8, Y, 5) && num < 0) {
233:    if (placeFurniture(st, CHAIR, num8, Y, 5) && num > 0) {
354:        if (typeAt(st, n11 - 1, n10) === T.DOOR_CLOSED || typeAt(st, n11 + 1, n10) === T.DOOR_CLOSED) flag4 = true;
357:          if (typeAt(st, n11, n10) === T.DOOR_CLOSED) flag4 = true;
361:      if (typeAt(st, n11 - 1, n10) === T.DOOR_CLOSED || typeAt(st, n11 + 1, n10) === T.DOOR_CLOSED) flag5 = true;
364:        if (typeAt(st, n11, n10) === T.DOOR_CLOSED) flag5 = true;

```


---

## 🤖 Assistant · 2026-08-13T10:05:46.089Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Temple has workbench/table/chair but walls 87 (Lihzahrd Brick Wall? no—87 is a wall id in temple... wait `st.wall === 87` — hmm, that's the temple wall check). Wall 87 is NOT in WALL_HOUSE (list has 84,85,88,89,90,91,92,93 but not 87). Hmm, so temple rooms have wall 87 → not house wall → loose evidence may still pass where near bricks (solid). Temple rooms are large (>750 tiles?) → flood fails on size anyway. Also doors: temple door tiles? Let me not go down this path too far.

The user's actual observation: NPC moved into "地下小屋" (underground cabin). For that to happen in repo: cabin needs door+table+chair+light. Cabin has door ✓ (PlaceDoors), table/workbench ✓ (choices), candelabra light ✓, chair ✗. Hmm.

Unless... statue list includes "v_105...". Let me check STATUE_LIST contents in StatuesPass — could include sheet 15? No, statues are sheet 105.

Wait — maybe Housing's `countsAsChair` also matches "bed"? key.includes('chair')... Let me check TILE_DEFS keys for something in a cabin that includes 'chair'. Keg? no. Loom? no. Bookcase? no. Piano? no. Anvil? no. Hmm.

OR maybe the room flood in the cabin leaked into a neighboring area that had a chair? Unlikely.

Alternatively, maybe the user's "地下小屋/神龛" includes other structures like the Desert temple/Pyramid? Let me check PyramidPass for furniture. Also check "EnchantedSwordShrine". Also `CheckRoom` requires hasLight via def.light — maybe many tiles are flagged light.

Better: rather than chasing which structure, verify repo cabin truly has chair or not. Let me look at placeStatue/STATUE_LIST and also check the cabin door pass (placeDoors) — need to confirm cabin actually places doors (PlaceDoors). Yes: placeStairs/placeDoors exist (line 568+). Let me quickly check whether repo cabin places a chair somewhere else (e.g., line ~700: chest placing). Let me grep CaveHousePass for 'v_15' or sheet 15.

Actually, better approach: run a quick check on a generated world? Too heavy. Let me grep CaveHousePass for all placeFurniture keys used: lines 535, 539, 552, 559, 705, 708, plus statue. The 705/708 are chest. So no chair in cabins.

Hmm, so how did NPC move into a cabin? Maybe `countsAsTable`/`countsAsChair` heuristic over-matches: `countsAsChair(key, sheet)`: key.includes('chair') || key.includes('throne') || sheet===15 || sheet===21. Sheet 21 = toilet? Actually vanilla sheet 21 = "Toilet"? TileID 21 = Toilet? Hmm: TileID 21 = Toilet! In vanilla, toilets count as chairs (CountsAsChair includes toilets? hmm). Anyway statues have sheet 105, decor 186.

Wait — maybe 'v_186_decos_3x2' key... no.

Hmm, what about `def.light` on the candelabra ✓.

Alternatively the user might be seeing NPC home at a **Living Tree** interior or **Pyramid** or a **floating island house** that sank? No.

Let me reconsider: maybe repo cave cabin places **chairs via statue list**? Let me print STATUE_LIST from StatuesPass.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:05:46.122Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"STATUE_LIST\\s*=\\|export const STATUE_LIST\" -A 12 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StatuesPass.ts | head -25; echo ---; grep -rn \"DOOR\\|door\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts | head -12",
 "description": "Statue list and cabin doors"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:05:46.195Z

**📎 ToolResult**

```
12:export const STATUE_LIST: Array<[number, number]> = (() => {
13-  const list: Array<[number, number]> = [];
14-  for (let i = 0; i < 44; i++) list.push([105, i]);
15-  list[34] = [349, 0];
16-  list[43] = [105, 50];
17-  for (const s of [63, 64, 65, 66, 68, 69, 70, 71, 72, 73, 75,
18-    51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62,
19-    77, 78, 67, 74, 37, 2]) list.push([105, s]);
20-  return list;
21-})();
22-
23-const STATUE = STATUE_LIST;
24-
---
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:24:  tile: number; wall: number; beam: number; door: number; platformStyle: number;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:36:  wood:     { tile: T.WOOD, wall: 27, beam: TILE_BY_KEY['v_124_wooden_beam']!, door: 0, platformStyle: 0, chestStyle: 1, table: 0, workbench: 0, piano: 0, bookcase: 0 },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:37:  ice:      { tile: TILE_BY_KEY['v_321_boreal_wood']!, wall: 149, beam: TILE_BY_KEY['v_574_boreal_beam']!, door: 30, platformStyle: 19, chestStyle: 11, table: 28, workbench: 23, piano: 23, bookcase: 25 },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:38:  jungle:   { tile: TILE_BY_KEY['v_158_rich_mahogany']!, wall: 42, beam: TILE_BY_KEY['v_575_rich_mahogany_beam']!, door: 2, platformStyle: 2, chestStyle: 8, table: 2, workbench: 2, piano: 2, bookcase: 12 },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:39:  desert:   { tile: TILE_BY_KEY['sandstone']!, wall: 187, beam: TILE_BY_KEY['v_577_sandstone_column']!, door: 43, platformStyle: 42, chestStyle: 10, chestTile2: true, tables2: true, table: 7, workbench: 39, piano: 38, bookcase: 39 },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:40:  granite:  { tile: TILE_BY_KEY['v_369_smooth_granite_block']!, wall: 181, beam: TILE_BY_KEY['v_576_granite_column']!, door: 34, platformStyle: 28, chestStyle: 50, table: 33, workbench: 29, piano: 28, bookcase: 30 },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:41:  marble:   { tile: TILE_BY_KEY['v_357_smooth_marble_block']!, wall: 179, beam: TILE_BY_KEY['v_561_marble_column']!, door: 35, platformStyle: 29, chestStyle: 51, table: 34, workbench: 30, piano: 29, bookcase: 31 },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:42:  mushroom: { tile: TILE_BY_KEY['v_190_glowing_mushroom_block']!, wall: 74, beam: TILE_BY_KEY['v_578_mushroom_beam']!, door: 6, platformStyle: 18, chestStyle: 32, table: 27, workbench: 7, piano: 22, bookcase: 24 },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:621:        placeDoorClosed(st, x, exitY, def.door);

```


---

## 🤖 Assistant · 2026-08-13T10:06:12.903Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Statue 349 is the "Wall Anchor"? Hmm 349 = "ItemFrame"? no, 349 is... Actually statue list[34] = [349,0] = "Teleporter"? No — vanilla statue list includes the "Wall Safe"? Hmm, 349 = "Logic Sensor"? Let me not worry.

Important: some statue styles include **349 which is "Female/Male mannequin"?** no. In vanilla GenVars.statueList, entry 34 = tile 349 which is... let me check: tile 349 = "Teleportation Portal"? Hmm. Actually I recall statue list includes "Lihzahrd statue" and the "Sealed/"... Not needed.

OK — chairs aren't in cabins. So how did NPC move in? Let me check whether Housing flood requires hasChair strictly... yes line 346: `!hasDoor || !hasTable || !hasChair || !hasLight`. Hmm.

Unless the countsAsChair heuristic matches `v_105...` statue keys? No. But wait — sheet 21: TILE_DEFS sheet 21 might be "toilet" and statue styles? no, statues are sheet 105.

Alternatively, maybe the structure the user saw is the **IslandHouse** (sky) that's not underground, or a **Living Tree** room. Living tree: places CHAIR (line 222/233) and doors? Let me check LivingTreePass for table/light/door placement — line 354 checks DOOR_CLOSED, meaning the tree's interior scan treats doors... Let me read the LivingTreePass region around 200-240 to see the room furniture. But the user says underground.

Hmm — maybe the actual structure is the **Desert temple (Pyramid)**? Let me check PyramidPass furniture.

Alternatively, maybe the user's NPC moved into a **floating island house** — no, underground.

Wait, maybe more simply: the user might be using the word 地下世界 loosely and the structure could be a **ruined house / cave cabin** in which the repo has chairs because `fillRooms` choices include... no chairs.

Let me be efficient and instead verify empirically-ish: grep the repo for gen structures that place all four (door, table, chair, light). Compute: files placing chair AND door:
- IslandHousePass, TemplePass, LivingTreePass, DungeonPass place chairs.
Underground ones: TemplePass (jungle temple, wall 87 not house wall... but flood wall check has the loose-evidence fallback — solid tiles count as evidence! The temple interior tiles adjacent to bricks pass; center tiles >2 from bricks fail... temple rooms are large though).
- DungeonPass: dungeon has chairs (DungeonPass CHAIR const). Dungeon walls (41/62/63?) — wall 41 IS in WALL_HOUSE (41 present!). Hmm! Dungeon walls are 41 (blue brick), 61? Let me check: DungeonPass CHAIR, and dungeon brick walls. If repo dungeon has door + table + chair + torch and wall 41 (which is in WALL_HOUSE), then a dungeon room could be a valid house in repo! In vanilla, dungeon walls: 41 is blue dungeon brick wall which IS player-placeable (wallHouse true). But vanilla dungeon rooms: do they have doors? Dungeon doors exist (tile 10 locked? no, dungeon uses tile 10 doors that are locked until Skeletron?). Vanilla dungeon rooms have doors (locked dungeon doors - tile 384?). Vanilla has "Dungeon Door" = tile 10 with special? In 1.4, dungeon doors are tile 384 (DoorOpen?) Hmm. Also vanilla NPC wouldn't scan there anyway.

This is getting deep. The conclusion is already solid regardless of which structure: **the deviation is the whole-map house scan + (possibly) cabin furniture/light looseness**, and vanilla never auto-claims generated structures.

For the report, the load-bearing facts:

**原版事实**:
1. 原版无"全图找房"：QuickFindHome (WorldGen.cs:5665-5727) 只校验 NPC 现有 homeTile（home±1，再 home±10 螺旋）。新 NPC 的 home 锚点 = SpawnHomelessNPC (WorldGen.cs:5012-5033) 从**已安家 NPC 的 home** 随机取，或 LastFoundHouse（WorldGen.cs:5002）。Main.cs:65092 每轮对已安家 NPC 重校验。
2. 墙判定（CheckRoom WorldGen.cs:6150-6185）：每个空气格需自身 wall ∈ wallHouse，或 ±2 横竖窗口内出现 wallHouse 墙 / 实心 tile / HousingWalls tile——天然墙（土/石 1? no）不在 wallHouse 则靠"附近实心"豁免；没有任何"必须地表/出生点附近"的位置限制（只要求离世界边 ≥10，StartRoomCheck :6010）。
3. **生成的小屋在原版不能成为住房**：CaveHouse 的 FillRooms (HouseBuilder.cs:421-504) 只放 画/烛台(34)/桌(14)/工作台(18)/织布机(86)/钢琴(87)/酒桶(94)/书架(101)/雕像/箱 — **从不放椅子**（ChairStyle 配置全文件无处使用），RoomNeeds (WorldGen.cs:5616-5663) 四件套缺 chair 直接 fail。另外 WoodHouseBuilder.AgeRoom (:36) 对地下房间把 27 号木墙按 Dither(0.85) 清墙——墙也不完整。所以原版生成结构（无论地表/地下）天然不满足住房。
4. 沙漠小屋墙 187 → aged 216：216 不在 wallHouse；granite/marble 180/178、jungle 64、mushroom 清墙 —— 这些墙也不在 wallHouse。

**本仓差异**:
- Housing.ts:361-391 findFreeHouse 全图扫描（y 3..h-4 / x 3..w-3），anchor (spawnX/spawnY) 只做同分距离 tie-break，不限制候选 → 任何地点（含深层地下）的合格房间都会被入住。Housing.ts:355 注释自认"全图找房为本仓库自有——原版无"。
- Game.ts:10479 / 10547 调用点。
- CaveHousePass.ts 墙/家具 1:1（含烛台 539、清墙 385/400/448/466/486/509）→ 与原版一致，不是偏差源。但需注意：repo cabin 无椅子 → 单个 cabin 理论上仍不该合格；用户看到的可能是有椅子的其它生成结构（Temple/Dungeon/LivingTree/IslandHouse 均放椅子）——但根因同样是全图扫描。
- WALL_HOUSE 表 (Housing.ts:21-37) 与原版 265 项一致（含 187/216 排除一致）→ 无 wallHouse 门缺失。

结论 B：根因 = findFreeHouse 全图扫描（原版无此概念），修复 = 原版语义：新 NPC 的找房应锚定"已有住房 NPC 的 home（随机）或出生点"，候选仅 ±10（QuickFindHome WorldGen.cs:5684-5691）内做 StartRoomCheck/RoomNeeds/ScoreRoom；Game.ts:10477-10486 循环应改为对锚点邻域校验而非全图找最优房。

Let me double check one thing quickly: does the DungeonPass place chairs+doors+table+light underground? That would explain the user report concretely ("地下世界生成时就有的房子"). Let me grep DungeonPass for door/torch/table.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:06:13.572Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"CHAIR\\|TABLE\\|WORKBENCH\\|TORCH\\|DOOR\\|table\\|torch\\|door\\|workbench\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts | head -20",
 "description": "Dungeon furniture check"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:06:13.646Z

**📎 ToolResult**

```
25:const DOOR = TILE_BY_KEY['door_closed']!;
47:const TABLE = TILE_BY_KEY['table']!;
48:const CHAIR = TILE_BY_KEY['chair']!;
49:const WORKBENCH = TILE_BY_KEY['workbench']!;
52:const ALCHEMY = TILE_BY_KEY['v_355_alchemy_table']!;
53:const BEWITCH = TILE_BY_KEY['v_354_bewitching_table']!;
200:  const doorStyle = theme === 0 ? 16 : theme === 1 ? 17 : 18;  // Item 1411-1413 placeStyle
204:  const doorData: DDoor[] = [];
961:        doorData.push({ x: num - 1, y, dir: -1, hall: false, skipOther: false, skipSpace: false, clear: true, fluff: 3 }); f4 = true;
964:        doorData.push({ x: num2 + 1, y, dir: 1, hall: false, skipOther: false, skipSpace: false, clear: true, fluff: 3 }); f5 = true;
972:    if (Math.abs(hl.sdy) <= 0.1) doorData.push({ x: Math.trunc(hl.sx), y: Math.trunc(hl.sy), dir: 0, hall: true, skipOther: false, skipSpace: false, clear: true, fluff: 0 });
974:    if (Math.abs(hl.edy) <= 0.1) doorData.push({ x: Math.trunc(hl.ex), y: Math.trunc(hl.ey), dir: 0, hall: true, skipOther: false, skipSpace: false, clear: true, fluff: 0 });
1201:    if (t === DOOR) return false;                       // IsLockedDoor(style13)
1206:    for (const d of doorData) {
1208:      const style = rn(3) === 0 ? doorStyle : 13;
1227:              if (inW(a, b, 0) && actAt(a, b) !== 0 && typAt(a, b) === DOOR) { flag = false; break outer1; }
1327:      st.flags[ti] = 1; st.type[ti] = DOOR;
1794:      const anchor = (dgSolid(a - 1, b) && typAt(a - 1, b) !== DOOR)
1795:        || (dgSolid(a + 1, b) && typAt(a + 1, b) !== DOOR) || dgSolid(a, b + 1);
1887:    const badAnchor = (xx: number, yy: number): boolean => typAt(xx, yy) === DOOR || typAt(xx, yy) === SPIKE;

```


---

## 🤖 Assistant · 2026-08-13T10:06:18.481Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Dungeon places doors (tile 10, some style 13 locked), tables, chairs, workbenches — and dungeon walls (41/61/62?) Let me check which wall ids dungeon uses: 41 (blue) is in WALL_HOUSE. Dungeon also places torches? grep TORCH: none found in first 20 (the grep matched only door/table/chair/workbench lines). Let me check torch in DungeonPass.

Actually the dungeon rooms have chandeliers/candles? Vanilla dungeon has "dungeon candle"? Hmm. Let me check for light in DungeonPass quickly. But regardless — this is a plausible concrete source: dungeon rooms with door+table+chair+light+wall41 → valid house in repo → NPC moves into dungeon. That matches "地下世界生成时就有的房子".

Let me grep for light-emitting furniture in DungeonPass (candle/chandelier/candelabra/lantern).
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:06:19.494Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"candle\\|CANDLE\\|chandelier\\|CHANDELIER\\|candelabra\\|lantern\\|LANTERN\\|light\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts | head -12; echo ---; grep -n \"WALL\\|wall =\\|setWallSilent\\|wall:\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts | head -12",
 "description": "Dungeon lights and wall ids"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:06:19.557Z

**📎 ToolResult**

```
7:// （相对序 A→B→Seed→shelf→lantern→skewed）——pre-dungeon 检查点哈希保持现状。
28:const LANTERN = TILE_BY_KEY['lantern']!;
29:const CHANDELIER = TILE_BY_KEY['chandelier']!;
40:const CANDELABRA = TILE_BY_KEY['candelabra']!;
44:const CANDLE = TILE_BY_KEY['candle']!;
45:const WATER_CANDLE = TILE_BY_KEY['water_candle']!;
194:  const lantern = [rn(7), 0, 0];      // cs:255-266
195:  do { lantern[1] = rn(7); } while (lantern[1] === lantern[0]);
196:  lantern[2] = rn(7);
197:  while (lantern[2] === lantern[0] || lantern[2] === lantern[1]) lantern[2] = rn(7);
1691:                placeSimple(x, y, n12v === 49 ? WATER_CANDLE : TILE_BY_KEY['v_13_bottles']);
1733:              if (inW(a, b, 0) && actAt(a, b) !== 0 && (typAt(a, b) === LANTERN || typAt(a, b) === CHANDELIER)) {
---
65:const DG_DUNGEON_WALLS = new Set([7, 8, 9, 94, 95, 96, 97, 98, 99]);
176:  const wall = theme === 0 ? 7 : theme === 1 ? 8 : 9;
178:  const wallVariants: number[] = wall === 8 ? [8, 98, 99] : wall === 9 ? [9, 96, 97] : [7, 94, 95];
2265:  const isDW = (v: number): boolean => v > 0 && DG_DUNGEON_WALLS.has(v);   // 墙 id 即原版 id
2427:  const wall = st.inBounds(x, y) ? st.wall[st.idx(x, y)] : 0;
2428:  const rx = wall === mainWall ? 15 : 8;
2429:  const ry = wall === mainWall ? 10 : 5;

```


---

## 🤖 Assistant · 2026-08-13T10:06:27.403Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Dungeon walls 7/8/9/94-99 — none are in WALL_HOUSE (list has no 7,8,9,94-99). So dungeon interior walls aren't house walls → the flood wall check: air tiles with wall 7 need loose evidence (house wall/solid tile within ±2 both axes). Deep inside a dungeon room (>2 tiles from brick), that fails → room invalid. Unless dungeon rooms are small. Hmm.

OK. I've spent enough. The precise structure isn't critical — but I should be honest about which structures qualify. What about LivingTreePass? Living tree = surface-ish but tree interior rooms: chair placed; walls? Living tree walls are wood 27? no — living tree interior walls: 227? Let me check quickly what wall living tree uses and whether it places door/table/light. Actually, let me just check one candidate with all four: grep LivingTreePass for table/torch/door/light.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:06:28.038Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"TABLE\\|WORKBENCH\\|TORCH\\|CANDLE\\|CHANDELIER\\|CANDELABRA\\|LANTERN\\|DOOR_CLOSED\\|table\\|torch\\|door\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts | head -15; echo ---; grep -n \"wall\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts | head -8",
 "description": "Living tree furniture and walls"
}
```


---

## 👤 User(sidechain) · 2026-08-13T10:06:28.099Z

**📎 ToolResult**

```
354:        if (typeAt(st, n11 - 1, n10) === T.DOOR_CLOSED || typeAt(st, n11 + 1, n10) === T.DOOR_CLOSED) flag4 = true;
357:          if (typeAt(st, n11, n10) === T.DOOR_CLOSED) flag4 = true;
361:      if (typeAt(st, n11 - 1, n10) === T.DOOR_CLOSED || typeAt(st, n11 + 1, n10) === T.DOOR_CLOSED) flag5 = true;
364:        if (typeAt(st, n11, n10) === T.DOOR_CLOSED) flag5 = true;
---
33:/** Main.wallDungeon（cs:10777 起）= 地牢墙族 */
53:function wallAt(st: TileStore, x: number, y: number): number {
54:  return st.inBounds(x, y) ? st.wall[st.idx(x, y)] : 0;
151:  const wl = wallAt(st, x, y);
177:      if (wallAt(st, i, j) === 0 && !activeAt(st, i, j) && j < worldSurface) return;
189:      if (wallAt(st, k, l) !== WALL_LIVING_WOOD && sheetAt(st, k, l) !== 19) setLivingWood(st, k, l);
193:        st.wall[i] = WALL_LIVING_WOOD;
207:      if (wallAt(st, m, n) !== WALL_LIVING_WOOD && sheetAt(st, m, n) !== 19) setLivingWood(st, m, n);

```


---

## 🤖 Assistant · 2026-08-13T10:06:52.089Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Living tree uses living wood walls (192?) — WALL_LIVING_WOOD value? Not critical.

I have enough. Time to write the report (≤30 lines).

Let me also confirm: the repo scoreRoom uses `st.wall` via WALL_HOUSE — the gate exists (Housing.ts:310). And hasLooseWallEvidence replicates 6150-6185. So the wall logic is 1:1. The deviation is solely the scan scope + the fact repo cave cabins... hmm wait, one more possibility I should verify quickly: does repo's cave cabin place a chair via `def`? No. So a plain cave cabin can't be a valid house in repo either (no chair). Then what did the user see? Options: (a) a cabin adjacent to something with a chair; (b) jungle temple / dungeon / living tree / island house; (c) the loose-evidence wall rule + a chair from another structure. Or (d) — hmm, `countsAsTable` matches key.includes('table'): 'v_355_alchemy_table' etc. And maybe `countsAsChair` matches... 'workbench'? no.

Wait — actually! Check `countsAsChair(key, sheet)`: sheet === 15 → chair sheet. And statue 349? sheet of tile 349 = 349. Hmm. What about `'v_186_decos_3x2'` sheet 186.

Hmm, one more: desert tables2 'v_469_tables_group_2' - contains 'table' ✓ (table). Chairs? No.

So I'll note in the report: cave cabin itself lacks a chair in both vanilla and repo, so the structure the user saw likely had a chair (jungle temple/dungeon/living tree/island house all place chairs in this repo) — but regardless the root cause is the whole-map scan: vanilla never searches the world for a house; it only validates ±10 around an anchor (existing NPC home / LastFoundHouse / spawn). Also note vanilla generated cabins can never be housing (no chair, walls partly cleared).

Actually, wait. I should double-check the jungle temple: does TemplePass place doors and lights? If temple rooms are within 750 tiles and have wall 87 (not house wall) — loose evidence would fail for center tiles. Let me not verify further; the conclusion stands.

One more check worth doing: are there other underground structures with house walls + full furniture? E.g. PyramidPass (desert pyramid: wall 227? gold brick?) Let me check PyramidPass quickly for chair/table/door/light — pyramids are underground-ish (desert) and their walls are sandstone brick (216?) which is NOT house wall. Fine.

Let me write the report now, concise ≤30 lines, with file:line refs.

Key line refs:
- Original:
  - WorldGen.cs:5665-5727 QuickFindHome (锚点±10 only; :5684-5691 ±10 螺旋)
  - WorldGen.cs:4985-5033 SpawnHomelessNPC (锚点=已安家 NPC home 随机 / :5002 LastFoundHouse)
  - Main.cs:65092 每轮 QuickFindHome 重校验
  - WorldGen.cs:6150-6185 CheckRoom 墙判定（wallHouse 或 ±2 实心/HousingWalls 豁免；wall==0→HoleInWallIsTooBig）
  - WorldGen.cs:6010 无地表/出生点位置限制（仅离世界边≥10）
  - WorldGen.cs:5616-5663 RoomNeeds 四件套
  - HouseBuilder.cs:421-504 FillRooms 无椅子（ChairStyle 死配置）；WoodHouseBuilder.cs:36 地下清墙
- Repo:
  - src/world/Housing.ts:361-391 findFreeHouse 全图扫描（:370-372 y 3..h-4 / x 3..w-3）；anchor 仅同分 tie-break（:380-381）；:355 注释自认原版无全图找房
  - src/world/Housing.ts:21-37 WALL_HOUSE 与原版 265 项一致（无缺门）；:310/:277-290 墙判定 1:1
  - src/core/Game.ts:10477-10486（每 7200 tick 轮）/ :10479 / :10547 调用
  - CaveHousePass.ts:36-42 墙 id 与原版一致（27/149/42/187/181/179/74）；:385/:400/:448/:466/:486/:509 清墙/换墙 1:1
- 结论 B。修复建议。

Also mention: vanilla generated cabin can never be housing because no chair → so NPC living in a generated structure is impossible in vanilla even before considering scan scope. Therefore B.

Fix suggestion (precise):
1. Game.ts updateTownNpcArrival ① 轮：改为原版 SpawnHomelessNPC+QuickFindHome 语义——锚点取 `homes` 随机一项（或 spawn），在锚点 ±10（每 2 格）+锚点±1 邻域做 StartRoomCheck/RoomNeeds/ScoreRoom；禁止全图扫描。
2. 或者最小改动：findFreeHouse 加半径限制（如锚点 ±10 内才枚举门），且 Game.ts 传入锚点为已有 home 随机/spawn 而非仅 spawn。

I'll write it in Chinese, ≤30 lines.
```

</details>


---

## 🤖 Assistant · 2026-08-13T10:06:56.566Z · glm-x-preview-260804

```
## 调查结论：**B（本仓判定偏差）**——不是墙判定，是"找房扫描范围"

### 原版事实（Terarria1456/）
1. **原版根本没有"全图找房"**。`QuickFindHome`（`Terraria/WorldGen.cs:5665-5727`）只对 NPC **既有 homeTile** 校验：先 home±1（:5675-5680），再 **home ±10 螺旋**（:5684-5691），之外不搜索。新 NPC 的 home 锚点来自 `SpawnHomelessNPC`（`WorldGen.cs:5012-5033`）= **从"已安家 NPC 的 home"里随机取一个**，或 `LastFoundHouse`（:5002）；`Main.cs:65092` 每轮只对已有 home 重校验。
2. 墙判定（`CheckRoom`，`WorldGen.cs:6150-6185`）：空气格需自身墙 ∈ `Main.wallHouse`，否则在 ±2 横竖窗口内出现 wallHouse 墙 / 实心 tile / `TileID.Sets.HousingWalls` 即豁免；wall==0 且无证据 → HoleInWallIsTooBig。**没有任何"必须近地表/出生点"的位置限制**（`StartRoomCheck` :6010 只查离世界边 ≥10）。`RoomNeeds`（:5616-5663）要求门+桌+**椅**+灯四件套。
3. **生成的小屋在原版永远不是合法住房**：`HouseBuilder.FillRooms`（`Terraria.GameContent.Biomes.CaveHouse/HouseBuilder.cs:421-504`）只放画/烛台34/桌14/工作台18/织布机86/钢琴87/酒桶94/书架101/雕像/箱——**从不放椅子**（`ChairStyle` 是死配置，全目录仅赋值无使用）；且 `WoodHouseBuilder.cs:36` 对地下房间按 Dither(0.85) **清墙**（27 号木墙）。缺椅 → RoomNeeds 必 fail。墙 id：wood 27（house 墙）/ ice 149 / jungle 42 / desert 187→aged 216（**均非 house 墙**，216/187 不在 wallHouse）/ granite 181→aged 180 / marble 179→178 / mushroom 清墙。

### 本仓现状
- `game/src/world/Housing.ts:361-391` `findFreeHouse` **全图扫描**（:370-372 `y=3..h-4, x=3..w-3` 枚举每扇门），anchor（`Game.ts:10479/10547` 传 spawnX/spawnY）**只做同分距离 tie-break，不限制候选**——任意深层地下的合格房都会被入住。`:355` 注释自认"全图找房为本仓库自有——原版无"。
- 墙判定**无偏差**：`Housing.ts:310`（wallHouse 门）+ `:277-290 hasLooseWallEvidence`（6150-6185 1:1）；`WALL_HOUSE`（:21-37）与原版 265 项逐条一致（187/216 同样排除）。`CaveHousePass.ts:36-42` 墙 id 与原版完全一致，清墙/换墙链（:385/400/448/466/486/509）也是 1:1。
- 附注：仓库洞穴小屋同样**不放椅子**（`CaveHousePass.ts:516-523` choices 七件套同原版），单间 cabin 理论上不该合格——用户看到的更可能是有椅子的其它生成结构（`TemplePass.ts:718`、`DungeonPass.ts:48`、`LivingTreePass.ts:26`、`IslandHousePass.ts:15` 均放椅子，其中神庙/地牢在地下），但根因相同。

### 修复建议（精确）
- `Game.ts:10477-10486` 入驻轮改为原版 `SpawnHomelessNPC`+`QuickFindHome` 语义：锚点 = `homes` 随机一项（首个 NPC 用 spawn/LastFoundHouse），仅在锚点 ±10（步长 2）+ ±1 邻域做房间校验+打分，**删除全图枚举**。
- 最小改法：`Housing.ts:370-372` 加锚点半径门（如 `|x-ax|<=10 && |y-ay|<=10` 才枚举门），且 `Game.ts:10479` 锚点改传随机已有 home 而非固定 spawn。
```
