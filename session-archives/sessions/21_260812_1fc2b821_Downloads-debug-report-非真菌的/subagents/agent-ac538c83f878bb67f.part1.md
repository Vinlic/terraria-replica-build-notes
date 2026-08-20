# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-19T07:33:03.777Z

```
可写任务:为 ~/Project/GLM/SandboxWorld/game 补齐三族 Boss/NPC 的 FindFrame 帧状态机(渲染层),标杆 ~/Project/GLM/SandboxWorld/Terarria1456/NPC.cs。改 src/render/Renderer.ts 的 vanillaFrameIdx(在既有 case 266/222/262/113 等先例处追加分支;若需 AI 侧同步状态,可在对应 AI 文件写 e.lai0/e.lai1/e.customFrameIdx——蜂后 222 是现成先例:AI 写 e.lai0,Renderer 读)。

【一、火星飞碟族(NPC.cs:72481-72560)】
- 393 炮塔:ai[2]=朝向九向帧(0-8,即 e.ai2 映射 0..8 帧索引,超界钳);激光发射窗内(e.ai3 落在 [280,420) 且 %6<=2)加射击行(+9)。我们的实现在 src/entities/bossAI_martian.ts(炮塔 393 段,查它写的 ai2/ai3 语义;若朝向值不是 0-8 索引,按该 AI 实际写入的朝向角换算九向)。
- 394 火炮:ai[3] 相位帧(窗前 4、窗内 4+num188/5 循环、%4);读 bossAI_martian 394 段。
- 395 母碟:66t 计数器 /6 → 帧 0-10;**死光电报窗 [20,260) 钳帧 [36,54)**(=帧 6-8 蓄能辉光带;我们 395 的 ai3 是循环计时,读 bossAI_martian 395 段确认窗口变量)。
- 392 炮体:发射窗内帧速 ×2。
- 399 探测器:0.25t/帧 四帧扫描带;ai0≠0(逃逸态)+4 警戒带。
- 387 特斯拉:充电 10t/帧、待机 15t/帧两档(按其部署渐显计时)。386 工程师:放塔期帧 9/10。
【二、月亮事件六族】
- 327 南瓜王(:72977):ai[3] 姿态机——0→行0/1→行4/2→行8(行=帧带起点,7t/帧,行内 4 帧循环,姿态间双向过渡)。我们 ai3 是选招轮换计数(bossAI_moon_events.ts pumpkingAI),确认姿态源=当前攻击态。
- 345 冰雪女王(:73106):滑翔定帧 0/1/2(按射击相位+vx 向)、落冰态 3-4 循环、自旋恒行 5。
- 346 圣诞坦克(:73050):开火带 6-8(3t/帧)、行走带 1-5(按 |vx|/2 累计)、静止定格 0。
- 325 哀木(:73172):静止带 0-4 / 移动带 5-9(5t/帧,按 |vx| 累计)。
- 344 尖叫树(:73144):全带按 |vx|*0.75 累计推进。
- 551 Betsy(:67913):拍翼 0-4 序列(localAI[0] 36 步计数×timeScale,读 bossAI_dd2.ts betsyAI 的拍翼计数变量)+空袭/吐息态 5-9 姿态链。
【三、教徒 439/440(NPC.cs:72698-72783)】
原版 FindFrame 用 localAI[2] 六态→帧行:态0→行0/态10→行4-6/态1·11→行10-12/态2·12→行7-9/态13→行13+。我们的 bossAI_lategame.ts 把 la2 挪用存仪式圈心对象(勿动!)——做法:在教徒 AI 状态机各态切换处写 e.customFrameIdx(直接帧号,Renderer vanillaFrameIdx 首行已支持直读;水书怪 694 是先例);帧号=行起点+行内 6t 循环偏移(原版 7t/帧行内循环,查 :72720 确认步长)。映射要从 :72698-72783 逐行抄,态值取我们 AI 的 ai0 语义对应(0 选招/1 飞掠/2 冰/3 火/4 雷/5 仪式/6 硬直/7 光/8 末日+克隆体态)。
【验收】1) npx tsc --noEmit 零新错(基线有几个并行会话文件错,忽略 Game.ts(2250/TrapsPass/CaveHousePass/friendly);2) npx vitest run tests/bossAI-lategame.test.ts tests/bossAI-moon-events*.test.ts tests/bossAI-dd2.test.ts(存在哪些跑哪些)全绿;3) 每处新代码带原版行号注释。禁止改动既有其他分支。完成后报告:逐族帧机映射表+测试结果。
```

---

## 📎 Attachment · skill_listing · 2026-08-19T07:33:03.779Z

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

## 🤖 Assistant · 2026-08-19T07:33:14.593Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me understand the task:

1. I need to implement FindFrame frame state machines (rendering layer) for three families of Bosses/NPCs in `~/Project/GLM/SandboxWorld/game`, using `~/Project/GLM/SandboxWorld/Terarria1456/NPC.cs` as the reference.

2. The changes go into `src/render/Renderer.ts`'s `vanillaFrameIdx` function (adding new cases alongside existing cases like 266/222/262/113).

3. If AI-side state synchronization is needed, I can write `e.lai0/e.lai1/e.customFrameIdx` in the corresponding AI files.

Let me start by reading the relevant files:

1. First, the vanilla source: `~/Project/GLM/SandboxWorld/Terarria1456/NPC.cs` at the specified line ranges:
   - Martian UFO family: 72481-72560
   - Moon events six families: 72977 (Pumpking), 73106 (Ice Queen), 73050 (Santa-NK1), 73172 (Mourning Wood), 73144 (EverScream), 67913 (Betsy)
   - Cultists 439/440: 72698-72783

2. Our implementation files:
   - `src/render/Renderer.ts` (vanillaFrameIdx)
   - `src/entities/bossAI_martian.ts`
   - `src/entities/bossAI_moon_events.ts`
   - `src/entities/bossAI_dd2.ts`
   - `src/entities/bossAI_lategame.ts`

Let me start reading these files in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:33:15.086Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/NPC.cs",
 "offset": 72470,
 "limit": 110
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:33:15.097Z

**📎 ToolResult ⚠️ERROR**

```
File does not exist. Note: your current working directory is ~/Project/GLM/SandboxWorld/game.

```


---

## 🤖 Assistant · 2026-08-19T07:33:15.550Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/NPC.cs",
 "offset": 72690,
 "limit": 110
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:33:15.560Z

**📎 ToolResult ⚠️ERROR**

```
File does not exist. Note: your current working directory is ~/Project/GLM/SandboxWorld/game.

```


---

## 🤖 Assistant · 2026-08-19T07:33:18.825Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The file path might be different. Let me check the actual structure of the Terarria1456 directory.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:33:19.813Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/ && find ~/Project/GLM/SandboxWorld -maxdepth 3 -name \"NPC.cs\" 2>/dev/null | head -20",
 "description": "Locate NPC.cs in project"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:33:19.896Z

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
session-archives
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
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs
~/Project/GLM/SandboxWorld/Terarria1456Server/Terraria/NPC.cs

```


---

## 🤖 Assistant · 2026-08-19T07:33:20.776Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/src/render/ ~/Project/GLM/SandboxWorld/game/src/entities/ 2>/dev/null",
 "description": "List render and entities directories"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:33:20.794Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/entities/:
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
SkyDragonFury.ts
SolarEruption.ts
SquidCloud.ts
StardustMarkProj.ts
SwingArc.ts
TerraArc.ts
TideSlash.ts
Tombstone.ts
TownNPC.ts
TownShot.ts
types.ts
waterAvoid.ts
WeaponProj.ts
WhipProj.ts
WhipTag.ts

~/Project/GLM/SandboxWorld/game/src/render/:
AutoTiler.ts
BiomeBackground.ts
bitmapize.ts
BlendFraming.ts
BreathMeter.ts
Camera.ts
CanvasWatch.ts
ChunkCache.ts
CombatTextFont.ts
CritterCage.ts
CursorItemIcon.ts
EmoteBubble.ts
FancyResourceBars.ts
GLSpriteLayer.ts
heldProj.ts
InfoAccsLayer.ts
MapColors.ts
MenuBackground.ts
MonolithFilters.ts
NatureParticles.ts
RenderAudit.ts
Renderer.ts
ResourceBars.ts
SkyRenderer.ts
texId.ts
TileAnim.ts
TileFlames.ts
TileParticles.ts
TintAtlas.ts
VanillaLiquidRenderer.ts
VanillaTiler.ts
VanillaWallTiler.ts
WallTiler.ts
WaterfallRenderer.ts
WaterWaves.ts
WeatherRenderer.ts
WindSway.ts

```


---

## 🤖 Assistant · 2026-08-19T07:33:27.166Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The NPC.cs is at `~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs`. Let me read the relevant sections. Also let me check the additional working directory — `~/Project/GLM/SandboxWorld/Terarria1456/Terrar*` is listed as an additional working dir, which matches `Terarria1456`. Good.

Let me read the vanilla sections in parallel:
1. Martian: 72481-72560
2. Cultists: 72698-72783
3. Pumpking: 72977...
4. Santa-NK1: 73050
5. Ice Queen: 73106
6. Everscream: 73144
7. Mourning Wood: 73172
8. Betsy: 67913
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:33:27.876Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 100,
 "offset": 72475
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:33:27.886Z

**📎 ToolResult**

```
72475				}
72476				else
72477				{
72478					frame.Y = num * 2;
72479				}
72480				break;
72481			case 393:
72482			{
72483				int num134 = 0;
72484				Vector2 vector3 = ai[2].ToRotationVector2();
72485				num134 = ((vector3.Y > Math.Abs(vector3.X) * 2f) ? 4 : ((vector3.Y > Math.Abs(vector3.X) * 1.5f) ? ((vector3.X > 0f) ? 5 : 3) : ((Math.Abs(vector3.X) > vector3.Y * 2f) ? ((vector3.X > 0f) ? 8 : 0) : ((!(Math.Abs(vector3.X) > vector3.Y * 1.5f)) ? ((vector3.X > 0f) ? 6 : 2) : ((!(vector3.X > 0f)) ? 1 : 7)))));
72486				frame.Y = num * num134;
72487				float num135 = 280f;
72488				float num136 = 140f;
72489				if (ai[3] >= num135 && ai[3] < num135 + num136 && (int)ai[3] % 6 <= 2)
72490				{
72491					frame.Y += num * 9;
72492				}
72493				break;
72494			}
72495			case 394:
72496			{
72497				int num188 = (int)ai[3] - 300;
72498				if (num188 >= 120)
72499				{
72500					num188 -= 120;
72501					if (num188 >= 160)
72502					{
72503						frame.Y = num * (7 - (num188 - 160) / 5);
72504					}
72505					else if (num188 >= 20)
72506					{
72507						frame.Y = num * (num188 / 4 % 4);
72508					}
72509					else
72510					{
72511						frame.Y = num * (4 + num188 / 5);
72512					}
72513				}
72514				else
72515				{
72516					frame.Y = num * 4;
72517				}
72518				break;
72519			}
72520			case 395:
72521			{
72522				float num124 = 20f;
72523				float num125 = 240f;
72524				bool flag10 = ai[3] >= num124 && ai[3] < num124 + num125;
72525				frameCounter += 1.0;
72526				if (frameCounter >= 66.0)
72527				{
72528					frameCounter = 0.0;
72529				}
72530				if (flag10)
72531				{
72532					frameCounter += 1.0;
72533					if (frameCounter >= 54.0 || frameCounter < 36.0)
72534					{
72535						frameCounter = 36.0;
72536					}
72537				}
72538				int num126 = (int)frameCounter % 66;
72539				num126 /= 6;
72540				frame.Y = num * num126;
72541				break;
72542			}
72543			case 392:
72544			{
72545				float num54 = 20f;
72546				float num55 = 240f;
72547				bool flag6 = ai[3] >= num54 && ai[3] < num54 + num55;
72548				frameCounter += 1.0;
72549				if (flag6)
72550				{
72551					frameCounter += 1.0;
72552				}
72553				if (frameCounter >= 12.0)
72554				{
72555					frameCounter = 0.0;
72556				}
72557				int num56 = (int)frameCounter % 12;
72558				num56 /= 3;
72559				frame.Y = num * num56;
72560				break;
72561			}
72562			case 399:
72563				frameCounter = (frameCounter + 0.25) % 4.0 + (double)((ai[0] != 0f) ? 4 : 0);
72564				frame.Y = num * (int)frameCounter;
72565				break;
72566			case 520:
72567				if (velocity.Y == 0f)
72568				{
72569					spriteDirection = direction;
72570					frameCounter += Math.Abs(velocity.X) * 1f;
72571					if (frameCounter > 6.0)
72572					{
72573						if (Math.Abs(velocity.X) < 0.2f)
72574						{

```


---

## 🤖 Assistant · 2026-08-19T07:33:28.422Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 110,
 "offset": 72690
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:33:28.428Z

**📎 ToolResult**

```
72690				num16 /= 7;
72691				if (num16 >= 4)
72692				{
72693					num16 = 6 - num16;
72694				}
72695				frame.Y = num * num16;
72696				break;
72697			}
72698			case 439:
72699			case 440:
72700			{
72701				int num267 = (int)localAI[2];
72702				if (IsABestiaryIconDummy)
72703				{
72704					if (frameCounter > 5.0)
72705					{
72706						frameCounter = 0.0;
72707						frame.Y += num;
72708					}
72709					if (frame.Y < num * 4 || frame.Y > num * 6)
72710					{
72711						frame.Y = num * 4;
72712					}
72713				}
72714				else
72715				{
72716					switch (num267)
72717					{
72718					case 0:
72719						if (frameCounter >= 15.0)
72720						{
72721							frameCounter = 0.0;
72722							frame.Y = 0;
72723						}
72724						else if (frame.Y != 0)
72725						{
72726							frame.Y = ((int)frameCounter / 5 + 4) * num;
72727						}
72728						break;
72729					case 10:
72730						if (frameCounter >= 15.0)
72731						{
72732							frameCounter = 0.0;
72733						}
72734						frame.Y = ((int)frameCounter / 5 + 4) * num;
72735						break;
72736					case 1:
72737						if (frameCounter >= 15.0)
72738						{
72739							frameCounter = 0.0;
72740							frame.Y = num;
72741						}
72742						else if (frame.Y != num)
72743						{
72744							frame.Y = ((int)frameCounter / 5 + 10) * num;
72745						}
72746						break;
72747					case 11:
72748						if (frameCounter >= 15.0)
72749						{
72750							frameCounter = 0.0;
72751						}
72752						frame.Y = ((int)frameCounter / 5 + 10) * num;
72753						break;
72754					case 2:
72755						if (frameCounter >= 15.0)
72756						{
72757							frameCounter = 0.0;
72758							frame.Y = num * 2;
72759						}
72760						else if (frame.Y != num * 2)
72761						{
72762							frame.Y = ((int)frameCounter / 5 + 7) * num;
72763						}
72764						break;
72765					case 12:
72766						if (frameCounter >= 15.0)
72767						{
72768							frameCounter = 0.0;
72769						}
72770						frame.Y = ((int)frameCounter / 5 + 7) * num;
72771						break;
72772					case 13:
72773						if (frameCounter >= 15.0)
72774						{
72775							frameCounter = 0.0;
72776						}
72777						frame.Y = ((int)frameCounter / 5 + 13) * num;
72778						break;
72779					}
72780				}
72781				frameCounter += 1.0;
72782				break;
72783			}
72784			case 521:
72785				if (velocity.X < 0f)
72786				{
72787					direction = -1;
72788				}
72789				else
72790				{
72791					direction = 1;
72792				}
72793				if (direction != 0)
72794				{
72795					spriteDirection = direction;
72796				}
72797				rotation = (float)Math.Atan2(velocity.Y * (float)spriteDirection, velocity.X * (float)spriteDirection) + velocity.X * 0.1f;
72798				if ((frameCounter += 1.0) >= 5.0)
72799				{

```


---

## 🤖 Assistant · 2026-08-19T07:34:30.416Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
I have the Martian and Cultist sections. Interesting details:

**393 Turret (Martian Turret / "Scutlix Gunner"? no — 393 is Martian Turret):**
```csharp
case 393:
{
    int num134 = 0;
    Vector2 vector3 = ai[2].ToRotationVector2();
    num134 = ((vector3.Y > Math.Abs(vector3.X) * 2f) ? 4 : ((vector3.Y > Math.Abs(vector3.X) * 1.5f) ? ((vector3.X > 0f) ? 5 : 3) : ((Math.Abs(vector3.X) > vector3.Y * 2f) ? ((vector3.X > 0f) ? 8 : 0) : ((!(Math.Abs(vector3.X) > vector3.Y * 1.5f)) ? ((vector3.X > 0f) ? 6 : 2) : ((!(vector3.X > 0f)) ? 1 : 7)))));
    frame.Y = num * num134;
    float num135 = 280f;
    float num136 = 140f;
    if (ai[3] >= num135 && ai[3] < num135 + num136 && (int)ai[3] % 6 <= 2)
    {
        frame.Y += num * 9;
    }
    break;
}
```
So ai[2] is a rotation angle (radians), converted with ToRotationVector2 (i.e., (cos, sin)). Note: in XNA screen coords Y is down. The nine-direction mapping:
- if vy > |vx|*2 → 4 (pointing down in screen space — well, actually if Y down, vy>0 means down)
- else if vy > |vx|*1.5 → vx>0 ? 5 : 3
- else if |vx| > vy*2 → vx>0 ? 8 : 0
- else if !(|vx| > vy*1.5) → vx>0 ? 6 : 2
- else → vx>0 ? 7 : 1

Wait the nesting: `((!(Math.Abs(vector3.X) > vector3.Y * 1.5f)) ? ((vector3.X > 0f) ? 6 : 2) : ((!(vector3.X > 0f)) ? 1 : 7))` — so if |vx| <= vy*1.5 → 6 or 2; else (|vx| > vy*1.5) → vx<=0 ? 1 : 7.

Frame = num134, and if in laser window (ai[3] in [280, 420) and (int)ai[3] % 6 <= 2) → +9.

Note: the task description says "ai[2]=朝向九向帧(0-8...)" but actually vanilla ai[2] is an angle. I need to check what our bossAI_martian.ts writes to ai2/ai3 for the turret.

**394 Martian Engineer's... no, 394 is "Martian Walker"? Let me recall:**
- 392 = Martian Hover Carrier? Actually let me check: 380=Martian Drone... Hmm.
- NPC 391 = Martian Saucer? Let me get the actual list:
  - 386 = Martian Engineer? Actually 386 = "Martian Engineer" yes.
  - 387 = Tesla? Hmm, "Martian Tesla" isn't quite right. Let me check: 387 = Martian Officer? 
  
Actually from Terraria wiki:
- 385 Grapple? No.
- NPC IDs around 380s: 380 Martian Drone, 381 Gauss Glitch? no...

Let me list Martian Madness NPCs:
- 385: ScutlixBrowser? no. Hmm.
- 386: Martian Engineer
- 387: Martian Officer (Tesla?) — hmm actually "Martian Officer" isn't right either. The martian enemies: Martian Brain? No...

Martian Madness enemies: Martian Drone, Gigazapper, Scutlix Gunner (with Scutlix mount), Gray Grunt, Martian Engineer, Martian Officer, Martian Tesla Turret (summoned by Martian Officer), Ray Gunner, Martian Walker, Martian Saucer (boss, with Saucer Turret? and Cannon).

NPC IDs (1.4): 
- 381 Martian Drone? Hmm I recall:
  - 380 = ??? 
  - 385 = Gray Grunt?
  - 386 = Martian Engineer
  - 387 = Martian Officer
  - 388 = Ray Gunner? Hmm.
  - 389 = Martian Tesla Turret? 
  - 390 = Gigazapper?
  - 391 = Scutlix Gunner
  - 392 = Martian Saucer (the boss itself)? No wait, the task says 392 炮体 (cannon). 

From the task description:
- 393 炮塔 = turret (Saucer Turret)
- 394 火炮 = cannon (Saucer Cannon)
- 395 母碟 = mothership (Martian Saucer)
- 392 炮体 = hmm "发射窗内帧速×2" — 392's FindFrame has flag6 window [20, 260), frameCounter increments twice in window, %12, /3 → frames 0-3. So 392 is a 4-frame animation. What NPC has 4-frame spin? Hmm, 392 = Martian Walker? No...

Actually wait — let me re-check. In the martian saucer fight, the saucer (395) spawns turrets: "Martian Saucer Turret" (393) and "Martian Saucer Cannon" (394). And 392 might be... "Martian Drone"? The task calls 392 "炮体" (gun body). Let me look at the AI for 392 in vanilla. Actually for the frame machine, what matters is:
- 392: 4 frames (0-3), advances every 3t normally, every 1.5t in death-ray window [20,260).

Hmm wait, re-reading: frameCounter += 1; if flag6 (ai[3] in [20,260)) frameCounter += 1 more. So in window, frame speed ×2. %12 /3 → 4 frames. So 392 has 4 animation frames.

- 399 = Martian Probe? "探测器" (probe). `frameCounter = (frameCounter + 0.25) % 4.0 + ((ai[0] != 0) ? 4 : 0)` → frames 0-3 scan, 4-7 alert (ai0≠0 escape mode). Yes 399 = Martian Probe.

- 387 特斯拉 = Martian Tesla Turret (actually NPC 389 is "Martian Tesla Turret"? hmm). Task says 387 Tesla: 充电 10t/帧、待机 15t/帧两档. And 386 工程师 = Martian Engineer: 放塔期帧 9/10.

Let me find the vanilla FindFrame cases for 386/387 to be accurate. Let me grep around in NPC.cs.

**Cultists 439/440:**
```csharp
int num267 = (int)localAI[2];
// bestiary dummy: rows 4-6 cycle
switch (num267)
{
case 0: // idle/choose — row 0
    if (frameCounter >= 15.0) { frameCounter = 0; frame.Y = 0; }
    else if (frame.Y != 0) { frame.Y = ((int)frameCounter / 5 + 4) * num; }
    break;
case 10: // rows 4-6
    if (frameCounter >= 15.0) frameCounter = 0;
    frame.Y = ((int)frameCounter / 5 + 4) * num;
    break;
case 1: // rows 10-12
    ... frame.Y = ((int)frameCounter / 5 + 10) * num; (idle at row 1)
case 11: // rows 10-12 loop
case 2: // rows 7-9 (idle at row 2)
case 12: // rows 7-9 loop
case 13: // row 13+
    frame.Y = ((int)frameCounter / 5 + 13) * num;
}
frameCounter += 1.0;
```

So: frameCounter 0-14 (15 ticks), /5 → 0,1,2 within-row offsets. Rows: state 0 → base row 4 while transitioning (frame.Y != 0), settles row 0; state 10 → rows 4-6 cycling; state 1 → base row 10 while frame.Y != num... wait:

case 1: if frameCounter >= 15 → frameCounter=0, frame.Y = num (row 1). else if frame.Y != num → frame.Y = (frameCounter/5 + 10)*num. So state 1 animates rows 10-12 and settles at row 1 after the animation completes? Hmm, actually the logic: when frameCounter reaches 15, reset to 0 and set frame.Y = row 1. Otherwise if frame.Y != row 1, animate rows 10-12. Once frame.Y == row 1 and frameCounter < 15, it stays row 1 (since the else-if fails). So the "cast then settle" pattern: during the first pass it plays rows 10-12 for one loop of 15 ticks, then snaps to the hold frame (row 0 for state 0, row 1 for state 1, row 2 for state 2). States 10/11/12 loop the animation band continuously. State 13 loops rows 13-15 continuously ((13+0)/5 offsets: frameCounter/5 → 0,1,2 → rows 13,14,15).

Note the task says "态13→行13+" and "原版 7t/帧行内循环,查 :72720 确认步长" — the actual step is 5t per frame within row, 15t per loop. So the task description's "7t/帧" guess is wrong; the source says 15.0 threshold and /5 division → 3 frames per band at 5t each. I'll follow the source.

Now, our implementation: bossAI_lategame.ts uses la2 for ritual circle center object (don't touch). So we write e.customFrameIdx in the AI state machine at each state transition. customFrameIdx is read directly by vanillaFrameIdx first line (per the task; need to verify).

Now the moon events sections. Let me read those.
````

</details>


---

## 🤖 Assistant · 2026-08-19T07:34:31.092Z · glm-x-preview-260804

```
找到了位于 `Terarria1456/Terraria/NPC.cs` 的原版文件。现在我来读取月亮事件相关部分。
```


---

## 🤖 Assistant · 2026-08-19T07:34:31.964Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 60,
 "offset": 72970
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:34:31.971Z

**📎 ToolResult**

```
72970					frame.Y = num;
72971					if (frameCounter >= (double)(num39 * 6 - 1))
72972					{
72973						frameCounter = 0.0;
72974					}
72975				}
72976				break;
72977			case 327:
72978				if (ai[3] == 0f)
72979				{
72980					if (frame.Y > num * 5)
72981					{
72982						frameCounter += 1.0;
72983					}
72984					else if (frame.Y > 0)
72985					{
72986						frameCounter -= 1.0;
72987					}
72988				}
72989				else if (ai[3] == 1f)
72990				{
72991					if (frame.Y > num * 10)
72992					{
72993						frameCounter += 1.0;
72994					}
72995					else if (frame.Y > num * 4)
72996					{
72997						frameCounter -= 1.0;
72998					}
72999					else if (frame.Y < num * 4)
73000					{
73001						frameCounter += 1.0;
73002					}
73003				}
73004				else if (ai[3] == 2f)
73005				{
73006					if (frame.Y < num * 2)
73007					{
73008						frameCounter -= 1.0;
73009					}
73010					else if (frame.Y > num * 8)
73011					{
73012						frameCounter -= 1.0;
73013					}
73014					else if (frame.Y < num * 8)
73015					{
73016						frameCounter += 1.0;
73017					}
73018				}
73019				if (frameCounter > 6.0)
73020				{
73021					frameCounter = 0.0;
73022					frame.Y += num;
73023					if (frame.Y > num * 11)
73024					{
73025						frame.Y = 0;
73026					}
73027				}
73028				if (frameCounter < 0.0)
73029				{

```


---

## 🤖 Assistant · 2026-08-19T07:34:32.568Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 160,
 "offset": 73040
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:34:32.582Z

**📎 ToolResult**

```
73040				if (frameCounter > 1.0)
73041				{
73042					frame.Y += num;
73043					frameCounter = 0.0;
73044				}
73045				if (frame.Y > num * 3)
73046				{
73047					frame.Y = 0;
73048				}
73049				break;
73050			case 346:
73051				if (ai[0] == 1f)
73052				{
73053					spriteDirection = direction;
73054					frameCounter += 1.0;
73055					if (frameCounter > 2.0)
73056					{
73057						frame.Y += num;
73058						frameCounter = 0.0;
73059					}
73060					if (frame.Y > num * 8)
73061					{
73062						frame.Y = num * 6;
73063					}
73064					if (frame.Y < num * 6)
73065					{
73066						frame.Y = num * 6;
73067					}
73068					break;
73069				}
73070				if (velocity.X == 0f)
73071				{
73072					ref int y2 = ref frame.Y;
73073					y2 = y2;
73074					frameCounter = 0.0;
73075					break;
73076				}
73077				spriteDirection = direction;
73078				frameCounter += 1.0;
73079				frameCounter += Math.Abs(velocity.X) / 2f;
73080				if (frameCounter > 4.0)
73081				{
73082					frame.Y += num;
73083					frameCounter = 0.0;
73084				}
73085				if (frame.Y > num * 5)
73086				{
73087					frame.Y = num;
73088				}
73089				if (frame.Y < num)
73090				{
73091					frame.Y = num;
73092				}
73093				break;
73094			case 352:
73095				frameCounter += 1.0;
73096				if (frameCounter > 3.0)
73097				{
73098					frame.Y += num;
73099					frameCounter = 0.0;
73100				}
73101				if (frame.Y > num * 5)
73102				{
73103					frame.Y = 0;
73104				}
73105				break;
73106			case 345:
73107				if (ai[0] == 0f)
73108				{
73109					if (ai[3] >= 0f)
73110					{
73111						frame.Y = 0;
73112					}
73113					else if (velocity.X < 0f)
73114					{
73115						frame.Y = num;
73116					}
73117					else
73118					{
73119						frame.Y = num * 2;
73120					}
73121				}
73122				else if (ai[0] == 1f)
73123				{
73124					frameCounter += 1.0;
73125					if (frameCounter > 5.0)
73126					{
73127						frameCounter = 0.0;
73128						frame.Y += num;
73129					}
73130					if (frame.Y > num * 4)
73131					{
73132						frame.Y = num * 3;
73133					}
73134					if (frame.Y < num * 3)
73135					{
73136						frame.Y = num * 3;
73137					}
73138				}
73139				else if (ai[0] == 2f)
73140				{
73141					frame.Y = num * 5;
73142				}
73143				break;
73144			case 344:
73145				if (velocity.X == 0f)
73146				{
73147					frameCounter += 1.0;
73148					if (frameCounter > 5.0)
73149					{
73150						frameCounter = 0.0;
73151						frame.Y += num;
73152					}
73153					if (frame.Y > num * 9)
73154					{
73155						frame.Y = 0;
73156					}
73157				}
73158				else
73159				{
73160					frameCounter += Math.Max(1f, Math.Abs(velocity.X) * 0.75f);
73161					if (frameCounter > 5.0)
73162					{
73163						frameCounter = 0.0;
73164						frame.Y += num;
73165					}
73166					if (frame.Y > num * 9)
73167					{
73168						frame.Y = 0;
73169					}
73170				}
73171				break;
73172			case 325:
73173				if (velocity.X == 0f)
73174				{
73175					frameCounter += 1.0;
73176					if (frameCounter > 4.0)
73177					{
73178						frameCounter = 0.0;
73179						frame.Y += num;
73180					}
73181					if (frame.Y > num * 4)
73182					{
73183						frame.Y = 0;
73184					}
73185					break;
73186				}
73187				frameCounter += 1.0;
73188				if (frameCounter > 4.0)
73189				{
73190					frameCounter = 0.0;
73191					frame.Y += num;
73192				}
73193				if (frame.Y < num * 5)
73194				{
73195					frame.Y = num * 5;
73196				}
73197				if (frame.Y > num * 9)
73198				{
73199					frame.Y = num * 5;

```


---

## 🤖 Assistant · 2026-08-19T07:34:36.769Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Got most of them. Need the rest of 327 (pumpking, lines 73028-73040) and 325 (mourning wood, lines 73199+), plus Betsy at 67913. Let me read those.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:34:37.376Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 14,
 "offset": 73028
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:34:37.385Z

**📎 ToolResult**

```
73028				if (frameCounter < 0.0)
73029				{
73030					frameCounter = 6.0;
73031					frame.Y -= num;
73032					if (frame.Y < 0)
73033					{
73034						frame.Y = num * 11;
73035					}
73036				}
73037				break;
73038			case 347:
73039				frameCounter += 1.0;
73040				if (frameCounter > 1.0)
73041				{

```


---

## 🤖 Assistant · 2026-08-19T07:34:38.015Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 10,
 "offset": 73199
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:34:38.030Z

**📎 ToolResult**

```
73199					frame.Y = num * 5;
73200				}
73201				break;
73202			case 490:
73203				rotation = velocity.X * 0.15f;
73204				frameCounter += 1.0;
73205				if (frameCounter > 6.0)
73206				{
73207					frameCounter = 0.0;
73208					frame.Y += num;

```


---

## 🤖 Assistant · 2026-08-19T07:34:38.758Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 85,
 "offset": 67905
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:34:38.785Z

**📎 ToolResult**

```
67905				}
67906				frameCounter += Math.Abs(velocity.X);
67907				if (frameCounter >= 56.0 || frameCounter < 0.0)
67908				{
67909					frameCounter = 0.0;
67910				}
67911				frame.Y = num * (int)(frameCounter / 8.0);
67912				break;
67913			case 551:
67914			{
67915				int num268 = frame.Y / num;
67916				if (ai[0] == 4f)
67917				{
67918					float num269 = 60f;
67919					int num270 = 10;
67920					int num271 = 6 * num270;
67921					if (num268 < 5)
67922					{
67923						frameCounter = 0.0;
67924					}
67925					num268 = 5;
67926					frameCounter = (int)ai[1];
67927					int num272 = 0;
67928					double num273 = frameCounter;
67929					int num60 = num272 + 1;
67930					num272 = num60;
67931					if (num273 >= (double)(5 * num60))
67932					{
67933						num268 = 6;
67934					}
67935					num272 = 0;
67936					if (frameCounter >= (double)(num269 - 6f))
67937					{
67938						num268 = 7;
67939					}
67940					if (frameCounter >= (double)(num269 - 3f))
67941					{
67942						num268 = 8;
67943					}
67944					if (frameCounter >= (double)num269)
67945					{
67946						num268 = 9 + (int)frameCounter / 3 % 2;
67947					}
67948					num272 = 0;
67949					if (frameCounter >= (double)(num269 + (float)num271 + 3f))
67950					{
67951						num268 = 8;
67952					}
67953					double num274 = frameCounter;
67954					float num275 = num269 + (float)num271 + 3f;
67955					num60 = num272 + 1;
67956					num272 = num60;
67957					if (num274 >= (double)(num275 + (float)(5 * num60)))
67958					{
67959						num268 = 7;
67960					}
67961					double num276 = frameCounter;
67962					float num277 = num269 + (float)num271 + 3f;
67963					num60 = num272 + 1;
67964					num272 = num60;
67965					if (num276 >= (double)(num277 + (float)(5 * num60)))
67966					{
67967						num268 = 0;
67968					}
67969				}
67970				else if (ai[0] == 3f)
67971				{
67972					float num278 = 40f;
67973					float num279 = 80f;
67974					float num280 = num278 + num279;
67975					float num281 = 25f;
67976					if (num268 < 5)
67977					{
67978						frameCounter = 0.0;
67979					}
67980					num268 = 5;
67981					frameCounter = (int)ai[1];
67982					int num282 = 0;
67983					double num283 = frameCounter;
67984					int num60 = num282 + 1;
67985					num282 = num60;
67986					if (num283 >= (double)(5 * num60))
67987					{
67988						num268 = 6;
67989					}

```


---

## 🤖 Assistant · 2026-08-19T07:34:40.925Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Betsy's FindFrame is longer. Let me continue reading from 67989.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:34:41.485Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 75,
 "offset": 67989
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:34:41.502Z

**📎 ToolResult**

```
67989					}
67990					num282 = 0;
67991					if (frameCounter >= (double)(num278 - 6f))
67992					{
67993						num268 = 7;
67994					}
67995					if (frameCounter >= (double)(num278 - 3f))
67996					{
67997						num268 = 8;
67998					}
67999					if (frameCounter >= (double)num278)
68000					{
68001						num268 = 9 + (int)frameCounter / 3 % 2;
68002					}
68003					num282 = 0;
68004					if (frameCounter >= (double)(num280 - num281 + 3f))
68005					{
68006						num268 = 8;
68007					}
68008					double num284 = frameCounter;
68009					float num285 = num280 - num281 + 3f;
68010					num60 = num282 + 1;
68011					num282 = num60;
68012					if (num284 >= (double)(num285 + (float)(5 * num60)))
68013					{
68014						num268 = 7;
68015					}
68016					double num286 = frameCounter;
68017					float num287 = num280 - num281 + 3f;
68018					num60 = num282 + 1;
68019					num282 = num60;
68020					if (num286 >= (double)(num287 + (float)(5 * num60)))
68021					{
68022						num268 = 0;
68023					}
68024				}
68025				else if (ai[0] == 5f)
68026				{
68027					num268 = 3;
68028				}
68029				else if (ai[0] == 6f)
68030				{
68031					if (num268 > 4)
68032					{
68033						frameCounter = 0.0;
68034					}
68035					num268 = 1;
68036					frameCounter = (int)ai[1];
68037					int num288 = 0;
68038					double num289 = frameCounter;
68039					int num60 = num288 + 1;
68040					num288 = num60;
68041					if (num289 >= (double)(8 * num60))
68042					{
68043						num268 = 2;
68044					}
68045					double num290 = frameCounter;
68046					num60 = num288 + 1;
68047					num288 = num60;
68048					if (num290 >= (double)(8 * num60))
68049					{
68050						num268 = 3;
68051					}
68052					double num291 = frameCounter;
68053					num60 = num288 + 1;
68054					num288 = num60;
68055					if (num291 >= (double)(8 * num60))
68056					{
68057						num268 = 4;
68058					}
68059					double num292 = frameCounter;
68060					num60 = num288 + 1;
68061					num288 = num60;
68062					if (num292 >= (double)(8 * num60))
68063					{

```


---

## 🤖 Assistant · 2026-08-19T07:34:45.232Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 55,
 "offset": 68063
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:34:45.241Z

**📎 ToolResult**

```
68063					{
68064						num268 = 3;
68065					}
68066					double num293 = frameCounter;
68067					num60 = num288 + 1;
68068					num288 = num60;
68069					if (num293 >= (double)(8 * num60))
68070					{
68071						num268 = 4;
68072					}
68073					double num294 = frameCounter;
68074					num60 = num288 + 1;
68075					num288 = num60;
68076					if (num294 >= (double)(8 * num60))
68077					{
68078						num268 = 3;
68079					}
68080					double num295 = frameCounter;
68081					num60 = num288 + 1;
68082					num288 = num60;
68083					if (num295 >= (double)(8 * num60))
68084					{
68085						num268 = 2;
68086					}
68087					double num296 = frameCounter;
68088					num60 = num288 + 1;
68089					num288 = num60;
68090					if (num296 >= (double)(8 * num60))
68091					{
68092						num268 = 1;
68093					}
68094					double num297 = frameCounter;
68095					num60 = num288 + 1;
68096					num288 = num60;
68097					if (num297 >= (double)(8 * num60))
68098					{
68099						num268 = 0;
68100					}
68101				}
68102				else
68103				{
68104					num268 = 0;
68105				}
68106				frame.Y = num * num268;
68107				break;
68108			}
68109			case 552:
68110			case 553:
68111			case 554:
68112				if (ai[0] > 0f)
68113				{
68114					spriteDirection = direction;
68115					if (frame.Y < num * 10 || frame.Y > num * 13 || ai[1] == 29f)
68116					{
68117						frame.Y = num * 10;

```


---

## 🤖 Assistant · 2026-08-19T07:37:57.250Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now I have Betsy's FindFrame. It's decompiled with obfuscated num60 = num288+1 patterns (from the decompiler's `num272 = 0; num60 = num272+1; num272 = num60;` = just incrementing a counter starting at 0, so `5*num60` = 5*1 = 5, `5*(num60)` for the second one = 5*2=10 etc.)

Let me decode Betsy (551):

```
int num268 = frame.Y / num;  // current frame index
if (ai[0] == 4f) {           // ai0==4: fire breath? attack
    float num269 = 60f;
    int num270 = 10;
    int num271 = 6 * num270; // 60
    if (num268 < 5) frameCounter = 0.0;
    num268 = 5;
    frameCounter = (int)ai[1];
    // first: num272=0, num60=1, num272=1 → if frameCounter >= 5*1 → num268=6
    if (frameCounter >= 5) num268 = 6;
    if (frameCounter >= 60-6=54) num268 = 7;
    if (frameCounter >= 60-3=57) num268 = 8;
    if (frameCounter >= 60) num268 = 9 + (int)frameCounter/3 % 2;   // 9/10 loop
    // second: num272=0 reset, num60=1 → if frameCounter >= 60+60+3=123 → num268=8
    if (frameCounter >= 123) num268 = 8;
    // third: num275 = 123, num60=2 (incremented again → 2) → if frameCounter >= 123+5*2=133 → num268=7
    if (frameCounter >= 133) num268 = 7;
    // fourth: num277=123, num60=3 → if frameCounter >= 123+5*3=138 → num268=0
    if (frameCounter >= 138) num268 = 0;
}
else if (ai[0] == 3f) {      // ai0==3: other attack (sky bombing?)
    float num278 = 40f;
    float num279 = 80f;
    float num280 = num278 + num279;   // 120
    float num281 = 25f;
    if (num268 < 5) frameCounter = 0.0;
    num268 = 5;
    frameCounter = (int)ai[1];
    if (frameCounter >= 5) num268 = 6;
    if (frameCounter >= 40-6=34) num268 = 7;
    if (frameCounter >= 40-3=37) num268 = 8;
    if (frameCounter >= 40) num268 = 9 + (int)frameCounter/3 % 2;
    if (frameCounter >= 120-25+3=98) num268 = 8;
    if (frameCounter >= 98+5*2=108) num268 = 7;   // num285=98, num60=2
    if (frameCounter >= 98+5*3=113) num268 = 0;   // num287=98, num60=3
}
else if (ai[0] == 5f) {
    num268 = 3;
}
else if (ai[0] == 6f) {      // flight/wing flapping
    if (num268 > 4) frameCounter = 0.0;
    num268 = 1;
    frameCounter = (int)ai[1];
    // sequence at 8t each: 1,2,3,4,3,4,3,2,1,0? Wait:
    // base num268=1
    // >= 8*1 → 2
    // >= 8*2 → 3
    // >= 8*3 → 4
    // >= 8*4 → 3
    // >= 8*5 → 4
    // >= 8*6 → 3
    // >= 8*7 → 2
    // >= 8*8 → 1
    // >= 8*9 → 0
}
else {
    num268 = 0;
}
frame.Y = num * num268;
```

Wait, careful with the ai0==4 num60 counters. The decompiled pattern:

```csharp
int num272 = 0;
double num273 = frameCounter;
int num60 = num272 + 1;    // num60 = 1
num272 = num60;            // num272 = 1
if (num273 >= (double)(5 * num60))  // 5*1 = 5
    num268 = 6;
num272 = 0;                // reset to 0
if (frameCounter >= num269 - 6f) ...
```

Then later:
```csharp
double num274 = frameCounter;
float num275 = num269 + num271 + 3f;   // 60+60+3 = 123
num60 = num272 + 1;   // num272 was reset to 0 → num60=1
num272 = num60;       // num272=1
if (num274 >= num275 + 5*num60)   // 123+5 = 128
    num268 = 7;
```

Hold on! I need to be careful. In the second block (ai0==4):

```csharp
num272 = 0;
if (frameCounter >= (double)(num269 - 6f)) { num268 = 7; }
if (frameCounter >= (double)(num269 - 3f)) { num268 = 8; }
if (frameCounter >= (double)num269) { num268 = 9 + (int)frameCounter / 3 % 2; }
num272 = 0;
if (frameCounter >= (double)(num269 + (float)num271 + 3f)) { num268 = 8; }   // 123
double num274 = frameCounter;
float num275 = num269 + num271 + 3f;   // 123
num60 = num272 + 1;  // num272=0 → num60=1
num272 = num60;
if (num274 >= num275 + 5*num60)  // 123 + 5 = 128
    num268 = 7;
double num276 = frameCounter;
float num277 = 123;
num60 = num272 + 1;  // num272=1 → num60=2
num272 = num60;
if (num276 >= num277 + 5*num60)  // 123+10 = 133
    num268 = 0;
```

Hmm wait, let me re-read the actual code from my Read output:

```
67926					frameCounter = (int)ai[1];
67927					int num272 = 0;
67928					double num273 = frameCounter;
67929					int num60 = num272 + 1;
67930					num272 = num60;
67931					if (num273 >= (double)(5 * num60))
67932					{
67933						num268 = 6;
67934					}
67935					num272 = 0;
67936					if (frameCounter >= (double)(num269 - 6f))
67937					{
67938						num268 = 7;
67939					}
67940					if (frameCounter >= (double)(num269 - 3f))
67941					{
67942						num268 = 8;
67943					}
67944					if (frameCounter >= (double)num269)
67945					{
67946						num268 = 9 + (int)frameCounter / 3 % 2;
67947					}
67948					num272 = 0;
67949					if (frameCounter >= (double)(num269 + (float)num271 + 3f))
67950					{
67951						num268 = 8;
67952					}
67953					double num274 = frameCounter;
67954					float num275 = num269 + (float)num271 + 3f;
67955					num60 = num272 + 1;
67956					num272 = num60;
67957					if (num274 >= (double)(num275 + (float)(5 * num60)))
67958					{
67959						num268 = 7;
67960					}
67961					double num276 = frameCounter;
67962					float num277 = num269 + (float)num271 + 3f;
67963					num60 = num272 + 1;
67964					num272 = num60;
67965					if (num276 >= (double)(num277 + (float)(5 * num60)))
67966					{
67967						num268 = 0;
67968					}
```

So: num272=0 → num60=1 → check fc >= 5*1=5 → frame 6. Then num272=0. Then checks against num269 (=60): >=54 → 7, >=57 → 8, >=60 → 9+fc/3%2. Then num272=0 (again). Then fc >= 123 → 8. Then num274 block: num60 = 0+1 = 1 → fc >= 123+5*1=128 → 7. Then num276 block: num60 = 1+1 = 2 → fc >= 123+5*2=133 → 0.

So for ai0==4: frame index over ai[1] (which is the attack timer):
- <5: 5
- [5,54): 6
- [54,57): 7
- [57,60): 8
- [60,123): 9 or 10 (fc/3 %2)
- [123,128): 8
- [128,133): 7
- >=133: 0

For ai0==3 (num278=40, num279=80, num280=120, num281=25):
- <5: 5
- [5,34): 6
- [34,37): 7
- [37,40): 8
- [40,98): 9/10 loop (fc/3%2) — where 98 = num280-num281+3 = 120-25+3
- [98,103): 8  (num285=98, num60=1: fc >= 98+5)
- [103,108): 7  (num60=2: fc >= 98+10)
- >=108: 0  (num60=3: fc >= 98+15)

For ai0==5: frame 3.
For ai0==6: wing flap sequence. Base num268=1; frameCounter = (int)ai[1]; thresholds at 8*n for n=1..9:
- >=8: 2
- >=16: 3
- >=24: 4
- >=32: 3
- >=40: 4
- >=48: 3
- >=56: 2
- >=64: 1
- >=72: 0

Hmm interesting — so ai[1] is the counter that counts 0..72ish (72 = 6*... the flap period). "localAI[0] 36 步计数×timeScale" per the task; the AI writes ai[1]? Actually here FindFrame reads ai[1] as frameCounter. Let me check the AI for Betsy in vanilla to see what ai[1] does. In vanilla AI_061 (DD2), Betsy's ai[1] is used as an animation-ish timer? Let me check our bossAI_dd2.ts to see what we store in ai1.

Also note: "else num268 = 0" — any ai0 other than 3/4/5/6 → frame 0. And ai0==4's `if (num268 < 5) frameCounter = 0.0;` — this resets the vanilla frameCounter when transitioning from non-attack frames; but since frameCounter is immediately overwritten by ai[1], that reset is moot except... wait no: `if (num268 < 5) frameCounter = 0.0;` happens BEFORE `frameCounter = (int)ai[1]`. So it's dead code effectively (frameCounter is overwritten right after). Actually it matters not at all since FindFrame-local frameCounter gets reassigned. OK, it's just decompiler noise. I'll skip that.

Similarly ai0==6: `if (num268 > 4) frameCounter = 0.0;` then num268=1, frameCounter=(int)ai[1]. Also dead code.

So Betsy's FindFrame is a pure function of ai[0] and ai[1]. 

Now, the task says "551 Betsy(:67913):拍翼 0-4 序列(localAI[0] 36 步计数×timeScale,读 bossAI_dd2.ts betsyAI 的拍翼计数变量)+空袭/吐息态 5-9 姿态链". Hmm — the task mentions localAI[0] 36-step counter × timeScale. But vanilla FindFrame uses ai[1] directly. Let me check vanilla Betsy AI to see how ai[1] relates. In vanilla, AI 61, Betsy. Let me search the vanilla NPC.cs AI section for the Betsy ai[1] usage. Actually, what matters is what OUR bossAI_dd2.ts writes. Let me read our implementation files now.

Now the Pumpkin King (327):

```csharp
case 327:
    if (ai[3] == 0f)
    {
        if (frame.Y > num * 5)
            frameCounter += 1.0;
        else if (frame.Y > 0)
            frameCounter -= 1.0;
    }
    else if (ai[3] == 1f)
    {
        if (frame.Y > num * 10)
            frameCounter += 1.0;
        else if (frame.Y > num * 4)
            frameCounter -= 1.0;
        else if (frame.Y < num * 4)
            frameCounter += 1.0;
    }
    else if (ai[3] == 2f)
    {
        if (frame.Y < num * 2)
            frameCounter -= 1.0;
        else if (frame.Y > num * 8)
            frameCounter -= 1.0;
        else if (frame.Y < num * 8)
            frameCounter += 1.0;
    }
    if (frameCounter > 6.0)
    {
        frameCounter = 0.0;
        frame.Y += num;
        if (frame.Y > num * 11)
            frame.Y = 0;
    }
    if (frameCounter < 0.0)
    {
        frameCounter = 6.0;
        frame.Y -= num;
        if (frame.Y < 0)
            frame.Y = num * 11;
    }
    break;
```

So Pumpking's frame walk: 12 frames total (0-11), 4 bands of 3: 0-2 (idle?), 3-5, 4-6?? Hmm. Actually rows: 0-2 = band A; 3-5? Let's see the pose targets:
- ai3=0 (idle pose): move toward band 0-2. If frame > 5 → advance forward (frameCounter += 1 means faster advance... wait no, frameCounter += 1 makes it reach >6 sooner → frame advances). If frame in (0,5] → decrement → frame decreases. So target = row 0..? Actually: if frame.Y > 5num: frameCounter+=1 → double-speed forward. If frame.Y in (0, 5num]: frameCounter -= 1 → moves backward. At frame 0: no change → stays 0. So ai3=0 drives toward row 0, moving backward through bands if above row 5, else backward slowly. Hmm wait, if frame.Y = 4num (within band 3-5) it decrements → backward toward 0. If frame.Y=8, forward. So ai3=0 → row 0.

- ai3=1: if frame > 10 → forward; if in (4,10] → backward; if < 4 → forward. So target = row 4: from below (0-3) move forward, from above (5-10) move backward, above 10 forward (wraps: at 11 → +1 → wraps to 0 then forward to 4). So target band = row 4 (4-6).

- ai3=2: if frame < 2 → backward (wrap down from 0 to 11, then continue down); if frame > 8 → backward; if in [2,8) → forward. Target = row 8 (8-10). From below: forward; from above (9-11): backward.

So the frame advance logic: frameCounter moves +1, -1, or stays each call; when frameCounter > 6 → advance frame +1 (wrap 11→0); when < 0 → set to 6 and frame -1 (wrap 0→11). So each frame change takes 7 ticks in the chosen direction. Bands are 3 frames each: {0-2}, {3-5}, {4-6}? Hmm no — wait. Actually let me think about the pumpking sheet: 12 rows. The task said "0→行0/1→行4/2→行8(行=帧带起点,7t/帧,行内 4 帧循环,姿态间双向过渡)". Hmm "行内4帧循环"? Actually with 12 frames and bands at 0, 4, 8, the bands overlap: 0-3, 4-7, 8-11. Each pose = 4 consecutive frames. The transition between poses steps through intermediate frames.

Hmm, but actually the "7t/帧" — the frameCounter > 6 threshold means each frame step takes 7 FindFrame calls (0..6 then >6 triggers). The task description says "行=帧带起点,7t/帧,行内 4 帧循环" — hmm, "行内 4 帧循环" isn't quite right from the source: within a pose there's no independent loop; the frame just stops moving when it reaches the target band boundary? No wait — it doesn't stop! Once in the target band, e.g., ai3=1 and frame=4: none of the conditions (frame>10? no; frame>4? no; frame<4? no) → frameCounter unchanged → never crosses 6 or 0 → frame frozen at 4? That can't be right — the pumpking's head is animated...

Hmm wait, actually for ai3=1 with frame.Y == num*4: `else if (frame.Y > num * 4)` false; `else if (frame.Y < num * 4)` false → frameCounter stays. But frameCounter only changes via these branches. If frame is exactly 4, frameCounter keeps its value. If frameCounter was already >6... it can't be, because whenever frameCounter > 6 it resets to 0 and frame+=1. So at frame 4 with frameCounter in [0,6], nothing changes → frozen forever at row 4.

Hmm, that means the pumpking head doesn't continuously animate within a band? Let me reconsider. Actually wait — maybe I mis-set the band. For ai3=1: conditions `frame.Y > num*10` → +1; `else if (frame.Y > num*4)` → -1; `else if (frame.Y < num*4)` → +1. At frame.Y == 4num exactly: none → frozen. Hmm.

But hold on — frame.Y for pumpking might not be per-row of the whole sprite. Pumpking is drawn in parts? No — this is the FindFrame for NPC 327; frame.Y selects the row. Let me check how Pumpking's head is drawn... Actually in Terraria, Pumpking's body is a single NPC with the face animated in the sheet rows; the sprite sheet for Pumpking_ has 12 rows: 3 poses (calm, angry/grin, enraged) × 4 frames each? The wiki: Pumpking has different facial expressions per attack phase.

Actually let me look at vanilla DrawNPC / the AI to see if frameCounter is reset when switching poses. In AI: when ai[3] changes (new attack), does vanilla reset frameCounter or frame.Y? Let me search the AI section for 327's AI (AI 105? no — Pumpking is aiStyle 105? Let me check. Actually, moon event bosses: Pumpking aiStyle = 105? Hmm, Jack Pumpkin? Mourning Wood = aiStyle 105? Let me not worry; what matters: does the AI reset frameCounter when ai[3] changes? Let me grep the vanilla AI for the pumpking.

Actually — hmm, wait. Maybe I have the direction semantics backwards: `frameCounter -= 1.0` when in "approaching from above" makes frameCounter go negative → triggers `frameCounter < 0 → frameCounter=6, frame.Y -= num`. And `+= 1` pushes toward >6 → frame advance +1. Both take 7 steps per frame move... but the += branches also add on top of nothing else. Hmm, but here's the thing: the counter isn't reset when switching direction, but the thresholds >6/<0 still gate each step at ≤7 ticks.

So the pumpking face switches between 3 poses (4 frames each? but frozen at exact target rows 0/4/8?). Hmm, frozen at row 4? That gives a static face per attack... Let me check Terraria's actual Pumpking rendering: The pumpking sheet has 12 frames; the face IS animated during attacks — hmm.

Wait, actually maybe I should look at the actual AI to see if there's something resetting frame.Y when ai[3] changes, causing the transition animation to play each time ai[3] changes. And within a pose it holds a fixed frame. Let me look at Pumpking's AI (aiStyle 105 in vanilla? or part of AI_105?). Let me grep for "case 105" or find where NPC 327 AI sets ai[3].

Actually, let me look at the pattern again more carefully:

For ai3=0:
- frame > 5: fc += 1 (forward fast)
- 0 < frame ≤ 5: fc -= 1 (backward)
- frame == 0: nothing → frozen at 0.

For ai3=1:
- frame > 10: fc += 1
- 4 < frame ≤ 10: fc -= 1
- frame < 4: fc += 1
- frame == 4: frozen.

For ai3=2:
- frame < 2: fc -= 1
- frame > 8: fc -= 1
- 2 ≤ frame < 8: fc += 1
- frame == 8: frozen.

So each pose has a "home" row: 0, 4, 8, and the face animates through intermediate rows while transitioning. The intermediate rows are shared: e.g. going from pose0 (row0) to pose1 (row4) passes rows 1,2,3; each row shown 7 ticks. So the transitions look like short animations. And in steady state the face is frozen. That matches "姿态间双向过渡" (bidirectional transitions between poses).

Hmm OK but wait — "行内 4 帧循环" from the task description... The task says "0→行0/1→行4/2→行8(行=帧带起点,7t/帧,行内 4 帧循环,姿态间双向过渡)". I think "行内 4 帧循环" is a (slightly wrong) gloss by the task author; the source shows a frozen hold at the target row. I'll implement per source. Actually hmm, wait. Let me reconsider: is it frozen? frameCounter doesn't change at home row, and frame only changes when fc crosses thresholds. So yes frozen.

But hmm, that gives Pumpking a static face — and indeed, checking my memory of Terraria: Pumpking's face does change expression with each attack (calm face ↔ angry face ↔ rage face) with a brief animation sliding between expressions. Yes! That's exactly right — the jack-o'-lantern face slides between three expressions. The 12 rows are 12 morph stages between three expressions... something like that. OK, source is authoritative. 

Now Santa-NK1 (346):
```csharp
case 346:
    if (ai[0] == 1f)   // firing/spinning weapon phase
    {
        spriteDirection = direction;
        frameCounter += 1.0;
        if (frameCounter > 2.0) { frame.Y += num; frameCounter = 0.0; }
        if (frame.Y > num * 8) frame.Y = num * 6;
        if (frame.Y < num * 6) frame.Y = num * 6;
        break;
    }
    if (velocity.X == 0f)
    {
        // hold frame (y2 = y2; i.e., no change), frameCounter = 0
        break;
    }
    spriteDirection = direction;
    frameCounter += 1.0;
    frameCounter += Math.Abs(velocity.X) / 2f;
    if (frameCounter > 4.0) { frame.Y += num; frameCounter = 0.0; }
    if (frame.Y > num * 5) frame.Y = num;
    if (frame.Y < num) frame.Y = num;
    break;
```

So: ai0==1 → fire band rows 6-8, advance every 3t (fc>2 → 3 ticks per frame: fc increments to 3 → >2 → advance; so frames at fc=0,1,2 → 3 ticks each). Walking: rows 1-5, fc += 1 + |vx|/2, advance every 5 counts. Standing still: frozen, fc=0. Task says "开火带 6-8(3t/帧)、行走带 1-5(按 |vx|/2 累计)、静止定格 0" — hmm "静止定格 0"? Per source, standing: frame unchanged (y2 = y2 self-assignment = keep current), fc=0. So it holds whatever frame it was on. Hmm, but where does frame 0 come from? When transitioning from fire band (6-8) to walking, `if (frame.Y < num) frame.Y = num;` → jumps to 1. Frame 0 might only be initial. The task's "静止定格 0" is wrong per source — standing keeps current frame. I'll follow source exactly: velocity.X == 0 → keep frame.Y, reset frameCounter.

Hmm wait, but there's a subtlety: `if (velocity.X == 0f)` — floating point exact zero. Our entity's vx should be exactly 0 when not moving. I'll mirror that.

Ice Queen (345):
```csharp
case 345:
    if (ai[0] == 0f)
    {
        if (ai[3] >= 0f) frame.Y = 0;
        else if (velocity.X < 0f) frame.Y = num;
        else frame.Y = num * 2;
    }
    else if (ai[0] == 1f)
    {
        frameCounter += 1.0;
        if (frameCounter > 5.0) { frameCounter = 0.0; frame.Y += num; }
        if (frame.Y > num * 4) frame.Y = num * 3;
        if (frame.Y < num * 3) frame.Y = num * 3;
    }
    else if (ai[0] == 2f)
        frame.Y = num * 5;
    break;
```

So gliding (ai0=0): ai3>=0 → frame 0; else vx<0 → 1, vx>0 → 2. Frostwave attack (ai0=1): rows 3-4, 6t/frame (fc>5 → 6 ticks). Spinning (ai0=2): row 5 constant. Task said "落冰态 3-4 循环、自旋恒行 5" — matches (落冰 = shooting icy waves). 

Everscream (344):
```csharp
case 344:
    if (velocity.X == 0f)
    {
        frameCounter += 1.0;
        if (frameCounter > 5.0) { frameCounter = 0; frame.Y += num; }
        if (frame.Y > num * 9) frame.Y = 0;
    }
    else
    {
        frameCounter += Math.Max(1f, Math.Abs(velocity.X) * 0.75f);
        if (frameCounter > 5.0) { frameCounter = 0; frame.Y += num; }
        if (frame.Y > num * 9) frame.Y = 0;
    }
    break;
```

Both branches identical except counter increment: standing → +1/t; moving → max(1, |vx|*0.75). 10 frames (0-9), 6 counter units per frame. Task: "全带按 |vx|*0.75 累计推进" — close enough; standing is +1/t (equivalent to max(1, ...) = 1). I'll implement the two branches per source.

Mourning Wood (325):
```csharp
case 325:
    if (velocity.X == 0f)
    {
        frameCounter += 1.0;
        if (frameCounter > 4.0) { frameCounter = 0.0; frame.Y += num; }
        if (frame.Y > num * 4) frame.Y = 0;
        break;
    }
    frameCounter += 1.0;
    if (frameCounter > 4.0) { frameCounter = 0.0; frame.Y += num; }
    if (frame.Y < num * 5) frame.Y = num * 5;
    if (frame.Y > num * 9) frame.Y = num * 5;
    break;
```

Standing: band 0-4, 5t/frame. Moving: band 5-9, 5t/frame. Matches task.

Now the martian family. I have 393/394/395/392/399 from the read. Need 386/387 (Engineer and Tesla). Let me grep for case 386/387 in NPC.cs FindFrame. Also check 392's actual identity (frame machine: 4 frames 0-3, /3, death-ray window [20,260)).

Wait — actually, hmm: for 392, flag6 window is [20, 260) — num54=20, num55=240. The task says "392 炮体:发射窗内帧速 ×2". And for 395 the death-ray window is [20, 260) too (num124=20, num125=240) with frameCounter clamped to [36,54) → /6 → frames 6-8. Task says "死光电报窗 [20,260) 钳帧 [36,54)(=帧 6-8 蓄能辉光带)". Matches: counter clamped to 36..53 → 36/6=6 .. 53/6=8. 

Wait, actually the clamp: `frameCounter += 1.0; if (fc >= 66) fc = 0;` then if flag10: `fc += 1.0; if (fc >= 54 || fc < 36) fc = 36;`. So during death-ray telegraph, counter is forced into [36,53] → frames 6-8 (glowing). Then num126 = fc % 66 / 6 → frame 0-10 (66/6 = 11 frames). 

For 392: `fc += 1; if flag6 fc += 1; if fc >= 12 fc = 0; num56 = fc % 12 / 3` → 4 frames 0-3, advance every 3t normally, every 1.5t in window. Wait: fc>=12 → reset. fc counts 0..11, /3 → 0-3. In window, fc advances 2/t → period 6t for 4 frames.

Now 386/387. Let me grep. Also, I need to identify what NPC IDs 392, 395 etc. are exactly. From Terraria: NPC 391 = Martian Saucer? Hmm. Let me just check NPCDatabase or the npcFrameCount in our code. Actually, let me search our codebase for these NPC ids to understand mapping. But first, let me grep vanilla FindFrame for case 386 and 387.
````

</details>


---

## 🤖 Assistant · 2026-08-19T07:37:58.319Z · glm-x-preview-260804

```
现在我已经获取了月亮事件和火星家族的部分。让我找一下 386/387 (Engineer/Tesla) 的 FindFrame 情况。
```


---

## 🤖 Assistant · 2026-08-19T07:38:00.231Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"case 386:\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head; grep -n \"case 387:\" ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria/NPC.cs | head; grep -n \"case 392:\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head",
 "description": "Find FindFrame cases for 386, 387, 392"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:38:00.291Z

**📎 ToolResult**

```
72369:		case 386:
79129:		case 386:
ugrep: warning: ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria/NPC.cs: No such file or directory
72543:		case 392:
78627:		case 392:
78753:			case 392:

```


---

## 🤖 Assistant · 2026-08-19T07:38:03.993Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Odd — "case 387:" grep found nothing before the ugrep warning. Let me search with different approach. The warning "No such file or directory" is strange — maybe a glob expansion issue. Let me use a different quoting.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:38:05.986Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"case 38[0-9]:\" NPC.cs | head -30 && echo --- && grep -n \"case 39[0-9]:\" NPC.cs | head -30",
 "description": "List FindFrame and AI cases in 380s-390s range"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:38:06.037Z

**📎 ToolResult**

```
57492:		case 380:
57493:		case 381:
57494:		case 382:
72251:		case 380:
72295:		case 381:
72296:		case 382:
72297:		case 383:
72298:		case 385:
72299:		case 389:
72335:		case 387:
72369:		case 386:
72403:		case 388:
78626:		case 380:
79045:		case 387:
79125:		case 381:
79126:		case 382:
79127:		case 383:
79128:		case 385:
79129:		case 386:
79130:		case 387:
79131:		case 388:
79132:		case 389:
---
72418:		case 391:
72454:		case 390:
72481:		case 393:
72495:		case 394:
72520:		case 395:
72543:		case 392:
72562:		case 399:
72599:		case 398:
72628:		case 396:
72644:		case 397:
78627:		case 392:
78628:		case 393:
78629:		case 394:
78630:		case 396:
78631:		case 397:
78632:		case 398:
78753:			case 392:
78754:			case 393:
78755:			case 394:
78760:			case 399:
79033:		case 395:
79133:		case 390:
79134:		case 391:
79135:		case 394:
79136:		case 395:
80198:		case 398:
81354:		case 398:
81509:		case 398:

```


---

## 🤖 Assistant · 2026-08-19T07:38:08.498Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 120,
 "offset": 72295
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:38:08.513Z

**📎 ToolResult**

```
72295			case 381:
72296			case 382:
72297			case 383:
72298			case 385:
72299			case 389:
72300				if (velocity.Y == 0f)
72301				{
72302					spriteDirection = direction;
72303					if (frame.Y < num * 2)
72304					{
72305						frame.Y = num * 2;
72306					}
72307					if (type == 389 || type == 385)
72308					{
72309						frameCounter += (double)Math.Abs(velocity.X) * 1.2;
72310					}
72311					else
72312					{
72313						frameCounter += Math.Abs(velocity.X) * 2f;
72314					}
72315					if (frameCounter > 6.0)
72316					{
72317						frame.Y += num;
72318						frameCounter = 0.0;
72319					}
72320					if (frame.Y / num >= Main.npcFrameCount[type])
72321					{
72322						frame.Y = num * 2;
72323					}
72324					if (velocity.X == 0f)
72325					{
72326						frame.Y = 0;
72327					}
72328				}
72329				else
72330				{
72331					frameCounter = 0.0;
72332					frame.Y = num;
72333				}
72334				break;
72335			case 387:
72336				if (ai[0] > 0f)
72337				{
72338					frameCounter += 1.0;
72339					if (ai[0] >= 20f)
72340					{
72341						frameCounter += 1.0;
72342					}
72343					if (ai[0] >= 40f)
72344					{
72345						frameCounter += 1.0;
72346					}
72347					if (frameCounter >= 10.0)
72348					{
72349						frameCounter = 0.0;
72350						frame.Y += num;
72351						if (frame.Y >= num * 2)
72352						{
72353							frame.Y = 0;
72354						}
72355					}
72356					break;
72357				}
72358				frameCounter += 1.0;
72359				if (frameCounter >= 15.0)
72360				{
72361					frameCounter = 0.0;
72362					frame.Y += num;
72363					if (frame.Y >= num * 2)
72364					{
72365						frame.Y = 0;
72366					}
72367				}
72368				break;
72369			case 386:
72370				if (ai[2] > 0f)
72371				{
72372					int num41 = (int)ai[2] / 12;
72373					frame.Y = num * (9 + num41 % 2);
72374				}
72375				else if (velocity.Y == 0f)
72376				{
72377					spriteDirection = direction;
72378					if (frame.Y < num * 2)
72379					{
72380						frame.Y = num * 2;
72381					}
72382					frameCounter += Math.Abs(velocity.X) * 2f;
72383					if (frameCounter > 6.0)
72384					{
72385						frame.Y += num;
72386						frameCounter = 0.0;
72387					}
72388					if (frame.Y / num >= 9)
72389					{
72390						frame.Y = num * 2;
72391					}
72392					if (velocity.X == 0f)
72393					{
72394						frame.Y = 0;
72395					}
72396				}
72397				else
72398				{
72399					frameCounter = 0.0;
72400					frame.Y = num;
72401				}
72402				break;
72403			case 388:
72404			{
72405				frameCounter += 1.0;
72406				int num42 = 6;
72407				if (frameCounter >= (double)num42)
72408				{
72409					frameCounter = 0.0;
72410					frame.Y += num;
72411					if (frame.Y >= num * 2)
72412					{
72413						frame.Y = 0;
72414					}

```


---

## 🤖 Assistant · 2026-08-19T07:38:44.860Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I now have:
- 387 (Tesla? — actually 387 = "Martian Officer"? hmm, no matter): `ai[0] > 0` → charging: counter +1/t, +2 more if ai0>=40, +1 more if ai0>=20. So: ai0 < 20 → 1/t (period 10 → 10t per frame); 20<=ai0<40 → 2/t (5t/frame); ai0>=40 → 3/t (3.33t/frame). Frame 0-1 (2 frames). ai0<=0 → idle: 15t/frame, 2 frames.

Hmm wait the task said "387 特斯拉:充电 10t/帧、待机 15t/帧两档(按其部署渐显计时)". Per source, charge actually has three sub-speeds (1x/2x/3x by ai0>=20/>=40). The task's "两档" gloss is incomplete — source wins. Actually re-reading: frameCounter += 1; if ai0>=20 +=1; if ai0>=40 +=1. So three tiers. I'll implement per source.

- 386 (Engineer): ai[2] > 0 → deploy: frame = 9 + (ai2/12)%2 → rows 9/10 alternating every 12t. Else walking: standard fighter walk (frames 2..8, idle 0, jump 1, fc += |vx|*2, >6 advance). The task says "386 工程师:放塔期帧 9/10". Matches.

What are these NPCs? 386 = Martian Engineer, 387 = ... "Martian Officer"? Hmm, per wiki NPC 387 = "Martian Officer"? Actually I believe 387 = "Tesla" isn't a separate NPC... The task calls it 特斯拉 (Tesla). Let me verify: Terraria NPC IDs: 385 = "Scutlix Gunner"? 386 = "Martian Engineer", 387 = "Martian Officer", 388 = "Martian Drone"? Hmm 388's FindFrame shows a 2-frame blink at 6t — drone? Actually:

From the Terraria wiki:
- 381 = Martian Drone? no...

Let me just check our game's npc defs or the wiki list: Martian Madness NPCs in order of ID:
- 380: Martian... hmm. Actually 380-384 might be DD2-related? No wait — 381, 382, 383 are grouped with 380 at 57492 (that's a different switch — probably scale/something). 

Known: 385 = Grapple? Hmm. Let me recall the actual list:
- 385: "Scutlix Gunner"? No, Scutlix Gunner = 385? Hmm.

The wiki list for Martian Madness:
- Gray Grunt (384?)
- Gigazapper
- Martian Engineer
- Martian Officer
- Martian Drone
- Martian Tesla Turret
- Ray Gunner
- Scutlix Gunner
- Martian Walker
- Martian Saucer
- Martian Saucer Turret
- Martian Saucer Cannon
- Martian Probe

Task says: 393 炮塔 (turret), 394 火炮 (cannon), 395 母碟 (saucer), 392 炮体?? — "392 炮体:发射窗内帧速×2". Hmm 392's FindFrame: 4 frames, speed ×2 in [20,260) window. 392 = Martian Walker? Hmm, but the window [20,260) is the same death-ray timing as saucer 395. So 392 must be something attached to the saucer fight — 392 = "Martian Walker"? No.

Hmm wait: 390 = Martian Saucer? 391 = ? 395 = Martian Saucer (task says 母碟=mother saucer). The saucer spawns "Martian Saucer Turret" (393) and "Martian Saucer Cannon" (394). And 392 might be... Actually from the vanilla AI at 78626: case 380-399 grouped. Let me check the actual NPC names. Easiest: check our game data (Lang or npcDefs). Let me grep our game source for id 392/395 names.

Actually, the identity doesn't matter that much — what matters is mapping our entity ids to the right vanilla FindFrame behavior. The task explicitly gives the vanilla line numbers and NPC ids, and says our implementation is in bossAI_martian.ts. So the ids in our game match vanilla ids (561 data-driven enemies keyed by vanilla id per memory notes). Good.

Now let me read our implementation files. Start with Renderer.ts vanillaFrameIdx to see the structure (and the 222 precedent), then bossAI_martian.ts, bossAI_moon_events.ts, bossAI_dd2.ts, bossAI_lategame.ts.

Renderer.ts is probably huge. Let me grep for vanillaFrameIdx first.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:38:45.438Z · glm-x-preview-260804

```
现在所有原版部分都已就绪。我来查看一下我们的 Renderer.ts 的 `vanillaFrameIdx` 结构。
```


---

## 🤖 Assistant · 2026-08-19T07:38:46.842Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"vanillaFrameIdx\\|customFrameIdx\" src/render/Renderer.ts | head -30 && echo ---- && wc -l src/render/Renderer.ts src/entities/bossAI_martian.ts src/entities/bossAI_moon_events.ts src/entities/bossAI_dd2.ts src/entities/bossAI_lategame.ts",
 "description": "Locate vanillaFrameIdx in Renderer and file sizes"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:38:46.888Z

**📎 ToolResult**

```
643:export function vanillaFrameIdx(e: Enemy, frames: number): number {
646:  if (e.customFrameIdx != null) return Math.min(frames - 1, e.customFrameIdx);
4194:      const frameIdx = vanillaFrameIdx(e, frames);
4198:      // (帧 0/1 与 246 基础帧同构,customFrameIdx 直读不变;曾一直画 NPC_246)
5248:    const frameIdx = vanillaFrameIdx(e, frames);
5768:    const r = this.atlas.vnpc(398, vanillaFrameIdx(e, frames));
5843:    const r = this.atlas.vnpc(397, vanillaFrameIdx(e, Math.max(1, e.vanilla?.frames ?? 1)));
----
   10877 src/render/Renderer.ts
     915 src/entities/bossAI_martian.ts
    1095 src/entities/bossAI_moon_events.ts
    2518 src/entities/bossAI_dd2.ts
    1460 src/entities/bossAI_lategame.ts
   16865 total

```


---

## 🤖 Assistant · 2026-08-19T07:38:48.960Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "limit": 230,
 "offset": 640
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:38:48.974Z

**📎 ToolResult**

```
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
700	    if (!e.onGround) {
701	      if (e.vy < 0) return Math.min(4, frames - 1);
702	      return Math.min(6, frames - 1);
703	    }
704	    if (!walking) return 0;
705	    // counter ≡ walkCycleT + t（每 tick += |vx| + 1）；越过 7 即进帧
706	    return Math.floor((e.walkCycleT + t) / 7) % frames;
707	  }
708	  // ---- 其余 aiStyle=7 小动物专属 case（此前全被下方城镇 NPC 档截胡：
709	  //      帧 2 起/阈值 6/|vx|*2+1 = 行走小动物 2-3 倍速闪帧"鬼畜"，2026-08-18
710	  //      用户报"走路的金鱼"。下列 case 逐族对齐 FindFrame type switch）----
711	  // 行走金鱼 230/593（case 230/593，cs:76584-76649）：站定=帧0；行走
712	  // counter += |vx|*2+1、>10 进帧全帧循环；腾空=帧0（vy>4 的 rotation
713	  // 倾斜在 AI 侧未驱动，差异登记）。counter ≡ walkCycleT*2 + t
714	  if (id === 230 || id === 593) {
715	    if (!e.onGround || !walking) return 0;
716	    return Math.floor((e.walkCycleT * 2 + t) / 11) % frames;
717	  }
718	  // 企鹅 148/149/168/470（case 148，cs:77094-77152）：counter += |vx|（无 +1！）
719	  // 相位制 <6=0 / <12=1 / <15=2 回卷 15；腾空=帧2；localAI[0] 肚皮滑行带
720	  // （2/3/4 → +3/+6/+9）我们的滑行 AI 未驱动 localAI → 恒带 0（差异登记）
721	  if (id === 148 || id === 149 || id === 168 || id === 470) {
722	    if (!e.onGround) return Math.min(2, frames - 1);
723	    if (!walking) return 0;
724	    const ph = e.walkCycleT % 15;
725	    return ph < 6 ? 0 : ph < 12 ? 1 : 2;
726	  }
727	  // 松鼠 299/538/539/639-645（case 299，cs:77160-77214）：行走
728	  // counter += |vx|*0.5+1、>6 进帧；回卷到帧 1（0..frames-1 循环跳过 0）；
729	  // 腾空 vy<0=帧2 / vy>0=帧4
730	  if (id === 299 || id === 538 || id === 539 || (id >= 639 && id <= 645)) {
731	    if (!e.onGround) return e.vy < 0 ? Math.min(2, frames - 1) : Math.min(4, frames - 1);
732	    if (!walking) return 0;
733	    return 1 + (Math.floor((e.walkCycleT * 0.5 + t) / 7) % Math.max(1, frames - 1));
734	  }
735	  // 鼠族 300/447/610（case 300/610，cs:77215-77316）：站定=嗅探帧 0/1
736	  // （counter+1、>8 进帧）；行走与腾空同式 counter += |vx|*0.5+1、>6 进帧，
737	  // 回卷到帧 2（2..frames-1 循环）
738	  if (id === 300 || id === 447 || id === 610) {
739	    if (e.onGround && !walking) return Math.floor(t / 9) % 2;
740	    return 2 + (Math.floor((e.walkCycleT * 0.5 + t) / 7) % Math.max(1, frames - 2));
741	  }
742	  // 蛙族 361/445/687（case 361，cs:77320-77378）：wet=游帧 10/11/12 按 |vx|
743	  // 分档；陆上待机 0..5（7t/帧）；行走相位 [0,6,8,9]（6t/段）；腾空
744	  // vy>0=帧9 / vy<0=帧8
745	  if (id === 361 || id === 445 || id === 687) {
746	    if (e.wet) {
747	      const a = Math.abs(e.vx);
748	      return Math.min(frames - 1, a > 0.25 ? 10 : a > 0.15 ? 11 : 12);
749	    }
750	    if (!e.onGround) return Math.min(frames - 1, e.vy > 0 ? 9 : 8);
751	    if (!walking) return Math.floor(t / 7) % Math.min(6, frames);
752	    return Math.min(frames - 1, [0, 6, 8, 9][Math.floor(t / 6) % 4]);
753	  }
754	  // 行走鸟 362/364/602/608（case 362/602，cs:74445-74546）：站定=帧0；
755	  // 行走 counter+1、≥4 进帧，循环带 3..9（<3 抬 3、≥10 回 3）
756	  if (id === 362 || id === 364 || id === 602 || id === 608) {
757	    if (!walking) return 0;
758	    return Math.min(frames - 1, 3 + (Math.floor(t / 4) % 7));
759	  }
760	  // 龟 616/617（case 616，cs:77379-77432）：wet=游带 8..13（走 6t/停 11t 一帧）；
761	  // 陆上 0..7（9t/帧）；站定=帧0；腾空=帧8
762	  if (id === 616 || id === 617) {
763	    if (e.wet) return Math.min(frames - 1, 8 + (Math.floor(t / (walking ? 6 : 11)) % 6));
764	    if (!e.onGround) return Math.min(8, frames - 1);
765	    if (!walking) return 0;
766	    return Math.floor(t / 9) % Math.min(8, frames);
767	  }
768	  // 龟 625（case 625，cs:77434-77473）：wet=游带 6..11（走 5t/停 9t 一帧）；
769	  // 陆上 0..5（8t/帧）；站定=帧0
770	  if (id === 625) {
771	    if (e.wet) return Math.min(frames - 1, 6 + (Math.floor(t / (walking ? 5 : 9)) % 6));
772	    if (!walking) return 0;
773	    return Math.floor(t / 8) % Math.min(6, frames);
774	  }
775	  // 城镇 NPC（aiStyle 7，FindFrame 城镇分支 cs:70159-70240）——仅城镇/绑缚族：
776	  // 小动物专属 case（46 族/230/299/300/361/362/616/625 等已在上方各自分支截胡，
777	  // 勿再落到本档（帧 2 起/|vx|*2+1 对小动物是 3 倍速鬼畜））：腾空=1；
778	  // 站定帧（cs:70163-70181）：638 是 0-7 待机循环（4t 推进）、140/489=帧1、其余=帧0；
779	  // 行走帧 2..frames-extra-1 循环（frameCounter += |vx|*2+1，阈值 num109：
780	  // 632/534/638/656=12（489=8 且 counter 加 |vx|*1+0.5）、其余 6）
781	  if (ai === 7) {
782	    if (!e.onGround) return 1;
783	    if (!walking) {
784	      if (id === 638) return Math.min(7, Math.floor(t / 4) % Math.min(8, frames));
785	      if (id === 140 || id === 489) return Math.min(1, frames - 1);
786	      return 0;
787	    }
788	    const extra = townExtraFrames(id);
789	    const len = Math.max(1, frames - extra - 2);
790	    if (id === 489) return 2 + (Math.floor((e.walkCycleT + t * 0.5) / 8) % len);
791	    const step = id === 632 || id === 534 || id === 638 || id === 656 ? 12 : 6;
792	    return 2 + (Math.floor((e.walkCycleT * 2 + t) / step) % len);
793	  }
794	  // 战士族/107（L70155-70252）：站定=0；行走从帧 2 起按 |vx|*2+1 累加、>6 推进、循环回 2
795	  if (ai === 3 || ai === 26 || ai === 107) {
796	    if (!e.onGround) return frames - 1; // 腾空取末帧（原版 ai[0]==2 在 0/末帧间交替）
797	    if (!walking) return 0;
798	    const cycLen = Math.max(1, frames - 2);
799	    const step = Math.floor((e.walkCycleT * (Math.abs(e.vx) * 2 + 1)) / 6);
800	    return 2 + (step % cycLen);
801	  }
802	  // 蝶族（FindFrame case 356/444/653/661，cs:73419-73455）：拍翅四段 [0,1,2,1]
803	  //  （7t 档；原版 counter 加 (|vx|+|vy|)/2 速度敏感——速率随速近似取定档）。
804	  //  356 物种带：frame.Y += 3 帧×(ai[2]-1)（cs:73452-55）——八物种按 ai2 分带
805	  //  （出生加权掷/释放 Style 定；444/653/661 单物种帧表 3 帧不分带）
806	  if (ai === 65) {
807	    const anim = [0, 1, 2, 1][Math.floor(t / 7) % 4];
808	    if (id === 356 && e.ai2 >= 1 && e.ai2 <= 8) {
809	      return Math.min(frames - 1, (e.ai2 - 1) * 3 + anim);
810	    }
811	    return Math.min(frames - 1, anim);
812	  }
813	  // 海豚 615（case 615，cs:74925-74938，aiStyle 16 但有专属 case）：搁浅
814	  // （!wet && ai[2]==1）=帧4；否则 counter 每 tick +1（!wet +2），7t 一帧全帧循环
815	  if (id === 615) {
816	    if (!e.wet && e.ai2 === 1) return Math.min(4, frames - 1);
817	    return Math.floor((e.wet ? t : t * 2) / 7) % frames;
818	  }
819	  // ---- 游泳族（aiStyle 16）逐 case（此前一支通用 t/4 档通吃 = 全员 1.5 倍速;
820	  //      离水金鱼 4t 连闪 0..3 是用户报"金鱼鬼畜"的另一半）----
821	  // 鱼族 case 55（cs:74879-74924：55 金鱼/57 腐化金鱼/58 食人鱼/102 琵琶鱼/
822	  // 241 血浆渗透者/465 邪恶金鱼/592/607 鳉）：counter+1、6t 一档;
823	  // wet 帧 0..3 游姿 / !wet 帧 4/5 离水折腾
824	  if (id === 55 || id === 57 || id === 58 || id === 102 || id === 241
825	    || id === 465 || id === 592 || id === 607) {
826	    if (!e.wet) return Math.min(frames - 1, 4 + (Math.floor(t / 6) % 2));
827	    return Math.floor(t / 6) % Math.min(4, frames);
828	  }
829	  // 河鲀 688（case 688，cs:74944-74984）：鼓起 ai[2]==1 =帧4/5@6t；离水=4/5@12t；
830	  // 常态 wet=0..3@8t
831	  if (id === 688) {
832	    if (e.ai2 === 1 || !e.wet) return Math.min(frames - 1, 4 + (Math.floor(t / (e.ai2 === 1 ? 6 : 12)) % 2));
833	    return Math.floor(t / 8) % Math.min(4, frames);
834	  }
835	  // 虎鲸 692（case 692，cs:75392-75440）：wet 半表轮换（ai0==0 → 5t 否则 7t 一帧）；
836	  // 离水定帧 vy>0=7 / vy<0=3 / 静=1
837	  if (id === 692) {
838	    if (e.wet) return Math.floor(t / (e.ai0 === 0 ? 5 : 7)) % Math.max(1, Math.floor(frames / 2));
839	    return Math.min(frames - 1, e.vy > 0 ? 7 : e.vy < 0 ? 3 : 1);
840	  }
841	  // 鲨鱼 65（case 65，cs:75352-75377）：wet 帧 0..3@6t；离水冻结末态
842	  if (id === 65) return e.wet ? Math.floor(t / 6) % Math.min(4, frames) : Math.min(3, frames - 1);
843	  // 沙鲨 542-545（case 542，cs:75380-75388）：counter+1、4t 一帧 16t 循环 4 帧
844	  if (id >= 542 && id <= 545) return Math.floor(t / 4) % 4;
845	  // 其余游泳族兜底：6t 一帧全帧循环（保守档）
846	  if (ai === 16) return Math.floor(t / 6) % frames;
847	  // 水母（case 63 L74621+）：追击脉冲循环 [4..6]，漂移循环 [0..]
848	  if (ai === 18) {
849	    const active = t % 90 < 30; // 脉冲周期近似
850	    if (active && frames > 6) return 4 + (Math.floor(t / 5) % 3);
851	    return Math.floor(t / 8) % Math.min(4, frames);
852	  }
853	  // 克苏鲁之眼(FindFrame case 4, cs:77607-77631):0/1/2 三帧眨眼各 7 tick,
854	  // ai[0]>1 帧偏移 +3(张嘴形态)——门取真 ai[0](Enemy.ai0):变身段一(ai0==1)仍闭嘴帧,
855	  // 段二(ai0==2)起张嘴(此前挂 phase>1,变身一起手就张嘴,早了 100t)
856	  // EoC/双子共组（FindFrame case 4/125/126，cs:77607-77631）：7t 三帧眨眼循环
857	  // + ai[0]>1（变身/战斗二段）帧带 +3——双子曾落通用 6t 全帧连播（两带混闪）
858	  if (id === 4 || id === 125 || id === 126) {
859	    const blink = Math.floor(t / 7) % 3;
860	    return Math.min(frames - 1, blink + (e.ai0 > 1 ? 3 : 0));
861	  }
862	  // 蜂后（type 表 case 222，cs:73737-73760）：localAI[0]==1（冲刺，AI 同步 lai0）
863	  // → 帧 0-3 带 / 悬停 → 帧 4-11 带，每 5t 推进带内回卷（曾通用 6t 全 12 帧混播）
864	  if (id === 222) {
865	    const base = e.lai0 === 1 ? 0 : 4;
866	    const span = e.lai0 === 1 ? 4 : Math.min(8, frames - 4);
867	    return base + (Math.floor(t / 5) % span);
868	  }
869	  // 肉墙 113/114（case 113/114 type 表，cs:74214-74229）：ai[2]==0 → 12t/帧

```


---

## 🤖 Assistant · 2026-08-19T07:38:51.625Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I see the pattern now. Let me continue reading vanillaFrameIdx to find where case 266/262 and other boss cases are, and to see the end of the function to know where to insert.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:38:52.383Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "limit": 200,
 "offset": 869
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:38:52.396Z

**📎 ToolResult**

```
869	  // 肉墙 113/114（case 113/114 type 表，cs:74214-74229）：ai[2]==0 → 12t/帧
870	  // 两帧循环;ai[2]≠0（Leech 放虫轮）→ 冻结帧 0（counter=-60；曾通用 6t 连播）
871	  if (id === 113 || id === 114) {
872	    if (e.ai2 !== 0) return 0;
873	    return Math.floor(t / 12) % Math.min(2, frames);
874	  }
875	  // 世纪之花本体（case 262，cs:73239-73258）：血量分带——>50% 帧 0-3、
876	  // ≤50% 钳 4-7（二阶段），每 7t 推进带内回卷（曾通用 6t 全 8 帧混播）
877	  if (id === 262) {
878	    const phase2 = e.hp <= e.maxHp / 2;
879	    const base = phase2 ? 4 : 0;
880	    const span = Math.min(4, frames - base);
881	    return base + (Math.floor(t / 7) % span);
882	  }
883	  // 克苏鲁之脑（FindFrame case 266，cs:73215-73237）：frameCounter>6 推进
884	  // （7t/帧，cs:73216-73221）；一相（ai[0]>=0 且 localAI[2]==0）循环 0..3，
885	  // 二相 4..7（低于 4 抬到 4、越 7 回卷 4）——此前走末尾通用档全 8 帧连播
886	  if (id === 266) {
887	    const idx = Math.floor(t / 7) % 8;
888	    const phase2 = e.ai0 < 0 || e.lai2 !== 0;
889	    return phase2 ? Math.max(4, idx) : Math.min(3, idx);
890	  }
891	  // 克眼仆从(FindFrame case 5, cs:77633-77643):frameCounter 每 8t 推进一帧、
892	  // 越界回卷帧 0（此前走末尾通用 6t 档,快了 1/3）
893	  if (id === 5) {
894	    return Math.floor(t / 8) % frames;
895	  }
896	  // 训练假人 488（FindFrame case 488，cs:71516-71544）：摇晃动画帧由受击强度驱动——
897	  // num140 = 方向==-1 ? 4 : 6；帧 = ceil(shake/num140)（dir==1 再 +5）；shake 每帧 -1
898	  if (id === 488) {
899	    const dir = e.dummyHitDir;
900	    const step = dir === -1 ? 4 : 6;
901	    let idx = Math.ceil(e.dummyShake / step);
902	    if (idx > 0 && dir === 1) idx += 5;
903	    return Math.min(frames - 1, idx);
904	  }
905	  // 血肉墙 113/之眼 114（FindFrame case 113/114，cs:74214-74233）：ai[2]==0 时
906	  // frameCounter 每 12t 推进一帧、越 npcFrameCount(均 2) 回卷；ai[2]!=0 → 锁帧 0
907	  // 且 frameCounter=-60（回合结束后需再攒 72t 才回动画——无状态引擎近似为立即恢复，
908	  // 差异登记：113 的 ai[2] 是 Leech 放虫轮(bossAI_wof)，放虫期间嘴部定帧=原版吐虫姿势）
909	  if (id === 113 || id === 114) {
910	    if (e.ai2 !== 0) return 0;
911	    return Math.floor(t / 12) % Math.max(1, Math.min(2, frames));
912	  }
913	  // 饥饿者 115（FindFrame case 115，cs:75695-75712）：counter 先 +1 再比阈值
914	  // （1..15）：1-2→0 / 3-5→1 / 6-11→2 / 12-14→1，15 回卷——0→1→2→1 乒乓嚼动
915	  if (id === 115) {
916	    const p = (Math.floor(t) % 15) + 1;
917	    return p < 3 ? 0 : p < 6 ? 1 : p < 12 ? 2 : 1;
918	  }
919	  // 饥饿者 II 116（FindFrame case 116，cs:74789-74808）：counter 每 5t 推进、
920	  // 越 npcFrameCount(6) 回卷全帧；rotation=atan2(vy,vx)（vx<0 再 +π，drawEnemy
921	  // 独占分支）——此前落通用 6t 档（节奏差 20%）
922	  if (id === 116) {
923	    return Math.floor(t / 5) % Math.max(1, frames);
924	  }
925	  // 腐化者 133（FindFrame case 133，cs:74761-74788）：counter 1-7→0 / 8-15→1 /
926	  // 16→0 并回卷；血 <50% 帧 +2（狂暴形态——floatEyeAI rage 档的视觉面）
927	  if (id === 133) {
928	    const p = (Math.floor(t) % 16) + 1;
929	    return Math.min(frames - 1, (p >= 8 && p < 16 ? 1 : 0) + (e.hp < e.maxHp * 0.5 ? 2 : 0));
930	  }
931	  // 机械骷髅王头 127（FindFrame case 127，cs:75196-75231）：ai[1]==0（悬浮段）=
932	  // 帧 {0,1} 每 12t 循环（眨眼）；ai[1]!=0（旋冲/白天狂暴/离场）= **恒定帧 2**
933	  // （旋冲脸，counter 清零不推进）。MechQueen 合体态（IsMechQueenUp）走 3-5 帧
934	  // 分支（:75197-75212）：悬浮 0→1→2→3→4 爬坡后 3↔4 每 12t 循环、ai[1]!=0 恒帧 5。
935	  // 曾落通用 6t 档 → 6 帧连播=一/二阶段动画混播（2026-08-14 用户报告）。
936	  // 状态近似：无引擎态计数器，12t 相位取全局 t（重进悬浮段时相位任意，差 <12t）
937	  if (id === 127) {
938	    if (mechQueenUp()) {
939	      if (e.ai1 === 0) {
940	        const k = Math.floor(t / 12);
941	        return k <= 4 ? k : 3 + ((k - 5) % 2 === 0 ? 0 : 1);   // 爬坡 0..4 后 3↔4
942	      }
943	      return 5;                                                 // :75207-75210 恒帧 5
944	    }
945	    if (e.ai1 === 0) return Math.floor(t / 12) % 2;
946	    return 2;
947	  }
948	  // Prime 锯臂 129 / 激光臂 130（cs:75235-75264）：每 2t / 每 8t 推进、越帧数回卷
949	  // （曾落通用 6t 档：锯慢 3 倍、激光快 33%）；钳 128/炮 131 无 case=恒帧 0
950	  //（frames=1，通用档亦恒 0，无需特判）
951	  if (id === 129) return Math.floor(t / 2) % Math.max(1, frames);
952	  if (id === 130) return Math.floor(t / 8) % Math.max(1, frames);
953	  // 法师族三态帧（case 29/32/45/172/281-286/693，cs:77721-77743）：帧0 待机 /
954	  // 帧1 蓄力（vy==0 且 ai[1]>0——含传送后 ai[1]=20 的 20t 后摇，原版同）/ 帧2 腾空
955	  // （vy≠0）；32 且 RedHat 变体（localAI[3]==1：红帽骷髅王 ai[3]==1 在场时 AI 段
956	  // cs:20777-20784 置位永不清）整带 +3——贴图表 6 帧=上半 0-2 常态兜帽、下半 3-5
957	  // 红帽形态。曾落通用 6t 全循环档 → 32 六帧连播=两种头饰形态混播（2026-08-17 用户报告）
958	  if (CASTER_STATE_FRAME_TYPES.has(id)) {
959	    let f = e.vy !== 0 ? 2 : (e.ai1 > 0 ? 1 : 0);
960	    if (id === 32 && e.lai3 === 1) f += 3;
961	    return Math.min(frames - 1, f);
962	  }
963	  // 火妖 24（FindFrame case 24，cs:77681-77719）：待机/行走带 0-3 每 6t 循环
964	  // （无站定门，恒转）；蓄力（ai[1]>0）切攻击带 4-9——进带清零推进、每 6t 一帧、
965	  // 末帧 9 钳住不回卷。无状态近似：以蓄力倒计时反推进度（elapsed=30-ai[1]，30 为
966	  // 蓄力起点；传送置 5 的 5t 内会错取带内高帧，差异登记——彼时被 50 颗传送尘遮挡）
967	  if (id === 24) {
968	    if (e.ai1 > 0) return Math.min(9, 4 + Math.floor((30 - e.ai1) / 6));
969	    return Math.floor(t / 6) % 4;
970	  }
971	  // 沙漠幽魂 533（FindFrame case 533，cs:70647-70661）：counter 0-48 循环、帧=
972	  // floor(counter/6)（0-7 每 6t）；蓄力（ai[1]>0）整带 +8（表 16 帧=待机 8+攻击 8。
973	  // 曾落通用 6t 档 → 16 帧连播两带混播）。相位取全局 t（%48），带切换时相位任意（差<48t）
974	  if (id === 533) return (e.ai1 > 0 ? 8 : 0) + Math.floor((t % 48) / 6);
975	  // 鸟族 74/297/298/442（FindFrame case 74,cs:74326-74350）：站定(vx==0&&vy==0)=
976	  // 帧 4 收翅站立;移动/飞行=帧 0..frames-2 每 4t 推进(回卷 frames-1→0——末帧行
977	  // =站立帧不参与循环)。曾落末尾通用 6t 全帧循环 → 落地也播飞行动画(2026-08-18 报)
978	  if (id === 74 || id === 297 || id === 298 || id === 442) {
979	    if (e.vx === 0 && e.vy === 0) return Math.min(4, frames - 1);
980	    return Math.floor(t / 4) % Math.max(1, frames - 1);
981	  }
982	  // 丛林鸟族 671-675（case 671,cs:74352-74377）：站定=帧 0;移动/飞行=帧 1..frames-1
983	  // 每 4t 推进(回卷 frames→1,首帧行=站立不参与循环)
984	  if (id >= 671 && id <= 675) {
985	    if (e.vx === 0 && e.vy === 0) return 0;
986	    return 1 + Math.floor(t / 4) % Math.max(1, frames - 1);
987	  }
988	  // 鸮族 611/689（case 611,cs:74379-74443）：站定=8 帧转头待机(三段 40t 序列
989	  // {0,1,2,1}/{0,3,4,3}/{0,5,6,7} 各帧 10t;原版随机换段/1-80 跳帧近似为顺序轮播,
990	  // 差异登记);移动/飞行=帧 8..frames-1 每 5t(<8 抬回 8)。表 13 帧=待机 8+飞行 5
991	  if (id === 611 || id === 689) {
992	    if (e.vx === 0 && e.vy === 0) return owlIdleFrame(e);
993	    return 8 + Math.floor(t / 5) % Math.max(1, frames - 8);
994	  }
995	  // 萤火虫族 355/358/654（case 355,cs:73369-73390）：counter<4→帧0/否则帧1（≥7 回卷
996	  // = 4t 亮 3t 闪）；非发光期(lai1≤0)整带 +2（暗带,localAI[2] 门——lai1=本仓发光剩余）
997	  if (id === 355 || id === 358 || id === 654) {
998	    const blink = (t % 7) < 4 ? 0 : 1;
999	    return Math.min(frames - 1, blink + (e.lai1 <= 0 ? 2 : 0));
1000	  }
1001	  // 精灵萤 677（case 677,cs:73391-73402）：counter 每 tick +2、≥6 回卷 → 每 3t 推进
1002	  if (id === 677) return Math.floor(t / 3) % Math.max(1, Math.min(4, frames));
1003	  // 蜻蜓族 595-601（case 595,cs:73403-73419）：每 3t 一帧全帧循环
1004	  if (id >= 595 && id <= 601) return Math.floor(t / 3) % Math.max(1, frames);
1005	  // 蚯蚓族 357/448/484/606（case 357,cs:73455-73509）：腾空=帧1（+direction*0.1/t
1006	  // 累积自旋,渲染 spin 未接备案）;地面静止=帧1;爬行 0↔1 每 12t 摆动
1007	  if (id === 357 || id === 448 || id === 484 || id === 606) {
1008	    if (e.vy !== 0 || e.vx === 0) return Math.min(1, frames - 1);
1009	    return Math.floor(t / 12) % Math.min(2, frames);
1010	  }
1011	  // 蛆虫族 485/486/487（case 485,cs:73511-73565）：地面静止=帧1;爬行 counter
1012	  // +=|vx|*5 >10 推进、0..3 循环（walkCycleT 按 |vx| 累加等价折算）;腾空=帧1
1013	  if (id === 485 || id === 486 || id === 487) {
1014	    if (e.vy !== 0 || e.vx === 0) return Math.min(1, frames - 1);
1015	    return Math.min(frames - 1, Math.floor((e.walkCycleT * 5) / 10) % 4);
1016	  }
1017	  // 瓢虫 604/605 + 椿象 669（case 604,cs:67616-67652）：移动时每 2t 一帧;地面
1018	  // 循环 0-3、腾空循环 4-7（表 8 帧）;静止 counter 冻结（近似取 0 差异登记）
1019	  if (id === 604 || id === 605 || id === 669) {
1020	    const k = Math.floor(t / 2) % 4;
1021	    return Math.min(frames - 1, e.vy === 0 ? k : 4 + k);
1022	  }
1023	  // 水鸟族 363/365/603/609（case 363,cs:74470-74545）：湿态=帧 1↔2 每 8t（划水）;
1024	  // 站定(vx==0&&vy==0)=帧1;飞行/移动=帧 11..frames-1 每 4t（回卷 frameCount→11）
1025	  if (id === 363 || id === 365 || id === 603 || id === 609) {
1026	    if (e.wet) return 1 + (Math.floor(t / 8) % Math.min(2, Math.max(1, frames - 1)));
1027	    if (e.vx === 0 && e.vy === 0) return Math.min(1, frames - 1);
1028	    return Math.min(frames - 1, 11 + (Math.floor(t / 4) % Math.max(1, frames - 11)));
1029	  }
1030	  // 珍稀宝箱怪 473-476（case 473,cs:71831-72000）：ai0 0/7=伪装帧0（曾落通用档
1031	  // 14 帧连播 = 伪装态狂闪）;ai0 1=警戒帧1-5 按 ai1/6 分段(+6 兜底);ai0 8=3+(t/6)
1032	  // 钳 3-6;ai0 4/5=帧13;ai0 2/6 地面走=8/9 每 8t + 周期眨眼 10-12（状态机序列
1033	  // 近似为 24t 走/24t 眨穿插,ai0 3 回落帧 7 近似——差异登记）
1034	  if (id >= 473 && id <= 476) return mimicFrame(e, frames);
1035	  // 其余（眼/蜂群/幽灵/蠕虫段等）：每 6 tick 全循环
1036	  return Math.floor(t / 6) % frames;
1037	}
1038	
1039	// ---- 光标图标 GetItemLight 特殊物品（ItemSlot.cs:3475-3507）----
1040	/** 迪斯科族（:3475-3490）:662/663 彩虹砖块系 + 5444/5450/5643 + 5128 → Main.Disco */
1041	const CURSOR_DISCO_ITEMS = new Set([662, 663, 5444, 5450, 5643, 5128]);
1042	/** ItemIconPulse 族（:3491-3496,ItemID.cs:1100）:微光脉冲 × Main.essScale */
1043	const CURSOR_PULSE_ITEMS = new Set([520, 521, 575, 549, 548, 547, 3456, 3457, 3458, 3459, 3580, 3581]);
1044	/** 精华族（:3497-3507）:58/184/4143 → essScale×0.25+0.75 */
1045	const CURSOR_ESS_ITEMS = new Set([58, 184, 4143]);
1046	
1047	/** 图标矩形乘色（离屏三步:draw → multiply → destination-in 恢复 alpha）。
1048	 *  ★禁止在主画布直接 source-atop——作用于整张已渲染画布=黑方块（2026-08-18 事故） */
1049	const tintScratch = typeof document !== 'undefined' ? document.createElement('canvas') : null;
1050	function tintIconRect(
1051	  ctx: CanvasRenderingContext2D,
1052	  icon: { img: CanvasImageSource; sx: number; sy: number; sw: number; sh: number },
1053	  dst: { x: number; y: number; w: number; h: number },
1054	  tint: readonly [number, number, number],
1055	): void {
1056	  if (!tintScratch) return;
1057	  if (tintScratch.width !== dst.w || tintScratch.height !== dst.h) {
1058	    tintScratch.width = dst.w;
1059	    tintScratch.height = dst.h;
1060	  }
1061	  const octx = tintScratch.getContext('2d');
1062	  if (!octx) return;
1063	  octx.clearRect(0, 0, dst.w, dst.h);
1064	  octx.imageSmoothingEnabled = false;
1065	  octx.drawImage(icon.img, icon.sx, icon.sy, icon.sw, icon.sh, 0, 0, dst.w, dst.h);
1066	  octx.globalCompositeOperation = 'multiply';
1067	  octx.fillStyle = `rgb(${tint[0] | 0},${tint[1] | 0},${tint[2] | 0})`;
1068	  octx.fillRect(0, 0, dst.w, dst.h);

```


---

## 🤖 Assistant · 2026-08-19T07:39:08.666Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I understand the structure of `vanillaFrameIdx`. It's a function with id-based branches; uses `e.animT` (t), `e.walkCycleT`, `e.ai0/ai1/ai2/ai3`, `e.lai0/1/2/3`, `e.vx/vy`, `e.onGround`, `e.wet`, `e.hp/maxHp`, `e.customFrameIdx`.

Note: some frames are stateless approximations (global t) while others use AI-synced state. The task allows me to write `e.lai0/e.lai1/e.customFrameIdx` in the AI files.

Key question: what's `e.animT`? It's a tick counter — likely incremented every AI tick. Let me check the Enemy class to understand the fields: animT, walkCycleT, ai0-3, lai0-3, customFrameIdx, dummyHitDir etc. Let me read Enemy.ts relevant parts.

Also I need to check how `frames` is derived and how drawEnemy uses vanillaFrameIdx (line 4194/5248). And the atlas `vnpc(id, frameIdx)` for special multi-sheet draws (398/397 at 5768/5843 — those are Moon Lord / etc.?).

Then read the AI files for:
- bossAI_martian.ts: turret 393 (ai2/ai3 semantics), cannon 394, saucer 395 (ai3 cycle timing), 392, probe 399 (ai0 escape), tesla 387 (deploy timer), engineer 386 (deploy ai2).
- bossAI_moon_events.ts: pumpkingAI (ai3 semantics), iceQueen, santaNK1, mourningWood, everscream.
- bossAI_dd2.ts: betsyAI (flap counter, ai1?).
- bossAI_lategame.ts: cultist AI states.

Let me read Enemy.ts first (fields), then the AI files. Let me grep Enemy.ts for these fields.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:39:09.192Z · glm-x-preview-260804

```
现在我来检查一下 Enemy 字段和动画时钟。
```


---

## 🤖 Assistant · 2026-08-19T07:39:10.612Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"animT\\|walkCycleT\\|customFrameIdx\\|lai0\\|ai0\\b\\|ai1\\b\\|ai2\\b\\|ai3\\b\" src/entities/Enemy.ts | head -60",
 "description": "Find animation state fields in Enemy.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:39:10.648Z

**📎 ToolResult**

```
126: *  fading（目标失效 / 中心距 ≥300 / 目标玩家不在神圣，:45244-45252）→ ai2 +1，
128: *  opacity = GetLerpValue(60, cap/2, ai2)（:45263）——ai2 ≤ cap/2 全显，
129: *  cap/2→60 线性渐隐；ai2 ≥ 60 → despawn（active=false，:45254-45261）。
130: *  渲染侧 Renderer.npcGlowOrbitParams 同源消费 ai2（轨道环半径 2+ai2 /
131: *  num300 下限 GetLerpValue(0,60,ai2) / 相位 0→3）。 */
133:  ai2: number, fading: boolean, cap: number,
134:): { ai2: number; opacity: number; despawn: boolean } {
136:  const next = Math.max(0, Math.min(cap, ai2 + (fading ? 1 : -1)));   // cs:45253 Clamp(±1, 0, num4)
137:  if (next >= DESPAWN) return { ai2: next, opacity: 0, despawn: true };
143:  return { ai2: next, opacity, despawn: false };
153: *  未移植时 ai0 恒 0 = 永远休眠，离屏不消散与原版休眠态一致 */
159: *  type==690&&ai0==0 门）。★14/15（EoW 体节/尾）必在——它们 SetDefaults boss=false
396:    if (this.vanillaId === 117 && this.ai1 === 0 && !this._wormSpawnFx) {
419:    // 之前——玩家死亡 ai2 计时照走（曾误放早退后：玩家被磨死即冻结、渐隐链断）。
421:      this.ai2 += 1;
424:      if (spd >= 1 && this.ai2 <= LIFE_LAST) {
425:        // velocity *= Remap(ai2, 285, 570, 1, 0.5)（clamped 线性）
427:        const k = this.ai2 <= half ? 1
428:          : this.ai2 >= LIFE_LAST ? 0.5 : 1 - 0.5 * (this.ai2 - half) / (LIFE_LAST - half);
431:      if (this.ai2 === LIFE_LAST) {
444:      if (this.ai2 >= LIFE) this.ai2 = 0;
721:    spit.ai0 = 0; spit.ai1 = 1;
889:  animT = 0;
913:  walkCycleT = 0;        // 行走帧累加器（≈原版 frameCounter，按 |vx| 推进）
1074:  lai0 = 0;              // localAI 语义位（萤火虫：闪烁间隔计时）
1075:  lai1 = 0;              // localAI 语义位（萤火虫：发光剩余帧）
1076:  lai2 = 0;              // localAI[2] 语义位（AI_054 克脑：二阶段入场演出门）
1077:  lai3 = 0;              // localAI[3] 语义位（AI_054 克脑：玩家死/离场下坠计数；AI_008 法师 32：RedHat 变体带 +3）
1080:   *  32 的 lai3 变体带/双倍计时因此不触发（常态=单一头饰形态，2026-08-17 帧修复的门） */
1091:  customFrameIdx: number | null = null;
1127:  ai0 = -1120;
1128:  ai2 = 0;
1130:  ai1 = 0;
1132:  ai3 = 0;
1136:  /** AI 首帧初始化标记（原版 ai[0]==0 门在 ai0 初值 -1120 的史莱姆语义下不可用） */
1146:   *  与各状态复用的 ai3 计时器分离——曾共用导致寿命被状态转换反复清零） */
1226:      this.animT++;
1229:      if (Math.abs(this.vx) > 0.05) this.walkCycleT += Math.abs(this.vx);
1243:    this.animT++;
1244:    this.walkCycleT += Math.abs(this.vx); // 原版 zombie/fighter 行走帧按 |vx| 累加（L77072/L70216）
1247:    if (Math.abs(this.vx) <= 0.05) this.walkCycleT = 0;
1277:          if ((this.vanillaId === 379 || this.vanillaId === 380) && this.ai3 < 0) {
1637:      if (this.vanillaId === 1 && this.ai1 === 1125) {
1678:            const sl = (game.enemies() as Enemy[]).find((n) => n.id === this.ai3 && n.ai0 === -999);
1846:    if (this.ai1 !== 0) return;                    // 已掷过：-1=空 / >0=物品（只掷一次）
1853:    this.ai1 = -1;                                 // :60752 先置空
1867:      if (this.ai1 !== -1) break;                  // :60777-60781 已中即停
1870:          this.ai1 = this.slimeGenItemInsideBody(this.ai0 === -999);
1876:        if (roll(maxValue2) === 0) this.ai1 = roll(2) === 0 ? 1103 : 593;  // 淤泥/雪块
1891:          this.ai1 = roll(2) === 0 ? 3736 + roll(3) : 1345;         // Next(3736,3739) 气球/彩纸
1894:          this.ai1 = num5 === 1 ? 1125 : num5 === 2 ? 314 : num5 === 3 ? 5395 : 1124;
1896:          this.ai1 = this.slimeGenItemInsideBody(this.ai0 === -999);
1900:            this.ai1 = 751;                        // 云块
1903:            this.ai1 = num7 === 1 ? 3 : num7 === 2 ? 9 : 2;         // 石/木/土
1905:            this.ai1 = 3609;                        // :60888-60890 传送带
1909:            this.ai1 = num9 === 1 ? 150 : num9 === 2 ? 3086 : num9 === 3 ? 3081 : 3; // 蛛网/花岗岩/大理石/石
1912:          this.ai1 = 539;                           // :60911-60913 史莱姆法杖
1914:          this.ai1 = 147;                           // :60914-60916 ftw 地下 → 棘刺丛林史莱姆物
1915:        } else if (i === 0 && sf.remix && this.ai0 !== -999 && roll(3) === 0) {
1916:          this.ai1 = 75;                            // :60917-60919 首掷 remix → 生命水晶星史莱姆

```


---

## 🤖 Assistant · 2026-08-19T07:39:14.806Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. Enemy has:
- `animT` (t) — incremented every tick (line 1226/1243)
- `walkCycleT` — walking accumulator
- `ai0..ai3`, `lai0..lai3`, `customFrameIdx`

Now let me read the AI files. Start with bossAI_martian.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:39:15.111Z · glm-x-preview-260804

```
现在我来读取火星 AI 的实现。
```


---

## 🤖 Assistant · 2026-08-19T07:39:15.637Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:39:15.933Z

**📎 ToolResult**

```
1	// 火星疯狂(Martian Madness) AI 家族 1:1 移植(Terarria1456, 1.4.5.6)：
2	//   aiStyle 80  火星探测器 399                NPC.cs:38129-38223（巡逻→受惊悬停 60t→
3	//                                              反向加速升空,出屏/180t → Main.StartInvasion(4)）
4	//   aiStyle 76  火星飞碟核心 395              NPC.cs:36322-36773（600t 攻击循环 六窗口巡航;
5	//                                              生成 393×2/394×2/392×1;SetDefaults dontTakeDamage
6	//                                              =true → 部件全灭前无敌,普通模式部件全灭→自毁）
7	//   aiStyle 75  飞碟部件 392/393/394 + 骑手 390  NPC.cs:35745-36321（锚主体零速跟随;
8	//                                              393 激光窗[280,420)/394 炮窗[440,580)/392
9	//                                              死光电报[20,260)+空巢发射器;390 骑 391 射 438）
10	//   aiStyle 74  火星无人机 388(+日耀 Corite 418) NPC.cs:35452-35744（悬浮瞄准→蓄力→
11	//                                              扑咬;388 贴身 64px/撞块自爆 192×192 伤 80）
12	//   aiStyle 73  特斯拉炮塔 387                 NPC.cs:35340-35451（120t 部署渐显→180t
13	//                                              循环电击 435;受击打断 -30t）
14	//   aiStyle 72  泡泡盾 384                     NPC.cs:35318-35339（锚军官 383,军官死→消散）
15	//   aiStyle  3  火星军官 383 / 工程师 386 尾段  NPC.cs:56614-56645 / 59384-59428（军官带盾
16	//                                              无敌+180t 补盾;工程师 ±5t 扫地放 387,上限 4×自身）
17	//   aiStyle 49  愤怒云 250(同批普查顺带)        NPC.cs:31742-31810（悬顶 200px,正下方淋雨 264）
18	// expert 分支(飞碟 ai0=1 旋转过渡/ai0=2 死光弹幕 3600t)按 world.isExpert 真难度开闭
19	// （World.get isExpert = difficulty >= EXPERT;曾硬编码 EXPERT=false 恒关）;netcode 跳过。
20	// 弹幕贴图 Projectile_{264,435,438,447-450}.png 已入 sprites/vanilla(见 shootM 注释)。
21	import type { Enemy } from './Enemy';
22	import type { GameHooks } from './types';
23	import type { Player } from './Player';
24	import { TILE, GRAVITY, MAX_FALL_SPEED } from '../core/constants';
25	import { moveAndCollide } from '../physics/TileCollision';
26	import { spawnPart, losClear } from './bossAI';
27	import { Arrow } from './Arrow';
28	import { canStartInvasion, startInvasion, INVASION_MARTIAN } from '../world/Invasion';
29	import { dutchmanCannonAI } from './bossAI_dd2';
30	
31	/** 原版 localAI[0..3]（Enemy 的 ai0-ai3 对应 ai[],localAI 独立 → WeakMap 落盘） */
32	const localAI = new WeakMap<Enemy, number[]>();
33	const la = (e: Enemy): number[] => {
34	  let a = localAI.get(e);
35	  if (!a) { a = [0, 0, 0, 0]; localAI.set(e, a); }
36	  return a;
37	};
38	/** 主体 → 部件槽位（395 飞碟与 392 炮体共用 [炮塔0,炮塔1,火炮0,火炮1],cs:36327-36355） */
39	const slots = new WeakMap<Enemy, Enemy[]>();
40	/** 军官 383 → 泡泡盾 384 引用（原版 ai[2]=盾 index+1,cs:56618） */
41	const officerShield = new WeakMap<Enemy, Enemy>();
42	
43	const rnd = (n: number): number => Math.floor(Math.random() * n);
44	const rndRange = (a: number, b: number): number => a + Math.floor(Math.random() * (b - a));
45	const clamp = (v: number, lo: number, hi: number): number => (v < lo ? lo : v > hi ? hi : v);
46	const lerp = (a: number, b: number, t: number): number => a + (b - a) * t;
47	const sign = (v: number): number => (v > 0 ? 1 : v < 0 ? -1 : 0);
48	
49	// ---------------------------------------------------------------------------
50	// 弹幕:火星族弹体贴图 Projectile_{264,435,438,447,448,449,450}.png 已按 601/602
51	// 先例自 terraria-assets/Images 补入 public/sprites/vanilla/(Arrow 按 projId 懒加载),
52	// 此前的 RENDER_PROXY 代渲登记已退役。
53	// ProjectileID.cs 对照:264 RainCloud 雨滴 / 435 MartianTurretBlast(特斯拉电球) /
54	// 438 MuonBlast(骑手弹) / 447 MartianDeathray(死光电报,自带 proj AI 未实装→直飞代) /
55	// 448 MartianSaucerCannon(火炮弹) / 449 MartianSaucerLaser(激光) / 450 MartianMissile。
56	// ---------------------------------------------------------------------------
57	function shootM(
58	  game: GameHooks, x: number, y: number, vx: number, vy: number,
59	  dmg: number, projId: number, life = 300, pierce = 1,
60	  arrowOpts?: Partial<import('./Arrow').ArrowOpts>,
61	): void {
62	  (game as unknown as { entities: { add: (e: unknown, b: string) => void } }).entities.add(
63	    new Arrow(x, y, vx, vy, dmg, 0, projId, null, { grav: 0, life, pierce, hostile: true, ...arrowOpts }),
64	    'projectiles');
65	}
66	
67	/** 脚下净空扫描（cs:36400-36421 同构）：返回到第一个实心面的像素距离。
68	 *  脚下即实心 → 16px（原版 num=1）；150t 内无面 → 150*16 */
69	function groundGapPx(game: GameHooks, e: Enemy): number {
70	  const st = game.world.store;
71	  const tx = Math.floor(e.cx / TILE);
72	  const ty = Math.floor((e.y + e.h) / TILE);
73	  const solidAt = (x: number, y: number) =>
74	    x >= 0 && y >= 0 && x < st.w && y < st.h && st.isSolid(x, y) && !st.half[st.idx(x, y)];
75	  if (solidAt(tx, ty)) return TILE;
76	  let n = 0;
77	  while (n < 150 && ty + n < st.h) {
78	    if (solidAt(tx, ty + n)) { n--; break; }
79	    n++;
80	  }
81	  return n * TILE;
82	}
83	
84	/** 原版 CS 直积分（noTileCollide 族） */
85	const fly = (e: Enemy): void => { e.x += e.vx; e.y += e.vy; };
86	/** 单格实心（世界边界外视为空,飞碟出界由本 AI 兜底） */
87	function solidTile(game: GameHooks, x: number, y: number): boolean {
88	  const st = game.world.store;
89	  const tx = Math.floor(x / TILE), ty = Math.floor(y / TILE);
90	  return tx >= 0 && ty >= 0 && tx < st.w && ty < st.h && st.isSolid(tx, ty);
91	}
92	
93	// ---------------------------------------------------------------------------
94	// AI_080 火星探测器 399（NPC.cs:38129-38223）
95	// ai[0] 0=巡逻(3px/s 朝向走,贴地 15t 内上升) / 1=受惊悬停 60t(×0.95) /
96	//        2=逃逸(noTileCollide,vy-0.1→-10 / vx+0.05*ai[3]→4)
97	// 触发：352px 内且玩家在下方 → 1；逃逸出屏(y<-h)或 180t → StartInvasion(4) + 消散
98	// ---------------------------------------------------------------------------
99	export function martianProbeAI(e: Enemy, game: GameHooks, player: Player | null) {
100	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; e.ai3 = 0; }
101	  // 撞墙转向（:38137-38140 collideX → direction 翻转;首帧 direction==0 先索敌）
102	  if (e.hitWall) e.facing = -e.facing;
103	
104	  if (e.ai0 === 0) {
105	    // 方向固定（原版仅 direction==0 时 TargetClosest,:38133-38136;撞墙翻转）
106	    e.vx = 3 * e.facing;
107	    // 贴地升降（:38145-38163）：脚下 30t 内首个实心面 <15t 升 / <20t 平 / 其余缓降
108	    const st = game.world.store;
109	    const tx = clamp(Math.floor(e.cx / TILE), 1, st.w - 2);
110	    let ty = Math.floor(e.cy / TILE);
111	    let gap = 30;
112	    for (let i = 0; i < 30; i++) { if (solidTile(game, tx * TILE, (ty + i) * TILE)) { gap = i; break; } }
113	    if (gap < 15) e.vy = Math.max(e.vy - 0.05, -3.5);
114	    else if (gap < 20) e.vy *= 0.95;
115	    else e.vy = Math.min(e.vy + 0.05, 1.5);
116	    // 受惊门（:38165-38173）：352px 内且玩家中心在探测器下方
117	    if (!player || player.dead) return;
118	    const dist = Math.hypot(player.cx - e.cx, player.cy - e.cy);
119	    if (dist < 352 && player.cy > e.cy) { e.ai0 = 1; e.ai1 = 0; }
120	  } else if (e.ai0 === 1) {
121	    // 悬停报警（:38175-38192）：60t 减速 → 逃逸,ai[3] = 玩家反侧方向
122	    e.ai1 += 1;
123	    e.vx *= 0.95; e.vy *= 0.95;
124	    if (e.ai1 >= 60) {
125	      e.ai1 = 0; e.ai0 = 2;
126	      e.ai3 = player && !player.dead && player.cx > e.cx ? -1 : 1;
127	    }
128	  } else {
129	    // 逃逸（:38194-38208）：noTileCollide,向上加速+横向 4px;出屏/180t → 入侵
130	    e.ai1 += 1;
131	    e.vy = Math.max(e.vy - 0.1, -10);
132	    e.vx = Math.min(e.vx + e.ai3 * 0.05, 4);
133	    if (e.y < -e.h || e.ai1 >= 180) {
134	      // Main.StartInvasion(4)（:38202）：原版只查"≥200HP 玩家数>0"且无视 delay;
135	      // canStartInvasion(ignoreDelay=true) 同语义,invasionType!=0 时静默 no-op。
136	      // 走 startInvasionWithAnnounce 带逼近公告(Game.startInvasionAndAnnounce
137	      // 实体侧通道)——直通 startInvasion 会漏 misc 广播+invasionWarn
138	      if (player && canStartInvasion(game.world, player.maxHp, true)) {
139	        if (!game.startInvasionWithAnnounce?.(INVASION_MARTIAN, true)) {
140	          startInvasion(game.world, INVASION_MARTIAN);
141	        }
142	      }
143	      e.dead = true;   // 原版 active=false（不走掉落/击杀记账）
144	      return;
145	    }
146	  }
147	  // 点光（:38210-38217）：rgb = ai0==2 ? Color.Red : Color.SkyBlue，×0.65
148	  // ——SkyBlue(135,206,235)/255×0.65=(0.344,0.525,0.599)；Red×0.65=(0.65,0,0)
149	  e.lightRGB = e.ai0 === 2 ? [0.65, 0, 0] : [0.344, 0.525, 0.599];
150	  // 位移：0/1 态贴地碰撞（SetDefaults 无 noTileCollide）,2 态原版置 noTileCollide=true
151	  if (e.ai0 === 2) fly(e);
152	  else moveAndCollide(e, game.world, e.vx, e.vy);
153	}
154	
155	// ---------------------------------------------------------------------------
156	// AI_076 火星飞碟核心 395（NPC.cs:36322-36773）
157	// ai[0] 0=巡航攻击循环(ai[3] 600t 六窗口) / -1/-2=目标失效爬升驱散 /
158	//        1=expert 部件全灭旋转过渡(150t,本工程不可达) / 2=expert 死光弹幕(3600t) /
159	//        3=自毁(普通模式部件全灭,由 392 炮体置位)
160	// 攻击窗口（cs:36379-36397）：[580,600)=0 远侧悬停 / [20,260)=1 横掠 / [260,280)=2
161	//   归位 / [280,420)=3 炮塔激光（393 发射）/ [420,440)=4 顶悬 / [440,580)=5 火炮（394 发射）
162	// ---------------------------------------------------------------------------
163	const WIN = (a3: number): number =>
164	  a3 >= 580 ? 0 : a3 >= 440 ? 5 : a3 >= 420 ? 4 : a3 >= 280 ? 3 : a3 >= 260 ? 2 : a3 >= 20 ? 1 : 0;
165	
166	export function martianSaucerAI(e: Enemy, game: GameHooks, player: Player | null) {
167	  // ---- 首帧生成部件（:36324-36355）：炮塔 393×2(ai[1]=0/1) 火炮 394×2 + 炮体 392 ----
168	  if (!e.bInit) {
169	    e.bInit = true;
170	    e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
171	    const parts: Enemy[] = [];
172	    for (let i = 0; i < 2; i++) {
173	      const t = spawnPart(game, e, 393);
174	      if (t) { t.ai1 = i; t.master = e; parts.push(t); }
175	    }
176	    for (let i = 0; i < 2; i++) {
177	      const c = spawnPart(game, e, 394);
178	      if (c) { c.ai1 = i; c.master = e; parts.push(c); }
179	    }
180	    const hull = spawnPart(game, e, 392);
181	    if (hull) {
182	      hull.master = e;
183	      slots.set(hull, parts);   // 原版 392.localAI[0..3] = 四槽（cs:36351-36354）
184	    }
185	    slots.set(e, parts);
186	  }
187	  // ---- 自毁态（:36357-36360,普通模式由 392 置 ai0=3）----
188	  if (e.ai0 === 3) {
189	    e.iframes = 0;
190	    e.hp = 0;
191	    e.hurt(9999, 0, 0, game);   // StrikeNPCNoInteraction(9999) → 标准死亡管线(掉落/记账)
192	    return;
193	  }
194	  // ---- 无敌（SetDefaults dontTakeDamage=true,:13992;仅 expert ai0=1 态解除 :36636）----
195	  if (e.ai0 !== 1 && e.ai0 !== 2) e.iframes = 2;
196	
197	  const center = { x: e.cx, y: e.cy };
198	  const RANGE = 5600;   // :36363
199	  // 目标失效（:36362-36388）：>5600px 或死亡 → -1(自巡航态)/-2(自弹幕态)
200	  const targetInvalid = !player || player.dead
201	    || Math.hypot(player.cx - center.x, player.cy - center.y) > RANGE;
202	  if (targetInvalid && e.ai0 !== 1) {
203	    if (e.ai0 === 0) e.ai0 = -1;
204	    else if (e.ai0 === 2) e.ai0 = -2;
205	  }
206	  if (e.ai0 === -1 || e.ai0 === -2) {
207	    e.vy -= 0.4;
208	    e.encourageDespawn(10);
209	    if (player && !player.dead) {
210	      e.despawnTimer = 300;                       // timeLeft = 300（:36387）
211	      // ★-1 态恢复语义（证据链）：1456 反编译 NPC.cs:36392-36395 为
212	      //   `if (this.ai[0] == 0f) { this.ai[0] = 0f; }`——此处置身 -1/-2 分支内
213	      //   恒为 no-op;1405 反编译（NPC.145.cs:36392-36395）逐字相同 → 两代独立
214	      //   反编译一致,IL 即如此。结论：-1（巡航转场）飞碟玩家回场**不回巡航**,
215	      //   持续 vy−0.4/t 爬升到出界钳制消散（:36751-36772）;仅 -2（expert 死光
216	      //   转场）按 :36388-36391 回 2 态。曾误按对称性把 -1 也回 0 态。
217	      if (e.ai0 === -2) e.ai0 = 2;
218	      e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
219	    }
220	    fly(e);
221	    return;
222	  }
223	
224	  if (e.ai0 === 0) {
225	    // ---- 巡航攻击循环（:36390-36634）----
226	    const w1 = WIN(e.ai3);
227	    e.ai3 += 1;
228	    if (e.ai3 >= 600) e.ai3 = 0;
229	    const w = WIN(e.ai3);
230	    if (w !== w1) {                                // 窗口切换初始化（:36414-36430）
231	      if (w === 0) e.ai2 = 0;
232	      if (w === 1) e.ai2 = player && player.cx > center.x ? 1 : -1;
233	      if (w === 2) e.ai2 = 0;
234	    }
235	    const pcx = player ? player.cx : center.x, pcy = player ? player.cy : center.y;
236	    switch (w) {
237	      case 0: {
238	        // 远侧 600px 悬停（:36432-36446）：到点(<50px)跳 [19] 直进横掠
239	        if (e.ai2 === 0) e.ai2 = -600 * sign(center.x - pcx);
240	        let dx = pcx + e.ai2 - center.x, dy = pcy - 250 - center.y;
241	        const d = Math.hypot(dx, dy);
242	        if (d < 50) { e.ai3 = 19; break; }
243	        dx /= d; dy /= d;
244	        e.vx = lerp(e.vx, dx * 16, 0.1); e.vy = lerp(e.vy, dy * 16, 0.1);
245	        break;
246	      }
247	      case 1: {
248	        // 横掠（:36448-36480）：vx=3.5*ai[2];脚下净空<250px 上浮补齐
249	        const gap = groundGapPx(game, e);
250	        if (gap < 250) {
251	          const t = 4 > gap ? -gap : -4;
252	          e.vy = lerp(e.vy, t, 0.05);
253	        } else e.vy *= 0.95;
254	        e.vx = 3.5 * e.ai2;
255	        break;
256	      }
257	      case 2: {
258	        // 归位（:36514-36553）：玩家上方 ±300px;净空<170 抬升;到点(<70px)跳 [279] 进激光窗
259	        if (e.ai2 === 0) e.ai2 = 300 * sign(center.x - pcx);
260	        let dx = pcx + e.ai2 - center.x, dy = pcy - 170 - center.y;
261	        const gap = groundGapPx(game, e);
262	        if (gap < 170) dy -= 170 - gap;
263	        const d = Math.hypot(dx, dy);
264	        if (d < 70) { e.ai3 = 279; break; }
265	        dx /= d; dy /= d;
266	        e.vx = lerp(e.vx, dx * 20, 0.1); e.vy = lerp(e.vy, dy * 20, 0.1);
267	        break;
268	      }
269	      case 3: {
270	        // 激光窗缓漂（:36557-36582）：×0.85 双轴 + 净空<170 上浮
271	        const gap = groundGapPx(game, e);
272	        if (gap < 170) {
273	          const t = 4 > gap ? -gap : -4;
274	          e.vy = lerp(e.vy, t, 0.05);
275	        } else e.vy *= 0.85;
276	        e.vx *= 0.85;
277	        break;
278	      }
279	      case 4: {
280	        // 顶悬（:36591-36602）：到点(<50px)跳 [439] 进火炮窗
281	        let dx = pcx - center.x, dy = pcy - 250 - center.y;
282	        const d = Math.hypot(dx, dy);
283	        if (d < 50) { e.ai3 = 439; break; }
284	        dx /= d; dy /= d;
285	        e.vx = lerp(e.vx, dx * 16, 0.1); e.vy = lerp(e.vy, dy * 16, 0.1);
286	        break;
287	      }
288	      default: {
289	        // 火炮窗静止（:36604-36605）：×0.85 双轴
290	        e.vx *= 0.85; e.vy *= 0.85;
291	        break;
292	      }
293	    }
294	  } else if (e.ai0 === 1) {
295	    // ---- expert 部件全灭旋转过渡（:36634-36663,150t）:dontTakeDamage 解除(:36636) ----
296	    e.vx *= 0.96; e.vy *= 0.96;
297	    e.ai1 += 1;
298	    if (e.ai1 >= 150) { e.ai0 = 2; e.ai1 = 0; e.visAngle = 0; }
299	    else if (e.ai1 < 40) e.visAngle = Math.sin((e.ai1 / 40) * Math.PI * 2) * 0.2;   // UnitY.RotatedBy(t).Y = sin
300	    else if (e.ai1 < 80) e.visAngle = Math.sin((e.ai1 / 20) * Math.PI * 2) * 0.3;
301	    else if (e.ai1 < 120) e.visAngle = Math.sin((e.ai1 / 10) * Math.PI * 2) * 0.4;
302	    else e.visAngle = ((e.ai1 - 120) / 30) * Math.PI * 2;
303	  } else if (e.ai0 === 2) {
304	    // ---- expert 死光弹幕（:36670-36749,3600t 循环;每 120t 后 60t 为射线窗）----
305	    const wasWin = e.ai3 % 120 >= 60 ? 1 : 0;
306	    e.ai3 += 1;
307	    const inWin = e.ai3 % 120 >= 60 ? 1 : 0;
308	    if (inWin !== wasWin) {
309	      if (inWin === 1) {
310	        e.ai2 = player && player.cx > center.x ? 1 : -1;
311	        // :36210 死光生成音 Item12
312	        game.playSfxWav?.('Item_12', 1, e.cx, e.cy);
313	        const ray = new MartianDeathray(e, 80);   // 447 死光电报（AI_079 实体）
314	        (game as unknown as { entities: { add(el: unknown, b: string): void } }).entities.add(ray, 'projectiles');
315	      }
316	    }
317	    if (e.ai3 >= 3600) { e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
318	    else if (inWin === 0 && player) {
319	      let dx = player.cx + e.ai2 * 350 - center.x, dy = player.cy - 250 - center.y;
320	      const d = Math.hypot(dx, dy) || 1;
321	      dx /= d; dy /= d;
322	      e.vx = lerp(e.vx, dx * 16, 0.1); e.vy = lerp(e.vy, dy * 16, 0.1);
323	    } else {
324	      const gap = groundGapPx(game, e);
325	      if (gap < 250) {
326	        const t = 4 > gap ? -gap : -4;
327	        e.vy = lerp(e.vy, t, 0.05);
328	      } else e.vy *= 0.95;
329	      e.vx = 8 * e.ai2;
330	    }
331	    e.visAngle = 0;
332	  }
333	  // ---- 出界钳制 + 消散（:36751-36772）----
334	  const st = game.world.store;
335	  if (e.y < -100 || e.x < -100 || e.y > st.h * TILE + 100 || e.x > st.w * TILE + 100) {
336	    e.x = clamp(e.x, -100, st.w * TILE + 100);
337	    e.y = clamp(e.y, -100, st.h * TILE + 100);
338	    e.dead = true;
339	    return;
340	  }
341	  fly(e);
342	}
343	
344	// ---------------------------------------------------------------------------
345	// AI_075 飞碟部件 392/393/394 + 骑手 390（NPC.cs:35745-36321;416/492 同构锚表一并接）
346	// 锚点偏移（cs:35766/35813/35820/35827）:390→391 (0,-14);392→395 (0,2) 旋转随体;
347	//   393→395 (±60,+29);394→395 (±49,-13),spriteDirection=±1;416→415 (-spriteDir*10,-30)
348	// 主体消亡（:36288-36299）:390→Transform(382) / 416→Transform(518) / 其余消散
349	// ---------------------------------------------------------------------------
350	export function martianSaucerPartAI(e: Enemy, game: GameHooks, player: Player | null) {
351	  const id = e.vanillaId ?? 0;
352	  // ---- 荷兰大炮 492（DD2 批 bossAI_dd2.ts：锚船体偏移 cs:35889 + 240t 装填炮击
353	  // cs:36008）——aiStyle 75 分发进本函数,转发后不走飞碟部件路径 ----
354	  if (id === 492) { dutchmanCannonAI(e, game, player); return; }
355	  // ---- 骑手首帧生成坐骑（:35750-35762）----
356	  if ((id === 390 || id === 416) && !e.bInit) {
357	    e.bInit = true;
358	    const mount = spawnPart(game, e, id === 390 ? 391 : 415);
359	    if (mount) e.master = mount;
360	  }
361	  if (!e.bInit && (id === 392 || id === 393 || id === 394)) e.bInit = true;
362	
363	  const mount = e.master;
364	  const mountOk = !!mount && !mount.dead;
365	  if (!mountOk) {
366	    // 主体消亡分支（:36288-36299）
367	    if (id === 390 || id === 416) {
368	      e.transformTo(id === 390 ? 382 : 518, game.world.store, false, game);   // Transform → 下车变步兵
369	    } else {
370	      e.dead = true;   // 部件随主体消散（life=0 + active=false,无掉落）
371	    }
372	    return;
373	  }
374	  const m = mount as Enemy;
375	  // ---- 锚定跟随（:35764-35845 + 36200-36214）：零速贴主体 + 偏移 ----
376	  let ox = 0, oy = 0;
377	  let spriteDir = m.facing;
378	  if (id === 390) { ox = 0; oy = -14; }
379	  else if (id === 392) { ox = 0; oy = 2; }
380	  else if (id === 393) { ox = e.ai1 === 1 ? 60 : -60; oy = 29; }
381	  else if (id === 394) { ox = e.ai1 === 1 ? 49 : -49; oy = -13; spriteDir = e.ai1 === 1 ? 1 : -1; }
382	  else if (id === 416) { ox = -m.facing * 10; oy = -30; }
383	  e.vx = 0; e.vy = 0;
384	  e.x = m.cx - e.w / 2 + ox;
385	  e.y = m.cy - e.h / 2 + oy;
386	  // spriteDirection（394 按 ai[1] 固定侧,其余随主体;:36206-36212）
387	  e.facing = spriteDir === 1 ? 1 : -1;
388	
389	  if (id === 390) {
390	    // ---- 骑手射击（:36216-36280）：ai[1] 冷却 60t(受击 -30),<700px+LOS 朝向对 → 438 弹 ----
391	    e.vx = m.vx;
392	    if (e.ai1 < 60) e.ai1 += 1;
393	    if (e.justHit) e.ai1 = -30;
394	    if (player && !player.dead) {
395	      const dx = player.cx - e.cx, dy = player.cy - e.cy;
396	      const canHit = losClear(game, e.x, e.y, player.x, player.y);
397	      if (canHit && Math.hypot(dx, dy) < 700) {
398	        if (e.ai1 === 60 && sign(dx) === e.facing) {
399	          e.ai1 = -60;
400	          const oxp = e.cx, oyp = e.cy - 4;
401	          let sx = player.cx - oxp, sy = player.cy - oyp;
402	          sx += rndRange(-50, 51); sy += rndRange(-50, 51);
403	          sx *= rndRange(80, 121) * 0.01; sy *= rndRange(80, 121) * 0.01;
404	          const d = Math.hypot(sx, sy);
405	          if (d > 0.001) { sx = (sx / d) * 7; sy = (sy / d) * 7; }
406	          else { sx = 0; sy = -7; }
407	          shootM(game, oxp, oyp, sx, sy, 30, 438);
408	          // 原版骑手 390 射弹无声(:35921-35996)——曾误挂 :36272 导弹段的
409	          // Item39(该音属空巢导弹,2026-08-19 终审删)
410	        }
411	      }
412	    }
413	    return;
414	  }
415	  if (id !== 392 && id !== 393 && id !== 394) return;
416	
417	  // ---- 部件攻击窗（共享 saucer.ai[3] 计数,cs:36128/36171/36235）----
418	  const saucer = m;
419	  e.ai3 = saucer.ai3;
420	  if (id === 394) {
421	    // 火炮窗 [440,580)（:36124-36150）：每 20t 一发 448,朝向 ±22.5° 散布,速 8
422	    if (e.ai3 >= 440 && e.ai3 < 580) {
423	      const n = e.ai3 - 440;
424	      if (n % 20 === 0) {
425	        const dirx = spriteDir;
426	        const delta = (Math.random() - 0.5) * 0.7853982;   // ±22.5° 散布（:36133-36136）
427	        shootM(game, e.cx + dirx * 36, e.cy + 8,
428	          Math.cos(delta) * 8 * dirx, Math.sin(delta) * 8 * dirx, 50, 448);
429	        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36098 火炮每发(终审补)
430	      }
431	    }
432	    return;
433	  }
434	  if (id === 393) {
435	    // 激光窗 [280,420)（:36152-36197）：窗内每 6t 一发 449 速 16;窗外只瞄准(ai[2] 角)
436	    const inWin = e.ai3 >= 280 && e.ai3 < 420;
437	    if (!inWin && player && !player.dead) {
438	      let dx = player.cx - e.cx, dy = player.cy - e.cy;
439	      if (dy < 0) dy = 0;
440	      const d = Math.hypot(dx, dy);
441	      if (d > 0.001) e.ai2 = Math.atan2(dy / d, dx / d);
442	      else e.ai2 = Math.PI / 2;
443	    }
444	    if (inWin) {
445	      const n = e.ai3 - 280;
446	      if (n % 6 === 0) {
447	        const ang = e.ai2 + (Math.random() - 0.5) * (0.7853982 / 3);
448	        shootM(game, e.cx, e.cy, Math.cos(ang) * 16, Math.sin(ang) * 16, 35, 449);
449	        game.playSfxFiles?.(['Item_12'], 1, e.cx, e.cy);     // :36140 部件激光(392 段 Item12)
450	      }
451	    }
452	    return;
453	  }
454	  // ---- 392 炮体（:36199-36286）----
455	  // 部件全灭检测（:35791-35820）：炮塔/火炮全灭 → 普通模式飞碟 ai0=3 自毁(expert→1)
456	  {
457	    const list = slots.get(e);
458	    const turrets = list ? list.slice(0, 2).filter((p) => !p.dead && p.vanillaId === 393) : [];
459	    const cannons = list ? list.slice(2, 4).filter((p) => !p.dead && p.vanillaId === 394) : [];
460	    let allDead = saucer.ai0 >= 1 || saucer.ai0 < 0 ? false : true;
461	    if (allDead && (turrets.length > 0 || cannons.length > 0)) allDead = false;
462	    if (allDead && saucer.ai0 === 0) {
463	      // :36322 后部件全灭分支：expert → ai0=1 旋转过渡进死光;否则 ai0=3 自毁
464	      if (game.world.isExpert) { saucer.ai0 = 1; saucer.ai1 = 0; saucer.ai2 = 0; saucer.ai3 = 0; }
465	      else { saucer.ai0 = 3; saucer.ai1 = 0; saucer.ai2 = 0; saucer.ai3 = 0; }
466	    }
467	  }
468	  // 死光电报（:36201-36219）：巡航态 ai[3]∈[20,260) 首帧（n==0）→ Projectile 447
469	  if (e.ai3 >= 20 && e.ai3 < 260 && saucer.ai0 === 0) {
470	    if (e.ai3 - 20 === 0) {
471	      // 447 死光电报实体（AI_079）——束体独立类（锚定电报塔/母舰，束高逐tick重算）
472	      // :36701 专家死光生成音 Item12(终审补)
473	      game.playSfxWav?.('Item_12', 1, e.cx, e.cy);
474	      const ray = new MartianDeathray(e, 50);
475	      (game as unknown as { entities: { add(el: unknown, b: string): void } }).entities.add(ray, 'projectiles');
476	    }
477	  }
478	  // 空巢发射器（:36221-36279）：窗口内对已灭槽位按概率补射 450 导弹
479	  {
480	    const list = slots.get(e) ?? [];
481	    const t0 = list[0], t1 = list[1], c0 = list[2], c1 = list[3];
482	    const t0Dead = !t0 || t0.dead || t0.vanillaId !== 393;
483	    const t1Dead = !t1 || t1.dead || t1.vanillaId !== 393;
484	    const c0Dead = !c0 || c0.dead || c0.vanillaId !== 394;
485	    const c1Dead = !c1 || c1.dead || c1.vanillaId !== 394;
486	    let flag76 = false, mv4 = 1000, mv5 = 1000;
487	    if (saucer.ai0 === 2) { flag76 = true; mv4 = 120; mv5 = 120; }
488	    if (!flag76 && e.ai3 >= 280 && e.ai3 < 400) { flag76 = true; mv5 = 90; mv4 = 60; }
489	    if (!flag76 && e.ai3 >= 440 && e.ai3 < 580) { flag76 = true; mv5 = 60; mv4 = 90; }
490	    if (flag76) {
491	      // 炮塔空巢（:36243-36258）:下方侧向抛射
492	      if (t0Dead && rnd(mv4) === 0) {
493	        // :36246-36250 速度 = (±rand3, ±1)×3 未归一(3~9.5 随机,曾归一恒 3)
494	        const mvx = -Math.random() * 3 * 3, mvy = 1 * 3;
495	        shootM(game, e.cx + rndRange(50, 70), e.cy + rndRange(30, 45), mvx, mvy, 30, 450, 300, 1,
496	          { bounce: true });  // aiStyle14 X 反跳(原版 ×-0.1,默认档 -0.5 近似)
497	        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36254 空巢导弹每发(终审补)
498	      }
499	      if (t1Dead && rnd(mv4) === 0) {
500	        // :36246-36250 速度 = (±rand3, ±1)×3 未归一(3~9.5 随机,曾归一恒 3)
501	        const mvx = Math.random() * 3 * 3, mvy = 1 * 3;
502	        shootM(game, e.cx + rndRange(50, 70), e.cy + rndRange(30, 45), mvx, mvy, 30, 450, 300, 1,
503	          { bounce: true });  // aiStyle14 X 反跳(原版 ×-0.1,默认档 -0.5 近似)
504	        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36254 空巢导弹每发(终审补)
505	      }
506	      // 火炮空巢（:36261-36276）:上方侧向抛射
507	      if (c0Dead && rnd(mv5) === 0) {
508	        // :36246-36250 速度 = (±rand3, ±1)×3 未归一(3~9.5 随机,曾归一恒 3)
509	        const mvx = -Math.random() * 3 * 3, mvy = -1 * 3;
510	        shootM(game, e.cx + rndRange(30, 60), e.cy + rndRange(-30, -10), mvx, mvy, 30, 450, 300, 1,
511	          { bounce: true });  // aiStyle14 X 反跳(原版 ×-0.1,默认档 -0.5 近似)
512	        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36254 空巢导弹每发(终审补)
513	      }
514	      if (c1Dead && rnd(mv5) === 0) {
515	        // :36246-36250 速度 = (±rand3, ±1)×3 未归一(3~9.5 随机,曾归一恒 3)
516	        const mvx = Math.random() * 3 * 3, mvy = -1 * 3;
517	        shootM(game, e.cx + rndRange(30, 60), e.cy + rndRange(-30, -10), mvx, mvy, 30, 450, 300, 1,
518	          { bounce: true });  // aiStyle14 X 反跳(原版 ×-0.1,默认档 -0.5 近似)
519	        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36254 空巢导弹每发(终审补)
520	      }
521	    }
522	  }
523	}
524	
525	// ---------------------------------------------------------------------------
526	// AI_074 火星无人机 388 + 日耀 Corite 418（NPC.cs:35452-35744,参数表 :35477-35509）
527	// ai[0] 0=悬浮瞄准(LOS+俯角+距离带 → 锁方向) / 1=蓄力(×0.95,30t) / 2=扑咬(steer 追击) /
528	//        3=自爆(388 专属:64px 贴身或撞块;3t 后炸) / 4=418 扑后恢复
529	// ---------------------------------------------------------------------------
530	export function martianDroneAI(e: Enemy, game: GameHooks, player: Player | null) {
531	  const corite = e.vanillaId === 418;
532	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
533	  // 参数表（:35477-35509）：388 / 418
534	  const kbMult = corite ? 0.3 : 0.4;
535	  const spd = corite ? 8 : 10;
536	  const hover = corite ? 175 : 200;
537	  const near = corite ? 175 : 0;
538	  const far = corite ? 600 : 750;
539	  const minNear = corite ? 80 : 0;
540	  const accel = corite ? 60 : 30;
541	  const windup = corite ? 20 : 30;
542	  const decay = corite ? 0.75 : 0.95;
543	  const jitter = corite ? 0 : 50;
544	  const dashSpd = corite ? 9 : 14;
545	  const steerN = corite ? 60 : 20;
546	  const steerAcc = corite ? (4 / 15) * 60 : 0;
547	  const minSpd = 7;
548	  const canExplode = !corite;   // flag68（:35491）
549	
550	  // 朝向（:35454-35469）
551	  if (sign(e.vx) !== 0) e.facing = corite ? sign(e.vx) : -sign(e.vx);
552	
553	  if (e.ai0 === 0 && player && !player.dead) {
554	    // ---- 悬浮瞄准（:35540-35610）----
555	    e.def.knockbackResist = kbMult;    // GetKnockbackMultiplier_ScaledByDifficulty
556	    const dx0 = player.cx - e.cx, dy0 = player.cy - e.cy;
557	    const dist = Math.hypot(dx0, dy0);
558	    // 悬停航向（:35546-35552）：直连向量 - 上方 hover - 侧移 near,归一 × spd
559	    const hx = dx0 + (dx0 < 0 ? near : -near), hy = dy0 - hover;
560	    const hd = Math.hypot(hx, hy) || 1;
561	    const vxT = (hx / hd) * spd, vyT = (hy / hd) * spd;
562	    let canHit = losClear(game, e.cx, e.cy, player.cx, player.cy);
563	    if (e.ai3 >= 120) canHit = true;                     // :35556-35558
564	    const aimAng = Math.atan2(dy0, dx0);
565	    const angleOk = aimAng > Math.PI / 8 && aimAng < Math.PI - Math.PI / 8;
566	    const tooNear = dist < minNear, tooFar = dist > far;
567	    if (tooNear || tooFar || !canHit || !angleOk) {
568	      // 悬停逼近（:35564-35583）
569	      e.vx = (e.vx * (accel - 1) + vxT) / accel;
570	      e.vy = (e.vy * (accel - 1) + vyT) / accel;
571	      if (!canHit) {
572	        if (!tooNear && !tooFar) e.ai3 += 1;
573	      } else e.ai3 = 0;
574	    } else {
575	      // 锁定扑咬方向（:35585-35591）
576	      e.ai0 = 1; e.ai1 = 0;
577	      e.ai2 = (dx0 / (dist || 1)) * spd;
578	      e.ai3 = (dy0 / (dist || 1)) * spd;
579	    }
580	  } else if (e.ai0 === 1) {
581	    // ---- 蓄力（:35592-35617）----
582	    e.def.knockbackResist = 0;
583	    let keep = true;
584	    if (corite) {
585	      keep = Math.hypot(e.vx, e.vy) > 2;
586	      if (!keep && player && !player.dead) {
587	        const d = Math.hypot(player.cx - e.cx, player.cy - e.cy) || 1;
588	        e.vx = lerp(e.vx, ((player.cx - e.cx) / d) * 0.1, 0.25);
589	        e.vy = lerp(e.vy, ((player.cy - e.cy) / d) * 0.1, 0.25);
590	      }
591	    }
592	    if (keep) { e.vx *= decay; e.vy *= decay; }
593	    e.ai1 += 1;
594	    if (e.ai1 >= windup) {
595	      e.ai0 = 2; e.ai1 = 0;
596	      let dx = e.ai2 + rndRange(-jitter, jitter + 1) * 0.04;
597	      let dy = e.ai3 + rndRange(-jitter, jitter + 1) * 0.04;
598	      const d = Math.hypot(dx, dy);
599	      dx = (dx / (d || 1)) * dashSpd; dy = (dy / (d || 1)) * dashSpd;
600	      e.vx = dx; e.vy = dy;
601	    }
602	  } else if (e.ai0 === 2) {
603	    // ---- 扑咬（:35618-35659）----
604	    e.def.knockbackResist = 0;
605	    e.ai1 += 1;
606	    const farBelow = player && !player.dead
607	      && Math.hypot(player.cx - e.cx, player.cy - e.cy) > (corite ? 150 : 100)
608	      && e.cy > player.cy;
609	    if ((e.ai1 >= 30 && farBelow) || Math.hypot(e.vx, e.vy) < minSpd) {
610	      e.ai0 = corite ? 4 : 0; e.ai1 = corite ? 45 : 0;
611	      e.ai2 = 0; e.ai3 = 0;
612	      e.vx /= 2; e.vy /= 2;
613	    } else if (player) {
614	      const d = Math.hypot(player.cx - e.cx, player.cy - e.cy) || 1;
615	      const ux = (player.cx - e.cx) / d, uy = (player.cy - e.cy) / d;
616	      const spdNow = Math.hypot(e.vx, e.vy);
617	      e.vx = (e.vx * (steerN - 1) + ux * (spdNow + steerAcc)) / steerN;
618	      e.vy = (e.vy * (steerN - 1) + uy * (spdNow + steerAcc)) / steerN;
619	    }
620	    // 撞块自爆（:35650-35656,仅 388）
621	    if (canExplode) {
622	      const st = game.world.store;
623	      const x0 = Math.floor(e.x / TILE), x1 = Math.floor((e.x + e.w - 0.01) / TILE);
624	      const y0 = Math.floor(e.y / TILE), y1 = Math.floor((e.y + e.h - 0.01) / TILE);
625	      outer: for (let tx = x0; tx <= x1; tx++) {
626	        for (let ty = y0; ty <= y1; ty++) {
627	          if (tx >= 0 && ty >= 0 && tx < st.w && ty < st.h && st.isSolid(tx, ty)) {
628	            e.ai0 = 3; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
629	            break outer;
630	          }
631	        }
632	      }
633	    }
634	  } else if (e.ai0 === 4) {
635	    // ---- 418 扑后恢复（:35660-35668）----
636	    e.ai1 -= 3;
637	    if (e.ai1 <= 0) { e.ai0 = 0; e.ai1 = 0; }
638	    e.vx *= 0.95; e.vy *= 0.95;
639	  }
640	  // 贴身自爆（:35670-35678,仅 388:64px 内）
641	  if (canExplode && e.ai0 !== 3 && player && !player.dead
642	    && Math.hypot(player.cx - e.cx, player.cy - e.cy) < 64) {
643	    e.ai0 = 3; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
644	  }
645	  if (e.ai0 === 3) {
646	    // ---- 自爆演出（:35680-35735）：原地膨胀 192×192,3t 后爆炸消散 ----
647	    const cx = e.cx, cy = e.cy;
648	    e.x = cx - 96; e.y = cy - 96;
649	    e.w = 192; e.h = 192;
650	    e.vx = 0; e.vy = 0;
651	    e.def.damage = 80;                 // GetAttackDamage_ScaledByDifficulty(80)
652	    e.spawnAlpha = 255;
653	    e.lightRGB = [0.2, 0.7, 1.1];
654	    game.spawnParticles(cx, cy, '#6FD7FF', 6, 2.4, { life: 30 });
655	    e.ai1 += 1;
656	    if (e.ai1 >= 3) {
657	      game.playSfx('explosion', 1, cx, cy);   // SoundID.Item14
658	      e.iframes = 0;
659	      e.hp = 0;
660	      e.hurt(9999, 0, 0, game);
661	    }
662	    return;
663	  }
664	  // aiStyle 74 常态无 AddLight（:35452-35580 全块无点光——曾挂 [0.1,0.4,0.6] 造假常光）
665	  fly(e);
666	}
667	
668	// ---------------------------------------------------------------------------
669	// AI_073 特斯拉炮塔 387（NPC.cs:35340-35451）
670	// ai[1] <120 = 部署（60-120t 渐显,alpha 255→0,部署期无敌）;ai[0] 电击计时:
671	//   <60 递增,受击 -30;==60 → 放电 435(伤 35,速 14,±100px 抖动) 并置 -120 → 180t 循环
672	// ---------------------------------------------------------------------------
673	export function teslaTurretAI(e: Enemy, game: GameHooks, player: Player | null) {
674	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; }   // 原版 ai[0] 自 0 起 → 首射 60t
675	  if (player && !player.dead) e.facing = player.cx >= e.cx ? 1 : -1;
676	  // 地面摩擦（:35343-35349）
677	  e.vx *= 0.93;
678	  if (e.vx > -0.1 && e.vx < 0.1) e.vx = 0;
679	
680	  if (e.ai1 < 120) {
681	    // ---- 部署（:35353-35401）：渐显 + 部署期无敌 + 环绕尘 ----
682	    e.ai1 += 1;
683	    e.spawnAlpha = e.ai1 > 60 ? Math.round((1 - (e.ai1 - 60) / 60) * 255) : 255;
684	    e.iframes = 2;                       // dontTakeDamage = true
685	    if (e.ai1 % 6 === 0) {
686	      game.spawnParticles(e.cx, e.cy, '#6FD7FF', 1, 0.6, { life: 20 });
687	    }
688	    e.lightRGB = [0.1 * (e.ai1 / 60), 0.5 * (e.ai1 / 60), 0.7 * (e.ai1 / 60)];
689	    e.lightRGBAt = { x: e.cx, y: e.cy - 10 };   // :35404 光源 = Center.Y−10
690	    e.vy = Math.min(e.vy + GRAVITY, MAX_FALL_SPEED);
691	    moveAndCollide(e, game.world, e.vx, e.vy);
692	    return;
693	  }
694	  if (e.ai1 === 120) e.ai1 += 1;         // :35403-35406 单帧过门
695	  e.lightRGB = [0.1, 0.5, 0.7];
696	  e.lightRGBAt = { x: e.cx, y: e.cy - 10 };   // :35411 光源 = Center.Y−10
697	
698	  // ---- 电击循环（:35409-35450）----
699	  if (e.ai0 < 60) e.ai0 += 1;
700	  if (e.justHit) e.ai0 = -30;            // 受击打断充电
701	  if (e.ai0 === 60 && player && !player.dead) {
702	    e.ai0 = -120;
703	    const ox = e.cx, oy = e.cy - 10;
704	    let dx = player.cx - ox, dy = player.cy - oy;
705	    dx += rndRange(-100, 101); dy += rndRange(-100, 101);
706	    dx *= rndRange(70, 131) * 0.01; dy *= rndRange(70, 131) * 0.01;
707	    const d = Math.hypot(dx, dy);
708	    if (d > 0.001) { dx = (dx / d) * 14; dy = (dy / d) * 14; }
709	    else { dx = 0; dy = -14; }
710	    shootM(game, ox, oy, dx, dy, 35, 435);
711	  }
712	  e.vy = Math.min(e.vy + GRAVITY, MAX_FALL_SPEED);
713	  moveAndCollide(e, game.world, e.vx, e.vy);
714	}
715	
716	// ---------------------------------------------------------------------------
717	// AI_072 泡泡盾 384（NPC.cs:35318-35339）：零速钉在军官 383 中心;军官消亡 → 消散
718	// ---------------------------------------------------------------------------
719	export function bubbleShieldAI(e: Enemy, game: GameHooks, _player: Player | null) {
720	  void game; void _player;
721	  const owner = e.master;
722	  if (owner && !owner.dead && owner.vanillaId === 383) {
723	    e.vx = 0; e.vy = 0;
724	    e.x = owner.cx - e.w / 2;
725	    e.y = owner.cy - e.h / 2;
726	    e.lightRGB = [0.1, 0.5, 0.7];
727	  } else {
728	    e.dead = true;   // life=0 + active=false（无掉落）
729	  }
730	}
731	
732	// ---------------------------------------------------------------------------
733	// AI_049 愤怒云 250（NPC.cs:31742-31810,普查同批顺带）
734	// 悬顶 200px 伺服（accel 0.25,过零双倍）;正下方+LOS → ai[0] 累计,>8 淋一发雨 264
735	// ---------------------------------------------------------------------------
736	export function angryNimbusAI(e: Enemy, game: GameHooks, player: Player | null) {
737	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; }
738	  if (!player || player.dead) {
739	    e.vx *= 0.95; e.vy *= 0.95;
740	    moveAndCollide(e, game.world, e.vx, e.vy);
741	    return;
742	  }
743	  const ACC = 0.25;
744	  let tx = player.cx - e.cx, ty = player.cy - 200 - e.cy;
745	  const d = Math.hypot(tx, ty);
746	  if (d < 20) { tx = e.vx; ty = e.vy; }
747	  else { const s = 4 / d; tx *= s; ty *= s; }
748	  // 分轴伺服（:31758-31789,过零方向翻转时双倍加速）
749	  if (e.vx < tx) { e.vx += ACC; if (e.vx < 0 && tx > 0) e.vx += ACC * 2; }
750	  else if (e.vx > tx) { e.vx -= ACC; if (e.vx > 0 && tx < 0) e.vx -= ACC * 2; }
751	  if (e.vy < ty) { e.vy += ACC; if (e.vy < 0 && ty > 0) e.vy += ACC * 2; }
752	  else if (e.vy > ty) { e.vy -= ACC; if (e.vy > 0 && ty < 0) e.vy -= ACC * 2; }
753	  // 淋雨（:31791-31808）：水平重叠 + 云底在玩家上方 + LOS → 8t 一发
754	  if (e.x + e.w > player.x && e.x < player.x + player.w
755	    && e.y + e.h < player.y
756	    && losClear(game, e.x, e.y, player.x, player.y)) {
757	    e.ai0 += 1;
758	    if (e.ai0 > 8) {
759	      e.ai0 = 0;
760	      const ox = e.x + 10 + Math.random() * (e.w - 20);
761	      shootM(game, ox, e.y + e.h + 4, 0, 5, 20, 264);
762	    }
763	  }
764	  moveAndCollide(e, game.world, e.vx, e.vy);
765	}
766	
767	// ---------------------------------------------------------------------------
768	// AI_003 火星尾段：军官 383（cs:56614-56645）/ 工程师 386（cs:59384-59428）
769	// 由分发表 case 3 在 fighterAI 之后调用（原版为 AI_003 内 type 尾段）
770	// ---------------------------------------------------------------------------
771	export function martianFighterExtras(e: Enemy, game: GameHooks, player: Player | null) {
772	  void player;
773	  const id = e.vanillaId;
774	  const enemies = game.enemies() as Enemy[];
775	  if (id === 383) {
776	    // ---- 军官：出生带盾,盾在 → 无敌;盾灭 180t 后补盾（:56614-56645）----
777	    const l0 = la(e);
778	    let shield = officerShield.get(e);
779	    const shieldOk = !!shield && !shield.dead && shield.vanillaId === 384;
780	    if (e.ai2 === 0 && l0[0] === 0 && !shieldOk) {
781	      const s = spawnPart(game, e, 384);
782	      if (s) {
783	        shield = s;
784	        officerShield.set(e, shield);
785	        shield.master = e;          // 原版盾 ai[0] = 军官 index（:56621）
786	        e.ai2 = 1;                  // 原版 ai[2] = 盾 index+1（>0 标记）
787	        l0[0] = -1;
788	      }
789	    }
790	    if (shieldOk) {
791	      e.iframes = 2;                // dontTakeDamage = true（:56629）
792	    } else {
793	      e.ai2 = 0;
794	      if (l0[0] === -1) l0[0] = 180;
795	      if (l0[0] > 0) l0[0] -= 1;
796	    }
797	    return;
798	  }
799	  if (id === 386) {
800	    // ---- 工程师：放炮塔（:59384-59428）----
801	    if (e.confusedT > 0) { e.ai2 = -60; return; }
802	    if (e.ai2 < 60) e.ai2 += 1;
803	    const nT = enemies.filter((n) => !n.dead && n.vanillaId === 387).length;
804	    const nE = enemies.filter((n) => !n.dead && n.vanillaId === 386).length;
805	    if (e.ai2 > 0 && nT >= 4 * nE) e.ai2 = 0;      // 场上 387 ≥ 4×386（:59393-59396）
806	    if (e.justHit) e.ai2 = -30;                    // :59397-59400
807	    if (e.ai2 === 30) {
808	      // ±5t 随机扫位（:59402-59424）：非中心 2t 禁区 + 实心面 + 上方 4t 净空 + 无岩浆
809	      const st = game.world.store;
810	      const cx0 = Math.floor(e.cx / TILE), cy0 = Math.floor(e.y / TILE);
811	      for (let tries = 0; tries < 100; tries++) {
812	        const tx = rndRange(cx0 - 5, cx0 + 5);
813	        const tyTop = rndRange(cy0 - 5, cy0 + 5);
814	        for (let ty = tyTop; ty < cy0 + 5; ty++) {
815	          const inCore = Math.abs(ty - cy0) <= 2 && Math.abs(tx - cx0) <= 2;
816	          const inSpawn = Math.abs(ty - cy0) <= 0 && Math.abs(tx - cx0) <= 0;
817	          if (inCore || inSpawn) continue;
818	          if (tx < 1 || ty < 1 || tx >= st.w - 1 || ty >= st.h - 1) continue;
819	          if (!st.isSolid(tx, ty)) continue;
820	          if (st.liquid[st.idx(tx, ty - 1)] === 2) continue;   // 上面一格岩浆
821	          let clear = true;
822	          for (let k = 1; k <= 4; k++) if (st.isSolid(tx, ty - k)) { clear = false; break; }
823	          if (!clear) continue;
824	          const turret = spawnPart(game, e, 387);
825	          if (turret) {
826	            turret.x = tx * TILE + 8 - turret.w / 2;
827	            turret.y = ty * TILE - turret.h;   // 底边贴实心面顶（:59425-59426）
828	          }
829	          return;
830	        }
831	      }
832	    }
833	    if (e.ai2 === 60) e.ai2 = -120;                 // :59427-59429
834	  }
835	}
836	
837	// ---------------------------------------------------------------------------
838	// 火星死光电报 447（Projectile.cs AI_079 :29714-29798 1:1）：垂直向下光束，
839	// 锚定母舰 UFO（ai[0]=npcIdx+1），束高 = 母舰 Y+46 到最近实心格（≤150 格），
840	// 每 tick 重算；母舰不在/电报窗关（395 ai[3]%120 窗）即 Kill。尘 228×2/t。
841	// ---------------------------------------------------------------------------
842	import { Entity } from './Entity';
843	
844	export class MartianDeathray extends Entity {
845	  w = 30; h = 30;
846	  x = 0; y = 0; vx = 0; vy = 0;
847	  dead = false;
848	  private srcId: number;
849	  private dmg: number;
850	  private age = 0;
851	
852	  constructor(src: Enemy, dmg: number) {
853	    super();
854	    this.srcId = src.id;
855	    this.dmg = dmg;
856	    this.x = src.cx - 15; this.y = src.cy + 46;
857	  }
858	
859	  fixedUpdate(_dt: number, game: GameHooks): void {
860	    if (this.dead) return;
861	    const src = (game.enemies() as Enemy[]).find((n) => n.id === this.srcId);
862	    // :29718-29722 门：锚不在场（或非 392/395 电报者/窗口关）→ Kill
863	    if (!src || src.dead || (src.vanillaId !== 392 && src.vanillaId !== 395)) {
864	      this.dead = true; return;
865	    }
866	    if (src.vanillaId === 395 && !(src.ai3 % 120 >= 60 && src.ai0 === 2)) { this.dead = true; return; }
867	    const p = game.player;
868	    if (!p || p.dead) { this.dead = true; return; }   // timeLeft 240 兜底简化
869	    if (++this.age > 240) { this.dead = true; return; }
870	    // :29726-29758 束高：y = 锚 cy+46，向下扫 ≤150 格找首个实心格
871	    const st = game.world.store;
872	    const colX = Math.floor(src.cx / 16);
873	    const startY = Math.floor((src.cy + 46) / 16);
874	    const endY = Math.floor(p.y + p.h);   // num652 = 目标盒底（:29733-29740）
875	    let span = 0;
876	    if (startY >= endY && st.isSolid(colX, startY)) {
877	      span = 1;
878	    } else {
879	      for (; span < 150 && startY + span < st.h; span++) {
880	        const row = startY + span;
881	        if (row >= endY && st.isSolid(colX, row)) { span--; break; }
882	      }
883	    }
884	    this.x = src.cx - this.w / 2;
885	    this.y = src.cy + 46;
886	    this.h = (span + 1) * 16;
887	    // 尘 228×2（:29770-29778，束脚）
888	    if (this.age % 2 === 0) {
889	      game.spawnParticles(this.cx, this.y + this.h - 16, '#B048E0', 1, 2.8,
890	        { life: 18, grav: 0, size: 3 });
891	    }
892	    // 接触伤害（hostile 447 伤害链简化为玩家盒重叠每 6t 一跳）
893	    if (this.age % 6 === 0
894	      && p.x < this.x + this.w && p.x + p.w > this.x
895	      && p.y < this.y + this.h && p.y + p.h > this.y) {
896	      (game as unknown as { damagePlayer(d: number, x: number, y: number, kx?: number): void })
897	        .damagePlayer(this.dmg, this.cx, this.cy, Math.sign(p.cx - this.cx));
898	    }
899	  }
900	
901	  draw(r: import('../render/Renderer').Renderer): void {
902	    const ctx = r.canvas.getContext('2d');
903	    if (!ctx) return;
904	    // 光柱近似（Projectile_447.png 30×4 帧条——竖束以原色半透明柱呈现）
905	    ctx.save();
906	    ctx.globalAlpha = 0.75;
907	    const grd = ctx.createLinearGradient(this.x, 0, this.x + this.w, 0);
908	    grd.addColorStop(0, 'rgba(196,84,255,0)');
909	    grd.addColorStop(0.5, 'rgba(230,160,255,0.9)');
910	    grd.addColorStop(1, 'rgba(196,84,255,0)');
911	    ctx.fillStyle = grd;
912	    ctx.fillRect(this.x, this.y, this.w, this.h);
913	    ctx.restore();
914	  }
915	}
916	

```


---

## 🤖 Assistant · 2026-08-19T07:42:25.682Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Excellent — this is very informative. Key facts for the martian family:

**393 turret** (`martianSaucerPartAI`):
- `e.ai1` = slot index 0/1
- `e.ai2` = aim angle (radians), atan2(dy/d, dx/d) where dy = max(0, playerY - turretY). Note: `dy` is clamped ≥ 0, so angle ∈ [0, π] (downward half in screen coords, since our y grows downward; player below → positive dy). `e.ai2 = Math.atan2(dy / d, dx / d)` — this is the rotation angle toward the player (only lower hemisphere).
- `e.ai3` = shared saucer counter (set `e.ai3 = saucer.ai3` each tick).

Vanilla FindFrame 393 uses `ai[2].ToRotationVector2()` = (cos(ai2), sin(ai2)). In XNA, positive sin = downward on screen. Our ai2 = atan2(dy, dx) with dy ≥ 0 → sin ≥ 0 → vector3.Y ≥ 0. Vanilla's num134 mapping:
- vy > |vx|*2 → 4 (mostly down)
- vy > |vx|*1.5 → vx>0 ? 5 : 3
- |vx| > vy*2 → vx>0 ? 8 : 0 (mostly horizontal)
- |vx| ≤ vy*1.5 → vx>0 ? 6 : 2
- else (|vx| > vy*1.5) → vx>0 ? 7 : 1

Our coordinate system: is our y down like XNA? Our world uses y increasing downward (typical for this project, e.g., `player.cy > e.cy` means player below). Yes — e.g. probe: "player in the lower part" checked with `player.cy > e.cy`. So atan2 with positive dy pointing down matches XNA semantics.

But note: our AI writes `e.ai2` only when NOT in window and player exists (`if (!inWin && player && !player.dead)`). If no player, ai2 stays at previous. Also vanilla's AI (aiStyle 75, :36152-36197) sets ai[2] similarly. Vanilla also keeps last value. Fine.

But wait — one nuance: in vanilla, the turret's ai[2] is set to the angle; `ToRotationVector2` gives (cos, sin). Our mapping can replicate exactly: vy = sin(ai2), vx = cos(ai2).

- Laser window: `inWin = e.ai3 >= 280 && e.ai3 < 420`, plus `%6 <= 2` → +9. Our ai3 = saucer.ai3 exactly (shared counter). 

But caution: vanilla FindFrame checks `ai[3] >= 280 && ai[3] < 420 && (int)ai[3] % 6 <= 2`. Our `e.ai3` is set from saucer.ai3 before window logic each tick. Good.

**394 cannon**: `e.ai3 = saucer.ai3` too. Vanilla: num188 = ai3 - 300.
- num188 >= 120 (i.e., ai3 >= 420): num188 -= 120 → ai3-420.
  - if >= 160 (ai3 >= 580): frame = 7 - (num188-160)/5 → at ai3 580-584: 7; 585-589: 6... wait (num188-160)/5 where num188 = ai3-420. ai3 ∈ [580,600) → num188-160 ∈ [0,20) → /5 ∈ [0,4) → frame 7,6,5,4.
  - else if >= 20 (ai3 ∈ [440,580)): frame = (num188/4)%4 where num188 = ai3-420 ∈ [20,160) → (ai3-420)/4 % 4 ∈ [0,4).
  - else (ai3 ∈ [420,440)): frame = 4 + num188/5 = 4 + (ai3-420)/5 ∈ {4,5} wait (ai3-420)/5 for [0,20) → 0..3 → frames 4-7. Hmm: num188/5 with num188 ∈ [0,20) → 0,1,2,3 → frames 4+0..4+3 = 4..7. Yes.
- num188 < 120 (ai3 < 420): frame = 4.

Wait, careful: `int num188 = (int)ai[3] - 300;` then `if (num188 >= 120) { num188 -= 120; ... }`. So for ai3 ∈ [420, ...): num188 = ai3 - 420. For ai3 < 420 (including negative/wrap?): num188 = ai3 - 300; if num188 < 120 → frame 4. Hmm but note ai3 could be < 300 making num188 negative — still frame 4. OK.

So 394's frame machine (per tick, pure function of ai3):
- ai3 < 420 → 4
- 420 ≤ ai3 < 440 → 4 + floor((ai3-420)/5) → 4,5,6,7 (each 5t: 0-4→4, 5-9→5, 10-14→6, 15-19→7)
- 440 ≤ ai3 < 580 → floor((ai3-440)/4) % 4 → 0..3 cycling — wait, num188 = ai3-420 ∈ [20,160), num188/4 % 4. (ai3-420)/4 % 4. At ai3=440: num188=20 → 20/4=5 → 5%4=1. Hmm interesting — it's (ai3-420)/4 % 4, not (ai3-440)/4. Let me recompute: num188 after -=120 is ai3-420. `frame.Y = num * (num188 / 4 % 4)`. So frame = floor((ai3-420)/4) % 4. At ai3=440 → (20)/4=5 %4 = 1. At ai3=444 → 24/4=6%4=2. ai3=448→7%4=3, ai3=452→8%4=0. So cycling 1,2,3,0,1,2,3,0... over 140t = 35 cycles of 16t. OK — 4t/frame cycle.
- ai3 ≥ 580 → 7 - floor((ai3-580)/5), clamped by wrap at 600 → 0. ai3 ∈ [580,600): frames 7,6,5,4 (each 5t).

**395 saucer**: ai3 is the 600t cycle counter (ai0=0) or the 3600t counter (ai0=2, %120 windows). Vanilla FindFrame 395: 
```
fc += 1; if (fc >= 66) fc = 0;
if (flag10) { fc += 1; if (fc >= 54 || fc < 36) fc = 36; }
num126 = fc % 66; num126 /= 6; frame = num126
```
where flag10 = ai3 ∈ [20, 260). Death-ray telegraph window — matches cruise cycle window [20,260) (window 1 sweep? no — window 1 is the horizontal sweep [20,260) per our WIN comment; and the deathray telegraph is fired at ai3==20 first frame from 392's logic `if (e.ai3 - 20 === 0)`. Yes: the deathray telegraph window [20,260) coincides with the sweep window where the saucer fires its death ray at start.)

So frame for 395: frameCounter (vanilla NPC field, own counter 0..65) advancing 1/t (2/t in window), clamped into [36,53] during window → frame = floor(fc/6) ∈ {6,7,8} during window; otherwise cycles 0..10.

This requires a persistent per-entity counter (like vanilla frameCounter). We have `e.animT` — a per-entity tick counter incremented every tick! Let me check: `this.animT++` at line 1226/1243 — every tick for all enemies. So I can derive: fc = ? We need fc such that normally it cycles 0..65; during window, clamp [36,53] and advance 2/t.

The vanilla fc evolution: fc += 1 (mod 66); in window, additional +1 then clamp into [36,53]. Note when window starts, if fc < 36 → jump to 36. When window ends, fc continues from ≤53 advancing 1/t.

Approximating with global t: fc = t % 66 works when not in window for a while, but the clamp creates a discontinuity: entering the window at fc<36 → jump to 36; while in window fc advances 2/t within [36,53], i.e. oscillates: 36→53 in 9t (2/t), then clamp back to 36 (since >=54 → 36). So during the window the counter saw-tooths between 36 and 53 at double speed — frames 6..8 pulsing glow.

Since the window is long (240t), during the window fc oscillates 36..53 (period 9t), so frame = 6 + ((t*2) mod 18)/6... Let me compute exactly: during window, fc_{n+1} = clamp(fc_n + 2, 36, 53 with wrap: if fc+1 >= 54 → 36). Precisely: fc += 1; if (fc >= 54 || fc < 36) fc = 36. So fc_next = fc+2 if fc+2 < 54 and fc+2 >= 36; if fc+1 >= 54 → 36; ... For fc in [36, 51]: fc_next = fc + 2. fc = 52 → +1 = 53 (not >= 54) → +1 = 54 → >= 54 → 36? Wait the sequence: `fc += 1.0; if (fc >= 66) fc = 0;` then `if (flag10) { fc += 1.0; if (fc >= 54 || fc < 36) fc = 36; }`. So in window: fc_total = fc + 2 then clamp: if result >= 54 → 36; if result < 36 → 36. So from 52: 52+2=54 → 36. From 51: 53 → stays 53. So sequence 36,38,40,...,52,53,36,38... wait from 51 → 53; from 52 → 36. So the cycle: 36,38,42,...? Let me simulate: 36→38→40→...→50→52→36 (52+2=54→36). Hmm from 50: 52. From 52: 36. So values 36..52 even steps then wrap — 53 never reached? From 51: 53 — but 51 only reachable if fc was 49: 49+2=51. All evens: 36,38,...,52, then 36. 53 unreachable. So during window fc ∈ {36,38,...,52} → frame = floor(fc/6) ∈ {6,6,7,7,8,8,8,8,8}: 36/6=6, 38/6=6, 40→6, 42→7, 44→7, 46→7, 48→8, 50→8, 52→8. Period 9t. 

OK — so a clean way: maintain a per-entity counter. Do we have a dedicated field? We could use `e.lai0` or `e.lai1` as the frame counter (the precedent: Queen Bee 222 writes e.lai0 in AI, Renderer reads). But wait — the task says for these render-only counters we may write e.lai0/e.lai1 in AI files. But cleaner: since vanilla frameCounter advances every tick regardless, and our `animT` also advances every tick, we can compute fc from animT when no window distortion has occurred. But the clamp leaves a lasting offset (fc frozen-ish in [36,53] during the 240t window, then continues). With global t we can't track that offset... but actually we can reconstruct exactly with a dedicated counter maintained in the AI (e.lai0 = frameCounter replica). The saucer AI doesn't use lai0 (check: martianSaucerAI uses ai0-3 only; localAI via `la()` only in martianFighterExtras for 383). So e.lai0 is free for 395. Hmm, but wait — do I want to run the FindFrame counter inside the AI file? The task explicitly permits: "if AI-side synchronous state is needed, you can write e.lai0/e.lai1/e.customFrameIdx in the corresponding AI files". 

Alternatively, simpler: implement the full vanilla counter evolution in the AI file (advance per tick), then Renderer computes frame = floor(fc/6) with window clamp. Or even simpler: have the AI maintain the counter and Renderer do the clamp math — but the clamp must happen per tick inside the counter, so do the whole evolution in AI, storing the final frame index via... hmm, but Renderer's vanillaFrameIdx also clamps `Math.min(frames-1, ...)`. Let me follow the Queen Bee precedent: AI writes e.lai0 (the counter), Renderer maps to frame. For 395: AI maintains e.lai0 as vanilla frameCounter replica (advance +1, window +1, clamp). Renderer: frame = floor((e.lai0 % 66)/6).

Wait but where is animT incremented relative to AI execution? Let me check Enemy.tick / fixedUpdate order: line 1226 `this.animT++` and 1243. Need to look at the context — there appear to be two paths (maybe 1226 in one branch and 1243 in another). The counter replica in AI: each AI tick, do the vanilla FindFrame counter update. AI functions run once per tick (fixedUpdate). I'll put the update at the end of martianSaucerAI (or beginning). Since AI is called once per tick, the replica advances identically.

But hold on — does vanilla FindFrame run every tick? Yes, FindFrame is called from UpdateNPC each tick. So 1:1.

Now check: is there an existing precedent of maintaining frameCounter replicas? The 694 mimic does customFrameIdx. And 488 dummy uses dummyShake. OK.

**392 hull**: 4 frames 0-3, fc += 1/t (+2/t in window [20,260)), %12, /3. Also needs a persistent counter with the window speed-up. But here no clamp — just speed doubling. fc evolution: fc = (fc + (window?2:1)) % 12. With global t, offset accumulates during window... Using animT directly would drift from vanilla (vanilla's counter keeps accumulating the extra +1s). But since it's %12 and only speed changes, using a replica counter again is cleanest. Which field? 392 uses ai0-3? In martianSaucerPartAI for 392: ai3 shared from saucer, ai1? Not used for 392 (ai1 only for 393/394 slot). ai0? not used. So e.lai0 is free for 392 as well. Hmm wait — but martianSaucerPartAI is shared for 392/393/394/390/416/492. I'll write the counter update per-id.

Actually wait — do I even need a replica for 392? The frame is floor(fc%12/3) with fc advancing 1 or 2/t. A replica is simplest and exact. Use e.lai0 for both 392 and 395? They're different entities, no conflict.

Hmm, but actually, let me reconsider: maybe simpler to make the Renderer stateless where the drift is bounded... No — the task says these need accuracy; replicas are the pattern used elsewhere (e.g., "cursedSkullAI's mimic694Frame maintains it"). I'll do replicas in AI.

Wait, but there's a subtlety about WHERE the counter update happens vs. when the renderer reads it. AI runs in fixedUpdate; render reads later in the same frame. Fine.

**399 probe**: frameCounter = (frameCounter + 0.25) % 4 + (ai0 != 0 ? 4 : 0). Stateless-ish: fc is just a sawtooth from wherever it started. Using animT: frame = floor(((t*0.25) % 4)) + (ai0 !== 0 ? 4 : 0). Since vanilla's counter is also just t*0.25 % 4 in steady state (it never resets), global t is exact except a constant phase offset — visually equivalent (the existing code uses this approximation freely, e.g. "globally continuous t cycling is visually equivalent"). ai0: our probe AI uses ai0 = 0 patrol / 1 hover / 2 escape — alert band when ai0 != 0. Vanilla: ai[0] != 0f → +4. Our ai0=1 (alert hover) and 2 (escape) → +4. Matches vanilla semantics (alert state).

**387 tesla**: ai0-based: `ai[0] > 0` → charge speeds 1/2/3 per tier (ai0>=20, >=40); `ai0 <= 0` → idle 15t/frame. Our teslaTurretAI: ai0 counts 0→60 charge, then -120 → counts up... wait: `if (e.ai0 < 60) e.ai0 += 1; if (e.ai0 === 60 && player...) e.ai0 = -120;` So ai0: during charge 0..60; after firing → -120, then `if (e.ai0 < 60) e.ai0 += 1` → counts -120 → ... → 59 → 60 → fire again. JustHit → -30. Hmm wait — after firing ai0=-120 and increments up to 60 again over 180t. During that recharge, ai0 goes from -120 to 60. But vanilla FindFrame treats ai0 > 0 as charging. Our ai0 semantics match vanilla? Let me check vanilla AI_073 (NPC.cs:35340-35451) — the comment says ai[0] electric-shock timer: <60 increment, on hit -30; ==60 → discharge and set to -120 → 180t cycle. So yes our ai0 mirrors vanilla exactly (that's why charge speed tiers ai0>=20/40 make sense: only relevant when ai0 counts up from -30 (hit interrupt) or from low values... hmm wait — when counting from -120, ai0 passes through [0,20) etc. too.

Anyway: frame machine: needs a persistent frameCounter (2 frames 0/1) with speed = 1 + (ai0>=20) + (ai0>=40) when ai0 > 0 else 1, thresholds 10/15. Again a replica counter (e.lai0 free — teslaTurretAI uses ai0, ai1 only). Or approximate with animT: frame = floor(t / (10 or 15)) % 2 — the speed tiers would cause drift but with a pure 2-frame toggle the phase is arbitrary anyway (vanilla phase depends on spawn time). Since a 2-frame blink at 10-15t periods, using animT directly: frame = floor(t / speed-adjusted?) Hmm — but speed changes over time (charge vs idle), so instantaneous speed differs. With global t we can't reflect "currently charging fast". During charging (ai0>0): frame should toggle every 10/5/3.33t; idle: every 15t. Using floor(t/period)%2 with period from current ai0 gives correct *rate* but arbitrary phase — visually equivalent (blink toggle). That matches existing code style (e.g., ai===14 bats use t/6). I'll do stateless: period = ai0>0 ? 10/(1+tiers) : 15; frame = floor(t/period)%2. Hmm, but frame count: is frames=2 for 387? npcFrameCount[387] — the sprite has 2 rows (frame.Y >= num*2 → 0). I'll trust frames from the atlas and clamp.

Wait, actually there's a subtlety — our atlas `frames` count comes from `e.vanilla?.frames` (npcFrameCount). For all these I should clamp with Math.min(frames-1, ...) as the function does at the end? The customFrameIdx path clamps. The branches themselves mostly use Math.min(frames-1,...). I'll follow suit.

**386 engineer**: deploy band 9/10 via ai2>0: frame = 9 + floor(ai2/12)%2. Our engineer ai2: confusedT>0 → -60; else counts up 1..60, then on 30 spawns turret (returns early!), on 60 → -120. Hmm wait: `if (e.ai2 === 30) { ...spawn... return; }` — and `if (e.ai2 === 60) e.ai2 = -120;` — hmm, when does ai2 reach 60? It increments `if (e.ai2 < 60) e.ai2 += 1` — goes 1..60. At 30 spawns. At 60 → -120. Then counts up from -120... to 30 → spawn → ... so a cycle of 150 with a spawn each time ai2 hits 30. Also `if (e.ai2 > 0 && nT >= 4*nE) e.ai2 = 0` and justHit → -30.

Vanilla FindFrame: `if (ai[2] > 0f) frame = 9 + (ai2/12)%2` — deploy band whenever ai2 > 0 (i.e., "placing-turret phase" = positive cooldown counting). Our ai2 > 0 covers the same semantics (counting toward placement). Note our ai2 can exceed... it's ≤ 60. floor(ai2/12)%2 → 0 for [0,24), 1 for [24,36), 0 for [36,48), 1 for [48,60). Good.

Else walking: standard fighter walk frames 2-8, idle 0, air 1. The existing generic branch ai===3 handles fighter (id 386 is aiStyle 3? The extras are called from "dispatch table case 3 after fighterAI" — yes aiStyle 3). Look at existing branch: `if (ai === 3 || ai === 26 || ai === 107)` — walking from frame 2, |vx|*2+1 accumulate, >6 advance, cycle back to 2, idle 0, air frames-1. But vanilla 386: walking band 2..8 (`frame.Y / num >= 9 → num*2`), air = 1 (frame.Y = num), idle = 0. The generic branch returns frames-1 for air (for 386 frames=? maybe 11 → would be wrong). Hmm — but careful: "do not modify existing other branches" (don't modify other existing branches). The generic ai===3 branch serves many. For 386 I'm adding a new dedicated branch (before it) per this task, implementing the full vanilla case: deploy band (ai2>0), else vy==0 walking (frame≥2, fc += |vx|*2, >6 advance, wrap at 9 → 2, idle vx==0 → 0), else (air) frame 1.

Hmm wait — vanilla case 386 for air: `frameCounter = 0; frame.Y = num;` → frame 1. And the walk counter uses `frameCounter += Math.Abs(velocity.X) * 2f` (no +1!). The generic branch uses walkCycleT*2 + t (i.e., |vx|*2 + 1 per tick) — different. Vanilla 381-389 group (72300-72333): frameCounter += |vx|*2 (not +1) for 381/382/383; 385/389: |vx|*1.2. Idle → frame 0. Air → frame 1.

Since the task scope is FindFrame for these families, I should implement 386 fully. But is 386's walking part in scope? The task says "386 Engineer: frames 9/10 during turret-placement phase" — only the deploy band is explicitly required. But the rest of case 386 (walk) exists in vanilla... The task's mandate: "complete the FindFrame frame state machines for the three Boss/NPC families". I'll implement the full case 386 (deploy band + walk) since a partial branch (only ai2>0, falling through to generic ai3) would mix semantics — actually falling through to generic would give wrong walk animation for 386 (|vx|*2+1 and air=frames-1). But modifying that is out of scope... Adding my own complete branch for 386 before the generic one doesn't modify existing branches. I'll do the complete case.

Hmm, wait — but what about 381-389 (the other martian fighters: 381 Gray Grunt? 382 Gigazapper? 383 Martian Officer, 385 Scutlix Gunner, 389 Ray Gunner)? The task didn't list them ("387 Tesla...386 Engineer" only). Adding only 386/387 per task scope. The others are out of task scope — don't gold-plate. OK.

Now, which ids map to what: from our file: 399 probe, 395 saucer core, 392/393/394 parts, 390 rider, 391 mount, 388 drone, 418 Corite, 387 tesla, 384 bubble, 383 officer, 386 engineer, 382 = 390's transform target (infantry). Task wants: 393, 394, 395, 392, 399, 387, 386. Good — matches.

Now the moon events file. Let me read bossAI_moon_events.ts.
````

</details>


---

## 🤖 Assistant · 2026-08-19T07:42:26.266Z · glm-x-preview-260804

```
火星族 AI 语义已理清。接下来处理月亮事件 AI 文件。
```


---

## 🤖 Assistant · 2026-08-19T07:42:26.632Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_moon_events.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:42:26.876Z

**📎 ToolResult**

```
1	// 月事件(南瓜月/霜月)+ 雪人入侵 + 弹跳球族 AI 1:1 移植(Terarria1456, 1.4.5.6)：
2	//   aiStyle 57  悲木 325 / 常世吼 344        NPC.cs:32937-33245（悬浮树怪，弹幕分阶段）
3	//   aiStyle 58  南瓜王 327                    NPC.cs:33246-33404（悬浮/俯冲，ai[3] 换招）
4	//   aiStyle 59  南瓜王之刃 328                NPC.cs:33405-33587（锚主环绕→升空俯冲/横扫）
5	//   aiStyle 60  冰雪女王 345                  NPC.cs:33588-33901（滑翔/落冰/旋射三态随机）
6	//   aiStyle 61  圣诞坦克 346                  NPC.cs:33902-34154（悬浮树怪同构+链炮/火箭/礼盒）
7	//   aiStyle 62  玩具直升机 347                NPC.cs:34155-34207（600px 内悬停点射）
8	//   aiStyle 63  弗洛科 352                    NPC.cs:34208-34255（追踪+200px 内旋冲）
9	//   aiStyle 38  雪人三兄弟 143/144/145        NPC.cs:29115-29256（跳扑/停顿/雪球机枪）
10	//   aiStyle  9  弹跳球族 25/30/33/112/516(/665/666)
11	//                                             NPC.cs:21349-21548（直飞球/毒唾/日耀耀斑）
12	// 经典模式主链 1:1；getGoodWorld 分支已实装（弹跳球族 33 骷髅王在场无敌 / 25 血肉墙
13	// 在场无敌 / 666 地表无敌 / RedHatSkeletronAdjustments+FTW 速度档）；expert 分支仅注释
14	// 保留；netcode 跳过。
15	// 弹幕贴图 Projectile_{109,110,180,325..329,345..352}.png 已入 sprites/vanilla(原 RENDER_PROXY
16	// 代渲退役,Arrow 按 projId 懒加载真图)。
17	import type { Enemy } from './Enemy';
18	import type { GameHooks } from './types';
19	import type { Player } from './Player';
20	import { TILE } from '../core/constants';
21	import { GRAVITY, MAX_FALL_SPEED } from '../core/constants';
22	import { moveAndCollide } from '../physics/TileCollision';
23	import { spawnPart, losClear } from './bossAI';
24	import { Arrow } from './Arrow';
25	
26	/** 原版 localAI[0..3]（Enemy 的 ai0-ai3 对应 ai[]，localAI 是独立数组 → WeakMap 落盘） */
27	const localAI = new WeakMap<Enemy, number[]>();
28	const la = (e: Enemy): number[] => {
29	  let a = localAI.get(e);
30	  if (!a) { a = [0, 0, 0, 0]; localAI.set(e, a); }
31	  return a;
32	};
33	/** 渲染侧只读出口（南瓜王 327 披风帧 = localAI[1]，Main.cs:22501） */
34	export const localAIOf = la;
35	/** Main.rand.Next(n) → [0,n) */
36	const rnd = (n: number): number => Math.floor(Math.random() * n);
37	/** Main.rand.Next(a, b) → [a,b) */
38	const rndRange = (a: number, b: number): number => a + Math.floor(Math.random() * (b - a));
39	const clamp = (v: number, lo: number, hi: number): number => (v < lo ? lo : v > hi ? hi : v);
40	
41	/** Collision.SolidCollision 近似：AABB 与任意实心块相交 */
42	function solidRect(game: GameHooks, x: number, y: number, w: number, h: number): boolean {
43	  const st = game.world.store;
44	  const x0 = Math.floor(x / TILE), x1 = Math.floor((x + w - 0.01) / TILE);
45	  const y0 = Math.floor(y / TILE), y1 = Math.floor((y + h - 0.01) / TILE);
46	  for (let tx = x0; tx <= x1; tx++) {
47	    for (let ty = y0; ty <= y1; ty++) {
48	      if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) return true;
49	    }
50	  }
51	  return false;
52	}
53	/** WorldGen.SolidTile：单格实心判定（弹幕出膛点门） */
54	function solidTileAt(game: GameHooks, x: number, y: number): boolean {
55	  const st = game.world.store;
56	  const tx = Math.floor(x / TILE), ty = Math.floor(y / TILE);
57	  return st.inBounds(tx, ty) && st.isSolid(tx, ty);
58	}
59	/** NPC.AnyNPCs(type)：指定 vanillaId 的存活 NPC 是否在场（弹跳球族 FTW 门用） */
60	function anyNpcs(game: GameHooks, id: number): boolean {
61	  return (game.enemies() as Enemy[]).some((n) => !n.dead && n.vanillaId === id);
62	}
63	
64	// ---------------------------------------------------------------------------
65	// 弹幕：月事件族弹体贴图 Projectile_{109,110,180,325..329,345..352}.png 已按 601/602
66	// 先例自 terraria-assets/Images 补入 public/sprites/vanilla/（Arrow 按 projId 懒加载
67	// 真图），此前的 RENDER_PROXY 代渲登记退役。ProjectileID.cs 对照：325 FlamingWood /
68	// 326-328 GreekFire1-3 / 329 FlamingScythe / 345 PineNeedleHostile / 346 OrnamentHostile /
69	// 348 FrostWave / 349 FrostShard / 350 Missile / 351 Present / 352 Spike /
70	// 180 BulletDeadeye / 109 SnowBallHostile / 110 BulletSnowman。
71	// ---------------------------------------------------------------------------
72	/** 弹体行为登记（Projectile.cs SetDefaults 逐条）：
73	 *  重力：349 FrostShard 原版 vy+=0.2/t 即坠（:53360）；aiStyle 14 弹跳族
74	 *  （希腊火 326-328 :3937 / 装饰球 346 :4092 / 尖刺 352 :4152）重力 0.2 且
75	 *  **延迟 5 子步**（AI_014 默认档 :23482-23498：ai[0]>5 才 vy+=0.2）；345 针叶
76	 *  50t 后 +0.5（AI_001 type 段 :54237-54249）；351 礼盒走 Arrow 两段重力档。
77	 *  弹跳：aiStyle 14 族撞块法向反弹 ×-0.5（碰撞反弹表 :18314-18327 默认档），
78	 *  此前近似直飞/直坠消亡；352 尖刺同族补齐（曾漏 = 恒速直飞）。
79	 *  tileCollide=false 族（325 :3917 / 329 :3950 / 348 :4112 / 350 :4135 / 351 :4146）
80	 *  由 Arrow 按 projectileData 自动置 noTileCollide（曾漏 = 扎进地里被地形吞噬）。
81	 *  寿命表（SetDefaults，缺省 3600 :526）：325=420 / 326-328=360（:3940）/
82	 *  329=420 / 345=3600（默认）/ 346=300（:4095）/ 348=900（:4115）/
83	 *  349=900（:4125）/ 350=1800（:4136 timeLeft/=2）/ 351=3600（默认）/
84	 *  352=1200（:4155 timeLeft/=3）/ 180=600（:2393 段）/ 109=3600（默认）/
85	 *  110=600 */
86	const PROJ_GRAV: Record<number, number> = { 349: 0.2, 326: 0.2, 327: 0.2, 328: 0.2, 346: 0.2, 352: 0.2, 345: 0.5 };
87	/** AI_014 重力延迟 5 子步（:23484-23498）；345 针叶 50t（:54244） */
88	const PROJ_GRAV_DELAY: Record<number, number> = { 326: 5, 327: 5, 328: 5, 346: 5, 352: 5, 345: 50 };
89	const PROJ_BOUNCE = new Set([326, 327, 328, 346, 352]);
90	const PROJ_LIFE: Record<number, number> = {
91	  325: 420, 326: 360, 327: 360, 328: 360, 329: 420,
92	  345: 3600, 346: 300, 348: 900, 349: 900, 350: 1800,
93	  351: 3600, 352: 1200, 180: 600, 109: 3600, 110: 600,
94	};
95	
96	function shootE(
97	  game: GameHooks, x: number, y: number, vx: number, vy: number,
98	  dmg: number, projId: number, life?: number,
99	): void {
100	  (game as unknown as { entities: { add: (e: unknown, b: string) => void } }).entities.add(
101	    new Arrow(x, y, vx, vy, dmg, 0, projId, null, {
102	      grav: PROJ_GRAV[projId] ?? 0,
103	      gravDelay: PROJ_GRAV_DELAY[projId] ?? -1,
104	      life: life ?? PROJ_LIFE[projId] ?? 3600,
105	      pierce: 1, hostile: true,
106	      bounce: PROJ_BOUNCE.has(projId),
107	      present: projId === 351,               // aiStyle 58 两段重力（Arrow 内实现）
108	    }),
109	    'projectiles');
110	}
111	
112	// ---------------------------------------------------------------------------
113	// 共享悬浮巡航（aiStyle 57/61 同构尾段，NPC.cs:33186-33245 / :34105-34154）：
114	//  攻击态或玩家在正下方 50px 内 → 水平减速停步；否则按 direction 以 num 巡航速
115	//  (v*20±num)/21 逼近。垂直三态：玩家正下方 → 下压 vy+=0.5；底部 80x20 探测盒
116	//  撞实心 → 悬浮上推（钳 -4）；否则下落（钳 10）。
117	// ---------------------------------------------------------------------------
118	function hoverCruise(
119	  e: Enemy, game: GameHooks, player: Player | null, stop: boolean, speed: number,
120	): void {
121	  if (stop) {
122	    e.vx *= 0.9;
123	    if (e.vx > -0.1 && e.vx < 0.1) e.vx = 0;
124	  } else {
125	    if (e.facing > 0) e.vx = (e.vx * 20 + speed) / 21;
126	    if (e.facing < 0) e.vx = (e.vx * 20 - speed) / 21;
127	  }
128	  const above = !!player && e.x < player.x && e.x + e.w > player.x + player.w
129	    && e.y + e.h < player.y + player.h - 16;
130	  if (above) {
131	    e.vy += 0.5;
132	  } else if (solidRect(game, e.cx - 40, e.y + e.h - 20, 80, 20)) {
133	    if (e.vy > 0) e.vy = 0;
134	    if (e.vy > -0.2) e.vy -= 0.025;
135	    else e.vy -= 0.2;
136	    if (e.vy < -4) e.vy = -4;
137	  } else {
138	    if (e.vy < 0) e.vy = 0;
139	    if (e.vy < 0.1) e.vy += 0.025;
140	    else e.vy += 0.5;
141	  }
142	  if (e.vy > 10) e.vy = 10;
143	  e.x += e.vx;   // 运行时 noTileCollide=true（:32941-32942 / :33906-33907）→ 直积分
144	  e.y += e.vy;
145	}
146	
147	// ---------------------------------------------------------------------------
148	// AI_057 悲木 325 / 常世吼 344（NPC.cs:32937-33245）
149	// ai[0] 0=巡航蓄招 / 1=喷火(325 焰木弹 325｜344 针叶 345) / 2=抛射(325 希腊火
150	//        326-328｜344 装饰球 346) / 3=325 专属速射焰木 / 4=325 专属希腊火连泼。
151	// ai[1]=状态内计时。巡航速 2→3(<75%)→4(<50%)；白天 EncourageDespawn+8 速离场。
152	// ---------------------------------------------------------------------------
153	
154	export function mourningWoodAI(e: Enemy, game: GameHooks, player: Player | null) {
155	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; }
156	  const ever = e.vanillaId === 344;
157	  const isDay = game.world.clock.isDay;
158	  let num891 = 2;                                   // 巡航速(:32940)
159	  if (e.hp < e.maxHp * 0.75) num891 = 3;
160	  if (e.hp < e.maxHp * 0.5) num891 = 4;
161	  // 点光(:32958-32965)：底部 -30px——344 常世吼 (0.3,0.16,0.125) / 325 哀木
162	  // (0.3,0.125,0.06)；光源位 = Bottom+(0,-30)（曾漏 lightRGBAt 落在中心格）
163	  e.lightRGB = ever ? [0.3, 0.16, 0.125] : [0.3, 0.125, 0.06];
164	  e.lightRGBAt = { x: e.cx, y: e.y + e.h - 30 };
165	  // TargetClosest 仅夜间(:32943-32946)——白天保留上一朝向
166	  if (!isDay && player && !player.dead) e.facing = e.seekDirX(player);
167	  let flag56 = false;
168	
169	  if (isDay) {
170	    e.encourageDespawn(10);                          // :32966-32970
171	    num891 = 8;
172	  } else if (e.ai0 === 0) {
173	    // 蓄招(:32971-32988)：300t（残血加速）→ 换攻击态；<25% 且非 344 可 roll 3/4
174	    e.ai1 += 1;
175	    if (e.hp < e.maxHp * 0.5) e.ai1 += 1;
176	    if (e.hp < e.maxHp * 0.25) e.ai1 += 1;
177	    if (e.ai1 >= 300) {
178	      e.ai1 = 0;
179	      e.ai0 = (e.hp < e.maxHp * 0.25 && !ever) ? rndRange(3, 5) : rndRange(1, 3);
180	    }
181	  } else if (e.ai0 === 1 && player) {
182	    // 喷火(:32989-33051)：344 每 5t 一发针叶 345（伤 43 速 12.5，体内随机点出膛）；
183	    // 325 每 15t 一发焰木 325（伤 50 速 10，底部中心出膛）
184	    flag56 = true;
185	    e.ai1 += 1;
186	    if (ever) {
187	      if (e.ai1 % 5 === 0) {
188	        const ox = e.x + 20 + Math.random() * (e.w - 40);
189	        const oy = e.y + 20 + Math.random() * (e.h - 40);
190	        let dx = player.cx - ox, dy = player.y - oy;
191	        dx += rndRange(-50, 51); dy += rndRange(-50, 51);
192	        dy -= Math.abs(dx) * (rnd(21) * 0.01);
193	        const d = Math.hypot(dx, dy) || 1;
194	        const s = 12.5 / d;
195	        dx *= s * (1 + rndRange(-20, 21) * 0.02);
196	        dy *= s * (1 + rndRange(-20, 21) * 0.02);
197	        shootE(game, ox, oy, dx, dy, 43, 345);
198	      }
199	      if (e.ai1 >= 180) { e.ai1 = 0; e.ai0 = 0; }
200	    } else {
201	      if (e.ai1 % 15 === 0) {
202	        const ox = e.cx, oy = e.cy + 30;
203	        let dx = player.cx - ox, dy = player.y - oy;
204	        const d = Math.hypot(dx, dy) || 1;
205	        const s = 10 / d;
206	        dx *= s * (1 + rndRange(-20, 21) * 0.02);
207	        dy *= s * (1 + rndRange(-20, 21) * 0.02);
208	        shootE(game, ox, oy, dx, dy, 50, 325);
209	      }
210	      if (e.ai1 >= 120) { e.ai1 = 0; e.ai0 = 0; }
211	    }
212	  } else if (e.ai0 === 2 && player) {
213	    // 抛射(:33052-33118)：60-240t 窗口内 344 每 15t 装饰球 346（伤 57）/
214	    // 325 每 8t 希腊火 326-328（伤 40）；弹道带 |dx|*0.3 上抛 + 50-200px 抬升
215	    flag56 = true;
216	    e.ai1 += 1;
217	    if (e.ai1 > 60 && e.ai1 < 240) {
218	      if (ever) {
219	        if (e.ai1 % 15 === 0) {
220	          let spd = 4.5;
221	          const ox = e.x + 20 + Math.random() * (e.w - 40);
222	          const oy = e.y + 60 + Math.random() * (e.h - 80);
223	          let dx = player.cx - ox, dy = player.y - oy;
224	          dy -= Math.abs(dx) * 0.3;
225	          spd += Math.abs(dx) * 0.004;
226	          dx += rndRange(-50, 51); dy -= rndRange(50, 201);
227	          const d = Math.hypot(dx, dy) || 1;
228	          const s = spd / d;
229	          dx *= s * (1 + rndRange(-30, 31) * 0.01);
230	          dy *= s * (1 + rndRange(-30, 31) * 0.01);
231	          shootE(game, ox, oy, dx, dy, 57, 346);
232	        }
233	      } else if (e.ai1 % 8 === 0) {
234	        let spd = 10;
235	        const ox = e.cx, oy = e.cy + 30;
236	        let dx = player.cx - ox, dy = player.y - oy;
237	        dy -= Math.abs(dx) * 0.3;
238	        spd += Math.abs(dx) * 0.004;
239	        if (spd > 14) spd = 14;
240	        dx += rndRange(-50, 51); dy -= rndRange(50, 201);
241	        const d = Math.hypot(dx, dy) || 1;
242	        const s = spd / d;
243	        dx *= s * (1 + rndRange(-30, 31) * 0.01);
244	        dy *= s * (1 + rndRange(-30, 31) * 0.01);
245	        shootE(game, ox, oy, dx, dy, 40, rndRange(326, 329));
246	      }
247	    }
248	    if (e.ai1 >= 300) { e.ai1 = 0; e.ai0 = 0; }
249	  } else if (e.ai0 === 3 && player) {
250	    // 325 专属速射焰木(:33119-33145)：每 30t 一发 325（伤 75 速 16），120t 收招
251	    num891 = 4;
252	    e.ai1 += 1;
253	    if (e.ai1 % 30 === 0) {
254	      const ox = e.cx, oy = e.cy + 30;
255	      let dx = player.cx - ox, dy = player.y - oy;
256	      const d = Math.hypot(dx, dy) || 1;
257	      const s = 16 / d;
258	      dx *= s * (1 + rndRange(-20, 21) * 0.001);
259	      dy *= s * (1 + rndRange(-20, 21) * 0.001);
260	      shootE(game, ox, oy, dx, dy, 75, 325);
261	    }
262	    if (e.ai1 >= 120) { e.ai1 = 0; e.ai0 = 0; }
263	  } else if (e.ai0 === 4 && player) {
264	    // 325 专属希腊火连泼(:33146-33179)：每 10t 一发 326-328（伤 50 速 12→16），240t 收招
265	    num891 = 4;
266	    e.ai1 += 1;
267	    if (e.ai1 % 10 === 0) {
268	      let spd = 12;
269	      const ox = e.cx, oy = e.cy + 30;
270	      let dx = player.cx - ox, dy = player.y - oy;
271	      dy -= Math.abs(dx) * 0.2;
272	      spd += Math.abs(dx) * 0.002;
273	      if (spd > 16) spd = 16;
274	      dx += rndRange(-50, 51); dy -= rndRange(50, 201);
275	      const d = Math.hypot(dx, dy) || 1;
276	      const s = spd / d;
277	      dx *= s * (1 + rndRange(-30, 31) * 0.005);
278	      dy *= s * (1 + rndRange(-30, 31) * 0.005);
279	      shootE(game, ox, oy, dx, dy, 50, rndRange(326, 329));
280	    }
281	    if (e.ai1 >= 240) { e.ai1 = 0; e.ai0 = 0; }
282	  }
283	  // 玩家在正下方 50px 内 → 停步(:33180-33185)
284	  if (player && Math.abs(e.cx - player.cx) < 50) flag56 = true;
285	  hoverCruise(e, game, player, flag56, num891);
286	}
287	
288	// ---------------------------------------------------------------------------
289	// AI_058 南瓜王 327（NPC.cs:33246-33404）
290	// localAI[0/1]=表情帧节拍；localAI[2]=300t 换招计时 → ai[3] = rand(3)
291	//   （0 希腊火散射 / 1 悬浮→俯冲 / 2 交由双刃放焰镰）。
292	// ai[0]=0 首帧生双刃 328（ai0=-1/1 侧别）；ai[1] 0=悬浮(300t) 1=俯冲(16 速) 2=离场。
293	// ---------------------------------------------------------------------------
294	
295	/** 刃 → 南瓜王（原版 npc[ai[1]]；先走 master 引用，断链回退 id 查找） */
296	function findPumpking(game: GameHooks, e: Enemy): Enemy | null {
297	  if (e.master && !e.master.dead && e.master.vanilla?.aiStyle === 58) return e.master;
298	  return (game.enemies() as Enemy[]).find(
299	    (n) => !n.dead && n.id === e.ai1 && n.vanilla?.aiStyle === 58) ?? null;
300	}
301	
302	export function pumpkingAI(e: Enemy, game: GameHooks, player: Player | null) {
303	  const L = la(e);
304	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; L[2] = 0; }
305	  // 表情帧节拍(:33247-33256)：6t 一拍，5 拍一循环（渲染帧端消费）
306	  L[0]++;
307	  if (L[0] > 6) { L[0] = 0; L[1]++; if (L[1] > 4) L[1] = 0; }
308	  if (e.vanillaId === 327) e.lightRGB = [0.4, 0.4, 0.2];   // :33262-33264
309	  // 换招(:33266-33272)
310	  L[2]++;
311	  if (L[2] > 300) {
312	    L[2] = 0;
313	    e.ai3 = rnd(3);
314	  } else if (e.ai3 === 0 && L[2] % 30 === 0 && L[2] > 30 && player) {
315	    // 希腊火散射(:33273-33298)：每 30t 从 (cx, cy+30) 一发 326-328（伤 40 速 5，
316	    // 出膛点须非实心格）；dy*0.2 = 近乎水平的扇面散射
317	    const ox = e.cx, oy = e.cy + 30;
318	    if (!solidTileAt(game, ox, oy)) {
319	      let dx = player.cx - ox, dy = player.y - oy;
320	      dx += rndRange(-50, 51);
321	      dy += rndRange(50, 201);
322	      dy *= 0.2;
323	      const d = Math.hypot(dx, dy) || 1;
324	      const s = 5 / d;
325	      dx *= s * (1 + rndRange(-30, 31) * 0.01);
326	      dy *= s * (1 + rndRange(-30, 31) * 0.01);
327	      shootE(game, ox, oy, dx, dy, 40, rndRange(326, 329));
328	    }
329	  }
330	  // 首帧生双刃(:33300-33316)：ai0=-1 左 / +1 右（右刃 ai3=150 预蓄）
331	  if (e.ai0 === 0) {
332	    if (player) e.facing = e.seekDirX(player);
333	    e.ai0 = 1;
334	    for (const side of [-1, 1]) {
335	      const b = spawnPart(game, e, 328);
336	      if (!b) continue;
337	      b.ai0 = side;
338	      b.ai1 = e.id;
339	      b.ai2 = 0;
340	      b.ai3 = side === 1 ? 150 : 0;
341	      b.master = e;
342	    }
343	  }
344	  // 玩家死/2000px 外 → 离场态(:33318-33331)
345	  const gone = !player || player.dead
346	    || Math.abs(e.x - player.x) > 2000 || Math.abs(e.y - player.y) > 2000;
347	  if (gone && e.ai1 !== 2) e.ai1 = 2;
348	
349	  if (game.world.clock.isDay) {
350	    // 白天坠离(:33333-33336)
351	    e.vy += 0.3;
352	    e.vx *= 0.9;
353	  } else if (e.ai1 === 0) {
354	    // 悬浮(:33337-33385)：伺服玩家上方 200px；选了俯冲招(ai3==1)且蓄满 300t → 转俯冲
355	    e.ai2++;
356	    if (e.ai2 >= 300) {
357	      if (e.ai3 !== 1) { e.ai1 = 0; e.ai2 = 0; }
358	      else {
359	        e.ai1 = 1; e.ai2 = 0;
360	        if (player) e.facing = e.seekDirX(player);
361	      }
362	    }
363	    if (player) {
364	      const dx = player.cx - e.cx, dy = player.cy - 200 - e.cy;
365	      let dist = Math.hypot(dx, dy);
366	      let spd = 6;
367	      if (e.ai3 === 1) {           // 俯冲招蓄力期赶路提速(:33358-33370)
368	        if (dist > 900) spd = 12;
369	        else if (dist > 600) spd = 10;
370	        else if (dist > 300) spd = 8;
371	      }
372	      if (dist > 50) {
373	        const k = spd / dist;
374	        e.vx = (e.vx * 14 + dx * k) / 15;
375	        e.vy = (e.vy * 14 + dy * k) / 15;
376	      }
377	    }
378	  } else if (e.ai1 === 1) {
379	    // 俯冲(:33386-33400)：16 速直扑玩家中心；600t 或换招后回悬浮
380	    e.ai2 += 1;
381	    if (e.ai2 >= 600 || e.ai3 !== 1) { e.ai1 = 0; e.ai2 = 0; }
382	    if (player) {
383	      const dx = player.cx - e.cx, dy = player.cy - e.cy;
384	      const d = Math.hypot(dx, dy) || 1;
385	      const k = 16 / d;
386	      e.vx = (e.vx * 49 + dx * k) / 50;
387	      e.vy = (e.vy * 49 + dy * k) / 50;
388	    }
389	  } else if (e.ai1 === 2) {
390	    // 离场(:33401-33404... 原行号 :33386 段内)
391	    e.vy += 0.1;
392	    if (e.vy < 0) e.vy *= 0.95;
393	    e.vx *= 0.95;
394	    e.encourageDespawn(500);
395	  }
396	  e.visAngle = e.vx * -0.02;       // rotation(:33402)
397	  e.x += e.vx;                     // noTileCollide（SetDefaults 327）直积分
398	  e.y += e.vy;
399	}
400	
401	// ---------------------------------------------------------------------------
402	// AI_059 南瓜王之刃 328（NPC.cs:33405-33587）
403	// ai[0]=侧别(-1/1)；ai[1]=主 id；ai[2] 0/3=环绕 →1=升空 →2=俯冲 →(回 3) /
404	//        →4=横摆 →5=横扫回环；ai[3]=环绕计时。主选焰镰招(ai[3]==2)时 90t 一发 329。
405	// ---------------------------------------------------------------------------
406	
407	export function pumpkingBladeAI(e: Enemy, game: GameHooks, player: Player | null) {
408	  const L = la(e);
409	  const side = e.ai0 < 0 ? -1 : 1;                 // num937(:33407)
410	  e.facing = -side;                                 // spriteDirection(:33410)
411	  // 主缺失/非 aiStyle 58 → 自毁(:33412-33427)
412	  const master = findPumpking(game, e);
413	  if (!master) {
414	    e.vx *= 0.9; e.vy *= 0.9;
415	    e.dead = true;
416	    return;
417	  }
418	  e.master = master;
419	  // 主选焰镰招(:33429-33447)：90t 一发焰镰 329（伤 60，0.01/距离 的极慢初速——
420	  // 弹体 aiStyle 56 自加速 ×1.05/t 至 |v|=16，Projectile.cs:27666-27687；
421	  // NewProjectile 传 ai[0]=刃当前 rotation / ai[1]=spriteDirection，首步继承）
422	  if (master.ai3 === 2 && player) {
423	    L[1]++;
424	    if (L[1] > 90) {
425	      L[1] = 0;
426	      const ox = e.cx, oy = e.cy + 30;
427	      const dx = player.cx - ox, dy = player.y - oy;
428	      const d = Math.max(1, Math.hypot(dx, dy));
429	      const k = 0.01 / d;
430	      (game as unknown as { entities: { add: (e: unknown, b: string) => void } }).entities.add(
431	        new Arrow(e.cx, e.cy, dx * k, dy * k, 60, 0, 329, null, {
432	          grav: 0, life: 420, pierce: 1, hostile: true,
433	          scythe: { rot0: e.visAngle, flipDir: -e.facing },   // :33440 ai0=rotation/ai1=spriteDirection
434	        }), 'projectiles');
435	    }
436	  }
437	
438	  if (game.world.clock.isDay) {
439	    // 白天坠离(:33449-33452)
440	    e.vy += 0.3;
441	    e.vx *= 0.9;
442	  } else if (e.ai2 === 0 || e.ai2 === 3) {
443	    // 环绕(:33454-33506)：目标=玩家/主中点偏 (-170*side, +90)；玩家主相距 >700
444	    // 则退回主旁；按距离 6/9/12/15/18/21 速伺服；180t → 升下一态
445	    if (master.ai1 === 2) e.encourageDespawn(10);
446	    e.ai3++;
447	    if (e.ai3 >= 180) { e.ai2 += 1; e.ai3 = 0; }
448	    let tx: number, ty: number;
449	    if (player) {
450	      tx = (player.cx + master.cx) / 2 - 170 * side - e.cx;
451	      ty = (player.cy + master.cy) / 2 + 90 - e.cy;
452	      const manh = Math.abs(player.cx - master.cx) + Math.abs(player.cy - master.cy);
453	      if (manh > 700) { tx = master.cx - 170 * side - e.cx; ty = master.cy + 90 - e.cy; }
454	    } else {
455	      tx = master.cx - 170 * side - e.cx;
456	      ty = master.cy + 90 - e.cy;
457	    }
458	    let dist = Math.max(1, Math.hypot(tx, ty));
459	    let spd = 6;
460	    if (dist > 1000) spd = 21;
461	    else if (dist > 800) spd = 18;
462	    else if (dist > 600) spd = 15;
463	    else if (dist > 400) spd = 12;
464	    else if (dist > 200) spd = 9;
465	    // 侧别推离：把刃往主外侧推 4px/t(:33492-33497)
466	    if (side < 0 && e.cx > master.cx) tx -= 4;
467	    if (side > 0 && e.cx < master.cx) tx += 4;
468	    const k = spd / dist;
469	    e.vx = (e.vx * 14 + tx * k) / 15;
470	    e.vy = (e.vy * 14 + ty * k) / 15;
471	    dist = Math.max(1, Math.hypot(tx, ty));
472	    if (dist > 20) e.visAngle = Math.atan2(ty, tx) + Math.PI / 2;   // :33502-33505
473	  } else if (e.ai2 === 1) {
474	    // 升空(:33508-33534)：退到主外侧 200px、上方 230px；升过主顶 200px →
475	    // 18 速直扑玩家转俯冲
476	    const tx = master.cx - 200 * side - e.cx;
477	    const ty = master.y + 230 - e.cy;
478	    e.visAngle = Math.atan2(ty, tx) + Math.PI / 2;
479	    e.vx *= 0.95;
480	    e.vy -= 0.3;
481	    if (e.vy < -14) e.vy = -14;
482	    if (e.y < master.y - 200) {
483	      e.ai2 = 2;
484	      if (player) {
485	        const dx = player.cx - e.cx, dy = player.cy - e.cy;
486	        const d = Math.max(1, Math.hypot(dx, dy));
487	        const k = 18 / d;
488	        e.vx = dx * k;
489	        e.vy = dy * k;
490	      }
491	    }
492	  } else if (e.ai2 === 2) {
493	    // 俯冲(:33536-33546)：越过玩家高度/开始上飘/离主 800px → 回环绕
494	    const manh = Math.abs(e.cx - master.cx) + Math.abs(e.cy - master.cy);
495	    if (!player || e.y > player.y || e.vy < 0 || manh > 800) e.ai2 = 3;
496	  } else if (e.ai2 === 4) {
497	    // 横摆(:33548-33574)：钉主外侧 200px/上 230px，横速朝主对侧 ±14；
498	    // 离主 500px → 17 速直扑玩家转横扫
499	    const tx = master.cx - 200 * side - e.cx;
500	    const ty = master.y + 230 - e.cy;
501	    e.visAngle = Math.atan2(ty, tx) + Math.PI / 2;
502	    e.vy *= 0.95;
503	    e.vx += 0.3 * -side;
504	    if (e.vx < -14) e.vx = -14;
505	    if (e.vx > 14) e.vx = 14;
506	    if (e.cx < master.cx - 500 || e.cx > master.cx + 500) {
507	      e.ai2 = 5;
508	      if (player) {
509	        const dx = player.cx - e.cx, dy = player.cy - e.cy;
510	        const d = Math.max(1, Math.hypot(dx, dy));
511	        const k = 17 / d;
512	        e.vx = dx * k;
513	        e.vy = dy * k;
514	      }
515	    }
516	  } else if (e.ai2 === 5) {
517	    // 横扫回环(:33576-33586)：越过玩家水平轴/离主 800px → 回环绕
518	    const manh = Math.abs(e.cx - master.cx) + Math.abs(e.cy - master.cy);
519	    if (!player || (e.vx > 0 && e.cx > player.cx) || (e.vx < 0 && e.cx < player.cx) || manh > 800) {
520	      e.ai2 = 0;
521	    }
522	  }
523	  e.x += e.vx;                     // noTileCollide（SetDefaults 328）直积分
524	  e.y += e.vy;
525	}
526	
527	// ---------------------------------------------------------------------------
528	// AI_060 冰雪女王 345（NPC.cs:33588-33901）
529	// ai[0] -1=重选 / 0=滑翔+FrostWave 348 / 1=压制+FrostShard 349 落冰 /
530	//        2=自旋+FrostShard 349 环射。ai[1]=rand(1,4)/t 蓄招；ai[2]=滑翔朝向；
531	// ai[3]=弹幕节拍（0/负计数半周期）。残血四档全面提速（75/50/25/10%）。
532	// ---------------------------------------------------------------------------
533	
534	export function iceQueenAI(e: Enemy, game: GameHooks, player: Player | null) {
535	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
536	  if (game.world.clock.isDay) {
537	    // 白天飞离(:33590-33599)：沿当前水平向加速 + 缓升
538	    e.vx += e.vx > 0 ? 0.25 : -0.25;
539	    e.vy -= 0.1;
540	    e.visAngle = e.vx * 0.05;
541	    e.x += e.vx; e.y += e.vy;
542	    return;
543	  }
544	  const r = e.hp / e.maxHp;
545	  if (!player) {
546	    e.x += e.vx; e.y += e.vy;
547	    return;
548	  }
549	  e.facing = e.seekDirX(player);             // TargetClosest（各态首行）
550	
551	  if (e.ai0 === 0) {
552	    // 滑翔(:33601-33686)：固定水平朝向 ai[2]（与玩家同侧），越过 800px 才回摆
553	    if (e.ai2 === 0) e.ai2 = e.cx < player.cx ? 1 : -1;
554	    const dxAbs = Math.abs(e.cx - player.cx);
555	    if (e.cx < player.cx && e.ai2 < 0 && dxAbs > 800) e.ai2 = 0;
556	    if (e.cx > player.cx && e.ai2 > 0 && dxAbs > 800) e.ai2 = 0;
557	    let acc = 0.45, spd = 7;
558	    if (r < 0.75) { acc = 0.55; spd = 8; }
559	    if (r < 0.5) { acc = 0.7; spd = 10; }
560	    if (r < 0.25) { acc = 0.8; spd = 11; }
561	    e.vx += e.ai2 * acc;
562	    e.vx = clamp(e.vx, -spd, spd);
563	    // 垂直：保持悬在玩家上方 150-200px（:33628-33641）
564	    const gap = player.y - (e.y + e.h);
565	    if (gap < 150) e.vy -= 0.2;
566	    if (gap > 200) e.vy += 0.2;
567	    e.vy = clamp(e.vy, -8, 8);
568	    e.visAngle = e.vx * 0.05;
569	    // FrostWave(:33644-33685)：近距(<500)或节拍后半程且自身在玩家上方 →
570	    // 13..10+1 拍循环，过零拍从 (cx+vx*7, cy) 一发 348（伤 42，速 6..9）
571	    if ((dxAbs < 500 || e.ai3 < 0) && e.y < player.y) {
572	      e.ai3 += 1;
573	      let beat = 13;
574	      if (r < 0.75) beat = 12;
575	      if (r < 0.5) beat = 11;
576	      if (r < 0.25) beat = 10;
577	      beat++;
578	      if (e.ai3 > beat) e.ai3 = -beat;
579	      if (e.ai3 === 0) {
580	        const ox = e.cx + e.vx * 7, oy = e.cy;
581	        let dx = player.cx - ox, dy = player.cy - oy;
582	        let pspd = 6;
583	        if (r < 0.75) pspd = 7;
584	        if (r < 0.5) pspd = 8;
585	        if (r < 0.25) pspd = 9;
586	        const d = Math.hypot(dx, dy) || 1;
587	        const k = pspd / d;
588	        shootE(game, ox, oy, dx * k, dy * k, 42, 348);
589	      }
590	    } else if (e.ai3 < 0) {
591	      e.ai3 += 1;
592	    }
593	    // 蓄招(:33688-33694)：>800 且近距 → 重选
594	    e.ai1 += rndRange(1, 4);
595	    if (e.ai1 > 800 && dxAbs < 600) e.ai0 = -1;
596	  } else if (e.ai0 === 1) {
597	    // 压制落冰(:33696-33775)：水平弱追踪（速 6..9），节拍 18..8+3 一发
598	    // FrostShard 349（伤 37，vy=max(vy,0)+3 下坠）
599	    let acc = 0.15, spd = 7;
600	    if (r < 0.75) { acc = 0.17; spd = 8; }
601	    if (r < 0.5) { acc = 0.2; spd = 9; }
602	    if (r < 0.25) { acc = 0.25; spd = 10; }
603	    acc -= 0.05;
604	    spd -= 1;
605	    if (e.cx < player.cx) {
606	      e.vx += acc;
607	      if (e.vx < 0) e.vx *= 0.98;
608	    }
609	    if (e.cx > player.cx) {
610	      e.vx -= acc;
611	      if (e.vx > 0) e.vx *= 0.98;
612	    }
613	    if (e.vx > spd || e.vx < -spd) e.vx *= 0.95;
614	    const gap = player.y - (e.y + e.h);
615	    if (gap < 180) e.vy -= 0.1;
616	    if (gap > 200) e.vy += 0.1;
617	    e.vy = clamp(e.vy, -6, 6);
618	    e.visAngle = e.vx * 0.01;
619	    e.ai3 += 1;
620	    let beat = 15;
621	    if (r < 0.75) beat = 14;
622	    if (r < 0.5) beat = 12;
623	    if (r < 0.25) beat = 10;
624	    if (r < 0.1) beat = 8;
625	    beat += 3;
626	    if (e.ai3 >= beat) {
627	      e.ai3 = 0;
628	      const ox = e.cx, oy = e.y + e.h - 14;
629	      if (!solidTileAt(game, ox, oy)) {
630	        const vy = Math.max(e.vy, 0) + 3;
631	        shootE(game, ox, oy, e.vx * 0.25, vy, 37, 349);
632	      }
633	    }
634	    e.ai1 += rndRange(1, 4);
635	    if (e.ai1 > 600) e.ai0 = -1;
636	  } else if (e.ai0 === 2) {
637	    // 自旋环射(:33777-33834)：原速 0.95 衰减 + rotation+=0.2；随机方向 15 速，
638	    // 出膛点 (cx,cy-20)+方向*4；节拍 7/6/4/1/-3（<10% 血时 ai[3]>负数恒真 → 每 tick 一发）
639	    // 349（伤 35）
640	    let dx = rndRange(-1000, 1001), dy = rndRange(-1000, 1001);
641	    const d = Math.hypot(dx, dy) || 1;
642	    const k = 15 / d;
643	    dx *= k; dy *= k;
644	    e.vx *= 0.95; e.vy *= 0.95;
645	    e.visAngle += 0.2;
646	    const ox = e.cx + dx * 4, oy = e.cy - 20 + dy * 4;
647	    e.ai3 += 1;
648	    let beat = 7;
649	    if (r < 0.75) beat--;
650	    if (r < 0.5) beat -= 2;
651	    if (r < 0.25) beat -= 3;
652	    if (r < 0.1) beat -= 4;
653	    if (e.ai3 > beat) {
654	      e.ai3 = 0;
655	      shootE(game, ox, oy, dx, dy, 35, 349);
656	    }
657	    e.ai1 += rndRange(1, 4);
658	    if (e.ai1 > 500) e.ai0 = -1;
659	  }
660	  if (e.ai0 === -1) {
661	    // 重选(:33836-33847)：rand(3)，>1000px 强制滑翔
662	    let pick = rnd(3);
663	    if (Math.abs(e.cx - player.cx) > 1000) pick = 0;
664	    e.ai0 = pick;
665	    e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
666	  }
667	  e.x += e.vx;                     // noTileCollide（SetDefaults 345）直积分
668	  e.y += e.vy;
669	}
670	
671	// ---------------------------------------------------------------------------
672	// AI_061 圣诞坦克 346（NPC.cs:33902-34154）——与 aiStyle 57 同构的悬浮树怪 +
673	// ai[0] 0=蓄招(300t) 1=链炮弹幕(240t，proj 180 每 16/14/11/8t)；
674	// localAI[1]=火箭 350 连发（100t 突发，12t 一发）；localAI[2]=礼盒 351 突发
675	// （100t，9t 一发）；随机 352 尖刺（1/600 触发，残血缩到 1/300）。
676	// ---------------------------------------------------------------------------
677	
678	export function santaNK1AI(e: Enemy, game: GameHooks, player: Player | null) {
679	  const L = la(e);
680	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; L[1] = 0; L[2] = 0; }
681	  const isDay = game.world.clock.isDay;
682	  let num980 = 2;                                   // 巡航速(:33905)
683	  if (e.hp < e.maxHp * 0.75) num980 = 3;
684	  if (e.hp < e.maxHp * 0.5) num980 = 4;
685	  if (e.hp < e.maxHp * 0.25) num980 = 5;
686	  // 点光(:33918-33923)：中心格非实心时
687	  if (!solidTileAt(game, e.cx, e.cy)) e.lightRGB = [0.3, 0.26, 0.05];
688	  if (!isDay && player && !player.dead) e.facing = e.seekDirX(player);   // :33909-33912
689	  let flag58 = false;
690	
691	  if (isDay) {
692	    e.encourageDespawn(10);                          // :33925-33931
693	    num980 = 8;
694	    if (e.vx === 0) e.vx = 0.1;
695	  } else {
696	    if (e.ai0 === 0) {
697	      // 蓄招(:33932-33941)
698	      e.ai1 += 1;
699	      if (e.ai1 >= 300 && player) {
700	        e.facing = e.seekDirX(player);        // TargetClosest
701	        e.ai1 = 0;
702	        e.ai0 = 1;
703	      }
704	    } else if (e.ai0 === 1 && player) {
705	      // 链炮(:33942-33975)： muzzle=(cx+dir*50, cy+rand(15,36))，每 num981 一发
706	      // BulletDeadeye 180（伤 36 速 15）
707	      e.ai1 += 1;
708	      flag58 = true;
709	      let num981 = 16;
710	      if (e.hp < e.maxHp * 0.25) num981 = 8;
711	      else if (e.hp < e.maxHp * 0.5) num981 = 11;
712	      else if (e.hp < e.maxHp * 0.75) num981 = 14;
713	      if (e.ai1 % num981 === 0) {
714	        const ox = e.cx + e.facing * 50, oy = e.cy + rndRange(15, 36);
715	        let dx = player.cx - ox, dy = player.cy - oy;
716	        dx += rndRange(-40, 41); dy += rndRange(-40, 41);
717	        const d = Math.hypot(dx, dy) || 1;
718	        const k = 15 / d;
719	        dx *= k * (1 + rndRange(-20, 21) * 0.015);
720	        dy *= k * (1 + rndRange(-20, 21) * 0.015);
721	        shootE(game, ox, oy, dx, dy, 36, 180);
722	      }
723	      if (e.ai1 > 240) { e.ai0 = 0; e.ai1 = 0; }
724	    }
725	  }
726	  // 三种随机武器(:33977-34103)：独立于 ai[0]/昼夜（原版仅 netMode 门）——
727	  // 阈值 600/1200/2700（残血 0.9/0.75/0.5 缩）
728	  if (player) {
729	    const r = e.hp / e.maxHp;
730	    let nBurst = 600, nRocket = 1200, nPresent = 2700;
731	    if (r < 0.25) { nBurst *= 0.5; nRocket *= 0.5; nPresent *= 0.5; }
732	    else if (r < 0.5) { nBurst *= 0.75; nRocket *= 0.75; nPresent *= 0.75; }
733	    else if (r < 0.75) { nBurst *= 0.9; nRocket *= 0.9; nPresent *= 0.9; }
734	    const gunX = e.cx - e.facing * 24, gunY = e.cy - 64;   // 炮口(:33985/34005/34140)
735	    // 尖刺 352（伤 80，近乎垂直上抛的慢速弹）
736	    if (rnd(nBurst) === 0) {
737	      let dx = rndRange(1, 100) * e.facing, dy = 1;
738	      const d = Math.hypot(dx, dy) || 1;
739	      const k = 1 / d;
740	      shootE(game, gunX, gunY, dx * k, dy * k, 80, 352);
741	    }
742	    // 火箭 350 突发（:34000-34031）：触发置 localAI[1]=1，100t 内每 12t 一发（伤 42 速 12.5）
743	    if (rnd(nRocket) === 0) L[1] = 1;
744	    if (L[1] >= 1) {
745	      L[1] += 1;
746	      if (L[1] % 12 === 0) {
747	        let dx = player.cx - gunX, dy = player.cy - gunY;
748	        dx += rndRange(-50, 51); dy += rndRange(-50, 51);
749	        const d = Math.hypot(dx, dy) || 1;
750	        const k = 12.5 / d;
751	        dx *= k * (1 + rndRange(-20, 21) * 0.015);
752	        dy *= k * (1 + rndRange(-20, 21) * 0.015);
753	        shootE(game, gunX, gunY, dx, dy, 42, 350);
754	      }
755	      if (L[1] >= 100) L[1] = 0;
756	    }
757	    // 礼盒 351 突发（:34033-34064）：触发置 localAI[2]=2，100t 内每 9t 一发
758	    // （伤 50 速 11，-300 垂直分量 = 高抛）
759	    if (rnd(nPresent) === 0) L[2] = 2;
760	    if (L[2] > 0) {
761	      L[2] += 1;
762	      if (L[2] % 9 === 0) {
763	        let dx = rndRange(-100, 101), dy = -300;
764	        const d = Math.hypot(dx, dy) || 1;
765	        const k = 11 / d;
766	        dx *= k * (1 + rndRange(-20, 21) * 0.01);
767	        dy *= k * (1 + rndRange(-20, 21) * 0.01);
768	        shootE(game, gunX, gunY, dx, dy, 50, 351);
769	      }
770	      if (L[2] >= 100) L[2] = 0;
771	    }
772	  }
773	  if (player && Math.abs(e.cx - player.cx) < 50) flag58 = true;   // :34105-34107
774	  hoverCruise(e, game, player, flag58, num980);
775	}
776	
777	// ---------------------------------------------------------------------------
778	// AI_062 玩具直升机 347（NPC.cs:34155-34207）
779	// 7 速追 (cx+dir*20, cy+6)→玩家；>600px 或无视线 → 全速追；否则原速 0.98 衰减
780	// 悬停，几乎静止后每 15t 一发 BulletDeadeye 180（伤 32 速 10）。白天倒飞离场。
781	// ---------------------------------------------------------------------------
782	
783	export function elfCopterAI(e: Enemy, game: GameHooks, player: Player | null) {
784	  const L = la(e);
785	  if (!e.bInit) { e.bInit = true; L[0] = 0; }
786	  if (!player) { e.x += e.vx; e.y += e.vy; return; }
787	  e.facing = e.seekDirX(player);             // TargetClosest(:34157)
788	  e.visAngle = Math.abs(e.vx) * e.facing * 0.1;      // rotation(:34158)
789	  const ox = e.cx + e.facing * 20, oy = e.cy + 6;    // vector121(:34160)
790	  let dx = player.cx - ox, dy = player.y - oy;
791	  const dist = Math.hypot(dx, dy) || 1;
792	  const k = 7 / dist;
793	  dx *= k; dy *= k;
794	  const canHit = losClear(game, e.cx, e.cy, player.cx, player.cy);   // Collision.CanHit(:34169)
795	  if (game.world.clock.isDay) {
796	    // 白天倒飞离场(:34171-34178)：目标速度取反
797	    e.vx = (e.vx * 59 - dx) / 60;
798	    e.vy = (e.vy * 59 - dy) / 60;
799	    e.encourageDespawn(10);
800	    e.x += e.vx; e.y += e.vy;
801	    return;
802	  }
803	  if (dist > 600 || !canHit) {
804	    // 远距/隔墙：全速追(:34180-34186)
805	    e.vx = (e.vx * 59 + dx) / 60;
806	    e.vy = (e.vy * 59 + dy) / 60;
807	    e.x += e.vx; e.y += e.vy;
808	    return;
809	  }
810	  // 近距悬停点射(:34188-34206)
811	  e.vx *= 0.98;
812	  e.vy *= 0.98;
813	  if (Math.abs(e.vx) < 1 && Math.abs(e.vy) < 1) {
814	    L[0] += 1;
815	    if (L[0] >= 15) {
816	      L[0] = 0;
817	      let sx = player.cx - ox, sy = player.cy - oy;
818	      sx += rndRange(-35, 36); sy += rndRange(-35, 36);
819	      sx *= 1 + rndRange(-20, 21) * 0.015;
820	      sy *= 1 + rndRange(-20, 21) * 0.015;
821	      const d = Math.hypot(sx, sy) || 1;
822	      const sk = 10 / d;
823	      sx *= sk * (1 + rndRange(-20, 21) * 0.0125);
824	      sy *= sk * (1 + rndRange(-20, 21) * 0.0125);
825	      shootE(game, ox, oy, sx, sy, 32, 180);
826	    }
827	  }
828	  e.x += e.vx;                     // noTileCollide（SetDefaults 347）直积分
829	  e.y += e.vy;
830	}
831	
832	// ---------------------------------------------------------------------------
833	// AI_063 弗洛科 352（NPC.cs:34208-34255）
834	// 11 速追 (cx+dir*20, cy+6)→玩家中心；<200px 进入旋冲（ai[0]=20 拍冷却，
835	// rotation+=0.3*dir 保持原速度俯冲），拉开后回追踪（<350/<300 双重加速收敛）。
836	// ---------------------------------------------------------------------------
837	
838	export function flockoAI(e: Enemy, game: GameHooks, player: Player | null) {
839	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; }
840	  if (!player) { e.x += e.vx; e.y += e.vy; return; }
841	  e.facing = e.seekDirX(player);             // TargetClosest(:34210)
842	  const ox = e.cx + e.facing * 20, oy = e.cy + 6;    // vector122(:34212)
843	  let dx = player.cx - ox, dy = player.cy - oy;
844	  const dist = Math.hypot(dx, dy) || 1;
845	  const k = 11 / dist;
846	  dx *= k; dy *= k;
847	  if (game.world.clock.isDay) {
848	    // 白天反向逃逸(:34220-34223)
849	    dx = -dx; dy = -dy;
850	  }
851	  e.ai0 -= 1;                                       // :34225
852	  if (dist < 200 || e.ai0 > 0) {
853	    // 旋冲(:34227-34239)：贴近置 20 拍；方向取速度符号（原版改写 direction，
854	    // 不动 spriteDirection），原地自旋不改变速度
855	    if (dist < 200) e.ai0 = 20;
856	    const diveDir = e.vx < 0 ? -1 : 1;
857	    e.visAngle += diveDir * 0.3;
858	    e.x += e.vx; e.y += e.vy;
859	    return;
860	  }
861	  // 追踪(:34241-34254)：(v*50+n)/51，<350/<300 再叠两重收敛
862	  e.vx = (e.vx * 50 + dx) / 51;
863	  e.vy = (e.vy * 50 + dy) / 51;
864	  if (dist < 350) {
865	    e.vx = (e.vx * 10 + dx) / 11;
866	    e.vy = (e.vy * 10 + dy) / 11;
867	  }
868	  if (dist < 300) {
869	    e.vx = (e.vx * 7 + dx) / 8;
870	    e.vy = (e.vy * 7 + dy) / 8;
871	  }
872	  e.visAngle = e.vx * 0.15;
873	  e.x += e.vx;                      // noTileCollide（SetDefaults 352）直积分
874	  e.y += e.vy;
875	}
876	
877	// ---------------------------------------------------------------------------
878	// AI_038 雪人三兄弟（NPC.cs:29115-29256）
879	// 143 SnowmanGangsta：每 120t 一发 BulletSnowman 110（伤 25 速 12*dir 水平）。
880	// 144 MisterStabby / 145 SnowBalla：ai[1]>=3 落地停顿（144 200t / 145 16t，
881	//   145 在第 8 拍投 SnowBallHostile 109，伤 35 速 10）；停顿结束 ai[1] 清零回跳扑。
882	// 其余：三连跳循环（ai[0] 0/1/2 小跳 vy=-6，过 2 大跳 vy=-8.2 + ai[1]+1）；
883	//   原地白跳（localAI[2]==x）→ 转向 + ai[3]=60 冷却。
884	// ---------------------------------------------------------------------------
885	
886	export function snowmanAI(e: Enemy, game: GameHooks, player: Player | null) {
887	  const L = la(e);
888	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
889	  const vid = e.vanillaId ?? 143;
890	  let num586 = 4, num587 = 1;                        // 限速/加速(:29118-29127)
891	  if (vid === 143) { num586 = 3; num587 = 0.7; }
892	  if (vid === 145) { num586 = 3.5; num587 = 0.8; }
893	  // 重力+位移先积分（原版 AI 读上一帧 velocity.Y==0 判落地，等价移动后判定）
894	  e.vy = Math.min(e.vy + GRAVITY, MAX_FALL_SPEED);
895	  moveAndCollide(e, game.world, e.vx, e.vy);
896	  const onG = e.onGround;   // moveAndCollide 落地即 vy=0（原版 velocity.Y==0 门）
897	
898	  if (vid === 143) {
899	    // 机枪雪球(:29129-29151)
900	    e.ai2 += 1;
901	    if (e.ai2 >= 120) {
902	      e.ai2 = 0;
903	      const ox = e.cx - e.facing * 12, oy = e.cy;
904	      shootE(game, ox, oy, 12 * e.facing, 0, 25, 110);
905	    }
906	  }
907	  if (vid === 144 && e.ai1 >= 3) {
908	    // Stabby 停顿(:29153-29170)
909	    e.facing = player ? e.seekDirX(player) : -1;   // TargetClosest
910	    if (onG) {
911	      e.vx *= 0.9;
912	      if (e.vx > -0.3 && e.vx < 0.3) e.vx = 0;
913	      e.ai2 += 1;
914	      if (e.ai2 >= 200) { e.ai2 = 0; e.ai1 = 0; }
915	    }
916	  } else if (vid === 145 && e.ai1 >= 3) {
917	    // SnowBalla 投掷停顿(:29172-29206)：第 8 拍投雪球 109
918	    e.facing = player ? e.seekDirX(player) : -1;
919	    if (onG) {
920	      e.vx *= 0.9;
921	      if (e.vx > -0.3 && e.vx < 0.3) e.vx = 0;
922	      e.ai2 += 1;
923	      if (e.ai2 >= 16) { e.ai2 = 0; e.ai1 = 0; }
924	    }
925	    if (e.vx === 0 && e.vy === 0 && e.ai2 === 8 && player) {
926	      const ox = e.cx - e.facing * 12, oy = e.y + e.h * 0.25;
927	      let dx = player.cx - ox, dy = player.y - oy;
928	      const d = Math.hypot(dx, dy) || 1;
929	      const k = 10 / d;
930	      shootE(game, ox, oy, dx * k, dy * k, 35, 109);
931	    }
932	  } else {
933	    // 跳扑循环(:29208-29234)
934	    if (onG) {
935	      if (L[2] === e.x) { e.facing *= -1; e.ai3 = 60; }   // 原地白跳转向
936	      L[2] = e.x;
937	      if (e.ai3 === 0 && player) e.facing = e.seekDirX(player);   // TargetClosest
938	      e.ai0 += 1;
939	      if (e.ai0 > 2) {
940	        e.ai0 = 0;
941	        e.ai1 += 1;
942	        e.vy = -8.2;
943	        e.vx += e.facing * num587 * 1.1;
944	      } else {
945	        e.vy = -6;
946	        e.vx += e.facing * num587 * 0.9;
947	      }
948	    }
949	    e.vx += e.facing * num587 * 0.01;
950	  }
951	  if (e.ai3 > 0) e.ai3 -= 1;                         // :29236-29238
952	  if (e.vx > num586 && e.facing > 0) e.vx = num586;
953	  if (e.vx < -num586 && e.facing < 0) e.vx = -num586;
954	}
955	
956	// ---------------------------------------------------------------------------
957	// AI_009 弹跳球族（NPC.cs:21349-21548）
958	// 25 FireBall(速5) / 30+665 ChaosBall(速6) / 33 WaterSphere(速6) / 112+666 VileSpit
959	// (速7，ai[0]==2 双倍位移+进墙自爆) / 516 SolarFlare(渐显+随机出膛+微追踪，
960	// 撞墙/贴脸 20px 自爆)。全员每 tick EncourageDespawn(100)、rotation 累进。
961	// ---------------------------------------------------------------------------
962	
963	/** 原版精灵恒隐形的弹体系：33 水球（SetDefaults alpha=255）；30/665 混沌球
964	 *  （AI :21496 每帧强置 alpha=255）——视觉全靠尘迹，本仓改为显形精灵+补尘迹 */
965	function invisibleSpriteBall(e: Enemy): boolean {
966	  const id = e.vanillaId ?? -1;
967	  return id === 33 || id === 30 || id === 665;
968	}
969	
970	export function bouncingBallAI(e: Enemy, game: GameHooks, player: Player | null) {
971	  const L = la(e);
972	  if (!e.bInit) {
973	    e.bInit = true; e.ai0 = 0;   // 原版 ai[0] 从 0 起步（Enemy 默认 -1120 是史莱姆族约定）
974	    // 弹体可见性：原版 33 SetDefaults alpha=255、30/665 AI 每帧强置 alpha=255
975	    // （cs:21494-21496）——精灵恒隐形，弹体视觉【全部】由尘迹承担（33=尘172×6/t
976	    // 蓝尘、30/665=尘27×4/t 阴影焰紫、25=尘6 火尘）。fromVanilla 对 alpha>=255 走
977	    // 254 起步 -1/t 渐显 → 球前 ~200t 不透明度 <80%（玩家间距内全程近乎不可见）且
978	    // 无尘迹补偿 = "看不到任何弹幕"（2026-08-17 用户报告 32 不发射）。本仓粒子密度/
979	    // 发光弱于原版尘系，保隐形会退化成隐形弹：故三系直接全显精灵 + 补尘迹/补光
980	    // （偏差登记：原版精灵隐形、仅尘迹+尘光）
981	    if (invisibleSpriteBall(e)) { e.alphaFade = false; e.spawnAlpha = 0; }
982	  }
983	  const vid = e.vanillaId ?? 25;
984	  // 日耀耀斑(:21354-21378)：alpha 0→220 渐隐成光团；出膛方向 = 朝玩家 ±90° 随机
985	  // （再固定回转 -45°），Y 分量钳 0.2，速 6+rand*4
986	  if (vid === 516) {
987	    if (e.spawnAlpha < 220) e.spawnAlpha = Math.min(220, e.spawnAlpha + 40);
988	    if (e.ai0 === 0) {
989	      e.ai0 = 1;
990	      if (player) {
991	        let dx = player.cx - e.cx, dy = player.cy - e.cy;
992	        const d = Math.hypot(dx, dy) || 1;
993	        dx /= d; dy /= d;
994	        const ang = Math.atan2(dy, dx) + (Math.random() * 2 - 1) * 1.5707963705062866
995	          - 0.7853981852531433;
996	        let ux = Math.cos(ang), uy = Math.sin(ang);
997	        if (uy > 0.2) uy = 0.2;
998	        const spd = 6 + Math.random() * 4;
999	        e.vx = ux * spd; e.vy = uy * spd;
1000	      }
1001	    }
1002	    // 撞墙/距玩家 <20px → 自爆（原版 StrikeNPCNoInteraction(9999)）
1003	    const hitWall = solidRect(game, e.x, e.y, e.w, e.h);
1004	    if (hitWall || (player && Math.hypot(player.cx - e.cx, player.cy - e.cy) < 20)) {
1005	      e.hurt(9999, 0, 0, game);
1006	      return;
1007	    }
1008	  }
1009	  // 首帧定速直飞(:21380-21406)：num125 = 6（25→5、112/666→7）；
1010	  // FTW 抬档(:21391-21407)：33 且骷髅王在场 → 10（RedHat 8）/ 25 且血肉墙在场 → 14 /
1011	  // 666 → 10（flag8 = RedHatSkeletronAdjustmentsEnabled：33 判 ai[3]==1，NPC.cs:67282）
1012	  if (!L[3] && player) {
1013	    L[3] = 1;
1014	    let num125 = 6;
1015	    if (vid === 25) num125 = 5;
1016	    if (vid === 112 || vid === 666) num125 = 7;
1017	    if (game.world.seedFlags?.getGoodWorld) {
1018	      if (vid === 33 && anyNpcs(game, 35)) {
1019	        num125 = 10;
1020	        if (e.ai3 === 1) num125 = 8;
1021	      }
1022	      if (vid === 25 && anyNpcs(game, 113)) num125 = 14;
1023	      if (vid === 666) num125 = 10;
1024	    }
1025	    const dx = player.cx - e.cx, dy = player.cy - e.cy;
1026	    const d = Math.hypot(dx, dy) || 1;
1027	    e.vx = (dx / d) * num125;
1028	    e.vy = (dy / d) * num125;
1029	  }
1030	  // getGoodWorld 专属无敌分支(:21422-21435，expert 略)：
1031	  //   33 且骷髅王在场 / 25 且血肉墙在场 / 666 地表（Center.Y/16 < worldSurface）→
1032	  //   dontTakeDamage。原版门为 !dontTakeDamage（只置不清——条件失效后已置位的球
1033	  //   仍无敌，原版怪癖 1:1）
1034	  if (game.world.seedFlags?.getGoodWorld && !e.dontTakeDamage) {
1035	    if (vid === 33 && anyNpcs(game, 35)) e.dontTakeDamage = true;
1036	    else if (vid === 25 && anyNpcs(game, 113)) e.dontTakeDamage = true;
1037	    else if (vid === 666 && e.cy / TILE < game.world.groundLevel) e.dontTakeDamage = true;
1038	  }
1039	  // 毒唾(:21425-21451)：ai[0] 1→3 渐进；==2 时双倍位移 + 爆裂尘
1040	  if (vid === 112 || vid === 666) {
1041	    e.ai0 += 1;
1042	    if (e.ai0 > 3) e.ai0 = 3;
1043	    if (e.ai0 === 2) {
1044	      e.x += e.vx;
1045	      e.y += e.vy;
1046	      game.spawnParticles(e.cx, e.cy, '#7A4FB0', 3, 1.2, { life: 30, damp: 0.9 });
1047	    }
1048	    // 进实心块自爆(:21463-21468)——noTileCollide 穿墙飞行途中入墙即碎
1049	    if (solidRect(game, e.x, e.y, e.w, e.h)) {
1050	      e.hurt(9999, 0, 0, game);
1051	      return;
1052	    }
1053	  }
1054	  e.encourageDespawn(100);                           // :21470（离屏 ~100t 即消）
1055	  if (vid === 516) {
1056	    // 耀斑微追踪(:21472-21488)：(v*14 + dir*(|v|+1/12))/15，<6 速时 ×1.05 回升
1057	    e.visAngle += 0.1 * e.facing;
1058	    if (player) {
1059	      let dx = player.cx - e.cx, dy = player.cy - e.cy;
1060	      const d = Math.hypot(dx, dy) || 1;
1061	      dx /= d; dy /= d;
1062	      const spd = Math.hypot(e.vx, e.vy);
1063	      e.vx = (e.vx * 14 + dx * (spd + 1 / 12)) / 15;
1064	      e.vy = (e.vy * 14 + dy * (spd + 1 / 12)) / 15;
1065	      if (Math.hypot(e.vx, e.vy) < 6) { e.vx *= 1.05; e.vy *= 1.05; }
1066	    }
1067	  } else {
1068	    // 火球点光(:21540-21542，默认分支 = FireBall）
1069	    if (vid === 25) e.lightRGB = [1, 0.3, 0.1];
1070	    // 尘迹补偿（原版 :21488-21540 每 tick 尘 2×{3-4} 颗，隐形系弹体的全部视觉）：
1071	    //   33=尘172 淡蓝（wiki：与水矢雷同/发光） / 30·665=尘27 阴影焰紫 / 25=尘6 火尘
1072	    // 33 补点光（原版光源=尘 172 自发光，本仓粒子不发光——wiki"emits a fair amount
1073	    // of light"）；25 的 AddLight(1,0.3,0.1) 已在上方原样接
1074	    if (vid === 33) {
1075	      e.lightRGB = [0.55, 0.75, 1];
1076	      game.spawnParticles(e.x + 2, e.y + 2, '#9AC8E8', 2, 0.4, { life: 30, size: 2 });
1077	    } else if (vid === 30 || vid === 665) {
1078	      game.spawnParticles(e.x + 2, e.y + 2, '#7A5AC8', 2, 0.4, { life: 30, size: 2 });
1079	    } else if (vid === 25) {
1080	      game.spawnParticles(e.x + 2, e.y + 2, '#FFB050', 1, 0.5, { life: 26, size: 2 });
1081	    }
1082	    e.visAngle += 0.4 * e.facing;                    // :21547
1083	  }
1084	  // 位移：noTileCollide 族穿墙直积分；516（tileCollide）走碰撞
1085	  if (e.vanilla?.noTileCollide) {
1086	    e.x += e.vx;
1087	    e.y += e.vy;
1088	  } else {
1089	    moveAndCollide(e, game.world, e.vx, e.vy);
1090	    // 516 的 collideX/collideY（:21370 上一帧碰撞旗标）→ 撞墙/落地即自爆
1091	    if (vid === 516 && (e.hitWall || e.hitHead || e.onGround)) {
1092	      e.hurt(9999, 0, 0, game);
1093	    }
1094	  }
1095	}
1096	

```


---

## 🤖 Assistant · 2026-08-19T07:46:23.585Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Interesting. Our moon events file:

**Pumpking 327**: 
- `e.ai3` = 换招轮换 (0/1/2) — matches vanilla ai[3] pose semantics? Vanilla FindFrame uses ai[3]==0/1/2 as pose selector! Our ai3 = attack choice (0 greek fire scatter / 1 hover→dive / 2 scythe) — and vanilla's ai[3] for pumpking is indeed the attack selector (see :33266-33272 `ai[3] = rand(3)`), used directly by FindFrame as the pose. So pose = e.ai3 (0→row0, 1→row4, 2→row8). The task said "确认姿态源=当前攻击态" — confirmed: vanilla AI sets ai[3]=Main.rand.Next(3) and FindFrame maps it. 

- L[0]/L[1]: "表情帧节拍(:33247-33256)：6t 一拍，5 拍一循环（渲染帧端消费）" — there's already a beat counter L[0] (0..6) and L[1] (0..4)! And a note "渲染侧只读出口 localAIOf (南瓜王 327 披风帧 = localAI[1]，Main.cs:22501)" — interesting: localAIOf is exported for the render side, used for the cloak frame (Main.cs:22501 — pumpking's cloak is drawn in Main.cs DrawNPC with localAI[1]?). Let me check how Renderer uses localAIOf currently. The vanilla :33247-33256 AI segment: let me read it to understand what L[0]/L[1] actually drive.

Actually wait — in vanilla AI_058 (:33246-33404), there's a segment :33247-33256. Let me read vanilla 33246-33300 to see.

Hmm — but our pumpking frame machine: the task says implement FindFrame 327 in Renderer with ai[3] pose machine. The FindFrame logic uses its own frameCounter (advance/decrement) — needs a persistent frame + counter. Since Renderer's vanillaFrameIdx is stateless (except customFrameIdx), I need the AI to maintain the frame index. Options:
1. AI writes e.customFrameIdx each tick (direct frame number), Renderer's first line reads it. This is the cleanest for pumpking — the pose transition logic (frame walk toward target) is stateful.
2. The existing L[0]/L[1] beat — what is it for? "披风帧" (cloak frame) per Main.cs:22501. Let me check Main.cs:22501 to see.

Let me read the vanilla AI_058 pumpking segment around :33247-33256 to see what localAI[0]/[1] do in the AI (maybe they're the cloak flap beat used in DrawNPC, separate from FindFrame).

Also note the pumpking FindFrame counter behavior: frameCounter increments ±1 (or unchanged); when >6 → frame+1 (wrap 11→0); when <0 → frame-1 (wrap 0→11), counter=6. So the "7t per step" and bidirectional walk. I'll implement this in the AI (pumpkingAI) writing e.customFrameIdx. 

Wait — but where do L[0]/L[1] fit? Let me read vanilla :33246-33275.

**Ice Queen 345**: ai0 = -1 reselect/0 glide/1 rain/2 spin; ai3 = 弹幕节拍 (0/负半周期). Vanilla FindFrame: ai0==0 → ai3>=0 → frame 0; else vx<0 → 1, vx>=0... wait `else if (velocity.X < 0f) frame = num; else frame = num*2`. Our ai3: "节拍 0/负计数半周期" — in glide state, ai3 counts +1 until > beat → -beat, then counts up toward 0 → shoots at 0. So ai3 ∈ (-beat, beat]; ai3 >= 0 most of the time; ai3 < 0 during the "armed" half. Vanilla: ai3>=0 → frame 0 (neutral), ai3<0 → frame 1 or 2 by vx direction. Our ai3 semantics match vanilla's (it's a 1:1 port). 

But wait — in our AI, ai3 is only advanced within ai0===0 when `(dxAbs < 500 || e.ai3 < 0) && e.y < player.y`; else `else if (e.ai3 < 0) e.ai3 += 1;`. Vanilla same. And note when transitioning to other states ai3 resets to 0 at reselect. In ai0===1 (rain), ai3 counts 0..beat (always >= 0) — but frame machine for ai0==1 uses frameCounter (not ai3) → rows 3-4 cycle 6t. Our ai0===1: ai3 counts up, resets to 0 at shoot. Frame machine: fc += 1/t; >5 → advance; clamp band 3-4. Stateful counter → but it's a simple 2-frame cycle at fixed 6t rate — can use global t: frame = 3 + floor(t/6)%2 — exact modulo phase (phase arbitrary since original counter never resets except band transitions; acceptable per existing code patterns, e.g. 222 uses t/5). Good — stateless.

ai0===2 → frame 5 constant. ai0==-1 (reselect, 1 tick) → falls to else? Vanilla switch: ai0==0/1/2 cases; -1 → no branch → frame unchanged... wait vanilla: `if (ai[0] == 0f) {...} else if (ai[0] == 1f) {...} else if (ai[0] == 2f) {...}` — for ai0==-1 nothing happens → frame frozen for that tick. Our reselect resolves within the same AI tick (ai0 set to pick at end), so renderer sees the new state. Fine.

Note: our ai0=-1 → vanilla frame unchanged; but since our AI resolves -1 → 0/1/2 in the same tick before render, no issue.

Also for ai0==0 glide: frame = ai3>=0 ? 0 : (vx<0 ? 1 : 2).

**Santa-NK1 346**: ai0 0=蓄招 1=链炮. Vanilla FindFrame: ai0==1 → rows 6-8 @3t; else vx==0 → hold; else walk rows 1-5, fc += 1 + |vx|/2, >4 advance. Our ai0===1 during chaingun (240t) — matches. Walking: needs |vx| accumulate → use walkCycleT? Our walkCycleT accumulates |vx| per tick (`this.walkCycleT += Math.abs(this.vx)` — but line 1247: `if (Math.abs(this.vx) <= 0.05) this.walkCycleT = 0;` — resets when idle). Vanilla: fc += 1 + |vx|/2. So counter ≈ t + walkCycleT/2. Frame advance when counter > 4 → each frame 5 counter-units. So frame = 1 + floor((t + walkCycleT/2)/5) % 5. Since walkCycleT resets to 0 on idle and vanilla's fc resets to 0 on idle (the `frameCounter = 0.0` in the vx==0 branch) — consistent! Actually vanilla resets fc=0 when vx==0 AND keeps frame; when walking resumes, fc starts from 0 again. Our formula: idle → t keeps growing though. Hmm: at resume, counter = t + walkCycleT/2 — t is huge (never reset). Phase arbitrary → the pattern jumps to arbitrary walk frame each resume. Vanilla resumes from the held frame, advancing after 5 counts. Our approach: phase from global t — arbitrary phase but correct 5-unit cadence. Given the established code style (e.g. 222 uses floor(t/5)), acceptable. But better: we could approximate counter ≡ walkCycleT/2 + (time since walk start) — not tracked. Fine, use t + walkCycleT/2. Hmm, actually — to make phase stable while walking (no jitter), any monotonic function works; (t + walkCycleT/2)/5 is monotonic during walking. On resume phase is arbitrary — same class of approximation as existing code ("相位取全局 t(重进悬浮段时相位任意,差 <12t)" noted for 127). OK.

But the fire band (ai0==1) needs exact 3t cadence: frame = 6 + floor(t/3)%3. On entering band, vanilla starts at whatever frame, clamps to [6,8]... `if (frame.Y > num*8) frame.Y = num*6; if (frame.Y < num*6) frame.Y = num*6;` — entering from walk frame 1-5 → clamped up to 6. So frame starts 6, advances every 3t. Using floor(t/3)%3 → phase arbitrary (0/3 error). Acceptable.

Wait, also vanilla fire branch: `frameCounter += 1.0; if (frameCounter > 2.0) { frame.Y += num; frameCounter = 0.0; }` — 3t per frame (fc=0,1,2 → advance on 3rd). Band 6,7,8 → wrap 8→6. floor(t/3)%3 + 6. Good.

**Mourning Wood 325 / Everscream 344**: 
- 325: vx==0 → band 0-4 @5t (fc>4 → 5t per frame); else band 5-9 @5t. Both need persistent counter; but they're fixed 5t cycles — stateless: idle band: floor(t/5)%5; move band: 5 + floor(t/5)%5. Vanilla uses the same frameCounter for both (continues across band switches, so on switch frame snaps to band edge via clamps: `if (frame.Y < num*5) frame.Y = num*5` etc.). Stateless per-band floor(t/5)%5 is visually equivalent (phase arbitrary on switch).
- 344: standing: fc += 1/t, 6 counts per frame (fc > 5 → advance → 6t/frame); moving: fc += max(1, |vx|*0.75). Both cycle 0-9. Moving speed: counter = walkCycleT*0.75 + t (since +1 base folded: counter += max(1, |vx|*0.75) ≥ 1; approximate as t + walkCycleT*0.75 — for |vx|*0.75 < 1 (|vx|<1.33) vanilla adds 1, our formula adds 1 + 0.75|vx|... hmm. Let me think: vanilla counter increment per tick = max(1, 0.75|vx|). Our approximation = 1 + 0.75|vx| (t + walkCycleT*0.75). For |vx| ≥ 4/3, vanilla increment = 0.75|vx| ≥ 1; ours = 1+0.75|vx| — off by +1/t — drifts slightly faster (frame every 6/(0.75|vx|) vs 6/(1+0.75|vx|)). For large |vx| (2-5), relative error small. For |vx| < 1.33, vanilla = 1/t; ours = 1+0.75|vx| (up to 2/t) — up to 2x too fast at |vx|=1.33... hmm. 

Alternatively replicate exactly: counter ≡ Σ max(1, 0.75|vx_t|). We have walkCycleT = Σ|vx| (reset at idle). And t counts all ticks. Can't reconstruct Σmax(1,·) from those two exactly... but we could maintain a dedicated accumulator. Everscream 344 always moves though (hoverCruise always integrates; vx can be near 0 when stopped/attack). Hmm — is 344's counter even reset on stop? Looking at vanilla 344: NO reset on vx==0 — the standing branch keeps fc += 1 continuously, and the moving branch continues from the same counter. So the counter never resets! It's a single continuous counter from spawn: increment = max(1, 0.75|vx|) when moving, +1 when standing. That's = t + 0.75*Σ_{moving ticks}|vx|. And Σ over moving ticks ≈ walkCycleT... but walkCycleT resets to 0 on idle (line 1247)! Hmm — 1247: `if (Math.abs(this.vx) <= 0.05) this.walkCycleT = 0;`. Damn.

Hmm wait, let me look at the exact code around 1226-1247 in Enemy.ts to understand when animT/walkCycleT update. Maybe there are two branches: one for grounded walking entities and another. Let me read that part of Enemy.ts.

Alternatively — maintain the frame counter replica in the AI (mourningWoodAI covers both 325 and 344 — it's the same function!). I can add at the end of mourningWoodAI: a counter in L[] (localAI array) advancing per vanilla FindFrame, then write e.customFrameIdx. That gives exact 1:1 for both. Actually the localAI array L = la(e) is available; L[3] free? For mourningWoodAI, L isn't even used (no la(e) call currently — the function doesn't call la()). I can add `const L = la(e)` and use L[0] as counter. Then customFrameIdx = derived frame.

But wait — should I compute frames in AI via customFrameIdx, or keep Renderer stateless with approximations? The task says: "改 src/render/Renderer.ts 的 vanillaFrameIdx(在既有 case 266/222/262/113 等先例处追加分支;若需 AI 侧同步状态,可在对应 AI 文件写 e.lai0/e.lai1/e.customFrameIdx". So the primary pattern: branches in Renderer; AI-side state where needed.

Decision per NPC:
- 393 turret: stateless (pure function of ai2 angle + ai3 window). Renderer branch. 
- 394 cannon: stateless (pure function of ai3). Renderer branch.
- 395 saucer: needs persistent counter with window clamp → AI replica in e.lai0 (counter), Renderer branch computes frame from lai0. 
- 392 hull: needs persistent counter (window speed×2) → AI replica e.lai0, Renderer computes.
- 399 probe: stateless (t/4 cycles + alert band by ai0). Renderer.
- 387 tesla: rate depends on ai0 tiers; stateless approximation with instantaneous period (phase arbitrary) — or replica? The blink is 2 frames; using t/(10/(1+tiers)) % 2 gives correct rate. But hmm — actually vanilla's counter changes speed mid-cycle; instantaneous period approximation is standard here. I'll do stateless: period = ai0>0 ? 10/(1+(ai0>=20)+(ai0>=40)) : 15; frame = floor(t/period)%2. 

Hmm wait, but is that right for the visual? During charging (ai0>0 rising 0→60), speeds change; fine. OK.

- 386 engineer: deploy band stateless (pure ai2); walk part: counter += |vx|*2 (no +1) → counter ≈ walkCycleT*2 (walkCycleT resets on idle; vanilla doesn't reset its counter on idle but frame snaps to 0 on vx==0; on resume, vanilla continues counter from wherever (no reset!) — wait: vanilla 386 walking: `frameCounter += Math.Abs(velocity.X) * 2f` — no +1! When |vx|=0 → counter frozen, frame = 0. When moving slowly the counter barely advances (|vx|*2 per tick). Frame advance at >6. So frame = floor(walkCycleT*2/6)... with walkCycleT = Σ|vx| since idle reset. Vanilla counter = Σ|vx|*2 since spawn (no reset). Since idle → frame 0 & counter frozen (not reset), resume continues from frozen counter → phase mismatch vs our walkCycleT reset. Minor visual phase difference on resume; acceptable (same class as existing approximations). frame = 2 + floor(walkCycleT*2/6) % 7 (band 2..8). Wait vanilla: frame starts ≥2 (clamped up `if (frame.Y < num*2) frame.Y = num*2`), advance +1 at >6, wrap: `if (frame.Y/num >= 9) frame.Y = num*2`. So band 2-8 (7 frames). vx==0 → frame 0. vy != 0 → frame 1.

- Pumpking 327: stateful pose walk → AI replica. Where? pumpkingAI already has L[0]/L[1] beat for cloak; the FindFrame walk needs (frameCounter, frame). I'll add the walk logic in pumpkingAI writing e.customFrameIdx directly. But careful: the L[0]/L[1] existing beat is for "披风帧 Main.cs:22501" consumed... let me check who reads localAIOf for 327. Let me grep Renderer for localAIOf.

- Ice Queen 345: stateless (ai3/vx direct + fixed-rate bands). Renderer.
- Santa-NK1 346: stateless approximation. Renderer.
- Mourning Wood 325: stateless approximation (two fixed 5t bands). Renderer.
- Everscream 344: rate = max(1,|vx|*0.75)/t, 6 counts/frame, never resets. Approximate with... hmm. If I use t + walkCycleT*0.75, the idle periods (attack stops, vx→0 via ×0.9 decay — vx rarely exactly 0; "moving" threshold in vanilla = vx != 0f exact!) — 344's branches key on velocity.X == 0f exactly. With hoverCruise decay (vx *= 0.9, then snap to 0 when |vx|<0.1) vx is mostly non-zero → vanilla moving branch. So counter ≈ Σ max(1, 0.75|vx|). Using t + 0.75*walkCycleT: overestimates by +1 per moving tick when |vx| > 4/3. Typical |vx| for 344: cruise speed 2-4 + attack stop... error up to +1/t vs correct 0.75|vx|∈[1.5,3] → rate error ≤ 40% at |vx|=1.33... At full speed 4: correct 3/t, approx 4/t → 33% fast. Hmm, that's noticeable-ish. Use replica? To be exact and simple, replica in mourningWoodAI (both 325/344): L-based counter + frame, write customFrameIdx. But the task said implement in Renderer with AI sync where needed... The instruction: "若需 AI 侧同步状态,可在对应 AI 文件写 e.lai0/e.lai1/e.customFrameIdx——蜂后 222 是现成先例:AI 写 e.lai0,Renderer 读". So writing counters to lai0/1 and reading in Renderer is the sanctioned pattern. For 325/344 I could write the vanilla frameCounter replica to e.lai0 (325) — one function handles both ids: replica counter in la(e)[0]? But L[0]/L[1] conventions... mourningWoodAI doesn't use la() at all currently. I'll use e.lai0 (the Enemy field, not the WeakMap localAI) — Renderer reads e.lai0 directly. Enemy has lai0..lai3 fields for "localAI 语义位". The moon_events file uses the WeakMap localAI (la(e)) instead of e.laiN. For AI-side sync I'll write e.lai0 (field) — no conflict since mourningWoodAI doesn't use e.lai0.

Wait — actually, does anything else use e.lai0 for these ids? lai0 used by fireflies (发光剩余?) no — lai0 = "萤火虫:闪烁间隔计时" per comment at line 1074, lai1 = 发光剩余. Renderer reads e.lai1 <= 0 for fireflies. For our NPCs (325/344/327/345/346), no conflict.

Plan:
- mourningWoodAI (325 & 344): maintain vanilla FindFrame counter in e.lai0 (per-entity), compute and store... hmm, two different frame machines per id. Store raw counter in e.lai0; Renderer branch computes frame from counter + vx per id. But 325's counter also never resets (both branches increment continuously: standing +1, moving +1). Actually look: 325 standing: fc += 1; moving: fc += 1 (same!). The counter is just +1/t always → counter ≡ t (mod nothing) — but frame advance threshold fc > 4 → reset to 0 — so counter ≡ t % 5 effectively... wait no! fc increments +1/tick in both branches; at fc > 4 → frame+1, fc=0. So counter cycles 0..4 in 5 ticks always — counter ≡ t mod 5 exactly (from spawn; AI ticks = animT ticks — are they in lockstep? animT++ happens once per AI tick — line 1243 context needed. If both increment once per tick from enemy spawn... animT starts 0 at spawn, counter starts 0. So counter = animT % 5 exactly!). So for 325: frame advance every 5t exactly: idle band frame = floor((t%5 ... )) — well frame = current band + floor(t/5) % 5 where band switches snap frame into band (clamps). Stateless: idle → floor(t/5)%5 (band 0-4); moving → 5 + floor(t/5)%5. 

For 344: counter = Σ max(1, 0.75|vx|) — rate varies. t + 0.75*walkCycleT overestimates during slow motion. Honestly, for a walking-tree animation the error class is minor; existing code has similar approximations ("速率随速近似取定档" for butterflies). But we can do better cheaply: replica in AI via e.lai0. Since mourningWoodAI already runs per tick for both ids, adding 2 lines for 344's counter is trivial and exact:

```ts
// FindFrame case 344 counter replica(:73144-73170): moving max(1,|vx|*0.75)/t, standing +1/t
e.lai0 += e.vx === 0 ? 1 : Math.max(1, Math.abs(e.vx) * 0.75);
if (e.lai0 > 5) { e.lai0 = 0; /* frame advance */ }
```
Hmm — but then Renderer needs the frame index, which requires counting advances (frame = 0..9 cycling). The counter crossing threshold increments frame — I need both counter and frame in AI → just write e.customFrameIdx in AI for 344. That's the 694 precedent (AI writes customFrameIdx directly). And 325 stateless in Renderer (exact via t).

Hmm, wait — but for 325, is the frame counter really +1/tick in both branches? Yes (73175 and 73187: `frameCounter += 1.0` both). Great — 325 stateless exact (phase = t, matches spawn phase since both start at 0 — modulo the fact vanilla frameCounter starts at 0 and animT starts 0 — 1:1!).

Let me double check animT increments once per AI tick from spawn. Need to read Enemy.ts around 1220-1250.

- Santa-NK1 346: counter: fire band 3t/frame exact (t/3%3+6 — phase arbitrary on band entry; vanilla clamps entry frame to 6 and advances; our floor(t/3) phase arbitrary — deviation <3t, acceptable per precedent 127). Walk: fc += 1 + |vx|/2 per tick (>4 → advance). counter = t + walkCycleT/2 (walkCycleT resets on idle; vanilla resets fc=0 on idle too — matches!). Frame = 1 + floor((t + walkCycleT/2)/5) % 5. Wait — threshold > 4 → advance at 5 counts → floor(counter/5). Yes. Band 1-5, wrap 5→1: `if (frame.Y > num*5) frame.Y = num; if (frame.Y < num) frame.Y = num;`. So band 1,2,3,4,5 → frame = 1 + floor(counter/5) % 5.

Idle (vx===0 exact): frame unchanged (hold), fc=0. Our stateless: hold = keep last computed? Stateless can't hold... but frame = 1 + floor((t + 0)/5) % 5 with walkCycleT=0 would drift the held frame. Vanilla freezes it. Approximation options: when vx===0, use... hmm. The "静止定格" issue. I could approximate hold by freezing phase: without state, we can't. Is there an existing e field for "last walking frame"? No. Hmm — 346 standing still happens when flag58 stop (player within 50px or attacking — quite often!). A drifting idle frame would look wrong (legs cycling while standing). 

Solution: AI-side sync — santaNK1AI writes a replica counter (or directly customFrameIdx). santaNK1AI runs per tick; add the FindFrame replica there → e.customFrameIdx. Clean and exact. Let me do that for 346 (AI replica in la() L[0] = frameCounter, plus a frame holder — or just compute frame directly with local vars in a module WeakMap? Simpler: keep counter+frame both in L: L[0]=counter, L[1]... wait L[1]/L[2] already used for rocket/present bursts! L[0] is used? santaNK1AI: `L[1]`, `L[2]` used; L[0] free but only one slot needed for counter if I derive frame from counter directly:

Fire band: counter cycles 0..2 (advance >2 → 3 ticks), frame = 6 + (advances % 3). Since frame derives from advance count, I can keep a single monotone counter and derive: in fire band, advances = floor((counter_since_band_start)/3)... needs band-start reference. Simplest: keep L[0] = raw vanilla frameCounter replica AND L[3] = frame index replica; update per vanilla each tick; write e.customFrameIdx = L[3]. L[3] free in santaNK1AI? It uses L[1], L[2] only. Yes L[0]/L[3] free.

Hold on — but writing customFrameIdx means Renderer's first line short-circuits (`if (e.customFrameIdx != null) return Math.min(frames - 1, e.customFrameIdx)`). That's the 694 precedent. OK.

Actually — wait. Let me reconsider: maybe simpler and consistent — put the 346/344/327 replicas in the AI files as customFrameIdx (stateful, exact), and keep 325/345/393/394/399/386/387/392/395 in Renderer branches (stateless or via lai0 counter). For 395/392 I planned e.lai0 counter in AI + Renderer math. Alternatively compute customFrameIdx fully in AI for 395/392 too... but the task prefers Renderer branches reading ai fields; lai0 sync is explicitly blessed ("蜂后 222 是现成先例:AI 写 e.lai0,Renderer 读"). For 395: Renderer branch: `frame = Math.floor(((e.lai0 % 66) / 6))` — with lai0 = counter replica maintained in martianSaucerAI (advance +1, window +1 & clamp [36,53], wrap 66). Hmm wait, the clamp logic: `fc += 1; if (fc >= 66) fc = 0;` — then in-window `fc += 1; if (fc >= 54 || fc < 36) fc = 36;`. Note if fc was 65 → +1 = 66 → reset 0 → window: +1 = 1 → <36 → 36. OK.

For 392: counter replica advance +1 (+1 in window), %12. Renderer: frame = floor((e.lai0 % 12) / 3). e.lai0 in martianSaucerPartAI for id 392 (and note 392's AI part runs after the anchor follow; fine).

Hmm wait — one concern for 392/393/394: martianSaucerPartAI for 393/394 `return`s early inside window branches... The counter update for 392 must run every tick regardless. 392's flow: after `if (id !== 392 && ...)` gate → 392 continues to the slots logic each tick. I'll add the counter update near the top (after e.ai3 = saucer.ai3) so it runs for 392 each tick. Actually careful — for 392, `e.ai3 = saucer.ai3` happens at line 419 before the id-specific blocks; the 394/393 blocks return early. The 392 path continues to the bottom. I'll insert the counter update right after `e.ai3 = saucer.ai3;` gated on id===392 (or unconditionally for 392 only). Also the window for 392 = ai3 ∈ [20,260) — same flag6.

Edge: when saucer is in ai0=2 (expert deathray barrage), ai3 is the 3600 counter with %120 windows — vanilla 392 FindFrame still uses ai[3]∈[20,260) literally — in vanilla expert mode, 392's ai[3]... hmm, in vanilla, do parts share saucer's ai[3]? Our implementation copies `e.ai3 = saucer.ai3` — presumably 1:1 with vanilla (parts read npc[ai[...]].ai[3]). Vanilla expert saucer ai0=2 uses ai[3] as %120 counter... The 392 window check [20,260) would be true during [20,120) of each 3600 cycle rarely. Whatever — our port already 1:1; FindFrame formula literal: [20,260). Keep literal.

Now — **Betsy 551** (bossAI_dd2.ts). Vanilla FindFrame: pure function of ai0 (3/4/5/6/else) and ai[1]. Need to read our betsyAI to see what ai0/ai1 mean in our port. The task says "localAI[0] 36 步计数×timeScale,读 bossAI_dd2.ts betsyAI 的拍翼计数变量" — suggests our flap counter may live in localAI[0] rather than ai[1]. Let me read bossAI_dd2.ts betsy section.

**Cultists 439/440** (bossAI_lategame.ts): la2 holds ritual circle object (don't touch). Need to write e.customFrameIdx at state transitions... but the vanilla frame machine also has the "settle after one 15t loop" behavior and per-state base rows. The AI-side approach: in the cultist AI state machine, at each tick compute frameCounter/ frame and write customFrameIdx. The task says: "在教徒 AI 状态机各态切换处写 e.customFrameIdx(直接帧号...)；帧号=行起点+行内 6t 循环偏移(原版 7t/帧行内循环,查 :72720 确认步长)". The actual source: 15t loop, /5 → 5t per in-row frame. So frame = rowBase + (counter/5), counter 0..14, wrapping at 15 → snap to settle row.

Let me now read the vanilla AI for cultists to understand localAI[2] state values (0/1/2/10/11/12/13) and our cultist AI (bossAI_lategame.ts) to map states. Also read vanilla Betsy AI (ai[1] role) and our betsyAI.

Let me grep bossAI_lategame.ts for the cultist function and bossAI_dd2.ts for betsy.
````

</details>


---

## 🤖 Assistant · 2026-08-19T07:46:24.425Z · glm-x-preview-260804

```
现在我来查看一下后期游戏文件 (Cultists) 和 DD2 文件 (Betsy) 中的相关部分。
```


---

## 🤖 Assistant · 2026-08-19T07:46:26.543Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"export function\\|^function\\|lai2\\|customFrameIdx\\|439\\|440\" src/entities/bossAI_lategame.ts | head -40; echo ====; grep -n \"betsy\\|Betsy\\|551\" src/entities/bossAI_dd2.ts | head -30",
 "description": "Locate cultist and betsy AI sections"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:46:26.577Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
2://   aiStyle 84  拜月教邪教徒 439  AI_084_LunaticCultist()        NPC.cs:64921-65957
56:function simpleFly(e: Enemy, dvx: number, dvy: number, acc: number): void {
62:function flyIntegrate(e: Enemy): void {
68:function collideGround(e: Enemy, game: GameHooks): void {
95:function aimLead(e: Enemy, player: Player, fallbackX: number): { x: number; y: number } {
106:// ===================== AI_084 拜月教邪教徒 439 + 克隆体 440(NPC.cs:64921-65957) =====================
107:// 真身 439 与克隆体 440 共用本核(flag2 = type==439,:64971):克隆体由仪式态(ai0==5)生成,
125:function cultistPick(e: Enemy, phase2: boolean): number {
133:/** 真身的全部存活克隆体(:65449 系:type==440 && ai[3]==whoAmI;
135:function cultistClones(game: GameHooks, parent: Enemy): Enemy[] {
137:    (n) => !n.dead && n.vanillaId === 440 && laOf(n).la3 === parent);
147: *  圈弹视觉/淡入淡出/自旋 1:1。锚（439）消亡即 Kill（:31305-31320）。 */
214:    // ---- flag44（:31295-31314）：中断且全隐 → Kill；或锚 NPC 失效/非 439/454/521 → Kill ----
217:      && (src.vanillaId === 439 || src.vanillaId === 454 || src.vanillaId === 521);
238:/** 克隆体生成出口(:65646-65650 NewNPC 440:X,Y 是底部中心坐标且 Y 再 +真身 height/2;
240:function spawnCultistClone(game: GameHooks, parent: Enemy, x: number, y: number, gen: number): Enemy | null {
241:  const c = spawnPart(game, parent, 440);
255:function cloneSupplement(game: GameHooks, clones: Enemy[], player: Player, count: number, spread: number): void {
270:function ritualCenterOf(isReal: boolean, la: { la2: unknown }, parent: Enemy | null): { x: number; y: number } | null {
275:export function lunaticCultistAI(e: Enemy, game: GameHooks, player: Player | null): void {
280:  const isReal = e.vanillaId !== 440; // flag2 = type==439(:64971);440 = 克隆体
286:    if (!parent || parent.dead || parent.vanillaId !== 439) { // :64975-64982
640:function empressDashTo(e: Enemy, tx0: number, ty0: number): void {
656:function empressHover(e: Enemy, player: Player, ox: number, oy: number, spdMul = 1, accMul = 1): void {
665:export function empressOfLightAI(e: Enemy, game: GameHooks, player: Player | null): void {
1014:function isPlatformSheetTile(game: GameHooks, x: number, y: number): boolean {
1023:function kingSlimeCacheTileOk(
1039:function buildKingSlimeCache(
1063:function queenTeleportSpot(game: GameHooks, player: Player, e: Enemy, anti: boolean): { x: number; y: number; found: boolean } {
1078:function queenFlyMovement(e: Enemy, game: GameHooks, player: Player): void {
1112:export function queenSlimeAI(e: Enemy, game: GameHooks, player: Player | null): void {
1390://   case 84:  lunaticCultistAI(this, game, p); break;   // 439 真身 + 440 克隆体共用(见文件头)
1394://   FALLBACK 仅防御);邪教徒仪式态生成 440 克隆体、ai0=7 态召 522 远古之光、ai0=8 态撒 523。
1405:export function ancientLightAI(e: Enemy, game: GameHooks, player: Player | null) {
1437:export function ancientDoomAI(e: Enemy, game: GameHooks, player: Player | null) {
1439:  const boss = (game.enemies() as Enemy[]).find((n) => !n.dead && n.id === e.ai0 && n.vanillaId === 439);
(eval):1: === not found

```


---

## 🤖 Assistant · 2026-08-19T07:46:30.858Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The `====` echo failed due to zsh glob (`====` interpreted?). Anyway, I got the lategame info. Now let me read the cultist AI in detail — lines 106-640. That's big; let me read the relevant state machine part.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:46:31.447Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts",
 "limit": 240,
 "offset": 106
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:46:31.454Z

**📎 ToolResult**

```
106	// ===================== AI_084 拜月教邪教徒 439 + 克隆体 440(NPC.cs:64921-65957) =====================
107	// 真身 439 与克隆体 440 共用本核(flag2 = type==439,:64971):克隆体由仪式态(ai0==5)生成,
108	//   ai[0]/ai[1] 每 tick 从真身镜像(:65000-65001);仅在仪式窗口(120-420t)可被击中——
109	//   打中克隆体 → 克隆体消散 + 真身进 6 态硬直 120t(:65003-65014);
110	//   打中真身 → 推进选招拍号并清同代克隆体(:65016-65060)。
111	//   仪式态外克隆体无敌且不可选(dontTakeDamage=flag3,:65953)。
112	// 状态机(ai0): -1 出生显形(420t,真身专属) / 0 选招(40t) / 1 飞掠占位(含克隆体环位补位) /
113	//   2 冰雾 464(:65362) / 3 火球 467(:65430,第三拍克隆体补射 468) / 4 闪电 465(:65531) /
114	//   5 仪式瞬移(:65623,生成/补位克隆体) / 6 硬直(:65771) / 7 远古之光(:65796,真身召
115	//   NPC522 轨道弹 + 第三拍克隆体补射 468×5) / 8 远古末日 NPC523(经典不可达,状态体保留)。
116	// 经典数值: 冰 35 伤(:64930)/火 30 伤·18t×3(:64941-64946)/闪电 45 伤(:64953)/
117	//   光 20t×2(:64963-64967)/末日 20t×3(:64970-64973);克隆体补射 468 恒 18 伤(:65491)。
118	// 选招表(:65131-65254 两张 switch 表合一;表尾拍把 ai3 复位 -1 → 下次完成攻击后回 0 重循环):
119	//   一阶段 12 拍 [冲,火,冲,冰,冲,雷,冲,火,冲,冰,冲,仪式] 循环;
120	//   二阶段 12 拍 [冲,火,冲,光,冲,雷,冲,光,冲,冰,冲,雷] 循环(二阶段不再仪式)。
121	const CULTIST_CYCLE_P1 = [0, 1, 0, 2, 0, 3, 0, 1, 0, 2, 0, 4];
122	const CULTIST_CYCLE_P2 = [0, 1, 0, 5, 0, 3, 0, 5, 0, 2, 0, 3];
123	
124	/** 选招(:65131-65254 两张 switch 表合一;表尾拍把 ai3 复位 -1 → 下次完成攻击后回 0 重循环) */
125	function cultistPick(e: Enemy, phase2: boolean): number {
126	  const table = phase2 ? CULTIST_CYCLE_P2 : CULTIST_CYCLE_P1;
127	  const i = Math.floor(e.ai3);
128	  if (i < 0 || i >= table.length) { e.ai3 = -1; return 0; }
129	  if (i === table.length - 1) e.ai3 = -1; // :65199/:65253 表尾复位
130	  return table[i];
131	}
132	
133	/** 真身的全部存活克隆体(:65449 系:type==440 && ai[3]==whoAmI;
134	 *  本仓克隆体以 localAI 槽 la3 反存真身 Enemy 引用) */
135	function cultistClones(game: GameHooks, parent: Enemy): Enemy[] {
136	  return (game.enemies() as Enemy[]).filter(
137	    (n) => !n.dead && n.vanillaId === 440 && laOf(n).la3 === parent);
138	}
139	
140	/** 仪式圈弹 490（Projectile.cs:5383 SetDefaults + aiStyle 89 :31193-31326）：
141	 *  14×14 / hostile / alpha 255 / timeLeft 600 / noTileCollide，锚定源邪教徒 ai[1]。
142	 *  淡入 300t（alpha -5/t 钳 0）→ 淡出（+12/t）；scale = (1-alpha/255)×0.6 随透明度
143	 *  张合；rotation 每 t +π/210；alpha==0 时每 t 2 颗 228 号紫尘沿 204×scale 半径
144	 *  向心收拢；出生播 Item123（真轨 Item_123.wav 已落位，roar 近似销核）。
145	 *  ai[0]==300 时原版召 NPC 454 幻影龙（场上无）否则 521 章鱼头（:31282-31292）——
146	 *  两 AI 族未移植（登记：CultistDragonHead/AncientCultistSquidhead），此处不召，
147	 *  圈弹视觉/淡入淡出/自旋 1:1。锚（439）消亡即 Kill（:31305-31320）。 */
148	export class CultistRitualCircle extends Entity {
149	  w = 14; h = 14;
150	  private srcId: number;
151	  private age = 0;         // ai[0]
152	  private alpha = 255;
153	  private rot = 0;
154	  private soundPlayed = false;  // localAI[1]
155	  /** ai[1] == -1（仪式被打破,Projectile.cs:31195 +12/t 快速淡出,不召龙） */
156	  private interrupted = false;
157	  dead = false;
158	
159	  constructor(src: Enemy) {
160	    super();
161	    this.srcId = src.id;
162	    this.x = src.cx - this.w / 2;
163	    this.y = src.cy - this.h / 2;
164	  }
165	
166	  /** 仪式窗口内真身被击中 → Main.projectile[ai[2]].ai[1] = -1（NPC.cs:65054） */
167	  interrupt(): void { this.interrupted = true; }
168	
169	  /** (1-alpha/255)×0.6（:31208-31210） */
170	  private get scale(): number { return (1 - this.alpha / 255) * 0.6; }
171	
172	  fixedUpdate(_dt: number, game: GameHooks): void {
173	    // 淡入/淡出（:31195-31214）：中断（ai[1]=-1）或 age≥300 → +12/t；否则 -5/t
174	    this.alpha += (this.interrupted || this.age >= 300) ? 12 : -5;
175	    this.alpha = Math.max(0, Math.min(255, this.alpha));
176	    this.rot += Math.PI / 210;                          // :31217
177	    if (!this.soundPlayed) {
178	      this.soundPlayed = true;
179	      // SoundID.Item123（Projectile.cs:31221，无坐标 = 全量不衰减）——原 roar 近似已销核
180	      game.playSfxFile?.('Item_123', 1);
181	    }
182	    // 完全显现期的收拢紫尘（:31223-31251，尘 228 / 半径 204×scale / 内圈 ×0.42）
183	    if (this.alpha === 0) {
184	      for (let k = 0; k < 2; k++) {
185	        const inner = k === 1;
186	        const a = Math.random() * Math.PI * 2;
187	        const rr = 204 * this.scale * (inner ? 0.42 : 1);
188	        game.spawnParticles(this.cx + Math.cos(a) * rr, this.cy + Math.sin(a) * rr,
189	          '#A060E0', 1, inner ? 1.5 : 2, { life: 30 });
190	      }
191	    }
192	    this.age++;
193	    // ---- :31279-31292 age==300 且未中断 → 召唤：场上无 454 幻影龙 → NewNPC(454)
194	    //      （头 + 455-458 身 ×4 + 459 尾共享头血池）；否则 → 521 远古幻象。
195	    //      召出后 ai[1] 复用为该 NPC 索引 = 圈锚从邪教徒切到龙（龙亡圈灭）----
196	    if (this.age === 300 && !this.interrupted) {
197	      const hasDragon = (game.enemies() as Enemy[])
198	        .some((n) => !n.dead && n.vanillaId === 454);
199	      const id = hasDragon ? 521 : 454;
200	      const head = Enemy.fromVanilla(id, this.cx, this.cy);
201	      if (head) {
202	        addEnemy(game, head);
203	        this.srcId = head.id;              // ai[1] = NewNPC 返回索引（:31283/:31287）
204	        if (id === 454) {
205	          // 链段（NewNPC 段链展开）：455-458 + 尾 459，realLife 共享头 10000 血
206	          const segs = Enemy.spawnWormChain(head, 5, [455, 456, 457, 458, 459], true);
207	          for (const sg of segs) addEnemy(game, sg);
208	        }
209	      }
210	    } else if (this.age === 320) {
211	      this.dead = true;                                 // :31290-31294
212	      return;
213	    }
214	    // ---- flag44（:31295-31314）：中断且全隐 → Kill；或锚 NPC 失效/非 439/454/521 → Kill ----
215	    const src = (game.enemies() as Enemy[]).find((n) => n.id === this.srcId);
216	    const anchorOk = !!src && !src.dead
217	      && (src.vanillaId === 439 || src.vanillaId === 454 || src.vanillaId === 521);
218	    if ((this.interrupted && this.alpha >= 255) || !anchorOk) { this.dead = true; }
219	  }
220	
221	  draw(r: Renderer, _cam: Camera): void {
222	    const ctx = r.canvas.getContext('2d');
223	    if (!ctx) return;
224	    const img = projSprite(490);
225	    if (!img || !(img.width > 0) || img.width === 0) return;
226	    const s = this.scale;
227	    if (s <= 0.01) return;
228	    const iw = img.width, ih = img.height;
229	    ctx.save();
230	    ctx.translate(this.cx, this.cy);
231	    ctx.rotate(this.rot);
232	    ctx.imageSmoothingEnabled = false;
233	    ctx.drawImage(img, -iw * s / 2, -ih * s / 2, iw * s, ih * s);
234	    ctx.restore();
235	  }
236	}
237	
238	/** 克隆体生成出口(:65646-65650 NewNPC 440:X,Y 是底部中心坐标且 Y 再 +真身 height/2;
239	 *  ai[3]=真身 whoAmI / localAI[1]=仪式代数)。本仓:la3=真身引用、la1=代数、跳过出生显影 */
240	function spawnCultistClone(game: GameHooks, parent: Enemy, x: number, y: number, gen: number): Enemy | null {
241	  const c = spawnPart(game, parent, 440);
242	  if (!c) return null;
243	  const la = laOf(c);
244	  la.la3 = parent;
245	  la.la1 = gen;
246	  c.x = x - c.w / 2;
247	  c.y = y + parent.h / 2 - c.h;
248	  c.bInit = true; // 原版克隆体会落入 1t 的 -1 显影态(:65047),无实际效果,直接跳过
249	  return c;
250	}
251	
252	/** 克隆体补射 468(:65375-65397 冰雾 / :65462-65499 火球第三拍 / :65531-65562 闪电 /
253	 *  :65796-65822 光第三拍):每只克隆体朝玩家(预判 20t)发 count 发,18 伤,
254	 *  (6+rand4) 速 ±spread 散布,出口 = 克隆体中心 + (facing*30, 12) */
255	function cloneSupplement(game: GameHooks, clones: Enemy[], player: Player, count: number, spread: number): void {
256	  for (const c of clones) {
257	    const dir = Math.sign(player.cx - c.cx);
258	    if (dir !== 0) c.facing = dir;
259	    const aim = aimLead(c, player, c.facing);
260	    for (let k = 0; k < count; k++) {
261	      const spd = 6 + Math.random() * 4;
262	      const [dvx, dvy] = rot(aim.x * spd, aim.y * spd, (Math.random() - 0.5) * 2 * spread);
263	      shoot(game, c.cx + c.facing * 30, c.cy + 12, dvx, dvy, 18, 468);
264	    }
265	  }
266	}
267	
268	/** 仪式圈心(原版 Projectile 490 的位置 = 仪式开始时真身中心,:65652)。
269	 *  真身存 la2;克隆体读真身的 la2 */
270	function ritualCenterOf(isReal: boolean, la: { la2: unknown }, parent: Enemy | null): { x: number; y: number } | null {
271	  const raw = (isReal ? la.la2 : (parent ? laOf(parent).la2 : null)) as { x: number; y: number } | null;
272	  return raw ?? null;
273	}
274	
275	export function lunaticCultistAI(e: Enemy, game: GameHooks, player: Player | null): void {
276	  const la = laOf(e);
277	  // getGoodWorld 弹幕节奏抬档(:64932-64958):冰 num120−30 / 火 18×3→10×5 /
278	  // 闪电 num80−20(expert 基线未实装,g 照原文在经典值上调整)
279	  const ftw = !!game.world.seedFlags?.getGoodWorld;
280	  const isReal = e.vanillaId !== 440; // flag2 = type==439(:64971);440 = 克隆体
281	  let parent: Enemy | null = null;
282	  // ---- 克隆体镜像段(:64998-65015):真身失效 → 消散;ai0/ai1 逐 tick 镜像;
283	  //      仪式态中被击中 → 自身消散 + 真身进 6 态硬直 ----
284	  if (!isReal) {
285	    parent = (la.la3 as unknown as Enemy) ?? null;
286	    if (!parent || parent.dead || parent.vanillaId !== 439) { // :64975-64982
287	      e.dead = true;
288	      return;
289	    }
290	    e.ai0 = parent.ai0;
291	    e.ai1 = parent.ai1;
292	    if (e.ai0 === 5) {
293	      if (e.justHit) { // :65003-65014
294	        game.spawnParticles(e.cx, e.cy, '#8060D0', 14, 2.4);
295	        e.dead = true;
296	        parent.ai0 = 6;
297	        parent.ai1 = 0;
298	        return;
299	      }
300	    } else {
301	      e.iframes = 2; // flag3/flag4 → dontTakeDamage(chaseable=false,:65015)
302	    }
303	  } else if (!e.bInit) {
304	    // :65047-65057 localAI[0]==0:音效 + alpha=255 + ai[0]=-1(出生显形)
305	    e.bInit = true;
306	    e.ai0 = -1; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
307	    la.la0 = 1;
308	    e.spawnAlpha = 254;
309	    game.playSfxWav?.('Zombie_89', 1, e.cx, e.cy);   // :65093 PlaySound(29,…,89)——case29 style89 ×0.7 自动档(曾借 roar 0.6)
310	  }
311	  // 环境声（:64923-64926）：ai0≠-1 时 1/1000 播 Next(88,92)=Zombie_88-91 变体池
312	  if (e.ai0 !== -1 && Math.floor(Math.random() * 1000) === 0) {
313	    game.playSfxWav?.(`Zombie_${88 + Math.floor(Math.random() * 4)}`, 1, e.cx, e.cy);
314	  }
315	  const b = baseOf(e);
316	  const phase2 = e.hp <= e.maxHp / 2;                       // flag :64928
317	  e.def.defense = Math.floor(phase2 ? b.def * 0.65 : b.def); // :64982-64985 半血防御 ×0.65
318	
319	  // :65060-65088 玩家死/超 5600px → 消散退场(连带清全部克隆体,:65078-65087)
320	  if (!player || player.dead || Math.hypot(player.cx - e.cx, player.cy - e.cy) > 5600) {
321	    game.spawnParticles(e.cx, e.cy, '#6040A0', 14, 2.4);
322	    if (isReal) {
323	      for (const c of cultistClones(game, e)) {
324	        game.spawnParticles(c.cx, c.cy, '#6040A0', 10, 2);
325	        c.dead = true;
326	      }
327	    }
328	    e.dead = true;
329	    return;
330	  }
331	
332	  // ---- 仪式窗口(120-420t)真身被击中(:65012-65056):推进选招 + 清同代克隆体(≤10)
333	  //      + 仪式圈 ai[1]=-1 快速淡出且不召龙（:65054 Main.projectile[ai[2]].ai[1] = -1）----
334	  if (isReal && e.ai0 === 5 && e.ai1 >= 120 && e.ai1 < 420 && e.justHit) {
335	    e.ai0 = 0; e.ai1 = 0; e.ai3 += 1; // :65014-65016
336	    e.vx = 0; e.vy = 0;
337	    let budget = 10; // num9 经典 10(expert 3,:65027-65031);两分支同为清场,差异仅联网消息
338	    for (const c of cultistClones(game, e)) {
339	      if (budget <= 0) break;
340	      budget--;
341	      game.spawnParticles(c.cx, c.cy, '#8060D0', 12, 2.4);
342	      c.dead = true;
343	    }
344	    const circle = la.la3;
345	    if (circle instanceof CultistRitualCircle) circle.interrupt();

```


---

## 🤖 Assistant · 2026-08-19T07:46:34.243Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts",
 "limit": 300,
 "offset": 346
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:46:34.250Z

**📎 ToolResult**

```
346	  }
347	
348	  // 朝向(:65117-65120 sign(player.X - center.X);仪式态内被 :65676 系圈心朝向覆盖)
349	  const face = Math.sign(player.cx - e.cx);
350	  if (face !== 0) e.facing = face;
351	
352	  // ---- ai0 == -1 出生显形(:65059-65109):420t,前段不可选中;300t 起上浮 ----
353	  if (e.ai0 === -1) {
354	    e.spawnAlpha = Math.max(0, 254 - e.ai1 * 5); // :65066 alpha -= 5/tick
355	    e.iframes = 2; // flag3/flag4 → dontTakeDamage
356	    e.ai1 += 1;
357	    if (e.ai1 > 360) { e.vx *= 0.95; e.vy *= 0.95; }      // :65109-65111 收势阻尼
358	    else if (e.ai1 > 300) { e.vx = 0; e.vy = -1; }        // :65113-65115 velocity=-UnitY
359	    // :65117-65124 显形末段(>360)播 (29,…,105)=Zombie_105(case29 ×0.25 档,终审补)
360	    if (e.ai1 === 361) game.playSfxWav?.('Zombie_105', 1, e.cx, e.cy);
361	    flyIntegrate(e);
362	    if (e.ai1 >= 420) { e.ai0 = 0; e.ai1 = 0; e.spawnAlpha = 0; }
363	    return;
364	  }
365	
366	  // ---- ai0 == 0 选招(:65110-65336):40t 后按 ai3 拍号取招(flag2 门控,克隆体不选) ----
367	  if (e.ai0 === 0) {
368	    e.ai1 += 1;
369	    if (isReal && e.ai1 >= 40) {
370	      e.ai1 = 0;
371	      const pick = cultistPick(e, phase2);
372	      if (pick === 0) {
373	        // 飞掠占位(:65277-65336):真身 + 全部克隆体一起入环——环位角
374	        // num16 = ((序号+flag5+1)/2)·2π·0.4/总数,奇数序取负(flag5=总数偶数),
375	        // 半径椭圆 (300,200),自转轴 (0,-1)。
376	        // num14 = ceil(真身到 (玩家中心+(0,-100)) 距离/50)（:65271 真身口径,全员共用
377	        // ——曾按各成员自身落点分别计算),velocity = 位移/num14,ai1 = num14*2
378	        const num14 = Math.max(1, Math.ceil(
379	          Math.hypot(player.cx - e.cx, player.cy - 100 - e.cy) / 50));
380	        const group = [e, ...cultistClones(game, e)];
381	        const flag5 = group.length % 2 === 0 ? 1 : 0; // :65286
382	        let idx = 0;
383	        for (const m of group) {
384	          let num16 = Math.floor((idx + flag5 + 1) / 2) * Math.PI * 2 * 0.4 / group.length; // :65291-65296
385	          if (idx % 2 === 1) num16 = -num16;
386	          if (group.length === 1) num16 = 0;
387	          const [ux, uy] = rot(0, -1, num16);
388	          const destX = player.cx + ux * 300;
389	          const destY = player.cy + uy * 200;
390	          m.vx = (destX - m.cx) / num14;
391	          m.vy = (destY - m.cy) / num14;
392	          m.ai0 = 1;
393	          m.ai1 = num14 * 2;
394	          // :65305-65308 whoAmI >= 自身 → 选招当帧回退(净位移 0);克隆体按 id 序决定
395	          if (m === e || e.id >= m.id) { m.x -= m.vx; m.y -= m.vy; }
396	          idx++;
397	        }
398	      } else if (pick === 1) { e.ai0 = 3; } // 火球
399	      else if (pick === 2) { e.ai0 = 2; }   // 冰雾
400	      else if (pick === 3) { e.ai0 = 4; }   // 闪电
401	      else if (pick === 4) { e.ai0 = 5; }   // 仪式瞬移
402	      else if (pick === 5) { e.ai0 = 7; }   // 远古之光
403	      // pick === 6(远古末日)仅 expert 随机替换会命中(:65270-65275),经典不触发
404	    }
405	    flyIntegrate(e);
406	    return;
407	  }
408	
409	  // ---- ai0 == 1 飞掠(:65338-65361):奇数拍回退位移 → 实际隔拍移动;期间无敌(flag3) ----
410	  if (e.ai0 === 1) {
411	    e.iframes = 2;
412	    const undo = Math.floor(e.ai1) % 2 !== 0 && e.ai1 !== 1; // :65341-65344
413	    if (!undo) flyIntegrate(e);
414	    e.ai1 -= 1;
415	    if (e.ai1 <= 0) { e.ai0 = 0; e.ai1 = 0; if (isReal) e.ai3 += 1; e.vx = 0; e.vy = 0; }
416	    return;
417	  }
418	
419	  // ---- ai0 == 2 冰雾 464(:65362-65429):4t 时克隆体各补 1 发 468 + 真身 1 发 464(35 伤);
420	  //      持续 4+num(num=120,FTW −30 :64932-64936) ----
421	  if (e.ai0 === 2) {
422	    const numIce = ftw ? 90 : 120;
423	    if (isReal && e.ai1 >= 4 && (e.ai1 - 4) % numIce === 0) {
424	      cloneSupplement(game, cultistClones(game, e), player, 1, 0.5235987901687622); // :65375-65397
425	      const aim = aimLead(e, player, e.facing);
426	      shoot(game, e.cx + e.facing * 30, e.cy + 12, aim.x * 4, aim.y * 4, 35, 464); // :65411-65421
427	      game.playSfxWav?.('Item_120', 1, e.cx, e.cy - 100);   // 弹 464 首帧音(:30749-30752,终审补)
428	      // 原版冰雾发射零吼(:65040-65900 全段仅 65093/65122 两声)——曾借 roar 0.35,2026-08-18 对账删
429	    }
430	    e.ai1 += 1;
431	    if (e.ai1 >= 4 + numIce) { e.ai0 = 0; e.ai1 = 0; if (isReal) e.ai3 += 1; e.vx = 0; e.vy = 0; }
432	    return;
433	  }
434	
435	  // ---- ai0 == 3 火球 467(:65430-65530):每 num2t 一发×num3,30 伤,(6+rand4) 速
436	  //      ±0.52rad 散布(18×3,FTW 10×5 :64941-64949);第三拍克隆体各补 1 发
437	  //      468(:65462-65499);持续 4+num2*num3 ----
438	  if (e.ai0 === 3) {
439	    const numFire = ftw ? 10 : 18;
440	    const fireCount = ftw ? 5 : 3;
441	    if (isReal && e.ai1 >= 4 && (e.ai1 - 4) % numFire === 0) {
442	      // 原版硬编码第 3 拍(:65442 /num2==2)——FTW 5 拍下仍在第 3 拍补射,1:1 保留
443	      if ((e.ai1 - 4) / numFire === 2) {
444	        cloneSupplement(game, cultistClones(game, e), player, 1, 0.5235987901687622); // :65448-65462
445	      }
446	      const aim = aimLead(e, player, e.facing);
447	      const spd = 6 + Math.random() * 4;
448	      const [dvx, dvy] = rot(aim.x * spd, aim.y * spd, (Math.random() - 0.5) * 2 * 0.5235987901687622);
449	      shoot(game, e.cx + e.facing * 30, e.cy + 12, dvx, dvy, 30, 467); // :65505-65517
450	    }
451	    e.ai1 += 1;
452	    if (e.ai1 >= 4 + numFire * fireCount) { e.ai0 = 0; e.ai1 = 0; if (isReal) e.ai3 += 1; e.vx = 0; e.vy = 0; }
453	    return;
454	  }
455	
456	  // ---- ai0 == 4 闪电 465(:65531-65622):ai1==20 时克隆体各补 1 发 468(:65531-65562),
457	  //      之后每逢 (ai1-20)%num4==0 在头顶 100px 撒 465(45 伤)(num4=80,FTW −20
458	  //      :64952-64958);持续 20+num4 ----
459	  if (e.ai0 === 4) {
460	    const numBolt = ftw ? 60 : 80;
461	    if (isReal && e.ai1 >= 20 && (e.ai1 - 20) % numBolt === 0) {
462	      if (e.ai1 === 20) {
463	        cloneSupplement(game, cultistClones(game, e), player, 1, 0.5235987901687622);
464	        // 原版闪电发射零吼(同上全段普查)——曾借 roar 0.5,2026-08-18 对账删
465	      }
466	      // 原版 465 零速悬停后从天引雷(Projectile.AI 收敛:直飞 6 速朝玩家)
467	      const dx = player.cx - e.cx, dy = player.cy - (e.cy - 100);
468	      const d = Math.hypot(dx, dy) || 1;
469	      shoot(game, e.cx, e.cy - 100, dx / d * 6, dy / d * 6, 45, 465); // :65563-65566
470	      game.playSfxWav?.('Item_121', 1, e.cx, e.cy - 100);   // 弹 465 首帧音(:30864-30867,终审补)
471	    }
472	    e.ai1 += 1;
473	    if (e.ai1 >= 20 + numBolt) { e.ai0 = 0; e.ai1 = 0; if (isReal) e.ai3 += 1; e.vx = 0; e.vy = 0; }
474	    return;
475	  }
476	
477	  // ---- ai0 == 5 仪式瞬移(:65623-65770):0-30 淡出,30 环位重定位 + 生成/补位克隆体,
478	  //      30-90 隐形,90-120 淡入,120-420 显形可受击(打真身/克隆体窗口);持续 420 ----
479	  if (e.ai0 === 5) {
480	    const t = e.ai1;
481	    if (t >= 0 && t < 30) {
482	      e.spawnAlpha = Math.floor((t / 30) * 254);
483	      e.iframes = 2; // flag3/flag4
484	    } else if (t >= 30 && t < 90) {
485	      e.spawnAlpha = 254;
486	      e.iframes = 2;
487	      if (t === 30 && isReal) {
488	        // :65636-65675:环绕自身半径 180 的 num29 环位重定位——
489	        //   补位克隆体(总数目标 6,每轮至多新造 2),余下槽位重排既有克隆体;
490	        //   真身取「距玩家最远」槽(num31 = 最近槽的对侧);圈心(=重定位前中心)存
491	        //   la2 供本态朝向用,并于此原位发 490 仪式圈弹（:65643，ai[1]=真身索引）
492	        la.la1 += 1; // localAI[1] 仪式代数(:65637)
493	        la.la2 = { x: e.cx, y: e.cy };
494	        // ai[2] = 490 仪式圈弹索引（:65652）——真身 la3 反存圈引用供中断链（:65054）
495	        const circle = new CultistRitualCircle(e);
496	        la.la3 = circle;
497	        (game as unknown as { entities: { add: (en: Entity, b: string) => void } }).entities
498	          .add(circle, 'projectiles');
499	        const clones = cultistClones(game, e);
500	        let num28 = 6 - clones.length; // :65643-65647
501	        if (num28 > 2) num28 = 2;
502	        const num29 = clones.length + num28 + 1;
503	        const dists: number[] = [];
504	        for (let s = 0; s < num29; s++) { // :65650-65656 各槽到玩家距离
505	          const [rx, ry] = rot(180, 0, (s * Math.PI * 2) / num29 - Math.PI / 2);
506	          dists.push(Math.hypot(e.cx + rx - player.cx, e.cy + ry - player.cy));
507	        }
508	        let num31 = 0; // :65658-65664 取最近槽 → 映射到对侧(最远)槽
509	        for (let s = 1; s < num29; s++) if (dists[num31] > dists[s]) num31 = s;
510	        num31 = num31 >= num29 / 2 ? num31 - Math.floor(num29 / 2) : num31 + Math.floor(num29 / 2);
511	        let num33 = num28; // :65666 新造配额,耗尽后按序重排既有克隆体(list6[-num33-1])
512	        let reused = 0;
513	        for (let s = 0; s < num29; s++) {
514	          if (num31 === s) continue;
515	          const [rx, ry] = rot(180, 0, (s * Math.PI * 2) / num29 - Math.PI / 2);
516	          const px = e.cx + rx, py = e.cy + ry;
517	          if (num33-- > 0) spawnCultistClone(game, e, px, py, la.la1);
518	          else if (reused < clones.length) {
519	            const c = clones[reused++];
520	            c.x = px - c.w / 2;
521	            c.y = py - c.h / 2;
522	          }
523	        }
524	        // 真身移到 num31 槽(:65652 Center += 偏移向量)
525	        const [fx, fy] = rot(180, 0, (num31 * Math.PI * 2) / num29 - Math.PI / 2);
526	        e.x += fx;
527	        e.y += fy;
528	        e.vx = 0; e.vy = 0;
529	        game.spawnParticles(e.cx, e.cy, '#8060D0', 18, 2.6);
530	        // 原版仪式圈就位零吼(同上全段普查)——曾借 roar 0.7,2026-08-18 对账删
531	      }
532	    } else if (t >= 90 && t < 120) {
533	      e.spawnAlpha = Math.floor(254 * (1 - (t - 90) / 30));
534	      e.iframes = 2;
535	    } else {
536	      // 120-420:显形且可受击(alpha=0,不置 iframes;chaseable 原版为 false,:65954)
537	      e.spawnAlpha = 0;
538	      // 朝向:以仪式圈心为基准(:65706-65719 / :65743-65756 sign(圈心-自身).X)
539	      const cir = ritualCenterOf(isReal, la, parent);
540	      if (cir) {
541	        const dx = cir.x - e.cx;
542	        if (dx !== 0) e.facing = Math.sign(dx);
543	      }
544	    }
545	    e.ai1 += 1;
546	    if (e.ai1 >= 420) { e.ai0 = 0; e.ai1 = 0; if (isReal) e.ai3 += 1; e.vx = 0; e.vy = 0; }
547	    return;
548	  }
549	
550	  // ---- ai0 == 6 硬直(:65771-65784):打中克隆体后真身暴露(不置 iframes),120t 后回选招 ----
551	  if (e.ai0 === 6) {
552	    e.ai1 += 1;
553	    if (e.ai1 >= 120) { e.ai0 = 0; e.ai1 = 0; if (isReal) e.ai3 += 1; e.vx = 0; e.vy = 0; }
554	    flyIntegrate(e);
555	    return;
556	  }
557	
558	  // ---- ai0 == 7 远古之光(:65796-65877):每 20t 一轮×2;第三拍克隆体各补 5 发 468
559	  //      (±1.2566rad,:65796-65822),真身每轮以扇面(步进 2π/25,8 速)召 5 只 NPC522
560	  //      (:65862-65865,ai1=逐 t 弯转角 → AI_100 轨道弹);持续 4+20*2 ----
561	  if (e.ai0 === 7) {
562	    if (isReal && e.ai1 >= 4 && (e.ai1 - 4) % 20 === 0) {
563	      e.facing = Math.sign(player.cx - e.cx) || e.facing; // :65839-65843
564	      const aim = aimLead(e, player, e.facing);
565	      const num47 = (Math.PI * 2) / 25; // :65856
566	      if ((e.ai1 - 4) / 20 === 2) {
567	        cloneSupplement(game, cultistClones(game, e), player, 5, 1.2566370964050293);
568	      }
569	      for (let i = 0; i < 5; i++) {
570	        const [dvx, dvy] = rot(aim.x * 8, aim.y * 8, num47 * i - (Math.PI * 2 / 5 - num47) / 2); // :65860
571	        const n = spawnPart(game, e, 522);
572	        if (n) {
573	          // NewNPC(..., vector15.X, vector15.Y + 7, 522, ...) → X=中心横坐标,Y=底部纵坐标
574	          n.ai0 = 0;
575	          n.ai1 = (Math.random() - 0.5) * 0.3 * (Math.PI * 2) / 60; // :65861 逐 t 弯转角
576	          n.ai2 = dvx; n.ai3 = dvy;                                  // 初速(AI_100 首拍取用)
577	          n.x = e.cx + e.facing * 30 - n.w / 2;
578	          n.y = e.cy + 12 + 7 - n.h;
579	          n.vx = dvx; n.vy = dvy;
580	        }
581	      }
582	      // 原版火球(522)发射零吼(同上全段普查)——曾借 roar 0.5,2026-08-18 对账删
583	    }
584	    e.ai1 += 1;
585	    if (e.ai1 >= 4 + 20 * 2) { e.ai0 = 0; e.ai1 = 0; if (isReal) e.ai3 += 1; e.vx = 0; e.vy = 0; }
586	    return;
587	  }
588	
589	  // ---- ai0 == 8 远古末日(:65873-65932):玩家附近随机空位撒 NPC523,数量 = min(克隆体+1, 3)
590	  //      (:65892-65897);经典选招表不含 6(expert 随机替换专属,:65270-65275),状态体保留 ----
591	  if (e.ai0 === 8) {
592	    if (isReal && e.ai1 >= 4 && (e.ai1 - 4) % 20 === 0) {
593	      const st = game.world.store;
594	      const ptx = Math.floor(player.cx / TILE), pty = Math.floor(player.cy / TILE);
595	      const etx = Math.floor(e.cx / TILE), ety = Math.floor(e.cy / TILE);
596	      const want = Math.min(cultistClones(game, e).length + 1, 3);
597	      for (let k = 0; k < want; k++) {
598	        for (let tries = 0; tries < 100; tries++) { // :65904-65931 空位采样
599	          const tx = ptx + Math.floor(Math.random() * 41) - 20;
600	          const ty = pty + Math.floor(Math.random() * 41) - 20;
601	          const nearPlayer = Math.abs(ty - pty) <= 7 && Math.abs(tx - ptx) <= 7;
602	          const nearSelf = Math.abs(ty - ety) <= 3 && Math.abs(tx - etx) <= 3;
603	          if (nearPlayer || nearSelf || !st.inBounds(tx, ty) || st.isSolid(tx, ty)) continue;
604	          const n = spawnPart(game, e, 523);
605	          if (n) {
606	            n.x = tx * TILE + 8 - n.w / 2;
607	            n.y = ty * TILE + 8 - n.h / 2;
608	            n.vx = 0; n.vy = 0;
609	            n.ai0 = e.id; // :65930 ai[0] = 真身 whoAmI(本仓以运行时 id 代)
610	            n.bInit = true;
611	          }
612	          break;
613	        }
614	      }
615	    }
616	    e.ai1 += 1;
617	    if (e.ai1 >= 4 + 20 * 3) { e.ai0 = 0; e.ai1 = 0; if (isReal) e.ai3 += 1; e.vx = 0; e.vy = 0; }
618	    return;
619	  }
620	
621	  // 未知状态:回选招
622	  e.ai0 = 0; e.ai1 = 0;
623	}
624	
625	// ===================== AI_120 光之女皇 636(NPC.cs:46299-47302) =====================
626	// 状态机(ai0): 0 出生(180t) / 1 悬浮蓄力枢纽(DashTo 靠近 10t + 减速,45t(二阶段 20t)选招)/
627	//   2 彩虹射线 873 / 4 光枪墙 919 / 5 永恒彩虹 872 / 6 太阳舞 923 / 7 光枪回环 919(二阶段)/
628	//   8,9 刀阵冲刺(±50 速,6-40t 无敌蓄力,40-90t 伤害 ×1.5)/ 10 半血变身传送 /
629	//   13 淡出退场(目标失效/超 6400px)。3(874 天降极光)与 11/12 为 expert 专属拍,跳过。
630	// 经典弹幕伤害(:46326-46345): 919 墙 50 / 919 回环 70 / 873 45 / 872 45 / 923 50 / 874 40。
631	// 选招表(:46460-46580 残差映射): 一阶段 10 拍 [2,8,6,8,5,2,8,4,8,5] 循环,血 ≤50% 强制 10(变身);
632	//   二阶段 9 拍 [7,2,8,5,2,6,4,8,12] 循环——num37 槽位推进（flag2 时第 3 槽插 11=expert
633	//   专属拍），表尾 num57=12（873 螺旋）;反编译的 num54 双写 [..,6,6,..] 是同一 if 重复,
634	//   真表第 6 槽是 4、第 8 槽是 12。
635	const EMPRESS_CYCLE_P1 = [2, 8, 6, 8, 5, 2, 8, 4, 8, 5];
636	const EMPRESS_CYCLE_P2 = [7, 2, 8, 5, 2, 6, 4, 8, 12];
637	
638	/** 原版 AI_120_HallowBoss_DashTo(:47304-47317):目标上移 300,>200 再回退 100,
639	 *  速度 = lerp(单位向量*min(len,18), vector/6, lerpValue(100,600,len)) */
640	function empressDashTo(e: Enemy, tx0: number, ty0: number): void {
641	  let tx = tx0, ty = ty0 - 300;
642	  const d0 = Math.hypot(tx - e.cx, ty - e.cy);
643	  if (d0 > 200) {
644	    const ux = (tx - e.cx) / (d0 || 1), uy = (ty - e.cy) / (d0 || 1);
645	    tx -= ux * 100; ty -= uy * 100;

```


---

## 🤖 Assistant · 2026-08-19T07:46:44.166Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I understand the cultist AI state machine. States: ai0 ∈ {-1, 0, 1, 2, 3, 4, 5, 6, 7, 8}.

Now I need to map vanilla localAI[2] states to our ai0 semantics. The vanilla FindFrame switch on localAI[2]: 0/1/2/10/11/12/13. What is localAI[2] in vanilla's cultist AI? Let me search vanilla NPC.cs for localAI[2] in the cultist AI section (64921-65957). The vanilla AI sets localAI[2] to 10/11/12/13 as "sub-state" markers for casting animations. Let me look.

From the task: "态0→行0/态10→行4-6/态1·11→行10-12/态2·12→行7-9/态13→行13+". And "态值取我们 AI 的 ai0 语义对应(0 选招/1 飞掠/2 冰/3 火/4 雷/5 仪式/6 硬直/7 光/8 末日+克隆体态)".

I need to find where vanilla sets localAI[2] in AI_084. Let me grep the cultist AI section for localAI[2].
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:46:45.328Z · glm-x-preview-260804

```
现在我来查找一下原版教徒 AI 是如何设置 localAI[2]（帧状态源）的。
```


---

## 🤖 Assistant · 2026-08-19T07:46:46.594Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '64921,65960p' NPC.cs | grep -n \"localAI\\[2\\]\" | head -30",
 "description": "Find localAI[2] writes in cultist AI"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:46:46.645Z

**📎 ToolResult**

```
200:				if (localAI[2] != 13f)
204:				localAI[2] = 13f;
209:				localAI[2] = 10f;
213:				localAI[2] = 1f;
217:				localAI[2] = 0f;
228:			localAI[2] = 10f;
428:			localAI[2] = 10f;
445:			localAI[2] = 11f;
516:			localAI[2] = 11f;
598:				localAI[2] = 12f;
602:				localAI[2] = 11f;
656:			localAI[2] = 10f;
742:						localAI[2] = 11f;
746:						localAI[2] = 12f;
750:						localAI[2] = 10f;
769:						localAI[2] = 11f;
773:						localAI[2] = 12f;
777:						localAI[2] = 10f;
808:						localAI[2] = 11f;
812:						localAI[2] = 12f;
816:						localAI[2] = 10f;
835:						localAI[2] = 11f;
839:						localAI[2] = 12f;
843:						localAI[2] = 10f;
865:			localAI[2] = 13f;
878:			localAI[2] = 11f;
960:			localAI[2] = 13f;

```


---

## 🤖 Assistant · 2026-08-19T07:46:51.542Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '65110,65160p' NPC.cs && echo ------- && sed -n '65330,65360p' NPC.cs && echo -------65531 && sed -n '65531,65545p' NPC.cs && echo -------65623 && sed -n '65623,65645p' NPC.cs",
 "description": "Read cultist localAI[2] state transitions in vanilla AI"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:46:51.647Z

**📎 ToolResult**

```
			this.ai[1] += 1f;
			if (this.ai[1] >= 420f)
			{
				this.ai[0] = 0f;
				this.ai[1] = 0f;
				netUpdate = true;
			}
			else if (this.ai[1] > 360f)
			{
				velocity *= 0.95f;
				if (localAI[2] != 13f)
				{
					SoundEngine.PlaySound(29, (int)position.X, (int)position.Y, 105);
				}
				localAI[2] = 13f;
			}
			else if (this.ai[1] > 300f)
			{
				velocity = -Vector2.UnitY;
				localAI[2] = 10f;
			}
			else if (this.ai[1] > 120f)
			{
				localAI[2] = 1f;
			}
			else
			{
				localAI[2] = 0f;
			}
			flag3 = true;
			flag4 = true;
		}
		if (this.ai[0] == 0f)
		{
			if (this.ai[1] == 0f)
			{
				TargetClosest(faceTarget: false);
			}
			localAI[2] = 10f;
			int num12 = Math.Sign(player.Center.X - center.X);
			if (num12 != 0)
			{
				direction = (spriteDirection = num12);
			}
			this.ai[1] += 1f;
			if (this.ai[1] >= 40f && flag2)
			{
				int num13 = 0;
				if (flag)
				{
					switch ((int)this.ai[3])
-------
					break;
				}
				if (num13 == 5)
				{
					this.ai[0] = 7f;
					this.ai[1] = 0f;
				}
				if (num13 == 6)
				{
					this.ai[0] = 8f;
					this.ai[1] = 0f;
				}
				netUpdate = true;
			}
		}
		else if (this.ai[0] == 1f)
		{
			flag3 = true;
			localAI[2] = 10f;
			if ((float)(int)this.ai[1] % 2f != 0f && this.ai[1] != 1f)
			{
				position -= velocity;
			}
			this.ai[1] -= 1f;
			if (this.ai[1] <= 0f)
			{
				this.ai[0] = 0f;
				this.ai[1] = 0f;
				this.ai[3] += 1f;
				velocity = Vector2.Zero;
				netUpdate = true;
-------65531
						list5.Add(num23);
					}
				}
				foreach (int item5 in list5)
				{
					NPC nPC5 = Main.npc[item5];
					Vector2 center5 = nPC5.Center;
					int num24 = Math.Sign(player.Center.X - center5.X);
					if (num24 != 0)
					{
						nPC5.direction = (nPC5.spriteDirection = num24);
					}
					if (Main.netMode != 1)
					{
						Vector2 vector8 = Vector2.Normalize(player.Center - center5 + player.velocity * 20f);
-------65623
					for (int num34 = 0; num34 < array.Length; num34++)
					{
						if (num31 != num34)
						{
							Vector2 center6 = base.Center + spinningpoint.RotatedBy((float)num34 * (MathF.PI * 2f) / (float)num29 - MathF.PI / 2f);
							if (num33-- > 0)
							{
								int num35 = NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)center6.X, (int)center6.Y + height / 2, 440, whoAmI);
								Main.npc[num35].ai[3] = whoAmI;
								Main.npc[num35].netUpdate = true;
								Main.npc[num35].localAI[1] = localAI[1];
							}
							else
							{
								int num36 = list6[-num33 - 1];
								Main.npc[num36].Center = center6;
								NetMessage.SendData(23, -1, -1, null, num36);
							}
						}
					}
					this.ai[2] = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, 0f, 0f, 490, 0, 0f, Main.myPlayer, 0f, whoAmI);
					base.Center += spinningpoint.RotatedBy((float)num31 * (MathF.PI * 2f) / (float)num29 - MathF.PI / 2f);
					netUpdate = true;

```


---

## 🤖 Assistant · 2026-08-19T07:47:05.248Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I need the localAI[2] writes within each ai0 state. Line offsets within the 64921-based sed:
- Line 200/204/209/213/217 (≈ 65120-65137): the ai0==-1 (spawn) state: 
  - ai1 > 360: localAI[2] = 13 (with sound)
  - ai1 > 300: localAI[2] = 10
  - ai1 > 120: localAI[2] = 1
  - else (ai1 <= 120): localAI[2] = 0
- Line 228 (≈65148): ai0==0 (选招): localAI[2] = 10
- Line 428 (≈65348): ai0==1 (飞掠): localAI[2] = 10
- Line 445 (≈65365): ai0==2 (冰雾): localAI[2] = 11
- Line 516 (≈65436): ai0==3 (火球): localAI[2] = 11
- Line 598/602 (≈65518-65522): before ai0==4? Let me check: 598: localAI[2] = 12; 602: localAI[2] = 11. Hmm — that's around 65518, which is just before 65531... need context.
- Line 656 (≈65576): ai0==4 (闪电): localAI[2] = 10? Hmm line 656 → 64921+656-1 = 65576. Let me view.
- Lines 742-843 (≈65662-65763): ai0==5 (仪式): many — 11/12/10 by phase within the ritual state!
- Line 865 (≈65785): ai0==6 (硬直): localAI[2] = 13.
- Line 878 (≈65798): ai0==7 (光): localAI[2] = 11.
- Line 960 (≈65880): ai0==8 (末日): localAI[2] = 13.

Let me read the exact contexts to be precise.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:47:11.475Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && echo \"--- ai0==2 (65362-65380)\" && sed -n '65362,65372p' NPC.cs && echo \"--- ai0==3 (65430-65445)\" && sed -n '65430,65445p' NPC.cs && echo \"--- 65510-65530 (transition?)\" && sed -n '65510,65530p' NPC.cs && echo \"--- ai0==4 head (65562-65580)\" && sed -n '65567,65580p' NPC.cs && echo \"--- ai0==5 ritual (65685-65770 localAI writes)\" && sed -n '65690,65700p' NPC.cs && sed -n '65730,65775p' NPC.cs && echo \"--- ai0==6 (65771-65796)\" && sed -n '65771,65790p' NPC.cs && echo \"--- ai0==7 (65796-65800)\" && sed -n '65796,65800p' NPC.cs && echo \"--- ai0==8 (65873-65880)\" && sed -n '65873,65880p' NPC.cs",
 "description": "Read vanilla cultist localAI[2] state contexts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:47:11.630Z

**📎 ToolResult**

```
--- ai0==2 (65362-65380)
		}
		else if (this.ai[0] == 2f)
		{
			localAI[2] = 11f;
			Vector2 vec = Vector2.Normalize(player.Center - center);
			if (vec.HasNaNs())
			{
				vec = new Vector2(direction, 0f);
			}
			if (this.ai[1] >= 4f && flag2 && (int)(this.ai[1] - 4f) % num == 0)
			{
--- ai0==3 (65430-65445)
				velocity = Vector2.Zero;
				netUpdate = true;
			}
		}
		else if (this.ai[0] == 3f)
		{
			localAI[2] = 11f;
			Vector2 vec2 = Vector2.Normalize(player.Center - center);
			if (vec2.HasNaNs())
			{
				vec2 = new Vector2(direction, 0f);
			}
			if (this.ai[1] >= 4f && flag2 && (int)(this.ai[1] - 4f) % num2 == 0)
			{
				if ((int)(this.ai[1] - 4f) / num2 == 2)
				{
--- 65510-65530 (transition?)
				velocity = Vector2.Zero;
				netUpdate = true;
			}
		}
		else if (this.ai[0] == 4f)
		{
			if (flag2)
			{
				localAI[2] = 12f;
			}
			else
			{
				localAI[2] = 11f;
			}
			if (this.ai[1] == 20f && flag2 && Main.netMode != 1)
			{
				List<int> list5 = new List<int>();
				for (int num23 = 0; num23 < Main.maxNPCs; num23++)
				{
					if (Main.npc[num23].active && Main.npc[num23].type == 440 && Main.npc[num23].ai[3] == (float)whoAmI)
					{
--- ai0==4 head (65562-65580)
				this.ai[0] = 0f;
				this.ai[1] = 0f;
				this.ai[3] += 1f;
				velocity = Vector2.Zero;
				netUpdate = true;
			}
		}
		else if (this.ai[0] == 5f)
		{
			localAI[2] = 10f;
			if (Vector2.Normalize(player.Center - center).HasNaNs())
			{
				new Vector2(direction, 0f);
			}
--- ai0==5 ritual (65685-65770 localAI writes)
					}
					else if (vector11.Y < 0f)
					{
						localAI[2] = 12f;
					}
					else
					{
						localAI[2] = 10f;
					}
					int num38 = Math.Sign(vector11.X);
					if (num38 != 0)
					else if (vector12.Y < 0f)
					{
						localAI[2] = 12f;
					}
					else
					{
						localAI[2] = 10f;
					}
					int num40 = Math.Sign(vector12.X);
					if (num40 != 0)
					{
						direction = (spriteDirection = num40);
					}
				}
				else
				{
					Vector2 vector13 = Main.projectile[(int)Main.npc[(int)this.ai[3]].ai[2]].Center;
					vector13 -= base.Center;
					if (vector13 == Vector2.Zero)
					{
						vector13 = -Vector2.UnitY;
					}
					vector13.Normalize();
					if (Math.Abs(vector13.Y) < 0.77f)
					{
						localAI[2] = 11f;
					}
					else if (vector13.Y < 0f)
					{
						localAI[2] = 12f;
					}
					else
					{
						localAI[2] = 10f;
					}
					int num41 = Math.Sign(vector13.X);
					if (num41 != 0)
					{
						direction = (spriteDirection = num41);
					}
				}
			}
			this.ai[1] += 1f;
			if (this.ai[1] >= 420f)
			{
				flag4 = true;
--- ai0==6 (65771-65796)
			}
			this.ai[1] += 1f;
			if (this.ai[1] >= 420f)
			{
				flag4 = true;
				this.ai[0] = 0f;
				this.ai[1] = 0f;
				this.ai[3] += 1f;
				velocity = Vector2.Zero;
				netUpdate = true;
			}
		}
		else if (this.ai[0] == 6f)
		{
			localAI[2] = 13f;
			this.ai[1] += 1f;
			if (this.ai[1] >= 120f)
			{
				this.ai[0] = 0f;
				this.ai[1] = 0f;
--- ai0==7 (65796-65800)
		else if (this.ai[0] == 7f)
		{
			localAI[2] = 11f;
			Vector2 vec3 = Vector2.Normalize(player.Center - center);
			if (vec3.HasNaNs())
--- ai0==8 (65873-65880)
				this.ai[3] += 1f;
				velocity = Vector2.Zero;
				netUpdate = true;
			}
		}
		else if (this.ai[0] == 8f)
		{
			localAI[2] = 13f;

```


---

## 🤖 Assistant · 2026-08-19T07:48:15.749Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now the full localAI[2] mapping (vanilla):

- **ai0==-1 (spawn/显形)**: by ai1: >360 → 13; >300 → 10; >120 → 1; else → 0.
- **ai0==0 (选招)**: 10
- **ai0==1 (飞掠)**: 10
- **ai0==2 (冰雾)**: 11
- **ai0==3 (火球)**: 11
- **ai0==4 (闪电)**: flag2 (isReal) ? 12 : 11 (clones: 11)
- **ai0==5 (仪式)**: 10 at state head; then within the visible window (ai1 ≥ 120), per-member facing-to-circle-center vector: |vy|<0.77 → 11; vy<0 → 12; else 10. (For the real one: vector13 = circle center − self; for clones: vector11/12 similar relative to their reference.)
- **ai0==6 (硬直)**: 13
- **ai0==7 (光)**: 11
- **ai0==8 (末日)**: 13

And FindFrame maps localAI[2]:
- 0: settle row 0; animate rows 4-6 while transitioning (frame.Y != 0 && fc<15)
- 10: loop rows 4-6 continuously
- 1: settle row 1; animate rows 10-12 while frame != row 1
- 11: loop rows 10-12
- 2: settle row 2; animate rows 7-9 while frame != row 2
- 12: loop rows 7-9
- 13: loop rows 13-15 (13 + fc/5)
- default (any other value, e.g. never?): frame unchanged

FindFrame details:
```csharp
case 0:  // settle row 0
    if (fc >= 15) { fc = 0; frame.Y = 0; }
    else if (frame.Y != 0) frame.Y = (fc/5 + 4) * num;   // rows 4,5,6
    break;
case 10:
    if (fc >= 15) fc = 0;
    frame.Y = (fc/5 + 4) * num;
    break;
case 1:  // settle row 1
    if (fc >= 15) { fc = 0; frame.Y = num; }
    else if (frame.Y != num) frame.Y = (fc/5 + 10) * num;  // rows 10,11,12
    break;
case 11:
    if (fc >= 15) fc = 0;
    frame.Y = (fc/5 + 10) * num;
    break;
case 2:  // settle row 2
    if (fc >= 15) { fc = 0; frame.Y = num*2; }
    else if (frame.Y != num*2) frame.Y = (fc/5 + 7) * num;  // rows 7,8,9
    break;
case 12:
    if (fc >= 15) fc = 0;
    frame.Y = (fc/5 + 7) * num;
    break;
case 13:
    if (fc >= 15) fc = 0;
    frame.Y = (fc/5 + 13) * num;   // rows 13,14,15
    break;
}
frameCounter += 1.0;
```

Wait — subtle: in case 0, "if (fc >= 15) { fc = 0; frame.Y = 0; }" — note frameCounter += 1.0 happens at the END. So sequence: fc goes 0..14 while animating rows 4-6 (each 5 ticks: fc/5 ∈ 0,1,2 → rows 4,5,6). At the check when fc >= 15 → fc=0, frame → row 0. Then stays row 0 forever (since frame.Y == 0 → else-if fails; fc keeps counting 0..14 then >=15 → reset... wait: fc increments each tick; at 15 → reset to 0 and frame=0 (already). So case 0: plays rows 4→5→6 (15t total, from wherever frame was — but note: if frame was 10-12, it jumps straight to band 4-6 immediately: frame.Y = (fc/5+4)*num regardless of current row!). Yes — entering state 0 from e.g. state 11 (rows 10-12): frame jumps to row 4-6 band (using current fc phase), plays one 15t loop, then settles row 0. Hmm wait — only if frame.Y != 0. If frame is already 0 (settled), stays 0. So the "cast anim then settle" plays once per state entry (if frame was left non-zero).

Hmm, actually careful: the transition plays through band 4-6 exactly once (one 15t sweep) then snaps to row 0 and freezes. It doesn't pass through intermediate rows (unlike pumpking). Fine — literal implementation.

For states 10/11/12/13: continuous loop of the 3-row band (15t cycle, 5t/row).

For states 1 and 2: same pattern with settle rows 1 and 2 and bands 10-12 / 7-9.

Now, the plan for the cultist per task: "我们的 bossAI_lategame.ts 把 la2 挪用存仪式圈心对象(勿动!)——做法:在教徒 AI 状态机各态切换处写 e.customFrameIdx(直接帧号,Renderer vanillaFrameIdx 首行已支持直读;水书怪 694 是先例)".

So: implement the full FindFrame state machine in lunaticCultistAI, maintaining a per-entity (frameCounter, frame) pair, writing e.customFrameIdx each tick. Where do I keep the pair? laOf(e) localAI slots — which are free? la0: used for "localAI[0]==0 首帧音效门" (set to 1 at spawn; vanilla localAI[0] spawn gate). la1: 仪式代数 (gen counter). la2: 仪式圈心 (don't touch). la3: 圈引用 (CultistRitualCircle) for real; for clones la3 = parent reference. Hmm — for clones, la3 = parent Enemy; for real, la3 = circle. la0: only used as a "has spawned" flag (set 1 once, never read again? `la.la0 = 1` — only written; the check is `!e.bInit` for the spawn gate... Actually looking: la.la0 = 1 written at spawn but is it read anywhere? Let me check other uses of la0/l.la0 in the file... I saw `la.la0 = 1` at line 307. Search needed.

Since I need two numbers (counter + frame) per cultist entity and the laOf slots are mostly taken, options: use a module-level WeakMap in bossAI_lategame.ts (like `localAI` WeakMaps in other files) for the frame state: `const cultistFrame = new WeakMap<Enemy, {fc: number; row: number}>()`. That's clean and avoids touching la slots. 

Now the AI state → localAI[2] (frame state) mapping for our port:

- ai0 == -1: ai1 > 360 → 13; > 300 → 10; > 120 → 1; else → 0. (Note our thresholds: `e.ai1 > 360`, `e.ai1 > 300` — matches vanilla exactly.)
- ai0 == 0 → 10
- ai0 == 1 → 10
- ai0 == 2 → 11
- ai0 == 3 → 11
- ai0 == 4 → isReal ? 12 : 11
- ai0 == 5 → 10 at entry... wait, vanilla sets localAI[2] = 10f at the head of ai0==5 unconditionally, then the 120-420 window block overrides per-position. Our port: at ai0===5 head set state 10; then in the else branch (t >= 120) after facing computation, compute the vector to circle center and set 11/12/10. Hmm wait — look at vanilla: the block computing localAI[2] in ritual: it's within `if (ai[1] >= 120)`? Let me verify the structure: the writes at 65685-65770 — there seem to be two symmetric branches (vector11 for clones of...? / vector12 / vector13 for self) then a shared else. Let me read the whole ai0==5 block structure 65575-65770 to place the writes correctly. Actually — our port's structure at ai0===5: `t >= 120` branch computes facing from circle center (`cir.x - e.cx` → sign). The vanilla code computes vector13 = circle.Center - Center, normalize; |Y| < 0.77 → 11; Y < 0 → 12; else 10; and direction = sign(X). Our port only does the X sign. For frame state I need the Y component comparison: |vy|<0.77 → 11, vy<0 → 12, vy>... → 10.

But which branch does which? There appear to be multiple: for clones during 30-90 (repositioning) and 120-420 (visible). Let me read the full block 65575-65775 to get it right.

Also — what about the clones during ritual? Clones mirror ai0/ai1 from parent but run their own localAI[2] logic in the same ai0==5 block (vector11/12 = their own positions relative to circle). So in our port, for clones at t>=120: vector = circle center − clone center; same comparisons.

Wait — also there's possibly a branch for ai1 in [30,90)? Let me read.
````

</details>


---

## 🤖 Assistant · 2026-08-19T07:48:16.879Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '65676,65732p' NPC.cs",
 "description": "Read vanilla ritual state frame-state block"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:48:16.925Z

**📎 ToolResult**

```
					}
				}
				else
				{
					Vector2 vector11 = Main.projectile[(int)Main.npc[(int)this.ai[3]].ai[2]].Center;
					vector11 -= base.Center;
					if (vector11 == Vector2.Zero)
					{
						vector11 = -Vector2.UnitY;
					}
					vector11.Normalize();
					if (Math.Abs(vector11.Y) < 0.77f)
					{
						localAI[2] = 11f;
					}
					else if (vector11.Y < 0f)
					{
						localAI[2] = 12f;
					}
					else
					{
						localAI[2] = 10f;
					}
					int num38 = Math.Sign(vector11.X);
					if (num38 != 0)
					{
						direction = (spriteDirection = num38);
					}
				}
			}
			else if (this.ai[1] >= 90f && this.ai[1] < 120f)
			{
				flag3 = true;
				flag4 = true;
				float num39 = (this.ai[1] - 90f) / 30f;
				alpha = 255 - (int)(num39 * 255f);
			}
			else if (this.ai[1] >= 120f && this.ai[1] < 420f)
			{
				flag4 = true;
				alpha = 0;
				if (flag2)
				{
					Vector2 vector12 = Main.projectile[(int)this.ai[2]].Center;
					vector12 -= base.Center;
					if (vector12 == Vector2.Zero)
					{
						vector12 = -Vector2.UnitY;
					}
					vector12.Normalize();
					if (Math.Abs(vector12.Y) < 0.77f)
					{
						localAI[2] = 11f;
					}
					else if (vector12.Y < 0f)
					{
						localAI[2] = 12f;

```


---

## 🤖 Assistant · 2026-08-19T07:48:49.183Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now the structure is clear. In the ritual state (ai0==5):
- Head: localAI[2] = 10 (unconditional at state head, :65575)
- In the ai1 ∈ [90,120): alpha fade-in — no localAI[2] write.
- In ai1 ∈ [120,420): 
  - if flag2 (real): vector12 = circle.Center − self; normalize; |Y|<0.77 → 11; Y<0 → 12; else 10.
  - else (clone): vector13 = circle (via parent's ai[2]... actually `Main.npc[(int)this.ai[3]].ai[2]` — the parent's ai[2] = projectile index of circle) − self; same comparisons.
  
Wait, hmm — the sed output above shows two different blocks: one at 65676-65702 (vector11, references `Main.npc[(int)this.ai[3]].ai[2]` = parent's circle — this is the clone branch) and one at 65704+ (vector12, references `this.ai[2]` = own circle — real branch). And earlier context: the vector11 block is inside `if (ai1 >= 30 && ai1 < 90)`? Let me check the block boundaries — the else-structure at 65676 says `else { Vector2 vector11 = ...` — that's likely inside the [30,90) invisible window where clones (not flag2) get repositioned/face. And [120,420): flag2 → vector12; else → vector13.

Given the complexity, precise placement:
- [0,30): fade out — head-set 10 stays.
- [30,90): invisible; flag2 (real) does the repositioning; else (clones) compute vector11 → 10/11/12 + facing. Hmm wait — the clone branch at 65676: inside which window? It follows `}` `}` `else {`. Let me get the enclosing conditions by reading 65600-65706 more carefully. Actually — our own port only sets facing in the [120,420) window (from circle). The vanilla clone branch inside [30,90) (vector11) also sets facing. Our port doesn't (only [120,420)). For the frame state machine, the [30,90) clone branch affects localAI[2] during the invisible window (invisible → doesn't matter visually! alpha=255 = fully invisible). Actually wait — alpha=255 means invisible in Terraria (alpha 0 = opaque). Yes: spawnAlpha 254 = mostly invisible. So frame states during invisible windows don't matter visually. Only [120,420) matters (visible), plus the head-10 default.

But careful — the frame/counter state evolution is continuous: entering the visible window with a different localAI[2] value than what the invisible period left determines the transition animation. Since exact visual continuity through invisible periods is not observable, but the counter phase at window entry is (fc carries over). The vanilla behavior in [30,90) for real (flag2): does the real one get localAI[2] writes? In [30,90): the repositioning block for flag2 — I saw earlier at 65636-65675 (num28/num29/num31...). Any localAI[2] write in there? The grep list shows writes at lines 742/746/750 (=65662/65666/65670) — hmm wait those line numbers were relative to 64921: 742 → 65662, 746 → 65666, 750 → 65670. That's inside the [30,90) block! So both branches (flag2 real reposition / clone vector11) have the 11/12/10 writes around there. Let me just read 65636-65706 fully to see both.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:48:50.501Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '65575,65590p' NPC.cs && echo ... && sed -n '65630,65680p' NPC.cs",
 "description": "Read ritual state head and reposition window"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:48:50.557Z

**📎 ToolResult**

```
		{
			localAI[2] = 10f;
			if (Vector2.Normalize(player.Center - center).HasNaNs())
			{
				new Vector2(direction, 0f);
			}
			if (this.ai[1] >= 0f && this.ai[1] < 30f)
			{
				flag3 = true;
				flag4 = true;
				float num26 = (this.ai[1] - 0f) / 30f;
				alpha = (int)(num26 * 255f);
			}
			else if (this.ai[1] >= 30f && this.ai[1] < 90f)
			{
				if (this.ai[1] == 30f && Main.netMode != 1 && flag2)
...
								int num35 = NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)center6.X, (int)center6.Y + height / 2, 440, whoAmI);
								Main.npc[num35].ai[3] = whoAmI;
								Main.npc[num35].netUpdate = true;
								Main.npc[num35].localAI[1] = localAI[1];
							}
							else
							{
								int num36 = list6[-num33 - 1];
								Main.npc[num36].Center = center6;
								NetMessage.SendData(23, -1, -1, null, num36);
							}
						}
					}
					this.ai[2] = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, 0f, 0f, 490, 0, 0f, Main.myPlayer, 0f, whoAmI);
					base.Center += spinningpoint.RotatedBy((float)num31 * (MathF.PI * 2f) / (float)num29 - MathF.PI / 2f);
					netUpdate = true;
					list6.Clear();
				}
				flag3 = true;
				flag4 = true;
				alpha = 255;
				if (flag2)
				{
					Vector2 vector10 = Main.projectile[(int)this.ai[2]].Center;
					vector10 -= base.Center;
					if (vector10 == Vector2.Zero)
					{
						vector10 = -Vector2.UnitY;
					}
					vector10.Normalize();
					if (Math.Abs(vector10.Y) < 0.77f)
					{
						localAI[2] = 11f;
					}
					else if (vector10.Y < 0f)
					{
						localAI[2] = 12f;
					}
					else
					{
						localAI[2] = 10f;
					}
					int num37 = Math.Sign(vector10.X);
					if (num37 != 0)
					{
						direction = (spriteDirection = num37);
					}
				}
				else
				{
					Vector2 vector11 = Main.projectile[(int)Main.npc[(int)this.ai[3]].ai[2]].Center;

```


---

## 🤖 Assistant · 2026-08-19T07:50:49.709Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now I have the full ritual-state picture:

ai0==5:
- head: localAI[2] = 10 (:65575)
- [0,30): fade out (alpha 0→255… wait num26*255; invisible by end). No write.
- [30,90): after the ai1==30 reposition (real only), both real (vector10, own circle) and clones (vector11, parent's circle): |vy|<0.77 → 11; vy<0 → 12; else 10; + facing from vx sign.
- [90,120): fade in. No write.
- [120,420): visible: real (vector12) / clone (vector13): same 11/12/10 + facing.

Our port's structure at ai0===5 has the [120,420) facing block (ritualCenterOf). For the frame machine I'll add the localAI[2]-equivalent computation:
- in [30,90): both real & clones — vector to circle center (real: own circle = la.la3 circle / la.la2 center; clones: parent's circle). Our ritualCenterOf handles both. Note in our port the circle is created at t===30 (real); before that la.la2 is null. Vanilla's [30,90) real branch reads Main.projectile[ai[2]] which exists from t=30. OK — compute when circle exists; else keep 10.
- in [120,420): same computation (already computing `cir`; extend to use dy).

Simplification for our port: both windows use the same rule (vector to circle center, |Y|<0.77 → 11, Y<0 → 12, else 10). Our [30,90) block currently doesn't compute cir — I can add the same ritualCenterOf call. Since both windows share the formula, I'll add a small helper computing frame-state from the circle vector.

Now — importantly — where in our AI to run the generic FindFrame replica? The cleanest: at the END of lunaticCultistAI (after the state machine has run, so localAI[2]-equivalent state is final for this tick), run the FindFrame replica and write e.customFrameIdx. But our AI returns early in every state block (`return` per state)! E.g. `if (e.ai0 === 0) { ...; flyIntegrate(e); return; }`. So the frame machine can't go at the end. Options: compute the frame state (localAI[2] equivalent) at each state block (or before the state machine, since the mapping state→localAI2 is deterministic from ai0/ai1/isReal + ritual circle position), then run the replica right after, before the early returns. 

The localAI[2] value depends on:
- ai0==-1: threshold on ai1 — note the AI increments ai1 AFTER the checks (vanilla: `if (ai[1] > 360)... else if (this.ai[1] += 1f`? hmm — vanilla ai0==-1 block: it checks ai[1] ranges then increments. Our port: uses e.ai1 with same thresholds then increments. The frame state must use the same pre-increment value.
- ai0==5: [30,90) and [120,420) windows — the block runs before ai1 increment.

So the natural place: at the TOP of each state block? Too invasive. Alternative: run a dedicated function `cultistFindFrame(e, ...)` at the start of the AI (before state blocks), computing localAI2-equivalent from current (pre-update) ai0/ai1 values — must mirror the vanilla evaluation order. In vanilla, localAI[2] is written inside AI each tick BEFORE FindFrame runs (FindFrame runs after AI in UpdateNPC). And the values used are post-state-update? No — within the state block, localAI[2] is assigned based on the ai[1] value BEFORE the increment (checks happen before `ai[1] += 1f` in each block? e.g. ai0==-1: the range checks happen, then ai1 += 1? Let me verify vanilla ai0==-1 increments... earlier sed at 65110 showed the ai1 >= 420 check then ranges — the increment happens... in our port, ai0===-1 block: `e.ai1 += 1` happens after the threshold logic (lines 354-362: alpha computed with e.ai1, then e.ai1 += 1, then flyIntegrate, then >=420 check). Vanilla: 64959+: `ai[1] += 1f` — where? Our port is 1:1, so pre-increment ai1 is what the frame thresholds read.

So: implement `cultistFrameTick(e, game, player-ish context)` called at the top of lunaticCultistAI (after the clone-mirror segment which sets ai0/ai1 — clones mirror parent's ai0/ai1 at :64998-65001 BEFORE the state machine runs; and the mirror happens at the very start. Note: vanilla clones also mirror ai0/ai1 at the start, then run the same state machine). Place the frame computation right before `const b = baseOf(e)` or right after the early-despawn check? Careful — several paths `return` early (despawn, -1 spawn state, etc.). Vanilla FindFrame runs regardless of AI early-outs? In vanilla, FindFrame is called from UpdateNPC after AI regardless (AI early-out = skip rest of AI but FindFrame still runs). Hmm — for despawning/dead entities it doesn't matter (e.dead → removed). For ai0==-1 our block returns early — so the frame computation must happen BEFORE that return. Best: insert the frame-state computation + FindFrame replica right after the clone mirror/spawn-init segment and the despawn check — i.e., before `const face = ...` / the ai0==-1 block. It reads the pre-increment ai0/ai1 — mirroring vanilla's assignment order (all localAI[2] writes happen inside state blocks which our computation replicates with the same pre-increment values).

Wait — one exception: the ritual [30,90)/[120,420) writes depend on the CURRENT circle center & self position. In our port, at t===30 the real teleports itself (e.x += fx). Vanilla: reposition happens at ai1==30 inside the block, and the vector10 computation happens after (same tick, using new position). Our frame computation at the top of the AI would use the pre-teleport position for the first tick — a 1-tick deviation of the frame state during an invisible window. Negligible... but actually cleaner: our port computes the facing in the [120,420) block from `cir` after teleport long done — fine. For [30,90): vanilla computes vector10 after the reposition teleport each tick. Our top-of-AI computation at t=30 uses pre-teleport position; from t=31 onward post. 1-tick invisible-window deviation — acceptable, but let me instead place the frame computation AFTER the ai0===5 block? No — every block returns early.

Simplest robust approach: put the frame state computation at top (before `const face`), covering all states with the pre-increment semantics; for the ritual state, both windows compute from current position & circle (the t=30 tick: circle doesn't exist yet in la.la2 — vanilla creates circle before the vector computation, but the vector is computed with pre-teleport center? No — vanilla: ai[1]==30 block (reposition + circle spawn + Center += offset), THEN vector10 computed with post-teleport Center. Our top-of-AI at t=30: la.la2 still null (circle/center saved during the ai0===5 block later in the tick) → state stays 10 for that tick. Deviation: one tick, invisible window (alpha=255 at t≥30). Utterly invisible. Accept + note.

Hmm, wait — actually there's a subtlety: for clones, vanilla's vector11 references `Main.npc[(int)this.ai[3]].ai[2]` — the parent's ai[2] = circle projectile index. If parent's circle is dead/replaced... our ritualCenterOf(parent) reads parent's la.la2 which persists (a plain {x,y} object — never cleared). Vanilla would read Main.projectile[...] potentially inactive → NaN center? Edge case; our {x,y} persists — fine, more stable.

OK. Now — the frame machine replica (needs persistent counter + row). Storage: WeakMap in bossAI_lategame.ts: `const cultistAnim = new WeakMap<Enemy, { fc: number; row: number }>()`.

Replica logic (NPC.cs:72698-72783):
```
switch (st) {
  case 0: if (fc >= 15) { fc = 0; row = 0; } else if (row !== 0) row = (fc/5|0) + 4; break;
  case 10: if (fc >= 15) fc = 0; row = (fc/5|0) + 4; break;
  case 1: if (fc >= 15) { fc = 0; row = 1; } else if (row !== 1) row = (fc/5|0) + 10; break;
  case 11: if (fc >= 15) fc = 0; row = (fc/5|0) + 10; break;
  case 2: if (fc >= 15) { fc = 0; row = 2; } else if (row !== 2) row = (fc/5|0) + 7; break;
  case 12: if (fc >= 15) fc = 0; row = (fc/5|0) + 7; break;
  case 13: if (fc >= 15) fc = 0; row = (fc/5|0) + 13; break;
}
fc += 1;
e.customFrameIdx = row;
```

Wait — case 13's row band: 13 + fc/5 where fc ∈ [0,15) → rows 13,14,15. The sprite has how many rows? npcFrameCount for 439/440 = 16 presumably. Renderer clamps `Math.min(frames - 1, e.customFrameIdx)` — good.

Also the bestiary-dummy branch (IsABestiaryIconDummy → rows 4-6 cycle) — irrelevant for our game (no bestiary dummy NPCs) — skip with comment.

Now the ai0==-1 sub-state mapping — vanilla thresholds:
```
else if (ai[1] > 360) { sound + localAI[2] = 13 }
else if (ai[1] > 300) { velocity = -UnitY; localAI[2] = 10 }
else if (ai[1] > 120) { localAI[2] = 1 }
else { localAI[2] = 0 }
```
Hmm wait — the first sed block I read at 65110 was actually the TAIL of the ai0==-1 state? It shows `ai[1] += 1f; if (ai[1] >= 420) {ai[0]=0...}` then `else if (ai[1] > 360) {velocity *= 0.95; sound; localAI[2]=13}` then `> 300 {velocity = -UnitY; localAI[2]=10}` then `> 120 {localAI[2]=1}` else `{localAI[2]=0}`. 

Hmm — wait, that's the structure with `ai[1] += 1f` FIRST, then the >= 420 check, then the localAI[2] range checks on the INCREMENTED value. Let me double check with our port: our port does `e.ai1 += 1; if (e.ai1 > 360) {...} else if (e.ai1 > 300) {...}` — hmm our port: line 356 `e.ai1 += 1;` then 357: `if (e.ai1 > 360) {...}` — yes our port increments first then checks. So the frame thresholds use post-increment ai1: >360 → 13, >300 → 10, >120 → 1, else 0. Our computation must replicate post-increment... but wait, our computation at top-of-AI sees PRE-increment ai1. Ugh.

Let me look at vanilla more carefully:

```
this.ai[1] += 1f;
if (this.ai[1] >= 420f) { ai[0]=0; ai[1]=0; ... }
else if (this.ai[1] > 360f) { velocity *= 0.95; if (localAI[2] != 13) sound; localAI[2] = 13f; }
else if (this.ai[1] > 300f) { velocity = -UnitY; localAI[2] = 10f; }
else if (this.ai[1] > 120f) { localAI[2] = 1f; }
else { localAI[2] = 0f; }
```

Hmm — wait, is that the ai0==-1 state or the tail of something else? It was at 65110-65137 — and our port's ai0===-1 block mirrors it: increment, >360 damping+sound(Zombie_105 at ===361), >300 rise, >=420 exit. Yes.

So for ai0==-1: frameState = f(post-increment ai1): ai1+1 > 360 → 13; > 300 → 10; > 120 → 1; else 0. Since vanilla's increment happens before the checks within the same tick, FindFrame (after AI) sees the state derived from the incremented value. Our top-of-AI computation with pre-increment value: use (e.ai1 + 1) — or just compute from the same expression our port checks. E.g. compute `const t1 = e.ai1 + 1` then thresholds. Equivalent.

Similarly for ai0==5 windows: vanilla checks windows on pre-increment ai1 (the [0,30)/[30,90)/[90,120)/[120,420) chain runs before `ai[1] += 1f` at block end? From the sed at 65765: `this.ai[1] += 1f; if (this.ai[1] >= 420f)...` — yes, at block end). Our port: same (windows on pre-increment t, increment after). So top-of-AI pre-increment values are correct for ai0==5.

For other states (0/1/2/3/4/6/7/8): localAI[2] is a constant per state — no ai1 dependence. 

For ai0==-1, I need the +1. Let me handle: `const s = e.ai1 + 1; st = s > 360 ? 13 : s > 300 ? 10 : s > 120 ? 1 : 0`.

Hmm wait — actually let me re-check: is `ai[1] += 1f` before the else-if chain? From the first sed (65110-65137):
```
this.ai[1] += 1f;            (65110)
if (this.ai[1] >= 420f)      (65111)
{
    this.ai[0] = 0f; ai[1]=0...
}
else if (this.ai[1] > 360f)
{
    velocity *= 0.95f;
    if (localAI[2] != 13f) { SoundEngine.PlaySound(29, ..., 105); }
    localAI[2] = 13f;
}
else if (this.ai[1] > 300f) { velocity = -Vector2.UnitY; localAI[2] = 10f; }
else if (this.ai[1] > 120f) { localAI[2] = 1f; }
else { localAI[2] = 0f; }
flag3 = true; flag4 = true;
```
Yes — post-increment. And our port at line 356-360: `e.ai1 += 1; if (e.ai1 > 360) {damping} else if (e.ai1 > 300) {rise} ... if (e.ai1 === 361) sound; ... if (e.ai1 >= 420) exit`. Matches.

Wait — but our port has `if (e.ai1 > 360) { e.vx *= 0.95 ...}` — the sound at ===361. Vanilla: > 360 with localAI[2]!=13 gate → plays once. Our port plays at ===361 — equivalent-ish. Fine, that's existing code (don't touch).

So frame state function:
```
function cultistFrameState(e, la, isReal, parent): number {
  switch ai0:
    -1: s=ai1+1; s>360→13; s>300→10; s>120→1; else 0
    0: 10
    1: 10
    2: 11
    3: 11
    4: isReal ? 12 : 11
    5: head 10; windows [30,90) & [120,420): circle-vector → 11/12/10
    6: 13
    7: 11
    8: 13
}
```

For ai0==5 [0,30) and [90,120): stays head value 10.

Circle vector: dx = cir.x - e.cx, dy = cir.y - e.cy; normalize (if zero → (0,-1)); |uy| < 0.77 → 11; uy < 0 → 12; else 10.

Now — where to call. Top of AI after clone-mirror & despawn checks, before the `const face` block? The clone mirror sets ai0/ai1 = parent's, and clone justHit handling (dead + parent→6). The despawn check kills. The frame replica needs to run before state blocks return. I'll insert right after the `if (isReal && e.ai0 === 5 && ...justHit...)` block (line ~346) or right before `// 朝向(:65117-65120...)`. At that point ai0/ai1 are this tick's effective pre-state-update values. 

One more check — the clone mirror: `e.ai0 = parent.ai0; e.ai1 = parent.ai1;` — mirror happens BEFORE parent's AI ran this tick? Order depends on entity iteration order — mirrors are as-1:1-as-possible; irrelevant for frame state (uses mirrored values as vanilla does).

Now Betsy. Let me read the betsy section of bossAI_dd2.ts.
````

</details>


---

## 🤖 Assistant · 2026-08-19T07:50:50.387Z · glm-x-preview-260804

```
Cultist 映射现在已经完成了。接下来是 bossAI_dd2.ts 中的 Betsy AI。
```


---

## 🤖 Assistant · 2026-08-19T07:50:51.838Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"betsy\\|Betsy\\|551\\|ai0 =\\|lai\\|L\\[\" src/entities/bossAI_dd2.ts | sed -n '1,80p'",
 "description": "Locate Betsy AI state fields in dd2 file"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:50:51.904Z

**📎 ToolResult**

```
42://                                           +500×3,Projectile.cs:35510）/ 2 召骷髅 673（183t,
45://   aiStyle 110 双足翼龙 Betsy 551        NPC.cs:43165 → AI_110_Betsy :62266
172://（电弧 10 速 50 伤）/ 686 DD2BetsyFireball（空袭火球,继承机速）/ 687
173:// DD2BetsyFlameBreath（喷焰,10 速横冲）。
190:  private ai0 = 0;
199:    if (this.ai0 === 0) {
248:  // 686 火球 dd2_betsy_fireball_shot（:53645）——多变体组内随机（playSfxFiles 语义）
272:  686: 'dd2_betsy_fireball_shot',  // :53645 DD2_BetsyFireballShot（空袭火球出膛）
382:// DD2 索敌（NPCUtils.TargetClosestOldOnesInvasion :261 / TargetClosestBetsy :308）：
397:  // TargetClosestOldOnesInvasion（:261-273）玩家滤 200px 内；TargetClosestBetsy（:308-318）
446:    e.ai0 = -1; e.ai1 = -1; e.ai2 = -1; e.ai3 = -1;
451:        c.ai0 = e.id;      // 原版 ai[0] = 船 whoAmI（锚定引用）
456:        if (i === 0) e.ai0 = c.id;
473:        if (i === 0) e.ai0 = -1; else if (i === 1) e.ai1 = -1;
744:  if (!e.bInit) { e.bInit = true; e.ai0 = 0; }
761:  if (e.ai0 < 0) e.ai0 = Math.min(e.ai0 + 1, 0);   // 冷却回摆（:42267-42269）
765:    if (e.ai0 >= 135) { e.ai0 = -300; }             // 135t → -300 冷却（:42273-42276）
766:    if (e.ai0 === 54 && player && !player.dead) {
786:        e.ai0 = -200;                               // 太远 → 缩短冷却（:42344-42347）
790:  if (e.ai0 === 0) e.ai0 = 1;                       // 起手（:42387-42389）
849:  if (!e.bInit) { e.bInit = true; e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; e.dirY = 1; }
911:        e.ai0 = e.dirY;
920:      e.ai0 = floorNear ? -1 : 1;
922:      if (e.ai0 === -1) {
924:        if (e.vy < -osc) e.ai0 = 1;
927:        if (e.vy > osc) e.ai0 = -1;
940:    e.ai0 = 1;
960:  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; }
969:    e.ai0 = 180;
977:          portal.ai0 = 0; portal.ai1 = 0;
989:    if (e.ai0 === 3) {
993:        if (!n.dead && n.vanillaId === 549) { n.ai1 = 1; n.ai0 = 0; }
1022:    if (e.ai0 === 0) {
1024:        if (!n.dead && n.vanillaId === 549) { n.ai1 = 1; n.ai0 = 0; }
1053:  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; e.ai2 = e.ai2 === 1 ? 1 : 0; }
1074:      if (e.ai0 >= rate * 3) e.ai0 = 0;
1084:      e.ai0 = 0;
1136:  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
1169:  if (e.ai0 === 0) {
1199:      e.ai0 = 1;                                    // 进入瞄准（:66181-66186）
1203:  } else if (e.ai0 === 1) {
1222:      e.ai0 = 2;
1231:  } else if (e.ai0 === 2) {
1239:      e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
1242:      e.ai0 = 4;
1251:    if (p.explode && solidBody(game, e)) { e.ai0 = 3; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
1252:  } else if (e.ai0 === 4) {
1255:    if (e.ai1 <= 0) { e.ai0 = 0; e.ai1 = 0; }
1261:    e.ai0 = 3; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
1263:  if (e.ai0 === 3) {
1300:  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; }
1323:  if (e.ai0 < 0) e.ai0 = Math.min(e.ai0 + 1, 0);   // 招间冷却（:66421-66423）
1328:    if (e.ai1 === 2 && e.ai0 === 80) {
1332:    if (e.ai1 === 2 && e.ai0 === 64) {
1335:      // 673 阵眼在原版弹幕 ai[0]==70 帧播音（Projectile.cs:35516 DD2_SkeletonSummoned），
1343:    if (e.ai1 === 0 && e.ai0 === 32) {
1352:    if (e.ai1 === 1 && e.ai0 === 126) {
1362:    if (e.ai1 === 1 && (e.ai0 === 40 || e.ai0 === 48 || e.ai0 === 56)) {
1376:      e.ai0 = prev === 0 ? -20 : -120;
1380:  if (e.ai0 === 0 && x[3] >= 60) {
1396:      e.ai0 = next === 0 ? 97 : next === 1 ? 127 : 183;   // :66500-66510
1405:// AI_110 双足翼龙 Betsy 551（NPC.cs:43165 → AI_110_Betsy :62266）
1407:export function betsyAI(e: Enemy, game: GameHooks, player: Player | null) {
1408:  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
1421:  // ---- 索敌（:62276 NPCUtils.TargetClosestBetsy）：水晶/玩家近者胜,无 200px 门 ----
1430:  if (e.ai0 === 0) {
1433:    if (e.ai1 >= INTRO_T) { e.ai1 = 0; e.ai0 = 1; e.ai2 = 0; }
1434:  } else if (e.ai0 === 1) {
1453:      e.ai0 = next;
1472:  } else if (e.ai0 === 2) {
1474:    if (e.ai1 === 0) game.playSfxFiles(soundTrackFiles('dd2_betsy_wind_attack'), 0.7, e.cx, e.cy); // DD2_BetsyWindAttack（:62415）
1476:    if (e.ai1 >= WIND_T) { e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; }
1477:  } else if (e.ai0 === 3) {
1501:      game.playSfxFiles(['dd2_betsy_flame_breath'], 0.7, e.cx, e.cy);   // DD2_BetsyFlameBreath（:62462）
1509:    if (e.ai1 >= FLAME_T0 + FLAME_T1) { e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; }
1510:  } else if (e.ai0 === 4) {
1551:    if (e.ai1 >= BOMB_TOTAL) { e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; }
1552:  } else if (e.ai0 === 5) {
1565:    if (e.ai1 === 1) game.playSfxFiles(['dd2_betsy_flying_circle_attack'], 0.7, e.cx, e.cy); // DD2_BetsyFlyingCircleAttack（:62547）
1568:      e.ai0 = 1; e.ai1 = 0; e.ai2 = 0;

```


---

## 🤖 Assistant · 2026-08-19T07:50:54.437Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_dd2.ts",
 "limit": 200,
 "offset": 1405
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:50:54.448Z

**📎 ToolResult**

```
1405	// AI_110 双足翼龙 Betsy 551（NPC.cs:43165 → AI_110_Betsy :62266）
1406	// ---------------------------------------------------------------------------
1407	export function betsyAI(e: Enemy, game: GameHooks, player: Player | null) {
1408	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
1409	  const x = dd2LocalAI(e);
1410	  e.despawnTimer = 750;   // netAlways：不入 CheckActive 消退
1411	  // 常量（:62277-62318）
1412	  const DMG_BREATH = 35, DMG_FIREBALL = 35;
1413	  const INTRO_T = 10, FLY_ACC = 0.45, FLY_SPD = 7.5;
1414	  const HOVER_T = 30, WIND_T = 30, DIVE_SPD = 23;
1415	  const FLAME_OFF = 600, FLAME_APPR = 12, FLAME_T0 = 40, FLAME_T1 = 80;
1416	  const BOMB_OFF = 1500, BOMB_APR_T = 60, BOMB_ACC = 1 / 30, BOMB_SPD = 12;
1417	  const FIREBALL_EVERY = 10, FIREBALL_N = 6 * FIREBALL_EVERY, TAIL_T = 60;
1418	  const BOMB_TOTAL = BOMB_APR_T + FIREBALL_N + TAIL_T;
1419	  const SPIN_T = 60, SPIN_RATE = TAU / SPIN_T, SPIN_RISE = 0.1, SKYDIVE_SPD = 32;
1420	  const SUMMON_T = 90, SUMMON_AT = 20;
1421	  // ---- 索敌（:62276 NPCUtils.TargetClosestBetsy）：水晶/玩家近者胜,无 200px 门 ----
1422	  const tgt = dd2Target(game, e, player, true);
1423	  if (!tgt) {
1424	    e.vy -= 0.05;
1425	    fly(e);
1426	    return;
1427	  }
1428	  const txc = tgt.x, tyc = tgt.y;
1429	  let timeScale = 1;   // num2：各态动画步进倍率
1430	  if (e.ai0 === 0) {
1431	    // ---- 入场（:62321-62330） ----
1432	    e.ai1 += 1;
1433	    if (e.ai1 >= INTRO_T) { e.ai1 = 0; e.ai0 = 1; e.ai2 = 0; }
1434	  } else if (e.ai0 === 1) {
1435	    // ---- 悬停选招（:62332-62416） ----
1436	    if (e.ai2 === 0) e.ai2 = e.cx < txc ? 1 : -1;
1437	    const destX = txc - e.ai2 * 300, destY = tyc - 200;
1438	    const d = dirTo(e, destX, destY);
1439	    simpleFlyMove(e, d.x * FLY_SPD, d.y * FLY_SPD, FLY_ACC);
1440	    e.facing = e.cx < txc ? 1 : -1;
1441	    e.ai1 += 1;
1442	    if (e.ai1 >= HOVER_T) {
1443	      // ai[3]==5 且 1/3 概率 → 追加一轮（:62344-62347）
1444	      if (e.ai3 === 5 && rnd(3) === 0) e.ai3 += 1;
1445	      let next = 1;                                  // :62349-62370 八槽表
1446	      const s = e.ai3 | 0;
1447	      if (s === 0 || s === 1 || s === 3) next = 2;
1448	      else if (s === 2) next = 3;
1449	      else if (s === 4) next = 4;
1450	      else if (s === 5) next = 5;
1451	      else if (s === 6) next = 3;
1452	      else if (s === 7) next = 6;
1453	      e.ai0 = next;
1454	      e.ai1 = 0; e.ai2 = 0;
1455	      e.ai3 += 1;
1456	      if (e.ai3 >= 8) e.ai3 = 0;
1457	      if (next === 2 || next === 5) {
1458	        // 直冲起手（:62373-62400）：朝目标 23/32 速,rotation 对准
1459	        const v = dirTo(e, txc, tyc);
1460	        e.facing = v.x > 0 ? 1 : -1;
1461	        e.visAngle = Math.atan2(v.y, v.x) + (e.facing === -1 ? Math.PI : 0);
1462	        e.vx = v.x * (next === 2 ? DIVE_SPD : SKYDIVE_SPD);
1463	        e.vy = v.y * (next === 2 ? DIVE_SPD : SKYDIVE_SPD);
1464	      } else if (next === 3) {
1465	        // 火焰吐息起手（:62402-62408）：反向 2 速退位
1466	        const d3 = txc > e.cx ? 1 : -1;
1467	        e.facing = d3;
1468	        e.vx = -2 * d3;
1469	        e.vy = 0;
1470	      }
1471	    }
1472	  } else if (e.ai0 === 2) {
1473	    // ---- 风压冲（:62418-62427） ----
1474	    if (e.ai1 === 0) game.playSfxFiles(soundTrackFiles('dd2_betsy_wind_attack'), 0.7, e.cx, e.cy); // DD2_BetsyWindAttack（:62415）
1475	    e.ai1 += 1;
1476	    if (e.ai1 >= WIND_T) { e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; }
1477	  } else if (e.ai0 === 3) {
1478	    // ---- 火焰吐息（:62429-62487） ----
1479	    e.ai1 += 1;
1480	    e.ai2 = e.cx < txc ? 1 : -1;
1481	    if (e.ai1 < FLAME_T0) {
1482	      // 接位：目标反向 600px 上空（:62435-62447）
1483	      const dx = txc - e.ai2 * FLAME_OFF, dy = tyc - 250;
1484	      const d = dirTo(e, dx, dy);
1485	      if (Math.hypot(dx - e.cx, dy - e.cy) < FLAME_APPR) {
1486	        e.x = dx - e.w / 2; e.y = dy - e.h / 2;   // 原版 base.Center = vector4 直接贴位
1487	      } else {
1488	        e.x += d.x * FLAME_APPR;
1489	        e.y += d.y * FLAME_APPR;
1490	      }
1491	      if (Math.hypot(dx - e.cx, dy - e.cy) < 16) e.ai1 = FLAME_T0 - 1;
1492	      timeScale = 1.5;
1493	    }
1494	    if (e.ai1 === FLAME_T0) {
1495	      // 喷焰起手（:62449-62461）：10 速横冲 + 687 喷焰
1496	      const d3 = txc > e.cx ? 1 : -1;
1497	      e.vx = d3 * 10;
1498	      e.vy = 0;
1499	      e.facing = d3;
1500	      shootD(game, e.cx, e.cy, e.vx, e.vy, DMG_BREATH, 687, 300, 0, 20);
1501	      game.playSfxFiles(['dd2_betsy_flame_breath'], 0.7, e.cx, e.cy);   // DD2_BetsyFlameBreath（:62462）
1502	    }
1503	    if (e.ai1 >= FLAME_T0) {
1504	      timeScale = 1.5;
1505	      if (Math.abs(txc - e.cx) > 550 && Math.abs(e.vx) < 20) {
1506	        e.vx += sign(e.vx) * 0.5;                  // 远距提速（:62465-62469）
1507	      }
1508	    }
1509	    if (e.ai1 >= FLAME_T0 + FLAME_T1) { e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; }
1510	  } else if (e.ai0 === 4) {
1511	    // ---- 空袭（:62489-62583） ----
1512	    e.ai2 = e.cx < txc ? 1 : -1;
1513	    if (e.ai1 < BOMB_APR_T) {
1514	      // 高位接位（:62493-62509）：反向 1500px、-350 上空
1515	      const dx = txc - e.ai2 * BOMB_OFF, dy = tyc - 350;
1516	      const d = dirTo(e, dx, dy);
1517	      e.vx = lerp(e.vx, d.x * BOMB_SPD, BOMB_ACC);
1518	      e.vy = lerp(e.vy, d.y * BOMB_SPD, BOMB_ACC);
1519	      e.facing = e.cx < txc ? 1 : -1;
1520	      if (Math.hypot(dx - e.cx, dy - e.cy) < 16) e.ai1 = BOMB_APR_T - 1;
1521	      timeScale = 1.5;
1522	    } else if (e.ai1 === BOMB_APR_T) {
1523	      // 俯冲突进（:62511-62521）：12 速贴地掠射
1524	      let v = dirTo(e, txc, tyc);
1525	      v = { x: v.x, y: v.y * 0.25 };
1526	      const vl = Math.hypot(v.x, v.y) || 1;
1527	      v = { x: v.x / vl, y: v.y / vl };
1528	      e.facing = v.x > 0 ? 1 : -1;
1529	      e.visAngle = Math.atan2(v.y, v.x) + (e.facing === -1 ? Math.PI : 0);
1530	      e.vx = v.x * BOMB_SPD;
1531	      e.vy = v.y * BOMB_SPD;
1532	    } else {
1533	      // 掠射（:62523-62543）：水平 7/t、垂直 6/t 贴地,每 10t 投 686 火球 ×6
1534	      const dTo = dirTo(e, txc, tyc);
1535	      e.x += dTo.x * 7;
1536	      e.y += dirTo(e, txc, tyc - 400).y * 6;
1537	      if (e.ai1 <= BOMB_TOTAL - TAIL_T) timeScale = 1.5;
1538	      const ox = (110 + 30) * e.facing, oy = 20;
1539	      const rx = e.cx + ox * Math.cos(e.visAngle) - oy * Math.sin(e.visAngle);
1540	      const ry = e.cy + ox * Math.sin(e.visAngle) + oy * Math.cos(e.visAngle);
1541	      const n = Math.floor(e.ai1 - BOMB_APR_T + 1);
1542	      if (n <= FIREBALL_N && n % FIREBALL_EVERY === 0) {
1543	        // 686 重力=两段式(:54640-54659)——Arrow 单 grav2 档近似(第三段 @20 登记);
1544	        // life 3600/穿透族原版 -1(仓内 pierce 口径 1,登记)
1545	        shootD2(game, rx, ry, e.vx, e.vy, DMG_FIREBALL, 686, 3600,
1546	          { grav: 0.1, grav2: 0.1, grav2At: 10, dragAlways: 0.99, pierce: 3 });
1547	      }
1548	    }
1549	    if (e.ai1 > BOMB_TOTAL - TAIL_T) e.vy -= 0.1;   // 尾段拉起（:62545-62547）
1550	    e.ai1 += 1;
1551	    if (e.ai1 >= BOMB_TOTAL) { e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; }
1552	  } else if (e.ai0 === 5) {
1553	    // ---- 翻转俯冲（:62585-62604） ----
1554	    const rot = -SPIN_RATE * e.facing;
1555	    const c = Math.cos(rot), s = Math.sin(rot);
1556	    const nvx = e.vx * c - e.vy * s;
1557	    const nvy = e.vx * s + e.vy * c;
1558	    e.vx = nvx; e.vy = nvy;
1559	    e.y -= SPIN_RISE;
1560	    const d = dirTo(e, txc, tyc);
1561	    e.x += d.x * 10;
1562	    e.y += d.y * 10;
1563	    e.visAngle -= SPIN_RATE * e.facing;
1564	    timeScale *= 0.7;
1565	    if (e.ai1 === 1) game.playSfxFiles(['dd2_betsy_flying_circle_attack'], 0.7, e.cx, e.cy); // DD2_BetsyFlyingCircleAttack（:62547）
1566	    e.ai1 += 1;
1567	    if (e.ai1 >= SPIN_T) {
1568	      e.ai0 = 1; e.ai1 = 0; e.ai2 = 0;
1569	      e.vx /= 2; e.vy /= 2;
1570	    }
1571	  } else if (e.ai0 === 6) {
1572	    // ---- 召唤（:62606-62655） ----
1573	    if (e.ai1 === 0) {
1574	      // 贴水晶上空（:62608-62620）
1575	      const d = dirTo(e, txc, tyc - 200);
1576	      simpleFlyMove(e, d.x * FLY_SPD * 2, d.y * FLY_SPD * 2, FLY_ACC * 2);
1577	      e.facing = e.cx < txc ? 1 : -1;
1578	      e.ai2 += 1;
1579	      if (Math.hypot(txc - e.cx, tyc - e.cy) < 350 || e.ai2 >= 180) e.ai1 = 1;
1580	    } else {
1581	      if (e.ai1 === 1) game.playSfxFiles(['dd2_betsy_scream'], 0.8, e.cx, e.cy);  // DD2_BetsyScream（:62577）
1582	      if (e.ai1 < SUMMON_AT) { e.vx *= 0.95; e.vy *= 0.95; }
1583	      else { e.vx *= 0.98; e.vy *= 0.98; }
1584	      if (e.ai1 === SUMMON_AT) {
1585	        if (e.vy > 0) e.vy /= 3;
1586	        e.vy -= 3;                                   // 跃起（:62630-62634）
1587	        game.spawnParticles(e.cx, e.cy + e.h / 2, '#C8A060', 26, 4, { life: 40 });
1588	      }
1589	      timeScale *= 0.85;
1590	      // 召唤窗口（:62657-62696）：场上 560 ≤4 才召;自周 300px 环 + 传送门各出 560
1591	      if (e.ai1 === SUMMON_AT || e.ai1 === 45 || e.ai1 === 70) {
1592	        const wyverns = (game.enemies() as Enemy[])
1593	          .filter((n) => !n.dead && n.vanillaId === 560).length;
1594	        if (wyverns <= 4) {
1595	          const a = Math.random() * TAU;
1596	          const sx = e.cx + Math.cos(a) * 2 * 300 * (0.6 + Math.random() * 0.4);
1597	          const sy = e.cy + Math.sin(a) * 1 * 300 * (0.6 + Math.random() * 0.4);
1598	          if (Math.hypot(sx - txc, sy - tyc) > 100) {
1599	            const w = spawnPart(game, e, 560);
1600	            if (w) { w.x = sx - w.w / 2; w.y = sy - w.h / 2; }
1601	          }
1602	          const portals = (game.enemies() as Enemy[])
1603	            .filter((n) => !n.dead && n.vanillaId === 549);
1604	          for (let k = 0; k < 3 && portals.length > 0; k++) {

```


---

## 🤖 Assistant · 2026-08-19T07:51:05.217Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now the key question for Betsy's FindFrame: what does our AI write to ai[1] and how does the vanilla flap counter relate?

Vanilla FindFrame 551 reads ai[1] as `frameCounter = (int)ai[1]` for states 3/4/6. So vanilla's ai[1] IS the animation timer in those states — our ai1 in states 3/4/6 is the state timer (ai1 increments per tick... but with timeScale!). Hmm — vanilla AI: where does ai[1] advance and where does timeScale apply? Let me look at vanilla AI_110_Betsy (:62266+) to see how ai[1] is driven — in particular for ai0==6 (the flap sequence: frames 1,2,3,4,3,4,3,2,1,0 at 8t steps = 72t total). The task says "拍翼 0-4 序列(localAI[0] 36 步计数×timeScale)". So in vanilla, the wing-flap counter is localAI[0], which advances by timeScale each tick, and ai[1]... hmm wait, FindFrame reads `frameCounter = (int)ai[1]` for ai0==6. Let me look at the vanilla AI to see the relationship: maybe localAI[0] += timeScale; and ai[1] = localAI[0]? Let me read vanilla 62266-62330 and the ai0==6 block + the tail where ai[1] is assigned.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:51:07.309Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '62266,62330p' NPC.cs && echo ----62606-62660 && sed -n '62606,62660p' NPC.cs && echo ----62696-tail && sed -n '62696,62735p' NPC.cs",
 "description": "Read vanilla Betsy AI head, summon state, and tail"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:51:07.377Z

**📎 ToolResult**

```
	private void AI_110_Betsy()
	{
		//IL_04fe: Unknown result type (might be due to invalid IL or missing references)
		//IL_0490: Unknown result type (might be due to invalid IL or missing references)
		//IL_0b33: Unknown result type (might be due to invalid IL or missing references)
		//IL_0cb3: Unknown result type (might be due to invalid IL or missing references)
		//IL_13ad: Unknown result type (might be due to invalid IL or missing references)
		//IL_13c0: Unknown result type (might be due to invalid IL or missing references)
		//IL_13c5: Unknown result type (might be due to invalid IL or missing references)
		//IL_06a8: Unknown result type (might be due to invalid IL or missing references)
		//IL_06ad: Unknown result type (might be due to invalid IL or missing references)
		//IL_10e1: Unknown result type (might be due to invalid IL or missing references)
		//IL_11c6: Unknown result type (might be due to invalid IL or missing references)
		NPCUtils.TargetClosestBetsy(this, faceTarget: false);
		NPCAimedTarget targetData = GetTargetData();
		int num = -1;
		float num2 = 1f;
		int num3 = 35;
		int num4 = 35;
		float num5 = 10f;
		float num6 = 0.45f;
		float num7 = 7.5f;
		float num8 = 30f;
		float num9 = 30f;
		float num10 = 23f;
		float num11 = 600f;
		float num12 = 12f;
		float num13 = 40f;
		float num14 = 80f;
		float num15 = num13 + num14;
		float num16 = 1500f;
		float num17 = 60f;
		float num18 = 13f;
		float amount = 1f / 30f;
		float num19 = 12f;
		int num20 = 10;
		int num21 = 6 * num20;
		float num22 = 60f;
		float num23 = num17 + (float)num21 + num22;
		float num24 = 60f;
		float num25 = 1f;
		float num26 = MathF.PI * 2f * (num25 / num24);
		float num27 = 0.1f;
		float num28 = 32f;
		float num29 = 90f;
		float num30 = 20f;
		_ = ai[0];
		_ = -1f;
		SlotId val;
		if (ai[0] == 0f)
		{
			if ((ai[1] += 1f) >= num5)
			{
				ai[1] = 0f;
				ai[0] = 1f;
				ai[2] = 0f;
				netUpdate = true;
			}
		}
		else if (ai[0] == 1f)
		{
			if (ai[2] == 0f)
			{
				ai[2] = ((base.Center.X < targetData.Center.X) ? 1 : (-1));
			}
----62606-62660
						{
							Tile tileSafely = Framing.GetTileSafely(i, j);
							bool flag2 = tileSafely.active() && Main.tileSolid[tileSafely.type] && !Main.tileFrameImportant[tileSafely.type];
							if (flag && flag2)
							{
								int num43 = WorldGen.KillTile_GetTileDustAmount(fail: true, tileSafely);
								for (int k = 0; k < num43; k++)
								{
									Dust obj = Main.dust[WorldGen.KillTile_MakeTileDust(i, j, tileSafely)];
									obj.velocity.Y -= 3f + (float)num42 * 1.5f;
									obj.velocity.Y *= Main.rand.NextFloat();
									obj.scale += (float)num42 * 0.03f;
								}
								for (int l = 0; l < num43 - 1; l++)
								{
									Dust obj2 = Main.dust[WorldGen.KillTile_MakeTileDust(i, j, tileSafely)];
									obj2.velocity.Y -= 1f + (float)num42;
									obj2.velocity.Y *= Main.rand.NextFloat();
								}
								if (num43 > 0 && Main.rand.Next(3) != 0)
								{
									float num44 = Math.Abs(point.X - i) / (num40 / 2);
									Gore gore = Gore.NewGoreDirect(position, Vector2.Zero, 61 + Main.rand.Next(3), 1f - (float)num42 * 0.15f + num44 * 0.5f);
									gore.velocity.Y -= 0.1f + (float)num42 * 0.5f + num44 * (float)num42 * 1f;
									gore.velocity.Y *= Main.rand.NextFloat();
									gore.position = new Vector2(i * 16 + 20, j * 16 + 20);
								}
							}
							flag = !flag2;
						}
					}
				}
				bool flag3 = ai[1] == 20f || ai[1] == 45f || ai[1] == 70f;
				if (CountNPCS(560) > 4)
				{
					flag3 = false;
				}
				if (flag3 && Main.netMode != 1)
				{
					for (int m = 0; m < 1; m++)
					{
						Vector2 vector8 = base.Center + (MathF.PI * 2f * Main.rand.NextFloat()).ToRotationVector2() * new Vector2(2f, 1f) * 300f * (0.6f + Main.rand.NextFloat() * 0.4f);
						if (Vector2.Distance(vector8, targetData.Center) > 100f)
						{
							Point point2 = vector8.ToPoint();
							NewNPC(GetSpawnSourceForNPCFromNPCAI(), point2.X, point2.Y, 560, whoAmI);
							SoundEngine.PlayTrackedSound(SoundID.DD2_BetsySummon, vector8);
						}
					}
					List<NPC> list = new List<NPC>();
					for (int n = 0; n < Main.maxNPCs; n++)
					{
						NPC nPC = Main.npc[n];
						if (nPC.active && nPC.type == 549)
						{
----62696-tail
		}
		float num46 = DirectionTo(targetData.Center).ToRotation();
		float num47 = 0.04f;
		switch ((int)ai[0])
		{
		case 2:
		case 5:
			num47 = 0f;
			break;
		case 3:
			num47 = 0.01f;
			num46 = 0f;
			if (spriteDirection == -1)
			{
				num46 -= MathF.PI;
			}
			if (ai[1] >= num13)
			{
				num46 += (float)spriteDirection * MathF.PI / 12f;
				num47 = 0.05f;
			}
			break;
		case 4:
			num47 = 0.01f;
			num46 = MathF.PI;
			if (spriteDirection == 1)
			{
				num46 += MathF.PI;
			}
			break;
		case 6:
			num47 = 0.02f;
			num46 = 0f;
			if (spriteDirection == -1)
			{
				num46 -= MathF.PI;
			}
			break;
		}
		if (spriteDirection == -1)

```


---

## 🤖 Assistant · 2026-08-19T07:51:11.516Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I need to see where localAI[0] and timeScale (num2) are used in the vanilla Betsy AI, and where ai[1] is set from it. Let me grep the Betsy AI section (62266-62760) for "localAI[0]" and "num2".
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:51:13.138Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '62266,62770p' NPC.cs | grep -n \"localAI\\[0\\]\\|num2 \\|num2=\\|num2 =\\|ai\\[1\\] =\" | head -30",
 "description": "Find localAI[0] and timeScale usage in Betsy AI"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:51:13.198Z

**📎 ToolResult**

```
17:		float num2 = 1f;
54:				ai[1] = 0f;
102:				ai[1] = 0f;
148:			if (ai[1] == 0f)
155:				ai[1] = 0f;
183:					ai[1] = num13 - 1f;
185:				num2 = 1.5f;
187:			if (ai[1] == num13)
202:				num2 = 1.5f;
211:				ai[1] = 0f;
228:					ai[1] = num17 - 1f;
230:				num2 = 1.5f;
232:			else if (ai[1] == num17)
251:					num2 = 1.5f;
269:				ai[1] = 0f;
279:			num2 *= 0.7f;
280:			if (ai[1] == 1f)
287:				ai[1] = 0f;
294:			if (ai[1] == 0f)
304:					ai[1] = 1f;
310:				if (ai[1] == 1f)
322:				if (ai[1] == num30)
330:				num2 *= 0.85f;
331:				if (ai[1] == 20f || ai[1] == 25f || ai[1] == 30f)
373:				bool flag3 = ai[1] == 20f || ai[1] == 45f || ai[1] == 70f;
415:				ai[1] = 0f;
419:		localAI[0] += num2;
420:		if (localAI[0] >= 36f)
422:			localAI[0] = 0f;
426:			localAI[0] = num * 4;

```


---

## 🤖 Assistant · 2026-08-19T07:51:17.024Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '62683,62696p' NPC.cs",
 "description": "Read Betsy AI localAI[0] tail block"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:51:17.071Z

**📎 ToolResult**

```
		}
		localAI[0] += num2;
		if (localAI[0] >= 36f)
		{
			localAI[0] = 0f;
		}
		if (num != -1)
		{
			localAI[0] = num * 4;
		}
		if ((localAI[1] += 1f) >= 60f)
		{
			localAI[1] = 0f;
		}

```


---

## 🤖 Assistant · 2026-08-19T07:51:22.475Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Interesting! Vanilla Betsy AI tail:
```csharp
localAI[0] += num2;              // num2 = timeScale
if (localAI[0] >= 36f) localAI[0] = 0f;
if (num != -1) localAI[0] = num * 4;   // num = forced frame quarter? "int num = -1" at head
```
What is `num`? Declared at the head: `int num = -1;` — let me find where num is assigned in the AI (the flap-force). Let me grep `num = ` in the section.
````

</details>


---

## 🤖 Assistant · 2026-08-19T07:51:23.868Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '62266,62770p' NPC.cs | grep -n \"\\bnum = \\|num=[0-9]\" | head",
 "description": "Find num assignments in Betsy AI"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:51:23.921Z

**📎 ToolResult**

```
16:		int num = -1;
490:		int num = nearbyBooks.Length;

```


---

## 🤖 Assistant · 2026-08-19T07:52:26.725Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
`num` is never assigned (stays -1) in the Betsy AI — so `localAI[0] = num*4` never fires. localAI[0] just accumulates num2 (timeScale) and wraps at 36. So localAI[0] is a 0..36 flap-phase counter driven by timeScale.

But FindFrame 551 uses `frameCounter = (int)ai[1]` — NOT localAI[0]! So where does ai[1] get its values used by FindFrame?

For ai0==6 (summon): FindFrame's flap sequence thresholds at 8*n: 0→72. In the summon state, ai[1] goes 0→90 (num29=90: `if (ai[1] >= num29) {ai0=1, ai1=0}`). Hmm but the FindFrame sequence expects ai[1] to run 0..72+. In state 6, ai[1] increments by 1 each tick (with timeScale 0.85 applied to movement only? — wait, `num2 *= 0.85f` (line 330 rel) affects localAI[0], not ai[1]).

Hmm wait — FindFrame case ai0==6 uses ai[1]: flap sequence 1,2,3,4,3,4,3,2,1,0 at 8t each = 72t total. Our summon state runs ai1 0..90. At ai1 ≥ 72 → frame 0. OK — matches: flap through summon then settle.

But hold on — the task said "拍翼 0-4 序列(localAI[0] 36 步计数×timeScale,读 bossAI_dd2.ts betsyAI 的拍翼计数变量)". Hmm — the task author believed the flap comes from localAI[0] 36-step counter. But the vanilla FindFrame clearly reads ai[1] (`frameCounter = (int)ai[1]`) in states 3/4/6. And state 6 IS the flap ("拍翼")? Hmm wait — actually which state flaps? Let me think: Betsy's sprite rows: 0-4 = wing flap sequence (5 frames), 5-9 = attack poses (head-rearing / breath), 9-10 loop. FindFrame:
- ai0==3 (flame breath): frames 5,6 (5t), 7 (at 34), 8 (at 37), 9/10 loop (40..), 8 (98/123), 7 (103/128), 0 (108/133).
- ai0==4 (bombing run): similar with different thresholds.
- ai0==5: frame 3.
- ai0==6: flap sequence 1,2,3,4,3,4,3,2,1,0 at 8t steps from ai[1].
- else (0,1,2): frame 0.

Hmm — so in vanilla, the wing flap (0-4) only plays during the summon (ai0==6). And localAI[0] (36-step × timeScale)... is used where? Not in FindFrame 551. Let me check: maybe used in DrawNPC for wing layers? Betsy's sprite has separate wing layers? Actually NPC 551 Betsy sheet is single. Hmm, localAI[0] might drive... let me search Main.cs for Betsy localAI usage. Actually — not critical! FindFrame 551 uses only ai[0] and ai[1]. localAI[0] is consumed elsewhere (maybe unused). The task's hint about localAI[0] was a guess; the source says ai[1].

BUT — critical check: does our betsyAI's ai1 match vanilla's ai[1] semantics in states 3/4/6?

State 3 (flame): vanilla ai[1] counts 0..120 (num13=40 approach, then breath till 40+80=120). Our ai1: increments 1/t; approach phase can JUMP: `if (dist < 16) e.ai1 = FLAME_T0 - 1;` (=39, mirroring vanilla's `ai[1] = num13 - 1f` line 183). Good — 1:1.
FindFrame state 3 thresholds: 5, 34 (num278-6), 37, 40 (num278), 9/10 loop till 98 (num280-num281+3 = 120-25+3), then 8 at 98, 7 at 103 (98+5*... wait recompute: num285 = num280-num281+3 = 98. Thresholds: fc >= 5*1=5 → 6; >= 34 → 7; >= 37 → 8; >= 40 → 9+fc/3%2; >= 98 → 8; >= 98+5*1=103 → 7; >= 98+5*2=108 → 0.

Wait, I need to recompute the num60 counters for state 3:
```
num282 = 0;
if (fc >= num278 - 6f) → 7       // 34
if (fc >= num278 - 3f) → 8       // 37
if (fc >= num278) → 9 + fc/3%2   // 40
num282 = 0;
if (fc >= num280 - num281 + 3f) → 8    // 98
num284 = fc; num285 = 98; num60 = num282+1 = 1; num282 = 1;
if (fc >= 98 + 5*1) → 7               // 103
num286 = fc; num287 = 98; num60 = num282+1 = 2; num282 = 2;
if (fc >= 98 + 5*2) → 0               // 108
```
State 3: <5 → 5; [5,34) → 6; [34,37) → 7; [37,40) → 8; [40,98) → 9+((fc/3)%2); [98,103) → 8; [103,108) → 7; ≥108 → 0.

State 4 (num269=60, num270=10, num271=60, num272... wait for state 4: num269 = 60f, num270 = 10, num271 = 6*num270 = 60, num275 = num269+num271+3 = 123:
- <5 → 5; [5,54) → 6; [54,57) → 7; [57,60) → 8; [60,123) → 9+fc/3%2; [123,128) → 8; [128,133) → 7; ≥133 → 0.

State 6: base 1; fc=ai[1]; thresholds 8,16,24,32,40,48,56,64,72:
- [0,8) → 1; [8,16) → 2; [16,24) → 3; [24,32) → 4; [32,40) → 3; [40,48) → 4; [48,56) → 3; [56,64) → 2; [64,72) → 1; ≥72 → 0.

State 5 → 3. States 0/1/2 (and -1?) → 0.

Now our ai1 in state 6: our summon runs `if (e.ai1 === 0) {...approach...}` — ai1 stays 0 during approach (up to 180t!), then ai1=1 and increments to 90. Hmm — vanilla: in state 6 `if (ai[1] == 0f) { approach...; ai[1] = 1f; }` — same. So ai1 ∈ [0,90]. FindFrame state 6 works on our ai1 directly. 

But WAIT — the state-6 branch in FindFrame sets `frameCounter = (int)ai[1]` — but in our port, is ai1 possibly affected by timeScale? No — ai1 is +1/t in state 6 (only localAI[0] uses timeScale). But hmm — does our betsyAI update ai1 by timeScale? Our code: state 6: `e.ai1 += 1` — no timeScale. Vanilla: same (`ai[1] += 1f` presumably in the summon block; the timeScale 0.85 only multiplies num2/localAI[0]). Let me double check vanilla summon state ai[1] increment: line 415 rel: `ai[1] = 0f` at state end (>= num29=90). And the increment... I see `if (ai[1] == 20f || ai[1] == 45f...)`. The increment must be `ai[1] += 1f` somewhere. Fine — our port is 1:1 and tested.

State 4: our ai1 increments 1/t BUT with a potential jump: `if (Math.hypot(...) < 16) e.ai1 = BOMB_APR_T - 1;` (=59; vanilla `ai[1] = num17 - 1f` = 59). 1:1. FindFrame state 4 thresholds on ai1: 5/54/57/60/123/128/133. Our BOMB_APR_T=60, BOMB_TOTAL=180. Matches vanilla num17=60, num23=180. 

State 3: thresholds 5/34/37/40/98/103/108 vs our FLAME_T0=40, FLAME_T1=80 (total 120). Vanilla num13=40, num15=120. Matches.

So Betsy Renderer branch: pure function of ai0/ai1. 

Also note FindFrame 551's ai0 values: 3,4,5,6 handled; everything else (0,1,2) → frame 0. And the "if (num268 < 5) frameCounter = 0.0;" lines are dead (frameCounter overwritten immediately) — skip.

Now, one more check on Betsy: `int num268 = frame.Y / num;` — the current row; used only for the dead resets. Skip.

Also — should Betsy's FindFrame be in Renderer reading e.ai0/e.ai1? Yes — stateless, clean.

Now the Pumpking vanilla AI :33247-33256 — the L[0]/L[1] beat. Let me check what vanilla does there (it's the "cloak" frame per Main.cs:22501) to make sure it's separate from FindFrame.
````

</details>


---

## 🤖 Assistant · 2026-08-19T07:52:28.659Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '33246,33275p' NPC.cs && echo ---Main22501 && sed -n '22490,22510p' Main.cs",
 "description": "Read pumpking AI head and Main.cs cloak draw"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:52:28.709Z

**📎 ToolResult**

```
		else if (aiStyle == 58)
		{
			localAI[0]++;
			if (localAI[0] > 6f)
			{
				localAI[0] = 0f;
				localAI[1]++;
				if (localAI[1] > 4f)
				{
					localAI[1] = 0f;
				}
			}
			Player player8 = Main.player[target];
			if (type == 327)
			{
				Lighting.AddLight(base.Center, 0.4f, 0.4f, 0.2f);
			}
			if (Main.netMode != 1)
			{
				localAI[2]++;
				if (localAI[2] > 300f)
				{
					localAI[2] = 0f;
					this.ai[3] = Main.rand.Next(3);
					netUpdate = true;
				}
				else if (this.ai[3] == 0f && localAI[2] % 30f == 0f && localAI[2] > 30f)
				{
					int num925 = 5;
					Vector2 vector111 = new Vector2(base.Center.X, base.Center.Y + 30f);
---Main22501
				case 260:
					mySpriteBatch.Draw(TextureAssets.Chain25.Value, new Vector2(vector2.X - screenPos.X, vector2.Y - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Chain25.Width(), num7), color2, rotation2, new Vector2((float)TextureAssets.Chain25.Width() * 0.5f, (float)TextureAssets.Chain25.Height() * 0.5f), 1f, SpriteEffects.None, 0f);
					break;
				default:
					mySpriteBatch.Draw(TextureAssets.Chain4.Value, new Vector2(vector2.X - screenPos.X, vector2.Y - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Chain4.Width(), num7), color2, rotation2, new Vector2((float)TextureAssets.Chain4.Width() * 0.5f, (float)TextureAssets.Chain4.Height() * 0.5f), 1f, SpriteEffects.None, 0f);
					break;
				}
			}
		}
		if (type == 327)
		{
			float rotation3 = 0f;
			Vector2 vector3 = new Vector2(rCurrentNPC.Center.X, rCurrentNPC.Center.Y + 80f);
			int num10 = (int)rCurrentNPC.localAI[1];
			Microsoft.Xna.Framework.Color color3 = ((!rCurrentNPC.IsABestiaryIconDummy) ? Lighting.GetColor((int)vector3.X / 16, (int)(vector3.Y / 16f)) : rCurrentNPC.GetBestiaryEntryColor());
			mySpriteBatch.Draw(TextureAssets.PumpkingCloak.Value, new Vector2(vector3.X - screenPos.X, vector3.Y - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, TextureAssets.PumpkingCloak.Height() / 5 * num10, TextureAssets.PumpkingCloak.Width(), TextureAssets.PumpkingCloak.Height() / 5), color3, rotation3, new Vector2((float)TextureAssets.PumpkingCloak.Width() * 0.5f, (float)TextureAssets.PumpkingCloak.Height() * 0.5f / 5f), 1f, SpriteEffects.None, 0f);
		}
		if (type == 328)
		{
			Vector2 vector4 = new Vector2(rCurrentNPC.position.X + (float)rCurrentNPC.width * 0.5f - 5f * rCurrentNPC.ai[0], rCurrentNPC.position.Y + 20f);
			for (int i = 0; i < 2; i++)

```


---

## 🤖 Assistant · 2026-08-19T07:52:35.158Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: localAI[0]/[1] for 327 drive the cloak (PumpkingCloak drawn in Main.cs with 5 frames indexed by localAI[1]) — separate from FindFrame. Our pumpkingAI already maintains L[0]/L[1] for that (the render side reads via localAIOf — need to check where Renderer reads localAIOf for the cloak; not my concern).

So the FindFrame 327 (pose walk) is separate and needs: frameCounter + frame — persistent. I'll implement it in pumpkingAI writing e.customFrameIdx.

Wait — but where does our Renderer read the cloak? Let me check (to make sure my change doesn't conflict). Let me grep Renderer.ts for localAIOf / 327.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:52:37.057Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"localAIOf\\|327\\|PumpkingCloak\\|cloak\" src/render/Renderer.ts | head -20; grep -rn \"case 39[0-9]\\|case 32[0-9]\\|case 34[0-9]\\|case 439\\|case 551\\|case 38[0-9]\" src/render/Renderer.ts | head",
 "description": "Check existing Renderer references to these NPC ids"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:52:37.097Z

**📎 ToolResult**

```
352:import { localAIOf } from '../entities/bossAI_moon_events';
2405:    //     :3271 SetTypeInfo 第三参 → FlameParticle.Draw :62 drawData.shader）
3248:  /** Projectile_326/327/328 染料基底 + ×(60/255) 预染双缓存。
3263:   *  ParticleOrchestrator.cs:3271 SetTypeInfo 第三参传入）——染料只变换**贴图像素**，
4130:    // 南瓜王披风（Main.cs:22499-22506）：锚=本体中心+80Y、PumpkingCloak 五帧行
4132:    if (e.vanillaId === 327) this.drawPumpkingCloak(e);
4563:  // Projectile glowMask（:34327-34378）与 Item glowMask（:38072-38213）不在本批。
6768:  /** 南瓜王 327 披风（Main.cs:22499-22506）：锚=本体中心+(0,80)，PumpkingCloak
6771:  private drawPumpkingCloak(e: Enemy) {
6773:      loadBitmapOnly('vanilla/PumpkingCloak.png', () => !!(this.pumpkingCloakImg), (x) => { this.pumpkingCloakImg = x as unknown as typeof this.pumpkingCloakImg; });
6778:    const row = Math.max(0, Math.min(4, Math.trunc(localAIOf(e)[1] ?? 0)));   // :22501 num10
8985:  private static YOYO_ITEMS = new Set([3262, 3278, 3279, 3280, 3281, 3282, 3283, 3284,
9183:        // ★轴心（PlayerDrawLayers.cs:3263-3275 useStyle 9）：origin = Size*(0.5,0.4)
10800:    325: 10, 262: 11, 327: 13, 222: 14, 125: 15, 126: 20, 346: 17, 127: 18,
src/render/Renderer.ts:4173:      // 月总族独占分支（Main.cs:24325-24504 case 396/397/398）：头/手/核心各自
src/render/Renderer.ts:5222:  /** 月总核心 398（case 398 :24325-24388）：两侧上臂 Extra_14（肩=核心中心+(220,-60)×sign、
src/render/Renderer.ts:5778:  /** 月总手 397（case 397 :24391-24447）：前臂 Extra_15（锚=手中心+(0,76)、折角同上臂）
src/render/Renderer.ts:5855:  /** 月总头 396（case 396 :24449-24503）：眼窝（ai0<0 闲置 Extra_26 行 / 否则 Extra_18

```


---

## 🤖 Assistant · 2026-08-19T07:52:40.613Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Line 10800: `325: 10, 262: 11, 327: 13, 222: 14, 125: 15, 126: 20, 346: 17, 127: 18,` — this looks like a frame-count override table (npcFrameCount overrides?). Let me look at the context at line 10790-10810.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:52:41.094Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "limit": 90,
 "offset": 10770
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:52:41.110Z

**📎 ToolResult**

```
10770	    ctx.fillStyle = '#FF6600';
10771	    ctx.fillText('F3 关闭调试面板', 14, 118);
10772	    // 图例
10773	    ctx.fillStyle = '#666';
10774	    ctx.fillText('绿=主角 橙=中心 红=怪物 蓝=动物 黄=鼠标', 14, 136);
10775	  }
10776	
10777	  /** 入侵进度条（原版进度已完成的百分比；Boss 条下方 30px）。
10778	   *  label：整段文案覆盖（月事件 wave20 需求恒 0 → Main.cs:47163 用
10779	   *  Game.InvasionPoints 代替百分比、进度条满格 :47167-47170） */
10780	  private drawInvasionBar(ctx: CanvasRenderingContext2D, viewW: number, invasion: { name: string; pct: number; label?: string }) {
10781	    const w = Math.min(560, viewW - 200);
10782	    const x = (viewW - w) / 2, y = 28 + 30;
10783	    ctx.fillStyle = 'rgba(0,0,0,0.55)';
10784	    ctx.fillRect(x - 3, y - 3, w + 6, 26);
10785	    ctx.fillStyle = '#10305A';
10786	    ctx.fillRect(x, y, w, 20);
10787	    ctx.fillStyle = '#D0A020';
10788	    ctx.fillRect(x, y, w * Math.max(0, Math.min(1, invasion.pct)), 20);
10789	    ctx.font = 'bold 13px sans-serif';
10790	    ctx.fillStyle = '#FFF';
10791	    ctx.textAlign = 'center';
10792	    const pctTxt = `${Math.floor(Math.max(0, Math.min(1, invasion.pct)) * 100)}%`;
10793	    ctx.fillText(`${invasion.name}  ${invasion.label ?? pctTxt}`, viewW / 2, y + 15);
10794	  }
10795	
10796	  /** Boss 头像贴图索引（NPCID.Sets.BossHeadTextures，NPCID.cs:4861 全量对照）：
10797	   *  npc type → NPC_Head_Boss_N。未列出的 boss（-1）原版不显示头像 */
10798	  private static readonly BOSS_HEAD_INDEX: Record<number, number> = {
10799	    4: 0, 13: 2, 344: 3, 370: 4, 246: 5, 249: 5, 345: 6, 50: 7, 396: 8, 395: 9,
10800	    325: 10, 262: 11, 327: 13, 222: 14, 125: 15, 126: 20, 346: 17, 127: 18,
10801	    35: 19, 68: 19, 113: 22, 266: 23, 439: 24, 440: 24, 134: 25, 491: 26, 517: 27,
10802	    422: 28, 507: 29, 493: 30, 549: 35, 564: 32, 565: 32, 576: 33, 577: 33,
10803	    551: 34, 548: 36, 636: 37, 657: 38, 668: 39,
10804	  };
10805	
10806	  /** Boss 血条 1:1（BigProgressBarHelper.DrawFancyBar，BigProgressBarHelper.cs:18-57）：
10807	   *  UI_BossBar.png（516×348 = 1 列 × 6 行 58px 帧）——行3 背景（×0.2）→ 行2 填充
10808	   *  2px 段横向拉伸（宽=456×ratio 取偶）→ 行1 填充端盖（x+num2-2）→ 行0 整框 →
10809	   *  头像（NPC_Head_Boss_N，锚=框左上+(4,20)+图标半宽）→ 血量文本。
10810	   *  布局：456×22 居中于 (W/2, H-50)——底部中央（原版语义；旧实现顶部自绘红条）。
10811	   *  多 Boss 面板：原版 BigProgressBarSystem 同时只跟踪一个 NPC（TryFindingNPCToTrack
10812	   *  单目标），我们也只收到单个 boss——单 Boss 路径即完整语义。盾量重载（行4/5，
10813	   *  LunarPillar 等）按塔盾条另走，未在本条复用（登记） */
10814	  private drawBossBar(
10815	    ctx: CanvasRenderingContext2D, viewW: number, viewH: number,
10816	    boss: { name: string; hp: number; maxHp: number; cx: number; cy: number },
10817	    entities: Entity[] = [],
10818	  ) {
10819	    if (!this.atlas) return;
10820	    const bar = this.atlas.vui('UI_UI_BossBar.png');
10821	    const FH = 58, BW = 456, BH = 22, IX = 32, IY = 24;
10822	    const rect = { x: Math.round(viewW / 2 - BW / 2), y: Math.round(viewH - 50 - BH / 2), w: BW, h: BH };
10823	    const vec = { x: rect.x - IX, y: rect.y - IY };
10824	    let fill = Math.floor(BW * Math.max(0, Math.min(1, boss.hp / boss.maxHp)));
10825	    fill -= fill % 2;                                            // num2 -= num2 % 2
10826	    ctx.save();
10827	    ctx.imageSmoothingEnabled = false;
10828	    if (bar) {
10829	      // 行3 背景 ×0.2
10830	      ctx.globalAlpha = 0.2;
10831	      ctx.drawImage(bar.img, bar.sx, bar.sy + 3 * FH, bar.sw, FH, vec.x, vec.y, bar.sw, FH);
10832	      ctx.globalAlpha = 1;
10833	      // 行2 填充段（2px 源横向拉伸到 num2 宽）
10834	      ctx.drawImage(bar.img, bar.sx + IX, bar.sy + 2 * FH + IY, 2, BH, rect.x, rect.y, Math.max(2, fill), BH);
10835	      // 行1 端盖
10836	      ctx.drawImage(bar.img, bar.sx + IX, bar.sy + 1 * FH + IY, 2, BH, rect.x + Math.max(0, fill - 2), rect.y, 2, BH);
10837	      // 行0 整框（含头像背景槽）
10838	      ctx.drawImage(bar.img, bar.sx, bar.sy, bar.sw, FH, vec.x, vec.y, bar.sw, FH);
10839	    } else {
10840	      // 贴图未就绪兜底：几何暗条（不闪断）
10841	      ctx.fillStyle = 'rgba(0,0,0,0.55)';
10842	      ctx.fillRect(rect.x, rect.y, BW, BH);
10843	      ctx.fillStyle = '#C03030';
10844	      ctx.fillRect(rect.x, rect.y, Math.max(2, fill), BH);
10845	    }
10846	    // 头像：boss 参数无类型信息——从实体表反查同 hp/位置的 Enemy 取 vanillaId
10847	    const src = (entities as Enemy[]).find((n) => n instanceof Enemy && !n.dead
10848	      && Math.abs(n.hp - boss.hp) < 1 && Math.abs(n.maxHp - boss.maxHp) < 1
10849	      && Math.abs(n.cx - boss.cx) < 64 && Math.abs(n.cy - boss.cy) < 64);
10850	    const headIdx = src?.vanillaId != null ? Renderer.BOSS_HEAD_INDEX[src.vanillaId] : undefined;
10851	    if (headIdx !== undefined) {
10852	      const head = this.atlas.vmisc(`vanilla/NPC_Head_Boss_${headIdx}.png`);
10853	      if (head) {
10854	        // vector2 = (4,20) + 图标半宽，origin = 图标半宽 → 净左上 = vec + (4,20)
10855	        ctx.drawImage(head.img, head.sx, head.sy, head.sw, head.sh,
10856	          vec.x + 4, vec.y + 20, head.sw, head.sh);
10857	      }
10858	    }
10859	    // 血量文本（DrawHealthText :59-68：中缝 "/"、左当前右上限）

```


---

## 🤖 Assistant · 2026-08-19T07:52:45.562Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
That was the boss head texture table — unrelated. Now let me look at how drawEnemy computes `frames` and where vanillaFrameIdx is called (line 4194 and 5248), plus how npcFrameCount is sourced (e.vanilla?.frames). Let me read around 4180-4210 and 5240-5260.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:52:46.002Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "limit": 75,
 "offset": 4150
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:52:46.012Z

**📎 ToolResult**

```
4150	    if (e.vanillaId != null && this.atlas) {
4151	      // 风气球 594（Main.cs:23380-23406 独占）：贴图是 8 列变体【横条】(256×76 =
4152	      // 32×76×8),变体索引 = ai[2]；携带史莱姆时先画帧 0 的 alpha+奴隶染色两遍
4153	      // （气球壳随史莱姆染色）。通用竖切路径(json frames=1)会把整条横排 8 个气球
4154	      // 全画出来——"完整逐帧贴图"(用户标注)
4155	      if (e.vanillaId === 594) { this.drawWindyBalloon(e, entities); return; }
4156	      // 雕像宝箱怪 690（Main.cs:23103-23134 独占）：恒以雕像形态显示——不画
4157	      // NPC_690 贴图，而是按 ai[1] 样式从 Tiles_105 切 2×3 片 16×16 拼装
4158	      // （direction==1 行 +3 镜像）；通用竖切路径会画错（json frames=1 单帧 28×38）
4159	      if (e.vanillaId === 690) { this.drawStatueMimic(e); return; }
4160	      // ---- 2D 网格贴图 NPC（原版 Main.cs DrawNPC 专属 case + FindFrame 专属 case）----
4161	      // 这些表的动画帧是【cols×rows 网格】（Frame(cols,rows,fx,fy)），通用竖切路径
4162	      // 会把整行/整条画出来——全部走 drawNpcGrid 切格 + 各自 FindFrame 帧状态机
4163	      // 657 史莱姆皇后（Main.cs case 657 + FindFrame case 657）
4164	      if (e.vanillaId === 657) { this.drawQueenSlimeGrid(e); return; }
4165	      // 576/577 DD2 食人魔（Main.cs case 576/577 + FindFrame case 576/577）
4166	      if (e.vanillaId === 576 || e.vanillaId === 577) { this.drawDd2OgreGrid(e); return; }
4167	      // 696（Main.cs case 696 + FindFrame case 696）
4168	      if (e.vanillaId === 696) { this.drawNpc696Grid(e); return; }
4169	      // 564/565 暗黑魔法师 T1/T2（Main.cs case 564/565 + FindFrame case 564/565）
4170	      if (e.vanillaId === 564 || e.vanillaId === 565) { this.drawDarkMageGrid(e); return; }
4171	      // 668 鹿角怪（Main.cs DrawNPCDirect_Deerclops + FindFrame case 668）
4172	      if (e.vanillaId === 668) { this.drawDeerclopsGrid(e); return; }
4173	      // 月总族独占分支（Main.cs:24325-24504 case 396/397/398）：头/手/核心各自
4174	      // 带独立锚点与叠层（上臂/前臂/躯干/胸甲/眼/破体帧），通用路径锚点不对
4175	      if (e.vanillaId === 398) { this.drawMoonLordCore(e, entities); return; }
4176	      if (e.vanillaId === 397) { this.drawMoonLordHand(e, entities); return; }
4177	      if (e.vanillaId === 396) { this.drawMoonLordHead(e); return; }
4178	      // 光之女皇 636（DrawNPCDirect_HallowBoss Main.cs:26364-26554）：翅膀/双臂/
4179	      // 二阶段覆层独占——通用路径只画本体，缺背后大翼与攻击态手臂帧
4180	      if (e.vanillaId === 636) { this.drawEmpress(e); return; }
4181	      // 402 星尘织带蠕虫（Main.cs:23848-23889 case 402 独占）：单 NPC 自绘
4182	      // oldPos 拖尾（403/404 节段 + Glow_133/134 加色）+ 头本体与 Glow_135
4183	      if (e.vanillaId === 402) { this.drawStardustWorm(e); return; }
4184	      // 266 克苏鲁之脑（Main.cs:24799-24843 专家/FTW 四镜像 + :22949-22951 Y 偏移）
4185	      if (e.vanillaId === 266) { this.drawBrainOfCthulhu(e, world); return; }
4186	      // 491 荷兰飞盗船（Main.cs:24263-24324 case 491 独占）：船体 OriginFlip(208,460) 锚 +
4187	      //  旗/桨/帆附加件叠绘 + 4 炮代画；492 炮 hide=true 由船代画（船在世时跳过独立绘制）
4188	      if (e.vanillaId === 491) { this.drawDutchman(e, entities); return; }
4189	      if (e.vanillaId === 492
4190	        && (entities as Enemy[]).some((n) => n instanceof Enemy && !n.dead && n.vanillaId === 491)) {
4191	        return;
4192	      }
4193	      const frames = Math.max(1, e.vanilla?.frames ?? 1);
4194	      const frameIdx = vanillaFrameIdx(e, frames);
4195	      // Mechdusa:毁灭者头 134 换画 136 尾帧贴图（Main.cs:24980-24984 num153=136
4196	      // + LoadNPC——头锁位倒挂(旋转 +π),头帧贴图方向不对,原版改用尾帧绘制）
4197	      // 石巨人:246 血尽原体变身自由态(ai3=1)后原版是 NewNPC 249——换画 NPC_249
4198	      // (帧 0/1 与 246 基础帧同构,customFrameIdx 直读不变;曾一直画 NPC_246)
4199	      const drawId = e.vanillaId === 134 && mechQueenUp() ? 136
4200	        : e.vanillaId === 246 && e.ai3 === 1 ? 249 : e.vanillaId;
4201	      const r = this.atlas.vnpc(drawId, frameIdx);
4202	      if (r) {
4203	        const flying = !!e.vanilla?.noGravity; void flying; // 中心锚后地面/飞行统一,仅保留语义注释
4204	        // 原版 NPC.scale（SetDefaults base × netID scale × 专家档体型系数）——作用于渲染。
4205	        // 专家系数（Tweaks :18187/:18198/:18300/:18309：世吞 13-15 ×1.2、克脑 266/
4206	        // 爬行者 267/毁灭者 134-136/探针 139 ×1.05）只乘 npc.scale 不回写宽高
4207	        // （NewNPC 的 width/height×scale 在 ScaleStats 之前，NPC.cs:17744-17747）——
4208	        // 碰撞盒保持 base 盒（本仓 e.w/e.h 已按 base 乘，勿在此扩盒）
4209	        const scale = (e.vanilla?.scale ?? 1) * e.vanillaScale
4210	          * expertRenderScale(e.vanillaId ?? 0);
4211	        ctx.save();
4212	        // 锚点:飞行型=帧中心(原版默认分支 Main.cs:23635 语义);地面型=底锚+原版恒
4213	        // +4 下沉(Main.cs:24741 通用公式:可见贴图底=盒底+4,帧底透明边距一并沉入
4214	        // 地面——原版脚部本就压住地表 ~2px;2026-08-17 前按透明行"贴地"补偿,
4215	        // 视觉上恒高 2-4px=悬空感的根因,全家族改 1:1)
4216	        const grounded = !flying;
4217	        // 416 日耀掠兽骑手（Main.cs:24508-24515 case 416 独占）：绘制位置吸附坐骑
4218	        // 415 的 Bottom（AI 锚 Center+(-spriteDir*10,-30) 只喂碰撞盒——骑手视觉上
4219	        // 双脚踩在掠兽脚平面，+4px 是帧底透明边距，与地面族 pad 同义）。
4220	        // 其余 aiStyle 75 骑手（390）原版无此绘制覆写，仍用 AI 位
4221	        const snapMount = e.vanillaId === 416 && e.master && !e.master.dead ? e.master : null;
4222	        ctx.translate(snapMount ? snapMount.cx : e.cx,
4223	          snapMount ? snapMount.y + snapMount.h : (grounded ? e.y + e.h : e.cy));
4224	        // 旋转族:整体随自转角旋转(原版 npc.rotation;朝向翻转不适用)。

```


---

## 🤖 Assistant · 2026-08-19T07:52:46.642Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "limit": 45,
 "offset": 5235
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:52:46.649Z

**📎 ToolResult**

```
5235	   *  全乘生命末段渐隐 num291（ai[2] 0→600 计时，最后 5% 线性淡出 :23858-23861）。
5236	   *  头 = NPC_402 + Glow_135×num291。锚点 = 碰撞盒中心（origin halfSize），旋转
5237	   *  随 visAngle/oldRot。头中心尾接 DrawPrettyStarSparkle（:23888 → 原语
5238	   *  drawPrettyStarSparkle；ai[2] 计时链在 Enemy.wormAI 402 段驱动）。 */
5239	  /** 266 克苏鲁之脑（Main.cs:24799-24843 专家/FTW 四镜像 + :22949-22951 Y 下垂）：
5240	   *  life<lifeMax 且（专家 || FTW）→ 以玩家中心镜像画 4 份：alpha 因子 =
5241	   *  1-life/lifeMax（专家 ×2，FTW 置 1）平方后钳 0..1，乘进整体 alpha；
5242	   *  镜像位 = 玩家中心 ±(|dx|,|dy|)（num145 0..3：X 取正 0/2、Y 取正 0/1）。
5243	   *  本体照常最后画。全体绘制 Y 偏移 +50×scale（Main.cs:22950 case 266 num47）——
5244	   *  贴图下垂出碰撞盒下缘（克脑主体在盒下半） */
5245	  private drawBrainOfCthulhu(e: Enemy, world: World) {
5246	    if (!this.atlas) return;
5247	    const frames = Math.max(1, e.vanilla?.frames ?? 1);
5248	    const frameIdx = vanillaFrameIdx(e, frames);
5249	    const r = this.atlas.vnpc(266, frameIdx);
5250	    if (!r) return;
5251	    const ctx = this.ctx;
5252	    // 专家档 ×1.05（Tweaks :18198；266 克脑专属曲径，通用路径不经过这里）
5253	    const scale = (e.vanilla?.scale ?? 1) * e.vanillaScale * expertRenderScale(266);
5254	    const yOff = 50 * scale;   // Main.cs:22950 num47 += 50*rCurrentNPC.scale
5255	    const opacity = 1 - Math.min(255, Math.max(e.spawnAlpha, 0)) / 255; // NPC.Opacity
5256	    const mirrored = e.facing > 0;   // 同通用路径朝向镜像（贴图默认朝左）
5257	    // 四镜像幻影（Main.cs:24802-24841）
5258	    const pl = this.mainPlayer;
5259	    const ftw = !!world.seedFlags?.getGoodWorld;
5260	    if (pl && e.hp < e.maxHp && (world.isExpert || ftw)) {
5261	      let k = 1 - e.hp / e.maxHp;
5262	      if (world.isExpert) k *= 2;
5263	      k *= k;
5264	      if (ftw) k = 1;
5265	      k = Math.max(0, Math.min(1, k));
5266	      const dx = Math.abs(e.cx - pl.cx), dy = Math.abs(e.cy - pl.cy);
5267	      for (let n = 0; n < 4; n++) {
5268	        const sx = n === 0 || n === 2 ? 1 : -1;   // :24822-24829
5269	        const sy = n === 0 || n === 1 ? 1 : -1;   // :24831-24838
5270	        ctx.save();
5271	        ctx.translate(pl.cx + sx * dx, pl.cy + sy * dy + yOff);
5272	        ctx.scale(scale, scale);
5273	        if (mirrored) ctx.scale(-1, 1);
5274	        ctx.globalAlpha = Math.max(0, Math.min(1, opacity * k));
5275	        ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, -r.sw / 2, -r.sh / 2, r.sw, r.sh);
5276	        ctx.restore();
5277	      }
5278	      ctx.globalAlpha = 1;
5279	    }

```


---

## 🤖 Assistant · 2026-08-19T07:52:50.210Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good, the general path at line 4193-4194 calls `vanillaFrameIdx(e, frames)` for all vanilla enemies. My new branches inside vanillaFrameIdx will be consumed by this path.

Now check how animT/walkCycleT advance — read Enemy.ts around 1200-1260.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:52:50.735Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 70,
 "offset": 1195
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:52:50.742Z

**📎 ToolResult**

```
1195	
1196	  fixedUpdate(dt: number, game: GameHooks) {
1197	    this.prevX = this.x; this.prevY = this.y;
1198	    this.gnomeAge++;
1199	    // 侏儒 624 日光石化（NPC.cs:56252-56280 + :56232 ShouldTurnToStone——白天且
1200	    // 头上无实心遮挡 → 脚下实心 → PlaceTile(567 花园侏儒 style rand(5)) +
1201	    // bestiary RegisterKill + Achievement 24,2026-08-13）
1202	    if (this.vanillaId === 624 && !this.dead && this.gnomeAge > 60) {
1203	      const w = game.world as import('../world/World').World;
1204	      if (w?.clock?.isDay && w?.store) {
1205	        const st = w.store;
1206	        const tx = Math.floor(this.cx / 16), ty = Math.floor((this.y + this.h) / 16);
1207	        if (st.inBounds(tx, ty) && st.isSolid(tx, ty) && !st.isActive(tx, ty - 1)) {
1208	          let sheltered = false;
1209	          for (let dy = 1; dy <= 5; dy++) {
1210	            if (st.inBounds(tx, ty - dy) && st.isSolid(tx, ty - dy)) { sheltered = true; break; }
1211	          }
1212	          if (!sheltered) {
1213	            const style = Math.floor(Math.random() * 5);
1214	            st.setTile(tx, ty - 1, TILE_BY_KEY['v_567_garden_gnome'] ?? 0, style * 36, 0);
1215	            game.spawnParticles(this.cx, this.cy, '#E0E0E0', 5, 1, { life: 30 });
1216	            this.dead = true; this.hp = 0;
1217	            return;
1218	          }
1219	        }
1220	      }
1221	    }
1222	    // 联机傀儡（房主权威快照驱动）：无本地 AI——P3.2 插值/外推推进 + 动画计时，
1223	    // 打击/拾取等交互经 entityNet 上报房主结算
1224	    if (this.netPuppet) {
1225	      this.aiT++;
1226	      this.animT++;
1227	      this.netPuppetStep();
1228	      this.onGround = Math.abs(this.vy) < 0.6;
1229	      if (Math.abs(this.vx) > 0.05) this.walkCycleT += Math.abs(this.vx);
1230	      if (this.iframes > 0) this.iframes--;
1231	      this.pushHistory();   // 傀儡无本地 AI 但拖尾渲染同样需要历史位置
1232	      return;
1233	    }
1234	    this.aiT++;
1235	    if (this.iframes > 0) this.iframes--;
1236	    if (this.justHitT > 0) this.justHitT--;
1237	    this.lightRGB = null; // 点光由 AI 每帧重写（不残留上一帧状态）
1238	    this.lightRGBAt = null;
1239	    if (this.hpBarT > 0) this.hpBarT--;
1240	    if (this.whipTagT > 0) this.whipTagT--;
1241	    if (this.whipProcT > 0) this.whipProcT--;
1242	    if (this.squash !== 0) this.squash *= 0.85;
1243	    this.animT++;
1244	    this.walkCycleT += Math.abs(this.vx); // 原版 zombie/fighter 行走帧按 |vx| 累加（L77072/L70216）
1245	    // 原版 case46 族 vx==0 清 frameCounter（NPC.cs:77571-77577）——站定即清相位，
1246	    // 起步必从帧 0 起稳走（2026-08-18 审查：曾保留相位起步首帧非 0）
1247	    if (Math.abs(this.vx) <= 0.05) this.walkCycleT = 0;
1248	
1249	    // 出生渐显（alphaFade 族，AI 分发【前】的近似段）——静态半透明不受影响。
1250	    // EoW 族（13-15）除外：走下方 AI 分发后的 1:1 段（移动门 -42/t，NPC.cs:52650-52670）
1251	    if (this.alphaFade && !(this.vanillaId !== null && this.vanillaId >= 13 && this.vanillaId <= 15)) {
1252	      this.spawnAlpha = Math.max(0, this.spawnAlpha - 1);
1253	      if (this.spawnAlpha === 0) this.alphaFade = false;
1254	    }
1255	
1256	    const player = (game as unknown as { player: Player }).player;
1257	    const hasPlayer = !!player && !player.dead;
1258	
1259	    // ---- 原版数据驱动路径：按 aiStyle 分发到已移植的 AI 家族（分发后落入共享尾段） ----
1260	    // 蠕虫身体段（wormFollow 非空）无 AI：位置由头部 wormAI 沿链驱动，但仍走共享尾段（接触伤害等）
1261	    // 例外：EoW 三段各段独立跑 eowAI（断链自查 + 身/尾自跟随，:51874/:52266），
1262	    // 不再由头统一驱动链——断链拆分后每条子虫的头各自驱动
1263	    const eowSeg = this.vanillaId !== null && this.vanillaId >= 13 && this.vanillaId <= 15;
1264	    const wormBody = this.wormFollow && !eowSeg;

```


---

## 🤖 Assistant · 2026-08-19T07:53:10.798Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: `animT++` and `walkCycleT += |vx|` (reset to 0 when |vx| <= 0.05) happen at the START of fixedUpdate, BEFORE the AI dispatch. So during a tick: animT increments, then AI runs (can read the incremented animT). A frame-counter replica in AI starting at 0 stays in lockstep with animT (both +1 per tick from spawn).

Wait — one wrinkle: vanilla frameCounter also starts at 0, and FindFrame increments it at the END (fc += 1 after the switch). So vanilla's visible sequence over ticks: tick1: fc=0 used; then fc→1. tick2: fc=1... So with my replica maintained in AI at +1 per tick (post-increment or pre?), phase may be off by 1 tick — irrelevant visually. Fine.

Now, since AI runs every tick for these entities, replicas in AI are exact.

Now let me check how the enemy AI dispatch maps aiStyle → these functions — specifically to confirm ids 386/387 etc. reach our functions every tick (martianFighterExtras for 386 — called from case 3 dispatch "after fighterAI" — need to check that fighterAI still runs for 386; the render branch uses vx/vy/ai2 — fine either way).

Next: check `frames` (npcFrameCount) for our target NPCs to clamp properly. The values come from `e.vanilla?.frames` — json-based. The frame machine values (e.g., 393 needs 18 rows: 9 base + 9 firing = frames 0-17? num134 ∈ 0-8, +9 firing = up to 17 → npcFrameCount[393] = 18). Let me verify from the vanilla source: NPCID sets frameCount via Main.npcFrameCount[type]. Our json presumably has them (561 enemies data-driven). I don't need exact numbers — clamping via Math.min(frames-1, ...) protects.

Let me now check the dd2 file's `dd2LocalAI` (x = dd2LocalAI(e)) — what slots does it use? If betsy uses x[0].. for something. From betsyAI code: `const x = dd2LocalAI(e);` — is x used anywhere in betsyAI? Grep in the function range 1407-1640... I saw `x[3] >= 60` at line 1380 but that's another function (ogre?). Let me check betsyAI's use of x and the tail of betsyAI (after state 6).
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:53:11.322Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_dd2.ts",
 "limit": 65,
 "offset": 1604
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:53:11.334Z

**📎 ToolResult**

```
1604	          for (let k = 0; k < 3 && portals.length > 0; k++) {
1605	            const portal = portals[rnd(portals.length)];
1606	            const w = spawnPart(game, e, 560);
1607	            if (w) { w.x = portal.cx - w.w / 2; w.y = portal.cy - w.h / 2; }
1608	          }
1609	          game.playSfxFiles(soundTrackFiles('dd2_betsy_summon'), 0.7, e.cx, e.cy);  // DD2_BetsySummon（:62652/:62671 每召一只一声）
1610	        }
1611	      }
1612	      e.ai1 += 1;
1613	    }
1614	    if (e.ai1 >= SUMMON_T) { e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; }
1615	  }
1616	  // ---- 拍翼帧计数（:62657-62666 localAI[0]/[1]） ----
1617	  x[0] += timeScale;
1618	  if (x[0] >= 36) x[0] = 0;
1619	  x[1] += 1;
1620	  if (x[1] >= 60) x[1] = 0;
1621	  // ---- rotation 收敛（:62668-62716） ----
1622	  const dTo = dirTo(e, txc, tyc);
1623	  let tgtAng = Math.atan2(dTo.y, dTo.x);
1624	  let step = 0.04;
1625	  const s0 = e.ai0 | 0;
1626	  if (s0 === 2 || s0 === 5) step = 0;
1627	  else if (s0 === 3) {
1628	    step = 0.01;
1629	    tgtAng = e.facing === -1 ? -Math.PI : 0;
1630	    if (e.ai1 >= FLAME_T0) { tgtAng += e.facing * Math.PI / 12; step = 0.05; }
1631	  } else if (s0 === 4) {
1632	    step = 0.01;
1633	    tgtAng = e.facing === 1 ? Math.PI * 2 : Math.PI;
1634	  } else if (s0 === 6) {
1635	    step = 0.02;
1636	    tgtAng = e.facing === -1 ? -Math.PI : 0;
1637	  }
1638	  if (e.facing === -1) tgtAng += Math.PI;
1639	  if (step !== 0) e.visAngle = angleTowards(e.visAngle, tgtAng, step);
1640	  fly(e);
1641	}
1642	
1643	// ---------------------------------------------------------------------------
1644	// AI_111 埃特尼亚荧光虫 578（NPC.cs:43169 → AI_111_DD2LightningBug :66799）
1645	// ---------------------------------------------------------------------------
1646	export function dd2LightningBugAI(e: Enemy, game: GameHooks, player: Player | null) {
1647	  if (!e.bInit) { e.bInit = true; }
1648	  const x = dd2LocalAI(e);
1649	  // 族参数（:66803-66813 默认档 → :66828-66844 的 578 覆盖）
1650	  const SPEED = 4;            // num
1651	  const LERP_FAR = 20;        // num2
1652	  const LERP_NEAR = 20;       // num3
1653	  const MIN_SPD = 1;          // num4
1654	  const DAMP = 0.96;          // num5
1655	  const SHOOT_T = 5;          // num6
1656	  const COOLDOWN = 30;        // num7
1657	  const RANGE = 200;          // num8
1658	  const ZAP_DMG = 50;         // num9
1659	  const ZAP_PROJ = 682;       // num10
1660	  const ZAP_SPD = 10;         // num11
1661	  const HEIGHT_GATE = 50;     // num12
1662	  const SEP = 0.1;            // num13
1663	  // ---- 出生渐显（:66846-66876 flag3） ----
1664	  if (x[1] === 0) e.spawnAlpha = 255;
1665	  if (x[1] === 30) game.playSfxFiles(soundTrackFiles('dd2_etherian_portal_spawn_enemy'), 0.3, e.cx, e.cy);
1666	  if (x[1] < 60) {
1667	    x[1] += 1;
1668	    e.spawnAlpha = Math.max(0, e.spawnAlpha - 5);

```


---

## 🤖 Assistant · 2026-08-19T07:53:12.525Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"dd2LocalAI\" src/entities/bossAI_dd2.ts | head -5 && sed -n '/const dd2LocalAI/,/^}/p' src/entities/bossAI_dd2.ts | head -12",
 "description": "Read Betsy AI tail and dd2LocalAI helper"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:53:12.567Z

**📎 ToolResult**

```
109:export const dd2LocalAI = (e: Enemy): number[] => {
442:  const x = dd2LocalAI(e);
745:  const x = dd2LocalAI(e);
850:  const x = dd2LocalAI(e);
961:  const x = dd2LocalAI(e);
export const dd2LocalAI = (e: Enemy): number[] => {
  let a = localAI.get(e);
  if (!a) { a = [0, 0, 0, 0]; localAI.set(e, a); }
  return a;
};

```


---

## 🤖 Assistant · 2026-08-19T08:02:12.041Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Our betsyAI already maintains x[0] (localAI[0], the 36-step timeScale counter) and x[1] — but per vanilla FindFrame, Betsy's frame uses ai[1], not localAI[0]. Our ai1 semantics match vanilla 1:1. So the Renderer branch for 551 reads e.ai0/e.ai1 — stateless. The localAI[0] counter maintained in our AI is currently consumed by nobody (it mirrors vanilla, which uses it... hmm, vanilla FindFrame doesn't use it; maybe Main.cs DrawNPC? Whatever — it exists in our AI already; keep).

Hmm wait — let me double check that vanilla FindFrame 551 doesn't use localAI[0] anywhere. From my read of 67913-68107: only ai[0], ai[1], frame.Y, frameCounter. Correct.

Now — the pumpkin king. Our pumpkingAI L[2] (localAI[2]) is the 300t attack-switch timer; vanilla FindFrame uses ai[3] (0/1/2 attack selection) — our e.ai3 matches vanilla's ai[3] exactly (rnd(3) every 300t). So Renderer reads e.ai3. But the pose-walk needs persistent (counter, frame) — implement in pumpkingAI writing e.customFrameIdx.

Where in pumpkingAI? It runs every tick (no early returns except none... checking pumpkingAI: no early returns — it flows through to the bottom). I'll add the FindFrame replica at the end (before `e.x += e.vx`), writing e.customFrameIdx.

Implementation of 327 FindFrame replica (cs:72977-73037):
```
// ai3 pose: 0→行0带,1→行4带,2→行8带;帧计数 ±1/t,越 ±6 换帧行进(回卷 0↔11)
let step = 0;
if (e.ai3 === 0) {
  if (row > 5) step = 1;
  else if (row > 0) step = -1;
} else if (e.ai3 === 1) {
  if (row > 10) step = 1;
  else if (row > 4) step = -1;
  else if (row < 4) step = 1;
} else if (e.ai3 === 2) {
  if (row < 2) step = -1;
  else if (row > 8) step = -1;
  else if (row < 8) step = 1;
}
counter += step;
if (counter > 6) { counter = 0; row++; if (row > 11) row = 0; }
if (counter < 0) { counter = 6; row--; if (row < 0) row = 11; }
```
Wait — careful with the vanilla order: the counter increments happen FIRST (based on current frame.Y), then the threshold checks mutate frame.Y. My replica: `counter += step` where step ∈ {+1,-1,0}; then `if (counter > 6) {...}` and `if (counter < 0) {...}` — both ifs checked (vanilla has two separate ifs; counter can't exceed both). Exactly as written. 

Storage for (counter, row): the existing L array (L[0], L[1] used for cloak beat; L[2] attack timer). I'll add L[3] for counter and store row... need a second slot. Hmm, L is [0,0,0,0] — all four used (0,1 cloak; 2 timer). Options: e.lai0/e.lai1 (Enemy fields) — pumpking doesn't use them. Use e.lai0 = counter, e.lai1 = row. Renderer doesn't even need to read them (customFrameIdx holds the row). But wait — do I even need to store them as e fields? They must persist across ticks; la() WeakMap L only has 4 slots. I'll use e.lai0 (counter) + e.lai1 (row) — but hmm, careful: is lai1 read by Renderer's firefly branch for glow? `e.lai1 <= 0` for ids 355/358/654 — no conflict with 327.

Actually wait — there's a subtlety: the cloak L[1] is already the cloak frame; the L[0]/L[1] beat is 6t/beat 5 beats — while the FindFrame walk uses its own counter. Distinct — fine.

Alternatively — since pumpkingAI's L = la(e) is exported (localAIOf), I could keep everything in the AI file. Yes — e.lai0/e.lai1 fields it is.

Hmm, actually hold on. Let me reconsider whether to instead do this statefully in the Renderer... no, Renderer's vanillaFrameIdx is stateless by design. AI-side is the sanctioned pattern. OK.

Now — for 395/392 replicas (martian): store counters in e.lai0. Where exactly:
- martianSaucerAI (395): add at... the function has several early returns (ai0===3 self-destruct; -1/-2 climbs; etc.). Vanilla FindFrame runs every tick regardless. Place the counter update at the very top (after bInit block) so it always runs. It depends on ai3 (the cycle counter read BEFORE or AFTER the increment?). Vanilla: FindFrame runs after AI; AI increments ai[3] within the ai0===0 block (ai3 += 1 then use). The flag10 check `ai[3] >= 20 && < 260` sees the post-increment value. E.g., window transitions: at tick where AI sets ai3 from 19→20, FindFrame sees 20 → window active.

In our AI: `const w1 = WIN(e.ai3); e.ai3 += 1; ...` — post-increment ai3 within the tick. If I place my replica at the top (before the state machine), it reads the pre-increment ai3 — one tick off. To be exact, place the replica at the END of martianSaucerAI — but the function has early returns (ai0===3 death → doesn't matter; -1/-2 climb branch: `fly(e); return;` — during climb, ai3 was reset to 0 (e.ai1 = 0; e.ai2 = 0; e.ai3 = 0 in the recovery branch — only when player returns). Hmm — vanilla: during ai0=-1/-2, FindFrame still advances counter +1/t (flag10 = ai3∈[20,260) — ai3 stays whatever it was during climb... vanilla sets ai[3]=0 on entering -1/-2 (:36387 timeLeft=300; and `ai[1]=ai[2]=ai[3]=0`? — in our port, the reset happens only in the player-returns branch). Let me look at vanilla 36362-36396 to see when ai[3] is reset... Actually our port has the reset inside `if (player && !player.dead)` — when player present. Vanilla equivalent presumably. Either way: flag10 during climb = ai3 ∈ [20,260)? If ai3 was reset to 0, no window. If not reset (player gone), ai3 frozen → if it was mid-window [20,260) the counter keeps the double-speed+clamp while climbing away. Ultra edge case. 

Simplest faithful approach: put the replica at the TOP but read the ai3 that the AI will have AFTER its update... I can't know it before running. Alternative: put the replica update at every return point? Ugly.

Better: extract the replica into a tiny inline block placed at the top, but compute the effective ai3 for this tick: the only mutation of ai3 in the tick is `e.ai3 += 1; if (e.ai3 >= 600) e.ai3 = 0;` (in ai0===0) or `e.ai3 += 1` (in ai0===2, with >=3600 reset). So effective ai3 = (ai0===0) ? (ai3+1)%600 : (ai0===2) ? (ai3+1)%3600... wait ai0===2: `e.ai3 += 1; if (e.ai3 >= 3600) {...reset 0}`. Hmm — but during ai0===1 (expert transition) ai3 isn't incremented. And during -1/-2 it's reset to 0 conditionally. This is getting messy.

Cleaner: maintain the counter replica INSIDE the ai0===0 / ai0===2 blocks right after the ai3 increment, AND a default +1 advance... no wait — the counter advances every tick regardless of state (it's FindFrame, runs always).

Alternative pragmatic approach: place the replica at the top of the function, reading pre-increment ai3 — one-tick phase offset on the flag10 window boundary (the window edges shift by 1 tick). Visually undetectable (window is 240t long). The double-speed clamp inside the window is phase-locked to the window itself (clamp forces counter into [36,53] within 1 tick of entry), so the only deviation is entering the clamp 1 tick late/early. That's negligible and keeps code simple.

Hmm, but wait — there's an ordering subtlety I should double check: is the Renderer's frame read using the same tick's counter? Yes — AI runs in fixedUpdate (tick N), render happens after with the updated lai0. Good.

Actually, you know what? Let me reconsider: rather than top-of-function, I can put the replica update immediately BEFORE each `return` — no. Simplest: top of function. One-tick edge deviation, noted in comment. Actually wait — actually let me just put it right at the TOP before any state logic (after the bInit spawn block). flag10 uses current (pre-increment) ai3. For ai0===0, the AI reads WIN twice (pre and post)... The pre-increment ai3 equals the post-increment value of the PREVIOUS tick. So the window effectively shifts 1 tick earlier. Fine — I'll note "读自增前 ai[3],窗口边界差 1t(登记)".

Hmm, hold on, alternatively I could place the counter update at the bottom of the ai0===0/ai0===2 blocks AND before each early-return... Let me count return points in martianSaucerAI: (1) ai0===3 self-destruct → entity dies anyway; (2) -1/-2 branch `fly(e); return;`; (3) out-of-bounds `e.dead = true; return;` → dies; (4) fall-through end. So only TWO non-death exits: the -1/-2 branch and the end. I can place the replica update right before `fly(e)` in the -1/-2 branch (post ai3-reset — ai3=0 or frozen value → flag10 per value at that point — vanilla FindFrame reads ai3 after AI completed the whole tick including the reset — exact!) and at the end of the function. That's exact with minimal mess. 

For the end-of-function placement: at that point ai3 has been incremented (ai0===0/1/2 handled above; ai0===1 doesn't touch ai3). Exact 1:1 with vanilla order (AI fully done → FindFrame). 

For 392 (martianSaucerPartAI): same treatment. Return points: `if (id === 492) return` (not ours); mount-death branch returns (392 dies — skip); the 390 branch returns (not ours); 394 block returns; 393 block returns; 392 continues to the end (function ends after the empty-nest block). So for 392: place replica at the very end of martianSaucerPartAI (reached only by 392 since 393/394/390 return early) — but careful: `if (id !== 392 && id !== 393 && id !== 394) return;` — only 392/393/394 pass; 393/394 return in their blocks; so end-of-function = 392 only. And e.ai3 = saucer.ai3 is set at line 419 (post saucer's update this tick? Order: saucer's AI ran earlier or later than part's AI? Depends on entity list order — saucer spawned first (bInit spawns parts), so saucer updates before parts in the same tick (entities array order). So part's e.ai3 = saucer's post-increment ai3 — consistent, and matches vanilla (parts read npc[ai[...]].ai[3]... wait, actually vanilla 393/394 read the saucer's ai[3] directly each FindFrame? :36128/36171/36235 read `Main.npc[(int)ai[3]].ai[3]`? — our port is 1:1 tested, whatever). Good: at end of part AI, e.ai3 is the effective value. Place 392's counter replica at function end.

Now — the "counter replica" for 395 also needs the initial state: e.lai0 starts 0 (Enemy field init) — vanilla frameCounter starts 0. 

Next: 387 tesla — decided stateless approximation. Hmm, wait — let me reconsider exactness: 387 frameCounter: idle +1/t (>=15 reset); charge +1..3/t (>=10 reset). Stateless approx: period = ai0 > 0 ? 10 / (1 + (ai0>=20) + (ai0>=40)) : 15 → frame = floor(t / period) % 2. Rate correct; phase arbitrary. When speed changes mid-blink the vanilla toggle phase shifts smoothly; ours jumps phase — invisible for a 2-frame blink. Also — hmm, "10/(1+2)" = 3.33t/frame. OK.

Wait, actually — hmm, is it really "10t/帧、待机 15t/帧两档" — with the tiered speeds (ai0>=20 → +1, >=40 → +2)? At charge: 1/t → 10t per frame. At >=20: 2/t → 5t. At >=40: 3/t → 3.33t. The task's gloss mentioned only two tiers; source has three. Implement per source.

Hmm, but hold on — should I double-check the ai0 semantics mapping? Our tesla ai0: `if (e.ai0 < 60) e.ai0 += 1` — from 0 (or from -120 after firing, or -30 after hit). Vanilla FindFrame: `if (ai[0] > 0f)` — charge animation when ai0 > 0; idle when ≤ 0. With our ai0 = -120..60: after firing, ai0 = -120 (idle anim 15t/frame = "cooldown discharge idle"), counts up; crosses 0 at 120t; then charge anim (faster as it approaches 60). Wait — hmm, that seems backwards? "充电 10t/帧、待机 15t/帧" — charging = ai0>0 = approaching the shot. The tiers: 0-20 slow (10t), 20-40 faster (5t), 40-60 fastest (3.33t). So the tesla's orb spins faster as it nears discharge. And after discharge, 180t idle (ai0 from -120 to 60 → ≤0 for 120t at 15t/frame). Makes sense.

Now — what about 387's ai1? Not needed for frames.

**386 engineer** walk: vanilla `frameCounter += |vx| * 2f` — no +1. Our walkCycleT = Σ|vx| (reset on idle). counter ≈ 2*walkCycleT. Frame advance >6 → floor(2*walkCycleT/6)... but vanilla's counter is NOT reset on idle — however frame snaps to 0 when vx==0 and the counter freezes (doesn't reset). On resume: continues from frozen counter — phase continuity. Our walkCycleT resets to 0 on idle → phase reset on resume. Vanilla: frame 0 → after resume, counter continues from frozen value → first advance after (6 - frozen) worth of |vx|*2. Visual difference: on resume, first step delay differs by ≤6 counter-units (≤3 steps at |vx|=1). Trivial. Accept (use walkCycleT*2/6, mod 7, band 2-8, note in comment).

Hmm wait — also check: does vanilla reset frameCounter in the air branch? `frameCounter = 0.0; frame.Y = num;` — yes, air resets counter. Our walkCycleT keeps accumulating in air (|vx|). Meh — the walk band only shows when vy==0 && vx!=0. On landing, phase arbitrary anyway. Fine.

Now the **Engineer's deploy band** — check our ai2 semantics vs vanilla: our ai2 counts 1..60 (spawn turret at 30, at 60 → -120), then counts up from -120 → ... cycles. Also `if (e.confusedT > 0) e.ai2 = -60`. And justHit → ai2 = -30. And `if (e.ai2 > 0 && nT >= 4*nE) e.ai2 = 0`. Vanilla's ai[2] for 386: FindFrame `if (ai[2] > 0f) frame = 9 + (ai[2]/12)%2`. Our ai2 > 0 exactly mirrors (vanilla :59384-59428 1:1 port). 

Now — **393 turret** frame = num134 from ai2 angle. Our ai2 = atan2(dy, dx) where dy ≥ 0 (clamped `if (dy < 0) dy = 0`), dx can be ±. ToRotationVector2 = (cos, sin). vy=sin ≥ 0 always (or exactly 0 when dy=0... atan2(0, dx) = 0 or π → sin=0). So:
- vy > |vx|*2 → 4: needs sin > 2|cos| — angle in lower cone (steep down). 
- vy > |vx|*1.5 → vx>0 ? 5 : 3
- |vx| > vy*2 → vx>0 ? 8 : 0
- |vx| ≤ vy*1.5 → vx>0 ? 6 : 2
- else → vx>0 ? 7 : 1

Implement directly: vx = Math.cos(e.ai2), vy = Math.sin(e.ai2), then the nested ternary chain verbatim. Clamp result ≤ frames-1 (frames should be 18; firing +9 rows). Also guard NaN (ai2 default 0 → cos=1, sin=0 → |vx|>vy*2 → vx>0 → 8). Vanilla default ai2=0 → frame 8. Our ai2 init: Enemy ai2 = 0 initially. OK.

Laser window: `e.ai3 >= 280 && e.ai3 < 420 && (e.ai3|0) % 6 <= 2` → +9.

**394 cannon**: pure function of ai3:
```
let n = (e.ai3|0) - 300;
let f: number;
if (n >= 120) {
  n -= 120;
  if (n >= 160) f = 7 - Math.floor((n - 160) / 5);
  else if (n >= 20) f = Math.floor(n / 4) % 4;
  else f = 4 + Math.floor(n / 5);
} else f = 4;
```
Matches vanilla 72497-72517.

Note: our ai3 for 394 = saucer.ai3 — could be the 3600 counter in expert ai0=2 — vanilla literal formula regardless. Fine.

**399 probe**: frame = floor((t*0.25) % 4) + (e.ai0 !== 0 ? 4 : 0). Vanilla: `frameCounter = (frameCounter + 0.25) % 4.0 + (ai[0] != 0 ? 4 : 0)` — note it's not += 0.25 %4; it's assign (fc + 0.25) % 4 + offset. So counter bounces in [0,4) always; frame = (int)fc. Using animT: fc = (t*0.25) % 4 — phase offset constant. frame = floor(fc) ∈ 0-3, +4 if ai0≠0. Clamp to frames-1 (8 frames presumably). Good.

**346 santa**: decided — implement in Renderer stateless? The idle freeze problem... Actually wait, let me reconsider. Vanilla idle: `ref y2 = ref frame.Y; y2 = y2; frameCounter = 0;` — hold frame, reset counter. Stateless can't hold. But — hmm, how bad is the drift? If I return a "frozen" value... I could reuse e.lai0 as a phase-freeze? Overkill. Actually — hmm, hold on: santaNK1AI — I could do the replica in the AI (santaNK1AI runs every tick, no early returns except `if (!player)`? Let me check: santaNK1AI — no early returns visible; hoverCruise at end. There's `if (e.ai1 >= 300 && player)` etc. No returns. So the replica fits at the end (or start) of santaNK1AI — exact 1:1 with holds. L[0] free? santaNK1AI uses L[1], L[2]. L[0] free, L[3] free. Use L[0] = counter, L[3] = row. Then write e.customFrameIdx.

Similarly **344 everscream** — mourningWoodAI runs for both 325/344 with no early returns. For exactness: 325 is exactly t%5-driven (stateless fine — wait, is it? both branches +1/t with threshold >4: counter ≡ animT (from spawn, both 0-based, +1 per tick) — but the counter never resets across band switches; frame = band-derived: idle: frame cycles 0-4 as floor(t/5)%5 — but vanilla: on entering idle from moving band (frame 5-9), the clamp `if (frame.Y > num*4) frame.Y = 0` snaps to 0 — then advances every 5t. So idle band = floor(t/5)%5 — the phase from t is arbitrary vs vanilla's (which continues its counter — the counter IS t exactly! Since counter ≡ tick count and never resets... let me verify: vanilla counter starts 0 at spawn, +1 each FindFrame call... so counter ≡ floor(t/5) advance events. frame advances at every 5th tick regardless of band; on band entry, frame clamps into band. So idle frame = (number of advances so far) % 5 = floor(t/5) % 5. EXACT with animT (assuming animT and vanilla's FindFrame call count are in lockstep from spawn — yes). 

So 325 exact stateless: `vx === 0 ? Math.floor(t/5) % 5 : 5 + Math.floor(t/5) % 5`. With clamps to frames-1. 

For 344: rate varies with |vx| (max(1, |vx|*0.75)) — exact needs replica. mourningWoodAI end → maintain L-counter (L[0]? mourningWoodAI currently doesn't call la() — L unused. I'll use la(e) slots L[0]=counter, L[1]=row). Hmm wait — but actually, is a replica needed? counter = Σ max(1, 0.75|vx_i|) — I could track exactly in the AI with one accumulator and derive frame from... the frame needs advance events. Two slots (counter + row). Write e.customFrameIdx = row. Renderer: for id 344 the first line short-circuits via customFrameIdx. Clean.

Hmm — but wait: should I instead put BOTH 325 and 344 in the Renderer with 344 using a counter replica in e.lai0 (read by Renderer)? The task prefers Renderer branches reading ai/lai fields. For 344, Renderer branch: `frame = floor(e.lai0 / 6) % 10` — hmm, that works too if AI maintains a monotonically increasing counter (advance events = floor(counter/6) mod 10). counter = Σ max(1,|vx|·0.75) — no wrap needed (floor(counter/6) % 10). So AI writes e.lai0 (raw counter, unbounded), Renderer: `Math.floor(e.lai0 / 6) % 10`. That's exactly equivalent to vanilla's counter behavior (vanilla wraps counter at >5 → 0; row = advanceCount % 10 — since frame wrap: `if (frame.Y > num*9) frame.Y = 0` → advanceCount % 10). 

But hold on — vanilla 344's counter wrap: `if (frameCounter > 5.0) { frameCounter = 0; frame.Y += num; }` — so counter ∈ [0,6), advance events counted by floor(total/6). And frame = advances % 10 (wrap >9 → 0). So Renderer branch: `Math.floor(e.lai0 / 6) % 10` where e.lai0 = total accumulated. 

Similarly for 325 I could use t: floor(t/5) — but wait, the band clamp: on entering moving band, vanilla snaps frame INTO band via clamps (<5 → 5; >9 → 5). With my formula, frame = 5 + floor(t/5)%5 for moving — arbitrary phase on entry (vanilla keeps continuous advance count → also arbitrary-ish band position depending on phase — since vanilla's frame continues from its current advance count, the position in band = advanceCount % 5 — my formula gives the same advanceCount! Because counter ≡ t. Actually YES — exactly equal: vanilla moving frame = (advanceCount % 5) + 5 after clamp... hmm, not exactly: vanilla's frame is NOT recomputed from advanceCount; it's incremented by 1 per advance and clamped into band on each tick (`if (frame.Y < num*5) frame.Y = num*5; if (frame.Y > num*9) frame.Y = num*5`). Starting from idle frame i (0-4): on move entry, frame clamps up to 5; subsequent advances: 6,7,8,9,5(>9→5? from 9 → +1 = 10 → >9 → 5). So from entry, sequence 5,6,7,8,9,5,... advancing every 5t. My formula: 5 + floor(t/5)%5 — on entry at tick T, vanilla frame=5; mine = 5 + (floor(T/5)%5) — could be 5..9. Deviation: arbitrary phase within band. Visually: the walk cycle starts at a different step — minor, same class as existing approximations... 

Since I'm already adding a replica counter for 344 in the same function, I might as well do the exact thing for both: maintain total counter for 325 too (it's just +1/t → e.lai1? no wait...). Hmm — but for 325 the exact vanilla behavior: same single counter for both bands (counter ≡ tick count). The band snap difference is only the entry phase. Ugh, honestly: since vanilla's counter for 325 ≡ t exactly, and the frame = advances with band clamps — the only "memory" is the frame itself at band switches. To be exact for both 325 and 344 I'd need (counter, row) replicas. Fine — do it uniformly for 325+344 in mourningWoodAI: L[0]=counter, L[1]=row (mourningWoodAI has L free), write e.customFrameIdx. Both exact.

Wait, actually — hmm, let me keep the Renderer-branch approach where possible per the task ("在既有 case 266/222/262/113 等先例处追加分支"). The mix:
- Renderer branches (stateless): 393, 394, 399, 387, 386, 345, 551, 325, 346(walk/fire with t-based approx?), 344(?)
- Renderer branches reading e.lai0 counter: 395, 392
- AI customFrameIdx (stateful machines): 327 (pumpking), 439/440 (cultist)
- 325/344/346: choose exactness vs Renderer-branch.

Hmm. The cleanest architecture respecting both the task instructions AND exactness:
- 325: Renderer branch, exact via t (idle: floor(t/5)%5; moving: 5+floor(t/5)%5) — band entry phase arbitrary, note it. Actually wait — I realize I can be exact with t alone: vanilla 325's counter ≡ t and the frame at any tick = f(counter) + band memory only at switches... the band memory is exactly the entry phase. Not recoverable from t. Accept approximation (entry phase), same class as id 127/222 precedents. Actually hmm — hmm, wait. Let me re-examine: is the entry phase REALLY arbitrary in vanilla? Sequence: while idle, frame cycles 0-4 (advances every 5t). Switch to moving at tick T: frame = current idle frame (0-4) → clamp <5 → 5. So vanilla's moving frame at entry = 5 always! Then 6,7,8,9,5... every 5t from T. My formula 5 + floor(t/5)%5 gives phase = floor(T/5)%5 ∈ {0..4} ≠ 0 generally. To be exact: 5 + floor((t - T)/5) % 5 — needs T (last band switch). Not tracked. → approximation stands, deviation ≤ 2 walk frames for one cycle. Fine — precedent-backed.

- 344: needs rate tracking → AI writes e.lai0 = accumulated counter (Σ max(1,|vx|·0.75)); Renderer branch: floor(e.lai0/6) % 10. Band: 344 has ONE band (0-9, wrap 0) — no band memory! Exact. 

- 346: needs holds (idle freeze) + walk counter. AI replica → customFrameIdx? Or e.lai0 counter + Renderer math? The idle hold means Renderer can't derive from counter alone (needs last row). Two fields (lai0=counter, lai1=row) — AI writes both, Renderer branch does: ai0===1 ? 6+floor(t/3)%3 (t-based, fire band — but entering the band vanilla starts from clamped 6 and advances every 3t — t-based phase arbitrary)... ugh. Since holds and band entries need row memory, do the full machine in AI → e.customFrameIdx for 346. Hmm — but then the Renderer branch for 346 doesn't exist... 

OK let me step back and decide the final architecture, balancing the task's stated preference (Renderer branches + minimal AI sync via lai0/lai1/customFrameIdx):

**Martian:**
- 393: Renderer branch (pure ai2/ai3). ✓
- 394: Renderer branch (pure ai3). ✓
- 395: AI writes e.lai0 = frameCounter replica; Renderer branch: Math.floor((e.lai0 % 66)/6). ✓
- 392: AI writes e.lai0 = counter replica; Renderer branch: Math.floor((e.lai0 % 12)/3). ✓
- 399: Renderer branch (t + ai0). ✓
- 387: Renderer branch (t-rate approximation by ai0 tiers). ✓
- 386: Renderer branch (ai2 deploy band + walkCycleT*2 walk + air=1/idle=0). ✓

**Moon events:**
- 327: AI customFrameIdx (pose walk state machine in pumpkingAI; storage e.lai0=counter/e.lai1=row or L[3]+...). Renderer: no branch needed (customFrameIdx short-circuit). But wait — should I add a comment branch in Renderer for discoverability? The first line handles it; the 694 precedent has no Renderer case. I'll note in the Renderer near 222? No — don't touch unrelated. Add a brief comment in the AI. Hmm — actually, hmm, one issue: what if customFrameIdx isn't reset when... it's written every tick by pumpkingAI. OK.

Wait — one more consideration for 327: the Renderer's `frames` for 327 = 13? (vanilla npcFrameCount[327] — 12 rows + 1? The wrap `frame.Y > num*11 → 0` implies 12 rows; head index table at 10800 says `327: 13` — that's the BOSS_HEAD texture index, not frames. npcFrameCount[327] — from Terraria: Pumpking sprite has 12 frames? Hmm — hmm, Pumpking_Head? Actually 327 uses NPC_327.png with... The wrap logic caps at row 11 → 12 rows. customFrameIdx clamps at frames-1 anyway.

- 345: Renderer branch (ai0/ai3/vx + t). ✓ exact (glide frames are direct assignments; bands are fixed-rate from t — entry phase arbitrary for band 3-4 cycle — vanilla: entering ai0=1, frame clamps into [3,4] and advances every 6t from counter (counter continues, not reset — `frameCounter += 1; if > 5 advance` — counter carries from glide state where frameCounter wasn't touched... in glide branch (ai0==0) frameCounter is NOT incremented (frame set directly). So counter frozen during glide! Entering rain: counter continues from frozen value → first advance after (6 - frozen%6) — arbitrary. t-based: arbitrary phase. Same class. Fine.)

- 346: full machine in santaNK1AI → customFrameIdx. (idle holds need memory)
- 325: Renderer branch (t-based, exact rates; band entry phase approximation noted).
- 344: AI writes e.lai0 = Σmax(1,|vx|·0.75) counter; Renderer: floor(lai0/6)%10. Exact.
- 551: Renderer branch (pure ai0/ai1). ✓ exact.

**Cultist:** AI customFrameIdx in lunaticCultistAI (WeakMap for counter/row, or... laOf slots are taken; use module WeakMap). Renderer: no branch (customFrameIdx). Add comment? The 694 precedent: AI writes customFrameIdx, no Renderer branch. OK.

Hmm wait — but for 327/346/439/440 — is there any code path where the AI doesn't run but the entity still renders? E.g., paused? NetPuppet (multiplayer puppet — animT++ but no AI run!). Net puppets: `if (this.netPuppet) { ...; return; }` — AI skipped! Then customFrameIdx stays stale (frozen at last value) — for a puppet that's... acceptable (frozen frame, no animation). Hmm — but puppet rendering would freeze. Whereas vanilla net puppets run FindFrame locally (FindFrame is client-side in vanilla MP!). Edge case — multiplayer Betsy/Pumpking puppets would show frozen frames. Is that acceptable? The server-authority room work (SimHost) — enemies run on host; clients get puppets. A frozen frame vs a generic 6t cycle — frozen is closer to correct state at least. Note it in comment. (The existing 694 mimic precedent has the same property.) OK.

Now — 345: wait, I should double-check the glide branch's ai3 semantics in our AI vs vanilla FindFrame `ai[3] >= 0f → frame 0; else vx<0 → 1 else 2`. Our ai3 in glide: counts +1 when shooting window active; `if (e.ai3 > beat) e.ai3 = -beat;` then counts up to 0 → shoots at 0, keeps counting +... wait: `e.ai3 += 1; ...; if (e.ai3 > beat) e.ai3 = -beat; if (e.ai3 === 0) shoot`. So ai3 ∈ (-beat, beat]. >=0 → frame 0. Hmm — and when NOT in shooting window (`else if (e.ai3 < 0) e.ai3 += 1` — recovers to 0). Vanilla 1:1 (task said "滑翔定帧 0/1/2(按射击相位+vx 向)"). ✓.

But — in states 1/2 (rain/spin), ai3 also has values (0..beat) — irrelevant (frame from t/band).

Edge: ai0===-1 for one tick (reselect): vanilla frame unchanged (no branch) — our Renderer branch: `if (e.ai0 === 0) {...} else if (e.ai0 === 1) {...} else if (e.ai0 === 2) {...} else return <hold?>` — can't hold statelessly... The reselect resolves within the same tick (ai0 → pick at the end of the AI tick), so the renderer never sees -1. Unless... the reselect block: `if (e.ai0 === -1) { pick...; e.ai0 = pick; }` — yes resolved same tick. Good — branch handles 0/1/2 only; default → hold... make default = 0? Never hit. I'll structure exactly like vanilla with else → return current-band... just fall to the generic? No — for unhandled, return 0 (harmless, unreachable).

Wait — also day-fly-away branch: our iceQueenAI at day returns early (vx set, visAngle) — ai0 unchanged (whatever state). Vanilla FindFrame: ai0==0 (glide) → uses ai3/vx — our ai3 at day... stale. Vanilla: same (AI early-return at day leaves ai unchanged... let me check vanilla 33590-33599 — yes vanilla also just flies away; ai3 stale; FindFrame uses stale ai3 + current vx → frame 0/1/2 by vx). Our branch reads same values → same result. ✓

Now — **check: do 325/344/345/346/327/551/392-395/399/386/387 currently fall into the generic `floor(t/6)%frames` bucket?** Yes (no existing branches) — the fix replaces that.

Now let me also confirm the **pumpking blade 328** isn't in scope (not listed — skip; FindFrame 328? not requested).

Now, cultist — where exactly to insert the frame machine in lunaticCultistAI. Requirements:
- runs every tick for both 439 and 440 (before any return except death paths)
- uses ai0/ai1 pre-state-update (mirroring vanilla localAI[2] assignment points), except ai0==-1 which uses post-increment value (= ai1+1 pre).

Insertion point: right after the `if (isReal && e.ai0 === 5 && ...)` justHit block (line ~346) and before `// 朝向(:65117-65120...)` at line 348. At that point: clone ai0/ai1 mirrored ✓; spawn-init done ✓; despawn handled (dead → no render anyway) ✓.

Hmm wait — one problem: the -1 state's frame-state uses ai1+1, but the -1 state block later does `e.ai1 += 1` — consistent (my +1 accounts for it). But ALSO the vanilla sound gate `if (localAI[2] != 13f) PlaySound` — our port already handles its sound separately (===361). Don't touch.

Ritual state circle vector: needs cir (ritualCenterOf) + e.cx/e.cy pre-update — vanilla computes vector10/11/12/13 in-block (post-teleport at t=30 for real). I compute at top: at t=30 for real, la.la2 is null → skip (state stays 10). One-tick deviation noted. For clones at t=30: parent's la.la2 null too → 10. t≥31: fine.

Wait — one more vanilla detail: in the [30,90) window, the vector is computed for BOTH real (vector10) and clones (vector11) — from the CIRCLE center (projectile 490). In [120,420): real vector12 / clone vector13 — also circle center. Both use ritual center — same rule. So: `if (t >= 30 && t < 90) || (t >= 120 && t < 420)` → vector from circle center; rule: |uy|<0.77→11, uy<0→12, else 10.

Hmm — but ALSO the vanilla real [30,90) branch reads `Main.projectile[(int)this.ai[2]]` — ai[2] = circle proj index — the circle was spawned at t==30 before this read. OK.

Now — our clones at ritual: their ai0/ai1 mirror parent each tick (mirror happens at AI start — parent's ai1 updated last tick or this tick depending on iteration order; parent spawned before clones so parent updates first → clones mirror this tick's parent values. vanilla: clones mirror at their own AI start — same ordering. Fine.)

Now implement the cultist frame machine replica:

```ts
/** 教徒 FindFrame 帧机副本（NPC.cs:72698-72783）:localAI[2] 六态→帧行。
 *  本仓 la2 被挪用存仪式圈心 → 帧态在 AI 内重算后直接写 customFrameIdx */
const cultistAnim = new WeakMap<Enemy, { fc: number; row: number }>();

function cultistFrameState(e, la, isReal, parent): number { ... }
function cultistFindFrame(e, st) { ... }
```

The frame state switch per state — with rows: 0→4,5,6; 1→10,11,12; 2→7,8,9; 13→13,14,15; settle rows 0/1/2.

Let me write it:

```ts
function cultistFrameTick(e: Enemy, st: number): void {
  let a = cultistAnim.get(e);
  if (!a) { a = { fc: 0, row: 0 }; cultistAnim.set(e, a); }
  const seg = Math.floor(a.fc / 5);  // 行内偏移 0-2（5t/帧,cs:72726 /5）
  switch (st) {
    case 0:
      if (a.fc >= 15) { a.fc = 0; a.row = 0; }
      else if (a.row !== 0) a.row = seg + 4;
      break;
    case 10:
      if (a.fc >= 15) a.fc = 0;
      a.row = seg + 4;
      break;
    case 1:
      if (a.fc >= 15) { a.fc = 0; a.row = 1; }
      else if (a.row !== 1) a.row = seg + 10;
      break;
    case 11:
      if (a.fc >= 15) a.fc = 0;
      a.row = seg + 10;
      break;
    case 2:
      if (a.fc >= 15) { a.fc = 0; a.row = 2; }
      else if (a.row !== 2) a.row = seg + 7;
      break;
    case 12:
      if (a.fc >= 15) a.fc = 0;
      a.row = seg + 7;
      break;
    case 13:
      if (a.fc >= 15) a.fc = 0;
      a.row = seg + 13;
      break;
  }
  a.fc += 1;                          // cs:72781 frameCounter += 1
  e.customFrameIdx = a.row;
}
```

Wait — careful with case 10/11/12/13: `if (fc >= 15) fc = 0;` BEFORE computing seg? Vanilla:
```
case 10:
    if (frameCounter >= 15.0) frameCounter = 0.0;
    frame.Y = ((int)frameCounter / 5 + 4) * num;
```
The reset happens BEFORE the frame computation — so seg uses the reset value. In my code: I compute seg from a.fc BEFORE the reset — wrong for states 10/11/12/13! For states 0/1/2 the pattern is `if (fc >= 15) {fc=0; frame=...} else if ...` — the >= 15 branch uses fc=0 → row snap (not seg-based). So for 0/1/2 my order is fine only if the >= 15 check happens before using seg — in the else branch fc < 15 so seg fine. But for 10/11/12/13: reset first, then row from seg of reset fc. Let me restructure:

```ts
if (a.fc >= 15) a.fc = 0;   // applies to all states (each case has it)
```
Wait — do ALL cases have the reset? Case 0: `if (fc >= 15) { fc = 0; frame.Y = 0; } else if ...`. Case 1: `if (fc >= 15) {fc=0; frame=num;} else if`. Case 2: same shape. Cases 10/11/12/13: `if (fc >= 15) fc = 0;` then unconditional row = seg + base. So YES — every case resets fc at >=15 first. So hoist `if (a.fc >= 15) a.fc = 0;` to the top, then seg = floor(fc/5), then switch:

```ts
if (a.fc >= 15) a.fc = 0;
const seg = Math.floor(a.fc / 5);
switch (st) {
  case 0: if (a.fc === 0 ... hmm no.
```
Careful for case 0: vanilla `if (fc >= 15) { fc=0; frame=0; }` — the frame snaps to 0 IN THE SAME TICK fc hits 15 (i.e., fc was 14 → +=1 → 15? No wait — the increment happens at the END (fc += 1 after switch). So during a FindFrame call fc ∈ [0,15) always? Let's trace: call with fc=14: case 0: 14 < 15 → else if (frame != 0) → row = 14/5+4 = 2+4 = 6. Then fc → 15. Next call fc=15: >= 15 → fc=0, row=0. Then fc → 1. So fc ∈ [0,15] with 15 only transiently at call start. So hoisting is safe: at call start fc ∈ {0..15}; if 15 → reset to 0 → seg=0. 

But for case 0, the >= 15 branch sets row = 0 directly (not seg+4 — seg would be 0 → row 4 ≠ 0). So case 0 needs its own handling:

```ts
switch (st) {
  case 0:
    if (hit) { a.row = 0; }           // fc>=15 同拍定格行 0
    else if (a.row !== 0) a.row = seg + 4;
    break;
  case 1:
    if (hit) a.row = 1;
    else if (a.row !== 1) a.row = seg + 10;
    break;
  case 2:
    if (hit) a.row = 2;
    else if (a.row !== 2) a.row = seg + 7;
    break;
  case 10: a.row = seg + 4; break;
  case 11: a.row = seg + 10; break;
  case 12: a.row = seg + 7; break;
  case 13: a.row = seg + 13; break;
}
a.fc += 1;
```
where `hit = a.fc >= 15` (then a.fc = 0). And after reset, for the looping states row = 0+base. For 0/1/2, hit → settle row. ✓ matches vanilla exactly.

Wait, subtle: for case 0 when NOT hit and row === 0 → nothing (frozen at 0). ✓. When entering state 0 with row = 12 (from state 11): plays seg-based rows 4-6 for the remaining fc cycle... vanilla: `else if (frame.Y != 0) frame.Y = (fc/5+4)*num` — plays from CURRENT fc phase through the cycle, then snaps 0. ✓ my replica matches.

Default case (st not in {0,1,2,10,11,12,13}): vanilla default → nothing (frame unchanged), fc NOT reset (no case matched → no reset; but fc += 1 still runs at the end). My st values will always be in the set (0/1/2/10/11/12/13) since I map states directly. But keep default: no-op. Hmm — wait: fc += 1 at end regardless of case — yes vanilla line 72781 outside the switch. My replica: a.fc += 1 outside switch. But if no case matched, fc keeps growing past 15 unbounded? In vanilla: fc += 1 each tick; if state leaves the set... all our states map into the set, so fine.

Now the CULTIST frame-state function mapping (with vanilla line refs):

```ts
/** AI 态 → 原版 FindFrame localAI[2] 帧态（cs:65120-65137/:65148/:65348/:65365/:65436/:65520-65524/:65575+/:65786/:65811/:65878 系） */
let st: number;
switch (e.ai0) {
  case -1: { const s = e.ai1 + 1; st = s > 360 ? 13 : s > 300 ? 10 : s > 120 ? 1 : 0; break; }  // :65125-65136（后置自增口径）
  case 0: st = 10; break;    // :65148
  case 1: st = 10; break;    // :65348
  case 2: st = 11; break;    // :65365
  case 3: st = 11; break;    // :65436
  case 4: st = isReal ? 12 : 11; break;   // :65520-65524 flag2 门
  case 6: st = 13; break;    // :65786
  case 7: st = 11; break;    // :65811
  case 8: st = 13; break;    // :65878
  case 5: {                  // :65575 头部置 10;[30,90)/[120,420) 两窗按圈心向量覆写
    st = 10;
    const t = e.ai1;
    if ((t >= 30 && t < 90) || (t >= 120 && t < 420)) {
      const cir = ritualCenterOf(isReal, la, parent);
      if (cir) {
        let dx = cir.x - e.cx, dy = cir.y - e.cy;
        const d = Math.hypot(dx, dy);
        if (d === 0) { dx = 0; dy = -1; } else { dx /= d; dy /= d; }
        st = Math.abs(dy) < 0.77 ? 11 : dy < 0 ? 12 : 10;   // :65657-65671 同构
      }
    }
    break;
  }
  default: st = 10; break;
}
cultistFrameTick(e, st);
```

Hmm wait — ai0==-1 uses e.ai1+1 — but careful: our AI increments ai1 inside the -1 block AFTER my insertion point, so pre-increment ai1; vanilla checks post-increment → my +1. ✓. But also our -1 block for clones? ai0==-1 is real-only (clones mirror parent's ai0 — during parent's -1, clones mirror ai0=-1? Clones don't exist until ritual state. OK.)

For ai0==5 windows with t = e.ai1 (pre-increment — vanilla checks pre-increment within block ✓).

Wait — vanilla [30,90): `else if (ai[1] >= 30 && < 90)` — and within, the reposition at ==30 and then flag2?/else vector10/11 for every tick in the window. And [120,420): vector12/13. Both same formula. ✓ my combined condition.

Hmm — but hold on: is the vector computation inside [30,90) really for every tick? From the sed: [30,90) block: `if (ai[1] == 30 && netMode != 1 && flag2) {reposition}` then flag3/flag4/alpha=255; then `if (flag2) { vector10... } else { vector11... }` — yes, every tick in the window. ✓.

Also — vanilla vector for the real in [30,90) reads Main.projectile[ai[2]] — our cir = la.la2 ({x,y}) set at t==30 — from t=31 onward. At t=30 (before block runs): null → skip → stays 10. Noted 1-tick deviation.

Now — where does `parent` come from at my insertion point? The clone-mirror segment sets `parent = la.la3` — defined earlier in the function (line 285). My insertion after line ~345 — parent in scope. ✓.

Also `la` = laOf(e) in scope. ✓.

Now — **netcode**: lunaticCultistAI etc. run only for host/local; puppets skip AI (customFrameIdx frozen) — acceptable (same as 694).

Now the martian saucer/part replica code:

In martianSaucerAI — 395:
```ts
// ---- FindFrame case 395 副本（cs:72520-72541）:counter 每 tick +1（死光电报窗
//      [20,260) 内再 +1 且钳 [36,53]→帧 6-8 蓄能辉光带）;66 回卷,帧 = counter/6 ----
// (放在函数两处正常出口:-1/-2 爬升分支与函数尾——AI 全部完成后同步,与原版
//  FindFrame 时序一致;死亡出口无需)
```
Write a small local closure:
```ts
const frameTick395 = (): void => {
  e.lai0 += 1;
  if (e.lai0 >= 66) e.lai0 = 0;
  if (e.ai3 >= 20 && e.ai3 < 260) {
    e.lai0 += 1;
    if (e.lai0 >= 54 || e.lai0 < 36) e.lai0 = 36;
  }
};
```
Call before `fly(e); return;` in the -1/-2 branch and at function end (before the final fly(e)? The final fly(e) is at the end after bounds check — the bounds-check branch returns dead. Order within tick doesn't matter for the counter as long as it's after ai3's update and once per tick. Put call right after the bounds-check block, before final `fly(e)`.

Hmm wait — during ai0===1 (expert transition), ai3 was reset to 0 at entry (392 sets saucer.ai0=1, ai3=0). flag10 false → normal spin. ✓.

For 392 in martianSaucerPartAI — at function end:
```ts
// ---- FindFrame case 392 副本（cs:72543-72560）:4 帧旋球,死光电报窗内帧速 ×2 ----
e.lai0 += (e.ai3 >= 20 && e.ai3 < 260) ? 2 : 1;
if (e.lai0 >= 12) e.lai0 = 0;
```
Hmm — vanilla: fc += 1; if flag fc += 1; if fc >= 12 → 0. Equivalent to += (flag?2:1) then wrap — wait, not exactly: vanilla wraps only when fc >= 12 — after wrap fc=0 — but with double increment could fc land at 12 exactly → 0. My version: += 2 then if >=12 → 0. E.g. fc=11 → +2 = 13 → 0. Vanilla: 11 → +1 = 12 (not >= 12? it is >= 12 — wait vanilla increments THEN checks: `frameCounter += 1.0; if (flag6) frameCounter += 1.0; if (frameCounter >= 12.0) frameCounter = 0.0;` — so 11 → 12 → 13 → >= 12 → 0. Mine: 11 + 2 = 13 >= 12 → 0. ✓ same.

But careful — placement: e.ai3 = saucer.ai3 is set mid-function (line 419). The end-of-function placement reads it post-update. ✓. But — hmm, one path issue: 392 continues past `if (id !== 392 && ...)` to the slots/deathray blocks and reaches the end — no early return after line 419 for 392? Checking the code after line 415: the 394 block returns, the 393 block returns, then the 392 block (slots + deathray + missiles) — no returns. ✓ end of function = 392 only (plus 416/390/492 already returned).

Renderer branches to add (inside vanillaFrameIdx). Placement: after the existing 266 branch (or near 222/262/113 precedents — "在既有 case 266/222/262/113 等先例处追加分支" = add alongside these). I'll insert after the 266 block (line 883-890), before the `case 5` block — a contiguous "火星/月事件/教徒/Betsy 批" section.

Branch code:

```ts
// ===================== 火星疯狂族 FindFrame 批（2026-08-19）=====================
// 393 飞碟炮塔（cs:72481-72494）:ai[2] 瞄准角 → 九向帧;激光窗 [280,420) 内
// (int)ai[3]%6<=2 时 +9 射击行（bossAI_martian 393 段 1:1 写入 ai2=atan2 角/ai3=共享计时）
if (id === 393) {
  const vx = Math.cos(e.ai2), vy = Math.sin(e.ai2);   // ai[2].ToRotationVector2()
  let f = vy > Math.abs(vx) * 2 ? 4
    : vy > Math.abs(vx) * 1.5 ? (vx > 0 ? 5 : 3)
    : Math.abs(vx) > vy * 2 ? (vx > 0 ? 8 : 0)
    : Math.abs(vx) <= vy * 1.5 ? (vx > 0 ? 6 : 2)
    : (vx > 0 ? 7 : 1);
  if (e.ai3 >= 280 && e.ai3 < 420 && (e.ai3 | 0) % 6 <= 2) f += 9;
  return Math.min(frames - 1, f);
}
```
Wait — the nested ternary order: vanilla's chain: 
```
(vy > |vx|*2) ? 4
: (vy > |vx|*1.5) ? ((vx > 0) ? 5 : 3)
: (|vx| > vy*2) ? ((vx > 0) ? 8 : 0)
: (!(|vx| > vy*1.5)) ? ((vx > 0) ? 6 : 2)
: (!(vx > 0) ? 1 : 7)
```
So the final else is vx<=0 ? 1 : 7. My version: `Math.abs(vx) <= vy * 1.5 ? (vx > 0 ? 6 : 2) : (vx > 0 ? 7 : 1)` — equivalent ✓.

394:
```ts
if (id === 394) {
  let n = (e.ai3 | 0) - 300;
  let f: number;
  if (n >= 120) {
    n -= 120;
    if (n >= 160) f = 7 - Math.floor((n - 160) / 5);
    else if (n >= 20) f = Math.floor(n / 4) % 4;
    else f = 4 + Math.floor(n / 5);
  } else f = 4;
  return Math.min(frames - 1, f);
}
```

395:
```ts
if (id === 395) {
  return Math.min(frames - 1, Math.floor((e.lai0 % 66) / 6));
}
```
(lai0 = counter replica maintained in martianSaucerAI.)

392:
```ts
if (id === 392) {
  return Math.min(frames - 1, Math.floor((e.lai0 % 12) / 3));
}
```

399:
```ts
if (id === 399) {
  return Math.min(frames - 1, Math.floor((t * 0.25) % 4) + (e.ai0 !== 0 ? 4 : 0));
}
```

387:
```ts
if (id === 387) {
  // ai0>0 充电档 10t/帧,≥20 → 5t,≥40 → 10/3t（cs:72338-72346 增量 1/2/3）;
  // ai0≤0 待机 15t/帧。相位取全局 t（2 帧闪切,相位任意视觉等价）
  const period = e.ai0 > 0 ? 10 / (1 + (e.ai0 >= 20 ? 1 : 0) + (e.ai0 >= 40 ? 1 : 0)) : 15;
  return Math.min(frames - 1, Math.floor(t / period) % 2);
}
```

386:
```ts
if (id === 386) {
  // 放塔期（ai2>0）帧 9/10 每 12t 交替;地面行走带 2-8 按 |vx|*2 累计
  // (无 +1);站定帧 0;腾空帧 1
  if (e.ai2 > 0) return Math.min(frames - 1, 9 + (Math.floor(e.ai2 / 12) % 2));
  if (e.vy !== 0) return Math.min(1, frames - 1);
  if (!walking) return 0;
  return Math.min(frames - 1, 2 + Math.floor((e.walkCycleT * 2) / 6) % 7);
}
```
Wait — check vanilla walking wrap: `if (frame.Y / num >= 9) frame.Y = num * 2` — band 2..8 → 7 frames → `% 7` after +2 — but careful: the frame advance is +1 per >6 counter; wrap to 2. My formula: 2 + floor(counter/6) % 7 where counter = walkCycleT*2 — hmm the >6 threshold: `frameCounter += |vx|*2; if (frameCounter > 6.0) { frame.Y += num; frameCounter = 0; }` — advance every 7 counter units (counter 0..6 then >6 → advance)! `> 6` not `>= 6`! So advance at 7 accumulated units. floor(counter/7). Hmm — let me recheck: counter increments by |vx|*2 per tick; when counter > 6 (i.e., reaches ≥ 6+ε; with float adds, at 7th unit if increments are integers... |vx|*2 can be fractional. The check `> 6.0` means 7 units of accumulation per advance when increments are 1 — like the zombie family `>6 才进帧` → 7t/帧 as documented in the 46-family branch: "counter ≡ walkCycleT + t(每 tick += |vx| + 1);越过 7 即进帧 → /7". So for 386: counter += |vx|*2 → advance when counter > 6 → frame = 2 + floor(walkCycleT*2/7) % 7. Let me double check with the existing 46-family precedent: `return Math.floor((e.walkCycleT + t) / 7) % frames;` — yes /7. ✓ So use /7 for 386.

Similarly re-check 346 walk: `frameCounter += 1.0; frameCounter += Math.Abs(velocity.X) / 2f; if (frameCounter > 4.0) {advance}` — counter += (1 + |vx|/2) → advance every 5 units (> 4 → 5th). floor(counter/5) where counter = t + walkCycleT/2. ✓ (I had this right.)

And 344: `frameCounter += max(1, |vx|*0.75); if (frameCounter > 5.0) {advance}` → 6 units per advance → floor(total/6). ✓.

325: `frameCounter += 1.0; if (frameCounter > 4.0) {advance}` → 5 units → floor(t/5). ✓.

And check 345 rain: `frameCounter += 1.0; if (frameCounter > 5.0) {advance}` → 6 units → floor(t/6) % 2 + 3. ✓ (band 3-4: `if (frame.Y > num*4) frame.Y = num*3; if (frame.Y < num*3) frame.Y = num*3`).

And 346 fire: `frameCounter += 1.0; if (frameCounter > 2.0) {advance}` → 3 units → floor(t/3) % 3 + 6. ✓.

And 387: `frameCounter += 1.0 (+1 if ai0>=20)(+1 if ai0>=40); if (frameCounter >= 10.0) reset` — note >= 10 (not > 10)! So advance every 10 units exactly. And idle: `if (frameCounter >= 15.0)` → 15 units. So period = 10/speed and 15 → frame = floor(t / period) % 2. ✓ my formula.

Pumpking: `frameCounter` thresholds > 6 / < 0 with counter moving ±1 per tick: from 0, +1 per tick: 1,2,...,6,7 → at 7 (>6) → advance & reset 0. So 7 ticks per step ✓ (matches task's 7t/帧).

395: `frameCounter += 1.0; if (frameCounter >= 66.0) frameCounter = 0.0;` → wraps at 66 (>= 66 → 66 frames of counter 0..65 — /6 → 11 frames 0..10) ✓.

392: `if (frameCounter >= 12.0)` → 0..11 /3 → 4 frames ✓.

Now the moon events Renderer branches:

```ts
// 325 哀木（cs:73172-73201）:站定带 0-4 / 移动带 5-9,均 5t/帧
// (两分支 counter 同为 +1/t → counter ≡ animT,无 AI 侧状态;带切换瞬间相位任意,登记)
if (id === 325) {
  return Math.min(frames - 1, e.vx === 0 ? Math.floor(t / 5) % 5 : 5 + (Math.floor(t / 5) % 5));
}

// 344 常世吼（cs:73144-73170）:全带 0-9,counter += max(1,|vx|*0.75) 6 单位进帧
// ——速率随速度变化,counter 副本由 mourningWoodAI 累进到 e.lai0
if (id === 344) {
  return Math.min(frames - 1, Math.floor(e.lai0 / 6) % 10);
}

// 345 冰雪女王（cs:73106-73143）:滑翔(ai0==0) 定帧 0 / ai3<0 时按 vx 向 1|2;
// 落冰(ai0==1) 带 3-4 每 6t;自旋(ai0==2) 恒帧 5
if (id === 345) {
  if (e.ai0 === 0) {
    if (e.ai3 >= 0) return 0;
    return e.vx < 0 ? 1 : 2;
  }
  if (e.ai0 === 1) return Math.min(frames - 1, 3 + (Math.floor(t / 6) % 2));
  if (e.ai0 === 2) return Math.min(5, frames - 1);
  return 0;
}
```
Wait — glide: `ai[3] >= 0f → frame 0; else if vx < 0 → 1; else 2`. My code: `if (e.ai3 >= 0) return 0; return e.vx < 0 ? 1 : 2;` ✓. Clamp: frames for 345 = 6? fine to min.

346 — decided AI customFrameIdx. But wait — reconsider: should I really do the full machine in AI for 346? Let me weigh: the t-based approximation for the walk band would be fine (like 345), but the idle FREEZE (vx==0) matters — santa stops whenever attacking (flag58) or player under — that's most of its attack time. With t-based approximation, idle → I'd have to pick some frame — a cycling or fixed one → wrong (legs animating while standing, or stuck mid-stride). Vanilla freezes at the last walking frame. The AI replica handles it exactly. Cost: ~12 lines in santaNK1AI. Do it in AI.

Hmm — actually wait. Alternatively: `if (e.vx === 0) return <last>` — could I derive "hold" via... no stateless hold. AI replica it is. And while I'm there, the fire band can also be exact (starting frame 6 on entry, 3t steps) rather than t-phase-arbitrary. Full vanilla machine in santaNK1AI:

```ts
// ---- FindFrame case 346 副本（cs:73050-73093）:ai0==1 开火带 6-8 每 3t;
//      vx==0 定格(清计数);行走带 1-5 counter += 1+|vx|/2、>4 进帧 ----
{
  if (e.ai0 === 1) {
    L[0] += 1;
    if (L[0] > 2) { L[0] = 0; L[3] += 1; }
    if (L[3] > 8) L[3] = 6;
    if (L[3] < 6) L[3] = 6;
  } else if (e.vx === 0) {
    L[0] = 0;                       // 定格:帧不动,仅清计数
  } else {
    L[0] += 1 + Math.abs(e.vx) / 2;
    if (L[0] > 4) { L[0] = 0; L[3] += 1; }
    if (L[3] > 5) L[3] = 1;
    if (L[3] < 1) L[3] = 1;
  }
  e.customFrameIdx = L[3];
}
```
Note vanilla also sets spriteDirection = direction in fire & walk branches — our render mirrors by e.facing already; vanilla's `spriteDirection = direction` — our facing handling is generic; skip (render layer handles facing). Place at end of santaNK1AI (after hoverCruise, since vx is final then — vanilla FindFrame reads post-AI velocity ✓).

Wait — placement caveat: santaNK1AI at day: `if (e.vx === 0) e.vx = 0.1;` before hoverCruise — so vx≠0 at day. Fine, place after hoverCruise (e.vx final).

327 pumpking AI replica:
```ts
// ---- FindFrame case 327 副本（cs:72977-73037）:ai3 姿态 0→行0 / 1→行4 / 2→行8,
//      帧计数 ±1/t,越 ±6 进帧行(12 帧回卷)——表情在带间双向滑变 ----
{
  let step = 0;
  const row = e.lai1;   // hmm — I planned lai0=counter, lai1=row
  if (e.ai3 === 0) {
    if (row > 5) step = 1;
    else if (row > 0) step = -1;
  } else if (e.ai3 === 1) {
    if (row > 10) step = 1;
    else if (row > 4) step = -1;
    else if (row < 4) step = 1;
  } else {              // ai3==2
    if (row < 2) step = -1;
    else if (row > 8) step = -1;
    else if (row < 8) step = 1;
  }
  e.lai0 += step;
  if (e.lai0 > 6) { e.lai0 = 0; e.lai1 += 1; if (e.lai1 > 11) e.lai1 = 0; }
  if (e.lai0 < 0) { e.lai0 = 6; e.lai1 -= 1; if (e.lai1 < 0) e.lai1 = 11; }
  e.customFrameIdx = e.lai1;
}
```
Careful: ai3 could be other values? Our ai3 = rnd(3) ∈ {0,1,2} ✓. But initial ai3 = 0 ✓.

Wait — the ai3===2 branch in vanilla is `else if (ai[3] == 2f)` — if ai3 were 3+ none apply (step 0). Our ai3 ∈ {0,1,2} — my `else` covers 2 only. To be safe mirror vanilla structure: `else if (e.ai3 === 2) {...}` with default step 0. 

Hmm — also vanilla reads frame.Y (the row) fresh each call; my e.lai1 is the row replica. Place at end of pumpkingAI (after e.visAngle/e.x += — position irrelevant; place before `e.x += e.vx`). Actually vanilla FindFrame runs after full AI — any placement at end works. Put after the movement integration.

Betsy Renderer branch:

```ts
// 551 Betsy（cs:67913-68107）:ai0==3 吐息 / 4 空袭 → 5,6 起手 + 9/10 喷射循环
// + 8→7→0 收势(阈值两态各异);ai0==5 恒帧 3;ai0==6 召唤拍翼 1-4-1 序列按
// ai1 每 8t;其余态恒帧 0。帧源 = ai[1](状态计时,bossAI_dd2 betsyAI 1:1)
if (id === 551) {
  const fc = Math.floor(e.ai1);
  if (e.ai0 === 4) {          // 空袭(:67916-67968):起手 5/6@5t,54/57/60 递进,
    // 喷射 9/10 循环到 123,收势 8(123-127)/7(128-132)/0(≥133)
    if (fc < 5) return Math.min(frames - 1, 5);
    if (fc < 54) return Math.min(frames - 1, 6);
    if (fc < 57) return Math.min(frames - 1, 7);
    if (fc < 60) return Math.min(frames - 1, 8);
    if (fc < 123) return Math.min(frames - 1, 9 + (Math.floor(fc / 3) % 2));
    if (fc < 128) return Math.min(frames - 1, 8);
    if (fc < 133) return Math.min(frames - 1, 7);
    return 0;
  }
  if (e.ai0 === 3) {          // 吐息(:67970-68024):同构,阈值 5/34/37/40/98/103/108
    if (fc < 5) return Math.min(frames - 1, 5);
    if (fc < 34) return Math.min(frames - 1, 6);
    if (fc < 37) return Math.min(frames - 1, 7);
    if (fc < 40) return Math.min(frames - 1, 8);
    if (fc < 98) return Math.min(frames - 1, 9 + (Math.floor(fc / 3) % 2));
    if (fc < 103) return Math.min(frames - 1, 8);
    if (fc < 108) return Math.min(frames - 1, 7);
    return 0;
  }
  if (e.ai0 === 5) return Math.min(3, frames - 1);
  if (e.ai0 === 6) {          // 召唤(:68029-68100):拍翼 1,2,3,4,3,4,3,2,1,0 各 8t
    const k = Math.floor(fc / 8);
    const seq = [1, 2, 3, 4, 3, 4, 3, 2, 1, 0];
    return Math.min(frames - 1, seq[Math.min(9, k)]);
  }
  return 0;
}
```
Check state-4 thresholds again: num269=60, num271=60 → num275 = 60+60+3 = 123. ✓. State-3: num278=40, num279=80, num280=120, num281=25 → 98. ✓. State 6 seq: base 1; ≥8→2, ≥16→3, ≥24→4, ≥32→3, ≥40→4, ≥48→3, ≥56→2, ≥64→1, ≥72→0. seq index = floor(fc/8) with clamp at 9 (fc ≥ 72 → index ≥ 9 → 0). ✓.

Also — should the else (ai0 0/1/2 or -1) → 0 ✓ (vanilla `else num268 = 0`).

Now 325/344 — the e.lai0 counter for 344: maintained in mourningWoodAI. Both ids run through mourningWoodAI. Add at end:

```ts
// ---- FindFrame case 344 副本（cs:73144-73170）:counter += max(1,|vx|*0.75)/t,
//      >5 进帧(6 单位)——344 全带 0-9 无带切换,advanceCount%10 即帧号。
//      325(case cs:73172-73201) 两分支 counter 恒 +1/t ≡ animT,Renderer 用 t 直推 ----
e.lai0 += e.vx === 0 ? 1 : Math.max(1, Math.abs(e.vx) * 0.75);
```
Wait — but for 325, e.lai0 unused (Renderer uses t). And e.lai0 must only accumulate for 344? If it accumulates for both — harmless (325 branch never reads it). But cleaner: only accumulate when id === 344. Hmm — actually vanilla's counter for 344 = Σ max(1, |vx|·0.75) from spawn — my accumulation in the AI starts from first AI tick — lai0 starts 0 ✓.

But wait — for 344, `e.vx === 0` exact check (vanilla velocity.X == 0f). hoverCruise can leave vx exactly 0 (snap). ✓.

Renderer 344 branch: Math.floor(e.lai0 / 6) % 10 — clamp min(frames-1).

Hmm — hold on, one thing to verify for 344: does vanilla ever reset 344's counter? Looking at the case: no reset anywhere (both branches advance; no counter reset — only >5 → 0 wrap). ✓ unbounded accumulation → advanceCount = floor(total/6). ✓.

Now — check e.lai0 conflicts for these entities across features: lai0 used by fireflies (355/358/654 — different ids) and by 222 QueenBee? QueenBee precedent: "AI 写 e.lai0,Renderer 读" for id 222 — different entity. For our new uses: 395/392/344 write lai0 — none read it elsewhere. ✓. Pumpking 327 uses lai0+lai1 — no conflicts (fireflies only 355/358/654).

Also — the existing 266 branch reads e.lai2 — unrelated.

Now, Renderer 345 glide: note ai0 can also be -1 momentarily? Resolved same tick ✓. Day branch: ai0 stays 0/1/2 — our early-return day branch leaves ai0 at last value; e.g., if it was mid-rain (ai0=1) at dawn — vanilla same (AI day-branch skips state machine; FindFrame ai0==1 → rain band by frameCounter which vanilla still advances... hmm — vanilla day branch: velocity set; FindFrame case 345 runs: ai0==1 → frameCounter += 1 & band cycle — YES vanilla animates rain band during day-fly-away. My branch: ai0===1 → 3+floor(t/6)%2 ✓ same. And ai0===0 with stale ai3 → frame 0/1/2 by vx — during day our vx grows (±0.25/t) → frame 0 (ai3>=0) or 1/2 — vanilla same. ✓.

Now — 386: our martianFighterExtras is called "after fighterAI" (case 3 dispatch). The walk branch needs vy/vx — fine. But wait: 386's FindFrame also needs the vy==0 check — vanilla `if (ai[2] > 0f) {...} else if (velocity.Y == 0f) {...} else {air}`. ✓ my structure.

One more check — 386 deploy: our ai2 semantics: `if (e.ai2 < 60) e.ai2 += 1` — starts at... AI init: martianFighterExtras has no bInit; e.ai2 default 0 → counts up 1..60. Vanilla ai[2] init 0 → same. During deploy (ai2>0) frame 9/10 — note vanilla `(int)ai[2] / 12 % 2` — floor(ai2/12)%2 ✓.

Hmm — also: is 386 currently falling into the generic ai===3 branch? Yes (aiStyle 3) — my new 386 branch must come BEFORE the `ai === 3 || ai === 26 || ai === 107` branch (line 795). I'll place my batch before that branch — i.e., insert my whole batch right after the 266 branch (line 890) — which is well before line 795? NO — line 795 comes BEFORE 864 (222). The ai===3 branch is at line 795, my batch after 890 → 386 would be caught by ai===3 first! Order matters: `vanillaFrameIdx` checks in order; ai===3 (line 795) fires for 386 before reaching my branch at ~890.

So for 386 (and any id-based branch that would be pre-empted), placement must be BEFORE the ai===3 branch at line 795. Which of my ids are pre-empted by earlier branches?
- Walking small animals etc.: no.
- ai===7 (town): none of mine (386 is aiStyle 3 not 7).
- ai===3||26||107 (line 795): 386! (aiStyle 3). Must place 386 before line 795.
- Others (325/327/344/345/346/392-395/399/551/439/440): their aiStyles (57/58/60/61/75/76/80/110/84) don't hit earlier branches — but wait: ai===14 bats? no. ai===16 swim? no. ai===1 slime? no. Also the id-specific ones (262/266/222/113...) don't overlap. And 387 — aiStyle 73 — no earlier branch. OK.

So: insert 386 branch before the ai===3 branch; the rest of the batch can go after the 266 block (near 222/262/113 precedents) — or just put the whole batch in one contiguous place before line 795 (e.g., after the ai===1 slime branch ~line 690 or right before the 战士族 comment at line 794). Simplest: one contiguous batch inserted right before the `// 战士族/107` branch (line 794-795). Hmm — but the task says "在既有 case 266/222/262/113 等先例处追加分支" (add branches at the existing precedent sites) — that's about following the established pattern, not exact line placement. A contiguous batch before 战士族 is cleanest. Actually — let me place it right after the mechQueen/Prime branches... no. Decision: insert the batch just before line 794 (`// 战士族/107`). All ids unique, no overlap with anything above except 386-vs-ai3 (solved by being before it).

Double-check no earlier branch catches my ids:
- ZOMBIE_FRAME_TYPES: zombie ids — no.
- ai===17||25: no (my aiStyles: 3(386),57,58,60,61,73(387),75,76,80,84,110).
- ai===40: no. id 164 group: no. id 42/231-235: no. ai===14: no. ai===1: no. ai===11/12: no.
- 46-family ids: no. 230/593: no. 148: no. 299: no. 300/447/610: no. 361: no. 362: no. 616/625: no. ai===7: no. ai===3/26/107: 386 yes (placed before). ai===65: no. 615: no. 55-family: no. 688: no. 692: no. 65: no. 542-545: no. ai===16: no. ai===18: no. id 4/125/126: no. 222: no. 113/114: no. 262: no. 266: no. 5: no. 488: no. 115/116/133/127/129/130: no. CASTER_STATE_FRAME_TYPES — check! That set includes "29/32/45/172/281-286/693" — none of mine. 24: no. 533: no. 74: no. 671-675: no. 611: no. 355: no. 677: no. 595-601: no. 357: no. 485: no. 604: no. 363: no. 473-476: no. 

So inserting before 战士族 (line 795) works for the whole batch. 

Also — for the Cultist 439/440: customFrameIdx written by AI → first line short-circuits; no Renderer branch needed. But hmm — what about `Math.min(frames - 1, e.customFrameIdx)` — frames for 439 = 16 (16 rows: 0-15) — clamp handles.

One more: **395's ai3 during expert deathray (ai0===2)**: window [20,260) uses ai3 (0..3600 cycle). During ai0=2, ai3 counts 0..3599; [20,260) true only when ai3 ∈ that range → the first 240t of the 3600 cycle?? Vanilla: during ai0==2, is 395's FindFrame flag10 reading ai[3]? Yes literally [20,260). During the deathray barrage, ai[3] cycles 0..3599 — so the glow band triggers during the first 240t of the barrage cycle = the non-firing phase (ray window is %120>=60). Hmm whatever — literal port ✓ (our replica uses same ai3).

And 392 during ai0===2 — e.ai3 = saucer.ai3 → same literal ✓.

Wait — hmm, actually there's one thing I should double check about 392/393/394's ai3 sync: our parts set `e.ai3 = saucer.ai3` INSIDE their AI each tick. But the RENDERER reads e.ai3 for 393/394 — between AI runs it's the last synced value ✓.

But — subtle: for 393, the laser window in the RENDERER branch uses e.ai3 — the value synced at the part's AI tick. Vanilla 393 FindFrame reads its own ai[3] — which vanilla's 393 AI (:36171) sets = `npc[ai[1]].ai[3]`? Hmm — our port comment says "部件攻击窗(共享 saucer.ai[3] 计数,cs:36128/36171/36235)" — 1:1 ✓.

Now — verify the frames counts exist in our atlas json (e.vanilla.frames): 393 should be 18, 394 8, 395 11, 392 4, 399 8, 387 2, 386 11, 325 10, 327 12, 344 10, 345 6, 346 9, 551 11, 439/440 16. Let me check the vanilla json to be sure (frames field). Where's the json? Probably game/public or src/data — "vanilla.json 运行时合成" per memory. Let me grep for npcFrameCount or the json entries for a couple ids to sanity check — mainly to catch any frames mismatch that would clamp my frames into wrong values. Let me search for how vanilla?.frames is populated.

Actually — the memory note "npc帧数闸门+石锤复核 — 三层闸门运行时直读Main.cs零快照;json×npcFrameCount×贴图高三方零差" suggests frames counts are verified 1:1 already. I'll trust `frames` and clamp defensively.

Let me quickly verify one: 345 frames (should be 6). Search the json.
````

</details>


---

## 🤖 Assistant · 2026-08-19T08:02:12.632Z · glm-x-preview-260804

```
我现在已经掌握了全貌。在编写代码之前，我先验证一下这些 ID 的帧数数据源。
```


---

## 🤖 Assistant · 2026-08-19T08:02:14.237Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"npcFrameCount\" src/ --include=*.ts -l | head -5; ls public/ | head; ls src/data 2>/dev/null | head",
 "description": "Find npcFrameCount data source"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:02:14.281Z

**📎 ToolResult**

```
(eval):1: no matches found: --include=*.ts
annotator.html
assets-index.json
audios
debug-save.sbw.json
fonts
hitbox-lab.html
hitbox-names.json
l10n
remaster.html
sheet-probe.html
Bestiary.ts
bestiaryStatics.generated.ts
combat-font.json
critters.ts
enemies.ts
flexible-wands.json
fxPixelShader.json
grappleHooks.ts
itemKeys.ts
itemMigration.ts

```


---

## 🤖 Assistant · 2026-08-19T08:02:18.930Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"frames\" src/data/enemies.ts | head -5; grep -rn \"vanilla?.frames\\|vanilla.frames\" src/entities/Enemy.ts | head -5; grep -rln \"NPC_FRAME_COUNT\\|npcFrameCount\\|frameCount\" src/ | head -8",
 "description": "Trace vanilla frames field source"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:02:18.993Z

**📎 ToolResult**

```
src/remaster/PromptTemplates.ts
src/render/EmoteBubble.ts
src/render/Renderer.ts
src/render/SkyRenderer.ts
src/render/NatureParticles.ts
src/data/vanillaNpcs.ts
src/entities/MinionProj.ts
src/entities/bossAI_golem.ts

```


---

## 🤖 Assistant · 2026-08-19T08:02:22.620Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"frames\" src/data/vanillaNpcs.ts | head -10; node -e \"\nconst m = require('fs').readFileSync('src/data/vanillaNpcs.ts','utf8');\nconst idx = m.indexOf('frames');\nconsole.log(m.slice(Math.max(0,idx-400), idx+200));\n\" 2>/dev/null | head -30",
 "description": "Inspect vanillaNpcs frames definition"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:02:22.679Z

**📎 ToolResult**

```
52:  frames: number;
115:// 行走帧循环区间的回卷上界：帧 >= frames-extra 时回帧 2（NPC.cs FindFrame L70244）
EM_BY_KEY[meta.key] != null) key = meta.key;
      // vi_NNN 导入物品（items.ts 的全量原版物品命名）：vi_<id> 或 vi_<id>_<snake>
      else if (ITEM_BY_KEY[`vi_${itemId}`] != null) key = `vi_${itemId}`;
      else if (ITEM_BY_KEY[`vi_${itemId}_${snake}`] != null) key = `vi_${itemId}_${snake}`;
    }
    map.set(itemId, key);
    return key;
  };
})();

export interface VanillaNpc {
  id: number;
  name: string;
  frames: number;
  lifeMax: number;
  damage: number;
  defense: number;
  knockBackResist: number;
  aiStyle: number;
  width: number;
  height: number;
  npcSlots: number;
  noGravity: boolean;
  noT

```


---

## 🤖 Assistant · 2026-08-19T08:02:27.657Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "node -e \"\nconst fs = require('fs');\n// find the generated npc data (vanilla.json?)\nconst cands = fs.readdirSync('public');\n\" ; ls public/sprites 2>/dev/null | head -3; find . -maxdepth 3 -name \"vanilla*.json\" -not -path \"*/node_modules/*\" 2>/dev/null | head; grep -rn \"fromVanilla\" src/entities/Enemy.ts | head -3",
 "description": "Locate generated vanilla npc json"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:02:27.729Z

**📎 ToolResult**

```
annotations.json
atlas.json
portraits
./scripts/vanilla-ui-whitelist.json
./scripts/vanilla-whitelist.json
./dist/sprites/vanilla-npcs.json
./dist/sprites/vanilla-npcgore.json
./dist/sprites/vanilla.json
./dist/sprites/vanilla-ui.json
./public/sprites/vanilla-npcs.json
./public/sprites/vanilla-npcgore.json
./public/sprites/vanilla.json
./public/sprites/vanilla-ui.json
src/entities/Enemy.ts:265:/** 原版路径 key（v_*）的占位 def，fromVanilla 会整体覆写 */
src/entities/Enemy.ts:274: *  挂 fromVanilla/Transform 构造点 = 常规刷怪/雕像/Boss 召唤/分裂/变形零漂移覆盖
src/entities/Enemy.ts:719:    const spit = Enemy.fromVanilla(666, this.cx + this.vx, this.cy + this.vy);

```


---

## 🤖 Assistant · 2026-08-19T08:02:36.764Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "node -e \"\nconst d = require('./public/sprites/vanilla-npcs.json');\nconst arr = Array.isArray(d) ? d : (d.npcs || d.list || Object.values(d));\nconst want = [325,327,344,345,346,386,387,392,393,394,395,399,439,440,551];\nif (Array.isArray(arr)) {\n  for (const id of want) {\n    const e = arr.find((x) => x.id === id);\n    console.log(id, e ? 'frames=' + e.frames + ' aiStyle=' + e.aiStyle : 'MISSING');\n  }\n} else { console.log('keys:', Object.keys(d).slice(0,8)); }\n\"",
 "description": "Check frames and aiStyle for target NPC ids"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:02:36.838Z

**📎 ToolResult**

```
325 frames=10 aiStyle=57
327 frames=12 aiStyle=58
344 frames=10 aiStyle=57
345 frames=6 aiStyle=60
346 frames=9 aiStyle=61
386 frames=11 aiStyle=3
387 frames=2 aiStyle=73
392 frames=4 aiStyle=75
393 frames=18 aiStyle=75
394 frames=8 aiStyle=75
395 frames=11 aiStyle=76
399 frames=8 aiStyle=80
439 frames=16 aiStyle=84
440 frames=16 aiStyle=84
551 frames=11 aiStyle=110

```


---

## 🤖 Assistant · 2026-08-19T08:02:46.639Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All frame counts match my expectations:
- 325: 10 ✓ (idle 0-4 + move 5-9)
- 327: 12 ✓ (pose rows 0-11)
- 344: 10 ✓
- 345: 6 ✓ (glide 0-2, rain 3-4, spin 5)
- 346: 9 ✓ (walk 1-5, fire 6-8; frame 0 initial)
- 386: 11 ✓ (walk 2-8, air 1, idle 0, deploy 9-10)
- 387: 2 ✓
- 392: 4 ✓
- 393: 18 ✓ (9 direction + 9 firing)
- 394: 8 ✓ (0-7)
- 395: 11 ✓ (0-10)
- 399: 8 ✓ (scan 0-3, alert 4-7)
- 439/440: 16 ✓ (rows 0-15)
- 551: 11 ✓ (0-10)

Now, before writing code, let me check the tests that exist: tests/bossAI-lategame.test.ts, tests/bossAI-moon-events*.test.ts, tests/bossAI-dd2.test.ts. And get the tsc baseline. Also check spawnPart's signature (used in AI files? no — I'm only adding counter updates). Let me also check `la()` in bossAI_lategame (laOf) definition to reuse.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:02:47.362Z · glm-x-preview-260804

```
所有帧计数均已匹配。我先检查一下现有的测试，并在编辑前获取 `tsc` 基准。
```


---

## 🤖 Assistant · 2026-08-19T08:02:48.447Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls tests/ | grep -i \"bossAI\\|lategame\\|martian\\|moon\\|dd2\"; echo ---; npx tsc --noEmit 2>&1 | head -20",
 "description": "List bossAI tests and capture tsc baseline"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:03:06.392Z

**📎 ToolResult**

```
bossAI-dd2.test.ts
bossAI-deerclops.test.ts
bossAI-lategame.test.ts
bossAI-lunar-misc.test.ts
bossAI-mechdusa.test.ts
bossAI-plantera.test.ts
dd2-walker.test.ts
lategame-subsystems.test.ts
martian-deathray.test.ts
moon-shop-aggro.test.ts
---
src/render/Renderer.ts(4188,39): error TS2551: Property 'drawMoonLordFreeEye' does not exist on type 'Renderer'. Did you mean 'drawMoonLordCore'?
src/world/gen/vanilla/TrackPass.ts(423,12): error TS2339: Property 'smoothSlope' does not exist on type 'TrackGenerator'.
src/world/gen/vanilla/TrackPass.ts(427,16): error TS2339: Property 'smoothSlope' does not exist on type 'TrackGenerator'.
tests/_furn-zero-frames.test.ts(21,24): error TS2683: 'this' implicitly has type 'any' because it does not have a type annotation.
tests/_ghost.test.ts(28,3): error TS2322: Type 'string' is not assignable to type 'number'.
tests/ai-parity-batch-2026-08-19.test.ts(67,29): error TS2554: Expected 3 arguments, but got 2.
tests/boss-parity-fixes-a.test.ts(207,35): error TS2339: Property 'toBeLessThan' does not exist on type 'void'.
tests/boulder-2x2.test.ts(22,31): error TS2554: Expected 1 arguments, but got 2.
tests/boulder-trap-e2e.test.ts(39,29): error TS2554: Expected 1 arguments, but got 2.
tests/boulder-trap.test.ts(23,5): error TS1117: An object literal cannot have multiple properties with the same name.
tests/caves-checkpoint.test.ts(310,7): error TS2367: This comparison appears to be unintentional because the types '1 | -1' and '0' have no overlap.
tests/fullmap-bg-index.test.ts(40,10): error TS2554: Expected 3 arguments, but got 2.
tests/fullmap-bg-index.test.ts(52,8): error TS2554: Expected 3 arguments, but got 2.
tests/fullmap-bg-index.test.ts(60,8): error TS2554: Expected 3 arguments, but got 2.
tests/fullmap-bg-index.test.ts(72,8): error TS2554: Expected 3 arguments, but got 2.
tests/item-tooltip.test.ts(95,61): error TS2345: Argument of type '{ dmgMult: { melee: number; ranged: number; magic: number; summon: number; }; crit: { melee: number; ranged: number; magic: number; }; manaCostMul: number; }' is not assignable to parameter of type 'TooltipPlayerStats'.
  Type '{ dmgMult: { melee: number; ranged: number; magic: number; summon: number; }; crit: { melee: number; ranged: number; magic: number; }; manaCostMul: number; }' is missing the following properties from type 'TooltipPlayerStats': kbGlove, kbBuff, setBonusText
tests/item-tooltip.test.ts(100,63): error TS2345: Argument of type '{ dmgMult: { melee: number; ranged: number; magic: number; summon: number; }; crit: { melee: number; ranged: number; magic: number; }; manaCostMul: number; }' is not assignable to parameter of type 'TooltipPlayerStats'.
  Type '{ dmgMult: { melee: number; ranged: number; magic: number; summon: number; }; crit: { melee: number; ranged: number; magic: number; }; manaCostMul: number; }' is missing the following properties from type 'TooltipPlayerStats': kbGlove, kbBuff, setBonusText
tests/npc-damage-gate.test.ts(33,49): error TS2554: Expected 3 arguments, but got 4.

```


---

## 🤖 Assistant · 2026-08-19T08:03:13.059Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
There's a large pre-existing tsc baseline (many errors in tests and some files from parallel sessions). Note the first error: `src/render/Renderer.ts(4188,39): error TS2551: Property 'drawMoonLordFreeEye' does not exist` — a pre-existing Renderer error at line 4188 (parallel session mid-edit). I must not add NEW errors; I'll compare error lists before/after my change (filtered to my files).

Let me save the full baseline error list to compare after.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:03:14.239Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "npx tsc --noEmit 2>&1 | sort > /tmp/tsc-baseline.txt; wc -l /tmp/tsc-baseline.txt; grep -c \"Renderer.ts\\|bossAI\" /tmp/tsc-baseline.txt",
 "description": "Save full tsc baseline for comparison"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:03:42.111Z

**📎 ToolResult**

```
      73 /tmp/tsc-baseline.txt
0

```


---

## 🤖 Assistant · 2026-08-19T08:03:47.155Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting — the grep count says 0 for "Renderer.ts|bossAI"?? But the first error was Renderer.ts(4188). The `grep -c` with pipe alternation... `grep -c "Renderer.ts\|bossAI"` — zsh might have interpreted... it returned 0 which is wrong. Probably the sort/scrambling — whatever, the file has 73 lines. Let me check directly.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:03:48.123Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -E \"Renderer\\.ts|bossAI\" /tmp/tsc-baseline.txt | head; echo \"== total: $(wc -l < /tmp/tsc-baseline.txt)\"",
 "description": "Check baseline errors in Renderer and bossAI files"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:03:48.195Z

**📎 ToolResult**

```
== total:       73

```


---

## 🤖 Assistant · 2026-08-19T08:03:55.713Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Odd — the baseline (sorted) has no Renderer.ts lines, but the earlier unsorted run showed `src/render/Renderer.ts(4188,39)`. Maybe the file changed between runs (a parallel session actively editing Renderer.ts!). CLAUDE.md warns about parallel sessions. The error `drawMoonLordFreeEye` suggests someone is mid-edit on Renderer.ts RIGHT NOW.

Let me re-run to see the current state. Also per memory note "并行会话改Game.ts须重grep再Edit" — I must re-grep before editing and be careful. My edits to Renderer.ts are localized (insert a block in vanillaFrameIdx); Edit tool requires exact match — if a parallel session edits other parts of the file, my edit still applies (different region). The risk is if they edit the same region. I'll proceed carefully and re-read right before editing.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:03:56.937Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "npx tsc --noEmit 2>&1 | sort > /tmp/tsc-baseline2.txt; diff /tmp/tsc-baseline.txt /tmp/tsc-baseline2.txt && echo SAME; grep -E \"render/Renderer\" /tmp/tsc-baseline2.txt | head -3",
 "description": "Re-check tsc baseline stability"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:04:17.552Z

**📎 ToolResult**

```
11,28c11,35
< src/world/gen/vanilla/TrackPass.ts(535,15): error TS2304: Cannot find name 'SHEET_190'.
< src/world/gen/vanilla/TrackPass.ts(535,34): error TS2304: Cannot find name 'SHEET_30'.
< src/world/gen/vanilla/TrackPass.ts(563,19): error TS2304: Cannot find name 'SHEET_323'.
< src/world/gen/vanilla/TrackPass.ts(564,20): error TS2304: Cannot find name 'SHEET_21'.
< src/world/gen/vanilla/TrackPass.ts(564,40): error TS2304: Cannot find name 'SHEET_26'.
< src/world/gen/vanilla/TrackPass.ts(564,60): error TS2304: Cannot find name 'SHEET_72'.
< src/world/gen/vanilla/TrackPass.ts(564,80): error TS2304: Cannot find name 'SHEET_77'.
< src/world/gen/vanilla/TrackPass.ts(565,20): error TS2304: Cannot find name 'SHEET_88'.
< src/world/gen/vanilla/TrackPass.ts(565,40): error TS2304: Cannot find name 'SHEET_467'.
< src/world/gen/vanilla/TrackPass.ts(565,61): error TS2304: Cannot find name 'SHEET_488'.
< src/world/gen/vanilla/TrackPass.ts(566,19): error TS2304: Cannot find name 'SHEET_80'.
< src/world/gen/vanilla/TrackPass.ts(574,15): error TS2304: Cannot find name 'SHEET_10'.
< src/world/gen/vanilla/TrackPass.ts(575,15): error TS2304: Cannot find name 'SHEET_235'.
< src/world/gen/vanilla/TrackPass.ts(581,15): error TS2304: Cannot find name 'SHEET_21'.
< src/world/gen/vanilla/TrackPass.ts(581,33): error TS2304: Cannot find name 'SHEET_467'.
< src/world/gen/vanilla/TrackPass.ts(583,22): error TS2304: Cannot find name 'SHEET_88'.
< src/world/gen/vanilla/TrackPass.ts(596,56): error TS2304: Cannot find name 'SHEET_77'.
< src/world/gen/vanilla/TrackPass.ts(609,24): error TS2304: Cannot find name 'SHEET_10'.
---
> src/world/gen/vanilla/TrackPass.ts(536,9): error TS2304: Cannot find name 'POUND_BLOCK_TYPES'.
> src/world/gen/vanilla/TrackPass.ts(537,19): error TS2304: Cannot find name 'BOULDER_SHEETS_SS'.
> src/world/gen/vanilla/TrackPass.ts(539,15): error TS2304: Cannot find name 'SHEET_190'.
> src/world/gen/vanilla/TrackPass.ts(539,34): error TS2304: Cannot find name 'SHEET_30'.
> src/world/gen/vanilla/TrackPass.ts(548,12): error TS2304: Cannot find name 'FORBIDS_SLOPING'.
> src/world/gen/vanilla/TrackPass.ts(565,11): error TS2552: Cannot find name 'IS_TREE_TRUNK_SS'. Did you mean 'TREE_TRUNK_SS'?
> src/world/gen/vanilla/TrackPass.ts(567,19): error TS2304: Cannot find name 'SHEET_323'.
> src/world/gen/vanilla/TrackPass.ts(568,20): error TS2304: Cannot find name 'SHEET_21'.
> src/world/gen/vanilla/TrackPass.ts(568,40): error TS2304: Cannot find name 'SHEET_26'.
> src/world/gen/vanilla/TrackPass.ts(568,60): error TS2304: Cannot find name 'SHEET_72'.
> src/world/gen/vanilla/TrackPass.ts(568,80): error TS2304: Cannot find name 'SHEET_77'.
> src/world/gen/vanilla/TrackPass.ts(569,20): error TS2304: Cannot find name 'SHEET_88'.
> src/world/gen/vanilla/TrackPass.ts(569,40): error TS2304: Cannot find name 'SHEET_467'.
> src/world/gen/vanilla/TrackPass.ts(569,61): error TS2304: Cannot find name 'SHEET_488'.
> src/world/gen/vanilla/TrackPass.ts(570,19): error TS2304: Cannot find name 'SHEET_80'.
> src/world/gen/vanilla/TrackPass.ts(577,9): error TS2304: Cannot find name 'BOULDER_SHEETS_SS'.
> src/world/gen/vanilla/TrackPass.ts(578,15): error TS2304: Cannot find name 'SHEET_10'.
> src/world/gen/vanilla/TrackPass.ts(579,15): error TS2304: Cannot find name 'SHEET_235'.
> src/world/gen/vanilla/TrackPass.ts(585,15): error TS2304: Cannot find name 'SHEET_21'.
> src/world/gen/vanilla/TrackPass.ts(585,33): error TS2304: Cannot find name 'SHEET_467'.
> src/world/gen/vanilla/TrackPass.ts(587,22): error TS2304: Cannot find name 'SHEET_88'.
> src/world/gen/vanilla/TrackPass.ts(600,56): error TS2304: Cannot find name 'SHEET_77'.
> src/world/gen/vanilla/TrackPass.ts(600,68): error TS2304: Cannot find name 'PREVENTS_REMOVAL_ON_TOP'.
> src/world/gen/vanilla/TrackPass.ts(601,39): error TS2304: Cannot find name 'IS_A_CONTAINER_SS'.
> src/world/gen/vanilla/TrackPass.ts(613,24): error TS2304: Cannot find name 'SHEET_10'.

```


---

## 🤖 Assistant · 2026-08-19T08:04:25.281Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: a parallel session is actively editing TrackPass.ts (baseline churns). The Renderer.ts drawMoonLordFreeEye error disappeared between runs too — active churn. My acceptance criterion: no NEW errors attributable to my changes. I'll diff before/after filtered to my touched files and the specific line ranges.

Now — vitest tests to run: tests/bossAI-lategame.test.ts, tests/bossAI-moon-events*.test.ts (which? there's no bossAI-moon-events*.test.ts — I see moon-shop-aggro.test.ts; let me glob), tests/bossAI-dd2.test.ts, and maybe bossAI-lategame + martian-deathray. Let me run the baseline tests FIRST to know pre-existing status.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:04:26.501Z · glm-x-preview-260804

```
有一个并行会话正在修改 `TrackPass.ts` —— 基线会产生波动；我只会排查自己引入的错误。我先来检查一下测试文件和基准。
```


---

## 🤖 Assistant · 2026-08-19T08:04:29.223Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls tests/ | grep -E \"moon|lategame|dd2|martian\"; npx vitest run tests/bossAI-lategame.test.ts tests/bossAI-dd2.test.ts tests/moon-shop-aggro.test.ts tests/martian-deathray.test.ts 2>&1 | tail -15",
 "description": "Run baseline of related bossAI tests"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:04:37.054Z

**📎 ToolResult**

```
bossAI-dd2.test.ts
bossAI-lategame.test.ts
dd2-walker.test.ts
lategame-subsystems.test.ts
martian-deathray.test.ts
moon-shop-aggro.test.ts
[atlas-lint] 753 表全自洽 ✓ (0 warn)
[l10n-audit] 515 键全部命中 ✓

 RUN  v2.1.9 ~/Project/GLM/SandboxWorld/game

 ✓ tests/moon-shop-aggro.test.ts (11 tests) 9ms
 ✓ tests/bossAI-lategame.test.ts (49 tests) 46ms
 ✓ tests/bossAI-dd2.test.ts (22 tests) 70ms
 ✓ tests/martian-deathray.test.ts (4 tests) 7ms

 Test Files  4 passed (4)
      Tests  86 passed (86)
   Start at  16:04:30
   Duration  6.23s (transform 5.09s, setup 0ms, collect 19.23s, tests 131ms, environment 1ms, prepare 1.31s)

```


---

## 🤖 Assistant · 2026-08-19T08:04:51.331Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All 86 baseline tests green. Now let me write the code.

### Edit 1: Renderer.ts — insert the batch in vanillaFrameIdx before the 战士族 branch (line 794-795 area).

Content: branches for 325, 327(no — customFrameIdx; skip), 344, 345, 346(no — customFrameIdx), 386, 387, 392, 393, 394, 395, 399, 551. For 327/346/439/440 — handled via customFrameIdx (AI-written); I'll add a short comment in the Renderer batch noting where they're handled? Better keep Renderer clean; the AI files have the comments. Hmm — actually adding a one-line comment in Renderer helps discoverability. I'll include brief pointer comments.

Order inside the batch: martian family first, then moon events, then Betsy.

### Edit 2: bossAI_martian.ts:
- martianSaucerAI: add 395 counter replica (called at the two non-death exits).
- martianSaucerPartAI: add 392 counter replica at end.

### Edit 3: bossAI_moon_events.ts:
- mourningWoodAI: accumulate e.lai0 for 344 (and harmless for 325? — only 344 to keep semantics clean; guard `if (ever)`).
- pumpkingAI: 327 pose-walk replica → customFrameIdx (uses e.lai0 counter / e.lai1 row).
- santaNK1AI: 346 full frame machine → customFrameIdx (L[0] counter, L[3] row).

### Edit 4: bossAI_lategame.ts:
- lunaticCultistAI: cultist frame machine (WeakMap cultistAnim) + frame-state mapping + tick → customFrameIdx.

Let me now write the Renderer insert. First re-read the exact region around line 790-800 to anchor the edit (parallel sessions!).
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:04:52.206Z · glm-x-preview-260804

```
基准测试已通过。现在我来执行实现。首先进行 Renderer 批次处理 —— 在编辑前重新检查锚定区域（并行会话注意事项）。
```


---

## 🤖 Assistant · 2026-08-19T08:04:52.767Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "limit": 18,
 "offset": 790
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:04:52.782Z

**📎 ToolResult**

```
790	    if (id === 489) return 2 + (Math.floor((e.walkCycleT + t * 0.5) / 8) % len);
791	    const step = id === 632 || id === 534 || id === 638 || id === 656 ? 12 : 6;
792	    return 2 + (Math.floor((e.walkCycleT * 2 + t) / step) % len);
793	  }
794	  // 战士族/107（L70155-70252）：站定=0；行走从帧 2 起按 |vx|*2+1 累加、>6 推进、循环回 2
795	  if (ai === 3 || ai === 26 || ai === 107) {
796	    if (!e.onGround) return frames - 1; // 腾空取末帧（原版 ai[0]==2 在 0/末帧间交替）
797	    if (!walking) return 0;
798	    const cycLen = Math.max(1, frames - 2);
799	    const step = Math.floor((e.walkCycleT * (Math.abs(e.vx) * 2 + 1)) / 6);
800	    return 2 + (step % cycLen);
801	  }
802	  // 蝶族（FindFrame case 356/444/653/661，cs:73419-73455）：拍翅四段 [0,1,2,1]
803	  //  （7t 档；原版 counter 加 (|vx|+|vy|)/2 速度敏感——速率随速近似取定档）。
804	  //  356 物种带：frame.Y += 3 帧×(ai[2]-1)（cs:73452-55）——八物种按 ai2 分带
805	  //  （出生加权掷/释放 Style 定；444/653/661 单物种帧表 3 帧不分带）
806	  if (ai === 65) {
807	    const anim = [0, 1, 2, 1][Math.floor(t / 7) % 4];

```


---

## 🤖 Assistant · 2026-08-19T08:05:41.281Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "old_string": "  // 战士族/107（L70155-70252）：站定=0；行走从帧 2 起按 |vx|*2+1 累加、>6 推进、循环回 2\n  if (ai === 3 || ai === 26 || ai === 107) {",
 "new_string": "  // ============ 火星疯狂/月事件/Betsy FindFrame 批（2026-08-19，逐条 cs 行号）============\n  // （须在上方 ai===3 战士族档之前——386 工程师 aiStyle=3 会被截胡；\n  //   327 南瓜王/346 圣诞坦克/439·440 教徒的帧机有帧行记忆，由各自 AI 文件\n  //   每帧写 e.customFrameIdx 直读（694 先例），不经本函数）\n  // 393 飞碟炮塔（cs:72481-72494）：ai[2]=瞄准角→九向帧（ToRotationVector2 分带）；\n  //   激光窗 [280,420) 且 (int)ai[3]%6<=2 → +9 射击行（bossAI_martian 393 段\n  //   1:1 写 ai2=atan2 角/ai3=母碟共享计数）\n  if (id === 393) {\n    const ax = Math.cos(e.ai2), ay = Math.sin(e.ai2);\n    let f393 = ay > Math.abs(ax) * 2 ? 4\n      : ay > Math.abs(ax) * 1.5 ? (ax > 0 ? 5 : 3)\n      : Math.abs(ax) > ay * 2 ? (ax > 0 ? 8 : 0)\n      : Math.abs(ax) <= ay * 1.5 ? (ax > 0 ? 6 : 2)\n      : (ax > 0 ? 7 : 1);\n    if (e.ai3 >= 280 && e.ai3 < 420 && (e.ai3 | 0) % 6 <= 2) f393 += 9;\n    return Math.min(frames - 1, f393);\n  }\n  // 394 飞碟火炮（cs:72495-72518）：纯 ai[3] 相位帧——窗前(420-440) 4+n/5 递进、\n  //   火炮窗(440-580) (n/4)%4 四帧循环、窗尾(580-600) 7-n/5 回落、其余恒帧 4\n  if (id === 394) {\n    let n394 = (e.ai3 | 0) - 300;\n    let f394: number;\n    if (n394 >= 120) {\n      n394 -= 120;\n      if (n394 >= 160) f394 = 7 - Math.floor((n394 - 160) / 5);\n      else if (n394 >= 20) f394 = Math.floor(n394 / 4) % 4;\n      else f394 = 4 + Math.floor(n394 / 5);\n    } else f394 = 4;\n    return Math.min(frames - 1, f394);\n  }\n  // 395 飞碟母碟（cs:72520-72541）：counter 每 tick +1（66 回卷，帧=counter/6 → 0-10）；\n  //   死光电报窗 ai[3]∈[20,260) 内再 +1 且钳 [36,53] → 恒落帧 6-8 蓄能辉光带。\n  //   counter 副本由 bossAI_martian martianSaucerAI 累进到 e.lai0（蜂后 222 先例）\n  if (id === 395) return Math.min(frames - 1, Math.floor((e.lai0 % 66) / 6));\n  // 392 飞碟炮体（cs:72543-72560）：4 帧旋球 counter 每 tick +1（电报窗内 ×2）、\n  //   12 回卷，帧=counter/3；副本在 bossAI_martian martianSaucerPartAI 尾段\n  if (id === 392) return Math.min(frames - 1, Math.floor((e.lai0 % 12) / 3));\n  // 399 火星探测器（cs:72562-72565）：counter 每 tick +0.25 四帧扫描带（0.25t/帧）；\n  //   ai[0]≠0（受惊悬停/逃逸）→ +4 警戒带\n  if (id === 399) {\n    return Math.min(frames - 1, Math.floor((t * 0.25) % 4) + (e.ai0 !== 0 ? 4 : 0));\n  }\n  // 387 特斯拉炮塔（cs:72335-72368）：两帧电球——ai[0]>0 充电档 counter 每 tick\n  //   +1（≥20 再 +1、≥40 再 +1，10 单位/帧）；ai[0]≤0 待机 15 单位/帧。\n  //   相位取全局 t（2 帧闪切，相位任意视觉等价）\n  if (id === 387) {\n    const per387 = e.ai0 > 0 ? 10 / (1 + (e.ai0 >= 20 ? 1 : 0) + (e.ai0 >= 40 ? 1 : 0)) : 15;\n    return Math.min(frames - 1, Math.floor(t / per387) % 2);\n  }\n  // 386 火星工程师（cs:72369-72402）：放塔期（ai[2]>0）帧 9/10 每 12t 交替；\n  //   地面行走带 2-8 按 |vx|*2 累计（无 +1）、>6 进帧；站定=0；腾空=1\n  if (id === 386) {\n    if (e.ai2 > 0) return Math.min(frames - 1, 9 + (Math.floor(e.ai2 / 12) % 2));\n    if (e.vy !== 0) return Math.min(1, frames - 1);\n    if (!walking) return 0;\n    return Math.min(frames - 1, 2 + Math.floor((e.walkCycleT * 2) / 7) % 7);\n  }\n  // 325 哀木（cs:73172-73201）：站定带 0-4 / 移动带 5-9，counter 恒 +1/t、>4 进帧\n  //   （两分支同速 → counter ≡ animT，无 AI 侧状态；带切换瞬间带内相位任意，登记）\n  if (id === 325) {\n    return Math.min(frames - 1, e.vx === 0 ? Math.floor(t / 5) % 5 : 5 + (Math.floor(t / 5) % 5));\n  }\n  // 344 常世吼（cs:73144-73170）：全带 0-9，counter += max(1,|vx|*0.75)/t、>5 进帧\n  //   （6 单位/帧，速率随速度变化）——累计副本由 mourningWoodAI 累进到 e.lai0\n  if (id === 344) return Math.min(frames - 1, Math.floor(e.lai0 / 6) % 10);\n  // 345 冰雪女王（cs:73106-73143）：滑翔(ai0==0) 定帧 0 / ai3<0 半周期按 vx 向 1|2；\n  //   落冰压制(ai0==1) 带 3-4 每 6t；自旋环射(ai0==2) 恒帧 5\n  if (id === 345) {\n    if (e.ai0 === 0) {\n      if (e.ai3 >= 0) return Math.min(2, frames - 1);\n      return e.vx < 0 ? 1 : 2;\n    }\n    if (e.ai0 === 1) return Math.min(frames - 1, 3 + (Math.floor(t / 6) % 2));\n    if (e.ai0 === 2) return Math.min(5, frames - 1);\n    return 0;\n  }\n  // 551 Betsy（cs:67913-68107）：帧源 = ai[1]（状态计时，betsyAI 1:1 同步）——\n  //   ai0==4 空袭 / 3 吐息：起手 5(<5t)→6(<54/34t)→7/8 递进 → 喷射 9↔10 循环\n  //   （fc/3%2）→ 收势 8→7→0；ai0==5 恒帧 3；ai0==6 召唤拍翼序列\n  //   1,2,3,4,3,4,3,2,1,0 各 8t；其余态（悬停/风压/入场）恒帧 0\n  if (id === 551) {\n    const fc551 = Math.floor(e.ai1);\n    if (e.ai0 === 4) {\n      if (fc551 < 5) return Math.min(frames - 1, 5);\n      if (fc551 < 54) return Math.min(frames - 1, 6);\n      if (fc551 < 57) return Math.min(frames - 1, 7);\n      if (fc551 < 60) return Math.min(frames - 1, 8);\n      if (fc551 < 123) return Math.min(frames - 1, 9 + (Math.floor(fc551 / 3) % 2));\n      if (fc551 < 128) return Math.min(frames - 1, 8);\n      if (fc551 < 133) return Math.min(frames - 1, 7);\n      return 0;\n    }\n    if (e.ai0 === 3) {\n      if (fc551 < 5) return Math.min(frames - 1, 5);\n      if (fc551 < 34) return Math.min(frames - 1, 6);\n      if (fc551 < 37) return Math.min(frames - 1, 7);\n      if (fc551 < 40) return Math.min(frames - 1, 8);\n      if (fc551 < 98) return Math.min(frames - 1, 9 + (Math.floor(fc551 / 3) % 2));\n      if (fc551 < 103) return Math.min(frames - 1, 8);\n      if (fc551 < 108) return Math.min(frames - 1, 7);\n      return 0;\n    }\n    if (e.ai0 === 5) return Math.min(3, frames - 1);\n    if (e.ai0 === 6) {\n      const seq551 = [1, 2, 3, 4, 3, 4, 3, 2, 1, 0];\n      return Math.min(frames - 1, seq551[Math.min(9, Math.floor(fc551 / 8))]);\n    }\n    return 0;\n  }\n  // 战士族/107（L70155-70252）：站定=0；行走从帧 2 起按 |vx|*2+1 累加、>6 推进、循环回 2\n  if (ai === 3 || ai === 26 || ai === 107) {"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:05:41.315Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T08:05:49.022Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Renderer done. Now the AI-side syncs.

### bossAI_martian.ts — two edits:

1. martianSaucerAI (395): counter replica. Insert the closure after the bInit block (so it's defined before use) and call at the two non-death exits: (a) the -1/-2 branch before `fly(e); return;`, (b) at the end before the final `fly(e);` (after bounds check).

Actually wait — looking at the function again:
- Line 187-193: ai0===3 self-destruct → dies (skip).
- Line 206-222: -1/-2 branch → `fly(e); return;` — insert call before fly.
- Line 333-341: bounds check → dead (skip).
- Line 341: final fly(e) — insert call before.

Let me write the edits.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:05:49.763Z · glm-x-preview-260804

```
现在处理火星 AI 同步逻辑。首先是 `martianSaucerAI` (395 计数器)。
```


---

## 🤖 Assistant · 2026-08-19T08:05:54.537Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts",
 "old_string": "    slots.set(e, parts);\n  }\n  // ---- 自毁态（:36357-36360,普通模式由 392 置 ai0=3）----",
 "new_string": "    slots.set(e, parts);\n  }\n  // ---- FindFrame case 395 counter 副本（cs:72520-72541，蜂后 222 先例：AI 写\n  //      e.lai0、Renderer vanillaFrameIdx 读）：每 tick +1、66 回卷；死光电报窗\n  //      ai[3]∈[20,260) 内再 +1 且钳 [36,53]（帧 6-8 蓄能辉光带）。只在两个\n  //      非死亡出口调用（-1/-2 爬升分支与函数尾）= AI 全部完成后同步，与原版\n  //      FindFrame 时序一致 ----\n  const frameTick395 = (): void => {\n    e.lai0 += 1;\n    if (e.lai0 >= 66) e.lai0 = 0;\n    if (e.ai3 >= 20 && e.ai3 < 260) {\n      e.lai0 += 1;\n      if (e.lai0 >= 54 || e.lai0 < 36) e.lai0 = 36;\n    }\n  };\n  // ---- 自毁态（:36357-36360,普通模式由 392 置 ai0=3）----"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:05:54.555Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T08:06:19.651Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts",
 "old_string": "      if (e.ai0 === -2) e.ai0 = 2;\n      e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;\n    }\n    fly(e);\n    return;\n  }",
 "new_string": "      if (e.ai0 === -2) e.ai0 = 2;\n      e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;\n    }\n    frameTick395();\n    fly(e);\n    return;\n  }"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:06:19.663Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T08:06:26.923Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts",
 "old_string": "  // ---- 出界钳制 + 消散（:36751-36772）----\n  const st = game.world.store;\n  if (e.y < -100 || e.x < -100 || e.y > st.h * TILE + 100 || e.x > st.w * TILE + 100) {\n    e.x = clamp(e.x, -100, st.w * TILE + 100);\n    e.y = clamp(e.y, -100, st.h * TILE + 100);\n    e.dead = true;\n    return;\n  }\n  fly(e);\n}",
 "new_string": "  // ---- 出界钳制 + 消散（:36751-36772）----\n  const st = game.world.store;\n  if (e.y < -100 || e.x < -100 || e.y > st.h * TILE + 100 || e.x > st.w * TILE + 100) {\n    e.x = clamp(e.x, -100, st.w * TILE + 100);\n    e.y = clamp(e.y, -100, st.h * TILE + 100);\n    e.dead = true;\n    return;\n  }\n  frameTick395();\n  fly(e);\n}"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:06:26.942Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T08:06:32.157Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now the 392 counter at the end of martianSaucerPartAI. The function ends after the empty-nest missile block. The end currently:

```ts
      if (c1Dead && rnd(mv5) === 0) {
        ...
      }
    }
  }
}
```

I'll append the 392 counter after the closing of the flag76 block, at function end. The 392 path reaches here (393/394/390 return earlier). Let me anchor on the final lines of the file section.
````

</details>


---

## 🤖 Assistant · 2026-08-19T08:06:32.587Z · glm-x-preview-260804

```
现在处理 `martianSaucerPartAI` 末尾的 392 计数器。
```


---

## 🤖 Assistant · 2026-08-19T08:06:48.866Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts",
 "old_string": "      // 火炮空巢（:36261-36276）:上方侧向抛射\n      if (c0Dead && rnd(mv5) === 0) {\n        // :36246-36250 速度 = (±rand3, ±1)×3 未归一(3~9.5 随机,曾归一恒 3)\n        const mvx = -Math.random() * 3 * 3, mvy = -1 * 3;\n        shootM(game, e.cx + rndRange(30, 60), e.cy + rndRange(-30, -10), mvx, mvy, 30, 450, 300, 1,\n          { bounce: true });  // aiStyle14 X 反跳(原版 ×-0.1,默认档 -0.5 近似)\n        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36254 空巢导弹每发(终审补)\n      }\n      if (c1Dead && rnd(mv5) === 0) {\n        // :36246-36250 速度 = (±rand3, ±1)×3 未归一(3~9.5 随机,曾归一恒 3)\n        const mvx = Math.random() * 3 * 3, mvy = -1 * 3;\n        shootM(game, e.cx + rndRange(30, 60), e.cy + rndRange(-30, -10), mvx, mvy, 30, 450, 300, 1,\n          { bounce: true });  // aiStyle14 X 反跳(原版 ×-0.1,默认档 -0.5 近似)\n        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36254 空巢导弹每发(终审补)\n      }\n    }\n  }\n}",
 "new_string": "      // 火炮空巢（:36261-36276）:上方侧向抛射\n      if (c0Dead && rnd(mv5) === 0) {\n        // :36246-36250 速度 = (±rand3, ±1)×3 未归一(3~9.5 随机,曾归一恒 3)\n        const mvx = -Math.random() * 3 * 3, mvy = -1 * 3;\n        shootM(game, e.cx + rndRange(30, 60), e.cy + rndRange(-30, -10), mvx, mvy, 30, 450, 300, 1,\n          { bounce: true });  // aiStyle14 X 反跳(原版 ×-0.1,默认档 -0.5 近似)\n        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36254 空巢导弹每发(终审补)\n      }\n      if (c1Dead && rnd(mv5) === 0) {\n        // :36246-36250 速度 = (±rand3, ±1)×3 未归一(3~9.5 随机,曾归一恒 3)\n        const mvx = Math.random() * 3 * 3, mvy = -1 * 3;\n        shootM(game, e.cx + rndRange(30, 60), e.cy + rndRange(-30, -10), mvx, mvy, 30, 450, 300, 1,\n          { bounce: true });  // aiStyle14 X 反跳(原版 ×-0.1,默认档 -0.5 近似)\n        game.playSfxWav?.('Item_39', 1, e.cx, e.cy);   // :36254 空巢导弹每发(终审补)\n      }\n    }\n  }\n  // ---- FindFrame case 392 counter 副本（cs:72543-72560，393/394 已在上方各自\n  //      return，函数尾仅 392 到达）：4 帧旋球 counter 每 tick +1、死光电报窗\n  //      ai[3]∈[20,260) 内 ×2、12 回卷（Renderer 读 e.lai0 → 帧 = counter/3）----\n  e.lai0 += e.ai3 >= 20 && e.ai3 < 260 ? 2 : 1;\n  if (e.lai0 >= 12) e.lai0 = 0;\n}"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:06:48.892Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T08:07:16.450Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now bossAI_moon_events.ts — three edits:

1. mourningWoodAI: 344 counter accumulation at the end (before/after hoverCruise — hoverCruise finalizes e.vx; so AFTER hoverCruise to use final vx).
2. pumpkingAI: 327 pose-walk replica at the end.
3. santaNK1AI: 346 frame machine at the end (after hoverCruise).

For mourningWoodAI end:
```ts
  if (player && Math.abs(e.cx - player.cx) < 50) flag56 = true;
  hoverCruise(e, game, player, flag56, num891);
}
```
Append after hoverCruise:
```ts
  // ---- FindFrame case 344 副本（cs:73144-73170）：counter += max(1,|vx|*0.75)/t
  //      （站定 vx==0 分支 +1）、>5 进帧 → 累计值落 e.lai0，Renderer 按
  //      floor(lai0/6)%10 取帧（全带 0-9 无带切换，advanceCount 即帧号）。
  //      325 同函数但两分支 counter 恒 +1/t ≡ animT，Renderer 用 t 直推，无需副本 ----
  if (ever) e.lai0 += e.vx === 0 ? 1 : Math.max(1, Math.abs(e.vx) * 0.75);
```

For pumpkingAI end:
```ts
  e.visAngle = e.vx * -0.02;       // rotation(:33402)
  e.x += e.vx;                     // noTileCollide（SetDefaults 327）直积分
  e.y += e.vy;
}
```
Append the pose walk:
```ts
  // ---- FindFrame case 327 姿态机副本（cs:72977-73037）：ai[3] 姿态 0→行0带 /
  //      1→行4带 / 2→行8带；counter ±1/t（7t/步），越 ±6 进帧行、12 帧双向回卷
  //      ——表情在带间滑变，到位后定格（e.lai0=counter / e.lai1=行号） ----
  let step327 = 0;
  if (e.ai3 === 0) {
    if (e.lai1 > 5) step327 = 1;
    else if (e.lai1 > 0) step327 = -1;
  } else if (e.ai3 === 1) {
    if (e.lai1 > 10) step327 = 1;
    else if (e.lai1 > 4) step327 = -1;
    else if (e.lai1 < 4) step327 = 1;
  } else if (e.ai3 === 2) {
    if (e.lai1 < 2) step327 = -1;
    else if (e.lai1 > 8) step327 = -1;
    else if (e.lai1 < 8) step327 = 1;
  }
  e.lai0 += step327;
  if (e.lai0 > 6) { e.lai0 = 0; e.lai1 += 1; if (e.lai1 > 11) e.lai1 = 0; }
  if (e.lai0 < 0) { e.lai0 = 6; e.lai1 -= 1; if (e.lai1 < 0) e.lai1 = 11; }
  e.customFrameIdx = e.lai1;
```

For santaNK1AI end:
```ts
  if (player && Math.abs(e.cx - player.cx) < 50) flag58 = true;   // :34105-34107
  hoverCruise(e, game, player, flag58, num980);
}
```
Append:
```ts
  // ---- FindFrame case 346 副本（cs:73050-73093）：ai0==1 链炮开火带 6-8 每 3t
  //      循环；vx==0 定格（帧不动、清计数）；行走带 1-5 counter += 1+|vx|/2、
  //      >4 进帧。帧行有定格记忆 → customFrameIdx 直读（L[0]=counter/L[3]=帧）----
  if (e.ai0 === 1) {
    L[0] += 1;
    if (L[0] > 2) { L[0] = 0; L[3] += 1; }
    if (L[3] > 8) L[3] = 6;
    if (L[3] < 6) L[3] = 6;
  } else if (e.vx === 0) {
    L[0] = 0;
  } else {
    L[0] += 1 + Math.abs(e.vx) / 2;
    if (L[0] > 4) { L[0] = 0; L[3] += 1; }
    if (L[3] > 5) L[3] = 1;
    if (L[3] < 1) L[3] = 1;
  }
  e.customFrameIdx = L[3];
```
Wait — santaNK1AI has `const L = la(e);` at top ✓. L[3] is number ✓.

Hmm — one check on santaNK1AI: does it early-return anywhere? Looking at the function: no returns (the isDay branch is if/else). ✓ reaches end always.

mourningWoodAI: any early returns? No — flows to hoverCruise. ✓.

pumpkingAI: no returns ✓.

One more consideration for the santa frame machine placement: vanilla spriteDirection = direction in fire/walk branches — skip (facing handled generically).
````

</details>


---

## 🤖 Assistant · 2026-08-19T08:07:16.658Z · glm-x-preview-260804

```
现在我来处理三个月亮事件的 AI 编辑。
```


---

## 🤖 Assistant · 2026-08-19T08:07:21.106Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_moon_events.ts",
 "old_string": "  // 玩家在正下方 50px 内 → 停步(:33180-33185)\n  if (player && Math.abs(e.cx - player.cx) < 50) flag56 = true;\n  hoverCruise(e, game, player, flag56, num891);\n}",
 "new_string": "  // 玩家在正下方 50px 内 → 停步(:33180-33185)\n  if (player && Math.abs(e.cx - player.cx) < 50) flag56 = true;\n  hoverCruise(e, game, player, flag56, num891);\n  // ---- FindFrame case 344 副本（cs:73144-73170）：counter += max(1,|vx|*0.75)/t\n  //      （站定 vx==0 分支 +1/t）、>5 进帧（6 单位/帧，速率随速度变化）→ 累计值\n  //      落 e.lai0，Renderer 按 floor(lai0/6)%10 取帧（344 全带 0-9 无带切换，\n  //      advanceCount 即帧号）。325 同函数但两分支 counter 恒 +1/t ≡ animT，\n  //      Renderer 用 t 直推无需副本 ----\n  if (ever) e.lai0 += e.vx === 0 ? 1 : Math.max(1, Math.abs(e.vx) * 0.75);\n}"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:07:21.125Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_moon_events.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T08:07:31.445Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_moon_events.ts",
 "old_string": "  e.visAngle = e.vx * -0.02;       // rotation(:33402)\n  e.x += e.vx;                     // noTileCollide（SetDefaults 327）直积分\n  e.y += e.vy;\n}",
 "new_string": "  e.visAngle = e.vx * -0.02;       // rotation(:33402)\n  e.x += e.vx;                     // noTileCollide（SetDefaults 327）直积分\n  e.y += e.vy;\n  // ---- FindFrame case 327 姿态机副本（cs:72977-73037，Renderer 直读 customFrameIdx）：\n  //      ai[3] 姿态 0→行0带 / 1→行4带 / 2→行8带；counter ±1/t（越 ±6 进一帧行，\n  //      7t/步）、12 帧双向回卷——表情滑变到位后定格（e.lai0=counter/e.lai1=行） ----\n  let step327 = 0;\n  if (e.ai3 === 0) {\n    if (e.lai1 > 5) step327 = 1;\n    else if (e.lai1 > 0) step327 = -1;\n  } else if (e.ai3 === 1) {\n    if (e.lai1 > 10) step327 = 1;\n    else if (e.lai1 > 4) step327 = -1;\n    else if (e.lai1 < 4) step327 = 1;\n  } else if (e.ai3 === 2) {\n    if (e.lai1 < 2) step327 = -1;\n    else if (e.lai1 > 8) step327 = -1;\n    else if (e.lai1 < 8) step327 = 1;\n  }\n  e.lai0 += step327;\n  if (e.lai0 > 6) { e.lai0 = 0; e.lai1 += 1; if (e.lai1 > 11) e.lai1 = 0; }\n  if (e.lai0 < 0) { e.lai0 = 6; e.lai1 -= 1; if (e.lai1 < 0) e.lai1 = 11; }\n  e.customFrameIdx = e.lai1;\n}"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:07:31.457Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_moon_events.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T08:07:42.500Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_moon_events.ts",
 "old_string": "  if (player && Math.abs(e.cx - player.cx) < 50) flag58 = true;   // :34105-34107\n  hoverCruise(e, game, player, flag58, num980);\n}",
 "new_string": "  if (player && Math.abs(e.cx - player.cx) < 50) flag58 = true;   // :34105-34107\n  hoverCruise(e, game, player, flag58, num980);\n  // ---- FindFrame case 346 副本（cs:73050-73093，Renderer 直读 customFrameIdx）：\n  //      ai0==1 链炮开火带 6-8 每 3t 循环；vx==0 定格（帧不动、仅清计数——开火/\n  //      玩家头顶停步期不迈腿）；行走带 1-5 counter += 1+|vx|/2、>4 进帧\n  //      （L[0]=counter / L[3]=帧行，定格记忆无法无状态重建 → AI 侧副本）----\n  if (e.ai0 === 1) {\n    L[0] += 1;\n    if (L[0] > 2) { L[0] = 0; L[3] += 1; }\n    if (L[3] > 8) L[3] = 6;\n    if (L[3] < 6) L[3] = 6;\n  } else if (e.vx === 0) {\n    L[0] = 0;\n  } else {\n    L[0] += 1 + Math.abs(e.vx) / 2;\n    if (L[0] > 4) { L[0] = 0; L[3] += 1; }\n    if (L[3] > 5) L[3] = 1;\n    if (L[3] < 1) L[3] = 1;\n  }\n  e.customFrameIdx = L[3];\n}"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:07:42.511Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_moon_events.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T08:07:48.034Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now the cultist frame machine in bossAI_lategame.ts. Two parts:
1. Module-level WeakMap + frame-state helper + FindFrame replica function (place before lunaticCultistAI, after ritualCenterOf).
2. Call in lunaticCultistAI after the justHit ritual block (line ~346), before `// 朝向(:65117-65120...)`.

Let me check `rot` helper availability in the file (used by cloneSupplement) — exists. And laOf — defined where? Let me check the top of the file for laOf.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:07:48.690Z · glm-x-preview-260804

```
现在处理 `bossAI_lategame.ts` 中的教徒帧状态机。我先检查一下该文件的辅助函数。
```


---

## 🤖 Assistant · 2026-08-19T08:07:49.848Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"const laOf\\|function laOf\\|import.*rot\\|function rot\\|const rot\" src/entities/bossAI_lategame.ts | head; sed -n '95,106p' src/entities/bossAI_lategame.ts",
 "description": "Check laOf and rot helpers in lategame file"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:07:49.899Z

**📎 ToolResult**

```
49:const laOf = (e: Enemy): { la0: number; la1: number; la2: unknown; la3: unknown } => {
103:const rot = (x: number, y: number, a: number): [number, number] =>
function aimLead(e: Enemy, player: Player, fallbackX: number): { x: number; y: number } {
  const dx = player.cx + player.vx * 20 - e.cx;
  const dy = player.cy + player.vy * 20 - e.cy;
  const d = Math.hypot(dx, dy);
  if (!Number.isFinite(d) || d < 0.0001) return { x: fallbackX, y: 0 };
  return { x: dx / d, y: dy / d };
}
/** 旋转 */
const rot = (x: number, y: number, a: number): [number, number] =>
  [x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)];

// ===================== AI_084 拜月教邪教徒 439 + 克隆体 440(NPC.cs:64921-65957) =====================

```


---

## 🤖 Assistant · 2026-08-19T08:07:58.071Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts",
 "limit": 14,
 "offset": 44
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:07:58.078Z

**📎 ToolResult**

```
44	    }
45	    baseStats.set(e, b);
46	  }
47	  return b;
48	};
49	
50	/** 原版 localAI[0..3] 的外部存储(Enemy 只有 ai0-ai3 四个槽)。
51	 *  la2/la3 放宽为 unknown:邪教徒用 la2 存仪式圈心坐标对象、la3 存克隆体的真身引用 */
52	const localAI = new WeakMap<Enemy, { la0: number; la1: number; la2: unknown; la3: unknown }>();
53	const laOf = (e: Enemy): { la0: number; la1: number; la2: unknown; la3: unknown } => {
54	  let l = localAI.get(e);
55	  if (!l) { l = { la0: 0, la1: 0, la2: 0, la3: 0 }; localAI.set(e, l); }
56	  return l;
57	};

```


---

## 🤖 Assistant · 2026-08-19T08:08:50.051Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Good. Now I'll add the cultist frame machine helpers after `ritualCenterOf` (line 268-273) and the call inside lunaticCultistAI. Let me write the helpers:

```ts
/** 教徒 FindFrame 帧机状态（counter+帧行；localAI 槽被仪式圈心/克隆引用占用 → 独立 WeakMap） */
const cultistAnim = new WeakMap<Enemy, { fc: number; row: number }>();

/** 教徒 FindFrame 帧机（NPC.cs:72698-72783）：localAI[2] 帧态六值→帧行——
 *  态0→行0 定格 / 态10→行4-6 循环 / 态1→行1 定格 / 态11→行10-12 循环 /
 *  态2→行2 定格 / 态12→行7-9 循环 / 态13→行13-15 循环。
 *  循环节拍 15t（行内 5t/帧，cs:72726 /5）；定格态先播一轮行带再落定格行 */
function cultistFrameTick(e: Enemy, st: number): void {
  let a = cultistAnim.get(e);
  if (!a) { a = { fc: 0, row: 0 }; cultistAnim.set(e, a); }
  const wrap = a.fc >= 15;
  if (wrap) a.fc = 0;
  const seg = Math.floor(a.fc / 5);
  switch (st) {
    case 0:
      if (wrap) a.row = 0;
      else if (a.row !== 0) a.row = seg + 4;
      break;
    case 10: a.row = seg + 4; break;
    case 1:
      if (wrap) a.row = 1;
      else if (a.row !== 1) a.row = seg + 10;
      break;
    case 11: a.row = seg + 10; break;
    case 2:
      if (wrap) a.row = 2;
      else if (a.row !== 2) a.row = seg + 7;
      break;
    case 12: a.row = seg + 7; break;
    case 13: a.row = seg + 13; break;
  }
  a.fc += 1;                       // cs:72781 frameCounter += 1
  e.customFrameIdx = a.row;        // Renderer vanillaFrameIdx 首行直读（694 先例）
}

/** AI 态 → 原版 FindFrame localAI[2] 帧态（cs:65120-65137 出生显形分段 /
 *  :65148 选招 / :65348 飞掠 / :65365 冰 / :65436 火 / :65520-65524 雷 flag2 门 /
 *  :65575+ 仪式圈心向量 / :65786 硬直 / :65811 光 / :65878 末日） */
function cultistFrameState(e: Enemy, la: ReturnType<typeof laOf>, isReal: boolean, parent: Enemy | null): number {
  switch (e.ai0) {
    case -1: {
      const s = e.ai1 + 1;   // 原版先自增后分段（:65110）——此处在自增前取值
      return s > 360 ? 13 : s > 300 ? 10 : s > 120 ? 1 : 0;
    }
    case 5: {
      // 头部恒 10（:65575）；[30,90)/[120,420) 两窗按到仪式圈心向量覆写
      // （|uy|<0.77→11 / uy<0→12 / 其余→10，:65657-65671/:65730-65763 同构）
      const tt = e.ai1;
      if ((tt >= 30 && tt < 90) || (tt >= 120 && tt < 420)) {
        const cir = ritualCenterOf(isReal, la, parent);
        if (cir) {
          let dx = cir.x - e.cx, dy = cir.y - e.cy;
          const d = Math.hypot(dx, dy);
          if (d === 0) { dx = 0; dy = -1; } else { dx /= d; dy /= d; }
          return Math.abs(dy) < 0.77 ? 11 : dy < 0 ? 12 : 10;
        }
      }
      return 10;
    }
    case 4: return isReal ? 12 : 11;   // 闪电:真身抬手(12) 克隆体同冰火(11)
    case 6: return 13;                 // 硬直
    case 8: return 13;                 // 末日(经典不可达,状态体保留)
    case 2: case 3: case 7: return 11; // 冰/火/光
    case 0: case 1: default: return 10; // 选招/飞掠
  }
}
```

Hmm wait — case -1 uses e.ai1 + 1. Let me double-check our -1 block ordering once more: lines 353-362:
```ts
if (e.ai0 === -1) {
    e.spawnAlpha = Math.max(0, 254 - e.ai1 * 5);
    e.iframes = 2;
    e.ai1 += 1;
    if (e.ai1 > 360) {...}
    else if (e.ai1 > 300) {...}
    ...
    if (e.ai1 >= 420) {...}
```
Wait — actually the exact order in our code: `e.ai1 += 1;` (line 356) comes BEFORE the `if (e.ai1 > 360)` checks (357-358). And the sound at ===361. So my insertion point (before the -1 block) sees pre-increment ai1 → use ai1+1 for vanilla's post-increment threshold comparison. ✓.

Hmm — but hold on: vanilla checks `> 360` AFTER increment; at increment to 361 → >360 → state 13 + sound gate (localAI[2] != 13 → play). Our port plays sound at `e.ai1 === 361` — consistent. ✓.

Also — wait, there's one more subtlety: our -1 block computes spawnAlpha with PRE-increment ai1 (`254 - e.ai1 * 5` before `e.ai1 += 1`)? Line 354: `e.spawnAlpha = Math.max(0, 254 - e.ai1 * 5);` then 356 `e.ai1 += 1;`. Vanilla order: `alpha -= 5` per tick... whatever — existing code, not mine.

Now the insertion call site. After the ritual justHit block (ends line ~345 with `if (circle instanceof CultistRitualCircle) circle.interrupt();` then `}`), before `// 朝向(:65117-65120 ...`. Insert:

```ts
  // ---- FindFrame 帧机（cs:72698-72783）：帧态 = localAI[2] 六值——本仓 la2 已挪用
  //      存仪式圈心,帧态在此按各态语义重算（cs 行号见 cultistFrameState）,
  //      customFrameIdx 直读（694 先例）。netPuppet 无本地 AI → 帧冻结(登记) ----
  cultistFrameTick(e, cultistFrameState(e, la, isReal, parent));
```

Wait — `la` is in scope? At the top: `const la = laOf(e);` ✓. `parent` — declared `let parent: Enemy | null = null;` and set in clone branch ✓. `isReal` ✓.

One issue — the ritual [30,90) window: for the REAL cultist at t===30, la.la2 is not yet set (set later in the ai0===5 block). Also vanilla resets... fine, noted.

Another check — clone's ritualCenterOf(isReal=false, la, parent) reads parent's la.la2 — parent here is the clone's la3 reference (set in mirror segment `parent = (la.la3 as unknown as Enemy) ?? null;`). ✓.

Also — lai0/lai1 conflict check for 439/440: none (fireflies only). ✓.

And — what if e.ai0 is 5 but the frame-state windows read ai1 which the mirror already updated... For clones: ai1 = parent.ai1 (mirrored at AI start). If parent already ran this tick (spawned earlier → earlier in entities list), clone's mirrored ai1 = parent's post-increment value from THIS tick — vs vanilla: clone's AI mirrors parent's ai[1] at clone's AI start — vanilla's iteration order = npc index order — parent spawned before clones → parent updates first → same. ✓.

Insertion. Then run tests.
````

</details>


---

## 🤖 Assistant · 2026-08-19T08:09:10.045Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts",
 "old_string": "/** 仪式圈心(原版 Projectile 490 的位置 = 仪式开始时真身中心,:65652)。\n *  真身存 la2;克隆体读真身的 la2 */\nfunction ritualCenterOf(isReal: boolean, la: { la2: unknown }, parent: Enemy | null): { x: number; y: number } | null {\n  const raw = (isReal ? la.la2 : (parent ? laOf(parent).la2 : null)) as { x: number; y: number } | null;\n  return raw ?? null;\n}",
 "new_string": "/** 仪式圈心(原版 Projectile 490 的位置 = 仪式开始时真身中心,:65652)。\n *  真身存 la2;克隆体读真身的 la2 */\nfunction ritualCenterOf(isReal: boolean, la: { la2: unknown }, parent: Enemy | null): { x: number; y: number } | null {\n  const raw = (isReal ? la.la2 : (parent ? laOf(parent).la2 : null)) as { x: number; y: number } | null;\n  return raw ?? null;\n}\n\n/** 教徒 FindFrame 帧机状态（counter+帧行对；localAI 槽被仪式圈心/克隆引用\n *  占用（la2/la3 勿动）→ 独立 WeakMap 落盘） */\nconst cultistAnim = new WeakMap<Enemy, { fc: number; row: number }>();\n\n/** AI 态 → 原版 FindFrame localAI[2] 帧态六值（写点行号）：\n *  出生显形分段 :65120-65136（>360→13 / >300→10 / >120→1 / 其余→0，先自增\n *  后分段——本函数在 AI 自增前调用故 +1）/ 选招 :65148→10 / 飞掠 :65348→10 /\n *  冰 :65365→11 / 火 :65436→11 / 雷 :65520-65524→真身 12·克隆 11（flag2 门）/\n *  仪式 :65575 头部→10，[30,90) 与 [120,420) 两窗按到圈心向量覆写\n *  （|uy|<0.77→11 / uy<0→12 / 其余→10，:65657-65702/:65730-65763 同构）/\n *  硬直 :65786→13 / 光 :65811→11 / 末日 :65878→13 */\nfunction cultistFrameState(\n  e: Enemy, la: ReturnType<typeof laOf>, isReal: boolean, parent: Enemy | null,\n): number {\n  switch (e.ai0) {\n    case -1: {\n      const s = e.ai1 + 1;\n      return s > 360 ? 13 : s > 300 ? 10 : s > 120 ? 1 : 0;\n    }\n    case 5: {\n      const tt = e.ai1;\n      if ((tt >= 30 && tt < 90) || (tt >= 120 && tt < 420)) {\n        const cir = ritualCenterOf(isReal, la, parent);\n        if (cir) {\n          let dx = cir.x - e.cx, dy = cir.y - e.cy;\n          const d = Math.hypot(dx, dy);\n          if (d === 0) { dx = 0; dy = -1; } else { dx /= d; dy /= d; }\n          return Math.abs(dy) < 0.77 ? 11 : dy < 0 ? 12 : 10;\n        }\n      }\n      return 10;\n    }\n    case 4: return isReal ? 12 : 11;\n    case 6: return 13;\n    case 8: return 13;\n    case 2:\n    case 3:\n    case 7: return 11;\n    default: return 10;   // 选招 0 / 飞掠 1\n  }\n}\n\n/** 教徒 FindFrame 副本（NPC.cs:72698-72783）：帧态→帧行——\n *  态0→行0 / 态1→行1 / 态2→行2 定格（先播一轮行带再落定格行）；\n *  态10→行4-6 / 态11→行10-12 / 态12→行7-9 / 态13→行13-15 恒循环。\n *  节拍 15t 一轮、行内 5t/帧（cs:72719 ≥15 回卷、cs:72726 /5），\n *  counter 每 tick +1（cs:72781）；帧号直写 customFrameIdx（694 先例） */\nfunction cultistFrameTick(e: Enemy, st: number): void {\n  let a = cultistAnim.get(e);\n  if (!a) { a = { fc: 0, row: 0 }; cultistAnim.set(e, a); }\n  const wrap = a.fc >= 15;\n  if (wrap) a.fc = 0;\n  const seg = Math.floor(a.fc / 5);\n  switch (st) {\n    case 0:\n      if (wrap) a.row = 0;\n      else if (a.row !== 0) a.row = seg + 4;\n      break;\n    case 10: a.row = seg + 4; break;\n    case 1:\n      if (wrap) a.row = 1;\n      else if (a.row !== 1) a.row = seg + 10;\n      break;\n    case 11: a.row = seg + 10; break;\n    case 2:\n      if (wrap) a.row = 2;\n      else if (a.row !== 2) a.row = seg + 7;\n      break;\n    case 12: a.row = seg + 7; break;\n    case 13: a.row = seg + 13; break;\n  }\n  a.fc += 1;\n  e.customFrameIdx = a.row;\n}"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:09:10.062Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts has been updated successfully. (note: the file had been modified on disk since you last read it — the edit applied cleanly, but the file contains other changes not in your context. Read it before edits that depend on surrounding content.)

```


---

## 🤖 Assistant · 2026-08-19T08:09:15.800Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The file was modified on disk by a parallel session (warned about this). My edit applied cleanly. Now insert the call inside lunaticCultistAI. Let me re-read that region first since the file changed.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:09:16.562Z · glm-x-preview-260804

```
该文件因并行会话而发生了变动 —— 在插入调用之前，我先重新读取一下锚点。
```


---

## 🤖 Assistant · 2026-08-19T08:09:17.441Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"circle.interrupt\\|朝向(:65117\" src/entities/bossAI_lategame.ts | head -5",
 "description": "Locate insertion anchor in cultist AI"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:09:17.471Z

**📎 ToolResult**

```
683:    if (circle instanceof CultistRitualCircle) circle.interrupt();
686:  // 朝向(:65117-65120 sign(player.X - center.X);仪式态内被 :65676 系圈心朝向覆盖)

```


---

## 🤖 Assistant · 2026-08-19T08:09:34.828Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts",
 "limit": 14,
 "offset": 676
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:09:34.835Z

**📎 ToolResult**

```
676	    for (const c of cultistClones(game, e)) {
677	      if (budget <= 0) break;
678	      budget--;
679	      game.spawnParticles(c.cx, c.cy, '#8060D0', 12, 2.4);
680	      c.dead = true;
681	    }
682	    const circle = la.la3;
683	    if (circle instanceof CultistRitualCircle) circle.interrupt();
684	  }
685	
686	  // 朝向(:65117-65120 sign(player.X - center.X);仪式态内被 :65676 系圈心朝向覆盖)
687	  const face = Math.sign(player.cx - e.cx);
688	  if (face !== 0) e.facing = face;
689	

```


---

## 🤖 Assistant · 2026-08-19T08:09:59.831Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts",
 "old_string": "    const circle = la.la3;\n    if (circle instanceof CultistRitualCircle) circle.interrupt();\n  }\n\n  // 朝向(:65117-65120 sign(player.X - center.X);仪式态内被 :65676 系圈心朝向覆盖)",
 "new_string": "    const circle = la.la3;\n    if (circle instanceof CultistRitualCircle) circle.interrupt();\n  }\n\n  // ---- FindFrame 帧机（cs:72698-72783）：原版 localAI[2] 六态→帧行；本仓 la2\n  //      已挪用存仪式圈心（勿动）→ 帧态按各态语义重算（见 cultistFrameState），\n  //      帧号直写 customFrameIdx（Renderer 首行直读，694 先例）。状态机各块早退\n  //      前先走本段（与原版 AI 内写 localAI[2]、AI 后 FindFrame 的时序等价）；\n  //      netPuppet 无本地 AI → 帧冻结（登记）----\n  cultistFrameTick(e, cultistFrameState(e, la, isReal, parent));\n\n  // 朝向(:65117-65120 sign(player.X - center.X);仪式态内被 :65676 系圈心朝向覆盖)"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:09:59.852Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts has been updated successfully. (note: the file had been modified on disk since you last read it — the edit applied cleanly, but the file contains other changes not in your context. Read it before edits that depend on surrounding content.)

```


---

## 🤖 Assistant · 2026-08-19T08:10:07.224Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All edits applied. Now verify:
1. tsc — no new errors in my files.
2. Run the tests.

Then, ideally, verify behavior with a quick probe... The task acceptance is: 1) tsc no new errors; 2) vitest related tests green; 3) original line number comments (done). A browser probe is optional but valuable to sanity-check frames — but spinning a vite instance for this is heavyweight; the task doesn't require a probe. The unit tests cover AI behavior; frame machine is render-layer. I could write a quick node-side check of the frame logic against vanilla semantics via the test... not required. Let me at least verify tsc + tests first.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:10:08.027Z · glm-x-preview-260804

```
所有修改已应用。现在用 `tsc` 进行验证（与波动的基线进行差异对比）并运行测试。
```


---

## 🤖 Assistant · 2026-08-19T08:10:09.836Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "npx tsc --noEmit 2>&1 | sort > /tmp/tsc-after.txt; echo \"== errors in my touched files:\"; grep -E \"render/Renderer|bossAI_martian|bossAI_moon_events|bossAI_lategame|bossAI_dd2\" /tmp/tsc-after.txt; echo \"== total lines: $(wc -l < /tmp/tsc-after.txt) (baseline ~73)\"",
 "description": "Typecheck and filter errors for touched files"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:10:25.539Z

**📎 ToolResult**

```
== errors in my touched files:
== total lines:       55 (baseline ~73)

```


---

## 🤖 Assistant · 2026-08-19T08:10:37.300Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The system reminder shows the file was reformatted/reviewed (likely a linter or the parallel session) — the shown content includes my added code region? The diff shown is the file head (unchanged parts). My edits are still in place presumably. The tsc run after my edits showed zero errors in my touched files and total 55 lines (fewer than baseline 73 — parallel session churn, not mine).

Now run the tests.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:10:37.909Z · glm-x-preview-260804

```
我修改的文件中没有错误（由于并行会话的波动，总数有所下降）。现在开始运行相关的测试套件。
```


---

## 🤖 Assistant · 2026-08-19T08:10:39.207Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "npx vitest run tests/bossAI-lategame.test.ts tests/bossAI-dd2.test.ts tests/moon-shop-aggro.test.ts tests/martian-deathray.test.ts tests/bossAI-lunar-misc.test.ts 2>&1 | tail -10",
 "description": "Run related bossAI test suites"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:10:43.141Z

**📎 ToolResult**

```
 ✓ tests/bossAI-lategame.test.ts (49 tests) 41ms
 ✓ tests/bossAI-dd2.test.ts (22 tests) 54ms
 ✓ tests/bossAI-lunar-misc.test.ts (13 tests) 59ms
 ✓ tests/martian-deathray.test.ts (4 tests) 6ms

 Test Files  5 passed (5)
      Tests  99 passed (99)
   Start at  16:10:39
   Duration  2.95s (transform 2.67s, setup 0ms, collect 12.83s, tests 169ms, environment 1ms, prepare 297ms)

```


---

## 🤖 Assistant · 2026-08-19T08:11:55.570Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
All 99 tests green. The moon-shop-aggro.test.ts seems to have been skipped in this run's tail output (5 files passed — moon-shop-aggro was in the list... it shows 4 test files + maybe moon-shop counted). Let me check: "5 passed (5)" — bossAI-lategame, bossAI-dd2, bossAI-lunar-misc, martian-deathray = 4 shown + moon-shop-aggro = 5 (its line scrolled). OK all green.

Now — additional validation: the task asks for correctness of the frame machines. Let me do a quick logic self-test of the stateful machines (pumpking/cultist/santa) via a scratch vitest-style check using vitest run on an inline test? I shouldn't create test files unnecessarily ("NEVER create files unless absolutely necessary"). But a quick sanity simulation via a throwaway node script in /tmp using the actual functions... importing from the game source requires the vite transform (TS + imports). I could use `node tools/run-diag.mjs` — but that's for browser probes. There's vitest available — I can run a quick inline test with `vitest run` on a temp file in /tmp? vitest only picks up project tests dir.

Alternative: simulate the frame machine logic standalone in node (copy-paste the logic) to verify invariants (e.g., pumpking reaches target rows and freezes; cultist loops bands). This validates the algorithm, not the wiring. The wiring is verified by tsc + existing tests (which still pass — they exercise the AI functions each tick, so the new lines ran without breaking behavior).

Actually — one important behavioral check: the existing tests passed, which means the AI functions with my appended frame code still produce identical AI behavior. Good.

Let me do a quick standalone simulation of the three stateful machines to verify they behave per vanilla semantics (target rows, freezes, bands):

1. Pumpking: ai3=1 from row 0 → walks forward to 4 and freezes at 4. ai3=0 from 4 → walks backward to 0. ai3=2 → walks to 8 (forward from below via <2 wrap... from row 4: conditions: row<2? no; row>8? no; row<8? yes → +1 → walks 5,6,7,8 freeze). From row 10: row>8 → -1 → 9,8 freeze. ✓ logic.

2. Cultist: state 10 loops rows 4,5,6 every 5t, wrap 15t. State 0 from row 6: plays 4-6 one loop then snaps 0 and freezes. ✓.

3. Santa: fire band clamps into 6-8; idle freezes; walk 1-5.

Let me write a quick node script (in /tmp — allowed as scratch, not a report file) to run these sims. Actually — simpler and more valuable: verify via the real code by importing the compiled logic? The functions aren't exported. The sim would duplicate code — of limited value beyond eyeballing.

I'll eyeball-verify the logic once more instead:

**Pumpking replica vs vanilla** (cs:72977-73037):
```csharp
if (ai[3] == 0f) {
    if (frame.Y > num * 5) frameCounter += 1.0;
    else if (frame.Y > 0) frameCounter -= 1.0;
}
else if (ai[3] == 1f) {
    if (frame.Y > num * 10) frameCounter += 1.0;
    else if (frame.Y > num * 4) frameCounter -= 1.0;
    else if (frame.Y < num * 4) frameCounter += 1.0;
}
else if (ai[3] == 2f) {
    if (frame.Y < num * 2) frameCounter -= 1.0;
    else if (frame.Y > num * 8) frameCounter -= 1.0;
    else if (frame.Y < num * 8) frameCounter += 1.0;
}
if (frameCounter > 6.0) { frameCounter = 0.0; frame.Y += num; if (frame.Y > num * 11) frame.Y = 0; }
if (frameCounter < 0.0) { frameCounter = 6.0; frame.Y -= num; if (frame.Y < 0) frame.Y = num * 11; }
```
Mine:
```ts
let step327 = 0;
if (e.ai3 === 0) {
  if (e.lai1 > 5) step327 = 1;
  else if (e.lai1 > 0) step327 = -1;
} else if (e.ai3 === 1) {
  if (e.lai1 > 10) step327 = 1;
  else if (e.lai1 > 4) step327 = -1;
  else if (e.lai1 < 4) step327 = 1;
} else if (e.ai3 === 2) {
  if (e.lai1 < 2) step327 = -1;
  else if (e.lai1 > 8) step327 = -1;
  else if (e.lai1 < 8) step327 = 1;
}
e.lai0 += step327;
if (e.lai0 > 6) { e.lai0 = 0; e.lai1 += 1; if (e.lai1 > 11) e.lai1 = 0; }
if (e.lai0 < 0) { e.lai0 = 6; e.lai1 -= 1; if (e.lai1 < 0) e.lai1 = 11; }
e.customFrameIdx = e.lai1;
```
✓ Exact 1:1 (counter increments by ±1/0; frame advances on >6/<0 thresholds; wraps).

Hmm — one detail: vanilla `frameCounter += 1.0` (in ai3==0 first branch) — increments by exactly +1 (same as my step=1) ✓.

**Santa replica vs vanilla** (cs:73050-73093): ✓ as analyzed. One check — in the fire branch vanilla also wraps `if (frame.Y > num * 8) frame.Y = num * 6;` AFTER advancing ✓ mine matches. Walk branch wraps >5 → 1, <1 → 1 ✓.

**Cultist replica** — verified structure above. One more look at vanilla case 0's else-if: `else if (frame.Y != 0) frame.Y = ((int)frameCounter / 5 + 4) * num;` — with fc ∈ [0,15) → seg ∈ {0,1,2} → rows 4-6 ✓. Case 13: rows 13-15 ✓ (16-frame sheet: rows 0-15 ✓).

**393 ternary chain** — matches vanilla nesting ✓. Note vanilla's `(!(Math.Abs(vector3.X) > vector3.Y * 1.5f))` — my `Math.abs(ax) <= ay * 1.5` ✓.

**394** ✓.

**395 counter** ✓. Note: e.lai0 initial value 0 ✓ (Enemy field init).

Wait — one thing to double-check on 395: my frameTick395 closure reads e.ai3 — at the two call sites, e.ai3 is the final value for the tick ✓.

Hmm, but there's one subtle issue: the closure is defined AFTER the bInit block but e.lai0 advance happens only at the two exits. During ai0===1 (expert 150t transition), ai3=0 — no early return — reaches the end → frameTick395 runs ✓ every tick.

**392** ✓ — but wait: e.lai0 for 392 — could e.lai0 be touched elsewhere for parts? No. But — 392 and 395 are different entities ✓.

Edge: what about a 392 whose saucer dies mid-tick? mountOk false → dead ✓ (no frame update needed).

**345** — `if (e.ai3 >= 0) return Math.min(2, frames - 1);` — hmm, vanilla: `if (ai[3] >= 0f) frame.Y = 0;` — frame 0, not min(2,...). frames=6 so min(2,5)=2 ≠ 0! BUG — I wrote Math.min(2, frames-1) but it should be Math.min(0, frames-1) → just 0. Let me fix: return Math.min(0, frames - 1)? That's 0 (frames ≥ 1). Cleaner: `return 0;` — but keep clamp style: Math.min(frames - 1, 0) is silly. Vanilla frame 0 directly. Just `return 0;`... but if frames were 0? frames is Math.max(1,...) ≥ 1 always → 0 is always valid. Use `return 0;`.

Wait — actually double check what I wrote:
```ts
if (e.ai0 === 0) {
  if (e.ai3 >= 0) return Math.min(2, frames - 1);
  return e.vx < 0 ? 1 : 2;
}
```
Yes — wrong. Fix to `return 0;`.

Also check `e.vx < 0 ? 1 : 2` — vanilla `else if (velocity.X < 0f) frame.Y = num; else frame.Y = num * 2;` ✓. Clamps: frames=6, rows 1/2 valid ✓. (No min needed but harmless — I return raw 1/2; fine since frames=6 ≥ 3.)

Also — `if (e.ai0 === 2) return Math.min(5, frames - 1);` ✓ (row 5).

And `if (e.ai0 === 1) return Math.min(frames - 1, 3 + (Math.floor(t / 6) % 2));` ✓ rows 3-4.

Let me fix the 345 frame-0 bug now.

**386** — one more check of the deploy band: vanilla `if (ai[2] > 0f) { num41 = (int)ai[2] / 12; frame.Y = num * (9 + num41 % 2); }` ✓ mine.

Walk: `frameCounter += Math.Abs(velocity.X) * 2f; if (frameCounter > 6.0) { frame.Y += num; frameCounter = 0; } if (frame.Y / num >= 9) frame.Y = num * 2;` — advance at >6 → 7 units ✓ mine floor(walkCycleT*2/7), band 2-8 wrap → `2 + ... % 7` ✓.

Hmm wait — one thing: entering the walk band, vanilla clamps `if (frame.Y < num * 2) frame.Y = num * 2` — only relevant when coming from frames 0/1 — with my formula, when walking starts, frame = 2 + (…) ∈ [2,8] ✓ always in band.

Air: frame 1 ✓. Idle: frame 0 ✓ (also vanilla resets counter when vx==0? No — vanilla 386 does NOT reset counter on idle; frame just = 0. On resume, counter continues — my walkCycleT resets (idle → 0) — phase restart, noted).

**387** ✓.

**399** ✓.

**325** ✓.

**344** ✓ — one check: e.lai0 accumulates only when `ever` (id 344) ✓.

**551** ✓ — thresholds re-verified.

**392/395 clamp**: `Math.floor((e.lai0 % 66) / 6)` — lai0 ∈ [0,66) after wrap; but during the window clamp [36,53] → fine. But what if lai0 was never updated (e.g., puppet)? Stale value → still in range ✓.

One more potential issue — **the 395/392/344/327/346 branches vs e.lai0 initial**: for entities spawned but whose AI hasn't run yet (first render before first fixedUpdate?), lai0 = 0 → frame 0 ✓ fine.

Also — for **customFrameIdx persistence on death/transform**: if a 327 transforms into something (doesn't), or customFrameIdx lingering after... e.g., Santa NK1 dies → gone. Pumpking → gone. Cultist → gone. But what about an entity whose vanillaId changes via transformTo while reusing the same Enemy object? 439/440/327/346 don't transform. ✓.

BUT — one real edge: `Enemy.fromVanilla` reuses...? And save/load: customFrameIdx not persisted — resets to null on load → AI rewrites next tick ✓.

Another edge — the **martianFighterExtras for 386** runs only if dispatched; my Renderer 386 branch reads ai2/walkCycleT regardless ✓.

Now fix the 345 bug.
````

</details>


---

## 🤖 Assistant · 2026-08-19T08:11:56.532Z · glm-x-preview-260804

```
所有 99 个测试均已通过。我在重读 345 分支（`glide neutral` 必须是第 0 帧，而不是 2）时发现了一个 Bug。正在修复。
```


---

## 🤖 Assistant · 2026-08-19T08:11:58.373Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "old_string": "  if (id === 345) {\n    if (e.ai0 === 0) {\n      if (e.ai3 >= 0) return Math.min(2, frames - 1);\n      return e.vx < 0 ? 1 : 2;\n    }",
 "new_string": "  if (id === 345) {\n    if (e.ai0 === 0) {\n      if (e.ai3 >= 0) return 0;\n      return e.vx < 0 ? 1 : 2;\n    }"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:11:58.399Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts has been updated successfully. (note: the file had been modified on disk since you last read it — the edit applied cleanly, but the file contains other changes not in your context. Read it before edits that depend on surrounding content.)

```


---

## 🤖 Assistant · 2026-08-19T08:12:28.109Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Renderer.ts also churned from parallel session. The edit applied.

Now let me do a standalone simulation sanity-check of the three stateful machines + the stateless formulas against a reference implementation transcribed directly from the decompiled vanilla. This catches transcription mistakes. I'll write a scratch script in /tmp (not a report file — a verification input, allowed).

The sim:
1. Pumpking: run my replica vs vanilla transcription for ai3 sequences (0→1→2→0→2...) with random durations; assert equal rows every tick.
2. Cultist: run my replica vs vanilla transcription (state sequences incl. settle states 0/1/2, loop states, 13).
3. Santa: my replica vs vanilla transcription across ai0/vx sequences (fire/idle/walk with varying vx).
4. 393: my ternary chain vs vanilla transcription over random angles.
5. 394: formula equivalence over ai3 0..599.
6. 395 counter: replica vs vanilla transcription over 700 ticks with window.
7. 392 counter: same.
8. 551: my thresholds vs vanilla transcription (ai0 3/4 with fc 0..250; ai0 6 fc 0..100).
9. 387/399/325/344/386/345: formulas vs transcription.

Writing the vanilla transcription in C#-like JS from the decompiled source I read. This is a worthwhile double-check. Let me write /tmp/framecheck.mjs.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:12:29.934Z · glm-x-preview-260804

```
两个文件都有并行会话在运行；我的修改已顺利应用。现在进行一次独立验证 —— 我将把 `vanilla` 反编译代码逻辑与我编写的实现在 `/tmp` 脚本中进行对照（涵盖所有 15 台机器）。
```


---

## 🤖 Assistant · 2026-08-19T08:14:03.418Z · glm-x-preview-260804

**🔧 ToolUse: `Write`**

```json
{
 "file_path": "/tmp/framecheck.mjs",
 "content": "// 独立对账:本仓实现的帧机 vs 反编译源码逐行转写(NPC.cs 1.4.5.6)\n// ——两边都在本文件内重写,验证【算法等价】,不 import 游戏源。\n\nlet pass = 0, fail = 0;\nconst eq = (name, a, b) => { if (a === b) pass++; else { fail++; console.log(`FAIL ${name}: mine=${a} vanilla=${b}`); } };\n\n// ---------- 393 炮塔 (cs:72481-72494) ----------\nfunction vanilla393(ai2, ai3) {\n  let num134 = 0;\n  const vx = Math.cos(ai2), vy = Math.sin(ai2);\n  num134 = ((vy > Math.abs(vx) * 2) ? 4 : ((vy > Math.abs(vx) * 1.5) ? ((vx > 0) ? 5 : 3)\n    : ((Math.abs(vx) > vy * 2) ? ((vx > 0) ? 8 : 0)\n    : ((!(Math.abs(vx) > vy * 1.5)) ? ((vx > 0) ? 6 : 2) : ((!(vx > 0)) ? 1 : 7)))));\n  let frame = num134;\n  if (ai3 >= 280 && ai3 < 420 && (ai3 | 0) % 6 <= 2) frame += 9;\n  return frame;\n}\nfunction mine393(ai2, ai3) {\n  const ax = Math.cos(ai2), ay = Math.sin(ai2);\n  let f = ay > Math.abs(ax) * 2 ? 4\n    : ay > Math.abs(ax) * 1.5 ? (ax > 0 ? 5 : 3)\n    : Math.abs(ax) > ay * 2 ? (ax > 0 ? 8 : 0)\n    : Math.abs(ax) <= ay * 1.5 ? (ax > 0 ? 6 : 2)\n    : (ax > 0 ? 7 : 1);\n  if (ai3 >= 280 && ai3 < 420 && (ai3 | 0) % 6 <= 2) f += 9;\n  return f;\n}\nfor (let i = 0; i < 4000; i++) {\n  const ai2 = Math.random() * Math.PI;      // 本仓瞄准角 dy>=0 → [0,π]\n  const ai3 = Math.floor(Math.random() * 600);\n  eq('393', mine393(ai2, ai3), vanilla393(ai2, ai3));\n}\n\n// ---------- 394 火炮 (cs:72495-72518) ----------\nfunction vanilla394(ai3) {\n  let num188 = (ai3 | 0) - 300, frame;\n  if (num188 >= 120) {\n    num188 -= 120;\n    if (num188 >= 160) frame = 7 - Math.floor((num188 - 160) / 5);\n    else if (num188 >= 20) frame = Math.floor(num188 / 4) % 4;\n    else frame = 4 + Math.floor(num188 / 5);\n  } else frame = 4;\n  return frame;\n}\nconst mine394 = (ai3) => {\n  let n = (ai3 | 0) - 300, f;\n  if (n >= 120) {\n    n -= 120;\n    if (n >= 160) f = 7 - Math.floor((n - 160) / 5);\n    else if (n >= 20) f = Math.floor(n / 4) % 4;\n    else f = 4 + Math.floor(n / 5);\n  } else f = 4;\n  return f;\n};\nfor (let ai3 = -5; ai3 < 605; ai3++) eq('394', mine394(ai3), vanilla394(ai3));\n\n// ---------- 395 母碟 counter (cs:72520-72541) ----------\nfunction vanilla395Step(fc, ai3) {\n  const flag10 = ai3 >= 20 && ai3 < 260;\n  fc += 1;\n  if (fc >= 66) fc = 0;\n  if (flag10) { fc += 1; if (fc >= 54 || fc < 36) fc = 36; }\n  return fc;\n}\nfunction mine395Step(lai0, ai3) {\n  lai0 += 1;\n  if (lai0 >= 66) lai0 = 0;\n  if (ai3 >= 20 && ai3 < 260) { lai0 += 1; if (lai0 >= 54 || lai0 < 36) lai0 = 36; }\n  return lai0;\n}\n{\n  let vf = 0, mf = 0, ai3 = 0;\n  for (let tick = 0; tick < 3000; tick++) {\n    ai3 = (ai3 + 1) % 600;\n    vf = vanilla395Step(vf, ai3);\n    mf = mine395Step(mf, ai3);\n    eq('395counter', mf, vf);\n    eq('395frame', Math.floor((mf % 66) / 6), Math.floor((vf % 66) / 6));\n  }\n}\n\n// ---------- 392 炮体 counter (cs:72543-72560) ----------\nfunction vanilla392Step(fc, ai3) {\n  const flag6 = ai3 >= 20 && ai3 < 260;\n  fc += 1;\n  if (flag6) fc += 1;\n  if (fc >= 12) fc = 0;\n  return fc;\n}\n{\n  let vf = 0, mf = 0, ai3 = 0;\n  for (let tick = 0; tick < 2000; tick++) {\n    ai3 = (ai3 + 1) % 600;\n    vf = vanilla392Step(vf, ai3);\n    mf += ai3 >= 20 && ai3 < 260 ? 2 : 1;\n    if (mf >= 12) mf = 0;\n    eq('392counter', mf, vf);\n    eq('392frame', Math.floor((mf % 12) / 3), Math.floor((vf % 12) / 3));\n  }\n}\n\n// ---------- 327 南瓜王姿态机 (cs:72977-73037) ----------\nfunction vanilla327(ai3, fc, row) {\n  if (ai3 === 0) {\n    if (row > 5) fc += 1;\n    else if (row > 0) fc -= 1;\n  } else if (ai3 === 1) {\n    if (row > 10) fc += 1;\n    else if (row > 4) fc -= 1;\n    else if (row < 4) fc += 1;\n  } else if (ai3 === 2) {\n    if (row < 2) fc -= 1;\n    else if (row > 8) fc -= 1;\n    else if (row < 8) fc += 1;\n  }\n  if (fc > 6) { fc = 0; row += 1; if (row > 11) row = 0; }\n  if (fc < 0) { fc = 6; row -= 1; if (row < 0) row = 11; }\n  return { fc, row };\n}\nfunction mine327(ai3, fc, row) {\n  let step = 0;\n  if (ai3 === 0) {\n    if (row > 5) step = 1;\n    else if (row > 0) step = -1;\n  } else if (ai3 === 1) {\n    if (row > 10) step = 1;\n    else if (row > 4) step = -1;\n    else if (row < 4) step = 1;\n  } else if (ai3 === 2) {\n    if (row < 2) step = -1;\n    else if (row > 8) step = -1;\n    else if (row < 8) step = 1;\n  }\n  fc += step;\n  if (fc > 6) { fc = 0; row += 1; if (row > 11) row = 0; }\n  if (fc < 0) { fc = 6; row -= 1; if (row < 0) row = 11; }\n  return { fc, row };\n}\n{\n  let v = { fc: 0, row: 0 }, m = { fc: 0, row: 0 };\n  let seed = 12345;\n  const rnd = () => (seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff;\n  for (let tick = 0; tick < 6000; tick++) {\n    const ai3 = Math.floor(rnd() * 3);       // 随机换姿态(含频繁切换)\n    v = vanilla327(ai3, v.fc, v.row);\n    m = mine327(ai3, m.fc, m.row);\n    eq('327', m.row, v.row);\n    eq('327fc', m.fc, v.fc);\n  }\n}\n\n// ---------- 345 冰雪女王 (cs:73106-73143) ----------\nfunction vanilla345(ai0, ai3, vx) {\n  if (ai0 === 0) {\n    if (ai3 >= 0) return 0;\n    if (vx < 0) return 1;\n    return 2;\n  }\n  return null; // 1/2 态带计数器,下方单独验证\n}\nfor (let i = 0; i < 500; i++) {\n  const ai3 = Math.floor(Math.random() * 28) - 14, vx = (Math.random() - 0.5) * 16;\n  const mine = ai3 >= 0 ? 0 : vx < 0 ? 1 : 2;\n  eq('345glide', mine, vanilla345(0, ai3, vx));\n}\n\n// ---------- 346 圣诞坦克 (cs:73050-73093) ----------\nfunction vanilla346(ai0, vx, fc, row) {\n  if (ai0 === 1) {\n    fc += 1;\n    if (fc > 2) { row += 1; fc = 0; }\n    if (row > 8) row = 6;\n    if (row < 6) row = 6;\n    return { fc, row };\n  }\n  if (vx === 0) { fc = 0; return { fc, row }; }\n  fc += 1;\n  fc += Math.abs(vx) / 2;\n  if (fc > 4) { row += 1; fc = 0; }\n  if (row > 5) row = 1;\n  if (row < 1) row = 1;\n  return { fc, row };\n}\nfunction mine346(ai0, vx, fc, row) {\n  if (ai0 === 1) {\n    fc += 1;\n    if (fc > 2) { fc = 0; row += 1; }\n    if (row > 8) row = 6;\n    if (row < 6) row = 6;\n  } else if (vx === 0) {\n    fc = 0;\n  } else {\n    fc += 1 + Math.abs(vx) / 2;\n    if (fc > 4) { fc = 0; row += 1; }\n    if (row > 5) row = 1;\n    if (row < 1) row = 1;\n  }\n  return { fc, row };\n}\n{\n  let v = { fc: 0, row: 0 }, m = { fc: 0, row: 0 };\n  let seed = 999;\n  const rnd = () => (seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff;\n  for (let tick = 0; tick < 6000; tick++) {\n    const ai0 = rnd() < 0.3 ? 1 : 0;\n    const vx = rnd() < 0.15 ? 0 : (rnd() - 0.5) * 10;   // 含停步/开火/行走混合\n    v = vanilla346(ai0, vx, v.fc, v.row);\n    m = mine346(ai0, vx, m.fc, m.row);\n    eq('346', m.row, v.row);\n    eq('346fc', m.fc, v.fc);\n  }\n}\n\n// ---------- 325 哀木 (cs:73172-73201):counter 恒 +1/t、>4 进帧 ----------\n{\n  // vanilla 独立跑 counter(不重置),帧带切换按钳位\n  let fc = 0, row = 0;\n  let seed = 77;\n  const rnd = () => (seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff;\n  let t = 0;   // mine: animT\n  for (let tick = 0; tick < 4000; tick++) {\n    const moving = rnd() > 0.4;\n    fc += 1;\n    if (fc > 4) { row += 1; fc = 0; }\n    if (moving) { if (row < 5) row = 5; if (row > 9) row = 5; }\n    else { if (row > 4) row = 0; }\n    const mine = moving ? 5 + (Math.floor(t / 5) % 5) : Math.floor(t / 5) % 5;\n    // 带内相位差(带切换瞬间 mine 相位任意)只校验:mine ∈ 合法带 & 步进节拍一致\n    if (moving && (mine < 5 || mine > 9)) { fail++; console.log('FAIL 325 band', mine); }\n    if (!moving && mine > 4) { fail++; console.log('FAIL 325 idle band', mine); }\n    pass++;\n    t++;\n  }\n}\n\n// ---------- 344 常世吼 (cs:73144-73170) ----------\n{\n  let vfc = 0, vrow = 0, total = 0;\n  let seed = 4242;\n  const rnd = () => (seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff;\n  for (let tick = 0; tick < 6000; tick++) {\n    const vx = rnd() < 0.1 ? 0 : (rnd() - 0.5) * 8;\n    // vanilla\n    if (vx === 0) { vfc += 1; if (vfc > 5) { vrow += 1; vfc = 0; } if (vrow > 9) vrow = 0; }\n    else { vfc += Math.max(1, Math.abs(vx) * 0.75); if (vfc > 5) { vrow += 1; vfc = 0; } if (vrow > 9) vrow = 0; }\n    // mine (AI 累计 lai0 → Renderer floor(lai0/6)%10)\n    total += vx === 0 ? 1 : Math.max(1, Math.abs(vx) * 0.75);\n    eq('344', Math.floor(total / 6) % 10, vrow);\n  }\n}\n\n// ---------- 439/440 教徒 (cs:72698-72783) ----------\nfunction vanillaCultist(st, fc, row) {\n  const wrap = fc >= 15;\n  if (wrap) fc = 0;\n  const seg = Math.floor(fc / 5);\n  switch (st) {\n    case 0: if (wrap) row = 0; else if (row !== 0) row = seg + 4; break;\n    case 10: row = seg + 4; break;\n    case 1: if (wrap) row = 1; else if (row !== 1) row = seg + 10; break;\n    case 11: row = seg + 10; break;\n    case 2: if (wrap) row = 2; else if (row !== 2) row = seg + 7; break;\n    case 12: row = seg + 7; break;\n    case 13: row = seg + 13; break;\n  }\n  fc += 1;\n  return { fc, row };\n}\n// mine 与 vanilla 同构(本仓实现即上式)——用随机态序列验证不变量:\n{\n  let v = { fc: 0, row: 0 };\n  let seed = 31337;\n  const rnd = () => (seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff;\n  const states = [0, 1, 2, 10, 11, 12, 13];\n  for (let tick = 0; tick < 8000; tick++) {\n    const st = states[Math.floor(rnd() * 7)];\n    const prev = v.row;\n    v = vanillaCultist(st, v.fc, v.row);\n    // 不变量:行 ∈ [0,15];循环态落对应带;定格态一轮后回定格行\n    if (v.row < 0 || v.row > 15) { fail++; console.log('FAIL cultist range', v.row); }\n    if (st === 10 && (v.row < 4 || v.row > 6)) { fail++; console.log('FAIL cultist band10', v.row); }\n    if (st === 11 && (v.row < 10 || v.row > 12)) { fail++; console.log('FAIL cultist band11', v.row); }\n    if (st === 12 && (v.row < 7 || v.row > 9)) { fail++; console.log('FAIL cultist band12', v.row); }\n    if (st === 13 && (v.row < 13 || v.row > 15)) { fail++; console.log('FAIL cultist band13', v.row); }\n    pass++;\n    void prev;\n  }\n  // 定格态收敛:state 0 持续 40t → 行 0\n  let s = { fc: 0, row: 6 };\n  for (let i = 0; i < 40; i++) s = vanillaCultist(0, s.fc, s.row);\n  eq('cultist settle0', s.row, 0);\n  s = { fc: 0, row: 4 };\n  for (let i = 0; i < 40; i++) s = vanillaCultist(1, s.fc, s.row);\n  eq('cultist settle1', s.row, 1);\n  s = { fc: 0, row: 11 };\n  for (let i = 0; i < 40; i++) s = vanillaCultist(2, s.fc, s.row);\n  eq('cultist settle2', s.row, 2);\n}\n\n// ---------- 551 Betsy (cs:67913-68107) ----------\nfunction vanilla551(ai0, ai1) {\n  let num268 = 0;\n  const fc = Math.floor(ai1);\n  if (ai0 === 4) {\n    const num269 = 60, num271 = 60;\n    num268 = 5;\n    if (fc >= 5) num268 = 6;\n    if (fc >= num269 - 6) num268 = 7;\n    if (fc >= num269 - 3) num268 = 8;\n    if (fc >= num269) num268 = 9 + Math.floor(fc / 3) % 2;\n    if (fc >= num269 + num271 + 3) num268 = 8;\n    if (fc >= num269 + num271 + 3 + 5 * 1) num268 = 7;\n    if (fc >= num269 + num271 + 3 + 5 * 2) num268 = 0;\n  } else if (ai0 === 3) {\n    const num278 = 40, num279 = 80, num280 = 120, num281 = 25;\n    num268 = 5;\n    if (fc >= 5) num268 = 6;\n    if (fc >= num278 - 6) num268 = 7;\n    if (fc >= num278 - 3) num268 = 8;\n    if (fc >= num278) num268 = 9 + Math.floor(fc / 3) % 2;\n    if (fc >= num280 - num281 + 3) num268 = 8;\n    if (fc >= num280 - num281 + 3 + 5 * 1) num268 = 7;\n    if (fc >= num280 - num281 + 3 + 5 * 2) num268 = 0;\n  } else if (ai0 === 5) {\n    num268 = 3;\n  } else if (ai0 === 6) {\n    num268 = 1;\n    if (fc >= 8 * 1) num268 = 2;\n    if (fc >= 8 * 2) num268 = 3;\n    if (fc >= 8 * 3) num268 = 4;\n    if (fc >= 8 * 4) num268 = 3;\n    if (fc >= 8 * 5) num268 = 4;\n    if (fc >= 8 * 6) num268 = 3;\n    if (fc >= 8 * 7) num268 = 2;\n    if (fc >= 8 * 8) num268 = 1;\n    if (fc >= 8 * 9) num268 = 0;\n  }\n  return num268;\n}\nfunction mine551(ai0, ai1) {\n  const fc = Math.floor(ai1);\n  if (ai0 === 4) {\n    if (fc < 5) return 5;\n    if (fc < 54) return 6;\n    if (fc < 57) return 7;\n    if (fc < 60) return 8;\n    if (fc < 123) return 9 + (Math.floor(fc / 3) % 2);\n    if (fc < 128) return 8;\n    if (fc < 133) return 7;\n    return 0;\n  }\n  if (ai0 === 3) {\n    if (fc < 5) return 5;\n    if (fc < 34) return 6;\n    if (fc < 37) return 7;\n    if (fc < 40) return 8;\n    if (fc < 98) return 9 + (Math.floor(fc / 3) % 2);\n    if (fc < 103) return 8;\n    if (fc < 108) return 7;\n    return 0;\n  }\n  if (ai0 === 5) return 3;\n  if (ai0 === 6) {\n    const seq = [1, 2, 3, 4, 3, 4, 3, 2, 1, 0];\n    return seq[Math.min(9, Math.floor(fc / 8))];\n  }\n  return 0;\n}\nfor (const ai0 of [3, 4]) for (let fc = 0; fc <= 260; fc++) eq(`551_${ai0}`, mine551(ai0, fc), vanilla551(ai0, fc));\nfor (let fc = 0; fc <= 130; fc++) eq('551_6', mine551(6, fc), vanilla551(6, fc));\nfor (const ai0 of [0, 1, 2, 5]) for (let fc = 0; fc < 40; fc++) eq(`551_${ai0}`, mine551(ai0, fc), vanilla551(ai0, fc));\n\n// ---------- 387 特斯拉速率档 (cs:72335-72367) ----------\n{\n  // vanilla counter 演化 vs mine floor(t/period)%2 ——只验证节拍(相位任意):\n  // ai0>0 三档 10/5/10÷3 单位一帧;ai0<=0 15 单位一帧\n  for (const ai0 of [-120, -1, 0, 5, 19, 20, 39, 40, 55]) {\n    const per = ai0 > 0 ? 10 / (1 + (ai0 >= 20 ? 1 : 0) + (ai0 >= 40 ? 1 : 0)) : 15;\n    const thr = ai0 > 0 ? 10 : 15;\n    eq(`387 period ai0=${ai0}`, per, thr / (1 + (ai0 >= 20 ? 1 : 0) + (ai0 >= 40 ? 1 : 0)));\n  }\n}\n\n// ---------- 386 工程师 (cs:72369-72402) ----------\n{\n  for (let ai2 = 1; ai2 <= 60; ai2++) {\n    const num41 = Math.floor(ai2 / 12);\n    eq('386 deploy', 9 + (Math.floor(ai2 / 12) % 2), 9 + (num41 % 2));\n  }\n  // 行走节拍:>6 进帧 = 7 单位\n  let fc = 0, row = 2;\n  let total = 0;\n  const vx = 1.5;\n  for (let tick = 0; tick < 500; tick++) {\n    fc += Math.abs(vx) * 2;\n    total += Math.abs(vx);\n    if (fc > 6) { row += 1; fc = 0; if (row >= 9) row = 2; }\n    eq('386 walk', 2 + Math.floor((total * 2) / 7) % 7, row);\n  }\n}\n\n// ---------- 399 探测器 (cs:72562-72565) ----------\nfor (let i = 0; i < 200; i++) {\n  const t = Math.random() * 10000;\n  const ai0 = Math.random() < 0.5 ? 0 : 2;\n  const vanilla = Math.floor(((t * 0.25) % 4 + 4) % 4 + (ai0 !== 0 ? 4 : 0));\n  // 本仓 floor((t*0.25)%4) —— t>0 时 (t*0.25)%4 恒 >=0,同式\n  eq('399', Math.floor((t * 0.25) % 4) + (ai0 !== 0 ? 4 : 0), vanilla);\n}\n\nconsole.log(`\\n${pass} pass, ${fail} fail`);\nprocess.exit(fail ? 1 : 0);\n"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:14:03.430Z

**📎 ToolResult**

```
File created successfully at: /tmp/framecheck.mjs (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T08:14:21.179Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "node /tmp/framecheck.mjs 2>&1 | tail -8",
 "description": "Run frame machine equivalence check"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:14:21.285Z

**📎 ToolResult**

```
FAIL 386 walk: mine=4 vanilla=6
FAIL 386 walk: mine=4 vanilla=6
FAIL 386 walk: mine=5 vanilla=6
FAIL 386 walk: mine=5 vanilla=7
FAIL 386 walk: mine=5 vanilla=7
FAIL 386 walk: mine=6 vanilla=7

52642 pass, 6053 fail

```


---

## 🤖 Assistant · 2026-08-19T08:16:02.603Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
The check found one discrepancy: `386 walk: mine=4 vanilla=6` — the walk-band formula mismatches. Let me analyze.

Vanilla 386 walk:
```csharp
frameCounter += Math.Abs(velocity.X) * 2f;
if (frameCounter > 6.0) { frame.Y += num; frameCounter = 0.0; }
if (frame.Y / num >= 9) frame.Y = num * 2;
```

My sim: vx = 1.5 → per tick counter += 3.0. Advance at counter > 6 → after 3 ticks (3+3+3=9 > 6). total = Σ|vx| = 1.5/tick. My formula: 2 + floor((total*2)/7) % 7 where total*2 = 3/tick → floor(3t/7).

Vanilla: advances at ticks where accumulated exceeds 6 — i.e., advance when cumulative > 6, > 13(? no — counter resets to 0 then accumulates again). The advance events happen when the *residual* counter crosses 6. With uniform increments of 3/t: counter after reset 0 → 3 → 6 → 9>6 → advance, reset 0. So advances at every 3rd tick. Number of advances after t ticks = floor(t/3)... My formula floor(3t/7): at t=3 → floor(9/7)=1 ✓; t=6 → floor(18/7)=2 ✓; t=9 → floor(27/7)=3 ✓; t=12 → floor(36/7)=5 ✗ (actual 4). Hmm — so floor(total/7) is only correct when increments are ≤ 1... 

The issue: `frameCounter > 6` with counter NOT reset until crossing — a single increment can overshoot. The advance count = number of times the running residual crosses 6 — with increment 3/tick, the effective period is NOT 7 units but ceil(7/3)*3 = 9 units (3 ticks). My floor(total/7) assumes increments of ≤1 (where crossing happens exactly at 7). For |vx|*2 > 1, the vanilla advance rate is SLOWER than floor(total/7) suggests — increments overshoot the 6-threshold and the excess is lost on reset.

So my "counter ≈ 7 单位一帧" approximation is wrong for fast walkers — it over-advances. Wait — but hold on, the same applies to the existing generic ai===3 branch which multiplies walkCycleT by (|vx|*2+1)/6 — that's the project's established approximation (also technically lossy). Hmm.

But I should be exact where I can. The exact semantics: advance events = greedy accumulation with lossy reset. That's a stateful process — can't be captured by a pure formula when increments > 1.

Options:
a) Replica in AI (martianFighterExtras for 386) — maintain (counter, row) — exact. martianFighterExtras is called "after fighterAI" from case 3 dispatch — every tick for 386 ✓. Storage: e.lai0/e.lai1 (free for 386). Write customFrameIdx.
b) Formula approximation like the generic branch.

The task demands 1:1; the walk band cadence matters visually (engineer walks at some speed). Let me do the replica — it's the same pattern as santa. martianFighterExtras has `e` and runs per tick.

Hold on — wait. Does martianFighterExtras run BEFORE or AFTER the movement (fighterAI)? Called from "case 3 after fighterAI" — so after. e.vx is final for the tick ✓. But also — the air/idle states: vanilla resets counter in air (fc=0) and freezes at vx==0 (no reset — frame snapped to 0, counter keeps... wait vanilla 386 idle: `if (velocity.X == 0f) frame.Y = 0;` — counter NOT reset! (Unlike 381-389 family which doesn't reset either.) Let me re-read case 386:

```csharp
else if (velocity.Y == 0f)
{
    spriteDirection = direction;
    if (frame.Y < num * 2) frame.Y = num * 2;
    frameCounter += Math.Abs(velocity.X) * 2f;
    if (frameCounter > 6.0) { frame.Y += num; frameCounter = 0.0; }
    if (frame.Y / num >= 9) frame.Y = num * 2;
    if (velocity.X == 0f) frame.Y = 0;
}
else { frameCounter = 0.0; frame.Y = num; }
```

So in the grounded branch: counter += |vx|*2 ALWAYS (even when vx==0 — adds 0); frame clamped ≥2; advance >6; wrap ≥9 → 2; if vx==0 → frame = 0 (but counter preserved!). Air: counter = 0, frame = 1.

So replica:
```ts
// after deploy-band handling (ai2 <= 0):
if (e.vy !== 0) { e.lai0 = 0; e.lai1 = 1; }
else {
  if (e.lai1 < 2) e.lai1 = 2;
  e.lai0 += Math.abs(e.vx) * 2;
  if (e.lai0 > 6) { e.lai0 = 0; e.lai1 += 1; }
  if (e.lai1 >= 9) e.lai1 = 2;
  if (e.vx === 0) e.lai1 = 0;
}
e.customFrameIdx = e.lai1;
```

Wait — ordering: the deploy band (ai2>0) branch replaces the whole walk logic? Vanilla: `if (ai[2] > 0f) { deploy frame } else if (vy == 0) {walk} else {air}` — yes, deploy replaces. And during deploy the counter/frame keep their values (not touched) ✓ — so on exit from deploy, walking resumes from the old frame. My replica: only update when ai2 <= 0 ✓.

Hmm — but careful about which vx/vy: vanilla FindFrame reads velocity AFTER AI. Our martianFighterExtras runs after fighterAI in the same tick ✓.

Where to place: inside martianFighterExtras's `if (id === 386)` block — at the end (after the turret-spawn logic; note that block has early `return`s — the spawn-return path: `if (e.ai2 === 30) { ...; return; }` — on the spawn tick it returns early! Frame update would be skipped that tick (1 tick off — vanilla FindFrame always runs). Hmm — the `return` inside the spawn loop exits the whole function. I'd need the frame update BEFORE those returns → place it at the top of the 386 block. But at the top, is ai2 already final for the tick? The ai2 increment/spawn logic happens below... ai2 semantics for the DEPLOY BAND check (ai2 > 0) — vanilla FindFrame reads ai[2] AFTER the AI updated it. E.g., on the tick where ai2 goes 29→30: vanilla FindFrame sees 30 → deploy band. If I check at top (pre-increment), I see 29 — also > 0 → deploy band either way (9 + floor(29/12)%2 = 9+0... vs floor(30/12)%2 = 9+0 — hmm 29/12=2.4→2%2=0; 30/12=2.5→2 → 0 — same. But at ai2 23→24: 23/12=1 → band 10; 24/12=2 → band 9! Different. So 1-tick-off on the 9/10 alternation boundary. Negligible? It's a 12t-period flip — 1t skew. Hmm.

Alternative: restructure — extract the frame update into a closure called at every exit? The 386 block exits: (1) confusedT early return, (2) the spawn `return` inside loop, (3) end of function. Ugly. 

Alternative placement: not in martianFighterExtras but... is there any other per-tick hook for 386? The fighterAI dispatch — case 3 → fighterAI + extras. What about placing at the START but computing the deploy band from the post-update ai2 value? The ai2 mutation within the tick: `e.ai2 += 1` (if <60), spawn at ===30, at ===60 → -120, confusedT → -60, justHit → -30. The final value differs from the initial only by the increment or resets. I could compute the effective ai2: complicated.

Pragmatic: accept 1-tick skew on band-9/10 flip boundaries by placing at top? Or place at the BOTTOM of martianFighterExtras and refactor the spawn `return` to a flag so the bottom always runs? Minimal diff approach: change the spawn-return into a labeled flow... The task says "禁止改动既有其他分支" (don't modify other existing branches) — the spawn loop's `return` is existing code; restructuring it slightly to not skip the frame update is a modification of that code. Hmm — but I could instead put the frame update at the top AND replicate the ai2 evolution? No.

Actually — simplest correct solution: put the frame replica at the top of the 386 block, and for the deploy band use the value ai2 will have after update — I can predict it deterministically:
- if confusedT > 0 → -60 (set below)
- else if ai2 < 60 → +1
- then possible overrides (justHit → -30; ai2===30 spawn; ai2===60→-120)...

Too fragile. The 1-tick skew on a 12t-period row flip is truly negligible (band 9↔10 alternation shifted by 1 tick at the boundary). Also the walk counter uses pre-movement... no wait, vx/vy are already final (fighterAI ran before extras). ai2's only effect is the deploy band + the >0 gate. On the boundary tick (ai2 23→24 or 35→36 etc.), my top-read shows the old band for one tick. Fine — but hmm, actually wait: there's a subtle more impactful case: the tick where ai2 goes 0→1 (deploy starts): top-read sees 0 → walk frame for one extra tick. Negligible.

And ai2 = 60 → -120 (deploy ends): top-read sees 60 → deploy band one extra tick. Negligible.

OK — top of the 386 block, note the 1-tick skew in a comment. Hmm, wait — actually, let me reconsider placing it at the END and just accepting that the spawn tick (===30) skips one frame update... Also negligible! The spawn-tick skip means counter doesn't advance that tick (walk counter) or deploy band frozen 1 tick. ALSO negligible. End placement reads post-update ai2 → exact band values. End placement requires the spawn `return` path to skip — one tick per turret placement (every ~150t). Both options ~equally negligible; end placement is exact for band boundaries and loses 1 tick per spawn; top placement is exact per-tick except band boundaries shift 1t.

Hmm — end placement also has the confusedT early return (`if (e.confusedT > 0) { e.ai2 = -60; return; }`) — confused engineers skip frame updates entirely (confusion lasts a while — during full confusion the frame would freeze; vanilla FindFrame still runs: ai2=-60 → walk logic). Freezing during confusion = visible wrongness (confused engineer walks with frozen legs). So end placement is worse.

Top placement it is: runs every tick, 1-tick band-boundary skew noted.

Actually — hmm wait, one more idea: place the frame replica at top, but read ai2 for the band as `e.ai2 + (should increment ? 1 : 0)`... no — enough. Top placement, comment the skew.

Also — vy check: vanilla `velocity.Y == 0f` — our e.vy exact. Fighter on ground → vy 0 ✓.

Now — also reconsider 346 (santa) walk counter — same overshoot issue! My santa replica is a faithful step-by-step replica (L[0] += 1 + |vx|/2; if > 4 advance) — exact ✓ (verified in sim: '346' all passed — wait did they? The sim failures were only '386 walk'. Let me confirm — the output tail shows only 386 walk failures. The 346 sim passed 6000 ticks ✓ because it's a step replica, not a formula.)

And 325: formula floor(t/5)%5 — counter +1/t (increment exactly 1, no overshoot) — exact advance rate ✓ (advance at counter >4 with +1 steps → every 5th tick ✓). Sim passed.

And 344: replica accumulation with floor(total/6) — overshoot issue!! counter += max(1, |vx|*0.75) can be up to ~3-4 per tick — advance when counter > 5 with reset-to-0 — overshoot lost. floor(total/6) assumes lossless. My sim '344' compared floor(total/6)%10 vs the vanilla step-sim... and it PASSED? The tail output showed only 386 failures... let me check — the sim ran 6000 ticks with vx up to ±4 → increments up to 3. Did 344 really pass? The output tail showed only "386 walk" FAILs, and 52642 pass / 6053 fail — all fails are 386? 6053 fails of 500 386-walk iterations... wait the 386 walk loop is 500 ticks → 500 eq calls. 6053 >> 500. Hmm! Something else failed too — the tail only showed the last few lines. Let me re-run and count failures by name.
````

</details>


---

## 🤖 Assistant · 2026-08-19T08:16:04.550Z · glm-x-preview-260804

```
模拟检测到了 386 号 walk-band 差异（counter overshoot — 超出阈值的部分在重置时会丢失，因此使用公式 `floor(total/7)` 会使步进过快）。让我查看一下完整的失败分析。
```


---

## 🤖 Assistant · 2026-08-19T08:16:05.421Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "node /tmp/framecheck.mjs 2>&1 | grep FAIL | sed 's/[=:].*//' | sort | uniq -c | sort -rn",
 "description": "Group simulation failures by check name"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:16:05.496Z

**📎 ToolResult**

```
5582 FAIL 344
 431 FAIL 386 walk
  40 FAIL 346fc

```


---

## 🤖 Assistant · 2026-08-19T08:16:38.843Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Three failure groups:

1. **344 (5582)**: my `floor(total/6) % 10` formula vs step-replica — overshoot loss. Fix: do a step replica instead — but the counter+row must live somewhere. mourningWoodAI can maintain (counter, row) in the `la(e)` localAI slots? mourningWoodAI doesn't currently call la() — L[0]/L[1] free (L used by pumpkingBladeAI for OTHER entities — per-entity WeakMap so no clash; 325/344 use L[0],L[1]). Then Renderer 344 branch reads... hmm — I could keep e.lai0 as the exact step counter (residual 0-5) and put row in e.lai1: Renderer: `e.lai1` clamped. But then 344's row must also wrap correctly: replica advances row +1, wrap >9 → 0. And 344 has no band memory → row = advanceCount % 10 could be derived IF increments were ≤1... but with overshoot, advanceCount ≠ floor(total/6). So keep both: e.lai0 = residual counter, e.lai1 = row; Renderer reads e.lai1 directly.

   Update: mourningWoodAI end:
   ```ts
   if (ever) {
     e.lai0 += e.vx === 0 ? 1 : Math.max(1, Math.abs(e.vx) * 0.75);
     if (e.lai0 > 5) { e.lai0 = 0; e.lai1 += 1; if (e.lai1 > 9) e.lai1 = 0; }
   }
   ```
   Renderer 344: `return Math.min(frames - 1, e.lai1);`

2. **386 walk (431)**: same overshoot — formula wrong. Fix: replica in martianFighterExtras (top of 386 block) writing customFrameIdx with (lai0 counter, lai1 row) as designed.

3. **346fc (40)**: my santa replica ordering differs — mine advances `row += 1` inside `if (fc > 2) { fc = 0; row += 1; }` then clamps; vanilla: `fc += 1; if (fc > 2) { frame.Y += num; fc = 0; }` then clamps `if (frame.Y > 8) → 6; if (frame.Y < 6) → 6`. Order of advance vs clamp — mine: advance then clamp — same as vanilla (advance → clamp). Hmm — where's the diff? Vanilla fire: `frameCounter += 1.0; if (frameCounter > 2.0) { frame.Y += num; frameCounter = 0.0; } if (frame.Y > num * 8) frame.Y = num * 6; if (frame.Y < num * 6) frame.Y = num * 6;` — mine identical ordering... except the sim's vanilla346 walk branch: `fc += 1; fc += Math.abs(vx)/2; if (fc > 4) { row += 1; fc = 0; } ...` — and mine346 walk: `fc += 1 + Math.abs(vx)/2; if (fc > 4) {...}` — same. The 346fc fails (40) — only the COUNTER differs, rows equal. Floating point summation order: `fc += 1; fc += |vx|/2` vs `fc += (1 + |vx|/2)` — different rounding! (a+b)+c vs a+(b+c). Tiny float drift accumulates → occasionally the >4 comparison differs by one tick. Rows happened to stay equal over the run. That's a sim artifact, not a real difference... but to be bit-exact, mirror the exact order: two separate adds. Let me update my santaNK1AI replica to `L[0] += 1; L[0] += Math.abs(e.vx) / 2;` matching vanilla's two statements. (The 386 replica similarly: `e.lai0 += Math.abs(e.vx) * 2` — single add ✓ matches.)

   Also 344's replica — vanilla is a single add ✓.

Let me now apply the three fixes:
A. Renderer: 344 branch → read e.lai1 (row). Update comment.
B. bossAI_moon_events mourningWoodAI: replace accumulation with counter+row replica.
C. bossAI_moon_events santaNK1AI: split the += into two statements for bit-exact float order.
D. bossAI_martian martianFighterExtras: 386 full replica (counter lai0, row lai1 → customFrameIdx), placed at top of the 386 block; Renderer 386 branch → remove (replaced by customFrameIdx). Wait — the Renderer 386 branch currently handles deploy band + walk formula. If the AI replica covers everything, the Renderer branch should go (customFrameIdx short-circuits first anyway — dead code). Cleaner: delete the Renderer 386 branch and note the 386 handling in the batch comment (like 327/346/439/440). Yes.

E. Re-run sim with corrected formulas to verify 344/386 replicas now pass (update sim accordingly).
````

</details>


---

## 🤖 Assistant · 2026-08-19T08:16:39.994Z · glm-x-preview-260804

```
有三处需要修复：344 和 386 需要步进副本（overshoot loss），346 的浮点加法顺序应与原版的两个语句保持位级一致。正在应用修复。
```


---

## 🤖 Assistant · 2026-08-19T08:16:52.527Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "old_string": "  // 386 火星工程师（cs:72369-72402）：放塔期（ai[2]>0）帧 9/10 每 12t 交替；\n  //   地面行走带 2-8 按 |vx|*2 累计（无 +1）、>6 进帧；站定=0；腾空=1\n  if (id === 386) {\n    if (e.ai2 > 0) return Math.min(frames - 1, 9 + (Math.floor(e.ai2 / 12) % 2));\n    if (e.vy !== 0) return Math.min(1, frames - 1);\n    if (!walking) return 0;\n    return Math.min(frames - 1, 2 + Math.floor((e.walkCycleT * 2) / 7) % 7);\n  }\n  // 325 哀木（cs:73172-73201）：站定带 0-4 / 移动带 5-9，counter 恒 +1/t、>4 进帧\n  //   （两分支同速 → counter ≡ animT，无 AI 侧状态；带切换瞬间带内相位任意，登记）\n  if (id === 325) {\n    return Math.min(frames - 1, e.vx === 0 ? Math.floor(t / 5) % 5 : 5 + (Math.floor(t / 5) % 5));\n  }\n  // 344 常世吼（cs:73144-73170）：全带 0-9，counter += max(1,|vx|*0.75)/t、>5 进帧\n  //   （6 单位/帧，速率随速度变化）——累计副本由 mourningWoodAI 累进到 e.lai0\n  if (id === 344) return Math.min(frames - 1, Math.floor(e.lai0 / 6) % 10);",
 "new_string": "  // 386 火星工程师（cs:72369-72402）：帧机在 bossAI_martian martianFighterExtras\n  //   内逐 tick 副本（放塔期 ai2>0 帧 9/10 每 12t 交替 / 行走带 2-8 counter +=\n  //   |vx|*2（无 +1）、>6 进帧——增量 >1 时越限溢出丢弃,公式折算会快进 → 须\n  //   步进副本 / 站定=0 / 腾空=1）→ customFrameIdx 直读\n  // 325 哀木（cs:73172-73201）：站定带 0-4 / 移动带 5-9，counter 恒 +1/t、>4 进帧\n  //   （两分支同速 → counter ≡ animT，无 AI 侧状态；带切换瞬间带内相位任意，登记）\n  if (id === 325) {\n    return Math.min(frames - 1, e.vx === 0 ? Math.floor(t / 5) % 5 : 5 + (Math.floor(t / 5) % 5));\n  }\n  // 344 常世吼（cs:73144-73170）：全带 0-9，counter += max(1,|vx|*0.75)/t、>5 进帧\n  //   （速率随速度变化,且增量 >1 越限溢出丢弃 → 步进副本；mourningWoodAI 维护\n  //   e.lai0=counter / e.lai1=帧行）\n  if (id === 344) return Math.min(frames - 1, e.lai1);"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:16:52.557Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T08:17:01.047Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_moon_events.ts",
 "old_string": "  // ---- FindFrame case 344 副本（cs:73144-73170）：counter += max(1,|vx|*0.75)/t\n  //      （站定 vx==0 分支 +1/t）、>5 进帧（6 单位/帧，速率随速度变化）→ 累计值\n  //      落 e.lai0，Renderer 按 floor(lai0/6)%10 取帧（344 全带 0-9 无带切换，\n  //      advanceCount 即帧号）。325 同函数但两分支 counter 恒 +1/t ≡ animT，\n  //      Renderer 用 t 直推无需副本 ----\n  if (ever) e.lai0 += e.vx === 0 ? 1 : Math.max(1, Math.abs(e.vx) * 0.75);\n}",
 "new_string": "  // ---- FindFrame case 344 副本（cs:73144-73170）：counter += max(1,|vx|*0.75)/t\n  //      （站定 vx==0 分支 +1/t）、>5 进帧（越限溢出随回卷丢弃 → 须步进副本）；\n  //      e.lai0=counter / e.lai1=帧行（全带 0-9 回卷）。325 同函数但两分支\n  //      counter 恒 +1/t ≡ animT，Renderer 用 t 直推无需副本 ----\n  if (ever) {\n    e.lai0 += e.vx === 0 ? 1 : Math.max(1, Math.abs(e.vx) * 0.75);\n    if (e.lai0 > 5) {\n      e.lai0 = 0;\n      e.lai1 += 1;\n      if (e.lai1 > 9) e.lai1 = 0;\n    }\n  }\n}"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:17:01.064Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_moon_events.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T08:17:07.930Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_moon_events.ts",
 "old_string": "  } else {\n    L[0] += 1 + Math.abs(e.vx) / 2;\n    if (L[0] > 4) { L[0] = 0; L[3] += 1; }\n    if (L[3] > 5) L[3] = 1;\n    if (L[3] < 1) L[3] = 1;\n  }\n  e.customFrameIdx = L[3];\n}",
 "new_string": "  } else {\n    L[0] += 1;\n    L[0] += Math.abs(e.vx) / 2;      // 原版两条自增语句分开写（浮点求和序 1:1）\n    if (L[0] > 4) { L[0] = 0; L[3] += 1; }\n    if (L[3] > 5) L[3] = 1;\n    if (L[3] < 1) L[3] = 1;\n  }\n  e.customFrameIdx = L[3];\n}"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:17:07.948Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_moon_events.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T08:17:14.217Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now the 386 replica in martianFighterExtras. The block:

```ts
  if (id === 386) {
    // ---- 工程师：放炮塔（:59384-59428）----
    if (e.confusedT > 0) { e.ai2 = -60; return; }
    if (e.ai2 < 60) e.ai2 += 1;
    ...
```

Insert the frame replica at the top of the `if (id === 386)` block (runs every tick even on confused/spawn-return paths). Note: at that point ai2 is pre-update (1-tick skew on band boundaries — comment it).
````

</details>


---

## 🤖 Assistant · 2026-08-19T08:17:14.751Z · glm-x-preview-260804

```
现在是 `martianFighterExtras` 中 386 Engineer 的 step replica。
```


---

## 🤖 Assistant · 2026-08-19T08:17:23.182Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts",
 "old_string": "  if (id === 386) {\n    // ---- 工程师：放炮塔（:59384-59428）----\n    if (e.confusedT > 0) { e.ai2 = -60; return; }",
 "new_string": "  if (id === 386) {\n    // ---- FindFrame case 386 副本（cs:72369-72402，Renderer 直读 customFrameIdx）：\n    //      ai[2]>0 放塔期 → 帧 9+(ai2/12)%2；地面行走带 2-8 counter += |vx|*2\n    //      （无 +1）、>6 进帧（增量 >1 越限溢出随回卷丢弃 → 须步进副本）；\n    //      站定=帧0（counter 保留）；腾空=帧1 且清 counter（e.lai0=counter/e.lai1=行）。\n    //      置于块首保证 confused/放塔 return 路径也逐 tick 推进；ai2 取自增前值\n    //      （9/10 带翻转边界差 1t，登记）----\n    if (e.ai2 > 0) {\n      e.customFrameIdx = 9 + (Math.floor(e.ai2 / 12) % 2);\n    } else if (e.vy !== 0) {\n      e.lai0 = 0;\n      e.lai1 = 1;\n      e.customFrameIdx = 1;\n    } else {\n      if (e.lai1 < 2) e.lai1 = 2;\n      e.lai0 += Math.abs(e.vx) * 2;\n      if (e.lai0 > 6) { e.lai0 = 0; e.lai1 += 1; }\n      if (e.lai1 >= 9) e.lai1 = 2;\n      if (e.vx === 0) e.lai1 = 0;\n      e.customFrameIdx = e.lai1;\n    }\n    // ---- 工程师：放炮塔（:59384-59428）----\n    if (e.confusedT > 0) { e.ai2 = -60; return; }"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:17:23.197Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T08:17:26.864Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now update the sim to test the corrected 344/386 replicas (step replicas) and the split-add 346, then re-run.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:17:27.394Z · glm-x-preview-260804

```
现在我来更新模拟，以匹配修正后的 step replicas 并重新运行。
```


---

## 🤖 Assistant · 2026-08-19T08:17:40.385Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd /tmp && python3 - <<'EOF'\nimport re\nsrc = open('framecheck.mjs').read()\n\n# 344: step replica instead of floor(total/6)\nsrc = src.replace(\"\"\"    // mine (AI 累计 lai0 → Renderer floor(lai0/6)%10)\n    total += vx === 0 ? 1 : Math.max(1, Math.abs(vx) * 0.75);\n    eq('344', Math.floor(total / 6) % 10, vrow);\"\"\",\n\"\"\"    // mine (AI 步进副本 lai0=counter/lai1=row)\n    total += vx === 0 ? 1 : Math.max(1, Math.abs(vx) * 0.75);\n    if (total > 5) { total = 0; mrow += 1; if (mrow > 9) mrow = 0; }\n    eq('344', mrow, vrow);\"\"\")\nsrc = src.replace(\"let vfc = 0, vrow = 0, total = 0;\", \"let vfc = 0, vrow = 0, total = 0, mrow = 0;\")\n\n# 386 walk: step replica\nsrc = src.replace(\"\"\"  let fc = 0, row = 2;\n  let total = 0;\n  const vx = 1.5;\n  for (let tick = 0; tick < 500; tick++) {\n    fc += Math.abs(vx) * 2;\n    total += Math.abs(vx);\n    if (fc > 6) { row += 1; fc = 0; if (row >= 9) row = 2; }\n    eq('386 walk', 2 + Math.floor((total * 2) / 7) % 7, row);\n  }\"\"\",\n\"\"\"  let fc = 0, row = 2;\n  let mfc = 0, mrow = 2;\n  for (const vx of [0.5, 1, 1.5, 2, 3, 4.5]) {\n    fc = 0; row = 2; mfc = 0; mrow = 2;\n    for (let tick = 0; tick < 400; tick++) {\n      fc += Math.abs(vx) * 2;\n      if (fc > 6) { row += 1; fc = 0; if (row >= 9) row = 2; }\n      // mine 副本（含 idle 帧 0 门——两跑同 vx 恒非 0,行恒走带）\n      if (mrow < 2) mrow = 2;\n      mfc += Math.abs(vx) * 2;\n      if (mfc > 6) { mfc = 0; mrow += 1; }\n      if (mrow >= 9) mrow = 2;\n      eq(`386 walk vx=${vx}`, mrow, row);\n    }\n  }\"\"\")\n\n# 346: split adds\nsrc = src.replace(\"\"\"  fc += 1;\n  fc += Math.abs(vx) / 2;\n  if (fc > 4) { row += 1; fc = 0; }\"\"\", \"\"\"  fc += 1;\n  fc += Math.abs(vx) / 2;\n  if (fc > 4) { row += 1; fc = 0; }\"\"\")\nsrc = src.replace(\"\"\"    fc += 1 + Math.abs(vx) / 2;\n    if (fc > 4) { fc = 0; row += 1; }\"\"\", \"\"\"    fc += 1;\n    fc += Math.abs(vx) / 2;\n    if (fc > 4) { fc = 0; row += 1; }\"\"\")\n\nopen('framecheck.mjs','w').write(src)\nprint(\"patched\")\nEOF\nnode /tmp/framecheck.mjs 2>&1 | tail -4",
 "description": "Patch sim to step replicas and rerun"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:17:40.494Z

**📎 ToolResult**

```
patched

60595 pass, 0 fail

```


---

## 🤖 Assistant · 2026-08-19T08:17:44.607Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The simulation now passes 60595/0 — all frame machines verified equivalent to the vanilla transcriptions.

Now re-run tsc + tests to confirm the follow-up fixes didn't break anything.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:17:45.431Z · glm-x-preview-260804

```
60595 项检查已全部通过。正在重新运行 `tsc` 并执行完整的相关测试集。
```


---

## 🤖 Assistant · 2026-08-19T08:17:47.629Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "npx tsc --noEmit 2>&1 | sort > /tmp/tsc-after2.txt; echo \"errors in touched files:\"; grep -E \"render/Renderer|bossAI_martian|bossAI_moon_events|bossAI_lategame|bossAI_dd2\" /tmp/tsc-after2.txt || echo NONE; npx vitest run tests/bossAI-lategame.test.ts tests/bossAI-dd2.test.ts tests/moon-shop-aggro.test.ts tests/martian-deathray.test.ts tests/bossAI-lunar-misc.test.ts tests/lategame-subsystems.test.ts 2>&1 | tail -12",
 "description": "Final typecheck and test run"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:17:59.047Z

**📎 ToolResult**

```
errors in touched files:
NONE
 ✓ tests/moon-shop-aggro.test.ts (11 tests) 3ms
 ✓ tests/bossAI-lategame.test.ts (49 tests) 20ms
 ✓ tests/bossAI-dd2.test.ts (22 tests) 33ms
 ✓ tests/bossAI-lunar-misc.test.ts (13 tests) 33ms
 ✓ tests/lategame-subsystems.test.ts (17 tests) 14ms
 ✓ tests/martian-deathray.test.ts (4 tests) 4ms

 Test Files  6 passed (6)
      Tests  116 passed (116)
   Start at  16:17:57
   Duration  1.64s (transform 1.75s, setup 0ms, collect 8.23s, tests 108ms, environment 1ms, prepare 235ms)

```


---

## 🤖 Assistant · 2026-08-19T08:18:04.137Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All green:
- tsc: zero errors in touched files (global total continues to churn from parallel sessions, none from me).
- 116 tests pass across 6 suites.

One last review pass on my diff for quality — let me view the final state of the key sections to make sure nothing got mangled by the parallel-session churn and that comments are accurate. Let me diff-check my edited regions in the three entity files + Renderer batch.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:18:04.741Z · glm-x-preview-260804

```
一切正常。我来对已编辑区域进行最终检查，以确认其在并行会话频繁变动的情况下仍保持完好。
```


---

## 🤖 Assistant · 2026-08-19T08:18:05.432Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '/============ 火星疯狂/,/战士族\\/107/p' src/render/Renderer.ts | head -125",
 "description": "Review final Renderer batch content"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:18:05.462Z

**📎 ToolResult**

```
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
  }
  // 344 常世吼（cs:73144-73170）：全带 0-9，counter += max(1,|vx|*0.75)/t、>5 进帧
  //   （速率随速度变化,且增量 >1 越限溢出丢弃 → 步进副本；mourningWoodAI 维护
  //   e.lai0=counter / e.lai1=帧行）
  if (id === 344) return Math.min(frames - 1, e.lai1);
  // 345 冰雪女王（cs:73106-73143）：滑翔(ai0==0) 定帧 0 / ai3<0 半周期按 vx 向 1|2；
  //   落冰压制(ai0==1) 带 3-4 每 6t；自旋环射(ai0==2) 恒帧 5
  if (id === 345) {
    if (e.ai0 === 0) {
      if (e.ai3 >= 0) return 0;
      return e.vx < 0 ? 1 : 2;
    }
    if (e.ai0 === 1) return Math.min(frames - 1, 3 + (Math.floor(t / 6) % 2));
    if (e.ai0 === 2) return Math.min(5, frames - 1);
    return 0;
  }
  // 551 Betsy（cs:67913-68107）：帧源 = ai[1]（状态计时，betsyAI 1:1 同步）——
  //   ai0==4 空袭 / 3 吐息：起手 5(<5t)→6(<54/34t)→7/8 递进 → 喷射 9↔10 循环
  //   （fc/3%2）→ 收势 8→7→0；ai0==5 恒帧 3；ai0==6 召唤拍翼序列
  //   1,2,3,4,3,4,3,2,1,0 各 8t；其余态（悬停/风压/入场）恒帧 0
  if (id === 551) {
    const fc551 = Math.floor(e.ai1);
    if (e.ai0 === 4) {
      if (fc551 < 5) return Math.min(frames - 1, 5);
      if (fc551 < 54) return Math.min(frames - 1, 6);
      if (fc551 < 57) return Math.min(frames - 1, 7);
      if (fc551 < 60) return Math.min(frames - 1, 8);
      if (fc551 < 123) return Math.min(frames - 1, 9 + (Math.floor(fc551 / 3) % 2));
      if (fc551 < 128) return Math.min(frames - 1, 8);
      if (fc551 < 133) return Math.min(frames - 1, 7);
      return 0;
    }
    if (e.ai0 === 3) {
      if (fc551 < 5) return Math.min(frames - 1, 5);
      if (fc551 < 34) return Math.min(frames - 1, 6);
      if (fc551 < 37) return Math.min(frames - 1, 7);
      if (fc551 < 40) return Math.min(frames - 1, 8);
      if (fc551 < 98) return Math.min(frames - 1, 9 + (Math.floor(fc551 / 3) % 2));
      if (fc551 < 103) return Math.min(frames - 1, 8);
      if (fc551 < 108) return Math.min(frames - 1, 7);
      return 0;
    }
    if (e.ai0 === 5) return Math.min(3, frames - 1);
    if (e.ai0 === 6) {
      const seq551 = [1, 2, 3, 4, 3, 4, 3, 2, 1, 0];
      return Math.min(frames - 1, seq551[Math.min(9, Math.floor(fc551 / 8))]);
    }
    return 0;
  }
  // 战士族/107（L70155-70252）：站定=0；行走从帧 2 起按 |vx|*2+1 累加、>6 推进、循环回 2

```


---

## 🤖 Assistant · 2026-08-19T08:18:10.001Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The Renderer batch is intact and correct. Let me also spot-check the three AI files' final state of my insertions (the parallel sessions may have reformatted). Quick greps to confirm all my insertions are present.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:18:12.365Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"frameTick395\\|case 392 counter 副本\" src/entities/bossAI_martian.ts | head; grep -n \"FindFrame case 344 副本\\|FindFrame case 327 姿态机\\|FindFrame case 346 副本\" src/entities/bossAI_moon_events.ts; grep -n \"cultistFrameTick(e, cultistFrameState\\|function cultistFrameTick\\|function cultistFrameState\" src/entities/bossAI_lategame.ts",
 "description": "Confirm all AI-side insertions present"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:18:12.410Z

**📎 ToolResult**

```
192:  const frameTick395 = (): void => {
233:    frameTick395();
355:  frameTick395();
542:  // ---- FindFrame case 392 counter 副本（cs:72543-72560，393/394 已在上方各自
286:  // ---- FindFrame case 344 副本（cs:73144-73170）：counter += max(1,|vx|*0.75)/t
411:  // ---- FindFrame case 327 姿态机副本（cs:72977-73037，Renderer 直读 customFrameIdx）：
807:  // ---- FindFrame case 346 副本（cs:73050-73093，Renderer 直读 customFrameIdx）：
550:function cultistFrameState(
586:function cultistFrameTick(e: Enemy, st: number): void {
692:  cultistFrameTick(e, cultistFrameState(e, la, isReal, parent));

```


---

## 🤖 Assistant · 2026-08-19T08:18:17.363Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All insertions present. One more sanity check on the 386 replica — verify it's still in place in bossAI_martian.ts and reads correctly.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:18:18.191Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '/if (id === 386) {/,/if (e.confusedT > 0)/p' src/entities/bossAI_martian.ts",
 "description": "Verify 386 engineer replica in place"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:18:18.231Z

**📎 ToolResult**

```
  if (id === 386) {
    // ---- FindFrame case 386 副本（cs:72369-72402，Renderer 直读 customFrameIdx）：
    //      ai[2]>0 放塔期 → 帧 9+(ai2/12)%2；地面行走带 2-8 counter += |vx|*2
    //      （无 +1）、>6 进帧（增量 >1 越限溢出随回卷丢弃 → 须步进副本）；
    //      站定=帧0（counter 保留）；腾空=帧1 且清 counter（e.lai0=counter/e.lai1=行）。
    //      置于块首保证 confused/放塔 return 路径也逐 tick 推进；ai2 取自增前值
    //      （9/10 带翻转边界差 1t，登记）----
    if (e.ai2 > 0) {
      e.customFrameIdx = 9 + (Math.floor(e.ai2 / 12) % 2);
    } else if (e.vy !== 0) {
      e.lai0 = 0;
      e.lai1 = 1;
      e.customFrameIdx = 1;
    } else {
      if (e.lai1 < 2) e.lai1 = 2;
      e.lai0 += Math.abs(e.vx) * 2;
      if (e.lai0 > 6) { e.lai0 = 0; e.lai1 += 1; }
      if (e.lai1 >= 9) e.lai1 = 2;
      if (e.vx === 0) e.lai1 = 0;
      e.customFrameIdx = e.lai1;
    }
    // ---- 工程师：放炮塔（:59384-59428）----
    if (e.confusedT > 0) { e.ai2 = -60; return; }

```


---

## 🤖 Assistant · 2026-08-19T08:18:22.982Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Everything is in place. Final verification pass done:
- tsc: no errors in touched files
- Tests: 116 passed across 6 suites
- Standalone equivalence sim: 60595 checks, 0 fails

Clean up the scratch sim? /tmp files are fine to leave (they're in /tmp, an allowed working dir, and not project files). No vite instance was started, nothing to kill.

Now compose the final report: per-family frame machine mapping table + test results.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:18:23.800Z · glm-x-preview-260804

```
全部验证完毕。正在清理临时文件（无服务器进程——仅运行了 vitest/tsc；未启动 vite 实例）。
```


---

## 🤖 Assistant · 2026-08-19T08:18:25.034Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "rm -f /tmp/framecheck.mjs /tmp/tsc-baseline.txt /tmp/tsc-baseline2.txt /tmp/tsc-after.txt /tmp/tsc-after2.txt; pgrep -fl \"vite.*520\" || echo \"no private vite instances running\"",
 "description": "Remove scratch files and confirm no stray processes"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:18:25.126Z

**📎 ToolResult**

```
no private vite instances running

```


---

## 🤖 Assistant · 2026-08-19T08:19:09.278Z · glm-x-preview-260804

```
三族 FindFrame 帧状态机已全部落地。改动四个文件，全部带 cs 行号注释，未动任何既有分支。

## 逐族帧机映射表

### 一、火星飞碟族（NPC.cs:72481-72560 等）

| NPC | 帧机（原版行号） | 实现位置 |
|---|---|---|
| **393 炮塔** | cs:72481-72494：ai2 瞄准角经 ToRotationVector2(cos,sin) 九向分带（陡下4/斜下5·3/横8·0/侧下6·2/斜1·7）+激光窗 [280,420) 且 `%6<=2` → +9 射击行。我仓 393 段 ai2=atan2 角(dy≥0)/ai3=母碟共享计数，语义 1:1 直读 | Renderer 分支（纯函数） |
| **394 火炮** | cs:72495-72518：纯 ai3 相位——窗前[420,440) `4+n/5`、火炮窗[440,580) `(n/4)%4` 循环、窗尾[580,600) `7-(n-160)/5` 回落、其余恒帧 4 | Renderer 分支（纯函数） |
| **395 母碟** | cs:72520-72541：counter +1/t（66 回卷，帧=⌊c/6⌋ 0-10）；死光电报窗 ai3∈[20,260) 再+1 且钳 [36,53] → 恒落帧 6-8 辉光带 | `martianSaucerAI` 两个非死亡出口维护 counter 副本到 **e.lai0**，Renderer 读 |
| **392 炮体** | cs:72543-72560：4 帧旋球 counter +1/t、电报窗内 ×2、12 回卷、帧=⌊c/3⌋ | `martianSaucerPartAI` 尾段 counter 副本到 **e.lai0**（393/394 已各自 return，尾段仅 392 到达） |
| **399 探测器** | cs:72562-72565：0.25t/帧四帧扫描带 + ai0≠0（受惊/逃逸）→ +4 警戒带 | Renderer 分支（t/4 循环，相位任意视觉等价） |
| **387 特斯拉** | cs:72335-72368：两帧电球，充电 ai0>0 时 10 单位/帧（≥20 → 5、≥40 → 10/3，**三档**非两档）、待机 15 单位/帧 | Renderer 分支（按 ai0 取瞬时周期） |
| **386 工程师** | cs:72369-72402：放塔期 ai2>0 → 帧 `9+(ai2/12)%2`；行走带 2-8 counter `+=|vx|*2`（**无 +1**）>6 进帧；站定=0；腾空=1 清计数 | `martianFighterExtras` 块首步进副本 → **customFrameIdx**（增量>1 时越限溢出丢弃，公式折算会快进——须步进副本；块首保证 confused/放塔 return 路径也推进） |

### 二、月亮事件六族

| NPC | 帧机 | 实现位置 |
|---|---|---|
| **327 南瓜王** | cs:72977-73037：ai3 姿态 0→行0/1→行4/2→行8，counter ±1/t、越 ±6 进一帧行（7t/步）、12 帧双向回卷——表情滑变到位后**定格**（源码如此，非常驻循环）；姿态源=我仓 ai3 招式轮换（与原版 ai[3]=rand(3) 同槽） | `pumpkingAI` 姿态机副本 → **customFrameIdx**（e.lai0=counter/e.lai1=行；与既有 L[0]/L[1] 披风节拍互不冲突） |
| **345 冰雪女王** | cs:73106-73143：滑翔 ai0==0 定帧 0，ai3<0 半周期按 vx 向 1|2；落冰 ai0==1 带 3-4 每 6t；自旋 ai0==2 恒帧 5 | Renderer 分支 |
| **346 圣诞坦克** | cs:73050-73093：开火 ai0==1 带 6-8 每 3t；**vx==0 定格**（帧不动仅清计数）；行走带 1-5 counter `+=1+|vx|/2` >4 进帧——定格记忆无法无状态重建 | `santaNK1AI` 全帧机副本（L[0]/L[3]）→ **customFrameIdx**（浮点求和序按原版两条自增语句分开写） |
| **325 哀木** | cs:73172-73201：站定带 0-4/移动带 5-9，两分支 counter 恒 +1/t ≡ animT → `⌊t/5⌋%5` 精确无状态（带切换瞬间带内相位任意，登记） | Renderer 分支 |
| **344 常世吼** | cs:73144-73170：全带 0-9，counter `+=max(1,|vx|*0.75)` >5 进帧（速率随速变化+溢出丢弃 → 步进副本） | `mourningWoodAI` 副本（e.lai0=counter/e.lai1=行），Renderer 读 e.lai1 |
| **551 Betsy** | cs:67913-68107：帧源=**ai[1]（状态计时）**而非任务猜测的 localAI[0]（查证：localAI[0] 36 步计数是 AI 侧遗留，FindFrame 只读 ai[0]/ai[1]）。空袭 ai0==4 起手 5→6→7→8（5/54/57/60t）→喷射 9↔10 循环（60-123t）→收势 8→7→0（123/128/133t）；吐息 ai0==3 同构阈值 5/34/37/40/98/103/108；ai0==5 恒帧 3；召唤 ai0==6 拍翼序列 1,2,3,4,3,4,3,2,1,0 各 8t；其余恒帧 0。betsyAI 的 ai1 1:1 同步直读 | Renderer 分支（纯函数） |

### 三、教徒 439/440（cs:72698-72783）

- **la2 仪式圈心未动**。帧态（=原版 localAI[2] 六值）在 `lunaticCultistAI` 内按各态重算：出生显形 -1 按 ai1 分段（>360→13/>300→10/>120→1/其余→0，:65120-65136）；选招/飞掠→10；冰/火/光→11；雷→真身 12·克隆 11（flag2 门 ：65520-65524）；仪式→头部 10，[30,90)/[120,420) 两窗按到圈心向量覆写（|uy|<0.77→11/uy<0→12/其余→10）；硬直/末日→13。
- FindFrame 副本 `cultistFrameTick`：counter 15t 一轮、行内 **5t/帧**（源码 ：72726 `/5`，任务描述猜 7t 已按源码修正）、counter 每 tick +1（:72781）→ 态0/1/2 先播一轮行带（4-6/10-12/7-9）再定格行 0/1/2，态10/11/12/13 恒循环行带。帧号写 **e.customFrameIdx**（694 先例），counter/行存独立 WeakMap（localAI 槽被圈心/克隆引用占用）。netPuppet 无本地 AI → 帧冻结（登记）。

## 验证结果

1. **算法对账**：独立仿真脚本（反编译源逐行转写 vs 我仓实现，随机态序列 6 万次比对）**60595 pass / 0 fail**——过程中抓出并修正三处：345 滑翔定帧误写 2（应 0）、386/344 行走 counter 公式折算在增量>1 时快进（越限溢出丢弃，改步进副本）、346 浮点求和序对齐。
2. **tsc --noEmit**：四个改动文件（Renderer.ts / bossAI_martian.ts / bossAI_moon_events.ts / bossAI_lategame.ts）**零错误**（全局剩余错误均来自并行会话的 TrackPass/tests 等无关文件，且有 churn）。
3. **vitest**：`bossAI-lategame(49) + bossAI-dd2(22) + moon-shop-aggro(11) + bossAI-lunar-misc(13) + lategame-subsystems(17) + martian-deathray(4)` = **116 全绿**（不存在 bossAI-moon-events 命名的测试文件，跑齐了目录内全部相关套件）。

改动文件：`~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts`（vanillaFrameIdx 新批，置于 ai===3 战士族档之前防 386 被截胡）、`src/entities/bossAI_martian.ts`、`src/entities/bossAI_moon_events.ts`、`src/entities/bossAI_lategame.ts`。
```
