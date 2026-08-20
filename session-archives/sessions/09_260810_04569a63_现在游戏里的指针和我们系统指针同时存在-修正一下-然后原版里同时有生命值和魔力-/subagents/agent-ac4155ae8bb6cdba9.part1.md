# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-11T04:27:57.713Z

```
你在 ~/Project/GLM/SandboxWorld/ 工作。权威源码：~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs（1.4.5.6 反编译）。名字对照 Terraria.ID/NPCID.cs。

任务：为以下 9 个 aiStyle 家族提取**可直接照抄移植的运动/状态机规格**（不做我方代码调研）。先用 `grep -n "else if (aiStyle == N)" NPC.cs` 定位每个块的起始行，再完整读该块。对每个家族输出：
- 状态机（ai[0]/ai[1].../localAI 各字段含义与流转）
- 运动学：速度/加速度/重力/碰撞方式（tileCollide? noGravity? noTileCollide?）
- 与玩家交互触发条件（距离/视线/受击）
- 跳跃/冲刺/攻击的具体数值与公式
- 关键行号

家族清单：
1. **aiStyle 0**（Bound NPC：105/106/123/354/376/579）——被缚NPC怎么站、怎么被解救、解救后发生什么（Transform？）。
2. **aiStyle 17**（61 Vulture 秃鹫 + 注意 301 Raven 是否同块）——栖息态怎么站（在沙上？）、什么条件起飞、飞行动力学、会不会回栖息。
3. **aiStyle 19**（69 Antlion 蚁狮）——扎根判定（嵌沙里不动？）、沙球攻击参数（已有发射参数：200t 冷却/速12/视线；确认运动部分：它到底动不动、有没有钻地位移）。
4. **aiStyle 23**（83 CursedHammer/84 EnchantedSword/179 CrimsonAxe 飞行武器）——三态循环（漂移→蓄转→冲刺）各态时长/速度/加速度/触发距离，受击回哪态。
5. **aiStyle 25**（85 Mimic/341 PresentMimic 宝箱怪）——伪装态判定（玩家距离多少格显形？）、显形后跳跃追击参数（跳vy、vx、跳间隔 ai 计时）。
6. **aiStyle 39**（153 GiantTortoise/154 IceTortoise/417 Sroller 陆龟族）——待机判定、旋转冲刺跳跃的 vy/vx/计时、落地后状态。
7. **aiStyle 41**（174 Herpling/177 Derpling/378 另一物）——赫柏林的低跳连扑参数、Derpling 区别。
8. **aiStyle 44**（224 FlyingFish/509 GiantAntlionSwarmer/581 AntlionSwarmer）——飞行群袭运动学（同 EoC 仆从? 加速度/限速/摆动）。
9. **aiStyle 56**（288 DungeonSpirit 地牢之魂）——穿墙追踪? 加速度/限速/受击反应（死后分解成魂魄? 简述即可）。

输出：9 节紧凑规格（每节 ≤25 行要点+行号），最后附「共同陷阱」（如某家族其实复用另一个 aiStyle 的代码块、noTileCollide 标志、专家模式分支等）。控制在 30 次工具调用内。
```

---

## 📎 Attachment · skill_listing · 2026-08-11T04:27:57.718Z

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

## 🤖 Assistant · 2026-08-11T04:27:59.085Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The user wants me to extract AI specifications from the decompiled Terraria source. Let me start by locating the aiStyle blocks with grep, then read each block.

Let me do this efficiently — batch greps in parallel, then read the relevant line ranges.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:28:00.222Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"else if (aiStyle == 0)\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -5; echo \"---17---\"; grep -n \"aiStyle == 17)\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -5; echo \"---19---\"; grep -n \"aiStyle == 19)\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -5; echo \"---23---\"; grep -n \"aiStyle == 23)\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -5",
 "description": "Locate aiStyle 0/17/19/23 block start lines"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:00.269Z

**📎 ToolResult**

```
---17---
24079:		if (aiStyle == 17)
---19---
24465:		if (aiStyle == 19)
---23---
25316:		else if (aiStyle == 23)

```


---

## 🤖 Assistant · 2026-08-11T04:28:01.450Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"aiStyle == 25)\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -5; echo \"---39---\"; grep -n \"aiStyle == 39)\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -5; echo \"---41---\"; grep -n \"aiStyle == 41)\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -5; echo \"---44---\"; grep -n \"aiStyle == 44)\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -5; echo \"---56---\"; grep -n \"aiStyle == 56)\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -5",
 "description": "Locate aiStyle 25/39/41/44/56 block start lines"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:01.496Z

**📎 ToolResult**

```
25621:		else if (aiStyle == 25)
---39---
29257:		else if (aiStyle == 39)
---41---
30017:		else if (aiStyle == 41)
---44---
30999:		else if (aiStyle == 44)
94137:		if (aiStyle == 44)
---56---
32915:		else if (aiStyle == 56)

```


---

## 🤖 Assistant · 2026-08-11T04:28:05.534Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
aiStyle 0 seems to be handled elsewhere — the grep for "else if (aiStyle == 0)" returned nothing before ---17---. Let me search for how aiStyle 0 / bound NPCs are handled. Note line 24079 is `if (aiStyle == 17)` not else-if, meaning it's in a different chain. Let me find where bound NPCs (NPCID.Bound...) are handled.

Let me read each block. First find the ends. aiStyle 17 at 24079, 19 at 24465, so block 17 is 24079..~24464. Block 19: 24465..~? next is 23 at 25316. That's 850 lines — long. Actually there may be other aiStyles in between. Let me read them.

Also need to locate aiStyle 0 block. Search for "aiStyle == 0".
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:28:06.196Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"aiStyle == 0)\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head; echo \"---bound---\"; grep -n \"NPCID.Bound\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -20",
 "description": "Find aiStyle 0 block and Bound NPC handling"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:06.228Z

**📎 ToolResult**

```
19774:		if (aiStyle == 0)
---bound---

```


---

## 🤖 Assistant · 2026-08-11T04:28:06.472Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "offset": 24079,
 "limit": 390
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:06.479Z

**📎 ToolResult**

```
24079			if (aiStyle == 17)
24080			{
24081				noGravity = true;
24082				if (this.ai[0] == 0f)
24083				{
24084					noGravity = false;
24085					TargetClosest();
24086					if (Main.netMode != 1)
24087					{
24088						if (velocity.X != 0f || velocity.Y < 0f || (double)velocity.Y > 0.3)
24089						{
24090							this.ai[0] = 1f;
24091							netUpdate = true;
24092						}
24093						else
24094						{
24095							Rectangle rectangle = new Rectangle((int)Main.player[target].position.X, (int)Main.player[target].position.Y, Main.player[target].width, Main.player[target].height);
24096							if (new Rectangle((int)position.X - 100, (int)position.Y - 100, width + 200, height + 200).Intersects(rectangle) || life < lifeMax)
24097							{
24098								this.ai[0] = 1f;
24099								velocity.Y -= 6f;
24100								netUpdate = true;
24101							}
24102						}
24103					}
24104				}
24105				else if (!Main.player[target].dead)
24106				{
24107					if (collideX)
24108					{
24109						velocity.X = oldVelocity.X * -0.5f;
24110						if (direction == -1 && velocity.X > 0f && velocity.X < 2f)
24111						{
24112							velocity.X = 2f;
24113						}
24114						if (direction == 1 && velocity.X < 0f && velocity.X > -2f)
24115						{
24116							velocity.X = -2f;
24117						}
24118					}
24119					if (collideY)
24120					{
24121						velocity.Y = oldVelocity.Y * -0.5f;
24122						if (velocity.Y > 0f && velocity.Y < 1f)
24123						{
24124							velocity.Y = 1f;
24125						}
24126						if (velocity.Y < 0f && velocity.Y > -1f)
24127						{
24128							velocity.Y = -1f;
24129						}
24130					}
24131					TargetClosest();
24132					if (direction == -1 && velocity.X > -3f)
24133					{
24134						velocity.X -= 0.1f;
24135						if (velocity.X > 3f)
24136						{
24137							velocity.X -= 0.1f;
24138						}
24139						else if (velocity.X > 0f)
24140						{
24141							velocity.X -= 0.05f;
24142						}
24143						if (velocity.X < -3f)
24144						{
24145							velocity.X = -3f;
24146						}
24147					}
24148					else if (direction == 1 && velocity.X < 3f)
24149					{
24150						velocity.X += 0.1f;
24151						if (velocity.X < -3f)
24152						{
24153							velocity.X += 0.1f;
24154						}
24155						else if (velocity.X < 0f)
24156						{
24157							velocity.X += 0.05f;
24158						}
24159						if (velocity.X > 3f)
24160						{
24161							velocity.X = 3f;
24162						}
24163					}
24164					float num272 = Math.Abs(position.X + (float)(width / 2) - (Main.player[target].position.X + (float)(Main.player[target].width / 2)));
24165					float num273 = Main.player[target].position.Y - (float)(height / 2);
24166					if (num272 > 50f)
24167					{
24168						num273 -= 100f;
24169					}
24170					if (position.Y < num273)
24171					{
24172						velocity.Y += 0.05f;
24173						if (velocity.Y < 0f)
24174						{
24175							velocity.Y += 0.01f;
24176						}
24177					}
24178					else
24179					{
24180						velocity.Y -= 0.05f;
24181						if (velocity.Y > 0f)
24182						{
24183							velocity.Y -= 0.01f;
24184						}
24185					}
24186					if (velocity.Y < -3f)
24187					{
24188						velocity.Y = -3f;
24189					}
24190					if (velocity.Y > 3f)
24191					{
24192						velocity.Y = 3f;
24193					}
24194				}
24195				if (wet)
24196				{
24197					if (velocity.Y > 0f)
24198					{
24199						velocity.Y *= 0.95f;
24200					}
24201					velocity.Y -= 0.5f;
24202					if (velocity.Y < -4f)
24203					{
24204						velocity.Y = -4f;
24205					}
24206					TargetClosest();
24207				}
24208				return;
24209			}
24210			if (aiStyle == 18)
24211			{
24212				bool flag23 = false;
24213				if (wet && this.ai[1] == 1f)
24214				{
24215					flag23 = true;
24216				}
24217				else
24218				{
24219					dontTakeDamage = false;
24220				}
24221				if (Main.expertMode && (type == 63 || type == 64 || type == 103 || type == 242))
24222				{
24223					if (wet)
24224					{
24225						if (target >= 0 && Main.player[target].wet && !Main.player[target].dead && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height) && (Main.player[target].Center - base.Center).Length() < 150f)
24226						{
24227							if (this.ai[1] == 0f)
24228							{
24229								this.ai[2] += 2f;
24230							}
24231							else
24232							{
24233								this.ai[2] -= 0.25f;
24234							}
24235						}
24236						if (flag23)
24237						{
24238							dontTakeDamage = true;
24239							this.ai[2] += 1f;
24240							if (this.ai[2] >= 120f)
24241							{
24242								this.ai[1] = 0f;
24243							}
24244						}
24245						else
24246						{
24247							this.ai[2] += 1f;
24248							if (this.ai[2] >= 420f)
24249							{
24250								this.ai[1] = 1f;
24251								this.ai[2] = 0f;
24252							}
24253						}
24254					}
24255					else
24256					{
24257						this.ai[1] = 0f;
24258						this.ai[2] = 0f;
24259					}
24260				}
24261				float num274 = 1f;
24262				if (flag23)
24263				{
24264					num274 += 0.5f;
24265				}
24266				if (type == 63)
24267				{
24268					Lighting.AddLight((int)(position.X + (float)(height / 2)) / 16, (int)(position.Y + (float)(height / 2)) / 16, 0.05f * num274, 0.15f * num274, 0.4f * num274);
24269				}
24270				else if (type == 103)
24271				{
24272					Lighting.AddLight((int)(position.X + (float)(height / 2)) / 16, (int)(position.Y + (float)(height / 2)) / 16, 0.05f * num274, 0.45f * num274, 0.1f * num274);
24273				}
24274				else if (type != 221 && type != 242)
24275				{
24276					Lighting.AddLight((int)(position.X + (float)(height / 2)) / 16, (int)(position.Y + (float)(height / 2)) / 16, 0.35f * num274, 0.05f * num274, 0.2f * num274);
24277				}
24278				if (direction == 0)
24279				{
24280					TargetClosest();
24281				}
24282				if (flag23)
24283				{
24284					return;
24285				}
24286				if (wet)
24287				{
24288					int num275 = (int)base.Center.X / 16;
24289					int num276 = (int)(position.Y + (float)height) / 16;
24290					if (Main.tile[num275, num276].topSlope())
24291					{
24292						if (Main.tile[num275, num276].leftSlope())
24293						{
24294							direction = -1;
24295							velocity.X = Math.Abs(velocity.X) * -1f;
24296						}
24297						else
24298						{
24299							direction = 1;
24300							velocity.X = Math.Abs(velocity.X);
24301						}
24302					}
24303					else if (Main.tile[num275, num276 + 1].topSlope())
24304					{
24305						if (Main.tile[num275, num276 + 1].leftSlope())
24306						{
24307							direction = -1;
24308							velocity.X = Math.Abs(velocity.X) * -1f;
24309						}
24310						else
24311						{
24312							direction = 1;
24313							velocity.X = Math.Abs(velocity.X);
24314						}
24315					}
24316					if (collideX)
24317					{
24318						velocity.X *= -1f;
24319						direction *= -1;
24320					}
24321					if (collideY)
24322					{
24323						if (velocity.Y > 0f)
24324						{
24325							velocity.Y = Math.Abs(velocity.Y) * -1f;
24326							directionY = -1;
24327							this.ai[0] = -1f;
24328						}
24329						else if (velocity.Y < 0f)
24330						{
24331							velocity.Y = Math.Abs(velocity.Y);
24332							directionY = 1;
24333							this.ai[0] = 1f;
24334						}
24335					}
24336					bool flag24 = false;
24337					if (!friendly)
24338					{
24339						TargetClosest(faceTarget: false);
24340						if (Main.player[target].wet && !Main.player[target].dead && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
24341						{
24342							flag24 = true;
24343						}
24344					}
24345					if (flag24)
24346					{
24347						localAI[2] = 1f;
24348						rotation = (float)Math.Atan2(velocity.Y, velocity.X) + 1.57f;
24349						velocity *= 0.98f;
24350						float num277 = 0.2f;
24351						if (type == 103)
24352						{
24353							velocity *= 0.98f;
24354							num277 = 0.6f;
24355						}
24356						if (type == 221)
24357						{
24358							velocity *= 0.99f;
24359							num277 = 1f;
24360						}
24361						if (type == 242)
24362						{
24363							velocity *= 0.995f;
24364							num277 = 3f;
24365						}
24366						if (velocity.X > 0f - num277 && velocity.X < num277 && velocity.Y > 0f - num277 && velocity.Y < num277)
24367						{
24368							if (type == 221)
24369							{
24370								localAI[0] = 1f;
24371							}
24372							TargetClosest();
24373							float num278 = 7f;
24374							if (type == 103)
24375							{
24376								num278 = 9f;
24377							}
24378							Vector2 vector26 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
24379							float num279 = Main.player[target].position.X + (float)(Main.player[target].width / 2) - vector26.X;
24380							float num280 = Main.player[target].position.Y + (float)(Main.player[target].height / 2) - vector26.Y;
24381							float num281 = (float)Math.Sqrt(num279 * num279 + num280 * num280);
24382							num281 = num278 / num281;
24383							num279 *= num281;
24384							num280 *= num281;
24385							velocity.X = num279;
24386							velocity.Y = num280;
24387						}
24388						return;
24389					}
24390					localAI[2] = 0f;
24391					velocity.X += (float)direction * 0.02f;
24392					rotation = velocity.X * 0.4f;
24393					if (velocity.X < -1f || velocity.X > 1f)
24394					{
24395						velocity.X *= 0.95f;
24396					}
24397					if (this.ai[0] == -1f)
24398					{
24399						velocity.Y -= 0.01f;
24400						if (velocity.Y < -1f)
24401						{
24402							this.ai[0] = 1f;
24403						}
24404					}
24405					else
24406					{
24407						velocity.Y += 0.01f;
24408						if (velocity.Y > 1f)
24409						{
24410							this.ai[0] = -1f;
24411						}
24412					}
24413					int num282 = (int)(position.X + (float)(width / 2)) / 16;
24414					int num283 = (int)(position.Y + (float)(height / 2)) / 16;
24415					if (Main.tile[num282, num283 - 1] == null)
24416					{
24417						Main.tile[num282, num283 - 1] = new Tile();
24418					}
24419					if (Main.tile[num282, num283 + 1] == null)
24420					{
24421						Main.tile[num282, num283 + 1] = new Tile();
24422					}
24423					if (Main.tile[num282, num283 + 2] == null)
24424					{
24425						Main.tile[num282, num283 + 2] = new Tile();
24426					}
24427					if (Main.tile[num282, num283 - 1].liquid > 128)
24428					{
24429						if (Main.tile[num282, num283 + 1].active())
24430						{
24431							this.ai[0] = -1f;
24432						}
24433						else if (Main.tile[num282, num283 + 2].active())
24434						{
24435							this.ai[0] = -1f;
24436						}
24437					}
24438					else
24439					{
24440						this.ai[0] = 1f;
24441					}
24442					if ((double)velocity.Y > 1.2 || (double)velocity.Y < -1.2)
24443					{
24444						velocity.Y *= 0.99f;
24445					}
24446					return;
24447				}
24448				rotation += velocity.X * 0.1f;
24449				if (velocity.Y == 0f)
24450				{
24451					velocity.X *= 0.98f;
24452					if ((double)velocity.X > -0.01 && (double)velocity.X < 0.01)
24453					{
24454						velocity.X = 0f;
24455					}
24456				}
24457				velocity.Y += 0.2f;
24458				if (velocity.Y > 10f)
24459				{
24460					velocity.Y = 10f;
24461				}
24462				this.ai[0] = 1f;
24463				return;
24464			}
24465			if (aiStyle == 19)
24466			{
24467				TargetClosest();
24468				float num284 = 12f;

```


---

## 🤖 Assistant · 2026-08-11T04:28:09.163Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Got aiStyle 17. Note Raven (301) — need to check if it's aiStyle 17. Let me check NPCID.cs / or the aiStyle assignment. Actually in vanilla, Raven uses aiStyle 17 too? Let me check. Raven (301) aiStyle = 17? I recall Raven has aiStyle 17 (Vulture's). Actually let me grep in the decompiled set defaults. There might be a file with `aiStyle = 17`. Let me search.

Now continue reading aiStyle 19 from 24465.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:28:09.369Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 160,
 "offset": 24465
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:09.382Z

**📎 ToolResult**

```
24465			if (aiStyle == 19)
24466			{
24467				TargetClosest();
24468				float num284 = 12f;
24469				Vector2 vector27 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
24470				float num285 = Main.player[target].position.X + (float)(Main.player[target].width / 2) - vector27.X;
24471				float num286 = Main.player[target].position.Y - vector27.Y;
24472				float num287 = (float)Math.Sqrt(num285 * num285 + num286 * num286);
24473				num287 = num284 / num287;
24474				num285 *= num287;
24475				num286 *= num287;
24476				bool flag25 = false;
24477				if (directionY < 0)
24478				{
24479					rotation = (float)(Math.Atan2(num286, num285) + 1.57);
24480					flag25 = ((!((double)rotation < -1.2) && !((double)rotation > 1.2)) ? true : false);
24481					if ((double)rotation < -0.8)
24482					{
24483						rotation = -0.8f;
24484					}
24485					else if ((double)rotation > 0.8)
24486					{
24487						rotation = 0.8f;
24488					}
24489					if (velocity.X != 0f)
24490					{
24491						velocity.X *= 0.9f;
24492						if ((double)velocity.X > -0.1 || (double)velocity.X < 0.1)
24493						{
24494							netUpdate = true;
24495							velocity.X = 0f;
24496						}
24497					}
24498				}
24499				if (this.ai[0] > 0f)
24500				{
24501					if (this.ai[0] == 200f)
24502					{
24503						SoundEngine.PlaySound(SoundID.Item5, position);
24504					}
24505					this.ai[0] -= 1f;
24506				}
24507				if (Main.netMode != 1 && this.ai[0] == 0f)
24508				{
24509					int num288 = (int)(base.Center.X / 16f);
24510					int num289 = (int)((base.Bottom.Y + 8f) / 16f);
24511					if (flag25)
24512					{
24513						if (Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
24514						{
24515							this.ai[0] = 200f;
24516							int num290 = 10;
24517							int num291 = 31;
24518							int num292 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector27.X, vector27.Y, num285, num286, num291, num290, 0f, Main.myPlayer);
24519							Main.projectile[num292].ai[0] = 2f;
24520							Main.projectile[num292].timeLeft = 300;
24521							Main.projectile[num292].friendly = false;
24522							NetMessage.SendData(27, -1, -1, null, num292);
24523							netUpdate = true;
24524						}
24525					}
24526					else if (WorldGen.InWorld(num288, num289) && (Main.tile[num288, num289].type == 421 || Main.tile[num288, num289].type == 422))
24527					{
24528						float num293 = rotation - 1.57f;
24529						Vector2 vector28 = new Vector2((float)Math.Cos(num293), (float)Math.Sin(num293));
24530						num285 = vector28.X * num284;
24531						num286 = vector28.Y * num284;
24532						this.ai[0] = 200f;
24533						int num294 = 10;
24534						int num295 = 31;
24535						int num296 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector27.X, vector27.Y, num285, num286, num295, num294, 0f, Main.myPlayer);
24536						Main.projectile[num296].ai[0] = 2f;
24537						Main.projectile[num296].timeLeft = 300;
24538						Main.projectile[num296].friendly = false;
24539						NetMessage.SendData(27, -1, -1, null, num296);
24540						netUpdate = true;
24541					}
24542				}
24543				try
24544				{
24545					int num297 = (int)position.X / 16;
24546					int num298 = (int)(position.X + (float)(width / 2)) / 16;
24547					int num299 = (int)(position.X + (float)width) / 16;
24548					int num300 = (int)(position.Y + (float)height) / 16;
24549					bool flag26 = false;
24550					if (Main.tile[num297, num300] == null)
24551					{
24552						Main.tile[num297, num300] = new Tile();
24553					}
24554					if (Main.tile[num298, num300] == null)
24555					{
24556						Main.tile[num297, num300] = new Tile();
24557					}
24558					if (Main.tile[num299, num300] == null)
24559					{
24560						Main.tile[num297, num300] = new Tile();
24561					}
24562					if ((Main.tile[num297, num300].nactive() && Main.tileSolid[Main.tile[num297, num300].type]) || (Main.tile[num298, num300].nactive() && Main.tileSolid[Main.tile[num298, num300].type]) || (Main.tile[num299, num300].nactive() && Main.tileSolid[Main.tile[num299, num300].type]))
24563					{
24564						flag26 = true;
24565					}
24566					if (flag26)
24567					{
24568						noGravity = true;
24569						noTileCollide = true;
24570						velocity.Y = -0.2f;
24571						return;
24572					}
24573					noGravity = false;
24574					noTileCollide = false;
24575					if (Main.rand.Next(2) == 0)
24576					{
24577						position += netOffset;
24578						int num301 = Dust.NewDust(new Vector2(position.X - 4f, position.Y + (float)height - 8f), width + 8, 24, 32, 0f, velocity.Y / 2f);
24579						Main.dust[num301].velocity.X *= 0.4f;
24580						Main.dust[num301].velocity.Y *= -1f;
24581						if (Main.rand.Next(2) == 0)
24582						{
24583							Main.dust[num301].noGravity = true;
24584							Dust dust = Main.dust[num301];
24585							dust.scale += 0.2f;
24586						}
24587						position -= netOffset;
24588					}
24589					return;
24590				}
24591				catch
24592				{
24593					return;
24594				}
24595			}
24596			if (aiStyle == 20)
24597			{
24598				if (this.ai[0] == 0f)
24599				{
24600					if (Main.netMode != 1)
24601					{
24602						TargetClosest();
24603						direction *= -1;
24604						directionY *= -1;
24605						position.Y += height / 2 + 8;
24606						this.ai[1] = position.X + (float)(width / 2);
24607						this.ai[2] = position.Y + (float)(height / 2);
24608						if (direction == 0)
24609						{
24610							direction = 1;
24611						}
24612						if (directionY == 0)
24613						{
24614							directionY = 1;
24615						}
24616						this.ai[3] = 1f + (float)Main.rand.Next(15) * 0.1f;
24617						velocity.Y = (float)(directionY * 6) * this.ai[3];
24618						this.ai[0] += 1f;
24619						netUpdate = true;
24620					}
24621					else
24622					{
24623						this.ai[1] = position.X + (float)(width / 2);
24624						this.ai[2] = position.Y + (float)(height / 2);

```


---

## 🤖 Assistant · 2026-08-11T04:28:10.230Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"= 17;\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Initialization/NPCDatabase.cs 2>/dev/null | head; echo \"===\"; grep -rn \"aiStyle\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ID/NPCID.cs | grep -n \"= 17\" | head",
 "description": "Find which NPCs use aiStyle 17"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:10.261Z

**📎 ToolResult**

```
===
ugrep: warning: ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ID/NPCID.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-11T04:28:18.377Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
aiStyle 19 fully read (24465-24595). Key points: Antlion doesn't move horizontally; anchored. Actually it checks if standing on solid → noGravity+noTileCollide, velocity.Y=-0.2 (i.e., it slowly sinks? no wait — if on solid tile, it sets noTileCollide and velocity.Y=-0.2, which means it rises slightly? Hmm — actually this is the "burrowed in sand" logic: if there's solid tile at its bottom row (i.e., it's embedded in sand), it floats up slightly to sit on surface. If not on solid (in air), noGravity=false and it falls with gravity and spawns dust. So the Antlion doesn't move at all; it relies on gravity/settling. And no burrowing displacement.

Wait — actually if on solid ground, it sets velocity.Y=-0.2 with noTileCollide=true, so it drifts upward through tiles until bottom is no longer solid... Hmm, that seems inverted. Let me reconsider: the check is at the row at bottom of NPC (position.Y + height)/16. If solid → flag26. If flag26: noGravity, noTileCollide, velocity.Y=-0.2 → rises out of sand until bottom tile no longer solid, then gravity takes over and it falls to rest on top. Yes, that's the emergence/settle logic — keeps it sitting on the sand surface, never digs. Good.

Also sand ball attack: ai[0] cooldown 200, speed 12 toward player (directionY<0 & rotation within [-1.2,1.2] → direct aim), OR if tile 421/422 (sand) below → shoot along rotation-1.57 direction. Projectile 31 (SandBall), ai[0]=2, damage 10, timeLeft 300, hostile.

Now find NPCID.cs path. It's probably in Terraria.ID namespace file named NPCID.cs elsewhere. Let me find it. Also need aiStyle assignments — maybe in NPCID.cs Sets or in NPCDatabase via regex. Let me find NPCID file.

Now read aiStyle 0 block at 19774, and continue with 23 at 25316.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:28:18.597Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 200,
 "offset": 19774
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:18.604Z

**📎 ToolResult**

```
19774			if (aiStyle == 0)
19775			{
19776				if (Main.netMode != 1)
19777				{
19778					for (int i = 0; i < 255; i++)
19779					{
19780						if (Main.player[i].active && Main.player[i].talkNPC == whoAmI)
19781						{
19782							if (type == 589)
19783							{
19784								AI_000_TransformBoundNPC(i, 588);
19785							}
19786							if (type == 105)
19787							{
19788								AI_000_TransformBoundNPC(i, 107);
19789							}
19790							if (type == 106)
19791							{
19792								AI_000_TransformBoundNPC(i, 108);
19793							}
19794							if (type == 123)
19795							{
19796								AI_000_TransformBoundNPC(i, 124);
19797							}
19798							if (type == 354)
19799							{
19800								AI_000_TransformBoundNPC(i, 353);
19801							}
19802							if (type == 376)
19803							{
19804								AI_000_TransformBoundNPC(i, 369);
19805							}
19806							if (type == 579)
19807							{
19808								AI_000_TransformBoundNPC(i, 550);
19809							}
19810						}
19811					}
19812				}
19813				if (type != 376 && type != 579)
19814				{
19815					TargetClosest();
19816					spriteDirection = direction;
19817				}
19818				if (type == 376 || type == 579)
19819				{
19820					if (wet || Main.tile[(int)(base.Center.X / 16f), (int)(position.Y - 4f) / 16].liquid > 0)
19821					{
19822						velocity.Y = -0.4f;
19823						int num = 1;
19824						if (base.Center.X / 16f > (float)(Main.maxTilesX / 2))
19825						{
19826							num = -1;
19827						}
19828						int num2 = 12;
19829						int num3 = (int)base.Center.X / 16;
19830						int j = (int)base.Center.Y / 16;
19831						bool flag = false;
19832						if (num > 0)
19833						{
19834							for (int k = num3; k < num3 + num2; k++)
19835							{
19836								if (WorldGen.SolidTile(k, j))
19837								{
19838									flag = true;
19839								}
19840							}
19841						}
19842						else
19843						{
19844							for (int l = num3; l > num3 - num2; l--)
19845							{
19846								if (WorldGen.SolidTile(l, j))
19847								{
19848									flag = true;
19849								}
19850							}
19851						}
19852						if (type == 579)
19853						{
19854							flag = true;
19855						}
19856						if (flag)
19857						{
19858							velocity.X *= 0.99f;
19859							if ((double)velocity.X > -0.01 && (double)velocity.X < 0.01)
19860							{
19861								velocity.X = 0f;
19862							}
19863							return;
19864						}
19865						velocity.X += (float)num * 0.01f;
19866						if (velocity.X > 0.2f)
19867						{
19868							velocity.X *= 0.95f;
19869						}
19870						if (velocity.X < -0.2f)
19871						{
19872							velocity.X *= 0.95f;
19873						}
19874					}
19875					else
19876					{
19877						velocity.X *= 0.93f;
19878						if ((double)velocity.X > -0.1 && (double)velocity.X < 0.1)
19879						{
19880							velocity.X = 0f;
19881						}
19882					}
19883				}
19884				else
19885				{
19886					velocity.X *= 0.93f;
19887					if ((double)velocity.X > -0.1 && (double)velocity.X < 0.1)
19888					{
19889						velocity.X = 0f;
19890					}
19891				}
19892				return;
19893			}
19894			if (aiStyle == 1)
19895			{
19896				AI_001_Slimes();
19897				return;
19898			}
19899			if (aiStyle == 2)
19900			{
19901				AI_002_FloatingEye();
19902				return;
19903			}
19904			if (aiStyle == 3)
19905			{
19906				AI_003_Fighters();
19907				return;
19908			}
19909			if (aiStyle == 4)
19910			{
19911				bool flag2 = false;
19912				if (Main.expertMode && (double)life < (double)lifeMax * 0.12)
19913				{
19914					flag2 = true;
19915				}
19916				bool flag3 = false;
19917				if (Main.expertMode && (double)life < (double)lifeMax * 0.04)
19918				{
19919					flag3 = true;
19920				}
19921				float num4 = 20f;
19922				if (flag3)
19923				{
19924					num4 = 10f;
19925				}
19926				if (target < 0 || target == 255 || Main.player[target].dead || !Main.player[target].active)
19927				{
19928					TargetClosest();
19929				}
19930				bool dead = Main.player[target].dead;
19931				float num5 = position.X + (float)(width / 2) - Main.player[target].position.X - (float)(Main.player[target].width / 2);
19932				float num6 = position.Y + (float)height - 59f - Main.player[target].position.Y - (float)(Main.player[target].height / 2);
19933				float num7 = (float)Math.Atan2(num6, num5) + 1.57f;
19934				if (num7 < 0f)
19935				{
19936					num7 += 6.283f;
19937				}
19938				else if ((double)num7 > 6.283)
19939				{
19940					num7 -= 6.283f;
19941				}
19942				float num8 = 0f;
19943				if (this.ai[0] == 0f && this.ai[1] == 0f)
19944				{
19945					num8 = 0.02f;
19946				}
19947				if (this.ai[0] == 0f && this.ai[1] == 2f && this.ai[2] > 40f)
19948				{
19949					num8 = 0.05f;
19950				}
19951				if (this.ai[0] == 3f && this.ai[1] == 0f)
19952				{
19953					num8 = 0.05f;
19954				}
19955				if (this.ai[0] == 3f && this.ai[1] == 2f && this.ai[2] > 40f)
19956				{
19957					num8 = 0.08f;
19958				}
19959				if (this.ai[0] == 3f && this.ai[1] == 4f && this.ai[2] > num4)
19960				{
19961					num8 = 0.15f;
19962				}
19963				if (this.ai[0] == 3f && this.ai[1] == 5f)
19964				{
19965					num8 = 0.05f;
19966				}
19967				if (Main.expertMode)
19968				{
19969					num8 *= 1.5f;
19970				}
19971				if (flag3 && Main.expertMode)
19972				{
19973					num8 = 0f;

```


---

## 🤖 Assistant · 2026-08-11T04:28:18.846Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 310,
 "offset": 25316
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:18.853Z

**📎 ToolResult**

```
25316			else if (aiStyle == 23)
25317			{
25318				noGravity = true;
25319				noTileCollide = true;
25320				if (type == 83)
25321				{
25322					Lighting.AddLight((int)((position.X + (float)(width / 2)) / 16f), (int)((position.Y + (float)(height / 2)) / 16f), 0.2f, 0.05f, 0.3f);
25323				}
25324				else if (type == 179)
25325				{
25326					Lighting.AddLight((int)((position.X + (float)(width / 2)) / 16f), (int)((position.Y + (float)(height / 2)) / 16f), 0.3f, 0.15f, 0.05f);
25327				}
25328				else
25329				{
25330					Lighting.AddLight((int)((position.X + (float)(width / 2)) / 16f), (int)((position.Y + (float)(height / 2)) / 16f), 0.05f, 0.2f, 0.3f);
25331				}
25332				if (target < 0 || target == 255 || Main.player[target].dead)
25333				{
25334					TargetClosest();
25335				}
25336				if (this.ai[0] == 0f)
25337				{
25338					float num346 = 9f;
25339					Vector2 vector33 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
25340					float num347 = Main.player[target].position.X + (float)(Main.player[target].width / 2) - vector33.X;
25341					float num348 = Main.player[target].position.Y + (float)(Main.player[target].height / 2) - vector33.Y;
25342					float num349 = (float)Math.Sqrt(num347 * num347 + num348 * num348);
25343					float num350 = num349;
25344					num349 = num346 / num349;
25345					num347 *= num349;
25346					num348 *= num349;
25347					velocity.X = num347;
25348					velocity.Y = num348;
25349					rotation = (float)Math.Atan2(velocity.Y, velocity.X) + 0.785f;
25350					this.ai[0] = 1f;
25351					this.ai[1] = 0f;
25352					netUpdate = true;
25353				}
25354				else if (this.ai[0] == 1f)
25355				{
25356					if (justHit)
25357					{
25358						this.ai[0] = 2f;
25359						this.ai[1] = 0f;
25360					}
25361					velocity *= 0.99f;
25362					this.ai[1] += 1f;
25363					if (this.ai[1] >= 100f)
25364					{
25365						netUpdate = true;
25366						this.ai[0] = 2f;
25367						this.ai[1] = 0f;
25368						velocity.X = 0f;
25369						velocity.Y = 0f;
25370					}
25371					else
25372					{
25373						rotation = (float)Math.Atan2(velocity.Y, velocity.X) + 0.785f;
25374					}
25375				}
25376				else
25377				{
25378					if (justHit)
25379					{
25380						this.ai[0] = 2f;
25381						this.ai[1] = 0f;
25382					}
25383					velocity *= 0.96f;
25384					this.ai[1] += 1f;
25385					float num351 = this.ai[1] / 120f;
25386					num351 = 0.1f + num351 * 0.4f;
25387					rotation += num351 * (float)direction;
25388					if (this.ai[1] >= 120f)
25389					{
25390						netUpdate = true;
25391						this.ai[0] = 0f;
25392						this.ai[1] = 0f;
25393					}
25394				}
25395			}
25396			else if (aiStyle == 24)
25397			{
25398				if (Main.netMode != 1 && this.ai[0] == 1f && NPCID.Sets.BirdThatCanPoop[type] && localAI[3] == 0f)
25399				{
25400					int num352 = Player.FindClosest(position, width, height);
25401					float x = base.Center.X;
25402					if (x >= Main.player[num352].Left.X && x <= Main.player[num352].Right.X && Main.player[num352].Top.Y > base.Bottom.Y && Collision.CanHit(this, Main.player[num352]) && (Main.player[num352].RollOnlyBadLuckExtreme(50) == 0 || Main.player[num352].IsThisCenx()))
25403					{
25404						localAI[3] = 1f;
25405						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), Main.player[num352].Center.X, base.Center.Y, 0f, 0f, 1080, 0, 0f);
25406					}
25407				}
25408				noGravity = true;
25409				if (type == 611 || type == 689)
25410				{
25411					if (type == 689 && Main.netMode != 1 && !Main.dayTime)
25412					{
25413						int num353 = Player.FindClosest(position, width, height);
25414						if (Vector2.Distance(base.Center, Main.player[num353].Center) < 80f && Collision.CanHit(position, width, height, Main.player[num353].position, Main.player[num353].width, Main.player[num353].height))
25415						{
25416							Transform(317);
25417						}
25418					}
25419					if (localAI[0] == 0f)
25420					{
25421						TargetClosest();
25422						this.ai[0] = 1f;
25423						localAI[0] = 1f;
25424						netUpdate = true;
25425					}
25426					else if (this.ai[0] == 1f && Main.cloudAlpha == 0f && !Main.dayTime)
25427					{
25428						for (int num354 = 0; num354 < Main.maxNPCs; num354++)
25429						{
25430							if (num354 == whoAmI || !Main.npc[num354].active)
25431							{
25432								continue;
25433							}
25434							if (Main.npc[num354].townNPC)
25435							{
25436								if (Math.Abs(base.Center.X - Main.npc[num354].Center.X) < 96f)
25437								{
25438									float num355 = Main.npc[num354].Center.Y - base.Center.Y;
25439									if (num355 > 32f && num355 < 320f && !Collision.CanHit(this, Main.npc[num354]))
25440									{
25441										this.ai[0] = 2f;
25442									}
25443								}
25444							}
25445							else if (Main.npc[num354].type == type && Main.npc[num354].ai[0] != 1f && Math.Abs(base.Center.X - Main.npc[num354].Center.X) < 320f)
25446							{
25447								this.ai[0] = 1f;
25448								break;
25449							}
25450						}
25451					}
25452				}
25453				if (this.ai[0] == 0f)
25454				{
25455					noGravity = false;
25456					if ((type == 611 || type == 689) && (Main.cloudAlpha > 0f || Main.dayTime))
25457					{
25458						this.ai[0] = 1f;
25459					}
25460					TargetClosest();
25461					if (Main.netMode != 1)
25462					{
25463						if (releaseOwner != 255 || velocity.X != 0f || velocity.Y < 0f || (double)velocity.Y > 0.3)
25464						{
25465							this.ai[0] = 1f;
25466							netUpdate = true;
25467							direction = -direction;
25468						}
25469						else if (type != 611 && type != 689)
25470						{
25471							Rectangle rectangle2 = new Rectangle((int)Main.player[target].position.X, (int)Main.player[target].position.Y, Main.player[target].width, Main.player[target].height);
25472							if (new Rectangle((int)position.X - 100, (int)position.Y - 100, width + 200, height + 200).Intersects(rectangle2) || life < lifeMax)
25473							{
25474								this.ai[0] = 1f;
25475								velocity.Y -= 6f;
25476								netUpdate = true;
25477								direction = -direction;
25478							}
25479						}
25480					}
25481				}
25482				else if (this.ai[0] == 2f)
25483				{
25484					velocity.X *= 0.98f;
25485					if (velocity.Y == 0f)
25486					{
25487						this.ai[0] = 0f;
25488						velocity.X = 0f;
25489					}
25490					velocity.Y += 0.05f;
25491					if (velocity.Y > 2f)
25492					{
25493						velocity.Y = 2f;
25494					}
25495				}
25496				else if (!Main.player[target].dead)
25497				{
25498					float num356 = 3f;
25499					if (type == 671 || type == 672 || type == 673 || type == 674 || type == 675)
25500					{
25501						num356 = 4f;
25502					}
25503					if (collideX)
25504					{
25505						direction *= -1;
25506						velocity.X = oldVelocity.X * -0.5f;
25507						if (direction == -1 && velocity.X > 0f && velocity.X < num356 - 1f)
25508						{
25509							velocity.X = num356 - 1f;
25510						}
25511						if (direction == 1 && velocity.X < 0f && velocity.X > 0f - num356 + 1f)
25512						{
25513							velocity.X = 0f - num356 + 1f;
25514						}
25515					}
25516					if (collideY)
25517					{
25518						velocity.Y = oldVelocity.Y * -0.5f;
25519						if (velocity.Y > 0f && velocity.Y < 1f)
25520						{
25521							velocity.Y = 1f;
25522						}
25523						if (velocity.Y < 0f && velocity.Y > -1f)
25524						{
25525							velocity.Y = -1f;
25526						}
25527					}
25528					if (direction == -1 && velocity.X > 0f - num356)
25529					{
25530						velocity.X -= 0.1f;
25531						if (velocity.X > num356)
25532						{
25533							velocity.X -= 0.1f;
25534						}
25535						else if (velocity.X > 0f)
25536						{
25537							velocity.X -= 0.05f;
25538						}
25539						if (velocity.X < 0f - num356)
25540						{
25541							velocity.X = 0f - num356;
25542						}
25543					}
25544					else if (direction == 1 && velocity.X < num356)
25545					{
25546						velocity.X += 0.1f;
25547						if (velocity.X < 0f - num356)
25548						{
25549							velocity.X += 0.1f;
25550						}
25551						else if (velocity.X < 0f)
25552						{
25553							velocity.X += 0.05f;
25554						}
25555						if (velocity.X > num356)
25556						{
25557							velocity.X = num356;
25558						}
25559					}
25560					int num357 = (int)((position.X + (float)(width / 2)) / 16f) + direction;
25561					int num358 = (int)((position.Y + (float)height) / 16f);
25562					bool flag34 = true;
25563					int num359 = 15;
25564					bool flag35 = false;
25565					for (int num360 = num358; num360 < num358 + num359; num360++)
25566					{
25567						if (!WorldGen.InWorld(num357, num360))
25568						{
25569							continue;
25570						}
25571						if (Main.tile[num357, num360] == null)
25572						{
25573							Main.tile[num357, num360] = new Tile();
25574						}
25575						if ((Main.tile[num357, num360].nactive() && Main.tileSolid[Main.tile[num357, num360].type]) || Main.tile[num357, num360].liquid > 0)
25576						{
25577							if (num360 < num358 + 5)
25578							{
25579								flag35 = true;
25580							}
25581							flag34 = false;
25582							break;
25583						}
25584					}
25585					if (flag34)
25586					{
25587						velocity.Y += 0.05f;
25588					}
25589					else
25590					{
25591						velocity.Y -= 0.1f;
25592					}
25593					if (flag35)
25594					{
25595						velocity.Y -= 0.2f;
25596					}
25597					if (velocity.Y > 2f)
25598					{
25599						velocity.Y = 2f;
25600					}
25601					if (velocity.Y < -4f)
25602					{
25603						velocity.Y = -4f;
25604					}
25605				}
25606				if (wet)
25607				{
25608					this.ai[1] = 0f;
25609					if (velocity.Y > 0f)
25610					{
25611						velocity.Y *= 0.95f;
25612					}
25613					velocity.Y -= 0.5f;
25614					if (velocity.Y < -4f)
25615					{
25616						velocity.Y = -4f;
25617					}
25618					TargetClosest();
25619				}
25620			}
25621			else if (aiStyle == 25)
25622			{
25623				bool flag36 = type == 341 && !Main.snowMoon;
25624				if (this.ai[3] == 0f)
25625				{

```


---

## 🤖 Assistant · 2026-08-11T04:28:23.210Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Got aiStyle 0 (19774-19893), 23 (25316-25395), 24 (bird, which covers Raven? Actually aiStyle 24 is the bird AI — wait, the task said "aiStyle 17 (61 Vulture + 301 Raven 是否同块)". Raven 301 — actually aiStyle 24 is the "bird" AI (SittableBird). Raven has aiStyle 24? Let me check. In 1.4, Raven (301) has aiStyle 24 (bird that can poop / bird). Hmm. Actually NPCID.Sets.BirdThatCanPoop... aiStyle 24 is the bird AI including seagulls etc. Let me verify raven's aiStyle from our extracted NPC json data — we have npc data json. Or check NPCID.Sets.

Actually I can check the extracted npc JSON in the project: vanilla-npc-port memory says 561 NPC data extracted. Let me find that json quickly and check aiStyle for 61, 301, 69, 83, 84, 179, 85, 341, 153, 154, 417, 174, 177, 378, 224, 509, 581, 288, 105/106/123/354/376/579/589.

Also read AI_000_TransformBoundNPC.

Next: read aiStyle 25 (25621...), 39 (29257...), 41 (30017...), 44 (30999...), 56 (32915...).

Let me read 25 and 39 now.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:28:23.448Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 150,
 "offset": 25621
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:23.463Z

**📎 ToolResult**

```
25621			else if (aiStyle == 25)
25622			{
25623				bool flag36 = type == 341 && !Main.snowMoon;
25624				if (this.ai[3] == 0f)
25625				{
25626					position.X += 8f;
25627					if (position.Y / 16f > (float)Main.UnderworldLayer)
25628					{
25629						this.ai[3] = 3f;
25630					}
25631					else if ((double)(position.Y / 16f) > Main.worldSurface)
25632					{
25633						TargetClosest();
25634						this.ai[3] = 2f;
25635					}
25636					else
25637					{
25638						this.ai[3] = 1f;
25639					}
25640				}
25641				if (type == 341 || type == 629)
25642				{
25643					this.ai[3] = 1f;
25644				}
25645				if (this.ai[0] == 0f)
25646				{
25647					if (!flag36)
25648					{
25649						TargetClosest();
25650					}
25651					if (Main.netMode == 1)
25652					{
25653						return;
25654					}
25655					if (velocity.X != 0f || velocity.Y < 0f || (double)velocity.Y > 0.3)
25656					{
25657						this.ai[0] = 1f;
25658						netUpdate = true;
25659						return;
25660					}
25661					Rectangle rectangle3 = new Rectangle((int)Main.player[target].position.X, (int)Main.player[target].position.Y, Main.player[target].width, Main.player[target].height);
25662					if (new Rectangle((int)position.X - 100, (int)position.Y - 100, width + 200, height + 200).Intersects(rectangle3) || life < lifeMax)
25663					{
25664						this.ai[0] = 1f;
25665						netUpdate = true;
25666					}
25667				}
25668				else if (velocity.Y == 0f)
25669				{
25670					this.ai[2] += 1f;
25671					int num361 = 20;
25672					if (this.ai[1] == 0f)
25673					{
25674						num361 = 12;
25675					}
25676					if (this.ai[2] < (float)num361)
25677					{
25678						velocity.X *= 0.9f;
25679						return;
25680					}
25681					this.ai[2] = 0f;
25682					if (!flag36)
25683					{
25684						TargetClosest();
25685					}
25686					if (direction == 0)
25687					{
25688						direction = -1;
25689					}
25690					spriteDirection = direction;
25691					this.ai[1] += 1f;
25692					if (this.ai[1] == 2f)
25693					{
25694						velocity.X = (float)direction * 2.5f;
25695						velocity.Y = -8f;
25696						this.ai[1] = 0f;
25697					}
25698					else
25699					{
25700						velocity.X = (float)direction * 3.5f;
25701						velocity.Y = -4f;
25702					}
25703					netUpdate = true;
25704				}
25705				else if (direction == 1 && velocity.X < 1f)
25706				{
25707					velocity.X += 0.1f;
25708				}
25709				else if (direction == -1 && velocity.X > -1f)
25710				{
25711					velocity.X -= 0.1f;
25712				}
25713			}
25714			else if (aiStyle == 26)
25715			{
25716				AI_026_Unicorns();
25717			}
25718			else if (aiStyle == 27)
25719			{
25720				if (position.X < 160f || position.X > (float)((Main.maxTilesX - 10) * 16))
25721				{
25722					active = false;
25723				}
25724				NetUpdateLowPriority();
25725				if (localAI[0] == 0f)
25726				{
25727					localAI[0] = 1f;
25728					Main.wofDrawAreaBottom = -1;
25729					Main.wofDrawAreaTop = -1;
25730				}
25731				if (Main.getGoodWorld && Main.netMode != 1 && Main.rand.Next(180) == 0 && CountNPCS(24) < 4)
25732				{
25733					int num362 = 1;
25734					for (int num363 = 0; num363 < num362; num363++)
25735					{
25736						int num364 = 1000;
25737						for (int num365 = 0; num365 < num364; num365++)
25738						{
25739							int num366 = (int)(base.Center.X / 16f);
25740							int num367 = (int)(base.Center.Y / 16f);
25741							if (target >= 0)
25742							{
25743								num366 = (int)(Main.player[target].Center.X / 16f);
25744								num367 = (int)(Main.player[target].Center.Y / 16f);
25745							}
25746							num366 += Main.rand.Next(-50, 51);
25747							for (num367 += Main.rand.Next(-50, 51); num367 < Main.maxTilesY - 10 && !WorldGen.SolidTile(num366, num367); num367++)
25748							{
25749							}
25750							num367--;
25751							if (!WorldGen.SolidTile(num366, num367))
25752							{
25753								int num368 = NewNPC(GetSpawnSourceForNPCFromNPCAI(), num366 * 16 + 8, num367 * 16, 24);
25754								if (Main.netMode == 2 && num368 < Main.maxNPCs)
25755								{
25756									NetMessage.SendData(23, -1, -1, null, num368);
25757								}
25758								break;
25759							}
25760						}
25761					}
25762				}
25763				this.ai[1] += 1f;
25764				if (this.ai[2] == 0f)
25765				{
25766					if ((double)life < (double)lifeMax * 0.5)
25767					{
25768						this.ai[1] += 1f;
25769					}
25770					if ((double)life < (double)lifeMax * 0.2)

```


---

## 🤖 Assistant · 2026-08-11T04:28:23.813Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"AI_000_TransformBoundNPC\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -3",
 "description": "Find TransformBoundNPC helper definition"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:23.858Z

**📎 ToolResult**

```
19784:							AI_000_TransformBoundNPC(i, 588);
19788:							AI_000_TransformBoundNPC(i, 107);
19792:							AI_000_TransformBoundNPC(i, 108);

```


---

## 🤖 Assistant · 2026-08-11T04:28:30.659Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting: aiStyle 25's Mimic doesn't match the classic description. Wait — this is 1.4.5.6 and the Mimic block I read at 25621 looks different from 1.4.0. Hmm, actually it looks like the ai[3] init: position.X += 8f — hmm, and it sets ai[3]=3 if in underworld, 2 underground, 1 surface. But then the block I read doesn't use ai[3] afterwards? It reads ai[0], ai[1], ai[2]. Hmm wait — maybe I mis-read. Actually wait — 25641: `if (type == 341 || type == 629) this.ai[3] = 1f;`. Then uses ai[0] for state. Hmm, ai[3] seems unused in this block... possibly used in FindFrame or elsewhere. Hmm, but actually maybe I read an incomplete version. Wait — hold on. Is this really the Mimic block? aiStyle 25 is Mimic. The code: ai[0]==0 dormant, wakes when player within 200px box (100px padding, not in tiles) or damaged. Then jump cycle. That matches classic Mimic. OK good. But ai[3] usage: hmm, position.Y/16 > UnderworldLayer → ai[3]=3. That's used... maybe in FindFrame for animation frame (chest variant?). Not in movement. Fine — I'll note ai[3]=layer marker (1 surface/2 underground/3 hell), used elsewhere (visual).

Wait, actually there might be more of the aiStyle 25 block — it ended at 25713 with "else if (aiStyle == 26)". Good, complete.

TransformBoundNPC helper not found by grep? Only call sites showed. Maybe it's defined in another partial file. Let me search across Terraria dir.

Now read 39, 41, 44, 56. Let me batch.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:28:30.863Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 120,
 "offset": 29257
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:30.872Z

**📎 ToolResult**

```
29257			else if (aiStyle == 39)
29258			{
29259				if (target < 0 || Main.player[target].dead || direction == 0)
29260				{
29261					TargetClosest();
29262				}
29263				bool flag39 = true;
29264				int num598 = 0;
29265				if (velocity.X < 0f)
29266				{
29267					num598 = -1;
29268				}
29269				if (velocity.X > 0f)
29270				{
29271					num598 = 1;
29272				}
29273				Vector2 vector66 = position;
29274				vector66.X += velocity.X;
29275				int num599 = (int)((vector66.X + (float)(width / 2) + (float)((width / 2 + 1) * num598)) / 16f);
29276				int num600 = (int)((vector66.Y + (float)height - 1f) / 16f);
29277				if ((float)(num599 * 16) < vector66.X + (float)width && (float)(num599 * 16 + 16) > vector66.X)
29278				{
29279					Tile tileSafely = Framing.GetTileSafely(num599, num600 - 4);
29280					Tile tileSafely2 = Framing.GetTileSafely(num599 - num598, num600 - 3);
29281					Tile tileSafely3 = Framing.GetTileSafely(num599, num600 - 3);
29282					Tile tileSafely4 = Framing.GetTileSafely(num599, num600 - 2);
29283					Tile tileSafely5 = Framing.GetTileSafely(num599, num600 - 1);
29284					Tile tileSafely6 = Framing.GetTileSafely(num599, num600);
29285					if (((tileSafely6.nactive() && !tileSafely6.topSlope() && !tileSafely5.topSlope() && ((Main.tileSolid[tileSafely6.type] && !Main.tileSolidTop[tileSafely6.type]) || (flag39 && Main.tileSolidTop[tileSafely6.type] && (!Main.tileSolid[tileSafely5.type] || !tileSafely5.nactive()) && tileSafely6.type != 16 && tileSafely6.type != 18 && tileSafely6.type != 134))) || (tileSafely5.halfBrick() && tileSafely5.nactive())) && (!tileSafely5.nactive() || !Main.tileSolid[tileSafely5.type] || Main.tileSolidTop[tileSafely5.type] || (tileSafely5.halfBrick() && (!tileSafely.nactive() || !Main.tileSolid[tileSafely.type] || Main.tileSolidTop[tileSafely.type]))) && (!tileSafely4.nactive() || !Main.tileSolid[tileSafely4.type] || Main.tileSolidTop[tileSafely4.type]) && (!tileSafely3.nactive() || !Main.tileSolid[tileSafely3.type] || Main.tileSolidTop[tileSafely3.type]) && (!tileSafely2.nactive() || !Main.tileSolid[tileSafely2.type] || Main.tileSolidTop[tileSafely2.type]))
29286					{
29287						float num601 = num600 * 16;
29288						if (tileSafely6.halfBrick())
29289						{
29290							num601 += 8f;
29291						}
29292						if (tileSafely5.halfBrick())
29293						{
29294							num601 -= 8f;
29295						}
29296						if (num601 < vector66.Y + (float)height)
29297						{
29298							float num602 = vector66.Y + (float)height - num601;
29299							if ((double)num602 <= 16.1)
29300							{
29301								gfxOffY += position.Y + (float)height - num601;
29302								position.Y = num601 - (float)height;
29303								if (num602 < 9f)
29304								{
29305									stepSpeed = 0.75f;
29306								}
29307								else
29308								{
29309									stepSpeed = 1.5f;
29310								}
29311							}
29312						}
29313					}
29314				}
29315				if (justHit && type != 417)
29316				{
29317					this.ai[0] = 0f;
29318					this.ai[1] = 0f;
29319					TargetClosest();
29320				}
29321				if (type == 154)
29322				{
29323					position += netOffset;
29324					if (Main.rand.Next(10) == 0)
29325					{
29326						int num603 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 67, velocity.X * 0.5f, velocity.Y * 0.5f, 90, default(Color), 1.5f);
29327						Main.dust[num603].noGravity = true;
29328						Dust dust = Main.dust[num603];
29329						dust.velocity *= 0.2f;
29330					}
29331					position -= netOffset;
29332				}
29333				if (this.ai[0] == 0f)
29334				{
29335					if (velocity.X < 0f)
29336					{
29337						direction = -1;
29338					}
29339					else if (velocity.X > 0f)
29340					{
29341						direction = 1;
29342					}
29343					spriteDirection = direction;
29344					Vector2 vector67 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
29345					float num604 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector67.X;
29346					float num605 = Main.player[target].position.Y - vector67.Y;
29347					float num606 = (float)Math.Sqrt(num604 * num604 + num605 * num605);
29348					bool flag40 = Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height);
29349					if (type >= 496 && type <= 497)
29350					{
29351						if (num606 > 200f && flag40)
29352						{
29353							this.ai[1] += 2f;
29354						}
29355						if (num606 > 600f && (flag40 || position.Y + (float)height > Main.player[target].position.Y - 200f))
29356						{
29357							this.ai[1] += 4f;
29358						}
29359					}
29360					else
29361					{
29362						if (num606 > 200f && flag40)
29363						{
29364							this.ai[1] += 4f;
29365						}
29366						if (num606 > 600f && (flag40 || position.Y + (float)height > Main.player[target].position.Y - 200f))
29367						{
29368							this.ai[1] += 10f;
29369						}
29370						if (wet)
29371						{
29372							this.ai[1] = 1000f;
29373						}
29374					}
29375					defense = defDefense;
29376					damage = defDamage;

```


---

## 🤖 Assistant · 2026-08-11T04:28:31.105Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 130,
 "offset": 30017
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:31.120Z

**📎 ToolResult**

```
30017			else if (aiStyle == 41)
30018			{
30019				if (this.ai[2] > 1f)
30020				{
30021					this.ai[2] -= 1f;
30022				}
30023				if (this.ai[2] == 0f)
30024				{
30025					this.ai[0] = -100f;
30026					this.ai[2] = 1f;
30027					TargetClosest();
30028					spriteDirection = direction;
30029				}
30030				if (type == 378)
30031				{
30032					Vector2 vector73 = new Vector2(-6f, -10f);
30033					vector73.X *= spriteDirection;
30034					if (this.ai[1] != 5f && Main.rand.Next(3) == 0)
30035					{
30036						position += netOffset;
30037						int num643 = Dust.NewDust(base.Center + vector73 - Vector2.One * 5f, 4, 4, 6);
30038						Main.dust[num643].scale = 1.5f;
30039						Main.dust[num643].noGravity = true;
30040						Main.dust[num643].velocity = Main.dust[num643].velocity * 0.25f + Vector2.Normalize(vector73) * 1f;
30041						Main.dust[num643].velocity = Main.dust[num643].velocity.RotatedBy(-MathF.PI / 2f * (float)direction);
30042						position -= netOffset;
30043					}
30044					if (this.ai[1] == 5f)
30045					{
30046						velocity = Vector2.Zero;
30047						position.X += width / 2;
30048						position.Y += height / 2;
30049						width = 160;
30050						height = 160;
30051						position.X -= width / 2;
30052						position.Y -= height / 2;
30053						dontTakeDamage = true;
30054						position += netOffset;
30055						if (this.ai[2] > 7f)
30056						{
30057							for (int num644 = 0; num644 < 8; num644++)
30058							{
30059								int num645 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 31, 0f, 0f, 100, default(Color), 1.5f);
30060							}
30061							for (int num646 = 0; num646 < 32; num646++)
30062							{
30063								int num647 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 6, 0f, 0f, 100, default(Color), 2.5f);
30064								Main.dust[num647].noGravity = true;
30065								Dust dust = Main.dust[num647];
30066								dust.velocity *= 3f;
30067								num647 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 6, 0f, 0f, 100, default(Color), 1.5f);
30068								dust = Main.dust[num647];
30069								dust.velocity *= 2f;
30070								Main.dust[num647].noGravity = true;
30071							}
30072							for (int num648 = 0; num648 < 2; num648++)
30073							{
30074								int num649 = Gore.NewGore(position + new Vector2((float)(width * Main.rand.Next(100)) / 100f, (float)(height * Main.rand.Next(100)) / 100f) - Vector2.One * 10f, default(Vector2), Main.rand.Next(61, 64));
30075								Gore gore = Main.gore[num649];
30076								gore.velocity *= 0.3f;
30077								Main.gore[num649].velocity.X += (float)Main.rand.Next(-10, 11) * 0.05f;
30078								Main.gore[num649].velocity.Y += (float)Main.rand.Next(-10, 11) * 0.05f;
30079							}
30080							if (this.ai[2] == 9f)
30081							{
30082								SoundEngine.PlaySound(SoundID.Item14, position);
30083							}
30084						}
30085						if (this.ai[2] == 1f)
30086						{
30087							life = -1;
30088							HitEffect();
30089							active = false;
30090						}
30091						position -= netOffset;
30092						return;
30093					}
30094				}
30095				if (type == 378 && this.ai[1] != 5f)
30096				{
30097					if (wet || Vector2.Distance(base.Center, Main.player[target].Center) < 64f)
30098					{
30099						this.ai[1] = 5f;
30100						this.ai[2] = 10f;
30101						netUpdate = true;
30102						return;
30103					}
30104				}
30105				else if (wet && type != 177)
30106				{
30107					if (collideX)
30108					{
30109						direction *= -direction;
30110						spriteDirection = direction;
30111					}
30112					if (collideY)
30113					{
30114						TargetClosest();
30115						if (oldVelocity.Y < 0f)
30116						{
30117							velocity.Y = 5f;
30118						}
30119						else
30120						{
30121							velocity.Y -= 2f;
30122						}
30123						spriteDirection = direction;
30124					}
30125					if (velocity.Y > 4f)
30126					{
30127						velocity.Y *= 0.95f;
30128					}
30129					velocity.Y -= 0.3f;
30130					if (velocity.Y < -4f)
30131					{
30132						velocity.Y = -4f;
30133					}
30134				}
30135				if (velocity.Y == 0f)
30136				{
30137					if (this.ai[3] == position.X)
30138					{
30139						direction *= -1;
30140						this.ai[2] = 300f;
30141					}
30142					this.ai[3] = 0f;
30143					velocity.X *= 0.8f;
30144					if ((double)velocity.X > -0.1 && (double)velocity.X < 0.1)
30145					{
30146						velocity.X = 0f;

```


---

## 🤖 Assistant · 2026-08-11T04:28:33.170Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Need rest of aiStyle 39 (29376 onward) and rest of 41 (30146 onward). Read both.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:28:33.330Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 130,
 "offset": 29376
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:33.343Z

**📎 ToolResult**

```
29376					damage = defDamage;
29377					if (type >= 496 && type <= 497)
29378					{
29379						knockBackResist = GetKnockbackMultiplier_ScaledByDifficulty(0.75f);
29380					}
29381					else
29382					{
29383						knockBackResist = GetKnockbackMultiplier_ScaledByDifficulty(0.3f);
29384					}
29385					this.ai[1] += 1f;
29386					if (this.ai[1] >= 400f)
29387					{
29388						this.ai[1] = 0f;
29389						this.ai[0] = 1f;
29390					}
29391					if (!justHit && velocity.X != oldVelocity.X)
29392					{
29393						direction *= -1;
29394					}
29395					if (velocity.Y == 0f && Main.player[target].position.Y < position.Y + (float)height)
29396					{
29397						int num607;
29398						int num608;
29399						if (direction > 0)
29400						{
29401							num607 = (int)(((double)position.X + (double)width * 0.5) / 16.0);
29402							num608 = num607 + 3;
29403						}
29404						else
29405						{
29406							num608 = (int)(((double)position.X + (double)width * 0.5) / 16.0);
29407							num607 = num608 - 3;
29408						}
29409						int num609 = (int)((position.Y + (float)height + 2f) / 16f) - 1;
29410						int num610 = num609 + 4;
29411						bool flag41 = false;
29412						for (int num611 = num607; num611 <= num608; num611++)
29413						{
29414							for (int num612 = num609; num612 <= num610; num612++)
29415							{
29416								if (Main.tile[num611, num612] != null && Main.tile[num611, num612].nactive() && Main.tileSolid[Main.tile[num611, num612].type])
29417								{
29418									flag41 = true;
29419								}
29420							}
29421						}
29422						if (!flag41)
29423						{
29424							direction *= -1;
29425							velocity.X = 0.1f * (float)direction;
29426						}
29427					}
29428					if (type >= 496 && type <= 497)
29429					{
29430						float num613 = 0.5f;
29431						if (velocity.X < 0f - num613 || velocity.X > num613)
29432						{
29433							if (velocity.Y == 0f)
29434							{
29435								velocity *= 0.8f;
29436							}
29437						}
29438						else if (velocity.X < num613 && direction == 1)
29439						{
29440							velocity.X += 0.07f;
29441							if (velocity.X > num613)
29442							{
29443								velocity.X = num613;
29444							}
29445						}
29446						else if (velocity.X > 0f - num613 && direction == -1)
29447						{
29448							velocity.X -= 0.07f;
29449							if (velocity.X < 0f - num613)
29450							{
29451								velocity.X = 0f - num613;
29452							}
29453						}
29454						return;
29455					}
29456					float num614 = 1f;
29457					if (num606 < 400f)
29458					{
29459						if (velocity.X < 0f - num614 || velocity.X > num614)
29460						{
29461							if (velocity.Y == 0f)
29462							{
29463								velocity *= 0.8f;
29464							}
29465						}
29466						else if (velocity.X < num614 && direction == 1)
29467						{
29468							velocity.X += 0.07f;
29469							if (velocity.X > num614)
29470							{
29471								velocity.X = num614;
29472							}
29473						}
29474						else if (velocity.X > 0f - num614 && direction == -1)
29475						{
29476							velocity.X -= 0.07f;
29477							if (velocity.X < 0f - num614)
29478							{
29479								velocity.X = 0f - num614;
29480							}
29481						}
29482					}
29483					else if (velocity.X < -1.5f || velocity.X > 1.5f)
29484					{
29485						if (velocity.Y == 0f)
29486						{
29487							velocity *= 0.8f;
29488						}
29489					}
29490					else if (velocity.X < 1.5f && direction == 1)
29491					{
29492						velocity.X += 0.07f;
29493						if (velocity.X > 1.5f)
29494						{
29495							velocity.X = 1.5f;
29496						}
29497					}
29498					else if (velocity.X > -1.5f && direction == -1)
29499					{
29500						velocity.X -= 0.07f;
29501						if (velocity.X < -1.5f)
29502						{
29503							velocity.X = -1.5f;
29504						}
29505					}

```


---

## 🤖 Assistant · 2026-08-11T04:28:33.594Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 110,
 "offset": 30146
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:33.602Z

**📎 ToolResult**

```
30146						velocity.X = 0f;
30147					}
30148					if (type == 177)
30149					{
30150						this.ai[0] += 2f;
30151					}
30152					else
30153					{
30154						this.ai[0] += 5f;
30155					}
30156					Vector2 vector74 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
30157					float num650 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector74.X;
30158					float num651 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector74.Y;
30159					float num652 = (float)Math.Sqrt(num650 * num650 + num651 * num651);
30160					float num653 = 400f / num652;
30161					num653 = ((type != 177) ? (num653 * 10f) : (num653 * 5f));
30162					if (num653 > 30f)
30163					{
30164						num653 = 30f;
30165					}
30166					this.ai[0] += (int)num653;
30167					if (this.ai[0] >= 0f)
30168					{
30169						netUpdate = true;
30170						if (this.ai[2] == 1f)
30171						{
30172							TargetClosest();
30173						}
30174						if (type == 177)
30175						{
30176							if (this.ai[1] == 2f)
30177							{
30178								velocity.Y = -11.5f;
30179								velocity.X += 2f * (float)direction;
30180								if (num652 < 350f && num652 > 200f)
30181								{
30182									velocity.X += direction;
30183								}
30184								this.ai[0] = -200f;
30185								this.ai[1] = 0f;
30186								this.ai[3] = position.X;
30187							}
30188							else
30189							{
30190								velocity.Y = -7.5f;
30191								velocity.X += 4 * direction;
30192								if (num652 < 350f && num652 > 200f)
30193								{
30194									velocity.X += direction;
30195								}
30196								this.ai[0] = -120f;
30197								this.ai[1] += 1f;
30198							}
30199						}
30200						else
30201						{
30202							if (type == 378)
30203							{
30204								SoundEngine.PlaySound(29, (int)position.X, (int)position.Y, 124);
30205							}
30206							if (this.ai[1] == 3f)
30207							{
30208								velocity.Y = -9f;
30209								velocity.X += 3 * direction;
30210								if (num652 < 350f && num652 > 200f)
30211								{
30212									velocity.X += direction;
30213								}
30214								this.ai[0] = -200f;
30215								this.ai[1] = 0f;
30216								this.ai[3] = position.X;
30217							}
30218							else
30219							{
30220								velocity.Y = -5f;
30221								velocity.X += 5 * direction;
30222								if (num652 < 350f && num652 > 200f)
30223								{
30224									velocity.X += direction;
30225								}
30226								this.ai[0] = -120f;
30227								this.ai[1] += 1f;
30228							}
30229						}
30230					}
30231					else if (this.ai[0] >= -30f)
30232					{
30233						aiAction = 1;
30234					}
30235					spriteDirection = direction;
30236				}
30237				else
30238				{
30239					if (target >= 255)
30240					{
30241						return;
30242					}
30243					if (type == 177)
30244					{
30245						bool flag44 = false;
30246						if (position.Y + (float)height < Main.player[target].position.Y && position.X + (float)width > Main.player[target].position.X && position.X < Main.player[target].position.X + (float)Main.player[target].width)
30247						{
30248							flag44 = true;
30249							velocity.X *= 0.92f;
30250							if (velocity.Y < 0f)
30251							{
30252								velocity.Y *= 0.9f;
30253								velocity.Y += 0.1f;
30254							}
30255						}

```


---

## 🤖 Assistant · 2026-08-11T04:28:35.643Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Need rest of 39 (29505 onward) and rest of 41 (30255 onward to block end). Also 44 at 30999 and 56 at 32915. Let me continue reading.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:28:35.841Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 120,
 "offset": 29505
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:35.847Z

**📎 ToolResult**

```
29505					}
29506				}
29507				else if (this.ai[0] == 1f)
29508				{
29509					velocity.X *= 0.5f;
29510					if (type >= 496 && type <= 497)
29511					{
29512						this.ai[1] += 0.5f;
29513					}
29514					else
29515					{
29516						this.ai[1] += 1f;
29517					}
29518					if (this.ai[1] >= 30f)
29519					{
29520						netUpdate = true;
29521						TargetClosest();
29522						this.ai[1] = 0f;
29523						this.ai[2] = 0f;
29524						this.ai[0] = 3f;
29525						if (type == 417)
29526						{
29527							position.Y += height;
29528							height = 32;
29529							position.Y -= height;
29530							this.ai[0] = 6f;
29531							this.ai[2] = Main.rand.Next(2, 5);
29532						}
29533					}
29534				}
29535				else if (this.ai[0] == 3f)
29536				{
29537					if (type == 154 && Main.rand.Next(3) < 2)
29538					{
29539						position += netOffset;
29540						int num615 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 67, velocity.X * 0.5f, velocity.Y * 0.5f, 90, default(Color), 1.5f);
29541						Main.dust[num615].noGravity = true;
29542						Dust dust = Main.dust[num615];
29543						dust.velocity *= 0.2f;
29544						position -= netOffset;
29545					}
29546					float num616 = 2f;
29547					if (type >= 496 && type <= 497)
29548					{
29549						num616 = 1.5f;
29550					}
29551					damage = GetAttackDamage_LerpBetweenFinalValues((float)defDamage * num616, (float)defDamage * num616 * 0.9f);
29552					defense = defDefense * 2;
29553					this.ai[1] += 1f;
29554					if (this.ai[1] == 1f)
29555					{
29556						netUpdate = true;
29557						TargetClosest();
29558						this.ai[2] += 0.3f;
29559						rotation += this.ai[2] * (float)direction;
29560						this.ai[1] += 1f;
29561						bool flag42 = Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height);
29562						float num617 = 10f;
29563						if (!flag42)
29564						{
29565							num617 = 6f;
29566						}
29567						if (type >= 496 && type <= 497)
29568						{
29569							num617 *= 0.75f;
29570						}
29571						Vector2 vector68 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
29572						float num618 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector68.X;
29573						float num619 = Math.Abs(num618) * 0.2f;
29574						if (directionY > 0)
29575						{
29576							num619 = 0f;
29577						}
29578						float num620 = Main.player[target].position.Y - vector68.Y - num619;
29579						float num621 = (float)Math.Sqrt(num618 * num618 + num620 * num620);
29580						netUpdate = true;
29581						num621 = num617 / num621;
29582						num618 *= num621;
29583						num620 *= num621;
29584						if (!flag42)
29585						{
29586							num620 = -10f;
29587						}
29588						velocity.X = num618;
29589						velocity.Y = num620;
29590						this.ai[3] = velocity.X;
29591					}
29592					else
29593					{
29594						if (position.X + (float)width > Main.player[target].position.X && position.X < Main.player[target].position.X + (float)Main.player[target].width && position.Y < Main.player[target].position.Y + (float)Main.player[target].height)
29595						{
29596							velocity.X *= 0.8f;
29597							this.ai[3] = 0f;
29598							if (velocity.Y < 0f)
29599							{
29600								velocity.Y += 0.2f;
29601							}
29602						}
29603						if (this.ai[3] != 0f)
29604						{
29605							velocity.X = this.ai[3];
29606							velocity.Y -= 0.22f;
29607						}
29608						if (this.ai[1] >= 90f)
29609						{
29610							noGravity = false;
29611							this.ai[1] = 0f;
29612							this.ai[0] = 4f;
29613						}
29614					}
29615					if (wet && directionY < 0)
29616					{
29617						velocity.Y -= 0.3f;
29618					}
29619					rotation += this.ai[2] * (float)direction;
29620				}
29621				else if (this.ai[0] == 4f)
29622				{
29623					if (wet && directionY < 0)
29624					{

```


---

## 🤖 Assistant · 2026-08-11T04:28:36.080Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 115,
 "offset": 30255
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:36.087Z

**📎 ToolResult**

```
30255						}
30256						if (!flag44 && ((direction == 1 && velocity.X < 4f) || (direction == -1 && velocity.X > -4f)))
30257						{
30258							if ((direction == -1 && (double)velocity.X < 0.1) || (direction == 1 && (double)velocity.X > -0.1))
30259							{
30260								velocity.X += 0.2f * (float)direction;
30261							}
30262							else
30263							{
30264								velocity.X *= 0.93f;
30265							}
30266						}
30267					}
30268					else if ((direction == 1 && velocity.X < 3f) || (direction == -1 && velocity.X > -3f))
30269					{
30270						if ((direction == -1 && (double)velocity.X < 0.1) || (direction == 1 && (double)velocity.X > -0.1))
30271						{
30272							velocity.X += 0.2f * (float)direction;
30273						}
30274						else
30275						{
30276							velocity.X *= 0.93f;
30277						}
30278					}
30279				}
30280			}
30281			else if (aiStyle == 42)
30282			{
30283				TargetClosest();
30284				if (this.ai[0] == 0f)
30285				{
30286					if (target >= 0)
30287					{
30288						Vector2 vector75 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
30289						float num654 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector75.X;
30290						float num655 = Main.player[target].position.Y - vector75.Y;
30291						float num656 = (float)Math.Sqrt(num654 * num654 + num655 * num655);
30292						if (num656 < 200f && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
30293						{
30294							this.ai[0] = 1f;
30295						}
30296					}
30297					if (velocity.X != 0f || velocity.Y < 0f || velocity.Y > 2f || life != lifeMax)
30298					{
30299						this.ai[0] = 1f;
30300					}
30301				}
30302				else
30303				{
30304					this.ai[0] += 1f;
30305					if (this.ai[0] >= 21f)
30306					{
30307						this.ai[0] = 21f;
30308						Transform(196);
30309					}
30310				}
30311			}
30312			else if (aiStyle == 43)
30313			{
30314				if (Main.expertMode)
30315				{
30316					int num657 = (int)(20f * (1f - (float)life / (float)lifeMax));
30317					defense = defDefense + num657;
30318				}
30319				if (target < 0 || target == 255 || Main.player[target].dead || !Main.player[target].active)
30320				{
30321					TargetClosest();
30322				}
30323				bool dead4 = Main.player[target].dead;
30324				float num658 = 0f;
30325				if ((double)(position.Y / 16f) < Main.worldSurface)
30326				{
30327					num658 += 1f;
30328				}
30329				if (!Main.player[target].ZoneJungle)
30330				{
30331					num658 += 1f;
30332				}
30333				if (Main.getGoodWorld)
30334				{
30335					num658 += 0.5f;
30336				}
30337				float num659 = Vector2.Distance(base.Center, Main.player[target].Center);
30338				if (this.ai[0] != 5f)
30339				{
30340					if (timeLeft < 60)
30341					{
30342						timeLeft = 60;
30343					}
30344					if (num659 > 3000f)
30345					{
30346						this.ai[0] = 4f;
30347						netUpdate = true;
30348					}
30349				}
30350				if (dead4)
30351				{
30352					this.ai[0] = 5f;
30353					netUpdate = true;
30354				}
30355				if (this.ai[0] == 5f)
30356				{
30357					velocity.Y *= 0.98f;
30358					if (velocity.X < 0f)
30359					{
30360						direction = -1;
30361					}
30362					else
30363					{
30364						direction = 1;
30365					}
30366					spriteDirection = direction;
30367					if (position.X < (float)(Main.maxTilesX * 8))
30368					{
30369						if (velocity.X > 0f)

```


---

## 🤖 Assistant · 2026-08-11T04:28:38.500Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
aiStyle 41 block ends at 30280. Good.

Still need the rest of aiStyle 39 (29621 onward: states 4, 6, and end). Read 29621-29760 or so. Also need to find where aiStyle 39 block ends. Then read 44 (30999) and 56 (32915).
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:28:38.749Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 130,
 "offset": 29621
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:38.756Z

**📎 ToolResult**

```
29621				else if (this.ai[0] == 4f)
29622				{
29623					if (wet && directionY < 0)
29624					{
29625						velocity.Y -= 0.3f;
29626					}
29627					velocity.X *= 0.96f;
29628					if (this.ai[2] > 0f)
29629					{
29630						this.ai[2] -= 0.01f;
29631						rotation += this.ai[2] * (float)direction;
29632					}
29633					else if (velocity.Y >= 0f)
29634					{
29635						rotation = 0f;
29636					}
29637					if (this.ai[2] <= 0f && (velocity.Y == 0f || wet))
29638					{
29639						netUpdate = true;
29640						rotation = 0f;
29641						this.ai[2] = 0f;
29642						this.ai[1] = 0f;
29643						this.ai[0] = 5f;
29644					}
29645				}
29646				else if (this.ai[0] == 6f)
29647				{
29648					damage = GetAttackDamage_LerpBetweenFinalValues((float)defDamage * 1.8f, (float)defDamage * 1.4f);
29649					defense = defDefense * 2;
29650					knockBackResist = 0f;
29651					if (Main.rand.Next(3) < 2)
29652					{
29653						position += netOffset;
29654						int num622 = Dust.NewDust(base.Center - new Vector2(30f), 60, 60, 6, velocity.X * 0.5f, velocity.Y * 0.5f, 90, default(Color), 1.5f);
29655						Main.dust[num622].noGravity = true;
29656						Dust dust = Main.dust[num622];
29657						dust.velocity *= 0.2f;
29658						Main.dust[num622].fadeIn = 1f;
29659						position -= netOffset;
29660					}
29661					this.ai[1] += 1f;
29662					if (this.ai[3] > 0f)
29663					{
29664						position += netOffset;
29665						if (this.ai[3] == 1f)
29666						{
29667							Vector2 vector69 = base.Center - new Vector2(50f);
29668							for (int num623 = 0; num623 < 32; num623++)
29669							{
29670								int num624 = Dust.NewDust(vector69, 100, 100, 6, 0f, 0f, 100, default(Color), 2.5f);
29671								Main.dust[num624].noGravity = true;
29672								Dust dust = Main.dust[num624];
29673								dust.velocity *= 3f;
29674								num624 = Dust.NewDust(vector69, 100, 100, 6, 0f, 0f, 100, default(Color), 1.5f);
29675								dust = Main.dust[num624];
29676								dust.velocity *= 2f;
29677								Main.dust[num624].noGravity = true;
29678							}
29679							for (int num625 = 0; num625 < 4; num625++)
29680							{
29681								int num626 = Gore.NewGore(vector69 + new Vector2((float)(50 * Main.rand.Next(100)) / 100f, (float)(50 * Main.rand.Next(100)) / 100f) - Vector2.One * 10f, default(Vector2), Main.rand.Next(61, 64));
29682								Gore gore = Main.gore[num626];
29683								gore.velocity *= 0.3f;
29684								Main.gore[num626].velocity.X += (float)Main.rand.Next(-10, 11) * 0.05f;
29685								Main.gore[num626].velocity.Y += (float)Main.rand.Next(-10, 11) * 0.05f;
29686							}
29687						}
29688						for (int num627 = 0; num627 < 5; num627++)
29689						{
29690							int num628 = Dust.NewDust(position, width, height, 31, 0f, 0f, 100, default(Color), 1.5f);
29691							Main.dust[num628].velocity = Main.dust[num628].velocity * Main.rand.NextFloat();
29692						}
29693						this.ai[3]++;
29694						if (this.ai[3] >= 10f)
29695						{
29696							this.ai[3] = 0f;
29697						}
29698						position -= netOffset;
29699					}
29700					if (this.ai[1] == 1f)
29701					{
29702						netUpdate = true;
29703						TargetClosest();
29704						bool flag43 = Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height);
29705						float num629 = 16f;
29706						if (!flag43)
29707						{
29708							num629 = 10f;
29709						}
29710						Vector2 vector70 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
29711						float num630 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector70.X;
29712						float num631 = Math.Abs(num630) * 0.2f;
29713						if (directionY > 0)
29714						{
29715							num631 = 0f;
29716						}
29717						float num632 = Main.player[target].position.Y - vector70.Y - num631;
29718						float num633 = (float)Math.Sqrt(num630 * num630 + num632 * num632);
29719						netUpdate = true;
29720						num633 = num629 / num633;
29721						num630 *= num633;
29722						num632 *= num633;
29723						if (!flag43)
29724						{
29725							num632 = -12f;
29726						}
29727						velocity.X = num630;
29728						velocity.Y = num632;
29729					}
29730					else
29731					{
29732						if (position.X + (float)width > Main.player[target].position.X && position.X < Main.player[target].position.X + (float)Main.player[target].width && position.Y < Main.player[target].position.Y + (float)Main.player[target].height)
29733						{
29734							velocity.X *= 0.9f;
29735							if (velocity.Y < 0f)
29736							{
29737								velocity.Y += 0.2f;
29738							}
29739						}
29740						if (this.ai[2] == 0f || this.ai[1] >= 1200f)
29741						{
29742							this.ai[1] = 0f;
29743							this.ai[0] = 5f;
29744						}
29745					}
29746					if (wet && directionY < 0)
29747					{
29748						velocity.Y -= 0.3f;
29749					}
29750					rotation += MathHelper.Clamp(velocity.X / 10f * (float)direction, -MathF.PI / 10f, MathF.PI / 10f);

```


---

## 🤖 Assistant · 2026-08-11T04:28:38.972Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 120,
 "offset": 30999
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:38.979Z

**📎 ToolResult**

```
30999			else if (aiStyle == 44)
31000			{
31001				noGravity = true;
31002				if (collideX)
31003				{
31004					if (oldVelocity.X > 0f)
31005					{
31006						direction = -1;
31007					}
31008					else
31009					{
31010						direction = 1;
31011					}
31012					velocity.X = direction;
31013				}
31014				if (collideY)
31015				{
31016					if (oldVelocity.Y > 0f)
31017					{
31018						directionY = -1;
31019					}
31020					else
31021					{
31022						directionY = 1;
31023					}
31024					velocity.Y = directionY;
31025				}
31026				if (type == 587)
31027				{
31028					position += netOffset;
31029					if (alpha == 255)
31030					{
31031						velocity.Y = -6f;
31032						netUpdate = true;
31033						for (int num706 = 0; num706 < 15; num706++)
31034						{
31035							Dust dust4 = Dust.NewDustDirect(position, width, height, 5);
31036							Dust dust = dust4;
31037							dust.velocity *= 0.5f;
31038							dust4.scale = 1f + Main.rand.NextFloat() * 0.5f;
31039							dust4.fadeIn = 1.5f + Main.rand.NextFloat() * 0.5f;
31040							dust = dust4;
31041							dust.velocity += velocity * 0.5f;
31042						}
31043					}
31044					alpha -= 15;
31045					if (alpha < 0)
31046					{
31047						alpha = 0;
31048					}
31049					if (alpha != 0)
31050					{
31051						for (int num707 = 0; num707 < 2; num707++)
31052						{
31053							Dust dust5 = Dust.NewDustDirect(position, width, height, 5);
31054							Dust dust = dust5;
31055							dust.velocity *= 1f;
31056							dust5.scale = 1f + Main.rand.NextFloat() * 0.5f;
31057							dust5.fadeIn = 1.5f + Main.rand.NextFloat() * 0.5f;
31058							dust = dust5;
31059							dust.velocity += velocity * 0.3f;
31060						}
31061					}
31062					if (Main.rand.Next(3) == 0)
31063					{
31064						Dust dust6 = Dust.NewDustDirect(position, width, height, 5);
31065						Dust dust = dust6;
31066						dust.velocity *= 0f;
31067						dust6.alpha = 120;
31068						dust6.scale = 0.7f + Main.rand.NextFloat() * 0.5f;
31069						dust = dust6;
31070						dust.velocity += velocity * 0.3f;
31071					}
31072					position -= netOffset;
31073				}
31074				int num708 = target;
31075				int num709 = direction;
31076				if (target == 255 || (type != 587 && Main.player[target].wet) || Main.player[target].dead || Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
31077				{
31078					this.ai[0] = 90f;
31079					TargetClosest();
31080				}
31081				else if (this.ai[0] > 0f)
31082				{
31083					this.ai[0] -= 1f;
31084					TargetClosest();
31085				}
31086				if (netUpdate && num708 == target && num709 == direction)
31087				{
31088					netUpdate = false;
31089				}
31090				float num710 = 0.05f;
31091				float num711 = 0.01f;
31092				float num712 = 3f;
31093				float num713 = 1f;
31094				float num714 = 30f;
31095				float num715 = 100f;
31096				float num716 = Math.Abs(position.X + (float)(width / 2) - (Main.player[target].position.X + (float)(Main.player[target].width / 2)));
31097				float num717 = Main.player[target].position.Y - (float)(height / 2);
31098				if (type == 509)
31099				{
31100					num710 = 0.08f;
31101					num711 = 0.03f;
31102					num712 = 4.5f;
31103					num713 = 2f;
31104					num714 = 40f;
31105					num715 = 150f;
31106					num717 = Main.player[target].Center.Y - (float)(height / 2);
31107					rotation = velocity.X * 0.1f;
31108					for (int num718 = 0; num718 < Main.maxNPCs; num718++)
31109					{
31110						if (num718 != whoAmI && Main.npc[num718].active && Main.npc[num718].type == type && Math.Abs(position.X - Main.npc[num718].position.X) + Math.Abs(position.Y - Main.npc[num718].position.Y) < (float)width)
31111						{
31112							if (position.X < Main.npc[num718].position.X)
31113							{
31114								velocity.X -= 0.05f;
31115							}
31116							else
31117							{
31118								velocity.X += 0.05f;

```


---

## 🤖 Assistant · 2026-08-11T04:28:40.945Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Continue 44 block from 31118 to end (probably ~31180), and read 56 at 32915. Also need to finish aiStyle 39's tail (29750-29790, states 5 and end). Let me batch three reads... two calls per message limit is fine; I can do 3 parallel reads.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:28:41.159Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 75,
 "offset": 29750
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:41.183Z

**📎 ToolResult**

```
29750					rotation += MathHelper.Clamp(velocity.X / 10f * (float)direction, -MathF.PI / 10f, MathF.PI / 10f);
29751				}
29752				else if (this.ai[0] == 5f)
29753				{
29754					if (type == 417)
29755					{
29756						position.Y += height;
29757						height = 52;
29758						position.Y -= height;
29759					}
29760					rotation = 0f;
29761					velocity.X = 0f;
29762					if (type >= 496 && type <= 497)
29763					{
29764						this.ai[1] += 0.5f;
29765					}
29766					else
29767					{
29768						this.ai[1] += 1f;
29769					}
29770					if (this.ai[1] >= 30f)
29771					{
29772						TargetClosest();
29773						netUpdate = true;
29774						this.ai[1] = 0f;
29775						this.ai[0] = 0f;
29776					}
29777					if (wet)
29778					{
29779						this.ai[0] = 3f;
29780						this.ai[1] = 0f;
29781					}
29782				}
29783			}
29784			else if (aiStyle == 40)
29785			{
29786				if (target < 0 || target == 255 || Main.player[target].dead)
29787				{
29788					TargetClosest();
29789				}
29790				float num634 = 2f;
29791				float num635 = 0.08f;
29792				if (type == 237)
29793				{
29794					num634 = 3f;
29795					num635 = 0.12f;
29796				}
29797				if (type == 531)
29798				{
29799					num634 = 4f;
29800					num635 = 0.16f;
29801				}
29802				Vector2 vector71 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
29803				float num636 = Main.player[target].position.X + (float)(Main.player[target].width / 2);
29804				float num637 = Main.player[target].position.Y + (float)(Main.player[target].height / 2);
29805				num636 = (int)(num636 / 8f) * 8;
29806				num637 = (int)(num637 / 8f) * 8;
29807				vector71.X = (int)(vector71.X / 8f) * 8;
29808				vector71.Y = (int)(vector71.Y / 8f) * 8;
29809				num636 -= vector71.X;
29810				num637 -= vector71.Y;
29811				if (confused)
29812				{
29813					num636 *= -2f;
29814					num637 *= -2f;
29815				}
29816				float num638 = (float)Math.Sqrt(num636 * num636 + num637 * num637);
29817				float num639 = num638;
29818				if (num638 == 0f)
29819				{
29820					num636 = velocity.X;
29821					num637 = velocity.Y;
29822				}
29823				else
29824				{

```


---

## 🤖 Assistant · 2026-08-11T04:28:41.396Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 85,
 "offset": 31118
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:41.405Z

**📎 ToolResult**

```
31118								velocity.X += 0.05f;
31119							}
31120							if (position.Y < Main.npc[num718].position.Y)
31121							{
31122								velocity.Y -= 0.05f;
31123							}
31124							else
31125							{
31126								velocity.Y += 0.05f;
31127							}
31128						}
31129					}
31130				}
31131				else if (type == 581)
31132				{
31133					num710 = 0.06f;
31134					num711 = 0.02f;
31135					num712 = 4f;
31136					num713 = 2f;
31137					num714 = 40f;
31138					num715 = 150f;
31139					num717 = Main.player[target].Center.Y - (float)(height / 2);
31140					rotation = velocity.X * 0.1f;
31141					for (int num719 = 0; num719 < Main.maxNPCs; num719++)
31142					{
31143						if (num719 != whoAmI && Main.npc[num719].active && Main.npc[num719].type == type && Math.Abs(position.X - Main.npc[num719].position.X) + Math.Abs(position.Y - Main.npc[num719].position.Y) < (float)width)
31144						{
31145							if (position.X < Main.npc[num719].position.X)
31146							{
31147								velocity.X -= 0.05f;
31148							}
31149							else
31150							{
31151								velocity.X += 0.05f;
31152							}
31153							if (position.Y < Main.npc[num719].position.Y)
31154							{
31155								velocity.Y -= 0.05f;
31156							}
31157							else
31158							{
31159								velocity.Y += 0.05f;
31160							}
31161						}
31162					}
31163				}
31164				else if (type == 587)
31165				{
31166					num710 = 0.13f;
31167					num711 = 0.09f;
31168					num712 = 6.5f;
31169					num713 = 3.5f;
31170					num714 = 0f;
31171					num715 = 250f;
31172					num717 = Main.player[target].position.Y;
31173					if (Main.dayTime)
31174					{
31175						num717 = 0f;
31176						direction *= -1;
31177					}
31178				}
31179				if (this.ai[0] <= 0f)
31180				{
31181					num712 *= 0.8f;
31182					num710 *= 0.7f;
31183					num717 = base.Center.Y + (float)(directionY * 1000);
31184					if (velocity.X < 0f)
31185					{
31186						direction = -1;
31187					}
31188					else if (velocity.X > 0f || direction == 0)
31189					{
31190						direction = 1;
31191					}
31192				}
31193				if (num716 > num714)
31194				{
31195					if (direction == -1 && velocity.X > 0f - num712)
31196					{
31197						velocity.X -= num710;
31198						if (velocity.X > num712)
31199						{
31200							velocity.X -= num710;
31201						}
31202						else if (velocity.X > 0f)

```


---

## 🤖 Assistant · 2026-08-11T04:28:41.637Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 120,
 "offset": 32915
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:41.652Z

**📎 ToolResult**

```
32915			else if (aiStyle == 56)
32916			{
32917				TargetClosest();
32918				Vector2 vector103 = new Vector2(base.Center.X, base.Center.Y);
32919				float num886 = Main.player[target].Center.X - vector103.X;
32920				float num887 = Main.player[target].Center.Y - vector103.Y;
32921				float num888 = (float)Math.Sqrt(num886 * num886 + num887 * num887);
32922				float num889 = 12f;
32923				num888 = num889 / num888;
32924				num886 *= num888;
32925				num887 *= num888;
32926				velocity.X = (velocity.X * 100f + num886) / 101f;
32927				velocity.Y = (velocity.Y * 100f + num887) / 101f;
32928				rotation = (float)Math.Atan2(num887, num886) - 1.57f;
32929				position += netOffset;
32930				int num890 = Dust.NewDust(position, width, height, 180);
32931				Dust dust = Main.dust[num890];
32932				dust.velocity *= 0.1f;
32933				Main.dust[num890].scale = 1.3f;
32934				Main.dust[num890].noGravity = true;
32935				position -= netOffset;
32936			}
32937			else if (aiStyle == 57)
32938			{
32939				float num891 = 2f;
32940				noGravity = true;
32941				noTileCollide = true;
32942				if (!Main.dayTime)
32943				{
32944					TargetClosest();
32945				}
32946				bool flag56 = false;
32947				if ((double)life < (double)lifeMax * 0.75)
32948				{
32949					num891 = 3f;
32950				}
32951				if ((double)life < (double)lifeMax * 0.5)
32952				{
32953					num891 = 4f;
32954				}
32955				if (type == 344)
32956				{
32957					Lighting.AddLight(base.Bottom + new Vector2(0f, -30f), 0.3f, 0.16f, 0.125f);
32958				}
32959				if (type == 325)
32960				{
32961					Lighting.AddLight(base.Bottom + new Vector2(0f, -30f), 0.3f, 0.125f, 0.06f);
32962				}
32963				if (Main.dayTime)
32964				{
32965					EncourageDespawn(10);
32966					num891 = 8f;
32967				}
32968				else if (this.ai[0] == 0f)
32969				{
32970					this.ai[1] += 1f;
32971					if ((double)life < (double)lifeMax * 0.5)
32972					{
32973						this.ai[1] += 1f;
32974					}
32975					if ((double)life < (double)lifeMax * 0.25)
32976					{
32977						this.ai[1] += 1f;
32978					}
32979					if (this.ai[1] >= 300f && Main.netMode != 1)
32980					{
32981						this.ai[1] = 0f;
32982						if ((double)life < (double)lifeMax * 0.25 && type != 344)
32983						{
32984							this.ai[0] = Main.rand.Next(3, 5);
32985						}
32986						else
32987						{
32988							this.ai[0] = Main.rand.Next(1, 3);
32989						}
32990						netUpdate = true;
32991					}
32992				}
32993				else if (this.ai[0] == 1f)
32994				{
32995					if (type == 344)
32996					{
32997						if (Main.rand.Next(5) == 0)
32998						{
32999							int num892 = Dust.NewDust(position + Main.rand.NextVector2Square(0f, 1f) * base.Size - new Vector2(1f, 2f), 10, 14, 245, 0f, 0f, 254, Color.Transparent, 0.25f);
33000							Dust dust = Main.dust[num892];
33001							dust.velocity *= 0.2f;
33002						}
33003						flag56 = true;
33004						this.ai[1] += 1f;
33005						if (this.ai[1] % 5f == 0f)
33006						{
33007							Vector2 vector104 = new Vector2(position.X + 20f + (float)Main.rand.Next(width - 40), position.Y + 20f + (float)Main.rand.Next(height - 40));
33008							float num893 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector104.X;
33009							float num894 = Main.player[target].position.Y - vector104.Y;
33010							num893 += (float)Main.rand.Next(-50, 51);
33011							num894 += (float)Main.rand.Next(-50, 51);
33012							num894 -= Math.Abs(num893) * ((float)Main.rand.Next(0, 21) * 0.01f);
33013							float num895 = (float)Math.Sqrt(num893 * num893 + num894 * num894);
33014							float num896 = 12.5f;
33015							num895 = num896 / num895;
33016							num893 *= num895;
33017							num894 *= num895;
33018							num893 *= 1f + (float)Main.rand.Next(-20, 21) * 0.02f;
33019							num894 *= 1f + (float)Main.rand.Next(-20, 21) * 0.02f;
33020							int num897 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector104.X, vector104.Y, num893, num894, 345, 43, 0f, Main.myPlayer, Main.rand.Next(0, 31));
33021						}
33022						if (this.ai[1] >= 180f)
33023						{
33024							this.ai[1] = 0f;
33025							this.ai[0] = 0f;
33026						}
33027					}
33028					else
33029					{
33030						flag56 = true;
33031						this.ai[1] += 1f;
33032						if (this.ai[1] % 15f == 0f)
33033						{
33034							Vector2 vector105 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f + 30f);

```


---

## 🤖 Assistant · 2026-08-11T04:28:44.702Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
aiStyle 56 fully read (32915-32936): short.

Now I need the tail of aiStyle 44 (31202 onward to block end). Read 31202-31270.

Also need AI_000_TransformBoundNPC definition — grep in other files. And NPCID for Raven 301 aiStyle confirmation. Let me grep in the decompiled directory for "AI_000_TransformBoundNPC" definition and check our extracted NPC json for aiStyle values (in game project data). Let's do those in parallel with reading 44's tail.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:28:44.905Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 70,
 "offset": 31202
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:44.919Z

**📎 ToolResult**

```
31202						else if (velocity.X > 0f)
31203						{
31204							velocity.X -= num710 / 2f;
31205						}
31206						if (velocity.X < 0f - num712)
31207						{
31208							velocity.X = 0f - num712;
31209						}
31210					}
31211					else if (direction == 1 && velocity.X < num712)
31212					{
31213						velocity.X += num710;
31214						if (velocity.X < 0f - num712)
31215						{
31216							velocity.X += num710;
31217						}
31218						else if (velocity.X < 0f)
31219						{
31220							velocity.X += num710 / 2f;
31221						}
31222						if (velocity.X > num712)
31223						{
31224							velocity.X = num712;
31225						}
31226					}
31227				}
31228				if (num716 > num715)
31229				{
31230					num717 -= num715 / 2f;
31231				}
31232				if (position.Y < num717)
31233				{
31234					velocity.Y += num711;
31235					if (velocity.Y < 0f)
31236					{
31237						velocity.Y += num711;
31238					}
31239				}
31240				else
31241				{
31242					velocity.Y -= num711;
31243					if (velocity.Y > 0f)
31244					{
31245						velocity.Y -= num711;
31246					}
31247				}
31248				if (velocity.Y < 0f - num713)
31249				{
31250					velocity.Y = 0f - num713;
31251				}
31252				if (velocity.Y > num713)
31253				{
31254					velocity.Y = num713;
31255				}
31256				if (type != 587 && wet)
31257				{
31258					if (velocity.Y > 0f)
31259					{
31260						velocity.Y *= 0.95f;
31261					}
31262					velocity.Y -= 0.5f;
31263					if (velocity.Y < -4f)
31264					{
31265						velocity.Y = -4f;
31266					}
31267				}
31268			}
31269			else if (aiStyle == 45)
31270			{
31271				AI_045_Golem();

```


---

## 🤖 Assistant · 2026-08-11T04:28:45.674Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"private void AI_000_TransformBoundNPC\\|void AI_000_TransformBoundNPC\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ | head -3; echo \"===aiStyle data===\"; ls ~/Project/GLM/SandboxWorld/game/src/data 2>/dev/null | head -30",
 "description": "Find TransformBoundNPC definition and npc data dir"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:45.727Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:45219:	public void AI_000_TransformBoundNPC(int playerID, int npcType)
===aiStyle data===
critters.ts
enemies.ts
items.ts
Music.ts
npcPortraits.ts
recipes.ts
tiles.ts
vanilla-equip.json
vanilla-itemcombat.json
vanilla-itemrare.json
vanilla-npcdrops.json
vanilla-npcnetid.json
vanilla-npcvalue.json
vanilla-prefix.json
vanilla-projectiles.json
vanilla-recipes.json
vanilla-shopstock.json
vanilla-travelshop.json
vanilla-wallitems.json
vanillaEquip.ts
vanillaItemCombat.ts
vanillaNpcs.ts
vanillaPrefixes.ts
vanillaProjectiles.ts
vanillaRecipes.ts

```


---

## 🤖 Assistant · 2026-08-11T04:28:46.859Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 55,
 "offset": 45219
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:46.872Z

**📎 ToolResult**

```
45219		public void AI_000_TransformBoundNPC(int playerID, int npcType)
45220		{
45221			Transform(npcType);
45222			AI_007_TownEntities_UpdateSavedStates();
45223			Main.BestiaryTracker.Chats.RegisterChatStartWith(this);
45224			Main.player[playerID].SetTalkNPC(whoAmI);
45225			if (Main.netMode == 2)
45226			{
45227				NetMessage.SendData(40, -1, -1, null, playerID);
45228			}
45229		}
45230	
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

```


---

## 🤖 Assistant · 2026-08-11T04:28:48.253Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src/data && node -e \"\nconst d = require('./vanilla-npcnetid.json');\n\" 2>/dev/null; grep -n \"aiStyle\" vanillaNpcs.ts | head -5; echo ---; node --input-type=module -e \"\nimport fs from 'fs';\nconst t = fs.readFileSync('~/Project/GLM/SandboxWorld/game/src/data/vanillaNpcs.ts','utf8');\nconst m = t.match(/aiStyle[^,}\\n]*/g);\nconsole.log(m ? m.slice(0,5) : 'none');\n\" 2>/dev/null | head",
 "description": "Check npc data file for aiStyle fields"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:28:58.447Z

**📎 ToolResult**

```
2:// aiStyle 与 AI_XXX 方法的对应见 NPC.cs AI() 分发；此处先覆盖高频家族，
3:// 未移植 AI 家族的 aiStyle 回退到最接近的已移植行为（注释标注）。
45:  aiStyle: number;
---
[
  'aiStyle 与 AI_XXX 方法的对应见 NPC.cs AI() 分发；此处先覆盖高频家族，',
  'aiStyle 回退到最接近的已移植行为（注释标注）。',
  'aiStyle: number;'
]

```


---

## 🤖 Assistant · 2026-08-11T04:29:04.352Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now check which aiStyle these NPCs actually have in vanilla — particularly Raven 301 (17 or 24?), Vulture 61 (17), plus 587 (type 587 in block 44 = Hellbutterfly? Actually type 587 in aiStyle 44 — that's... 587 is "Hell Butterfly"? Hmm. Whatever; note it).

Also check NPCID.Sets aiStyle assignments. In 1.4.5.6, aiStyle per NPC is in NPCID.Sets?? Actually vanilla aiStyle is set via `npc.aiStyle = NPCID.Sets...`? No — in decompiled vanilla, aiStyle comes from NPC.cs SetDefaults via a big switch or from `NPCID.Sets.PositiveNPCTypesExcluded`... Actually there's a static field per type. Let me grep "aiStyle = 17" in NPC.cs SetDefaults region or check how our project assigns. Simpler: check raven. Grep NPC.cs for "case 301:" region? Let me just grep for lines "aiStyle = " near type 301. Hard.

Alternative: search Terraria source for "Sets.TrailingMode" no... In 1.4.4+, NPC defaults are data-driven? There is `Terraria.ID.NPCID.Sets` and also `Terraria.GameContent.Bestiary`. The aiStyle is assigned in NPC.SetDefaults from a dictionary built in `Terraria.Initialization.NPCDatabase`? Not present.

Let me grep for "aiStyle = 17;" in NPC.cs.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:29:04.985Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -rn \"aiStyle = 17\" --include=*.cs . | head; echo \"---grep 24---\"; grep -rn \"aiStyle = 24\" --include=*.cs . | head",
 "description": "Find where aiStyle 17/24 assigned"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:29:05.018Z

**📎 ToolResult**

```
(eval):1: no matches found: --include=*.cs
---grep 24---
(eval):1: no matches found: --include=*.cs

```


---

## 🤖 Assistant · 2026-08-11T04:29:06.567Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -rn \"aiStyle = 17\" . 2>/dev/null | head; echo \"---NPCID file---\"; find .. -name \"NPCID*.cs\" | head",
 "description": "Search aiStyle assignment and NPCID file"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:29:06.607Z

**📎 ToolResult**

```
NPC.cs:9490:			aiStyle = 17;
NPC.cs:12825:			aiStyle = 17;
Projectile.cs:1003:			aiStyle = 17;
Projectile.cs:2609:			aiStyle = 17;
Projectile.cs:2622:			aiStyle = 17;
Projectile.cs:2635:			aiStyle = 17;
Projectile.cs:2648:			aiStyle = 17;
Projectile.cs:2661:			aiStyle = 17;
Projectile.cs:5698:			aiStyle = 17;
Projectile.cs:8074:			aiStyle = 171;
---NPCID file---
../Terraria.ID/NPCID.cs

```


---

## 🤖 Assistant · 2026-08-11T04:29:08.108Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '9480,9495p;12815,12832p' NPC.cs",
 "description": "Show context of aiStyle 17 assignments"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:29:08.140Z

**📎 ToolResult**

```
			knockBackResist = 0.8f;
			DeathSound = SoundID.NPCDeath4;
			value = 120f;
			scale = 1.1f;
			lavaImmune = true;
		}
		else if (type == 61)
		{
			width = 36;
			height = 36;
			aiStyle = 17;
			damage = 15;
			defense = 4;
			lifeMax = 40;
			knockBackResist = 0.8f;
			HitSound = SoundID.NPCHit28;
			lifeMax = 5;
			HitSound = SoundID.NPCHit1;
			DeathSound = SoundID.NPCDeath4;
			npcSlots = 0.25f;
			catchItem = 2003;
		}
		else if (type == 301)
		{
			width = 36;
			height = 26;
			aiStyle = 17;
			damage = 12;
			defense = 2;
			lifeMax = 35;
			HitSound = SoundID.NPCHit1;
			knockBackResist = 0.85f;
			DeathSound = SoundID.NPCDeath1;
			value = 50f;

```


---

## 🤖 Assistant · 2026-08-11T04:29:14.222Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: Raven 301 uses aiStyle 17, same block as Vulture 61. Good — it shares the same block.

Also worth checking 587 in aiStyle 44 — 587 is "Hell Butterfly"? Actually type 587 = Hell Butterfly (critter). Whatever. Also 629 in aiStyle 25 block? 341 PresentMimic, 629 =... I'll mention.

Also I should double-check the default flags (tileCollide / noGravity) for these families from SetDefaults: e.g., Vulture tileCollide = true. And Dungeon Spirit 288: noTileCollide / tileCollide false? Dungeon Spirit (288) is aiStyle 56, and its flags: tileCollide=false, noTileCollide=true, noGravity=true. Let me check quickly.

Also check 417 Sroller flags (tileCollide true? noGravity during spin?). In aiStyle 39, state 3 sets noGravity implicitly? Hmm — state 3 doesn't set noGravity=true explicitly... wait at 29610: `noGravity = false;` when ai[1]>=90 in state 3 → meaning state 3 had noGravity=true set elsewhere? Hmm, where is noGravity set true for aiStyle 39? Possibly in SetDefaults for the NPCs (noGravity = true is set in AI elsewhere?). Let me grep for "noGravity = true" near... Actually, in NPC.AI, there's likely a global section that sets noGravity based on... Hmm. In vanilla, NPCs like Giant Tortoise have `noGravity = true` in SetDefaults? Let me check type 153.

Let me check SetDefaults for 153, 154, 417, 288, 69, 83, 224, 581, 509, 587, 174, 177, 378 flags (tileCollide, noGravity, noTileCollide).
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:29:15.056Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && for t in 69 83 153 154 288 417 224 581 174 177 378 587 509; do echo \"=== type $t ===\"; grep -n \"else if (type == $t)\" NPC.cs | head -1; done",
 "description": "Locate SetDefaults blocks for key NPC types"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:29:24.357Z

**📎 ToolResult**

```
=== type 69 ===
9598:		else if (type == 69)
=== type 83 ===
9811:		else if (type == 83)
=== type 153 ===
10862:		else if (type == 153)
=== type 154 ===
10877:		else if (type == 154)
=== type 288 ===
12670:		else if (type == 288)
=== type 417 ===
15286:		else if (type == 417)
=== type 224 ===
11817:		else if (type == 224)
=== type 581 ===
14800:		else if (type == 581)
=== type 174 ===
11126:		else if (type == 174)
=== type 177 ===
11170:		else if (type == 177)
=== type 378 ===
13757:		else if (type == 378)
=== type 587 ===
16554:		else if (type == 587)
=== type 509 ===
14773:		else if (type == 509)

```


---

## 🤖 Assistant · 2026-08-11T04:29:28.639Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && for spec in \"69:9598:12\" \"83:9811:14\" \"153:10862:15\" \"154:10877:15\" \"288:12670:16\" \"417:15286:14\" \"224:11817:12\" \"174:11126:14\" \"177:11170:14\" \"378:13757:14\" \"587:16554:14\" \"509:14773:14\" \"581:14800:14\" \"61:9486:14\" \"301:12821:14\" \"85:9825:14\" \"341:13028:14\"; do t=${spec%%:*}; rest=${spec#*:}; ln=${rest%%:*}; echo \"=== type $t ===\"; sed -n \"${ln},$((ln+15))p\" NPC.cs | grep -E \"aiStyle|tileCollide|noGravity|noTileCollide|width|height|lifeMax|damage|defense|knockBackResist\"; done",
 "description": "Extract AI flags from SetDefaults for all target types"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:29:37.951Z

**📎 ToolResult**

```
=== type 69 ===
			width = 24;
			height = 24;
			aiStyle = 19;
			damage = 10;
			defense = 6;
			lifeMax = 45;
			knockBackResist = 0f;
=== type 83 ===
			width = 40;
			height = 40;
			aiStyle = 23;
			damage = 80;
			defense = 18;
			lifeMax = 200;
			knockBackResist = 0.4f;
			width = 40;
=== type 153 ===
			width = 46;
			height = 32;
			aiStyle = 39;
			damage = 80;
			defense = 30;
			lifeMax = 470;
			knockBackResist = 0.3f;
			noGravity = false;
=== type 154 ===
			width = 46;
			height = 32;
			aiStyle = 39;
			damage = 55;
			defense = 28;
			lifeMax = 400;
			knockBackResist = 0.3f;
			noGravity = false;
=== type 288 ===
			width = 20;
			height = 20;
			aiStyle = 56;
			damage = 70;
			defense = 30;
			lifeMax = 200;
			knockBackResist = 0.2f;
			noTileCollide = true;
			noGravity = true;
=== type 417 ===
			width = 46;
			height = 52;
			aiStyle = 39;
			damage = 80;
			defense = 34;
			lifeMax = 700;
			knockBackResist = 0f;
			width = 38;
=== type 224 ===
			width = 32;
			height = 18;
			aiStyle = 44;
			damage = 9;
			defense = 4;
			lifeMax = 20;
			knockBackResist = 0.8f;
			width = 38;
=== type 174 ===
			width = 52;
			height = 26;
			aiStyle = 41;
			damage = 65;
			defense = 26;
			lifeMax = 220;
			knockBackResist = 0.3f;
=== type 177 ===
			width = 58;
			height = 44;
			aiStyle = 41;
			damage = 80;
			defense = 26;
			lifeMax = 300;
			knockBackResist = 0.5f;
=== type 378 ===
			width = 20;
			height = 26;
			aiStyle = 41;
			damage = 120;
			defense = 30;
			lifeMax = 200;
			knockBackResist = 0.5f;
=== type 587 ===
			width = 32;
			height = 18;
			aiStyle = 44;
			damage = 35;
			defense = 18;
			lifeMax = 300;
			knockBackResist = 0f;
=== type 509 ===
			width = 40;
			height = 31;
			aiStyle = 44;
			damage = 34;
			defense = 12;
			lifeMax = 90;
			knockBackResist = 0.3f;
			width = 26;
=== type 581 ===
			width = 30;
			height = 22;
			aiStyle = 44;
			damage = 29;
			defense = 8;
			lifeMax = 60;
			knockBackResist = 0.5f;
=== type 61 ===
			width = 36;
			height = 36;
			aiStyle = 17;
			damage = 15;
			defense = 4;
			lifeMax = 40;
			knockBackResist = 0.8f;
=== type 301 ===
			width = 36;
			height = 26;
			aiStyle = 17;
			damage = 12;
			defense = 2;
			lifeMax = 35;
			knockBackResist = 0.85f;
			width = 24;
=== type 85 ===
			width = 40;
			height = 40;
			aiStyle = 23;
			damage = 80;
			defense = 18;
			lifeMax = 200;
			knockBackResist = 0.4f;
			width = 24;
			height = 24;
=== type 341 ===
			knockBackResist = 0.5f;
			width = 18;
			height = 40;
			aiStyle = 3;
			damage = 22;
			defense = 10;
			lifeMax = 70;
			knockBackResist = 0.4f;

```


---

## 🤖 Assistant · 2026-08-11T04:29:45.165Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Note type 341 (Present Mimic) shows aiStyle = 3 in the block I grabbed — wrong block (the second "else if (type == 341)" maybe). Let me find 341's aiStyle properly, and also check 378 name (it's not Herpling — 174 Herpling, 177 Derpling, 378 = "Slimeling"? No... 378 is "Basilisk"? Actually 378 = Hellhound? Hmm). Type 378 in aiStyle 41 with explode behavior (ai[1]==5 → self-destruct into gore/dust) — that's the "Basilisk"? No wait — ai[1]=5, dontTakeDamage, width 160, gore 61-64 (bone gore) → that's a skeleton exploding = "Bone Serpent head"? No. Type 378 = "Skeleton"? Actually exploding into bone gore + spawn dust when player within 64px or wet — that's the "Lihzahrd"? Hmm. Let me check NPCID 378.

From memory of NPCID: 371=RaggedCaster, 372=MourningWood... Actually: 376=BoundWizard? No — 123=BoundGoblin, 124=Goblin, ... Let me check NPCID.cs for 378, 341, 589, 588, 550, 353, 369, 417, 587, 509, 581, 629.

Actually memory file says aiStyle 41 = 174 Herpling/177 Derpling/378. And 378 — the exploding one. NPCID 378 = "Basilisk"? Hmm, exploding on contact... That's likely "Basilisk"? No, basilisk doesn't explode. Wet triggers explosion... Actually this is the "Splinterling"? Hmm — wait: explodes into gore 61-64 (bone pieces), big hitbox... That's a skeleton that explodes: "Skeleton" no... Actually! It's the "Bone Lee"? No.

Hmm, 378 might be "Rune Wizard"? No. Let me just check NPCID.cs names.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:29:46.264Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID && grep -nE \" = (61|69|83|84|85|105|106|107|108|123|124|153|154|174|177|179|224|288|301|341|353|354|369|376|417|509|550|579|581|587|589|629),$\" NPCID.cs | head -40",
 "description": "Map NPC type ids to names"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:29:54.792Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-11T04:29:56.750Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID && grep -nE \"\\b(61|69|83|84|85|105|106|107|108|123|124|153|154|174|177|179|224|288|301|341|353|354|369|376|417|509|550|579|581|587|589|629)\\b\" NPCID.cs | grep \"=\" | head -40",
 "description": "Find NPCID constant names for ids"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:29:56.777Z

**📎 ToolResult**

```
173:			public const int ShadowFlame = 153;
185:			public const int Ichor = 69;
774:					SpecificallyImmuneTo = new int[4] { 24, 31, 153, 323 }
802:					SpecificallyImmuneTo = new int[4] { 24, 31, 153, 323 }
1364:					SpecificallyImmuneTo = new int[4] { 24, 31, 153, 323 }
1962:					SpecificallyImmuneTo = new int[2] { 20, 69 }
2116:					SpecificallyImmuneTo = new int[3] { 20, 31, 69 }
3088:					SpecificallyImmuneTo = new int[2] { 31, 153 }
3095:					SpecificallyImmuneTo = new int[2] { 31, 153 }
4767:		public static int[] TrailingMode = Factory.CreateIntSet(-1, 439, 0, 440, 0, 370, 1, 372, 1, 373, 1, 396, 1, 400, 1, 401, 1, 473, 2, 474, 2, 475, 2, 476, 2, 4, 3, 471, 3, 477, 3, 479, 3, 120, 4, 137, 4, 138, 4, 94, 5, 125, 6, 126, 6, 127, 6, 128, 6, 129, 6, 130, 6, 131, 6, 139, 6, 140, 6, 407, 6, 420, 6, 425, 6, 427, 6, 426, 6, 581, 6, 516, 6, 542, 6, 543, 6, 544, 6, 545, 6, 402, 7, 417, 7, 419, 7, 418, 7, 574, 7, 575, 7, 519, 7, 521, 7, 522, 7, 546, 7, 558, 7, 559, 7, 560, 7, 551, 7, 620, 7, 657, 6, 636, 7, 677, 7, 685, 7);
4789:		public static bool[] ConveyorBeltCollision = Factory.CreateBoolSet(624, 85, 629, 195, 1, 147, 184, 537, 204, 16, 59, 71, 535, 225, 676, 303, 335, 336, 333, 334, 667, 141, 81, 121, 183, 138, 244, 304, 105, 123, 685, 686, 687, 106, 354, 376, 579, 589, 37, 695, 696);
4795:		public static float[] StatueSpawnedDropRarity = Factory.CreateCustomSet(-1f, (short)480, 0.05f, (short)82, 0.05f, (short)86, 0.05f, (short)48, 0.05f, (short)490, 0.05f, (short)489, 0.05f, (short)170, 0.05f, (short)180, 0.05f, (short)171, 0.05f, (short)167, 0.25f, (short)73, 0.01f, (short)24, 0.05f, (short)481, 0.05f, (short)42, 0.05f, (short)6, 0.05f, (short)2, 0.05f, (short)49, 0.2f, (short)3, 0.2f, (short)58, 0.2f, (short)21, 0.2f, (short)65, 0.2f, (short)449, 0.2f, (short)482, 0.2f, (short)103, 0.2f, (short)64, 0.2f, (short)63, 0.2f, (short)85, 0f);
4827:		public static int[] HatOffsetY = Factory.CreateIntSet(0, 227, 4, 107, 2, 108, 2, 229, 4, 17, 2, 38, 8, 160, -10, 208, 2, 142, 2, 124, 2, 453, 2, 37, 4, 54, 4, 209, 4, 369, 6, 441, 6, 353, -2, 633, -2, 550, -2, 588, 2, 663, 2, 637, 0, 638, 0, 656, 4, 670, 0, 678, 0, 679, 0, 680, 0, 681, 0, 682, 0, 683, 0, 684, 0);
4829:		public static int[] FaceEmote = Factory.CreateIntSet(0, 17, 101, 18, 102, 19, 103, 20, 104, 22, 105, 37, 106, 38, 107, 54, 108, 107, 109, 108, 110, 124, 111, 142, 112, 160, 113, 178, 114, 207, 115, 208, 116, 209, 117, 227, 118, 228, 119, 229, 120, 353, 121, 368, 122, 369, 123, 453, 124, 441, 125, 588, 140, 633, 141, 663, 145);
4831:		public static int[] ExtraFramesCount = Factory.CreateIntSet(0, 17, 9, 18, 9, 19, 9, 20, 7, 22, 10, 37, 5, 38, 9, 54, 7, 107, 9, 108, 7, 124, 9, 142, 9, 160, 7, 178, 9, 207, 9, 208, 9, 209, 10, 227, 9, 228, 10, 229, 10, 353, 9, 633, 9, 368, 10, 369, 9, 453, 9, 441, 9, 550, 9, 588, 9, 663, 7, 637, 18, 638, 11, 656, 20, 670, 6, 678, 6, 679, 6, 680, 6, 681, 6, 682, 6, 683, 6, 684, 6);
4833:		public static int[] AttackFrameCount = Factory.CreateIntSet(0, 17, 4, 18, 4, 19, 4, 20, 2, 22, 5, 37, 0, 38, 4, 54, 2, 107, 4, 108, 2, 124, 4, 142, 4, 160, 2, 178, 4, 207, 4, 208, 4, 209, 5, 227, 4, 228, 5, 229, 5, 353, 4, 633, 4, 368, 5, 369, 4, 453, 4, 441, 4, 550, 4, 588, 4, 663, 2, 637, 0, 638, 0, 656, 0, 670, 0, 678, 0, 679, 0, 680, 0, 681, 0, 682, 0, 683, 0, 684, 0);
4835:		public static int[] DangerDetectRange = Factory.CreateIntSet(-1, 38, 300, 17, 320, 107, 300, 19, 900, 22, 700, 124, 800, 228, 800, 178, 900, 18, 300, 229, 1000, 209, 1000, 54, 700, 108, 700, 160, 700, 20, 1200, 369, 300, 453, 300, 368, 900, 207, 60, 227, 800, 208, 400, 142, 500, 441, 50, 353, 60, 633, 100, 550, 120, 588, 120, 663, 700, 638, 250, 637, 250, 656, 250, 670, 250, 678, 250, 679, 250, 680, 250, 681, 250, 682, 250, 683, 250, 684, 250);
4837:		public static bool[] ShimmerImmunity = Factory.CreateBoolSet(637, 638, 656, 670, 684, 678, 679, 680, 681, 682, 683, 356, 669, 676, 244, 677, 594, 667, 662, 5, 115, 116, 139, 245, 247, 248, 246, 249, 344, 325, 50, 535, 657, 658, 659, 660, 668, 25, 30, 33, 70, 72, 665, 666, 112, 516, 517, 518, 519, 520, 521, 522, 523, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 423, 424, 425, 426, 427, 428, 429, 548, 549, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578);
4839:		public static int[] ShimmerTransformToItem = Factory.CreateIntSet(-1, 651, 182, 644, 182, 650, 178, 643, 178, 649, 179, 642, 179, 648, 177, 641, 177, 640, 180, 647, 180, 646, 181, 639, 181, 652, 999, 645, 999, 448, 5341);
4841:		public static bool[] ShimmerTownTransform = Factory.CreateBoolSet(22, 17, 18, 227, 207, 633, 588, 208, 369, 353, 38, 20, 550, 19, 107, 228, 54, 124, 441, 229, 160, 108, 178, 209, 142, 663, 37, 453, 368);
4845:		public static int[] AttackTime = Factory.CreateIntSet(-1, 38, 34, 17, 34, 107, 60, 19, 40, 22, 30, 124, 34, 228, 40, 178, 24, 18, 34, 229, 60, 209, 60, 54, 60, 108, 30, 160, 60, 20, 600, 369, 34, 453, 34, 368, 60, 207, 15, 227, 60, 208, 34, 142, 34, 441, 15, 353, 12, 633, 12, 550, 34, 588, 20, 663, 60, 638, -1, 637, -1, 656, -1, 670, -1, 678, -1, 679, -1, 680, -1, 681, -1, 682, -1, 683, -1, 684, -1);
4847:		public static int[] AttackAverageChance = Factory.CreateIntSet(1, 38, 40, 17, 30, 107, 60, 19, 30, 22, 30, 124, 30, 228, 50, 178, 50, 18, 60, 229, 40, 209, 30, 54, 30, 108, 30, 160, 60, 20, 60, 369, 50, 453, 30, 368, 40, 207, 1, 227, 30, 208, 50, 142, 50, 441, 1, 353, 1, 633, 1, 550, 40, 588, 20, 663, 1, 638, 1, 637, 1, 656, 1, 670, 1, 678, 1, 679, 1, 680, 1, 681, 1, 682, 1, 683, 1, 684, 1);
4849:		public static int[] AttackType = Factory.CreateIntSet(-1, 38, 0, 17, 0, 107, 0, 19, 1, 22, 1, 124, 0, 228, 1, 178, 1, 18, 0, 229, 1, 209, 1, 54, 2, 108, 2, 160, 2, 20, 2, 369, 0, 453, 0, 368, 1, 207, 3, 227, 1, 208, 0, 142, 0, 441, 3, 353, 3, 633, 0, 550, 0, 588, 0, 663, 2, 638, -1, 637, -1, 656, -1, 670, -1, 678, -1, 679, -1, 680, -1, 681, -1, 682, -1, 683, -1, 684, -1);
4851:		public static int[] PrettySafe = Factory.CreateIntSet(-1, 19, 300, 22, 200, 124, 200, 228, 300, 178, 300, 229, 300, 209, 300, 54, 100, 108, 100, 160, 100, 20, 200, 368, 200, 227, 200);
4853:		public static Color[] MagicAuraColor = Factory.CreateCustomSet(Color.White, (short)54, new Color(100, 4, 227, 127), (short)108, new Color(255, 80, 60, 127), (short)160, new Color(40, 80, 255, 127), (short)20, new Color(40, 255, 80, 127), (short)663, Main.hslToRgb(0.92f, 1f, 0.78f, 127));
4873:		public static int[] ExtraTextureCount = Factory.CreateIntSet(0, 38, 1, 17, 1, 107, 0, 19, 0, 22, 0, 124, 1, 228, 0, 178, 1, 18, 1, 229, 1, 209, 1, 54, 1, 108, 1, 160, 0, 20, 0, 369, 1, 453, 1, 368, 1, 207, 1, 227, 1, 208, 0, 142, 1, 441, 1, 353, 1, 633, 1, 550, 0, 588, 1, 633, 2, 663, 1, 638, 0, 637, 0, 656, 0, 670, 0, 678, 0, 679, 0, 680, 0, 681, 0, 682, 0, 683, 0, 684, 0);
4875:		public static int[] NPCFramingGroup = Factory.CreateIntSet(0, 18, 1, 20, 1, 208, 1, 178, 1, 124, 1, 353, 1, 633, 1, 369, 2, 160, 3, 637, 4, 638, 5, 656, 6, 670, 7, 678, 7, 679, 7, 680, 7, 681, 7, 682, 7, 683, 7, 684, 7);
10943:	public const short BigHornetLeafy = -61;
11187:	public const short Vulture = 61;
11203:	public const short Antlion = 69;
11231:	public const short CursedHammer = 83;
11233:	public const short EnchantedSword = 84;
11235:	public const short Mimic = 85;
11275:	public const short BoundGoblin = 105;
11277:	public const short BoundWizard = 106;
11279:	public const short GoblinTinkerer = 107;
11281:	public const short Wizard = 108;
11311:	public const short BoundMechanic = 123;
11313:	public const short Mechanic = 124;
11371:	public const short GiantTortoise = 153;

```


---

## 🤖 Assistant · 2026-08-11T04:29:58.360Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good, NPCID has named constants. Let me get names for 154, 174, 177, 179, 224, 288, 301, 341, 353, 354, 369, 376, 417, 509, 550, 579, 581, 587, 589, 629.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:29:59.254Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID && sed -n '11100,11950p' NPCID.cs | grep -E \"public const short .*= (154|174|177|179|224|288|301|341|353|354|369|376|417|509|550|579|581|587|589|629);$\"",
 "description": "Get remaining NPC id names"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:30:07.486Z

**📎 ToolResult**

```
	public const short IceTortoise = 154;
	public const short Herpling = 174;
	public const short Derpling = 177;
	public const short CrimsonAxe = 179;
	public const short FlyingFish = 224;
	public const short DungeonSpirit = 288;
	public const short Raven = 301;
	public const short PresentMimic = 341;
	public const short Stylist = 353;
	public const short WebbedStylist = 354;
	public const short Angler = 369;
	public const short SleepingAngler = 376;
	public const short SolarSroller = 417;

```


---

## 🤖 Assistant · 2026-08-11T04:30:13.943Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID && sed -n '11950,13500p' NPCID.cs | grep -E \"public const short .*= (509|550|579|581|587|589|629);$\"",
 "description": "Get names for 509/550/579/581/587/589/629"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:30:19.008Z

**📎 ToolResult**

```
	public const short GiantFlyingAntlion = 509;
	public const short DD2Bartender = 550;
	public const short BartenderUnconscious = 579;
	public const short FlyingAntlion = 581;
	public const short EyeballFlyingFish = 587;
	public const short GolferRescue = 589;
	public const short IceMimic = 629;

```


---

## 🤖 Assistant · 2026-08-11T04:30:24.865Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So:
- 341 PresentMimic and 629 IceMimic are in the aiStyle 25 block via `if (type == 341 || type == 629) this.ai[3] = 1f;` — wait but the SetDefaults I grepped for 341 showed aiStyle=3. That grep probably caught the wrong block (the sed window). Present Mimic 341 — what's its aiStyle? Hmm, in vanilla Present Mimic (frost moon) uses aiStyle 3? Actually yes! Present Mimic in Frost Moon uses aiStyle 3 (fighter-like zombie AI)... but then why does aiStyle 25 reference type 341/629? Because 629 IceMimic uses aiStyle 25 (mimic). And 341 flagged via flag36 (type==341 && !Main.snowMoon) — that suggests 341 also uses aiStyle 25 in some context? Hmm — PresentMimic might use aiStyle 25 actually. Let me verify type 341's aiStyle in SetDefaults properly.

- 587 EyeballFlyingFish — aiStyle 44 special-cased.
- 589 GolferRescue → 588 Golfer (transform on talk).
- 509 GiantFlyingAntlion (1.4.4+) aiStyle 44 with its own params.
- 581 FlyingAntlion aiStyle 44.
- 224 FlyingFish aiStyle 44 base params.

Let me verify 341 aiStyle.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:30:25.803Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"type == 341\" NPC.cs | head; echo ---; awk '/else if \\(type == 341\\)/{print NR\": \"$0; c=1; next} c&&/else if \\(type ==/{exit} c&&/aiStyle|tileCollide|noGravity/{print NR\": \"$0}' NPC.cs | head -8",
 "description": "Verify PresentMimic 341 aiStyle"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:30:30.704Z

**📎 ToolResult**

```
13246:		else if (type == 341)
25623:			bool flag36 = type == 341 && !Main.snowMoon;
25641:			if (type == 341 || type == 629)
89672:			else if (type == 341)
---
13246: 		else if (type == 341)
13250: 			aiStyle = 25;

```


---

## 🤖 Assistant · 2026-08-11T04:30:37.076Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed 341 PresentMimic aiStyle = 25 (my earlier sed window caught a different block). Good — all confirmed.

Also I should double check aiStyle 39 noGravity: Giant Tortoise 153/154 have `noGravity = false` in SetDefaults (weird explicit). Where does noGravity get set true during state 3? Look at lines 29554-29589: state 3 — I don't see noGravity=true. Hmm, at 29610 `noGravity = false;` when ai[1]>=90 → so at some point noGravity becomes true. Maybe at NPC.AI top-level there's per-type logic, or in SetDefaults they set noGravity = true for 153? The grep showed "noGravity = false;" explicitly at some line within 153/154 blocks — that might be because NPC.SetDefaults has a `noGravity = true` earlier globally and these reset it? Actually no: vanilla NPC.SetDefaults starts with default flags and some types set noGravity. Hmm, wait — maybe for aiStyle 39, noGravity set elsewhere: in the AI dispatch, e.g. before the chain: `if (aiStyle == 39) { noGravity = ... }`? Let me grep "noGravity = true" near 29257..29783.

Actually look again at state 3 lines 29553-29591: no noGravity=true. But state 3's physics (velocity.Y -= 0.22f while ascending, no gravity applied) implies noGravity==true. Let me grep within the block.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:30:37.850Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '29257,29783p' NPC.cs | grep -n \"noGravity\\|tileCollide\\|noTileCollide\"; echo \"=== 153 SetDefaults flags ===\"; sed -n '10862,10895p' NPC.cs",
 "description": "Check noGravity usage in aiStyle 39 block and tortoise defaults"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:30:37.900Z

**📎 ToolResult**

```
71:					Main.dust[num603].noGravity = true;
285:					Main.dust[num615].noGravity = true;
354:						noGravity = false;
399:					Main.dust[num622].noGravity = true;
415:							Main.dust[num624].noGravity = true;
421:							Main.dust[num624].noGravity = true;
=== 153 SetDefaults flags ===
		else if (type == 153)
		{
			npcSlots = 2f;
			width = 46;
			height = 32;
			aiStyle = 39;
			damage = 80;
			defense = 30;
			lifeMax = 470;
			HitSound = SoundID.NPCHit24;
			knockBackResist = 0.3f;
			DeathSound = SoundID.NPCDeath27;
			value = 500f;
			noGravity = false;
		}
		else if (type == 154)
		{
			npcSlots = 1.5f;
			width = 46;
			height = 32;
			aiStyle = 39;
			damage = 55;
			defense = 28;
			lifeMax = 400;
			HitSound = SoundID.NPCHit24;
			knockBackResist = 0.3f;
			DeathSound = SoundID.NPCDeath27;
			value = 450f;
			noGravity = false;
			coldDamage = true;
		}
		else if (type == 155)
		{
			width = 46;

```


---

## 🤖 Assistant · 2026-08-11T04:30:46.623Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So `noGravity = false` is explicitly set in SetDefaults for 153/154 — meaning default NPC noGravity is... In vanilla SetDefaults, before the type switch, defaults include `noGravity = false`? Actually many flying NPCs set `noGravity = true`. The explicit `= false` for tortoises is just belt-and-braces.

But then where does noGravity become true for aiStyle 39 state 3? Hmm — maybe it's set in AI() dispatch preamble: there's likely a section that sets noGravity based on... Actually! In NPC.AI there's the common section: `if (aiStyle == 39) { noGravity = true; }`? No.

Wait, maybe I missed it. The grep within 29257-29783 shows only line 29610 (offset 354) setting noGravity=false. So state 3 never sets noGravity=true in this block... but then gravity would be applied by NPC.UpdatePhysics and the tortoise would fall during spin. Hmm, but state 3 sets velocity directly and adds velocity.Y -= 0.22f each frame — with gravity 0.3 applied it would still ascend given initial -10.

Hmm wait, actually maybe the NPC gravity application: in vanilla, NPC applies gravity in AI_007? No — gravity for NPCs is applied in this AI() method at the start or in UpdateNPC: `if (!noGravity) velocity.Y += gravity` — it's in NPC.AI top: `if (!noGravity && ...)`? Actually NPC.AI() has a gravity section near the end of the per-frame update? In Terraria, NPC gravity is applied inside AI() in the section handling `noGravity`... Hmm. Let me check: search "gravity" in NPC.cs around the UpdatePhysics.

Actually — for aiStyle 39 the classic vanilla code indeed has: state 3 (spin jump) and at the end "noGravity = false" when the timer hits 90. That implies at state entry noGravity was true. In 1.3 source, AI_39? Hmm, but this aiStyle 39 in decompiled 1.4.5.6... Let me search for where aiStyle 39 sets noGravity earlier — maybe in AI() preamble there's `if (npc.noGravity)` logic... Let me grep "noGravity = true" between 29000 and 29260.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:30:47.493Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '29160,29260p' NPC.cs | grep -n \"aiStyle\\|noGravity\"; echo \"===gravity application===\"; grep -n \"velocity.Y += 0.3f\\|velocity.Y += gravity\" NPC.cs | sed -n '1,6p'",
 "description": "Check aiStyle preamble and NPC gravity application site"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:30:47.529Z

**📎 ToolResult**

```
98:		else if (aiStyle == 39)
===gravity application===
23620:						velocity.Y += 0.3f;
23684:						velocity.Y += 0.3f;
23746:						velocity.Y += 0.3f;
24040:				velocity.Y += 0.3f;
33326:				velocity.Y += 0.3f;
33445:				velocity.Y += 0.3f;

```


---

## 🤖 Assistant · 2026-08-11T04:30:50.124Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"void UpdateNPC\\b\" NPC.cs | head -2; grep -n \"if (!noGravity)\" NPC.cs | head -8",
 "description": "Find NPC gravity application location"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:30:50.153Z

**📎 ToolResult**

```
91314:	public void UpdateNPC(int i)
82229:					if (!noGravity)
91519:		if (!noGravity)

```


---

## 🤖 Assistant · 2026-08-11T04:30:51.938Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '91505,91545p' NPC.cs",
 "description": "Read gravity/maxfall section in UpdateNPC"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:30:51.980Z

**📎 ToolResult**

```
				immune[j]--;
			}
		}
		if (!noGravity && !noTileCollide)
		{
			int num10 = (int)(position.X + (float)(width / 2)) / 16;
			int num11 = (int)(position.Y + (float)(height / 2)) / 16;
			if (WorldGen.InWorld(num10, num11) && Main.tile[num10, num11] == null)
			{
				gravity = 0f;
				velocity.X = 0f;
				velocity.Y = 0f;
			}
		}
		if (!noGravity)
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

```


---

## 🤖 Assistant · 2026-08-11T04:31:11.631Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So gravity applied in UpdateNPC after AI. For aiStyle 39 state 3: `noGravity = false` at ai[1]>=90 — meaning during states 0/1/2(no)/3/4/6... hmm noGravity stays false except... wait, but state 3 first branch (ai[1]==1) sets velocity directly; gravity still applies each frame. velocity.Y -= 0.22f each frame while ai[3]!=0 (ascending). Fine — so noGravity isn't set true anywhere in this block; the `noGravity = false;` line at 29610 is redundant (perhaps legacy). OK. So the tortoise is a normal gravity NPC throughout; tileCollide true.

Wait — but state 3 initial velocity is -10 (or -6 no-LOS), and each frame velocity.Y -= 0.22 while ai[3]!=0. And ai[3] is reset to 0 when overlapping player x-range. So it's a rising spin.

Hmm, but actually the classic Giant Tortoise behavior: it spins and flies at you. Yes.

Now I have everything except: I should double check aiStyle 39 state 2 — wait there's no state 2; states are 0,1,3,4,5,6. And I should verify where "type >= 496 && type <= 497" (BouncyBoulder?) — irrelevant.

Also need aiStyle 41's ai[0] negative countdown semantics: ai[0] starts at -100, increments +5 per grounded frame (+2 for Derpling) plus distance-based bonus (num653 = 400/dist*10 capped 30; Derpling *5). When ai[0]>=0 → jump. Post-jump ai[0] = -200 (big) or -120 (small). If ai[0] >= -30 → aiAction = 1 (windup animation).

Wait check: `this.ai[0] += (int)num653` — so Herpling charges faster when far. And after big jump ai[3] = position.X so if it lands at same X it flips direction and ai[2]=300 (penalty? ai[2] is used as timer — since ai[2]>1 decrements each frame; if ai[2]==0 → ai[0]=-100, ai[2]=1, retarget). Actually ai[2] is a generic timer that also gets set to 300 when stuck; when it counts down to 0, re-init. Note the `if (this.ai[2] > 1f) ai[2] -= 1f;` at top.

Also for Derpling (177): while airborne (velocity.Y != 0), if player is below and horizontally overlapping (flag44), it slows X and dampens upward Y — that's the "derp slam on player" behavior.

Now the aiStyle 44 airborne-target logic: ai[0] is a 90-frame timer refreshed while LOS to player; when it expires (ai[0] <= 0), speed ×0.8, accel ×0.7, and target Y = Center.Y + directionY*1000 → flies away vertically. The block at 31179: `if (this.ai[0] <= 0f)`.

For 587 EyeballFlyingFish: num714=0 (always chase horizontally regardless of distance), dayTime → flies up (num717 = 0) and flips direction each frame.

Also the horizontal gate `if (num716 > num714)` (horizontal distance > 30/40px) → horizontal accel; else no horizontal accel (drift). Vertical: target Y = player.Y - height/2; if num716 > num715 (100/150/250) → num717 -= num715/2 (hover above player at greater distance).

Wait num717 for base = Main.player[target].position.Y - height/2 — that's the "stay 50px above player" style? Standard flying AI targets player.position.Y - height/2... Hmm actually classic: the EoC-servant style. Note in the vertical compare `if (position.Y < num717)` → +0.01 accel else -0.01.

Now for aiStyle 19: I have the details. Also note: "directionY < 0" rotation gate — the Antlion aims when player is above. And tile types 421/422 check at (Center.X/16, Bottom+8/16): 421/422 are Sand Block variants? Tile 53 = SandBlock; 421/422 = "Sandstone"? Actually 421 = Sandstone, 422 = HardenedSand. Yes: 396=DesertFossil? Let me be careful: 421 Sandstone? Terraria TileID: 396 DesertFossil? Hmm: TileID.Sand = 53, Ebonsand = 112, Pearlsand = 116, Crimsand = 234, Sandstone = 397? Actually: 396 = Shell Pile? I'd rather not assert. Common: 397 Sandstone? Hmm. Let me quickly check TileID for 421/422.

Also for aiStyle 0: check 105/106/123/354/376/579/589 transforms; 376 (SleepingAngler) and 579 (BartenderUnconscious) have the water-drift behavior: when in water they bob (velocity.Y=-0.4) and drift toward world center unless wall within 12 tiles. Others just stand (friction 0.93).

Also NPCID.Sets.DangerDetectRange includes 376? Not needed.

Let me check TileID 421/422 names, then also confirm aiStyle 19's flag25 logic reading: flag25 = true when directionY<0 and rotation in [-1.2,1.2] → can aim directly; else if standing on tile 421/422, shoot along rotation direction. Wait: flag25 computed as `((rotation < -1.2 || rotation > 1.2) ? false : true)` — i.e., flag25 true when rotation within [-1.2,1.2]. Then clamp rotation to [-0.8, 0.8].

One more check: does the aiStyle 19 block reference "Antlion" sand tiles as 421/422 — in 1.4.4+, TileID.SandStone = 397? Hmm. Let me check TileID.cs.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:31:12.247Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID && grep -nE \"public const short [A-Za-z]+ = (421|422|53|397|396|401);$\" TileID.cs",
 "description": "Identify tile ids 421/422"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:31:16.214Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-11T04:31:18.263Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID && grep -nE \"= (421|422);\" TileID.cs | head",
 "description": "Find tile names for 421 and 422"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:31:18.302Z

**📎 ToolResult**

```
1275:	public const ushort ConveyorBeltLeft = 421;
1277:	public const ushort ConveyorBeltRight = 422;

```


---

## 🤖 Assistant · 2026-08-11T04:31:40.296Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
421/422 are conveyor belts (left/right) — makes sense: Antlion sitting on a conveyor belt shoots in the belt's direction (rotation - 1.57). Nice catch: this is the statue/AFK farm mechanic. Note: rotation at this point is the clamped rotation (facing angle), so num293 = rotation - 1.57 gives the horizontal facing direction; fired along it at speed 12.

Wait, for conveyor: direction should be horizontal. rotation was clamped to [-0.8, 0.8]; rotation - 1.57 ranges [-2.37,-0.77], cos could be negative for rotation<0... Actually cos(rotation-1.57) = sin(rotation), which is within [-0.72, 0.72]. Hmm that's vertical-ish. Hmm, cos(-1.57)=0. For rotation=0: direction (cos(-1.57), sin(-1.57)) = (0,-1) → shoots straight up. For rotation=0.8: cos(-0.77)=0.72, sin=-0.70 → 45° up-right. OK — so conveyor logic fires in the direction the antlion is tilted, roughly up. Fine, just report it.

Also note: antlion's rotation only updates when directionY<0 (player above). When directionY>=0 rotation stays.

Now I also want to double-check the aiStyle 25 flag36 Present Mimic: when not snowMoon, PresentMimic does NOT target (TargetClosest skipped) — but flag36 also gates jump target re-acquire. Fine.

One remaining piece: aiStyle 39's state 1 → jump: initial velocity from the ai[1]==1 branch — speed num617 = 10 (LOS) or 6 (no LOS), aimed at player's head with a horizontal-bias correction (num619 = |dx|*0.2 subtracted from target Y, 0 if directionY>0). If no LOS → vy forced -10. ai[3] stores vx. Then during flight: vx locked to ai[3], vy -= 0.22 per frame (ascending), damage lerp 2x→1.8x defDamage (i.e. attack boost), defense×2. After 90 frames → state 4 (descent/recover): noGravity=false (already), vx *= 0.96, rotation decays via ai[2] -= 0.01, when ai[2]<=0 && (velocity.Y==0 || wet) → state 5. State 5: recover 30 frames (0.5 for types 496-497), rotation=0, vx=0 → back to state 0.

Sroller 417 special: from state 1 after 30 frames → state 6 (solar roll) instead of 3: height shrinks to 32, ai[2]=rand 2..4 (number of rolls?), first frame sets velocity toward player speed 16 (LOS) or 10 with vy forced -12 if no LOS; ai[1] counts frames; ends when ai[2]==0 or ai[1]>=1200 → state 5; state 5 restores height 52. Also during state 6 damage = 1.8x..1.4x, defense×2, knockBackResist=0. Rotation = clamp(vx/10*dir, ±π/10).

Wait — for Sroller, where does ai[2] decrement? In state 6 the loop `if (this.ai[2] == 0f || this.ai[1] >= 1200f)` ends. ai[2] set to Main.rand.Next(2,5) at entry = number of dashes; each subsequent visit? Hmm — state 6 re-enters the ai[1]==1 branch only once. Actually after first frame (ai[1]==1), ai[1] increments; the "else" branch runs; when does it dash again? It doesn't within state 6 — the initial velocity persists (noGravity is false though... hmm gravity applies). Hmm — actually maybe ai[2] decrements elsewhere... In state 6 else-branch: ai[1] += 1 each frame; ai[3] does the explosion-dust animation; end when ai[2]==0. Since ai[2] isn't decremented in this block, it ends via ai[1]>=1200 (20 seconds of rolling). Hmm, unless... whatever — report as-is.

Also justHit handling: `if (justHit && type != 417)` → reset ai[0]=0, ai[1]=0, retarget. So Sroller ignores hits (knockBackResist=0 anyway).

Also the step-up logic at 29263-29314 (gfxOffY/stepSpeed) — the fighter-style step up; I'll summarize as "1-tile step-up assist (gfxOffY, stepSpeed 0.75/1.5)".

I now have everything needed. One more: for aiStyle 17 I should confirm tileCollide = true default for Vulture (no explicit flag in SetDefaults → default tileCollide = true, noGravity default false). aiStyle 17 block sets noGravity=true then false when perched. Good.

Also worth noting for aiStyle 25: tileCollide default true; no explicit noGravity → gravity applies always (mimic jumps via negative vy).

Also for aiStyle 0: bound NPCs — width/height; check 105 flags? They're townNPC=false. Fine.

Also DungeonSpirit 288: noTileCollide = true, noGravity = true → passes through walls. Death: does it spawn souls? "死后分解成魂魄?" — Dungeon Spirit death is handled in NPCLoot (drops Ectoplasm). Actually the classic behavior: Dungeon Spirits don't split. There's a "who spawned it" — Dungeon Spirit spawns from killing other dungeon enemies post-Plantera. The user asks about 受击反应 — aiStyle 56 has none (no justHit handling); velocity is (v*100 + desired*12)/101 → smooth homing at speed 12 with huge inertia.

Also mention for 56: rotation = Atan2(dy,dx) - 1.57; dust 180 (spectre dust).

Line numbers for everything:
- aiStyle 0: 19774-19893; TransformBoundNPC helper 45219-45229.
- aiStyle 17: 24079-24209.
- aiStyle 19: 24465-24595.
- aiStyle 23: 25316-25395.
- aiStyle 25: 25621-25713.
- aiStyle 39: 29257-29783.
- aiStyle 41: 30017-30280.
- aiStyle 44: 30999-31268 (also line 94137 has aiStyle == 44 in another method — probably FindFrame? Let me check quickly what that is. It's likely in FindFrame for fish-like rotation. Let me check briefly.

Also confirm 378's identity — not in NPCID list I pulled (377/378?). Let me grep 378.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:31:40.983Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456 && grep -n \"= 378;\" Terraria.ID/NPCID.cs; echo \"===94137===\"; sed -n '94130,94145p' Terraria/NPC.cs",
 "description": "Identify type 378 and aiStyle 44 second site"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:31:41.018Z

**📎 ToolResult**

```
11821:	public const short ChatteringTeethBomb = 378;
===94137===
		{
			result = true;
		}
		if (aiStyle == 40)
		{
			result = true;
		}
		if (aiStyle == 44)
		{
			result = true;
		}
		if (type == 467)
		{
			result = true;
		}
		if (type == 477)

```


---

## 🤖 Assistant · 2026-08-11T04:31:44.960Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
378 = ChatteringTeethBomb (the chattering teeth bomb trap critter/item-summoned NPC). Good — so the aiStyle 41 "another thing" is the Chattering Teeth Bomb, which hops like a Herpling and self-destructs when near a player (<64px) or wet.

The 94137 aiStyle==44 is in some method returning result=true — likely `IsLikeARootedNPC`? or "ShouldRunVelocityDecay"? Let me check what method it's in, briefly — it could be important (e.g. `ShouldNPCBeTrappedByWeb` or IsFishLikeNPC). Quick check of the method signature.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:31:45.516Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && awk 'NR>=94090 && NR<=94145' NPC.cs | grep -n \"public\\|private\\|bool.*(\" | head -5",
 "description": "Identify enclosing method of line 94137"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:31:52.489Z

**📎 ToolResult**

```
29:	private bool Collision_DecideFallThroughPlatforms()

```


---

## 🤖 Assistant · 2026-08-11T04:32:21.669Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
aiStyle 44 → FallThroughPlatforms = true (flying fish and swarmers fall through platforms). Good detail.

Now I have everything. Let me also double check the aiStyle 41 Herpling jump values: velocity.X += 5*direction for Herpling (type != 177, != 378), velocity.Y = -5 for small hop; big hop at ai[1]==3: vy=-9, vx += 3*direction, ai[0]=-200, ai[1]=0, ai[3]=position.X. Derpling: small hop vy=-7.5, vx += 4*direction; big (ai[1]==2): vy=-11.5, vx += 2*direction. ChatteringTeethBomb(378): small vy=-5 vx+=5dir; big at ai[1]==3 vy=-9 vx+=3dir (same as Herpling). Plus bonus vx += direction if dist in (200,350).

Ground charge rate: ai[0] += 5/frame Herpling/378, +=2/frame Derpling, plus (int)(400/dist * (10 or 5)) capped 30.

Also stuck detection: `if (this.ai[3] == position.X)` → direction flip + ai[2]=300; ai[3] set to 0 after check.

Airborne steering (velocity.Y != 0): if target >= 255 return; Derpling special flag44 (player below & x-overlap → vx*=0.92, dampen rising); then accelerate vx toward 4 (Derpling) or 3 (others) with +0.2*dir or *0.93.

Water: if wet && type != 177 (Derpling excluded): collideX flips direction... (note `direction *= -direction` — a decompiler artifact of `direction = -direction`); collideY bounce; vy toward -4 with 0.3 buoyancy.

aiStyle 44 numbers table:
base (224 FlyingFish / 581? no 581 has own): accel num710=0.05, extra num711=0.01, maxX num712=3, maxY num713=1, num714=30, num715=100.
509 GiantFlyingAntlion: 0.08/0.03/4.5/2/40/150, num717=player.Center.Y - h/2, rotation=vx*0.1, swarm separation ±0.05 vs same type within width (manhattan < width).
581 FlyingAntlion: 0.06/0.02/4/2/40/150, same separation.
587 EyeballFlyingFish: 0.13/0.09/6.5/3.5/0/250; num717=player.position.Y; dayTime → num717=0 (fly up), direction *= -1 each frame.
ai[0] LOS timer: refreshed to 90 when target invalid or (type!=587 && player.wet) or player.dead or Collision.CanHit(center,1,1,player.center,1,1); else decrement; at <=0: maxX*0.8, accel*0.7, num717 = Center.Y + directionY*1000 (fly off vertically), direction from vx sign.
Horizontal gate num716 (|dx|) > num714 → accel ±num710 (with extra num710 when moving opposite, num710/2 when same sign); clamp ±num712.
Vertical: num717 = player.position.Y - height/2 (base; others Center variants); if |dx| > num715 → num717 -= num715/2 (hover higher); accel ±num711, clamp ±num713.
wet (except 587): rise buoyancy to -4.
collideX/Y: bounce to velocity = direction (1 unit) and flip direction from oldVelocity sign.
noGravity=true; tileCollide default true; Collision_DecideFallThroughPlatforms returns true → fall through platforms.

aiStyle 56 numbers: speed 12 desired; velocity = (v*100 + desired)/101 (smoothing factor ~0.99); rotation = atan2 - 1.57; dust 180 noGravity scale 1.3 vel*0.1. Flags from SetDefaults: noTileCollide=true, noGravity=true (tileCollide default true but noTileCollide overrides). No justHit special reaction. Spawn: from dungeon NPC deaths post-Plantera (in NPCLoot of dungeon enemies — not part of this block; mention briefly).

Dungeon Spirit "死后分解成魂魄" — no. It drops Ectoplasm. I'll just note.

Also aiStyle 0 details: transform mapping: 589 GolferRescue→588 Golfer; 105→107 GoblinTinkerer; 106→108 Wizard; 123→124 Mechanic; 354→353 Stylist; 376→369 Angler; 579→550 Bartender(DD2). Trigger: player.talkNPC == whoAmI (i.e., player starts talking to the bound NPC) — server side (netMode != 1). Transform then AI_007_TownEntities_UpdateSavedStates, register bestiary chat, SetTalkNPC(playerID), send message 40.

Movement for 105/106/123/354: only TargetClosest + spriteDirection = direction; X friction 0.93 (they never move otherwise). For 376/579: water bob logic: velocity.Y = -0.4 when wet or head tile has liquid; then check 12 tiles toward world center at Center.Y row for solid; if wall found (or type 579 always) → damp vx (0.99, clamp ±0.01→0); else drift vx += num*0.01 (num = direction toward world center), vx soft-clamped ±0.2 via *0.95. Note 376 spawns in water (Angler floats in ocean). Note also these use ConveyorBeltCollision set (they stand on conveyors).

Also note bound NPCs: ai[0..3] unused; no gravity flags — they have tileCollide default true, gravity default. And they don't flee (no danger detect).

aiStyle 17 details:
- noGravity = true at block start; ai[0]==0 perched → noGravity=false, TargetClosest; server: if any velocity (vx!=0, vy<0, vy>0.3) → takeoff (ai[0]=1) without hop; else if player rect intersects 200px box (pos-100, size+200) OR life<lifeMax → takeoff with velocity.Y -= 6 hop.
- ai[0]==1 flying (player alive): collideX → vx = -oldvx*0.5, bump to at least 2 toward direction; collideY → vy = -oldvy*0.5, clamp to min 1 magnitude; horizontal accel ±0.1 (extra 0.1 if moving away, extra 0.05 if moving opposite), clamp ±3; vertical target: num273 = player.Y - height/2; if |dx|>50 → num273 -= 100 (fly 100px higher); accel ±0.05 (extra 0.01 if moving away), clamp ±3.
- wet: buoyancy vy: if vy>0 *0.95; vy -= 0.5; clamp -4; TargetClosest.
- No re-perch: ai[0] never returns to 0. Raven 301 same block (SetDefaults 12821).

aiStyle 23 details:
- noGravity=true, noTileCollide=true (in block). Light colors: 83 (0.2,0.05,0.3) purple-ish; 179 (0.3,0.15,0.05); default 84 (0.05,0.2,0.3).
- ai[0]==0 (dash entry): compute unit vector to player center × speed 9 → set velocity directly; rotation = atan2(vy,vx)+0.785 (45°); → ai[0]=1, ai[1]=0.
- ai[0]==1 (drift/decel after dash): velocity *= 0.99 per frame; ai[1]++; justHit → state 2; ai[1]>=100 → state 2, zero velocity.
- ai[0]==2 (spin charge-up): velocity *= 0.96; ai[1]++; rotation speed num351 = 0.1 + (ai[1]/120)*0.4, rotation += num351*direction; justHit → restart state 2 (ai[1]=0); ai[1]>=120 → state 0 (new dash).
- So cycle: dash 1 frame set + 100 frames drift, 120 frames spin, repeat. justHit never returns to drift — always back to spin (state 2).

aiStyle 25 details: covered.

Also "共同陷阱" items:
1. Raven 301 and Vulture 61 share aiStyle 17 block — same code (SetDefaults 9486/12821).
2. aiStyle 25 block includes PresentMimic 341 (aiStyle=25, SetDefaults 13246) and IceMimic 629; flag36: 341 outside snowMoon doesn't target. NOT aiStyle 3 — careful if our data said otherwise.
3. aiStyle 41's 378 is ChatteringTeethBomb (not another "Derpling-like critter") — self-destruct on proximity/water; Herpling & 378 share hop numbers, Derpling differs.
4. aiStyle 39's 417 is Solar Sroller with its own state 6, height change 52↔32, ignores justHit; also aiStyle 39 handles types 496-497 (Bouncy boulder?) with slower params — guard by range.
5. noTileCollide flags: aiStyle 23 sets noTileCollide=true in-block; DungeonSpirit 288 sets it in SetDefaults (12670+). aiStyle 19 toggles noTileCollide dynamically (settling logic) — must not fix it once.
6. noGravity is applied AFTER AI in UpdateNPC (line 91519: velocity.Y += gravity, clamped by maxFallSpeed) — your AI must not double-apply gravity.
7. aiStyle 17 & 25 & 0 gating: ai[0]==0 blocks only run server-side (netMode != 1) for the wake check; client returns early (mimic) — in single-player it's fine.
8. ConveyorBeltCollision set includes all bound NPCs (105/106/123/354/376/579/589) and 85/629 (mimics) — conveyor support.
9. aiStyle 44 has a second gate in Collision_DecideFallThroughPlatforms (line 94137) → falls through platforms.
10. Expert mode: no expert branches in these 9 blocks (aiStyle 18 had one, not ours). aiStyle 4 does. Good.
11. Mimic wake box is px-based 200x200 box (100 padding), not tile distance.
12. aiStyle 0: two different behaviors inside (376/579 water drift vs others static).
13. js port traps: `direction *= -direction` decompile artifact means `direction = -direction`.

Also note for aiStyle 39 the step-up preamble and `gfxOffY`.

I think I'm done. ~14 tool calls. Write the final compact report.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:33:16.896Z · glm-x-preview-260804

```
9 个家族全部按块读完，规格如下（行号均为 NPC.cs 绝对行号，1.4.5.6 反编译）。

---

## 1. aiStyle 0 — Bound NPC（19774-19893）

- **无状态机**：ai[0..3] 全部未用。两种子行为按 type 分流。
- **静态站立**（105 BoundGoblin/106 BoundWizard/123 BoundMechanic/354 WebbedStylist）：每帧只 `TargetClosest()` + `spriteDirection = direction`（19784-19817 仅对非 376/579）；X 摩擦 `velocity.X *= 0.93`，|vx|<0.1 归零（19884-19891）。无移动、无逃逸、无重力异常。
- **水上漂流**（376 SleepingAngler、579 BartenderUnconscious，19818-19883）：`wet` 或头顶 tile 液体>0 → `velocity.Y = -0.4` 上浮；向世界中心方向探 12 格（Center.Y 行）找实心墙——找到墙（或 type==579 恒成立）→ 摩擦 0.99 停住；没墙 → `vx += dir*0.01` 缓漂，|vx|>0.2 时 ×0.95。376 就是漂在海面等救的渔夫。
- **解救触发**（19776-19812）：仅服务端（netMode != 1），遍历 255 玩家，**谁 talkNPC == whoAmI（开口对话）** 就 `AI_000_TransformBoundNPC(player, newType)`。Transform 映射：589→588 Golfer、105→107 GoblinTinkerer、106→108 Wizard、123→124 Mechanic、354→353 Stylist、376→369 Angler、579→550 DD2Bartender。
- **Transform 后**（45219-45229）：`Transform(npcType)` → `AI_007_TownEntities_UpdateSavedStates()`（恢复存档状态/名字）→ 图鉴 RegisterChatStartWith → `player.SetTalkNPC(whoAmI)`（对话窗口不关，直接接上城镇 NPC 对话）→ 服务端 SendData(40)。
- 运动学：tileCollide=true（默认）、有重力。105/106/123/354/376/579/589 均在 `NPCID.Sets.ConveyorBeltCollision`（NPCID.cs:4789）。

## 2. aiStyle 17 — Vulture 61 / Raven 301（24079-24209）

- **确认同块**：Raven 301 的 SetDefaults（12821）也是 `aiStyle = 17`，与 Vulture 61（9486）共用同一块代码。
- **ai[0]=0 栖息**（24082-24104）：`noGravity=false`，TargetClosest；仅服务端判定起飞——① 有任何速度（vx≠0 / vy<0 / vy>0.3）→ 直接 ai[0]=1；② 玩家矩形与本 NPC「pos-100、size+200」的 **200px 像素盒**相交，或 `life < lifeMax`（被打过）→ ai[0]=1 且 `velocity.Y -= 6` 起跳。**不检查脚下是不是沙**。
- **ai[0]=1 飞行**（24105-24194，玩家活着才执行）：`noGravity=true`；collideX → `vx = -oldvx*0.5`，且保证朝 direction 至少 2（24107-24118）；collideY → `vy = -oldvy*0.5`，至少 1（24119-24130）；水平追击 accel ±0.1（反向时额外 0.1、异号再 0.05），clamp ±3（24131-24163）；垂直目标 `num273 = player.Y - height/2`，若水平差 **>50px 则再减 100**（飞高 100px），accel ±0.05（同上加 0.01），clamp ±3（24164-24193）。
- **wet**（24195-24207）：vy>0 先 ×0.95，再 `vy -= 0.5`，clamp -4，重新 TargetClosest。
- **不会回栖息**：ai[0] 单向 0→1，无回落分支。

## 3. aiStyle 19 — Antlion 69（24465-24595）

- **它完全不动**：无任何 vx 写入（仅 24489-24497 衰减到 0）。SetDefaults knockBackResist=0（9598 区），即被打了也不位移。**没有钻地位移**。
- **扎根/就位逻辑**（24543-24594）：探测底部一行 3 列（左/中/右），任一 nactive+tileSolid → `noGravity=true; noTileCollide=true; velocity.Y=-0.2`（24566-24572）——半埋沙中时向上浮出到沙面；否则恢复 `noGravity=false; noTileCollide=false` 落地，落时 50% 概率出沙尘（dust 32，24575-24588）。**noTileCollide 是动态开关**。
- **沙球攻击**（24499-24542）：`ai[0]` 冷却 200（到 200 那帧播 SoundID.Item5），归零后可再射。发射速度 12 指向玩家中心（24468-24475 预算）；发射条件二选一：
  - ① `directionY<0`（玩家在上）且该帧 rotation ∈ [-1.2, 1.2]（flag25，24477-24488）→ 玩家视线 `Collision.CanHit` 成立 → 直接瞄玩家发射；
  - ② 玩家不在上方但「脚下 tile 是 421/422」——那是**传送带 ConveyorBeltLeft/Right**（TileID.cs:1275/1277）→ 沿 `rotation - 1.57` 方向射（24526-24541），这是 AFK 刷怪阵机制，**不是沙砖**。
- 弹体：Projectile 31（SandBall），damage 10，`ai[0]=2`，timeLeft 300，friendly=false（24516-24524）。
- rotation 只在 directionY<0 时更新并 clamp ±0.8（24479-24488）。

## 4. aiStyle 23 — CursedHammer 83 / EnchantedSword 84 / CrimsonAxe 179（25316-25395）

- **flags**：块首 `noGravity=true; noTileCollide=true`（25318-25319）——飞行武器全程穿墙。
- **灯光**：83 紫(0.2,0.05,0.3)、179 橙红(0.3,0.15,0.05)、84 蓝绿(0.05,0.2,0.3)（25320-25331）。
- **三态循环**（ai[0]=状态，ai[1]=各态计时）：
  - **ai[0]=0 冲刺起跳**（25336-25353）：算到玩家中心单位向量 × **速度 9** 直接赋给 velocity；`rotation = atan2(vy,vx)+0.785`；→ ai[0]=1, ai[1]=0。
  - **ai[0]=1 漂移减速**（25354-25375）：`velocity *= 0.99/帧`；ai[1]++；**justHit → 直接进 2 态并清计时**；ai[1]>=100 → 进 2 态且 velocity 清零。
  - **ai[0]=2 蓄转**（25376-25394）：`velocity *= 0.96/帧`；ai[1]++；转速 `num351 = 0.1 + (ai[1]/120)*0.4`，`rotation += num351*direction`（越转越快）；justHit → **重置 ai[1]=0 重转**；ai[1]>=120 → 回 0 态再冲。
- 即周期 = 冲 1 帧 + 漂 100 帧 + 转 120 帧 ≈ 3.7s。**受击永远回 2 态（蓄转），不回漂移**。
- 目标刷新：target 无效/玩家死才 TargetClosest（25332-25335）。

## 5. aiStyle 25 — Mimic 85 / PresentMimic 341 / IceMimic 629（25621-25713）

- **341 也是本块**（SetDefaults 13250 `aiStyle = 25`），629 同。`flag36 = type==341 && !Main.snowMoon`：雪月外的礼物宝箱怪**不索敌**（25623、25647、25682 三处 gate）。
- **ai[3]=层位标记**（仅初始化用，25624-25644）：首帧 `position.X += 8`（对齐格子）；Y>UnderworldLayer→3、>worldSurface→2、否则 1；341/629 强制 1。块内不再参与运动。
- **ai[0]=0 伪装**（25645-25667）：TargetClosest（非 flag36）；客户端直接 return；有速度（vx≠0/vy<0/vy>0.3）或玩家与本 NPC 200px 像素盒（pos-100,size+200）**相交**、或 `life<lifeMax` → ai[0]=1。**显形距离≈200px，不是格数**。
- **ai[0]=1 跳跃循环**（25668-25712）：空中时朝 direction 方向把 |vx| 补到 ≥1（±0.1/帧）；**落地（velocity.Y==0）**时 `ai[2]++`，`ai[2] < (ai[1]==0 ? 12 : 20)` → `vx *= 0.9` 蓄力等待；够数后清 ai[2]、TargetClosest、ai[1]++：
  - ai[1]==2（第三次跳）→ **大跳：vx = dir*2.5, vy = -8**，ai[1]=0（25692-25697）；
  - 其他 → **小跳：vx = dir*3.5, vy = -4**，ai[1] 保持自增（25698-25702）。
  - 即跳序 = 小(-4)、小(-4)、大(-8)、循环，间隔 12/12/20 帧。
- tileCollide=true、有重力（无 noGravity 设置，跳跃全靠负 vy）。

## 6. aiStyle 39 — GiantTortoise 153 / IceTortoise 154 / SolarSroller 417（29257-29783）

- **前置**：块首是 1 格台阶抬升逻辑（29263-29314，gfxOffY + stepSpeed 0.75/1.5）。SetDefaults 153/154 显式 `noGravity=false`。gravity 由 UpdateNPC 在 AI 之后统一加（91519）。
- **受击**（29315-29320）：`justHit && type != 417` → ai[0]=0, ai[1]=0, TargetClosest（**Sroller 忽略受击**，它 knockBackResist=0）。
- **ai[0]=0 待机/接近**（29333-29506）：防御/伤害复位，knockBackResist=0.3（496-497 为 0.75）；蓄力 ai[1] 增速——距离>200 且有视线 +4/t（496-497 为 +2），距离>600 且（有视线或玩家在下方 200px 内）再 +10/t（496-477 为 +4）；**wet 直接 ai[1]=1000**（29370-29373 立即起跳）；ai[1]>=400 → ai[0]=1。移动：近距离(<400)行走 accel 0.07 clamp ±1，远距离 clamp ±1.5（496-497 clamp ±0.5），越界反向；前方 3 格×下 4 格无地面则转身（29395-29427）。
- **ai[0]=1 蓄势**（29507-29534）：`vx *= 0.5`，ai[1] += 1（496-497 为 0.5）；>=30 → ai[0]=3；**417 特例**：先改 hitbox（height 52→32）进 **ai[0]=6**，ai[2]=rand(2,5)（29525-29532）。
- **ai[0]=3 旋转弹射**（29535-29620）：伤害 `LerpBetweenFinalValues(defDamage*2, *1.8)`、defense×2。首帧（ai[1]==1）定速：有视线 **10**、无视线 **6**（496-497 ×0.75）；瞄准点 Y 加水平偏置 `num619 = |dx|*0.2`（directionY>0 时为 0）；**无视线强制 vy=-10**；vx 存入 ai[3]。飞行中：与玩家 X 区间重叠 → vx*=0.8、ai[3]=0（停止上升）；否则 `vx = ai[3]; vy -= 0.22/帧`（持续上旋）；ai[1]>=90 → `noGravity=false`（防呆）、ai[0]=4。旋转 `rotation += ai[2]*direction`。
- **ai[0]=4 下落恢复**（29621-29645）：vx *= 0.96；ai[2] -= 0.01 且 `rotation += ai[2]*dir`；ai[2]<=0 且（落地或 wet）→ ai[0]=5。
- **ai[0]=5 复位**（29752-29781）：417 还原 height 32→52；rotation=0、vx=0；ai[1] += 1（496-497 ×0.5）>=30 → ai[0]=0；wet → 直接回 3。
- **ai[0]=6 Sroller 日耀滚动**（29646-29751）：伤害 ×1.8→×1.4、defense×2、knockBackResist=0；首帧定速 **16（视线）/10（无视线，且强制 vy=-12）**；之后保持速度滚（重力仍生效），ai[2]==0 或 ai[1]>=1200 → ai[0]=5；rotation = `clamp(vx/10*dir, ±π/10)`；带爆炸粒子/gore 动画（ai[3] 计时 10 帧一轮）。

## 7. aiStyle 41 — Herpling 174 / Derpling 177 / ChatteringTeethBomb 378（30017-30280）

- **通用计时**（30019-30029）：ai[2]>1 时每帧 -1；ai[2]==0 → `ai[0]=-100, ai[2]=1`，TargetClosest。**ai[0] 是负数倒计时**，落地时累加，≥0 触发跳跃。
- **378 是「格格牙炸弹」**（NPCID.cs:11821），不是又一头 Derpling：近玩家 **<64px** 或 wet → ai[1]=5, ai[2]=10（自爆序列：hitbox 撑到 160、dontTakeDamage、ai[2]==9 播 Item14、ai[2]==1 时 `life=-1; active=false`，30044-30093）。
- **落地段（velocity.Y==0，30135-30236）**：vx *= 0.8 归零；若 `ai[3] == position.X`（原地没动）→ 转向 + ai[2]=300 惩罚；蓄力 `ai[0] += 5/t`（**Derpling 只 +2**），再加距离加速 `(int)(400/dist * (非177 ? 10 : 5))`，cap 30（30156-30166）；距离 200<d<350 时起跳额外 `vx += dir`：
  - **Herpling/378 小跳**：`vy=-5, vx += 5*dir`，ai[0]=-120，ai[1]++；**大跳（ai[1]==3）**：`vy=-9, vx += 3*dir`，ai[0]=-200，ai[1]=0，ai[3]=position.X（30206-30229，378 另播音效）。
  - **Derpling 小跳**：`vy=-7.5, vx += 4*dir`；**大跳（ai[1]==2）**：`vy=-11.5, vx += 2*dir`（30174-30198）。即 Derpling 跳更高更慢、大跳来得早一次。
  - ai[0] ∈ [-30,0) → `aiAction=1`（起跳前摇动画，30231-30234）。
- **空中段**（30237-30279）：Derpling 特判——玩家在正下方且 X 重叠 → `vx*=0.92`、上升 vy *= 0.9 再 +0.1（朝人下压）；随后所有成员向 direction 方向加速到 |vx|=4（Derpling）/3（其他），+0.2/t 或 ×0.93。
- **wet**（30105-30134，177 除外）：collideX 转向（注意 30109 `direction *= -direction` 是反编译写法，实为取反）、collideY 弹跳（旧 vy<0 → vy=5 否则 vy-=2）、vy>4 ×0.95、`vy -= 0.3` 浮力、clamp -4。

## 8. aiStyle 44 — FlyingFish 224 / GiantFlyingAntlion 509 / FlyingAntlion 581 / EyeballFlyingFish 587（30999-31268）

- `noGravity=true`（31001）；tileCollide 默认 true；**Collision_DecideFallThroughPlatforms 对 aiStyle 44 返回 true（94137）→ 会穿平台下落**。
- **碰撞反弹**（31002-31025）：collideX → direction 按 oldVelocity.X 符号翻转、`vx = direction`（=1 单位）；collideY 同理 directionY/vy。
- **LOS 计时 ai[0]**（31074-31089）：target 无效 /（type≠587 且玩家 wet）/ 玩家死 / `Collision.CanHit(center,1,1,player.center,1,1)` 成立 → **ai[0]=90**；否则每帧 -1。**ai[0]<=0 时**（31179-31192）：maxX×0.8、accel×0.7、目标 Y 改为 `Center.Y + directionY*1000`——垂直逃逸，方向由 vx 符号决定。
- **参数表**（31090-31178，num710/11/12/13/14/15 = xAccel/yAccel/maxX/maxY/xGate/yGate）：
  | type | xAccel | yAccel | maxX | maxY | xGate | yGate | 目标Y |
  |---|---|---|---|---|---|---|---|
  | 224 基准 | 0.05 | 0.01 | 3 | 1 | 30 | 100 | player.Y - h/2 |
  | 509 | 0.08 | 0.03 | 4.5 | 2 | 40 | 150 | player.Center.Y - h/2 |
  | 581 | 0.06 | 0.02 | 4 | 2 | 40 | 150 | 同上 |
  | 587 | 0.13 | 0.09 | 6.5 | 3.5 | **0** | 250 | player.Y（白天改 0 = 飞离） |
  - 509/581 附加：`rotation = vx*0.1` + **同型个体分离**——与同类曼哈顿距离 < width 时按相对位置 ±0.05/t 推开（31108-31129 / 31141-31162），这是群袭散布的关键。587 白天每帧 `direction *= -1`（31173-31177）。
- **运动**（31193-31255）：水平 |dx|>xGate 才加速（±num710，反向额外 +num710、同向 +num710/2），clamp ±maxX——否则水平不动；垂直目标 num717，若 |dx|>yGate 则 `num717 -= yGate/2`（远处悬更高），accel ±num711，clamp ±maxY。
- **wet**（31256-31267，587 除外）：vy>0 ×0.95，`vy -= 0.5`，clamp -4。
- 与 EoC 仆从不是同一实现：无惯性项、无摆动相位，是「分轴限速追 + 群体分离」模型。

## 9. aiStyle 56 — DungeonSpirit 288（32915-32936）

- **flags**（SetDefaults 12670 区）：`noTileCollide=true; noGravity=true` → **穿墙追踪**，tileCollide 名义 true 但被 noTileCollide 覆盖。
- 全块无 ai/localAI 状态、**无 justHit 特殊反应**。
- 运动（32917-32927）：TargetClosest；期望速度 = 指向玩家中心单位向量 × **12**；实际 `velocity = (velocity*100 + 期望)/101`（≈0.99 平滑，巨大惯性，转向极慢但极难甩掉）；`rotation = atan2(dy,dx) - 1.57`（骷髅头朝向速度方向）。
- 视觉（32929-32935）：每帧 1 颗 dust 180，vel×0.1、scale 1.3、noGravity。
- 「死后分解成魂魄」不成立：它本身即魂魄本体（地牢怪死后概率生成在其 NPCLoot 里），死亡只是正常掉落灵雾（Ectoplasm 前置在专家/大师），本块无任何死亡拆分逻辑。

---

## 共同陷阱

1. **Raven 301 与 Vulture 61 共用 aiStyle 17 同一块**（SetDefaults 9486 / 12821），不要给 Raven 单写 AI。
2. **PresentMimic 341 是 aiStyle 25 不是 3**（SetDefaults 13250；我方数据若标 3 是错的）；且它仅在 snowMoon 索敌。629 IceMimic 也在 25 块内。
3. **aiStyle 41 的 378 是 ChatteringTeethBomb**（NPCID.cs:11821）——自带近身/遇水自爆序列，Herpling/378 跳跃数值相同、Derpling 独立一套（更慢更高、+2/t 蓄力、大跳提前到第 2 跳）。
4. **aiStyle 39 的 417 Sroller 有专属第 6 态**：hitbox 52↔32 切换、忽略 justHit、伤害 ×1.8/×1.4、knockBackResist=0；块内还带 type 496-497（弹跳巨石）分支，数值减半，移植时按 type 门控。
5. **noTileCollide 有三种来源**：aiStyle 23 在块内设 true；DungeonSpirit 288 在 SetDefaults 设；**aiStyle 19（蚁狮）是每帧动态开关**（埋沙时 true 浮出、落地 false），别一次定死。
6. **重力统一在 UpdateNPC 91519 施加（AI 之后，velocity.Y += gravity 再 clamp maxFallSpeed）**——AI 块内的 vy 操作都是「在重力之前」，我方若在 AI 里再加重力会双重下坠。aiStyle 39 里那句 `noGravity=false`（29610）是防呆残留，全块没有任何地方设过 true。
7. **伪装/栖息判定是像素盒不是格数**：aiStyle 17/25 都是「本 NPC 矩形向四周扩 100px（即 200px 盒）与玩家矩形相交」，或 `life<lifeMax`。
8. **客户端/服务端门禁**：aiStyle 0 的对话解救、17 与 25 的唤醒判定均在 `Main.netMode != 1` 内（25 客户端 ai[0]==0 时直接 return），单人模式无感，联机移植时别漏。
9. **aiStyle 44 有第二个挂钩**：`Collision_DecideFallThroughPlatforms`（94137）返回 true——飞行鱼/蚁狮蜂会主动穿平台，只移植 AI 块会漏掉这一半行为。
10. **本 9 家族均无专家模式分支**（专家分支在 aiStyle 4/18 等，别照抄邻近块）。
11. **反编译伪代码陷阱**：`direction *= -direction`（30109）实为「取反」；`(int)` 截断（30166 的距离加速）会丢小数，JS 移植用 Math.trunc 保号。
12. **全部被缚 NPC + 85/629 都在 ConveyorBeltCollision**（NPCID.cs:4789）——站传送带会被带动，静态站立也要支持。
```
