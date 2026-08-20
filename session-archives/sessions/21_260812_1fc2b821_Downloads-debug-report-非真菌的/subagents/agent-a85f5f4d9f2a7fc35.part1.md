# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-19T08:50:24.240Z

```
可写任务:为 ~/Project/GLM/SandboxWorld/game 补四组,标杆 ~/Project/GLM/SandboxWorld/Terarria1456/NPC.cs。

【一、光女白天暴怒 expert 循环+case11(NPC.cs:47053-47103)】
我方 src/entities/bossAI_lategame.ts 光女段(读现状:选招表 P1/P2 已 1:1)。原版 flag2(isExpert‖dayEnrage)把二阶段表切成 10 槽 expert 表 [7,2,8,11,5,2,6,4,8,12](含 case11)。实装:①表按 flag2 切换(白天/专家时用 expert 表);②case11=预测型光枪墙:读 :47053-47103 逐行(919 光枪墙的预测变体:沿玩家速度预测线生成一排 919 预告→延时突进;具体参数照抄)——我们 919 已有收敛实现(直飞 12 速),case11 用同弹型+预测落点排布。
【二、猪鲨 FindFrame 状态机(NPC.cs:72824-72910)】
我方 bossAI_duke_moonlord.ts duke 段+Renderer。原版:0-5 游动帧(5t/帧按 |vx| 累计/4t 冲撞中)、冲撞与计时窗(状态 1/6 冲撞/3 龙卷蓄力)出 6/7 张口帧。修法:duke AI 侧写 e.customFrameIdx(694 先例)或 Renderer 加 case 370(读 ai0 态+animT);8 帧。
【三、WoF 死时三机械旗齐 misc[32](NPC.cs:80287-80290)】
我方 Game.ts 肉山死亡链(搜 SpawnWOF/113 死/StartHardmode):补"downed_125&&downed_127&&downed_134 全齐且 !hardMode → 公告 misc[32]"(drunk/FTW 边缘)。查我们 misc 公告 API(boss-summon 链 Lang.misc)。
【四、火星专家弹伤插值】
bossAI_martian.ts 部件射击(448/449/450/435):包 getAttackDamageForProjectiles(classic, expert 档)——原版 Remap:448 50→37/449 35→30/450 30→25/435 35→28(bossAI.ts 有 import 先例;各调用点 dmg 参数换算)。

【验收】npx tsc --noEmit 零新错(基线既有错忽略);npx vitest run tests/bossAI-lategame.test.ts tests/bossAI-dd2.test.ts tests/boss-hostile-proj-sim.test.ts tests/eoc-dash-speed.test.ts(存在哪些跑哪些)全绿;逐项带行号注释。禁止动光女状态机主链/猪鲨 AI 本体。完成后报告:四组落点+测试。
```

---

## 📎 Attachment · skill_listing · 2026-08-19T08:50:24.244Z

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

## 🤖 Assistant · 2026-08-19T08:50:39.827Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me break down this task. I need to implement four groups of features in ~/Project/GLM/SandboxWorld/game, with the reference being ~/Project/GLM/SandboxWorld/Terarria1456/NPC.cs.

1. **Empress of Light daytime enraged expert cycle + case11 (NPC.cs:47053-47103)**:
   - Our file: src/entities/bossAI_lategame.ts (Empress of Light section)
   - Vanilla flag2 (isExpert || dayEnrage) switches the second-phase attack table to a 10-slot expert table [7,2,8,11,5,2,6,4,8,12] (includes case11)
   - Implement: ① table switches on flag2 (day/expert uses expert table); ② case11 = predictive light lance wall: read lines 47053-47103 line by line (predictive variant of 919 light lance wall: generate a row of 919 telegraphs along the player velocity prediction line → delayed dash; copy exact parameters) — our 919 already has a convergent implementation (straight flight speed 12), case11 uses same projectile type + predicted landing arrangement.

2. **Duke Fishron FindFrame state machine (NPC.cs:72824-72910)**:
   - Our files: bossAI_duke_moonlord.ts duke section + Renderer
   - Vanilla: 0-5 swim frames (5t/frame by |vx| accumulation / 4t during dash), dash & timer windows (state 1/6 dash / 3 tornado charge) show 6/7 open-mouth frames
   - Fix: duke AI side writes e.customFrameIdx (694 precedent) or Renderer adds case 370 (read ai0 state + animT); 8 frames total.

3. **WoF death: three mechanical boss flags all in misc[32] (NPC.cs:80287-80290)**:
   - Our Game.ts Wall of Flesh death chain (search SpawnWOF/113 death/StartHardmode): add "downed_125&&downed_127&&downed_134 all present and !hardMode → announce misc[32]" (drunk/FTW edge). Check our misc announcement API (boss-summon chain Lang.misc).

4. **Martian expert projectile damage interpolation**:
   - bossAI_martian.ts part shooting (448/449/450/435): wrap getAttackDamageForProjectiles (classic, expert tiers) — vanilla Remap: 448 50→37/449 35→30/450 30→25/435 35→28 (bossAI.ts has import precedent; convert dmg params at each call site).

Acceptance: npx tsc --noEmit zero new errors (ignore baseline errors); npx vitest run tests/bossAI-lategame.test.ts tests/bossAI-dd2.test.ts tests/boss-hostile-proj-sim.test.ts tests/eoc-dash-speed.test.ts (run whichever exist) all green; line-number comments per item. Forbidden: touching Empress of Light state machine main chain / Duke AI core. Report: four group locations + tests.

Let me start by reading the reference decompiled source and our current implementations. Let me first look at the NPC.cs reference sections and our files in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:50:40.307Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/src/entities/ | head -50",
 "description": "List entities directory files"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:50:40.414Z

**📎 ToolResult**

```
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
LightningBoltProj.ts
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
PoopProj.ts
Portal.ts
PortalGunBolt.ts
PrismProj.ts
projStatus.ts
projTargets.ts
RainbowProj.ts

```


---

## 🤖 Assistant · 2026-08-19T08:50:40.875Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/NPC.cs",
 "offset": 47040,
 "limit": 80
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:50:40.887Z

**📎 ToolResult ⚠️ERROR**

```
File does not exist. Note: your current working directory is ~/Project/GLM/SandboxWorld/game.

```


---

## 🤖 Assistant · 2026-08-19T08:50:45.259Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The NPC.cs path failed. Let me find the correct path. The additional working directory is `~/Project/GLM/SandboxWorld/Terarria1456/Terrar*` — probably `Terarria1456/Terraria` or similar. Let me check.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:50:46.540Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls -d ~/Project/GLM/SandboxWorld/Terarria1456/*/ 2>/dev/null; find ~/Project/GLM/SandboxWorld/Terarria1456 -maxdepth 3 -name \"NPC.cs\" 2>/dev/null | head",
 "description": "Locate NPC.cs in decompiled source"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:50:46.618Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/BCrypt.Net/
~/Project/GLM/SandboxWorld/Terarria1456/Properties/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Achievements/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Audio/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Chat.Commands/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Chat/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Cinematics/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Enums/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Achievements/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Ambience/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Animations/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Bestiary/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.CaveHouse/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes.Desert/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Biomes/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Creative/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Dyes/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Events/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.FishDropRules/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Entrances/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Halls/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.LayoutProviders/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Rooms/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Golf/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.ItemDropRules/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Items/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.LeashedEntities/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Liquid/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.LootSimulation.LootSimulatorConditionSetterTypes/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.LootSimulation/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Metadata/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.NetModules/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.ObjectInteractions/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Personalities/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Prefixes/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.RGB/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Shaders/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Skies.CreditsRoll/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Skies/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Tile_Entities/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.BigProgressBar/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Chat/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Minimap/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.ResourceSets/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.States/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameInput/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.CameraModifiers/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Capture/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Effects/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Renderers/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Shaders/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Initializers/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.IO/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Localization/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Map/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Modules/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Net.Sockets/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Net/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ObjectData/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Physics/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Server/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Social.Base/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Social.Steam/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Social.WeGame/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Social/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Testing.ChatCommands/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Testing/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.UI.Chat/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.UI.Gamepad/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.UI/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Utilities.FileBrowser/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Utilities.Terraria.Utilities/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Utilities/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.WorldBuilding/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs

```


---

## 🤖 Assistant · 2026-08-19T08:50:50.521Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The NPC.cs is at `~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs`. Let me read the four reference sections in parallel:
1. NPC.cs:47053-47103 (Empress of Light case11 + expert table)
2. NPC.cs:72824-72910 (Duke Fishron FindFrame)
3. NPC.cs:80287-80290 (WoF death misc[32])

Also I need to see a bit more context for the Empress table switch (flag2). Let me read those.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:50:51.125Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 130,
 "offset": 46990
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:50:51.172Z

**📎 ToolResult**

```
46990				flag6 = !(this.ai[1] >= 6f) || !(this.ai[1] <= 40f);
46991				int num33 = ((this.ai[0] != 8f) ? 1 : (-1));
46992				AI_120_HallowBoss_DoMagicEffect(base.Center, 5, Utils.GetLerpValue(40f, 90f, this.ai[1], clamped: true));
46993				if (this.ai[1] <= 40f)
46994				{
46995					if (this.ai[1] == 20f)
46996					{
46997						SoundEngine.PlaySound(SoundID.Item160, base.Center);
46998					}
46999					NPCAimedTarget targetData3 = GetTargetData();
47000					Vector2 destination = (targetData3.Invalid ? base.Center : targetData3.Center) + new Vector2(num33 * -550, 0f);
47001					SimpleFlyMovement(DirectionTo(destination).SafeNormalize(Vector2.Zero) * num2, num * 2f);
47002					if (this.ai[1] == 40f)
47003					{
47004						velocity *= 0.3f;
47005					}
47006				}
47007				else if (this.ai[1] <= 90f)
47008				{
47009					velocity = Vector2.Lerp(value2: new Vector2(num33 * 50, 0f), value1: velocity, amount: 0.05f);
47010					if (this.ai[1] == 90f)
47011					{
47012						velocity *= 0.7f;
47013					}
47014					num16 *= 1.5f;
47015				}
47016				else
47017				{
47018					velocity *= 0.92f;
47019				}
47020				this.ai[1] += 1f;
47021				if (this.ai[1] >= 90f + num32)
47022				{
47023					this.ai[0] = 1f;
47024					this.ai[1] = 0f;
47025					netUpdate = true;
47026				}
47027				break;
47028			}
47029			case 10:
47030			{
47031				float num94 = 20 - num17;
47032				if (this.ai[1] == 0f)
47033				{
47034					SoundEngine.PlaySound(SoundID.Item161, base.Center);
47035				}
47036				flag6 = !(this.ai[1] >= 30f) || !(this.ai[1] <= 170f);
47037				velocity *= 0.95f;
47038				if (this.ai[1] == 90f)
47039				{
47040					if (this.ai[3] == 0f)
47041					{
47042						this.ai[3] = 1f;
47043					}
47044					if (this.ai[3] == 2f)
47045					{
47046						this.ai[3] = 3f;
47047					}
47048					base.Center = GetTargetData().Center + new Vector2(0f, -250f);
47049					netUpdate = true;
47050				}
47051				this.ai[1] += 1f;
47052				if (this.ai[1] >= 180f + num94)
47053				{
47054					this.ai[0] = 1f;
47055					this.ai[1] = 0f;
47056					this.ai[2] = 0f;
47057					netUpdate = true;
47058				}
47059				break;
47060			}
47061			case 11:
47062			{
47063				if (this.ai[1] == 0f)
47064				{
47065					SoundEngine.PlaySound(SoundID.Item162, base.Center);
47066				}
47067				float num58 = 20 - num17;
47068				new Vector2(0f, -100f);
47069				if (this.ai[1] >= 6f && this.ai[1] < 54f)
47070				{
47071					AI_120_HallowBoss_DoMagicEffect(base.Center + new Vector2(-55f, -20f), 2, Utils.GetLerpValue(0f, 100f, this.ai[1], clamped: true));
47072					AI_120_HallowBoss_DoMagicEffect(base.Center + new Vector2(55f, -20f), 4, Utils.GetLerpValue(0f, 100f, this.ai[1], clamped: true));
47073				}
47074				NPCAimedTarget targetData6 = GetTargetData();
47075				Vector2 vector12 = (targetData6.Invalid ? base.Center : targetData6.Center);
47076				if (Distance(vector12 + vector3) > num3)
47077				{
47078					SimpleFlyMovement(DirectionTo(vector12 + vector3).SafeNormalize(Vector2.Zero) * num2, num);
47079				}
47080				if ((int)this.ai[1] % 3 == 0 && this.ai[1] < 100f)
47081				{
47082					int num59 = 1;
47083					for (int k = 0; k < num59; k++)
47084					{
47085						Vector2 v = -targetData6.Velocity;
47086						v = v.SafeNormalize(-Vector2.UnitY);
47087						float num60 = 100f;
47088						Vector2 center2 = targetData6.Center;
47089						if (Distance(center2) > 2400f)
47090						{
47091							continue;
47092						}
47093						int num61 = 90;
47094						Vector2 vector13 = center2 + targetData6.Velocity * num61;
47095						Vector2 vector14 = center2 + v * num60;
47096						if (vector14.Distance(center2) < num60)
47097						{
47098							Vector2 vector15 = center2 - vector14;
47099							if (vector15 == Vector2.Zero)
47100							{
47101								vector15 = v;
47102							}
47103							vector14 = center2 - Vector2.Normalize(vector15) * num60;
47104						}
47105						Vector2 v2 = vector13 - vector14;
47106						if (Main.netMode != 1)
47107						{
47108							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector14, Vector2.Zero, 919, num6, 0f, Main.myPlayer, v2.ToRotation(), this.ai[1] / 100f);
47109						}
47110						if (Main.netMode == 1)
47111						{
47112							continue;
47113						}
47114						int num62 = (int)(this.ai[1] / 3f);
47115						for (int l = 0; l < 255; l++)
47116						{
47117							if (!Boss_CanShootExtraAt(l, num62 % 3, 3, 2400f))
47118							{
47119								continue;

```


---

## 🤖 Assistant · 2026-08-19T08:50:51.683Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 100,
 "offset": 72820
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:50:51.702Z

**📎 ToolResult**

```
72820			case 372:
72821			case 373:
72822				frame.Y = num;
72823				break;
72824			case 370:
72825			{
72826				if (ai[0] == 0f || ai[0] == 5f)
72827				{
72828					int num51 = 5;
72829					if (ai[0] == 5f)
72830					{
72831						num51 = 4;
72832					}
72833					frameCounter += 1.0;
72834					if (frameCounter > (double)num51)
72835					{
72836						frameCounter = 0.0;
72837						frame.Y += num;
72838					}
72839					if (frame.Y >= num * 6)
72840					{
72841						frame.Y = 0;
72842					}
72843				}
72844				if (ai[0] == 1f || ai[0] == 6f)
72845				{
72846					if (ai[2] < 10f)
72847					{
72848						frame.Y = num * 6;
72849					}
72850					else
72851					{
72852						frame.Y = num * 7;
72853					}
72854				}
72855				if (ai[0] == 2f || ai[0] == 7f)
72856				{
72857					if (ai[2] < 10f)
72858					{
72859						frame.Y = num * 6;
72860					}
72861					else
72862					{
72863						frame.Y = num * 7;
72864					}
72865				}
72866				if (ai[0] == 3f || ai[0] == 8f || ai[0] == -1f)
72867				{
72868					int num52 = 90;
72869					if (ai[2] < (float)(num52 - 30) || ai[2] > (float)(num52 - 10))
72870					{
72871						frameCounter += 1.0;
72872						if (frameCounter > 5.0)
72873						{
72874							frameCounter = 0.0;
72875							frame.Y += num;
72876						}
72877						if (frame.Y >= num * 6)
72878						{
72879							frame.Y = 0;
72880						}
72881					}
72882					else
72883					{
72884						frame.Y = num * 6;
72885						if (ai[2] > (float)(num52 - 20) && ai[2] < (float)(num52 - 15))
72886						{
72887							frame.Y = num * 7;
72888						}
72889					}
72890				}
72891				if (ai[0] != 4f && ai[0] != 9f)
72892				{
72893					break;
72894				}
72895				int num53 = 180;
72896				if (ai[2] < (float)(num53 - 60) || ai[2] > (float)(num53 - 20))
72897				{
72898					frameCounter += 1.0;
72899					if (frameCounter > 5.0)
72900					{
72901						frameCounter = 0.0;
72902						frame.Y += num;
72903					}
72904					if (frame.Y >= num * 6)
72905					{
72906						frame.Y = 0;
72907					}
72908				}
72909				else
72910				{
72911					frame.Y = num * 6;
72912					if (ai[2] > (float)(num53 - 50) && ai[2] < (float)(num53 - 25))
72913					{
72914						frame.Y = num * 7;
72915					}
72916				}
72917				break;
72918			}
72919			case 359:

```


---

## 🤖 Assistant · 2026-08-19T08:50:52.333Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 60,
 "offset": 80240
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:50:52.346Z

**📎 ToolResult**

```
80240			}
80241			case 4:
80242				SetEventFlagCleared(ref downedBoss1, 13);
80243				break;
80244			case 13:
80245			case 14:
80246			case 15:
80247			case 266:
80248				if (boss)
80249				{
80250					if (WorldGen.Skyblock.lowTiles)
80251					{
80252						WorldGen.shadowOrbSmashed = true;
80253					}
80254					if (!downedBoss2 || Main.rand.Next(2) == 0)
80255					{
80256						WorldGen.spawnMeteor = true;
80257					}
80258					SetEventFlagCleared(ref downedBoss2, 14);
80259				}
80260				break;
80261			case 35:
80262				if (boss)
80263				{
80264					SetEventFlagCleared(ref downedBoss3, 15);
80265				}
80266				break;
80267			case 127:
80268				if (boss)
80269				{
80270					SetEventFlagCleared(ref downedMechBoss3, 18);
80271					downedMechBossAny = true;
80272				}
80273				break;
80274			case 134:
80275				if (boss)
80276				{
80277					SetEventFlagCleared(ref downedMechBoss1, 16);
80278					downedMechBossAny = true;
80279				}
80280				break;
80281			case 113:
80282				if (Main.netMode != 1)
80283				{
80284					CreateBrickBoxForWallOfFlesh();
80285					bool eventFlag = Main.hardMode;
80286					WorldGen.StartHardmode();
80287					if (downedMechBoss1 && downedMechBoss2 && downedMechBoss3 && !eventFlag)
80288					{
80289						ChatHelper.BroadcastChatMessage(NetworkText.FromKey(Lang.misc[32].Key), ChatColors.World);
80290					}
80291					SetEventFlagCleared(ref eventFlag, 19);
80292				}
80293				break;
80294			case 661:
80295				if (Main.netMode != 1 && GetWereThereAnyInteractions())
80296				{
80297					int num = 636;
80298					if (!AnyNPCs(num))
80299					{

```


---

## 🤖 Assistant · 2026-08-19T08:51:35.289Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Good, I got three of the four references. Now I need:

1. The Empress of Light flag2 expert attack table switch (before line 47053, in the attack selection logic). Let me search for the table with [7,2,8,11,5,2,6,4,8,12]. Let me search around line 46300-46600 probably where the attack selection is.

2. Continue reading case 11 lines 47119-47180 or so to see the rest.

3. Martian projectile damage Remap — I should check where in vanilla the martian parts shoot. The task says "bossAI.ts 有 import 先例" (bossAI.ts has an import precedent for getAttackDamageForProjectiles). Let me look at the call sites for NPC.NewProjectile with 448/449/450/435 damage remap. Actually the task gives exact values: 448 50→37/449 35→30/450 30→25/435 35→28. These are `Utils.Remap(num, 0f, 1f, 50, 37)` style — i.e. classic → expert interpolation. In vanilla, the pattern is `int num = (int)Utils.Remap(GetAttackDamageForProjectiles(classValue, expertValue), 0f, 1f, classicMin, expertMin)`? Hmm, actually the typical pattern in 1.4.5 is:

```csharp
float num = GetAttackDamageForProjectiles(35, 30); // classic, expert
```

Wait no — GetAttackDamageForProjectiles(int damageInNormal, int damageInExpert) returns the remapped value based on difficulty. But the task mentions "Remap:448 50→37" — so the pattern is like `Utils.Remap(GetLifeScale... )`. Let me search vanilla for the martian scanner/Tesla damage to be sure. Actually the task says "包 getAttackDamageForProjectiles(classic, expert 档)——原版 Remap:448 50→37/449 35→30/450 30→25/435 35→28". So for projectile type 448 (Martian Saucer laser?) damage = Remap from 50 (classic) to 37 (expert)? Hmm wait, that's backwards: expert damage should be higher than classic in Terraria... Actually no! For martian saucer lasers: in normal mode the laser does more damage than expert? Let me check vanilla code.

Actually in vanilla 1.4, many boss projectiles have LOWER damage in expert master because boss HP/difficulty scaling works differently... No wait. In Terraria, expert mode increases enemy damage generally via NPC.damage scaling, but projectile damage is explicitly set via NewProjectile and vanilla often has `int num = Utils.Remap(...)` patterns like:

```csharp
int damage = Utils.Remap(Main.masterMode ? ... )
```

Hmm, let me actually grep the vanilla source for these. Let me search for "GetAttackDamageForProjectiles" in NPC.cs and for the martian saucer section (NPC 439? The Martian Saucer is NPC 439, Tesla coil etc are 440-443? Actually: 439 Martian Saucer, 440 Martian Saucer Turret?, 441 Scutlix... let me not guess — grep).

Actually wait: the projectile IDs 448/449/450 are Martian Saucer projectiles (Ray gunner?), 435 is Martian turret blast. And NPC ids: 439 = Martian Saucer, 440 = Saucer Turret(?), 441 = Tesla Coil, 442 = Deathray... Hmm. Let me grep vanilla.

The pattern in vanilla 1.4.4+ is:

```csharp
int num = (int)Utils.Remap(GetAttackDamageForProjectiles(), 0f, 1f, 50, 37f);
```

Hmm no. Let me look at actual code. In NPC.cs there's `GetAttackDamageForProjectiles(int projectileDamage, int? projectileDamageExpert = null)`:

```csharp
public int GetAttackDamageForProjectiles(int projectileDamage, int? projectileDamageExpert = null)
{
	float num = 1f;
	if (Main.expertMode)
	{
		num = (projectileDamageExpert.HasValue ? Utils.GetLerpValue(0f, 1f, ...) : ...)
	}
	...
}
```

Actually I recall in 1.4.4:

```csharp
public int GetAttackDamageForProjectiles(int projectileDamage, int? projectileDamageExpert = null)
{
	float num = 1f;
	if (projectileDamageExpert.HasValue)
	{
		float value = Main.masterMode ? 1f : (Main.expertMode ? 0.5f : 0f);
		return (int)Utils.Remap(value, 0f, 1f, projectileDamage, projectileDamageExpert.Value);
	}
	if (!Main.expertMode)
	{
		return projectileDamage;
	}
	return (int)((float)projectileDamage * Main.GameModeInfo.DamageMultiplier)... 
}
```

Something like that. So `Remap(448 50→37)` means: projectile 448 damage = Remap(lerp, 50, 37) where 50 is classic and 37 expert?? That seems inverted (expert weaker). Hmm wait — but maybe it's actually the opposite: classic 37, expert 50? The task says "448 50→37" and "包 getAttackDamageForProjectiles(classic, expert 档)". So call is getAttackDamageForProjectiles(50, 37)? That would mean classic=50, expert=37. Interesting — that IS actually a thing in Terraria: some projectile damages go DOWN in expert/master because the difficulty scaling... hmm, actually no.

Wait, I recall for Martian Saucer: the deathray damage is lower in expert mode than classic! Because in expert mode the deathray fires more often. Let me verify by grepping the vanilla source. Let me grep for "448" near Remap in NPC.cs.

Let me also find:
- The Empress expert attack table (search for flag2 / int[] array with 7,2,8,11 pattern).
- Our current implementations: bossAI_lategame.ts (Empress section), bossAI_duke_moonlord.ts, Game.ts WoF death chain, bossAI_martian.ts.
- bossAI.ts import precedent for getAttackDamageForProjectiles.

Let me do a bunch of greps in parallel.
````

</details>


---

## 🤖 Assistant · 2026-08-19T08:51:37.228Z · glm-x-preview-260804

```
我已经定位到 NPC.cs 位于 `Terarria1456/Terraria/NPC.cs`。现在我来看一下剩余的原版参考章节 —— 光女（Empress）的选招表切换逻辑、case 11 的剩余部分，以及火星人的伤害重映射（damage Remap）模式。
```


---

## 🤖 Assistant · 2026-08-19T08:51:38.142Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"flag2\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | sed -n '1,60p'",
 "description": "Find flag2 usages in NPC.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:51:38.224Z

**📎 ToolResult**

```
1117:				bool flag2 = spawnTileY > Main.UnderworldLayer;
1118:				if (num9 || flag2)
1206:				bool flag2 = true;
1208:				while (flag2)
1211:					flag2 = false;
1214:						flag2 = true;
1218:						flag2 = true;
1222:						flag2 = true;
18451:		bool flag2 = !NPCID.Sets.DontDoHardmodeScaling[type];
18456:				flag2 = false;
18460:				flag2 = false;
18464:				flag2 = false;
18469:			flag2 = false;
18471:		if (!flag2)
18898:				bool flag2 = true;
18903:						flag2 = false;
18908:					flag2 = false;
18910:				if (!flag2 || (!teleportInAir && !Main.tileSolid[Main.tile[num5, i].type]))
18931:							flag2 = false;
18937:				if (flag2)
19042:			bool flag2 = false;
19059:						flag2 = true;
19064:			if (flag2)
19487:		bool flag2 = false;
19501:					flag2 = true;
19531:			if (!flag2)
19588:					if (!flag2)
19911:			bool flag2 = false;
19914:				flag2 = true;
20351:				if (flag2)
20363:			if (this.ai[1] == 0f && flag2)
20537:				if (this.ai[3] == 4f && flag2 && base.Center.Y > Main.player[target].Center.Y)
21906:			bool flag20 = RedHatSkeletronAdjustmentsEnabled();
22008:				if (flag20)
22013:				if (flag20)
22023:					if (flag20)
22041:				if (flag20)
22107:				if (Main.getGoodWorld || flag20)
22113:					if (Main.netMode != 1 && (num173 == 0 || flag20))
22117:						if (flag20)
22175:				if (flag20)
22232:				if (flag20)
22306:			bool flag21 = RedHatSkeletronAdjustmentsEnabled();
22307:			if (flag21)
22317:				if (Main.npc[(int)this.ai[1]].ai[1] != 0f && !flag21)
22371:					if (flag21)
22500:				if (flag21)
22529:					num211 = (flag21 ? (24f / num211) : ((!Main.expertMode) ? (18f / num211) : (21f / num211)));
22551:				if (flag21)
22592:					num215 = (flag21 ? (25f / num215) : ((!Main.expertMode) ? (17f / num215) : (22f / num215)));
23757:				bool flag22 = false;
23763:						flag22 = true;
23794:				if (!flag22)
23823:				if (flag22)
24212:			bool flag23 = false;
24215:				flag23 = true;
24236:					if (flag23)
24262:			if (flag23)
24282:			if (flag23)
24336:				bool flag24 = false;

```


---

## 🤖 Assistant · 2026-08-19T08:51:38.787Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 75,
 "offset": 47119
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:51:38.821Z

**📎 ToolResult**

```
47119								continue;
47120							}
47121							Player player = Main.player[l];
47122							v = -player.velocity;
47123							v = v.SafeNormalize(-Vector2.UnitY);
47124							num60 = 100f;
47125							center2 = player.Center;
47126							num61 = 90;
47127							Vector2 vector16 = center2 + player.velocity * num61;
47128							vector14 = center2 + v * num60;
47129							if (vector14.Distance(center2) < num60)
47130							{
47131								Vector2 vector17 = center2 - vector14;
47132								if (vector17 == Vector2.Zero)
47133								{
47134									vector17 = v;
47135								}
47136								vector14 = center2 - Vector2.Normalize(vector17) * num60;
47137							}
47138							v2 = vector16 - vector14;
47139							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector14, Vector2.Zero, 919, num6, 0f, Main.myPlayer, v2.ToRotation(), this.ai[1] / 100f);
47140						}
47141					}
47142				}
47143				this.ai[1] += 1f;
47144				if (this.ai[1] >= 100f + num58)
47145				{
47146					this.ai[0] = 1f;
47147					this.ai[1] = 0f;
47148					netUpdate = true;
47149				}
47150				break;
47151			}
47152			case 12:
47153			{
47154				float num21 = 90f - (float)num17;
47155				Vector2 vector6 = new Vector2(-55f, -30f);
47156				if (this.ai[1] == 0f)
47157				{
47158					SoundEngine.PlaySound(SoundID.Item165, base.Center);
47159					velocity = new Vector2(0f, -12f);
47160				}
47161				velocity *= 0.95f;
47162				bool flag11 = this.ai[1] < 60f && this.ai[1] >= 10f;
47163				if (flag11)
47164				{
47165					AI_120_HallowBoss_DoMagicEffect(base.Center + vector6, 1, Utils.GetLerpValue(0f, 60f, this.ai[1], clamped: true));
47166				}
47167				int num22 = 6;
47168				if (flag2)
47169				{
47170					num22 = 4;
47171				}
47172				float num23 = (this.ai[1] - 10f) / 50f;
47173				if ((int)this.ai[1] % num22 == 0 && flag11)
47174				{
47175					_ = this.ai[1] / 60f;
47176					Vector2 vector7 = (vector7 = new Vector2(0f, -20f).RotatedBy(MathF.PI * 2f * num23));
47177					if (Main.netMode != 1)
47178					{
47179						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center + vector6, vector7, 873, num8, 0f, Main.myPlayer, target, num23);
47180					}
47181					if (Main.netMode != 1)
47182					{
47183						int num24 = (int)(this.ai[1] % (float)num22);
47184						for (int j = 0; j < 255; j++)
47185						{
47186							if (Boss_CanShootExtraAt(j, num24 % 3, 3, 2400f))
47187							{
47188								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center + vector6, vector7, 873, num8, 0f, Main.myPlayer, j, num23);
47189							}
47190						}
47191					}
47192				}
47193				this.ai[1] += 1f;

```


---

## 🤖 Assistant · 2026-08-19T08:51:46.373Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The flag2 grep didn't hit in the AI_120 section. The flag in the Empress section might be named differently (decompiler naming). Let me look at the beginning of AI_120 (HallowBoss) to find where the second phase attack selection happens. Let me search for "HallowBoss" and the attack selection array.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:51:48.301Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"AI_120\\|HallowBoss\" ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria/NPC.cs | head -30; echo ---; grep -n \"case 7:\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | awk -F: '$1>46000 && $1<47500' | head",
 "description": "Find AI_120 HallowBoss section boundaries"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:51:48.519Z

**📎 ToolResult**

```
ugrep: warning: ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria/NPC.cs: No such file or directory
---
46883:		case 7:

```


---

## 🤖 Assistant · 2026-08-19T08:51:53.763Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Odd — the first grep failed with "No such file or directory" but the second worked. That's likely a shell quoting issue or transient — actually both used the same path... The second awk command's grep worked. Maybe the first grep hit the ugrep alias warning because of the pipe to head? Weird. Let me retry. Actually it says "ugrep: warning" — the system grep is aliased to ugrep. The second command succeeded, so the file exists. Possibly a transient error. Let me retry the first grep.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:51:54.490Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"AI_120\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -30",
 "description": "Find AI_120 HallowBoss method boundaries"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:51:54.595Z

**📎 ToolResult**

```
43207:			AI_120_HallowBoss();
46160:	public bool AI_120_HallowBoss_IsInPhase2()
46169:	public bool AI_120_HallowBoss_IsGenuinelyEnraged()
46178:	private void AI_120_HallowBoss_DoMagicEffect(Vector2 spot, int effectType, float progress)
46299:	private void AI_120_HallowBoss()
46316:		bool flag = AI_120_HallowBoss_IsInPhase2();
46320:		if (life == lifeMax && flag4 && !AI_120_HallowBoss_IsGenuinelyEnraged())
46413:				if (flag4 && !AI_120_HallowBoss_IsGenuinelyEnraged())
46447:				AI_120_HallowBoss_DashTo(center);
46584:			if (AI_120_HallowBoss_IsGenuinelyEnraged())
46629:				AI_120_HallowBoss_DoMagicEffect(base.Center + vector35, 1, Utils.GetLerpValue(0f, 60f, this.ai[1], clamped: true));
46701:				AI_120_HallowBoss_DoMagicEffect(base.Center + new Vector2(-55f, -20f), 2, Utils.GetLerpValue(0f, 100f, this.ai[1], clamped: true));
46702:				AI_120_HallowBoss_DoMagicEffect(base.Center + new Vector2(55f, -20f), 4, Utils.GetLerpValue(0f, 100f, this.ai[1], clamped: true));
46813:				AI_120_HallowBoss_DoMagicEffect(base.Center + vector18, 3, Utils.GetLerpValue(0f, 42f, this.ai[1], clamped: true));
46992:			AI_120_HallowBoss_DoMagicEffect(base.Center, 5, Utils.GetLerpValue(40f, 90f, this.ai[1], clamped: true));
47071:				AI_120_HallowBoss_DoMagicEffect(base.Center + new Vector2(-55f, -20f), 2, Utils.GetLerpValue(0f, 100f, this.ai[1], clamped: true));
47072:				AI_120_HallowBoss_DoMagicEffect(base.Center + new Vector2(55f, -20f), 4, Utils.GetLerpValue(0f, 100f, this.ai[1], clamped: true));
47165:				AI_120_HallowBoss_DoMagicEffect(base.Center + vector6, 1, Utils.GetLerpValue(0f, 60f, this.ai[1], clamped: true));
47218:				if (AI_120_HallowBoss_IsGenuinelyEnraged())
47304:	private void AI_120_HallowBoss_DashTo(Vector2 targetPosition)
67678:			frame.Y = (AI_120_HallowBoss_IsInPhase2() ? num : 0);

```


---

## 🤖 Assistant · 2026-08-19T08:51:59.398Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 140,
 "offset": 46299
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:51:59.434Z

**📎 ToolResult**

```
46299		private void AI_120_HallowBoss()
46300		{
46301			Vector2 vector = new Vector2(-150f, -250f);
46302			Vector2 vector2 = new Vector2(150f, -250f);
46303			Vector2 vector3 = new Vector2(0f, -350f);
46304			Vector2 vector4 = new Vector2(0f, -350f);
46305			Vector2 vector5 = new Vector2(-80f, -500f);
46306			float num = 0.5f;
46307			float num2 = 12f;
46308			float num3 = 40f;
46309			float num4 = 6400f;
46310			int num5 = 40;
46311			int num6 = 50;
46312			int num7 = 70;
46313			int num8 = 45;
46314			int num9 = 45;
46315			int num10 = 50;
46316			bool flag = AI_120_HallowBoss_IsInPhase2();
46317			bool flag2 = Main.expertMode;
46318			bool flag3 = flag && flag2;
46319			bool flag4 = ShouldEmpressBeEnraged();
46320			if (life == lifeMax && flag4 && !AI_120_HallowBoss_IsGenuinelyEnraged())
46321			{
46322				this.ai[3] += 2f;
46323			}
46324			bool flag5 = true;
46325			int num11 = 30;
46326			int num12 = 30;
46327			int num13 = 30;
46328			int num14 = 35;
46329			int num15 = 65;
46330			if (flag)
46331			{
46332				num6 = 60;
46333				num8 = 50;
46334				num9 = 50;
46335				num10 = 60;
46336				num7 = 65;
46337				num11 = 35;
46338				num12 = 35;
46339				num13 = 35;
46340				num14 = 40;
46341				num15 = 30;
46342			}
46343			num6 = GetAttackDamage_ForProjectiles(num6, num11);
46344			num8 = GetAttackDamage_ForProjectiles(num8, num12);
46345			num9 = GetAttackDamage_ForProjectiles(num9, num13);
46346			num10 = GetAttackDamage_ForProjectiles(num10, num14);
46347			num7 = GetAttackDamage_ForProjectiles(num7, num15);
46348			if (flag4)
46349			{
46350				num6 = 9999;
46351				num8 = 9999;
46352				num9 = 9999;
46353				num10 = 9999;
46354				num7 = 9999;
46355				flag2 = true;
46356			}
46357			float num16 = 1f;
46358			bool flag6 = true;
46359			int num17 = 0;
46360			if (flag)
46361			{
46362				num17 += 15;
46363			}
46364			if (flag2)
46365			{
46366				num17 += 5;
46367			}
46368			switch ((int)this.ai[0])
46369			{
46370			case 0:
46371				if (this.ai[1] == 0f)
46372				{
46373					velocity = new Vector2(0f, 5f);
46374					if (Main.netMode != 1)
46375					{
46376						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center + new Vector2(0f, -80f), Vector2.Zero, 874, 0, 0f, Main.myPlayer);
46377					}
46378				}
46379				if (this.ai[1] == 10f)
46380				{
46381					SoundEngine.PlaySound(SoundID.Item161, base.Center);
46382				}
46383				velocity *= 0.95f;
46384				if (this.ai[1] > 10f && this.ai[1] < 150f)
46385				{
46386					int num67 = 2;
46387					for (int m = 0; m < num67; m++)
46388					{
46389						float num68 = MathHelper.Lerp(1.3f, 0.7f, Opacity) * Utils.GetLerpValue(0f, 120f, this.ai[1], clamped: true);
46390						Color newColor2 = Main.hslToRgb(this.ai[1] / 180f, 1f, 0.5f);
46391						int num69 = Dust.NewDust(position, width, height, 267, 0f, 0f, 0, newColor2);
46392						Main.dust[num69].position = base.Center + Main.rand.NextVector2Circular((float)width * 3f, (float)height * 3f) + new Vector2(0f, -150f);
46393						Main.dust[num69].velocity *= Main.rand.NextFloat() * 0.8f;
46394						Main.dust[num69].noGravity = true;
46395						Main.dust[num69].fadeIn = 0.6f + Main.rand.NextFloat() * 0.7f * num68;
46396						Main.dust[num69].velocity += Vector2.UnitY * 3f;
46397						Main.dust[num69].scale = 0.35f;
46398						if (num69 != 6000)
46399						{
46400							Dust dust2 = Dust.CloneDust(num69);
46401							dust2.scale /= 2f;
46402							dust2.fadeIn *= 0.85f;
46403							dust2.color = new Color(255, 255, 255, 255);
46404						}
46405					}
46406				}
46407				this.ai[1] += 1f;
46408				flag5 = false;
46409				flag6 = false;
46410				Opacity = MathHelper.Clamp(this.ai[1] / 180f, 0f, 1f);
46411				if (this.ai[1] >= 180f)
46412				{
46413					if (flag4 && !AI_120_HallowBoss_IsGenuinelyEnraged())
46414					{
46415						this.ai[3] += 2f;
46416					}
46417					this.ai[0] = 1f;
46418					this.ai[1] = 0f;
46419					netUpdate = true;
46420					TargetClosest();
46421				}
46422				break;
46423			case 1:
46424			{
46425				float num34 = (flag ? 20f : 45f);
46426				if (Main.getGoodWorld)
46427				{
46428					num34 /= 2f;
46429				}
46430				if (this.ai[1] <= 10f)
46431				{
46432					if (this.ai[1] == 0f)
46433					{
46434						TargetClosest();
46435					}
46436					NPCAimedTarget targetData4 = GetTargetData();
46437					if (targetData4.Invalid)
46438					{

```


---

## 🤖 Assistant · 2026-08-19T08:52:02.895Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So `flag2 = Main.expertMode`, and `flag4 = ShouldEmpressBeEnraged()` — when enraged (daytime), `flag2 = true`. So flag2 = isExpert || dayEnrage. Good.

Now I need to find the attack selection logic — where the second phase table [7,2,8,11,5,2,6,4,8,12] is used. Let me continue reading case 1 (the idle/selection state) to find the attack table.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:52:03.450Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 150,
 "offset": 46439
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:52:03.475Z

**📎 ToolResult**

```
46439						this.ai[0] = 13f;
46440						this.ai[1] = 0f;
46441						this.ai[2] += 1f;
46442						velocity /= 4f;
46443						netUpdate = true;
46444						break;
46445					}
46446					Vector2 center = targetData4.Center;
46447					AI_120_HallowBoss_DashTo(center);
46448					netUpdate = true;
46449				}
46450				if (velocity.Length() > 16f && this.ai[1] > 10f)
46451				{
46452					velocity /= 2f;
46453				}
46454				velocity *= 0.92f;
46455				this.ai[1] += 1f;
46456				if (!(this.ai[1] >= num34))
46457				{
46458					break;
46459				}
46460				int num35 = (int)this.ai[2];
46461				int num36 = 2;
46462				int num37 = 0;
46463				if (!flag)
46464				{
46465					int num38 = num37++;
46466					int num39 = num37++;
46467					int num40 = num37++;
46468					int num41 = num37++;
46469					int num42 = num37++;
46470					int num43 = num37++;
46471					int num44 = num37++;
46472					int num45 = num37++;
46473					int num46 = num37++;
46474					int num47 = num37++;
46475					if (num35 % num37 == num38)
46476					{
46477						num36 = 2;
46478					}
46479					if (num35 % num37 == num39)
46480					{
46481						num36 = 8;
46482					}
46483					if (num35 % num37 == num40)
46484					{
46485						num36 = 6;
46486					}
46487					if (num35 % num37 == num41)
46488					{
46489						num36 = 8;
46490					}
46491					if (num35 % num37 == num42)
46492					{
46493						num36 = 5;
46494					}
46495					if (num35 % num37 == num43)
46496					{
46497						num36 = 2;
46498					}
46499					if (num35 % num37 == num44)
46500					{
46501						num36 = 8;
46502					}
46503					if (num35 % num37 == num45)
46504					{
46505						num36 = 4;
46506					}
46507					if (num35 % num37 == num46)
46508					{
46509						num36 = 8;
46510					}
46511					if (num35 % num37 == num47)
46512					{
46513						num36 = 5;
46514					}
46515					if ((float)life / (float)lifeMax <= 0.5f)
46516					{
46517						num36 = 10;
46518					}
46519				}
46520				if (flag)
46521				{
46522					int num48 = num37++;
46523					int num49 = num37++;
46524					int num50 = num37++;
46525					int num51 = -1;
46526					if (flag2)
46527					{
46528						num51 = num37++;
46529					}
46530					int num52 = num37++;
46531					int num53 = num37++;
46532					int num54 = num37++;
46533					int num55 = num37++;
46534					int num56 = num37++;
46535					int num57 = num37++;
46536					if (num35 % num37 == num48)
46537					{
46538						num36 = 7;
46539					}
46540					if (num35 % num37 == num49)
46541					{
46542						num36 = 2;
46543					}
46544					if (num35 % num37 == num50)
46545					{
46546						num36 = 8;
46547					}
46548					if (num35 % num37 == num52)
46549					{
46550						num36 = 5;
46551					}
46552					if (num35 % num37 == num53)
46553					{
46554						num36 = 2;
46555					}
46556					if (num35 % num37 == num54)
46557					{
46558						num36 = 6;
46559					}
46560					if (num35 % num37 == num54)
46561					{
46562						num36 = 6;
46563					}
46564					if (num35 % num37 == num55)
46565					{
46566						num36 = 4;
46567					}
46568					if (num35 % num37 == num56)
46569					{
46570						num36 = 8;
46571					}
46572					if (num35 % num37 == num51)
46573					{
46574						num36 = 11;
46575					}
46576					if (num35 % num37 == num57)
46577					{
46578						num36 = 12;
46579					}
46580				}
46581				TargetClosest();
46582				NPCAimedTarget targetData5 = GetTargetData();
46583				bool flag12 = false;
46584				if (AI_120_HallowBoss_IsGenuinelyEnraged())
46585				{
46586					if (!Main.dayTime)
46587					{
46588						flag12 = true;

```


---

## 🤖 Assistant · 2026-08-19T08:52:48.430Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now I understand the vanilla table logic:

- `num35 = (int)ai[2]` (attack counter), `num36 = 2` default (attack to run).
- Phase 1 (!flag): 10 slots (num37=10): [2,8,6,8,5,2,8,4,8,5]
- Phase 2 (flag): num37 starts at 0, increments: num48=0, num49=1, num50=2, num51=-1 or 3 (if flag2), then num52, num53... 

Wait careful: `num37` is 0 at start. In phase 2 block:
- num48 = num37++ → 0
- num49 = num37++ → 1
- num50 = num37++ → 2
- num51 = -1; if (flag2) num51 = num37++ → 3
- num52 = num37++ → 4 (or 3 if !flag2)
- num53 = num37++ → 5 (or 4)
- num54 = num37++ → 6 (or 5)
- num55 = num37++ → 7 (or 6)
- num56 = num37++ → 8 (or 7)
- num57 = num37++ → 9 (or 8)

So with flag2: total num37 = 10 slots: 
- slot 0 → 7
- slot 1 → 2
- slot 2 → 8
- slot 3 → 11
- slot 4 → 5
- slot 5 → 2
- slot 6 → 6
- slot 7 → 4
- slot 8 → 8
- slot 9 → 12

That matches the task's [7,2,8,11,5,2,6,4,8,12]. 

Without flag2 (phase 2, classic/night): 9 slots:
- slot 0 → 7
- slot 1 → 2
- slot 2 → 8
- slot 3 (num52) → 5
- slot 4 (num53) → 2
- slot 5 (num54) → 6
- slot 6 (num55) → 4
- slot 7 (num56) → 8
- slot 8 (num57) → 12

So [7,2,8,5,2,6,4,8,12] — 9 slots.

Also the phase-1 block: `if ((float)life / (float)lifeMax <= 0.5f) num36 = 10;` forces transition to phase 2 when HP ≤ 50%.

Also `num17`: attack-duration trim: base 0; +15 if phase2 (flag), +5 if flag2. This num17 is used in the attack cases: e.g. case 11: `num58 = 20 - num17` and ends at `ai[1] >= 100 + num58`... wait: `if (this.ai[1] >= 100f + num58)`. num58 = 20 - num17, so 120 - num17 total. With phase2+expert: num17 = 20 → num58 = 0 → ends at 100. Hmm wait, in expert+phase2: num17 = 15+5 = 20, so num58 = 0, duration = 100 ticks. In classic phase2: num17 = 15 → num58 = 5 → 105 ticks.

Wait, actually let me recheck: case 11 shooting window: `(int)this.ai[1] % 3 == 0 && this.ai[1] < 100f`. And `this.ai[1] >= 100f + num58` ends. And the projectile spawn passes `ai[1] = this.ai[1] / 100f` as ai0? Wait: `Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector14, Vector2.Zero, 919, num6, 0f, Main.myPlayer, v2.ToRotation(), this.ai[1] / 100f)`. Projectile 919's ai0 = rotation (v2.ToRotation()), ai1 = this.ai[1] / 100f.

Hmm interesting. So the projectile 919 (Prismatic Lance?) gets ai1 = spawn time normalized (ai1/100). Let me look at projectile 919 AI in Projectile.cs to understand the delay. The task says "case11=预测型光枪墙:919 光枪墙的预测变体:沿玩家速度预测线生成一排 919 预告→延时突进;具体参数照抄". So I need to read Projectile 919's AI to see how ai1 (delay) works.

Also what's num6? num6 = 50, in phase2 num6=60, then GetAttackDamage_ForProjectiles(num6, num11): num11 = 30→35 in phase2. And if enraged (flag4), num6 = 9999 (one-shot in daytime). So damage for 919 = num6.

Now, the task says "我方 919 已有收敛实现(直飞 12 速)" — our 919 already has an implementation (straight flight speed 12). case11 uses same projectile type + predicted landing arrangement. So I need to check our existing 919 (Empress Sun Dance? No — 919 is "Prismatic Lance" I think). Let me check our implementation in bossAI_lategame.ts.

Also note: in case 11, the spawn position logic:
```
v = -targetData.Velocity (normalized, default -UnitY)
num60 = 100
center2 = target center
if Distance(center2) > 2400 skip
num61 = 90
vector13 = center2 + velocity * 90   (predicted position)
vector14 = center2 + v * 100  (spawn point 100px opposite of player's movement direction... wait v = -velocity normalized, so vector14 = center - velocityDir * 100 — 100px "behind" the player's motion)
if (vector14.Distance(center2) < num60) { vector15 = center2 - vector14; if zero → v; vector14 = center2 - Normalize(vector15) * 100 }
```

Hmm wait, that if is weird: vector14 = center2 + v*100 where v is normalized. Distance from center2 is exactly 100 unless v was zero... v is SafeNormalize(-UnitY) so it's unit length. So vector14 is always exactly 100 from center2. The `if (vector14.Distance(center2) < num60)` is thus dead code in practice (or handles NaN). Actually wait — SafeNormalize with fallback -UnitY returns unit vector if input is non-zero. If player velocity is zero → v = -UnitY = (0,-1), still unit. So yes, always distance exactly 100. The inner check is a safety net. I'll replicate straightforwardly.

v2 = vector13 - vector14 → direction from spawn point to predicted player position. Projectile spawns at vector14 (100px opposite of player's velocity direction from player), aims at player's predicted position 90 ticks ahead. ai0 = v2.ToRotation() (aim angle), ai1 = this.ai[1]/100 (spawn progress as delay).

Then there's the multi-player duplication: `Boss_CanShootExtraAt(l, num62 % 3, 3, 2400)` — every 3rd shot also spawns at each extra player. Since we're single-player, that part is mostly irrelevant, but for parity I can keep the loop (only matters multiplayer; our engine is single player presumably — but the sim host might support multiple players? Let me check what Boss_CanShootExtraAt does and whether our codebase has a precedent in other cases like case 12 which uses the same pattern `Boss_CanShootExtraAt(j, num24 % 3, 3, 2400)`).

Now I need to see how our bossAI_lategame.ts implements the Empress (639? Empress of Light is NPC 639... Actually Empress of Light type = 639? Let me check: 639 is Empress of Light? I recall 639 = Empress of Light, 640 = Empress "enraged"? No — 639 is Empress of Light. Let me confirm from our code.)

Let me now read our implementation files. Priorities:
1. src/entities/bossAI_lategame.ts (Empress section + 919)
2. src/entities/bossAI_duke_moonlord.ts (duke section)
3. Renderer (customFrameIdx / case handling) — search for customFrameIdx precedent (694)
4. Game.ts WoF death chain + misc announcement API
5. bossAI_martian.ts shooting sites + bossAI.ts getAttackDamageForProjectiles import precedent

Let me read bossAI_lategame.ts first.
````

</details>


---

## 🤖 Assistant · 2026-08-19T08:52:49.774Z · glm-x-preview-260804

```
现在我已经有了 vanilla 的选招表逻辑。让我检查一下 case 1 的其余部分（读取 `Boss_CanShootExtraAt` 上下文并确认表语义），然后阅读我们的实现。
```


---

## 🤖 Assistant · 2026-08-19T08:52:50.377Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 60,
 "offset": 46580
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:52:50.390Z

**📎 ToolResult**

```
46580				}
46581				TargetClosest();
46582				NPCAimedTarget targetData5 = GetTargetData();
46583				bool flag12 = false;
46584				if (AI_120_HallowBoss_IsGenuinelyEnraged())
46585				{
46586					if (!Main.dayTime)
46587					{
46588						flag12 = true;
46589					}
46590					if (Main.dayTime && Main.time >= 53400.0)
46591					{
46592						flag12 = true;
46593					}
46594				}
46595				if (targetData5.Invalid || Distance(targetData5.Center) > num4 || flag12)
46596				{
46597					num36 = 13;
46598				}
46599				if (num36 == 8 && targetData5.Center.X > base.Center.X)
46600				{
46601					num36 = 9;
46602				}
46603				if (flag2 && num36 != 5 && num36 != 12)
46604				{
46605					velocity = DirectionFrom(targetData5.Center).SafeNormalize(Vector2.Zero).RotatedBy(MathF.PI / 2f * (float)(targetData5.Center.X > base.Center.X).ToDirectionInt()) * 20f;
46606				}
46607				this.ai[0] = num36;
46608				this.ai[1] = 0f;
46609				this.ai[2] += 1f;
46610				netUpdate = true;
46611				break;
46612			}
46613			case 2:
46614			{
46615				if (this.ai[1] == 0f)
46616				{
46617					SoundEngine.PlaySound(SoundID.Item164, base.Center);
46618				}
46619				float num90 = 90f - (float)num17;
46620				Vector2 vector35 = new Vector2(-55f, -30f);
46621				NPCAimedTarget targetData11 = GetTargetData();
46622				Vector2 vector36 = (targetData11.Invalid ? base.Center : targetData11.Center);
46623				if (Distance(vector36 + vector) > num3)
46624				{
46625					SimpleFlyMovement(DirectionTo(vector36 + vector).SafeNormalize(Vector2.Zero) * num2, num);
46626				}
46627				if (this.ai[1] < 60f)
46628				{
46629					AI_120_HallowBoss_DoMagicEffect(base.Center + vector35, 1, Utils.GetLerpValue(0f, 60f, this.ai[1], clamped: true));
46630				}
46631				int num91 = 3;
46632				if (flag2)
46633				{
46634					num91 = 2;
46635				}
46636				if ((int)this.ai[1] % num91 == 0 && this.ai[1] < 60f)
46637				{
46638					float ai3 = this.ai[1] / 60f;
46639					Vector2 vector37 = new Vector2(0f, -6f).RotatedBy(MathF.PI / 2f * Main.rand.NextFloatDirection());

```


---

## 🤖 Assistant · 2026-08-19T08:52:51.913Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts ~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts",
 "description": "Get line counts of our boss AI files"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:52:51.981Z

**📎 ToolResult**

```
    1812 ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts
    1882 ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts
     959 ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts
    2056 ~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts
    6709 total

```


---

## 🤖 Assistant · 2026-08-19T08:52:55.224Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read our bossAI_lategame.ts — the Empress of Light section.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:52:55.243Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:52:55.514Z

**📎 ToolResult**

```
1	// 后期三大 Boss AI 1:1 移植(Terarria1456 = 1.4.5.6 反编译源码,经典模式主链):
2	//   aiStyle 84  拜月教邪教徒 439  AI_084_LunaticCultist()        NPC.cs:64921-65957
3	//   aiStyle 120 光之女皇     636  AI_120_HallowBoss()           NPC.cs:46299-47302(+DashTo :47304)
4	//   aiStyle 121 史莱姆皇后   657  AI_121_QueenSlime()           NPC.cs:45543-46177(+FlyMovement :45467)
5	// 由 Enemy.fixedUpdate 的 aiStyle 分发调用(接线见文件尾「接线清单」);本文件不改动任何已有文件。
6	// 弹幕统一走 bossAI.shoot(Arrow 直飞桶);原版「定点预告→延时冲刺」类投射物中
7	// 465 闪电球/464 冰雾母云已实体化(IceMistCloud/LightningOrb,见各类头注),
8	// 919/923 仍收敛为带初速直飞(见各处注释)。getGoodWorld 分支已实装(女皇招式间隔折半/
9	// 史后空中横移+砸地蓄力+凝胶环抬档);expert/大师分支只注释不实现;netcode 跳过。
10	import { Enemy } from './Enemy';
11	import type { GameHooks } from './types';
12	import type { Player } from './Player';
13	import type { Camera } from '../render/Camera';
14	import type { Renderer } from '../render/Renderer';
15	import { TILE } from '../core/constants';
16	import { TILE_DEFS } from '../data/tiles';
17	import { spawnPart, shoot, losClear, addEnemy } from './bossAI';
18	import { Entity } from './Entity';
19	import { projSprite, projFrameImg } from './Arrow';
20	import { hitPlayer, hitTownNpcs, hitCritters } from './projTargets';
21	import { canHit } from '../physics/LineOfSight';
22	import { LightningBoltProj } from './LightningBoltProj';
23	import { upgradeToBitmap } from '../assets/SpriteAtlas';
24	
25	// ===================== 共用工具(与 bossAI.ts 同语义,私有副本) =====================
26	
27	/** 原版 MathHelper.Clamp */
28	const clamp = (v: number, lo: number, hi: number): number => (v < lo ? lo : v > hi ? hi : v);
29	/** 原版 Utils.GetLerpValue(clamped) */
30	const lerpValue = (from: number, to: number, t: number): number =>
31	  from === to ? (t < from ? 0 : 1) : clamp((t - from) / (to - from), 0, 1);
32	/** 原版 Vector2.Lerp */
33	const vLerp = (a: number, b: number, t: number): number => a + (b - a) * t;
34	
35	/** 伤害/防御基值缓存(状态机每 tick 从基值派生临时修正,防重复乘膨胀;同 bossAI.baseStats) */
36	const baseStats = new WeakMap<Enemy, { dmg: number; def: number }>();
37	const baseOf = (e: Enemy): { dmg: number; def: number } => {
38	  let b = baseStats.get(e);
39	  if (!b) {
40	    // 首次进入时 def 可能已被别的状态改写——重新取原版数据基值兜底
41	    b = { dmg: e.def.damage, def: e.def.defense ?? 0 };
42	    if (e.vanilla) {
43	      b.dmg = e.vanilla.damage ?? b.dmg;
44	      b.def = e.vanilla.defense ?? b.def;
45	    }
46	    baseStats.set(e, b);
47	  }
48	  return b;
49	};
50	
51	/** 原版 localAI[0..3] 的外部存储(Enemy 只有 ai0-ai3 四个槽)。
52	 *  la2/la3 放宽为 unknown:邪教徒用 la2 存仪式圈心坐标对象、la3 存克隆体的真身引用 */
53	const localAI = new WeakMap<Enemy, { la0: number; la1: number; la2: unknown; la3: unknown }>();
54	const laOf = (e: Enemy): { la0: number; la1: number; la2: unknown; la3: unknown } => {
55	  let l = localAI.get(e);
56	  if (!l) { l = { la0: 0, la1: 0, la2: 0, la3: 0 }; localAI.set(e, l); }
57	  return l;
58	};
59	
60	/** 原版 SimpleFlyMovement(NPC.cs:23866 雏形):逐轴向目标速度以加速度步进(钳 ±acc) */
61	function simpleFly(e: Enemy, dvx: number, dvy: number, acc: number): void {
62	  e.vx += clamp(dvx - e.vx, -acc, acc);
63	  e.vy += clamp(dvy - e.vy, -acc, acc);
64	}
65	
66	/** 无碰撞积分(noTileCollide 族) */
67	function flyIntegrate(e: Enemy): void {
68	  e.x += e.vx;
69	  e.y += e.vy;
70	}
71	
72	/** 地形碰撞(bossAI.collideGround 的私有副本:Queen Slime 走路/砸地需要) */
73	function collideGround(e: Enemy, game: GameHooks): void {
74	  const st = game.world.store;
75	  const tx = Math.floor(e.cx / TILE);
76	  const ty = Math.floor((e.y + e.h) / TILE);
77	  if (st.inBounds(tx, ty) && st.isSolid(tx, ty) && e.vy >= 0) {
78	    e.y = ty * TILE - e.h;
79	    e.vy = 0;
80	    e.onGround = true;
81	  } else {
82	    e.onGround = false;
83	  }
84	  const ty2 = Math.floor(e.y / TILE);
85	  if (st.inBounds(tx, ty2) && st.isSolid(tx, ty2) && e.vy < 0) {
86	    e.y = (ty2 + 1) * TILE;
87	    e.vy = 0;
88	  }
89	  const tx2 = Math.floor((e.x + e.w) / TILE);
90	  if (st.inBounds(tx2, Math.floor(e.cy / TILE)) && st.isSolid(tx2, Math.floor(e.cy / TILE)) && e.vx > 0) {
91	    e.x = tx2 * TILE - e.w; e.vx = 0;
92	  }
93	  const tx3 = Math.floor(e.x / TILE);
94	  if (st.inBounds(tx3, Math.floor(e.cy / TILE)) && st.isSolid(tx3, Math.floor(e.cy / TILE)) && e.vx < 0) {
95	    e.x = (tx3 + 1) * TILE; e.vx = 0;
96	  }
97	}
98	
99	/** 朝玩家预测位置的单位向量(player.velocity*20 预判,NPC.cs:65380 系) */
100	function aimLead(e: Enemy, player: Player, fallbackX: number): { x: number; y: number } {
101	  const dx = player.cx + player.vx * 20 - e.cx;
102	  const dy = player.cy + player.vy * 20 - e.cy;
103	  const d = Math.hypot(dx, dy);
104	  if (!Number.isFinite(d) || d < 0.0001) return { x: fallbackX, y: 0 };
105	  return { x: dx / d, y: dy / d };
106	}
107	/** 旋转 */
108	const rot = (x: number, y: number, a: number): [number, number] =>
109	  [x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)];
110	
111	// ===================== AI_084 拜月教邪教徒 439 + 克隆体 440(NPC.cs:64921-65957) =====================
112	// 真身 439 与克隆体 440 共用本核(flag2 = type==439,:64971):克隆体由仪式态(ai0==5)生成,
113	//   ai[0]/ai[1] 每 tick 从真身镜像(:65000-65001);仅在仪式窗口(120-420t)可被击中——
114	//   打中克隆体 → 克隆体消散 + 真身进 6 态硬直 120t(:65003-65014);
115	//   打中真身 → 推进选招拍号并清同代克隆体(:65016-65060)。
116	//   仪式态外克隆体无敌且不可选(dontTakeDamage=flag3,:65953)。
117	// 状态机(ai0): -1 出生显形(420t,真身专属) / 0 选招(40t) / 1 飞掠占位(含克隆体环位补位) /
118	//   2 冰雾 464(:65362) / 3 火球 467(:65430,第三拍克隆体补射 468) / 4 闪电 465(:65531) /
119	//   5 仪式瞬移(:65623,生成/补位克隆体) / 6 硬直(:65771) / 7 远古之光(:65796,真身召
120	//   NPC522 轨道弹 + 第三拍克隆体补射 468×5) / 8 远古末日 NPC523(经典不可达,状态体保留)。
121	// 经典数值: 冰 35 伤(:64930)/火 30 伤·18t×3(:64941-64946)/闪电 45 伤(:64953)/
122	//   光 20t×2(:64963-64967)/末日 20t×3(:64970-64973);克隆体补射 468 恒 18 伤(:65491)。
123	// 选招表(:65131-65254 两张 switch 表合一;表尾拍把 ai3 复位 -1 → 下次完成攻击后回 0 重循环):
124	//   一阶段 12 拍 [冲,火,冲,冰,冲,雷,冲,火,冲,冰,冲,仪式] 循环;
125	//   二阶段 12 拍 [冲,火,冲,光,冲,雷,冲,光,冲,冰,冲,雷] 循环(二阶段不再仪式)。
126	const CULTIST_CYCLE_P1 = [0, 1, 0, 2, 0, 3, 0, 1, 0, 2, 0, 4];
127	const CULTIST_CYCLE_P2 = [0, 1, 0, 5, 0, 3, 0, 5, 0, 2, 0, 3];
128	
129	/** 选招(:65131-65254 两张 switch 表合一;表尾拍把 ai3 复位 -1 → 下次完成攻击后回 0 重循环) */
130	function cultistPick(e: Enemy, phase2: boolean): number {
131	  const table = phase2 ? CULTIST_CYCLE_P2 : CULTIST_CYCLE_P1;
132	  const i = Math.floor(e.ai3);
133	  if (i < 0 || i >= table.length) { e.ai3 = -1; return 0; }
134	  if (i === table.length - 1) e.ai3 = -1; // :65199/:65253 表尾复位
135	  return table[i];
136	}
137	
138	/** 真身的全部存活克隆体(:65449 系:type==440 && ai[3]==whoAmI;
139	 *  本仓克隆体以 localAI 槽 la3 反存真身 Enemy 引用) */
140	function cultistClones(game: GameHooks, parent: Enemy): Enemy[] {
141	  return (game.enemies() as Enemy[]).filter(
142	    (n) => !n.dead && n.vanillaId === 440 && laOf(n).la3 === parent);
143	}
144	
145	/** 仪式圈弹 490（Projectile.cs:5383 SetDefaults + aiStyle 89 :31193-31326）：
146	 *  14×14 / hostile / alpha 255 / timeLeft 600 / noTileCollide，锚定源邪教徒 ai[1]。
147	 *  淡入 300t（alpha -5/t 钳 0）→ 淡出（+12/t）；scale = (1-alpha/255)×0.6 随透明度
148	 *  张合；rotation 每 t +π/210；alpha==0 时每 t 2 颗 228 号紫尘沿 204×scale 半径
149	 *  向心收拢；出生播 Item123（真轨 Item_123.wav 已落位，roar 近似销核）。
150	 *  ai[0]==300 时原版召 NPC 454 幻影龙（场上无）否则 521 章鱼头（:31282-31292）——
151	 *  两 AI 族未移植（登记：CultistDragonHead/AncientCultistSquidhead），此处不召，
152	 *  圈弹视觉/淡入淡出/自旋 1:1。锚（439）消亡即 Kill（:31305-31320）。 */
153	export class CultistRitualCircle extends Entity {
154	  w = 14; h = 14;
155	  private srcId: number;
156	  private age = 0;         // ai[0]
157	  private alpha = 255;
158	  private rot = 0;
159	  private soundPlayed = false;  // localAI[1]
160	  /** ai[1] == -1（仪式被打破,Projectile.cs:31195 +12/t 快速淡出,不召龙） */
161	  private interrupted = false;
162	  dead = false;
163	
164	  constructor(src: Enemy) {
165	    super();
166	    this.srcId = src.id;
167	    this.x = src.cx - this.w / 2;
168	    this.y = src.cy - this.h / 2;
169	  }
170	
171	  /** 仪式窗口内真身被击中 → Main.projectile[ai[2]].ai[1] = -1（NPC.cs:65054） */
172	  interrupt(): void { this.interrupted = true; }
173	
174	  /** (1-alpha/255)×0.6（:31208-31210） */
175	  private get scale(): number { return (1 - this.alpha / 255) * 0.6; }
176	
177	  fixedUpdate(_dt: number, game: GameHooks): void {
178	    // 淡入/淡出（:31195-31214）：中断（ai[1]=-1）或 age≥300 → +12/t；否则 -5/t
179	    this.alpha += (this.interrupted || this.age >= 300) ? 12 : -5;
180	    this.alpha = Math.max(0, Math.min(255, this.alpha));
181	    this.rot += Math.PI / 210;                          // :31217
182	    if (!this.soundPlayed) {
183	      this.soundPlayed = true;
184	      // SoundID.Item123（Projectile.cs:31221，无坐标 = 全量不衰减）——原 roar 近似已销核
185	      game.playSfxFile?.('Item_123', 1);
186	    }
187	    // 完全显现期的收拢紫尘（:31223-31251，尘 228 / 半径 204×scale / 内圈 ×0.42）
188	    if (this.alpha === 0) {
189	      for (let k = 0; k < 2; k++) {
190	        const inner = k === 1;
191	        const a = Math.random() * Math.PI * 2;
192	        const rr = 204 * this.scale * (inner ? 0.42 : 1);
193	        game.spawnParticles(this.cx + Math.cos(a) * rr, this.cy + Math.sin(a) * rr,
194	          '#A060E0', 1, inner ? 1.5 : 2, { life: 30 });
195	      }
196	    }
197	    this.age++;
198	    // ---- :31279-31292 age==300 且未中断 → 召唤：场上无 454 幻影龙 → NewNPC(454)
199	    //      （头 + 455-458 身 ×4 + 459 尾共享头血池）；否则 → 521 远古幻象。
200	    //      召出后 ai[1] 复用为该 NPC 索引 = 圈锚从邪教徒切到龙（龙亡圈灭）----
201	    if (this.age === 300 && !this.interrupted) {
202	      const hasDragon = (game.enemies() as Enemy[])
203	        .some((n) => !n.dead && n.vanillaId === 454);
204	      const id = hasDragon ? 521 : 454;
205	      const head = Enemy.fromVanilla(id, this.cx, this.cy);
206	      if (head) {
207	        addEnemy(game, head);
208	        this.srcId = head.id;              // ai[1] = NewNPC 返回索引（:31283/:31287）
209	        if (id === 454) {
210	          // 链段（NewNPC 段链展开）：455-458 + 尾 459，realLife 共享头 10000 血
211	          const segs = Enemy.spawnWormChain(head, 5, [455, 456, 457, 458, 459], true);
212	          for (const sg of segs) addEnemy(game, sg);
213	        }
214	      }
215	    } else if (this.age === 320) {
216	      this.dead = true;                                 // :31290-31294
217	      return;
218	    }
219	    // ---- flag44（:31295-31314）：中断且全隐 → Kill；或锚 NPC 失效/非 439/454/521 → Kill ----
220	    const src = (game.enemies() as Enemy[]).find((n) => n.id === this.srcId);
221	    const anchorOk = !!src && !src.dead
222	      && (src.vanillaId === 439 || src.vanillaId === 454 || src.vanillaId === 521);
223	    if ((this.interrupted && this.alpha >= 255) || !anchorOk) { this.dead = true; }
224	  }
225	
226	  draw(r: Renderer, _cam: Camera): void {
227	    const ctx = r.canvas.getContext('2d');
228	    if (!ctx) return;
229	    const img = projSprite(490);
230	    if (!img || !(img.width > 0) || img.width === 0) return;
231	    const s = this.scale;
232	    if (s <= 0.01) return;
233	    const iw = img.width, ih = img.height;
234	    ctx.save();
235	    ctx.translate(this.cx, this.cy);
236	    ctx.rotate(this.rot);
237	    ctx.imageSmoothingEnabled = false;
238	    ctx.drawImage(img, -iw * s / 2, -ih * s / 2, iw * s, ih * s);
239	    ctx.restore();
240	  }
241	}
242	
243	/** Extra_35（24×222 冰雾六角波纹，1×3 帧）懒加载（StardustMarkProj.beamSprite 同款） */
244	let hexWaveImg: ImageBitmap | HTMLImageElement | null = null;
245	let hexWaveTried = false;
246	function extra35(): ImageBitmap | HTMLImageElement | null {
247	  if (hexWaveTried) return hexWaveImg;
248	  hexWaveTried = true;
249	  if (typeof Image === 'undefined') return null;
250	  const im = new Image();
251	  im.onload = () => upgradeToBitmap(im, (b) => { hexWaveImg = b; });
252	  im.src = 'sprites/vanilla/Extra_35.png';
253	  hexWaveImg = im;
254	  return im;
255	}
256	
257	/** 冰雾母云/子体 464（Projectile.cs aiStyle 86 :30747-30821 + SetDefaults :5078-5087）：
258	 *  邪教徒冰雾态(:65411-65421)发的是 ai[1]=1 的【母云】——60×60 / hostile /
259	 *  tileCollide=false / penetrate=-1 / alpha 255；速度=瞄玩家预判 ×4（发射向量），
260	 *  母云终身保持该速度漂移（UpdatePosition :19026 无早退）。
261	 *  母云（ai[1]==1，:30763-30790）：ai0<130 淡入 alpha−10/t、≥130 淡出 +10/t（钳
262	 *  0..255）；≥150 Kill；每 ai0%30==0 沿自转 rotation 派生一颗【子体 464】（同伤/
263	 *  同击退，速度=rotation 单位向量）；rotation += π/30 自旋；AddLight(0.3,0.75,0.9)。
264	 *  子体（ai[1]==0，:30792-30821）：AI 侧 position−=velocity + 引擎 UpdatePosition
265	 *  +velocity → 净静止（速度只作尘环几何参数）；<40t 淡入 −40/t、≥40 淡出 +3/t、
266	 *  ≥45 Kill；六角尘环——(0,−720).RotatedBy(速度角)×(ai0%45/45) 为半径向量，
267	 *  六个 60° 角点各 AddLight + 2 颗 197 号尘（noGravity）。
268	 *  绘制：母云走 Projectile_464.png 随 rotation 旋转（Main.cs:32360 大表分支默认画）；
269	 *  子体【不画 464 贴图】——六角点各画一张 Extra_35（1×3 帧带按角点序循环、旋
270	 *  角=角点角+速度角+π，Main.cs:32699-32721）。接触伤害=传入 damage（教徒冰雾 35）。
271	 *  首帧 Item_120 音（:30749-30752，母云与每颗子体各自首帧播——原调用点单播已随
272	 *  实体化迁入此处，避免双播）。 */
273	export class IceMistCloud extends Entity {
274	  readonly projId = 464;
275	  damage: number;
276	  w = 60; h = 60;                  // SetDefaults :5079-5080
277	  /** ai[1]==1 = 母云档 */
278	  private readonly mother: boolean;
279	  private ai0 = 0;
280	  private alpha = 255;
281	  private rot = 0;                 // rotation（NewProjectile 缺省 0，仅母云自旋改写）
282	  private sndPlayed = false;       // localAI[1]
283	
284	  /** x/y = NewProjectile 的 X/Y（中心锚）；vx/vy = 发射向量（母云=瞄速 4） */
285	  constructor(x: number, y: number, vx: number, vy: number, damage: number, mother: boolean) {
286	    super();
287	    this.x = x - this.w / 2;
288	    this.y = y - this.h / 2;
289	    this.vx = vx; this.vy = vy;
290	    this.damage = damage;
291	    this.mother = mother;
292	  }
293	
294	  fixedUpdate(_dt: number, game: GameHooks): void {
295	    if (!this.sndPlayed) {         // :30749-30752（母云与子体各自首帧）
296	      this.sndPlayed = true;
297	      game.playSfxWav?.('Item_120', 1, this.x, this.y);
298	    }
299	    this.ai0++;
300	    if (this.mother) {
301	      // ---- 母云档（:30763-30790）----
302	      this.alpha = Math.max(0, Math.min(255, this.alpha + (this.ai0 >= 130 ? 10 : -10)));
303	      if (this.ai0 >= 150) { this.dead = true; return; }          // :30778-30781
304	      if (this.ai0 % 30 === 0) {                                   // :30782-30787
305	        const child = new IceMistCloud(this.cx, this.cy,
306	          Math.cos(this.rot), Math.sin(this.rot), this.damage, false);
307	        (game as unknown as { entities: { add: (en: Entity, b: string) => void } }).entities
308	          .add(child, 'projectiles');
309	      }
310	      this.rot += Math.PI / 30;                                    // :30788
311	      game.addLightAt?.(this.cx, this.cy, 0.3, 0.75, 0.9);         // :30789
312	      this.x += this.vx;                                           // 引擎速度积分（漂移）
313	      this.y += this.vy;
314	    } else {
315	      // ---- 子体档（:30792-30821）----
316	      this.x -= this.vx;                                           // :30792（与引擎积分抵消→净静止）
317	      this.y -= this.vy;
318	      this.alpha = Math.max(0, Math.min(255, this.alpha + (this.ai0 >= 40 ? 3 : -40)));
319	      if (this.ai0 >= 45) { this.dead = true; return; }            // :30805-30808
320	      // 六角尘环（:30810-30821）
321	      const hex = this.hexPoints();
322	      for (let i = 0; i < 6; i++) {
323	        game.addLightAt?.(hex[i][0], hex[i][1], 0.3, 0.75, 0.9);
324	        for (let k = 0; k < 2; k++) {
325	          game.spawnDust?.(hex[i][0] + (Math.random() * 8 - 4), hex[i][1] + (Math.random() * 8 - 4),
326	            8, 8, 197, 0, 0, 100, null, 1, true);   // 尘 197 noGravity（:30817-30820）
327	        }
328	      }
329	      this.x += this.vx;                                           // 引擎速度积分（:19026）
330	      this.y += this.vy;
331	    }
332	    // 接触伤害（hostile penetrate=-1，命中不消耗；敌弹 ×2 缩放在 hitPlayer 内）
333	    hitPlayer(this, game, this.damage);
334	    hitTownNpcs(this, game, this.damage, 0, 'hostile');
335	    hitCritters(this, game);
336	  }
337	
338	  /** 六角波纹角点（中心+偏移）：(0,−720).RotatedBy(速度角)×(ai0%45/45) 再各旋 k·60° */
339	  private hexPoints(): Array<[number, number]> {
340	    const va = Math.atan2(this.vy, this.vx);
341	    const [rx, ry] = rot(0, -720, va);
342	    const k = (this.ai0 % 45) / 45;
343	    const sx = rx * k, sy = ry * k;
344	    const pts: Array<[number, number]> = [];
345	    for (let i = 0; i < 6; i++) {
346	      const [hx, hy] = rot(sx, sy, (i * Math.PI * 2) / 6);
347	      pts.push([this.cx + hx, this.cy + hy]);
348	    }
349	    return pts;
350	  }
351	
352	  draw(r: Renderer, _cam: Camera): void {
353	    const ctx = r.canvas.getContext('2d');
354	    if (!ctx) return;
355	    const bright = (255 - this.alpha) / 255;
356	    if (bright <= 0) return;
357	    ctx.save();
358	    ctx.imageSmoothingEnabled = false;
359	    ctx.globalAlpha = bright;
360	    if (this.mother) {
361	      // Projectile_464.png × rotation（Main.cs:32360 大表分支默认画法）
362	      const img = projSprite(464);
363	      if (img && img.width > 0) {
364	        ctx.translate(this.cx, this.cy);
365	        ctx.rotate(this.rot);
366	        ctx.drawImage(img, -img.width / 2, -img.height / 2, img.width, img.height);
367	      } else {
368	        ctx.fillStyle = '#9FD8E8';
369	        ctx.beginPath(); ctx.arc(this.cx, this.cy, 24, 0, Math.PI * 2); ctx.fill();
370	      }
371	    } else {
372	      // 六角波纹 Extra_35（Main.cs:32699-32721）：角点 i 用第 i%3 帧带、
373	      // 旋角=角点角+速度角+π；不画 464 贴图
374	      const img = extra35();
375	      const va = Math.atan2(this.vy, this.vx);
376	      const hex = this.hexPoints();
377	      for (let i = 0; i < 6; i++) {
378	        const ang = (i * Math.PI * 2) / 6;
379	        ctx.save();
380	        ctx.translate(hex[i][0], hex[i][1]);
381	        ctx.rotate(ang + va + Math.PI);
382	        if (img && img.width > 0) {
383	          const band = img.height / 3;
384	          ctx.drawImage(img, 0, (i % 3) * band, img.width, band,
385	            -img.width / 2, -band / 2, img.width, band);
386	        } else {
387	          ctx.fillStyle = '#BFE8F0';
388	          ctx.beginPath(); ctx.arc(0, 0, 8, 0, Math.PI * 2); ctx.fill();
389	        }
390	        ctx.restore();
391	      }
392	    }
393	    ctx.restore();
394	  }
395	}
396	
397	/** 闪电球 465（Projectile.cs aiStyle 88 type 段 :30860-30937 + SetDefaults :5109-5118）：
398	 *  邪教徒闪电态(:65563-65566)在头顶 100px 零速定点生成（原版 NewProjectile 速度 0——
399	 *  本仓旧实现曾坍缩为 6 速直飞 Arrow，实体化后还原定点）。
400	 *  80×80 / hostile / alpha 255 / tileCollide=false（无 timeLeft 覆写，AI 自灭）。
401	 *  生命周期：ai0<180 淡入 alpha−5/t（钳 0）；≥180 淡出 +5/t，≥255 Kill（:30870-30887）。
402	 *  每逢 ai0%30==0 且 <180（:30889-30917）：对 ≤5 个 <2000px 且 Collision.CanHit
403	 *  （1×1 点对）的玩家各掷一颗 466 闪电链（LightningBoltProj）——方向=弹心→玩家心
404	 *  RotatedByRandom(0.785) 归一 ×7 速、ai0=该方向角、ai1=Next(100) 种子。
405	 *  4 帧循环（frameCounter≥4 推帧，projFrames[465]=4，:30919-30925）；AddLight
406	 *  (0.4,0.85,0.9)；alpha<150 且 ai0<180 时每子步 2 圈尘 226（半径 w×0.2/0.6，
407	 *  速度=离心 2 / 0，:30929-30960）。首帧 Item_121 音（:30864-30867）保留在教徒
408	 *  调用点（任务约定不双播）。接触伤害=传入 damage（教徒闪电 45）。 */
409	export class LightningOrb extends Entity {
410	  readonly projId = 465;
411	  damage: number;
412	  w = 80; h = 80;                  // SetDefaults :5110-5111
413	  private ai0 = 0;
414	  private alpha = 255;
415	  private frameCounter = 0;
416	  private frame = 0;               // projFrames[465]=4（vanilla-projframes.json）
417	
418	  /** x/y = NewProjectile 的 X/Y（中心锚 = 教徒 Center −(0,100)）；速度恒 0 */
419	  constructor(x: number, y: number, damage: number) {
420	    super();
421	    this.x = x - this.w / 2;
422	    this.y = y - this.h / 2;
423	    this.damage = damage;
424	  }
425	
426	  fixedUpdate(_dt: number, game: GameHooks): void {
427	    // 淡入/淡出（:30870-30887）
428	    if (this.ai0 < 180) this.alpha = Math.max(0, this.alpha - 5);
429	    else {
430	      this.alpha = Math.min(255, this.alpha + 5);
431	      if (this.alpha >= 255) { this.dead = true; return; }
432	    }
433	    this.ai0++;
434	    // 每 30t 掷 466（:30889-30917；单人=1 目标，CanHit 1×1 点对视线门）
435	    if (this.ai0 % 30 === 0 && this.ai0 < 180) {
436	      const p = game.player;
437	      if (p && !p.dead) {
438	        const dist = Math.hypot(p.cx - this.cx, p.cy - this.cy);
439	        if (dist < 2000
440	          && canHit(game.world.store, this.cx, this.cy, 1, 1, p.cx, p.cy, 1, 1)) {
441	          const v83x = p.cx - this.cx, v83y = p.cy - this.cy;
442	          const seed = Math.floor(Math.random() * 100);      // Main.rand.Next(100)
443	          // Normalize(v83.RotatedByRandom(0.785))×7（:30913-30914）
444	          const [rvx, rvy] = rot(v83x, v83y, (Math.random() - 0.5) * 2 * 0.7853981852531433);
445	          const d = Math.hypot(rvx, rvy) || 1;
446	          const bolt = new LightningBoltProj(this.cx, this.cy,
447	            (rvx / d) * 7, (rvy / d) * 7, 466, this.damage,
448	            Math.atan2(v83y, v83x), seed);
449	          (game as unknown as { entities: { add: (en: Entity, b: string) => void } }).entities
450	            .add(bolt, 'projectiles');
451	        }
452	      }
453	    }
454	    game.addLightAt?.(this.cx, this.cy, 0.4, 0.85, 0.9);     // :30918
455	    // 4 帧循环（:30919-30925）
456	    if (++this.frameCounter >= 4) {
457	      this.frameCounter = 0;
458	      this.frame = (this.frame + 1) % 4;
459	    }
460	    // 尘 226 双圈（:30929-30960；速度 0 → RotatedBy(0) 不转；alpha≥150 或 ≥180t 停）
461	    if (this.alpha < 150 && this.ai0 < 180) {
462	      for (const [radius, centrifugal] of [[this.w * 0.2, true], [this.w * 0.6, false]] as const) {
463	        const a = (Math.random() - 0.5) * Math.PI * 2;       // num781 ∈ ±0.5 ×2π
464	        const ox = Math.cos(a) * radius, oy = Math.sin(a) * radius;
465	        const d = game.spawnDust?.(this.cx + ox, this.cy + oy, 0, 0, 226,
466	          0, 0, 150, null, 0.7, true);
467	        if (d && centrifugal) {
468	          // 内圈尘离心 2（:30946）；外圈速度 0（:30958）
469	          const dl = Math.hypot(d.x - this.cx, d.y - this.cy) || 1;
470	          d.vx = ((d.x - this.cx) / dl) * 2;
471	          d.vy = ((d.y - this.cy) / dl) * 2;
472	        }
473	      }
474	    }
475	    // 接触伤害（hostile；敌弹 ×2 缩放在 hitPlayer 内）
476	    hitPlayer(this, game, this.damage);
477	    hitTownNpcs(this, game, this.damage, 0, 'hostile');
478	    hitCritters(this, game);
479	  }
480	
481	  draw(r: Renderer, _cam: Camera): void {
482	    // Main.cs:32812 帧切分支：Projectile_465.png 四帧行按 frame 切片居中、alpha 渐显
483	    const ctx = r.canvas.getContext('2d');
484	    if (!ctx) return;
485	    const bright = (255 - this.alpha) / 255;
486	    if (bright <= 0) return;
487	    const img = projFrameImg(465, this.frame) ?? projSprite(465);
488	    ctx.save();
489	    ctx.imageSmoothingEnabled = false;
490	    ctx.globalAlpha = bright;
491	    if (img && img.width > 0) {
492	      ctx.drawImage(img, this.cx - img.width / 2, this.cy - img.height / 2,
493	        img.width, img.height);
494	    } else {
495	      ctx.fillStyle = '#9FE8F0';
496	      ctx.beginPath(); ctx.arc(this.cx, this.cy, 28, 0, Math.PI * 2); ctx.fill();
497	    }
498	    ctx.restore();
499	  }
500	}
501	
502	/** 克隆体生成出口(:65646-65650 NewNPC 440:X,Y 是底部中心坐标且 Y 再 +真身 height/2;
503	 *  ai[3]=真身 whoAmI / localAI[1]=仪式代数)。本仓:la3=真身引用、la1=代数、跳过出生显影 */
504	function spawnCultistClone(game: GameHooks, parent: Enemy, x: number, y: number, gen: number): Enemy | null {
505	  const c = spawnPart(game, parent, 440);
506	  if (!c) return null;
507	  const la = laOf(c);
508	  la.la3 = parent;
509	  la.la1 = gen;
510	  c.x = x - c.w / 2;
511	  c.y = y + parent.h / 2 - c.h;
512	  c.bInit = true; // 原版克隆体会落入 1t 的 -1 显影态(:65047),无实际效果,直接跳过
513	  return c;
514	}
515	
516	/** 克隆体补射 468(:65375-65397 冰雾 / :65462-65499 火球第三拍 / :65531-65562 闪电 /
517	 *  :65796-65822 光第三拍):每只克隆体朝玩家(预判 20t)发 count 发,18 伤,
518	 *  (6+rand4) 速 ±spread 散布,出口 = 克隆体中心 + (facing*30, 12) */
519	function cloneSupplement(game: GameHooks, clones: Enemy[], player: Player, count: number, spread: number): void {
520	  for (const c of clones) {
521	    const dir = Math.sign(player.cx - c.cx);
522	    if (dir !== 0) c.facing = dir;
523	    const aim = aimLead(c, player, c.facing);
524	    for (let k = 0; k < count; k++) {
525	      const spd = 6 + Math.random() * 4;
526	      const [dvx, dvy] = rot(aim.x * spd, aim.y * spd, (Math.random() - 0.5) * 2 * spread);
527	      shoot(game, c.cx + c.facing * 30, c.cy + 12, dvx, dvy, 18, 468);
528	    }
529	  }
530	}
531	
532	/** 仪式圈心(原版 Projectile 490 的位置 = 仪式开始时真身中心,:65652)。
533	 *  真身存 la2;克隆体读真身的 la2 */
534	function ritualCenterOf(isReal: boolean, la: { la2: unknown }, parent: Enemy | null): { x: number; y: number } | null {
535	  const raw = (isReal ? la.la2 : (parent ? laOf(parent).la2 : null)) as { x: number; y: number } | null;
536	  return raw ?? null;
537	}
538	
539	/** 教徒 FindFrame 帧机状态（counter+帧行对；localAI 槽被仪式圈心/克隆引用
540	 *  占用（la2/la3 勿动）→ 独立 WeakMap 落盘） */
541	const cultistAnim = new WeakMap<Enemy, { fc: number; row: number }>();
542	
543	/** AI 态 → 原版 FindFrame localAI[2] 帧态六值（写点行号）：
544	 *  出生显形分段 :65120-65136（>360→13 / >300→10 / >120→1 / 其余→0，先自增
545	 *  后分段——本函数在 AI 自增前调用故 +1）/ 选招 :65148→10 / 飞掠 :65348→10 /
546	 *  冰 :65365→11 / 火 :65436→11 / 雷 :65520-65524→真身 12·克隆 11（flag2 门）/
547	 *  仪式 :65575 头部→10，[30,90) 与 [120,420) 两窗按到圈心向量覆写
548	 *  （|uy|<0.77→11 / uy<0→12 / 其余→10，:65657-65702/:65730-65763 同构）/
549	 *  硬直 :65786→13 / 光 :65811→11 / 末日 :65878→13 */
550	function cultistFrameState(
551	  e: Enemy, la: ReturnType<typeof laOf>, isReal: boolean, parent: Enemy | null,
552	): number {
553	  switch (e.ai0) {
554	    case -1: {
555	      const s = e.ai1 + 1;
556	      return s > 360 ? 13 : s > 300 ? 10 : s > 120 ? 1 : 0;
557	    }
558	    case 5: {
559	      const tt = e.ai1;
560	      if ((tt >= 30 && tt < 90) || (tt >= 120 && tt < 420)) {
561	        const cir = ritualCenterOf(isReal, la, parent);
562	        if (cir) {
563	          let dx = cir.x - e.cx, dy = cir.y - e.cy;
564	          const d = Math.hypot(dx, dy);
565	          if (d === 0) { dx = 0; dy = -1; } else { dx /= d; dy /= d; }
566	          return Math.abs(dy) < 0.77 ? 11 : dy < 0 ? 12 : 10;
567	        }
568	      }
569	      return 10;
570	    }
571	    case 4: return isReal ? 12 : 11;
572	    case 6: return 13;
573	    case 8: return 13;
574	    case 2:
575	    case 3:
576	    case 7: return 11;
577	    default: return 10;   // 选招 0 / 飞掠 1
578	  }
579	}
580	
581	/** 教徒 FindFrame 副本（NPC.cs:72698-72783）：帧态→帧行——
582	 *  态0→行0 / 态1→行1 / 态2→行2 定格（先播一轮行带再落定格行）；
583	 *  态10→行4-6 / 态11→行10-12 / 态12→行7-9 / 态13→行13-15 恒循环。
584	 *  节拍 15t 一轮、行内 5t/帧（cs:72719 ≥15 回卷、cs:72726 /5），
585	 *  counter 每 tick +1（cs:72781）；帧号直写 customFrameIdx（694 先例） */
586	function cultistFrameTick(e: Enemy, st: number): void {
587	  let a = cultistAnim.get(e);
588	  if (!a) { a = { fc: 0, row: 0 }; cultistAnim.set(e, a); }
589	  const wrap = a.fc >= 15;
590	  if (wrap) a.fc = 0;
591	  const seg = Math.floor(a.fc / 5);
592	  switch (st) {
593	    case 0:
594	      if (wrap) a.row = 0;
595	      else if (a.row !== 0) a.row = seg + 4;
596	      break;
597	    case 10: a.row = seg + 4; break;
598	    case 1:
599	      if (wrap) a.row = 1;
600	      else if (a.row !== 1) a.row = seg + 10;
601	      break;
602	    case 11: a.row = seg + 10; break;
603	    case 2:
604	      if (wrap) a.row = 2;
605	      else if (a.row !== 2) a.row = seg + 7;
606	      break;
607	    case 12: a.row = seg + 7; break;
608	    case 13: a.row = seg + 13; break;
609	  }
610	  a.fc += 1;
611	  e.customFrameIdx = a.row;
612	}
613	
614	export function lunaticCultistAI(e: Enemy, game: GameHooks, player: Player | null): void {
615	  const la = laOf(e);
616	  // getGoodWorld 弹幕节奏抬档(:64932-64958):冰 num120−30 / 火 18×3→10×5 /
617	  // 闪电 num80−20(expert 基线未实装,g 照原文在经典值上调整)
618	  const ftw = !!game.world.seedFlags?.getGoodWorld;
619	  const isReal = e.vanillaId !== 440; // flag2 = type==439(:64971);440 = 克隆体
620	  let parent: Enemy | null = null;
621	  // ---- 克隆体镜像段(:64998-65015):真身失效 → 消散;ai0/ai1 逐 tick 镜像;
622	  //      仪式态中被击中 → 自身消散 + 真身进 6 态硬直 ----
623	  if (!isReal) {
624	    parent = (la.la3 as unknown as Enemy) ?? null;
625	    if (!parent || parent.dead || parent.vanillaId !== 439) { // :64975-64982
626	      e.dead = true;
627	      return;
628	    }
629	    e.ai0 = parent.ai0;
630	    e.ai1 = parent.ai1;
631	    if (e.ai0 === 5) {
632	      if (e.justHit) { // :65003-65014
633	        game.spawnParticles(e.cx, e.cy, '#8060D0', 14, 2.4);
634	        e.dead = true;
635	        parent.ai0 = 6;
636	        parent.ai1 = 0;
637	        return;
638	      }
639	    } else {
640	      e.iframes = 2; // flag3/flag4 → dontTakeDamage(chaseable=false,:65015)
641	    }
642	  } else if (!e.bInit) {
643	    // :65047-65057 localAI[0]==0:音效 + alpha=255 + ai[0]=-1(出生显形)
644	    e.bInit = true;
645	    e.ai0 = -1; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
646	    la.la0 = 1;
647	    e.spawnAlpha = 254;
648	    game.playSfxWav?.('Zombie_89', 1, e.cx, e.cy);   // :65093 PlaySound(29,…,89)——case29 style89 ×0.7 自动档(曾借 roar 0.6)
649	  }
650	  // 环境声（:64923-64926）：ai0≠-1 时 1/1000 播 Next(88,92)=Zombie_88-91 变体池
651	  if (e.ai0 !== -1 && Math.floor(Math.random() * 1000) === 0) {
652	    game.playSfxWav?.(`Zombie_${88 + Math.floor(Math.random() * 4)}`, 1, e.cx, e.cy);
653	  }
654	  const b = baseOf(e);
655	  const phase2 = e.hp <= e.maxHp / 2;                       // flag :64928
656	  e.def.defense = Math.floor(phase2 ? b.def * 0.65 : b.def); // :64982-64985 半血防御 ×0.65
657	
658	  // :65060-65088 玩家死/超 5600px → 消散退场(连带清全部克隆体,:65078-65087)
659	  if (!player || player.dead || Math.hypot(player.cx - e.cx, player.cy - e.cy) > 5600) {
660	    game.spawnParticles(e.cx, e.cy, '#6040A0', 14, 2.4);
661	    if (isReal) {
662	      for (const c of cultistClones(game, e)) {
663	        game.spawnParticles(c.cx, c.cy, '#6040A0', 10, 2);
664	        c.dead = true;
665	      }
666	    }
667	    e.dead = true;
668	    return;
669	  }
670	
671	  // ---- 仪式窗口(120-420t)真身被击中(:65012-65056):推进选招 + 清同代克隆体(≤10)
672	  //      + 仪式圈 ai[1]=-1 快速淡出且不召龙（:65054 Main.projectile[ai[2]].ai[1] = -1）----
673	  if (isReal && e.ai0 === 5 && e.ai1 >= 120 && e.ai1 < 420 && e.justHit) {
674	    e.ai0 = 0; e.ai1 = 0; e.ai3 += 1; // :65014-65016
675	    e.vx = 0; e.vy = 0;
676	    let budget = 10; // num9 经典 10(expert 3,:65027-65031);两分支同为清场,差异仅联网消息
677	    for (const c of cultistClones(game, e)) {
678	      if (budget <= 0) break;
679	      budget--;
680	      game.spawnParticles(c.cx, c.cy, '#8060D0', 12, 2.4);
681	      c.dead = true;
682	    }
683	    const circle = la.la3;
684	    if (circle instanceof CultistRitualCircle) circle.interrupt();
685	  }
686	
687	  // ---- FindFrame 帧机（cs:72698-72783）：原版 localAI[2] 六态→帧行；本仓 la2
688	  //      已挪用存仪式圈心（勿动）→ 帧态按各态语义重算（见 cultistFrameState），
689	  //      帧号直写 customFrameIdx（Renderer 首行直读，694 先例）。状态机各块早退
690	  //      前先走本段（与原版 AI 内写 localAI[2]、AI 后 FindFrame 的时序等价）；
691	  //      netPuppet 无本地 AI → 帧冻结（登记）----
692	  cultistFrameTick(e, cultistFrameState(e, la, isReal, parent));
693	
694	  // 朝向(:65117-65120 sign(player.X - center.X);仪式态内被 :65676 系圈心朝向覆盖)
695	  const face = Math.sign(player.cx - e.cx);
696	  if (face !== 0) e.facing = face;
697	
698	  // ---- ai0 == -1 出生显形(:65059-65109):420t,前段不可选中;300t 起上浮 ----
699	  if (e.ai0 === -1) {
700	    e.spawnAlpha = Math.max(0, 254 - e.ai1 * 5); // :65066 alpha -= 5/tick
701	    e.iframes = 2; // flag3/flag4 → dontTakeDamage
702	    e.ai1 += 1;
703	    if (e.ai1 > 360) { e.vx *= 0.95; e.vy *= 0.95; }      // :65109-65111 收势阻尼
704	    else if (e.ai1 > 300) { e.vx = 0; e.vy = -1; }        // :65113-65115 velocity=-UnitY
705	    // :65117-65124 显形末段(>360)播 (29,…,105)=Zombie_105(case29 ×0.25 档,终审补)
706	    if (e.ai1 === 361) game.playSfxWav?.('Zombie_105', 1, e.cx, e.cy);
707	    flyIntegrate(e);
708	    if (e.ai1 >= 420) { e.ai0 = 0; e.ai1 = 0; e.spawnAlpha = 0; }
709	    return;
710	  }
711	
712	  // ---- ai0 == 0 选招(:65110-65336):40t 后按 ai3 拍号取招(flag2 门控,克隆体不选) ----
713	  if (e.ai0 === 0) {
714	    e.ai1 += 1;
715	    if (isReal && e.ai1 >= 40) {
716	      e.ai1 = 0;
717	      const pick = cultistPick(e, phase2);
718	      if (pick === 0) {
719	        // 飞掠占位(:65277-65336):真身 + 全部克隆体一起入环——环位角
720	        // num16 = ((序号+flag5+1)/2)·2π·0.4/总数,奇数序取负(flag5=总数偶数),
721	        // 半径椭圆 (300,200),自转轴 (0,-1)。
722	        // num14 = ceil(真身到 (玩家中心+(0,-100)) 距离/50)（:65271 真身口径,全员共用
723	        // ——曾按各成员自身落点分别计算),velocity = 位移/num14,ai1 = num14*2
724	        const num14 = Math.max(1, Math.ceil(
725	          Math.hypot(player.cx - e.cx, player.cy - 100 - e.cy) / 50));
726	        const group = [e, ...cultistClones(game, e)];
727	        const flag5 = group.length % 2 === 0 ? 1 : 0; // :65286
728	        let idx = 0;
729	        for (const m of group) {
730	          let num16 = Math.floor((idx + flag5 + 1) / 2) * Math.PI * 2 * 0.4 / group.length; // :65291-65296
731	          if (idx % 2 === 1) num16 = -num16;
732	          if (group.length === 1) num16 = 0;
733	          const [ux, uy] = rot(0, -1, num16);
734	          const destX = player.cx + ux * 300;
735	          const destY = player.cy + uy * 200;
736	          m.vx = (destX - m.cx) / num14;
737	          m.vy = (destY - m.cy) / num14;
738	          m.ai0 = 1;
739	          m.ai1 = num14 * 2;
740	          // :65305-65308 whoAmI >= 自身 → 选招当帧回退(净位移 0);克隆体按 id 序决定
741	          if (m === e || e.id >= m.id) { m.x -= m.vx; m.y -= m.vy; }
742	          idx++;
743	        }
744	      } else if (pick === 1) { e.ai0 = 3; } // 火球
745	      else if (pick === 2) { e.ai0 = 2; }   // 冰雾
746	      else if (pick === 3) { e.ai0 = 4; }   // 闪电
747	      else if (pick === 4) { e.ai0 = 5; }   // 仪式瞬移
748	      else if (pick === 5) { e.ai0 = 7; }   // 远古之光
749	      // pick === 6(远古末日)仅 expert 随机替换会命中(:65270-65275),经典不触发
750	    }
751	    flyIntegrate(e);
752	    return;
753	  }
754	
755	  // ---- ai0 == 1 飞掠(:65338-65361):奇数拍回退位移 → 实际隔拍移动;期间无敌(flag3) ----
756	  if (e.ai0 === 1) {
757	    e.iframes = 2;
758	    const undo = Math.floor(e.ai1) % 2 !== 0 && e.ai1 !== 1; // :65341-65344
759	    if (!undo) flyIntegrate(e);
760	    e.ai1 -= 1;
761	    if (e.ai1 <= 0) { e.ai0 = 0; e.ai1 = 0; if (isReal) e.ai3 += 1; e.vx = 0; e.vy = 0; }
762	    return;
763	  }
764	
765	  // ---- ai0 == 2 冰雾 464(:65362-65429):4t 时克隆体各补 1 发 468 + 真身 1 发 464(35 伤);
766	  //      持续 4+num(num=120,FTW −30 :64932-64936) ----
767	  if (e.ai0 === 2) {
768	    const numIce = ftw ? 90 : 120;
769	    if (isReal && e.ai1 >= 4 && (e.ai1 - 4) % numIce === 0) {
770	      cloneSupplement(game, cultistClones(game, e), player, 1, 0.5235987901687622); // :65375-65397
771	      // :65411-65421 发的是 ai[1]=1 母云(IceMistCloud 实体,Projectile.cs:30763-30790)——
772	      // 每 30t 沿自转派生子体,150t 寿终;曾坍缩为单发直飞 Arrow(旧注释「直飞桶」);
773	      // Item_120 首帧音随实体化迁入 IceMistCloud 首帧(母云+每颗子体各播,:30749-30752)
774	      const aim = aimLead(e, player, e.facing);
775	      const cloud = new IceMistCloud(e.cx + e.facing * 30, e.cy + 12,
776	        aim.x * 4, aim.y * 4, 35, true);
777	      (game as unknown as { entities: { add: (en: Entity, b: string) => void } }).entities
778	        .add(cloud, 'projectiles');
779	      // 原版冰雾发射零吼(:65040-65900 全段仅 65093/65122 两声)——曾借 roar 0.35,2026-08-18 对账删
780	    }
781	    e.ai1 += 1;
782	    if (e.ai1 >= 4 + numIce) { e.ai0 = 0; e.ai1 = 0; if (isReal) e.ai3 += 1; e.vx = 0; e.vy = 0; }
783	    return;
784	  }
785	
786	  // ---- ai0 == 3 火球 467(:65430-65530):每 num2t 一发×num3,30 伤,(6+rand4) 速
787	  //      ±0.52rad 散布(18×3,FTW 10×5 :64941-64949);第三拍克隆体各补 1 发
788	  //      468(:65462-65499);持续 4+num2*num3 ----
789	  if (e.ai0 === 3) {
790	    const numFire = ftw ? 10 : 18;
791	    const fireCount = ftw ? 5 : 3;
792	    if (isReal && e.ai1 >= 4 && (e.ai1 - 4) % numFire === 0) {
793	      // 原版硬编码第 3 拍(:65442 /num2==2)——FTW 5 拍下仍在第 3 拍补射,1:1 保留
794	      if ((e.ai1 - 4) / numFire === 2) {
795	        cloneSupplement(game, cultistClones(game, e), player, 1, 0.5235987901687622); // :65448-65462
796	      }
797	      const aim = aimLead(e, player, e.facing);
798	      const spd = 6 + Math.random() * 4;
799	      const [dvx, dvy] = rot(aim.x * spd, aim.y * spd, (Math.random() - 0.5) * 2 * 0.5235987901687622);
800	      shoot(game, e.cx + e.facing * 30, e.cy + 12, dvx, dvy, 30, 467); // :65505-65517
801	    }
802	    e.ai1 += 1;
803	    if (e.ai1 >= 4 + numFire * fireCount) { e.ai0 = 0; e.ai1 = 0; if (isReal) e.ai3 += 1; e.vx = 0; e.vy = 0; }
804	    return;
805	  }
806	
807	  // ---- ai0 == 4 闪电 465(:65531-65622):ai1==20 时克隆体各补 1 发 468(:65531-65562),
808	  //      之后每逢 (ai1-20)%num4==0 在头顶 100px 撒 465(45 伤)(num4=80,FTW −20
809	  //      :64952-64958);持续 20+num4 ----
810	  if (e.ai0 === 4) {
811	    const numBolt = ftw ? 60 : 80;
812	    if (isReal && e.ai1 >= 20 && (e.ai1 - 20) % numBolt === 0) {
813	      if (e.ai1 === 20) {
814	        cloneSupplement(game, cultistClones(game, e), player, 1, 0.5235987901687622);
815	        // 原版闪电发射零吼(同上全段普查)——曾借 roar 0.5,2026-08-18 对账删
816	      }
817	      // 原版 465 零速定点 180t(LightningOrb 实体,Projectile.cs:30860-30937),每 30t
818	      // 朝 ≤5 玩家掷 466 闪电链——曾坍缩为 6 速直飞 Arrow,实体化还原定点悬停
819	      const orb = new LightningOrb(e.cx, e.cy - 100, 45);   // :65563-65566(速度 0/45 伤)
820	      (game as unknown as { entities: { add: (en: Entity, b: string) => void } }).entities
821	        .add(orb, 'projectiles');
822	      game.playSfxWav?.('Item_121', 1, e.cx, e.cy - 100);   // 弹 465 首帧音(:30864-30867,保留调用点播,防实体内双播)
823	    }
824	    e.ai1 += 1;
825	    if (e.ai1 >= 20 + numBolt) { e.ai0 = 0; e.ai1 = 0; if (isReal) e.ai3 += 1; e.vx = 0; e.vy = 0; }
826	    return;
827	  }
828	
829	  // ---- ai0 == 5 仪式瞬移(:65623-65770):0-30 淡出,30 环位重定位 + 生成/补位克隆体,
830	  //      30-90 隐形,90-120 淡入,120-420 显形可受击(打真身/克隆体窗口);持续 420 ----
831	  if (e.ai0 === 5) {
832	    const t = e.ai1;
833	    if (t >= 0 && t < 30) {
834	      e.spawnAlpha = Math.floor((t / 30) * 254);
835	      e.iframes = 2; // flag3/flag4
836	    } else if (t >= 30 && t < 90) {
837	      e.spawnAlpha = 254;
838	      e.iframes = 2;
839	      if (t === 30 && isReal) {
840	        // :65636-65675:环绕自身半径 180 的 num29 环位重定位——
841	        //   补位克隆体(总数目标 6,每轮至多新造 2),余下槽位重排既有克隆体;
842	        //   真身取「距玩家最远」槽(num31 = 最近槽的对侧);圈心(=重定位前中心)存
843	        //   la2 供本态朝向用,并于此原位发 490 仪式圈弹（:65643，ai[1]=真身索引）
844	        la.la1 += 1; // localAI[1] 仪式代数(:65637)
845	        la.la2 = { x: e.cx, y: e.cy };
846	        // ai[2] = 490 仪式圈弹索引（:65652）——真身 la3 反存圈引用供中断链（:65054）
847	        const circle = new CultistRitualCircle(e);
848	        la.la3 = circle;
849	        (game as unknown as { entities: { add: (en: Entity, b: string) => void } }).entities
850	          .add(circle, 'projectiles');
851	        const clones = cultistClones(game, e);
852	        let num28 = 6 - clones.length; // :65643-65647
853	        if (num28 > 2) num28 = 2;
854	        const num29 = clones.length + num28 + 1;
855	        const dists: number[] = [];
856	        for (let s = 0; s < num29; s++) { // :65650-65656 各槽到玩家距离
857	          const [rx, ry] = rot(180, 0, (s * Math.PI * 2) / num29 - Math.PI / 2);
858	          dists.push(Math.hypot(e.cx + rx - player.cx, e.cy + ry - player.cy));
859	        }
860	        let num31 = 0; // :65658-65664 取最近槽 → 映射到对侧(最远)槽
861	        for (let s = 1; s < num29; s++) if (dists[num31] > dists[s]) num31 = s;
862	        num31 = num31 >= num29 / 2 ? num31 - Math.floor(num29 / 2) : num31 + Math.floor(num29 / 2);
863	        let num33 = num28; // :65666 新造配额,耗尽后按序重排既有克隆体(list6[-num33-1])
864	        let reused = 0;
865	        for (let s = 0; s < num29; s++) {
866	          if (num31 === s) continue;
867	          const [rx, ry] = rot(180, 0, (s * Math.PI * 2) / num29 - Math.PI / 2);
868	          const px = e.cx + rx, py = e.cy + ry;
869	          if (num33-- > 0) spawnCultistClone(game, e, px, py, la.la1);
870	          else if (reused < clones.length) {
871	            const c = clones[reused++];
872	            c.x = px - c.w / 2;
873	            c.y = py - c.h / 2;
874	          }
875	        }
876	        // 真身移到 num31 槽(:65652 Center += 偏移向量)
877	        const [fx, fy] = rot(180, 0, (num31 * Math.PI * 2) / num29 - Math.PI / 2);
878	        e.x += fx;
879	        e.y += fy;
880	        e.vx = 0; e.vy = 0;
881	        game.spawnParticles(e.cx, e.cy, '#8060D0', 18, 2.6);
882	        // 原版仪式圈就位零吼(同上全段普查)——曾借 roar 0.7,2026-08-18 对账删
883	      }
884	    } else if (t >= 90 && t < 120) {
885	      e.spawnAlpha = Math.floor(254 * (1 - (t - 90) / 30));
886	      e.iframes = 2;
887	    } else {
888	      // 120-420:显形且可受击(alpha=0,不置 iframes;chaseable 原版为 false,:65954)
889	      e.spawnAlpha = 0;
890	      // 朝向:以仪式圈心为基准(:65706-65719 / :65743-65756 sign(圈心-自身).X)
891	      const cir = ritualCenterOf(isReal, la, parent);
892	      if (cir) {
893	        const dx = cir.x - e.cx;
894	        if (dx !== 0) e.facing = Math.sign(dx);
895	      }
896	    }
897	    e.ai1 += 1;
898	    if (e.ai1 >= 420) { e.ai0 = 0; e.ai1 = 0; if (isReal) e.ai3 += 1; e.vx = 0; e.vy = 0; }
899	    return;
900	  }
901	
902	  // ---- ai0 == 6 硬直(:65771-65784):打中克隆体后真身暴露(不置 iframes),120t 后回选招 ----
903	  if (e.ai0 === 6) {
904	    e.ai1 += 1;
905	    if (e.ai1 >= 120) { e.ai0 = 0; e.ai1 = 0; if (isReal) e.ai3 += 1; e.vx = 0; e.vy = 0; }
906	    flyIntegrate(e);
907	    return;
908	  }
909	
910	  // ---- ai0 == 7 远古之光(:65796-65877):每 20t 一轮×2;第三拍克隆体各补 5 发 468
911	  //      (±1.2566rad,:65796-65822),真身每轮以扇面(步进 2π/25,8 速)召 5 只 NPC522
912	  //      (:65862-65865,ai1=逐 t 弯转角 → AI_100 轨道弹);持续 4+20*2 ----
913	  if (e.ai0 === 7) {
914	    if (isReal && e.ai1 >= 4 && (e.ai1 - 4) % 20 === 0) {
915	      e.facing = Math.sign(player.cx - e.cx) || e.facing; // :65839-65843
916	      const aim = aimLead(e, player, e.facing);
917	      const num47 = (Math.PI * 2) / 25; // :65856
918	      if ((e.ai1 - 4) / 20 === 2) {
919	        cloneSupplement(game, cultistClones(game, e), player, 5, 1.2566370964050293);
920	      }
921	      for (let i = 0; i < 5; i++) {
922	        const [dvx, dvy] = rot(aim.x * 8, aim.y * 8, num47 * i - (Math.PI * 2 / 5 - num47) / 2); // :65860
923	        const n = spawnPart(game, e, 522);
924	        if (n) {
925	          // NewNPC(..., vector15.X, vector15.Y + 7, 522, ...) → X=中心横坐标,Y=底部纵坐标
926	          n.ai0 = 0;
927	          n.ai1 = (Math.random() - 0.5) * 0.3 * (Math.PI * 2) / 60; // :65861 逐 t 弯转角
928	          n.ai2 = dvx; n.ai3 = dvy;                                  // 初速(AI_100 首拍取用)
929	          n.x = e.cx + e.facing * 30 - n.w / 2;
930	          n.y = e.cy + 12 + 7 - n.h;
931	          n.vx = dvx; n.vy = dvy;
932	        }
933	      }
934	      // 原版火球(522)发射零吼(同上全段普查)——曾借 roar 0.5,2026-08-18 对账删
935	    }
936	    e.ai1 += 1;
937	    if (e.ai1 >= 4 + 20 * 2) { e.ai0 = 0; e.ai1 = 0; if (isReal) e.ai3 += 1; e.vx = 0; e.vy = 0; }
938	    return;
939	  }
940	
941	  // ---- ai0 == 8 远古末日(:65873-65932):玩家附近随机空位撒 NPC523,数量 = min(克隆体+1, 3)
942	  //      (:65892-65897);经典选招表不含 6(expert 随机替换专属,:65270-65275),状态体保留 ----
943	  if (e.ai0 === 8) {
944	    if (isReal && e.ai1 >= 4 && (e.ai1 - 4) % 20 === 0) {
945	      const st = game.world.store;
946	      const ptx = Math.floor(player.cx / TILE), pty = Math.floor(player.cy / TILE);
947	      const etx = Math.floor(e.cx / TILE), ety = Math.floor(e.cy / TILE);
948	      const want = Math.min(cultistClones(game, e).length + 1, 3);
949	      for (let k = 0; k < want; k++) {
950	        for (let tries = 0; tries < 100; tries++) { // :65904-65931 空位采样
951	          const tx = ptx + Math.floor(Math.random() * 41) - 20;
952	          const ty = pty + Math.floor(Math.random() * 41) - 20;
953	          const nearPlayer = Math.abs(ty - pty) <= 7 && Math.abs(tx - ptx) <= 7;
954	          const nearSelf = Math.abs(ty - ety) <= 3 && Math.abs(tx - etx) <= 3;
955	          if (nearPlayer || nearSelf || !st.inBounds(tx, ty) || st.isSolid(tx, ty)) continue;
956	          const n = spawnPart(game, e, 523);
957	          if (n) {
958	            n.x = tx * TILE + 8 - n.w / 2;
959	            n.y = ty * TILE + 8 - n.h / 2;
960	            n.vx = 0; n.vy = 0;
961	            n.ai0 = e.id; // :65930 ai[0] = 真身 whoAmI(本仓以运行时 id 代)
962	            n.bInit = true;
963	          }
964	          break;
965	        }
966	      }
967	    }
968	    e.ai1 += 1;
969	    if (e.ai1 >= 4 + 20 * 3) { e.ai0 = 0; e.ai1 = 0; if (isReal) e.ai3 += 1; e.vx = 0; e.vy = 0; }
970	    return;
971	  }
972	
973	  // 未知状态:回选招
974	  e.ai0 = 0; e.ai1 = 0;
975	}
976	
977	// ===================== AI_120 光之女皇 636(NPC.cs:46299-47302) =====================
978	// 状态机(ai0): 0 出生(180t) / 1 悬浮蓄力枢纽(DashTo 靠近 10t + 减速,45t(二阶段 20t)选招)/
979	//   2 彩虹射线 873 / 4 光枪墙 919 / 5 永恒彩虹 872 / 6 太阳舞 923 / 7 光枪回环 919(二阶段)/
980	//   8,9 刀阵冲刺(±50 速,6-40t 无敌蓄力,40-90t 伤害 ×1.5)/ 10 半血变身传送 /
981	//   13 淡出退场(目标失效/超 6400px)。3(874 天降极光)与 11/12 为 expert 专属拍,跳过。
982	// 经典弹幕伤害(:46326-46345): 919 墙 50 / 919 回环 70 / 873 45 / 872 45 / 923 50 / 874 40。
983	// 选招表(:46460-46580 残差映射): 一阶段 10 拍 [2,8,6,8,5,2,8,4,8,5] 循环,血 ≤50% 强制 10(变身);
984	//   二阶段 9 拍 [7,2,8,5,2,6,4,8,12] 循环——num37 槽位推进（flag2 时第 3 槽插 11=expert
985	//   专属拍），表尾 num57=12（873 螺旋）;反编译的 num54 双写 [..,6,6,..] 是同一 if 重复,
986	//   真表第 6 槽是 4、第 8 槽是 12。
987	const EMPRESS_CYCLE_P1 = [2, 8, 6, 8, 5, 2, 8, 4, 8, 5];
988	const EMPRESS_CYCLE_P2 = [7, 2, 8, 5, 2, 6, 4, 8, 12];
989	
990	/** 原版 AI_120_HallowBoss_DashTo(:47304-47317):目标上移 300,>200 再回退 100,
991	 *  速度 = lerp(单位向量*min(len,18), vector/6, lerpValue(100,600,len)) */
992	function empressDashTo(e: Enemy, tx0: number, ty0: number): void {
993	  let tx = tx0, ty = ty0 - 300;
994	  const d0 = Math.hypot(tx - e.cx, ty - e.cy);
995	  if (d0 > 200) {
996	    const ux = (tx - e.cx) / (d0 || 1), uy = (ty - e.cy) / (d0 || 1);
997	    tx -= ux * 100; ty -= uy * 100;
998	  }
999	  const vx = tx - e.cx, vy = ty - e.cy;
1000	  const len = Math.hypot(vx, vy) || 1;
1001	  const lv = lerpValue(100, 600, len);
1002	  const cap = Math.min(len, 18);
1003	  e.vx = vLerp((vx / len) * cap, vx / 6, lv);
1004	  e.vy = vLerp((vy / len) * cap, vy / 6, lv);
1005	}
1006	
1007	/** 悬浮趋近(:46502 系):距 (玩家+偏移) > 40 才以 SimpleFlyMovement(dir*12, 0.5) 靠近 */
1008	function empressHover(e: Enemy, player: Player, ox: number, oy: number, spdMul = 1, accMul = 1): void {
1009	  const tx = player.cx + ox, ty = player.cy + oy;
1010	  if (Math.hypot(tx - e.cx, ty - e.cy) > 40) {
1011	    const dx = tx - e.cx, dy = ty - e.cy;
1012	    const d = Math.hypot(dx, dy) || 1;
1013	    simpleFly(e, (dx / d) * 12 * spdMul, (dy / d) * 12 * spdMul, 0.5 * accMul);
1014	  }
1015	}
1016	
1017	export function empressOfLightAI(e: Enemy, game: GameHooks, player: Player | null): void {
1018	  if (!e.bInit) {
1019	    e.bInit = true;
1020	    e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
1021	    e.spawnAlpha = 254; // Opacity = ai1/180 渐显(:46410)
1022	    game.spawnParticles(e.cx, e.cy - 80, '#FFE080', 20, 2.5);
1023	  }
1024	  const phase2 = e.ai3 === 1 || e.ai3 === 3; // AI_120_HallowBoss_IsInPhase2 :46179
1025	  const dayEnrage = game.world.clock.isDay;  // flag4 = ShouldEmpressBeEnraged() = Main.dayTime（:46296）
1026	  // flag2 = Main.expertMode（:46317）；白天暴怒 flag4 时强制置真（:46355）——
1027	  // 全六处行为：num17+5（:46364）/选招起手环移（:46603）/case2 射速 2（:46632）/
1028	  // case4 五枪+450 环（:46711-46731）/case6 八辐（:46859）/case7 六线 18 枪（:46888）
1029	  const flag2 = game.world.isExpert || dayEnrage;
1030	  // num17：二阶段 +15，flag2 再 +5（:46360-46367）——各态时长均减 num17
1031	  const num17 = (phase2 ? 15 : 0) + (flag2 ? 5 : 0);
1032	  const b = baseOf(e);
1033	  // :47296-47301 二阶段防御 ×1.2;白天暴怒（flag4,:47296 段 damage=9999——wiki"白天必秒杀"）
1034	  // ——2026-08-13 接通:白天召唤女皇不再无风险
1035	  // :46319-46323 满血+白天且未暴怒 → ai3 += 2（白天召出即 Enraged 档 2;
1036	  // 受过伤再转白天不补——原版"只在白天受过伤"语义）。NpcDrops 的
1037	  // EmpressOfLightIsGenuinelyEnraged(:46169)读 ai3∈{2,3} → 夜光 5005 掉落门
1038	  if (e.hp === e.maxHp && dayEnrage && e.ai3 !== 2 && e.ai3 !== 3) e.ai3 += 2;
1039	  e.def.damage = dayEnrage ? 9999 : b.dmg;
1040	  e.def.defense = Math.floor(phase2 ? b.def * 1.2 : b.def);
1041	
1042	  // 目标失效/超 6400px → 淡出退场(:46437-46444/:46595 num36=13;此后只有 13 态不触 player)
1043	  // flag12（:46584-46594）：真狂暴（ai3∈{2,3}）且（入夜 或 白天 Main.time≥53400——
1044	  // 昼 54000t 的末 600t ≈ 19:20PM 后）→ 强制 13 态离场。Main.time 换算：
1045	  // (timeOfDay − DAWN) × 86400（昼 0.625 天 ↔ 54000t）
1046	  const genuinelyEnraged = e.ai3 === 2 || e.ai3 === 3;
1047	  const mainTime = (game.world.clock.timeOfDay - 4.5 / 24) * 86400;
1048	  const enragedLeave = genuinelyEnraged && (!dayEnrage || mainTime >= 53400);
1049	  if ((!player || player.dead || Math.hypot(player.cx - e.cx, player.cy - e.cy) > 6400 || enragedLeave) && e.ai0 !== 13) {
1050	    e.ai0 = 13; e.ai1 = 0; e.ai2 += 1;
1051	    e.vx /= 4; e.vy /= 4;
1052	  }
1053	  if (player) e.facing = e.seekDirX(player);
1054	  if (!player) {
1055	    // 目标彻底失效:上方已强制 ai0=13,此处推进淡出自毁(:47236/:47264-47271)。
1056	    // ★bossFled 同置——原版是静默 active=false,曾只写 dead 被 Game 记为"击败":
1057	    // 假公告+误写 downed_636+误触 LanternNight 且零掉落(2026-08-19 终审修)
1058	    e.spawnAlpha = Math.min(254, e.spawnAlpha + 5);
1059	    e.vx *= 0.95; e.vy *= 0.95;
1060	    e.ai1 += 1;
1061	    flyIntegrate(e);
1062	    if (e.ai1 >= 20 && e.spawnAlpha >= 254) { e.bossFled = true; e.dead = true; }
1063	    return;
1064	  }
1065	
1066	  // 冲刺窗口伤害倍率(num16,:46352/:47006):8/9 态 40-90t 时 ×1.5
1067	  // （白天 9999 基伤同样参与 ×1.5——原版 flag4 先把 num 全置 9999 再乘 num16;
1068	  //  曾按 b.dmg 重算把 9999 整档覆盖掉,白天暴怒伤害从未生效）
1069	  const dashBoost = (e.ai0 === 8 || e.ai0 === 9) && e.ai1 > 40 && e.ai1 <= 90;
1070	  // :47294-47299 damage = def×num16 后 flag4 **直接覆写 9999**（不乘 1.5）——
1071	  //  曾得 9999×1.5=14999（乘区序错，2026-08-18 审查勘误）
1072	  e.def.damage = dayEnrage ? 9999 : Math.round(b.dmg * (dashBoost ? 1.5 : 1));
1073	
1074	  switch (e.ai0) {
1075	    // ---- 0 出生(:46370-46422):velocity=(0,5) 后 0.95 阻尼,180t 渐显;全程无敌(flag6=false) ----
1076	    case 0: {
1077	      if (e.ai1 === 0) {
1078	        e.vx = 0; e.vy = 5;
1079	        // :46376 出生头顶 874 极光演出弹（0 速 0 伤）
1080	        shoot(game, e.cx, e.cy - 80, 0, 0, 0, 874);
1081	      }
1082	      if (e.ai1 === 10) game.playSfxWav?.('Item_161', 1, e.cx, e.cy);   // :46381
1083	      e.iframes = 2; // :46408-46409 flag6=false → dontTakeDamage
1084	      e.vx *= 0.95; e.vy *= 0.95;
1085	      e.spawnAlpha = Math.max(0, 254 - Math.floor(clamp(e.ai1 / 180, 0, 1) * 254));
1086	      e.ai1 += 1;
1087	      if (e.ai1 >= 180) { e.ai0 = 1; e.ai1 = 0; }
1088	      break;
1089	    }
1090	    // ---- 1 悬浮蓄力枢纽(:46418-46511):前 10t DashTo 冲近,之后阻尼;到时按表选招 ----
1091	    case 1: {
1092	      // num34 :46422(flag=二阶段 20/一阶段 45);getGoodWorld 折半(:46425-4628)
1093	      let dur = phase2 ? 20 : 45;
1094	      if (game.world.seedFlags?.getGoodWorld) dur /= 2;
1095	      if (e.ai1 <= 10) empressDashTo(e, player.cx, player.cy);
1096	      if (Math.hypot(e.vx, e.vy) > 16 && e.ai1 > 10) { e.vx /= 2; e.vy /= 2; }
1097	      e.vx *= 0.92; e.vy *= 0.92;
1098	      e.ai1 += 1;
1099	      if (e.ai1 < dur) break;
1100	      const table = phase2 ? EMPRESS_CYCLE_P2 : EMPRESS_CYCLE_P1;
1101	      let next = table[Math.floor(e.ai2) % table.length];
1102	      if (!phase2 && e.hp / e.maxHp <= 0.5) next = 10; // :46463 半血强制变身
1103	      if (next === 8 && player.cx > e.cx) next = 9;     // :46493 冲刺方向
1104	      // :46603-46606 flag2（expert/暴怒）且选招非 5/12：起手朝玩家向量旋 ±90° × 20 速
1105	      if (flag2 && next !== 5 && next !== 12) {
1106	        const side = (player.cx > e.cx ? 1 : -1);       // ToDirectionInt(目标在右)
1107	        const [svx, svy] = rot(side, 0, (Math.PI / 2) * side);
1108	        e.vx = svx * 20; e.vy = svy * 20;
1109	      }
1110	      e.ai0 = next; e.ai1 = 0; e.ai2 += 1;
1111	      break;
1112	    }
1113	    // ---- 2 彩虹射线 873(:46613-46667):悬玩家左上(-150,-250),每 num91t 一发直飞,60t 止 ----
1114	    case 2: {
1115	      if (e.ai1 === 0) game.playSfxWav?.('Item_164', 1, e.cx, e.cy);   // :46617
1116	      empressHover(e, player, -150, -250);
1117	      const dur = 60 + (90 - num17);       // num90 = 90 - num17（:46619）
1118	      const num91 = flag2 ? 2 : 3;          // :46631-46635 flag2 射速加密
1119	      if (Math.floor(e.ai1) % num91 === 0 && e.ai1 < 60) {
1120	        const [dvx, dvy] = rot(0, -6, (Math.PI / 2) * (Math.random() * 2 - 1));
1121	        shoot(game, e.cx - 55, e.cy - 30, dvx, dvy, dayEnrage ? 9999 : phase2 ? 50 : 45, 873);  // num8 :46333
1122	      }
1123	      e.ai1 += 1;
1124	      if (e.ai1 >= dur) { e.ai0 = 1; e.ai1 = 0; }
1125	      break;
1126	    }
1127	    // ---- 4 光枪墙 919(:46691-46799):悬玩家上 (0,-350),每 4t 在玩家周围环上布枪 ----
1128	    case 4: {
1129	      if (e.ai1 === 0) game.playSfxWav?.('Item_162', 1, e.cx, e.cy);   // :46697
1130	      empressHover(e, player, 0, -350);
1131	      const dur = 100 + (20 - num17);
1132	      // :46715 每 4t 布一杆;:46734 距玩家 >2400 跳过当拍(原版 continue,计时不断)
1133	      if (Math.floor(e.ai1) % 4 === 0 && e.ai1 < 100 && Math.hypot(player.cx - e.cx, player.cy - e.cy) <= 2400) {
1134	        const num82 = flag2 ? 5 : 4;       // :46710-46714 flag2 五枪
1135	        const ringR = flag2 ? 450 : 300;   // :46728-46732 flag2 环径 450
1136	        const num85 = Math.floor(e.ai1) / 4;
1137	        let ux = Math.cos(Math.PI / (num82 * 2) + num85 * (Math.PI / num82));
1138	        let uy = Math.sin(Math.PI / (num82 * 2) + num85 * (Math.PI / num82));
1139	        if (!flag2) ux += ux > 0 ? 0.5 : -0.5; // 经典横向外扩(:46723-46726,flag2 关)
1140	        const ul = Math.hypot(ux, uy) || 1; ux /= ul; uy /= ul;
1141	        if (player.vx * ux + player.vy * uy > 0) { ux = -ux; uy = -uy; } // 逆着玩家速度布枪(:46738)
1142	        const leadX = player.cx + player.vx * 90, leadY = player.cy + player.vy * 90;
1143	        let px = player.cx + ux * ringR - player.vx * 30;
1144	        let py = player.cy + uy * ringR - player.vy * 30;
1145	        const pd = Math.hypot(px - player.cx, py - player.cy);
1146	        if (pd < ringR) { // 环距不足外推(:46745-46753)
1147	          const ex = player.cx - px, ey = player.cy - py;
1148	          const el = Math.hypot(ex, ey) || 1;
1149	          px = player.cx - (ex / el) * ringR; py = player.cy - (ey / el) * ringR;
1150	        }
1151	        const ax = leadX - px, ay = leadY - py;
1152	        const al = Math.hypot(ax, ay) || 1;
1153	        // 原版 919 零速预告后沿 v4 方向冲刺(Projectile.AI 收敛:12 速直飞)
1154	        shoot(game, px, py, (ax / al) * 12, (ay / al) * 12, dayEnrage ? 9999 : phase2 ? 60 : 50, 919, 240);  // num6 :46332
1155	      }
1156	      e.ai1 += 1;
1157	      if (e.ai1 >= dur) { e.ai0 = 1; e.ai1 = 0; }
1158	      break;
1159	    }
1160	    // ---- 5 永恒彩虹 872(:46801-46841):悬玩家上,开场 13 发环形彩弹(8 速) ----
1161	    case 5: {
1162	      if (e.ai1 === 0) game.playSfxWav?.('Item_163', 1, e.cx, e.cy);   // :46805
1163	      empressHover(e, player, 0, -350);
1164	      const dur = 42 + (30 - num17);
1165	      if (Math.floor(e.ai1) % 42 === 0 && e.ai1 < 42) {
1166	        const base = Math.random() * Math.PI * 2;
1167	        for (let k = 0; k < 13; k++) {
1168	          const t = k / 13;
1169	          const [ux, uy] = rot(0, 1, Math.PI / 2 + Math.PI * 2 * t + base);
1170	          const [ox, oy] = rot(ux, uy, -Math.PI / 2);
1171	          shoot(game, e.cx + 55 + ox * 30, e.cy - 30 + oy * 30, ux * 8, uy * 8,
1172	            dayEnrage ? 9999 : phase2 ? 50 : 45, 872);   // num9 :46334
1173	        }
1174	      }
1175	      e.ai1 += 1;
1176	      if (e.ai1 >= dur) { e.ai0 = 1; e.ai1 = 0; }
1177	      break;
1178	    }
1179	    // ---- 6 太阳舞 923(:46843-46881):悬玩家上 (-80,-500) 低速,每 60t 一环,3 环 ----
1180	    case 6: {
1181	      empressHover(e, player, -80, -500, 0.3, 0.7);
1182	      const dur = 180 + (120 - num17);
1183	      const spokes = flag2 ? 8 : 6;        // num28（:46858-46862 flag2 八辐）
1184	      if (Math.floor(e.ai1) % 60 === 0 && e.ai1 < 180) {
1185	        const volley = Math.floor(e.ai1) / 60;
1186	        const flip = player.cx > e.cx ? 1 : 0;
1187	        for (let t = 0; t < 1; t += 1 / spokes) {
1188	          const slot = (t + (1 / spokes) * 0.5 + volley * (1 / spokes) * 0.5) % 1;
1189	          const a = Math.PI * 2 * (slot + flip);
1190	          // 原版 923 零速绕体公转(收敛:8 速放射)
1191	          shoot(game, e.cx, e.cy - 100, Math.cos(a) * 8, Math.sin(a) * 8,
1192	            dayEnrage ? 9999 : phase2 ? 60 : 50, 923, 240);   // num10 :46335
1193	            game.playSfxWav?.('Item_159', 1, e.cx, e.cy);   // 弹 923 首帧音(pcs:42324)
1194	        }
1195	      }
1196	      e.ai1 += 1;
1197	      if (e.ai1 >= dur) { e.ai0 = 1; e.ai1 = 0; }
1198	      break;
1199	    }
1200	    // ---- 7 光枪回环 919(二阶段,:46883-46982):每 num71t 以玩家为中心布 num74 连枪线 ----
1201	    case 7: {
1202	      empressHover(e, player, 0, -350, 0.4, 1);
1203	      // :46885-46894 flag2：间隔 40t、6 线、18 枪/线、跨距 ×0.5；经典：60t、4 线、13 枪
1204	      const num71 = flag2 ? 40 : 60;
1205	      const num72 = num71 * (flag2 ? 6 : 4);
1206	      const num70 = (flag2 ? 40 : 20) - num17;
1207	      const dur = num72 + num70;
1208	      if (Math.floor(e.ai1) % num71 === 0 && e.ai1 < num72) {
1209	        game.playSfxWav?.('Item_162', 1, e.cx, e.cy);   // :46903 每线发射（曾误 Item_160）
1210	        const line = Math.floor(e.ai1) / num71;
1211	        let cx0 = player.cx, cy0 = player.cy;
1212	        let dirX = 0, dirY = 0, axX = 0, axY = 0, toPlayer = false;
1213	        const num74 = flag2 ? 18 : 13;   // 枪数/线
1214	        const num75 = flag2 ? 200 : 150; // 枪距
1215	        const span = num74 * num75 * (flag2 ? 0.5 : 1);   // num76 :46908/:46922
1216	        switch (line) { // :46924-46956 线几何（4/5 线仅 flag2 可达,朝玩家会聚）
1217	          case 0: cx0 += -span / 2; dirX = 0; dirY = span; axX = 1; axY = 0; break;
1218	          case 1: cx0 += span / 2; cy0 += num75 / 2; dirX = 0; dirY = span; axX = -1; axY = 0; break;
1219	          case 2: cx0 += -span * 0.4; cy0 += -span * 0.4; dirX = span * 1.4; dirY = 0; axX = 1; axY = 1; break;
1220	          case 3: cx0 += span * 0.4 + num75 / 2; cy0 += -span * 0.4; dirX = -span * 1.4; dirY = 0; axX = -1; axY = 1; break;
1221	          default:
1222	            // :46946-46955 第 4/5 线（flag2 专属）：偏移 ±(span·0.4, span·0.4)（第 5 线 X 再 +num75/2）
1223	            toPlayer = true;
1224	            if (line === 4) { cx0 += -span * 0.4; cy0 += span * 0.4; dirX = span * 1.4; }
1225	            else { cx0 += span * 0.4 + num75 / 2; cy0 += span * 0.4; dirX = -span * 1.4; }
1226	            dirY = 0;
1227	            break;
1228	        }
1229	        const al = Math.hypot(axX, axY) || 1;
1230	        for (let t = 0; t <= 1.0001; t += 1 / num74) {
1231	          const ox = cx0 + dirX * (t - 0.5), oy = cy0 + dirY * (t - 0.5);
1232	          let vx = (axX / al) * 12, vy = (axY / al) * 12;
1233	          if (flag2 && toPlayer) {
1234	            // :46961-46966 flag2 第 4/5 线：枪向 = 基向向"玩家预测位"Lerp 0.75
1235	            const tx = player.cx + player.vx * 20 * t - ox, ty = player.cy - oy;
1236	            const tl = Math.hypot(tx, ty) || 1;
1237	            const lx = vLerp(1, tx / tl, 0.75), ly = vLerp(0, ty / tl, 0.75);
1238	            const ll = Math.hypot(lx, ly) || 1;
1239	            vx = (lx / ll) * 12; vy = (ly / ll) * 12;
1240	          }
1241	          shoot(game, ox, oy, vx, vy, dayEnrage ? 9999 : phase2 ? 65 : 70, 919, 240);  // num7 :46336
1242	        }
1243	      }
1244	      e.ai1 += 1;
1245	      if (e.ai1 >= dur) { e.ai0 = 1; e.ai1 = 0; }
1246	      break;
1247	    }
1248	    // ---- 8/9 刀阵冲刺(:46984-47027):0-40t 冲到玩家侧后 550px(6-40t 无敌),
1249	    //      40-90t 以 ±50 横速突进(伤害 ×1.5),其后 0.92 阻尼 ----
1250	    case 8:
1251	    case 9: {
1252	      const side = e.ai0 === 8 ? -1 : 1; // num33 :46991
1253	      if (e.ai1 === 20) game.playSfxWav?.('Item_160', 1, e.cx, e.cy);   // :46997
1254	      if (e.ai1 <= 40) {
1255	        if (e.ai1 >= 6) e.iframes = 2; // flag6 → dontTakeDamage(:46990)
1256	        const destX = player.cx + side * -550, destY = player.cy;
1257	        const dx = destX - e.cx, dy = destY - e.cy;
1258	        const d = Math.hypot(dx, dy) || 1;
1259	        simpleFly(e, (dx / d) * 12, (dy / d) * 12, 1.0);
1260	        if (e.ai1 === 40) { e.vx *= 0.3; e.vy *= 0.3; }
1261	      } else if (e.ai1 <= 90) {
1262	        // :46959-46962 Lerp(velocity, (±50,0)) 5%/t——从当前速向 ±50/0 渐进
1263	        // (40t 爬坡;曾实参颠倒=一帧跳到 95% 目标速,终审修)
1264	        e.vx = vLerp(e.vx, side * 50, 0.05);
1265	        e.vy = vLerp(e.vy, 0, 0.05);
1266	        if (e.ai1 === 90) { e.vx *= 0.7; e.vy *= 0.7; }
1267	      } else {
1268	        e.vx *= 0.92; e.vy *= 0.92;
1269	      }
1270	      e.ai1 += 1;
1271	      if (e.ai1 >= 90 + (20 - num17)) { e.ai0 = 1; e.ai1 = 0; }
1272	      break;
1273	    }
1274	    // ---- 10 半血变身(:47106-47135):90t 时传送玩家上 250 处并 ai3 0→1(进入二阶段) ----
1275	    case 10: {
1276	      if (e.ai1 >= 30 && e.ai1 <= 170) e.iframes = 2; // flag6 → dontTakeDamage(:47110)
1277	      if (e.ai1 === 0) game.playSfxFiles?.(['Item_161'], 1, e.cx, e.cy); // :47036 状态开始音（仅此一次）
1278	      e.vx *= 0.95; e.vy *= 0.95;
1279	      if (e.ai1 === 90) {
1280	        if (e.ai3 === 0) e.ai3 = 1; // :47040-47043
1281	        if (e.ai3 === 2) e.ai3 = 3; // :47044-47047 白天暴怒档同步进二阶段(3=暴怒+二阶段)
1282	        e.x = player.cx - e.w / 2;
1283	        e.y = player.cy - 250 - e.h / 2;
1284	        // 原版此传送为纯 position 改写（:47039-47052）：无 dust 无传送音——
1285	        // 曾错加 roar+黄尘（已移除对齐）
1286	      }
1287	      e.ai1 += 1;
1288	      if (e.ai1 >= 180 + (20 - num17)) { e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; }
1289	      break;
1290	    }
1291	    // ---- 12 螺旋射线 873(:47152-47200,二阶段表尾拍,经典可达——num57→12 无专家门,
1292	    //      11 才是 expert 专属):起手 (0,-12) 上冲 + 0.95 阻尼;[10,60) 窗口内每 num22t
1293	    //      一发 873（速向 = (0,-20) 旋 2π·进度,弹 ai[1]=num23 螺旋相位） ----
1294	    case 12: {
1295	      if (e.ai1 === 0) {
1296	        game.playSfxWav?.('Item_165', 1, e.cx, e.cy);   // :47158
1297	        e.vx = 0; e.vy = -12;                            // :47159
1298	      }
1299	      e.vx *= 0.95; e.vy *= 0.95;                        // :47161
1300	      const dur = 60 + (90 - num17);                     // num21 = 90 - num17
1301	      const num22 = flag2 ? 4 : 6;                       // :47167-47171 flag2 射速加密
1302	      const flag11 = e.ai1 < 60 && e.ai1 >= 10;          // :47162
1303	      const num23 = (e.ai1 - 10) / 50;                   // 螺旋相位
1304	      if (Math.floor(e.ai1) % num22 === 0 && flag11) {
1305	        const [svx, svy] = rot(0, -20, Math.PI * 2 * num23);   // :47176
1306	        shoot(game, e.cx - 55, e.cy - 30, svx, svy,
1307	          dayEnrage ? 9999 : phase2 ? 50 : 45, 873);     // num8（:47179）
1308	      }
1309	      e.ai1 += 1;
1310	      if (e.ai1 >= dur) { e.ai0 = 1; e.ai1 = 0; }
1311	      break;
1312	    }
1313	    // ---- 13 淡出退场(:47202-47276):alpha ±5 双向——flag7（狂暴末班/目标失效/超距）
1314	    //      为真 +5 渐隐,回假 -5 复显;ai1≥20 且到达端点才结算:全隐 → 移除,
1315	    //      全显 → 回 1 态续战（可回归,曾单向只出不回） ----
1316	    case 13: {
1317	      if (e.ai1 === 0) {
1318	        game.playSfxWav?.('Item_165', 1, e.cx, e.cy);   // :47207
1319	        e.vx = 0; e.vy = -7;                            // :47208
1320	      }
1321	      e.vx *= 0.95; e.vy *= 0.95;                        // :47210
1322	      // flag7（:47216-47235）：真狂暴末班（入夜或白天 time≥53400）或目标失效/超 6400
1323	      const flag7 = enragedLeave
1324	        || !player || player.dead || Math.hypot(player.cx - e.cx, player.cy - e.cy) > 6400;
1325	      e.spawnAlpha = clamp(e.spawnAlpha + (flag7 ? 5 : -5), 0, 254);
1326	      e.ai1 += 1;
1327	      if (e.ai1 >= 20 && (e.spawnAlpha <= 0 || e.spawnAlpha >= 254)) {
1328	        // :47264-47271 全隐 → active=false(静默,非击杀——bossFled 同置,终审修)
1329	        if (e.spawnAlpha >= 254) { e.bossFled = true; e.dead = true; return; }
1330	        e.ai0 = 1; e.ai1 = 0;                            // :47273-47275 全显 → 回战斗
1331	      }
1332	      break;
1333	    }
1334	    default:
1335	      e.ai0 = 1; e.ai1 = 0;
1336	      break;
1337	  }
1338	  // :47292 alpha 渐隐回落(0/13 态各自管控 spawnAlpha,不参与)
1339	  if (e.ai0 !== 0 && e.ai0 !== 13) e.spawnAlpha = Math.max(0, e.spawnAlpha - 5);
1340	  flyIntegrate(e);
1341	
1342	  // 点光(:47298-47302 AI_120 尾段)：白光 × Opacity（=1−alpha/255；本仓
1343	  // spawnAlpha 254=全隐 → 0=全显，故 Opacity≈1−spawnAlpha/254）
1344	  const o = 1 - e.spawnAlpha / 254;
1345	  e.lightRGB = [o, o, o];
1346	}
1347	
1348	// ===================== AI_121 史莱姆皇后 657(NPC.cs:45543-46177) =====================
1349	// 状态机(ai0): 0 待机(一阶段地面/二阶段 FlyMovement) / 1 传送后显形 / 2 传送消散 /
1350	//   3 走路连跳(-8,-8,-6,-13 四连) / 4 升空砸地(ai2=0 升空 60t → ai2=1 重力坠,落地撒 922) /
1351	//   5 凝胶环(ai2=0 蓄 50t → ai2=1 撒 926 环)。
1352	// 半血(flag2)进二阶段:悬浮 FlyMovement + 攻速变化 + 暴怒(离开神圣之地)分支按任务跳过。
1353	// 经典数值(:45546-45552): 砸地 922 40 伤 / 凝胶环 926 30 伤;砸地蓄力 30t(二阶段 10t);
1354	//   凝胶环 6 发(二阶段 10 发);仆从按掉血 2%(二阶段 1.5%)撒 1-2 只 NPC 658/659/660。
1355	const QUEEN_MINION_VANILLA = [658, 659, 660]; // vanilla :46134-46146 蓝/粉/紫仆从
1356	// 数据核对(1.4.5.6):658/659/660 已在 public/sprites/vanilla-npcs.json,与 SetDefaults
1357	//   :17261-17284 逐字段一致(658/659 QueenSlimeMinion 24×18 aiStyle1 伤40 防35 血150;
1358	//   660 QueenSlimeMinionPurple 40×30 aiStyle14 伤50 防30 血120),贴图 NPC_658/659/660.png
1359	//   亦在 sprites/vanilla —— 真身直连,aiStyle 1/14 均已接线。
1360	// FALLBACK 仅作数据文件缺失时的防御(535 刺史莱姆/537 沙史莱姆/16 蓝史莱姆)。
1361	const QUEEN_MINION_FALLBACK = [535, 537, 16];
1362	
1363	/** TileID.Sets.Platforms（:43378 第二析取项）——平台四件套 sheet id（本仓 isPlatform
1364	 *  还含可站家具（工作台/铁砧等不在 Sets.Platforms）,故按 sheet 精确过滤） */
1365	const PLATFORM_SHEETS = new Set([19, 239, 380, 427]);
1366	function isPlatformSheetTile(game: GameHooks, x: number, y: number): boolean {
1367	  const st = game.world.store;
1368	  const d = TILE_DEFS[st.type[st.idx(x, y)]];
1369	  return !!d?.platform && PLATFORM_SHEETS.has(d.vanilla?.sheet ?? -1);
1370	}
1371	
1372	/** AddKingSlimeTeleportCacheTiles（NPC.cs:43371-43389）逐格验证：
1373	 *  nactive 且（tileSolid && !tileSolidTop 或 Sets.Platforms）且上一格非实心
1374	 *  （1 格净空,非 7 格）,落位 (x*16+8, y*16−height/2) 无岩浆且到玩家 CanHitLine。 */
1375	function kingSlimeCacheTileOk(
1376	  game: GameHooks, player: Player, e: Enemy, x: number, y: number,
1377	): boolean {
1378	  const st = game.world.store;
1379	  if (!st.inBounds(x, y) || !st.isActive(x, y)) return false;
1380	  const ground = (st.isSolid(x, y) && !st.isPlatform(x, y)) || isPlatformSheetTile(game, x, y);
1381	  if (!ground) return false;
1382	  if (!st.inBounds(x, y - 1) || st.isSolid(x, y - 1)) return false;   // 1 格净空（:43378）
1383	  const li = st.idx(x, y);
1384	  if (st.liquid[li] > 0 && st.liquidType[li] === 2) return false;     // tile.lava()
1385	  const landX = x * TILE + 8, landY = y * TILE - e.h / 2;             // :43380 落位中心
1386	  return losClear(game, landX, landY, player.cx, player.cy);          // :43381
1387	}
1388	
1389	/** BuildKingSlimeTeleportCache（:43392-43400）：外环四条带扫描（外距 outer,
1390	 *  内距 inner 的环带）。返回全部合格格。 */
1391	function buildKingSlimeCache(
1392	  game: GameHooks, player: Player, e: Enemy, tx: number, ty: number, outer: number, inner: number,
1393	): Array<[number, number]> {
1394	  const out: Array<[number, number]> = [];
1395	  const bands: Array<[number, number, number, number]> = [
1396	    [tx - outer, tx - inner, ty - outer, ty + outer],
1397	    [tx + inner, tx + outer, ty - outer, ty + outer],
1398	    [tx - inner, tx + inner, ty - outer, ty - inner],
1399	    [tx - inner, tx + inner, ty + inner, ty + outer],
1400	  ];
1401	  for (const [x0, x1, y0, y1] of bands) {
1402	    for (let x = x0; x <= x1; x++) {
1403	      for (let y = y0; y <= y1; y++) {
1404	        if (kingSlimeCacheTileOk(game, player, e, x, y)) out.push([x, y]);
1405	      }
1406	    }
1407	  }
1408	  return out;
1409	}
1410	
1411	/** AI_015_KingSlime_FindTeleportSpot（NPC.cs:43402-43434）1:1：
1412	 *  anti → 玩家脚下（返回 false——调用方仍进传送态但蓄能清零,落点已写入）;
1413	 *  环带 (10,7) 找随机格 → (x*16+8, y*16) Bottom 锚;
1414	 *  空则缩环 (6,2) 重试;再空 → 最近玩家脚下兜底（返回 false）。 */
1415	function queenTeleportSpot(game: GameHooks, player: Player, e: Enemy, anti: boolean): { x: number; y: number; found: boolean } {
1416	  if (anti) return { x: player.x + player.w / 2, y: player.y + player.h, found: false }; // :43404-43409
1417	  const ptx = Math.floor(player.cx / TILE), pty = Math.floor(player.cy / TILE);
1418	  for (const [outer, inner] of [[10, 7], [6, 2]] as const) {   // :43412/:43421 双档环带
1419	    const cands = buildKingSlimeCache(game, player, e, ptx, pty, outer, inner);
1420	    if (cands.length > 0) {
1421	      const [x, y] = cands[Math.floor(Math.random() * cands.length)];
1422	      return { x: x * TILE + TILE / 2, y: y * TILE, found: true };   // :43417-43418
1423	    }
1424	  }
1425	  return { x: player.x + player.w / 2, y: player.y + player.h, found: false }; // :43430-43433
1426	}
1427	
1428	/** AI_121_QueenSlime_FlyMovement(:45467-45542):12 速/0.085 加速度趋近玩家上方 250,
1429	 *  反向且 >100px 时加速度 ×2;旋转 = vx*0.1 钳 ±0.5 */
1430	function queenFlyMovement(e: Enemy, game: GameHooks, player: Player): void {
1431	  e.onGround = false;
1432	  const spd = 12, accBase = 0.085, hover = 250;
1433	  let tx = player.cx, ty = player.cy - hover;
1434	  if (losClear(game, e.cx, e.cy, player.cx, player.cy)) {
1435	    tx = player.cx; ty = player.cy - hover;
1436	  } else {
1437	    // :45478-45496 无视线 → 逐级上探玩家上方第一个实心格下方(简化:玩家上方 16px 一档,探 16 档)
1438	    const st = game.world.store;
1439	    let found = false;
1440	    for (let i = 0; i < 16; i++) {
1441	      const py = player.cy - 16 * i;
1442	      const ptx = Math.floor(player.cx / TILE), pty = Math.floor(py / TILE);
1443	      if (st.inBounds(ptx, pty) && st.isSolid(ptx, pty)) {
1444	        tx = player.cx; ty = py + 16;
1445	        found = true;
1446	        break;
1447	      }
1448	    }
1449	    if (!found) { tx = player.cx; ty = player.cy; }
1450	  }
1451	  let dvx = tx - e.cx, dvy = ty - e.cy;
1452	  const dist = Math.hypot(dvx, dvy);
1453	  let acc = accBase;
1454	  if (Math.abs(dvx) < 40) dvx = e.vx;                       // :45512-45514
1455	  const lim = spd - 2;
1456	  if (dist > 100 && ((e.vx < -lim && dvx > 0) || (e.vx > lim && dvx < 0))) acc *= 2; // :45516-45519
1457	  if (dist < 40) { dvx = e.vx; dvy = e.vy; }                // :45521-45522
1458	  else if (dist < 80) { dvx = (dvx / (dist || 1)) * spd * 0.65; dvy = (dvy / (dist || 1)) * spd * 0.65; }
1459	  else { dvx = (dvx / (dist || 1)) * spd; dvy = (dvy / (dist || 1)) * spd; }
1460	  simpleFly(e, dvx, dvy, acc);
1461	  e.spin = clamp(e.vx * 0.1, -0.5, 0.5); // :45536-45541
1462	}
1463	
1464	export function queenSlimeAI(e: Enemy, game: GameHooks, player: Player | null): void {
1465	  const la = laOf(e);
1466	  if (!e.bInit) {
1467	    // :45559-45566 localAI[0]==0:ai[1]=-100,localAI[0]=lifeMax
1468	    e.bInit = true;
1469	    e.ai0 = 0; e.ai1 = -100; e.ai2 = 0; e.ai3 = 0;
1470	    la.la0 = e.maxHp;
1471	  }
1472	  const phase2 = e.hp <= e.maxHp / 2; // flag2 :45552
1473	  // 点光(:45557-45558 AI_121 头段,恒亮无门)：Center (1,0.7,0.9) 粉光
1474	  e.lightRGB = [1, 0.7, 0.9];
1475	  // 掉血阈值撒仆从(:46147-46177):localAI[0] 记上次标记血量,差值超 2%(二阶段 1.5%)即撒
1476	  if (la.la0 >= e.maxHp / 2 && e.hp < e.maxHp / 2) {
1477	    la.la0 = e.hp;            // :46142-46148 进二阶段复位状态
1478	    e.ai0 = 0; e.ai1 = 0; e.ai2 = 0;
1479	  }
1480	  const b = baseOf(e);
1481	  e.def.damage = b.dmg;
1482	  e.def.defense = b.def;
1483	  // 玩家死/超 500 格 → 鼓励离场(EncourageDespawn:45576;简化为远距上浮,不清除)
1484	  if (!player || player.dead || Math.abs(e.cx - player.cx) / 16 > 500) {
1485	    e.encourageDespawn(10); // :45574 二次判定后仍失败 → EncourageDespawn(10)
1486	    if (player) e.facing = player.cx < e.cx ? 1 : -1; // 背对玩家（:45576-45582）
1487	    e.vy -= 0.06;
1488	    e.y += e.vy; e.x += e.vx;
1489	    e.spin = clamp(e.vx * 0.1, -0.5, 0.5);
1490	    return;
1491	  }
1492	  const dirToPlayer = player.cx >= e.cx ? 1 : -1;
1493	  e.facing = dirToPlayer;
1494	
1495	  // 传送蓄能(ai3,一阶段专属 :45576-45618):无视线或高差 >320 时 +1.5/t,否则 -1/t;
1496	  // 满 300 且落地待机 → **无条件**先置 ai0=2（:45578——搜索失败也照传送,
1497	  // 落点兜底=最近玩家脚下）;FindTeleportSpot 失败仅清 ai3 重攒（:45596-45599）。
1498	  // 反挂机(蓄满 360 或距玩家 >2000)→ anti 直落玩家脚下(:45587-45595)。
1499	  if (!phase2) {
1500	    const blocked = !losClear(game, e.cx, e.cy, player.cx, player.cy) || Math.abs(e.y - (player.y + player.h)) > 320;
1501	    if (blocked) e.ai3 += 1.5;
1502	    else e.ai3 = Math.max(0, e.ai3 - 1);
1503	    if (e.ai3 >= 300 && e.ai0 === 0 && e.vy === 0) {
1504	      e.ai0 = 2; e.ai1 = 0;                            // :45578 先进传送态（无门）
1505	      const anti = e.ai3 >= 360 || Math.hypot(player.cx - e.cx, player.cy - e.cy) > 2000; // :45588
1506	      if (e.ai3 >= 360) e.ai3 = 360;                   // :45590-45593
1507	      const spot = queenTeleportSpot(game, player, e, anti);
1508	      la.la1 = spot.x; la.la2 = spot.y;
1509	      if (!spot.found) e.ai3 = 0;                      // :45596-45599 失败 → 蓄能清零（传送照走）
1510	    }
1511	  }
1512	
1513	  // noGravity/noTileCollide 置位(:45634-45635 默认关;case 4/5 与二阶段飞行开启)——
1514	  // 原版 case 4 整段(含 ai2=0 升空)置 noGravity,故一阶段升空同样免重力
1515	  const flying = e.ai0 === 5 || (e.ai0 === 4 && e.ai2 === 0) || (phase2 && e.ai0 === 0);
1516	  if (!flying) {
1517	    // 通用重力(NPC.cs:91519-91524,!noGravity 时 +0.3 钳 maxFallSpeed 10;
1518	    // 俯冲段(:45945)自身 +1 钳 14 与此叠加,实际仍受 10 上限——与原版一致)
1519	    if (!e.onGround) e.vy += 0.3;
1520	    if (e.vy > 10) e.vy = 10;
1521	  } else {
1522	    e.onGround = false;
1523	  }
1524	
1525	  switch (e.ai0) {
1526	    // ---- 0 待机(:45628-45686):地面摩擦 / 二阶段飞行;ai1 过阈值(60/120)选下一招 ----
1527	    case 0: {
1528	      if (phase2) {
1529	        queenFlyMovement(e, game, player);
1530	      } else if (e.onGround) {
1531	        e.vx *= 0.8;
1532	        if (Math.abs(e.vx) < 0.1) e.vx = 0;
1533	        e.spin = 0;
1534	      }
1535	      // :45673 一阶段空中(!flag2 && velocity.Y!=0)不计数,落地后才推进选拍
1536	      if (!phase2 && !e.onGround && e.vy !== 0) break;
1537	      e.ai1 += 1;
1538	      const idle = phase2 ? 120 : 60; // num10 :45648-45652
1539	      if (e.ai1 > idle) {
1540	        e.ai1 = 0;
1541	        if (phase2) {
1542	          // :45660-45678 二阶段:默认砸地(ai2=1),玩家在上方或横距 >250 改凝胶环
1543	          let next = Math.random() < 0.5 ? 4 : 5;
1544	          let sub = next === 4 ? 1 : 0;
1545	          if (next === 4 && (player.y + player.h < e.y + e.h || Math.abs(player.cx - e.cx) > 250)) {
1546	            next = 5; sub = 0;
1547	          }
1548	          e.ai0 = next; e.ai2 = sub;
1549	        } else {
1550	          // :45680-45686 一阶段:随机 跳(3)/砸地(4)/凝胶环(5)
1551	          const r = Math.floor(Math.random() * 3);
1552	          e.ai0 = r === 0 ? 3 : r === 1 ? 4 : 5;
1553	          e.ai2 = 0;
1554	        }
1555	      }
1556	      break;
1557	    }
1558	    // ---- 1 传送后显形(:45689-45720):30t;缩放动画(num3)为纯视觉,跳过 ----
1559	    case 1: {
1560	      e.spin = 0;
1561	      // 到达每帧 10 尘 4（:45747-45754）：GetDustColor=粉蓝 lerp（近似两色抽样）
1562	      game.spawnParticles(e.cx, e.cy, Math.random() < 0.5 ? '#50A0FF' : '#E060E0', 10, 2.4, { life: 30 });
1563	      e.ai1 += 1;
1564	      if (e.ai1 >= 30) { e.ai0 = 0; e.ai1 = 0; }
1565	      break;
1566	    }
1567	    // ---- 2 传送消散(:45721-45758):60t 后落位到 la1/la2(底部对齐) ----
1568	    case 2: {
1569	      e.spin = 0;
1570	      // 离场每帧 10 尘 4 ×0.5（:45780-45787）
1571	      game.spawnParticles(e.cx, e.cy, Math.random() < 0.5 ? '#50A0FF' : '#E060E0', 10, 1.2, { life: 30 });
1572	      e.ai1 += 1;
1573	      if (e.ai1 >= 60 && la.la1 !== 0) {
1574	        e.iframes = 2; // dontTakeDamage = hide(:46138)
1575	        e.x = la.la1 - e.w / 2;
1576	        e.y = (la.la2 as number) - e.h;
1577	        e.vx = 0; e.vy = 0;
1578	        e.ai0 = 1; e.ai1 = 0;
1579	        game.spawnParticles(e.cx, e.cy, '#7040A0', 16, 2.4);
1580	      } else if (e.ai1 > 90) {
1581	        e.ai0 = 1; e.ai1 = 0; // 找不到落点的兜底
1582	      }
1583	      break;
1584	    }
1585	    // ---- 3 走路连跳(:45759-45844):四连跳 vy=-8/-8/-6/-13,横速递增 4/4.5/4/3.5;
1586	    //      落地重跳倒计时 ai1(血量 <66%/<33% 各 +4/t 加速) ----
1587	    case 3: {
1588	      e.spin = 0;
1589	      if (e.onGround) {
1590	        e.vx *= 0.8;
1591	        if (Math.abs(e.vx) < 0.1) e.vx = 0;
1592	        e.ai1 += 4;
1593	        if (e.hp < e.maxHp * 0.66) e.ai1 += 4;
1594	        if (e.hp < e.maxHp * 0.33) e.ai1 += 4;
1595	        if (e.ai1 >= 0) {
1596	          if (e.ai2 === 3) {
1597	            e.vy = -13; e.vx += 3.5 * dirToPlayer;
1598	            e.ai1 = 0; e.ai2 = 0;
1599	            e.ai0 = 0; // 大跳结束回待机
1600	            game.spawnParticles(e.cx, e.y + e.h, '#8060C0', 10, 2.2);
1601	          } else if (e.ai2 === 2) {
1602	            e.vy = -6; e.vx += 4.5 * dirToPlayer;
1603	            e.ai1 = -40; e.ai2 += 1;
1604	          } else {
1605	            e.vy = -8; e.vx += 4 * dirToPlayer;
1606	            e.ai1 = -40; e.ai2 += 1;
1607	          }
1608	          e.onGround = false;
1609	        }
1610	      } else {
1611	        // 空中横移(:45819-45844):朝玩家 0.2/t,上限 3(FTW 7,:45853-45857;
1612	        // 反向时 0.93 阻尼)
1613	        const cap = game.world.seedFlags?.getGoodWorld ? 7 : 3;
1614	        if ((dirToPlayer === 1 && e.vx < cap) || (dirToPlayer === -1 && e.vx > -cap)) {
1615	          if ((dirToPlayer === -1 && e.vx < 0.1) || (dirToPlayer === 1 && e.vx > -0.1)) {
1616	            e.vx += 0.2 * dirToPlayer;
1617	          } else {
1618	            e.vx *= 0.93;
1619	          }
1620	        }
1621	      }
1622	      break;
1623	    }
1624	    // ---- 4 升空砸地(:45845-46006):ai2=0 飞向玩家上 384(60t) → ai2=1 重力坠(蓄力 30/10t,
1625	    //      FTW 0=无蓄力直接坠,:45885-45889;vy+1/t 钳 14,FTW 双倍加速钳 15.99,
1626	    //      :45944-45953);落地撒 922 冲击波(40 伤)+ 尘暴,回待机 ----
1627	    case 4: {
1628	      e.spin *= 0.9;
1629	      if (e.ai2 === 1) {
1630	        const num13 = game.world.seedFlags?.getGoodWorld ? 0 : phase2 ? 10 : 30; // :45856-45860
1631	        e.vx *= 0.8;
1632	        if (!e.onGround) {
1633	          // (首帧越过 num13 的原版蓄冲吼经对账证伪删除——:45856-45960 零 PlaySound)
1634	          e.ai1 += 1;
1635	          if (e.ai1 >= num13) {
1636	            e.vy += 1;
1637	            // FTW(:45947-45952):额外 +1/t、钳 15.99
1638	            if (game.world.seedFlags?.getGoodWorld) {
1639	              e.vy += 1;
1640	              if (e.vy === 0) e.vy = 0.01;
1641	              if (e.vy >= 15.99) e.vy = 15.99;
1642	            } else {
1643	              if (e.vy === 0) e.vy = 0.01;
1644	              if (e.vy >= 14) e.vy = 14; // num17 = 14(经典)
1645	            }
1646	          } else {
1647	            e.vy *= 0.8;
1648	          }
1649	          if (phase2 && e.ai1 > num13 + 120) { // 二阶段超时兜底(:45931-45938)
1650	            e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.vy *= 0.8;
1651	          }
1652	        } else {
1653	          // 落地冲击(:45870-45890):922 冲击波 + 尘暴 + 回待机
1654	          shoot(game, e.cx, e.y + e.h, 0, 0, 40, 922, 240);
1655	          game.spawnParticles(e.cx, e.y + e.h, '#B090E0', 20, 3);
1656	          game.playSfxWav?.('Item_167', 1, e.cx, e.cy);   // :45902 落地冲击(曾借 roar 0.7)
1657	          e.ai0 = 0; e.ai1 = 0; e.ai2 = 0;
1658	        }
1659	      } else {
1660	        // ai2=0 升空(:45967-46005):前 30t 原地蓄势(:45972-45974),之后 20 速冲向
1661	        // 玩家上方 384(超 500 格用自身),满 60t 转 ai2=1 俯冲
1662	        e.ai1 += 1;
1663	        if (e.ai1 >= 30) {
1664	          let tx = e.cx, ty = e.cy - 384;
1665	          if (Math.abs(e.cx - player.cx) / 16 <= 500) { tx = player.cx; ty = player.cy - 384; }
1666	          const dx = tx - e.cx, dy = ty - e.cy;
1667	          const d = Math.hypot(dx, dy);
1668	          if (Math.abs(e.vy) < 0.5) { // 原版判 velocity.Y == 0;浮点残留放宽半格
1669	            const l = d || 1;
1670	            e.vx = (dx / l) * 20; e.vy = (dy / l) * 20;
1671	          } else {
1672	            e.vy *= 0.95;
1673	          }
1674	          if (e.ai1 >= 60) {
1675	            e.ai1 = 0; e.ai2 = 1;
1676	            e.vy = -3; // :45982-45985（仅 vy=-3,无 vx 衰减——曾多乘 ×0.5）
1677	          }
1678	        }
1679	      }
1680	      break;
1681	    }
1682	    // ---- 5 凝胶环(:46007-46121):ai2=0 蓄 50t(二阶段兼飞)→ ai2=1 第 10t 撒 926 环
1683	    //      (num6=10(FTW 15,:46026-46029)分度,num7 = 二阶段 num6 / 一阶段 6 发,
1684	    //      30 伤,9 速,-i*2π/num6) ----
1685	    case 5: {
1686	      e.spin *= 0.9;
1687	      if (e.ai2 === 1) {
1688	        e.ai1 += 1;
1689	        if (e.ai1 >= 10) {
1690	          const num6 = game.world.seedFlags?.getGoodWorld ? 15 : 10;
1691	          const count = phase2 ? num6 : 6;
1692	          for (let i = 0; i < count; i++) {
1693	            const a = (-i * Math.PI * 2) / num6;
1694	            shoot(game, e.cx, e.cy, Math.cos(a) * 9, Math.sin(a) * 9, 30, 926);
1695	            game.playSfxWav?.('Item_155', 1, e.cx, e.cy);   // 弹 926 首帧音(pcs:52218)
1696	          }
1697	          // 原版凝胶环发射零吼(:46105 的 65 号声是 QueenSlime 1/360 环境声,
1698	          // 与发射时机无关)——曾借 roar 0.5,2026-08-18 对账删
1699	          e.ai0 = 0; e.ai1 = 0; e.ai2 = 0;
1700	        }
1701	      } else {
1702	        e.ai1 += 1;
1703	        if (e.ai1 >= 50) { e.ai1 = 0; e.ai2 = 1; }
1704	        if (phase2) queenFlyMovement(e, game, player);
1705	      }
1706	      break;
1707	    }
1708	    default:
1709	      e.ai0 = 0; e.ai1 = 0; e.ai2 = 0;
1710	      break;
1711	  }
1712	
1713	  // 积分 + 碰撞(飞行态无碰撞)
1714	  e.x += e.vx;
1715	  e.y += e.vy;
1716	  if (!flying) collideGround(e, game);
1717	
1718	  if (e.hp <= 0) return;
1719	
1720	  // 掉血撒仆从(:46147-46177):差值超阈值 → 1-2 只,本体附近随机落点,ai0=-500*rand3
1721	  const threshold = Math.floor(e.maxHp * (phase2 ? 0.015 : 0.02));
1722	  if (e.hp + threshold < la.la0) {
1723	    la.la0 = e.hp;
1724	    const n = 1 + Math.floor(Math.random() * 2); // Next(1,3)
1725	    for (let k = 0; k < n; k++) {
1726	      const pick = Math.floor(Math.random() * 3);
1727	      let minion = spawnPart(game, e, QUEEN_MINION_VANILLA[pick]);
1728	      if (!minion) minion = spawnPart(game, e, QUEEN_MINION_FALLBACK[pick]); // 数据缺 658-660
1729	      if (minion) {
1730	        minion.x = e.x + Math.random() * Math.max(1, e.w - 32);
1731	        minion.y = e.y + Math.random() * Math.max(1, e.h - 32);
1732	        minion.vx = (Math.floor(Math.random() * 31) - 15) * 0.1;
1733	        minion.vy = (-Math.floor(Math.random() * 31)) * 0.1;
1734	        minion.ai0 = -500 * Math.floor(Math.random() * 3);
1735	        minion.ai1 = 0;
1736	      }
1737	    }
1738	  }
1739	}
1740	
1741	// ===================== 接线清单(Enemy.ts aiStyle case 表已接线) =====================
1742	//   case 84:  lunaticCultistAI(this, game, p); break;   // 439 真身 + 440 克隆体共用(见文件头)
1743	//   case 120: empressOfLightAI(this, game, p); break;   // 636 光之女皇(原版 AI_120 无 rotation,仅 facing)
1744	//   case 121: queenSlimeAI(this, game, p); break;       // 657 史莱姆皇后(俯仰用 spin)
1745	// 召唤 key: spawnPart(game, src, id)——史后仆从 658/659/660(数据/贴图齐,直连真身;
1746	//   FALLBACK 仅防御);邪教徒仪式态生成 440 克隆体、ai0=7 态召 522 远古之光、ai0=8 态撒 523。
1747	// 弹幕 key: shoot(game, x, y, vx, vy, dmg, projId)——464 冰雾/465 闪电球/467 火球/468 光珠;
1748	//   872 永恒彩虹/873 虹迹/874 极光/919 光枪/923 日舞/922 砸地冲击/926 凝胶弹。
1749	// 贴图:Projectile_464/465/467/468/872/873/874/919/922/923/926.png 均已在
1750	//   public/sprites/vanilla/(Arrow 按 projId 懒加载自动生效)。
1751	
1752	// ============================================================================
1753	// AI_100 远古之光 522(NPC.cs:42064-42142):轨道投射物型 NPC(邪教徒 ai0=7 直召)。
1754	// 初速 ai[2]/ai[3];ai[0]>60 后按 ai[1] 逐 t 弯转(小随机角 → 环绕/收敛弧线)、
1755	// >120 阻尼 0.98;触地(ai0>=0 时)→ 停驻 5t 自灭。(尘 261 系为纯视觉,略)
1756	// ============================================================================
1757	export function ancientLightAI(e: Enemy, game: GameHooks, player: Player | null) {
1758	  // bInit 原只复位 vx/vy——ai0 泄漏 -1120 时 `ai0>=0` 三门全假 = 计时不启动、
1759	  // 落地不停 → 永不弯转/自灭的直飞弹(F6 可直接造出,2026-08-13 ai0 清查)
1760	  if (!e.bInit) { e.bInit = true; if (e.ai0 < 0) e.ai0 = 0; e.vx = e.ai2; e.vy = e.ai3; }
1761	  if (e.vy === 0 && e.ai0 >= 0) { e.ai0 = -1; e.ai1 = 0; return; }
1762	  if (e.ai0 === -1) {
1763	    e.vx = 0; e.vy = 0;
1764	    e.ai1 += 1;
1765	    if (e.ai1 >= 5) e.dead = true;
1766	    return;
1767	  }
1768	  e.spin = Math.atan2(e.vy, e.vx) - Math.PI / 2;
1769	  if (e.ai0 >= 0) {
1770	    e.ai0 += 1;
1771	    if (e.ai0 > 60) {
1772	      const c = Math.cos(e.ai1), s = Math.sin(e.ai1);
1773	      const nvx = e.vx * c - e.vy * s, nvy = e.vx * s + e.vy * c;
1774	      e.vx = nvx; e.vy = nvy;
1775	    }
1776	    if (e.ai0 > 120) { e.vx *= 0.98; e.vy *= 0.98; }
1777	    if (Math.hypot(e.vx, e.vy) < 0.2) { e.vx = 0; e.vy = 0; }
1778	  }
1779	  e.x += e.vx;
1780	  e.y += e.vy;
1781	  void game; void player;
1782	}
1783	
1784	// ============================================================================
1785	// AI_101 远古末日 523(NPC.cs:42143-42221):锚定邪教徒(ai0=头 id)蓄能 420t 显形,
1786	// 蓄满朝四方喷 593 弹(damage)后消散;头失效/蓄满 → 自灭。
1787	// (经典模式邪教徒不可达,专家专属;专家档未开时仅作数据完整性)
1788	// ============================================================================
1789	export function ancientDoomAI(e: Enemy, game: GameHooks, player: Player | null) {
1790	  const CHARGE_MAX = 420;
1791	  const boss = (game.enemies() as Enemy[]).find((n) => !n.dead && n.id === e.ai0 && n.vanillaId === 439);
1792	  // flag108 累加前快照（:42151）：只看锚失效（boss 亡/不在）——满 420 在累加后
1793	  // 自置（:42206-42216），曾把 `>= 420` 提前并入快照 → 蓄满当拍不死、下一拍
1794	  // 双份 593 齐射
1795	  let gone = !boss || e.ai1 < 0;
1796	  let rate = 1;
1797	  if (boss && boss.hp < boss.maxHp / 2) rate = 2;
1798	  if (boss && boss.hp < boss.maxHp / 4) rate = 3;
1799	  e.ai1 += rate;
1800	  const prog = Math.max(0, Math.min(1, e.ai1 / 120)); // :42168 显形进度(前 120t)
1801	  e.vanillaScale = prog;                 // 原版 scale 0→1 显形
1802	  e.spawnAlpha = Math.round(255 - prog * 255); // 原版 alpha 255→0
1803	  if (e.ai1 >= CHARGE_MAX) {
1804	    gone = true;                          // :42208 满能同拍置位 → 齐射一次即灭
1805	    for (let k = 0; k < 4; k++) {
1806	      const ang = -Math.PI / 2 + (Math.PI / 2) * k;
1807	      shoot(game, e.cx, e.cy, Math.cos(ang) * 4, Math.sin(ang) * 4, e.def.damage, 593);
1808	    }
1809	  }
1810	  if (gone) e.dead = true;
1811	  void player;
1812	}
1813	

```


---

## 🤖 Assistant · 2026-08-19T08:54:47.202Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now I understand the current Empress implementation. The task:

1. Table switch on flag2: currently `EMPRESS_CYCLE_P2 = [7, 2, 8, 5, 2, 6, 4, 8, 12]` (9 slots, classic phase2). Add expert phase2 table `[7, 2, 8, 11, 5, 2, 6, 4, 8, 12]` (10 slots, flag2). The task says "表按 flag2 切换(白天/专家时用 expert 表)".

2. case 11: implement the predictive 919 wall per NPC.cs:47061-47151:
   - ai1==0: play Item_162 sound
   - num58 = 20 - num17
   - dur = 100 + num58
   - Magic effects at ±55,-20 during [6,54): visual only (DoMagicEffect - dust; our implementation may skip or approximate; the task says "具体参数照抄" for the wall; DoMagicEffect is dust visual; let me check how our other cases handled DoMagicEffect — they didn't implement it at all. So I can skip it, consistent with existing cases 2/4 etc. which don't have the DoMagicEffect either. Actually looking at case 2 in our code — vanilla case 2 has DoMagicEffect at :46629 and our case 2 doesn't implement it. So consistent to skip. But maybe add a comment.)
   - Hover movement: `if (Distance(vector12 + vector3) > num3)` where vector3 = (0,-350), num3 = 40: SimpleFlyMovement(DirectionTo(vector12 + vector3).normalized * num2(12), num(0.5)) — same as empressHover(e, player, 0, -350). 
   - Every `(int)ai1 % 3 == 0 && ai1 < 100`:
     - v = -targetData.Velocity normalized (fallback -UnitY)
     - num60 = 100; center2 = target center
     - if Distance(center2) > 2400 skip (this is NPC.Distance(center2) = distance from NPC to player > 2400 → continue)
     - num61 = 90; vector13 = center2 + velocity*90 (predicted)
     - vector14 = center2 + v*100 (spawn 100px behind player's motion)
     - if vector14.Distance(center2) < 100: push out (dead code but harmless)
     - v2 = vector13 - vector14
     - NewProjectile(vector14, zero, 919, num6, 0, myPlayer, v2.ToRotation(), ai1/100)
   - The multi-player extra: for l in 0..254: if Boss_CanShootExtraAt(l, num62 % 3, 3, 2400) → same spawn for that player. Single player: skip (num62 = ai1/3; Boss_CanShootExtraAt for main player is presumably false since the main spawn already happened). Let me check Boss_CanShootExtraAt semantics quickly to be sure. Actually in case 12 our implementation skipped it too. Let me keep consistent (single-player only).
   - ai1 += 1; end at >= 100 + num58 → ai0=1, ai1=0.

   Our 919 handling in case 4/case 7: `shoot(game, px, py, (ax/al)*12, (ay/al)*12, dmg, 919, 240)` — the Arrow bucket with 12 speed direct flight and 240 timeLeft presumably. So case 11 will do the same: spawn at vector14 with velocity = normalized(v2)*12, damage num6 (50 classic P1... wait in phase2 60; but case 11 only reachable in phase 2 via expert table. num6: base 50; phase2 → 60; then GetAttackDamage_ForProjectiles(num6, num11): classic returns num6 (60); expert would scale. Our implementation uses `dayEnrage ? 9999 : phase2 ? 60 : 50` — consistent with existing. So for case 11 use same damage expression: `dayEnrage ? 9999 : phase2 ? 60 : 50`.

   Note: vanilla case 11 passes ai1 = this.ai1/100 to the projectile (its delay parameter). Our convergent implementation treats 919 as direct-flight Arrow with speed 12, so there's no delay. The task says: "我们 919 已有收敛实现(直飞 12 速),case11 用同弹型+预测落点排布" — use same projectile type + predicted landing arrangement. So just shoot with the same convergent behavior. Good — no delay.

   Also, `num62 = (int)(ai1 / 3f)` and Boss_CanShootExtraAt(l, num62 % 3, 3, 2400) — for extra players only; skip.

3. Also need the table constant EMPRESS_CYCLE_P2_EXPERT = [7, 2, 8, 11, 5, 2, 6, 4, 8, 12]. And the selection: `const table = phase2 ? (flag2 ? EMPRESS_CYCLE_P2_EXPERT : EMPRESS_CYCLE_P2) : EMPRESS_CYCLE_P1;`

Wait, need to double check the slot assignment. Vanilla phase-2 with flag2:
- num48=0→7, num49=1→2, num50=2→8, num51=3→11, num52=4→5, num53=5→2, num54=6→6, num55=7→4, num56=8→8, num57=9→12.

Without flag2:
- num48=0→7, num49=1→2, num50=2→8, num52=3→5, num53=4→2, num54=5→6, num55=6→4, num56=7→8, num57=8→12.

Our current EMPRESS_CYCLE_P2 = [7,2,8,5,2,6,4,8,12] — matches. Expert table [7,2,8,11,5,2,6,4,8,12] — matches task spec. 

Note case 11 in vanilla requires flag2 to be *selectable* — but the case itself can be entered regardless if ai0=11. In our implementation, case 11 will only be entered via the expert table (day or expert). Fine.

Also "禁止动光女状态机主链" — don't touch the Empress state machine main chain. Adding the table switch in case 1 and a new case 11 block is what's being asked. The instruction "禁止动光女状态机主链/猪鲨 AI 本体" means don't restructure the existing cases; only add the table switch + new case 11.

Wait, but careful about "flag2 把二阶段表切成 10 槽 expert 表" — in our current code, `flag2 = game.world.isExpert || dayEnrage`. The switch should be: phase2 && flag2 → expert table. Note: phase2 in our code = `e.ai3 === 1 || e.ai3 === 3`.

Now for case 11, need to double-check hover: vanilla case 11:
```
NPCAimedTarget targetData6 = GetTargetData();
Vector2 vector12 = (targetData6.Invalid ? base.Center : targetData6.Center);
if (Distance(vector12 + vector3) > num3)   // vector3 = (0, -350), num3 = 40
    SimpleFlyMovement(DirectionTo(vector12 + vector3).SafeNormalize(Vector2.Zero) * num2, num);
```
That's exactly empressHover(e, player, 0, -350). Good.

But wait — in case 11, "if (Distance(center2) > 2400f) continue;" — Distance is NPC.Distance(center2) = distance from NPC center to target center > 2400 → skip spawning. Our case 4 used `Math.hypot(player.cx - e.cx, player.cy - e.cy) <= 2400` gate. Same.

And num6 damage for 919 in case 11.

Also sound at ai1==0: Item_162 (same as case 4/7).

Duration: `if (this.ai[1] >= 100f + num58) { ai0=1; ai1=0; netUpdate }` where num58 = 20 - num17. So dur = 100 + (20 - num17), same formula as case 4. In our code case 4: `const dur = 100 + (20 - num17);`. Same for case 11.

Now the shooting cadence: `(int)this.ai[1] % 3 == 0 && this.ai[1] < 100f` — every 3 ticks, 1 lance each (num59 = 1, loop k < num59). Each spawns ONE 919 at vector14 aimed at v2 direction. Plus for each other qualifying player (Boss_CanShootExtraAt), one more. Single-player: 1 lance per 3 ticks for 100 ticks ≈ 33 lances. They spawn 100px opposite the player's velocity direction, aimed at the position the player will be in 90 ticks.

Now — is there also the localAI "vector3"? In case 11 at :47068 `new Vector2(0f, -100f);` — dead code (unused expression). Ignore.

OK. Now let me also check what num17 is at the time case 11 runs: num17 = 0 + 15(phase2) + 5(flag2) = 20 (since case 11 requires flag2). num58 = 0. dur = 100.

One more check on flag2's effect on case 1 selection: "if (flag2 && num36 != 5 && num36 != 12) { velocity = ...RotatedBy(±90°)*20 }" — already implemented in our case 1.

Now, group 2: Duke Fishron FindFrame (NPC.cs:72824-72910 — actual case 370 at 72824-72917).

The state machine:
- ai0 == 0 (swim): frameCounter += 1; if > 5 (num51=5): frameCounter=0, frame.Y += num; wrap at num*6 → 0. So 6 swim frames (0-5), advancing every 6 ticks (counter > 5 means advance at 6th tick... frameCounter increments each tick; when it exceeds 5 (i.e., reaches 6) reset to 0 and advance. So 6 ticks per frame? frameCounter goes 1,2,3,4,5,6 → >5 at 6 → advance. Yes, every 6 ticks.
  Wait the task says "0-5 游动帧(5t/帧按 |vx| 累计/4t 冲撞中)"? Hmm, the task says "5t/帧按 |vx| 累计/4t 冲撞中" — but the decompiled 1456 code shows fixed num51=5 (ai0==0) or 4 (ai0==5). Hmm wait, let me re-read: `int num51 = 5; if (ai[0] == 5f) num51 = 4;` — ai0==0 → 5 (advance every 6 ticks since >5), ai0==5 → 4 (advance every 5 ticks). Hmm, ">5" means advance when frameCounter becomes 6, i.e., 6 ticks per frame for ai0==0. Wait: frameCounter += 1.0 each FindFrame call (FindFrame is called per tick in vanilla — actually frameCounter increments in FindFrame which runs every update). if frameCounter > num51 → reset & advance. So for num51=5: ticks 1,2,3,4,5 (not >5), tick 6 → >5 → advance. So 6 ticks/frame. For num51=4: 5 ticks/frame.

  Hmm, but the task description says "0-5 游动帧(5t/帧按 |vx| 累计/4t 冲撞中)". That mentions |vx| accumulation which is NOT in the 1456 code I just read. Maybe the task author was describing from memory or from 1405. The instruction says 1456 is authoritative: "1456 版数值/行为一律取最终态". The task says "读现状" and "原版:0-5 游动帧(5t/帧按 |vx| 累计/4t 冲撞中)、冲撞与计时窗(状态 1/6 冲撞/3 龙卷蓄力)出 6/7 张口帧。修法:duke AI 侧写 e.customFrameIdx(694 先例)或 Renderer 加 case 370(读 ai0 态+animT);8 帧。"

  Hmm wait — but actually let me check: is there a `frameCounter += Math.Abs(velocity.X)` variant for case 370 in 1456? Let me search around. The code I read at 72824-72917 is the actual case 370. It says frameCounter += 1.0 fixed. But maybe I should double-check whether there's more to it (the task description mentions |vx| accumulation — maybe that's for a different boss like case 370 in 1405, or the task author misremembered from the walk-cycle family). Since CLAUDE.md says 1456 is the authority and I've read the 1456 code directly, I'll implement exactly what 1456 says: fixed tick counters.

  Actually wait, let me look more carefully. Maybe there are two FindFrame variants: one at :72824 (case 370) which I read. Let me double check there's no additional velocity-based logic in the duke's FindFrame... The read shows the full case 370 block from 72824 to 72917. It's fixed-rate. The description in the task ("5t/帧按 |vx| 累计/4t 冲撞中") might be loose. I'll follow the source exactly with line-number comments. Good — "报异常先查反编译源码" — source is king.

- ai0 == 1 or 6 (dash): frame 6 (mouth closed) if ai2 < 10, else frame 7 (mouth open).
- ai0 == 2 or 7: same as 1/6 (frames 6/7 by ai2<10).
- ai0 == 3, 8, or -1 (tornado charge / bubbles): num52 = 90; if ai2 < 60 || ai2 > 80: swim anim (advance every 6 ticks, wrap 6). else: frame 6; if ai2 > 70 && ai2 < 75 → frame 7.
- ai0 == 4 or 9: num53 = 180; if ai2 < 120 || ai2 > 160: swim anim; else frame 6, and if ai2 > 130 && ai2 < 155 → frame 7.

So the frame states: swim frames 0-5 cycled; open-mouth frames 6/7.

Now, our implementation: "修法:duke AI 侧写 e.customFrameIdx(694 先例)或 Renderer 加 case 370(读 ai0 态+animT)". I need to look at how duke AI works in bossAI_duke_moonlord.ts, what ai0 states it uses (0/1/2/3/4/5 and second-phase 6/7/8/9?), what customFrameIdx is and how Renderer consumes it (694 precedent). Also "animT" — maybe an animation timer on Enemy.

Let me check Enemy for customFrameIdx, animT, and Renderer's handling.

3. WoF death misc[32]: In Game.ts, find the WoF (113) death chain — search for StartHardmode / hardMode transitions. Add: `if (downedMechBoss1 && downedMechBoss2 && downedMechBoss3 && !hardModeBefore) → announce Lang.misc[32]`. Need to check our misc announcement API (boss-summon chain uses Lang.misc — search for "misc[" or Lang.misc usage).

Note vanilla semantics: 
```csharp
bool eventFlag = Main.hardMode;
WorldGen.StartHardmode();
if (downedMechBoss1 && downedMechBoss2 && downedMechBoss3 && !eventFlag)
    ChatHelper.BroadcastChatMessage(NetworkText.FromKey(Lang.misc[32].Key), ChatColors.World);
SetEventFlagCleared(ref eventFlag, 19);
```
Note eventFlag captured BEFORE StartHardmode (so !eventFlag = was not hardmode before this kill — hardmode just started). downedMechBoss1 = The Destroyer (134 sets downedMechBoss1), downedMechBoss2 = The Twins (125? — twins is 125/126, sets downedMechBoss2), downedMechBoss3 = Skeletron Prime (127). Task says "downed_125&&downed_127&&downed_134 全齐且 !hardMode → 公告 misc[32]" — 125 = Twins (Retinazer? actually 125 is Twintail... hmm: 125 = The Twins retinazer? Twins are 125/126, mechanical skull prime is 127... wait 127 sets downedMechBoss3 per :80267-80272 — 127 = Skeletron Prime. 134 sets downedMechBoss1 — 134 = The Destroyer. And downedMechBoss2 set by... 125 (Twins) presumably at another case. Task says downed_125&&downed_127&&downed_134 — matches Twins+Prime+Destroyer.

In our codebase, there are probably flags like `downed_mechBossAny`, `hardMode` etc. in Game.ts. Need to search. Also "查我们 misc 公告 API(boss-summon 链 Lang.misc)" — find how boss-summon announcements use Lang.misc (e.g. misc[37] etc.). Then add misc[32] broadcast. Lang.misc[32] — need the localization key. Let me check Lang.misc array in the decompiled source to get the key for index 32. In vanilla, Lang.misc is defined via MiscMap... misc[32] should be something like "The ancient spirits of light and dark have been released." Hmm, that's usually for WoF normal kill ("The ancient spirits of light and dark have been released"). Actually that's misc[32]? Let me check. In 1.4, after killing WoF: "The ancient spirits of light and dark have been released." is Lang.misc[32]? And when hardmode is triggered while all mechs downed (drunk world / FTW edge where mechs spawn pre-hardmode... actually in drunk worlds you can fight mechs before WoF), the message is the same. Let me verify by grepping Lang.cs for misc and index 32.

4. Martian: bossAI_martian.ts — wrap damage with getAttackDamageForProjectiles. Check bossAI.ts import precedent. Vanilla Remap values: 448: 50→37, 449: 35→30, 450: 30→25, 435: 35→28. Let me verify these in the vanilla source (NPC.cs martian saucer section, NPC 439? Martian Saucer = NPC 439? no that's cultist. Martian Saucer is 439? no. Martian Saucer = NPC 439 is cultist. Martian Saucer is 392? Hmm — Martian Saucer: NPC 439 is Lunatic Cultist. Martian saucer = 439? no. Let me recall: 380 = Martian Saucer? Actually: 380 = Martian Drone? The IDs: 378 Martian Brain? ... I'll just grep.

Projectile IDs: 435 = Martian Turret Blast? 448 = Raygunner? 449 = Raygunner2? 450 = Laser Blaster? Whatever — grep vanilla for these.

Let me grep vanilla NPC.cs for GetAttackDamageForProjectiles to see the Remap pattern and the martian usage sites.

Let me now read the remaining files. Priorities:
1. bossAI_duke_moonlord.ts duke section + how frames handled
2. Enemy.ts customFrameIdx / animT
3. Renderer case 370 handling / customFrameIdx consumption
4. Game.ts WoF death chain
5. bossAI_martian.ts shooting sites
6. bossAI.ts getAttackDamageForProjectiles
7. vanilla martian damage Remap sites
8. Lang.misc[32] key

Let me run a batch of greps.
````

</details>


---

## 🤖 Assistant · 2026-08-19T08:54:47.942Z · glm-x-preview-260804

```
现在我来查看猪鲨 (Duke) 的实现、`customFrameIdx` 的先例，以及火星人的伤害位置。
```


---

## 🤖 Assistant · 2026-08-19T08:54:49.845Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"customFrameIdx\\|animT\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -20; echo ===; grep -rn \"customFrameIdx\" ~/Project/GLM/SandboxWorld/game/src --include=*.ts -l; echo ===; grep -n \"GetAttackDamageForProjectiles\\|getAttackDamageForProjectiles\" ~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts | head",
 "description": "Find customFrameIdx and getAttackDamageForProjectiles usages"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:54:49.944Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
893:  animT = 0;
1095:  customFrameIdx: number | null = null;
1235:      this.animT++;
1252:    this.animT++;
5347:    // 帧机（FindFrame case 694 :77905-77980——AI 侧维护，customFrameIdx 供渲染端直读；
5485:   *  npcFrameT = frameCounter（态切换清零），customFrameIdx 供渲染端直读 */
5488:    let n = this.customFrameIdx ?? 0;
5512:    this.customFrameIdx = n;
6519:      if (this.lai0 === 1) { this.customFrameIdx = 0; this.lai0 = 0; }
6522:        this.customFrameIdx = Math.min(frames - 1, (this.customFrameIdx ?? 0) + 1);
6526:      this.customFrameIdx = ((this.customFrameIdx ?? 0) + 1) % frames;
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-19T08:54:51.806Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"case 370\\|370\" ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts | head -20; echo ===; grep -rn \"vanillaId === 370\\|id === 370\\|=== 370\\|, 370\" ~/Project/GLM/SandboxWorld/game/src --include=*.ts | grep -v Renderer | head -20",
 "description": "Find Duke Fishron (370) rendering and AI references"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:54:51.896Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
378:// ---- 拴绳风筝绘制（Main.DrawKite :36614-37069）工具 ----
547:// 134-136=毁灭者链、261-265=世花族(孢子/本体/钩蔓/触须)、370=猪鲨、396/397=月总头/手、657=史莱姆皇后(飞行倾斜)
548:const ROTATION_NPC = new Set([35, 68, 113, 114, 115, 116, 125, 126, 127, 128, 129, 130, 131, 134, 135, 136, 246, 247, 248, 249, 261, 262, 263, 264, 265, 370, 396, 397, 657]);
3473:    245, 246, 247, 248, 249, 564, 565, 551, 576, 577, 87, 510, 454, 621, 439, 370,
3554:   *  - 风筝：Main.DrawKite :36614-37069 全量（锚绳 FishingLine 分段 + 逐型 Extra 绳尾）
3712:   * Main.DrawKite（Main.cs:36614-37069）全量 1:1：
3817:    // ---- 绳尾（:36947-37067）----
3873:        // :37005-37008 换段长是【持久赋值】（num5 = num10，跨段跨条延续）
3898:      if (rope.lineToo) {                              // :37033-37047 FishingLine 垫层
3914:      for (let n = list.length - 2; n >= 0; n--) {      // :37048-37066 尾段贴图（倒序）
3934:    // ---- 本体（:37068）----
9162:  private static KITE_ITEMS = new Set([4367, 4368, 4369, 4370, 4371, 4379, 4610, 4611,
9318:          // ★绘制角 = itemRotation + 0.785*direction（PlayerDrawLayers.cs:3370——法杖斜持
10973:    4: 0, 13: 2, 344: 3, 370: 4, 246: 5, 249: 5, 345: 6, 50: 7, 396: 8, 395: 9,
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-19T08:54:59.952Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The `===` echo failed (zsh interpreted `===` specially?). Anyway, got the info:
- Enemy.ts has `customFrameIdx: number | null = null` at line 1095, and `animT` at 893.
- Renderer.ts has ROTATION_NPC set including 370 (Duke has rotation-based rendering like worm/twist — the pig shark rotates).
- bossAI.ts grep for getAttackDamageForProjectiles returned nothing visible (first command exited 1 due to the `== not found` error in zsh — the `echo ===` was interpreted... Actually "(eval):1: == not found" — zsh treats `===` as a command? Yes, `echo ===` — zsh expands `=cmd` as "path to command" — `===` triggers "== not found". Need to quote. Let me redo greps with quoted separators.

Let me check bossAI.ts for getAttackDamageForProjectiles.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:55:00.874Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"getAttackDamageForProjectiles\" ~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts ~/Project/GLM/SandboxWorld/game/src/entities/*.ts | head -20",
 "description": "Find getAttackDamageForProjectiles import precedent"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:00.939Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:8:import { mainExpertMode, getAttackDamageForProjectiles } from '../stats/ScaleStats';
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:119:        getAttackDamageForProjectiles(17, 17, e.difficulty), 270, 300, { pierce: 3, skullBone: true });
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:169:    e.def.damage = getAttackDamageForProjectiles(b.dmg, b.dmg * 1.3, e.difficulty);
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:957:        getAttackDamageForProjectiles(25, 22, e.difficulty), 84);
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:1087:            getAttackDamageForProjectiles(25, 22, e.difficulty), 96);
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:1113:            getAttackDamageForProjectiles(20, 19, e.difficulty), 83);
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:1263:          shoot(game, ox, oy, fx, fy, getAttackDamageForProjectiles(30, 27, e.difficulty), 101);
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:1282:          getAttackDamageForProjectiles(25, 23, e.difficulty), 100);
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:1349:        getAttackDamageForProjectiles(18, 17, e.difficulty), 100);
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:1984:        shoot(game, ox + n8 * 5, oy + n9 * 5, n8, n9, getAttackDamageForProjectiles(22, 18, e.difficulty), 100, 300);
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_queenbee_plantera.ts:15:import { getAttackDamageScaledByDifficulty, getAttackDamageForProjectiles } from '../stats/ScaleStats';
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_queenbee_plantera.ts:556:        num806 = getAttackDamageForProjectiles(num806, num806 * 0.9, e.difficulty);
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:8:import { mainExpertMode, getAttackDamageForProjectiles } from '../stats/ScaleStats';
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:119:        getAttackDamageForProjectiles(17, 17, e.difficulty), 270, 300, { pierce: 3, skullBone: true });
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:169:    e.def.damage = getAttackDamageForProjectiles(b.dmg, b.dmg * 1.3, e.difficulty);
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:957:        getAttackDamageForProjectiles(25, 22, e.difficulty), 84);
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:1087:            getAttackDamageForProjectiles(25, 22, e.difficulty), 96);
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:1113:            getAttackDamageForProjectiles(20, 19, e.difficulty), 83);
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:1263:          shoot(game, ox, oy, fx, fy, getAttackDamageForProjectiles(30, 27, e.difficulty), 101);
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:1282:          getAttackDamageForProjectiles(25, 23, e.difficulty), 100);

```


---

## 🤖 Assistant · 2026-08-19T08:55:01.731Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"duke\\|Duke\\|370\" ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts | head -40",
 "description": "Locate Duke section in bossAI_duke_moonlord.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:01.778Z

**📎 ToolResult**

```
1:// Boss AI 1:1 移植(二):猪鲨鱼龙 AI_069(NPC 370)与月亮领主 aiStyle 77/78/79(NPC 398 核心 / 397 手 / 396 头)。
3://   猪鲨 AI_069_DukeFishron        :49143-50127
72:interface DukeX { dir: number; spr: number }
73:const dukeX = new WeakMap<Enemy, DukeX>();
74:const dukeOf = (e: Enemy): DukeX => {
75:  let x = dukeX.get(e);
76:  if (!x) { x = { dir: 1, spr: 1 }; dukeX.set(e, x); }
130:// AI_069 猪鲨鱼龙(NPC 370,NPC.cs:49143-50127)
161:function dukeEnraged(game: GameHooks, player: Player): boolean {
169:function dukePick1(e: Enemy, enraged: boolean): number {
180:function dukePick2(e: Enemy, enraged: boolean): number {
186:  // flag2(expert hp≤15%):next=4 → ai0=9(:49756-49759)——经典模式不可达,代码保留见 dukeState9
191:function dukeCharge(e: Enemy, player: Player, spd: number, toState: number, st: DukeX) {
205:function dukeHover(e: Enemy, player: Player, acc: number, spd: number, sideOff: number, st: DukeX) {
220:export function dukeFishronAI(e: Enemy, game: GameHooks, player: Player | null) {
221:  const st = dukeOf(e);
224:  const enraged = player ? dukeEnraged(game, player) : false;
297:      dukeHover(e, player, hoverAcc, hoverSpd, 300, st);
300:        const next = dukePick1(e, enraged);
301:        if (next === 1) dukeCharge(e, player, chargeSpd, 1, st);
342:    case 3: dukeSharknado(e, game, player, st, false); break;          // :49638-49660
354:      dukeHover(e, player, hoverAcc, hoverSpd, 300, st);
357:        const next = dukePick2(e, enraged);
358:        if (next === 1) dukeCharge(e, player, chargeSpd, 6, st);
409:    case 8: dukeSharknado(e, game, player, st, true); break;           // :49865-49885
424:      dukeHover(e, player, hoverAcc, hoverSpd, 360, st);
429:        if (next === 1) dukeCharge(e, player, chargeSpd, 11, st);
495: *  NewNPC 372/373 鲨鱼(见 DukeSharknadoBolt / DukeSharknadoTornado)。 */
496:function dukeSharknado(e: Enemy, game: GameHooks, player: Player, st: DukeX, big: boolean) {
504:      addProj(game, new DukeSharknadoBolt(e.cx, e.cy, 0, 0, true, dukeEnraged(game, player), e));
510:      addProj(game, new DukeSharknadoBolt(e.cx + ox, e.cy, st.dir * 2, 8, false, false, e));
511:      addProj(game, new DukeSharknadoBolt(e.cx + ox, e.cy, -st.dir * 2, 8, false, false, e));
541:export class DukeSharknadoBolt extends Entity {
551:  /** 鲨鱼生成所需的 Duke 引用(spawnPart 位置供体,实际落点由龙卷覆写) */
612:      addProj(game, new DukeSharknadoTornado(tx * TILE + 8, ground * TILE - 24, true, this.src));
616:      addProj(game, new DukeSharknadoTornado(this.cx - dir * 30, this.cy - 4, false, this.src));
644:export class DukeSharknadoTornado extends Entity {
856:export function dukeBubbleAI(e: Enemy, game: GameHooks, player: Player | null) {
1281:/** :36934-36952(死亡演出 ai1==60)/:37074-37099(玩家全灭离场 ai1==40)清弹段:
1365:  } else if (e.ai0 === 2) { // 死亡演出(:36925-37064)

```


---

## 🤖 Assistant · 2026-08-19T08:55:06.355Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. `getAttackDamageForProjectiles(classic, expert, e.difficulty)` from '../stats/ScaleStats'. Let me look at ScaleStats to understand the signature and semantics.

Also let me read the duke AI section of bossAI_duke_moonlord.ts (lines 130-500) and Enemy.ts around customFrameIdx + how Renderer consumes it (the 694 precedent at Enemy.ts:5347 and :5485-5512).
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:55:07.926Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"getAttackDamageForProjectiles\\|export function\\|Remap\" ~/Project/GLM/SandboxWorld/game/src/stats/ScaleStats.ts | head; echo '---'; sed -n '1,60p' ~/Project/GLM/SandboxWorld/game/src/stats/ScaleStats.ts",
 "description": "Read ScaleStats getAttackDamageForProjectiles"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:08.069Z

**📎 ToolResult**

```
10://   Utils.GetLerpValue/Remap          Utils.cs:283-320
50:// Utils.GetLerpValue / Remap（Utils.cs:283-320，Remap 重载默认 clamped=true）
52:export function getLerpValue(from: number, to: number, t: number, clamped = false): number {
71:/** Utils.Remap（:313，默认 clamped=true）——float 重载入参先 (float) 对齐 */
72:export function remap(fromValue: number, fromMin: number, fromMax: number, toMin: number, toMax: number): number {
83:export function sampleCurve(keys: readonly CurveKey[], value: number): number {
126://   slider <= 0.33 → Remap(slider, 0, 0.33, 0.5, 1)
127://   else           → Remap(slider, 0.33, 1, 1, 3)
131:export function strengthOfDifficultySlider(slider: number): number {
157:export function mainDifficulty(world: DifficultyWorldView | null | undefined): number {
---
// ============================================================================
// 专家/大师世界强度轴 1:1 移植（Terarria1456 ilspycmd 反编译为唯一标杆）
//   NPC.ScaleStats                    NPC.cs:18081-18105
//   NPC.ScaleStats_ByDifficulty       NPC.cs:18106-18116
//   NPC.ScaleStats_ByDifficulty_Tweaks NPC.cs:18118-18447
//   NPC.ScaleStats_ForExpertHardmode  NPC.cs:18448-18497
//   NPC.ScaleStats_ByPlayerCount      NPC.cs:18498-18659
//   GameDifficultyData.LinearCurve    GameDifficultyData.cs:16-70
//   GameDifficultyLevel               GameDifficultyLevel.cs:8-16
//   Utils.GetLerpValue/Remap          Utils.cs:283-320
//   Main.Difficulty/expertMode/masterMode  Main.cs:2760-2786
//   NPC.GetAttackDamage_ScaledByDifficulty / ForProjectiles  NPC.cs:7015-7035
//   NPC.GetNPCInvasionGroup           NPC.cs:79095-79212
//   NPCID.Sets 四张表                 NPCID.cs:4440/4771/4799/4801
//
// 消费面：Enemy.fromVanilla 造怪（对应原版 NewNPC→SetDefaults→ScaleStats，
// NPC.cs:8322/17791 两个调用点都无差别进 ScaleStats，**Boss 不豁免**——
// 仅 ScaleStats_ForExpertHardmode 对 boss 提前 return，:18471-18474）。
// 本模块纯函数化（状态全走入参/出参 bundle），世界上下文经 bindScaleStatsWorld
// 注入（Game.afterWorldLoad；对应原版 Main 静态单例）。
// ============================================================================
import type { World } from '../world/World';

// ---------------------------------------------------------------------------
// GameDifficultyLevel（GameDifficultyLevel.cs:8-16）：档位是【浮点值】不是枚举序号
//   Journey 0.5 / Classic 1 / Expert 2 / Master 3 / Legendary 4
// ---------------------------------------------------------------------------
export const GDL = {
  JOURNEY: 0.5,
  CLASSIC: 1,
  EXPERT: 2,
  MASTER: 3,
  LEGENDARY: 4,
} as const;

/** float32（C# float 字面量/强转位）。JS number 是 float64，在原版显式 (float) 处对齐 */
export const f32 = (v: number): number => Math.fround(v);

/** C# Math.Round(double)（默认 MidpointRounding.ToEven 银行家舍入：.5 → 就近偶数；
 *  JS Math.round 是 .5 远离零舍入，逐半值处会差 1） */
export const roundCS = (v: number): number => {
  const f = Math.floor(v);
  const d = v - f;
  if (d < 0.5) return f;
  if (d > 0.5) return f + 1;
  return f % 2 === 0 ? f : f + 1;
};

// ---------------------------------------------------------------------------
// Utils.GetLerpValue / Remap（Utils.cs:283-320，Remap 重载默认 clamped=true）
// ---------------------------------------------------------------------------
export function getLerpValue(from: number, to: number, t: number, clamped = false): number {
  if (clamped) {
    if (from < to) {
      if (t < from) return 0;
      if (t > to) return 1;
    } else {
      if (t < to) return 1;
      if (t > from) return 0;
    }

```


---

## 🤖 Assistant · 2026-08-19T08:55:08.306Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts",
 "limit": 140,
 "offset": 130
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:08.335Z

**📎 ToolResult**

```
130	// AI_069 猪鲨鱼龙(NPC 370,NPC.cs:49143-50127)
131	// ---------------------------------------------------------------------------
132	// 状态 ai0:-1 出生(75t) → 一阶段循环 0 悬浮(num3 t)→1 冲撞(num6 t)×5→2 泡泡弹(80t)
133	//   →3 鲨鱼龙卷(90t);血 ≤50% →4 变身(180t) →5 二阶段循环:0→6 冲撞→7 旋转泡泡冲刺(120t)
134	//   →8 鲨鱼龙卷;9(expert 15% 血)二段变身(180t) →10 隐身悬浮→11 冲撞/12 瞬移(30t)/13 旋转冲刺。
135	// 经典参数:悬浮 60t/0.45/7.5、冲撞 30t@16 速、泡泡 80t 每 4t 一发、龙卷 90t(60t 时发射)、变身 180t。
136	
137	const DUKE = {
138	  spawnT: 75,          // num21 :49215
139	  hoverT: 60,          // num3  :49168(经典)
140	  hoverAcc: 0.45,      // num4  :49169
141	  hoverSpd: 7.5,       // num5  :49170
142	  chargeT: 30,         // num6  :49187
143	  chargeSpd: 16,       // num7  :49188
144	  bubbleT: 80,         // num8  :49202
145	  bubbleEvery: 4,      // num9  :49203
146	  bubbleAcc: 0.3,      // num10 :49204
147	  bubbleSpd: 5,        // num11 :49205
148	  nadoT: 90,           // num12 :49206
149	  p1T: 180,            // num13 :49207(一→二阶段变身)
150	  p2T: 180,            // num14 :49208(二段狂暴变身,expert)
151	  teleT: 30,           // num15 :49209(瞬移)
152	  spinT: 120,          // num16 :49210(旋转冲刺)
153	  spinEvery: 4,        // num17 :49211
154	  spinBubbleSpd: 6,    // num18 :49212
155	  spinDashSpd: 20,     // num19 :49213
156	};
157	/** 旋转冲刺角速度 num20 = 2π/(num16/2) = 2π/60(:49214) */
158	const DUKE_SPIN_RATE = TAU / (DUKE.spinT / 2);
159	
160	/** 狂暴判定 flag6(:49238):玩家在太空(y<800)/地下(y>worldSurface*16)/离开两侧海洋带 */
161	function dukeEnraged(game: GameHooks, player: Player): boolean {
162	  const st = game.world.store;
163	  const surface = (game.world.groundLevel || Math.floor(st.h * 0.3)) * TILE;
164	  return player.y < 800 || player.y > surface ||
165	    (player.x > 6400 && player.x < st.w * TILE - 6400);
166	}
167	
168	/** 一阶段悬浮结束的下一招(:49471-49542) */
169	function dukePick1(e: Enemy, enraged: boolean): number {
170	  const a3 = Math.floor(e.ai3);
171	  let next = 0; // 0=无事(原版 switch 无匹配分支,ai2 继续累计)
172	  if (a3 >= 0 && a3 <= 9) next = 1;          // 冲撞
173	  else if (a3 === 10) { e.ai3 = 1; next = 2; } // 泡泡弹
174	  else if (a3 === 11) { e.ai3 = 0; next = 3; } // 鲨鱼龙卷
175	  if (enraged && next === 2) next = 3;       // :49495 狂暴时泡泡弹换龙卷
176	  if (e.hp <= e.maxHp * 0.5) next = 4;       // :49499 半血变身
177	  return next;
178	}
179	/** 二阶段悬浮结束的下一招(:49736-49809) */
180	function dukePick2(e: Enemy, enraged: boolean): number {
181	  const a3 = Math.floor(e.ai3);
182	  let next = 0;
183	  if (a3 >= 0 && a3 <= 5) next = 1;          // 冲撞(6)
184	  else if (a3 === 6) { e.ai3 = 1; next = 2; } // 旋转泡泡冲刺(7)
185	  else if (a3 === 7) { e.ai3 = 0; next = 3; } // 鲨鱼龙卷(8)
186	  // flag2(expert hp≤15%):next=4 → ai0=9(:49756-49759)——经典模式不可达,代码保留见 dukeState9
187	  if (enraged && next === 2) next = 3;       // :49760
188	  return next;
189	}
190	/** 冲撞起手(:49503-49520 / :49764-49781 / :49988-50004 同构):定速直冲+朝向修正 */
191	function dukeCharge(e: Enemy, player: Player, spd: number, toState: number, st: DukeX) {
192	  const dx = player.cx - e.cx, dy = player.cy - e.cy;
193	  const d = Math.hypot(dx, dy) || 1;
194	  e.vx = (dx / d) * spd;
195	  e.vy = (dy / d) * spd;
196	  e.ai0 = toState; e.ai1 = 0; e.ai2 = 0;
197	  e.spin = Math.atan2(e.vy, e.vx);
198	  const s = Math.sign(dx) || st.dir;
199	  st.dir = s;
200	  if (st.spr === 1) e.spin += Math.PI;
201	  st.spr = -s;
202	}
203	/** 悬浮段共用(:49415-49468 / :49680-49733 / :49932-49967 同构):
204	 *  目标点 = 玩家 + (ai1 侧偏, -200);desired = normalize(目标-自身-速度)*spd 后 SimpleFlyMovement */
205	function dukeHover(e: Enemy, player: Player, acc: number, spd: number, sideOff: number, st: DukeX) {
206	  if (e.ai1 === 0) e.ai1 = sideOff * Math.sign(e.cx - player.cx || 1);
207	  const dx = player.cx + e.ai1 - e.cx - e.vx;
208	  const dy = player.cy - 200 - e.cy - e.vy;
209	  const d = Math.hypot(dx, dy) || 1;
210	  e.vx = accelTo(e.vx, (dx / d) * spd, acc);
211	  e.vy = accelTo(e.vy, (dy / d) * spd, acc);
212	  const s = Math.sign(player.cx - e.cx) || st.dir;
213	  if (e.ai2 === 0 && s !== st.dir) e.spin += Math.PI;
214	  st.dir = s;
215	  if (st.spr !== -st.dir) e.spin += Math.PI;
216	  st.spr = -st.dir;
217	}
218	
219	/** AI_069 主入口(经典模式) */
220	export function dukeFishronAI(e: Enemy, game: GameHooks, player: Player | null) {
221	  const st = dukeOf(e);
222	  if (!e.bInit) { e.bInit = true; e.ai0 = -1; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; e.spawnAlpha = 255; } // :49247-49257
223	  const b = baseOf(e);
224	  const enraged = player ? dukeEnraged(game, player) : false;
225	  const flag = e.hp <= e.maxHp * 0.5;                       // flag  :49147 二阶段
226	  const flag3 = e.ai0 > 4;                                  // flag3 :49149(二阶段状态 5-13)
227	  const flag4 = e.ai0 > 9;                                  // flag4 :49150(expert 狂暴段 10-13)
228	  const flag5 = e.ai3 < (flag3 ? 3 : 5) * 2;                // flag5 :49151-49152
229	
230	  // 伤害/防御修正(:49153-49167 + 狂暴 :49239-49245)——每 tick 从基值派生
231	  if (flag4) { e.def.damage = Math.round(b.dmg * 1.1); e.def.defense = 0; }
232	  else if (flag3) { e.def.damage = Math.round(b.dmg * 1.2); e.def.defense = Math.round(b.def * 0.8); }
233	  else { e.def.damage = b.dmg; e.def.defense = b.def; }
234	  if (enraged) { e.def.damage = b.dmg * 2; e.def.defense = b.def * 2; }
235	
236	  // 悬浮/冲撞参数(:49168-49201;expert 档注释)
237	  let hoverT = DUKE.hoverT, hoverAcc = DUKE.hoverAcc, hoverSpd = DUKE.hoverSpd;
238	  if (flag4) { hoverAcc = 0.7; hoverSpd = 12; hoverT = 30; }            // :49171-49176
239	  else if (flag3 && flag5) { hoverAcc = 0.5; hoverSpd = 8; hoverT = 20; } // :49177-49182
240	  else if (flag5 && !flag3 && !flag4) hoverT = 30;                       // :49183-49186
241	  let chargeT = DUKE.chargeT, chargeSpd = DUKE.chargeSpd;
242	  if (flag4) { chargeT = 25; chargeSpd = 27; }                           // :49189-49193(expert 同档)
243	  if (enraged) { hoverT = 10; chargeSpd += 6; }                          // :49239-49245
244	
245	  // 玩家死/远离 5600px(:49218-49237):减速升空离场(原版另 EncourageDespawn(10);
246	  // 本工程 Boss 不参与 despawn 块,故仅保留升空)。原版此处无回血逻辑。
247	  if (!player || player.dead || Math.hypot(player.cx - e.cx, player.cy - e.cy) > 5600) {
248	    e.vy -= 0.4;
249	    e.encourageDespawn(10); // :49234 急升逃离 + EncourageDespawn(10)
250	    e.ai0 = e.ai0 > 4 ? 5 : 0;
251	    e.ai2 = 0;
252	    e.x += e.vx; e.y += e.vy;
253	    return;
254	  }
255	
256	  // ---- 身体旋转朝向(:49258-49345)----
257	  let target = Math.atan2(player.cy - e.cy, player.cx - e.cx);
258	  if (st.spr === 1) target += Math.PI;
259	  if (target < 0) target += TAU; else if (target > TAU) target -= TAU;
260	  if (e.ai0 === -1 || e.ai0 === 3 || e.ai0 === 4 || e.ai0 === 8) target = 0; // :49271-49286
261	  let step = 0.04;                                                            // num23 :49287
262	  if (e.ai0 === 1 || e.ai0 === 6 || e.ai0 === 7) step = 0;                    // :49288-49295
263	  if (e.ai0 === 3 || e.ai0 === 4 || e.ai0 === 8) step = 0.01;                 // :49296-49307
264	  let rot = e.spin;
265	  if (rot < target) rot += (target - rot > Math.PI ? -step : step);
266	  if (rot > target) rot += (rot - target > Math.PI ? step : -step);
267	  if (rot > target - step && rot < target + step) rot = target;
268	  if (rot < 0) rot += TAU; else if (rot > TAU) rot -= TAU;
269	  if (rot > target - step && rot < target + step) rot = target;

```


---

## 🤖 Assistant · 2026-08-19T08:55:13.659Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me continue reading the duke AI (lines 270-500) to see all states and where the frame/anim logic would fit.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:55:14.210Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts",
 "limit": 230,
 "offset": 269
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:14.235Z

**📎 ToolResult**

```
269	  if (rot > target - step && rot < target + step) rot = target;
270	  e.spin = rot;
271	
272	  // ---- 透明度(:49346-49363;近似为 spawnAlpha 渐变)----
273	  // 入实心块 +15/出块 −15,钳 [0,150](★上限 150 非 255——入块半隐,2026-08-19 台账 E 修)
274	  if (e.ai0 !== -1 && e.ai0 < 9) e.spawnAlpha = inSolid(game, e) ? Math.min(150, e.spawnAlpha + 15) : Math.max(0, e.spawnAlpha - 15);
275	
276	  let invuln = false; // flag7(dontTakeDamage = !flag7,:50126)
277	  switch (e.ai0) {
278	    case -1: { // 出生(:49365-49414)
279	      invuln = true;
280	      e.vx *= 0.98; e.vy *= 0.98;
281	      const s = Math.sign(player.cx - e.cx) || st.dir;
282	      st.dir = s; st.spr = -s;
283	      if (e.ai2 > 20) {
284	        e.vy = -2;
285	        e.spawnAlpha = clamp(e.spawnAlpha - 5 + (inSolid(game, e) ? 15 : 0), 0, 150); // :49375-49391
286	      } else if (e.spawnAlpha < 255) e.spawnAlpha = 255;
287	      if (e.ai2 === DUKE.nadoT - 30) { // :49392 出生尘环
288	        game.spawnParticles(e.cx, e.cy, '#8FD8FF', 18, 2.4, { life: 40 });
289	        game.playSfxWav?.('Zombie_20', 1, e.cx, e.cy);   // :49404 PlaySound(29,…,20) 满响(曾借 roar 0.8)
290	      }
291	      e.ai2 += 1;
292	      if (e.ai2 >= DUKE.spawnT) { e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; }
293	      break;
294	    }
295	    case 0: { // 一阶段悬浮(:49415-49543)
296	      if (player.dead) break;
297	      dukeHover(e, player, hoverAcc, hoverSpd, 300, st);
298	      e.ai2 += 1;
299	      if (e.ai2 >= hoverT) {
300	        const next = dukePick1(e, enraged);
301	        if (next === 1) dukeCharge(e, player, chargeSpd, 1, st);
302	        else if (next === 2) { e.ai0 = 2; e.ai1 = 0; e.ai2 = 0; }
303	        else if (next === 3) {
304	          e.ai0 = 3; e.ai1 = 0; e.ai2 = 0;
305	          if (enraged) e.ai2 = DUKE.nadoT - 40; // :49530-49533 狂暴跳过前摇
306	        } else if (next === 4) { e.ai0 = 4; e.ai1 = 0; e.ai2 = 0; }
307	      }
308	      break;
309	    }
310	    case 1: { // 冲撞(:49544-49566)
311	      game.spawnParticles(e.cx + e.w / 2 - Math.cos(e.spin) * e.w * 0.3, e.cy + e.h / 2 - Math.sin(e.spin) * e.h * 0.3, '#8FD8FF', 2, 1.5, { life: 18 });
312	      e.ai2 += 1;
313	      if (e.ai2 >= chargeT) { e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 += 2; }
314	      break;
315	    }
316	    case 2: { // 泡泡弹幕(:49567-49637)
317	      if (player.dead) break;
318	      if (e.ai1 === 0) e.ai1 = 300 * Math.sign(e.cx - player.cx || 1);
319	      const dx = player.cx + e.ai1 - e.cx - e.vx;
320	      const dy = player.cy - 200 - e.cy - e.vy;
321	      const d = Math.hypot(dx, dy) || 1;
322	      e.vx = accelTo(e.vx, (dx / d) * DUKE.bubbleSpd, DUKE.bubbleAcc);
323	      e.vy = accelTo(e.vy, (dy / d) * DUKE.bubbleSpd, DUKE.bubbleAcc);
324	      if (e.ai2 === 0) game.playSfxWav?.('Zombie_20', 1, e.cx, e.cy);   // :49608 PlaySound(29,…,20) 满响(曾借 roar 0.5)
325	      if (e.ai2 % DUKE.bubbleEvery === 0) { // :49610-49618 每 4t 吐一颗爆裂泡泡(NPC 371)
326	        const ddx = player.cx - e.cx, ddy = player.cy - e.cy;
327	        const dd = Math.hypot(ddx, ddy) || 1;
328	        const bub = spawnPart(game, e, 371);
329	        if (bub) {
330	          bub.x = e.cx + (ddx / dd) * ((e.w + 20) / 2) - bub.w / 2;
331	          bub.y = e.cy + (ddy / dd) * ((e.w + 20) / 2) + 45 - bub.h / 2;
332	        }
333	        // :49612 每吐一颗播 PlaySound(4,…,19)=NPC_Killed_19(case4=死音库)
334	        game.playSfxWav?.('NPC_Killed_19', 1, e.cx, e.cy);
335	      }
336	      const s = Math.sign(player.cx - e.cx) || st.dir;
337	      st.dir = s; st.spr = -s;
338	      e.ai2 += 1;
339	      if (e.ai2 >= DUKE.bubbleT) { e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; }
340	      break;
341	    }
342	    case 3: dukeSharknado(e, game, player, st, false); break;          // :49638-49660
343	    case 4: { // 一→二阶段变身(:49661-49679)
344	      invuln = true;
345	      e.vx *= 0.98;
346	      e.vy = lerp(e.vy, 0, 0.02);
347	      if (e.ai2 === DUKE.p1T - 60) game.playSfxWav?.('Zombie_20', 1, e.cx, e.cy);   // :49668 PlaySound(29,…,20)(曾借 roar 0.9)
348	      e.ai2 += 1;
349	      if (e.ai2 >= DUKE.p1T) { e.ai0 = 5; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
350	      break;
351	    }
352	    case 5: { // 二阶段悬浮(:49680-49811)
353	      if (player.dead) break;
354	      dukeHover(e, player, hoverAcc, hoverSpd, 300, st);
355	      e.ai2 += 1;
356	      if (e.ai2 >= hoverT) {
357	        const next = dukePick2(e, enraged);
358	        if (next === 1) dukeCharge(e, player, chargeSpd, 6, st);
359	        else if (next === 2) { // 旋转泡泡冲刺起手(:49782-49797):20 速直冲
360	          const dx = player.cx - e.cx, dy = player.cy - e.cy;
361	          const d = Math.hypot(dx, dy) || 1;
362	          e.vx = (dx / d) * DUKE.spinDashSpd;
363	          e.vy = (dy / d) * DUKE.spinDashSpd;
364	          e.spin = Math.atan2(e.vy, e.vx);
365	          const s = Math.sign(dx) || st.dir;
366	          st.dir = s;
367	          if (st.spr === 1) e.spin += Math.PI;
368	          st.spr = -s;
369	          e.ai0 = 7; e.ai1 = 0; e.ai2 = 0;
370	        } else if (next === 3) { e.ai0 = 8; e.ai1 = 0; e.ai2 = 0; }
371	        else if (next === 4) { e.ai0 = 9; e.ai1 = 0; e.ai2 = 0; } // expert
372	      }
373	      break;
374	    }
375	    case 6: { // 二阶段冲撞(:49812-49834)
376	      game.spawnParticles(e.cx, e.cy, '#8FD8FF', 2, 1.5, { life: 18 });
377	      e.ai2 += 1;
378	      if (e.ai2 >= chargeT) { e.ai0 = 5; e.ai1 = 0; e.ai2 = 0; e.ai3 += 2; }
379	      break;
380	    }
381	    case 7: { // 旋转泡泡冲刺(:49835-49864)
382	      if (e.ai2 === 0) game.playSfxWav?.('Zombie_20', 1, e.cx, e.cy);   // :49839 PlaySound(29,…,20)(曾借 roar 0.6)
383	      if (e.ai2 % DUKE.spinEvery === 0) { // 每 4t 沿垂直方向甩一颗泡泡
384	        const vlen = Math.hypot(e.vx, e.vy) || 1;
385	        const bub = spawnPart(game, e, 371);
386	        game.playSfxWav?.('NPC_Killed_19', 1, e.cx, e.cy);   // :49843 每颗吐音(case4,19)
387	        if (bub) {
388	          bub.bInit = true; bub.ai0 = 0; bub.ai1 = 0;          // 预置初速,跳过自初始化
389	          bub.ai3 = (80 + Math.random() * 41) / 100;            // :49751 随机 scale
390	          bub.x = e.cx + (e.vx / vlen) * ((e.w + 20) / 2) - bub.w / 2;
391	          bub.y = e.cy + (e.vy / vlen) * ((e.w + 20) / 2) + 45 - bub.h / 2;
392	          const ang = Math.atan2(e.vy / vlen, e.vx / vlen) + (Math.PI / 2) * st.dir;
393	          bub.vx = Math.cos(ang) * DUKE.spinBubbleSpd;
394	          bub.vy = Math.sin(ang) * DUKE.spinBubbleSpd;
395	        }
396	      }
397	      // 速度/身体同步旋转(-num20*direction,:49854-49855)
398	      {
399	        const r = -DUKE_SPIN_RATE * st.dir;
400	        const cos = Math.cos(r), sin = Math.sin(r);
401	        const nvx = e.vx * cos - e.vy * sin, nvy = e.vx * sin + e.vy * cos;
402	        e.vx = nvx; e.vy = nvy;
403	        e.spin -= DUKE_SPIN_RATE * st.dir;
404	      }
405	      e.ai2 += 1;
406	      if (e.ai2 >= DUKE.spinT) { e.ai0 = 5; e.ai1 = 0; e.ai2 = 0; }
407	      break;
408	    }
409	    case 8: dukeSharknado(e, game, player, st, true); break;           // :49865-49885
410	    case 9: { // expert 二段狂暴变身(:49886-49931;经典不可达,保留供 expert 接线)
411	      invuln = true;
412	      if (e.ai2 < DUKE.p2T - 90) e.spawnAlpha = clamp(e.spawnAlpha + (inSolid(game, e) ? 15 : -15), 0, 255);
413	      else e.spawnAlpha = Math.min(255, e.spawnAlpha + 4);
414	      e.vx *= 0.98;
415	      e.vy = lerp(e.vy, 0, 0.02);
416	      if (e.ai2 === DUKE.p2T - 60) game.playSfxWav?.('Zombie_20', 1, e.cx, e.cy);   // :49920 PlaySound(29,…,20)(曾借 roar 0.9)
417	      e.ai2 += 1;
418	      if (e.ai2 >= DUKE.p2T) { e.ai0 = 10; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
419	      break;
420	    }
421	    case 10: { // expert 狂暴段悬浮(:49932-50018)
422	      if (player.dead) break;
423	      e.spawnAlpha = Math.min(255, e.spawnAlpha + 25); // 隐身逼近
424	      dukeHover(e, player, hoverAcc, hoverSpd, 360, st);
425	      e.ai2 += 1;
426	      if (e.ai2 >= hoverT) {
427	        const a3 = Math.floor(e.ai3);
428	        const next = (a3 === 0 || a3 === 2 || a3 === 3 || a3 === 5 || a3 === 6 || a3 === 7) ? 1 : 2;
429	        if (next === 1) dukeCharge(e, player, chargeSpd, 11, st);
430	        else { e.ai0 = 12; e.ai1 = 0; e.ai2 = 0; }
431	      }
432	      break;
433	    }
434	    case 11: { // expert 狂暴段冲撞(:50019-50047)
435	      e.spawnAlpha = Math.max(0, e.spawnAlpha - 25);
436	      game.spawnParticles(e.cx, e.cy, '#8FD8FF', 2, 1.5, { life: 18 });
437	      e.ai2 += 1;
438	      if (e.ai2 >= chargeT) { e.ai0 = 10; e.ai1 = 0; e.ai2 = 0; e.ai3 += 1; }
439	      break;
440	    }
441	    case 12: { // expert 瞬移爆冲(:50048-50107)
442	      invuln = true;
443	      e.spawnAlpha = Math.min(255, e.spawnAlpha + 17);
444	      e.vx *= 0.98;
445	      e.vy = lerp(e.vy, 0, 0.02);
446	      if (e.ai2 === DUKE.teleT / 2) { // :50066-50093 中点瞬移到玩家另一侧
447	        if (e.ai1 === 0) e.ai1 = 300 * Math.sign(e.cx - player.cx || 1);
448	        e.x = player.cx - e.ai1 - e.w / 2;
449	        e.y = player.cy - 200 - e.h / 2;
450	        // :50075-50091 侧翻补偿:瞬移后 num41=玩家在新身哪侧,direction 重定;
451	        // spriteDirection != -direction 时 rotation += π(朝向翻转 180°,
452	        // 2026-08-19 台账 E 补——曾漏 = 瞬移后鱼头朝向不变);(原版 :50078 的
453	        // ai[2]==0 门在 ai[2]==num15/2 内恒假=死代码,略)
454	        const s = Math.sign(player.cx - e.cx);
455	        if (s !== 0) {
456	          st.dir = s;
457	          if (st.spr !== -s) e.spin += Math.PI;
458	          st.spr = -s;
459	        }
460	        game.spawnParticles(e.cx, e.cy, '#8FD8FF', 14, 2.4, { life: 30 });
461	        game.playSfxWav?.('Zombie_20', 1, e.cx, e.cy);   // :50064 PlaySound(29,…,20)(曾借 roar 0.6)
462	      }
463	      e.ai2 += 1;
464	      if (e.ai2 >= DUKE.teleT) {
465	        e.ai0 = 10; e.ai1 = 0; e.ai2 = 0; e.ai3 += 1;
466	        if (e.ai3 >= 9) e.ai3 = 0;
467	      }
468	      break;
469	    }
470	    case 13: { // expert 狂暴段旋转冲刺(:50108-50125;不吐泡泡)
471	      if (e.ai2 === 0) game.playSfxWav?.('Zombie_20', 1, e.cx, e.cy);   // :50112 PlaySound(29,…,20)(曾借 roar 0.6)
472	      {
473	        const r = -DUKE_SPIN_RATE * st.dir;
474	        const cos = Math.cos(r), sin = Math.sin(r);
475	        const nvx = e.vx * cos - e.vy * sin, nvy = e.vx * sin + e.vy * cos;
476	        e.vx = nvx; e.vy = nvy;
477	        e.spin -= DUKE_SPIN_RATE * st.dir;
478	      }
479	      e.ai2 += 1;
480	      if (e.ai2 >= DUKE.spinT) { e.ai0 = 10; e.ai1 = 0; e.ai2 = 0; e.ai3 += 1; }
481	      break;
482	    }
483	    default: break;
484	  }
485	  if (invuln) e.iframes = 2;
486	  e.facing = st.spr;
487	  e.x += e.vx;
488	  e.y += e.vy;
489	}
490	
491	/** 鲨鱼龙卷(状态 3 :49638-49660 / 状态 8 :49865-49885 共用):
492	 *  减速悬停,ai2==60(nadoT-30)时发射龙卷水弹 proj 385(伤害 0 的落地生成器)——
493	 *  小龙卷两发斜落(±dir*2, 8)、克苏龙卷一发原地(0,0,ai0=1=追踪型,ai2=狂暴旗)。
494	 *  落地/近身 50px 后由弹体自身 Kill 生成 384/386 龙卷,龙卷逐段向上生长并周期
495	 *  NewNPC 372/373 鲨鱼(见 DukeSharknadoBolt / DukeSharknadoTornado)。 */
496	function dukeSharknado(e: Enemy, game: GameHooks, player: Player, st: DukeX, big: boolean) {
497	  e.vx *= 0.98;
498	  e.vy = lerp(e.vy, 0, 0.02);

```


---

## 🤖 Assistant · 2026-08-19T08:55:30.903Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I understand the Duke AI. The AI states: -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13.

The FindFrame case 370 (vanilla):
- ai0==0 or 5: swim frames 0-5, advance every (num51+1) ticks where num51=5 (ai0==0) or 4 (ai0==5). frame.Y wraps at 6 frames.
  Wait actually: `frameCounter += 1.0; if (frameCounter > num51) { frameCounter = 0; frame.Y += num; }` — advance happens when counter exceeds num51. So for ai0==0: 6 ticks per frame advance (counter 1..6, at 6 >5 → advance). For ai0==5: 5 ticks per frame.
- ai0==1 or 6: frame = ai2 < 10 ? 6 : 7.
- ai0==2 or 7: frame = ai2 < 10 ? 6 : 7.
- ai0==3, 8, or -1: num52=90; if ai2 < 60 || ai2 > 80 → swim anim (advance every 6 ticks); else frame 6 (ai2>70 && ai2<75 → 7).
- ai0==4 or 9: num53=180; if ai2 < 120 || ai2 > 160 → swim anim; else frame 6 (ai2 > 130 && ai2 < 155 → 7).

What about ai0==10-13 (expert enraged states)? The vanilla FindFrame case 370 has no branch for those (they're only reachable in expert; FindFrame doesn't touch them → frame stays whatever it was). Fine, replicate: no change for 10-13.

Now where should this be implemented? The task says "修法:duke AI 侧写 e.customFrameIdx(694 先例)或 Renderer 加 case 370(读 ai0 态+animT)". Let me look at the Enemy.ts frame logic (line 5347 comment about 694, and 5485-5512 the npcFrameT mechanism) to understand the existing machinery. Also how the Renderer consumes customFrameIdx vs default frame cycling.

Let me read Enemy.ts around 5330-5560 and check how `npcFrameT`/frame advancement works generally, plus the Renderer's NPC drawing to see how frameIdx is used (search "customFrameIdx" in Renderer.ts).
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:55:31.444Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 120,
 "offset": 5330
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:31.484Z

**📎 ToolResult**

```
5330	   *  ai[1] 追击计数 >600 加速档（×8/速度4）>650 清零；贴脸 <100 时 ai[1]=-60（L21620-21634）；
5331	   *  noTileCollide 穿墙直移 */
5332	  private cursedSkullAI(game: GameHooks, player: Player | null) {
5333	    // AI_010 全块 1:1（NPC.cs:21552-21888）。flag9 族员 = 694 水书宝箱怪（多状态机）；
5334	    // 34 诅咒头骨/289 巨型诅咒颅走通用悬浮档
5335	    const isMimic = this.vanillaId === 694;
5336	    let maxSpd = 1, accel = 0.011;                 // num145/num146（:21562-21563）
5337	    const num147 = 600, num148 = 650;              // 脱离加速门（:21564-21565）
5338	    let dx = player ? player.cx - this.cx : this.facing * 100;
5339	    let dy = player ? player.cy - this.cy : -100;
5340	    const dist = Math.hypot(dx, dy) || 1;          // num153
5341	    if (this.ai3 !== 3) this.ai1 += 1;             // :21577-21579
5342	    const flag13 = this.ai2 >= 0 && this.ai3 === 2;   // 冲刺态（694 专属）
5343	    const flag14 = this.ai2 >= 0 && this.ai3 === 1;   // 咒球态（694 专属）
5344	    const flag15 = this.ai1 > num147;
5345	    const flag16 = this.ai1 < -30;
5346	    const flag17 = isMimic && !flag13 && !flag14 && !flag15 && flag16;  // 逃逸档
5347	    // 帧机（FindFrame case 694 :77905-77980——AI 侧维护，customFrameIdx 供渲染端直读；
5348	    // 34/289 单帧恒 0 由渲染端缺省，不进此链）
5349	    if (isMimic) this.mimic694Frame();
5350	    // ---- 伪装态 ai[3]==3（:21581-21590）：钉死成"放着的书"——静止、无旋转、
5351	    //      击退免疫；受击 → ai[3]=4 觉醒。AI 早退（不移动不索敌）----
5352	    if (this.ai3 === 3) {
5353	      this.facing = 1; this.visAngle = 0;
5354	      this.vx = 0; this.vy = 0;
5355	      this.kbResistOverride = 0;                   // knockBackResist=0f（:21586）
5356	      if (this.justHit) this.ai3 = 4;              // :21587-21589（frameCounter 清零在帧机）
5357	      return;
5358	    }
5359	    // ---- 觉醒态 ai[3]==4（:21592-21601）：翻书动画 80t，静止，结束转 0----
5360	    if (this.ai3 === 4) {
5361	      this.facing = 1; this.visAngle = 0;
5362	      this.vx = 0; this.vy = 0;
5363	      this.kbResistOverride = 1;                   // knockBackResist=1f（:21597）
5364	      if (this.ai1 > 80) { this.ai1 = 0; this.ai3 = 0; }   // :21598-21600 num149=80
5365	      return;
5366	    }
5367	    if (isMimic) this.kbResistOverride = null;     // :21603-21605 knockBackResist=0.2（def 数据）
5368	    // ---- 逼近/悬停段（:21607-21636；冲刺态跳过）----
5369	    if (!flag13) {
5370	      if (flag15) {
5371	        accel *= 8; maxSpd = 4;                    // 超时脱离加速（:21609-21611）
5372	        if (this.ai1 > num148) this.ai1 = 0;
5373	      } else if (isMimic && player && dist < 100 && this.ai1 >= 0) {
5374	        this.ai1 = -60;                            // 贴脸重置冷却（:21615-21621 flag10 专属）
5375	      } else if (dist < 250) {
5376	        this.ai0 += 0.9;                           // 近距 8 字漂移（:21622-21635）
5377	        if (this.ai0 < -200) this.ai0 = 0;         // 类默认 -1120 钳回（同 swarmerAI 清查）
5378	        this.vy += this.ai0 > 0 ? 0.019 : -0.019;
5379	        this.vx += (this.ai0 < -100 || this.ai0 > 100) ? 0.019 : -0.019;
5380	        if (this.ai0 > 200) this.ai0 = -200;
5381	      }
5382	    }
5383	    // 速度档（:21638-21658）：逃逸 8/0.25 → >350 5/0.3 → >300 3/0.2 → >250 1.5/0.1 → 默认 1/0.011
5384	    if (flag17) { maxSpd = 8; accel = 0.25; }
5385	    else if (dist > 350) { maxSpd = 5; accel = 0.3; }
5386	    else if (dist > 300) { maxSpd = 3; accel = 0.2; }
5387	    else if (dist > 250) { maxSpd = 1.5; accel = 0.1; }
5388	    let sx = (dx / dist) * maxSpd, sy = (dy / dist) * maxSpd;   // num150/num151
5389	    const num154 = sx, num155 = sy;                // 未反向的目标方向（朝向判据）
5390	    if (flag17) { sx = -sx; sy = -sy; }            // :21662-21665 逃逸反向
5391	    if (!player) { sx = this.facing * maxSpd / 2; sy = -maxSpd / 2; }  // 玩家死亡漂移（:21666-21669）
5392	    if (flag13) {
5393	      // 冲刺态速度（:21700-21711）：前 10t 速度 ×0.5（≥18t 归零）；之后以 14px/t
5394	      // 直线冲（方向 = 当前速度，慢于 0.1 时改取朝玩家）
5395	      const n156 = this.ai2;
5396	      if (n156 < 10) {
5397	        this.vx *= 0.5; this.vy *= 0.5;
5398	        if (n156 >= 18) { this.vx = 0; this.vy = 0; }
5399	      } else {
5400	        let vx2 = this.vx, vy2 = this.vy;
5401	        // 玩家死于冲刺段（player=null）保持现速度方向（原版 Main.player[target]
5402	        // 槽位坐标恒可读不判 null——我们等价取"维持最后方向"；曾 player!.cx
5403	        // 对 null 解引用炸整帧敌怪更新,2026-08-19 审计 A-1）
5404	        if (player && Math.hypot(this.vx, this.vy) < 0.1) { vx2 = player.cx - this.cx; vy2 = player.cy - this.cy; }
5405	        const vl = Math.hypot(vx2, vy2) || 1;
5406	        this.vx = (vx2 / vl) * 14;
5407	        this.vy = (vy2 / vl) * 14;
5408	      }
5409	    } else {
5410	      if (this.vx < sx) this.vx += accel;
5411	      else if (this.vx > sx) this.vx -= accel;
5412	      if (this.vy < sy) this.vy += accel;
5413	      else if (this.vy > sy) this.vy -= accel;
5414	    }
5415	    // 朝向/旋转（:21713-21727；冲刺态冻结）：num154>0 → 右向不翻 + atan2；
5416	    // <0 → 翻转 + atan2+π；694 的 spriteDirection 再取反（贴图口朝向与 34 相反）
5417	    if (!flag13) {
5418	      if (num154 > 0) { this.facing = -1; this.visAngle = Math.atan2(num155, num154); }
5419	      else if (num154 < 0) { this.facing = 1; this.visAngle = Math.atan2(num155, num154) + Math.PI; }
5420	      if (isMimic) this.facing *= -1;
5421	    }
5422	    // ---- 巨型诅咒颅 289 暗影焰（:21730-21761）：justHit 清态 + ≤500px 状态机
5423	    //      （0 累计 120t → 1 冲刺段 40t），冲刺段 ai[2]==20 发射暗影焰（速 6、伤 25）----
5424	    if (this.vanillaId === 289) {
5425	      if (this.justHit) { this.ai2 = 0; this.ai3 = 0; }    // :21733-21735（受击打断蓄力）
5426	      dx = player ? player.cx - this.cx : this.facing * 100;
5427	      dy = player ? player.cy - this.cy : -100;
5428	      const d289 = Math.hypot(dx, dy) || 1;
5429	      if (player && d289 <= 500) {
5430	        this.ai2 += 1;
5431	        if (this.ai3 === 0) {
5432	          if (this.ai2 > 120) { this.ai2 = 0; this.ai3 = 1; }
5433	        } else {
5434	          if (this.ai2 === 20) this.shootDart(game, this.cx, this.cy, dx, dy, 6, 25, 299);
5435	          if (this.ai2 > 40) { this.ai3 = 0; this.ai2 = 0; }
5436	        }
5437	      } else { this.ai2 = 0; this.ai3 = 0; }
5438	    }
5439	    this.x += this.vx;
5440	    this.y += this.vy;
5441	    // ---- 694 水书宝箱怪攻击状态机（:21763-21888）----
5442	    if (!isMimic) return;
5443	    if (this.justHit) { this.ai2 = 0; this.ai3 = 0; }      // :21765-21767
5444	    const mcx = this.cx, mcy = this.cy + 10;               // center4 = Center+(0,10)（:21768）
5445	    const mdx = player ? player.cx - mcx : this.facing * 100;
5446	    const mdy = player ? player.cy - mcy : -100;
5447	    const md = Math.hypot(mdx, mdy);                       // num152
5448	    // :21776-21783 flag18 = 中距带[100,300]+态 0/2（冲刺蓄力）;flag19 = ≤500+态 0/1（咒球蓄力）
5449	    const flag18 = md >= 100 && md <= 300 && this.ai2 >= 0 && (this.ai3 === 0 || this.ai3 === 2);

```


---

## 🤖 Assistant · 2026-08-19T08:55:32.866Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"customFrameIdx\\|npcFrameT\" ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts | head; echo '---'; grep -n \"npcFrameT\\|frameIdx\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -30",
 "description": "Find frame index consumption in Renderer and Enemy"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:32.982Z

**📎 ToolResult**

```
646:  if (e.customFrameIdx != null) return Math.min(frames - 1, e.customFrameIdx);
797:  //   每帧写 e.customFrameIdx 直读（694 先例），不经本函数）
846:  //   步进副本 / 站定=0 / 腾空=1）→ customFrameIdx 直读
4320:      // (帧 0/1 与 246 基础帧同构,customFrameIdx 直读不变;曾一直画 NPC_246)
---
1093:  npcFrameT = 0;
5485:   *  npcFrameT = frameCounter（态切换清零），customFrameIdx 供渲染端直读 */
5487:    this.npcFrameT += 1;
5490:      n = 0; this.npcFrameT = 0;
5492:      if (this.npcFrameT >= 5) { this.npcFrameT = 0; n = Math.min(16, n + 1); }
5496:      if (this.npcFrameT >= 5) {
5497:        this.npcFrameT = 0; n += 1;
5503:      if (this.npcFrameT >= 5) { this.npcFrameT = 0; n = Math.min(29, n + 1); }
5506:      if (this.npcFrameT >= 6) {
5507:        this.npcFrameT = 0;
6517:    this.npcFrameT += 1;
6520:      if (this.npcFrameT >= 8) {
6521:        this.npcFrameT = 0;
6524:    } else if (this.npcFrameT >= 13) {
6525:      this.npcFrameT = 0;

```


---

## 🤖 Assistant · 2026-08-19T08:55:36.845Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me look at Renderer.ts lines 640-660 and 790-860 to see how frames are computed, and Enemy.ts lines 5480-5530 for the mimic694Frame precedent (npcFrameT usage).
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:55:37.398Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "limit": 80,
 "offset": 620
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:37.421Z

**📎 ToolResult**

```
620	    s.counter += 1;
621	    if (s.frame < 7) s.frame = 12;
622	    if (s.frame < 10) {
623	      if (s.counter > 8) {
624	        s.frame += 1;
625	        s.counter = 0;
626	        if (s.frame === 10) s.counter = 12;
627	      }
628	    } else if (s.counter < 6) s.frame = 12;
629	    else if (s.counter < 12) s.frame = 11;
630	    else if (s.counter < 18) s.frame = 10;
631	    else {
632	      s.frame = 11;
633	      if (s.counter >= 23) s.counter = 0;
634	    }
635	  } else {
636	    s.counter = 0;
637	    s.frame = 13;
638	  }
639	  return Math.min(frames - 1, s.frame);
640	}
641	
642	/** 按原版 FindFrame 分族规则算当前帧 index（导出供 DebugReport tiles.focus.frameEngine 复算） */
643	export function vanillaFrameIdx(e: Enemy, frames: number): number {
644	  // AI 侧算定的帧号直读（694 水书宝箱怪态机帧——态切换清零的 frameCounter
645	  // 无法从全局 t 推出，cursedSkullAI 的 mimic694Frame 维护）
646	  if (e.customFrameIdx != null) return Math.min(frames - 1, e.customFrameIdx);
647	  const id = e.vanillaId ?? 0;
648	  const ai = e.vanilla?.aiStyle ?? 0;
649	  const t = e.animT; // tick 计数（≈原版 frameCounter 驱动源）
650	  const walking = Math.abs(e.vx) > 0.05;
651	  // 僵尸族（L77049-77085）：行走 0,1,2,1 按 |vx| 累加；腾空=2；站定=0
652	  if (ZOMBIE_FRAME_TYPES.has(id)) {
653	    if (!e.onGround) return Math.min(2, frames - 1);
654	    if (!walking) return 0;
655	    const phase = (e.walkCycleT + Math.abs(e.vx) * 8) % 32; // 每 tick +|vx|，32 一循环
656	    return phase < 8 ? 0 : phase < 16 ? 1 : phase < 24 ? 2 : 1;
657	  }
658	  // 栖息态 NPC（秃鹫 61 cs:24082 ai[0]=0 栖息 / 宝箱怪 85 族 cs:25645 ai[0]=0 伪装）：
659	  // 静止帧 0；激活后从帧 1 起循环
660	  if (ai === 17 || ai === 25) {
661	    // FindFrame case 61(:74235-74255):vx==vy==0 → 帧0(栖息);飞行帧每 5 tick 推进
662	    // (:74247 num148=5),原版用 frameCounter(栖息清零)——全局 t 连续循环视觉等价
663	    if (e.vx === 0 && e.vy === 0) return 0;
664	    return frames > 1 ? 1 + Math.floor(t / 5) % (frames - 1) : 0;
665	  }
666	  // 爬墙蜘蛛族（FindFrame case 165/237/238/240/531, cs:73795-73817）：
667	  // frameCounter += (|vx|+|vy|)×0.5（531 ×0.4），24 一循环 4 帧
668	  if (ai === 40) {
669	    return Math.floor(((e.crawlT ?? 0) / 6)) % frames;
670	  }
671	  // 蜘蛛地面形态（FindFrame case 164/236/239/530, cs:73766-73783）：
672	  // 腾空 vy<0=帧4 / vy>0=帧0；行走 |vx|×1.1 累加 6 步进 0..3 循环
673	  if (id === 164 || id === 236 || id === 239 || id === 530) {
674	    if (!e.onGround) return e.vy < 0 ? Math.min(4, frames - 1) : 0;
675	    if (!walking) return 0;
676	    return Math.floor((e.walkCycleT * 1.1) / 6) % 4;
677	  }
678	  // 黄蜂族（FindFrame case 42，cs:75607-75633）：counter 每 tick+1，2 tick 一换，
679	  // 序列 0→1→2→1→回卷（8 tick 一循环）——翅膀对称拍动
680	  if (id === 42 || (id >= 231 && id <= 235)) {
681	    return [0, 1, 2, 1][Math.floor(t / 2) % 4];
682	  }
683	  // 蝙蝠族（case 49 块 cs:75523-75585）：每 6 tick 推进、回卷含帧 0
684	  // （cs:75577-75584 `if (frame.Y >= num*num305) frame.Y = 0`——此前 max(1,…) 跳过帧 0）
685	  if (ai === 14) {
686	    const cap = BAT_SKIP_LAST.has(id) ? frames - 1 : frames;
687	    return Math.min(frames - 1, Math.floor(t / 6) % Math.max(1, cap));
688	  }
689	  // 史莱姆（case 1, L71506）：每 8 tick 推进，全循环
690	  if (ai === 1) return Math.floor(t / 8) % frames;
691	  // 骷髅王头/手（case 35/36, L67378-67388）：常规恒帧 0；RedHatSkeletron 变体
692	  // （35/36 的 ai[3]==1）帧 1——曾恒 0 = 红帽头/手渲染成普通版(终审修)
693	  if (ai === 11 || ai === 12) return e.vanillaId !== 68 && e.ai3 === 1 ? 1 : 0;
694	  // 兔/地面小动物族（FindFrame case 46，cs:77553-77600：46/47 兔·病害兔、303/337/
695	  // 443/464/540/614、646-652）：站定=帧0 清计数；腾空 vy<0=帧4 / vy>0=帧6；
696	  // 行走 counter += |vx|+1，**>6 才进一帧**、0..frames-1 全帧含帧 0 循环回 0。
697	  // （曾错走城镇 NPC 档帧 2 起每 |vx|*2+1 计——兔子 3 倍速闪帧,2026-08-18 用户报告）
698	  if (id === 46 || id === 47 || id === 303 || id === 337 || id === 443 || id === 464
699	    || id === 540 || id === 614 || (id >= 646 && id <= 652)) {

```


---

## 🤖 Assistant · 2026-08-19T08:55:37.980Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 70,
 "offset": 5478
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:38.005Z

**📎 ToolResult**

```
5478	      this.ai3 = 0;
5479	    }
5480	  }
5481	
5482	  /** 694 帧机（FindFrame case 694，NPC.cs:77905-77980）：
5483	   *  态 3 伪装 → 帧 0；态 4 觉醒 → 帧 0..16（5t/帧）；态 2 冲刺 → 17..19(<40t)/..23；
5484	   *  态 1 咒球 → 24..29；态 0 巡航 → 17/22/23 三帧循环（6t/帧）。
5485	   *  npcFrameT = frameCounter（态切换清零），customFrameIdx 供渲染端直读 */
5486	  private mimic694Frame(): void {
5487	    this.npcFrameT += 1;
5488	    let n = this.customFrameIdx ?? 0;
5489	    if (this.ai3 === 3) {
5490	      n = 0; this.npcFrameT = 0;
5491	    } else if (this.ai3 === 4) {
5492	      if (this.npcFrameT >= 5) { this.npcFrameT = 0; n = Math.min(16, n + 1); }
5493	    } else if (this.ai3 === 2) {
5494	      if (this.ai2 === 0) n = 17;
5495	      if (n < 17 || n > 23) n = 17;
5496	      if (this.npcFrameT >= 5) {
5497	        this.npcFrameT = 0; n += 1;
5498	        if (this.ai2 < 40 && n > 19) n = 19;
5499	        if (n > 23) n = 23;
5500	      }
5501	    } else if (this.ai3 === 1) {
5502	      if (n < 24 || n > 29) n = 24;
5503	      if (this.npcFrameT >= 5) { this.npcFrameT = 0; n = Math.min(29, n + 1); }
5504	    } else {
5505	      if (n < 17 || n > 23) n = 17;
5506	      if (this.npcFrameT >= 6) {
5507	        this.npcFrameT = 0;
5508	        n = n === 17 ? 22 : n === 22 ? 23 : 17;
5509	      }
5510	      if (n >= 30) n = 0;
5511	    }
5512	    this.customFrameIdx = n;
5513	  }
5514	
5515	  // AI_011 骷髅王(35)战斗状态机在 bossAI.ts skeletronBossAI；68 守卫走下方专用分支
5516	
5517	  /** AI_011 地牢守卫(68)（NPC.145.cs:21937-21941, 22277-22288）：
5518	   *  恒 ai[1]=2：伤害 9999、恒速 8 直线追击；玩家死/超 2000px → ai[1]=3 下坠脱场。
5519	   *  noTileCollide 直移。生成瞬间一声 Roar（:21929-21933 localAI[0]==0 单次——
5520	   *  地牢守卫是全游戏唯一"非物品召唤也咆哮"的生成点） */
5521	  private dungeonGuardianAI(game: GameHooks, player: Player | null) {
5522	    if (!this.aiInit) {
5523	      this.aiInit = true; this.ai0 = 1;   // 初始化（L21910；68 无手 NPC）
5524	      game.playSfx('roar', 1, this.cx, this.cy);
5525	    }
5526	    if (!player || Math.abs(this.cx - player.cx) > 2000 || Math.abs(this.cy - player.cy) > 2000) {
5527	      this.ai1 = 3;
5528	    } else if (this.ai1 !== 3) {
5529	      this.ai1 = 2;
5530	    }
5531	    if (this.ai1 === 2) {
5532	      this.def.damage = 9999;
5533	      const dx = player!.cx - this.cx, dy = player!.cy - this.cy;
5534	      const d = Math.hypot(dx, dy) || 1;
5535	      this.vx = (dx / d) * 8;
5536	      this.vy = (dy / d) * 8;
5537	    } else {
5538	      this.vy += 0.1;
5539	      if (this.vy < 0) this.vy *= 0.95;
5540	      this.vx *= 0.95;
5541	    }
5542	    this.x += this.vx;
5543	    this.y += this.vy;
5544	  }
5545	
5546	  /** AI_020 火轮（NPC.cs:24596-24673，type 70）：ai[3]=1+Next(15)*0.1 速度档；
5547	   *  出生 W1 批（2026-08-19）补 TargetClosest + 双取反（:24602-24604 direction 与

```


---

## 🤖 Assistant · 2026-08-19T08:57:03.027Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
I now understand the pattern. The 694 precedent: a private frame method in Enemy.ts (mimic694Frame) called from the AI, using `npcFrameT` as the frameCounter and writing `customFrameIdx`, which `vanillaFrameIdx` in Renderer.ts reads directly at line 646.

For the Duke, the AI lives in bossAI_duke_moonlord.ts (not Enemy.ts). The task says "修法:duke AI 侧写 e.customFrameIdx(694 先例)或 Renderer 加 case 370(读 ai0 态+animT)". The simplest faithful approach: add a `dukeFindFrame(e)` function in bossAI_duke_moonlord.ts called from dukeFishronAI each tick, replicating vanilla FindFrame case 370 exactly, writing e.customFrameIdx. It needs a persistent frameCounter — can use e.npcFrameT (public? it's `npcFrameT = 0` at line 1093, so public). And the frame value persists in customFrameIdx (vanilla frame.Y persists across states; e.g., dash sets frame directly without resetting).

Important: vanilla FindFrame persists `frame.Y` — when dashing (ai0 1/6/2/7), frame.Y is SET to 6 or 7 directly. When returning to swim, the swim animation continues from the current frame.Y (e.g., 6 or 7 → advances to 7, then wraps: `if (frame.Y >= num*6) frame.Y = 0` — so from 7, next advance goes to 8 → >= 6 → 0. So it wraps back into the 0-5 range. OK, replicate exactly:

```
function dukeFindFrame(e: Enemy): void {
  e.npcFrameT += 1;   // frameCounter += 1
  let f = e.customFrameIdx ?? 0;
  const swimAdvance = (threshold: number): void => {
    if (e.npcFrameT > threshold) { e.npcFrameT = 0; f += 1; }
    if (f >= 6) f = 0;
  };
  ...
}
```

Wait, careful: vanilla increments frameCounter FIRST then checks `if (frameCounter > num51)`. And the wrap check `if (frame.Y >= num * 6) frame.Y = 0;` happens every tick after advancing (only inside the branch). Actually:

```csharp
frameCounter += 1.0;
if (frameCounter > (double)num51) {
    frameCounter = 0.0;
    frame.Y += num;
}
if (frame.Y >= num * 6) {
    frame.Y = 0;
}
```

The wrap check runs every tick (regardless of whether advanced) — matters because after dash sets frame.Y = num*7, when returning to swim state, on the first tick the wrap check fires immediately (7 >= 6 → frame 0). Hmm interesting: so after a dash ends and swim resumes, the first FindFrame call in swim state resets frame to 0 if it was 6 or 7. So effectively swim always restarts from 0 after dash. But if swim was at frame 3, it continues from 3.

Wait no — during dash the frame is set to 6/7 directly each tick (frameCounter not touched). After dash ends, ai0 becomes 0 (hover). Then in FindFrame ai0==0: frameCounter += 1; if >5 → advance (6→7? No wait, frame.Y was num*6 or num*7 from dash); regardless of advance, wrap check: frame >= 6 → 0. So on the first hover tick, frame snaps to 0. 

For ai0==3/8/-1 (tornado/transform): the swim branch inside has its own counter += 1 and wrap check. The open-mouth branch (else) sets frame directly.

The dash branch (ai0 1/6/2/7): `if (ai[2] < 10) frame 6 else frame 7` — set every tick.

Note: ai[2] in the dash states — in our AI, charge state ai2 counts up from 0 (e.ai2 += 1 each tick). During charge (ai0==1), ai2 < 10 → frame 6; ≥10 → frame 7. chargeT = 30 ticks. Good.

For tornado state 3/8: ai2 counts 0..90 (nadoT). num52=90: if ai2 < 60 || ai2 > 80 → swim anim; else frame 6 (ai2 > 70 && ai2 < 75 → 7).

For transform state 4 (p1T=180): num53=180: if ai2 < 120 || ai2 > 160 → swim anim; else frame 6 (ai2 > 130 && ai2 < 155 → frame 7).

State 9 (expert p2T=180): ai0==9 → same num53 branch.

State -1 (spawn, 75t): ai0==-1 → same as 3/8 branch (num52=90); ai2 counts 0..75 — always < 60 → swim anim. OK.

States 10-13 (expert enraged): no branch in vanilla FindFrame → frame unchanged (stays at whatever). Our implementation: just don't touch f. Since customFrameIdx persists, that's automatic — but the frameCounter still increments in vanilla? No — for unhandled ai0 values, vanilla FindFrame case 370 does nothing (no counter increment, no frame change). Hmm wait — frameCounter += 1 happens inside the specific ai0 branches only. For states 10-13 nothing happens. OK — so in our function, only increment npcFrameT within the branches that vanilla does.

Careful design:

```ts
/** Duke FindFrame(NPC.cs FindFrame case 370 :72824-72917)— AI 侧维护,customFrameIdx 直读(694 先例) */
function dukeFrame(e: Enemy): void {
  const a0 = Math.floor(e.ai0);
  let f = e.customFrameIdx ?? 0;
  const swim = (threshold: number): void => {   // 游动帧 0-5(threshold=5→6t/帧、4→5t/帧)
    e.npcFrameT += 1;
    if (e.npcFrameT > threshold) { e.npcFrameT = 0; f += 1; }
    if (f >= 6) f = 0;
  };
  if (a0 === 0 || a0 === 5) {
    swim(a0 === 5 ? 4 : 5);   // num51 :72828-72832
  } else if (a0 === 1 || a0 === 6 || a0 === 2 || a0 === 7) {
    f = e.ai2 < 10 ? 6 : 7;   // :72844-72865
  } else if (a0 === 3 || a0 === 8 || a0 === -1) {
    // num52=90 :72868
    if (e.ai2 < 60 || e.ai2 > 80) swim(5);
    else { f = 6; if (e.ai2 > 70 && e.ai2 < 75) f = 7; }  // :72883-72888
  } else if (a0 === 4 || a0 === 9) {
    // num53=180 :72895
    if (e.ai2 < 120 || e.ai2 > 160) swim(5);
    else { f = 6; if (e.ai2 > 130 && e.ai2 < 155) f = 7; } // :72910-72915
  }
  e.customFrameIdx = f;
}
```

Wait, but careful with the swim advance condition: vanilla `if (frameCounter > num51)` where num51=5 for ai0==0 — with counter incremented first. My `swim(5)` = 6 ticks per frame (counter goes 1,2,3,4,5,6 → at 6 >5 reset+advance). Correct.

Hmm — actually double check: counter += 1 → check > 5. Tick sequence: counter values after increment: 1,2,3,4,5,6. At 6, >5 → advance & reset. So yes 6 ticks per frame advance for threshold 5; 5 ticks for threshold 4.

Now: does vanilla FindFrame get called every update tick for flying/any NPC? Yes, FindFrame is called from AI loop each tick (for NPCs that aren't inactive). Our dukeFishronAI is called every fixedUpdate tick, so calling dukeFrame(e) at its top or bottom each tick is equivalent. But careful: our dukeFishronAI has early returns (the !player/despawn path returns early, and case -1 etc all break, no early return except despawn and... let me check: the despawn block at :247-254 returns early. In vanilla, when player is far/dead, AI still runs FindFrame (FindFrame runs regardless of AI branch — FindFrame is called by the main NPC update after AI). Hmm, actually in vanilla, FindFrame is called in NPC.UpdateNPC → ... → after AI, via `FindFrame()` if flag10 etc. Let me confirm FindFrame is called even when despawning. In vanilla NPC.UpdateNPC: `if (aiStyle != 0) ... AI(); ... FindFrame();` — FindFrame runs every tick for every active NPC regardless. So to be exact, dukeFrame should be called unconditionally each tick, including the despawn early-return path. I'll place the dukeFrame(e) call at the very top of dukeFishronAI (before the despawn early return). But wait — at the top, ai2 may not have been incremented yet this tick; in vanilla, AI runs first, then FindFrame reads the updated ai values. E.g., dash: ai2 increments then FindFrame reads ai2. If I call dukeFrame before the switch, it reads the pre-increment ai2 — one tick off. 

Where does vanilla call FindFrame relative to AI? In NPC.UpdateNPC (NPC.cs ~ line 24xxx-25xxx): the sequence is `... this.AI(); ... FindFrame(); ...`. FindFrame comes AFTER AI within the same tick. So the frame computed this tick uses this tick's post-AI ai2. To replicate, call dukeFrame(e) at the END of dukeFishronAI — but there are early returns (despawn path returns before the switch). For the despawn path, vanilla would still run FindFrame after AI returns. The despawn path sets ai0 = ai0 > 4 ? 5 : 0 — under FindFrame, ai0==5 → swim at 5t/frame; ai0==0 → 6t/frame. Fine, call dukeFrame before `return` there too. Simplest: restructure minimally — call `dukeFrame(e)` at the end of the function body, and in the despawn early-return branch call it too before returning. That keeps AI-body untouched (task forbids touching duke AI 本体 — adding frame writing is the sanctioned fix; I'll keep changes surgical: two call sites of dukeFrame, one in the despawn branch, one at the end).

Actually — "禁止动光女状态机主链/猪鲨 AI 本体" — don't modify the Duke AI logic itself. Adding the frame call doesn't alter AI behavior. Good.

Also need to reset npcFrameT on state transitions? Vanilla frameCounter persists across states (it's the NPC's frameCounter, never reset in case 370). It only resets when it exceeds threshold. So keep persistent — npcFrameT is fine (it may be used elsewhere? npcFrameT is Enemy's generic frame counter; duke previously didn't use it. vanillaFrameIdx uses animT, not npcFrameT. OK, using npcFrameT is safe. Actually wait — let me check if npcFrameT is used by the generic Enemy frame tick for NPCs (line 1235: `this.animT++`... line 1252 also animT++). npcFrameT at 1093 — grep shows it used in mimic694Frame and 6517-6525 (some other AI). For duke it's untouched. Good.)

And Renderer: `vanillaFrameIdx` line 646: `if (e.customFrameIdx != null) return Math.min(frames - 1, e.customFrameIdx);` — direct read, no Renderer change needed. 

But wait — how many frames does the Duke sheet have? "8 帧" per the task. `frames` param comes from npcFrameCount presumably (the json). Vanilla NPC_370 has 8 frames (6 swim + 2 mouth). Good — Math.min(frames-1, ...) clamps.

Now — does the ROTATION_NPC rendering path for 370 use vanillaFrameIdx? Presumably yes (line 547-548 comment lists 370 in ROTATION_NPC for flight tilt). The frame row would be customFrameIdx * frameHeight. Should be fine since vanillaFrameIdx is the common path.

Let me now check how `frames` is computed for NPC 370 in the Renderer (npcFrameCount) — check the "npc-frame-golden-gate" memory: json×npcFrameCount×贴图高三方零差. Fine.

Next: WoF death chain in Game.ts. Search for StartHardmode / hardmode / 113 death.
````

</details>


---

## 🤖 Assistant · 2026-08-19T08:57:04.293Z · glm-x-preview-260804

```
猪鲨的情况已经明确了。现在我来处理 `Game.ts` 中 WoF 的死亡链以及 `misc` 公告 API，再加上 `Lang.misc[32]` 键。
```


---

## 🤖 Assistant · 2026-08-19T08:57:05.929Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"StartHardmode\\|startHardmode\\|hardMode\\|113\" ~/Project/GLM/SandboxWorld/game/src/Game.ts | grep -in \"hardmode\\|wof\\|113\" | head -30",
 "description": "Find WoF death and hardmode chain in Game.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:57:05.997Z

**📎 ToolResult**

```
ugrep: warning: ~/Project/GLM/SandboxWorld/game/src/Game.ts: No such file or directory

```


---

## 🤖 Assistant · 2026-08-19T08:57:08.136Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"misc\\[\" ~/Project/GLM/SandboxWorld/game/src --include=*.ts | head -20; echo '---'; grep -rn \"misc\" ~/Project/GLM/SandboxWorld/game/src/core/Lang.ts 2>/dev/null | head; ls ~/Project/GLM/SandboxWorld/game/src/core/ | head -30",
 "description": "Find Lang.misc announcement API usage"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:57:08.239Z

**📎 ToolResult**

```
(eval):1: no matches found: --include=*.ts
---
Achievements.ts
Audio.ts
constants.ts
csCompat.ts
DebugSummonPanel.ts
Game.ts
GfxQuality.ts
HitTile.ts
Input.ts
Options.ts
rng.ts
Sfx.ts

```


---

## 🤖 Assistant · 2026-08-19T08:57:12.608Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Game.ts is in src/core/Game.ts, not src/Game.ts. And the zsh glob issue with `--include=*.ts` — need quotes. Let me redo.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:57:13.890Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"StartHardmode\\|startHardmode\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | head; echo '---'; grep -rn \"misc\\[\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | head -20",
 "description": "Find hardmode chain and Lang.misc usage"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:57:13.993Z

**📎 ToolResult**

```
287:import { createBrickBoxForWallOfFlesh, startHardmode } from '../world/gen/vanilla/HardmodePass';
389:  // （SetEventFlagCleared 捕获的是 StartHardmode **之前**的 hardMode——仅首次击杀
4576:          // hardMode → StartHardmode(置位+V 带转化+洞穴墙回填) → 灯笼夜 19(仅首次)
4581:            const { wasHard } = startHardmode(w);
---
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4567:          // downedPlantBoss，首杀翻转 → BroadcastChatMessage(Lang.misc[33],
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4577:          // → misc[15] 公告 + 成就 9(随本链迁移,2026-08-13 之前击杀即发的旧点已删))
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4603:              // downedMechBoss1&&2&&3 && hardMode → Lang.misc[32] 广播
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4610:          // downed_439 通用置位处直接追加，四塔就位 + 满盾 + misc[43] 公告）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4780:        // hardMode && downedMechBossAny && 1/20 → eclipse=true + misc[20] 公告 +
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4845:        // 派对入夜结算（BirthdayParty.CheckNight :40-53）：进行中则结束 + 粉字广播 misc[99]
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4866:      // 1/3（天顶 1/10）&& 城镇 NPC>=4 → spawnEye + misc[9]。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4891:          // 三机械未全灭 → 三选一（只选未击败；1000 次重抽语义）+ misc[28/29/30]
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7521:          //（关天界事件 + 倒计时 720t + misc[52] 广播 + 清教徒 437/438/379——
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:8013:      // 成功 → Main.eclipse=true + Lang.misc[20] 公告；非白天/已日食/肉前静默不可用——
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:8256:      //      StartBloodMoon：sound 15、moonPhase==4(新月)时拨到 5、misc[8] 公告。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:9208:    // 世界公告（:48991/:49008/:49021——ChatHelper misc[12/13/14 基础,+9=替代矿变体],
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10454:   *  （:54320-54352,对侧已存活则跳过）；1/2 颗世界广播 misc[10/11]；
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:18291:   *  - 血月 = 黄昏 roll 命中体(bloodMoon+清晷冷却+misc[8],Main.cs:64813-64831);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:18293:   *  - 日食 = 黎明 roll 命中体(eclipse+misc[20],Main.cs:64898-64920);黄昏自然清除,
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:19750:    // 公告（SpawnBoss :81492-81496：127 且 mechQueen 命中 → misc[107]，非 HasAwoken）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:19968:   *  default → Announcement.HasAwoken（"{名}已苏醒！"）；125 双子专项 Lang.misc[48]；
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:19983:      announce(Lang.misc(48));                              // 双子魔眼已苏醒！（misc[48]）
~/Project/GLM/SandboxWorld/game/src/world/FurnitureItems.ts:88:    case 'display_doll': return 19; // equip[9] + misc[1] + dye[9]（TEDisplayDoll.cs:156-278）
~/Project/GLM/SandboxWorld/game/src/world/Eclipse.ts:23:/** ChatColors.World（50,255,130）——日食公告（misc[20]，remix 世界 misc[106] 本仓无对应） */

```


---

## 🤖 Assistant · 2026-08-19T08:57:17.102Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 70,
 "offset": 4555
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:57:17.122Z

**📎 ToolResult**

```
4555	          const twinsPart = this.boss.vanillaId === 125 || this.boss.vanillaId === 126;
4556	          const downedKey = `downed_${twinsPart ? 125 : this.boss.vanillaId ?? 0}`;
4557	          // SetEventFlagCleared(NPC.cs:79557) 首次语义:downed 旗标翻转(false→true)
4558	          // 才触发灯笼夜——此前每次击杀都预约(2026-08-13 对齐;肉山 19 在下方链内单独投递)
4559	          const wasDowned = !!w.flags[downedKey];
4560	          // EoW/BoC 陨石首杀快照（NPC.cs:80254-80258：陨石 roll 在
4561	          // SetEventFlagCleared 之前读【旧】downedBoss2——须在写键前捕获；
4562	          // 腐化/猩红共享 downedBoss2，对侧旗一并并入）
4563	          boss2Already = wasDowned
4564	            || !!(this.boss.vanillaId === 266 ? w.flags['downed_13'] : w.flags['downed_266']);
4565	          w.flags[downedKey] = true;
4566	          // 世花首杀公告（NPC.cs:80229-80237 case 262：置旗前捕获旧
4567	          // downedPlantBoss，首杀翻转 → BroadcastChatMessage(Lang.misc[33],
4568	          // ChatColors.World)"地牢中回荡着尖叫声……"——此前缺）
4569	          if (this.boss.vanillaId === 262 && !wasDowned) {
4570	            this.newText(Lang.misc(33), 50, 255, 130);
4571	          }
4572	          // NPC.downedPlantBoss → Wiring 死门接活（Wiring.cs:3216 蜥蜴砖致动 / :1554
4573	          // 神庙传送器捕获：世纪之花前两处 return 拒绝）
4574	          if (this.boss.vanillaId === 262 && this.wiring) this.wiring.planteraDowned = true;
4575	          // 肉山：困难模式世界变换全链（NPC.cs:80281-80292 原序：砖盒 → 捕获旧
4576	          // hardMode → StartHardmode(置位+V 带转化+洞穴墙回填) → 灯笼夜 19(仅首次)
4577	          // → misc[15] 公告 + 成就 9(随本链迁移,2026-08-13 之前击杀即发的旧点已删))
4578	          if (this.boss.vanillaId === 113) {
4579	            const wof = this.boss;
4580	            createBrickBoxForWallOfFlesh(w.store, Math.trunc(wof.cx / 16), Math.trunc(wof.cy / 16), wof.w, w.crimson);
4581	            const { wasHard } = startHardmode(w);
4582	            this.recLog('world', { ev: 'hardmode', on: w.flags.hardMode });   // 行为录制：困难模式置位（肉山首杀）
4583	            if (!wasHard) LanternNight.onGameEventCleared(19);
4584	            this.newText(Lang.misc(15), 50, 255, 130);
4585	            this.achievements.notifyProgressionEvent(9);
4586	          }
4587	          // 首胜灯笼夜预约（NPC.cs NPCLoot 各 case SetEventFlagCleared 实参 →
4588	          // OnGameEventClearedForTheFirstTime default/10/16-18 翻转；4/21/22 排除）。
4589	          // id 表：11 史王 8 蜂后 13 EoC 14 世吞|克脑 15 骷髅王 19 肉山 12 世纪之花
4590	          // 6 石头人 7 猪鲨 9 邪教徒 10 月总 24 史后 23 光女 25 鹿角怪 16/17/18 三王
4591	          if (this.boss.vanillaId != null) {
4592	            const ev = BOSS_GAME_EVENT_BY_NPC[this.boss.vanillaId];
4593	            if (ev !== undefined && !wasDowned) LanternNight.onGameEventCleared(ev);
4594	            // 三王全灭 → 保底世花球茎（NPC.cs:79578-79585 case 16/17/18 →
4595	            // OnGameEventClearedForTheFirstTime 首杀翻转门内 →
4596	            // WorldGen.GeneratePlanteraBulbOnAllMechsDefeated：netMode!=1 &&
4597	            // hardMode && 三旗齐——★补 !wasDowned：原版只在旗标首次翻转那杀
4598	            // 生成（重复杀不超发灯泡，此前每杀都 burst，2026-08-18 修）
4599	            if ((ev === 16 || ev === 17 || ev === 18) && !wasDowned && w.flags.hardMode
4600	              && w.flags['downed_134'] && w.flags['downed_125'] && w.flags['downed_127']) {
4601	              this.evolution.planteraBulbBurst();
4602	              // 三旗首齐公告（NPC.cs:79670-79673 SetEventFlagCleared 尾段：!flag &&
4603	              // downedMechBoss1&&2&&3 && hardMode → Lang.misc[32] 广播
4604	              // "丛林变得焦躁不安……"——!wasDowned=本次击杀才翻转该旗；三旗各只
4605	              // 翻一次 → 恰广播一次（旧档已齐三旗时 wasDowned 恒 true 不补发）
4606	              this.newText(Lang.misc(32), 50, 255, 130);
4607	            }
4608	          }
4609	          // 星璇塔触发（NPC.cs:80194-80197：教徒 439 死 → TriggerLunarApocalypse——
4610	          // downed_439 通用置位处直接追加，四塔就位 + 满盾 + misc[43] 公告）
4611	          if (this.boss.vanillaId === 439) this.triggerLunarApocalypse();
4612	          // Badger's Hat 同日双杀（DoDeathEvents_DropBossPotionsAndHearts 尾段，
4613	          // NPC.cs:79800-79814）：type==4 置 EoCKilledToday / type==113 置 WoFKilledToday
4614	          // （:79805-79811）；双旗齐 → ResetBadgerHatTime + 掉 5004 Badger's Hat
4615	          // （:79812-79814）。记账为运行时态，入夜 StartNight 清零（Main.cs:64703）
4616	          if (this.boss.vanillaId === 4) this.eocKilledToday = true;
4617	          else if (this.boss.vanillaId === 113) this.wofKilledToday = true;
4618	          if (this.eocKilledToday && this.wofKilledToday) {
4619	            this.eocKilledToday = false;
4620	            this.wofKilledToday = false;
4621	            const hat = VI(5004);
4622	            if (hat && ITEM_BY_KEY[hat] !== undefined) {
4623	              this.spawnDrop(this.boss.cx, this.boss.cy, hat, 1);
4624	              this.newText(Lang.itemName(5004) ?? 'Badger’s Hat', 255, 220, 120);

```


---

## 🤖 Assistant · 2026-08-19T08:57:54.597Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Interesting! I found the WoF death chain at Game.ts:4578-4586 and the misc[32] precedent at 4599-4607 for the mech-boss path (NPC.cs:79670-79673, from SetEventFlagCleared tail).

The task group 3: WoF death should ALSO broadcast misc[32] when the three mech flags are all downed and !hardMode (before the kill) — NPC.cs:80287-80290:
```csharp
bool eventFlag = Main.hardMode;
WorldGen.StartHardmode();
if (downedMechBoss1 && downedMechBoss2 && downedMechBoss3 && !eventFlag)
    ChatHelper.BroadcastChatMessage(NetworkText.FromKey(Lang.misc[32].Key), ChatColors.World);
```

Wait — careful. There are two misc[32] sites:
1. NPC.cs:80287-80290 (case 113 WoF death): `if (downedMechBoss1 && downedMechBoss2 && downedMechBoss3 && !eventFlag)` where eventFlag = hardMode BEFORE StartHardmode → broadcast misc[32].
2. NPC.cs:79670-79673 (SetEventFlagCleared tail): `!flag && downedMechBoss1&&2&&3 && hardMode` → misc[32] (the one already implemented at Game.ts:4599-4606).

Wait — hmm, both broadcast misc[32]? Let me check what misc[32] actually says. Let me check Lang.misc in the decompiled source and how our Lang.misc is defined. In vanilla:
- misc[32] = "The jungle grows restless..." (丛林变得焦躁不安)

Site 2 (SetEventFlagCleared): when the third mech flag flips while hardMode → "jungle grows restless" (plantera bulbs). Already implemented.

Site 1 (WoF death, :80287-80290): when mechs are ALL downed but the world wasn't hardmode (drunk/FTW worlds let you summon mechs pre-hardmode... actually in drunk worlds, mechanical bosses can be summoned before WoF) — killing WoF then triggers hardmode AND the "jungle grows restless" message since plantera bulbs should spawn. That's the task: "补 downed_125&&downed_127&&downed_134 全齐且 !hardMode → 公告 misc[32] (drunk/FTW 边缘)".

In our code: at Game.ts:4578-4586, the WoF block: `const { wasHard } = startHardmode(w);` — wasHard is the pre-StartHardmode hardMode. So add after startHardmode:

```ts
if (!wasHard && w.flags['downed_134'] && w.flags['downed_125'] && w.flags['downed_127']) {
  this.newText(Lang.misc(32), 50, 255, 130);
}
```

Wait — vanilla checks downedMechBoss1 && downedMechBoss2 && downedMechBoss3. downedMechBoss1 = Destroyer (134), downedMechBoss2 = Twins (125/126 → our downed_125), downedMechBoss3 = Skeletron Prime (127). Our flags: downed_134, downed_125, downed_127 — exactly what the existing mech path at :4599-4600 uses. 

Also note: should the planteraBulbBurst also happen here? In vanilla, killing WoF when all mechs downed → hardMode starts. Does plantera bulb generation happen? The bulb burst in vanilla happens in SetEventFlagCleared (mech kill chain) only — not in the WoF chain. The WoF chain only broadcasts the message. Hmm wait, but do bulbs spawn? Plantera bulbs in vanilla are generated by WorldGen.PlanteraBulbCheck / UpdatePlanteraBulbs — actually the "GeneratePlanteraBulbOnAllMechsDefeated" is called from SetEventFlagCleared. So WoF death doesn't generate bulbs in vanilla 1.4.5.6. The task only asks for the misc[32] announcement. Stick to the task.

Where exactly to place: after `startHardmode(w)` and before/after LanternNight — vanilla order: CreateBrickBox → capture eventFlag → StartHardmode → check mechs & !eventFlag → broadcast → SetEventFlagCleared(ref eventFlag, 19). So the broadcast happens BEFORE the lantern-night (eventFlag 19). Our existing code: brick box → startHardmode → LanternNight(19) if !wasHard → misc[15] + achievement. Hmm wait — misc[15] announcement... vanilla case 113 doesn't broadcast misc[15] — misc[15] is "The ancient spirits of light and dark have been released." Hmm, actually that might be exactly what SetEventFlagCleared(ref eventFlag, 19) does? SetEventFlagCleared broadcasts misc[15]? Let me check SetEventFlagCleared :79557ish. Actually per the comment at 4577 "→ misc[15] 公告 + 成就 9" — our code already replicates. The ordering difference (lantern night before/after) doesn't matter for the message. I'll insert the misc[32] check right after startHardmode, before the LanternNight line, matching vanilla order (broadcast at :80289 precedes SetEventFlagCleared(19) at :80291).

Hmm wait, actually where is misc[15] broadcast in vanilla? Possibly in SetEventFlagCleared case 19. Order-wise: message misc[32] first, then misc[15]. Our code: newText(misc15) after LanternNight. I'll insert my line right after `startHardmode` line, i.e. before LanternNight/misc15. That preserves vanilla order: misc[32] then misc[15].

Also need to check: `w.flags['downed_134']` etc. are the flag keys used. At :4599-4600 exactly these keys. Good.

Now — Lang.misc function: `Lang.misc(32)`. Check it exists in our Lang (used at 4606 with Lang.misc(32) — yes! misc[32] already used). 

Now group 4: Martian. Let me read bossAI_martian.ts to find the part-shooting sites for projectiles 448/449/450/435.
````

</details>


---

## 🤖 Assistant · 2026-08-19T08:57:55.729Z · glm-x-preview-260804

```
已经找到了 `misc[32]` 的先例（`Game.ts:4606` 处的机械路径）。现在我来处理火星人文件以及原版火星人的伤害部位。
```


---

## 🤖 Assistant · 2026-08-19T08:57:56.677Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"448\\|449\\|450\\|435\\|damage\\|dmg\" ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts | head -50",
 "description": "Find projectile damage sites in bossAI_martian.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:57:56.747Z

**📎 ToolResult**

```
13://                                              循环电击 435;受击打断 -30t）
20:// 弹幕贴图 Projectile_{264,435,438,447-450}.png 已入 sprites/vanilla(见 shootM 注释)。
50:// 弹幕:火星族弹体贴图 Projectile_{264,435,438,447,448,449,450}.png 已按 601/602
53:// ProjectileID.cs 对照:264 RainCloud 雨滴 / 435 MartianTurretBlast(特斯拉电球) /
55:// 448 MartianSaucerCannon(火炮弹) / 449 MartianSaucerLaser(激光) / 450 MartianMissile。
59:  dmg: number, projId: number, life = 300, pierce = 1,
63:    new Arrow(x, y, vx, vy, dmg, 0, projId, null, { grav: 0, life, pierce, hostile: true, ...arrowOpts }),
262:        // 横掠（:36448-36480）：vx=3.5*ai[2];脚下净空<250px 上浮补齐
436:    // 火炮窗 [440,580)（:36124-36150）：每 20t 一发 448,朝向 ±22.5° 散布,速 8;
446:          Math.cos(delta) * 8 * dirx, Math.sin(delta) * 8 * dirx, 50, 448, 3600, 1,
454:    // 激光窗 [280,420)（:36152-36197）：窗内每 6t 一发 449 速 16;窗外只瞄准(ai[2] 角)
467:        shootM(game, e.cx, e.cy, Math.cos(ang) * 16, Math.sin(ang) * 16, 35, 449);
497:  // 空巢发射器（:36221-36279）：窗口内对已灭槽位按概率补射 450 导弹
514:        shootM(game, e.cx + rndRange(50, 70), e.cy + rndRange(30, 45), mvx, mvy, 30, 450, 300, 1,
521:        shootM(game, e.cx + rndRange(50, 70), e.cy + rndRange(30, 45), mvx, mvy, 30, 450, 300, 1,
529:        shootM(game, e.cx + rndRange(30, 60), e.cy + rndRange(-30, -10), mvx, mvy, 30, 450, 300, 1,
536:        shootM(game, e.cx + rndRange(30, 60), e.cy + rndRange(-30, -10), mvx, mvy, 30, 450, 300, 1,
675:    e.def.damage = 80;                 // GetAttackDamage_ScaledByDifficulty(80)
695://   <60 递增,受击 -30;==60 → 放电 435(伤 35,速 14,±100px 抖动) 并置 -120 → 180t 循环
722:  // ---- 电击循环（:35409-35450）----
734:    shootM(game, ox, oy, dx, dy, 35, 435);
893:  private dmg: number;
896:  constructor(src: Enemy, dmg: number) {
899:    this.dmg = dmg;
940:      (game as unknown as { damagePlayer(d: number, x: number, y: number, kx?: number): void })
941:        .damagePlayer(this.dmg, this.cx, this.cy, Math.sign(p.cx - this.cx));

```


---

## 🤖 Assistant · 2026-08-19T08:57:58.077Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"448\\|449\\|450\\|435\" ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria/NPC.cs | awk -F: '$1 > 53000 && $1 < 56000' | head -30",
 "description": "Find martian projectile sites in vanilla NPC.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:57:58.177Z

**📎 ToolResult**

```
ugrep: warning: ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria/NPC.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-19T08:58:03.023Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The ugrep alias seems flaky with awk pipes. Let me retry the vanilla grep differently.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:58:04.334Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \", 448,\\|, 449,\\|, 450,\\|, 435,\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -20",
 "description": "Find NewProjectile sites for martian projectiles"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:58:04.445Z

**📎 ToolResult**

```
6537:		300, 375, 450, 525, 675, 850, 1025, 1325, 1550, 2000,
35449:				Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector127.X, vector127.Y, vector128.X, vector128.Y, 435, num1089, 0f, Main.myPlayer);
36096:								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector141.X, vector141.Y, spinningpoint3.X, spinningpoint3.Y, 448, attackDamage_ForProjectiles9, 0f, Main.myPlayer, 0f, 20f);
36137:								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector142.X, vector142.Y, spinningpoint4.X, spinningpoint4.Y, 449, attackDamage_ForProjectiles10, 0f, Main.myPlayer);
87399:					Gore.NewGore(new Vector2(position.X + 14f, position.Y), velocity, 448, scale);
87403:					Gore.NewGore(position, velocity, 449, scale);
87404:					Gore.NewGore(new Vector2(position.X + 14f, position.Y), velocity, 450, scale);

```


---

## 🤖 Assistant · 2026-08-19T08:58:10.138Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Found:
- :35449 → 435 with num1089 damage (Tesla coil turret)
- :36096 → 448 with attackDamage_ForProjectiles9
- :36137 → 449 with attackDamage_ForProjectiles10
- 450 not found via this pattern — maybe different arg layout (missiles use ai params). Let me search for "450" around the martian saucer section (36000-36300).
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:58:11.536Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"attackDamage_ForProjectiles\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | awk -F: '$1 > 35900 && $1 < 36400'",
 "description": "Find all attackDamage_ForProjectiles defs in saucer section"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:58:11.635Z

**📎 ToolResult**

```
36081:					int attackDamage_ForProjectiles9 = GetAttackDamage_ForProjectiles(50f, 37f);
36096:								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector141.X, vector141.Y, spinningpoint3.X, spinningpoint3.Y, 448, attackDamage_ForProjectiles9, 0f, Main.myPlayer, 0f, 20f);
36105:					int attackDamage_ForProjectiles10 = GetAttackDamage_ForProjectiles(35f, 30f);
36137:								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector142.X, vector142.Y, spinningpoint4.X, spinningpoint4.Y, 449, attackDamage_ForProjectiles10, 0f, Main.myPlayer);
36148:				int attackDamage_ForProjectiles11 = GetAttackDamage_ForProjectiles(50f, 50f);
36160:							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), center24.X, center24.Y, 0f, 0f, 447, attackDamage_ForProjectiles11, 0f, Main.myPlayer, whoAmI + 1);
36169:				int attackDamage_ForProjectiles12 = GetAttackDamage_ForProjectiles(30f, 25f);
36229:							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector143.X, vector143.Y, spinningpoint5.X, spinningpoint5.Y, num1157, attackDamage_ForProjectiles12, 0f, Main.myPlayer);
36241:							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector144.X, vector144.Y, spinningpoint6.X, spinningpoint6.Y, num1157, attackDamage_ForProjectiles12, 0f, Main.myPlayer);
36257:							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector145.X, vector145.Y, spinningpoint7.X, spinningpoint7.Y, num1157, attackDamage_ForProjectiles12, 0f, Main.myPlayer);
36269:							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector146.X, vector146.Y, spinningpoint8.X, spinningpoint8.Y, num1157, attackDamage_ForProjectiles12, 0f, Main.myPlayer);

```


---

## 🤖 Assistant · 2026-08-19T08:58:17.948Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed vanilla values (NPC.cs):
- :36081: 448 = GetAttackDamage_ForProjectiles(50, 37)
- :36105: 449 = GetAttackDamage_ForProjectiles(35, 30)
- :36169: num1157 (=450, the missile) = GetAttackDamage_ForProjectiles(30, 25) — need to confirm num1157 == 450. Let me check around 36200-36230. The task says 450 30→25, matches.
- 435: :35449 num1089 — need to find where num1089 is defined. Task says 35→28.

Let me check num1089 and num1157.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:58:19.877Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"num1089 = \\|num1157 = \" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head; grep -n \"GetAttackDamage_ForProjectiles(35f, 28f)\\|(35f, 28f)\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head",
 "description": "Find num1089 and num1157 definitions"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:58:20.026Z

**📎 ToolResult**

```
35442:				int num1089 = 35;
35448:				num1089 = GetAttackDamage_ForProjectiles(num1089, (float)num1089 * num1090);
36168:				int num1157 = 450;

```


---

## 🤖 Assistant · 2026-08-19T08:58:22.652Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 14,
 "offset": 35440
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:58:22.663Z

**📎 ToolResult**

```
35440					}
35441					vector128 *= 14f;
35442					int num1089 = 35;
35443					float num1090 = 1f;
35444					if (type >= 381 && type <= 392)
35445					{
35446						num1090 = 0.8f;
35447					}
35448					num1089 = GetAttackDamage_ForProjectiles(num1089, (float)num1089 * num1090);
35449					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector127.X, vector127.Y, vector128.X, vector128.Y, 435, num1089, 0f, Main.myPlayer);
35450				}
35451			}
35452			else if (aiStyle == 74)
35453			{

```


---

## 🤖 Assistant · 2026-08-19T08:58:28.945Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
435 (Tesla coil turret blast): damage = GetAttackDamage_ForProjectiles(35, 35 * num1090), where num1090 = 0.8 if type is 381-392 (the event martian NPCs — Tesla Coil is 381? Let me check: 381 = Martian Tesla Coil? The types 381-392 are martian madness NPCs). So expert damage = 35 * 0.8 = 28. Matches the task's "435 35→28".

Now let me check our getAttackDamageForProjectiles in ScaleStats to confirm signature/semantics match (classic, expert, difficulty).
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:58:30.391Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"getAttackDamageForProjectiles\\|GetAttackDamage_ForProjectiles\\|getAttackDamageScaledByDifficulty\" ~/Project/GLM/SandboxWorld/game/src/stats/ScaleStats.ts; echo '---'; sed -n '/export function getAttackDamageForProjectiles/,/^}/p' ~/Project/GLM/SandboxWorld/game/src/stats/ScaleStats.ts",
 "description": "Read getAttackDamageForProjectiles implementation"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:58:30.450Z

**📎 ToolResult**

```
244:export function getAttackDamageScaledByDifficulty(normalDamage: number, difficulty: number): number {
283:/** GetAttackDamage_ForProjectiles（:7031）：Remap(difficulty, Classic, Expert, normal, expert) */
284:export function getAttackDamageForProjectiles(normalDamage: number, expertDamage: number, difficulty: number): number {
584:  s.damage = getAttackDamageScaledByDifficulty(s.damage, s.difficulty);  // :18113
---
export function getAttackDamageForProjectiles(normalDamage: number, expertDamage: number, difficulty: number): number {
  return Math.trunc(remap(difficulty, GDL.CLASSIC, GDL.EXPERT, normalDamage, expertDamage));
}

```


---

## 🤖 Assistant · 2026-08-19T08:58:37.174Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
`getAttackDamageForProjectiles(normalDamage, expertDamage, difficulty)` = Remap(difficulty, 1, 2, normal, expert) truncated. Matches vanilla GetAttackDamage_ForProjectiles(float, float). For classic difficulty=1 → 50; expert=2 → 37; master (3) → Remap clamped → 37. Good.

Now let me read bossAI_martian.ts fully around the shoot sites (lines 420-560 and 690-760), plus check whether the file already imports getAttackDamageForProjectiles, and what `e.difficulty` is (Enemy.difficulty field).
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:58:37.681Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts",
 "limit": 150,
 "offset": 420
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:58:37.706Z

**📎 ToolResult**

```
420	          if (d > 0.001) { sx = (sx / d) * 7; sy = (sy / d) * 7; }
421	          else { sx = 0; sy = -7; }
422	          shootM(game, oxp, oyp, sx, sy, 30, 438);
423	          // 原版骑手 390 射弹无声(:35921-35996)——曾误挂 :36272 导弹段的
424	          // Item39(该音属空巢导弹,2026-08-19 终审删)
425	        }
426	      }
427	    }
428	    return;
429	  }
430	  if (id !== 392 && id !== 393 && id !== 394) return;
431	
432	  // ---- 部件攻击窗（共享 saucer.ai[3] 计数,cs:36128/36171/36235）----
433	  const saucer = m;
434	  e.ai3 = saucer.ai3;
435	  if (id === 394) {
436	    // 火炮窗 [440,580)（:36124-36150）：每 20t 一发 448,朝向 ±22.5° 散布,速 8;
437	    // 出生 ai[1]=20 引信（:36099 NewProjectile 第 10 参）——20t 倒数后点火
438	    // +4 加速(8→12)+8 尘爆+锁定,30t 内 20%/t 转向玩家,180t 自毁/近身 42px 爆炸
439	    //（aiStyle 80 :29801-29890,Kill 爆炸 :70544-70580;life=原版默认 3600）
440	    if (e.ai3 >= 440 && e.ai3 < 580) {
441	      const n = e.ai3 - 440;
442	      if (n % 20 === 0) {
443	        const dirx = spriteDir;
444	        const delta = (Math.random() - 0.5) * 0.7853982;   // ±22.5° 散布（:36133-36136）
445	        shootM(game, e.cx + dirx * 36, e.cy + 8,
446	          Math.cos(delta) * 8 * dirx, Math.sin(delta) * 8 * dirx, 50, 448, 3600, 1,
447	          { martianRocket: true });
448	        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36098 火炮每发(终审补)
449	      }
450	    }
451	    return;
452	  }
453	  if (id === 393) {
454	    // 激光窗 [280,420)（:36152-36197）：窗内每 6t 一发 449 速 16;窗外只瞄准(ai[2] 角)
455	    const inWin = e.ai3 >= 280 && e.ai3 < 420;
456	    if (!inWin && player && !player.dead) {
457	      let dx = player.cx - e.cx, dy = player.cy - e.cy;
458	      if (dy < 0) dy = 0;
459	      const d = Math.hypot(dx, dy);
460	      if (d > 0.001) e.ai2 = Math.atan2(dy / d, dx / d);
461	      else e.ai2 = Math.PI / 2;
462	    }
463	    if (inWin) {
464	      const n = e.ai3 - 280;
465	      if (n % 6 === 0) {
466	        const ang = e.ai2 + (Math.random() - 0.5) * (0.7853982 / 3);
467	        shootM(game, e.cx, e.cy, Math.cos(ang) * 16, Math.sin(ang) * 16, 35, 449);
468	        game.playSfxFiles?.(['Item_12'], 1, e.cx, e.cy);     // :36140 部件激光(392 段 Item12)
469	      }
470	    }
471	    return;
472	  }
473	  // ---- 392 炮体（:36199-36286）----
474	  // 部件全灭检测（:35791-35820）：炮塔/火炮全灭 → 普通模式飞碟 ai0=3 自毁(expert→1)
475	  {
476	    const list = slots.get(e);
477	    const turrets = list ? list.slice(0, 2).filter((p) => !p.dead && p.vanillaId === 393) : [];
478	    const cannons = list ? list.slice(2, 4).filter((p) => !p.dead && p.vanillaId === 394) : [];
479	    let allDead = saucer.ai0 >= 1 || saucer.ai0 < 0 ? false : true;
480	    if (allDead && (turrets.length > 0 || cannons.length > 0)) allDead = false;
481	    if (allDead && saucer.ai0 === 0) {
482	      // :36322 后部件全灭分支：expert → ai0=1 旋转过渡进死光;否则 ai0=3 自毁
483	      if (game.world.isExpert) { saucer.ai0 = 1; saucer.ai1 = 0; saucer.ai2 = 0; saucer.ai3 = 0; }
484	      else { saucer.ai0 = 3; saucer.ai1 = 0; saucer.ai2 = 0; saucer.ai3 = 0; }
485	    }
486	  }
487	  // 死光电报（:36201-36219）：巡航态 ai[3]∈[20,260) 首帧（n==0）→ Projectile 447
488	  if (e.ai3 >= 20 && e.ai3 < 260 && saucer.ai0 === 0) {
489	    if (e.ai3 - 20 === 0) {
490	      // 447 死光电报实体（AI_079）——束体独立类（锚定电报塔/母舰，束高逐tick重算）
491	      // :36701 专家死光生成音 Item12(终审补)
492	      game.playSfxWav?.('Item_12', 1, e.cx, e.cy);
493	      const ray = new MartianDeathray(e, 50);
494	      (game as unknown as { entities: { add(el: unknown, b: string): void } }).entities.add(ray, 'projectiles');
495	    }
496	  }
497	  // 空巢发射器（:36221-36279）：窗口内对已灭槽位按概率补射 450 导弹
498	  {
499	    const list = slots.get(e) ?? [];
500	    const t0 = list[0], t1 = list[1], c0 = list[2], c1 = list[3];
501	    const t0Dead = !t0 || t0.dead || t0.vanillaId !== 393;
502	    const t1Dead = !t1 || t1.dead || t1.vanillaId !== 393;
503	    const c0Dead = !c0 || c0.dead || c0.vanillaId !== 394;
504	    const c1Dead = !c1 || c1.dead || c1.vanillaId !== 394;
505	    let flag76 = false, mv4 = 1000, mv5 = 1000;
506	    if (saucer.ai0 === 2) { flag76 = true; mv4 = 120; mv5 = 120; }
507	    if (!flag76 && e.ai3 >= 280 && e.ai3 < 400) { flag76 = true; mv5 = 90; mv4 = 60; }
508	    if (!flag76 && e.ai3 >= 440 && e.ai3 < 580) { flag76 = true; mv5 = 60; mv4 = 90; }
509	    if (flag76) {
510	      // 炮塔空巢（:36243-36258）:下方侧向抛射
511	      if (t0Dead && rnd(mv4) === 0) {
512	        // :36246-36250 速度 = (±rand3, ±1)×3 未归一(3~9.5 随机,曾归一恒 3)
513	        const mvx = -Math.random() * 3 * 3, mvy = 1 * 3;
514	        shootM(game, e.cx + rndRange(50, 70), e.cy + rndRange(30, 45), mvx, mvy, 30, 450, 300, 1,
515	          { bounce: true });  // aiStyle14 X 反跳(原版 ×-0.1,默认档 -0.5 近似)
516	        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36254 空巢导弹每发(终审补)
517	      }
518	      if (t1Dead && rnd(mv4) === 0) {
519	        // :36246-36250 速度 = (±rand3, ±1)×3 未归一(3~9.5 随机,曾归一恒 3)
520	        const mvx = Math.random() * 3 * 3, mvy = 1 * 3;
521	        shootM(game, e.cx + rndRange(50, 70), e.cy + rndRange(30, 45), mvx, mvy, 30, 450, 300, 1,
522	          { bounce: true });  // aiStyle14 X 反跳(原版 ×-0.1,默认档 -0.5 近似)
523	        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36254 空巢导弹每发(终审补)
524	      }
525	      // 火炮空巢（:36261-36276）:上方侧向抛射
526	      if (c0Dead && rnd(mv5) === 0) {
527	        // :36246-36250 速度 = (±rand3, ±1)×3 未归一(3~9.5 随机,曾归一恒 3)
528	        const mvx = -Math.random() * 3 * 3, mvy = -1 * 3;
529	        shootM(game, e.cx + rndRange(30, 60), e.cy + rndRange(-30, -10), mvx, mvy, 30, 450, 300, 1,
530	          { bounce: true });  // aiStyle14 X 反跳(原版 ×-0.1,默认档 -0.5 近似)
531	        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36254 空巢导弹每发(终审补)
532	      }
533	      if (c1Dead && rnd(mv5) === 0) {
534	        // :36246-36250 速度 = (±rand3, ±1)×3 未归一(3~9.5 随机,曾归一恒 3)
535	        const mvx = Math.random() * 3 * 3, mvy = -1 * 3;
536	        shootM(game, e.cx + rndRange(30, 60), e.cy + rndRange(-30, -10), mvx, mvy, 30, 450, 300, 1,
537	          { bounce: true });  // aiStyle14 X 反跳(原版 ×-0.1,默认档 -0.5 近似)
538	        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36254 空巢导弹每发(终审补)
539	      }
540	    }
541	  }
542	  // ---- FindFrame case 392 counter 副本（cs:72543-72560，393/394 已在上方各自
543	  //      return，函数尾仅 392 到达）：4 帧旋球 counter 每 tick +1、死光电报窗
544	  //      ai[3]∈[20,260) 内 ×2、12 回卷（Renderer 读 e.lai0 → 帧 = counter/3）----
545	  e.lai0 += e.ai3 >= 20 && e.ai3 < 260 ? 2 : 1;
546	  if (e.lai0 >= 12) e.lai0 = 0;
547	}
548	
549	// ---------------------------------------------------------------------------
550	// AI_074 火星无人机 388 + 日耀 Corite 418（NPC.cs:35452-35744,参数表 :35477-35509）
551	// ai[0] 0=悬浮瞄准(LOS+俯角+距离带 → 锁方向) / 1=蓄力(×0.95,30t) / 2=扑咬(steer 追击) /
552	//        3=自爆(388 专属:64px 贴身或撞块;3t 后炸) / 4=418 扑后恢复
553	// ---------------------------------------------------------------------------
554	export function martianDroneAI(e: Enemy, game: GameHooks, player: Player | null) {
555	  const corite = e.vanillaId === 418;
556	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
557	  // 参数表（:35477-35509）：388 / 418
558	  const kbMult = corite ? 0.3 : 0.4;
559	  const spd = corite ? 8 : 10;
560	  const hover = corite ? 175 : 200;
561	  const near = corite ? 175 : 0;
562	  const far = corite ? 600 : 750;
563	  const minNear = corite ? 80 : 0;
564	  const accel = corite ? 60 : 30;
565	  const windup = corite ? 20 : 30;
566	  const decay = corite ? 0.75 : 0.95;
567	  const jitter = corite ? 0 : 50;
568	  const dashSpd = corite ? 9 : 14;
569	  const steerN = corite ? 60 : 20;

```


---

## 🤖 Assistant · 2026-08-19T08:58:48.294Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Found the 448/449/450 sites. Now the 435 site — line 734 area (`shootM(game, ox, oy, dx, dy, 35, 435)` in the Tesla coil turret section, NPC 381? Let me read the section around 690-760 of bossAI_martian.ts to see the Tesla coil (435) site and what NPC id it is (for the num1090 = 0.8 gate check: vanilla `type >= 381 && type <= 392 → num1090 = 0.8` — the Tesla coil shooter at :35409-35450... which aiStyle is that? :35452 says "else if (aiStyle == 74)" so the 435 block is aiStyle 73 (Tesla Coil, type 381? no wait — Tesla Coil is NPC 381? Let me check: the block is before aiStyle 74. The 435 electric blast is from the Tesla Coil NPC (type 381?). Actually the file header says "循环电击 435" in the martian file. num1090 = 0.8 for type in [381,392] — Tesla coil type is 381 (in range → 0.8). Hmm, but which NPC is the 435 shooter? Let me read the section in our file, lines 660-760.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:58:48.983Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts",
 "limit": 90,
 "offset": 665
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:58:48.999Z

**📎 ToolResult**

```
665	  if (canExplode && e.ai0 !== 3 && player && !player.dead
666	    && Math.hypot(player.cx - e.cx, player.cy - e.cy) < 64) {
667	    e.ai0 = 3; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
668	  }
669	  if (e.ai0 === 3) {
670	    // ---- 自爆演出（:35680-35735）：原地膨胀 192×192,3t 后爆炸消散 ----
671	    const cx = e.cx, cy = e.cy;
672	    e.x = cx - 96; e.y = cy - 96;
673	    e.w = 192; e.h = 192;
674	    e.vx = 0; e.vy = 0;
675	    e.def.damage = 80;                 // GetAttackDamage_ScaledByDifficulty(80)
676	    e.spawnAlpha = 255;
677	    e.lightRGB = [0.2, 0.7, 1.1];
678	    game.spawnParticles(cx, cy, '#6FD7FF', 6, 2.4, { life: 30 });
679	    e.ai1 += 1;
680	    if (e.ai1 >= 3) {
681	      game.playSfx('explosion', 1, cx, cy);   // SoundID.Item14
682	      e.iframes = 0;
683	      e.hp = 0;
684	      e.hurt(9999, 0, 0, game);
685	    }
686	    return;
687	  }
688	  // aiStyle 74 常态无 AddLight（:35452-35580 全块无点光——曾挂 [0.1,0.4,0.6] 造假常光）
689	  fly(e);
690	}
691	
692	// ---------------------------------------------------------------------------
693	// AI_073 特斯拉炮塔 387（NPC.cs:35340-35451）
694	// ai[1] <120 = 部署（60-120t 渐显,alpha 255→0,部署期无敌）;ai[0] 电击计时:
695	//   <60 递增,受击 -30;==60 → 放电 435(伤 35,速 14,±100px 抖动) 并置 -120 → 180t 循环
696	// ---------------------------------------------------------------------------
697	export function teslaTurretAI(e: Enemy, game: GameHooks, player: Player | null) {
698	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; }   // 原版 ai[0] 自 0 起 → 首射 60t
699	  if (player && !player.dead) e.facing = player.cx >= e.cx ? 1 : -1;
700	  // 地面摩擦（:35343-35349）
701	  e.vx *= 0.93;
702	  if (e.vx > -0.1 && e.vx < 0.1) e.vx = 0;
703	
704	  if (e.ai1 < 120) {
705	    // ---- 部署（:35353-35401）：渐显 + 部署期无敌 + 环绕尘 ----
706	    e.ai1 += 1;
707	    e.spawnAlpha = e.ai1 > 60 ? Math.round((1 - (e.ai1 - 60) / 60) * 255) : 255;
708	    e.iframes = 2;                       // dontTakeDamage = true
709	    if (e.ai1 % 6 === 0) {
710	      game.spawnParticles(e.cx, e.cy, '#6FD7FF', 1, 0.6, { life: 20 });
711	    }
712	    e.lightRGB = [0.1 * (e.ai1 / 60), 0.5 * (e.ai1 / 60), 0.7 * (e.ai1 / 60)];
713	    e.lightRGBAt = { x: e.cx, y: e.cy - 10 };   // :35404 光源 = Center.Y−10
714	    e.vy = Math.min(e.vy + GRAVITY, MAX_FALL_SPEED);
715	    moveAndCollide(e, game.world, e.vx, e.vy);
716	    return;
717	  }
718	  if (e.ai1 === 120) e.ai1 += 1;         // :35403-35406 单帧过门
719	  e.lightRGB = [0.1, 0.5, 0.7];
720	  e.lightRGBAt = { x: e.cx, y: e.cy - 10 };   // :35411 光源 = Center.Y−10
721	
722	  // ---- 电击循环（:35409-35450）----
723	  if (e.ai0 < 60) e.ai0 += 1;
724	  if (e.justHit) e.ai0 = -30;            // 受击打断充电
725	  if (e.ai0 === 60 && player && !player.dead) {
726	    e.ai0 = -120;
727	    const ox = e.cx, oy = e.cy - 10;
728	    let dx = player.cx - ox, dy = player.cy - oy;
729	    dx += rndRange(-100, 101); dy += rndRange(-100, 101);
730	    dx *= rndRange(70, 131) * 0.01; dy *= rndRange(70, 131) * 0.01;
731	    const d = Math.hypot(dx, dy);
732	    if (d > 0.001) { dx = (dx / d) * 14; dy = (dy / d) * 14; }
733	    else { dx = 0; dy = -14; }
734	    shootM(game, ox, oy, dx, dy, 35, 435);
735	  }
736	  e.vy = Math.min(e.vy + GRAVITY, MAX_FALL_SPEED);
737	  moveAndCollide(e, game.world, e.vx, e.vy);
738	}
739	
740	// ---------------------------------------------------------------------------
741	// AI_072 泡泡盾 384（NPC.cs:35318-35339）：零速钉在军官 383 中心;军官消亡 → 消散
742	// ---------------------------------------------------------------------------
743	export function bubbleShieldAI(e: Enemy, game: GameHooks, _player: Player | null) {
744	  void game; void _player;
745	  const owner = e.master;
746	  if (owner && !owner.dead && owner.vanillaId === 383) {
747	    e.vx = 0; e.vy = 0;
748	    e.x = owner.cx - e.w / 2;
749	    e.y = owner.cy - e.h / 2;
750	    e.lightRGB = [0.1, 0.5, 0.7];
751	  } else {
752	    e.dead = true;   // life=0 + active=false（无掉落）
753	  }
754	}

```


---

## 🤖 Assistant · 2026-08-19T08:58:55.043Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Tesla Turret is NPC 387 ("特斯拉炮塔 387"). Vanilla gate: `type >= 381 && type <= 392 → num1090 = 0.8`. 387 is in range → expert damage = 35 * 0.8 = 28. Good — `getAttackDamageForProjectiles(35, 28, e.difficulty)`.

Now let me check the top of bossAI_martian.ts for imports and the `e.difficulty` field on Enemy, plus whether the saucer parts (393/394/392) have `difficulty`. The getAttackDamageForProjectiles calls need `e.difficulty` — check Enemy.ts for `difficulty`.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:58:56.170Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1,70p' ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts; echo '---DIFF---'; grep -n \"difficulty\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -5",
 "description": "Read martian file header and Enemy difficulty field"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:58:56.217Z

**📎 ToolResult**

```
// 火星疯狂(Martian Madness) AI 家族 1:1 移植(Terarria1456, 1.4.5.6)：
//   aiStyle 80  火星探测器 399                NPC.cs:38129-38223（巡逻→受惊悬停 60t→
//                                              反向加速升空,出屏/180t → Main.StartInvasion(4)）
//   aiStyle 76  火星飞碟核心 395              NPC.cs:36322-36773（600t 攻击循环 六窗口巡航;
//                                              生成 393×2/394×2/392×1;SetDefaults dontTakeDamage
//                                              =true → 部件全灭前无敌,普通模式部件全灭→自毁）
//   aiStyle 75  飞碟部件 392/393/394 + 骑手 390  NPC.cs:35745-36321（锚主体零速跟随;
//                                              393 激光窗[280,420)/394 炮窗[440,580)/392
//                                              死光电报[20,260)+空巢发射器;390 骑 391 射 438）
//   aiStyle 74  火星无人机 388(+日耀 Corite 418) NPC.cs:35452-35744（悬浮瞄准→蓄力→
//                                              扑咬;388 贴身 64px/撞块自爆 192×192 伤 80）
//   aiStyle 73  特斯拉炮塔 387                 NPC.cs:35340-35451（120t 部署渐显→180t
//                                              循环电击 435;受击打断 -30t）
//   aiStyle 72  泡泡盾 384                     NPC.cs:35318-35339（锚军官 383,军官死→消散）
//   aiStyle  3  火星军官 383 / 工程师 386 尾段  NPC.cs:56614-56645 / 59384-59428（军官带盾
//                                              无敌+180t 补盾;工程师 ±5t 扫地放 387,上限 4×自身）
//   aiStyle 49  愤怒云 250(同批普查顺带)        NPC.cs:31742-31810（悬顶 200px,正下方淋雨 264）
// expert 分支(飞碟 ai0=1 旋转过渡/ai0=2 死光弹幕 3600t)按 world.isExpert 真难度开闭
// （World.get isExpert = difficulty >= EXPERT;曾硬编码 EXPERT=false 恒关）;netcode 跳过。
// 弹幕贴图 Projectile_{264,435,438,447-450}.png 已入 sprites/vanilla(见 shootM 注释)。
import type { Enemy } from './Enemy';
import type { GameHooks } from './types';
import type { Player } from './Player';
import { TILE, GRAVITY, MAX_FALL_SPEED } from '../core/constants';
import { moveAndCollide } from '../physics/TileCollision';
import { spawnPart, losClear } from './bossAI';
import { Arrow } from './Arrow';
import { canStartInvasion, startInvasion, INVASION_MARTIAN } from '../world/Invasion';
import { dutchmanCannonAI } from './bossAI_dd2';

/** 原版 localAI[0..3]（Enemy 的 ai0-ai3 对应 ai[],localAI 独立 → WeakMap 落盘） */
const localAI = new WeakMap<Enemy, number[]>();
const la = (e: Enemy): number[] => {
  let a = localAI.get(e);
  if (!a) { a = [0, 0, 0, 0]; localAI.set(e, a); }
  return a;
};
/** 主体 → 部件槽位（395 飞碟与 392 炮体共用 [炮塔0,炮塔1,火炮0,火炮1],cs:36327-36355） */
const slots = new WeakMap<Enemy, Enemy[]>();
/** 军官 383 → 泡泡盾 384 引用（原版 ai[2]=盾 index+1,cs:56618） */
const officerShield = new WeakMap<Enemy, Enemy>();

const rnd = (n: number): number => Math.floor(Math.random() * n);
const rndRange = (a: number, b: number): number => a + Math.floor(Math.random() * (b - a));
const clamp = (v: number, lo: number, hi: number): number => (v < lo ? lo : v > hi ? hi : v);
const lerp = (a: number, b: number, t: number): number => a + (b - a) * t;
const sign = (v: number): number => (v > 0 ? 1 : v < 0 ? -1 : 0);

// ---------------------------------------------------------------------------
// 弹幕:火星族弹体贴图 Projectile_{264,435,438,447,448,449,450}.png 已按 601/602
// 先例自 terraria-assets/Images 补入 public/sprites/vanilla/(Arrow 按 projId 懒加载),
// 此前的 RENDER_PROXY 代渲登记已退役。
// ProjectileID.cs 对照:264 RainCloud 雨滴 / 435 MartianTurretBlast(特斯拉电球) /
// 438 MuonBlast(骑手弹) / 447 MartianDeathray(死光电报,自带 proj AI 未实装→直飞代) /
// 448 MartianSaucerCannon(火炮弹) / 449 MartianSaucerLaser(激光) / 450 MartianMissile。
// ---------------------------------------------------------------------------
function shootM(
  game: GameHooks, x: number, y: number, vx: number, vy: number,
  dmg: number, projId: number, life = 300, pierce = 1,
  arrowOpts?: Partial<import('./Arrow').ArrowOpts>,
): void {
  (game as unknown as { entities: { add: (e: unknown, b: string) => void } }).entities.add(
    new Arrow(x, y, vx, vy, dmg, 0, projId, null, { grav: 0, life, pierce, hostile: true, ...arrowOpts }),
    'projectiles');
}

/** 脚下净空扫描（cs:36400-36421 同构）：返回到第一个实心面的像素距离。
 *  脚下即实心 → 16px（原版 num=1）；150t 内无面 → 150*16 */
function groundGapPx(game: GameHooks, e: Enemy): number {
  const st = game.world.store;
---DIFF---
287:  /** npc.difficulty（ScaleStats 写入，NPC.cs:18086 = strengthOverride ?? Main.Difficulty）：
291:  difficulty = 0;
804:      scale: seedS.scale, difficulty: 0,
807:    e.difficulty = ss.difficulty;          // npc.difficulty（AI 段 GetAttackDamage_* 消费）
1967:   *  Classic, Master, difficulty) 钳 [0,1]——GDL 档位是浮点 Classic=1/Expert=2/

```


---

## 🤖 Assistant · 2026-08-19T08:59:07.700Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. `e.difficulty` is the field. bossAI.ts imports `getAttackDamageForProjectiles` from '../stats/ScaleStats' and calls `getAttackDamageForProjectiles(classic, expert, e.difficulty)`.

Now I have everything for groups 3 and 4. Let me look at the remaining pieces:

For group 1 (Empress), I need to check:
1. `game.world.isExpert` exists (used in bossAI_martian.ts line 483: `game.world.isExpert`). Good.
2. The shoot() signature in bossAI.ts: `shoot(game, x, y, vx, vy, dmg, projId, life?)` — in bossAI_lategame.ts, case 4 calls `shoot(game, px, py, (ax/al)*12, (ay/al)*12, dmg, 919, 240)` — 8th param 240 = life probably.

Let me verify the shoot signature.

Also for group 1, I should double check the vanilla case 11 hover uses vector3 = (0,-350) — from the top: `Vector2 vector3 = new Vector2(0f, -350f);` (line 46303: vector3 = (0,-350); wait line 46303 is vector3 = (0,-350)? Looking at the top: vector = (-150,-250), vector2 = (150,-250), vector3 = (0,-350), vector4 = (0,-350), vector5 = (-80,-500). Yes vector3 = (0,-350). Case 11 uses vector3 in the hover distance check: `Distance(vector12 + vector3) > num3` with num3 = 40. That's empressHover(e, player, 0, -350) — matches.

Let me verify the `shoot` export signature from bossAI.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:59:09.141Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"^export function shoot\\|^function shoot\" ~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts; sed -n \"$(grep -n 'export function shoot' ~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts | head -1 | cut -d: -f1),+8p\" ~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts",
 "description": "Read shoot() signature in bossAI.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:59:09.209Z

**📎 ToolResult**

```
885:export function shoot(game: GameHooks, x: number, y: number, vx: number, vy: number, dmg: number, projId: number, life = 300, arrowOpts?: Partial<import('./Arrow').ArrowOpts>): void {
export function shoot(game: GameHooks, x: number, y: number, vx: number, vy: number, dmg: number, projId: number, life = 300, arrowOpts?: Partial<import('./Arrow').ArrowOpts>): void {
  (game as unknown as { entities: { add: (e: unknown, b: string) => void } }).entities.add(
    new Arrow(x, y, vx, vy, dmg, 0, projId, null, { grav: 0, life, pierce: 1, hostile: true, ...arrowOpts }), 'projectiles');
}

/** NPC.SpawnMechQueen 合体召唤链(NPC.cs:19739-19748,Game.summonMechdusa 调用)：
 *  queen(127) 落位 → markMechQueen(=SpawnBoss :81472 写 ai[3]=mechQueen 非零标记)
 *  → 以 queen Center 为共同出生点同点 NewNPC 125/126/134 + 2×139 探针
 *  (ai2=毁灭者头引用,ai3=∓1 侧位——原版第 7/8 参 ai2/ai3,曾误记 ai0)。

```


---

## 🤖 Assistant · 2026-08-19T08:59:11.518Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"misc\\[32\\]\\|misc(32)\" ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria/Lang.cs | head -3; grep -n \"\\\"Misc\\.\\|MiscMap\\|misc = \" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Lang.cs | head -8",
 "description": "Check Lang.misc definition in vanilla"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:59:11.564Z

**📎 ToolResult**

```
ugrep: warning: ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria/Lang.cs: No such file or directory
33:	public static LocalizedText[] misc = new LocalizedText[201];
145:		RegisterGlobalSubstitution("WorldEvilStone", () => (!WorldGen.crimson) ? Language.GetTextValue("Misc.Ebonstone") : Language.GetTextValue("Misc.Crimstone"));
1166:			text = text + num + (abbreviated ? (" " + Language.GetTextValue("Misc.ShortDays")) : ((num == 1) ? " day" : " days"));
1180:			text = text + num2 + (abbreviated ? (" " + Language.GetTextValue("Misc.ShortHours")) : ((num2 == 1) ? " hour" : " hours"));
1194:			text = text + num3 + (abbreviated ? (" " + Language.GetTextValue("Misc.ShortMinutes")) : ((num3 == 1) ? " minute" : " minutes"));
1201:		return text + time.Seconds + (abbreviated ? (" " + Language.GetTextValue("Misc.ShortSeconds")) : ((time.Seconds == 1) ? " second" : " seconds"));

```


---

## 🤖 Assistant · 2026-08-19T08:59:18.706Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Lang.misc is fine — our Lang.misc(32) already exists and is used at Game.ts:4606 for the same message ("丛林变得焦躁不安" presumably). No l10n work needed since the key is already used.

Now let me verify the vanilla `Boss_CanShootExtraAt` semantics just to be safe for case 11 (to document correctly), and check where misc[32] is in our Lang (exists). Also — for the Empress case 11, the shooting loop has the "for k < num59 (1)" loop plus the extra-player loop. Single player: just one projectile per 3 ticks. But note `Boss_CanShootExtraAt(l, num62 % 3, 3, 2400f)` — for l = the current target? Let me quickly check Boss_CanShootExtraAt to see if it excludes the main player.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:59:20.426Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"private bool Boss_CanShootExtraAt\\|public bool Boss_CanShootExtraAt\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; sed -n \"$(grep -n 'bool Boss_CanShootExtraAt' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -1 | cut -d: -f1),+20p\" ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria/NPC.cs",
 "description": "Read Boss_CanShootExtraAt implementation"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:59:20.484Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
47322:	public bool Boss_CanShootExtraAt(int playerIndex, int rotationIndexToAttack, int rotationSize, float attackScanDistance, bool alwaysSkipMainTarget = true)
sed: ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria/NPC.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-19T08:59:22.690Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 28,
 "offset": 47322
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:59:22.701Z

**📎 ToolResult**

```
47322		public bool Boss_CanShootExtraAt(int playerIndex, int rotationIndexToAttack, int rotationSize, float attackScanDistance, bool alwaysSkipMainTarget = true)
47323		{
47324			if (playerIndex == target && alwaysSkipMainTarget)
47325			{
47326				return false;
47327			}
47328			if (playerIndex % rotationSize != rotationIndexToAttack)
47329			{
47330				return false;
47331			}
47332			Player player = Main.player[playerIndex];
47333			if (!player.active || player.dead || !playerInteraction[playerIndex])
47334			{
47335				return false;
47336			}
47337			if (Distance(player.Center) > attackScanDistance)
47338			{
47339				return false;
47340			}
47341			return true;
47342		}
47343	
47344		private void AI_119_Dandelion()
47345		{
47346			if (!Main.IsItAHappyWindyDay && timeLeft > 10)
47347			{
47348				timeLeft = 10;
47349			}

```


---

## 🤖 Assistant · 2026-08-19T08:59:30.308Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
`Boss_CanShootExtraAt` skips the main target (`playerIndex == target && alwaysSkipMainTarget` → false). So for single player, the extra loop spawns nothing. Our code is single-player; consistent with case 12's existing implementation which skips the extra loop. Good — case 11: one lance every 3 ticks while ai1 < 100 and NPC-to-player distance ≤ 2400.

Now let me check the vanilla Projectile 919's use of ai1 (delay) — the task says our 919 converges to direct flight at 12 speed (used in case 4 & 7 with velocity directly). So for case 11, I'll shoot with velocity = normalize(v2) * 12. That's "同弹型+预测落点排布". 

Now let me check the tests that exist: tests/bossAI-lategame.test.ts etc.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:59:30.898Z · glm-x-preview-260804

```
现在我来检查一下任务中提到的测试，并查看 `bossAI_lategame` 的现有测试结构。
```


---

## 🤖 Assistant · 2026-08-19T08:59:32.536Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/tests/ | grep -i \"bossAI\\|eoc\\|hostile\" | head; echo '---'; grep -n \"describe\\|EMPRESS\\|empress\" ~/Project/GLM/SandboxWorld/game/tests/bossAI-lategame.test.ts | head -20",
 "description": "List relevant test files and empress test structure"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:59:32.577Z

**📎 ToolResult**

```
boss-hostile-proj-sim.test.ts
bossAI-dd2.test.ts
bossAI-deerclops.test.ts
bossAI-lategame.test.ts
bossAI-lunar-misc.test.ts
bossAI-mechdusa.test.ts
bossAI-plantera.test.ts
eoc-dash-probe.test.ts
eoc-dash-speed.test.ts
hostile-proj-player-hit.test.ts
---
5:import { describe, it, expect } from 'vitest';
90:describe('AI_084 邪教徒克隆体 440', () => {
186:describe('AI_100 远古之光 522(邪教徒 ai0=7 召出)', () => {
208:describe('史后仆从 658-660 数据直连', () => {
229:describe('弹幕贴图管线(601/602 先例:PNG 落 sprites/vanilla,Arrow 按 projId 懒加载)', () => {
252:describe('月总召怪段(bossAI_duke_moonlord.ts)', () => {
303:describe('冰雾母云/子体 464（aiStyle 86，Projectile.cs:30747-30821）', () => {
336:describe('闪电球 465 + 闪电链 466（aiStyle 88，Projectile.cs:30860-30937/:31017-31185）', () => {
373:describe('邪教徒弹幕实体化接线', () => {

```


---

## 🤖 Assistant · 2026-08-19T08:59:35.216Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/tests/bossAI-lategame.test.ts",
 "limit": 110
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:59:35.222Z

**📎 ToolResult**

```
1	// 后期 Boss AI 批探针(bossAI_lategame.ts 邪教徒 439/克隆体 440/女皇 636/史后 657
2	// + bossAI_duke_moonlord.ts 月总召怪段):
3	//   克隆体生成节拍 / 环位补位 / 真假区分与死亡反馈 / 远古之光 522 轨道弹 /
4	//   史后仆从 658-660 fromVanilla / 弹幕贴图管线 sprite 断言 / 月总真眼与月噬怪召出。
5	import { describe, it, expect } from 'vitest';
6	import { readFileSync } from 'node:fs';
7	import { Enemy } from '../src/entities/Enemy';
8	import { World } from '../src/world/World';
9	import { TILE } from '../src/core/constants';
10	import { spawnPart } from '../src/entities/bossAI';
11	import { BuffState, BuffType } from '../src/stats/Buffs';
12	import type { GameHooks } from '../src/entities/types';
13	
14	const W = 160, H = 120, FLOOR = 100;
15	
16	function makeWorld(): World {
17	  const w = new World(W, H, 7, 'lategame-test');
18	  const st = w.store;
19	  w.groundLevel = 50;
20	  for (let x = 0; x < W; x++) {
21	    st.setTile(x, FLOOR, 1);
22	    st.setTile(x, FLOOR + 1, 1);
23	  }
24	  return w;
25	}
26	
27	function makeHooks(world: World, playerAt: { x: number; y: number }) {
28	  const enemies: Enemy[] = [];
29	  const projectiles: unknown[] = [];
30	  const em = {
31	    nextId: 1,
32	    add: (e: unknown, bucket: 'enemies' | 'projectiles') => {
33	      const ent = e as { id: number };
34	      ent.id = em.nextId++;
35	      if (bucket === 'enemies') enemies.push(e as Enemy);
36	      else projectiles.push(e);
37	    },
38	  };
39	  const px = playerAt.x * TILE, py = playerAt.y * TILE;
40	  const player = {
41	    x: px, y: py, w: 20, h: 42, cx: px + 10, cy: py + 21,
42	    vx: 0, vy: 0, hp: 400, maxHp: 400, dead: false, useTime: 1,
43	    buffs: new BuffState(),
44	    aabbOverlaps: () => false,
45	  };
46	  const hooks = {
47	    world, player,
48	    enemies: () => enemies,
49	    critters: () => [],
50	    spawnDrop: () => null,
51	    damagePlayer: () => {},
52	    addDamageNumber: () => {},
53	    cutTile: () => {},
54	    onEnemyKilled: () => {},
55	    spawnEnemy: () => {},
56	    spawnParticles: () => {},
57	    notifyInventoryChanged: () => {},
58	    playSfx: () => {},
59	    playSfxFiles: () => {},
60	    showPickupLabel: () => {},
61	    entities: em,
62	  } as unknown as GameHooks;
63	  return { hooks, enemies, projectiles, em, player };
64	}
65	
66	function spawn(h: ReturnType<typeof makeHooks>, id: number, tx: number, ty: number): Enemy {
67	  const e = Enemy.fromVanilla(id, tx * TILE, ty * TILE)!;
68	  e.id = h.em.nextId++;
69	  h.enemies.push(e);
70	  return e;
71	}
72	
73	/** 逐 tick 驱动(默认全部敌人——克隆体镜像需要与真身同拍推进) */
74	function tick(h: ReturnType<typeof makeHooks>, n: number, only?: Enemy[]) {
75	  for (let i = 0; i < n; i++) {
76	    for (const e of only ?? h.enemies) {
77	      if (!e.dead) e.fixedUpdate(1 / 60, h.hooks);
78	    }
79	  }
80	}
81	
82	/** 仪式态直接落位:ai0=5 且跳过出生显影 */
83	function ritualCultist(h: ReturnType<typeof makeHooks>): Enemy {
84	  const cult = spawn(h, 439, 80, 80);
85	  cult.bInit = true;
86	  cult.ai0 = 5; cult.ai1 = 0; cult.ai2 = 0; cult.ai3 = 0;
87	  return cult;
88	}
89	
90	describe('AI_084 邪教徒克隆体 440', () => {
91	  it('仪式 ai1==30 生成节拍:首轮补 2 只克隆体,真身移到离玩家最远环位', () => {
92	    const h = makeHooks(makeWorld(), { x: 80, y: 96 });
93	    const cult = ritualCultist(h);
94	    const x0 = cult.cx, y0 = cult.cy;
95	    tick(h, 31, [cult]);                       // t=0..30,t===30 当帧生成
96	    const clones = h.enemies.filter((n) => n.vanillaId === 440);
97	    expect(clones.length).toBe(2);             // num28 = min(6-0, 2)
98	    expect(cult.ai1).toBe(31);
99	    // 真身 Center += 半径 180 环位偏移(:65652)——位置必须跳变
100	    expect(Math.hypot(cult.cx - x0, cult.cy - y0)).toBeCloseTo(180, 0);
101	    // 克隆体生成坐标:环位(绕真身旧中心)+height/2 底部中心(:65646)
102	    for (const c of clones) {
103	      expect(Math.hypot(c.cx - x0, c.cy - y0)).toBeCloseTo(180, 0);
104	    }
105	  });
106	
107	  it('第二轮仪式:既有克隆体重排环位,只补足到 2 只新造', () => {
108	    const h = makeHooks(makeWorld(), { x: 80, y: 96 });
109	    const cult = ritualCultist(h);
110	    tick(h, 31, [cult]);

```


---

## 🤖 Assistant · 2026-08-19T09:01:00.029Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
I have the test structure. Now let me check what `game.world.isExpert` looks like (World.get isExpert) and the clock.isDay used in the empress code — both already used in the file. Also `game.world.seedFlags.getGoodWorld` precedent.

Now let me write the four changes.

### Group 1: Empress expert table + case 11

In bossAI_lategame.ts:

1. Add `const EMPRESS_CYCLE_P2_EXPERT = [7, 2, 8, 11, 5, 2, 6, 4, 8, 12];` with comment mapping to vanilla slots (:46520-46580, num51 slot 3 → 11 when flag2).

2. In case 1 selection: `const table = phase2 ? (flag2 ? EMPRESS_CYCLE_P2_EXPERT : EMPRESS_CYCLE_P2) : EMPRESS_CYCLE_P1;`

3. Add case 11 block before case 12 (following vanilla order 10→11→12). Content:

```ts
// ---- 11 预测光枪墙 919(expert 表专属拍,:47061-47151):每 3t 在玩家速度反方向
//      100px 处布一杆,瞄玩家 90t 预测位;悬玩家上 (0,-350) ----
case 11: {
  if (e.ai1 === 0) game.playSfxWav?.('Item_162', 1, e.cx, e.cy);   // :47065
  const dur = 100 + (20 - num17);                                  // num58 = 20 - num17（:47067/:47144）
  empressHover(e, player, 0, -350);                                // :47074-47079（vector3/num3）
  // :47080 每 3t 一杆、<100t;:47089 距玩家 >2400 跳过当拍（continue,计时不断）
  if (Math.floor(e.ai1) % 3 === 0 && e.ai1 < 100
    && Math.hypot(player.cx - e.cx, player.cy - e.cy) <= 2400) {
    // v = -玩家速度单位向量(零速兜底 (0,-1))（:47085-47086）
    let vx = -player.vx, vy = -player.vy;
    const vl = Math.hypot(vx, vy);
    if (!(vl > 0)) { vx = 0; vy = -1; } else { vx /= vl; vy /= vl; }
    // vector13 = 玩家 90t 预测位;vector14 = 玩家速度反向 100px 布枪点（:47093-47095）
    const leadX = player.cx + player.vx * 90, leadY = player.cy + player.vy * 90;
    let px = player.cx + vx * 100, py = player.cy + vy * 100;
    // :47096-47104 布枪点距玩家 <100 时外推到 100(v 已单位,防御性死代码 1:1)
    const pd = Math.hypot(px - player.cx, py - player.cy);
    if (pd < 100) {
      let ex = player.cx - px, ey = player.cy - py;
      const el = Math.hypot(ex, ey);
      if (el === 0) { ex = vx; ey = vy; } else { ex /= el; ey /= el; }
      px = player.cx - ex * 100; py = player.cy - ey * 100;
    }
    // v2 = 预测位 - 布枪点 → 弹向（919 收敛实现:12 速直飞）
    const ax = leadX - px, ay = leadY - py;
    const al = Math.hypot(ax, ay) || 1;
    shoot(game, px, py, (ax / al) * 12, (ay / al) * 12,
      dayEnrage ? 9999 : phase2 ? 60 : 50, 919, 240);  // num6 :46332
    // :47114-47140 多人补射门(Boss_CanShootExtraAt 恒跳主目标,单人无效,略)
  }
  e.ai1 += 1;
  if (e.ai1 >= dur) { e.ai0 = 1; e.ai1 = 0; }
  break;
}
```

Wait — check the exact vanilla order in the shoot gate: `if ((int)this.ai[1] % 3 == 0 && this.ai[1] < 100f)` then inside: `Vector2 v = -targetData6.Velocity; v = v.SafeNormalize(-Vector2.UnitY); float num60 = 100f; Vector2 center2 = targetData6.Center; if (Distance(center2) > num2400) continue;` — the distance check is INSIDE the loop after computing v. Our restructure with the gate combined is equivalent (skip → no spawn).

Hmm, one nuance: SafeNormalize(-UnitY) — if velocity is zero, returns -UnitY = (0,-1). If velocity nonzero, normalize. My code: vl > 0 → normalize else (0,-1). Good.

Also the dead-code branch `if (vector14.Distance(center2) < num60)`: since v is unit, vector14 is exactly 100 from center2, so `< 100` is false except NaN. My port replicates it (cheap, 1:1).

DoMagicEffect at [6,54) — visual dust effects (case 2/4 also skip in our impl). Skip, no comment needed... Actually, I could add a small comment noting the skip. Existing cases 2/4 don't mention it. I'll skip.

Now, ordering of the switch cases in our file: 0, 1, 2, 4, 5, 6, 7, 8/9, 10, 12, 13. Insert case 11 between case 10 and case 12.

Also update the header comment block for the Empress section: "3(874 天降极光)与 11/12 为 expert 专属拍,跳过" — this is now stale for 11/12. Line 981: "//   8,9 刀阵冲刺... 10 半血变身传送 / 13 淡出退场...。3(874 天降极光)与 11/12 为 expert 专属拍,跳过。" — update: 12 is already implemented (case 12 exists, classic reachable). Wait, the header says "3(874 天降极光)与 11/12 为 expert 专属拍,跳过" but case 12 IS implemented below with a comment saying "11 才是 expert 专属". The header line 981 is outdated relative to case 12. I'll update the header to reflect: 3 = expert 专属跳过;11 = expert/白天暴怒二阶段表专属拍(已实装);12 已实装。And the table comment at :983-986 needs updating to mention the expert 10-slot table.

Also file header line 8-9: "919/923 仍收敛为带初速直飞(见各处注释)。getGoodWorld 分支已实装...;expert/大师分支只注释不实现" — the expert branches are now partially implemented (flag2 was already implemented). Hmm, line 1029 already implements flag2 = isExpert || dayEnrage. The header is already stale there. I'll make a minimal targeted update mentioning case11/table since that's my change. Let me not over-edit; just update the Empress section comments.

### Group 2: Duke FindFrame

In bossAI_duke_moonlord.ts:
- Add `dukeFindFrame(e)` function (module-level, before dukeFishronAI) with line-number comments for NPC.cs:72824-72917.
- Call it: at the end of dukeFishronAI (after `e.y += e.vy;`) AND in the despawn early-return branch before return (vanilla FindFrame runs regardless of AI branch).

Wait — actually, let me think again about placement. In vanilla, FindFrame is called from NPC.UpdateNPC AFTER AI() — unconditionally per tick (for active NPCs). The despawn branch in our AI returns early, but the AI function still ran (that IS the AI for this tick); FindFrame would still execute after. So calling dukeFindFrame before the `return` in the despawn branch is correct.

Also the ai0 = -1 spawn state: covered (a0 === -1 → the num52 branch). ai2 counts 0..75 there — always < 60 → swim anim every 6t/frame.

One question: `e.npcFrameT` — is it a public field I can write from outside the class? Line 1093 `npcFrameT = 0;` — public by default in TS class. bossAI_duke_moonlord.ts writes e.customFrameIdx? The 694 precedent is inside Enemy.ts (mimic694Frame is a method of Enemy). For duke, I'm writing from the bossAI module — that's the "AI 侧写 e.customFrameIdx" option the task mentions. Enemy fields are public (e.g., e.ai0 writes everywhere in bossAI files). Fine.

Also, does anything else write customFrameIdx for duke currently? grep showed only Enemy.ts (mimic + another at 6519-6526 for... line 6519: `if (this.lai0 === 1) ...` — some other AI). Not duke. Good.

Also — Renderer.vanillaFrameIdx line 646 reads customFrameIdx when non-null. But careful: `vanillaFrameIdx` is only reached if... let me check the ROTATION_NPC drawing path actually uses vanillaFrameIdx for frame row. Let me check how the renderer picks the frame for NPCs generally (the "npc-frame-golden-gate" memory says json×npcFrameCount×texture height). The gate: if customFrameIdx != null → use it. That's the entry of vanillaFrameIdx, so any caller benefits. Duke rendering surely goes through vanillaFrameIdx (it's the general NPC frame function). Let me verify quickly with a grep of where vanillaFrameIdx is called in Renderer and whether duke 370 path could bypass it.

### Group 3: WoF misc[32]

Game.ts:4578-4586: insert after startHardmode:

```ts
// :80287-80290 drunk/FTW 边缘:杀肉山前三机械旗已齐(机械 boss 先于肉山被击杀)
// 且此前非困难模式 → 三旗齐 misc[32] 公告(与 :79670-79673 机械链同一文案;
// 本仓键 downed_134/125/127)
if (!wasHard && w.flags['downed_134'] && w.flags['downed_125'] && w.flags['downed_127']) {
  this.newText(Lang.misc(32), 50, 255, 130);
}
```

Vanilla order: broadcast misc[32] (:80289) BEFORE SetEventFlagCleared(ref eventFlag, 19) (:80291) which internally does lantern night + misc[15]. Our current code: startHardmode → LanternNight → misc(15). So inserting right after startHardmode preserves order misc[32] → (lantern) → misc[15].

### Group 4: Martian expert damage

bossAI_martian.ts:
- import { getAttackDamageForProjectiles } from '../stats/ScaleStats';
- 448 site (line 446): `50` → `getAttackDamageForProjectiles(50, 37, e.difficulty)` — vanilla :36081 GetAttackDamage_ForProjectiles(50f, 37f).
- 449 site (line 467): `35` → `getAttackDamageForProjectiles(35, 30, e.difficulty)` — :36105 (35f, 30f).
- 450 sites (lines 514/521/529/536): `30` → `getAttackDamageForProjectiles(30, 25, e.difficulty)` — :36169 (30f, 25f).
- 435 site (line 734): `35` → `getAttackDamageForProjectiles(35, 28, e.difficulty)` — :35442-35448 (35, 35×0.8=28, type 387 ∈ [381,392] → num1090=0.8).

Wait — the 435 gate: `if (type >= 381 && type <= 392) num1090 = 0.8;`. Our teslaTurretAI is for NPC 387 only? The header says "AI_073 特斯拉炮塔 387". But vanilla aiStyle 73 block — which NPC types share it? aiStyle 73 = TeslaCoil only (387). The type-range check in vanilla covers other hypothetical types but only 387 has aiStyle 73. Actually wait, careful: the block at :35340-35451 — is it a type==387 block or aiStyle==73? :35452 `else if (aiStyle == 74)` suggests preceding block was keyed by... let me check the structure around 35340. It might be `if (type == 387)` inside a big aiStyle switch. The 435 shooting is in the AI_073 block (Tesla Coil). Since only type 387 uses it, num1090 = 0.8 always. So expert 28. Good.

Hmm — but actually, is the 435 shooter possibly also the saucer (395) or others? The comment in our file says AI_073 特斯拉炮塔 387 ... 放电 435. And vanilla :35449 is in that block. OK.

Also check: is there another 435 usage — "循环电击 435" only in teslaTurretAI. Yes, one site.

Now, about `e.difficulty` for these martian entities: 392/393/394/395 parts and 387 — Enemy.fromVanilla sets e.difficulty via ScaleStats (line 807). spawnPart presumably goes through fromVanilla. OK.

Also — the saucer core 395 deathray (447) damage 50 → (50, 50) — same both, skip (no change needed; task only lists 448/449/450/435).

Wait, also line 422: `shootM(game, oxp, oyp, sx, sy, 30, 438)` — rider projectile 438 damage 30. Task doesn't list 438. Check vanilla: the rider 390 shoots 438 — what damage does vanilla use? Let me check :35921-35996. The task says only 448/449/450/435. Let me quickly verify what vanilla does for 438 to make sure I'm not missing a listed item... task explicitly lists four. I'll stick to the four.

Now — where's 447 deathray? `new MartianDeathray(e, 50)` — vanilla :36148 GetAttackDamage_ForProjectiles(50f, 50f) — same value both tiers, no change needed.

Now the Empress group needs one more check: `game.world.isExpert` — used at bossAI_martian.ts:483, and in bossAI_lategame.ts:1029 `game.world.isExpert`. Good.

Let me also double check the test file names to run: tests/bossAI-lategame.test.ts, tests/bossAI-dd2.test.ts, tests/boss-hostile-proj-sim.test.ts, tests/eoc-dash-speed.test.ts. All exist (listed: boss-hostile-proj-sim.test.ts, bossAI-dd2.test.ts, bossAI-lategame.test.ts, eoc-dash-speed.test.ts). 

Now for the Duke frame: need to double check the Renderer path for duke — ROTATION_NPC includes 370; the frame selection. Let me check how ROTATION_NPC NPCs get their frame (search vanillaFrameIdx call sites).
````

</details>


---

## 🤖 Assistant · 2026-08-19T09:01:01.258Z · glm-x-preview-260804

```
所有参考信息已收集完毕。我先确认一下 Renderer 是如何为 Duke 获取帧的（以确保 `customFrameIdx` 会被调用），然后再进行修改。
```


---

## 🤖 Assistant · 2026-08-19T09:01:02.676Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"vanillaFrameIdx\" ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts | head; echo '---'; sed -n '790,850p' ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "description": "Check vanillaFrameIdx call sites and frame logic context"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:01:02.713Z

**📎 ToolResult**

```
643:export function vanillaFrameIdx(e: Enemy, frames: number): number {
4316:      const frameIdx = vanillaFrameIdx(e, frames);
5379:    const frameIdx = vanillaFrameIdx(e, frames);
5899:    const r = this.atlas.vnpc(398, vanillaFrameIdx(e, frames));
5974:    const r = this.atlas.vnpc(397, vanillaFrameIdx(e, Math.max(1, e.vanilla?.frames ?? 1)));
6094:    // origin (95.5,65)、scale 2；帧 0-7（FindFrame case 396 = vanillaFrameIdx 396 档）
6098:      const idx = vanillaFrameIdx(e, 8);
6137:   *  （FindFrame case 400 = vanillaFrameIdx 400 档，0-3）随 rotation（origin
6149:    const r = this.atlas.vnpc(400, vanillaFrameIdx(e, Math.max(1, e.vanilla?.frames ?? 1)));
---
    if (id === 489) return 2 + (Math.floor((e.walkCycleT + t * 0.5) / 8) % len);
    const step = id === 632 || id === 534 || id === 638 || id === 656 ? 12 : 6;
    return 2 + (Math.floor((e.walkCycleT * 2 + t) / step) % len);
  }
  // ============ 火星疯狂/月事件/Betsy FindFrame 批（2026-08-19，逐条 cs 行号）============
  // （须在上方 ai===3 战士族档之前——386 工程师 aiStyle=3 会被截胡；
  //   327 南瓜王/346 圣诞坦克/439·440 教徒的帧机有帧行记忆，由各自 AI 文件
  //   每帧写 e.customFrameIdx 直读（694 先例），不经本函数）
  // 393 飞碟炮塔（cs:72481-72494）：ai[2]=瞄准角→九向帧（ToRotationVector2 分带）；
  //   激光窗 [280,420) 且 (int)ai[3]%6<=2 → +9 射击行（bossAI_martian 393 段
  //   1:1 写 ai2=atan2 角/ai3=母碟共享计数）
  if (id === 393) {
    const ax = Math.cos(e.ai2), ay = Math.sin(e.ai2);
    let f393 = ay > Math.abs(ax) * 2 ? 4
      : ay > Math.abs(ax) * 1.5 ? (ax > 0 ? 5 : 3)
      : Math.abs(ax) > ay * 2 ? (ax > 0 ? 8 : 0)
      : Math.abs(ax) <= ay * 1.5 ? (ax > 0 ? 6 : 2)
      : (ax > 0 ? 7 : 1);
    if (e.ai3 >= 280 && e.ai3 < 420 && (e.ai3 | 0) % 6 <= 2) f393 += 9;
    return Math.min(frames - 1, f393);
  }
  // 394 飞碟火炮（cs:72495-72518）：纯 ai[3] 相位帧——窗前(420-440) 4+n/5 递进、
  //   火炮窗(440-580) (n/4)%4 四帧循环、窗尾(580-600) 7-n/5 回落、其余恒帧 4
  if (id === 394) {
    let n394 = (e.ai3 | 0) - 300;
    let f394: number;
    if (n394 >= 120) {
      n394 -= 120;
      if (n394 >= 160) f394 = 7 - Math.floor((n394 - 160) / 5);
      else if (n394 >= 20) f394 = Math.floor(n394 / 4) % 4;
      else f394 = 4 + Math.floor(n394 / 5);
    } else f394 = 4;
    return Math.min(frames - 1, f394);
  }
  // 395 飞碟母碟（cs:72520-72541）：counter 每 tick +1（66 回卷，帧=counter/6 → 0-10）；
  //   死光电报窗 ai[3]∈[20,260) 内再 +1 且钳 [36,53] → 恒落帧 6-8 蓄能辉光带。
  //   counter 副本由 bossAI_martian martianSaucerAI 累进到 e.lai0（蜂后 222 先例）
  if (id === 395) return Math.min(frames - 1, Math.floor((e.lai0 % 66) / 6));
  // 392 飞碟炮体（cs:72543-72560）：4 帧旋球 counter 每 tick +1（电报窗内 ×2）、
  //   12 回卷，帧=counter/3；副本在 bossAI_martian martianSaucerPartAI 尾段
  if (id === 392) return Math.min(frames - 1, Math.floor((e.lai0 % 12) / 3));
  // 399 火星探测器（cs:72562-72565）：counter 每 tick +0.25 四帧扫描带（0.25t/帧）；
  //   ai[0]≠0（受惊悬停/逃逸）→ +4 警戒带
  if (id === 399) {
    return Math.min(frames - 1, Math.floor((t * 0.25) % 4) + (e.ai0 !== 0 ? 4 : 0));
  }
  // 387 特斯拉炮塔（cs:72335-72368）：两帧电球——ai[0]>0 充电档 counter 每 tick
  //   +1（≥20 再 +1、≥40 再 +1，10 单位/帧）；ai[0]≤0 待机 15 单位/帧。
  //   相位取全局 t（2 帧闪切，相位任意视觉等价）
  if (id === 387) {
    const per387 = e.ai0 > 0 ? 10 / (1 + (e.ai0 >= 20 ? 1 : 0) + (e.ai0 >= 40 ? 1 : 0)) : 15;
    return Math.min(frames - 1, Math.floor(t / per387) % 2);
  }
  // 386 火星工程师（cs:72369-72402）：帧机在 bossAI_martian martianFighterExtras
  //   内逐 tick 副本（放塔期 ai2>0 帧 9/10 每 12t 交替 / 行走带 2-8 counter +=
  //   |vx|*2（无 +1）、>6 进帧——增量 >1 时越限溢出丢弃,公式折算会快进 → 须
  //   步进副本 / 站定=0 / 腾空=1）→ customFrameIdx 直读
  // 325 哀木（cs:73172-73201）：站定带 0-4 / 移动带 5-9，counter 恒 +1/t、>4 进帧
  //   （两分支同速 → counter ≡ animT，无 AI 侧状态；带切换瞬间带内相位任意，登记）
  if (id === 325) {
    return Math.min(frames - 1, e.vx === 0 ? Math.floor(t / 5) % 5 : 5 + (Math.floor(t / 5) % 5));

```


---

## 🤖 Assistant · 2026-08-19T09:01:08.191Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
vanillaFrameIdx is called at Renderer.ts:4316 and 5379 for general NPC drawing. Let me quickly check the context at 4316 and 5379 to ensure the Duke drawing path (which likely passes through one of these) will respect customFrameIdx. Line 4316 — let me look at what's around there (it mentioned "246 基础帧同构,customFrameIdx 直读不变;曾一直画 NPC_246" at 4320 — that's the martian... whatever). Let me just check 5379's context quickly, and also check where ROTATION_NPC is consumed.
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:01:09.926Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '5360,5395p' ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts; echo '---'; grep -n \"ROTATION_NPC\" ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts | head -5",
 "description": "Check NPC draw path frame selection and ROTATION_NPC usage"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:01:09.967Z

**📎 ToolResult**

```
  /** 风气球 594（Main.cs:23380-23406 + FindFrame case 594 :68652-68656 独占绘制）：
   *  - 贴图 NPC_594.png 为 8 列变体横条 32×76/帧；变体 = ai[2]（1-7 装饰随机）
   *  - 携带史莱姆（slave ai0=-999）时：帧 0 以 slave 的 alpha+color 两遍绘制
   *    （气球壳染成史莱姆色），scale 取 slave.scale；之后叠 ai[2] 变体帧
   *  - 锚点 = npc.Top + origin(0.5,0)（顶部居中）,随 rotation(visAngle) 倾斜 */
  /** 402 星尘织带蠕虫（Main.cs:23848-23889 case 402 独占自绘，1:1）：
   *  单 NPC 无段链——视觉节段 = oldPos 间隔 2 取样，每档两份（第二份向更旧帧
   *  lerp 0.5 补位），贴图 404/403 交替 + Glow_134/133 加色罩（A=0 白的 additive
   *  语义用 lighter 还原）。本体 alpha = Opacity×(0.8−0.14·i/2)、glow = 1−0.14·i/2，
   *  全乘生命末段渐隐 num291（ai[2] 0→600 计时，最后 5% 线性淡出 :23858-23861）。
   *  头 = NPC_402 + Glow_135×num291。锚点 = 碰撞盒中心（origin halfSize），旋转
   *  随 visAngle/oldRot。头中心尾接 DrawPrettyStarSparkle（:23888 → 原语
   *  drawPrettyStarSparkle；ai[2] 计时链在 Enemy.wormAI 402 段驱动）。 */
  /** 266 克苏鲁之脑（Main.cs:24799-24843 专家/FTW 四镜像 + :22949-22951 Y 下垂）：
   *  life<lifeMax 且（专家 || FTW）→ 以玩家中心镜像画 4 份：alpha 因子 =
   *  1-life/lifeMax（专家 ×2，FTW 置 1）平方后钳 0..1，乘进整体 alpha；
   *  镜像位 = 玩家中心 ±(|dx|,|dy|)（num145 0..3：X 取正 0/2、Y 取正 0/1）。
   *  本体照常最后画。全体绘制 Y 偏移 +50×scale（Main.cs:22950 case 266 num47）——
   *  贴图下垂出碰撞盒下缘（克脑主体在盒下半） */
  private drawBrainOfCthulhu(e: Enemy, world: World) {
    if (!this.atlas) return;
    const frames = Math.max(1, e.vanilla?.frames ?? 1);
    const frameIdx = vanillaFrameIdx(e, frames);
    const r = this.atlas.vnpc(266, frameIdx);
    if (!r) return;
    const ctx = this.ctx;
    // 专家档 ×1.05（Tweaks :18198；266 克脑专属曲径，通用路径不经过这里）
    const scale = (e.vanilla?.scale ?? 1) * e.vanillaScale * expertRenderScale(266);
    const yOff = 50 * scale;   // Main.cs:22950 num47 += 50*rCurrentNPC.scale
    const opacity = 1 - Math.min(255, Math.max(e.spawnAlpha, 0)) / 255; // NPC.Opacity
    const mirrored = e.facing > 0;   // 同通用路径朝向镜像（贴图默认朝左）
    // 四镜像幻影（Main.cs:24802-24841）
    const pl = this.mainPlayer;
    const ftw = !!world.seedFlags?.getGoodWorld;
    if (pl && e.hp < e.maxHp && (world.isExpert || ftw)) {
      let k = 1 - e.hp / e.maxHp;
---
548:const ROTATION_NPC = new Set([35, 68, 113, 114, 115, 116, 125, 126, 127, 128, 129, 130, 131, 134, 135, 136, 246, 247, 248, 249, 261, 262, 263, 264, 265, 370, 396, 397, 657]);
4348:        const rotId = ROTATION_NPC.has(e.vanillaId);
5662:   *  旋转 = AI 侧 spin（飞行 vx*0.1 钳 ±0.5，同通用 ROTATION_NPC 段）。

```


---

## 🤖 Assistant · 2026-08-19T09:01:15.618Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "limit": 60,
 "offset": 4300
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:01:15.624Z

**📎 ToolResult**

```
4300	      // 光之女皇 636（DrawNPCDirect_HallowBoss Main.cs:26364-26554）：翅膀/双臂/
4301	      // 二阶段覆层独占——通用路径只画本体，缺背后大翼与攻击态手臂帧
4302	      if (e.vanillaId === 636) { this.drawEmpress(e); return; }
4303	      // 402 星尘织带蠕虫（Main.cs:23848-23889 case 402 独占）：单 NPC 自绘
4304	      // oldPos 拖尾（403/404 节段 + Glow_133/134 加色）+ 头本体与 Glow_135
4305	      if (e.vanillaId === 402) { this.drawStardustWorm(e); return; }
4306	      // 266 克苏鲁之脑（Main.cs:24799-24843 专家/FTW 四镜像 + :22949-22951 Y 偏移）
4307	      if (e.vanillaId === 266) { this.drawBrainOfCthulhu(e, world); return; }
4308	      // 491 荷兰飞盗船（Main.cs:24263-24324 case 491 独占）：船体 OriginFlip(208,460) 锚 +
4309	      //  旗/桨/帆附加件叠绘 + 4 炮代画；492 炮 hide=true 由船代画（船在世时跳过独立绘制）
4310	      if (e.vanillaId === 491) { this.drawDutchman(e, entities); return; }
4311	      if (e.vanillaId === 492
4312	        && (entities as Enemy[]).some((n) => n instanceof Enemy && !n.dead && n.vanillaId === 491)) {
4313	        return;
4314	      }
4315	      const frames = Math.max(1, e.vanilla?.frames ?? 1);
4316	      const frameIdx = vanillaFrameIdx(e, frames);
4317	      // Mechdusa:毁灭者头 134 换画 136 尾帧贴图（Main.cs:24980-24984 num153=136
4318	      // + LoadNPC——头锁位倒挂(旋转 +π),头帧贴图方向不对,原版改用尾帧绘制）
4319	      // 石巨人:246 血尽原体变身自由态(ai3=1)后原版是 NewNPC 249——换画 NPC_249
4320	      // (帧 0/1 与 246 基础帧同构,customFrameIdx 直读不变;曾一直画 NPC_246)
4321	      const drawId = e.vanillaId === 134 && mechQueenUp() ? 136
4322	        : e.vanillaId === 246 && e.ai3 === 1 ? 249 : e.vanillaId;
4323	      const r = this.atlas.vnpc(drawId, frameIdx);
4324	      if (r) {
4325	        const flying = !!e.vanilla?.noGravity; void flying; // 中心锚后地面/飞行统一,仅保留语义注释
4326	        // 原版 NPC.scale（SetDefaults base × netID scale × 专家档体型系数）——作用于渲染。
4327	        // 专家系数（Tweaks :18187/:18198/:18300/:18309：世吞 13-15 ×1.2、克脑 266/
4328	        // 爬行者 267/毁灭者 134-136/探针 139 ×1.05）只乘 npc.scale 不回写宽高
4329	        // （NewNPC 的 width/height×scale 在 ScaleStats 之前，NPC.cs:17744-17747）——
4330	        // 碰撞盒保持 base 盒（本仓 e.w/e.h 已按 base 乘，勿在此扩盒）
4331	        const scale = (e.vanilla?.scale ?? 1) * e.vanillaScale
4332	          * expertRenderScale(e.vanillaId ?? 0);
4333	        ctx.save();
4334	        // 锚点:飞行型=帧中心(原版默认分支 Main.cs:23635 语义);地面型=底锚+原版恒
4335	        // +4 下沉(Main.cs:24741 通用公式:可见贴图底=盒底+4,帧底透明边距一并沉入
4336	        // 地面——原版脚部本就压住地表 ~2px;2026-08-17 前按透明行"贴地"补偿,
4337	        // 视觉上恒高 2-4px=悬空感的根因,全家族改 1:1)
4338	        const grounded = !flying;
4339	        // 416 日耀掠兽骑手（Main.cs:24508-24515 case 416 独占）：绘制位置吸附坐骑
4340	        // 415 的 Bottom（AI 锚 Center+(-spriteDir*10,-30) 只喂碰撞盒——骑手视觉上
4341	        // 双脚踩在掠兽脚平面，+4px 是帧底透明边距，与地面族 pad 同义）。
4342	        // 其余 aiStyle 75 骑手（390）原版无此绘制覆写，仍用 AI 位
4343	        const snapMount = e.vanillaId === 416 && e.master && !e.master.dead ? e.master : null;
4344	        ctx.translate(snapMount ? snapMount.cx : e.cx,
4345	          snapMount ? snapMount.y + snapMount.h : (grounded ? e.y + e.h : e.cy));
4346	        // 旋转族:整体随自转角旋转(原版 npc.rotation;朝向翻转不适用)。
4347	        // 4=克眼 visAngle;35/68=骷髅王头 spin;125/126=双子;127-131=Prime 头+部件;134-136=毁灭者链
4348	        const rotId = ROTATION_NPC.has(e.vanillaId);
4349	        // ★旋转驱动族总判定：朝向完全由 rotation 决定，原版这些家族不动 spriteDirection
4350	        // （默认 -1 从不镜像）——渲染层禁止对其叠加 facing 镜像，否则"屁股朝前"
4351	        // （噬魂怪 aiStyle5 实踩）。新增旋转族 AI 时必须登记在此，旋转与镜像共用本判定。
4352	        // 例外：AI_005 内的"仅倾斜"成员（黄蜂 42/231-235、孢子蝠 176/205、蜜蜂 210/211）
4353	        // 贴图横画、只 tilt 不转头——它们仍需镜像翻转朝向（原版同款 spriteDirection 翻转）。
4354	        // 23 陨石头/139 探针为"转头+镜像"复合成员（AI 侧 visAngle=atan2(sy,sx)+π、
4355	        // facing=sx 符号,cs:50962-51026）——留在 tiltOnly5 借用镜像通道,旋转走 visAngle。
4356	        const idR = e.vanillaId ?? -1;
4357	        const stR = e.vanilla?.aiStyle ?? 0;
4358	        const tiltOnly5 = stR === 5 && (idR === 23 || idR === 42 || idR === 139 || idR === 176 || idR === 205
4359	          || idR === 210 || idR === 211 || (idR >= 231 && idR <= 235));

```


---

## 🤖 Assistant · 2026-08-19T09:01:25.858Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The general NPC draw path at :4315-4323 uses `vanillaFrameIdx(e, frames)`, and duke 370 goes through this path (ROTATION_NPC at 4348 handles rotation). `vanillaFrameIdx` reads `e.customFrameIdx` first (line 646). So writing customFrameIdx from the duke AI is sufficient — no Renderer change needed. 

Let me now check the enemy's `frames` value for NPC 370 — vanilla frames for Duke: 8 (npcFrameCount). The wrap logic I implement uses f >= 6 → 0, frames 6/7 direct. Fine.

One important check: does `vanillaFrameIdx` have any existing case for id 370 that would conflict? customFrameIdx != null short-circuits at the top, so no conflict.

But wait — there might be an issue: `e.customFrameIdx` may be `null` initially; mimic694Frame starts from `this.customFrameIdx ?? 0`. Same for duke.

Now also check: is there a "frame 帧数闸门" — vanilla npcFrameCount for 370 in our data? Let me check public/sprites/vanilla-npcs.json for 370 frames = 8. Quick check.
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:01:29.728Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 -c \"\nimport json\nd = json.load(open('~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json'))\n# find entry for id 370\ndef find(o):\n    if isinstance(o, dict):\n        if str(o.get('id')) == '370' or o.get('vanillaId') == 370: return o\n        for v in o.values():\n            r = find(v)\n            if r: return r\n    elif isinstance(o, list):\n        for v in o:\n            r = find(v)\n            if r: return r\n    return None\nimport sys\ne = find(d)\nprint(json.dumps(e, ensure_ascii=False)[:400] if e else 'not-found-top')\n\" 2>/dev/null; grep -o '\"370\"[^}]*}' ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json | head -3",
 "description": "Check NPC 370 frame count in sprites json"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:01:29.799Z

**📎 ToolResult**

```
{"id": 370, "name": "Duke Fishron", "frames": 8, "lifeMax": 60000, "damage": 100, "defense": 50, "knockBackResist": 0, "aiStyle": 69, "width": 150, "height": 100, "npcSlots": 10, "noGravity": true, "noTileCollide": true, "HitSound": "NPCHit14", "DeathSound": "NPCDeath20"}
"370":{"id":370,"name":"Duke Fishron","frames":8,"lifeMax":60000,"damage":100,"defense":50,"knockBackResist":0,"aiStyle":69,"width":150,"height":100,"npcSlots":10,"noGravity":true,"noTileCollide":true,"HitSound":"NPCHit14","DeathSound":"NPCDeath20"}

```


---

## 🤖 Assistant · 2026-08-19T09:01:36.927Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
NPC 370 has 8 frames. All confirmed. Now let me implement all four changes.

### Edit 1: bossAI_lategame.ts — Empress expert table + case 11

First the table constants + header comment update.
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:01:37.630Z · glm-x-preview-260804

```
所有前置条件已确认。现在我来执行这四组修改，首先从 `bossAI_lategame.ts` 中的光女专家表和 case 11 开始。
```


---

## 🤖 Assistant · 2026-08-19T09:01:47.472Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts",
 "old_string": "// 经典弹幕伤害(:46326-46345): 919 墙 50 / 919 回环 70 / 873 45 / 872 45 / 923 50 / 874 40。\n// 选招表(:46460-46580 残差映射): 一阶段 10 拍 [2,8,6,8,5,2,8,4,8,5] 循环,血 ≤50% 强制 10(变身);\n//   二阶段 9 拍 [7,2,8,5,2,6,4,8,12] 循环——num37 槽位推进（flag2 时第 3 槽插 11=expert\n//   专属拍），表尾 num57=12（873 螺旋）;反编译的 num54 双写 [..,6,6,..] 是同一 if 重复,\n//   真表第 6 槽是 4、第 8 槽是 12。\nconst EMPRESS_CYCLE_P1 = [2, 8, 6, 8, 5, 2, 8, 4, 8, 5];\nconst EMPRESS_CYCLE_P2 = [7, 2, 8, 5, 2, 6, 4, 8, 12];",
 "new_string": "// 经典弹幕伤害(:46326-46345): 919 墙 50 / 919 回环 70 / 873 45 / 872 45 / 923 50 / 874 40。\n// 选招表(:46460-46580 残差映射): 一阶段 10 拍 [2,8,6,8,5,2,8,4,8,5] 循环,血 ≤50% 强制 10(变身);\n//   二阶段经典 9 拍 [7,2,8,5,2,6,4,8,12]——num37 槽位推进,flag2(expert/白天暴怒)时第 3 槽\n//   (num51,:46528)插 11 → 10 拍 expert 表 [7,2,8,11,5,2,6,4,8,12](含 case 11 预测光枪墙);\n//   表尾 num57=12(873 螺旋);反编译的 num54 双写 [..,6,6,..] 是同一 if 重复,\n//   真表第 6 槽是 4、第 8 槽是 12。\nconst EMPRESS_CYCLE_P1 = [2, 8, 6, 8, 5, 2, 8, 4, 8, 5];\nconst EMPRESS_CYCLE_P2 = [7, 2, 8, 5, 2, 6, 4, 8, 12];\nconst EMPRESS_CYCLE_P2_EXPERT = [7, 2, 8, 11, 5, 2, 6, 4, 8, 12];"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:01:47.491Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T09:01:56.021Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts",
 "old_string": "// 状态机(ai0): 0 出生(180t) / 1 悬浮蓄力枢纽(DashTo 靠近 10t + 减速,45t(二阶段 20t)选招)/\n//   2 彩虹射线 873 / 4 光枪墙 919 / 5 永恒彩虹 872 / 6 太阳舞 923 / 7 光枪回环 919(二阶段)/\n//   8,9 刀阵冲刺(±50 速,6-40t 无敌蓄力,40-90t 伤害 ×1.5)/ 10 半血变身传送 /\n//   13 淡出退场(目标失效/超 6400px)。3(874 天降极光)与 11/12 为 expert 专属拍,跳过。",
 "new_string": "// 状态机(ai0): 0 出生(180t) / 1 悬浮蓄力枢纽(DashTo 靠近 10t + 减速,45t(二阶段 20t)选招)/\n//   2 彩虹射线 873 / 4 光枪墙 919 / 5 永恒彩虹 872 / 6 太阳舞 923 / 7 光枪回环 919(二阶段)/\n//   8,9 刀阵冲刺(±50 速,6-40t 无敌蓄力,40-90t 伤害 ×1.5)/ 10 半血变身传送 /\n//   11 预测光枪墙 919(expert 表专属拍) / 12 螺旋射线 873 / 13 淡出退场(目标失效/超 6400px)。\n//   3(874 天降极光)为 expert 专属拍,跳过。"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:01:56.043Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T09:01:59.448Z · glm-x-preview-260804

```
现在处理 case 1 中的表格切换逻辑以及新的 case 11 代码块。
```


---

## 🤖 Assistant · 2026-08-19T09:02:01.042Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts",
 "old_string": "      const table = phase2 ? EMPRESS_CYCLE_P2 : EMPRESS_CYCLE_P1;",
 "new_string": "      // :46520-46579 二阶段表:flag2(expert/白天暴怒)时 num51 第 3 槽插 11 → 10 拍 expert 表\n      const table = phase2\n        ? (flag2 ? EMPRESS_CYCLE_P2_EXPERT : EMPRESS_CYCLE_P2)\n        : EMPRESS_CYCLE_P1;"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:02:01.060Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T09:02:19.519Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts",
 "old_string": "    // ---- 12 螺旋射线 873(:47152-47200,二阶段表尾拍,经典可达——num57→12 无专家门,\n    //      11 才是 expert 专属):起手 (0,-12) 上冲 + 0.95 阻尼;[10,60) 窗口内每 num22t\n    //      一发 873（速向 = (0,-20) 旋 2π·进度,弹 ai[1]=num23 螺旋相位） ----",
 "new_string": "    // ---- 11 预测光枪墙 919(:47061-47151,expert 二阶段表第 3 槽专属拍):悬玩家上\n    //      (0,-350),每 3t 在玩家速度反向 100px 处布一杆 919,瞄玩家 90t 预测位 ----\n    case 11: {\n      if (e.ai1 === 0) game.playSfxWav?.('Item_162', 1, e.cx, e.cy);   // :47065\n      const dur = 100 + (20 - num17);                                  // num58 = 20 - num17（:47067/:47144）\n      empressHover(e, player, 0, -350);                                // :47074-47079（vector3=(0,-350)/num3=40/num2=12/num=0.5）\n      // :47080 每 3t 一杆(num59=1)、<100t;:47089 NPC 距玩家 >2400 跳过当拍(continue,计时不断)\n      if (Math.floor(e.ai1) % 3 === 0 && e.ai1 < 100\n        && Math.hypot(player.cx - e.cx, player.cy - e.cy) <= 2400) {\n        // v = -玩家速度单位向量,零速兜底 (0,-1)（:47085-47086 SafeNormalize(-UnitY)）\n        let ux = -player.vx, uy = -player.vy;\n        const ul = Math.hypot(ux, uy);\n        if (ul > 0) { ux /= ul; uy /= ul; } else { ux = 0; uy = -1; }\n        // vector13 = 玩家 90t 预测位(num61=90,:47093-47094);vector14 = 玩家速度反向\n        // 100px 布枪点(num60=100,:47095)\n        const leadX = player.cx + player.vx * 90, leadY = player.cy + player.vy * 90;\n        let px = player.cx + ux * 100, py = player.cy + uy * 100;\n        // :47096-47104 布枪点距玩家 <100 时外推(v 已单位,防御性死代码 1:1)\n        if (Math.hypot(px - player.cx, py - player.cy) < 100) {\n          let ex = player.cx - px, ey = player.cy - py;\n          const el = Math.hypot(ex, ey);\n          if (el === 0) { ex = ux; ey = uy; } else { ex /= el; ey /= el; }\n          px = player.cx - ex * 100; py = player.cy - ey * 100;\n        }\n        // v2 = 预测位 − 布枪点 → 弹向（:47105-47108;919 收敛实现:12 速直飞,弹 ai1=\n        // ai1/100 延时参随收敛省略）;Boss_CanShootExtraAt 多人补射(:47114-47140)恒跳\n        // 主目标(:47324),单人无效,略\n        const ax = leadX - px, ay = leadY - py;\n        const al = Math.hypot(ax, ay) || 1;\n        shoot(game, px, py, (ax / al) * 12, (ay / al) * 12,\n          dayEnrage ? 9999 : phase2 ? 60 : 50, 919, 240);  // num6 :46332\n      }\n      e.ai1 += 1;\n      if (e.ai1 >= dur) { e.ai0 = 1; e.ai1 = 0; }\n      break;\n    }\n    // ---- 12 螺旋射线 873(:47152-47200,二阶段表尾拍,经典可达——num57→12 无专家门,\n    //      11 才是 expert 专属):起手 (0,-12) 上冲 + 0.95 阻尼;[10,60) 窗口内每 num22t\n    //      一发 873（速向 = (0,-20) 旋 2π·进度,弹 ai[1]=num23 螺旋相位） ----"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:02:19.537Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T09:02:41.262Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Group 1 done (table + case 11). Note the case 11 damage: num6 (919 wall damage) — `dayEnrage ? 9999 : phase2 ? 60 : 50` consistent with case 4's num6. Since case 11 only reachable in phase 2, phase2 will be true, but keeping the same expression as case 4 is the faithful pattern (num6 = 50 base, 60 in phase2).

Wait — one detail: in the expert table, case 11 fires while phase2 — the damage in vanilla is num6 which in phase 2 = 60, then GetAttackDamage_ForProjectiles(60, 35). Classic → 60. Expert → 35?? Hmm wait: num11 = 30 base / 35 in phase 2 (:46325-46341). So in expert phase2, damage = remap(60, 35) → expert → 35! Interesting — the expert damage is LOWER (35) than classic (60). That's the vanilla pattern (like the martian 50→37). But our current implementation for other cases (case 4, case 2, etc.) uses `phase2 ? 60 : 50` WITHOUT expert scaling — i.e., our port is classic-only main chain ("expert/大师分支只注释不实现" per file header). The task says for group 1: implement table switch + case 11 with "具体参数照抄" for the wall geometry; damage-wise follow our existing convergent pattern (same as case 4). Since the whole Empress AI is classic-damage (no getAttackDamageForProjectiles there), keeping `dayEnrage ? 9999 : phase2 ? 60 : 50` matches the file's established convention. The flag2 switch only affects pattern table + num17 (already implemented globally via num17). Good — that's consistent with how flag2 already affects case 2/4/6/7 (which are also reachable in expert via flag2 without expert damage scaling).

Hmm wait — but is that right? In expert mode the table would now include case 11, and the damage would use classic values (60). The task explicitly said the goal is the expert TABLE (选招表) and case 11 geometry, not expert damage tiers for the Empress. Fine — consistent.

Also `dur` for case 11: 100 + (20 - num17) — with flag2+phase2 num17=20 → 100. Classic-phase2 wouldn't reach case 11. OK.

Now Group 2: Duke FindFrame. Add the function + two call sites in bossAI_duke_moonlord.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:02:41.973Z · glm-x-preview-260804

```
第一组已完成。现在进行第二组——处理 `bossAI_duke_moonlord.ts` 中的猪鲨（Duke）FindFrame 状态机。
```


---

## 🤖 Assistant · 2026-08-19T09:02:59.356Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts",
 "old_string": "/** AI_069 主入口(经典模式) */",
 "new_string": "/** 猪鲨 FindFrame(NPC.cs FindFrame case 370 :72824-72917)——AI 侧每 tick 维护,\n *  帧号直写 customFrameIdx 供渲染端直读(694 先例;npcFrameT = frameCounter)。\n *  帧 0-5 = 游动帶(6t/帧,二阶段悬浮 5t/帧)、6/7 = 张口帶;8 帧贴图:\n *  - ai0 0/5 悬浮:游动循环,ai0==5 步进加速(num51 5→4,:72828-72832);\n *  - ai0 1/6 冲撞与 2/7 旋转冲刺:ai2<10 帧 6,≥10 帧 7(:72844-72865);\n *  - ai0 3/8 龙卷蓄力与 -1 出生(num52=90):ai2<60 或 >80 游动,否则帧 6\n *    (ai2∈(70,75) 帧 7)(:72866-72889);\n *  - ai0 4/9 变身(num53=180):ai2<120 或 >160 游动,否则帧 6(ai2∈(130,155) 帧 7)\n *    (:72891-72916);\n *  - ai0 10-13(expert 狂暴段)原版无分支 → 帧保持不变。\n *  游动帶回卷门 `frame.Y >= 6 → 0` 每 tick 生效(:72839-72842)——张口帧 6/7 收\n *  尾回到悬浮帶时首 tick 即回卷到帧 0,与原版一致。 */\nfunction dukeFindFrame(e: Enemy): void {\n  const a0 = Math.floor(e.ai0);\n  let f = e.customFrameIdx ?? 0;\n  /** 游动帶步进(threshold=num51:counter 先 +1 再比 >num51 → 5=6t/帧、4=5t/帧) */\n  const swim = (threshold: number): void => {\n    e.npcFrameT += 1;\n    if (e.npcFrameT > threshold) { e.npcFrameT = 0; f += 1; }\n    if (f >= 6) f = 0;                                     // :72839-72842 回卷\n  };\n  if (a0 === 0 || a0 === 5) {\n    swim(a0 === 5 ? 4 : 5);                                // :72826-72843\n  } else if (a0 === 1 || a0 === 6 || a0 === 2 || a0 === 7) {\n    f = e.ai2 < 10 ? 6 : 7;                                // :72844-72865\n  } else if (a0 === 3 || a0 === 8 || a0 === -1) {\n    if (e.ai2 < 60 || e.ai2 > 80) swim(5);                 // num52=90-30/90-10 :72868-72881\n    else {                                                  // :72882-72889 计时窗张口\n      f = 6;\n      if (e.ai2 > 70 && e.ai2 < 75) f = 7;\n    }\n  } else if (a0 === 4 || a0 === 9) {\n    if (e.ai2 < 120 || e.ai2 > 160) swim(5);               // num53=180-60/180-20 :72895-72908\n    else {                                                  // :72909-72916 变身窗张口\n      f = 6;\n      if (e.ai2 > 130 && e.ai2 < 155) f = 7;\n    }\n  }\n  e.customFrameIdx = f;\n}\n\n/** AI_069 主入口(经典模式) */"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:02:59.376Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts has been updated successfully. (note: the file had been modified on disk since you last read it — the edit applied cleanly, but the file contains other changes not in your context. Read it before edits that depend on surrounding content.)

```


---

## 🤖 Assistant · 2026-08-19T09:03:02.474Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The file was modified on disk since I read it (parallel session?). I need to re-read before making the call-site edits, which depend on the surrounding content (the despawn branch and end of dukeFishronAI). Let me read the relevant region again.
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:03:03.104Z · glm-x-preview-260804

```
文件在磁盘上已被并发修改——在触及调用点（call sites）之前，我先重新读取一下 AI body。
```


---

## 🤖 Assistant · 2026-08-19T09:03:03.690Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts",
 "limit": 80,
 "offset": 262
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:03:03.706Z

**📎 ToolResult**

```
262	export function dukeFishronAI(e: Enemy, game: GameHooks, player: Player | null) {
263	  const st = dukeOf(e);
264	  if (!e.bInit) { e.bInit = true; e.ai0 = -1; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; e.spawnAlpha = 255; } // :49247-49257
265	  const b = baseOf(e);
266	  const enraged = player ? dukeEnraged(game, player) : false;
267	  const flag = e.hp <= e.maxHp * 0.5;                       // flag  :49147 二阶段
268	  const flag3 = e.ai0 > 4;                                  // flag3 :49149(二阶段状态 5-13)
269	  const flag4 = e.ai0 > 9;                                  // flag4 :49150(expert 狂暴段 10-13)
270	  const flag5 = e.ai3 < (flag3 ? 3 : 5) * 2;                // flag5 :49151-49152
271	
272	  // 伤害/防御修正(:49153-49167 + 狂暴 :49239-49245)——每 tick 从基值派生
273	  if (flag4) { e.def.damage = Math.round(b.dmg * 1.1); e.def.defense = 0; }
274	  else if (flag3) { e.def.damage = Math.round(b.dmg * 1.2); e.def.defense = Math.round(b.def * 0.8); }
275	  else { e.def.damage = b.dmg; e.def.defense = b.def; }
276	  if (enraged) { e.def.damage = b.dmg * 2; e.def.defense = b.def * 2; }
277	
278	  // 悬浮/冲撞参数(:49168-49201;expert 档注释)
279	  let hoverT = DUKE.hoverT, hoverAcc = DUKE.hoverAcc, hoverSpd = DUKE.hoverSpd;
280	  if (flag4) { hoverAcc = 0.7; hoverSpd = 12; hoverT = 30; }            // :49171-49176
281	  else if (flag3 && flag5) { hoverAcc = 0.5; hoverSpd = 8; hoverT = 20; } // :49177-49182
282	  else if (flag5 && !flag3 && !flag4) hoverT = 30;                       // :49183-49186
283	  let chargeT = DUKE.chargeT, chargeSpd = DUKE.chargeSpd;
284	  if (flag4) { chargeT = 25; chargeSpd = 27; }                           // :49189-49193(expert 同档)
285	  if (enraged) { hoverT = 10; chargeSpd += 6; }                          // :49239-49245
286	
287	  // 玩家死/远离 5600px(:49218-49237):减速升空离场(原版另 EncourageDespawn(10);
288	  // 本工程 Boss 不参与 despawn 块,故仅保留升空)。原版此处无回血逻辑。
289	  if (!player || player.dead || Math.hypot(player.cx - e.cx, player.cy - e.cy) > 5600) {
290	    e.vy -= 0.4;
291	    e.encourageDespawn(10); // :49234 急升逃离 + EncourageDespawn(10)
292	    e.ai0 = e.ai0 > 4 ? 5 : 0;
293	    e.ai2 = 0;
294	    e.x += e.vx; e.y += e.vy;
295	    return;
296	  }
297	
298	  // ---- 身体旋转朝向(:49258-49345)----
299	  let target = Math.atan2(player.cy - e.cy, player.cx - e.cx);
300	  if (st.spr === 1) target += Math.PI;
301	  if (target < 0) target += TAU; else if (target > TAU) target -= TAU;
302	  if (e.ai0 === -1 || e.ai0 === 3 || e.ai0 === 4 || e.ai0 === 8) target = 0; // :49271-49286
303	  let step = 0.04;                                                            // num23 :49287
304	  if (e.ai0 === 1 || e.ai0 === 6 || e.ai0 === 7) step = 0;                    // :49288-49295
305	  if (e.ai0 === 3 || e.ai0 === 4 || e.ai0 === 8) step = 0.01;                 // :49296-49307
306	  let rot = e.spin;
307	  if (rot < target) rot += (target - rot > Math.PI ? -step : step);
308	  if (rot > target) rot += (rot - target > Math.PI ? step : -step);
309	  if (rot > target - step && rot < target + step) rot = target;
310	  if (rot < 0) rot += TAU; else if (rot > TAU) rot -= TAU;
311	  if (rot > target - step && rot < target + step) rot = target;
312	  e.spin = rot;
313	
314	  // ---- 透明度(:49346-49363;近似为 spawnAlpha 渐变)----
315	  // 入实心块 +15/出块 −15,钳 [0,150](★上限 150 非 255——入块半隐,2026-08-19 台账 E 修)
316	  if (e.ai0 !== -1 && e.ai0 < 9) e.spawnAlpha = inSolid(game, e) ? Math.min(150, e.spawnAlpha + 15) : Math.max(0, e.spawnAlpha - 15);
317	
318	  let invuln = false; // flag7(dontTakeDamage = !flag7,:50126)
319	  switch (e.ai0) {
320	    case -1: { // 出生(:49365-49414)
321	      invuln = true;
322	      e.vx *= 0.98; e.vy *= 0.98;
323	      const s = Math.sign(player.cx - e.cx) || st.dir;
324	      st.dir = s; st.spr = -s;
325	      if (e.ai2 > 20) {
326	        e.vy = -2;
327	        e.spawnAlpha = clamp(e.spawnAlpha - 5 + (inSolid(game, e) ? 15 : 0), 0, 150); // :49375-49391
328	      } else if (e.spawnAlpha < 255) e.spawnAlpha = 255;
329	      if (e.ai2 === DUKE.nadoT - 30) { // :49392 出生尘环
330	        game.spawnParticles(e.cx, e.cy, '#8FD8FF', 18, 2.4, { life: 40 });
331	        game.playSfxWav?.('Zombie_20', 1, e.cx, e.cy);   // :49404 PlaySound(29,…,20) 满响(曾借 roar 0.8)
332	      }
333	      e.ai2 += 1;
334	      if (e.ai2 >= DUKE.spawnT) { e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; }
335	      break;
336	    }
337	    case 0: { // 一阶段悬浮(:49415-49543)
338	      if (player.dead) break;
339	      dukeHover(e, player, hoverAcc, hoverSpd, 300, st);
340	      e.ai2 += 1;
341	      if (e.ai2 >= hoverT) {

```


---

## 🤖 Assistant · 2026-08-19T09:03:08.952Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The AI body is unchanged (only whitespace/parallel changes elsewhere). Now add the two dukeFindFrame call sites:
1. In the despawn early-return branch (before `return;` at line 295).
2. At the end of dukeFishronAI after `e.x += e.vx; e.y += e.vy;` (line ~531).
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:03:14.076Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts",
 "old_string": "  if (!player || player.dead || Math.hypot(player.cx - e.cx, player.cy - e.cy) > 5600) {\n    e.vy -= 0.4;\n    e.encourageDespawn(10); // :49234 急升逃离 + EncourageDespawn(10)\n    e.ai0 = e.ai0 > 4 ? 5 : 0;\n    e.ai2 = 0;\n    e.x += e.vx; e.y += e.vy;\n    return;\n  }",
 "new_string": "  if (!player || player.dead || Math.hypot(player.cx - e.cx, player.cy - e.cy) > 5600) {\n    e.vy -= 0.4;\n    e.encourageDespawn(10); // :49234 急升逃离 + EncourageDespawn(10)\n    e.ai0 = e.ai0 > 4 ? 5 : 0;\n    e.ai2 = 0;\n    e.x += e.vx; e.y += e.vy;\n    dukeFindFrame(e); // FindFrame 在 AI 之后仍逐 tick 执行(原版 UpdateNPC 时序)\n    return;\n  }"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:03:14.097Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T09:03:19.251Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts",
 "old_string": "  if (invuln) e.iframes = 2;\n  e.facing = st.spr;\n  e.x += e.vx;\n  e.y += e.vy;\n}",
 "new_string": "  if (invuln) e.iframes = 2;\n  e.facing = st.spr;\n  e.x += e.vx;\n  e.y += e.vy;\n  dukeFindFrame(e); // FindFrame case 370(:72824-72917)——AI 后逐 tick,customFrameIdx 直读\n}"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:03:19.263Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T09:03:25.786Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Wait — that `old_string` might not be unique (the pattern `if (invuln) e.iframes = 2; e.facing = st.spr; ...` — dukeFishronAI ends with that; the edit succeeded so it was unique. Good.)

But wait, I should double check there isn't another function ending with the same lines (e.g., the dukeBubbleAI or moonlord sections). The Edit succeeded without a uniqueness error, so it's fine.

Now Group 3: Game.ts WoF misc[32]. Re-read the WoF block first (Game.ts may have been modified by parallel sessions too — the CLAUDE.md warns "并行会话改 Game.ts 须重 grep 再 Edit").
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:03:26.974Z · glm-x-preview-260804

```
第 2 组已完成。现在进行第 3 组 —— 处理 `Game.ts` 中的 `WoF` 死亡 `misc[32]`。根据并行会话约定，先重新 grep 代码块。
```


---

## 🤖 Assistant · 2026-08-19T09:03:28.251Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"createBrickBoxForWallOfFlesh\\|startHardmode(w)\\|Lang.misc(15)\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | head",
 "description": "Re-locate WoF death chain in Game.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:03:28.303Z

**📎 ToolResult**

```
287:import { createBrickBoxForWallOfFlesh, startHardmode } from '../world/gen/vanilla/HardmodePass';
4580:            createBrickBoxForWallOfFlesh(w.store, Math.trunc(wof.cx / 16), Math.trunc(wof.cy / 16), wof.w, w.crimson);
4581:            const { wasHard } = startHardmode(w);
4584:            this.newText(Lang.misc(15), 50, 255, 130);

```


---

## 🤖 Assistant · 2026-08-19T09:03:32.313Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 16,
 "offset": 4574
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:03:32.327Z

**📎 ToolResult**

```
4574	          if (this.boss.vanillaId === 262 && this.wiring) this.wiring.planteraDowned = true;
4575	          // 肉山：困难模式世界变换全链（NPC.cs:80281-80292 原序：砖盒 → 捕获旧
4576	          // hardMode → StartHardmode(置位+V 带转化+洞穴墙回填) → 灯笼夜 19(仅首次)
4577	          // → misc[15] 公告 + 成就 9(随本链迁移,2026-08-13 之前击杀即发的旧点已删))
4578	          if (this.boss.vanillaId === 113) {
4579	            const wof = this.boss;
4580	            createBrickBoxForWallOfFlesh(w.store, Math.trunc(wof.cx / 16), Math.trunc(wof.cy / 16), wof.w, w.crimson);
4581	            const { wasHard } = startHardmode(w);
4582	            this.recLog('world', { ev: 'hardmode', on: w.flags.hardMode });   // 行为录制：困难模式置位（肉山首杀）
4583	            if (!wasHard) LanternNight.onGameEventCleared(19);
4584	            this.newText(Lang.misc(15), 50, 255, 130);
4585	            this.achievements.notifyProgressionEvent(9);
4586	          }
4587	          // 首胜灯笼夜预约（NPC.cs NPCLoot 各 case SetEventFlagCleared 实参 →
4588	          // OnGameEventClearedForTheFirstTime default/10/16-18 翻转；4/21/22 排除）。
4589	          // id 表：11 史王 8 蜂后 13 EoC 14 世吞|克脑 15 骷髅王 19 肉山 12 世纪之花

```


---

## 🤖 Assistant · 2026-08-19T09:03:36.333Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The file was reformatted/reviewed by a linter or parallel session — the truncated diff shows my changes are likely still there (the header was reorganized with sections). Let me verify my dukeFindFrame function and call sites survived.
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:03:37.182Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"dukeFindFrame\" ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts",
 "description": "Verify dukeFindFrame survived the parallel edit"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:03:37.220Z

**📎 ToolResult**

```
232:function dukeFindFrame(e: Enemy): void {
295:    dukeFindFrame(e); // FindFrame 在 AI 之后仍逐 tick 执行(原版 UpdateNPC 时序)
532:  dukeFindFrame(e); // FindFrame case 370(:72824-72917)——AI 后逐 tick,customFrameIdx 直读

```


---

## 🤖 Assistant · 2026-08-19T09:03:42.948Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
My duke changes survived. Now group 3: Game.ts WoF misc[32]. Insert after startHardmode, before LanternNight (matching vanilla order misc[32] → SetEventFlagCleared(19)).
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:03:43.484Z · glm-x-preview-260804

```
Duke 相关的修改已整合。现在进行第三组 —— `Game.ts`。
```


---

## 🤖 Assistant · 2026-08-19T09:03:52.204Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "old_string": "          if (this.boss.vanillaId === 113) {\n            const wof = this.boss;\n            createBrickBoxForWallOfFlesh(w.store, Math.trunc(wof.cx / 16), Math.trunc(wof.cy / 16), wof.w, w.crimson);\n            const { wasHard } = startHardmode(w);\n            this.recLog('world', { ev: 'hardmode', on: w.flags.hardMode });   // 行为录制：困难模式置位（肉山首杀）\n            if (!wasHard) LanternNight.onGameEventCleared(19);\n            this.newText(Lang.misc(15), 50, 255, 130);\n            this.achievements.notifyProgressionEvent(9);\n          }",
 "new_string": "          if (this.boss.vanillaId === 113) {\n            const wof = this.boss;\n            createBrickBoxForWallOfFlesh(w.store, Math.trunc(wof.cx / 16), Math.trunc(wof.cy / 16), wof.w, w.crimson);\n            const { wasHard } = startHardmode(w);\n            this.recLog('world', { ev: 'hardmode', on: w.flags.hardMode });   // 行为录制：困难模式置位（肉山首杀）\n            // drunk/FTW 边缘（NPC.cs:80287-80290）：三机械旗全齐（机械 Boss 先于\n            // 肉山被杀,本仓键 downed_134/125/127 = downedMechBoss1/2/3）且杀前\n            // 非困难模式（!eventFlag,wasHard 为 StartHardmode 前快照）→ 三旗齐\n            // misc[32] \"丛林变得焦躁不安\"公告（与 :79670-79673 机械链同一文案）;\n            // 原版序在本条 SetEventFlagCleared(19) 之前 → 置于灯笼夜/misc[15] 前\n            if (!wasHard && w.flags['downed_134'] && w.flags['downed_125'] && w.flags['downed_127']) {\n              this.newText(Lang.misc(32), 50, 255, 130);\n            }\n            if (!wasHard) LanternNight.onGameEventCleared(19);\n            this.newText(Lang.misc(15), 50, 255, 130);\n            this.achievements.notifyProgressionEvent(9);\n          }"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:03:52.249Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/core/Game.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T09:03:57.662Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Also update the comment above the block (line 4575-4577) mentioning the chain order? The comment says "NPC.cs:80281-80292 原序:砖盒 → 捕获旧 hardMode → StartHardmode(置位+V 带转化+洞穴墙回填) → 灯笼夜 19(仅首次) → misc[15] 公告 + 成就 9" — it's now missing the misc[32] step. Let me update it for accuracy.
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:04:01.797Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "old_string": "          // 肉山：困难模式世界变换全链（NPC.cs:80281-80292 原序：砖盒 → 捕获旧\n          // hardMode → StartHardmode(置位+V 带转化+洞穴墙回填) → 灯笼夜 19(仅首次)\n          // → misc[15] 公告 + 成就 9(随本链迁移,2026-08-13 之前击杀即发的旧点已删))",
 "new_string": "          // 肉山：困难模式世界变换全链（NPC.cs:80281-80292 原序：砖盒 → 捕获旧\n          // hardMode → StartHardmode(置位+V 带转化+洞穴墙回填) → 三机械齐 misc[32]\n          // (仅 !wasHard 时) → 灯笼夜 19(仅首次) → misc[15] 公告 + 成就 9(随本链迁移,\n          // 2026-08-13 之前击杀即发的旧点已删))"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:04:01.830Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/core/Game.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T09:04:04.775Z · glm-x-preview-260804

```
现在开始第四组 — 处理 `bossAI_martian.ts` 中的火星专家弹幕伤害插值。
```


---

## 🤖 Assistant · 2026-08-19T09:04:06.017Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts",
 "old_string": "import { spawnPart, losClear } from './bossAI';\nimport { Arrow } from './Arrow';",
 "new_string": "import { spawnPart, losClear } from './bossAI';\nimport { getAttackDamageForProjectiles } from '../stats/ScaleStats';\nimport { Arrow } from './Arrow';"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:04:06.035Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T09:04:13.593Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts",
 "old_string": "      if (n % 20 === 0) {\n        const dirx = spriteDir;\n        const delta = (Math.random() - 0.5) * 0.7853982;   // ±22.5° 散布（:36133-36136）\n        shootM(game, e.cx + dirx * 36, e.cy + 8,\n          Math.cos(delta) * 8 * dirx, Math.sin(delta) * 8 * dirx, 50, 448, 3600, 1,\n          { martianRocket: true });\n        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36098 火炮每发(终审补)\n      }",
 "new_string": "      if (n % 20 === 0) {\n        const dirx = spriteDir;\n        const delta = (Math.random() - 0.5) * 0.7853982;   // ±22.5° 散布（:36133-36136）\n        // :36081 伤 = GetAttackDamage_ForProjectiles(50, 37)——expert 插值档\n        shootM(game, e.cx + dirx * 36, e.cy + 8,\n          Math.cos(delta) * 8 * dirx, Math.sin(delta) * 8 * dirx,\n          getAttackDamageForProjectiles(50, 37, e.difficulty), 448, 3600, 1,\n          { martianRocket: true });\n        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36098 火炮每发(终审补)\n      }"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:04:13.617Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T09:04:19.705Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts",
 "old_string": "      if (n % 6 === 0) {\n        const ang = e.ai2 + (Math.random() - 0.5) * (0.7853982 / 3);\n        shootM(game, e.cx, e.cy, Math.cos(ang) * 16, Math.sin(ang) * 16, 35, 449);\n        game.playSfxFiles?.(['Item_12'], 1, e.cx, e.cy);     // :36140 部件激光(392 段 Item12)\n      }",
 "new_string": "      if (n % 6 === 0) {\n        const ang = e.ai2 + (Math.random() - 0.5) * (0.7853982 / 3);\n        // :36105 伤 = GetAttackDamage_ForProjectiles(35, 30)——expert 插值档\n        shootM(game, e.cx, e.cy, Math.cos(ang) * 16, Math.sin(ang) * 16,\n          getAttackDamageForProjectiles(35, 30, e.difficulty), 449);\n        game.playSfxFiles?.(['Item_12'], 1, e.cx, e.cy);     // :36140 部件激光(392 段 Item12)\n      }"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:04:19.726Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T09:04:30.209Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now the four 450 sites. They share similar text; let me edit each with enough context to be unique. The four blocks:

1. t0Dead block: `const mvx = -Math.random() * 3 * 3, mvy = 1 * 3;` + shootM with rndRange(50, 70), rndRange(30, 45), 30, 450
2. t1Dead block: `const mvx = Math.random() * 3 * 3, mvy = 1 * 3;` + rndRange(50, 70), rndRange(30, 45)
3. c0Dead block: `const mvx = -Math.random() * 3 * 3, mvy = -1 * 3;` + rndRange(30, 60), rndRange(-30, -10)
4. c1Dead block: `const mvx = Math.random() * 3 * 3, mvy = -1 * 3;` + rndRange(30, 60), rndRange(-30, -10)

Blocks 1&2 differ by mvx sign; 3&4 likewise. So each block's full text (comment + mvx line + shootM) is unique. Let me define a helper first to avoid repeating? The task says wrap with getAttackDamageForProjectiles at each call site ("各调用点 dmg 参数换算"). A local const computed once before the block would also be faithful (vanilla computes attackDamage_ForProjectiles12 once at :36169 before the window). Actually vanilla computes it once per AI tick before the empty-nest launcher block. I'll follow vanilla: compute `const dmg450 = getAttackDamageForProjectiles(30, 25, e.difficulty);` once before the `flag76` checks — mirroring :36169 placement. Let me place it right before `let flag76 = false...`.
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:04:58.416Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts",
 "old_string": "    let flag76 = false, mv4 = 1000, mv5 = 1000;\n    if (saucer.ai0 === 2) { flag76 = true; mv4 = 120; mv5 = 120; }\n    if (!flag76 && e.ai3 >= 280 && e.ai3 < 400) { flag76 = true; mv5 = 90; mv4 = 60; }\n    if (!flag76 && e.ai3 >= 440 && e.ai3 < 580) { flag76 = true; mv5 = 60; mv4 = 90; }\n    if (flag76) {\n      // 炮塔空巢（:36243-36258）:下方侧向抛射\n      if (t0Dead && rnd(mv4) === 0) {\n        // :36246-36250 速度 = (±rand3, ±1)×3 未归一(3~9.5 随机,曾归一恒 3)\n        const mvx = -Math.random() * 3 * 3, mvy = 1 * 3;\n        shootM(game, e.cx + rndRange(50, 70), e.cy + rndRange(30, 45), mvx, mvy, 30, 450, 300, 1,\n          { bounce: true });  // aiStyle14 X 反跳(原版 ×-0.1,默认档 -0.5 近似)\n        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36254 空巢导弹每发(终审补)\n      }\n      if (t1Dead && rnd(mv4) === 0) {\n        // :36246-36250 速度 = (±rand3, ±1)×3 未归一(3~9.5 随机,曾归一恒 3)\n        const mvx = Math.random() * 3 * 3, mvy = 1 * 3;\n        shootM(game, e.cx + rndRange(50, 70), e.cy + rndRange(30, 45), mvx, mvy, 30, 450, 300, 1,\n          { bounce: true });  // aiStyle14 X 反跳(原版 ×-0.1,默认档 -0.5 近似)\n        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36254 空巢导弹每发(终审补)\n      }\n      // 火炮空巢（:36261-36276）:上方侧向抛射\n      if (c0Dead && rnd(mv5) === 0) {\n        // :36246-36250 速度 = (±rand3, ±1)×3 未归一(3~9.5 随机,曾归一恒 3)\n        const mvx = -Math.random() * 3 * 3, mvy = -1 * 3;\n        shootM(game, e.cx + rndRange(30, 60), e.cy + rndRange(-30, -10), mvx, mvy, 30, 450, 300, 1,\n          { bounce: true });  // aiStyle14 X 反跳(原版 ×-0.1,默认档 -0.5 近似)\n        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36254 空巢导弹每发(终审补)\n      }\n      if (c1Dead && rnd(mv5) === 0) {\n        // :36246-36250 速度 = (±rand3, ±1)×3 未归一(3~9.5 随机,曾归一恒 3)\n        const mvx = Math.random() * 3 * 3, mvy = -1 * 3;\n        shootM(game, e.cx + rndRange(30, 60), e.cy + rndRange(-30, -10), mvx, mvy, 30, 450, 300, 1,\n          { bounce: true });  // aiStyle14 X 反跳(原版 ×-0.1,默认档 -0.5 近似)\n        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36254 空巢导弹每发(终审补)\n      }\n    }",
 "new_string": "    let flag76 = false, mv4 = 1000, mv5 = 1000;\n    if (saucer.ai0 === 2) { flag76 = true; mv4 = 120; mv5 = 120; }\n    if (!flag76 && e.ai3 >= 280 && e.ai3 < 400) { flag76 = true; mv5 = 90; mv4 = 60; }\n    if (!flag76 && e.ai3 >= 440 && e.ai3 < 580) { flag76 = true; mv5 = 60; mv4 = 90; }\n    // :36168-36169 空巢导弹 450 伤 = GetAttackDamage_ForProjectiles(30, 25)——\n    // expert 插值档,窗检前一次算定(四处发射共用)\n    const dmg450 = getAttackDamageForProjectiles(30, 25, e.difficulty);\n    if (flag76) {\n      // 炮塔空巢（:36243-36258）:下方侧向抛射\n      if (t0Dead && rnd(mv4) === 0) {\n        // :36246-36250 速度 = (±rand3, ±1)×3 未归一(3~9.5 随机,曾归一恒 3)\n        const mvx = -Math.random() * 3 * 3, mvy = 1 * 3;\n        shootM(game, e.cx + rndRange(50, 70), e.cy + rndRange(30, 45), mvx, mvy, dmg450, 450, 300, 1,\n          { bounce: true });  // aiStyle14 X 反跳(原版 ×-0.1,默认档 -0.5 近似)\n        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36254 空巢导弹每发(终审补)\n      }\n      if (t1Dead && rnd(mv4) === 0) {\n        // :36246-36250 速度 = (±rand3, ±1)×3 未归一(3~9.5 随机,曾归一恒 3)\n        const mvx = Math.random() * 3 * 3, mvy = 1 * 3;\n        shootM(game, e.cx + rndRange(50, 70), e.cy + rndRange(30, 45), mvx, mvy, dmg450, 450, 300, 1,\n          { bounce: true });  // aiStyle14 X 反跳(原版 ×-0.1,默认档 -0.5 近似)\n        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36254 空巢导弹每发(终审补)\n      }\n      // 火炮空巢（:36261-36276）:上方侧向抛射\n      if (c0Dead && rnd(mv5) === 0) {\n        // :36246-36250 速度 = (±rand3, ±1)×3 未归一(3~9.5 随机,曾归一恒 3)\n        const mvx = -Math.random() * 3 * 3, mvy = -1 * 3;\n        shootM(game, e.cx + rndRange(30, 60), e.cy + rndRange(-30, -10), mvx, mvy, dmg450, 450, 300, 1,\n          { bounce: true });  // aiStyle14 X 反跳(原版 ×-0.1,默认档 -0.5 近似)\n        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36254 空巢导弹每发(终审补)\n      }\n      if (c1Dead && rnd(mv5) === 0) {\n        // :36246-36250 速度 = (±rand3, ±1)×3 未归一(3~9.5 随机,曾归一恒 3)\n        const mvx = Math.random() * 3 * 3, mvy = -1 * 3;\n        shootM(game, e.cx + rndRange(30, 60), e.cy + rndRange(-30, -10), mvx, mvy, dmg450, 450, 300, 1,\n          { bounce: true });  // aiStyle14 X 反跳(原版 ×-0.1,默认档 -0.5 近似)\n        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36254 空巢导弹每发(终审补)\n      }\n    }"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:04:58.438Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T09:05:00.881Z · glm-x-preview-260804

```
现在我来处理特斯拉炮塔 435 站点。
```


---

## 🤖 Assistant · 2026-08-19T09:05:04.706Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts",
 "old_string": "    if (d > 0.001) { dx = (dx / d) * 14; dy = (dy / d) * 14; }\n    else { dx = 0; dy = -14; }\n    shootM(game, ox, oy, dx, dy, 35, 435);",
 "new_string": "    if (d > 0.001) { dx = (dx / d) * 14; dy = (dy / d) * 14; }\n    else { dx = 0; dy = -14; }\n    // :35442-35448 伤 = GetAttackDamage_ForProjectiles(35, 35×0.8)——type 387 ∈\n    // [381,392] → num1090=0.8 → expert 档 28\n    shootM(game, ox, oy, dx, dy, getAttackDamageForProjectiles(35, 28, e.difficulty), 435);"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:05:04.724Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T09:05:12.795Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Also update the file header comment for the tesla turret section (line 695: "放电 435(伤 35,速 14,±100px 抖动)") — keep as is; it describes classic values. Fine.

Now — check the martian file for whether the "e" in teslaTurretAI and martianSaucerPartAI is the Enemy with difficulty. Yes, both are Enemy.

Now run tsc and the tests. But first — quick sanity check of the case 11 code I added to bossAI_lategame.ts. One thing to verify: in case 1, the table edit — make sure `phase2`/`flag2` are in scope there (yes, defined at function top). Also the case 11 block — verify the switch allows case 11 (it's inside the same switch). Let me view the edited region to double-check syntax.
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:05:13.612Z · glm-x-preview-260804

```
四个小组的代码修改已完成。让我来验证一下修改区域的语法，然后运行类型检查和测试。
```


---

## 🤖 Assistant · 2026-08-19T09:05:15.026Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1096,1112p' ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts; echo '...'; sed -n '1286,1330p' ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts",
 "description": "Review edited Empress table switch and case 11 block"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:05:15.060Z

**📎 ToolResult**

```
      let dur = phase2 ? 20 : 45;
      if (game.world.seedFlags?.getGoodWorld) dur /= 2;
      if (e.ai1 <= 10) empressDashTo(e, player.cx, player.cy);
      if (Math.hypot(e.vx, e.vy) > 16 && e.ai1 > 10) { e.vx /= 2; e.vy /= 2; }
      e.vx *= 0.92; e.vy *= 0.92;
      e.ai1 += 1;
      if (e.ai1 < dur) break;
      // :46520-46579 二阶段表:flag2(expert/白天暴怒)时 num51 第 3 槽插 11 → 10 拍 expert 表
      const table = phase2
        ? (flag2 ? EMPRESS_CYCLE_P2_EXPERT : EMPRESS_CYCLE_P2)
        : EMPRESS_CYCLE_P1;
      let next = table[Math.floor(e.ai2) % table.length];
      if (!phase2 && e.hp / e.maxHp <= 0.5) next = 10; // :46463 半血强制变身
      if (next === 8 && player.cx > e.cx) next = 9;     // :46493 冲刺方向
      // :46603-46606 flag2（expert/暴怒）且选招非 5/12：起手朝玩家向量旋 ±90° × 20 速
      if (flag2 && next !== 5 && next !== 12) {
        const side = (player.cx > e.cx ? 1 : -1);       // ToDirectionInt(目标在右)
...
        if (e.ai3 === 0) e.ai3 = 1; // :47040-47043
        if (e.ai3 === 2) e.ai3 = 3; // :47044-47047 白天暴怒档同步进二阶段(3=暴怒+二阶段)
        e.x = player.cx - e.w / 2;
        e.y = player.cy - 250 - e.h / 2;
        // 原版此传送为纯 position 改写（:47039-47052）：无 dust 无传送音——
        // 曾错加 roar+黄尘（已移除对齐）
      }
      e.ai1 += 1;
      if (e.ai1 >= 180 + (20 - num17)) { e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; }
      break;
    }
    // ---- 11 预测光枪墙 919(:47061-47151,expert 二阶段表第 3 槽专属拍):悬玩家上
    //      (0,-350),每 3t 在玩家速度反向 100px 处布一杆 919,瞄玩家 90t 预测位 ----
    case 11: {
      if (e.ai1 === 0) game.playSfxWav?.('Item_162', 1, e.cx, e.cy);   // :47065
      const dur = 100 + (20 - num17);                                  // num58 = 20 - num17（:47067/:47144）
      empressHover(e, player, 0, -350);                                // :47074-47079（vector3=(0,-350)/num3=40/num2=12/num=0.5）
      // :47080 每 3t 一杆(num59=1)、<100t;:47089 NPC 距玩家 >2400 跳过当拍(continue,计时不断)
      if (Math.floor(e.ai1) % 3 === 0 && e.ai1 < 100
        && Math.hypot(player.cx - e.cx, player.cy - e.cy) <= 2400) {
        // v = -玩家速度单位向量,零速兜底 (0,-1)（:47085-47086 SafeNormalize(-UnitY)）
        let ux = -player.vx, uy = -player.vy;
        const ul = Math.hypot(ux, uy);
        if (ul > 0) { ux /= ul; uy /= ul; } else { ux = 0; uy = -1; }
        // vector13 = 玩家 90t 预测位(num61=90,:47093-47094);vector14 = 玩家速度反向
        // 100px 布枪点(num60=100,:47095)
        const leadX = player.cx + player.vx * 90, leadY = player.cy + player.vy * 90;
        let px = player.cx + ux * 100, py = player.cy + uy * 100;
        // :47096-47104 布枪点距玩家 <100 时外推(v 已单位,防御性死代码 1:1)
        if (Math.hypot(px - player.cx, py - player.cy) < 100) {
          let ex = player.cx - px, ey = player.cy - py;
          const el = Math.hypot(ex, ey);
          if (el === 0) { ex = ux; ey = uy; } else { ex /= el; ey /= el; }
          px = player.cx - ex * 100; py = player.cy - ey * 100;
        }
        // v2 = 预测位 − 布枪点 → 弹向（:47105-47108;919 收敛实现:12 速直飞,弹 ai1=
        // ai1/100 延时参随收敛省略）;Boss_CanShootExtraAt 多人补射(:47114-47140)恒跳
        // 主目标(:47324),单人无效,略
        const ax = leadX - px, ay = leadY - py;
        const al = Math.hypot(ax, ay) || 1;
        shoot(game, px, py, (ax / al) * 12, (ay / al) * 12,
          dayEnrage ? 9999 : phase2 ? 60 : 50, 919, 240);  // num6 :46332
      }
      e.ai1 += 1;
      if (e.ai1 >= dur) { e.ai0 = 1; e.ai1 = 0; }

```


---

## 🤖 Assistant · 2026-08-19T09:05:20.381Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The edits look correct. Now run tsc --noEmit and the tests. First capture a tsc baseline — since there may be pre-existing errors, run tsc and compare against a baseline. I don't have a stored baseline; the task says "零新错(基线既有错忽略)". Let me run tsc and check errors are only in files unrelated to my edits, or pre-existing in those files. To determine "new" vs baseline, I can use git... but this isn't a git repo ("Is directory a git repo: No"). Hmm. Let me just run tsc and inspect any errors mentioning my four files.
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:05:21.069Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "npx tsc --noEmit 2>&1 | tail -30",
 "description": "Run TypeScript check",
 "timeout": 300000
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:05:37.420Z

**📎 ToolResult**

```
    Type '{ "2": number[]; "3": number[]; "8": number[]; "9": number[]; "11": number[]; "12": number[]; "13": number[]; "14": number[]; "71": number[]; "72": number[]; "73": number[]; "147": number[]; "150": number[]; "166": number[]; "174": number[]; "314": number[]; "364": number[]; "365": number[]; ... 25 more ...; "5395":...' is not comparable to type 'Record<string, [number, number]>'.
      Property '"2"' is incompatible with index signature.
        Type 'number[]' is not comparable to type '[number, number]'.
          Target requires 2 element(s) but source may have fewer.
tests/player-sitting.test.ts(4,10): error TS2300: Duplicate identifier 'World'.
tests/player-sitting.test.ts(5,10): error TS2300: Duplicate identifier 'TILE_BY_KEY'.
tests/player-sitting.test.ts(7,10): error TS2300: Duplicate identifier 'Player'.
tests/player-sitting.test.ts(8,10): error TS2300: Duplicate identifier 'Inventory'.
tests/player-sitting.test.ts(77,10): error TS2300: Duplicate identifier 'World'.
tests/player-sitting.test.ts(78,10): error TS2300: Duplicate identifier 'TILE_BY_KEY'.
tests/player-sitting.test.ts(118,10): error TS2300: Duplicate identifier 'Inventory'.
tests/player-sitting.test.ts(119,10): error TS2300: Duplicate identifier 'Player'.
tests/slimebody-typegate.test.ts(21,32): error TS2698: Spread types may only be created from object types.
tests/slimebody-typegate.test.ts(29,36): error TS2698: Spread types may only be created from object types.
tests/slimebody-typegate.test.ts(37,34): error TS2698: Spread types may only be created from object types.
tests/snow-biome-plants.test.ts(41,51): error TS2345: Argument of type 'number' is not assignable to parameter of type '19 | 20 | 21'.
tests/swingarc.test.ts(295,10): error TS2339: Property 'entities' does not exist on type 'GameHooks'.
tests/town-npc-attack.test.ts(37,59): error TS2554: Expected 3 arguments, but got 4.
tests/town-npc-attack.test.ts(53,62): error TS2554: Expected 3 arguments, but got 4.
tests/town-npc-attack.test.ts(67,59): error TS2554: Expected 3 arguments, but got 4.
tests/town-npc-attack.test.ts(77,59): error TS2554: Expected 3 arguments, but got 4.
tests/town-npc-attack.test.ts(96,59): error TS2554: Expected 3 arguments, but got 4.
tests/town-npc-hurt.test.ts(30,59): error TS2554: Expected 3 arguments, but got 4.
tests/town-npc-hurt.test.ts(38,59): error TS2554: Expected 3 arguments, but got 4.
tests/town-npc-hurt.test.ts(39,62): error TS2554: Expected 3 arguments, but got 4.
tests/town-npc-hurt.test.ts(48,62): error TS2554: Expected 3 arguments, but got 4.
tests/town-npc-hurt.test.ts(56,59): error TS2554: Expected 3 arguments, but got 4.
tests/town-npc-hurt.test.ts(68,59): error TS2554: Expected 3 arguments, but got 4.
tests/town-npc-hurt.test.ts(81,59): error TS2554: Expected 3 arguments, but got 4.
tests/vanilla-pets.test.ts(21,65): error TS18046: 'v' is of type 'unknown'.

```


---

## 🤖 Assistant · 2026-08-19T09:05:40.951Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "npx tsc --noEmit 2>&1 | grep -E \"bossAI_lategame|bossAI_duke_moonlord|bossAI_martian|core/Game\\.ts\" | head -20; echo \"exit-grep:$?\"",
 "description": "Check tsc errors in the four edited files",
 "timeout": 300000
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:05:56.899Z

**📎 ToolResult**

```
exit-grep:0

```


---

## 🤖 Assistant · 2026-08-19T09:06:02.947Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Wait — "exit-grep:0" printed but no matching lines above it. Actually grep exit 0 means matches found... but nothing printed? Odd. Hmm, `echo "exit-grep:$?"` — $? is from the grep. If grep found nothing it exits 1. It printed exit-grep:0 with no lines... that's contradictory. Unless the grep matched something that got... no. Let me re-run more carefully — maybe tsc output went differently. Actually the head -20 consumed... no, head passes through. Let me rerun the grep explicitly.
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:06:04.653Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "npx tsc --noEmit 2>&1 > /tmp/tsc-out.txt; grep -cE \"error TS\" /tmp/tsc-out.txt; grep -E \"bossAI_lategame|bossAI_duke_moonlord|bossAI_martian|src/core/Game\" /tmp/tsc-out.txt | head; echo \"matches-done\"",
 "description": "Count tsc errors and check edited files",
 "timeout": 300000
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:06:20.323Z

**📎 ToolResult**

```
46
matches-done

```


---

## 🤖 Assistant · 2026-08-19T09:06:28.708Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
46 total errors, and NONE in my four edited files (bossAI_lategame.ts, bossAI_duke_moonlord.ts, bossAI_martian.ts, src/core/Game.ts). These 46 are the pre-existing baseline (in tests/ files as seen). Zero new errors. 

Now run the four test files.
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:06:29.896Z · glm-x-preview-260804

```
`tsc` 在四个已编辑的文件中均无错误（46 个预存的基准错误全部位于无关的测试文件中）。现在我来运行验收测试。
```


---

## 🤖 Assistant · 2026-08-19T09:06:30.880Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "npx vitest run tests/bossAI-lategame.test.ts tests/bossAI-dd2.test.ts tests/boss-hostile-proj-sim.test.ts tests/eoc-dash-speed.test.ts 2>&1 | tail -25",
 "description": "Run the four acceptance test files",
 "timeout": 300000
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:06:34.662Z

**📎 ToolResult**

```
[atlas-lint] 753 表全自洽 ✓ (0 warn)
[l10n-audit] 515 键全部命中 ✓

 RUN  v2.1.9 ~/Project/GLM/SandboxWorld/game

 ✓ tests/bossAI-lategame.test.ts (56 tests) 50ms
 ✓ tests/bossAI-dd2.test.ts (22 tests) 53ms
 ✓ tests/eoc-dash-speed.test.ts (1 test) 7ms
 ✓ tests/boss-hostile-proj-sim.test.ts (1 test) 14ms

 Test Files  4 passed (4)
      Tests  80 passed (80)
   Start at  17:06:31
   Duration  2.96s (transform 2.05s, setup 0ms, collect 10.19s, tests 125ms, environment 1ms, prepare 240ms)

```


---

## 🤖 Assistant · 2026-08-19T09:07:09.930Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All 4 test files pass (80 tests). 

Now let me add targeted test coverage for the four changes to make the work verifiable — the task says "逐项带行号注释" (done in code) and "完成后报告:四组落点+测试". It says run the listed tests green — done. Should I ADD tests? The task's acceptance only requires the existing named tests to pass. But a quick sanity test would strengthen the work. The task didn't explicitly ask to add tests. Given the guidance "Complete the task fully—don't gold-plate", the acceptance criteria are met. However, a smoke-verification that my new code paths actually execute correctly (e.g., Empress case 11 table selection in expert, Duke frame machine writing customFrameIdx) would catch wiring mistakes. Let me write a quick throwaway check via vitest? Or a quick node script? The project convention: one-off diagnostic scripts `_*.mjs` go through tools/run-diag.mjs with a private vite instance — that's for browser probes. For pure logic, I can write a temporary vitest test file and delete it, or better: use `npx vitest run` with an inline test? Simplest: create a temporary test file, run it, then delete it. Actually — tests directory files persist; creating then deleting is fine but the CLAUDE.md says "删文件前先 pgrep 确认无关联进程" (about processes). A temp test file is low risk.

Actually, let me reconsider: the unit-test harness in tests/bossAI-lategame.test.ts already exercises empressOfLightAI? Let me check if there are empress tests — grep showed describes for cultist/clones/ancient light/queen slime minions/textures/moonlord/ice mist/lightning. No empress AI test. The duke section of bossAI_duke_moonlord.ts has "月总召怪段" tests only.

Given the risk that my case 11 has a runtime bug (e.g., unreachable, or table wrong), a quick smoke test is worthwhile — cheap and validates the wiring. I'll write a temporary test file /tmp? vitest needs it under the project. I'll create tests/_tmp-fourgroups.test.ts, run, then delete. Hmm — name with `_` prefix marks it as one-off. Fine.

Test plan:
1. Empress expert table: create world with isExpert (how do tests set difficulty? World constructor `new World(W, H, 7, seed)` — difficulty param? Let me check World constructor signature: `new World(160, 120, 7, 'lategame-test')` — 4th is seed name. difficulty likely a field on world (world.difficulty?). Check World for `difficulty` / `isExpert`.)

Let me check how World exposes difficulty.
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:07:11.051Z · glm-x-preview-260804

```
全部通过。我来对两个新的运行时路径进行冒烟测试（专家表选择 + 猪鲨帧机），使用一个之后会删除的临时测试文件。
```


---

## 🤖 Assistant · 2026-08-19T09:07:12.167Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"isExpert\\|difficulty\" ~/Project/GLM/SandboxWorld/game/src/world/World.ts | head -10; grep -n \"constructor\" ~/Project/GLM/SandboxWorld/game/src/world/World.ts | head -3",
 "description": "Check World difficulty API"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:07:12.206Z

**📎 ToolResult**

```
80:   *  0 经典 / 1 专家 / 2 大师 / 3 旅程。与角色难度（Appearance.difficulty 0软/1中/2硬/3旅）
84:  difficulty = 0;
116:   *  stopBiomeSpread/difficultySlider）、玩家侧进 player 段（godmode/
137:  get isExpert(): boolean { return mainDifficulty(this) >= GDL.EXPERT; }
141:  get isJourney(): boolean { return this.difficulty === 3; }
331:    if (p.difficulty !== undefined) w.difficulty = p.difficulty;   // Main.GameMode（旧包缺省 0）
56:  constructor(dayLengthMs: number) { this.dayLengthMs = dayLengthMs; }
303:  constructor(w: number, h: number, seed: number, name = '新世界', skipStore = false) {

```


---

## 🤖 Assistant · 2026-08-19T09:07:55.496Z · glm-x-preview-260804

**🔧 ToolUse: `Write`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/tests/_tmp-fourgroups.test.ts",
 "content": "// 一次性冒烟探针(四组验收补测,跑完即删):光女 expert 表/case11 布枪几何 +\n// 猪鲨 FindFrame 帧机 + 火星 expert 伤插值。\nimport { describe, it, expect } from 'vitest';\nimport { Enemy } from '../src/entities/Enemy';\nimport { World } from '../src/world/World';\nimport { TILE } from '../src/core/constants';\nimport { getAttackDamageForProjectiles } from '../src/stats/ScaleStats';\nimport type { GameHooks } from '../src/entities/types';\n\nconst W = 200, H = 140, FLOOR = 120;\n\nfunction makeWorld(expert: boolean): World {\n  const w = new World(W, H, 7, 'fourgroups-test');\n  w.groundLevel = 60;\n  if (expert) w.difficulty = 1;\n  for (let x = 0; x < W; x++) {\n    w.store.setTile(x, FLOOR, 1);\n    w.store.setTile(x, FLOOR + 1, 1);\n  }\n  return w;\n}\n\nfunction makeHooks(world: World, playerAt: { x: number; y: number }) {\n  const enemies: Enemy[] = [];\n  const projectiles: Array<{ x: number; y: number; vx: number; vy: number; dmg: number; projId?: number }> = [];\n  const em = {\n    nextId: 1,\n    add: (e: unknown, bucket: 'enemies' | 'projectiles') => {\n      const ent = e as { id: number };\n      ent.id = em.nextId++;\n      if (bucket === 'enemies') enemies.push(e as Enemy);\n      else projectiles.push(e as { x: number; y: number; vx: number; vy: number; dmg: number; projId?: number });\n    },\n  };\n  const px = playerAt.x * TILE, py = playerAt.y * TILE;\n  const player = {\n    x: px, y: py, w: 20, h: 42, cx: px + 10, cy: py + 21,\n    vx: 0, vy: 0, hp: 400, maxHp: 400, dead: false,\n    aabbOverlaps: () => false,\n  };\n  const hooks = {\n    world, player,\n    enemies: () => enemies,\n    critters: () => [],\n    spawnDrop: () => null,\n    damagePlayer: () => {},\n    addDamageNumber: () => {},\n    cutTile: () => {},\n    onEnemyKilled: () => {},\n    spawnEnemy: () => {},\n    spawnParticles: () => {},\n    notifyInventoryChanged: () => {},\n    playSfx: () => {},\n    playSfxFiles: () => {},\n    showPickupLabel: () => {},\n    entities: em,\n  } as unknown as GameHooks;\n  return { hooks, enemies, projectiles, player };\n}\n\nfunction spawn(h: ReturnType<typeof makeHooks>, id: number, tx: number, ty: number): Enemy {\n  const e = Enemy.fromVanilla(id, tx * TILE, ty * TILE)!;\n  e.id = 100;\n  h.enemies.push(e);\n  return e;\n}\n\nfunction tick(h: ReturnType<typeof makeHooks>, n: number, only?: Enemy[]) {\n  for (let i = 0; i < n; i++) {\n    for (const e of only ?? h.enemies) {\n      if (!e.dead) e.fixedUpdate(1 / 60, h.hooks);\n    }\n  }\n}\n\ndescribe('光女 expert 二阶段表 + case11', () => {\n  it('expert 二阶段第 3 拍(ai2=3)选 11:布枪点=玩家速度反向 100px,弹向指向 90t 预测位', () => {\n    const h = makeHooks(makeWorld(true), { x: 100, y: 100 });\n    const e = spawn(h, 636, 100, 80);\n    e.bInit = true;\n    e.ai0 = 1; e.ai1 = 0; e.ai2 = 3;   // 二阶段表第 3 槽(slot 3)\n    e.ai3 = 1;                          // IsInPhase2\n    e.hp = e.maxHp / 2 - 1;\n    // 玩家向右跑 → 布枪点在玩家左侧 100px\n    h.player.vx = 10; h.player.vy = 0;\n    h.projectiles.length = 0;\n    // 选招枢纽 20t(expert 二阶段 20-5=15? phase2 num17=20 → dur=20)后进 case11\n    tick(h, 25, [e]);\n    expect(e.ai0).toBe(11);\n    // case11 内推进若干拍,枪应在每 3t 出一杆\n    h.projectiles.length = 0;\n    tick(h, 6, [e]);\n    expect(h.projectiles.length).toBeGreaterThanOrEqual(2);\n    for (const p of h.projectiles) {\n      const dx = p.x - (h.player.cx - 100);   // Arrow 左上角锚;粗校验:枪在玩家左 100px 附近\n      void dx;\n    }\n    // 第一杆(ai1=0 当拍)几何:出生点 ≈ 玩家中心 + (-100, 0)(Arrow 构造 x/y 是左上角)\n    // Arrow(x, y, ...) 的 x/y 即传参坐标 —— shoot 传的是 px/py(布枪点),w≈弹宽。\n    const first = h.projectiles[0] as unknown as { x: number; y: number };\n    expect(Math.abs(first.x - (h.player.cx - 100))).toBeLessThan(40);\n    // 弹向:预测位 = 玩家 + (900, 0),布枪点在 (-100,0) → 弹向 +X\n    const v = h.projectiles[0] as unknown as { vx: number; vy: number };\n    expect(v.vx).toBeGreaterThan(11.9);\n    expect(Math.abs(v.vy)).toBeLessThan(0.5);\n  });\n\n  it('经典夜战二阶段第 3 拍(ai2=3)不选 11(9 拍经典表槽 3=5)', () => {\n    const h = makeHooks(makeWorld(false), { x: 100, y: 100 });\n    // 夜间:isDay 置否\n    (h.hooks.world.clock as unknown as { isDay: boolean }).isDay = false;\n    const e = spawn(h, 636, 100, 80);\n    e.bInit = true;\n    e.ai0 = 1; e.ai1 = 0; e.ai2 = 3;\n    e.ai3 = 1;\n    e.hp = e.maxHp / 2 - 1;\n    tick(h, 50, [e]);\n    expect(e.ai0 === 11).toBe(false);\n  });\n});\n\ndescribe('猪鲨 FindFrame case 370', () => {\n  it('冲撞态 ai2<10 帧 6、≥10 帧 7;悬浮态 0-5 游动 6t/帧', () => {\n    const h = makeHooks(makeWorld(false), { x: 100, y: 100 });\n    const e = spawn(h, 370, 100, 90);\n    // 直落冲撞态\n    e.bInit = true;\n    e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;\n    tick(h, 1, [e]);\n    expect(e.customFrameIdx).toBe(6);      // ai2=0(<10)\n    tick(h, 11, [e]);\n    expect(e.customFrameIdx).toBe(7);      // ai2≥10\n    // 悬浮态:游动帧从 0 起,每 6t 进一帧\n    e.ai0 = 0; e.ai2 = 0; e.npcFrameT = 0; e.customFrameIdx = null;\n    tick(h, 1, [e]);\n    expect(e.customFrameIdx).toBe(0);\n    tick(h, 6, [e]);\n    expect(e.customFrameIdx).toBe(1);\n    tick(h, 6 * 4, [e]);\n    expect(e.customFrameIdx).toBe(5);\n    tick(h, 6, [e]);\n    expect(e.customFrameIdx).toBe(0);      // 回卷\n  });\n\n  it('龙卷态 3 计时窗 [60,80] 张口帧 6/7', () => {\n    const h = makeHooks(makeWorld(false), { x: 100, y: 100 });\n    const e = spawn(h, 370, 100, 90);\n    e.bInit = true;\n    e.ai0 = 3; e.ai1 = 0; e.ai2 = 65; e.ai3 = 0;\n    e.npcFrameT = 0; e.customFrameIdx = null;\n    tick(h, 1, [e]);\n    expect(e.customFrameIdx).toBe(6);      // ai2=65 ∈ [60,80],非 (70,75) → 6\n    e.ai2 = 72;\n    tick(h, 1, [e]);\n    expect(e.customFrameIdx).toBe(7);      // ai2 ∈ (70,75) → 7\n  });\n});\n\ndescribe('火星 expert 弹伤插值', () => {\n  it('Remap 档:448 50→37 / 449 35→30 / 450 30→25 / 435 35→28', () => {\n    expect(getAttackDamageForProjectiles(50, 37, 1)).toBe(50);\n    expect(getAttackDamageForProjectiles(50, 37, 2)).toBe(37);\n    expect(getAttackDamageForProjectiles(35, 30, 2)).toBe(30);\n    expect(getAttackDamageForProjectiles(30, 25, 2)).toBe(25);\n    expect(getAttackDamageForProjectiles(35, 28, 2)).toBe(28);\n  });\n});\n"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:07:55.516Z

**📎 ToolResult**

```
File created successfully at: ~/Project/GLM/SandboxWorld/game/tests/_tmp-fourgroups.test.ts (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T09:07:58.016Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "npx vitest run tests/_tmp-fourgroups.test.ts 2>&1 | tail -30",
 "description": "Run temp smoke test",
 "timeout": 180000
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:08:02.149Z

**📎 ToolResult**

```
       |                                                            ^
    112|     const e = spawn(h, 636, 100, 80);
    113|     e.bInit = true;

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/2]⎯

 FAIL  tests/_tmp-fourgroups.test.ts > 猪鲨 FindFrame case 370 > 冲撞态 ai2<10 帧 6、≥10 帧 7;悬浮态 0-5 游动 6t/帧
AssertionError: expected 7 to be 5 // Object.is equality

- Expected
+ Received

- 5
+ 7

 ❯ tests/_tmp-fourgroups.test.ts:140:30
    138|     expect(e.customFrameIdx).toBe(1);
    139|     tick(h, 6 * 4, [e]);
    140|     expect(e.customFrameIdx).toBe(5);
       |                              ^
    141|     tick(h, 6, [e]);
    142|     expect(e.customFrameIdx).toBe(0);      // 回卷

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/2]⎯

 Test Files  1 failed (1)
      Tests  2 failed | 3 passed (5)
   Start at  17:07:58
   Duration  3.04s (transform 1.97s, setup 0ms, collect 2.72s, tests 22ms, environment 0ms, prepare 50ms)

```


---

## 🤖 Assistant · 2026-08-19T09:08:21.021Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Two failures — need to investigate whether they're bugs in my implementation or in the test assumptions.

Failure 2: "冲撞态 ai2<10 帧 6、≥10 帧 7;悬浮态" — after charge state frame 7, I switched to ai0=0 (hover), set npcFrameT=0, customFrameIdx=null, ticked 1 → frame 0 expected... wait the failure is at line 140: after `tick(h, 1)` → 0 ✓ (line 136 passed presumably), then `tick(h, 6)` → 1 ✓ (line 138 passed), then `tick(h, 24)` → expected 5, got 7.

Why would hover produce frame 7? Because during the 24 ticks, the duke hover (ai0=0) runs dukeHover → ai2 accumulates → at hoverT (60, or enraged → 10) it picks next attack. hoverT: flag5 = ai3 < (flag3?3:5)*2 = 10 → ai3=0 <10 → hoverT = 30 (flag5 && !flag3 && !flag4 → hoverT=30). After 30 ticks of hover, dukePick1: a3 = 0 → next=1 → dukeCharge → ai0=1! Then FindFrame with ai0=1, ai2=0 <10 → frame 6... hmm but got 7.

Wait — actually also dukeEnraged: player at y = 100*16 = 1600 ≥ 800; surface = groundLevel(60)*16 = 960; player.y (1600) > surface (960) → enraged=true → hoverT = 10. So after ~10 ticks of hover, it charges: ai0=1, ai2 resets 0, then charge runs 10+ ticks → ai2 ≥ 10 → frame 7. That's exactly the observed 7. So the test environment (player underground) makes duke enraged → transitions to charge. Not an implementation bug — test assumption issue. I should either prevent state transition or check frames before the transition. The state machine is working correctly.

Failure 1: empress test — error at line 111/113 area (the failure output truncated). It says [1/2] shows lines 112-113 — probably `e.ai0` wasn't 11 after 25 ticks, or an exception. The visible part: something at line 111 with `^` pointing... the snippet shows lines 112-113 only; the actual assertion error for test 1 isn't fully shown. Let me re-run with more output to see the first failure detail.
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:08:22.119Z · glm-x-preview-260804

```
有两个失败 —— 需检查是 test-harness 假设问题还是真正的 bug。让我查看一下第一个失败的详细信息。
```


---

## 🤖 Assistant · 2026-08-19T09:08:22.717Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "npx vitest run tests/_tmp-fourgroups.test.ts 2>&1 | head -60",
 "description": "See first failure details",
 "timeout": 180000
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:08:26.343Z

**📎 ToolResult**

```
[atlas-lint] 753 表全自洽 ✓ (0 warn)
[l10n-audit] 515 键全部命中 ✓

 RUN  v2.1.9 ~/Project/GLM/SandboxWorld/game

 ❯ tests/_tmp-fourgroups.test.ts (5 tests | 2 failed) 16ms
   × 光女 expert 二阶段表 + case11 > 经典夜战二阶段第 3 拍(ai2=3)不选 11(9 拍经典表槽 3=5) 3ms
     → Cannot set property isDay of #<Clock> which has only a getter
   × 猪鲨 FindFrame case 370 > 冲撞态 ai2<10 帧 6、≥10 帧 7;悬浮态 0-5 游动 6t/帧 4ms
     → expected 7 to be 5 // Object.is equality

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 2 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  tests/_tmp-fourgroups.test.ts > 光女 expert 二阶段表 + case11 > 经典夜战二阶段第 3 拍(ai2=3)不选 11(9 拍经典表槽 3=5)
TypeError: Cannot set property isDay of #<Clock> which has only a getter
 ❯ tests/_tmp-fourgroups.test.ts:111:60
    109|     const h = makeHooks(makeWorld(false), { x: 100, y: 100 });
    110|     // 夜间:isDay 置否
    111|     (h.hooks.world.clock as unknown as { isDay: boolean }).isDay = fal…
       |                                                            ^
    112|     const e = spawn(h, 636, 100, 80);
    113|     e.bInit = true;

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/2]⎯

 FAIL  tests/_tmp-fourgroups.test.ts > 猪鲨 FindFrame case 370 > 冲撞态 ai2<10 帧 6、≥10 帧 7;悬浮态 0-5 游动 6t/帧
AssertionError: expected 7 to be 5 // Object.is equality

- Expected
+ Received

- 5
+ 7

 ❯ tests/_tmp-fourgroups.test.ts:140:30
    138|     expect(e.customFrameIdx).toBe(1);
    139|     tick(h, 6 * 4, [e]);
    140|     expect(e.customFrameIdx).toBe(5);
       |                              ^
    141|     tick(h, 6, [e]);
    142|     expect(e.customFrameIdx).toBe(0);      // 回卷

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/2]⎯

 Test Files  1 failed (1)
      Tests  2 failed | 3 passed (5)
   Start at  17:08:23
   Duration  2.75s (transform 1.74s, setup 0ms, collect 2.39s, tests 16ms, environment 0ms, prepare 77ms)

```


---

## 🤖 Assistant · 2026-08-19T09:09:01.609Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Both failures are test-harness issues, not implementation bugs:

1. `clock.isDay` is a getter-only property — I can't set it directly. Instead the empress reads `game.world.clock.isDay` — I need to control day/night via timeOfDay. Let me check Clock: isDay is computed from timeOfDay presumably. Let me check how to set night. Clock fields: timeOfDay (0..1), isDay getter. In makeWorld, the default timeOfDay likely starts at 8:15 AM (day). To make night, set clock.timeOfDay to a night value (e.g., 0 = 12:00 midnight? The convention: timeOfDay 0 = midnight? From memory: "时间系统1:1 DAWN/DUSK=4:30/19:30" and empress code computes mainTime = (timeOfDay − 4.5/24) × 86400. Day starts at timeOfDay = 4.5/24. So night = timeOfDay < 4.5/24, e.g. 0.0 = midnight).

Actually wait — the FIRST empress test (expert, case 11) PASSED. That test ran with default world state — which might be DAY (flag4 dayEnrage → flag2 true regardless of expert). Hmm! That means the first test might have passed via dayEnrage rather than the expert table! Let me check: makeWorld(true) sets difficulty=1 → isExpert. Default clock timeOfDay — if it starts at 8:15am → isDay true → dayEnrage also true. So the pass doesn't prove the expert-table path specifically. I should set night (timeOfDay 0) in the expert test so that ONLY isExpert drives flag2.

2. Duke hover test: state transitioned to charge (enraged → hoverT=10). Fix: put the player above ground level (not underground) to avoid enrage: player at y such that 800 <= y <= surface. surface = groundLevel * TILE = 60*16 = 960. Player y must be in [800, 960)?? That's a narrow band — also the x check: player.x > 6400 && player.x < worldWidth*16-6400 → x=100*16=1600 < 6400 → false. So need y in [800, 960): y tile ~52-59. Set player at (100, 55) → py = 880 ∈ [800,960) → not enraged. But wait, dukeEnraged uses player.y < 800 → py=880 not < 800 ✓; player.y > surface (960)? 880 < 960 ✓ not enraged. Good. But then hoverT = 30 (flag5, not flag3) — after 30 ticks it charges again. For the 24-tick swim test, 1+6+24+6 = 37 ticks > 30 → charge again. Hmm. To avoid the transition mid-test, I can directly test the frame machine instead of driving full AI: set ai0=0 and tick only up to the needed counts, or pin ai2 low by resetting. Alternative: call dukeFishronAI ticks but with hoverT=30, total ticks 37 crosses 30. I could split assertions: instead of continuous ticking, set e.ai2 = 0 after the transition... Simplest: verify the swim wrap with fewer ticks — swim 6t/frame; to see frames 0→5 needs 36 ticks. That exceeds hoverT=30. 

Option: test the swim animation via a non-enraged, non-transitioning state — state 3 (tornado) with ai2 < 60 also runs the swim branch via my dukeFindFrame... but state 3's AI (dukeSharknado) also advances ai2 and at ai2=60 fires. The frame machine's swim cadence is identical across states; I can verify wrap in state -1 (spawn, 75t, ai2 always < 60 → swim). Spawn state lasts 75 ticks — enough for 36 ticks of swim. But spawn ai0=-1... after 75t becomes 0. 36 < 75. 

Plan for duke test:
- charge frames: as before (passed).
- swim cadence: state -1: set e.ai0=-1, e.ai2=0, npcFrameT=0, customFrameIdx=null. tick 1 → frame 0; tick 6 → 1; tick 24 → 5; tick 6 → 0. Total 37 < 75 ✓. But careful: spawn state sets spawnAlpha etc. — irrelevant.
- Also the wrap-from-7: after charge frame 7, hover first tick wraps to 0 — covered by the frame-null reset... actually I explicitly set customFrameIdx=null. To test wrap honestly: after charge (frame 7), switch to ai0=0 with customFrameIdx=7 intact, tick 1 → frame 0 immediately (wrap gate). That validates the :72839-72842 every-tick wrap.

But hover at ai0=0 will transition after 10-30 ticks; 1 tick is fine.

3. Empress night test: set clock.timeOfDay. Check the Clock class for settable fields.
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:09:02.873Z · glm-x-preview-260804

```
两者都是 `test-harness` 的问题（`isDay` 是一个 getter-only 属性；玩家位于地下导致猪鲨暴怒 → 导致过早冲锋）。我来检查一下 `Clock API` 并修复测试。
```


---

## 🤖 Assistant · 2026-08-19T09:09:03.771Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"isDay\\|timeOfDay\" ~/Project/GLM/SandboxWorld/game/src/world/World.ts | head -8",
 "description": "Check Clock isDay/timeOfDay definition"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:09:03.799Z

**📎 ToolResult**

```
39:  timeOfDay: number = 8.25 / 24;   // 0-1，0=午夜 0.5=正午（起始 8:15AM = Main.time 13500）
60:    this.timeOfDay += dtMs / this.dayLengthMs;
61:    while (this.timeOfDay >= 1) { this.timeOfDay -= 1; this.dayCount++; }
63:  get isDay(): boolean { return this.timeOfDay > Clock.DAWN && this.timeOfDay < Clock.DUSK; }
66:    const t = this.timeOfDay;
72:  get hourFloat(): number { return this.timeOfDay * 24; }
332:    w.clock.timeOfDay = p.clock.timeOfDay;

```


---

## 🤖 Assistant · 2026-08-19T09:09:46.171Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
`clock.timeOfDay` is settable (default 8.25/24 = day). Night: timeOfDay = 0 (midnight). DAWN = 4.5/24 presumably.

Also important: my first empress test passed with default timeOfDay = 8:15AM = DAY → dayEnrage was true, so flag2 came from dayEnrage, not isExpert. To specifically prove the expert table, set timeOfDay = 0 (night) in the expert test too. Let me rewrite the temp test:

- Expert test: world difficulty=1, timeOfDay=0 (night) → flag2 = isExpert only. Expect case 11 selected at slot 3.

Wait — but hold on: with night + expert, is there any interference from `enragedLeave`? genuinelyEnraged = ai3∈{2,3}. I set ai3=1 (phase2, not enraged). But at full HP + dayEnrage the code sets ai3 += 2 — it's night now so no. Also `dayEnrage ? 9999 : ...` damage — night → normal damage 60. Good.

But another consideration: in case 11 hover, the empress hovers toward player; the shooting geometry test — the empress position vs player distance ≤ 2400 required. Empress at (100,80) tiles, player at (100,100) tiles → 20 tiles = 320px < 2400 ✓.

Also case 1 dur: phase2 → 20; getGoodWorld undefined → no halving. ai1 reaches 20 after 20 ticks, then picks. 25 ticks is enough. But — first tick: empressDashTo runs; fine.

One more check on the first test's assertion about projectile x: `shoot(game, px, py, ...)` → Arrow(x, y, ...) where x/y are... In bossAI.ts shoot, `new Arrow(x, y, vx, vy, ...)` — need to know if Arrow's x/y is top-left or the passed point. In test I wrote tolerance 40px which absorbs the frame width. It passed with tolerance — but since I'm rewriting, keep tolerance 40.

Projectile velocity: aiming from gun point (-100, 0) relative to player toward predicted (+900): direction (1000, 0) normalized → (1,0) × 12 → vx=12, vy=0. Assertions: vx > 11.9, |vy| < 0.5. ✓.

Now the empress night-classic test: difficulty=0, timeOfDay=0 (night). Slot 3 in classic 9-slot table = value 5 (eternal rainbow). After transition, ai0 should be 5 (not 11). But note: with ai0=5 (rainbow) the AI runs case 5 — fine, just assert ai0 !== 11 (and ideally === 5). Timing: classic phase2 dur=20 ticks; 50 ticks is enough (case 5 dur = 42+(30-15)=57 — it stays 5 for a while). Assert e.ai0 === 5 at some point... it could move on if 50 ticks > 20+57=77? No, 50 < 77, so at tick 50: case 1 (20t) → case 5 started at t=20, runs 57t → still in 5 at t=50. Assert ai0 === 5.

Duke test rewrite:
- charge: as before (works).
- swim cadence in spawn state -1 (75t window).
- wrap gate: after charge frame 7 → ai0=0 → 1 tick → 0.
- tornado mouth windows: keep (passed).

Also for the swim test I previously relied on ai0=0 hover; switch to ai0=-1 to avoid transitions. In state -1, e.ai2 += 1 each tick from 0; at ai2 > 20 vy=-2 etc. — harmless. After 37 ticks ai2=37 < 60 → swim branch. ✓.

Also ensure not enraged in duke tests: move player to (100, 55) → py = 55*16 = 880 ∈ [800, 960). Good — and for charge test the transition doesn't matter (I set ai0=1 directly; charge runs its 30t then back to hover — I only tick 12).

Actually wait — charge test: tick(h, 1) → ai2 becomes 1 → frame reads ai2=1 <10 → 6 ✓. Then tick(h, 11) → ai2 = 12 ≥ 10 → 7 ✓. (Passed already.)

Let me also double-check duke spawn state bInit: my spawn sets e.bInit = true to skip re-init, ai0=-1 directly. In dukeFishronAI, ai0=-1 → case -1 runs; invuln; ai2 += 1. Fine.

Rewrite the temp test file.
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:10:15.155Z · glm-x-preview-260804

**🔧 ToolUse: `Write`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/tests/_tmp-fourgroups.test.ts",
 "content": "// 一次性冒烟探针(四组验收补测,跑完即删):光女 expert 表/case11 布枪几何 +\n// 猪鲨 FindFrame 帧机 + 火星 expert 伤插值。\nimport { describe, it, expect } from 'vitest';\nimport { Enemy } from '../src/entities/Enemy';\nimport { World } from '../src/world/World';\nimport { TILE } from '../src/core/constants';\nimport { getAttackDamageForProjectiles } from '../src/stats/ScaleStats';\nimport type { GameHooks } from '../src/entities/types';\n\nconst W = 200, H = 140, FLOOR = 120;\n\nfunction makeWorld(expert: boolean): World {\n  const w = new World(W, H, 7, 'fourgroups-test');\n  w.groundLevel = 60;\n  if (expert) w.difficulty = 1;\n  w.clock.timeOfDay = 0;   // 午夜(flag2 只剩 isExpert 一路)\n  for (let x = 0; x < W; x++) {\n    w.store.setTile(x, FLOOR, 1);\n    w.store.setTile(x, FLOOR + 1, 1);\n  }\n  return w;\n}\n\nfunction makeHooks(world: World, playerAt: { x: number; y: number }) {\n  const enemies: Enemy[] = [];\n  const projectiles: Array<{ x: number; y: number; vx: number; vy: number }> = [];\n  const em = {\n    nextId: 1,\n    add: (e: unknown, bucket: 'enemies' | 'projectiles') => {\n      const ent = e as { id: number };\n      ent.id = em.nextId++;\n      if (bucket === 'enemies') enemies.push(e as Enemy);\n      else projectiles.push(e as { x: number; y: number; vx: number; vy: number });\n    },\n  };\n  const px = playerAt.x * TILE, py = playerAt.y * TILE;\n  const player = {\n    x: px, y: py, w: 20, h: 42, cx: px + 10, cy: py + 21,\n    vx: 0, vy: 0, hp: 400, maxHp: 400, dead: false,\n    aabbOverlaps: () => false,\n  };\n  const hooks = {\n    world, player,\n    enemies: () => enemies,\n    critters: () => [],\n    spawnDrop: () => null,\n    damagePlayer: () => {},\n    addDamageNumber: () => {},\n    cutTile: () => {},\n    onEnemyKilled: () => {},\n    spawnEnemy: () => {},\n    spawnParticles: () => {},\n    notifyInventoryChanged: () => {},\n    playSfx: () => {},\n    playSfxFiles: () => {},\n    showPickupLabel: () => {},\n    entities: em,\n  } as unknown as GameHooks;\n  return { hooks, enemies, projectiles, player };\n}\n\nfunction spawn(h: ReturnType<typeof makeHooks>, id: number, tx: number, ty: number): Enemy {\n  const e = Enemy.fromVanilla(id, tx * TILE, ty * TILE)!;\n  e.id = 100;\n  h.enemies.push(e);\n  return e;\n}\n\nfunction tick(h: ReturnType<typeof makeHooks>, n: number, only?: Enemy[]) {\n  for (let i = 0; i < n; i++) {\n    for (const e of only ?? h.enemies) {\n      if (!e.dead) e.fixedUpdate(1 / 60, h.hooks);\n    }\n  }\n}\n\ndescribe('光女 expert 二阶段表 + case11', () => {\n  it('夜间 expert 二阶段第 3 拍(ai2=3)选 11:布枪点=玩家速度反向 100px,弹向指向 90t 预测位', () => {\n    const h = makeHooks(makeWorld(true), { x: 100, y: 100 });\n    const e = spawn(h, 636, 100, 80);\n    e.bInit = true;\n    e.ai0 = 1; e.ai1 = 0; e.ai2 = 3;   // 二阶段表第 3 槽(expert 表 = 11)\n    e.ai3 = 1;                          // IsInPhase2\n    e.hp = e.maxHp / 2 - 1;\n    h.player.vx = 10; h.player.vy = 0;  // 玩家向右跑 → 布枪点在玩家左侧 100px\n    tick(h, 25, [e]);                   // 选招枢纽 20t 后进 case11\n    expect(e.ai0).toBe(11);\n    h.projectiles.length = 0;\n    tick(h, 6, [e]);                    // 每 3t 一杆\n    expect(h.projectiles.length).toBeGreaterThanOrEqual(2);\n    // 第一杆(ai1=0 当拍)几何:出生点 ≈ 玩家中心 + (-100, 0)\n    const first = h.projectiles[0];\n    expect(Math.abs(first.x - (h.player.cx - 100))).toBeLessThan(40);\n    // 弹向:预测位 = 玩家 + (900, 0),布枪点 (-100,0) → 弹向 +X 12 速\n    expect(first.vx).toBeGreaterThan(11.9);\n    expect(Math.abs(first.vy)).toBeLessThan(0.5);\n  });\n\n  it('夜间经典二阶段第 3 拍(ai2=3)不选 11(9 拍经典表槽 3=5 永恒彩虹)', () => {\n    const h = makeHooks(makeWorld(false), { x: 100, y: 100 });\n    const e = spawn(h, 636, 100, 80);\n    e.bInit = true;\n    e.ai0 = 1; e.ai1 = 0; e.ai2 = 3;\n    e.ai3 = 1;\n    e.hp = e.maxHp / 2 - 1;\n    tick(h, 50, [e]);                   // 20t 选 5,case5 持续 57t → 仍处 5\n    expect(e.ai0).toBe(5);\n  });\n});\n\ndescribe('猪鲨 FindFrame case 370', () => {\n  it('冲撞态 ai2<10 帧 6、≥10 帧 7;回悬浮首 tick 由 7 回卷 0', () => {\n    const h = makeHooks(makeWorld(false), { x: 100, y: 55 });  // y=880px 不触发狂暴\n    const e = spawn(h, 370, 100, 50);\n    e.bInit = true;\n    e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;\n    e.npcFrameT = 0; e.customFrameIdx = null;\n    tick(h, 1, [e]);\n    expect(e.customFrameIdx).toBe(6);      // ai2=0(<10)\n    tick(h, 11, [e]);\n    expect(e.customFrameIdx).toBe(7);      // ai2≥10\n    // 张口帧 7 → 悬浮帶首 tick 回卷门(:72839-72842 每 tick 生效)\n    e.ai0 = 0; e.ai2 = 0;\n    tick(h, 1, [e]);\n    expect(e.customFrameIdx).toBe(0);\n  });\n\n  it('游动帶 0-5 六帶 6t/帧循环回卷(出生态 -1 全程游动)', () => {\n    const h = makeHooks(makeWorld(false), { x: 100, y: 55 });\n    const e = spawn(h, 370, 100, 50);\n    e.bInit = true;\n    e.ai0 = -1; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;\n    e.npcFrameT = 0; e.customFrameIdx = null;\n    tick(h, 1, [e]);\n    expect(e.customFrameIdx).toBe(0);\n    tick(h, 6, [e]);\n    expect(e.customFrameIdx).toBe(1);\n    tick(h, 6 * 4, [e]);\n    expect(e.customFrameIdx).toBe(5);\n    tick(h, 6, [e]);\n    expect(e.customFrameIdx).toBe(0);      // 回卷\n  });\n\n  it('龙卷态 3 计时窗 [60,80] 张口帧 6/7', () => {\n    const h = makeHooks(makeWorld(false), { x: 100, y: 55 });\n    const e = spawn(h, 370, 100, 50);\n    e.bInit = true;\n    e.ai0 = 3; e.ai1 = 0; e.ai2 = 65; e.ai3 = 0;\n    e.npcFrameT = 0; e.customFrameIdx = null;\n    tick(h, 1, [e]);\n    expect(e.customFrameIdx).toBe(6);      // ai2=65 ∈ [60,80],非 (70,75) → 6\n    e.ai2 = 72;\n    tick(h, 1, [e]);\n    expect(e.customFrameIdx).toBe(7);      // ai2 ∈ (70,75) → 7\n  });\n});\n\ndescribe('火星 expert 弹伤插值', () => {\n  it('Remap 档:448 50→37 / 449 35→30 / 450 30→25 / 435 35→28', () => {\n    expect(getAttackDamageForProjectiles(50, 37, 1)).toBe(50);\n    expect(getAttackDamageForProjectiles(50, 37, 2)).toBe(37);\n    expect(getAttackDamageForProjectiles(35, 30, 2)).toBe(30);\n    expect(getAttackDamageForProjectiles(30, 25, 2)).toBe(25);\n    expect(getAttackDamageForProjectiles(35, 28, 2)).toBe(28);\n  });\n});\n"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:10:15.166Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/tests/_tmp-fourgroups.test.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T09:10:30.612Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "npx vitest run tests/_tmp-fourgroups.test.ts 2>&1 | tail -30",
 "description": "Re-run temp smoke test",
 "timeout": 180000
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:10:33.148Z

**📎 ToolResult**

```
[atlas-lint] 753 表全自洽 ✓ (0 warn)
[l10n-audit] 515 键全部命中 ✓

 RUN  v2.1.9 ~/Project/GLM/SandboxWorld/game

 ✓ tests/_tmp-fourgroups.test.ts (6 tests) 9ms

 Test Files  1 passed (1)
      Tests  6 passed (6)
   Start at  17:10:31
   Duration  1.89s (transform 1.18s, setup 0ms, collect 1.64s, tests 9ms, environment 0ms, prepare 42ms)

```


---

## 🤖 Assistant · 2026-08-19T09:10:55.622Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All 6 smoke tests pass, confirming:
1. Empress expert table selects case 11 at slot 3 in night+expert (flag2 from isExpert only), lances spawn at player-velocity-opposite 100px aimed at 90t-predicted position with 12 speed.
2. Classic night phase-2 slot 3 → case 5 (not 11).
3. Duke FindFrame: charge frames 6/7 by ai2<10, wrap 7→0 on return to swim, 6 swim frames at 6t/frame with wrap, tornado window mouth frames 6/7.
4. Martian Remap values.

Now, should I keep these tests or delete? The task says the temp file is one-off (跑完即删 per my own header). The acceptance criteria only named existing tests. Keeping a new test file in tests/ isn't requested — but valuable? The guidance: don't create files unless necessary; don't gold-plate. The task explicitly says report "四组落点+测试" — tests meaning run the named ones green. I'll delete the temp file per my plan (pgrep check for associated processes first per CLAUDE.md — it's a vitest file, no long-running process; the vitest run already exited).

Actually, let me reconsider — would the maintainers want these assertions? The repo has extensive test coverage culture (135+ tests). But the task instruction is precise about acceptance and my mandate is the four groups with the named tests green. The temp file header says 跑完即删. I'll delete it.

Then re-run the four named tests + tsc once more to confirm final state (tsc after all edits — Game.ts edit happened before my last tsc? Order: tsc ran AFTER all four groups' edits (I edited Game.ts and martian before running tsc? Let me verify order: I edited lategame (2 edits + case11), duke (3 edits), Game.ts (2 edits), martian (5 edits) — THEN ran tsc (46 errors, none in my files) and vitest. Yes, all edits preceded tsc/vitest. The only thing after was the temp test file (deleted now). No source changes since. But the duke file was modified by a linter/parallel session AFTER my edit — tsc ran after that too. Good.

Wait — actually one more check: the parallel-session note said bossAI_duke_moonlord.ts was modified after my edit (the truncated diff showed the file header reorganized into sections "// 猪鲨 AI_069..." at :130 — that matches what I saw when re-reading at line 130-136 which already had the restructured header). My greps confirmed dukeFindFrame still at 232/295/532. And tsc+vitest ran after that. All green.

Now delete the temp file. Check no process holds it: pgrep for vitest/node processes referencing it — vitest exits after run. Simple rm is fine; CLAUDE.md says "删文件前先 pgrep 确认无关联进程" — let me pgrep quickly for safety.
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:10:56.385Z · glm-x-preview-260804

```
所有 6 个冒烟测试均已通过。现在我来删除临时测试文件（按照 CLAUDE.md，先执行 `pgrep`）并进行最终确认。
```


---

## 🤖 Assistant · 2026-08-19T09:10:57.564Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "pgrep -fl \"vitest|_tmp-fourgroups\" | head; echo '---'; rm ~/Project/GLM/SandboxWorld/game/tests/_tmp-fourgroups.test.ts && echo deleted",
 "description": "Verify no running process then delete temp test"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:10:57.618Z

**📎 ToolResult**

```
---
deleted

```


---

## 🤖 Assistant · 2026-08-19T09:11:02.351Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "npx vitest run tests/bossAI-lategame.test.ts tests/bossAI-dd2.test.ts tests/boss-hostile-proj-sim.test.ts tests/eoc-dash-speed.test.ts 2>&1 | tail -8; npx tsc --noEmit 2>&1 | grep -cE \"error TS\"; npx tsc --noEmit 2>&1 | grep -E \"bossAI_lategame|bossAI_duke_moonlord|bossAI_martian|src/core/Game\" | head -3; echo \"edited-files-clean\"",
 "description": "Final acceptance run: tests plus tsc",
 "timeout": 600000
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:11:26.628Z

**📎 ToolResult**

```
 ✓ tests/eoc-dash-speed.test.ts (1 test) 4ms
 ✓ tests/boss-hostile-proj-sim.test.ts (1 test) 7ms

 Test Files  4 passed (4)
      Tests  80 passed (80)
   Start at  17:11:03
   Duration  2.12s (transform 1.44s, setup 0ms, collect 7.11s, tests 91ms, environment 1ms, prepare 189ms)

47
src/core/Game.ts(8700,70): error TS2554: Expected 7 arguments, but got 8.
edited-files-clean

```


---

## 🤖 Assistant · 2026-08-19T09:11:59.326Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Hmm — now there's an error in src/core/Game.ts at line 8700: "Expected 7 arguments, but got 8" — and the total error count went from 46 to 47. Did this appear because of my edit? My edit was at ~4578-4586, not 8700. But the count changed from 46 to 47! Let me check whether this error is mine or from a parallel session's edit to Game.ts (the environment warns of parallel sessions). Let me look at line 8700 and check whether it references something I touched.
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:12:00.366Z · glm-x-preview-260804

```
在 `Game.ts:8700` 处出现了一个新错误，且错误总数从 46 变为 47 —— 我来检查一下这是我导致的，还是由并行会话的修改引起的。
```


---

## 🤖 Assistant · 2026-08-19T09:12:01.137Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '8690,8705p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Inspect Game.ts line 8700 error site"
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:12:01.206Z

**📎 ToolResult**

```
        yoyo.critChance = critTotal;
        yoyo.armorPen = this.player.equipStats.armorPen + this.player.meleeArmorPen; // ⑥
        // 配重球（counterWeight：悠悠球命中时落配重投射物，原版环绕弹的直线坠落近似）
        if (this.player.equipStats.counterWeight) {
          (yoyo as unknown as { spawnWeight?: (x: number, y: number, dmg: number) => void }).spawnWeight =
            (wx, wy, wdmg) => {
              // 配重球 = 环绕实体（AI_099_1 :64472-64610 1:1——曾直线坠落 Arrow 近似）
              const cwOwn = () => (this.player.dead ? null : this.player);
              const cwAlive = () => !yoyo.dead && (yoyo as unknown as { dead: boolean }).dead === false;
              const cwE = new CounterweightProj(wx, wy, wdmg, this.player.equipStats.kbGlove ? 4 : 2,
                556 + Math.floor(Math.random() * 6), cwOwn, cwAlive, this.player.equipStats.yoyoString);
              cwE.critChance = critTotal;
              cwE.armorPen = this.player.equipStats.armorPen + this.player.meleeArmorPen;
              this.entities.add(cwE, 'projectiles');
            };
        }

```


---

## 🤖 Assistant · 2026-08-19T09:12:15.566Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This is at line ~8700 — the counterweight (配重球) code from a different feature (yoyo combat), completely unrelated to my four edits (WoF misc[32] at ~4578). This is a parallel session's in-flight edit (the environment noted bossAI_duke_moonlord.ts was concurrently modified too). The error "Expected 7 arguments, but got 8" at (8700,70) — line 8700 is `const cwE = new CounterweightProj(wx, wy, wdmg, this.player.equipStats.kbGlove ? 4 : 2, 556 + ..., cwOwn, cwAlive, this.player.equipStats.yoyoString);` — someone is mid-edit on CounterweightProj's constructor.

My four edited files: bossAI_lategame.ts, bossAI_duke_moonlord.ts, bossAI_martian.ts — zero errors. Game.ts has 1 error but at line 8700, not my region (4578). To be certain my Game.ts edit is clean, the error is at 8700 — 4100+ lines away, in the yoyo counterweight feature. Clearly a parallel session's work-in-progress.

Let me confirm my specific edit region has no error by checking the full tsc output for any Game.ts error locations.
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:12:16.745Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "npx tsc --noEmit 2>&1 | grep \"src/core/Game.ts\" ; echo '---'; npx tsc --noEmit 2>&1 | grep -E \"bossAI_lategame|bossAI_duke_moonlord|bossAI_martian\"; echo \"my-files-clean\"",
 "description": "List all Game.ts tsc error locations",
 "timeout": 300000
}
```


---

## 👤 User(sidechain) · 2026-08-19T09:12:53.907Z

**📎 ToolResult**

```
src/core/Game.ts(8700,70): error TS2554: Expected 7 arguments, but got 8.
---
my-files-clean

```


---

## 🤖 Assistant · 2026-08-19T09:13:18.870Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: the only Game.ts error is at line 8700 — the yoyo counterweight call site (a parallel session's in-flight edit; my WoF edit is at ~4578 and produces no error). My three AI files are completely clean. The count went 46 → 47 because a parallel session edited Game.ts between my two tsc runs (the same session that reorganized bossAI_duke_moonlord.ts's header).

All four groups are complete:

1. **光女白天暴怒 expert 循环 + case11** — bossAI_lategame.ts:
   - `EMPRESS_CYCLE_P2_EXPERT = [7,2,8,11,5,2,6,4,8,12]` (10 slots, :46520-46579 num51 slot 3 inserts 11)
   - Case 1 table switch: `phase2 ? (flag2 ? EXPERT : P2) : P1`
   - New case 11 block (:47061-47151): Item_162 at start, dur = 100+(20-num17), hover (0,-350), every 3t <100t with ≤2400px gate: lance spawns at player center + (-velocity normalized)×100, aimed at player's 90t-predicted position, 12-speed convergent 919, damage num6 (9999 day-enrage / 60 phase2 / 50), 240 life; Boss_CanShootExtraAt multiplayer supplement documented as skipped (always skips main target :47324).

2. **猪鲨 FindFrame** — bossAI_duke_moonlord.ts:
   - `dukeFindFrame(e)` (:72824-72917 1:1): swim frames 0-5 (6t/frame, 5t in phase-2 hover ai0==5), frames 6/7 for ai0 1/6/2/7 by ai2<10, ai0 3/8/-1 num52=90 window (swim outside [60,80], frame 6 in-window, 7 when ai2∈(70,75)), ai0 4/9 num53=180 (swim outside [120,160], 6 in-window, 7 when ai2∈(130,155)), ai0 10-13 untouched (vanilla has no branch). Wrap gate every tick.
   - Called at end of dukeFishronAI + in the despawn early-return (vanilla FindFrame runs after AI unconditionally). Writes `e.customFrameIdx` (694 precedent; Renderer.vanillaFrameIdx:646 direct read; NPC 370 = 8 frames confirmed in vanilla-npcs.json).
   - Duke AI core untouched.

3. **WoF 三机械旗 misc[32]** — Game.ts (~4583): after `startHardmode(w)`, before LanternNight/misc[15] (vanilla order :80287-80290 broadcast precedes SetEventFlagCleared(19)): `if (!wasHard && downed_134 && downed_125 && downed_127) newText(Lang.misc(32), 50,255,130)` — wasHard is the pre-StartHardmode snapshot (vanilla eventFlag). Comment chain header updated.

4. **火星专家弹伤插值** — bossAI_martian.ts:
   - import getAttackDamageForProjectiles from ScaleStats (bossAI.ts precedent)
   - 448: `getAttackDamageForProjectiles(50, 37, e.difficulty)` (:36081)
   - 449: `(35, 30, e.difficulty)` (:36105)
   - 450: `dmg450 = (30, 25, e.difficulty)` computed once before the window (:36168-36169), shared by all 4 empty-nest launch sites
   - 435: `(35, 28, e.difficulty)` — 35×0.8 for type 387∈[381,392] (:35442-35448)

Verification:
- tsc: zero errors in my files; the single Game.ts error (line 8700) is a parallel session's yoyo-counterweight in-flight edit, ~4100 lines away from my change (count moved 46→47 between runs while I made no Game.ts edits after the first tsc).
- vitest: 4 named test files, 80 tests, all green (run twice).
- Temp smoke test (deleted after passing): 6/6 green — night+expert slot 3 → case 11 with exact spawn geometry (player-velocity-opposite 100px, +X aim toward 90t-predicted position at 12 speed); night-classic slot 3 → case 5 (no 11); duke charge frames 6/7 by ai2<10, wrap 7→0 returning to swim, 6-frame swim cycle at 6t/frame with wrap, tornado window frames 6/7; martian Remap tier values 50→37/35→30/30→25/35→28.

No l10n keys added, no CLAUDE.md-restricted changes, no dev server used. Done — write the final report.
```

</details>


---

## 🤖 Assistant · 2026-08-19T09:13:43.099Z · glm-x-preview-260804

```
四个组已全部完成并验证。Game.ts:8700 的错误属于一个并行会话中正在进行的悠悠球配重（yoyo-counterweight）修改（与我在 4583 行的 WoF 编辑相距 4100 行 —— 在我两次 `tsc` 运行之间错误数量从 46 变为 47，期间我没对 Game.ts 进行任何后续修改；我修改的三个 AI 文件完全无错误）。

## 完成报告:四组落点 + 测试

### 一、光女 expert 循环 + case11 预测光枪墙 — `src/entities/bossAI_lategame.ts`
- **expert 表**: 新增 `EMPRESS_CYCLE_P2_EXPERT = [7,2,8,11,5,2,6,4,8,12]`(NPC.cs:46520-46579,flag2 时 num51 第 3 槽插 11);case 1 选招切表 `phase2 ? (flag2 ? EXPERT : P2) : P1`。flag2 = isExpert‖白天暴怒(:46317/:46355)原有逻辑不动。
- **case 11**(:47061-47151 逐行 1:1): 开场 Item_162;时长 100+(20−num17);悬玩家上 (0,-350);每 3t(<100t 且 NPC 距玩家 ≤2400)布一杆 919 —— 布枪点 = 玩家中心 − 玩家速度单位向量 ×100(零速兜底 (0,-1)),弹向指向玩家 90t 预测位,12 速直飞(同 919 收敛实现),伤 num6(白天 9999/二阶段 60),life 240;含 :47096-47104 防御性外推死代码;Boss_CanShootExtraAt 多人补射恒跳主目标(:47324)单人无效,注释备案。状态机主链其余各 case 未动。

### 二、猪鲨 FindFrame 状态机 — `src/entities/bossAI_duke_moonlord.ts`
- 新增 `dukeFindFrame(e)`(:72824-72917 1:1),帧号直写 `e.customFrameIdx`(694 先例,Renderer `vanillaFrameIdx`:646 首行直读,NPC 370 贴图 8 帧已核):0-5 游动帶 6t/帧(ai0==5 二阶段悬浮 5t/帧)、每 tick 回卷门 `≥6→0`(张口帧 7 回悬浮首拍归 0);ai0 1/6/2/7 按 ai2<10 → 帧 6/7;ai0 3/8/-1(num52=90)窗外游动、窗内 [60,80] 帧 6(ai2∈(70,75) 帧 7);ai0 4/9(num53=180)窗外游动、窗内 [120,160] 帧 6(ai2∈(130,155) 帧 7);ai0 10-13 原版无分支保持不动。
- 调用点两处:AI 体尾 + 远距脱场早退分支前(原版 FindFrame 在 AI 后无条件逐 tick);**AI 本体逻辑零改动**。

### 三、WoF 三机械旗 misc[32] — `src/core/Game.ts`(≈:4583)
- `startHardmode(w)` 之后、灯笼夜 19/misc[15] 之前(原版序 :80287-80290 广播先于 SetEventFlagCleared(19))补:`!wasHard && downed_134 && downed_125 && downed_127 → newText(Lang.misc(32), 50,255,130)`。wasHard 即原版 eventFlag(StartHardmode 前快照);与既有机械链公告(Game.ts:4606)同文案同 API,无 l10n 新键。

### 四、火星专家弹伤插值 — `src/entities/bossAI_martian.ts`
- import `getAttackDamageForProjectiles`(bossAI.ts 先例),四处换算:
  - 448 火炮弹 `getAttackDamageForProjectiles(50, 37, e.difficulty)`(:36081)
  - 449 激光 `(35, 30, e.difficulty)`(:36105)
  - 450 空巢导弹 ×4 发射点共用 `dmg450 = (30, 25, e.difficulty)`,窗检前一次算定(:36168-36169 同位)
  - 435 特斯拉电球 `(35, 28, e.difficulty)`(35×0.8,type 387∈[381,392],:35442-35448)

### 测试
- `npx tsc --noEmit`:三个 AI 文件 + Game.ts 我的改动区**零错**;全仓 47 错均为基线/并行会话(唯一 Game.ts 错在 :8700 配重球构造参,系并行会话半成品,与本次无关)。
- `npx vitest run tests/bossAI-lategame.test.ts tests/bossAI-dd2.test.ts tests/boss-hostile-proj-sim.test.ts tests/eoc-dash-speed.test.ts` → **4 文件 80 测试全绿**(跑两遍确认)。
- 一次性冒烟探针(6/6 绿后已删,删前 pgrep 无关联进程):夜间 expert 二阶段第 3 拍确实选 11 且布枪几何精确(速度反向 100px 出生、朝 90t 预测位 12 速);夜间经典同槽走 5 不进 11;猪鲨冲撞 6/7 帧、7→0 回卷、游动六帶 6t/帧循环、龙卷窗 6/7 帧;火星四档 Remap 值逐个断言。
```
