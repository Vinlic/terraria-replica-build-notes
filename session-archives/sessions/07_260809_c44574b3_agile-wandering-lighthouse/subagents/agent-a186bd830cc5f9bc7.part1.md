# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-17T04:32:27.373Z

```
你是泰拉瑞亚 1.4.5.6 复刻项目（TypeScript+Canvas）的对账审计员。只读审计，不修改任何文件。

我们的代码：~/Project/GLM/SandboxWorld/game/src/（NPC 主体 entities/Enemy.ts 或 NPC 专属文件、AI 家族在 entities/ai/ 或类似、城镇行为 Game.ts/VanillaSpawner）
原版唯一真理：~/Project/GLM/SandboxWorld/Terarria1456/Terrarid/*.cs 修正路径：~/Project/GLM/SandboxWorld/Terarria1456/Terraria/*.cs（TownNPC 相关：NPC.cs AI_007 TownNPC 段、Main.cs UpdateTime/NPC update、TownNPCProfile、NPC.cs :9000-11000 城镇行为区）

任务：审计**城镇 NPC（其他角色）日常生活行为**是否对齐原版。已知已实现：AI_007 四态（闲逛/对话/战斗/回家）、自卫攻击+持械视觉、表情气泡（Extra_48）、开门/关门、夜间回家、住房系统、快乐度+关系表、派对旗帜、图鉴。

逐项核对以下行为（原版 1.4.4+ 城镇 NPC 生活行为）在反编译源码中的语义与我们是否一致：
1. **坐椅子**：原版城镇 NPC 会坐在椅子上（NPC.cs SittingChat/SittingFor讨论? 搜索 npc.ai 中 town NPC sitting：1.4.0 加的"sitting on chairs"——搜索 NPC.cs 中 "chair" / ai[3] 坐姿、NPCSpriteSheet? 找到具体行为：什么条件坐下、坐多久、坐下时帧（NPC 坐姿帧））
2. **睡觉**：1.4.4 城镇 NPC 会在夜里睡在床上吗（搜 NPC.cs sleep 相关）——如原版没有就标"原版无此行为"
3. 闲逛行为参数：走停节奏（timer 掷骰区间、概率常量）、转身频率、跳跃越障、避水/避崖（不走出平台边缘的检查）
4. 对话触发：靠近玩家主动说话的冷却/概率、名字替换、不同 NPC 特殊对话条件
5. 传送回家：夜间瞬移回家的条件（玩家远离+时间）原版语义
6. 派对/事件行为：派对期间跳舞/购物折扣
7. 被玩家推动/挤开行为
8. 死亡表现：城镇 NPC 死亡掉落/重生计时（respawnTimer）
9. 防御姿态（受击护头?）与无敌帧
10. 全 NPC 通用的受击闪白/击退/浸液（蜂蜜/岩浆）行为

输出：偏离清单按严重度排序，每条附原版行号证据+我们现状（file:line，找不到实现就写"未实现"）+修复规格。已对齐项列 ✓。最终回复用中文。
```

---

## 📎 Attachment · skill_listing · 2026-08-17T04:32:27.376Z

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

## 🤖 Assistant · 2026-08-17T04:32:32.504Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by understanding the task. I need to audit town NPC daily life behaviors in our TypeScript Terraria 1.4.5.6 recreation against the decompiled vanilla source code. This is a read-only audit.

Let me start by exploring both codebases:
1. Our code: ~/Project/GLM/SandboxWorld/game/src/
2. Vanilla: ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs and Main.cs

Let me first look at the vanilla source for town NPC behaviors, and our implementation.

Key items to audit:
1. Sitting on chairs
2. Sleeping in beds
3. Wandering parameters (walk/stop rhythm, turn frequency, jumping over obstacles, avoiding water/cliffs)
4. Dialogue triggers (cooldown/probability, name replacement, special conditions)
5. Teleport home at night
6. Party/event behaviors (dancing, shopping discounts)
7. Being pushed by players
8. Death: drops/respawn timer
9. Defense posture + invincibility frames
10. Hit flash/knockback/liquid (honey/lava) behaviors common to all NPCs

Let me start by exploring the file structure.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:32:33.393Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/src/ && ls ~/Project/GLM/SandboxWorld/game/src/entities/ 2>/dev/null | head -50",
 "description": "List our source directories"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:32:33.430Z

**📎 ToolResult**

```
assets
core
data
debug
dev
drops
entities
fx
i18n
items
lighting
main.ts
mainFlow.ts
net
physics
player
render
save
stats
ui
vui
wld
workers
world
Arrow.ts
Bobber.ts
BookProj.ts
bossAI_dd2.ts
bossAI_deerclops.ts
bossAI_duke_moonlord.ts
bossAI_golem.ts
bossAI_lategame.ts
bossAI_lunar_misc.ts
bossAI_martian.ts
bossAI_moon_events.ts
bossAI_queenbee_plantera.ts
bossAI_wof.ts
bossAI.ts
Celeb2.ts
ChainsawProj.ts
CoinPortalProj.ts
Critter.ts
Dart.ts
DebrisProj.ts
Enemy.ts
Entity.ts
FallingBlock.ts
FallingStar.ts
fighterFamilies.ts
FirstFractal.ts
GolfBall.ts
GorePiece.ts
GrappleProj.ts
HealProj.ts
ItemDrop.ts
LeashedCritter.ts
LunarNebula.ts
MagicProj.ts
mechQueen.ts
MeteorChunk.ts
Minecart.ts
MinionProj.ts
MissileProj.ts
Mounts.ts
npcLiquid.ts
PetFollower.ts
Player.ts
Portal.ts
PortalGunBolt.ts
PrismProj.ts
projStatus.ts
projTargets.ts
RainbowProj.ts
SkyDragonFury.ts

```


---

## 🤖 Assistant · 2026-08-17T04:32:34.077Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ | head -60; echo ---; wc -l ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "description": "List vanilla decompiled source files"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:32:34.118Z

**📎 ToolResult**

```
AdvancedPopupRequest.cs
Animation.cs
BitsByte.cs
Chest.cs
Cloud.cs
Collision.cs
CombatText.cs
Control.cs
DelegateMethods.cs
Dust.cs
Entity.cs
EquipmentLoadout.cs
FocusHelper.cs
FrameSkipTest.cs
Framing.cs
GetItemSettings.cs
Gore.cs
HitTile.cs
IEntitySourceTarget.cs
IngameOptions.cs
InitData.cs
Item.cs
ItemSerializationContext.cs
Lang.cs
Lighting.cs
Liquid.cs
LiquidBuffer.cs
MacLaunch.cs
Main.cs
MapRenderer.cs
MessageBuffer.cs
Minecart.cs
Mount.cs
NetMessage.cs
Netplay.cs
NewProjectileModifier.cs
NewProjectileModifiers.cs
NPC.cs
NPCSpawningFlagsForDualDungeons.cs
NPCSpawnParams.cs
PartyHatColor.cs
Player.cs
PlayerSpawnContext.cs
PopupText.cs
PopupTextContext.cs
Program.cs
Projectile.cs
Rain.cs
Recipe.cs
RecipeGroup.cs
Ref.cs
RemoteClient.cs
RemoteServer.cs
ResolutionChangeEvent.cs
SceneMetrics.cs
SceneMetricsScanSettings.cs
SceneState.cs
ScriptSandbox.cs
ShoppingSettings.cs
Sign.cs
---
   96369 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs
   66229 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs
  162598 total

```


---

## 🤖 Assistant · 2026-08-17T04:32:36.049Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me look at the town NPC AI section in vanilla NPC.cs first. Let me search for AI_007 town NPC section, sitting, chair, sleep, party, etc.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:32:37.008Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"aiStyle == 7\\b\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head; echo ---; grep -n -i \"chair\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -30",
 "description": "Find AI_007 and chair references in vanilla NPC.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:32:37.053Z

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
---

```


---

## 🤖 Assistant · 2026-08-17T04:32:37.748Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE \"sitting|Sitting\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -40",
 "description": "Find sitting references in vanilla NPC.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:32:37.776Z

**📎 ToolResult**

```
53264:	private void AI_007_TryForcingSitting(int homeFloorX, int homeFloorY)
54078:							AI_007_TryForcingSitting(floorX, floorY);
54701:					Main.sittingManager.AddNPC(whoAmI, coords);
55790:						if (Main.player[num120].active && Main.player[num120].sitting.isSitting && Main.player[num120].Center.ToTileCoordinates() == point)
56081:				AI_007_TryForcingSitting(homeFloorX, homeFloorY);

```


---

## 🤖 Assistant · 2026-08-17T04:32:39.890Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting — no "chair" text in NPC.cs but there's a sitting manager. Let me look at the AI_007 town NPC section. The town NPC AI section is around lines 53000-56500 apparently. Let me read the AI_007 region.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:32:40.703Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"private void AI_007\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; grep -n \"void AI_007_TownNPC\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Find AI_007 method boundaries"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:32:40.739Z

**📎 ToolResult**

```
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

## 🤖 Assistant · 2026-08-17T04:32:41.776Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE \"sleep|Sleeping\" ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria/NPC.cs | head -30; echo ---; grep -n -iE \"sleep\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head -20",
 "description": "Find sleep references in vanilla sources"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:32:41.819Z

**📎 ToolResult**

```
ugrep: warning: ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria/NPC.cs: No such file or directory
---
95:		public static int SleepingPlayersCount;
2200:	public static AnchoredEntitiesCollection sleepingManager;
5237:	public void NeverSleep()
5245:	public void YouCanSleepNow()
5255:		NeverSleep();
5769:			YouCanSleepNow();
5830:						Thread.Sleep(num10 - 1);
5834:							Thread.Sleep(10);
5839:			Thread.Sleep(0);
5846:		YouCanSleepNow();
6280:		bool flag = CurrentFrameFlags.SleepingPlayersCount == CurrentFrameFlags.ActivePlayersCount && CurrentFrameFlags.SleepingPlayersCount > 0;
6421:		sleepingManager = new AnchoredEntitiesCollection();
16854:			ThreadUtilities.HighPrecisionSleep(DebugOptions.UpdateWaitInMs);
16903:			base.InactiveSleepTime = (ThrottleWhenInactive ? TimeSpan.FromMilliseconds(20.0) : TimeSpan.Zero);
16970:					base.InactiveSleepTime = TimeSpan.Zero;
17679:		sleepingManager.ClearPlayerAnchors();
17692:					if (player[i].sleeping.FullyFallenAsleep)
17707:		CurrentFrameFlags.SleepingPlayersCount = num2;
17740:		sleepingManager.ClearNPCAnchors();
61426:			ThreadUtilities.HighPrecisionSleep(DebugOptions.DrawWaitInMs);

```


---

## 🤖 Assistant · 2026-08-17T04:32:47.492Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The second grep in the first command failed because of a shell quoting issue (the path got mangled?). Actually it says "No such file or directory" — probably because `head -30; echo ---; grep` — the path is fine... Actually the issue: "ugrep: warning: ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs: No such file or directory" — weird. Maybe the filename has some issue. Let me retry.

So in vanilla: town NPCs don't sleep in beds — they have "sitting" via sittingManager (chairs/beds?) and sleepingManager is for players. Let me check the sitting manager usage in AI_007.

Let me read the AI_007_TownEntities method from line 53366 to ~56063. That's about 2700 lines. Let me read it in chunks, focusing on key behaviors:
- State machine ai[0]: 0=wander, 1=?, 2=?, 3/4=talk, 5=sitting?, 16/17=shimmer?, 25=?

Let me read carefully.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:32:48.095Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '53195,53420p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_007 helper methods (resting spot, sitting)"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:32:48.139Z

**📎 ToolResult**

```
	private void AI_007_FindGoodRestingSpot(int myTileX, int myTileY, out int floorX, out int floorY)
	{
		floorX = homeTileX;
		floorY = homeTileY;
		if (floorX == -1 || floorY == -1)
		{
			return;
		}
		while (!SolidOrSlopedTileOrPlatform(Main.tile[floorX, floorY]) && floorY < Main.maxTilesY - 20)
		{
			floorY++;
		}
		if (Main.dayTime || (ai[0] == 5f && Math.Abs(myTileX - floorX) < 7 && Math.Abs(myTileY - floorY) < 7))
		{
			return;
		}
		Point point = new Point(floorX, floorY);
		Point point2 = new Point(-1, -1);
		int num = -1;
		if (type == 638 || type == 656 || NPCID.Sets.IsTownSlime[type] || ai[0] == 5f)
		{
			return;
		}
		int num2 = 7;
		int num3 = 6;
		int num4 = 2;
		int num5 = 1;
		int num6 = 2;
		for (int i = point.X - num2; i <= point.X + num2; i += num5)
		{
			for (int num7 = point.Y + num4; num7 >= point.Y - num3; num7 -= num6)
			{
				Tile tile = Main.tile[i, num7];
				if (tile != null && tile.active() && TileID.Sets.CanBeSatOnForNPCs[tile.type] && (tile.frameY % 40 != 0 || num7 + 1 <= point.Y + num4))
				{
					int num8 = Math.Abs(i - point.X) + Math.Abs(num7 - point.Y);
					if (num == -1 || num8 < num)
					{
						num = num8;
						point2.X = i;
						point2.Y = num7;
					}
				}
			}
		}
		if (num == -1)
		{
			return;
		}
		Tile tile2 = Main.tile[point2.X, point2.Y];
		if (tile2.type == 497 || tile2.type == 15)
		{
			if (tile2.frameY % 40 != 0)
			{
				point2.Y--;
			}
			point2.Y += 2;
		}
		for (int j = 0; j < Main.maxNPCs; j++)
		{
			if (Main.npc[j].active && Main.npc[j].aiStyle == 7 && Main.npc[j].townNPC && Main.npc[j].ai[0] == 5f && (Main.npc[j].Bottom + Vector2.UnitY * -2f).ToTileCoordinates() == point2)
			{
				return;
			}
		}
		floorX = point2.X;
		floorY = point2.Y;
	}

	private void AI_007_TryForcingSitting(int homeFloorX, int homeFloorY)
	{
		if (!WorldGen.InWorld(homeFloorX, homeFloorY))
		{
			return;
		}
		Tile tile = Main.tile[homeFloorX, homeFloorY - 1];
		bool flag = type != 638 && type != 656 && !NPCID.Sets.IsTownSlime[type] && ai[0] != 5f;
		if (flag)
		{
			flag &= tile != null && tile.active() && (tile.type == 15 || tile.type == 497);
		}
		if (flag)
		{
			flag &= tile.type != 15 || tile.frameY < 1080 || tile.frameY > 1098;
		}
		if (flag)
		{
			Point point = (base.Bottom + Vector2.UnitY * -2f).ToTileCoordinates();
			for (int i = 0; i < Main.maxNPCs; i++)
			{
				if (Main.npc[i].active && Main.npc[i].aiStyle == 7 && Main.npc[i].townNPC && Main.npc[i].ai[0] == 5f && (Main.npc[i].Bottom + Vector2.UnitY * -2f).ToTileCoordinates() == point)
				{
					flag = false;
					break;
				}
			}
		}
		if (flag)
		{
			ai[0] = 5f;
			ai[1] = 900 + Main.rand.Next(10800);
			direction = ((tile.frameX != 0) ? 1 : (-1));
			base.Bottom = new Vector2(homeFloorX * 16 + 8 + 2 * direction, homeFloorY * 16);
			velocity = Vector2.Zero;
			localAI[3] = 0f;
			netUpdate = true;
		}
	}

	public void UpdateHomeTileState(bool homeless, int x, int y)
	{
		bool num = x != homeTileX || y != homeTileY || this.homeless != homeless;
		oldHomeless = (this.homeless = homeless);
		oldHomeTileX = (homeTileX = x);
		oldHomeTileY = (homeTileY = y);
		if (num && Main.netMode != 1)
		{
			byte householdStatus = WorldGen.TownManager.GetHouseholdStatus(this);
			NetMessage.SendData(60, -1, -1, null, whoAmI, homeTileX, homeTileY, (int)householdStatus);
		}
	}

	public Color GetMagicAuraColor()
	{
		Color result = NPCID.Sets.MagicAuraColor[type];
		if (type == 160 && townNpcVariationIndex == 1)
		{
			result = new Color(result.B, result.G, result.R, result.A);
		}
		if (type == 20 && townNpcVariationIndex == 1)
		{
			result = new Color(90, 20, 210, result.A);
		}
		if (type == 663 && townNpcVariationIndex == 1)
		{
			result = new Color(255, 0, 77, result.A);
		}
		return result;
	}

	private void AI_007_TownEntities_UpdateSavedStates()
	{
		switch (type)
		{
		case 588:
			savedGolfer = true;
			break;
		case 441:
			savedTaxCollector = true;
			break;
		case 107:
			savedGoblin = true;
			break;
		case 108:
			savedWizard = true;
			break;
		case 124:
			savedMech = true;
			break;
		case 353:
			savedStylist = true;
			break;
		case 369:
			savedAngler = true;
			break;
		case 550:
			savedBartender = true;
			break;
		}
	}

	private void AI_007_TownEntities()
	{
		ShimmeredTownNPCs[type] = IsShimmerVariant;
		if (type == 441 && GivenName == "Andrew")
		{
			defDefense = 200;
		}
		if (Main.onlyShimmerOceanWorlds && type == 680 && GivenName == "Slimefors")
		{
			life = lifeMax;
			defDefense = 99999;
		}
		int num = 300;
		if (type == 638 || type == 656 || NPCID.Sets.IsTownSlime[type])
		{
			num = 0;
		}
		bool flag = Main.raining;
		if (!Main.dayTime)
		{
			flag = true;
		}
		if (Main.eclipse)
		{
			flag = true;
		}
		if (Main.slimeRain)
		{
			flag = true;
		}
		if (Main.IsItStorming && (double)(position.Y / 16f) < Main.worldSurface)
		{
			flag = true;
		}
		float num2 = 1f;
		if (Main.masterMode)
		{
			defense = (dryadWard ? (defDefense + 20) : defDefense);
		}
		else if (Main.expertMode)
		{
			defense = (dryadWard ? (defDefense + 15) : defDefense);
		}
		else
		{
			defense = (dryadWard ? (defDefense + 10) : defDefense);
		}
		float num3 = 2f;
		bool flag2 = false;
		if (isLikeATownNPC)
		{
			bool flag3 = life == lifeMax;
			lifeMax = defLifeMax;
			if (combatBookWasUsed)
			{

```


---

## 🤖 Assistant · 2026-08-17T04:32:52.831Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This is the beginning of AI_007_TownEntities. This is a huge method (53366 to ~55982, about 2600 lines). Let me read it in chunks. I'll read the whole thing in ~400-line chunks to understand all the behaviors. Let me be systematic.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:32:53.377Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '53420,53800p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_007_TownEntities lines 53420-53800"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:32:53.406Z

**📎 ToolResult**

```
			{
				lifeMax += 250;
				num3 *= 0.8f;
				num2 += 0.25f;
				defense += 8;
			}
			if (combatBookVolumeTwoWasUsed)
			{
				lifeMax += 250;
				num3 *= 0.8f;
				num2 += 0.25f;
				defense += 8;
			}
			if (lifeMax > defLifeMax && flag3)
			{
				life = lifeMax;
			}
			if (downedSlimeKing)
			{
				num3 *= 0.985f;
				num2 += 0.05f;
				defense += 2;
			}
			if (downedBoss1)
			{
				num3 *= 0.985f;
				num2 += 0.05f;
				defense += 2;
			}
			if (downedDeerclops)
			{
				num3 *= 0.985f;
				num2 += 0.1f;
				defense += 3;
			}
			if (downedBoss2)
			{
				num3 *= 0.985f;
				num2 += 0.1f;
				defense += 3;
			}
			if (downedBoss3)
			{
				num3 *= 0.985f;
				num2 += 0.1f;
				defense += 3;
			}
			if (downedQueenBee)
			{
				num3 *= 0.985f;
				num2 += 0.1f;
				defense += 3;
			}
			if (Main.hardMode)
			{
				num3 *= 0.985f;
				num2 += 0.4f;
				defense += 12;
			}
			if (downedQueenSlime)
			{
				num3 *= 0.985f;
				num2 += 0.15f;
				defense += 6;
			}
			if (downedMechBoss1)
			{
				num3 *= 0.985f;
				num2 += 0.15f;
				defense += 6;
			}
			if (downedMechBoss2)
			{
				num3 *= 0.985f;
				num2 += 0.15f;
				defense += 6;
			}
			if (downedMechBoss3)
			{
				num3 *= 0.985f;
				num2 += 0.15f;
				defense += 6;
			}
			if (downedPlantBoss)
			{
				num3 *= 0.985f;
				num2 += 0.15f;
				defense += 8;
			}
			if (downedEmpressOfLight)
			{
				num3 *= 0.985f;
				num2 += 0.15f;
				defense += 8;
			}
			if (downedFishron)
			{
				num3 *= 0.985f;
				num2 += 0.15f;
				defense += 8;
			}
			if (downedGolemBoss)
			{
				num3 *= 0.985f;
				num2 += 0.15f;
				defense += 8;
			}
			if (downedAncientCultist)
			{
				num3 *= 0.985f;
				num2 += 0.15f;
				defense += 20;
			}
			if (Main.infectedSeed && type == 20)
			{
				flag2 = true;
				life = lifeMax;
				defDefense = 99999;
				immortal = true;
			}
			if (Main.netMode != 1 && WorldGen.Skyblock.lowTiles)
			{
				if (num3 > 1f)
				{
					num3 = (num3 + 1f) / 2f;
				}
				num2 += 0.5f;
			}
			if (type == 209)
			{
				num3 /= 3f;
			}
			if (tipsy)
			{
				defense = (int)((double)defense * 1.1);
				num2 *= 1.1f;
				num3 *= 0.9f;
			}
		}
		if (type == 142 && Main.netMode != 1 && !Main.xMas)
		{
			StrikeNPCNoInteraction(9999, 0f, 0);
			if (Main.netMode == 2)
			{
				NetMessage.SendData(28, -1, -1, null, whoAmI, 9999f);
			}
		}
		if ((type == 148 || type == 149) && localAI[0] == 0f)
		{
			localAI[0] = Main.rand.Next(1, 5);
		}
		if (type == 124)
		{
			int num4 = lazyNPCOwnedProjectileSearchArray[whoAmI];
			bool flag4 = false;
			if (Main.projectile.IndexInRange(num4))
			{
				Projectile projectile = Main.projectile[num4];
				if (projectile.active && projectile.type == 582 && projectile.ai[1] == (float)whoAmI)
				{
					flag4 = true;
				}
			}
			localAI[0] = flag4.ToInt();
		}
		if ((type == 362 || type == 364 || type == 602 || type == 608) && Main.netMode != 1 && (velocity.Y > 4f || velocity.Y < -4f || wet))
		{
			Transform(type + 1);
			return;
		}
		AI_007_TownEntities_UpdateSavedStates();
		dontTakeDamage = false;
		if (ai[0] == 25f)
		{
			dontTakeDamage = true;
			if (ai[1] == 0f)
			{
				velocity.X = 0f;
			}
			shimmerWet = false;
			wet = false;
			lavaWet = false;
			honeyWet = false;
			if (ai[1] == 0f && Main.netMode == 1)
			{
				return;
			}
			if (ai[1] == 0f && ai[2] < 1f)
			{
				AI_007_TownEntities_Shimmer_TeleportToLandingSpot();
			}
			if (ai[2] > 0f)
			{
				ai[2] -= 1f;
				if (ai[2] <= 0f)
				{
					ai[1] = 1f;
				}
				return;
			}
			ai[1] += 1f;
			if (ai[1] >= 30f)
			{
				if (!Collision.WetCollision(position, width, height))
				{
					shimmerTransparency = MathHelper.Clamp(shimmerTransparency - 1f / 60f, 0f, 1f);
				}
				else
				{
					ai[1] = 30f;
				}
				velocity = new Vector2(0f, -4f * shimmerTransparency);
			}
			Rectangle hitbox = base.Hitbox;
			hitbox.Y += 20;
			hitbox.Height -= 20;
			float num5 = Main.rand.NextFloatDirection();
			Lighting.AddLight(base.Center, Main.hslToRgb((float)Main.timeForVisualEffects / 360f % 1f, 0.6f, 0.65f).ToVector3() * Utils.Remap(ai[1], 30f, 90f, 0f, 0.7f));
			if (Main.rand.NextFloat() > Utils.Remap(ai[1], 30f, 60f, 1f, 0.5f))
			{
				Dust.NewDustPerfect(Main.rand.NextVector2FromRectangle(hitbox) + Main.rand.NextVector2Circular(8f, 0f) + new Vector2(0f, 4f), 309, new Vector2(0f, -2f).RotatedBy(num5 * (MathF.PI * 2f) * 0.11f), 0, default(Color), 1.7f - Math.Abs(num5) * 1.3f);
			}
			if (ai[1] > 60f && Main.rand.Next(15) == 0)
			{
				for (int i = 0; i < 3; i++)
				{
					Vector2 vector = Main.rand.NextVector2FromRectangle(base.Hitbox);
					ParticleOrchestrator.RequestParticleSpawn(clientOnly: true, ParticleOrchestraType.ShimmerBlock, new ParticleOrchestraSettings
					{
						PositionInWorld = vector,
						MovementVector = DirectionTo(vector).RotatedBy(MathF.PI * 9f / 20f * (float)(Main.rand.Next(2) * 2 - 1)) * Main.rand.NextFloat()
					});
				}
			}
			TargetClosest();
			NPCAimedTarget targetData = GetTargetData();
			if (ai[1] >= 75f && shimmerTransparency <= 0f && Main.netMode != 1)
			{
				ai[0] = 0f;
				ai[1] = 0f;
				ai[2] = 0f;
				ai[3] = 0f;
				Math.Sign(targetData.Center.X - base.Center.X);
				velocity = new Vector2(0f, -4f);
				localAI[0] = 0f;
				localAI[1] = 0f;
				localAI[2] = 0f;
				localAI[3] = 0f;
				netUpdate = true;
				townNpcVariationIndex = ((townNpcVariationIndex != 1) ? 1 : 0);
				NetMessage.SendData(56, -1, -1, null, whoAmI);
				Teleport(position, 12);
				ParticleOrchestrator.BroadcastParticleSpawn(ParticleOrchestraType.ShimmerTownNPC, new ParticleOrchestraSettings
				{
					PositionInWorld = base.Center
				});
				if (townNpcVariationIndex == 1)
				{
					AchievementsHelper.NotifyProgressionEvent(43);
				}
			}
			return;
		}
		if (type >= 0 && type < NPCID.Count && NPCID.Sets.TownCritter[type] && target == 255)
		{
			TargetClosest();
			if (position.X < Main.player[target].position.X)
			{
				direction = 1;
				spriteDirection = direction;
			}
			if (position.X > Main.player[target].position.X)
			{
				direction = -1;
				spriteDirection = direction;
			}
			if (homeTileX == -1)
			{
				UpdateHomeTileState(homeless, (int)((position.X + (float)(width / 2)) / 16f), homeTileY);
			}
		}
		else if (homeTileX == -1 && homeTileY == -1 && velocity.Y == 0f && !shimmering)
		{
			UpdateHomeTileState(homeless, (int)base.Center.X / 16, (int)(position.Y + (float)height + 4f) / 16);
		}
		bool flag5 = false;
		int num6 = (int)(position.X + (float)(width / 2)) / 16;
		int num7 = (int)(position.Y + (float)height + 1f) / 16;
		AI_007_FindGoodRestingSpot(num6, num7, out var floorX, out var floorY);
		if (type == 441)
		{
			taxCollector = true;
		}
		directionY = -1;
		if (direction == 0)
		{
			direction = 1;
		}
		bool num8 = ai[0] == 24f;
		int num9 = 0;
		if (!num8)
		{
			for (int j = 0; j < 255; j++)
			{
				if (!Main.player[j].active || Main.player[j].talkNPC != whoAmI)
				{
					continue;
				}
				flag5 = true;
				if (ai[0] != 10f && ai[0] != 12f && ai[0] != 14f && ai[0] != 15f)
				{
					if (ai[0] != 0f)
					{
						netUpdate = true;
					}
					ai[0] = 0f;
					ai[1] = 300f;
					localAI[3] = 100f;
					num9 = ((!(Main.player[j].position.X + (float)(Main.player[j].width / 2) < position.X + (float)(width / 2))) ? 1 : (-1));
				}
			}
		}
		if (ai[3] == 1f)
		{
			life = -1;
			HitEffect();
			active = false;
			netUpdate = true;
			if (type == 37 || type == 54)
			{
				SoundEngine.PlaySound(15, (int)position.X, (int)position.Y, 0);
			}
			return;
		}
		if (type == 37 && Main.netMode != 1)
		{
			UpdateHomeTileState(homeless: false, Main.dungeonX, Main.dungeonY);
			if (downedBoss3)
			{
				ai[3] = 1f;
				netUpdate = true;
			}
		}
		if (type == 368)
		{
			homeless = true;
			if (!Main.dayTime)
			{
				if (!shimmering)
				{
					UpdateHomeTileState(homeless, (int)(base.Center.X / 16f), (int)(position.Y + (float)height + 2f) / 16);
				}
				if (!flag5 && ai[0] == 0f)
				{
					ai[0] = 1f;
					ai[1] = 200f;
				}
				flag = false;
			}
		}
		if (type == 369 && homeless && wet)
		{
			if (base.Center.X / 16f < 380f || base.Center.X / 16f > (float)(Main.maxTilesX - 380))
			{
				UpdateHomeTileState(homeless, Main.spawnTileX, Main.spawnTileY);
				ai[0] = 1f;
				ai[1] = 200f;
			}
			if (position.X / 16f < 300f)
			{
				direction = 1;
			}
			else if (position.X / 16f > (float)(Main.maxTilesX - 300))
			{
				direction = -1;
			}
		}
		if (NPCID.Sets.CritterThatCanTurnOnPlayers[type])
		{
			if (Main.netMode != 1)
			{

```


---

## 🤖 Assistant · 2026-08-17T04:32:55.678Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This is a very long method. Let me continue reading. I need to see the whole thing. Let me read the next chunks.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:32:56.209Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '53800,54200p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_007_TownEntities lines 53800-54200"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:32:56.247Z

**📎 ToolResult**

```
			{
				int num10 = Player.FindClosest(position, width, height);
				if (Collision.CanHit(this, Main.player[num10]) && (Main.player[num10].RollOnlyBadLuckExtreme(3000) == 0 || Main.player[num10].IsThisCenx()))
				{
					ai[3] = 2f;
					netUpdate = true;
				}
			}
			if (ai[3] != 0f)
			{
				if (lifeMax == 5)
				{
					lifeMax = 25;
					life = 25;
					defense = defDefense + 6;
					damage = 20;
				}
				aiStyle = 3;
			}
		}
		if (!WorldGen.InWorld(num6, num7) || Main.tile[num6, num7] == null)
		{
			return;
		}
		if (Main.tile[num6, num7].type == 666 && Main.netMode != 1)
		{
			TryAddingRepeatedBuff(120, 180);
		}
		if (!homeless && Main.netMode != 1 && townNPC && (flag || (type == 37 && Main.tileDungeon[Main.tile[num6, num7].type])) && !AI_007_TownEntities_IsInAGoodRestingSpot(num6, num7, floorX, floorY))
		{
			bool flag6 = true;
			for (int k = 0; k < 2; k++)
			{
				if (!flag6)
				{
					break;
				}
				Rectangle rectangle = new Rectangle((int)(position.X + (float)(width / 2) - (float)(sWidth / 2) - (float)safeRangeX), (int)(position.Y + (float)(height / 2) - (float)(sHeight / 2) - (float)safeRangeY), sWidth + safeRangeX * 2, sHeight + safeRangeY * 2);
				if (k == 1)
				{
					rectangle = new Rectangle(floorX * 16 + 8 - sWidth / 2 - safeRangeX, floorY * 16 + 8 - sHeight / 2 - safeRangeY, sWidth + safeRangeX * 2, sHeight + safeRangeY * 2);
				}
				for (int l = 0; l < 255; l++)
				{
					if (Main.player[l].active && new Rectangle((int)Main.player[l].position.X, (int)Main.player[l].position.Y, Main.player[l].width, Main.player[l].height).Intersects(rectangle))
					{
						flag6 = false;
						break;
					}
				}
			}
			if (flag6)
			{
				AI_007_TownEntities_TeleportToHome(floorX, floorY);
			}
		}
		bool flag7 = type == 300 || type == 447 || type == 610;
		bool flag8 = type == 616 || type == 617 || type == 625;
		bool flag9 = type == 361 || type == 445 || type == 687;
		bool flag10 = NPCID.Sets.IsTownSlime[type];
		_ = NPCID.Sets.IsTownPet[type];
		bool flag11 = flag8 || flag9;
		bool flag12 = flag8 || flag9;
		bool flag13 = flag10;
		bool flag14 = flag10;
		float num11 = 200f;
		if (NPCID.Sets.DangerDetectRange[type] != -1)
		{
			num11 = NPCID.Sets.DangerDetectRange[type];
		}
		float num12 = num11;
		if (flag5 && NPCID.Sets.AttackType[type] == 3 && num12 < 250f)
		{
			num12 = 250f;
		}
		bool flag15 = false;
		bool flag16 = false;
		bool flag17 = false;
		bool flag18 = false;
		float num13 = -1f;
		float num14 = -1f;
		int num15 = 0;
		int num16 = -1;
		int num17 = -1;
		if (!flag8 && Main.netMode != 1)
		{
			for (int m = 0; m < Main.maxNPCs; m++)
			{
				if (!Main.npc[m].active || NPCID.Sets.CritterThatCanTurnOnPlayers[Main.npc[m].type] || Main.npc[m].type == 690 || ((Main.npc[m].friendly || Main.npc[m].damage <= 0) && !Main.npc[m].stinky) || m == whoAmI || !(Main.npc[m].Distance(base.Center) < num12) || (type == 453 && NPCID.Sets.Skeletons[Main.npc[m].type]) || (!Main.npc[m].noTileCollide && !Collision.CanHit(base.Center, 0, 0, Main.npc[m].Center, 0, 0)))
				{
					continue;
				}
				flag15 = true;
				if (Main.npc[m].Distance(base.Center) >= num11)
				{
					continue;
				}
				bool flag19 = Main.npc[m].CanBeChasedBy(this);
				flag16 = true;
				if (Main.npc[m].stinky)
				{
					flag17 = true;
				}
				float num18 = Main.npc[m].Center.X - base.Center.X;
				if (type == 614)
				{
					if (num18 < 0f && (num13 == -1f || num18 > num13))
					{
						num14 = num18;
						num17 = m;
					}
					if (num18 > 0f && (num14 == -1f || num18 < num14))
					{
						num13 = num18;
						num16 = m;
					}
					continue;
				}
				if (num18 < 0f && (num13 == -1f || num18 > num13))
				{
					num13 = num18;
					if (flag19)
					{
						num16 = m;
					}
				}
				if (num18 > 0f && (num14 == -1f || num18 < num14))
				{
					num14 = num18;
					if (flag19)
					{
						num17 = m;
					}
				}
			}
			if (!flag16 && !flag5)
			{
				for (int n = 0; n < 255; n++)
				{
					if (Main.player[n].active && !Main.player[n].dead && Main.player[n].stinky && Main.player[n].Distance(base.Center) < num11 && (Main.player[n].stinky || (type != 633 && type != 37 && type != 441 && type != 228 && type != 107 && type != 453)))
					{
						flag16 = true;
						flag17 = true;
						float num19 = Main.player[n].Center.X - base.Center.X;
						if (num19 < 0f && (num13 == -1f || num19 > num13))
						{
							num13 = num19;
							num16 = n;
						}
						if (num19 > 0f && (num14 == -1f || num19 < num14))
						{
							num14 = num19;
							num17 = n;
						}
					}
				}
			}
			if (flag16 && !flag5)
			{
				num15 = ((num13 == -1f) ? 1 : ((num14 != -1f) ? (num14 < 0f - num13).ToDirectionInt() : (-1)));
				float num20 = 0f;
				if (num13 != -1f)
				{
					num20 = 0f - num13;
				}
				if (num20 == 0f || (num14 < num20 && num14 > 0f))
				{
					num20 = num14;
				}
				if (ai[0] == 8f)
				{
					if (direction == -num15)
					{
						ai[0] = 1f;
						ai[1] = 300 + Main.rand.Next(300);
						ai[2] = 0f;
						localAI[3] = 0f;
						netUpdate = true;
					}
				}
				else if (ai[0] != 10f && ai[0] != 12f && ai[0] != 13f && ai[0] != 14f && ai[0] != 15f)
				{
					if (NPCID.Sets.PrettySafe[type] != -1 && (float)NPCID.Sets.PrettySafe[type] < num20)
					{
						flag16 = false;
					}
					else if (ai[0] != 1f)
					{
						int tileX = (int)((position.X + (float)(width / 2) + (float)(15 * direction)) / 16f);
						int tileY = (int)((position.Y + (float)height - 16f) / 16f);
						bool currentlyDrowning = wet && !flag11;
						AI_007_TownEntities_GetWalkPrediction(num6, floorX, flag11, currentlyDrowning, tileX, tileY, out var _, out var avoidFalling);
						if (!avoidFalling)
						{
							if (ai[0] == 3f || ai[0] == 4f || ai[0] == 16f || ai[0] == 17f)
							{
								NPC nPC = Main.npc[(int)ai[2]];
								if (nPC.active)
								{
									nPC.ai[0] = 1f;
									nPC.ai[1] = 120 + Main.rand.Next(120);
									nPC.ai[2] = 0f;
									nPC.localAI[3] = 0f;
									nPC.direction = -num15;
									nPC.netUpdate = true;
								}
							}
							ai[0] = 1f;
							ai[1] = 120 + Main.rand.Next(120);
							ai[2] = 0f;
							localAI[3] = 0f;
							if (flag2)
							{
								direction = num15;
							}
							else
							{
								direction = -num15;
							}
							netUpdate = true;
						}
					}
					else if (!flag2 && ai[0] == 1f && direction != -num15)
					{
						direction = -num15;
						netUpdate = true;
					}
				}
			}
		}
		if (ai[0] == 0f)
		{
			if (flag5 && num9 != 0 && !flag16 && !flag15)
			{
				direction = num9;
			}
			if (stinky)
			{
				ai[0] = 1f;
			}
			if (localAI[3] > 0f)
			{
				localAI[3] -= 1f;
			}
			int num21 = 120;
			if (type == 638)
			{
				num21 = 60;
			}
			if ((flag9 || flag10) && wet)
			{
				ai[0] = 1f;
				ai[1] = 200 + Main.rand.Next(500, 700);
				ai[2] = 0f;
				localAI[3] = 0f;
				netUpdate = true;
			}
			else if (flag && !flag5 && !NPCID.Sets.TownCritter[type])
			{
				if (Main.netMode != 1)
				{
					if (num6 == floorX && num7 == floorY)
					{
						if (velocity.X != 0f)
						{
							netUpdate = true;
						}
						if (velocity.X > 0.1f)
						{
							velocity.X -= 0.1f;
						}
						else if (velocity.X < -0.1f)
						{
							velocity.X += 0.1f;
						}
						else
						{
							velocity.X = 0f;
							AI_007_TryForcingSitting(floorX, floorY);
						}
						if (NPCID.Sets.IsTownPet[type])
						{
							AI_007_AttemptToPlayIdleAnimationsForPets(num21 * 4);
						}
					}
					else
					{
						if (num6 > floorX)
						{
							direction = -1;
						}
						else
						{
							direction = 1;
						}
						ai[0] = 1f;
						ai[1] = 200 + Main.rand.Next(200);
						ai[2] = 0f;
						localAI[3] = 0f;
						netUpdate = true;
					}
				}
			}
			else
			{
				if (flag7)
				{
					velocity.X *= 0.5f;
				}
				if (velocity.X > 0.1f)
				{
					velocity.X -= 0.1f;
				}
				else if (velocity.X < -0.1f)
				{
					velocity.X += 0.1f;
				}
				else
				{
					velocity.X = 0f;
				}
				if (Main.netMode != 1)
				{
					if (!flag5 && NPCID.Sets.IsTownPet[type] && ai[1] >= 100f && ai[1] <= 150f)
					{
						AI_007_AttemptToPlayIdleAnimationsForPets(num21);
					}
					if (ai[1] > 0f)
					{
						ai[1] -= 1f;
					}
					bool flag20 = true;
					int tileX2 = (int)((position.X + (float)(width / 2) + (float)(15 * direction)) / 16f);
					int tileY2 = (int)((position.Y + (float)height - 16f) / 16f);
					bool currentlyDrowning2 = wet && !flag11;
					AI_007_TownEntities_GetWalkPrediction(num6, floorX, flag11, currentlyDrowning2, tileX2, tileY2, out var _, out var avoidFalling2);
					if (wet && !flag11)
					{
						bool currentlyDrowning3 = Collision.DrownCollision(position, width, height, 1f, includeSlopes: true);
						if (AI_007_TownEntities_CheckIfWillDrown(currentlyDrowning3))
						{
							ai[0] = 1f;
							ai[1] = 200 + Main.rand.Next(300);
							ai[2] = 0f;
							if (NPCID.Sets.TownCritter[type])
							{
								ai[1] += Main.rand.Next(200, 400);
							}
							localAI[3] = 0f;
							netUpdate = true;
						}
					}
					if (avoidFalling2)
					{
						flag20 = false;
					}
					if (ai[1] <= 0f)
					{
						if (flag20 && !avoidFalling2)
						{
							ai[0] = 1f;
							ai[1] = 200 + Main.rand.Next(300);
							ai[2] = 0f;
							if (NPCID.Sets.TownCritter[type])
							{
								ai[1] += Main.rand.Next(200, 400);
							}
							localAI[3] = 0f;
							netUpdate = true;
						}
						else
						{
							direction *= -1;
							ai[1] = 60 + Main.rand.Next(120);
							netUpdate = true;
						}
					}
				}
			}
			if (Main.netMode != 1 && (!flag || AI_007_TownEntities_IsInAGoodRestingSpot(num6, num7, floorX, floorY)))
			{
				if (num6 < floorX - 25 || num6 > floorX + 25)
				{
					if (localAI[3] == 0f)
					{
						if (num6 < floorX - 50 && direction == -1)
						{
							direction = 1;
							netUpdate = true;
						}
						else if (num6 > floorX + 50 && direction == 1)
						{
							direction = -1;
							netUpdate = true;
						}
					}
				}
				else if (Main.rand.Next(80) == 0 && localAI[3] == 0f)
				{
					localAI[3] = 200f;
					direction *= -1;

```


---

## 🤖 Assistant · 2026-08-17T04:32:59.830Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '54200,54600p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_007_TownEntities lines 54200-54600"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:32:59.867Z

**📎 ToolResult**

```
					direction *= -1;
					netUpdate = true;
				}
			}
		}
		else if (ai[0] == 1f)
		{
			if (Main.netMode != 1 && flag && AI_007_TownEntities_IsInAGoodRestingSpot(num6, num7, floorX, floorY) && !NPCID.Sets.TownCritter[type])
			{
				ai[0] = 0f;
				ai[1] = 200 + Main.rand.Next(200);
				localAI[3] = 60f;
				netUpdate = true;
			}
			else
			{
				bool flag21 = !flag11 && Collision.DrownCollision(position, width, height, 1f, includeSlopes: true);
				if (!flag21)
				{
					if (Main.netMode != 1 && !homeless && !Main.tileDungeon[Main.tile[num6, num7].type] && (num6 < floorX - 35 || num6 > floorX + 35))
					{
						if (position.X < (float)(floorX * 16) && direction == -1)
						{
							ai[1] -= 5f;
						}
						else if (position.X > (float)(floorX * 16) && direction == 1)
						{
							ai[1] -= 5f;
						}
					}
					ai[1] -= 1f;
				}
				if (ai[1] <= 0f)
				{
					ai[0] = 0f;
					ai[1] = 300 + Main.rand.Next(300);
					ai[2] = 0f;
					if (NPCID.Sets.TownCritter[type])
					{
						ai[1] -= Main.rand.Next(100);
					}
					else
					{
						ai[1] += Main.rand.Next(900);
					}
					localAI[3] = 60f;
					netUpdate = true;
				}
				if (closeDoor && ((position.X + (float)(width / 2)) / 16f > (float)(doorX + 2) || (position.X + (float)(width / 2)) / 16f < (float)(doorX - 2)))
				{
					Tile tileSafely = Framing.GetTileSafely(doorX, doorY);
					if (tileSafely.type == 11)
					{
						if (WorldGen.CloseDoor(doorX, doorY))
						{
							closeDoor = false;
							NetMessage.SendData(19, -1, -1, null, 1, doorX, doorY, direction);
						}
						if ((position.X + (float)(width / 2)) / 16f > (float)(doorX + 4) || (position.X + (float)(width / 2)) / 16f < (float)(doorX - 4) || (position.Y + (float)(height / 2)) / 16f > (float)(doorY + 4) || (position.Y + (float)(height / 2)) / 16f < (float)(doorY - 4))
						{
							closeDoor = false;
						}
					}
					else if (tileSafely.type == 389)
					{
						if (WorldGen.ShiftTallGate(doorX, doorY, closing: true))
						{
							closeDoor = false;
							NetMessage.SendData(19, -1, -1, null, 5, doorX, doorY);
						}
						if ((position.X + (float)(width / 2)) / 16f > (float)(doorX + 4) || (position.X + (float)(width / 2)) / 16f < (float)(doorX - 4) || (position.Y + (float)(height / 2)) / 16f > (float)(doorY + 4) || (position.Y + (float)(height / 2)) / 16f < (float)(doorY - 4))
						{
							closeDoor = false;
						}
					}
					else
					{
						closeDoor = false;
					}
				}
				float num22 = 1f;
				float num23 = 0.07f;
				if (type == 614 && flag16)
				{
					num22 = 1.5f;
					num23 = 0.1f;
				}
				else if (type == 299 || type == 539 || type == 538 || (type >= 639 && type <= 645))
				{
					num22 = 1.5f;
				}
				else if (flag8)
				{
					if (wet)
					{
						num23 = 1f;
						num22 = 2f;
					}
					else
					{
						num23 = 0.07f;
						num22 = 0.5f;
					}
				}
				if (type == 625)
				{
					if (wet)
					{
						num23 = 1f;
						num22 = 2.5f;
					}
					else
					{
						num23 = 0.07f;
						num22 = 0.2f;
					}
				}
				if (flag7)
				{
					num22 = 2f;
					num23 = 1f;
				}
				if (friendly && (flag16 || flag21))
				{
					num22 = 1.5f;
					float num24 = 1f - (float)life / (float)lifeMax;
					num22 += num24 * 0.9f;
					num23 = 0.1f;
				}
				if (flag13 && wet)
				{
					num22 = 2f;
					num23 = 0.2f;
				}
				if (flag9 && wet)
				{
					if (Math.Abs(velocity.X) < 0.05f && Math.Abs(velocity.Y) < 0.05f)
					{
						velocity.X += num22 * 10f * (float)direction;
					}
					else
					{
						velocity.X *= 0.9f;
					}
				}
				else if (velocity.X < 0f - num22 || velocity.X > num22)
				{
					if (velocity.Y == 0f)
					{
						velocity *= 0.8f;
					}
				}
				else if (velocity.X < num22 && direction == 1)
				{
					velocity.X += num23;
					if (velocity.X > num22)
					{
						velocity.X = num22;
					}
				}
				else if (velocity.X > 0f - num22 && direction == -1)
				{
					velocity.X -= num23;
					if (velocity.X > num22)
					{
						velocity.X = num22;
					}
				}
				bool flag22 = true;
				if ((float)(homeTileY * 16 - 32) > position.Y)
				{
					flag22 = false;
				}
				if (!flag22 && velocity.Y == 0f)
				{
					Collision.StepDown(ref position, ref velocity, width, height, ref stepSpeed, ref gfxOffY);
				}
				if (velocity.Y >= 0f)
				{
					float num25 = gfxOffY;
					Vector2 vector2 = position;
					Vector2 vector3 = velocity;
					Collision.StepUp(ref position, ref velocity, width, height, ref stepSpeed, ref gfxOffY, 1, flag22, 1);
					if (num25 == gfxOffY && vector2 == position && vector3 == velocity && ai[1] < 100f && ai[1] % 10f == 0f && Main.netMode != 1)
					{
						ai[0] = 1f;
						ai[1] = 200 + Main.rand.Next(300);
						ai[2] = 0f;
						if (NPCID.Sets.TownCritter[type])
						{
							ai[1] += Main.rand.Next(200, 400);
						}
						direction *= -1;
						velocity.X *= -1f;
						netUpdate = true;
						return;
					}
				}
				if (velocity.Y == 0f)
				{
					int num26 = (int)((position.X + (float)(width / 2) + (float)(15 * direction)) / 16f);
					int num27 = (int)((position.Y + (float)height - 16f) / 16f);
					int num28 = 180;
					AI_007_TownEntities_GetWalkPrediction(num6, floorX, flag11, flag21, num26, num27, out var keepwalking3, out var avoidFalling3);
					bool flag23 = false;
					bool flag24 = false;
					if (wet && !flag11 && isLikeATownNPC && (flag24 = AI_007_TownEntities_CheckIfWillDrown(flag21)) && localAI[3] <= 0f)
					{
						avoidFalling3 = true;
						localAI[3] = num28;
						int num29 = 0;
						for (int num30 = 0; num30 <= 10 && Framing.GetTileSafely(num26 - direction, num27 - num30).liquid != 0; num30++)
						{
							num29++;
						}
						float num31 = 0.3f;
						float num32 = (float)Math.Sqrt((float)(num29 * 16 + 16) * 2f * num31);
						if (num32 > 26f)
						{
							num32 = 26f;
						}
						velocity.Y = 0f - num32;
						localAI[3] = position.X;
						flag23 = true;
					}
					if (avoidFalling3 && !flag23)
					{
						int num33 = (int)((position.X + (float)(width / 2)) / 16f);
						int num34 = 0;
						for (int num35 = -1; num35 <= 1; num35++)
						{
							Tile tileSafely2 = Framing.GetTileSafely(num33 + num35, num27 + 1);
							if (tileSafely2.nactive() && Main.tileSolid[tileSafely2.type])
							{
								num34++;
							}
						}
						if (num34 <= 2)
						{
							if (velocity.X != 0f)
							{
								netUpdate = true;
							}
							keepwalking3 = (avoidFalling3 = false);
							ai[0] = 0f;
							ai[1] = 50 + Main.rand.Next(50);
							ai[2] = 0f;
							localAI[3] = 40f;
						}
					}
					if (position.X == localAI[3] && !flag23)
					{
						direction *= -1;
						netUpdate = true;
						localAI[3] = num28;
					}
					if (flag21 && !flag23)
					{
						if (localAI[3] > (float)num28)
						{
							localAI[3] = num28;
						}
						if (localAI[3] > 0f)
						{
							localAI[3] -= 1f;
						}
					}
					else
					{
						localAI[3] = -1f;
					}
					Tile tileSafely3 = Framing.GetTileSafely(num26, num27);
					Tile tileSafely4 = Framing.GetTileSafely(num26, num27 - 1);
					Tile tileSafely5 = Framing.GetTileSafely(num26, num27 - 2);
					bool flag25 = height / 16 < 3;
					if (townNPC && tileSafely5.nactive() && (tileSafely5.type == 10 || tileSafely5.type == 388) && (Main.rand.Next(10) == 0 || flag))
					{
						if (Main.netMode != 1)
						{
							if (WorldGen.OpenDoor(num26, num27 - 2, direction))
							{
								closeDoor = true;
								doorX = num26;
								doorY = num27 - 2;
								NetMessage.SendData(19, -1, -1, null, 0, num26, num27 - 2, direction);
								netUpdate = true;
								ai[1] += 80f;
							}
							else if (WorldGen.OpenDoor(num26, num27 - 2, -direction))
							{
								closeDoor = true;
								doorX = num26;
								doorY = num27 - 2;
								NetMessage.SendData(19, -1, -1, null, 0, num26, num27 - 2, -direction);
								netUpdate = true;
								ai[1] += 80f;
							}
							else if (WorldGen.ShiftTallGate(num26, num27 - 2, closing: false))
							{
								closeDoor = true;
								doorX = num26;
								doorY = num27 - 2;
								NetMessage.SendData(19, -1, -1, null, 4, num26, num27 - 2);
								netUpdate = true;
								ai[1] += 80f;
							}
							else
							{
								direction *= -1;
								netUpdate = true;
							}
						}
					}
					else
					{
						if ((velocity.X < 0f && direction == -1) || (velocity.X > 0f && direction == 1))
						{
							bool flag26 = false;
							bool flag27 = false;
							if (tileSafely5.nactive() && Main.tileSolid[tileSafely5.type] && !Main.tileSolidTop[tileSafely5.type] && (!flag25 || (tileSafely4.nactive() && Main.tileSolid[tileSafely4.type] && !Main.tileSolidTop[tileSafely4.type])))
							{
								if (!Collision.SolidTilesVersatile(num26 - direction * 2, num26 - direction, num27 - 5, num27 - 1) && !Collision.SolidTiles(num26, num26, num27 - 5, num27 - 3))
								{
									velocity.Y = -6f;
									netUpdate = true;
								}
								else if (flag7)
								{
									if (WorldGen.SolidTile((int)(base.Center.X / 16f) + direction, (int)(base.Center.Y / 16f)))
									{
										direction *= -1;
										velocity.X *= 0f;
										netUpdate = true;
									}
								}
								else if (flag16)
								{
									flag27 = true;
									flag26 = true;
								}
								else if (!flag24)
								{
									flag26 = true;
								}
							}
							else if (tileSafely4.nactive() && Main.tileSolid[tileSafely4.type] && !Main.tileSolidTop[tileSafely4.type])
							{
								if (!Collision.SolidTilesVersatile(num26 - direction * 2, num26 - direction, num27 - 4, num27 - 1) && !Collision.SolidTiles(num26, num26, num27 - 4, num27 - 2))
								{
									velocity.Y = -5f;
									netUpdate = true;
								}
								else if (flag16)
								{
									flag27 = true;
									flag26 = true;
								}
								else
								{
									flag26 = true;
								}
							}
							else if (position.Y + (float)height - (float)(num27 * 16) > 20f && tileSafely3.nactive() && Main.tileSolid[tileSafely3.type] && !tileSafely3.topSlope())
							{
								if (!Collision.SolidTilesVersatile(num26 - direction * 2, num26, num27 - 3, num27 - 1))
								{
									velocity.Y = -4.4f;
									netUpdate = true;
								}
								else if (flag16)
								{
									flag27 = true;
									flag26 = true;
								}
								else
								{
									flag26 = true;
								}
							}
							else if (avoidFalling3)
							{
								if (!flag24)
								{
									flag26 = true;
								}
								if (flag16)
								{
									flag27 = true;
								}
							}
							else if (flag14 && !Collision.SolidTilesVersatile(num26 - direction * 2, num26 - direction, num27 - 2, num27 - 1))
							{
								velocity.Y = -5f;
								netUpdate = true;
							}
							if (flag27)
							{
								keepwalking3 = false;
								velocity.X = 0f;
								ai[0] = 8f;
								ai[1] = 240f;

```


---

## 🤖 Assistant · 2026-08-17T04:33:03.790Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Continuing to read. Let me continue to 55000.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:33:03.869Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '54600,55000p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_007_TownEntities lines 54600-55000"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:33:03.901Z

**📎 ToolResult**

```
								ai[1] = 240f;
								netUpdate = true;
							}
							if (flag26)
							{
								direction *= -1;
								velocity.X *= -1f;
								netUpdate = true;
							}
							if (keepwalking3)
							{
								ai[1] = 90f;
								netUpdate = true;
							}
							if (velocity.Y < 0f)
							{
								localAI[3] = position.X;
							}
						}
						if (velocity.Y < 0f && wet)
						{
							velocity.Y *= 1.2f;
						}
						if (velocity.Y < 0f && NPCID.Sets.TownCritter[type] && !flag7)
						{
							velocity.Y *= 1.2f;
						}
					}
				}
				else if (flag14 && !wet)
				{
					int num36 = (int)(base.Center.X / 16f);
					int num37 = (int)((position.Y + (float)height - 16f) / 16f);
					int num38 = 0;
					for (int num39 = -1; num39 <= 1; num39++)
					{
						for (int num40 = 1; num40 <= 6; num40++)
						{
							Tile tileSafely6 = Framing.GetTileSafely(num36 + num39, num37 + num40);
							if (tileSafely6.liquid > 0 || (tileSafely6.nactive() && Main.tileSolid[tileSafely6.type]))
							{
								num38++;
							}
						}
					}
					if (num38 <= 2)
					{
						if (velocity.X != 0f)
						{
							netUpdate = true;
						}
						velocity.X *= 0.2f;
						ai[0] = 0f;
						ai[1] = 50 + Main.rand.Next(50);
						ai[2] = 0f;
						localAI[3] = 40f;
					}
				}
			}
		}
		else if (ai[0] == 2f || ai[0] == 11f)
		{
			if (Main.netMode != 1)
			{
				localAI[3] -= 1f;
				if (Main.rand.Next(60) == 0 && localAI[3] == 0f)
				{
					localAI[3] = 60f;
					direction *= -1;
					netUpdate = true;
				}
			}
			ai[1] -= 1f;
			velocity.X *= 0.8f;
			if (ai[1] <= 0f)
			{
				localAI[3] = 40f;
				ai[0] = 0f;
				ai[1] = 60 + Main.rand.Next(60);
				netUpdate = true;
			}
		}
		else if (ai[0] == 3f || ai[0] == 4f || ai[0] == 5f || ai[0] == 8f || ai[0] == 9f || ai[0] == 16f || ai[0] == 17f || ai[0] == 20f || ai[0] == 21f || ai[0] == 22f || ai[0] == 23f)
		{
			velocity.X *= 0.8f;
			ai[1] -= 1f;
			if (ai[0] == 8f && ai[1] < 60f && flag16)
			{
				ai[1] = 180f;
				netUpdate = true;
			}
			if (ai[0] == 5f)
			{
				Point coords = (base.Bottom + Vector2.UnitY * -2f).ToTileCoordinates();
				Tile tile = Main.tile[coords.X, coords.Y];
				if (tile != null && tile.type != 15 && tile.type != 497)
				{
					ai[1] = 0f;
				}
				else
				{
					Main.sittingManager.AddNPC(whoAmI, coords);
				}
			}
			if (ai[1] <= 0f)
			{
				ai[0] = 0f;
				ai[1] = 60 + Main.rand.Next(60);
				ai[2] = 0f;
				localAI[3] = 30 + Main.rand.Next(60);
				netUpdate = true;
			}
		}
		else if (ai[0] == 6f || ai[0] == 7f || ai[0] == 18f || ai[0] == 19f)
		{
			if (ai[0] == 18f && (localAI[3] < 1f || localAI[3] > 2f))
			{
				localAI[3] = 2f;
			}
			velocity.X *= 0.8f;
			ai[1] -= 1f;
			int num41 = (int)ai[2];
			if (num41 < 0 || num41 > 255 || !Main.player[num41].CanBeTalkedTo || Main.player[num41].Distance(base.Center) > 200f || !Collision.CanHitLine(base.Top, 0, 0, Main.player[num41].Top, 0, 0))
			{
				ai[1] = 0f;
			}
			if (ai[1] > 0f)
			{
				int num42 = ((base.Center.X < Main.player[num41].Center.X) ? 1 : (-1));
				if (num42 != direction)
				{
					netUpdate = true;
				}
				direction = num42;
			}
			else
			{
				ai[0] = 0f;
				ai[1] = 60 + Main.rand.Next(60);
				ai[2] = 0f;
				localAI[3] = 30 + Main.rand.Next(60);
				netUpdate = true;
			}
		}
		else if (ai[0] == 10f)
		{
			int num43 = 0;
			int num44 = 0;
			float knockBack = 0f;
			float num45 = 0f;
			int num46 = 0;
			int num47 = 0;
			int maxValue = 0;
			float num48 = 0f;
			float num49 = NPCID.Sets.DangerDetectRange[type];
			float num50 = 0f;
			if ((float)NPCID.Sets.AttackTime[type] == ai[1])
			{
				frameCounter = 0.0;
				localAI[3] = 0f;
			}
			if (type == 38)
			{
				num43 = 30;
				num45 = 6f;
				num44 = 20;
				num46 = 10;
				num47 = 180;
				maxValue = 120;
				num48 = 16f;
				knockBack = 7f;
			}
			else if (type == 633)
			{
				num43 = 880;
				num45 = 24f;
				num44 = 15;
				num46 = 1;
				num48 = 0f;
				knockBack = 7f;
				num47 = 15;
				maxValue = 10;
				if (ShouldBestiaryGirlBeLycantrope())
				{
					num43 = 929;
					num44 = (int)((float)num44 * 1.5f);
				}
			}
			else if (type == 550)
			{
				num43 = 669;
				num45 = 6f;
				num44 = 24;
				num46 = 10;
				num47 = 120;
				maxValue = 60;
				num48 = 16f;
				knockBack = 9f;
			}
			else if (type == 588)
			{
				num43 = 721;
				num45 = 8f;
				num44 = 15;
				num46 = 5;
				num47 = 20;
				maxValue = 10;
				num48 = 16f;
				knockBack = 9f;
			}
			else if (type == 208)
			{
				num43 = 588;
				num45 = 6f;
				num44 = 30;
				num46 = 10;
				num47 = 60;
				maxValue = 120;
				num48 = 16f;
				knockBack = 6f;
			}
			else if (type == 17)
			{
				num43 = 48;
				num45 = 9f;
				num44 = 12;
				num46 = 10;
				num47 = 60;
				maxValue = 60;
				num48 = 16f;
				knockBack = 1.5f;
			}
			else if (type == 369)
			{
				num43 = 520;
				num45 = 12f;
				num44 = 10;
				num46 = 10;
				num47 = 0;
				maxValue = 1;
				num48 = 16f;
				knockBack = 3f;
			}
			else if (type == 453)
			{
				num43 = 21;
				num45 = 14f;
				num44 = 14;
				num46 = 10;
				num47 = 0;
				maxValue = 1;
				num48 = 16f;
				knockBack = 3f;
			}
			else if (type == 107)
			{
				num43 = 24;
				num45 = 5f;
				num44 = 15;
				num46 = 10;
				num47 = 60;
				maxValue = 60;
				num48 = 16f;
				knockBack = 1f;
			}
			else if (type == 124)
			{
				num43 = 582;
				num45 = 10f;
				num44 = 11;
				num46 = 1;
				num47 = 30;
				maxValue = 30;
				knockBack = 3.5f;
			}
			else if (type == 18)
			{
				num43 = 583;
				num45 = 8f;
				num44 = 8;
				num46 = 1;
				num47 = 15;
				maxValue = 10;
				knockBack = 2f;
				num48 = 10f;
			}
			else if (type == 142)
			{
				num43 = 589;
				num45 = 7f;
				num44 = 22;
				num46 = 1;
				num47 = 10;
				maxValue = 1;
				knockBack = 2f;
				num48 = 10f;
			}
			num44 = GetAttackDamage_ForTownNPC((float)num44 * num2);
			velocity.X *= 0.8f;
			ai[1] -= 1f;
			localAI[3] += 1f;
			if (localAI[3] == (float)num46 && Main.netMode != 1)
			{
				Vector2 vec = -Vector2.UnitY;
				if (num15 == 1 && spriteDirection == 1 && num17 != -1)
				{
					vec = DirectionTo(Main.npc[num17].Center + new Vector2(0f, (0f - num48) * MathHelper.Clamp(Distance(Main.npc[num17].Center) / num49, 0f, 1f)));
				}
				if (num15 == -1 && spriteDirection == -1 && num16 != -1)
				{
					vec = DirectionTo(Main.npc[num16].Center + new Vector2(0f, (0f - num48) * MathHelper.Clamp(Distance(Main.npc[num16].Center) / num49, 0f, 1f)));
				}
				if (vec.HasNaNs() || Math.Sign(vec.X) != spriteDirection)
				{
					vec = new Vector2(spriteDirection, -1f);
				}
				vec *= num45;
				vec += Utils.RandomVector2(Main.rand, 0f - num50, num50);
				int num51 = 1000;
				num51 = ((type == 124) ? Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec.X, vec.Y, num43, num44, knockBack, Main.myPlayer, 0f, whoAmI, townNpcVariationIndex) : ((type != 142) ? Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec.X, vec.Y, num43, num44, knockBack, Main.myPlayer) : Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec.X, vec.Y, num43, num44, knockBack, Main.myPlayer, 0f, Main.rand.Next(5))));
				Main.projectile[num51].npcProj = true;
				Main.projectile[num51].noDropItem = true;
				if (type == 588)
				{
					Main.projectile[num51].timeLeft = 480;
				}
			}
			if (ai[1] <= 0f && 0 == 0)
			{
				ai[0] = ((localAI[2] == 8f && flag16) ? 8 : 0);
				ai[1] = num47 + Main.rand.Next(maxValue);
				ai[2] = 0f;
				localAI[1] = (localAI[3] = num47 / 2 + Main.rand.Next(maxValue));
				netUpdate = true;
			}
		}
		else if (ai[0] == 12f)
		{
			int num52 = 0;
			int num53 = 0;
			float num54 = 0f;
			int num55 = 0;
			int num56 = 0;
			int maxValue2 = 0;
			float knockBack2 = 0f;
			int num57 = 0;
			bool flag28 = false;
			float num58 = 0f;
			if ((float)NPCID.Sets.AttackTime[type] == ai[1])
			{
				frameCounter = 0.0;
				localAI[3] = 0f;
			}
			int num59 = -1;
			if (num15 == 1 && spriteDirection == 1)
			{
				num59 = num17;
			}
			if (num15 == -1 && spriteDirection == -1)
			{
				num59 = num16;
			}
			if (type == 19)
			{
				num52 = 14;
				num54 = 13f;
				num53 = 24;
				num56 = 14;
				maxValue2 = 4;
				knockBack2 = 3f;
				num55 = 1;
				num58 = 0.5f;
				if ((float)NPCID.Sets.AttackTime[type] == ai[1])
				{
					frameCounter = 0.0;
					localAI[3] = 0f;
				}
				if (Main.hardMode)
				{
					num53 = 15;
					if (localAI[3] > (float)num55)
					{
						num55 = 10;
						flag28 = true;
					}
					if (localAI[3] > (float)num55)
					{
						num55 = 20;
						flag28 = true;
					}
					if (localAI[3] > (float)num55)
					{
						num55 = 30;
						flag28 = true;
					}
				}
			}
			else if (type == 227)
			{
				num52 = 587;
				num54 = 10f;

```


---

## 🤖 Assistant · 2026-08-17T04:33:06.957Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I've now seen state 10, 12 (combat), 0, 1, 2/11, 3/4/5/8/9/16/17/20/21/22/23, 6/7/18/19. Let me continue reading 55000-55400 to see states 13/14/15 and the party/dance states, plus dialogue trigger code.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:33:07.406Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '55000,55400p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_007_TownEntities lines 55000-55400"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:33:07.439Z

**📎 ToolResult**

```
				num54 = 10f;
				num53 = 8;
				num56 = 10;
				maxValue2 = 1;
				knockBack2 = 1.75f;
				num55 = 1;
				num58 = 0.5f;
				if (localAI[3] > (float)num55)
				{
					num55 = 12;
					flag28 = true;
				}
				if (localAI[3] > (float)num55)
				{
					num55 = 24;
					flag28 = true;
				}
				if (Main.hardMode)
				{
					num53 += 2;
				}
			}
			else if (type == 368)
			{
				num52 = 14;
				num54 = 13f;
				num53 = 24;
				num56 = 12;
				maxValue2 = 5;
				knockBack2 = 2f;
				num55 = 1;
				num58 = 0.2f;
				if (Main.hardMode)
				{
					num53 = 30;
					num52 = 357;
				}
			}
			else if (type == 22)
			{
				num54 = 10f;
				num53 = 12;
				num55 = 1;
				if (Main.hardMode)
				{
					num52 = 2;
					num56 = 15;
					maxValue2 = 10;
					num53 += 6;
				}
				else
				{
					num52 = 1;
					num56 = 30;
					maxValue2 = 20;
				}
				knockBack2 = 2.75f;
				num57 = 4;
				num58 = 0.7f;
			}
			else if (type == 228)
			{
				num52 = 267;
				num54 = 14f;
				num53 = 20;
				num55 = 1;
				num56 = 10;
				maxValue2 = 1;
				knockBack2 = 3f;
				num57 = 6;
				num58 = 0.4f;
			}
			else if (type == 178)
			{
				num52 = 242;
				num54 = 13f;
				num53 = ((!Main.hardMode) ? 11 : 15);
				num56 = 10;
				maxValue2 = 1;
				knockBack2 = 2f;
				num55 = 1;
				if (localAI[3] > (float)num55)
				{
					num55 = 8;
					flag28 = true;
				}
				if (localAI[3] > (float)num55)
				{
					num55 = 16;
					flag28 = true;
				}
				num58 = 0.3f;
			}
			else if (type == 229)
			{
				num52 = 14;
				num54 = 14f;
				num53 = 24;
				num56 = 10;
				maxValue2 = 1;
				knockBack2 = 2f;
				num55 = 1;
				num58 = 0.7f;
				if (localAI[3] > (float)num55)
				{
					num55 = 16;
					flag28 = true;
				}
				if (localAI[3] > (float)num55)
				{
					num55 = 24;
					flag28 = true;
				}
				if (localAI[3] > (float)num55)
				{
					num55 = 32;
					flag28 = true;
				}
				if (localAI[3] > (float)num55)
				{
					num55 = 40;
					flag28 = true;
				}
				if (localAI[3] > (float)num55)
				{
					num55 = 48;
					flag28 = true;
				}
				if (localAI[3] == 0f && num59 != -1 && Distance(Main.npc[num59].Center) < (float)NPCID.Sets.PrettySafe[type])
				{
					num58 = 0.1f;
					num52 = 162;
					num53 = 50;
					knockBack2 = 10f;
					num54 = 24f;
				}
			}
			else if (type == 209)
			{
				num52 = Utils.SelectRandom<int>(Main.rand, 134, 133, 135);
				num55 = 1;
				switch (num52)
				{
				case 135:
					num54 = 12f;
					num53 = 30;
					num56 = 30;
					maxValue2 = 10;
					knockBack2 = 7f;
					num58 = 0.2f;
					break;
				case 133:
					num54 = 10f;
					num53 = 25;
					num56 = 10;
					maxValue2 = 1;
					knockBack2 = 6f;
					num58 = 0.2f;
					break;
				case 134:
					num54 = 13f;
					num53 = 20;
					num56 = 20;
					maxValue2 = 10;
					knockBack2 = 4f;
					num58 = 0.1f;
					break;
				}
			}
			num53 = GetAttackDamage_ForTownNPC((float)num53 * num2);
			velocity.X *= 0.8f;
			ai[1] -= 1f;
			localAI[3] += 1f;
			if (localAI[3] == (float)num55 && Main.netMode != 1)
			{
				Vector2 vec2 = Vector2.Zero;
				if (num59 != -1)
				{
					vec2 = DirectionTo(Main.npc[num59].Center + new Vector2(0f, -num57));
				}
				if (vec2.HasNaNs() || Math.Sign(vec2.X) != spriteDirection)
				{
					vec2 = new Vector2(spriteDirection, 0f);
				}
				vec2 *= num54;
				vec2 += Utils.RandomVector2(Main.rand, 0f - num58, num58);
				int num60 = 1000;
				num60 = ((type != 227) ? Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec2.X, vec2.Y, num52, num53, knockBack2, Main.myPlayer) : Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec2.X, vec2.Y, num52, num53, knockBack2, Main.myPlayer, 0f, (float)Main.rand.Next(12) / 6f));
				Main.projectile[num60].npcProj = true;
				Main.projectile[num60].noDropItem = true;
			}
			if (localAI[3] == (float)num55 && flag28 && num59 != -1)
			{
				Vector2 vector4 = DirectionTo(Main.npc[num59].Center);
				if (vector4.Y <= 0.5f && vector4.Y >= -0.5f)
				{
					ai[2] = vector4.Y;
				}
			}
			if (ai[1] <= 0f && 0 == 0)
			{
				ai[0] = ((localAI[2] == 8f && flag16) ? 8 : 0);
				ai[1] = num56 + Main.rand.Next(maxValue2);
				ai[2] = 0f;
				localAI[1] = (localAI[3] = num56 / 2 + Main.rand.Next(maxValue2));
				netUpdate = true;
			}
		}
		else if (ai[0] == 13f)
		{
			velocity.X *= 0.8f;
			if ((float)NPCID.Sets.AttackTime[type] == ai[1])
			{
				frameCounter = 0.0;
			}
			ai[1] -= 1f;
			localAI[3] += 1f;
			if (localAI[3] == 1f && Main.netMode != 1)
			{
				Vector2 vec3 = DirectionTo(Main.npc[(int)ai[2]].Center + new Vector2(0f, -20f));
				if (vec3.HasNaNs() || Math.Sign(vec3.X) == -spriteDirection)
				{
					vec3 = new Vector2(spriteDirection, -1f);
				}
				vec3 *= 8f;
				int num61 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec3.X, vec3.Y, 584, 0, 0f, Main.myPlayer, ai[2]);
				Main.projectile[num61].npcProj = true;
				Main.projectile[num61].noDropItem = true;
			}
			if (ai[1] <= 0f)
			{
				ai[0] = 0f;
				ai[1] = 10 + Main.rand.Next(10);
				ai[2] = 0f;
				localAI[3] = 5 + Main.rand.Next(10);
				netUpdate = true;
			}
		}
		else if (ai[0] == 14f)
		{
			int num62 = 0;
			int num63 = 0;
			float num64 = 0f;
			int num65 = 0;
			int num66 = 0;
			int maxValue3 = 0;
			float knockBack3 = 0f;
			float num67 = 0f;
			float num68 = NPCID.Sets.DangerDetectRange[type];
			float num69 = 1f;
			float num70 = 0f;
			if ((float)NPCID.Sets.AttackTime[type] == ai[1])
			{
				frameCounter = 0.0;
				localAI[3] = 0f;
			}
			int num71 = -1;
			if (num15 == 1 && spriteDirection == 1)
			{
				num71 = num17;
			}
			if (num15 == -1 && spriteDirection == -1)
			{
				num71 = num16;
			}
			if (type == 54)
			{
				num62 = 585;
				num64 = 10f;
				num63 = 16;
				num65 = 30;
				num66 = 20;
				maxValue3 = 15;
				knockBack3 = 2f;
				num70 = 1f;
			}
			else if (type == 108)
			{
				num62 = 15;
				num64 = 6f;
				num63 = 18;
				num65 = 15;
				num66 = 15;
				maxValue3 = 5;
				knockBack3 = 3f;
				num67 = 20f;
			}
			else if (type == 160)
			{
				num62 = 590;
				num63 = 40;
				num65 = 15;
				num66 = 10;
				maxValue3 = 1;
				knockBack3 = 3f;
				for (; localAI[3] > (float)num65; num65 += 15)
				{
				}
			}
			else if (type == 663)
			{
				num62 = 950;
				num63 = ((!Main.hardMode) ? 15 : 20);
				num65 = 15;
				num66 = 0;
				maxValue3 = 0;
				knockBack3 = 3f;
				for (; localAI[3] > (float)num65; num65 += 10)
				{
				}
			}
			else if (type == 20)
			{
				num62 = 586;
				num65 = 24;
				num66 = 10;
				maxValue3 = 1;
				knockBack3 = 3f;
			}
			num63 = GetAttackDamage_ForTownNPC((float)num63 * num2);
			velocity.X *= 0.8f;
			ai[1] -= 1f;
			localAI[3] += 1f;
			if (localAI[3] == (float)num65 && Main.netMode != 1)
			{
				Vector2 vec4 = Vector2.Zero;
				if (num71 != -1)
				{
					vec4 = DirectionTo(Main.npc[num71].Center + new Vector2(0f, (0f - num67) * MathHelper.Clamp(Distance(Main.npc[num71].Center) / num68, 0f, 1f)));
				}
				if (vec4.HasNaNs() || Math.Sign(vec4.X) != spriteDirection)
				{
					vec4 = new Vector2(spriteDirection, 0f);
				}
				vec4 *= num64;
				vec4 += Utils.RandomVector2(Main.rand, 0f - num70, num70);
				if (type == 108)
				{
					int num72 = Utils.SelectRandom<int>(Main.rand, 1, 1, 1, 1, 2, 2, 3);
					for (int num73 = 0; num73 < num72; num73++)
					{
						Vector2 vector5 = Utils.RandomVector2(Main.rand, -3.4f, 3.4f);
						int num74 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec4.X + vector5.X, vec4.Y + vector5.Y, num62, num63, knockBack3, Main.myPlayer, 0f, 0f, townNpcVariationIndex);
						Main.projectile[num74].npcProj = true;
						Main.projectile[num74].noDropItem = true;
					}
				}
				else if (type == 160)
				{
					if (num71 != -1)
					{
						Vector2 vector6 = Main.npc[num71].position - Main.npc[num71].Size * 2f + Main.npc[num71].Size * Utils.RandomVector2(Main.rand, 0f, 1f) * 5f;
						int num75 = 10;
						while (num75 > 0 && WorldGen.SolidTile(Framing.GetTileSafely((int)vector6.X / 16, (int)vector6.Y / 16)))
						{
							num75--;
							vector6 = Main.npc[num71].position - Main.npc[num71].Size * 2f + Main.npc[num71].Size * Utils.RandomVector2(Main.rand, 0f, 1f) * 5f;
						}
						int num76 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector6.X, vector6.Y, 0f, 0f, num62, num63, knockBack3, Main.myPlayer, 0f, 0f, townNpcVariationIndex);
						Main.projectile[num76].npcProj = true;
						Main.projectile[num76].noDropItem = true;
					}
				}
				else if (type == 663)
				{
					if (num71 != -1)
					{
						Vector2 vector7 = Main.npc[num71].position + Main.npc[num71].Size * Utils.RandomVector2(Main.rand, 0f, 1f) * 1f;
						int num77 = 5;
						while (num77 > 0 && WorldGen.SolidTile(Framing.GetTileSafely((int)vector7.X / 16, (int)vector7.Y / 16)))
						{
							num77--;
							vector7 = Main.npc[num71].position + Main.npc[num71].Size * Utils.RandomVector2(Main.rand, 0f, 1f) * 1f;
						}
						int num78 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector7.X, vector7.Y, 0f, 0f, num62, num63, knockBack3, Main.myPlayer, 0f, 0f, townNpcVariationIndex);
						Main.projectile[num78].npcProj = true;
						Main.projectile[num78].noDropItem = true;
					}
				}
				else if (type == 20)
				{
					int num79 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec4.X, vec4.Y, num62, num63, knockBack3, Main.myPlayer, 0f, whoAmI, townNpcVariationIndex);
					Main.projectile[num79].npcProj = true;
					Main.projectile[num79].noDropItem = true;
				}
				else
				{
					int num80 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec4.X, vec4.Y, num62, num63, knockBack3, Main.myPlayer);
					Main.projectile[num80].npcProj = true;
					Main.projectile[num80].noDropItem = true;
				}
			}
			if (num69 > 0f)
			{
				Vector3 vector8 = GetMagicAuraColor().ToVector3() * num69;
				Lighting.AddLight(base.Center, vector8.X, vector8.Y, vector8.Z);
			}
			if (ai[1] <= 0f && 0 == 0)
			{
				ai[0] = ((localAI[2] == 8f && flag16) ? 8 : 0);
				ai[1] = num66 + Main.rand.Next(maxValue3);

```


---

## 🤖 Assistant · 2026-08-17T04:33:09.858Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '55400,55830p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_007_TownEntities lines 55400-55830"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:33:09.897Z

**📎 ToolResult**

```
				ai[1] = num66 + Main.rand.Next(maxValue3);
				ai[2] = 0f;
				localAI[1] = (localAI[3] = num66 / 2 + Main.rand.Next(maxValue3));
				netUpdate = true;
			}
		}
		else if (ai[0] == 15f)
		{
			int num81 = 0;
			int maxValue4 = 0;
			if ((float)NPCID.Sets.AttackTime[type] == ai[1])
			{
				frameCounter = 0.0;
				localAI[3] = 0f;
			}
			int num82 = 0;
			float num83 = 0f;
			int num84 = 0;
			int num85 = 0;
			if (num15 == 1)
			{
				_ = spriteDirection;
				_ = 1;
			}
			if (num15 == -1)
			{
				_ = spriteDirection;
				_ = -1;
			}
			if (type == 207)
			{
				num82 = 11;
				num84 = (num85 = 32);
				num81 = 12;
				maxValue4 = 6;
				num83 = 4.25f;
			}
			else if (type == 441)
			{
				num82 = 9;
				num84 = (num85 = 28);
				num81 = 9;
				maxValue4 = 3;
				num83 = 3.5f;
				if (GivenName == "Andrew")
				{
					num82 *= 2;
					num83 *= 2f;
				}
			}
			else if (type == 353)
			{
				num82 = 10;
				num84 = (num85 = 32);
				num81 = 15;
				maxValue4 = 8;
				num83 = 5f;
			}
			else if (NPCID.Sets.IsTownPet[type])
			{
				num82 = 10;
				num84 = (num85 = 32);
				num81 = 15;
				maxValue4 = 8;
				num83 = 3f;
			}
			num82 = GetAttackDamage_ForTownNPC((float)num82 * num2);
			velocity.X *= 0.8f;
			ai[1] -= 1f;
			if (Main.netMode != 1)
			{
				Tuple<Vector2, float> swingStats = GetSwingStats(NPCID.Sets.AttackTime[type] * 2, (int)ai[1], spriteDirection, num84, num85);
				Rectangle itemRectangle = new Rectangle((int)swingStats.Item1.X, (int)swingStats.Item1.Y, num84, num85);
				if (spriteDirection == -1)
				{
					itemRectangle.X -= num84;
				}
				itemRectangle.Y -= num85;
				TweakSwingStats(NPCID.Sets.AttackTime[type] * 2, (int)ai[1], spriteDirection, ref itemRectangle);
				int myPlayer = Main.myPlayer;
				for (int num86 = 0; num86 < Main.maxNPCs; num86++)
				{
					NPC nPC2 = Main.npc[num86];
					if (nPC2.active && nPC2.immune[myPlayer] == 0 && !nPC2.dontTakeDamage && !nPC2.friendly && nPC2.damage > 0 && itemRectangle.Intersects(nPC2.Hitbox) && (nPC2.noTileCollide || Collision.CanHit(position, width, height, nPC2.position, nPC2.width, nPC2.height)))
					{
						nPC2.StrikeNPCNoInteraction(num82, num83, spriteDirection);
						if (Main.netMode != 0)
						{
							NetMessage.SendData(28, -1, -1, null, num86, num82, num83, spriteDirection);
						}
						nPC2.netUpdate = true;
						nPC2.immune[myPlayer] = (int)ai[1] + 2;
					}
				}
			}
			if (ai[1] <= 0f)
			{
				bool flag29 = false;
				if (flag16)
				{
					int num87 = -num15;
					if (!Collision.CanHit(base.Center, 0, 0, base.Center + Vector2.UnitX * num87 * 32f, 0, 0) || localAI[2] == 8f)
					{
						flag29 = true;
					}
					if (flag29)
					{
						int num88 = NPCID.Sets.AttackTime[type];
						int num89 = ((num15 == 1) ? num17 : num16);
						int num90 = ((num15 == 1) ? num16 : num17);
						if (num89 != -1 && !Collision.CanHit(base.Center, 0, 0, Main.npc[num89].Center, 0, 0))
						{
							num89 = ((num90 == -1 || !Collision.CanHit(base.Center, 0, 0, Main.npc[num90].Center, 0, 0)) ? (-1) : num90);
						}
						if (num89 != -1)
						{
							ai[0] = 15f;
							ai[1] = num88;
							ai[2] = 0f;
							localAI[3] = 0f;
							direction = ((position.X < Main.npc[num89].position.X) ? 1 : (-1));
							netUpdate = true;
						}
						else
						{
							flag29 = false;
						}
					}
				}
				if (!flag29)
				{
					ai[0] = ((localAI[2] == 8f && flag16) ? 8 : 0);
					ai[1] = num81 + Main.rand.Next(maxValue4);
					ai[2] = 0f;
					localAI[1] = (localAI[3] = num81 / 2 + Main.rand.Next(maxValue4));
					netUpdate = true;
				}
			}
		}
		else if (ai[0] == 24f)
		{
			velocity.X *= 0.8f;
			ai[1] -= 1f;
			localAI[3] += 1f;
			direction = 1;
			spriteDirection = 1;
			Vector3 vector9 = GetMagicAuraColor().ToVector3();
			Lighting.AddLight(base.Center, vector9.X, vector9.Y, vector9.Z);
			if (ai[1] <= 0f)
			{
				ai[0] = 0f;
				ai[1] = 480f;
				ai[2] = 0f;
				localAI[1] = 480f;
				netUpdate = true;
			}
		}
		if (flag13 && wet)
		{
			int num91 = (int)(base.Center.X / 16f);
			int num92 = 5;
			if (collideX || (num91 < num92 && direction == -1) || (num91 > Main.maxTilesX - num92 && direction == 1))
			{
				direction *= -1;
				velocity.X *= -0.25f;
				netUpdate = true;
			}
			velocity.Y *= 0.9f;
			velocity.Y -= 0.5f;
			if (velocity.Y < -15f)
			{
				velocity.Y = -15f;
			}
		}
		if (flag12 && wet)
		{
			if (flag9)
			{
				ai[1] = 50f;
			}
			int num93 = (int)(base.Center.X / 16f);
			int num94 = 5;
			if (collideX || (num93 < num94 && direction == -1) || (num93 > Main.maxTilesX - num94 && direction == 1))
			{
				direction *= -1;
				velocity.X *= -0.25f;
				netUpdate = true;
			}
			if (Collision.GetWaterLine(base.Center.ToTileCoordinates(), out var waterLineHeight))
			{
				float num95 = base.Center.Y + 1f;
				if (base.Center.Y > waterLineHeight)
				{
					velocity.Y -= 0.8f;
					if (velocity.Y < -4f)
					{
						velocity.Y = -4f;
					}
					if (num95 + velocity.Y < waterLineHeight)
					{
						velocity.Y = waterLineHeight - num95;
					}
				}
				else
				{
					velocity.Y = MathHelper.Min(velocity.Y, waterLineHeight - num95);
				}
			}
			else
			{
				velocity.Y -= 0.2f;
			}
		}
		if (Main.netMode != 1 && isLikeATownNPC && (!flag5 || flag16))
		{
			if (flag5)
			{
				num3 *= 0.8f;
				num15 = ((num13 == -1f) ? 1 : ((num14 != -1f) ? (num14 < 0f - num13).ToDirectionInt() : (-1)));
			}
			bool flag30 = ai[0] < 2f && !flag16 && !wet;
			bool flag31 = (ai[0] < 2f || ai[0] == 8f) && (flag16 || flag18) && !flag17;
			if (localAI[1] > 0f)
			{
				localAI[1] -= 1f;
			}
			if (localAI[1] > 0f)
			{
				flag31 = false;
			}
			if (flag31 && type == 124 && localAI[0] == 1f)
			{
				flag31 = false;
			}
			if (flag31 && type == 20)
			{
				flag31 = false;
				for (int num96 = 0; num96 < Main.maxNPCs; num96++)
				{
					NPC nPC3 = Main.npc[num96];
					if (nPC3.active && nPC3.townNPC && !(Distance(nPC3.Center) > 1200f) && nPC3.FindBuffIndex(165) == -1)
					{
						flag31 = true;
						break;
					}
				}
			}
			if (CanTalk && flag30 && ai[0] == 0f && velocity.Y == 0f && Main.rand.Next(300) == 0)
			{
				int num97 = 420;
				num97 = ((Main.rand.Next(2) != 0) ? (num97 * Main.rand.Next(1, 3)) : (num97 * Main.rand.Next(1, 4)));
				int num98 = 100;
				int num99 = 20;
				for (int num100 = 0; num100 < Main.maxNPCs; num100++)
				{
					NPC nPC4 = Main.npc[num100];
					bool flag32 = (nPC4.ai[0] == 1f && nPC4.closeDoor) || (nPC4.ai[0] == 1f && nPC4.ai[1] > 200f) || nPC4.ai[0] > 1f || nPC4.wet;
					if (nPC4 != this && nPC4.active && nPC4.CanBeTalkedTo && !flag32 && nPC4.Distance(base.Center) < (float)num98 && nPC4.Distance(base.Center) > (float)num99 && Collision.CanHit(base.Center, 0, 0, nPC4.Center, 0, 0))
					{
						int num101 = (position.X < nPC4.position.X).ToDirectionInt();
						ai[0] = 3f;
						ai[1] = num97;
						ai[2] = num100;
						direction = num101;
						netUpdate = true;
						nPC4.ai[0] = 4f;
						nPC4.ai[1] = num97;
						nPC4.ai[2] = whoAmI;
						nPC4.direction = -num101;
						nPC4.netUpdate = true;
						break;
					}
				}
			}
			else if (CanTalk && flag30 && ai[0] == 0f && velocity.Y == 0f && Main.rand.Next(1800) == 0)
			{
				int num102 = 420;
				num102 = ((Main.rand.Next(2) != 0) ? (num102 * Main.rand.Next(1, 3)) : (num102 * Main.rand.Next(1, 4)));
				int num103 = 100;
				int num104 = 20;
				for (int num105 = 0; num105 < Main.maxNPCs; num105++)
				{
					NPC nPC5 = Main.npc[num105];
					bool flag33 = (nPC5.ai[0] == 1f && nPC5.closeDoor) || (nPC5.ai[0] == 1f && nPC5.ai[1] > 200f) || nPC5.ai[0] > 1f || nPC5.wet;
					if (nPC5 != this && nPC5.active && nPC5.CanBeTalkedTo && !NPCID.Sets.IsTownPet[nPC5.type] && !flag33 && nPC5.Distance(base.Center) < (float)num103 && nPC5.Distance(base.Center) > (float)num104 && Collision.CanHit(base.Center, 0, 0, nPC5.Center, 0, 0))
					{
						int num106 = (position.X < nPC5.position.X).ToDirectionInt();
						ai[0] = 16f;
						ai[1] = num102;
						ai[2] = num105;
						localAI[2] = Main.rand.Next(4);
						localAI[3] = Main.rand.Next(3 - (int)localAI[2]);
						direction = num106;
						netUpdate = true;
						nPC5.ai[0] = 17f;
						nPC5.ai[1] = num102;
						nPC5.ai[2] = whoAmI;
						nPC5.localAI[2] = 0f;
						nPC5.localAI[3] = 0f;
						nPC5.direction = -num106;
						nPC5.netUpdate = true;
						break;
					}
				}
			}
			else if (!NPCID.Sets.IsTownPet[type] && flag30 && ai[0] == 0f && velocity.Y == 0f && Main.rand.Next(1200) == 0 && (type == 208 || (BirthdayParty.PartyIsUp && NPCID.Sets.AttackType[type] == NPCID.Sets.AttackType[208])))
			{
				int num107 = 300;
				int num108 = 150;
				for (int num109 = 0; num109 < 255; num109++)
				{
					Player player = Main.player[num109];
					if (player.active && !player.dead && player.Distance(base.Center) < (float)num108 && Collision.CanHitLine(base.Top, 0, 0, player.Top, 0, 0))
					{
						int num110 = (position.X < player.position.X).ToDirectionInt();
						ai[0] = 6f;
						ai[1] = num107;
						ai[2] = num109;
						direction = num110;
						netUpdate = true;
						break;
					}
				}
			}
			else if (flag30 && ai[0] == 0f && velocity.Y == 0f && Main.rand.Next(600) == 0 && type == 550)
			{
				int num111 = 300;
				int num112 = 150;
				for (int num113 = 0; num113 < 255; num113++)
				{
					Player player2 = Main.player[num113];
					if (player2.active && !player2.dead && player2.Distance(base.Center) < (float)num112 && Collision.CanHitLine(base.Top, 0, 0, player2.Top, 0, 0))
					{
						int num114 = (position.X < player2.position.X).ToDirectionInt();
						ai[0] = 18f;
						ai[1] = num111;
						ai[2] = num113;
						direction = num114;
						netUpdate = true;
						break;
					}
				}
			}
			else if (!NPCID.Sets.IsTownPet[type] && flag30 && ai[0] == 0f && velocity.Y == 0f && Main.rand.Next(1800) == 0)
			{
				ai[0] = 2f;
				ai[1] = 45 * Main.rand.Next(1, 2);
				netUpdate = true;
			}
			else if (flag30 && ai[0] == 0f && velocity.Y == 0f && Main.rand.Next(600) == 0 && type == 229 && !flag18)
			{
				ai[0] = 11f;
				ai[1] = 30 * Main.rand.Next(1, 4);
				netUpdate = true;
			}
			else if (flag30 && ai[0] == 0f && velocity.Y == 0f && Main.rand.Next(1200) == 0)
			{
				int num115 = 220;
				int num116 = 150;
				for (int num117 = 0; num117 < 255; num117++)
				{
					Player player3 = Main.player[num117];
					if (player3.CanBeTalkedTo && player3.Distance(base.Center) < (float)num116 && Collision.CanHitLine(base.Top, 0, 0, player3.Top, 0, 0))
					{
						int num118 = (position.X < player3.position.X).ToDirectionInt();
						ai[0] = 7f;
						ai[1] = num115;
						ai[2] = num117;
						direction = num118;
						netUpdate = true;
						break;
					}
				}
			}
			else if (flag30 && ai[0] == 1f && velocity.Y == 0f && num > 0 && Main.rand.Next(num) == 0)
			{
				Point point = (base.Bottom + Vector2.UnitY * -2f).ToTileCoordinates();
				bool flag34 = WorldGen.InWorld(point.X, point.Y, 1);
				if (flag34)
				{
					for (int num119 = 0; num119 < Main.maxNPCs; num119++)
					{
						if (Main.npc[num119].active && Main.npc[num119].aiStyle == 7 && Main.npc[num119].townNPC && Main.npc[num119].ai[0] == 5f && (Main.npc[num119].Bottom + Vector2.UnitY * -2f).ToTileCoordinates() == point)
						{
							flag34 = false;
							break;
						}
					}
					for (int num120 = 0; num120 < 255; num120++)
					{
						if (Main.player[num120].active && Main.player[num120].sitting.isSitting && Main.player[num120].Center.ToTileCoordinates() == point)
						{
							flag34 = false;
							break;
						}
					}
				}
				if (flag34)
				{
					Tile tile2 = Main.tile[point.X, point.Y];
					flag34 = tile2.type == 15 || tile2.type == 497;
					if (flag34 && tile2.type == 15 && tile2.frameY >= 1080 && tile2.frameY <= 1098)
					{
						flag34 = false;
					}
					if (flag34)
					{
						ai[0] = 5f;
						ai[1] = 900 + Main.rand.Next(10800);
						direction = ((tile2.frameX != 0) ? 1 : (-1));
						base.Bottom = new Vector2(point.X * 16 + 8 + 2 * direction, point.Y * 16 + 16);
						velocity = Vector2.Zero;
						localAI[3] = 0f;
						netUpdate = true;
					}
				}
			}
			else if (flag30 && ai[0] == 1f && velocity.Y == 0f && Main.rand.Next(600) == 0 && Utils.PlotTileLine(base.Top, base.Bottom, width, DelegateMethods.SearchAvoidedByNPCs))
			{
				Point point2 = (base.Center + new Vector2(direction * 10, 0f)).ToTileCoordinates();
				bool flag35 = WorldGen.InWorld(point2.X, point2.Y, 1);
				if (flag35)
				{
					Tile tileSafely7 = Framing.GetTileSafely(point2.X, point2.Y);
					if (!tileSafely7.nactive() || !TileID.Sets.InteractableByNPCs[tileSafely7.type])
					{
						flag35 = false;
					}
				}
				if (flag35)
				{

```


---

## 🤖 Assistant · 2026-08-17T04:33:11.769Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Continuing. Let me read to the end of the method (~55982), and then also read TeleportToHome and GetWalkPrediction, and the party/dance parts.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:33:12.522Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '55830,56175p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_007_TownEntities tail + teleport + walk prediction"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:33:12.557Z

**📎 ToolResult**

```
				{
					ai[0] = 9f;
					ai[1] = 40 + Main.rand.Next(90);
					velocity = Vector2.Zero;
					localAI[3] = 0f;
					netUpdate = true;
				}
			}
			if (Main.netMode != 1 && ai[0] < 2f && velocity.Y == 0f && type == 18 && breath > 0)
			{
				int num121 = -1;
				for (int num122 = 0; num122 < Main.maxNPCs; num122++)
				{
					NPC nPC6 = Main.npc[num122];
					if (nPC6.active && nPC6.townNPC && nPC6.life != nPC6.lifeMax && (num121 == -1 || nPC6.lifeMax - nPC6.life > Main.npc[num121].lifeMax - Main.npc[num121].life) && Collision.CanHitLine(position, width, height, nPC6.position, nPC6.width, nPC6.height) && Distance(nPC6.Center) < 500f)
					{
						num121 = num122;
					}
				}
				if (num121 != -1)
				{
					ai[0] = 13f;
					ai[1] = 34f;
					ai[2] = num121;
					localAI[3] = 0f;
					direction = ((position.X < Main.npc[num121].position.X) ? 1 : (-1));
					netUpdate = true;
				}
			}
			int num123 = (int)((float)NPCID.Sets.AttackAverageChance[type] * num3);
			if (num123 < 1)
			{
				num123 = 1;
			}
			if (flag31 && velocity.Y == 0f && NPCID.Sets.AttackType[type] == 0 && NPCID.Sets.AttackAverageChance[type] > 0 && Main.rand.Next(num123) == 0)
			{
				int num124 = NPCID.Sets.AttackTime[type];
				int num125 = ((num15 == 1) ? num17 : num16);
				int num126 = ((num15 == 1) ? num16 : num17);
				if (num125 != -1 && !Collision.CanHit(base.Center, 0, 0, Main.npc[num125].Center, 0, 0))
				{
					num125 = ((num126 == -1 || !Collision.CanHit(base.Center, 0, 0, Main.npc[num126].Center, 0, 0)) ? (-1) : num126);
				}
				bool flag36 = num125 != -1;
				if (flag36 && type == 633)
				{
					flag36 = Vector2.Distance(base.Center, Main.npc[num125].Center) <= 50f;
				}
				if (flag36)
				{
					localAI[2] = ai[0];
					ai[0] = 10f;
					ai[1] = num124;
					ai[2] = 0f;
					localAI[3] = 0f;
					direction = ((position.X < Main.npc[num125].position.X) ? 1 : (-1));
					netUpdate = true;
				}
			}
			else if (flag31 && velocity.Y == 0f && NPCID.Sets.AttackType[type] == 1 && NPCID.Sets.AttackAverageChance[type] > 0 && Main.rand.Next(num123) == 0)
			{
				int num127 = NPCID.Sets.AttackTime[type];
				int num128 = ((num15 == 1) ? num17 : num16);
				int num129 = ((num15 == 1) ? num16 : num17);
				if (num128 != -1 && !Collision.CanHitLine(base.Center, 0, 0, Main.npc[num128].Center, 0, 0))
				{
					num128 = ((num129 == -1 || !Collision.CanHitLine(base.Center, 0, 0, Main.npc[num129].Center, 0, 0)) ? (-1) : num129);
				}
				if (num128 != -1)
				{
					Vector2 vector10 = DirectionTo(Main.npc[num128].Center);
					if (vector10.Y <= 0.5f && vector10.Y >= -0.5f)
					{
						localAI[2] = ai[0];
						ai[0] = 12f;
						ai[1] = num127;
						ai[2] = vector10.Y;
						localAI[3] = 0f;
						direction = ((position.X < Main.npc[num128].position.X) ? 1 : (-1));
						netUpdate = true;
					}
				}
			}
			if (flag31 && velocity.Y == 0f && NPCID.Sets.AttackType[type] == 2 && NPCID.Sets.AttackAverageChance[type] > 0 && Main.rand.Next(num123) == 0)
			{
				int num130 = NPCID.Sets.AttackTime[type];
				int num131 = ((num15 == 1) ? num17 : num16);
				int num132 = ((num15 == 1) ? num16 : num17);
				if (num131 != -1 && !Collision.CanHitLine(base.Center, 0, 0, Main.npc[num131].Center, 0, 0))
				{
					num131 = ((num132 == -1 || !Collision.CanHitLine(base.Center, 0, 0, Main.npc[num132].Center, 0, 0)) ? (-1) : num132);
				}
				if (num131 != -1)
				{
					localAI[2] = ai[0];
					ai[0] = 14f;
					ai[1] = num130;
					ai[2] = 0f;
					localAI[3] = 0f;
					direction = ((position.X < Main.npc[num131].position.X) ? 1 : (-1));
					netUpdate = true;
				}
				else if (type == 20)
				{
					localAI[2] = ai[0];
					ai[0] = 14f;
					ai[1] = num130;
					ai[2] = 0f;
					localAI[3] = 0f;
					netUpdate = true;
				}
			}
			if (flag31 && velocity.Y == 0f && NPCID.Sets.AttackType[type] == 3 && NPCID.Sets.AttackAverageChance[type] > 0 && Main.rand.Next(num123) == 0)
			{
				int num133 = NPCID.Sets.AttackTime[type];
				int num134 = ((num15 == 1) ? num17 : num16);
				int num135 = ((num15 == 1) ? num16 : num17);
				if (num134 != -1 && !Collision.CanHit(base.Center, 0, 0, Main.npc[num134].Center, 0, 0))
				{
					num134 = ((num135 == -1 || !Collision.CanHit(base.Center, 0, 0, Main.npc[num135].Center, 0, 0)) ? (-1) : num135);
				}
				if (num134 != -1)
				{
					localAI[2] = ai[0];
					ai[0] = 15f;
					ai[1] = num133;
					ai[2] = 0f;
					localAI[3] = 0f;
					direction = ((position.X < Main.npc[num134].position.X) ? 1 : (-1));
					netUpdate = true;
				}
			}
		}
		if (type == 681)
		{
			float R = 0f;
			float G = 0f;
			float B = 0f;
			TorchID.TorchColor(23, out R, out G, out B);
			float num136 = 0.35f;
			R *= num136;
			G *= num136;
			B *= num136;
			Lighting.AddLight(base.Center, R, G, B);
		}
		if (type == 683 || type == 687)
		{
			float num137 = Utils.WrappedLerp(0.75f, 1f, (float)Main.timeForVisualEffects % 120f / 120f);
			Lighting.AddLight(base.Center, 0.25f * num137, 0.25f * num137, 0.1f * num137);
		}
	}

	private void AI_007_TownEntities_Shimmer_TeleportToLandingSpot()
	{
		Vector2? vector = AI_007_TownEntities_Shimmer_ScanForBestSpotToLandOn();
		if (vector.HasValue)
		{
			Vector2 vector2 = position;
			position = vector.Value;
			Vector2 movementVector = position - vector2;
			int num = 560;
			if (movementVector.Length() >= (float)num)
			{
				ai[2] = 30f;
				ParticleOrchestrator.BroadcastParticleSpawn(ParticleOrchestraType.ShimmerTownNPCSend, new ParticleOrchestraSettings
				{
					PositionInWorld = vector2 + base.Size / 2f,
					MovementVector = movementVector
				});
			}
			netUpdate = true;
		}
	}

	private Vector2? AI_007_TownEntities_Shimmer_ScanForBestSpotToLandOn()
	{
		Point point = base.Top.ToTileCoordinates();
		int num = 30;
		Vector2? result = null;
		bool flag = homeless && (homeTileX == -1 || homeTileY == -1);
		for (int i = 1; i < num; i += 2)
		{
			Vector2? vector = ShimmerHelper.FindSpotWithoutShimmer(this, point.X, point.Y, i, flag);
			if (vector.HasValue)
			{
				result = vector.Value;
				break;
			}
		}
		if (!result.HasValue && homeTileX != -1 && homeTileY != -1)
		{
			for (int j = 1; j < num; j += 2)
			{
				Vector2? vector2 = ShimmerHelper.FindSpotWithoutShimmer(this, homeTileX, homeTileY, j, flag);
				if (vector2.HasValue)
				{
					result = vector2.Value;
					break;
				}
			}
		}
		if (!result.HasValue)
		{
			int num2 = (flag ? 30 : 0);
			num = 60;
			flag = true;
			for (int k = num2; k < num; k += 2)
			{
				Vector2? vector3 = ShimmerHelper.FindSpotWithoutShimmer(this, point.X, point.Y, k, flag);
				if (vector3.HasValue)
				{
					result = vector3.Value;
					break;
				}
			}
		}
		if (!result.HasValue && homeTileX != -1 && homeTileY != -1)
		{
			num = 60;
			flag = true;
			for (int l = 30; l < num; l += 2)
			{
				Vector2? vector4 = ShimmerHelper.FindSpotWithoutShimmer(this, homeTileX, homeTileY, l, flag);
				if (vector4.HasValue)
				{
					result = vector4.Value;
					break;
				}
			}
		}
		return result;
	}

	private void AI_007_TownEntities_TeleportToHome(int homeFloorX, int homeFloorY)
	{
		bool flag = false;
		for (int i = 0; i < 3; i++)
		{
			int num = homeFloorX + i switch
			{
				1 => -1, 
				0 => 0, 
				_ => 1, 
			};
			if (type == 37 || !Collision.SolidTiles(num - 1, num + 1, homeFloorY - 3, homeFloorY - 1))
			{
				velocity.X = 0f;
				velocity.Y = 0f;
				position.X = num * 16 + 8 - width / 2;
				position.Y = (float)(homeFloorY * 16 - height) - 0.1f;
				netUpdate = true;
				AI_007_TryForcingSitting(homeFloorX, homeFloorY);
				flag = true;
				break;
			}
		}
		if (!flag)
		{
			homeless = true;
			WorldGen.QuickFindHome(whoAmI);
		}
	}

	private void AI_007_TownEntities_GetWalkPrediction(int myTileX, int homeFloorX, bool canBreathUnderWater, bool currentlyDrowning, int tileX, int tileY, out bool keepwalking, out bool avoidFalling)
	{
		keepwalking = false;
		avoidFalling = true;
		bool flag = myTileX >= homeFloorX - 35 && myTileX <= homeFloorX + 35;
		if (isLikeATownNPC && ai[1] < 30f)
		{
			keepwalking = !Utils.PlotTileLine(base.Top, base.Bottom, width, DelegateMethods.SearchAvoidedByNPCs);
			if (!keepwalking)
			{
				Rectangle hitbox = base.Hitbox;
				hitbox.X -= 20;
				hitbox.Width += 40;
				for (int i = 0; i < Main.maxNPCs; i++)
				{
					if (Main.npc[i].active && Main.npc[i].friendly && i != whoAmI && Main.npc[i].velocity.X == 0f && hitbox.Intersects(Main.npc[i].Hitbox))
					{
						keepwalking = true;
						break;
					}
				}
			}
		}
		if (!keepwalking && currentlyDrowning)
		{
			keepwalking = true;
		}
		if (avoidFalling && (NPCID.Sets.TownCritter[type] || (!flag && direction == Math.Sign(homeFloorX - myTileX))))
		{
			avoidFalling = false;
		}
		if (!avoidFalling)
		{
			return;
		}
		bool flag2 = false;
		Point p = default(Point);
		int num = 0;
		for (int j = -1; j <= 4; j++)
		{
			Tile tileSafely = Framing.GetTileSafely(tileX, tileY + j);
			if (tileSafely.liquid > 0)
			{
				num++;
				if (tileSafely.lava())
				{
					flag2 = true;
					break;
				}
			}
			if (tileSafely.nactive() && Main.tileSolid[tileSafely.type])
			{
				if (num > 0)
				{
					p.X = tileX;
					p.Y = tileY + j;
				}
				avoidFalling = false;
				break;
			}
		}
		avoidFalling |= flag2;
		double num2 = Math.Ceiling((float)height / 16f);
		if ((double)num >= num2)
		{
			avoidFalling = true;
		}
		if (!avoidFalling && p.X != 0 && p.Y != 0)
		{
			Vector2 vector = p.ToWorldCoordinates(8f, 0f) + new Vector2(-width / 2, -height);
			avoidFalling = Collision.DrownCollision(vector, width, height, 1f);
		}
	}

	private bool AI_007_TownEntities_CheckIfWillDrown(bool currentlyDrowning)
	{
		return currentlyDrowning;
	}

	private void AI_007_AttemptToPlayIdleAnimationsForPets(int petIdleChance)
	{
		if (velocity.X == 0f && Main.netMode != 1 && Main.rand.Next(petIdleChance) == 0)
		{

```


---

## 🤖 Assistant · 2026-08-17T04:34:10.351Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have a good understanding of vanilla AI_007. Key points:

**ai[0] state machine (vanilla 1.4.5.6):**
- 0: idle (standing)
- 1: walking
- 2: emote (talk bubble?) — actually ai[0]==2: "45 * Main.rand.Next(1,2)" — random chat with themselves? It's the "idle emote" state
- 3: chatting with NPC (pair talk)
- 4: chatting with NPC (pair, other side)
- 5: sitting on chair
- 6: facing player (party chat? no — 6/7 is facing player)
- 7: facing player (player nearby look)
- 8: danger "hiding"/waiting (240 ticks when danger too close)
- 9: interacting with tile (SearchAvoidedByNPCs? no — PlotTileLine + InteractableByNPCs, e.g. torches? — actually it's the "looks at interactable tile" state)
- 10: attack type 0 (shooting)
- 11: Santa? no, type 229 emote (Nurse? no — 229 is... town slime? no). ai[0]==11 with type 229 — "party" dance? Actually 229 might be the Clothier? no. 229 is the... Let me check: type 229 = Party Girl? no, Party Girl is 208. 229 = Santa Claus? No, Santa is 142. 229 = Tax Collector? No, 441. 229 = Stylist (353). Actually 229 might be the "TownSlime"? Hmm. type 229 attack type 1 with lots of escalation... it's likely the "Wizard"? no 108. Let me not worry.
- 12: attack type 1 (thrown/magic)
- 13: Nurse heal (projectile 584)
- 14: attack type 2 (magic)
- 15: attack type 3 (melee swing)
- 16/17: pair chat variant 2 (chat with emotes? localAI[2] up to 4)
- 18/19: bartender talk to player
- 20/21/22/23: ? (in the same "idle-ish" group: velocity.X *= 0.8, ai[1] -= 1) — these are pet idle animations probably
- 24: town pet glow state? (direction=1, magic aura light — for infected dryad?)
- 25: shimmer transformation

**Key behaviors to check in our implementation:**

1. Sitting (ai[0]==5): 
   - Trigger: at night (flag = !dayTime etc.), when at resting spot (num6==floorX && num7==floorY decelerates then TryForcingSitting); also random chance while walking: `Main.rand.Next(num)==0` where num=300 (0 for town slimes), requires standing on chair tile (type 15 chair or 497 throne, not the "toilet"? frameY 1080-1098 is toilet variant), no other NPC sitting there, no player sitting there. ai[1] = 900 + Next(10800) (15s to 3min). direction = frameX != 0 ? 1 : -1. Bottom = x*16+8+2*direction, y*16+16 (for random sit) or y*16 (TryForcingSitting). Sitting uses Main.sittingManager.AddNPC — which drives the sitting frame/position.
   - AI_007_FindGoodRestingSpot: at night, scan home area ±7 x, +2..-6 y for TileID.Sets.CanBeSatOnForNPCs tiles, Manhattan distance minimal, avoid occupied.

2. Sleeping: Town NPCs do NOT sleep in beds in vanilla — sleepingManager is for players only. Town NPCs sit on chairs at night instead. Confirmed: no "sleep" in NPC.cs aside from town NPC? Let me verify no NPC sleep. The grep earlier failed due to weird path issue. Let me re-run the sleep grep on NPC.cs.

3. Wander parameters:
   - idle→walk: ai[1] init? At spawn: ai[1] starts at 0? For idle state 0: ai[1] counts down from initial; when <=0: 60% (flag20 && !avoidFalling2 → walk with ai[1]=200+Next(300) [+200-400 for TownCritter]), else turn around ai[1]=60+Next(120).
   - Actually looking: on transition to state 0, ai[1] = 300+Next(300) then +Next(900) — hmm that's in state 1 → 0: ai[1] = 300 + Next(300) + Next(900).
   - walk→idle: ai[1] counts down 1/tick (minus 5 extra when far from home walking away, beyond ±35 tiles); when <=0 → state 0 with ai[1] = 300+Next(300)+Next(900).
   - turn around at random: `Main.rand.Next(80) == 0` when within ±25 of home and localAI[3]==0 → localAI[3]=200, direction *= -1.
   - far from home: >25 tiles → force direction home if beyond ±50.
   - walk speed: num22=1 (max vel), num23=0.07 (accel); variants for types.
   - obstacle jump: velocity.Y = -6 / -5 / -4.4 depending on obstacle height (2-tile/1-tile/half-tile steps).
   - door opening: tile type 10 (closed door) or 388 (tall gate closed) at head level: 1/10 chance or when "danger" (flag = night/rain etc.). OpenDoor, closeDoor=true, doorX/doorY remembered; ai[1] += 80. If can't open → turn around.
   - door closing: when closeDoor and |x - doorX| > 2 tiles → WorldGen.CloseDoor. Also give up beyond ±4.
   - avoid falling/cliff: GetWalkPrediction — avoidFalling logic, drowning jump out of water (num29 loop computing water depth, velocity.Y = -sqrt(depth*2*0.3) capped 26 → jump out), avoidFalling → check 3 tiles below feet (num33±1, num27+1): if ≤2 solid → stop walking (state 0, ai[1]=50+Next(50), localAI[3]=40).
   - StepDown when above home? flag22 = (homeTileY*16-32) <= position.Y; if !flag22 (below home level? no — position above home tile) → StepDown.
   - StepUp; if blocked (position/velocity unchanged, ai[1]<100, ai[1]%10==0) → turn around.
   - anti-stuck: position.X == localAI[3] → turn.
   - Danger avoidance: enemies within DangerDetectRange (default 200? NPCID.Sets.DangerDetectRange default -1 → num11=200) → run away from danger (direction = -num15 means away? num15 is direction to danger; direction = -num15 → run away). PrettySafe threshold. state 8 (freeze 240 ticks) when very close and can't flee.
   - teleport home at night: flag = raining/night/eclipse/slimeRain/storm; if housed & !dungeon-floor & not in good resting spot & no player within sWidth×sHeight+safeRange rect (2 checks: at NPC position and at home spot) → TeleportToHome. That's the "teleport home when night & player not watching" behavior.

4. Dialogue: 
   - NPC↔NPC chat: state 3/4 (1/300 per tick, distance 20..100, can hit), duration 420×(1..3) or 420×(1..4) (50/50).
   - pair chat variant 16/17: 1/1800 per tick (with localAI[2]=Next(4) random emote).
   - face player state 6: party girl birthday-party-related? — the code at Next(1200) with type 208 or party up → ai[0]=6 (300 ticks facing player). That's "party chat"? It's actually 1.4 party where NPCs face the player? Hmm wait, this uses type 208 or (BirthdayParty.PartyIsUp && same AttackType as 208)... this is for party: state 6.
   - bartender 550: state 18 (1/600).
   - state 2: 1/1800 → random emote/bubble? ai[1] = 45*Next(1,2).
   - state 7: 1/1200 face nearby player (220 ticks).
   - state 11 (type 229 — party girl? no...): 1/600 dance? ai[1]=30*Next(1,4). Actually type 229 is the... let me check. 229 = "TownSlime"? No. Let me check quickly later — might be Party Girl? Party Girl is 208. 229 is likely "Santa"? no 142. 229 is... checking NPCID: 228 = Pirate, 229 = ... Confusion. Actually 228 = Pirate. 229 = Stylist? no 353. Hmm 229 = "Confused"? Let me grep. Actually earlier: type 228 attack type 1 (267 = cannonball?), type 229 attack type 1 num52=14 (arrow) with escalation — 229 might be the "Steampunker"? no that's 178? Wait 178 = Steampunker (242 =... hmm). Let me just grep NPC names for 229.
   
   Player-initiated talk: player.talkNPC → ai[0]=0, ai[1]=300, localAI[3]=100, face player.

5. Teleport home: as above — requires: housed, (night || rain || eclipse || slimeRain || storm above ground), not already in good resting spot, no player intersecting NPC bbox+safeRange at either current pos or home pos → TeleportToHome (3 attempts x-1/x/x+1, check solid tiles above; if blocked → homeless + QuickFindHome). Also TryForcingSitting after teleport.

6. Party: BirthdayParty — during party, NPCs dance? Let me check: vanilla town NPCs during party: party hats (PartyHatColor), and dancing? Let me grep "PartyIsUp" in NPC.cs. Also shopping discount during party: BirthdayParty.GatherPartyNightCash? Actually price adjustment: "Main.worldPartyNight"? There's a 20% discount during parties? Hmm — vanilla: during BirthdayParty, items sold... no discount. Actually there IS: "PartyBunny"? No discount in vanilla I believe. Let me check Player.cs / chest? The party discount: BirthdayParty of 1.4: shopping? I recall no discount. But there's the party gift (present). Let me grep.

7. Push: NPC pushed by players? Vanilla: town NPCs are pushed... there's "npc.ai[0] == 24"? No. Push by player: Player.cs PushNPC? Hmm. In vanilla, walking into NPCs pushes them slightly? I don't think players push NPCs; NPCs push each other? There is collision separation between NPCs (Collision.TileCollision? no). There's code in NPC.AI or UpdateNPC that separates overlapping NPCs? Let me grep.

8. Death: town NPC death → no drops (townNPC drops nothing except...?) — respawn via townNPC spawn system in NPC.SpawnNPC / checkTownNPCs: respawnTimer for town NPC re-spawn: "Main.checkForSpawns"? Town NPCs respawn after death with a delay (they respawn via the town NPC spawning quota system). There's also "npc.spawnRateForTownNPCs"? Let me look at Main.cs UpdateTime spawn logic.

9. Defense posture: town NPCs have "hurt" animation? cowering? Vanilla: town NPCs when danger near (state 8) they cower (frame?). Also dontTakeDamage during shimmer. There's also "cowering" frames used by 633 etc.? The "defense posture" like shielding head — that's actually the "town NPC frightened" visual? Let me search for "cower".

10. Hit flash / knockback / liquids: NPC.HitEffect / StrikeNPC; hitFlash (npc.immunity frames = 10 default? immunityTime), knockback resist for townNPC (knockBack *= ...?), honey slow (npcLiquid.ts exists in our code — likely ported), lava damage for NPCs (TouchDamage? no that's tiles). NPC in lava → takes damage 10/s? There's "wet/honeyWet/lavaWet" handling in Entity.cs / NPC update: "if (lavaWet) ... damage". Let me check our npcLiquid.ts vs vanilla.

Now, let me look at our implementation. Files: game/src/entities/Enemy.ts (NPC主体), entities/ai/? Let me list the ai directory and find the town NPC AI (AI_007). Memory says "town-npc-attack-port" — AI_007四态+持械视觉 done. Let me find the file.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:34:10.811Z · glm-x-preview-260804

```
现在我来看一下 AI_007 辅助函数以及对应的实现文件。
```


---

## 🤖 Assistant · 2026-08-17T04:34:11.917Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/src/entities/ai/ 2>/dev/null; echo ---; grep -rn \"aiStyle7\\|aiStyle === 7\\|AI_007\\|townNPCAI\\|townEntities\" ~/Project/GLM/SandboxWorld/game/src/ --include=\"*.ts\" -l | head -20",
 "description": "Find our AI_007 town NPC implementation files"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:34:11.957Z

**📎 ToolResult**

```
---
~/Project/GLM/SandboxWorld/game/src/core/constants.ts
~/Project/GLM/SandboxWorld/game/src/core/Game.ts
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts
~/Project/GLM/SandboxWorld/game/src/world/wiring/devices.ts
~/Project/GLM/SandboxWorld/game/src/data/vanillaNpcs.ts
~/Project/GLM/SandboxWorld/game/src/data/vanillaTownAttack.ts
~/Project/GLM/SandboxWorld/game/src/data/critters.ts
~/Project/GLM/SandboxWorld/game/src/data/grappleHooks.ts
~/Project/GLM/SandboxWorld/game/src/data/vanillaItemCombat.ts
~/Project/GLM/SandboxWorld/game/src/stats/ScaleStats.ts
~/Project/GLM/SandboxWorld/game/src/entities/PrismProj.ts
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts
~/Project/GLM/SandboxWorld/game/src/entities/TownShot.ts
~/Project/GLM/SandboxWorld/game/src/entities/GrappleProj.ts
~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts
~/Project/GLM/SandboxWorld/game/src/entities/npcLiquid.ts
~/Project/GLM/SandboxWorld/game/src/player/SmartCursor.ts
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts

```


---

## 🤖 Assistant · 2026-08-17T04:34:13.122Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -iE \"\\bsleep\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -30",
 "description": "Search sleep references in vanilla NPC.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:34:13.153Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-17T04:34:17.296Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
No "sleep" references in vanilla NPC.cs at all — confirmed: **town NPCs do not sleep in beds in vanilla 1.4.5.6**. The night behavior is sitting on chairs (state 5).

Now let me read our TownNPC.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:34:18.287Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts ~/Project/GLM/SandboxWorld/game/src/entities/npcLiquid.ts ~/Project/GLM/SandboxWorld/game/src/entities/TownShot.ts ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "description": "Line counts of our town NPC files"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:34:18.310Z

**📎 ToolResult**

```
    1367 ~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts
     232 ~/Project/GLM/SandboxWorld/game/src/entities/npcLiquid.ts
     274 ~/Project/GLM/SandboxWorld/game/src/entities/TownShot.ts
    6970 ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts
    8843 total

```


---

## 🤖 Assistant · 2026-08-17T04:34:19.673Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:34:19.844Z

**📎 ToolResult**

```
1	// 城镇 NPC：游走、夜间回家、对话气泡
2	// 贴图 = 原版 Images/NPC_{id}（Terarria1456 素材条），帧语义按原版 FindFrame 城镇分支
3	// （NPC.cs:69152+）：地面站定=帧0；腾空=帧1；行走帧 2..frames-extra-1 循环
4	// （frameCounter += |vx|*2+1 每 tick，>6 推进一帧，越界回卷帧2）
5	import { Entity } from './Entity';
6	import type { GameHooks } from './types';
7	import type { Player } from './Player';
8	import { GRAVITY, MAX_FALL_SPEED, TILE } from '../core/constants';
9	import { moveAndCollide } from '../physics/TileCollision';
10	import { openDoor, closeDoor as closeDoorTile, shiftTallGate } from '../world/Door';
11	import { TILE_BY_KEY as TILE_BY_KEY_DOOR_TILES, TILE_DEFS } from '../data/tiles';
12	import type { TileStore } from '../world/TileStore';
13	import { TOWN_NPC_IDS, VANILLA_NPCS } from '../data/vanillaNpcs';
14	import { isNpcTownShimmerable, findShimmerFreeSpot } from '../stats/Shimmer';
15	import { townNpcAltTexture, townNpcProfileSheet, shouldBestiaryGirlBeLycantrope } from '../data/townNpcProfiles';
16	import { getAttackDamageForTownNPC, mainDifficulty } from '../stats/ScaleStats';
17	import { hslToRgb } from '../player/Appearance';
18	import { newNpcName } from '../i18n/RandomText';
19	import { canHit } from '../physics/LineOfSight';
20	import {
21	  TOWN_ATTACK_TIME, TOWN_ATTACK_CHANCE, TOWN_ATTACK_TYPE, TOWN_DANGER_RANGE,
22	  TOWN_MELEE, TOWN_BOW, TOWN_MAGIC, TOWN_SWING, TOWN_PRETTY_SAFE,
23	  type TownShotParams,
24	} from '../data/vanillaTownAttack';
25	import { TownShot } from './TownShot';
26	import { visEffectFrames, mouseTextColorApprox } from './Enemy';
27	
28	export interface NpcHome { x: number; y: number; }
29	
30	// ===================== 坐姿（AI_007 ai[0]==5）纯函数 =====================
31	// 可坐格族 = TileID.Sets.CanBeSatOnForNPCs（TileID.cs:211）恰好 {15 椅, 497 马桶}
32	// ——王座(102)/长凳(89) 只在 CanBeSatOnFor*Players* 集，城镇 NPC 不坐；
33	// 按 sheet 反查内部 tile id（LiquidSim bySheet 同款 reduce）
34	const sheetTileIds = (sheets: ReadonlySet<number>): ReadonlySet<number> => new Set(
35	  TILE_DEFS.reduce<number[]>((acc, d, id) => {
36	    if (d.vanilla && sheets.has(d.vanilla.sheet)) acc.push(id);
37	    return acc;
38	  }, []),
39	);
40	const CHAIR_TILE_IDS = sheetTileIds(new Set([15]));
41	const TOILET_TILE_IDS = sheetTileIds(new Set([497]));
42	/** 不坐椅的城镇实体（FindGoodRestingSpot :53214：type 638 狗 / 656 兔宠物 +
43	 *  IsTownSlime 族 NPCID.cs:4446 = 670/678-684——它们只在地面休息位趴窝） */
44	const NO_SIT_NPC_IDS = new Set([638, 656, 670, 678, 679, 680, 681, 682, 683, 684]);
45	
46	/** FindGoodRestingSpot 扫描期成员判定（:53223 CanBeSatOnForNPCs，无 style 门——
47	 *  style 门在 TryForcingSitting，见 canSitAt） */
48	export function isSitTile(tileId: number): boolean {
49	  return CHAIR_TILE_IDS.has(tileId) || TOILET_TILE_IDS.has(tileId);
50	}
51	
52	/** AI_007_TryForcingSitting 坐下门（NPC.cs:53269-53275）：椅/马桶格 + 椅子
53	 *  style 27 排除（type 15 且 frameY∈[1080,1098]——上格 1080 / 下格 1098 两帧
54	 *  恰好夹住该样式行带；马桶无此门） */
55	export function canSitAt(tileId: number, frameY: number): boolean {
56	  if (TOILET_TILE_IDS.has(tileId)) return true;
57	  if (!CHAIR_TILE_IDS.has(tileId)) return false;
58	  return frameY < 1080 || frameY > 1098;
59	}
60	
61	export interface SitSpot { x: number; y: number; }
62	
63	/** AI_007_FindGoodRestingSpot 夜椅扫描（NPC.cs:53195-53262）：
64	 *  - 自 home 向下找地面（SolidOrSlopedTileOrPlatform = 实心非 top 或平台，:53186）
65	 *  - ±7 列 × 行 {+2,0,-2,-4,-6}（num2/num4/num3/num6）扫可坐格；上格(frameY%40==0)
66	 *    仅当 row+1<=floorY+2 收（:53224），下格恒收
67	 *  - 取 |dx|+|dy| 最小（严格 <，先到先得，:53226-53233）
68	 *  - 归一（:53247-53252）：下格(frameY%40!=0)先 -1 再 +2、上格直接 +2 → 返回
69	 *    {x, y}=落座地面行（椅上格 +2 = 地面行）。无椅 → null（白天原版直接返回
70	 *    home 地面（:53209-53212），由调用方不调本扫描） */
71	export function findChairSpot(st: TileStore, homeX: number, homeY: number): SitSpot | null {
72	  let fx = homeX, fy = homeY;
73	  if (fx < 0 || fy < 0) return null;                       // :53200-53203 home 无效
74	  while (fy < st.h - 20 && !(st.isSolid(fx, fy) || st.isPlatform(fx, fy))) fy++;
75	  let best: { x: number; y: number; d: number; frameY: number } | null = null;
76	  for (let i = fx - 7; i <= fx + 7; i++) {
77	    for (let r = fy + 2; r >= fy - 6; r -= 2) {
78	      if (!st.inBounds(i, r)) continue;
79	      const ti = st.idx(i, r);
80	      if (!isSitTile(st.type[ti])) continue;               // tile.active() 同义（type!=0）
81	      const topFrame = st.frameY[ti] % 40 === 0;
82	      if (topFrame && !(r + 1 <= fy + 2)) continue;        // :53224
83	      const d = Math.abs(i - fx) + Math.abs(r - fy);       // :53226
84	      if (!best || d < best.d) best = { x: i, y: r, d, frameY: st.frameY[ti] };
85	    }
86	  }
87	  if (!best) return null;                                  // :53255-53257
88	  let ry = best.y;
89	  if (best.frameY % 40 !== 0) ry--;                        // :53249-53251 下格 → 上移一行
90	  ry += 2;                                                 // :53252 → 地面行
91	  return { x: best.x, y: ry };
92	}
93	
94	/** 坐姿朝向（:53284 / PlayerSittingHelper.cs:231 同式）：frameX!=0（椅 flip 档
95	 *  +18）→ 1 朝右，否则 -1 朝左 */
96	export function chairFacing(frameX: number): number {
97	  return frameX !== 0 ? 1 : -1;
98	}
99	
100	/** 坐姿锚（:53285-53286）：Bottom = (x*16 + 8 + 2*dir, y*16)——脚底贴地面行顶，
101	 *  比玩家坐姿（PlayerSittingHelper 座面上 16px）更低，即原版城镇 NPC"陷坐"观感 */
102	export function sittingAnchor(x: number, y: number, dir: number): { x: number; y: number } {
103	  return { x: x * TILE + 8 + 2 * dir, y: y * TILE };
104	}
105	
106	/** 入座时长（:53283）：ai[1] = 900 + rand(10800) */
107	export const SIT_TIME_BASE = 900;
108	export const SIT_TIME_RAND = 10800;
109	/** 时限起身后的转向冷却（:54707 localAI[3] = 30 + rand(60)；本仓由 wanderT 承接） */
110	export const SIT_STAND_WANDER_BASE = 30;
111	export const SIT_STAND_WANDER_RAND = 60;
112	
113	/** 坐姿帽 Y 修正链 num6（Main.cs:26965-26987：ai[0]==5 时默认 −4，例外表如下；
114	 *  550/588 原版显式列 −4 = 默认值，不重复入表） */
115	export const SITTING_HAT_OFFSET_Y_DEFAULT = -4;
116	export const SITTING_HAT_OFFSET_Y: Record<number, number> = {
117	  38: -8, 124: -2, 108: -6, 178: -6, 637: -12, 663: -8,
118	};
119	/** 坐姿帽 Y 修正取值（Renderer.drawPartyHat 消费） */
120	export function sittingHatY(id: number): number {
121	  return SITTING_HAT_OFFSET_Y[id] ?? SITTING_HAT_OFFSET_Y_DEFAULT;
122	}
123	
124	// ===================== shimmerTransparency（NPC.cs:6112，0..1）=====================
125	export const SHIMMER_ST_RAMP = 0.01;      // 浸微光 +0.01/t（:92469）
126	export const SHIMMER_ST_TRANSFORM = 0.9;  // >0.9 触发 GetShimmered（:92471）
127	export const SHIMMER_ST_RISE = 0.89;      // 城镇转化置 0.89（:92568）
128	export const SHIMMER_ST_DECAY_RISE = 1 / 60;  // ai[0]=25 上升态 −1/60/t（:53625）
129	export const SHIMMER_ST_DECAY_HIT = 0.1;      // justHit −0.1/t（:92484）
130	export const SHIMMER_ST_DECAY_IDLE = 0.001;   // 常规 −0.001/t（:92492）
131	
132	/** shimmerTransparency 每 tick 推进（赋值时序 NPC.cs:92468-92497 + :53625）：
133	 *  浸微光 +0.01 cap 1（rise 态抑制——GetShimmered 已摘除 buff 353（:92570-92573），
134	 *  上升态内 shimmering 恒 false，st 走 −1/60 衰减）；非浸按 justHit/rise/常规
135	 *  三档衰减，下限 0。>0.9 的转化触发由调用方判（见 fixedUpdate 微光块） */
136	export function shimmerTransparencyNext(
137	  st: number, shimmering: boolean, justHit: boolean, rise: boolean,
138	): number {
139	  if (shimmering && !rise) return Math.min(1, st + SHIMMER_ST_RAMP);
140	  const rate = justHit ? SHIMMER_ST_DECAY_HIT : rise ? SHIMMER_ST_DECAY_RISE : SHIMMER_ST_DECAY_IDLE;
141	  return Math.max(0, st - rate);
142	}
143	
144	/** 消费①：本体渐显/渐隐（GetAlpha NPC.cs:94874-94878：CurrentlyShimmerTransparent
145	 *  → 四通道 ×(1−shimmerTransparency)；Renderer 本体 alpha 用） */
146	export function shimmerBodyAlpha(shimmerTransparency: number): number {
147	  return 1 - shimmerTransparency;
148	}
149	
150	/** 消费②：160 松露人微光态 Glow RGB 衰减（Main.cs:25770-25776：case 160 专属，
151	 *  209 无此档）——'lighter' 加性混合下 tint RGB ×(1−st) ≡ alpha ×(1−st) */
152	export function shimmerGlowAlpha(baseAlpha: number, shimmerTransparency: number): number {
153	  return shimmerTransparency > 0 ? baseAlpha * (1 - shimmerTransparency) : baseAlpha;
154	}
155	
156	// ===================== ai[0]=25 微光上升态（NPC.cs:53594-53682）=====================
157	export const SHIMMER_RISE_VELOCITY_TICK = 30;   // ai[1]≥30 起 st 衰减 + 上浮速度（:53621）
158	export const SHIMMER_RISE_END_TICK = 75;        // ai[1]≥75 且 st≤0 → 转化收尾（:53653）
159	export const SHIMMER_RISE_PAUSE = 30;           // 远距落点后 ai[2]=30 暂停（:53604）
160	export const SHIMMER_RISE_TELEPORT_DIST = 560;  // 落点位移 ≥560px 才暂停+发送粒子（:56001）
161	
162	/** Utils.Remap（Utils.cs:313，clamped 默认 true）：fromMin..fromMax 归一后
163	 *  线性映到 toMin..toMax（区间外钳端值） */
164	export function remapClamped(
165	  v: number, fromMin: number, fromMax: number, toMin: number, toMax: number,
166	): number {
167	  const t = fromMax === fromMin ? 0 : (v - fromMin) / (fromMax - fromMin);
168	  return toMin + (Math.max(0, Math.min(1, t))) * (toMax - toMin);
169	}
170	
171	/** Main.IsItStorming（Main.cs:2978 = _shouldUseStormMusic；UpdateWindyDayState
172	 *  :12927-12960 迟滞机，阈值 _minWind 0.34/_maxWind 0.4/_minRain 0.4/_maxRain
173	 *  0.5 见 Main.cs:66137-66140）逐步推进的纯函数：无云恒 false；低雨/低风翻
174	 *  false；高雨(≥0.5)+强风(|w|≥0.4) 翻 true；中间带保持前值（迟滞）。带 prev
175	 *  逐步喂入 ≡ 原版每帧重算的全局字段。remixWorld 强制 false 分支本仓无 remix 世界 */
176	export function isItStormingNext(cloudAlpha: number, windSpeedTarget: number, prev: boolean): boolean {
177	  if (cloudAlpha === 0) return false;
178	  if (cloudAlpha < 0.4 || Math.abs(windSpeedTarget) < 0.34) return false;
179	  if (cloudAlpha >= 0.5 && Math.abs(windSpeedTarget) >= 0.4) return true;
180	  return prev;
181	}
182	
183	// ===================== Boss 击杀进度强化链（AI_007_TownEntities NPC.cs:53400-53557）=====================
184	// num2 = 伤害乘区（先于难度曲线：num = GetAttackDamage_ForTownNPC(num × num2)，
185	// 四攻击态入参 ：54897/:55169/:55319/:55466）；num3 = 攻击频率门除数（:55859
186	// num123=(int)(AttackAverageChance×num3)，钳 ≥1 后 rand(num123)==0）。两者在同一
187	// isLikeATownNPC 块内逐项累计。块内不属本函数的条目：防御档 :53401-53412
188	// （dryadWard +20/15/10 按难度——树妖结界 buff 本仓无载体，hurt 侧防御链另批）、
189	// type==209 num3÷3（:53548，attackUpdate 消费点内联）、对话中 num3×0.8（:55617，
190	// 本仓 talking 恒不入攻击态——触发门 :835 已挡，不可达登记）。
191	/** 进度强化链输入（全 bool；各字段 = 原版静态位/实例位，括注声明行+置位点） */
192	export interface TownNpcProgression {
193	  combatBookWasUsed: boolean;            // NPC.combatBookWasUsed（:6256；书 4382 使用 Player.cs:44710）
194	  combatBookVolumeTwoWasUsed: boolean;   // NPC.combatBookVolumeTwoWasUsed（:6258；书 5336 Player.cs:44723）
195	  downedSlimeKing: boolean;              // NPC.downedSlimeKing（:6270；case 50 event 11 :80217）
196	  downedBoss1: boolean;                  // NPC.downedBoss1（:6262；克眼 4 event 13 :80242）
197	  downedDeerclops: boolean;              // NPC.downedDeerclops（:6314；668 event 25 :80156）
198	  downedBoss2: boolean;                  // NPC.downedBoss2（:6264；世吞/克脑 13/14/15/266 event 14 :80258）
199	  downedBoss3: boolean;                  // NPC.downedBoss3（:6266；骷髅王 35 event 15 :80264）
200	  downedQueenBee: boolean;               // NPC.downedQueenBee（:6268；蜂后 222 event 8 :80188）
201	  hardMode: boolean;                     // Main.hardMode（肉山 113 → WorldGen.StartHardmode :80286）
202	  downedQueenSlime: boolean;             // NPC.downedQueenSlime（:6312；657 event 24 :80159）
203	  downedMechBoss1: boolean;              // NPC.downedMechBoss1（:6340；毁灭者 134 event 16 :80277）
204	  downedMechBoss2: boolean;              // NPC.downedMechBoss2（:6342；双子 125/126 event 17 :80227）
205	  downedMechBoss3: boolean;              // NPC.downedMechBoss3（:6344；Prime 127 event 18 :80270）
206	  downedPlantBoss: boolean;              // NPC.downedPlantBoss（:6280；世花 262 event 12 :80234）
207	  downedEmpressOfLight: boolean;         // NPC.downedEmpressOfLight（:6310；光女 636 event 23 :80153）
208	  downedFishron: boolean;                // NPC.downedFishron（:6286；猪鲨 370 event 7 :80150）
209	  downedGolemBoss: boolean;              // NPC.downedGolemBoss（:6282；石巨人 245 event 6 :80147）
210	  downedAncientCultist: boolean;         // NPC.downedAncientCultist（:6298；拜月教主 439 event 9 :80195）
211	  skyblockLowTiles: boolean;             // WorldGen.Skyblock.lowTiles（WorldGen.cs:3076；天空盒世界扫块率<0.1 置位 :3210-3216）
212	  tipsy: boolean;                        // NPC.tipsy（:6146；buff 25 UpdateNPC_BuffSetFlags :93179）
213	}
214	
215	/** num2/num3 进度强化链 1:1（NPC.cs:53400-53557，仅 isLikeATownNPC 块内条目）。
216	 *  返回 damageMul=num2 / chanceMul=num3。顺序敏感项：Skyblock 的 num3 折半
217	 *  （num3>1 才取 (num3+1)/2，:53542-53545，非乘法）在链中段；tipsy 在链尾
218	 *  乘算（:53555 damage×1.1 / :53556 chance×0.9）。209 的 num3÷3（:53548）
219	 *  在 Skyblock 之后、tipsy 之前——由消费点内联（对乘法项可交换，仅与 Skyblock
220	 *  折半的组合序有差；skyblockLowTiles 本仓恒 false，见 fromWorld 登记） */
221	export function townNpcProgressionBoost(p: TownNpcProgression): { damageMul: number; chanceMul: number } {
222	  let damage = 1;                        // num2 = 1f（:53400）
223	  let chance = 2;                        // num3 = 2f（:53413）
224	  if (p.combatBookWasUsed) {             // :53419-53425（lifeMax+250/防+8 留 hurt 侧）
225	    chance *= 0.8; damage += 0.25;
226	  }
227	  if (p.combatBookVolumeTwoWasUsed) {    // :53426-53432
228	    chance *= 0.8; damage += 0.25;
229	  }
230	  if (p.downedSlimeKing) {               // :53437-53442
231	    chance *= 0.985; damage += 0.05;
232	  }
233	  if (p.downedBoss1) {                   // :53443-53448
234	    chance *= 0.985; damage += 0.05;
235	  }
236	  if (p.downedDeerclops) {               // :53449-53454
237	    chance *= 0.985; damage += 0.1;
238	  }
239	  if (p.downedBoss2) {                   // :53455-53460
240	    chance *= 0.985; damage += 0.1;
241	  }
242	  if (p.downedBoss3) {                   // :53461-53466
243	    chance *= 0.985; damage += 0.1;
244	  }
245	  if (p.downedQueenBee) {                // :53467-53472
246	    chance *= 0.985; damage += 0.1;
247	  }
248	  if (p.hardMode) {                      // :53473-53478（+0.4 最大单项）
249	    chance *= 0.985; damage += 0.4;
250	  }
251	  if (p.downedQueenSlime) {              // :53479-53484
252	    chance *= 0.985; damage += 0.15;
253	  }
254	  if (p.downedMechBoss1) {               // :53485-53490
255	    chance *= 0.985; damage += 0.15;
256	  }
257	  if (p.downedMechBoss2) {               // :53491-53496
258	    chance *= 0.985; damage += 0.15;
259	  }
260	  if (p.downedMechBoss3) {               // :53497-53502
261	    chance *= 0.985; damage += 0.15;
262	  }
263	  if (p.downedPlantBoss) {               // :53503-53508
264	    chance *= 0.985; damage += 0.15;
265	  }
266	  if (p.downedEmpressOfLight) {          // :53509-53514
267	    chance *= 0.985; damage += 0.15;
268	  }
269	  if (p.downedFishron) {                 // :53515-53520
270	    chance *= 0.985; damage += 0.15;
271	  }
272	  if (p.downedGolemBoss) {               // :53521-53526
273	    chance *= 0.985; damage += 0.15;
274	  }
275	  if (p.downedAncientCultist) {          // :53527-53532（防 +20 最大防御项）
276	    chance *= 0.985; damage += 0.15;
277	  }
278	  if (p.skyblockLowTiles) {              // :53540-53547（netMode!=1 单机恒过）
279	    if (chance > 1) chance = (chance + 1) / 2;
280	    damage += 0.5;
281	  }
282	  if (p.tipsy) {                         // :53552-53557（链尾乘算）
283	    damage *= 1.1; chance *= 0.9;
284	  }
285	  return { damageMul: damage, chanceMul: chance };
286	}
287	
288	/** world.flags → 进度强化链输入。Boss 旗标本仓 = Game Boss 槽击杀通用记账
289	 *  `downed_<vanillaId>`（Game.ts 击败链，双子归一 125；世吞归一 13/克脑 266），
290	 *  与 Game.shopCondOk 同源键序；旧档/导入别名（downedEyeOfCthulhu/downedSkeletron/
291	 *  downedSlimeKing）双读。恒 false 两项 = 精确登记非近似：
292	 *  - skyblockLowTiles：WorldGen.Skyblock.ScanTiles 只在世界装载时跑一次
293	 *    （WorldFile.cs:771），活跃块率 <0.1 且 skyblockWorld 才置（WorldGen.cs
294	 *    :3210-3216）。本仓无 skyblock 世界生成链（sf.skyblock 仅拒绝墓园 pass,
295	 *    生成的是常规满图世界 >10%），WldParser 导入亦不保留该位 → 本仓可产的
296	 *    任何世界恒 false,不可拿 seedFlags.skyblock 近似；
297	 *  - tipsy：NPC 实例位非世界旗标（buff 25,:93179）——本函数恒 false,由消费点
298	 *    （attackUpdate 触发门 / swingUpdate / shootAt）按 this.tipsy 覆盖；施加链
299	 *    = 麦酒弹 669 Kill 爆炸（TownShot.kill669,Projectile.cs:68725-68734） */
300	export function townNpcProgressionFromWorld(world: {
301	  flags: Record<string, boolean>;
302	}): TownNpcProgression {
303	  const f = world.flags;
304	  return {
305	    combatBookWasUsed: !!f.combatBookWasUsed,
306	    combatBookVolumeTwoWasUsed: !!f.combatBookVolumeTwoWasUsed,
307	    downedSlimeKing: !!(f['downed_50'] || f.downedSlimeKing),
308	    downedBoss1: !!(f['downed_4'] || f.downedEyeOfCthulhu),
309	    downedDeerclops: !!f['downed_668'],
310	    downedBoss2: !!(f['downed_13'] || f['downed_266']),
311	    downedBoss3: !!(f['downed_35'] || f.downedSkeletron),
312	    downedQueenBee: !!f['downed_222'],
313	    hardMode: !!f.hardMode,
314	    downedQueenSlime: !!f['downed_657'],
315	    downedMechBoss1: !!f['downed_134'],
316	    downedMechBoss2: !!(f['downed_125'] || f['downed_126']),
317	    downedMechBoss3: !!f['downed_127'],
318	    downedPlantBoss: !!f['downed_262'],
319	    downedEmpressOfLight: !!f['downed_636'],
320	    downedFishron: !!f['downed_370'],
321	    downedGolemBoss: !!f['downed_245'],
322	    downedAncientCultist: !!f['downed_439'],
323	    skyblockLowTiles: false,
324	    tipsy: false,
325	  };
326	}
327	
328	export class TownNPC extends Entity {
329	  w = 20; h = 42;
330	  stepUp = true;
331	  stepUpHolds = true; stepUpNpc = true;   // holdsMatching + IgnoredByNpcStepUp（NPC.cs:54382 flag22 恒 true） // 原版 NPC 全体走 Collision.StepUp（NPC.cs:54382）
332	  npcKey: string; // 'guide'
333	  /** 原版 NPCID（TOWN_NPC_IDS；Renderer 经 atlas.vnpc 取 NPC_{id}.png 贴图条） */
334	  vanillaId: number;
335	  facing = 1;
336	  /** 随机名字（NPC.getNewNPCNameInner 名字池；无池类型如守卫老人为空串） */
337	  givenName = '';
338	  animT = 0;
339	  frame = 0;       // 当前贴图帧（原版 frame.Y/帧高）
340	  frameT = 0;      // 行走帧累加器（≈原版 frameCounter）
341	  wanderT = 0;
342	  home: NpcHome | null = null;
343	  /** 定点站岗（守卫老人）：门口地带是山坡+塔心竖井,白天的自由游走会坠入地牢；
344	   *  原版观感也是整日守在门口走廊 */
345	  stationary = false;
346	  /** 被绑待救援（原版为独立 NPC 类型：BoundGoblin105/BoundWizard106/BoundMechanic123/
347	   *  WebbedStylist354/GolferRescue589，本作以本标记近似；渲染按真帧走各捆绑姿态表——
348	   *  Renderer.BOUND_NPC_SHEET。原地不动，右键解救 → savedXxx 旗标置位成为正式城镇 NPC） */
349	  bound = false;
350	  // ---- NPC 开关门（原版 AI_007，NPC.cs:54478 开门 / 54243 过门关门）----
351	  private closeDoor = false;
352	  private doorX = 0; private doorY = 0;
353	  /** 白天游走但不远离 home(守卫老人:锚地牢门口走廊,防走失) */
354	  leashHome = false;
355	  /** 正在与玩家对话（原版 AI_007 :53721：talkNPC==本体 → ai[0]=0 站定、面向玩家） */
356	  talking = false;
357	  talkCooldown = 0;
358	  /** 微光化变体 = townNpcVariationIndex==1（NPCID.Sets.ShimmerTownTransform 入
359	   *  微光 → GetShimmered :92561-92573 → ai[0]=25 上升态；上升收尾 :53664 翻转——
360	   *  **双向**：已微光化再浸微光翻转回原形态）。变体贴图经 townSheet getter 切
361	   *  TownNPCs/Shimmered 档（Profiles.StackedNPCProfile 档位 1），对话差分登记 GAP */
362	  shimmered = false;
363	  /** 当前 altTexture（UpdateAltTexture NPC.cs:91254-91273：1=派对 2=狼人；
364	   *  fixedUpdate 每 tick 由 townNpcAltTexture 刷新——月相/血月/派对随时翻态） */
365	  altTexture = 0;
366	  // ---- 坐姿（AI_007 ai[0]==5，NPC.cs:53264-53287 入座 / :54682-54710 态推进）----
367	  /** 正坐在椅/马桶上（ai[0]==5）。仅夜/雨"该回家"窗口（flag，:53383-53402）入座：
368	   *  FindGoodRestingSpot 扫 home 附近可坐格 → 走到/传送落到落座格 → TryForcingSitting。
369	   *  渲染消费：drawPartyHat 坐姿帽 Y 链（sittingHatY）+ hatStateOffsetX 的 550 档 */
370	  sitting = false;
371	  /** ai[1] 坐姿倒计时（入座 = 900+rand(10800)，:53283） */
372	  private sitTimer = 0;
373	  /** 本 tick 的夜椅 rest spot（FindGoodRestingSpot 缓存；白天/无 home = null） */
374	  private restSpot: SitSpot | null = null;
375	  /** 本 tick 刚走"回家传送"（TeleportToHome :56063-56090 落位后即
376	   *  TryForcingSitting :56081——免"站定+同格"门，:54074 门只管走到场的情形） */
377	  private teleportedHome = false;
378	  /** 微光转化透明度（NPC.cs:6112，0..1；赋值时序 :92468-92497/:92568/:53625）。
379	   *  消费：Renderer 本体 alpha=1−st（GetAlpha :94874）+ 160 Glow ×(1−st)
380	   *  （Main.cs:25771-25776）——微光转化渐显/渐隐的唯一驱动字段 */
381	  shimmerTransparency = 0;
382	  /** 微光上升态旗标（原版 ai[0]==25，NPC.cs:53594-53682：落点传送 → ai[1]≥30
383	   *  起 −1/60/t 衰减 + velocity.Y=−4×st 上浮 → st 归零后翻转变体 + 到场粒子 +
384	   *  成就 43；态内 dontTakeDamage——推进见 shimmerRiseUpdate） */
385	  private shimmerRise = false;
386	  /** ai[1]：上升态计时（0 起，暂停期外每 tick +1；浸液钳 30） */
387	  private shimmerRiseT = 0;
388	  /** ai[2]：远距落点传送后的暂停倒计时（:53604） */
389	  private shimmerRisePause = 0;
390	  /** Main.IsItStorming 缓存（isItStormingNext 逐步推进；坐姿/回家 flag 消费） */
391	  private storming = false;
392	  /** ai[0]==25 上升态只读（渲染/测试消费） */
393	  get shimmerRising(): boolean { return this.shimmerRise; }
394	
395	  /** 生命（原版城镇 NPC 可被陷阱弹幕误伤：vanilla-npcs.json lifeMax 250 / defense 15） */
396	  hp: number;
397	  maxHp: number;
398	  iframes = 0;
399	  // ---- 自卫攻击（AI_007 攻击态 ai[0]=10/12/14/15,NPC.cs:54747-55538）----
400	  /** 当前攻击态(0 空闲 / 10 近战弹 / 12 弓 / 14 魔法 / 15 挥击) */
401	  private atkState = 0;
402	  /** ai[0] 攻击态只读（AI_007 :54747 起的 10/12/14/15；原版同值）——渲染侧消费：
403	   *  drawPartyHat 海盗帽位修正（Main.cs:27001-27008 的 229 ai[0]==12 门）。
404	   *  坐姿 ai[0]==5 由 sitting 布尔建模（渲染侧 n.sitting?5:attackState 还原 ai0）；
405	   *  二者互斥：坐姿不满足攻击触发门 flag31 的 ai[0]<2（:55621），攻击态中不入座 */
406	  get attackState(): number { return this.atkState; }
407	  /** ai[2] 持械瞄准值（DrawNPCExtras :27121 消费 = 武器旋转 ai[2]×90°×朝向；
408	   *  :55191-55197 发射档取目标方向 Y 钳 ±0.5，态尽归零）——弓族攻击态持械绘制用 */
409	  get holdoutAim(): number { return this.holdAim; }
410	  /** world.flags.hardMode 缓存（攻击Update 每 tick 刷新）——持械表 pre/hm 选档用 */
411	  get hardMode(): boolean { return this.hardModeFlag; }
412	  /** ai[2]：弓族发射档写入，其余恒 0 */
413	  private holdAim = 0;
414	  /** ai[1]:态倒计时(AttackTime) */
415	  private atkTimer = 0;
416	  /** localAI[1]:触发冷却(flag31 门) */
417	  private atkCd = 0;
418	  /** localAI[3]:态内 tick 计数 */
419	  private atkTick = 0;
420	  /** 当前发射档 num46/55/65(连发升级链推进) */
421	  private atkNextShot = 0;
422	  private atkBurstIdx = 0;
423	  /** world.flags.hardMode 缓存(attackUpdate 每 tick 刷新) */
424	  private hardModeFlag = false;
425	  /** 633 狼人态缓存(attackUpdate 每 tick 刷新,ShouldBestiaryGirlBeLycantrope
426	   *  NPC.cs:94961-94972:血月夜或满月[moonPhase==0]夜)——发射端换 proj 929 +
427	   *  dmg×1.5 截断(:54782-54785) */
428	  private werewolfFlag = false;
429	  // 表情气泡:字段/掷骰已退役——统一走 render/EmoteBubble 模块(spawnEmote,
430	  // 并行会话 1:1 版);空闲随机冒泡由 Game.tickNpcEmotes 窗口喂(双画修复 2026-08-13)
431	  // ---- 环境与互殴受击(NPC.cs :91538 族调用点的三件套)----
432	  /** 岩浆专属冷却(原版 immune[255]=30,Collision_LavaCollision :94522) */
433	  private lavaCd = 0;
434	  /** NPC 互殴专属冷却(原版 immune[255]=30,GetHurtByOtherNPCs :93667;初始 0) */
435	  private npcVsCd = 0;
436	  /** 溺水呼吸(NPC.CheckDrowning :96118:初始 200,水内每 7t -1,离水 +3/t) */
437	  private breath = 200;
438	  private breathCounter = 0;
439	
440	  constructor(key: string, x: number, y: number) {
441	    super();
442	    this.npcKey = key;
443	    this.x = x;
444	    this.y = y - this.h;
445	    const town = TOWN_NPC_IDS[key];
446	    this.vanillaId = town?.id ?? 22; // 未登记 key 兜底向导贴图
447	    this.givenName = newNpcName(this.vanillaId);
448	    const v = VANILLA_NPCS[String(this.vanillaId)];
449	    this.maxHp = this.hp = v?.lifeMax ?? 250;
450	  }
451	
452	  /** 被陷阱弹幕等命中：dmg - defense*0.5（下限 1），8 tick 无敌帧；
453	   *  死亡即移除——"重生"由入驻轮承担（原版 UpdateTime_SpawnTownNPCs：不在场且
454	   *  条件满足 → 重新入驻，≈次日回归），无需独立重生系统 */
455	  hurt(dmg: number, kbx: number, _kby: number, game: GameHooks): boolean {
456	    if (this.iframes > 0 || this.dead) return false;
457	    if (this.shimmerRise) return false;   // ai[0]==25 dontTakeDamage（NPC.cs:53596）
458	    const books = (game.world.flags.combatBookWasUsed ? 1 : 0) + (game.world.flags.combatBookVolumeTwoWasUsed ? 1 : 0);
459	    const def = (VANILLA_NPCS[String(this.vanillaId)]?.defense ?? 15) + books * 8; // NPC.cs:53419
460	    dmg = Math.max(1, Math.round(dmg - def * 0.5));
461	    this.hp -= dmg;
462	    this.iframes = 8;
463	    game.addDamageNumber(this.cx, this.y, dmg, false, '#FFD060');
464	    // 受击血粒子(原版 StrikeNPC 尘近似,与 Enemy.hurt 同规)
465	    game.spawnParticles(this.cx, this.cy, '#B01818', 5, 1.4, { life: 22, grav: 0.06 });
466	    this.vx += kbx * 0.6;
467	    if (this.hp <= 0) {
468	      this.dead = true;
469	      game.spawnParticles(this.cx, this.cy, '#C03030', 8, 2);
470	      game.spawnParticles(this.cx, this.cy, '#8A1818', 4, 1.2);
471	      game.playSfxFiles(['NPC_Killed_1'], 0.8);
472	    } else {
473	      game.playSfxFiles(['NPC_Hit_1'], 0.6);
474	    }
475	    return true;
476	  }
477	
478	  /** 战斗书增益（NPC.cs:53419-53430：每本 lifeMax+250 / 伤害出力×0.8 / 移速+0.25 /
479	   *  防+8——伤害/移速两项无对应战斗系统，落 lifeMax/防；每本可叠加，由调用方按旗标次数调） */
480	  applyCombatBook(): void {
481	    this.maxHp += 250;
482	    this.hp = Math.min(this.maxHp, this.hp + 250);
483	  }
484	
485	  private cbApplied = false;
486	
487	  /** buff 25 Tipsy 剩余 tick（NPC.buffType/buffTime 单槽近似——本仓城镇 NPC 无
488	   *  buff 栏,只为 num2 链建此单槽）。唯一施加点 = 麦酒弹 669 Kill 爆炸
489	   *  （Projectile.cs:68725-68734 AddBuff(25, 3659),酒馆老板 550 自卫投掷,
490	   *  TownShot.kill669 落点）;每 tick 递减（NPC.cs:93174 lowerBuffTime）,归零
491	   *  即失效（:93333 整段重置）。消费:进度链 tipsy 位（num2×1.1/num3×0.9 链尾
492	   *  :53552-53557）+ 醉酒气泡金尘（:92349 rand(4)==0 且 rand(2)==0 → 净 1/8） */
493	  tipsyT = 0;
494	
495	  /** NPC.AddBuff(25, ticks)（同 buff 合并取更长剩余——标准 buffTime 合并语义） */
496	  applyTipsy(ticks: number): void {
497	    if (ticks > this.tipsyT) this.tipsyT = ticks;
498	  }
499	
500	  /** 本 tick 的 NPC.tipsy 位（:93179 buff25 在列 → true）。快照语义：原版
501	   *  递减（:93174）后置位——剩余 1t 的最后一 tick 仍 true,次 tick 才 false */
502	  private tipsyNow = false;
503	
504	  get tipsy(): boolean { return this.tipsyNow; }
505	
506	  /** GetMagicAuraColor（NPC.cs:53317-53332）1:1：NPCID.Sets.MagicAuraColor
507	   *  （NPCID.cs:4853）五人恰好 = AttackType-2 魔法攻击族（54 裁缝/108 巫师/
508	   *  160 松露/20 树妖/663 公主；五人 TownNPCProfiles 全走 LegacyWithSimpleShimmer
509	   *  二档 StackedNPCProfile → variationIndex∈{0,1}，==1 ⟺ 微光变体）。
510	   *  townNpcVariationIndex==1（= 本仓 shimmered，IsShimmerVariant NPC.cs:6646-6650）
511	   *  → 160 R/B 互换、20 固定 (90,20,210)、663 固定 (255,0,77)。Color.ToVector3()
512	   *  丢弃 alpha → 三通道 0-1 归一（663 基色 = Main.hslToRgb(0.92,1,0.78) = 255,143,197）*/
513	  private magicAuraColor(): [number, number, number] {
514	    switch (this.vanillaId) {
515	      case 54: return [100 / 255, 4 / 255, 227 / 255];
516	      case 108: return [1, 80 / 255, 60 / 255];
517	      case 160: return this.shimmered ? [1, 80 / 255, 40 / 255] : [40 / 255, 80 / 255, 1];
518	      case 20: return this.shimmered ? [90 / 255, 20 / 255, 210 / 255] : [40 / 255, 1, 80 / 255];
519	      case 663: return this.shimmered ? [1, 0, 77 / 255] : [1, 143 / 255, 197 / 255];
520	      default: return [1, 1, 1];        // 集合缺省 Color.White（ToVector3 丢 alpha）
521	    }
522	  }
523	
524	  /** 本 tick 点光（NPC.cs 城镇 NPC 侧三处恒亮）：
525	   *  - 160 松露（UpdateNPC_CastLights :93544-93566）：num3=Next(28,42)×0.005+
526	   *    (270−mouseTextColor)/500，基色 (0.1,0.3+num3/2,0.6+num3)×0.35；变体 1
527	   *    （townNpcVariationIndex==1）R/B 互换——以 shimmered 承接（:93563-93567）
528	   *  - 209 电子人（:93590-93599）：同式抖动 ×0.35、B 基 0.4；ai[0]==12（火箭射击
529	   *    态，AttackType[209]=1 → ai0=12，NPC.cs:55902/:54936）追加 Top (0.3,0.1,0.1)
530	   *    （:93594-93596）——单槽逐通道 max 合并（Enemy.mergeLightRGB 同款近似）
531	   *  - 681 彩虹城镇史莱姆（AI_007 尾段 :55963-55974）= TorchColor(23)×0.35
532	   *  - 683 黄城镇史莱姆（:55974-55979）= (0.25,0.25,0.1)×WrappedLerp(0.75,1,t%120/120)
533	   *  条件态：魔法光环 ai[0]==14（:55394，num69=1 恒满档，atkState===14 承接）
534	   *  ×GetMagicAuraColor；微光上升光 :53637（ai[1] 30→90，shimmerRise 态内已接）；
535	   *  跳过一处——:55546 ai[0]==24（树妖 Stardew 演出 HaveDryadDoStardewAnimation
536	   *  :19123，公主礼物彩蛋无载体） */
537	  get lightRGB(): [number, number, number] | null {
538	    let rgb: [number, number, number] | null = null;
539	    // 逐通道 max 合并（原版同帧多 AddLight，单槽近似视觉并集；不挪光源位）
540	    const merge = (c: [number, number, number]) => {
541	      rgb = rgb ? [Math.max(rgb[0], c[0]), Math.max(rgb[1], c[1]), Math.max(rgb[2], c[2])] : c;
542	    };
543	    if (this.vanillaId === 160) {
544	      const n3 = (28 + Math.random() * 14) * 0.005 + (270 - mouseTextColorApprox()) / 500;
545	      const base: [number, number, number] = [0.1 * 0.35, (0.3 + n3 / 2) * 0.35, (0.6 + n3) * 0.35];
546	      // :93563-93567 变体 1（shimmered）→ R/B 互换（num7 交换 num4/num6）
547	      merge(this.shimmered ? [base[2], base[1], base[0]] : base);
548	    }
549	    if (this.vanillaId === 209) {
550	      const n3 = (28 + Math.random() * 14) * 0.005 + (270 - mouseTextColorApprox()) / 500;
551	      merge([0.1 * 0.35, (0.3 + n3 / 2) * 0.35, (0.4 + n3 / 2) * 0.35]);
552	      if (this.atkState === 12) merge([0.3, 0.1, 0.1]);   // :93594 火箭射击态 Top 追加光
553	    }
554	    if (this.vanillaId === 681) {
555	      const num = Math.min(1, Math.max(0, 0.9 + (270 - mouseTextColorApprox()) / 900));
556	      merge([num * 0.9 * 0.35, 0.55 * 0.35, num * 1.2 * 0.35]);   // TorchColor(23)×0.35
557	    }
558	    if (this.vanillaId === 683) {
559	      const p = (visEffectFrames() % 120) / 120;
560	      const tri = p * 2 > 1 ? 2 - p * 2 : p * 2;                   // Utils.WrappedLerp
561	      const l = 0.75 + 0.25 * tri;
562	      merge([0.25 * l, 0.25 * l, 0.1 * l]);
563	    }
564	    // 魔法光环（:55390-55396）：ai[0]==14 魔法攻击态内 num69=1 恒满档 → GetMagicAuraColor
565	    if (this.atkState === 14
566	      && (this.vanillaId === 54 || this.vanillaId === 108 || this.vanillaId === 160
567	        || this.vanillaId === 20 || this.vanillaId === 663)) {
568	      merge(this.magicAuraColor());
569	    }
570	    // 微光上升光（:53637-53639）：Center 处 hslToRgb(t/360%1, 0.6, 0.65) ×
571	    // Remap(ai[1],30,90,0,0.7)——Remap 钳位使 ai[1]<30 时恒 0（无光）
572	    if (this.shimmerRise) {
573	      const k = remapClamped(this.shimmerRiseT, SHIMMER_RISE_VELOCITY_TICK, 90, 0, 0.7);
574	      const c = hslToRgb((visEffectFrames() / 360) % 1, 0.6, 0.65);
575	      merge([c[0] * k, c[1] * k, c[2] * k]);
576	    }
577	    return rgb;
578	  }
579	  lightRGBAt: { x: number; y: number } | null = null;
580	
581	  fixedUpdate(dt: number, game: GameHooks) {
582	    this.animT++;
583	    // justHit 近似（原版逐 tick 旗标）：hurt() 置 iframes=8 且只在无无敌帧时生效
584	    // → 递减前 ==8 恰好标记"自上 tick 起受过击"（微光衰减 −0.1 档 NPC.cs:92484）
585	    const justHit = this.iframes === 8;
586	    if (this.iframes > 0) this.iframes--;
587	    // buff 25 Tipsy 递减（NPC.cs:93174 lowerBuffTime,UpdateNPC 每 tick 头部）+
588	    // 醉酒气泡金尘（:92349-92370：rand(4)==0 且 rand(2)==0 → 净 1/8,尘 4
589	    // 金 (245,200,30,155) alpha 75(+25×2 随机档) scale 0.9,vel×0.2 后 +0.2 下沉）
590	    if (this.tipsyT > 0) {
591	      // :93170 顶部守卫 time>0 → :93174 递减 → :93179 置位（递减后仍按本 tick 生效）
592	      this.tipsyNow = true;
593	      this.tipsyT--;
594	      if (Math.random() < 1 / 8) {
595	        game.spawnParticles(this.x - 2, this.y - 2, 'rgba(245,200,30,0.61)', 1, 0.3,
596	          { life: 40, grav: 0.005, size: 2 });
597	      }
598	    } else {
599	      this.tipsyNow = false;   // :93333 整段重置
600	    }
601	    this.teleportedHome = false;
602	    const world = game.world;
603	    // 战斗书增益一次性套用（后入驻的 NPC 在首 tick 补；使用书时对在场者即时叠）
604	    if (!this.cbApplied) {
605	      this.cbApplied = true;
606	      const books0 = (world.flags.combatBookWasUsed ? 1 : 0) + (world.flags.combatBookVolumeTwoWasUsed ? 1 : 0);
607	      for (let k = 0; k < books0; k++) this.applyCombatBook();
608	    }
609	
610	    // ---- 城镇微光转化链 1:1（GetShimmered NPC.cs:92561-92573 + AI_007 ai[0]==25
611	    //      :53594-53682）。触发：浸微光 st +0.01/t（:92469），>0.9 → GetShimmered
612	    //      （:92471，约 91t 渐隐非即刻）；城镇分支置 st=0.89 并进 ai[0]=25 上升态
613	    //      （:92562-92568，摘 buff 353 :92570-92573——城镇 buff 系统未建，无载体）。
614	    //      上升态 = 落点传送 → ai[1]≥30 起 −1/60/t 衰减 + velocity.Y=−4×st 上浮 →
615	    //      st 归零后翻转微光变体 + 到场粒子 + 成就 43（推进见 shimmerRiseUpdate）。
616	    //      变体贴图走 townSheet getter（已接），对话差分未接（GAP）。
617	    //      注：原版 UpdateNPC_BuffApplyVFX（:92492）上升态外仍每 tick −0.001 共衰减，
618	    //      本仓并入 −1/60 单档（既有 shimmerTransparencyNext 模型，纯函数测试锁定）----
619	    const st0 = world.store;
620	    const si = st0.idx(
621	      Math.max(0, Math.min(st0.w - 1, Math.floor(this.cx / TILE))),
622	      Math.max(0, Math.min(st0.h - 1, Math.floor(this.cy / TILE))),
623	    );
624	    const inShimmer = st0.liquid[si] > 30 && st0.liquidType[si] === 4;
625	    // 上升态内 st 由 shimmerRiseUpdate 独占推进（ai[1]<30 期间原样保持 0.89）
626	    if (!this.shimmerRise) {
627	      this.shimmerTransparency = shimmerTransparencyNext(
628	        this.shimmerTransparency, inShimmer, justHit, false,
629	      );
630	      if (isNpcTownShimmerable(this.vanillaId) && inShimmer
631	        && this.shimmerTransparency > SHIMMER_ST_TRANSFORM) {
632	        this.shimmerRise = true;                    // ai[0]=25（:92562）
633	        this.shimmerRiseT = 0;                      // ai[1]=0（:92563）
634	        this.shimmerRisePause = 0;                  // ai[2]=0（:92564）
635	        this.shimmerTransparency = SHIMMER_ST_RISE; // :92568
636	      }
637	    }
638	    if (this.shimmerRise && this.shimmerRiseUpdate(world, game, st0.liquid[si] > 0)) {
639	      // ai[0]==25 块整段 return（:53682）：AI_007 游走/坐姿/攻击/开门全跳过；
640	      // 只补 UpdateNPC 尾段的重力 + 碰撞 + 找帧（:91521-91565，AI() 之后照常执行）
641	      this.vy = Math.min(this.vy + GRAVITY, MAX_FALL_SPEED);
642	      moveAndCollide(this, world, this.vx, this.vy);
643	      this.updateWalkFrame();
644	      return;
645	    }
646	
647	    // ---- altTexture 刷新（UpdateAltTexture NPC.cs:91254-91273，原版 UpdateNPC 每
648	    //      tick 末尾调 :91358）：派对进行（441/453/633 除外）→ 1；633 狼人条件 → 2。
649	    //      partyUp 取 world.scene（Game 每 15t 写入）；MakeTransitionEffectsForTextureChanges
650	    //      的变身尘/烟粒子（:91277-91309）未接（登记） ----
651	    this.altTexture = townNpcAltTexture(
652	      this.vanillaId, !!world.scene?.partyUp,
653	      world.clock.moonPhase, world.clock.bloodMoon, world.clock.isDay,
654	    );
655	
656	    // 被绑待救援：原地不动（仅重力落定），解救在 Game.talkToNearbyNpc / 净化粉
657	    // （原版 bound 类型同走 TargetClosest + spriteDirection，NPC.cs:19813-19816：
658	    //  恒面向最近玩家——捆绑姿态转向救援者）
659	    if (this.bound) {
660	      const bp = (game as unknown as { player: Player }).player;
661	      if (bp && !bp.dead) this.facing = bp.cx < this.cx ? -1 : 1;
662	      this.vx = 0;
663	      this.vy = Math.min(this.vy + GRAVITY, MAX_FALL_SPEED);
664	      moveAndCollide(this, world, this.vx, this.vy);
665	      return;
666	    }
667	
668	    // ---- 夜椅 rest spot（AI_007_FindGoodRestingSpot NPC.cs:53195-53262，原版
669	    //      每 tick 开头算一次 :53708）：夜/雨"该回家"窗口（flag :53383-53402，与
670	    //      回家传送同式）+ **夜间**才扫椅（:53209 dayTime 早退——白天雨天也只回
671	    //      home 地面不坐）；以 home 为锚扫 ±7 列可坐格；城镇宠物/史莱姆不坐
672	    //      （:53214 type 638/656 + IsTownSlime 族 NPCID.cs:4446）→ 本仓 null ----
673	    // 风暴门（:53399-53402）：Main.IsItStorming 且 NPC 头顶行 < worldSurface
674	    // （= world.groundLevel，SceneMetrics 同源；缺省 0=未知世界恒 false）。迟滞机
675	    // 每 tick 逐步推进（原版 Main 全局字段 _shouldUseStormMusic 逐帧重算）
676	    this.storming = isItStormingNext(world.weather.cloudAlpha, world.weather.windSpeedTarget, this.storming);
677	    const sitFlag = world.weather.raining || !world.clock.isDay
678	      || !!world.clock.eclipse || !!world.weather.slimeRain
679	      || (this.storming && this.y / TILE < world.groundLevel);
680	    this.restSpot = (sitFlag && !world.clock.isDay && this.home
681	      && !NO_SIT_NPC_IDS.has(this.vanillaId))
682	      ? findChairSpot(world.store, this.home.x, this.home.y) : null;
683	
684	    let wantDir = 0;
685	    // 对话中站定并面向玩家（原版 AI_007 NPC.cs:53721-53742：talkNPC==本体 →
686	    // ai[0]=0 停走、ai[1]=300、direction 指向玩家——杜绝"聊着聊着走开丢对话"）
687	    if (this.talking) {
688	      const p = (game as unknown as { player: Player }).player;
689	      if (p) this.facing = p.cx < this.cx ? -1 : 1;
690	      // 对话打断坐姿（:53738：非攻击态被 talkNPC 命中 → ai[0]=5 归 0——玩家
691	      // 靠近说话即起身；ai[1]=300/localAI[3]=100 两计时由既有 wanderT 链近似）
692	      if (this.sitting) { this.sitting = false; this.sitTimer = 0; }
693	      this.vx *= 0.6;
694	      this.wanderT = 0;
695	    } else if (!this.stationary && world.clock.isDay && !this.sitting) {
696	      // 坐姿中不参与白天游走的随机转向（原版 ai[0]==5 不走 :54119+ 的
697	      // idle 翻向链——坐姿朝向由椅子 frameX 锁定）
698	      // 白天家门口附近游走;leashHome 者离 home 超过 ~10 格时折返(守卫老人不离地牢)
699	      if (this.leashHome && this.home
700	        && Math.abs(this.cx - (this.home.x * TILE + 8)) > 10 * TILE) {
701	        wantDir = Math.sign(this.home.x * TILE + 8 - this.cx);
702	      } else {
703	        this.wanderT--;
704	        if (this.wanderT <= 0) {
705	          this.wanderT = 90 + Math.random() * 180;
706	          this.facing = Math.random() < 0.5 ? -1 : 1;
707	          if (Math.random() < 0.35) this.facing = 0;
708	        }
709	        wantDir = this.facing;
710	      }
711	    } else if (this.home) {
712	      // 夜间回家（AI_007 :54060-54106：落位目标 = FindGoodRestingSpot 的 rest
713	      // spot——夜里即椅/马桶的落座地面格，走到即坐；无椅回退 home 列。有椅时
714	      // 收紧停走阈到 4px（原版按 num6==floorX 逐格对齐，:54074），保证落进同格
715	      // 触发坐姿站定门）
716	      const tx = this.restSpot ? this.restSpot.x : this.home.x;
717	      const dx = tx * TILE + 8 - this.cx;
718	      if (Math.abs(dx) > (this.restSpot ? 4 : TILE)) wantDir = Math.sign(dx);
719	    }
720	    // ---- 回家传送（AI_007_TownEntities_TeleportToHome :56063-56086 + 触发 :53828-53856）：
721	    //  flag = 雨天||夜间||日食||史莱姆雨（= 该回家的状态）；且当前不在家休息位；
722	    //  双矩形视野门（玩家屏±safeRange 不与 NPC 位置/home 位置相交）→ 静默传回家
723	    //  （无 dust 无音效，纯 position 改写）。本仓"好休息位"近似=家 ±4 格内 ----
724	    if (this.home) {
725	      const flag = sitFlag;
726	      // IsInAGoodRestingSpot（NPC.cs:53165-53177）：夜间坐姿放宽 ±7 格（:53168-
727	      // 53176——防"坐在椅上被回家传送拽起"）；常态沿用 home ±4 格既有近似。
728	      // 本仓 home.y 是站格（地面行 −1），±7 容差吸收该 1 行口径差
729	      const nearHome = this.sitting
730	        ? Math.abs(Math.floor(this.cx / TILE) - this.home.x) <= 7
731	          && Math.abs(Math.floor((this.y + this.h) / TILE) - this.home.y) <= 7
732	        : Math.abs(this.cx - (this.home.x * TILE + 8)) < 4 * TILE
733	          && Math.abs(this.cy - (this.home.y * TILE)) < 4 * TILE;
734	      if (flag && !nearHome) {
735	        const pl = (game as unknown as { player: { x: number; y: number; w: number; h: number; dead: boolean } | null }).player;
736	        const screenR = 42 * TILE;   // 屏幕半宽+safeRange 近似（1360/16/2×1.52≈64? 取保守值 42 格=见不到）
737	        const farFromNpc = !pl || pl.dead
738	          || Math.hypot(pl.x + pl.w / 2 - this.cx, pl.y + pl.h / 2 - this.cy) > screenR;
739	        const homePx = { x: this.home.x * TILE + 8, y: this.home.y * TILE };
740	        const farFromHome = !pl || pl.dead
741	          || Math.hypot(pl.x + pl.w / 2 - homePx.x, pl.y + pl.h / 2 - homePx.y) > screenR;
742	        if (farFromNpc && farFromHome) {
743	          // 三列落位（:56066-56085：home-1/home/home+1，头顶净空即收；全堵=放弃）
744	          let moved = false;
745	          for (const off of [0, -1, 1]) {
746	            const hx = this.home.x + off, hy = this.home.y;
747	            let clear = true;
748	            for (let ax = hx - 1; ax <= hx + 1 && clear; ax++) {
749	              for (let ay = hy - 3; ay <= hy - 1; ay++) {
750	                if (world.store.inBounds(ax, ay) && world.store.isSolid(ax, ay)) { clear = false; break; }
751	              }
752	            }
753	            if (!clear) continue;
754	            this.x = hx * TILE + 8 - this.w / 2;
755	            this.y = hy * TILE - this.h - 0.1;
756	            this.vx = 0; this.vy = 0;
757	            moved = true;
758	            break;
759	          }
760	          // 落位即试坐（TeleportToHome → TryForcingSitting :56081）
761	          if (moved) this.teleportedHome = true;
762	        }
763	      }
764	    }
765	
766	    // ---- 坐姿（ai[0]==5 族，见 sittingUpdate 注）----
767	    if (this.sittingUpdate(world, game)) wantDir = 0;
768	
769	    // ---- 自卫攻击（AI_007 攻击态 ：54747-55538;攻击中站定替代游走）----
770	    if (this.attackUpdate(world, game)) wantDir = 0;
771	
772	    // ---- 环境与互殴受击(NPC.cs:91534-91544:townNPC 每帧 CheckDrowning +
773	    //      GetHurtByOtherNPCs;岩浆走 Collision_LavaCollision :94511-94530)----
774	    this.envHurtUpdate(world, game);
775	
776	
777	    this.vx += wantDir * 0.06;
778	    this.vx = Math.max(-0.8, Math.min(0.8, this.vx));
779	    if (wantDir === 0) {
780	      // 原版驻留刹车（NPC.cs:54096-54106）：不走路时每 tick ±0.1 主动减速。
781	      // 缺此刹车时 facing=0（站立意图）仍以 0.8px/tick 惯性滑行且贴图不镜像
782	      // → 向右滑行显示朝左贴图（偶发"太空步"）
783	      if (this.vx > 0.1) this.vx -= 0.1;
784	      else if (this.vx < -0.1) this.vx += 0.1;
785	      else this.vx = 0;
786	    }
787	    if (this.onGround && this.hitWall && wantDir !== 0) this.vy = -6; // 跳台阶
788	    this.vy = Math.min(this.vy + GRAVITY, MAX_FALL_SPEED);
789	    moveAndCollide(this, world, this.vx, this.vy);
790	    if (this.hitWall) this.vx *= 0.5;
791	    if (wantDir !== 0) this.facing = wantDir;
792	    // 开关门（原版 54478-54500：撞到关着的门 → 1/10（或卡住必试）开门，两方向回退；
793	    // 54243-54252：走过门 >2 格关门，>4 格放弃）
794	    this.npcDoorUpdate(world, game);
795	
796	    // ---- 原版 FindFrame 城镇分支（NPC.cs:70172-70262，UpdateNPC :91565 调）----
797	    this.updateWalkFrame();
798	
799	  }
800	
801	  /** FindFrame 城镇分支（NPC.cs:70172-70262）：腾空=帧1；地面站定=帧0、计数清零；
802	   *  行走 frameCounter += |vx|*2+1，>6 推进，帧区间 2..frames-extra-1（越界回卷
803	   *  帧2）。微光上升态同样调（原版 FindFrame 在 AI 早退之后仍执行 :91565） */
804	  private updateWalkFrame(): void {
805	    if (!this.onGround) {
806	      this.frame = 1;
807	      this.frameT = 0;
808	    } else if (Math.abs(this.vx) < 0.05) {
809	      this.frame = 0;
810	      this.frameT = 0;
811	    } else {
812	      const total = VANILLA_NPCS[String(this.vanillaId)]?.frames ?? 1;
813	      const extra = TOWN_NPC_IDS[this.npcKey]?.extra ?? 2;
814	      this.frameT += Math.abs(this.vx) * 2 + 1;
815	      if (this.frame < 2) this.frame = 2;
816	      if (this.frameT > 6) {
817	        this.frameT = 0;
818	        this.frame++;
819	      }
820	      if (this.frame >= total - extra) this.frame = 2;
821	    }
822	  }
823	
824	  /** AI_007 ai[0]==25 微光上升态（NPC.cs:53594-53682）1:1，返回 true = 态中。
825	   *  时间线：ai[1]==0 落点传送（:53609，位移 ≥560px 则 ai[2]=30 暂停 + 发送
826	   *  粒子）→ ai[2] 倒计时毕置 ai[1]=1（:53612-53618）→ 此后每 tick ai[1]+1
827	   *  （:53620）→ ≥30 起非浸液 st−1/60、浸液钳 30 等待（:53621-53629）+
828	   *  velocity=(0,−4×st)（:53631）→ ai[1]≥75 且 st≤0 收尾（:53653-53669）：
829	   *  变体翻转（双向）+ 原地 Teleport(12)（TeleportEffect 无 style 12 分支 =
830	   *  纯重锚无视觉，Main.cs:13169-13414）+ ShimmerTownNPC 到场粒子 + 成就 43 */
831	  private shimmerRiseUpdate(
832	    world: import('../world/World').World, game: GameHooks, wet: boolean,
833	  ): boolean {
834	    if (this.shimmerRiseT === 0) this.vx = 0;                     // :53597-53599
835	    if (this.shimmerRiseT === 0 && this.shimmerRisePause < 1) {
836	      this.shimmerLandAt(world.store, game);                      // :53609
837	    }
838	    if (this.shimmerRisePause > 0) {                              // :53612-53618
839	      this.shimmerRisePause--;
840	      if (this.shimmerRisePause <= 0) this.shimmerRiseT = 1;
841	      return true;
842	    }
843	    this.shimmerRiseT++;                                          // :53620
844	    if (this.shimmerRiseT >= SHIMMER_RISE_VELOCITY_TICK) {        // :53621
845	      if (!wet) {
846	        // WetCollision 近似 = 中心格任意液体（:53622-53626）
847	        this.shimmerTransparency = shimmerTransparencyNext(this.shimmerTransparency, false, false, true);
848	      } else {
849	        this.shimmerRiseT = SHIMMER_RISE_VELOCITY_TICK;           // :53627 浸液等待
850	      }
851	      this.vx = 0;
852	      this.vy = -4 * this.shimmerTransparency;                    // :53631
853	    }
854	    // 上升演出（:53634-53649）——dust 309 / ShimmerBlock 的 Remap 门在 ai[1]<30
855	    // 时钳到恒假，与原版同 tick 生效（光走 lightRGB 的 shimmerRise 分支）
856	    const num5 = Math.random() * 2 - 1;                           // NextFloatDirection
857	    if (Math.random() > remapClamped(this.shimmerRiseT, 30, 60, 1, 0.5)) {
858	      // dust 309（:53640-53646）：下半身盒（Y+20/H−20）内随机点 + 圆偏(8,0)+(0,4)，
859	      // velocity=(0,−2).RotatedBy(num5×2π×0.11)、scale 1.7−|num5|×1.3（size 档
860	      // spawnBurst 无参不建模）
861	      game.spawnBurst?.(
862	        this.x + Math.random() * this.w + (Math.random() * 2 - 1) * 8,
863	        this.y + 20 + Math.random() * (this.h - 20) + 4,
864	        '#BFE8FF', 1, 2, -Math.PI / 2 + num5 * Math.PI * 2 * 0.11, 0,
865	        { life: 30, grav: -0.04 },
866	      );
867	    }
868	    if (this.shimmerRiseT > 60 && Math.floor(Math.random() * 15) === 0) {
869	      // ShimmerBlock ×3（:53642-53649 → Spawn_ShimmerBlock :1791-1811）：星尘带
870	      // MovementVector = DirectionTo(v).RotatedBy(9π/20×±1)×rand 减速漂散——
871	      // 无粒子编排器，随机向小速度近似
872	      for (let i = 0; i < 3; i++) {
873	        game.spawnBurst?.(
874	          this.x + Math.random() * this.w, this.y + Math.random() * this.h,
875	          '#C9C2FF', 1, 0.8, Math.random() * Math.PI * 2, Math.PI, { life: 45, damp: 0.98 },
876	        );
877	      }
878	    }
879	    // TargetClosest（:53651）：面向最近玩家
880	    const tp = (game as unknown as { player?: { x: number; y: number; w: number; h: number; dead: boolean } }).player;
881	    if (tp && !tp.dead) this.facing = tp.x + tp.w / 2 < this.cx ? -1 : 1;
882	    if (this.shimmerRiseT >= SHIMMER_RISE_END_TICK && this.shimmerTransparency <= 0) {
883	      this.shimmerRise = false;                                   // ai[0]=0（:53654）
884	      this.shimmerRiseT = 0;
885	      this.shimmerRisePause = 0;
886	      this.vx = 0; this.vy = -4;                                  // :53660
887	      this.shimmered = !this.shimmered;                           // :53664 变体翻转（双向）
888	      // ShimmerTownNPC 到场粒子（:53666 → Spawn_ShimmerTownNPC :1696-1752）：
889	      // 40 PrettySparkle（hsl(rand,1,0.5)+白，30×60 盒上升）+ 20 dust 308 四色
890	      // （#FFFFD2/#BEF5FF/#FF96FF/#BEAFFF = 1:1:1:3，vy−8）+ SoundID.Item29
891	      //（= Item bank cue 29，Sfx 键 manaCrystal → sounds/Item_29.wav；曾因登记
892	      //  "素材缺"走 shimmerSplash 近似——素材实测在库，已换真声）
893	      game.spawnParticles(this.cx, this.cy, '#BEAFFF', 12, 3.2, { life: 34, grav: -0.12 });
894	      game.spawnParticles(this.cx, this.cy, '#BEF5FF', 4, 3.2, { life: 34, grav: -0.12 });
895	      game.spawnParticles(this.cx, this.cy, '#FF96FF', 4, 3.2, { life: 34, grav: -0.12 });
896	      game.playSfx('manaCrystal', 1, this.cx, this.cy);
897	      if (this.shimmered) game.achievements?.notifyProgressionEvent(43);   // :53667-53669
898	    }
899	    return true;
900	  }
901	
902	  /** AI_007_TownEntities_Shimmer_TeleportToLandingSpot（:53609 → :55982-56010 +
903	   *  ScanForBestSpotToLandOn :55996-56059）：以自身顶格扫无微光落点（home 锚
904	   *  兜底），传送过去；位移 ≥560px → ai[2]=30 暂停 + ShimmerTownNPCSend 粒子
905	   *  （Spawn_ :1657-1694）。复用 stats/Shimmer.findShimmerFreeSpot（玩家脱困
906	   *  版同谓词）：环扫为原版 8 点环超集、r 并到 59、平台落点恒允许（原版仅
907	   *  homeless 无 home 时 allowSolidTop）——行为相容近似 */
908	  private shimmerLandAt(st: TileStore, game: GameHooks): void {
909	    const spot = findShimmerFreeSpot(
910	      st, Math.floor(this.x / TILE), Math.floor(this.y / TILE),   // Top.ToTileCoordinates
911	      this.home?.x, this.home?.y,
912	    );
913	    if (!spot) return;
914	    const nx = spot.x * TILE - this.w / 2, ny = spot.y * TILE - this.h;   // ShimmerHelper.cs:9
915	    const dist = Math.hypot(nx - this.x, ny - this.y);
916	    this.x = nx;
917	    this.y = ny;
918	    if (dist >= SHIMMER_RISE_TELEPORT_DIST) {
919	      this.shimmerRisePause = SHIMMER_RISE_PAUSE;                 // :56004
920	      game.spawnParticles(this.cx, this.cy, '#BEAFFF', 14, 1.2, { life: 30, grav: -0.05 });
921	      game.spawnParticles(this.cx, this.cy, '#BEF5FF', 10, 1.2, { life: 30, grav: -0.05 });
922	    }
923	  }
924	
925	  /** 环境与互殴受击(NPC.cs:91534-91544 的 townNPC 分支三件套):
926	   *  ① 岩浆(Collision_LavaCollision :94511-94530):immun[255]=30 + StrikeNPC(50) 直伤
927	   *    (OnFire buff 24/420t 未接城镇 NPC buff 系统,略——登记)
928	   *  ② 溺水(NPC.CheckDrowning :96118-96154):水内每 7t breath--;breath≤0 后
929	   *    每 7t life-=2,归零一击 StrikeNPC(2);离水 breath+3/t cap 200
930	   *  ③ 敌怪互殴(GetHurtByOtherNPCs :93605-93690):任一 !friendly 且 damage>0 的
931	   *    NPC 接触 → StrikeNPC(DamageVar(attacker.damage), 6, 方向),immune[255]=30;
932	   *    dryadWard 荆棘反伤(num5/3)与 HurtingBees 未接,略
933	   *  Enemy.def.damage 已含难度缩放(ScaleStats),DamageVar≈1(Classic)直用。 */
934	  private envHurtUpdate(world: import('../world/World').World, game: GameHooks): void {
935	    if (this.dead) return;
936	    const st = world.store;
937	    if (this.lavaCd > 0) this.lavaCd--;
938	    if (this.npcVsCd > 0) this.npcVsCd--;
939	    const ci = st.idx(
940	      Math.max(0, Math.min(st.w - 1, Math.floor(this.cx / TILE))),
941	      Math.max(0, Math.min(st.h - 1, Math.floor(this.cy / TILE))),
942	    );
943	    // ① 岩浆(:94511-94530)
944	    if (st.liquid[ci] > 30 && st.liquidType[ci] === 2 && this.lavaCd <= 0) {
945	      this.lavaCd = 30;
946	      this.hurt(50, 0, 0, game);
947	    }
948	    // ② 溺水(:96118-96154;DrownCollision=头部浸水,取头顶格)
949	    const headY = Math.max(0, Math.floor((this.y + 6) / TILE));
950	    const hi = st.idx(Math.max(0, Math.min(st.w - 1, Math.floor(this.cx / TILE))), headY);
951	    const submerged = st.liquid[hi] > 30 && st.liquidType[hi] === 1;
952	    if (submerged) {
953	      if (++this.breathCounter >= 7) {
954	        this.breathCounter = 0;
955	        this.breath--;
956	        if (this.breath <= 0) {
957	          this.breath = 0;
958	          this.hp -= 2; // life-=2 直伤(不过防御,原版 :96137)
959	          if (this.hp <= 0) { this.hp = 1; this.hurt(2, 0, 0, game); } // :96141-96144 致死一击
960	          else game.addDamageNumber(this.cx, this.y, 2, false, '#FFD060');
961	        }
962	      }
963	    } else {
964	      this.breath = Math.min(200, this.breath + 3);
965	      this.breathCounter = 0;
966	    }
967	    // ③ 敌怪互殴(:93605-93690)
968	    if (this.npcVsCd <= 0) {
969	      for (const ent of game.enemies()) {
970	        const e = ent as unknown as { x: number; y: number; w: number; h: number; dead: boolean;
971	          damage?: number; def?: { damage?: number } };
972	        if (e.dead) continue;
973	        const dmg = e.damage ?? e.def?.damage ?? 0;
974	        if (dmg <= 0) continue;
975	        if (!(this.x < e.x + e.w && this.x + this.w > e.x && this.y < e.y + e.h && this.y + this.h > e.y)) continue;
976	        const dir = e.x + e.w / 2 > this.cx ? -1 : 1; // :93662 攻击者在右侧 → 向左击退
977	        this.npcVsCd = 30;                              // immune[255]=30
978	        this.hurt(dmg, dir * 6, 0, game);               // kb=6(:93661)
979	        break;
980	      }
981	    }
982	  }
983	
984	  /** 城镇 NPC 自卫攻击（AI_007 攻击态机,NPC.cs:54747-55538 + 触发门 :55621-55966）。
985	   *  返回 true = 攻击态中(调用方停走)。语义对照:
986	   *  - flag31 门 ≈ 空闲+站地+触发冷却尽+探测范围内有可打敌(flag16;stinky 分支无系统跳过)
987	   *  - 掷骰 rand(max(1,chance×num3))==0,num3=2(209 ÷3),:53813/:53562
988	   *  - 入态:ai[1]=AttackTime,面向目标;态内每 tick ai[1]--/localAI[3]++/vx×0.8
989	   *  - 发射档:localAI[3]==num46/55/65;连发链 `localAI[3]>档 → 推下一档`(:55066 族)
990	   *  - 退出:ai[1]<=0 → 冷却 localAI[1] = cdBase/2 + rand(cdRand)(:54927-54934 族)
991	   *  伤害缩放(考古销项 2026-08-14):四态伤害统一走 GetAttackDamage_ForTownNPC
992	   *  (NPC.cs:7041-7044 = ×TownNPCDamageMultiplier.Sample(Main.Difficulty),
993	   *  GameDifficultyData.cs:69:Journey 2/Classic 1/Expert 1.5/Legendary 2,Master 3
994	   *  无键→区间插值 1.75)——已接 ScaleStats.getAttackDamageForTownNPC +
995	   *  mainDifficulty(旅程强度滑杆/getGoodWorld +1 同链)。
996	   *  num2 进度强化链(2026-08-14 接):AI_007 头部 :53400-53557 = 战斗书两本
997	   *  +0.25/17 Boss 旗标+硬模式(+0.05~+0.4)/Skyblock+0.5/醉酒尾乘×1.1——
998	   *  townNpcProgressionBoost(FromWorld) 1:1,num3(频率门除数)同链同步接;
999	   *  恒 false 登记:skyblockLowTiles(无 ScanTiles 计数链,见 fromWorld 注);
1000	   *  tipsy=实例位(669 麦酒爆炸施加,TownShot.kill669→applyTipsy,本类
1001	   *  tipsyT/tipsyNow 承接——消费点按 this.tipsy 覆盖 fromWorld 的 false)。
1002	   *  已销项:633 狼人变体 proj929+×1.5/108 连发 1-3(权重 4:2:1)±3.4/160·663
1003	   *  落点弹原版几何+重掷次数(10/5)。
1004	   *  登记未接:挥击态逐 tick 弧形判定(GetSwingStats/TweakSwingStats,近似中段
1005	   *  一击);:55864 族 flag28 LOS 掷骰直存;对话中 num3×0.8(:55617,本仓 talking
1006	   *  不入攻击态不可达);防御链 :53401-53531(dryadWard+Boss 防,另批) */
1007	  private attackUpdate(world: import('../world/World').World, game: GameHooks): boolean {
1008	    if (this.atkCd > 0) this.atkCd--;
1009	    const atkType = TOWN_ATTACK_TYPE[this.vanillaId];
1010	    if (atkType === undefined) return false;
1011	    this.hardModeFlag = !!(world.flags as Record<string, boolean>).hardMode;
1012	    this.werewolfFlag = this.vanillaId === 633
1013	      && shouldBestiaryGirlBeLycantrope(world.clock.moonPhase, world.clock.bloodMoon, world.clock.isDay);
1014	    if (this.atkState === 0) {
1015	      // 触发门:站地 + 冷却尽 + 探测范围内有 LOS 敌(:55621 flag31 + :55864 族掷骰)
1016	      // 坐姿 ai[0]==5 不满足 flag31 的 ai[0]<2 门(:55621)——坐着不打,起身再打
1017	      if (!this.onGround || this.atkCd > 0 || this.talking || this.sitting) return false;
1018	      const range = TOWN_DANGER_RANGE[this.vanillaId] ?? 200;
1019	      const target = this.pickSideTarget(world, game, range);
1020	      if (!target) return false;
1021	      let chance = TOWN_ATTACK_CHANCE[this.vanillaId] ?? 1;
1022	      // num3 = 进度强化链频率除数(:53413 起 19 项累计;2026-08-14 前恒 2 近似已废)
1023	      // tipsy = 实例位（NPC.tipsy :93179,669 麦酒爆炸施加——非世界旗标）
1024	      const progGate = townNpcProgressionFromWorld(world);
1025	      progGate.tipsy = this.tipsy;
1026	      let num3 = townNpcProgressionBoost(progGate).chanceMul;
1027	      if (this.vanillaId === 209) num3 /= 3;    // :53548 蒸汽朋克人三倍勤
1028	      const gate = Math.max(1, Math.floor(chance * num3));
1029	      if (Math.random() >= 1 / gate) return false;  // rand(gate)==0
1030	      const params = this.atkParams(atkType);
1031	      if (!params && atkType !== 3) return false;
1032	      this.atkState = atkType === 0 ? 10 : atkType === 1 ? 12 : atkType === 2 ? 14 : 15;
1033	      this.holdAim = 0;                       // ai[2] 入态清零(:54931 族)
1034	      this.atkTimer = TOWN_ATTACK_TIME[this.vanillaId] ?? 30;
1035	      this.atkTick = 0;
1036	      this.atkBurstIdx = 0;
1037	      this.atkNextShot = (params as TownShotParams | undefined)?.shootTick ?? 1;
1038	      this.facing = (target as { cx: number }).cx < this.cx ? -1 : 1;
1039	      return true;
1040	    }
1041	    // ---- 态内推进 ----
1042	    this.atkTimer--;
1043	    this.atkTick++;
1044	    this.vx *= 0.8;
1045	    const range = TOWN_DANGER_RANGE[this.vanillaId] ?? 200;
1046	    if (this.atkState === 15) {
1047	      this.swingUpdate(world, game);
1048	    } else {
1049	      const params = this.atkParams(TOWN_ATTACK_TYPE[this.vanillaId]) as TownShotParams;
1050	      // 连发链:localAI[3] 超过当前档 → 推下一档(原版逐档 if 链)
1051	      const burst = params.burst ?? [];
1052	      while (this.atkBurstIdx < burst.length && this.atkTick > this.atkNextShot) {
1053	        this.atkNextShot = burst[this.atkBurstIdx++];
1054	      }
1055	      if (this.atkTick === this.atkNextShot) this.shootAt(world, game, params, range);
1056	    }
1057	    if (this.atkTimer <= 0) {
1058	      // 退出 + 冷却(:54927/:55199/:55397/:55529 族):localAI[1] = cdBase/2 + rand(cdRand)
1059	      const p = this.atkParams(TOWN_ATTACK_TYPE[this.vanillaId]);
1060	      const cdBase = (p as TownShotParams | undefined)?.cdBase ?? 10;
1061	      const cdRand = (p as TownShotParams | undefined)?.cdRand ?? 1;
1062	      this.atkState = 0;
1063	      this.holdAim = 0;                       // ai[2] 态尽归零(:55203 族)
1064	      this.atkCd = Math.floor(cdBase / 2) + Math.floor(Math.random() * Math.max(1, cdRand));
1065	    }
1066	    return true;
1067	  }
1068	
1069	  /** 当前类型的态参数(10/12/14;15 走 TOWN_SWING);hardMode 覆盖按 world.flags */
1070	  private atkParams(atkType: 0 | 1 | 2 | 3): TownShotParams | undefined {
1071	    const table = atkType === 0 ? TOWN_MELEE : atkType === 1 ? TOWN_BOW : atkType === 2 ? TOWN_MAGIC : undefined;
1072	    if (!table) return undefined;
1073	    const base = table[this.vanillaId];
1074	    if (!base) return undefined;
1075	    if (base.hardMode && this.hardModeFlag) return { ...base, ...base.hardMode } as TownShotParams;
1076	    // 633 狼人态(:54782-54785):换 proj 929 + dmg×1.5 取(int)截断(15→22)
1077	    if (this.vanillaId === 633 && this.werewolfFlag) {
1078	      return { ...base, proj: 929, dmg: Math.trunc(base.dmg * 1.5) };
1079	    }
1080	    return base;
1081	  }
1082	
1083	
1084	  /** 挥击态(15):前方矩形近战判定(:55469-55494;原版逐 tick 弧形挥击,近似中段一击) */
1085	  private swingUpdate(world: import('../world/World').World, game: GameHooks): void {
1086	    const sw = TOWN_SWING[this.vanillaId];
1087	    if (!sw) return;
1088	    const t = TOWN_ATTACK_TIME[this.vanillaId] ?? 15;
1089	    if (this.atkTick !== Math.max(1, Math.floor(t / 2))) return; // 挥击中段
1090	    const rect = sw.rect;
1091	    const rx = this.facing === 1 ? this.cx : this.cx - rect;
1092	    const ry = this.cy - rect / 2;
1093	    let dmg = sw.dmg;
1094	    let kb = sw.kb;
1095	    if (this.vanillaId === 441 && this.givenName === 'Andrew') { dmg *= 2; kb *= 2; } // 猫单特典 :55431
1096	    // num2 进度强化链(:53400-53557)先于难度曲线(:55466 同式)
1097	    // tipsy = 实例位（NPC.tipsy :93179,669 麦酒爆炸施加——非世界旗标）
1098	    const progSwing = townNpcProgressionFromWorld(world);
1099	    progSwing.tipsy = this.tipsy;
1100	    const num2 = townNpcProgressionBoost(progSwing).damageMul;
1101	    for (const ent of game.enemies()) {
1102	      const e = ent as unknown as { x: number; y: number; w: number; h: number; dead: boolean;
1103	        hurt: (d: number, kx: number, ky: number, g: GameHooks) => boolean };
1104	      if (e.dead) continue;
1105	      if (!(rx < e.x + e.w && rx + rect > e.x && ry < e.y + e.h && ry + rect > e.y)) continue;
1106	      // 伤害结算(:55466):GetAttackDamage_ForTownNPC(num82*num2)——(int) 截断
1107	      if (e.hurt(getAttackDamageForTownNPC(dmg * num2, mainDifficulty(world)), this.facing * kb, 0, game)) {
1108	        game.addDamageNumber(e.x, e.y, dmg, false, '#FFD060');
1109	      }
1110	    }
1111	  }
1112	
1113	  /** 探测范围内按侧取最近可打敌(:53887-53958 近侧目标;LOS=Collision.CanHit)。
1114	   *  返回含实体 position/Size——160/663 落点弹几何按原版 Main.npc[n].position/Size 采样 */
1115	  private pickSideTarget(world: import('../world/World').World, game: GameHooks, range: number):
1116	    { cx: number; cy: number; x: number; y: number; w: number; h: number } | null {
1117	    let bestL: { cx: number; cy: number; x: number; y: number; w: number; h: number; d: number } | null = null;
1118	    let bestR: { cx: number; cy: number; x: number; y: number; w: number; h: number; d: number } | null = null;
1119	    for (const ent of game.enemies()) {
1120	      const e = ent as unknown as { x: number; y: number; w: number; h: number; dead: boolean;
1121	        damage?: number; def?: { damage?: number } };
1122	      if (e.dead) continue;
1123	      // 原版扫描门(:53887):!friendly && damage>0 才算威胁(0 伤敌/友好不算)
1124	      const edmg = e.damage ?? e.def?.damage ?? 0;
1125	      if (edmg <= 0) continue;
1126	      // 中心由 x/y/w/h 推导(敌实体有 cx/cy,但勿依赖——判距门曾因 NaN 恒假失效)
1127	      const ecx = e.x + e.w / 2, ecy = e.y + e.h / 2;
1128	      const dx = ecx - this.cx;
1129	      const d = Math.hypot(dx, ecy - this.cy);
1130	      if (d >= range) continue;
1131	      if (!canHit(world.store, this.x, this.y, this.w, this.h, e.x, e.y, e.w, e.h)) continue;
1132	      const cand = { cx: ecx, cy: ecy, x: e.x, y: e.y, w: e.w, h: e.h, d };
1133	      if (dx < 0) { if (!bestL || d < bestL.d) bestL = cand; }
1134	      else { if (!bestR || d < bestR.d) bestR = cand; }
1135	    }
1136	    // num15 侧选择(:53960):两侧都有 → 距离近者;仅一侧 → 该侧
1137	    if (bestL && bestR) return bestL.d <= bestR.d ? bestL : bestR;
1138	    return bestL ?? bestR;
1139	  }
1140	
1141	  /** 发射(:54903/:55175/:55325 三族瞄准公式统一在此) */
1142	  private shootAt(world: import('../world/World').World, game: GameHooks, params: TownShotParams, range: number): void {
1143	    const st = world.store;
1144	    let proj = params.proj;
1145	    let dmg = params.dmg;
1146	    let speed = params.speed;
1147	    let kb = params.kb;
1148	    let spread = params.spread;
1149	    // 229 PrettySafe 近距保命换炮弹(:55128-55135)
1150	    const pretty = TOWN_PRETTY_SAFE[this.vanillaId];
1151	    const target = this.pickSideTarget(world, game, range);
1152	    if (params.panic && pretty && target && Math.hypot(target.cx - this.cx, target.cy - this.cy) < pretty
1153	      && this.atkTick === params.shootTick) {
1154	      proj = params.panic.proj; dmg = params.panic.dmg; speed = params.panic.speed;
1155	      kb = params.panic.kb; spread = params.panic.spread;
1156	    }
1157	    // 209 三选一弹(:55139)
1158	    if (this.vanillaId === 209 && !params.panic) {
1159	      const pick = [134, 133, 135][Math.floor(Math.random() * 3)];
1160	      proj = pick;
1161	      const m: Record<number, [number, number, number, number, number]> = {
1162	        134: [20, 13, 4, 0.1, 20], 133: [25, 10, 6, 0.2, 10], 135: [30, 12, 7, 0.2, 30],
1163	      };
1164	      [dmg, speed, kb, spread] = [m[pick][0], m[pick][1], m[pick][2], m[pick][3]];
1165	    }
1166	    // 瞄准:弓 = 目标上抬 aimLift 取向;近战/魔法 = aimLiftScaled×(dist/range 归一)上抬
1167	    let vx = this.facing, vy = 0;
1168	    if (target) {
1169	      // ai[2] 持械瞄准值(:55191-55197):弓族发射档取【目标中心】方向 Y 钳 ±0.5
1170	      // (原版另有 flag28 LOS 门——触发门已验 LOS,此处近似直存;aimLift 不参与)
1171	      if (this.atkState === 12) {
1172	        const pdx = target.cx - this.cx, pdy = target.cy - this.cy;
1173	        const pdl = Math.hypot(pdx, pdy) || 1;
1174	        this.holdAim = Math.max(-0.5, Math.min(0.5, pdy / pdl));
1175	      }
1176	      let lift = params.aimLift ?? 0;
1177	      if (this.atkState === 10 || this.atkState === 14) {
1178	        const dist = Math.hypot(target.cx - this.cx, target.cy - this.cy);
1179	        lift = (params.aimLiftScaled ?? 0) * Math.max(0, Math.min(1, dist / range));
1180	        vy = -1; // 近战/魔法默认上抛分量(初值 -UnitY)
1181	      }
1182	      const dx = target.cx - this.cx;
1183	      const dy = target.cy - lift - this.cy;
1184	      const dl = Math.hypot(dx, dy) || 1;
1185	      vx = dx / dl; vy = dy / dl;
1186	      if (Math.sign(vx) !== this.facing) { vx = this.facing; vy = this.atkState === 12 ? 0 : -1; }
1187	    } else if (this.atkState !== 12) {
1188	      vy = -1;
1189	    }
1190	    vx *= speed; vy *= speed;
1191	    // 散布(Utils.RandomVector2 ±spread;近战态恒 0)
1192	    if (spread > 0) {
1193	      vx += (Math.random() * 2 - 1) * spread;
1194	      vy += (Math.random() * 2 - 1) * spread;
1195	    }
1196	    // 伤害结算(近战 :54897/弓 :55169/魔法 :55319 同式):
1197	    // GetAttackDamage_ForTownNPC(dmg*num2)——(int) 截断;num2 进度强化链
1198	    // (:53400-53557,2026-08-14 接,2026-08-14 前恒 1 近似已废)
1199	    // tipsy = 实例位（NPC.tipsy :93179,669 麦酒爆炸施加——非世界旗标）
1200	    const progShot = townNpcProgressionFromWorld(world);
1201	    progShot.tipsy = this.tipsy;
1202	    const num2 = townNpcProgressionBoost(progShot).damageMul;
1203	    const dmgFinal = getAttackDamageForTownNPC(dmg * num2, mainDifficulty(world));
1204	    const sx = this.cx + this.facing * 16 - 5;
1205	    const sy = this.cy - 2 - 5;
1206	    // 落点弹(160/663):目标区域随机点生成 velocity=0;实心重掷(160≤10/:55351、
1207	    // 663≤5/:55369),重掷耗尽仍实心则按末次落点照常生成(原版 while 语义)
1208	    if (speed === 0 && target) {
1209	      const is160 = this.vanillaId === 160;
1210	      let retries = is160 ? 10 : 5;
1211	      let px = 0, py = 0;
1212	      do {
1213	        if (is160) {   // :55349 position − Size×2 + Size×rand(0..1)×5(逐轴独立)
1214	          px = target.x - target.w * 2 + target.w * Math.random() * 5;
1215	          py = target.y - target.h * 2 + target.h * Math.random() * 5;
1216	        } else {       // :55367 position + Size×rand(0..1)
1217	          px = target.x + target.w * Math.random();
1218	          py = target.y + target.h * Math.random();
1219	        }
1220	      } while (retries-- > 0 && st.isSolid(Math.floor(px / TILE), Math.floor(py / TILE)));
1221	      game.spawnTownShot?.(new TownShot(px - 5, py - 5, 0, 0, dmgFinal, kb, proj, { noGravity: true }));
1222	      return;
1223	    }
1224	    // 108 巫师连发(:55336-55348):SelectRandom(1,1,1,1,2,2,3) 掷 1-3 发(权重 4:2:1),
1225	    // 每发速度额外 ±3.4 逐轴随机(共基速 vec4,叠加 vector5)
1226	    if (this.vanillaId === 108) {
1227	      const n = [1, 1, 1, 1, 2, 2, 3][Math.floor(Math.random() * 7)];
1228	      for (let i = 0; i < n; i++) {
1229	        const ox = (Math.random() * 2 - 1) * 3.4;
1230	        const oy = (Math.random() * 2 - 1) * 3.4;
1231	        game.spawnTownShot?.(new TownShot(sx, sy, vx + ox, vy + oy, dmgFinal, kb, proj, {}));
1232	      }
1233	      return;
1234	    }
1235	    game.spawnTownShot?.(new TownShot(sx, sy, vx, vy, dmgFinal, kb, proj, {
1236	      life: this.vanillaId === 588 ? 480 : undefined,
1237	    }));
1238	  }
1239	
1240	  /** 城镇 NPC 开关门（原版 NPC.cs:54478-54500/54243-54252，含高门 389 族 ShiftTallGate） */
1241	  private npcDoorUpdate(world: import('../world/World').World, game: GameHooks) {
1242	    const st = world.store;
1243	    const DOOR_OPEN = TILE_BY_KEY_DOOR_TILES['door_open'] ?? -1;
1244	    const GATE_OPEN = TILE_BY_KEY_DOOR_TILES['tall_gate_open'] ?? -1;
1245	    // 过门关门：中心距门 >2 格 → 关；>4 格或换层 → 放弃（原版 54243-54252）
1246	    if (this.closeDoor) {
1247	      const tx = Math.floor(this.cx / TILE), ty = Math.floor(this.cy / TILE);
1248	      if (Math.abs(tx - this.doorX) > 2 || Math.abs(ty - this.doorY) > 4) {
1249	        const doorType = st.type[st.idx(this.doorX, this.doorY)];
1250	        if (Math.abs(tx - this.doorX) <= 4 && Math.abs(ty - this.doorY) <= 4) {
1251	          if (doorType === DOOR_OPEN) closeDoorTile(st, this.doorX, this.doorY);
1252	          else if (doorType === GATE_OPEN) {
1253	            // 高门关门（原版 54266-54274：ShiftTallGate(closing:true)，tile 389 → 388）
1254	            shiftTallGate(st, this.doorX, this.doorY, true, () => game.playSfx('door_close', 1, this.cx, this.cy));
1255	          }
1256	        }
1257	        this.closeDoor = false;
1258	      }
1259	      return;
1260	    }
1261	    // 撞门开门：前方碰撞点是关着的普通门（10）或高门（388）
1262	    // （原版 54478-54500：Next(10)==0；普通门两方向回退，高门 ShiftTallGate(closing:false)）
1263	    if (!this.hitWall) return;
1264	    const fx = Math.floor((this.cx + this.facing * (this.w / 2 + 2)) / TILE);
1265	    const fy = Math.floor((this.y + this.h - 8) / TILE);
1266	    for (const dy of [0, -1]) {
1267	      const x = fx, y = fy + dy;
1268	      if (x < 1 || y < 1 || x >= st.w - 1 || y >= st.h - 1) continue;
1269	      const t = st.type[st.idx(x, y)];
1270	      if (Math.random() >= 0.1) return;   // 原版 Next(10)==0
1271	      if (t === TILE_BY_KEY_DOOR_TILES['door_closed']) {
1272	        const before = st.type[st.idx(x, y)];
1273	        const opened = openDoor(st, x, y, this.facing) || openDoor(st, x, y, -this.facing);
1274	        if (opened && before !== st.type[st.idx(x, y)]) {
1275	          this.closeDoor = true;
1276	          this.doorX = x; this.doorY = y;
1277	          game.playSfx('door_open', 1, this.cx, this.cy);
1278	        }
1279	        return;
1280	      }
1281	      if (t === TILE_BY_KEY_DOOR_TILES['tall_gate_closed']) {
1282	        const anchor = shiftTallGate(st, x, y, false, () => game.playSfx('door_open', 1, this.cx, this.cy));
1283	        if (anchor) {
1284	          this.closeDoor = true;
1285	          this.doorX = anchor[0]; this.doorY = anchor[1];
1286	        }
1287	        return;
1288	      }
1289	    }
1290	  }
1291	
1292	  /** 坐姿状态机（AI_007 ai[0]==5 族，NPC.cs:53264-53287 入座 / :54682-54710 态推进）。
1293	   *  返回 true = 坐姿中（调用方停走）。语义对照：
1294	   *  - 入座门：夜/雨 flag（restSpot 非空）+ 非对话 + 非攻击态（坐姿与攻击互斥：
1295	   *    flag31 的 ai[0]<2 门 :55621 不含 5）+ 站定在 rest spot 同格（:54074
1296	   *    num6==floorX && num7==floorY）——刚走回家传送者免站定门
1297	   *    （TeleportToHome 落位即 TryForcingSitting :56081）
1298	   *  - 入座（forceSit）：ai[1]=900+rand(10800)、direction=frameX!=0?1:-1、
1299	   *    Bottom=(x*16+8+2*dir, y*16)、velocity=0（:53283-53287）
1300	   *  - 态内：vx×0.8、ai[1]--；椅格（Bottom−2px）非椅/马桶 → ai[1]=0 立即起身
1301	   *    （:54691-54697）；对话打断在 talking 块（:53738）
1302	   *  - 时限起身：ai[1]<=0 → ai[0]=0 / localAI[3]=30+rand(60)（:54703-54709；
1303	   *    本仓 wanderT 承接转向冷却）。原版 Main.sittingManager.AddNPC（:54701，
1304	   *    同椅叠坐错位）无对应渲染载体，略——占位互斥由 forceSit 的占位门承担 */
1305	  private sittingUpdate(world: import('../world/World').World, _game: GameHooks): boolean {
1306	    if (this.sitting) {
1307	      this.vx *= 0.8;                                   // :54684
1308	      this.sitTimer--;                                  // :54685
1309	      const st = world.store;
1310	      const tx = Math.floor(this.cx / TILE);
1311	      const ty = Math.floor((this.y + this.h - 2) / TILE);   // Bottom−2px 格（:54692）
1312	      if (!st.inBounds(tx, ty) || !canSitAt(st.type[st.idx(tx, ty)], st.frameY[st.idx(tx, ty)])) {
1313	        this.sitTimer = 0;                              // 椅子没了 → 起身（:54695）
1314	      }
1315	      if (this.sitTimer <= 0) {
1316	        this.sitting = false;
1317	        this.wanderT = SIT_STAND_WANDER_BASE + Math.floor(Math.random() * SIT_STAND_WANDER_RAND);
1318	      }
1319	      return this.sitting;
1320	    }
1321	    if (!this.restSpot || this.talking || this.atkState !== 0 || !this.home) return false;
1322	    if (!this.teleportedHome) {
1323	      if (!this.onGround || Math.abs(this.vx) > 0.05) return false;
1324	      // 站定同格门（:54074）：myTile == rest spot
1325	      const myX = Math.floor(this.cx / TILE), myY = Math.floor((this.y + this.h) / TILE);
1326	      if (myX !== this.restSpot.x || myY !== this.restSpot.y) return false;
1327	    }
1328	    return this.forceSit(world, _game, this.restSpot);
1329	  }
1330	
1331	  /** AI_007_TryForcingSitting（NPC.cs:53264-53287）：落座地面格上一行须为可坐格
1332	   *  （canSitAt 含椅 style 27 排除门）+ 无其他坐姿城镇 NPC 占位 → 坐下 */
1333	  private forceSit(world: import('../world/World').World, game: GameHooks, spot: SitSpot): boolean {
1334	    const st = world.store;
1335	    const cx = spot.x, cy = spot.y - 1;            // 椅格 = 落座地面格上一行（:53270）
1336	    if (!st.inBounds(cx, cy)) return false;
1337	    const ci = st.idx(cx, cy);
1338	    if (st.type[ci] === 0 || !canSitAt(st.type[ci], st.frameY[ci])) return false;
1339	    // 占位门（:53278-53286）：任一坐姿城镇 NPC 的 Bottom−2px 格 == 本椅格 → 放弃
1340	    for (const o of game.npcs?.() ?? []) {
1341	      const n = o as { sitting?: boolean; cx?: number; y?: number; h?: number; dead?: boolean };
1342	      if (o === this || n.dead || !n.sitting) continue;
1343	      const ox = Math.floor((n.cx ?? 0) / TILE);
1344	      const oy = Math.floor(((n.y ?? 0) + (n.h ?? 0) - 2) / TILE);
1345	      if (ox === cx && oy === cy) return false;
1346	    }
1347	    this.sitting = true;
1348	    this.sitTimer = SIT_TIME_BASE + Math.floor(Math.random() * SIT_TIME_RAND);   // :53283
1349	    this.facing = chairFacing(st.frameX[ci]);                                    // :53284
1350	    const anchor = sittingAnchor(spot.x, spot.y, this.facing);                   // :53285-53286
1351	    this.x = anchor.x - this.w / 2;
1352	    this.y = anchor.y - this.h;
1353	    this.vx = 0; this.vy = 0;
1354	    return true;
1355	  }
1356	
1357	  /** 当前应使用的贴图 sheet（= DrawNPCCheckAlt Main.cs:22304-22309 →
1358	   *  TownNPCProfiles.GetProfile + profile.GetTextureNPCShouldUse 净效果）。
1359	   *  微光态 → TownNPCs/Shimmered/{Name}_Default 档；派对/狼人 alt → 同档的
1360	   *  _Party / _Transformed 变体。无档案类型（637/638/656 宠物等）返回 null，
1361	   *  渲染端回落 NPC_{id} 竖条。Renderer.drawTownNPC 消费 */
1362	  get townSheet(): string | null {
1363	    return townNpcProfileSheet(this.vanillaId, this.shimmered ? 1 : 0, this.altTexture);
1364	  }
1365	
1366	  draw() { /* Renderer 统一绘制 */ }
1367	}
1368	

```


---

## 🤖 Assistant · 2026-08-17T04:35:37.255Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Our TownNPC.ts is quite comprehensive for: sitting (chair spot scan, TryForcingSitting), shimmer rise, attack states, door open/close, teleport home (approx), env hurt (lava/drowning/NPC vs NPC).

Now I need to check deviations. Let me list what I noticed so far comparing against vanilla:

**1. Sitting (坐椅子)** — mostly implemented (findChairSpot, canSitAt, forceSit, sittingUpdate). Deviations to check:
- Vanilla has TWO sitting entry paths: (a) TryForcingSitting after arriving at resting spot at night (via `flag` deceleration in state 0 when num6==floorX && num7==floorY → AI_007_TryForcingSitting(floorX, floorY)), and (b) random sit while walking (1/300 per tick when standing at chair tile... wait no — path (b) is in the big else-if chain at :55699+: `flag30 && ai[0] == 1f && velocity.Y == 0f && num > 0 && Main.rand.Next(num) == 0` — while WALKING (ai[0]==1), standing on a chair tile (Bottom-2px tile is chair/throne 15/497, not toilet-style), no NPC sitting there, no player sitting there → sit. num=300 for regular town NPCs (0 for town slimes → always).
  - Our implementation only has the night-rest-spot path + teleportedHome. We do NOT have the daytime random sit (ai[0]==1 path). Vanilla: daytime town NPCs DO sit on chairs randomly (1/300 per tick while walking). This is a real deviation — daytime sitting missing!
  - Also the restSpot scanning in ours requires `!world.clock.isDay` — vanilla FindGoodRestingSpot returns early `if (Main.dayTime || ...)` → correct for rest spot. But the random walk-sit path (:55699) is NOT gated on night — it happens any time (flag30 = ai[0]<2 && !flag16 && !wet). Yes — vanilla NPCs sit on chairs during the day too. Ours: only at night. Deviation.
- Vanilla sitting anchor: `base.Bottom = new Vector2(homeFloorX * 16 + 8 + 2 * direction, homeFloorY * 16)` for TryForcingSitting; for the random sit path: `point.Y * 16 + 16` where point is the chair tile → chairTile.Y*16+16 = (chairY+1)*16 → same as ground row below the chair. OK equivalent.
- Vanilla frame during sitting: handled by sittingManager + FindFrame? Let me check how sitting NPC frames are drawn — Main.sittingManager affects draw position, and the "sitting" frame? Let me check FindFrame for town NPC sitting (frame = ? there's a special sitting frame). Let me grep "sitting" in FindFrame region. Actually NPC FindFrame: `if (ai[0] == 5f)` maybe sets frame to 0? The sitting pose comes from the sitting manager offset + regular frame? Hmm — in vanilla, sitting town NPCs use frame 0 (standing frame) but positioned lower (sunk). Actually PlayerSittingHelper moves the NPC draw position. Let me check Main.cs sittingManager draw for NPCs.

- Also our sitting doesn't check "no player sitting" occupancy (only NPC). Minor.
- Missing: vanilla state-0 deceleration path at resting spot calls TryForcingSitting when `flag` (night/rain) — ours requires night for restSpot (isDay check) — vanilla FindGoodRestingSpot early-returns during day so floorX/floorY = home ground; but the "flag" deceleration+sitting at spot only happens at night anyway (flag=false during day unless raining/eclipse/storm). Wait flag = raining || !dayTime || eclipse || slimeRain || storm(above ground). During day rain, flag=true, and FindGoodRestingSpot returns home floor (day early return), so no chairs found during day rain → no sitting during day rain. Ours: restSpot requires `!world.clock.isDay` — so during day rain we don't even scan → same result (no sit). OK equivalent there.
- BUT the random-sit-while-walking path (1/300) is missing entirely — that's the daytime sitting. Actually wait — is it gated by flag30 which requires !flag16 (no danger) and !wet. No day/night gate. So daytime sitting exists in vanilla. Our NPCs never sit during the day. **Deviation (moderate)**.

**2. Sleeping** — vanilla has none for town NPCs. Our implementation: none. ✓ aligned (mark 原版无此行为).

**3. Wander parameters** — ours is heavily simplified:
- Vanilla idle: ai[1] counts down; on expiry → walk (ai[1]=200+Next(300)) or turn (ai[1]=60+Next(120)) depending on avoidFalling. Random turn-around: 1/80 per tick when within ±25 tiles of home & localAI[3]==0 → localAI[3]=200 (turn lockout).
- Our: wanderT = 90 + rand(180); facing random ±1, 35% chance facing=0 (stand). Walk accel 0.06, cap 0.8. Vanilla: accel 0.07, cap 1 (num22=1, num23=0.07). **Speed deviation: ours 0.8/0.06 vs vanilla 1/0.07.**
- Vanilla walk duration: 200-500 ticks; idle duration: 300-1500. Ours: uniform wanderT 90-270 for both walking and standing (no separate walk/idle timers, no direction-lockout).
- Vanilla home leash: ±25 tiles normal wander, force turn at ±50, faster countdown (-5/tick extra) when beyond ±35 walking away. Ours: no leash for regular NPCs (only leashHome special for old man)! **Deviation: vanilla NPCs stay within ±25-50 of home; ours wander infinitely** (well, they flip randomly but can drift). Actually ours has no home-range check in the day branch. Hmm wait — vanilla leash applies ALWAYS (day too): "if (num6 < floorX - 25 || num6 > floorX + 25)" force direction home beyond ±50. Ours lacks it except leashHome flag. **Real deviation.**
- Cliff avoidance (avoidFalling / GetWalkPrediction): ours has none — NPCs walk off platforms. Vanilla: full prediction (scan ahead tile, drop-off check, 3-tile ground check, drowning jump). Ours: missing → town NPCs will walk off cliffs/platform edges. **Deviation.**
- Jump over obstacles: ours: `if (onGround && hitWall && wantDir !== 0) vy = -6`. Vanilla: three-tier jump (-6 for 2-high, -5 for 1-high, -4.4 for half/slope), with ceiling check (SolidTilesVersatile) → if blocked, turn around instead of jumping. Ours: single -6, no ceiling check → jump spam against walls instead of turning around. Also vanilla door open before jump (door at head). Ours handles doors separately. Moderate deviation.
- Vanilla turn-on-stuck: StepUp no-op + ai[1]<100 && %10==0 → turn. Ours: hitWall → vx *= 0.5 + jump. 
- Water: vanilla drowning escape (jump out with computed velocity); ours: none for town NPC (drowning damage modeled in envHurtUpdate though).
- Vanilla "wet" speed changes for town pets/slimes; ours stationary/bound skip.

**4. Dialogue triggers**:
- Player talk: ✓ (talking → face player, stand).
- NPC↔NPC chat pairs (ai[0]=3/4 1/300; 16/17 1/1800 with emotes): need to check our Game.tickNpcEmotes — memory says EmoteBubble module exists with spawnEmote. But do we have the pair-chat state (two NPCs facing each other, 420×(1..3 or 1..4) duration)? Need to check.
- Face player randomly (ai[0]=7, 1/1200, 220 ticks): need to check.
- Party girl (208/party) state 6 (1/1200 → face player 300 ticks): check.
- Bartender state 18 (1/600): check.
- Random emote state 2 (1/1800, 45 ticks... ai[1]=45*Next(1,2)=45): check.
- Name replacement: our dialogue box? Game.talkToNearbyNpc — need to check chat text handling (button selection etc. is shop UI — separate).
- Also "talkNPC while walking" — vanilla sets ai[0]=0, ai[1]=300, localAI[3]=100, faces player (num9). Ours: talking → vx *= 0.6, wanderT=0 — vx *= 0.6 is wrong vs vanilla velocity.X *= 0.8 in state 0 decel chain ±0.1. Minor.

**5. Teleport home**: ours approximates. Vanilla conditions: `!homeless && townNPC && (flag || dungeon floor) && !IsInAGoodRestingSpot` + no player intersecting TWO rectangles: NPC bbox expanded by safeRangeX/Y (sWidth/sHeight = screen dims? sWidth= Main.screenWidth? Let me check what sWidth/sHeight/safeRangeX are — likely NPC sprite width... Actually `sWidth` and `sHeight` — in NPC.cs these are fields? There are `width`/`height`. Let me grep sWidth in NPC.cs). Our version: distance > 42 tiles from NPC and from home. Rectangle vs circle — approximation, but roughly OK? The vanilla rectangle is sWidth+safeRangeX*2 — need to check what sWidth is. If sWidth is the screen width (e.g. 1920+?), hmm. Let me check.
- Also vanilla: teleport only if BOTH rects (at NPC pos and at home spot) have no player. Ours ✓ both.
- Vanilla: TeleportToHome tries homeFloorX-1/0/+1 (switch order: i=0→0, 1→-1, 2→1 → order is 0,-1,1) with SolidTiles check 3 wide × 3 tall above floor; ours ✓ [0,-1,1] same order! ✓. But vanilla: if all blocked → homeless=true + QuickFindHome; ours: just gives up (moved=false). Deviation (minor).
- Vanilla teleports also for Guide when on dungeon floor tile (type 37 special).
- Note: vanilla gate is `!homeless && townNPC` — ours checks `this.home` only (homeless NPCs in our impl have home? need to check how home assigned — homeless NPCs with home==null skip). Also vanilla IsInAGoodRestingSpot — ours ±4 tiles approx. Fine.

**6. Party**: 
- Party hats (drawPartyHat + sittingHatY) ✓.
- Dancing? Let me check vanilla: during party, NPCs dance? There's the "party" dance where NPCs bob? I recall NPCs during party show emotes and wear hats; also "PartyIsUp" gate for the state 6 chat. Also gathering at party center? Yes! During parties, town NPCs walk toward the party center (BirthdayParty.PartyCenter) — let me check Main.cs/NPC.cs for PartyCenter usage in AI_007. Hmm, I didn't see it in AI_007. Let me grep "PartyIsUp" and "partyCenter" in NPC.cs.
- Shopping discount: during party, price multiplier? Let me grep in Player/ShoppingSettings? There IS a party discount? I don't think vanilla has a discount. Let me check.

**7. Pushed by players**: vanilla — do players push NPCs? I don't believe there's player→NPC push. NPC↔NPC collision: vanilla NPCs don't collide with each other. There IS "NPC pushed by... " hmm. In vanilla, town NPCs can be moved by Conveyor belts! And by minecarts? Let me check: NPC.cs has conveyor handling ("num243" velocity.X adjustments on conveyors). Player pushing: no. Let me verify quickly by grepping "Conveyor" in NPC.cs.

**8. Death**: town NPC death in vanilla:
- Drops: townNPC drop nothing except money? Vanilla: `if (townNPC)` in NPCLoot: drops nothing, but the Guide voodoo... Also "dropItemNorm"... Actually town NPCs drop nothing (except unspecific). Let me check NPCLoot townNPC branch.
- Respawn: vanilla town NPC respawn: Main.UpdateTime_SpawnTownNPCs — checks every second (Main.checkForSpawns?), needs housing available, spawn delay: "NPC.spawnRateForTownNPCs"? There's a timer: town NPCs respawn if conditions met — new NPC spawns when a house is empty and the NPC is unlocked — with 1 check per in-game... let me look at Main.cs UpdateTime / checkTownNPCs. There's `Main.checkForSpawns` counter and `TownNPCSpawnRate`? Ours: "重新入驻，≈次日回归" per comment. Need to check Game.ts respawn logic for town NPCs.

**9. Defense posture/cowering**: vanilla town NPCs when danger close & can't flee (state 8) — they use "cowering" frames? Hmm — state 8 is just standing (velocity 0). But there's also the "frightened" behavior. And defense posture "护头"? Actually item 10 in task: "受击护头?" — town NPCs crouch when hurt? I don't recall vanilla town NPCs having a hit-flinch animation... There IS a "hurt" frame for NPCs? Vanilla NPC FindFrame: town NPC frame when velocity... no special hurt frames. But there IS the "scared" frame for 633? Let me not overreach: task asks to check. Let me search for evidence.

Actually — I remember: vanilla town NPCs DO have a cower animation when enemies are near (the "NPC frightened" with hands over head) — it's in FindFrame? Let me grep "cower" — hmm I don't think "cower" exists in decompiled. Let me search FindFrame ai[0]==8. Let me look at FindFrame town branch for state 8 — the frames used. Let me read NPC.cs FindFrame around 70172.

**10. Hit flash / knockback / liquids**: 
- Ours: hurt() — dmg − def*0.5 floor 1, iframes 8, knockback kbx*0.6, no hit flash white (we spawn particles). Vanilla: StrikeNPC → HitEffect; immunity frames for town NPC? NPC.immune[255]: default immunity = 10 ticks? Actually NPC immunity: `immune[255]` general cooldown 10 ticks on hit (hitDuration?). For townNPC hit by projectile: immunity = 10. Vanilla knockback for town NPCs: townNPC resist? There's "if (townNPC) knockBack *= 0.6"? Hmm — actually NPC.StrikeNPC has knockBack resist via `knockBack *= (1 - knockBackResist)`. Town NPCs have no special resist. 
- Honey: vanilla NPC in honey gets slowed? NPC honeyWet → velocity *= ? For NPCs: honey slows movement (NPC.aiStyle 7 wet handling? no). In Entity/NPC update: if honeyWet, velocity *= 0.9? Hmm. Our npcLiquid.ts — need to check it's for Enemy. TownNPC envHurtUpdate handles lava + drowning but NOT honey slow and NOT lava OnFire buff (noted). Honey for town NPCs: vanilla NPC honeyWet has no damage, but movement? Let me check.

Let me now also check our Game.ts for: town NPC respawn, emote/chat pair, party behaviors, dialogue trigger cooldowns. And Renderer for sitting draw position (sittingManager equivalent). Let me grep relevant parts.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:35:38.261Z · glm-x-preview-260804

```
现在让我检查原版中关于 FindFrame 城镇分支（坐姿帧）、sittingManager 绘制、派对行为以及 NPC 与 NPC 之间聊天状态的部分。
```


---

## 🤖 Assistant · 2026-08-17T04:35:38.730Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '70172,70270p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla FindFrame town NPC branch"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:35:38.764Z

**📎 ToolResult**

```
							if (num108 > 7)
							{
								num108 = 0;
							}
						}
						frame.Y = num108 * num;
					}
					else if (type == 140 || type == 489)
					{
						frame.Y = num;
						frameCounter = 0.0;
					}
					else
					{
						frame.Y = 0;
						frameCounter = 0.0;
					}
				}
				else
				{
					int num109 = 6;
					if (type == 632)
					{
						num109 = 12;
					}
					if (type == 534)
					{
						num109 = 12;
					}
					if (type == 638)
					{
						num109 = 12;
					}
					if (type == 656)
					{
						num109 = 12;
					}
					if (flag7)
					{
						num109 = 12;
					}
					if (type == 489)
					{
						num109 = 8;
						frameCounter += Math.Abs(velocity.X) * 1f;
						frameCounter += 0.5;
					}
					else
					{
						frameCounter += Math.Abs(velocity.X) * 2f;
						frameCounter += 1.0;
					}
					if (type == 462)
					{
						num109 = 9;
					}
					int num110 = num * 2;
					if (type == 638)
					{
						num110 = num * 9;
					}
					if (type == 656)
					{
						num110 = num;
					}
					if (flag7)
					{
						num110 = num;
					}
					if (frame.Y < num110)
					{
						frame.Y = num110;
					}
					if (frameCounter > (double)num109)
					{
						frame.Y += num;
						frameCounter = 0.0;
					}
					if (frame.Y / num >= Main.npcFrameCount[type] - num57)
					{
						frame.Y = num110;
					}
				}
				break;
			}
			if (type == 462)
			{
				frameCounter = 0.0;
				if (velocity.Y < 0f)
				{
					frame.Y = num;
				}
				else
				{
					frame.Y = num * 2;
				}
				break;
			}
			if (flag7)

```


---

## 🤖 Assistant · 2026-08-17T04:35:39.896Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"PartyIsUp\\|partyCenter\\|PartyCenter\\|BirthdayParty\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -20; echo === ; grep -n \"sWidth\\|safeRangeX\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -10",
 "description": "Search party and safeRange in vanilla NPC.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:35:39.930Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
1552:				else if (BirthdayParty.PartyIsUp && Main.rand.Next(3) != 0)
2503:					else if (!flag11 && BirthdayParty.PartyIsUp && Main.rand.Next(3) != 0)
4199:							else if (BirthdayParty.PartyIsUp && Main.rand.Next(3) != 0)
55705:			else if (!NPCID.Sets.IsTownPet[type] && flag30 && ai[0] == 0f && velocity.Y == 0f && Main.rand.Next(1200) == 0 && (type == 208 || (BirthdayParty.PartyIsUp && NPCID.Sets.AttackType[type] == NPCID.Sets.AttackType[208])))
60854:					else if (BirthdayParty.GenuineParty && (double)base.Center.Y < Main.worldSurface * 16.0)
67241:			return BirthdayParty.PartyIsUp;
91255:			bool flag = BirthdayParty.PartyIsUp || ForcePartyHatOn;
96088:		if (BirthdayParty.PartyIsUp && Main.rand.Next(3) == 0 && !NPCID.Sets.HasNoPartyText[type] && GetSpecialEventTextIfNotEmpty(specialTextCategoryKey + "SpecialText.Party", ref specialEventText))
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-17T04:35:44.265Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me find the sitting frame in FindFrame and the sWidth/safeRangeX definition. Also check 1552 and 1503 region (emote selection during party), 60854 (party center gathering). Let me look at those.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:35:45.292Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"sWidth\\|safeRangeX\\|safeRangeY\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head; echo ===; sed -n '60840,60890p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Find sWidth fields and party center logic"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:35:45.328Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
843:			int num = (int)((double)(sWidth / 16) * 0.7);
845:			safeRangeX = (int)((double)(sWidth / 16) * 0.52);
846:			safeRangeY = (int)((double)(sHeight / 16) * 0.52);
866:				num += (int)((double)(sWidth / 16) * 0.5 / (double)num3);
868:				safeRangeX += (int)((double)(sWidth / 16) * 0.5 / (double)num3);
869:				safeRangeY += (int)((double)(sHeight / 16) * 0.5 / (double)num3);
872:			safeArea = Utils.CenteredRectangle(player.position.ToTileCoordinates(), new Point(safeRangeX * 2, safeRangeY * 2));
875:				safeArea = Utils.CenteredRectangle(player.position.ToTileCoordinates(), new Point(safeRangeX, safeRangeY));
5347:			int num = sWidth / 2;
5354:					Rectangle value = new Rectangle((int)(player.Center.X - (float)num - (float)safeRangeX), (int)(player.Center.Y - (float)num2 - (float)safeRangeY), sWidth + safeRangeX * 2, sHeight + safeRangeY * 2);
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-17T04:35:46.533Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"ai\\[0\\] == 5f\\|sittingManager\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head -20; echo ===; grep -n \"AnchoredEntitiesPosition\\|PlayerSittingHelper\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head",
 "description": "Find sitting draw handling in Main.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:35:46.583Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
2198:	public static AnchoredEntitiesCollection sittingManager;
6420:		sittingManager = new AnchoredEntitiesCollection();
17678:		sittingManager.ClearPlayerAnchors();
17739:		sittingManager.ClearNPCAnchors();
22010:		if (theNPC.townNPC && theNPC.ai[0] == 5f)
23972:						if (rCurrentNPC.ai[0] == 0f || rCurrentNPC.ai[0] == 5f || rCurrentNPC.ai[0] == 10f)
24178:					if (rCurrentNPC.ai[0] == 5f && rCurrentNPC.ai[1] >= 0f && rCurrentNPC.ai[1] < 30f)
24844:					else if (type == 421 && rCurrentNPC.ai[0] == 5f)
25548:						if ((int)rCurrentNPC.ai[0] == 4 || rCurrentNPC.ai[0] == 5f || rCurrentNPC.ai[0] == 6f)
26968:			if (n.ai[0] == 5f)
27005:			if (n.type == 550 && n.ai[0] == 5f)
33326:					if (proj.ai[0] == 5f)
37569:			else if (npc[i].type == 421 && npc[i].ai[0] == 5f)
42559:		if (npc[i].type == 637 && npc[i].ai[0] == 5f)
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-17T04:35:49.619Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting: Main.cs:24178 — `rCurrentNPC.ai[0] == 5f && rCurrentNPC.ai[1] >= 0f && rCurrentNPC.ai[1] < 30f` — probably sitting down animation (first 30 ticks). Let me read Main.cs 22010 region (DrawNPC sitting) and 24178 region.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:35:50.597Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '22000,22040p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs; echo ======; sed -n '24160,24230p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "description": "Read DrawNPC sitting handling in Main.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:35:50.638Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
		switch (theNPC.type)
		{
		case 269:
		case 270:
		case 271:
		case 274:
		case 277:
			num -= 2f;
			break;
		}
		if (theNPC.townNPC && theNPC.ai[0] == 5f)
		{
			num -= 4f;
			if (theNPC.type == 124)
			{
				num -= 2f;
			}
			if (theNPC.type == 637 || theNPC.type == 656 || NPCID.Sets.IsTownSlime[theNPC.type])
			{
				num -= 10f;
			}
		}
		if (theNPC.type == 671 || theNPC.type == 672 || theNPC.type == 673 || theNPC.type == 674 || theNPC.type == 675)
		{
			num += 10f;
		}
		return num * theNPC.scale;
	}

	internal void DrawProjectiles()
	{
		TimeLogger.StartTimestamp fromTimestamp = TimeLogger.Start();
		spriteBatch.Begin(SpriteSortMode.Deferred, BlendState.AlphaBlend, DefaultSamplerState, DepthStencilState.None, Rasterizer, null, Transform);
		CurrentDrawnEntity = null;
		CurrentDrawnEntityShader = 0;
		for (int i = 0; i < 1000; i++)
		{
			Projectile projectile = Main.projectile[i];
			if (!projectile.active || projectile.type <= 0 || projectile.hide || projectile.drawLayer != 0)
			{
				continue;
(eval):1: ===== not found

```


---

## 🤖 Assistant · 2026-08-17T04:35:53.654Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '24150,24240p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "description": "Read sitting NPC draw adjustment Main.cs 24150-24240"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:35:53.680Z

**📎 ToolResult**

```
					else if (rCurrentNPC.ai[0] == 1f)
					{
						white6 = Microsoft.Xna.Framework.Color.White;
						amount9 = 0.5f;
						num244 = 4;
						num245 = 2;
						num246 = 1;
					}
					else
					{
						color41 = npcColor;
					}
					for (int num247 = num246; num247 < num244; num247 += num245)
					{
						_ = ref rCurrentNPC.oldPos[num247];
						Microsoft.Xna.Framework.Color value71 = color41;
						value71 = Microsoft.Xna.Framework.Color.Lerp(value71, white6, amount9);
						value71 = rCurrentNPC.GetAlpha(value71);
						value71 *= (float)(num244 - num247) / (float)num244;
						value71.A = 100;
						Vector2 position28 = rCurrentNPC.oldPos[num247] + new Vector2(rCurrentNPC.width, rCurrentNPC.height) / 2f - screenPos;
						position28 -= rectangle12.Size() * rCurrentNPC.scale / 2f;
						position28 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
						mySpriteBatch.Draw(value70, position28, rectangle12, value71, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
					}
					int num248 = 0;
					float num249 = 0f;
					float num250 = 0f;
					if (rCurrentNPC.ai[0] == 5f && rCurrentNPC.ai[1] >= 0f && rCurrentNPC.ai[1] < 30f)
					{
						num248 = 4;
						num249 = 1f - (float)Math.Cos((rCurrentNPC.ai[1] - 0f) / 30f * MathF.PI);
						num249 /= 2f;
						num250 = 70f;
					}
					for (int num251 = 0; num251 < num248; num251++)
					{
						Microsoft.Xna.Framework.Color value72 = npcColor;
						value72 = Microsoft.Xna.Framework.Color.Lerp(value72, white6, amount9);
						value72 = rCurrentNPC.GetAlpha(value72);
						value72 *= 1f - num249;
						Vector2 position29 = rCurrentNPC.Center + ((float)num251 / (float)num248 * (MathF.PI * 2f) + rCurrentNPC.rotation).ToRotationVector2() * num250 * num249 - screenPos;
						position29 -= new Vector2(value69.Width, value69.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
						position29 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
						mySpriteBatch.Draw(value70, position29, rectangle12, value72, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
					}
					Vector2 position30 = rCurrentNPC.Center - screenPos;
					position30 -= new Vector2(value69.Width, value69.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
					position30 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
					mySpriteBatch.Draw(value69, position30, rCurrentNPC.frame, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
					break;
				}
				case 392:
				case 393:
				case 394:
				case 395:
				{
					Texture2D value62 = TextureAssets.Npc[type].Value;
					Vector2 vec = rCurrentNPC.Center - screenPos + Vector2.UnitY * rCurrentNPC.gfxOffY;
					vec = vec.Floor();
					float num225 = 0f;
					if (type == 393)
					{
						num225 = -8f;
					}
					mySpriteBatch.Draw(value62, vec, rCurrentNPC.frame, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize + Vector2.UnitY * num225, rCurrentNPC.scale, spriteEffects, 0f);
					if (type == 392)
					{
						mySpriteBatch.Draw(TextureAssets.GlowMask[48].Value, vec, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(200, 200, 200, 0), rCurrentNPC.rotation, halfSize + Vector2.UnitY * num225, rCurrentNPC.scale, spriteEffects, 0f);
					}
					if (type == 395)
					{
						mySpriteBatch.Draw(TextureAssets.GlowMask[49].Value, vec, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(200, 200, 200, 0), rCurrentNPC.rotation, halfSize + Vector2.UnitY * num225, rCurrentNPC.scale, spriteEffects, 0f);
					}
					if (type == 394)
					{
						mySpriteBatch.Draw(TextureAssets.GlowMask[50].Value, vec, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(200, 200, 200, 0), rCurrentNPC.rotation, halfSize + Vector2.UnitY * num225, rCurrentNPC.scale, spriteEffects, 0f);
					}
					break;
				}
				case 83:
				case 84:
				case 179:
					mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46), rCurrentNPC.frame, Microsoft.Xna.Framework.Color.White, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
					break;
				case 87:
				case 88:
				case 89:
				case 90:
				case 91:
				case 92:

```


---

## 🤖 Assistant · 2026-08-17T04:35:59.485Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
That was a special-effect case (TownNPC shadow clones for... 392-395? no this was for a specific type). The ai[0]==5 with ai[1]<30 circle effect is for a special NPC type (probably 666?). Not the general sitting draw.

The general sitting: `Main.sittingManager.AddNPC` — the sitting manager adjusts the draw offset. Let me check PlayerSittingHelper usage for NPCs — in Main.DrawNPC: there's `sittingManager.GetNextPlayersIndex`... Let me search how sittingManager affects NPC drawing. Search "sitting" in Main.cs around DrawNPC.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:36:00.869Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"sitting\\.\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head -20; echo ===; grep -rn \"sittingManager\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/PlayerSittingHelper.cs 2>/dev/null | head; ls ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ | grep -i sit",
 "description": "Find sitting manager usage and PlayerSittingHelper file"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:36:00.899Z

**📎 ToolResult**

```
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-17T04:36:03.230Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The `===` in the echo is causing zsh issues ("== not found"). Let me avoid that.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:36:04.079Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"sitting\\.\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head -20; ls ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ | grep -i -E \"sit|anchor\"",
 "description": "Find sitting usage in Main.cs and helper files"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:36:04.118Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-17T04:36:07.776Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"PlayerSittingHelper\" ~/Project/GLM/SandboxWorld/Terarria1456/ --include=\"*.cs\" -l | head; grep -rn \"class AnchoredEntitiesCollection\" ~/Project/GLM/SandboxWorld/Terarria1456/ --include=\"*.cs\" | head -3",
 "description": "Locate PlayerSittingHelper class file"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:36:07.864Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/PlayerSittingHelper.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/AnchoredEntitiesCollection.cs:6:public class AnchoredEntitiesCollection

```


---

## 🤖 Assistant · 2026-08-17T04:36:13.509Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"sitting\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/PlayerSittingHelper.cs | head -30; echo ---; sed -n '1,80p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/PlayerSittingHelper.cs",
 "description": "Read PlayerSittingHelper for NPC sitting draw semantics"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:36:13.542Z

**📎 ToolResult**

```
16:	public int sittingIndex;
22:			posOffset = new Vector2(sittingIndex * player.direction * 8, (float)sittingIndex * player.gravDir * -4f);
66:		if (Main.sittingManager.GetNextPlayerStackIndexInCoords(coords) >= 2)
86:		Main.sittingManager.AddPlayerAndGetItsStackedIndexInCoords(player.whoAmI, coords, out sittingIndex);
95:			sittingIndex = -1;
114:			flag &= Main.sittingManager.GetNextPlayerStackIndexInCoords((playerSittingPosition + new Vector2(0f, -2f)).ToTileCoordinates()) < 2;
136:		Main.sittingManager.AddPlayerAndGetItsStackedIndexInCoords(player.whoAmI, new Point(x, y), out sittingIndex);
---
using Microsoft.Xna.Framework;
using Terraria.ID;

namespace Terraria.GameContent;

public struct PlayerSittingHelper
{
	public const int ChairSittingMaxDistance = 40;

	public bool isSitting;

	public ExtraSeatInfo details;

	public Vector2 offsetForSeat;

	public int sittingIndex;

	public void GetSittingOffsetInfo(Player player, out Vector2 posOffset, out float seatAdjustment)
	{
		if (isSitting)
		{
			posOffset = new Vector2(sittingIndex * player.direction * 8, (float)sittingIndex * player.gravDir * -4f);
			seatAdjustment = -4f;
			seatAdjustment += (int)offsetForSeat.Y;
			posOffset += offsetForSeat * player.Directions;
		}
		else
		{
			posOffset = Vector2.Zero;
			seatAdjustment = 0f;
		}
	}

	public bool TryGetSittingBlock(Player player, out Tile tile)
	{
		tile = null;
		if (!isSitting)
		{
			return false;
		}
		Point pt = (player.Bottom + new Vector2(0f, -2f)).ToTileCoordinates();
		if (!GetSittingTargetInfo(player, pt.X, pt.Y, out var _, out var _, out var _, out var _))
		{
			return false;
		}
		tile = Framing.GetTileSafely(pt);
		return true;
	}

	public void UpdateSitting(Player player)
	{
		if (!isSitting)
		{
			return;
		}
		Point coords = (player.Bottom + new Vector2(0f, -2f)).ToTileCoordinates();
		if (!GetSittingTargetInfo(player, coords.X, coords.Y, out var targetDirection, out var _, out var seatDownOffset, out var extraInfo))
		{
			SitUp(player);
			return;
		}
		if (player.controlLeft || player.controlRight || player.controlUp || player.controlDown || player.controlJump || player.pulley || player.mount.Active || targetDirection != player.direction)
		{
			SitUp(player);
		}
		if (Main.sittingManager.GetNextPlayerStackIndexInCoords(coords) >= 2)
		{
			SitUp(player);
		}
		if (!isSitting)
		{
			return;
		}
		if (Main.netMode != 1 && !Main.IsItDay())
		{
			int num = 2322;
			int num2 = 2358;
			Tile tile = Main.tile[coords.X, coords.Y];
			if (tile.type == 89 && tile.frameX >= num && tile.frameX <= num2)
			{

```


---

## 🤖 Assistant · 2026-08-17T04:36:16.531Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This is player sitting. For NPCs, the sittingManager.AddNPC is used for what? Probably for stacking visual (NPCs sitting at same seat offset). Let me check how NPC sitting draw offset is applied — search in Main.cs for "GetNPCStackIndex" or similar. Actually let me search AnchoredEntitiesCollection usage for NPC draw offset.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:36:17.523Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"AddNPC\\|NPCStackIndex\\|GetNextNPCStack\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/AnchoredEntitiesCollection.cs | head; echo ---; grep -rn \"sittingManager\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Check AnchoredEntitiesCollection NPC stacking API"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:36:17.573Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/AnchoredEntitiesCollection.cs:37:	public void AddNPC(int npcIndex, Point coords)
---
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:54701:					Main.sittingManager.AddNPC(whoAmI, coords);

```


---

## 🤖 Assistant · 2026-08-17T04:36:21.537Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"AddNPC\\|npcIndexToMap\\|GetNextPlayerStackIndex\\|GetNPC\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/AnchoredEntitiesCollection.cs; echo ---; grep -rn \"sittingManager\\|SittingIndex\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head; grep -n \"seatDownOffset\\|offsetForSeat\" ~/Project/GLM/SandboxWorld/Terarria1456/Terrarria.GameContent/PlayerSittingHelper.cs | head",
 "description": "Check NPC sitting stack consumption"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:36:21.583Z

**📎 ToolResult**

```
37:	public void AddNPC(int npcIndex, Point coords)
46:	public int GetNextPlayerStackIndexInCoords(Point coords)
---
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:54701:					Main.sittingManager.AddNPC(whoAmI, coords);
ugrep: warning: ~/Project/GLM/SandboxWorld/Terarria1456/Terrarria.GameContent/PlayerSittingHelper.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-17T04:36:26.468Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The sittingManager.AddNPC registers NPCs per seat coordinates — used to prevent multiple NPCs sitting on the same chair (occupancy check happens in the entry paths via "any NPC with ai[0]==5 at same tile" — wait, those checks scan NPCs directly, not the manager). Actually the manager is used by PlayerSittingHelper.GetNextPlayerStackIndexInCoords for players (max 2 per seat). AddNPC registers NPC anchors so players won't stack on NPC-occupied seats? Let me quickly check where the npc anchors are consumed: ClearNPCAnchors in Main (17740) each frame, and... let me check.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:36:28.056Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1,80p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/AnchoredEntitiesCollection.cs; grep -n \"FilledSeats\\|seat\\|Seat\" ~/Project/GLM/SandboxWorld/Terarria1456/Terrarria.GameContent/PlayerSittingHelper.cs | head",
 "description": "Read AnchoredEntitiesCollection"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:36:28.091Z

**📎 ToolResult**

```
using System.Collections.Generic;
using Microsoft.Xna.Framework;

namespace Terraria.DataStructures;

public class AnchoredEntitiesCollection
{
	private struct IndexPointPair
	{
		public int index;

		public Point coords;
	}

	private List<IndexPointPair> _anchoredNPCs;

	private List<IndexPointPair> _anchoredPlayers;

	public int AnchoredPlayersAmount => _anchoredPlayers.Count;

	public AnchoredEntitiesCollection()
	{
		_anchoredNPCs = new List<IndexPointPair>();
		_anchoredPlayers = new List<IndexPointPair>();
	}

	public void ClearNPCAnchors()
	{
		_anchoredNPCs.Clear();
	}

	public void ClearPlayerAnchors()
	{
		_anchoredPlayers.Clear();
	}

	public void AddNPC(int npcIndex, Point coords)
	{
		_anchoredNPCs.Add(new IndexPointPair
		{
			index = npcIndex,
			coords = coords
		});
	}

	public int GetNextPlayerStackIndexInCoords(Point coords)
	{
		return GetEntitiesInCoords(coords);
	}

	public void AddPlayerAndGetItsStackedIndexInCoords(int playerIndex, Point coords, out int stackedIndexInCoords)
	{
		stackedIndexInCoords = GetEntitiesInCoords(coords);
		_anchoredPlayers.Add(new IndexPointPair
		{
			index = playerIndex,
			coords = coords
		});
	}

	private int GetEntitiesInCoords(Point coords)
	{
		int num = 0;
		for (int i = 0; i < _anchoredNPCs.Count; i++)
		{
			if (_anchoredNPCs[i].coords == coords)
			{
				num++;
			}
		}
		for (int j = 0; j < _anchoredPlayers.Count; j++)
		{
			if (_anchoredPlayers[j].coords == coords)
			{
				num++;
			}
		}
		return num;
	}
}
ugrep: warning: ~/Project/GLM/SandboxWorld/Terarria1456/Terrarria.GameContent/PlayerSittingHelper.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-17T04:36:33.413Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
OK — sittingManager is only for stack index (players sitting get offset; NPCs sitting at same coords as a player get counted). It's a rendering/occupancy nicety; not core behavior. Our comment already notes this is skipped ("无对应渲染载体，略").

Now the more important thing: **what frame does a sitting town NPC use?** Let me look at FindFrame for ai[0]==5 — grep in FindFrame region. The FindFrame town branch I saw handles standing/walking. Let me check for the sitting frame — search "ai[0] == 5f" in NPC.cs around FindFrame (line ~69000-70300).
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:36:34.543Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "awk 'NR>=69000 && NR<=70300 && /ai\\[0\\] == 5f|sitting|frame.Y = 0|num57/' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head; grep -n \"num57 = \" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -5",
 "description": "Find sitting frame in FindFrame"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:36:34.615Z

**📎 ToolResult**

```
					frame.Y = 0;
			int num57 = (isLikeATownNPC ? NPCID.Sets.ExtraFramesCount[type] : 0);
						frame.Y = 0;
						frame.Y = 0;
						frame.Y = 0;
							frame.Y = 0;
						frame.Y = 0;
				else if (ai[0] == 5f)
						frame.Y = 0;
						frame.Y = 0;
5022:						int num57 = Main.rand.Next(4);
20592:						float num57 = Math.Abs(velocity.Y);
46535:				int num57 = num37++;
52216:			float num57 = num46 * 1.3f;
54945:			int num57 = 0;

```


---

## 🤖 Assistant · 2026-08-17T04:36:37.969Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"else if (ai\\[0\\] == 5f)\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; sed -n '70100,70172p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read FindFrame sitting frame branch"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:36:38.008Z

**📎 ToolResult**

```
62538:		else if (ai[0] == 5f)
68025:			else if (ai[0] == 5f)
69638:				else if (ai[0] == 5f)
70714:			else if (ai[0] == 5f)
70889:			else if (ai[0] == 5f)
78050:			else if (ai[0] == 5f)
						if (num104 == 1)
						{
							Main.npc[(int)ai[2]].localAI[2] += 1f;
							num100++;
						}
						int num106 = Utils.SelectRandom<int>(Main.rand, 38, 37, 36);
						int num107 = num106;
						switch (num104)
						{
						case 0:
							switch (num106)
							{
							case 38:
								num107 = 37;
								break;
							case 37:
								num107 = 36;
								break;
							case 36:
								num107 = 38;
								break;
							}
							break;
						case 1:
							switch (num106)
							{
							case 38:
								num107 = 36;
								break;
							case 37:
								num107 = 38;
								break;
							case 36:
								num107 = 37;
								break;
							}
							break;
						}
						if (num103 == 0)
						{
							if (num99 >= 2)
							{
								num106 -= 3;
							}
							if (num100 >= 2)
							{
								num107 -= 3;
							}
						}
						EmoteBubble.NewBubble(num106, new WorldUIAnchor(this), num96);
						EmoteBubble.NewBubble(num107, new WorldUIAnchor(Main.npc[(int)ai[2]]), num96);
					}
					frame.Y = num * (flag9 ? num95 : num95);
					if (frameCounter >= 420.0)
					{
						frameCounter = 0.0;
					}
				}
				else if (velocity.X == 0f)
				{
					if (type == 638)
					{
						int num108 = frame.Y / num;
						if (num108 > 7)
						{
							num108 = 0;
						}
						frameCounter += 1.0;
						if (frameCounter > 4.0)
						{
							frameCounter = 0.0;
							num108++;
							if (num108 > 7)

```


---

## 🤖 Assistant · 2026-08-17T04:36:41.014Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '69620,69700p' ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria/NPC.cs",
 "description": "Read FindFrame ai0==5 sitting frame branch at 69638"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:36:41.042Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
sed: ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria/NPC.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-17T04:36:43.613Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Odd — that path error again. It seems intermittent; the earlier `sed -n '70100,70172p'` worked with the same path. Maybe the file is being accessed concurrently or something weird with ugrep/sed caching? Let me retry.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:36:44.074Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '69620,69700p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"",
 "description": "Read FindFrame sitting frame branch"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:36:44.104Z

**📎 ToolResult**

```
						if (frameCounter >= 100.0 && Main.rand.Next(20) == 0)
						{
							frame.Y = 0;
							frameCounter = 0.0;
						}
					}
					else if (frame.Y / num == 0 && frameCounter >= 20.0)
					{
						frame.Y = num * (num58 - 1);
						frameCounter = 0.0;
						EmoteBubble.NewBubble(89, new WorldUIAnchor(this), 90);
					}
					else if (frame.Y != 0 && frame.Y != num * (num58 - 1))
					{
						frame.Y = 0;
						frameCounter = 0.0;
					}
				}
				else if (ai[0] == 5f)
				{
					frame.Y = num * (num58 - 3);
					if (type == 637)
					{
						frame.Y = num * 19;
					}
					frameCounter = 0.0;
				}
				else if (ai[0] == 6f)
				{
					frameCounter += 1.0;
					int num67 = frame.Y / num;
					int num60 = num58 - num67;
					if ((uint)(num60 - 1) > 1u && (uint)(num60 - 4) > 1u && num67 != 0)
					{
						frame.Y = 0;
						frameCounter = 0.0;
					}
					int num68 = 0;
					num68 = ((!(frameCounter < 10.0)) ? ((frameCounter < 16.0) ? (num58 - 5) : ((frameCounter < 46.0) ? (num58 - 4) : ((frameCounter < 60.0) ? (num58 - 5) : ((!(frameCounter < 66.0)) ? ((frameCounter < 72.0) ? (num58 - 5) : ((frameCounter < 102.0) ? (num58 - 4) : ((frameCounter < 108.0) ? (num58 - 5) : ((!(frameCounter < 114.0)) ? ((frameCounter < 120.0) ? (num58 - 5) : ((frameCounter < 150.0) ? (num58 - 4) : ((frameCounter < 156.0) ? (num58 - 5) : ((!(frameCounter < 162.0)) ? ((frameCounter < 168.0) ? (num58 - 5) : ((frameCounter < 198.0) ? (num58 - 4) : ((frameCounter < 204.0) ? (num58 - 5) : ((!(frameCounter < 210.0)) ? ((frameCounter < 216.0) ? (num58 - 5) : ((frameCounter < 246.0) ? (num58 - 4) : ((frameCounter < 252.0) ? (num58 - 5) : ((!(frameCounter < 258.0)) ? ((frameCounter < 264.0) ? (num58 - 5) : ((frameCounter < 294.0) ? (num58 - 4) : ((frameCounter < 300.0) ? (num58 - 5) : 0))) : 0)))) : 0)))) : 0)))) : 0)))) : 0)))) : 0);
					if (num68 == num58 - 4 && num67 == num58 - 5)
					{
						Vector2 vector2 = base.Center + new Vector2(10 * direction, -4f);
						for (int l = 0; l < 8; l++)
						{
							int num69 = Main.rand.Next(139, 143);
							int num70 = Dust.NewDust(vector2, 0, 0, num69, velocity.X + (float)direction, velocity.Y - 2.5f, 0, default(Color), 1.2f);
							Main.dust[num70].velocity.X += (float)direction * 1.5f;
							Dust dust = Main.dust[num70];
							dust.position -= new Vector2(4f);
							dust = Main.dust[num70];
							dust.velocity *= 2f;
							Main.dust[num70].scale = 0.7f + Main.rand.NextFloat() * 0.3f;
						}
					}
					frame.Y = num * num68;
					if (frameCounter >= 300.0)
					{
						frameCounter = 0.0;
					}
				}
				else if ((ai[0] == 7f || ai[0] == 19f) && !NPCID.Sets.IsTownPet[type])
				{
					frameCounter += 1.0;
					int num71 = frame.Y / num;
					int num60 = num58 - num71;
					if ((uint)(num60 - 1) > 1u && (uint)(num60 - 4) > 1u && num71 != 0)
					{
						frame.Y = 0;
						frameCounter = 0.0;
					}
					int num72 = 0;
					if (frameCounter < 16.0)
					{
						num72 = 0;
					}
					else if (frameCounter == 16.0)
					{
						EmoteBubble.NewBubbleNPC(new WorldUIAnchor(this), 112);
					}
					else if (frameCounter < 128.0)
					{

```


---

## 🤖 Assistant · 2026-08-17T04:37:00.115Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Excellent — this is the FindFrame town NPC section. Key findings:
- ai[0]==5 (sitting): `frame.Y = num * (num58 - 3)` where num58 = npcFrameCount - ExtraFramesCount... let me figure out: num58 is probably the "total frames including extra" — sitting frame = (num58-3). For a standard town NPC sheet: frames = npcFrameCount, num58 = Main.npcFrameCount[type]... Let me check what num58 is. And 637 (town pet?) gets frame 19.
- ai[0]==6 (party dance / facing player 208): full dancing animation with a 300-tick frameCounter timeline, music note dust (139-143)! This is the party dance. num68 timeline: frames num58-5 / num58-4 alternating every ~30 ticks → this is the DANCING animation (bobbing), plus dust sparkles. State 6 = dancing (party girl & during party when AttackType matches 208 — actually the trigger at :55705 requires type==208 OR (PartyIsUp && AttackType[type]==AttackType[208]) — wait, that reads: `type == 208 || (BirthdayParty.PartyIsUp && NPCID.Sets.AttackType[type] == NPCID.Sets.AttackType[208])`. Hmm what's AttackType[208]? Party Girl throws... Let me check: AttackType for party girl = 0? No wait — the state 6 with dance — this applies to ALL town NPCs during a party! (If their AttackType matches party girl's = 1 (thrown)). So during party, town NPCs with thrown attack type dance near players. Wait but party dancing in vanilla happens at the party center for all NPCs... this is the actual implementation: NPC near player during party → ai[0]=6 → dance animation. Yes!
- ai[0]==7/19 (facing player): emote 112 (chat bubble?) at frameCounter==16.

So our implementation needs: sitting frame (num58-3), party dance state 6, face-player emote 7. Let me check what num58 is. Let me find num58 assignment in FindFrame.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:37:00.965Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "awk 'NR>=69400 && NR<=69640' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | grep -n \"num58\\|num = \\|ai\\[0\\] == 3f\\|ai\\[0\\] == 16f\" | head -20",
 "description": "Find num58 definition in FindFrame"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:37:01.038Z

**📎 ToolResult**

```
181:					if (frame.Y / num == num58 - 1 && frameCounter >= 5.0)
188:						frame.Y = num * (num58 - 1);
191:					else if (frame.Y != 0 && frame.Y != num * (num58 - 1))
200:					if (frame.Y / num == num58 - 1 && frameCounter >= 50.0)
229:						frame.Y = num * (num58 - 1);
233:					else if (frame.Y != 0 && frame.Y != num * (num58 - 1))
241:					frame.Y = num * (num58 - 3);

```


---

## 🤖 Assistant · 2026-08-17T04:37:01.549Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '69440,69560p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"",
 "description": "Read FindFrame town branch start"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:37:01.581Z

**📎 ToolResult**

```
							}
						}
						break;
					case 21:
						if (type == 656)
						{
							if (ai[1] > 30f && (num62 < 10 || num62 > 16))
							{
								num62 = 10;
							}
							if (num62 > 0)
							{
								frameCounter += 1.0;
							}
							if (frameCounter > 4.0)
							{
								frameCounter = 0.0;
								num62++;
								if (num62 > 13 && ai[1] > 30f)
								{
									num62 = 13;
								}
								if (num62 > 16)
								{
									num62 = 0;
								}
							}
						}
						if (type == 637)
						{
							if (ai[1] > 30f && (num62 < 17 || num62 > 21))
							{
								num62 = 17;
							}
							if (num62 > 0)
							{
								frameCounter += 1.0;
							}
							if (frameCounter > 4.0)
							{
								frameCounter = 0.0;
								num62++;
								if (num62 > 19 && ai[1] > 30f)
								{
									num62 = 19;
								}
								if (num62 > 21)
								{
									num62 = 0;
								}
							}
						}
						if (type != 638)
						{
							break;
						}
						if (ai[1] > 30f && (num62 < 17 || num62 > 22))
						{
							num62 = 17;
						}
						if (num62 > 0)
						{
							frameCounter += 1.0;
						}
						if (frameCounter > 4.0)
						{
							frameCounter = 0.0;
							num62++;
							if (num62 > 21 && ai[1] > 30f)
							{
								num62 = 18;
							}
							if (num62 > 22)
							{
								num62 = 0;
							}
						}
						break;
					case 22:
						if (type == 656)
						{
							int num63 = Main.npcFrameCount[type];
							if (ai[1] > 40f && (num62 < 17 || num62 >= num63))
							{
								num62 = 17;
							}
							if (num62 > 0)
							{
								frameCounter += 1.0;
							}
							if (frameCounter > 4.0)
							{
								frameCounter = 0.0;
								num62++;
								if (num62 > 20 && ai[1] > 40f)
								{
									num62 = 19;
								}
								if (num62 >= num63)
								{
									num62 = 0;
								}
							}
						}
						if (type != 637)
						{
							break;
						}
						if (ai[1] > 30f && (num62 < 17 || num62 > 27))
						{
							num62 = 17;
						}
						if (num62 > 0)
						{
							frameCounter += 1.0;
						}
						if (frameCounter > 4.0)
						{
							frameCounter = 0.0;
							num62++;
							if (num62 > 27)

```


---

## 🤖 Assistant · 2026-08-17T04:37:03.283Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I need to find the num58 definition. Let me search in FindFrame with context.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:37:04.511Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"int num58\\|num58 =\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | head; grep -n \"int num59\\|num59 =\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | head -5",
 "description": "Find num58/num59 definitions"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:37:04.553Z

**📎 ToolResult**

```
20612:							float num58 = Math.Abs(velocity.X);
29097:						int num583 = 25;
29098:						int num584 = 100;
29106:						int num585 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector63.X, vector63.Y, num579, num580, num584, num583, 0f, Main.myPlayer);
29142:							int num588 = 25;
29143:							int num589 = 110;
47067:			float num58 = 20 - num17;
52217:			float num58 = num46 * 0.7f;
54947:			float num58 = 0f;
54971:				num58 = 0.5f;
20613:							float num59 = Math.Abs(velocity.Y);
29144:							int num590 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector64.X, vector64.Y, speedX, speedY, num589, num588, 0f, Main.myPlayer);
29202:						int num595 = 35;
29203:						int num596 = 109;
29204:						int num597 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector65.X, vector65.Y, num592, num593, num596, num595, 0f, Main.myPlayer);

```


---

## 🤖 Assistant · 2026-08-17T04:37:07.198Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "awk '/private void FindFrame/,/^\t}$/' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | grep -n \"num58\\|isLikeATownNPC ?\" | head -10",
 "description": "Find num58 in FindFrame method scope"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:37:07.320Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-17T04:37:10.185Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"public void FindFrame\\|private void FindFrame\\|void FindFrame\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"",
 "description": "Find FindFrame method location"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:37:10.209Z

**📎 ToolResult**

```
67295:	public void FindFrame()

```


---

## 🤖 Assistant · 2026-08-17T04:37:13.003Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '69330,69440p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"",
 "description": "Read FindFrame around town NPC frame variables"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:37:13.032Z

**📎 ToolResult**

```
					}
					int num61 = 0;
					num61 = ((!(frameCounter < 6.0)) ? (num58 - 4) : (num58 - 5));
					if (ai[1] < 6f)
					{
						num61 = num58 - 5;
					}
					frame.Y = num * num61;
				}
				else if (ai[0] >= 20f && ai[0] <= 22f)
				{
					int num62 = frame.Y / num;
					switch ((int)ai[0])
					{
					case 20:
						if (flag7)
						{
							if (ai[1] > 30f && (num62 < 8 || num62 > 13))
							{
								num62 = 8;
							}
							if (num62 > 0)
							{
								frameCounter += 1.0;
							}
							if (frameCounter >= 12.0)
							{
								frameCounter = 0.0;
								num62++;
								if (num62 > 13 && ai[1] > 30f)
								{
									num62 = 8;
								}
								if (num62 > 13)
								{
									num62 = 0;
								}
							}
						}
						if (type == 656)
						{
							if (ai[1] > 30f && (num62 < 7 || num62 > 9))
							{
								num62 = 7;
							}
							if (num62 > 0)
							{
								frameCounter += 1.0;
							}
							if (frameCounter > 4.0)
							{
								frameCounter = 0.0;
								num62++;
								if (num62 > 8 && ai[1] > 30f)
								{
									num62 = 8;
								}
								if (num62 > 9)
								{
									num62 = 0;
								}
							}
						}
						if (type == 637)
						{
							if (ai[1] > 30f && (num62 < 10 || num62 > 16))
							{
								num62 = 10;
							}
							if (num62 > 0)
							{
								frameCounter += 1.0;
							}
							if (frameCounter > 4.0)
							{
								frameCounter = 0.0;
								num62++;
								if (num62 > 13 && ai[1] > 30f)
								{
									num62 = 13;
								}
								if (num62 > 16)
								{
									num62 = 0;
								}
							}
						}
						if (type != 638)
						{
							break;
						}
						if (ai[1] > 30f && (num62 < 23 || num62 > 27))
						{
							num62 = 23;
						}
						if (num62 > 0)
						{
							frameCounter += 1.0;
						}
						if (frameCounter > 4.0)
						{
							frameCounter = 0.0;
							num62++;
							if (num62 > 26 && ai[1] > 30f)
							{
								num62 = 24;
							}
							if (num62 > 27)
							{
								num62 = 0;
							}

```


---

## 🤖 Assistant · 2026-08-17T04:37:15.047Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '69150,69330p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"",
 "description": "Read FindFrame town states 0-9 (chat/dance/sitting frames)"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:37:15.075Z

**📎 ToolResult**

```
				break;
			}
			if ((double)rotation > 3.14)
			{
				rotation -= 6.28f;
			}
			if ((double)rotation > -0.01 && (double)rotation < 0.01)
			{
				rotation = 0f;
			}
			else
			{
				rotation *= 0.9f;
			}
			if (velocity.Y == 0f)
			{
				if (direction == 1)
				{
					spriteDirection = 1;
				}
				if (direction == -1)
				{
					spriteDirection = -1;
				}
				if (velocity.X == 0f)
				{
					frame.Y = 0;
					frameCounter = 0.0;
					break;
				}
				if (frame.Y < num * 2)
				{
					frame.Y = num * 2;
				}
				frameCounter += Math.Abs(velocity.X);
				frameCounter += 1.0;
				if (frameCounter > 9.0)
				{
					frame.Y += num;
					frameCounter = 0.0;
				}
				if (frame.Y / num > 7)
				{
					frame.Y = num * 2;
				}
			}
			else
			{
				frameCounter = 0.0;
				frame.Y = num;
			}
			break;
		case 17:
		case 18:
		case 19:
		case 20:
		case 21:
		case 22:
		case 26:
		case 27:
		case 28:
		case 31:
		case 37:
		case 38:
		case 44:
		case 54:
		case 73:
		case 77:
		case 78:
		case 79:
		case 80:
		case 104:
		case 107:
		case 108:
		case 120:
		case 124:
		case 140:
		case 142:
		case 159:
		case 160:
		case 162:
		case 167:
		case 178:
		case 181:
		case 185:
		case 196:
		case 197:
		case 198:
		case 201:
		case 202:
		case 203:
		case 207:
		case 208:
		case 209:
		case 212:
		case 213:
		case 227:
		case 228:
		case 229:
		case 287:
		case 294:
		case 295:
		case 296:
		case 310:
		case 311:
		case 312:
		case 313:
		case 314:
		case 322:
		case 323:
		case 324:
		case 326:
		case 338:
		case 339:
		case 340:
		case 353:
		case 368:
		case 369:
		case 441:
		case 453:
		case 460:
		case 462:
		case 463:
		case 489:
		case 534:
		case 550:
		case 588:
		case 630:
		case 632:
		case 633:
		case 635:
		case 637:
		case 638:
		case 656:
		case 663:
		case 670:
		case 678:
		case 679:
		case 680:
		case 681:
		case 682:
		case 683:
		case 684:
		{
			int num57 = (isLikeATownNPC ? NPCID.Sets.ExtraFramesCount[type] : 0);
			bool flag7 = NPCID.Sets.IsTownSlime[type];
			if (false && !Main.dedServ && TownNPCProfiles.Instance.GetProfile(type, out var profile))
			{
				Asset<Texture2D> textureNPCShouldUse = profile.GetTextureNPCShouldUse(this);
				if (textureNPCShouldUse.IsLoaded)
				{
					num = textureNPCShouldUse.Height() / Main.npcFrameCount[type];
					frame.Width = textureNPCShouldUse.Width();
					frame.Height = num;
				}
			}
			if (velocity.Y == 0f)
			{
				if (direction == 1)
				{
					spriteDirection = 1;
				}
				if (direction == -1)
				{
					spriteDirection = -1;
				}
				if (NPCID.Sets.IsTownSlime[type])
				{
					spriteDirection *= -1;
				}
				int num58 = Main.npcFrameCount[type] - NPCID.Sets.AttackFrameCount[type];
				if (ai[0] == 23f)
				{
					frameCounter += 1.0;
					int num59 = frame.Y / num;
					int num60 = num58 - num59;
					if ((uint)(num60 - 1) > 1u && (uint)(num60 - 4) > 1u && num59 != 0)
					{
						frame.Y = 0;
						frameCounter = 0.0;
					}

```


---

## 🤖 Assistant · 2026-08-17T04:37:41.283Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I understand the frame layout: `num58 = Main.npcFrameCount[type] - NPCID.Sets.AttackFrameCount[type]` = last non-attack frame index. So:
- Sitting frame = num58 - 3
- Dance frames: num58-5, num58-4 (bobbing)
- ai[0]==3 (chat with NPC): frames num58-1 (talking mouth open) / holding; with emote bubbles 36/37/38 (chat symbols: item/heart/...?) — I saw "EmoteBubble.NewBubble(num106, num107...)" with values 36,37,38 = emote IDs (question, exclamation? etc.) — actually 36/37/38 might be "talk" emotes.
- ai[0]==7/19: emote 112 at tick 16.
- ai[0]==23: frameCounter timeline with emote bubbles — let me read that (69330 above shows ai[0]==23 handling: num61 = frameCounter<6 ? num58-5 : num58-4, ai[1]<6 → num58-5). State 23 = "cheer"? This is likely the party "celebrate" state.

Let me now read the ai[0]==3/4 chat frame part (69560-69640 covered states with emote 36/37/38 at ~70100? no wait that was in the walking part... hmm, actually the 36/37/38 emote code I saw at 70100 area was within FindFrame? It appeared in my sed of 70100-70172 which showed EmoteBubble.NewBubble with num96 duration. That's part of ai[0]==16/17 chat (pair chat with emotes).

OK. I have enough on vanilla side for frames. Now — the key question for the audit: does OUR implementation handle:
1. Sitting frame (num58-3) when sitting? — check Renderer.
2. Party dance state 6? — check.
3. NPC↔NPC chat states 3/4/16/17 with facing + emotes? — check Game.ts / EmoteBubble.
4. Face player state 7 + emote 112.
5. Daytime random sit (1/300 while walking on chair tile).
6. Home leash ±25/±50, walk speed 1.0/0.07, walk/idle durations 200-500/300-1500.
7. Cliff avoidance GetWalkPrediction.
8. Obstacle 3-tier jumps + turn when blocked.
9. Drowning escape jump.
10. Stinky/fleeing from enemies (danger flee: direction away, state 8 freeze when blocked, PrettySafe). — attackUpdate handles fighting but NOT fleeing! Vanilla: town NPCs FLEE from enemies within DangerDetectRange (200) — they only fight if PrettySafe exceeded... wait no. Let me re-read: flag16 (danger detected within num11=200) → they turn and WALK AWAY from danger (direction = -num15) and only attack when flag31 (ai[0]<2 or 8, flag16, !stinky) with attack chance roll. Both: they flee AND occasionally attack. Actually looking at the danger block: if ai[0]==8 and danger still → reset; else if not attack state → set ai[0]=1 walking, direction = -num15 (AWAY from danger) — with GetWalkPrediction avoidFalling check; if avoidFalling (would fall off) then they DON'T flee (stay). Plus flag26/flag27 in the walking obstacle section: when flag16 (danger), if obstacle blocks and can't jump → flag27 → state 8 (frozen cowering 240 ticks).
    So vanilla town NPC behavior near enemies: try to run away; if can't (obstacle), freeze (state 8 = standing still = "cower"); while fleeing/frozen, they attack on chance roll. Our implementation: attackUpdate only — NO fleeing at all! Town NPCs in our version stand and fight instead of running away. **Major deviation** (well-known vanilla behavior: NPCs run from enemies).
    Wait — actually let me double check: is fleeing in our code? Search TownNPC.ts for "flee" / danger. I don't see it. Game.ts may have something? Let me check. The vanilla flee direction: `direction = -num15` — hmm wait, num15 is direction to nearest danger? Let me recheck: num15 = side selection (1 = danger on right?). If danger on right (num15=1), direction = -num15 = -1 → move left = away. Yes flee away. But note flag2 (infected dryad) → direction = num15 (toward).

11. Danger 8 cower frame? ai[0]==8 → falls in the "else if (ai[0] == 3f || 4f || 5f || 8f ...)" group — velocity decay only; frame = standing (frame 0). So no special cower frame — just standing. OK.

Also: 
12. `ai[3] == 1` — town NPC "death" flag removal (used for bound NPC transform / old man).
13. Type 368 (tax collector?) no — 368 is... whatever, special.
14. Guide 37 dungeon teleport: UpdateHomeTileState(dungeonX, dungeonY) when downedBoss3 (Skeletron) → Guide disappears. And type 37 on dungeon floor → teleport home.

15. Taxi... let me not go too deep on per-type specials.

Now let me check our Game.ts for: town NPC respawn (UpdateTime_SpawnTownNPCs equivalent), emote pair chat, party dance, dialogue. Let me grep.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:37:41.796Z · glm-x-preview-260804

```
现在让我来检查我们的 `Game.ts`，以了解城镇 NPC 的生成/重生、表情以及派对行为。
```


---

## 🤖 Assistant · 2026-08-17T04:37:42.773Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i \"townNpc\\|town_npc\\|spawnTownNpc\\|respawn\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | head -40",
 "description": "Find town NPC spawn/respawn in our Game.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:37:42.798Z

**📎 ToolResult**

```
80:import { dryadMoonPhaseStock, skeletonMerchantMoonPriceMul } from '../data/townNpcProfiles';
115:import { vanillaNpc, TOWN_NPC_IDS, getGemSquirrelToSpawn, getGemBunnyToSpawn, soundTrackFiles, TOWN_NPC_HEAD_INDEX } from '../data/vanillaNpcs';
141:import { TownNPC } from '../entities/TownNPC';
674:   *  （放置 spawn / 破坏 removeAt / 读档 respawnAll），实体本身不落盘 */
2484:    // 拴绳实体重生（TELeashedEntityAnchor.OnWorldLoaded → RespawnLeashedEntity，
2488:    this.leashed.respawnAll(
2729:    const savedNpcs = this.world.pendingTownNpcs ?? [];
2730:    this.world.pendingTownNpcs = [];
2734:        const t = new TownNPC(n.key, n.x, n.y);
2737:        if (n.shimmered) t.shimmered = true;   // 微光变体恢复（townNpcVariationIndex,WF:2927）
2743:        this.entities.add(new TownNPC('guide', this.world.spawnX * 16 + 8, (this.world.spawnY - 2) * 16), 'npcs');
2748:        this.maybeRespawnOldMan();
2753:      // 商人/护士等由 checkTownArrival 按原版条件 + 房屋系统入住(见 updateTownNpcArrival)
2754:      if (!this.entities.npcs.some((n) => n instanceof TownNPC && n.npcKey === 'guide' && !n.dead)) {
2755:        this.entities.add(new TownNPC('guide', this.world.spawnX * 16 + 8, (this.world.spawnY - 2) * 16), 'npcs');
2759:        this.maybeRespawnOldMan();
2811:    if (this.entities.npcs.some((n) => n instanceof TownNPC && !n.dead && n.npcKey === 'angler')) return false;
2839:    if (this.entities.npcs.some((n) => n instanceof TownNPC && !n.dead && n.npcKey === key)) return false;
2842:    const npc = new TownNPC(key, x * TILE + 8, (y + 1) * TILE);
2849:  private freeBoundNpc(npc: TownNPC): void {
2910:        const ms = new TownNPC('town_slime_yellow', c.x, c.y);
2917:      const npc = n as TownNPC;
2918:      if (!(npc instanceof TownNPC) || npc.dead || !npc.bound) continue;
2927:    // ★生成期 bound TownNPC 放置移除（2026-08-13）后，534 由 Spawner 地狱链以
2929:    // 是 Enemy 而非 bound TownNPC）；上方 npcs 桶扫描保留兜底旧存档的 bound 残留
2936:        const tc = new TownNPC('tax_collector', en.cx, en.y + en.h);
2952:  private maybeRespawnOldMan() {
2954:    if (this.entities.npcs.some((n) => n instanceof TownNPC && n.npcKey === 'old_man' && !n.dead)) return;
3010:    const oldMan = new TownNPC('old_man', spot.x * 16 - 8, spot.y * 16);
3174:      // ±1920×±1200px 内的 townNPC——曾误用 1080(高偏窄,2026-08-13 对齐)）——
3176:      const townNPCCount = this.entities.npcs.filter((n) => {
3177:        const tn = n as TownNPC;
3180:      this.scene = scanScene(w, this.player.cx, this.player.cy, townNPCCount, partyIsUp(this.partyState));
3507:        if (e.dead || e instanceof TownNPC || e.vanillaId == null) continue;
3728:      player.respawnTimer++;
3729:      // GetRespawnTime（Player.cs:38384-38422）：600t=10s 基准;专家 ×1.5=900;
3732:      if (player.respawnTimer > 600 * (mainExpertMode(this.world) ? 1.5 : 1)
3734:          : this.entities.enemies.some((en) => (en as unknown as { def?: { boss?: boolean } }).def?.boss && !en.dead) ? 600 : 0)) this.respawnPlayer();
4080:          this.maybeRespawnOldMan();
4096:    //      ≈ UpdateTime_SpawnTownNPCs(forceUpdate)）。

```


---

## 🤖 Assistant · 2026-08-17T04:37:43.512Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"partyUp\\|dance\\|danc\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts | head -20",
 "description": "Find party dance in our code"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:37:43.542Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1198:      party: !!this.scene?.partyUp,
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:5948:        if (this.scene?.partyUp && world) this.drawPartyHat(ctx, n, world);

```


---

## 🤖 Assistant · 2026-08-17T04:37:46.094Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '4090,4160p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Read our town NPC arrival/respawn logic"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:37:46.116Z

**📎 ToolResult**

```
      }
    }

    // ---- 树苗生长（每 5 秒扫一次） ----
    if (this.tickCount % 300 === 0) this.growSaplings();
    // ---- 城镇 NPC 入驻评估（原版 Main.cs:65021 每 7200 tick 一轮；载入后 10s 首轮
    //      ≈ UpdateTime_SpawnTownNPCs(forceUpdate)）。
    //      固定周期 = 原版语义，非偏差（:65032-65036 checkForSpawns++ 攒到
    //      7200/worldUpdateRate 才评估，无随机化）；差异仅在相位锚——原版
    //      StartNight/StartDay 双双清 checkForSpawns（:64711-64712/:64857-64858），
    //      计数锚在昼夜切换点，本仓锚全局 tick，不影响入驻节奏 ----
    if (this.tickCount % 7200 === 600) this.updateTownNpcArrival();
    // ---- 昼夜事件（UpdateTime_StartNight :64817 / StartDay :64876 语义） ----
    {
      const ct = w.clock.timeOfDay, pt = this._lastClockT;
      this._lastClockT = ct;
      const crossed = (a: number) => pt < a && ct >= a;
      if (crossed(Clock.DAWN)) {
        // 摇树表清空（UpdateTime_StartDay 首行 Main.cs:64846 WorldGen.ResetTreeShakes）——
        // 每树每日一摇的门
        this.treeShakes.reset();
        // 日晷快进落点（UpdateTime_StartDay :64844-64847 头部）：清 fastForwardTimeToDawn
        // → dayRate 自动回到常规档（World.dayRate() 每 tick 重算，无需显式 UpdateTimeRate）；
        // 日晷冷却 -1（:64885-64887，使用时置 8 → 8 个黎明后归零可再用）
        if (w.fastForwardTimeToDawn) w.fastForwardTimeToDawn = false;
        if (w.sundialCooldown > 0) w.sundialCooldown--;
        // 渔夫任务每日重掷（UpdateTime_StartDay :64852 → Main.AnglerQuestSwap）：清
        // 今日交付名单/完成旗 + 按世界门（困难/邪恶类型/Boss 进度）重选任务鱼
        this.anglerQuestSwap();
        // 成就：熬过一夜（Main.cs:64894 event 1）+ 血月夜结束（:64862-64866 event 5，
        // 血月旗在清除前求值——本块首两行即原序）
        this.achievements.notifyProgressionEvent(1);
        if (w.clock.bloodMoon) this.achievements.notifyProgressionEvent(5);
        // 黎明：月相推进 + 血月清除 + 季节重算（Main.cs:64877-64890）
        w.clock.moonPhase = (w.clock.moonPhase + 1) % 8;
        w.clock.bloodMoon = false;
        // drunkWorld 黎明翻转世界邪恶类型（Main.cs:64883-64886：!dayTime 期交替腐化/猩红）
        if (w.seedFlags?.drunkWorld) w.crimson = !w.crimson;
        // 自然召唤旗白天清除（UpdateTime :64625-64626）
        this.spawnEyePending = false;
        this.spawnHardBossPending = 0;
        // 普通事件 roll 压制（Main.cs:64652-64660 ShouldNormalEventsBeAbleToStart，在
        // StartDay 之前求值——此时 CheckMorning 未跑，LanternsUp 仍为真；除灯笼夜外
        // 天界入侵进行中/场上有月总/月总倒计时>0 同样置 stopEvents=true）
        const stopEvents = LanternNight.lanternsUp || w.lunarEvent.active
          || w.lunarEvent.moonLordCountdown > 0
          || this.entities.enemies.some((e) => !((e as Enemy).dead) && (e as Enemy).vanillaId === 398);
        // 灯笼夜黎明收场（Main.cs:64854 = LanternNight.CheckMorning）：双旗清零
        LanternNight.checkMorning();
        // ---- 月事件黎明结算（UpdateTime_StartDay :64867-64871，顺序固定：
        //      总分广播 → 强制季节 → stop；须在下方日食 roll 之前）----
        // CheckForMoonEventsStartingTemporarySeasons（Main.cs:10833-10862 1:1）：
        // 先记昨日值 → 清 ForToday → wave≥15 按事件重设 → Forever 位压制（:10845-10849，
        // 永久季种子位，随存档 flags 持久化）→ 与昨日值不同才广播 Started/Ended（:10855-10861）
        const prevForceHalloween = this.forceHalloweenForToday;
        const prevForceXMas = this.forceXMasForToday;
        this.forceHalloweenForToday = false;
        this.forceXMasForToday = false;
        if (moonEventActive(w)) {
          // CheckForMoonEventsScoreDisplay（Main.cs:10865-10877）：Misc.*MoonScore
          this.newText(
            Lang.text(w.moonEvent.kind === MOON_KIND_PUMPKIN
              ? 'Misc.PumpkinMoonScore' : 'Misc.FrostMoonScore',
            Math.floor(w.moonEvent.totalInvasionPoints)), 175, 75, 255);
          // wave≥15 → 当日强制季节（:10837-10843：南瓜月→万圣 / 霜月→圣诞）
          if (w.moonEvent.waveNumber >= 15) {
            if (w.moonEvent.kind === MOON_KIND_PUMPKIN) this.forceHalloweenForToday = true;
            else this.forceXMasForToday = true;
          }
          // stopMoonEvent（Main.cs:10879-10901）：三字段清零（不进存档）
          stopMoonEvent(w);

```


---

## 🤖 Assistant · 2026-08-17T04:37:48.738Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me look at updateTownNpcArrival (our respawn logic) and compare with vanilla Main.cs:65021 UpdateTime_SpawnTownNPCs. Let me read both.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:37:49.469Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"updateTownNpcArrival\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts; sed -n '2760,2850p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Read our updateTownNpcArrival"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:37:49.499Z

**📎 ToolResult**

```
2753:      // 商人/护士等由 checkTownArrival 按原版条件 + 房屋系统入住(见 updateTownNpcArrival)
4101:    if (this.tickCount % 7200 === 600) this.updateTownNpcArrival();
12761:  private updateTownNpcArrival() {
      }
      // ★bound 救援 NPC 生成期【不放置】（2026-08-13 对齐原版，实证链）：
      //   ① WorldGen SpawnStarterNPCs（cs:19830-20041）普通种子分支只 NewNPC(22)
      //     向导（最终 else :20037-20041），无任何 bound NPC；
      //   ② bound NPC（105/106/123/354/589/534/685）唯一来源 = NPC.Spawner 链
      //     （三人组 :1994-2008 / 造型师 :1576 / 高尔夫 :1600 / 机械师 :2563 /
      //     税务员 :4777），各带前置门+概率+!saved+!AnyNPCs；
      //   ③ Spawner.SpawnNPC(X,Y,Type)（:5146）= 普通 NewNPC，bound 形态即类型本体。
      //  此前 placeBoundRescueNpcs 在生成期直接放五只 bound（开局即可无门救出全部），
      //  已移除——由 VanillaSpawner 各链 1:1 供给（589/685 走 spawnBound 占位）。
      // 渔夫任务链首掷（WorldGen.cs:22655 → Main.AnglerQuestSwap）+ 沙滩睡渔夫放置
      this.anglerQuestSwap();
      this.placeSleepingAngler();
    }
    // 昼夜事件基线：季节旗标 + 时钟快照
    this.checkSeasonal();
    // MysticLogFairiesEvent.StartWorld（WorldGen.cs:3303 OnWorldLoad）：读图/新世界
    // 扫一次倒木桩（StartNight 会重扫，此为入夜前的首扫）
    mysticLogs.startWorld(this.fairyCtx());
    // setFireFlyChance 读档重掷（WorldFile.cs:770 加载回调末尾 = 液体沉降后；
    // 五静态位不落盘、初值全 0——原版每次读档都重掷，白昼存读当夜值随之刷新）
    setFireFlyChance(this.world);
    this._lastClockT = this.world.clock.timeOfDay;
    // 成就：解锁弹窗（原版 InGamePopups.AchievementUnlockedPopup,InGameNotificationsTracker
    // 底部居中锚 screenHeight-40、300t 寿命——非 Steam 专属;UI 无 popup 钩子时回退 toast）
    // + 进世界基线
    this.achievements.onUnlock = (name) => {
      const disp = Lang.text(`Achievements.${name}_Name`);
      if (this.cb.onAchievementPopup) this.cb.onAchievementPopup(name, disp);
      else this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.AchievementUnlocked', disp));
      // 背包内提示牌即时换下一目标（原版每帧重绘的等价触发）
      this.cb.onInventoryChanged?.();
    };
    // Journey 研究（Research 内核，子代理 E 移植）：成就桥 + 进世界 forced 检查
    // （Player.cs:318 OnEnterWorld forced:true）
    this.research.onProgressionEvent = (ev) => this.achievements.notifyProgressionEvent(ev);
    this.research.checkResearchAchievement(true);
    this.achOnWorldEnter();
    (window as unknown as { __swResearch?: unknown }).__swResearch = this.research;
    this.cb.onInventoryChanged();
  }

  /** 沙滩睡渔夫（NPC 376）放置。原版由 SpawnNPC 海洋段掷出（NPC.cs:1705-1728 海洋
   *  水域 / :1835-1837 沙滩干沙分支——两分支同门：!savedAngler && !AnyNPCs(376) &&
   *  横向边缘 380 格内 && 地表以上）。本仓在生成期与入驻轮确定性补放：就近取出生点
   *  一侧的合格干沙格（空气×2 + 沙格 + 地表以上），差异仅"何时放"不含条件语义。
   *  解救后写 flags.savedAngler（NPC.savedAngler，WF:1334/2160 随存档）。 */
  private placeSleepingAngler(): boolean {
    const w = this.world;
    const st = w.store;
    if (w.flags.savedAngler) return false;   // NPC.savedAngler
    if (this.entities.npcs.some((n) => n instanceof TownNPC && !n.dead && n.npcKey === 'angler')) return false;
    // Main.tileSand（NPC.cs:7177-7180）：黄沙/黑檀沙/珍珠沙/猩红沙
    const sands = new Set(['sand', 'v_112_ebonsand_block', 'v_116_pearlsand_block', 'v_234_crimsand_block']
      .map((k) => TILE_BY_KEY[k]).filter((v): v is number => v !== undefined));
    const surface = Math.floor(w.groundLevel);                              // y < worldSurface 门（:1835）
    const sides: Array<[number, number]> = [[8, 1], [st.w - 9, -1]];        // 双侧海洋，向外到内
    const spawnTx = Math.floor((this.player.cx || w.spawnX * TILE) / TILE);
    sides.sort((a, b) => Math.abs(a[0] - spawnTx) - Math.abs(b[0] - spawnTx));
    for (const [x0, dir] of sides) {
      for (let k = 0; k < 380; k++) {         // WorldGen.beachDistance（WorldGen.cs:4102）
        const x = x0 + dir * k;
        if (x < 8 || x > st.w - 9) break;
        for (let y = Math.max(4, surface - 40); y < surface; y++) {
          if (!sands.has(st.get(x, y)) || st.liquid[st.idx(x, y)] > 0) continue;   // !waterTile
          if (st.isSolid(x, y - 1) || st.isSolid(x, y - 2)) continue;              // 空气×2
          if (this.placeBoundNpc('angler', 'savedAngler', x, y - 1)) return true;
          break;
        }
      }
    }
    return false;
  }

  /** 深度带内找 bound 落脚点（空气×2 + 下方实心），返回 [x, 脚底上一格y] */
  /** 放置一名 bound 救援 NPC（已解救/已在场/落点无效时跳过）。x,y = 脚底上一格 */
  private placeBoundNpc(key: string, savedFlag: string, x: number, y: number): boolean {
    const st = this.world.store;
    if (this.world.flags[savedFlag]) return false;
    if (this.entities.npcs.some((n) => n instanceof TownNPC && !n.dead && n.npcKey === key)) return false;
    if (x < 3 || y < 3 || x > st.w - 4 || y > st.h - 4) return false;
    if (st.isSolid(x, y) || st.isSolid(x, y - 1)) return false;
    const npc = new TownNPC(key, x * TILE + 8, (y + 1) * TILE);
    npc.bound = true;
    this.entities.add(npc, 'npcs');
    return true;
  }

  /** 右键解救 bound NPC（原版 bound 类型右键 → 转正 + AI_007_UpdateSavedStates 置 saved 旗标） */
  private freeBoundNpc(npc: TownNPC): void {
    // 685 抖箱保真门（Main.cs:42454 + TryFreeingElderSlime :42536-42553）：须消耗金钥匙 327

```


---

## 🤖 Assistant · 2026-08-17T04:37:53.390Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '12761,12900p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Read updateTownNpcArrival implementation"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:37:53.413Z

**📎 ToolResult**

```
  private updateTownNpcArrival() {
    // 入侵/月事件进行中暂停城镇 NPC 入驻（SpawnHomelessNPC :4987 门；月事件原版经
    // !dayTime 间接压制——本入驻轮无昼夜门，显式补 moonEventActive）
    if (invasionActive(this.world) || moonEventActive(this.world)) return;
    const npcs = this.entities.npcs.filter((n) => n instanceof TownNPC && !n.dead) as TownNPC[];
    const has = (key: string) => npcs.some((n) => n.npcKey === key);
    // npcId 随 home 携带（ScoreRoom 占用豁免 CanNPCsLiveWithEachOther 用）
    const homes = npcs.filter((n) => n.home)
      .map((n) => ({ x: n.home!.x, y: n.home!.y, npcId: n.vanillaId }));
    const st = this.world.store;
    // 入驻锚点（SpawnHomelessNPC :5014-5036 1:1）：已安家 townNPC 的 home 随机取一——
    // 原版房表口径 townNPC && type!=37 && !homeless（:5019）：宠物算锚（宠物
    // townNPC=true，NPC.cs:17145）；old_man(type 37) 虽有地牢驻点 home 也不可作锚。
    // ★锚池为空 = 原版 :5035-5037 `if (num == 0) return`——整轮不找不发（出生点/
    // 玩家位兜底曾为两轮偏离,远程基地的正版通路=住房查询 UI 手动分配,已随
    // moveRoom 语义实装回收偏离,2026-08-15 用户定案"百分百对齐"）
    const anchorPool = homes.filter((h) => h.npcId !== 37);   // 37 = Old Man（:5019 排除）
    const pickAnchor = (): { x: number; y: number } =>
      anchorPool[Math.floor(Math.random() * anchorPool.length)];

    // ①' 被绑巫师【不补放】（2026-08-13 对齐原版）：106 BoundWizard 唯一来源 =
    // SpawnAnNPC 三人组链（NPC.cs:1999-2002，hardMode && 1/20 && 洞穴层深处门），
    // VanillaSpawner 已 1:1——困难模式开启后由链自然掷出，入驻轮直接补放非原版
    // （生成期 placeBoundRescueNpcs 同批移除，实证见 onWorldReady 注释）
    // ①'' 睡渔夫补放（原版 SpawnNPC 海洋/沙滩分支每轮掷——补放近似其"未解救则持续在场"）
    this.placeSleepingAngler();

    // ① QuickFindHome（Main.cs:65072：每轮对未安家 NPC 找房入住）
    // ★锚池空 → 原版 :5035-5037 直接 return（找/发都停）——无任何兜底
    // bound（被绑待救）不入住不搬动——原版 AI_007 bound 态原地，否则五个救援 NPC
    // 会被塞进同一间空房叠在一点（读档/新世界 7200 tick 后必现）
    if (anchorPool.length > 0) {
      for (const n of npcs) {
        if (n.home || n.bound || n.npcKey === 'old_man') continue;
        const anchor = pickAnchor();
        const house = findFreeHouse(st, homes, anchor.x, anchor.y, n.vanillaId);
        if (!house) continue; // 该锚点 ±10 窗内无房：NPC 留 homeless，下一 NPC 换锚点重试（锚点各异不整体放弃）
        n.home = { x: house.standX, y: house.standY };
        n.leashHome = true; // 有家者白天在家附近游走
        homes.push({ x: house.standX, y: house.standY, npcId: n.vanillaId });
        n.x = house.standX * TILE + 8 - n.w / 2;
        n.y = (house.standY + 1) * TILE - n.h;
      }
    }

    // ② 优先级链（Main.cs num42 完整顺序；护士/爆破手要求商人在场，
    //    染料商 ≥4 人、油漆工 ≥8 人、派对女孩 ≥20 人且 1/40 重掷）
    // ★锚池空 → 原版 SpawnHomelessNPC 在 num10>=1 门内(Main.cs:64530-64537),
    //   整轮（含新 NPC 生成）不跑——冷启世界的第一个入住只能走住房 UI 手动分配
    if (anchorPool.length === 0) return;
    const merchantHere = has('merchant');
    const allow = (key: string) => this.townNpcSpawnAllowed(key);
    const n = npcs.length; // num40：在场城镇 NPC 总数（含守卫老人，原版同）
    // 严格按 Main.cs:65458-65570 num42 优先链原序（2026-08-13 对齐：补 angler
    // 369/酒保 550、造型师归位到裁缝后、史莱姆第二轮按 :65557-65574 原序重排）
    const prio: Array<[string, boolean]> = [
      ['guide', !has('guide')],
      ['merchant', !merchantHere && allow('merchant')],
      ['nurse', !has('nurse') && merchantHere && allow('nurse')],
      ['arms_dealer', !has('arms_dealer') && allow('arms_dealer')],
      ['goblin_tinkerer', !has('goblin_tinkerer') && allow('goblin_tinkerer')],
      ['wizard', !has('wizard') && allow('wizard')],
      ['dryad', !has('dryad') && allow('dryad')],
      ['demolitionist', !has('demolitionist') && merchantHere && allow('demolitionist')],
      ['witch_doctor', !has('witch_doctor') && allow('witch_doctor')],
      ['steampunker', !has('steampunker') && allow('steampunker')],
      ['mechanic', !has('mechanic') && allow('mechanic')],
      ['angler', !has('angler') && allow('angler')],            // :65489（369）
      ['cyborg', !has('cyborg') && allow('cyborg')],
      ['pirate', !has('pirate') && allow('pirate')],
      ['clothier', !has('clothier') && allow('clothier')],
      ['stylist', !has('stylist') && allow('stylist')],         // :65506（354，裁缝后）
      ['dyer', !has('dyer') && n >= 4 && allow('dyer')],
      ['painter', !has('painter') && n >= 8],
      ['party_girl', !has('party_girl') && n >= 20 && allow('party_girl')],
      ['santa_claus', !has('santa_claus') && allow('santa_claus')],
      ['tavernkeep', !has('tavernkeep') && allow('tavernkeep')],  // :65516（550）
      ['golfer', !has('golfer') && allow('golfer')],
      ['tax_collector', !has('tax_collector') && allow('tax_collector')],
      ['truffle', !has('truffle') && allow('truffle')],
      ['zoologist', !has('zoologist') && allow('zoologist')],
      ['princess', !has('princess') && allow('princess')],
      // ---- 城镇史莱姆族第二轮（Main.cs:65391-65422 + :65557-65574 原序：
      //  铜侍从 684 → 蓝 670 → 酷 678 → 老 679 → 紫 680 → 红 682 → 黄 683 → 彩虹 681；
      //  兔 656/猫 637/狗 638 的 bought* 旗依赖许可证商店未实装，登记缺失）----
      ['town_slime_squire', !has('town_slime_squire') && !!this.world.flags.unlockedSlimeCopperSpawn],
      ['town_slime_blue', !has('town_slime_blue') && !!this.world.flags.unlockedSlimeBlueSpawn],
      ['town_slime_cool', !has('town_slime_cool')
        && (!!this.partyState.genuineParty || !!this.world.flags.unlockedSlimeGreenSpawn)],  // :65274 真派对门
      ['town_slime_old', !has('town_slime_old') && !!this.world.flags.unlockedSlimeOldSpawn],
      ['town_slime_clumsy', !has('town_slime_clumsy') && !!this.world.flags.unlockedSlimePurpleSpawn],
      ['town_slime_red', !has('town_slime_red') && !!this.world.flags.unlockedSlimeRedSpawn],
      ['town_slime_yellow', !has('town_slime_yellow') && !!this.world.flags.unlockedSlimeYellowSpawn],
      ['town_slime_diva', !has('town_slime_diva') && !!this.world.flags.unlockedSlimeRainbowSpawn],
      // ---- 宠物三只（:65567-65574 序：兔 656 → 猫 637 → 狗 638；bought* 旗由
      //  许可证使用置位——Chest.cs:3265-3280 动物学家进货：4829 无门/4830 图鉴
      //  ≥25%/4910 ≥45%；NPCID.Sets.IsTownPet 含宠物+全部城镇史莱姆=免房入住）----
      ['town_bunny', !has('town_bunny') && !!this.world.flags.boughtBunny],
      ['town_cat', !has('town_cat') && !!this.world.flags.boughtCat],
      ['town_dog', !has('town_dog') && !!this.world.flags.boughtDog],
    ];
    const pick = prio.find(([, ok]) => ok)?.[0];
    if (!pick) return;
    if (pick === 'town_slime_cool') this.world.flags.unlockedSlimeGreenSpawn = true;  // WorldGen.cs:5543

    // ③ 入住 / 流浪生成（askingNpcId = 待生成者，占用豁免/同房避让用）。
    // 锚点同 ①（pickAnchor：已安家 home 随机取一/冷启出生点）——原版此处为
    // SpawnTownNPC(LastFoundHouse) 失败后走 :5014-5033 randomNext homes，
    // 新 NPC 落锚点后经 QuickFindHome(:5135) 在锚点 ±10 窗内找房
    const id = TOWN_NPC_IDS[pick].id;
    const anchor = pickAnchor();
    const house = findFreeHouse(st, homes, anchor.x, anchor.y, id);
    const name = Lang.npcName(id) ?? pick;
    // NPCID.Sets.IsTownPet（NPCID.cs:4444）= 宠物三只+全部城镇史莱姆：WorldGen.
    // IsThereASpawnablePrioritizedTownNPC(:4855) 对本集免房放行——无房时在出生点
    // 附近流浪生成（不设 home），不占用 SpawnHomelessNPC 的白天/有家锚点门
    const TOWN_PET_KEYS = new Set(['town_bunny', 'town_cat', 'town_dog',
      'town_slime_blue', 'town_slime_cool', 'town_slime_old', 'town_slime_clumsy',
      'town_slime_diva', 'town_slime_red', 'town_slime_yellow', 'town_slime_squire']);
    if (!house && TOWN_PET_KEYS.has(pick)) {
      const ax = this.world.spawnX + (Math.random() < 0.5 ? -1 : 1) * (20 + Math.floor(Math.random() * 40));
      if (ax > 3 && ax < st.w - 4) {
        let ay = Math.max(4, this.world.spawnY - 20);
        const limit = Math.min(st.h - 3, this.world.spawnY + 20);
        while (ay < limit && !st.isSolid(ax, ay)) ay++;
        if (ay < limit) {
          const npc = new TownNPC(pick, ax * TILE + 8, (ay + 1) * TILE);
          this.entities.add(npc, 'npcs');
          this.newText(Lang.text('Announcement.HasArrived', name), 50, 125, 255);
        }
      }
      return;
    }
    // 松露人特判（WorldGen.CheckSpecialTownNPCSpawningConditions :4919-4946）：
    // unlockedTruffleSpawn 未置时房间须整体在地表（roomY2 ≤ worldSurface），
    // 且房内蘑菇族 tile（70 草/71 植/72 树/528 藤）≥ SceneMetrics.
    // MushroomTileThreshold(=100)——此前按全域找房（备案），现 1:1；不满足则本轮跳过
    if (house && pick === 'truffle') {
      const MUSH = [TILE_BY_KEY['v_70_mushroom_grass_block'], TILE_BY_KEY['v_71_mushroom_plant'],
        TILE_BY_KEY['v_72_mushroom_tree'], TILE_BY_KEY['v_528_mushroom_vines']].filter(

```


---

## 🤖 Assistant · 2026-08-17T04:38:01.117Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Our arrival system is quite comprehensive. Now let me verify vanilla Main.cs UpdateTime_SpawnTownNPCs for comparison (line 65021) and the checkTownNPCs conditions (spawn gate: checkForSpawns every 7200, night-only gate etc.). Let me also confirm the death-related drops (NPCLoot for townNPC) and "strike" behaviors.

But first — priority: check our remaining missing pieces:
1. Flee from danger (direction = -num15) — check for it in TownNPC/Game.
2. NPC↔NPC chat states 3/4/16/17 — check EmoteBubble/Game.tickNpcEmotes.
3. State 7 face player + emote 112; state 6 party dance.
4. Daytime random sit.
5. Sitting frame in Renderer.
6. Cliff avoidance.
7. Death respawn timing (vanilla: town NPC death → not directly respawn; but checkTownNPCs re-spawns via UpdateTime_SpawnTownNPCs every 7200 ticks with conditions).
8. Death drops for town NPC (NPCLoot).
9. Push by player? Let me check vanilla — is there any player→NPC push? I don't think so. NPCs push PLAYERS? no. Actually there's "Town NPC collision with player"? no.
10. Honey slow / hit flash.

Let me check our Game.tickNpcEmotes and EmoteBubble module.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:38:02.000Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"tickNpcEmotes\\|spawnEmote\\|EmoteBubble\" ~/Project/GLM/SandboxWorld/game/src/ --include=\"*.ts\" -l; echo ---; grep -n \"tickNpcEmotes\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Find emote bubble implementation"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:38:02.037Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/core/Game.ts
~/Project/GLM/SandboxWorld/game/src/render/EmoteBubble.ts
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts
~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts
---
4614:    this.tickNpcEmotes();
13978:  private tickNpcEmotes(): void {

```


---

## 🤖 Assistant · 2026-08-17T04:38:03.690Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '13978,14100p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Read our tickNpcEmotes"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:38:03.709Z

**📎 ToolResult**

```
  private tickNpcEmotes(): void {
    if (this.world.clock.isDay && --this.emoteCooldown <= 0) {
      this.emoteCooldown = 600; // 每 10s 窗口一次
      const npcs = this.entities.npcs.filter(
        (n) => n instanceof TownNPC && !n.dead && !n.bound && !n.talking) as TownNPC[];
      if (npcs.length >= 2) {
        for (let i = 0; i < npcs.length - 1; i++) {
          const a = npcs[i];
          for (let j = i + 1; j < npcs.length; j++) {
            const b = npcs[j];
            if (Math.hypot(a.cx - b.cx, a.cy - b.cy) > 6 * TILE) continue;
            // 表情池（EmoteID 实号：25 群系/90 道具/100 火/87 疑惑/89 睡意——原版社交段同源）
            const pool = [25, 90, 100, 87, 89];
            spawnEmote(a, pool[Math.floor(Math.random() * pool.length)], 180);
            spawnEmote(b, pool[Math.floor(Math.random() * pool.length)], 180);
            a.facing = b.cx < a.cx ? -1 : 1;  // 面向对方（原版社交状态朝向）
            b.facing = a.cx < b.cx ? -1 : 1;
            // 原版进入 ai[0]=7 社交态即停走；近似：重置游走计时让双方站定片刻
            a.wanderT = Math.max(a.wanderT, 220); b.wanderT = Math.max(b.wanderT, 220);
            a.vx *= 0.3; b.vx *= 0.3;
            return;
          }
        }
      }
      // 空闲随机冒泡(原版散落情境 NewBubble 的可见子集;emote 均匀 0..120,
      // 240t)——单 NPC 也冒泡,喂同一 EmoteBubble 模块(TownNPC 内联版已退役)
      if (npcs.length >= 1 && Math.random() < 0.5) {
        const n = npcs[Math.floor(Math.random() * npcs.length)];
        spawnEmote(n, Math.floor(Math.random() * 121), 240);
      }
    }
  }

  closeNpcDialog(): void {
    if (this.dialogNpc) this.dialogNpc.talking = false;
    this.dialogNpc = null;
    this.dialogHappiness = null;   // currentShoppingSettings = NotInShop（Player.cs:4189）
    this.npcShopClose();           // 店面板随对话关闭（Main.npcShop=-1 + 回购记清）
    this.sfx.play('menuClose');
    this.cb.onNpcDialogClose?.();
  }

  // ---- 商店(Chest.SetupShop case 1 = Merchant,Chest.cs:1325+) ----

  /** 各 NPC 商店商品表（Chest.SetupShop 1:1 提取，tools/extract-shops.mjs 生成；
   *  NPCInteractions.cs:489-513 的 type→shop 槽位映射） */
  private static readonly SHOPSTOCK: Record<string, Array<{ id: number; price: number | null; cond: string | null }>> =
    (shopstockJson as { shops: Record<string, Array<{ id: number; price: number | null; cond: string | null }>> }).shops;

  /** 当前对话 NPC 的商店商品表（Chest.SetupShop 数据驱动提取，tools/extract-shops.mjs） */
  private shopStockFor(npc: TownNPC): Array<[number, number]> {
    if (npc.npcKey === 'travelling_merchant') return this.travelStock.slice();  // 动态股票
    const stock = Game.SHOPSTOCK[String(npc.vanillaId)];
    if (!stock) return [];
    const out: Array<[number, number]> = stock.filter((s) => this.shopCondOk(s.cond)).map((s) => [s.id, s.price ?? 100] as [number, number]);
    // 派对女孩灯笼夜专柜（Chest.cs:2282：LanternNight.LanternsUp → 上架 4702 放飞灯笼；
    // extract-shops.mjs 未捕获该 if 门——与 moonPhase 同类缺口，此处直接补）。
    // 原版 SetDefaults(4702) 无价格覆盖 → 按 item value 100 铜出售
    if (npc.vanillaId === 208 && LanternNight.lanternsUp) out.push([4702, 100] as [number, number]);
    // 油漆师基础 12 色（Chest.cs:2424-2428 `for (int j = 1073; j <= 1084; j++)` 循环上架——
    // extract-shops.mjs 不展开 for 循环，vanilla-shopstock.json 缺 1073-1084，
    // 与 4702/moonPhase 同类提取缺口，此处按原版循环直补；价格 25 = Item.value（Item.cs:13374））
    if (npc.vanillaId === 227) {
      for (let j = 1073; j <= 1084; j++) out.push([j, 25] as [number, number]);
    }
    // ---- 月相分档专柜（extract-shops.mjs 只记 cond:'moonPhase' 未捕获 case 值——
    //      剔除恒真条目，按 Chest.cs switch 实表补 8 相位档）----
    const phase = this.world.clock.moonPhase;
    const price = (id: number) => ITEM_VALUES[String(id)] ?? 100;
    const day = this.world.clock.isDay;
    const add = (ids: number[]) => { for (const id of ids) out.push([id, price(id)] as [number, number]); };
    if (npc.npcKey !== 'travelling_merchant') {
      // 上述条目按相位重排（JSON 无 moonPhase 条目的 NPC 也进——分档表是权威）
      switch (npc.vanillaId) {
        case 453: { // 骷髅商（Chest.cs:2780-2940）
          add([[284], [946], [3069], [4341], [285], [953], [3068], [3084]][phase]);
          add(phase % 2 === 0 ? [3001] : this.world.flags.hardMode ? [188] : [28]);
          add(!day || phase === 0 ? [3002] : [282]);
          add(phase === 0 || phase === 1 || phase === 4 || phase === 5 ? [3003] : [40]);
          add([[3310], [3313], [3312], [3311]][phase % 4]);
          add(phase === 1 || phase === 2 ? [5640] : phase === 3 || phase === 5 ? [5641] : [5642]);
          if (phase === 0 && !day) add([3043]); // 满月夜魔法灯笼（:2930-2934）
          break;
        }
        case 20: { // 树妖月相轮换货（Chest.cs:1650-1697；NPCInteractions.cs:491
          // `Shop(20, 3)` 槽位 3=树妖(20)——提取器把相位 switch 摊平成 hardMode/
          // !hardMode 条目，先清 out 里的 4430-4441 再按相位补；
          // 逐相实表提纯到 townNpcProfiles.dryadMoonPhaseStock）
          for (let i = out.length - 1; i >= 0; i--) {
            if (out[i][0] >= 4430 && out[i][0] <= 4441) out.splice(i, 1);
          }
          add(dryadMoonPhaseStock(phase, !!this.world.flags.hardMode));
          break;
        }
        case 54: // 裁缝套装（:1795-1923）
          if (phase === 0) { add([245, 246]); if (!day) add([1288, 1289]); }
          else if (phase === 1) add([325, 326]);
          else if (this.world.flags.hardMode) {
            if (phase === 2) add([869]);
            else if (phase === 3) add([4994, 4997]);
            else if (phase === 4) add([864, 865]);
            else if (phase === 5) add([4995, 4998]);
            else if (phase === 6) add([873, 874, 875]);
            else add([4996, 4999]);
          }
          break;
        case 124: // 机械师（:2058-2062：渔夫在场且奇相位 → 机械师钓竿）
          if (phase % 2 === 1 && this.entities.npcs.some((n) => n instanceof TownNPC && !n.dead && n.vanillaId === 369)) {
            add([2295]);
          }
          break;
        case 207: if (phase === 0) add([2871, 2872]); break; // 染料商满月暗影/负片染料（:2233-2237）
        case 353: if ((phase % 2 === 0) === day) add([1981]); break; // 造型师时光染料（:2720-2724）
        case 588: // 高尔夫球手（Chest.cs:3135-3245 case 22 分数门槛 + 月相画）——
          // 门槛表提纯到 world/golf/golferShop.ts（含 >500/>1000/>2000/>=1000/>=2000 五档）
          add(golferShopScoreGates(this.player.golferScoreAccumulated, phase,
            !!(this.world.flags['downed_35'] || this.world.flags.downedSkeletron)));
          break;
        case 663: // 公主（Chest.cs:3427-3445：十周年+hardMode+击败海盗 → 相位对海盗四件）
          if (this.world.seedFlags?.tenthAnniversary && this.world.flags.hardMode && this.world.flags['downedPirates']
            && ![2584, 854, 855, 905].some((id) => out.some((e) => e[0] === id))) {
            add([[2584], [854], [855], [905]][Math.floor(phase / 2)]);
          }

```


---

## 🤖 Assistant · 2026-08-17T04:38:22.192Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Our emote system: tickNpcEmotes — every 600 ticks during day, picks one pair within 6 tiles, spawns emotes from pool [25,90,100,87,89], sets facing, "approximates" standing with wanderT=220. This is a significant simplification vs vanilla's rich pair-chat system:
- Vanilla: state 3/4 pair chat (1/300 per NPC per tick, 20<dist<100, LOS), duration 420×(1..3) or 420×(1..4); frame animation (talking frames num58-1/num58-2 alternating) + emotes 36/37/38 every ~60-90 ticks (frameCounter 100? let me check the exact emote cadence — the code at 69560-69640 showed "frameCounter >= 100 && rand(20)==0" and "frame.Y/num == 0 && frameCounter >= 20 → frame num58-1 + emote 89" — that's state 0 idle yawning? no wait. Hmm, that segment: `else if (frame.Y / num == 0 && frameCounter >= 20.0) { frame.Y = num * (num58 - 1); emote 89 }` — hmm 89 = sleepy emote? That's likely the ai[0]==2 state (random emote 45 ticks... no).
  
  Actually let me properly parse the FindFrame town states: I should read the full town branch 69296-69700 carefully. Let me do that to catalog frames per state. But given time constraints, I'll focus on: state 3/4 chat (which part handles?), 16/17 (chat with emote bubbles 36/37/38 — the code I saw at 70100 region was inside FindFrame? no — 70100 is past 69700. Hmm, the EmoteBubble.NewBubble(num106/num107) code at ~70050-70135 IS in FindFrame (FindFrame is 67295-~70300). OK.

So vanilla state 16/17 chat: while chatting, every ~90 ticks (num96?) both NPCs emit paired emotes from {36,37,38} with mirrored variants. States 3/4: talk frame animation.

Our version: single random pair every 600 ticks, emote pool {25,90,100,87,89}, duration 180 ticks, both stand (wanderT=220). No talking frames, wrong emote set (should be 36/37/38 = chat emotes... wait actually emote IDs: 36 = "Item"? Hmm. Emote ID 36/37/38: 33=Alarm, 34=Angry... let me not guess; vanilla chat uses 36,37,38 (whatever they are — question/heart/item?) with the special mirror logic. And state 7 uses emote 112 (= "chat"?). Actually 112 might be the "talk" bubble with dots.

Our pool [25, 90, 100, 87, 89]: 25=biome? 90=item, 100=fire... whatever — different semantics.

Also ours only runs `if (this.world.clock.isDay)` — vanilla NPC chats happen at night too (though at night they're usually home/sitting; pair chat can still trigger — flag30 requires ai[0]<2 which includes walking home state 1... yes vanilla chats any time).

OK. Now let me check the Renderer for sitting frame and talking/dance frames. And check how our Renderer draws TownNPC sitting (frame selection).
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:38:22.688Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"sitting\\|attackState\\|drawTownNPC\" ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts | head -30",
 "description": "Find sitting draw handling in Renderer"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:38:22.714Z

**📎 ToolResult**

```
148:import { TownNPC, sittingHatY, shimmerBodyAlpha, shimmerGlowAlpha } from '../entities/TownNPC';
1413:      else if (e instanceof TownNPC) { this.drawTownNPC(e, world); this.drawHealthBar(e); }
3836:   *  返回 null = 该 id 无变体链。已接通：drawTownNPC 本体后按本档 'lighter' 叠画
5813:   *  酒保 550 坐姿 ai[0]==5 → +7×dir。仓内映射：229 = TownNPC.attackState 12
5815:   *  550 = TownNPC.sitting（调用方传 ai0=5，drawPartyHat 还原） */
5852:    // 坐姿 ai[0]==5 +7×dir——ai0 还原：坐姿 = 5（TownNPC.sitting），否则 attackState
5853:    const ai0 = n.sitting ? 5 : n.attackState;
5862:      + (n.sitting ? sittingHatY(n.vanillaId) : 0);   // num6 链（:26965-26987：默认 −4，
5878:  private drawTownNPC(n: TownNPC, world?: World) {
5954:        if (!n.bound && n.attackState === 12) this.drawTownHoldout(ctx, n);
6618:    //      Position 消费 :4083-4087）：sittingIndex 单人恒 0 → posOffset=offsetForSeat×
6621:    if (p.sitting) {
6985:    if (p.sitting) ctx.restore();   // 坐椅偏移收口

```


---

## 🤖 Assistant · 2026-08-17T04:38:29.599Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '5878,5975p' ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "description": "Read our drawTownNPC for frame selection"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:38:29.621Z

**📎 ToolResult**

```
  private drawTownNPC(n: TownNPC, world?: World) {
    const ctx = this.ctx;
    // 血条统一走实体循环的 drawHealthBar(原版 HealthBar1/2 贴图版,Main.cs:21721+;
    // 此前这里另画早期程序化矩形条 = 双血条,已移除)
    // 表情气泡统一走实体层的 EmoteBubble 模块(drawEmotes :1112,并行会话 1:1 版:
    // GetPosition 头顶锚/开合帧/8tick 图标帧)——本函数的内联气泡版已退役(双画,
    // 与双血条同病;review 2026-08-13)
    // ---- 原版贴图条（Images/NPC_{id}，40×56 帧、默认朝左）：帧语义见 TownNPC.fixedUpdate ----
    // 注意：不再回退 Maples 角色/NPC_1.png——那是原版绿史莱姆贴图（Maples 沿用原版命名），
    // 曾导致全部城镇 NPC 显示为史莱姆
    if (this.atlas) {
      // bound 态：走专属捆绑姿态表（原版是独立 NPC 类型，见 BOUND_NPC_SHEET 注释）
      // ---- TownNPCs 档案切表（DrawNPCCheckAlt Main.cs:22304-22309 → profile.
      //      GetTextureNPCShouldUse）：n.townSheet 按微光档（townNpcVariationIndex，
      //      = shimmered）+ altTexture（1 派对 / 2 狼人）选 {Name}_Default{,_Party,
      //      _Transformed} / Shimmered_{Name}_…；无档案类型（637/638/656 宠物）返回
      //      null → 落回 NPC_{id} 竖条 ----
      const sheetPath = n.bound ? null : n.townSheet;
      const profileImg = sheetPath ? this.atlas.ensureVImage(sheetPath) : null;
      let r: DrawRect | null;
      if (profileImg) {
        // 帧数 = vanilla-npcs.json frames（见 townSheetFrameCount 口径注）;
        // idx 钳位保证任何数据出入都界内
        const count = townSheetFrameCount(n.vanillaId);
        const fh = Math.floor(profileImg.height / count);
        const idx = Math.max(0, Math.min(count - 1, n.frame));
        r = { img: profileImg, sx: 0, sy: idx * fh, sw: profileImg.width, sh: fh };
      } else {
        r = n.bound ? this.boundNpcSheet(n) : this.atlas.vnpc(n.vanillaId, n.frame);
      }
      if (r) {
        ctx.save();
        // 底锚 + 逐帧实测底部透明行数补偿(spriteBottomPad):帧底 ~2px 透明边距
        // 裸底锚悬空 2px、中心锚入地 2px(实测反馈)——pad 补偿保证贴地,
        // 与怪物(:854)/纸娃娃(:1266)/legacy(:1301)统一
        const pad = this.spriteBottomPad(r, `npc${n.bound ? 'bound' : n.vanillaId}:f${n.frame}`);
        ctx.translate(n.cx, n.y + n.h); // 脚底中心
        if (n.facing > 0) ctx.scale(-1, 1); // 原版贴图默认朝左，向右镜像
        // 微光转化渐显/渐隐（GetAlpha NPC.cs:94874-94878：CurrentlyShimmerTransparent
        // → 全通道 ×(1−shimmerTransparency)）——st 由 TownNPC 微光链驱动（浸微光
        // +0.01/t、转化置 0.89、上升态 −1/60/t）。派对帽同 save 块内继承该 alpha，
        // 恰好等价原版帽档 num8 = 1−st（Main.cs:27073-27075）
        ctx.globalAlpha = shimmerBodyAlpha(n.shimmerTransparency);
        if (n.iframes > 0 && n.iframes % 4 < 2) ctx.filter = 'brightness(2.5)'; // 受击闪白
        ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, -r.sw / 2, -r.sh + pad, r.sw, r.sh);
        // ---- 160/209 Glow 变体档（Main.cs:25769-25799，S 备案 npcGlowVariantTex 接通）----
        //      城镇 NPC 不经 drawNpcGlow → 本体后挂同档 Glow：Color(128−α/2,×3,0)
        //      A=0 → 'lighter' 加性（'128a2' 同款表达式）；160 松露人微光态 Glow_352、
        //      209 电子人微光态按 altTexture 选 Glow_350(≠1)/Glow_351(==1)。α=城镇 NPC
        //      静态 0 → 128/255；160 档的 shimmerTransparency RGB 衰减（:25771-25776）
        //      经 shimmerGlowAlpha 落在 alpha 上（加性混合下 ×(1−st) 等价），209 无此档。
        //      表布局与 NPC 表同构 → 帧 = 当前 townSheet 行（微光档案表帧高可异于本体，
        //      故按 Glow 表自身高/帧数切片，行号取 n.frame）
        const glowTex = n.bound ? null : Renderer.npcGlowVariantTex(n.vanillaId, n.shimmered, n.altTexture);
        if (glowTex) {
          const gi = this.atlas.ensureVImage(glowTex);
          if (gi && (gi.width > 0) && gi.width) {
            const gCount = townSheetFrameCount(n.vanillaId);
            const gfh = Math.max(1, Math.floor(gi.height / gCount));
            const gIdx = Math.min(gCount - 1, Math.max(0, n.frame));
            const op = ctx.globalCompositeOperation;
            const ga = ctx.globalAlpha;
            ctx.globalCompositeOperation = 'lighter';
            ctx.globalAlpha = shimmerGlowAlpha(128 / 255, n.vanillaId === 160 ? n.shimmerTransparency : 0);
            // (128 − α/2)/255 × (1−st)（α=0；st 衰减仅 160，:25771-25776）
            ctx.drawImage(gi, 0, gIdx * gfh, gi.width, gfh, -r.sw / 2, -r.sh + pad, r.sw, r.sh);
            ctx.globalCompositeOperation = op;
            ctx.globalAlpha = ga;
          }
        }
        if (this.scene?.partyUp && world) this.drawPartyHat(ctx, n, world);
        ctx.filter = 'none';
        ctx.restore();
        // ---- AttackType1 持械（DrawNPCExtras Main.cs:27121-27195）：弓/枪族攻击态
        //      ai[0]==12 全程手持武器图标——旋转 = ai[2]×90°×朝向；228/229/209 原版
        //      提前 return 无持械（:27124-27126,表里不列即同效）
        if (!n.bound && n.attackState === 12) this.drawTownHoldout(ctx, n);
        return;
      }
      // 贴图条懒加载首帧未就绪：落入下方程序化兜底，本帧后懒加载完成
    }
    const spr = this.assets.enemySprites.get(n.npcKey);
    if (!spr) return;
    ctx.save();
    ctx.translate(n.cx, n.cy);
    ctx.scale(n.facing >= 0 ? 1 : -1, 1);
    ctx.drawImage(spr.canvas, -spr.fw / 2, -spr.fh / 2, spr.fw, spr.fh);
    ctx.restore();
  }

  /** AttackType1（弓/枪族）攻击态持械（DrawNPCExtras Main.cs:27121-27195 1:1）。
   *  触发 = AttackType==1 && ai[0]==12（攻击态全程）；228/229/209 原版提前 return
   *  （:27124-27126）——TOWN_HOLDOUT 不列即同效。
   *  锚 = Bottom − OffsetsNPCOffhand[2](14,26)，spriteDirection==1 时偏移 X 取负(:27102)；
   *  旋转 = ai[2]×90°×spriteDirection(:27109)；握位 num12=floor(W/2)−grip（DrawPlayerItemPos
   *  .X 恒 =W/2，:27164-27168）——右向 dx=num12、左向经 scale(-1,1) 镜像（=原版
   *  origin=(W+num12,H/2)+Flip 的等价几何；旋转先绕锚后镜像的次序差 ≤2px 不再追）。
   *  微光 alpha 与本体同档（GetShimmerColor 经 npcColor 通道）。 */

```


---

## 🤖 Assistant · 2026-08-17T04:38:38.485Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Found: sitting NPC uses `n.frame` — but our `updateWalkFrame()` in TownNPC never sets the sitting frame! When sitting, `this.vx *= 0.8` decays → |vx|<0.05 → frame = 0 (standing). Vanilla: sitting = frame num58-3 = (npcFrameCount - AttackFrameCount) - 3. So our sitting NPCs stand at the chair position instead of showing the sitting pose. **Deviation (visual, moderate-high).**

Wait — let me double check our updateWalkFrame: yes, `Math.abs(this.vx) < 0.05 → frame = 0`. While sitting, vx=0 → frame 0. So no sitting frame. Vanilla sitting frame = num58-3. For a standard town NPC sheet with npcFrameCount=23? e.g. Guide has 25 frames, AttackFrameCount=? The typical sheet: walk frames 2.., attack frames at end. num58 = npcFrameCount - AttackFrameCount. E.g., Merchant: frames 23, ExtraFramesCount... The sitting frame is 3 before the "special" frames.

Also missing: party dance state 6 animation (frames num58-5/num58-4 bobbing + note dust), chat frames for states 3/4/16/17, face-player emote 112, state 23 cheer frames. And attack frames (ai[0]=10/12/14/15 → FindFrame attack animation) — does our renderer animate attack states? n.frame stays walking frame 0 during attack (atkUpdate sets vx*=0.8 → frame 0; vanilla FindFrame during attack states uses attack frames num58..npcFrameCount-1 with frameCounter advancing). Let me verify vanilla FindFrame attack-state handling to confirm frames used during attack. Search FindFrame for ai[0]==10 etc.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:38:39.168Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '69700,69900p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"",
 "description": "Read FindFrame attack states and walking branch"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:38:39.196Z

**📎 ToolResult**

```
					{
						num72 = ((frameCounter % 16.0 < 8.0) ? (num58 - 2) : 0);
					}
					else if (frameCounter < 160.0)
					{
						num72 = 0;
					}
					else if (frameCounter != 160.0)
					{
						num72 = ((frameCounter < 220.0) ? ((frameCounter % 12.0 < 6.0) ? (num58 - 2) : 0) : 0);
					}
					else
					{
						EmoteBubble.NewBubbleNPC(new WorldUIAnchor(this), 60);
					}
					frame.Y = num * num72;
					if (frameCounter >= 220.0)
					{
						frameCounter = 0.0;
					}
				}
				else if (ai[0] == 9f)
				{
					frameCounter += 1.0;
					int num73 = frame.Y / num;
					int num60 = num58 - num73;
					if ((uint)(num60 - 1) > 1u && (uint)(num60 - 4) > 1u && num73 != 0)
					{
						frame.Y = 0;
						frameCounter = 0.0;
					}
					int num74 = 0;
					num74 = ((!(frameCounter < 10.0)) ? ((!(frameCounter < 16.0)) ? (num58 - 4) : (num58 - 5)) : 0);
					if (ai[1] < 16f)
					{
						num74 = num58 - 5;
					}
					if (ai[1] < 10f)
					{
						num74 = 0;
					}
					frame.Y = num * num74;
				}
				else if (ai[0] == 18f)
				{
					frameCounter += 1.0;
					int num75 = frame.Y / num;
					int num60 = num58 - num75;
					if ((uint)(num60 - 1) > 1u && (uint)(num60 - 4) > 1u && num75 != 0)
					{
						frame.Y = 0;
						frameCounter = 0.0;
					}
					int num76 = 0;
					if (frameCounter < 10.0)
					{
						num76 = 0;
					}
					else if (frameCounter < 16.0)
					{
						num76 = num58 - 1;
					}
					else
					{
						num76 = num58 - 2;
					}
					if (ai[1] < 16f)
					{
						num76 = num58 - 1;
					}
					if (ai[1] < 10f)
					{
						num76 = 0;
					}
					num76 = Main.npcFrameCount[type] - 2;
					frame.Y = num * num76;
				}
				else if (ai[0] == 10f || ai[0] == 13f)
				{
					frameCounter += 1.0;
					int num77 = frame.Y / num;
					int num60 = num77 - num58;
					if ((uint)num60 > 3u && num77 != 0)
					{
						frame.Y = 0;
						frameCounter = 0.0;
					}
					int num78 = 10;
					int num79 = 6;
					if (type == 633)
					{
						num78 = 0;
						num79 = 2;
					}
					int num80 = 0;
					num80 = ((!(frameCounter < (double)num78)) ? ((frameCounter < (double)(num78 + num79)) ? num58 : ((frameCounter < (double)(num78 + num79 * 2)) ? (num58 + 1) : ((frameCounter < (double)(num78 + num79 * 3)) ? (num58 + 2) : ((frameCounter < (double)(num78 + num79 * 4)) ? (num58 + 3) : 0)))) : 0);
					frame.Y = num * num80;
				}
				else if (ai[0] == 15f)
				{
					frameCounter += 1.0;
					int num81 = frame.Y / num;
					int num60 = num81 - num58;
					if ((uint)num60 > 3u && num81 != 0)
					{
						frame.Y = 0;
						frameCounter = 0.0;
					}
					float num82 = ai[1] / (float)NPCID.Sets.AttackTime[type];
					int num83 = 0;
					num83 = ((num82 > 0.65f) ? num58 : ((num82 > 0.5f) ? (num58 + 1) : ((num82 > 0.35f) ? (num58 + 2) : ((num82 > 0f) ? (num58 + 3) : 0))));
					frame.Y = num * num83;
				}
				else if (ai[0] == 25f)
				{
					frame.Y = num;
				}
				else if (ai[0] == 12f)
				{
					frameCounter += 1.0;
					int num84 = frame.Y / num;
					int num60 = num84 - num58;
					if ((uint)num60 > 4u && num84 != 0)
					{
						frame.Y = 0;
						frameCounter = 0.0;
					}
					int num85 = num58 + GetShootingFrame(ai[2]);
					frame.Y = num * num85;
				}
				else if (ai[0] == 14f || ai[0] == 24f)
				{
					frameCounter += 1.0;
					int num86 = frame.Y / num;
					int num60 = num86 - num58;
					if ((uint)num60 > 1u && num86 != 0)
					{
						frame.Y = 0;
						frameCounter = 0.0;
					}
					int num87 = 12;
					int num88 = ((frameCounter % (double)num87 * 2.0 < (double)num87) ? num58 : (num58 + 1));
					frame.Y = num * num88;
					if (ai[0] == 24f)
					{
						if (frameCounter == 60.0)
						{
							EmoteBubble.NewBubble(87, new WorldUIAnchor(this), 60);
						}
						if (frameCounter == 150.0)
						{
							EmoteBubble.NewBubble(3, new WorldUIAnchor(this), 90);
						}
						if (frameCounter >= 240.0)
						{
							frame.Y = 0;
						}
					}
				}
				else if (ai[0] == 1001f)
				{
					frame.Y = num * (num58 - 1);
					frameCounter = 0.0;
				}
				else if (CanTalk && (ai[0] == 3f || ai[0] == 4f))
				{
					frameCounter += 1.0;
					int num89 = frame.Y / num;
					int num60 = num58 - num89;
					if ((uint)(num60 - 1) > 1u && (uint)(num60 - 4) > 1u && num89 != 0)
					{
						frame.Y = 0;
						frameCounter = 0.0;
					}
					bool flag8 = ai[0] == 3f;
					int num90 = 0;
					int num91 = 0;
					int num92 = -1;
					int num93 = -1;
					if (frameCounter < 10.0)
					{
						num90 = 0;
					}
					else if (frameCounter < 16.0)
					{
						num90 = num58 - 5;
					}
					else if (frameCounter < 46.0)
					{
						num90 = num58 - 4;
					}
					else if (frameCounter < 60.0)
					{
						num90 = num58 - 5;
					}
					else if (frameCounter < 216.0)
					{
						num90 = 0;
					}
					else if (frameCounter == 216.0 && Main.netMode != 1)
					{

```


---

## 🤖 Assistant · 2026-08-17T04:39:01.320Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
This confirms the frame machinery. Our implementation uses only frames 0/1/2+ (walk) — missing: sitting frame (num58-3), dance (num58-5/-4), chat (num58-1/-2 alternating), attack frames (num58..+3), shooting frames (GetShootingFrame), swing (num58..+3 by progress), state 7 face (0 with emote 112), state 18 (npcFrameCount-2), state 23 cheer.

Wait — actually, does our attack visual show any attack frames? attackUpdate does vx*=0.8 → frame 0. So town NPCs attack while standing in walk frame 0 — no attack animation. That's part of "自卫攻击+持械视觉" which memory says was done — the holdout weapon for bow family is drawn (attackState===12 → drawTownHoldout) but the frame stays 0. Vanilla uses GetShootingFrame(ai[2]) aiming frames. So partial.

Now — let me also verify the "night" state in our code handles rain-day: vanilla `flag` includes rain during day — NPCs go home during rain even in daytime. Ours: `else if (this.home)` branch — the condition is `!stationary && world.clock.isDay && !this.sitting` — daytime walking; else (night OR sitting OR stationary) → go home. During day rain: isDay=true → walk branch (not home!). Wait: the walk branch condition is `!this.stationary && world.clock.isDay && !this.sitting` — during day rain, NPCs keep wandering instead of going home. Vanilla: rain during day → flag=true → housed NPCs that are not at resting spot teleport home (and walk home if at home area? no — during flag, state 0 handles "walk to floorX/floorY"; they return home). **Deviation: day-rain home return missing.**

Actually wait — let me double check vanilla behavior for rain during day: flag = Main.raining → true. Then:
- The teleport-home block runs (rain → teleport if no player nearby & not at good resting spot).
- State 0: `else if (flag && !flag5 && !TownCritter)` → if not at floor spot → set state 1 walk toward home (direction toward floorX).
- FindGoodRestingSpot during day returns home floor (no chair scan since dayTime) → floorX/floorY = home ground. So NPCs walk/teleport home during day rain and stand there (no sitting — day early return). ✓ vanilla: NPCs go home when raining, even during day.

Ours: no — during day rain, NPCs wander freely (only sitFlag used for restSpot=null since isDay, teleport-home uses flag=sitFlag ✓ — wait the teleport home block DOES use `flag = sitFlag` which includes rain during day! So ours does teleport home during day rain when player far. But the walk-home branch (`else if (this.home)`) only runs when NOT day. So during day rain with player nearby (no teleport), our NPCs keep wandering instead of walking home. Partial deviation.

Hmm wait, actually let me re-read our branch:
```
} else if (!this.stationary && world.clock.isDay && !this.sitting) {
  // day wander
} else if (this.home) {
  // night go home
}
```
So during day: wander (unless stationary or sitting). During night: walk toward home/restSpot. During day rain: wander + teleport-home (if player far). Vanilla: walk home during rain day. Deviation (minor-moderate).

Also note: vanilla wander leash to home applies at ALL times (day too) — the ±25/±50 forcing is in state 0/1 general flow (`if (Main.netMode != 1 && (!flag || IsInAGoodRestingSpot))` — during day flag=false unless raining so it applies). Our day wander has NO leash (except leashHome=true ones which get set when housed: `n.leashHome = true` in updateTownNpcArrival — wait! In updateTownNpcArrival, when a house is assigned, `n.leashHome = true`. And leashHome logic: turn back when >10 tiles from home. So housed NPCs DO have a leash of 10 tiles. Unhoused (homeless) NPCs have no leash — vanilla homeless NPCs wander freely (no home → homeTileX set to spawn point at first ground contact? Actually `homeless` NPCs: homeTileX/homeTileY = where they currently stand? At :53704: `else if (homeTileX == -1 && homeTileY == -1 && velocity.Y == 0f) UpdateHomeTileState(homeless, centerX/16, feetY/16)` — homeless NPCs anchor home at first standing spot, then wander ±25 around THAT. So vanilla homeless NPCs stay near where they settled. Ours: homeless wander unbounded.

Leash radius: ours 10 tiles vs vanilla 25 (soft, force-turn at 50). Different magnitude.

Now walk speeds: ours accel 0.06 cap 0.8; vanilla 0.07 accel cap 1.0 (num22=1f, num23=0.07f). Deviation.

Also vanilla: while walking away from home beyond ±35 tiles, ai[1] -= 5 extra per tick (walk home faster). Ours N/A.

Next, check our danger flee. Let me grep for any flee logic in TownNPC or Game — search "flee".
````

</details>


---

## 🤖 Assistant · 2026-08-17T04:39:02.371Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"flee\\|cower\\|stinky\\|PrettySafe\\|TOWN_PRETTY_SAFE\" ~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts | head; grep -rn \"flee\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | head -5",
 "description": "Check flee/cower logic in our town NPC"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:39:02.409Z

**📎 ToolResult**

```
22:  TOWN_MELEE, TOWN_BOW, TOWN_MAGIC, TOWN_SWING, TOWN_PRETTY_SAFE,
986:   *  - flag31 门 ≈ 空闲+站地+触发冷却尽+探测范围内有可打敌(flag16;stinky 分支无系统跳过)
1149:    // 229 PrettySafe 近距保命换炮弹(:55128-55135)
1150:    const pretty = TOWN_PRETTY_SAFE[this.vanillaId];

```


---

## 🤖 Assistant · 2026-08-17T04:39:04.070Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"PrettySafe\\|DangerDetectRange\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | sed -n '1,5p'; grep -n \"public static int\\[\\] DangerDetectRange\\|DangerDetectRange = \\|PrettySafe = \\|AttackAverageChance = \" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPCID.cs\" 2>/dev/null | head; ls ~/Project/GLM/SandboxWorld/Terarria1456/ | head -20",
 "description": "Check NPCID sets defaults"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:39:04.110Z

**📎 ToolResult**

```
53866:		if (NPCID.Sets.DangerDetectRange[type] != -1)
53868:			num11 = NPCID.Sets.DangerDetectRange[type];
53982:					if (NPCID.Sets.PrettySafe[type] != -1 && (float)NPCID.Sets.PrettySafe[type] < num20)
54754:			float num49 = NPCID.Sets.DangerDetectRange[type];
55128:				if (localAI[3] == 0f && num59 != -1 && Distance(Main.npc[num59].Center) < (float)NPCID.Sets.PrettySafe[type])
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

```


---

## 🤖 Assistant · 2026-08-17T04:39:11.267Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: **no flee behavior** in our TownNPC — only attack. Vanilla town NPCs flee from danger (direction = away from enemy, num22 speed boost 1.5 + damage-based extra speed when fleeing in danger: `if (friendly && (flag16 || flag21)) { num22 = 1.5f + num24*0.9f; num23=0.1f }` — they run FASTER when fleeing (1.5× + up to +0.9 based on missing life). And state 8 freeze when cornered. Our NPCs stand still and fight. **Major behavioral deviation.**

Wait — I should double check: maybe fleeing is handled elsewhere in our code (Game.ts or Enemy.ts?). Let me search "runAway" or similar... Let me search more broadly for danger handling in TownNPC context.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:39:12.631Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"TOWN_DANGER_RANGE\\|danger\" ~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts ~/Project/GLM/SandboxWorld/game/src/data/vanillaTownAttack.ts | head -15; grep -rn \"townNpc.*flee\\|npc.*runAway\\|runFrom\" ~/Project/GLM/SandboxWorld/game/src/ --include=\"*.ts\" | head -5",
 "description": "Check danger range usage and any flee logic anywhere"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:39:12.680Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/data/vanillaTownAttack.ts:11:export const TOWN_DANGER_RANGE: Record<number, number> = {
~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts:21:  TOWN_ATTACK_TIME, TOWN_ATTACK_CHANCE, TOWN_ATTACK_TYPE, TOWN_DANGER_RANGE,
~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts:1018:      const range = TOWN_DANGER_RANGE[this.vanillaId] ?? 200;
~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts:1045:    const range = TOWN_DANGER_RANGE[this.vanillaId] ?? 200;

```


---

## 🤖 Assistant · 2026-08-17T04:39:28.835Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed — flee behavior entirely missing. Now let me verify vanilla NPC death handling for town NPCs (NPCLoot) and the respawn semantics. Also check "hit flash" (vanilla GetAlpha flash) vs ours, and check honey behavior for NPCs. Also check knockback for town NPC (vanilla StrikeNPC knockback applied, townNPC no resist?), iframes default.

Let me look at vanilla StrikeNPC/HitEffect quickly for town NPC specifics: NPC.immunity — town NPC hit immunity default 10 ticks? In vanilla, when NPC is struck: `immune[255]`? Actually NPC has `immune[256]`? NPC immunity is `immune[playerCount+1]`... NPC.cs: immune array is per-attacker plus [255] for environment. For player strikes, immunity = 10 ticks typically ("npc.immune[Main.myPlayer] = 10"). For town NPC hurt by our system — we use single iframes=8. Vanilla: `if (townNPC) ... immune = 10`? Let me check StrikeNPCHitInfo and "immune[" assignments. This is item 9/10 (invincibility frames).

Also check vanilla hit flash: NPC color flash when hit — "justHit" in Main.DrawNPC (`if (npc.justHit)` white flash?). Vanilla: NPCs flash when hit via `npc.HitEffect` → in draw, `GetAlpha` with `npc.justHit` → brighter? Let me check quickly.

Also — player pushing NPCs: let me verify vanilla has none. Actually! There IS: `Collision` between player and town NPC? No. But there IS the "NPC pushed by Conveyor belts" — `npc.Conveyor` handling in AI_007? I saw none in AI_007; conveyors are handled in Collision.TileCollision? Hmm, conveyors affect NPC velocity in `Collision.TileCollision`? Actually conveyor movement for NPCs is in NPC.VanillaAI... there's `num243` stuff. Not part of the 10 audit items though item 7 is "被玩家推动/挤开行为" — answer likely "原版无玩家推挤 NPC 行为"（玩家与 NPC 无实体碰撞）。Let me confirm quickly by checking Player collision with NPC — there is none in vanilla (players walk through NPCs). Actually wait — vanilla players DO collide with town NPCs? No! Players pass through NPCs. Confirmed by gameplay knowledge; but let me grep for evidence. In Player.cs there's no NPC collision. NPC push by other NPCs? There's `NPCSeparation`? no. OK.

Now death: vanilla town NPC death:
- NPCLoot: town NPC drops nothing except... let me check. Also gore. And "lifeRegen"? And on death, they respawn via checkTownNPCs (UpdateTime_SpawnTownNPCs) — every 7200 ticks check: if NPC not present && conditions met (has house? no — town NPC respawn requires empty house? Let me read Main.cs 65021-65100).
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:39:29.296Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '65021,65120p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs\"",
 "description": "Read vanilla UpdateTime_SpawnTownNPCs"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:39:29.326Z

**📎 ToolResult**

```
	private static void UpdateTime_SpawnTownNPCs(bool forceUpdate)
	{
		int worldUpdateRate = WorldGen.GetWorldUpdateRate();
		if (netMode == 1 || !(worldUpdateRate > 0 || forceUpdate))
		{
			return;
		}
		checkForSpawns++;
		if (!forceUpdate && checkForSpawns < 7200 / worldUpdateRate)
		{
			return;
		}
		checkForSpawns = 0;
		int num = 0;
		for (int i = 0; i < 255; i++)
		{
			if (player[i].active)
			{
				num++;
			}
		}
		for (int j = 0; j < NPCID.Count; j++)
		{
			townNPCCanSpawn[j] = false;
		}
		WorldGen.prioritizedTownNPCType = 0;
		int num2 = 0;
		int num3 = 0;
		int num4 = 0;
		int num5 = 0;
		int num6 = 0;
		int num7 = 0;
		int num8 = 0;
		int num9 = 0;
		int num10 = 0;
		int num11 = 0;
		int num12 = 0;
		int num13 = 0;
		int num14 = 0;
		int num15 = 0;
		int num16 = 0;
		int num17 = 0;
		int num18 = 0;
		int num19 = 0;
		int num20 = 0;
		int num21 = 0;
		int num22 = 0;
		int num23 = 0;
		int num24 = 0;
		int num25 = 0;
		int num26 = 0;
		int num27 = 0;
		int num28 = 0;
		int num29 = 0;
		int num30 = 0;
		int num31 = 0;
		int num32 = 0;
		int num33 = 0;
		int num34 = 0;
		int num35 = 0;
		int num36 = 0;
		int num37 = 0;
		int num38 = 0;
		int num39 = 0;
		int num40 = 0;
		for (int k = 0; k < maxNPCs; k++)
		{
			if (npc[k].active && npc[k].townNPC)
			{
				if (npc[k].type != 368 && npc[k].type != 37 && npc[k].type != 453 && !npc[k].homeless)
				{
					WorldGen.QuickFindHome(k);
				}
				if (npc[k].type == 37)
				{
					num7++;
				}
				if (npc[k].type == 17)
				{
					num2++;
				}
				if (npc[k].type == 18)
				{
					num3++;
				}
				if (npc[k].type == 19)
				{
					num5++;
				}
				if (npc[k].type == 20)
				{
					num4++;
				}
				if (npc[k].type == 22)
				{
					num6++;
				}
				if (npc[k].type == 38)
				{
					num8++;

```


---

## 🤖 Assistant · 2026-08-17T04:39:34.425Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This confirms the every-7200-ticks town NPC evaluation — our implementation runs at `tickCount % 7200 === 600` and does a similar job (with QuickFindHome for homeless etc.). Note vanilla: `if (npc[k].type != 368 && type != 37 && != 453 && !homeless) WorldGen.QuickFindHome(k)` — every cycle re-validates homes. Ours: `for (const n of npcs) { if (n.home || n.bound ...) continue; findFreeHouse... }` — we only re-house NPCs WITHOUT home, we don't re-validate existing homes. Minor.

Now vanilla NPCLoot for townNPC death. Let me check.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:39:35.268Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"public void NPCLoot\\|void NPCLoot(DamageType\" \"~/Project/GLM/SandboxWorld/Terrarria1456/Terraria/NPC.cs\"; grep -n \"if (townNPC)\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | head -20",
 "description": "Find NPCLoot and townNPC branches"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:39:35.301Z

**📎 ToolResult**

```
ugrep: warning: ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria/NPC.cs: No such file or directory
81904:			if (townNPC)
82033:			if (townNPC)
91252:		if (townNPC)
91533:			if (townNPC)
91648:		if (townNPC)

```


---

## 🤖 Assistant · 2026-08-17T04:39:40.282Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"void NPCLoot\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"; sed -n '91240,91290p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"; echo ---; sed -n '91520,91620p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"",
 "description": "Read townNPC death handling in NPCLoot and UpdateNPC"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:39:40.340Z

**📎 ToolResult**

```
79628:	public void NPCLoot()
79726:	private void NPCLoot_DropItems(Player closestPlayer)
79899:	private void NPCLoot_DropHeals(Player closestPlayer)
80332:	private void NPCLoot_DropCommonLifeAndMana(Player closestPlayer)
80351:	private void NPCLoot_DropDungeonStuff()
80377:	private void NPCLoot_DropTempleTraps()
80384:	private void NPCLoot_DropLihzahrdStuff()
80393:	private void NPCLoot_DropAltar()
80406:	private void NPCLoot_DropHellforge()
80412:	private void NPCLoot_DropMoney(Player closestPlayer)
			{
				SoundEngine.PlaySound(29, (int)position.X, (int)position.Y, Main.rand.Next(84, 86));
			}
			else if (type == 391 && Main.rand.Next(700) == 0)
			{
				SoundEngine.PlaySound(29, (int)position.X, (int)position.Y, Main.rand.Next(86, 87));
			}
		}
	}

	public void UpdateAltTexture()
	{
		if (townNPC)
		{
			int oldAltTexture = altTexture;
			bool flag = BirthdayParty.PartyIsUp || ForcePartyHatOn;
			if (type == 441 || type == 453 || type == 633)
			{
				flag = false;
			}
			altTexture = 0;
			if (flag)
			{
				altTexture = 1;
			}
			if (type == 633 && ShouldBestiaryGirlBeLycantrope())
			{
				altTexture = 2;
			}
			if (!ForcePartyHatOn)
			{
				MakeTransitionEffectsForTextureChanges(oldAltTexture, altTexture);
			}
		}
	}

	private void MakeTransitionEffectsForTextureChanges(int oldAltTexture, int currentAltTexture)
	{
		if (oldAltTexture == 0 && currentAltTexture == 1)
		{
			for (int i = 0; i < 20; i++)
			{
				Dust.NewDust(position, width, height / 4, 139 + Main.rand.Next(4), 0f, -2f);
			}
		}
		if (oldAltTexture == 1 && currentAltTexture == 0)
		{
			Utils.PoofOfSmoke(position);
		}
		if (type != 633)
		{
---
		{
			velocity.Y += gravity;
			if (velocity.Y > maxFallSpeed)
			{
				velocity.Y = maxFallSpeed;
			}
		}
		if ((double)velocity.X < 0.005 && (double)velocity.X > -0.005)
		{
			velocity.X = 0f;
		}
		if (Main.netMode != 1 && type != 37 && (friendly || NPCID.Sets.TakesDamageFromHostilesWithoutBeingFriendly[type]))
		{
			if (townNPC)
			{
				CheckDrowning();
			}
			CheckLifeRegen();
			GetHurtByOtherNPCs(NPCID.Sets.AllNPCs);
		}
		if (Main.netMode != 1 && (npcsFoundForCheckActive[210] || npcsFoundForCheckActive[211]) && NPCID.Sets.CanBeHurtByBees[type] && (type != 1 || (ai[1] != 1124f && ai[1] != 1125f)))
		{
			GetHurtByOtherNPCs(NPCID.Sets.HurtingBees);
		}
		if (!noTileCollide)
		{
			UpdateCollision();
		}
		else
		{
			oldPosition = position;
			oldDirection = direction;
			position += velocity;
			if (Collision.WetCollision(position, width, height))
			{
				TryRemovingWaterPerishableEffects(isInLava: false);
			}
		}
		if (Main.netMode != 1 && !noTileCollide && lifeMax > 1 && Collision.SwitchTiles(this, position, width, height, oldPosition, 2) && (type == 46 || type == 148 || type == 149 || type == 303 || type == 361 || type == 362 || type == 364 || type == 366 || type == 367 || (type >= 442 && type <= 448) || type == 602 || type == 608 || type == 614 || type == 687))
		{
			ai[0] = 1f;
			ai[1] = 400f;
			ai[2] = 0f;
		}
		CheckDialogue();
		FindFrame();
		UpdateNPC_UpdateTrails();
		UpdateNetworkCode(i);
		CheckActive();
		netUpdate = false;
		justHit = false;
	}

	private void CheckDialogue()
	{
		if (Main.netMode != 2)
		{
			if ((Main.GameUpdateCount + whoAmI) % 10 == 0L)
			{
				ConditionalDialogue.TryGetPendingDialogue(this, out nextDialogue);
			}
			else if (nextDialogue != null && !nextDialogue.ConditionsMet(this))
			{
				nextDialogue = null;
			}
		}
	}

	private void SubAI_HandleTemporaryCatchableNPCPlayerInvulnerability()
	{
		if (type >= 0 && type < NPCID.Count && Main.npcCatchable[type])
		{
			if (releaseOwner != 255 || SpawnedFromStatue)
			{
				catchableNPCTempImmunityCounter = 0;
			}
			bool num = friendly;
			if (catchableNPCTempImmunityCounter > 0)
			{
				catchableNPCTempImmunityCounter--;
				friendly = true;
			}
			else
			{
				friendly = false;
			}
			if (num != friendly)
			{
				netUpdate = true;
			}
		}
	}

	private void TrySyncingUniqueTownNPCData(int npcIndex)
	{
		if (Main.netMode == 1 && needsUniqueInfoUpdate && isLikeATownNPC)
		{
			needsUniqueInfoUpdate = false;
			NetMessage.SendData(56, -1, -1, null, npcIndex);
		}
	}

```


---

## 🤖 Assistant · 2026-08-17T04:39:43.267Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Important find: **CheckDialogue** — `ConditionalDialogue.TryGetPendingDialogue` every 10 ticks — this is the "NPC proactively talks to player with dialogue bubble" system (1.4.4)! Let me check ConditionalDialogue to catalog conditions (this is item 4: 对话触发). Let me find it.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:39:43.914Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/Terarria1456 -name \"ConditionalDialogue.cs\" | head -2; grep -rn \"class ConditionalDialogue\" ~/Project/GLM/SandboxWorld/Terarria1456/ --include=\"*.cs\" | head -2",
 "description": "Locate ConditionalDialogue class"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:39:43.971Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/ConditionalDialogue.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/ConditionalDialogue.cs:9:public abstract class ConditionalDialogue

```


---

## 🤖 Assistant · 2026-08-17T04:39:47.099Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/Terarria1456/Terrarria.GameContent/ConditionalDialogue.cs; sed -n '1,120p' ~/Project/GLM/SandboxWorld/Terarria1456/Terrarria.GameContent/ConditionalDialogue.cs",
 "description": "Read ConditionalDialogue system"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:39:47.127Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
wc: ~/Project/GLM/SandboxWorld/Terarria1456/Terrarria.GameContent/ConditionalDialogue.cs: open: No such file or directory
sed: ~/Project/GLM/SandboxWorld/Terarria1456/Terrarria.GameContent/ConditionalDialogue.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-17T04:39:49.209Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The directory name is "Terraria.GameContent" — I typo'd "Terrarria.GameContent". Let me fix.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:39:51.051Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/ConditionalDialogue.cs\"; grep -c \"new ConditionalDialogue\\|ShowIf\\|: ConditionalDialogue\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/ConditionalDialogue.cs\"; grep -n \"Lang.lp\\|GetSpecialEventText\\|bubbleText\\|TimedConditionalDialogue\\|class .*ConditionalDialogue\" \"~/Project/GLM/SandboxWorld/Terrarria1456/Terraria.GameContent/ConditionalDialogue.cs\" | head -20",
 "description": "Survey ConditionalDialogue classes"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:39:51.097Z

**📎 ToolResult**

```
     127 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/ConditionalDialogue.cs
1
ugrep: warning: ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria.GameContent/ConditionalDialogue.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-17T04:39:53.198Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/ConditionalDialogue.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:39:53.209Z

**📎 ToolResult**

```
1	using System;
2	using System.Collections.Generic;
3	using Terraria.DataStructures;
4	using Terraria.ID;
5	using Terraria.Localization;
6	
7	namespace Terraria.GameContent;
8	
9	public abstract class ConditionalDialogue
10	{
11		public static class ItemGroups
12		{
13			public static RecipeGroup Ore = new RecipeGroup("RecipeGroups.Ore", 699, 12, 11, 700, 14, 701, 13, 702);
14	
15			public static RecipeGroup Bars = new RecipeGroup("RecipeGroups.Bar", 703, 20, 22, 704, 21, 705, 19, 706);
16	
17			public static RecipeGroup Anvils = new RecipeGroup("ItemName.IronAnvil", 35, 716);
18	
19			public static RecipeGroup Whips = new RecipeGroup("RecipeGroups.Whip");
20	
21			public static RecipeGroup Mounts = new RecipeGroup("RecipeGroups.Mount");
22	
23			internal static void PostSetupContent()
24			{
25				foreach (Item value in ContentSamples.ItemsByType.Values)
26				{
27					if (ProjectileID.Sets.IsAWhip[value.shoot])
28					{
29						Whips.Add(value.type);
30					}
31				}
32				foreach (Item value2 in ContentSamples.ItemsByType.Values)
33				{
34					if (value2.mountType != -1)
35					{
36						Mounts.Add(value2.type);
37					}
38				}
39			}
40		}
41	
42		private class FreeCakeDialogue : ConditionalDialogue
43		{
44			public FreeCakeDialogue()
45				: base((NPC _) => NPC.freeCake)
46			{
47			}
48	
49			public override string GetChatAndClearCondition(NPC npc)
50			{
51				NPC.freeCake = false;
52				NetMessage.SendData(51, -1, -1, null, 0, 10f);
53				Item item = new Item();
54				item.SetDefaults(3750);
55				Main.LocalPlayer.QuickSpawnItem(new EntitySource_Gift(npc), item, GetItemSettings.GiftRecieved);
56				return Language.GetTextValue("PartyGirlSpecialText.Cake" + Main.rand.Next(1, 4));
57			}
58		}
59	
60		private static List<ConditionalDialogue>[] _registry = new List<ConditionalDialogue>[NPCID.Count];
61	
62		public readonly Predicate<NPC> ConditionsMet;
63	
64		public bool ShowIndicator { get; private set; }
65	
66		private static void Register(int npcType, ConditionalDialogue dialogue)
67		{
68			List<ConditionalDialogue> list = _registry[npcType];
69			if (list == null)
70			{
71				list = (_registry[npcType] = new List<ConditionalDialogue>());
72			}
73			list.Add(dialogue);
74		}
75	
76		public static bool TryGetPendingDialogue(NPC npc, out ConditionalDialogue dialogue)
77		{
78			dialogue = null;
79			List<ConditionalDialogue> list = _registry[npc.type];
80			if (list == null)
81			{
82				return false;
83			}
84			foreach (ConditionalDialogue item in list)
85			{
86				if (item.ConditionsMet(npc))
87				{
88					dialogue = item;
89					return true;
90				}
91			}
92			return false;
93		}
94	
95		public ConditionalDialogue(Predicate<NPC> condition = null)
96		{
97			ShowIndicator = true;
98			ConditionsMet = condition ?? ((Predicate<NPC>)((NPC _) => true));
99		}
100	
101		public void HideIndicator()
102		{
103			ShowIndicator = false;
104		}
105	
106		public abstract string GetChatAndClearCondition(NPC npc);
107	
108		public void Register(int npcType)
109		{
110			Register(npcType, this);
111		}
112	
113		internal static void Init()
114		{
115			new FreeCakeDialogue().Register(208);
116		}
117	
118		public static Predicate<NPC> CreateInventoryCondition(RecipeGroup item, int stack)
119		{
120			return CreateInventoryCondition(new Recipe.RequiredItemEntry(item, stack));
121		}
122	
123		public static Predicate<NPC> CreateInventoryCondition(params Recipe.RequiredItemEntry[] requiredItems)
124		{
125			return (NPC _) => Recipe.CollectedEnoughItemsToCraft(requiredItems);
126		}
127	}
128	

```


---

## 🤖 Assistant · 2026-08-17T04:39:58.952Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
ConditionalDialogue in vanilla base game only registers FreeCakeDialogue (party girl cake gift). The rest (merchant "you have 50 silver" etc.) — those come from... wait, that's vanilla 1.4.4's system where modded-like conditional dialogues; the vanilla game registers only FreeCake. The classic "merchant arrives" announcements etc. are elsewhere. Actually the "eye icon" / indicator over NPCs when they have something to say — in vanilla 1.4.4, NPCs show a "..." bubble? The nextDialogue → shown in draw (NPC draws dialogue bubble when nextDialogue != null, position 5 over head). Let me check where nextDialogue is consumed (draw). grep nextDialogue in Main.cs.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:39:59.628Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"nextDialogue\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs\" | head; grep -rn \"nextDialogue\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs\" | head -5",
 "description": "Find nextDialogue consumption"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:39:59.681Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:45484:				bool flag2 = npc[num2].nextDialogue != null && npc[num2].nextDialogue.ShowIndicator;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:56028:		if (theNPC is NPC { nextDialogue: not null } nPC && nPC.nextDialogue.ShowIndicator)

```


---

## 🤖 Assistant · 2026-08-17T04:40:04.364Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '56015,56060p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs\"; sed -n '45470,45520p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs\"",
 "description": "Read nextDialogue draw and interaction"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:40:04.401Z

**📎 ToolResult**

```
		if (!dedServ)
		{
			Pings.Add(position);
			if (netMode == 1)
			{
				NetManager.Instance.SendToServer(NetPingModule.Serialize(position));
			}
		}
	}

	private static void DrawNPCHeadFriendly(Entity theNPC, byte alpha, float headScale, SpriteEffects dir, int townHeadId, float x, float y)
	{
		TownNPCHeadRenderer.DrawWithOutlines(townHeadId, new Vector2(x, y), new Microsoft.Xna.Framework.Color(alpha, alpha, alpha, alpha), 0f, headScale, dir);
		if (theNPC is NPC { nextDialogue: not null } nPC && nPC.nextDialogue.ShowIndicator)
		{
			Utils.DrawNotificationIcon(spriteBatch, new Vector2(x, y - 20f));
		}
	}

	private static void DrawNPCHeadBoss(Entity theNPC, byte alpha, float headScale, float rotation, SpriteEffects effects, int bossHeadId, float x, float y)
	{
		BossNPCHeadRenderer.DrawWithOutlines(bossHeadId, new Vector2(x, y), new Microsoft.Xna.Framework.Color(alpha, alpha, alpha, alpha), rotation, headScale, effects);
	}

	private static void DrawWithOutlines(Entity entity, Texture2D tex, Vector2 position, Microsoft.Xna.Framework.Rectangle? rect, Microsoft.Xna.Framework.Color color, float rotation, Vector2 origin, float scale, SpriteEffects effects)
	{
		float num = 2f * scale;
		Microsoft.Xna.Framework.Color white = Microsoft.Xna.Framework.Color.White;
		int colorOnlyShaderIndex = ContentSamples.DyeShaderIDs.ColorOnlyShaderIndex;
		DrawData value = new DrawData(tex, position, rect, color, rotation, origin, scale, effects);
		GameShaders.Armor.Apply(colorOnlyShaderIndex, entity, value);
		Microsoft.Xna.Framework.Color black = Microsoft.Xna.Framework.Color.Black;
		black *= (float)(int)color.A / 255f;
		black *= (float)(int)color.A / 255f;
		Microsoft.Xna.Framework.Color color2 = white;
		color2 *= (float)(int)color.A / 255f;
		color2 *= (float)(int)color.A / 255f;
		int num2 = 2;
		Vector2 vector;
		for (int i = -num2; i <= num2; i++)
		{
			for (int j = -num2; j <= num2; j++)
			{
				if (Math.Abs(i) + Math.Abs(j) == num2)
				{
					vector = new Vector2((float)i * num, (float)j * num).RotatedBy(rotation);
					Vector2 stringSize = ChatManager.GetStringSize(FontAssets.MouseText.Value, npc[num2].GivenOrTypeName, Vector2.One);
					Vector2 vector3 = npc[num2].Bottom - screenPosition + new Vector2(0f, 10f);
					if (NPC.GetNPCLocation(num2, seekHead: true, averageDirection: true, out var _, out var pos))
					{
						vector3 = pos - screenPosition + new Vector2(0f, 10 + npc[num2].height / 2);
						if (player[myPlayer].gravDir == -1f)
						{
							vector3 = ReverseGravitySupport(vector3, -npc[num2].height - 20);
						}
						Vector2 origin = stringSize * new Vector2(0.5f, 0f);
						ChatManager.DrawColorCodedStringShadow(spriteBatch, FontAssets.MouseText.Value, npc[num2].GivenOrTypeName, vector3, Microsoft.Xna.Framework.Color.Black * npc[num2].nameOver * 0.5f, 0f, origin, Vector2.One);
						ChatManager.DrawColorCodedString(spriteBatch, FontAssets.MouseText.Value, npc[num2].GivenOrTypeName, vector3, Microsoft.Xna.Framework.Color.White * npc[num2].nameOver, 0f, origin, Vector2.One);
					}
				}
				bool flag2 = npc[num2].nextDialogue != null && npc[num2].nextDialogue.ShowIndicator;
				bool flag3 = false;
				if (!flag2 && NPC.CanShowHomelessText(num2))
				{
					flag2 = true;
					flag3 = true;
				}
				if (flag2 && (!flag3 || LocalPlayer.Distance(npc[num2].Center) < 105f))
				{
					Utils.DrawNotificationIcon(spriteBatch, npc[num2].Top + new Vector2(0f, npc[num2].gfxOffY - 10f), 1f, worldSpace: true);
				}
				if (npc[num2].type == 548 && !npc[num2].dontTakeDamageFromHostiles && DD2Event.TimeLeftBetweenWaves > 0 && !hideUI)
				{
					Vector2 position = npc[num2].Bottom - screenPosition + new Vector2(0f, -100f);
					int num7 = DD2Event.TimeLeftBetweenWaves / 60;
					string text = $"{num7}";
					DynamicSpriteFont value = FontAssets.MouseText.Value;
					float num8 = 1f;
					Vector2 origin2 = value.MeasureString(text) * num8 * new Vector2(0.5f, 0.5f);
					ChatManager.DrawColorCodedStringWithShadow(spriteBatch, value, text, position, Microsoft.Xna.Framework.Color.White, 0f, origin2, Vector2.One * num8);
				}
				npc[num2].position -= npc[num2].netOffset;
			}
		}
		for (int k = 0; k < 255; k++)
		{
			if (k != myPlayer && player[k].active && !player[k].ghost && !player[k].dead && !player[k].invis && player[k].statLife != player[k].statLifeMax2)
			{
				Vector2 vector4 = player[k].Bottom + player[k].netOffset + new Vector2(0f, player[k].gfxOffY);
				if (HealthBarDrawSettings == 1)
				{
					int num9 = 10;
					DrawHealthBar(vector4.X, vector4.Y + (float)num9, player[k].statLife, player[k].statLifeMax2, player[k].stealth * Lighting.Brightness((int)((player[k].position.X + (float)(player[k].width / 2)) / 16f), (int)((player[k].position.Y + (float)(player[k].height / 2) + player[k].gfxOffY) / 16f)));
				}
				else if (HealthBarDrawSettings == 2)
				{
					int num10 = -20;

```


---

## 🤖 Assistant · 2026-08-17T04:40:09.077Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good — vanilla has the "notification icon" (talk indicator) over NPCs with pending dialogue or homeless text (NPC.CanShowHomelessText + distance < 105). This is the "speech bubble icon" over NPCs heads. Ours? Let me check if we draw any indicator. Probably not — check Renderer for "homeless" or notification icon.

Now let me check the vanilla NPCLoot town NPC drop behavior (line 79628-79726).
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:40:09.429Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '79628,79726p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"",
 "description": "Read vanilla NPCLoot head"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:40:09.460Z

**📎 ToolResult**

```
	public void NPCLoot()
	{
		if (Main.netMode == 1 || type >= NPCID.Count || ((Main.getGoodWorld || !Main.isThereAWorldSurface) && !downedBoss3 && !Main.onlyShimmerOceanWorlds && (type == 31 || type == 294 || type == 296 || type == 295 || type == 32 || type == 34 || type == 71 || type == 693 || type == 694)) || (type == 32 && localAI[3] == 1f))
		{
			return;
		}
		Player closestPlayer = Main.player[Player.FindClosest(position, width, height)];
		if (0 == 0)
		{
			CountKillForAchievements();
			if (GetWereThereAnyInteractions())
			{
				if (IsNPCValidForBestiaryKillCredit())
				{
					Main.BestiaryTracker.Kills.RegisterKill(this);
				}
				CountKillForBannersAndDropThem();
			}
		}
		if ((SpawnedFromStatue && NPCID.Sets.NoEarlymodeLootWhenSpawnedFromStatue[type] && !Main.hardMode) || (SpawnedFromStatue && NPCID.Sets.StatueSpawnedDropRarity[type] != -1f && (Main.rand.NextFloat() >= NPCID.Sets.StatueSpawnedDropRarity[type] || !AnyInteractions())))
		{
			return;
		}
		bool flag = downedMechBoss1 && downedMechBoss2 && downedMechBoss3;
		DoDeathEvents_BeforeLoot(closestPlayer);
		NPCLoot_DropItems(closestPlayer);
		DoDeathEvents(closestPlayer);
		if (SpecialSeedFeatures.Mechdusa)
		{
			int num = type;
			if ((uint)(num - 125) <= 2u || num == 134)
			{
				bool flag2 = type == 127 || !AnyNPCs(127);
				bool flag3 = type == 134 || !AnyNPCs(134);
				bool num2 = type == 126 || !AnyNPCs(126);
				bool flag4 = type == 125 || !AnyNPCs(125);
				if (num2 && flag4 && flag3 && flag2)
				{
					AchievementsHelper.NotifyProgressionEvent(31);
				}
			}
		}
		if (!flag && downedMechBoss1 && downedMechBoss2 && downedMechBoss3 && Main.hardMode)
		{
			ChatHelper.BroadcastChatMessage(NetworkText.FromKey(Lang.misc[32].Key), ChatColors.World);
		}
		if (IsNPCValidForBestiaryKillCredit())
		{
			if (type == 4 && WorldGen.Skyblock.noAltars)
			{
				NPCLoot_DropAltar();
			}
			if ((type == 14 || type == 13 || type == 15 || type == 266) && WorldGen.Skyblock.noDungeon)
			{
				NPCLoot_DropDungeonStuff();
			}
			if (type == 35 && WorldGen.Skyblock.noHellforge)
			{
				NPCLoot_DropHellforge();
			}
			if (type == 262 && WorldGen.Skyblock.noTemple)
			{
				NPCLoot_DropLihzahrdStuff();
			}
			if (type == 245 && WorldGen.Skyblock.lowTiles)
			{
				NPCLoot_DropTempleTraps();
			}
		}
		NPCLoot_DropMoney(closestPlayer);
		NPCLoot_DropHeals(closestPlayer);
	}

	public bool IsNPCValidForBestiaryKillCredit()
	{
		switch (type)
		{
		case 121:
			return false;
		case 13:
		case 14:
		case 15:
			return boss;
		default:
			return true;
		}
	}

	private void DoDeathEvents_BeforeLoot(Player closestPlayer)
	{
		int num = type;
		if ((uint)(num - 125) <= 1u && AnyNPCs((type == 125) ? 126 : 125))
		{
			value = 0f;
			boss = false;
		}
	}

	private void NPCLoot_DropItems(Player closestPlayer)

```


---

## 🤖 Assistant · 2026-08-17T04:40:26.044Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Town NPC death in vanilla: NPCLoot_DropItems — town NPCs drop nothing normally (dropItem = 0 for town NPCs; there's the special case: guide voodoo... and "Santa" etc.). Also DoDeathEvents (gore). And money/heals: townNPC drop money? NPCLoot_DropMoney: `if (type == ...)` — town NPCs don't drop money (npc.value for town NPC is 0? Actually townNPC drop money? no). And DoDeathEvents spawns gore (Town NPC death gore + "NPC_Killed" sound).

Actually the key vanilla death behaviors for town NPC:
1. Gore pieces (each town NPC has gore via `Gore.NewGore` in HitEffect death — NPC.HitEffect case per type spawns specific gore textures).
2. Sound NPC_Killed_1.
3. No item drops (except special: tax collector? no).
4. Respawn: not immediate — the checkTownNPCs cycle (every 7200 ticks) re-spawns them if unlock conditions persist and housing available. So death respawn delay ≈ up to 2 minutes (7200 ticks = 2 min) — actually respawn happens on the next cycle, so worst case 2 min, average 1 min. Plus vanilla requires empty house? For already-unlocked NPC that died: `townNPCCanSpawn` — the standard requirement is: NPC not present, conditions met (e.g. merchant needs 50 silver), and... house? For the prioritized spawn: WorldGen.QuickFindHome etc. Actually vanilla respawns town NPCs without requiring the player to re-earn (except housing availability? they become homeless if no house). Fine.

Our death: hurt() → dead=true, particles + NPC_Killed_1 sound ✓, respawn via updateTownNpcArrival every 7200 ✓ (matches vanilla cadence). Gore pieces — we use red particles, not actual gore textures. Vanilla HitEffect for town NPCs spawns gore (e.g. guide gore pieces). Our approximation noted. Minor visual deviation.

One important vanilla death nuance: **townNPC death by player → townNPC don't retaliate**; also killing town NPC with player weapon: our TownNPC.hurt is only called by traps/projectiles? Player weapons hitting town NPCs — do we allow? Vanilla: friendly NPCs can be hit by player projectiles when... actually vanilla town NPCs can't be damaged by player weapons unless wearing voodoo doll etc.? No wait — town NPCs CAN be hit by players' attacks (except in Journey?). Hmm: vanilla town NPCs are hittable by player projectiles/weapons (they take damage, e.g. killing the Guide with weapons works... actually yes you can kill NPCs with weapons). NPC friendly: `if (npc.friendly)` projectiles don't hit them — player projectiles skip friendly NPCs EXCEPT voodoo... Let me not go down this path; it's outside the 10 items.

Now, let me check remaining specifics:

**Honey slow for town NPCs**: vanilla — honeyWet affects NPC movement? For players honey slows; for NPCs: NPC update has `if (honeyWet) velocity *= ...`? Let me check quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:40:26.847Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"honeyWet\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | head -10; grep -n \"justHit\\|GetAlpha\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | sed -n '1,12p'",
 "description": "Check honey and hit flash for NPCs"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:40:26.891Z

**📎 ToolResult**

```
8344:		honeyWet = false;
53602:			honeyWet = false;
91943:			else if (honeyWet)
93731:			honeyWet = false;
93752:			else if (honeyWet)
94267:				honeyWet = true;
94326:					else if (honeyWet)
94424:					else if (honeyWet)
96157:		if (flag && Main.rand.Next(20) == 0 && !lavaWet && !honeyWet && !shimmerWet)
6370:	public bool justHit;
8438:		justHit = false;
20806:				if (justHit)
21588:				if (justHit)
21752:				if (justHit)
21813:			if (justHit)
22826:				if (justHit)
22859:			if (justHit)
23559:					if (justHit && this.ai[2] == 0f)
23575:							if (justHit)
24742:			if (justHit)
24862:				if (justHit)

```


---

## 🤖 Assistant · 2026-08-17T04:40:30.082Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '91920,91985p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"; sed -n '94310,94440p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | grep -n \"honeyWet\\|velocity\" | head -12",
 "description": "Read NPC wet/honey velocity handling"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:40:30.133Z

**📎 ToolResult**

```
		else if (aiStyle == 7 && ai[0] == 25f)
		{
			gravity = 0f;
		}
		float num = (float)Main.maxTilesX / 4200f;
		num *= num;
		float num2 = (float)((double)(position.Y / 16f - (60f + 10f * num)) / (Main.worldSurface / 6.0));
		if ((double)num2 < 0.25)
		{
			num2 = 0.25f;
		}
		if (num2 > 1f)
		{
			num2 = 1f;
		}
		gravity *= num2;
		if (wet)
		{
			if (shimmerWet)
			{
				gravity = 0.15f;
				maxFallSpeed = 5.5f;
			}
			else if (honeyWet)
			{
				gravity = 0.1f;
				maxFallSpeed = 4f;
			}
			else
			{
				gravity = 0.2f;
				maxFallSpeed = 7f;
			}
		}
	}

	private void UpdateNPC_SoulDrainDebuff()
	{
		if (!soulDrain)
		{
			return;
		}
		int num = 1100;
		for (int i = 0; i < 255; i++)
		{
			if (Main.player[i].active && !Main.player[i].dead && (base.Center - Main.player[i].position).Length() < (float)num && Main.player[i].inventory[Main.player[i].selectedItem].type == 3006 && Main.player[i].itemAnimation > 0)
			{
				if (i == Main.myPlayer)
				{
					Main.player[i].soulDrain++;
				}
				if (Main.rand.Next(3) != 0)
				{
					Vector2 center = base.Center;
					center.X += (float)Main.rand.Next(-100, 100) * 0.05f;
					center.Y += (float)Main.rand.Next(-100, 100) * 0.05f;
					center += velocity;
					int num2 = Dust.NewDust(center, 1, 1, 235);
					Main.dust[num2].velocity *= 0f;
					Main.dust[num2].scale = (float)Main.rand.Next(70, 85) * 0.01f;
					Main.dust[num2].fadeIn = i + 1;
				}
			}
		}
	}

17:					else if (honeyWet)
22:							Main.dust[num2].velocity.Y -= 1f;
23:							Main.dust[num2].velocity.X *= 2.5f;
38:							Main.dust[num3].velocity.Y -= 4f;
39:							Main.dust[num3].velocity.X *= 2.5f;
55:						Main.dust[num4].velocity.Y -= 1.5f;
56:						Main.dust[num4].velocity.X *= 2.5f;
71:			velocity.X *= 0.5f;
75:				velocity.Y -= 8f;
89:								Main.dust[num5].velocity.Y -= 4f;
90:								Main.dust[num5].velocity.X *= 2.5f;
115:					else if (honeyWet)

```


---

## 🤖 Assistant · 2026-08-17T04:40:37.390Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Vanilla liquid physics for ALL NPCs: in water → gravity 0.2/maxFall 7; honey → gravity 0.1/maxFall 4; shimmer → 0.15/5.5. Ours: TownNPC uses fixed GRAVITY/MAX_FALL_SPEED always (no liquid damping). Enemy presumably uses npcLiquid.ts. TownNPC: `this.vy = Math.min(this.vy + GRAVITY, MAX_FALL_SPEED)` — no water/honey adjustments. **Deviation: town NPC in liquid doesn't slow-sink (honey/water gravity profile missing).**

Also vanilla buoyancy swim for town NPCs in water — AI_007 drowning jump handles escape. OK.

Hit flash: vanilla justHit → drawn with white flash? Let me check the draw: `npc.justHit` used in Main.DrawNPC? Search 24742 region quickly... Those are AI usages. For drawing, NPCs flash red/white on hit? Vanilla NPC hit flash: Main.DrawNPC uses `num2` = 1f + (npc.justHit ? ... )? Let me check "justHit" in Main.cs.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:40:38.319Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"justHit\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs\" | head; grep -n \"public Color GetAlpha\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"; sed -n '94860,94890p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"",
 "description": "Check NPC hit flash in draw"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:40:38.365Z

**📎 ToolResult**

```
94611:	public Color GetAlpha(Color newColor)
						num2 = 255;
					}
					if (num3 > 255)
					{
						num3 = 255;
					}
					if (num4 > 255)
					{
						num4 = 255;
					}
				}
			}
		}
		if (CurrentlyShimmerTransparent())
		{
			num2 = (byte)((float)num2 * (1f - shimmerTransparency));
			num3 = (byte)((float)num3 * (1f - shimmerTransparency));
			num4 = (byte)((float)num4 * (1f - shimmerTransparency));
			num5 = (byte)((float)num5 * (1f - shimmerTransparency));
		}
		if (num5 < 0)
		{
			num5 = 0;
		}
		if (num5 > 255)
		{
			num5 = 255;
		}
		return new Color(num2, num3, num4, num5);
	}

```


---

## 🤖 Assistant · 2026-08-17T04:40:45.271Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '94611,94660p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"",
 "description": "Read NPC.GetAlpha for hit flash"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:40:45.295Z

**📎 ToolResult**

```
	public Color GetAlpha(Color newColor)
	{
		if (IsABestiaryIconDummy)
		{
			newColor = Color.White;
		}
		float num = (float)(255 - alpha) / 255f;
		int num2 = (int)((float)(int)newColor.R * num);
		int num3 = (int)((float)(int)newColor.G * num);
		int num4 = (int)((float)(int)newColor.B * num);
		int num5 = newColor.A - alpha;
		if (type == 694)
		{
			if (ai[3] == 3f)
			{
				return newColor;
			}
			if (ai[3] == 4f)
			{
				float num6 = (float)frame.Y / 40f;
				float num7 = 17f;
				return Color.Lerp(newColor, Color.White, Math.Max(0f, Math.Min(1f, num6 / num7)));
			}
			return Color.White;
		}
		if (type == 1 && (ai[1] == 364f || ai[1] == 1104f || ai[1] == 365f || ai[1] == 1105f || ai[1] == 366f || ai[1] == 1106f))
		{
			return this.color;
		}
		if (type == 1 && ai[1] == 8f && Main.getGoodWorld)
		{
			return this.color;
		}
		if ((type == 147 || type == 184) && ai[1] == 1103f)
		{
			return new Color(200, 200, 200, 100);
		}
		if ((type == 147 || type == 184) && ai[1] == 593f)
		{
			return new Color(200, 200, 200, 100);
		}
		if (type == 402)
		{
			return new Color(255, 255, 255, 255);
		}
		if (type == 484)
		{
			return new Color(250, 250, 250, 200);
		}
		if (type >= 542 && type <= 545 && num2 + num3 + num4 > 10 && num2 + num3 + num4 >= 60)

```


---

## 🤖 Assistant · 2026-08-17T04:41:08.191Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
No special "hit flash" in GetAlpha for regular NPCs — the hit flash for NPCs in vanilla: when struck, `npc.color` briefly? Actually vanilla NPCs flash when hit via `HitEffect` + the immunity — hmm, actually vanilla enemies DO flash when hit: it's done via `npc.color = Color.White` lerp in draw — `DrawNPC` uses `npcColor = npc.GetColor`... There's `npc.color` blending where hit flash is... Let me not spend more: our Renderer does `if (n.iframes > 0 && n.iframes % 4 < 2) filter brightness(2.5)` — a white-flash approximation. Vanilla: NPC hit flash — in Main.DrawNPC there IS: `float num17 = 1f; if (npc.justHit) num17 = ...`? Let me grep "justHit" usage in draw code... The grep showed only NPC.cs usages. In Main.cs no justHit. So vanilla NPC hit feedback = CombatText + blood dust (HitEffect) — no white flash on the sprite itself. Our brightness flash = extra but harmless visually? It's a deviation from vanilla visuals (minor). Actually wait — vanilla enemies DO get a "flash" — the red blood particles + damage numbers. The sprite itself doesn't flash. Ours adds brightness(2.5) — non-vanilla visual. Minor.

Now, immunity frames: vanilla NPC immunity when struck by player: `immune[Main.myPlayer] = 10` typically (10 ticks). Ours: iframes=8 for TownNPC. What's vanilla for town NPC struck by projectile? Projectile.StrikeNPC: `npc.immune[owner] = 10`. So 8 vs 10 — minor deviation. Also hurt() applies `dmg - def*0.5` — vanilla StrikeNPC: damage = damage - defense*0.5 rounded via `Main.DamageVar`? For NPC: `num = damage - defense * 0.5f; if (num < 1) num = 1`. ✓ same formula. Knockback: vanilla applies full knockback with direction; ours `vx += kbx * 0.6` — 0.6 factor non-vanilla (vanilla: velocity.X = knockBack * direction... with `knockBack` resist). Minor.

Wait — one more important thing: vanilla townNPC hurt by ENEMIES uses GetHurtByOtherNPCs: damage = DamageVar(attacker.damage) with kb 6 → ours ✓ (envHurtUpdate). ✓ good.

Vanilla town NPC vs enemy contact is via GetHurtByOtherNPCs with immune[255]=30 ✓ ours npcVsCd=30 ✓.

Lava: vanilla Collision_LavaCollision: every 30 ticks (immune[255]=30) StrikeNPC(50, 0, 0) + sets OnFire 24/420. Ours: lavaCd=30, hurt(50) ✓ (OnFire noted as not implemented). ✓ mostly.

Now, let me check the remaining items:
- **被玩家推动**: no vanilla behavior → confirm and mark.
- **防御姿态（受击护头?）**: no vanilla town NPC cower frame — state 8 is standing. But there IS the "town NPC turns away"... Actually let me double check FindFrame state 8: falls into the group "ai[0] == 3f || 4f || 5f || 8f || 9f ..." which does NOT set frames → whatever frame they had? No — FindFrame: those ai states fall to... the branch `else if (velocity.X == 0f)` → frame 0. So standing frame. No cower animation. Mark "原版无护头姿态".
- **Defense posture**: vanilla town NPC defense = defDefense + dryadWard bonus; combat book +8 each. Our hurt(): def = base + books*8 ✓ (but no dryadWard — noted no载体, and no boss-progression defense chain — noted in comment as "另批" — actually vanilla applies downedBoss defense chain every tick to `defense` (e.g., hardMode +12). Our hurt only adds books*8, missing the progression defense chain (+2..+20). Let me verify: vanilla :53401-53531: defense += 2/3/6/8/12/20 per boss flag. Our hurt() doesn't include those. Deviation (defense numbers when hurt by traps/enemies). It's explicitly noted in our comment "防御链 :53401-53531(dryadWard+Boss 防,另批)" — registered as known gap.
- **Sleep**: none in vanilla ✓.
- **Party dancing**: vanilla state 6 (dance animation) triggered 1/1200 for party girl or all NPCs during party with AttackType==party girl's (need value: AttackType[208]? Let me check NPCID.Sets.AttackType[208] — Party Girl throws... she's type 208, attack type 0? Let me check quickly. Also 23 = cheer state (crowd cheering during party?) — the trigger for ai[0]=23? I didn't see it in AI_007 triggers... it's probably set by BirthdayParty elsewhere. Let me check BirthdayParty for NPC cheering (PartyIsUp → set ai[0]=23?).
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:41:09.852Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"ai\\[0\\] = 23f\\|ai\\[0\\] = 22f\\|ai\\[0\\] = 21f\\|ai\\[0\\] = 20f\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs\" 2>/dev/null | head; grep -rn \"ShouldNPCDance\\|NPCID.Sets.AttackType\\[208\\]\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | head -3",
 "description": "Find cheer/dance state triggers"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:41:09.905Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:30307:					this.ai[0] = 21f;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:34229:					this.ai[0] = 20f;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:55705:			else if (!NPCID.Sets.IsTownPet[type] && flag30 && ai[0] == 0f && velocity.Y == 0f && Main.rand.Next(1200) == 0 && (type == 208 || (BirthdayParty.PartyIsUp && NPCID.Sets.AttackType[type] == NPCID.Sets.AttackType[208])))

```


---

## 🤖 Assistant · 2026-08-17T04:41:13.321Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
States 20/21 are pet-specific (dogs etc.). 23 isn't triggered in NPC.cs — let me search BirthdayParty.cs for ai[0]=23 or cheering.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:41:14.459Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"ai\\[0\\] = 23\\|= 23f\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/BirthdayParty.cs\" 2>/dev/null | head; find ~/Project/GLM/SandboxWorld/Terarria1456 -name \"BirthdayParty.cs\"; grep -rn \"ai\\[0\\] = 23f\" ~/Project/GLM/SandboxWorld/Terarria1456/ --include=\"*.cs\" | head -5",
 "description": "Find ai0=23 trigger source"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:41:14.599Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Events/BirthdayParty.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Animations/Actions.cs:270:					obj.ai[0] = 23f;

```


---

## 🤖 Assistant · 2026-08-17T04:41:19.084Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"ai\\[0\\]\\|Party\\|cheer\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Animations/Actions.cs\" | sed -n '1,15p'; sed -n '255,285p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Animations/Actions.cs\"",
 "description": "Check Actions.cs ai0=23 context"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:41:19.131Z

**📎 ToolResult**

```
270:					obj.ai[0] = 23f;
278:				if (obj.ai[0] == 23f)
281:					obj.ai[0] = 0f;
471:				obj.ai[0] = 21f;
531:					obj.ai[0] = 0f;
534:						obj.ai[0] = 1001f;
576:		public class PartyHard : INPCAction, IAnimationSegmentAction<NPC>
582:				obj.ForcePartyHatOn = true;
				_delay = delay;
			}

			public void ApplyTo(NPC obj, float localTimeForObj)
			{
				if (!(localTimeForObj < _delay))
				{
					float num = localTimeForObj - _delay;
					if (num > (float)_duration)
					{
						FixNPCIfWasHoldingItem(obj);
						return;
					}
					obj.velocity = Vector2.Zero;
					obj.frameCounter = num;
					obj.ai[0] = 23f;
					obj.ai[1] = (float)_duration - num;
					obj.ai[2] = _itemIdToShow;
				}
			}

			private void FixNPCIfWasHoldingItem(NPC obj)
			{
				if (obj.ai[0] == 23f)
				{
					obj.frameCounter = 0.0;
					obj.ai[0] = 0f;
					obj.ai[1] = 0f;
					obj.ai[2] = 0f;
				}
			}

```


---

## 🤖 Assistant · 2026-08-17T04:41:23.231Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
ai[0]=23 is a cutscene animation action (PartyHard — the credits/ending animation sequence "PartyHard" cinematic). Not daily behavior — skip.

Now the party girl AttackType — what's AttackType[208]? Let me check NPCID.cs Sets.AttackType init values for 208 (Party Girl). And confirm the dance trigger applies to which NPCs during party.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:41:24.327Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"AttackType\\[208\\]\\|AttackType\\[228\\]\\|AttackType\\[229\\]\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ID/NPCID.cs 2>/dev/null | head; find ~/Project/GLM/SandboxWorld/Terarria1456 -name \"NPCID.cs\"",
 "description": "Find NPCID.cs AttackType for party girl"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:41:24.385Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/NPCID.cs

```


---

## 🤖 Assistant · 2026-08-17T04:41:27.362Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"AttackType\\[208\\]\\|AttackType\\[\\] AttackType\\|AttackType = new\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/NPCID.cs | head -5; grep -n \"AttackType\\[208\\]\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/NPCID.cs",
 "description": "Find AttackType array init for 208"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:41:27.421Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-17T04:41:31.734Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"AttackType\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/NPCID.cs | head -8",
 "description": "Find AttackType in NPCID.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:41:31.776Z

**📎 ToolResult**

```
4849:		public static int[] AttackType = Factory.CreateIntSet(-1, 38, 0, 17, 0, 107, 0, 19, 1, 22, 1, 124, 0, 228, 1, 178, 1, 18, 0, 229, 1, 209, 1, 54, 2, 108, 2, 160, 2, 20, 2, 369, 0, 453, 0, 368, 1, 207, 3, 227, 1, 208, 0, 142, 0, 441, 3, 353, 3, 633, 0, 550, 0, 588, 0, 663, 2, 638, -1, 637, -1, 656, -1, 670, -1, 678, -1, 679, -1, 680, -1, 681, -1, 682, -1, 683, -1, 684, -1);

```


---

## 🤖 Assistant · 2026-08-17T04:41:39.423Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
AttackType[208] = 0. So the dance trigger at :55705: `type == 208 || (PartyIsUp && AttackType[type] == AttackType[208])` — AttackType==0 NPCs (guide 38? no wait 38=0? yes merchant 17=0? no — 17 is 0? The list: 38→0, 17→0, 107→0, 19→1, ...). So during party, ALL town NPCs with AttackType 0 (most NPCs: merchant 17? no — 17→0 yes, guide 38→0, dryad? 20→2...). Hmm: AttackType values: 0=shooting projectiles (bow-like), 1=thrown/aimed flat, 2=magic, 3=melee swing. Party girl 208→0. So during party, NPCs with AttackType 0 near a player dance (1/1200 per tick).

So vanilla party behavior: NPCs with bow-type attack dance when player within 150px + LOS, 300 ticks, using dance frames (num58-5/num58-4) with music-note dust (139-143). Plus party hats (we have ✓) + FreeCake dialogue indicator. Shopping discount during party: **none** in vanilla (no price modifier). Let me confirm there's no party price discount — grep "PartyIsUp" in Player/ShoppingSettings price calc.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:41:40.751Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"PartyIsUp\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ShoppingSettings.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Chest.cs 2>/dev/null | head; grep -rn \"partyDiscount\\|PartyDiscount\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ --include=\"*.cs\" | head -3",
 "description": "Check party shopping discount in vanilla"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:41:40.805Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Chest.cs:1400:			if (BirthdayParty.PartyIsUp)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Chest.cs:1942:			if (BirthdayParty.PartyIsUp)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Chest.cs:2318:			if (BirthdayParty.PartyIsUp)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Chest.cs:3354:			if (BirthdayParty.PartyIsUp)

```


---

## 🤖 Assistant · 2026-08-17T04:41:43.518Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1395,1412p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Chest.cs\"",
 "description": "Check party effect in shops"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:41:43.553Z

**📎 ToolResult**

```
			}
			if (!Main.dayTime)
			{
				array[num++].SetDefaults(282);
			}
			if (BirthdayParty.PartyIsUp)
			{
				array[num++].SetDefaults(5643);
			}
			if (NPC.downedBoss3)
			{
				array[num].SetDefaults(346);
				num++;
			}
			if (Main.hardMode)
			{
				array[num].SetDefaults(488);
				num++;

```


---

## 🤖 Assistant · 2026-08-17T04:42:03.963Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Party during shops = extra item stock (5643 party present / confetti etc.), NOT a price discount. Confirmed: **原版无派对购物折扣** — party only adds stock + hats + dance + cake. Good, that resolves item 6.

Now let me verify a few remaining things in our code:
1. Do we have the party stock additions (5643 etc.) in shopStockFor? The SHOPSTOCK is data-driven from extraction — party items may be missed (like the moonPhase conds). Let me grep for 5643 in our shop handling.
2. Check our EmoteBubble / speech indicator (homeless text icon).
3. Check our night-walk behavior: does the NPC actually walk home at night (we have it) — and vanilla: at night housed NPCs go to restSpot via state 1 with direction toward floorX (only when flag). ✓ ours approximates.
4. Check danger-detect range defaults and whether our pickSideTarget excludes friendly... fine.

Also for the audit item 3 "避水/避崖": vanilla drowning jump + avoidFalling — both missing in ours. Confirmed above.

Item 3 "跳跃越障": ours vy=-6 single-tier + jump spam (no turn-around when ceiling blocked). Vanilla 3-tier + turn.

Let me now check where our TownNPC day-wander speed constants are vs vanilla (0.06/0.8 vs 0.07/1.0) — confirmed in fixedUpdate lines 777-778.

Also vanilla: `if (wet && velocity.Y < 0) velocity.Y *= 1.2` (jump out of water stronger) — ours none.

Also vanilla idle random turn: `Main.rand.Next(80)==0 → localAI[3]=200, direction*=-1` (only when within ±25 of home). Ours: wanderT expiry randomizes facing with 35% stand. Different but functional approximation.

Now — very important vanilla behavior I should double check we have or not: **NPC names / dialogue when talked to** — task item 4: "靠近玩家主动说话的冷却/概率、名字替换、不同 NPC 特殊对话条件". "主动说话" for vanilla town NPC near player: the state 7 (face player 220 ticks, 1/1200) + emote 112 — not actual speech. The actual proactive SPEECH (bubble text) is the ConditionalDialogue (FreeCake) + homeless text. Also there's the classic "townNPC chat" random lines when you talk — handled by our dialog UI presumably. Let me check our talkToNearbyNpc for chat text with name replacement.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:42:04.615Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"talkToNearbyNpc\\|GetChat\\|chatText\\|npcChat\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | head -20",
 "description": "Find our NPC dialogue handling"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:42:04.652Z

**📎 ToolResult**

```
5533:      } else if (this.talkToNearbyNpc(tx, ty)) {
12965:  private talkToNearbyNpc(ctX: number, ctY: number): boolean {
12979:  // ================= NPC 对话系统(SetTalkNPC + NPC.GetChat NPC.cs:94974 1:1) =================
13031:    // 守卫老人:夜晚出现「诅咒」(白天只闲聊,原版 GetChat 语义)
13324:  /** 台词 = NPC.GetChat(NPC.cs:94974+) type 17/18/22/37/19/20/38 分支 1:1。
13335:    // GetChat 在场旗标(cs:94996-95046):其他城镇 NPC 是否在场
13342:    // FreeCakeDialogue（ConditionalDialogue.cs:42-61）：原版 GetChat 第一句即
14447:   *  打开详情浮层——报告逐条 + 价格倍率（原版把 HappinessReport 写进 npcChatText） */

```


---

## 🤖 Assistant · 2026-08-17T04:42:07.840Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '12965,13060p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts; sed -n '13324,13420p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Read our talk/dialogue system"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:42:07.891Z

**📎 ToolResult**

```
  private talkToNearbyNpc(ctX: number, ctY: number): boolean {
    const p = this.player;
    for (const n of this.entities.npcs) {
      const npc = n as TownNPC;
      if (Math.hypot(npc.cx - p.cx, npc.cy - p.cy) > TILE * 3.5) continue;
      const mx = (ctX + 0.5) * TILE, my = (ctY + 0.5) * TILE;
      if (mx < npc.x - 8 || mx > npc.x + npc.w + 8 || my < npc.y - 8 || my > npc.y + npc.h + 8) continue;
      if (npc.bound) { this.freeBoundNpc(npc); return true; } // 救援 NPC：右键直接解救
      this.openNpcDialog(npc);
      return true;
    }
    return false;
  }

  // ================= NPC 对话系统(SetTalkNPC + NPC.GetChat NPC.cs:94974 1:1) =================

  private dialogNpc: TownNPC | null = null;

  // ---- 下落沙族(原版 SandBallFalling 系,AI_010) ----
  /** 会下落的 tile(原版 53 沙/112 黑檀沙/116 珍珠沙/234 猩红沙/123 淤泥/224 雪泥) */
  private static readonly FALLING_TILES = new Set<number>(
    ['sand', 'v_112_ebonsand_block', 'v_116_pearlsand_block', 'v_234_crimsand_block', 'silt', 'v_224_slush_block']
      .map((k) => TILE_BY_KEY[k])
      .filter((v): v is number => v !== undefined),
  );
  /** 待检查的下落候选格(监听器入队,fixedUpdate 消费;级联自然发生:
   *  沙转投射物时的 setTile 会再次触发监听器 → 上方沙继续入队) */
  private sandQueue: Array<[number, number]> = [];

  /** 打开对话框:台词/按钮按 NPC 类型生成,UI 经 onNpcDialog 渲染 */
  private openNpcDialog(npc: TownNPC) {
    this.dialogNpc = npc;
    // 图鉴聊天解锁（NPC.cs:45223 SetTalkNPC→RegisterChatStartWith：与城镇 NPC 对话即记）
    this.world.bestiary.registerChat(npc.vanillaId);
    this.achCheckBestiary();
    // 快乐度快照（Player.SetTalkNPC Player.cs:4189-4193：GetShoppingSettings 一次算好，
    // currentShoppingSettings 供商店价格/心情报告/成就共用）
    this.dialogHappiness = this.computeShopHappiness(npc);
    // 成就：与最大快乐度 NPC 对话（Player.cs:4195-4197 PriceAdjustment<=0.82 → event 20）
    if (this.dialogHappiness.priceMul <= 0.82) {
      this.achievements.handleSpecialEvent(20, {
        statLifeMax: this.player.maxHp, statManaMax: this.player.maxMana,
      });
    }
    npc.talking = true;  // 原版 AI_007:53721 对话中站定面向玩家
    npc.talkCooldown = 30;
    this.sfx.play('menuOpen'); // 对话面板打开音（原版 UI 面板开合语义 id 10/11）
    const typeName = Lang.npcName(npc.vanillaId) ?? npc.npcKey;
    // FullName 语义（NPC.FullName:6657 + Game.NPCTitle，zh "{1}{0}"=类型名+个人名）
    const name = npc.givenName ? Lang.text('Game.NPCTitle', npc.givenName, typeName) : typeName;
    this.cb.onNpcDialog?.(name, this.formatDialogTags(this.townNpcChat(npc)),
      this.npcDialogButtons(npc), portraitUrl(npc.vanillaId));
  }

  /** 对话框按钮组（NPCInteractions.cs 各 NPCInteraction 注册序）：商店/治疗/收税/
   *  重铸/诅咒/渔夫任务（AnglerQuest :134-152，标签 Lang.inter[64]「任务」） */
  private npcDialogButtons(npc: TownNPC): Array<{ id: NpcButtonId; label: string }> {
    const buttons: Array<{ id: NpcButtonId; label: string }> = [];
    // 商店按钮(NPCInteractions.cs:489-513 Shop 注册表覆盖的全部 NPC)
    if (Game.SHOPSTOCK[String(npc.vanillaId)]) buttons.push({ id: 'shop', label: Lang.inter(28) });
    if (npc.npcKey === 'nurse') buttons.push({ id: 'heal', label: Lang.inter(54) });       // 治疗
    // 树妖：世界状态（NPCInteractions.cs:124-129 Register Status——注册序在商店后）
    if (npc.npcKey === 'dryad') buttons.push({ id: 'status', label: Lang.text('Mods.SandboxWorld.NPC.WorldStatus') });
    if (npc.npcKey === 'tax_collector') buttons.push({ id: 'collect', label: Lang.inter(89) }); // 收集税款
    // 哥布林工匠：重铸（NPCChatText_TinkererReforge Main.cs:39431）
    if (npc.npcKey === 'goblin_tinkerer') buttons.push({ id: 'reforge', label: Lang.inter(19) });
    // 守卫老人:夜晚出现「诅咒」(白天只闲聊,原版 GetChat 语义)
    if (npc.npcKey === 'old_man' && !this.world.clock.isDay && !this.world.flags.hardMode) {
      buttons.push({ id: 'curse', label: Lang.inter(50) });                                 // 诅咒
    }
    // 渔夫：任务交付（NPCInteractions.AnglerQuest.GetText = Lang.inter[64]）
    if (npc.vanillaId === 369) buttons.push({ id: 'quest', label: Lang.inter(64) });
    // 快乐度（ReportHappiness，NPCInteractions.cs:289-314；注册序在全部商店/其它交互之后）：
    // 无家 NPC 换成 RequestHome 不显示（NPC.CanShowHomelessText NPC.cs:96048-96060），
    // 旅行商/骷髅商/老人 HappinessReport 为空也不显示
    if (!this.canShowHomelessText(npc) && (this.dialogHappiness?.report.length ?? 0) > 0) {
      buttons.push({ id: 'happiness', label: Lang.text('UI.NPCCheckHappiness') });
    }
    buttons.push({ id: 'close', label: Lang.inter(52) });                                   // 关闭
    return buttons;
  }

  /** NPC.CanShowHomelessText（NPC.cs:96048-96060）：无家且非 37/368/453 → true
   *  （此时 ReportHappiness 让位 RequestHome，快乐度按钮不显示） */
  private canShowHomelessText(npc: TownNPC): boolean {
    return !npc.home && npc.vanillaId !== 37 && npc.vanillaId !== 368 && npc.vanillaId !== 453;
  }

  /** 已开对话框的台词区重绘（交付结算后替换为 AnglerQuestChat 文案，不重开面板） */
  private refreshNpcDialog(npc: TownNPC, chat: string): void {
    const typeName = Lang.npcName(npc.vanillaId) ?? npc.npcKey;
    const name = npc.givenName ? Lang.text('Game.NPCTitle', npc.givenName, typeName) : typeName;
    this.cb.onNpcDialog?.(name, this.formatDialogTags(chat),
      this.npcDialogButtons(npc), portraitUrl(npc.vanillaId));
  }

  /** 台词 = NPC.GetChat(NPC.cs:94974+) type 17/18/22/37/19/20/38 分支 1:1。
   *  环境事件文案（HasSpecialEventText 墓园/派对/雨/风日/风暴 + 向导日食/史莱姆雨/
   *  灯笼夜 Lantern1/2）已接；DD2 段跳过，走常规池。
   *  曾把未覆盖类型全部落到守卫老人自建文案池——向导会说出"解除诅咒"台词,已修 */
  private townNpcChat(npc: TownNPC): string {
    const p = this.player;
    const w = this.world;
    const dialog = (n: number) => Lang.text(`LegacyDialog.${n}`);
    const rN = (n: number) => Math.floor(Math.random() * n);
    const r3 = () => rN(3);
    const r2 = () => (Math.random() < 0.5 ? 0 : 1);
    // GetChat 在场旗标(cs:94996-95046):其他城镇 NPC 是否在场
    const present = (id: number) =>
      this.entities.npcs.some((n) => n instanceof TownNPC && !n.dead && n.vanillaId === id);
    // downedBoss1/2/3(cs 全局):EoC / 世吞|克脑 / 骷髅王
    const boss1 = !!(w.flags['downed_4'] || w.flags.downedEyeOfCthulhu);
    const boss2 = !!(w.flags['downed_13'] || w.flags['downed_266']);
    const boss3 = !!(w.flags['downed_35'] || w.flags.downedSkeletron);
    // FreeCakeDialogue（ConditionalDialogue.cs:42-61）：原版 GetChat 第一句即
    // nextDialogue 先行（NPC.cs:94974-94978，nextDialogue 每帧刷新于 :91579）——
    // 蛋糕台词压过包括事件文案在内的一切分支。仅注册于派对女孩 208（:115）：
    // 生日派对开张（NPC.freeCake=true，BirthdayParty.cs:106）后首次对话 →
    // PartyGirlSpecialText.Cake1-3 + 直接入包切片蛋糕 3750（QuickSpawnItem
    // EntitySource_Gift）+ 清旗（联机 msg51 广播位不适用单机）。
    // 曾排在 npcSpecialEventText 之后=优先级反了（派对+血月同存时先出血月文案）
    if (npc.vanillaId === 208 && this.freeCake) {
      this.freeCake = false;
      const cake = VI(3750);
      if (cake && ITEM_BY_KEY[cake] !== undefined) this.player.inv.add(ITEM_BY_KEY[cake], 1);
      return Lang.specialText('PartyGirlSpecialText.Cake')
        ?? Lang.text('PartyGirlSpecialText.Cake1');
    }
    // HasSpecialEventText（cs:96081-96105，各类型分支首位）：哥布林/巫师/机械师
    // 的流浪态优先于事件文案（cs:95286/95336/95429 homeless 先行），其余类型事件优先
    const HOMELESS_FIRST = new Set([107, 108, 124]);
    if (!(HOMELESS_FIRST.has(npc.vanillaId) && !npc.home)) {
      const special = this.npcSpecialEventText(npc);
      if (special) return special;
    }
    if (npc.vanillaId === 17) {
      // 商人(NPC.cs:95077-95105)
      if (!boss1 && r3() === 0) {
        if (p.maxHp < 200) return dialog(1);
        if (p.defense > 10) return dialog(3);
        return dialog(2);
      }
      if (w.clock.isDay) {
        const f = (w.clock.timeOfDay - 0.25) / 0.5; // 昼内进度 0-1(原版 Main.time/43200)
        if (f < 16200 / 43200) return dialog(4 + r3());   // 清晨 4-6
        if (f > 37800 / 43200) return dialog(7 + r3());   // 傍晚 7-9
        return dialog(10 + r3());                          // 白昼 10-12
      }
      const nf = (((w.clock.timeOfDay - Clock.DUSK) % 1) + 1) % 1 / 0.375; // 夜内进度 0-1（32400t 窗口）
      if (nf < 9720 / 43200) return dialog(r2() ? 19 : 18);
      if (nf > 22680 / 43200) return dialog(r2() ? 21 : 20);
      return dialog(22 + r3());                            // 深夜 22-24
    }
    if (npc.vanillaId === 18) {
      // 护士(NPC.cs:95104-95190):三成概率提醒老人(!downedBoss3);按血量分档
      if (r3() === 0 && !boss3) return dialog(32);
      const ratio = p.hp / p.maxHp;
      if (ratio < 0.33) return dialog(36 + Math.floor(Math.random() * 5)); // 36-40
      if (ratio < 0.66) return dialog(41 + Math.floor(Math.random() * 7)); // 41-47
      return dialog(48 + Math.floor(Math.random() * 4));                   // 48-51
    }
    if (npc.vanillaId === 22) {
      // 向导(cs:95473-95489)：血月 170-172 → 灯笼夜 Lantern1/2（cs:95480：
      // LanternsUp && !downedMoonlord → Lantern1 / LanternsUp && downedMoonlord →
      // Lantern2）→ 日食 Eclipse → 史莱姆雨 SlimeRain → 夜晚 173 → 白天
      // hardMode Chatter 池（8 选 1）→ 白天 174-176
      if (w.clock.bloodMoon) return dialog(170 + r3());
      if (LanternNight.lanternsUp) {
        return Lang.text(w.flags['downed_398'] ? 'GuideSpecialText.Lantern2' : 'GuideSpecialText.Lantern1');
      }
      if (w.clock.eclipse) return Lang.text('GuideSpecialText.Eclipse');
      if (w.weather.slimeRain) return Lang.text('GuideSpecialText.SlimeRain');
      if (!w.clock.isDay) return dialog(173);
      // hardMode Chatter 池（原版双段：Chatter_1 需税务官在场 / Chatter_2 任意，各 1/8
      // ——此处合并为池随机 1/8）
      if (w.flags.hardMode && Math.random() < 1 / 8) {
        return Lang.chatter('GuideChatter') ?? dialog(174 + r3());
      }
      return dialog(174 + r3());
    }
    if (npc.vanillaId === 37) {
      // 守卫老人(cs:95224-95240):白天 82-84;夜晚(生命<300 或防御<10)85-88,否则 89-92
      if (!w.clock.isDay) {
        return dialog(p.maxHp < 300 || p.defense < 10 ? 85 + Math.floor(Math.random() * 4) : 89 + Math.floor(Math.random() * 4));
      }
      return dialog(82 + r3());
    }
    if (npc.vanillaId === 19) {
      // 军火商(cs:95195-95203):向导在场+已败骷髅王+非困难 58;护士/树妖/爆破手在场随机互cue;
      // 常规池 66-68(血月 64/65 未实现)
      if (present(22) && boss3 && !w.flags.hardMode) return dialog(58);
      if (present(18) && Math.floor(Math.random() * 5) === 0) return dialog(59);
      if (present(18) && Math.floor(Math.random() * 5) === 0) return dialog(60);

```


---

## 🤖 Assistant · 2026-08-17T04:42:17.942Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Our dialogue system is well-implemented (GetChat 1:1, FreeCake, special events, name replacement via Game.NPCTitle). ✓ Good.

Now let me quickly verify remaining bits:

1. Our EmoteBubble module — check that it exists and emotes drawn. And speech indicator icon (notification icon) for homeless text/pending dialogue — probably missing. Check Renderer for notification.

2. Check our "talkCooldown" usage — set 30 but is it consumed? grep talkCooldown.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:42:18.835Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"talkCooldown\" ~/Project/GLM/SandboxWorld/game/src/ --include=\"*.ts\"; echo ---; grep -n \"DrawNotificationIcon\\|notification\" ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts | head -5",
 "description": "Check talkCooldown consumption and notification icon"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:42:18.890Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:13010:    npc.talkCooldown = 30;
~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts:357:  talkCooldown = 0;
---

```


---

## 🤖 Assistant · 2026-08-17T04:42:29.486Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
- talkCooldown: dead field (set, never consumed) — vanilla doesn't have such cooldown either (dialog re-open is instant). Fine — vanilla: talking to NPC again re-rolls chat immediately. OK aligned effectively.
- No notification icon (talk indicator) over homeless NPCs / pending dialogue — vanilla draws it (Main.cs:45484 + Utils.DrawNotificationIcon, homeless text within 105px). Minor visual gap. Actually — item 4 relevance: "无家可归" indicator icon missing.

Now let me verify our EmoteBubble implementation quickly and confirm emote pool. Then check the door-close bug possibility (vanilla closes door when >2 tiles away — ours closes when >2 tiles... ours uses `Math.abs(tx - doorX) > 2` on x, y >4 — vanilla: x > doorX+2 || x < doorX-2 → close; give-up x>±4 or y>±4. Ours: close when |dx|>2 or |dy|>4?? Wait ours: `if (Math.abs(tx - this.doorX) > 2 || Math.abs(ty - this.doorY) > 4)` then close if |dx|<=4 && |dy|<=4. Vanilla: close when dx>2 or dx<-2 (X only); abandon when |dx|>4 OR |dy|>4. Ours adds |dy|>4 as a close trigger — slight deviation (vanilla only closes based on X distance; y>4 = give up without closing). Minor.

Hmm — actually ours has a subtle bug vs vanilla: vanilla closes door only on X displacement >2; y displacement alone (falling) doesn't trigger closing (it triggers give-up at ±4). Ours triggers close when ty differs >4 (then since dy<=4 fails, it just sets closeDoor=false without closing — actually if |ty-doorY|>4, first condition true, then the inner `if (|dx|<=4 && |dy|<=4)` — |dy|>4 fails → no close, closeDoor=false → give up. So effectively same-ish. OK minor.

Now check EmoteBubble file briefly.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:42:30.097Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "head -80 ~/Project/GLM/SandboxWorld/game/src/render/EmoteBubble.ts; grep -c \"\" ~/Project/GLM/SandboxWorld/game/src/render/EmoteBubble.ts",
 "description": "Read our EmoteBubble module"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:42:30.138Z

**📎 ToolResult**

```
// 原版 EmoteBubble（Terraria.GameContent.UI/EmoteBubble.cs）移植——NPC 头顶表情气泡。
// 素材 = Extra_48.png（272×1092，8 列 × 39 行，格 34×28：行0 列0/1 = 气泡框闭合/张开，
// 行 1+emote/4、列 emote*2%8+frame = 表情图标，每表情 2 帧动画、8 tick/帧）。
// 锚定（GetPosition Entity 分支）：位置 = 头顶 + (-dir*w*0.75, 2)，origin 底中，
// dir≠-1 时水平翻转（气泡尾巴指向 NPC）。
export interface EmoteBubbleInstance {
  npc: { cx: number; y: number; w: number; facing: number };
  emote: number;
  lifeTime: number;
  lifeStart: number;
  frame: number;
  frameCounter: number;
}

const bubbles: EmoteBubbleInstance[] = [];

/** 调试/探针：当前活跃气泡数 */
export function emoteCount(): number { return bubbles.length; }

// 探针句柄：挂在 window 上保证与 Game/Renderer 同一模块实例（HMR ?t= 分叉时
// 动态 import 会拿到另一份模块实例，气泡数恒 0 的假象来源）
if (typeof window !== 'undefined') {
  (window as unknown as { __swEmotes?: unknown }).__swEmotes = { spawn: spawnEmote, count: emoteCount, draw: drawEmotes };
}

/** NewBubble(emoticon, anchor, time)：默认存活 180 tick */
export function spawnEmote(npc: EmoteBubbleInstance['npc'], emote: number, time = 180): void {
  if (bubbles.some((b) => b.npc === npc)) return; // 同一实体一次一个（原版 byID 近似）
  bubbles.push({ npc, emote, lifeTime: time, lifeStart: time, frame: 0, frameCounter: 0 });
}

/** Update()（EmoteBubble.cs:177）：--life；每 8 tick 图标帧 0↔1 */
export function tickEmotes(): void {
  for (let i = bubbles.length - 1; i >= 0; i--) {
    const b = bubbles[i];
    if (--b.lifeTime <= 0) { bubbles.splice(i, 1); continue; }
    if (++b.frameCounter >= 8) {
      b.frameCounter = 0;
      if (++b.frame >= 2) b.frame = 0;
    }
  }
}

/** 绘制（Draw :203-231 1:1）。img = Extra_48 表。
 *  ※在渲染器的世界变换内调用（ctx 已 scale(z)/translate(-cam)）——直接用世界坐标锚定 */
export function drawEmotes(ctx: CanvasRenderingContext2D, img: ImageBitmap | HTMLImageElement): void {
  if (!img || !(img.width > 0) || img.width === 0) return;
  const CW = 34, CH = 28; // 272/8=34, 1092/39=28
  for (const b of bubbles) {
    const opening = b.lifeTime < 6 || b.lifeStart - b.lifeTime < 6; // flag：开合动画 → 行0 列0
    // 位置（GetPosition Entity 分支）：头顶 + (-dir*w*0.75, 2)px；origin = (格宽/2, 格高)
    const ax = b.npc.cx - b.npc.facing * b.npc.w * 0.75;
    const ay = b.npc.y + 2;
    const flip = b.npc.facing !== -1; // dir≠-1 → 水平翻转
    ctx.save();
    ctx.translate(ax, ay);
    if (flip) ctx.scale(-1, 1);
    // 气泡框：行 0，列 opening?0:1
    ctx.drawImage(img, (opening ? 0 : 1) * CW, 0, CW, CH, -CW / 2, -CH, CW, CH);
    if (!opening) {
      // 表情图标：列 = emote*2%8 + frame，行 = 1 + emote/4
      ctx.drawImage(img, (b.emote * 2 % 8 + b.frame) * CW, (1 + Math.floor(b.emote / 4)) * CH, CW, CH, -CW / 2, -CH, CW, CH);
    }
    ctx.restore();
  }
}
66

```


---

## 🤖 Assistant · 2026-08-17T04:42:54.239Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
EmoteBubble module is fine for rendering, but the *drivers* are simplified (Game.tickNpcEmotes every 600 ticks vs vanilla per-NPC per-tick rolls).

Now let me quantify the vanilla chat triggers precisely for the report:
- Pair chat 3/4: `Main.rand.Next(300) == 0` per tick per NPC (idle standing, on ground, not talking-to-player, no danger, not wet... flag30 = ai[0]<2 && !flag16 && !wet). Partner: CanBeTalkedTo, 20<dist<100 px, LOS, partner not walking-with-door/ai[1]>200/ai[0]>1/wet. Duration: 420×1..3 (50%) or 420×1..4 (50%).
- Pair chat 16/17: 1/1800, with localAI[2]=rand(4) random emote theme; both NPCs face each other; partner same checks (IsTownPet excluded).
- Face player 7: 1/1200, player within 150px, LOS, 220 ticks, emote 112 at tick 16; NPC turns to face player.
- Party dance 6: 1/1200 (party girl always; others during party with AttackType 0), player within 150px, LOS, 300 ticks; dance frames + music dust.
- Bartender 18: 1/600, 300 ticks (frame = npcFrameCount-2), faces player.
- Random emote state 2: 1/1800, ai[1]=45×rand(1,2) → 45 ticks... Actually `45 * Main.rand.Next(1, 2)` = 45×1 = 45 always (Next(1,2)=1). Hmm funny — 1.4.5.6 fixed range makes it constant 45. In 1.4.4 it was Next(1,4)? whatever — 45 ticks. What does state 2 do? FindFrame: state 2 → "else if (ai[0] == 2f || ai[0] == 11f)" in AI (velocity decay, rand(60)==0 → turn while localAI[3]... wait that's AI side). FindFrame for state 2: at 69620-69640 area I saw `frameCounter >= 100 && rand(20)==0 → frame 0` and `frame.Y/num==0 && frameCounter>=20 → frame num58-1 + emote 89`. Which states do those frames belong to? That was within some ai state... possibly state 2 (the "sit and think" state? no). Actually those lines belong to `else if (velocity.X == 0f)` — the default idle branch (ai[0]=0): standing NPCs occasionally play a special frame (num58-1) with emote 89 (hmm — 89 might be "yawn/sleepy"?). Wait — that means: idle standing town NPCs randomly (frameCounter>=20, one-time) show frame num58-1 + emote 89?? Let me re-read that block:

```
else if (frame.Y / num == 0 && frameCounter >= 20.0)
{
    frame.Y = num * (num58 - 1);
    frameCounter = 0.0;
    EmoteBubble.NewBubble(89, new WorldUIAnchor(this), 90);
}
else if (frame.Y != 0 && frame.Y != num * (num58 - 1))
{
    frame.Y = 0;
    frameCounter = 0.0;
}
```

Hmm, this is inside which state? Let me look at what precedes — at 69600-69640. It follows the ai[0]==6 dance branch and ai[0]==7/19 branch. So this must be inside ai[0]==7/19 branch? No wait — the sed output showed: dance (6), then 7/19 with emote 112 and frames 0/(num58-2) alternating (num72), then `frame.Y = num*num72; if frameCounter>=220 → 0`. Then `else if (ai[0] == 9f)` etc. Then BEFORE the 69620 block I saw "frameCounter >= 100.0 && Main.rand.Next(20) == 0 → frame 0" — that was in the ai[0]==7/19 branch too? The exact sed at 69620-69700 started mid-branch. The sequence was: [69600-69620: state 7/19 tail with num72 alternation], then "else if (frame.Y/num == 0 && frameCounter >= 20) { frame num58-1; emote 89 }" — hmm this looks like it's still within the state 7/19 else-if chain as a fallback? No — it must be a separate branch for ai[0]==2/11 or the default idle.

Actually — I realize the fragment "frameCounter >= 100 && rand(20)==0 → frame 0" + "frame.Y/num==0 && frameCounter>=20 → num58-1 + emote 89" — I bet this is the ai[0]==2 (idle emote) branch: NPC stands, shows "bored" frame with emote. Whatever — fine-grained frame detail. The point for the audit: our NPCs have no idle-animation frames and no emote-89 idle bubble.

Emote 89: in EmoteBubble list, 89 = "sleep"? EmoteID 89 = EmoteID.Sleep? There's "Sleep" at... The pool our Game uses [25(biome),90(item),100(alarm?),87(?),89]. Vanilla idle/party uses 36/37/38 (chat), 89, 112, 3. Let me get EmoteID meanings quickly for accuracy — check EmoteID.cs.
````

</details>


---

## 🤖 Assistant · 2026-08-17T04:42:54.491Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"= 36\\|= 37\\|= 38\\|= 89\\|= 112\\|= 3,\\|= 60\\|= 87\\|= 90\\|= 100\\|= 25,\" ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria.GameContent.UI/EmoteID.cs 2>/dev/null | head -20; find ~/Project/GLM/SandboxWorld/Terarria1456 -name \"EmoteID.cs\"",
 "description": "Get EmoteID meanings"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:42:54.549Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI/EmoteID.cs

```


---

## 🤖 Assistant · 2026-08-17T04:42:58.125Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -nE \"\t(const int|.*) (Item|Question|Heart|Sleep|MusicNotes|Talk|Alarm|Emote|Biome|Grass|Fire|Wind|Emotion|Idea|Love|Anger|Happy|Sad) = [0-9]+\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI/EmoteID.cs | head -30",
 "description": "Read EmoteID constants"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:42:58.186Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-17T04:43:01.164Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"= 36;\\|= 37;\\|= 38;\\|= 89;\\|= 112;\\|= 87;\\|= 90;\\|= 100;\\|= 25;\\|= 60;\\|= 3;\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI/EmoteID.cs",
 "description": "Find emote id name mappings"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:43:01.217Z

**📎 ToolResult**

```
17:	public const int RPSScissors = 36;
19:	public const int RPSRock = 37;
21:	public const int RPSPaper = 38;
77:	public const int ItemPickaxe = 90;
157:	public const int BossMartianship = 60;
169:	public const int EmotionAlert = 3;
177:	public const int EmoteConfused = 87;
181:	public const int EmoteSleep = 89;
205:	public const int MiscFire = 100;
213:	public const int BiomeCrimson = 25;
251:	public const int TownSanta = 112;

```


---

## 🤖 Assistant · 2026-08-17T04:43:14.881Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now it makes sense:
- Pair chat 16/17: NPCs play **rock-paper-scissors** (36=scissors, 37=rock, 38=paper) with the mirrored pairing logic (rock vs paper etc.)! That's the famous town NPC RPS mini-interaction.
- ai[0]==2 idle: emote 89 = Sleep (bored/sleepy bubble) + frame num58-1.
- ai[0]==7 face player: emote 112 = TownSanta?? Hmm no wait — 112 TownSanta. Hmm, but the code at 69690 area: `frameCounter == 16.0 → EmoteBubble.NewBubbleNPC(..., 112)` — NewBubbleNPC might be a different function (NPC-name bubble!). Let me check EmoteBubble.NewBubbleNPC — it's likely the "NPC portrait bubble" (showing a town NPC's face). Yes! EmoteBubble.NewBubbleNPC shows the bubble with an NPC icon — "Town NPC X" portrait. So state 7: NPC faces player and shows a bubble with... its own icon? That's the "NPC wants to talk" behavior. And 60 = BossMartianship shown at state 7 frameCounter==160 — a boss warning bubble (martian saucer?) during... hmm that's odd — this must be part of state 7: shows NPC face bubble at 16, then at 160 shows boss 60 bubble? That's the "NPC reacts to event" — actually no: this is probably the party girl or... whatever, special.

Our pool [25(BiomeCrimson), 90(ItemPickaxe), 100(MiscFire), 87(Confused), 89(Sleep)] — so ours picks random themed emotes vs vanilla's RPS games + sleep bubbles. Different content entirely.

OK — now I have a comprehensive picture. Let me also double-check two remaining claims:

1. **我们的白天游走无悬崖保护/溺水跳跃** — confirmed by reading fixedUpdate (no cliff check).
2. **Homeless NPC 游走锚** — vanilla: homeless NPCs anchor homeTile at first ground stand, wander ±25 around it. Ours: no home → `else if (this.home)` branch skipped → day wander unbounded; at night they just wander too (no home). Vanilla homeless at night: FindGoodRestingSpot home anchor → they go stand at their anchor. Deviation.

3. Item 5 teleport-home conditions vanilla vs ours:
- Vanilla: gated on `!homeless && townNPC && (flag || (type==37 && dungeon tile)) && !IsInAGoodRestingSpot`; player rect checks use sWidth (sprite width? or screen?) — wait: `Rectangle rectangle = new Rectangle((int)(position.X + width/2 - sWidth/2 - safeRangeX), ...sWidth + safeRangeX*2, sHeight + safeRangeY*2)`. What are sWidth/sHeight here? They're NPC.cs fields? Let me check: NPC has `sWidth`? Hmm — actually I bet these are `Main.screenWidth`? No wait, in NPC.cs context... Let me grep "sWidth = " in NPC.cs.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:43:16.046Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"int sWidth\\|sWidth =\\|int sHeight\\|sHeight =\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | head; grep -n \"public int sWidth\\|public int sHeight\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Entity.cs\" 2>/dev/null; find ~/Project/GLM/SandboxWorld/Terarria1456 -name \"Entity.cs\" | head -2",
 "description": "Find sWidth sHeight definitions"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:43:16.117Z

**📎 ToolResult**

```
6695:	public static int sWidth => 1920;
6697:	public static int sHeight => 1200;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Entity.cs

```


---

## 🤖 Assistant · 2026-08-17T04:43:38.322Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
`sWidth => 1920; sHeight => 1200` — static 1920×1200! So the teleport-home visibility rectangle = 1920×1200 + safeRange(=0? safeRangeX/safeRangeY are Main fields — Main.safeRangeX = sWidth/16*0.52 tiles? No wait — those were in Main.cs line 845: safeRangeX = (sWidth/16)*0.52 in *tiles*. But in NPC.cs :53835 the Rectangle uses `safeRangeX` directly added to `sWidth` (pixels vs tiles mixing?) — decompiler artifact aside: the check rectangle ≈ 1920+safeRangeX×2 px wide × 1200+safeRangeY×2 px tall, i.e., roughly "is the player anywhere near a 1920×1200 screen centered on the NPC". That's a generous "off-screen" test. Ours: 42-tile (672px) radius circle — MUCH smaller than vanilla's ~1920×1200 rect (~60×37.5 tiles + margins). Consequence: ours teleports NPCs home while player is much closer than vanilla would (vanilla requires player to be roughly a full screen away). Ours teleports when player is 42 tiles away — that's within a 1920-wide screen at typical zoom? At default zoom, a 1920px screen ≈ 120 tiles wide × 75 tall... wait Terraria default zoom: 1920×1080 screen shows about 1920/16=120 tiles wide at zoom 1. So vanilla waits until player is >~a screen away. Ours: 42 tiles = 672px — NPC can vanish while still on screen (if screen shows 60+ tiles). **Deviation: teleport-home player-distance threshold too small → visible vanishing.**

Also vanilla TeleportToHome fallback: all 3 columns blocked → homeless + QuickFindHome. Ours: silently gives up. Minor.

Now — night walk home: vanilla during flag, if NPC not at resting spot: state 1 walk toward floorX with ai[1]=200+Next(200). If at spot: decelerate then TryForcingSitting. Ours walks toward home with 4px threshold (restSpot) or TILE threshold. Roughly OK.

One more check — during night, if NPC is homeless (no home): vanilla homeless NPCs just wander (flag doesn't apply since !homeless gate). Ours: no home → wanders ✓.

Now check "door open" chance: vanilla `Main.rand.Next(10) == 0 || flag` (night/rain → always try). Ours: `Math.random() >= 0.1 return` — no flag boost (at night ours still 1/10 per tick — but since ours opens door only when hitWall, effectively similar since NPC keeps bumping). Vanilla also checks door at head tile (num27-2) while walking; and after opening, ai[1] += 80 (walk longer). Ours: no ai[1] extension. Minor.

Also vanilla: NPC closes door only for type 11 open door / 389 tall gate ✓ ours.

Let me now double-check our sitting entry during NIGHT walking home: our walk-home target = restSpot with 4px threshold; vanilla requires exact tile match (num6==floorX && num7==floorY) then decelerates and TryForcingSitting. Ours requires onGround && |vx|<0.05 && same tile — equivalent-ish. ✓.

BUT ours: `this.restSpot = (sitFlag && !world.clock.isDay && this.home && !NO_SIT...)` — during day-rain, restSpot=null → walk-home branch uses home.x with TILE threshold ✓ vanilla day-rain: FindGoodRestingSpot early-return → floor = home ground ✓. But ours day-rain doesn't trigger walk-home at all (the else-if chain: isDay → wander). Only teleport (if player far). Partial.

Also: our walk-home branch runs only when NOT sitting and (night OR sitting OR stationary). During night: NPCs walk home — good. Note `stationary` (old man) always → walk home branch at all times (day too)? stationary → first branch `!this.stationary` false → falls to `else if (this.home)` → old man walks to home all day if far. Old man has home? maybeRespawnOldMan sets home? Not critical.

Now — vanilla danger fleeing also has: PrettySafe (retreat threshold — if nearest threat beyond PrettySafe distance, don't flee). And townsfolk speed boost. Our attackUpdate uses TOWN_PRETTY_SAFE only for pirate panic shot. Missing flee entirely.

Let me also check our Enemy.ts hit flash and knockback for Enemy (item 10 is "全 NPC 通用" — Enemy side likely already audited in other sessions; I'll spot-check npcLiquid.ts which exists (honey/lava/water gravity for enemies ✓) — TownNPC doesn't use it though. Let me verify quickly that Enemy handles honey/lava/drowning.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:43:39.130Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "head -60 ~/Project/GLM/SandboxWorld/game/src/entities/npcLiquid.ts; grep -n \"lava\\|honey\\|drown\\|breath\" ~/Project/GLM/SandboxWorld/game/src/entities/npcLiquid.ts | head -15",
 "description": "Check Enemy liquid handling module"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:43:39.174Z

**📎 ToolResult**

```
// 敌怪液体交互 1:1（1.4.5.6 NPC.cs UpdateCollision :93712-93805 + Collision_MoveWhileWet :93986
// + Collision.cs WetCollision :1575 / LavaCollision :1657 + TryRemovingWaterPerishableEffects :94537）。
//
// 原版全量语义（本模块逐条实现）：
//  1. wet 判定 = Collision.WetCollision：**中心小盒**（宽 min(10,w) × 高 min(h/2,h)，居中），
//     而非整包围盒；液体格按液面高度收缩（(256-liquid)/32 ×2px 下探、有效高 16-该值）；
//     坡面格（slope≠0 且上方格有液体）按整格 16px 计。岩浆格同样令 wet=true。
//  2. 永不沾水族（:94252）：(690 且 ai[0]==0) | 72 | aiStyle21 | aiStyle67 | 376 | 579 | 541
//     | (aiStyle7 且 ai[0]==25) → wet 恒 false、wetCount=0；且随后 `if(!wet)` 会把本 tick
//     岩浆判定留下的 lavaWet 一并清掉 → 这族在岩浆里照常受伤但移动不受任何液体减速。
//  3. 出入水 transition（wetCount 10t 去抖，:94280/:94386）：入水/出水瞬间各播一次溅落；
//     出水瞬间 velocity.X *= 0.5（:94381）；620 火把僵尸出水朝上玩家补 vy-=8（:94384）。
//  4. 移动积分（Collision_MoveWhileWet :93986）：wet 时位移 ×factor —— **velocity 本身不变**，
//     只缩位移（TileCollision.moveAndCollide 入口按 liqFactor 缩 dx/dy 同语义）。
//     factor 默认表（NPC.cs:5946-5952）：水 .5 / 岩浆 .5 / 蜂蜜 .25 / 微光 .375；
//     优先级 微光 > 蜂蜜 > 岩浆 > 水（:93748-93762）。例外 = 1f：DD2 族
//     （LazySetLiquidMovementDD2 :18031，类型 548/549/551-578/620）与 612/613（:16810）。
//  5. 入水熄火（TryRemovingWaterPerishableEffects :94537）：wet 且非岩浆 → DelBuff 24(OnFire)
//     与 323(OnFire3)。蜂蜜/微光同样熄火（门只查 lavaWet）。
//  6. 岩浆（Collision_LavaCollision :94513）：lavaWet=true；非 lavaImmune 族 30t 独立冷却
//     （immune[255]）→ AddBuff(24,420) + 50 直伤。
//
// 本仓差异说明：原版 AI() 先跑、UpdateCollision 后跑（AI 读的是上一 tick 的 wet）；
// 本仓 AI 内部自带移动积分，故液体状态在 AI 之后更新，liqFactor 生效于下一 tick——
// 入水首帧差 1 帧全速，量级 <4px，不可感知。AI 分支读 wet 的时序与原版一致。
import { TILE } from '../core/constants';
import type { TileStore } from '../world/TileStore';
import type { GameHooks } from './types';
import type { Player } from './Player';
import { liquidCollision } from '../stats/TouchDamage';
import { NPC_LAVA_IMMUNE } from '../data/npcLavaImmune';

/** Collision.WetCollision（Collision.cs:1575-1656）1:1：中心小盒 + 液面收缩 + 坡上液体。 */
export function wetCollision(
  st: TileStore, px: number, py: number, pw: number, ph: number,
): { wet: boolean; honey: boolean; shimmer: boolean } {
  const TS = TILE;
  let num = 10;                       // 盒宽（>Width 时取 Width）
  let num2 = Math.floor(ph / 2);      // 盒高（>Height 时取 Height）
  if (num > pw) num = pw;
  if (num2 > ph) num2 = ph;
  const vx = px + pw / 2 - num / 2;   // 盒左上（实体中心居中）
  const vy = py + ph / 2 - num2 / 2;
  const i0 = Math.max(0, Math.floor(px / TS) - 1);
  const i1 = Math.min(st.w - 1, Math.floor((px + pw) / TS) + 2);
  const j0 = Math.max(0, Math.floor(py / TS) - 1);
  const j1 = Math.min(st.h - 40, Math.floor((py + ph) / TS) + 2);
  let honey = false;
  let shimmer = false;
  for (let i = i0; i < i1; i++) {
    for (let j = j0; j < j1; j++) {
      if (!st.inBounds(i, j)) continue;
      const idx = st.idx(i, j);
      if (st.liquid[idx] > 0) {
        // 液面高度：liquid 255 → 几乎满格；不足时表面下探、有效高收缩（:1609-1616）
        const drop = (256 - st.liquid[idx]) / 32;
        const surfY = j * TS + drop * 2;
        const effH = TS - Math.trunc(drop * 2);
        if (vx + num > i * TS && vx < i * TS + TS && vy + num2 > surfY && vy < surfY + effH) {
          if (st.liquidType[idx] === 3) honey = true;
10://     岩浆判定留下的 lavaWet 一并清掉 → 这族在岩浆里照常受伤但移动不受任何液体减速。
19://     与 323(OnFire3)。蜂蜜/微光同样熄火（门只查 lavaWet）。
20://  6. 岩浆（Collision_LavaCollision :94513）：lavaWet=true；非 lavaImmune 族 30t 独立冷却
36:): { wet: boolean; honey: boolean; shimmer: boolean } {
48:  let honey = false;
60:          if (st.liquidType[idx] === 3) honey = true;
62:          return { wet: true, honey, shimmer };
70:          if (st.liquidType[above] === 3) honey = true;
72:          return { wet: true, honey, shimmer };
77:  return { wet: false, honey, shimmer };
113:  if (b.honeyWet) return 0.25;
114:  if (b.lavaWet) return 0.5;
118:/** 永不沾水族（NPC.cs:94252）：wet 恒 false（连带本 tick lavaWet 被清） */
135:  honeyWet: boolean;
137:  lavaWet: boolean;

```


---

## 🤖 Assistant · 2026-08-17T04:44:08.255Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The Enemy-side liquid module is comprehensive (Enemy uses it). TownNPC doesn't use it — TownNPC's fixedUpdate uses fixed GRAVITY/MAX_FALL_SPEED without liquid movement factors or the water/honey gravity profile. TownNPC's envHurtUpdate covers lava/drowning/NPC-vs-NPC but not honey/water movement factor, not wet splash, not water gravity 0.2/7. Vanilla UpdateNPC applies the wet gravity profile (:91928-91942) to ALL NPCs including town NPCs, plus Collision_MoveWhileWet displacement factors. So town NPC in water falls at full speed in ours.

Now let me compile the final numbers on vanilla line references. Let me collect the precise line numbers for each behavior from vanilla:

1. Sitting:
- FindGoodRestingSpot: NPC.cs:53195-53262 (chair scan at night only :53209 dayTime early return; CanBeSatOnForNPCs :53223; frameY%40 top/bottom tile handling :53247-53252)
- TryForcingSitting: :53264-53287 (chair style 27 toilet exclusion frameY 1080-1098 :53274-53275; occupancy :53277-53286; sit: ai[1]=900+Next(10800) :53283, direction=frameX!=0 :53284, anchor :53285-53286)
- Random daytime sit while walking: :55699-55736 (`flag30 && ai[0]==1 && velocity.Y==0 && num>0 && rand(num)==0` num=300 :53372-53376; tile 15/497 check :55723-55731; player-sitting occupancy :55790-55797)
- Sitting state advance: :54682-54710 (chair removed → stand :54691-54697; expire :54703-54709; sittingManager.AddNPC :54701)
- Sitting frame: FindFrame :69638-69644 `frame.Y = num * (num58 - 3)` (637 → 19)
- Sitting hat Y: Main.cs:26968-26976 (already implemented in ours ✓)

2. Sleeping: NO references in NPC.cs (only player sleepingManager). → 原版无.

3. Wander:
- state 0 idle: :54119-54212 (decel ±0.1 :54096-54106; drown check :54155-54171; turn at rand(80) :54195-54201; walk start ai[1]=200+Next(300) :54174-54182)
- state 1 walking: :54204-54648 (speed num22=1/num23=0.07 :54287-54318; flee speed 1.5+missing-life*0.9 :54319-54326; far-from-home faster countdown -5 :54217-54224; door open 1/10 or flag :54552-54590; obstacle jumps -6/-5/-4.4 :54600-54640; turn when blocked :54641-54647; drowning jump-out :54450-54467; avoidFalling ground check :54468-54484; anti-stuck :54485-54490)
- walk→idle: ai[1]=300+Next(300)+Next(900) :54225-54235
- leash: ±25 soft / ±50 force turn :54186-54199
- GetWalkPrediction: :56093-56170 (avoidFalling: drop-off + lava + drowning lookahead)

4. Dialogue/social:
- player talkNPC → state 0 face player: :53721-53742
- pair chat 3/4: :55636-55674 (rand(300), dist 20..100, duration 420×(1..3|1..4))
- pair chat 16/17 (RPS emotes 36/37/38): :55675-55703 (rand(1800)); RPS mirror logic FindFrame :70030-70135
- face player state 7: :55760-55780 (rand(1200), dist<150, 220t; emote NPC-portrait 112 at tick 16 FindFrame :69691)
- party dance state 6: :55704-55730 (rand(1200), type 208 or party+AttackType0; 300t; dance frames+music dust FindFrame :69645-69700)
- bartender 18: :55731-55751 (rand(600), 300t)
- idle emote state 2: :55752-55759 (rand(1800), 45t; sleepy emote 89 + frame num58-1 FindFrame :69620-69640)
- CheckDialogue/ConditionalDialogue: :91577-91588 + ConditionalDialogue.cs (FreeCake 208 only; indicator icon Main.cs:45484/:56028; homeless icon CanShowHomelessText :96048 + dist<105)
- GetChat with name etc: :94974+ (ours 1:1 ✓)

5. Teleport home: :53828-53856 trigger (flag=raining||!dayTime||eclipse||slimeRain||storm-above-ground :53383-53402; dungeon-floor guide special; !IsInAGoodRestingSpot; player rect checks with sWidth=1920/sHeight=1200 + safeRange); TeleportToHome :56063-56090 (columns 0/-1/+1; SolidTiles 3×3; fail → homeless+QuickFindHome :56087-56089; then TryForcingSitting)

6. Party: hats UpdateAltTexture :91252-91266 ✓ours; dance :55704; party shop stock (Chest.cs:1400 etc. 5643 etc.) — need check ours has party stock; no price discount in vanilla ✓.

7. Push: no player→NPC push in vanilla (players pass through NPCs). NPC→NPC: no physical push (only sitting occupancy + keepwalking friendly-blocked check in GetWalkPrediction :56105-56116: walking NPC stops if another friendly NPC blocks path... actually keepwalking=true if a stationary friendly NPC is in the way — that's pathing, not pushing).

8. Death: NPCLoot :79628 (town NPC drops nothing; gore via HitEffect per-type), respawn via checkTownNPCs cycle every 7200t (Main.cs:65021-65040) ✓ ours cadence; vanilla re-runs QuickFindHome each cycle :65079-65083.

9. Defense: dryadWard + boss-progression defense chain :53401-53531 (defense += 2..20), tipsy ×1.1. Ours: only books +8 (registered as gap in comment). Invincibility: immune frames standard 10 (player strikes); shimmer rise dontTakeDamage ✓ ours.

10. Hit flash/knockback/liquids:
- wet gravity profile :91928-91942 (water 0.2/7, honey 0.1/4, shimmer 0.15/5.5) — ours TownNPC missing
- liquid movement factor (water .5 / honey .25) via Collision_MoveWhileWet — Enemy has, TownNPC missing
- lava 30t cd 50dmg + OnFire 24/420 :94511-94530 — ours hurt ✓ but no OnFire (noted)
- drowning :96118-96154 ✓ ours
- GetHurtByOtherNPCs :93605-93690 ✓ ours (30t cd, kb 6)
- no sprite white flash in vanilla (blood dust + damage numbers instead); ours adds brightness(2.5) flicker
- knockback: vanilla applies hit knockback directly (velocity = kb*dir with height factor); ours vx += kb*0.6 (0.6 factor + additive, not set)

Let me verify our shop party stock quickly — grep 5643.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:44:09.524Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"5643\\|partyUp\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | grep -in \"shop\\|stock\\|5643\" | head; grep -n \"5643\" ~/Project/GLM/SandboxWorld/game/src/data/vanilla-shopstock.json 2>/dev/null | head -3; ls ~/Project/GLM/SandboxWorld/game/src/data/ | grep -i shop",
 "description": "Check party shop stock in our data"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:44:09.614Z

**📎 ToolResult**

```
<persisted-output>
Output too large (56.4KB). Full output saved to: ~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/c44574b3-7d4d-403b-8e39-61a13d11a1c6/tool-results/bv2xuki14.txt

Preview (first 2KB):
1:~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4654:    // （附 4.5 格泛光近似省略）；5643 彩虹 = Disco 轮转
2:~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4661:      if (gvid === 5643) {
1:{"values":{"1":2000,"4":1800,"6":1400,"7":1600,"8":50,"10":1600,"11":500,"12":250,"15":1000,"16":5000,"17":10000,"19":6000,"20":750,"21":3000,"22":1500,"23":5,"24":100,"25":200,"27":10,"28":300,"29":75000,"31":20,"32":300,"33":300,"34":150,"35":5000,"36":150,"37":1000,"38":500,"39":100,"40":5,"41":10,"42":15,"44":18000,"45":13500,"46":13500,"47":40,"48":500,"49":50000,"50":50000,"51":100,"52":300,"53":50000,"54":50000,"55":50000,"59":500,"60":50,"62":20,"63":5000,"65":50000,"66":75,"67":100,"68":10,"69":100,"71":5,"72":500,"73":50000,"74":5000000,"76":1000,"77":4000,"78":10000,"79":20000,"80":1250,"81":5000,"82":12500,"83":25000,"84":20000,"85":200,"86":500,"87":10000,"88":40000,"89":750,"90":3000,"91":7500,"92":15000,"95":50000,"97":7,"98":350000,"99":1400,"100":22500,"101":30000,"102":37500,"103":18000,"104":15000,"106":3000,"107":12000,"108":24000,"110":100,"112":500000,"114":50000,"116":1000,"117":7000,"118":1000,"119":100000,"120":27000,"121":27000,"122":27000,"123":45000,"124":30000,"125":30000,"126":20,"127":20000,"128":50000,"151":45000,"152":30000,"153":30000,"154":50,"158":27000,"160":27000,"161":80,"166":300,"167":2000,"168":75,"175":20000,"177":5625,"178":11250,"179":7500,"180":3750,"181":1875,"182":15000,"183":50,"185":20000,"186":10000,"187":10000,"188":1000,"189":250,"190":27000,"191":50000,"193":27000,"194":150,"195":150,"196":50,"197":500000,"198":27000,"199":27000,"200":27000,"201":27000,"202":27000,"203":27000,"204":15000,"208":100,"209":200,"210":1000,"211":50000,"212":50000,"213":25000,"215":100,"217":27000,"221":3000,"222":100,"223":27000,"224":2000,"225":1000,"226":1500,"227":1500,"228":45000,"229":30000,"230":30000,"231":45000,"232":30000,"233":30000,"234":8,"235":500,"236":5000,"237":10000,"238":10000,"239":10000,"240":5000,"241":5000,"24
...
</persisted-output>

```


---

## 🤖 Assistant · 2026-08-17T04:44:14.350Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The grep output is too large; the key question — does the shop system add party-conditional stock (Chest.cs `if (BirthdayParty.PartyIsUp) array[num++].SetDefaults(5643)` at 1400/1942/2318/3354 — these are for merchant(17)? line 1400 in a shop = merchant or demolitionist etc.)? Our shopCondOk handles conds — party items would have cond like "PartyIsUp". Let me check the extraction JSON for party conds — search for "PartyIsUp" in the shopstock json.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:44:16.291Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 -c \"\nimport json\nd=json.load(open('~/Project/GLM/SandboxWorld/game/src/data/vanilla-shopstock.json'))\nshops=d.get('shops',{})\nfor k,items in shops.items():\n    for it in items:\n        if it.get('cond') and ('party' in str(it['cond']).lower() or it['cond'] in ('PartyIsUp','party')):\n            print(k, it)\n\" 2>/dev/null | head; grep -o \"PartyIsUp\" ~/Project/GLM/SandboxWorld/game/src/data/vanilla-shopstock.json | head -3; grep -rn \"shopCondOk\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | head -3",
 "description": "Check party conditional stock in shop data"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:44:16.401Z

**📎 ToolResult**

```
17 {'id': 5643, 'price': 20, 'cond': 'party'}
54 {'id': 3730, 'price': 20000, 'cond': 'party'}
54 {'id': 3731, 'price': 20000, 'cond': 'party'}
54 {'id': 3733, 'price': 30000, 'cond': 'party'}
54 {'id': 3734, 'price': 30000, 'cond': 'party'}
54 {'id': 3735, 'price': 30000, 'cond': 'party'}
208 {'id': 3749, 'price': 2000, 'cond': 'party'}
208 {'id': 3746, 'price': 10000, 'cond': 'party'}
208 {'id': 3739, 'price': None, 'cond': 'party'}
208 {'id': 3740, 'price': None, 'cond': 'party'}
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:14032:    const out: Array<[number, number]> = stock.filter((s) => this.shopCondOk(s.cond)).map((s) => [s.id, s.price ?? 100] as [number, number]);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:14148:  private shopCondOk(cond: string | null): boolean {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:14152:    if (cond.includes('||')) return cond.split('||').some((c) => this.shopCondOk(c));

```


---

## 🤖 Assistant · 2026-08-17T04:44:19.832Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Party shop stock is extracted and gated by 'party' cond — need to verify shopCondOk handles 'party' → partyIsUp. Quick check.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:44:20.195Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '14148,14195p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Read shopCondOk for party handling"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:44:20.228Z

**📎 ToolResult**

```
  private shopCondOk(cond: string | null): boolean {
    if (!cond) return true;
    // 顶层 OR（extract-shops.mjs 2026-08-13 OR 感知产出,如军火商银子弹
    // `downedBoss2&&night||hardMode`）:任一支成立即上架（|| 优先级低于 &&）
    if (cond.includes('||')) return cond.split('||').some((c) => this.shopCondOk(c));
    // 复合门（extract-shops.mjs parseGate：嵌套 if 的全部开门按 '&&' 连接，
    // 如 `hardMode && ZoneGraveyard`——外层与内层同时成立才上架）
    if (cond.includes('&&')) return cond.split('&&').every((c) => this.shopCondOk(c));
    // 取反 token（extract-shops.mjs else-if 互斥链生成，如 '!zoneGraveyard&&day'
    // = 非墓地白天）：Chest.SetupShop 的 else-if 分支只在全部前支不成立时执行。
    // 未知 token 取反同样 false（无法证明成立 → 保守不上架，与正向 default 同策略）
    if (cond.startsWith('!')) return !this.shopCondOk(cond.slice(1));
    const f = this.world.flags;
    switch (cond) {
      case 'hardMode': return !!f.hardMode;
      case 'downedBoss1': return !!(f['downed_4'] || f.downedEyeOfCthulhu);
      case 'downedBoss2': return !!(f['downed_13'] || f['downed_266']);
      case 'downedBoss3': return !!(f['downed_35'] || f.downedSkeletron);
      case 'downedMechBossAny':
        return !!(f['downed_125'] || f['downed_126'] || f['downed_127'] || f['downed_134']);
      // 单机械王（造型师 1985 染发剂 = hardMode && 三机械全灭 等,Chest.cs:2737）。
      // vanilla 语义(NPC.cs:80256-80277)：mech1=毁灭者 134 / mech2=双子 125(126 旧档
      // 兼容读) / mech3=Prime 127——曾 125/126/127 顺位错指三家
      case 'downedMechBoss1': return !!f['downed_134'];
      case 'downedMechBoss2': return !!(f['downed_125'] || f['downed_126']);
      case 'downedMechBoss3': return !!f['downed_127'];
      // NPC.downedPlantBoss（世纪之花商店门：爆破专家地雷 937 / 松露自动锤 1551 /
      // 巫医 Tiki 套·灵液瓶·叶翼 / 画家回声涂层 5344 / 动物学家泥芽 4701）
      case 'downedPlantBoss': return !!f['downed_262'];
      case 'downedPirates': return !!f.downedPirates;
      case 'moonPhase':
        // 月相门：extract-shops.mjs 未捕获 case 相位值——恒 false，分档上架由
        // shopStockFor 的相位实表负责（改 true 会全相位重复上架）
        return false;
      case 'night': return !this.world.clock.isDay;
      case 'day': return this.world.clock.isDay;
      case 'zoneSnow': return !!this.scene?.zoneSnow;
      case 'zoneJungle': return !!this.scene?.zoneJungle;
      case 'zoneGraveyard': return !!this.scene?.zoneGraveyard;
      case 'zoneMeteor': return !!this.scene?.zoneMeteor;
      case 'zoneUnderworld': return !!this.scene?.zoneUnderworldHeight;
      case 'crimson': return this.world.crimson;
      case 'bloodMoon': return this.world.clock.bloodMoon;
      case 'xMas': return this.world.clock.xMas;
      case 'eclipse': return !!this.world.clock.eclipse; // 日食（电子人 774 等）
      case 'party': return partyIsUp(this.partyState);   // 派对进行中（派对商品族）
      case 'lanternNight': return LanternNight.lanternsUp; // 灯笼夜（派对女孩 4702 放飞灯笼）
      // 动物学家图鉴门（Chest.cs:3265-3280：狗狗许可证 4830 ≥25% / 兔兔许可证

```


---

## 🤖 Assistant · 2026-08-17T04:44:30.832Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Party shop stock ✓ (cond 'party' handled). Party system ✓ hats, ✓ shop, ✗ dance.

Now let me double check one remaining thing — the "night walk home" vanilla also has NPCs at night with no chair walking to home and standing (not sitting). Ours ✓.

And what about vanilla NPC at night walking home — do they open doors on the way? Yes (door open chance boosted at flag). Ours ✓ doors.

One more check: does our town NPC use TILE-defined solid vs platform for step? Not critical.

Let me also double check our TownNPC jump: `if (this.onGround && this.hitWall && wantDir !== 0) this.vy = -6` — need hitWall from moveAndCollide. OK.

Also missing: vanilla `if (velocity.Y < 0f && wet) velocity.Y *= 1.2f` — jump-through-water boost for escape. Part of missing water behaviors.

Now, let me verify our emote during night: tickNpcEmotes gated `if (this.world.clock.isDay && ...)` — so NO emotes at night at all. Vanilla pair chat can happen at night (NPCs standing at home). Minor.

Let me also spot check that the Renderer has "attack frames" — search for GetShootingFrame equivalent or attack frame handling — grep "num58\|attackFrame\|TOWN_ATTACK_FRAME" in Renderer.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:44:32.719Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"ShootingFrame\\|attackFrame\\|atkFrame\\|TOWN_ATTACK_FRAME\\|frame.*attack\\|AttackFrameCount\" ~/Project/GLM/SandboxWorld/game/src/ --include=\"*.ts\" | grep -iv \"atkTimer\\|atkState\\|attackState\\|attackUpdate\" | head -10; grep -rn \"ExtraFramesCount\\|extraFrames\\|extra\" ~/Project/GLM/SandboxWorld/game/src/data/townNpcProfiles.ts | head -5",
 "description": "Check attack frame animation in our renderer"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:44:32.809Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-17T04:44:42.614Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
No attack-frame animation at all (except holdout weapon for bow). Frames used: 0/1/2..walk only.

Let me now verify the TOWN_ATTACK tables & whether ExtraFramesCount data exists anywhere (for the report's fix spec). Check vanillaTownAttack.ts quickly for what's available (shootTick, burst, cd, etc. — this supports attack states but not frames).

Now let me check the last two open questions:

1. **Item 7 (player pushing NPCs)**: vanilla — Player walking into NPC: no push. BUT there is one interaction: standing on NPCs? No. NPC push by player: none. I'm fairly confident. Let me do a quick sanity grep in Player.cs for npc push — "PushNPC"? Not needed; vanilla players pass through town NPCs freely. Also NPC↔NPC: vanilla town NPCs walk through each other (no physical collision), with the "keepwalking" social logic. So answer: 原版无推挤行为 → ours also none → ✓ 对齐 (both no-op).

2. **Guide-37 disappear after Skeletron** (ai[3]=1 removal) — ours? The old man becomes... vanilla: type 37 with downedBoss3 → ai[3]=1 → NPC removed (dungeon curse lifted, old man gone → becomes Clothier spawn). Ours: maybeRespawnOldMan — check the gate.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:44:43.109Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '2952,3010p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Read maybeRespawnOldMan for post-Skeletron behavior"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:44:43.155Z

**📎 ToolResult**

```
  private maybeRespawnOldMan() {
    if (this.world.dungeonX <= 0 || this.world.flags.downedSkeletron) return;
    if (this.entities.npcs.some((n) => n instanceof TownNPC && n.npcKey === 'old_man' && !n.dead)) return;
    const st = this.world.store;
    const dX = this.world.dungeonX;
    const dY = this.world.dungeonY || Math.floor(this.world.groundLevel);
    // 双侧由外向内扫门 tile(外廊门或塔基门),取最外侧一扇
    let doorX = -1, doorY = -1;
    for (let r = 70; r >= 3 && doorX < 0; r--) {
      for (const sd of [1, -1]) {
        const x = dX + sd * r;
        if (x < 3 || x > st.w - 4) continue;
        for (let y = Math.max(4, dY - 45); y < Math.min(st.h - 3, dY + 45); y++) {
          if (st.type[st.idx(x, y)] === T.DOOR_CLOSED) { doorX = x; doorY = y; break; }
        }
        if (doorX > 0) break;
      }
    }
    // 落位候选(按优先级):门外开阔侧 3 格 > 门内 1 格 > 门外 6/10 格 > 门内 4 格 >
    // 塔心入口扫描 > 裸兜底。每候选:向下 ≤10 格找地面 + 头顶 3 格净空(身高 40px)
    // + 3 宽地板(左右也实心,防站在竖井/悬崖边缘)
    const standSpot = (sx: number, syTop: number): { x: number; y: number } | null => {
      if (sx < 3 || sx > st.w - 4) return null;
      let yy = Math.max(4, syTop);
      const limit = Math.min(st.h - 3, syTop + 10);
      while (yy < limit && !st.isSolid(sx, yy)) yy++;
      if (yy >= limit) return null;
      if (!st.isSolid(sx - 1, yy) || !st.isSolid(sx + 1, yy)) return null;
      for (let k = 1; k <= 3; k++) if (st.isSolid(sx, yy - k)) return null;
      return { x: sx, y: yy - 3 };
    };
    const side = doorX >= dX ? 1 : -1; // 门相对塔心的方位,外侧 = 再往外
    const baseY = (doorY > 0 ? doorY : dY) - 2;
    // 首选 dungeonX/Y 本身(=门厅站立点);其余候选为门扫描兜底
    const cands: Array<[number, number]> = [[dX, dY - 3], [doorX + side * 3, baseY],
      [doorX - side, baseY], [doorX + side * 6, baseY],
      [doorX + side * 10, baseY], [doorX - side * 4, baseY], [dX, dY - 10]];
    let spot = cands.map(([cx0, cy0]) => standSpot(cx0, cy0)).find((s) => s) ?? null;
    if (!spot) {
      // 末级兜底①:门高平面 ±70 列扫任一有效落脚
      for (let r = 1; r <= 70 && !spot; r++) {
        for (const sd of [1, -1]) {
          spot = standSpot(dX + sd * r, baseY);
          if (spot) break;
        }
      }
    }
    if (!spot) {
      // 末级兜底②:门口悬空(地牢在陡坡上) → 塔外 20-70 列从天空向下扫地表,
      // 站到门外山坡(依然在门口视野内);再不行站塔顶
      for (let r = 20; r <= 70 && !spot; r++) {
        for (const sd of [1, -1]) {
          spot = standSpot(dX + sd * r, 8);
          if (spot) break;
        }
      }
    }
    if (!spot) spot = standSpot(dX, 8) ?? { x: dX, y: dY - 3 };
    const oldMan = new TownNPC('old_man', spot.x * 16 - 8, spot.y * 16);

```


---

## 🤖 Assistant · 2026-08-17T04:45:07.175Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Old man handling fine (gated on !downedSkeletron → disappears after Skeletron ✓ matches vanilla ai[3]=1 removal semantics approximately).

I now have everything needed. Let me also grab the exact vanilla line numbers for a few things I'll cite, and verify a couple of "ours" line numbers:

Ours (TownNPC.ts):
- wander speed: lines 777-778 (`this.vx += wantDir * 0.06; clamp ±0.8`)
- wander rhythm: lines 703-709 (wanderT = 90+rand(180), facing random, 35% stand)
- jump: line 787 (`vy=-6`)
- teleport home: lines 724-764 (42-tile circle)
- day wander branch: line 695 (`else if (!this.stationary && world.clock.isDay && !this.sitting)`)
- leash: lines 699-701 (leashHome 10 tiles)
- sitting entry night-only restSpot: lines 680-682
- sittingUpdate: 1305-1329; forceSit: 1333-1355
- updateWalkFrame (no sitting frame): 804-822
- attackUpdate trigger (no flee): 1007-1039
- envHurtUpdate: 934-982
- hurt: 455-476
- emote driver: Game.ts 13978-14011

Vanilla (NPC.cs) line refs:
- AI_007_TownEntities 53366
- num=300 sit chance base: 53372-53376
- danger scan: 53884-53958; flee/walk-away decision: 53960-54022 (direction = -num15 at ~54000; PrettySafe 53982)
- state 8 set: 54600-54603 (flag27 → ai[0]=8, ai[1]=240)
- rain/night flag: 53383-53402
- teleport trigger: 53830-53856
- TeleportToHome: 56063-56090
- walk speeds: 54287-54326
- obstacle jump: 54600-54644
- door open: 54552-54590
- door close: 54237-54277
- pair chat 3/4: 55636-55674
- pair chat 16/17: 55675-55703
- party dance 6: 55704-55730
- bartender 18: 55731-55751
- idle emote 2: 55752-55759
- face player 7: 55760-55780
- daytime random sit: 55699-55736 (wait — this is inside the same else-if chain; the sit branch is `else if (flag30 && ai[0]==1f && velocity.Y==0 && num>0 && rand(num)==0 ...` at ~55699; the numbers: I saw it in the sed output between state 7 branch and state 9 (SearchAvoidedByNPCs / interactable). Line numbers from my reading: the sed at 55400-55830 covered it; the sit branch began around 55698 ("else if (flag30 && ai[0] == 1f && velocity.Y == 0f && num > 0 && Main.rand.Next(num) == 0)") — I'll cite ~55698-55736.
- interactable tile look state 9: ~55830-55840 (PlotTileLine + InteractableByNPCs → ai[0]=9, 40+Next(90)) — NPCs stop and "look at" interactable furniture (torch etc.)! That's another idle behavior: NPC stops to look at nearby furniture. Ours: missing. Let me include it (minor).
- FindFrame: sitting 69638-69644; dance 69645-69700; face 7/19 ~69680-69714; state 9 frames 69717-69744; state 18 69745-69775; attack 10/13 frames 69776-69798; swing 15 69799-69817; shimmer 25 frame 1 :69818; shooting 12 GetShootingFrame 69825-69836; magic 14/24 69837-69860; chat 3/4 69865+; walk/idle 70130-70246.
- GetShootingFrame exists — let me get its line number for the report.
- wet gravity: 91928-91942
- liquid movement factors: NPC.cs:5946-5952 (per npcLiquid.ts header) + Collision_MoveWhileWet :93986
- lava: 94511-94530
- drowning: 96118-96154
- NPC vs NPC: 93605-93690
- CheckDialogue: 91577-91588
- homeless indicator: 96048-96060 + Main.cs:45484-45495
- progression defense chain: 53401-53531 (defense += at 53401-53412 dryadWard; +8 books at 53423/53431; +2/+3/+6/+8/+12/+20 chain 53437-53532; tipsy ×1.1 53553)
- NPCLoot: 79628; respawn cycle: Main.cs 65021-65040 + QuickFindHome per cycle 65079-65083
- UpdateAltTexture: 91252-91266

Let me get exact line for GetShootingFrame and double-check the "look at interactable" state 9 trigger lines.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:45:08.016Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"GetShootingFrame\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | head -3; awk 'NR>=55810 && NR<=55845' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | head -40",
 "description": "Get GetShootingFrame line and state 9 trigger"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:45:08.115Z

**📎 ToolResult**

```
67061:	public int GetShootingFrame(float circleY)
69827:					int num85 = num58 + GetShootingFrame(ai[2]);
						base.Bottom = new Vector2(point.X * 16 + 8 + 2 * direction, point.Y * 16 + 16);
						velocity = Vector2.Zero;
						localAI[3] = 0f;
						netUpdate = true;
					}
				}
			}
			else if (flag30 && ai[0] == 1f && velocity.Y == 0f && Main.rand.Next(600) == 0 && Utils.PlotTileLine(base.Top, base.Bottom, width, DelegateMethods.SearchAvoidedByNPCs))
			{
				Point point2 = (base.Center + new Vector2(direction * 10, 0f)).ToTileCoordinates();
				bool flag35 = WorldGen.InWorld(point2.X, point2.Y, 1);
				if (flag35)
				{
					Tile tileSafely7 = Framing.GetTileSafely(point2.X, point2.Y);
					if (!tileSafely7.nactive() || !TileID.Sets.InteractableByNPCs[tileSafely7.type])
					{
						flag35 = false;
					}
				}
				if (flag35)
				{
					ai[0] = 9f;
					ai[1] = 40 + Main.rand.Next(90);
					velocity = Vector2.Zero;
					localAI[3] = 0f;
					netUpdate = true;
				}
			}
			if (Main.netMode != 1 && ai[0] < 2f && velocity.Y == 0f && type == 18 && breath > 0)
			{
				int num121 = -1;
				for (int num122 = 0; num122 < Main.maxNPCs; num122++)
				{
					NPC nPC6 = Main.npc[num122];
					if (nPC6.active && nPC6.townNPC && nPC6.life != nPC6.lifeMax && (num121 == -1 || nPC6.lifeMax - nPC6.life > Main.npc[num121].lifeMax - Main.npc[num121].life) && Collision.CanHitLine(position, width, height, nPC6.position, nPC6.width, nPC6.height) && Distance(nPC6.Center) < 500f)
					{

```


---

## 🤖 Assistant · 2026-08-17T04:45:11.606Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All confirmed. Let me quickly get the exact line numbers of a few key blocks I'll cite using grep -n on distinctive strings, so my citations are accurate:
1. `else if (flag30 && ai[0] == 1f && velocity.Y == 0f && num > 0 && Main.rand.Next(num) == 0` — daytime sit
2. `direction = -num15` — flee direction
3. num22/num23 defaults
4. jump velocities
5. GetWalkPrediction
6. `Main.rand.Next(80) == 0` turn
7. state 3/4 trigger `Main.rand.Next(300)`
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:45:13.540Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"Main.rand.Next(num) == 0\\|direction = -num15\\|direction = num15;\\|float num23 = 0.07f\\|velocity.Y = -6f\\|velocity.Y = -5f\\|velocity.Y = -4.4f\\|Main.rand.Next(80) == 0\\|Main.rand.Next(300) == 0\\|Main.rand.Next(1800) == 0\\|Main.rand.Next(1200) == 0\\|num22 = 1.5f\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | head -25",
 "description": "Pin exact line numbers for citations"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:45:13.587Z

**📎 ToolResult**

```
1565:			else if (!savedBartender && DD2Event.ReadyToFindBartender && !AnyNPCs(579) && Main.rand.Next(80) == 0 && !waterTile)
3466:					if (downedPlantBoss && Main.rand.Next(80) == 0 && !AnyNPCs(477))
4277:						else if (!waterTile && num46 > Main.maxTilesX / 3 && spawnTileType == 2 && Main.rand.Next(300) == 0 && !AnyNPCs(50))
4912:					if (Main.rand.Next(80) == 0)
22340:							velocity.Y = -6f;
23662:							velocity.Y = -6f;
23705:							velocity.Y = -6f;
26179:				velocity.Y = -5f;
28683:							velocity.Y = -6f;
28919:							velocity.Y = -6f;
29237:						velocity.Y = -6f;
30220:							velocity.Y = -5f;
31031:					velocity.Y = -6f;
33789:					velocity.Y = -6f;
40951:			if (Main.netMode != 1 && Main.rand.Next(300) == 0)
43645:						velocity.Y = -6f;
45835:					velocity.Y = -6f;
45911:						Main.dust[num14].velocity.Y = -5f + Main.rand.NextFloat() * -3f;
48598:				velocity.Y = -5f;
50647:				velocity.Y = -6f;
50787:					velocity.Y = -6f;
54003:									nPC.direction = -num15;
54013:								direction = num15;
54017:								direction = -num15;
54024:						direction = -num15;

```


---

## 🤖 Assistant · 2026-08-17T04:45:18.629Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"flag30 && ai\\[0\\] == 1f && velocity.Y == 0f && num > 0\\|num22 = 1f\\|float num22 = 1f\\|num23 = 0.07f\\|ai\\[0\\] == 1f && Main.rand.Next(num)\\|Next(600) == 0 && Utils.PlotTileLine\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | head; grep -n \"54347\\|velocity.Y = -6f;\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | awk -F: '$1>54300 && $1<54700' | head",
 "description": "Pin remaining line numbers"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:45:18.686Z

**📎 ToolResult**

```
54280:				float num22 = 1f;
54281:				float num23 = 0.07f;
54300:						num23 = 0.07f;
54313:						num23 = 0.07f;
55774:			else if (flag30 && ai[0] == 1f && velocity.Y == 0f && num > 0 && Main.rand.Next(num) == 0)
55817:			else if (flag30 && ai[0] == 1f && velocity.Y == 0f && Main.rand.Next(600) == 0 && Utils.PlotTileLine(base.Top, base.Bottom, width, DelegateMethods.SearchAvoidedByNPCs))
54523:									velocity.Y = -6f;

```


---

## 🤖 Assistant · 2026-08-17T04:45:23.532Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Line numbers pinned:
- Daytime random sit: 55774-55814
- Interactable-look state 9: 55817-55839
- Walk speed: 54280-54281 (num22=1, num23=0.07)
- Obstacle jumps: 54523 (-6), 54534 (-5), 54543 (-4.4)
- Flee direction: 54024 (`direction = -num15` in the non-state-8 branch); 54017 within ai[0]==8 handling.

Let me pin the exact chat trigger lines and turn/leash lines with one more grep, plus ai[0]==8 set (240) and walk→idle numbers.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:45:25.140Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"CanTalk && flag30\\|flag30 && ai\\[0\\] == 0f && velocity.Y == 0f\\|ai\\[0\\] = 8f;\\|ai\\[1\\] = 240f;\\|num6 < floorX - 25\\|num6 > floorX + 50\\|ai\\[1\\] = 200 + Main.rand.Next(300)\\|ai\\[1\\] = 300 + Main.rand.Next(300)\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | head -14",
 "description": "Pin chat trigger and leash line numbers"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:45:25.181Z

**📎 ToolResult**

```
39633:						this.ai[0] = 8f;
44407:					this.ai[0] = 8f;
49799:					ai[0] = 8f;
53974:						ai[1] = 300 + Main.rand.Next(300);
54142:							ai[1] = 200 + Main.rand.Next(300);
54161:							ai[1] = 200 + Main.rand.Next(300);
54181:				if (num6 < floorX - 25 || num6 > floorX + 25)
54190:						else if (num6 > floorX + 50 && direction == 1)
54235:					ai[1] = 300 + Main.rand.Next(300);
54386:						ai[1] = 200 + Main.rand.Next(300);
54599:								ai[0] = 8f;
54600:								ai[1] = 240f;
55647:			if (CanTalk && flag30 && ai[0] == 0f && velocity.Y == 0f && Main.rand.Next(300) == 0)
55674:			else if (CanTalk && flag30 && ai[0] == 0f && velocity.Y == 0f && Main.rand.Next(1800) == 0)

```


---

## 🤖 Assistant · 2026-08-17T04:45:37.612Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All line numbers pinned. One more verification — I want to confirm our TownNPC "night walk home" doesn't handle homeless NPC anchor, and check that Enemy.ts hurt flash for Enemy (item 10 is about general NPC — Enemy already has its own pipeline; I'll spot check Enemy hurt has iframes=10?). Let me check Enemy.hurt briefly.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:45:38.098Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"iframes\\|immune\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -12",
 "description": "Check Enemy iframes"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:45:38.142Z

**📎 ToolResult**

```
696:  iframes = 0;
724:  /** 岩浆接触冷却（原版 immune[255]=30,NPC.cs:94528）与 onFire 状态（buff 24,秒） */
884:   *  不可击；AI 段自行清除）。与 iframes 不同：持续态而非帧计数 */
1000:      if (this.iframes > 0) this.iframes--;
1005:    if (this.iframes > 0) this.iframes--;
4189:      if (this.iframes > 0 && this.iframes % 4 === 0) { this.ai3 = 0; this.ai2 = 0; } // justHit 清充能
4211:      if (this.iframes > 0 && this.iframes % 4 === 0) this.ai3 = -45; // 受击冷却
4244:      if ((flee || this.iframes > 0) && this.onGround) {
6350:   *  原版 dontTakeDamage（盾>0 完全免伤，:41162-41176 每 tick 重算）用 iframes=2 每 tick
6378:      this.iframes = 2;                                  // dontTakeDamage = true（:41042）
6405:        this.iframes = 0;
6419:    if (le.shield[key] > 0) this.iframes = 2;

```


---

## 🤖 Assistant · 2026-08-17T04:45:44.066Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"hurt(dmg\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -3; sed -n '/hurt(dmg: number/,/^  }/p' ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -40",
 "description": "Read Enemy.hurt for iframes/flash"
}
```


---

## 👤 User(sidechain) · 2026-08-17T04:45:44.125Z

**📎 ToolResult**

```
6576:  hurt(dmg: number, kbx: number, kby: number, game: GameHooks, armorPen = 0, crit = false, pierce = 0, fromPlayer = false, penPercent = 0): boolean {
  hurt(dmg: number, kbx: number, kby: number, game: GameHooks, armorPen = 0, crit = false, pierce = 0, fromPlayer = false, penPercent = 0): boolean {
    // pierce 语义（Projectile.cs:11903-11907/13152-13155 Damage_PVE）：
    //   0   = 近战/荆棘等非弹幕 → 命中设免疫 10t（原版 immune[owner] 默认档）；
    //   1   = 单发弹（maxPenetrate==1，flag3）→ **无视免疫且命中后不设帧**
    //         ——同 tick 多发（霰弹/多随从）全部生效,不再互挡（旧全局 iframes=8
    //         致 8 发四管霰弹只吃 1 发,DPS≈1/8,2026-08-13 修）；
    //   >1  = 穿透弹 → 设 10t;同弹重复命中由弹侧 hitSet 拦（原版 per-owner 槽单人
    //         近似;弹型覆写 1-8 表 :13032 未接,登记）
    // Critter 兼容：critters 桶的调用方按 Critter.hurt(game) 单参调用；
    // 原版小动物是 Enemy 进该桶，这里把 Game 对象重映射回 game 参、伤害取固定 5
    if (typeof dmg === 'object' && dmg !== null) {
      game = dmg as unknown as GameHooks;
      dmg = 5; kbx = 0; kby = 0;
    }
    const rawDmg = dmg; // 傀儡上报用原始值（下方 def 凘认算只做一次，双端一致）
    // 死亡单次门(用户报"多弹头武器打出双份僵尸碎块"):pierce=1 豁免免疫帧后,
    // 同 tick 多弹头(霰弹/食人鱼咬+随从)会全部进 hurt——首发致死后,后续弹头
    // 对"已死未出列"的敌怪二次触发死亡管线(碎块/掉落/音效翻倍)。原版由
    // Damage_PVE 的 npc.active 前置门(Projectile.cs:11869)天然防重;此处等价。
    if (this.dead) return false;
    if (pierce !== 1 && this.iframes > 0) return false; // 单发弹豁免免疫检查（flag3）
    // 旗 buff 加伤（Main.GetBannerBuffEffect → StrikeNPC 乘区,ItemID.cs:11-44 普通族:
    // 经典 ×1.5/专家 ×2;DD2 0.2 族不区分,登记）——统一入口=StrikeNPC 全通道语义
    if (this.vanillaId != null && (game as { bannerNpcActive?: (n: number) => boolean }).bannerNpcActive?.(this.vanillaId)) {
      const g = game as { world?: { flags?: Record<string, boolean> } };
      dmg = Math.max(1, Math.round(dmg * (g.world?.flags?.hardMode ? 2 : 1.5)));
    }
    if (this.dontTakeDamage) return false; // 原版 NPC.dontTakeDamage（StrikeNPC 早退）
    this.justHitT = 2; // 原版 justHit 单帧旗标（AI_023 飞行武器/陆龟受击回态消费）
    // 训练假人（NPC 488，cs:83498 localAI 赋值）：immortal 永不死，
    // 受击只记摇晃强度+方向（渲染帧端消费），掉血由 dummyAI 回满
    if (this.vanillaId === 488) {
      this.dummyShake = Math.max(20, Math.min(120, dmg));
      this.dummyHitDir = Math.sign(kbx) || this.dummyHitDir;
      this.iframes = 8;
      return true;
    }
    // 猪鲨爆裂泡泡（NPC 371，StrikeNPC cs:82102-82107）：伤害清零(num=0)不扣血，
    // 直接转入爆炸态 ai[0]=1/ai[1]=4 + dontTakeDamage——"被击即爆"而非"被打死"；
    // aiStyle 70 (:35180-35194) 据此扩 100×100 并 EncourageDespawn(3) 消散

```


---

## 🤖 Assistant · 2026-08-17T04:46:27.533Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Enemy.hurt is well-developed (pierce semantics, banners, etc.) — the Enemy side of item 10 is in good shape. TownNPC.hurt is simpler (iframes=8 vs vanilla 10 for standard hits; knockback additive *0.6).

I now have everything I need for the final report. Let me also double-check whether our TownNPC handles the "state 9 look at interactable" — no (confirmed no PlotTileLine usage). And "wet" gating for pair chat — ours doesn't check wet — trivial.

One last check — is there anything in our code about town NPC sitting PLAYER occupancy (vanilla :55790 checks player sitting on same chair before NPC sits)? Ours forceSit only checks NPC occupancy, not player. Minor.

Also confirm: our night sitting only triggered from restSpot walk-home or teleport. Vanilla ALSO has state-0-at-resting-spot deceleration path (NPC walking at night reaches home area, slows, then TryForcingSitting via the flag branch at :54074-54080). Ours: walk-home → 4px threshold → sittingUpdate requires onGround + |vx|<0.05 + same tile → forceSit. Equivalent ✓.

Daytime sit missing entirely (vanilla 1/300 while walking over a chair tile). 

Now — severity ranking. Let me organize the final report:

**P0/严重 (行为缺失，肉眼可见):**
1. 危险逃离全缺失 — vanilla town NPCs run from enemies (flee direction, speed boost 1.5+0.9×missing life, state 8 cower-freeze 240t when blocked, PrettySafe threshold); ours stand & fight only. NPC.cs:53884-54022, 54287-54326 (flee speed), 54597-54603 (state 8), 53982 (PrettySafe). Ours: TownNPC.ts:1007-1039 attackUpdate only; no flee anywhere.
2. 坐姿帧未实现 — sitting uses frame 0 (standing); vanilla frame = num58-3 (FindFrame :69638-69644). Renderer/ TownNPC.updateWalkFrame (TownNPC.ts:804-822). Also party dance frames, chat frames, attack/shooting/swing frames all missing (FindFrame :69645-69860/69865+; GetShootingFrame :67061). This is the biggest visual giveaway of the sitting feature.

**P1/中等:**
3. 白天随机坐椅缺失 — vanilla :55774-55814 (walking NPC 1/300 per tick sits on chair tile 15/497, checks NPC+player occupancy, sits 900+Next(10800)); ours: restSpot night-only (TownNPC.ts:680-682) → daytime NPCs never sit.
4. 悬崖/坑洞避让缺失 — GetWalkPrediction (vanilla :56093-56170) + avoidFalling stop (:54468-54484) + drowning jump-out (:54444-54467); ours walks off any ledge; also homeless NPC wander anchor (vanilla anchors homeTile at first standing spot :53704-53706, wanders ±25).
5. 回家传送玩家视野阈值过小 — vanilla uses 1920×1200 + safeRange rects (:53835-53847, sWidth=>1920 :6695); ours 42-tile circle (TownNPC.ts:736) → NPCs visibly vanish/teleport closer than vanilla. Also TeleportToHome failure fallback (homeless+QuickFindHome :56087-56089) missing.
6. 游走节奏/速度常量偏差 — vanilla walk max 1.0/accel 0.07 (:54280-54281), walk duration 200-500t, idle 300-1500t (:54235), random turn 1/80 with 200t lockout (:54195-54201), leash ±25/force ±50 (:54181-54199); ours: 0.8/0.06, wanderT 90-270 uniform both states, no turn lockout, leash 10 tiles only for leashHome (TownNPC.ts:695-710, 777-778).
7. 越障跳跃简化 — vanilla 3-tier (-6/-5/-4.4 by obstacle height, :54523/54534/54543) + ceiling check → turn around when blocked (:54525-54551) + anti-stuck; ours single vy=-6 on hitWall (TownNPC.ts:787) → wall-hopping never turns back; door-open ai[1]+=80 missing.
8. 社交系统简化 — vanilla per-NPC per-tick rolls: pair chat 3/4 1/300 (:55647) dur 420×(1..3|1..4) with talk frames; pair chat 16/17 1/1800 (:55674) = rock-paper-scissors emotes 36/37/38 with mirror logic (FindFrame :70030-70135); face-player 7 1/1200 (:55760) 220t + NPC-portrait bubble 112; idle sleep emote state 2 1/1800 (:55752) + frame num58-1 + emote 89; bartender 18 1/600; interactable-look state 9 1/600 (:55817). Ours: single global pair every 600 ticks, wrong emote pool, day-only (Game.ts:13978-14011).
9. 派对跳舞缺失 — vanilla state 6 dance (:55704-55730; party girl always 1/1200; during party all AttackType==0 NPCs; dance frames + music-note dust 139-143 FindFrame :69645-69700); ours: no dance. (Party hats ✓, party shop stock ✓, no discount = 原版无 ✓.)

**P2/轻微:**
10. 白天雨不回家 — vanilla flag includes day rain → walk/teleport home; ours walk-home branch day-gated (TownNPC.ts:695), only teleport applies.
11. 液体物理缺失 for town NPC — vanilla wet gravity 0.2/7 honey 0.1/4 shimmer 0.15/5.5 (:91928-91942) + movement factors (water .5/honey .25, :5946-5952); ours fixed GRAVITY/MAX_FALL (TownNPC.ts:641,788); jump-out-of-water ×1.2 (:54646) missing.
12. 受击细节 — iframes 8 vs vanilla 10; knockback additive ×0.6 vs vanilla set; boss-progression defense chain (+2..+20, :53437-53532) & dryadWard missing in hurt (TownNPC.ts:455-476) — partially registered in comments; lava OnFire buff 24/420 missing (noted); non-vanilla white flash brightness(2.5) (Renderer.ts:5940).
13. 死亡表现 — ours: red particles + NPC_Killed_1 + respawn via 7200t arrival cycle ✓ (cadence matches Main.cs:65021-65040); missing: per-type gore pieces (HitEffect), vanilla re-runs QuickFindHome each cycle (:65079-65083) vs ours only houses homeless.
14. 对话气泡指示标 — vanilla notification icon over NPC with pending dialogue (FreeCake) or homeless (<105px) (Main.cs:45484-45495, NPC.cs:96048-96060); ours: none.
15. 坐椅占位缺玩家检查 (:55790-55797) — ours forceSit only checks NPCs (TownNPC.ts:1339-1346).
16. sittingManager.AddNPC 座位叠坐 index (:54701) — registered skipped in our comments; low impact.

**对齐项 ✓:**
- 睡觉: 原版城镇 NPC 无睡眠行为 (NPC.cs 无 sleep 引用; sleepingManager 仅玩家) → 我们也没有 ✓
- 坐椅核心链: 夜椅扫描 FindGoodRestingSpot ±7列/+2..-6行/曼哈顿最近 ✓ (TownNPC.ts:71-92); TryForcingSitting 门(椅15/马桶497/style27排除帧带1080-1098/占位) ✓ (:48-59, 1333-1355); 入座 900+rand(10800)/朝向 frameX/锚点 ✓; 椅子被拆起身 ✓; 时限起身冷却 ✓; 免站定门(teleportedHome) ✓
- 微光转化/上升态 ai[0]=25 ✓ 1:1
- 自卫攻击四态(10/12/14/15)+持械视觉+进度强化链+633狼人 ✓ (已审)
- 开关门 ✓ (1/10 撞门开门两向回退/过门>2格关/±4放弃/高门 388/389)
- 夜间回家走位 ✓ 近似; 回家传送三列落位(0,-1,1 同序)+头顶净空 ✓
- 对话系统 GetChat/名字替换/特殊事件文案/FreeCake ✓ 1:1
- 快乐度/住房/入驻轮 7200t ✓
- 派对帽(含坐姿帽Y修正链) ✓; 派对商品上架 ✓; 原版无购物折扣 ✓
- 玩家推挤: 原版无此行为 ✓ 我们也无
- 环境受击三件套(岩浆30t/50伤、溺水7t呼吸、敌怪互殴30t/kb6) ✓
- 受击护头姿态: 原版无 cower 帧(危险冻结 state 8 = 站立帧) — 我们无特殊姿态 ✓对齐(但 state 8 本身缺失归入#1)
- 死亡重生节奏 7200t ✓

Wait — I should double-check #12 iframes: vanilla town NPC hit by enemy contact: GetHurtByOtherNPCs sets immune[255]=30 — ours npcVsCd=30 ✓. Player projectile hits town NPC → immune[owner]=10. Ours iframes=8 — only traps path. Minor.

Also should double check: does our town NPC get hit by player weapons at all? (vanilla: player attacks don't hit friendly town NPCs except... hmm, actually in vanilla, player projectiles DO hit town NPCs? Let me think — "friendly" NPCs: Projectile.Damage check `!Main.npc[i].friendly` — town NPCs are friendly=true → player projectiles skip them. Weapons: melee hits check friendly too. So town NPCs are invulnerable to player attacks (except RPS? no). Voodoo dolls let you kill guide via WoF. Actually you CAN hurt town NPCs with... thorns? no. In vanilla you cannot damage town NPCs with player attacks directly. Ours: TownNPC.hurt is called from traps/projectiles (TownShot? no). OK skip — outside scope.

One more sanity check for #1 flee: also vanilla flee applies "num22 = 1.5f" only when `friendly && (flag16 || flag21)` (:54319-54326) — note ALL town NPCs are friendly → flee speed boost. And direction away. Also PrettySafe: if nearest danger beyond PrettySafe distance → don't treat as danger (PrettySafe default -1 → check skipped? `if (NPCID.Sets.PrettySafe[type] != -1 && PrettySafe < num20) flag16 = false` — so only NPCs with PrettySafe set (like pirate 228? no — 229? whichever) ignore far dangers.

I'm confident in the audit now. Time to write the final report in Chinese, ordered by severity, with vanilla line evidence + our file:line status + fix specs. Keep it organized but complete.
```

</details>


---

## 🤖 Assistant · 2026-08-17T04:47:29.519Z · glm-x-preview-260804

```
审计完成。以下为城镇 NPC 日常生活行为的对账结果（原版 = Terarria1456 反编译源码，我方 = game/src）。

# 城镇 NPC 生活行为对账报告

## 一、偏离清单（按严重度排序）

### P0-1 危险逃离行为完全缺失（城镇 NPC 站桩打架，不逃跑）
- **原版**：NPC.cs:53884-53958 危险扫描（默认 200px/DangerDetectRange）→ :53960-54024 非攻击态者 `direction = -num15` **背向危险走逃**（感染树妖 flag2 反向追击）；:54319-54326 逃跑提速 `num22=1.5 + 失血比例×0.9`；:54597-54603 障碍挡路且跳不过 → **ai[0]=8 冻结 240t**（受逼墙角僵立）；:53982 PrettySafe 距离外不视为危险；逃跑中仍按概率还击（flag31 含 ai[0]==8）。
- **我方**：`TownNPC.attackUpdate`（TownNPC.ts:1007-1039）只实现了还击，全仓 grep 无 flee/cower 逻辑。
- **修复规格**：attackUpdate 前插危险评估——range 内有敌（!friendly && damage>0 && LOS）→ wantDir=背向最近敌；速度上限临时提至 1.5+0.9×(1-hp/maxHp)；前方悬崖（GetWalkPrediction 语义）则原地站定 240t；同时保留攻击掷骰（冻结态也可打）。

### P0-2 坐姿帧未接（坐下仍是站立贴图）
- **原版**：FindFrame NPC.cs:69638-69644 `ai[0]==5 → frame.Y = num*(num58-3)`（num58 = npcFrameCount − AttackFrameCount；637 例外=帧19）。同族缺：派对舞帧 num58-5/-4（:69645-69700）、聊天帧 num58-1/-2 交替（:69865+）、攻击帧 num58..+3（:69776-69817）、弓瞄准帧 `num58+GetShootingFrame(ai[2])`（:69827，GetShootingFrame :67061）。
- **我方**：`updateWalkFrame`（TownNPC.ts:804-822）只产 0/1/2..行走帧，坐姿/攻击/聊天全落帧0；Renderer.drawTownNPC（Renderer.ts:5878+）直接消费 n.frame。
- **修复规格**：sitting=true → frame = frames − AttackFrameCount − 3；attackState 10/13 按 atkTick 分四档攻击帧、12 按 holdAim 查 GetShootingFrame 表、15 按 atkTimer/AttackTime 比例四档。

### P1-3 白天随机坐椅缺失（原版城镇 NPC 白天也会坐椅子）
- **原版**：NPC.cs:55774-55814 行走态（ai[0]==1）每 tick `rand(num)==0`（num=300，:53372-53376）→ 脚下格（Bottom−2px）为椅15/马桶497 且无其他坐姿 NPC（:55777-55789）**且无玩家坐着**（:55790-55797）→ 坐 900+rand(10800)。**无昼夜门**。
- **我方**：TownNPC.ts:680-682 restSpot 仅 `!isDay` 才扫 → 白天永坐不了。
- **修复规格**：白天在 fixedUpdate 游走态补一路：站地且脚下格 canSitAt 且 rand(300)==0 且占位门（含玩家坐姿格比对）→ forceSit。

### P1-4 悬崖/坑洞避让 + 溺水逃生缺失（NPC 会走下平台掉坑）
- **原版**：AI_007_TownEntities_GetWalkPrediction NPC.cs:56093-56170（前视 tileX 列扫 -1..+4 行：实心落地则放行、岩浆/深水/脚高以上水位→avoidFalling）；:54468-54484 avoidFalling 且脚下 3 列仅≤2 实心 → 停走站定；:54444-54467 溺水按水深算跳速 `−sqrt(depth×2×0.3)`（cap 26）跃出水面；:54646 `vy<0 && wet → vy×1.2`。
- **我方**：无任何边缘检查（TownNPC.ts:695-710 游走 + 787 跳跃）。
- **修复规格**：走路意图施加前查前方 1 格脚下扫描（复用 findChairSpot 同款 TileStore 读法）；无落点→wantDir=0 并 wanderT=50+rand(50)；头部浸水且前方水 → 按上式 vy 跃出。

### P1-5 回家传送的玩家视野阈值过小（NPC 在玩家眼前消失）
- **原版**：触发 :53830-53856，可见性判定矩形 = sWidth=1920 × sHeight=1200 + safeRange 边距（:53835-53847；`sWidth => 1920` :6695-6697），在 NPC 位与 home 位各测一次——即玩家须离 NPC/home 约**一整个屏幕**外才传送。落位失败 → `homeless=true + QuickFindHome`（:56087-56089）。
- **我方**：TownNPC.ts:736-741 用 42 格（672px）圆形判定——约原版阈值的 1/3，玩家还看得见 NPC 就瞬移走了；三列落位失败仅放弃（无 QuickFindHome 回退）。
- **修复规格**：改矩形判定（半宽 60 格、半高 37.5 格级）；全堵时置 homeless 并走找房（复用 findFreeHouse）。

### P1-6 游走节奏/速度/拴绳常量全面偏离
- **原版**：走速 max 1.0/加速 0.07（:54280-54281）；走程 200-500t（:54142 起 300+Next(300)+Next(900) 停程 :54235）；随机转身 1/80/锁 200t 且仅限 home±25 内（:54195-54201）；拴绳 ±25 格软界、±50 格强制折返（:54181-54199）；背离 home >±35 格时倒计时额外 −5/t（:54217-54224）；无家者首落地锚定 homeTile 就地游走（:53704-53706）。
- **我方**：TownNPC.ts:703-709（wanderT=90+rand(180) 双态共用、35% 原地、无转身锁）、:777-778（0.06/±0.8）、:699-701（仅 leashHome 者有 10 格拴绳；无家者无锚）。
- **修复规格**：速度 0.07/1.0；走/停两计时分开（走 200+rand(300)、停 300+rand(300)+rand(900)）；home±25 内 rand(80) 转身；超 ±50 强制朝家；无家 NPC 首次落地记录锚点。

### P1-7 越障跳跃只有一档、卡墙不折返
- **原版**：三档跳 −6/−5/−4.4（按障碍 2 格/1 格/半格，:54523/54534/54543），且先做头顶净空检查（SolidTilesVersatile）——**跳不过就转身**（:54525-54551 flag26/27）；StepUp 无位移且 ai[1]<100 每 10t 强制折返（:54409-54422）；同位防卡（:54485-54490）。
- **我方**：TownNPC.ts:787 单档 `vy=-6` 撞墙就跳 → 对高墙反复跳跃永不离开。
- **修复规格**：按前方第 2/1/半格实心分档取速；头顶 5 格净空检查失败 → facing 取反 + vx 取反；开门成功后走程 +80t（:54578）。

### P1-8 社交系统大幅简化（错表情池、错触发节奏）
- **原版**：每 NPC 每 tick 掷骰——结对聊天 3/4：1/300（:55647）距 20-100px+LOS，时长 420×(1..3 或 1..4)，聊天帧交替；结对聊天 16/17：1/1800（:55674）＝**石头剪刀布表情 36/37/38 镜像对局**（FindFrame :70030-70135）；面向玩家 7：1/1200（:55760-55780）220t＋tick16 冒 NPC 头像气泡（NewBubbleNPC 112）；发呆 2：1/1800（:55752）45t＋睡意表情 89＋帧 num58-1；酒保 18：1/600；驻足看家具 9：1/600（:55817，InteractableByNPCs 前方格）。禁触条件=水湿/带门行走/对玩家说话中。
- **我方**：Game.ts:13978-14011 tickNpcEmotes——**全局每 600t 挑一对**、表情池 [25猩红群系,90镐,100火,87困惑,89睡]（内容错位：应为 RPS 36/37/38 与头像 112）、仅白天跑、无聊天帧、无面向玩家/看家具态。
- **修复规格**：改为每 NPC 每 tick 独立掷骰四类社交（数值同上）；表情池换 36/37/38（RPS 对局按原版镜像逻辑）与 89/112；去掉 isDay 门；补“驻足看可交互家具”态（前方 10px 格 InteractableByNPCs，40+rand(90)t）。

### P1-9 派对期间无跳舞
- **原版**：NPC.cs:55704-55730 派对女孩恒 1/1200、**派对进行中全部 AttackType==0 城镇 NPC** 同门 → ai[0]=6 跳舞 300t（舞帧 num58-5/-4 交替 + 音符尘 139-143，FindFrame :69645-69700），触发需玩家 150px 内+LOS。
- **我方**：无（派对帽 ✓、派对商品上架 ✓ Game.ts shopCondOk 'party'、FreeCake ✓）。
- **修复规格**：派对旗（partyState）期间在社交掷骰链补 ai0=6 等价态：站定 300t + 舞帧 + 每 30t 音符尘。

### P2-10 白天雨不回家
- 原版 flag（:53383-53402）含**白天雨**→ 有房者走/传送回家（白天不坐椅只站家里）；我方走回家分支被 `isDay` 挡（TownNPC.ts:695），只有玩家远时传送生效。修复：走家分支的门从 `!isDay` 改为 `sitFlag`（raining||!isDay||eclipse||slimeRain||风暴地表）。

### P2-11 城镇 NPC 液体物理缺失
- 原版全 NPC 通用：浸水 gravity 0.2/maxFall 7、蜂蜜 0.1/4、微光 0.15/5.5（:91928-91942）+ 水中位移×0.5/蜂蜜×0.25（:5946-5952 + Collision_MoveWhileWet :93986）。我方 TownNPC 恒用 GRAVITY/MAX_FALL_SPEED（TownNPC.ts:641,788），Enemy 侧已有 npcLiquid.ts 可直接复用。

### P2-12 受击细节
- 无敌帧 8 vs 原版 10（TownNPC.ts:462）；击退为 `vx+=kb×0.6` 叠加，原版为直接设定式；**Boss 进度防御链**（+2..+20，:53437-53532，我方 hurt 只叠战斗书+8，TownNPC.ts:458-459，注释已登记“另批”）；岩浆 OnFire buff24/420 未接（已登记）；Renderer.ts:5940 `brightness(2.5)` 受击闪白为**原版没有**的视觉（原版只有血尘+飘字）。

### P2-13 死亡表现与家复核
- 重生节奏 ✓（7200t 入驻轮，对应 Main.cs:65021-65040）。缺：各类型 gore 碎块（HitEffect 分支）用红色粒子近似；原版每轮对全部有房 NPC 重跑 QuickFindHome（:65079-65083），我方只给无家者找房（Game.ts:12794-12804）。

### P2-14 对话指示标缺失
- 原版 NPC 头顶在“有待触发对话（FreeCake）”或“无家可归（玩家 105px 内）”时画通知图标（Main.cs:45484-45495、NPC.cs:96048-96060、CheckDialogue :91577-91588）。我方无。

### P3-15 其他小项
- 坐椅占位门缺“玩家正坐同椅”检查（:55790-55797；我方 forceSit 只查 NPC，TownNPC.ts:1339-1346）；关门触发我方把 y 位移>4 也当“过门”条件（原版仅 x>±2 关门、y>±4 是放弃，TownNPC.ts:1248）；sittingManager 叠坐 index（:54701）无渲染载体（我方注释已登记，视觉影响≈0）。

## 二、已对齐项 ✓

1. **睡觉**：原版城镇 NPC **无睡眠行为**（NPC.cs 全文无 sleep；sleepingManager 仅玩家，Main.cs:6421/17679）→ 我方无 ✓。
2. **坐椅核心链**：夜椅扫描 FindGoodRestingSpot（±7 列×{+2,0,-2,-4,-6} 行、曼哈顿最近、frameY%40 上下格归一，TownNPC.ts:71-92 对照 :53195-53262）✓；TryForcingSitting 门（椅15/马桶497、style27 帧带 1080-1098 排除、NPC 占位互斥，:48-59/:1333-1355）✓；入座 900+rand(10800)/朝向 frameX/锚点 (x*16+8+2*dir, y*16) ✓；椅被拆即起身（:54691-69697）✓；传送落位免站定门（:56081）✓；坐姿帽 Y 修正链（Main.cs:26965-26987）✓。
3. **微光城镇转化**：ai[0]=25 上升态全链（触发/落点传送/−4×st 上浮/粒子/成就43/双向翻转，TownNPC.ts:156-185, 824-923 对照 :53594-53682/:92561-92573）✓。
4. **自卫攻击**：四态 10/12/14/15 + 持械视觉（DrawNPCExtras）+ 进度强化链 num2/num3（含战斗书/17 Boss 旗/tipsy）+ 633 狼人 + 160/663 落点弹重掷 + 441 Andrew 特典 ✓（前批已审，本次复核无新偏离）。
5. **开门/关门**：1/10 撞门开门两向回退、高门 388/389 ShiftTallGate、过门 >2 格关、>4 格放弃 ✓（TownNPC.ts:1240-1290 对照 :54237-54277/:54552-54590，仅 P3-15 的 y 条件小差）。
6. **夜间回家走位/传送三列落位**（0,-1,+1 同序 + 头顶 3×3 净空，TownNPC.ts:745-759 对照 :56063-56086）✓。
7. **对话系统**：GetChat 各类型分支/血月/灯笼夜/日食/在场互 cue/名字替换（Game.NPCTitle）/FreeCake 优先级 ✓ 1:1（Game.ts:13324+）。
8. **派对**：派对帽+坐姿帽修正 ✓、派对专属商品上架（含 5643 族）✓、**原版无购物折扣**（Chest.cs 派对只加库存）——无需实现 ✓。
9. **玩家推挤**：原版无玩家推 NPC/无 NPC 互推物理（仅 GetWalkPrediction 的“友方挡路则停”路径语义）→ 我方同样无 ✓。
10. **受击护头/防御姿态**：原版无 cower 帧（危险冻结 state 8 就是站立帧）→ 无需实现（state 8 行为本体归 P0-1）✓。
11. **环境受击三件套**：岩浆 30t 冷却/50 直伤、溺水 7t 呼吸节律/致死一击、敌怪互殴 30t/kb6（TownNPC.ts:934-982 对照 :94511-94530/:96118-96154/:93605-93690）✓。
12. **入驻/重生节奏**：7200t 周期 + 优先级链 + 锚池空即 return（Game.ts:12761+ 对照 Main.cs:65021-65574）✓。

## 三、总结

最核心的两条肉眼可见缺口是**危险逃离**（P0-1，城镇 NPC 应跑应缩，我方站桩对射）与**坐姿帧**（P0-2，坐下仍站立贴图）；其次是白天坐椅、悬崖避让、社交掷骰节奏/表情内容（RPS 对局）、派对跳舞这四个 1.4.x 标志性生活行为。坐椅数据链、微光、攻击、对话、派对帽/商品等主体框架已相当扎实，偏离集中在“帧动画层”与“游走物理层”两块。
```
