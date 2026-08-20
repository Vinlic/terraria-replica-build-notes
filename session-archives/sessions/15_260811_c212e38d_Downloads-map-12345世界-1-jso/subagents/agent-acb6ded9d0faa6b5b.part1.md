# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-12T16:26:56.090Z

```
你在 ~/Project/GLM/SandboxWorld 工作。任务:从反编译源码 "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs" 的 AI_007_TownEntities 方法中,机械转录城镇 NPC 自卫攻击状态机里 **ai[0]==10(近战态,:54747-54936 附近)与 ai[0]==12(弓态,:54936-55240 附近)** 两个分支的全部 per-type 参数块。

每个分支的结构:一串 `if (type == N) {...} else if (type == M) {...}` 参数块,块内变量含义(已确认):
- num43(近战)/num52(弓) = 发射的投射物 id
- num44/num53 = 基础伤害
- num45/num54 = 弹速
- num46/num55 = 发射 tick(进入状态后第几 tick 发射;注意块内的 `if (localAI[3] > num55) { num55 = X; flag28 = true; }` 链 = 连发升级:每过 X tick 再发一箭,flag28 标记多段)
- num47/num56 = ??? (记录原始赋值)
- maxValue/maxValue2 = ???
- num48/num58 = 弹道随机散布(±)
- knockBack/knockBack2 = 击退
- 块内还可能有 hardMode 覆盖、Main.rand 随机选弹(如 209 三选一)、PrettySafe 特判(368)等——全部照抄
- 另外记录 num57(弓态垂直瞄准偏移)在哪赋值、如何计算(在 :55160 附近的发射段)

输出:一个 JSON 对象(直接作为你的最终回复文本,不要写文件):
{
  "melee10": { "<npcType>": { "proj":…, "dmg":…, "speed":…, "shootTick":…, "extraField_num47":…, "maxValue":…, "spread":…, "kb":…, "hardMode": {…} , "special": "原文要点" }, … },
  "bow12":   { …同结构,extra 字段名 num56/maxValue2/num58… },
  "bow_num57_aim_offset": "源码行号+计算逻辑描述",
  "state_exit": "ai[1]<=0 退出时发生什么(找 state 末尾)"
}
只要转录,不要解读不要建议。数值必须逐字精确。
```

---

## 📎 Attachment · skill_listing · 2026-08-12T16:26:56.108Z

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

## 🤖 Assistant · 2026-08-12T16:27:00.045Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The task is clear: mechanically transcribe the ai[0]==10 and ai[0]==12 branches from AI_007_TownEntities in NPC.cs, lines around 54747-55240. Let me read the file.
```

</details>


---

## 🤖 Assistant · 2026-08-12T16:27:00.295Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "offset": 54600,
 "limit": 300
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:27:00.329Z

**📎 ToolResult**

```
54600									ai[1] = 240f;
54601									netUpdate = true;
54602								}
54603								if (flag26)
54604								{
54605									direction *= -1;
54606									velocity.X *= -1f;
54607									netUpdate = true;
54608								}
54609								if (keepwalking3)
54610								{
54611									ai[1] = 90f;
54612									netUpdate = true;
54613								}
54614								if (velocity.Y < 0f)
54615								{
54616									localAI[3] = position.X;
54617								}
54618							}
54619							if (velocity.Y < 0f && wet)
54620							{
54621								velocity.Y *= 1.2f;
54622							}
54623							if (velocity.Y < 0f && NPCID.Sets.TownCritter[type] && !flag7)
54624							{
54625								velocity.Y *= 1.2f;
54626							}
54627						}
54628					}
54629					else if (flag14 && !wet)
54630					{
54631						int num36 = (int)(base.Center.X / 16f);
54632						int num37 = (int)((position.Y + (float)height - 16f) / 16f);
54633						int num38 = 0;
54634						for (int num39 = -1; num39 <= 1; num39++)
54635						{
54636							for (int num40 = 1; num40 <= 6; num40++)
54637							{
54638								Tile tileSafely6 = Framing.GetTileSafely(num36 + num39, num37 + num40);
54639								if (tileSafely6.liquid > 0 || (tileSafely6.nactive() && Main.tileSolid[tileSafely6.type]))
54640								{
54641									num38++;
54642								}
54643							}
54644						}
54645						if (num38 <= 2)
54646						{
54647							if (velocity.X != 0f)
54648							{
54649								netUpdate = true;
54650							}
54651							velocity.X *= 0.2f;
54652							ai[0] = 0f;
54653							ai[1] = 50 + Main.rand.Next(50);
54654							ai[2] = 0f;
54655							localAI[3] = 40f;
54656						}
54657					}
54658				}
54659			}
54660			else if (ai[0] == 2f || ai[0] == 11f)
54661			{
54662				if (Main.netMode != 1)
54663				{
54664					localAI[3] -= 1f;
54665					if (Main.rand.Next(60) == 0 && localAI[3] == 0f)
54666					{
54667						localAI[3] = 60f;
54668						direction *= -1;
54669						netUpdate = true;
54670					}
54671				}
54672				ai[1] -= 1f;
54673				velocity.X *= 0.8f;
54674				if (ai[1] <= 0f)
54675				{
54676					localAI[3] = 40f;
54677					ai[0] = 0f;
54678					ai[1] = 60 + Main.rand.Next(60);
54679					netUpdate = true;
54680				}
54681			}
54682			else if (ai[0] == 3f || ai[0] == 4f || ai[0] == 5f || ai[0] == 8f || ai[0] == 9f || ai[0] == 16f || ai[0] == 17f || ai[0] == 20f || ai[0] == 21f || ai[0] == 22f || ai[0] == 23f)
54683			{
54684				velocity.X *= 0.8f;
54685				ai[1] -= 1f;
54686				if (ai[0] == 8f && ai[1] < 60f && flag16)
54687				{
54688					ai[1] = 180f;
54689					netUpdate = true;
54690				}
54691				if (ai[0] == 5f)
54692				{
54693					Point coords = (base.Bottom + Vector2.UnitY * -2f).ToTileCoordinates();
54694					Tile tile = Main.tile[coords.X, coords.Y];
54695					if (tile != null && tile.type != 15 && tile.type != 497)
54696					{
54697						ai[1] = 0f;
54698					}
54699					else
54700					{
54701						Main.sittingManager.AddNPC(whoAmI, coords);
54702					}
54703				}
54704				if (ai[1] <= 0f)
54705				{
54706					ai[0] = 0f;
54707					ai[1] = 60 + Main.rand.Next(60);
54708					ai[2] = 0f;
54709					localAI[3] = 30 + Main.rand.Next(60);
54710					netUpdate = true;
54711				}
54712			}
54713			else if (ai[0] == 6f || ai[0] == 7f || ai[0] == 18f || ai[0] == 19f)
54714			{
54715				if (ai[0] == 18f && (localAI[3] < 1f || localAI[3] > 2f))
54716				{
54717					localAI[3] = 2f;
54718				}
54719				velocity.X *= 0.8f;
54720				ai[1] -= 1f;
54721				int num41 = (int)ai[2];
54722				if (num41 < 0 || num41 > 255 || !Main.player[num41].CanBeTalkedTo || Main.player[num41].Distance(base.Center) > 200f || !Collision.CanHitLine(base.Top, 0, 0, Main.player[num41].Top, 0, 0))
54723				{
54724					ai[1] = 0f;
54725				}
54726				if (ai[1] > 0f)
54727				{
54728					int num42 = ((base.Center.X < Main.player[num41].Center.X) ? 1 : (-1));
54729					if (num42 != direction)
54730					{
54731						netUpdate = true;
54732					}
54733					direction = num42;
54734				}
54735				else
54736				{
54737					ai[0] = 0f;
54738					ai[1] = 60 + Main.rand.Next(60);
54739					ai[2] = 0f;
54740					localAI[3] = 30 + Main.rand.Next(60);
54741					netUpdate = true;
54742				}
54743			}
54744			else if (ai[0] == 10f)
54745			{
54746				int num43 = 0;
54747				int num44 = 0;
54748				float knockBack = 0f;
54749				float num45 = 0f;
54750				int num46 = 0;
54751				int num47 = 0;
54752				int maxValue = 0;
54753				float num48 = 0f;
54754				float num49 = NPCID.Sets.DangerDetectRange[type];
54755				float num50 = 0f;
54756				if ((float)NPCID.Sets.AttackTime[type] == ai[1])
54757				{
54758					frameCounter = 0.0;
54759					localAI[3] = 0f;
54760				}
54761				if (type == 38)
54762				{
54763					num43 = 30;
54764					num45 = 6f;
54765					num44 = 20;
54766					num46 = 10;
54767					num47 = 180;
54768					maxValue = 120;
54769					num48 = 16f;
54770					knockBack = 7f;
54771				}
54772				else if (type == 633)
54773				{
54774					num43 = 880;
54775					num45 = 24f;
54776					num44 = 15;
54777					num46 = 1;
54778					num48 = 0f;
54779					knockBack = 7f;
54780					num47 = 15;
54781					maxValue = 10;
54782					if (ShouldBestiaryGirlBeLycantrope())
54783					{
54784						num43 = 929;
54785						num44 = (int)((float)num44 * 1.5f);
54786					}
54787				}
54788				else if (type == 550)
54789				{
54790					num43 = 669;
54791					num45 = 6f;
54792					num44 = 24;
54793					num46 = 10;
54794					num47 = 120;
54795					maxValue = 60;
54796					num48 = 16f;
54797					knockBack = 9f;
54798				}
54799				else if (type == 588)
54800				{
54801					num43 = 721;
54802					num45 = 8f;
54803					num44 = 15;
54804					num46 = 5;
54805					num47 = 20;
54806					maxValue = 10;
54807					num48 = 16f;
54808					knockBack = 9f;
54809				}
54810				else if (type == 208)
54811				{
54812					num43 = 588;
54813					num45 = 6f;
54814					num44 = 30;
54815					num46 = 10;
54816					num47 = 60;
54817					maxValue = 120;
54818					num48 = 16f;
54819					knockBack = 6f;
54820				}
54821				else if (type == 17)
54822				{
54823					num43 = 48;
54824					num45 = 9f;
54825					num44 = 12;
54826					num46 = 10;
54827					num47 = 60;
54828					maxValue = 60;
54829					num48 = 16f;
54830					knockBack = 1.5f;
54831				}
54832				else if (type == 369)
54833				{
54834					num43 = 520;
54835					num45 = 12f;
54836					num44 = 10;
54837					num46 = 10;
54838					num47 = 0;
54839					maxValue = 1;
54840					num48 = 16f;
54841					knockBack = 3f;
54842				}
54843				else if (type == 453)
54844				{
54845					num43 = 21;
54846					num45 = 14f;
54847					num44 = 14;
54848					num46 = 10;
54849					num47 = 0;
54850					maxValue = 1;
54851					num48 = 16f;
54852					knockBack = 3f;
54853				}
54854				else if (type == 107)
54855				{
54856					num43 = 24;
54857					num45 = 5f;
54858					num44 = 15;
54859					num46 = 10;
54860					num47 = 60;
54861					maxValue = 60;
54862					num48 = 16f;
54863					knockBack = 1f;
54864				}
54865				else if (type == 124)
54866				{
54867					num43 = 582;
54868					num45 = 10f;
54869					num44 = 11;
54870					num46 = 1;
54871					num47 = 30;
54872					maxValue = 30;
54873					knockBack = 3.5f;
54874				}
54875				else if (type == 18)
54876				{
54877					num43 = 583;
54878					num45 = 8f;
54879					num44 = 8;
54880					num46 = 1;
54881					num47 = 15;
54882					maxValue = 10;
54883					knockBack = 2f;
54884					num48 = 10f;
54885				}
54886				else if (type == 142)
54887				{
54888					num43 = 589;
54889					num45 = 7f;
54890					num44 = 22;
54891					num46 = 1;
54892					num47 = 10;
54893					maxValue = 1;
54894					knockBack = 2f;
54895					num48 = 10f;
54896				}
54897				num44 = GetAttackDamage_ForTownNPC((float)num44 * num2);
54898				velocity.X *= 0.8f;
54899				ai[1] -= 1f;

```


---

## 🤖 Assistant · 2026-08-12T16:27:00.531Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "offset": 54900,
 "limit": 400
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:27:00.555Z

**📎 ToolResult**

```
54900				localAI[3] += 1f;
54901				if (localAI[3] == (float)num46 && Main.netMode != 1)
54902				{
54903					Vector2 vec = -Vector2.UnitY;
54904					if (num15 == 1 && spriteDirection == 1 && num17 != -1)
54905					{
54906						vec = DirectionTo(Main.npc[num17].Center + new Vector2(0f, (0f - num48) * MathHelper.Clamp(Distance(Main.npc[num17].Center) / num49, 0f, 1f)));
54907					}
54908					if (num15 == -1 && spriteDirection == -1 && num16 != -1)
54909					{
54910						vec = DirectionTo(Main.npc[num16].Center + new Vector2(0f, (0f - num48) * MathHelper.Clamp(Distance(Main.npc[num16].Center) / num49, 0f, 1f)));
54911					}
54912					if (vec.HasNaNs() || Math.Sign(vec.X) != spriteDirection)
54913					{
54914						vec = new Vector2(spriteDirection, -1f);
54915					}
54916					vec *= num45;
54917					vec += Utils.RandomVector2(Main.rand, 0f - num50, num50);
54918					int num51 = 1000;
54919					num51 = ((type == 124) ? Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec.X, vec.Y, num43, num44, knockBack, Main.myPlayer, 0f, whoAmI, townNpcVariationIndex) : ((type != 142) ? Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec.X, vec.Y, num43, num44, knockBack, Main.myPlayer) : Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec.X, vec.Y, num43, num44, knockBack, Main.myPlayer, 0f, Main.rand.Next(5))));
54920					Main.projectile[num51].npcProj = true;
54921					Main.projectile[num51].noDropItem = true;
54922					if (type == 588)
54923					{
54924						Main.projectile[num51].timeLeft = 480;
54925					}
54926				}
54927				if (ai[1] <= 0f && 0 == 0)
54928				{
54929					ai[0] = ((localAI[2] == 8f && flag16) ? 8 : 0);
54930					ai[1] = num47 + Main.rand.Next(maxValue);
54931					ai[2] = 0f;
54932					localAI[1] = (localAI[3] = num47 / 2 + Main.rand.Next(maxValue));
54933					netUpdate = true;
54934				}
54935			}
54936			else if (ai[0] == 12f)
54937			{
54938				int num52 = 0;
54939				int num53 = 0;
54940				float num54 = 0f;
54941				int num55 = 0;
54942				int num56 = 0;
54943				int maxValue2 = 0;
54944				float knockBack2 = 0f;
54945				int num57 = 0;
54946				bool flag28 = false;
54947				float num58 = 0f;
54948				if ((float)NPCID.Sets.AttackTime[type] == ai[1])
54949				{
54950					frameCounter = 0.0;
54951					localAI[3] = 0f;
54952				}
54953				int num59 = -1;
54954				if (num15 == 1 && spriteDirection == 1)
54955				{
54956					num59 = num17;
54957				}
54958				if (num15 == -1 && spriteDirection == -1)
54959				{
54960					num59 = num16;
54961				}
54962				if (type == 19)
54963				{
54964					num52 = 14;
54965					num54 = 13f;
54966					num53 = 24;
54967					num56 = 14;
54968					maxValue2 = 4;
54969					knockBack2 = 3f;
54970					num55 = 1;
54971					num58 = 0.5f;
54972					if ((float)NPCID.Sets.AttackTime[type] == ai[1])
54973					{
54974						frameCounter = 0.0;
54975						localAI[3] = 0f;
54976					}
54977					if (Main.hardMode)
54978					{
54979						num53 = 15;
54980						if (localAI[3] > (float)num55)
54981						{
54982							num55 = 10;
54983							flag28 = true;
54984						}
54985						if (localAI[3] > (float)num55)
54986						{
54987							num55 = 20;
54988							flag28 = true;
54989						}
54990						if (localAI[3] > (float)num55)
54991						{
54992							num55 = 30;
54993							flag28 = true;
54994						}
54995					}
54996				}
54997				else if (type == 227)
54998				{
54999					num52 = 587;
55000					num54 = 10f;
55001					num53 = 8;
55002					num56 = 10;
55003					maxValue2 = 1;
55004					knockBack2 = 1.75f;
55005					num55 = 1;
55006					num58 = 0.5f;
55007					if (localAI[3] > (float)num55)
55008					{
55009						num55 = 12;
55010						flag28 = true;
55011					}
55012					if (localAI[3] > (float)num55)
55013					{
55014						num55 = 24;
55015						flag28 = true;
55016					}
55017					if (Main.hardMode)
55018					{
55019						num53 += 2;
55020					}
55021				}
55022				else if (type == 368)
55023				{
55024					num52 = 14;
55025					num54 = 13f;
55026					num53 = 24;
55027					num56 = 12;
55028					maxValue2 = 5;
55029					knockBack2 = 2f;
55030					num55 = 1;
55031					num58 = 0.2f;
55032					if (Main.hardMode)
55033					{
55034						num53 = 30;
55035						num52 = 357;
55036					}
55037				}
55038				else if (type == 22)
55039				{
55040					num54 = 10f;
55041					num53 = 12;
55042					num55 = 1;
55043					if (Main.hardMode)
55044					{
55045						num52 = 2;
55046						num56 = 15;
55047						maxValue2 = 10;
55048						num53 += 6;
55049					}
55050					else
55051					{
55052						num52 = 1;
55053						num56 = 30;
55054						maxValue2 = 20;
55055					}
55056					knockBack2 = 2.75f;
55057					num57 = 4;
55058					num58 = 0.7f;
55059				}
55060				else if (type == 228)
55061				{
55062					num52 = 267;
55063					num54 = 14f;
55064					num53 = 20;
55065					num55 = 1;
55066					num56 = 10;
55067					maxValue2 = 1;
55068					knockBack2 = 3f;
55069					num57 = 6;
55070					num58 = 0.4f;
55071				}
55072				else if (type == 178)
55073				{
55074					num52 = 242;
55075					num54 = 13f;
55076					num53 = ((!Main.hardMode) ? 11 : 15);
55077					num56 = 10;
55078					maxValue2 = 1;
55079					knockBack2 = 2f;
55080					num55 = 1;
55081					if (localAI[3] > (float)num55)
55082					{
55083						num55 = 8;
55084						flag28 = true;
55085					}
55086					if (localAI[3] > (float)num55)
55087					{
55088						num55 = 16;
55089						flag28 = true;
55090					}
55091					num58 = 0.3f;
55092				}
55093				else if (type == 229)
55094				{
55095					num52 = 14;
55096					num54 = 14f;
55097					num53 = 24;
55098					num56 = 10;
55099					maxValue2 = 1;
55100					knockBack2 = 2f;
55101					num55 = 1;
55102					num58 = 0.7f;
55103					if (localAI[3] > (float)num55)
55104					{
55105						num55 = 16;
55106						flag28 = true;
55107					}
55108					if (localAI[3] > (float)num55)
55109					{
55110						num55 = 24;
55111						flag28 = true;
55112					}
55113					if (localAI[3] > (float)num55)
55114					{
55115						num55 = 32;
55116						flag28 = true;
55117					}
55118					if (localAI[3] > (float)num55)
55119					{
55120						num55 = 40;
55121						flag28 = true;
55122					}
55123					if (localAI[3] > (float)num55)
55124					{
55125						num55 = 48;
55126						flag28 = true;
55127					}
55128					if (localAI[3] == 0f && num59 != -1 && Distance(Main.npc[num59].Center) < (float)NPCID.Sets.PrettySafe[type])
55129					{
55130						num58 = 0.1f;
55131						num52 = 162;
55132						num53 = 50;
55133						knockBack2 = 10f;
55134						num54 = 24f;
55135					}
55136				}
55137				else if (type == 209)
55138				{
55139					num52 = Utils.SelectRandom<int>(Main.rand, 134, 133, 135);
55140					num55 = 1;
55141					switch (num52)
55142					{
55143					case 135:
55144						num54 = 12f;
55145						num53 = 30;
55146						num56 = 30;
55147						maxValue2 = 10;
55148						knockBack2 = 7f;
55149						num58 = 0.2f;
55150						break;
55151					case 133:
55152						num54 = 10f;
55153						num53 = 25;
55154						num56 = 10;
55155						maxValue2 = 1;
55156						knockBack2 = 6f;
55157						num58 = 0.2f;
55158						break;
55159					case 134:
55160						num54 = 13f;
55161						num53 = 20;
55162						num56 = 20;
55163						maxValue2 = 10;
55164						knockBack2 = 4f;
55165						num58 = 0.1f;
55166						break;
55167					}
55168				}
55169				num53 = GetAttackDamage_ForTownNPC((float)num53 * num2);
55170				velocity.X *= 0.8f;
55171				ai[1] -= 1f;
55172				localAI[3] += 1f;
55173				if (localAI[3] == (float)num55 && Main.netMode != 1)
55174				{
55175					Vector2 vec2 = Vector2.Zero;
55176					if (num59 != -1)
55177					{
55178						vec2 = DirectionTo(Main.npc[num59].Center + new Vector2(0f, -num57));
55179					}
55180					if (vec2.HasNaNs() || Math.Sign(vec2.X) != spriteDirection)
55181					{
55182						vec2 = new Vector2(spriteDirection, 0f);
55183					}
55184					vec2 *= num54;
55185					vec2 += Utils.RandomVector2(Main.rand, 0f - num58, num58);
55186					int num60 = 1000;
55187					num60 = ((type != 227) ? Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec2.X, vec2.Y, num52, num53, knockBack2, Main.myPlayer) : Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec2.X, vec2.Y, num52, num53, knockBack2, Main.myPlayer, 0f, (float)Main.rand.Next(12) / 6f));
55188					Main.projectile[num60].npcProj = true;
55189					Main.projectile[num60].noDropItem = true;
55190				}
55191				if (localAI[3] == (float)num55 && flag28 && num59 != -1)
55192				{
55193					Vector2 vector4 = DirectionTo(Main.npc[num59].Center);
55194					if (vector4.Y <= 0.5f && vector4.Y >= -0.5f)
55195					{
55196						ai[2] = vector4.Y;
55197					}
55198				}
55199				if (ai[1] <= 0f && 0 == 0)
55200				{
55201					ai[0] = ((localAI[2] == 8f && flag16) ? 8 : 0);
55202					ai[1] = num56 + Main.rand.Next(maxValue2);
55203					ai[2] = 0f;
55204					localAI[1] = (localAI[3] = num56 / 2 + Main.rand.Next(maxValue2));
55205					netUpdate = true;
55206				}
55207			}
55208			else if (ai[0] == 13f)
55209			{
55210				velocity.X *= 0.8f;
55211				if ((float)NPCID.Sets.AttackTime[type] == ai[1])
55212				{
55213					frameCounter = 0.0;
55214				}
55215				ai[1] -= 1f;
55216				localAI[3] += 1f;
55217				if (localAI[3] == 1f && Main.netMode != 1)
55218				{
55219					Vector2 vec3 = DirectionTo(Main.npc[(int)ai[2]].Center + new Vector2(0f, -20f));
55220					if (vec3.HasNaNs() || Math.Sign(vec3.X) == -spriteDirection)
55221					{
55222						vec3 = new Vector2(spriteDirection, -1f);
55223					}
55224					vec3 *= 8f;
55225					int num61 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec3.X, vec3.Y, 584, 0, 0f, Main.myPlayer, ai[2]);
55226					Main.projectile[num61].npcProj = true;
55227					Main.projectile[num61].noDropItem = true;
55228				}
55229				if (ai[1] <= 0f)
55230				{
55231					ai[0] = 0f;
55232					ai[1] = 10 + Main.rand.Next(10);
55233					ai[2] = 0f;
55234					localAI[3] = 5 + Main.rand.Next(10);
55235					netUpdate = true;
55236				}
55237			}
55238			else if (ai[0] == 14f)
55239			{
55240				int num62 = 0;
55241				int num63 = 0;
55242				float num64 = 0f;
55243				int num65 = 0;
55244				int num66 = 0;
55245				int maxValue3 = 0;
55246				float knockBack3 = 0f;
55247				float num67 = 0f;
55248				float num68 = NPCID.Sets.DangerDetectRange[type];
55249				float num69 = 1f;
55250				float num70 = 0f;
55251				if ((float)NPCID.Sets.AttackTime[type] == ai[1])
55252				{
55253					frameCounter = 0.0;
55254					localAI[3] = 0f;
55255				}
55256				int num71 = -1;
55257				if (num15 == 1 && spriteDirection == 1)
55258				{
55259					num71 = num17;
55260				}
55261				if (num15 == -1 && spriteDirection == -1)
55262				{
55263					num71 = num16;
55264				}
55265				if (type == 54)
55266				{
55267					num62 = 585;
55268					num64 = 10f;
55269					num63 = 16;
55270					num65 = 30;
55271					num66 = 20;
55272					maxValue3 = 15;
55273					knockBack3 = 2f;
55274					num70 = 1f;
55275				}
55276				else if (type == 108)
55277				{
55278					num62 = 15;
55279					num64 = 6f;
55280					num63 = 18;
55281					num65 = 15;
55282					num66 = 15;
55283					maxValue3 = 5;
55284					knockBack3 = 3f;
55285					num67 = 20f;
55286				}
55287				else if (type == 160)
55288				{
55289					num62 = 590;
55290					num63 = 40;
55291					num65 = 15;
55292					num66 = 10;
55293					maxValue3 = 1;
55294					knockBack3 = 3f;
55295					for (; localAI[3] > (float)num65; num65 += 15)
55296					{
55297					}
55298				}
55299				else if (type == 663)

```


---

## 🤖 Assistant · 2026-08-12T16:27:18.373Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have all the data I need. Both branches fully read (54744-55207). Let me transcribe precisely into JSON.

melee10 types: 38, 633, 550, 588, 208, 17, 369, 453, 107, 124, 18, 142.

For 124: num48 never assigned (stays 0). Actually num48 initialized 0f at 54753; 124 block doesn't set num48. Also note fire code uses num48 for aim offset (not spread — interesting, in melee branch num48 is used as aim elevation offset clamped by num49/num50; num50 is the random spread, initialized 0f and never assigned). I should note num50 stays 0 for all melee types (no assignment in any block). Record exact.

Also note the melee exit at 54927-54934. Bow exit 55199-55206. Both same shape.

num57 assignments: type 22 → 4; 228 → 6; others no assignment (default 0). Computed use at 55178: vec2 = DirectionTo(target.Center + (0, -num57)) — aim offset upward by num57 pixels.

flag28 extra: at 55191-55198, if fired && flag28 && target valid, vector4 = DirectionTo(target.Center); if Y in [-0.5,0.5] then ai[2] = vector4.Y. Interesting: actually reads `ai[2] = vector4.Y` — wait, decompiled shows `ai[2] = vector4.Y;`? Yes line 55196.

Now write JSON as final response. Values must be verbatim.

melee10:
- 38: proj 30, dmg 20, speed 6f, shootTick 10, num47 180, maxValue 120, spread num48 16f, kb 7f. special: none.
- 633: proj 880, dmg 15, speed 24f, tick 1, num47 15, maxValue 10, num48 0f (unassigned), kb 7f. special: if ShouldBestiaryGirlBeLycantrope() → num43=929, num44=(int)((float)num44*1.5f).
- 550: proj 669, dmg 24, speed 6, tick 10, num47 120, maxValue 60, num48 16f, kb 9f.
- 588: proj 721, dmg 15, speed 8, tick 5, num47 20, maxValue 10, num48 16f, kb 9f. special: projectile timeLeft=480 (line 54922-54925).
- 208: proj 588, dmg 30, speed 6, tick 10, num47 60, maxValue 120, num48 16f, kb 6f.
- 17: proj 48, dmg 12, speed 9, tick 10, num47 60, maxValue 60, num48 16f, kb 1.5f.
- 369: proj 520, dmg 10, speed 12, tick 10, num47 0, maxValue 1, num48 16f, kb 3f.
- 453: proj 21, dmg 14, speed 14, tick 10, num47 0, maxValue 1, num48 16f, kb 3f.
- 107: proj 24, dmg 15, speed 5, tick 10, num47 60, maxValue 60, num48 16f, kb 1f.
- 124: proj 582, dmg 11, speed 10, tick 1, num47 30, maxValue 30, num48 0f (未赋值), kb 3.5f. special: NewProjectile 带 ai0=0f, ai1=whoAmI, ai2=townNpcVariationIndex.
- 18: proj 583, dmg 8, speed 8, tick 1, num47 15, maxValue 10, num48 10f, kb 2f.
- 142: proj 589, dmg 22, speed 7, tick 1, num47 10, maxValue 1, num48 10f, kb 2f. special: NewProjectile ai0=0f, ai1=Main.rand.Next(5).

Note: num44 = GetAttackDamage_ForTownNPC(num44 * num2) at 54897, applies to all.

bow12:
- 19: proj 14, dmg 24, speed 13, tick 1, num56 14, maxValue2 4, num58 0.5f, kb 3f, num57 0. hardMode: num53=15; 连发链 num55 1→10→20→30 flag28. Also duplicate frameCounter reset check inside block (54972-54976).
- 227: proj 587, dmg 8, speed 10, tick 1, num56 10, maxValue2 1, num58 0.5f, kb 1.75f. 连发: 1→12→24. hardMode: num53+=2. special: NewProjectile ai1=(float)Main.rand.Next(12)/6f.
- 368: proj 14, dmg 24, speed 13, tick 1, num56 12, maxValue2 5, num58 0.2f, kb 2f. hardMode: num53=30, num52=357. (PrettySafe not in this block actually — user mentioned 368 PrettySafe but actually PrettySafe is in 229 block. 368 is the Tavernkeep? No, 368 is... whatever. I transcribe what's there. Note: PrettySafe check is in type 229 block, not 368. I should flag this correction.)
- 22: proj — hardMode? 2 : 1; dmg 12 (hardMode +6 → 18); speed 10; tick 1; num56 hardMode 15 else 30; maxValue2 hardMode 10 else 20; num58 0.7f; kb 2.75f; num57 4.
- 228: proj 267, dmg 20, speed 14, tick 1, num56 10, maxValue2 1, num58 0.4f, kb 3f, num57 6.
- 178: proj 242, dmg hardMode?15:11, speed 13, tick 1, num56 10, maxValue2 1, num58 0.3f, kb 2f. 连发 1→8→16.
- 229: proj 14, dmg 24, speed 14, tick 1, num56 10, maxValue2 1, num58 0.7f, kb 2f. 连发 1→16→24→32→40→48 (6 links). PrettySafe: localAI[3]==0 && num59!=-1 && Distance < NPCID.Sets.PrettySafe[type] → num58=0.1f, num52=162, num53=50, knockBack2=10f, num54=24f.
- 209: proj = Utils.SelectRandom<int>(Main.rand, 134, 133, 135), tick 1, switch: 135 → speed 12, dmg 30, num56 30, maxValue2 10, kb 7f, num58 0.2f; 133 → speed 10, dmg 25, num56 10, maxValue2 1, kb 6f, num58 0.2f; 134 → speed 13, dmg 20, num56 20, maxValue2 10, kb 4f, num58 0.1f.

num57 aim offset: assigned only in type 22 (=4) and 228 (=6) blocks; default 0. Used at 55178: vec2 = DirectionTo(Main.npc[num59].Center + new Vector2(0f, -num57)) — target center raised by num57 pixels before direction calc.

state_exit:
- melee (54927-54934): if ai[1]<=0: ai[0] = (localAI[2]==8f && flag16) ? 8 : 0; ai[1] = num47 + Main.rand.Next(maxValue); ai[2]=0f; localAI[1]=localAI[3]=num47/2 + Main.rand.Next(maxValue); netUpdate=true.
- bow (55199-55206): same shape with num56/maxValue2.

Also note flag28 side effect 55191-55198.

Output JSON directly.
```

</details>


---

## 🤖 Assistant · 2026-08-12T16:27:40.848Z · glm-x-preview-260804

````
```json
{
  "melee10": {
    "38": { "proj": 30, "dmg": 20, "speed": "6f", "shootTick": 10, "extraField_num47": 180, "maxValue": 120, "spread_num48": "16f", "kb": "7f", "hardMode": null, "special": "无" },
    "633": { "proj": 880, "dmg": 15, "speed": "24f", "shootTick": 1, "extraField_num47": 15, "maxValue": 10, "spread_num48": "0f(块内未赋值,保持初始0)", "kb": "7f", "hardMode": null, "special": "if (ShouldBestiaryGirlBeLycantrope()) { num43=929; num44=(int)((float)num44*1.5f); }" },
    "550": { "proj": 669, "dmg": 24, "speed": "6f", "shootTick": 10, "extraField_num47": 120, "maxValue": 60, "spread_num48": "16f", "kb": "9f", "hardMode": null, "special": "无" },
    "588": { "proj": 721, "dmg": 15, "speed": "8f", "shootTick": 5, "extraField_num47": 20, "maxValue": 10, "spread_num48": "16f", "kb": "9f", "hardMode": null, "special": "发射后 :54922-54925 if (type==588) Main.projectile[num51].timeLeft = 480" },
    "208": { "proj": 588, "dmg": 30, "speed": "6f", "shootTick": 10, "extraField_num47": 60, "maxValue": 120, "spread_num48": "16f", "kb": "6f", "hardMode": null, "special": "无" },
    "17": { "proj": 48, "dmg": 12, "speed": "9f", "shootTick": 10, "extraField_num47": 60, "maxValue": 60, "spread_num48": "16f", "kb": "1.5f", "hardMode": null, "special": "无" },
    "369": { "proj": 520, "dmg": 10, "speed": "12f", "shootTick": 10, "extraField_num47": 0, "maxValue": 1, "spread_num48": "16f", "kb": "3f", "hardMode": null, "special": "无" },
    "453": { "proj": 21, "dmg": 14, "speed": "14f", "shootTick": 10, "extraField_num47": 0, "maxValue": 1, "spread_num48": "16f", "kb": "3f", "hardMode": null, "special": "无" },
    "107": { "proj": 24, "dmg": 15, "speed": "5f", "shootTick": 10, "extraField_num47": 60, "maxValue": 60, "spread_num48": "16f", "kb": "1f", "hardMode": null, "special": "无" },
    "124": { "proj": 582, "dmg": 11, "speed": "10f", "shootTick": 1, "extraField_num47": 30, "maxValue": 30, "spread_num48": "0f(块内未赋值,保持初始0)", "kb": "3.5f", "hardMode": null, "special": ":54919 NewProjectile 尾参特化: ai0=0f, ai1=whoAmI, ai2=townNpcVariationIndex" },
    "18": { "proj": 583, "dmg": 8, "speed": "8f", "shootTick": 1, "extraField_num47": 15, "maxValue": 10, "spread_num48": "10f", "kb": "2f", "hardMode": null, "special": "无" },
    "142": { "proj": 589, "dmg": 22, "speed": "7f", "shootTick": 1, "extraField_num47": 10, "maxValue": 1, "spread_num48": "10f", "kb": "2f", "hardMode": null, "special": ":54919 NewProjectile 尾参特化: ai0=0f, ai1=Main.rand.Next(5)" }
  },
  "melee10_shared": {
    "damage_scale": ":54897 num44 = GetAttackDamage_ForTownNPC((float)num44 * num2) — 对所有 type 统一缩放",
    "aim_not_spread": "近战态 num48 不是随机散布,是瞄准上抬补偿: :54903-54915 vec 初值 -Vector2.UnitY;若朝向侧有目标(num17/num16)则 vec = DirectionTo(目标.Center + (0, -num48 * MathHelper.Clamp(Distance/num49,0,1))),num49 = NPCID.Sets.DangerDetectRange[type](:54754);无效或符号不匹配则回退 new Vector2(spriteDirection, -1f)",
    "random_spread": "近战态真正散布是 num50: :54755 初始化 0f 且所有块均不赋值; :54917 vec += Utils.RandomVector2(Main.rand, -num50, num50) — 恒为 0",
    "spawn": ":54919 位置 base.Center.X + spriteDirection*16, base.Center.Y - 2;发射条件 localAI[3] == num46 且 Main.netMode != 1;发射后统一 npcProj=true, noDropItem=true"
  },
  "bow12": {
    "19": { "proj": 14, "dmg": 24, "speed": "13f", "shootTick": 1, "extraField_num56": 14, "maxValue2": 4, "spread_num58": "0.5f", "kb": "3f", "num57": 0, "hardMode": { "num53": 15, "burst_chain": "localAI[3]>num55 时: num55 1→10→20→30, 每次 flag28=true" }, "special": "块内 :54972-54976 重复了一份 if (NPCID.Sets.AttackTime[type]==ai[1]) { frameCounter=0; localAI[3]=0; }(与 :54948 外层重复)" },
    "227": { "proj": 587, "dmg": 8, "speed": "10f", "shootTick": 1, "extraField_num56": 10, "maxValue2": 1, "spread_num58": "0.5f", "kb": "1.75f", "num57": 0, "hardMode": { "num53": "+= 2 (8→10)" }, "special": "连发链: localAI[3]>num55 时 num55 1→12→24, 每次 flag28=true; :55187 NewProjectile 尾参 ai1=(float)Main.rand.Next(12)/6f" },
    "368": { "proj": 14, "dmg": 24, "speed": "13f", "shootTick": 1, "extraField_num56": 12, "maxValue2": 5, "spread_num58": "0.2f", "kb": "2f", "num57": 0, "hardMode": { "num53": 30, "num52": 357 }, "special": "注意: PrettySafe 特判不在此块,在 229 块" },
    "22": { "proj": "hardMode ? 2 : 1", "dmg": 12, "speed": "10f", "shootTick": 1, "extraField_num56": "hardMode ? 15 : 30", "maxValue2": "hardMode ? 10 : 20", "spread_num58": "0.7f", "kb": "2.75f", "num57": 4, "hardMode": { "num52": 2, "num56": 15, "maxValue2": 10, "num53": "12 += 6 → 18" }, "special": "非硬直模式分支: num52=1, num56=30, maxValue2=20" },
    "228": { "proj": 267, "dmg": 20, "speed": "14f", "shootTick": 1, "extraField_num56": 10, "maxValue2": 1, "spread_num58": "0.4f", "kb": "3f", "num57": 6, "hardMode": null, "special": "无" },
    "178": { "proj": 242, "dmg": "!hardMode ? 11 : 15", "speed": "13f", "shootTick": 1, "extraField_num56": 10, "maxValue2": 1, "spread_num58": "0.3f", "kb": "2f", "num57": 0, "hardMode": { "num53": 15 }, "special": "连发链: localAI[3]>num55 时 num55 1→8→16, 每次 flag28=true" },
    "229": { "proj": 14, "dmg": 24, "speed": "14f", "shootTick": 1, "extraField_num56": 10, "maxValue2": 1, "spread_num58": "0.7f", "kb": "2f", "num57": 0, "hardMode": null, "special": "连发链(6段): localAI[3]>num55 时 num55 1→16→24→32→40→48, 每次 flag28=true; PrettySafe 特判 :55128-55135: localAI[3]==0f && num59!=-1 && Distance(Main.npc[num59].Center) < (float)NPCID.Sets.PrettySafe[type] 时 { num58=0.1f; num52=162; num53=50; knockBack2=10f; num54=24f; }" },
    "209": { "proj": "Utils.SelectRandom<int>(Main.rand, 134, 133, 135)", "dmg": "per-proj", "speed": "per-proj", "shootTick": 1, "extraField_num56": "per-proj", "maxValue2": "per-proj", "spread_num58": "per-proj", "kb": "per-proj", "num57": 0, "hardMode": null, "special": ":55139 num52 三选一后 switch(num52): case 135 → num54=12f, num53=30, num56=30, maxValue2=10, knockBack2=7f, num58=0.2f; case 133 → num54=10f, num53=25, num56=10, maxValue2=1, knockBack2=6f, num58=0.2f; case 134 → num54=13f, num53=20, num56=20, maxValue2=10, knockBack2=4f, num58=0.1f" }
  },
  "bow12_shared": {
    "damage_scale": ":55169 num53 = GetAttackDamage_ForTownNPC((float)num53 * num2) — 对所有 type 统一缩放",
    "target_pick": ":54953-54961 num59 = (num15==1 && spriteDirection==1) ? num17 : (num15==-1 && spriteDirection==-1) ? num16 : -1",
    "spawn": ":55187 位置 base.Center.X + spriteDirection*16, base.Center.Y - 2;发射条件 localAI[3] == num55 且 Main.netMode != 1;发射后统一 npcProj=true, noDropItem=true;散布 vec2 += Utils.RandomVector2(Main.rand, -num58, num58) (:55185)",
    "flag28_side_effect": ":55191-55198 if (localAI[3]==(float)num55 && flag28 && num59!=-1) { vector4 = DirectionTo(Main.npc[num59].Center); if (vector4.Y<=0.5f && vector4.Y>=-0.5f) ai[2] = vector4.Y; }"
  },
  "bow_num57_aim_offset": "赋值: 仅两处 — type 22 块 :55057 num57=4; type 228 块 :55069 num57=6;其余 type 未赋值,保持 :54945 初始 int num57 = 0。计算/使用: :55175-55183 发射段 — vec2 = Vector2.Zero; if (num59!=-1) vec2 = DirectionTo(Main.npc[num59].Center + new Vector2(0f, -num57)); 即把目标中心向上抬 num57 像素后再取方向;若 NaN 或 Math.Sign(vec2.X)!=spriteDirection 则回退 new Vector2(spriteDirection, 0f);之后 vec2 *= num54。另外 :55193 flag28 段直接 DirectionTo(Main.npc[num59].Center),不做 num57 补偿",
  "state_exit": "近战态 :54927-54934 — if (ai[1]<=0f && 0==0) { ai[0] = ((localAI[2]==8f && flag16) ? 8 : 0); ai[1] = num47 + Main.rand.Next(maxValue); ai[2] = 0f; localAI[1] = (localAI[3] = num47/2 + Main.rand.Next(maxValue)); netUpdate = true; }。弓态 :55199-55206 同构 — { ai[0] = ((localAI[2]==8f && flag16) ? 8 : 0); ai[1] = num56 + Main.rand.Next(maxValue2); ai[2] = 0f; localAI[1] = (localAI[3] = num56/2 + Main.rand.Next(maxValue2)); netUpdate = true; }。即退出时若 localAI[2]==8 且 flag16(受惊标记)回到状态 8,否则回空闲 0;冷却 = 基础(num47/num56) + rand(maxValue/maxValue2),localAI[1]/localAI[3] 同步设为 基础/2 + rand"
}
```
````
