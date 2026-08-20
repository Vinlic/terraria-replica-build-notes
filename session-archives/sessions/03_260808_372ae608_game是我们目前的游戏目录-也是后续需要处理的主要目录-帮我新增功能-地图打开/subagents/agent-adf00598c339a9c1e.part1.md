# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-11T05:43:01.590Z

```
你在 ~/Project/GLM/SandboxWorld/ 项目工作。Terraria 复刻，必须 1:1 对齐反编译源码 Terarria1456/（1.4.5.6）。

任务：**只读审查**（禁止修改任何文件），对照原版 NPC 刷怪【选点链与 flag/zone 链】，产出差异清单。

原版：Terarria1456/Terraria/NPC.cs SpawnAnNPC 前半（选点部分，约 L820-1186）：随机点→skyMob 判定→向下找落脚面→HasTileSpawnSpace→CheckNotSpawningOnScreen→GetProperGroundSpawnTileTypeAndWallType→PostCheckChosenSpawnTile（地牢门）→waterTile/xRange 等 flag 设置；以及 L5306+ 的 HasTileSpawnSpace、L5344 CheckNotSpawningOnScreen、SpawnNPC 里的 spawnRate/maxSpawns 计算（约 L700-820，getSpawnRate 对应原版哪段）。
我们的：game/src/world/spawn/VanillaSpawner.ts 全文件（858 行），重点 findSpawnTile（约 418 行起）、hasTileSpawnSpace、checkNotSpawningOnScreen、setFlagsForChosenTile（约 240-300）、getSpawnRate（约 351 行起）、Zone 判定（约 294 行附近）。

已知：skyMob 判定我们改成了"露天高空"语义（兼容存量中央浮空岛，有意为之，勿报告）；海洋/海滩 x 阈值已改为 van 缩放（勿报告）。

重点检查：
1. 选点扫描范围（spawnArea 的 L/R/T/B 与 viewHalf 的关系，原版 rangeX/rangeY 公式 vs 我们的 ×1.4/×1.04）。
2. 向下找落脚面的扫描上限与边界（我们 areaB；原版是不是到世界底部或别的）。
3. waterTile 判定（原版 L957 附近：落脚格上方两格液体且是水——我们 248 行；原版是否还检查液体量阈值 255/byte 单位换算——我们 liquid 是 0-255 还是 0-1 归一？查 TileStore.liquid 的语义并与原版 tile.liquid byte 语义对齐！我们 `st.liquid[above1] > 0` 阈值是否对应原版）。
4. Zone 判定窗口（SceneMetrics 169×123 计数 ≥300）我们 294 行注释声称对齐，抽查几个 Zone 的计数条件。
5. getSpawnRate：原版 spawnRate 公式（L? 搜索 "spawnRate" 或 timeRate）逐分支对照我们的 351-417。
6. 尝试次数上限（我们 50 次）与原版对应。

产出（≤50 行）：差异清单（每条：我们文件:行 / 原版锚点 / 原版语义 / 我们现状 / 是否真 bug）。不要修改文件。
```

---

## 📎 Attachment · skill_listing · 2026-08-11T05:43:01.592Z

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

## 🤖 Assistant · 2026-08-11T05:43:03.233Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by exploring the relevant files. This is a read-only review task comparing the decompiled Terraria 1.4.5.6 source NPC.cs spawn logic against our VanillaSpawner.ts implementation.

Let me find the files first.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:43:03.880Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/src/world/spawn/ && wc -l ~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts && ls ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "List spawn dir and check file sizes"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:43:03.930Z

**📎 ToolResult**

```
VanillaSpawner.ts
     873 ~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs

```


---

## 🤖 Assistant · 2026-08-11T05:43:04.444Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"SpawnAnNPC\\|HasTileSpawnSpace\\|CheckNotSpawningOnScreen\\|GetProperGroundSpawnTileTypeAndWallType\\|PostCheckChosenSpawnTile\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -40",
 "description": "Locate spawn functions in NPC.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:43:04.479Z

**📎 ToolResult**

```
196:					if (TrySpawnAnNPC(player))
204:		private bool TrySpawnAnNPC(Player player)
220:			if (!CheckNotSpawningOnScreen(spawnTileX, spawnTileY))
226:			GetProperGroundSpawnTileTypeAndWallType(spawnTileX, spawnTileY, out spawnTileType, out spawnWallType);
227:			if (!PostCheckChosenSpawnTile(spawnTileX, spawnTileY, spawnTileType, spawnWallType))
247:			SpawnAnNPC(spawnTileX, spawnTileY, spawnTileType, xRange, player.whoAmI);
910:				if (!safeArea.Contains(spawnTileX, spawnTileY) && HasTileSpawnSpace(spawnTileX, spawnTileY))
922:		private bool PostCheckChosenSpawnTile(int spawnTileX, int spawnTileY, int spawnTileType, int spawnWallType)
1186:		public void SpawnAnNPC(int spawnTileX, int spawnTileY, int spawnTileType, bool xRange, int target)
5306:		public static bool HasTileSpawnSpace(int spawnTileX, int spawnTileY)
5344:		public static bool CheckNotSpawningOnScreen(int spawnTileX, int spawnTileY)
5789:		public static void GetProperGroundSpawnTileTypeAndWallType(int x, int y, out int spawnTileType, out int spawnWallType)
5922:					if (!safeArea.Contains(num3, num4) && CheckNotSpawningOnScreen(num3, num4))
62774:				if (checkPlayerScreenRanges && !Spawner.CheckNotSpawningOnScreen((int)vector3.X, (int)vector3.Y))
81413:				if (flag && !flag2 && !Spawner.HasTileSpawnSpace(num10, num11))
81422:			if ((!flag || flag2 || Spawner.CheckNotSpawningOnScreen(num10, num11)) && flag)

```


---

## 🤖 Assistant · 2026-08-11T05:43:06.350Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The decompiled NPC.cs appears different from the expected line numbers (L820-1186). Let me look at the structure. Let me read the relevant sections: SpawnNPC spawnRate computation (~L700-820), TrySpawnAnNPC (~L204), the spawn selection (~L820-1186?), HasTileSpawnSpace (L5306), CheckNotSpawningOnScreen (L5344), GetProperGroundSpawnTileTypeAndWallType (L5789).

Let me read multiple sections in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:43:06.666Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '150,330p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read NPC.cs L150-330 (TrySpawnAnNPC etc)"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:43:06.704Z

**📎 ToolResult**

```
		public bool ZoneWaterCandle;

		public bool ZonePeaceCandle;

		public bool ZoneShadowCandle;

		public int defaultTarget = 255;

		public Spawner()
		{
			numberOfActivePlayers = Main.CurrentFrameFlags.ActivePlayersCount;
			float num = 0f;
			for (int i = 0; i < Main.maxNPCs; i++)
			{
				if (Main.npc[i].active)
				{
					switch (Main.npc[i].type)
					{
					case 315:
					case 325:
					case 327:
					case 328:
					case 344:
					case 345:
					case 346:
						num += Main.npc[i].npcSlots;
						break;
					}
				}
			}
			int num2 = (int)((float)defaultMaxSpawns * (2f + 0.3f * (float)numberOfActivePlayers));
			reachedInvasionBossCap = num >= (float)(numberOfActivePlayers * num2);
		}

		public void SpawnNPC()
		{
			for (int i = 0; i < 255; i++)
			{
				Player player = Main.player[i];
				if (CanSpawnEnemiesNear(player))
				{
					if (Main.slimeRain)
					{
						SlimeRainSpawns(player);
					}
					if (TrySpawnAnNPC(player))
					{
						break;
					}
				}
			}
		}

		private bool TrySpawnAnNPC(Player player)
		{
			SetSpawnFlags(player);
			GetSpawnRate(player, out var spawnRate, out var maxSpawns);
			if (player.nearbyActiveNPCs >= (float)maxSpawns)
			{
				return false;
			}
			if (Main.rand.Next(spawnRate) != 0)
			{
				return false;
			}
			if (!FindSpawnTile(player, out var spawnTileX, out var spawnTileY, out var xRange))
			{
				return false;
			}
			if (!CheckNotSpawningOnScreen(spawnTileX, spawnTileY))
			{
				return false;
			}
			int spawnTileType = 0;
			int spawnWallType = 0;
			GetProperGroundSpawnTileTypeAndWallType(spawnTileX, spawnTileY, out spawnTileType, out spawnWallType);
			if (!PostCheckChosenSpawnTile(spawnTileX, spawnTileY, spawnTileType, spawnWallType))
			{
				return false;
			}
			SetSpawnFlagsForChosenTile(spawnTileX, spawnTileY, spawnTileType, spawnWallType);
			if (dualDungeonsSpawnRules && ZoneDungeon)
			{
				if (!player.ZoneDungeon)
				{
					ZoneDungeon = false;
				}
				else
				{
					Tile tile = Main.tile[pX, pY];
					if (tile == null || !Main.wallDungeon[tile.wall])
					{
						ZoneDungeon = false;
					}
				}
			}
			SpawnAnNPC(spawnTileX, spawnTileY, spawnTileType, xRange, player.whoAmI);
			if (Main.netMode == 2)
			{
				SyncNewlySpawnedNPCs();
			}
			return true;
		}

		public static bool CanSpawnEnemiesNear(Player player)
		{
			if (!player.active || player.dead)
			{
				return false;
			}
			if (Main.IsJourneyMode)
			{
				CreativePowers.SpawnRateSliderPerPlayerPower power = CreativePowerManager.Instance.GetPower<CreativePowers.SpawnRateSliderPerPlayerPower>();
				if (power != null && power.GetIsUnlocked() && power.GetShouldDisableSpawnsFor(player.whoAmI))
				{
					return false;
				}
			}
			if (player.isNearNPC(398, MoonLordFightingDistance))
			{
				return false;
			}
			return true;
		}

		private void SetSpawnFlags(Player player)
		{
			pX = (int)player.Center.X / 16;
			pY = (int)player.Center.Y / 16;
			luck = player.luck;
			dayTime = Main.dayTime;
			raining = Main.raining;
			skyMob = false;
			spawnFriendly = false;
			ignoreSafeWalls = false;
			waterTile = false;
			nearGranite = false;
			nearMarble = false;
			spawnSpider = false;
			spawnUndergroundDesert = false;
			hardDungeon = downedPlantBoss && Main.hardMode;
			ZoneCorrupt = player.ZoneCorrupt;
			ZoneCrimson = player.ZoneCrimson;
			ZoneHallow = player.ZoneHallow;
			ZoneJungle = player.ZoneJungle;
			ZoneSnow = player.ZoneSnow;
			ZoneGlowshroom = player.ZoneGlowshroom;
			ZoneMeteor = player.ZoneMeteor;
			ZoneGraveyard = player.ZoneGraveyard;
			ZoneDungeon = player.ZoneDungeon;
			ZoneLihzhardTemple = player.ZoneLihzhardTemple;
			ZoneSandstorm = player.ZoneSandstorm;
			ZoneTowerSolar = player.ZoneTowerSolar;
			ZoneTowerVortex = player.ZoneTowerVortex;
			ZoneTowerNebula = player.ZoneTowerNebula;
			ZoneTowerStardust = player.ZoneTowerStardust;
			ZoneOldOneArmy = player.ZoneOldOneArmy;
			ZoneWaterCandle = player.ZoneWaterCandle;
			ZonePeaceCandle = player.ZonePeaceCandle;
			ZoneShadowCandle = player.ZoneShadowCandle;
			dualDungeonsSpawnRules = Main.dualDungeonsSeed;
			inDualDungeon = dualDungeonsSpawnRules && player.insideUnbreakableWalls;
			tresspassingDualDungeon = inDualDungeon && DangerousDungeonCurse.GetProgressPlayerCanSafelyMatch() < DangerousDungeonCurse.GetProgressPlayerNeedsToMatch(player);
			invaders = ShouldSpawnInvasionEnemies(player.position);
			if (ZoneTowerSolar || ZoneTowerNebula || ZoneTowerVortex || ZoneTowerStardust)
			{
				invaders = true;
				ignoreSafeWalls = true;
			}
			townNPCs = player.townNPCs;
			noWorms = WorldGen.InWorld(pX, pY) && Main.wallHouse[Main.tile[pX, pY].wall];
			noGroundWorms = player.afkCounter >= Player.AFKTimeNeededForNoWormSpawns;
			skyBehindPlayer = Main.wallLight[Main.tile[pX, pY].wall] || Main.tile[pX, pY].wall == 73;
			livingTree = Main.tile[pX, pY].wall == 244;
			inRemixStartingArea = Main.remixWorld && (double)(player.Center.X / 16f) > (double)Main.maxTilesX * 0.39 + 50.0 && (double)(player.Center.X / 16f) < (double)Main.maxTilesX * 0.61;
			offensiveToTim = (player.armor[1].type == 4256 || (player.armor[1].type >= 1282 && player.armor[1].type <= 1287)) && player.armor[0].type != 238;
			playerHasStartingHealth = player.statLifeMax <= 100;
			if (ZoneShadowCandle)
			{
				noWorms = false;

```


---

## 🤖 Assistant · 2026-08-11T05:43:07.073Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '600,930p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read NPC.cs L600-930 (SpawnNPC spawnRate)"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:43:07.181Z

**📎 ToolResult**

```
					spawnRate = (int)((float)spawnRate * 0.7f);
				}
				else if ((double)player.nearbyActiveNPCs < (double)maxSpawns * 0.4)
				{
					spawnRate = (int)((float)spawnRate * 0.9f);
				}
			}
			if (Main.remixWorld && (double)(player.position.Y / 16f) < Main.worldSurface && (ZoneCorrupt || ZoneCrimson))
			{
				spawnRate = (int)((double)spawnRate * 0.8);
				maxSpawns *= 2;
			}
			if (player.invis)
			{
				spawnRate = (int)((float)spawnRate * 1.2f);
				maxSpawns = (int)((float)maxSpawns * 0.8f);
			}
			if (player.calmed)
			{
				spawnRate = (int)((float)spawnRate * 1.65f);
				maxSpawns = (int)((float)maxSpawns * 0.6f);
			}
			if (player.sunflower)
			{
				spawnRate = (int)((float)spawnRate * 1.2f);
				maxSpawns = (int)((float)maxSpawns * 0.8f);
			}
			if (player.anglerSetSpawnReduction)
			{
				spawnRate = (int)((float)spawnRate * 1.3f);
				maxSpawns = (int)((float)maxSpawns * 0.7f);
			}
			if (player.enemySpawns)
			{
				spawnRate = (int)((double)spawnRate * 0.5);
				maxSpawns = (int)((float)maxSpawns * 2f);
			}
			if (ZoneWaterCandle)
			{
				if (!ZonePeaceCandle)
				{
					spawnRate = (int)((double)spawnRate * 0.75);
					maxSpawns = (int)((float)maxSpawns * 1.5f);
				}
			}
			else if (ZonePeaceCandle)
			{
				spawnRate = (int)((double)spawnRate * 1.3);
				maxSpawns = (int)((float)maxSpawns * 0.7f);
			}
			if (ZoneWaterCandle && (double)(player.position.Y / 16f) < Main.worldSurface * 0.3499999940395355)
			{
				spawnRate = (int)((double)spawnRate * 0.5);
			}
			if (player.isNearFairy())
			{
				spawnRate = (int)((float)spawnRate * 1.2f);
				maxSpawns = (int)((float)maxSpawns * 0.8f);
			}
			if ((double)spawnRate < (double)defaultSpawnRate * 0.1)
			{
				spawnRate = (int)((double)defaultSpawnRate * 0.1);
			}
			if (maxSpawns > defaultMaxSpawns * 3)
			{
				maxSpawns = defaultMaxSpawns * 3;
			}
			if (Main.getGoodWorld)
			{
				spawnRate = (int)((float)spawnRate * 0.8f);
				maxSpawns = (int)((float)maxSpawns * 1.2f);
			}
			if (Main.IsJourneyMode)
			{
				CreativePowers.SpawnRateSliderPerPlayerPower power = CreativePowerManager.Instance.GetPower<CreativePowers.SpawnRateSliderPerPlayerPower>();
				if (power != null && power.GetIsUnlocked() && power.GetRemappedSliderValueFor(player.whoAmI, out var value))
				{
					spawnRate = (int)((float)spawnRate / value);
					maxSpawns = (int)((float)maxSpawns * value);
				}
			}
			if ((Main.pumpkinMoon || Main.snowMoon) && (Main.remixWorld || (double)player.position.Y < Main.worldSurface * 16.0))
			{
				maxSpawns = (int)((double)defaultMaxSpawns * (2.0 + 0.3 * (double)numberOfActivePlayers));
				spawnRate = 20;
			}
			if (DD2Event.Ongoing && ZoneOldOneArmy)
			{
				maxSpawns = defaultMaxSpawns;
				spawnRate = defaultSpawnRate;
			}
			if (invaders)
			{
				maxSpawns = (int)((double)defaultMaxSpawns * (2.0 + 0.3 * (double)numberOfActivePlayers));
				spawnRate = 20;
			}
			if (ZoneDungeon && !downedBoss3)
			{
				spawnRate = 10;
			}
			if (WorldGen.Skyblock.lowTiles)
			{
				spawnRate /= 2;
			}
			bool flag = ZoneCorrupt || ZoneCrimson;
			if (Main.infectedSeed)
			{
				flag = false;
			}
			if (!invaders && ((!Main.bloodMoon && !Main.pumpkinMoon && !Main.snowMoon) || Main.dayTime) && (!Main.eclipse || !Main.dayTime) && !flag && !ZoneCrimson && !ZoneMeteor && !ZoneOldOneArmy)
			{
				if (player.Center.Y / 16f > (float)Main.UnderworldLayer && !inRemixStartingArea)
				{
					if (townNPCs == 1)
					{
						if (!WorldGen.Skyblock.lowTiles)
						{
							if (Main.rand.Next(2) == 0)
							{
								noWorms = true;
							}
							if (Main.rand.Next(10) == 0)
							{
								spawnFriendly = true;
								maxSpawns = (int)((double)(float)maxSpawns * 0.5);
							}
							else
							{
								spawnRate = (int)((double)(float)spawnRate * 1.25);
							}
						}
					}
					else if (townNPCs == 2)
					{
						if (Main.rand.Next(4) != 0)
						{
							noWorms = true;
						}
						if (Main.rand.Next(5) == 0)
						{
							spawnFriendly = true;
							maxSpawns = (int)((double)(float)maxSpawns * 0.5);
						}
						else
						{
							spawnRate = (int)((double)(float)spawnRate * 1.5);
						}
					}
					else if (townNPCs >= 3)
					{
						if (Main.rand.Next(10) != 0)
						{
							noWorms = true;
						}
						if (Main.rand.Next(3) == 0)
						{
							spawnFriendly = true;
							maxSpawns = (int)((double)(float)maxSpawns * 0.5);
						}
						else
						{
							spawnRate = (int)((float)spawnRate * 2f);
						}
					}
				}
				else if (townNPCs == 1)
				{
					noWorms = true;
					if (!WorldGen.Skyblock.lowTiles)
					{
						if (ZoneGraveyard && (!ZonePeaceCandle || Main.rand.Next(3) == 0))
						{
							spawnRate = (int)((double)(float)spawnRate * 1.66);
							if (Main.rand.Next(9) == 1)
							{
								spawnFriendly = true;
								maxSpawns = (int)((double)(float)maxSpawns * 0.6);
							}
						}
						else if (Main.rand.Next(3) == 1)
						{
							spawnFriendly = true;
							maxSpawns = (int)((double)(float)maxSpawns * 0.6);
						}
						else
						{
							spawnRate = (int)((float)spawnRate * 2f);
						}
					}
				}
				else if (townNPCs == 2)
				{
					noWorms = true;
					if (ZoneGraveyard && (!ZonePeaceCandle || Main.rand.Next(3) == 0))
					{
						spawnRate = (int)((double)(float)spawnRate * 2.33);
						if (Main.rand.Next(6) == 1)
						{
							spawnFriendly = true;
							maxSpawns = (int)((double)(float)maxSpawns * 0.6);
						}
					}
					else if (Main.rand.Next(3) != 0)
					{
						spawnFriendly = true;
						maxSpawns = (int)((double)(float)maxSpawns * 0.6);
					}
					else
					{
						spawnRate = (int)((float)spawnRate * 3f);
					}
				}
				else if (townNPCs >= 3)
				{
					noWorms = true;
					if (ZoneGraveyard && (!ZonePeaceCandle || Main.rand.Next(3) == 0))
					{
						spawnRate = (int)((float)spawnRate * 3f);
						if (Main.rand.Next(3) == 1)
						{
							spawnFriendly = true;
							maxSpawns = (int)((double)(float)maxSpawns * 0.6);
						}
					}
					else
					{
						if (!Main.expertMode || Main.rand.Next(30) != 0)
						{
							spawnFriendly = true;
						}
						maxSpawns = (int)((double)(float)maxSpawns * 0.6);
					}
				}
			}
			if (!spawnFriendly && RollOnlyBadLuckExtreme(50) == 0)
			{
				spawnRate = (int)((float)spawnRate * 0.85f);
				maxSpawns = (int)((float)maxSpawns * 1.15f);
			}
		}

		public static void GetSpawnArea(Player player, out Rectangle spawnArea, out Rectangle safeArea)
		{
			int num = (int)((double)(sWidth / 16) * 0.7);
			int num2 = (int)((double)(sHeight / 16) * 0.7);
			safeRangeX = (int)((double)(sWidth / 16) * 0.52);
			safeRangeY = (int)((double)(sHeight / 16) * 0.52);
			if (player.inventory[player.selectedItem].type == 1254 || player.inventory[player.selectedItem].type == 1299 || player.scope)
			{
				float num3 = 1.5f;
				if (player.inventory[player.selectedItem].type == 1254 && player.scope)
				{
					num3 = 1.25f;
				}
				else if (player.inventory[player.selectedItem].type == 1254)
				{
					num3 = 1.5f;
				}
				else if (player.inventory[player.selectedItem].type == 1299)
				{
					num3 = 1.5f;
				}
				else if (player.scope)
				{
					num3 = 2f;
				}
				num += (int)((double)(sWidth / 16) * 0.5 / (double)num3);
				num2 += (int)((double)(sHeight / 16) * 0.5 / (double)num3);
				safeRangeX += (int)((double)(sWidth / 16) * 0.5 / (double)num3);
				safeRangeY += (int)((double)(sHeight / 16) * 0.5 / (double)num3);
			}
			spawnArea = WorldUtils.ClampToWorld(Utils.CenteredRectangle(player.position.ToTileCoordinates(), new Point(num * 2, num2 * 2)));
			safeArea = Utils.CenteredRectangle(player.position.ToTileCoordinates(), new Point(safeRangeX * 2, safeRangeY * 2));
			if (Main.dualDungeonsSeed && !player.ZoneOverworldHeight && !player.ZoneSkyHeight)
			{
				safeArea = Utils.CenteredRectangle(player.position.ToTileCoordinates(), new Point(safeRangeX, safeRangeY));
			}
		}

		public bool FindSpawnTile(Player player, out int spawnTileX, out int spawnTileY, out bool xRange)
		{
			GetSpawnArea(player, out var spawnArea, out var safeArea);
			for (int i = 0; i < 50; i++)
			{
				int num = Main.rand.Next(spawnArea.Left, spawnArea.Right);
				int j = Main.rand.Next(spawnArea.Top, spawnArea.Bottom);
				if ((Main.tile[num, j].nactive() && Main.tileSolid[Main.tile[num, j].type]) || (!ignoreSafeWalls && Main.wallHouse[Main.tile[num, j].wall]))
				{
					continue;
				}
				if (!invaders && (double)j < Main.worldSurface * 0.3499999940395355 && !spawnFriendly && ((double)num < (double)Main.maxTilesX * 0.45 || (double)num > (double)Main.maxTilesX * 0.55 || Main.hardMode))
				{
					skyMob = true;
				}
				else if (!invaders && (double)j < Main.worldSurface * 0.44999998807907104 && !spawnFriendly && Main.hardMode && Main.rand.Next(10) == 0)
				{
					skyMob = true;
				}
				else
				{
					for (; j < Main.maxTilesY && j < spawnArea.Bottom && (!Main.tile[num, j].nactive() || !Main.tileSolid[Main.tile[num, j].type]); j++)
					{
					}
					if (j >= spawnArea.Bottom)
					{
						continue;
					}
				}
				spawnTileX = num;
				spawnTileY = j;
				if (!safeArea.Contains(spawnTileX, spawnTileY) && HasTileSpawnSpace(spawnTileX, spawnTileY))
				{
					xRange = spawnTileX >= safeArea.Left && spawnTileX < safeArea.Right;
					return true;
				}
			}
			spawnTileX = 0;
			spawnTileY = 0;
			xRange = false;
			return false;
		}

		private bool PostCheckChosenSpawnTile(int spawnTileX, int spawnTileY, int spawnTileType, int spawnWallType)
		{
			if (ZoneDungeon && (!Main.tileDungeon[spawnTileType] || spawnWallType == 0))
			{
				return false;
			}
			if (Main.dualDungeonsSeed && Main.tile[spawnTileX, spawnTileY].type == 48)
			{
				return false;

```


---

## 🤖 Assistant · 2026-08-11T05:43:10.445Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The decompiled 1.4.5.6 has a `Spawner` class structure. Now let me read our VanillaSpawner.ts fully, and the original HasTileSpawnSpace / CheckNotSpawningOnScreen / GetSpawnRate beginning / SetSpawnFlagsForChosenTile.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:43:10.747Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '330,620p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read NPC.cs L330-620 (GetSpawnRate start)"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:43:10.877Z

**📎 ToolResult**

```
				noWorms = false;
				noGroundWorms = false;
				townNPCs = 0;
			}
		}

		private void SetSpawnFlagsForChosenTile_ForDualDungeon(int spawnTileX, int spawnTileY, int spawnTileType, int spawnWallType)
		{
			bool npcSpawnPointIsInDualDungeon = true;
			NPCSpawningFlagsForDualDungeons nPCSpawningFlagsForDualDungeons = default(NPCSpawningFlagsForDualDungeons);
			nPCSpawningFlagsForDualDungeons.ScanZonesFor(scanOnly: false, spawnTileX, spawnTileY, spawnTileType, spawnWallType, npcSpawnPointIsInDualDungeon);
			ZoneDungeon = nPCSpawningFlagsForDualDungeons.ZoneDungeon;
			ZoneSnow = nPCSpawningFlagsForDualDungeons.ZoneSnow;
			ZoneGlowshroom = nPCSpawningFlagsForDualDungeons.ZoneGlowshroom;
			ZoneCorrupt = nPCSpawningFlagsForDualDungeons.ZoneCorrupt;
			ZoneCrimson = nPCSpawningFlagsForDualDungeons.ZoneCrimson;
			ZoneJungle = nPCSpawningFlagsForDualDungeons.ZoneJungle;
			ZoneHallow = nPCSpawningFlagsForDualDungeons.ZoneHallow;
			ZoneLihzhardTemple = nPCSpawningFlagsForDualDungeons.ZoneLihzhardTemple;
			spawnUndergroundDesert = nPCSpawningFlagsForDualDungeons.ZoneUndergroundDesert;
		}

		public static bool ShouldSpawnInvasionEnemies(Vector2 position)
		{
			if (Main.invasionType <= 0 || Main.invasionDelay != 0 || Main.invasionSize <= 0)
			{
				return false;
			}
			if ((double)position.Y < Main.worldSurface * 16.0 + (double)sHeight || (double)Main.spawnTileY > Main.worldSurface)
			{
				int num = 3000;
				if ((double)position.X > Main.invasionX * 16.0 - (double)num && (double)position.X < Main.invasionX * 16.0 + (double)num)
				{
					return true;
				}
				if (Main.invasionX >= (double)(Main.maxTilesX / 2 - 5) && Main.invasionX <= (double)(Main.maxTilesX / 2 + 5))
				{
					for (int i = 0; i < Main.maxNPCs; i++)
					{
						if (Main.npc[i].townNPC && Math.Abs(position.X - Main.npc[i].Center.X) < (float)num)
						{
							if (Main.rand.Next(3) == 0)
							{
								break;
							}
							return true;
						}
					}
				}
			}
			return false;
		}

		private void GetSpawnRate(Player player, out int spawnRate, out int maxSpawns)
		{
			spawnRate = defaultSpawnRate;
			maxSpawns = defaultMaxSpawns;
			if (Main.hardMode)
			{
				spawnRate = (int)((double)defaultSpawnRate * 0.9);
				maxSpawns = defaultMaxSpawns + 1;
			}
			if (player.position.Y > (float)(Main.UnderworldLayer * 16))
			{
				maxSpawns = (int)((float)maxSpawns * 2f);
			}
			else if ((double)player.position.Y > Main.rockLayer * 16.0 + (double)sHeight)
			{
				if (Main.remixWorld)
				{
					if (Main.hardMode)
					{
						spawnRate = (int)((double)spawnRate * 0.45);
						maxSpawns = (int)((float)maxSpawns * 1.8f);
					}
					else
					{
						spawnRate = (int)((double)spawnRate * 0.5);
						maxSpawns = (int)((float)maxSpawns * 1.7f);
					}
				}
				else
				{
					spawnRate = (int)((double)spawnRate * 0.4);
					maxSpawns = (int)((float)maxSpawns * 1.9f);
				}
			}
			else if ((double)player.position.Y > Main.worldSurface * 16.0 + (double)sHeight)
			{
				if (Main.remixWorld)
				{
					spawnRate = (int)((double)spawnRate * 0.4);
					maxSpawns = (int)((float)maxSpawns * 1.9f);
				}
				else if (Main.hardMode)
				{
					spawnRate = (int)((double)spawnRate * 0.45);
					maxSpawns = (int)((float)maxSpawns * 1.8f);
				}
				else
				{
					spawnRate = (int)((double)spawnRate * 0.5);
					maxSpawns = (int)((float)maxSpawns * 1.7f);
				}
			}
			else if (Main.remixWorld)
			{
				if (!Main.dayTime)
				{
					spawnRate = (int)((double)spawnRate * 0.6);
					maxSpawns = (int)((float)maxSpawns * 1.3f);
				}
			}
			else if (!Main.dayTime)
			{
				spawnRate = (int)((double)spawnRate * 0.6);
				maxSpawns = (int)((float)maxSpawns * 1.3f);
				if (Main.bloodMoon)
				{
					spawnRate = (int)((double)spawnRate * 0.3);
					maxSpawns = (int)((float)maxSpawns * 1.8f);
				}
				if ((Main.pumpkinMoon || Main.snowMoon) && (double)player.position.Y < Main.worldSurface * 16.0)
				{
					spawnRate = (int)((double)spawnRate * 0.2);
					maxSpawns *= 2;
				}
			}
			else if (Main.dayTime && Main.eclipse)
			{
				spawnRate = (int)((double)spawnRate * 0.2);
				maxSpawns = (int)((float)maxSpawns * 1.9f);
			}
			if (Main.remixWorld)
			{
				if (!Main.dayTime)
				{
					if (Main.bloodMoon)
					{
						spawnRate = (int)((double)spawnRate * 0.3);
						maxSpawns = (int)((float)maxSpawns * 1.8f);
						if ((double)player.position.Y > Main.rockLayer * 16.0 + (double)sHeight)
						{
							spawnRate = (int)((double)spawnRate * 0.6);
						}
					}
					if (Main.pumpkinMoon || Main.snowMoon)
					{
						spawnRate = (int)((double)spawnRate * 0.2);
						maxSpawns *= 2;
						if ((double)player.position.Y > Main.rockLayer * 16.0 + (double)sHeight)
						{
							spawnRate = (int)((double)spawnRate * 0.6);
						}
					}
				}
				else if (Main.dayTime && Main.eclipse)
				{
					spawnRate = (int)((double)spawnRate * 0.2);
					maxSpawns = (int)((float)maxSpawns * 1.9f);
				}
			}
			if (ZoneSnow && (double)(player.position.Y / 16f) < Main.worldSurface)
			{
				maxSpawns = (int)((float)maxSpawns + (float)maxSpawns * Main.cloudAlpha);
				spawnRate = (int)((float)spawnRate * (1f - Main.cloudAlpha + 1f) / 2f);
			}
			if (Main.drunkWorld && Main.tile[pX, pY].wall == 86)
			{
				spawnRate = (int)((double)spawnRate * 0.3);
				maxSpawns = (int)((float)maxSpawns * 1.8f);
			}
			if (inDualDungeon || ZoneDungeon)
			{
				spawnRate = (int)((double)spawnRate * 0.3);
				maxSpawns = (int)((float)maxSpawns * 1.8f);
			}
			else if (ZoneSandstorm)
			{
				spawnRate = (int)((float)spawnRate * (Main.hardMode ? 0.4f : 0.9f));
				maxSpawns = (int)((float)maxSpawns * (Main.hardMode ? 1.5f : 1.2f));
			}
			else if (player.ZoneUndergroundDesert)
			{
				spawnRate = (int)((float)spawnRate * 0.2f);
				maxSpawns = (int)((float)maxSpawns * 3f);
			}
			else if (ZoneJungle)
			{
				if (townNPCs == 0)
				{
					spawnRate = (int)((double)spawnRate * 0.4);
					maxSpawns = (int)((float)maxSpawns * 1.5f);
				}
				else if (townNPCs == 1)
				{
					spawnRate = (int)((double)spawnRate * 0.55);
					maxSpawns = (int)((double)maxSpawns * 1.4);
				}
				else if (townNPCs == 2)
				{
					spawnRate = (int)((double)spawnRate * 0.7);
					maxSpawns = (int)((float)maxSpawns * 1.3f);
				}
				else
				{
					spawnRate = (int)((double)spawnRate * 0.85);
					maxSpawns = (int)((float)maxSpawns * 1.2f);
				}
			}
			else if (ZoneCorrupt || ZoneCrimson)
			{
				spawnRate = (int)((double)spawnRate * 0.65);
				maxSpawns = (int)((float)maxSpawns * 1.3f);
			}
			else if (ZoneMeteor)
			{
				spawnRate = (int)((double)spawnRate * 0.4);
				maxSpawns = (int)((float)maxSpawns * 1.1f);
			}
			if (ZoneLihzhardTemple)
			{
				spawnRate = (int)((float)spawnRate * 0.8f);
				maxSpawns = (int)((float)maxSpawns * 1.2f);
				if (Main.remixWorld)
				{
					spawnRate = (int)((double)spawnRate * 0.4);
					maxSpawns = (int)((float)maxSpawns * 1.5f);
				}
			}
			if (Main.remixWorld && (ZoneCorrupt || ZoneCrimson) && (double)(player.position.Y / 16f) < Main.worldSurface)
			{
				spawnRate = (int)((double)spawnRate * 0.5);
				maxSpawns *= 2;
			}
			if (ZoneHallow && (double)player.position.Y > Main.rockLayer * 16.0 + (double)sHeight)
			{
				spawnRate = (int)((double)spawnRate * 0.65);
				maxSpawns = (int)((float)maxSpawns * 1.3f);
			}
			if (tresspassingDualDungeon)
			{
				spawnRate = (int)((float)spawnRate * 0.6f);
				maxSpawns = (int)((float)maxSpawns * 1.3f);
			}
			if (Main.wofNPCIndex >= 0 && player.position.Y > (float)(Main.UnderworldLayer * 16))
			{
				maxSpawns = (int)((float)maxSpawns * 0.3f);
				spawnRate *= 3;
			}
			if ((double)player.nearbyActiveNPCs < (double)maxSpawns * 0.2)
			{
				spawnRate = (int)((float)spawnRate * 0.6f);
			}
			else if ((double)player.nearbyActiveNPCs < (double)maxSpawns * 0.4)
			{
				spawnRate = (int)((float)spawnRate * 0.7f);
			}
			else if ((double)player.nearbyActiveNPCs < (double)maxSpawns * 0.6)
			{
				spawnRate = (int)((float)spawnRate * 0.8f);
			}
			else if ((double)player.nearbyActiveNPCs < (double)maxSpawns * 0.8)
			{
				spawnRate = (int)((float)spawnRate * 0.9f);
			}
			if ((double)(player.position.Y / 16f) > (Main.worldSurface + Main.rockLayer) / 2.0 || ZoneCorrupt || ZoneCrimson)
			{
				if ((double)player.nearbyActiveNPCs < (double)maxSpawns * 0.2)
				{
					spawnRate = (int)((float)spawnRate * 0.7f);
				}
				else if ((double)player.nearbyActiveNPCs < (double)maxSpawns * 0.4)
				{
					spawnRate = (int)((float)spawnRate * 0.9f);
				}
			}
			if (Main.remixWorld && (double)(player.position.Y / 16f) < Main.worldSurface && (ZoneCorrupt || ZoneCrimson))
			{
				spawnRate = (int)((double)spawnRate * 0.8);
				maxSpawns *= 2;
			}
			if (player.invis)
			{
				spawnRate = (int)((float)spawnRate * 1.2f);
				maxSpawns = (int)((float)maxSpawns * 0.8f);
			}
			if (player.calmed)
			{
				spawnRate = (int)((float)spawnRate * 1.65f);
				maxSpawns = (int)((float)maxSpawns * 0.6f);

```


---

## 🤖 Assistant · 2026-08-11T05:43:10.907Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:43:11.166Z

**📎 ToolResult**

```
1	// 原版 1.4.5.6 NPC.Spawner 内嵌类 1:1 移植（Terarria1456/Terraria/NPC.cs:39-5952）。
2	// 结构：SetSpawnFlags(L276) → GetSpawnRate(L383-640) → FindSpawnTile(L879) →
3	//       SetSpawnFlagsForChosenTile(L950) → SpawnAnNPC(L1186-5144 巨型 if-else 链)。
4	// 权重语义：Main.rand.Next(N)==0（1/N 命中）；越靠前优先级越高。
5	// 困难模式分支保留并挂在 world.flags.hardMode（当前默认 false → 只走肉前）。
6	// 净 ID（负数）= SetDefaultsFromNetId(L7633)：基底类型 × scale + 属性/颜色覆盖。
7	// 原版 spawnTileType = NPC 落脚处上方格（GetProperGroundSpawnTileTypeAndWallType L5789）；
8	// 我们的等价 = 落脚格下方第一个实心格的 tile type。
9	import { TILE } from '../../core/constants';
10	import { RNG } from '../../core/rng';
11	import type { World } from '../World';
12	import { TILE_DEFS, TILE_BY_KEY } from '../../data/tiles';
13	import { Enemy } from '../../entities/Enemy';
14	import { debugPoolOverride } from '../../data/vanillaNpcs';
15	
16	// ---- 原版 tile type 常量（TileID），我们通过 TILE_BY_KEY 反查内部 id ----
17	const T = (() => {
18	  const get = (k: string) => TILE_BY_KEY[k] ?? 0;
19	  return {
20	    DIRT: get('dirt'), GRASS: get('grass'), STONE: get('stone'),
21	    SAND: get('sand'), SNOW: get('snow'), ICE: get('ice'), MUD: get('mud'),
22	    JUNGLE_GRASS: get('v_60_jungle_grass_block'), CORRUPT_GRASS: get('v_23_corrupt_grass_block'),
23	    CRIMSON_GRASS: get('v_199_crimson_grass_block'), MUSHROOM_GRASS: get('v_70_mushroom_grass_block'),
24	    EBONSAND: get('v_112_ebonsand_block'), CRIMSAND: get('v_234_crimsand_block'),
25	    PEARLSAND: get('v_116_pearlsand_block'), HARDENED_SAND: get('hardened_sand'),
26	    SANDSTONE: get('sandstone'), FOSSIL: get('desert_fossil'),
27	    MARBLE: get('v_367_marble_block'), GRANITE: get('v_368_granite_block'),
28	    CACTUS: get('v_80_cactus'), SNOW_BRICK: get('snow_brick'),
29	    CORRUPT_ICE: get('v_163_purple_ice_block'), CRIMSON_ICE: get('v_200_red_ice_block'),
30	    // 164 粉冰(神圣冰)引擎未注册 → 0(ZoneHallow 冰分支暂不触发,与已知缺口一致)
31	    HOLLOW_ICE: get('v_164_hallowed_ice'), DUNGEON_BLUE: get('v_41_blue_brick'),
32	    DUNGEON_GREEN: get('v_43_green_brick'), DUNGEON_PINK: get('v_44_pink_brick'),
33	    // 恶土系计数(SceneMetrics.cs:613-615 的 _tileCounts 公式)
34	    EBONSTONE: get('v_25_ebonstone_block'), CORRUPT_PLANT: get('v_24_corruption_short_plants'),
35	    CORRUPT_THORN: get('v_32_corruption_thorns'), CORRUPT_HARDSAND: get('v_398_corrupt_hardened_sand_block'),
36	    CRIMSTONE: get('v_203_crimstone_block'), CRIMSON_PLANT: get('v_201_crimson_short_plants'),
37	    CRIMSAND_THORN: get('v_352_crimtane_thorns'), CRIMSON_HARDSAND: get('v_399_crimson_hardened_sand_block'),
38	    SUNFLOWER: get('v_27_sunflower'),
39	  };
40	})();
41	/** 房屋墙表（Main.cs wallHouse[N]=true 全提取，265 项）：可由玩家放置的墙。
42	 *  FindSpawnTile L886：落点格带房屋墙 → 弃选（房屋内不刷怪的主守卫）；
43	 *  SetSpawnFlags L321：玩家所站格带房屋墙 → noWorms（房屋内不出蠕虫） */
44	const WALL_HOUSE = new Set([1, 4, 5, 6, 10, 11, 12, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 44, 45, 46, 47, 60, 66, 67, 68, 72, 73, 74, 75, 76, 77, 78, 82, 84, 85, 88, 89, 90, 91, 92, 93, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 167, 168, 169, 172, 173, 174, 175, 176, 177, 179, 181, 182, 183, 184, 186, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366]);
45	
46	/** EvilTileCount 计数表(SceneMetrics.cs:613):23/661/24/25/32/112/163/400/398 计 1,27 向日葵 −10。
47	 *  661/400 等引擎无 def 的按 0 计 */
48	const EVIL_LOOKUP = (() => {
49	  const t = new Uint8Array(TILE_DEFS.length);
50	  for (const id of [T.CORRUPT_GRASS, T.EBONSTONE, T.CORRUPT_PLANT, T.CORRUPT_THORN,
51	    T.EBONSAND, T.CORRUPT_ICE, T.CORRUPT_HARDSAND]) if (id) t[id] = 1;
52	  return t;
53	})();
54	/** BloodTileCount 计数表(SceneMetrics.cs:615):199/662/201/203/200/401/399/234/352 计 1 */
55	const BLOOD_LOOKUP = (() => {
56	  const t = new Uint8Array(TILE_DEFS.length);
57	  for (const id of [T.CRIMSON_GRASS, T.CRIMSTONE, T.CRIMSON_PLANT, T.CRIMSON_ICE,
58	    T.CRIMSAND, T.CRIMSAND_THORN, T.CRIMSON_HARDSAND]) if (id) t[id] = 1;
59	  return t;
60	})();
61	
62	// ---- 洞穴主池 cavernMonsterType 表（NPC.cs:6498 + 世界生成时 18058-18064 填充） ----
63	export let cavernMonsterType: number[][] = [[49, 49, 49], [49, 49, 49]];
64	export function rollCavernMonsterType(rng: RNG): void {
65	  for (let i = 0; i < 2; i++) {
66	    cavernMonsterType[i][0] = rng.int(494, 496); // v_494/v_495（洞穴蝾螈族）
67	    cavernMonsterType[i][1] = rng.int(496, 498);
68	    cavernMonsterType[i][2] = rng.int(498, 507);
69	  }
70	}
71	
72	// ---- 原版 netID（负数）→ SetDefaultsFromNetId（L7633-7820）：基底 id + scale + 属性覆盖 ----
73	// scale/color/alpha 一律取源数据（public/sprites/vanilla-npcnetid.json，extract-npccolors.mjs 提取）
74	import vanillaNetIdJson from '../../data/vanilla-npcnetid.json';
75	const NET_ID_OVERRIDE: Record<string, { scale?: number; color?: number[]; alpha?: number }> = vanillaNetIdJson;
76	
77	const NET_ID_MAP: Record<number, { base: number; scale: number; hp?: number; dmg?: number; def?: number }> = {
78	  '-1': { base: 16, scale: 0.6, hp: 90, dmg: 45, def: 10 },   // 母史莱姆
79	  '-2': { base: 16, scale: 0.9, hp: 90, dmg: 45, def: 20 },
80	  '-3': { base: 1, scale: 0.9, hp: 14, dmg: 6, def: 0 },   // 绿史莱姆
81	  '-4': { base: 1, scale: 0.6, hp: 150, dmg: 5, def: 5 },
82	  '-5': { base: 1, scale: 0.9, hp: 30, dmg: 13, def: 4 },  // 黑史莱姆
83	  '-6': { base: 1, scale: 1.05, hp: 45, dmg: 15, def: 4 },
84	  '-7': { base: 1, scale: 1.2, hp: 40, dmg: 12, def: 6 },
85	  '-8': { base: 1, scale: 1.025, hp: 35, dmg: 12, def: 4 }, // 红（母史莱姆子代）
86	  '-9': { base: 1, scale: 1.2, hp: 45, dmg: 15, def: 7 },   // 黄
87	  '-10': { base: 1, scale: 1.1, hp: 60, dmg: 18, def: 6 },  // 丛林
88	  '-11': { base: 6, scale: 0.85 },   // 小噬魂怪
89	  '-12': { base: 6, scale: 1.15 },   // 大噬魂怪
90	  // 黄蜂族大小变体（FromNetId NetIdMap[55..64]：两两一族 231-235；scale 取 netid 表）
91	  '-16': { base: 42, scale: 0.85 }, '-17': { base: 42, scale: 1.2 },    // Little/Big Stinger
92	  '-56': { base: 231, scale: 0.85 }, '-57': { base: 231, scale: 1.25 },
93	  '-58': { base: 232, scale: 0.8 }, '-59': { base: 232, scale: 1.17 },
94	  '-60': { base: 233, scale: 0.83 }, '-61': { base: 233, scale: 1.21 },
95	  '-62': { base: 234, scale: 0.78 }, '-63': { base: 234, scale: 1.16 },
96	  '-64': { base: 235, scale: 0.87 }, '-65': { base: 235, scale: 1.21 },
97	  // 地牢骷髅变体（SetDefaultsFromNetId L7770-7788：scale 后再乘 stat）
98	  '-13': { base: 31, scale: 0.9, hp: 72, dmg: 23, def: 7 },    // Short Bones(80/26/8 ×0.9)
99	  '-14': { base: 31, scale: 1.15, hp: 101, dmg: 33, def: 10 }, // Big Boned(×1.15 再 ×1.1)
100	  '-15': { base: 1, scale: 1.15 },   // 史莱姆王子
101	  '-22': { base: 223, scale: 1.0 }, '-23': { base: 223, scale: 1.0 },
102	  '-24': { base: 223, scale: 1.0 }, '-25': { base: 223, scale: 1.0 },
103	  // 僵尸/骷髅/眼变种 = 基底 + scale（贴图同基底，属性缩放）
104	  '-38': { base: 3, scale: 0.85 }, '-39': { base: 3, scale: 0.85 }, '-40': { base: 3, scale: 0.85 },
105	  '-41': { base: 3, scale: 0.85 }, '-42': { base: 3, scale: 0.85 },
106	  '-43': { base: 2, scale: 0.85 },  // 小恶魔眼
107	  '-46': { base: 21, scale: 0.9 }, '-47': { base: 21, scale: 0.9 },
108	  '-48': { base: 201, scale: 0.9 }, '-49': { base: 201, scale: 0.9 },
109	  '-50': { base: 202, scale: 0.9 }, '-51': { base: 202, scale: 0.9 },
110	  '-52': { base: 203, scale: 0.9 }, '-53': { base: 203, scale: 0.9 },
111	  '-54': { base: 223, scale: 0.9 }, '-55': { base: 223, scale: 0.9 },
112	};
113	
114	export class VanillaSpawner {
115	  // ---- SpawnFlags（Spawner 字段 L39-137） ----
116	  private pX = 0; private pY = 0;
117	  private dayTime = true;
118	  private hardMode = false;
119	  private waterTile = false;
120	  private noWorms = false;         // 原版 wallHouse（房屋内不出蠕虫）
121	  private skyMob = false;
122	  private surfaceSpawn = false;
123	  private underGround = false;      // 原 underGround = worldSurface < y < rockLayer
124	  private deeperThanRockLayer = false;
125	  private isOcean = false;
126	  private isBeach = false;
127	  private nearMarble = false;
128	  private nearGranite = false;
129	  private spawnUndergroundDesert = false;
130	  /** 蜘蛛巢旗标（L1066/L1074）：落点邻域 ±5..15 格内有墙 62（1/3 概率扫描），
131	   *  或玩家所站格墙 62（2/3 概率查玩家位）——蜘蛛巢内/附近必出蜘蛛的真正触发器 */
132	  private spawnSpider = false;
133	  private ZoneSnow = false; private ZoneCorrupt = false; private ZoneCrimson = false;
134	  private ZoneHallow = false; private ZoneJungle = false; private ZoneGlowshroom = false;
135	  private ZoneDungeon = false; private ZoneGraveyard = false; private ZoneBeach = false;
136	  /** 原版 downedBoss3（杀过骷髅王）：地牢分支切换 守卫→常规怪池 */
137	  private downedBoss3 = false;
138	  private spawnTileX = 0; private spawnTileY = 0;
139	  /** FindSpawnTile 的 xRange 输出（L911：落脚点横向在 safeArea 内，传给 SpawnAnNPC） */
140	  private xRange = false;
141	  private spawnTileType = 0;
142	  /** 落脚点（Game 放置用） */
143	  currentSpawnX = 0;
144	  currentSpawnY = 0;
145	
146	  constructor(private world: World) {}
147	
148	  /** 玩家级 Zone 旗标（原版 Spawner.SetSpawnFlags L300：ZoneDungeon = player.ZoneDungeon——
149	   *  SceneMetrics 按玩家中心窗口判定，与落脚点无关）。Game 每帧刷怪前调用。
150	   *  invaders = ShouldSpawnInvasionEnemies(NPC.cs:352，入侵前线 3000px 内的地表玩家)；
151	   *  activeIds = 场上存活 NPC 的 vanillaId 集（选表 AnyNPCs 去重用） */
152	  invaders = false;
153	  activeIds: Set<number> = new Set();
154	  setPlayerFlags(zoneDungeon: boolean, downedSkeletron: boolean,
155	    invaders = false, activeIds: Set<number> = new Set()): void {
156	    this.ZoneDungeon = zoneDungeon;
157	    this.downedBoss3 = downedSkeletron;
158	    this.invaders = invaders;
159	    this.activeIds = activeIds;
160	  }
161	
162	  /** 天气注入（Game 每 15 tick 下发）：cloudAlpha（雨强度，雪原刷怪修正）与沙尘暴态（怪池） */
163	  rainCloudAlpha = 0;
164	  sandstormHappening = false;
165	  zoneSandstorm = false;
166	  setWeather(cloudAlpha: number, sandstormHappening: boolean, zoneSandstorm: boolean): void {
167	    this.rainCloudAlpha = cloudAlpha;
168	    this.sandstormHappening = sandstormHappening;
169	    this.zoneSandstorm = zoneSandstorm;
170	  }
171	
172	  /** SlimeRainSpawns（NPC.cs:5829-5898 1:1）：史莱姆雨天空落怪。
173	   *  独立于常规 spawnRate 概率门（原版每玩家每帧先调本函数再 TrySpawnAnNPC）。
174	   *  nearbySlots>15 / 玩家过深直接拒绝；num3=45+450×(nearby/15)（专家 ×0.85）。
175	   *  落点：x=玩家±viewW、y=玩家上方 (1.5~0.75)×viewH 带 → 格门：
176	   *  x∈[10,w+10]、y∈[surface×0.3, surface]、周围 7×8 无实心、落点无房屋墙。
177	   *  选怪：1/200 蓝(-4)；专家 1/7 大(-7)、1/3 绿(-3)；普通 1/10 大、2/5 绿；默认蓝(1) */
178	  slimeRainSpawns(px: number, py: number, nearbySlots: number, viewW: number, viewH: number, rng: RNG, expert: boolean): Enemy | null {
179	    const w = this.world;
180	    const worldSurface = w.groundLevel;
181	    if (py > worldSurface * 16 + viewH / 2 || nearbySlots > 15) return null;
182	    const num2 = nearbySlots / 15;
183	    let num3 = 45 + Math.floor(450 * num2);
184	    if (expert) num3 = Math.floor(num3 * 0.85);
185	    if (num3 < 1) num3 = 1;
186	    if (rng.int(0, num3 - 1) !== 0) return null;
187	    const x0 = Math.floor(px - viewW), x1 = x0 + viewW * 2;
188	    const y0 = Math.floor(py - viewH * 1.5), y1 = Math.floor(py - viewH * 0.75);
189	    const tx = Math.floor(rng.int(x0, x1 - 1) / 16);
190	    const ty = Math.floor(rng.int(y0, y1 - 1) / 16);
191	    const st = w.store;
192	    if (tx < 10 || tx > st.w + 10 || ty < worldSurface * 0.3 || ty > worldSurface) return null;
193	    if (!st.inBounds(tx, ty)) return null;
194	    for (let dx = -3; dx <= 3; dx++) {
195	      for (let dy = -5; dy <= 2; dy++) {
196	        if (st.inBounds(tx + dx, ty + dy) && st.isSolid(tx + dx, ty + dy)) return null;
197	      }
198	    }
199	    if (WALL_HOUSE.has(st.wall[st.idx(tx, ty)])) return null;
200	    let netId = 1;
201	    if (rng.int(0, 199) === 0) netId = -4;
202	    else if (expert) {
203	      if (rng.int(0, 6) === 0) netId = -7;
204	      else if (rng.int(0, 2) === 0) netId = -3;
205	    } else {
206	      if (rng.int(0, 9) === 0) netId = -7;
207	      else if (rng.int(0, 4) < 2) netId = -3;
208	    }
209	    return this.spawnNPC(tx * 16 + 8, ty * 16, netId, rng);
210	  }
211	
212	  /** 造怪入口：netId 可为负（SetDefaultsFromNetId 映射）；
213	   *  ai0/ai1 = 原版 SpawnNPC 第 6/7 参（如攀爬者 101 的锚点格，NPC.cs:4040） */
214	  private spawnNPC(x: number, y: number, netId: number, rng: RNG, ai0?: number, ai1?: number): Enemy | null {
215	    const map = NET_ID_MAP[netId];
216	    const baseId = map?.base ?? netId;
217	    const e = Enemy.fromVanilla(baseId, x, y);
218	    if (!e) return null;
219	    // 原版 NewNPC 锚点(NPC.cs:46596-46597):X-width/2, Y-height(底部贴格顶)。
220	    // 此前 fromVanilla 中心锚(y-h/2)把怪埋进落脚实心格半格高——飞行怪沿地面内沿
221	    // 漂移穿过侧壁,看起来像穿墙(噬魂怪等 ai5 族)
222	    e.y = y - e.h;
223	    const ov = NET_ID_OVERRIDE[String(netId)];
224	    e.vanillaNetId = netId;
225	    if (map) {
226	      e.vanillaScale = ov?.scale ?? map.scale;   // scale 优先源数据（SetDefaults_ForNetId 第 3 参）
227	      if (map.hp != null) e.hp = e.maxHp = map.hp;
228	      if (map.dmg != null) e.def.damage = map.dmg;
229	      if (map.def != null) e.def.defense = map.def;
230	    } else if (ov?.scale != null) {
231	      e.vanillaScale = ov.scale;
232	    }
233	    // SetDefaultsFromNetId 覆盖 color/alpha（L7633+：color = new Color(...) / alpha = N）
234	    if (ov?.color) e.colorRGBA = [ov.color[0], ov.color[1], ov.color[2], ov.color[3] ?? 255];
235	    if (ov?.alpha != null) e.spawnAlpha = ov.alpha;
236	    // 植物族锚点（aiStyle 13：锚点格存 ai0/ai1）
237	    if (ai0 !== undefined && ai1 !== undefined) { e.ai0 = ai0; e.ai1 = ai1; }
238	    e.id = this.world.store.w; // 占位，Game 侧会重编
239	    return e;
240	  }
241	
242	  // ---- SetSpawnFlagsForChosenTile（L950-1185） ----
243	  private setFlagsForChosenTile(spawnTileX: number, spawnTileY: number, spawnTileType: number, rng: RNG): void {
244	    const st = this.world.store;
245	    this.spawnTileX = spawnTileX; this.spawnTileY = spawnTileY; this.spawnTileType = spawnTileType;
246	    // waterTile（L957）：落脚格上方两格都是液体且为水
247	    const above1 = st.idx(spawnTileX, spawnTileY - 1), above2 = st.idx(spawnTileX, spawnTileY - 2);
248	    this.waterTile = st.liquid[above1] > 0 && st.liquid[above2] > 0 && st.liquidType[above1] === 1;
249	    // nearMarble/nearGranite（L960-1046）：落点 tile → 玩家 tile → 两轮邻近扫描
250	    // (落点 ±Next(20,30) 步长 Next(1,4) + 玩家 ±Next(30,60) 步长 Next(3,7) 抽样)。
251	    // 只查落点/玩家两格会让小体量大理石/花岗岩洞几乎永远探测不到
252	    if (spawnTileType === T.MARBLE) this.nearMarble = true;
253	    else if (spawnTileType === T.GRANITE) this.nearGranite = true;
254	    else if (st.type[st.idx(this.pX, this.pY)] === T.MARBLE) this.nearMarble = true;
255	    else if (st.type[st.idx(this.pX, this.pY)] === T.GRANITE) this.nearGranite = true;
256	    else {
257	      const scanType = (cx0: number, cy0: number, r: number, stepI: number, stepJ: number) => {
258	        const x0 = Math.max(0, cx0 - r), x1 = Math.min(st.w - 1, cx0 + r);
259	        const y0 = Math.max(0, cy0 - r), y1 = Math.min(st.h - 1, cy0 + r);
260	        for (let i = x0; i <= x1; i += stepI) {
261	          for (let j = y0; j <= y1; j += stepJ) {
262	            const tt = st.type[st.idx(i, j)];
263	            if (tt === T.MARBLE) this.nearMarble = true;
264	            else if (tt === T.GRANITE) this.nearGranite = true;
265	          }
266	        }
267	      };
268	      scanType(spawnTileX, spawnTileY, rng.int(20, 30), rng.int(1, 3), 1 + (rng.next() * 3 | 0));
269	      scanType(this.pX, this.pY, rng.int(30, 60), rng.int(3, 6), 3 + (rng.next() * 4 | 0));
270	    }
271	    // 地下沙漠（L1078-1100）：同蜘蛛巢的双路触发——1/3 扫落点 ±Next(5,15) 墙集
272	    // {216,217,187};2/3 查玩家所站格墙。此前只查落点一格(巢腔墙多在空气格,地板格常是天然墙)
273	    const DESERT_WALL = (w: number) => w === 216 || w === 217 || w === 187;
274	    if (spawnTileY < this.world.rockLevel && spawnTileY > 200 && !this.ZoneDungeon) {
275	      if (rng.next() < 1 / 3) {
276	        const r = rng.int(5, 14);
277	        const x0 = Math.max(0, spawnTileX - r), x1 = Math.min(st.w - 1, spawnTileX + r - 1);
278	        const y0 = Math.max(0, spawnTileY - r), y1 = Math.min(st.h - 1, spawnTileY + r - 1);
279	        for (let sx = x0; sx <= x1 && !this.spawnUndergroundDesert; sx++) {
280	          for (let sy = y0; sy <= y1; sy++) {
281	            if (DESERT_WALL(st.wall[st.idx(sx, sy)])) { this.spawnUndergroundDesert = true; break; }
282	          }
283	        }
284	      } else if (DESERT_WALL(st.wall[st.idx(this.pX, this.pY)])) {
285	        this.spawnUndergroundDesert = true;
286	      }
287	    }
288	    this.surfaceSpawn = spawnTileY <= this.world.groundLevel;
289	    this.deeperThanRockLayer = spawnTileY >= this.world.rockLevel;
290	    this.underGround = spawnTileY > this.world.groundLevel && spawnTileY < this.world.rockLevel;
291	    // isOcean（L1104）：边缘 + 沙 tile + 岩石层上
292	    // 海洋/海滩 x 阈值与 BeachPass 同源缩放（van = w/4200：oceanWater 220~260、
293	    // beachSandRandomCenter+20=340）——此前硬编码 250/340，非 4200 宽世界会错位：
294	    // 大世界海洋 250~sc(260) 段漏判 isOcean → 海滩水走水池段刷出水母
295	    const van = st.w / 4200;
296	    const oceanX = Math.max(1, Math.floor(260 * van));
297	    const beachX = Math.floor(340 * van);
298	    this.isOcean = (spawnTileX < oceanX || spawnTileX > st.w - oceanX) && spawnTileType === T.SAND && spawnTileY < this.world.rockLevel;
299	    this.isBeach = spawnTileY <= this.world.groundLevel && (spawnTileX < beachX || spawnTileX > st.w - beachX);
300	    // Zone 判定（SceneMetrics.cs:16/613-615/678）：以玩家为中心 169×123 窗口计数 ≥300。
301	    // 旧实现只看落脚格类型且漏黑檀石 25——腐化地表大量铺黑檀石导致噬魂怪永不触发
302	    this.ZoneSnow = spawnTileType === T.SNOW || spawnTileType === T.ICE || spawnTileType === T.SNOW_BRICK;
303	    this.ZoneCorrupt = this.countTiles(EVIL_LOOKUP, this.pX, this.pY) >= 300;
304	    this.ZoneCrimson = this.countTiles(BLOOD_LOOKUP, this.pX, this.pY) >= 300;
305	    this.ZoneHallow = spawnTileType === T.PEARLSAND || spawnTileType === T.HOLLOW_ICE;
306	    this.ZoneJungle = spawnTileType === T.MUD || spawnTileType === T.JUNGLE_GRASS;
307	    this.ZoneGlowshroom = spawnTileType === T.MUSHROOM_GRASS;
308	    // ZoneDungeon 不在此设置：原版取玩家 SceneMetrics（SetSpawnFlags L300），见 setPlayerFlags
309	    // ---- 蜘蛛巢旗标（L1045-1079）:岩石层~地狱层 && 非地牢时 ----
310	    // 1/3 概率扫落点 ±Next(5,15) 立方盒内任意墙 62;否则查玩家所站格墙 62。
311	    // 此前只查落点一格,玩家站巢里时屏幕外环带点几乎全在巢外 → 蜘蛛永不触发
312	    if (spawnTileY > this.world.rockLevel && spawnTileY < st.h - 200 && !this.ZoneDungeon) {
313	      if (rng.next() < 1 / 3) {
314	        const r = rng.int(5, 14);
315	        const x0 = Math.max(0, spawnTileX - r), x1 = Math.min(st.w - 1, spawnTileX + r - 1);
316	        const y0 = Math.max(0, spawnTileY - r), y1 = Math.min(st.h - 1, spawnTileY + r - 1);
317	        for (let sx = x0; sx <= x1 && !this.spawnSpider; sx++) {
318	          for (let sy = y0; sy <= y1; sy++) {
319	            if (st.wall[st.idx(sx, sy)] === 62) { this.spawnSpider = true; break; }
320	          }
321	        }
322	      } else if (st.wall[st.idx(this.pX, this.pY)] === 62) {
323	        this.spawnSpider = true;
324	      }
325	    }
326	  }
327	
328	  /** tileDungeon 集（Main.cs:7941-7946）：41/43/44 主砖（677-679 安全变体未注册缺席=0）。
329	   *  PostCheckChosenSpawnTile L924：ZoneDungeon 时落脚点必须踩地牢砖且头顶有墙 */
330	  private isDungeonTile(t: number): boolean {
331	    return t === T.DUNGEON_BLUE || t === T.DUNGEON_GREEN || t === T.DUNGEON_PINK;
332	  }
333	
334	  /** SceneMetrics.ScanTiles 近似:中心 169×123 窗口(zoneScanSize=120×75+padding 25×2−1)计数 */
335	  private countTiles(lookup: Uint8Array, cx: number, cy: number): number {
336	    const st = this.world.store;
337	    const x0 = Math.max(2, cx - 84), x1 = Math.min(st.w - 3, cx + 84);
338	    const y0 = Math.max(2, cy - 61), y1 = Math.min(st.h - 3, cy + 61);
339	    let n = 0;
340	    for (let y = y0; y <= y1; y++) {
341	      const row = y * st.w;
342	      for (let x = x0; x <= x1; x++) {
343	        const t = st.type[row + x];
344	        if (lookup[t]) n++;
345	        else if (t === T.SUNFLOWER) n -= 10; // 向日葵每株 −10(SceneMetrics.cs:588 num=-10)
346	      }
347	    }
348	    return n;
349	  }
350	
351	  // ---- FindSpawnTile（L879-920）----
352	  /** GetSpawnRate（L383-668，单机非 remix 分支）：
353	   *  defaultSpawnRate=600 / defaultMaxSpawns=5（L6108/6110）。
354	   *  深度带/昼夜/附近怪分层/水蜡烛修正 + clamp（L655-662）。
355	   *  血月/日食/南瓜月/和平蜡烛/向日葵/calmed/隐身/仙女未实现（无对应系统）
356	   *  UnderworldLayer 暂用 h-200 近似（待接世界生成精确值） */
357	  getSpawnRate(playerYpx: number, nearbySlots: number, waterCandle: boolean, sHeightPx: number): { spawnRate: number; maxSpawns: number } {
358	    // 入侵覆盖（L691-695）：rate=20（每帧 1/20 尝试），上限 5*(2+0.3n)（单人 11）
359	    if (this.invaders) {
360	      return { spawnRate: 20, maxSpawns: Math.floor(5 * (2 + 0.3 * 1)) };
361	    }
362	    let spawnRate = 600;
363	    let maxSpawns = 5;
364	    const w = this.world;
365	    const underworldY = (w.store.h - 200) * 16;
366	    if (playerYpx > underworldY) {
367	      // L389-392：地狱 maxSpawns×2
368	      maxSpawns = Math.floor(maxSpawns * 2);
369	    } else if (playerYpx > w.rockLevel * 16 + sHeightPx) {
370	      // L402-407：洞穴层 spawnRate×0.4 / max×1.9
371	      spawnRate = Math.floor(spawnRate * 0.4);
372	      maxSpawns = Math.floor(maxSpawns * 1.9);
373	    } else if (playerYpx > w.groundLevel * 16 + sHeightPx) {
374	      // L418-422：地下层 spawnRate×0.5 / max×1.7
375	      spawnRate = Math.floor(spawnRate * 0.5);
376	      maxSpawns = Math.floor(maxSpawns * 1.7);
377	    } else if (!this.dayTime) {
378	      // L455-459：夜晚 spawnRate×0.6 / max×1.3；血月再 ×0.3/×1.8（L447-450）
379	      spawnRate = Math.floor(spawnRate * 0.6);
380	      maxSpawns = Math.floor(maxSpawns * 1.3);
381	      if (w.clock.bloodMoon) {
382	        spawnRate = Math.floor(spawnRate * 0.3);
383	        maxSpawns = Math.floor(maxSpawns * 1.8);
384	      }
385	    }
386	    // L583-591（无条件）：附近怪 <20%/40%/60%/80% 上限时 ×0.6/×0.7/×0.8/×0.9
387	    if (nearbySlots < maxSpawns * 0.2) spawnRate = Math.floor(spawnRate * 0.6);
388	    else if (nearbySlots < maxSpawns * 0.4) spawnRate = Math.floor(spawnRate * 0.7);
389	    else if (nearbySlots < maxSpawns * 0.6) spawnRate = Math.floor(spawnRate * 0.8);
390	    else if (nearbySlots < maxSpawns * 0.8) spawnRate = Math.floor(spawnRate * 0.9);
391	    // L592-604：地下中点以下/腐化/猩红再叠加（Zone flags 为上次生成残留，同原版）
392	    if (playerYpx / TILE > (w.groundLevel + w.rockLevel) / 2 || this.ZoneCorrupt || this.ZoneCrimson) {
393	      if (nearbySlots < maxSpawns * 0.2) spawnRate = Math.floor(spawnRate * 0.7);
394	      else if (nearbySlots < maxSpawns * 0.4) spawnRate = Math.floor(spawnRate * 0.9);
395	    }
396	    // L640-646：水蜡烛 spawnRate×0.75 / max×1.5；天空层再 ×0.5
397	    if (waterCandle) {
398	      spawnRate = Math.floor(spawnRate * 0.75);
399	      maxSpawns = Math.floor(maxSpawns * 1.5);
400	      if (playerYpx / TILE < w.groundLevel * 0.35) spawnRate = Math.floor(spawnRate * 0.5);
401	    }
402	    // L655-662：下限 spawnRate≥60，上限 maxSpawns≤15
403	    if (spawnRate < 60) spawnRate = 60;
404	    if (maxSpawns > 15) maxSpawns = 15;
405	    // 地牢（L502-506）：spawnRate×0.3 / max×1.8；未杀骷髅王再压到 10（L696，
406	    // 在 clamp 之后赋值故不受 ≥60 下限影响——守卫快速轮换）
407	    if (this.ZoneDungeon) {
408	      spawnRate = Math.floor(spawnRate * 0.3);
409	      maxSpawns = Math.floor(maxSpawns * 1.8);
410	      if (!this.downedBoss3) spawnRate = 10;
411	    }
412	    // 雨天雪原（NPC.cs:494-496）：ZoneSnow 且玩家在地表 → max×(1+cloudAlpha) / rate×(1-cloudAlpha+1)/2
413	    if (this.ZoneSnow && this.rainCloudAlpha > 0 && playerYpx / 16 < w.groundLevel) {
414	      maxSpawns = Math.floor(maxSpawns * (1 + this.rainCloudAlpha));
415	      spawnRate = Math.floor(spawnRate * (1 - this.rainCloudAlpha + 1) / 2);
416	    }
417	    return { spawnRate, maxSpawns };
418	  }
419	
420	  /** FindSpawnTile（L879-927）+ GetSpawnArea（L841-877）1:1：
421	   *  spawnArea = 玩家 ±(0.7×全屏格)（均匀取点，不是环带外扩！），
422	   *  safeArea = 玩家 ±(0.52×全屏格)——生成点必须落在画面外（!safeArea.Contains）。
423	   *  viewHalfW/H = 半屏格数 → 0.7×全屏 = ×1.4 半屏；0.52×全屏 = ×1.04 半屏 */
424	  private findSpawnTile(rng: RNG, viewHalfW: number, viewHalfH: number): boolean {
425	    const st = this.world.store;
426	    const px = this.pX, py = this.pY;
427	    const rangeX = Math.max(1, Math.floor(viewHalfW * 1.4));
428	    const rangeY = Math.max(1, Math.floor(viewHalfH * 1.4));
429	    const safeX = Math.max(1, Math.floor(viewHalfW * 1.04));
430	    const safeY = Math.max(1, Math.floor(viewHalfH * 1.04));
431	    // WorldUtils.ClampToWorld
432	    const areaL = Math.max(2, px - rangeX), areaR = Math.min(st.w - 3, px + rangeX);
433	    const areaT = Math.max(2, py - rangeY), areaB = Math.min(st.h - 3, py + rangeY);
434	    for (let attempt = 0; attempt < 50; attempt++) {
435	      const tx = rng.int(areaL, areaR);
436	      let ty = rng.int(areaT, areaB);
437	      // L886-888：点在实心格 或 带房屋墙 → 重试（房屋内不刷怪的主守卫）
438	      if (st.isSolid(tx, ty)) continue;
439	      if (WALL_HOUSE.has(st.wall[st.idx(tx, ty)])) continue;
440	      this.skyMob = false;
441	      // L890-897：天空怪——高于 worldSurface×0.35 且露天（原版以"两侧 45% 带外"为条件，
442	      // 隐含不变量 = 浮空岛只在两侧、中央带无高空地面。此处改判"落脚面上方两格无墙"，
443	      // 在合法原版世界上与原版等价（岛皆露天），且兼容含中央浮空岛的存量世界——
444	      // 否则中央岛会被当地表刷僵尸/水母）
445	      if (ty < this.world.groundLevel * 0.35 && st.wall[st.idx(tx, ty - 1)] === 0 && st.wall[st.idx(tx, ty - 2)] === 0) {
446	        this.skyMob = true;
447	      } else {
448	        // L900-906：向下找第一个实心格 = 落脚面（扫描上限 = spawnArea.Bottom，非世界底）
449	        let j = ty;
450	        while (j < areaB && !st.isSolid(tx, j)) j++;
451	        if (j >= areaB) continue;
452	        ty = j;
453	      }
454	      // L910：safeArea 内（画面内）一律拒绝 + HasTileSpawnSpace 落点空间校验
455	      if (Math.abs(tx - px) < safeX && Math.abs(ty - py) < safeY) continue;
456	      if (!this.hasTileSpawnSpace(tx, ty)) continue;
457	      // L911：xRange = 落脚点在 safeArea 横向范围内（原版传给 SpawnAnNPC 的水生成判定）
458	      this.xRange = tx >= px - safeX && tx < px + safeX;
459	      this.spawnTileX = tx; this.spawnTileY = ty;
460	      // 落脚处 tile type（原版 GetProperGroundSpawnTileTypeAndWallType）
461	      const groundType = this.skyMob ? 0 : st.type[st.idx(tx, ty)];
462	      // PostCheckChosenSpawnTile L924：地牢内刷怪点必须踩地牢砖且上方格有墙，否则换点重试
463	      if (this.ZoneDungeon &&
464	        (!this.isDungeonTile(groundType) || st.wall[st.idx(tx, ty)] === 0)) continue;
465	      this.setFlagsForChosenTile(tx, ty, groundType, rng);
466	      return true;
467	    }
468	    return false;
469	  }
470	
471	  /** HasTileSpawnSpace（L5306+5330）：落脚格上方 spawnSpaceX=2 × spawnSpaceY=3 区域
472	   *  逐格 CanSpawnInTile——非实心且非岩浆（防刷进实心/岩浆里） */
473	  private hasTileSpawnSpace(tx: number, ty: number): boolean {
474	    const st = this.world.store;
475	    for (let dx = -1; dx <= 0; dx++) {
476	      for (let dy = -3; dy <= -1; dy++) {
477	        const x = tx + dx, y = ty + dy;
478	        if (x < 0 || y < 0 || x >= st.w || y >= st.h) return false;
479	        const i = st.idx(x, y);
480	        if (st.isSolid(x, y)) return false;
481	        if (st.liquid[i] > 0 && st.liquidType[i] === 2) return false;
482	      }
483	    }
484	    return true;
485	  }
486	
487	  /** CheckNotSpawningOnScreen（L5344-5366）像素级双保险：
488	   *  落脚格 16×16 与"玩家屏幕 ±safeRange"矩形相交 → 拒绝。
489	   *  注意原版单位混用（L5354）：safeRangeX/Y 是格数但直接当像素偏移加——实际外扩仅 ~2 格 */
490	  private checkNotSpawningOnScreen(px: number, py: number, viewHalfW: number, viewHalfH: number): boolean {
491	    const sW = viewHalfW * 2 * TILE, sH = viewHalfH * 2 * TILE;
492	    const safePxX = viewHalfW * 1.04, safePxY = viewHalfH * 1.04; // 格数直接当像素（原版 L5354 原样）
493	    const rectX = px - sW / 2 - safePxX, rectY = py - sH / 2 - safePxY;
494	    const rectW = sW + safePxX * 2, rectH = sH + safePxY * 2;
495	    const tX = this.spawnTileX * TILE, tY = this.spawnTileY * TILE;
496	    return !(tX < rectX + rectW && tX + TILE > rectX && tY < rectY + rectH && tY + TILE > rectY);
497	  }
498	
499	  /** SpawnHornet（NPC.cs:5189-5255 1:1）：Next(8) 选族——
500	   *  case0-4 黄蜂族 231-235（各 1/4 小 -2k/大 -2k+1 变体）；default(case5-7) 蜂刺族 42 */
501	  private spawnHornet(x: number, y: number, rng: RNG): Enemy | null {
502	    const v = rng.int(0, 8);
503	    const table: Array<[number, number, number]> = [
504	      [-56, -57, 231], [-58, -59, 232], [-60, -61, 233],
505	      [-62, -63, 234], [-64, -65, 235],
506	      [-16, -17, 42],
507	    ];
508	    const row = table[Math.min(v, 5)];
509	    if (rng.next() < 0.25) return this.spawnNPC(x, y, row[0], rng);
510	    if (rng.next() < 0.25) return this.spawnNPC(x, y, row[1], rng);
511	    return this.spawnNPC(x, y, row[2], rng);
512	  }
513	
514	  // ---- SpawnAnNPC（L1186-5144）——肉前分支 1:1，hardMode 分支保留 ----
515	  private spawnAnNPC(rng: RNG): Enemy | null {
516	    const st = this.world.store;
517	    const x = this.spawnTileX * TILE + 8;
518	    const y = this.spawnTileY * TILE;
519	    const N = (n: number) => rng.next() < 1 / n;  // Main.rand.Next(n)==0
520	    const hardMode = this.hardMode;
521	    const t = this.spawnTileType;
522	    const D = (id: number) => this.spawnNPC(x, y, id, rng);
523	    const any = (id: number) => this.activeIds.has(id);
524	
525	    // ---- 天空怪（原版 NPC.cs:1290-1331：else-if 链最前、invaders 之前——
526	    //  skyMob 优先于入侵分支；肉前 = 兜底鸟妖 48，困难 = 1/10 飞龙 87（场内唯一））----
527	    if (this.skyMob) {
528	      if (hardMode && !any(87) && N(10)) return D(87);
529	      return D(48);
530	    }
531	    // ---- 入侵分支（L1333-1401：else if (invaders)，与普通链互斥）----
532	    if (this.invaders) {
533	      const it = this.world.invasionType;
534	      if (it === 1) {
535	        // 哥布林（L1335-1360）：召唤师(1/30,困难,唯一)→法师→小兵→弓手→盗贼→兜底战士
536	        if (hardMode && !any(471) && N(30)) return D(471);
537	        if (N(9)) return D(29);
538	        if (N(5)) return D(26);
539	        if (N(3)) return D(111);
540	        if (N(3)) return D(27);
541	        return D(28);
542	      }
543	      if (it === 2) {
544	        // 雪人军团（L1362-1372）：雪球怪 1/7 → 黑帮雪人 1/3 → 兜底 刺客雪人
545	        if (N(7)) return D(145);
546	        if (N(3)) return D(143);
547	        return D(144);
548	      }
549	      if (it === 3) {
550	        // 海盗（L1377-1401；491 飞船为多部件飞行体暂缺，跳过其分支）：
551	        // 船长(1/30,唯一)→弩手→鹦鹉→神枪手→海盗→兜底 甲板水手
552	        if (N(30) && !any(216)) return D(216);
553	        if (N(11)) return D(215);
554	        if (N(9)) return D(252);
555	        if (N(7)) return D(214);
556	        if (N(3)) return D(213);
557	        return D(212);
558	      }
559	    }
560	
561	    // ---- 蜘蛛巢（L1569-1587）：落点墙 62 或 spawnSpider 旗标 ----
562	    const wall = st.wall[st.idx(this.spawnTileX, this.spawnTileY)];
563	    if (wall === 62 || this.spawnSpider) {
564	      // 造型师 354（1/8,岩石层深处+场内无 354）：解绑城镇 NPC 救援链路,注释保留
565	      if (this.hardMode && !N(10)) return D(163);  // hardMode 9/10 黑寡妇(L1577)
566	      return D(164);                               // 爬墙者
567	    }
568	    // ---- 地下沙漠（L1589-1672）----
569	    if (this.spawnUndergroundDesert) {
570	      if (N(15)) return D(537);
571	      const r = rng.next();
572	      if (r < 0.5) return D(580);
573	      if (r < 0.9) return D(581);
574	      return D(69);
575	    }
576	    // ---- 海洋（L1705-1834）----
577	    if (this.waterTile && this.isOcean) {
578	      // 海鸥 602（L1767：水面上方有干格时 1/10；落点由 Game 的 critter 放置抬到水面线）
579	      if (N(10)) return D(602);
580	      if (N(10)) return D(220);
581	      if (N(18)) return D(221);
582	      if (N(3)) return D(67);   // 螃蟹
583	      return D(64);             // 默认粉水母
584	    }
585	    // ---- 水池段（L1839-1905）----
586	    if (this.waterTile && !this.isOcean) {
587	      // 原版水池在地下也是这些
588	      if (N(6)) return D(63);   // 蓝水母
589	      return D(63);
590	    }
591	    // ---- 小动物（spawnFriendly 段 L2006-2535，白天 + 草/土 tile + Next(15) 门）----
592	    if (this.dayTime && !this.waterTile && this.surfaceSpawn &&
593	      (t === T.GRASS || t === T.DIRT || t === T.SNOW || t === T.SNOW_BRICK || t === 477)) {
594	      if (N(15)) {
595	        if (t === T.SNOW || t === T.SNOW_BRICK) {
596	          // 雪原小动物（L148→148|149 Next(2)）
597	          if (N(2)) return D(148);
598	          return D(149);
599	        }
600	        // 森林小动物概率表（原版 butterflyChance/stinkBugChance 动态值，取代表值）
601	        const r = rng.next();
602	        if (r < 0.2) return D(357);       // 蚯蚓
603	        if (r < 0.45) return D(377);      // 蚱蜢
604	        if (r < 0.65) return D(46);       // 兔子
605	        if (r < 0.8) return D(299);       // 松鼠
606	        if (r < 0.9) return D(300);       // 老鼠
607	        return D(74);                     // 鸟
608	      }
609	    }
610	    // ---- 地牢（L2536-2706：CheckToSpawnDungeonEnemies = ZoneDungeon 且玩家在 dungeonY+40 以下）----
611	    {
612	      const dungeonY = this.world.dungeonY || Math.floor(this.world.groundLevel);
613	      if (this.ZoneDungeon && !(this.pY < dungeonY + 40)) {
614	        // 墙变体（L2540-2552）：94/96/98→1、95/97/99→2；RollLuck(7) 重掷（0.9 尺度下 1/7≈1/7）
615	        const wallA = st.wall[st.idx(this.spawnTileX, this.spawnTileY)];
616	        const wallB = st.wall[st.idx(this.spawnTileX, this.spawnTileY - 1)];
617	        let variant = 0;
618	        if (wallA === 94 || wallA === 96 || wallA === 98 || wallB === 94 || wallB === 96 || wallB === 98) variant = 1;
619	        if (wallA === 95 || wallA === 97 || wallA === 99 || wallB === 95 || wallB === 97 || wallB === 99) variant = 2;
620	        if (N(7)) variant = rng.int(0, 3);
621	        // 未杀骷髅王（flag12）→ 地牢守卫 68（9999 伤，1:1 原版劝退机制）
622	        if (!this.downedBoss3) return D(68);
623	        // L2559 机械师(124)：savedMech/AnyNPCs 未实现，暂缺
624	        // hardDungeon(hardMode && downedPlantBoss) 分支省略（无此旗标系统）
625	        if (N(35)) return D(71);   // 地牢史莱姆
626	        if (variant === 1 && N(3)) return D(70);   // 火轮
627	        if (variant === 2 && N(5)) return D(72);   // 刺球
628	        if (variant === 0 && N(7)) return D(34);   // 诅咒头骨
629	        if (N(7)) return D(32);    // 黑魔法师
630	        // 书架书怪 693/694（AI_FindNearbyBook）：书架实体系统未实现，暂缺
631	        const av = rng.int(0, 5);
632	        if (av === 0) return D(294);
633	        if (av === 1) return D(295);
634	        if (av === 2) return D(296);
635	        if (N(4)) return D(-14);   // Big Boned
636	        if (N(5)) return D(-13);   // Short Bones
637	        return D(31);              // 愤怒骨怪
638	      }
639	    }
640	    // ---- 蘑菇地（L3540-3610，tile 70）----
641	    if (t === T.MUSHROOM_GRASS) {
642	      if (this.surfaceSpawn) {
643	        if (N(3)) {
644	          if (N(4)) return D(259);
645	          return D(257);
646	        }
647	        return D(254);
648	      }
649	      if (N(8)) return D(360);
650	      if (N(4)) return D(259);
651	      return D(257);
652	    }
653	    // ---- 蜂巢墙 86（NPC.cs:3833-3835）：7/8 SpawnHornet ----
654	    if (wall === 86 && !N(8)) return this.spawnHornet(x, y, rng);
655	    // ---- 丛林草 tile 60（NPC.cs:3839-3856；旧实现误在肉前出 158 巨型蝙蝠，原版无此分支）----
656	    if (t === T.JUNGLE_GRASS) {
657	      const midY = (this.world.groundLevel + this.world.rockLevel) / 2;
658	      if (this.spawnTileY > midY) {
659	        // 深层丛林（原版 remix 分支省略）：1/4 棘刺丛林史莱姆 / 1/4 食人怪(锚点) / else 黄蜂族
660	        if (N(4)) return D(204);
661	        if (N(4)) return this.spawnNPC(x, y, 43, rng, this.spawnTileX, this.spawnTileY);
662	        return this.spawnHornet(x, y, rng);
663	      }
664	      // 浅层：1/4 丛林蝙蝠 / 1/8 魔腾怪(锚点)
665	      if (N(4)) return D(51);
666	      if (N(8)) return this.spawnNPC(x, y, 56, rng, this.spawnTileX, this.spawnTileY);
667	    }
668	    // ---- 沙尘暴怪池（NPC.cs:3859-3885：Happening && ZoneSandstorm && 沙格落脚）----
669	    //  肉前：1/2 雨蚁狮(546)，否则 1/2 秃鹫(61)，否则蚁狮(69)；
670	    //  困难：1/20 沙尘元素(541)（场上≤1），1/3 沙虫(510)（≤4 段），其余落常规池
671	    if (this.sandstormHappening && this.zoneSandstorm && (t === T.SAND || t === T.HARDENED_SAND || t === T.SANDSTONE)) {
672	      const any541 = (id: number) => [...this.activeIds].includes(id);
673	      if (!hardMode) {
674	        if (N(2)) return D(546);
675	        else if (N(2)) return D(61);
676	        else return D(69);
677	      } else {
678	        if (N(20) && !any541(541)) return D(541);
679	        // 沙虫 510 段数检查以 activeIds 近似（>4 不出）
680	        let seg510 = 0;
681	        for (const id of this.activeIds) if (id === 510) seg510++;
682	        if (seg510 < 4 && N(3)) return D(510);
683	      }
684	    }
685	    // ---- 沙漠地表（L3859-3928，沙尘暴外简化为沙漠 tile 段）----
686	    // 原版 L3859 沙地族 = 53 沙/112 黑檀沙/116 珍珠沙/234 猩红沙/397 硬化沙/396 沙岩/404 化石
687	    if (t === T.SAND || t === T.HARDENED_SAND || t === T.SANDSTONE || t === T.FOSSIL) {
688	      if (!hardMode) {
689	        if (N(6)) return D(69);   // 蚁狮
690	        return D(61);             // 秃鹫（地表沙）
691	      }
692	    }
693	    // ---- 猩红（L3973-4031）----
694	    if (this.ZoneCrimson) {
695	      if (N(5)) return D(182);
696	      if (N(2)) return D(268);
697	      if (N(2)) return D(181);
698	      return D(173);  // 默认 Crimera
699	    }
700	    // ---- 腐化(NPC.cs:4032-4074 一比一)----
701	    // 门禁 = 落脚面 tile:腐化草 23 / 黑檀石 25 / 黑沙 112 / 腐化冰 163 / 腐化丛林草 661,
702	    // 或(黄沙 22 && ZoneCorrupt)。攀爬者 101 仅困难模式+岩石层下 1/3,锚点格随 spawn 传入
703	    const corruptFloor = t === T.CORRUPT_GRASS || t === T.EBONSTONE || t === T.EBONSAND
704	      || t === T.CORRUPT_ICE || ((t === T.SAND) && this.ZoneCorrupt);
705	    const ugRock = this.spawnTileY >= this.world.rockLevel; // flag16
706	    if (corruptFloor) {
707	      if (hardMode && ugRock && N(40)) return D(83);       // World Feeder(蠕虫,1/40)
708	      if (hardMode && ugRock && N(3)) {
709	        return this.spawnNPC(x, y, 101, rng, this.spawnTileX, this.spawnTileY); // 攀爬者(锚点格)
710	      }
711	      if (hardMode && N(3)) return D(N(3) ? 121 : 81);     // 史莱姆法师/腐化史莱姆
712	      if (hardMode && (N(2) || ugRock)) return D(94);      // 腐化史莱姆
713	      if (N(3)) return D(-11);   // 小噬魂怪
714	      if (N(3)) return D(-12);   // 大噬魂怪
715	      return D(6);               // 默认 Eater of Souls
716	    }
717	    // ---- 地表（L4075-4717）----
718	    if (this.surfaceSpawn) {
719	      if (this.ZoneSnow) {
720	        // 雪原地表（L4560+）
721	        if (hardMode && N(3)) return D(155);
722	        if (N(6)) return D(147);   // 冰史莱姆
723	        return D(161);             // 雪原狼
724	      }
725	      if (this.dayTime) {
726	        // 白天地表小动物门已过 → 池底
727	        if (!this.waterTile) {
728	          return D(this.getBasicSlimeToSpawn(true, t, rng));  // L4402
729	        }
730	        return null;
731	      }
732	      // 夜晚（L4454-4716）：Next(6) 门
733	      if (N(6) || (this.world.clock.dayCount >= 0 && N(2) && false)) {  // moonPhase 暂无
734	        if (N(2)) {
735	          if (N(4)) return D(-43);  // 小恶魔眼
736	          return D(2);              // 恶魔眼
737	        }
738	        // switch(Next(5)) 僵尸系
739	        const zv = rng.int(0, 5);
740	        const zm = [190, 191, 192, 193, 194][zv] ?? 3;
741	        if (N(3)) {
742	          // 各配 1/3 概率小变种
743	          const small = [-38, -39, -40, -41, -42][zv] ?? -38;
744	          return D(small);
745	        }
746	        return D(zm);
747	      }
748	      // 夜间池底（L4561+ torch zombie 等）
749	      if (!this.ZoneSnow && !this.ZoneJungle && !this.waterTile) {
750	        return D(3);  // 普通僵尸兜底
751	      }
752	      return null;
753	    }
754	    // ---- 地下层（L4718-4770，worldSurface < y < rockLayer）----
755	    if (this.underGround) {
756	      if (!this.noWorms && N(50) && !this.ZoneSnow) {
757	        return D(10);   // Giant Worm
758	      }
759	      if (this.ZoneSnow) return D(147);
760	      return D(this.getBasicSlimeToSpawn(false, t, rng));
761	    }
762	    // ---- 地狱（L4771-4820，y > maxTilesY-190）----
763	    if (this.spawnTileY > st.h - 190) {
764	      if (N(40)) return D(39);   // Bone Serpent
765	      if (N(14)) return D(24);   // Fire Imp
766	      if (N(7)) {
767	        if (N(10)) return D(66);  // Voodoo Demon
768	        return D(62);             // Demon
769	      }
770	      if (N(3)) return D(59);    // Lava Slime
771	      return D(60);              // Hellbat
772	    }
773	    // ---- 洞穴通用池（L4825-5142）----
774	    if (N(60)) {
775	      if (this.ZoneSnow) return D(218);
776	      return D(217);
777	    }
778	    if (!this.noWorms && N(100) && !this.ZoneHallow) {
779	      if (!hardMode) {
780	        if (this.ZoneSnow) return D(185);
781	        return D(10);
782	      }
783	    }
784	    if (this.ZoneSnow && N(20)) return D(185);
785	    if ((!hardMode && N(10)) || (hardMode && N(20))) {
786	      if (this.ZoneSnow) return D(184);
787	      if (N(3)) return D(-6);  // 黑史莱姆
788	      return D(16);            // 母史莱姆
789	    }
790	    if ((!hardMode) && N(4)) {
791	      if (this.ZoneSnow) return D(184);
792	      if (N(3)) return D(-6);
793	      return D(184);
794	    }
795	    if (N(2)) {
796	      // 洞穴主池（L4896+）
797	      // 骷髅商 453（L4906-4910）：1/35，非水域（影烛未实现），场上无 453
798	      // —— Game.trySpawnEnemy 把 453 转成 TownNPC 放 npcs 桶
799	      if (N(35) && !this.waterTile) return D(453);
800	      if (N(80)) return D(195);                     // Tim（罕）
801	      if (N(200)) return D(45);                     // Bound Goblin
802	      if (this.nearMarble && !N(4)) {
803	        if (hardMode && N(6)) return D(480);
804	        return D(481);
805	      }
806	      if (this.nearGranite && !N(5)) {
807	        if (N(6)) return D(483);
808	        return D(482);
809	      }
810	      if (N(20)) return D(44);   // 附魔剑
811	      // switch(Next(4)) 骷髅系
812	      const sv = rng.int(0, 4);
813	      const sm = [21, 201, 202, 203][sv] ?? 21;
814	      if (N(3)) {
815	        const small = [[-46, -47], [-48, -49], [-50, -51], [-52, -53]][sv] ?? [-46, -47];
816	        return D(rng.next() < 0.5 ? small[0] : small[1]);
817	      }
818	      return D(sm);
819	    }
820	    // 洞穴兜底（L5101-5142）
821	    if (this.ZoneJungle) return D(51);
822	    if (this.ZoneSnow) return D(150);
823	    return D(49);  // Cave Bat
824	
825	    return null;
826	  }
827	
828	  /** GetBasicSlimeToSpawn（L5537-5580） */
829	  private getBasicSlimeToSpawn(surface: boolean, tileType: number, rng: RNG): number {
830	    if (!surface) {
831	      // 地下：Next(5)==0→-9（黄），否则 Next(2)==0→1（蓝）/-8（红）
832	      if (rng.next() < 0.2) return -9;
833	      return rng.next() < 0.5 ? 1 : -8;
834	    }
835	    switch (tileType) {
836	      case T.MUD: return -10;     // 丛林
837	      case T.SNOW: case T.SNOW_BRICK: return 147;  // 冰
838	      default:
839	        if (rng.next() < 1 / 3) return -3;         // 绿
840	        if (rng.next() < 0.1) return -7;           // 紫
841	        return 1;                                   // 蓝
842	    }
843	  }
844	
845	  /** 主入口：Game.trySpawnEnemy 调用 */
846	  spawn(playerX: number, playerY: number, rng: RNG, viewHalfW: number, viewHalfH: number): Enemy | null {
847	    this.pX = Math.floor(playerX / TILE);
848	    this.pY = Math.floor(playerY / TILE);
849	    this.dayTime = this.world.clock.isDay;
850	    this.hardMode = !!this.world.flags.hardMode;
851	    // SetSpawnFlags L321：noWorms = 玩家所站格带房屋墙（房屋内不出蠕虫）
852	    this.noWorms = this.world.store.inBounds(this.pX, this.pY)
853	      && WALL_HOUSE.has(this.world.store.wall[this.world.store.idx(this.pX, this.pY)]);
854	    this.skyMob = false;
855	    this.spawnSpider = false;
856	    // 邻近旗标每尝试复位(原版每次 TrySpawnAnNPC 全新置旗;
857	    // 泄漏会导致碰过大理石后全图永远出蛇发女妖)
858	    this.nearMarble = false;
859	    this.nearGranite = false;
860	    this.spawnUndergroundDesert = false;
861	    if (!this.findSpawnTile(rng, viewHalfW, viewHalfH)) return null;
862	    // TrySpawnAnNPC L220：CheckNotSpawningOnScreen 像素级二次校验（画面内/贴屏拒绝）
863	    if (!this.checkNotSpawningOnScreen(playerX, playerY, viewHalfW, viewHalfH)) return null;
864	    this.currentSpawnX = this.spawnTileX;
865	    this.currentSpawnY = this.spawnTileY;
866	    // 探针调试覆盖：debugPoolOverride 非空时绕过原版链直接从池选（确定性验证）
867	    if (debugPoolOverride && debugPoolOverride.length) {
868	      return this.spawnNPC(this.spawnTileX * 16 + 8, this.spawnTileY * 16,
869	        debugPoolOverride[rng.int(0, debugPoolOverride.length - 1)], rng);
870	    }
871	    return this.spawnAnNPC(rng);
872	  }
873	}
874	

```


---

## 🤖 Assistant · 2026-08-11T05:43:13.230Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read the original HasTileSpawnSpace (L5306), CheckNotSpawningOnScreen (L5344), SetSpawnFlagsForChosenTile (L950-1185), and GetProperGroundSpawnTileTypeAndWallType (L5789). Also check the GetSpawnArea in detail (L841-877) — I saw it. Let me also check defaultSpawnRate/defaultMaxSpawns and spawnSpaceX/spawnSpaceY values, and TileStore.liquid semantics.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:43:13.601Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '5290,5400p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read HasTileSpawnSpace/CheckNotSpawningOnScreen"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:43:13.667Z

**📎 ToolResult**

```
				else
				{
					num *= 20;
					if (AnyNPCs(624))
					{
						num *= 20;
					}
				}
			}
			if (Main.remixWorld)
			{
				num /= 2;
			}
			return num;
		}

		public static bool HasTileSpawnSpace(int spawnTileX, int spawnTileY)
		{
			Rectangle rectangle = new Rectangle(spawnTileX - spawnSpaceX / 2, spawnTileY - spawnSpaceY, spawnSpaceX, spawnSpaceY);
			if (WorldGen.InWorld(rectangle))
			{
				return CanSpawnInTiles(rectangle);
			}
			return false;
		}

		public static bool CanSpawnInTiles(Rectangle tileRect)
		{
			for (int i = tileRect.Left; i < tileRect.Right; i++)
			{
				for (int j = tileRect.Top; j < tileRect.Bottom; j++)
				{
					if (!CanSpawnInTile(i, j))
					{
						return false;
					}
				}
			}
			return true;
		}

		public static bool CanSpawnInTile(int x, int y)
		{
			if (Main.tile[x, y].nactive() && Main.tileSolid[Main.tile[x, y].type])
			{
				return false;
			}
			if (Main.tile[x, y].anyLava())
			{
				return false;
			}
			return true;
		}

		public static bool CheckNotSpawningOnScreen(int spawnTileX, int spawnTileY)
		{
			Rectangle rectangle = new Rectangle(spawnTileX * 16, spawnTileY * 16, 16, 16);
			int num = sWidth / 2;
			int num2 = sHeight / 2;
			for (int i = 0; i < 255; i++)
			{
				Player player = Main.player[i];
				if (player.active && (!Main.dualDungeonsSeed || !player.insideUnbreakableWalls))
				{
					Rectangle value = new Rectangle((int)(player.Center.X - (float)num - (float)safeRangeX), (int)(player.Center.Y - (float)num2 - (float)safeRangeY), sWidth + safeRangeX * 2, sHeight + safeRangeY * 2);
					if (rectangle.Intersects(value))
					{
						return false;
					}
				}
			}
			return true;
		}

		public static bool Spawning_SandstoneCheck(int x, int y)
		{
			if (!WorldGen.InWorld(x, y, 10))
			{
				return false;
			}
			int num = 0;
			for (int i = 0; i < 8; i++)
			{
				Tile tile = Main.tile[x, y + i];
				if (!tile.active() || !TileID.Sets.Conversion.Sand[tile.type])
				{
					break;
				}
				num++;
				for (int j = 1; j <= 4; j++)
				{
					tile = Main.tile[x + j, y + i];
					if (!tile.active() || !TileID.Sets.Conversion.Sand[tile.type])
					{
						break;
					}
					num++;
				}
				for (int k = 1; k <= 4; k++)
				{
					tile = Main.tile[x - k, y + i];
					if (!tile.active() || !TileID.Sets.Conversion.Sand[tile.type])
					{
						break;
					}
					num++;
				}
			}
			if (Main.remixWorld)
			{
				return num >= 10;

```


---

## 🤖 Assistant · 2026-08-11T05:43:13.941Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '930,1190p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read SetSpawnFlagsForChosenTile"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:43:13.998Z

**📎 ToolResult**

```
				return false;
			}
			if (Main.tile[spawnTileX, spawnTileY - 1].liquid > 0 && Main.tile[spawnTileX, spawnTileY - 2].liquid > 0 && !Main.tile[spawnTileX, spawnTileY - 1].lava())
			{
				if (Main.tile[spawnTileX, spawnTileY - 1].shimmer())
				{
					return false;
				}
				if (Main.tile[spawnTileX, spawnTileY - 1].honey())
				{
					return false;
				}
			}
			if ((spawnTileType == 477 || spawnTileType == 492) && !Main.bloodMoon && !Main.eclipse && Main.invasionType <= 0 && !Main.pumpkinMoon && !Main.snowMoon && !Main.slimeRain && Main.rand.Next(100) < 10)
			{
				return false;
			}
			return true;
		}

		public void SetSpawnFlagsForChosenTile(int spawnTileX, int spawnTileY, int spawnTileType, int spawnWallType)
		{
			if (!skyMob && noGroundWorms)
			{
				noWorms = true;
			}
			Tile tile = Main.tile[spawnTileX, spawnTileY];
			waterTile = Main.tile[spawnTileX, spawnTileY - 1].liquid > 0 && Main.tile[spawnTileX, spawnTileY - 2].liquid > 0 && Main.tile[spawnTileX, spawnTileY - 1].liquidType() == 0;
			if (tile.type == 367)
			{
				nearMarble = true;
			}
			else if (tile.type == 368)
			{
				nearGranite = true;
			}
			else if (Main.tile[pX, pY].type == 367)
			{
				nearMarble = true;
			}
			else if (Main.tile[pX, pY].type == 368)
			{
				nearGranite = true;
			}
			else
			{
				int num = Main.rand.Next(20, 31);
				int num2 = Main.rand.Next(1, 4);
				if (spawnTileX - num < 0)
				{
					num = spawnTileX;
				}
				if (spawnTileY - num < 0)
				{
					num = spawnTileY;
				}
				if (spawnTileX + num >= Main.maxTilesX)
				{
					num = Main.maxTilesX - spawnTileX - 1;
				}
				if (spawnTileY + num >= Main.maxTilesY)
				{
					num = Main.maxTilesY - spawnTileY - 1;
				}
				for (int i = spawnTileX - num; i <= spawnTileX + num; i += num2)
				{
					int num3 = Main.rand.Next(1, 4);
					for (int j = spawnTileY - num; j <= spawnTileY + num; j += num3)
					{
						if (Main.tile[i, j].type == 367)
						{
							nearMarble = true;
						}
						if (Main.tile[i, j].type == 368)
						{
							nearGranite = true;
						}
					}
				}
				num = Main.rand.Next(30, 61);
				num2 = Main.rand.Next(3, 7);
				if (pX - num < 0)
				{
					num = pX;
				}
				if (pY - num < 0)
				{
					num = pY;
				}
				if (pX + num >= Main.maxTilesX)
				{
					num = Main.maxTilesX - pX - 2;
				}
				if (pY + num >= Main.maxTilesY)
				{
					num = Main.maxTilesY - pY - 2;
				}
				for (int k = pX - num; k <= pX + num; k += num2)
				{
					int num4 = Main.rand.Next(3, 7);
					for (int l = pY - num; l <= pY + num; l += num4)
					{
						if (Main.tile[k, l].type == 367)
						{
							nearMarble = true;
						}
						if (Main.tile[k, l].type == 368)
						{
							nearGranite = true;
						}
					}
				}
			}
			underGround = (double)spawnTileY <= Main.rockLayer;
			if (Main.remixWorld)
			{
				underGround = (double)spawnTileY > Main.rockLayer && spawnTileY <= Main.maxTilesY - 190;
			}
			bool flag = (double)spawnTileY > Main.rockLayer && spawnTileY < Main.UnderworldLayer;
			if (Main.dontStarveWorld)
			{
				flag = spawnTileY < Main.UnderworldLayer;
			}
			if (flag && !ZoneDungeon && !invaders)
			{
				if (Main.rand.Next(3) == 0)
				{
					int num5 = Main.rand.Next(5, 15);
					if (spawnTileX - num5 >= 0 && spawnTileX + num5 < Main.maxTilesX)
					{
						for (int m = spawnTileX - num5; m < spawnTileX + num5; m++)
						{
							for (int n = spawnTileY - num5; n < spawnTileY + num5; n++)
							{
								if (Main.tile[m, n].wall == 62)
								{
									spawnSpider = true;
								}
							}
						}
					}
				}
				else if (Main.tile[pX, pY].wall == 62)
				{
					spawnSpider = true;
				}
			}
			if ((double)spawnTileY < Main.rockLayer && spawnTileY > 200 && !ZoneDungeon && !invaders)
			{
				if (Main.rand.Next(3) == 0)
				{
					int num6 = Main.rand.Next(5, 15);
					if (spawnTileX - num6 >= 0 && spawnTileX + num6 < Main.maxTilesX)
					{
						for (int num7 = spawnTileX - num6; num7 < spawnTileX + num6; num7++)
						{
							for (int num8 = spawnTileY - num6; num8 < spawnTileY + num6; num8++)
							{
								if (WallID.Sets.AllowsUndergroundDesertEnemiesToSpawn[Main.tile[num7, num8].wall])
								{
									spawnUndergroundDesert = true;
								}
							}
						}
					}
				}
				else if (WallID.Sets.AllowsUndergroundDesertEnemiesToSpawn[Main.tile[pX, pY].wall])
				{
					spawnUndergroundDesert = true;
				}
			}
			isSpawningInWindDirection = (float)(pX - spawnTileX) * Main.windSpeedTarget > 0f;
			surfaceSpawn = (double)spawnTileY <= Main.worldSurface;
			deeperThanRockLayer = (double)spawnTileY >= Main.rockLayer;
			isOcean = ((spawnTileX < WorldGen.oceanDistance || spawnTileX > Main.maxTilesX - WorldGen.oceanDistance) && Main.tileSand[spawnTileType] && (double)spawnTileY < Main.rockLayer) || (spawnTileType == 53 && WorldGen.oceanDepths(spawnTileX, spawnTileY));
			isBeach = (double)spawnTileY <= Main.worldSurface && (spawnTileX < WorldGen.beachDistance || spawnTileX > Main.maxTilesX - WorldGen.beachDistance);
			if (Main.remixWorld)
			{
				if ((double)spawnTileY > Main.worldSurface && (double)spawnTileY < Main.rockLayer)
				{
					deeperThanRockLayer = true;
				}
				else
				{
					deeperThanRockLayer = false;
				}
				bool num9 = (double)spawnTileY < Main.worldSurface + 5.0;
				bool flag2 = spawnTileY > Main.UnderworldLayer;
				if (num9 || flag2)
				{
					raining = false;
				}
				if (num9)
				{
					dayTime = false;
				}
				if (ZoneCorrupt || ZoneCrimson)
				{
					isOcean = false;
					isBeach = false;
				}
				if ((double)spawnTileX < (double)Main.maxTilesX * 0.43 || (double)spawnTileX > (double)Main.maxTilesX * 0.57)
				{
					if ((double)spawnTileY > Main.rockLayer - 200.0 && spawnTileY < Main.maxTilesY - 200 && Main.rand.Next(2) == 0)
					{
						isOcean = true;
					}
					if ((double)spawnTileY > Main.rockLayer - 200.0 && spawnTileY < Main.maxTilesY - 200 && Main.rand.Next(2) == 0)
					{
						isBeach = true;
					}
				}
				if ((double)spawnTileY > Main.rockLayer - 20.0)
				{
					if (spawnTileY <= Main.maxTilesY - 190 && Main.rand.Next(3) != 0)
					{
						surfaceSpawn = true;
						dayTime = Main.rand.Next(2) == 0;
					}
					else if ((Main.bloodMoon || (Main.eclipse && Main.dayTime)) && (double)spawnTileX > (double)Main.maxTilesX * 0.38 + 50.0 && (double)spawnTileX < (double)Main.maxTilesX * 0.62)
					{
						surfaceSpawn = true;
					}
				}
			}
			if (dualDungeonsSpawnRules && (double)spawnTileY > Main.worldSurface && spawnTileY < Main.UnderworldLayer)
			{
				switch (Main.rand.Next(7))
				{
				case 0:
				case 1:
					surfaceSpawn = true;
					underGround = false;
					deeperThanRockLayer = false;
					break;
				case 2:
					surfaceSpawn = false;
					underGround = true;
					deeperThanRockLayer = false;
					break;
				case 3:
				case 4:
				case 5:
				case 6:
					surfaceSpawn = false;
					underGround = false;
					deeperThanRockLayer = true;
					break;
				}
				if (!tile.active() || tile.type != 48)
				{
					SetSpawnFlagsForChosenTile_ForDualDungeon(spawnTileX, spawnTileY, spawnTileType, spawnWallType);
				}
			}
		}

		public void SpawnAnNPC(int spawnTileX, int spawnTileY, int spawnTileType, bool xRange, int target)
		{
			int num = Main.tile[spawnTileX, spawnTileY - 1].wall;
			if (Main.tile[spawnTileX, spawnTileY - 2].wall == 244 || Main.tile[spawnTileX, spawnTileY].wall == 244)
			{

```


---

## 🤖 Assistant · 2026-08-11T05:43:42.330Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now, key details:

1. **waterTile (L957)**: `Main.tile[spawnTileX, spawnTileY - 1].liquid > 0 && ... && liquidType() == 0`. Tile.liquid is a byte 0-255. `liquid > 0` means any liquid amount. Our code: `st.liquid[above1] > 0` — need to check TileStore.liquid semantics. Let me check.

2. **underGround in original**: `underGround = (double)spawnTileY <= Main.rockLayer;` — note: original underGround is spawnTileY <= rockLayer (covers surface AND underground!). Our: `this.underGround = spawnTileY > this.world.groundLevel && spawnTileY < this.world.rockLevel;` — different! Actually our semantics differ significantly. But wait — in SpawnAnNPC the branches use `underGround` — in the original 1.4.4.9 code the flag was `underGround = spawnTileY <= rockLayer` meaning "not in cavern layer" — actually let me check the SpawnAnNPC chain to see how surfaceSpawn and underGround are used. In original SpawnAnNPC the ordering is surfaceSpawn first, then `if (underGround)`. Hmm, since surfaceSpawn checked first, underGround = y <= rockLayer effectively means "not deeper than rock layer" i.e. the "underground" (non-cavern) branch. Our implementation restricts to groundLevel < y < rockLevel. Behaviorally equivalent after surfaceSpawn branch taken first? surfaceSpawn = spawnTileY <= worldSurface. If surfaceSpawn is false, then spawnTileY > worldSurface. underGround original = spawnTileY <= rockLayer → so underground branch covers worldSurface < y <= rockLayer. Ours: groundLevel < y < rockLevel. So difference: spawnTileY == rockLevel exactly → original underGround true, ours false (falls to deeperThanRockLayer/cavern pool). Minor off-by-one. Worth noting.

Also note original `flag = (double)spawnTileY > Main.rockLayer && spawnTileY < Main.UnderworldLayer;` for spider. Ours: `spawnTileY > this.world.rockLevel && spawnTileY < st.h - 200`. Uses h-200 as UnderworldLayer approx — consistent with getSpawnRate. Also original desert check requires `!invaders` — ours doesn't check invaders. Minor.

Also spider scan in original: `for (int m = spawnTileX - num5; m < spawnTileX + num5; m++)` — no y bound check for world edges (they check x bounds with num5 but not y). Ours clamps. Minor.

Also note original: `if (spawnTileX - num5 >= 0 && spawnTileX + num5 < Main.maxTilesX)` — if x out of bounds, skip scanning entirely (even the player check). Ours clamps the scan box. Minor difference.

3. **HasTileSpawnSpace**: `Rectangle(spawnTileX - spawnSpaceX / 2, spawnTileY - spawnSpaceY, spawnSpaceX, spawnSpaceY)`. Need spawnSpaceX/Y values — search. Probably 2 and 3. Rectangle Right = Left + Width, Bottom = Top + Height. So x in [tx-1, tx+1), y in [ty-3, ty). Our loops dx -1..0 (2 tiles: tx-1, tx) and dy -3..-1 (ty-3, ty-2, ty-1). That matches if spawnSpaceX=2, spawnSpaceY=3. Good.

CanSpawnInTile: `nactive() && tileSolid` → false; `anyLava()` → false. Note nactive() = active() && !inActive(). Our isSolid may not check inActive (actuated tiles). Check TileStore.isSolid. Also anyLava() — Tile.anyLava likely checks liquidType==Lava && liquid>0? Let me check Tile.cs anyLava. Also our check `st.liquid[i] > 0 && st.liquidType[i] === 2` for lava.

Also note HasTileSpawnSpace's WorldGen.InWorld(rectangle) — InWorld for rectangle checks bounds with some margin? Let me check WorldGen.InWorld(Rectangle). Might require margin 1 or so. Our bounds check x<0||y<0 etc. Let's check.

4. **CheckNotSpawningOnScreen**: original loops over ALL 255 players and rejects if intersects ANY active player's screen (except dual dungeon). Our implementation only checks the one player passed in. In multiplayer this would differ, but our game is likely single-player. Also note: in our findSpawnTile we compute safeArea in tile coords using 0.52*screen tiles, then in checkNotSpawningOnScreen use safeRangeX as pixels (matching original quirk). Our rect: rectX = px - sW/2 - safePxX where safePxX = viewHalfW*1.04 (a tile count used as pixels, like original). That matches the original quirk. OK.

Wait, original: `safeRangeX` is in tiles (set in GetSpawnArea as `(int)(sWidth/16 * 0.52)`) but used in CheckNotSpawningOnScreen as pixels added to pixel rect. Our safePxX = viewHalfW * 1.04 — but that's the *half* tile count × 1.04, not full-screen-tiles × 0.52. viewHalfW = sWidth/32 tiles, so viewHalfW*1.04 = sWidth/32*1.04 ≈ 0.0325*sWidth. Original safeRangeX = sWidth/16*0.52 ≈ 0.0325*sWidth. Same. Good.

But in findSpawnTile, safeX = floor(viewHalfW * 1.04) tiles; original safeRangeX tiles = sWidth/16*0.52 = viewHalfW*1.04 (as real number, then int cast of full expression). Our floor(viewHalfW*1.04) vs original (int)((sWidth/16)*0.52). viewHalfW presumably integer = floor(sWidth/32)? If viewHalfW is sWidth/32 exactly then same. Roughly equal. Fine.

Now the safeArea check: original `!safeArea.Contains(spawnTileX, spawnTileY)`. Rectangle.Contains(x,y) = x >= Left && x < Left+Width && y >= Top && y < Top+Height. safeArea = CenteredRectangle(tile coords, Point(safeRangeX*2, safeRangeY*2)) then clamped to world. So Contains = |tx-cx| < safeRangeX && |ty-cy| < safeRangeY. Our: `Math.abs(tx-px) < safeX && Math.abs(ty-py) < safeY` → continue if inside. Equivalent. Good.

But important: original spawns happen for xRange = spawnTileX >= safeArea.Left && spawnTileX < safeArea.Right — i.e., whether spawn is horizontally on screen (used for water spawning xRange semantics). Our: `tx >= px - safeX && tx < px + safeX` — but original uses safeArea.Left/Right which are clamped to world bounds, not px-safeRangeX. At world edges this differs slightly. Minor.

5. **FindSpawnTile scan range**: original spawnArea: num = (int)((sWidth/16)*0.7), spawnArea = CenteredRectangle(tile, Point(num*2, num2*2)) clamped to world. So half-width = num = 0.7 × full-screen tiles = 1.4 × viewHalfW. Ours rangeX = floor(viewHalfW*1.4). Equivalent given viewHalfW = sWidth/32. Good.

Downward scan: original `for (; j < Main.maxTilesY && j < spawnArea.Bottom && (!nactive || !solid); j++)` then `if (j >= spawnArea.Bottom) continue;`. So scan limit is min(maxTilesY, spawnArea.Bottom) = spawnArea.Bottom. Ours: `while (j < areaB && !solid) j++; if (j >= areaB) continue;` — matches. But note original also checks the initial solid check at j itself; ours too since while checks first. Good. But original nactive()&&tileSolid — actuator nuance again.

Also: original checks `(Main.tile[num, j].nactive() && Main.tileSolid[...])` for initial point; ours `st.isSolid(tx,ty)`. Also original condition `(!ignoreSafeWalls && Main.wallHouse[...])` — the initial-point house wall skip is skipped when ignoreSafeWalls (invasion/towers). Ours doesn't have ignoreSafeWalls. Minor (we don't implement towers).

skyMob: intentionally changed, don't report.

6. **Try attempts 50** — matches (original `for (int i = 0; i < 50; i++)`). Good.

7. **spawnRate flow order in TrySpawnAnNPC**: original order: SetSpawnFlags → GetSpawnRate → check nearbyActiveNPCs >= maxSpawns → rand.Next(spawnRate)==0 → FindSpawnTile → CheckNotSpawningOnScreen → GetProperGround... → PostCheck → SetSpawnFlagsForChosenTile → SpawnAnNPC.

Our flow (Game.trySpawnEnemy presumably calls getSpawnRate separately then spawn()). In our `spawn()`, we do findSpawnTile then checkNotSpawningOnScreen then setFlags inside findSpawnTile. PostCheck ordering: ours does PostCheck inside findSpawnTile (continue retry on fail) — original: PostCheck fail → return false (no retry!). Original: `if (!PostCheckChosenSpawnTile(...)) return false;` — this aborts the entire attempt without trying another point. Ours treats it as a retry condition (continue) — a real semantic difference. Since ZoneDungeon rarely set, low impact but a real bug (behavior: original gives up for this frame; ours keeps sampling points and can spawn elsewhere).

Also ours doesn't do the "GetProperGroundSpawnTileTypeAndWallType" — the original spawnTileType is the tile at spawnTileY-1? Let me read GetProperGroundSpawnTileTypeAndWallType (L5789).

Also note ours sets skyMob groundType=0.

Also original PostCheck: `if (ZoneDungeon && (!Main.tileDungeon[spawnTileType] || spawnWallType == 0)) return false;` where spawnWallType comes from GetProperGround... Let me read that function. Also the water tile check in PostCheck (liquid & !lava, shimmer, honey → false) and tile 477/492 check.

Also important: original PostCheck has the water/liquid rejection: if the two tiles above have liquid and not lava → return false (i.e., don't spawn swimming enemies through this path? Actually it returns false meaning abort). Let me read full PostCheck from L922.

Let me now read L5789-5830 (GetProperGround...) and L922-950 (PostCheck full), and find spawnSpaceX/spawnSpaceY defaults, defaultSpawnRate, and check TileStore.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:43:43.330Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '915,950p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo ====; sed -n '5789,5835p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo ====; grep -n \"spawnSpaceX\\|spawnSpaceY\\|defaultSpawnRate\\s*=\\|defaultMaxSpawns\\s*=\\|sWidth\\s*=\\|sHeight\\s*=\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -20",
 "description": "Read PostCheck + GetProperGround + constants"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:43:43.359Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
			}
			spawnTileX = 0;
			spawnTileY = 0;
			xRange = false;
			return false;
		}

		private bool PostCheckChosenSpawnTile(int spawnTileX, int spawnTileY, int spawnTileType, int spawnWallType)
		{
			if (ZoneDungeon && (!Main.tileDungeon[spawnTileType] || spawnWallType == 0))
			{
				return false;
			}
			if (Main.dualDungeonsSeed && Main.tile[spawnTileX, spawnTileY].type == 48)
			{
				return false;
			}
			if (Main.tile[spawnTileX, spawnTileY - 1].liquid > 0 && Main.tile[spawnTileX, spawnTileY - 2].liquid > 0 && !Main.tile[spawnTileX, spawnTileY - 1].lava())
			{
				if (Main.tile[spawnTileX, spawnTileY - 1].shimmer())
				{
					return false;
				}
				if (Main.tile[spawnTileX, spawnTileY - 1].honey())
				{
					return false;
				}
			}
			if ((spawnTileType == 477 || spawnTileType == 492) && !Main.bloodMoon && !Main.eclipse && Main.invasionType <= 0 && !Main.pumpkinMoon && !Main.snowMoon && !Main.slimeRain && Main.rand.Next(100) < 10)
			{
				return false;
			}
			return true;
		}

		public void SetSpawnFlagsForChosenTile(int spawnTileX, int spawnTileY, int spawnTileType, int spawnWallType)
(eval):1: === not found

```


---

## 🤖 Assistant · 2026-08-11T05:43:43.917Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"liquid\" ~/Project/GLM/SandboxWorld/game/src/world/store/TileStore.ts | head -30; echo ====; grep -rn \"isSolid\\s*(\" ~/Project/GLM/SandboxWorld/game/src/world/store/TileStore.ts | head",
 "description": "Check TileStore liquid and isSolid semantics"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:43:43.946Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
ugrep: warning: ~/Project/GLM/SandboxWorld/game/src/world/store/TileStore.ts: No such file or directory
(eval):1: === not found

```


---

## 🤖 Assistant · 2026-08-11T05:43:45.421Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The `====` echo got interpreted weirdly? "(eval):1: === not found" — zsh treats `====` as glob? Anyway, first part output partially. Let me redo carefully with quoted separators.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:43:46.110Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"spawnSpaceX\\|spawnSpaceY\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head; echo \"----\"; grep -n \"defaultSpawnRate\\|defaultMaxSpawns\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head",
 "description": "Find spawnSpace and default rate constants"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:43:46.143Z

**📎 ToolResult**

```
41:		public static int spawnSpaceX = 2;
43:		public static int spawnSpaceY = 3;
5308:			Rectangle rectangle = new Rectangle(spawnTileX - spawnSpaceX / 2, spawnTileY - spawnSpaceY, spawnSpaceX, spawnSpaceY);
----
181:			int num2 = (int)((float)defaultMaxSpawns * (2f + 0.3f * (float)numberOfActivePlayers));
385:			spawnRate = defaultSpawnRate;
386:			maxSpawns = defaultMaxSpawns;
389:				spawnRate = (int)((double)defaultSpawnRate * 0.9);
390:				maxSpawns = defaultMaxSpawns + 1;
659:			if ((double)spawnRate < (double)defaultSpawnRate * 0.1)
661:				spawnRate = (int)((double)defaultSpawnRate * 0.1);
663:			if (maxSpawns > defaultMaxSpawns * 3)
665:				maxSpawns = defaultMaxSpawns * 3;
683:				maxSpawns = (int)((double)defaultMaxSpawns * (2.0 + 0.3 * (double)numberOfActivePlayers));

```


---

## 🤖 Assistant · 2026-08-11T05:43:46.580Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/game/src -name \"TileStore*\"; echo \"----\"; grep -rn \"liquid\" ~/Project/GLM/SandboxWorld/game/src/world/World.ts | head -20",
 "description": "Locate TileStore and liquid field"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:43:46.687Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts
----
~/Project/GLM/SandboxWorld/game/src/world/World.ts:160:  liquidAt(px: number, py: number): number {
~/Project/GLM/SandboxWorld/game/src/world/World.ts:161:    return this.store.liquid[this.store.idx(Math.floor(px / 16), Math.floor(py / 16))];

```


---

## 🤖 Assistant · 2026-08-11T05:43:48.297Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
defaultSpawnRate/defaultMaxSpawns must be defined in Main.cs. Let me check. Also read TileStore.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:43:54.037Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"defaultSpawnRate\\|defaultMaxSpawns\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head; echo \"----\"; grep -n \"liquid\\|isSolid\\|inActive\\|actuator\" ~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts | head -40",
 "description": "Check Main defaults and TileStore liquid/isSolid"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:43:54.102Z

**📎 ToolResult**

```
----
13:  readonly liquid: Uint8Array;   // 0-255 液量
14:  readonly liquidType: Uint8Array; // 0无 1水 2岩浆 3蜂蜜
17:  readonly wire: Uint8Array;      // 电路位（原版 Tile.cs sTileHeader）：bit0红 bit1蓝 bit2绿 bit3黄 bit4致动器 bit5已致动(inActive)
18:  // wire 位掩码常量（对应原版 Tile.cs:396-459 的 wire/wire2/wire3/wire4/actuator/inActive）
31:  /** 本地 tile 变更上报（协议层 TileOp 收集器）。liquid 通道不报（客户端本地模拟） */
46:      this.liquid = new Uint8Array(bufs.liquid);
47:      this.liquidType = new Uint8Array(bufs.liquidType);
59:    this.liquid = new Uint8Array(n);
60:    this.liquidType = new Uint8Array(n);
75:    // 原版 nactive() = active && !inActive（Tile.cs:383-394）：已致动格视为不活跃
80:  /** 原版 inActive()：致动器翻转后的"缩入地下"态（有 type 但不碰撞不阻挡） */
85:  isSolid(x: number, y: number): boolean {
104:  private liquidListeners: Array<(x: number, y: number) => void> = [];
106:    this.liquidListeners.push(fn);
177:  /** 致动器翻转 inActive 态（Wiring.DeActive/ReActive 用）：影响碰撞与渲染，须发 listeners */
192:    if (this.liquid[i] === a && this.liquidType[i] === type) return;
193:    this.liquid[i] = a;
194:    this.liquidType[i] = type;
195:    this.liquidListeners.forEach((fn) => fn(x, y));

```


---

## 🤖 Assistant · 2026-08-11T05:44:05.800Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
TileStore.liquid is Uint8Array 0-255 — same byte semantics as original Tile.liquid (byte). So `> 0` matches original. Good, and liquidType: 0 none, 1 water, 2 lava, 3 honey. Original liquidType(): 0 water, 1 lava, 2 honey (LiquidID: Water=0, Lava=1, Honey=2). So our liquidType===1 means water in our scheme — matches original `liquidType() == 0` (water). Good.

Now check isSolid definition (L75-102) to see nactive semantics.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:44:05.991Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts",
 "offset": 60,
 "limit": 50
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:44:05.997Z

**📎 ToolResult**

```
60	    this.liquidType = new Uint8Array(n);
61	    this.half = new Uint8Array(n);
62	    this.slope = new Uint8Array(n);
63	    this.wire = new Uint8Array(n);
64	  }
65	
66	  idx(x: number, y: number): number { return y * this.w + x; }
67	
68	  inBounds(x: number, y: number): boolean {
69	    return x >= 0 && y >= 0 && x < this.w && y < this.h;
70	  }
71	
72	  get(x: number, y: number): number { return this.inBounds(x, y) ? this.type[this.idx(x, y)] : 0; }
73	
74	  isActive(x: number, y: number): boolean {
75	    // 原版 nactive() = active && !inActive（Tile.cs:383-394）：已致动格视为不活跃
76	    return this.inBounds(x, y) && this.type[this.idx(x, y)] !== 0
77	      && (this.wire[this.idx(x, y)] & TileStore.WIRE_ACTUATED) === 0;
78	  }
79	
80	  /** 原版 inActive()：致动器翻转后的"缩入地下"态（有 type 但不碰撞不阻挡） */
81	  isActuated(x: number, y: number): boolean {
82	    return this.inBounds(x, y) && (this.wire[this.idx(x, y)] & TileStore.WIRE_ACTUATED) !== 0;
83	  }
84	
85	  isSolid(x: number, y: number): boolean {
86	    if (!this.inBounds(x, y)) return false; // 世界外视为空（边缘自由）
87	    if (this.wire[this.idx(x, y)] & TileStore.WIRE_ACTUATED) return false; // 已致动不碰撞
88	    const d = TILE_DEFS[this.type[this.idx(x, y)]];
89	    return !!d && d.solid;
90	  }
91	
92	  isPlatform(x: number, y: number): boolean {
93	    if (!this.inBounds(x, y)) return false;
94	    const d = TILE_DEFS[this.type[this.idx(x, y)]];
95	    return !!d && d.platform;
96	  }
97	
98	  onTileChanged(fn: (x: number, y: number) => void) {
99	    this.listeners.push(fn);
100	  }
101	
102	  /** 液体变化独立通道：chunk 缓存不订阅（水不入烘焙画布，无需重建），
103	   *  只有光照订阅（水的光衰减）——避免水流时每帧冲爆 chunk 重建队列造成卡顿 */
104	  private liquidListeners: Array<(x: number, y: number) => void> = [];
105	  onLiquidChanged(fn: (x: number, y: number) => void) {
106	    this.liquidListeners.push(fn);
107	  }
108	
109	  /** 唯一的写入入口（生成/导入期可绕过用 setTileSilent） */

```


---

## 🤖 Assistant · 2026-08-11T05:44:06.625Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"defaultSpawnRate\\|defaultMaxSpawns\\|public static int sWidth\\|public static int sHeight\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/*.cs | grep -v \"NPC.cs\" | head",
 "description": "Find defaultSpawnRate in other files"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:44:06.667Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-11T05:44:08.703Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
defaultSpawnRate/defaultMaxSpawns not found in Terraria/*.cs grep outside NPC.cs — they're probably `Spawner.defaultSpawnRate` static fields declared elsewhere in NPC.cs (fields). Let me grep within NPC.cs lines 39-140.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:44:09.307Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '39,140p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -n \"default\\|safeRange\\|static int\" ",
 "description": "Read Spawner field declarations"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:44:09.363Z

**📎 ToolResult**

```
3:		public static int spawnSpaceX = 2;
5:		public static int spawnSpaceY = 3;

```


---

## 🤖 Assistant · 2026-08-11T05:44:09.862Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"anyLava\\|public bool liquidType\\|liquidType()\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Tile.cs | head",
 "description": "Check Tile.anyLava semantics"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:44:09.898Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Tile.cs:265:	public byte liquidType()
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Tile.cs:428:		return liquidType() == 0;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Tile.cs:440:	public bool anyLava()

```


---

## 🤖 Assistant · 2026-08-11T05:44:11.856Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"defaultSpawnRate\\|defaultMaxSpawns\\|safeRangeX\\|safeRangeY\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -8; echo \"----\"; sed -n '425,450p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Tile.cs",
 "description": "Find field defaults and anyLava"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:44:11.891Z

**📎 ToolResult**

```
181:			int num2 = (int)((float)defaultMaxSpawns * (2f + 0.3f * (float)numberOfActivePlayers));
385:			spawnRate = defaultSpawnRate;
386:			maxSpawns = defaultMaxSpawns;
389:				spawnRate = (int)((double)defaultSpawnRate * 0.9);
390:				maxSpawns = defaultMaxSpawns + 1;
659:			if ((double)spawnRate < (double)defaultSpawnRate * 0.1)
661:				spawnRate = (int)((double)defaultSpawnRate * 0.1);
663:			if (maxSpawns > defaultMaxSpawns * 3)
----

	public bool water()
	{
		return liquidType() == 0;
	}

	public bool anyWater()
	{
		if (liquid > 0)
		{
			return water();
		}
		return false;
	}

	public bool anyLava()
	{
		if (liquid > 0)
		{
			return lava();
		}
		return false;
	}

	public bool anyHoney()
	{

```


---

## 🤖 Assistant · 2026-08-11T05:44:14.056Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Fields defaultSpawnRate/defaultMaxSpawns are declared in NPC.cs earlier — grep only matched usages, meaning declaration lines might be `public static int defaultSpawnRate = 600;` — but grep for "defaultSpawnRate" should match those too. The head -8 cut them off maybe (they'd be at lines 39-140). Let me grep with line numbers limited to < 200.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:44:14.621Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"defaultSpawnRate\\|defaultMaxSpawns\\|safeRangeX\\|safeRangeY\\|sWidth =\\|sHeight =\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | awk -F: '$1<200'",
 "description": "Find field declarations in first 200 lines"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:44:22.777Z

**📎 ToolResult**

```
181:			int num2 = (int)((float)defaultMaxSpawns * (2f + 0.3f * (float)numberOfActivePlayers));

```


---

## 🤖 Assistant · 2026-08-11T05:44:24.514Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '39,145p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read Spawner class fields"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:44:24.546Z

**📎 ToolResult**

```
	public class Spawner
	{
		public static int spawnSpaceX = 2;

		public static int spawnSpaceY = 3;

		public static bool fairyLog = false;

		public int numberOfActivePlayers;

		public bool reachedInvasionBossCap;

		public int pX;

		public int pY;

		public float luck;

		public bool dayTime;

		public bool raining;

		public int townNPCs;

		public bool skyMob;

		public bool noWorms;

		public bool noGroundWorms;

		public bool invaders;

		public bool spawnFriendly;

		public bool ignoreSafeWalls;

		public bool waterTile;

		public bool nearGranite;

		public bool nearMarble;

		public bool spawnSpider;

		public bool surfaceSpawn;

		public bool spawnUndergroundDesert;

		public bool hardDungeon;

		public bool deeperThanRockLayer;

		public bool underGround;

		public bool isOcean;

		public bool isBeach;

		public bool isSpawningInWindDirection;

		public bool skyBehindPlayer;

		public bool livingTree;

		public bool dualDungeonsSpawnRules;

		public bool inDualDungeon;

		public bool tresspassingDualDungeon;

		public bool inRemixStartingArea;

		public bool offensiveToTim;

		public bool playerHasStartingHealth;

		public bool ZoneCorrupt;

		public bool ZoneCrimson;

		public bool ZoneHallow;

		public bool ZoneJungle;

		public bool ZoneSnow;

		public bool ZoneGlowshroom;

		public bool ZoneMeteor;

		public bool ZoneGraveyard;

		public bool ZoneDungeon;

		public bool ZoneLihzhardTemple;

		public bool ZoneGranite;

		public bool ZoneMarble;

		public bool ZoneSandstorm;

		public bool ZoneTowerSolar;

		public bool ZoneTowerVortex;

		public bool ZoneTowerNebula;

```


---

## 🤖 Assistant · 2026-08-11T05:44:27.309Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '145,200p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read remaining fields incl defaults"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:44:27.336Z

**📎 ToolResult**

```
		public bool ZoneTowerNebula;

		public bool ZoneTowerStardust;

		public bool ZoneOldOneArmy;

		public bool ZoneWaterCandle;

		public bool ZonePeaceCandle;

		public bool ZoneShadowCandle;

		public int defaultTarget = 255;

		public Spawner()
		{
			numberOfActivePlayers = Main.CurrentFrameFlags.ActivePlayersCount;
			float num = 0f;
			for (int i = 0; i < Main.maxNPCs; i++)
			{
				if (Main.npc[i].active)
				{
					switch (Main.npc[i].type)
					{
					case 315:
					case 325:
					case 327:
					case 328:
					case 344:
					case 345:
					case 346:
						num += Main.npc[i].npcSlots;
						break;
					}
				}
			}
			int num2 = (int)((float)defaultMaxSpawns * (2f + 0.3f * (float)numberOfActivePlayers));
			reachedInvasionBossCap = num >= (float)(numberOfActivePlayers * num2);
		}

		public void SpawnNPC()
		{
			for (int i = 0; i < 255; i++)
			{
				Player player = Main.player[i];
				if (CanSpawnEnemiesNear(player))
				{
					if (Main.slimeRain)
					{
						SlimeRainSpawns(player);
					}
					if (TrySpawnAnNPC(player))
					{
						break;
					}
				}

```


---

## 🤖 Assistant · 2026-08-11T05:44:29.361Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
defaultSpawnRate/defaultMaxSpawns/sWidth/sHeight/safeRangeX/safeRangeY must be static fields in the outer NPC class (not Spawner). Search whole NPC.cs for "static int defaultSpawnRate" — grep found none with "="; maybe declared as `public static int defaultSpawnRate;` set in Main? Or fields in NPC class elsewhere. Let me grep the whole repo.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:44:30.037Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"defaultSpawnRate\\b\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ | grep -v \"NPC.cs\" | head; echo \"----\"; grep -rn \"defaultSpawnRate\\s*=\\s*600\\|defaultSpawnRate =\" ~/Project/GLM/SandboxWorld/Terarria1456/ | head",
 "description": "Search defaultSpawnRate definition repo-wide"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:44:30.108Z

**📎 ToolResult**

```
----
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:6108:	private static int defaultSpawnRate = 600;

```


---

## 🤖 Assistant · 2026-08-11T05:44:32.026Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '6100,6115p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo \"----\"; grep -n \"safeRangeX\\|safeRangeY\\|static int sWidth\\|static int sHeight\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | tail -5",
 "description": "Read default constants and sWidth/sHeight decls"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:44:32.059Z

**📎 ToolResult**

```
	private static int townRangeY = sHeight;

	public float npcSlots = 1f;

	private static bool noSpawnCycle = false;

	private static int activeTime = 750;

	private static int defaultSpawnRate = 600;

	private static int defaultMaxSpawns = 5;

	public float shimmerTransparency;

	public bool dontCountMe;

----
6092:	public static int safeRangeY = (int)((double)(sHeight / 16) * 0.52);
6695:	public static int sWidth => 1920;
6697:	public static int sHeight => 1200;
53837:				Rectangle rectangle = new Rectangle((int)(position.X + (float)(width / 2) - (float)(sWidth / 2) - (float)safeRangeX), (int)(position.Y + (float)(height / 2) - (float)(sHeight / 2) - (float)safeRangeY), sWidth + safeRangeX * 2, sHeight + safeRangeY * 2);
53840:					rectangle = new Rectangle(floorX * 16 + 8 - sWidth / 2 - safeRangeX, floorY * 16 + 8 - sHeight / 2 - safeRangeY, sWidth + safeRangeX * 2, sHeight + safeRangeY * 2);

```


---

## 🤖 Assistant · 2026-08-11T05:44:33.261Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '6085,6095p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read safeRangeX declaration"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:44:33.294Z

**📎 ToolResult**

```
	public int realLife = -1;

	private string _givenName = "";

	public static int safeRangeX = (int)((double)(sWidth / 16) * 0.52);

	public static int safeRangeY = (int)((double)(sHeight / 16) * 0.52);

	private static int activeRangeX = (int)((double)sWidth * 2.1);

```


---

## 🤖 Assistant · 2026-08-11T05:44:37.315Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting: `safeRangeX = (int)((sWidth/16)*0.52)` — sWidth = 1920 (const). Note that sWidth is a compile-time-ish const (1920×1200), NOT actual screen size. So safeRangeX ≈ 62 tiles, safeRangeY ≈ 39 tiles. And in GetSpawnArea, safeRangeX is recomputed from the same formula (0.52 × full screen tiles). Our viewHalfW = actual screen half in tiles presumably from the game (Game passes viewHalfW). Let me check what Game passes as viewHalfW/H.

Also key point: spawnArea num = (int)((sWidth/16)*0.7) where sWidth=1920 → 84 tiles; ×2 = 168 wide. So our ×1.4 of viewHalfW is equivalent only if viewHalfW = sWidth/32. Let me check the game's call site.

Now GetProperGroundSpawnTileTypeAndWallType (L5789) — I need to see it. Earlier sed 5789-5835 didn't print due to the error. Let me read it.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:44:37.613Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '5789,5860p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read GetProperGroundSpawnTileTypeAndWallType"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:44:37.648Z

**📎 ToolResult**

```
		public static void GetProperGroundSpawnTileTypeAndWallType(int x, int y, out int spawnTileType, out int spawnWallType)
		{
			spawnTileType = Main.tile[x, y].type;
			spawnWallType = ((y > 0) ? Main.tile[x, y - 1].wall : 0);
			if (TileID.Sets.UsesADifferentTileTypeForNPCSpawning[spawnTileType] && WorldGen.InWorld(x, y + 1) && WorldGen.SolidTile3(x, y + 1))
			{
				Tile tile = Main.tile[x, y];
				spawnTileType = Main.tile[x, y + 1].type;
				spawnWallType = tile.wall;
			}
			if (IsValidSpawningGroundTile(x, y))
			{
				return;
			}
			for (int i = y + 1; i < y + 30; i++)
			{
				if (IsValidSpawningGroundTile(x, i))
				{
					Tile tile2 = Main.tile[x, i - 1];
					spawnTileType = Main.tile[x, i].type;
					spawnWallType = tile2.wall;
					break;
				}
			}
		}

		public static bool IsValidSpawningGroundTile(int x, int y)
		{
			Tile tile = Main.tile[x, y];
			if (!tile.nactive())
			{
				return false;
			}
			if (!Main.tileSolid[tile.type] || Main.tileSolidTop[tile.type])
			{
				return false;
			}
			return true;
		}

		public static void SlimeRainSpawns(Player player)
		{
			int y = Main.MaxWorldViewSize.Y;
			int x = Main.MaxWorldViewSize.X;
			float num = 15f;
			if ((double)player.position.Y > Main.worldSurface * 16.0 + (double)(y / 2) || player.nearbyActiveNPCs > num)
			{
				return;
			}
			float num2 = player.nearbyActiveNPCs / num;
			int num3 = 45 + (int)(450f * num2);
			if (Main.expertMode)
			{
				num3 = (int)((double)num3 * 0.85);
			}
			if (Main.IsJourneyMode)
			{
				CreativePowers.SpawnRateSliderPerPlayerPower power = CreativePowerManager.Instance.GetPower<CreativePowers.SpawnRateSliderPerPlayerPower>();
				if (power != null && power.GetIsUnlocked() && power.GetRemappedSliderValueFor(player.whoAmI, out var value))
				{
					num3 = (int)((float)num3 / value);
				}
			}
			if (Main.rand.Next(num3) != 0)
			{
				return;
			}
			int num4 = (int)(player.Center.X - (float)x);
			int maxValue = num4 + x * 2;
			int minValue = (int)((double)player.Center.Y - (double)y * 1.5);
			int maxValue2 = (int)((double)player.Center.Y - (double)y * 0.75);
			int num5 = Main.rand.Next(num4, maxValue);

```


---

## 🤖 Assistant · 2026-08-11T05:44:38.205Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"trySpawnEnemy\\|vanillaSpawner.spawn\\|\\.spawn(\" ~/Project/GLM/SandboxWorld/game/src --include=*.ts | grep -i spawn | head",
 "description": "Find Game call site for spawner"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:44:38.231Z

**📎 ToolResult**

```
(eval):1: no matches found: --include=*.ts

```


---

## 🤖 Assistant · 2026-08-11T05:44:49.475Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
GetProperGround: spawnTileType = Main.tile[x,y].type (the tile at the spawn tile itself, which is the first solid tile found going down — wait, in FindSpawnTile the loop ends when nactive && tileSolid, so spawnTileY is a SOLID tile. Then GetProperGround takes tile[x,y].type where y = spawnTileY — the solid tile itself). But then "UsesADifferentTileTypeForNPCSpawning" and "IsValidSpawningGroundTile" — if the tile at spawnTileY is not a valid spawning ground (e.g. it's a platform / solidTop), it searches DOWN up to 30 tiles for the first valid ground and takes that tile's type and the wall above it.

Important: spawnWallType = wall of tile ABOVE the ground tile (tile[x, i-1].wall) — which is what PostCheck uses (`spawnWallType == 0` → reject in dungeon). Our implementation uses `st.wall[idx(tx,ty)]` — the wall at the spawn tile (which is solid ground, likely natural/dirt wall) rather than the wall at the tile above. That's a real bug: dungeon check requires wall above the ground tile ≠ 0; since we check the wall at the ground tile itself, deep dungeon floors would almost always have a wall ≠ 0 anyway... Actually for the dungeon, PostCheck requires spawnWallType != 0, i.e., there's a wall directly above the ground. Since the spawn tile y is the solid floor, wall at (tx, ty-1) is the free space above. Hmm — wait, GetProperGround: spawnWallType = Main.tile[x, y-1].wall where y=spawnTileY. So wall above the solid floor. In our code: `st.wall[st.idx(tx, ty)]` — wall at the solid floor tile itself. In a dungeon interior, the floor tile also typically has dungeon wall behind it (walls extend behind solid tiles too). Actually walls exist behind solid tiles if generated... In Terraria, dungeon walls are placed in empty spaces mostly, but the brick tiles themselves may have wall 0. Hmm. Also our skyMob groundType=0 special-case.

So real bug #1: our spawnTileType derivation. We take `st.type[tx,ty]` directly (the solid tile found). Original takes tile[x,y].type too — same when the solid tile is a valid spawning ground (solid and not solidTop). But original additionally: (a) UsesADifferentTileTypeForNPCSpawning mapping; (b) if the found solid tile is a platform/solidTop (IsValidSpawningGroundTile false), it scans DOWN up to 30 tiles for real ground and uses THAT type and the wall above it — importantly the spawn Y stays the same but the type used for pool selection differs. Ours lacks both. Given our findSpawnTile stops at first solid (isSolid → TILE_DEFS solid; platforms likely not solid), the platform case is mostly moot. But note original FindSpawnTile loop condition uses `Main.tileSolid[type]` (any solid, including platforms? tileSolid is true for platforms? Actually platforms: Main.tileSolid[19] (wood platform) is true? In Terraria, tileSolid is true for platforms — they're "solid" but with solidTop also true). So original can stop on a platform, then GetProperGround corrects by scanning down. Our isSolid may return false for platforms → we'd scan past them. Minor.

Now let me check the Game call site to verify viewHalfW semantics and the spawnRate gating order.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:44:49.992Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"trySpawnEnemy\" ~/Project/GLM/SandboxWorld/game/src -l; echo \"----\"; grep -rn \"getSpawnRate\" ~/Project/GLM/SandboxWorld/game/src | head",
 "description": "Locate Game spawn orchestration"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:44:50.029Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/core/Game.ts
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts
----
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1411:    // 水蜡烛(Main.waterCandle 语义):手持或 32 格内有放置态 → 刷怪率修正（getSpawnRate 内）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1450:    // （Next(spawnRate)==0；spawnRate 修正表见 VanillaSpawner.getSpawnRate）。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1451:    // 水蜡烛（heldWaterCandle/waterCandleNear）在 getSpawnRate 内修正，不再改节流
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3897:    const { spawnRate, maxSpawns } = this.vanillaSpawner.getSpawnRate(
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:357:  getSpawnRate(playerYpx: number, nearbySlots: number, waterCandle: boolean, sHeightPx: number): { spawnRate: number; maxSpawns: number } {

```


---

## 🤖 Assistant · 2026-08-11T05:44:51.638Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '3860,3960p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Read Game spawn orchestration"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:44:51.659Z

**📎 ToolResult**

```
  private trySpawnEnemy() {
    // 联机模式：刷怪归房主权威（房主跑完整模拟，快照广播给访客；访客不本地刷怪）
    if (this.net && !this.net.policy.isHost) return;
    const w = this.world;
    const p = this.player;
    if (p.dead) return;
    if (this.boss) return;

    // 原版 Spawner 1:1（VanillaSpawner.ts）：选点+选怪全部按 SpawnAnNPC 链
    if (!this.vanillaSpawner) this.vanillaSpawner = new VanillaSpawner(w);
    // 原版 Spawner.SetSpawnFlags：地牢旗标取玩家 SceneMetrics（15 tick 刷新的 scene），
    // downedBoss3（杀过骷髅王）决定地牢出 守卫/常规池；
    // invaders = ShouldSpawnInvasionEnemies（NPC.cs:352：入侵前线 3000px 内的地表玩家）；
    // activeIds = 场上存活 NPC 集（入侵选表 AnyNPCs 去重）
    const invaders = shouldSpawnInvasionEnemies(w, p.cx, p.cy, this.camera.viewH / (this.camera.zoom || 1),
      this.entities.npcs.filter((n) => n instanceof TownNPC && !n.dead).map((n) => (n as TownNPC).cx));
    const activeIds = new Set<number>();
    for (const e of this.entities.enemies) {
      const en = e as Enemy;
      if (!en.dead && en.vanillaId != null) activeIds.add(en.vanillaId);
    }
    this.vanillaSpawner.setPlayerFlags(!!this.scene?.zoneDungeon, !!w.flags.downedSkeletron, invaders, activeIds);
    // 天气注入（雪原雨刷怪率修正 + 沙尘暴怪池门）
    this.vanillaSpawner.setWeather(
      w.weather.cloudAlpha,
      w.weather.sandstorm.happening,
      !!this.scene?.zoneDesert && p.cy / 16 < w.groundLevel + 30,
    );
    // TrySpawnAnNPC L23：nearbyActiveNPCs >= maxSpawns 拒绝
    // （原版 nearbyActiveNPCs = 附近 NPC 的 npcSlots 加权和；我们的怪全部由 spawner 生成
    //  在玩家附近，直接全量求和。蠕虫段也是独立 NPC，原版同样计入）
    const nearby = this.entities.enemies.reduce((s, e) => {
      const en = e as Enemy;
      if (en.def.boss) return s;
      return s + (en.vanilla?.npcSlots ?? 1);
    }, 0);
    const sHeightPx = this.camera.viewH / (this.camera.zoom || 1);
    const { spawnRate, maxSpawns } = this.vanillaSpawner.getSpawnRate(
      p.cy, nearby, this.heldWaterCandle || this.waterCandleNear, sHeightPx);
    if (nearby >= maxSpawns) return;
    // TrySpawnAnNPC L30：Main.rand.Next(spawnRate) != 0 拒绝（每帧 1/spawnRate 概率）
    if (Math.floor(Math.random() * spawnRate) !== 0) return;
    const viewHalfW = Math.ceil(this.camera.viewW / (this.camera.zoom || 1) / 2 / TILE);
    const viewHalfH = Math.ceil(this.camera.viewH / (this.camera.zoom || 1) / 2 / TILE);
    const rng = new RNG((Math.random() * 1e9) | 0);
    const picked = this.vanillaSpawner.spawn(p.cx, p.cy, rng, viewHalfW, viewHalfH);
    if (!picked) return;
    // 骷髅商（NPC.cs:4906-4910）：转 TownNPC 进 npcs 桶；场上已有则跳过（CountNPCS(453)==0）
    if (picked.vanillaId === 453) {
      if (this.entities.npcs.some((n) => n instanceof TownNPC && !n.dead && n.npcKey === 'skeleton_merchant')) return;
      const sm = new TownNPC('skeleton_merchant', this.vanillaSpawner.currentSpawnX * TILE + 8, (this.vanillaSpawner.currentSpawnY + 1) * TILE);
      this.entities.add(sm, 'npcs');
      return;
    }
    // 放置：原版 SpawnNPC 直接落位；水生/蠕虫分支由链内返回的怪自带 AI 处理落脚
    const st = w.store;
    const ptx = this.vanillaSpawner.currentSpawnX;
    const pty = this.vanillaSpawner.currentSpawnY;
    if (ptx < 2 || pty < 2 || ptx > st.w - 3 || pty > st.h - 3) return;
    if (picked.vanilla?.aiStyle === 6) {
      // 蠕虫族：段链（AI_006 的 NewNPC 链）
      picked.x = ptx * TILE + 8 - picked.w / 2;
      picked.y = pty * TILE + 8 - picked.h / 2;
      picked.id = this.entities.nextId++;
      this.entities.enemies.push(picked);
      const segs = Enemy.spawnWormChain(picked, 5 + ((rng.next() * 4) | 0));
      for (const seg of segs) { seg.id = this.entities.nextId++; this.entities.enemies.push(seg); }
      return;
    }
    if (picked.vanilla?.aiStyle === 16 || picked.vanilla?.aiStyle === 18) {
      // 水生族：找水下格
      for (let dy = -8; dy <= 100; dy++) {
        const yy = pty + dy;
        if (yy < 2 || yy > st.h - 3) continue;
        if (st.liquid[st.idx(ptx, yy)] > 150 && !st.isSolid(ptx, yy)) {
          picked.x = ptx * TILE + 8 - picked.w / 2;
          picked.y = yy * TILE;
          picked.id = this.entities.nextId++;
          this.entities.enemies.push(picked);
          return;
        }
      }
      return;
    }
    if (picked.vanilla?.critter) {
      // 小动物进 critters 桶（不计怪上限）
      let groundY = pty;
      while (groundY > 2 && st.isSolid(ptx, groundY)) groundY--;
      picked.x = ptx * TILE + 8 - picked.w / 2;
      picked.y = groundY * TILE - picked.h;
      picked.id = this.entities.nextId++;
      this.entities.add(picked, 'critters');
      return;
    }
    // 普通怪：落脚位（原版 HasTileSpawnSpace：上方两格净空）
    let spawnY = -1;
    for (let dy = -4; dy <= 8; dy++) {
      const yy = pty + dy;
      if (yy < 2 || yy > st.h - 3) continue;
      const dry = st.liquid[st.idx(ptx, yy)] <= 40 && st.liquid[st.idx(ptx, yy - 1)] <= 40;
      const clear = !st.isSolid(ptx, yy) && !st.isSolid(ptx, yy - 1) && dry;

```


---

## 🤖 Assistant · 2026-08-11T05:44:59.360Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now check viewHalfW: `Math.ceil(viewW / zoom / 2 / TILE)`. In original, spawnArea uses sWidth/16 = full screen tiles where sWidth is the fixed 1920 (or actual screen). So num = 0.7 × (sWidth/16) tiles; our rangeX = floor(viewHalfW × 1.4) = floor(ceil(sW_px/2/16) × 1.4) ≈ 0.7 × sW/16. Equivalent. Good. ClampToWorld: our areaL = max(2, px-rangeX) etc. — need to check WorldUtils.ClampToWorld semantics (probably clamps to [0, maxTilesX-1] with no margin). Our margin of 2 may differ; let me check WorldUtils.ClampToWorld. Also Utils.CenteredRectangle uses tile coordinates from player.position.ToTileCoordinates() — note this is floor(position/16) not center/16! player.position is top-left. Our pX = floor(playerX/TILE) — if Game passes p.cx (center) then ours uses center while original uses top-left position. Let me check: Game calls `this.vanillaSpawner.spawn(p.cx, p.cy, ...)`. p.cx is center presumably. Original SetSpawnFlags: `pX = (int)player.Center.X / 16;` — wait! In original SetSpawnFlags (L287): `pX = (int)player.Center.X / 16;` — center. But GetSpawnArea uses `player.position.ToTileCoordinates()` — that's the top-left! And CheckNotSpawningOnScreen uses `player.Center`. So original uses THREE different anchors:
- SetSpawnFlags pX/pY = Center tile
- GetSpawnArea spawnArea/safeArea = position (top-left) tile
- CheckNotSpawningOnScreen = Center pixel

Our findSpawnTile uses px=this.pX (center tile) for the area center. Original uses top-left tile for the area. Off by half player height/width (player is 2×3 tiles → ~1×1.5 tiles). Minor but real difference, especially vertically (1-2 tiles shift). Also `Math.abs(tx-px) < safeX` uses center, original uses safeArea centered on position tile. Same offset issue.

Let me verify CenteredRectangle and ClampToWorld.

Also verify p.cx is center in our code. And check slimeRain / etc. Not needed.

Let me check WorldUtils.ClampToWorld.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:44:59.895Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"ClampToWorld\\|CenteredRectangle\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldUtils.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Utils.cs | head",
 "description": "Find ClampToWorld implementation"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:44:59.919Z

**📎 ToolResult**

```
ugrep: warning: ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldUtils.cs: No such file or directory
929:	public static Rectangle CenteredRectangle(Vector2 center, Vector2 size)
934:	public static Rectangle CenteredRectangle(Point center, Point size)

```


---

## 🤖 Assistant · 2026-08-11T05:45:00.284Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"get cx\\|get cy\" ~/Project/GLM/SandboxWorld/game/src/entities/*.ts ~/Project/GLM/SandboxWorld/game/src/core/*.ts | head",
 "description": "Check cx/cy semantics"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:45:00.316Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/entities/Entity.ts:24:  get cx() { return this.x + this.w / 2; }
~/Project/GLM/SandboxWorld/game/src/entities/Entity.ts:25:  get cy() { return this.y + this.h / 2; }

```


---

## 🤖 Assistant · 2026-08-11T05:45:01.952Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '925,945p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Utils.cs; echo \"----\"; grep -rn \"ClampToWorld\" ~/Project/GLM/SandboxWorld/Terarria1456/ | head -3",
 "description": "Read CenteredRectangle and ClampToWorld"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:45:01.992Z

**📎 ToolResult**

```
		lineAmount = Math.Min(num + 1, maxLines);
		return array;
	}

	public static Rectangle CenteredRectangle(Vector2 center, Vector2 size)
	{
		return new Rectangle((int)(center.X - size.X / 2f), (int)(center.Y - size.Y / 2f), (int)size.X, (int)size.Y);
	}

	public static Rectangle CenteredRectangle(Point center, Point size)
	{
		return new Rectangle(center.X - size.X / 2, center.Y - size.Y / 2, size.X, size.Y);
	}

	public static Rectangle Including(this Rectangle rect, Point point)
	{
		int num = Math.Min(rect.Left, point.X);
		int num2 = Math.Max(rect.Right, point.X);
		int num3 = Math.Min(rect.Top, point.Y);
		int num4 = Math.Max(rect.Bottom, point.Y);
		return new Rectangle(num, num3, num2 - num, num4 - num3);
----
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.WorldBuilding/WorldUtils.cs:9:	public static Rectangle ClampToWorld(Rectangle tileRectangle, int fluff = 0)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.WorldBuilding/WorldUtils.cs:26:	public static Rectangle ClampToWorldBorders(Rectangle worldRect)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.States/UIWorldGenDebug.cs:1485:		tileRectangle = WorldUtils.ClampToWorld(tileRectangle, 40);

```


---

## 🤖 Assistant · 2026-08-11T05:45:03.745Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1,25p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.WorldBuilding/WorldUtils.cs",
 "description": "Read ClampToWorld"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:45:03.769Z

**📎 ToolResult**

```
using System;
using Microsoft.Xna.Framework;
using Terraria.Testing;

namespace Terraria.WorldBuilding;

public static class WorldUtils
{
	public static Rectangle ClampToWorld(Rectangle tileRectangle, int fluff = 0)
	{
		int num = Math.Max(fluff, Math.Min(tileRectangle.Left, Main.maxTilesX - fluff));
		int num2 = Math.Max(fluff, Math.Min(tileRectangle.Top, Main.maxTilesY - fluff));
		int num3 = Math.Max(fluff, Math.Min(tileRectangle.Right, Main.maxTilesX - fluff));
		int num4 = Math.Max(fluff, Math.Min(tileRectangle.Bottom, Main.maxTilesY - fluff));
		return new Rectangle(num, num2, num3 - num, num4 - num2);
	}

	public static Rectangle GetWorldPlayArea()
	{
		int num = 640;
		Point point = new Point((int)Main.leftWorld + num, (int)Main.topWorld + num);
		Point point2 = new Point((int)Main.rightWorld - num, (int)Main.bottomWorld - num);
		return new Rectangle(point.X, point.Y, point2.X - point.X, point2.Y - point.Y);
	}

```


---

## 🤖 Assistant · 2026-08-11T05:45:08.773Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
ClampToWorld with fluff=0: clamps to [0, maxTilesX]. Rectangle.Right is exclusive; `Main.rand.Next(Left, Right)` uses exclusive Right. Original: Right clamped to maxTilesX - 0 = maxTilesX → x ranges to maxTilesX-1. Ours: areaR = min(st.w-3, px+rangeX) → max st.w-3. So ours excludes the outermost 2 tiles on right/bottom (and left/top margin 2). Original allows 0..maxTilesX-1. Minor difference: ours reduces spawnable band by 2 tiles at each edge. Also note original rectangle width = num*2, Right = Left + num*2, so [cx-num, cx+num) — i.e. right side exclusive at cx+num. Ours rng.int(areaL, areaR) — check RNG.int semantics inclusive/exclusive. Let me check RNG.int.

Also CheckNotSpawningOnScreen loops all 255 players — ours single player. Fine to note briefly.

Also the original `Main.rand.Next(spawnArea.Left, spawnArea.Right)` — for tile Y original uses spawnArea.Bottom similarly.

Now check RNG.int bounds.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:45:09.224Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"int(\" ~/Project/GLM/SandboxWorld/game/src/core/rng.ts | head; echo \"----\"; sed -n '1,60p' ~/Project/GLM/SandboxWorld/game/src/core/rng.ts",
 "description": "Check RNG.int bounds semantics"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:45:09.262Z

**📎 ToolResult**

```
18:  int(min: number, max: number): number {
----
// 确定性随机数：mulberry32 + 2D hash（世界生成用）
export class RNG {
  private s: number;
  constructor(seed: number) {
    this.s = seed >>> 0;
  }
  next(): number {
    // mulberry32
    this.s = (this.s + 0x6d2b79f5) >>> 0;
    let t = this.s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  }
  range(min: number, max: number): number {
    return min + this.next() * (max - min);
  }
  int(min: number, max: number): number {
    return Math.floor(this.range(min, max + 1));
  }
  chance(p: number): boolean {
    return this.next() < p;
  }
  pick<T>(arr: T[]): T {
    return arr[Math.floor(this.next() * arr.length)];
  }
}

export function hashString(str: string): number {
  let h = 2166136261 >>> 0;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

// 2D 整数 hash → [0,1)，无状态确定性噪声
export function hash2(x: number, y: number, seed: number): number {
  let h = seed >>> 0;
  h = Math.imul(h ^ (x | 0), 0x27d4eb2d);
  h = Math.imul(h ^ (y | 0), 0x85ebca6b);
  h ^= h >>> 15;
  h = Math.imul(h, 0x2c1b3c6d);
  h ^= h >>> 12;
  return (h >>> 0) / 4294967296;
}

```


---

## 🤖 Assistant · 2026-08-11T05:45:17.888Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Our `rng.int(min,max)` is INCLUSIVE on both ends (floor(range(min, max+1))). Original `Main.rand.Next(min, max)` is EXCLUSIVE of max. In findSpawnTile: `rng.int(areaL, areaR)` — ours includes areaR, which is min(st.w-3, px+rangeX); original excludes px+rangeX. Off-by-one, and at right edge ours can pick st.w-3 (valid tile) where original excluded it; original allowed up to st.w-1 (since Right clamp = maxTilesX exclusive → max index maxTilesX-1). Net: right edge one tile. Very minor. But in `setFlagsForChosenTile` scans `rng.int(20,30)` for marble: original `Main.rand.Next(20,31)` = 20..30 inclusive — ours `rng.int(20,30)` = 20..30 inclusive. Matches (they adapted). For spider `rng.int(5,14)` vs original Next(5,15)=5..14. OK.

But `rng.next() < 1/3` vs original `Main.rand.Next(3)==0` — same 1/3. OK.

Marble step: original `num2 = Next(1,4)` = 1..3, ours `rng.int(1,3)`=1..3 ✓. Inner `num3 = Next(1,4)` per row — ours uses fixed stepJ = 1+(next*3|0) = 1..3 fixed, original re-rolls per row. Minor non-1:1 but low impact. Also second scan: original num2=Next(3,7)=3..6, ours rng.int(3,6)=3..6 ✓; inner Next(3,7) re-rolled per row, ours fixed 3+(next*4|0)=3..6 ✓ fixed. Also original clamps num asymmetrically (x: maxTilesX - spawnTileX - 1, y: maxTilesY - spawnTileY - 1; second loop: -2). Ours clamps the box with max(0,...) and min(w-1,...) — different at edges. Minor.

Note: original's box loop bounds `i <= spawnTileX + num` inclusive; ours `x1 = min(w-1, cx0+r)` and `i <= x1` ✓ inclusive.

One real difference: original marble/granite scan `if (spawnTileX - num < 0) num = spawnTileX;` etc. — adjusts radius so box stays in world, ours clamps box. Similar effect.

Now the important stuff for Zone metrics: SceneMetrics.cs L613-615 formulas. Let me check the actual SceneMetrics code for ZoneCorrupt/ZoneCrimson/ZoneSnow/ZoneJungle/ZoneHallow/ZoneGlowshroom thresholds and window size (169×123, count>=300?). Let me grep.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:45:18.636Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"zoneScanSize\\|_tileCounts\\|EvilTileCount\\|BloodTileCount\\|HolyTileCount\\|JungleTileCount\\|SnowTileCount\\|MushroomTileCount\\|>= 300\\|>= 40\\|>= 60\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/SceneMetrics.cs | head -40",
 "description": "Check SceneMetrics zone thresholds"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:45:18.675Z

**📎 ToolResult**

```
142:	private readonly int[] _tileCounts = new int[TileID.Count];
180:	public int EvilTileCount { get; set; }
182:	public int HolyTileCount { get; set; }
192:	public int MushroomTileCount { get; private set; }
194:	public int SnowTileCount { get; private set; }
206:	public int BloodTileCount { get; private set; }
208:	public int JungleTileCount { get; private set; }
254:	public bool EnoughTilesForJungle => JungleTileCount >= JungleTileThreshold;
256:	public bool EnoughTilesForHallow => HolyTileCount >= HallowTileThreshold;
258:	public bool EnoughTilesForSnow => SnowTileCount >= SnowTileThreshold;
260:	public bool EnoughTilesForGlowingMushroom => MushroomTileCount >= MushroomTileThreshold;
264:	public bool EnoughTilesForCorruption => EvilTileCount >= CorruptionTileThreshold;
266:	public bool EnoughTilesForCrimson => BloodTileCount >= CrimsonTileThreshold;
375:				_tileCounts[tile.type]++;
593:		if (_tileCounts[27] > 0)
597:		if (_tileCounts[567] > 0)
602:		HoneyBlockCount = _tileCounts[229];
603:		HolyTileCount = _tileCounts[109] + _tileCounts[492] + _tileCounts[110] + _tileCounts[113] + _tileCounts[117] + _tileCounts[116] + _tileCounts[164] + _tileCounts[403] + _tileCounts[402];
604:		SnowTileCount = _tileCounts[147] + _tileCounts[148] + _tileCounts[161] + _tileCounts[162] + _tileCounts[164] + _tileCounts[163] + _tileCounts[200];
607:			JungleTileCount = _tileCounts[60] + _tileCounts[61] + _tileCounts[62] + _tileCounts[74] + _tileCounts[225];
608:			EvilTileCount = _tileCounts[23] + _tileCounts[661] + _tileCounts[24] + _tileCounts[25] + _tileCounts[32] + _tileCounts[112] + _tileCounts[163] + _tileCounts[400] + _tileCounts[398] + _tileCounts[27] * num + _tileCounts[474];
609:			BloodTileCount = _tileCounts[199] + _tileCounts[662] + _tileCounts[201] + _tileCounts[203] + _tileCounts[200] + _tileCounts[401] + _tileCounts[399] + _tileCounts[234] + _tileCounts[352] + _tileCounts[27] * num + _tileCounts[195];
613:			JungleTileCount = _tileCounts[60] + _tileCounts[61] + _tileCounts[62] + _tileCounts[74] + _tileCounts[226] + _tileCounts[225];
614:			EvilTileCount = _tileCounts[23] + _tileCounts[661] + _tileCounts[24] + _tileCounts[25] + _tileCounts[32] + _tileCounts[112] + _tileCounts[163] + _tileCounts[400] + _tileCounts[398] + _tileCounts[27] * num;
615:			BloodTileCount = _tileCounts[199] + _tileCounts[662] + _tileCounts[201] + _tileCounts[203] + _tileCounts[200] + _tileCounts[401] + _tileCounts[399] + _tileCounts[234] + _tileCounts[352] + _tileCounts[27] * num;
617:		MushroomTileCount = _tileCounts[70] + _tileCounts[71] + _tileCounts[72] + _tileCounts[528];
618:		MeteorTileCount = _tileCounts[37];
619:		DungeonTileCount = _tileCounts[41] + _tileCounts[43] + _tileCounts[44] + _tileCounts[481] + _tileCounts[482] + _tileCounts[483];
620:		SandTileCount = _tileCounts[53] + _tileCounts[112] + _tileCounts[116] + _tileCounts[234] + _tileCounts[397] + _tileCounts[398] + _tileCounts[402] + _tileCounts[399] + _tileCounts[396] + _tileCounts[400] + _tileCounts[403] + _tileCounts[401];
621:		PartyMonolithCount = _tileCounts[455];
622:		GraveyardTileCount = _tileCounts[85];
623:		GraveyardTileCount -= _tileCounts[27] / 2;
624:		if (_tileCounts[27] > 0)
636:		if (HolyTileCount < 0)
638:			HolyTileCount = 0;
640:		if (EvilTileCount < 0)
642:			EvilTileCount = 0;
644:		if (BloodTileCount < 0)
646:			BloodTileCount = 0;
648:		int holyTileCount = HolyTileCount;

```


---

## 🤖 Assistant · 2026-08-11T05:45:27.399Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '242,270p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/SceneMetrics.cs; echo \"----\"; sed -n '585,600p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/SceneMetrics.cs; echo \"----\"; grep -n \"zoneScanSize\\|ScanTiles\\|new Point(\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/SceneMetrics.cs | head",
 "description": "Read thresholds and scan window"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:45:27.431Z

**📎 ToolResult**

```
	public bool RadioThingMonolith { get; private set; }

	public bool HasCatBast { get; private set; }

	public int GraveyardTileCount { get; private set; }

	public int DesertSandTileCount { get; private set; }

	public int OceanSandTileCount { get; private set; }

	public bool EnoughTilesForShimmer => ShimmerTileCount >= ShimmerTileThreshold;

	public bool EnoughTilesForJungle => JungleTileCount >= JungleTileThreshold;

	public bool EnoughTilesForHallow => HolyTileCount >= HallowTileThreshold;

	public bool EnoughTilesForSnow => SnowTileCount >= SnowTileThreshold;

	public bool EnoughTilesForGlowingMushroom => MushroomTileCount >= MushroomTileThreshold;

	public bool EnoughTilesForDesert => DesertSandTileCount >= DesertTileThreshold;

	public bool EnoughTilesForCorruption => EvilTileCount >= CorruptionTileThreshold;

	public bool EnoughTilesForCrimson => BloodTileCount >= CrimsonTileThreshold;

	public bool EnoughTilesForMeteor => MeteorTileCount >= MeteorTileThreshold;

	public bool EnoughTilesForDungeon => DungeonTileCount >= DungeonTileThreshold;
----

	private void AggregateTileCounts()
	{
		int num = -10;
		if (Main.infectedSeed)
		{
			num *= 3;
		}
		if (_tileCounts[27] > 0)
		{
			HasSunflower = true;
		}
		if (_tileCounts[567] > 0)
		{
			HasGardenGnome = true;
		}
----
12:	private static readonly Point AssumedConstantScreenSize = new Point(1920, 1200);
16:	public static readonly Point ZoneScanSize = new Point(AssumedConstantScreenSize.X / 16 + ZoneScanPadding * 2 - 1, AssumedConstantScreenSize.Y / 16 + ZoneScanPadding * 2 - 1);
335:			ScanTiles();
354:	private void ScanTiles()
448:				UpdateOreFinder(new Point(i, j), tile);
716:		Point pt = new Point(TileCenter.X, TileCenter.Y);
724:				Tile tileSafely3 = Framing.GetTileSafely(new Point(pt.X, pt.Y - 1));
893:			Point point = new Point(pos.X - TileCenter.X, pos.Y - TileCenter.Y);

```


---

## 🤖 Assistant · 2026-08-11T05:45:31.452Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"TileThreshold\\|ZoneScanPadding\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/SceneMetrics.cs | head -20; echo \"----\"; sed -n '354,380p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/SceneMetrics.cs",
 "description": "Read thresholds and ScanTiles loop"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:45:31.492Z

**📎 ToolResult**

```
14:	private static readonly int ZoneScanPadding = 25;
16:	public static readonly Point ZoneScanSize = new Point(AssumedConstantScreenSize.X / 16 + ZoneScanPadding * 2 - 1, AssumedConstantScreenSize.Y / 16 + ZoneScanPadding * 2 - 1);
24:	public static int ShimmerTileThreshold = 300;
26:	public static int CorruptionTileThreshold = 300;
30:	public static int CrimsonTileThreshold = 300;
34:	public static int HallowTileThreshold = 125;
38:	public static int JungleTileThreshold = 140;
52:	public static int MushroomTileThreshold = 100;
56:	public static int MeteorTileThreshold = 75;
58:	public static int DungeonTileThreshold = 250;
64:	public static int GraveyardTileThreshold = 28;
154:	public static int SnowTileThreshold
166:	public static int DesertTileThreshold
252:	public bool EnoughTilesForShimmer => ShimmerTileCount >= ShimmerTileThreshold;
254:	public bool EnoughTilesForJungle => JungleTileCount >= JungleTileThreshold;
256:	public bool EnoughTilesForHallow => HolyTileCount >= HallowTileThreshold;
258:	public bool EnoughTilesForSnow => SnowTileCount >= SnowTileThreshold;
260:	public bool EnoughTilesForGlowingMushroom => MushroomTileCount >= MushroomTileThreshold;
262:	public bool EnoughTilesForDesert => DesertSandTileCount >= DesertTileThreshold;
264:	public bool EnoughTilesForCorruption => EvilTileCount >= CorruptionTileThreshold;
----
	private void ScanTiles()
	{
		Rectangle tileRectangle = Utils.CenteredRectangle(TileCenter, ZoneScanSize);
		tileRectangle = WorldUtils.ClampToWorld(tileRectangle);
		for (int i = tileRectangle.Left; i < tileRectangle.Right; i++)
		{
			for (int j = tileRectangle.Top; j < tileRectangle.Bottom; j++)
			{
				Tile tile = Main.tile[i, j];
				if (tile == null)
				{
					continue;
				}
				if (!tile.active())
				{
					if (tile.liquid > 0)
					{
						_liquidCounts[tile.liquidType()]++;
					}
					continue;
				}
				_tileCounts[tile.type]++;
				if (TileID.Sets.isDesertBiomeSand[tile.type] && WorldGen.oceanDepths(i, j))
				{
					OceanSandTileCount++;
				}
				if (TileID.Sets.Campfires[tile.type] && tile.frameY < 36)

```


---

## 🤖 Assistant · 2026-08-11T05:45:43.920Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
ZoneScanSize = (1920/16 + 50 - 1, 1200/16 + 50 - 1) = (120+49, 75+49) = (169, 124). Hmm: 1200/16 = 75, +50-1 = 124. Our comment says 123 and our code uses cy±61 (y1-y0 = 122 or 123 tiles). Let's compute: our y0 = max(2, cy-61), y1 = min(h-3, cy+61) → up to 123 rows (inclusive both ends). Original height 124 → y from cy-62 to cy+61 inclusive (Rectangle Top = TileCenter.Y - 124/2 = cy-62, Bottom = Top+124 = cy+62 exclusive → rows cy-62..cy+61 = 124 rows). Ours cy-61..cy+61 = 123 rows. Off by one row. X: original 169 wide → cx-84..cx+84 (since 169/2=84.5 → int division: CenteredRectangle(Point) does `center.X - size.X/2` = cx-84 (integer division 169/2=84), width 169 → Right = cx-84+169 = cx+85 exclusive → x in [cx-84, cx+84] = 169 tiles. Ours cx-84..cx+84 ✓ 169. Good for X; Y off by one (123 vs 124). Very minor.

Now check SceneMetrics EvilTileCount: `_tileCounts[23]+[661]+[24]+[25]+[32]+[112]+[163]+[400]+[398] + [27]*num` where num=-10 normally (sunflower -10 each; -30 infected seed). Our countTiles subtracts 10 per sunflower ✓ (matches num=-10). Our EVIL_LOOKUP includes: CORRUPT_GRASS(23), EBONSTONE(25), CORRUPT_PLANT(24), CORRUPT_THORN(32), EBONSAND(112), CORRUPT_ICE(163), CORRUPT_HARDSAND(398). Missing 661 (corrupt jungle grass) and 400 — commented as engine-absent → 0. OK, matches comment.

BLOOD_LOOKUP: 199,203,201,200,234,352,399 ✓ matches original 199+662+201+203+200+401+399+234+352.

But note: original counts ALL tiles of those types in the window regardless of active/inactive? `_tileCounts[tile.type]++` for active tiles only (if !tile.active() → skip). Ours counts type regardless (actuated tiles would count in ours, not original). Minor.

However — MAJOR: our ZoneCorrupt/ZoneCrimson use countTiles (player window) ✓ matches SceneMetrics. But ZoneSnow/ZoneHallow/ZoneJungle/ZoneGlowshroom in our setFlagsForChosenTile are based on spawnTileType (the single ground tile!), NOT the SceneMetrics window counts. That's a real divergence from the original: original takes these from player.ZoneSnow etc. (SceneMetrics window counts with thresholds: Hallow 125, Jungle 140, Snow (dynamic threshold), Mushroom 100). Our snow check `t===SNOW||ICE||SNOW_BRICK` only checks the single floor tile — so standing on dirt in a snow biome with 300+ snow tiles in window would NOT set ZoneSnow in ours, whereas original would. Real bug. The comment at L300 claims alignment but only corrupt/crimson actually use window counts.

Let me check SnowTileThreshold (dynamic) to be accurate. sed 154-170.

Also original ZoneSnow tile list: 147+148+161+162+164+163+200.

Also getSpawnRate uses this.ZoneSnow at L413 — ours only fires if ground tile is snow. Actually getSpawnRate is called before findSpawnTile, using flags from the PREVIOUS spawn (as commented "Zone flags 为上次生成残留，同原版" — hmm original: GetSpawnRate is called after SetSpawnFlags which reads player.Zone* fresh each attempt. So original uses the player's current zone flags; ours uses stale last-spawn ground-tile flags. That's a divergence worth reporting.)

Let me read SceneMetrics L154-170 for SnowTileThreshold.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:45:44.176Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '150,175p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/SceneMetrics.cs",
 "description": "Read SnowTileThreshold"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:45:44.216Z

**📎 ToolResult**

```
	public Point TileCenter { get; private set; }

	public Point BestOrePosition { get; private set; }

	public static int SnowTileThreshold
	{
		get
		{
			if (WorldGen.Skyblock.lowTiles)
			{
				return SnowTileSkyblockThreshold;
			}
			return SnowTileNormalThreshold;
		}
	}

	public static int DesertTileThreshold
	{
		get
		{
			if (WorldGen.Skyblock.lowTiles)
			{
				return DesertTileSkyblockThreshold;
			}
			return DesertTileNormalThreshold;
		}

```


---

## 🤖 Assistant · 2026-08-11T05:45:46.144Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"SnowTileNormalThreshold\\|DesertTileNormalThreshold\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/SceneMetrics.cs | head",
 "description": "Snow threshold value"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:45:46.176Z

**📎 ToolResult**

```
42:	public static int SnowTileNormalThreshold = 1500;
48:	public static int DesertTileNormalThreshold = 1500;
162:			return SnowTileNormalThreshold;
174:			return DesertTileNormalThreshold;

```


---

## 🤖 Assistant · 2026-08-11T05:46:16.584Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
SnowTileThreshold = 1500 — with window 169×124 ≈ 20956 tiles, that's dense snow. Anyway.

Now check the getSpawnRate diffs more carefully against original order. Original order of GetSpawnRate:

1. default 600/5
2. hardMode: rate×0.9, max+1 — ours: not present (hardMode flag exists but unused in getSpawnRate). Ours has `this.hardMode` field but doesn't apply the hardMode modifier. Real divergence (hardMode is in world.flags).
3. depth bands ✓ (underworld max×2; rock+sHeight ×0.4/1.9; worldSurface+sHeight ×0.5/1.7; night ×0.6/1.3 + bloodmoon ×0.3/1.8) ✓ — ours matches (non-remix). Note original eclipse (dayTime && eclipse) ×0.2/1.9 missing; pumpkin/snow moon missing — noted as unimplemented in comment. Also missing: ZoneSnow-cloudAlpha (we have it), drunkWorld wall 86, dungeon ×0.3/1.8 (ours has but at END, after clamp — see below), sandstorm, undergroundDesert (×0.2/×3), jungle (×0.4/1.5 townNPCs=0...), corrupt/crimson ×0.65/1.3, meteor ×0.4/1.1, lihzhard temple, hallow-deep, wof, tresspassingDualDungeon.

Big one: original `if (inDualDungeon || ZoneDungeon) rate×0.3, max×1.8` appears in the MAIN chain (L502-506) BEFORE the nearby-slots adjustments and BEFORE clamp; and then L696 `if (ZoneDungeon && !downedBoss3) spawnRate = 10;` after clamp. Our implementation applies the ZoneDungeon ×0.3/×1.8 AFTER clamp (max×1.8 computed after max capped at 15 → can yield up to 27). Original: maxSpawns capped at 15 AFTER all ×1.8 multiplications... wait original order: dungeon ×1.8 happens at L505; then nearby-slots rate adjustments; then clamp maxSpawns ≤ 15 at L663. So in original, dungeon max = (5×1.8 adjusted) then capped 15 → 9→ fine. In ours, max first capped at 15 then ×1.8 → 5×1.8=9 anyway when base... could exceed 15 if base already raised: e.g. underworld max=10 → ours: capped 15, ×1.8 = 18; original: 10×1.8=18 then capped 15. So ours can exceed original cap. Real (minor) bug. Also ours applies rain-snow AFTER dungeon & clamp — original applies ZoneSnow+cloudAlpha at L494 before. Order matters slightly.

Also ours ZoneSnow modifier requires rainCloudAlpha>0 whereas original applies always (multiplier with cloudAlpha; cloudAlpha=0 → max×1, rate×1). Same effect when 0. Fine.

Also ours missing `spawnRate < defaultSpawnRate*0.1` uses 60 const ✓ equivalent (600×0.1=60) ✓.

Also original pumpkin/snow moon → maxSpawns = defaultMaxSpawns*(2+0.3n), rate 20 — missing (noted). Also invaders early return: ours returns rate 20 max 5*(2+0.3) = 11 for single player — matches L683-ish for invaders (yes original: `if (invaders) { maxSpawns = defaultMaxSpawns*(2.0+0.3*numberOfActivePlayers); spawnRate = 20; }`). ✓. But original invaders block also skips... fine.

Important: our invaders early-return happens BEFORE underworld/night modifications — original's invaders assignment is at the END of GetSpawnRate (after everything), so it overrides — same result. ✓.

Also missing: `if (Main.wofNPCIndex >= 0 ...)` etc. Not important.

Also note original `if (player.nearbyActiveNPCs >= (float)maxSpawns) return false;` in TrySpawnAnNPC — Game does `if (nearby >= maxSpawns) return;` ✓.

Also original SpawnNPC loop: for each player, if TrySpawnAnNPC true break. Single player fine.

Now, `Main.rand.Next(spawnRate) != 0` — Game uses Math.random()*spawnRate !== 0 ✓.

Now check additional flag-chain items: original SetSpawnFlagsForChosenTile sets underGround = spawnTileY <= rockLayer; ours groundLevel<y<rockLevel. Also original surfaceSpawn = spawnTileY <= worldSurface ✓ ours. deeperThanRockLayer = spawnTileY >= rockLayer ✓ ours.

waterTile: original checks tile[y-1].liquid>0 && tile[y-2].liquid>0 && liquidType()==0 (water). Ours: liquid[above1]>0 && liquid[above2]>0 && liquidType[above1]===1 (our water=1). ✓ byte semantics match (0-255 Uint8Array). Good — so point 3 of the task: no bug. But note original waterTile doesn't check shimmer/honey (PostCheck handles those); ours also has no honey/shimmer rejection — original PostCheck rejects shimmer/honey spawns. We don't have shimmer/honey systems probably; minor note.

Also PostCheck original rejects tileType 477/492 (sand piles / ???) 10% — ours missing; minor.

Original PostCheck is checked ONCE per attempt after FindSpawnTile; on failure aborts the frame (no retry). Ours uses it as retry filter within the 50 attempts. Real divergence.

Also the dungeon PostCheck uses spawnWallType = wall of the tile ABOVE the ground tile (from GetProperGround). Ours uses wall at the ground tile itself. Let me think about which is right: In dungeon, PostCheck requires spawnWallType != 0 → the wall above the spawn position must exist. If we check wall at the solid floor tile (tx,ty): dungeon interior floor tiles — walls are usually not placed behind solid tiles? Actually in Terraria, walls exist in the air spaces of dungeon; the brick floor tiles themselves have wall 0 typically? Hmm. WorldGen places dungeon walls in the air corridors. The tile at spawnTileY is solid brick (no wall). So original checks wall at (x, y-1) which is the air tile above — in dungeon interior that has dungeon wall (non-zero) → passes. Ours checks wall at (x,y) = solid brick tile → wall likely 0 → we'd REJECT nearly all dungeon spawns and retry until attempts exhausted → no dungeon spawns at all! That's a potentially serious bug. But wait — does our TILE wall array include walls behind solid tiles? Depends on our world gen. Let me quickly grep how dungeon walls are placed in our world gen to determine. Actually I should just report it as a likely bug: original uses wall above ground tile; ours uses wall at ground tile.

Let me verify by checking our dungeon generation: does it set wall on air tiles only? Quick grep for wall assignment in dungeon pass.

Also check `isOcean`: original `Main.tileSand[spawnTileType]` (sand family incl. ebonsand/crimsand/pearlsand/hardened?) and also `spawnTileType == 53 && WorldGen.oceanDepths(...)`. Ours: `spawnTileType === T.SAND && spawnTileY < rockLevel` — missing the `tileSand` family (ebonsand etc. would fail isOcean) and oceanDepths check; also ours requires spawnTileType sand which original also effectively requires for first clause. Note tileSand includes 53,112,116,234,397(?),398,399,404... Using only SAND means corrupt/crimson oceans won't be isOcean. Minor divergence. But user said don't report ocean x-threshold change; the tileSand family issue is separate and reportable.

Now, the `findSpawnTile` retry `continue` for PostCheck — also note that original, after PostCheck fails, returns false → no NPC that frame, and `skyMob`/flags untouched. Ours: continue → tries other points. Real bug (documented above).

Another: original FindSpawnTile initial-point check also skips when the point tile is solid — but importantly the original loop condition for skyMob also has `!spawnFriendly` and `invaders` guards, which ours omits (we have no spawnFriendly) — spawnFriendly is a town-NPC mechanic (not implemented). Note briefly.

Original second skyMob branch: hardMode && y < worldSurface*0.45 && rand.Next(10)==0 → skyMob. Ours missing this hardmode branch entirely (known change? The known note says skyMob changed to "露天高空" semantics deliberately; the hardmode 0.45 branch missing might be part of that). I'll mention briefly as part of skyMob (excluded by instruction). Skip.

CheckNotSpawningOnScreen: original iterates all 255 players and rejects if spawn rect intersects ANY active player's extended screen (excluding dual-dungeon-inside players). Ours only checks the local player. In multiplayer host-authoritative mode, other players' screens not respected → enemies can spawn on their screens. Real divergence worth reporting.

Also note: original `CheckNotSpawningOnScreen` uses player.Center for the rect center; ours uses p.cx,p.cy passed (center) ✓.

One more: In original TrySpawnAnNPC order, CheckNotSpawningOnScreen is called BEFORE GetProperGround/PostCheck/SetFlags. Ours: findSpawnTile (which includes safeArea check + HasTileSpawnSpace + PostCheck + SetFlags) then CheckNotSpawningOnScreen after. Since our findSpawnTile already applied the safeArea filter, the second check is redundant but consistent. Order difference: original's SetSpawnFlagsForChosenTile happens after CheckNotSpawningOnScreen; if the check fails, flags aren't set (matters only for stale flags next frame). Ours sets flags then check fails → flags set but unused. Negligible.

Also original HasTileSpawnSpace: `WorldGen.InWorld(rectangle)` — let me check the InWorld(Rectangle) overload — might require 1-tile margin. Let me grep quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:46:17.378Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"public static bool InWorld\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs | head; echo \"----\"; sed -n \"$(grep -n 'InWorld(Rectangle' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs | head -1 | cut -d: -f1),+25p\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs",
 "description": "Read WorldGen.InWorld rectangle overload"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:46:22.867Z

**📎 ToolResult**

```
9630:	public static bool InWorld(Point p, int fluff = 0)
9635:	public static bool InWorld(int x, int y, int fluff = 0)
9644:	public static bool InWorld(Rectangle rect, int fluff = 0)
----
	public static bool InWorld(Rectangle rect, int fluff = 0)
	{
		int x = rect.X;
		int y = rect.Y;
		int num = rect.X + rect.Width;
		int num2 = rect.Y + rect.Height;
		if (x < fluff || num >= Main.maxTilesX - fluff || y < fluff || num2 >= Main.maxTilesY - fluff)
		{
			return false;
		}
		return true;
	}

	public static void gemCave(int x, int y)
	{
		countTiles(x, y);
		for (int i = 0; i < 6; i++)
		{
			gem[i] = false;
		}
		gem[genRand.Next(6)] = true;
		for (int j = 0; j < 6; j++)
		{
			if (genRand.Next(6) == 0)
			{
				gem[j] = true;

```


---

## 🤖 Assistant · 2026-08-11T05:46:27.343Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
InWorld(rect) with fluff 0: requires rect.X >= 0, rect.Right < maxTilesX (strictly less), i.e. Right <= maxTilesX-1. Our hasTileSpawnSpace checks x<0||y<0||x>=w||y>=h → equivalent to fluff=0 semantics? Original requires num < maxTilesX, where num = X+Width = tx-1+2 = tx+1 < maxTilesX → tx < maxTilesX-1, i.e. tx <= maxTilesX-2. Ours allows x up to w-1. So original rejects spawns in the outermost tile column/row; ours allows. Off-by-one edge difference. Minor.

Also CanSpawnInTile: `nactive() && tileSolid` — ours isSolid uses TILE_DEFS solid; consistent with nactive+tileSolid if TILE_DEFS.solid mirrors tileSolid. Actuated handled ✓. anyLava: liquid>0 && liquidType==lava; ours `st.liquid[i] > 0 && st.liquidType[i] === 2` ✓ (our 2=lava).

Now let me double-check the dungeon wall question in our world gen: do solid tiles get walls? Check dungeon pass / wall placement. Let me grep for dungeon wall ids 41/43/44 in gen, or how wall is assigned.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:46:29.013Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"DUNGEON_BLUE\\|v_41\\|dungeon\" ~/Project/GLM/SandboxWorld/game/src/world/gen/*.ts -l 2>/dev/null | head; echo \"----\"; ls ~/Project/GLM/SandboxWorld/game/src/world/gen/ 2>/dev/null || find ~/Project/GLM/SandboxWorld/game/src -name \"*ungeon*\"",
 "description": "Locate dungeon generation"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:46:29.055Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts
----
SeedEasterEggs.ts
vanilla
WorldGen.ts

```


---

## 🤖 Assistant · 2026-08-11T05:46:31.875Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"wall\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts 2>/dev/null | head -20; ls ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/ | head -30",
 "description": "Inspect dungeon pass wall placement"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:46:31.904Z

**📎 ToolResult**

```
40:const HANGING = TILE_BY_KEY['v_240_wall_hangings_3x3']!;
52:  brick: number; wall: number;
64:  constructor(brick: number, wall: number, x: number, y: number) {
65:    this.brick = brick; this.wall = wall;
70:    const wl = st.wall[st.idx(x, y)];
71:    return wl === this.wall || (wl >= 94 && wl <= 99);
100:        if (st.flags[i] || st.liquid[i] > 0 || st.wall[i] > 0) break;
127:  const wallId = brick === BLUE ? 7 : brick === GREEN ? 8 : 9;
137:  const dc = new DungeonCtx(brick, wallId, x0, y0);
224:            st.flags[i] = 0; st.wall[i] = dc.wall;
328:        if (edge) st.wall[st.idx(x, y)] = dc.wall;
346:        st.wall[i] = dc.wall;
383:        if (edge) st.wall[i] = dc.wall;
385:          st.flags[i] = 0; st.wall[i] = dc.wall;
443:          if (!st.inBounds(probeX, yy) || st.wall[st.idx(probeX, yy)] !== 0) { open = false; break; }
468:        if (st.inBounds(x, y)) st.wall[st.idx(x, y)] = dc.wall;
478:        st.flags[i] = 0; st.wall[i] = dc.wall;
493: * 0.6 框清墙 → **0.5 框 active=false+wall=0(开放门厅,老头 NPC 位)** →
513:      st.wall[ti] = 0;
514:      if (paintWall) st.wall[ti] = dc.wall;
BeachPass.ts
BuriedChestsPass.ts
CaveHousePass.ts
CavesPass.ts
CleanupPass.ts
CorruptionPass.ts
DesertPass.ts
DirtToMudPass.ts
DungeonPass.ts
GenState.ts
GrassPass.ts
HalfBrickPass.ts
HellforgesPass.ts
HellFortPass.ts
HiveSpiderPass.ts
IceBiomePass.ts
IslandHousePass.ts
JunglePass.ts
JungleShrinePass.ts
LakesPass.ts
MarbleGranitePass.ts
MountCavesPass.ts
MushroomPass.ts
OceanCavesPass.ts
ShiniesPass.ts
Spread.ts
StatuesPass.ts
StructuresPass.ts
SwordShrinePass.ts
TemplePass.ts

```


---

## 🤖 Assistant · 2026-08-11T05:46:38.937Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
In DungeonPass, walls are painted on interior/air tiles (st.flags[i] = 0 → tile cleared + wall set). Solid floor tiles may not get the wall. So our PostCheck dungeon wall test `st.wall[idx(tx,ty)]===0` on the solid floor tile likely rejects most dungeon spawns → retry loop → few/no dungeon spawns. Worth reporting as a likely real bug (needs verification of whether floor tiles get walls). Line 328: `if (edge) st.wall[...] = dc.wall;` — edge tiles (walls of rooms). Floors probably not. I'll report it as "likely blocks dungeon spawns".

Actually wait: also the ground type check. FindSpawnTile in dungeon: the found solid tile must be a dungeon brick (41/43/44) — floors are dungeon brick ✓.

But there's another subtlety: our spawnTileType for the dungeon variant branch in spawnAnNPC uses walls 94-99 — fine.

Also `GetProperGroundSpawnTileTypeAndWallType` — our header comment L7-8 says "我们的等价 = 落脚格下方第一个实心格的 tile type" but the code actually uses the found solid tile (tx,ty) itself. Since findSpawnTile's downward scan lands on the solid tile, the spawn position ty IS the solid tile. So our groundType = the solid tile type = original's spawnTileType in the common case ✓. Difference remains: (1) wall type (above tile vs ground tile), (2) UsesADifferentTileTypeForNPCSpawning remap, (3) invalid ground (platform/solidTop) down-scan of 30.

What is UsesADifferentTileTypeForNPCSpawning set for? Probably for certain tiles like sandstone/... let me check quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:46:39.712Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"UsesADifferentTileTypeForNPCSpawning\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ID/TileID.Sets.cs | head; echo \"----\"; grep -rn \"UsesADifferentTileTypeForNPCSpawning.Add\\|UsesADifferentTileTypeForNPCSpawning\\[\" ~/Project/GLM/SandboxWorld/Terarria1456/ | head",
 "description": "Find tiles using different spawn type"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:46:39.765Z

**📎 ToolResult**

```
ugrep: warning: ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ID/TileID.Sets.cs: No such file or directory
----
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:5793:			if (TileID.Sets.UsesADifferentTileTypeForNPCSpawning[spawnTileType] && WorldGen.InWorld(x, y + 1) && WorldGen.SolidTile3(x, y + 1))

```


---

## 🤖 Assistant · 2026-08-11T05:46:41.230Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rln \"UsesADifferentTileTypeForNPCSpawning\" ~/Project/GLM/SandboxWorld/Terarria1456/ | head",
 "description": "Find Sets registration file"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:46:41.269Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs

```


---

## 🤖 Assistant · 2026-08-11T05:46:44.481Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"UsesADifferentTileTypeForNPCSpawning\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs",
 "description": "Read registration entries"
}
```


---

## 👤 User(sidechain) · 2026-08-11T05:46:44.503Z

**📎 ToolResult**

```
351:		public static bool[] UsesADifferentTileTypeForNPCSpawning = Factory.CreateBoolSet(false, 421, 422);

```


---

## 🤖 Assistant · 2026-08-11T05:46:58.427Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Tiles 421/422 (sandstone brick / ...). Our engine probably lacks them → negligible.

Now finalize the report. Let me compile the diff list, prioritized, ≤50 lines. Also verify a couple of remaining specifics:

- Attempt cap 50 ✓ matches (point 6 answer: aligned).
- getSpawnRate hardMode branch missing: original L389-390 `if (Main.hardMode) rate×0.9, max+1`. Ours doesn't (hardMode exists as field). Real bug.
- Order issue: original dungeon ×0.3/×1.8 occurs mid-chain before clamp; ours after clamp → max can exceed 15 cap. Also original rate×0.3 then further multiplied by nearby-slots modifiers and the ×0.6-0.9 bands... wait no — those bands come AFTER dungeon in original (L583+), so both orderings have dungeon before the bands... ours has dungeon after water candle & clamp, and rain-snow after dungeon. Since rain-snow requires ZoneSnow+cloudAlpha>0 and dungeon rarely overlap, minor. The clamp-order issue is the notable one.
- ZoneSnow/ZoneHallow/ZoneJungle/ZoneGlowshroom single-tile vs window-count: real bug (comment claims alignment).
- Also getSpawnRate reads Zone flags from previous spawn (stale) — original SetSpawnFlags reads fresh player SceneMetrics each attempt. Real.
- spawnTileY == rockLevel boundary for underGround (original `<=` includes rockLayer, ours `<`). Minor off-by-one.
- Underground-desert / spider checks: original conditions include `!invaders` (both), ours doesn't — minor; also original requires `spawnTileX-num5 >= 0 && spawnTileX+num5 < maxTilesX` else skips entirely (no player fallback), ours clamps. Minor.
- getSpawnRate missing branches: eclipse, pumpkin/snow moon, jungle/corrupt/crimson/meteor/desert-sandstorm/underground-desert zone modifiers, getGoodWorld, water candle high-altitude check ✓ (have). Report as grouped omission, some are intentional per comment. The zone-based ones (jungle ×0.4/1.5 etc.) are significant for jungle spawn feel — worth reporting as one item.
- SpawnArea anchor: original CenteredRectangle uses player.position tile (top-left), ours center tile → ~1 tile horizontal / ~1.5 tile vertical shift. Minor but 1:1 relevant.
- areaL/areaR margins 2 vs original 0 fluff → 2-tile narrower band; also rng.int inclusive vs Next exclusive.
- CheckNotSpawningOnScreen single player vs all players.
- PostCheck-as-retry vs abort-frame.
- PostCheck wall check on ground tile vs above tile.
- Missing PostCheck shimmer/honey + 477/492 rejection (minor).
- waterTile: aligned (0-255 byte, >0 same as original liquid>0; liquidType 1=water ↔ original 0=water).
- HasTileSpawnSpace aligned (2×3, nactive+solid, anyLava); edge: ours allows outermost tile, original rejects (Right < maxTilesX).
- SceneMetrics window: X 169 ✓, Y 123 vs 124 (off-by-one); threshold evil 300 ✓, blood 300 ✓; but only used for corrupt/crimson.

Also point 2 (downward scan limit): aligned — original limit is spawnArea.Bottom (min with maxTilesY), not world bottom. Our areaB matches ✓. Good, answer: aligned.

Point 1: rangeX/rangeY ×1.4 of viewHalf ≈ 0.7×full screen ✓ aligned; safeX ×1.04 ✓. Only anchor (top-left vs center) + edge margins differ.

Let me write the final list ≤50 lines with file:line / original anchor / original semantics / our status / bug verdict.
```

</details>


---

## 🤖 Assistant · 2026-08-11T05:47:22.693Z · glm-x-preview-260804

```
## 差异清单（VanillaSpawner.ts vs Terarria1456/Terraria/NPC.cs `NPC.Spawner` + SceneMetrics）

原版锚点均指 NPC.cs（1.4.5.6 的 `Spawner` 内嵌类），如无说明。

**A. 选点链（重点 1/2/6）**
1. `VanillaSpawner.ts:432` / `GetSpawnArea` L841-877：选点面积公式已对齐（`0.7×全屏格 = 1.4×半屏`、safe `0.52 = 1.04×半屏`），**但原版面积中心 = `player.position.ToTileCoordinates()`（左上角格）**，`CheckNotSpawningOnScreen` 才用 `Center`；我们统一用 `pX/pY`（`spawn()` L847 由 `p.cx/cy` 传入 = 中心）。横向偏 ~1 格、纵向偏 ~1.5 格 → 区域整体偏移。**轻微，非关键**。
2. `VanillaSpawner.ts:432-433`：原版 `ClampToWorld` fluff=0（允许 0..maxTiles-1），我们留 2 格边距（`max(2,..)` / `min(w-3,..)`）→ 边缘 2 格不刷。且 `rng.int` 双闭 vs 原版 `Next(L,R)` 右开。**轻微**。
3. 向下找落脚面（重点 2）：`VanillaSpawner.ts:450` vs L900-906 —— **对齐**。原版扫描上限同样是 `spawnArea.Bottom`（`j < maxTilesY && j < Bottom`），非世界底；我们 `areaB` 一致。
4. 尝试次数（重点 6）：`L434` 50 次 = 原版 L883 `for i<50`。**对齐**。
5. `VanillaSpawner.ts:463-464`（PostCheck 用作重试）vs `TrySpawnAnNPC` L227：原版 `PostCheckChosenSpawnTile` 失败即 `return false` **整帧放弃、不换点**；我们 `continue` 继续抽点。语义不同（我们更容易在别处成功刷怪）。**真 bug（行为级）**。
6. `VanillaSpawner.ts:464` 地牢墙校验：原版 `spawnWallType = Main.tile[x, y-1].wall`（`GetProperGroundSpawnTileTypeAndWallType` L5790-5792，**落脚实心格上方一格的墙**）；我们用 `st.wall[idx(tx,ty)]`（落脚实心格自身）。DungeonPass 只给空腔/边缘刷墙、地板砖通常 `wall=0` → 我们几乎全部拒点，50 次耗尽 → **地牢可能完全不刷怪，真 bug（高危，建议实测）**。
7. `VanillaSpawner.ts:461`：缺原版 `UsesADifferentTileTypeForNPCSpawning`(421/422) 重映射与 `IsValidSpawningGroundTile` 失败时向下扫 30 格取真实地面类型（L5797-5812）。421/422 引擎未注册、平台族我们 `isSolid` 为 false 会直接扫过 → 影响极小。**非 bug**。

**B. HasTileSpawnSpace / CheckNotSpawningOnScreen**
8. `VanillaSpawner.ts:473-485` vs L5306-5337：2×3 窗口、`nactive&&tileSolid`、`anyLava()` 全对齐；边界原版 `InWorld(rect)` 要求 `Right < maxTilesX`（最外圈拒），我们允许到 `w-1`。**对齐（边缘 off-by-one，忽略级）**。
9. `VanillaSpawner.ts:490-497` vs L5344-5366：原版**遍历全部 255 名玩家**，与任一活跃玩家扩展屏相交即拒；我们只查本地玩家。联机房主权威下会刷到访客屏幕内。**真 bug（联机场景）**。

**C. waterTile / flag 链（重点 3）**
10. `VanillaSpawner.ts:248` vs L957：**对齐**。原版 `tile.liquid > 0`（byte 0-255，无 255/量阈值）；`TileStore.ts:13` `liquid: Uint8Array` 同为 0-255 byte 语义，`>0` 等价；`liquidType===1(我们水)` ↔ `liquidType()==0(原版水)`。**非 bug**。
11. `VanillaSpawner.ts:290`：`underGround = groundLevel<y<rockLevel`；原版 L1011 `underGround = spawnTileY <= rockLayer`（含 ==rockLayer 及全部地表上层，实际由 surfaceSpawn 分支先行截胡）。仅 `y == rockLevel` 一格归属差（落洞穴池）。**轻微 off-by-one**。
12. `VanillaSpawner.ts:274,312`：原版地下沙漠(L1078)与蜘蛛巢(L1024)均带 `!invaders` 前置，我们未判 `invaders`；且原版 x 越界时整个扫描跳过（连玩家格回退也不查），我们 clamp 后照扫。**轻微**。
13. `VanillaSpawner.ts:268-269`：大理石/花岗岩扫描原版内层步长每行重掷 `Next(1,4)`/`Next(3,7)`，我们行外固定。采样密度略异。**非关键**。
14. `VanillaSpawner.ts:298`：isOcean 用 `T.SAND` 单类型；原版 L1104 是 `Main.tileSand[spawnTileType]`（含 112/116/234/397/398/399/404 族）+ `type==53 && oceanDepths` 兜底 → 黑檀沙/猩红沙/硬化沙海岸不判海洋。x 阈值缩放本身按约定不报。**真 bug（小）**。
15. 缺原版 PostCheck L932-948 的 shimmer/honey 拒绝与 477/492 的 1/10 拒绝（`VanillaSpawner.ts` 全文件无对应）。引擎无 shimmer/honey 系统则仅 477/492 缺失。**轻微**。

**D. Zone 判定（重点 4）**
16. `VanillaSpawner.ts:300-307` 注释声称对齐 SceneMetrics，**实际只有 ZoneCorrupt/ZoneCrimson 走窗口计数**（L303-304 ✓ 阈值 300、EVIL/BLOOD 表与 SceneMetrics.cs:614-615 一致、向日葵 −10 ✓）；**ZoneSnow/ZoneHallow/ZoneJungle/ZoneGlowshroom 只看落脚单格 tile**，原版是玩家窗口计数 ≥ 阈值（Snow 1500、Hallow 125、Jungle 140、Mushroom 100，SceneMetrics.cs:34/38/42/52）。站在雪原泥土/丛林泥土上不触发 Zone → 雪原/丛林怪池与刷怪率修正失效。**真 bug（显著）**。
17. `VanillaSpawner.ts:335-349 countTiles`：X 窗 169 ✓（169/2=84）；Y 用 `cy±61`=123 行，原版 `ZoneScanSize.Y = 75+49 = 124`（`cy-62..cy+61`）。**off-by-one 一行，忽略级**。

**E. getSpawnRate（重点 5）**
18. `VanillaSpawner.ts:357-418` 缺原版 L389-390 `Main.hardMode → rate×0.9 / max+1`（`this.hardMode` 字段已存在却未用）。**真 bug**。
19. `VanillaSpawner.ts:407-411`：地牢 ×0.3/×1.8 放在 clamp **之后**；原版 L504-505 在链中段、L663 clamp `max≤15` 在其后 → 我们可产出 max>15（如地狱 10×1.8=18 不封顶）。**真 bug（小）**。另原版 L696 `rate=10`（未杀骷髅王）确实在 clamp 后，我们处理 ✓。
20. `VanillaSpawner.ts:392`：ZoneCorrupt/Crimson/ZoneSnow 取**上一次成功生成的残留 flag**；原版每次 `SetSpawnFlags`(L300) 从玩家 SceneMetrics 现取 → 刷怪率修正滞后一拍。**真 bug（小）**。
21. 整段缺原版 zone 修正：Jungle L524-543、Corrupt/Crimson L544-547、Meteor L548-551、Sandstorm L507-511、UndergroundDesert L512-516、Hallow-deep L555、Lihzhard L518、WoF L562、getGoodWorld L668、eclipse L460-463、pumpkin/snowMoon L455-458 与 L674-678（注释已声明血月外多数未实现，但 Jungle/Corrupt/Crimson 的 ×0.4-0.65 对丛林/腐化体感影响明显）。**缺口（部分有意）**。
22. `VanillaSpawner.ts:365`：UnderworldLayer 用 `h-200` 近似（注释已声明）；原版地狱深判定为 `player.position.Y > UnderworldLayer*16`，position(左上) vs 我们 `p.cy`(中心)，深界差 ~24px。**轻微**。

**结论**：高危 2 项（#6 地牢墙校验位置、#16 Zone 单格判定）、行为级 3 项（#5 PostCheck 重试化、#9 单玩家屏检、#18 hardMode 缺失）、其余为边缘/off-by-one 或已知缺口。选点扫描范围、向下扫面上限、尝试次数 50、waterTile byte 语义均已对齐。
```
