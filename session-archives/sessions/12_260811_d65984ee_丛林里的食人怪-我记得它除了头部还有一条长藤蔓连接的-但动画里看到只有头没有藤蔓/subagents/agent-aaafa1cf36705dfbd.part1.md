# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-11T07:14:10.679Z

```
在 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs 中（1.4.5.6 反编译源码），系统性枚举 DrawNPCs/DrawNPC 里所有"NPC 附属部件程序化叠画"的特例分支。搜索范围约 Main.cs:22300-26200（已知锚点：22370 aiStyle==25、22433 aiStyle==13 藤蔓、22593 aiStyle==47、22633 aiStyle 33-36、22714 aiStyle==20、22798 史莱姆王忍者、22980 aiStyle==10、24746 aiStyle==7、25546 aiStyle==87、25791 aiStyle==7 等），但也要在这个范围前后扫一遍别漏。

对每个分支输出一行记录：
- Main.cs 行号范围
- 触发条件（npc.type 具体值 / aiStyle 值 / 其他门禁如 ai[0]==0）
- 画的是什么（TextureAssets 具体贴图名、几段、什么几何：链段步进/IK/跟随/缩放等）
- 附带语义（是否有 localAI/ai 参数驱动、特殊旋转）

只统计"在 NPC 本体贴图之外额外画的东西"（链/藤蔓/手臂/披风/忍者/王冠/光环/拖尾等）。不要统计纯颜色/alpha/帧选择逻辑。最后给一个完整的 markdown 表。不要改任何文件。
```

---

## 📎 Attachment · skill_listing · 2026-08-11T07:14:10.682Z

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

## 🤖 Assistant · 2026-08-11T07:14:12.688Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The user wants a systematic enumeration of special-case branches in DrawNPCs/DrawNPC in a decompiled Terraria 1.4.5.6 Main.cs. I need to scan roughly lines 22300-26200 plus surrounding areas. Let me start by checking the file and finding DrawNPC/DrawNPCs method boundaries.

Let me grep for the method definitions and key anchors first.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:14:14.443Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"private void DrawNPC\\|public void DrawNPC\\|void DrawNPCs\\|DrawNPC(bool\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head -40",
 "description": "Find DrawNPC/DrawNPCs method definitions"
}
```


---

## 🤖 Assistant · 2026-08-11T07:14:14.472Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "description": "Count lines in Main.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:14.479Z

**📎 ToolResult**

```
22159:	internal void DrawNPCs(bool behindTiles = false)
22318:	public void DrawNPCDirect_QueenSlimeWings(NPC rCurrentNPC, SpriteBatch mySpriteBatch, Vector2 screenPos, Vector2 drawCenter, Microsoft.Xna.Framework.Color originColor)
22350:	public void DrawNPCDirect(SpriteBatch mySpriteBatch, NPC rCurrentNPC, bool behindTiles, Vector2 screenPos)
41438:	private void DrawNPCHousesInUI(int inventoryTop)

```


---

## 👤 User(sidechain) · 2026-08-11T07:14:14.492Z

**📎 ToolResult**

```
   66229 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs

```


---

## 🤖 Assistant · 2026-08-11T07:14:15.896Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
DrawNPCs starts at 22159, DrawNPCDirect at 22350. Let me find the end of DrawNPCDirect. DrawNPC is probably a large method. Let me look at the region 22159 to ~26500.

Let me read the whole region in chunks. That's about 4000+ lines. Let me read them efficiently.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:14:16.163Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "offset": 22159,
 "limit": 240
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:16.170Z

**📎 ToolResult**

```
22159		internal void DrawNPCs(bool behindTiles = false)
22160		{
22161			if (!behindTiles)
22162			{
22163				LeashedEntity.DrawEntities();
22164			}
22165			TimeLogger.StartTimestamp fromTimestamp = TimeLogger.Start();
22166			bool flag = false;
22167			Microsoft.Xna.Framework.Rectangle rectangle = new Microsoft.Xna.Framework.Rectangle((int)screenPosition.X - 800, (int)screenPosition.Y - 800, screenWidth + 1600, screenHeight + 1600);
22168			for (int num = maxNPCs - 1; num >= 0; num--)
22169			{
22170				try
22171				{
22172					if (npc[num].active && npc[num].type > 0 && npc[num].type < NPCID.Count && !npc[num].hide)
22173					{
22174						npc[num].position += npc[num].netOffset;
22175						if (npc[num].behindTiles == behindTiles)
22176						{
22177							if (npc[num].type == 125 || npc[num].type == 126)
22178							{
22179								if (!NPC.IsMechQueenUp && !flag)
22180								{
22181									flag = true;
22182									for (int i = 0; i < maxNPCs; i++)
22183									{
22184										if (!npc[i].active || num == i || (npc[i].type != 125 && npc[i].type != 126))
22185										{
22186											continue;
22187										}
22188										float scale = npc[i].scale;
22189										float x = npc[i].Center.X;
22190										float num2 = npc[i].Bottom.Y - (float)npc[i].height * 0.5f * scale;
22191										float x2 = npc[num].Center.X;
22192										float y = npc[num].Bottom.Y - (float)npc[num].height * 0.5f * scale;
22193										Vector2 vector = new Vector2(x2, y);
22194										float num3 = x - vector.X;
22195										float num4 = num2 - vector.Y;
22196										float rotation = (float)Math.Atan2(num4, num3) - 1.57f;
22197										bool flag2 = true;
22198										float num5 = (float)Math.Sqrt(num3 * num3 + num4 * num4);
22199										if (num5 > 2000f)
22200										{
22201											flag2 = false;
22202										}
22203										float num6 = 40f * scale;
22204										while (flag2)
22205										{
22206											num5 = (float)Math.Sqrt(num3 * num3 + num4 * num4);
22207											if (num5 < num6)
22208											{
22209												flag2 = false;
22210												continue;
22211											}
22212											num5 = (float)TextureAssets.Chain12.Height() * scale / num5;
22213											num3 *= num5;
22214											num4 *= num5;
22215											vector.X += num3;
22216											vector.Y += num4;
22217											num3 = x - vector.X;
22218											num4 = num2 - vector.Y;
22219											Microsoft.Xna.Framework.Color color = Lighting.GetColor((int)vector.X / 16, (int)(vector.Y / 16f));
22220											spriteBatch.Draw(TextureAssets.Chain12.Value, new Vector2(vector.X - screenPosition.X, vector.Y - screenPosition.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Chain12.Width(), TextureAssets.Chain12.Height()), color, rotation, new Vector2((float)TextureAssets.Chain12.Width() * 0.5f, (float)TextureAssets.Chain12.Height() * 0.5f), scale, SpriteEffects.None, 0f);
22221										}
22222									}
22223								}
22224							}
22225							else if (npc[num].type == 263 && npc[num].aiStyle == 52 && NPC.plantBoss >= 0)
22226							{
22227								Vector2 vector2 = new Vector2(npc[num].position.X + (float)(npc[num].width / 2), npc[num].position.Y + (float)(npc[num].height / 2));
22228								float num7 = npc[NPC.plantBoss].Center.X - vector2.X;
22229								float num8 = npc[NPC.plantBoss].Center.Y - vector2.Y;
22230								float rotation2 = (float)Math.Atan2(num8, num7) - 1.57f;
22231								bool flag3 = true;
22232								while (flag3)
22233								{
22234									int num9 = 16;
22235									int num10 = 32;
22236									float num11 = (float)Math.Sqrt(num7 * num7 + num8 * num8);
22237									if (num11 < (float)num10)
22238									{
22239										num9 = (int)num11 - num10 + num9;
22240										flag3 = false;
22241									}
22242									num11 = (float)num9 / num11;
22243									num7 *= num11;
22244									num8 *= num11;
22245									vector2.X += num7;
22246									vector2.Y += num8;
22247									num7 = npc[NPC.plantBoss].Center.X - vector2.X + npc[NPC.plantBoss].netOffset.X;
22248									num8 = npc[NPC.plantBoss].Center.Y - vector2.Y + npc[NPC.plantBoss].netOffset.Y;
22249									Microsoft.Xna.Framework.Color color2 = Lighting.GetColor((int)vector2.X / 16, (int)(vector2.Y / 16f));
22250									spriteBatch.Draw(TextureAssets.Chain26.Value, new Vector2(vector2.X - screenPosition.X, vector2.Y - screenPosition.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Chain26.Width(), num9), color2, rotation2, new Vector2((float)TextureAssets.Chain26.Width() * 0.5f, (float)TextureAssets.Chain26.Height() * 0.5f), 1f, SpriteEffects.None, 0f);
22251								}
22252							}
22253							else if (npc[num].type == 264 && npc[num].aiStyle == 53 && NPC.plantBoss >= 0)
22254							{
22255								int num12 = NPC.plantBoss;
22256								if (npc[num].ai[3] > 0f)
22257								{
22258									num12 = (int)npc[num].ai[3] - 1;
22259								}
22260								Vector2 vector3 = new Vector2(npc[num].position.X + (float)(npc[num].width / 2), npc[num].position.Y + (float)(npc[num].height / 2));
22261								float num13 = npc[num12].Center.X - vector3.X;
22262								float num14 = npc[num12].Center.Y - vector3.Y;
22263								float rotation3 = (float)Math.Atan2(num14, num13) - 1.57f;
22264								bool flag4 = true;
22265								while (flag4)
22266								{
22267									int num15 = 16;
22268									int num16 = 32;
22269									float num17 = (float)Math.Sqrt(num13 * num13 + num14 * num14);
22270									if (num17 < (float)num16)
22271									{
22272										num15 = (int)num17 - num16 + num15;
22273										flag4 = false;
22274									}
22275									num17 = (float)num15 / num17;
22276									num13 *= num17;
22277									num14 *= num17;
22278									vector3.X += num13;
22279									vector3.Y += num14;
22280									num13 = npc[num12].Center.X - vector3.X + npc[num12].netOffset.X;
22281									num14 = npc[num12].Center.Y - vector3.Y + npc[num12].netOffset.Y;
22282									Microsoft.Xna.Framework.Color color3 = Lighting.GetColor((int)vector3.X / 16, (int)(vector3.Y / 16f));
22283									spriteBatch.Draw(TextureAssets.Chain27.Value, new Vector2(vector3.X - screenPosition.X, vector3.Y - screenPosition.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Chain27.Width(), num15), color3, rotation3, new Vector2((float)TextureAssets.Chain27.Width() * 0.5f, (float)TextureAssets.Chain27.Height() * 0.5f), 1f, SpriteEffects.None, 0f);
22284								}
22285							}
22286							if (NPCID.Sets.MustAlwaysDraw[npc[num].type] || rectangle.Intersects(new Microsoft.Xna.Framework.Rectangle((int)npc[num].position.X, (int)npc[num].position.Y, npc[num].width, npc[num].height)))
22287							{
22288								DrawNPCCheckAlt(npc[num]);
22289								DrawNPC(num, behindTiles);
22290							}
22291						}
22292						npc[num].position -= npc[num].netOffset;
22293					}
22294				}
22295				catch
22296				{
22297					npc[num].active = false;
22298				}
22299			}
22300			TimeLogger.NPCs.AddTime(fromTimestamp);
22301		}
22302	
22303		protected void DrawNPCCheckAlt(NPC n)
22304		{
22305			if (TownNPCProfiles.Instance.GetProfile(n.type, out var profile))
22306			{
22307				TextureAssets.Npc[n.type] = profile.GetTextureNPCShouldUse(n);
22308			}
22309		}
22310	
22311		protected void DrawNPC(int iNPCIndex, bool behindTiles)
22312		{
22313			NPC rCurrentNPC = npc[iNPCIndex];
22314			Vector2 screenPos = screenPosition;
22315			DrawNPCDirect(spriteBatch, rCurrentNPC, behindTiles, screenPos);
22316		}
22317	
22318		public void DrawNPCDirect_QueenSlimeWings(NPC rCurrentNPC, SpriteBatch mySpriteBatch, Vector2 screenPos, Vector2 drawCenter, Microsoft.Xna.Framework.Color originColor)
22319		{
22320			Texture2D value = TextureAssets.Extra[185].Value;
22321			Microsoft.Xna.Framework.Rectangle rectangle = value.Frame(1, 4, 0, (int)rCurrentNPC.localAI[3] / 6);
22322			float scale = 0.8f;
22323			for (int i = 0; i < 2; i++)
22324			{
22325				float x = 1f;
22326				float num = 0f;
22327				SpriteEffects effects = SpriteEffects.None;
22328				if (i == 1)
22329				{
22330					x = 0f;
22331					num = 0f - num + 2f;
22332					effects = SpriteEffects.FlipHorizontally;
22333				}
22334				Vector2 origin = rectangle.Size() * new Vector2(x, 0.5f);
22335				Vector2 vector = new Vector2(drawCenter.X + num, drawCenter.Y);
22336				if (rCurrentNPC.rotation != 0f)
22337				{
22338					vector = vector.RotatedBy(rCurrentNPC.rotation, rCurrentNPC.Bottom);
22339				}
22340				vector -= screenPos;
22341				float num2 = MathHelper.Clamp(rCurrentNPC.velocity.Y, -6f, 6f) * -0.1f;
22342				if (i == 0)
22343				{
22344					num2 *= -1f;
22345				}
22346				mySpriteBatch.Draw(value, vector, rectangle, originColor, rCurrentNPC.rotation + num2, origin, scale, effects, 0f);
22347			}
22348		}
22349	
22350		public void DrawNPCDirect(SpriteBatch mySpriteBatch, NPC rCurrentNPC, bool behindTiles, Vector2 screenPos)
22351		{
22352			int type = rCurrentNPC.type;
22353			rCurrentNPC.SetFrameSize();
22354			if (rCurrentNPC.realLife == -1 && rCurrentNPC.life >= rCurrentNPC.lifeMax && !rCurrentNPC.boss)
22355			{
22356				bool flag = Lighting.GetColor((int)((double)rCurrentNPC.position.X + (double)rCurrentNPC.width * 0.5) / 16, (int)(((double)rCurrentNPC.position.Y + (double)rCurrentNPC.height * 0.5) / 16.0)).ToVector3().Length() > 0.4325f;
22357				bool flag2 = false;
22358				if (LockOnHelper.AimedTarget == rCurrentNPC)
22359				{
22360					flag2 = true;
22361				}
22362				else if (rCurrentNPC.Distance(Main.player[myPlayer].Center) < 350f && flag)
22363				{
22364					flag2 = true;
22365				}
22366				if (flag2 && rCurrentNPC.lifeMax < 5)
22367				{
22368					flag2 = false;
22369				}
22370				if (flag2 && rCurrentNPC.aiStyle == 25 && rCurrentNPC.ai[0] == 0f)
22371				{
22372					flag2 = false;
22373				}
22374				if (flag2)
22375				{
22376					rCurrentNPC.nameOver = MathHelper.Clamp(rCurrentNPC.nameOver + 0.025f, 0f, 1f);
22377				}
22378				else
22379				{
22380					rCurrentNPC.nameOver = MathHelper.Clamp(rCurrentNPC.nameOver - 0.025f, 0f, 1f);
22381				}
22382			}
22383			else
22384			{
22385				rCurrentNPC.nameOver = MathHelper.Clamp(rCurrentNPC.nameOver - 0.025f, 0f, 1f);
22386			}
22387			if (type == 1 && rCurrentNPC.ai[0] == -999f)
22388			{
22389				return;
22390			}
22391			if (type == 101)
22392			{
22393				bool flag3 = true;
22394				Vector2 vector = new Vector2(rCurrentNPC.position.X + (float)(rCurrentNPC.width / 2), rCurrentNPC.position.Y + (float)(rCurrentNPC.height / 2));
22395				float num = rCurrentNPC.ai[0] * 16f + 8f - vector.X;
22396				float num2 = rCurrentNPC.ai[1] * 16f + 8f - vector.Y;
22397				float rotation = (float)Math.Atan2(num2, num) - 1.57f;
22398				bool flag4 = true;

```


---

## 🤖 Assistant · 2026-08-11T07:14:17.795Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I need to read DrawNPCDirect from 22350 onwards. It's a huge method. Let me read in chunks of 2000 lines. Let me read 22390-24400, then 24400-26400, and also scan after 26400 for the method end.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:14:18.058Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "limit": 810,
 "offset": 22398
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:18.184Z

**📎 ToolResult**

```
22398				bool flag4 = true;
22399				while (flag4)
22400				{
22401					float num3 = 0.75f;
22402					int height = 28;
22403					float num4 = (float)Math.Sqrt(num * num + num2 * num2);
22404					if (num4 < 28f * num3)
22405					{
22406						height = (int)num4 - 40 + 28;
22407						flag4 = false;
22408					}
22409					num4 = 20f * num3 / num4;
22410					num *= num4;
22411					num2 *= num4;
22412					vector.X += num;
22413					vector.Y += num2;
22414					num = rCurrentNPC.ai[0] * 16f + 8f - vector.X;
22415					num2 = rCurrentNPC.ai[1] * 16f + 8f - vector.Y;
22416					Microsoft.Xna.Framework.Color color = Lighting.GetColor((int)vector.X / 16, (int)(vector.Y / 16f));
22417					if (rCurrentNPC.IsABestiaryIconDummy)
22418					{
22419						color = rCurrentNPC.GetBestiaryEntryColor();
22420					}
22421					if (!flag3)
22422					{
22423						flag3 = true;
22424						mySpriteBatch.Draw(TextureAssets.Chain10.Value, new Vector2(vector.X - screenPos.X, vector.Y - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Chain10.Width(), height), color, rotation, new Vector2((float)TextureAssets.Chain10.Width() * 0.5f, (float)TextureAssets.Chain10.Height() * 0.5f), num3, SpriteEffects.None, 0f);
22425					}
22426					else
22427					{
22428						flag3 = false;
22429						mySpriteBatch.Draw(TextureAssets.Chain11.Value, new Vector2(vector.X - screenPos.X, vector.Y - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Chain10.Width(), height), color, rotation, new Vector2((float)TextureAssets.Chain10.Width() * 0.5f, (float)TextureAssets.Chain10.Height() * 0.5f), num3, SpriteEffects.None, 0f);
22430					}
22431				}
22432			}
22433			else if (rCurrentNPC.aiStyle == 13)
22434			{
22435				Vector2 vector2 = new Vector2(rCurrentNPC.position.X + (float)(rCurrentNPC.width / 2), rCurrentNPC.position.Y + (float)(rCurrentNPC.height / 2));
22436				float num5 = rCurrentNPC.ai[0] * 16f + 8f - vector2.X;
22437				float num6 = rCurrentNPC.ai[1] * 16f + 8f - vector2.Y;
22438				float rotation2 = (float)Math.Atan2(num6, num5) - 1.57f;
22439				bool flag5 = true;
22440				while (flag5)
22441				{
22442					int num7 = 28;
22443					int num8 = 40;
22444					if (type == 259 || type == 260)
22445					{
22446						num8 = 20;
22447						num7 = 12;
22448					}
22449					float num9 = (float)Math.Sqrt(num5 * num5 + num6 * num6);
22450					if (num9 < (float)num8)
22451					{
22452						num7 = (int)num9 - num8 + num7;
22453						flag5 = false;
22454					}
22455					num9 = (float)num7 / num9;
22456					num5 *= num9;
22457					num6 *= num9;
22458					vector2.X += num5;
22459					vector2.Y += num6;
22460					num5 = rCurrentNPC.ai[0] * 16f + 8f - vector2.X;
22461					num6 = rCurrentNPC.ai[1] * 16f + 8f - vector2.Y;
22462					Microsoft.Xna.Framework.Color color2 = Lighting.GetColor((int)vector2.X / 16, (int)(vector2.Y / 16f));
22463					if (rCurrentNPC.IsABestiaryIconDummy)
22464					{
22465						color2 = rCurrentNPC.GetBestiaryEntryColor();
22466					}
22467					if (type == 259 || type == 260)
22468					{
22469						color2.B = byte.MaxValue;
22470						if (color2.R < 100)
22471						{
22472							color2.R = 100;
22473						}
22474						if (color2.G < 150)
22475						{
22476							color2.G = 150;
22477						}
22478					}
22479					switch (type)
22480					{
22481					case 56:
22482						mySpriteBatch.Draw(TextureAssets.Chain5.Value, new Vector2(vector2.X - screenPos.X, vector2.Y - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Chain4.Width(), num7), color2, rotation2, new Vector2((float)TextureAssets.Chain4.Width() * 0.5f, (float)TextureAssets.Chain4.Height() * 0.5f), 1f, SpriteEffects.None, 0f);
22483						break;
22484					case 175:
22485						mySpriteBatch.Draw(TextureAssets.Chain14.Value, new Vector2(vector2.X - screenPos.X, vector2.Y - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Chain14.Width(), num7), color2, rotation2, new Vector2((float)TextureAssets.Chain14.Width() * 0.5f, (float)TextureAssets.Chain14.Height() * 0.5f), 1f, SpriteEffects.None, 0f);
22486						break;
22487					case 259:
22488						mySpriteBatch.Draw(TextureAssets.Chain24.Value, new Vector2(vector2.X - screenPos.X, vector2.Y - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Chain24.Width(), num7), color2, rotation2, new Vector2((float)TextureAssets.Chain24.Width() * 0.5f, (float)TextureAssets.Chain24.Height() * 0.5f), 1f, SpriteEffects.None, 0f);
22489						break;
22490					case 260:
22491						mySpriteBatch.Draw(TextureAssets.Chain25.Value, new Vector2(vector2.X - screenPos.X, vector2.Y - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Chain25.Width(), num7), color2, rotation2, new Vector2((float)TextureAssets.Chain25.Width() * 0.5f, (float)TextureAssets.Chain25.Height() * 0.5f), 1f, SpriteEffects.None, 0f);
22492						break;
22493					default:
22494						mySpriteBatch.Draw(TextureAssets.Chain4.Value, new Vector2(vector2.X - screenPos.X, vector2.Y - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Chain4.Width(), num7), color2, rotation2, new Vector2((float)TextureAssets.Chain4.Width() * 0.5f, (float)TextureAssets.Chain4.Height() * 0.5f), 1f, SpriteEffects.None, 0f);
22495						break;
22496					}
22497				}
22498			}
22499			if (type == 327)
22500			{
22501				float rotation3 = 0f;
22502				Vector2 vector3 = new Vector2(rCurrentNPC.Center.X, rCurrentNPC.Center.Y + 80f);
22503				int num10 = (int)rCurrentNPC.localAI[1];
22504				Microsoft.Xna.Framework.Color color3 = ((!rCurrentNPC.IsABestiaryIconDummy) ? Lighting.GetColor((int)vector3.X / 16, (int)(vector3.Y / 16f)) : rCurrentNPC.GetBestiaryEntryColor());
22505				mySpriteBatch.Draw(TextureAssets.PumpkingCloak.Value, new Vector2(vector3.X - screenPos.X, vector3.Y - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, TextureAssets.PumpkingCloak.Height() / 5 * num10, TextureAssets.PumpkingCloak.Width(), TextureAssets.PumpkingCloak.Height() / 5), color3, rotation3, new Vector2((float)TextureAssets.PumpkingCloak.Width() * 0.5f, (float)TextureAssets.PumpkingCloak.Height() * 0.5f / 5f), 1f, SpriteEffects.None, 0f);
22506			}
22507			if (type == 328)
22508			{
22509				Vector2 vector4 = new Vector2(rCurrentNPC.position.X + (float)rCurrentNPC.width * 0.5f - 5f * rCurrentNPC.ai[0], rCurrentNPC.position.Y + 20f);
22510				for (int i = 0; i < 2; i++)
22511				{
22512					float num11 = npc[(int)rCurrentNPC.ai[1]].position.X + (float)(npc[(int)rCurrentNPC.ai[1]].width / 2) - vector4.X;
22513					float num12 = npc[(int)rCurrentNPC.ai[1]].position.Y + (float)(npc[(int)rCurrentNPC.ai[1]].height / 2) - 30f - vector4.Y;
22514					float num13 = 0f;
22515					if (i == 0)
22516					{
22517						num11 -= 200f * rCurrentNPC.ai[0];
22518						num12 += 130f;
22519						num13 = (float)Math.Sqrt(num11 * num11 + num12 * num12);
22520						num13 = 92f / num13;
22521						vector4.X += num11 * num13;
22522						vector4.Y += num12 * num13;
22523					}
22524					else
22525					{
22526						num11 -= 50f * rCurrentNPC.ai[0];
22527						num12 += 80f;
22528						num13 = (float)Math.Sqrt(num11 * num11 + num12 * num12);
22529						num13 = 60f / num13;
22530						vector4.X += num11 * num13;
22531						vector4.Y += num12 * num13;
22532					}
22533					float rotation4 = (float)Math.Atan2(num12, num11) - 1.57f;
22534					Microsoft.Xna.Framework.Color color4 = Lighting.GetColor((int)vector4.X / 16, (int)(vector4.Y / 16f));
22535					mySpriteBatch.Draw(TextureAssets.PumpkingArm.Value, new Vector2(vector4.X - screenPos.X, vector4.Y - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.PumpkingArm.Width(), TextureAssets.PumpkingArm.Height()), color4, rotation4, new Vector2((float)TextureAssets.PumpkingArm.Width() * 0.5f, (float)TextureAssets.PumpkingArm.Height() * 0.5f), 1f, SpriteEffects.None, 0f);
22536					if (i == 0)
22537					{
22538						vector4.X += num11 * num13 / 2f;
22539						vector4.Y += num12 * num13 / 2f;
22540					}
22541				}
22542			}
22543			if (type == 36)
22544			{
22545				Vector2 vector5 = new Vector2(rCurrentNPC.position.X + (float)rCurrentNPC.width * 0.5f - 5f * rCurrentNPC.ai[0], rCurrentNPC.position.Y + 20f);
22546				for (int j = 0; j < 2; j++)
22547				{
22548					float num14 = npc[(int)rCurrentNPC.ai[1]].position.X + (float)(npc[(int)rCurrentNPC.ai[1]].width / 2) - vector5.X;
22549					float num15 = npc[(int)rCurrentNPC.ai[1]].position.Y + (float)(npc[(int)rCurrentNPC.ai[1]].height / 2) - vector5.Y;
22550					float num16 = 0f;
22551					if (j == 0)
22552					{
22553						num14 -= 200f * rCurrentNPC.ai[0];
22554						num15 += 130f;
22555						num16 = (float)Math.Sqrt(num14 * num14 + num15 * num15);
22556						num16 = 92f / num16;
22557						vector5.X += num14 * num16;
22558						vector5.Y += num15 * num16;
22559					}
22560					else
22561					{
22562						num14 -= 50f * rCurrentNPC.ai[0];
22563						num15 += 80f;
22564						num16 = (float)Math.Sqrt(num14 * num14 + num15 * num15);
22565						num16 = 60f / num16;
22566						vector5.X += num14 * num16;
22567						vector5.Y += num15 * num16;
22568					}
22569					float rotation5 = (float)Math.Atan2(num15, num14) - 1.57f;
22570					Microsoft.Xna.Framework.Color color5 = Lighting.GetColor((int)vector5.X / 16, (int)(vector5.Y / 16f));
22571					if (rCurrentNPC.localAI[3] == 1f)
22572					{
22573						mySpriteBatch.Draw(TextureAssets.BoneArm3.Value, new Vector2(vector5.X - screenPos.X, vector5.Y - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.BoneArm.Width(), TextureAssets.BoneArm.Height()), color5, rotation5, new Vector2((float)TextureAssets.BoneArm.Width() * 0.5f, (float)TextureAssets.BoneArm.Height() * 0.5f), 1f, SpriteEffects.None, 0f);
22574					}
22575					else
22576					{
22577						mySpriteBatch.Draw(TextureAssets.BoneArm.Value, new Vector2(vector5.X - screenPos.X, vector5.Y - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.BoneArm.Width(), TextureAssets.BoneArm.Height()), color5, rotation5, new Vector2((float)TextureAssets.BoneArm.Width() * 0.5f, (float)TextureAssets.BoneArm.Height() * 0.5f), 1f, SpriteEffects.None, 0f);
22578					}
22579					if (j == 0)
22580					{
22581						vector5.X += num14 * num16 / 2f;
22582						vector5.Y += num15 * num16 / 2f;
22583					}
22584					else if (FocusHelper.AllowMiscDustEffects)
22585					{
22586						vector5.X += num14 * num16 - 16f;
22587						vector5.Y += num15 * num16 - 6f;
22588						int num17 = Dust.NewDust(new Vector2(vector5.X, vector5.Y), 30, 10, 5, num14 * 0.02f, num15 * 0.02f, 0, default(Microsoft.Xna.Framework.Color), 2f);
22589						dust[num17].noGravity = true;
22590					}
22591				}
22592			}
22593			if (rCurrentNPC.aiStyle == 47)
22594			{
22595				float scale = rCurrentNPC.scale;
22596				Vector2 vector6 = new Vector2(rCurrentNPC.Center.X, rCurrentNPC.Center.Y);
22597				Vector2 center = rCurrentNPC.Center;
22598				if (NPC.golemBoss != -1)
22599				{
22600					center = npc[NPC.golemBoss].Center;
22601				}
22602				float num18 = center.X - vector6.X;
22603				float num19 = center.Y - vector6.Y;
22604				num19 -= 7f * scale;
22605				num18 = ((type != 247) ? (num18 + 66f * scale) : (num18 - 70f * scale));
22606				float rotation6 = (float)Math.Atan2(num19, num18) - 1.57f;
22607				bool flag6 = true;
22608				while (flag6)
22609				{
22610					float num20 = (float)Math.Sqrt(num18 * num18 + num19 * num19);
22611					if (num20 < 16f)
22612					{
22613						flag6 = false;
22614						continue;
22615					}
22616					num20 = 16f * scale / num20;
22617					num18 *= num20;
22618					num19 *= num20;
22619					vector6.X += num18;
22620					vector6.Y += num19;
22621					num18 = center.X - vector6.X;
22622					num19 = center.Y - vector6.Y;
22623					num19 -= 7f * scale;
22624					num18 = ((type != 247) ? (num18 + 66f * scale) : (num18 - 70f * scale));
22625					if (getGoodWorld)
22626					{
22627						num19 += 8f;
22628					}
22629					Microsoft.Xna.Framework.Color color6 = Lighting.GetColor((int)vector6.X / 16, (int)(vector6.Y / 16f));
22630					mySpriteBatch.Draw(TextureAssets.Chain21.Value, new Vector2(vector6.X - screenPos.X, vector6.Y - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Chain21.Width(), TextureAssets.Chain21.Height()), color6, rotation6, new Vector2((float)TextureAssets.Chain21.Width() * 0.5f, (float)TextureAssets.Chain21.Height() * 0.5f), scale, SpriteEffects.None, 0f);
22631				}
22632			}
22633			if (rCurrentNPC.aiStyle >= 33 && rCurrentNPC.aiStyle <= 36)
22634			{
22635				Vector2 vector7 = new Vector2(rCurrentNPC.position.X + (float)rCurrentNPC.width * 0.5f - 5f * rCurrentNPC.ai[0], rCurrentNPC.position.Y + 20f);
22636				for (int k = 0; k < 2; k++)
22637				{
22638					float num21 = npc[(int)rCurrentNPC.ai[1]].position.X + (float)(npc[(int)rCurrentNPC.ai[1]].width / 2) - vector7.X;
22639					float num22 = npc[(int)rCurrentNPC.ai[1]].position.Y + (float)(npc[(int)rCurrentNPC.ai[1]].height / 2) - vector7.Y;
22640					float num23 = 0f;
22641					if (k == 0)
22642					{
22643						num21 -= 200f * rCurrentNPC.ai[0];
22644						num22 += 130f;
22645						num23 = (float)Math.Sqrt(num21 * num21 + num22 * num22);
22646						num23 = 92f / num23;
22647						vector7.X += num21 * num23;
22648						vector7.Y += num22 * num23;
22649					}
22650					else
22651					{
22652						num21 -= 50f * rCurrentNPC.ai[0];
22653						num22 += 80f;
22654						num23 = (float)Math.Sqrt(num21 * num21 + num22 * num22);
22655						num23 = 60f / num23;
22656						vector7.X += num21 * num23;
22657						vector7.Y += num22 * num23;
22658					}
22659					float rotation7 = (float)Math.Atan2(num22, num21) - 1.57f;
22660					Microsoft.Xna.Framework.Color color7 = Lighting.GetColor((int)vector7.X / 16, (int)(vector7.Y / 16f));
22661					mySpriteBatch.Draw(TextureAssets.BoneArm2.Value, new Vector2(vector7.X - screenPos.X, vector7.Y - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.BoneArm.Width(), TextureAssets.BoneArm.Height()), color7, rotation7, new Vector2((float)TextureAssets.BoneArm.Width() * 0.5f, (float)TextureAssets.BoneArm.Height() * 0.5f), 1f, SpriteEffects.None, 0f);
22662					if (k == 0)
22663					{
22664						vector7.X += num21 * num23 / 2f;
22665						vector7.Y += num22 * num23 / 2f;
22666					}
22667					else if (FocusHelper.AllowMiscDustEffects)
22668					{
22669						vector7.X += num21 * num23 - 16f;
22670						vector7.Y += num22 * num23 - 6f;
22671						int num24 = Dust.NewDust(new Vector2(vector7.X, vector7.Y), 30, 10, 6, num21 * 0.02f, num22 * 0.02f, 0, default(Microsoft.Xna.Framework.Color), 2.5f);
22672						dust[num24].noGravity = true;
22673					}
22674				}
22675			}
22676			if (type == 693)
22677			{
22678				float num25 = rCurrentNPC.localAI[1];
22679				float num26 = num25 - 60f;
22680				float num27 = rCurrentNPC.localAI[0];
22681				Texture2D value = TextureAssets.Extra[289].Value;
22682				float num28 = 1f;
22683				float num29 = rCurrentNPC.localAI[3];
22684				float num30 = num27 * 0.016f * num29;
22685				float num31 = 1f;
22686				float num32 = rCurrentNPC.localAI[2] / 10f;
22687				if (num32 > 0f)
22688				{
22689					num28 += num32 * 0.2f;
22690					num31 -= num32 * 0.25f;
22691				}
22692				Microsoft.Xna.Framework.Color color8 = new Microsoft.Xna.Framework.Color(num31, num31, num31, num31 / 2f);
22693				if (num27 < 60f)
22694				{
22695					float num33 = Utils.Remap(num27, 0f, 60f, 0f, 1f);
22696					byte b = (color8.R = (byte)((num28 = num33 * num33) * 255f));
22697					color8.G = b;
22698					color8.B = b;
22699					color8.A = (byte)(b / 2);
22700				}
22701				else if (num27 > num26)
22702				{
22703					float num34 = Utils.Remap(num27, num26, num25, 0f, 1f);
22704					num34 *= num34;
22705					num30 += num34 * 1.7f * num29;
22706					num28 += num34;
22707					byte b3 = (color8.R = (byte)((1f - num34) * 255f));
22708					color8.G = b3;
22709					color8.B = b3;
22710					color8.A = (byte)(b3 / 2);
22711				}
22712				mySpriteBatch.Draw(value, rCurrentNPC.Top - screenPos, null, color8, num30, value.Size() * 0.5f, num28, SpriteEffects.None, 0f);
22713			}
22714			if (rCurrentNPC.aiStyle == 20)
22715			{
22716				Vector2 vector8 = new Vector2(rCurrentNPC.position.X + (float)(rCurrentNPC.width / 2), rCurrentNPC.position.Y + (float)(rCurrentNPC.height / 2));
22717				float num35 = rCurrentNPC.ai[1] - vector8.X;
22718				float num36 = rCurrentNPC.ai[2] - vector8.Y;
22719				float num37 = (rCurrentNPC.rotation = (float)Math.Atan2(num36, num35) - 1.57f);
22720				bool flag7 = true;
22721				while (flag7)
22722				{
22723					int height2 = 12;
22724					float num38 = (float)Math.Sqrt(num35 * num35 + num36 * num36);
22725					if (num38 < 20f)
22726					{
22727						height2 = (int)num38 - 20 + 12;
22728						flag7 = false;
22729					}
22730					num38 = 12f / num38;
22731					num35 *= num38;
22732					num36 *= num38;
22733					vector8.X += num35;
22734					vector8.Y += num36;
22735					num35 = rCurrentNPC.ai[1] - vector8.X;
22736					num36 = rCurrentNPC.ai[2] - vector8.Y;
22737					Microsoft.Xna.Framework.Color color9 = Lighting.GetColor((int)vector8.X / 16, (int)(vector8.Y / 16f));
22738					mySpriteBatch.Draw(TextureAssets.Chain.Value, new Vector2(vector8.X - screenPos.X, vector8.Y - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Chain.Width(), height2), color9, num37, new Vector2((float)TextureAssets.Chain.Width() * 0.5f, (float)TextureAssets.Chain.Height() * 0.5f), 1f, SpriteEffects.None, 0f);
22739				}
22740				mySpriteBatch.Draw(TextureAssets.SpikeBase.Value, new Vector2(rCurrentNPC.ai[1] - screenPos.X, rCurrentNPC.ai[2] - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.SpikeBase.Width(), TextureAssets.SpikeBase.Height()), Lighting.GetColor((int)rCurrentNPC.ai[1] / 16, (int)(rCurrentNPC.ai[2] / 16f)), num37 - 0.75f, new Vector2((float)TextureAssets.SpikeBase.Width() * 0.5f, (float)TextureAssets.SpikeBase.Height() * 0.5f), 1f, SpriteEffects.None, 0f);
22741			}
22742			Microsoft.Xna.Framework.Color npcColor = Lighting.GetColor((int)((double)rCurrentNPC.position.X + (double)rCurrentNPC.width * 0.5) / 16, (int)(((double)rCurrentNPC.position.Y + (double)rCurrentNPC.height * 0.5) / 16.0));
22743			if (rCurrentNPC.IsABestiaryIconDummy)
22744			{
22745				npcColor = rCurrentNPC.GetBestiaryEntryColor();
22746			}
22747			if (type >= 277 && type <= 280)
22748			{
22749				if (npcColor.R < byte.MaxValue)
22750				{
22751					npcColor.R = byte.MaxValue;
22752				}
22753				if (npcColor.G < 175)
22754				{
22755					npcColor.G = 175;
22756				}
22757			}
22758			if (type == -4)
22759			{
22760				int r = npcColor.R;
22761				int g = npcColor.G;
22762				int b5 = npcColor.B;
22763				r *= 2;
22764				if (r > 255)
22765				{
22766					r = 255;
22767				}
22768				g *= 2;
22769				if (g > 255)
22770				{
22771					g = 255;
22772				}
22773				b5 *= 2;
22774				if (b5 > 255)
22775				{
22776					b5 = 255;
22777				}
22778				npcColor = new Microsoft.Xna.Framework.Color(r, g, b5);
22779			}
22780			if (behindTiles && type != 113 && type != 114)
22781			{
22782				int num39 = (int)((rCurrentNPC.position.X - 8f) / 16f);
22783				int num40 = (int)((rCurrentNPC.position.X + (float)rCurrentNPC.width + 8f) / 16f);
22784				int num41 = (int)((rCurrentNPC.position.Y - 8f) / 16f);
22785				int num42 = (int)((rCurrentNPC.position.Y + (float)rCurrentNPC.height + 8f) / 16f);
22786				for (int l = num39; l <= num40; l++)
22787				{
22788					for (int m = num41; m <= num42; m++)
22789					{
22790						if (Lighting.Brightness(l, m) == 0f)
22791						{
22792							npcColor = Microsoft.Xna.Framework.Color.Black;
22793						}
22794					}
22795				}
22796			}
22797			npcColor = rCurrentNPC.GetNPCColorTintedByBuffs(npcColor);
22798			if (type == 50)
22799			{
22800				Vector2 zero = Vector2.Zero;
22801				float num43 = 0f;
22802				zero.Y -= rCurrentNPC.velocity.Y;
22803				zero.X -= rCurrentNPC.velocity.X * 2f;
22804				num43 += rCurrentNPC.velocity.X * 0.05f;
22805				if (rCurrentNPC.frame.Y == 120)
22806				{
22807					zero.Y += 2f;
22808				}
22809				if (rCurrentNPC.frame.Y == 360)
22810				{
22811					zero.Y -= 2f;
22812				}
22813				if (rCurrentNPC.frame.Y == 480)
22814				{
22815					zero.Y -= 6f;
22816				}
22817				mySpriteBatch.Draw(TextureAssets.Ninja.Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) + zero.X, rCurrentNPC.position.Y - screenPos.Y + (float)(rCurrentNPC.height / 2) + zero.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Ninja.Width(), TextureAssets.Ninja.Height()), npcColor, num43, new Vector2(TextureAssets.Ninja.Width() / 2, TextureAssets.Ninja.Height() / 2), 1f, SpriteEffects.None, 0f);
22818			}
22819			if (type == 71)
22820			{
22821				Vector2 zero2 = Vector2.Zero;
22822				float num44 = 0f;
22823				zero2.Y -= rCurrentNPC.velocity.Y * 0.3f;
22824				zero2.X -= rCurrentNPC.velocity.X * 0.6f;
22825				num44 += rCurrentNPC.velocity.X * 0.09f;
22826				if (rCurrentNPC.frame.Y == 120)
22827				{
22828					zero2.Y += 2f;
22829				}
22830				if (rCurrentNPC.frame.Y == 360)
22831				{
22832					zero2.Y -= 2f;
22833				}
22834				if (rCurrentNPC.frame.Y == 480)
22835				{
22836					zero2.Y -= 6f;
22837				}
22838				GetItemDrawFrame(327, out var itemTexture, out var rectangle);
22839				mySpriteBatch.Draw(itemTexture, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) + zero2.X, rCurrentNPC.position.Y - screenPos.Y + (float)(rCurrentNPC.height / 2) + zero2.Y), rectangle, npcColor, num44, rectangle.Size() / 2f, 1f, SpriteEffects.None, 0f);
22840			}
22841			if (type == 69)
22842			{
22843				mySpriteBatch.Draw(TextureAssets.AntLion.Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2), rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height + 14f), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.AntLion.Width(), TextureAssets.AntLion.Height()), npcColor, (0f - rCurrentNPC.rotation) * 0.3f, new Vector2(TextureAssets.AntLion.Width() / 2, TextureAssets.AntLion.Height() / 2), 1f, SpriteEffects.None, 0f);
22844			}
22845			if (NPCID.Sets.SlimeCanContainItems[type] && rCurrentNPC.ai[1] > 0f)
22846			{
22847				DrawNPC_SlimeItem(rCurrentNPC, type, npcColor, 0f);
22848			}
22849			float num45 = 0f;
22850			float num46 = 0f;
22851			float num47 = NPCAddHeight(rCurrentNPC);
22852			Vector2 halfSize = new Vector2(TextureAssets.Npc[type].Width() / 2, TextureAssets.Npc[type].Height() / npcFrameCount[type] / 2);
22853			if (type == 108 || type == 124 || type == 625)
22854			{
22855				num46 = 2f;
22856			}
22857			else if (type == 357)
22858			{
22859				num46 = rCurrentNPC.localAI[0];
22860			}
22861			else if (type == 467)
22862			{
22863				num46 = 7f;
22864			}
22865			else if (type == 537)
22866			{
22867				num46 = 2f;
22868			}
22869			else if (type == 581)
22870			{
22871				num46 = -6f;
22872			}
22873			else if (type == 490)
22874			{
22875				num46 = 4f;
22876			}
22877			else if (type == 484)
22878			{
22879				num46 = 2f;
22880			}
22881			else if (type == 483)
22882			{
22883				num46 = 14f;
22884			}
22885			else if (type == 477)
22886			{
22887				num47 = 22f;
22888			}
22889			else if (type == 478)
22890			{
22891				num46 -= 2f;
22892			}
22893			else if (type == 606)
22894			{
22895				num46 -= 2f;
22896			}
22897			else if (type == 612 || type == 613)
22898			{
22899				num46 -= 2f;
22900			}
22901			else if (type == 469 && rCurrentNPC.ai[2] == 1f)
22902			{
22903				num46 = 14f;
22904			}
22905			else
22906			{
22907				switch (type)
22908				{
22909				case 4:
22910					halfSize = new Vector2(55f, 107f);
22911					break;
22912				case 125:
22913					halfSize = new Vector2(55f, 107f);
22914					break;
22915				case 126:
22916					halfSize = new Vector2(55f, 107f);
22917					break;
22918				case 626:
22919				case 627:
22920					if (rCurrentNPC.wet)
22921					{
22922						num46 = -2f;
22923						halfSize = rCurrentNPC.frame.Size() * new Vector2(0.5f, 0.5f) + new Vector2(0f, -4f);
22924					}
22925					else
22926					{
22927						num46 = 2f;
22928					}
22929					break;
22930				case 692:
22931					num46 = ((!rCurrentNPC.wet) ? 10f : 6f);
22932					break;
22933				case 63:
22934				case 64:
22935				case 103:
22936					halfSize.Y += 4f;
22937					break;
22938				case 69:
22939					halfSize.Y += 8f;
22940					break;
22941				case 262:
22942					halfSize.Y = 77f;
22943					num47 += 26f;
22944					break;
22945				case 264:
22946					halfSize.Y = 21f;
22947					num47 += 2f;
22948					break;
22949				case 266:
22950					num47 += 50f * rCurrentNPC.scale;
22951					break;
22952				case 268:
22953					num47 += 16f;
22954					break;
22955				case 288:
22956					num47 += 6f;
22957					break;
22958				case 694:
22959					num45 += (float)rCurrentNPC.direction;
22960					num46 -= 2f;
22961					if (rCurrentNPC.ai[3] == 3f)
22962					{
22963						num45 += 4f;
22964						num46 += 16f;
22965					}
22966					else if (rCurrentNPC.ai[3] == 4f)
22967					{
22968						float num48 = (float)rCurrentNPC.frame.Y / 40f;
22969						float num49 = 17f;
22970						float num50 = 1f - Math.Max(0f, Math.Min(1f, num48 / num49));
22971						num45 += (float)(int)(4f * num50);
22972						num46 += (float)(int)(16f * num50);
22973					}
22974					break;
22975				case 688:
22976					num46 += 10f;
22977					break;
22978				}
22979			}
22980			if ((rCurrentNPC.aiStyle == 10 && type != 694) || type == 72)
22981			{
22982				npcColor = Microsoft.Xna.Framework.Color.White;
22983			}
22984			SpriteEffects spriteEffects = SpriteEffects.None;
22985			if (rCurrentNPC.spriteDirection == 1)
22986			{
22987				spriteEffects = SpriteEffects.FlipHorizontally;
22988			}
22989			if (type == 124 && rCurrentNPC.localAI[0] == 0f)
22990			{
22991				int num51 = 0;
22992				if (rCurrentNPC.frame.Y > 56)
22993				{
22994					num51 += 4;
22995				}
22996				num51 += rCurrentNPC.frame.Y / 56;
22997				if (num51 >= OffsetsPlayerHeadgear.Length)
22998				{
22999					num51 = 0;
23000				}
23001				float y = OffsetsPlayerHeadgear[num51].Y;
23002				LoadProjectile(582);
23003				Texture2D value2 = TextureAssets.Projectile[582].Value;
23004				if (rCurrentNPC.townNpcVariationIndex == 1)
23005				{
23006					value2 = TextureAssets.Extra[263].Value;
23007				}
23008				Vector2 position = rCurrentNPC.Bottom - screenPos;
23009				Vector2 zero3 = Vector2.Zero;
23010				zero3 += new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY + y);
23011				zero3 -= new Vector2(0f, rCurrentNPC.height / 2);
23012				zero3 -= new Vector2(value2.Width / 2, 0f);
23013				zero3 += new Vector2(-rCurrentNPC.spriteDirection * 2, -2f);
23014				zero3 += new Vector2(-1 * rCurrentNPC.spriteDirection, 1f);
23015				zero3 *= rCurrentNPC.scale;
23016				if (rCurrentNPC.scale == 2f)
23017				{
23018					zero3.Y += -6f;
23019				}
23020				if (rCurrentNPC.scale == 3f)
23021				{
23022					zero3.Y += -12f;
23023				}
23024				position += zero3;
23025				mySpriteBatch.Draw(value2, position, null, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, value2.Size() * new Vector2(0f, 0.5f), rCurrentNPC.scale, spriteEffects, 0f);
23026			}
23027			switch (type)
23028			{
23029			default:
23030				if (type != 546 && type != 552 && type != 553 && type != 554 && type != 561 && type != 562 && type != 563 && type != 555 && type != 556 && type != 557 && type != 558 && type != 559 && type != 560 && type != 574 && type != 575 && type != 568 && type != 569 && type != 572 && type != 573 && type != 566 && type != 567 && type != 570 && type != 578 && type != 571 && type != 583 && type != 584 && type != 585 && type != 618 && type != 620 && type != 661)
23031				{
23032					switch (type)
23033					{
23034					case 551:
23035					{
23036						Texture2D value3 = TextureAssets.Npc[type].Value;
23037						Vector2 vector9 = rCurrentNPC.Center - screenPos;
23038						Microsoft.Xna.Framework.Rectangle frame = rCurrentNPC.frame;
23039						_ = frame.Size() / 2f;
23040						SpriteEffects spriteEffects2 = spriteEffects ^ SpriteEffects.FlipHorizontally;
23041						float rotation8 = rCurrentNPC.rotation;
23042						Microsoft.Xna.Framework.Color color10 = npcColor;
23043						Microsoft.Xna.Framework.Color color11 = Microsoft.Xna.Framework.Color.Lerp(color10, Microsoft.Xna.Framework.Color.White, 0.6f);
23044						color11.A = 66;
23045						Vector2 vector10 = new Vector2(171f, 44f);
23046						Vector2 vector11 = new Vector2(230f, 52f);
23047						Vector2 vector12 = Vector2.Lerp(vector10, vector11, 0.5f) + new Vector2(-50f, 30f);
23048						int num52 = (int)rCurrentNPC.localAI[0] / 4;
23049						Vector2 spinningpoint = vector10 - vector12;
23050						Vector2 spinningpoint2 = vector11 - vector12;
23051						Texture2D value4 = TextureAssets.Extra[82].Value;
23052						if ((spriteEffects2 & SpriteEffects.FlipHorizontally) != SpriteEffects.None)
23053						{
23054							spinningpoint2.X *= -1f;
23055						}
23056						Microsoft.Xna.Framework.Rectangle value5 = value4.Frame(2, 5, num52 / 5, num52 % 5);
23057						Vector2 origin = new Vector2(16f, 176f);
23058						if ((spriteEffects2 & SpriteEffects.FlipHorizontally) != SpriteEffects.None)
23059						{
23060							origin.X = (float)value5.Width - origin.X;
23061						}
23062						if ((spriteEffects2 & SpriteEffects.FlipHorizontally) != SpriteEffects.None)
23063						{
23064							vector12.X = (float)frame.Width - vector12.X;
23065						}
23066						Texture2D value6 = TextureAssets.Extra[81].Value;
23067						if ((spriteEffects2 & SpriteEffects.FlipHorizontally) != SpriteEffects.None)
23068						{
23069							spinningpoint.X *= -1f;
23070						}
23071						Microsoft.Xna.Framework.Rectangle value7 = value6.Frame(2, 5, num52 / 5, num52 % 5);
23072						Vector2 origin2 = new Vector2(215f, 170f);
23073						if ((spriteEffects2 & SpriteEffects.FlipHorizontally) != SpriteEffects.None)
23074						{
23075							origin2.X = (float)value7.Width - origin2.X;
23076						}
23077						float lerpValue = Utils.GetLerpValue(0f, 30f, rCurrentNPC.localAI[1], clamped: true);
23078						if (lerpValue == 1f)
23079						{
23080							lerpValue = Utils.GetLerpValue(60f, 30f, rCurrentNPC.localAI[1], clamped: true);
23081						}
23082						lerpValue = 2f;
23083						Vector2 vector13 = rCurrentNPC.Size / 2f - screenPos;
23084						int num53 = -3;
23085						int num54 = 0;
23086						byte b6 = 2;
23087						for (int n = 9; n > num54; n += num53)
23088						{
23089							Vector2 vector14 = rCurrentNPC.oldPos[n] + vector13;
23090							float num55 = rCurrentNPC.oldRot[n];
23091							Microsoft.Xna.Framework.Color color12 = color10 * (1f - (float)n / 10f) * 0.35f;
23092							color12.A /= b6;
23093							mySpriteBatch.Draw(value4, vector14 + spinningpoint2.RotatedBy(num55), value5, color12, num55, origin, 1f, spriteEffects2, 0f);
23094							mySpriteBatch.Draw(value3, vector14, frame, color12, num55, vector12, 1f, spriteEffects2, 0f);
23095							mySpriteBatch.Draw(value6, vector14 + spinningpoint.RotatedBy(num55), value7, color12, num55, origin2, 1f, spriteEffects2, 0f);
23096						}
23097						mySpriteBatch.Draw(value4, vector9 + spinningpoint2.RotatedBy(rotation8), value5, color10, rotation8, origin, 1f, spriteEffects2, 0f);
23098						mySpriteBatch.Draw(value3, vector9, frame, color10, rotation8, vector12, 1f, spriteEffects2, 0f);
23099						mySpriteBatch.Draw(TextureAssets.GlowMask[226].Value, vector9, frame, color11 * (0.7f + 0.3f * lerpValue), rotation8, vector12, 1f, spriteEffects2, 0f);
23100						mySpriteBatch.Draw(value6, vector9 + spinningpoint.RotatedBy(rotation8), value7, color10, rotation8, origin2, 1f, spriteEffects2, 0f);
23101						return;
23102					}
23103					case 690:
23104					{
23105						LoadTiles(105);
23106						Texture2D value18 = TextureAssets.Tile[105].Value;
23107						Vector2 position10 = rCurrentNPC.Center - screenPos;
23108						position10.Y -= 3f;
23109						float rotation9 = rCurrentNPC.rotation;
23110						Microsoft.Xna.Framework.Color alpha2 = rCurrentNPC.GetAlpha(npcColor);
23111						SpriteEffects effects = SpriteEffects.None;
23112						int num74 = (int)rCurrentNPC.ai[1];
23113						int num75 = 55;
23114						int num76 = 3;
23115						int num77 = num74 % num75;
23116						int num78 = num74 / num75;
23117						if (rCurrentNPC.direction == 1)
23118						{
23119							num78 += num76;
23120						}
23121						for (int num79 = 0; num79 < 2; num79++)
23122						{
23123							for (int num80 = 0; num80 < 3; num80++)
23124							{
23125								int x = num77 * 36 + num79 * 18;
23126								int y2 = num78 * 54 + num80 * 18;
23127								Microsoft.Xna.Framework.Rectangle value19 = new Microsoft.Xna.Framework.Rectangle(x, y2, 16, 16);
23128								Vector2 origin8 = new Vector2(1f - (float)num79, 1.5f - (float)num80) * 16f;
23129								mySpriteBatch.Draw(value18, position10, value19, alpha2, rotation9, origin8, 1f, effects, 0f);
23130							}
23131						}
23132						return;
23133					}
23134					case 657:
23135					{
23136						Texture2D value23 = TextureAssets.Npc[type].Value;
23137						Vector2 position14 = rCurrentNPC.Bottom - screenPos;
23138						position14.Y += 2f;
23139						int num89 = npcFrameCount[rCurrentNPC.type];
23140						int num90 = rCurrentNPC.frame.Y / rCurrentNPC.frame.Height;
23141						Microsoft.Xna.Framework.Rectangle rectangle8 = value23.Frame(2, 16, num90 / num89, num90 % num89);
23142						rectangle8.Inflate(0, -2);
23143						Vector2 origin10 = rectangle8.Size() * new Vector2(0.5f, 1f);
23144						Microsoft.Xna.Framework.Color color21 = Microsoft.Xna.Framework.Color.Lerp(Microsoft.Xna.Framework.Color.White, npcColor, 0.5f);
23145						if (rCurrentNPC.life <= rCurrentNPC.lifeMax / 2)
23146						{
23147							DrawNPCDirect_QueenSlimeWings(rCurrentNPC, mySpriteBatch, screenPos, rCurrentNPC.Center, color21);
23148						}
23149						Texture2D value24 = TextureAssets.Extra[186].Value;
23150						Microsoft.Xna.Framework.Rectangle rectangle9 = value24.Frame();
23151						Vector2 origin11 = rectangle9.Size() * new Vector2(0.5f, 0.5f);
23152						Vector2 vector20 = new Vector2(rCurrentNPC.Center.X, rCurrentNPC.Center.Y);
23153						float num91 = 0f;
23154						switch (num90)
23155						{
23156						case 1:
23157						case 6:
23158							num91 -= 10f;
23159							break;
23160						case 3:
23161						case 5:
23162							num91 += 10f;
23163							break;
23164						case 4:
23165						case 12:
23166						case 13:
23167						case 14:
23168						case 15:
23169							num91 += 18f;
23170							break;
23171						case 7:
23172						case 8:
23173							num91 -= 14f;
23174							break;
23175						case 9:
23176							num91 -= 16f;
23177							break;
23178						case 10:
23179							num91 -= 18f;
23180							break;
23181						case 11:
23182							num91 += 20f;
23183							break;
23184						case 20:
23185							num91 -= 14f;
23186							break;
23187						case 21:
23188						case 23:
23189							num91 -= 18f;
23190							break;
23191						case 22:
23192							num91 -= 22f;
23193							break;
23194						}
23195						vector20.Y += num91;
23196						if (rCurrentNPC.rotation != 0f)
23197						{
23198							vector20 = vector20.RotatedBy(rCurrentNPC.rotation, rCurrentNPC.Bottom);
23199						}
23200						vector20 -= screenPos;
23201						if (!rCurrentNPC.IsABestiaryIconDummy)
23202						{
23203							mySpriteBatch.End();
23204							mySpriteBatch.Begin(SpriteSortMode.Immediate, BlendState.AlphaBlend, SamplerState.PointClamp, DepthStencilState.Default, RasterizerState.CullNone, null, Transform);
23205						}
23206						GameShaders.Misc["QueenSlime"].Apply();
23207						if (rCurrentNPC.ai[0] == 4f && rCurrentNPC.velocity.Y != 0f)

```


---

## 🤖 Assistant · 2026-08-11T07:14:19.481Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This is a huge method. Continue reading. I'll read the next chunks. Let me continue from 23208.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:14:19.567Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "limit": 800,
 "offset": 23208
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:19.802Z

**📎 ToolResult**

```
23208						{
23209							float num92 = 1f;
23210							if (rCurrentNPC.ai[2] == 1f)
23211							{
23212								num92 = 6f;
23213							}
23214							for (int num93 = 7; num93 >= 0; num93--)
23215							{
23216								float num94 = 1f - (float)num93 / 8f;
23217								Vector2 vector21 = rCurrentNPC.oldPos[num93] + new Vector2((float)rCurrentNPC.width * 0.5f, rCurrentNPC.height);
23218								vector21 -= (rCurrentNPC.Bottom - Vector2.Lerp(vector21, rCurrentNPC.Bottom, 0.75f)) * num92;
23219								vector21 -= screenPos;
23220								Microsoft.Xna.Framework.Color color22 = color21 * num94;
23221								mySpriteBatch.Draw(value23, vector21, rectangle8, color22, rCurrentNPC.rotation, origin10, rCurrentNPC.scale, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
23222							}
23223						}
23224						if (!rCurrentNPC.IsABestiaryIconDummy)
23225						{
23226							mySpriteBatch.End();
23227							mySpriteBatch.Begin(SpriteSortMode.Deferred, BlendState.AlphaBlend, DefaultSamplerState, DepthStencilState.None, Rasterizer, null, Transform);
23228						}
23229						pixelShader.CurrentTechnique.Passes[0].Apply();
23230						mySpriteBatch.Draw(value24, vector20, rectangle9, color21, rCurrentNPC.rotation, origin11, 1f, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
23231						GameShaders.Misc["QueenSlime"].Apply();
23232						if (!rCurrentNPC.IsABestiaryIconDummy)
23233						{
23234							mySpriteBatch.End();
23235							mySpriteBatch.Begin(SpriteSortMode.Immediate, BlendState.AlphaBlend, SamplerState.PointClamp, DepthStencilState.Default, RasterizerState.CullNone, null, Transform);
23236						}
23237						DrawData value25 = new DrawData(value23, position14, rectangle8, rCurrentNPC.GetAlpha(color21), rCurrentNPC.rotation, origin10, rCurrentNPC.scale, spriteEffects ^ SpriteEffects.FlipHorizontally);
23238						GameShaders.Misc["QueenSlime"].Apply(value25);
23239						value25.Draw(mySpriteBatch);
23240						pixelShader.CurrentTechnique.Passes[0].Apply();
23241						if (!rCurrentNPC.IsABestiaryIconDummy)
23242						{
23243							mySpriteBatch.End();
23244							mySpriteBatch.Begin(SpriteSortMode.Deferred, BlendState.AlphaBlend, DefaultSamplerState, DepthStencilState.None, Rasterizer, null, Transform);
23245						}
23246						Texture2D value26 = TextureAssets.Extra[177].Value;
23247						rectangle8 = value26.Frame();
23248						origin10 = rectangle8.Size() * new Vector2(0.5f, 0.5f);
23249						position14 = new Vector2(rCurrentNPC.Center.X, rCurrentNPC.Top.Y - (float)rectangle8.Bottom + 44f);
23250						float num95 = 0f;
23251						switch (num90)
23252						{
23253						case 1:
23254							num95 -= 10f;
23255							break;
23256						case 3:
23257						case 5:
23258						case 6:
23259							num95 += 10f;
23260							break;
23261						case 4:
23262						case 12:
23263						case 13:
23264						case 14:
23265						case 15:
23266							num95 += 18f;
23267							break;
23268						case 7:
23269						case 8:
23270							num95 -= 14f;
23271							break;
23272						case 9:
23273							num95 -= 16f;
23274							break;
23275						case 10:
23276							num95 -= 18f;
23277							break;
23278						case 11:
23279							num95 += 20f;
23280							break;
23281						case 20:
23282							num95 -= 14f;
23283							break;
23284						case 21:
23285						case 23:
23286							num95 -= 18f;
23287							break;
23288						case 22:
23289							num95 -= 22f;
23290							break;
23291						}
23292						position14.Y += num95;
23293						if (rCurrentNPC.rotation != 0f)
23294						{
23295							position14 = position14.RotatedBy(rCurrentNPC.rotation, rCurrentNPC.Bottom);
23296						}
23297						position14 -= screenPos;
23298						mySpriteBatch.Draw(value26, position14, rectangle8, color21, rCurrentNPC.rotation, origin10, 1f, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
23299						return;
23300					}
23301					case 576:
23302					case 577:
23303					{
23304						Texture2D value13 = TextureAssets.Npc[type].Value;
23305						Vector2 vector16 = rCurrentNPC.Bottom - screenPos;
23306						Microsoft.Xna.Framework.Rectangle rectangle4 = value13.Frame(5, 10, rCurrentNPC.frame.Y / 10, rCurrentNPC.frame.Y % 10);
23307						Vector2 origin5 = rectangle4.Size() * new Vector2(0.5f, 1f);
23308						origin5.Y -= 4f;
23309						int num67 = 94;
23310						if (rCurrentNPC.spriteDirection == 1)
23311						{
23312							origin5.X = num67;
23313						}
23314						else
23315						{
23316							origin5.X = rectangle4.Width - num67;
23317						}
23318						Microsoft.Xna.Framework.Color value14 = Microsoft.Xna.Framework.Color.White;
23319						float amount3 = 0f;
23320						float amount4 = 0f;
23321						int num68 = 0;
23322						float num69 = 0f;
23323						Microsoft.Xna.Framework.Color color17 = npcColor;
23324						if (rCurrentNPC.localAI[3] < 60f)
23325						{
23326							_ = 8f;
23327							float num70 = rCurrentNPC.localAI[3] / 60f;
23328							num68 = 3;
23329							num69 = 1f - num70 * num70;
23330							value14 = new Microsoft.Xna.Framework.Color(127, 0, 255, 0);
23331							amount4 = 1f;
23332							color17 = Microsoft.Xna.Framework.Color.Lerp(Microsoft.Xna.Framework.Color.Transparent, color17, num70 * num70);
23333						}
23334						for (int num71 = 0; num71 < num68; num71++)
23335						{
23336							Microsoft.Xna.Framework.Color value15 = npcColor;
23337							value15 = Microsoft.Xna.Framework.Color.Lerp(value15, value14, amount3);
23338							value15 = rCurrentNPC.GetAlpha(value15);
23339							value15 = Microsoft.Xna.Framework.Color.Lerp(value15, value14, amount4);
23340							value15 *= 1f - num69;
23341							Vector2 position8 = vector16;
23342							position8 -= new Vector2(value13.Width, value13.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
23343							position8 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
23344							mySpriteBatch.Draw(value13, position8, rectangle4, value15, rCurrentNPC.rotation, origin5, rCurrentNPC.scale, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
23345						}
23346						mySpriteBatch.Draw(value13, vector16, rectangle4, rCurrentNPC.GetAlpha(color17), rCurrentNPC.rotation, origin5, rCurrentNPC.scale, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
23347						return;
23348					}
23349					case 696:
23350					{
23351						Texture2D value16 = TextureAssets.Npc[type].Value;
23352						Vector2 vector17 = rCurrentNPC.Bottom - screenPos;
23353						Microsoft.Xna.Framework.Rectangle rectangle5 = value16.Frame(6, 27, rCurrentNPC.frame.Y / 9, rCurrentNPC.frame.Y % 9);
23354						Vector2 origin6 = rectangle5.Size() * new Vector2(0.5f, 1f);
23355						origin6.Y -= 4f;
23356						Microsoft.Xna.Framework.Color newColor2 = npcColor;
23357						mySpriteBatch.Draw(value16, vector17, rectangle5, rCurrentNPC.GetAlpha(newColor2), rCurrentNPC.rotation, origin6, rCurrentNPC.scale, spriteEffects, 0f);
23358						rectangle5.Y += rectangle5.Height * 18;
23359						ulong seed = TileFrameSeed;
23360						for (int num72 = 0; num72 < 2; num72++)
23361						{
23362							Vector2 vector18 = new Vector2(Utils.RandomInt(ref seed, -1, 2), Utils.RandomInt(ref seed, -1, 2));
23363							if (num72 == 0)
23364							{
23365								vector18 = Vector2.Zero;
23366							}
23367							mySpriteBatch.Draw(value16, vector17 + vector18, rectangle5, new Microsoft.Xna.Framework.Color(255, 255, 255, 127) * rCurrentNPC.Opacity, rCurrentNPC.rotation, origin6, rCurrentNPC.scale, spriteEffects, 0f);
23368						}
23369						if (rCurrentNPC.ai[0] == 2f)
23370						{
23371							int num73 = 60;
23372							int emoteId = 0;
23373							if (rCurrentNPC.ai[1] < (float)num73)
23374							{
23375								EmoteBubble.DrawTemporaryBubble(spriteBatch, emoteId, num73, num73 - (int)rCurrentNPC.ai[1], rCurrentNPC);
23376							}
23377						}
23378						return;
23379					}
23380					case 594:
23381					{
23382						Texture2D value11 = TextureAssets.Npc[type].Value;
23383						Vector2 position7 = rCurrentNPC.Top - screenPos;
23384						Microsoft.Xna.Framework.Rectangle rectangle3 = value11.Frame(8, 1, rCurrentNPC.frame.Y);
23385						Microsoft.Xna.Framework.Rectangle value12 = value11.Frame(8);
23386						Vector2 origin4 = rectangle3.Size() * new Vector2(0.5f, 0f);
23387						Microsoft.Xna.Framework.Color color16 = npcColor;
23388						float scale3 = 1f;
23389						NPC nPC = rCurrentNPC.AI_113_WindyBalloon_GetSlaveNPC();
23390						if (nPC != null)
23391						{
23392							scale3 = nPC.scale;
23393							if (nPC.ai[1] > 0f)
23394							{
23395								DrawNPC_SlimeItem(nPC, nPC.type, color16, rCurrentNPC.rotation);
23396							}
23397							mySpriteBatch.Draw(value11, position7, value12, nPC.GetAlpha(color16), rCurrentNPC.rotation, origin4, scale3, spriteEffects, 0f);
23398							mySpriteBatch.Draw(value11, position7, value12, nPC.GetColor(color16), rCurrentNPC.rotation, origin4, scale3, spriteEffects, 0f);
23399						}
23400						mySpriteBatch.Draw(value11, position7, rectangle3, rCurrentNPC.GetAlpha(color16), rCurrentNPC.rotation, origin4, scale3, spriteEffects, 0f);
23401						return;
23402					}
23403					case 686:
23404					{
23405						Texture2D value17 = TextureAssets.Npc[type].Value;
23406						Vector2 position9 = rCurrentNPC.Top - screenPos;
23407						Microsoft.Xna.Framework.Rectangle rectangle6 = value17.Frame();
23408						Vector2 origin7 = rectangle6.Size() * new Vector2(0.5f, 0f);
23409						Microsoft.Xna.Framework.Color newColor3 = npcColor;
23410						mySpriteBatch.Draw(value17, position9, rectangle6, rCurrentNPC.GetAlpha(newColor3), rCurrentNPC.rotation, origin7, rCurrentNPC.scale, spriteEffects, 0f);
23411						return;
23412					}
23413					case 564:
23414					case 565:
23415					{
23416						Texture2D value20 = TextureAssets.Npc[type].Value;
23417						Vector2 vector19 = rCurrentNPC.Bottom - screenPos;
23418						Microsoft.Xna.Framework.Rectangle rectangle7 = value20.Frame(5, 9, rCurrentNPC.frame.Y / 9, rCurrentNPC.frame.Y % 9);
23419						Vector2 origin9 = rectangle7.Size() * new Vector2(0.5f, 1f);
23420						origin9.Y -= 10f;
23421						int num81 = 52;
23422						if (rCurrentNPC.spriteDirection == 1)
23423						{
23424							origin9.X = num81;
23425						}
23426						else
23427						{
23428							origin9.X = rectangle7.Width - num81;
23429						}
23430						Microsoft.Xna.Framework.Color value21 = Microsoft.Xna.Framework.Color.White;
23431						float amount5 = 0f;
23432						float amount6 = 0f;
23433						int num82 = 0;
23434						float num83 = 0f;
23435						float num84 = 0f;
23436						Microsoft.Xna.Framework.Color color18 = npcColor;
23437						if (rCurrentNPC.localAI[3] < 60f)
23438						{
23439							float num85 = rCurrentNPC.localAI[3] / 60f;
23440							num82 = 3;
23441							num83 = 1f - num85 * num85;
23442							num84 = 8f;
23443							value21 = new Microsoft.Xna.Framework.Color(127, 0, 255, 0);
23444							amount6 = 1f;
23445							color18 = Microsoft.Xna.Framework.Color.Lerp(Microsoft.Xna.Framework.Color.Transparent, color18, num85 * num85);
23446						}
23447						for (int num86 = 0; num86 < num82; num86++)
23448						{
23449							Microsoft.Xna.Framework.Color value22 = npcColor;
23450							value22 = Microsoft.Xna.Framework.Color.Lerp(value22, value21, amount5);
23451							value22 = rCurrentNPC.GetAlpha(value22);
23452							value22 = Microsoft.Xna.Framework.Color.Lerp(value22, value21, amount6);
23453							value22 *= 1f - num83;
23454							Vector2 position11 = vector19;
23455							position11 -= new Vector2(value20.Width, value20.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
23456							position11 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
23457							position11 += ((float)num86 / (float)num82 * (MathF.PI * 2f)).ToRotationVector2() * num84 * num83;
23458							mySpriteBatch.Draw(value20, position11, rectangle7, value22, rCurrentNPC.rotation, origin9, rCurrentNPC.scale, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
23459						}
23460						Microsoft.Xna.Framework.Color alpha3 = rCurrentNPC.GetAlpha(color18);
23461						num82 = 4;
23462						num84 = 4f;
23463						num83 = 0.625f + (float)Math.Sin(GlobalTimeWrappedHourly * (MathF.PI * 2f) * 0.75f + MathF.PI) * 0.125f;
23464						for (int num87 = 0; num87 < num82; num87++)
23465						{
23466							Microsoft.Xna.Framework.Color color19 = alpha3;
23467							color19 *= 1f - num83;
23468							Vector2 position12 = vector19;
23469							position12 -= new Vector2(value20.Width, value20.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
23470							position12 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
23471							position12 += ((float)num87 / (float)num82 * (MathF.PI * 2f)).ToRotationVector2() * num84 * num83;
23472							mySpriteBatch.Draw(value20, position12, rectangle7, color19, rCurrentNPC.rotation, origin9, rCurrentNPC.scale, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
23473						}
23474						mySpriteBatch.Draw(value20, vector19, rectangle7, alpha3, rCurrentNPC.rotation, origin9, rCurrentNPC.scale, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
23475						if (rCurrentNPC.Opacity > 0f)
23476						{
23477							Microsoft.Xna.Framework.Color white2 = Microsoft.Xna.Framework.Color.White;
23478							white2.A /= 2;
23479							white2 *= rCurrentNPC.Opacity;
23480							mySpriteBatch.Draw(TextureAssets.GlowMask[225].Value, vector19, rectangle7, white2, rCurrentNPC.rotation, origin9, rCurrentNPC.scale, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
23481							num82 = 4;
23482							num84 = 4f;
23483							num83 = 0.5f + (float)Math.Sin(GlobalTimeWrappedHourly * (MathF.PI * 2f) * 0.75f) * 0.5f;
23484							for (int num88 = 0; num88 < num82; num88++)
23485							{
23486								Microsoft.Xna.Framework.Color color20 = white2 * 0.35f;
23487								color20 *= 1f - num83;
23488								Vector2 position13 = vector19;
23489								position13 -= new Vector2(value20.Width, value20.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
23490								position13 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
23491								position13 += ((float)num88 / (float)num82 * (MathF.PI * 2f)).ToRotationVector2() * num84 * num83;
23492								mySpriteBatch.Draw(TextureAssets.GlowMask[225].Value, position13, rectangle7, color20, rCurrentNPC.rotation, origin9, rCurrentNPC.scale, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
23493							}
23494						}
23495						return;
23496					}
23497					case 548:
23498					{
23499						Texture2D value9 = TextureAssets.Npc[type].Value;
23500						Vector2 vector15 = rCurrentNPC.Bottom - screenPos;
23501						Microsoft.Xna.Framework.Rectangle rectangle2 = value9.Frame();
23502						Vector2 origin3 = rectangle2.Size() / 2f;
23503						origin3.Y += 30f;
23504						origin3.Y += 8f;
23505						origin3.X -= 1f;
23506						Microsoft.Xna.Framework.Color white = Microsoft.Xna.Framework.Color.White;
23507						float amount = 0f;
23508						float amount2 = 0f;
23509						int num56 = 0;
23510						float num57 = 0f;
23511						float num58 = 0f;
23512						Microsoft.Xna.Framework.Color newColor = npcColor;
23513						for (int num59 = 0; num59 < num56; num59++)
23514						{
23515							Microsoft.Xna.Framework.Color value10 = npcColor;
23516							value10 = Microsoft.Xna.Framework.Color.Lerp(value10, white, amount);
23517							value10 = rCurrentNPC.GetAlpha(value10);
23518							value10 = Microsoft.Xna.Framework.Color.Lerp(value10, white, amount2);
23519							value10 *= 1f - num57;
23520							Vector2 position3 = vector15;
23521							position3 -= new Vector2(value9.Width, value9.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
23522							position3 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
23523							position3 += ((float)num59 / (float)num56 * (MathF.PI * 2f)).ToRotationVector2() * num58 * num57;
23524							mySpriteBatch.Draw(value9, position3, rectangle2, value10, rCurrentNPC.rotation, origin3, rCurrentNPC.scale, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
23525						}
23526						Microsoft.Xna.Framework.Color alpha = rCurrentNPC.GetAlpha(newColor);
23527						num56 = 4;
23528						num58 = 4f;
23529						num57 = 0.625f + (float)Math.Sin(GlobalTimeWrappedHourly * (MathF.PI * 2f) * 0.75f + MathF.PI) * 0.125f;
23530						for (int num60 = 0; num60 < num56; num60++)
23531						{
23532							Microsoft.Xna.Framework.Color color13 = alpha;
23533							color13.A = 0;
23534							color13 *= 1f - num57;
23535							Vector2 position4 = vector15;
23536							position4 -= new Vector2(value9.Width, value9.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
23537							position4 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
23538							position4 += ((float)num60 / (float)num56 * (MathF.PI * 2f)).ToRotationVector2() * num58 * num57;
23539							mySpriteBatch.Draw(value9, position4, rectangle2, color13, rCurrentNPC.rotation, origin3, rCurrentNPC.scale, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
23540						}
23541						mySpriteBatch.Draw(value9, vector15, rectangle2, alpha, rCurrentNPC.rotation, origin3, rCurrentNPC.scale, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
23542						if (rCurrentNPC.ai[1] == 2f)
23543						{
23544							float num61 = Math.Min(1f, rCurrentNPC.ai[0] / 120f);
23545							mySpriteBatch.Draw(value9, vector15, rectangle2, new Microsoft.Xna.Framework.Color(1f, 1f, 1f, 0f) * num61, rCurrentNPC.rotation, origin3, rCurrentNPC.scale, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
23546							float progress = MathHelper.Clamp(rCurrentNPC.ai[0] / 450f, 0f, 1f);
23547							if (!Terraria.Graphics.Effects.Filters.Scene["CrystalWin"].IsActive())
23548							{
23549								Terraria.Graphics.Effects.Filters.Scene.Activate("CrystalWin", rCurrentNPC.Center);
23550							}
23551							else
23552							{
23553								Terraria.Graphics.Effects.Filters.Scene["CrystalWin"].GetShader().UseProgress(progress);
23554							}
23555							Terraria.Graphics.Effects.Filters.Scene["CrystalWin"].GetShader().UseTargetPosition(rCurrentNPC.Center);
23556						}
23557						num56 = 4;
23558						num58 = 4f;
23559						num57 = 0.625f + (float)Math.Sin(GlobalTimeWrappedHourly * (MathF.PI * 2f) * 0.75f) * 0.125f;
23560						for (int num62 = 0; num62 < num56; num62++)
23561						{
23562							Microsoft.Xna.Framework.Color color14 = alpha;
23563							color14.A = 0;
23564							color14 *= 0.3f;
23565							color14 *= 1f - num57;
23566							Vector2 position5 = vector15;
23567							position5 -= new Vector2(value9.Width, value9.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
23568							position5 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
23569							position5 += ((float)num62 / (float)num56 * (MathF.PI * 2f)).ToRotationVector2() * num58 * num57;
23570							mySpriteBatch.Draw(value9, position5, rectangle2, color14, rCurrentNPC.rotation, origin3, rCurrentNPC.scale, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
23571						}
23572						if (rCurrentNPC.alpha < 255)
23573						{
23574							float num63 = GlobalTimeWrappedHourly % 3f / 3f;
23575							float num64 = num63;
23576							if (num64 > 0.5f)
23577							{
23578								num64 = 1f - num63;
23579							}
23580							if (num64 < 0f)
23581							{
23582								num64 = 0f;
23583							}
23584							float num65 = (num63 + 0.5f) % 1f;
23585							float num66 = num65;
23586							if (num66 > 0.5f)
23587							{
23588								num66 = 1f - num65;
23589							}
23590							if (num66 < 0f)
23591							{
23592								num66 = 0f;
23593							}
23594							value9 = TextureAssets.GlowMask[239].Value;
23595							rectangle2 = value9.Frame();
23596							origin3 = rectangle2.Size() / 2f;
23597							Vector2 position6 = vector15 + new Vector2(0f, -40f);
23598							Microsoft.Xna.Framework.Color color15 = new Microsoft.Xna.Framework.Color(140, 50, 255, 0);
23599							color15 *= 0.6f;
23600							mySpriteBatch.Draw(value9, position6, rectangle2, color15, rCurrentNPC.rotation, origin3, rCurrentNPC.scale * 0.75f, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
23601							num57 = 1f + num63 * 0.75f;
23602							mySpriteBatch.Draw(value9, position6, rectangle2, color15 * num64, rCurrentNPC.rotation, origin3, rCurrentNPC.scale * 0.75f * num57, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
23603							num57 = 1f + num65 * 0.75f;
23604							mySpriteBatch.Draw(value9, position6, rectangle2, color15 * num66, rCurrentNPC.rotation, origin3, rCurrentNPC.scale * 0.75f * num57, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
23605							value9 = TextureAssets.Extra[89].Value;
23606							rectangle2 = value9.Frame();
23607							origin3 = rectangle2.Size() / 2f;
23608							Vector2 scale2 = new Vector2(0.75f, 1f + num57) * 1.5f;
23609							num57 = 1f + num65 * 0.75f;
23610							if (rCurrentNPC.dontTakeDamageFromHostiles)
23611							{
23612								scale2.Y *= 0.6f;
23613							}
23614							position6.Y -= 6f;
23615							mySpriteBatch.Draw(value9, position6, rectangle2, color15 * num66, rCurrentNPC.rotation + MathF.PI / 2f, origin3, scale2, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
23616							mySpriteBatch.Draw(value9, position6, rectangle2, Microsoft.Xna.Framework.Color.Lerp(color15, Microsoft.Xna.Framework.Color.White, 0.5f), rCurrentNPC.rotation + MathF.PI / 2f, origin3, 1.5f, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
23617						}
23618						return;
23619					}
23620					default:
23621						if (type < 621 || type > 623)
23622						{
23623							break;
23624						}
23625						goto case 371;
23626					case 371:
23627					case 454:
23628					case 455:
23629					case 456:
23630					case 457:
23631					case 458:
23632					case 459:
23633					{
23634						Texture2D value8 = TextureAssets.Npc[type].Value;
23635						Vector2 position2 = rCurrentNPC.Center - screenPos;
23636						position2 -= new Vector2(value8.Width, value8.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
23637						position2 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
23638						mySpriteBatch.Draw(value8, position2, rCurrentNPC.frame, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
23639						return;
23640					}
23641					}
23642					switch (type)
23643					{
23644					case 549:
23645					{
23646						Texture2D value77 = TextureAssets.Npc[type].Value;
23647						Vector2 vector66 = rCurrentNPC.Center - screenPos;
23648						Microsoft.Xna.Framework.Rectangle frame9 = rCurrentNPC.frame;
23649						Vector2 origin24 = new Vector2(70f, 127f);
23650						origin24.Y += 8f;
23651						Vector2 scale6 = new Vector2(rCurrentNPC.scale);
23652						float num269 = rCurrentNPC.localAI[0];
23653						if (num269 < 120f)
23654						{
23655							scale6 *= num269 / 240f + 0.5f;
23656						}
23657						Microsoft.Xna.Framework.Color alpha13 = rCurrentNPC.GetAlpha(npcColor);
23658						float lerpValue2 = Utils.GetLerpValue(0f, 120f, num269, clamped: true);
23659						float num270 = MathHelper.Lerp(32f, 0f, lerpValue2);
23660						Microsoft.Xna.Framework.Color color42 = alpha13;
23661						color42.A = (byte)MathHelper.Lerp((int)color42.A, 0f, lerpValue2);
23662						color42 *= lerpValue2;
23663						if (num269 >= 120f)
23664						{
23665							color42 = alpha13;
23666						}
23667						mySpriteBatch.Draw(value77, vector66, frame9, color42, rCurrentNPC.rotation, origin24, scale6, spriteEffects, 0f);
23668						float y4 = (((rCurrentNPC.ai[0] + 54f) % 180f - 120f) / 180f * 2f * (MathF.PI * 2f)).ToRotationVector2().Y;
23669						if (num269 >= 120f)
23670						{
23671							num270 = y4 * 0f;
23672							color42.A = (byte)((float)(int)color42.A * 0.5f);
23673							color42 *= y4 / 2f + 0.5f;
23674							float num271 = 1f;
23675							for (float num272 = 0f; num272 < num271; num272 += 1f)
23676							{
23677								mySpriteBatch.Draw(value77, vector66 + (MathF.PI * 2f / num271 * num272).ToRotationVector2() * num270, frame9, color42, rCurrentNPC.rotation, origin24, scale6, spriteEffects, 0f);
23678							}
23679						}
23680						float num273 = rCurrentNPC.ai[0] / 180f - 0.76f;
23681						if (num273 < 0f)
23682						{
23683							num273 += 1f;
23684						}
23685						float num274 = 0f;
23686						float num275 = 0f;
23687						float num276 = 0.6f;
23688						float num277 = 0.8f;
23689						if (num273 >= num276 && num273 <= num277)
23690						{
23691							num274 = Utils.GetLerpValue(num276, num277, num273);
23692							num275 = MathHelper.Lerp(0.75f, 0.85f, num274);
23693						}
23694						num276 = num277;
23695						num277 = num276 + 0.13f;
23696						if (num273 >= num276 && num273 <= num277)
23697						{
23698							num274 = 1f - Utils.GetLerpValue(num276, num277, num273);
23699							num275 = MathHelper.Lerp(1.3f, 0.85f, num274);
23700						}
23701						Vector2 vector67 = new Vector2(0f, -150f);
23702						int frameNumber = frame9.Y / frame9.Height;
23703						float num278 = MathHelper.Clamp((num269 - 100f) / 40f, 0f, 1f);
23704						DrawElderEye(mySpriteBatch, rCurrentNPC.Center + vector67, 0.75f * num278, 0.75f, frameNumber, Microsoft.Xna.Framework.Color.White);
23705						DrawElderEye(mySpriteBatch, rCurrentNPC.Center + vector67, 0.75f * num278, 0.75f, frameNumber, new Microsoft.Xna.Framework.Color(255, 255, 255, 127) * (y4 / 2f + 0.5f));
23706						if (num274 > 0f && num275 > 0f)
23707						{
23708							DrawElderEye(mySpriteBatch, rCurrentNPC.Center + vector67, num274 * 0.5f, num275, frameNumber, new Microsoft.Xna.Framework.Color(255, 255, 255, 127));
23709						}
23710						if (num269 < 120f)
23711						{
23712							float num279 = MathF.PI * 2f * lerpValue2 * (float)Math.Pow(lerpValue2, 2.0) * 2f + lerpValue2;
23713							color42.A = (byte)((float)(int)alpha13.A * (float)Math.Pow(lerpValue2, 2.0) * 0.5f);
23714							float num280 = 3f;
23715							for (float num281 = 0f; num281 < num280; num281 += 1f)
23716							{
23717								mySpriteBatch.Draw(value77, vector66 + (num279 + MathF.PI * 2f / num280 * num281).ToRotationVector2() * num270, frame9, color42, rCurrentNPC.rotation, origin24, scale6, spriteEffects, 0f);
23718							}
23719						}
23720						break;
23721					}
23722					case 636:
23723						DrawNPCDirect_HallowBoss(mySpriteBatch, rCurrentNPC, ref screenPos, type, ref npcColor, ref halfSize, spriteEffects);
23724						break;
23725					case 677:
23726						DrawNPCDirect_Faeling(mySpriteBatch, rCurrentNPC, ref screenPos, type, ref npcColor, ref halfSize, spriteEffects);
23727						break;
23728					case 668:
23729						DrawNPCDirect_Deerclops(mySpriteBatch, rCurrentNPC, ref screenPos, type, ref npcColor, ref halfSize, spriteEffects);
23730						break;
23731					case 422:
23732					case 493:
23733					case 507:
23734					case 517:
23735					{
23736						Texture2D value74 = TextureAssets.Npc[type].Value;
23737						Vector2 vector64 = rCurrentNPC.Center - screenPos;
23738						Vector2 vector65 = vector64 - new Vector2(300f, 310f);
23739						vector64 -= new Vector2(value74.Width, value74.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
23740						vector64 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
23741						mySpriteBatch.Draw(value74, vector64, rCurrentNPC.frame, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
23742						switch (type)
23743						{
23744						case 493:
23745						{
23746							value74 = TextureAssets.GlowMask[132].Value;
23747							float num262 = 4f + (rCurrentNPC.GetAlpha(npcColor).ToVector3() - new Vector3(0.5f)).Length() * 4f;
23748							for (int num263 = 0; num263 < 4; num263++)
23749							{
23750								mySpriteBatch.Draw(value74, vector64 + rCurrentNPC.velocity.RotatedBy((float)num263 * (MathF.PI / 2f)) * num262, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(64, 64, 64, 0) * rCurrentNPC.Opacity, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
23751							}
23752							break;
23753						}
23754						case 507:
23755						{
23756							value74 = TextureAssets.GlowMask[143].Value;
23757							float num258 = 4f + (rCurrentNPC.GetAlpha(npcColor).ToVector3() - new Vector3(0.5f)).Length() * 4f;
23758							for (int num259 = 0; num259 < 4; num259++)
23759							{
23760								mySpriteBatch.Draw(value74, vector64 + rCurrentNPC.velocity.RotatedBy((float)num259 * (MathF.PI / 2f)) * num258, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(64, 64, 64, 0) * rCurrentNPC.Opacity, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
23761							}
23762							break;
23763						}
23764						case 422:
23765						{
23766							value74 = TextureAssets.GlowMask[149].Value;
23767							float num260 = 4f + (rCurrentNPC.GetAlpha(npcColor).ToVector3() - new Vector3(0.5f)).Length() * 4f;
23768							for (int num261 = 0; num261 < 4; num261++)
23769							{
23770								mySpriteBatch.Draw(value74, vector64 + rCurrentNPC.velocity.RotatedBy((float)num261 * (MathF.PI / 2f)) * num260, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(64, 64, 64, 0) * rCurrentNPC.Opacity, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
23771							}
23772							break;
23773						}
23774						case 517:
23775						{
23776							value74 = TextureAssets.GlowMask[162].Value;
23777							float num256 = 2f + (rCurrentNPC.GetAlpha(npcColor).ToVector3() - new Vector3(0.5f)).Length() * 9f;
23778							for (int num257 = 0; num257 < 4; num257++)
23779							{
23780								mySpriteBatch.Draw(value74, vector64 + rCurrentNPC.velocity.RotatedBy((float)num257 * (MathF.PI / 2f)) * num256 + Vector2.UnitX * 2f, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(64, 64, 64, 0) * rCurrentNPC.Opacity, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
23781							}
23782							break;
23783						}
23784						}
23785						int num264 = 0;
23786						string key = "";
23787						switch (type)
23788						{
23789						case 422:
23790							num264 = NPC.ShieldStrengthTowerVortex;
23791							key = "Vortex";
23792							break;
23793						case 507:
23794							num264 = NPC.ShieldStrengthTowerNebula;
23795							key = "Nebula";
23796							break;
23797						case 517:
23798							num264 = NPC.ShieldStrengthTowerSolar;
23799							key = "Solar";
23800							break;
23801						case 493:
23802							num264 = NPC.ShieldStrengthTowerStardust;
23803							key = "Stardust";
23804							break;
23805						}
23806						float num265 = (float)num264 / (float)NPC.ShieldStrengthTowerMax;
23807						if (rCurrentNPC.IsABestiaryIconDummy)
23808						{
23809							break;
23810						}
23811						if (num264 > 0)
23812						{
23813							mySpriteBatch.End();
23814							mySpriteBatch.Begin(SpriteSortMode.Immediate, BlendState.AlphaBlend, SamplerState.PointWrap, DepthStencilState.Default, RasterizerState.CullNone, null, Transform);
23815							float num266 = 0f;
23816							if (rCurrentNPC.ai[3] > 0f && rCurrentNPC.ai[3] <= 30f)
23817							{
23818								num266 = 1f - rCurrentNPC.ai[3] / 30f;
23819							}
23820							Terraria.Graphics.Effects.Filters.Scene[key].GetShader().UseIntensity(1f + num266).UseProgress(0f);
23821							DrawData value75 = new DrawData(Assets.Request<Texture2D>("Images/Misc/Perlin", (AssetRequestMode)1).Value, vector65 + new Vector2(300f, 300f), new Microsoft.Xna.Framework.Rectangle(0, 0, 600, 600), Microsoft.Xna.Framework.Color.White * (num265 * 0.8f + 0.2f), rCurrentNPC.rotation, new Vector2(300f, 300f), rCurrentNPC.scale * (1f + num266 * 0.05f), spriteEffects);
23822							GameShaders.Misc["ForceField"].UseColor(new Vector3(1f + num266 * 0.5f));
23823							GameShaders.Misc["ForceField"].Apply(value75);
23824							value75.Draw(mySpriteBatch);
23825							mySpriteBatch.End();
23826							mySpriteBatch.Begin(SpriteSortMode.Deferred, BlendState.AlphaBlend, DefaultSamplerState, DepthStencilState.None, Rasterizer, null, Transform);
23827						}
23828						else if (rCurrentNPC.ai[3] > 0f)
23829						{
23830							mySpriteBatch.End();
23831							mySpriteBatch.Begin(SpriteSortMode.Immediate, BlendState.AlphaBlend, SamplerState.PointWrap, DepthStencilState.Default, RasterizerState.CullNone, null, Transform);
23832							float num267 = rCurrentNPC.ai[3] / 120f;
23833							float num268 = Math.Min(rCurrentNPC.ai[3] / 30f, 1f);
23834							Terraria.Graphics.Effects.Filters.Scene[key].GetShader().UseIntensity(Math.Min(5f, 15f * num267) + 1f).UseProgress(num267);
23835							DrawData value76 = new DrawData(Assets.Request<Texture2D>("Images/Misc/Perlin", (AssetRequestMode)1).Value, vector65 + new Vector2(300f, 300f), new Microsoft.Xna.Framework.Rectangle(0, 0, 600, 600), new Microsoft.Xna.Framework.Color(new Vector4(1f - (float)Math.Sqrt(num268))), rCurrentNPC.rotation, new Vector2(300f, 300f), rCurrentNPC.scale * (1f + num268), spriteEffects);
23836							GameShaders.Misc["ForceField"].UseColor(new Vector3(2f));
23837							GameShaders.Misc["ForceField"].Apply(value76);
23838							value76.Draw(mySpriteBatch);
23839							mySpriteBatch.End();
23840							mySpriteBatch.Begin(SpriteSortMode.Deferred, BlendState.AlphaBlend, DefaultSamplerState, DepthStencilState.None, Rasterizer, null, Transform);
23841						}
23842						else
23843						{
23844							Terraria.Graphics.Effects.Filters.Scene[key].GetShader().UseIntensity(0f).UseProgress(0f);
23845						}
23846						break;
23847					}
23848					case 402:
23849					{
23850						LoadNPC(403);
23851						LoadNPC(404);
23852						Texture2D value79 = TextureAssets.Npc[rCurrentNPC.type].Value;
23853						Vector2 vector69 = rCurrentNPC.Center - screenPos;
23854						vector69 -= new Vector2(value79.Width, value79.Height / npcFrameCount[rCurrentNPC.type]) * rCurrentNPC.scale / 2f;
23855						vector69 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
23856						int num286 = 0;
23857						float num287 = 2f / (float)rCurrentNPC.oldPos.Length * 0.7f;
23858						float num288 = 600f;
23859						float num289 = num288 - 30f;
23860						float num290 = Utils.Remap(rCurrentNPC.ai[2], 0f, num288, 0f, 1f);
23861						float num291 = 1f - Utils.Remap(num290, 0.5f, num289 / num288, 0f, 1f) * Utils.Remap(num290, num289 / num288, 1f, 1f, 0f);
23862						int num292 = rCurrentNPC.oldPos.Length - 1;
23863						while ((float)num292 >= 1f)
23864						{
23865							for (int num293 = 0; num293 < 2; num293++)
23866							{
23867								value79 = ((num286 != 0) ? TextureAssets.Npc[403].Value : TextureAssets.Npc[404].Value);
23868								Vector2 position31 = vector69 + rCurrentNPC.oldPos[num292] - rCurrentNPC.position;
23869								float rotation11 = rCurrentNPC.oldRot[num292];
23870								if (num292 >= 1 && num293 == 1)
23871								{
23872									Vector2 vector70 = Vector2.Lerp(rCurrentNPC.oldPos[num292], rCurrentNPC.oldPos[num292 - 1], 0.5f) - rCurrentNPC.oldPos[num292];
23873									rotation11 = MathHelper.WrapAngle(rCurrentNPC.oldRot[num292 - 1] * 0.5f + rCurrentNPC.oldRot[num292] * 0.5f);
23874									position31 += vector70;
23875								}
23876								float scale7 = rCurrentNPC.scale;
23877								mySpriteBatch.Draw(value79, position31, null, rCurrentNPC.GetAlpha(npcColor) * (0.8f - num287 * (float)num292 / 2f) * num291, rotation11, halfSize, scale7, spriteEffects, 0f);
23878								value79 = ((num286 != 0) ? TextureAssets.GlowMask[133].Value : TextureAssets.GlowMask[134].Value);
23879								mySpriteBatch.Draw(value79, position31, null, new Microsoft.Xna.Framework.Color(255, 255, 255, 0) * (1f - num287 * (float)num292 / 2f) * num291, rotation11, halfSize, scale7, spriteEffects, 0f);
23880								num286++;
23881							}
23882							num292 -= 2;
23883						}
23884						value79 = TextureAssets.Npc[rCurrentNPC.type].Value;
23885						mySpriteBatch.Draw(value79, vector69, rCurrentNPC.frame, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
23886						value79 = TextureAssets.GlowMask[135].Value;
23887						mySpriteBatch.Draw(value79, vector69, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255, 255, 255, 0) * num291, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
23888						DrawPrettyStarSparkle(Utils.Remap(rCurrentNPC.ai[2], 0f, num288, 0f, 1f), SpriteEffects.None, vector69, new Microsoft.Xna.Framework.Color(255, 255, 255, 0), Microsoft.Xna.Framework.Color.CornflowerBlue, num290, 0.5f, num289 / num288, num289 / num288, 1f, MathF.PI * 2f * num290, new Vector2(2f, 2f), new Vector2(2f, 2f));
23889						break;
23890					}
23891					case 519:
23892					{
23893						Texture2D value78 = TextureAssets.Npc[rCurrentNPC.type].Value;
23894						Vector2 vector68 = rCurrentNPC.Center - screenPos;
23895						vector68 -= new Vector2(value78.Width, value78.Height / npcFrameCount[rCurrentNPC.type]) * rCurrentNPC.scale / 2f;
23896						vector68 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
23897						value78 = TextureAssets.Npc[rCurrentNPC.type].Value;
23898						mySpriteBatch.Draw(value78, vector68, rCurrentNPC.frame, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
23899						int num282 = 0;
23900						float num283 = 1f / (float)rCurrentNPC.oldPos.Length * 0.7f;
23901						int num284 = rCurrentNPC.oldPos.Length - 1;
23902						while ((float)num284 >= 0f)
23903						{
23904							float num285 = (float)(rCurrentNPC.oldPos.Length - num284) / (float)rCurrentNPC.oldPos.Length;
23905							Microsoft.Xna.Framework.Color pink = Microsoft.Xna.Framework.Color.Pink;
23906							pink *= 1f - num283 * (float)num284 / 1f;
23907							pink.A = (byte)((float)(int)pink.A * (1f - num285));
23908							mySpriteBatch.Draw(value78, vector68 + rCurrentNPC.oldPos[num284] - rCurrentNPC.position, null, pink, rCurrentNPC.oldRot[num284], halfSize, rCurrentNPC.scale * MathHelper.Lerp(0.3f, 1.1f, num285), spriteEffects, 0f);
23909							num282++;
23910							num284--;
23911						}
23912						break;
23913					}
23914					case 522:
23915					{
23916						Texture2D value73 = TextureAssets.Npc[rCurrentNPC.type].Value;
23917						Vector2 vector63 = rCurrentNPC.Center - screenPos;
23918						vector63 -= new Vector2(value73.Width, value73.Height / npcFrameCount[rCurrentNPC.type]) * rCurrentNPC.scale / 2f;
23919						vector63 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
23920						int num252 = 0;
23921						float num253 = 1f / (float)rCurrentNPC.oldPos.Length * 1.1f;
23922						int num254 = rCurrentNPC.oldPos.Length - 1;
23923						while ((float)num254 >= 0f)
23924						{
23925							float num255 = (float)(rCurrentNPC.oldPos.Length - num254) / (float)rCurrentNPC.oldPos.Length;
23926							Microsoft.Xna.Framework.Color white7 = Microsoft.Xna.Framework.Color.White;
23927							white7 *= 1f - num253 * (float)num254 / 1f;
23928							white7.A = (byte)((float)(int)white7.A * (1f - num255));
23929							mySpriteBatch.Draw(value73, vector63 + rCurrentNPC.oldPos[num254] - rCurrentNPC.position, null, white7, rCurrentNPC.oldRot[num254], halfSize, rCurrentNPC.scale * MathHelper.Lerp(0.8f, 0.3f, num255), spriteEffects, 0f);
23930							num252++;
23931							num254--;
23932						}
23933						value73 = TextureAssets.Extra[57].Value;
23934						mySpriteBatch.Draw(value73, vector63, null, new Microsoft.Xna.Framework.Color(255, 255, 255, 0), 0f, value73.Size() / 2f, rCurrentNPC.scale, spriteEffects, 0f);
23935						break;
23936					}
23937					case 370:
23938					case 372:
23939					case 373:
23940					{
23941						Texture2D value63 = TextureAssets.Npc[type].Value;
23942						Microsoft.Xna.Framework.Color value64 = Microsoft.Xna.Framework.Color.White;
23943						float amount8 = 0f;
23944						bool flag12 = type == 370 && rCurrentNPC.ai[0] > 4f;
23945						bool num226 = type == 370 && rCurrentNPC.ai[0] > 9f;
23946						int num227 = 120;
23947						int num228 = 60;
23948						Microsoft.Xna.Framework.Color color39 = npcColor;
23949						if (num226)
23950						{
23951							npcColor = buffColor(npcColor, 0.4f, 0.8f, 0.4f, 1f);
23952						}
23953						else if (flag12)
23954						{
23955							npcColor = buffColor(npcColor, 0.5f, 0.7f, 0.5f, 1f);
23956						}
23957						else if (type == 370 && rCurrentNPC.ai[0] == 4f && rCurrentNPC.ai[2] > (float)num227)
23958						{
23959							float num229 = rCurrentNPC.ai[2] - (float)num227;
23960							num229 /= (float)num228;
23961							npcColor = buffColor(npcColor, 1f - 0.5f * num229, 1f - 0.3f * num229, 1f - 0.5f * num229, 1f);
23962						}
23963						int num230 = 10;
23964						int num231 = 2;
23965						switch (type)
23966						{
23967						case 370:
23968							if (rCurrentNPC.ai[0] == -1f)
23969							{
23970								num230 = 0;
23971							}
23972							if (rCurrentNPC.ai[0] == 0f || rCurrentNPC.ai[0] == 5f || rCurrentNPC.ai[0] == 10f)
23973							{
23974								num230 = 7;
23975							}
23976							if (rCurrentNPC.ai[0] == 1f)
23977							{
23978								value64 = Microsoft.Xna.Framework.Color.Blue;
23979								amount8 = 0.5f;
23980							}
23981							else
23982							{
23983								color39 = npcColor;
23984							}
23985							break;
23986						case 372:
23987						case 373:
23988							if (rCurrentNPC.ai[0] == 1f)
23989							{
23990								value64 = Microsoft.Xna.Framework.Color.Blue;
23991								amount8 = 0.5f;
23992							}
23993							break;
23994						}
23995						for (int num232 = 1; num232 < num230; num232 += num231)
23996						{
23997							_ = ref rCurrentNPC.oldPos[num232];
23998							Microsoft.Xna.Framework.Color value65 = color39;
23999							value65 = Microsoft.Xna.Framework.Color.Lerp(value65, value64, amount8);
24000							value65 = rCurrentNPC.GetAlpha(value65);
24001							value65 *= (float)(num230 - num232) / 15f;
24002							Vector2 position23 = rCurrentNPC.oldPos[num232] + new Vector2(rCurrentNPC.width, rCurrentNPC.height) / 2f - screenPos;
24003							position23 -= new Vector2(value63.Width, value63.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
24004							position23 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
24005							mySpriteBatch.Draw(value63, position23, rCurrentNPC.frame, value65, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24006						}
24007						int num233 = 0;

```


---

## 🤖 Assistant · 2026-08-11T07:14:20.930Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This is very long. Let me continue reading 24007 onward.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:14:21.151Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "limit": 800,
 "offset": 24007
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:21.294Z

**📎 ToolResult**

```
24007						int num233 = 0;
24008						float num234 = 0f;
24009						float num235 = 0f;
24010						if (type == 370)
24011						{
24012							if (rCurrentNPC.ai[0] == -1f)
24013							{
24014								num233 = 0;
24015							}
24016							if (rCurrentNPC.ai[0] == 3f || rCurrentNPC.ai[0] == 8f)
24017							{
24018								int num236 = 60;
24019								int num237 = 30;
24020								if (rCurrentNPC.ai[2] > (float)num236)
24021								{
24022									num233 = 6;
24023									num234 = 1f - (float)Math.Cos((rCurrentNPC.ai[2] - (float)num236) / (float)num237 * (MathF.PI * 2f));
24024									num234 /= 3f;
24025									num235 = 40f;
24026								}
24027							}
24028							if (rCurrentNPC.ai[0] == 4f && rCurrentNPC.ai[2] > (float)num227)
24029							{
24030								num233 = 6;
24031								num234 = 1f - (float)Math.Cos((rCurrentNPC.ai[2] - (float)num227) / (float)num228 * (MathF.PI * 2f));
24032								num234 /= 3f;
24033								num235 = 60f;
24034							}
24035							if (rCurrentNPC.ai[0] == 9f && rCurrentNPC.ai[2] > (float)num227)
24036							{
24037								num233 = 6;
24038								num234 = 1f - (float)Math.Cos((rCurrentNPC.ai[2] - (float)num227) / (float)num228 * (MathF.PI * 2f));
24039								num234 /= 3f;
24040								num235 = 60f;
24041							}
24042							if (rCurrentNPC.ai[0] == 12f)
24043							{
24044								num233 = 6;
24045								num234 = 1f - (float)Math.Cos(rCurrentNPC.ai[2] / 30f * (MathF.PI * 2f));
24046								num234 /= 3f;
24047								num235 = 20f;
24048							}
24049						}
24050						for (int num238 = 0; num238 < num233; num238++)
24051						{
24052							Microsoft.Xna.Framework.Color value66 = npcColor;
24053							value66 = Microsoft.Xna.Framework.Color.Lerp(value66, value64, amount8);
24054							value66 = rCurrentNPC.GetAlpha(value66);
24055							value66 *= 1f - num234;
24056							Vector2 position24 = rCurrentNPC.Center + ((float)num238 / (float)num233 * (MathF.PI * 2f) + rCurrentNPC.rotation).ToRotationVector2() * num235 * num234 - screenPos;
24057							position24 -= new Vector2(value63.Width, value63.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
24058							position24 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
24059							mySpriteBatch.Draw(value63, position24, rCurrentNPC.frame, value66, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24060						}
24061						Vector2 position25 = rCurrentNPC.Center - screenPos;
24062						position25 -= new Vector2(value63.Width, value63.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
24063						position25 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
24064						mySpriteBatch.Draw(value63, position25, rCurrentNPC.frame, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24065						if (type != 370 || !(rCurrentNPC.ai[0] >= 4f))
24066						{
24067							break;
24068						}
24069						value63 = TextureAssets.DukeFishron.Value;
24070						Microsoft.Xna.Framework.Color color40 = Microsoft.Xna.Framework.Color.Lerp(Microsoft.Xna.Framework.Color.White, Microsoft.Xna.Framework.Color.Yellow, 0.5f);
24071						value64 = Microsoft.Xna.Framework.Color.Yellow;
24072						amount8 = 1f;
24073						num234 = 0.5f;
24074						num235 = 10f;
24075						num231 = 1;
24076						if (rCurrentNPC.ai[0] == 4f)
24077						{
24078							float num239 = rCurrentNPC.ai[2] - (float)num227;
24079							num239 /= (float)num228;
24080							value64 *= num239;
24081							color40 *= num239;
24082						}
24083						if (rCurrentNPC.ai[0] == 12f)
24084						{
24085							float num240 = rCurrentNPC.ai[2];
24086							num240 /= 30f;
24087							if (num240 > 0.5f)
24088							{
24089								num240 = 1f - num240;
24090							}
24091							num240 *= 2f;
24092							num240 = 1f - num240;
24093							value64 *= num240;
24094							color40 *= num240;
24095						}
24096						for (int num241 = 1; num241 < num230; num241 += num231)
24097						{
24098							_ = ref rCurrentNPC.oldPos[num241];
24099							Microsoft.Xna.Framework.Color value67 = color40;
24100							value67 = Microsoft.Xna.Framework.Color.Lerp(value67, value64, amount8);
24101							value67 *= (float)(num230 - num241) / 15f;
24102							Vector2 position26 = rCurrentNPC.oldPos[num241] + new Vector2(rCurrentNPC.width, rCurrentNPC.height) / 2f - screenPos;
24103							position26 -= new Vector2(value63.Width, value63.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
24104							position26 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
24105							mySpriteBatch.Draw(value63, position26, rCurrentNPC.frame, value67, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24106						}
24107						for (int num242 = 1; num242 < num233; num242++)
24108						{
24109							Microsoft.Xna.Framework.Color value68 = color40;
24110							value68 = Microsoft.Xna.Framework.Color.Lerp(value68, value64, amount8);
24111							value68 = rCurrentNPC.GetAlpha(value68);
24112							value68 *= 1f - num234;
24113							Vector2 position27 = rCurrentNPC.Center + ((float)num242 / (float)num233 * (MathF.PI * 2f) + rCurrentNPC.rotation).ToRotationVector2() * num235 * num234 - screenPos;
24114							position27 -= new Vector2(value63.Width, value63.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
24115							position27 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
24116							mySpriteBatch.Draw(value63, position27, rCurrentNPC.frame, value68, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24117						}
24118						mySpriteBatch.Draw(value63, position25, rCurrentNPC.frame, color40, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24119						break;
24120					}
24121					case 439:
24122					case 440:
24123					{
24124						int num243 = rCurrentNPC.frame.Y / (TextureAssets.Npc[type].Height() / npcFrameCount[type]);
24125						Texture2D value69 = TextureAssets.Npc[type].Value;
24126						Texture2D value70 = TextureAssets.Extra[30].Value;
24127						Microsoft.Xna.Framework.Rectangle rectangle12 = value70.Frame();
24128						rectangle12.Height /= 2;
24129						if (num243 >= 4)
24130						{
24131							rectangle12.Y += rectangle12.Height;
24132						}
24133						Microsoft.Xna.Framework.Color white6 = Microsoft.Xna.Framework.Color.White;
24134						float amount9 = 0f;
24135						Microsoft.Xna.Framework.Color color41 = npcColor;
24136						int num244 = 0;
24137						int num245 = 0;
24138						int num246 = 0;
24139						if (rCurrentNPC.ai[0] == -1f)
24140						{
24141							if (rCurrentNPC.ai[1] >= 320f && rCurrentNPC.ai[1] < 960f)
24142							{
24143								white6 = Microsoft.Xna.Framework.Color.White;
24144								amount9 = 0.5f;
24145								num244 = 6;
24146								num245 = 2;
24147								num246 = 1;
24148							}
24149						}
24150						else if (rCurrentNPC.ai[0] == 1f)
24151						{
24152							white6 = Microsoft.Xna.Framework.Color.White;
24153							amount9 = 0.5f;
24154							num244 = 4;
24155							num245 = 2;
24156							num246 = 1;
24157						}
24158						else
24159						{
24160							color41 = npcColor;
24161						}
24162						for (int num247 = num246; num247 < num244; num247 += num245)
24163						{
24164							_ = ref rCurrentNPC.oldPos[num247];
24165							Microsoft.Xna.Framework.Color value71 = color41;
24166							value71 = Microsoft.Xna.Framework.Color.Lerp(value71, white6, amount9);
24167							value71 = rCurrentNPC.GetAlpha(value71);
24168							value71 *= (float)(num244 - num247) / (float)num244;
24169							value71.A = 100;
24170							Vector2 position28 = rCurrentNPC.oldPos[num247] + new Vector2(rCurrentNPC.width, rCurrentNPC.height) / 2f - screenPos;
24171							position28 -= rectangle12.Size() * rCurrentNPC.scale / 2f;
24172							position28 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
24173							mySpriteBatch.Draw(value70, position28, rectangle12, value71, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24174						}
24175						int num248 = 0;
24176						float num249 = 0f;
24177						float num250 = 0f;
24178						if (rCurrentNPC.ai[0] == 5f && rCurrentNPC.ai[1] >= 0f && rCurrentNPC.ai[1] < 30f)
24179						{
24180							num248 = 4;
24181							num249 = 1f - (float)Math.Cos((rCurrentNPC.ai[1] - 0f) / 30f * MathF.PI);
24182							num249 /= 2f;
24183							num250 = 70f;
24184						}
24185						for (int num251 = 0; num251 < num248; num251++)
24186						{
24187							Microsoft.Xna.Framework.Color value72 = npcColor;
24188							value72 = Microsoft.Xna.Framework.Color.Lerp(value72, white6, amount9);
24189							value72 = rCurrentNPC.GetAlpha(value72);
24190							value72 *= 1f - num249;
24191							Vector2 position29 = rCurrentNPC.Center + ((float)num251 / (float)num248 * (MathF.PI * 2f) + rCurrentNPC.rotation).ToRotationVector2() * num250 * num249 - screenPos;
24192							position29 -= new Vector2(value69.Width, value69.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
24193							position29 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
24194							mySpriteBatch.Draw(value70, position29, rectangle12, value72, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24195						}
24196						Vector2 position30 = rCurrentNPC.Center - screenPos;
24197						position30 -= new Vector2(value69.Width, value69.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
24198						position30 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
24199						mySpriteBatch.Draw(value69, position30, rCurrentNPC.frame, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24200						break;
24201					}
24202					case 392:
24203					case 393:
24204					case 394:
24205					case 395:
24206					{
24207						Texture2D value62 = TextureAssets.Npc[type].Value;
24208						Vector2 vec = rCurrentNPC.Center - screenPos + Vector2.UnitY * rCurrentNPC.gfxOffY;
24209						vec = vec.Floor();
24210						float num225 = 0f;
24211						if (type == 393)
24212						{
24213							num225 = -8f;
24214						}
24215						mySpriteBatch.Draw(value62, vec, rCurrentNPC.frame, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize + Vector2.UnitY * num225, rCurrentNPC.scale, spriteEffects, 0f);
24216						if (type == 392)
24217						{
24218							mySpriteBatch.Draw(TextureAssets.GlowMask[48].Value, vec, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(200, 200, 200, 0), rCurrentNPC.rotation, halfSize + Vector2.UnitY * num225, rCurrentNPC.scale, spriteEffects, 0f);
24219						}
24220						if (type == 395)
24221						{
24222							mySpriteBatch.Draw(TextureAssets.GlowMask[49].Value, vec, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(200, 200, 200, 0), rCurrentNPC.rotation, halfSize + Vector2.UnitY * num225, rCurrentNPC.scale, spriteEffects, 0f);
24223						}
24224						if (type == 394)
24225						{
24226							mySpriteBatch.Draw(TextureAssets.GlowMask[50].Value, vec, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(200, 200, 200, 0), rCurrentNPC.rotation, halfSize + Vector2.UnitY * num225, rCurrentNPC.scale, spriteEffects, 0f);
24227						}
24228						break;
24229					}
24230					case 83:
24231					case 84:
24232					case 179:
24233						mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46), rCurrentNPC.frame, Microsoft.Xna.Framework.Color.White, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24234						break;
24235					case 87:
24236					case 88:
24237					case 89:
24238					case 90:
24239					case 91:
24240					case 92:
24241					{
24242						Microsoft.Xna.Framework.Color alpha14 = rCurrentNPC.GetAlpha(npcColor);
24243						byte b7 = (byte)((tileColor.R + tileColor.G + tileColor.B) / 3);
24244						if (alpha14.R < b7)
24245						{
24246							alpha14.R = b7;
24247						}
24248						if (alpha14.G < b7)
24249						{
24250							alpha14.G = b7;
24251						}
24252						if (alpha14.B < b7)
24253						{
24254							alpha14.B = b7;
24255						}
24256						mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46), rCurrentNPC.frame, alpha14, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24257						break;
24258					}
24259					default:
24260					{
24261						switch (type)
24262						{
24263						case 491:
24264						{
24265							Texture2D value42 = TextureAssets.Npc[rCurrentNPC.type].Value;
24266							Microsoft.Xna.Framework.Rectangle frame3 = rCurrentNPC.frame;
24267							Vector2 origin17 = frame3.OriginFlip(new Vector2(208f, 460f), spriteEffects);
24268							Vector2 vector36 = rCurrentNPC.Center - screenPos;
24269							Vector2 vector37 = new Vector2(((spriteEffects & SpriteEffects.FlipHorizontally) == 0) ? 1 : (-1), 1f);
24270							Microsoft.Xna.Framework.Color alpha8 = rCurrentNPC.GetAlpha(npcColor);
24271							mySpriteBatch.Draw(value42, vector36, frame3, alpha8, rCurrentNPC.rotation, origin17, rCurrentNPC.scale, spriteEffects, 0f);
24272							int num112 = (int)rCurrentNPC.localAI[3] / 8;
24273							value42 = TextureAssets.Extra[40].Value;
24274							frame3 = value42.Frame(1, 4, 0, num112 % 4);
24275							origin17 = frame3.Size() * new Vector2(0.5f, 1f);
24276							mySpriteBatch.Draw(value42, vector36 + (new Vector2(102f, -384f) * vector37).RotatedBy(rCurrentNPC.rotation), frame3, alpha8, rCurrentNPC.rotation, origin17, rCurrentNPC.scale, spriteEffects, 0f);
24277							value42 = TextureAssets.Extra[41].Value;
24278							frame3 = value42.Frame(1, 8, 0, num112 % 8);
24279							origin17 = frame3.Size() * new Vector2(0.5f, 0f) + new Vector2(0f, 10f);
24280							for (int num113 = 0; num113 < 5; num113++)
24281							{
24282								mySpriteBatch.Draw(value42, vector36 + (new Vector2(-96 + 34 * num113, 40f) * vector37).RotatedBy(rCurrentNPC.rotation), frame3, alpha8, rCurrentNPC.rotation, origin17, rCurrentNPC.scale, spriteEffects, 0f);
24283							}
24284							value42 = TextureAssets.Extra[42].Value;
24285							frame3 = value42.Frame(1, 4, 0, num112 % 4);
24286							origin17 = frame3.Size() * new Vector2(0.5f, 0f);
24287							for (int num114 = 0; num114 < 2; num114++)
24288							{
24289								mySpriteBatch.Draw(value42, vector36 + (new Vector2(158 - 106 * num114, -302f) * vector37).RotatedBy(rCurrentNPC.rotation), frame3, alpha8, rCurrentNPC.rotation, origin17, rCurrentNPC.scale, spriteEffects, 0f);
24290							}
24291							value42 = TextureAssets.Extra[43].Value;
24292							frame3 = value42.Frame(1, 4, 0, num112 % 4);
24293							origin17 = frame3.Size() * new Vector2(0.5f, 0f);
24294							for (int num115 = 0; num115 < 2; num115++)
24295							{
24296								mySpriteBatch.Draw(value42, vector36 + (new Vector2(42 - 178 * num115, -444f) * vector37).RotatedBy(rCurrentNPC.rotation), frame3, alpha8, rCurrentNPC.rotation, origin17, rCurrentNPC.scale, spriteEffects, 0f);
24297							}
24298							value42 = TextureAssets.Extra[44].Value;
24299							frame3 = value42.Frame(1, 4, 0, num112 % 4);
24300							origin17 = frame3.Size() * new Vector2(0.5f, 0f);
24301							mySpriteBatch.Draw(value42, vector36 + (new Vector2(-134f, -302f) * vector37).RotatedBy(rCurrentNPC.rotation), frame3, alpha8, rCurrentNPC.rotation, origin17, rCurrentNPC.scale, spriteEffects, 0f);
24302							value42 = TextureAssets.Extra[45].Value;
24303							frame3 = value42.Frame(1, 4, 0, (2 + num112) % 4);
24304							origin17 = frame3.Size() * new Vector2(0.5f, 0f);
24305							mySpriteBatch.Draw(value42, vector36 + (new Vector2(-60f, -330f) * vector37).RotatedBy(rCurrentNPC.rotation), frame3, alpha8, rCurrentNPC.rotation, origin17, rCurrentNPC.scale, spriteEffects, 0f);
24306							LoadNPC(492);
24307							if (!TextureAssets.Npc[492].IsLoaded)
24308							{
24309								return;
24310							}
24311							value42 = TextureAssets.Npc[492].Value;
24312							frame3 = value42.Frame(1, 9);
24313							origin17 = frame3.Size() * new Vector2(0.5f, 0f) + new Vector2(0f, 10f);
24314							for (int num116 = 0; num116 < 4; num116++)
24315							{
24316								int num117 = (int)rCurrentNPC.ai[num116];
24317								if (num117 >= 0)
24318								{
24319									frame3.Y = npc[num117].frame.Y;
24320									mySpriteBatch.Draw(value42, vector36 + (new Vector2(-122 + 68 * num116, -20f) * vector37).RotatedBy(rCurrentNPC.rotation), frame3, alpha8, rCurrentNPC.rotation, origin17, rCurrentNPC.scale, spriteEffects, 0f);
24321								}
24322							}
24323							return;
24324						}
24325						case 398:
24326						{
24327							bool flag8 = false;
24328							Texture2D value27 = TextureAssets.Npc[type].Value;
24329							Texture2D value28 = TextureAssets.Extra[16].Value;
24330							Texture2D value29 = TextureAssets.Extra[14].Value;
24331							float num97 = 340f;
24332							float num98 = 0.5f;
24333							Vector2 vector22 = new Vector2(220f, -60f);
24334							Vector2 vector23 = new Vector2(76f, 66f);
24335							Texture2D value30 = TextureAssets.Extra[13].Value;
24336							Vector2 origin12 = new Vector2(value30.Width, 278f);
24337							Vector2 origin13 = new Vector2(0f, 278f);
24338							Vector2 vector24 = new Vector2(0f, 76f);
24339							Vector2 center2 = rCurrentNPC.Center;
24340							Microsoft.Xna.Framework.Point point = (rCurrentNPC.Center + new Vector2(0f, -150f)).ToTileCoordinates();
24341							Microsoft.Xna.Framework.Color alpha5 = rCurrentNPC.GetAlpha(Microsoft.Xna.Framework.Color.Lerp(Lighting.GetColor(point.X, point.Y), Microsoft.Xna.Framework.Color.White, 0.3f));
24342							for (int num99 = 0; num99 < 2; num99++)
24343							{
24344								bool flag9 = num99 == 0;
24345								Vector2 vector25 = new Vector2((!flag9) ? 1 : (-1), 1f);
24346								int num100 = -1;
24347								for (int num101 = 0; num101 < maxNPCs; num101++)
24348								{
24349									if (npc[num101].active && npc[num101].type == 397 && npc[num101].ai[2] == (float)num99 && npc[num101].ai[3] == (float)rCurrentNPC.whoAmI)
24350									{
24351										num100 = num101;
24352										break;
24353									}
24354								}
24355								if (num100 != -1)
24356								{
24357									Vector2 vector26 = center2 + vector22 * vector25;
24358									Vector2 vector27 = (npc[num100].Center + vector24 - vector26) * num98;
24359									if (flag8)
24360									{
24361										dust[Dust.NewDust(vector26 + vector27, 0, 0, 6)].noGravity = true;
24362									}
24363									float num102 = (float)Math.Acos(vector27.Length() / num97) * (0f - vector25.X);
24364									SpriteEffects effects2 = ((!flag9) ? SpriteEffects.FlipHorizontally : SpriteEffects.None);
24365									Vector2 origin14 = vector23;
24366									if (!flag9)
24367									{
24368										origin14.X = (float)value29.Width - origin14.X;
24369									}
24370									mySpriteBatch.Draw(value29, vector26 - screenPos, null, alpha5, vector27.ToRotation() - num102 - MathF.PI / 2f, origin14, 1f, effects2, 0f);
24371									if (flag8)
24372									{
24373										dust[Dust.NewDust(vector26, 0, 0, 6)].noGravity = true;
24374									}
24375									if (flag8)
24376									{
24377										dust[Dust.NewDust(center2, 0, 0, 6)].noGravity = true;
24378									}
24379									if (flag8)
24380									{
24381										dust[Dust.NewDust(vector26 + new Vector2(0f, num97).RotatedBy(vector27.ToRotation() - num102 - MathF.PI / 2f), 0, 0, 6)].noGravity = true;
24382									}
24383								}
24384							}
24385							mySpriteBatch.Draw(value30, center2 - screenPos, null, alpha5, 0f, origin12, 1f, SpriteEffects.None, 0f);
24386							mySpriteBatch.Draw(value30, center2 - screenPos, null, alpha5, 0f, origin13, 1f, SpriteEffects.FlipHorizontally, 0f);
24387							mySpriteBatch.Draw(value28, center2 - screenPos, null, alpha5, 0f, new Vector2(112f, 101f), 1f, SpriteEffects.None, 0f);
24388							mySpriteBatch.Draw(value27, center2 - screenPos, rCurrentNPC.frame, alpha5, 0f, rCurrentNPC.frame.Size() / 2f, 1f, SpriteEffects.None, 0f);
24389							return;
24390						}
24391						case 397:
24392						{
24393							Texture2D value43 = TextureAssets.Npc[type].Value;
24394							float num118 = 0.5f;
24395							Vector2 vector38 = new Vector2(220f, -60f);
24396							Vector2 vector39 = new Vector2(0f, 76f);
24397							Texture2D value44 = TextureAssets.Extra[15].Value;
24398							Vector2 vector40 = new Vector2(60f, 30f);
24399							float num119 = 340f;
24400							Vector2 center3 = npc[(int)rCurrentNPC.ai[3]].Center;
24401							Microsoft.Xna.Framework.Point point4 = rCurrentNPC.Center.ToTileCoordinates();
24402							Microsoft.Xna.Framework.Color alpha9 = rCurrentNPC.GetAlpha(Microsoft.Xna.Framework.Color.Lerp(Lighting.GetColor(point4.X, point4.Y), Microsoft.Xna.Framework.Color.White, 0.3f));
24403							bool flag10 = rCurrentNPC.ai[2] == 0f;
24404							Vector2 vector41 = new Vector2((!flag10) ? 1 : (-1), 1f);
24405							Vector2 origin18 = new Vector2(120f, 180f);
24406							if (!flag10)
24407							{
24408								origin18.X = (float)value43.Width - origin18.X;
24409							}
24410							Texture2D value45 = TextureAssets.Extra[17].Value;
24411							Texture2D value46 = TextureAssets.Extra[19].Value;
24412							Vector2 vector42 = new Vector2(26f, 42f);
24413							if (!flag10)
24414							{
24415								vector42.X = (float)value45.Width - vector42.X;
24416							}
24417							Vector2 vector43 = new Vector2(30f, 66f);
24418							Vector2 vector44 = new Vector2(1f * (0f - vector41.X), 3f);
24419							Texture2D value47 = TextureAssets.Extra[26].Value;
24420							Microsoft.Xna.Framework.Rectangle value48 = value47.Frame();
24421							value48.Height /= 4;
24422							Vector2 vector45 = center3 + vector38 * vector41;
24423							Vector2 vector46 = rCurrentNPC.Center + vector39;
24424							Vector2 v = vector45 - vector46;
24425							v *= 1f - num118;
24426							Vector2 origin19 = vector40;
24427							if (!flag10)
24428							{
24429								origin19.X = (float)value44.Width - origin19.X;
24430							}
24431							float num120 = (float)Math.Acos(v.Length() / num119) * (0f - vector41.X);
24432							mySpriteBatch.Draw(value44, vector46 - screenPos, null, alpha9, v.ToRotation() + num120 - MathF.PI / 2f, origin19, 1f, spriteEffects, 0f);
24433							if (rCurrentNPC.ai[0] == -2f)
24434							{
24435								int num121 = (int)rCurrentNPC.ai[1];
24436								num121 /= 8;
24437								value48.Y += value48.Height * num121;
24438								mySpriteBatch.Draw(value47, rCurrentNPC.Center - screenPos, value48, alpha9, 0f, vector42 - new Vector2(4f, 4f), 1f, spriteEffects, 0f);
24439							}
24440							else
24441							{
24442								mySpriteBatch.Draw(value45, rCurrentNPC.Center - screenPos, null, alpha9, 0f, vector42, 1f, spriteEffects, 0f);
24443								Vector2 vector47 = Utils.Vector2FromElipse(rCurrentNPC.localAI[0].ToRotationVector2(), vector43 * rCurrentNPC.localAI[1]);
24444								mySpriteBatch.Draw(value46, rCurrentNPC.Center - screenPos + vector47 + vector44, null, alpha9, 0f, new Vector2(value46.Width, value46.Height) / 2f, 1f, SpriteEffects.None, 0f);
24445							}
24446							mySpriteBatch.Draw(value43, rCurrentNPC.Center - screenPos, rCurrentNPC.frame, alpha9, 0f, origin18, 1f, spriteEffects, 0f);
24447							return;
24448						}
24449						case 396:
24450						{
24451							Texture2D value33 = TextureAssets.Npc[type].Value;
24452							Vector2 origin15 = new Vector2(191f, 130f) / 2f;
24453							Texture2D value34 = TextureAssets.Extra[18].Value;
24454							Texture2D value35 = TextureAssets.Extra[19].Value;
24455							Vector2 vector28 = new Vector2(19f, 34f);
24456							Vector2 vector29 = new Vector2(27f, 59f);
24457							Vector2 vector30 = new Vector2(0f, 0f);
24458							Texture2D value36 = TextureAssets.Extra[25].Value;
24459							Vector2 vector31 = new Vector2(0f, 214f).RotatedBy(rCurrentNPC.rotation);
24460							Microsoft.Xna.Framework.Rectangle rectangle10 = value36.Frame();
24461							rectangle10.Height /= 3;
24462							rectangle10.Y += rectangle10.Height * (int)(rCurrentNPC.localAI[2] / 7f);
24463							Texture2D value37 = TextureAssets.Extra[29].Value;
24464							Vector2 vector32 = new Vector2(0f, 4f).RotatedBy(rCurrentNPC.rotation);
24465							Microsoft.Xna.Framework.Rectangle rectangle11 = value37.Frame();
24466							rectangle11.Height /= 4;
24467							rectangle11.Y += rectangle11.Height * (int)(rCurrentNPC.localAI[3] / 5f);
24468							Texture2D value38 = TextureAssets.Extra[26].Value;
24469							Microsoft.Xna.Framework.Rectangle value39 = value38.Frame();
24470							value39.Height /= 4;
24471							_ = npc[(int)rCurrentNPC.ai[3]].Center;
24472							Microsoft.Xna.Framework.Point point2 = rCurrentNPC.Center.ToTileCoordinates();
24473							Microsoft.Xna.Framework.Color alpha6 = rCurrentNPC.GetAlpha(Microsoft.Xna.Framework.Color.Lerp(Lighting.GetColor(point2.X, point2.Y), Microsoft.Xna.Framework.Color.White, 0.3f));
24474							if (rCurrentNPC.ai[0] < 0f)
24475							{
24476								int num107 = (int)rCurrentNPC.ai[1];
24477								num107 /= 8;
24478								value39.Y += value39.Height * num107;
24479								mySpriteBatch.Draw(value38, rCurrentNPC.Center - screenPos, value39, alpha6, rCurrentNPC.rotation, vector28 + new Vector2(4f, 4f), 1f, spriteEffects, 0f);
24480							}
24481							else
24482							{
24483								mySpriteBatch.Draw(value34, rCurrentNPC.Center - screenPos, null, alpha6, rCurrentNPC.rotation, vector28, 1f, spriteEffects, 0f);
24484								Vector2 vector33 = Utils.Vector2FromElipse(rCurrentNPC.localAI[0].ToRotationVector2(), vector29 * rCurrentNPC.localAI[1]);
24485								mySpriteBatch.Draw(value35, rCurrentNPC.Center - screenPos + vector33 + vector30, null, alpha6, rCurrentNPC.rotation, new Vector2(value35.Width, value35.Height) / 2f, 1f, SpriteEffects.None, 0f);
24486							}
24487							mySpriteBatch.Draw(value33, rCurrentNPC.Center - screenPos, value33.Frame(3, 3, rCurrentNPC.frame.Y / 3, rCurrentNPC.frame.Y % 3), alpha6, rCurrentNPC.rotation, origin15, 2f, spriteEffects, 0f);
24488							mySpriteBatch.Draw(value37, (rCurrentNPC.Center - screenPos + vector32).Floor(), rectangle11, alpha6, rCurrentNPC.rotation, rectangle11.Size() / 2f, 1f, spriteEffects, 0f);
24489							mySpriteBatch.Draw(value36, (rCurrentNPC.Center - screenPos + vector31).Floor(), rectangle10, alpha6, rCurrentNPC.rotation, rectangle10.Size() / 2f, 1f, spriteEffects, 0f);
24490							return;
24491						}
24492						case 400:
24493						{
24494							Texture2D value40 = TextureAssets.Npc[type].Value;
24495							Texture2D value41 = TextureAssets.Extra[19].Value;
24496							Vector2 origin16 = new Vector2(40f, 40f);
24497							Vector2 vector34 = new Vector2(30f, 30f);
24498							_ = rCurrentNPC.Center;
24499							Microsoft.Xna.Framework.Point point3 = rCurrentNPC.Center.ToTileCoordinates();
24500							Microsoft.Xna.Framework.Color alpha7 = rCurrentNPC.GetAlpha(Microsoft.Xna.Framework.Color.Lerp(Lighting.GetColor(point3.X, point3.Y), Microsoft.Xna.Framework.Color.White, 0.3f));
24501							mySpriteBatch.Draw(value40, rCurrentNPC.Center - screenPos, rCurrentNPC.frame, alpha7, rCurrentNPC.rotation, origin16, 1f, spriteEffects, 0f);
24502							Vector2 vector35 = Utils.Vector2FromElipse(rCurrentNPC.localAI[0].ToRotationVector2(), vector34 * rCurrentNPC.localAI[1]);
24503							mySpriteBatch.Draw(value41, rCurrentNPC.Center - screenPos + vector35, null, alpha7, rCurrentNPC.rotation, value41.Size() / 2f, rCurrentNPC.localAI[2], SpriteEffects.None, 0f);
24504							return;
24505						}
24506						case 416:
24507						{
24508							int num108 = -1;
24509							int num109 = (int)rCurrentNPC.ai[0];
24510							Vector2 position16 = rCurrentNPC.position;
24511							Vector2 spinningpoint3 = Vector2.Zero;
24512							if (npc[num109].active && npc[num109].type == 415)
24513							{
24514								num108 = num109;
24515							}
24516							if (num108 != -1)
24517							{
24518								Vector2 position17 = rCurrentNPC.position;
24519								rCurrentNPC.Bottom = npc[num108].Bottom;
24520								position16 = rCurrentNPC.position;
24521								rCurrentNPC.position = position17;
24522								rCurrentNPC.gfxOffY = npc[num108].gfxOffY;
24523								spinningpoint3 = npc[num108].velocity;
24524							}
24525							Microsoft.Xna.Framework.Rectangle frame2 = rCurrentNPC.frame;
24526							mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(position16.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, position16.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame2, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24527							if (rCurrentNPC.color != default(Microsoft.Xna.Framework.Color))
24528							{
24529								mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(position16.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, position16.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame2, rCurrentNPC.GetColor(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24530							}
24531							mySpriteBatch.Draw(TextureAssets.GlowMask[156].Value, position16 + rCurrentNPC.Size * new Vector2(0.5f, 1f) - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24532							float num110 = 0.5f + (rCurrentNPC.GetAlpha(npcColor).ToVector3() - new Vector3(0.5f)).Length() * 0.5f;
24533							for (int num111 = 0; num111 < 4; num111++)
24534							{
24535								mySpriteBatch.Draw(TextureAssets.GlowMask[156].Value, position16 + rCurrentNPC.Size * new Vector2(0.5f, 1f) - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY) + spinningpoint3.RotatedBy((float)num111 * (MathF.PI / 2f)) * num110, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(64, 64, 64, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24536							}
24537							return;
24538						}
24539						case 399:
24540						{
24541							Texture2D value31 = TextureAssets.Npc[type].Value;
24542							(rCurrentNPC.position - screenPos + Vector2.UnitY * rCurrentNPC.gfxOffY).Floor();
24543							float num103 = 5f;
24544							for (int num104 = 0; (float)num104 < num103; num104++)
24545							{
24546								float num105 = 1f - (GlobalTimeWrappedHourly + (float)num104) % num103 / num103;
24547								Microsoft.Xna.Framework.Color color23 = Microsoft.Xna.Framework.Color.LimeGreen;
24548								if (rCurrentNPC.ai[0] == 1f)
24549								{
24550									color23 = Microsoft.Xna.Framework.Color.Lerp(Microsoft.Xna.Framework.Color.LimeGreen, Microsoft.Xna.Framework.Color.Red, MathHelper.Clamp(rCurrentNPC.ai[1] / 20f, 0f, 1f));
24551								}
24552								if (rCurrentNPC.ai[0] == 2f)
24553								{
24554									color23 = Microsoft.Xna.Framework.Color.Red;
24555								}
24556								color23 *= 1f - num105;
24557								color23.A = 0;
24558								for (int num106 = 0; num106 < 2; num106++)
24559								{
24560									mySpriteBatch.Draw(TextureAssets.Extra[27].Value, rCurrentNPC.Center - screenPos + Vector2.UnitY * (rCurrentNPC.gfxOffY - 4f + 6f), null, color23, MathF.PI / 2f, new Vector2(10f, 48f), num105 * 4f, SpriteEffects.None, 0f);
24561								}
24562							}
24563							mySpriteBatch.Draw(value31, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24564							value31 = TextureAssets.GlowMask[100].Value;
24565							mySpriteBatch.Draw(value31, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(127 - rCurrentNPC.alpha / 2, 127 - rCurrentNPC.alpha / 2, 127 - rCurrentNPC.alpha / 2, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24566							value31 = TextureAssets.Extra[20].Value;
24567							Microsoft.Xna.Framework.Rectangle value32 = value31.Frame(1, 4, 0, (int)rCurrentNPC.ai[0] + 1);
24568							Vector2 position15 = new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)value31.Width * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY + 18f + 6f);
24569							mySpriteBatch.Draw(value31, position15, value32, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24570							value31 = TextureAssets.GlowMask[101].Value;
24571							mySpriteBatch.Draw(value31, position15, value32, new Microsoft.Xna.Framework.Color(127 - rCurrentNPC.alpha / 2, 127 - rCurrentNPC.alpha / 2, 127 - rCurrentNPC.alpha / 2, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24572							return;
24573						}
24574						case 94:
24575						{
24576							for (int num96 = 1; num96 < 6; num96 += 2)
24577							{
24578								_ = ref rCurrentNPC.oldPos[num96];
24579								Microsoft.Xna.Framework.Color alpha4 = rCurrentNPC.GetAlpha(npcColor);
24580								alpha4.R = (byte)(alpha4.R * (10 - num96) / 15);
24581								alpha4.G = (byte)(alpha4.G * (10 - num96) / 15);
24582								alpha4.B = (byte)(alpha4.B * (10 - num96) / 15);
24583								alpha4.A = (byte)(alpha4.A * (10 - num96) / 15);
24584								alpha4 = rCurrentNPC.GetShimmerColor(alpha4);
24585								mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(rCurrentNPC.oldPos[num96].X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.oldPos[num96].Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), rCurrentNPC.frame, alpha4, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24586							}
24587							break;
24588						}
24589						case 384:
24590							return;
24591						}
24592						if (type == 125 || type == 126 || type == 127 || type == 128 || type == 129 || type == 130 || type == 131 || (type == 139 && rCurrentNPC.ai[3] == 0f) || type == 140)
24593						{
24594							for (int num122 = 9; num122 >= 0; num122 -= 2)
24595							{
24596								_ = ref rCurrentNPC.oldPos[num122];
24597								Microsoft.Xna.Framework.Color alpha10 = rCurrentNPC.GetAlpha(npcColor);
24598								alpha10.R = (byte)(alpha10.R * (10 - num122) / 20);
24599								alpha10.G = (byte)(alpha10.G * (10 - num122) / 20);
24600								alpha10.B = (byte)(alpha10.B * (10 - num122) / 20);
24601								alpha10.A = (byte)(alpha10.A * (10 - num122) / 20);
24602								mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(rCurrentNPC.oldPos[num122].X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.oldPos[num122].Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), rCurrentNPC.frame, alpha10, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24603							}
24604						}
24605						if (type == 417 && rCurrentNPC.ai[0] >= 6f && rCurrentNPC.ai[0] <= 6f)
24606						{
24607							for (int num123 = 5; num123 >= 0; num123--)
24608							{
24609								_ = ref rCurrentNPC.oldPos[num123];
24610								Microsoft.Xna.Framework.Color alpha11 = rCurrentNPC.GetAlpha(npcColor);
24611								alpha11.R = (byte)(alpha11.R * (10 - num123) / 20);
24612								alpha11.G = (byte)(alpha11.G * (10 - num123) / 20);
24613								alpha11.B = (byte)(alpha11.B * (10 - num123) / 20);
24614								alpha11.A = (byte)(alpha11.A * (10 - num123) / 20);
24615								mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(rCurrentNPC.oldPos[num123].X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.oldPos[num123].Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), rCurrentNPC.frame, alpha11, rCurrentNPC.oldRot[num123], halfSize, MathHelper.Lerp(0.5f, 1f, (5f - (float)num123) / 6f), spriteEffects, 0f);
24616							}
24617						}
24618						if (type == 419 && rCurrentNPC.ai[2] <= -9f)
24619						{
24620							int num124 = TextureAssets.GlowMask[154].Height() / npcFrameCount[type];
24621							int num125 = rCurrentNPC.frame.Y / num124;
24622							for (int num126 = 6; num126 >= 0; num126--)
24623							{
24624								_ = ref rCurrentNPC.oldPos[num126];
24625								Microsoft.Xna.Framework.Color white3 = Microsoft.Xna.Framework.Color.White;
24626								white3.R = (byte)(255 * (10 - num126) / 20);
24627								white3.G = (byte)(255 * (10 - num126) / 20);
24628								white3.B = (byte)(255 * (10 - num126) / 20);
24629								white3.A = 0;
24630								Microsoft.Xna.Framework.Rectangle frame4 = rCurrentNPC.frame;
24631								int num127 = (num125 - 3 - num126) % 3;
24632								if (num127 < 0)
24633								{
24634									num127 += 3;
24635								}
24636								num127 += 5;
24637								frame4.Y = num124 * num127;
24638								mySpriteBatch.Draw(TextureAssets.GlowMask[154].Value, new Vector2(rCurrentNPC.oldPos[num126].X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.oldPos[num126].Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), frame4, white3, rCurrentNPC.oldRot[num126], halfSize, MathHelper.Lerp(0.75f, 1.2f, (10f - (float)num126) / 10f), spriteEffects, 0f);
24639							}
24640						}
24641						if (type == 418 && (rCurrentNPC.ai[0] == 2f || rCurrentNPC.ai[0] == 4f))
24642						{
24643							Texture2D value49 = TextureAssets.Extra[55].Value;
24644							Vector2 origin20 = new Vector2(value49.Width / 2, value49.Height / 8 + 14);
24645							int num128 = (int)rCurrentNPC.ai[1] / 2;
24646							float num129 = -MathF.PI / 2f * (float)rCurrentNPC.spriteDirection;
24647							float num130 = rCurrentNPC.ai[1] / 45f;
24648							if (num130 > 1f)
24649							{
24650								num130 = 1f;
24651							}
24652							num128 %= 4;
24653							for (int num131 = 6; num131 >= 0; num131--)
24654							{
24655								_ = ref rCurrentNPC.oldPos[num131];
24656								Microsoft.Xna.Framework.Color value50 = Microsoft.Xna.Framework.Color.Lerp(Microsoft.Xna.Framework.Color.Gold, Microsoft.Xna.Framework.Color.OrangeRed, num130);
24657								value50 = Microsoft.Xna.Framework.Color.Lerp(value50, Microsoft.Xna.Framework.Color.Blue, (float)num131 / 12f);
24658								value50.A = (byte)(64f * num130);
24659								value50.R = (byte)(value50.R * (10 - num131) / 20);
24660								value50.G = (byte)(value50.G * (10 - num131) / 20);
24661								value50.B = (byte)(value50.B * (10 - num131) / 20);
24662								value50.A = (byte)(value50.A * (10 - num131) / 20);
24663								value50 *= num130;
24664								int num132 = (num128 - num131) % 4;
24665								if (num132 < 0)
24666								{
24667									num132 += 4;
24668								}
24669								Microsoft.Xna.Framework.Rectangle value51 = value49.Frame(1, 4, 0, num132);
24670								mySpriteBatch.Draw(value49, new Vector2(rCurrentNPC.oldPos[num131].X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.oldPos[num131].Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), value51, value50, rCurrentNPC.oldRot[num131] + num129, origin20, MathHelper.Lerp(0.1f, 1.2f, (10f - (float)num131) / 10f), spriteEffects, 0f);
24671							}
24672						}
24673						if (type == 516)
24674						{
24675							int num133 = TextureAssets.Npc[type].Height() / npcFrameCount[type];
24676							int num134 = rCurrentNPC.frame.Y / num133;
24677							for (int num135 = 6; num135 >= 0; num135--)
24678							{
24679								_ = ref rCurrentNPC.oldPos[num135];
24680								Microsoft.Xna.Framework.Color white4 = Microsoft.Xna.Framework.Color.White;
24681								white4.R = (byte)(255 * (10 - num135) / 20);
24682								white4.G = (byte)(255 * (10 - num135) / 20);
24683								white4.B = (byte)(255 * (10 - num135) / 20);
24684								white4.A = (byte)(255 * (10 - num135) / 20);
24685								white4 = Microsoft.Xna.Framework.Color.Lerp(white4, Microsoft.Xna.Framework.Color.Transparent, (float)num135 / 6f);
24686								Microsoft.Xna.Framework.Rectangle frame5 = rCurrentNPC.frame;
24687								int num136 = (num134 - 4 - num135) % 4;
24688								if (num136 < 0)
24689								{
24690									num136 += 4;
24691								}
24692								frame5.Y = num133 * num136;
24693								mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(rCurrentNPC.oldPos[num135].X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.oldPos[num135].Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), frame5, white4, rCurrentNPC.rotation, halfSize, MathHelper.Lerp(0.35f, 1.2f, (10f - (float)num135) / 10f), spriteEffects, 0f);
24694							}
24695						}
24696						if (rCurrentNPC.type == 390 && rCurrentNPC.IsABestiaryIconDummy)
24697						{
24698							LoadNPC(391);
24699							Texture2D value52 = TextureAssets.Npc[391].Value;
24700							Microsoft.Xna.Framework.Rectangle value53 = value52.Frame(1, npcFrameCount[391], 0, (int)rCurrentNPC.localAI[3]);
24701							Vector2 vector48 = new Vector2(-rCurrentNPC.width - 8, 10f);
24702							mySpriteBatch.Draw(value52, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY) + vector48, value53, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24703						}
24704						Microsoft.Xna.Framework.Rectangle frame6 = rCurrentNPC.frame;
24705						if (type == 182 || type == 289)
24706						{
24707							frame6.Height -= 2;
24708						}
24709						switch (type)
24710						{
24711						case 420:
24712						case 421:
24713						case 423:
24714						case 424:
24715						{
24716							float num140 = 9f + 3f * (float)Math.Cos(MathF.PI * 2f * GlobalTimeWrappedHourly);
24717							Vector2 spinningpoint5 = Vector2.UnitX * num140;
24718							Microsoft.Xna.Framework.Color color25 = Microsoft.Xna.Framework.Color.Teal * (num140 / 12f) * 0.8f;
24719							color25.A /= 2;
24720							for (float num141 = 0f; num141 < MathF.PI * 2f; num141 += MathF.PI / 2f)
24721							{
24722								Vector2 vector51 = rCurrentNPC.position + spinningpoint5.RotatedBy(num141);
24723								mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(vector51.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, vector51.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, color25, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24724							}
24725							break;
24726						}
24727						case 662:
24728						{
24729							float num137 = 4f + 2f * (float)Math.Cos(MathF.PI * 2f * GlobalTimeWrappedHourly);
24730							Vector2 spinningpoint4 = Vector2.UnitX * num137;
24731							Microsoft.Xna.Framework.Color color24 = Microsoft.Xna.Framework.Color.Cyan * (num137 / 12f) * 0.4f;
24732							color24.A /= 4;
24733							for (float num138 = 0.9f; num138 >= 0f; num138 -= 0.125f)
24734							{
24735								Vector2 vector49 = rCurrentNPC.position - rCurrentNPC.velocity * 10f * num138;
24736								mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(vector49.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, vector49.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, color24 * (1f - num138), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24737							}
24738							for (float num139 = 0f; num139 < MathF.PI * 2f; num139 += MathF.PI / 2f)
24739							{
24740								Vector2 vector50 = rCurrentNPC.position + spinningpoint4.RotatedBy(num139);
24741								mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(vector50.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, vector50.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, color24, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24742							}
24743							break;
24744						}
24745						}
24746						if (rCurrentNPC.aiStyle == 7)
24747						{
24748							DrawNPCExtras(rCurrentNPC, beforeDraw: true, num47, num46, npcColor, halfSize, spriteEffects, screenPos);
24749						}
24750						if (type == 346 && (double)rCurrentNPC.life < (double)rCurrentNPC.lifeMax * 0.5)
24751						{
24752							mySpriteBatch.Draw(TextureAssets.SantaTank.Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24753						}
24754						else if (type == 356)
24755						{
24756							frame6.Height--;
24757							mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24758						}
24759						else if (type == 360)
24760						{
24761							int num142 = 0;
24762							if (rCurrentNPC.ai[2] == 0f)
24763							{
24764								if (rCurrentNPC.rotation == 3.14f || rCurrentNPC.rotation == -3.14f)
24765								{
24766									num47 = 2f;
24767								}
24768								if (rCurrentNPC.direction < 0 && (rCurrentNPC.rotation == 1.57f || rCurrentNPC.rotation == 4.71f))
24769								{
24770									num142 = 1;
24771								}
24772								if (rCurrentNPC.direction > 0 && (rCurrentNPC.rotation == 1.57f || rCurrentNPC.rotation == 4.71f))
24773								{
24774									num142 = -1;
24775								}
24776							}
24777							mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale + (float)num142, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24778						}
24779						else if (type == 655)
24780						{
24781							int num143 = 0;
24782							if (rCurrentNPC.ai[2] == 0f)
24783							{
24784								if (rCurrentNPC.rotation == 3.14f || rCurrentNPC.rotation == -3.14f)
24785								{
24786									num47 = 2f;
24787								}
24788								if (rCurrentNPC.direction < 0 && (rCurrentNPC.rotation == 1.57f || rCurrentNPC.rotation == 4.71f))
24789								{
24790									num143 = 1;
24791								}
24792								if (rCurrentNPC.direction > 0 && (rCurrentNPC.rotation == 1.57f || rCurrentNPC.rotation == 4.71f))
24793								{
24794									num143 = -1;
24795								}
24796							}
24797							mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale + (float)num143, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, rCurrentNPC.GetAlpha(Microsoft.Xna.Framework.Color.Orange), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24798						}
24799						else if (type == 266 && rCurrentNPC.life < rCurrentNPC.lifeMax && (expertMode || getGoodWorld))
24800						{
24801							Microsoft.Xna.Framework.Color alpha12 = rCurrentNPC.GetAlpha(npcColor);
24802							float num144 = 1f - (float)rCurrentNPC.life / (float)rCurrentNPC.lifeMax;
24803							if (expertMode)
24804							{
24805								num144 *= 2f;
24806							}

```


---

## 🤖 Assistant · 2026-08-11T07:14:22.556Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Continuing. Read 24806-25600.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:14:22.807Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "limit": 800,
 "offset": 24806
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:22.964Z

**📎 ToolResult**

```
24806							}
24807							num144 *= num144;
24808							if (getGoodWorld)
24809							{
24810								num144 = 1f;
24811							}
24812							num144 = MathHelper.Clamp(num144, 0f, 1f);
24813							alpha12.R = (byte)((float)(int)alpha12.R * num144);
24814							alpha12.G = (byte)((float)(int)alpha12.G * num144);
24815							alpha12.B = (byte)((float)(int)alpha12.B * num144);
24816							alpha12.A = (byte)((float)(int)alpha12.A * num144);
24817							for (int num145 = 0; num145 < 4; num145++)
24818							{
24819								Vector2 position18 = rCurrentNPC.position;
24820								float num146 = Math.Abs(rCurrentNPC.Center.X - Main.player[myPlayer].Center.X);
24821								float num147 = Math.Abs(rCurrentNPC.Center.Y - Main.player[myPlayer].Center.Y);
24822								if (num145 == 0 || num145 == 2)
24823								{
24824									position18.X = Main.player[myPlayer].Center.X + num146;
24825								}
24826								else
24827								{
24828									position18.X = Main.player[myPlayer].Center.X - num146;
24829								}
24830								position18.X -= rCurrentNPC.width / 2;
24831								if (num145 == 0 || num145 == 1)
24832								{
24833									position18.Y = Main.player[myPlayer].Center.Y + num147;
24834								}
24835								else
24836								{
24837									position18.Y = Main.player[myPlayer].Center.Y - num147;
24838								}
24839								position18.Y -= rCurrentNPC.height / 2;
24840								mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(position18.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, position18.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, alpha12, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24841							}
24842							mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24843						}
24844						else if (type == 421 && rCurrentNPC.ai[0] == 5f)
24845						{
24846							Player player = Main.player[rCurrentNPC.target];
24847							if (player.gravDir == -1f)
24848							{
24849								spriteEffects |= SpriteEffects.FlipVertically;
24850							}
24851							mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(player.direction * 4, player.gfxOffY) + ((player.gravDir == 1f) ? player.Top : player.Bottom) - screenPos, frame6, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, frame6.Size() / 2f, rCurrentNPC.scale, spriteEffects, 0f);
24852							mySpriteBatch.Draw(TextureAssets.GlowMask[146].Value, new Vector2(player.direction * 4, player.gfxOffY) + ((player.gravDir == 1f) ? player.Top : player.Bottom) - screenPos, frame6, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, frame6.Size() / 2f, rCurrentNPC.scale, spriteEffects, 0f);
24853						}
24854						else
24855						{
24856							switch (type)
24857							{
24858							case 518:
24859							{
24860								Vector2 vector55 = new Vector2(-10f, 0f);
24861								mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize + vector55, rCurrentNPC.scale, spriteEffects, 0f);
24862								if (rCurrentNPC.color != default(Microsoft.Xna.Framework.Color))
24863								{
24864									mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, rCurrentNPC.GetColor(npcColor), rCurrentNPC.rotation, halfSize + vector55, rCurrentNPC.scale, spriteEffects, 0f);
24865								}
24866								break;
24867							}
24868							case 676:
24869							case 681:
24870							{
24871								if (rCurrentNPC.IsAPortraitDummy)
24872								{
24873									Matrix uIScaleMatrix = UIScaleMatrix;
24874									Microsoft.Xna.Framework.Rectangle scissorRectangle = mySpriteBatch.GraphicsDevice.ScissorRectangle;
24875									mySpriteBatch.End();
24876									mySpriteBatch.Begin(SpriteSortMode.Immediate, BlendState.AlphaBlend, SamplerState.PointClamp, DepthStencilState.Default, ScissorState, null, uIScaleMatrix);
24877									mySpriteBatch.GraphicsDevice.ScissorRectangle = scissorRectangle;
24878								}
24879								else if (!rCurrentNPC.IsABestiaryIconDummy)
24880								{
24881									RasterizerState rasterizerState = mySpriteBatch.GraphicsDevice.RasterizerState;
24882									mySpriteBatch.End();
24883									mySpriteBatch.Begin(SpriteSortMode.Immediate, BlendState.AlphaBlend, SamplerState.PointClamp, DepthStencilState.Default, rasterizerState, null, Transform);
24884								}
24885								DrawData value54 = new DrawData(TextureAssets.Npc[type].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects);
24886								GameShaders.Misc["RainbowTownSlime"].Apply(value54);
24887								value54.Draw(mySpriteBatch);
24888								pixelShader.CurrentTechnique.Passes[0].Apply();
24889								if (rCurrentNPC.IsAPortraitDummy)
24890								{
24891									Matrix uIScaleMatrix2 = UIScaleMatrix;
24892									Microsoft.Xna.Framework.Rectangle scissorRectangle2 = mySpriteBatch.GraphicsDevice.ScissorRectangle;
24893									mySpriteBatch.End();
24894									mySpriteBatch.Begin(SpriteSortMode.Immediate, BlendState.AlphaBlend, SamplerState.PointClamp, DepthStencilState.Default, ScissorState, null, uIScaleMatrix2);
24895									mySpriteBatch.GraphicsDevice.ScissorRectangle = scissorRectangle2;
24896								}
24897								else if (!rCurrentNPC.IsABestiaryIconDummy)
24898								{
24899									mySpriteBatch.End();
24900									mySpriteBatch.Begin(SpriteSortMode.Deferred, BlendState.AlphaBlend, DefaultSamplerState, DepthStencilState.None, Rasterizer, null, Transform);
24901								}
24902								break;
24903							}
24904							case 685:
24905							{
24906								Vector2 scale4 = new Vector2(rCurrentNPC.scale);
24907								float num154 = rCurrentNPC.rotation;
24908								int num155 = 9;
24909								Vector2 vector52 = rCurrentNPC.oldPos[num155];
24910								if (vector52 != Vector2.Zero && rCurrentNPC.velocity.Y == 0f)
24911								{
24912									Vector2 position20 = rCurrentNPC.position;
24913									Vector2 vector53 = vector52 - position20;
24914									float num156 = (float)Math.Sin(vector53.X / 30f * (MathF.PI * 2f));
24915									float num157 = (float)Math.Sin(vector53.Y / 30f * (MathF.PI * 2f));
24916									float num158 = Utils.Remap(vector53.Length(), 0f, 30f, 0f, 1f);
24917									scale4.X += num156 * num158 * 0.25f;
24918									scale4.Y += num157 * num158 * 0.25f;
24919									float num159 = (float)Math.Sin(Utils.Remap(vector53.Length(), 0f, 20f, 0f, 1f) * (MathF.PI * 2f));
24920									num154 += num159 * (MathF.PI / 4f) * 0.1f * (float)rCurrentNPC.spriteDirection;
24921								}
24922								Vector2 vector54 = new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - 2f - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY);
24923								if (rCurrentNPC.velocity.Y == 0f)
24924								{
24925									vector54 = vector54.Floor();
24926									int num160 = 2;
24927									float num161 = vector54.X % 16f;
24928									if (num161 < (float)num160)
24929									{
24930										vector54.X -= num161;
24931									}
24932									if (num161 > (float)(16 - num160))
24933									{
24934										vector54.X += 16f - num161;
24935									}
24936								}
24937								mySpriteBatch.Draw(TextureAssets.Npc[type].Value, vector54, frame6, rCurrentNPC.GetAlpha(npcColor), num154, halfSize, scale4, spriteEffects, 0f);
24938								break;
24939							}
24940							case 267:
24941							{
24942								Vector2 position21 = rCurrentNPC.Center + new Vector2(0f, num47 + num46 + rCurrentNPC.gfxOffY) - screenPos;
24943								mySpriteBatch.Draw(TextureAssets.Npc[type].Value, position21, frame6, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24944								if (rCurrentNPC.color != default(Microsoft.Xna.Framework.Color))
24945								{
24946									mySpriteBatch.Draw(TextureAssets.Npc[type].Value, position21, frame6, rCurrentNPC.GetColor(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24947								}
24948								break;
24949							}
24950							default:
24951								if (rCurrentNPC.aiStyle == 7 && rCurrentNPC.ai[0] == 25f)
24952								{
24953									int num148 = type;
24954									float num149 = Utils.Remap(rCurrentNPC.ai[1], 0f, 60f, 0f, 1f);
24955									mySpriteBatch.End();
24956									mySpriteBatch.Begin(SpriteSortMode.Immediate, BlendState.AlphaBlend, SamplerState.PointClamp, DepthStencilState.Default, RasterizerState.CullNone, null, Transform);
24957									DrawData drawData = new DrawData(TextureAssets.Npc[num148].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, Microsoft.Xna.Framework.Color.White * Utils.Remap(num149, 0f, 1f, 0f, 1f) * ((float)(int)rCurrentNPC.GetAlpha(npcColor).A / 255f), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects);
24958									drawData.shader = ContentSamples.DyeShaderIDs.ColorOnlyShaderIndex;
24959									GameShaders.Armor.Apply(ContentSamples.DyeShaderIDs.ColorOnlyShaderIndex, rCurrentNPC, drawData);
24960									float num150 = Utils.Remap(rCurrentNPC.ai[1], 45f, 90f, 0f, 1f);
24961									for (float num151 = 0f; num151 < 1f; num151 += 1f / 6f)
24962									{
24963										DrawData drawData2 = drawData;
24964										drawData2.color = hslToRgb(num151, 0.9f, 0.65f) * num150 * 0.5f;
24965										drawData2.position += ((GlobalTimeWrappedHourly + num151) * (MathF.PI * 2f)).ToRotationVector2() * 4f * num150;
24966										drawData2.Draw(mySpriteBatch);
24967									}
24968									drawData.Draw(mySpriteBatch);
24969									pixelShader.CurrentTechnique.Passes[0].Apply();
24970									Microsoft.Xna.Framework.Color drawColor = new Microsoft.Xna.Framework.Color(255, 255, 255, 0);
24971									float num152 = (float)Math.Sin(timeForVisualEffects * 6.2831854820251465 / 20.0);
24972									DrawPrettyStarSparkle(num149, SpriteEffects.None, drawData.position, drawColor, hslToRgb(GlobalTimeWrappedHourly % 1f, 1f, 0.65f, 127), Utils.Remap(rCurrentNPC.ai[1], 30f, 60f, 0f, 30f), 0f, 30f, 30f, 36f, 0f, new Vector2(1.5f, 2.5f) * (1f + num152 * 0.025f), new Vector2(2f, 2f));
24973									DrawPrettyStarSparkle(num149, SpriteEffects.None, drawData.position, drawColor, hslToRgb(GlobalTimeWrappedHourly % 1f, 1f, 0.65f, 127), Utils.Remap(rCurrentNPC.ai[1], 30f, 60f, 0f, 30f), 0f, 30f, 30f, 36f, MathF.PI / 4f, new Vector2(2.5f, 2.5f) * (1f + num152 * 0.025f), new Vector2(1f, 1f));
24974									mySpriteBatch.End();
24975									mySpriteBatch.Begin(SpriteSortMode.Deferred, BlendState.AlphaBlend, DefaultSamplerState, DepthStencilState.None, Rasterizer, null, Transform);
24976								}
24977								else
24978								{
24979									int num153 = type;
24980									if (NPC.IsMechQueenUp && num153 == 134)
24981									{
24982										num153 = 136;
24983										LoadNPC(num153);
24984									}
24985									Vector2 position19 = new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale + num45, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY);
24986									mySpriteBatch.Draw(TextureAssets.Npc[num153].Value, position19, frame6, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24987									if (rCurrentNPC.color != default(Microsoft.Xna.Framework.Color))
24988									{
24989										mySpriteBatch.Draw(TextureAssets.Npc[num153].Value, position19, frame6, rCurrentNPC.GetColor(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
24990									}
24991								}
24992								break;
24993							}
24994						}
24995						if (rCurrentNPC.type == 695 && rCurrentNPC.ai[0] == 2f)
24996						{
24997							int num162 = 60;
24998							int emoteId2 = 0;
24999							if (rCurrentNPC.ai[1] < (float)num162)
25000							{
25001								EmoteBubble.DrawTemporaryBubble(spriteBatch, emoteId2, num162, num162 - (int)rCurrentNPC.ai[1], rCurrentNPC);
25002							}
25003						}
25004						if (rCurrentNPC.confused)
25005						{
25006							mySpriteBatch.Draw(TextureAssets.Confuse.Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 - (float)TextureAssets.Confuse.Height() - 20f), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Confuse.Width(), TextureAssets.Confuse.Height()), rCurrentNPC.GetShimmerColor(new Microsoft.Xna.Framework.Color(250, 250, 250, 70)), rCurrentNPC.velocity.X * -0.05f, new Vector2(TextureAssets.Confuse.Width() / 2, TextureAssets.Confuse.Height() / 2), essScale + 0.2f, SpriteEffects.None, 0f);
25007						}
25008						if (type == 247 || type == 248)
25009						{
25010							Vector2 vector56 = new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY);
25011							Texture2D value55 = TextureAssets.Npc[type].Value;
25012							if (rCurrentNPC.ai[0] == 1f)
25013							{
25014								for (int num163 = 0; num163 < 3; num163++)
25015								{
25016									int num164 = num163 * 5;
25017									int num165 = num164 + 15;
25018									float num166 = Utils.Remap(rCurrentNPC.ai[1], num164, num165, 0f, 1f);
25019									if (num166 != 0f)
25020									{
25021										float num167 = Utils.Remap(num166, 0f, 1f, 2f, 1.1f + 0.1f * (float)num163);
25022										float num168 = num166;
25023										mySpriteBatch.Draw(color: new Microsoft.Xna.Framework.Color(255, 255, 255, 0) * num168, texture: value55, position: vector56, sourceRectangle: frame6, rotation: rCurrentNPC.rotation, origin: halfSize, scale: rCurrentNPC.scale * num167, effects: spriteEffects, layerDepth: 0f);
25024									}
25025								}
25026							}
25027							if (rCurrentNPC.ai[0] == 2f)
25028							{
25029								Microsoft.Xna.Framework.Color color26 = new Microsoft.Xna.Framework.Color(255, 255, 255, 0) * Utils.Remap(rCurrentNPC.ai[1], 0f, 30f, 1f, 0f);
25030								for (int num169 = 0; num169 < 3; num169++)
25031								{
25032									float num170 = 1f;
25033									Vector2 position22 = vector56 + rCurrentNPC.velocity * num169 * -2f;
25034									float num171 = Utils.Remap(num169, 0f, 3f, 1f, 0f);
25035									mySpriteBatch.Draw(value55, position22, frame6, color26 * num171, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale * num170, spriteEffects, 0f);
25036								}
25037								for (int num172 = 0; num172 < 3; num172++)
25038								{
25039									float num173 = 1.1f + 0.1f * (float)num172;
25040									mySpriteBatch.Draw(value55, vector56, frame6, color26, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale * num173, spriteEffects, 0f);
25041								}
25042							}
25043						}
25044						if (type == 24)
25045						{
25046							mySpriteBatch.Draw(TextureAssets.GlowMask[360].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, rCurrentNPC.GetAlpha(Microsoft.Xna.Framework.Color.White), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25047						}
25048						if (type >= 639 && type <= 645)
25049						{
25050							mySpriteBatch.Draw(TextureAssets.GlowMask[286].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, rCurrentNPC.GetAlpha(Microsoft.Xna.Framework.Color.White), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25051						}
25052						if (type >= 646 && type <= 652)
25053						{
25054							mySpriteBatch.Draw(TextureAssets.GlowMask[287].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, rCurrentNPC.GetAlpha(Microsoft.Xna.Framework.Color.White), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25055						}
25056						if (type >= 134 && type <= 136 && npcColor != Microsoft.Xna.Framework.Color.Black)
25057						{
25058							mySpriteBatch.Draw(TextureAssets.Dest[type - 134].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255, 255, 255, 0) * (1f - (float)rCurrentNPC.alpha / 255f), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25059						}
25060						else if (type == 125)
25061						{
25062							mySpriteBatch.Draw(TextureAssets.EyeLaser.Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255, 255, 255, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25063						}
25064						else if (type == 139)
25065						{
25066							mySpriteBatch.Draw(TextureAssets.Probe.Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255, 255, 255, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25067						}
25068						else if (type == 127)
25069						{
25070							if (NPC.IsMechQueenUp)
25071							{
25072								rCurrentNPC.whoAmI = rCurrentNPC.whoAmI;
25073								for (int num174 = 0; num174 < maxNPCs; num174++)
25074								{
25075									if (!npc[num174].active || (npc[num174].type != 125 && npc[num174].type != 126))
25076									{
25077										continue;
25078									}
25079									float scale5 = npc[num174].scale;
25080									float x2 = npc[num174].Center.X;
25081									float y3 = npc[num174].Center.Y;
25082									Vector2 mechQueenCenter = rCurrentNPC.GetMechQueenCenter();
25083									Vector2 vector57 = new Vector2((npc[num174].type == 125) ? (-18) : 20, -18f);
25084									vector57 = vector57.RotatedBy(rCurrentNPC.rotation);
25085									Vector2 vector58 = mechQueenCenter + vector57;
25086									float num175 = x2 - vector58.X;
25087									float num176 = y3 - vector58.Y;
25088									float rotation10 = (float)Math.Atan2(num176, num175) - 1.57f;
25089									bool flag11 = true;
25090									float num177 = (float)Math.Sqrt(num175 * num175 + num176 * num176);
25091									if (num177 > 2000f)
25092									{
25093										flag11 = false;
25094									}
25095									float num178 = 40f * scale5;
25096									while (flag11)
25097									{
25098										num177 = (float)Math.Sqrt(num175 * num175 + num176 * num176);
25099										if (num177 < num178)
25100										{
25101											flag11 = false;
25102											continue;
25103										}
25104										num177 = (float)TextureAssets.Chain12.Height() * scale5 / num177;
25105										num175 *= num177;
25106										num176 *= num177;
25107										Microsoft.Xna.Framework.Color color27 = Lighting.GetColor((int)vector58.X / 16, (int)(vector58.Y / 16f));
25108										spriteBatch.Draw(TextureAssets.Chain12.Value, new Vector2(vector58.X - screenPosition.X, vector58.Y - screenPosition.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Chain12.Width(), TextureAssets.Chain12.Height()), color27, rotation10, new Vector2((float)TextureAssets.Chain12.Width() * 0.5f, 0f), scale5, SpriteEffects.None, 0f);
25109										vector58.X += num175;
25110										vector58.Y += num176;
25111										num175 = x2 - vector58.X;
25112										num176 = y3 - vector58.Y;
25113									}
25114								}
25115							}
25116							else
25117							{
25118								mySpriteBatch.Draw(TextureAssets.BoneEyes.Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(200, 200, 200, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25119							}
25120						}
25121						else if (type == 131)
25122						{
25123							mySpriteBatch.Draw(TextureAssets.BoneLaser.Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(200, 200, 200, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25124						}
25125						else if (type == 120)
25126						{
25127							for (int num179 = 1; num179 < rCurrentNPC.oldPos.Length; num179++)
25128							{
25129								_ = ref rCurrentNPC.oldPos[num179];
25130								Microsoft.Xna.Framework.Color shimmerColor = rCurrentNPC.GetShimmerColor(new Microsoft.Xna.Framework.Color
25131								{
25132									R = (byte)(150 * (10 - num179) / 15),
25133									G = (byte)(100 * (10 - num179) / 15),
25134									B = (byte)(150 * (10 - num179) / 15),
25135									A = (byte)(50 * (10 - num179) / 15)
25136								});
25137								mySpriteBatch.Draw(TextureAssets.Chaos.Value, new Vector2(rCurrentNPC.oldPos[num179].X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.oldPos[num179].Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), rCurrentNPC.frame, shimmerColor, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25138							}
25139						}
25140						else if (type == 137 || type == 138)
25141						{
25142							for (int num180 = 1; num180 < rCurrentNPC.oldPos.Length; num180++)
25143							{
25144								_ = ref rCurrentNPC.oldPos[num180];
25145								Microsoft.Xna.Framework.Color shimmerColor2 = rCurrentNPC.GetShimmerColor(new Microsoft.Xna.Framework.Color
25146								{
25147									R = (byte)(150 * (10 - num180) / 15),
25148									G = (byte)(100 * (10 - num180) / 15),
25149									B = (byte)(150 * (10 - num180) / 15),
25150									A = (byte)(50 * (10 - num180) / 15)
25151								});
25152								mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(rCurrentNPC.oldPos[num180].X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.oldPos[num180].Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), rCurrentNPC.frame, shimmerColor2, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25153							}
25154						}
25155						else if (type == 327)
25156						{
25157							mySpriteBatch.Draw(TextureAssets.PumpkingFace.Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), rCurrentNPC.frame, Microsoft.Xna.Framework.Color.White, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25158							for (int num181 = 1; num181 < 10; num181++)
25159							{
25160								Microsoft.Xna.Framework.Color color28 = new Microsoft.Xna.Framework.Color(110 - num181 * 10, 110 - num181 * 10, 110 - num181 * 10, 110 - num181 * 10);
25161								Vector2 vector59 = new Vector2((float)rand.Next(-10, 11) * 0.2f, (float)rand.Next(-10, 11) * 0.2f);
25162								mySpriteBatch.Draw(TextureAssets.PumpkingFace.Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47) + vector59, rCurrentNPC.frame, color28, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25163							}
25164						}
25165						else if (type == 325)
25166						{
25167							mySpriteBatch.Draw(TextureAssets.TreeFace.Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), rCurrentNPC.frame, Microsoft.Xna.Framework.Color.White, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25168							for (int num182 = 1; num182 < 10; num182++)
25169							{
25170								Microsoft.Xna.Framework.Color color29 = new Microsoft.Xna.Framework.Color(110 - num182 * 10, 110 - num182 * 10, 110 - num182 * 10, 110 - num182 * 10);
25171								Vector2 vector60 = new Vector2((float)rand.Next(-10, 11) * 0.2f, (float)rand.Next(-10, 11) * 0.2f);
25172								mySpriteBatch.Draw(TextureAssets.TreeFace.Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47) + vector60, rCurrentNPC.frame, color29, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25173							}
25174						}
25175						else if (type == 345)
25176						{
25177							mySpriteBatch.Draw(TextureAssets.IceQueen.Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), rCurrentNPC.frame, Microsoft.Xna.Framework.Color.White, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25178							for (int num183 = 1; num183 < 5; num183++)
25179							{
25180								mySpriteBatch.Draw(color: new Microsoft.Xna.Framework.Color(100 - num183 * 10, 100 - num183 * 10, 100 - num183 * 10, 100 - num183 * 10), texture: TextureAssets.IceQueen.Value, position: new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47) - rCurrentNPC.velocity * num183 * 0.2f, sourceRectangle: rCurrentNPC.frame, rotation: rCurrentNPC.rotation, origin: halfSize, scale: rCurrentNPC.scale, effects: spriteEffects, layerDepth: 0f);
25181							}
25182						}
25183						else if (type == 355)
25184						{
25185							mySpriteBatch.Draw(TextureAssets.Firefly.Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255, 255, 255, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25186						}
25187						else if (type == 358)
25188						{
25189							mySpriteBatch.Draw(TextureAssets.Lightningbug.Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255, 255, 255, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25190						}
25191						else if (type == 654)
25192						{
25193							mySpriteBatch.Draw(TextureAssets.GlowMask[290].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255, 255, 255, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25194						}
25195						else if (type == 653)
25196						{
25197							mySpriteBatch.Draw(TextureAssets.GlowMask[288].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 3f + halfSize.Y * rCurrentNPC.scale + num47), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255, 255, 255, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25198						}
25199						else if (type == 82)
25200						{
25201							mySpriteBatch.Draw(TextureAssets.WraithEye.Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), rCurrentNPC.frame, Microsoft.Xna.Framework.Color.White, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25202							for (int num184 = 1; num184 < 10; num184++)
25203							{
25204								mySpriteBatch.Draw(color: new Microsoft.Xna.Framework.Color(110 - num184 * 10, 110 - num184 * 10, 110 - num184 * 10, 110 - num184 * 10), texture: TextureAssets.WraithEye.Value, position: new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47) - rCurrentNPC.velocity * num184 * 0.5f, sourceRectangle: rCurrentNPC.frame, rotation: rCurrentNPC.rotation, origin: halfSize, scale: rCurrentNPC.scale, effects: spriteEffects, layerDepth: 0f);
25205							}
25206						}
25207						else if (type == 253)
25208						{
25209							mySpriteBatch.Draw(TextureAssets.ReaperEye.Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 3f + halfSize.Y * rCurrentNPC.scale + num47), rCurrentNPC.frame, Microsoft.Xna.Framework.Color.White, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25210							for (int num185 = 1; num185 < 20; num185++)
25211							{
25212								mySpriteBatch.Draw(color: new Microsoft.Xna.Framework.Color(210 - num185 * 20, 210 - num185 * 20, 210 - num185 * 20, 210 - num185 * 20), texture: TextureAssets.ReaperEye.Value, position: new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 3f + halfSize.Y * rCurrentNPC.scale + num47) - rCurrentNPC.velocity * num185 * 0.5f, sourceRectangle: rCurrentNPC.frame, rotation: rCurrentNPC.rotation, origin: halfSize, scale: rCurrentNPC.scale, effects: spriteEffects, layerDepth: 0f);
25213							}
25214						}
25215						else if (type == 245 && rCurrentNPC.alpha == 0 && !getGoodWorld)
25216						{
25217							mySpriteBatch.Draw(color: new Microsoft.Xna.Framework.Color(mouseTextColor, mouseTextColor, mouseTextColor, 0), texture: TextureAssets.Golem[3].Value, position: new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), sourceRectangle: frame6, rotation: rCurrentNPC.rotation, origin: halfSize, scale: rCurrentNPC.scale, effects: spriteEffects, layerDepth: 0f);
25218						}
25219						else if (type == 246 && !getGoodWorld)
25220						{
25221							Microsoft.Xna.Framework.Color color30 = new Microsoft.Xna.Framework.Color(mouseTextColor, mouseTextColor, mouseTextColor, 0);
25222							if (rCurrentNPC.frame.Y < 222)
25223							{
25224								if (!getGoodWorld)
25225								{
25226									mySpriteBatch.Draw(TextureAssets.Golem[1].Value, new Vector2(rCurrentNPC.Center.X - screenPos.X - 20f, rCurrentNPC.Center.Y - screenPos.Y - 27f), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Golem[1].Width(), TextureAssets.Golem[1].Height() / 2), color30, 0f, default(Vector2), 1f, SpriteEffects.None, 0f);
25227								}
25228								Microsoft.Xna.Framework.Rectangle value56 = frame6;
25229								value56.Y = 0;
25230								mySpriteBatch.Draw(TextureAssets.Extra[107].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), value56, color30, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25231							}
25232							else if (!getGoodWorld && rCurrentNPC.frame.Y < 444)
25233							{
25234								mySpriteBatch.Draw(TextureAssets.Golem[2].Value, new Vector2(rCurrentNPC.Center.X - screenPos.X + 26f, rCurrentNPC.Center.Y - screenPos.Y - 28f), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Golem[2].Width(), TextureAssets.Golem[2].Height() / 4), color30, 0f, default(Vector2), 1f, SpriteEffects.None, 0f);
25235							}
25236							else if (!getGoodWorld)
25237							{
25238								mySpriteBatch.Draw(TextureAssets.Golem[2].Value, new Vector2(rCurrentNPC.Center.X - screenPos.X - 38f, rCurrentNPC.Center.Y - screenPos.Y - 28f), new Microsoft.Xna.Framework.Rectangle(0, TextureAssets.Golem[2].Height() / 2, TextureAssets.Golem[2].Width(), TextureAssets.Golem[2].Height() / 4), color30, 0f, default(Vector2), 1f, SpriteEffects.None, 0f);
25239							}
25240						}
25241						else if (type == 249 && !getGoodWorld)
25242						{
25243							Microsoft.Xna.Framework.Color color31 = new Microsoft.Xna.Framework.Color(mouseTextColor, mouseTextColor, mouseTextColor, 0);
25244							if (!getGoodWorld)
25245							{
25246								mySpriteBatch.Draw(TextureAssets.Golem[1].Value, new Vector2(rCurrentNPC.Center.X - screenPos.X - 20f, rCurrentNPC.Center.Y - screenPos.Y - 47f), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Golem[1].Width(), TextureAssets.Golem[1].Height() / 2), color31, 0f, default(Vector2), 1f, SpriteEffects.None, 0f);
25247							}
25248							int num186 = (int)rCurrentNPC.frameCounter / 4;
25249							Texture2D value57 = TextureAssets.Extra[106].Value;
25250							Microsoft.Xna.Framework.Rectangle value58 = value57.Frame(1, 8);
25251							_ = Microsoft.Xna.Framework.Color.White;
25252							value58.Y += value58.Height * 2 * num186 + frame6.Y;
25253							mySpriteBatch.Draw(value57, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), value58, color31, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25254							value57 = TextureAssets.Extra[107].Value;
25255							value58 = frame6;
25256							mySpriteBatch.Draw(value57, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), value58, color31, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25257						}
25258						else if (type == 383)
25259						{
25260							mySpriteBatch.Draw(TextureAssets.GlowMask[11].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, new Microsoft.Xna.Framework.Color(255, 255, 255, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25261							if (rCurrentNPC.ai[2] != 0f && npc[(int)rCurrentNPC.ai[2] - 1].active && npc[(int)rCurrentNPC.ai[2] - 1].type == 384)
25262							{
25263								_ = rCurrentNPC.ai[2];
25264								mySpriteBatch.Draw(TextureAssets.Npc[384].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), null, new Microsoft.Xna.Framework.Color(100, 100, 100, 0), rCurrentNPC.rotation, new Vector2(TextureAssets.Npc[384].Width(), TextureAssets.Npc[384].Height()) / 2f, rCurrentNPC.scale, spriteEffects, 0f);
25265							}
25266						}
25267						else if (type == 381)
25268						{
25269							Vector2 zero4 = Vector2.Zero;
25270							Vector2 origin21 = Vector2.Zero;
25271							int num187 = TextureAssets.Npc[type].Height() / npcFrameCount[type];
25272							int num188 = rCurrentNPC.frame.Y / num187;
25273							Microsoft.Xna.Framework.Rectangle value59 = new Microsoft.Xna.Framework.Rectangle(0, 0, 32, 42);
25274							switch (num188)
25275							{
25276							case 0:
25277								zero4 += new Vector2(8f, 32f);
25278								break;
25279							case 1:
25280								zero4 += new Vector2(6f, 72f);
25281								break;
25282							case 2:
25283								zero4 += new Vector2(8f, 126f);
25284								break;
25285							case 3:
25286								zero4 += new Vector2(6f, 174f);
25287								break;
25288							case 4:
25289								zero4 += new Vector2(6f, 224f);
25290								break;
25291							case 5:
25292								zero4 += new Vector2(8f, 272f);
25293								break;
25294							case 6:
25295								zero4 += new Vector2(10f, 318f);
25296								break;
25297							case 7:
25298								zero4 += new Vector2(14f, 366f);
25299								break;
25300							case 8:
25301								zero4 += new Vector2(10f, 414f);
25302								break;
25303							}
25304							zero4.Y -= num187 * num188;
25305							zero4 -= halfSize;
25306							int num189 = 2;
25307							if (rCurrentNPC.ai[2] > 0f)
25308							{
25309								num189 = (int)rCurrentNPC.ai[2] - 1;
25310							}
25311							if (rCurrentNPC.velocity.Y != 0f)
25312							{
25313								num189 = 3;
25314							}
25315							value59.Y += 44 * num189;
25316							switch (num189)
25317							{
25318							case 0:
25319								origin21 = new Vector2(10f, 18f);
25320								break;
25321							case 1:
25322								origin21 = new Vector2(8f, 20f);
25323								break;
25324							case 2:
25325								origin21 = new Vector2(8f, 20f);
25326								break;
25327							case 3:
25328								origin21 = new Vector2(8f, 20f);
25329								break;
25330							case 4:
25331								origin21 = new Vector2(6f, 18f);
25332								break;
25333							}
25334							if ((spriteEffects & SpriteEffects.FlipHorizontally) != SpriteEffects.None)
25335							{
25336								zero4.X *= -1f;
25337								origin21.X = (float)value59.Width - origin21.X;
25338							}
25339							zero4 += rCurrentNPC.Center;
25340							zero4 -= screenPos;
25341							zero4.Y += rCurrentNPC.gfxOffY;
25342							mySpriteBatch.Draw(TextureAssets.Extra[0].Value, zero4, value59, npcColor, rCurrentNPC.rotation, origin21, rCurrentNPC.scale, spriteEffects, 0f);
25343							mySpriteBatch.Draw(TextureAssets.GlowMask[24].Value, zero4, value59, new Microsoft.Xna.Framework.Color(255, 255, 255, 0), rCurrentNPC.rotation, origin21, rCurrentNPC.scale, spriteEffects, 0f);
25344						}
25345						else if (type == 382)
25346						{
25347							Vector2 zero5 = Vector2.Zero;
25348							Vector2 origin22 = Vector2.Zero;
25349							int num190 = TextureAssets.Npc[type].Height() / npcFrameCount[type];
25350							int num191 = rCurrentNPC.frame.Y / num190;
25351							Microsoft.Xna.Framework.Rectangle value60 = new Microsoft.Xna.Framework.Rectangle(0, 0, 30, 42);
25352							switch (num191)
25353							{
25354							case 0:
25355								zero5 += new Vector2(8f, 30f);
25356								break;
25357							case 1:
25358								zero5 += new Vector2(6f, 68f);
25359								break;
25360							case 2:
25361								zero5 += new Vector2(8f, 120f);
25362								break;
25363							case 3:
25364								zero5 += new Vector2(6f, 166f);
25365								break;
25366							case 4:
25367								zero5 += new Vector2(6f, 214f);
25368								break;
25369							case 5:
25370								zero5 += new Vector2(8f, 260f);
25371								break;
25372							case 6:
25373								zero5 += new Vector2(14f, 304f);
25374								break;
25375							case 7:
25376								zero5 += new Vector2(14f, 350f);
25377								break;
25378							case 8:
25379								zero5 += new Vector2(10f, 396f);
25380								break;
25381							}
25382							zero5.Y -= num190 * num191;
25383							zero5 -= halfSize;
25384							int num192 = 2;
25385							if (rCurrentNPC.ai[2] > 0f)
25386							{
25387								num192 = (int)rCurrentNPC.ai[2] - 1;
25388							}
25389							if (rCurrentNPC.velocity.Y != 0f)
25390							{
25391								num192 = 3;
25392							}
25393							value60.Y += 44 * num192;
25394							switch (num192)
25395							{
25396							case 0:
25397								origin22 = new Vector2(10f, 18f);
25398								break;
25399							case 1:
25400								origin22 = new Vector2(8f, 20f);
25401								break;
25402							case 2:
25403								origin22 = new Vector2(8f, 20f);
25404								break;
25405							case 3:
25406								origin22 = new Vector2(8f, 20f);
25407								break;
25408							case 4:
25409								origin22 = new Vector2(6f, 18f);
25410								break;
25411							}
25412							if ((spriteEffects & SpriteEffects.FlipHorizontally) != SpriteEffects.None)
25413							{
25414								zero5.X *= -1f;
25415								origin22.X = (float)value60.Width - origin22.X;
25416							}
25417							zero5 += rCurrentNPC.Center;
25418							zero5 -= screenPos;
25419							zero5.Y += rCurrentNPC.gfxOffY;
25420							mySpriteBatch.Draw(TextureAssets.Extra[1].Value, zero5, value60, npcColor, rCurrentNPC.rotation, origin22, rCurrentNPC.scale, spriteEffects, 0f);
25421						}
25422						else if (type == 520)
25423						{
25424							mySpriteBatch.Draw(TextureAssets.GlowMask[164].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, new Microsoft.Xna.Framework.Color(255, 255, 255, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25425							Vector2 zero6 = Vector2.Zero;
25426							Vector2 origin23 = new Vector2(4f, 4f);
25427							int num193 = TextureAssets.Npc[type].Height() / npcFrameCount[type];
25428							_ = rCurrentNPC.frame.Y / num193;
25429							if ((spriteEffects & SpriteEffects.FlipHorizontally) != SpriteEffects.None)
25430							{
25431								zero6.X *= -1f;
25432								origin23.X = (float)TextureAssets.Extra[56].Width() - origin23.X;
25433							}
25434							zero6 += rCurrentNPC.Top + new Vector2(0f, 20f);
25435							zero6 -= screenPos;
25436							zero6.Y += rCurrentNPC.gfxOffY;
25437							float num194 = rCurrentNPC.localAI[3];
25438							if ((spriteEffects & SpriteEffects.FlipHorizontally) != SpriteEffects.None)
25439							{
25440								num194 += MathF.PI;
25441							}
25442							mySpriteBatch.Draw(TextureAssets.Extra[56].Value, zero6, null, npcColor, num194, origin23, rCurrentNPC.scale, spriteEffects, 0f);
25443							mySpriteBatch.Draw(TextureAssets.GlowMask[165].Value, zero6, null, new Microsoft.Xna.Framework.Color(255, 255, 255, 0), num194, origin23, rCurrentNPC.scale, spriteEffects, 0f);
25444						}
25445						else if (type == 386)
25446						{
25447							mySpriteBatch.Draw(TextureAssets.GlowMask[31].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, new Microsoft.Xna.Framework.Color(255, 255, 255, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25448						}
25449						else if (type == 387)
25450						{
25451							Microsoft.Xna.Framework.Color color32 = new Microsoft.Xna.Framework.Color(1f, 1f, 1f, 1f) * 0.75f;
25452							if (rCurrentNPC.ai[0] > 0f)
25453							{
25454								float amount7 = (rCurrentNPC.ai[0] + 1f) / 60f;
25455								color32 = Microsoft.Xna.Framework.Color.Lerp(color32, Microsoft.Xna.Framework.Color.White, amount7);
25456								color32.A = (byte)MathHelper.Lerp((int)color32.A, 0f, amount7);
25457							}
25458							color32 *= (255f - (float)rCurrentNPC.alpha) / 255f;
25459							mySpriteBatch.Draw(TextureAssets.GlowMask[32].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, color32, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25460						}
25461						else if (type == 388)
25462						{
25463							mySpriteBatch.Draw(TextureAssets.GlowMask[33].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, new Microsoft.Xna.Framework.Color(255, 255, 255, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25464						}
25465						else if (type == 389)
25466						{
25467							mySpriteBatch.Draw(TextureAssets.GlowMask[34].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, new Microsoft.Xna.Framework.Color(255, 255, 255, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25468						}
25469						else if (type == 4 && rCurrentNPC.ai[1] >= 4f && rCurrentNPC.ai[0] == 3f)
25470						{
25471							for (int num195 = 1; num195 < rCurrentNPC.oldPos.Length; num195++)
25472							{
25473								_ = ref rCurrentNPC.oldPos[num195];
25474								Microsoft.Xna.Framework.Color color33 = npcColor;
25475								color33.R = (byte)(0.5 * (double)(int)color33.R * (double)(10 - num195) / 20.0);
25476								color33.G = (byte)(0.5 * (double)(int)color33.G * (double)(10 - num195) / 20.0);
25477								color33.B = (byte)(0.5 * (double)(int)color33.B * (double)(10 - num195) / 20.0);
25478								color33.A = (byte)(0.5 * (double)(int)color33.A * (double)(10 - num195) / 20.0);
25479								mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(rCurrentNPC.oldPos[num195].X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.oldPos[num195].Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), rCurrentNPC.frame, color33, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25480							}
25481						}
25482						else if (type == 437)
25483						{
25484							Microsoft.Xna.Framework.Color white5 = Microsoft.Xna.Framework.Color.White;
25485							white5.A = 200;
25486							mySpriteBatch.Draw(TextureAssets.GlowMask[109].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), frame6, white5, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25487							mySpriteBatch.Draw(TextureAssets.GlowMask[108].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + num46 + rCurrentNPC.gfxOffY), null, white5, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25488						}
25489						else if (type == 471 && rCurrentNPC.ai[3] < 0f)
25490						{
25491							for (int num196 = 1; num196 < rCurrentNPC.oldPos.Length; num196++)
25492							{
25493								_ = ref rCurrentNPC.oldPos[num196];
25494								Microsoft.Xna.Framework.Color color34 = npcColor;
25495								color34.R = (byte)(0.5 * (double)(int)color34.R * (double)(10 - num196) / 20.0);
25496								color34.G = (byte)(0.5 * (double)(int)color34.G * (double)(10 - num196) / 20.0);
25497								color34.B = (byte)(0.5 * (double)(int)color34.B * (double)(10 - num196) / 20.0);
25498								color34.A = (byte)(0.5 * (double)(int)color34.A * (double)(10 - num196) / 20.0);
25499								mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(rCurrentNPC.oldPos[num196].X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.oldPos[num196].Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), rCurrentNPC.frame, color34, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25500							}
25501						}
25502						else if (type == 477 && rCurrentNPC.velocity.Length() > 9f)
25503						{
25504							for (int num197 = 1; num197 < rCurrentNPC.oldPos.Length; num197++)
25505							{
25506								_ = ref rCurrentNPC.oldPos[num197];
25507								Microsoft.Xna.Framework.Color color35 = npcColor;
25508								color35.R = (byte)(0.5 * (double)(int)color35.R * (double)(10 - num197) / 20.0);
25509								color35.G = (byte)(0.5 * (double)(int)color35.G * (double)(10 - num197) / 20.0);
25510								color35.B = (byte)(0.5 * (double)(int)color35.B * (double)(10 - num197) / 20.0);
25511								color35.A = (byte)(0.5 * (double)(int)color35.A * (double)(10 - num197) / 20.0);
25512								Microsoft.Xna.Framework.Rectangle frame7 = rCurrentNPC.frame;
25513								int num198 = TextureAssets.Npc[type].Height() / npcFrameCount[type];
25514								frame7.Y -= num198 * num197;
25515								while (frame7.Y < 0)
25516								{
25517									frame7.Y += num198 * npcFrameCount[type];
25518								}
25519								mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(rCurrentNPC.oldPos[num197].X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.oldPos[num197].Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), frame7, color35, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25520							}
25521						}
25522						if (type == 479 && (double)rCurrentNPC.velocity.Length() > 6.5)
25523						{
25524							for (int num199 = 1; num199 < rCurrentNPC.oldPos.Length; num199++)
25525							{
25526								_ = ref rCurrentNPC.oldPos[num199];
25527								Microsoft.Xna.Framework.Color color36 = npcColor;
25528								color36.R = (byte)(0.5 * (double)(int)color36.R * (double)(10 - num199) / 20.0);
25529								color36.G = (byte)(0.5 * (double)(int)color36.G * (double)(10 - num199) / 20.0);
25530								color36.B = (byte)(0.5 * (double)(int)color36.B * (double)(10 - num199) / 20.0);
25531								color36.A = (byte)(0.5 * (double)(int)color36.A * (double)(10 - num199) / 20.0);
25532								Microsoft.Xna.Framework.Rectangle frame8 = rCurrentNPC.frame;
25533								int num200 = TextureAssets.Npc[type].Height() / npcFrameCount[type];
25534								frame8.Y -= num200 * num199;
25535								while (frame8.Y < 0)
25536								{
25537									frame8.Y += num200 * npcFrameCount[type];
25538								}
25539								mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(rCurrentNPC.oldPos[num199].X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.oldPos[num199].Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), frame8, color36, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25540							}
25541						}
25542						else if (type == 472)
25543						{
25544							mySpriteBatch.Draw(TextureAssets.GlowMask[110].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25545						}
25546						else if (rCurrentNPC.aiStyle == 87)
25547						{
25548							if ((int)rCurrentNPC.ai[0] == 4 || rCurrentNPC.ai[0] == 5f || rCurrentNPC.ai[0] == 6f)
25549							{
25550								for (int num201 = 1; num201 < rCurrentNPC.oldPos.Length; num201++)
25551								{
25552									_ = ref rCurrentNPC.oldPos[num201];
25553									Microsoft.Xna.Framework.Color newColor4 = npcColor;
25554									newColor4.R = (byte)(0.5 * (double)(int)newColor4.R * (double)(10 - num201) / 20.0);
25555									newColor4.G = (byte)(0.5 * (double)(int)newColor4.G * (double)(10 - num201) / 20.0);
25556									newColor4.B = (byte)(0.5 * (double)(int)newColor4.B * (double)(10 - num201) / 20.0);
25557									newColor4.A = (byte)(0.5 * (double)(int)newColor4.A * (double)(10 - num201) / 20.0);
25558									newColor4 = rCurrentNPC.GetShimmerColor(newColor4);
25559									mySpriteBatch.Draw(TextureAssets.Npc[type].Value, new Vector2(rCurrentNPC.oldPos[num201].X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[type].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.oldPos[num201].Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[type].Height() * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47), rCurrentNPC.frame, newColor4, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25560								}
25561							}
25562						}
25563						else
25564						{
25565							switch (type)
25566							{
25567							case 50:
25568							{
25569								Texture2D value61 = TextureAssets.Extra[39].Value;
25570								Vector2 center4 = rCurrentNPC.Center;
25571								float num223 = 0f;
25572								switch (rCurrentNPC.frame.Y / (TextureAssets.Npc[type].Height() / npcFrameCount[type]))
25573								{
25574								case 0:
25575									num223 = 2f;
25576									break;
25577								case 1:
25578									num223 = -6f;
25579									break;
25580								case 2:
25581									num223 = 2f;
25582									break;
25583								case 3:
25584									num223 = 10f;
25585									break;
25586								case 4:
25587									num223 = 2f;
25588									break;
25589								case 5:
25590									num223 = 0f;
25591									break;
25592								}
25593								center4.Y += rCurrentNPC.gfxOffY - (70f - num223) * rCurrentNPC.scale;
25594								mySpriteBatch.Draw(value61, center4 - screenPos, null, npcColor, 0f, value61.Size() / 2f, 1f, spriteEffects, 0f);
25595								break;
25596							}
25597							case 411:
25598								mySpriteBatch.Draw(TextureAssets.GlowMask[136].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25599								break;
25600							case 409:
25601								mySpriteBatch.Draw(TextureAssets.GlowMask[138].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25602								break;
25603							case 410:
25604								mySpriteBatch.Draw(TextureAssets.GlowMask[137].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25605								break;

```


---

## 🤖 Assistant · 2026-08-11T07:14:24.327Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Continuing. Read 25605-26400.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:14:24.521Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "limit": 820,
 "offset": 25605
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:24.848Z

**📎 ToolResult**

```
25605								break;
25606							case 407:
25607								mySpriteBatch.Draw(TextureAssets.GlowMask[139].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25608								break;
25609							case 405:
25610								mySpriteBatch.Draw(TextureAssets.GlowMask[141].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25611								break;
25612							case 406:
25613								mySpriteBatch.Draw(TextureAssets.GlowMask[142].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25614								break;
25615							case 424:
25616								mySpriteBatch.Draw(TextureAssets.GlowMask[144].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25617								break;
25618							case 423:
25619								mySpriteBatch.Draw(TextureAssets.GlowMask[145].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25620								break;
25621							case 421:
25622								mySpriteBatch.Draw(TextureAssets.GlowMask[146].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25623								break;
25624							case 420:
25625								mySpriteBatch.Draw(TextureAssets.GlowMask[147].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25626								break;
25627							case 425:
25628							{
25629								Vector2 vector62 = rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY);
25630								mySpriteBatch.Draw(TextureAssets.GlowMask[150].Value, vector62, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25631								Vector2 drawpos = vector62 + new Vector2(27 * -rCurrentNPC.spriteDirection, 0f);
25632								float num224 = rCurrentNPC.ai[3];
25633								DrawPrettyStarSparkle(Utils.Remap(num224, 0f, 15f, 0f, 1f), SpriteEffects.None, drawpos, new Microsoft.Xna.Framework.Color(255, 255, 255, 0), Microsoft.Xna.Framework.Color.Green, num224, 0f, 30f, 30f, 36f, 0f, new Vector2(3f, 1.5f), new Vector2(2f, 2f));
25634								break;
25635							}
25636							case 429:
25637								mySpriteBatch.Draw(TextureAssets.GlowMask[151].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25638								break;
25639							case 418:
25640							{
25641								mySpriteBatch.Draw(TextureAssets.GlowMask[161].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25642								float num221 = 0.25f + (rCurrentNPC.GetAlpha(npcColor).ToVector3() - new Vector3(0.5f)).Length() * 0.25f;
25643								for (int num222 = 0; num222 < 4; num222++)
25644								{
25645									mySpriteBatch.Draw(TextureAssets.GlowMask[161].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY) + rCurrentNPC.velocity.RotatedBy((float)num222 * (MathF.PI / 2f)) * num221, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(64, 64, 64, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25646								}
25647								break;
25648							}
25649							case 412:
25650							case 413:
25651							case 414:
25652							{
25653								Microsoft.Xna.Framework.Color color38 = new Microsoft.Xna.Framework.Color(255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 0);
25654								int num218 = 157 + type - 412;
25655								if (type == 414 && rCurrentNPC.localAI[2] != 0f)
25656								{
25657									int num219 = (int)rCurrentNPC.localAI[2];
25658									if (rCurrentNPC.localAI[2] < 0f)
25659									{
25660										num219 = 128 + (int)rCurrentNPC.localAI[2];
25661									}
25662									int num220 = 255 - num219;
25663									color38 = new Microsoft.Xna.Framework.Color(num220, num219, num219, num220);
25664								}
25665								mySpriteBatch.Draw(TextureAssets.GlowMask[num218].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, color38, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25666								break;
25667							}
25668							default:
25669								switch (type)
25670								{
25671								case 415:
25672								{
25673									mySpriteBatch.Draw(TextureAssets.GlowMask[155].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25674									float num202 = 0.5f + (rCurrentNPC.GetAlpha(npcColor).ToVector3() - new Vector3(0.5f)).Length() * 0.5f;
25675									for (int num203 = 0; num203 < 4; num203++)
25676									{
25677										mySpriteBatch.Draw(TextureAssets.GlowMask[155].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY) + rCurrentNPC.velocity.RotatedBy((float)num203 * (MathF.PI / 2f)) * num202, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(64, 64, 64, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25678									}
25679									break;
25680								}
25681								case 419:
25682									mySpriteBatch.Draw(TextureAssets.GlowMask[154].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25683									if (rCurrentNPC.ai[2] >= -6f)
25684									{
25685										float num208 = 0.5f + (rCurrentNPC.GetAlpha(npcColor).ToVector3() - new Vector3(0.5f)).Length() * 0.5f;
25686										for (int num209 = 0; num209 < 4; num209++)
25687										{
25688											mySpriteBatch.Draw(TextureAssets.GlowMask[154].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY) + rCurrentNPC.velocity.RotatedBy((float)num209 * (MathF.PI / 2f)) * num208, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(64, 64, 64, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25689										}
25690									}
25691									else
25692									{
25693										float num210 = 4f;
25694										for (int num211 = 0; num211 < 4; num211++)
25695										{
25696											mySpriteBatch.Draw(TextureAssets.GlowMask[154].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY) + Vector2.UnitX.RotatedBy((float)num211 * (MathF.PI / 2f)) * num210, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(64, 64, 64, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25697										}
25698									}
25699									break;
25700								case 417:
25701								{
25702									mySpriteBatch.Draw(TextureAssets.GlowMask[160].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25703									float num212 = 0.25f + (rCurrentNPC.GetAlpha(npcColor).ToVector3() - new Vector3(0.5f)).Length() * 0.25f;
25704									for (int num213 = 0; num213 < 4; num213++)
25705									{
25706										mySpriteBatch.Draw(TextureAssets.GlowMask[160].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY) + rCurrentNPC.velocity.RotatedBy((float)num213 * (MathF.PI / 2f)) * num212, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(64, 64, 64, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25707									}
25708									break;
25709								}
25710								case 516:
25711								{
25712									mySpriteBatch.Draw(TextureAssets.Npc[type].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25713									float num204 = 0.5f + (rCurrentNPC.GetAlpha(npcColor).ToVector3() - new Vector3(0.5f)).Length() * 0.5f;
25714									for (int num205 = 0; num205 < 4; num205++)
25715									{
25716										mySpriteBatch.Draw(TextureAssets.Npc[type].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY) + rCurrentNPC.velocity.RotatedBy((float)num205 * (MathF.PI / 2f)) * num204, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(64, 64, 64, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25717									}
25718									break;
25719								}
25720								case 518:
25721								{
25722									Vector2 vector61 = new Vector2(-10f, 0f);
25723									mySpriteBatch.Draw(TextureAssets.GlowMask[163].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha), rCurrentNPC.rotation, halfSize + vector61, rCurrentNPC.scale, spriteEffects, 0f);
25724									float num216 = 0.5f + (rCurrentNPC.GetAlpha(npcColor).ToVector3() - new Vector3(0.5f)).Length() * 0.5f;
25725									for (int num217 = 0; num217 < 4; num217++)
25726									{
25727										mySpriteBatch.Draw(TextureAssets.GlowMask[163].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY) + rCurrentNPC.velocity.RotatedBy((float)num217 * (MathF.PI / 2f)) * num216, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(64, 64, 64, 0), rCurrentNPC.rotation, halfSize + vector61, rCurrentNPC.scale, spriteEffects, 0f);
25728									}
25729									break;
25730								}
25731								case 344:
25732									mySpriteBatch.Draw(TextureAssets.GlowMask[253].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(200, 200, 200, 100) * 0.5f, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25733									break;
25734								case 346:
25735								{
25736									float num214 = 4f;
25737									for (int num215 = 0; num215 < 4; num215++)
25738									{
25739										mySpriteBatch.Draw(TextureAssets.GlowMask[254].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY) + Vector2.UnitX.RotatedBy((float)num215 * (MathF.PI / 2f)) * num214, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(64, 64, 64, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25740									}
25741									mySpriteBatch.Draw(TextureAssets.GlowMask[254].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(200, 200, 200, 100), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25742									break;
25743								}
25744								case 315:
25745								{
25746									float num206 = 2f;
25747									for (int num207 = 0; num207 < 4; num207++)
25748									{
25749										mySpriteBatch.Draw(TextureAssets.GlowMask[255].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY) + Vector2.UnitX.RotatedBy((float)num207 * (MathF.PI / 2f)) * num206, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(64, 64, 64, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25750									}
25751									mySpriteBatch.Draw(TextureAssets.GlowMask[255].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(200, 200, 200, 200), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25752									break;
25753								}
25754								case 525:
25755									mySpriteBatch.Draw(TextureAssets.GlowMask[169].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(200, 200, 200, 100), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25756									break;
25757								case 526:
25758									mySpriteBatch.Draw(TextureAssets.GlowMask[170].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(200, 200, 200, 100), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25759									break;
25760								case 527:
25761									mySpriteBatch.Draw(TextureAssets.GlowMask[171].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(200, 200, 200, 100), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25762									break;
25763								case 533:
25764									mySpriteBatch.Draw(TextureAssets.GlowMask[172].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255, 255, 255, 100), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25765									break;
25766								case 160:
25767								{
25768									Texture2D texture2D2 = null;
25769									texture2D2 = ((rCurrentNPC.townNpcVariationIndex != 1) ? TextureAssets.GlowMask[166].Value : TextureAssets.GlowMask[352].Value);
25770									Microsoft.Xna.Framework.Color color37 = new Microsoft.Xna.Framework.Color(128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 0);
25771									if (rCurrentNPC.shimmerTransparency > 0f)
25772									{
25773										color37.R = (byte)((float)(int)color37.R * (1f - rCurrentNPC.shimmerTransparency));
25774										color37.G = (byte)((float)(int)color37.G * (1f - rCurrentNPC.shimmerTransparency));
25775										color37.B = (byte)((float)(int)color37.B * (1f - rCurrentNPC.shimmerTransparency));
25776									}
25777									mySpriteBatch.Draw(texture2D2, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, color37, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25778									break;
25779								}
25780								case 209:
25781								{
25782									Texture2D texture2D = null;
25783									texture2D = ((rCurrentNPC.townNpcVariationIndex != 1) ? TextureAssets.GlowMask[167].Value : ((rCurrentNPC.altTexture != 1) ? TextureAssets.GlowMask[350].Value : TextureAssets.GlowMask[351].Value));
25784									mySpriteBatch.Draw(texture2D, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
25785									break;
25786								}
25787								}
25788								break;
25789							}
25790						}
25791						if (rCurrentNPC.aiStyle == 7)
25792						{
25793							DrawNPCExtras(rCurrentNPC, beforeDraw: false, num47, num46, npcColor, halfSize, spriteEffects, screenPos);
25794						}
25795						break;
25796					}
25797					case 488:
25798						break;
25799					}
25800					break;
25801				}
25802				goto case 426;
25803			case 426:
25804			case 427:
25805			case 428:
25806			case 521:
25807			case 523:
25808			case 541:
25809			case 542:
25810			case 543:
25811			case 544:
25812			case 545:
25813			case 581:
25814			{
25815				Texture2D value80 = TextureAssets.Npc[type].Value;
25816				Microsoft.Xna.Framework.Color color43 = Microsoft.Xna.Framework.Color.White;
25817				float amount10 = 0f;
25818				float amount11 = 0f;
25819				int num294 = 0;
25820				int num295 = 0;
25821				int num296 = 1;
25822				int num297 = 15;
25823				int num298 = 0;
25824				float scale8 = rCurrentNPC.scale;
25825				float value81 = rCurrentNPC.scale;
25826				int num299 = 0;
25827				float num300 = 0f;
25828				float num301 = 0f;
25829				float num302 = 0f;
25830				Microsoft.Xna.Framework.Color color44 = npcColor;
25831				Vector2 origin25 = halfSize;
25832				switch (type)
25833				{
25834				case 558:
25835				case 559:
25836				case 560:
25837				case 574:
25838				case 575:
25839					if (rCurrentNPC.ai[0] != 2f)
25840					{
25841						num294 = 0;
25842						break;
25843					}
25844					num294 = 6;
25845					num295 = 2;
25846					num297 = num294 * 3;
25847					num298 = 1;
25848					break;
25849				case 566:
25850				case 567:
25851				case 578:
25852					num294 = 0;
25853					num47 = -2f;
25854					break;
25855				case 552:
25856				case 553:
25857				case 554:
25858				case 555:
25859				case 556:
25860				case 557:
25861				case 561:
25862				case 562:
25863				case 563:
25864				case 568:
25865				case 569:
25866				case 570:
25867				case 571:
25868				case 572:
25869				case 573:
25870					num294 = 0;
25871					if (type == 561 || type == 562 || type == 563)
25872					{
25873						num47 = -8f;
25874					}
25875					if (type == 555 || type == 556 || type == 557)
25876					{
25877						num47 = -5f;
25878					}
25879					if (type == 572 || type == 573)
25880					{
25881						num47 = -4f;
25882					}
25883					if (type == 570 || type == 571)
25884					{
25885						spriteEffects ^= SpriteEffects.FlipHorizontally;
25886						num47 = -2f;
25887					}
25888					if (type == 568 || type == 569)
25889					{
25890						spriteEffects ^= SpriteEffects.FlipHorizontally;
25891						num47 = -3f;
25892						num299 = 4;
25893						num301 = 4f;
25894						num300 = (float)Math.Cos(GlobalTimeWrappedHourly % 1.5f / 1.5f * (MathF.PI * 2f)) / 6f + 0.75f;
25895						color43 = Microsoft.Xna.Framework.Color.HotPink;
25896						color43.A = 127;
25897						amount10 = 0.5f;
25898					}
25899					if (rCurrentNPC.localAI[3] < 60f)
25900					{
25901						float num315 = rCurrentNPC.localAI[3] / 60f;
25902						num299 = 3;
25903						num300 = 1f - num315 * num315;
25904						num301 = 8f;
25905						color43 = new Microsoft.Xna.Framework.Color(127, 0, 255, 0);
25906						amount11 = 1f;
25907						color44 = Microsoft.Xna.Framework.Color.Lerp(Microsoft.Xna.Framework.Color.Transparent, color44, num315 * num315);
25908					}
25909					break;
25910				case 541:
25911					num299 = 4;
25912					num301 = 6f;
25913					num300 = (float)Math.Cos(GlobalTimeWrappedHourly % 2.4f / 2.4f * (MathF.PI * 2f)) / 2f + 0.5f;
25914					color43 = Microsoft.Xna.Framework.Color.Gold;
25915					amount10 = 0.5f;
25916					break;
25917				case 661:
25918					num299 = 6;
25919					num301 = 6f;
25920					num300 = (float)Math.Cos(GlobalTimeWrappedHourly % 2.4f / 2.4f * (MathF.PI * 2f)) / 2f + 0.5f;
25921					num300 = MathHelper.Max(num300, Utils.GetLerpValue(0f, 60f, rCurrentNPC.ai[2], clamped: true));
25922					amount10 = 0.5f;
25923					break;
25924				case 426:
25925					num299 = 4;
25926					num301 = 4f;
25927					num300 = (float)Math.Cos(GlobalTimeWrappedHourly % 1.2f / 1.2f * (MathF.PI * 2f)) / 2f + 0.5f;
25928					color43 = Microsoft.Xna.Framework.Color.Turquoise;
25929					amount10 = 0.5f;
25930					num294 = 6;
25931					num295 = 2;
25932					num297 = num294;
25933					break;
25934				case 427:
25935					num294 = 8;
25936					num295 = 2;
25937					num297 = num294 * 3;
25938					break;
25939				case 546:
25940					num294 = 8;
25941					num295 = 2;
25942					num297 = num294 * 3;
25943					break;
25944				case 542:
25945				case 543:
25946				case 544:
25947				case 545:
25948					num294 = 6;
25949					num295 = 3;
25950					num297 = num294 * 2;
25951					break;
25952				case 581:
25953					num294 = 6;
25954					num295 = 2;
25955					num297 = num294 * 3;
25956					break;
25957				case 521:
25958					num294 = 10;
25959					num295 = 2;
25960					num297 = num294;
25961					num298 = 1;
25962					value81 = 0.3f;
25963					break;
25964				case 523:
25965					num299 = 3;
25966					num301 = 10f * rCurrentNPC.scale;
25967					amount10 = 0.5f;
25968					amount11 = 0.8f;
25969					color43 = Microsoft.Xna.Framework.Color.HotPink;
25970					color43.A = 128;
25971					num302 = rCurrentNPC.localAI[0];
25972					num300 = rCurrentNPC.localAI[1];
25973					break;
25974				case 620:
25975					num47 = -9f;
25976					origin25 = rCurrentNPC.frame.Size() * new Vector2(0.5f, 0.5f) + new Vector2(-4 * rCurrentNPC.spriteDirection, 0f);
25977					num299 = 4;
25978					num301 = 6f;
25979					num300 = (float)Math.Cos(GlobalTimeWrappedHourly % 2.4f / 2.4f * (MathF.PI * 2f)) / 2f + 0.5f;
25980					color43 = Microsoft.Xna.Framework.Color.Gold;
25981					amount10 = 0.5f;
25982					num294 = 6;
25983					num295 = 2;
25984					num297 = num294 * 3;
25985					num298 = 1;
25986					break;
25987				case 618:
25988				{
25989					float num303 = 90f;
25990					float num304 = 180f;
25991					if (rCurrentNPC.ai[0] == 1f && rCurrentNPC.ai[1] < num303)
25992					{
25993						int num305 = 3;
25994						float num306 = num303 / (float)num305;
25995						float num307 = rCurrentNPC.ai[1] % num306 / num306;
25996						num299 = 6;
25997						num301 = 15f;
25998						num300 = num307 * 0.8f + 0.2f;
25999					}
26000					if (rCurrentNPC.ai[0] == 3f && rCurrentNPC.ai[1] < num304)
26001					{
26002						int num308 = 1;
26003						float num309 = num304 / (float)num308;
26004						float num310 = rCurrentNPC.ai[1] % num309 / num309;
26005						num299 = 4;
26006						num301 = 25f;
26007						num300 = num310;
26008						Vector2 vector71 = rCurrentNPC.scale * new Vector2(1f, 0.5f + num310 * 0.75f);
26009						Texture2D value82 = TextureAssets.Extra[59].Value;
26010						Microsoft.Xna.Framework.Rectangle rectangle13 = value82.Frame();
26011						Vector2 origin26 = rectangle13.Size() * new Vector2(0.5f, 0.5f);
26012						for (int num311 = 0; num311 < num299; num311++)
26013						{
26014							Microsoft.Xna.Framework.Color white8 = Microsoft.Xna.Framework.Color.White;
26015							white8 *= Utils.GetLerpValue(0f, 0.5f, num300) * Utils.GetLerpValue(1f, 0.5f, num300) * 0.25f;
26016							white8.A = 0;
26017							white8.G = 0;
26018							white8.B = 0;
26019							float num312 = (float)num311 / (float)num299 * (MathF.PI * 2f) + rCurrentNPC.rotation + num302;
26020							Vector2 position32 = rCurrentNPC.Center + num312.ToRotationVector2() * num301 * num300 - screenPos;
26021							position32 -= new Vector2(value80.Width, value80.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
26022							position32 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
26023							mySpriteBatch.Draw(value82, position32, rectangle13, white8, num312, origin26, vector71 * 1.8f, spriteEffects, 0f);
26024						}
26025						for (int num313 = 0; num313 < num299; num313++)
26026						{
26027							Microsoft.Xna.Framework.Color white9 = Microsoft.Xna.Framework.Color.White;
26028							white9 *= Utils.GetLerpValue(0f, 0.5f, num300) * Utils.GetLerpValue(1f, 0.5f, num300) * 0.25f;
26029							white9.A = 0;
26030							float num314 = (float)num313 / (float)num299 * (MathF.PI * 2f) + rCurrentNPC.rotation + num302;
26031							Vector2 position33 = rCurrentNPC.Center + num314.ToRotationVector2() * num301 * num300 - screenPos;
26032							position33 -= new Vector2(value80.Width, value80.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
26033							position33 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
26034							mySpriteBatch.Draw(value82, position33, rectangle13, white9, num314, origin26, vector71 * 1.5f, spriteEffects, 0f);
26035						}
26036					}
26037					break;
26038				}
26039				}
26040				for (int num316 = num296; num316 < num294; num316 += num295)
26041				{
26042					_ = ref rCurrentNPC.oldPos[num316];
26043					Microsoft.Xna.Framework.Color value83 = color44;
26044					value83 = Microsoft.Xna.Framework.Color.Lerp(value83, color43, amount10);
26045					value83 = rCurrentNPC.GetAlpha(value83);
26046					value83 *= (float)(num294 - num316) / (float)num297;
26047					_ = rCurrentNPC.rotation;
26048					if (num298 == 1)
26049					{
26050						_ = rCurrentNPC.oldRot[num316];
26051					}
26052					float scale9 = MathHelper.Lerp(scale8, value81, 1f - (float)(num294 - num316) / (float)num297);
26053					Vector2 position34 = rCurrentNPC.oldPos[num316] + new Vector2(rCurrentNPC.width, rCurrentNPC.height) / 2f - screenPos;
26054					position34 -= new Vector2(value80.Width, value80.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
26055					position34 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
26056					mySpriteBatch.Draw(value80, position34, rCurrentNPC.frame, value83, rCurrentNPC.rotation, halfSize, scale9, spriteEffects, 0f);
26057				}
26058				for (int num317 = 0; num317 < num299; num317++)
26059				{
26060					Microsoft.Xna.Framework.Color value84 = npcColor;
26061					value84 = Microsoft.Xna.Framework.Color.Lerp(value84, color43, amount10);
26062					value84 = rCurrentNPC.GetAlpha(value84);
26063					value84 = Microsoft.Xna.Framework.Color.Lerp(value84, color43, amount11);
26064					value84 *= 1f - num300;
26065					Vector2 position35 = rCurrentNPC.Center + ((float)num317 / (float)num299 * (MathF.PI * 2f) + rCurrentNPC.rotation + num302).ToRotationVector2() * num301 * num300 - screenPos;
26066					position35 -= new Vector2(value80.Width, value80.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
26067					position35 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
26068					mySpriteBatch.Draw(value80, position35, rCurrentNPC.frame, value84, rCurrentNPC.rotation, origin25, rCurrentNPC.scale, spriteEffects, 0f);
26069				}
26070				Vector2 vector72 = rCurrentNPC.Center - screenPos;
26071				vector72 -= new Vector2(value80.Width, value80.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
26072				vector72 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
26073				mySpriteBatch.Draw(value80, vector72, rCurrentNPC.frame, rCurrentNPC.GetAlpha(color44), rCurrentNPC.rotation, origin25, rCurrentNPC.scale, spriteEffects, 0f);
26074				switch (type)
26075				{
26076				case 427:
26077					mySpriteBatch.Draw(TextureAssets.GlowMask[152].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 255 - rCurrentNPC.alpha, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
26078					break;
26079				case 426:
26080					mySpriteBatch.Draw(TextureAssets.GlowMask[153].Value, rCurrentNPC.Bottom - screenPos + new Vector2((float)(-TextureAssets.Npc[type].Width()) * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, (float)(-TextureAssets.Npc[type].Height()) * rCurrentNPC.scale / (float)npcFrameCount[type] + 4f + halfSize.Y * rCurrentNPC.scale + num47 + rCurrentNPC.gfxOffY), rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 128 - rCurrentNPC.alpha / 2, 0), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
26081					break;
26082				}
26083				if (type == 541)
26084				{
26085					Microsoft.Xna.Framework.Color color45 = new Microsoft.Xna.Framework.Color(127 - rCurrentNPC.alpha, 127 - rCurrentNPC.alpha, 127 - rCurrentNPC.alpha, 0).MultiplyRGBA(Microsoft.Xna.Framework.Color.Gold);
26086					for (int num318 = 0; num318 < num299; num318++)
26087					{
26088						Microsoft.Xna.Framework.Color newColor5 = color45;
26089						newColor5 = rCurrentNPC.GetAlpha(newColor5);
26090						newColor5 *= 1f - num300;
26091						Vector2 position36 = rCurrentNPC.Center + ((float)num318 / (float)num299 * (MathF.PI * 2f) + rCurrentNPC.rotation + num302).ToRotationVector2() * (4f * num300 + 2f) - screenPos;
26092						position36 -= new Vector2(value80.Width, value80.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
26093						position36 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
26094						mySpriteBatch.Draw(TextureAssets.GlowMask[216].Value, position36, rCurrentNPC.frame, newColor5, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
26095					}
26096					mySpriteBatch.Draw(TextureAssets.GlowMask[216].Value, vector72, rCurrentNPC.frame, color45, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
26097				}
26098				if (type == 661)
26099				{
26100					num302 = MathHelper.Lerp(0f, 3f, Utils.GetLerpValue(0f, 60f, rCurrentNPC.ai[2], clamped: true));
26101					for (int num319 = 0; num319 < num299; num319++)
26102					{
26103						Microsoft.Xna.Framework.Color newColor6 = new Microsoft.Xna.Framework.Color(127 - rCurrentNPC.alpha, 127 - rCurrentNPC.alpha, 127 - rCurrentNPC.alpha, 0).MultiplyRGBA(hslToRgb((GlobalTimeWrappedHourly + (float)num319 / (float)num299) % 1f, 1f, 0.5f));
26104						newColor6 = rCurrentNPC.GetAlpha(newColor6);
26105						newColor6 *= 1f - num300 * 0.5f;
26106						newColor6.A = 0;
26107						float num320 = 2f + rCurrentNPC.ai[2];
26108						Vector2 position37 = rCurrentNPC.Center + ((float)num319 / (float)num299 * (MathF.PI * 2f) + rCurrentNPC.rotation + num302).ToRotationVector2() * (num320 * num300 + 2f) - screenPos;
26109						position37 -= new Vector2(value80.Width, value80.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
26110						position37 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
26111						mySpriteBatch.Draw(value80, position37, rCurrentNPC.frame, newColor6, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
26112					}
26113					mySpriteBatch.Draw(value80, vector72, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255, 255, 255, 0) * 0.1f, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
26114				}
26115				if ((type == 568 || type == 569) && rCurrentNPC.localAI[3] >= 60f)
26116				{
26117					Microsoft.Xna.Framework.Color color46 = new Microsoft.Xna.Framework.Color(127 - rCurrentNPC.alpha, 127 - rCurrentNPC.alpha, 127 - rCurrentNPC.alpha, 0).MultiplyRGBA(color43);
26118					for (int num321 = 0; num321 < num299; num321++)
26119					{
26120						Microsoft.Xna.Framework.Color newColor7 = color46;
26121						newColor7 = rCurrentNPC.GetAlpha(newColor7);
26122						newColor7 *= 1f - num300;
26123						Vector2 position38 = rCurrentNPC.Center + ((float)num321 / (float)num299 * (MathF.PI * 2f) + rCurrentNPC.rotation + num302).ToRotationVector2() * (4f * num300 + 2f) - screenPos;
26124						position38 -= new Vector2(value80.Width, value80.Height / npcFrameCount[type]) * rCurrentNPC.scale / 2f;
26125						position38 += halfSize * rCurrentNPC.scale + new Vector2(0f, num46 + num47 + rCurrentNPC.gfxOffY);
26126						mySpriteBatch.Draw(TextureAssets.GlowMask[224].Value, position38, rCurrentNPC.frame, newColor7, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
26127					}
26128					mySpriteBatch.Draw(TextureAssets.GlowMask[224].Value, vector72, rCurrentNPC.frame, color46, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
26129					float num322 = rCurrentNPC.localAI[0];
26130					if (num322 > 0f)
26131					{
26132						byte alpha15 = (byte)((Math.Cos(num322 * (MathF.PI * 2f) / 60f) * 0.5 + 0.5) * 32.0 + 0.0);
26133						Microsoft.Xna.Framework.Color color47 = new Microsoft.Xna.Framework.Color(180, 90, 255, alpha15) * 0.75f;
26134						float num323 = 1f;
26135						if (num322 < 60f)
26136						{
26137							float lerpValue3 = Utils.GetLerpValue(0f, 60f, num322);
26138							color47 *= lerpValue3;
26139							num323 = MathHelper.Lerp(1f, 0.5f, 1f - lerpValue3 * lerpValue3);
26140						}
26141						Texture2D value85 = TextureAssets.Extra[89].Value;
26142						Vector2 origin27 = value85.Size() / 2f;
26143						Vector2 scale10 = new Vector2(num323);
26144						float num324 = num322 * 0.0041887905f;
26145						float num325 = MathF.PI / 2f;
26146						scale10.Y *= 1f;
26147						scale10.X *= 1f;
26148						for (float num326 = 0f; num326 < 16f; num326 += 1f)
26149						{
26150							float num327 = num324 + MathF.PI * 2f * (num326 / 16f);
26151							Vector2 position39 = rCurrentNPC.Center - screenPos + num327.ToRotationVector2() * 400f * num323;
26152							mySpriteBatch.Draw(value85, position39, null, color47, num327 + MathF.PI / 2f + num325, origin27, scale10, SpriteEffects.None, 0f);
26153						}
26154					}
26155				}
26156				if (type == 546)
26157				{
26158					mySpriteBatch.Draw(TextureAssets.Extra[76].Value, vector72, rCurrentNPC.frame, new Microsoft.Xna.Framework.Color(255, 255, 255, 200), MathHelper.Clamp(rCurrentNPC.velocity.X * 0.1f, -MathF.PI / 8f, MathF.PI / 8f), halfSize, rCurrentNPC.scale, spriteEffects, 0f);
26159				}
26160				if ((type == 566 || type == 567) && rCurrentNPC.localAI[3] >= 115f)
26161				{
26162					int frameY = (int)(GlobalTimeWrappedHourly % 0.5f / 0.5f * 4f);
26163					Texture2D value86 = TextureAssets.Extra[80].Value;
26164					Microsoft.Xna.Framework.Rectangle rectangle14 = value86.Frame(1, 4, 0, frameY);
26165					Vector2 vector73 = new Vector2(rCurrentNPC.spriteDirection * 8, -26f) * rCurrentNPC.scale;
26166					int num328 = rCurrentNPC.frame.Y / rCurrentNPC.frame.Height;
26167					int num329 = 0;
26168					switch (num328)
26169					{
26170					case 0:
26171						num329 = 6;
26172						break;
26173					case 1:
26174						num329 = 4;
26175						break;
26176					case 2:
26177						num329 = 2;
26178						break;
26179					case 3:
26180						num329 = 6;
26181						break;
26182					case 4:
26183						num329 = 8;
26184						break;
26185					case 5:
26186						num329 = 6;
26187						break;
26188					case 6:
26189						num329 = 4;
26190						break;
26191					case 7:
26192						num329 = 6;
26193						break;
26194					case 8:
26195						num329 = 2;
26196						break;
26197					}
26198					Microsoft.Xna.Framework.Color color48 = new Microsoft.Xna.Framework.Color(255, 255, 255, 130);
26199					vector73.Y += num329;
26200					mySpriteBatch.Draw(value86, vector72 + vector73 * rCurrentNPC.scale, rectangle14, color48, MathHelper.Clamp(rCurrentNPC.velocity.X * 0.1f, -MathF.PI / 8f, MathF.PI / 8f), rectangle14.Size() / 2f, rCurrentNPC.scale * 0.7f, spriteEffects ^ SpriteEffects.FlipHorizontally, 0f);
26201				}
26202				if (type == 618)
26203				{
26204					mySpriteBatch.Draw(TextureAssets.Extra[129].Value, vector72, rCurrentNPC.frame, rCurrentNPC.GetAlpha(color44), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, spriteEffects, 0f);
26205				}
26206				break;
26207			}
26208			}
26209		}
26210	
26211		private static void DrawNPCDirect_Deerclops(SpriteBatch mySpriteBatch, NPC rCurrentNPC, ref Vector2 screenPos, int typeCache, ref Microsoft.Xna.Framework.Color npcColor, ref Vector2 halfSize, SpriteEffects npcSpriteEffect)
26212		{
26213			Texture2D value = TextureAssets.Npc[typeCache].Value;
26214			Vector2 vector = rCurrentNPC.Bottom - screenPos;
26215			Microsoft.Xna.Framework.Rectangle rectangle = value.Frame(5, 5, rCurrentNPC.frame.Y / 5, rCurrentNPC.frame.Y % 5, 2, 2);
26216			Vector2 origin = rectangle.Size() * new Vector2(0.5f, 1f);
26217			origin.Y -= 4f;
26218			int num = 106;
26219			if (rCurrentNPC.spriteDirection == 1)
26220			{
26221				origin.X = num;
26222			}
26223			else
26224			{
26225				origin.X = rectangle.Width - num;
26226			}
26227			Microsoft.Xna.Framework.Color value2 = Microsoft.Xna.Framework.Color.White;
26228			float amount = 0f;
26229			float amount2 = 0f;
26230			int num2 = 0;
26231			float num3 = 0f;
26232			float num4 = 0f;
26233			float num5 = 10f;
26234			Microsoft.Xna.Framework.Color color = npcColor;
26235			if (rCurrentNPC.localAI[3] > 0f)
26236			{
26237				float num6 = rCurrentNPC.localAI[3] / 36f;
26238				num2 = 2;
26239				num3 = num6 * num6;
26240				num4 = 20f;
26241				value2 = new Microsoft.Xna.Framework.Color(80, 0, 0, 255) * 0.5f;
26242				amount2 = 1f;
26243				color = Microsoft.Xna.Framework.Color.Lerp(Microsoft.Xna.Framework.Color.Transparent, color, 1f - num6 * num6);
26244			}
26245			for (int i = 0; i < num2; i++)
26246			{
26247				Microsoft.Xna.Framework.Color value3 = npcColor;
26248				value3 = Microsoft.Xna.Framework.Color.Lerp(value3, value2, amount);
26249				value3 = rCurrentNPC.GetAlpha(value3);
26250				value3 = Microsoft.Xna.Framework.Color.Lerp(value3, value2, amount2);
26251				value3 *= 1f - num3 * 0.5f;
26252				Vector2 vector2 = vector;
26253				mySpriteBatch.Draw(value, vector2 + new Vector2(0f, 1f).RotatedBy((float)i * (MathF.PI * 2f) / (float)num2 + GlobalTimeWrappedHourly * num5) * num3 * num4, rectangle, value3, rCurrentNPC.rotation, origin, rCurrentNPC.scale, npcSpriteEffect ^ SpriteEffects.FlipHorizontally, 0f);
26254			}
26255			Microsoft.Xna.Framework.Color color2 = rCurrentNPC.GetAlpha(color);
26256			Microsoft.Xna.Framework.Color value4 = new Microsoft.Xna.Framework.Color(50, 0, 160);
26257			float num7 = 0f;
26258			if (rCurrentNPC.localAI[3] > 0f)
26259			{
26260				float amount3 = Utils.Remap(rCurrentNPC.localAI[3], 0f, 20f, 0f, 1f);
26261				color2 = Microsoft.Xna.Framework.Color.Lerp(color2, value4, amount3);
26262			}
26263			if (rCurrentNPC.ai[0] == 7f || rCurrentNPC.ai[0] == 8f)
26264			{
26265				num7 = Utils.Remap(rCurrentNPC.ai[1], 20f, 60f, 0f, 2f);
26266				if (num7 > 1f)
26267				{
26268					num7 = 2f - num7;
26269				}
26270				color2 = Microsoft.Xna.Framework.Color.Lerp(color2, value4, num7);
26271				color2 *= 1f - num7;
26272				float num8 = 5f;
26273				for (int j = 0; (float)j < num8; j++)
26274				{
26275					Vector2 vector3 = vector;
26276					float num9 = num7 * num7;
26277					float num10 = 80f * num9;
26278					float num11 = 80f * num9 + (float)(30 * j) * num9;
26279					Vector2 vector4 = Vector2.UnitX.RotatedBy((float)j * (MathF.PI * 2f) / num8 + GlobalTimeWrappedHourly * 6f) * num10;
26280					Vector2 vector5 = Vector2.UnitX.RotatedBy((float)j * (MathF.PI * 2f) / num8 + GlobalTimeWrappedHourly * 3f * ((float)j * 0.5f)) * num11;
26281					mySpriteBatch.Draw(value, vector3 + vector4 + vector5, rectangle, color2 * 0.5f, rCurrentNPC.rotation, origin, rCurrentNPC.scale, npcSpriteEffect ^ SpriteEffects.FlipHorizontally, 0f);
26282				}
26283			}
26284			mySpriteBatch.Draw(value, vector, rectangle, color2, rCurrentNPC.rotation, origin, rCurrentNPC.scale, npcSpriteEffect ^ SpriteEffects.FlipHorizontally, 0f);
26285			if (rCurrentNPC.localAI[3] > 0f)
26286			{
26287				Texture2D value5 = TextureAssets.Extra[245].Value;
26288				float num12 = Utils.Remap(rCurrentNPC.localAI[3], 0f, 20f, 0f, 1f);
26289				Microsoft.Xna.Framework.Color color3 = new Microsoft.Xna.Framework.Color(255, 30, 30, 66) * rCurrentNPC.Opacity * num12 * 0.25f * (1f - num7);
26290				for (int k = 0; k < num2; k++)
26291				{
26292					Vector2 vector6 = vector;
26293					mySpriteBatch.Draw(value5, vector6 + new Vector2(0f, 1f).RotatedBy((float)k * (MathF.PI * 2f) / (float)num2 + GlobalTimeWrappedHourly * num5) * num3 * 4f, rectangle, color3, rCurrentNPC.rotation, origin, rCurrentNPC.scale, npcSpriteEffect ^ SpriteEffects.FlipHorizontally, 0f);
26294				}
26295			}
26296		}
26297	
26298		private static void DrawNPCDirect_DeerclopsLeg(SpriteBatch mySpriteBatch, NPC rCurrentNPC, ref Vector2 screenPos, int typeCache, ref Microsoft.Xna.Framework.Color npcColor, ref Vector2 halfSize, SpriteEffects npcSpriteEffect)
26299		{
26300			Microsoft.Xna.Framework.Rectangle? sourceRectangle = null;
26301			int num = 0;
26302			int num2 = 0;
26303			mySpriteBatch.Draw(TextureAssets.Npc[typeCache].Value, new Vector2(rCurrentNPC.position.X - screenPos.X + (float)(rCurrentNPC.width / 2) - (float)TextureAssets.Npc[typeCache].Width() * rCurrentNPC.scale / 2f + halfSize.X * rCurrentNPC.scale, rCurrentNPC.position.Y - screenPos.Y + (float)rCurrentNPC.height - (float)TextureAssets.Npc[typeCache].Height() * rCurrentNPC.scale / (float)npcFrameCount[typeCache] + 4f + halfSize.Y * rCurrentNPC.scale + (float)num2 + (float)num + rCurrentNPC.gfxOffY), sourceRectangle, rCurrentNPC.GetAlpha(npcColor), rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, npcSpriteEffect, 0f);
26304		}
26305	
26306		private static void DrawNPCDirect_Faeling(SpriteBatch mySpriteBatch, NPC rCurrentNPC, ref Vector2 screenPos, int typeCache, ref Microsoft.Xna.Framework.Color npcColor, ref Vector2 halfSize, SpriteEffects npcSpriteEffect)
26307		{
26308			Texture2D value = TextureAssets.Npc[typeCache].Value;
26309			Vector2 vector = rCurrentNPC.Center - screenPos;
26310			int num = 5;
26311			int horizontalFrames = 4;
26312			float num2 = ((float)rCurrentNPC.whoAmI * 0.11f + (float)timeForVisualEffects / 360f) % 1f;
26313			Microsoft.Xna.Framework.Color color = hslToRgb(num2, 1f, 0.65f);
26314			color.A /= 2;
26315			float rotation = rCurrentNPC.rotation;
26316			Microsoft.Xna.Framework.Rectangle rectangle = value.Frame(horizontalFrames, num, 0, rCurrentNPC.frame.Y);
26317			Vector2 origin = rectangle.Size() / 2f;
26318			float scale = rCurrentNPC.scale;
26319			Microsoft.Xna.Framework.Rectangle value2 = value.Frame(horizontalFrames, num, 2);
26320			Microsoft.Xna.Framework.Color color2 = new Microsoft.Xna.Framework.Color(255, 255, 255, 0) * 1f;
26321			int num3 = rCurrentNPC.oldPos.Length;
26322			int num4 = num3 - 1 - 5;
26323			int num5 = 5;
26324			int num6 = 3;
26325			float num7 = 32f;
26326			float num8 = 16f;
26327			float fromMax = new Vector2(num7, num8).Length();
26328			float num9 = Utils.Remap(Vector2.Distance(rCurrentNPC.oldPos[num4], rCurrentNPC.position), 0f, fromMax, 0f, 100f);
26329			num9 = (int)num9 / 5;
26330			num9 *= 5f;
26331			num9 /= 100f;
26332			num8 *= num9;
26333			num7 *= num9;
26334			float num10 = 9f;
26335			float num11 = 0.5f;
26336			float num12 = MathF.PI;
26337			for (int num13 = num4; num13 >= num5; num13 -= num6)
26338			{
26339				Vector2 vector2 = rCurrentNPC.oldPos[num13] - rCurrentNPC.position;
26340				float num14 = Utils.Remap(num13, 0f, num3, 1f, 0f);
26341				float num15 = 1f - num14;
26342				Vector2 spinningpoint = new Vector2((float)Math.Sin((double)((float)rCurrentNPC.whoAmI / 17f) + timeForVisualEffects / (double)num10 + (double)(num14 * 2f * (MathF.PI * 2f))) * num8, 0f - num7) * num15;
26343				vector2 += spinningpoint.RotatedBy(num12);
26344				Microsoft.Xna.Framework.Color color3 = hslToRgb((num2 + num15 * num11) % 1f, 1f, 0.5f);
26345				color3.A = 0;
26346				mySpriteBatch.Draw(value, vector + vector2, value2, color3 * num14 * 0.16f, rotation, origin, scale * Utils.Remap(num14 * num14, 0f, 1f, 0f, 2.5f), npcSpriteEffect, 0f);
26347			}
26348			mySpriteBatch.Draw(value, vector, value2, color2, rotation, origin, scale, npcSpriteEffect, 0f);
26349			Microsoft.Xna.Framework.Rectangle value3 = value.Frame(horizontalFrames, num, 1, rCurrentNPC.frame.Y);
26350			Microsoft.Xna.Framework.Color white = Microsoft.Xna.Framework.Color.White;
26351			white.A /= 2;
26352			mySpriteBatch.Draw(value, vector, value3, white, rotation, origin, scale, npcSpriteEffect, 0f);
26353			mySpriteBatch.Draw(value, vector, rectangle, color, rotation, origin, scale, npcSpriteEffect, 0f);
26354			float num16 = MathHelper.Clamp((float)Math.Sin(timeForVisualEffects / 60.0) * 0.3f + 0.3f, 0f, 1f);
26355			float num17 = 0.8f + (float)Math.Sin(timeForVisualEffects / 15.0 * 6.2831854820251465) * 0.3f;
26356			Microsoft.Xna.Framework.Rectangle value4 = value.Frame(horizontalFrames, num, 3, rCurrentNPC.whoAmI % num);
26357			Microsoft.Xna.Framework.Color color4 = Microsoft.Xna.Framework.Color.Lerp(color, new Microsoft.Xna.Framework.Color(255, 255, 255, 0), 0.5f) * num16;
26358			mySpriteBatch.Draw(value, vector, value4, color4, rotation, origin, scale * num17, SpriteEffects.None, 0f);
26359			Microsoft.Xna.Framework.Rectangle value5 = value.Frame(horizontalFrames, num, 3, 1);
26360			Microsoft.Xna.Framework.Color color5 = Microsoft.Xna.Framework.Color.Lerp(color, new Microsoft.Xna.Framework.Color(255, 255, 255, 0), 0.5f) * num16;
26361			mySpriteBatch.Draw(value, vector, value5, color5, rotation, origin, scale * num17, SpriteEffects.None, 0f);
26362		}
26363	
26364		private static void DrawNPCDirect_HallowBoss(SpriteBatch mySpriteBatch, NPC rCurrentNPC, ref Vector2 screenPos, int typeCache, ref Microsoft.Xna.Framework.Color npcColor, ref Vector2 halfSize, SpriteEffects npcSpriteEffect)
26365		{
26366			Texture2D value = TextureAssets.Npc[typeCache].Value;
26367			Vector2 vector = rCurrentNPC.Center - screenPos;
26368			bool flag = rCurrentNPC.AI_120_HallowBoss_IsInPhase2();
26369			int num = (int)rCurrentNPC.ai[0];
26370			Texture2D value2 = TextureAssets.Extra[159].Value;
26371			Microsoft.Xna.Framework.Rectangle rectangle = value2.Frame(1, 11, 0, (int)(rCurrentNPC.localAI[0] / 4f) % 11);
26372			Microsoft.Xna.Framework.Color color = rCurrentNPC.GetAlpha(npcColor);
26373			Texture2D value3 = TextureAssets.Extra[158].Value;
26374			Texture2D value4 = TextureAssets.Extra[160].Value;
26375			Texture2D value5 = TextureAssets.Extra[157].Value;
26376			DrawNPCDirect_GetHallowBossArmFrame(rCurrentNPC, out var armFrame_Count, out var armFrameToUseLeft, out var armFrameToUseRight);
26377			Microsoft.Xna.Framework.Rectangle rectangle2 = value3.Frame(1, armFrame_Count, 0, armFrameToUseLeft);
26378			Microsoft.Xna.Framework.Rectangle rectangle3 = value4.Frame(1, armFrame_Count, 0, armFrameToUseRight);
26379			Vector2 origin = rectangle2.Size() / 2f;
26380			Vector2 origin2 = rectangle3.Size() / 2f;
26381			int num2 = 0;
26382			int num3 = 0;
26383			if (armFrameToUseLeft == 5)
26384			{
26385				num2 = 1;
26386			}
26387			if (armFrameToUseRight == 5)
26388			{
26389				num3 = 1;
26390			}
26391			float num4 = 1f;
26392			int num5 = 0;
26393			int num6 = 0;
26394			float num7 = 0f;
26395			float num8 = 0f;
26396			float num9 = 0f;
26397			if (num == 8 || num == 9)
26398			{
26399				num7 = Utils.GetLerpValue(0f, 30f, rCurrentNPC.ai[1], clamped: true) * Utils.GetLerpValue(90f, 30f, rCurrentNPC.ai[1], clamped: true);
26400				num8 = Utils.GetLerpValue(0f, 30f, rCurrentNPC.ai[1], clamped: true) * Utils.GetLerpValue(90f, 70f, rCurrentNPC.ai[1], clamped: true);
26401				num9 = Utils.GetLerpValue(0f, 15f, rCurrentNPC.ai[1], clamped: true) * Utils.GetLerpValue(45f, 30f, rCurrentNPC.ai[1], clamped: true);
26402				color = Microsoft.Xna.Framework.Color.Lerp(color, Microsoft.Xna.Framework.Color.White, num7);
26403				num4 *= 1f - num9;
26404				num5 = 4;
26405				num6 = 3;
26406			}
26407			if (num == 10)
26408			{
26409				num7 = Utils.GetLerpValue(30f, 90f, rCurrentNPC.ai[1], clamped: true) * Utils.GetLerpValue(165f, 90f, rCurrentNPC.ai[1], clamped: true);
26410				num8 = Utils.GetLerpValue(0f, 60f, rCurrentNPC.ai[1], clamped: true) * Utils.GetLerpValue(180f, 120f, rCurrentNPC.ai[1], clamped: true);
26411				num9 = Utils.GetLerpValue(0f, 60f, rCurrentNPC.ai[1], clamped: true) * Utils.GetLerpValue(180f, 120f, rCurrentNPC.ai[1], clamped: true);
26412				color = Microsoft.Xna.Framework.Color.Lerp(color, Microsoft.Xna.Framework.Color.White, num7);
26413				num4 *= 1f - num9;
26414				num6 = 4;
26415			}
26416			if (num6 + num5 > 0)
26417			{
26418				for (int i = -num6; i <= num6 + num5; i++)
26419				{
26420					if (i == 0)
26421					{
26422						continue;
26423					}
26424					Microsoft.Xna.Framework.Color color2 = Microsoft.Xna.Framework.Color.White;

```


---

## 🤖 Assistant · 2026-08-11T07:14:31.116Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I've now covered through 26209 (end of the switch statement of DrawNPCDirect). The method ends at 26209. Helper methods continue: DrawNPCDirect_Deerclops, Faeling, HallowBoss, etc. These are also called from DrawNPCDirect.

Also there's DrawNPCExtras (aiStyle == 7) which is a big extra-drawing method — that's definitely "NPC 附属部件程序化叠画" territory (worm body segments etc.). The user asked to enumerate DrawNPCs/DrawNPC special branches. DrawNPCExtras is called at 24748 and 25793. Should I include it? The user's anchors include 24746 aiStyle==7 and 25791 aiStyle==7. So the aiStyle==7 branches are the calls. But "系统性枚举 DrawNPCs/DrawNPC 里所有'NPC 附属部件程序化叠画'的特例分支" — the focus is on branches within DrawNPCs/DrawNPC. DrawNPCExtras is a separate method; I should mention it as a delegated branch with a brief summary.

Let me check DrawNPCExtras to summarize what it draws. Let me find it.

Also need to check the region after 26209? The DrawNPCDirect method ends at 26209 (line 26209 closes it). Good. And before 22159? Let me check there's nothing else relevant. The user said scan around the range too. DrawNPCs begins 22159. Before that might be DrawGore etc. Let me quickly check what's around 21500-22159 for NPC-related draws. Probably not NPC. Let me quickly grep for other Draw methods that draw NPC extras, e.g. DrawNPCExtras, DrawNPC_SlimeItem, DrawElderEye.

Let me look at DrawNPCExtras signature and main content briefly.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:14:31.678Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"private void DrawNPCExtras\\|void DrawNPC_SlimeItem\\|void DrawElderEye\\|DrawNPCDirect_\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head -30",
 "description": "Find helper drawing method definitions"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:31.699Z

**📎 ToolResult**

```
22149:	protected void DrawElderEye(SpriteBatch spriteBatch, Vector2 worldPosition, float opacity, float scale, int frameNumber, Microsoft.Xna.Framework.Color passedColor)
22318:	public void DrawNPCDirect_QueenSlimeWings(NPC rCurrentNPC, SpriteBatch mySpriteBatch, Vector2 screenPos, Vector2 drawCenter, Microsoft.Xna.Framework.Color originColor)
23147:						DrawNPCDirect_QueenSlimeWings(rCurrentNPC, mySpriteBatch, screenPos, rCurrentNPC.Center, color21);
23723:					DrawNPCDirect_HallowBoss(mySpriteBatch, rCurrentNPC, ref screenPos, type, ref npcColor, ref halfSize, spriteEffects);
23726:					DrawNPCDirect_Faeling(mySpriteBatch, rCurrentNPC, ref screenPos, type, ref npcColor, ref halfSize, spriteEffects);
23729:					DrawNPCDirect_Deerclops(mySpriteBatch, rCurrentNPC, ref screenPos, type, ref npcColor, ref halfSize, spriteEffects);
26211:	private static void DrawNPCDirect_Deerclops(SpriteBatch mySpriteBatch, NPC rCurrentNPC, ref Vector2 screenPos, int typeCache, ref Microsoft.Xna.Framework.Color npcColor, ref Vector2 halfSize, SpriteEffects npcSpriteEffect)
26298:	private static void DrawNPCDirect_DeerclopsLeg(SpriteBatch mySpriteBatch, NPC rCurrentNPC, ref Vector2 screenPos, int typeCache, ref Microsoft.Xna.Framework.Color npcColor, ref Vector2 halfSize, SpriteEffects npcSpriteEffect)
26306:	private static void DrawNPCDirect_Faeling(SpriteBatch mySpriteBatch, NPC rCurrentNPC, ref Vector2 screenPos, int typeCache, ref Microsoft.Xna.Framework.Color npcColor, ref Vector2 halfSize, SpriteEffects npcSpriteEffect)
26364:	private static void DrawNPCDirect_HallowBoss(SpriteBatch mySpriteBatch, NPC rCurrentNPC, ref Vector2 screenPos, int typeCache, ref Microsoft.Xna.Framework.Color npcColor, ref Vector2 halfSize, SpriteEffects npcSpriteEffect)
26376:		DrawNPCDirect_GetHallowBossArmFrame(rCurrentNPC, out var armFrame_Count, out var armFrameToUseLeft, out var armFrameToUseRight);
26552:	private static void DrawNPCDirect_GetHallowBossArmFrame(NPC rCurrentNPC, out int armFrame_Count, out int armFrameToUseLeft, out int armFrameToUseRight)
26709:	private static void DrawNPC_SlimeItem(NPC rCurrentNPC, int typeCache, Microsoft.Xna.Framework.Color npcColor, float addedRotation)

```


---

## 🤖 Assistant · 2026-08-11T07:14:33.601Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
DrawNPCExtras — search in Main.cs or elsewhere? grep found no "private void DrawNPCExtras" in Main.cs. It may be in another file (Main.Partial.cs). Let me grep the repo.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:14:33.919Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"void DrawNPCExtras\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ | head",
 "description": "Find DrawNPCExtras definition"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:33.947Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:26812:	protected void DrawNPCExtras(NPC n, bool beforeDraw, float addHeight, float addY, Microsoft.Xna.Framework.Color npcColor, Vector2 halfSize, SpriteEffects npcSpriteEffect, Vector2 screenPosition)

```


---

## 🤖 Assistant · 2026-08-11T07:14:35.458Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "limit": 190,
 "offset": 26812
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:35.466Z

**📎 ToolResult**

```
26812		protected void DrawNPCExtras(NPC n, bool beforeDraw, float addHeight, float addY, Microsoft.Xna.Framework.Color npcColor, Vector2 halfSize, SpriteEffects npcSpriteEffect, Vector2 screenPosition)
26813		{
26814			if (!beforeDraw && n.UsesPartyHat())
26815			{
26816				int num = n.frame.Y / n.frame.Height;
26817				int[] array = NPCID.Sets.TownNPCsFramingGroups[NPCID.Sets.NPCFramingGroup[n.type]];
26818				if (num >= array.Length)
26819				{
26820					num = 0;
26821				}
26822				Texture2D value = TextureAssets.Extra[72].Value;
26823				int num2 = 0;
26824				switch (n.GetPartyHatColor())
26825				{
26826				case PartyHatColor.Pink:
26827					num2 = 16;
26828					break;
26829				case PartyHatColor.Cyan:
26830					num2 = 17;
26831					break;
26832				case PartyHatColor.Purple:
26833					num2 = 18;
26834					break;
26835				case PartyHatColor.White:
26836					num2 = 19;
26837					break;
26838				}
26839				Microsoft.Xna.Framework.Rectangle rectangle = value.Frame(20, 1, num2 % 20);
26840				rectangle.Width -= 2;
26841				rectangle.Height -= 2;
26842				int num3 = 0;
26843				int num4 = 0;
26844				int num5 = n.spriteDirection;
26845				if (n.type == 663)
26846				{
26847					num3 = 1;
26848				}
26849				if (n.type == 637)
26850				{
26851					num3 = 6;
26852					switch (num)
26853					{
26854					case 19:
26855					case 22:
26856					case 23:
26857					case 24:
26858					case 25:
26859					case 26:
26860					case 27:
26861						num3 -= 2;
26862						break;
26863					case 11:
26864					case 12:
26865					case 13:
26866					case 14:
26867					case 15:
26868						num3 += 2;
26869						break;
26870					}
26871				}
26872				if (n.type == 638)
26873				{
26874					num3 = 12;
26875				}
26876				if (n.type == 656)
26877				{
26878					num3 = 6;
26879					switch (num)
26880					{
26881					case 1:
26882					case 2:
26883					case 3:
26884						num3 -= 2;
26885						break;
26886					case 18:
26887					case 19:
26888					case 20:
26889					case 21:
26890					case 22:
26891					case 23:
26892					case 24:
26893					case 25:
26894						num3 -= 4;
26895						break;
26896					case 8:
26897						num3 -= 2;
26898						break;
26899					}
26900				}
26901				if (NPCID.Sets.IsTownSlime[n.type])
26902				{
26903					num5 *= -1;
26904					switch (n.type)
26905					{
26906					default:
26907						num3 = 1;
26908						break;
26909					case 670:
26910					case 679:
26911						num3 = -1;
26912						break;
26913					case 681:
26914						num3 = -2;
26915						break;
26916					case 682:
26917						num3 = -1;
26918						num4 = 2;
26919						break;
26920					case 683:
26921						num3 = -1;
26922						num4 = -2;
26923						break;
26924					case 684:
26925						num3 = -4;
26926						break;
26927					}
26928				}
26929				if (n.IsShimmerVariant)
26930				{
26931					switch (n.type)
26932					{
26933					case 38:
26934						num3 += 2;
26935						num4 = -2;
26936						break;
26937					case 178:
26938					case 228:
26939						num3 = -4;
26940						num4 = -4;
26941						break;
26942					case 107:
26943						num3 = 2;
26944						num4 = -6;
26945						break;
26946					case 54:
26947						num4 = -6;
26948						break;
26949					case 160:
26950						num4 = -2;
26951						break;
26952					case 108:
26953					case 124:
26954					case 208:
26955					case 209:
26956					case 227:
26957						num4 = -4;
26958						break;
26959					}
26960				}
26961				Vector2 bottom = n.Bottom;
26962				Vector2 vector = -new Vector2(0f, n.height) + new Vector2(-2 * num5, n.gfxOffY);
26963				vector.X += num3 * num5;
26964				vector.Y += array[num];
26965				vector.Y += num4;
26966				vector.Y += NPCID.Sets.HatOffsetY[n.type];
26967				int num6 = 0;
26968				if (n.ai[0] == 5f)
26969				{
26970					num6 = -4;
26971					if (n.type == 38)
26972					{
26973						num6 = -8;
26974					}
26975					if (n.type == 124)
26976					{
26977						num6 = -2;
26978					}
26979					if (n.type == 550)
26980					{
26981						num6 = -4;
26982					}
26983					if (n.type == 588)
26984					{
26985						num6 = -4;
26986					}
26987					if (n.type == 108 || n.type == 178)
26988					{
26989						num6 = -6;
26990					}
26991					if (n.type == 637)
26992					{
26993						num6 = -12;
26994					}
26995					if (n.type == 663)
26996					{
26997						num6 = -8;
26998					}
26999				}
27000				vector.Y += num6;
27001				if (n.type == 229 && n.ai[0] == 12f)

```


---

## 🤖 Assistant · 2026-08-11T07:16:09.626Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
OK, DrawNPCExtras is the town NPC extras (party hats, and more). That's a delegated branch. I'll summarize it.

Now I should compile the table. Let me organize by section. Key criteria: only "things drawn in addition to the NPC body texture" — chains/vines/arms/capes/ninjas/crowns/halos/trails. Exclude pure color/alpha/frame selection logic.

Important: glow masks — the user says "光环" (halo/aura) counts as extra. Glow masks are extra overlays drawn on top of the body; they're technically a second draw of a glow texture. The user explicitly lists "光环" as counting. So include glow mask overlays. But wait — "不要统计纯颜色/alpha/帧选择逻辑" — glow mask draws are additional texture draws, so include them. However there are MANY glow mask cases (types 24, 411, 409, 410, 407, 405, 406, 424, 423, 421, 420, 429, 418, 412-414, 415, 419, 417, 516, 518, 344, 346, 315, 525, 526, 527, 533, 160, 209, 426, 427, 437, 472, 386, 387, 388, 389, 520, 383, 381, 382, 654, 653, 639-645, 646-652...). These are single flat glow overlays — arguably "纯颜色叠加"? They're extra textures (glow mask) drawn over the body. Hmm. The user said "只统计'在 NPC 本体贴图之外额外画的东西'（链/藤蔓/手臂/披风/忍者/王冠/光环/拖尾等）". 光环 = halo/aura → glow masks count. I'll include them but group them in one row or a few rows, noting they're flat glow overlays. Actually the flat glow masks with no geometry (no afterimage/trail/offset) are borderline "纯颜色/alpha" logic. I think best: include a row for "flat GlowMask overlay" group listing all types, and separate rows for the ones with geometric effects (velocity-offset copies, afterimages, extra drawn parts).

Let me be systematic. I'll now enumerate all branches in order, from 22159 to 26209.

**DrawNPCs (22159-22301):**
1. 22177-22224: type==125||126 (Mechdusa heads? Actually 125/126 = Prime Cannon/Saw... in 1.4.4 these are Retinazer-ish? No — type 125 = Prime Cannon, 126 = Prime Saw; but the chain drawn is TextureAssets.Chain12 connecting them; in 1.4.4, Mechdusa). Condition: !NPC.IsMechQueenUp && !flag. Draws Chain12 in a step loop (40*scale step) linking the two NPCs. Flag ensures once.
2. 22225-22252: type==263 && aiStyle==52 && NPC.plantBoss>=0 (Plantera's Hook). Draws Chain26 in a step loop toward plantBoss center.
3. 22253-22285: type==264 && aiStyle==53 && NPC.plantBoss>=0 (Plantera's Tentacle). Draws Chain27 step loop; target = ai[3]-1 if ai[3]>0 else plantBoss.

**DrawNPCDirect (22350-26209):**

4. 22391-22432: type==101 (Man Eater / 食人花 snaptrap? type 101 = Man Eater). Draws alternating Chain10/Chain11 segments (0.75 scale, height 28→clamped) toward tile coords ai[0], ai[1]. Bestiary color handling.
5. 22433-22498: aiStyle==13 (vine-type hanging enemies: 42? Actually types: 56 = Wall Creeper, 175 = Black Recluse hangs?, 259/260 = ...). Chain textures by type: 56→Chain5, 175→Chain14, 259→Chain24, 260→Chain25, default→Chain4. Step 28/40 (12/20 for 259/260). Target tile ai[0], ai[1].
6. 22499-22506: type==327 (Pumpking). Draws TextureAssets.PumpkingCloak (5 frames, frame = localAI[1]) at Center + (0,80). Cape below body.
7. 22507-22542: type==328 (PumpkingBlade? Actually 328 = PumpkingBlade... no wait. 328 draws PumpkingArm twice with offset toward npc[ai[1]] — that's Pumpking's scythe arms? Hmm, type 328 = PumpkingBlade. But it draws "PumpkingArm" 2 segments with offsets of 200*ai[0]/130 and 50/80. Hmm this is actually the Pumpking boss head's arms? Actually in code: vector4 = position + width*0.5 - 5*ai[0], y+20; targets npc[ai[1]] (Pumpking). It's the blade's handle/arm. Anyway: type 328 draws PumpkingArm 2 segments.
8. 22543-22592: type==36 (Skeletron hand? No — type 36 = SkeletronHand? Actually 33-36 are Skeletron head/hands: 36 = SkeletronHand). Draws BoneArm / BoneArm3 (if localAI[3]==1) 2 segments with same 200/130, 50/80 offsets toward npc[ai[1]]; dust at tip when AllowMiscDustEffects.
9. 22593-22632: aiStyle==47 (Golem fist, types 247/248? no — aiStyle 47 is Golem Fist; type 247 is GolemFistLeft, 248 GolemFistRight... hmm type !=247 check: num18 = (type != 247) ? +66*scale : -70*scale). Draws Chain21 step loop (16*scale step) toward golemBoss center offset.
10. 22633-22675: aiStyle 33-36 (Skeletron prime hands: aiStyle 33/34/35/36). Draws BoneArm2 2 segments (200/130, 50/80 offsets) toward npc[ai[1]]; dust at tip.
11. 22676-22713: type==693 (new 1.4.5 NPC?). Draws TextureAssets.Extra[289] as a swirl/halo at rCurrentNPC.Top, rotation = localAI[0]*0.016*localAI[3], scale by localAI[2], fade in/out by localAI[0] vs localAI[1] (duration) — a spinning portal/ring. Extra draw.
12. 22714-22741: aiStyle==20 (spiked ball / flail-like? aiStyle 20 = "spike ball"? Actually aiStyle 20 is the spiked ball chain... no, aiStyle 20 is the "SpikeBase + Chain" e.g. type 23 Spiked Ball? Hmm. It draws Chain in 12-step loop toward ai[1], ai[2] (world coords) and then SpikeBase at anchor rotated by rotation-0.75. This is the chain+base of the spiked ball / dungeon flail enemies. Note it also sets rCurrentNPC.rotation.
13. 22798-22818: type==50 (King Slime). Draws TextureAssets.Ninja (the ninja inside King Slime) offset by -velocity*2 (X), -velocity.Y, rotation by velocity.X*0.05, plus frame-based Y tweaks.
14. 22819-22840: type==71 (Voodoo demon? No, 71 = Tim? Hmm. It draws GetItemDrawFrame(327,...) — item 327 is Ninja Hood? No, item 327... Actually type 71 = "Blazing Wheel"? Let me think: type 71 draws an item frame (item 327). NPC 71 = Tim? Hmm — Tim wears a wizard hat? Item 327 in 1.4 = "Wizard Hat"? Let me not overclaim; I can say "draws item texture (itemID 327) as a hat offset". Actually NPC 71 is Tim, and item 327 might be the Magic Hat. Hmm. Let me verify quickly with NPCID names if available. I'll grep NPCID for names.

Actually let me check whether there's an NPCID.cs with constants to name types. That would improve the report.

15. 22841-22844: type==69 (Antlion charger? No—69 = Antlion? It draws TextureAssets.AntLion at bottom, i.e., the sand mound part of Antlion). Extra part: AntLion mound drawn at feet.
16. 22845-22848: NPCID.Sets.SlimeCanContainItems[type] && ai[1]>0 → DrawNPC_SlimeItem — draws the item inside slime.
17. 22989-23026: type==124 && localAI[0]==0 (Santa? no, 124 = Flying Snake? Hmm 124 = "Flying Snake"? Actually 124 draws Projectile 582 headgear offsets → this is the "bestiary"/town NPC with headgear — type 124 = Santa Claus? Santa uses headgear... Let me check: type 124 in 1.4.4 is "Santa Claus". It draws Projectile[582] or Extra[263] (variant) as a hat (Santa hat) on head, using OffsetsPlayerHeadgear.
18. 23034-23102: case 551 (Empress of Light's "Prismatic Lacewing"? No—551 draws Extra[82]/Extra[81] wings + body + GlowMask[226], plus oldPos afterimage loop (9→0 step -3) drawing wing textures & body → that's Queen Slime? no. Type 551 = "Empress of Light"? Actually 636 is HallowBoss (Empress). 551 = "Butterfly"? Hmm. It draws Extra[81]/[82] as spinning wings with localAI[0] frames, localAI[1], plus afterimages. Type 551... Let me look up: 551 might be "Fairy critter"? No, critters have wing-like extras. Actually with oldPos afterimages and wings at (171,44) and (230,52) offsets — that's a fairy (Fairy critter, types 551? no 551 is...). Let me check NPCID names in the repo if available.
19. 23103-23133: case 690 (new). Draws Tile[105] (some tile texture) as a 2x3 block grid on the NPC (using ai[1] as frame), rotation. Composite multi-part body.
20. 23134-23300: case 657 (Queen Slime). Wings via DrawNPCDirect_QueenSlimeWings (only if life <= lifeMax/2), Extra[186] crystal (QueenSlime crystal) with frame-based Y offsets and QueenSlime shader, plus ai[0]==4&&velocity.Y!=0 jump afterimages (8 copies of the body), then Extra[177] (crown/tiara? at Top-...). Multi-part.
21. 23301-23348: cases 576/577 (Queen Slime's blob minions? Actually 576/577 = QueenSlimeMinionPink/Purple). Spawns ghost afterimages during localAI[3]<60 (spawn animation).
22. 23349-23379: case 696 (new 1.4.5). Body + second frame row (Y+=Height*18) drawn twice with random offsets (TileFrameSeed jitter) as a static-y overlay; emote bubble when ai[0]==2.
23. 23380-23402: case 594 (Windy Balloon? Actually 594 = WindyBalloon). Frame(8,1) balloon; draws slave slime NPC (AI_113_WindyBalloon_GetSlaveNPC) body inside/attached (DrawNPC_SlimeItem + two draws of slave NPC texture). So balloon + carried slime.
24. 23403-23412: case 686. Simple full-texture draw (no extras) — skip? It just draws body. Not an extra. Exclude (it's the dedicated draw branch but no extra). I'll mention only if needed. The user wants extras only. Skip.
25. 23413-23496: cases 564/565 (Empress minions? 564 = ? ). Ghost afterimages during localAI[3]<60 spawn + 4 radial pulsing afterimages + GlowMask[225] glow with 4 radial copies. Extra: afterimages + glow.
26. 23497-23619: case 548 (Crystal? "Crystal" — the Crystal in shimmer? Actually 548 = "Crystal"?: draws GlowMask[239] halo above (position -40 Y) pulsing, Extra[89] beam, 4 radial afterimages, and when ai[1]==2 CrystalWin filter). This is likely "Empress Crystal"? Hmm 548... Might be "Vortex"? Whatever. Extra: aura/glow/afterimages.
27. 23621-23641: case 371/454-459/621-623 — simple body draw, no extras. Exclude.
28. 23642-23721: case 549 (Moon Leech? no — 549 = "Empress"? 549 uses DrawElderEye and orbiting body copies, localAI[0]<120 spawn scale). Draws orbiting afterimage copies + DrawElderEye (Extra? DrawElderEye at 22149 draws elder eye texture). Type 549 = "Empress of Light"? no. 549 is likely "Fairy"? Hmm, DrawElderEye is used by... it's used for type 549 which is probably "Moon Lord's eye"? no. Let me check: DrawElderEye draws "Extra_?" I saw at 22149. Elder = old ones' army? 549 could be "Old One's Army" boss (Betsy is 551!). Wait — 551 = Betsy. Yes! Betsy draws wings (Extra[81]/[82] as wings) with afterimages. So 549 = Ogre? Ogre has an eye? Actually DrawElderEye draws the Ogre's... hmm, Ogre is 549? Ogre's hammer? Betsy is 551, Ogre is 549? Dark mage is 547? Let me recall 1.4 NPC ids: 549 = Ogre? I think 549 = "Ogre" (dd2 ogre), 551 = Betsy, 576/577 = ... no. Hmm, actually Betsy = 551? I believe Betsy is 551. Ogre = 549. And DrawElderEye — Ogre's big eye? Ogre doesn't have a prominent eye... Betsy? Hmm. Actually DrawElderEye is probably for the Ogre2? I'd better check NPCID for names.

Let me grep NPCID.cs if exists in the decompiled source.

29. 23722-23724: case 636 → DrawNPCDirect_HallowBoss (Empress of Light): draws Extra[157]/[158]/[159]/[160] arms/wings + body, with ai[0] 8/9/10 clone copies. Delegate.
30. 23725-23727: case 677 → DrawNPCDirect_Faeling: body layers + trail (oldPos) swirl trail.
31. 23728-23730: case 668 → DrawNPCDirect_Deerclops: body + localAI[3] spawn ghosts + ai[0] 7/8 teleport copies + Extra[245] red glow overlay.
32. 23731-23847: cases 422/493/507/517 (Lunar pillar towers? no, these are Vortex/Nebula/Solar/Stardust Pillar? no, 422=Vortex? Hmm. These draw GlowMask radial velocity afterimages (4 copies) + ForceField Perlin shield when ShieldStrengthTower>0). These are the "Lunar Pillar" NPCs? Actually NPC 422 = Lunar Tower Vortex? No, towers are 422 (Vortex), 493 (Stardust), 507 (Nebula), 517 (Solar)? Hmm, in 1.4: MoonLordCore=398, Cultist... Towers: NPCID IDs 422? I recall TowerVortex etc. The code references NPC.ShieldStrengthTowerVortex etc. for type 422 → yes towers. Extra: glow afterimages + force field shield (Perlin noise texture with ForceField shader).
33. 23848-23890: case 402 (Moon Lord Core). Draws oldPos trail using Npc[403]/Npc[404] textures (Moon Lord's eye trails? 403/404 = MoonLordFreeEye / MoonLordHand?) Actually 402 = MoonLordCore, 403 = MoonLordHand, 404 = MoonLordFreeEye? Hmm reversed. It draws alternating segments along oldPos plus GlowMask[133]/[134]/[135] + DrawPrettyStarSparkle. Extra: long trail.
34. 23891-23913: case 519 (Martian probe? no. 519 = "Empress"? draws pink oldPos afterimages fading). Extra: trail.
35. 23914-23936: case 522 (Solar/?? draws oldPos white afterimages shrinking + Extra[57] overlay). Extra: afterimage trail.
36. 23937-24120: cases 370/372/373 (Duke Fishron 370, Sharkron 372/373). oldPos afterimages + radial orbiting copies (ai[0] states 3/8/4/9/12) + when type 370 and ai[0]>=4 draws TextureAssets.DukeFishron (enraged glow texture) overlay with yellow tint afterimages. Extra: trails + enraged glow skin.
37. 24121-24201: cases 439/440 (?? these draw Extra[30] (2-frame) with oldPos ghost + ai[0]==5 radial copies). 439/440 = ? maybe "SolarCultist"? no. They could be "NebulaHead"? Hmm. Let me check names.
38. 24202-24229: cases 392-395 (Moon lord parts: 392=MoonLordHead, 393=MoonLordHand, 394=MoonLordFreeEye, 395=MoonLordCore?). Draw GlowMask[48]/[49]/[50] overlays. Extra: glow mask.
39. 24230-24234: cases 83/84/179 — plain body, exclude.
40. 24235-24258: cases 87-92 — plain, exclude.
41. 24263-24324: case 491 — draws many Extra parts: Extra[40] (1x4 anim), Extra[41] x5, Extra[42] x2, Extra[43] x2, Extra[44], Extra[45], plus Npc[492] frames x4 from ai[0..3] (chained slave NPCs). This is a composite multi-part NPC (some 1.4.4 boss?). Type 491 = ? Maybe "Deerclops"? no that's 668. 491 could be "QueenSlimeBoss"? no 657. Hmm 491... Empress is 636. 491 might be "Plantera"? no. Let me check NPCID.
42. 24325-24390: case 398 (Moon Lord? no 398 = ? draws Extra[16] body + Extra[13] legs x2 + Extra[14] hands x2 targeting type 397 NPCs). 398 = "MoonLord"? Hmm, MoonLord is 398. Wait — 398 with hands 397 (MoonLordHand). Yes: 398 = MoonLord (head?), 397 = MoonLordHand, 396 = MoonLordCore? Actually: 396=MoonLordCore, 397=MoonLordHand, 398=MoonLordHead, 399=MoonLordFreeEye... Hmm but 392-395 also referenced as MoonLordHead etc. Let me verify with NPCID file.
43. 24391-24448: case 397 (MoonLordHand) — draws Extra[15] (forearm) with IK-ish angle toward head, Extra[17]/Extra[19] (eye bits) or Extra[26] (charging frame) based on ai[0], localAI[0]/[1] ellipse offset.
44. 24449-24491: case 396 (MoonLordCore) — draws Extra[18] (heart), Extra[19] (eye), Extra[25] (anim, localAI[2]/7), Extra[29] (localAI[3]/5), Extra[26] when ai[0]<0 (charging), body.
45. 24492-24505: case 399 (MoonLordFreeEye) — body + Extra[19] eye at ellipse offset scaled by localAI[2].
46. 24506-24538: case 416 (Stardust cell? no. 416 draws GlowMask[156] + 4 velocity radial copies; aligns Bottom to NPC 415 (its parent)). 416 = ? Maybe "Solar"? Hmm. 415/416 pair.
47. 24539-24573: case 399 covered above (that's at 24539). Also case 399 draws Extra[27] x2 vertical beam trails colored by ai[0] state + GlowMask[100] + Extra[20] frame(ai[0]+1) + GlowMask[101]. Wait, careful: lines 24539-24573 labeled "case 399" is a second case 399? No — decompiled switch may have duplicate case labels in different switches. Looking at structure: `case 399:` at 24539 inside the nested switch — hmm but there's already `case 399` at 24492. Actually 24492 is `case 399:` and 24539 is also `case 399:`?? Let me re-read: 24492 "case 399" then 24506 "case 416" then 24539 "case 399". That can't be in the same switch. Probably the second is a different switch level (the decompiler nested). It doesn't matter much; both belong to type 399 handling. I'll treat 24492-24505 and 24539-24573 as type 399 parts (they're in different nested switches though...). Actually no — looking again: the inner switch at 24261 has cases 491, 398, 397, 396, 399, 416, then... 24539 "case 399" — hmm that appears after "case 416" block ending 24538. Two `case 399` in same switch would be a compile error. So likely one of them is `case 399:` inside a different switch — the decompiler output shows nested switches. Since the second block draws Extra[27] trails colored by ai[0] (green→red) plus Extra[20] — that's the MoonLordFreeEye laser charging. Hmm, but type 399 per NPCID = "Moon Lord Free Eye"? Its ai[0] 1/2 red = charging laser. Plausible that both blocks are type 399 but in different switch nesting (the first switch handles some types, then falls to another). Whatever — I'll report as type 399 (appearing twice).

Hmm wait, actually I bet the second one (24539) is `case 399` in the *outer* default switch (the one that also has case 94 at 24574). And the first (24492) is in the inner switch. Both are type 399 branches. Fine.

48. 24574-24588: case 94 (Eater of Souls? no — 94 = "Chaos Elemental"? It draws oldPos afterimages 1..5 step2 of own texture). Type 94 = "Elite...? " Hmm, 94 = "Fritz"? I'll check names.
49. 24592-24604: types 125-131, 139(ai[3]==0), 140 — oldPos afterimages (10→0 step 2). Mechanical boss part trails.
50. 24605-24617: type 417 && ai[0]==6 — oldPos afterimages with scaling/oldRot.
51. 24618-24640: type 419 && ai[2]<=-9 — GlowMask[154] trail with frame cycling (frames 5-7) along oldPos.
52. 24641-24672: type 418 && ai[0] in {2,4} — Extra[55] fire trail (4 frames, colored gold→orange→blue), rotation -PI/2*spriteDirection, along oldPos.
53. 24673-24695: type 516 — own texture afterimage trail with frame offset cycling.
54. 24696-24703: type 390 && IsABestiaryIconDummy — draws Npc[391] (companion) beside body.
55. 24709-24726: types 420/421/423/424 — 4 radial orbiting copies (Teal) of own texture with pulsing radius.
56. 24727-24744: type 662 — velocity trail (8 copies behind) + 4 radial cyan copies.
57. 24746-24749: aiStyle==7 → DrawNPCExtras(beforeDraw:true) — town NPC pre-draw extras.
58. 24750-24753: type 346 && life<50% — draws TextureAssets.SantaTank instead of body (Santa-NK1 tank mode). Hmm — that's replacing body, not extra. But it draws SantaTank texture at the body position — a different texture than Npc[346]. It's a "tank mode" alternate body. I'd count it as extra part (SantaTank is a separate texture asset). Include with note.
59. 24799-24843: type 266 && life<lifeMax && (expert||getGood) — 4 mirror copies around the player (Paladin? no 266 = Cultist? Hmm 266 = "Ancient Cultist"? no, 266 is... The mirroring around player is the Lunatic Cultist's clone mechanic but with player-based mirroring? Actually it mirrors positions around player center — that's the "Solar Pillar"? Hmm. 266 = "CultistBoss"? I'll check names. Whatever: 4 mirrored copies.
60. 24844-24853: type 421 && ai[0]==5 — draws body + GlowMask[146] at the *player's* head position (riding on player?). Interesting: draws at player Top/Bottom. Extra.
61. 24858-24866: case 518 — body draw with shifted origin; no extra (exclude, though GlowMask[163] comes later).
62. 24868-24903: cases 676/681 — RainbowTownSlime shader (pure shader, exclude).
63. 24904-24939: case 685 — squash/stretch scale modulation + pixel snap (exclude — pure transform).
64. 24940-24949: case 267 — plain, exclude.
65. 24951-24976: aiStyle==7 && ai[0]==25 (town NPC sleeping? no, ai[0]==25 is the "shimmered/town NPC transformed"? It applies ColorOnlyShader + 6 rainbow orbiting copies + 2 DrawPrettyStarSparkle). Extra: rainbow orbiting copies + sparkles.
66. 24995-25003: type 695 && ai[0]==2 — emote bubble (extra? it's an emote, minor). Could include briefly.
67. 25004-25007: confused → Confuse icon (general, not per-type; borderline "buff icon" — exclude or mention). Probably exclude since it's a buff overlay for all NPCs, not a per-type special.
68. 25008-25043: types 247/248 (Golem head/fists?) — ai[0]==1: 3 scale-pulsing white copies; ai[0]==2: 3 velocity-trail copies + 3 scale-pulsing. Extra.
69. 25044-25047: type 24 — GlowMask[360] overlay. Flat glow.
70. 25048-25055: types 639-645 → GlowMask[286]; 646-652 → GlowMask[287]. Flat glow overlays.
71. 25056-25059: types 134-136 → TextureAssets.Dest[type-134] overlay.  Flat overlay (dest = "destroyed" mode textures? Dest[0..2]).
72. 25060-25063: type 125 → EyeLaser overlay. Extra part (eye laser glow).
73. 25064-25067: type 139 → Probe overlay.
74. 25068-25120: type 127 — if IsMechQueenUp: draws Chain12 chains connecting to types 125/126 from MechQueen anchor points; else BoneEyes overlay.
75. 25121-25124: type 131 → BoneLaser overlay.
76. 25125-25139: type 120 (Demon Eye? no — draws TextureAssets.Chaos along oldPos as trail). Type 120 = "DemonEye2"? Chaos texture = "Chaos" asset. Probably the "Red Devil"? no. I'll name by texture.
77. 25140-25154: types 137/138 — oldPos shimmer afterimages.
78. 25155-25164: type 327 — PumpkingFace overlay + 9 jitter copies (flame flicker).
79. 25165-25174: type 325 — TreeFace overlay (Mourning Wood? no 325 = "Splinterling"? Tree 1? Actually 325 = "Splinterling"? Hmm — TreeFace: likely "Splinterling"/"Mourningwood"? I'll check names) + 9 jitter copies.
80. 25175-25182: type 345 (Ice Queen) — IceQueen overlay + 4 velocity afterimages.
81. 25183-25186: type 355 — Firefly overlay (glow). Flat glow.
82. 25187-25190: type 358 — Lightningbug overlay. Flat glow.
83. 25191-25198: type 654 → GlowMask[290]; 653 → GlowMask[288]. Flat glow.
84. 25199-25206: type 82 (Wraith) — WraithEye overlay + 9 velocity afterimages.
85. 25207-25214: type 253 (Reaper) — ReaperEye overlay + 19 afterimages.
86. 25215-25218: type 245 && alpha==0 && !getGoodWorld — Golem[3] overlay (golem head eyes?). 
87. 25219-25240: type 246 — Golem[1]/Golem[2] fist overlay at fixed offsets (left/right) depending on frame, + Extra[107].
88. 25241-25257: type 249 — Golem[1] + Extra[106] (anim 8 frames) + Extra[107].
89. 25258-25266: type 383 — GlowMask[11] overlay + Npc[384] drawn semi-transparent if ai[2] linked (parent ghost). Extra.
90. 25267-25344: type 381 — Extra[0] (32x42 frame selected by ai[2]) + GlowMask[24], positioned per body frame offsets (9-frame table). This is like a shield/arm. 
91. 25345-25421: type 382 — Extra[1] similar.
92. 25422-25444: type 520 — GlowMask[164] overlay + Extra[56] rotated by localAI[3] + GlowMask[165]. 
93. 25445-25468: types 386/387/388/389 — GlowMask[31]/[32]/[33]/[34] overlays (flat glow; 387 with ai[0] fade).
94. 25469-25481: type 4 && ai[1]>=4 && ai[0]==3 (Eye of Cthulhu spin) — oldPos afterimages.
95. 25482-25488: type 437 — GlowMask[109] (framed) + GlowMask[108] (unframed) overlays.
96. 25489-25501: type 471 && ai[3]<0 — oldPos afterimages.
97. 25502-25521: type 477 && velocity>9 — oldPos afterimages with frame offset.
98. 25522-25541: type 479 && velocity>6.5 — oldPos afterimages with frame offset. (note: this is `if ... else if (type==472)` chain)
99. 25542-25545: type 472 — GlowMask[110] overlay.
100. 25546-25562: aiStyle==87 && ai[0] in {4,5,6} — oldPos shimmer afterimages.
101. 25567-25596: case 50 — Extra[39] crown overlay (King Slime crown at head, frame-dependent Y offset). 
102. 25597-25789: glow mask overlays: 411→156? no: 411→GlowMask[136], 409→[138], 410→[137], 407→[139], 405→[141], 406→[142], 424→[144], 423→[145], 421→[146], 420→[147], 425→[150]+DrawPrettyStarSparkle green, 429→[151], 418→[161]+4 velocity copies, 412/413/414→GlowMask[157+type-412] (with 414 localAI[2] tint), 415→[155]+4 velocity copies, 419→[154]+4 velocity copies (or 4 unit-x copies), 417→[160]+4 velocity copies, 516→own texture + 4 velocity copies, 518→GlowMask[163]+4 velocity copies, 344→[253], 346→[254] +4 radial, 315→[255]+4 radial, 525→[169], 526→[170], 527→[171], 533→[172], 160→[166]/[352] (variant), 209→[167]/[350]/[351] (variant).
103. 25791-25794: aiStyle==7 → DrawNPCExtras(beforeDraw:false).
104. 25803-26207: the big "case 426/427/428/521/523/541-545/552-563/566-575/578/581/618/620/646/558-560/574/575" branch — afterimage/trail system with per-type configs + extras: 426/427 glow masks [152]/[153]; 541 GlowMask[216] orbiting gold copies; 661 rainbow orbiting; 568/569 GlowMask[224] + Extra[89] ring of 16 rotating beams; 546 Extra[76] overlay; 566/567 (localAI[3]>=115) Extra[80] 4-frame anim above head (crown? "status"?); 618 Extra[59] radial swirls during ai[0]==3 and Extra[129] overlay.

Also within that: types 558-560/574/575 ai[0]==2 trail; 427 trail num294=8; 546; 542-545; 581; 521; 523 radial orbit; 620; 618.

Also 26098-26114: type 661 rainbow orbit.
26115-26155: 568/569 localAI[3]>=60 → GlowMask[224] + Extra[89] 16-beam ring rotating by localAI[0].

Also DrawNPCDirect_HallowBoss (636) draws Extra[157..160] arms/wings — delegate (26364-26551).
DrawNPCDirect_Faeling (677) — trail.
DrawNPCDirect_Deerclops (668).
DrawNPCDirect_QueenSlimeWings (22318-22348) — Extra[185] wings, 2 sides, localAI[3] frame, rotation.

Also DrawNPC_SlimeItem (26709) — item inside slime.

Now, to name NPC types, let me check if NPCID.cs exists with comments/names.

Given the volume, I should be pragmatic: give type IDs plus texture names, and NPC names where I'm confident. Let me check the decompiled source for NPCID or Lang names to name types. Let me grep.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:16:10.199Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ | head -50; ls ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ID/ 2>/dev/null | head",
 "description": "List decompiled source files"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:16:10.225Z

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

```


---

## 🤖 Assistant · 2026-08-11T07:16:12.548Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
No ID folder. NPC names can be derived from Lang displayNames maybe not present. Let me check if there's NPCID list elsewhere in the project (game dir ~/Project/GLM/SandboxWorld/game).
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:16:13.167Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld -iname \"*NPCID*\" -not -path \"*/node_modules/*\" 2>/dev/null | head; grep -rln \"GolemHead\" ~/Project/GLM/SandboxWorld --include=*.cs 2>/dev/null | head",
 "description": "Search for NPCID definitions in project"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:16:13.238Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1405/ID/NPCID.cs
~/Project/GLM/SandboxWorld/Terarria1456Server/Terraria.ID/NPCID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/NPCID.cs
~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit/Converters/NpcIdToPreviewConverter.cs
(eval):1: no matches found: --include=*.cs

```


---

## 🤖 Assistant · 2026-08-11T07:16:17.470Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -nE \"public const short (MoonLord|CultistBoss|DukeFishron|Betsy|Ogre|EmpressOfLight|QueenSlimeBoss|Deerclops|Golem|Plantera|Pumpking|KingSlime|MoonLordCore|MoonLordHead|MoonLordHand|MoonLordFreeEye|LunarTower|SolarCultist|Cultist|WindyBalloon|Fairy|Faeling|TownSlime|Slime|Illuminant|Chaos|CultistTablet|AncientLight|AncientDoom|CultistProject|Skeleton|Skeletron|SkeletronPrime|Prime|Retinazer|Spazmatism|TheDestroyer|Eater|Creeper|Servant|GolemFist|GolemHead|PlanterasHook|PlanterasTentacle|FlyingSnake|Lihzahrd|ManEater|Snatcher|WallCreeper|BloodCrawler|BlackRecluse|WallCreep|CaveBat|IceQueen|SantaNK1|SantaNK2|Everscream|IceQueen|PumpkingBlade|PumpkingHead|Pumpking|MourningWood|Splinterling|HellArmoredBones) \" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/NPCID.cs | head -80",
 "description": "Look up NPC type ID constants"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:16:17.500Z

**📎 ToolResult**

```
11107:	public const short Skeleton = 21;
11151:	public const short ManEater = 43;
11163:	public const short CaveBat = 49;
11165:	public const short KingSlime = 50;
11177:	public const short Snatcher = 56;
11315:	public const short Retinazer = 125;
11317:	public const short Spazmatism = 126;
11319:	public const short SkeletronPrime = 127;
11333:	public const short TheDestroyer = 134;
11391:	public const short BlackRecluse = 163;
11393:	public const short WallCreeper = 164;
11461:	public const short Lihzahrd = 198;
11517:	public const short FlyingSnake = 226;
11543:	public const short BloodCrawler = 239;
11555:	public const short Golem = 245;
11557:	public const short GolemHead = 246;
11589:	public const short Plantera = 262;
11591:	public const short PlanterasHook = 263;
11593:	public const short PlanterasTentacle = 264;
11599:	public const short Creeper = 267;
11619:	public const short HellArmoredBones = 277;
11715:	public const short MourningWood = 325;
11717:	public const short Splinterling = 326;
11719:	public const short Pumpking = 327;
11721:	public const short PumpkingBlade = 328;
11753:	public const short Everscream = 344;
11755:	public const short IceQueen = 345;
11757:	public const short SantaNK1 = 346;
11805:	public const short DukeFishron = 370;
11857:	public const short MoonLordHead = 396;
11859:	public const short MoonLordHand = 397;
11861:	public const short MoonLordCore = 398;
11865:	public const short MoonLordFreeEye = 400;
11937:	public const short CultistTablet = 437;
11941:	public const short CultistBoss = 439;
12109:	public const short AncientLight = 522;
12111:	public const short AncientDoom = 523;
12253:	public const short WindyBalloon = 594;
12379:	public const short QueenSlimeBoss = 657;
12401:	public const short Deerclops = 668;

```


---

## 🤖 Assistant · 2026-08-11T07:16:24.686Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Wait, MoonLordHead = 396, MoonLordHand = 397, MoonLordCore = 398, MoonLordFreeEye = 400. But the code had case 396 drawing Extra[18] (heart?) + Extra[19]... and 399 drawing laser stuff. 399 must be "MoonLordLeech"? Hmm. Let me get full mapping of the specific IDs I need. Let me grep the NPCID.cs for the specific numbers with names. Easier: print lines with their constant names and check each ID I care about: 4, 24, 36, 50, 56, 69, 71, 82, 94, 101, 120, 124, 125-131, 134-140, 160, 175, 179, 182, 209, 226?, 239, 245-249, 253, 259, 260, 263, 264, 266, 267, 277-280, 288, 289, 315, 325, 327, 328, 344-346, 355, 356, 358, 370-373, 381-390, 392-400, 402, 405-407, 409-414, 415-421, 422-429, 437, 439, 440, 454-459, 466-479, 491-493, 507, 516-526, 533, 537, 541-549, 551, 552-575, 576-578, 581, 594, 612, 620, 621-627, 636, 639-657, 661, 662, 668, 676, 677, 681, 683-696.

Rather than grep each, dump the NPCID.cs region and map. The file is huge (id list). Let me write a small python to parse const shorts into dict and print names for my list of IDs. But that's fine to run read-only (no file writes).

Let me run python3 with inline -c reading the file.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:16:29.661Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 -c \"\nimport re\nd={}\nfor m in re.finditer(r'public const short (\\w+) = (\\d+);', open('~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/NPCID.cs').read()):\n    d[int(m.group(2))]=m.group(1)\nids=[1,4,24,36,50,56,69,71,82,94,101,120,124,125,126,127,128,129,130,131,134,135,136,137,138,139,140,160,175,245,246,247,248,249,253,259,260,263,264,266,267,288,315,325,327,328,344,345,346,355,356,358,370,372,373,381,382,383,384,386,387,388,389,390,392,393,394,395,396,397,398,399,400,402,405,406,407,409,410,411,412,413,414,415,416,417,418,419,420,421,422,423,424,425,426,427,428,429,437,439,440,454,455,456,457,458,459,471,472,477,478,479,483,490,491,492,493,507,516,517,518,519,520,521,522,523,525,526,527,533,541,542,543,544,545,546,551,552,553,554,555,556,557,558,559,560,561,562,563,564,565,566,567,568,569,570,571,572,573,574,575,576,577,578,581,594,618,620,621,622,623,625,626,627,636,639,640,641,642,643,644,645,646,647,648,649,650,651,652,653,654,655,657,661,662,668,676,677,681,685,686,690,692,693,694,695,696]\nfor i in ids: print(i, d.get(i,'?'))\n\"",
 "description": "Map NPC type IDs to names"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:16:37.970Z

**📎 ToolResult**

```
1 BlueSlime
4 EyeofCthulhu
24 FireImp
36 SkeletronHand
50 KingSlime
56 Snatcher
69 Antlion
71 DungeonSlime
82 Wraith
94 Corruptor
101 Clinger
120 ChaosElemental
124 Mechanic
125 Retinazer
126 Spazmatism
127 SkeletronPrime
128 PrimeCannon
129 PrimeSaw
130 PrimeVice
131 PrimeLaser
134 TheDestroyer
135 TheDestroyerBody
136 TheDestroyerTail
137 IlluminantBat
138 IlluminantSlime
139 Probe
140 PossessedArmor
160 Truffle
175 AngryTrapper
245 Golem
246 GolemHead
247 GolemFistLeft
248 GolemFistRight
249 GolemHeadFree
253 Reaper
259 FungiBulb
260 GiantFungiBulb
263 PlanterasHook
264 PlanterasTentacle
266 BrainofCthulhu
267 Creeper
288 DungeonSpirit
315 HeadlessHorseman
325 MourningWood
327 Pumpking
328 PumpkingBlade
344 Everscream
345 IceQueen
346 SantaNK1
355 Firefly
356 Butterfly
358 LightningBug
370 DukeFishron
372 Sharkron
373 Sharkron2
381 BrainScrambler
382 RayGunner
383 MartianOfficer
384 ForceBubble
386 MartianEngineer
387 MartianTurret
388 MartianDrone
389 GigaZapper
390 ScutlixRider
392 MartianSaucer
393 MartianSaucerTurret
394 MartianSaucerCannon
395 MartianSaucerCore
396 MoonLordHead
397 MoonLordHand
398 MoonLordCore
399 MartianProbe
400 MoonLordFreeEye
402 StardustWormHead
405 StardustCellBig
406 StardustCellSmall
407 StardustJellyfishBig
409 StardustSpiderBig
410 StardustSpiderSmall
411 StardustSoldier
412 SolarCrawltipedeHead
413 SolarCrawltipedeBody
414 SolarCrawltipedeTail
415 SolarDrakomire
416 SolarDrakomireRider
417 SolarSroller
418 SolarCorite
419 SolarSolenian
420 NebulaBrain
421 NebulaHeadcrab
422 LunarTowerVortex
423 NebulaBeast
424 NebulaSoldier
425 VortexRifleman
426 VortexHornetQueen
427 VortexHornet
428 VortexLarva
429 VortexSoldier
437 CultistTablet
439 CultistBoss
440 CultistBossClone
454 CultistDragonHead
455 CultistDragonBody1
456 CultistDragonBody2
457 CultistDragonBody3
458 CultistDragonBody4
459 CultistDragonTail
471 GoblinSummoner
472 ShadowFlameApparition
477 Mothron
478 MothronEgg
479 MothronSpawn
483 GraniteFlyer
490 Drippler
491 PirateShip
492 PirateShipCannon
493 LunarTowerStardust
507 LunarTowerNebula
516 SolarFlare
517 LunarTowerSolar
518 SolarSpearman
519 SolarGoop
520 MartianWalker
521 AncientCultistSquidhead
522 AncientLight
523 AncientDoom
525 DesertGhoulCorruption
526 DesertGhoulCrimson
527 DesertGhoulHallow
533 DesertDjinn
541 SandElemental
542 SandShark
543 SandsharkCorrupt
544 SandsharkCrimson
545 SandsharkHallow
546 Tumbleweed
551 DD2Betsy
552 DD2GoblinT1
553 DD2GoblinT2
554 DD2GoblinT3
555 DD2GoblinBomberT1
556 DD2GoblinBomberT2
557 DD2GoblinBomberT3
558 DD2WyvernT1
559 DD2WyvernT2
560 DD2WyvernT3
561 DD2JavelinstT1
562 DD2JavelinstT2
563 DD2JavelinstT3
564 DD2DarkMageT1
565 DD2DarkMageT3
566 DD2SkeletonT1
567 DD2SkeletonT3
568 DD2WitherBeastT2
569 DD2WitherBeastT3
570 DD2DrakinT2
571 DD2DrakinT3
572 DD2KoboldWalkerT2
573 DD2KoboldWalkerT3
574 DD2KoboldFlyerT2
575 DD2KoboldFlyerT3
576 DD2OgreT2
577 DD2OgreT3
578 DD2LightningBugT3
581 FlyingAntlion
594 WindyBalloon
618 BloodNautilus
620 GoblinShark
621 BloodEelHead
622 BloodEelBody
623 BloodEelTail
625 SeaTurtle
626 Seahorse
627 GoldSeahorse
636 HallowBoss
639 GemSquirrelAmethyst
640 GemSquirrelTopaz
641 GemSquirrelSapphire
642 GemSquirrelEmerald
643 GemSquirrelRuby
644 GemSquirrelDiamond
645 GemSquirrelAmber
646 GemBunnyAmethyst
647 GemBunnyTopaz
648 GemBunnySapphire
649 GemBunnyEmerald
650 GemBunnyRuby
651 GemBunnyDiamond
652 GemBunnyAmber
653 HellButterfly
654 Lavafly
655 MagmaSnail
657 QueenSlimeBoss
661 EmpressButterfly
662 PirateGhost
668 Deerclops
676 ShimmerSlime
677 Shimmerfly
681 TownSlimeRainbow
685 BoundTownSlimeOld
686 BoundTownSlimePurple
690 StatueMimic
692 Orca
693 LibrarianSkeleton
694 WaterBoltMimic
695 PalworldCattivaDistressed
696 PalworldFoxsparksDistressed

```


---

## 🤖 Assistant · 2026-08-11T07:16:51.949Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting — this is a modified decompile? "PalworldCattivaDistressed" — the source tree seems to be modded/1.4.5 custom. Anyway names map.

Wait — 695/696 are Palworld creatures (this seems to be a modded version, "SandboxWorld"). OK.

Note: DrawNPCDirect case 686 = BoundTownSlimePurple? Hmm the switch said case 686 draws full texture. Fine.

Some corrections:
- case 398 in the switch (line 24325) = MoonLordCore? But MoonLordCore=398. It draws Extra[13]/[14]/[16] with hands tracked via type 397 (MoonLordHand). Yes: MoonLordCore draws its heart + hands? Hmm actually the code at 24325 draws hands (Extra[14]) targeting NPC type 397 and legs/heart Extra[13], body Extra[16]. Fine — MoonLordCore.
- case 396 at 24449 = MoonLordHead: draws Extra[18] (brow), Extra[19] (eye), Extra[25], Extra[29], Extra[26]. Good.
- case 400 at 24492 = MoonLordFreeEye: draws Extra[19] (eye) ellipse offset by localAI[0..2].
- case 399 at 24539 = MartianProbe: draws Extra[27] twin green/red light trails + GlowMask[100] + Extra[20] (4-frame, ai[0]+1) + GlowMask[101]. 
- case 392-395 = MartianSaucer family: GlowMask[48] (saucer), [49] (core 395), [50] (cannon 394).
- case 402 = StardustWormHead: trail of Npc[403]/Npc[404]? Wait 403/404 would be StardustWormBody/Tail? Those weren't in my list. IDs 403=StardustWormBody? Probably. It alternates textures for the trail.
- case 416 = SolarDrakomireRider: GlowMask[156] + 4 velocity copies; snaps to parent 415 (SolarDrakomire).
- case 491 = PirateShip: draws Extra[40..45] (masts, cannons, etc.) + Npc[492] (PirateShipCannon) frames per ai[0..3]. 
- case 594 = WindyBalloon: draws carried slime.
- type 693 = LibrarianSkeleton: Extra[289] swirl at Top.
- type 690 = StatueMimic: draws Tile[105] grid — mimic disguised as a statue (tile 105 = Statue tile). Yes! Mimic disguised as statue.
- type 696 = PalworldFoxsparksDistressed: jitter overlay (second frame row drawn with random offsets).
- type 695 = PalworldCattivaDistressed: emote bubble.
- case 686 = BoundTownSlimePurple — plain.

Hmm wait, case 696's second frame-row overlay — "Static jitter" is an extra draw of the same texture with a different frame, drawn on top — counts as an effect overlay. Borderline. I'll include as extra.

- case 551 = DD2Betsy: wings Extra[81]/[82] + afterimages.
- case 549 wasn't in my list. It's at 23642-23721 (case 549). 549 = ? Let me get. Probably "DD2OgreT1"? no that's 576/577. Let me query 549. Also 467, 490 (Drippler), 484 etc. And 537, 466-470, 480-489, 494-506, 508-515, 528-532... Only needed: 549, plus 467/490/553 etc. Let me query 549.

Also case 548 at 23497 — 548 = ? Query. And case 564/565 = DD2DarkMageT1/T3. 546 = Tumbleweed (Extra[76] overlay = grass?). 566/567 = Skeleton T1/T3 with Extra[80] when localAI[3]>=115 — probably a "crown"/helmet? Extra[80] 4-frame at head offset — likely the skeleton's glowing eyes or helmet. I'll describe neutrally.

Let me query 546,548,549,551 plus 266 (Brain of Cthulhu — mirror copies), 4 (EyeofCthulhu), etc. Already have most. Need: 548, 549. And 553-560 done. Also 612/613? not needed.

Let me query 548, 549, 550.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:16:52.852Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 -c \"\nimport re\nd={}\nfor m in re.finditer(r'public const short (\\w+) = (\\d+);', open('~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/NPCID.cs').read()):\n    d[int(m.group(2))]=m.group(1)\nfor i in [548,549,550,403,404,467,537,581,612,613,625,662]: print(i, d.get(i,'?'))\n\"",
 "description": "Look up remaining NPC IDs"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:16:56.788Z

**📎 ToolResult**

```
548 DD2EterniaCrystal
549 DD2LanePortal
550 DD2Bartender
403 StardustWormBody
404 StardustWormTail
467 DeadlySphere
537 SandSlime
581 FlyingAntlion
612 WaterStrider
613 GoldWaterStrider
625 SeaTurtle
662 PirateGhost

```


---

## 🤖 Assistant · 2026-08-11T07:17:00.872Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have everything. Let me also double-check the region before 22159 (e.g., anything NPC-extra related just before DrawNPCs) and confirm nothing after 26209 within DrawNPCDirect (method ends at 26209). Also check DrawNPC_SlimeItem briefly (26709) to describe.

Also check the top part of DrawNPCDirect between 22350-22391 (nameOver logic — exclude) and confirm there are no extra-draw branches between 22741 and 22798 (npcColor stuff — exclude) — correct.

Also 22845 DrawNPC_SlimeItem call. And NPCAddHeight offsets — exclude (positional only).

Let me quickly view DrawNPC_SlimeItem (26709-26760ish) to describe it.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:17:01.090Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "limit": 60,
 "offset": 26709
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:17:01.099Z

**📎 ToolResult**

```
26709		private static void DrawNPC_SlimeItem(NPC rCurrentNPC, int typeCache, Microsoft.Xna.Framework.Color npcColor, float addedRotation)
26710		{
26711			int num = (int)rCurrentNPC.ai[1];
26712			float num2 = 1f;
26713			float num3 = 22f * rCurrentNPC.scale;
26714			float num4 = 18f * rCurrentNPC.scale;
26715			GetItemDrawFrame(num, out var itemTexture, out var rectangle);
26716			float num5 = rectangle.Width;
26717			float num6 = rectangle.Height;
26718			bool num7 = (int)rCurrentNPC.ai[0] == -999;
26719			if (num7)
26720			{
26721				num3 = 14f * rCurrentNPC.scale;
26722				num4 = 14f * rCurrentNPC.scale;
26723			}
26724			if (num5 > num3)
26725			{
26726				num2 *= num3 / num5;
26727				num5 *= num2;
26728				num6 *= num2;
26729			}
26730			if (num6 > num4)
26731			{
26732				num2 *= num4 / num6;
26733				num5 *= num2;
26734				num6 *= num2;
26735			}
26736			float num8 = -1f;
26737			float num9 = 1f;
26738			int num10 = rCurrentNPC.frame.Y / (TextureAssets.Npc[typeCache].Height() / npcFrameCount[typeCache]);
26739			float num11 = 0.2f;
26740			if (rCurrentNPC.type == 537)
26741			{
26742				num11 = 0f;
26743				num10 = 0;
26744				num9 += 4f;
26745			}
26746			num9 -= (float)num10;
26747			num8 += (float)(num10 * 2);
26748			num11 -= 0.3f * (float)num10;
26749			if (num7)
26750			{
26751				if (rCurrentNPC.velocity.X < 0f)
26752				{
26753					num11 *= -1f;
26754				}
26755				num9 -= 6f;
26756				if ((double)num2 >= 0.8)
26757				{
26758					num9 -= 1f;
26759				}
26760				if (num2 >= 1f)
26761				{
26762					num9 -= 3f;
26763				}
26764				if (num != 1345)
26765				{
26766					addedRotation = ((!(addedRotation < 0f)) ? (addedRotation * 4.5f) : (addedRotation * 5.5f));
26767				}
26768				else

```


---

## 🤖 Assistant · 2026-08-11T07:17:03.797Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good enough. Now check DrawNPCExtras remainder (27001-27100ish) for other extras like Christmas hats etc. Let me skim quickly to summarize what extras it draws (party hat, and what beforeDraw=true does). Let me read 27001-27200.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:17:04.034Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "limit": 180,
 "offset": 27001
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:17:04.040Z

**📎 ToolResult**

```
27001				if (n.type == 229 && n.ai[0] == 12f)
27002				{
27003					vector.X -= num5 * 4;
27004				}
27005				if (n.type == 550 && n.ai[0] == 5f)
27006				{
27007					vector.X += num5 * 7;
27008				}
27009				Vector2 origin = rectangle.Size() - new Vector2(rectangle.Width / 2, 12f);
27010				int num7 = 0;
27011				switch (n.type)
27012				{
27013				case 550:
27014					num7 = -4;
27015					break;
27016				case 588:
27017					num7 = 0;
27018					break;
27019				case 227:
27020					num7 = -4;
27021					break;
27022				case 228:
27023				case 678:
27024				case 681:
27025				case 682:
27026					num7 = -2;
27027					break;
27028				case 17:
27029				case 18:
27030				case 19:
27031				case 20:
27032				case 22:
27033				case 124:
27034				case 229:
27035				case 353:
27036				case 633:
27037				case 637:
27038				case 638:
27039				case 656:
27040				case 670:
27041				case 679:
27042				case 680:
27043				case 683:
27044				case 684:
27045					num7 = -1;
27046					break;
27047				case 37:
27048				case 38:
27049				case 54:
27050				case 107:
27051				case 108:
27052				case 160:
27053				case 207:
27054				case 209:
27055					num7 = -3;
27056					break;
27057				case 178:
27058				case 208:
27059				case 369:
27060					num7 = 1;
27061					break;
27062				}
27063				vector.X += num7 * num5;
27064				vector.X += 4 * num5;
27065				vector *= n.scale;
27066				bottom += vector;
27067				SpriteEffects spriteEffects = npcSpriteEffect;
27068				if (NPCID.Sets.IsTownSlime[n.type])
27069				{
27070					spriteEffects ^= SpriteEffects.FlipHorizontally;
27071				}
27072				float num8 = 1f;
27073				if (n.shimmerTransparency > 0f)
27074				{
27075					num8 *= 1f - n.shimmerTransparency;
27076				}
27077				if (n.IsAPortraitDummy)
27078				{
27079					if (n.scale == 2f)
27080					{
27081						bottom.Y -= 4f;
27082					}
27083					if (n.scale == 3f)
27084					{
27085						bottom.Y -= 8f;
27086					}
27087				}
27088				bottom -= screenPosition;
27089				spriteBatch.Draw(value, bottom, rectangle, npcColor * n.Opacity * num8, 0f, origin, n.scale, spriteEffects, 0f);
27090			}
27091			if (!beforeDraw && n.type == 681)
27092			{
27093				spriteBatch.Draw(TextureAssets.Extra[250].Value, new Vector2(n.position.X - screenPosition.X + (float)(n.width / 2) - (float)TextureAssets.Npc[n.type].Width() * n.scale / 2f + halfSize.X * n.scale, n.position.Y - screenPosition.Y + (float)n.height - (float)TextureAssets.Npc[n.type].Height() * n.scale / (float)npcFrameCount[n.type] + 4f + halfSize.Y * n.scale + addHeight + addY + n.gfxOffY), n.frame, n.GetAlpha(npcColor), n.rotation, halfSize, n.scale, npcSpriteEffect, 0f);
27094			}
27095			if (NPCID.Sets.AttackType[n.type] == 1 && n.ai[0] == 12f && !beforeDraw)
27096			{
27097				if (n.type == 228 || n.type == 229 || n.type == 209)
27098				{
27099					return;
27100				}
27101				float num9 = n.ai[2];
27102				Vector2 vector2 = OffsetsNPCOffhand[2];
27103				if (n.spriteDirection == 1)
27104				{
27105					vector2.X *= -1f;
27106				}
27107				Vector2 vector3 = n.Bottom - vector2;
27108				if (n.type == 22 && n.ai[2] > -0.1f)
27109				{
27110					vector3.Y += 4f;
27111				}
27112				if (n.type == 368 && hardMode && n.ai[2] > -0.1f)
27113				{
27114					vector3.Y += 4f;
27115				}
27116				if (n.type == 368 && !hardMode && n.ai[2] < -0.1f)
27117				{
27118					vector3.Y -= 8f;
27119				}
27120				float rotation = num9 * (MathF.PI / 2f) * (float)n.spriteDirection;
27121				float num10 = 1f;
27122				int itemtype = 0;
27123				int num11 = 4;
27124				if (n.type == 19)
27125				{
27126					itemtype = (hardMode ? 98 : 95);
27127					if (hardMode)
27128					{
27129						vector3.X -= 10 * n.direction;
27130						vector3.Y += 4f;
27131					}
27132				}
27133				else if (n.type == 22)
27134				{
27135					itemtype = 39;
27136					num11 = 18;
27137				}
27138				else if (n.type == 178)
27139				{
27140					itemtype = 434;
27141				}
27142				else if (n.type == 227)
27143				{
27144					itemtype = 3350;
27145					num11 = 16;
27146					num10 = 0.85f;
27147				}
27148				else if (n.type == 368)
27149				{
27150					itemtype = (hardMode ? 2223 : 2269);
27151					if (hardMode)
27152					{
27153						num11 = 18;
27154					}
27155					else
27156					{
27157						if (n.ai[2] < -0.1f)
27158						{
27159							num11 = 28;
27160						}
27161						num10 = 0.75f;
27162					}
27163				}
27164				Vector2 vector4 = DrawPlayerItemPos(1f, itemtype);
27165				GetItemDrawFrame(itemtype, out var itemTexture, out var value2);
27166				int num12 = (int)vector4.X - num11;
27167				Vector2 origin2 = new Vector2(-num12, value2.Height / 2);
27168				if (n.spriteDirection == -1)
27169				{
27170					origin2 = new Vector2(value2.Width + num12, value2.Height / 2);
27171				}
27172				spriteBatch.Draw(itemTexture, new Vector2((int)(vector3.X - screenPosition.X), (int)(vector3.Y - screenPosition.Y)), value2, npcColor, rotation, origin2, n.scale * num10, npcSpriteEffect ^ SpriteEffects.FlipHorizontally, 0f);
27173				if (n.type == 22 && n.frame.Y / (TextureAssets.Npc[n.type].Height() / npcFrameCount[n.type]) >= 21)
27174				{
27175					Texture2D value3 = TextureAssets.Extra[52].Value;
27176					if (n.IsShimmerVariant)
27177					{
27178						value3 = TextureAssets.Extra[264].Value;
27179					}
27180					Microsoft.Xna.Framework.Rectangle value4 = value3.Frame(1, 5, 0, n.frame.Y / (TextureAssets.Npc[n.type].Height() / npcFrameCount[n.type]) - 21);

```


---

## 🤖 Assistant · 2026-08-11T07:17:06.934Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
DrawNPCExtras draws: party hat (Extra[72]), TownSlimeRainbow overlay (Extra[250] for type 681), held item in hand when attacking (ai[0]==12, AttackType==1), plus probably more below (held items for other attack types). That's enough summary.

Now, also the beforeDraw=true call at 24748 — what does DrawNPCExtras do when beforeDraw is true? Looking at the method: the party hat requires !beforeDraw; the item requires !beforeDraw. Let me check for beforeDraw-true-specific content. Let me grep within DrawNPCExtras for "beforeDraw".
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:17:07.337Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '26812,27330p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | grep -n \"beforeDraw\"",
 "description": "Find beforeDraw checks in DrawNPCExtras"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:17:07.370Z

**📎 ToolResult**

```
1:	protected void DrawNPCExtras(NPC n, bool beforeDraw, float addHeight, float addY, Microsoft.Xna.Framework.Color npcColor, Vector2 halfSize, SpriteEffects npcSpriteEffect, Vector2 screenPosition)
3:		if (!beforeDraw && n.UsesPartyHat())
280:		if (!beforeDraw && n.type == 681)
284:		if (NPCID.Sets.AttackType[n.type] == 1 && n.ai[0] == 12f && !beforeDraw)
383:		if (NPCID.Sets.AttackType[n.type] == 2 && (n.ai[0] == 14f || (n.ai[0] == 24f && n.frameCounter < 240.0)) && !beforeDraw)
401:				if (beforeDraw)
414:				if (!beforeDraw)
428:				if (!beforeDraw)
445:			if (beforeDraw)
488:		if (beforeDraw || n.ai[0] != 23f)

```


---

## 🤖 Assistant · 2026-08-11T07:17:09.498Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So beforeDraw=true does something around lines 26812+400 (=27212ish). Let me quickly read 27190-27300 to characterize.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:17:09.761Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "limit": 160,
 "offset": 27190
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:17:09.771Z

**📎 ToolResult**

```
27190					Microsoft.Xna.Framework.Rectangle value6 = value5.Frame(1, 5, 0, n.frame.Y / (TextureAssets.Npc[n.type].Height() / npcFrameCount[n.type]) - 21);
27191					spriteBatch.Draw(value5, new Vector2(n.position.X - screenPosition.X + (float)(n.width / 2) - (float)TextureAssets.Npc[n.type].Width() * n.scale / 2f + halfSize.X * n.scale, n.position.Y - screenPosition.Y + (float)n.height - (float)TextureAssets.Npc[n.type].Height() * n.scale / (float)npcFrameCount[n.type] + 4f + halfSize.Y * n.scale + addHeight + addY + n.gfxOffY), value6, n.GetAlpha(npcColor), n.rotation, halfSize, n.scale, npcSpriteEffect, 0f);
27192				}
27193			}
27194			if (NPCID.Sets.AttackType[n.type] == 2 && (n.ai[0] == 14f || (n.ai[0] == 24f && n.frameCounter < 240.0)) && !beforeDraw)
27195			{
27196				Texture2D value7 = TextureAssets.Extra[51].Value;
27197				Vector2 vector5 = n.Bottom + new Vector2(0f, n.gfxOffY + 4f);
27198				Microsoft.Xna.Framework.Rectangle rectangle2 = value7.Frame(1, 4, 0, (int)n.frameCounter % 48 / 12);
27199				Vector2 origin3 = rectangle2.Size() * new Vector2(0.5f, 1f);
27200				spriteBatch.Draw(value7, new Vector2((int)(vector5.X - screenPosition.X), (int)(vector5.Y - screenPosition.Y)), rectangle2, n.GetMagicAuraColor(), 0f, origin3, n.scale, npcSpriteEffect ^ SpriteEffects.FlipHorizontally, 0f);
27201			}
27202			if (NPCID.Sets.AttackType[n.type] == 3 && n.ai[0] == 15f)
27203			{
27204				int num13 = 32;
27205				float num14 = 0f;
27206				Vector2 zero = Vector2.Zero;
27207				short num15 = 4;
27208				if (n.type == 207)
27209				{
27210					num15 = 3349;
27211					num14 = 0.15f;
27212					if (beforeDraw)
27213					{
27214						return;
27215					}
27216					if (n.ai[1] > (float)NPCID.Sets.AttackTime[n.type] * 0.66f)
27217					{
27218						zero.Y = 12f;
27219					}
27220				}
27221				else if (n.type == 353)
27222				{
27223					num15 = 3352;
27224					num14 = 0.15f;
27225					if (!beforeDraw)
27226					{
27227						return;
27228					}
27229					if (n.ai[1] > (float)NPCID.Sets.AttackTime[n.type] * 0.66f)
27230					{
27231						zero.Y = 12f;
27232					}
27233				}
27234				else if (n.type == 441)
27235				{
27236					num15 = 3351;
27237					num13 = 28;
27238					num14 = 0.1f;
27239					if (!beforeDraw)
27240					{
27241						return;
27242					}
27243					if (n.ai[1] > (float)NPCID.Sets.AttackTime[n.type] * 0.66f)
27244					{
27245						zero.Y = 12f;
27246					}
27247				}
27248				GetItemDrawFrame(num15, out var itemTexture2, out var rectangle3);
27249				Tuple<Vector2, float> swingStats = n.GetSwingStats(NPCID.Sets.AttackTime[n.type] * 2, (int)n.ai[1], n.spriteDirection, num13, num13);
27250				Vector2 vector6 = swingStats.Item1 + (swingStats.Item1 - n.Center) * num14 + zero;
27251				Vector2 origin4 = rectangle3.Size() * new Vector2((n.spriteDirection != 1) ? 1 : 0, 1f);
27252				spriteBatch.Draw(itemTexture2, new Vector2((int)(vector6.X - screenPosition.X), (int)(vector6.Y - screenPosition.Y)), rectangle3, n.GetAlpha(npcColor), swingStats.Item2, origin4, n.scale, npcSpriteEffect ^ SpriteEffects.FlipHorizontally, 0f);
27253			}
27254			if (n.type == 550 && n.ai[0] == 18f)
27255			{
27256				if (beforeDraw)
27257				{
27258					return;
27259				}
27260				instance.LoadItem(353);
27261				Texture2D value8 = TextureAssets.Item[353].Value;
27262				int num16 = 32;
27263				float num17 = 0.15f;
27264				Vector2 zero2 = Vector2.Zero;
27265				Microsoft.Xna.Framework.Rectangle rectangle4 = value8.Frame(1, 3, 0, 1);
27266				int num18 = (int)n.ai[2];
27267				if (num18 >= 0 && num18 < 255)
27268				{
27269					Player player = Main.player[num18];
27270					bool flag = player.HeldItem.type == 353 && player.direction == Math.Sign(n.Center.X - player.Center.X);
27271					float num19 = player.Hitbox.Distance(n.Center);
27272					float num20 = n.localAI[3];
27273					if (num19 < 46f && flag)
27274					{
27275						n.localAI[3] = 1f;
27276						if (n.localAI[3] != num20)
27277						{
27278							Vector2 vector7 = n.Center + new Vector2(n.spriteDirection * 30, -6f);
27279							Vector2 vector8 = new Vector2(10f, 10f);
27280							for (int i = 0; i < 30; i++)
27281							{
27282								Dust obj = Dust.NewDustDirect(vector7 - vector8 / 2f, (int)vector8.X, (int)vector8.Y, 4, 0f, 0f, 50, new Microsoft.Xna.Framework.Color(245, 200, 30, 155), 0.7f);
27283								obj.noGravity = true;
27284								obj.velocity *= 1f;
27285								Dust.NewDustDirect(vector7 - vector8 / 2f, (int)vector8.X, (int)vector8.Y, 4, 0f, 0f, 50, new Microsoft.Xna.Framework.Color(245, 200, 30, 155), 0.6f).velocity *= 2f;
27286							}
27287						}
27288					}
27289					else if (n.localAI[3] == 1f)
27290					{
27291						n.localAI[3] = 2f;
27292					}
27293				}
27294				Tuple<Vector2, float> swingStats2 = n.GetSwingStats(40, 12, n.spriteDirection, num16, num16);
27295				Vector2 vector9 = swingStats2.Item1 + (swingStats2.Item1 - n.Center) * num17 + zero2;
27296				Vector2 origin5 = rectangle4.Size() * new Vector2((n.spriteDirection != 1) ? 1 : 0, 1f);
27297				spriteBatch.Draw(value8, new Vector2((int)(vector9.X - screenPosition.X), (int)(vector9.Y - screenPosition.Y)), rectangle4, n.GetAlpha(npcColor), swingStats2.Item2, origin5, n.scale, npcSpriteEffect ^ SpriteEffects.FlipHorizontally, 0f);
27298			}
27299			if (beforeDraw || n.ai[0] != 23f)
27300			{
27301				return;
27302			}
27303			int num21 = (int)n.ai[2];
27304			if (num21 <= 0 || num21 > ItemID.Count)
27305			{
27306				return;
27307			}
27308			GetItemDrawFrame(num21, out var itemTexture3, out var rectangle5);
27309			int num22 = 0;
27310			num22 = (((int)n.frameCounter < 6) ? 1 : 2);
27311			if (n.ai[1] < 6f)
27312			{
27313				num22 = 1;
27314			}
27315			if (num22 == 0)
27316			{
27317				return;
27318			}
27319			Vector2 vector10 = Vector2.Zero;
27320			if (num22 == 1)
27321			{
27322				vector10 = new Vector2(10f, 6f);
27323			}
27324			if (num22 == 2)
27325			{
27326				vector10 = new Vector2(16f, 0f);
27327			}
27328			if ((npcSpriteEffect & SpriteEffects.FlipHorizontally) == 0)
27329			{
27330				vector10.X *= -1f;
27331			}
27332			if (n.type == 369)
27333			{
27334				vector10.X *= 0.5f;
27335				vector10.Y += 4f;
27336			}
27337			if (n.type == 453)
27338			{
27339				vector10.Y += 8f;
27340			}
27341			if (n.type == 550)
27342			{
27343				if (num21 == 353)
27344				{
27345					rectangle5 = itemTexture3.Frame(1, 3, 0, 1);
27346				}
27347				vector10.Y += 6f;
27348			}
27349			Vector2 vector11 = n.Center + vector10;

```


---

## 🤖 Assistant · 2026-08-11T07:18:20.150Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Enough for DrawNPCExtras summary: party hats, Rainbow town slime overlay (681), held-weapon drawing (AttackType 1/2/3 states, magic aura Extra[51], specific items for 207/353/441/550), and ai[0]==23 hand-item drawing.

Now let me also confirm there's nothing between 22000-22159 that draws NPC extras, and nothing after 26209 in DrawNPCDirect (it ends there). Also check DrawNPCs only 22159-22301. Good.

Now assemble the final markdown table. The user asked one row per branch with:
- Main.cs line range
- trigger condition
- what's drawn (texture names, segments, geometry)
- semantics (localAI/ai driven, special rotation)

I need to be comprehensive but organized. I'll structure the table by section (A. DrawNPCs; B. DrawNPCDirect pre-body; C. per-type body branch switch; D. post-body overlays; E. delegated helpers). Since it's huge, I'll make one big table with a "区段" grouping column, or several tables per section. The user asked "最后给一个完整的 markdown 表" — one complete table. I'll do one table with sections separated by bold divider rows maybe. Simpler: one table with a "区块" column.

Row list (final):

DrawNPCs:
1. 22177–22224 | type 125/126 (Retinazer/Spazmatism), !NPC.IsMechQueenUp, once per frame (flag) | Chain12 链段循环 (40*scale 步进) 连接两只眼睛 | 目标 = 另一只眼 Bottom-高度/2*scale; 距离>2000 截断; 逐段采样光照
2. 22225–22252 | type 263 (PlanterasHook) && aiStyle 52 && NPC.plantBoss>=0 | Chain26, 16px 步进(收尾段裁剪高度) 指向 plantBoss Center | 含 netOffset 补偿
3. 22253–22285 | type 264 (PlanterasTentacle) && aiStyle 53 && plantBoss>=0 | Chain27 同上 | 目标 = ai[3]>0 ? npc[ai[3]-1] : plantBoss

DrawNPCDirect 前置(本体绘制前):
4. 22391–22432 | type 101 (Clinger) | Chain10/Chain11 交替, 0.75 缩放, 20*0.75 步进, 段高28(收尾裁剪) | 目标 = (ai[0],ai[1]) 瓦片坐标; bestiary 色覆盖
5. 22433–22498 | aiStyle 13 (悬吊型) type 56 Snatcher / 175 AngryTrapper / 259 FungiBulb / 260 GiantFungiBulb / 其它默认 | Chain5/Chain14/Chain24/Chain25/Chain4, 步进28/40 (259/260 用12/20), 收尾段裁剪 | 目标=(ai[0],ai[1])瓦片; 259/260 强制 B=255,R>=100,G>=150
6. 22499–22506 | type 327 Pumpking | PumpkingCloak (5 帧, 帧=localAI[1]) 固定在 Center+(0,80), rotation 0 | 披风
7. 22507–22542 | type 328 PumpkingBlade | PumpkingArm ×2 段: 目标 npc[ai[1]](Pumpking), 段1偏移 (-200*ai[0], +130) 归一化到 92px, 段2 (-50*ai[0],+80) 归一化 60px; 旋转 atan2-90° | ai[0] 为朝向
8. 22543–22592 | type 36 SkeletronHand | BoneArm(或 localAI[3]==1 时 BoneArm3) ×2 段, 同上 92/60 几何; 段2 后生 Dust 5 | localAI[3] 切换贴图
9. 22593–22632 | aiStyle 47 (Golem 拳 247/248 等) | Chain21 步进 16*scale, 指向 golemBoss Center 偏移 (+66*scale 或 type==247 时 -70*scale, -7*scale) | getGoodWorld 额外 +8
10. 22633–22675 | aiStyle 33–36 (SkeletronPrime 手) | BoneArm2 ×2 段, 92/60 几何指向 npc[ai[1]](本体) | 段2 后 Dust 6
11. 22676–22713 | type 693 LibrarianSkeleton | Extra[289] 旋转光环, 中心=Top, 旋转=localAI[0]*0.016*localAI[3], 缩放由 localAI[2]/10 提升; localAI[0]<60 淡入, >localAI[1]-60 淡出并加速旋转 | 纯 localAI 驱动
12. 22714–22741 | aiStyle 20 (尖球/链锤类) | Chain 步进 12px 指向 (ai[1],ai[2]) 世界坐标 + SpikeBase 锚点 (rotation-0.75) | 会写入 npc.rotation = atan2-90°
13. 22798–22818 | type 50 KingSlime | Ninja 贴图(藏着的忍者) 绘于身体中心, 偏移 = -velocity*(2,1), 旋转=velocity.X*0.05, frame.Y 120/360/480 时 Y±2/±6 | 拖尾式错位
14. 22819–22840 | type 71 DungeonSlime | GetItemDrawFrame(327) 物品贴图(金色钥匙)画在中心, 偏移 -velocity*(0.6,0.3), 旋转 velocity.X*0.09 | 
15. 22841–22844 | type 69 Antlion | AntLion 贴图(沙堆) 画在脚部 +14, 旋转 = -rotation*0.3 |
16. 22845–22848 | NPCID.Sets.SlimeCanContainItems && ai[1]>0 | DrawNPC_SlimeItem: 物品贴图按 22/18*scale 缩放画在体内, 帧偏移 & ai[0]==-999 特例 | ai[1]=物品ID

本体分支 switch (23027 起):
17. 22989–23026 | type 124 Mechanic && localAI[0]==0 | Projectile[582](或 townNpcVariationIndex==1 时 Extra[263]) 头饰, 位置随 OffsetsPlayerHeadgear[帧] | 变体索引换贴图
18. 23034–23102 | type 551 DD2Betsy | 本体 + Extra[81]/Extra[82] 双翼 (2x5 帧, 帧=localAI[0]/4), 翼根偏移 (171,44)/(230,52) 绕 (vector12) 旋转, 再沿 oldPos 9→0 步长-3 画 3 层残影(翼+本体+GlowMask[226]) | localAI[0] 翼动画, localAI[1] 亮度
19. 23103–23133 | type 690 StatueMimic | Tile[105](雕像图块) 2×3 网格拼接, ai[1] 决定取图区(55 列×3 行), direction/num76 选择行 | 伪装成雕像
20. 23134–23300 | type 657 QueenSlimeBoss | life<=lifeMax/2 时 DrawNPCDirect_QueenSlimeWings (Extra[185] 翼 1×4 帧 localAI[3]/6, 两翼翻转, velocity.Y 驱动摆动); Extra[186] 水晶(帧驱动的 Y 偏移表) 经 QueenSlime shader; ai[0]==4 && velocity.Y!=0 时 8 层跳跃残影; Extra[177] 头顶装饰(同样帧偏移表) |
21. 23301–23348 | type 576/577 DD2OgreT2/T3 | localAI[3]<60(出生)时 3 层紫色残影(固定偏移) |
22. 23349–23379 | type 696 PalworldFoxsparksDistressed | 本体(Frame 6×27) + 第 19 行帧(TileFrameSeed 随机抖动 ±1px)以半透明白重画两次; ai[0]==2 时临时表情泡 |
23. 23380–23402 | type 594 WindyBalloon | Frame(8,1) 气球本体 + 挂载的史莱姆 NPC(AI_113_WindyBalloon_GetSlaveNPC)整体(含其体内物品 DrawNPC_SlimeItem)以 slave.scale 画入, 随 rotation 旋转 |
24. 23413–23496 | type 564/565 DD2DarkMageT1/T3 | 出生(localAI[3]<60)3 层紫色残影 + 4 层径向脉冲残影(0.625±0.125 正弦) + GlowMask[225] 光环及 4 层径向拷贝 (Opacity 门禁) |
25. 23497–23619 | type 548 DD2EterniaCrystal | 4 层径向残影 ×3 组 + GlowMask[239] 顶部光环(Center-40) 双脉冲 + Extra[89] 竖直光束(旋转 90°, dontTakeDamage 时 Y 压 0.6); ai[1]==2 时 CrystalWin 场景滤镜 |
26. 23642–23721 | type 549 DD2LanePortal | 出生放大(localAI[0]<120, scale 0.5→1) + 循环轨道残影 + DrawElderEye×3(眼睛, 亮度由 (ai[0]+54)%180 相位驱动) |
27. 23722–23724 | type 636 HallowBoss → DrawNPCDirect_HallowBoss (26364) | Extra[157..160] 手臂/翼多层 + ai[0] 8/9/10 时径向克隆 | localAI[0] 翼帧
28. 23725–23727 | type 677 Shimmerfly → DrawNPCDirect_Faeling (26306) | 本体多层(Frame 4×5 第0/1/2/3行) + oldPos 采样拖尾(正弦摆动, 速度决定拖尾长度) | whoAmI 相位
29. 23728–23730 | type 668 Deerclops → DrawNPCDirect_Deerclops (26211) | 出生(localAI[3])2 层红色残影; ai[0]==7/8 时 5 层双层螺旋克隆; Extra[245] 红光覆盖 |
30. 23731–23847 | type 422/493/507/517 四座月塔 | GlowMask[149]/[132]/[143]/[162] 各 4 层 velocity 径向残影 + 护盾: Perlin 噪声贴图 + ForceField shader(ShieldStrengthTower>0 或消失动画 ai[3]) |
31. 23848–23890 | type 402 StardustWormHead | oldPos 双倍采样交替 Npc[403](身)/Npc[404](尾) 贴图 + GlowMask[133]/[134] 长拖尾(约 20 段) + GlowMask[135] + DrawPrettyStarSparkle | ai[2] 渐变
32. 23891–23913 | type 519 SolarGoop | 粉色 oldPos 全长残影(缩放 0.3→1.1) |
33. 23914–23936 | type 522 AncientLight | 白色 oldPos 残影(缩放 0.8→0.3) + Extra[57] 本体覆盖 |
34. 23937–24120 | type 370/372/373 DukeFishron/Sharkron/Sharkron2 | oldPos 残影(步长2, 帧数由 ai[0] 状态决定) + ai[0] 3/8/4/9/12 时的 6 层余弦轨道克隆(半径 20-60); type 370 && ai[0]>=4 额外用 TextureAssets.DukeFishron(狂暴贴图) 重画整套黄色残影 |
35. 24121–24201 | type 439/440 CultistBoss/Clone | Extra[30] (2 帧上半) oldPos 残影(ai[0]==-1&&ai[1] 320-960 或 ai[0]==1) + ai[0]==5 时 4 层 70px 余弦轨道克隆 |
36. 24202–24229 | type 392/395/394 MartianSaucer/Core/Cannon | GlowMask[48]/[50]/[49] 平铺发光覆盖 |
37. 24263–24324 | type 491 PirateShip | Extra[40](1×4 动画, localAI[3]/8)、Extra[41]×5、Extra[42]×2、Extra[43]×2、Extra[44]、Extra[45](相位+2) 全部按固定骨架偏移(随 rotation 旋转) + Npc[492] 大炮帧×4(ai[0..3] 各指向一门炮, 帧=对应炮的帧) |
38. 24325–24390 | type 398 MoonLordCore | Extra[13] 腿×2(镜像) + Extra[14] 手×2: 找到 type 397(MoonLordHand) 手 NPC, 用 0.5 插值 + acos(v.Length()/340) 弯曲角(伪 IK); Extra[16] 心脏 + 本体 |
39. 24391–24448 | type 397 MoonLordHand | Extra[15] 前臂: 朝 (头中心+ (220,-60)±) 的 0.5 收敛 + acos 弯曲; ai[0]==-2 时 Extra[26] (充能帧 ai[1]/8), 否则 Extra[17]+Extra[19](localAI[0]/[1] 椭圆眼位) + 本体 |
40. 24449–24491 | type 396 MoonLordHead | Extra[18](眉) 或 ai[0]<0 时 Extra[26]; Extra[19] 眼(localAI[0]/[1] 椭圆); 本体 3×3 帧×2 缩放; Extra[29](帧 localAI[3]/5) 顶部; Extra[25](帧 localAI[2]/7) 底部 |
41. 24492–24505 | type 400 MoonLordFreeEye | Extra[19] 眼球, 椭圆偏移 (30,30)*localAI[1] 角度=localAI[0], 缩放=localAI[2] |
42. 24506–24538 | type 416 SolarDrakomireRider | 先把自身 Bottom 对齐到 ai[0] 指向的 type 415 (SolarDrakomire) 并借 gfxOffY/velocity; GlowMask[156] + 4 层 velocity 径向残影 |
43. 24539–24573 | type 399 MartianProbe | Extra[27] ×2 竖直光柱(MathF.PI/2, 原点(10,48), 缩放随 (GlobalTime+i)%5) 颜色由 ai[0](0 绿/1 绿转红 ai[1]/20/2 红) + GlowMask[100] + Extra[20](1×4 帧=ai[0]+1) + GlowMask[101] |
44. 24574–24588 | type 94 Corruptor | oldPos 1,3,5 残影(shimmer 色) |
45. 24592–24604 | type 125–131 / 139(ai[3]==0) / 140 机械boss部件 | oldPos 9→0 步长2 残影 |
46. 24605–24617 | type 417 SolarSroller && ai[0]==6 | oldPos 6→0 残影, oldRot + 缩放 0.5→1 |
47. 24618–24640 | type 419 SolarSolenian && ai[2]<=-9 | GlowMask[154] 帧 5–7 循环的 7 段 oldPos 残影, 缩放 0.75→1.2 |
48. 24641–24672 | type 418 SolarCorite && ai[0]∈{2,4} | Extra[55] (1×4 帧) 7 段火焰拖尾, 颜色 Gold→OrangeRed→Blue, 旋转=oldRot - π/2*spriteDirection |
49. 24673–24695 | type 516 SolarFlare | 本体贴图帧错位(帧号-4-idx mod 4) 7 段残影, 缩放 0.35→1.2 |
50. 24696–24703 | type 390 ScutlixRider && IsABestiaryIconDummy | 在旁边 (-width-8, +10) 画 Npc[391](Scutlix) 的帧(localAI[3]) |
51. 24709–24726 | type 420/421/423/424 Nebula 系 | 4 层正交方向残影(半径 9+3cos(2πt)) 青色 |
52. 24727–24744 | type 662 PirateGhost | 8 层 -velocity*10*α 拖尾 + 4 层正交残影(半径 4+2cos) 青色 |
53. 24746–24749 | aiStyle 7 | DrawNPCExtras(beforeDraw:true) |
54. 24750–24753 | type 346 SantaNK1 && life<50% | 用 TextureAssets.SantaTank 替换本体贴图(坦克形态) |
55. 24799–24843 | type 266 BrainofCthulhu && 受伤 && (expert||getGood) | 以玩家为中心镜像的 4 份拷贝(位置按 |Δ| 镜像), alpha 随失血/专家倍率 |
56. 24844–24853 | type 421 NebulaHeadcrab && ai[0]==5 | 把本体+GlowMask[146] 画到目标玩家头/脚位置(gravity 翻转时 FlipVertically) |
57. 24951–24976 | aiStyle 7 && ai[0]==25 | ColorOnly 染料 shader 重绘本体 + 6 层彩虹轨道克隆(半径 4*(GlobalTime+i)) + 2 个 DrawPrettyStarSparkle |
58. 24995–25003 | type 695 && ai[0]==2 | EmoteBubble 临时表情泡(ai[1]<60) |
59. 25008–25043 | type 247/248 GolemFistL/R | ai[0]==1: 3 层白脉冲缩放(2→1.1+0.1i, 由 ai[1] 相位); ai[0]==2: 3 层 -velocity*2i 拖尾 + 3 层放大脉冲 |
60. 25044–25047 | type 24 FireImp | GlowMask[360] 覆盖 |
61. 25048–25055 | type 639–645 宝石松鼠 / 646–652 宝石兔 | GlowMask[286] / GlowMask[287] 覆盖 |
62. 25056–25124 | type 134–136 TheDestroyer 系 / 125 / 139 / 127 / 131 | Dest[i] 覆盖(134–136, alpha 渐隐); EyeLaser(125); Probe(139); 127: IsMechQueenUp 时从 GetMechQueenCenter 的两个锚点(±(18/20,-18) 旋转)向所有 125/126 画 Chain12 链, 否则 BoneEyes 覆盖; BoneLaser(131) |
63. 25125–25139 | type 120 ChaosElemental | TextureAssets.Chaos 沿 oldPos 的 shimmer 拖尾 |
64. 25140–25154 | type 137/138 IlluminantBat/Slime | 本体沿 oldPos shimmer 拖尾 |
65. 25155–25164 | type 327 Pumpking | PumpkingFace 覆盖 + 9 份随机 ±2px 抖动拷贝(火光闪烁) |
66. 25165–25174 | type 325 MourningWood | TreeFace 覆盖 + 9 份随机抖动拷贝 |
67. 25175–25182 | type 345 IceQueen | IceQueen 覆盖 + 4 层 -velocity*0.2i 拖尾 |
68. 25183–25190 | type 355 Firefly / 358 LightningBug | Firefly / Lightningbug 发光覆盖 |
69. 25191–25198 | type 654 Lavafly / 653 HellButterfly | GlowMask[290] / GlowMask[288] |
70. 25199–25206 | type 82 Wraith | WraithEye + 9 层 -velocity*0.5i 拖尾 |
71. 25207–25214 | type 253 Reaper | ReaperEye + 19 层拖尾 |
72. 25215–25218 | type 245 Golem && alpha==0 && !getGoodWorld | Golem[3] 覆盖(mouseTextColor 亮度) |
73. 25219–25240 | type 246 GolemHead && !getGoodWorld | Golem[1](左拳, 帧<222)/Golem[2] 上下半帧(右拳) 画在 Center±(26/−38,−28), 第一段再叠 Extra[107] |
74. 25241–25257 | type 249 GolemHeadFree && !getGoodWorld | Golem[1] + Extra[106](1×8, frameCounter/4 驱动) + Extra[107] |
75. 25258–25266 | type 383 MartianOfficer | GlowMask[11] + 若 ai[2] 关联的 type 384(ForceBubble) 存在则半透明画 Npc[384] |
76. 25267–25344 | type 381 BrainScrambler | Extra[0] (32×42, 帧行=ai[2]-1 或空中=3) + GlowMask[24], 位置按本体 9 帧偏移表; 水平翻转时 X 取反 |
77. 25345–25421 | type 382 RayGunner | Extra[1] (30×42) 同上几何 |
78. 25422–25444 | type 520 MartianWalker | GlowMask[164] + Extra[56](旋转=localAI[3], 翻转时 +π) + GlowMask[165] |
79. 25445–25468 | type 386/387/388/389 火星炮台/无人机/电炮 | GlowMask[31]/[32](387 随 ai[0] 渐隐)/[33]/[34] |
80. 25469–25481 | type 4 EyeofCthulhu && ai[1]>=4 && ai[0]==3(旋转冲锋) | oldPos 全长残影(半透明) |
81. 25482–25488 | type 437 CultistTablet | GlowMask[109](帧) + GlowMask[108](整图) |
82. 25489–25501 | type 471 GoblinSummoner && ai[3]<0 | oldPos 残影 |
83. 25502–25521 | type 477 Mothron && speed>9 | oldPos 残影(帧号 -i*frameHeight 循环错位) |
84. 25522–25541 | type 479 MothronSpawn && speed>6.5 同上 / 472 ShadowFlameApparition: GlowMask[110] |
85. 25546–25562 | aiStyle 87 && ai[0]∈{4,5,6} | oldPos shimmer 残影 |
86. 25567–25596 | type 50 KingSlime | Extra[39](王冠) 画在 Center + gfxOffY -(70-帧偏移)*scale, 帧偏移表 2/-6/2/10/2/0 |
87. 25597–25789 | 一大批发光覆盖/残影: 411→GlowMask[136], 409→[138], 410→[137], 407→[139], 405→[141], 406→[142], 424→[144], 423→[145], 421→[146], 420→[147], 425→[150]+绿色 DrawPrettyStarSparkle(ai[3]), 429→[151], 418→[161]+4 velocity 残影, 412/413/414→GlowMask[157+i](414 用 localAI[2] 变红), 415→[155]+4 velocity 残影, 419→[154]+4 残影(ai[2]<-6 时改为 4 向固定偏移), 417→[160]+4 残影, 516→本体+4 残影, 518→GlowMask[163]+4 残影(origin X-10), 344→[253], 346→[254]+4 向残影, 315 HeadlessHorseman→[255]+4 向残影, 525/526/527→[169]/[170]/[171], 533→[172], 160 Truffle→[166](变体[352]), 209→[167](变体[350]/[351] 由 altTexture) |
88. 25791–25794 | aiStyle 7 | DrawNPCExtras(beforeDraw:false): 派对帽 Extra[72](20 帧按 GetPartyHatColor), type 681 Extra[250] 覆盖, 手持武器(AttackType 1: 物品贴图按帧/类型 19/22/178/227/368; type 22 再叠 Extra[52]5帧), AttackType 2: Extra[51] 施法光环(4 帧), AttackType 3: 挥舞物品(207/353/441/550 各自 item 3349/3352/3351/353, GetSwingStats), ai[0]==23 手持物品 |
89. 25803–26207 | 大类: 426/427/428/521/523/541–545/546/552–563/566/567/568/569/570/571/572/573/574/575/578/581/618/620/661/558–560 | 通用残影系统(oldPos 拖尾 + 径向轨道克隆, 每类型配置数量/步长/半径/颜色) + 各自附加: 426/427 → GlowMask[153]/[152]; 541 → GlowMask[216] 金色轨道克隆; 661 EmpressButterfly → 彩虹轨道克隆(hslToRgb, 半径 2+ai[2]); 568/569 WitherBeast → GlowMask[224] 轨道克隆 + localAI[0]>0 时 Extra[89] 16 根 400px 旋转光束环; 546 Tumbleweed → Extra[76] 覆盖(随 velocity.X 倾斜); 566/567 Skeleton && localAI[3]>=115 → Extra[80](1×4) 头顶装饰; 618 BloodNautilus → ai[0]==1/3 时 Extra[59] 径向漩涡(双层) + Extra[129] 覆盖; 620 GoblinShark → 6 层金色轨道克隆+origin 偏移 |

That's the bulk. Note 25803 group: careful — this group is huge; I'll split it into sub-rows: (a) the shared afterimage engine applies to the listed types, (b) per-type extras.

Also there's type 655 (MagmaSnail) - that's a color branch (Orange tint), excluded. type 360/356/267 - positional, excluded. 576/577's localAI spawn ghosts included. 

Also type 552-557/561-563 etc. only set num47 offsets mostly (positional) — the 568/569 group has orbit; 558-560/574/575 has ai[0]==2 trail (num294=6, step 2, scale lerp). And the generic engine's radial loop only runs for those with num299>0 (541, 661, 523, 620, 568/569, 618, 426, 566/567/578 no). OK — I'll describe per-type config compactly.

Also missed: within 25803 group: case 542-545 (SandShark family) num294=6 step3 → oldPos trail. case 427: num294=8 trail; 546: trail 8 step2 (scale lerp 1→0.3... value81=0.3); 581: trail 6 step2; 521: trail 10 step2 with oldRot and scale to 0.3; 558-560/574/575: ai[0]==2 → trail 6 step2 + num298=1.

I'll compress these into the group row with a config summary.

Also 23621-23641: case 371/454-459/621-623 (Blood Eel, Cultist Dragon) — plain draws, excluded. Also case 490? Not present in this switch... "case 488: break;" at 25797. Fine.

Also 23053-...: halfSize adjustments excluded.

Also within first switch default: types listed in 23030 condition are those that skip this branch entirely.

Also 22980-22983: aiStyle 10 && type!=694 || type==72 → npcColor = White (color only, exclude).

Also 22853-22978: num46/num47 offsets (positional, exclude).

OK. Also mention 22318-22348 DrawNPCDirect_QueenSlimeWings as its own row (helper).

Now let me also double check the missing piece: lines 23101-23102 return; and 23034-23102 is case 551. Confirmed.

One more check — is there anything between 26209 (end of DrawNPCDirect) and helper methods that I should include? The helpers themselves (26211-26551 HallowBoss incl. GetHallowBossArmFrame at 26552). Let me peek at the rest of HallowBoss (26424-26551) to describe arms accurately.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:18:20.404Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "limit": 130,
 "offset": 26424
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:18:20.414Z

**📎 ToolResult**

```
26424					Microsoft.Xna.Framework.Color color2 = Microsoft.Xna.Framework.Color.White;
26425					Vector2 position = vector;
26426					if (num == 8 || num == 9)
26427					{
26428						float hue = ((float)i + 5f) / 10f;
26429						float num10 = 200f;
26430						float num11 = (float)timeForVisualEffects / 60f;
26431						Vector3 vector2 = Vector3.Transform(matrix: Matrix.CreateRotationX((num11 - 0.3f + (float)i * 0.1f) * 0.7f * (MathF.PI * 2f)) * Matrix.CreateRotationY((num11 - 0.8f + (float)i * 0.3f) * 0.7f * (MathF.PI * 2f)) * Matrix.CreateRotationZ((num11 + (float)i * 0.5f) * 0.1f * (MathF.PI * 2f)), position: Vector3.Forward);
26432						num10 += Utils.GetLerpValue(-1f, 1f, vector2.Z, clamped: true) * 150f;
26433						Vector2 spinningpoint = new Vector2(vector2.X, vector2.Y) * num10 * num7;
26434						float lerpValue = Utils.GetLerpValue(90f, 0f, rCurrentNPC.ai[1], clamped: true);
26435						color2 = hslToRgb(hue, 1f, MathHelper.Lerp(0.5f, 1f, lerpValue)) * 0.8f * num8;
26436						color2.A /= 3;
26437						position += spinningpoint.RotatedBy(rCurrentNPC.ai[1] / 180f * (MathF.PI * 2f));
26438					}
26439					if (num == 10)
26440					{
26441						if (rCurrentNPC.ai[1] >= 90f)
26442						{
26443							float num12 = (float)timeForVisualEffects / 90f;
26444							int num13 = i;
26445							if (num13 < 0)
26446							{
26447								num13++;
26448							}
26449							Vector2 vector3 = (((float)num13 + 0.5f) * (MathF.PI / 4f) + MathF.PI * 2f * num12).ToRotationVector2();
26450							position += vector3 * new Vector2(600f * num7, 150f * num7);
26451						}
26452						else
26453						{
26454							position += 200f * new Vector2(i, 0f) * num7;
26455						}
26456						color2 = Microsoft.Xna.Framework.Color.White * 0.8f * num8 * num4;
26457						color2.A /= 3;
26458					}
26459					if (i > num6)
26460					{
26461						float lerpValue2 = Utils.GetLerpValue(30f, 70f, rCurrentNPC.ai[1], clamped: true);
26462						if (lerpValue2 == 0f)
26463						{
26464							continue;
26465						}
26466						position = vector + rCurrentNPC.velocity * -3f * ((float)i - 4f) * lerpValue2;
26467						color2 *= 1f - num9;
26468					}
26469					mySpriteBatch.Draw(value2, position, rectangle, color2, rCurrentNPC.rotation, rectangle.Size() / 2f, rCurrentNPC.scale * 2f, npcSpriteEffect, 0f);
26470					mySpriteBatch.Draw(value5, position, rectangle, color2, rCurrentNPC.rotation, rectangle.Size() / 2f, rCurrentNPC.scale * 2f, npcSpriteEffect, 0f);
26471					if (flag)
26472					{
26473						Texture2D value6 = TextureAssets.Extra[187].Value;
26474						Microsoft.Xna.Framework.Rectangle value7 = value6.Frame(1, 8, 0, (int)(rCurrentNPC.localAI[0] / 4f) % 8);
26475						mySpriteBatch.Draw(value6, position, value7, color2, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, npcSpriteEffect, 0f);
26476					}
26477					mySpriteBatch.Draw(value, position, rCurrentNPC.frame, color2, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, npcSpriteEffect, 0f);
26478					for (int j = 0; j < 2; j++)
26479					{
26480						if (j == num2)
26481						{
26482							mySpriteBatch.Draw(value3, position, rectangle2, color2, rCurrentNPC.rotation, origin, rCurrentNPC.scale, npcSpriteEffect, 0f);
26483						}
26484						if (j == num3)
26485						{
26486							mySpriteBatch.Draw(value4, position, rectangle3, color2, rCurrentNPC.rotation, origin2, rCurrentNPC.scale, npcSpriteEffect, 0f);
26487						}
26488					}
26489				}
26490			}
26491			color *= num4;
26492			mySpriteBatch.Draw(value2, vector, rectangle, color, rCurrentNPC.rotation, rectangle.Size() / 2f, rCurrentNPC.scale * 2f, npcSpriteEffect, 0f);
26493			if (!rCurrentNPC.IsABestiaryIconDummy)
26494			{
26495				mySpriteBatch.End();
26496				mySpriteBatch.Begin(SpriteSortMode.Immediate, BlendState.AlphaBlend, SamplerState.PointClamp, DepthStencilState.Default, RasterizerState.CullNone, null, Transform);
26497			}
26498			DrawData value8 = new DrawData(value5, vector, rectangle, color, rCurrentNPC.rotation, rectangle.Size() / 2f, rCurrentNPC.scale * 2f, npcSpriteEffect);
26499			GameShaders.Misc["HallowBoss"].Apply(value8);
26500			value8.Draw(mySpriteBatch);
26501			pixelShader.CurrentTechnique.Passes[0].Apply();
26502			if (!rCurrentNPC.IsABestiaryIconDummy)
26503			{
26504				mySpriteBatch.End();
26505				mySpriteBatch.Begin(SpriteSortMode.Deferred, BlendState.AlphaBlend, DefaultSamplerState, DepthStencilState.None, Rasterizer, null, Transform);
26506			}
26507			float num14 = (float)Math.Sin(GlobalTimeWrappedHourly * (MathF.PI * 2f) * 0.5f) * 0.5f + 0.5f;
26508			Microsoft.Xna.Framework.Color color3 = hslToRgb((num14 * 0.08f + 0.6f) % 1f, 1f, 0.5f);
26509			color3.A = 0;
26510			color3 *= 0.6f;
26511			if (NPC.ShouldEmpressBeEnraged())
26512			{
26513				color3 = OurFavoriteColor;
26514				color3.A = 0;
26515				color3 *= 0.3f;
26516			}
26517			color3 *= num4 * rCurrentNPC.Opacity;
26518			if (flag)
26519			{
26520				Texture2D value9 = TextureAssets.Extra[187].Value;
26521				Microsoft.Xna.Framework.Rectangle value10 = value9.Frame(1, 8, 0, (int)(rCurrentNPC.localAI[0] / 4f) % 8);
26522				mySpriteBatch.Draw(value9, vector, value10, color, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, npcSpriteEffect, 0f);
26523				for (float num15 = 0f; num15 < 1f; num15 += 0.25f)
26524				{
26525					Vector2 vector4 = rCurrentNPC.rotation.ToRotationVector2().RotatedBy(num15 * (MathF.PI * 2f) + MathF.PI / 4f) * MathHelper.Lerp(2f, 8f, num14);
26526					mySpriteBatch.Draw(value9, vector + vector4, value10, color3, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, npcSpriteEffect, 0f);
26527				}
26528			}
26529			mySpriteBatch.Draw(value, vector, rCurrentNPC.frame, color, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, npcSpriteEffect, 0f);
26530			if (flag)
26531			{
26532				Texture2D value11 = TextureAssets.Extra[188].Value;
26533				for (float num16 = 0f; num16 < 1f; num16 += 0.25f)
26534				{
26535					Vector2 vector5 = rCurrentNPC.rotation.ToRotationVector2().RotatedBy(num16 * (MathF.PI * 2f) + MathF.PI / 4f) * MathHelper.Lerp(2f, 8f, num14);
26536					mySpriteBatch.Draw(value11, vector + vector5, null, color3, rCurrentNPC.rotation, halfSize, rCurrentNPC.scale, npcSpriteEffect, 0f);
26537				}
26538			}
26539			for (int k = 0; k < 2; k++)
26540			{
26541				if (k == num2)
26542				{
26543					mySpriteBatch.Draw(value3, vector, rectangle2, color, rCurrentNPC.rotation, origin, rCurrentNPC.scale, npcSpriteEffect, 0f);
26544				}
26545				if (k == num3)
26546				{
26547					mySpriteBatch.Draw(value4, vector, rectangle3, color, rCurrentNPC.rotation, origin2, rCurrentNPC.scale, npcSpriteEffect, 0f);
26548				}
26549			}
26550		}
26551	
26552		private static void DrawNPCDirect_GetHallowBossArmFrame(NPC rCurrentNPC, out int armFrame_Count, out int armFrameToUseLeft, out int armFrameToUseRight)
26553		{

```


---

## 🤖 Assistant · 2026-08-11T07:18:25.268Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have enough. Now compose the final answer: a markdown table with all rows. It'll be long, but that's what was asked. I'll organize with a 区块 column. Include absolute path reference.

Let me write the final answer in Chinese. Use one table (as requested "最后给一个完整的 markdown 表"). I'll keep each row compact.

I'll add short notes about excluded categories (color/alpha/frame-only, positional offsets) so the user knows coverage.

Line numbers: use the ranges I identified.

Let me finalize rows carefully with correct numbers:

Section 0 helper:
- 22318–22348 DrawNPCDirect_QueenSlimeWings (helper called at 23147)
- 22149 DrawElderEye (helper called at 23704-23708)
- 26211–26296 Deerclops, 26298–26304 DeerclopsLeg(未使用?), 26306–26362 Faeling, 26364–26550 HallowBoss, 26552+ arm frames, 26709+ SlimeItem, 26812+ DrawNPCExtras.

Row for DeerclopsLeg — it's defined but is it called? grep showed only definition at 26298. Not called in DrawNPCDirect (maybe called elsewhere). Skip or mention.

Now write the answer.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:19:42.164Z · glm-x-preview-260804

```
下面是对 `~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs` 中 `DrawNPCs`(22159–22301) / `DrawNPC`(22311–22316) / `DrawNPCDirect`(22350–26209) 及其专属辅助方法的系统性枚举。只统计“在本体贴图之外额外叠画的部件/拖尾/链段/光环”，已剔除纯颜色/alpha/帧选择/位置偏移(`num45`/`num46`/`num47`/halfSize 调整)和纯 shader 替换(RainbowTownSlime、ColorOnly 本体重绘除外，其中含几何克隆的已收录)。NPC 名称取自同仓库 `Terraria.ID/NPCID.cs`。

## 完整 Markdown 表

| 区块 | 行号范围 | 触发条件 | 画的内容(Texture / 段数 / 几何) | 语义/驱动 |
|---|---|---|---|---|
| DrawNPCs | 22177–22224 | `type==125‖126`(Retinazer/Spazmatism) 且 `!NPC.IsMechQueenUp`，每帧一次(flag 门) | `Chain12` 链段循环，步长 `40*scale`，段原点=段中心 | 目标=另一只眼的 `Bottom - height*0.5*scale`；距离>2000 截断；逐段采光照 |
| DrawNPCs | 22225–22252 | `type==263`(PlanterasHook) `aiStyle==52` `NPC.plantBoss>=0` | `Chain26` 链段，固定 16px 步进，收尾段裁剪高度 | 目标=plantBoss.Center，含目标 `netOffset` 补偿 |
| DrawNPCs | 22253–22285 | `type==264`(PlanterasTentacle) `aiStyle==53` `plantBoss>=0` | `Chain27`，同上几何 | 目标=`ai[3]>0 ? npc[ai[3]-1] : plantBoss`，含 netOffset |
| Direct-前置 | 22391–22432 | `type==101`(Clinger) | `Chain10`/`Chain11` 交替段，scale 0.75，步进 `20*0.75`，段高 28(收尾裁剪) | 目标=瓦片坐标 `(ai[0],ai[1])`；Bestiary 时整链换色 |
| Direct-前置 | 22433–22498 | `aiStyle==13`(悬吊型) | 链段按 type 选：56 Snatcher→`Chain5`、175 AngryTrapper→`Chain14`、259 FungiBulb→`Chain24`、260 GiantFungiBulb→`Chain25`、默认→`Chain4`；步进 28/40，259/260 用 12/20 | 目标=`(ai[0],ai[1])`；259/260 强制 `B=255,R≥100,G≥150` |
| Direct-前置 | 22499–22506 | `type==327`(Pumpking) | `PumpkingCloak`(1×5，帧=`localAI[1]`) 画在 `Center+(0,80)`，rotation=0 | 披风，纯 localAI 驱动 |
| Direct-前置 | 22507–22542 | `type==328`(PumpkingBlade) | `PumpkingArm` ×2 段：段1 偏移 `(-200*ai[0],+130)` 归一化到 92px、段2 `(-50*ai[0],+80)` 归一化到 60px，旋转 `atan2-90°` | 目标=`npc[ai[1]]`(Pumpking)中心；`ai[0]`=朝向 |
| Direct-前置 | 22543–22592 | `type==36`(SkeletronHand) | `BoneArm`(或 `localAI[3]==1` 时 `BoneArm3`) ×2 段，92/60 几何同上 | 目标=`npc[ai[1]]`(Skeletron)；段2 后出 Dust 5(受 `FocusHelper.AllowMiscDustEffects` 门禁) |
| Direct-前置 | 22593–22632 | `aiStyle==47`(Golem 拳 247/248) | `Chain21` 步进 `16*scale`，收尾 16 | 目标=golemBoss.Center 加偏移 `type!=247 ? +66*scale : -70*scale，-7*scale`；`getGoodWorld` 再 +8 |
| Direct-前置 | 22633–22675 | `aiStyle` 33–36(SkeletronPrime 手) | `BoneArm2` ×2 段，92/60 几何，旋转 `atan2-90°` | 目标=`npc[ai[1]]`(Prime 本体)；段2 后 Dust 6 |
| Direct-前置 | 22676–22713 | `type==693`(LibrarianSkeleton) | `Extra[289]` 单张贴图，中心=`Top`，旋转=`localAI[0]*0.016*localAI[3]` | `localAI[2]/10` 抬升缩放；`localAI[0]<60` 淡入，`>localAI[1]-60` 淡出并加速旋转(头顶漩涡光环) |
| Direct-前置 | 22714–22741 | `aiStyle==20`(链锤/尖球类) | `Chain` 步进 12px 指向 `(ai[1],ai[2])` 世界坐标 + `SpikeBase` 锚点贴图(旋转 `rotation-0.75`) | **会写回 `npc.rotation = atan2-90°`** |
| Direct-前置 | 22798–22818 | `type==50`(KingSlime) | `Ninja`(体内的忍者) 画于身体中心；偏移 `-velocity*(2,1)`，旋转 `velocity.X*0.05` | frame.Y==120/360/480 时 Y ±2/±6 |
| Direct-前置 | 22819–22840 | `type==71`(DungeonSlime) | `GetItemDrawFrame(327)` 金钥匙画于中心，偏移 `-velocity*(0.6,0.3)`，旋转 `velocity.X*0.09` | 同上帧修正 |
| Direct-前置 | 22841–22844 | `type==69`(Antlion) | `Antlion` 贴图(沙堆) 画在脚部 `+height+14`，旋转 `-rotation*0.3` | 无 |
| Direct-前置 | 22845–22848 | `NPCID.Sets.SlimeCanContainItems[type] && ai[1]>0` | `DrawNPC_SlimeItem`(26709)：体内物品贴图，按 `22/18*scale`(ai[0]==-999 时 14) 包围盒等比缩放 | `ai[1]`=物品 ID；537 特例；帧号参与位置 |
| 本体 switch | 22989–23026 | `type==124`(Mechanic) `localAI[0]==0` | `Projectile[582]`(变体 `townNpcVariationIndex==1` 时 `Extra[263]`) 头饰，画在头顶 | Y 随 `OffsetsPlayerHeadgear[帧]`；scale 2/3 时 -6/-12 |
| 本体 switch | 23034–23102 | `type==551`(DD2Betsy) | 本体 + `Extra[81]`/`Extra[82]` 双翼(2×5，帧=`localAI[0]/4`)，翼根偏移 `(171,44)`/`(230,52)` 绕 pivot 旋转；沿 `oldPos` 9→0(步长-3) 画 3 层残影(双翼+本体+`GlowMask[226]`) | `localAI[0]` 翼动画、`localAI[1]` 亮度；翻转时对 origin/翼根做镜像 |
| 本体 switch | 23103–23133 | `type==690`(StatueMimic) | `Tile[105]`(雕像图块) 按 2×3 网格 6 块拼接，原点 `(1-i, 1.5-j)*16` | 取图区由 `ai[1]` 决定(55 列×3 行)，`direction` 偏移行 |
| 本体 switch | 23134–23300 | `type==657`(QueenSlimeBoss) | `life<=lifeMax/2` 时 `DrawNPCDirect_QueenSlimeWings`；`Extra[186]` 水晶(帧驱动 Y 偏移表，QueenSlime shader)；`ai[0]==4 && velocity.Y!=0` 时 8 层跳跃残影；`Extra[177]` 头顶饰(同一帧偏移表) | 详见 22318 辅助方法行 |
| 辅助方法 | 22318–22348 | (由 657 在半血以下调用) | `Extra[185]` 双翼(1×4，帧=`localAI[3]/6`)，scale 0.8，两翼互为 FlipHorizontally | 旋转=`rotation + clamp(velocity.Y,-6,6)*∓0.1`，翻转时绕 Bottom 旋转 |
| 本体 switch | 23301–23348 | `type==576/577`(DD2OgreT2/T3) | 本体 + 出生(`localAI[3]<60`)时 3 层紫色残影(固定偏移，`1-(t/60)²` 渐隐) | 残影数量由 localAI 控制 |
| 本体 switch | 23349–23379 | `type==696`(PalworldFoxsparksDistressed) | 本体(Frame 6×27) + 第 19 行帧以 `TileFrameSeed` 随机 ±1px 抖动、半透明白重画 2 次 | `ai[0]==2 && ai[1]<60` 时临时表情泡 |
| 本体 switch | 23380–23402 | `type==594`(WindyBalloon) | `Frame(8,1)` 气球本体 + 挂载史莱姆(`AI_113_WindyBalloon_GetSlaveNPC`) 整体(含 `DrawNPC_SlimeItem`)，scale=slave.scale，随 `rotation` 旋转 | slave 存在才画；slave 的 `ai[1]` 触发体内物品 |
| 本体 switch | 23413–23496 | `type==564/565`(DD2DarkMageT1/T3) | 出生 3 层紫色残影 + 4 层径向脉冲残影(半径 `4*(0.625±0.125sin)`) + `GlowMask[225]` 光环及 4 层径向拷贝 | `localAI[3]<60` 门禁；`Opacity>0` 门禁光环 |
| 本体 switch | 23497–23619 | `type==548`(DD2EterniaCrystal) | 3 组 4 层径向残影 + `GlowMask[239]` 顶部光环(`Center-40`) 双相位脉冲 + `Extra[89]` 竖直光束(旋转 +π/2，`dontTakeDamageFromHostiles` 时 Y 压 0.6) | `ai[1]==2 && ai[0]/120` 渐显；激活 `CrystalWin` 场景滤镜 |
| 本体 switch | 23642–23721 | `type==549`(DD2LanePortal) | 出生缩放(`localAI[0]<120`: scale 0.5→1) + 1 层轨道残影(`(ai[0]+54)%180` 相位) + `DrawElderEye`×3(22149，眼贴图按本体帧) | localAI/ai 混合驱动 |
| 委托 | 23722–23724 / 26364–26550 | `type==636`(HallowBoss = 光之女皇) | `Extra[159]` 翼(1×11，`localAI[0]/4`)、`Extra[157]`/`Extra[160]` 左右手臂(帧由 `DrawNPCDirect_GetHallowBossArmFrame`,26552 决定，帧 5 时换行)、`Extra[158]`、Phase2 时 `Extra[187]`(1×8) 与 `Extra[188]` 各 4 层径向克隆 | `ai[0]` 8/9/10 时 3D 旋转矩阵产生 7~9 个彩虹克隆(`ai[1]` 计时)；HallowBoss shader 包裹核心层 |
| 委托 | 23725–23727 / 26306–26362 | `type==677`(Shimmerfly) | 本体 4 层(第 0/1/2/3 行帧) + `oldPos` 采样拖尾(正弦横向摆动 `sin(whoAmI/17 + t/9 + i*2π)`) | 拖尾长度由 `oldPos` 距离 Remap 决定；hue 随时间流转 |
| 委托 | 23728–23730 / 26211–26296 | `type==668`(Deerclops) | 出生(`localAI[3]>0`) 2 层红色残影；`ai[0]` 7/8 时 5 层双层螺旋克隆(80px+30j px 双半径)；`Extra[245]` 红光覆盖 2 层 | `localAI[3]/36`、`ai[1]` 计时驱动 |
| 本体 switch | 23731–23847 | `type==422/493/507/517`(四座月塔) | `GlowMask[149]/[132]/[143]/[162]` 各 4 层 `velocity` 旋转 90° 步进残影 + 护盾:`Images/Misc/Perlin`(600×600) 经 ForceField shader | `ShieldStrengthTower*` 与 `ai[3]`(破碎动画)驱动强度/缩放；跳过 Bestiary |
| 本体 switch | 23848–23890 | `type==402`(StardustWormHead) | `oldPos` 反向双倍采样交替 `Npc[403]`(身)/`Npc[404]`(尾) 贴图 + `GlowMask[133]/[134]` 约 20 段长拖尾 + 本体 + `GlowMask[135]` + `DrawPrettyStarSparkle` | 中间段用前后帧位置/旋转插值；`ai[2]` 0→600 渐隐 |
| 本体 switch | 23891–23913 | `type==519`(SolarGoop) | 本体 + 粉色 `oldPos` 全长残影(缩放 `Lerp(0.3,1.1)`) | 残影 alpha 随索引 |
| 本体 switch | 23914–23936 | `type==522`(AncientLight) | 白色 `oldPos` 残影(缩放 0.8→0.3) + `Extra[57]` 本体覆盖 | 同上 |
| 本体 switch | 23937–24120 | `type==370/372/373`(DukeFishron/Sharkron/Sharkron2) | 本体 + `oldPos` 残影(步长 2，段数由 `ai[0]` 状态定：0/10 段) + `ai[0]` 3/8/4/9/12 时 6 层余弦轨道克隆(半径 20/40/60)；`type==370 && ai[0]>=4` 再用 `TextureAssets.DukeFishron`(狂暴贴图) 重画整套黄色残影+轨道+本体 | `ai[0]/ai[2]` 计时；ai[0] 1 时残影染蓝 |
| 本体 switch | 24121–24201 | `type==439/440`(CultistBoss/Clone) | `Extra[30]`(上半 2 帧) 残影(`ai[0]==-1 && ai[1]∈[320,960)` 或 `ai[0]==1`，步长 2) + `ai[0]==5 && ai[1]<30` 时 4 层 70px 余弦轨道克隆 | `ai[0]/ai[1]` 驱动 |
| 本体 switch | 24202–24229 | `type==392/394/395`(MartianSaucer/Cannon/Core) | 本体 + `GlowMask[48]`(392)/`GlowMask[50]`(394)/`GlowMask[49]`(395) 发光覆盖 | 平铺覆盖 |
| 本体 switch | 24263–24324 | `type==491`(PirateShip) | 骨架拼装:`Extra[40]`(1×4，`localAI[3]/8`)、`Extra[41]`(1×8)×5、`Extra[42]`×2、`Extra[43]`×2、`Extra[44]`、`Extra[45]`(相位 +2)，全部按固定偏移(±102/-384 等)再 `RotatedBy(rotation)`；另取 `Npc[492]`(船炮) 帧画 4 门炮，帧=`npc[ai[i]].frame.Y` | `ai[0..3]`=四门炮的 whoAmI；`localAI[3]` 驱动动画帧 |
| 本体 switch | 24325–24390 | `type==398`(MoonLordCore) | `Extra[13]` 腿×2(镜像 origin) + `Extra[14]` 手×2：对每个 `type==397`(MoonLordHand) NPC，从肩点 `(Center+(±220,-60))` 朝手做 0.5 收敛 + `acos(len/340)` 弯曲角(伪 IK);`Extra[16]` 心脏 + 本体 | `ai[2]`(397 侧)=0/1 选左右手 |
| 本体 switch | 24391–24448 | `type==397`(MoonLordHand) | `Extra[15]` 前臂：朝 `(npc[ai[3]].Center + (±220,-60))` 收敛 0.5 + `acos(len/340)` 弯曲；`ai[0]==-2` 时画 `Extra[26]`(充能帧=`ai[1]/8`)，否则 `Extra[17]` + `Extra[19]`(椭圆偏移 `(30,66)*localAI[1]`，角度=`localAI[0]`);最后本体 | `ai[2]`=0/1 左右手，`ai[3]`=MoonLordCore whoAmI |
| 本体 switch | 24449–24491 | `type==396`(MoonLordHead) | `ai[0]<0` 时 `Extra[26]`(帧=`ai[1]/8`)，否则 `Extra[18]`;`Extra[19]` 眼(椭圆 `(27,59)*localAI[1]`，角=`localAI[0]`);本体(3×3 帧，2 倍缩放);`Extra[29]`(帧=`localAI[3]/5`,offset `(0,4)`)+`Extra[25]`(帧=`localAI[2]/7`,offset `(0,214)`) | 全 localAI 驱动 |
| 本体 switch | 24492–24505 | `type==400`(MoonLordFreeEye) | `Extra[19]` 眼球：椭圆偏移 `(30,30)*localAI[1]`，角度 `localAI[0]`，缩放 `localAI[2]` | 无 |
| 本体 switch | 24506–24538 | `type==416`(SolarDrakomireRider) | 先把自身 Bottom 对齐到 `npc[ai[0]]`(需为 type 415 SolarDrakomire) 并借用其 gfxOffY/velocity，再画本体 + `GlowMask[156]` + 4 层 velocity 径向残影 | `ai[0]`=坐骑 whoAmI |
| 本体 switch | 24539–24573 | `type==399`(MartianProbe) | `Extra[27]` ×2 竖直光柱(旋转 π/2，origin `(10,48)`,缩放随 `(GlobalTime+i)%5` 4→0)；`GlowMask[100]`;`Extra[20]`(1×4，帧=`ai[0]+1`) + `GlowMask[101]` | 颜色:ai[0]==0 绿、1 绿→红(`ai[1]/20`)、2 红 |
| 本体 switch | 24574–24588 | `type==94`(Corruptor) | 本体 + `oldPos` 1,3,5 三层 shimmer 残影 | GetShimmerColor |
| 本体 switch | 24592–24604 | `type` 125–131、139(`ai[3]==0`)、140(机械 Boss 部件) | 本体 + `oldPos` 9→0(步长 2) 残影 | 纯拖尾 |
| 本体 switch | 24605–24617 | `type==417`(SolarSroller) `ai[0]==6` | `oldPos` 6→0 残影，用 `oldRot`，缩放 `Lerp(0.5,1)` | ai 门禁 |
| 本体 switch | 24618–24640 | `type==419`(SolarSolenian) `ai[2]<=-9` | `GlowMask[154]` 帧 5–7 循环的 7 段 `oldPos` 残影，缩放 0.75→1.2 | 帧号 `(当前帧-3-i) mod 3 + 5` |
| 本体 switch | 24641–24672 | `type==418`(SolarCorite) `ai[0]∈{2,4}` | `Extra[55]`(1×4) 7 段火焰拖尾，颜色 Gold→OrangeRed(随 `ai[1]/45`)→Blue | 旋转=`oldRot - π/2*spriteDirection`,帧号 `(ai[1]/2 - i) mod 4` |
| 本体 switch | 24673–24695 | `type==516`(SolarFlare) | 本体贴图帧错位 7 段残影，缩放 0.35→1.2 | 帧号 `(当前-4-i) mod 4` |
| 本体 switch | 24696–24703 | `type==390`(ScutlixRider) 且 `IsABestiaryIconDummy` | 在本体左侧 `(-width-8,+10)` 画 `Npc[391]`(Scutlix) 的第 `localAI[3]` 帧 | 仅图鉴 |
| 本体 switch | 24709–24726 | `type==420/421/423/424`(Nebula 系) | 本体 + 4 层正交方向残影(半径 `9+3cos(2πt)`,Teal,α/2) | GlobalTime 驱动 |
| 本体 switch | 24727–24744 | `type==662`(PirateGhost) | 8 层 `-velocity*10*α` 拖尾 + 4 层正交残影(半径 `4+2cos`) | Cyan,α/4 |
| 调用点 | 24746–24749 | `aiStyle==7`(城镇 NPC) | `DrawNPCExtras(beforeDraw:true)` | 见下方 DrawNPCExtras 行 |
| 本体 switch | 24750–24753 | `type==346`(SantaNK1) `life<50%` | 用 `TextureAssets.SantaTank` 替代本体贴图(坦克形态) | 形态切换 |
| 本体 switch | 24799–24843 | `type==266`(BrainofCthulhu) 受伤 且 expert/getGood | 本体 + 以本地玩家为中心做 4 次镜像(|ΔX|/|ΔY| 四象限反射)的拷贝 | alpha=失血比例²(专家×2,getGood=1) |
| 本体 switch | 24844–24853 | `type==421`(NebulaHeadcrab) `ai[0]==5` | 把本体 + `GlowMask[146]` 画到 `player[target]` 的 Top/Bottom(附身目标) | `player.gravDir==-1` 时 FlipVertically |
| 本体 switch | 24951–24976 | `aiStyle==7 && ai[0]==25` | ColorOnly 染料 shader 重绘本体 + 6 层彩虹轨道克隆(hslToRgb,半径 `4*Remap(ai[1],45,90)`) + 2 个 `DrawPrettyStarSparkle` | `ai[1]` 计时 |
| 本体 switch | 24995–25003 | `type==695` `ai[0]==2` | `EmoteBubble.DrawTemporaryBubble` | `ai[1]<60` |
| 本体 switch | 25008–25043 | `type==247/248`(GolemFistLeft/Right) | `ai[0]==1`: 3 层白脉冲缩放(`2→1.1+0.1i`,随 `ai[1]` 相位分段);`ai[0]==2`: 3 层 `-velocity*2i` 拖尾 + 3 层放大脉冲(渐隐 `ai[1]/30`) | ai 驱动 |
| 后置覆盖 | 25044–25047 | `type==24`(FireImp) | `GlowMask[360]` 发光覆盖 | 平铺 |
| 后置覆盖 | 25048–25055 | `type` 639–645(宝石松鼠)/ 646–652(宝石兔) | `GlowMask[286]` / `GlowMask[287]` 覆盖 | 平铺 |
| 后置覆盖 | 25056–25124 | `type` 134–136(TheDestroyer 系)/125/139/127/131 | 134–136:`Dest[i]` 覆盖(`npcColor!=Black` 门)；125:`EyeLaser`;139:`Probe`;127:`IsMechQueenUp` 时从 `GetMechQueenCenter()` 两个锚点(`(±18/20,-18).RotatedBy(rotation)`)向所有 125/126 循环画 `Chain12`(步长 40*scale)，否则 `BoneEyes`;131:`BoneLaser` | 链段用 `spriteBatch`(全局)而非 mySpriteBatch |
| 后置覆盖 | 25125–25139 | `type==120`(ChaosElemental) | `TextureAssets.Chaos` 沿 `oldPos` 全长 shimmer 拖尾 | GetShimmerColor |
| 后置覆盖 | 25140–25154 | `type==137/138`(IlluminantBat/Slime) | 本体沿 `oldPos` shimmer 拖尾 | 同上 |
| 后置覆盖 | 25155–25164 | `type==327`(Pumpking) | `PumpkingFace` 覆盖 + 9 份 ±2px 随机抖动拷贝(alpha 100→10) | 火光闪烁 |
| 后置覆盖 | 25165–25174 | `type==325`(MourningWood) | `TreeFace` 覆盖 + 9 份随机抖动拷贝 | 同上 |
| 后置覆盖 | 25175–25182 | `type==345`(IceQueen) | `IceQueen` 覆盖 + 4 层 `-velocity*0.2i` 拖尾 | 纯 velocity |
| 后置覆盖 | 25183–25190 | `type==355`(Firefly)/`type==358`(LightningBug) | `Firefly` / `Lightningbug` 发光覆盖 | 平铺 |
| 后置覆盖 | 25191–25198 | `type==654`(Lavafly)/`type==653`(HellButterfly) | `GlowMask[290]` / `GlowMask[288]` | 平铺 |
| 后置覆盖 | 25199–25214 | `type==82`(Wraith)/`type==253`(Reaper) | `WraithEye` + 9 层 `-velocity*0.5i` 拖尾；`ReaperEye` + 19 层拖尾 | 纯 velocity |
| 后置覆盖 | 25215–25218 | `type==245`(Golem) `alpha==0 && !getGoodWorld` | `Golem[3]` 覆盖(亮度=mouseTextColor) | 门禁较多 |
| 后置覆盖 | 25219–25240 | `type==246`(GolemHead) `!getGoodWorld` | `Golem[1]`(帧<222，左拳) 画在 `Center+(-20,-27)`;帧 222–444:`Golem[2]` 上半帧画在 `Center+(26,-28)`;之后 `Golem[2]` 下半帧画在 `Center+(-38,-28)`;第一段再叠 `Extra[107]`(frame6) | 固定屏幕偏移，无旋转 |
| 后置覆盖 | 25241–25257 | `type==249`(GolemHeadFree) `!getGoodWorld` | `Golem[1]` + `Extra[106]`(1×8，`frameCounter/4` 驱动且叠加本体 frame6) + `Extra[107]` | 同上 |
| 后置覆盖 | 25258–25266 | `type==383`(MartianOfficer) | `GlowMask[11]` + 若 `ai[2]` 关联的 `type==384`(ForceBubble) 存在则半透明画 `Npc[384]` 整图 | `ai[2]-1`=whoAmI |
| 后置覆盖 | 25267–25344 | `type==381`(BrainScrambler) | `Extra[0]`(32×42，行=`ai[2]-1`,空中固定行 3) + `GlowMask[24]`;位置按本体 9 帧的偏移表(每帧不同 X/Y) | 翻转时 X 取反、origin 镜像 |
| 后置覆盖 | 25345–25421 | `type==382`(RayGunner) | `Extra[1]`(30×42) 同上几何 | 同上 |
| 后置覆盖 | 25422–25444 | `type==520`(MartianWalker) | `GlowMask[164]` + `Extra[56]`(旋转=`localAI[3]`,FlipHorizontally 时 +π) + `GlowMask[165]` | 画在 `Top+(0,20)` |
| 后置覆盖 | 25445–25468 | `type==386/387/388/389`(火星炮台/无人机/电炮) | `GlowMask[31]` / `GlowMask[32]`(387 随 `ai[0]` 渐白渐隐)/ `GlowMask[33]` / `GlowMask[34]` | 平铺 |
| 后置覆盖 | 25469–25481 | `type==4`(EyeofCthulhu) `ai[1]>=4 && ai[0]==3`(旋转冲锋) | 本体 + `oldPos` 全长半透明残影 | ai 门禁 |
| 后置覆盖 | 25482–25488 | `type==437`(CultistTablet) | `GlowMask[109]`(带帧) + `GlowMask[108]`(整图) | 双层覆盖 |
| 后置覆盖 | 25489–25501 | `type==471`(GoblinSummoner) `ai[3]<0` | `oldPos` 全长残影 | ai 门禁 |
| 后置覆盖 | 25502–25521 | `type==477`(Mothron) `velocity>9` / `type==479`(MothronSpawn) `velocity>6.5` | 本体帧号错位 `-i*frameHeight mod` 的 `oldPos` 残影 | 速度门禁 |
| 后置覆盖 | 25542–25545 | `type==472`(ShadowFlameApparation) | `GlowMask[110]` | 平铺 |
| 后置覆盖 | 25546–25562 | `aiStyle==87 && ai[0]∈{4,5,6}` | 本体 + `oldPos` 全长 shimmer 残影 | ai 门禁 |
| 后置覆盖 | 25567–25596 | `type==50`(KingSlime) | `Extra[39]`(王冠) 画在 `Center + gfxOffY -(70-帧偏移)*scale`,帧偏移表 2/-6/2/10/2/0 | 王冠，按动画帧浮动 |
| 后置覆盖 | 25597–25789 | 一批发光覆盖/残影 | 411→`GlowMask[136]`;409→[138];410→[137];407→[139];405→[141];406→[142];424→[144];423→[145];421→[146];420→[147];425→[150]+绿色 `DrawPrettyStarSparkle`(`ai[3]` 驱动)；429→[151];418→[161]+4 层 velocity 径向残影；412/413/414→`GlowMask[157+i]`(414 用 `localAI[2]` 红化)；415→[155]+4 层 velocity 残影；419→[154]+4 层残影(`ai[2]<-6` 改为 4 向固定 4px 偏移)；417→[160]+4 层残影；516→本体+4 层残影；518→`GlowMask[163]`+4 层残影(origin X-10);344→[253];346→[254]+4 向残影；315(HeadlessHorseman)→[255]+4 向残影；525/526/527→[169]/[170]/[171];533→[172];160(Truffle)→[166](变体 `[352]`);209→[167](变体 `[350]/[351]` 按 altTexture) | 多数平铺；带 "+N 残影” 的为几何克隆 |
| 调用点 | 25791–25794 | `aiStyle==7` | `DrawNPCExtras(beforeDraw:false)` | 见下 |
| 辅助方法 | 26812–27360+ | `aiStyle==7`(两次调用) | 派对帽 `Extra[72]`(20 帧，`GetPartyHatColor` 选 16–19);`type==681`(TownSlimeRainbow) 叠 `Extra[250]`;`AttackType==1 && ai[0]==12`: 手持物品贴图(19/22/178/227/368 各自 itemtype 95/98、39、434、3350、2223/2269,origin 按 `DrawPlayerItemPos`),type 22 再叠 `Extra[52]`(1×5) 或 shimmer 变体 `Extra[264]`;`AttackType==2 && ai[0]==14/24`: `Extra[51]`(1×4，`frameCounter%48/12`) 施法光环；`AttackType==3 && ai[0]==15`: 207/353/441 各画 item 3349/3352/3351(用 `GetSwingStats` 挥舞轨迹，beforeDraw 决定 207/353/441 谁先谁后);`type==550 && ai[0]==18`: 画 Item[353](含玩家持卡检测与尘土)；`ai[0]==23`: 手持 `ai[2]` 物品(帧偏移 1/2 两态，369/453/550 特例) | 大量 per-type 帽子/手持偏移表 + shimmer 修正 |
| 本体 switch | 25803–26207 | 大类：426/427/428/521/523/541–545/546/552–563/566/567/568/569/570–575/578/581/618/620/661/558–560 | 通用残影引擎：`oldPos` 拖尾(数量/步长/缩放目标 per-type)+ 径向轨道克隆(num299/num301/num300 配置)。各类型：558–560/574/575(`DD2Wyvern`/`KoboldFlyer`) `ai[0]==2` → 6 段拖尾；566/567/578 无残影；552–563/570/571/572/573 仅偏移/翻转；426(VortexHornetQueen) 4 层绿松石轨道 + 6 段拖尾；427(VortexHornet) 8 段拖尾；546(Tumbleweed) 8 段拖尾(缩放→0.3);542–545(SandShark 系) 6 段(步长 3);581(FlyingAntlion) 6 段；521(AncientCultistSquidhead) 10 段+oldRot；523(AncientDoom) 3 层半径 `10*scale` 轨道(角度/半径由 `localAI[0]/[1]` 提供)；620(GoblinShark) 6 层金色轨道+origin 偏移+6 段拖尾 | 见附加行 |
| 本体 switch | 26074–26082 | 上述大类中的 426/427 | `GlowMask[153]` / `GlowMask[152]` 覆盖 | 平铺 |
| 本体 switch | 26083–26097 | 上述大类中的 541(SandElemental) | `GlowMask[216]` 金色 4 层轨道克隆 + 本体层 | `num300` 余弦脉冲 |
| 本体 switch | 26098–26114 | 上述大类中的 661(EmpressButterfly) | 6 层彩虹轨道克隆(hslToRgb，半径 `(2+ai[2])*num300+2`) + 本体 10% 白 | `ai[2]` 相位(0→60 lerp 0..3) |
| 本体 switch | 26115–26155 | 上述大类中的 568/569(WitherBeast) `localAI[3]>=60` | `GlowMask[224]` 轨道克隆 + 本体层；`localAI[0]>0` 时 `Extra[89]` 16 根 400px 半径的旋转光束环(角速 `localAI[0]*0.004189`,相位 i/16·2π) | localAI 全驱动 |
| 本体 switch | 26156–26159 | 上述大类中的 546(Tumbleweed) | `Extra[76]` 覆盖(旋转=clamp(velocity.X*0.1, ±π/8)) | 草屑贴图 |
| 本体 switch | 26160–26201 | 上述大类中的 566/567(Skeleton) `localAI[3]>=115` | `Extra[80]`(1×4，帧=`GlobalTime%0.5/0.5*4`) 画在头顶 `(spriteDirection*8,-26+帧修正)`，scale 0.7 | 头顶装饰 |
| 本体 switch | 25987–26038 / 26202–26205 | 上述大类中的 618(BloodNautilus) | `ai[0]==1 && ai[1]<90` 时配置 6 层半径 15 轨道；`ai[0]==3 && ai[1]<180` 时 `Extra[59]` 两圈共 8 根径向漩涡(椭圆缩放 `1×(0.5+0.75t)`,旋转=相位角);最后叠 `Extra[129]` 覆盖 | ai 计时驱动 |

## 补充说明

- **方法边界**:`DrawNPCs` 22159–22301;`DrawNPC` 22311–22316(仅转发);`DrawNPCDirect` 22350–26209;专属辅助:`DrawNPCDirect_QueenSlimeWings` 22318、`DrawNPCDirect_Deerclops` 26211、`DrawNPCDirect_DeerclopsLeg` 26298(定义未见调用)、`DrawNPCDirect_Faeling` 26306、`DrawNPCDirect_HallowBoss` 26364(含 `DrawNPCDirect_GetHallowBossArmFrame` 26552)、`DrawNPC_SlimeItem` 26709、`DrawNPCExtras` 26812、`DrawElderEye` 22149。22159 之前与 26209 之后(除上述辅助)没有其它 NPC 附属叠画逻辑。
- **已剔除**(按要求):`nameOver` 名字显隐(22354–22390)、`npcColor`/alpha 修正(22742–22797)、`num45/num46/num47`/halfSize 位置补偿(22849–22978)、`aiStyle==10/type==72` 的纯白化(22980)、RainbowTownSlime 纯 shader 分支 676/681(24868–24903)、685 的挤压变形与像素吸附(24904–24939)、`confused` 的 Confuse 图标(25004,对所有 NPC 生效)、655/360/356/267 等纯贴图/位置分支。
- **两个“会改状态”的特例**值得注意:`aiStyle==20`(22719)会直接写回 `npc.rotation`;`type==416`(24519–24523)会临时改写 `rCurrentNPC.Bottom/gfxOffY` 后再复原。
- **链段族通用模式**:`Chain*` 系列都是“从部件中心向目标点按固定步进前进、每段独立采样光照、最后一段裁剪高度”的同构 while 循环；`acos(len/臂长)` 弯曲只出现在月总手/核心(397/398)这对伪 IK 上。
```
