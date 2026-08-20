# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-13T06:14:46.037Z

```
你在审计泰拉瑞亚 1:1 移植项目的【发光物光源全量对账】。这是三路代理中的【第一路：tile/墙/液体光源】。光照引擎本体（LightingEngine/LightMap 扫描 Blur）此前已 1:1 移植过，本次只审【光源端】——哪些物体发光、发光条件、发光颜色/强度。

本仓实现：
- `game/src/lighting/TileLightScanner.ts`（播种扫描器主干 + specialTileLight 动态特例）
- `game/src/lighting/lightTables.ts`（火把色 TORCH_COLORS、发光墙 WALL_EMISSIVE、透光墙 WALL_LIGHT、蘑菇组 MUSHROOM_GLOW_SHEETS、闪烁族 FLICKER_SHEETS、月相地板 MOON_FLOOR、衰减表）
- `game/src/data/tiles.ts` 每个 tile def 的 `light?: [r,g,b]` 静态字段（0-255 RGB 注释说从 TileLightScanner ApplyTileLight 提取）

原版标杆：`Terarria1456/Terraria/Graphics.Light/TileLightScanner.cs`（核心扫描器）+ `Terraria/Main.cs`（wallLight :10487-10503）+ `Terraria.ID/TorchID.cs`（:134-161 _lights）+ `Terraria/TileLoader.cs`。

审计任务（very thorough）：
1. **静态 tile 光源覆盖率**：TileLightScanner.cs 的 `ApplyTileLight`（约 :2900-3200+ 的巨型 switch，逐 tile case）——列出原版全部发光 tile 的 case 清单（tile id、发光条件如 frameX 门禁、颜色三元组）。然后对照本仓：tiles.ts 的 light 字段 + lightTables + TileLightScanner 特例，逐条判定 已实现/数值偏差/缺失。**特别核对发光条件**（如灯笼 frameX!=0 不发光、灯泡 frameX 位段逻辑、迪斯科球动态色）。
2. **发光墙 WALL_EMISSIVE 全表对账**：原版 ApplyWallLight（TileLightScanner.cs :167-342 附近）每个发光墙的 RGB 与本仓 19 条对照，找出缺失的墙/数值偏差。
3. **火把色表 TORCH_COLORS 24 条逐值对照** TorchID.cs:134-161（注意原版有 1.4.5 新增火把色没有？查 _lights 数组长度与注释的 22+2 动态）。
4. **液体光源**：岩浆（ApplyHellLight :3261 与 tile 48/137 熔岩块 :110 附近 lavaV 0.55+(270-mouse)/900）、水微光——本仓 TileLightScanner.ts:164/185/263 有实现，对照原版公式。
5. **WALL_LIGHT 透光墙全表**对照 Main.cs:10487-10503（本仓 14 条，原版 wallLight bool[] 全表）。

输出：五节结构化报告，每条 [原版行号+值, 本仓文件:行号+值, 判定 一致/偏差(N)/缺失]。数值精确到 3 位小数。不要贴大段代码。
```

---

## 📎 Attachment · skill_listing · 2026-08-13T06:14:46.040Z

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

## 🤖 Assistant · 2026-08-13T06:14:48.152Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This is a thorough audit task. I need to compare the repo's implementation (game/src/lighting/TileLightScanner.ts, lightTables.ts, game/src/data/tiles.ts) against the vanilla Terraria source (Terarria1456/Terraria). Let me first find the vanilla source files. The working directory is ~/Project/GLM/SandboxWorld/game. The vanilla benchmark is at Terarria1456/Terraria/... — I need to find where that is on disk. Probably a sibling directory like ~/Project/GLM/SandboxWorld/Terarria1456 or similar.

Let me start by exploring.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:14:49.041Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/ && ls ~/Project/GLM/SandboxWorld/game/src/lighting/ && find ~/Project/GLM/SandboxWorld -maxdepth 2 -iname \"*Terraria*\" -o -maxdepth 2 -iname \"*1456*\" 2>/dev/null | head -20",
 "description": "Locate vanilla Terraria source and lighting files"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:14:49.321Z

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
FastRandom.ts
LightingEngine.ts
LightMap.ts
lightTables.ts
SkyColor.ts
TileLightScanner.ts
~/Project/GLM/SandboxWorld/Terarria1456Server
~/Project/GLM/SandboxWorld/Terarria1456
~/Project/GLM/SandboxWorld/terraria-wiki-md
~/Project/GLM/SandboxWorld/terraria.wiki.gg_en_all_2026-07a.zim
~/Project/GLM/SandboxWorld/terraria-assets
~/Project/GLM/SandboxWorld/Terraria-Map-Editor
~/Project/GLM/SandboxWorld/Terarria1456Server/Terraria.IO.Data.ResourcePacksDefaultInfo.tsv
~/Project/GLM/SandboxWorld/Terarria1456Server/Terraria.GameContent.Liquid
~/Project/GLM/SandboxWorld/Terarria1456Server/Terraria.Localization.Content.ru-RU.Projectiles.json
~/Project/GLM/SandboxWorld/Terarria1456Server/Terraria.Localization.Content.zh-Hant.Game.json
~/Project/GLM/SandboxWorld/Terarria1456Server/Terraria.Localization.Content.ru-RU.Game.json
~/Project/GLM/SandboxWorld/Terarria1456Server/Terraria.Localization.Content.pl-PL.NPCs.json
~/Project/GLM/SandboxWorld/Terarria1456Server/Terraria.GameContent.RGB
~/Project/GLM/SandboxWorld/Terarria1456Server/Terraria.GameContent.Creative.Content.Sacrifices.tsv
~/Project/GLM/SandboxWorld/Terarria1456Server/Terraria.Properties
~/Project/GLM/SandboxWorld/Terarria1456Server/Terraria.Localization.Content.pl-PL.json
~/Project/GLM/SandboxWorld/Terarria1456Server/Terraria.Localization.Content.fr-FR.NPCs.json
~/Project/GLM/SandboxWorld/Terarria1456Server/Terraria.Localization.Content.pl-PL.Projectiles.json
~/Project/GLM/SandboxWorld/Terarria1456Server/Terraria.Achievements
~/Project/GLM/SandboxWorld/Terarria1456Server/Terraria.GameContent.LeashedEntities

```


---

## 🤖 Assistant · 2026-08-13T06:14:51.012Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Graphics/Light/ 2>/dev/null; ls ~/Project/GLM/SandboxWorld/Terarria1456/ | head; wc -l ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Graphics.Light.TileLightScanner.cs 2>/dev/null",
 "description": "Inspect vanilla source layout"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:14:51.248Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
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

```


---

## 🤖 Assistant · 2026-08-13T06:14:51.564Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/game/src/lighting/TileLightScanner.ts ~/Project/GLM/SandboxWorld/game/src/lighting/lightTables.ts ~/Project/GLM/SandboxWorld/game/src/data/tiles.ts",
 "description": "Count lines of repo lighting files"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:14:51.700Z

**📎 ToolResult**

```
     278 ~/Project/GLM/SandboxWorld/game/src/lighting/TileLightScanner.ts
     118 ~/Project/GLM/SandboxWorld/game/src/lighting/lightTables.ts
    1297 ~/Project/GLM/SandboxWorld/game/src/data/tiles.ts
    1693 total

```


---

## 🤖 Assistant · 2026-08-13T06:14:52.772Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The vanilla Terraria dir has files flattened with dots. Let me find TileLightScanner.cs.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:14:53.437Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/Terarria1456 -iname \"*TileLightScanner*\" -o -iname \"*TorchID*\" | head; find ~/Project/GLM/SandboxWorld/Terarria1456 -iname \"Main.cs\" -o -iname \"*TileLoader*\" | head",
 "description": "Find vanilla scanner, TorchID, Main.cs, TileLoader"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:14:53.656Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TorchID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScannerOptions.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs

```


---

## 🤖 Assistant · 2026-08-13T06:15:05.988Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:15:06.281Z

**📎 ToolResult**

```
1	using System;
2	using Microsoft.Xna.Framework;
3	using ReLogic.Threading;
4	using Terraria.GameContent;
5	using Terraria.GameContent.Liquid;
6	using Terraria.ID;
7	using Terraria.Utilities;
8	
9	namespace Terraria.Graphics.Light;
10	
11	public class TileLightScanner
12	{
13		private FastRandom _random = FastRandom.CreateWithRandomSeed();
14	
15		private bool _drawInvisibleWalls;
16	
17		public void ExportTo(Rectangle area, LightMap outputMap, TileLightScannerOptions options)
18		{
19			//IL_0044: Unknown result type (might be due to invalid IL or missing references)
20			//IL_004f: Expected O, but got Unknown
21			_drawInvisibleWalls = options.DrawInvisibleWalls;
22			FastParallel.For(area.Left, area.Right, (ParallelForAction)delegate(int start, int end, object context)
23			{
24				for (int i = start; i < end; i++)
25				{
26					for (int j = area.Top; j < area.Bottom; j++)
27					{
28						if (IsTileNullOrTouchingNull(i, j))
29						{
30							outputMap.SetMaskAt(i - area.X, j - area.Y, LightMaskMode.None);
31							outputMap[i - area.X, j - area.Y] = Vector3.Zero;
32						}
33						else
34						{
35							LightMaskMode tileMask = GetTileMask(Main.tile[i, j]);
36							outputMap.SetMaskAt(i - area.X, j - area.Y, tileMask);
37							GetTileLight(i, j, out var outputColor);
38							outputMap[i - area.X, j - area.Y] = outputColor;
39						}
40					}
41				}
42			}, (object)null);
43		}
44	
45		private bool IsTileNullOrTouchingNull(int x, int y)
46		{
47			if (WorldGen.InWorld(x, y, 1))
48			{
49				if (Main.tile[x, y] != null && Main.tile[x + 1, y] != null && Main.tile[x - 1, y] != null && Main.tile[x, y - 1] != null)
50				{
51					return Main.tile[x, y + 1] == null;
52				}
53				return true;
54			}
55			return true;
56		}
57	
58		public void Update()
59		{
60			_random.NextSeed();
61		}
62	
63		public LightMaskMode GetMaskMode(int x, int y)
64		{
65			return GetTileMask(Main.tile[x, y]);
66		}
67	
68		private LightMaskMode GetTileMask(Tile tile)
69		{
70			if (LightIsBlocked(tile) && tile.type != 131 && !tile.inActive() && tile.slope() == 0)
71			{
72				if (TileID.Sets.CrackedBricks[tile.type])
73				{
74					return LightMaskMode.CrackedBricks;
75				}
76				return LightMaskMode.Solid;
77			}
78			if (!tile.lava() && tile.liquid > 128)
79			{
80				if (!tile.honey())
81				{
82					return LightMaskMode.Water;
83				}
84				return LightMaskMode.Honey;
85			}
86			return LightMaskMode.None;
87		}
88	
89		public void GetTileLight(int x, int y, out Vector3 outputColor)
90		{
91			outputColor = Vector3.Zero;
92			Tile tile = Main.tile[x, y];
93			FastRandom localRandom = _random.WithModifier(x, y);
94			if (y <= (int)Main.worldSurface)
95			{
96				ApplySurfaceLight(tile, x, y, ref outputColor);
97			}
98			else if (y > Main.UnderworldLayer)
99			{
100				ApplyHellLight(tile, x, y, ref outputColor);
101			}
102			ApplyWallLight(tile, x, y, ref localRandom, ref outputColor);
103			if (tile.active())
104			{
105				ApplyTileLight(tile, x, y, ref localRandom, ref outputColor);
106			}
107			ApplyLiquidLight(tile, ref outputColor);
108		}
109	
110		private void ApplyLiquidLight(Tile tile, ref Vector3 lightColor)
111		{
112			if (tile.liquid <= 0)
113			{
114				return;
115			}
116			if (tile.lava())
117			{
118				float num = 0.55f;
119				num += (float)(270 - Main.mouseTextColor) / 900f;
120				if (lightColor.X < num)
121				{
122					lightColor.X = num;
123				}
124				if (lightColor.Y < num)
125				{
126					lightColor.Y = num * 0.6f;
127				}
128				if (lightColor.Z < num)
129				{
130					lightColor.Z = num * 0.2f;
131				}
132			}
133			else if (tile.shimmer())
134			{
135				float num2 = 0.7f;
136				float num3 = 0.7f;
137				num2 += (float)(270 - Main.mouseTextColor) / 900f;
138				num3 += (float)(270 - Main.mouseTextColor) / 125f;
139				if (lightColor.X < num2)
140				{
141					lightColor.X = num2 * 0.6f;
142				}
143				if (lightColor.Y < num3)
144				{
145					lightColor.Y = num3 * 0.25f;
146				}
147				if (lightColor.Z < num2)
148				{
149					lightColor.Z = num2 * 0.9f;
150				}
151			}
152		}
153	
154		private bool LightIsBlocked(Tile tile)
155		{
156			if (tile.active() && Main.tileBlockLight[tile.type])
157			{
158				if (tile.invisibleBlock())
159				{
160					return _drawInvisibleWalls;
161				}
162				return true;
163			}
164			return false;
165		}
166	
167		private void ApplyWallLight(Tile tile, int x, int y, ref FastRandom localRandom, ref Vector3 lightColor)
168		{
169			float num = 0f;
170			float num2 = 0f;
171			float num3 = 0f;
172			bool flag = false;
173			switch (tile.wall)
174			{
175			case 357:
176				if (!LightIsBlocked(tile))
177				{
178					num = 0.15f;
179					num2 = 0.27f;
180					num3 = 0.3f;
181					flag = true;
182				}
183				break;
184			case 182:
185				if (!LightIsBlocked(tile))
186				{
187					num = 0.24f;
188					num2 = 0.12f;
189					num3 = 0.089999996f;
190				}
191				break;
192			case 33:
193				if (!LightIsBlocked(tile))
194				{
195					num = 0.089999996f;
196					num2 = 0.052500002f;
197					num3 = 0.24f;
198				}
199				break;
200			case 174:
201				if (!LightIsBlocked(tile))
202				{
203					num = 0.2975f;
204				}
205				break;
206			case 175:
207				if (!LightIsBlocked(tile))
208				{
209					if (tile.wallColor() == 0)
210					{
211						num = 0.075f;
212						num2 = 0.15f;
213						num3 = 0.4f;
214					}
215					else
216					{
217						flag = true;
218					}
219				}
220				break;
221			case 176:
222				if (!LightIsBlocked(tile))
223				{
224					num = 0.1f;
225					num2 = 0.1f;
226					num3 = 0.1f;
227				}
228				break;
229			case 137:
230				if (!LightIsBlocked(tile))
231				{
232					float num4 = 0.4f;
233					num4 += (float)(270 - Main.mouseTextColor) / 1500f;
234					num4 += (float)localRandom.Next(0, 50) * 0.0005f;
235					num = 1f * num4;
236					num2 = 0.5f * num4;
237					num3 = 0.1f * num4;
238				}
239				break;
240			case 44:
241				if (!LightIsBlocked(tile))
242				{
243					num = (float)Main.DiscoR / 255f * 0.15f;
244					num2 = (float)Main.DiscoG / 255f * 0.15f;
245					num3 = (float)Main.DiscoB / 255f * 0.15f;
246				}
247				break;
248			case 154:
249				num = 0.6f;
250				num3 = 0.6f;
251				break;
252			case 166:
253				num = 0.6f;
254				num2 = 0.6f;
255				break;
256			case 165:
257				num3 = 0.6f;
258				break;
259			case 156:
260				num2 = 0.6f;
261				break;
262			case 164:
263				num = 0.6f;
264				break;
265			case 155:
266				num = 0.6f;
267				num2 = 0.6f;
268				num3 = 0.6f;
269				break;
270			case 153:
271				num = 0.6f;
272				num2 = 0.3f;
273				break;
274			case 341:
275				if (!LightIsBlocked(tile))
276				{
277					num = 0.25f;
278					num2 = 0.1f;
279					num3 = 0f;
280				}
281				break;
282			case 343:
283				if (!LightIsBlocked(tile))
284				{
285					num = 0f;
286					num2 = 0.25f;
287					num3 = 0f;
288				}
289				break;
290			case 344:
291				if (!LightIsBlocked(tile))
292				{
293					num = 0f;
294					num2 = 0.16f;
295					num3 = 0.34f;
296				}
297				break;
298			case 342:
299				if (!LightIsBlocked(tile))
300				{
301					num = 0.3f;
302					num2 = 0f;
303					num3 = 0.17f;
304				}
305				break;
306			case 345:
307				if (!LightIsBlocked(tile))
308				{
309					num = 0.3f;
310					num2 = 0f;
311					num3 = 0.35f;
312				}
313				break;
314			case 346:
315				if (!LightIsBlocked(tile))
316				{
317					num = (float)Main.DiscoR / 255f * 0.25f;
318					num2 = (float)Main.DiscoG / 255f * 0.25f;
319					num3 = (float)Main.DiscoB / 255f * 0.25f;
320				}
321				break;
322			}
323			if (flag && tile.wallColor() != 0)
324			{
325				Color color = WorldGen.paintColor(tile.wallColor());
326				num = (float)(int)color.R / 765f;
327				num2 = (float)(int)color.G / 765f;
328				num3 = (float)(int)color.B / 765f;
329			}
330			if (lightColor.X < num)
331			{
332				lightColor.X = num;
333			}
334			if (lightColor.Y < num2)
335			{
336				lightColor.Y = num2;
337			}
338			if (lightColor.Z < num3)
339			{
340				lightColor.Z = num3;
341			}
342		}
343	
344		private void ApplyTileLight(Tile tile, int x, int y, ref FastRandom localRandom, ref Vector3 lightColor)
345		{
346			float R = 0f;
347			float G = 0f;
348			float B = 0f;
349			bool flag = false;
350			if (Main.tileLighted[tile.type])
351			{
352				switch (tile.type)
353				{
354				case 658:
355					if (!tile.invisibleBlock())
356					{
357						TorchID.TorchColor(23, out R, out G, out B);
358						switch (tile.frameY / 54)
359						{
360						default:
361							R *= 0.2f;
362							G *= 0.2f;
363							B *= 0.2f;
364							break;
365						case 1:
366							R *= 0.3f;
367							G *= 0.3f;
368							B *= 0.3f;
369							break;
370						case 2:
371							R *= 0.1f;
372							G *= 0.1f;
373							B *= 0.1f;
374							break;
375						}
376					}
377					break;
378				case 356:
379					if (Main.sundialCooldown == 0)
380					{
381						R = 0.45f;
382						G = 0.25f;
383						B = 0f;
384					}
385					break;
386				case 663:
387					if (Main.moondialCooldown == 0)
388					{
389						R = 0f;
390						G = 0.25f;
391						B = 0.45f;
392					}
393					break;
394				case 656:
395					R = 0.2f;
396					G = 0.55f;
397					B = 0.5f;
398					break;
399				case 20:
400				{
401					int num28 = tile.frameX / 18;
402					if (num28 >= 30 && num28 <= 32)
403					{
404						R = 0.325f;
405						G = 0.15f;
406						B = 0.05f;
407					}
408					break;
409				}
410				case 634:
411					R = 0.65f;
412					G = 0.3f;
413					B = 0.1f;
414					break;
415				case 633:
416				case 637:
417				case 638:
418					R = 0.325f;
419					G = 0.15f;
420					B = 0.05f;
421					break;
422				case 463:
423					R = 0.2f;
424					G = 0.4f;
425					B = 0.8f;
426					break;
427				case 491:
428					R = 0.5f;
429					G = 0.4f;
430					B = 0.7f;
431					break;
432				case 209:
433					if (tile.frameX == 234 || tile.frameX == 252)
434					{
435						Vector3 vector11 = PortalHelper.GetPortalColor(Main.myPlayer, 0).ToVector3() * 0.65f;
436						R = vector11.X;
437						G = vector11.Y;
438						B = vector11.Z;
439					}
440					else if (tile.frameX == 306 || tile.frameX == 324)
441					{
442						Vector3 vector12 = PortalHelper.GetPortalColor(Main.myPlayer, 1).ToVector3() * 0.65f;
443						R = vector12.X;
444						G = vector12.Y;
445						B = vector12.Z;
446					}
447					break;
448				case 415:
449					R = 0.7f;
450					G = 0.5f;
451					B = 0.1f;
452					break;
453				case 500:
454					R = 0.525f;
455					G = 0.375f;
456					B = 0.075f;
457					break;
458				case 416:
459					R = 0f;
460					G = 0.6f;
461					B = 0.7f;
462					break;
463				case 501:
464					R = 0f;
465					G = 0.45f;
466					B = 0.525f;
467					break;
468				case 417:
469					R = 0.6f;
470					G = 0.2f;
471					B = 0.6f;
472					break;
473				case 502:
474					R = 0.45f;
475					G = 0.15f;
476					B = 0.45f;
477					break;
478				case 418:
479					R = 0.6f;
480					G = 0.6f;
481					B = 0.9f;
482					break;
483				case 503:
484					R = 0.45f;
485					G = 0.45f;
486					B = 0.675f;
487					break;
488				case 390:
489					R = 0.4f;
490					G = 0.2f;
491					B = 0.1f;
492					break;
493				case 597:
494					switch (tile.frameX / 54)
495					{
496					case 0:
497						R = 0.05f;
498						G = 0.8f;
499						B = 0.3f;
500						break;
501					case 1:
502						R = 0.7f;
503						G = 0.8f;
504						B = 0.05f;
505						break;
506					case 2:
507						R = 0.7f;
508						G = 0.5f;
509						B = 0.9f;
510						break;
511					case 3:
512						R = 0.6f;
513						G = 0.6f;
514						B = 0.8f;
515						break;
516					case 4:
517						R = 0.4f;
518						G = 0.4f;
519						B = 1.15f;
520						break;
521					case 5:
522						R = 0.85f;
523						G = 0.45f;
524						B = 0.1f;
525						break;
526					case 6:
527						R = 0.8f;
528						G = 0.8f;
529						B = 1f;
530						break;
531					case 7:
532						R = 0.5f;
533						G = 0.8f;
534						B = 1.2f;
535						break;
536					}
537					R *= 0.75f;
538					G *= 0.75f;
539					B *= 0.75f;
540					break;
541				case 564:
542					if (tile.frameX < 36)
543					{
544						R = 0.05f;
545						G = 0.3f;
546						B = 0.55f;
547					}
548					break;
549				case 568:
550					R = 1f;
551					G = 0.61f;
552					B = 0.65f;
553					break;
554				case 569:
555					R = 0.12f;
556					G = 1f;
557					B = 0.66f;
558					break;
559				case 570:
560					R = 0.57f;
561					G = 0.57f;
562					B = 1f;
563					break;
564				case 580:
565					R = 0.7f;
566					G = 0.3f;
567					B = 0.2f;
568					break;
569				case 391:
570					R = 0.3f;
571					G = 0.1f;
572					B = 0.25f;
573					break;
574				case 381:
575				case 517:
576				case 687:
577					R = 0.25f;
578					G = 0.1f;
579					B = 0f;
580					break;
581				case 534:
582				case 535:
583				case 689:
584					R = 0f;
585					G = 0.25f;
586					B = 0f;
587					break;
588				case 536:
589				case 537:
590				case 690:
591					R = 0f;
592					G = 0.16f;
593					B = 0.34f;
594					break;
595				case 539:
596				case 540:
597				case 688:
598					R = 0.3f;
599					G = 0f;
600					B = 0.17f;
601					break;
602				case 625:
603				case 626:
604				case 691:
605					R = 0.3f;
606					G = 0f;
607					B = 0.35f;
608					break;
609				case 627:
610				case 628:
611				case 692:
612					R = (float)Main.DiscoR / 255f * 0.25f;
613					G = (float)Main.DiscoG / 255f * 0.25f;
614					B = (float)Main.DiscoB / 255f * 0.25f;
615					break;
616				case 184:
617					if (tile.frameX == 110)
618					{
619						R = 0.25f;
620						G = 0.1f;
621						B = 0f;
622					}
623					if (tile.frameX == 132)
624					{
625						R = 0f;
626						G = 0.25f;
627						B = 0f;
628					}
629					if (tile.frameX == 154)
630					{
631						R = 0f;
632						G = 0.16f;
633						B = 0.34f;
634					}
635					if (tile.frameX == 176)
636					{
637						R = 0.3f;
638						G = 0f;
639						B = 0.17f;
640					}
641					if (tile.frameX == 198)
642					{
643						R = 0.3f;
644						G = 0f;
645						B = 0.35f;
646					}
647					if (tile.frameX == 220)
648					{
649						R = (float)Main.DiscoR / 255f * 0.25f;
650						G = (float)Main.DiscoG / 255f * 0.25f;
651						B = (float)Main.DiscoB / 255f * 0.25f;
652					}
653					break;
654				case 370:
655					R = 0.32f;
656					G = 0.16f;
657					B = 0.12f;
658					break;
659				case 659:
660				case 667:
661				case 708:
662				{
663					Vector4 shimmerBaseColor = LiquidRenderer.GetShimmerBaseColor(x, y);
664					R = shimmerBaseColor.X;
665					G = shimmerBaseColor.Y;
666					B = shimmerBaseColor.Z;
667					break;
668				}
669				case 711:
670					R = 0.01f;
671					G = 0.01f;
672					B = 0.01f;
673					break;
674				case 27:
675					if (tile.frameY < 36)
676					{
677						R = 0.3f;
678						G = 0.27f;
679					}
680					break;
681				case 336:
682					R = 0.85f;
683					G = 0.5f;
684					B = 0.3f;
685					break;
686				case 340:
687					R = 0.45f;
688					G = 1f;
689					B = 0.45f;
690					break;
691				case 341:
692					R = 0.4f * Main.demonTorch + 0.6f * (1f - Main.demonTorch);
693					G = 0.35f;
694					B = 1f * Main.demonTorch + 0.6f * (1f - Main.demonTorch);
695					break;
696				case 342:
697					R = 0.5f;
698					G = 0.5f;
699					B = 1.1f;
700					break;
701				case 343:
702					R = 0.85f;
703					G = 0.85f;
704					B = 0.3f;
705					break;
706				case 344:
707					R = 0.6f;
708					G = 1.026f;
709					B = 0.96000004f;
710					break;
711				case 327:
712				{
713					float num13 = 0.5f;
714					num13 += (float)(270 - Main.mouseTextColor) / 1500f;
715					num13 += (float)localRandom.Next(0, 50) * 0.0005f;
716					R = 1f * num13;
717					G = 0.5f * num13;
718					B = 0.1f * num13;
719					break;
720				}
721				case 316:
722				case 317:
723				case 318:
724				{
725					int num19 = x - tile.frameX / 18;
726					int num20 = y - tile.frameY / 18;
727					int num21 = num19 / 3 * (num20 / 3);
728					num21 %= Main.cageFrames;
729					int num22 = tile.type - 316;
730					bool flag5 = Main.jellyfishCageMode[num22, num21] == 2;
731					if (tile.type == 316)
732					{
733						if (flag5)
734						{
735							R = 0.2f;
736							G = 0.3f;
737							B = 0.8f;
738						}
739						else
740						{
741							R = 0.1f;
742							G = 0.2f;
743							B = 0.5f;
744						}
745					}
746					if (tile.type == 317)
747					{
748						if (flag5)
749						{
750							R = 0.2f;
751							G = 0.7f;
752							B = 0.3f;
753						}
754						else
755						{
756							R = 0.05f;
757							G = 0.45f;
758							B = 0.1f;
759						}
760					}
761					if (tile.type == 318)
762					{
763						if (flag5)
764						{
765							R = 0.7f;
766							G = 0.2f;
767							B = 0.5f;
768						}
769						else
770						{
771							R = 0.4f;
772							G = 0.1f;
773							B = 0.25f;
774						}
775					}
776					break;
777				}
778				case 719:
779				{
780					int num15 = (x + y + (int)(Main.GlobalTimeWrappedHourly * 15f)) % 14;
781					float num16 = 0f;
782					float num17 = 0f;
783					float num18 = 0f;
784					switch (num15)
785					{
786					case 0:
787						num16 = 255f;
788						num17 = 171f;
789						num18 = 183f;
790						break;
791					case 1:
792						num16 = 255f;
793						num17 = 170f;
794						num18 = 220f;
795						break;
796					case 2:
797						num16 = 252f;
798						num17 = 171f;
799						num18 = 255f;
800						break;
801					case 3:
802						num16 = 224f;
803						num17 = 171f;
804						num18 = 255f;
805						break;
806					case 4:
807						num16 = 192f;
808						num17 = 171f;
809						num18 = 255f;
810						break;
811					case 5:
812						num16 = 174f;
813						num17 = 178f;
814						num18 = 255f;
815						break;
816					case 6:
817						num16 = 168f;
818						num17 = 195f;
819						num18 = 255f;
820						break;
821					case 7:
822						num16 = 167f;
823						num17 = 224f;
824						num18 = 255f;
825						break;
826					case 8:
827						num16 = 168f;
828						num17 = 255f;
829						num18 = 252f;
830						break;
831					case 9:
832						num16 = 162f;
833						num17 = 255f;
834						num18 = 233f;
835						break;
836					case 10:
837						num16 = 158f;
838						num17 = 255f;
839						num18 = 198f;
840						break;
841					case 11:
842						num16 = 207f;
843						num17 = 255f;
844						num18 = 173f;
845						break;
846					case 12:
847						num16 = 255f;
848						num17 = 213f;
849						num18 = 186f;
850						break;
851					case 13:
852						num16 = 255f;
853						num17 = 192f;
854						num18 = 182f;
855						break;
856					}
857					R = num16 / 255f;
858					G = num17 / 255f;
859					B = num18 / 255f;
860					break;
861				}
862				case 718:
863					if (!Main.dayTime && !WorldGen.SolidTile3(x, y - 1))
864					{
865						R = localRandom.NextFloat() * 0.04f + 0.1f + (float)Main.DiscoR / 800f;
866						G = localRandom.NextFloat() * 0.04f + 0.1f + (float)Main.DiscoG / 800f;
867						B = localRandom.NextFloat() * 0.04f + 0.1f + (float)Main.DiscoB / 800f;
868					}
869					break;
870				case 717:
871				{
872					float num13 = 0.55f;
873					num13 += (float)(270 - Main.mouseTextColor) / 800f;
874					num13 += localRandom.NextFloat() * 0.03f;
875					num13 *= 0.5f;
876					R = num13 * 1.1f;
877					G = num13 * 0.4f;
878					B = num13 * 0.1f;
879					break;
880				}
881				case 429:
882				{
883					int num8 = tile.frameX / 18;
884					bool flag2 = num8 % 2 >= 1;
885					bool flag3 = num8 % 4 >= 2;
886					bool flag4 = num8 % 8 >= 4;
887					bool num9 = num8 % 16 >= 8;
888					if (flag2)
889					{
890						R += 0.5f;
891					}
892					if (flag3)
893					{
894						G += 0.5f;
895					}
896					if (flag4)
897					{
898						B += 0.5f;
899					}
900					if (num9)
901					{
902						R += 0.2f;
903						G += 0.2f;
904					}
905					break;
906				}
907				case 286:
908				case 619:
909					R = 0.1f;
910					G = 0.2f;
911					B = 0.7f;
912					break;
913				case 620:
914				{
915					Color color = new Color(230, 230, 230, 0).MultiplyRGBA(Main.hslToRgb(Main.GlobalTimeWrappedHourly * 0.5f % 1f, 1f, 0.5f));
916					color *= 0.4f;
917					R = (float)(int)color.R / 255f;
918					G = (float)(int)color.G / 255f;
919					B = (float)(int)color.B / 255f;
920					break;
921				}
922				case 582:
923				case 598:
924					R = 0.7f;
925					G = 0.2f;
926					B = 0.1f;
927					break;
928				case 270:
929					R = 0.73f;
930					G = 1f;
931					B = 0.41f;
932					break;
933				case 271:
934					R = 0.45f;
935					G = 0.95f;
936					B = 1f;
937					break;
938				case 581:
939					R = 1f;
940					G = 0.75f;
941					B = 0.5f;
942					break;
943				case 660:
944					TorchID.TorchColor(23, out R, out G, out B);
945					break;
946				case 572:
947					switch (tile.frameY / 36)
948					{
949					case 0:
950						R = 0.9f;
951						G = 0.5f;
952						B = 0.7f;
953						break;
954					case 1:
955						R = 0.7f;
956						G = 0.55f;
957						B = 0.96f;
958						break;
959					case 2:
960						R = 0.45f;
961						G = 0.96f;
962						B = 0.95f;
963						break;
964					case 3:
965						R = 0.5f;
966						G = 0.96f;
967						B = 0.62f;
968						break;
969					case 4:
970						R = 0.47f;
971						G = 0.69f;
972						B = 0.95f;
973						break;
974					case 5:
975						R = 0.92f;
976						G = 0.57f;
977						B = 0.51f;
978						break;
979					}
980					break;
981				case 262:
982					R = 0.75f;
983					B = 0.75f;
984					break;
985				case 263:
986					R = 0.75f;
987					G = 0.75f;
988					break;
989				case 264:
990					B = 0.75f;
991					break;
992				case 265:
993					G = 0.75f;
994					break;
995				case 266:
996					R = 0.75f;
997					break;
998				case 267:
999					R = 0.75f;
1000					G = 0.75f;
1001					B = 0.75f;
1002					break;
1003				case 268:
1004					R = 0.75f;
1005					G = 0.375f;
1006					break;
1007				case 237:
1008					R = 0.1f;
1009					G = 0.1f;
1010					break;
1011				case 238:
1012					if ((double)lightColor.X < 0.5)
1013					{
1014						lightColor.X = 0.5f;
1015					}
1016					if ((double)lightColor.Z < 0.5)
1017					{
1018						lightColor.Z = 0.5f;
1019					}
1020					break;
1021				case 235:
1022					if ((double)lightColor.X < 0.6)
1023					{
1024						lightColor.X = 0.6f;
1025					}
1026					if ((double)lightColor.Y < 0.6)
1027					{
1028						lightColor.Y = 0.6f;
1029					}
1030					break;
1031				case 405:
1032					if (tile.frameX < 54)
1033					{
1034						float num27 = (float)localRandom.Next(28, 42) * 0.005f;
1035						num27 += (float)(270 - Main.mouseTextColor) / 700f;
1036						switch (tile.frameX / 54)
1037						{
1038						case 1:
1039							R = 0.7f;
1040							G = 1f;
1041							B = 0.5f;
1042							break;
1043						case 2:
1044							R = 0.5f * Main.demonTorch + 1f * (1f - Main.demonTorch);
1045							G = 0.3f;
1046							B = 1f * Main.demonTorch + 0.5f * (1f - Main.demonTorch);
1047							break;
1048						case 3:
1049							R = 0.45f;
1050							G = 0.75f;
1051							B = 1f;
1052							break;
1053						case 4:
1054							R = 1.15f;
1055							G = 1.15f;
1056							B = 0.5f;
1057							break;
1058						case 5:
1059							R = (float)Main.DiscoR / 255f;
1060							G = (float)Main.DiscoG / 255f;
1061							B = (float)Main.DiscoB / 255f;
1062							break;
1063						default:
1064							R = 0.9f;
1065							G = 0.3f;
1066							B = 0.1f;
1067							break;
1068						}
1069						R += num27;
1070						G += num27;
1071						B += num27;
1072					}
1073					break;
1074				case 215:
1075					if (tile.frameY < 36)
1076					{
1077						float num26 = (float)localRandom.Next(28, 42) * 0.005f;
1078						num26 += (float)(270 - Main.mouseTextColor) / 700f;
1079						switch (tile.frameX / 54)
1080						{
1081						case 1:
1082							R = 0.7f;
1083							G = 1f;
1084							B = 0.5f;
1085							break;
1086						case 2:
1087							R = 0.5f * Main.demonTorch + 1f * (1f - Main.demonTorch);
1088							G = 0.3f;
1089							B = 1f * Main.demonTorch + 0.5f * (1f - Main.demonTorch);
1090							break;
1091						case 3:
1092							R = 0.45f;
1093							G = 0.75f;
1094							B = 1f;
1095							break;
1096						case 4:
1097							R = 1.15f;
1098							G = 1.15f;
1099							B = 0.5f;
1100							break;
1101						case 5:
1102							R = (float)Main.DiscoR / 255f;
1103							G = (float)Main.DiscoG / 255f;
1104							B = (float)Main.DiscoB / 255f;
1105							break;
1106						case 6:
1107							R = 0.75f;
1108							G = 1.2824999f;
1109							B = 1.2f;
1110							break;
1111						case 7:
1112							R = 0.95f;
1113							G = 0.65f;
1114							B = 1.3f;
1115							break;
1116						case 8:
1117							R = 1.4f;
1118							G = 0.85f;
1119							B = 0.55f;
1120							break;
1121						case 9:
1122							R = 0.25f;
1123							G = 1.3f;
1124							B = 0.8f;
1125							break;
1126						case 10:
1127							R = 0.95f;
1128							G = 0.4f;
1129							B = 1.4f;
1130							break;
1131						case 11:
1132							R = 1.4f;
1133							G = 0.7f;
1134							B = 0.5f;
1135							break;
1136						case 12:
1137							R = 1.25f;
1138							G = 0.6f;
1139							B = 1.2f;
1140							break;
1141						case 13:
1142							R = 0.75f;
1143							G = 1.45f;
1144							B = 0.9f;
1145							break;
1146						case 14:
1147							R = 0.25f;
1148							G = 0.65f;
1149							B = 1f;
1150							break;
1151						case 15:
1152							TorchID.TorchColor(23, out R, out G, out B);
1153							break;
1154						default:
1155							R = 0.9f;
1156							G = 0.3f;
1157							B = 0.1f;
1158							break;
1159						}
1160						R += num26;
1161						G += num26;
1162						B += num26;
1163					}
1164					break;
1165				case 92:
1166					if (tile.frameY <= 18 && tile.frameX == 0)
1167					{
1168						R = 1f;
1169						G = 1f;
1170						B = 1f;
1171					}
1172					break;
1173				case 592:
1174					if (tile.frameY > 0)
1175					{
1176						float num25 = (float)localRandom.Next(28, 42) * 0.005f;
1177						num25 += (float)(270 - Main.mouseTextColor) / 700f;
1178						R = 1.35f;
1179						G = 0.45f;
1180						B = 0.15f;
1181						R += num25;
1182						G += num25;
1183						B += num25;
1184					}
1185					break;
1186				case 593:
1187					if (tile.frameX < 18)
1188					{
1189						R = 0.8f;
1190						G = 0.3f;
1191						B = 0.1f;
1192					}
1193					break;
1194				case 594:
1195					if (tile.frameX < 36)
1196					{
1197						R = 0.8f;
1198						G = 0.3f;
1199						B = 0.1f;
1200					}
1201					break;
1202				case 548:
1203					if (tile.frameX / 54 >= 7)
1204					{
1205						R = 0.7f;
1206						G = 0.3f;
1207						B = 0.2f;
1208					}
1209					break;
1210				case 613:
1211				case 614:
1212					R = 0.7f;
1213					G = 0.3f;
1214					B = 0.2f;
1215					break;
1216				case 93:
1217					if (tile.frameX != 0)
1218					{
1219						break;
1220					}
1221					switch (tile.frameY / 54)
1222					{
1223					case 1:
1224						R = 0.95f;
1225						G = 0.95f;
1226						B = 0.5f;
1227						break;
1228					case 2:
1229						R = 0.85f;
1230						G = 0.6f;
1231						B = 1f;
1232						break;
1233					case 3:
1234						R = 0.75f;
1235						G = 1f;
1236						B = 0.6f;
1237						break;
1238					case 4:
1239					case 5:
1240						R = 0.75f;
1241						G = 0.85f;
1242						B = 1f;
1243						break;
1244					case 6:
1245						R = 1f;
1246						G = 0.95f;
1247						B = 0.65f;
1248						break;
1249					case 7:
1250						R = 1f;
1251						G = 0.97f;
1252						B = 0.85f;
1253						break;
1254					case 9:
1255						R = 1f;
1256						G = 1f;
1257						B = 0.7f;
1258						break;
1259					case 10:
1260						R = 1f;
1261						G = 0.95f;
1262						B = 0.65f;
1263						break;
1264					case 12:
1265						R = 1f;
1266						G = 0.95f;
1267						B = 0.65f;
1268						break;
1269					case 13:
1270						R = 1f;
1271						G = 1f;
1272						B = 0.6f;
1273						break;
1274					case 14:
1275						R = 1f;
1276						G = 0.95f;
1277						B = 0.65f;
1278						break;
1279					case 18:
1280						R = 1f;
1281						G = 0.95f;
1282						B = 0.65f;
1283						break;
1284					case 19:
1285						if (tile.color() == 0)
1286						{
1287							R = 0.37f;
1288							G = 0.8f;
1289							B = 1f;
1290						}
1291						else
1292						{
1293							flag = true;
1294						}
1295						break;
1296					case 20:
1297						R = 0f;
1298						G = 0.9f;
1299						B = 1f;
1300						break;
1301					case 21:
1302						R = 0.25f;
1303						G = 0.7f;
1304						B = 1f;
1305						break;
1306					case 23:
1307						R = 0.5f * Main.demonTorch + 1f * (1f - Main.demonTorch);
1308						G = 0.3f;
1309						B = 1f * Main.demonTorch + 0.5f * (1f - Main.demonTorch);
1310						break;
1311					case 24:
1312						R = 0.35f;
1313						G = 0.5f;
1314						B = 0.3f;
1315						break;
1316					case 25:
1317						R = 0.34f;
1318						G = 0.4f;
1319						B = 0.31f;
1320						break;
1321					case 26:
1322						R = 0.25f;
1323						G = 0.32f;
1324						B = 0.5f;
1325						break;
1326					case 29:
1327						R = 0.9f;
1328						G = 0.75f;
1329						B = 1f;
1330						break;
1331					case 30:
1332						R = 1f;
1333						G = 0.95f;
1334						B = 0.65f;
1335						break;
1336					case 31:
1337					{
1338						Vector3 vector10 = Main.hslToRgb(Main.demonTorch * 0.12f + 0.69f, 1f, 0.75f).ToVector3() * 1.2f;
1339						R = vector10.X;
1340						G = vector10.Y;
1341						B = vector10.Z;
1342						break;
1343					}
1344					case 32:
1345						R = 1f;
1346						G = 0.97f;
1347						B = 0.85f;
1348						break;
1349					case 33:
1350						R = 0.55f;
1351						G = 0.45f;
1352						B = 0.95f;
1353						break;
1354					case 34:
1355						R = 1f;
1356						G = 0.6f;
1357						B = 0.1f;
1358						break;
1359					case 35:
1360						R = 0.3f;
1361						G = 0.75f;
1362						B = 0.55f;
1363						break;
1364					case 36:
1365						R = 0.9f;
1366						G = 0.55f;
1367						B = 0.7f;
1368						break;
1369					case 37:
1370						R = 0.55f;
1371						G = 0.85f;
1372						B = 1f;
1373						break;
1374					case 38:
1375						R = 1f;
1376						G = 0.95f;
1377						B = 0.65f;
1378						break;
1379					case 39:
1380						R = 1f;
1381						G = 0.95f;
1382						B = 0.65f;
1383						break;
1384					case 40:
1385						R = 0.4f;
1386						G = 0.8f;
1387						B = 0.9f;
1388						break;
1389					case 41:
1390						R = 1f;
1391						G = 1f;
1392						B = 1f;
1393						break;
1394					case 42:
1395						R = 0.95f;
1396						G = 0.5f;
1397						B = 0.4f;
1398						break;
1399					case 43:
1400					{
1401						Vector4 vector9 = LiquidRenderer.GetShimmerBaseColor(x, y) * 1.5f;
1402						R = MathHelper.Clamp(vector9.X, 0f, 1f);
1403						G = MathHelper.Clamp(vector9.Y, 0f, 1f);
1404						B = MathHelper.Clamp(vector9.Z, 0f, 1f);
1405						break;
1406					}
1407					case 44:
1408						R = 1f;
1409						G = 0.95f;
1410						B = 0.65f;
1411						break;
1412					case 45:
1413						R = 1f;
1414						G = 2f / 3f;
1415						B = 66f / 85f;
1416						break;
1417					case 46:
1418						R = 1f;
1419						G = 0.95f;
1420						B = 0.65f;
1421						break;
1422					case 47:
1423						R = 81f / 85f;
1424						G = 77f / 85f;
1425						B = 0.36078432f;
1426						break;
1427					case 48:
1428						R = 54f / 85f;
1429						G = 0.5019608f;
1430						B = 1f;
1431						break;
1432					case 49:
1433						R = 1f;
1434						G = 20f / 51f;
1435						B = 20f / 51f;
1436						break;
1437					case 50:
1438						R = 38f / 51f;
1439						G = 38f / 51f;
1440						B = 1f;
1441						break;
1442					case 51:
1443						R = 2f / 3f;
1444						G = 0.7058824f;
1445						B = 1f;
1446						break;
1447					case 52:
1448						R = 1f;
1449						G = 0.95f;
1450						B = 0.65f;
1451						break;
1452					case 53:
1453						R = 1f;
1454						G = 0.95f;
1455						B = 0.75f;
1456						break;
1457					case 54:
1458						R = 1f;
1459						G = 0.85499996f;
1460						B = 0.585f;
1461						break;
1462					case 55:
1463						R = 0.5f;
1464						G = 0.9f;
1465						B = 1f;
1466						flag = true;
1467						break;
1468					case 56:
1469						R = 1f;
1470						G = 0.9f;
1471						B = 0.9f;
1472						break;
1473					case 57:
1474						R = 0.7058824f;
1475						G = 46f / 51f;
1476						B = 1f;
1477						break;
1478					case 58:
1479						R = 0.5882353f;
1480						G = 47f / 51f;
1481						B = 49f / 51f;
1482						break;
1483					case 59:
1484						R = 2f / 3f;
1485						G = 49f / 51f;
1486						B = 1f;
1487						break;
1488					case 60:
1489						R = 1f;
1490						G = 0.95f;
1491						B = 0.65f;
1492						break;
1493					case 61:
1494						R = 1f;
1495						G = 0.95f;
1496						B = 0.65f;
1497						break;
1498					case 62:
1499						R = 47f / 51f;
1500						G = 0.4117647f;
1501						B = 1f;
1502						break;
1503					case 63:
1504						R = 38f / 51f;
1505						G = 38f / 51f;
1506						B = 1f;
1507						break;
1508					case 64:
1509						R = 43f / 51f;
1510						G = 35f / 51f;
1511						B = 49f / 51f;
1512						break;
1513					default:
1514						R = 1f;
1515						G = 0.97f;
1516						B = 0.85f;
1517						break;
1518					}
1519					break;
1520				case 96:
1521					if (tile.frameX >= 36)
1522					{
1523						R = 0.5f;
1524						G = 0.35f;
1525						B = 0.1f;
1526					}
1527					break;
1528				case 98:
1529					if (tile.frameY == 0)
1530					{
1531						R = 1f;
1532						G = 0.97f;
1533						B = 0.85f;
1534					}
1535					break;
1536				case 4:
1537					if (tile.frameX < 66)
1538					{
1539						TorchID.TorchColor(tile.frameY / 22, out R, out G, out B);
1540					}
1541					break;
1542				case 372:
1543					if (tile.frameX == 0)
1544					{
1545						R = 0.9f;
1546						G = 0.1f;
1547						B = 0.75f;
1548					}
1549					break;
1550				case 646:
1551					if (tile.frameX == 0)
1552					{
1553						R = 0.2f;
1554						G = 0.3f;
1555						B = 0.32f;
1556					}
1557					break;
1558				case 33:
1559					if (tile.frameX != 0)
1560					{
1561						break;
1562					}
1563					switch (tile.frameY / 22)
1564					{
1565					case 0:
1566						R = 1f;
1567						G = 0.95f;
1568						B = 0.65f;
1569						break;
1570					case 1:
1571						R = 0.55f;
1572						G = 0.85f;
1573						B = 0.35f;
1574						break;
1575					case 2:
1576						R = 0.65f;
1577						G = 0.95f;
1578						B = 0.5f;
1579						break;
1580					case 3:
1581						R = 0.2f;
1582						G = 0.75f;
1583						B = 1f;
1584						break;
1585					case 5:
1586						R = 0.85f;
1587						G = 0.6f;
1588						B = 1f;
1589						break;
1590					case 7:
1591					case 8:
1592						R = 0.75f;
1593						G = 0.85f;
1594						B = 1f;
1595						break;
1596					case 9:
1597						R = 1f;
1598						G = 0.95f;
1599						B = 0.65f;
1600						break;
1601					case 10:
1602						R = 1f;
1603						G = 0.97f;
1604						B = 0.85f;
1605						break;
1606					case 14:
1607						R = 1f;
1608						G = 1f;
1609						B = 0.6f;
1610						break;
1611					case 15:
1612						R = 1f;
1613						G = 0.95f;
1614						B = 0.65f;
1615						break;
1616					case 18:
1617						R = 1f;
1618						G = 0.95f;
1619						B = 0.65f;
1620						break;
1621					case 19:
1622						if (tile.color() == 0)
1623						{
1624							R = 0.37f;
1625							G = 0.8f;
1626							B = 1f;
1627						}
1628						else
1629						{
1630							flag = true;
1631						}
1632						break;
1633					case 20:
1634						R = 0f;
1635						G = 0.9f;
1636						B = 1f;
1637						break;
1638					case 21:
1639						R = 0.25f;
1640						G = 0.7f;
1641						B = 1f;
1642						break;
1643					case 23:
1644						R = 1f;
1645						G = 0.95f;
1646						B = 0.65f;
1647						break;
1648					case 24:
1649						R = 1f;
1650						G = 0.95f;
1651						B = 0.65f;
1652						break;
1653					case 25:
1654						R = 0.5f * Main.demonTorch + 1f * (1f - Main.demonTorch);
1655						G = 0.3f;
1656						B = 1f * Main.demonTorch + 0.5f * (1f - Main.demonTorch);
1657						break;
1658					case 28:
1659						R = 0.9f;
1660						G = 0.75f;
1661						B = 1f;
1662						break;
1663					case 29:
1664						R = 1f;
1665						G = 0.95f;
1666						B = 0.65f;
1667						break;
1668					case 30:
1669					{
1670						Vector3 vector8 = Main.hslToRgb(Main.demonTorch * 0.12f + 0.69f, 1f, 0.75f).ToVector3() * 1.2f;
1671						R = vector8.X;
1672						G = vector8.Y;
1673						B = vector8.Z;
1674						break;
1675					}
1676					case 31:
1677						R = 1f;
1678						G = 0.97f;
1679						B = 0.85f;
1680						break;
1681					case 32:
1682						R = 0.55f;
1683						G = 0.45f;
1684						B = 0.95f;
1685						break;
1686					case 33:
1687						R = 1f;
1688						G = 0.6f;
1689						B = 0.1f;
1690						break;
1691					case 34:
1692						R = 0.3f;
1693						G = 0.75f;
1694						B = 0.55f;
1695						break;
1696					case 35:
1697						R = 0.9f;
1698						G = 0.55f;
1699						B = 0.7f;
1700						break;
1701					case 36:
1702						R = 0.55f;
1703						G = 0.85f;
1704						B = 1f;
1705						break;
1706					case 37:
1707						R = 1f;
1708						G = 0.95f;
1709						B = 0.65f;
1710						break;
1711					case 38:
1712						R = 1f;
1713						G = 0.95f;
1714						B = 0.65f;
1715						break;
1716					case 39:
1717						R = 0.4f;
1718						G = 0.8f;
1719						B = 0.9f;
1720						break;
1721					case 40:
1722						R = 1f;
1723						G = 1f;
1724						B = 1f;
1725						break;
1726					case 41:
1727						R = 0.95f;
1728						G = 0.5f;
1729						B = 0.4f;
1730						break;
1731					case 42:
1732					{
1733						Vector4 vector7 = LiquidRenderer.GetShimmerBaseColor(x, y) * 1.5f;
1734						R = MathHelper.Clamp(vector7.X, 0f, 1f);
1735						G = MathHelper.Clamp(vector7.Y, 0f, 1f);
1736						B = MathHelper.Clamp(vector7.Z, 0f, 1f);
1737						break;
1738					}
1739					case 43:
1740						R = 1f;
1741						G = 0.95f;
1742						B = 0.65f;
1743						break;
1744					case 44:
1745						R = 1f;
1746						G = 2f / 3f;
1747						B = 66f / 85f;
1748						break;
1749					case 45:
1750						R = 1f;
1751						G = 0.95f;
1752						B = 0.65f;
1753						break;
1754					case 46:
1755						R = 81f / 85f;
1756						G = 77f / 85f;
1757						B = 0.36078432f;
1758						break;
1759					case 47:
1760						R = 54f / 85f;
1761						G = 0.5019608f;
1762						B = 1f;
1763						break;
1764					case 48:
1765						R = 1f;
1766						G = 20f / 51f;
1767						B = 20f / 51f;
1768						break;
1769					case 49:
1770						R = 38f / 51f;
1771						G = 38f / 51f;
1772						B = 1f;
1773						break;
1774					case 50:
1775						R = 2f / 3f;
1776						G = 0.7058824f;
1777						B = 1f;
1778						break;
1779					case 51:
1780						R = 1f;
1781						G = 0.95f;
1782						B = 0.65f;
1783						break;
1784					case 52:
1785						R = 1f;
1786						G = 0.95f;
1787						B = 0.75f;
1788						break;
1789					case 53:
1790						R = 1f;
1791						G = 0.85499996f;
1792						B = 0.585f;
1793						break;
1794					case 54:
1795						R = 0.5f;
1796						G = 0.9f;
1797						B = 1f;
1798						flag = true;
1799						break;
1800					case 55:
1801						R = 1f;
1802						G = 0.9f;
1803						B = 0.9f;
1804						break;
1805					case 56:
1806						R = 0.7058824f;
1807						G = 46f / 51f;
1808						B = 1f;
1809						break;
1810					case 57:
1811						R = 0.5882353f;
1812						G = 47f / 51f;
1813						B = 49f / 51f;
1814						break;
1815					case 58:
1816						R = 2f / 3f;
1817						G = 49f / 51f;
1818						B = 1f;
1819						break;
1820					case 59:
1821						R = 1f;
1822						G = 0.95f;
1823						B = 0.65f;
1824						break;
1825					case 60:
1826						R = 1f;
1827						G = 0.95f;
1828						B = 0.65f;
1829						break;
1830					case 61:
1831						R = 47f / 51f;
1832						G = 0.4117647f;
1833						B = 1f;
1834						break;
1835					case 62:
1836						R = 38f / 51f;
1837						G = 38f / 51f;
1838						B = 1f;
1839						break;
1840					case 63:
1841						R = 43f / 51f;
1842						G = 35f / 51f;
1843						B = 49f / 51f;
1844						break;
1845					default:
1846						R = 1f;
1847						G = 0.95f;
1848						B = 0.65f;
1849						break;
1850					}
1851					break;
1852				case 174:
1853					if (tile.frameX == 0)
1854					{
1855						R = 1f;
1856						G = 0.95f;
1857						B = 0.65f;
1858					}
1859					break;
1860				case 100:
1861				case 173:
1862					if (tile.frameX >= 36)
1863					{
1864						break;
1865					}
1866					switch (tile.frameY / 36)
1867					{
1868					case 1:
1869						R = 0.95f;
1870						G = 0.95f;
1871						B = 0.5f;
1872						break;
1873					case 2:
1874						R = 0.85f;
1875						G = 0.6f;
1876						B = 1f;
1877						break;
1878					case 3:
1879						R = 1f;
1880						G = 0.6f;
1881						B = 0.6f;
1882						break;
1883					case 5:
1884						R = 1f;
1885						G = 0.95f;
1886						B = 0.65f;
1887						break;
1888					case 6:
1889					case 7:
1890						R = 1f;
1891						G = 0.95f;
1892						B = 0.65f;
1893						break;
1894					case 8:
1895						R = 1f;
1896						G = 0.97f;
1897						B = 0.85f;
1898						break;
1899					case 9:
1900						R = 0.75f;
1901						G = 0.85f;
1902						B = 1f;
1903						break;
1904					case 11:
1905						R = 1f;
1906						G = 1f;
1907						B = 0.7f;
1908						break;
1909					case 12:
1910						R = 1f;
1911						G = 0.95f;
1912						B = 0.65f;
1913						break;
1914					case 13:
1915						R = 1f;
1916						G = 1f;
1917						B = 0.6f;
1918						break;
1919					case 14:
1920						R = 1f;
1921						G = 0.95f;
1922						B = 0.65f;
1923						break;
1924					case 18:
1925						R = 1f;
1926						G = 0.95f;
1927						B = 0.65f;
1928						break;
1929					case 19:
1930						if (tile.color() == 0)
1931						{
1932							R = 0.37f;
1933							G = 0.8f;
1934							B = 1f;
1935						}
1936						else
1937						{
1938							flag = true;
1939						}
1940						break;
1941					case 20:
1942						R = 0f;
1943						G = 0.9f;
1944						B = 1f;
1945						break;
1946					case 21:
1947						R = 0.25f;
1948						G = 0.7f;
1949						B = 1f;
1950						break;
1951					case 25:
1952						R = 0.5f * Main.demonTorch + 1f * (1f - Main.demonTorch);
1953						G = 0.3f;
1954						B = 1f * Main.demonTorch + 0.5f * (1f - Main.demonTorch);
1955						break;
1956					case 22:
1957						R = 0.35f;
1958						G = 0.5f;
1959						B = 0.3f;
1960						break;
1961					case 23:
1962						R = 0.34f;
1963						G = 0.4f;
1964						B = 0.31f;
1965						break;
1966					case 24:
1967						R = 0.25f;
1968						G = 0.32f;
1969						B = 0.5f;
1970						break;
1971					case 29:
1972						R = 0.9f;
1973						G = 0.75f;
1974						B = 1f;
1975						break;
1976					case 30:
1977						R = 1f;
1978						G = 0.95f;
1979						B = 0.65f;
1980						break;
1981					case 31:
1982					{
1983						Vector3 vector6 = Main.hslToRgb(Main.demonTorch * 0.12f + 0.69f, 1f, 0.75f).ToVector3() * 1.2f;
1984						R = vector6.X;
1985						G = vector6.Y;
1986						B = vector6.Z;
1987						break;
1988					}
1989					case 32:
1990						R = 1f;
1991						G = 0.97f;
1992						B = 0.85f;
1993						break;
1994					case 33:
1995						R = 0.55f;
1996						G = 0.45f;
1997						B = 0.95f;
1998						break;
1999					case 34:
2000						R = 1f;
2001						G = 0.6f;
2002						B = 0.1f;
2003						break;
2004					case 35:
2005						R = 0.3f;
2006						G = 0.75f;
2007						B = 0.55f;
2008						break;
2009					case 36:
2010						R = 0.9f;
2011						G = 0.55f;
2012						B = 0.7f;
2013						break;
2014					case 37:
2015						R = 0.55f;
2016						G = 0.85f;
2017						B = 1f;
2018						break;
2019					case 38:
2020						R = 1f;
2021						G = 0.95f;
2022						B = 0.65f;
2023						break;
2024					case 39:
2025						R = 1f;
2026						G = 0.95f;
2027						B = 0.65f;
2028						break;
2029					case 40:
2030						R = 0.4f;
2031						G = 0.8f;
2032						B = 0.9f;
2033						break;
2034					case 41:
2035						R = 1f;
2036						G = 1f;
2037						B = 1f;
2038						break;
2039					case 42:
2040						R = 0.95f;
2041						G = 0.5f;
2042						B = 0.4f;
2043						break;
2044					case 43:
2045					{
2046						Vector4 vector5 = LiquidRenderer.GetShimmerBaseColor(x, y) * 1.5f;
2047						R = MathHelper.Clamp(vector5.X, 0f, 1f);
2048						G = MathHelper.Clamp(vector5.Y, 0f, 1f);
2049						B = MathHelper.Clamp(vector5.Z, 0f, 1f);
2050						break;
2051					}
2052					case 44:
2053						R = 1f;
2054						G = 0.95f;
2055						B = 0.65f;
2056						break;
2057					case 45:
2058						R = 1f;
2059						G = 2f / 3f;
2060						B = 66f / 85f;
2061						break;
2062					case 46:
2063						R = 1f;
2064						G = 0.95f;
2065						B = 0.65f;
2066						break;
2067					case 47:
2068						R = 81f / 85f;
2069						G = 77f / 85f;
2070						B = 0.36078432f;
2071						break;
2072					case 48:
2073						R = 54f / 85f;
2074						G = 0.5019608f;
2075						B = 1f;
2076						break;
2077					case 49:
2078						R = 1f;
2079						G = 20f / 51f;
2080						B = 20f / 51f;
2081						break;
2082					case 50:
2083						R = 38f / 51f;
2084						G = 38f / 51f;
2085						B = 1f;
2086						break;
2087					case 51:
2088						R = 2f / 3f;
2089						G = 0.7058824f;
2090						B = 1f;
2091						break;
2092					case 52:
2093						R = 1f;
2094						G = 0.95f;
2095						B = 0.65f;
2096						break;
2097					case 53:
2098						R = 1f;
2099						G = 0.95f;
2100						B = 0.75f;
2101						break;
2102					case 54:
2103						R = 1f;
2104						G = 0.85499996f;
2105						B = 0.585f;
2106						break;
2107					case 55:
2108						R = 0.5f;
2109						G = 0.9f;
2110						B = 1f;
2111						flag = true;
2112						break;
2113					case 56:
2114						R = 1f;
2115						G = 0.9f;
2116						B = 0.9f;
2117						break;
2118					case 57:
2119						R = 0.7058824f;
2120						G = 46f / 51f;
2121						B = 1f;
2122						break;
2123					case 58:
2124						R = 0.5882353f;
2125						G = 47f / 51f;
2126						B = 49f / 51f;
2127						break;
2128					case 59:
2129						R = 2f / 3f;
2130						G = 49f / 51f;
2131						B = 1f;
2132						break;
2133					case 60:
2134						R = 1f;
2135						G = 0.95f;
2136						B = 0.65f;
2137						break;
2138					case 61:
2139						R = 1f;
2140						G = 0.95f;
2141						B = 0.65f;
2142						break;
2143					case 62:
2144						R = 47f / 51f;
2145						G = 0.4117647f;
2146						B = 1f;
2147						break;
2148					case 63:
2149						R = 38f / 51f;
2150						G = 38f / 51f;
2151						B = 1f;
2152						break;
2153					case 64:
2154						R = 43f / 51f;
2155						G = 35f / 51f;
2156						B = 49f / 51f;
2157						break;
2158					default:
2159						R = 1f;
2160						G = 0.95f;
2161						B = 0.65f;
2162						break;
2163					}
2164					break;
2165				case 34:
2166				{
2167					if (tile.frameX % 108 >= 54)
2168					{
2169						break;
2170					}
2171					int num24 = tile.frameY / 54;
2172					switch (num24 + 37 * (tile.frameX / 108))
2173					{
2174					case 7:
2175						R = 0.95f;
2176						G = 0.95f;
2177						B = 0.5f;
2178						break;
2179					case 8:
2180						R = 0.85f;
2181						G = 0.6f;
2182						B = 1f;
2183						break;
2184					case 9:
2185						R = 1f;
2186						G = 0.6f;
2187						B = 0.6f;
2188						break;
2189					case 12:
2190						R = 1f;
2191						G = 0.95f;
2192						B = 0.65f;
2193						break;
2194					case 13:
2195						R = 1f;
2196						G = 0.97f;
2197						B = 0.85f;
2198						break;
2199					case 11:
2200					case 17:
2201						R = 0.75f;
2202						G = 0.85f;
2203						B = 1f;
2204						break;
2205					case 15:
2206						R = 1f;
2207						G = 1f;
2208						B = 0.7f;
2209						break;
2210					case 16:
2211						R = 1f;
2212						G = 0.95f;
2213						B = 0.65f;
2214						break;
2215					case 18:
2216						R = 1f;
2217						G = 1f;
2218						B = 0.6f;
2219						break;
2220					case 19:
2221						R = 1f;
2222						G = 0.95f;
2223						B = 0.65f;
2224						break;
2225					case 23:
2226						R = 1f;
2227						G = 0.95f;
2228						B = 0.65f;
2229						break;
2230					case 24:
2231						if (tile.color() == 0)
2232						{
2233							R = 0.37f;
2234							G = 0.8f;
2235							B = 1f;
2236						}
2237						else
2238						{
2239							flag = true;
2240						}
2241						break;
2242					case 25:
2243						R = 0f;
2244						G = 0.9f;
2245						B = 1f;
2246						break;
2247					case 26:
2248						R = 0.25f;
2249						G = 0.7f;
2250						B = 1f;
2251						break;
2252					case 27:
2253						R = 0.55f;
2254						G = 0.85f;
2255						B = 0.35f;
2256						break;
2257					case 28:
2258						R = 0.65f;
2259						G = 0.95f;
2260						B = 0.5f;
2261						break;
2262					case 29:
2263						R = 0.2f;
2264						G = 0.75f;
2265						B = 1f;
2266						break;
2267					case 30:
2268						R = 1f;
2269						G = 0.95f;
2270						B = 0.65f;
2271						break;
2272					case 32:
2273						R = 0.5f * Main.demonTorch + 1f * (1f - Main.demonTorch);
2274						G = 0.3f;
2275						B = 1f * Main.demonTorch + 0.5f * (1f - Main.demonTorch);
2276						break;
2277					case 35:
2278						R = 0.9f;
2279						G = 0.75f;
2280						B = 1f;
2281						break;
2282					case 36:
2283						R = 1f;
2284						G = 0.95f;
2285						B = 0.65f;
2286						break;
2287					case 37:
2288					{
2289						Vector3 vector4 = Main.hslToRgb(Main.demonTorch * 0.12f + 0.69f, 1f, 0.75f).ToVector3() * 1.2f;
2290						R = vector4.X;
2291						G = vector4.Y;
2292						B = vector4.Z;
2293						break;
2294					}
2295					case 38:
2296						R = 1f;
2297						G = 0.97f;
2298						B = 0.85f;
2299						break;
2300					case 39:
2301						R = 0.55f;
2302						G = 0.45f;
2303						B = 0.95f;
2304						break;
2305					case 40:
2306						R = 1f;
2307						G = 0.6f;
2308						B = 0.1f;
2309						break;
2310					case 41:
2311						R = 0.3f;
2312						G = 0.75f;
2313						B = 0.55f;
2314						break;
2315					case 42:
2316						R = 0.9f;
2317						G = 0.55f;
2318						B = 0.7f;
2319						break;
2320					case 43:
2321						R = 0.55f;
2322						G = 0.85f;
2323						B = 1f;
2324						break;
2325					case 44:
2326						R = 1f;
2327						G = 0.95f;
2328						B = 0.65f;
2329						break;
2330					case 45:
2331						R = 1f;
2332						G = 0.95f;
2333						B = 0.65f;
2334						break;
2335					case 46:
2336						R = 0.4f;
2337						G = 0.8f;
2338						B = 0.9f;
2339						break;
2340					case 47:
2341						R = 1f;
2342						G = 1f;
2343						B = 1f;
2344						break;
2345					case 48:
2346						R = 0.95f;
2347						G = 0.5f;
2348						B = 0.4f;
2349						break;
2350					case 49:
2351					{
2352						Vector4 vector3 = LiquidRenderer.GetShimmerBaseColor(x, y) * 1.5f;
2353						R = MathHelper.Clamp(vector3.X, 0f, 1f);
2354						G = MathHelper.Clamp(vector3.Y, 0f, 1f);
2355						B = MathHelper.Clamp(vector3.Z, 0f, 1f);
2356						break;
2357					}
2358					case 50:
2359						R = 1f;
2360						G = 0.95f;
2361						B = 0.65f;
2362						break;
2363					case 51:
2364						R = 1f;
2365						G = 2f / 3f;
2366						B = 66f / 85f;
2367						break;
2368					case 52:
2369						R = 1f;
2370						G = 0.95f;
2371						B = 0.65f;
2372						break;
2373					case 53:
2374						R = 81f / 85f;
2375						G = 77f / 85f;
2376						B = 0.36078432f;
2377						break;
2378					case 54:
2379						R = 54f / 85f;
2380						G = 0.5019608f;
2381						B = 1f;
2382						break;
2383					case 55:
2384						R = 1f;
2385						G = 20f / 51f;
2386						B = 20f / 51f;
2387						break;
2388					case 56:
2389						R = 38f / 51f;
2390						G = 38f / 51f;
2391						B = 1f;
2392						break;
2393					case 57:
2394						R = 2f / 3f;
2395						G = 0.7058824f;
2396						B = 1f;
2397						break;
2398					case 58:
2399						R = 1f;
2400						G = 0.95f;
2401						B = 0.65f;
2402						break;
2403					case 59:
2404						R = 1f;
2405						G = 0.95f;
2406						B = 0.75f;
2407						break;
2408					case 60:
2409						R = 1f;
2410						G = 0.85499996f;
2411						B = 0.585f;
2412						break;
2413					case 61:
2414						R = 0.5f;
2415						G = 0.9f;
2416						B = 1f;
2417						flag = true;
2418						break;
2419					case 62:
2420						R = 1f;
2421						G = 0.9f;
2422						B = 0.9f;
2423						break;
2424					case 63:
2425						R = 0.7058824f;
2426						G = 46f / 51f;
2427						B = 1f;
2428						break;
2429					case 64:
2430						R = 0.5882353f;
2431						G = 47f / 51f;
2432						B = 49f / 51f;
2433						break;
2434					case 65:
2435						R = 2f / 3f;
2436						G = 49f / 51f;
2437						B = 1f;
2438						break;
2439					case 66:
2440						R = 1f;
2441						G = 0.95f;
2442						B = 0.65f;
2443						break;
2444					case 67:
2445						R = 1f;
2446						G = 0.95f;
2447						B = 0.65f;
2448						break;
2449					case 68:
2450						R = 47f / 51f;
2451						G = 0.4117647f;
2452						B = 1f;
2453						break;
2454					case 69:
2455						R = 38f / 51f;
2456						G = 38f / 51f;
2457						B = 1f;
2458						break;
2459					case 70:
2460						R = 43f / 51f;
2461						G = 35f / 51f;
2462						B = 49f / 51f;
2463						break;
2464					default:
2465						R = 1f;
2466						G = 0.95f;
2467						B = 0.8f;
2468						break;
2469					}
2470					break;
2471				}
2472				case 35:
2473					if (tile.frameX < 36)
2474					{
2475						R = 0.75f;
2476						G = 0.6f;
2477						B = 0.3f;
2478					}
2479					break;
2480				case 95:
2481					if (tile.frameX < 36)
2482					{
2483						R = 1f;
2484						G = 0.95f;
2485						B = 0.8f;
2486					}
2487					break;
2488				case 17:
2489				case 133:
2490				case 302:
2491					R = 0.83f;
2492					G = 0.6f;
2493					B = 0.5f;
2494					break;
2495				case 77:
2496					R = 0.75f;
2497					G = 0.45f;
2498					B = 0.25f;
2499					break;
2500				case 37:
2501				{
2502					float num23 = (float)localRandom.Next(95, 106) * 0.01f;
2503					R = 0.56f * num23;
2504					G = 0.43f * num23;
2505					B = 0.15f * num23;
2506					break;
2507				}
2508				case 22:
2509				case 140:
2510					if (tile.color() != 27 && tile.color() != 26)
2511					{
2512						R = 0.12f;
2513					}
2514					G = 0.07f;
2515					B = 0.32f;
2516					break;
2517				case 171:
2518					if (tile.frameX < 10)
2519					{
2520						x -= tile.frameX;
2521						y -= tile.frameY;
2522					}
2523					switch ((Main.tile[x, y].frameY & 0x3C00) >> 10)
2524					{
2525					case 1:
2526						R = 0.1f;
2527						G = 0.1f;
2528						B = 0.1f;
2529						break;
2530					case 2:
2531						R = 0.2f;
2532						break;
2533					case 3:
2534						G = 0.2f;
2535						break;
2536					case 4:
2537						B = 0.2f;
2538						break;
2539					case 5:
2540						R = 0.125f;
2541						G = 0.125f;
2542						break;
2543					case 6:
2544						R = 0.2f;
2545						G = 0.1f;
2546						break;
2547					case 7:
2548						R = 0.125f;
2549						G = 0.125f;
2550						break;
2551					case 8:
2552						R = 0.08f;
2553						G = 0.175f;
2554						break;
2555					case 9:
2556						G = 0.125f;
2557						B = 0.125f;
2558						break;
2559					case 10:
2560						R = 0.125f;
2561						B = 0.125f;
2562						break;
2563					case 11:
2564						R = 0.1f;
2565						G = 0.1f;
2566						B = 0.2f;
2567						break;
2568					default:
2569						R = (G = (B = 0f));
2570						break;
2571					}
2572					R *= 0.5f;
2573					G *= 0.5f;
2574					B *= 0.5f;
2575					break;
2576				case 204:
2577				case 347:
2578					if (tile.color() != 27 && tile.color() != 26)
2579					{
2580						R = 0.35f;
2581					}
2582					break;
2583				case 42:
2584					if (tile.frameX != 0)
2585					{
2586						break;
2587					}
2588					switch (tile.frameY / 36)
2589					{
2590					case 0:
2591						R = 0.7f;
2592						G = 0.65f;
2593						B = 0.55f;
2594						break;
2595					case 1:
2596						R = 0.9f;
2597						G = 0.75f;
2598						B = 0.6f;
2599						break;
2600					case 2:
2601						R = 0.8f;
2602						G = 0.6f;
2603						B = 0.6f;
2604						break;
2605					case 3:
2606						R = 0.65f;
2607						G = 0.5f;
2608						B = 0.2f;
2609						break;
2610					case 4:
2611						R = 0.5f;
2612						G = 0.7f;
2613						B = 0.4f;
2614						break;
2615					case 5:
2616						R = 0.9f;
2617						G = 0.4f;
2618						B = 0.2f;
2619						break;
2620					case 6:
2621						R = 0.7f;
2622						G = 0.75f;
2623						B = 0.3f;
2624						break;
2625					case 7:
2626					{
2627						float num14 = Main.demonTorch * 0.2f;
2628						R = 0.9f - num14;
2629						G = 0.9f - num14;
2630						B = 0.7f + num14;
2631						break;
2632					}
2633					case 8:
2634						R = 0.75f;
2635						G = 0.6f;
2636						B = 0.3f;
2637						break;
2638					case 9:
2639						R = 1f;
2640						G = 0.3f;
2641						B = 0.5f;
2642						B += Main.demonTorch * 0.2f;
2643						R -= Main.demonTorch * 0.1f;
2644						G -= Main.demonTorch * 0.2f;
2645						break;
2646					case 11:
2647						R = 0.85f;
2648						G = 0.6f;
2649						B = 1f;
2650						break;
2651					case 14:
2652						R = 1f;
2653						G = 0.95f;
2654						B = 0.65f;
2655						break;
2656					case 15:
2657					case 16:
2658						R = 1f;
2659						G = 0.95f;
2660						B = 0.65f;
2661						break;
2662					case 17:
2663						R = 1f;
2664						G = 0.97f;
2665						B = 0.85f;
2666						break;
2667					case 18:
2668						R = 0.75f;
2669						G = 0.85f;
2670						B = 1f;
2671						break;
2672					case 21:
2673						R = 1f;
2674						G = 0.95f;
2675						B = 0.65f;
2676						break;
2677					case 22:
2678						R = 1f;
2679						G = 1f;
2680						B = 0.6f;
2681						break;
2682					case 23:
2683						R = 1f;
2684						G = 0.95f;
2685						B = 0.65f;
2686						break;
2687					case 27:
2688						R = 1f;
2689						G = 0.95f;
2690						B = 0.65f;
2691						break;
2692					case 28:
2693						if (tile.color() == 0)
2694						{
2695							R = 0.37f;
2696							G = 0.8f;
2697							B = 1f;
2698						}
2699						else
2700						{
2701							flag = true;
2702						}
2703						break;
2704					case 29:
2705						R = 0f;
2706						G = 0.9f;
2707						B = 1f;
2708						break;
2709					case 30:
2710						R = 0.25f;
2711						G = 0.7f;
2712						B = 1f;
2713						break;
2714					case 32:
2715						R = 0.5f * Main.demonTorch + 1f * (1f - Main.demonTorch);
2716						G = 0.3f;
2717						B = 1f * Main.demonTorch + 0.5f * (1f - Main.demonTorch);
2718						break;
2719					case 35:
2720						R = 0.7f;
2721						G = 0.6f;
2722						B = 0.9f;
2723						break;
2724					case 36:
2725						R = 1f;
2726						G = 0.95f;
2727						B = 0.65f;
2728						break;
2729					case 37:
2730					{
2731						Vector3 vector2 = Main.hslToRgb(Main.demonTorch * 0.12f + 0.69f, 1f, 0.75f).ToVector3() * 1.2f;
2732						R = vector2.X;
2733						G = vector2.Y;
2734						B = vector2.Z;
2735						break;
2736					}
2737					case 38:
2738						R = 1f;
2739						G = 0.97f;
2740						B = 0.85f;
2741						break;
2742					case 39:
2743						R = 0.55f;
2744						G = 0.45f;
2745						B = 0.95f;
2746						break;
2747					case 40:
2748						R = 1f;
2749						G = 0.6f;
2750						B = 0.1f;
2751						break;
2752					case 41:
2753						R = 0.3f;
2754						G = 0.75f;
2755						B = 0.55f;
2756						break;
2757					case 42:
2758						R = 0.9f;
2759						G = 0.55f;
2760						B = 0.7f;
2761						break;
2762					case 43:
2763						R = 0.55f;
2764						G = 0.85f;
2765						B = 1f;
2766						break;
2767					case 44:
2768						R = 1f;
2769						G = 0.95f;
2770						B = 0.65f;
2771						break;
2772					case 45:
2773						R = 1f;
2774						G = 0.95f;
2775						B = 0.65f;
2776						break;
2777					case 46:
2778						R = 0.4f;
2779						G = 0.8f;
2780						B = 0.9f;
2781						break;
2782					case 47:
2783						R = 1f;
2784						G = 1f;
2785						B = 1f;
2786						break;
2787					case 48:
2788						R = 0.95f;
2789						G = 0.5f;
2790						B = 0.4f;
2791						break;
2792					case 49:
2793					{
2794						Vector4 vector = LiquidRenderer.GetShimmerBaseColor(x, y) * 1.5f;
2795						R = MathHelper.Clamp(vector.X, 0f, 1f);
2796						G = MathHelper.Clamp(vector.Y, 0f, 1f);
2797						B = MathHelper.Clamp(vector.Z, 0f, 1f);
2798						break;
2799					}
2800					case 50:
2801						R = 1f;
2802						G = 0.95f;
2803						B = 0.65f;
2804						break;
2805					case 51:
2806						R = 1f;
2807						G = 2f / 3f;
2808						B = 66f / 85f;
2809						break;
2810					case 52:
2811						R = 1f;
2812						G = 0.95f;
2813						B = 0.65f;
2814						break;
2815					case 53:
2816						R = 81f / 85f;
2817						G = 77f / 85f;
2818						B = 0.36078432f;
2819						break;
2820					case 54:
2821						R = 54f / 85f;
2822						G = 0.5019608f;
2823						B = 1f;
2824						break;
2825					case 55:
2826						R = 1f;
2827						G = 20f / 51f;
2828						B = 20f / 51f;
2829						break;
2830					case 56:
2831						R = 38f / 51f;
2832						G = 38f / 51f;
2833						B = 1f;
2834						break;
2835					case 57:
2836						R = 2f / 3f;
2837						G = 0.7058824f;
2838						B = 1f;
2839						break;
2840					case 58:
2841						R = 1f;
2842						G = 0.95f;
2843						B = 0.65f;
2844						break;
2845					case 59:
2846						R = 1f;
2847						G = 0.95f;
2848						B = 0.75f;
2849						break;
2850					case 60:
2851						R = 1f;
2852						G = 0.85499996f;
2853						B = 0.585f;
2854						break;
2855					case 61:
2856						R = 0.5f;
2857						G = 0.9f;
2858						B = 1f;
2859						flag = true;
2860						break;
2861					case 62:
2862						R = 1f;
2863						G = 0.9f;
2864						B = 0.9f;
2865						break;
2866					case 63:
2867						R = 0.7058824f;
2868						G = 46f / 51f;
2869						B = 1f;
2870						break;
2871					case 64:
2872						R = 0.5882353f;
2873						G = 47f / 51f;
2874						B = 49f / 51f;
2875						break;
2876					case 65:
2877						R = 2f / 3f;
2878						G = 49f / 51f;
2879						B = 1f;
2880						break;
2881					case 66:
2882						R = 1f;
2883						G = 0.95f;
2884						B = 0.65f;
2885						break;
2886					case 67:
2887						R = 1f;
2888						G = 0.95f;
2889						B = 0.65f;
2890						break;
2891					case 68:
2892						R = 47f / 51f;
2893						G = 0.4117647f;
2894						B = 1f;
2895						break;
2896					case 69:
2897						R = 38f / 51f;
2898						G = 38f / 51f;
2899						B = 1f;
2900						break;
2901					case 70:
2902						R = 43f / 51f;
2903						G = 35f / 51f;
2904						B = 49f / 51f;
2905						break;
2906					default:
2907						R = 1f;
2908						G = 1f;
2909						B = 1f;
2910						break;
2911					}
2912					break;
2913				case 49:
2914					if (tile.frameX == 0)
2915					{
2916						R = 0f;
2917						G = 0.35f;
2918						B = 0.8f;
2919					}
2920					break;
2921				case 519:
2922					if (tile.frameY == 90)
2923					{
2924						if (tile.color() == 0)
2925						{
2926							float num12 = (float)localRandom.Next(28, 42) * 0.005f;
2927							num12 += (float)(270 - Main.mouseTextColor) / 1000f;
2928							R = 0.1f;
2929							G = 0.2f + num12 / 2f;
2930							B = 0.7f + num12;
2931						}
2932						else
2933						{
2934							flag = true;
2935						}
2936					}
2937					break;
2938				case 70:
2939				case 71:
2940				case 72:
2941				case 190:
2942				case 348:
2943				case 349:
2944				case 528:
2945				case 578:
2946					if (tile.type != 349 || tile.frameX >= 36)
2947					{
2948						float num11 = (float)localRandom.Next(28, 42) * 0.005f;
2949						num11 += (float)(270 - Main.mouseTextColor) / 1000f;
2950						if (tile.color() == 0)
2951						{
2952							R = 0f;
2953							G = 0.2f + num11 / 2f;
2954							B = 1f;
2955						}
2956						else
2957						{
2958							flag = true;
2959						}
2960					}
2961					break;
2962				case 739:
2963					R = 0.35f;
2964					G = 0.63f;
2965					B = 0.7f;
2966					flag = true;
2967					break;
2968				case 350:
2969				{
2970					double num10 = Main.timeForVisualEffects * 0.08;
2971					B = (G = (R = (float)((0.0 - Math.Cos(((int)(num10 / 6.283) % 3 == 1) ? num10 : 0.0)) * 0.1 + 0.1)));
2972					break;
2973				}
2974				case 61:
2975				case 703:
2976					if (tile.frameX == 144)
2977					{
2978						float num6 = 1f + (float)(270 - Main.mouseTextColor) / 400f;
2979						float num7 = 0.8f - (float)(270 - Main.mouseTextColor) / 400f;
2980						R = 0.42f * num7;
2981						G = 0.81f * num6;
2982						B = 0.52f * num7;
2983					}
2984					break;
2985				case 26:
2986				case 31:
2987				case 695:
2988				case 696:
2989					if (((tile.type == 31 || tile.type == 696) && tile.frameX >= 36) || ((tile.type == 26 || tile.type == 695) && tile.frameX >= 54))
2990					{
2991						float num4 = (float)localRandom.Next(-5, 6) * 0.0025f;
2992						R = 0.5f + num4 * 2f;
2993						G = 0.2f + num4;
2994						B = 0.1f;
2995					}
2996					else
2997					{
2998						float num5 = (float)localRandom.Next(-5, 6) * 0.0025f;
2999						R = 0.31f + num5;
3000						G = 0.1f;
3001						B = 0.44f + num5 * 2f;
3002					}
3003					break;
3004				case 699:
3005					R = 0.4f;
3006					G = 0.2f;
3007					B = 0.15f;
3008					break;
3009				case 84:
3010				{
3011					int num2 = tile.frameX / 18;
3012					float num3 = 0f;
3013					switch (num2)
3014					{
3015					case 2:
3016						num3 = (float)(270 - Main.mouseTextColor) / 400f;
3017						if (num3 > 1f)
3018						{
3019							num3 = 1f;
3020						}
3021						else if (num3 < 0f)
3022						{
3023							num3 = 0f;
3024						}
3025						R = num3 * 1.4f;
3026						G = num3 * 1.2f;
3027						B = num3 / 2f;
3028						break;
3029					case 5:
3030						num3 = 0.9f;
3031						R = num3;
3032						G = num3 * 0.8f;
3033						B = num3 * 0.2f;
3034						break;
3035					case 6:
3036						num3 = 0.08f;
3037						G = num3 * 0.8f;
3038						B = num3;
3039						break;
3040					}
3041					break;
3042				}
3043				case 83:
3044					if (tile.frameX == 18 && !Main.dayTime)
3045					{
3046						R = 0.1f;
3047						G = 0.4f;
3048						B = 0.6f;
3049					}
3050					if (tile.frameX == 90 && !Main.raining && Main.time > 40500.0)
3051					{
3052						R = 0.9f;
3053						G = 0.72f;
3054						B = 0.18f;
3055					}
3056					break;
3057				case 126:
3058					if (tile.frameX < 36)
3059					{
3060						R = (float)Main.DiscoR / 255f;
3061						G = (float)Main.DiscoG / 255f;
3062						B = (float)Main.DiscoB / 255f;
3063					}
3064					break;
3065				case 125:
3066				{
3067					float num = (float)localRandom.Next(28, 42) * 0.01f;
3068					num += (float)(270 - Main.mouseTextColor) / 800f;
3069					G = (lightColor.Y = 0.3f * num);
3070					B = (lightColor.Z = 0.6f * num);
3071					break;
3072				}
3073				case 129:
3074					switch (tile.frameX / 18 % 3)
3075					{
3076					case 0:
3077						R = 0f;
3078						G = 0.05f;
3079						B = 0.25f;
3080						break;
3081					case 1:
3082						R = 0.2f;
3083						G = 0f;
3084						B = 0.15f;
3085						break;
3086					case 2:
3087						R = 0.1f;
3088						G = 0f;
3089						B = 0.2f;
3090						break;
3091					}
3092					break;
3093				case 149:
3094					if (tile.frameX <= 36)
3095					{
3096						switch (tile.frameX / 18)
3097						{
3098						case 0:
3099							R = 0.1f;
3100							G = 0.2f;
3101							B = 0.5f;
3102							break;
3103						case 1:
3104							R = 0.5f;
3105							G = 0.1f;
3106							B = 0.1f;
3107							break;
3108						case 2:
3109							R = 0.2f;
3110							G = 0.5f;
3111							B = 0.1f;
3112							break;
3113						}
3114						R *= (float)localRandom.Next(970, 1031) * 0.001f;
3115						G *= (float)localRandom.Next(970, 1031) * 0.001f;
3116						B *= (float)localRandom.Next(970, 1031) * 0.001f;
3117					}
3118					break;
3119				case 160:
3120					R = (float)Main.DiscoR / 255f * 0.25f;
3121					G = (float)Main.DiscoG / 255f * 0.25f;
3122					B = (float)Main.DiscoB / 255f * 0.25f;
3123					break;
3124				case 354:
3125					R = 0.65f;
3126					G = 0.35f;
3127					B = 0.15f;
3128					break;
3129				}
3130			}
3131			if (flag && tile.color() != 0)
3132			{
3133				Color color2 = WorldGen.paintColor(tile.color());
3134				R = (float)(int)color2.R / 255f;
3135				G = (float)(int)color2.G / 255f;
3136				B = (float)(int)color2.B / 255f;
3137			}
3138			if (lightColor.X < R)
3139			{
3140				lightColor.X = R;
3141			}
3142			if (lightColor.Y < G)
3143			{
3144				lightColor.Y = G;
3145			}
3146			if (lightColor.Z < B)
3147			{
3148				lightColor.Z = B;
3149			}
3150		}
3151	
3152		private void ApplySurfaceLight(Tile tile, int x, int y, ref Vector3 lightColor)
3153		{
3154			float num = 0f;
3155			float num2 = 0f;
3156			float num3 = 0f;
3157			float num4 = (float)(int)Main.tileColor.R / 255f;
3158			float num5 = (float)(int)Main.tileColor.G / 255f;
3159			float num6 = (float)(int)Main.tileColor.B / 255f;
3160			float num7 = (num4 + num5 + num6) / 3f;
3161			if (tile.active() && TileID.Sets.AllowLightInWater[tile.type])
3162			{
3163				if (lightColor.X < num7 && (Main.wallLight[tile.wall] || tile.wall == 73 || tile.wall == 227 || (tile.invisibleWall() && !_drawInvisibleWalls)))
3164				{
3165					num = num4;
3166					num2 = num5;
3167					num3 = num6;
3168				}
3169			}
3170			else if ((!tile.active() || !Main.tileNoSunLight[tile.type] || ((tile.slope() != 0 || tile.halfBrick() || (tile.invisibleBlock() && !_drawInvisibleWalls)) && Main.tile[x, y - 1].liquid == 0 && Main.tile[x, y + 1].liquid == 0 && Main.tile[x - 1, y].liquid == 0 && Main.tile[x + 1, y].liquid == 0)) && lightColor.X < num7 && (Main.wallLight[tile.wall] || tile.wall == 73 || tile.wall == 227 || (tile.invisibleWall() && !_drawInvisibleWalls)))
3171			{
3172				if (tile.liquid < 200)
3173				{
3174					if (!tile.halfBrick() || Main.tile[x, y - 1].liquid < 200)
3175					{
3176						num = num4;
3177						num2 = num5;
3178						num3 = num6;
3179					}
3180				}
3181				else if (Main.liquidAlpha[13] > 0f)
3182				{
3183					if (Main.rand == null)
3184					{
3185						Main.rand = new UnifiedRandom();
3186					}
3187					num3 = num6 * 0.175f * (1f + Main.rand.NextFloat() * 0.13f) * Main.liquidAlpha[13];
3188				}
3189			}
3190			if ((!tile.active() || tile.halfBrick() || !Main.tileNoSunLight[tile.type]) && ((tile.wall >= 88 && tile.wall <= 93) || tile.wall == 241) && tile.liquid < byte.MaxValue)
3191			{
3192				num = num4;
3193				num2 = num5;
3194				num3 = num6;
3195				int num8 = tile.wall - 88;
3196				if (tile.wall == 241)
3197				{
3198					num8 = 6;
3199				}
3200				switch (num8)
3201				{
3202				case 0:
3203					num *= 0.9f;
3204					num2 *= 0.15f;
3205					num3 *= 0.9f;
3206					break;
3207				case 1:
3208					num *= 0.9f;
3209					num2 *= 0.9f;
3210					num3 *= 0.15f;
3211					break;
3212				case 2:
3213					num *= 0.15f;
3214					num2 *= 0.15f;
3215					num3 *= 0.9f;
3216					break;
3217				case 3:
3218					num *= 0.15f;
3219					num2 *= 0.9f;
3220					num3 *= 0.15f;
3221					break;
3222				case 4:
3223					num *= 0.9f;
3224					num2 *= 0.15f;
3225					num3 *= 0.15f;
3226					break;
3227				case 5:
3228				{
3229					float num9 = 0.2f;
3230					float num10 = 0.7f - num9;
3231					num *= num10 + (float)Main.DiscoR / 255f * num9;
3232					num2 *= num10 + (float)Main.DiscoG / 255f * num9;
3233					num3 *= num10 + (float)Main.DiscoB / 255f * num9;
3234					break;
3235				}
3236				case 6:
3237					num *= 0.9f;
3238					num2 *= 0.5f;
3239					num3 *= 0f;
3240					break;
3241				}
3242			}
3243			float num11 = 1f - Main.shimmerDarken;
3244			num *= num11;
3245			num2 *= num11;
3246			num3 *= num11;
3247			if (lightColor.X < num)
3248			{
3249				lightColor.X = num;
3250			}
3251			if (lightColor.Y < num2)
3252			{
3253				lightColor.Y = num2;
3254			}
3255			if (lightColor.Z < num3)
3256			{
3257				lightColor.Z = num3;
3258			}
3259		}
3260	
3261		private void ApplyHellLight(Tile tile, int x, int y, ref Vector3 lightColor)
3262		{
3263			float num = 0f;
3264			float num2 = 0f;
3265			float num3 = 0f;
3266			float num4 = 0.55f + (float)Math.Sin(Main.GlobalTimeWrappedHourly * 2f) * 0.08f;
3267			if ((!tile.active() || !Main.tileNoSunLight[tile.type] || ((tile.slope() != 0 || tile.halfBrick()) && Main.tile[x, y - 1].liquid == 0 && Main.tile[x, y + 1].liquid == 0 && Main.tile[x - 1, y].liquid == 0 && Main.tile[x + 1, y].liquid == 0)) && lightColor.X < num4 && (Main.wallLight[tile.wall] || tile.wall == 73 || tile.wall == 227 || (tile.invisibleWall() && !_drawInvisibleWalls)) && tile.liquid < 200 && (!tile.halfBrick() || Main.tile[x, y - 1].liquid < 200))
3268			{
3269				num = num4;
3270				num2 = num4 * 0.6f;
3271				num3 = num4 * 0.2f;
3272			}
3273			if ((!tile.active() || tile.halfBrick() || !Main.tileNoSunLight[tile.type]) && ((tile.wall >= 88 && tile.wall <= 93) || tile.wall == 241) && tile.liquid < byte.MaxValue)
3274			{
3275				num = num4;
3276				num2 = num4 * 0.6f;
3277				num3 = num4 * 0.2f;
3278				int num5 = tile.wall - 88;
3279				if (tile.wall == 241)
3280				{
3281					num5 = 6;
3282				}
3283				switch (num5)
3284				{
3285				case 0:
3286					num *= 0.9f;
3287					num2 *= 0.15f;
3288					num3 *= 0.9f;
3289					break;
3290				case 1:
3291					num *= 0.9f;
3292					num2 *= 0.9f;
3293					num3 *= 0.15f;
3294					break;
3295				case 2:
3296					num *= 0.15f;
3297					num2 *= 0.15f;
3298					num3 *= 0.9f;
3299					break;
3300				case 3:
3301					num *= 0.15f;
3302					num2 *= 0.9f;
3303					num3 *= 0.15f;
3304					break;
3305				case 4:
3306					num *= 0.9f;
3307					num2 *= 0.15f;
3308					num3 *= 0.15f;
3309					break;
3310				case 5:
3311				{
3312					float num6 = 0.2f;
3313					float num7 = 0.7f - num6;
3314					num *= num7 + (float)Main.DiscoR / 255f * num6;
3315					num2 *= num7 + (float)Main.DiscoG / 255f * num6;
3316					num3 *= num7 + (float)Main.DiscoB / 255f * num6;
3317					break;
3318				}
3319				case 6:
3320					num *= 0.9f;
3321					num2 *= 0.5f;
3322					num3 *= 0f;
3323					break;
3324				}
3325			}
3326			if (lightColor.X < num)
3327			{
3328				lightColor.X = num;
3329			}
3330			if (lightColor.Y < num2)
3331			{
3332				lightColor.Y = num2;
3333			}
3334			if (lightColor.Z < num3)
3335			{
3336				lightColor.Z = num3;
3337			}
3338		}
3339	}
3340	

```


---

## 🤖 Assistant · 2026-08-13T06:15:09.394Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have the full vanilla scanner. Next read the repo files: TileLightScanner.ts, lightTables.ts, and tiles.ts. Also TorchID.cs and Main.cs wallLight section.

Note this vanilla is 1.4.5 (Terarria1456), and it includes TileLoader? Actually ApplyTileLight here — in vanilla 1.4.4+ there's also TileLoader.ModifyLight. Let me check. Actually in this decompiled version the switch is fully inline. Note tile 739 exists — 1.4.5 new tile.

Let me read repo files.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:15:09.558Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/lighting/TileLightScanner.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:15:09.582Z

**📎 ToolResult**

```
1	// 播种扫描器(Terrarria1456 Terraria.Graphics.Light/TileLightScanner.cs 一比一主干)。
2	// GetTileMask(:68-87):遮挡分类;GetTileLight(:89-108):逐格 max-raise 播种
3	// (天空 ApplySurfaceLight:3152 → 地狱 ApplyHellLight:3261 → 墙 :167 → tile :344 → 液体 :110)。
4	// 洞穴(worldSurface..UnderworldLayer)零环境光。
5	import { TILE_DEFS } from '../data/tiles';
6	import { lightIsOn } from '../world/wiring/devices';
7	import { TileStore } from '../world/TileStore';
8	import { FastRandom } from './FastRandom';
9	import { CRACKED_SHEETS, FLICKER_SHEETS, MUSHROOM_GLOW_SHEETS, TORCH_COLORS, WALL_EMISSIVE, WALL_LIGHT } from './lightTables';
10	import { FlickerClock, skySeed } from './SkyColor';
11	import { LightMap, Mask } from './LightMap';
12	
13	/** 扫描器依赖的最小世界结构(引擎注入;World 满足该接口) */
14	export interface ScannerWorld {
15	  store: TileStore;
16	  groundLevel: number;  // 原版 worldSurface
17	  lavaLine: number;     // 原版 UnderworldLayer
18	  clock: { timeOfDay: number; dayCount: number; eclipse?: boolean };
19	}
20	
21	/** 动态点光(原版 Lighting.AddLight;0-1 RGB) */
22	export interface PerFrameLight { x: number; y: number; r: number; g: number; b: number }
23	
24	/**
25	 * 动态发光特例（原版 ApplyTileLight 帧条件/动态色 case 1:1）：
26	 * - 126 迪斯科球：frameX<36 → Disco RGB（TileLightScanner.cs:3057）
27	 * - 429 导线灯泡：frameX/18 位段 → 各线色 +0.5、致动器 +0.2R/G（cs:881-905）
28	 * - 209 传送门炮：frameX 234/252（紫）306/324（橙）×0.65（cs:432，PortalHelper 色近似）
29	 * - 84 开花药草：style2 死亡草随闪烁暗红 / style5 火焰草橙 / style6 颤骨草淡蓝（cs:3009）
30	 */
31	export function specialTileLight(
32	  sheet: number, frameX: number, frameY: number, flicker: FlickerClock,
33	): [number, number, number] | null {
34	  switch (sheet) {
35	    case 42: {
36	      // 灯笼(TileLightScanner 主 switch case 42):frameX!=0(灭档 18)不发光;
37	      // 光色按样式行 frameY/36 —— def.light 静态单色由 lantern def 移除,全走此表
38	      if (frameX !== 0) return null;
39	      const LANTERN_LIGHT: Record<number, [number, number, number]> = {
40	        0: [0.7, 0.65, 0.55], 1: [0.9, 0.75, 0.6], 2: [0.8, 0.6, 0.6],
41	        3: [0.65, 0.5, 0.2], 4: [0.5, 0.7, 0.4], 5: [0.9, 0.4, 0.2],
42	        6: [0.7, 0.75, 0.3], 8: [0.75, 0.6, 0.3],
43	        // 7/9 = demonTorch 调制档，见下方动态分支
44	        11: [0.85, 0.6, 1], 14: [1, 0.95, 0.65],
45	      };
46	      // 样式 7/9 原版叠加 Main.demonTorch 调制——并非火把计数，而是全局三角波
47	      // （Main.cs:1286 初值 1、DoUpdate_AnimateTileGlows :18089-18100 ±0.01/t 钳 0..1，
48	      // 周期 200t）：style7 cs:2638-2645 R=G=0.9-d*0.2、B=0.7+d*0.2；
49	      // style9 cs:2646-2652 R=1-d*0.1、G=0.3-d*0.2、B=0.5+d*0.2（FlickerClock.demonTorch
50	      // 已同构维护该波形，旧"取中值 0.5 近似"已退役）
51	      const st = Math.floor(frameY / 36);
52	      if (st === 7) {
53	        const n14 = flicker.demonTorch * 0.2;
54	        return [0.9 - n14, 0.9 - n14, 0.7 + n14];
55	      }
56	      if (st === 9) {
57	        const d = flicker.demonTorch;
58	        return [1 - d * 0.1, 0.3 - d * 0.2, 0.5 + d * 0.2];
59	      }
60	      return LANTERN_LIGHT[st] ?? [0.7, 0.65, 0.55];
61	    }
62	    case 126:
63	      if (frameX < 36) {
64	        const [r, g, b] = flicker.discoColor();
65	        return [r, g, b];
66	      }
67	      return null;
68	    case 429: {
69	      const n = Math.floor(frameX / 18);
70	      let r = 0, g = 0, b = 0;
71	      if (n % 2 >= 1) r += 0.5;
72	      if (n % 4 >= 2) g += 0.5;
73	      if (n % 8 >= 4) b += 0.5;
74	      if (n % 16 >= 8) { r += 0.2; g += 0.2; }
75	      return [r, g, b];
76	    }
77	    case 209:
78	      if (frameX === 234 || frameX === 252) return [0.42, 0.2, 0.65];   // 传送门 1 紫 ×0.65
79	      if (frameX === 306 || frameX === 324) return [0.65, 0.26, 0];     // 传送门 2 橙 ×0.65
80	      return null;
81	    case 84: {
82	      const style = Math.floor(frameX / 18);
83	      if (style === 2) {
84	        const n = Math.max(0, Math.min(1, (270 - flicker.mouseTextColor) / 400));
85	        return [n * 1.4, n * 1.2, n / 2];
86	      }
87	      if (style === 5) return [0.9, 0.72, 0.18];
88	      if (style === 6) return [0, 0.08 * 0.8, 0.08];
89	      return null;
90	    }
91	    default:
92	      return null;
93	  }
94	}
95	
96	export class TileLightScanner {
97	  private blocksLight: Uint8Array;
98	  private random = new FastRandom(0x9e3779b9);
99	  /** 每格局部随机(WithModifier(x,y);蜡烛闪烁) */
100	  private localRandom(x: number, y: number): FastRandom {
101	    return this.random.withModifier((y * 2654435761 + x) | 0);
102	  }
103	
104	  constructor(private flicker: FlickerClock) {
105	    // 从 TILE_DEFS 派生 tileBlockLight 近似(原版 Main.tileBlockLight[]):
106	    // 实心且近乎不透明才挡光——门(0.05)/平台(0.15)/树(0.1)/装饰(0.05)均不挡
107	    this.blocksLight = new Uint8Array(TILE_DEFS.length);
108	    TILE_DEFS.forEach((d, i) => {
109	      if (d && d.solid && !d.platform && d.opacity >= 0.9) this.blocksLight[i] = 1;
110	    });
111	  }
112	
113	  /** GetTileMask(:68-87) */
114	  getMask(st: TileStore, i: number): Mask {
115	    const type = st.type[i];
116	    const actuated = (st.wire[i] & TileStore.WIRE_ACTUATED) !== 0;
117	    if (type !== 0 && !actuated && this.blocksLight[type] && st.slope[i] === 0) {
118	      // 注意 actuated 已在上条件排除(原版 !tile.inActive())
119	      const sheet = TILE_DEFS[type]?.vanilla?.sheet ?? -1;
120	      return CRACKED_SHEETS.has(sheet) ? Mask.CrackedBricks : Mask.Solid;
121	    }
122	    if (st.liquidType[i] !== 2 && st.liquid[i] > 128) { // 岩浆 mask=None 只发光
123	      return st.liquidType[i] === 3 ? Mask.Honey : Mask.Water;
124	    }
125	    return Mask.None;
126	  }
127	
128	  /** 该格是否暴露于"天空/地狱光"(ApplySurfaceLight :3170 / ApplyHellLight :3270
129	   *  同构判定)。放行 = 满足下列任一 + 墙透光：
130	   *    ① 非活动(空气/水) 或 非挡阳类型；② 坡面/半砖 且【四邻液量全为 0】
131	   *  ——挡阳实心格（海底泥沙等）恒不放行：深水下海底不播天光，亮度只经水层
132	   *  传播衰减而来。此前误植为"自身 liquid>=200 才挡"= 海底方块自身无液被放行
133	   *  → 水底地面满天光自发光 */
134	  private exposed(st: TileStore, x: number, y: number): boolean {
135	    const i = st.idx(x, y);
136	    const type = st.type[i];
137	    if (type !== 0) {
138	      const actuated = (st.wire[i] & TileStore.WIRE_ACTUATED) !== 0;
139	      // AllowLightInWater（TileID.cs:359：玻璃 54/回声 541/彩纸 328/降雪 459/
140	      // 水族馆 748/尖刺 750）——水中也透天光（:3161 独立分支）
141	      const sheet = TILE_DEFS[type]?.vanilla?.sheet ?? -1;
142	      if (sheet === 54 || sheet === 541 || sheet === 328 || sheet === 459 || sheet === 748 || sheet === 750) {
143	        // 落到墙透光判定（原版此分支同样要求 wallLight）
144	      } else if (!actuated && this.blocksLight[type]) {
145	        if (st.slope[i] === 0 && st.half[i] === 0) return false;
146	        // 坡面/半砖例外：四邻必须全干（:3170 第三析取支的邻格 liquid==0）
147	        if (st.liquid[st.idx(x, y - 1)] !== 0 || st.liquid[st.idx(x, y + 1)] !== 0
148	          || st.liquid[st.idx(x - 1, y)] !== 0 || st.liquid[st.idx(x + 1, y)] !== 0) return false;
149	      }
150	    }
151	    const wall = st.wall[i];
152	    return wall === 0 || WALL_LIGHT.has(wall);
153	  }
154	
155	  /** ExportTo(:17-43)+ GetTileLight(:89-108):向工作图播种 mask 与颜色 */
156	  exportTo(w: ScannerWorld, map: LightMap, rx: number, ry: number, perFrame: PerFrameLight[]): void {
157	    const st = w.store;
158	    map.clear();
159	    const [skyR, skyG, skyB] = skySeed(w.clock.timeOfDay, w.clock.dayCount, !!w.clock.eclipse);
160	    // 地狱脉动(ApplyHellLight:3266-3271)
161	    const hellV = 0.55 + Math.sin(performance.now() * 0.002) * 0.08; // GlobalTimeWrappedHourly 近似
162	    const hellR = hellV, hellG = hellV * 0.6, hellB = hellV * 0.2;
163	    // 岩浆闪烁基础(ApplyLiquidLight:118-131)
164	    const lavaV = 0.55 + (270 - this.flicker.mouseTextColor) / 900;
165	    const osc = this.flicker.mouseTextColor;
166	
167	    for (let ly = 0; ly < map.h; ly++) {
168	      const ty = ry + ly;
169	      for (let lx = 0; lx < map.w; lx++) {
170	        const tx = rx + lx;
171	        if (tx < 1 || ty < 1 || tx >= st.w - 1 || ty >= st.h - 1) continue; // InWorld(x,y,1)
172	        const i = st.idx(tx, ty);
173	        const li = ly * map.w + lx;
174	        map.mask[li] = this.getMask(st, i);
175	
176	        let lr = 0, lg = 0, lb = 0;
177	        // ★ 深度门 liquid<200（ApplySurfaceLight :3172 / ApplyHellLight :3270）：
178	        //   仅液量 <200（表面 ~4/5 格）播满天空/地狱光；深层液体不播——亮度靠
179	        //   表层向深水传播（水衰减逐格 0.88×0.91 系）→ 水体越深越暗。此前漏此门
180	        //   整个水柱每层播满 = 深水自发光
181	        const shallowLiquid = st.liquid[i] < 200;
182	        // ① 天空 / 地狱(:94-101)
183	        if (ty <= w.groundLevel) {
184	          if (shallowLiquid && this.exposed(st, tx, ty)) { lr = skyR; lg = skyG; lb = skyB; }
185	        } else if (ty > w.lavaLine) {
186	          if (shallowLiquid && this.exposed(st, tx, ty)) { lr = Math.max(lr, hellR); lg = Math.max(lg, hellG); lb = Math.max(lb, hellB); }
187	        }
188	        // ② 发光墙(:102;大多要求 !LightIsBlocked——此处墙在实心块后不可见,实心格直接跳过)
189	        const wall = st.wall[i];
190	        if (wall !== 0 && st.type[i] === 0) {
191	          const we = WALL_EMISSIVE[wall];
192	          if (we) { lr = Math.max(lr, we[0]); lg = Math.max(lg, we[1]); lb = Math.max(lb, we[2]); }
193	          // 彩色玻璃墙彩光（ApplySurfaceLight :3190-3242）：墙 88-93（紫/黄/蓝/绿/
194	          // 红/彩虹玻璃）/241 橙——格式满光后按墙种 RGB 乘区染色（switch wall-88 档）
195	          if ((wall >= 88 && wall <= 93) || wall === 241) {
196	            const k = wall === 241 ? 6 : wall - 88;
197	            const TINT: Array<[number, number, number]> = [
198	              [0.9, 0.15, 0.9], [0.9, 0.9, 0.15], [0.15, 0.15, 0.9], [0.15, 0.9, 0.15],
199	              [0.9, 0.15, 0.15], [0.7 + 0.2, 0.7, 0.7], [0.9, 0.5, 0],
200	            ];
201	            // 原版 switch：0 紫(0.9,0.15,0.9) 1 黄(0.9,0.9,0.15) 2 蓝(0.15,0.15,0.9)
202	            // 3 绿(0.15,0.9,0.15) 4 红(0.9,0.15,0.15) 5 彩虹(0.7+Disco×0.2) 6 橙(0.9,0.5,0)
203	            const dc = this.flicker.discoColor();  // Main.Disco 轮转（:3229-3233 彩虹档）
204	            const t = k === 5
205	              ? [0.7 + (dc[0] / 255) * 0.2, 0.7 + (dc[1] / 255) * 0.2, 0.7 + (dc[2] / 255) * 0.2]
206	              : TINT[k];
207	            // 此分支原版作用在天空光之上（num=num4 系）且要求 tile 不挡阳/液<255：
208	            // 此处以 max 合成等效（墙格无挡阳块时天空已满 → 乘区改写）
209	            lr = Math.max(lr, t[0]); lg = Math.max(lg, t[1]); lb = Math.max(lb, t[2]);
210	          }
211	        }
212	        // ③ 发光 tile(:103-106)
213	        const type = st.type[i];
214	        if (type !== 0 && (st.wire[i] & TileStore.WIRE_ACTUATED) === 0) {
215	          const d = TILE_DEFS[type];
216	          const sheet = d?.vanilla?.sheet ?? -1;
217	          // 蘑菇雕像 349 门控(:2940):frameX<36 的 style 完全不发光——
218	          // 同时压制组公式与 def.light 静态兜底,故提到入口处判
219	          const shroomGateOk = !(sheet === 349 && st.frameX[i] < 36);
220	          if (d && (d.light || MUSHROOM_GLOW_SHEETS.has(sheet)) && shroomGateOk) {
221	            // 接线灯门控:关帧不发光(LIGHT_TOGGLE)
222	            const on = sheet < 0 || lightIsOn(sheet, st.frameX[i], st.frameY[i]);
223	            if (on) {
224	              let er: number, eg: number, eb: number;
225	              if (sheet === 4) {
226	                // 火把:24 色动态(TorchID;frameY/22 = style)
227	                const style = Math.floor(st.frameY[i] / 22) % 24;
228	                if (style === 7) [er, eg, eb] = this.flicker.demonTorchColor();
229	                else if (style === 14) [er, eg, eb] = this.flicker.discoColor();
230	                else if (style === 23) [er, eg, eb] = this.flicker.shimmerTorchColor();
231	                else {
232	                  const c = TORCH_COLORS[style] ?? TORCH_COLORS[0];
233	                  [er, eg, eb] = c;
234	                }
235	                // 蜡烛/篝火族闪烁(:1034-1036:localRand.Next(28,42)*0.005+(270-mouseTextColor)/700)
236	                const f = this.localRandom(tx, ty).next(28, 42) * 0.005 + (270 - osc) / 700;
237	                er += f; eg += f; eb += f;
238	              } else if (MUSHROOM_GLOW_SHEETS.has(sheet)) {
239	                // 蘑菇组发光（TileLightScanner.cs:2938-2960 case 70/71/72/190/348/349/528/578）：
240	                //   R=0、B=1，G=0.2+num11/2；num11=Next(28,42)*0.005+(270-mouseTextColor)/1000
241	                //   ——只抬 G（与 FLICKER_SHEETS 的三通道叠加不同）
242	                const num11 = this.localRandom(tx, ty).next(28, 42) * 0.005 + (270 - osc) / 1000;
243	                er = 0; eg = 0.2 + num11 / 2; eb = 1;
244	              } else {
245	                er = d.light![0] / 255; eg = d.light![1] / 255; eb = d.light![2] / 255;
246	                if (FLICKER_SHEETS.has(sheet)) {
247	                  const f = this.localRandom(tx, ty).next(28, 42) * 0.005 + (270 - osc) / 700;
248	                  er += f; eg += f; eb += f;
249	                }
250	              }
251	              lr = Math.max(lr, er); lg = Math.max(lg, eg); lb = Math.max(lb, eb);
252	            }
253	          }
254	          // ③b 动态发光特例（原版 ApplyTileLight 帧条件/动态色 case，def.light 静态表无法表达）
255	          const spSheet = d?.vanilla?.sheet ?? -1;
256	          const sp = specialTileLight(spSheet, st.frameX[i], st.frameY[i], this.flicker);
257	          if (sp) {
258	            lr = Math.max(lr, sp[0]); lg = Math.max(lg, sp[1]); lb = Math.max(lb, sp[2]);
259	          }
260	        }
261	        // ④ 液体光(:107;岩浆发光,水/蜂蜜不发光)
262	        if (st.liquid[i] > 0 && st.liquidType[i] === 2) {
263	          lr = Math.max(lr, lavaV); lg = Math.max(lg, lavaV * 0.6); lb = Math.max(lb, lavaV * 0.2);
264	        }
265	        map.r[li] = lr; map.g[li] = lg; map.b[li] = lb;
266	      }
267	    }
268	    // ⑤ 动态点光(ApplyPerFrameLights:204-227;区域内 max 合并)
269	    for (const l of perFrame) {
270	      const lx = l.x - rx, ly = l.y - ry;
271	      if (lx < 0 || ly < 0 || lx >= map.w || ly >= map.h) continue;
272	      const li = ly * map.w + lx;
273	      if (l.r > map.r[li]) map.r[li] = l.r;
274	      if (l.g > map.g[li]) map.g[li] = l.g;
275	      if (l.b > map.b[li]) map.b[li] = l.b;
276	    }
277	  }
278	}
279	

```


---

## 🤖 Assistant · 2026-08-13T06:15:09.746Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/lighting/lightTables.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:15:09.764Z

**📎 ToolResult**

```
1	// 光照常数与数据表(Terarria1456 Terraria.Graphics.Light/ 一比一提取)。
2	// 行号注释指向原版源码;所有颜色为 0-1 浮点 RGB。
3	
4	// ---- 传播衰减(LightMap.cs:47-58 默认值 / LightingEngine.cs:137-202 每帧覆盖) ----
5	// let + setter:LightingEngine.UpdateLightDecay 每帧按 waterStyle/夜枭覆盖(ESM live binding,
6	// LightMap 读到的即最新值)。基线:air 0.91 / solid 0.56 / honey (0.75,0.7,0.6)×0.91。
7	const NIGHT_VISION_MUL = 1.03;   // 夜枭 buff(UpdateLightDecay :184-187)
8	let nightVision = false;
9	export let DECAY_AIR = 0.91;
10	export let DECAY_SOLID = 0.56;
11	export const DECAY_CRACKED = 0.80;
12	/** 水衰减(按群系水色分 13 种,LightingEngine.cs:143-180;默认 0/1/7/8 基准) */
13	export let DECAY_WATER: [number, number, number] = [0.88 * 0.91, 0.96 * 0.91, 1.015 * 0.91];
14	/** 蜂蜜衰减 */
15	export const DECAY_HONEY: [number, number, number] = [0.75 * 0.91, 0.70 * 0.91, 0.60 * 0.91];
16	
17	/** LightingEngine.UpdateLightDecay :143-180 全表(每 waterStyle 的 RGB 水下衰减) */
18	const WATER_DECAY_BY_STYLE: Array<[number, number, number]> = [
19	  [0.88, 0.96, 1.015],  // 0 纯净(1 岩浆/7 地下/8 洞穴同)
20	  [0.88, 0.96, 1.015],  // 1 岩浆水域(原版同 case)
21	  [0.94, 0.85, 1.01],   // 2 腐化
22	  [0.84, 0.95, 1.015],  // 3 丛林
23	  [0.9, 0.86, 1.01],    // 4 神圣
24	  [0.84, 0.99, 1.01],   // 5 雪原
25	  [0.83, 0.93, 0.98],   // 6 沙漠
26	  [0.88, 0.96, 1.015],  // 7 地下
27	  [0.88, 0.96, 1.015],  // 8 洞穴
28	  [1.0, 0.88, 0.84],    // 9 血月
29	  [0.83, 1.0, 1.0],     // 10 猩红
30	  [0.88, 0.96, 1.015],  // 11 蜂蜜(原版 switch 无 11 → 保持基准)
31	  [0.95, 0.98, 0.85],   // 12 地下沙漠
32	  [0.9, 1.0, 1.02],     // 13 地狱
33	];
34	/** Game 每帧调用:按当前群系水色 + 夜枭更新衰减表(:137-187 主干) */
35	export function updateLightDecay(waterStyle: number, nightVisionOn: boolean, blackoutOn = false): void {
36	  nightVision = nightVisionOn;
37	  const base = WATER_DECAY_BY_STYLE[Math.max(0, Math.min(13, waterStyle))];
38	  DECAY_WATER = [base[0] * 0.91, base[1] * 0.91, base[2] * 0.91];
39	  // blackout（buff 80，Torch God 事件每 tick 刷新）×0.85（UpdateLightDecay :181-183）
40	  const blk = blackoutOn ? 0.85 : 1;
41	  DECAY_AIR = 0.91 * (nightVision ? NIGHT_VISION_MUL : 1) * blk;
42	  DECAY_SOLID = 0.56 * (nightVision ? NIGHT_VISION_MUL : 1) * blk;
43	  // 原版另有 blind ×0.95 / headcovered ×0.85 与 SceneState 调制——对应系统未实装,跳过
44	}
45	/** 通道熄灭阈值(LightMap.cs:132/148/164) */
46	export const DEAD_THRESHOLD = 0.0185;
47	/** 全局亮度(Lighting.cs:12-14) */
48	export const GLOBAL_BRIGHTNESS = 1.2;
49	/** 区域外扩(LightingEngine.cs:28)与不可见边距(:30) */
50	export const AREA_PADDING = 28;
51	export const NON_VISIBLE_PADDING = 18;
52	
53	// ---- 遮挡(LightMaskMode.cs / TileLightScanner.GetTileMask:68-87) ----
54	/** 裂砖 → 0.80 衰减档(TileID.cs:183: CrackedBricks = {481,482,483}) */
55	export const CRACKED_SHEETS = new Set([481, 482, 483]);
56	/** 透光墙(Main.cs:10487-10503 wallLight 全表)——天空光可穿过的墙(0=无墙含在内由调用方处理) */
57	export const WALL_LIGHT = new Set([21, 318, 106, 317, 107, 138, 140, 141, 139, 145, 150, 152, 245, 315, 168]);
58	
59	// ---- 火把色(TorchID.cs:134-161 _lights 全表;0-1 RGB) ----
60	export const TORCH_COLORS: ReadonlyArray<readonly [number, number, number]> = [
61	  [1, 0.95, 0.8],      // 0 火把
62	  [0, 0.1, 1.3],       // 1 蓝
63	  [1, 0.1, 0.1],       // 2 红
64	  [0, 1, 0.1],         // 3 绿
65	  [0.9, 0, 0.9],       // 4 紫
66	  [1.4, 1.4, 1.4],     // 5 白
67	  [0.9, 0.9, 0],       // 6 黄
68	  [1, 0.3, 0.5],       // 7 恶魔(动态,见 SkyColor.demonTorch 插值)
69	  [1, 1.6, 0.5],       // 8 诅咒
70	  [0.75, 0.85, 1.4],   // 9 冰
71	  [1, 0.5, 0],         // 10 橙
72	  [1.4, 1.4, 0.7],     // 11 圣液
73	  [0.75, 1.35, 1.5],   // 12 超亮
74	  [0.95, 0.75, 1.3],   // 13 骨头
75	  [1, 1, 1],           // 14 彩虹(动态,见 SkyColor.disco)
76	  [1, 0, 1],           // 15 粉
77	  [1.4, 0.85, 0.55],   // 16 沙漠
78	  [0.25, 1.3, 0.8],    // 17 珊瑚
79	  [0.95, 0.4, 1.4],    // 18 腐化
80	  [1.4, 0.7, 0.5],     // 19 猩红
81	  [1.25, 0.6, 1.2],    // 20 神圣
82	  [0.75, 1.45, 0.9],   // 21 丛林
83	  [0.3, 0.78, 1.2],    // 22 蘑菇
84	  [1, 1, 1],           // 23 微光(动态,见 SkyColor)
85	];
86	/** 蜡烛/吊灯/篝火等闪烁幅度来源的 sheet 集(燃烧类光源) */
87	export const FLICKER_SHEETS = new Set([33, 49, 92, 93, 174, 34, 149, 95, 100, 126, 173, 564, 215, 405, 4]);
88	/** 蘑菇组发光 sheet(TileLightScanner.cs:2938 case 70/71/72/190/348/349/528/578；
89	 *  R=0 B=1 G=0.2+num11/2 的呼吸蓝光,与 FLICKER_SHEETS 三通道叠加不同) */
90	export const MUSHROOM_GLOW_SHEETS = new Set([70, 71, 72, 190, 348, 349, 528, 578]);
91	
92	// ---- 发光墙(ApplyWallLight:167-342 精选;[wallId] → RGB) ----
93	export const WALL_EMISSIVE: Record<number, readonly [number, number, number]> = {
94	  33: [0.09, 0.0525, 0.24],     // 恶魔砖墙
95	  44: [0.15, 0.15, 0.15],       // 彩虹砖(静态近似;动态 disco 见 phase2)
96	  137: [0.5, 0.25, 0.05],       // 岩浆瀑布墙
97	  153: [0.6, 0.12, 0.6],        // 紫水晶宝石灯墙
98	  154: [0.6, 0.12, 0.6],
99	  155: [0.6, 0.42, 0.06],       // 琥珀
100	  156: [0.09, 0.6, 0.24],       // 祖母绿
101	  164: [0.09, 0.24, 0.6],       // 蓝宝石
102	  165: [0.6, 0.06, 0.09],       // 红宝石
103	  166: [0.42, 0.42, 0.6],       // 钻石
104	  174: [0.2975, 0, 0],          // 猩红砖墙(仅 R)
105	  175: [0.075, 0.15, 0.4],      // 蘑菇护板
106	  176: [0.1, 0.1, 0.1],         // 火星导管
107	  182: [0.24, 0.12, 0.09],      // 陨石砖墙
108	  341: [0.25, 0.1, 0],          // 熔岩苔墙
109	  342: [0, 0.25, 0],
110	  343: [0.3, 0, 0.17],
111	  344: [0, 0.16, 0.34],
112	  345: [0.3, 0, 0.35],
113	  346: [0.25, 0.25, 0.25],      // 彩虹苔砖墙(静态近似)
114	  357: [0.15, 0.27, 0.3],       // 水母墙
115	};
116	
117	// ---- 月相地板(Main.cs:63230-63266;索引 = dayCount%8,相位序 Empty→Full→Empty) ----
118	export const MOON_FLOOR = [11, 13, 15, 17, 19, 17, 15, 13];
119	

```


---

## 🤖 Assistant · 2026-08-13T06:15:11.354Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read the TorchID.cs _lights section and Main.cs wallLight section.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:15:11.641Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TorchID.cs",
 "limit": 80,
 "offset": 100
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:15:11.649Z

**📎 ToolResult**

```
100		public const short Cursed = 8;
101	
102		public const short Ice = 9;
103	
104		public const short Orange = 10;
105	
106		public const short Ichor = 11;
107	
108		public const short UltraBright = 12;
109	
110		public const short Bone = 13;
111	
112		public const short Rainbow = 14;
113	
114		public const short Pink = 15;
115	
116		public const short Desert = 16;
117	
118		public const short Coral = 17;
119	
120		public const short Corrupt = 18;
121	
122		public const short Crimson = 19;
123	
124		public const short Hallowed = 20;
125	
126		public const short Jungle = 21;
127	
128		public const short Mushroom = 22;
129	
130		public const short Shimmer = 23;
131	
132		public static readonly short Count = 24;
133	
134		public static void Initialize()
135		{
136			ITorchLightProvider[] array = new ITorchLightProvider[Count];
137			array[0] = new ConstantTorchLight(1f, 0.95f, 0.8f);
138			array[1] = new ConstantTorchLight(0f, 0.1f, 1.3f);
139			array[2] = new ConstantTorchLight(1f, 0.1f, 0.1f);
140			array[3] = new ConstantTorchLight(0f, 1f, 0.1f);
141			array[4] = new ConstantTorchLight(0.9f, 0f, 0.9f);
142			array[5] = new ConstantTorchLight(1.4f, 1.4f, 1.4f);
143			array[6] = new ConstantTorchLight(0.9f, 0.9f, 0f);
144			array[7] = default(DemonTorchLight);
145			array[8] = new ConstantTorchLight(1f, 1.6f, 0.5f);
146			array[9] = new ConstantTorchLight(0.75f, 0.85f, 1.4f);
147			array[10] = new ConstantTorchLight(1f, 0.5f, 0f);
148			array[11] = new ConstantTorchLight(1.4f, 1.4f, 0.7f);
149			array[12] = new ConstantTorchLight(0.75f, 1.3499999f, 1.5f);
150			array[13] = new ConstantTorchLight(0.95f, 0.75f, 1.3f);
151			array[14] = default(DiscoTorchLight);
152			array[15] = new ConstantTorchLight(1f, 0f, 1f);
153			array[16] = new ConstantTorchLight(1.4f, 0.85f, 0.55f);
154			array[17] = new ConstantTorchLight(0.25f, 1.3f, 0.8f);
155			array[18] = new ConstantTorchLight(0.95f, 0.4f, 1.4f);
156			array[19] = new ConstantTorchLight(1.4f, 0.7f, 0.5f);
157			array[20] = new ConstantTorchLight(1.25f, 0.6f, 1.2f);
158			array[21] = new ConstantTorchLight(0.75f, 1.45f, 0.9f);
159			array[22] = new ConstantTorchLight(0.3f, 0.78f, 1.2f);
160			array[23] = default(ShimmerTorchLight);
161			_lights = array;
162		}
163	
164		public static void TorchColor(int torchID, out float R, out float G, out float B)
165		{
166			if (torchID < 0 || torchID >= _lights.Length)
167			{
168				R = (G = (B = 0f));
169			}
170			else
171			{
172				_lights[torchID].GetRGB(out R, out G, out B);
173			}
174		}
175	}
176	

```


---

## 🤖 Assistant · 2026-08-13T06:15:12.030Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '10470,10515p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "description": "Read Main.cs wallLight table"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:15:12.270Z

**📎 ToolResult**

```
		wallHouse[295] = true;
		wallHouse[296] = true;
		wallHouse[297] = true;
		wallHouse[298] = true;
		wallHouse[299] = true;
		wallHouse[300] = true;
		wallHouse[301] = true;
		wallHouse[302] = true;
		wallHouse[303] = true;
		wallHouse[304] = true;
		wallHouse[305] = true;
		wallHouse[306] = true;
		wallHouse[307] = true;
		wallHouse[308] = true;
		wallHouse[309] = true;
		wallHouse[310] = true;
		wallHouse[311] = true;
		wallLight[0] = true;
		wallLight[21] = true;
		wallLight[318] = true;
		wallLight[106] = true;
		wallLight[317] = true;
		wallLight[107] = true;
		wallLight[138] = true;
		wallLight[140] = true;
		wallLight[141] = true;
		wallLight[139] = true;
		wallLight[145] = true;
		wallLight[150] = true;
		wallLight[152] = true;
		wallLight[245] = true;
		wallLight[315] = true;
		wallLight[168] = true;
		for (int num5 = 0; num5 < WallID.Count; num5++)
		{
			wallDungeon[num5] = false;
		}
		wallDungeon[7] = true;
		wallDungeon[8] = true;
		wallDungeon[9] = true;
		wallDungeon[94] = true;
		wallDungeon[95] = true;
		wallDungeon[96] = true;
		wallDungeon[97] = true;
		wallDungeon[98] = true;
		wallDungeon[99] = true;

```


---

## 🤖 Assistant · 2026-08-13T06:15:28.610Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
WALL_LIGHT: repo has 15 entries including 0 handled by caller. Vanilla wallLight true: 0, 21, 318, 106, 317, 107, 138, 140, 141, 139, 145, 150, 152, 245, 315, 168 = 16 entries (0 + 15). Repo set: [21, 318, 106, 317, 107, 138, 140, 141, 139, 145, 150, 152, 245, 315, 168] = 15 entries, and wall===0 handled in `exposed()` as `wall === 0 || WALL_LIGHT.has(wall)`. So complete — but wait, wallLight is a bool[] initialized to false; is there anywhere else that sets wallLight? Let me grep for "wallLight[" in Main.cs to confirm there aren't additional assignments elsewhere (e.g., in a loop or other method). Also check WallLoader. Let me grep.

Also TORCH_COLORS compare:
- 0: [1,0.95,0.8] ✓
- 1: [0,0.1,1.3] ✓
- 2: [1,0.1,0.1] ✓
- 3: [0,1,0.1] ✓
- 4: [0.9,0,0.9] ✓
- 5: [1.4,1.4,1.4] ✓
- 6: [0.9,0.9,0] ✓
- 7: dynamic DemonTorchLight — repo [1,0.3,0.5] as fallback placeholder; note scanner uses flicker.demonTorchColor() for style 7. Need to check SkyColor's demonTorchColor formula vs DemonTorchLight.GetRGB.
- 8: [1,1.6,0.5] ✓
- 9: [0.75,0.85,1.4] ✓
- 10: [1,0.5,0] ✓
- 11: [1.4,1.4,0.7] ✓
- 12: [0.75,1.3499999,1.5] vs repo 1.35 → matches to 3 decimals ✓
- 13: [0.95,0.75,1.3] ✓
- 14: dynamic Disco — placeholder [1,1,1]
- 15: [1,0,1] ✓
- 16: [1.4,0.85,0.55] ✓
- 17: [0.25,1.3,0.8] ✓
- 18: [0.95,0.4,1.4] ✓
- 19: [1.4,0.7,0.5] ✓
- 20: [1.25,0.6,1.2] ✓
- 21: [0.75,1.45,0.9] ✓
- 22: [0.3,0.78,1.2] ✓
- 23: dynamic Shimmer — placeholder [1,1,1]

So 21 constant entries match exactly, 3 dynamic (7/14/23) handled via flicker. Need to check DemonTorchLight/DiscoTorchLight/ShimmerTorchLight implementations and compare with SkyColor.ts.

Note there's an important detail: torch tile 4 applies flicker addition `Next(28,42)*0.005 + (270-mouseTextColor)/700` in the repo — but vanilla case 4 (torch) does NOT add flicker! Let me check: vanilla case 4 at :1536-1541: `if (tile.frameX < 66) TorchID.TorchColor(tile.frameY/22,...)`. No flicker. The flicker for torches comes from where? Actually in vanilla, torches don't flicker in TileLightScanner... Hmm, wait. Actually the `localRandom.Next(28,42)*0.005 + (270-mouseTextColor)/700` appears in cases 405 (fireplace), 215 (campfire), 592. So the repo adding flicker to sheet 4 torches is a deviation! Let me double check: repo code — `if (sheet === 4) { ...; const f = this.localRandom(tx,ty).next(28,42)*0.005 + (270-osc)/700; er += f; ...}`. Yes, that adds flicker to torches which vanilla doesn't. That's a deviation (torch light too bright/flickering).

Hmm wait — but does vanilla add anything for torch? No. Also note the tile 4 gate: vanilla requires tile.frameX < 66. Torch frameX values: 0 (off?), 22, 44, 66, 88... Actually torch tile 4 has frameX 0 = unlit? Let me think: In Terraria, torch tile 4: frameX 0 = normal torch, 22 = off? Hmm. Actually there's a `lightIsOn` gate for torch in repo: `const on = sheet < 0 || lightIsOn(sheet, st.frameX[i], st.frameY[i]);` Need to check devices.lightIsOn. The vanilla gate frameX < 66 means frames 0,22,44 emit light (frameX 66+ = crystal/other variants?). Hmm, in 1.4, torch tile 4 styles: frameX = 0 for the torch, 22 for... Actually I recall: tile 4 Torch — frameX 0 = lit torch on ground; frameX 22 = torch off? Let me check TileObjectData or the wiring. Actually the relevant vanilla logic: `case 4: if (tile.frameX < 66) TorchID.TorchColor(...)`. FrameX values 0, 22, 44 are the three "on" sub-frames (torch styles A/B/C?) and 66, 88 are off frames? In Terraria tile 4, the sprite sheet has 4 columns: frameX 0 = regular torch lit, 22 = ? Hmm.

Let me check lightIsOn in devices.ts and the tile 4 def in tiles.ts.

Also need to check `Main.tileLighted[]` — which tiles are in tileLighted. The repo's TILE_DEFS light field presumably encodes those. I need to check tiles.ts thoroughly for all `light:` fields.

Big job: Section 1 — enumerate vanilla emissive tile cases from ApplyTileLight and compare with repo. The vanilla switch covers ~150 tile types. Repo has static light fields plus specialTileLight plus MUSHROOM/FLICKER groups. I need to list which vanilla cases are missing in repo.

Let me read tiles.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:15:28.697Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/data/tiles.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:15:28.909Z

**📎 ToolResult**

```
1	// 内部 tile / wall 注册表。id 即数组下标。
2	// 数值（硬度/光照）为原创平衡设计；mapColor 参考 TEdit tiles.json 的地图配色后重新取整。
3	
4	export interface TileDef {
5	  key: string;
6	  name: string;
7	  solid: boolean;        // 参与碰撞
8	  platform: boolean;     // 单向平台（下跳可穿）
9	  decor: boolean;        // 装饰物（不碰撞、可被任何工具秒清）
10	  framed: boolean;       // 多格框架物体（使用 frameX/frameY 定位贴图）
11	  opacity: number;       // 光照阻挡 0-1
12	  light?: [number, number, number]; // 自发光 RGB
13	  pick: number;          // 所需镐力（-1 不可挖）
14	  axe: number;           // 所需斧力
15	  mapColor: string;      // 小地图颜色
16	  drop?: string | number | null;   // 破坏掉落:数字=原版 item id(2026-08 本地物品退役后统一);
17	                                   // 字符串=place_v_ 派生等存量 key;null = 显式无掉落,原版装饰类
18	  rope?: boolean;        // 绳索类（攀爬判定）
19	  blend: boolean;        // 是否参与同类边缘融合
20	  attach?: 'ground' | 'wall'; // 装饰物附着需求
21	  w?: number; h?: number;     // framed 物体占格数
22	  vanilla?: {                 // 原版素材渲染（terraria-assets + TEdit 数据）
23	    sheet: number;            // Tiles_N 表 id
24	    frame: 'auto' | 'style' | 'blend'; // auto=47 表 8 向；style=显式帧；blend=BlendRules 合并分帧（泥土/石/草族）
25	    fw?: number; fh?: number; // style 类的占格数（TEdit frameSize）
26	  };
27	}
28	
29	export const T = {
30	  EMPTY: 0, DIRT: 1, STONE: 2, GRASS: 3,
31	  ORE_COPPER: 4, ORE_IRON: 5, ORE_SILVER: 6, ORE_GOLD: 7,
32	  TREE: 8, LEAVES: 9, WOOD: 10, PLATFORM: 11,
33	  TORCH: 12, WORKBENCH: 13, FURNACE: 14, ANVIL: 15,
34	  CHEST: 16, DOOR_CLOSED: 17, DOOR_OPEN: 18,
35	  MUSHROOM: 19, FLOWER: 20, TALLGRASS: 21, SAND: 22, SNOW: 23,
36	  SAPLING: 24, ASH: 25,
37	} as const;
38	
39	export const TILE_DEFS: TileDef[] = [];
40	function def(d: Partial<TileDef> & { key: string }): number {
41	  const id = TILE_DEFS.length;
42	  TILE_DEFS.push({
43	    name: d.key, solid: false, platform: false, decor: false, framed: false,
44	    opacity: 0, pick: -1, axe: -1, mapColor: '#000', blend: false, ...d, id,
45	  } as TileDef);
46	  return id;
47	}
48	// 保证 id 与 T 常量一致（按顺序注册）
49	def({ key: 'empty', name: '空气' });
50	def({ key: 'dirt', name: '泥土', solid: true, opacity: 1, pick: 0, mapColor: '#976B4B', blend: true, drop: 2, vanilla: { sheet: 0, frame: 'blend' } });
51	def({ key: 'stone', name: '石块', solid: true, opacity: 1, pick: 0, mapColor: '#808080', blend: true, drop: 3, vanilla: { sheet: 1, frame: 'blend' } });
52	def({ key: 'grass', name: '草块', solid: true, opacity: 1, pick: 0, mapColor: '#1CD85E', blend: true, drop: 2, vanilla: { sheet: 2, frame: 'blend' } });
53	def({ key: 'ore_copper', name: '铜矿', solid: true, opacity: 1, pick: 0, mapColor: '#964316', blend: false, drop: 12, vanilla: { sheet: 7, frame: 'auto' } });
54	def({ key: 'ore_iron', name: '铁矿', solid: true, opacity: 1, pick: 0, mapColor: '#8C6550', blend: false, drop: 11, vanilla: { sheet: 6, frame: 'auto' } });
55	def({ key: 'ore_silver', name: '银矿', solid: true, opacity: 1, pick: 20, mapColor: '#B9C2C3', blend: false, drop: 14, vanilla: { sheet: 9, frame: 'auto' } });
56	def({ key: 'ore_gold', name: '金矿', solid: true, opacity: 1, pick: 40, mapColor: '#B9A417', blend: false, drop: 13, vanilla: { sheet: 8, frame: 'auto' } });
57	def({ key: 'tree', name: '树干', solid: false, framed: true, opacity: 0.1, axe: 0, mapColor: '#976B4B', drop: 9, vanilla: { sheet: 5, frame: 'style', fw: 1, fh: 1 } });
58	def({ key: 'leaves', name: '树叶', decor: true, framed: true, opacity: 0.05, pick: 0, axe: 0, mapColor: '#2E8B3D', drop: null });
59	def({ key: 'wood', name: '木材块', solid: true, opacity: 1, pick: 0, mapColor: '#976B4B', blend: true, drop: 9, vanilla: { sheet: 30, frame: 'auto' } });
60	def({ key: 'platform', name: '木平台', platform: true, opacity: 0.15, pick: 0, axe: 0, mapColor: '#BF8E6F', drop: 94, vanilla: { sheet: 19, frame: 'style', fw: 1, fh: 1 } });
61	def({ key: 'torch', name: '火把', decor: true, framed: true, opacity: 0, pick: 0, light: [255, 225, 150], mapColor: '#FDDD03', drop: 8, vanilla: { sheet: 4, frame: 'style', fw: 1, fh: 1 } });
62	// 注：火把光值见下（更亮版本）
63	def({ key: 'workbench', name: '工作台', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 1, mapColor: '#BF8E6F', drop: 36, vanilla: { sheet: 18, frame: 'style', fw: 2, fh: 1 } });
64	def({ key: 'furnace', name: '熔炉', solid: false, /* 原版 tileSolid[17]=false：熔炉可通行 */ framed: true, opacity: 1, pick: 0, w: 3, h: 2, light: [255, 140, 70], mapColor: '#909490', drop: 33, vanilla: { sheet: 17, frame: 'style', fw: 3, fh: 2 } });
65	def({ key: 'anvil', name: '铁砧', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 1, mapColor: '#8C8274', drop: 35, vanilla: { sheet: 16, frame: 'style', fw: 2, fh: 1 } });
66	def({ key: 'chest', name: '宝箱', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#AE815C', drop: 48, vanilla: { sheet: 21, frame: 'style', fw: 2, fh: 2 } });
67	def({ key: 'door_closed', name: '门', solid: true, framed: true, opacity: 0.05, pick: 0, w: 1, h: 3, mapColor: '#77694F', drop: 25, vanilla: { sheet: 10, frame: 'style', fw: 1, fh: 3 } });
68	def({ key: 'door_open', name: '门(开)', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 3, mapColor: '#77694F', drop: 25, vanilla: { sheet: 11, frame: 'style', fw: 2, fh: 3 } });
69	def({ key: 'mushroom', name: '蘑菇', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#1AC454', drop: 5, vanilla: { sheet: 3, frame: 'style', fw: 1, fh: 1 } });
70	def({ key: 'flower', name: '花', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#1AC454', drop: null, vanilla: { sheet: 3, frame: 'style', fw: 1, fh: 1 } });
71	def({ key: 'tallgrass', name: '草丛', decor: true, framed: true, opacity: 0, pick: 0, axe: 0, mapColor: '#1AC454', drop: 27, vanilla: { sheet: 3, frame: 'style', fw: 1, fh: 1 } });
72	def({ key: 'sand', name: '沙块', solid: true, opacity: 1, pick: 0, mapColor: '#BAA854', blend: true, drop: 169, vanilla: { sheet: 53, frame: 'blend' } });
73	def({ key: 'snow', name: '雪块', solid: true, opacity: 1, pick: 0, mapColor: '#D3ECF1', blend: true, drop: 593, vanilla: { sheet: 147, frame: 'blend' } });
74	def({ key: 'acorn_sapling', name: '树苗', decor: true, framed: true, opacity: 0, pick: 0, axe: 0, mapColor: '#A37451', drop: 27, vanilla: { sheet: 20, frame: 'style', fw: 1, fh: 2 } }); // fh:2=原版 TileObjectData Width1/Height2+frameSize[1,2](2026-08-13 atlas-lint ATL-06 裁决;此前 fh:1 错)
75	def({ key: 'ash', name: '灰烬块', solid: true, opacity: 1, pick: 0, mapColor: '#44444C', blend: true, drop: 3, vanilla: { sheet: 57, frame: 'auto' } });
76	
77	// ===================== 原版素材图块（terraria-assets + TEdit 数据） =====================
78	// 4a：矿石 / 宝石 / 冰雪 / 沙漠 / 基础方块（1x1 实心，frame:'auto' 8 向贴合）
79	// mapColor/pick 取自 TEdit tiles.json；sheet = 原版 Tiles_N 表 id
80	
81	// ---- 矿石（含替代矿与困难模式矿，后者先只做美术） ----
82	def({ key: 'ore_tin', name: '锡矿', solid: true, opacity: 1, pick: 0, mapColor: '#817D5D', drop: 699, vanilla: { sheet: 166, frame: 'auto' } });
83	def({ key: 'ore_lead', name: '铅矿', solid: true, opacity: 1, pick: 0, mapColor: '#3E5272', drop: 700, vanilla: { sheet: 167, frame: 'auto' } });
84	def({ key: 'ore_tungsten', name: '钨矿', solid: true, opacity: 1, pick: 20, mapColor: '#849D7F', drop: 701, vanilla: { sheet: 168, frame: 'auto' } });
85	def({ key: 'ore_platinum', name: '铂金矿', solid: true, opacity: 1, pick: 40, mapColor: '#98ABC6', drop: 702, vanilla: { sheet: 169, frame: 'auto' } });
86	def({ key: 'ore_demonite', name: '魔矿', solid: true, opacity: 1, pick: 55, mapColor: '#625FA7', drop: 56, light: [255, 255, 153], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 22, frame: 'auto' } });
87	def({ key: 'ore_meteorite', name: '陨石', solid: true, opacity: 1, pick: 50, mapColor: '#685654', drop: 116, light: [143, 110, 38], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 37, frame: 'auto' } });
88	def({ key: 'ore_hellstone', name: '狱石', solid: true, opacity: 1, pick: 65, mapColor: '#8E4242', drop: 174, light: [255, 90, 40], vanilla: { sheet: 58, frame: 'auto' } });
89	def({ key: 'ore_crimtane', name: '猩红矿', solid: true, opacity: 1, pick: 55, mapColor: '#7D3741', drop: 880, light: [89, 0, 0], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 204, frame: 'auto' } });
90	def({ key: 'ore_cobalt', name: '钴矿', solid: true, opacity: 1, pick: 100, mapColor: '#0B508F', drop: 364, vanilla: { sheet: 107, frame: 'auto' } });
91	def({ key: 'ore_mythril', name: '秘银矿', solid: true, opacity: 1, pick: 110, mapColor: '#5BA9A9', drop: 365, vanilla: { sheet: 108, frame: 'auto' } });
92	def({ key: 'ore_adamantite', name: '精金矿', solid: true, opacity: 1, pick: 150, mapColor: '#801A34', drop: 366, vanilla: { sheet: 111, frame: 'auto' } });
93	def({ key: 'ore_palladium', name: '钯金矿', solid: true, opacity: 1, pick: 100, mapColor: '#EF5A32', drop: 1104, vanilla: { sheet: 221, frame: 'auto' } });
94	def({ key: 'ore_orichalcum', name: '山铜矿', solid: true, opacity: 1, pick: 110, mapColor: '#E760E4', drop: 1105, vanilla: { sheet: 222, frame: 'auto' } });
95	def({ key: 'ore_titanium', name: '钛矿', solid: true, opacity: 1, pick: 150, mapColor: '#395565', drop: 1106, vanilla: { sheet: 223, frame: 'auto' } });
96	def({ key: 'ore_chlorophyte', name: '叶绿矿', solid: true, opacity: 1, pick: 65, mapColor: '#BFE973', drop: 947, vanilla: { sheet: 211, frame: 'auto' } });
97	
98	// ---- 宝石矿（掉对应宝石） ----
99	def({ key: 'gem_sapphire', name: '蓝宝石矿', solid: true, opacity: 1, pick: 30, mapColor: '#6E8CB6', drop: 177, vanilla: { sheet: 63, frame: 'auto' } });
100	def({ key: 'gem_ruby', name: '红宝石矿', solid: true, opacity: 1, pick: 30, mapColor: '#C46072', drop: 178, vanilla: { sheet: 64, frame: 'auto' } });
101	def({ key: 'gem_emerald', name: '翡翠矿', solid: true, opacity: 1, pick: 30, mapColor: '#389661', drop: 179, vanilla: { sheet: 65, frame: 'auto' } });
102	def({ key: 'gem_topaz', name: '黄玉矿', solid: true, opacity: 1, pick: 30, mapColor: '#A0763A', drop: 180, vanilla: { sheet: 66, frame: 'auto' } });
103	def({ key: 'gem_amethyst', name: '紫水晶矿', solid: true, opacity: 1, pick: 30, mapColor: '#8C3AA6', drop: 181, vanilla: { sheet: 67, frame: 'auto' } });
104	def({ key: 'gem_diamond', name: '钻石矿', solid: true, opacity: 1, pick: 30, mapColor: '#7DBFC5', drop: 182, vanilla: { sheet: 68, frame: 'auto' } });
105	
106	// ---- 冰雪 ----
107	def({ key: 'ice', name: '冰块', solid: true, opacity: 1, pick: 0, mapColor: '#90C3E8', blend: true, drop: 664, vanilla: { sheet: 161, frame: 'auto' } });
108	def({ key: 'thin_ice', name: '薄冰', solid: true, opacity: 1, pick: 0, mapColor: '#B8DBF0', blend: true, drop: 664, vanilla: { sheet: 162, frame: 'auto' } });
109	def({ key: 'ice_brick', name: '冰砖', solid: true, opacity: 1, pick: 0, mapColor: '#7CAFC9', blend: true, drop: 883, vanilla: { sheet: 206, frame: 'auto' } });
110	def({ key: 'snow_brick', name: '雪砖', solid: true, opacity: 1, pick: 0, mapColor: '#D3ECF1', blend: true, drop: 594, vanilla: { sheet: 148, frame: 'auto' } });
111	
112	// ---- 沙漠 / 基础方块 ----
113	def({ key: 'sandstone', name: '沙岩', solid: true, opacity: 1, pick: 0, mapColor: '#C67C4E', blend: true, drop: 3271, vanilla: { sheet: 396, frame: 'auto' } });
114	def({ key: 'hardened_sand', name: '硬化沙块', solid: true, opacity: 1, pick: 0, mapColor: '#D4C064', blend: true, drop: 3272, vanilla: { sheet: 397, frame: 'auto' } });
115	def({ key: 'desert_fossil', name: '沙漠化石', solid: true, opacity: 1, pick: 0, mapColor: '#D49458', blend: true, drop: 3347, vanilla: { sheet: 404, frame: 'auto' } });
116	def({ key: 'clay', name: '粘土块', solid: true, opacity: 1, pick: 0, mapColor: '#925144', blend: true, drop: 133, vanilla: { sheet: 40, frame: 'auto' } });
117	def({ key: 'glass', name: '玻璃', solid: true, opacity: 0.15, pick: 0, mapColor: '#C8F6FE', drop: 170, vanilla: { sheet: 54, frame: 'auto' } });
118	def({ key: 'obsidian', name: '黑曜石', solid: true, opacity: 1, pick: 55, mapColor: '#2B2854', blend: true, drop: 173, vanilla: { sheet: 56, frame: 'auto' } });
119	def({ key: 'gray_brick', name: '灰砖', solid: true, opacity: 1, pick: 0, mapColor: '#808080', blend: true, drop: 129, vanilla: { sheet: 38, frame: 'auto' } });
120	def({ key: 'red_brick', name: '红砖', solid: true, opacity: 1, pick: 0, mapColor: '#B53E3B', blend: true, drop: 131, vanilla: { sheet: 39, frame: 'auto' } });
121	def({ key: 'mud', name: '泥块', solid: true, opacity: 1, pick: 0, mapColor: '#5C4449', blend: true, drop: 176, vanilla: { sheet: 59, frame: 'blend' } });
122	def({ key: 'silt', name: '淤泥块', solid: true, opacity: 1, pick: 0, mapColor: '#6A6B76', blend: true, drop: 424, vanilla: { sheet: 123, frame: 'auto' } });
123	
124	// 4b：家具 / 装饰（多格 framed，frame:'style' 显式 18px 帧；w/h = TEdit frameSize）
125	const VAN = (sheet: number, w: number, h: number) => ({ vanilla: { sheet, frame: 'style' as const, fw: w, fh: h } });
126	
127	def({ key: 'table', name: '木桌', framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: 32, ...VAN(14, 3, 2) });
128	def({ key: 'chair', name: '木椅', framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#BF8E6F', drop: 34, ...VAN(15, 1, 2) });
129	def({ key: 'bed', name: '床', framed: true, opacity: 0.05, pick: 0, w: 4, h: 2, mapColor: '#BF8E6F', drop: 224, ...VAN(79, 4, 2) });
130	def({ key: 'bookcase', name: '书架', framed: true, opacity: 0.05, pick: 0, w: 3, h: 4, mapColor: '#BF8E6F', drop: 354, ...VAN(101, 3, 4) });
131	def({ key: 'grandfather_clock', name: '落地钟', framed: true, opacity: 0.05, pick: 0, w: 2, h: 5, mapColor: '#BF8E6F', drop: 359, ...VAN(104, 2, 5) });
132	def({ key: 'piano', name: '钢琴', framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: 333, ...VAN(87, 3, 2) });
133	def({ key: 'dresser', name: '梳妆台', framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: 334, ...VAN(88, 3, 2) });
134	def({ key: 'bench', name: '长凳', framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: 335, ...VAN(89, 3, 2) });
135	def({ key: 'bathtub', name: '浴缸', framed: true, opacity: 0.05, pick: 0, w: 4, h: 2, mapColor: '#909490', drop: 336, ...VAN(90, 4, 2) });
136	def({ key: 'keg', name: '酒桶', framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#BF8E6F', drop: 352, ...VAN(94, 2, 2) });
137	def({ key: 'cooking_pot', name: '汤锅', framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#909490', drop: 345, ...VAN(96, 2, 2) });
138	def({ key: 'clay_pot', name: '陶盆', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#796E61', drop: 222, ...VAN(78, 1, 1) });
139	def({ key: 'tombstone_v', name: '墓碑', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#C0C0C0', drop: 321, ...VAN(85, 2, 2) });
140	def({ key: 'crystal_heart', name: '水晶之心', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#AE1845', drop: 29, light: [255, 60, 90], ...VAN(12, 2, 2) });
141	// 发光灯具
142	def({ key: 'candle', name: '蜡烛', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#FDDD03', drop: 105, light: [255, 185, 110], ...VAN(33, 1, 1) });
143	def({ key: 'chandelier', name: '吊灯', decor: true, framed: true, opacity: 0, pick: 0, w: 3, h: 3, mapColor: '#EBA687', drop: 106, light: [255, 190, 120], ...VAN(34, 3, 3) });
144	def({ key: 'lantern', name: '吊挂灯笼', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 2, mapColor: '#FBEB7F', drop: 136, ...VAN(42, 1, 2) });
145	// 灯笼发光 = TileLightScanner specialTileLight case 42(样式色表+灭档门控),不走 def.light 静态色
146	def({ key: 'candelabra', name: '烛台', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#FDDD03', drop: 349, light: [255, 185, 110], ...VAN(100, 2, 2) });
147	def({ key: 'chinese_lantern', name: '中式灯笼', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#FFA21F', drop: 344, light: [255, 160, 70], ...VAN(95, 2, 2) });
148	def({ key: 'skull_lantern', name: '骷髅灯笼', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#FDDD03', drop: 347, light: [255, 160, 70], ...VAN(98, 2, 2) });
149	def({ key: 'water_candle', name: '水蜡烛', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#2B8FFF', drop: 148, light: [140, 180, 255], ...VAN(49, 1, 1) });
150	// 瓦罐（世界生成散布）：打破掉随机常用道具（breakTile 特判），不做放置物
151	def({ key: 'pot', name: '瓦罐', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#974F50', drop: null, vanilla: { sheet: 28, frame: 'style', fw: 2, fh: 2 } });
152	// ---- 玩家储物族（原版 Player.cs:32598 右键绑定：29→bank / 97→bank2 / 463→bank3 / 491→bank4）----
153	// drop 不写 → 破坏走 place_v_ 回退回收（储物内容在玩家 bank 数据里，不随方块掉落——原版同语义）
154	def({ key: 'v_29_piggy_bank', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 1, mapColor: '#AF6980', vanilla: { sheet: 29, frame: 'style', fw: 2, fh: 1 } }); // 存钱罐（compat-report 补全：导入曾清空丢弃）
155	def({ key: 'v_463_defenders_forge', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 4, mapColor: '#9BD6F0', light: [51, 102, 204], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 463, frame: 'style', fw: 3, fh: 4 } }); // 守护者熔炉（bank3）
156	
157	export const TILE_BY_KEY: Record<string, number> = {};
158	// 注意：构建必须放在文件末尾（所有 def() 之后），v_ 批量补全定义在下方，
159	// 此处先注册占位，末尾 rebuildTILE_BY_KEY() 统一回填
160	export function isSolidTile(type: number): boolean {
161	  const d = TILE_DEFS[type];
162	  return !!d && d.solid;
163	}
164	
165	// ---- 墙（id 直用原版 wld 墙 id：0 空 / 1 石墙 / 2 土墙(天然) / 3 黑檀石 / 4 木墙 …）----
166	export interface WallDef { id: number; key: string; name: string; mapColor: string; opacity: number; largeFrame?: 0 | 1 | 2; }
167	export const W = { NONE: 0, STONE: 1, DIRT: 2, WOOD: 4 } as const;
168	export const WALL_DEFS: WallDef[] = [];
169	export function wallDef(d: WallDef) { WALL_DEFS[d.id] = d; }
170	export const WALL_BY_KEY: Record<string, number> = {};
171	
172	// ===================== wld 导入全量补全（compat-report 驱动） =====================
173	// 实心 1x1 方块（frame:auto 8 向贴合）
174	def({ key: 'v_51_cobweb', name: '', solid: false, /* 原版非实心：蛛网减速不阻挡 */ opacity: 1, pick: 0, mapColor: '#C0CACB', blend: true, drop: null, vanilla: { sheet: 51, frame: 'auto' } });
175	def({ key: 'v_368_granite_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#322E68', blend: true, drop: null, vanilla: { sheet: 368, frame: 'auto' } });
176	def({ key: 'v_226_lihzahrd_brick', name: '', solid: true, opacity: 1, pick: 210, mapColor: '#8D3800', blend: true, drop: null, vanilla: { sheet: 226, frame: 'auto' } });
177	def({ key: 'v_367_marble_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#A8B2CC', blend: true, drop: null, vanilla: { sheet: 367, frame: 'auto' } });
178	def({ key: 'v_633_ash_grass_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#D28C64', blend: true, drop: null, light: [83, 38, 13], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 633, frame: 'auto' } });
179	def({ key: 'v_181_red_moss_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#863B31', blend: true, drop: null, vanilla: { sheet: 181, frame: 'auto' } });
180	def({ key: 'v_189_cloud_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#DFFFFF', blend: true, drop: null, vanilla: { sheet: 189, frame: 'auto' } });
181	def({ key: 'v_183_purple_moss_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#793186', blend: true, drop: null, vanilla: { sheet: 183, frame: 'auto' } });
182	def({ key: 'v_536_xenon_moss_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#00C5D0', blend: true, drop: null, light: [0, 41, 87], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 536, frame: 'auto' } });
183	def({ key: 'v_225_hive_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#E37D16', blend: true, drop: null, vanilla: { sheet: 225, frame: 'auto' } });
184	def({ key: 'v_483_cracked_pink_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#6B4463', blend: true, drop: null, vanilla: { sheet: 483, frame: 'auto' } });
185	def({ key: 'v_224_slush_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#6B848B', blend: true, drop: null, vanilla: { sheet: 224, frame: 'auto' } });
186	def({ key: 'v_383_living_mahogany_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#DD8890', blend: true, drop: null, vanilla: { sheet: 383, frame: 'auto' } });
187	def({ key: 'v_179_green_moss_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#318672', blend: true, drop: null, vanilla: { sheet: 179, frame: 'auto' } });
188	def({ key: 'v_384_living_mahogany_leaves_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#83CE0C', blend: true, drop: null, vanilla: { sheet: 384, frame: 'auto' } });
189	def({ key: 'v_273_stone_slab', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#808080', blend: true, drop: null, vanilla: { sheet: 273, frame: 'auto' } });
190	def({ key: 'v_381_lava_moss', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#FE7902', blend: true, drop: null, light: [255, 120, 30], vanilla: { sheet: 381, frame: 'auto' } });
191	def({ key: 'v_48_spike', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#808080', blend: true, drop: null, vanilla: { sheet: 48, frame: 'auto' } });
192	def({ key: 'v_192_living_leaf_block', name: '', solid: false, opacity: 1, pick: 0, mapColor: '#1AC454', blend: true, drop: null, vanilla: { sheet: 192, frame: 'auto' } });
193	// ↑ solid:Main.cs:10167 初值 true,但 LivingTrees pass 收尾 `Main.tileSolid[192] = false`
194	//   （WorldGen.cs:15789）——树叶块全程可穿行。生成+碰撞均按 false。
195	def({ key: 'v_191_living_wood_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#976B4B', blend: true, drop: null, vanilla: { sheet: 191, frame: 'auto' } });
196	def({ key: 'v_196_rain_cloud_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#9390B2', blend: true, drop: null, vanilla: { sheet: 196, frame: 'auto' } });
197	def({ key: 'v_118_pearlstone_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#EEE1DA', blend: true, drop: null, vanilla: { sheet: 118, frame: 'auto' } });
198	def({ key: 'v_321_boreal_wood', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#604D40', blend: true, drop: null, vanilla: { sheet: 321, frame: 'auto' } });
199	def({ key: 'v_152_ebonstone_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#8085B8', blend: true, drop: null, vanilla: { sheet: 152, frame: 'auto' } });
200	def({ key: 'v_158_rich_mahogany', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#915155', blend: true, drop: null, vanilla: { sheet: 158, frame: 'auto' } });
201	def({ key: 'v_357_smooth_marble_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#A8B2CC', blend: true, drop: null, vanilla: { sheet: 357, frame: 'auto' } });
202	def({ key: 'v_272_cog_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#797765', blend: true, drop: null, vanilla: { sheet: 272, frame: 'auto' } });
203	def({ key: 'v_229_honey_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#FF9C0C', blend: true, drop: null, vanilla: { sheet: 229, frame: 'auto' } });
204	def({ key: 'v_311_dynasty_wood', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#753D19', blend: true, drop: null, vanilla: { sheet: 311, frame: 'auto' } });
205	def({ key: 'v_130_active_stone_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#808080', blend: true, drop: null, vanilla: { sheet: 130, frame: 'auto' } });
206	def({ key: 'v_193_slime_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#3879FF', blend: true, drop: null, vanilla: { sheet: 193, frame: 'auto' } });
207	def({ key: 'v_190_glowing_mushroom_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#B6AF82', blend: true, drop: null, light: [0, 51, 255], /* 原版 tileLighted 发光色（TileLightScanner.cs:2938 蘑菇组 R=0 G=0.2+ B=1） */ vanilla: { sheet: 190, frame: 'auto' } });
208	def({ key: 'v_350_martian_conduit_plating', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#37619B', blend: true, drop: null, light: [26, 26, 26], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 350, frame: 'auto' } });
209	def({ key: 'v_369_smooth_granite_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#322E68', blend: true, drop: null, vanilla: { sheet: 369, frame: 'auto' } });
210	def({ key: 'v_137_traps', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 1, h: 1, mapColor: '#909490', drop: null, vanilla: { sheet: 137, frame: 'style', fw: 1, fh: 1 } });
211	def({ key: 'v_117_pearlstone_block', name: '', solid: true, opacity: 1, pick: 65, mapColor: '#B5ACBE', blend: true, drop: null, vanilla: { sheet: 117, frame: 'blend' } });
212	def({ key: 'v_112_ebonsand_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#67627A', blend: true, drop: null, vanilla: { sheet: 112, frame: 'auto' } });
213	def({ key: 'v_232_wooden_spike', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#915155', blend: true, drop: null, vanilla: { sheet: 232, frame: 'auto' } });
214	def({ key: 'v_274_sandstone_slab', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#BEAB5E', blend: true, drop: null, vanilla: { sheet: 274, frame: 'auto' } });
215	def({ key: 'v_322_palm_wood', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#C6AA68', blend: true, drop: null, vanilla: { sheet: 322, frame: 'auto' } });
216	def({ key: 'v_109_hallowed_grass_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#4EC1E3', blend: true, drop: null, vanilla: { sheet: 109, frame: 'auto' } });
217	def({ key: 'v_312_red_dynasty_shingles', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#CC5D49', blend: true, drop: null, vanilla: { sheet: 312, frame: 'auto' } });
218	def({ key: 'v_422_conveyor_belt_ccw', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#414B5A', blend: true, drop: null, vanilla: { sheet: 422, frame: 'auto' } });
219	def({ key: 'v_495_shell_pile_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#FDE3D7', blend: true, drop: null, vanilla: { sheet: 495, frame: 'auto' } });
220	def({ key: 'v_479_smooth_sandstone_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#B27244', blend: true, drop: null, vanilla: { sheet: 479, frame: 'auto' } });
221	def({ key: 'v_353_vine_rope', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#1CD85E', blend: true, drop: null, rope: true, vanilla: { sheet: 353, frame: 'auto' } });
222	def({ key: 'v_477_mowed_grass_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#1CD85E', blend: true, drop: null, vanilla: { sheet: 477, frame: 'auto' } });
223	def({ key: 'v_380_planter_boxes', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#BF8E6F', blend: true, drop: null, vanilla: { sheet: 380, frame: 'auto' } });
224	def({ key: 'v_230_crispy_honey_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#834F0D', blend: true, drop: null, vanilla: { sheet: 230, frame: 'auto' } });
225	def({ key: 'v_562_bamboo_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#A5A81A', blend: true, drop: null, vanilla: { sheet: 562, frame: 'auto' } });
226	def({ key: 'v_371_pink_slime_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#F965BD', blend: true, drop: null, vanilla: { sheet: 371, frame: 'auto' } });
227	def({ key: 'v_668_the_dirtiest_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#976B4B', blend: true, drop: null, vanilla: { sheet: 668, frame: 'auto' } });
228	def({ key: 'v_398_corrupt_hardened_sand_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#64527E', blend: true, drop: null, vanilla: { sheet: 398, frame: 'auto' } });
229	def({ key: 'v_379_bubble', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#FBD1F0', blend: true, drop: null, vanilla: { sheet: 379, frame: 'auto' } });
230	def({ key: 'v_618_stone_accent_slab', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#808080', blend: true, drop: null, vanilla: { sheet: 618, frame: 'auto' } });
231	
232	// framed 物体（frame:style 显式 18px 帧）
233	def({ key: 'v_165_cave_decos', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#73ADE5', drop: null, vanilla: { sheet: 165, frame: 'style', fw: 1, fh: 2 } });
234	def({ key: 'v_184_moss_plants', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#1D6A58', drop: null, light: [77, 0, 89], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 184, frame: 'style', fw: 1, fh: 1 } });
235	def({ key: 'v_314_minecart_track', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#B5A47D', drop: null, vanilla: { sheet: 314, frame: 'style', fw: 1, fh: 1 } });
236	def({ key: 'v_185_small_decos', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#636363', drop: null, vanilla: { sheet: 185, frame: 'style', fw: 1, fh: 1 } });
237	def({ key: 'v_373_water_drip', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#093DBF', drop: null, vanilla: { sheet: 373, frame: 'style', fw: 1, fh: 1 } });
238	def({ key: 'v_187_decos_3x2_group_2', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#636363', drop: null, vanilla: { sheet: 187, frame: 'style', fw: 3, fh: 2 } });
239	def({ key: 'v_484_rolling_cactus', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 2, h: 2, mapColor: '#497811', drop: null, vanilla: { sheet: 484, frame: 'style', fw: 2, fh: 2 } });
240	def({ key: 'v_374_lava_drip', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#FD2003', drop: null, vanilla: { sheet: 374, frame: 'style', fw: 1, fh: 1 } });
241	def({ key: 'v_233_jungle_large_plants', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#6BB61D', drop: null, vanilla: { sheet: 233, frame: 'style', fw: 3, fh: 2 } });
242	def({ key: 'v_105_statue', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#909490', drop: null, vanilla: { sheet: 105, frame: 'style', fw: 2, fh: 3 } });
243	def({ key: 'v_186_decos_3x2', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#636363', drop: null, vanilla: { sheet: 186, frame: 'style', fw: 3, fh: 2 } });
244	def({ key: 'v_461_sand_drip', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#D4C064', drop: null, vanilla: { sheet: 461, frame: 'style', fw: 1, fh: 1 } });
245	def({ key: 'v_178_gems', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#D05EC9', drop: null, vanilla: { sheet: 178, frame: 'style', fw: 1, fh: 1 } });
246	def({ key: 'v_485_antlion_larva', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#C68658', drop: null, vanilla: { sheet: 485, frame: 'style', fw: 2, fh: 2 } });
247	def({ key: 'v_637_ash_short_plants', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#C8784B', drop: null, light: [83, 38, 13], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 637, frame: 'style', fw: 1, fh: 1 } });
248	def({ key: 'v_444_bee_hive', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#bfb07c', drop: null, vanilla: { sheet: 444, frame: 'style', fw: 2, fh: 2 } });
249	def({ key: 'v_240_wall_hangings_3x3', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#78553C', drop: null, vanilla: { sheet: 240, frame: 'style', fw: 3, fh: 3 } });
250	def({ key: 'v_519_cattails', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#1CD86D', drop: null, light: [26, 51, 179], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 519, frame: 'style', fw: 1, fh: 1 } });
251	def({ key: 'v_138_boulder', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 2, h: 2, mapColor: '#808080', drop: null, vanilla: { sheet: 138, frame: 'style', fw: 2, fh: 2 } });
252	def({ key: 'v_634_ash_tree', name: '', solid: false, framed: true, opacity: 0.05, pick: -1, axe: 0, w: 1, h: 1, mapColor: '#917878', drop: null, light: [166, 77, 26], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 634, frame: 'style', fw: 1, fh: 1 } });
253	def({ key: 'v_26_altars', name: '', solid: false, framed: true, opacity: 0.05, pick: -1,  // 原版祭坛镐不可破坏(仅锤≥80+hardMode,Player.cs:45058)
254	  w: 3, h: 2, mapColor: '#77657D', drop: null, light: [79, 26, 112], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 26, frame: 'style', fw: 3, fh: 2 } });
255	def({ key: 'v_82_herbs_sprout', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#F6C51A', drop: null, vanilla: { sheet: 82, frame: 'style', fw: 1, fh: 1 } });
256	def({ key: 'v_323_palm_trees', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#B68D56', drop: null, vanilla: { sheet: 323, frame: 'style', fw: 1, fh: 1 } });
257	def({ key: 'v_135_pressure_plates', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#FD7272', drop: null, vanilla: { sheet: 135, frame: 'style', fw: 1, fh: 1 } });
258	def({ key: 'v_91_banners', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 3, mapColor: '#0D5882', drop: null, vanilla: { sheet: 91, frame: 'style', fw: 1, fh: 3 } });
259	def({ key: 'v_242_paintings_6x4', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 4, mapColor: '#63321E', drop: null, vanilla: { sheet: 242, frame: 'style', fw: 6, fh: 4 } });
260	def({ key: 'v_50_books', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#AA3072', drop: null, vanilla: { sheet: 50, frame: 'style', fw: 1, fh: 1 } });
261	def({ key: 'v_93_lamps', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 6, mapColor: '#FDDD03', drop: null, light: [255, 185, 110], vanilla: { sheet: 93, frame: 'style', fw: 1, fh: 3 } });
262	def({ key: 'v_549_seaweed', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#365314', drop: null, vanilla: { sheet: 549, frame: 'style', fw: 1, fh: 1 } });
263	def({ key: 'v_254_pumpkin_plant', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#F89E5C', drop: null, vanilla: { sheet: 254, frame: 'style', fw: 2, fh: 2 } });
264	def({ key: 'v_571_bamboo', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#A5A81A', drop: null, vanilla: { sheet: 571, frame: 'style', fw: 1, fh: 1 } });
265	def({ key: 'v_246_paintings_3x2', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#63321E', drop: null, vanilla: { sheet: 246, frame: 'style', fw: 3, fh: 2 } });
266	def({ key: 'v_245_paintings_2x3', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#63321E', drop: null, vanilla: { sheet: 245, frame: 'style', fw: 2, fh: 3 } });
267	def({ key: 'v_586_emerald_tree', name: '', solid: false, framed: true, opacity: 0.05, pick: -1, axe: 0, w: 1, h: 1, mapColor: '#7F7F7F', drop: null, vanilla: { sheet: 586, frame: 'style', fw: 1, fh: 1 } });
268	def({ key: 'v_596_vanity_tree_sakura', name: '', solid: false, framed: true, opacity: 0.05, pick: -1, axe: 0, w: 1, h: 1, mapColor: '#976B4B', drop: null, vanilla: { sheet: 596, frame: 'style', fw: 1, fh: 1 } });
269	def({ key: 'v_467_chests_group_2', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#813879', drop: null, vanilla: { sheet: 467, frame: 'style', fw: 2, fh: 2 } });
270	def({ key: 'v_443_geyser', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 1, mapColor: '#909490', drop: null, vanilla: { sheet: 443, frame: 'style', fw: 2, fh: 1 } });
271	def({ key: 'v_589_amber_tree', name: '', solid: false, framed: true, opacity: 0.05, pick: -1, axe: 0, w: 1, h: 1, mapColor: '#7F7F7F', drop: null, vanilla: { sheet: 589, frame: 'style', fw: 1, fh: 1 } });
272	def({ key: 'v_411_detonator', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#E32E2E', drop: null, vanilla: { sheet: 411, frame: 'style', fw: 2, fh: 2 } });
273	def({ key: 'v_518_lily_pads', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#1AC454', drop: null, vanilla: { sheet: 518, frame: 'style', fw: 1, fh: 1 } });
274	def({ key: 'v_588_diamond_tree', name: '', solid: false, framed: true, opacity: 0.05, pick: -1, axe: 0, w: 1, h: 1, mapColor: '#7F7F7F', drop: null, vanilla: { sheet: 588, frame: 'style', fw: 1, fh: 1 } });
275	def({ key: 'v_585_sapphire_tree', name: '', solid: false, framed: true, opacity: 0.05, pick: -1, axe: 0, w: 1, h: 1, mapColor: '#7F7F7F', drop: null, vanilla: { sheet: 585, frame: 'style', fw: 1, fh: 1 } });
276	def({ key: 'v_583_topaz_tree', name: '', solid: false, framed: true, opacity: 0.05, pick: -1, axe: 0, w: 1, h: 1, mapColor: '#7F7F7F', drop: null, vanilla: { sheet: 583, frame: 'style', fw: 1, fh: 1 } });
277	def({ key: 'v_13_placed_bottles', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#85D5F7', drop: null, vanilla: { sheet: 13, frame: 'style', fw: 1, fh: 1 } });
278	def({ key: 'v_530_oasis_plants', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#6BB600', drop: null, vanilla: { sheet: 530, frame: 'style', fw: 3, fh: 2 } });
279	def({ key: 'v_616_vanity_tree_yellow_willow', name: '', solid: false, framed: true, opacity: 0.05, pick: -1, axe: 0, w: 1, h: 1, mapColor: '#976B4B', drop: null, vanilla: { sheet: 616, frame: 'style', fw: 1, fh: 1 } });
280	def({ key: 'v_215_campfires', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#FE7902', drop: null, light: [255, 185, 110], vanilla: { sheet: 215, frame: 'style', fw: 3, fh: 2 } });
281	def({ key: 'v_141_explosives', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#C03B3B', drop: null, vanilla: { sheet: 141, frame: 'style', fw: 1, fh: 1 } });
282	def({ key: 'v_597_pylons', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 4, mapColor: '#1CD85E', drop: null, light: [13, 204, 77], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 597, frame: 'style', fw: 3, fh: 4 } });
283	def({ key: 'v_592_hanging_brazier', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#FE7902', drop: null, light: [255, 185, 110], vanilla: { sheet: 592, frame: 'style', fw: 2, fh: 3 } });
284	def({ key: 'v_375_honey_drip', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#FF9C0C', drop: null, vanilla: { sheet: 375, frame: 'style', fw: 1, fh: 1 } });
285	def({ key: 'v_227_dye_plants', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#4AC59B', drop: null, vanilla: { sheet: 227, frame: 'style', fw: 1, fh: 1 } });
286	def({ key: 'v_584_amethyst_tree', name: '', solid: false, framed: true, opacity: 0.05, pick: -1, axe: 0, w: 1, h: 1, mapColor: '#7F7F7F', drop: null, vanilla: { sheet: 584, frame: 'style', fw: 1, fh: 1 } });
287	def({ key: 'v_231_larva', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#E0C265', drop: null, vanilla: { sheet: 231, frame: 'style', fw: 3, fh: 3 } });
288	def({ key: 'v_395_item_frame', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#BF8E6F', vanilla: { sheet: 395, frame: 'style', fw: 2, fh: 2 } });
289	def({ key: 'v_241_catacombs', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 4, h: 3, mapColor: '#4D4A48', drop: null, vanilla: { sheet: 241, frame: 'style', fw: 4, fh: 3 } });
290	def({ key: 'v_587_ruby_tree', name: '', solid: false, framed: true, opacity: 0.05, pick: -1, axe: 0, w: 1, h: 1, mapColor: '#7F7F7F', drop: null, vanilla: { sheet: 587, frame: 'style', fw: 1, fh: 1 } });
291	def({ key: 'v_86_loom', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: null, vanilla: { sheet: 86, frame: 'style', fw: 3, fh: 2 } });
292	def({ key: 'v_376_fishing_crates', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#A0785C', drop: null, vanilla: { sheet: 376, frame: 'style', fw: 2, fh: 2 } });
293	def({ key: 'v_470_mannequins', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#BF8E6F', vanilla: { sheet: 470, frame: 'style', fw: 2, fh: 3 } });
294	def({ key: 'v_324_seashells', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#E4D5AD', drop: null, vanilla: { sheet: 324, frame: 'style', fw: 1, fh: 1 } });
295	def({ key: 'v_81_coral', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#F585BF', drop: null, vanilla: { sheet: 81, frame: 'style', fw: 1, fh: 1 } });
296	def({ key: 'v_136_switch', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#D5CBCC', drop: null, vanilla: { sheet: 136, frame: 'style', fw: 1, fh: 1 } });
297	def({ key: 'v_355_alchemy_table', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#8D6B59', drop: null, vanilla: { sheet: 355, frame: 'style', fw: 3, fh: 3 } });
298	def({ key: 'v_354_bewitching_table', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#8D6B59', drop: null, light: [166, 89, 38], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 354, frame: 'style', fw: 3, fh: 3 } });
299	def({ key: 'v_103_bowls', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 1, mapColor: '#8D624D', drop: null, vanilla: { sheet: 103, frame: 'style', fw: 2, fh: 1 } });
300	def({ key: 'v_529_sea_oats', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#639608', drop: null, vanilla: { sheet: 529, frame: 'style', fw: 1, fh: 2 } });
301	def({ key: 'v_506_bast_statue', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#3D3D3D', drop: null, vanilla: { sheet: 506, frame: 'style', fw: 2, fh: 3 } });
302	def({ key: 'v_349_mushroom_statue', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#909490', drop: null, light: [0, 51, 255], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 349, frame: 'style', fw: 2, fh: 3 } });
303	def({ key: 'v_377_sharpening_station', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: null, vanilla: { sheet: 377, frame: 'style', fw: 3, fh: 2 } });
304	def({ key: 'v_613_potted_lava_plants', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 5, mapColor: '#FA6432', drop: null, light: [179, 77, 51], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 613, frame: 'style', fw: 3, fh: 5 } });
305	def({ key: 'v_219_extractinator', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null, vanilla: { sheet: 219, frame: 'style', fw: 3, fh: 3 } });
306	def({ key: 'v_388_tall_gate_closed', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 1, h: 5, mapColor: '#7F5C45', drop: null, vanilla: { sheet: 388, frame: 'style', fw: 1, fh: 5 } });
307	def({ key: 'v_389_tall_gate_open', name: '', solid: false, framed: true, opacity: 1, pick: 0, w: 1, h: 5, mapColor: '#7F5C45', drop: null, vanilla: { sheet: 389, frame: 'style', fw: 1, fh: 5 } }); // 高门开启态：原版 389 未设 tileSolid → 可通行
308	def({ key: 'v_129_crystal_shard', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#FF75E0', drop: null, light: [0, 13, 64], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 129, frame: 'style', fw: 1, fh: 1 } });
309	def({ key: 'v_466_elder_cystal_stand', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 5, h: 4, mapColor: '#CD9949', drop: null, vanilla: { sheet: 466, frame: 'style', fw: 5, fh: 4 } });
310	def({ key: 'v_220_solidifier', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null, vanilla: { sheet: 220, frame: 'style', fw: 3, fh: 3 } });
311	def({ key: 'v_303_lihzahrd_furnace', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null, vanilla: { sheet: 303, frame: 'style', fw: 3, fh: 3 } });
312	def({ key: 'v_469_tables_group_2', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: null, vanilla: { sheet: 469, frame: 'style', fw: 3, fh: 2 } });
313	def({ key: 'v_304_living_loom', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null, vanilla: { sheet: 304, frame: 'style', fw: 3, fh: 3 } });
314	def({ key: 'v_488_fallen_log', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7F5C45', drop: null, vanilla: { sheet: 488, frame: 'style', fw: 3, fh: 2 } });
315	def({ key: 'v_548_potted_trees_group_2', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 6, mapColor: '#786E64', drop: null, light: [179, 77, 51], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 548, frame: 'style', fw: 3, fh: 6 } });
316	def({ key: 'v_614_potted_ember_tendrils', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 6, mapColor: '#FA6432', drop: null, light: [179, 77, 51], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 614, frame: 'style', fw: 3, fh: 6 } });
317	def({ key: 'v_598_lava_serpent_bowl', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, light: [255, 185, 110], vanilla: { sheet: 598, frame: 'style', fw: 2, fh: 2 } });
318	def({ key: 'v_406_chimney', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#787878', drop: null, vanilla: { sheet: 406, frame: 'style', fw: 3, fh: 3 } });
319	def({ key: 'v_305_sky_mill', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null, vanilla: { sheet: 305, frame: 'style', fw: 3, fh: 3 } });
320	def({ key: 'v_300_bone_welder', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null, vanilla: { sheet: 300, frame: 'style', fw: 3, fh: 3 } });
321	def({ key: 'v_302_glass_kiln', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null, light: [212, 153, 128], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 302, frame: 'style', fw: 3, fh: 3 } });
322	def({ key: 'v_306_ice_machine', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null, vanilla: { sheet: 306, frame: 'style', fw: 3, fh: 3 } });
323	def({ key: 'v_247_autohammer', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#8C9696', drop: null, vanilla: { sheet: 247, frame: 'style', fw: 3, fh: 3 } });
324	def({ key: 'v_491_void_vault', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#3C14A0', light: [128, 102, 179], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 491, frame: 'style', fw: 3, fh: 3 } }); // 虚空保险库（bank4；破坏回收见储物族注释）
325	def({ key: 'v_106_sawmill', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#BF8E6F', drop: null, vanilla: { sheet: 106, frame: 'style', fw: 3, fh: 3 } });
326	def({ key: 'v_642_chlorophyte_extractinator', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#95D459', drop: null, vanilla: { sheet: 642, frame: 'style', fw: 3, fh: 3 } });
327	def({ key: 'v_319_ship_in_a_bottle', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#604430', drop: null, vanilla: { sheet: 319, frame: 'style', fw: 2, fh: 2 } });
328	def({ key: 'v_487_picnic_tables', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 4, h: 2, mapColor: '#BF8E6F', drop: null, vanilla: { sheet: 487, frame: 'style', fw: 4, fh: 2 } });
329	def({ key: 'v_97_safe', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#909490', vanilla: { sheet: 97, frame: 'style', fw: 2, fh: 2 } }); // 保险箱（bank2；破坏回收见储物族注释）
330	def({ key: 'v_320_seaweed_planter', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#CBB997', drop: null, vanilla: { sheet: 320, frame: 'style', fw: 2, fh: 3 } });
331	def({ key: 'v_405_fireplace', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#8C8C8C', drop: null, light: [255, 185, 110], vanilla: { sheet: 405, frame: 'style', fw: 3, fh: 2 } });
332	def({ key: 'v_378_target_dummy', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#A07864', drop: null, vanilla: { sheet: 378, frame: 'style', fw: 2, fh: 3 } });
333	def({ key: 'v_218_meat_grinder', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#909490', drop: null, vanilla: { sheet: 218, frame: 'style', fw: 3, fh: 2 } });
334	def({ key: 'v_356_enchanted_sundial', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#E9CB18', drop: null, light: [115, 64, 0], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 356, frame: 'style', fw: 2, fh: 3 } });
335	def({ key: 'v_114_tinkerer_s_workshop', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: null, vanilla: { sheet: 114, frame: 'style', fw: 3, fh: 2 } });
336	def({ key: 'v_237_lihzahrd_altar', name: '', solid: false, framed: true, opacity: 0.05, pick: 210, w: 3, h: 2, mapColor: '#FFF133', drop: null, light: [26, 26, 0], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 237, frame: 'style', fw: 3, fh: 2 } });
337	def({ key: 'v_110_hallow_short_plants', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#30BA87', drop: null, vanilla: { sheet: 110, frame: 'style', fw: 1, fh: 1 } });
338	def({ key: 'v_621_slice_of_cake', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#FAFAFA', drop: null, vanilla: { sheet: 621, frame: 'style', fw: 2, fh: 2 } });
339	def({ key: 'v_387_trap_door_closed', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 2, h: 1, mapColor: '#7F5C45', drop: null, vanilla: { sheet: 387, frame: 'style', fw: 2, fh: 1 } });
340	def({ key: 'v_316_blue_jellyfish_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#9DB0E2', drop: null, light: [102, 26, 64], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 316, frame: 'style', fw: 2, fh: 2 } });
341	def({ key: 'v_125_crystal_ball', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#8DAFFF', drop: null, light: [0, 27, 54], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 125, frame: 'style', fw: 2, fh: 2 } });
342	def({ key: 'v_287_ammo_box', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#4F8011', drop: null, vanilla: { sheet: 287, frame: 'style', fw: 2, fh: 2 } });
343	def({ key: 'v_294_zebra_swallowtail_butterfly_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 294, frame: 'style', fw: 2, fh: 2 } });
344	def({ key: 'v_291_ulysses_butterfly_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 291, frame: 'style', fw: 2, fh: 2 } });
345	def({ key: 'v_292_sulphur_butterfly_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 292, frame: 'style', fw: 2, fh: 2 } });
346	def({ key: 'v_289_purple_emperor_butterfly_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 289, frame: 'style', fw: 2, fh: 2 } });
347	def({ key: 'v_172_sinks', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#BF8E6F', drop: null, vanilla: { sheet: 172, frame: 'style', fw: 2, fh: 2 } });
348	def({ key: 'v_656_glow_tulip', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#157CD4', drop: null, light: [255, 185, 110], vanilla: { sheet: 656, frame: 'style', fw: 1, fh: 1 } });
349	def({ key: 'v_113_hallow_tall_plants', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#30D0EA', drop: null, vanilla: { sheet: 113, frame: 'style', fw: 1, fh: 1 } });
350	def({ key: 'v_235_teleporter', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 3, h: 1, mapColor: '#D6B82E', drop: null, vanilla: { sheet: 235, frame: 'style', fw: 3, fh: 1 } });
351	def({ key: 'v_567_garden_gnome', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#909490', drop: null, vanilla: { sheet: 567, frame: 'style', fw: 1, fh: 2 } });
352	
353	// 装饰/植物/藤蔓（非实心非framed）
354	def({ key: 'v_638_ash_vines', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#C8784B', drop: null, light: [83, 38, 13], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 638, frame: 'auto' } });
355	def({ key: 'v_528_mushroom_vines', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#B6AF82', drop: null, light: [0, 51, 255], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 528, frame: 'auto' } });
356	def({ key: 'v_382_flower_vines', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#1CD85E', drop: null, vanilla: { sheet: 382, frame: 'auto' } });
357	def({ key: 'v_124_wooden_beam', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#493324', drop: null, vanilla: { sheet: 124, frame: 'auto' } });
358	def({ key: 'v_575_rich_mahogany_beam', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#7D3D41', drop: null, vanilla: { sheet: 575, frame: 'auto' } });
359	def({ key: 'v_213_rope', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#897843', drop: null, rope: true, vanilla: { sheet: 213, frame: 'auto' } });
360	def({ key: 'v_636_corrupt_vines', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#7A74DA', drop: null, vanilla: { sheet: 636, frame: 'auto' } });
361	def({ key: 'v_574_boreal_beam', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#4C392C', drop: null, vanilla: { sheet: 574, frame: 'auto' } });
362	def({ key: 'v_333_platinum_coin_pile', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#BEBEB2', drop: null, vanilla: { sheet: 333, frame: 'auto' } });
363	def({ key: 'v_332_gold_coin_pile', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#CCB548', drop: null, vanilla: { sheet: 332, frame: 'auto' } });
364	def({ key: 'v_577_sandstone_column', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#B2683A', drop: null, vanilla: { sheet: 577, frame: 'auto' } });
365	def({ key: 'v_561_marble_column', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#949EB8', drop: null, vanilla: { sheet: 561, frame: 'auto' } });
366	def({ key: 'v_576_granite_column', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#1E1A54', drop: null, vanilla: { sheet: 576, frame: 'auto' } });
367	def({ key: 'v_214_chain', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#676767', drop: null, vanilla: { sheet: 214, frame: 'auto' } });
368	def({ key: 'v_578_mushroom_beam', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#AC9B6E', drop: null, light: [0, 51, 255], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 578, frame: 'auto' } });
369	
370	// cleared 组补全（藤蔓/荆棘，原版 51/52/62/69）
371	def({ key: 'v_52_vines', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#17B14C', drop: null, vanilla: { sheet: 52, frame: 'auto' } });
372	def({ key: 'v_62_jungle_vines', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#79B018', drop: null, vanilla: { sheet: 62, frame: 'auto' } });
373	def({ key: 'v_69_jungle_thorns', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#BE965C', drop: null, vanilla: { sheet: 69, frame: 'auto' } });
374	
375	// ===================== FTW_V2 兼容补全 =====================
376	def({ key: 'v_625_neon_moss_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#DC0CED', blend: true, drop: null, light: [77, 0, 89], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 625, frame: 'auto' } });
377	def({ key: 'v_151_sandstone_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#BEAB5E', blend: true, drop: null, vanilla: { sheet: 151, frame: 'auto' } });
378	def({ key: 'v_234_crimsand_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#352C29', blend: true, drop: null, vanilla: { sheet: 234, frame: 'auto' } });
379	def({ key: 'v_182_blue_moss_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#2B568C', blend: true, drop: null, vanilla: { sheet: 182, frame: 'auto' } });
380	def({ key: 'v_205_crimson_vines', name: '', solid: false, /* 原版非实心 */ opacity: 1, pick: 0, mapColor: '#BA3234', blend: true, drop: null, vanilla: { sheet: 205, frame: 'auto' } });
381	def({ key: 'v_45_gold_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#B9A417', blend: true, drop: null, vanilla: { sheet: 45, frame: 'auto' } });
382	def({ key: 'v_399_crimson_hardened_sand_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#4D4C42', blend: true, drop: null, vanilla: { sheet: 399, frame: 'auto' } });
383	def({ key: 'v_352_crimtane_thorns', name: '', solid: false, /* 原版非实心：荆棘只伤不挡 */ opacity: 1, pick: 0, mapColor: '#EE615E', blend: true, drop: null, vanilla: { sheet: 352, frame: 'auto' } });
384	def({ key: 'v_248_palladium_column', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#DB4726', blend: true, drop: null, vanilla: { sheet: 248, frame: 'auto' } });
385	def({ key: 'v_340_living_cursed_fire_block', name: '', solid: false, /* 原版非实心：活性诅咒火可穿 */ opacity: 1, pick: 0, mapColor: '#60F802', blend: true, drop: null, light: [115, 255, 115], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 340, frame: 'auto' } });
386	def({ key: 'v_207_water_fountains', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 4, mapColor: '#909490', drop: null, vanilla: { sheet: 207, frame: 'style', fw: 2, fh: 4 } });
387	def({ key: 'v_144_timers', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#909490', drop: null, vanilla: { sheet: 144, frame: 'style', fw: 1, fh: 1 } });
388	def({ key: 'v_475_hat_rack', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 4, mapColor: '#BF8E6F', vanilla: { sheet: 475, frame: 'style', fw: 3, fh: 4 } });
389	def({ key: 'v_175_tin_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#817D5D', blend: true, drop: null, vanilla: { sheet: 175, frame: 'auto' } });
390	def({ key: 'v_132_lever', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#909490', drop: null, vanilla: { sheet: 132, frame: 'style', fw: 2, fh: 2 } });
391	
392	// ===================== 不负责任的女妖啤酒厂 兼容补全 =====================
393	def({ key: 'v_539_argon_moss_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#D0007E', blend: true, drop: null, light: [77, 0, 43], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 539, frame: 'auto' } });
394	def({ key: 'v_481_cracked_blue_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#42546D', blend: true, drop: null, vanilla: { sheet: 481, frame: 'auto' } });
395	def({ key: 'v_119_iridescent_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#6B5C6C', blend: true, drop: null, vanilla: { sheet: 119, frame: 'auto' } });
396	def({ key: 'v_120_mudstone_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#5C4449', blend: true, drop: null, vanilla: { sheet: 120, frame: 'auto' } });
397	def({ key: 'v_714_spider_boulder', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 2, h: 2, mapColor: '#808080', drop: null, vanilla: { sheet: 714, frame: 'style', fw: 2, fh: 2 } });
398	def({ key: 'v_752_chillet_egg', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7ad9e8', drop: null, vanilla: { sheet: 752, frame: 'style', fw: 2, fh: 2 } });
399	def({ key: 'v_751_sleeping_digtoise', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#baa854', drop: null, vanilla: { sheet: 751, frame: 'style', fw: 2, fh: 2 } });
400	def({ key: 'v_664_bouncy_boulder', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 2, h: 2, mapColor: '#808080', drop: null, vanilla: { sheet: 664, frame: 'style', fw: 2, fh: 2 } });
401	def({ key: 'v_711_rainbow_boulder', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 2, h: 2, mapColor: '#808080', drop: null, light: [3, 3, 3], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 711, frame: 'style', fw: 2, fh: 2 } });
402	def({ key: 'v_715_ghoulder', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 2, h: 2, mapColor: '#808080', drop: null, vanilla: { sheet: 715, frame: 'style', fw: 2, fh: 2 } });
403	def({ key: 'v_716_friendly_boulder', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 2, h: 2, mapColor: '#808080', drop: null, vanilla: { sheet: 716, frame: 'style', fw: 2, fh: 2 } });
404	def({ key: 'v_713_lava_boulder', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 2, h: 2, mapColor: '#808080', drop: null, vanilla: { sheet: 713, frame: 'style', fw: 2, fh: 2 } });
405	
406	// ===================== wld 独立映射修复（原为错误复用） =====================
407	def({ key: 'v_23_corrupt_grass_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#8D89DF', blend: true, drop: null, vanilla: { sheet: 23, frame: 'blend' } });
408	def({ key: 'v_31_orb_heart', name: '', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#8D78A8', drop: null, light: [79, 26, 112], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 31, frame: 'style', fw: 2, fh: 2 } });
409	def({ key: 'v_41_blue_brick', name: '', solid: true, opacity: 1, pick: 100, mapColor: '#42546D', blend: true, drop: null, vanilla: { sheet: 41, frame: 'auto' } });
410	def({ key: 'v_75_obsidian_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#1A1A1A', blend: true, drop: null, vanilla: { sheet: 75, frame: 'auto' } });
411	def({ key: 'v_199_crimson_grass_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#D05050', blend: true, drop: null, vanilla: { sheet: 199, frame: 'blend' } });
412	def({ key: 'v_60_jungle_grass_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#8FD71D', blend: true, drop: null, vanilla: { sheet: 60, frame: 'blend' } });
413	def({ key: 'v_70_mushroom_grass_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#5D7FFF', blend: true, drop: null, light: [0, 51, 255], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 70, frame: 'blend' } });
414	
415	def({ key: 'v_25_ebonstone_block', name: '', solid: true, opacity: 1, pick: 65, mapColor: '#6D5A80', blend: true, drop: null, vanilla: { sheet: 25, frame: 'blend' } });
416	def({ key: 'v_202_sunplate_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#D5B21C', blend: true, drop: null, vanilla: { sheet: 202, frame: 'auto' } });
417	def({ key: 'v_71_mushroom_plant', name: '', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#B6AF82', drop: null, light: [0, 51, 255], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 71, frame: 'style', fw: 1, fh: 1 } });
418	def({ key: 'v_24_corruption_short_plants', name: '', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#7A74DA', drop: null, vanilla: { sheet: 24, frame: 'style', fw: 1, fh: 1 } });
419	def({ key: 'v_32_corruption_thorns', name: '', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#9787B7', drop: null, vanilla: { sheet: 32, frame: 'style', fw: 1, fh: 1 } });
420	def({ key: 'v_27_sunflower', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 4, mapColor: '#369A36', drop: null, light: [255, 242, 166], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 27, frame: 'style', fw: 2, fh: 4 } });
421	def({ key: 'v_5_trees', name: '', decor: true, framed: true, opacity: 0, pick: 0, axe: 0, mapColor: '#976B4B', drop: null, vanilla: { sheet: 5, frame: 'style', fw: 1, fh: 1 } });
422	def({ key: 'v_80_cactus', name: '', decor: true, framed: true, opacity: 0, pick: 0, axe: 0, mapColor: '#497811', drop: null, vanilla: { sheet: 80, frame: 'style', fw: 1, fh: 1 } });
423	
424	def({ key: 'v_3_forest_short_plants', name: '', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#1AC454', drop: null, vanilla: { sheet: 3, frame: 'style', fw: 1, fh: 1 } });
425	// 自研像素方块(F11 图片→像素画工具,原版无此功能):实心 framed 块,RGB 编码进
426	// frameX=((r||1)<<8)|(g||1) / frameY=(b||1)(||1 防 0,0 触发 style 路径锚点重建扫描)。
427	// 渲染端 drawVanillaCell 顶部独占分支直画纯色+斜面,不取任何素材表。
428	// 可破坏(走镐挖路径)/进存档(type+frames 既有持久化,零格式改动)/联机走 setTile 上报。
429	def({ key: 'pixel_block', name: '像素方块', solid: true, framed: true, opacity: 1, pick: 0, mapColor: '#888888', drop: null, vanilla: { sheet: 0, frame: 'style', fw: 1, fh: 1 } });
430	def({ key: 'v_73_forest_tall_plants', name: '', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#1BC56D', drop: null, vanilla: { sheet: 73, frame: 'style', fw: 1, fh: 1 } });
431	def({ key: 'v_61_jungle_short_plants', name: '', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#87C41A', drop: null, light: [107, 207, 133], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 61, frame: 'style', fw: 1, fh: 1 } }); // 丛林矮草（16x20 表）
432	def({ key: 'v_74_jungle_tall_plants', name: '', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#60C51B', drop: null, vanilla: { sheet: 74, frame: 'style', fw: 1, fh: 2 } }); // 丛林高草（16x32 两格高）
433	def({ key: 'v_83_herbs_mature', name: '', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#F6C51A', drop: null, light: [230, 184, 46], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 83, frame: 'style', fw: 1, fh: 1 } });
434	def({ key: 'v_84_herbs_bloom', name: '', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#F6C51A', drop: null, vanilla: { sheet: 84, frame: 'style', fw: 1, fh: 1 } });
435	def({ key: 'v_72_mushroom_tree', name: '', decor: true, framed: true, opacity: 0, pick: -1, axe: 0, mapColor: '#B6AF82', drop: null, light: [0, 51, 255], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 72, frame: 'style', fw: 1, fh: 1 } });
436	def({ key: 'v_43_green_brick', name: '', solid: true, opacity: 1, pick: 100, mapColor: '#54643F', blend: true, drop: null, vanilla: { sheet: 43, frame: 'auto' } });
437	def({ key: 'v_44_pink_brick', name: '', solid: true, opacity: 1, pick: 100, mapColor: '#6B4463', blend: true, drop: null, vanilla: { sheet: 44, frame: 'auto' } });
438	def({ key: 'v_203_crimstone_block', name: '', solid: true, opacity: 1, pick: 65, mapColor: '#802C2D', blend: true, drop: null, vanilla: { sheet: 203, frame: 'blend' } });
439	def({ key: 'v_201_crimson_short_plants', name: '', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#CB3D40', drop: null, vanilla: { sheet: 201, frame: 'style', fw: 1, fh: 1 } });
440	
441	// 所有 def() 注册完毕后统一回填 key→id 映射（必须位于文件末尾）
442	// ===================== 电路系统器件(Wiring.cs HitWireSingle 器件表配套) =====================
443	def({ key: 'v_35_jackolanterns', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#E2911E', drop: null, light: [179, 153, 230], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 35, frame: 'style', fw: 2, fh: 2 } });
444	def({ key: 'v_92_lampposts', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 6, mapColor: '#D5E5ED', drop: null, light: [255, 255, 255], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 92, frame: 'style', fw: 1, fh: 6 } });
445	def({ key: 'v_126_discoball', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#9FD1E5', drop: null, vanilla: { sheet: 126, frame: 'style', fw: 2, fh: 2 } });
446	def({ key: 'v_131_inactivestoneblock', name: '', solid: false, /* 致动关闭态=inactive：不参与碰撞 */ opacity: 1, pick: 0, blend: true, mapColor: '#343434', drop: null, vanilla: { sheet: 131, frame: 'auto' } });
447	def({ key: 'v_139_musicboxes', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#BF8E6F', drop: null, vanilla: { sheet: 139, frame: 'style', fw: 2, fh: 2 } });
448	def({ key: 'v_142_inletpump', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#909490', drop: null, vanilla: { sheet: 142, frame: 'style', fw: 2, fh: 2 } });
449	def({ key: 'v_143_outletpump', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#909490', drop: null, vanilla: { sheet: 143, frame: 'style', fw: 2, fh: 2 } });
450	def({ key: 'v_149_holidaylights', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 1, mapColor: '#DC3232', drop: null, light: [26, 51, 128], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 149, frame: 'style', fw: 1, fh: 1 } });
451	def({ key: 'v_173_platinumcandelabra', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#FDDD03', drop: null, light: [255, 242, 166], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 173, frame: 'style', fw: 2, fh: 2 } });
452	def({ key: 'v_174_platinumcandle', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 1, mapColor: '#FDDD03', drop: null, light: [255, 242, 166], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 174, frame: 'style', fw: 1, fh: 1 } });
453	def({ key: 'v_209_cannon', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 4, h: 3, mapColor: '#909490', drop: null, vanilla: { sheet: 209, frame: 'style', fw: 4, fh: 3 } });
454	def({ key: 'v_210_landmine', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 1, mapColor: '#C03B3B', drop: null, vanilla: { sheet: 210, frame: 'style', fw: 1, fh: 1 } });
455	def({ key: 'v_212_snowballlauncher', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null, vanilla: { sheet: 212, frame: 'style', fw: 3, fh: 3 } });
456	def({ key: 'v_216_firework', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 2, mapColor: '#BF8E6F', drop: null, vanilla: { sheet: 216, frame: 'style', fw: 1, fh: 2 } });
457	def({ key: 'v_244_bubblemachine', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 3, h: 2, mapColor: '#C8F5FD', drop: null, vanilla: { sheet: 244, frame: 'style', fw: 3, fh: 2 } });
458	def({ key: 'v_255_amethystgemsparkoff', name: '', solid: true, opacity: 1, pick: 0, blend: true, mapColor: '#6B319A', drop: null, vanilla: { sheet: 255, frame: 'auto' } });
459	def({ key: 'v_256_topazgemsparkoff', name: '', solid: true, opacity: 1, pick: 0, blend: true, mapColor: '#9A9431', drop: null, vanilla: { sheet: 256, frame: 'auto' } });
460	def({ key: 'v_257_sapphiregemsparkoff', name: '', solid: true, opacity: 1, pick: 0, blend: true, mapColor: '#31319A', drop: null, vanilla: { sheet: 257, frame: 'auto' } });
461	def({ key: 'v_258_emeraldgemsparkoff', name: '', solid: true, opacity: 1, pick: 0, blend: true, mapColor: '#319A44', drop: null, vanilla: { sheet: 258, frame: 'auto' } });
462	def({ key: 'v_259_rubygemsparkoff', name: '', solid: true, opacity: 1, pick: 0, blend: true, mapColor: '#9A314D', drop: null, vanilla: { sheet: 259, frame: 'auto' } });
463	def({ key: 'v_260_diamondgemsparkoff', name: '', solid: true, opacity: 1, pick: 0, blend: true, mapColor: '#555976', drop: null, vanilla: { sheet: 260, frame: 'auto' } });
464	def({ key: 'v_261_ambergemsparkoff', name: '', solid: true, opacity: 1, pick: 0, blend: true, mapColor: '#9A5331', drop: null, vanilla: { sheet: 261, frame: 'auto' } });
465	def({ key: 'v_262_amethystgemspark', name: '', solid: true, opacity: 1, pick: 0, blend: true, mapColor: '#DD4FFF', drop: null, vanilla: { sheet: 262, frame: 'auto' } });
466	def({ key: 'v_263_topazgemspark', name: '', solid: true, opacity: 1, pick: 0, blend: true, mapColor: '#FAFF4F', drop: null, vanilla: { sheet: 263, frame: 'auto' } });
467	def({ key: 'v_264_sapphiregemspark', name: '', solid: true, opacity: 1, pick: 0, blend: true, mapColor: '#4F66FF', drop: null, vanilla: { sheet: 264, frame: 'auto' } });
468	def({ key: 'v_265_emeraldgemspark', name: '', solid: true, opacity: 1, pick: 0, blend: true, mapColor: '#4FFF59', drop: null, vanilla: { sheet: 265, frame: 'auto' } });
469	def({ key: 'v_266_rubygemspark', name: '', solid: true, opacity: 1, pick: 0, blend: true, mapColor: '#FF4F4F', drop: null, vanilla: { sheet: 266, frame: 'auto' } });
470	def({ key: 'v_267_diamondgemspark', name: '', solid: true, opacity: 1, pick: 0, blend: true, mapColor: '#F0F0F7', drop: null, vanilla: { sheet: 267, frame: 'auto' } });
471	def({ key: 'v_268_ambergemspark', name: '', solid: true, opacity: 1, pick: 0, blend: true, mapColor: '#FF914F', drop: null, vanilla: { sheet: 268, frame: 'auto' } });
472	def({ key: 'v_335_fireworksbox', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#D9AE89', drop: null, vanilla: { sheet: 335, frame: 'style', fw: 2, fh: 2 } });
473	def({ key: 'v_338_fireworkfountain', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 2, mapColor: '#55FFA0', drop: null, vanilla: { sheet: 338, frame: 'style', fw: 1, fh: 2 } });
474	def({ key: 'v_372_peacecandle', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 1, mapColor: '#FC80C9', drop: null, light: [230, 26, 191], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 372, frame: 'style', fw: 1, fh: 1 } });
475	def({ key: 'v_386_trapdooropen', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#7F5C45', drop: null, vanilla: { sheet: 386, frame: 'style', fw: 2, fh: 2 } });
476	def({ key: 'v_389_tallgateopen', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 5, mapColor: '#7F5C45', drop: null, vanilla: { sheet: 389, frame: 'style', fw: 1, fh: 5 } });
477	def({ key: 'v_410_lunarmonolith', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 3, mapColor: '#4B8BA6', drop: null, vanilla: { sheet: 410, frame: 'style', fw: 2, fh: 3 } });
478	def({ key: 'v_419_logicgatelamp', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 1, mapColor: '#585F72', drop: null, vanilla: { sheet: 419, frame: 'style', fw: 1, fh: 1 } });
479	def({ key: 'v_420_logicgate', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 1, mapColor: '#63FF6B', drop: null, vanilla: { sheet: 420, frame: 'style', fw: 1, fh: 1 } });
480	def({ key: 'v_421_conveyorbeltleft', name: '', solid: true, opacity: 1, pick: 0, blend: true, mapColor: '#414B5A', drop: null, vanilla: { sheet: 421, frame: 'auto' } });
481	def({ key: 'v_423_logicsensor', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 1, mapColor: '#F5C501', drop: null, vanilla: { sheet: 423, frame: 'style', fw: 1, fh: 1 } });
482	def({ key: 'v_424_wirepipe', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 1, mapColor: '#929BBB', drop: null, vanilla: { sheet: 424, frame: 'style', fw: 1, fh: 1 } });
483	def({ key: 'v_425_announcementbox', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#929BBB', drop: null, vanilla: { sheet: 425, frame: 'style', fw: 2, fh: 2 } });
484	def({ key: 'v_428_weightedpressureplate', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 1, mapColor: '#FFFFFF', drop: null, vanilla: { sheet: 428, frame: 'style', fw: 1, fh: 1 } });
485	def({ key: 'v_429_wirebulb', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 1, mapColor: '#DCDCDC', drop: null, vanilla: { sheet: 429, frame: 'style', fw: 1, fh: 1 } });
486	def({ key: 'v_440_gemlocks', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 3, h: 3, mapColor: '#EE3335', drop: null, vanilla: { sheet: 440, frame: 'style', fw: 3, fh: 3 } });
487	def({ key: 'v_441_fakecontainers', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#AE815C', drop: null, vanilla: { sheet: 441, frame: 'style', fw: 2, fh: 2 } });
488	def({ key: 'v_442_projectilepressurepad', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 1, mapColor: '#0390C9', drop: null, vanilla: { sheet: 442, frame: 'style', fw: 1, fh: 1 } });
489	def({ key: 'v_445_pixelbox', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 1, mapColor: '#F0F0F0', drop: null, vanilla: { sheet: 445, frame: 'style', fw: 1, fh: 1 } });
490	def({ key: 'v_452_sillyballoonmachine', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 3, h: 3, mapColor: '#FF96B5', drop: null, vanilla: { sheet: 452, frame: 'style', fw: 3, fh: 3 } });
491	def({ key: 'v_455_partymonolith', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 3, h: 3, mapColor: '#30E16E', drop: null, vanilla: { sheet: 455, frame: 'style', fw: 3, fh: 3 } });
492	def({ key: 'v_468_fakecontainers2', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#FFFFFF', drop: null, vanilla: { sheet: 468, frame: 'style', fw: 2, fh: 2 } });
493	def({ key: 'v_476_golfhole', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 1, h: 1, mapColor: '#A0A0A0', drop: null, vanilla: { sheet: 476, frame: 'style', fw: 1, fh: 1 } }); // 原版 tileSolid[476]=true
494	def({ key: 'v_480_bloodmoonmonolith', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 3, mapColor: '#783232', drop: null, vanilla: { sheet: 480, frame: 'style', fw: 2, fh: 3 } });
495	def({ key: 'v_497_toilets', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 2, mapColor: '#BF8E6F', drop: null, vanilla: { sheet: 497, frame: 'style', fw: 1, fh: 2 } });
496	def({ key: 'v_509_voidmonolith', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 3, mapColor: '#32323C', drop: null, vanilla: { sheet: 509, frame: 'style', fw: 2, fh: 3 } });
497	def({ key: 'v_531_boulderstatue', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 3, mapColor: '#909490', drop: null, vanilla: { sheet: 531, frame: 'style', fw: 2, fh: 3 } });
498	def({ key: 'v_546_grate', name: '', solid: true, opacity: 1, pick: 0, blend: true, mapColor: '#3C3C3C', drop: null, vanilla: { sheet: 546, frame: 'auto' } });
499	def({ key: 'v_557_grateclosed', name: '', solid: true, opacity: 1, pick: 0, blend: true, mapColor: '#3C3C3C', drop: null, vanilla: { sheet: 557, frame: 'auto' } });
500	def({ key: 'v_564_plasmalamp', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#577FDC', drop: null, light: [13, 77, 140], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 564, frame: 'style', fw: 2, fh: 2 } });
501	def({ key: 'v_565_fogmachine', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#636363', drop: null, vanilla: { sheet: 565, frame: 'style', fw: 2, fh: 2 } });
502	def({ key: 'v_593_volcanosmall', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 1, mapColor: '#77694F', drop: null, light: [204, 77, 26], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 593, frame: 'style', fw: 1, fh: 1 } });
503	def({ key: 'v_594_volcanolarge', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#77694F', drop: null, light: [204, 77, 26], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 594, frame: 'style', fw: 2, fh: 2 } });
504	
505	def({ key: 'v_482_cracked_green_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#54643F', blend: true, drop: null, vanilla: { sheet: 482, frame: 'auto' } });
506	def({ key: 'v_163_purple_ice_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#AE91D6', blend: true, drop: null, vanilla: { sheet: 163, frame: 'auto' } });
507	def({ key: 'v_200_red_ice_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#D89890', blend: true, drop: null, vanilla: { sheet: 200, frame: 'auto' } });
508	def({ key: 'v_116_pearlsand_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#EEE1DA', blend: true, drop: null, vanilla: { sheet: 116, frame: 'auto' } });
509	def({ key: 'v_76_hellstone_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#8E4242', blend: true, drop: null, vanilla: { sheet: 76, frame: 'auto' } });
510	def({ key: 'v_77_hellforge', name: '', solid: false, framed: true, opacity: 1, pick: 65, light: [255, 140, 70], mapColor: '#EE5546', drop: null, vanilla: { sheet: 77, frame: 'style', fw: 3, fh: 2 } }); // 地狱熔炉（原版专属表 Tiles_77；tileSolid 未设=可通行，火光同熔炉）
511	def({ key: 'v_55_signs', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#BF8E6F', drop: null, vanilla: { sheet: 55, frame: 'style', fw: 2, fh: 2 } });
512	// 动画制作台补全（原版 AnimateTiles 300-308 组 + 499；TEdit 实名 301/307/308 曾在素材表提取缺口）
513	def({ key: 'v_301_flesh_cloning_vat', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null, vanilla: { sheet: 301, frame: 'style', fw: 3, fh: 3 } });
514	def({ key: 'v_307_steampunk_boiler', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null, vanilla: { sheet: 307, frame: 'style', fw: 3, fh: 3 } });
515	def({ key: 'v_308_honey_dispenser', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null, vanilla: { sheet: 308, frame: 'style', fw: 3, fh: 3 } });
516	def({ key: 'v_499_decay_chamber', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#A0BB8E', drop: null, vanilla: { sheet: 499, frame: 'style', fw: 3, fh: 3 } });
517	
518	// ===================== TEdit 全量补齐（缺失 sheet 程序生成，勿手改） =====================
519	def({ key: 'v_36_presents', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#E6595C', drop: null, vanilla: { sheet: 36, frame: 'style', fw: 1, fh: 1 } });
520	def({ key: 'v_46_silver_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#B9C2C3', blend: true, drop: null, vanilla: { sheet: 46, frame: 'auto' } });
521	def({ key: 'v_47_copper_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#964316', blend: true, drop: null, vanilla: { sheet: 47, frame: 'auto' } });
522	def({ key: 'v_99_trash_can', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#909490', drop: null, vanilla: { sheet: 99, frame: 'style', fw: 2, fh: 2 } });
523	def({ key: 'v_102_throne', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 4, mapColor: '#E5D449', drop: null, vanilla: { sheet: 102, frame: 'style', fw: 3, fh: 4 } });
524	def({ key: 'v_115_hallowed_vines', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#21ABCF', blend: true, drop: null, vanilla: { sheet: 115, frame: 'auto' } });
525	def({ key: 'v_121_cobalt_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#0B508F', blend: true, drop: null, vanilla: { sheet: 121, frame: 'auto' } });
526	def({ key: 'v_122_mythril_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#5BA9A9', blend: true, drop: null, vanilla: { sheet: 122, frame: 'auto' } });
527	def({ key: 'v_127_ice_ice_rod', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#80CCE6', blend: true, drop: null, vanilla: { sheet: 127, frame: 'auto' } });
528	def({ key: 'v_128_mannequin_legacy', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#BF8E6F', drop: null, vanilla: { sheet: 128, frame: 'style', fw: 2, fh: 3 } });
529	def({ key: 'v_133_forges', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#E73538', drop: null, vanilla: { sheet: 133, frame: 'style', fw: 3, fh: 2 } });
530	def({ key: 'v_134_anvils_hardmode', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 1, mapColor: '#A6BB99', drop: null, vanilla: { sheet: 134, frame: 'style', fw: 2, fh: 1 } });
531	def({ key: 'v_140_demonite_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#625FA7', blend: true, drop: null, vanilla: { sheet: 140, frame: 'auto' } });
532	def({ key: 'v_145_red_candy_cane_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#C01E1E', blend: true, drop: null, vanilla: { sheet: 145, frame: 'auto' } });
533	def({ key: 'v_146_green_candy_cane_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#2BC01E', blend: true, drop: null, vanilla: { sheet: 146, frame: 'auto' } });
534	def({ key: 'v_150_adamantite_beam', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#801A34', blend: true, drop: null, vanilla: { sheet: 150, frame: 'auto' } });
535	def({ key: 'v_153_red_stucco', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#EF8D7E', blend: true, drop: null, vanilla: { sheet: 153, frame: 'auto' } });
536	def({ key: 'v_154_yellow_stucco', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#BEAB5E', blend: true, drop: null, vanilla: { sheet: 154, frame: 'auto' } });
537	def({ key: 'v_155_green_stucco', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#83A2A1', blend: true, drop: null, vanilla: { sheet: 155, frame: 'auto' } });
538	def({ key: 'v_156_gray_stucco', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#AAAB9D', blend: true, drop: null, vanilla: { sheet: 156, frame: 'auto' } });
539	def({ key: 'v_157_ebonwood', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#68647E', blend: true, drop: null, vanilla: { sheet: 157, frame: 'auto' } });
540	def({ key: 'v_159_pearlwood', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#948562', blend: true, drop: null, vanilla: { sheet: 159, frame: 'auto' } });
541	def({ key: 'v_160_rainbow_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#0000C8', blend: true, drop: null, vanilla: { sheet: 160, frame: 'auto' } });
542	def({ key: 'v_164_pink_ice_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#DAB6CC', blend: true, drop: null, vanilla: { sheet: 164, frame: 'auto' } });
543	def({ key: 'v_170_pine_tree_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#1B6D45', blend: true, drop: null, vanilla: { sheet: 170, frame: 'auto' } });
544	def({ key: 'v_171_christmas_tree', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 4, h: 8, mapColor: '#218755', drop: null, vanilla: { sheet: 171, frame: 'style', fw: 4, fh: 8 } });
545	def({ key: 'v_176_tungsten_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#849D7F', blend: true, drop: null, vanilla: { sheet: 176, frame: 'auto' } });
546	def({ key: 'v_177_platinum_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#98ABC6', blend: true, drop: null, vanilla: { sheet: 177, frame: 'auto' } });
547	def({ key: 'v_180_yellow_moss_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#7E8631', blend: true, drop: null, vanilla: { sheet: 180, frame: 'auto' } });
548	def({ key: 'v_188_cactus_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#497811', blend: true, drop: null, vanilla: { sheet: 188, frame: 'auto' } });
549	def({ key: 'v_194_bone_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#9D9D6B', blend: true, drop: null, vanilla: { sheet: 194, frame: 'auto' } });
550	def({ key: 'v_195_flesh_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#861622', blend: true, drop: null, vanilla: { sheet: 195, frame: 'auto' } });
551	def({ key: 'v_197_frozen_slime_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#61C8E1', blend: true, drop: null, vanilla: { sheet: 197, frame: 'auto' } });
552	def({ key: 'v_198_asphalt_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#3E3D34', blend: true, drop: null, vanilla: { sheet: 198, frame: 'auto' } });
553	def({ key: 'v_208_shadewood', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#586976', blend: true, drop: null, vanilla: { sheet: 208, frame: 'auto' } });
554	def({ key: 'v_217_blend_o_matic', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#909490', drop: null, vanilla: { sheet: 217, frame: 'style', fw: 3, fh: 2 } });
555	def({ key: 'v_228_dye_vat', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null, vanilla: { sheet: 228, frame: 'style', fw: 3, fh: 3 } });
556	def({ key: 'v_236_life_fruit_plant', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#95E857', drop: null, vanilla: { sheet: 236, frame: 'style', fw: 2, fh: 2 } });
557	def({ key: 'v_238_plantera_s_bulb', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#E180CE', drop: null, vanilla: { sheet: 238, frame: 'style', fw: 2, fh: 2 } });
558	def({ key: 'v_239_ore_bars', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 1, h: 1, mapColor: '#E0C265', drop: null, vanilla: { sheet: 239, frame: 'style', fw: 1, fh: 1 } });
559	def({ key: 'v_243_imbuing_station', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#C6C4AA', drop: null, vanilla: { sheet: 243, frame: 'style', fw: 3, fh: 3 } });
560	def({ key: 'v_249_bubblegum_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#EB26E7', blend: true, drop: null, vanilla: { sheet: 249, frame: 'auto' } });
561	def({ key: 'v_250_titanstone_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#56555C', blend: true, drop: null, vanilla: { sheet: 250, frame: 'auto' } });
562	def({ key: 'v_251_pumpkin_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#EB9617', blend: true, drop: null, vanilla: { sheet: 251, frame: 'auto' } });
563	def({ key: 'v_252_hay_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#99832C', blend: true, drop: null, vanilla: { sheet: 252, frame: 'auto' } });
564	def({ key: 'v_253_spooky_wood', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#393061', blend: true, drop: null, vanilla: { sheet: 253, frame: 'auto' } });
565	def({ key: 'v_269_womannequin_legacy', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#BF8E6F', drop: null, vanilla: { sheet: 269, frame: 'style', fw: 2, fh: 3 } });
566	def({ key: 'v_270_firefly_in_a_bottle', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#BBFF6B', drop: null, vanilla: { sheet: 270, frame: 'style', fw: 1, fh: 2 } });
567	def({ key: 'v_271_lightning_bug_in_a_bottle', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#6BFAFF', drop: null, vanilla: { sheet: 271, frame: 'style', fw: 1, fh: 2 } });
568	def({ key: 'v_275_bunny_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 275, frame: 'style', fw: 6, fh: 3 } });
569	def({ key: 'v_276_squirrel_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 276, frame: 'style', fw: 6, fh: 3 } });
570	def({ key: 'v_277_mallard_duck_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 277, frame: 'style', fw: 6, fh: 3 } });
571	def({ key: 'v_278_duck_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 278, frame: 'style', fw: 6, fh: 3 } });
572	def({ key: 'v_279_bird_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 279, frame: 'style', fw: 6, fh: 3 } });
573	def({ key: 'v_280_blue_jay_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 280, frame: 'style', fw: 6, fh: 3 } });
574	def({ key: 'v_281_cardinal_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 281, frame: 'style', fw: 6, fh: 3 } });
575	def({ key: 'v_282_fish_bowl', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 282, frame: 'style', fw: 2, fh: 2 } });
576	def({ key: 'v_283_heavy_work_bench', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#808080', drop: null, vanilla: { sheet: 283, frame: 'style', fw: 3, fh: 3 } });
577	def({ key: 'v_284_copper_plating', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#964316', blend: true, drop: null, vanilla: { sheet: 284, frame: 'auto' } });
578	def({ key: 'v_285_snail_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 285, frame: 'style', fw: 3, fh: 2 } });
579	def({ key: 'v_286_glowing_snail_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 286, frame: 'style', fw: 3, fh: 2 } });
580	def({ key: 'v_288_monarch_butterfly_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 288, frame: 'style', fw: 2, fh: 2 } });
581	def({ key: 'v_290_red_admiral_butterfly_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 290, frame: 'style', fw: 2, fh: 2 } });
582	def({ key: 'v_293_tree_nymph_butterfly_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 293, frame: 'style', fw: 2, fh: 2 } });
583	def({ key: 'v_295_julia_butterfly_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 295, frame: 'style', fw: 2, fh: 2 } });
584	def({ key: 'v_296_scorpion_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 296, frame: 'style', fw: 6, fh: 3 } });
585	def({ key: 'v_297_black_scorpion_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 297, frame: 'style', fw: 6, fh: 3 } });
586	def({ key: 'v_298_frog_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 298, frame: 'style', fw: 3, fh: 2 } });
587	def({ key: 'v_299_mouse_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 299, frame: 'style', fw: 3, fh: 2 } });
588	def({ key: 'v_309_penguin_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 309, frame: 'style', fw: 6, fh: 3 } });
589	def({ key: 'v_310_worm_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 310, frame: 'style', fw: 3, fh: 2 } });
590	def({ key: 'v_313_blue_dynasty_shingles', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#57969A', blend: true, drop: null, vanilla: { sheet: 313, frame: 'auto' } });
591	def({ key: 'v_315_coralstone_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#EB7250', blend: true, drop: null, vanilla: { sheet: 315, frame: 'auto' } });
592	def({ key: 'v_317_green_jellyfish_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#76E381', drop: null, vanilla: { sheet: 317, frame: 'style', fw: 2, fh: 2 } });
593	def({ key: 'v_318_pink_jellyfish_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#E376D7', drop: null, vanilla: { sheet: 318, frame: 'style', fw: 2, fh: 2 } });
594	def({ key: 'v_325_tin_plating', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#817D5D', blend: true, drop: null, vanilla: { sheet: 325, frame: 'auto' } });
595	def({ key: 'v_326_waterfall_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#093DBF', blend: true, drop: null, vanilla: { sheet: 326, frame: 'auto' } });
596	def({ key: 'v_327_lavafall_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#FD2003', blend: true, drop: null, vanilla: { sheet: 327, frame: 'auto' } });
597	def({ key: 'v_328_confetti_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#C8F6FE', blend: true, drop: null, vanilla: { sheet: 328, frame: 'auto' } });
598	def({ key: 'v_329_midnight_confetti_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#0F0F0F', blend: true, drop: null, vanilla: { sheet: 329, frame: 'auto' } });
599	def({ key: 'v_330_copper_coin_pile', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#E2764C', drop: null, vanilla: { sheet: 330, frame: 'auto' } });
600	def({ key: 'v_331_silver_coin_pile', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#A1ACAD', drop: null, vanilla: { sheet: 331, frame: 'auto' } });
601	def({ key: 'v_334_weapon_rack_legacy_do_not_use', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#BF8E6F', drop: null, vanilla: { sheet: 334, frame: 'style', fw: 3, fh: 3 } });
602	def({ key: 'v_336_living_fire_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#FD3E03', blend: true, drop: null, vanilla: { sheet: 336, frame: 'auto' } });
603	def({ key: 'v_337_text_statue', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#909490', drop: null, vanilla: { sheet: 337, frame: 'style', fw: 2, fh: 3 } });
604	def({ key: 'v_339_grasshopper_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 339, frame: 'style', fw: 3, fh: 2 } });
605	def({ key: 'v_341_living_demon_fire_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#694ACA', blend: true, drop: null, vanilla: { sheet: 341, frame: 'auto' } });
606	def({ key: 'v_342_living_frost_fire_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#1DF0FF', blend: true, drop: null, vanilla: { sheet: 342, frame: 'auto' } });
607	def({ key: 'v_343_living_ichor_fire_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#FECA50', blend: true, drop: null, vanilla: { sheet: 343, frame: 'auto' } });
608	def({ key: 'v_344_living_ultrabright_fire_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#83FCF5', blend: true, drop: null, vanilla: { sheet: 344, frame: 'auto' } });
609	def({ key: 'v_345_honeyfall_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#FF9C0C', blend: true, drop: null, vanilla: { sheet: 345, frame: 'auto' } });
610	def({ key: 'v_346_chlorophyte_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#95D459', blend: true, drop: null, vanilla: { sheet: 346, frame: 'auto' } });
611	def({ key: 'v_347_crimtane_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#EC4A4F', blend: true, drop: null, vanilla: { sheet: 347, frame: 'auto' } });
612	def({ key: 'v_348_shroomite_plating', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#2C1AE9', blend: true, drop: null, light: [0, 51, 255], /* 原版 tileLighted[348]（Main.cs:9923）+ 蘑菇组发光色（TileLightScanner.cs:2938） */ vanilla: { sheet: 348, frame: 'auto' } });
613	def({ key: 'v_351_smoke_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#1F1F1F', blend: true, drop: null, vanilla: { sheet: 351, frame: 'auto' } });
614	def({ key: 'v_358_gold_bird_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 358, frame: 'style', fw: 6, fh: 3 } });
615	def({ key: 'v_359_gold_bunny_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 359, frame: 'style', fw: 6, fh: 3 } });
616	def({ key: 'v_360_gold_butterfly_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 360, frame: 'style', fw: 2, fh: 2 } });
617	def({ key: 'v_361_gold_frog_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 361, frame: 'style', fw: 3, fh: 2 } });
618	def({ key: 'v_362_gold_grasshopper_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 362, frame: 'style', fw: 3, fh: 2 } });
619	def({ key: 'v_363_gold_mouse_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 363, frame: 'style', fw: 3, fh: 2 } });
620	def({ key: 'v_364_gold_worm_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 364, frame: 'style', fw: 3, fh: 2 } });
621	def({ key: 'v_365_silk_rope', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#9288CD', blend: true, drop: null, vanilla: { sheet: 365, frame: 'auto' } });
622	def({ key: 'v_366_web_rope', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#DFE8E9', blend: true, drop: null, vanilla: { sheet: 366, frame: 'auto' } });
623	def({ key: 'v_370_meteorite_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#7F74C2', blend: true, drop: null, vanilla: { sheet: 370, frame: 'auto' } });
624	def({ key: 'v_385_crystal_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#571590', blend: true, drop: null, vanilla: { sheet: 385, frame: 'auto' } });
625	def({ key: 'v_390_lava_lamp', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#FD2003', drop: null, vanilla: { sheet: 390, frame: 'style', fw: 1, fh: 2 } });
626	def({ key: 'v_391_cage_enchanted_nightcrawler', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 391, frame: 'style', fw: 3, fh: 2 } });
627	def({ key: 'v_392_buggy_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 392, frame: 'style', fw: 3, fh: 2 } });
628	def({ key: 'v_393_grubby_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 393, frame: 'style', fw: 3, fh: 2 } });
629	def({ key: 'v_394_sluggy_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 394, frame: 'style', fw: 3, fh: 2 } });
630	def({ key: 'v_400_corrupt_sandstone_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#604475', blend: true, drop: null, vanilla: { sheet: 400, frame: 'auto' } });
631	def({ key: 'v_401_crimson_sandstone_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#443C33', blend: true, drop: null, vanilla: { sheet: 401, frame: 'auto' } });
632	def({ key: 'v_402_hallow_hardened_sand_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#AEA8BA', blend: true, drop: null, vanilla: { sheet: 402, frame: 'auto' } });
633	def({ key: 'v_403_hallow_sandstone_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#CD98BA', blend: true, drop: null, vanilla: { sheet: 403, frame: 'auto' } });
634	def({ key: 'v_407_sturdy_fossil_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#FFE384', blend: true, drop: null, vanilla: { sheet: 407, frame: 'auto' } });
635	def({ key: 'v_408_luminite_ore', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#555352', blend: true, drop: null, vanilla: { sheet: 408, frame: 'auto' } });
636	def({ key: 'v_409_luminite_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#555352', blend: true, drop: null, vanilla: { sheet: 409, frame: 'auto' } });
637	def({ key: 'v_412_lunar_crafting_station', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#4B8BA6', drop: null, vanilla: { sheet: 412, frame: 'style', fw: 3, fh: 3 } });
638	def({ key: 'v_413_red_squirrel_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 413, frame: 'style', fw: 6, fh: 3 } });
639	def({ key: 'v_414_gold_squirrel_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 414, frame: 'style', fw: 6, fh: 3 } });
640	def({ key: 'v_415_solar_fragment_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#F94B07', blend: true, drop: null, vanilla: { sheet: 415, frame: 'auto' } });
641	def({ key: 'v_416_vortex_fragment_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#00A0AA', blend: true, drop: null, vanilla: { sheet: 416, frame: 'auto' } });
642	def({ key: 'v_417_nebula_fragment_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#A057EA', blend: true, drop: null, vanilla: { sheet: 417, frame: 'auto' } });
643	def({ key: 'v_418_stardust_fragment_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#16ADFE', blend: true, drop: null, vanilla: { sheet: 418, frame: 'auto' } });
644	def({ key: 'v_426_red_team_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#A8262F', blend: true, drop: null, vanilla: { sheet: 426, frame: 'auto' } });
645	def({ key: 'v_427_red_team_platform', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 1, h: 1, mapColor: '#B7353E', drop: null, vanilla: { sheet: 427, frame: 'style', fw: 1, fh: 1 } });
646	def({ key: 'v_430_green_team_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#27A860', blend: true, drop: null, vanilla: { sheet: 430, frame: 'auto' } });
647	def({ key: 'v_431_blue_team_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#275EA8', blend: true, drop: null, vanilla: { sheet: 431, frame: 'auto' } });
648	def({ key: 'v_432_yellow_team_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#F2DD64', blend: true, drop: null, vanilla: { sheet: 432, frame: 'auto' } });
649	def({ key: 'v_433_pink_team_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#E064F2', blend: true, drop: null, vanilla: { sheet: 433, frame: 'auto' } });
650	def({ key: 'v_434_white_team_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#C5C1D8', blend: true, drop: null, vanilla: { sheet: 434, frame: 'auto' } });
651	def({ key: 'v_435_green_team_platform', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 1, h: 1, mapColor: '#36B76F', drop: null, vanilla: { sheet: 435, frame: 'style', fw: 1, fh: 1 } });
652	def({ key: 'v_436_blue_team_platform', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 1, h: 1, mapColor: '#366DB7', drop: null, vanilla: { sheet: 436, frame: 'style', fw: 1, fh: 1 } });
653	def({ key: 'v_437_yellow_team_platform', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 1, h: 1, mapColor: '#FFEC73', drop: null, vanilla: { sheet: 437, frame: 'style', fw: 1, fh: 1 } });
654	def({ key: 'v_438_pink_team_platform', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 1, h: 1, mapColor: '#EF73FF', drop: null, vanilla: { sheet: 438, frame: 'style', fw: 1, fh: 1 } });
655	def({ key: 'v_439_white_team_platform', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 1, h: 1, mapColor: '#D4D0E7', drop: null, vanilla: { sheet: 439, frame: 'style', fw: 1, fh: 1 } });
656	def({ key: 'v_446_silly_pink_balloon_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#FF4298', blend: true, drop: null, vanilla: { sheet: 446, frame: 'auto' } });
657	def({ key: 'v_447_silly_purple_balloon_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#B384FF', blend: true, drop: null, vanilla: { sheet: 447, frame: 'auto' } });
658	def({ key: 'v_448_silly_green_balloon_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#00CEB4', blend: true, drop: null, vanilla: { sheet: 448, frame: 'auto' } });
659	def({ key: 'v_449_blue_streamer', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#5bbaf0', blend: true, drop: null, vanilla: { sheet: 449, frame: 'auto' } });
660	def({ key: 'v_450_green_streamer', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#5cf05b', blend: true, drop: null, vanilla: { sheet: 450, frame: 'auto' } });
661	def({ key: 'v_451_pink_streamer', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#f05b93', blend: true, drop: null, vanilla: { sheet: 451, frame: 'auto' } });
662	def({ key: 'v_453_silly_tied_balloon', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 3, mapColor: '#B384FF', drop: null, vanilla: { sheet: 453, frame: 'style', fw: 1, fh: 3 } });
663	def({ key: 'v_454_pigronata', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 4, h: 3, mapColor: '#ae10b0', drop: null, vanilla: { sheet: 454, frame: 'style', fw: 4, fh: 3 } });
664	def({ key: 'v_456_silly_tied_bundle_of_balloons', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#b384ff', drop: null, vanilla: { sheet: 456, frame: 'style', fw: 2, fh: 3 } });
665	def({ key: 'v_457_party_presents', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#96A4CE', drop: null, vanilla: { sheet: 457, frame: 'style', fw: 2, fh: 2 } });
666	def({ key: 'v_458_sandfall_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#d3c66f', blend: true, drop: null, vanilla: { sheet: 458, frame: 'auto' } });
667	def({ key: 'v_459_snowfall_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#bedfe8', blend: true, drop: null, vanilla: { sheet: 459, frame: 'auto' } });
668	def({ key: 'v_460_snow_cloud_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#8da3b5', blend: true, drop: null, vanilla: { sheet: 460, frame: 'auto' } });
669	def({ key: 'v_462_desert_spirit_lamp', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 1, mapColor: '#E7B21C', drop: null, vanilla: { sheet: 462, frame: 'style', fw: 2, fh: 1 } });
670	def({ key: 'v_464_war_table', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 5, h: 4, mapColor: '#E9B780', drop: null, vanilla: { sheet: 464, frame: 'style', fw: 5, fh: 4 } });
671	def({ key: 'v_465_war_table_banner', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#3354C3', drop: null, vanilla: { sheet: 465, frame: 'style', fw: 2, fh: 3 } });
672	def({ key: 'v_471_weapon_rack', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#BF8E6F', vanilla: { sheet: 471, frame: 'style', fw: 3, fh: 3 } });
673	def({ key: 'v_472_iron_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#BEA08C', blend: true, drop: null, vanilla: { sheet: 472, frame: 'auto' } });
674	def({ key: 'v_473_lead_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#55727B', blend: true, drop: null, vanilla: { sheet: 473, frame: 'auto' } });
675	def({ key: 'v_474_lesion_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#745E61', blend: true, drop: null, vanilla: { sheet: 474, frame: 'auto' } });
676	def({ key: 'v_478_crimstone_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#6C2223', blend: true, drop: null, vanilla: { sheet: 478, frame: 'auto' } });
677	def({ key: 'v_486_drum_set', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: null, vanilla: { sheet: 486, frame: 'style', fw: 3, fh: 2 } });
678	def({ key: 'v_489_pin_wheel', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#FF1D88', drop: null, vanilla: { sheet: 489, frame: 'style', fw: 2, fh: 3 } });
679	def({ key: 'v_490_weather_vane', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#D3D3D3', drop: null, vanilla: { sheet: 490, frame: 'style', fw: 2, fh: 2 } });
680	def({ key: 'v_492_hallowed_mowed_grass_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#4EC1E3', blend: true, drop: null, vanilla: { sheet: 492, frame: 'auto' } });
681	def({ key: 'v_493_pin_flags', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#FAF9FC', drop: null, vanilla: { sheet: 493, frame: 'style', fw: 1, fh: 2 } });
682	def({ key: 'v_494_golf_tee', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#E0DBEC', drop: null, vanilla: { sheet: 494, frame: 'style', fw: 1, fh: 1 } });
683	def({ key: 'v_496_anti_portal_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#A59F99', blend: true, drop: null, vanilla: { sheet: 496, frame: 'auto' } });
684	def({ key: 'v_498_spider_nest_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#CAAEA5', blend: true, drop: null, vanilla: { sheet: 498, frame: 'auto' } });
685	def({ key: 'v_500_solar_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#FE9E23', blend: true, drop: null, vanilla: { sheet: 500, frame: 'auto' } });
686	def({ key: 'v_501_vortex_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#22DD97', blend: true, drop: null, vanilla: { sheet: 501, frame: 'auto' } });
687	def({ key: 'v_502_nebula_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#F9AAEC', blend: true, drop: null, vanilla: { sheet: 502, frame: 'auto' } });
688	def({ key: 'v_503_stardust_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#23C8FE', blend: true, drop: null, vanilla: { sheet: 503, frame: 'auto' } });
689	def({ key: 'v_504_mystic_snake_rope', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#5C4B76', drop: null, vanilla: { sheet: 504, frame: 'auto' } });
690	def({ key: 'v_505_gold_fish_bowl', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 505, frame: 'style', fw: 2, fh: 2 } });
691	def({ key: 'v_507_gold_starry_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#050505', blend: true, drop: null, vanilla: { sheet: 507, frame: 'auto' } });
692	def({ key: 'v_508_blue_starry_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#050505', blend: true, drop: null, vanilla: { sheet: 508, frame: 'auto' } });
693	def({ key: 'v_510_arrow_sign', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#BF8E6F', drop: null, vanilla: { sheet: 510, frame: 'style', fw: 2, fh: 2 } });
694	def({ key: 'v_511_painted_arrow_sign', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#BB444A', drop: null, vanilla: { sheet: 511, frame: 'style', fw: 2, fh: 2 } });
695	def({ key: 'v_512_green_moss_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#318672', blend: true, drop: null, vanilla: { sheet: 512, frame: 'auto' } });
696	def({ key: 'v_513_brown_moss_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#7E8631', blend: true, drop: null, vanilla: { sheet: 513, frame: 'auto' } });
697	def({ key: 'v_514_red_moss_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#863B31', blend: true, drop: null, vanilla: { sheet: 514, frame: 'auto' } });
698	def({ key: 'v_515_blue_moss_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#2B568C', blend: true, drop: null, vanilla: { sheet: 515, frame: 'auto' } });
699	def({ key: 'v_516_purple_moss_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#793186', blend: true, drop: null, vanilla: { sheet: 516, frame: 'auto' } });
700	def({ key: 'v_517_lava_moss_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#FE7902', blend: true, drop: null, vanilla: { sheet: 517, frame: 'auto' } });
701	def({ key: 'v_520_plate', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#E0DBEC', vanilla: { sheet: 520, frame: 'style', fw: 1, fh: 1 } });
702	def({ key: 'v_521_black_dragonfly_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 521, frame: 'style', fw: 2, fh: 2 } });
703	def({ key: 'v_522_blue_dragonfly_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 522, frame: 'style', fw: 2, fh: 2 } });
704	def({ key: 'v_523_green_dragonfly_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 523, frame: 'style', fw: 2, fh: 2 } });
705	def({ key: 'v_524_orange_dragonfly_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 524, frame: 'style', fw: 2, fh: 2 } });
706	def({ key: 'v_525_red_dragonfly_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 525, frame: 'style', fw: 2, fh: 2 } });
707	def({ key: 'v_526_yellow_dragonfly_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 526, frame: 'style', fw: 2, fh: 2 } });
708	def({ key: 'v_527_gold_dragonfly_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 527, frame: 'style', fw: 2, fh: 2 } });
709	def({ key: 'v_532_maggot_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 532, frame: 'style', fw: 3, fh: 2 } });
710	def({ key: 'v_533_rat_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 533, frame: 'style', fw: 3, fh: 2 } });
711	def({ key: 'v_534_krypton_moss_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#72FE02', blend: true, drop: null, vanilla: { sheet: 534, frame: 'auto' } });
712	def({ key: 'v_535_krypton_moss_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#72FE02', blend: true, drop: null, vanilla: { sheet: 535, frame: 'auto' } });
713	def({ key: 'v_537_xenon_moss_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#00C5D0', blend: true, drop: null, vanilla: { sheet: 537, frame: 'auto' } });
714	def({ key: 'v_538_ladybug_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 538, frame: 'style', fw: 3, fh: 2 } });
715	def({ key: 'v_540_argon_moss_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#D0007E', blend: true, drop: null, vanilla: { sheet: 540, frame: 'auto' } });
716	def({ key: 'v_541_echo_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#326BC5', blend: true, drop: null, vanilla: { sheet: 541, frame: 'auto' } });
717	def({ key: 'v_542_owl_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 542, frame: 'style', fw: 6, fh: 3 } });
718	def({ key: 'v_543_pupfish_bowl', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 543, frame: 'style', fw: 2, fh: 2 } });
719	def({ key: 'v_544_gold_ladybug_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 544, frame: 'style', fw: 3, fh: 2 } });
720	def({ key: 'v_545_lawn_flamingo', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#FF7E91', drop: null, vanilla: { sheet: 545, frame: 'style', fw: 2, fh: 3 } });
721	def({ key: 'v_547_potted_trees', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 5, mapColor: '#786E64', drop: null, vanilla: { sheet: 547, frame: 'style', fw: 2, fh: 5 } });
722	def({ key: 'v_550_turtle_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 550, frame: 'style', fw: 6, fh: 3 } });
723	def({ key: 'v_551_jungle_turtle_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 551, frame: 'style', fw: 6, fh: 3 } });
724	def({ key: 'v_552_sandcastle_bucket', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BAA854', drop: null, vanilla: { sheet: 552, frame: 'style', fw: 3, fh: 2 } });
725	def({ key: 'v_553_grebe_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 553, frame: 'style', fw: 6, fh: 3 } });
726	def({ key: 'v_554_seagull_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 554, frame: 'style', fw: 6, fh: 3 } });
727	def({ key: 'v_555_water_strider_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 555, frame: 'style', fw: 3, fh: 2 } });
728	def({ key: 'v_556_gold_water_strider_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 556, frame: 'style', fw: 3, fh: 2 } });
729	def({ key: 'v_558_seahorse_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 558, frame: 'style', fw: 6, fh: 3 } });
730	def({ key: 'v_559_gold_seahorse_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 559, frame: 'style', fw: 6, fh: 3 } });
731	def({ key: 'v_560_golf_trophies', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#964316', drop: null, vanilla: { sheet: 560, frame: 'style', fw: 2, fh: 3 } });
732	def({ key: 'v_563_large_bamboo_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#A5A81A', blend: true, drop: null, vanilla: { sheet: 563, frame: 'auto' } });
733	def({ key: 'v_566_amber_stone_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#E9B45A', blend: true, drop: null, vanilla: { sheet: 566, frame: 'auto' } });
734	def({ key: 'v_568_pink_fairy_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#F8CBE9', drop: null, vanilla: { sheet: 568, frame: 'style', fw: 2, fh: 2 } });
735	def({ key: 'v_569_green_fairy_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#CBF8DA', drop: null, vanilla: { sheet: 569, frame: 'style', fw: 2, fh: 2 } });
736	def({ key: 'v_570_blue_fairy_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#A0F2FF', drop: null, vanilla: { sheet: 570, frame: 'style', fw: 2, fh: 2 } });
737	def({ key: 'v_572_souls_in_a_bottle', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#FFBAD4', drop: null, vanilla: { sheet: 572, frame: 'style', fw: 1, fh: 2 } });
738	def({ key: 'v_573_tattered_wood_sign', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#BF8E6F', drop: null, vanilla: { sheet: 573, frame: 'style', fw: 2, fh: 2 } });
739	def({ key: 'v_579_rock_golem_head', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#636363', drop: null, vanilla: { sheet: 579, frame: 'style', fw: 1, fh: 1 } });
740	def({ key: 'v_580_hell_butterfly_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 580, frame: 'style', fw: 2, fh: 2 } });
741	def({ key: 'v_581_lavafly_in_a_bottle', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#FF9696', drop: null, vanilla: { sheet: 581, frame: 'style', fw: 1, fh: 2 } });
742	def({ key: 'v_582_magma_snail_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 582, frame: 'style', fw: 3, fh: 2 } });
743	def({ key: 'v_590_gem_saplings', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#7F7F7F', drop: null, vanilla: { sheet: 590, frame: 'style', fw: 3, fh: 2 } }); // fw3 = 带宽 54px（原版 frameX/54 宝石序号，:72924 树苗成长判定）
744	def({ key: 'v_591_hanging_pots', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#725138', drop: null, vanilla: { sheet: 591, frame: 'style', fw: 2, fh: 3 } });
745	def({ key: 'v_595_sakura_sapling', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#976B4B', drop: null, vanilla: { sheet: 595, frame: 'style', fw: 1, fh: 2 } });
746	def({ key: 'v_599_amethyst_bunny_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 599, frame: 'style', fw: 6, fh: 3 } });
747	def({ key: 'v_600_topaz_bunny_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 600, frame: 'style', fw: 6, fh: 3 } });
748	def({ key: 'v_601_sapphire_bunny_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 601, frame: 'style', fw: 6, fh: 3 } });
749	def({ key: 'v_602_emerald_bunny_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 602, frame: 'style', fw: 6, fh: 3 } });
750	def({ key: 'v_603_ruby_bunny_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 603, frame: 'style', fw: 6, fh: 3 } });
751	def({ key: 'v_604_diamond_bunny_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 604, frame: 'style', fw: 6, fh: 3 } });
752	def({ key: 'v_605_amber_bunny_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 605, frame: 'style', fw: 6, fh: 3 } });
753	def({ key: 'v_606_amethyst_squirrel_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 606, frame: 'style', fw: 6, fh: 3 } });
754	def({ key: 'v_607_topaz_squirrel_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 607, frame: 'style', fw: 6, fh: 3 } });
755	def({ key: 'v_608_sapphire_squirrel_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 608, frame: 'style', fw: 6, fh: 3 } });
756	def({ key: 'v_609_emerald_squirrel_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 609, frame: 'style', fw: 6, fh: 3 } });
757	def({ key: 'v_610_ruby_squirrel_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 610, frame: 'style', fw: 6, fh: 3 } });
758	def({ key: 'v_611_diamond_squirrel_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 611, frame: 'style', fw: 6, fh: 3 } });
759	def({ key: 'v_612_amber_squirrel_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 612, frame: 'style', fw: 6, fh: 3 } });
760	def({ key: 'v_615_yellow_willow_sapling', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#976B4B', drop: null, vanilla: { sheet: 615, frame: 'style', fw: 1, fh: 2 } });
761	def({ key: 'v_617_relic_base', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 4, mapColor: '#E9CF5E', drop: null, vanilla: { sheet: 617, frame: 'style', fw: 3, fh: 4 } });
762	def({ key: 'v_619_truffle_worm_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 619, frame: 'style', fw: 3, fh: 2 } });
763	def({ key: 'v_620_prismatic_lacewing_jar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 620, frame: 'style', fw: 2, fh: 2 } });
764	def({ key: 'v_622_teapot', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#EBEBF9', drop: null, vanilla: { sheet: 622, frame: 'style', fw: 2, fh: 2 } });
765	def({ key: 'v_623_potted_crystal_plants', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 5, mapColor: '#DCD2F5', drop: null, vanilla: { sheet: 623, frame: 'style', fw: 2, fh: 5 } });
766	def({ key: 'v_624_abigail_s_flower', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#D25B4D', drop: null, vanilla: { sheet: 624, frame: 'style', fw: 1, fh: 1 } });
767	def({ key: 'v_626_neon_moss_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#DC0CED', blend: true, drop: null, vanilla: { sheet: 626, frame: 'auto' } });
768	def({ key: 'v_627_helium_moss_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#FF4C4C', blend: true, drop: null, vanilla: { sheet: 627, frame: 'auto' } });
769	def({ key: 'v_628_helium_moss_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#858585', blend: true, drop: null, vanilla: { sheet: 628, frame: 'auto' } });
770	def({ key: 'v_629_stinkbug_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 629, frame: 'style', fw: 3, fh: 2 } });
771	def({ key: 'v_630_stinkbug_blocker', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#759149', drop: null, vanilla: { sheet: 630, frame: 'style', fw: 1, fh: 1 } });
772	def({ key: 'v_631_ghostly_stinkbug_blocker', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#7AEAE1', drop: null, vanilla: { sheet: 631, frame: 'style', fw: 1, fh: 1 } });
773	def({ key: 'v_632_scarlet_macaw_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 632, frame: 'style', fw: 6, fh: 3 } });
774	def({ key: 'v_635_ash_wood', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#917878', blend: true, drop: null, vanilla: { sheet: 635, frame: 'auto' } });
775	def({ key: 'v_639_mana_crystal', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#6E69FF', drop: null, vanilla: { sheet: 639, frame: 'style', fw: 2, fh: 2 } });
776	def({ key: 'v_640_blue_macaw_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 640, frame: 'style', fw: 6, fh: 3 } });
777	def({ key: 'v_641_reef_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#EB7D96', blend: true, drop: null, vanilla: { sheet: 641, frame: 'auto' } });
778	def({ key: 'v_643_toucan_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 643, frame: 'style', fw: 6, fh: 3 } });
779	def({ key: 'v_644_yellow_cockatiel_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 644, frame: 'style', fw: 6, fh: 3 } });
780	def({ key: 'v_645_gray_cockatiel_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 645, frame: 'style', fw: 6, fh: 3 } });
781	def({ key: 'v_646_shadow_candle', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#6C858C', drop: null, vanilla: { sheet: 646, frame: 'style', fw: 1, fh: 1 } });
782	def({ key: 'v_647_large_rubble_3x2', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#828268', drop: null, vanilla: { sheet: 647, frame: 'style', fw: 3, fh: 2 } });
783	def({ key: 'v_648_large_rubble_3x2_group_2', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#5F7A40', drop: null, vanilla: { sheet: 648, frame: 'style', fw: 3, fh: 2 } });
784	def({ key: 'v_649_medium_rubble_2x1', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 1, mapColor: '#5C5C5C', drop: null, vanilla: { sheet: 649, frame: 'style', fw: 2, fh: 1 } });
785	def({ key: 'v_650_small_rubble_1x1', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#646464', drop: null, vanilla: { sheet: 650, frame: 'style', fw: 1, fh: 1 } });
786	def({ key: 'v_651_large_rubble_3x2_group_3', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#6BB61D', drop: null, vanilla: { sheet: 651, frame: 'style', fw: 3, fh: 2 } });
787	def({ key: 'v_652_medium_rubble_2x2', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#6BB61D', drop: null, vanilla: { sheet: 652, frame: 'style', fw: 2, fh: 2 } });
788	def({ key: 'v_653_pots_rubblemaker', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#533830', drop: null, vanilla: { sheet: 653, frame: 'style', fw: 2, fh: 2 } });
789	def({ key: 'v_654_tnt_barrel', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#C82C1C', drop: null, vanilla: { sheet: 654, frame: 'style', fw: 2, fh: 2 } });
790	def({ key: 'v_655_plantera_thorns', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#E180CE', drop: null, vanilla: { sheet: 655, frame: 'auto' } });
791	def({ key: 'v_657_echo_chamber', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#23CDD7', drop: null, vanilla: { sheet: 657, frame: 'style', fw: 2, fh: 3 } });
792	def({ key: 'v_658_aether_monolith', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#C869E6', drop: null, vanilla: { sheet: 658, frame: 'style', fw: 2, fh: 3 } });
793	def({ key: 'v_659_aetherium_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#F7E4FE', blend: true, drop: null, vanilla: { sheet: 659, frame: 'auto' } });
794	def({ key: 'v_660_faeling_in_a_bottle', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#FF9696', drop: null, vanilla: { sheet: 660, frame: 'style', fw: 1, fh: 2 } });
795	def({ key: 'v_661_corrupt_jungle_grass_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#8D89DF', blend: true, drop: null, vanilla: { sheet: 661, frame: 'auto' } });
796	def({ key: 'v_662_crimson_jungle_grass_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#D05050', blend: true, drop: null, vanilla: { sheet: 662, frame: 'auto' } });
797	def({ key: 'v_663_enchanted_moondial', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#18CBE9', drop: null, vanilla: { sheet: 663, frame: 'style', fw: 2, fh: 3 } });
798	def({ key: 'v_665_life_crystal_boulder', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#AE1845', drop: null, vanilla: { sheet: 665, frame: 'style', fw: 2, fh: 2 } });
799	def({ key: 'v_666_poo', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#733C28', blend: true, drop: null, vanilla: { sheet: 666, frame: 'auto' } });
800	def({ key: 'v_667_aetherium_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#F7E4FE', blend: true, drop: null, vanilla: { sheet: 667, frame: 'auto' } });
801	def({ key: 'v_669_lunar_rust_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#532E39', blend: true, drop: null, vanilla: { sheet: 669, frame: 'auto' } });
802	def({ key: 'v_670_dark_celestial_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#5B57A7', blend: true, drop: null, vanilla: { sheet: 670, frame: 'auto' } });
803	def({ key: 'v_671_astra_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#172151', blend: true, drop: null, vanilla: { sheet: 671, frame: 'auto' } });
804	def({ key: 'v_672_cosmic_ember_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#358567', blend: true, drop: null, vanilla: { sheet: 672, frame: 'auto' } });
805	def({ key: 'v_673_cryocore_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#0B4350', blend: true, drop: null, vanilla: { sheet: 673, frame: 'auto' } });
806	def({ key: 'v_674_mercury_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#28313C', blend: true, drop: null, vanilla: { sheet: 674, frame: 'auto' } });
807	def({ key: 'v_675_star_royale_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#150D4D', blend: true, drop: null, vanilla: { sheet: 675, frame: 'auto' } });
808	def({ key: 'v_676_heavenforge_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#C3C9D7', blend: true, drop: null, vanilla: { sheet: 676, frame: 'auto' } });
809	def({ key: 'v_677_ancient_blue_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#42546D', blend: true, drop: null, vanilla: { sheet: 677, frame: 'auto' } });
810	def({ key: 'v_678_ancient_green_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#54643F', blend: true, drop: null, vanilla: { sheet: 678, frame: 'auto' } });
811	def({ key: 'v_679_ancient_pink_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#6B4463', blend: true, drop: null, vanilla: { sheet: 679, frame: 'auto' } });
812	def({ key: 'v_680_ancient_gold_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#B9A417', blend: true, drop: null, vanilla: { sheet: 680, frame: 'auto' } });
813	def({ key: 'v_681_ancient_silver_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#B9C2C3', blend: true, drop: null, vanilla: { sheet: 681, frame: 'auto' } });
814	def({ key: 'v_682_ancient_copper_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#964316', blend: true, drop: null, vanilla: { sheet: 682, frame: 'auto' } });
815	def({ key: 'v_683_ancient_obsidian_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#645ABE', blend: true, drop: null, vanilla: { sheet: 683, frame: 'auto' } });
816	def({ key: 'v_684_ancient_hellstone_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#8E4242', blend: true, drop: null, vanilla: { sheet: 684, frame: 'auto' } });
817	def({ key: 'v_685_ancient_cobalt_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#0B508F', blend: true, drop: null, vanilla: { sheet: 685, frame: 'auto' } });
818	def({ key: 'v_686_ancient_mythril_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#5BA9A9', blend: true, drop: null, vanilla: { sheet: 686, frame: 'auto' } });
819	def({ key: 'v_687_lava_moss_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#FE7902', blend: true, drop: null, vanilla: { sheet: 687, frame: 'auto' } });
820	def({ key: 'v_688_argon_moss_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#D0007E', blend: true, drop: null, vanilla: { sheet: 688, frame: 'auto' } });
821	def({ key: 'v_689_krypton_moss_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#72FE02', blend: true, drop: null, vanilla: { sheet: 689, frame: 'auto' } });
822	def({ key: 'v_690_xenon_moss_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#00C5D0', blend: true, drop: null, vanilla: { sheet: 690, frame: 'auto' } });
823	def({ key: 'v_691_neon_moss_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#DC0CED', blend: true, drop: null, vanilla: { sheet: 691, frame: 'auto' } });
824	def({ key: 'v_692_helium_moss_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#050505', blend: true, drop: null, vanilla: { sheet: 692, frame: 'auto' } });
825	def({ key: 'v_693_mitey_titey', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#050505', drop: null, vanilla: { sheet: 693, frame: 'style', fw: 1, fh: 1 } });
826	def({ key: 'v_694_stalactite_1x2_echo', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#32323c', drop: null, vanilla: { sheet: 694, frame: 'style', fw: 1, fh: 2 } });
827	def({ key: 'v_695_replica_demon_altar', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#77657D', drop: null, vanilla: { sheet: 695, frame: 'style', fw: 3, fh: 2 } });
828	def({ key: 'v_696_replica_shadow_orb', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#8D78A8', drop: null, vanilla: { sheet: 696, frame: 'style', fw: 2, fh: 2 } });
829	def({ key: 'v_697_decorative_cobweb', name: '', decor: true, opacity: 0, pick: 0, mapColor: '#C0CACB', drop: null, vanilla: { sheet: 697, frame: 'auto' } });
830	def({ key: 'v_698_item_flask', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#C8C8C8', vanilla: { sheet: 698, frame: 'style', fw: 1, fh: 2 } });
831	def({ key: 'v_699_alchemy_flask', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 4, h: 4, mapColor: '#8D6B59', drop: null, vanilla: { sheet: 699, frame: 'style', fw: 4, fh: 4 } });
832	def({ key: 'v_700_abigails_flower_replica', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#D25B4D', drop: null, vanilla: { sheet: 700, frame: 'style', fw: 1, fh: 1 } });
833	def({ key: 'v_701_glow_tulip_replica', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#157CD4', drop: null, vanilla: { sheet: 701, frame: 'style', fw: 1, fh: 1 } });
834	def({ key: 'v_702_life_fruit_replica', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#95E857', drop: null, vanilla: { sheet: 702, frame: 'style', fw: 2, fh: 2 } });
835	def({ key: 'v_703_jungle_plants_echo', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#87C41A', drop: null, vanilla: { sheet: 703, frame: 'style', fw: 1, fh: 1 } });
836	def({ key: 'v_704_fallen_log_echo', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#7F5C45', drop: null, vanilla: { sheet: 704, frame: 'style', fw: 3, fh: 2 } });
837	def({ key: 'v_705_oasis_plants_echo', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#6BB600', drop: null, vanilla: { sheet: 705, frame: 'style', fw: 3, fh: 2 } });
838	def({ key: 'v_706_terragrim_shrine_echo', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#1cd86d', drop: null, vanilla: { sheet: 706, frame: 'style', fw: 3, fh: 2 } });
839	def({ key: 'v_707_books_echo', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#AA3072', drop: null, vanilla: { sheet: 707, frame: 'style', fw: 1, fh: 1 } });
840	def({ key: 'v_708_shimmerfall_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#EDDAF4', blend: true, drop: null, vanilla: { sheet: 708, frame: 'auto' } });
841	def({ key: 'v_709_magic_shimmer_dropper', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#F7E4FE', drop: null, vanilla: { sheet: 709, frame: 'style', fw: 1, fh: 1 } });
842	def({ key: 'v_710_pufferfish_cage', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 3, mapColor: '#7AD9E8', drop: null, vanilla: { sheet: 710, frame: 'style', fw: 6, fh: 3 } });
843	def({ key: 'v_712_poo_boulder', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 2, h: 2, mapColor: '#808080', drop: null, vanilla: { sheet: 712, frame: 'style', fw: 2, fh: 2 } });
844	def({ key: 'v_717_lava_cloud', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#7E6676', blend: true, drop: null, vanilla: { sheet: 717, frame: 'auto' } });
845	def({ key: 'v_718_star_cloud', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#F5D7C4', blend: true, drop: null, vanilla: { sheet: 718, frame: 'auto' } });
846	def({ key: 'v_719_rainbow_cloud', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#DFFFFF', blend: true, drop: null, vanilla: { sheet: 719, frame: 'auto' } });
847	def({ key: 'v_720_crt_monolith', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#A4AFAF', drop: null, vanilla: { sheet: 720, frame: 'style', fw: 2, fh: 3 } });
848	def({ key: 'v_721_retro_monolith', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#4DB090', drop: null, vanilla: { sheet: 721, frame: 'style', fw: 2, fh: 3 } });
849	def({ key: 'v_722_fallen_star_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#B9BE14', blend: true, drop: null, vanilla: { sheet: 722, frame: 'auto' } });
850	def({ key: 'v_723_kite_anchor', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#B9BE14', drop: null, vanilla: { sheet: 723, frame: 'style', fw: 1, fh: 1 } });
851	def({ key: 'v_724_critter_anchor', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#B9BE14', drop: null, vanilla: { sheet: 724, frame: 'style', fw: 1, fh: 1 } });
852	def({ key: 'v_725_film_projector', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#E54141', drop: null, vanilla: { sheet: 725, frame: 'style', fw: 2, fh: 3 } });
853	def({ key: 'v_726_cannonball', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 1, h: 1, mapColor: '#1E1E24', drop: null, vanilla: { sheet: 726, frame: 'style', fw: 1, fh: 1 } });
854	def({ key: 'v_727_dull_red_team_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#771634', blend: true, drop: null, vanilla: { sheet: 727, frame: 'auto' } });
855	def({ key: 'v_728_dull_green_team_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#17774F', blend: true, drop: null, vanilla: { sheet: 728, frame: 'auto' } });
856	def({ key: 'v_729_dull_blue_team_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#173677', blend: true, drop: null, vanilla: { sheet: 729, frame: 'auto' } });
857	def({ key: 'v_730_dull_yellow_team_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#774417', blend: true, drop: null, vanilla: { sheet: 730, frame: 'auto' } });
858	def({ key: 'v_731_dull_pink_team_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#4A1777', blend: true, drop: null, vanilla: { sheet: 731, frame: 'auto' } });
859	def({ key: 'v_732_dull_white_team_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#4E526D', blend: true, drop: null, vanilla: { sheet: 732, frame: 'auto' } });
860	def({ key: 'v_733_radio_thing', name: '', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#73451B', drop: null, vanilla: { sheet: 733, frame: 'style', fw: 3, fh: 3 } });
861	def({ key: 'v_734_feywood', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#A07350', blend: true, drop: null, vanilla: { sheet: 734, frame: 'auto' } });
862	def({ key: 'v_735_hallowed_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#EBC814', blend: true, drop: null, vanilla: { sheet: 735, frame: 'auto' } });
863	def({ key: 'v_736_easter_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#F082A0', blend: true, drop: null, vanilla: { sheet: 736, frame: 'auto' } });
864	def({ key: 'v_737_gothic_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#414B41', blend: true, drop: null, vanilla: { sheet: 737, frame: 'auto' } });
865	def({ key: 'v_738_flinx_fur_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#D2AAD7', blend: true, drop: null, vanilla: { sheet: 738, frame: 'auto' } });
866	def({ key: 'v_739_jellyfish_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#5A7DEB', blend: true, drop: null, vanilla: { sheet: 739, frame: 'auto' } });
867	def({ key: 'v_740_toybreaker_brick', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#7ad9e8', blend: true, drop: null, vanilla: { sheet: 740, frame: 'auto' } });
868	def({ key: 'v_741_pine_wood', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#A05A32', blend: true, drop: null, vanilla: { sheet: 741, frame: 'auto' } });
869	def({ key: 'v_742_harpy_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#1A8DCC', blend: true, drop: null, vanilla: { sheet: 742, frame: 'auto' } });
870	def({ key: 'v_743_moonplate_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#E3E3E3', blend: true, drop: null, vanilla: { sheet: 743, frame: 'auto' } });
871	def({ key: 'v_744_librarian_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#6A6760', blend: true, drop: null, vanilla: { sheet: 744, frame: 'auto' } });
872	def({ key: 'v_745_spike_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#78726C', blend: true, drop: null, vanilla: { sheet: 745, frame: 'auto' } });
873	def({ key: 'v_746_office_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#7A4E15', blend: true, drop: null, vanilla: { sheet: 746, frame: 'auto' } });
874	def({ key: 'v_747_forbidden_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#E7B21C', blend: true, drop: null, vanilla: { sheet: 747, frame: 'auto' } });
875	def({ key: 'v_748_aquarium_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#0272CE', blend: true, drop: null, vanilla: { sheet: 748, frame: 'auto' } });
876	def({ key: 'v_749_boulder_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#797979', blend: true, drop: null, vanilla: { sheet: 749, frame: 'auto' } });
877	def({ key: 'v_750_sharp_spike_block', name: '', solid: true, opacity: 1, pick: 0, mapColor: '#797979', blend: true, drop: null, vanilla: { sheet: 750, frame: 'auto' } });
878	TILE_DEFS.forEach((d, i) => (TILE_BY_KEY[d.key] = i));
879	
880	// ===================== 存档稳定 id(根治 TILE_DEFS 数组下标漂移;存档 v3 起生效) =====================
881	// 磁盘存"稳定 id":原版 tile 真身 = vanilla sheet id(1-752);下列自造/借用/变体 def = 私有段 1000+。
882	// 运行时仍用数组下标——SaveFile 保存/加载两个收口点经此双表映射,TILE_DEFS 顺序从此自由。
883	// ★ PRIV_TILE_STABLE 冻结表 append-only:新条目只许表尾追加,已分配号码永不复用/改派。
884	const PRIV_TILE_STABLE: Record<string, number> = {
885	  empty: 1000, leaves: 1001, table: 1002, chair: 1003, bed: 1004, bookcase: 1005,
886	  grandfather_clock: 1006, piano: 1007, dresser: 1008, bench: 1009, bathtub: 1010,
887	  keg: 1011, cooking_pot: 1012, clay_pot: 1013, tombstone_v: 1014, crystal_heart: 1015,
888	  candle: 1016, chandelier: 1017, lantern: 1018, candelabra: 1019, chinese_lantern: 1020,
889	  skull_lantern: 1021, water_candle: 1022,
890	  mushroom: 1023, flower: 1024, tallgrass: 1025,  // 自造装饰(真身 v_3_forest_short_plants 独占 sheet 3)
891	  tree: 1026,                                      // 自有树(真身 v_5_trees 独占 sheet 5)
892	  'v_389_tall_gate_open': 1027,                    // 开门态变体(真身 v_389_tallgateopen 独占 389)
893	  pixel_block: 1028,                               // 自研像素方块(F11 图片导入):RGB 编码进 frameX/Y,渲染端直画
894	  dirt: 1029,                                      // sheet=0 让位存档 air 哨兵(★曾误派 1028 与 pixel_block
895	                                                    //  冲突→pixel_block 双表被丢→图片方块群存档即变 air 丢失)
896	};
897	/** internal id → 稳定 id(保存方向;serialize 内联查表) */
898	export const TILE_STABLE_OF_INTERNAL = new Uint16Array(TILE_DEFS.length);
899	/** 稳定 id → internal id(加载方向;0=air 未映射) */
900	export const TILE_INTERNAL_OF_STABLE = new Uint16Array(2048);
901	for (let i = 1; i < TILE_DEFS.length; i++) {
902	  const d = TILE_DEFS[i];
903	  const s = PRIV_TILE_STABLE[d.key] ?? d.vanilla?.sheet;
904	  if (s === undefined || s === 0) { console.error(`[stable-id] tile 缺稳定 id: ${d.key}`); continue; }
905	  if (TILE_INTERNAL_OF_STABLE[s] !== 0) {
906	    console.error(`[stable-id] 稳定 id 冲突 ${s}: ${TILE_DEFS[TILE_INTERNAL_OF_STABLE[s]].key} / ${d.key}`);
907	    continue;
908	  }
909	  TILE_STABLE_OF_INTERNAL[i] = s;
910	  TILE_INTERNAL_OF_STABLE[s] = i;
911	}
912	
913	/** sheet(=原版 TileID) → 首个同 sheet def 的内部 tile id(-1=未注册)。
914	 *  放置回填(itemfunc.createTile → def.tile)与 wld 兜底导入共用(WldImport SHEET_FALLBACK 同语义) */
915	export const TILE_INTERNAL_BY_SHEET = new Map<number, number>();
916	/** sheet → 首个同 sheet def 的 tile key */
917	export const TILE_KEY_BY_SHEET = new Map<number, string>();
918	{
919	  for (let i = 0; i < TILE_DEFS.length; i++) {
920	    const sh = TILE_DEFS[i].vanilla?.sheet;
921	    if (sh === undefined || TILE_INTERNAL_BY_SHEET.has(sh)) continue;
922	    TILE_INTERNAL_BY_SHEET.set(sh, i);
923	    TILE_KEY_BY_SHEET.set(sh, TILE_DEFS[i].key);
924	  }
925	}
926	
927	// ===================== 墙注册表（TEdit walls.json 全量生成） =====================
928	wallDef({ id: 0, key: 'w0_none', name: '', mapColor: '#000000', opacity: 0 });
929	wallDef({ id: 1, key: 'w1_stone', name: '', mapColor: '#353535', opacity: 1 });
930	wallDef({ id: 2, key: 'w2_dirtunsafe', name: '', mapColor: '#573C30', opacity: 1 });
931	wallDef({ id: 3, key: 'w3_ebonstoneunsafe', name: '', mapColor: '#2F2935', opacity: 1 });
932	wallDef({ id: 4, key: 'w4_wood', name: '', mapColor: '#453225', opacity: 1 });
933	wallDef({ id: 5, key: 'w5_graybrick', name: '', mapColor: '#3B3B3B', opacity: 1 });
934	wallDef({ id: 6, key: 'w6_redbrick', name: '', mapColor: '#4C2C29', opacity: 1 });
935	wallDef({ id: 7, key: 'w7_bluedungeonunsafe', name: '', mapColor: '#2E3243', opacity: 1 });
936	wallDef({ id: 8, key: 'w8_greendungeonunsafe', name: '', mapColor: '#313D3D', opacity: 1 });
937	wallDef({ id: 9, key: 'w9_pinkdungeonunsafe', name: '', mapColor: '#4B2E46', opacity: 1 });
938	wallDef({ id: 10, key: 'w10_goldbrick', name: '', mapColor: '#6B5B22', opacity: 1 });
939	wallDef({ id: 11, key: 'w11_silverbrick', name: '', mapColor: '#4F5556', opacity: 1 });
940	wallDef({ id: 12, key: 'w12_copperbrick', name: '', mapColor: '#653919', opacity: 1 });
941	wallDef({ id: 13, key: 'w13_hellstonebrickunsafe', name: '', mapColor: '#4D302B', opacity: 1 });
942	wallDef({ id: 14, key: 'w14_obsidianbrickunsafe', name: '', mapColor: '#0C0C0C', opacity: 1 });
943	wallDef({ id: 15, key: 'w15_mudunsafe', name: '', mapColor: '#312B2C', opacity: 1 });
944	wallDef({ id: 16, key: 'w16_dirt', name: '', mapColor: '#513F36', opacity: 1 });
945	wallDef({ id: 17, key: 'w17_bluedungeon', name: '', mapColor: '#2E3243', opacity: 1 });
946	wallDef({ id: 18, key: 'w18_greendungeon', name: '', mapColor: '#313D3D', opacity: 1 });
947	wallDef({ id: 19, key: 'w19_pinkdungeon', name: '', mapColor: '#4B2E46', opacity: 1 });
948	wallDef({ id: 20, key: 'w20_obsidianbrick', name: '', mapColor: '#0C0C0C', opacity: 1 });
949	wallDef({ id: 21, key: 'w21_glass', name: '', mapColor: '#365962', opacity: 1 });
950	wallDef({ id: 22, key: 'w22_pearlstonebrick', name: '', mapColor: '#615C5E', opacity: 1 });
951	wallDef({ id: 23, key: 'w23_iridescentbrick', name: '', mapColor: '#382C3A', opacity: 1 });
952	wallDef({ id: 24, key: 'w24_mudstonebrick', name: '', mapColor: '#31282A', opacity: 1 });
953	wallDef({ id: 25, key: 'w25_cobaltbrick', name: '', mapColor: '#124262', opacity: 1 });
954	wallDef({ id: 26, key: 'w26_mythrilbrick', name: '', mapColor: '#224036', opacity: 1 });
955	wallDef({ id: 27, key: 'w27_planked', name: '', mapColor: '#3A302A', opacity: 1 });
956	wallDef({ id: 28, key: 'w28_pearlstonebrickunsafe', name: '', mapColor: '#4D4651', opacity: 1 });
957	wallDef({ id: 29, key: 'w29_candycane', name: '', mapColor: '#703A44', opacity: 1 });
958	wallDef({ id: 30, key: 'w30_greencandycane', name: '', mapColor: '#387350', opacity: 1 });
959	wallDef({ id: 31, key: 'w31_snowbrick', name: '', mapColor: '#5E656C', opacity: 1 });
960	wallDef({ id: 32, key: 'w32_adamantitebeam', name: '', mapColor: '#661430', opacity: 1 });
961	wallDef({ id: 33, key: 'w33_demonitebrick', name: '', mapColor: '#303049', opacity: 1 });
962	wallDef({ id: 34, key: 'w34_sandstonebrick', name: '', mapColor: '#565339', opacity: 1 });
963	wallDef({ id: 35, key: 'w35_ebonstonebrick', name: '', mapColor: '#363B52', opacity: 1 });
964	wallDef({ id: 36, key: 'w36_redstucco', name: '', mapColor: '#7C463F', opacity: 1 });
965	wallDef({ id: 37, key: 'w37_yellowstucco', name: '', mapColor: '#595437', opacity: 1 });
966	wallDef({ id: 38, key: 'w38_greenstucco', name: '', mapColor: '#3C5A46', opacity: 1 });
967	wallDef({ id: 39, key: 'w39_gray', name: '', mapColor: '#595954', opacity: 1 });
968	wallDef({ id: 40, key: 'w40_snowwallunsafe', name: '', mapColor: '#647681', opacity: 1 });
969	wallDef({ id: 41, key: 'w41_ebonwood', name: '', mapColor: '#393740', opacity: 1 });
970	wallDef({ id: 42, key: 'w42_richmaogany', name: '', mapColor: '#3E191B', opacity: 1 });
971	wallDef({ id: 43, key: 'w43_pearlwood', name: '', mapColor: '#3C372C', opacity: 1 });
972	wallDef({ id: 44, key: 'w44_rainbowbrick', name: '', mapColor: '#333333', opacity: 1 });
973	wallDef({ id: 45, key: 'w45_tinbrick', name: '', mapColor: '#413F39', opacity: 1 });
974	wallDef({ id: 46, key: 'w46_tungstenbrick', name: '', mapColor: '#445345', opacity: 1 });
975	wallDef({ id: 47, key: 'w47_platinumbrick', name: '', mapColor: '#424652', opacity: 1 });
976	wallDef({ id: 48, key: 'w48_amethystunsafe', name: '', mapColor: '#4E4553', opacity: 1 });
977	wallDef({ id: 49, key: 'w49_topazunsafe', name: '', mapColor: '#514A3F', opacity: 1 });
978	wallDef({ id: 50, key: 'w50_sapphireunsafe', name: '', mapColor: '#384251', opacity: 1 });
979	wallDef({ id: 51, key: 'w51_emeraldunsafe', name: '', mapColor: '#32493B', opacity: 1 });
980	wallDef({ id: 52, key: 'w52_rubyunsafe', name: '', mapColor: '#523B40', opacity: 1 });
981	wallDef({ id: 53, key: 'w53_diamondunsafe', name: '', mapColor: '#464F51', opacity: 1 });
982	wallDef({ id: 54, key: 'w54_caveunsafe', name: '', mapColor: '#2E3A36', opacity: 1 });
983	wallDef({ id: 55, key: 'w55_cave2unsafe', name: '', mapColor: '#38382E', opacity: 1 });
984	wallDef({ id: 56, key: 'w56_cave3unsafe', name: '', mapColor: '#393131', opacity: 1 });
985	wallDef({ id: 57, key: 'w57_cave4unsafe', name: '', mapColor: '#2D3338', opacity: 1 });
986	wallDef({ id: 58, key: 'w58_cave5unsafe', name: '', mapColor: '#38303B', opacity: 1 });
987	wallDef({ id: 59, key: 'w59_cave6unsafe', name: '', mapColor: '#503F37', opacity: 1 });
988	wallDef({ id: 60, key: 'w60_livingleaf', name: '', mapColor: '#003111', opacity: 1 });
989	wallDef({ id: 61, key: 'w61_cave7unsafe', name: '', mapColor: '#37281C', opacity: 1 });
990	wallDef({ id: 62, key: 'w62_spiderunsafe', name: '', mapColor: '#201C16', opacity: 1 });
991	wallDef({ id: 63, key: 'w63_grassunsafe', name: '', mapColor: '#194326', opacity: 1 });
992	wallDef({ id: 64, key: 'w64_jungleunsafe', name: '', mapColor: '#2F4319', opacity: 1 });
993	wallDef({ id: 65, key: 'w65_flowerunsafe', name: '', mapColor: '#194326', opacity: 1 });
994	wallDef({ id: 66, key: 'w66_grass', name: '', mapColor: '#194326', opacity: 1 });
995	wallDef({ id: 67, key: 'w67_jungle', name: '', mapColor: '#2F4319', opacity: 1 });
996	wallDef({ id: 68, key: 'w68_flower', name: '', mapColor: '#194326', opacity: 1 });
997	wallDef({ id: 69, key: 'w69_corruptgrassunsafe', name: '', mapColor: '#242539', opacity: 1 });
998	wallDef({ id: 70, key: 'w70_hallowedgrassunsafe', name: '', mapColor: '#193D43', opacity: 1 });
999	wallDef({ id: 71, key: 'w71_iceunsafe', name: '', mapColor: '#526C86', opacity: 1 });
1000	wallDef({ id: 72, key: 'w72_cactus', name: '', mapColor: '#2D5418', opacity: 1 });
1001	wallDef({ id: 73, key: 'w73_cloud', name: '', mapColor: '#D3D9DB', opacity: 1 });
1002	wallDef({ id: 74, key: 'w74_mushroom', name: '', mapColor: '#363C71', opacity: 1 });
1003	wallDef({ id: 75, key: 'w75_bone', name: '', mapColor: '#3D3D2C', opacity: 1 });
1004	wallDef({ id: 76, key: 'w76_slime', name: '', mapColor: '#1A336F', opacity: 1 });
1005	wallDef({ id: 77, key: 'w77_flesh', name: '', mapColor: '#4B1216', opacity: 1 });
1006	wallDef({ id: 78, key: 'w78_livingwood', name: '', mapColor: '#3A2318', opacity: 1 });
1007	wallDef({ id: 79, key: 'w79_obsidianbackunsafe', name: '', mapColor: '#242141', opacity: 1 });
1008	wallDef({ id: 80, key: 'w80_mushroomunsafe', name: '', mapColor: '#363C71', opacity: 1 });
1009	wallDef({ id: 81, key: 'w81_crimsongrassunsafe', name: '', mapColor: '#653434', opacity: 1 });
1010	wallDef({ id: 82, key: 'w82_discwall', name: '', mapColor: '#381300', opacity: 1 });
1011	wallDef({ id: 83, key: 'w83_crimstoneunsafe', name: '', mapColor: '#3E2C2D', opacity: 1 });
1012	wallDef({ id: 84, key: 'w84_icebrick', name: '', mapColor: '#4E6983', opacity: 1 });
1013	wallDef({ id: 85, key: 'w85_shadewood', name: '', mapColor: '#20272D', opacity: 1 });
1014	wallDef({ id: 86, key: 'w86_hiveunsafe', name: '', mapColor: '#795024', opacity: 1 });
1015	wallDef({ id: 87, key: 'w87_lihzahrdbrickunsafe', name: '', mapColor: '#1C080A', opacity: 1 });
1016	wallDef({ id: 88, key: 'w88_purplestainedglass', name: '', mapColor: '#73447C', opacity: 1 });
1017	wallDef({ id: 89, key: 'w89_yellowstainedglass', name: '', mapColor: '#81724A', opacity: 1 });
1018	wallDef({ id: 90, key: 'w90_bluestainedglass', name: '', mapColor: '#3E567B', opacity: 1 });
1019	wallDef({ id: 91, key: 'w91_greenstainedglass', name: '', mapColor: '#5A795E', opacity: 1 });
1020	wallDef({ id: 92, key: 'w92_redstainedglass', name: '', mapColor: '#873E3D', opacity: 1 });
1021	wallDef({ id: 93, key: 'w93_rainbowstainedglass', name: '', mapColor: '#646067', opacity: 1 });
1022	wallDef({ id: 94, key: 'w94_bluedungeonslabunsafe', name: '', mapColor: '#243039', opacity: 1 });
1023	wallDef({ id: 95, key: 'w95_bluedungeontileunsafe', name: '', mapColor: '#302E3A', opacity: 1 });
1024	wallDef({ id: 96, key: 'w96_pinkdungeonslabunsafe', name: '', mapColor: '#472E49', opacity: 1 });
1025	wallDef({ id: 97, key: 'w97_pinkdungeontileunsafe', name: '', mapColor: '#4C2E40', opacity: 1 });
1026	wallDef({ id: 98, key: 'w98_greendungeonslabunsafe', name: '', mapColor: '#333F39', opacity: 1 });
1027	wallDef({ id: 99, key: 'w99_greendungeontileunsafe', name: '', mapColor: '#313A40', opacity: 1 });
1028	wallDef({ id: 100, key: 'w100_bluedungeonslab', name: '', mapColor: '#243039', opacity: 1 });
1029	wallDef({ id: 101, key: 'w101_bluedungeontile', name: '', mapColor: '#302E3A', opacity: 1 });
1030	wallDef({ id: 102, key: 'w102_pinkdungeonslab', name: '', mapColor: '#472E49', opacity: 1 });
1031	wallDef({ id: 103, key: 'w103_pinkdungeontile', name: '', mapColor: '#4C2E40', opacity: 1 });
1032	wallDef({ id: 104, key: 'w104_greendungeonslab', name: '', mapColor: '#333F39', opacity: 1 });
1033	wallDef({ id: 105, key: 'w105_greendungeontile', name: '', mapColor: '#313A40', opacity: 1 });
1034	wallDef({ id: 106, key: 'w106_woodenfence', name: '', mapColor: '#614833', opacity: 1 });
1035	wallDef({ id: 107, key: 'w107_metalfence', name: '', mapColor: '#353535', opacity: 1 });
1036	wallDef({ id: 108, key: 'w108_hive', name: '', mapColor: '#795024', opacity: 1 });
1037	wallDef({ id: 109, key: 'w109_palladiumcolumn', name: '', mapColor: '#6E2513', opacity: 1 });
1038	wallDef({ id: 110, key: 'w110_bubblegumblock', name: '', mapColor: '#873989', opacity: 1 });
1039	wallDef({ id: 111, key: 'w111_titanstoneblock', name: '', mapColor: '#211915', opacity: 1 });
1040	wallDef({ id: 112, key: 'w112_lihzahrdbrick', name: '', mapColor: '#1C080A', opacity: 1 });
1041	wallDef({ id: 113, key: 'w113_pumpkin', name: '', mapColor: '#A04B07', opacity: 1 });
1042	wallDef({ id: 114, key: 'w114_hay', name: '', mapColor: '#362A13', opacity: 1 });
1043	wallDef({ id: 115, key: 'w115_spookywood', name: '', mapColor: '#2A1E35', opacity: 1 });
1044	wallDef({ id: 116, key: 'w116_christmastreewallpaper', name: '', mapColor: '#3C2219', opacity: 1 });
1045	wallDef({ id: 117, key: 'w117_ornamentwallpaper', name: '', mapColor: '#5B5340', opacity: 1 });
1046	wallDef({ id: 118, key: 'w118_candycanewallpaper', name: '', mapColor: '#3B3D36', opacity: 1 });
1047	wallDef({ id: 119, key: 'w119_festivewallpaper', name: '', mapColor: '#2F2719', opacity: 1 });
1048	wallDef({ id: 120, key: 'w120_starswallpaper', name: '', mapColor: '#50586F', opacity: 1 });
1049	wallDef({ id: 121, key: 'w121_squiggleswallpaper', name: '', mapColor: '#BAA78A', opacity: 1 });
1050	wallDef({ id: 122, key: 'w122_snowflakewallpaper', name: '', mapColor: '#6E778F', opacity: 1 });
1051	wallDef({ id: 123, key: 'w123_krampushornwallpaper', name: '', mapColor: '#8A806E', opacity: 1 });
1052	wallDef({ id: 124, key: 'w124_bluegreenwallpaper', name: '', mapColor: '#07301E', opacity: 1 });
1053	wallDef({ id: 125, key: 'w125_grinchfingerwallpaper', name: '', mapColor: '#4E6746', opacity: 1 });
1054	wallDef({ id: 126, key: 'w126_fancygraywallpaper', name: '', mapColor: '#6D6F7B', opacity: 1 });
1055	wallDef({ id: 127, key: 'w127_icefloewallpaper', name: '', mapColor: '#70A6E2', opacity: 1 });
1056	wallDef({ id: 128, key: 'w128_musicwallpaper', name: '', mapColor: '#45388C', opacity: 1 });
1057	wallDef({ id: 129, key: 'w129_purplerainwallpaper', name: '', mapColor: '#482C91', opacity: 1 });
1058	wallDef({ id: 130, key: 'w130_rainbowwallpaper', name: '', mapColor: '#725579', opacity: 1 });
1059	wallDef({ id: 131, key: 'w131_sparklestonewallpaper', name: '', mapColor: '#68779E', opacity: 1 });
1060	wallDef({ id: 132, key: 'w132_starlitheavenwallpaper', name: '', mapColor: '#4A4A4A', opacity: 1 });
1061	wallDef({ id: 133, key: 'w133_bubblewallpaper', name: '', mapColor: '#5F77BF', opacity: 1 });
1062	wallDef({ id: 134, key: 'w134_copperpipewallpaper', name: '', mapColor: '#904F16', opacity: 1 });
1063	wallDef({ id: 135, key: 'w135_duckywallpaper', name: '', mapColor: '#3E828A', opacity: 1 });
1064	wallDef({ id: 136, key: 'w136_waterfall', name: '', mapColor: '#3D62A9', opacity: 1 });
1065	wallDef({ id: 137, key: 'w137_lavafall', name: '', mapColor: '#B7540E', opacity: 1 });
1066	wallDef({ id: 138, key: 'w138_ebonwoodfence', name: '', mapColor: '#3D3945', opacity: 1 });
1067	wallDef({ id: 139, key: 'w139_richmahoganyfence', name: '', mapColor: '#4A2022', opacity: 1 });
1068	wallDef({ id: 140, key: 'w140_pearlwoodfence', name: '', mapColor: '#6E644C', opacity: 1 });
1069	wallDef({ id: 141, key: 'w141_shadewoodfence', name: '', mapColor: '#42463C', opacity: 1 });
1070	wallDef({ id: 142, key: 'w142_whitedynasty', name: '', mapColor: '#D6CEBB', opacity: 1 });
1071	wallDef({ id: 143, key: 'w143_bluedynasty', name: '', mapColor: '#536A63', opacity: 1 });
1072	wallDef({ id: 144, key: 'w144_arcanerunes', name: '', mapColor: '#594344', opacity: 1 });
1073	wallDef({ id: 145, key: 'w145_ironfence', name: '', mapColor: '#787878', opacity: 1 });
1074	wallDef({ id: 146, key: 'w146_copperplating', name: '', mapColor: '#673718', opacity: 1, largeFrame: 1 });
1075	wallDef({ id: 147, key: 'w147_stoneslab', name: '', mapColor: '#4D4D4D', opacity: 1, largeFrame: 1 });
1076	wallDef({ id: 148, key: 'w148_sail', name: '', mapColor: '#E5DAA1', opacity: 1 });
1077	wallDef({ id: 149, key: 'w149_borealwood', name: '', mapColor: '#524641', opacity: 1 });
1078	wallDef({ id: 150, key: 'w150_borealwoodfence', name: '', mapColor: '#51453E', opacity: 1 });
1079	wallDef({ id: 151, key: 'w151_palmwood', name: '', mapColor: '#674C24', opacity: 1 });
1080	wallDef({ id: 152, key: 'w152_palmwoodfence', name: '', mapColor: '#674C24', opacity: 1 });
1081	wallDef({ id: 153, key: 'w153_ambergemspark', name: '', mapColor: '#FF743F', opacity: 1 });
1082	wallDef({ id: 154, key: 'w154_amethystgemspark', name: '', mapColor: '#BF3FFF', opacity: 1 });
1083	wallDef({ id: 155, key: 'w155_diamondgemspark', name: '', mapColor: '#DBDBE8', opacity: 1 });
1084	wallDef({ id: 156, key: 'w156_emeraldgemspark', name: '', mapColor: '#3FFF47', opacity: 1 });
1085	wallDef({ id: 157, key: 'w157_ambergemsparkoff', name: '', mapColor: '#763F25', opacity: 1 });
1086	wallDef({ id: 158, key: 'w158_amethystgemsparkoff', name: '', mapColor: '#512576', opacity: 1 });
1087	wallDef({ id: 159, key: 'w159_diamondgemsparkoff', name: '', mapColor: '#404359', opacity: 1 });
1088	wallDef({ id: 160, key: 'w160_emeraldgemsparkoff', name: '', mapColor: '#257634', opacity: 1 });
1089	wallDef({ id: 161, key: 'w161_rubygemsparkoff', name: '', mapColor: '#76253A', opacity: 1 });
1090	wallDef({ id: 162, key: 'w162_sapphiregemsparkoff', name: '', mapColor: '#252576', opacity: 1 });
1091	wallDef({ id: 163, key: 'w163_topazgemsparkoff', name: '', mapColor: '#767125', opacity: 1 });
1092	wallDef({ id: 164, key: 'w164_rubygemspark', name: '', mapColor: '#FF3F3F', opacity: 1 });
1093	wallDef({ id: 165, key: 'w165_sapphiregemspark', name: '', mapColor: '#3F51FF', opacity: 1 });
1094	wallDef({ id: 166, key: 'w166_topazgemspark', name: '', mapColor: '#EFFF3F', opacity: 1 });
1095	wallDef({ id: 167, key: 'w167_tinplating', name: '', mapColor: '#4E4D3A', opacity: 1, largeFrame: 1 });
1096	wallDef({ id: 168, key: 'w168_confetti', name: '', mapColor: '#546154', opacity: 1 });
1097	wallDef({ id: 169, key: 'w169_confettiblack', name: '', mapColor: '#5C695A', opacity: 1 });
1098	wallDef({ id: 170, key: 'w170_cavewall', name: '', mapColor: '#5D442F', opacity: 1 });
1099	wallDef({ id: 171, key: 'w171_cavewall2', name: '', mapColor: '#543C27', opacity: 1 });
1100	wallDef({ id: 172, key: 'w172_honeyfall', name: '', mapColor: '#A87D00', opacity: 1 });
1101	wallDef({ id: 173, key: 'w173_chlorophytebrick', name: '', mapColor: '#316919', opacity: 1 });
1102	wallDef({ id: 174, key: 'w174_crimtanebrick', name: '', mapColor: '#453036', opacity: 1 });
1103	wallDef({ id: 175, key: 'w175_shroomiteplating', name: '', mapColor: '#2132BC', opacity: 1 });
1104	wallDef({ id: 176, key: 'w176_martianconduit', name: '', mapColor: '#4B8094', opacity: 1 });
1105	wallDef({ id: 177, key: 'w177_hellstonebrick', name: '', mapColor: '#48322E', opacity: 1 });
1106	wallDef({ id: 178, key: 'w178_marbleunsafe', name: '', mapColor: '#787F8F', opacity: 1 });
1107	wallDef({ id: 179, key: 'w179_marbleblock', name: '', mapColor: '#7C8394', opacity: 1, largeFrame: 1 });
1108	wallDef({ id: 180, key: 'w180_graniteunsafe', name: '', mapColor: '#0F102D', opacity: 1 });
1109	wallDef({ id: 181, key: 'w181_graniteblock', name: '', mapColor: '#1F1F4A', opacity: 1 });
1110	wallDef({ id: 182, key: 'w182_meteoritebrick', name: '', mapColor: '#393763', opacity: 1 });
1111	wallDef({ id: 183, key: 'w183_marble', name: '', mapColor: '#787F8F', opacity: 1 });
1112	wallDef({ id: 184, key: 'w184_granite', name: '', mapColor: '#0F102D', opacity: 1 });
1113	wallDef({ id: 185, key: 'w185_cave8unsafe', name: '', mapColor: '#3D3D3D', opacity: 1, largeFrame: 2 });
1114	wallDef({ id: 186, key: 'w186_crystal', name: '', mapColor: '#371764', opacity: 1 });
1115	wallDef({ id: 187, key: 'w187_sandstone', name: '', mapColor: '#7E442B', opacity: 1 });
1116	wallDef({ id: 188, key: 'w188_corruptionunsafe1', name: '', mapColor: '#3F2F3F', opacity: 1 });
1117	wallDef({ id: 189, key: 'w189_corruptionunsafe2', name: '', mapColor: '#41334D', opacity: 1 });
1118	wallDef({ id: 190, key: 'w190_corruptionunsafe3', name: '', mapColor: '#43483B', opacity: 1 });
1119	wallDef({ id: 191, key: 'w191_corruptionunsafe4', name: '', mapColor: '#3C2643', opacity: 1 });
1120	wallDef({ id: 192, key: 'w192_crimsonunsafe1', name: '', mapColor: '#7B382F', opacity: 1 });
1121	wallDef({ id: 193, key: 'w193_crimsonunsafe2', name: '', mapColor: '#57181A', opacity: 1 });
1122	wallDef({ id: 194, key: 'w194_crimsonunsafe3', name: '', mapColor: '#664035', opacity: 1 });
1123	wallDef({ id: 195, key: 'w195_crimsonunsafe4', name: '', mapColor: '#7A2E36', opacity: 1 });
1124	wallDef({ id: 196, key: 'w196_dirtunsafe1', name: '', mapColor: '#634637', opacity: 1 });
1125	wallDef({ id: 197, key: 'w197_dirtunsafe2', name: '', mapColor: '#664939', opacity: 1 });
1126	wallDef({ id: 198, key: 'w198_dirtunsafe3', name: '', mapColor: '#5C4131', opacity: 1 });
1127	wallDef({ id: 199, key: 'w199_dirtunsafe4', name: '', mapColor: '#6A4B3A', opacity: 1 });
1128	wallDef({ id: 200, key: 'w200_hallowunsafe1', name: '', mapColor: '#512153', opacity: 1 });
1129	wallDef({ id: 201, key: 'w201_hallowunsafe2', name: '', mapColor: '#604F63', opacity: 1 });
1130	wallDef({ id: 202, key: 'w202_hallowunsafe3', name: '', mapColor: '#7C2A68', opacity: 1 });
1131	wallDef({ id: 203, key: 'w203_hallowunsafe4', name: '', mapColor: '#6F3670', opacity: 1 });
1132	wallDef({ id: 204, key: 'w204_jungleunsafe1', name: '', mapColor: '#4B4437', opacity: 1 });
1133	wallDef({ id: 205, key: 'w205_jungleunsafe2', name: '', mapColor: '#53533B', opacity: 1 });
1134	wallDef({ id: 206, key: 'w206_jungleunsafe3', name: '', mapColor: '#27432C', opacity: 1 });
1135	wallDef({ id: 207, key: 'w207_jungleunsafe4', name: '', mapColor: '#4D4D37', opacity: 1 });
1136	wallDef({ id: 208, key: 'w208_lavaunsafe1', name: '', mapColor: '#5C241C', opacity: 1 });
1137	wallDef({ id: 209, key: 'w209_lavaunsafe2', name: '', mapColor: '#603027', opacity: 1 });
1138	wallDef({ id: 210, key: 'w210_lavaunsafe3', name: '', mapColor: '#6C2C1A', opacity: 1 });
1139	wallDef({ id: 211, key: 'w211_lavaunsafe4', name: '', mapColor: '#6A2A26', opacity: 1 });
1140	wallDef({ id: 212, key: 'w212_rocksunsafe1', name: '', mapColor: '#46453D', opacity: 1 });
1141	wallDef({ id: 213, key: 'w213_rocksunsafe2', name: '', mapColor: '#393C39', opacity: 1 });
1142	wallDef({ id: 214, key: 'w214_rocksunsafe3', name: '', mapColor: '#45393B', opacity: 1 });
1143	wallDef({ id: 215, key: 'w215_rocksunsafe4', name: '', mapColor: '#473C42', opacity: 1 });
1144	wallDef({ id: 216, key: 'w216_hardenedsand', name: '', mapColor: '#945D34', opacity: 1 });
1145	wallDef({ id: 217, key: 'w217_corrupthardenedsand', name: '', mapColor: '#332641', opacity: 1 });
1146	wallDef({ id: 218, key: 'w218_crimsonhardenedsand', name: '', mapColor: '#2B1816', opacity: 1 });
1147	wallDef({ id: 219, key: 'w219_hallowhardenedsand', name: '', mapColor: '#4E4972', opacity: 1 });
1148	wallDef({ id: 220, key: 'w220_corruptsandstone', name: '', mapColor: '#362444', opacity: 1 });
1149	wallDef({ id: 221, key: 'w221_crimsonsandstone', name: '', mapColor: '#49120C', opacity: 1 });
1150	wallDef({ id: 222, key: 'w222_hallowsandstone', name: '', mapColor: '#3A2F51', opacity: 1 });
1151	wallDef({ id: 223, key: 'w223_desertfossil', name: '', mapColor: '#734122', opacity: 1 });
1152	wallDef({ id: 224, key: 'w224_lunarbrickwall', name: '', mapColor: '#677068', opacity: 1, largeFrame: 2 });
1153	wallDef({ id: 225, key: 'w225_cogwall', name: '', mapColor: '#4C4738', opacity: 1 });
1154	wallDef({ id: 226, key: 'w226_sandfall', name: '', mapColor: '#857C42', opacity: 1 });
1155	wallDef({ id: 227, key: 'w227_snowfall', name: '', mapColor: '#536570', opacity: 1 });
1156	wallDef({ id: 228, key: 'w228_sillyballoonpinkwall', name: '', mapColor: '#8B0040', opacity: 1 });
1157	wallDef({ id: 229, key: 'w229_sillyballoonpurplewall', name: '', mapColor: '#500CA2', opacity: 1 });
1158	wallDef({ id: 230, key: 'w230_sillyballoongreenwall', name: '', mapColor: '#005D51', opacity: 1 });
1159	wallDef({ id: 231, key: 'w231_ironbrick', name: '', mapColor: '#51443E', opacity: 1 });
1160	wallDef({ id: 232, key: 'w232_leadbrick', name: '', mapColor: '#252F39', opacity: 1 });
1161	wallDef({ id: 233, key: 'w233_lesionblock', name: '', mapColor: '#483537', opacity: 1 });
1162	wallDef({ id: 234, key: 'w234_crimstonebrick', name: '', mapColor: '#672E30', opacity: 1 });
1163	wallDef({ id: 235, key: 'w235_smoothsandstone', name: '', mapColor: '#7E442B', opacity: 1 });
1164	wallDef({ id: 236, key: 'w236_spider', name: '', mapColor: '#3F2322', opacity: 1 });
1165	wallDef({ id: 237, key: 'w237_solarbrick', name: '', mapColor: '#392221', opacity: 1 });
1166	wallDef({ id: 238, key: 'w238_vortexbrick', name: '', mapColor: '#2D2E36', opacity: 1 });
1167	wallDef({ id: 239, key: 'w239_nebulabrick', name: '', mapColor: '#2B3438', opacity: 1 });
1168	wallDef({ id: 240, key: 'w240_stardustbrick', name: '', mapColor: '#3E2D21', opacity: 1 });
1169	wallDef({ id: 241, key: 'w241_orangestainedglass', name: '', mapColor: '#925F35', opacity: 1 });
1170	wallDef({ id: 242, key: 'w242_goldstarryglasswall', name: '', mapColor: '#4E4537', opacity: 1 });
1171	wallDef({ id: 243, key: 'w243_bluestarryglasswall', name: '', mapColor: '#173456', opacity: 1 });
1172	wallDef({ id: 244, key: 'w244_livingwoodunsafe', name: '', mapColor: '#3A2318', opacity: 1 });
1173	wallDef({ id: 245, key: 'w245_wroughtironfence', name: '', mapColor: '#4A4A4A', opacity: 1 });
1174	wallDef({ id: 246, key: 'w246_ebonstoneecho', name: '', mapColor: '#2F2935', opacity: 1 });
1175	wallDef({ id: 247, key: 'w247_mudwallecho', name: '', mapColor: '#312B2C', opacity: 1 });
1176	wallDef({ id: 248, key: 'w248_pearlstoneecho', name: '', mapColor: '#4D4651', opacity: 1 });
1177	wallDef({ id: 249, key: 'w249_snowwallecho', name: '', mapColor: '#647681', opacity: 1 });
1178	wallDef({ id: 250, key: 'w250_amethystecho', name: '', mapColor: '#4E4553', opacity: 1 });
1179	wallDef({ id: 251, key: 'w251_topazecho', name: '', mapColor: '#514A3F', opacity: 1 });
1180	wallDef({ id: 252, key: 'w252_sapphireecho', name: '', mapColor: '#384251', opacity: 1 });
1181	wallDef({ id: 253, key: 'w253_emeraldecho', name: '', mapColor: '#32493B', opacity: 1 });
1182	wallDef({ id: 254, key: 'w254_rubyecho', name: '', mapColor: '#523B40', opacity: 1 });
1183	wallDef({ id: 255, key: 'w255_diamondecho', name: '', mapColor: '#464F51', opacity: 1 });
1184	wallDef({ id: 256, key: 'w256_cave1echo', name: '', mapColor: '#2E3A36', opacity: 1 });
1185	wallDef({ id: 257, key: 'w257_cave2echo', name: '', mapColor: '#38382E', opacity: 1 });
1186	wallDef({ id: 258, key: 'w258_cave3echo', name: '', mapColor: '#393131', opacity: 1 });
1187	wallDef({ id: 259, key: 'w259_cave4echo', name: '', mapColor: '#2D3338', opacity: 1 });
1188	wallDef({ id: 260, key: 'w260_cave5echo', name: '', mapColor: '#38303B', opacity: 1 });
1189	wallDef({ id: 261, key: 'w261_cave6echo', name: '', mapColor: '#503F37', opacity: 1 });
1190	wallDef({ id: 262, key: 'w262_cave7echo', name: '', mapColor: '#37281C', opacity: 1 });
1191	wallDef({ id: 263, key: 'w263_spiderecho', name: '', mapColor: '#201C16', opacity: 1 });
1192	wallDef({ id: 264, key: 'w264_corruptgrassecho', name: '', mapColor: '#242539', opacity: 1 });
1193	wallDef({ id: 265, key: 'w265_hallowedgrassecho', name: '', mapColor: '#193D43', opacity: 1 });
1194	wallDef({ id: 266, key: 'w266_iceecho', name: '', mapColor: '#526C86', opacity: 1 });
1195	wallDef({ id: 267, key: 'w267_obsidianbackecho', name: '', mapColor: '#242141', opacity: 1 });
1196	wallDef({ id: 268, key: 'w268_crimsongrassecho', name: '', mapColor: '#653434', opacity: 1 });
1197	wallDef({ id: 269, key: 'w269_crimstoneecho', name: '', mapColor: '#3E2C2D', opacity: 1 });
1198	wallDef({ id: 270, key: 'w270_cavewall1echo', name: '', mapColor: '#5D442F', opacity: 1 });
1199	wallDef({ id: 271, key: 'w271_cavewall2echo', name: '', mapColor: '#543C27', opacity: 1 });
1200	wallDef({ id: 272, key: 'w272_marbleechounused', name: '', mapColor: '#787F8F', opacity: 1 });
1201	wallDef({ id: 273, key: 'w273_graniteechounused', name: '', mapColor: '#0F102D', opacity: 1 });
1202	wallDef({ id: 274, key: 'w274_cave8echo', name: '', mapColor: '#3D3D3D', opacity: 1, largeFrame: 2 });
1203	wallDef({ id: 275, key: 'w275_sandstoneecho', name: '', mapColor: '#7E442B', opacity: 1 });
1204	wallDef({ id: 276, key: 'w276_corruption1echo', name: '', mapColor: '#3F2F3F', opacity: 1 });
1205	wallDef({ id: 277, key: 'w277_corruption2echo', name: '', mapColor: '#41334D', opacity: 1 });
1206	wallDef({ id: 278, key: 'w278_corruption3echo', name: '', mapColor: '#43483B', opacity: 1 });
1207	wallDef({ id: 279, key: 'w279_corruption4echo', name: '', mapColor: '#3C2643', opacity: 1 });
1208	wallDef({ id: 280, key: 'w280_crimson1echo', name: '', mapColor: '#7B382F', opacity: 1 });
1209	wallDef({ id: 281, key: 'w281_crimson2echo', name: '', mapColor: '#57181A', opacity: 1 });
1210	wallDef({ id: 282, key: 'w282_crimson3echo', name: '', mapColor: '#664035', opacity: 1 });
1211	wallDef({ id: 283, key: 'w283_crimson4echo', name: '', mapColor: '#7A2E36', opacity: 1 });
1212	wallDef({ id: 284, key: 'w284_dirt1echo', name: '', mapColor: '#634637', opacity: 1 });
1213	wallDef({ id: 285, key: 'w285_dirt2echo', name: '', mapColor: '#664939', opacity: 1 });
1214	wallDef({ id: 286, key: 'w286_dirt3echo', name: '', mapColor: '#5C4131', opacity: 1 });
1215	wallDef({ id: 287, key: 'w287_dirt4echo', name: '', mapColor: '#6A4B3A', opacity: 1 });
1216	wallDef({ id: 288, key: 'w288_hallow1echo', name: '', mapColor: '#512153', opacity: 1 });
1217	wallDef({ id: 289, key: 'w289_hallow2echo', name: '', mapColor: '#604F63', opacity: 1 });
1218	wallDef({ id: 290, key: 'w290_hallow3echo', name: '', mapColor: '#7C2A68', opacity: 1 });
1219	wallDef({ id: 291, key: 'w291_hallow4echo', name: '', mapColor: '#6F3670', opacity: 1 });
1220	wallDef({ id: 292, key: 'w292_jungle1echo', name: '', mapColor: '#4B4437', opacity: 1 });
1221	wallDef({ id: 293, key: 'w293_jungle2echo', name: '', mapColor: '#53533B', opacity: 1 });
1222	wallDef({ id: 294, key: 'w294_jungle3echo', name: '', mapColor: '#27432C', opacity: 1 });
1223	wallDef({ id: 295, key: 'w295_jungle4echo', name: '', mapColor: '#4D4D37', opacity: 1 });
1224	wallDef({ id: 296, key: 'w296_lava1echo', name: '', mapColor: '#5C241C', opacity: 1 });
1225	wallDef({ id: 297, key: 'w297_lava2echo', name: '', mapColor: '#603027', opacity: 1 });
1226	wallDef({ id: 298, key: 'w298_lava3echo', name: '', mapColor: '#6C2C1A', opacity: 1 });
1227	wallDef({ id: 299, key: 'w299_lava4echo', name: '', mapColor: '#6A2A26', opacity: 1 });
1228	wallDef({ id: 300, key: 'w300_rocks1echo', name: '', mapColor: '#46453D', opacity: 1 });
1229	wallDef({ id: 301, key: 'w301_rocks2echo', name: '', mapColor: '#393C39', opacity: 1 });
1230	wallDef({ id: 302, key: 'w302_rocks3echo', name: '', mapColor: '#45393B', opacity: 1 });
1231	wallDef({ id: 303, key: 'w303_rocks4echo', name: '', mapColor: '#473C42', opacity: 1 });
1232	wallDef({ id: 304, key: 'w304_hardenedsandecho', name: '', mapColor: '#945D34', opacity: 1 });
1233	wallDef({ id: 305, key: 'w305_corrupthardenedsandecho', name: '', mapColor: '#332641', opacity: 1 });
1234	wallDef({ id: 306, key: 'w306_crimsonhardenedsandecho', name: '', mapColor: '#2B1816', opacity: 1 });
1235	wallDef({ id: 307, key: 'w307_hallowhardenedsandecho', name: '', mapColor: '#4E4972', opacity: 1 });
1236	wallDef({ id: 308, key: 'w308_corruptsandstoneecho', name: '', mapColor: '#362444', opacity: 1 });
1237	wallDef({ id: 309, key: 'w309_crimsonsandstoneecho', name: '', mapColor: '#49120C', opacity: 1 });
1238	wallDef({ id: 310, key: 'w310_hallowsandstoneecho', name: '', mapColor: '#3A2F51', opacity: 1 });
1239	wallDef({ id: 311, key: 'w311_desertfossilecho', name: '', mapColor: '#734122', opacity: 1 });
1240	wallDef({ id: 312, key: 'w312_bambooblockwall', name: '', mapColor: '#244110', opacity: 1 });
1241	wallDef({ id: 313, key: 'w313_largebambooblockwall', name: '', mapColor: '#213D13', opacity: 1 });
1242	wallDef({ id: 314, key: 'w314_amberstonewallecho', name: '', mapColor: '#4A3A2C', opacity: 1 });
1243	wallDef({ id: 315, key: 'w315_bamboofence', name: '', mapColor: '#72782D', opacity: 1 });
1244	wallDef({ id: 316, key: 'w316_ashwood', name: '', mapColor: '#3A3440', opacity: 1 });
1245	wallDef({ id: 317, key: 'w317_ashwoodfence', name: '', mapColor: '#504652', opacity: 1 });
1246	wallDef({ id: 318, key: 'w318_echowall', name: '', mapColor: '#060622', opacity: 1 });
1247	wallDef({ id: 319, key: 'w319_reefwall', name: '', mapColor: '#5B3052', opacity: 1 });
1248	wallDef({ id: 320, key: 'w320_poopwall', name: '', mapColor: '#42271B', opacity: 1 });
1249	wallDef({ id: 321, key: 'w321_shimmerblockwall', name: '', mapColor: '#3E536C', opacity: 1 });
1250	wallDef({ id: 322, key: 'w322_shimmerbrickwall', name: '', mapColor: '#3A5473', opacity: 1 });
1251	wallDef({ id: 323, key: 'w323_lunarrustbrickwall', name: '', mapColor: '#635E69', opacity: 1, largeFrame: 2 });
1252	wallDef({ id: 324, key: 'w324_darkcelestialbrickwall', name: '', mapColor: '#505C68', opacity: 1, largeFrame: 2 });
1253	wallDef({ id: 325, key: 'w325_astrabrickwall', name: '', mapColor: '#385F7C', opacity: 1, largeFrame: 2 });
1254	wallDef({ id: 326, key: 'w326_cosmicemberbrickwall', name: '', mapColor: '#5C5E50', opacity: 1, largeFrame: 2 });
1255	wallDef({ id: 327, key: 'w327_cryocorebrickwall', name: '', mapColor: '#3E6674', opacity: 1, largeFrame: 2 });
1256	wallDef({ id: 328, key: 'w328_mercurybrickwall', name: '', mapColor: '#626769', opacity: 1, largeFrame: 2 });
1257	wallDef({ id: 329, key: 'w329_starroyalebrickwall', name: '', mapColor: '#575C76', opacity: 1, largeFrame: 2 });
1258	wallDef({ id: 330, key: 'w330_heavenforgebrickwall', name: '', mapColor: '#545969', opacity: 1, largeFrame: 2 });
1259	wallDef({ id: 331, key: 'w331_ancientbluebrickwall', name: '', mapColor: '#2A2C51', opacity: 1 });
1260	wallDef({ id: 332, key: 'w332_ancientgreenbrickwall', name: '', mapColor: '#22421A', opacity: 1 });
1261	wallDef({ id: 333, key: 'w333_ancientpinkbrickwall', name: '', mapColor: '#401931', opacity: 1 });
1262	wallDef({ id: 334, key: 'w334_ancientgoldbrickwall', name: '', mapColor: '#4C4220', opacity: 1 });
1263	wallDef({ id: 335, key: 'w335_ancientsilverbrickwall', name: '', mapColor: '#3C4143', opacity: 1 });
1264	wallDef({ id: 336, key: 'w336_ancientcopperbrickwall', name: '', mapColor: '#4C2D20', opacity: 1 });
1265	wallDef({ id: 337, key: 'w337_ancientobsidianbrickwall', name: '', mapColor: '#25243B', opacity: 1 });
1266	wallDef({ id: 338, key: 'w338_ancienthellstonebrickwall', name: '', mapColor: '#392220', opacity: 1 });
1267	wallDef({ id: 339, key: 'w339_ancientcobaltbrickwall', name: '', mapColor: '#132B3C', opacity: 1 });
1268	wallDef({ id: 340, key: 'w340_ancientmythrilbrickwall', name: '', mapColor: '#2A433C', opacity: 1 });
1269	wallDef({ id: 341, key: 'w341_lavamossblockwall', name: '', mapColor: '#681700', opacity: 1 });
1270	wallDef({ id: 342, key: 'w342_argonmossblockwall', name: '', mapColor: '#5B0941', opacity: 1 });
1271	wallDef({ id: 343, key: 'w343_kryptonmossblockwall', name: '', mapColor: '#11592B', opacity: 1 });
1272	wallDef({ id: 344, key: 'w344_xenonmossblockwall', name: '', mapColor: '#05415E', opacity: 1 });
1273	wallDef({ id: 345, key: 'w345_violetmossblockwall', name: '', mapColor: '#3A0651', opacity: 1 });
1274	wallDef({ id: 346, key: 'w346_rainbowmossblockwall', name: '', mapColor: '#FF00FF', opacity: 1 });
1275	wallDef({ id: 347, key: 'w347_shimmerfall', name: '', mapColor: '#FF00FF', opacity: 1 });
1276	wallDef({ id: 348, key: 'w348_fallenstarwall', name: '', mapColor: '#FF00FF', opacity: 1 });
1277	wallDef({ id: 349, key: 'w349_stoneunsafe', name: '', mapColor: '#FF00FF', opacity: 1 });
1278	wallDef({ id: 350, key: 'w350_unbreakableblockwall', name: '', mapColor: '#FF00FF', opacity: 1 });
1279	wallDef({ id: 351, key: 'w351_feywoodwall', name: '', mapColor: '#FF00FF', opacity: 1 });
1280	wallDef({ id: 352, key: 'w352_hallowedbrickwall', name: '', mapColor: '#FF00FF', opacity: 1 });
1281	wallDef({ id: 353, key: 'w353_pinetreeblockwall', name: '', mapColor: '#FF00FF', opacity: 1 });
1282	wallDef({ id: 354, key: 'w354_easterblockwall', name: '', mapColor: '#FF00FF', opacity: 1, largeFrame: 1 });
1283	wallDef({ id: 355, key: 'w355_gothicbrickwall', name: '', mapColor: '#FF00FF', opacity: 1, largeFrame: 2 });
1284	wallDef({ id: 356, key: 'w356_flinxfurblockwall', name: '', mapColor: '#FF00FF', opacity: 1 });
1285	wallDef({ id: 357, key: 'w357_jellyfishblockwall', name: '', mapColor: '#FF00FF', opacity: 1 });
1286	wallDef({ id: 358, key: 'w358_pinewoodblockwall', name: '', mapColor: '#FF00FF', opacity: 1, largeFrame: 2 });
1287	wallDef({ id: 359, key: 'w359_harpyblockwall', name: '', mapColor: '#FF00FF', opacity: 1, largeFrame: 2 });
1288	wallDef({ id: 360, key: 'w360_moonplateblockwall', name: '', mapColor: '#FF00FF', opacity: 1 });
1289	wallDef({ id: 361, key: 'w361_librarianblockwall', name: '', mapColor: '#FF00FF', opacity: 1 });
1290	wallDef({ id: 362, key: 'w362_spikeblockwall', name: '', mapColor: '#FF00FF', opacity: 1, largeFrame: 2 });
1291	wallDef({ id: 363, key: 'w363_officeblockwall', name: '', mapColor: '#FF00FF', opacity: 1, largeFrame: 2 });
1292	wallDef({ id: 364, key: 'w364_forbiddenblockwall', name: '', mapColor: '#FF00FF', opacity: 1 });
1293	wallDef({ id: 365, key: 'w365_waterblockwall', name: '', mapColor: '#FF00FF', opacity: 1 });
1294	wallDef({ id: 366, key: 'w366_boulderblockwall', name: '', mapColor: '#FF00FF', opacity: 1, largeFrame: 2 });
1295	
1296	// 墙 key→id 回填（id 即原版 wld 墙 id）
1297	WALL_DEFS.forEach((d) => { if (d) WALL_BY_KEY[d.key] = d.id; });
1298	

```


---

## 🤖 Assistant · 2026-08-13T06:17:19.155Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have the repo's tiles.ts. I need to check which vanilla emissive cases exist in repo.

Also check SkyColor.ts for FlickerClock: discoColor, demonTorchColor, shimmerTorchColor, mouseTextColor. And devices.ts lightIsOn.

Let me read SkyColor.ts and the relevant part of devices.ts.

Also need to check vanilla Main.tileLighted list to know which tiles are in tileLighted (since repo def.light only matters for those it defined). Actually for audit, I compare per vanilla switch case.

Let me now extract vanilla emissive case list with line numbers. From the ApplyTileLight switch, cases:

1. 658 (Aether monolith): frameY/54 scaling (0.2/0.3/0.1) of TorchID 23. Repo: v_658_aether_monolith has no light, no special → missing.
2. 356 sundial: if sundialCooldown==0 → (0.45,0.25,0). Repo light [115,64,0] = 0.451,0.251,0 ✓ but no cooldown gate. Repo def v_356_enchanted_sundial light [115,64,0] ≈ 0.45/0.25/0 — matches (gate missing: lightIsOn? gate is sundialCooldown not wiring; need to check devices.lightIsOn for 356).
3. 663 moondial: if moondialCooldown==0 → (0,0.25,0.45). Repo v_663 has no light → missing.
4. 656 glow tulip: (0.2,0.55,0.5). Repo light [255,185,110] = (1.0,0.725,0.431) → deviation.
5. 20 (crimson hearts? tile 20 = Crimson Heart? Actually tile 20 = "CrystalHeart"? No—tile 20 in Terraria is Demonite... let me recall: TileID 20 = "ShadowOrbs"/Crimson Hearts? TileID.CrystalHeart = 58? Hmm. TileID 20 = "Shadow Orb" — actually TileID.ShadowOrbs = 23? Let me check: TileID 23 = ShadowOrbs? From repo: v_23_corrupt_grass_block (CorruptGrass=23). TileID 20 = "CrimsonHearts"? Hmm, let me check TileID.cs for names. Actually case 20 with frameX/18 in 30..32 → (0.325,0.15,0.05). TileID 20 = "CrimsonHeart"? I think TileID 20 = "CrimsonHearts". Let me verify by reading TileID.cs names for relevant ids. Not critical but useful for report. Let me grep names.

Anyway repo v_20? No def for sheet 20 (that's acorn_sapling which uses sheet 20! T.ACORN=24 acorn_sapling has sheet 20). Wait: vanilla tile 20 vs repo sheet 20 = acorn sapling. Vanilla tile 20 — hmm. Actually vanilla tile 20 is "CrimsonHeart"? Let me check TileID.cs: 20 = "CrimsonHearts"? I need names. Let me grep.

6. 634 ash tree: (0.65,0.3,0.1). Repo v_634_ash_tree light [166,77,26] = 0.651,0.302,0.102 ✓
7. 633/637/638 ash grass/short plants/vines: (0.325,0.15,0.05). Repo: v_633 light [83,38,13] = 0.325,0.149,0.051 ✓; v_637 same ✓; v_638 [83,38,13] ✓
8. 463 defenders forge: (0.2,0.4,0.8). Repo light [51,102,204] = 0.2,0.4,0.8 ✓
9. 491 void vault: (0.5,0.4,0.7). Repo [128,102,179] = 0.502,0.4,0.702 ✓
10. 209 cannon portal frames: (portal colors ×0.65). Repo special case 209 ✓ (approximate colors: purple portal1 [0.42,0.2,0.65]?? Need to check PortalHelper.GetPortalColor: portal colors are Color for portal 0 and 1. Let me check PortalHelper to verify repo's hardcoded values.)
11. 415 solar fragment block: (0.7,0.5,0.1). Repo: no light on v_415 → missing.
12. 500 solar brick: (0.525,0.375,0.075). Repo v_500 no light → missing.
13. 416 vortex fragment: (0,0.6,0.7). Repo v_416 no light → missing.
14. 501 vortex brick: (0,0.45,0.525). missing.
15. 417 nebula fragment: (0.6,0.2,0.6). missing.
16. 502 nebula brick: (0.45,0.15,0.45). missing.
17. 418 stardust fragment: (0.6,0.6,0.9). missing.
18. 503 stardust brick: (0.45,0.45,0.675). missing.
19. 390 lava lamp: (0.4,0.2,0.1). Repo v_390 no light → missing.
20. 597 pylon: style-based colors ×0.75. Repo light [13,204,77] = 0.051,0.8,0.3 = style 0 × 0.75 → (0.05,0.8,0.3)×0.75 = (0.0375,0.6,0.225). Repo (0.051,0.8,0.3) is style0 un-multiplied → deviation (missing ×0.75), and only style 0 covered.
21. 564 plasma lamp: frameX<36 → (0.05,0.3,0.55). Repo [13,77,140] = 0.051,0.302,0.549 ✓ but no frameX<36 gate (missing condition). Also FLICKER_SHEETS includes 564 → adds flicker which vanilla does NOT (case 564 has no flicker term). Deviation.
22. 568 pink fairy jar: (1,0.61,0.65). Repo v_568 no light → missing.
23. 569 green fairy jar: (0.12,1,0.66). missing.
24. 570 blue fairy jar: (0.57,0.57,1). missing.
25. 580 hell butterfly jar: (0.7,0.3,0.2). missing (v_580 no light).
26. 391 enchanted nightcrawler cage: (0.3,0.1,0.25). missing (v_391 no light).
27. 381/517/687 lava moss variants: (0.25,0.1,0). Repo: v_381_lava_moss light [255,120,30] = (1,0.47,0.118) → wrong! vanilla 381 → (0.25,0.1,0). v_517 no light, v_687 no light → missing.
28. 534/535/689 krypton moss: (0,0.25,0). Repo v_534 no light, v_535 no light, v_689 no light → missing.
29. 536/537/690 xenon moss: (0,0.16,0.34). Repo v_536 [0,41,87] = (0,0.161,0.341) ✓; v_537 no light → missing; v_690 no light → missing.
30. 539/540/688 argon moss: (0.3,0,0.17). Repo v_539 [77,0,43] = (0.302,0,0.169) ✓; v_540 no light → missing; v_688 no light → missing.
31. 625/626/691 neon moss: (0.3,0,0.35). Repo v_625 [77,0,89] = (0.302,0,0.349) ✓; v_626 no light; v_691 no light → missing.
32. 627/628/692 helium moss: disco ×0.25. Repo none → missing.
33. 184 moss plants: frameX-based colors (110→(0.25,0.1,0), 132→(0,0.25,0), 154→(0,0.16,0.34), 176→(0.3,0,0.17), 198→(0.3,0,0.35), 220→disco×0.25). Repo v_184 light [77,0,89] = (0.302,0,0.349) = only the 198 frame value → deviation (only 1 of 6 frame colors).
34. 370 meteorite brick: (0.32,0.16,0.12). Repo v_370 no light → missing.
35. 659/667/708 shimmerfall/shimmer block/shimmerfall block: GetShimmerBaseColor → missing.
36. 711 rainbow boulder: (0.01,0.01,0.01). Repo v_711 [3,3,3] = 0.0118 ✓ ≈ (0.01).
37. 27 sunflower: frameY<36 → (0.3,0.27,0). Repo v_27 light [255,242,166] = (1,0.949,0.651) → big deviation. Vanilla (0.3,0.27,0).
38. 336 living fire block: (0.85,0.5,0.3). Repo v_336 no light → missing.
39. 340 living cursed fire: (0.45,1,0.45). Repo [115,255,115] = (0.451,1,0.451) ✓
40. 341 living demon fire: demonTorch blend. Repo v_341 no light → missing.
41. 342 living frost fire: (0.5,0.5,1.1). missing.
42. 343 living ichor fire: (0.85,0.85,0.3). missing.
43. 344 living ultrabright fire: (0.6,1.026,0.96). missing.
44. 327 lavafall block: flicker base (1,0.5,0.1)×num13. Repo v_327 no light → missing.
45. 316/317/318 jellyfish cages: two states. Repo v_316 light [102,26,64]=(0.4,0.102,0.251)?? Vanilla 316: state2 (0.2,0.3,0.8) else (0.1,0.2,0.5). Repo is neither → deviation. v_317, v_318 no light → missing.
46. 719 rainbow cloud: animated hue. Repo v_719 no light → missing.
47. 718 star cloud: night & !SolidTile above → disco-ish. Repo none → missing.
48. 717 lava cloud: (num13 formula). Repo v_717 no light → missing.
49. 429 wire bulb: ✓ implemented special case. matches vanilla.
50. 286 glowing snail cage / 619 truffle worm cage: (0.1,0.2,0.7). Repo v_286 no light; v_619 no light → missing.
51. 620 prismatic lacewing jar: hue cycling ×0.4. missing.
52. 582 magma snail cage / 598 lava serpent bowl: (0.7,0.2,0.1). Repo v_598 light [255,185,110]=(1,0.725,0.431) → deviation (vanilla 0.7,0.2,0.1). v_582 no light → missing.
53. 270 firefly bottle: (0.73,1,0.41). Repo v_270 no light → missing.
54. 271 lightning bug bottle: (0.45,0.95,1). missing.
55. 581 lavafly bottle: (1,0.75,0.5). Repo v_581 no light → missing.
56. 660 faeling bottle: TorchID 23 (shimmer torch). missing.
57. 572 souls in bottle: frameY/36 styles. Repo none → missing.
58. 262 amethyst gemspark: (0.75,0,0.75). Repo: v_262 no light → missing.
59. 263 topaz: (0.75,0.75,0). missing.
60. 264 sapphire: B=0.75. missing.
61. 265 emerald: G=0.75. missing.
62. 266 ruby: R=0.75. missing.
63. 267 diamond: (0.75,0.75,0.75). missing.
64. 268 amber: (0.75,0.375,0). missing.
65. 237 lihzahrd altar: (0.1,0.1,0). Repo [26,26,0] = (0.102,0.102,0) ✓
66. 238 plantera bulb: raises lightColor X/Z to 0.5. Repo none → missing.
67. 235 teleporter: raises to 0.6/0.6. Repo v_235 no light → missing.
68. 405 fireplace: frameX<54 style colors + flicker. Repo light [255,185,110] and FLICKER_SHEETS has 405 → (1,0.725,0.431)+flicker. Vanilla default (0.9,0.3,0.1)+flicker for style 0. Deviation (color), style gate missing.
69. 215 campfire: frameY<36, styles 0-15 colors + flicker. Repo [255,185,110] → deviation; gate missing.
70. 92 lampposts: frameY<=18 && frameX==0 → (1,1,1). Repo v_92 light [255,255,255] ✓ but no frame gate (missing condition: should be off when frameY>18 or frameX!=0 — lightIsOn may handle?).
71. 592 hanging brazier: frameY>0 → (1.35,0.45,0.15)+flicker. Repo [255,185,110]+FLICKER → deviation.
72. 593 volcano small: frameX<18 → (0.8,0.3,0.1). Repo [204,77,26] = (0.8,0.302,0.102) ✓ but no frame gate.
73. 594 volcano large: frameX<36 → same. ✓ value; gate missing.
74. 548 potted trees group 2: frameX/54>=7 → (0.7,0.3,0.2). Repo [179,77,51] = (0.702,0.302,0.2) ✓ value, gate missing.
75. 613/614 potted lava plants: (0.7,0.3,0.2). Repo [179,77,51] ✓.
76. 93 lamps: frameX==0, style rows (frameY/54). Repo v_93 light [255,185,110] → deviation (vanilla style-dependent, default (1,0.97,0.85) for style 0). Actually default: R=1,G=0.97,B=0.85. Repo (1,0.725,0.431) → deviation.
77. 33 candle: frameX==0, frameY/22 styles. Repo candle light [255,185,110] = (1,0.725,0.431); vanilla default (1,0.95,0.65) → deviation.
78. 174 platinum candle: frameX==0 → (1,0.95,0.65). Repo v_174 [255,242,166] = (1,0.949,0.651) ✓ value; gate missing (frameX==0).
79. 100/173 candelabra: frameX<36, style frameY/36. Repo candelabra [255,185,110]; v_173 [255,242,166]=(1,0.949,0.651) ✓ value for default; gate missing.
80. 34 chandelier: frameX%108<54, style = frameY/54 + 37*(frameX/108). Repo chandelier [255,190,120]=(1,0.745,0.471); vanilla default (1,1,1) → deviation.
81. 35 jack-o-lantern: frameX<36 → (0.75,0.6,0.3). Repo v_35 [179,153,230]=(0.702,0.6,0.902) → deviation.
82. 95 chinese lantern: frameX<36 → (1,0.95,0.8). Repo [255,160,70]=(1,0.627,0.275) → deviation. (also FLICKER_SHEETS includes 95; vanilla case 95 has no flicker → extra flicker deviation)
83. 17/133/302 furnaces: (0.83,0.6,0.5). Repo furnace (sheet17) light [255,140,70]=(1,0.549,0.275) → deviation. v_133 (sheet 133) no light → missing. v_302 (glass kiln) [212,153,128]=(0.831,0.6,0.502) ✓. v_77 hellforge [255,140,70] → deviation (77 not in vanilla case list! vanilla has 17,133,302 only). So hellforge shouldn't glow per vanilla → extra.
84. 77 hellstone forge: not in vanilla switch → repo adds light → extra (not vanilla).
85. 49 water candle: frameX==0 → (0,0.35,0.8). Repo water_candle [140,180,255]=(0.549,0.706,1) → deviation. Also FLICKER_SHEETS has 49 → extra flicker (vanilla no flicker).
86. 519 cattail: frameY==90 → (0.1, 0.2+n/2, 0.7+n). Repo v_519 [26,51,179]=(0.102,0.2,0.702) ✓ approx (without flicker n); gate missing.
87. 70/71/72/190/348/349/528/578 mushroom group ✓ implemented via MUSHROOM_GLOW_SHEETS with 349 gate. Check formula: vanilla R=0, G=0.2+num11/2, B=1 where num11=Next(28,42)*0.005+(270-mouse)/1000. Repo matches ✓. Also 519 in same case? No, 519 is separate.
88. 739 jellyfish block: (0.35,0.63,0.7) + paint flag. Repo v_739 no light → missing.
89. 350 martian conduit plating: time-based pulse. Repo [26,26,26]=(0.102,0.102,0.102) static → approximation deviation (vanilla oscillates -cos*0.1+0.1 → 0..0.2 on cycle).
90. 61/703 jungle grass/jungle plants echo: frameX==144 → (0.42*num7, 0.81*num6, 0.52*num7). Repo v_61 light [107,207,133]=(0.42,0.812,0.522) ✓ value (without num multipliers); gate missing (frameX==144). v_703 no light → missing.
91. 26/31/695/696 altars & shadow orbs: vanilla (26 & 695): style-based. For tile 26 (demon altar): frameX>=54 (26/695) or >=36 (31/696) → (0.5+num4*2, 0.2+num4, 0.1) with num4=Next(-5,6)*0.0025; else (0.31+num5, 0.1, 0.44+num5*2). Repo v_26 [79,26,112]=(0.310,0.102,0.439) ✓ else-branch value; flicker missing (num5 ±0.0125); second-branch missing. v_31 [79,26,112] ✓ else branch; gate/frame branch missing. v_695/v_696 no light → missing.
92. 699 alchemy flask: (0.4,0.2,0.15). Repo v_699 no light → missing.
93. 84 herbs bloom: style cases 2/5/6 ✓ implemented. But vanilla has case 2 (num3=(270-mouse)/400 clamp 0..1, R=num3*1.4,G=num3*1.2,B=num3/2) — repo matches. case5: R=num3(0.9), G=0.9*0.8=0.72, B=0.9*0.2=0.18. Repo returns [0.9,0.72,0.18] ✓. case6: num3=0.08, G=0.064, B=0.08. Repo [0,0.064,0.08] ✓.
94. 83 herbs mature: frameX==18 && !dayTime → (0.1,0.4,0.6); frameX==90 && !raining && time>40500 → (0.9,0.72,0.18). Repo v_83 light [230,184,46]=(0.902,0.722,0.180) → deviation (applies unconditionally; only matches bloom-day branch).
95. 126 disco ball ✓ special; matches (frameX<36 gate ✓).
96. 125 crystal ball: G=0.3*num, B=0.6*num where num=Next(28,42)*0.01+(270-mouse)/800, and sets lightColor directly. Repo v_125 light [0,27,54]=(0,0.106,0.212) static → deviation (vanilla ranges: num ~ 0.28..0.42+0..0.3375 → up to ~0.76; G up to 0.23, B up to 0.45).
97. 129 crystal shard: frameX/18%3 colors. Repo v_129 [0,13,64]=(0,0.051,0.251) ✓ case 0 value; cases 1,2 missing.
98. 149 holiday lights: frameX<=36, style colors ×rand(0.97..1.03). Repo [26,51,128]=(0.102,0.2,0.502) ✓ case0 value; gate and other styles missing. Also in FLICKER_SHEETS → adds wrong flicker (vanilla uses rand multiplier 0.97-1.03 per channel, not additive flicker) → deviation.
99. 160 rainbow brick: disco×0.25. Repo v_160 no light → missing.
100. 354 bewitching table: (0.65,0.35,0.15). Repo [166,89,38]=(0.651,0.349,0.149) ✓
101. Also case 37 (meteorite): (0.56*num23, 0.43*num23, 0.15*num23) with num23=Next(95,106)*0.01. Repo ore_meteorite [143,110,38]=(0.561,0.431,0.149) ✓ value (mid), flicker missing.
102. 22/140 (demonite brick): (0.12,0.07,0.32) unless painted 26/27. Repo ore_demonite (sheet 22) [255,255,153]=(1,1,0.6)?? That's way off. Wait — ore_demonite uses sheet 22 which vanilla is "Demonite"? Hmm tile 22 = Demonite ore? Yes TileID 22 = Demonite. Vanilla case 22/140 → (0.12,0.07,0.32) R only if not painted. Repo [255,255,153] = (1,1,0.6) → big deviation. Hmm wait, but that comment says extracted. (1,1,0.6) looks like a candle color. Definitely wrong. Let me double check: case 22, 140 at :2508-2516: `if (tile.color() != 27 && tile.color() != 26) R = 0.12f; G = 0.07f; B = 0.32f;`. So (0.12,0.07,0.32). Repo (1.0,1.0,0.6) → deviation.
   v_140 demonite brick: no light → missing.
103. 171 logic sensor (tile 171 = LogicSensor): frameY & 0x3C00 >> 10 style colors ×0.5. Repo v_171 christmas_tree (sheet 171) no light → missing. Note repo's sheet 171 = christmas tree; vanilla tile 171 = LogicSensor. Hmm — repo tile id mapping differs from vanilla tile ids! Wait no: repo `vanilla.sheet` is the *vanilla tile id* used for rendering. v_171_christmas_tree has sheet 171 → that means repo thinks vanilla tile 171 is christmas tree. But vanilla TileID 171 = LogicSensor! And ChristmasTree = 199? Hmm. Let me check: In Terraria TileID: 171 = LogicSensor, 199 = ChristmasTree. Hmm, but repo v_199_crimson_grass_block sheet 199 (CrimsonGrass=199 ✓ vanilla). And v_170_pine_tree_block sheet 170 (PineTreeBlock=170 ✓). v_171 = christmas tree?? That would be wrong in repo data (but out of scope for light audit; though it means repo mislabels). Actually wait: TileID 171 might be ChristmasTree in 1.4.5? Let me check TileID.cs names to be accurate. I'll grep the names for the ids I care about.

104. 204/347: R=0.35 unless painted 26/27. Repo: sheet 204 = ore_crimtane? No wait repo ore_crimtane sheet 204... hmm vanilla tile 204 = "Crimtane"? Actually vanilla TileID.Crimtane = 204? Yes! TileID 204 = Crimtane. And case 204/347 → R=0.35 only (if not painted). Repo [89,0,0]=(0.349,0,0) ✓. 347 = crimtane brick; repo v_347 no light → missing.
105. 42 lantern ✓ implemented in specialTileLight with styles. Let me verify all style values against vanilla case 42:
   - case 0: (0.7,0.65,0.55) ✓
   - 1: (0.9,0.75,0.6) ✓
   - 2: (0.8,0.6,0.6) ✓
   - 3: (0.65,0.5,0.2) ✓
   - 4: (0.5,0.7,0.4) ✓
   - 5: (0.9,0.4,0.2) ✓
   - 6: (0.7,0.75,0.3) ✓
   - 7: demonTorch (0.9-d*0.2, 0.9-d*0.2, 0.7+d*0.2) ✓ repo matches
   - 8: (0.75,0.6,0.3) ✓
   - 9: demonTorch (1-d*0.1, 0.3-d*0.2, 0.5+d*0.2) ✓
   - 11: (0.85,0.6,1) ✓
   - 14: (1,0.95,0.65) ✓
   - default: vanilla default = (1,1,1)! Repo fallback `LANTERN_LIGHT[st] ?? [0.7, 0.65, 0.55]` → deviation (should be 1,1,1 for styles 10,12,13,...). Vanilla default at :2906-2909: R=1,G=1,B=1. So repo default fallback (0.7,0.65,0.55) is wrong → deviation.
   Also repo is missing styles 15/16 (1,0.95,0.65), 17 (1,0.97,0.85), 18 (0.75,0.85,1), 21 (1,0.95,0.65), 22 (1,1,0.6), 23 (1,0.95,0.65), 27, 28 (0.37,0.8,1/paint), 29 (0,0.9,1), 30 (0.25,0.7,1), 32 demon, 35-70 torch styles. So lantern is heavily partial: only 12 of ~60 styles covered, default wrong.
106. 49 water candle (above).
107. 372 peace candle: frameX==0 → (0.9,0.1,0.75). Repo [230,26,191]=(0.902,0.102,0.749) ✓ value; gate missing (frameX==0).
108. 646 shadow candle: frameX==0 → (0.2,0.3,0.32). Repo v_646 no light → missing.
109. 61 jungle grass ✓ value (gate missing).
110. 37 meteorite ✓.
111. 98 skull lantern: frameY==0 → (1,0.97,0.85). Repo [255,160,70]=(1,0.627,0.275) → deviation. Also FLICKER_SHEETS includes 98? No — FLICKER list: [33,49,92,93,174,34,149,95,100,126,173,564,215,405,4]. 98 not there. OK.
112. 4 torch ✓ but with extra flicker deviation and gate frameX<66. Need to check lightIsOn for sheet 4.
113. 96 (tile 96 = Lamps? no 96 = "Plate"? hmm) — case 96: frameX>=36 → (0.5,0.35,0.1). Which tile is 96? Let me check TileID names. Repo sheet 96 = cooking_pot. Hmm. Vanilla tile 96 = "CookingPot"? Hmm, I'm not sure. Let me grep names.
114. 100 candelabra group... covered above.
115. 35 covered.
116. 92 ✓.
117. 27 sunflower covered.
118. Also case 20 (crimson heart?) and 633 etc.

Also very important: Main.tileLighted[] — the switch is only entered when tileLighted[tile.type] is true. So repo's def.light must only be for tiles in tileLighted. Also missing light on tiles where tileLighted true.

Also there's TileLoader.ModifyLight for mod tiles — not relevant.

Additionally, vanilla case 739 new in 1.4.5, 711, 708, 719, 718, 717, 658, 663, 667, 703, 695, 696, 687-692, 739.

Also wall emissive: vanilla cases: 357, 182, 33, 174, 175, 176, 137, 44, 154, 166, 165, 156, 164, 155, 153, 341, 343, 344, 342, 345, 346 = 21 wall cases. Repo has 19 entries: 33,44,137,153,154,155,156,164,165,166,174,175,176,182,341,342,343,344,345,346,357 — that's 21! Let me count: 33,44,137,153,154,155,156,164,165,166,174,175,176,182,341,342,343,344,345,346,357 = 21 entries. The user said "本仓 19 条" but actual is 21. Fine.

Now compare values:
- 357: vanilla 0.15,0.27,0.3 + flag(paint) → repo 0.15,0.27,0.3 ✓ (paint branch missing — repo has no wall paint handling)
- 182: vanilla 0.24,0.12,0.089999996 → repo 0.24,0.12,0.09 ✓
- 33: vanilla 0.089999996,0.052500002,0.24 → repo 0.09,0.0525,0.24 ✓
- 174: vanilla num=0.2975 only (R) → repo [0.2975,0,0] ✓
- 175: vanilla if wallColor==0 → (0.075,0.15,0.4) else flag → repo static (0.075,0.15,0.4) — paint branch missing (approximation)
- 176: (0.1,0.1,0.1) ✓
- 137: num4=0.4+(270-mouse)/1500+Next(0,50)*0.0005 → R=num4, G=0.5*num4, B=0.1*num4. Repo static [0.5,0.25,0.05] ✓ base (no flicker/mouse modulation) — approximation, acceptable but note.
- 44: disco×0.15 → repo static [0.15,0.15,0.15] approximation (dynamic missing)
- 154: vanilla num=0.6, num3=0.6 → (0.6,0,0.6). Repo: [0.6,0.12,0.6] ← wait repo has 154: [0.6,0.12,0.6]. That's wrong! Vanilla case 154: num=0.6 (R), num3=0.6 (B). G=0. Repo G=0.12 → deviation.
  Hmm wait, careful: case 154: `num = 0.6f; num3 = 0.6f;` → R=0.6,B=0.6,G=0. Repo [0.6,0.12,0.6] → G deviation (0.12 vs 0). Note comment says "紫水晶宝石灯墙" for 153 and 154 both. Vanilla 154 = TopazGemspark? Let's see walls: 153 amber gemspark, 154 amethyst gemspark, 155 diamond, 156 emerald, 164 ruby, 165 sapphire, 166 topaz. Wait repo comments: 153 紫水晶 (amethyst) — but 153 = amber. Whatever; the key is values.
  Vanilla: 153: R=0.6,G=0.3 → (0.6,0.3,0). Repo 153: [0.6,0.12,0.6] → deviation (G should be 0.3, B should be 0).
  Hmm wait, let me re-read vanilla:
  - case 154: num=0.6 (R), num3=0.6 (B) → (0.6, 0, 0.6)
  - case 166: num=0.6 (R), num2=0.6 (G) → (0.6,0.6,0)
  - case 165: num3=0.6 (B) → (0,0,0.6)
  - case 156: num2=0.6 (G) → (0,0.6,0)
  - case 164: num=0.6 (R) → (0.6,0,0)
  - case 155: all 0.6 → (0.6,0.6,0.6)
  - case 153: R=0.6,G=0.3 → (0.6,0.3,0)
  
  Repo:
  - 153: [0.6,0.12,0.6] → should be (0.6,0.3,0) → deviation
  - 154: [0.6,0.12,0.6] → should be (0.6,0,0.6) → deviation (G 0.12 vs 0)
  - 155: [0.6,0.42,0.06] comment 琥珀 → should be (0.6,0.6,0.6) → deviation!! Vanilla 155 = DiamondGemspark → (0.6,0.6,0.6). Repo gives (0.6,0.42,0.06) — that's the *tile* 354 bewitching color. Wrong.
  Hmm wait — is 155 really diamond? WallID: 153=AmberGemspark, 154=AmethystGemspark, 155=DiamondGemspark, 156=EmeraldGemspark, 157=AmberGemsparkOff...164=RubyGemspark,165=SapphireGemspark,166=TopazGemspark. And repo's WALL_DEFS confirm: 153 amber, 154 amethyst, 155 diamond, 156 emerald, 164 ruby, 165 sapphire, 166 topaz. ✓
  So repo values are misassigned:
  - 153 amber → vanilla (0.6,0.3,0) [R=0.6, G=0.3]; repo (0.6,0.12,0.6) ✗
  - 154 amethyst → vanilla (0.6,0,0.6); repo (0.6,0.12,0.6) ✗ G
  - 155 diamond → vanilla (0.6,0.6,0.6); repo (0.6,0.42,0.06) ✗✗ (looks like bewitching table color)
  - 156 emerald → vanilla (0,0.6,0); repo (0.09,0.6,0.24) ✗ R 0.09 & B 0.24 extra
  - 164 ruby → vanilla (0.6,0,0); repo (0.09,0.24,0.6) ✗ (this is a blue-ish color; wrong)
  - 165 sapphire → vanilla (0,0,0.6); repo (0.6,0.06,0.09) ✗
  - 166 topaz → vanilla (0.6,0.6,0); repo (0.42,0.42,0.6) ✗
  
  So the entire gemspark wall block (153-166 subset) is scrambled: the repo appears to have used the gem *item/tile* colors rather than the wall's single-channel values. All 7 deviate.
- 341: (0.25,0.1,0) ✓
- 343: (0,0.25,0) ✓
- 344: (0,0.16,0.34) ✓
- 342: (0.3,0,0.17) ✓
- 345: (0.3,0,0.35) ✓
- 346: disco×0.25 → repo static 0.25 ✓ approx
All wall emissive present (21/21 ids). Also note vanilla gate: most require !LightIsBlocked(tile); repo gates on st.type[i]===0 which is roughly equivalent but stronger (vanilla allows if tile is active but doesn't block light, e.g. torch on gemspark wall). Note also cases 154-166 in vanilla have NO !LightIsBlocked gate (they emit even behind solid blocks? they always emit). Minor.

Wait, check which wall cases lack the LightIsBlocked gate: 154,166,165,156,164,155,153 have no gate (they always apply). Others have gate. Repo applies gate wall!==0 && type===0 for all. Deviation nuance.

Now liquid: 
- ApplyLiquidLight lava: num=0.55+(270-mouseTextColor)/900; if lightColor.X<num → X=num; Y=num*0.6; Z=num*0.2. Repo: lavaV=0.55+(270-mouse)/900; lr=max(lr,lavaV), lg=max(lg,lavaV*0.6), lb=max(lb,lavaV*0.2). ✓ Note subtle: vanilla only raises Y if Y<num, setting to num*0.6 — repo uses max with num*0.6, equivalent-ish (if Y>=num then Y stays; repo max(Y, 0.6num) ≤ Y fine). Equivalent.
- shimmer: num2=0.7+(270-mouse)/900, num3=0.7+(270-mouse)/125; X→num2*0.6, Y→num3*0.25, Z→num2*0.9. Repo: missing shimmer liquid light! Check TileLightScanner.ts: only lava (liquidType===2). Shimmer liquid (liquidType 4?) not implemented → missing.
- ApplyHellLight: num4=0.55+sin(GlobalTime*2)*0.08; gate (wallLight || wall==73 || wall==227 || invisibleWall) && liquid<200 && halfBrick check. Repo: hellV=0.55+sin(performance.now()*0.002)*0.08. Vanilla uses Main.GlobalTimeWrappedHourly*2 (GlobalTimeWrappedHourly increments in "hours"? Actually it's gameTimeUpdate / 3600? whatever). Repo approximates with performance.now()*0.002 → period = 2π/0.004 ms ≈ 1571 ms. Vanilla: GlobalTimeWrappedHourly increases at rate 1/3600 per frame-ish... This is an approximation, note it. Also the repo gates via exposed() which uses WALL_LIGHT (missing wall 73 cloud and 227 snowfall exceptions!). Vanilla: wallLight[tile.wall] || tile.wall==73 || tile.wall==227. WALL_LIGHT includes 315? No: wallLight true ids: 0,21,318,106,317,107,138,140,141,139,145,150,152,245,315,168. So wall 73 (cloud) and 227 (snowfall) are extra in vanilla! Repo WALL_LIGHT doesn't include 73 or 227 → missing 2 walls (cloud, snowfall) for sky/hell light transmission.
- Also ApplySurfaceLight has the stained glass wall tint branch — repo implements in the wall block with caveats; it also requires tile not active && ... hmm vanilla: `(!tile.active() || tile.halfBrick() || !Main.tileNoSunLight[tile.type]) && ((wall 88..93) || wall==241) && liquid<255`. Repo applies when type===0 (in the wall block) — approximates; it uses max rather than multiply. Note the deviation: vanilla multiplies the *sky light* by the tint factors (0.9/0.15/0.9 etc.), which *reduces* channels; repo uses max which only raises → for stained glass under dim sky, repo gives brighter/whiter result. Deviation noted.

Also `Main.mouseTextColor` — flicker.mouseTextColor; check SkyColor.

Also MOON_FLOOR — check Main.cs:63230-63266 later.

Now I need:
1. TileID names for the ids in question (to name them correctly in the report). Let me grep TileID.cs for specific names.
2. PortalHelper.GetPortalColor to verify repo 209 colors.
3. SkyColor.ts FlickerClock implementations (discoColor, demonTorchColor, shimmerTorchColor, mouseTextColor) and compare with vanilla DiscoTorchLight/DemonTorchLight/ShimmerTorchLight, Main.DiscoR/G/B.
4. devices.ts lightIsOn to check gates for torch/candle etc.
5. Main.cs tileLighted list (to confirm which tiles vanilla marks) — to catch repo defs with light that vanilla doesn't have (extra light) and vice versa.
6. Main.cs wallLight — done. But also check WallID/`wallLight` maybe set elsewhere; grep.
7. Check whether tile 48/137 lava blocks (user mentions "tile 48/137 熔岩块 :110 附近") — hmm user says "岩浆（ApplyHellLight :3261 与 tile 48/137 熔岩块 :110 附近 lavaV 0.55+(270-mouse)/900）". Tile 48 = spike? No wait. Hmm, in vanilla 1.4.4, tile 48 = "Spike"? Actually no. Let me check: ApplyLiquidLight is at :110. The user's mention of "tile 48/137 熔岩块" might refer to LiquidID lava? Whatever — I'll check TileID 48 and 137 names. Repo v_48_spike uses sheet 48. Vanilla tile 48 = Spike ✓ probably. And 137 = Traps.

Let me do these reads in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:17:22.092Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"public const short\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs | sed -n '1,5p'; for id in 4 17 20 22 26 27 31 33 34 35 37 42 49 61 70 71 72 77 83 84 92 93 95 96 98 100 125 126 129 133 140 149 160 171 174 173 184 190 204 209 215 235 237 238 270 271 286 302 316 317 318 327 336 340 341 342 343 344 347 348 349 354 356 381 390 391 405 415 416 417 418 429 463 491 500 501 502 503 517 519 528 534 535 536 537 539 540 548 551 564 568 569 570 572 580 581 582 592 593 594 597 598 613 614 619 620 625 626 627 628 633 634 637 638 656 658 659 660 663 667 687 688 689 690 691 692 695 696 699 703 708 711 717 718 719 739; do line=$(grep -n \"public const short .* = $id;\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs | head -1); echo \"$id => $line\"; done",
 "description": "Map vanilla tile ids to names"
}
```


---

## 🤖 Assistant · 2026-08-13T06:17:22.999Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"wallLight\\[\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs; echo ---; grep -rn \"GetPortalColor\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/PortalHelper.cs 2>/dev/null || find ~/Project/GLM/SandboxWorld/Terarria1456 -iname \"PortalHelper.cs\"",
 "description": "Check wallLight assignments and PortalHelper location"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:17:31.217Z

**📎 ToolResult**

```
4 => 
17 => 
20 => 
22 => 
26 => 
27 => 
31 => 
33 => 
34 => 
35 => 
37 => 
42 => 
49 => 
61 => 
70 => 
71 => 
72 => 
77 => 
83 => 
84 => 
92 => 
93 => 
95 => 
96 => 
98 => 
100 => 
125 => 
126 => 
129 => 
133 => 
140 => 
149 => 
160 => 
171 => 
174 => 
173 => 
184 => 
190 => 
204 => 
209 => 
215 => 
235 => 
237 => 
238 => 
270 => 
271 => 
286 => 
302 => 
316 => 
317 => 
318 => 
327 => 
336 => 
340 => 
341 => 
342 => 
343 => 
344 => 
347 => 
348 => 
349 => 
354 => 
356 => 
381 => 
390 => 
391 => 
405 => 
415 => 
416 => 
417 => 
418 => 
429 => 
463 => 
491 => 
500 => 
501 => 
502 => 
503 => 
517 => 
519 => 
528 => 
534 => 
535 => 
536 => 
537 => 
539 => 
540 => 
548 => 
551 => 
564 => 
568 => 
569 => 
570 => 
572 => 
580 => 
581 => 
582 => 
592 => 
593 => 
594 => 
597 => 
598 => 
613 => 
614 => 
619 => 
620 => 
625 => 
626 => 
627 => 
628 => 
633 => 
634 => 
637 => 
638 => 
656 => 
658 => 
659 => 
660 => 
663 => 
667 => 
687 => 
688 => 
689 => 
690 => 
691 => 
692 => 
695 => 
696 => 
699 => 
703 => 
708 => 
711 => 
717 => 
718 => 
719 => 
739 =>

```


---

## 👤 User(sidechain) · 2026-08-13T06:17:31.297Z

**📎 ToolResult**

```
10487:		wallLight[0] = true;
10488:		wallLight[21] = true;
10489:		wallLight[318] = true;
10490:		wallLight[106] = true;
10491:		wallLight[317] = true;
10492:		wallLight[107] = true;
10493:		wallLight[138] = true;
10494:		wallLight[140] = true;
10495:		wallLight[141] = true;
10496:		wallLight[139] = true;
10497:		wallLight[145] = true;
10498:		wallLight[150] = true;
10499:		wallLight[152] = true;
10500:		wallLight[245] = true;
10501:		wallLight[315] = true;
10502:		wallLight[168] = true;
54598:		if (!wallLight[tile.wall])
---
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/PortalHelper.cs

```


---

## 🤖 Assistant · 2026-08-13T06:17:39.103Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The grep pattern with "= <id>;" failed — probably names use different format. Let me look at TileID.cs format.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:17:39.114Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1,60p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs",
 "description": "Inspect TileID.cs format"
}
```


---

## 🤖 Assistant · 2026-08-13T06:17:39.137Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"GetPortalColor\" -A 30 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/PortalHelper.cs | head -60",
 "description": "Read PortalHelper.GetPortalColor"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:17:39.185Z

**📎 ToolResult**

```
377:	public static Color GetPortalColor(int colorIndex)
378-	{
379:		return GetPortalColor(colorIndex / 2, colorIndex % 2);
380-	}
381-
382:	public static Color GetPortalColor(int player, int portal)
383-	{
384-		Color white = Color.White;
385-		if (Main.netMode == 0)
386-		{
387-			white = ((portal != 0) ? Main.hslToRgb(0.52f, 1f, 0.6f) : Main.hslToRgb(0.12f, 1f, 0.5f));
388-		}
389-		else
390-		{
391-			float num = 0.08f;
392-			white = Main.hslToRgb((0.5f + (float)player * (num * 2f) + (float)portal * num) % 1f, 1f, 0.5f);
393-		}
394-		white.A = 66;
395-		return white;
396-	}
397-
398-	private static void GetPortalEdges(Vector2 position, float angle, out Vector2 start, out Vector2 end)
399-	{
400-		Vector2 vector = angle.ToRotationVector2();
401-		start = position + vector * -22f;
402-		end = position + vector * 22f;
403-	}
404-
405-	private static Vector2 GetPortalOutingPoint(Vector2 objectSize, Vector2 portalPosition, float portalAngle, out int bonusX, out int bonusY)
406-	{
407-		int num = (int)Math.Round(MathHelper.WrapAngle(portalAngle) / (MathF.PI / 4f));
408-		switch (num)
409-		{
410-		case -2:
411-		case 2:
412-			bonusX = ((num != 2) ? 1 : (-1));

```


---

## 👤 User(sidechain) · 2026-08-13T06:17:39.189Z

**📎 ToolResult**

```
using System.Collections.Generic;
using ReLogic.Reflection;

namespace Terraria.ID;

public class TileID
{
	public static class Sets
	{
		public static class Conversion
		{
			public static bool[] MergesWithDirtInASpecialWay = Factory.CreateBoolSet(2, 23, 109, 199, 477, 492);

			public static bool[] JungleGrass = Factory.CreateBoolSet(60, 661, 662);

			public static bool[] MushroomGrass = Factory.CreateBoolSet(70);

			public static bool[] Grass = Factory.CreateBoolSet(2, 23, 199, 109, 477, 492);

			public static bool[] GolfGrass = Factory.CreateBoolSet(477, 492);

			public static bool[] Dirt = Factory.CreateBoolSet(default(int));

			public static bool[] Snow = Factory.CreateBoolSet(147);

			public static bool[] Stone = Factory.CreateBoolSet(1, 25, 117, 203);

			public static bool[] Ice = Factory.CreateBoolSet(161, 163, 164, 200);

			public static bool[] Sand = Factory.CreateBoolSet(53, 112, 116, 234);

			public static bool[] HardenedSand = Factory.CreateBoolSet(397, 398, 402, 399);

			public static bool[] Sandstone = Factory.CreateBoolSet(396, 400, 403, 401);

			public static bool[] Thorn = Factory.CreateBoolSet(32, 352, 69, 655);

			public static bool[] Moss = Factory.CreateBoolSet(182, 180, 179, 381, 183, 181, 534, 536, 539, 625, 627);

			public static bool[] MossBrick = Factory.CreateBoolSet(512, 513, 514, 515, 516, 517, 535, 537, 540, 626, 628);

			public static bool Torch(Tile tile, int conversionType)
			{
				if (tile == null || !tile.active() || tile.type != 4)
				{
					return false;
				}
				int num = tile.frameY / 22;
				switch (conversionType)
				{
				case 0:
					if ((uint)(num - 18) <= 2u || num == 22)
					{
						return true;
					}
					break;
				case 11:
					if ((uint)(num - 18) <= 2u)
					{
						return true;

```


---

## 🤖 Assistant · 2026-08-13T06:17:46.543Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Portal colors: portal 0 = hslToRgb(0.12, 1, 0.5) → orange-ish; portal 1 = hslToRgb(0.52, 1, 0.6) → cyan/blue-ish! Wait: hsl(0.52) ≈ 187° → cyan. Repo has: frameX 234/252 → purple [0.42,0.2,0.65] (portal 0 ×0.65), 306/324 → orange [0.65,0.26,0] (portal 1 ×0.65). That's swapped/wrong colors. Portal 0 is orange (hue 0.12 = 43°), portal 1 is cyan (hue 0.52). Repo labels purple for portal 0 and orange for portal 1 → both wrong hue. Let me compute hslToRgb(0.12,1,0.5): H=0.12*360=43.2°, S=1, L=0.5 → pure orange RGB(255, 120, 0)/255 = (1, 0.47, 0). ×0.65 → (0.65, 0.306, 0). hslToRgb(0.52,1,0.6): H=187.2° → cyan (0, 0.798, 1)? Let me compute: L=0.6, S=1 → C=(1-|2*0.6-1|)*1=0.8; H'=0.52*6=3.12; X=C*(1-|H' mod 2 -1|)=0.8*(1-|1.12-1|)=0.8*0.88=0.704; m=L-C/2=0.6-0.4=0.2. H' in [3,4) → (0, X, C)+m = (0.2, 0.904, 1.0). ×0.65 → (0.13, 0.588, 0.65). So repo's [0.42,0.2,0.65] purple and [0.65,0.26,0] orange are both wrong (should be orange (0.65,0.31,0) for portal 0 and cyan-blue (0.13,0.59,0.65) for portal 1). Deviation confirmed.

Now TileID names — need to find where names are defined. The file is structured differently. Let me find names via a different approach: there might be a separate generated file or the const names at class level. Let me grep "public const" in TileID.cs.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:17:47.807Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"= [0-9]*;\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs | grep -v \"CreateBoolSet\\|Factory\\|default\" | head -40; echo ===; grep -c \"\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs; grep -rn \"class TileID\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs",
 "description": "Find tile id constants in TileID.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:17:47.873Z

**📎 ToolResult**

```
426:			for (int i = 0; i < SaveSlopes.Length; i++)
433:	public const ushort Dirt = 0;
435:	public const ushort Stone = 1;
437:	public const ushort Grass = 2;
439:	public const ushort Plants = 3;
441:	public const ushort Torches = 4;
443:	public const ushort Trees = 5;
445:	public const ushort Iron = 6;
447:	public const ushort Copper = 7;
449:	public const ushort Gold = 8;
451:	public const ushort Silver = 9;
453:	public const ushort ClosedDoor = 10;
455:	public const ushort OpenDoor = 11;
457:	public const ushort Heart = 12;
459:	public const ushort Bottles = 13;
461:	public const ushort Tables = 14;
463:	public const ushort Chairs = 15;
465:	public const ushort Anvils = 16;
467:	public const ushort Furnaces = 17;
469:	public const ushort WorkBenches = 18;
471:	public const ushort Platforms = 19;
473:	public const ushort Saplings = 20;
475:	public const ushort Containers = 21;
477:	public const ushort Demonite = 22;
479:	public const ushort CorruptGrass = 23;
481:	public const ushort CorruptPlants = 24;
483:	public const ushort Ebonstone = 25;
485:	public const ushort DemonAltar = 26;
487:	public const ushort Sunflower = 27;
489:	public const ushort Pots = 28;
491:	public const ushort PiggyBank = 29;
493:	public const ushort WoodBlock = 30;
495:	public const ushort ShadowOrbs = 31;
497:	public const ushort CorruptThorns = 32;
499:	public const ushort Candles = 33;
501:	public const ushort Chandeliers = 34;
503:	public const ushort Jackolanterns = 35;
505:	public const ushort Presents = 36;
507:	public const ushort Meteorite = 37;
509:	public const ushort GrayBrick = 38;
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-13T06:17:48.877Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID -iname \"*.cs\" | head -30; echo ===; grep -rn \"CrystalHeart\\|Demonite =\\|Hellstone =\\|Meteorite =\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/*.cs | head",
 "description": "Locate tile id constant definitions"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:17:48.975Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/GenPassNameID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TreeTopID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/MenuID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/ChainID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/ExtrasID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/AmmoID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/ImmunityCooldownID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/PlayerDifficultyID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/ArmorIDs.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/BuffID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/PlayerVariantID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/ContentSamples.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/BiomeConversionID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/PrefixID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TorchID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/WaterStyleID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/SoundID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/LiquidID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/ProjectileDrawLayerID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/AchievementHelperID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/NPCID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/MessageID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/PlayerItemSlotID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/RecipeGroups.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/HousingCategoryID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/PlayerVoiceOverrideID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/DustID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileChangeType.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/PlayerTextureID.cs
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-13T06:18:00.937Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -nE \"public const ushort [A-Za-z0-9_]+ = [0-9]+;\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs | awk -F'[= ;]+' '{print $3\" \"$5}' > /dev/null 2>&1; grep -nE \"public const ushort [A-Za-z0-9_]+ = (20|22|26|27|31|33|34|35|37|42|49|61|70|71|72|77|83|84|92|93|95|96|98|100|125|126|129|133|140|149|160|171|173|174|184|190|204|209|215|235|237|238|270|271|286|302|316|317|318|327|336|340|341|342|343|344|347|348|349|354|356|381|390|391|405|415|416|417|418|429|463|491|500|501|502|503|517|519|528|534|535|536|537|539|540|548|564|568|569|570|572|580|581|582|592|593|594|597|598|613|614|619|620|625|626|627|628|633|634|637|638|656|658|659|660|663|667|687|688|689|690|691|692|695|696|699|703|708|711|717|718|719|739);$\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs",
 "description": "Resolve tile id names for audit targets"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:18:08.921Z

**📎 ToolResult**

```
473:	public const ushort Saplings = 20;
477:	public const ushort Demonite = 22;
485:	public const ushort DemonAltar = 26;
487:	public const ushort Sunflower = 27;
495:	public const ushort ShadowOrbs = 31;
499:	public const ushort Candles = 33;
501:	public const ushort Chandeliers = 34;
503:	public const ushort Jackolanterns = 35;
507:	public const ushort Meteorite = 37;
517:	public const ushort HangingLanterns = 42;
531:	public const ushort WaterCandle = 49;
555:	public const ushort JunglePlants = 61;
573:	public const ushort MushroomGrass = 70;
575:	public const ushort MushroomPlants = 71;
577:	public const ushort MushroomTrees = 72;
587:	public const ushort Hellforge = 77;
599:	public const ushort MatureHerbs = 83;
601:	public const ushort BloomingHerbs = 84;
617:	public const ushort Lampposts = 92;
619:	public const ushort Lamps = 93;
623:	public const ushort ChineseLanterns = 95;
625:	public const ushort CookingPots = 96;
629:	public const ushort SkullLanterns = 98;
633:	public const ushort Candelabras = 100;
683:	public const ushort CrystalBall = 125;
685:	public const ushort DiscoBall = 126;
691:	public const ushort Crystals = 129;
699:	public const ushort AdamantiteForge = 133;
713:	public const ushort DemoniteBrick = 140;
731:	public const ushort HolidayLights = 149;
753:	public const ushort RainbowBrick = 160;
775:	public const ushort ChristmasTree = 171;
779:	public const ushort PlatinumCandelabra = 173;
781:	public const ushort PlatinumCandle = 174;
801:	public const ushort LongMoss = 184;
813:	public const ushort MushroomBlock = 190;
841:	public const ushort Crimtane = 204;
851:	public const ushort Cannon = 209;
863:	public const ushort Campfire = 215;
903:	public const ushort Teleporter = 235;
907:	public const ushort LihzahrdAltar = 237;
909:	public const ushort PlanteraBulb = 238;
973:	public const ushort FireflyinaBottle = 270;
975:	public const ushort LightningBuginaBottle = 271;
1005:	public const ushort GlowingSnailCage = 286;
1037:	public const ushort GlassKiln = 302;
1065:	public const ushort BlueJellyfishBowl = 316;
1067:	public const ushort GreenJellyfishBowl = 317;
1069:	public const ushort PinkJellyfishBowl = 318;
1087:	public const ushort Lavafall = 327;
1105:	public const ushort LivingFire = 336;
1113:	public const ushort LivingCursedFire = 340;
1115:	public const ushort LivingDemonFire = 341;
1117:	public const ushort LivingFrostFire = 342;
1119:	public const ushort LivingIchor = 343;
1121:	public const ushort LivingUltrabrightFire = 344;
1127:	public const ushort CrimtaneBrick = 347;
1129:	public const ushort ShroomitePlating = 348;
1131:	public const ushort MushroomStatue = 349;
1141:	public const ushort BewitchingTable = 354;
1145:	public const ushort Sundial = 356;
1195:	public const ushort LavaMoss = 381;
1213:	public const ushort LavaLamp = 390;
1215:	public const ushort CageEnchantedNightcrawler = 391;
1243:	public const ushort Fireplace = 405;
1263:	public const ushort LunarBlockSolar = 415;
1265:	public const ushort LunarBlockVortex = 416;
1267:	public const ushort LunarBlockNebula = 417;
1269:	public const ushort LunarBlockStardust = 418;
1291:	public const ushort WireBulb = 429;
1359:	public const ushort DefendersForge = 463;
1415:	public const ushort VoidVault = 491;
1433:	public const ushort SolarBrick = 500;
1435:	public const ushort VortexBrick = 501;
1437:	public const ushort NebulaBrick = 502;
1439:	public const ushort StardustBrick = 503;
1467:	public const ushort LavaMossBrick = 517;
1471:	public const ushort Cattail = 519;
1489:	public const ushort MushroomVines = 528;
1501:	public const ushort KryptonMoss = 534;
1503:	public const ushort KryptonMossBrick = 535;
1505:	public const ushort XenonMoss = 536;
1507:	public const ushort XenonMossBrick = 537;
1511:	public const ushort ArgonMoss = 539;
1513:	public const ushort ArgonMossBrick = 540;
1529:	public const ushort PottedPlants2 = 548;
1561:	public const ushort PlasmaLamp = 564;
1569:	public const ushort PinkFairyJar = 568;
1571:	public const ushort GreenFairyJar = 569;
1573:	public const ushort BlueFairyJar = 570;
1577:	public const ushort SoulBottles = 572;
1593:	public const ushort HellButterflyJar = 580;
1595:	public const ushort LavaflyinaBottle = 581;
1597:	public const ushort MagmaSnailCage = 582;
1617:	public const ushort BrazierSuspended = 592;
1619:	public const ushort VolcanoSmall = 593;
1621:	public const ushort VolcanoLarge = 594;
1627:	public const ushort TeleportationPylon = 597;
1629:	public const ushort LavafishBowl = 598;
1659:	public const ushort PottedLavaPlants = 613;
1661:	public const ushort PottedLavaPlantTendrils = 614;
1671:	public const ushort TruffleWormCage = 619;
1673:	public const ushort EmpressButterflyJar = 620;
1683:	public const ushort VioletMoss = 625;
1685:	public const ushort VioletMossBrick = 626;
1687:	public const ushort RainbowMoss = 627;
1689:	public const ushort RainbowMossBrick = 628;
1699:	public const ushort AshGrass = 633;
1701:	public const ushort TreeAsh = 634;
1707:	public const ushort AshPlants = 637;
1709:	public const ushort AshVines = 638;
1745:	public const ushort GlowTulip = 656;
1749:	public const ushort ShimmerMonolith = 658;
1751:	public const ushort ShimmerBlock = 659;
1753:	public const ushort ShimmerflyinaBottle = 660;
1759:	public const ushort Moondial = 663;
1767:	public const ushort ShimmerBrick = 667;
1807:	public const ushort LavaMossBlock = 687;
1809:	public const ushort ArgonMossBlock = 688;
1811:	public const ushort KryptonMossBlock = 689;
1813:	public const ushort XenonMossBlock = 690;
1815:	public const ushort VioletMossBlock = 691;
1817:	public const ushort RainbowMossBlock = 692;
1823:	public const ushort DemonAltarReplica = 695;
1825:	public const ushort ShadowOrbsReplica = 696;
1831:	public const ushort DeadCellsPotionStation = 699;
1839:	public const ushort JunglePlantsEcho = 703;
1849:	public const ushort Shimmerfall = 708;
1855:	public const ushort RainbowBoulder = 711;
1867:	public const ushort LavaCloud = 717;
1869:	public const ushort StarCloud = 718;
1871:	public const ushort RainbowCloud = 719;
1911:	public const ushort JellyfishBlock = 739;

```


---

## 🤖 Assistant · 2026-08-13T06:18:17.078Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting: tile 20 = Saplings! case 20 → frameX/18 in 30..32 → (0.325,0.15,0.05). That's for gem saplings (amethyst etc.? no—gem saplings are 590). Actually saplings tile 20 with frameX 30-32... those are... hmm, whatever. Repo's acorn_sapling uses sheet 20 without light. The vanilla case 20 applies to Saplings frames 30-32 which are gem saplings? No, gem saplings is 590. Saplings 30-32 = "ash sapling"? Whatever — note repo acorn_sapling (sheet 20) has no light → vanilla would emit for frames 540..? frameX/18 in 30..32 means frameX 540-593. Those are likely the 1.4.4 gem saplings styles placed in tile 20. Minor: report as missing condition.

Also tile 171 = ChristmasTree in vanilla — repo v_171_christmas_tree sheet 171 ✓ correct. And LogicSensor is 423 (case 171 in the switch was Christmas tree? no). Wait, the switch case 171 at :2517 is the `frameY & 0x3C00` logic — that's LogicSensor. But tile 171 = ChristmasTree?? Hmm, no: vanilla tile 171... let me check: from the grep, line 775: `public const ushort ChristmasTree = 171;`. But TileLightScanner case 171 with frameY & 0x3C00 >> 10 logic (lamps on/off) is clearly LogicSensor. Hmm — maybe LogicSensor is 171 and ChristmasTree is 199? The grep found "ChristmasTree = 171". And what about LogicSensor? Let me check line for LogicSensor. Also TileID.Sets: line 12 mentioned Thorn = Factory.CreateBoolSet(32, 352, 69, 655) — 655 = PlanteraThorns ✓ repo v_655. So the id mapping is standard 1.4.4.

Hmm wait — the decompiled TileID.cs may be inaccurate? No. Let me grep LogicSensor.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:18:18.197Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -nE \"LogicSensor|ChristmasTree|WeatherVane|FogMachine|PlasmaLamp|AmberGemspark|AmethystGemspark\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs | head; echo ---; grep -rn \"public const ushort\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs | sed -n '1,3p'",
 "description": "Verify LogicSensor id"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:18:18.271Z

**📎 ToolResult**

```
775:	public const ushort ChristmasTree = 171;
943:	public const ushort AmethystGemsparkOff = 255;
955:	public const ushort AmberGemsparkOff = 261;
957:	public const ushort AmethystGemspark = 262;
969:	public const ushort AmberGemspark = 268;
1279:	public const ushort LogicSensor = 423;
1413:	public const ushort WeatherVane = 490;
1561:	public const ushort PlasmaLamp = 564;
1563:	public const ushort FogMachine = 565;
---
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs:433:	public const ushort Dirt = 0;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs:435:	public const ushort Stone = 1;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs:437:	public const ushort Grass = 2;

```


---

## 🤖 Assistant · 2026-08-13T06:18:18.561Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"tileLighted\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head -40",
 "description": "Find tileLighted assignments in Main.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:18:18.613Z

**📎 ToolResult**

```
1419:	public static bool[] tileLighted = new bool[TileID.Count];
7015:		tileLighted[517] = true;
7019:		tileLighted[687] = true;
7023:		tileLighted[535] = true;
7027:		tileLighted[689] = true;
7031:		tileLighted[537] = true;
7035:		tileLighted[690] = true;
7039:		tileLighted[540] = true;
7043:		tileLighted[688] = true;
7047:		tileLighted[626] = true;
7051:		tileLighted[691] = true;
7055:		tileLighted[628] = true;
7059:		tileLighted[692] = true;
7060:		tileLighted[592] = true;
7061:		tileLighted[656] = true;
7062:		tileLighted[701] = true;
7063:		tileLighted[356] = true;
7064:		tileLighted[663] = true;
7262:		tileLighted[568] = true;
7266:		tileLighted[569] = true;
7270:		tileLighted[570] = true;
7274:		tileLighted[580] = true;
7277:		tileLighted[582] = true;
7280:		tileLighted[619] = true;
7284:		tileLighted[620] = true;
7288:		tileLighted[572] = true;
7294:		tileLighted[564] = true;
7303:		tileLighted[593] = true;
7307:		tileLighted[594] = true;
7308:		tileLighted[548] = true;
7309:		tileLighted[613] = true;
7310:		tileLighted[614] = true;
7321:		tileLighted[519] = true;
7333:		tileLighted[637] = true;
7342:		tileLighted[215] = true;
7369:		tileLighted[173] = true;
7370:		tileLighted[174] = true;
7372:		tileLighted[160] = true;
7373:		tileLighted[149] = true;
7417:		tileLighted[711] = true;

```


---

## 🤖 Assistant · 2026-08-13T06:18:28.796Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
So tile 171 is ChristmasTree, and the TileLightScanner `case 171` with 0x3C00 logic is... hmm that seems odd. Wait — maybe the decompiled switch cases are correct and case 171 is indeed... Christmas tree with lamp frame bits? No. Actually hold on: maybe in the decompiled TileLightScanner, `case 171` refers to... Let me reconsider: The 0x3C00 >> 10 frameY bitfield is used for "LogicSensor" tile 423? In vanilla 1.4.4 source (ILSpy), TileLightScanner case 171 = LogicSensor? Hmm.

Actually, I recall in the real Terraria source: 
```
case 171:
    if (tile.frameX < 10) { x -= tile.frameX; y -= tile.frameY; }
    switch ((Main.tile[x, y].frameY & 0x3C00) >> 10)
```
And TileID 171 in actual 1.4.4 is LogicSensor = 171? Let me double check with the vanilla Main.cs where LogicSensor lamp colors are set, or check TileID line 775 context. The decompiled TileID.cs says ChristmasTree = 171. Hmm, but actual Terraria TileID: ChristmasTree = 171? Let me verify: In 1.4, Christmas Tree is placeable from item 1739 (Christmas tree). TileID for it... TEdit lists 171 as "Christmas Tree". Yes! TEdit tiles.json: 171 = "Christmas Tree". And LogicSensor = 423 ✓ (TEdit 423 = Logic Sensor). So the TileLightScanner case 171 with frameY bits = ChristmasTree?? That doesn't make sense semantically... unless the decompiler mis-numbered.

Hmm, wait. Maybe it's right: ChristmasTree tile uses frameY bits 0x3C00 to store the "star/lights" on-off state for wiring! Yes! Christmas tree has logic: HitWire toggles lights on the tree, stored in frameY bits. That's exactly it — Terraria's ChristmasTree stores lamp colors in frameY & 0x3C00. I remember now: in Main.DrawTiles, `int num = (tile.frameY & 0x3C00) >> 10` for ChristmasTree lights. Yes! So case 171 = ChristmasTree ✓. And repo v_171_christmas_tree has NO light → missing (12 light-color variants).

OK. Now let me get the full tileLighted list from Main.cs to cross-check the repo's def.light entries against tiles vanilla considers lighted. Let me dump all tileLighted lines with context to associate ids. Actually the ids alone suffice.
````

</details>


---

## 🤖 Assistant · 2026-08-13T06:18:29.360Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -oE \"tileLighted\\[[0-9]+\\]\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | grep -oE \"[0-9]+\" | sort -n | uniq | tr '\\n' ' '",
 "description": "List all tileLighted ids"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:18:29.553Z

**📎 ToolResult**

```
4 17 19 20 22 26 27 31 33 34 35 37 42 49 58 61 70 71 72 76 77 83 84 92 93 95 96 98 100 109 125 126 129 133 140 149 160 171 173 174 184 190 204 209 215 237 238 270 271 286 302 316 317 318 327 336 340 341 342 343 344 346 347 348 349 350 354 356 370 372 381 390 391 405 415 416 417 418 429 463 491 500 501 502 503 517 519 528 534 535 536 537 539 540 548 564 568 569 570 572 578 580 581 582 592 593 594 597 598 613 614 619 620 625 626 627 628 633 634 637 638 646 656 658 659 660 663 667 684 687 688 689 690 691 692 695 696 699 701 703 708 711 717 718 719 739

```


---

## 🤖 Assistant · 2026-08-13T06:18:29.823Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"class FlickerClock\" -A 80 ~/Project/GLM/SandboxWorld/game/src/lighting/SkyColor.ts",
 "description": "Read FlickerClock implementation"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:18:30.208Z

**📎 ToolResult**

```
93:export class FlickerClock {
94-  /** mouseTextColor:190↔255 步进 1/帧(字节环绕) */
95-  mouseTextColor = 255;
96-  private mouseDir = -1;
97-  /** cursorAlpha(Main.cs:51897-51904):0.6↔1 步进 0.015/帧,驱动光标/心/星呼吸 */
98-  cursorAlpha = 1;
99-  private cursorDir = -1;
100-  /** demonTorch:0↔1 步进 0.01/帧 */
101-  demonTorch = 0;
102-  private demonDir = 1;
103-  /** Disco RGB:6 相循环,每通道步进 7/帧(0-255) */
104-  discoR = 255; discoG = 0; discoB = 0;
105-  private discoStyle = 0;
106-
107-  /** cursorScale(Main.cs:51905):= cursorAlpha*0.3 + 0.8,资源条 flag 心/星缩放脉冲源 */
108-  get cursorScale(): number { return this.cursorAlpha * 0.3 + 0.8; }
109-
110-  tick(): void {
111-    this.cursorAlpha += this.cursorDir * 0.015;
112-    if (this.cursorAlpha >= 1) { this.cursorAlpha = 1; this.cursorDir = -1; }
113-    else if (this.cursorAlpha <= 0.6) { this.cursorAlpha = 0.6; this.cursorDir = 1; }
114-
115-    this.mouseTextColor += this.mouseDir;
116-    if (this.mouseTextColor >= 255) this.mouseDir = -1;
117-    else if (this.mouseTextColor <= 190) this.mouseDir = 1;
118-
119-    this.demonTorch += this.demonDir * 0.01;
120-    if (this.demonTorch > 1) { this.demonTorch = 1; this.demonDir = -1; }
121-    else if (this.demonTorch < 0) { this.demonTorch = 0; this.demonDir = 1; }
122-
123-    // 6 相:G↑ → R↓ → B↑ → G↓ → R↑ → B↓(每帧步进 7,满额切换下一相)
124-    const STEP = 7;
125-    switch (this.discoStyle) {
126-      case 0: this.discoG += STEP; if (this.discoG >= 255) { this.discoG = 255; this.discoStyle = 1; } break;
127-      case 1: this.discoR -= STEP; if (this.discoR <= 0) { this.discoR = 0; this.discoStyle = 2; } break;
128-      case 2: this.discoB += STEP; if (this.discoB >= 255) { this.discoB = 255; this.discoStyle = 3; } break;
129-      case 3: this.discoG -= STEP; if (this.discoG <= 0) { this.discoG = 0; this.discoStyle = 4; } break;
130-      case 4: this.discoR += STEP; if (this.discoR >= 255) { this.discoR = 255; this.discoStyle = 5; } break;
131-      case 5: this.discoB -= STEP; if (this.discoB <= 0) { this.discoB = 0; this.discoStyle = 0; } break;
132-    }
133-  }
134-
135-  /** 恶魔火把色插值(TorchID DemonTorchLight:37-45) */
136-  demonTorchColor(): [number, number, number] {
137-    const d = this.demonTorch;
138-    return [0.5 * d + 1 * (1 - d), 0.3, 1 * d + 0.5 * (1 - d)];
139-  }
140-
141-  /** 微光火把色(TorchID ShimmerTorchLight:48-62;num/num2 由 mouseTextColor 派生钳 0-1) */
142-  shimmerTorchColor(): [number, number, number] {
143-    const num = Math.min(1, Math.max(0, (this.mouseTextColor - 190) / 65));
144-    const num2 = 1 - num;
145-    return [num * 0.9, num2 * 0.55, num * 1.2];
146-  }
147-
148-  discoColor(): [number, number, number] {
149-    return [this.discoR / 255, this.discoG / 255, this.discoB / 255];
150-  }
151-}

```


---

## 🤖 Assistant · 2026-08-13T06:18:34.305Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Check vanilla DemonTorchLight and ShimmerTorchLight implementations. They're in Terraria.ID? Let me find ITorchLightProvider implementations.

Also check mouseTextColor vanilla behavior: Main.mouseTextColor oscillates 190..255 (step 1 per frame?) — repo matches (190↔255). Vanilla: in Main.Update, `mouseTextColor -= mouseTextColorTime; ...` Let me verify quickly. Actually vanilla: mouseTextColor moves toward 255 at rate... Let me grep.

Also demonTorch: vanilla DoUpdate_AnimateTileGlows: demonTorch += 0.01f * (demonTorch < 1 ? ...)? Repo claims ±0.01 clamped 0..1, period 200t. Let me verify from Main.cs :18089-18100.

Let me check the torch light providers.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:18:34.848Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"class DemonTorchLight\\|class DiscoTorchLight\\|class ShimmerTorchLight\\|class ConstantTorchLight\\|class TorchLightProvider\" ~/Project/GLM/SandboxWorld/Terarria1456/ 2>/dev/null | head",
 "description": "Find torch light provider classes"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:18:35.033Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-13T06:18:35.523Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"demonTorch\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head -20; echo ---; grep -n \"mouseTextColor\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head -12",
 "description": "Check demonTorch and mouseTextColor dynamics"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:18:35.597Z

**📎 ToolResult**

```
1286:	public static float demonTorch = 1f;
1288:	public static int demonTorchDir = 1;
18090:		demonTorch += (float)demonTorchDir * 0.01f;
18091:		if (demonTorch > 1f)
18093:			demonTorch = 1f;
18094:			demonTorchDir = -1;
18096:		if (demonTorch < 0f)
18098:			demonTorch = 0f;
18099:			demonTorchDir = 1;
---
1741:	public static byte mouseTextColor;
1743:	public static int mouseTextColorChange = 1;
18066:		mouseTextColor += (byte)mouseTextColorChange;
18067:		if (mouseTextColor >= byte.MaxValue)
18069:			mouseTextColorChange = -1;
18071:		if (mouseTextColor <= 190)
18073:			mouseTextColorChange = 1;
20062:		new Microsoft.Xna.Framework.Color(mouseTextColor, mouseTextColor, mouseTextColor, mouseTextColor);
20095:		float num3 = (float)(int)mouseTextColor / 255f;
20096:		Microsoft.Xna.Framework.Color baseColor = new Microsoft.Xna.Framework.Color(mouseTextColor, mouseTextColor, mouseTextColor, mouseTextColor);
20099:			baseColor = new Microsoft.Xna.Framework.Color((byte)(255f * num3), (byte)(masterColor * 200f * num3), 0, mouseTextColor);
20103:			baseColor = new Microsoft.Xna.Framework.Color((byte)((float)DiscoR * num3), (byte)((float)DiscoG * num3), (byte)((float)DiscoB * num3), mouseTextColor);

```


---

## 🤖 Assistant · 2026-08-13T06:18:37.977Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
demonTorch and mouseTextColor match repo.

Torch light providers not found by that grep — maybe they're in Terraria.GameContent or as separate files. Let me search for "DemonTorchLight".
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:18:38.588Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rln \"DemonTorchLight\" ~/Project/GLM/SandboxWorld/Terarria1456/ | head; echo ---; grep -rn \"DemonTorchLight\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TorchID.cs | head",
 "description": "Locate DemonTorchLight definition"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:18:38.746Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TorchID.cs
---
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TorchID.cs:37:	private struct DemonTorchLight : ITorchLightProvider
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TorchID.cs:144:		array[7] = default(DemonTorchLight);

```


---

## 🤖 Assistant · 2026-08-13T06:18:40.454Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TorchID.cs",
 "limit": 70
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:18:40.464Z

**📎 ToolResult**

```
1	using System.Runtime.InteropServices;
2	using Microsoft.Xna.Framework;
3	
4	namespace Terraria.ID;
5	
6	public static class TorchID
7	{
8		public class Sets
9		{
10			public static SetFactory Factory = new SetFactory(Count);
11	
12			public static bool[] IsABiomeTorch = Factory.CreateBoolSet(false, 0, 18, 19, 20, 21, 23, 13, 7, 9, 22, 16);
13		}
14	
15		private interface ITorchLightProvider
16		{
17			void GetRGB(out float r, out float g, out float b);
18		}
19	
20		private struct ConstantTorchLight(float Red, float Green, float Blue) : ITorchLightProvider
21		{
22			public float R = Red;
23	
24			public float G = Green;
25	
26			public float B = Blue;
27	
28			public void GetRGB(out float r, out float g, out float b)
29			{
30				r = R;
31				g = G;
32				b = B;
33			}
34		}
35	
36		[StructLayout(LayoutKind.Sequential, Size = 1)]
37		private struct DemonTorchLight : ITorchLightProvider
38		{
39			public void GetRGB(out float r, out float g, out float b)
40			{
41				r = 0.5f * Main.demonTorch + (1f - Main.demonTorch);
42				g = 0.3f;
43				b = Main.demonTorch + 0.5f * (1f - Main.demonTorch);
44			}
45		}
46	
47		[StructLayout(LayoutKind.Sequential, Size = 1)]
48		private struct ShimmerTorchLight : ITorchLightProvider
49		{
50			public void GetRGB(out float r, out float g, out float b)
51			{
52				float num = 0.9f;
53				float num2 = 0.9f;
54				num += (float)(270 - Main.mouseTextColor) / 900f;
55				num2 += (float)(270 - Main.mouseTextColor) / 125f;
56				num = MathHelper.Clamp(num, 0f, 1f);
57				num2 = MathHelper.Clamp(num2, 0f, 1f);
58				r = num * 0.9f;
59				g = num2 * 0.55f;
60				b = num * 1.2f;
61			}
62		}
63	
64		[StructLayout(LayoutKind.Sequential, Size = 1)]
65		private struct DiscoTorchLight : ITorchLightProvider
66		{
67			public void GetRGB(out float r, out float g, out float b)
68			{
69				r = (float)Main.DiscoR / 255f;
70				g = (float)Main.DiscoG / 255f;

```


---

## 🤖 Assistant · 2026-08-13T06:18:50.178Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
DemonTorchLight ✓ repo matches.
ShimmerTorchLight: vanilla r = clamp(0.9+(270-mouse)/900, 0..1) * 0.9; g = clamp(0.9+(270-mouse)/125, 0..1)*0.55; b = num*1.2.

Repo shimmerTorchColor: num = clamp((mouseTextColor-190)/65, 0..1); num2=1-num; return [num*0.9, num2*0.55, num*1.2].

Vanilla: mouse ∈ [190,255]. (270-mouse)/900 ∈ [15/900=0.0167, 80/900=0.0889] → num (r base) = 0.9167..0.9889 → r = 0.825..0.89. Repo: r = ((mouse-190)/65)*0.9 = 0..0.9. Mismatch: repo uses a linear ramp 0→0.9; vanilla gives 0.825→0.89. 
g: vanilla num2 = clamp(0.9+(270-mouse)/125,0,1) = clamp(0.9+[0.12,0.64]) = 1.02..1.54 → clamped... wait (270-mouse)/125 for mouse=255 → 0.12 → 1.02; mouse=190 → 0.64 → 1.54. So num2 = 1.02..1.54 (not clamped at 1 for lower bound? clamp(1.02..1.54, 0, 1) = 1.0 always! Since min 1.02 > 1 → g = 1.0*0.55 = 0.55 constant!

So vanilla shimmer torch: r = 0.9167..0.9889 * 0.9 → wait no: `num` after adding is clamped then r = num*0.9. num = clamp(0.9+(270-mouse)/900, 0, 1) = 0.9167..0.9889 → r = 0.825..0.89. b = num*1.2 = 1.1..1.187. g = 0.55 constant.

Repo: r = 0..0.9, g = 0.55..0, b = 0..1.2 → significant deviation. So shimmerTorchColor is wrong.

Let me double check Main.mouseTextColor range: increments by mouseTextColorChange (±1) each Update, flipping at >=255 and <=190. So range [190,255] ✓.

So shimmer torch in repo flickers from black to bright, vanilla is nearly constant (r 0.825-0.89, g 0.55, b 1.1-1.19). Deviation.

Now DiscoTorchLight = Main.DiscoR/255 etc ✓ repo discoColor. Need to check Main.DiscoR dynamics vs repo 6-phase step-7. Let me check Main.cs DiscoR update.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:18:50.601Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"DiscoR\\b\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | sed -n '1,25p'",
 "description": "Check Disco color dynamics"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:18:50.641Z

**📎 ToolResult**

```
1018:	public static int DiscoR = 255;
19455:			DiscoR -= num;
19456:			if (DiscoR <= 0)
19458:				DiscoR = 0;
19482:			DiscoR += num;
19483:			if (DiscoR >= 255)
19485:				DiscoR = 255;
20103:			baseColor = new Microsoft.Xna.Framework.Color((byte)((float)DiscoR * num3), (byte)((float)DiscoG * num3), (byte)((float)DiscoB * num3), mouseTextColor);
20424:			result = new Microsoft.Xna.Framework.Color((byte)DiscoR, (byte)DiscoG, (byte)DiscoB);
32455:					Microsoft.Xna.Framework.Color color84 = new Microsoft.Xna.Framework.Color(DiscoR, DiscoG, DiscoB, 127);
34333:							newColor5 = new Microsoft.Xna.Framework.Color(DiscoR, DiscoG, DiscoB);
34942:				stringColor = new Microsoft.Xna.Framework.Color(DiscoR, DiscoG, DiscoB);
38192:				color2 = new Microsoft.Xna.Framework.Color(DiscoR, DiscoG, DiscoB);
41575:			color = new Microsoft.Xna.Framework.Color((byte)DiscoR, (byte)DiscoG, (byte)DiscoB);

```


---

## 🤖 Assistant · 2026-08-13T06:18:51.022Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"LIGHT_TOGGLE\\|export function lightIsOn\" -A 60 ~/Project/GLM/SandboxWorld/game/src/world/wiring/devices.ts | head -100",
 "description": "Read lightIsOn gate logic"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:18:51.062Z

**📎 ToolResult**

```
522:export const LIGHT_TOGGLE: Record<number, ['x' | 'y', number]> = {
523-  4: ['x', 66],
524-  33: ['x', 18], 174: ['x', 18], 49: ['x', 18], 372: ['x', 18],
525-  42: ['x', 18], 92: ['x', 18], 93: ['x', 18],
526-  95: ['x', 36], 100: ['x', 36], 126: ['x', 36], 173: ['x', 36], 564: ['x', 36],
527-  34: ['x', 54], 149: ['x', 54],
528-  215: ['y', 36],
529-};
530-
531-/** 该格灯光是否点亮(非灯器件恒 true;供 LightingEngine 查询) */
532:export function lightIsOn(sheet: number, frameX: number, frameY: number): boolean {
533:  const t = LIGHT_TOGGLE[sheet];
534-  if (!t) return true;
535-  const v = t[0] === 'x' ? frameX : frameY;
536-  return v % (2 * t[1]) < t[1];
537-}
538-
539-/** HitWireSingle 器件主分发表。返回 true = 已处理 */
540-export function deviceTable(w: Wiring, ctx: DeviceCtx, sheet: number, x: number, y: number): boolean {
541-  const st = w.st;
542-  const i = st.idx(x, y);
543-  switch (sheet) {
544-    case 4: // 火把 frameX ±66(:1207-1213)
545-      flipCell(w, x, y, 66);
546-      return true;
547-    case 10: // 关门 → 开(随机方向+反向,原版 :1171-1188)
548-      ctx.doorOpen(x, y);
549-      return true;
550-    case 11:
551-      ctx.doorClose(x, y);
552-      return true;
553-    case 15: { // 马桶椅样式（Wiring.cs:1498-1509 与 tile 497 共用分支；frameY/40==1 或 20）
554-      if (Math.floor(st.frameY[i] / 40) !== 1 && Math.floor(st.frameY[i] / 40) !== 20) return true;
555-      fireworkToilet(w, ctx, x, y);
556-      return true;
557-    }
558-    case 33: case 174: case 49: case 372: // 蜡烛族 frameX ±18(:1472-1480)
559-      flipCell(w, x, y, 18);
560-      return true;
561-    case 34: // 吊灯 3×3 frameX ±54(:1405-1428)
562-      flipBlock(w, x, y, 108, 54, 3, 3, 'x', 54, 54);
563-      return true;
564-    case 35: case 139: // 南瓜灯/八音盒：SwitchMB（WorldGen.cs:50977-51021；Wiring.cs:2019-2022）
565-      switchMB(w, x, y);
566-      return true;
567-    case 207: // 喷泉：SwitchFountain（WorldGen.cs:51171-51209；Wiring.cs:2023）
568-      switchFountain(w, x, y);
569-      return true;
570-    case 410: case 480: case 509: case 657: case 658: case 720: case 721: case 725: case 733:
571-      // 天塔柱族：SwitchMonolith（WorldGen.cs:51023-51169；Wiring.cs:2032-2036）
572-      switchMonolith(w, x, y);
573-      return true;
574-    case 42: // 挂链灯笼 1×2 frameX ±18(:1214-1227)
575-      flipBlock(w, x, y, 36, 36, 1, 2, 'x', 18, 18);
576-      return true;
577-    case 92: // 路灯柱 1×6 frameX ±18(:1483-1494)
578-      flipBlock(w, x, y, 18, 108, 1, 6, 'x', 18, 18);
579-      return true;
580-    case 93: // 蒂基火炬 1×3 frameX ±18(:1228-1243)
581-      flipBlock(w, x, y, 18, 54, 1, 3, 'x', 18, 18);
582-      return true;
583-    case 95: case 100: case 126: case 173: case 564: // 2×2 灯具族 frameX ±36(:1381-1404)
584-      flipBlock(w, x, y, 72, 36, 2, 2, 'x', 36, 36);
585-      return true;
586-    case 105:
587-      fireStatue(w, ctx, x, y);
588-      return true;
589-    case 130: { // 通电石:上方有宝箱则不缩(:878-884)
590-      const above = y > 0 ? w.sheetOf(x, y - 1) : -1;
591-      if (above === 21 || above === 88 || above === 467) return true;
592-      swapTile(w, x, y, 'v_130_active_stone_block', 'v_131_inactivestoneblock');
593-      return true;

```


---

## 🤖 Assistant · 2026-08-13T06:19:08.352Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The lightIsOn gate: torch sheet 4 → frameX % 132 < 66. Vanilla case 4: `if (tile.frameX < 66)` — i.e., only frameX 0..65 (lit frames 0? and 22? and 44?). Note vanilla gate is frameX < 66, not modulo. FrameX values for torch: 0 (lit), 66 (unlit). Torch is 1 tile wide, frameX toggles 0/66 via wiring. So frameX < 66 ⇔ lit ✓. Repo's modulo (2*66=132) handles 0/66 fine. OK equivalent for torch.

For sheet 33 (candle): repo gate frameX % 36 < 18. Vanilla: frameX == 0 (case 33 requires frameX==0). Vanilla candle frames: frameX 0 = lit, 18 = unlit. Repo gate: frameX%36<18 → 0 ✓ lit, 18 → 18%36=18 not <18 → off ✓. Equivalent for the simple toggle case. But note vanilla requires frameX==0 exactly — for a 1-wide candle it's the same.

Hmm but careful for candle: vanilla `case 33: if (tile.frameX != 0) break;` — yes frameX must be exactly 0.

Sheet 92 lampposts: vanilla `frameY <= 18 && frameX == 0`. Repo gate: frameX % 36 < 18 → frameX 0 ✓, 18 off ✓. But vanilla also requires frameY<=18! Lamppost is 1 wide × 6 tall; the wiring flip moves the whole column. The repo's lightIsOn gate doesn't check frameY, so for lamp posts the lower 5 tiles (frameY 18..90) would... hmm wait, frameY for multi-tile: each cell has its own frameY offset. For lampposts, frames: the lamp head is at frameY 0 and pole below at 18,36,54,72,90. Vanilla gate frameY<=18 means only the top two cells (frameY 0 and 18) emit light! Repo's gate doesn't check frameY → all 6 cells emit light → deviation (lamppost light column too tall). Similarly the def light [255,255,255] applies to all cells.

Sheet 93 lamps: vanilla gate frameX==0 && frameY/54 style. Repo gate frameX%36<18 → frameX 0 ✓. But Lamps is 1 wide × 3 tall: frameY 0,18,36 — vanilla applies the same style color to all rows? case 93 requires frameX==0 only (no frameY gate) — and style = frameY/54. Hmm frameY max 36 so style 0 always. Fine — all 3 cells emit. ✓

Sheet 215 campfire: repo gate frameY % 72 < 36. Vanilla gate: frameY < 36. Campfire is 3×2: cells frameY 0,18. Vanilla frameY<36 → both rows emit ✓ (frameY 0 and 18). But wait — the campfire's "off" state is frameY shifted +36. So gate equivalent ✓.

Sheet 34 chandelier: vanilla gate frameX % 108 < 54 (half of the 2-frame 108px cycle). Repo gate frameX % 108 < 54 ✓ matches.

Sheet 564 plasma lamp: repo gate frameX%72<36; vanilla gate frameX<36. Plasma lamp is 2 wide: cells frameX 0,18 lit; 36,54 unlit. Equivalent ✓.

Sheet 149: repo gate frameX%108<54 vs vanilla frameX<=36. Holiday lights: 1-wide tile, frameX 0 lit, 54 unlit. Equivalent ✓.

Sheet 95: repo gate frameX%72<36 vs vanilla frameX<36. Chinese lantern 2×2: lit frameX 0/18, unlit 36/54 ✓ equivalent.

Sheet 100: repo gate frameX%72<36 vs vanilla frameX<36 ✓ (candelabra 2×2). Plus style frameY/36 — repo ignores style (frameY rows for variants). Deviation noted already (only default color).

Sheet 42 lantern: specialTileLight handles frameX!==0 → null ✓ (matches vanilla frameX==0 gate).

Sheet 126 disco: gate frameX<36 ✓ (2×2; lit frames 0,18).

Sheet 174: gate frameX%36<18 ✓ (vanilla frameX==0).

Sheet 49: gate frameX%36<18 ✓ (vanilla frameX==0).

Sheet 372: gate frameX%36<18 ✓ (vanilla frameX==0).

Missing gates in LIGHT_TOGGLE: 356/663 (sundial/moondial cooldown), 658 (aether monolith: invisibleBlock gate + frameY/54 scaling), 646 (shadow candle frameX==0), 20 (sapling frames), 184, 26/31, 61/703, 597 pylon styles, 548, 592 (frameY>0), 593/594, 129, 519 (frameY==90), 83/84 (84 handled in special), 171, 238, 235, 327, etc.

Now check the Disco animation in vanilla Main.cs around 19440-19490 to compare with repo's 6-phase step 7.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:19:08.737Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '19440,19500p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "description": "Read vanilla Disco color animation"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:19:08.773Z

**📎 ToolResult**

```
	private void DoUpdate_AnimateDiscoRGB()
	{
		int num = 7;
		if (DiscoStyle == 0)
		{
			DiscoG += num;
			if (DiscoG >= 255)
			{
				DiscoG = 255;
				DiscoStyle++;
			}
		}
		if (DiscoStyle == 1)
		{
			DiscoR -= num;
			if (DiscoR <= 0)
			{
				DiscoR = 0;
				DiscoStyle++;
			}
		}
		if (DiscoStyle == 2)
		{
			DiscoB += num;
			if (DiscoB >= 255)
			{
				DiscoB = 255;
				DiscoStyle++;
			}
		}
		if (DiscoStyle == 3)
		{
			DiscoG -= num;
			if (DiscoG <= 0)
			{
				DiscoG = 0;
				DiscoStyle++;
			}
		}
		if (DiscoStyle == 4)
		{
			DiscoR += num;
			if (DiscoR >= 255)
			{
				DiscoR = 255;
				DiscoStyle++;
			}
		}
		if (DiscoStyle == 5)
		{
			DiscoB -= num;
			if (DiscoB <= 0)
			{
				DiscoB = 0;
				DiscoStyle = 0;
			}
		}
	}

	private static void DoUpdate_AnimateBackgrounds()

```


---

## 🤖 Assistant · 2026-08-13T06:19:19.577Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Disco animation ✓ matches repo exactly (6 phases, step 7, cascade `if` vs `switch` — subtle: vanilla uses sequential ifs so two phases can advance in one frame at boundaries; repo uses switch so one phase per frame. Minor 1-frame difference at phase boundaries. Negligible but could note.)

Now check MOON_FLOOR vs Main.cs:63230-63266 and whether it's used. And check the tile 48/137 note — the user's prompt mentions "tile 48/137 熔岩块" — probably meaning LiquidID? Let me quickly check Main.cs 63230 region for moon floor. Also confirm whether repo TileLightScanner handles liquid tile 48? Hmm. Actually in old Terraria (1.3), tile 48 = lava?? No... In 1.3, "Liquid" was tile type 48 (Lava) and 137? Hmm! Yes! In old Terraria 1.3, tile 48 = Lava (as tile), and... Actually TileID 48 in 1.4 = Spike. Hmm, but the audit prompt says "tile 48/137 熔岩块" — hmm, maybe in this repo's world import, liquid lava is stored... no, repo uses liquidType. Hmm, 137 = Traps (dart trap).

Wait, maybe the user is mistaken, or maybe they refer to `Main.tileLighted` not including those. Let me just double check TileID 48 and 137 names.

TileID 48: let me grep. And 137.

Actually, I realize the prompt might be referencing the OLD (1.3) TileLightScanner where `case 48:` was lava tiles. But in 1.4.5 vanilla, ApplyLiquidLight handles liquids, and there's no case 48/137 in ApplyTileLight. Let me confirm by checking whether 48 or 137 appear in the tileLighted list: the list I dumped doesn't include 48 or 137. So in 1.4.5 there's no tile-lava light. Good — I can report that as a clarification: vanilla 1.4.5 has no ApplyTileLight case for 48/137; lava light is purely ApplyLiquidLight :110-132. The user's premise about "tile 48/137 熔岩块 :110" refers to ApplyLiquidLight's position.

Now MOON_FLOOR — check Main.cs:63230-63266.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:19:19.594Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '63220,63275p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs; echo ---48/137---; grep -nE \"public const ushort [A-Za-z0-9_]+ = (48|137);$\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs",
 "description": "Read moon floor table and check tiles 48/137"
}
```


---

## 🤖 Assistant · 2026-08-13T06:19:19.751Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"MOON_FLOOR\" ~/Project/GLM/SandboxWorld/game/src --include=*.ts | head; echo ---; grep -rn \"shimmer\\|liquidType\" ~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts | head -20",
 "description": "Check MOON_FLOOR usage and liquidType semantics"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:19:24.501Z

**📎 ToolResult**

```
			}
			if (b4 < 15)
			{
				b4 = 15;
			}
			moonColor.R = (byte)r4;
			moonColor.G = (byte)g3;
			moonColor.B = (byte)b4;
		}
		byte minimalLight = 15;
		switch (GetMoonPhase())
		{
		case MoonPhase.Empty:
			minimalLight = 11;
			break;
		case MoonPhase.QuarterAtLeft:
		case MoonPhase.QuarterAtRight:
			minimalLight = 13;
			break;
		case MoonPhase.HalfAtLeft:
		case MoonPhase.HalfAtRight:
			minimalLight = 15;
			break;
		case MoonPhase.ThreeQuartersAtLeft:
		case MoonPhase.ThreeQuartersAtRight:
			minimalLight = 17;
			break;
		case MoonPhase.Full:
			minimalLight = 19;
			break;
		}
		if (dontStarveWorld)
		{
			DontStarveSeed.ModifyMinimumLightColorAtNight(ref minimalLight);
		}
		if (bgColorToSet.R < minimalLight)
		{
			bgColorToSet.R = minimalLight;
		}
		if (bgColorToSet.G < minimalLight)
		{
			bgColorToSet.G = minimalLight;
		}
		if (bgColorToSet.B < minimalLight)
		{
			bgColorToSet.B = minimalLight;
		}
		if (info.BloodMoonActive)
		{
			if (bgColorToSet.R < 25)
			{
				bgColorToSet.R = 25;
			}
			if (bgColorToSet.G < 25)
			{
				bgColorToSet.G = 25;
---48/137---
529:	public const ushort Spikes = 48;
707:	public const ushort Traps = 137;

```


---

## 👤 User(sidechain) · 2026-08-13T06:19:24.538Z

**📎 ToolResult**

```
(eval):1: no matches found: --include=*.ts
---
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts:7: *  血案 2026-08-12:水中箱 pass 照抄 `liquidType()!=0` 判水(原版 Water=0),
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts:9: *  (grep `liquidType.*=== *0\b|liquidType.*!== *0\b` 可快速排查同类移植错位) */
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts:27:  readonly liquidType: Uint8Array; // 取值见 LIQUID_TYPE(原版 +1 编码——照抄 C# liquidType()==0 判水必错,见 LIQUID_TYPE 注释)
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts:66:      this.liquidType = new Uint8Array(bufs.liquidType);
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts:84:    this.liquidType = new Uint8Array(n);
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts:264:    if (this.liquid[i] === a && this.liquidType[i] === type) return;
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts:266:    this.liquidType[i] = type;

```


---

## 🤖 Assistant · 2026-08-13T06:19:29.773Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
MOON_FLOOR matches vanilla moon phase minimal light (11,13,15,17,19,17,15,13 for Empty→QuarterL→? hmm: order Empty=11, QuarterAtLeft/Right=13, Half=15, ThreeQuarters=17, Full=19). Vanilla GetMoonPhase order for phases 0..7: Empty, QuarterAtRight, HalfAtRight, ThreeQuartersAtRight, Full, ThreeQuartersAtLeft, HalfAtLeft, QuarterAtLeft (need to verify). Repo comment says "相位序 Empty→Full→Empty" with [11,13,15,17,19,17,15,13]. Given min values 11,13,15,17,19,17,15,13 — consistent either direction. Fine, that's sky-color territory (another agent's lane maybe). But the user's scope for this lane includes MOON_FLOOR in lightTables. It matches the value table.

Now liquidType values: LIQUID_TYPE. Let me check TileStore for LIQUID_TYPE mapping (2=lava? 3=honey? 4=shimmer?).
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:19:30.483Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"LIQUID_TYPE\" -A 10 ~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts | head -25; echo ---; grep -rn \"liquidType\\[i\\] === 2\\|liquidType.*=== 4\\|shimmer\" ~/Project/GLM/SandboxWorld/game/src/lighting/*.ts",
 "description": "Check liquid type encoding and shimmer handling"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:19:30.513Z

**📎 ToolResult**

```
10:export const enum LIQUID_TYPE {
11-  NONE = 0,
12-  WATER = 1,
13-  LAVA = 2,
14-  HONEY = 3,
15-  SHIMMER = 4,
16-}
17-
18-export class TileStore {
19-  readonly w: number;
20-  readonly h: number;
--
27:  readonly liquidType: Uint8Array; // 取值见 LIQUID_TYPE(原版 +1 编码——照抄 C# liquidType()==0 判水必错,见 LIQUID_TYPE 注释)
28-  readonly half: Uint8Array;      // halfBrick 位（原版 Tile.cs bTileHeader bit1）：下半 8px 实心
29-  readonly slope: Uint8Array;     // 坡面 0-4（原版编码；渲染暂未支持，生成期少用）
30-  readonly wire: Uint8Array;      // 电路位（原版 Tile.cs sTileHeader）：bit0红 bit1蓝 bit2绿 bit3黄 bit4致动器 bit5已致动(inActive)
31-  /** 方块油漆 id（0-31，原版 Tile.cs:609-617 `color()` = sTileHeader & 0x1F）。
32-   *  PaintID 全表见 world/Paint.ts；深层漆 13-24 与浅层 1-12 同 RGB，
33-   *  区别只在渲染覆盖强度（TilePaintSystemV2）。 */
34-  readonly paint: Uint8Array;
35-  /** 背景墙油漆 id（0-31，原版 Tile.cs:365-373 `wallColor()` = bTileHeader & 0x1F） */
36-  readonly paintWall: Uint8Array;
37-  // wire 位掩码常量（对应原版 Tile.cs:396-459 的 wire/wire2/wire3/wire4/actuator/inActive）
---
~/Project/GLM/SandboxWorld/game/src/lighting/SkyColor.ts:142:  shimmerTorchColor(): [number, number, number] {
~/Project/GLM/SandboxWorld/game/src/lighting/TileLightScanner.ts:230:                else if (style === 23) [er, eg, eb] = this.flicker.shimmerTorchColor();
~/Project/GLM/SandboxWorld/game/src/lighting/TileLightScanner.ts:262:        if (st.liquid[i] > 0 && st.liquidType[i] === 2) {

```


---

## 🤖 Assistant · 2026-08-13T06:19:34.399Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: shimmer liquid (liquidType===4) has no light in the repo → missing (vanilla ApplyLiquidLight :133-151).

Also water: vanilla ApplyLiquidLight only handles lava and shimmer. Water/honey emit nothing ✓ repo.

Also the repo getMask: `if (st.liquidType[i] !== 2 && st.liquid[i] > 128)` — vanilla GetTileMask: `if (!tile.lava() && tile.liquid > 128)` then honey→Honey else Water. Shimmer in vanilla: tile.shimmer() is liquid type 4 → returns Water mask (since !lava && !honey). Repo: liquidType 4 !== 2 → not honey → Water ✓.

Now, additional vanilla emissive cases I should double check I haven't missed: the full switch case list. Let me enumerate all case labels in ApplyTileLight programmatically to be sure of the complete list and line numbers.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:19:35.476Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "awk 'NR>=352 && NR<=3129' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs | grep -nE \"^\\s*case [0-9]+:\" | sed -E 's/^([0-9]+):\\s*case ([0-9]+):/\\1 \\2/' | awk '{printf \"%s(L%s) \", $2, $1+351} END {print \"\"}'",
 "description": "Enumerate all switch case labels with line numbers"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:19:39.339Z

**📎 ToolResult**

```
case(L354) case(L365) case(L370) case(L378) case(L386) case(L394) case(L399) case(L410) case(L415) case(L416) case(L417) case(L422) case(L427) case(L432) case(L448) case(L453) case(L458) case(L463) case(L468) case(L473) case(L478) case(L483) case(L488) case(L493) case(L496) case(L501) case(L506) case(L511) case(L516) case(L521) case(L526) case(L531) case(L541) case(L549) case(L554) case(L559) case(L564) case(L569) case(L574) case(L575) case(L576) case(L581) case(L582) case(L583) case(L588) case(L589) case(L590) case(L595) case(L596) case(L597) case(L602) case(L603) case(L604) case(L609) case(L610) case(L611) case(L616) case(L654) case(L659) case(L660) case(L661) case(L669) case(L674) case(L681) case(L686) case(L691) case(L696) case(L701) case(L706) case(L711) case(L721) case(L722) case(L723) case(L778) case(L786) case(L791) case(L796) case(L801) case(L806) case(L811) case(L816) case(L821) case(L826) case(L831) case(L836) case(L841) case(L846) case(L851) case(L862) case(L870) case(L881) case(L907) case(L908) case(L913) case(L922) case(L923) case(L928) case(L933) case(L938) case(L943) case(L946) case(L949) case(L954) case(L959) case(L964) case(L969) case(L974) case(L981) case(L985) case(L989) case(L992) case(L995) case(L998) case(L1003) case(L1007) case(L1011) case(L1021) case(L1031) case(L1038) case(L1043) case(L1048) case(L1053) case(L1058) case(L1074) case(L1081) case(L1086) case(L1091) case(L1096) case(L1101) case(L1106) case(L1111) case(L1116) case(L1121) case(L1126) case(L1131) case(L1136) case(L1141) case(L1146) case(L1151) case(L1165) case(L1173) case(L1186) case(L1194) case(L1202) case(L1210) case(L1211) case(L1216) case(L1223) case(L1228) case(L1233) case(L1238) case(L1239) case(L1244) case(L1249) case(L1254) case(L1259) case(L1264) case(L1269) case(L1274) case(L1279) case(L1284) case(L1296) case(L1301) case(L1306) case(L1311) case(L1316) case(L1321) case(L1326) case(L1331) case(L1336) case(L1344) case(L1349) case(L1354) case(L1359) case(L1364) case(L1369) case(L1374) case(L1379) case(L1384) case(L1389) case(L1394) case(L1399) case(L1407) case(L1412) case(L1417) case(L1422) case(L1427) case(L1432) case(L1437) case(L1442) case(L1447) case(L1452) case(L1457) case(L1462) case(L1468) case(L1473) case(L1478) case(L1483) case(L1488) case(L1493) case(L1498) case(L1503) case(L1508) case(L1520) case(L1528) case(L1536) case(L1542) case(L1550) case(L1558) case(L1565) case(L1570) case(L1575) case(L1580) case(L1585) case(L1590) case(L1591) case(L1596) case(L1601) case(L1606) case(L1611) case(L1616) case(L1621) case(L1633) case(L1638) case(L1643) case(L1648) case(L1653) case(L1658) case(L1663) case(L1668) case(L1676) case(L1681) case(L1686) case(L1691) case(L1696) case(L1701) case(L1706) case(L1711) case(L1716) case(L1721) case(L1726) case(L1731) case(L1739) case(L1744) case(L1749) case(L1754) case(L1759) case(L1764) case(L1769) case(L1774) case(L1779) case(L1784) case(L1789) case(L1794) case(L1800) case(L1805) case(L1810) case(L1815) case(L1820) case(L1825) case(L1830) case(L1835) case(L1840) case(L1852) case(L1860) case(L1861) case(L1868) case(L1873) case(L1878) case(L1883) case(L1888) case(L1889) case(L1894) case(L1899) case(L1904) case(L1909) case(L1914) case(L1919) case(L1924) case(L1929) case(L1941) case(L1946) case(L1951) case(L1956) case(L1961) case(L1966) case(L1971) case(L1976) case(L1981) case(L1989) case(L1994) case(L1999) case(L2004) case(L2009) case(L2014) case(L2019) case(L2024) case(L2029) case(L2034) case(L2039) case(L2044) case(L2052) case(L2057) case(L2062) case(L2067) case(L2072) case(L2077) case(L2082) case(L2087) case(L2092) case(L2097) case(L2102) case(L2107) case(L2113) case(L2118) case(L2123) case(L2128) case(L2133) case(L2138) case(L2143) case(L2148) case(L2153) case(L2165) case(L2174) case(L2179) case(L2184) case(L2189) case(L2194) case(L2199) case(L2200) case(L2205) case(L2210) case(L2215) case(L2220) case(L2225) case(L2230) case(L2242) case(L2247) case(L2252) case(L2257) case(L2262) case(L2267) case(L2272) case(L2277) case(L2282) case(L2287) case(L2295) case(L2300) case(L2305) case(L2310) case(L2315) case(L2320) case(L2325) case(L2330) case(L2335) case(L2340) case(L2345) case(L2350) case(L2358) case(L2363) case(L2368) case(L2373) case(L2378) case(L2383) case(L2388) case(L2393) case(L2398) case(L2403) case(L2408) case(L2413) case(L2419) case(L2424) case(L2429) case(L2434) case(L2439) case(L2444) case(L2449) case(L2454) case(L2459) case(L2472) case(L2480) case(L2488) case(L2489) case(L2490) case(L2495) case(L2500) case(L2508) case(L2509) case(L2517) case(L2525) case(L2530) case(L2533) case(L2536) case(L2539) case(L2543) case(L2547) case(L2551) case(L2555) case(L2559) case(L2563) case(L2576) case(L2577) case(L2583) case(L2590) case(L2595) case(L2600) case(L2605) case(L2610) case(L2615) case(L2620) case(L2625) case(L2633) case(L2638) case(L2646) case(L2651) case(L2656) case(L2657) case(L2662) case(L2667) case(L2672) case(L2677) case(L2682) case(L2687) case(L2692) case(L2704) case(L2709) case(L2714) case(L2719) case(L2724) case(L2729) case(L2737) case(L2742) case(L2747) case(L2752) case(L2757) case(L2762) case(L2767) case(L2772) case(L2777) case(L2782) case(L2787) case(L2792) case(L2800) case(L2805) case(L2810) case(L2815) case(L2820) case(L2825) case(L2830) case(L2835) case(L2840) case(L2845) case(L2850) case(L2855) case(L2861) case(L2866) case(L2871) case(L2876) case(L2881) case(L2886) case(L2891) case(L2896) case(L2901) case(L2913) case(L2921) case(L2938) case(L2939) case(L2940) case(L2941) case(L2942) case(L2943) case(L2944) case(L2945) case(L2962) case(L2968) case(L2974) case(L2975) case(L2985) case(L2986) case(L2987) case(L2988) case(L3004) case(L3009) case(L3015) case(L3029) case(L3035) case(L3043) case(L3057) case(L3065) case(L3073) case(L3076) case(L3081) case(L3086) case(L3093) case(L3098) case(L3103) case(L3108) case(L3119) case(L3124)

```


---

## 🤖 Assistant · 2026-08-13T06:20:01.615Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
My awk output has a bug (printed "case(L354)" without the id) because the regex captured... whatever, I already read the whole file so I have the complete case list manually. I transcribed it above. Let me compile the definitive list of unique tile types from my reading:

658, 356, 663, 656, 20, 634, 633, 637, 638, 463, 491, 209, 415, 500, 416, 501, 417, 502, 418, 503, 390, 597, 564, 568, 569, 570, 580, 391, 381, 517, 687, 534, 535, 689, 536, 537, 690, 539, 540, 688, 625, 626, 691, 627, 628, 692, 184, 370, 659, 667, 708, 711, 27, 336, 340, 341, 342, 343, 344, 327, 316, 317, 318, 719, 718, 717, 429, 286, 619, 620, 582, 598, 270, 271, 581, 660, 572, 262, 263, 264, 265, 266, 267, 268, 237, 238, 235, 405, 215, 92, 592, 593, 594, 548, 613, 614, 93, 96, 98, 4, 372, 646, 33, 174, 100, 173, 34, 35, 95, 17, 133, 302, 77?? no. 42, 49, 519, 70,71,72,190,348,349,528,578, 739, 350, 61,703, 26,31,695,696, 699, 84, 83, 126, 125, 129, 149, 160, 354, 37, 22, 140, 171, 204, 347.

Wait also case 4 at :1536, 372 :1542, 646 :1550, 33 :1558, 174 :1852, 100/173 :1860, 34 :2165, 35 :2472, 95 :2480, 17/133/302 :2488-2490, 77 :2495?? Hmm :2495 → "case 77"? Let me check line 2495. From my reading: :2495 `case 77:` R=0.75,G=0.45,B=0.25. Yes! I missed case 77 (Hellforge). Let me re-read that bit:

```
2488	case 17:
2489	case 133:
2490	case 302:
2491		R = 0.83f; G = 0.6f; B = 0.5f;
2494	case 77:
2495		R = 0.75f;
2496		G = 0.45f;
2497		B = 0.25f;
```
So Hellforge 77 → (0.75, 0.45, 0.25). Repo v_77_hellforge light [255,140,70] = (1, 0.549, 0.275) → deviation.

And case 37 meteorite :2500. 22/140 :2508. 171 :2517. 204/347 :2576. 42 :2583.

So total unique emissive tiles = let me count: I'll list grouped:

Now, importantly: is there a case for tile 58 (Heart, life crystal)? tileLighted includes 58! But no case 58 in the switch → vanilla gives R=G=B=0 for tile 58? Hmm, tileLighted[58]=true but no case → ApplyTileLight sets nothing. But wait — LifeCrystal light: In 1.4, the heart crystal glow comes from... Actually case 4? no. Hmm, tile 58 = Heart (Life Crystal). tileLighted[58] = true means it enters the switch but matches no case → no light. Interesting. But repo gives crystal_heart light [255,60,90]. Vanilla: no light from tile 58 (the pink glow is draw-only? Actually there is `Main.tileLighted[58]`? Hmm wait, maybe I mis-extracted; let me check whether case 58 exists in the file... searching my list: no 58. Hmm but hold on, tileLighted[58]... Let me double-check by grepping "case 58:" in the file. Also 19, 76, 109, 684, 701 are in tileLighted but maybe have no case (701 = GlowTulipReplica? case? no). Let me grep for a few.

Also 109 (HallowedGrass) tileLighted — no case in switch → no light. OK.

Let me verify which tileLighted ids have no switch case: tileLighted list vs case list.

tileLighted: 4 17 19 20 22 26 27 31 33 34 35 37 42 49 58 61 70 71 72 76 77 83 84 92 93 95 96 98 100 109 125 126 129 133 140 149 160 171 173 174 184 190 204 209 215 237 238 270 271 286 302 316 317 318 327 336 340 341 342 343 344 346 347 348 349 350 354 356 370 372 390 391 405 415 416 417 418 429 463 491 500 501 502 503 517 519 528 534 535 536 537 539 540 548 564 568 569 570 572 578 580 581 582 592 593 594 597 598 613 614 619 620 625 626 627 628 633 634 637 638 646 656 658 659 660 663 667 684 687 688 689 690 691 692 695 696 699 701 703 708 711 717 718 719 739

Cases (from my reading): 658 356 663 656 20 634 633 637 638 463 491 209 415 500 416 501 417 502 418 503 390 597 564 568 569 570 580 391 381 517 687 534 535 689 536 537 690 539 540 688 625 626 691 627 628 692 184 370 659 667 708 711 27 336 340 341 342 343 344 327 316 317 318 719 718 717 429 286 619 620 582 598 270 271 581 660 572 262 263 264 265 266 267 268 237 238 235 405 215 92 592 593 594 548 613 614 93 96 98 4 372 646 33 174 100 173 34 35 95 17 133 302 77 42 49 519 70 71 72 190 348 349 528 578 739 350 61 703 26 31 695 696 699 84 83 126 125 129 149 160 354 37 22 140 171 204 347

tileLighted-only ids (no case): 19, 58, 76, 109, 346, 684, 701.
- 19 = Platforms; 58 = Heart; 76 = HellstoneBrick? hmm 76 = Hellstone? TileID 76 = Hellstone (the ore!). Wait: Hellstone = 58! Let me check: TileID: 58 = Hellstone, 76 = HellstoneBrick, 107 = Cobalt... Hmm repo: ore_hellstone sheet 58; v_76_hellstone_brick sheet 76. So 58 = Hellstone ore!

So case for Hellstone? There's no case 58 in ApplyTileLight. But tileLighted[58] = true. Hmm — then how does hellstone glow in vanilla? Let me grep "case 58" in the scanner... Let me check the actual switch again — maybe I missed it. In the file I read, I don't recall case 58. Let me search.

Also 346 = ChlorophyteBrick; 684 = AncientHellstoneBrick? (684 = AncientHellstoneBrick? hmm). 701 = GlowTulipReplica.

Let me grep these specific ids in the scanner file to be safe.
````

</details>


---

## 🤖 Assistant · 2026-08-13T06:20:02.889Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "for id in 19 58 76 109 346 684 701 77 48 137; do echo \"== $id ==\"; grep -n \"case $id:\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs; done; echo ---; grep -nE \"public const ushort [A-Za-z0-9_]+ = (19|58|76|109|346|684|701|349|739);$\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs",
 "description": "Verify tileLighted ids lacking switch cases"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:20:08.447Z

**📎 ToolResult**

```
== 19 ==
1284:				case 19:
1621:				case 19:
1929:				case 19:
2220:				case 19:
== 58 ==
1478:				case 58:
1815:				case 58:
2123:				case 58:
2398:				case 58:
2840:				case 58:
== 76 ==
== 109 ==
== 346 ==
314:		case 346:
== 684 ==
== 701 ==
== 77 ==
2495:			case 77:
== 48 ==
1427:				case 48:
1764:				case 48:
2072:				case 48:
2345:				case 48:
2787:				case 48:
== 137 ==
229:		case 137:
---
471:	public const ushort Platforms = 19;
549:	public const ushort Hellstone = 58;
585:	public const ushort HellstoneBrick = 76;
651:	public const ushort HallowedGrass = 109;
1125:	public const ushort ChlorophyteBrick = 346;
1131:	public const ushort MushroomStatue = 349;
1801:	public const ushort AncientHellstoneBrick = 684;
1835:	public const ushort GlowTulipReplica = 701;
1911:	public const ushort JellyfishBlock = 739;

```


---

## 🤖 Assistant · 2026-08-13T06:20:46.120Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: ids 19, 58, 76, 109, 346, 684, 701 are tileLighted but have NO case in ApplyTileLight → they emit no light in vanilla 1.4.5.

So repo's extra lights that vanilla doesn't have:
- crystal_heart (sheet 12 Heart)? Wait repo crystal_heart uses sheet 12 (Heart = 12 ✓). tileLighted doesn't include 12! Let me check: tileLighted list doesn't include 12. So vanilla Heart (life crystal, tile 12) emits no light at all. Repo gives [255,60,90] → extra (non-vanilla). Hmm wait, but in vanilla, life crystals do have a pink glow... via `Main.tileLighted`? No — via draw glow (Main.DrawTiles_GlowPaintMask?) Actually life crystal glow is drawn as a "glow mask" sprite (animation), not lighting. So repo's light on sheet 12 is non-vanilla. Let me double check that 12 not in tileLighted: list: "4 17 19 20 22 26 27 31 33 34 35 37 42 49 58..." — no 12. Correct.

- ore_hellstone (sheet 58): tileLighted[58]=true but no case → vanilla NO light. Repo [255,90,40] → extra.
- v_76_hellstone_brick: no light in repo ✓ correct (vanilla none).
- v_346_chlorophyte_brick: repo no light ✓ (vanilla none). 
- v_684: no light ✓.
- v_701: no light ✓.
- v_19 platform: no light ✓.
- v_109: no light ✓.

Also repo "mushroom" (T.MUSHROOM=19, sheet 3) no light ✓.

Extra lights in repo not in vanilla:
- crystal_heart sheet 12 [255,60,90] → vanilla tileLighted[12] false → extra.
- ore_hellstone sheet 58 [255,90,40] → vanilla no case → extra.
- furnace sheet 17 [255,140,70] → vanilla (0.83,0.6,0.5) → deviation (wrong values, too saturated).
- hellforge sheet 77 [255,140,70] → vanilla (0.75,0.45,0.25) → deviation.
- torch: flicker extra.

Also check: does repo give light to any tile where vanilla has none? Search tiles.ts light fields list:
1. torch (4): vanilla yes.
2. furnace (17): yes.
3. crystal_heart (12): EXTRA.
4. candle (33): yes.
5. chandelier (34): yes.
6. candelabra (100): yes.
7. chinese_lantern (95): yes.
8. skull_lantern (98): yes.
9. water_candle (49): yes.
10. v_463 (463): yes.
11. ore_demonite (22): yes (values wrong).
12. ore_meteorite (37): yes.
13. ore_hellstone (58): EXTRA (tileLighted yes but no case).
14. ore_crimtane (204): yes.
15. v_633 (633), v_536 (536), v_381 (381): yes (381 wrong).
16. v_190 (190): yes (mushroom group ✓).
17. v_350 (350): yes.
18. v_184 (184): partial.
19. v_637 (637): yes.
20. v_519 (519): yes.
21. v_634 (634): yes.
22. v_26 (26): yes.
23. v_93 (93): yes.
24. v_215 (215): yes.
25. v_597 (597): partial.
26. v_592 (592): yes.
27. v_354 (354): yes.
28. v_491 (491): yes.
29. v_405 (405): yes.
30. v_356 (356): yes.
31. v_237 (237): yes.
32. v_316 (316): partial.
33. v_125 (125): approx.
34. v_129 (129): partial.
35. v_149 (149): partial.
36. v_173/v_174 (173/174): yes.
37. v_372 (372): yes.
38. v_564 (564): yes.
39. v_593/v_594: yes.
40. v_528 (528), v_578 (578), v_70 (70), v_71 (71), v_72 (72), v_348 (348), v_349 (349): mushroom group ✓.
41. v_613/v_614, v_548: yes.
42. v_598 (598): wrong value.
43. v_302 (302): ✓.
44. v_77 (77): wrong value.
45. v_625 (625), v_539 (539): yes.
46. v_340 (340): ✓.
47. v_31 (31): yes.
48. v_27 (27): wrong.
49. v_61 (61): yes (gate missing).
50. v_83 (83): partial.
51. v_711 (711): ✓.
52. v_35 (35): wrong.
53. v_92 (92): ✓ (frameY gate missing).

Now also check the scanner's handling: `if (d && (d.light || MUSHROOM_GLOW_SHEETS.has(sheet)) && shroomGateOk)` — tiles with light but not in MUSHROOM group use d.light. And `specialTileLight` adds on top. Also note for tiles in FLICKER_SHEETS that don't have d.light (e.g. 126 disco has no def.light), no static light is applied — only specialTileLight. OK.

But important: FLICKER_SHEETS contains 4 (torch). For torch the flicker is added unconditionally in the sheet===4 branch. Vanilla case 4: NO flicker → deviation.

FLICKER_SHEETS contains 33 (candle), 174, 49, 92, 93, 95, 100, 126, 173, 149, 564, 215, 405, 34. Which vanilla cases actually have the additive flicker term `Next(28,42)*0.005+(270-mouse)/700`? Only 405 (:1034), 215 (:1077), 592 (:1176). Note 592 is NOT in repo's FLICKER_SHEETS — but repo v_592 has def.light and... 592 not in FLICKER_SHEETS so no flicker; but vanilla 592 HAS flicker. Meanwhile repo adds flicker to 33,49,92,93,95,100,126,173,149,564,34,174,4 which vanilla does NOT have. That's a big systematic deviation: repo applied the fireplace/campfire flicker to all "burning" lamps; vanilla only campfire/fireplace/brazier flicker.

Wait — careful: does vanilla candle flicker? In vanilla there's no flicker in TileLightScanner for candles. Hmm, but there IS `Main.tileLighted`... no. Actually hold on: in old 1.3 TileLightScanner, candles didn't flicker either. But wait, `localRandom` is used in cases 37 (meteorite), 215, 405, 592, 125, 149, 519, 70-group, 26/31, 137(wall), 327, 717, 718, 350(no), 84(no), 659 etc. So yes: only campfire/fireplace/brazier(592) have the additive flicker; plus meteorite has its own Next(95,106) multiplier; crystal ball has Next(28,42)*0.01; holiday lights rand multiplier; cattail; mushroom group.

So repo's FLICKER_SHEETS design is a systematic non-1:1 choice. Must report as deviation with the specific list.

Now, let me double check the specialTileLight case 42 default and check `lightIsOn` gate for lantern (42 in LIGHT_TOGGLE ✓).

Also check scanner handles `invisibleBlock` gate for 658 (aether monolith) — repo v_658 no light → missing entirely.

One more check: the scanner's MUSHROOM gate for 349: vanilla gate is `tile.type != 349 || tile.frameX >= 36` — repo: shroomGateOk = !(sheet===349 && frameX<36) ✓. But note vanilla applies the gate to the whole case group (70,71,72,190,348,349,528,578): if type==349 && frameX<36 → skip entirely ✓ repo same.

Also 519 cattail is a separate case (frameY==90). But note: repo v_519 has def.light AND 519 is not in MUSHROOM set, so it uses static [26,51,179] always (even frameY!=90). Vanilla only frameY==90. Also vanilla 519 not in the mushroom group. OK.

Also check: repo includes 519 in... no.

Now check the wall emissive gating nuance and the missing WALL_LIGHT walls 73/227 (cloud/snowfall). Vanilla ApplySurfaceLight condition: `(Main.wallLight[tile.wall] || tile.wall == 73 || tile.wall == 227 || (tile.invisibleWall() && !_drawInvisibleWalls))`. Repo `exposed()` returns `wall === 0 || WALL_LIGHT.has(wall)` → missing 73 (cloud), 227 (snowfall), and invisible-wall handling (echo walls? invisibleWall is for wall 318 echo? Actually tile.invisibleWall() is the "wall is invisible" flag (echo wall coating). Minor).

Now, one more: does repo handle `Main.tileLighted` gating? No — repo relies on def.light presence. Fine.

Also check `ApplySurfaceLight` shimmerDarken — out of scope (engine side).

Let me also verify the repo's hell light uses `Math.max(lr, hellR)` etc. and gates on exposed + shallowLiquid ✓. Vanilla gate also requires `lightColor.X < num4` — equivalent to max. ✓. And vanilla additionally requires `(!tile.active() || !tileNoSunLight || (slope/half && 4 neighbors liquid==0))` — repo's exposed() approximates: for active blocking tiles with slope==0 && half==0 → false; slope/half → check neighbors ✓. But vanilla's condition `tile.slope() != 0 || tile.halfBrick()` — note vanilla requires slope!=0 OR halfBrick for the exception; repo checks `st.slope[i] === 0 && st.half[i] === 0` → return false, else check neighbors ✓ equivalent.

Hmm, one nuance: vanilla's third clause `(tile.slope() != 0 || tile.halfBrick() || (tile.invisibleBlock() && !_drawInvisibleWalls))` includes invisibleBlock (echo coating) — repo doesn't handle invisibleBlock (echo-coated blocks still block sky). Minor, note.

Also vanilla ApplyHellLight has same structure ✓.

Also the repo misses `ApplySurfaceLight`'s `tile.liquid < 200` + halfBrick neighbor nuance ✓ implemented via shallowLiquid; and the shimmer-liquid surface tint branch (liquid>=200 with liquidAlpha[13]) — that's for shimmer at surface: `else if (Main.liquidAlpha[13] > 0f)` — only for shimmer liquid (liquid type 13? no, liquidAlpha[13] is waterStyle 13 = underworld?). Hmm: `tile.liquid < 200` → full sky; else if liquidAlpha[13]>0 → num3 = num6*0.175*(1+rand*0.13)*liquidAlpha[13] (B only). liquidAlpha index 13 = shimmer? LiquidID.Shimmer = 3; Main.liquidAlpha is indexed by... waterStyle? Probably shimmer-related. Repo doesn't implement → note as missing (shimmer surface dimming).

Let me check what liquidAlpha[13] is — Main.cs sets liquidAlpha[13] when? Let me grep quickly. This matters for section 4 completeness.

Also for the hell light: `Math.sin(performance.now()*0.002)` vs `Main.GlobalTimeWrappedHourly` — check vanilla GlobalTimeWrappedHourly rate. In Main: `GlobalTimeWrappedHourly += (float)gameTimeUpdate / 3600000f * (double)dayrate`? something. GlobalTimeWrappedHourly is in "hours" (0..24 wrapped). So sin(GlobalTimeWrappedHourly*2) has period π hours of game time ≈ π * (1/24 day) — a day in Terraria is 24 min real → period ≈ 3.14 h game = ~3.14 min real... wait: 24 game-hours = 24 real minutes (1 game hour = 1 min). So period = π game-hours ≈ 3.14 real minutes ≈ 188 s. Repo: 2π/0.004 rad/ms = 1571 ms period ≈ 1.57 s. So repo's hell pulse is ~120× faster than vanilla. Deviation (approximation, amplitude ✓ 0.08).

Let me check GlobalTimeWrappedHourly to be precise.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:20:46.711Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"GlobalTimeWrappedHourly\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head -8; echo ---; grep -n \"liquidAlpha\\[13\\]\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head -5",
 "description": "Check GlobalTimeWrappedHourly rate and liquidAlpha 13"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:20:46.766Z

**📎 ToolResult**

```
387:	public static float GlobalTimeWrappedHourly;
16777:			GlobalTimeWrappedHourly = (float)(gameTime.TotalGameTime.TotalSeconds % 3600.0);
16779:			Chroma.Update(GlobalTimeWrappedHourly);
16786:			GlobalTimeWrappedHourly = (float)(gameTime.TotalGameTime.TotalSeconds % 3600.0);
16892:			Chroma.Update(GlobalTimeWrappedHourly);
23463:					num83 = 0.625f + (float)Math.Sin(GlobalTimeWrappedHourly * (MathF.PI * 2f) * 0.75f + MathF.PI) * 0.125f;
23483:						num83 = 0.5f + (float)Math.Sin(GlobalTimeWrappedHourly * (MathF.PI * 2f) * 0.75f) * 0.5f;
23529:					num57 = 0.625f + (float)Math.Sin(GlobalTimeWrappedHourly * (MathF.PI * 2f) * 0.75f + MathF.PI) * 0.125f;
---

```


---

## ⚙️ System · 2026-08-13T06:22:26.441Z

Conversation compacted


---

## 👤 User(sidechain) · 2026-08-13T06:22:26.441Z

```
This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation.

Summary:
1. Primary Request and Intent:
   审计泰拉瑞亚 1:1 移植项目的【发光物光源全量对账】，我是三路代理中的【第一路：tile/墙/液体光源】。光照引擎本体（LightingEngine/LightMap）此前已移植，本次只审【光源端】。要求 very thorough，输出五节结构化报告，每条格式 [原版行号+值, 本仓文件:行号+值, 判定 一致/偏差(N)/缺失]，数值精确到 3 位小数，不要贴大段代码。五节为：
   1. **静态 tile 光源覆盖率**：TileLightScanner.cs ApplyTileLight（:344-3150 巨型 switch）全部发光 tile case 清单（tile id、发光条件如 frameX 门禁、颜色三元组），对照本仓 tiles.ts light 字段 + lightTables + TileLightScanner 特例，逐条判定；特别核对发光条件（灯笼 frameX!=0 不发光、灯泡 frameX 位段、迪斯科球动态色）。
   2. **发光墙 WALL_EMISSIVE 全表对账**：原版 ApplyWallLight（:167-342）每个发光墙 RGB 与本仓对照（用户说本仓 19 条，实际 21 条）。
   3. **火把色表 TORCH_COLORS 逐值对照** TorchID.cs:134-161（注意 _lights 数组 24 条 = 21 常量 + 3 动态 7/14/23；查 1.4.5 有无新增）。
   4. **液体光源**：岩浆 ApplyHellLight :3261 + ApplyLiquidLight :110（lavaV 0.55+(270-mouse)/900）、shimmer 微光；对照本仓 TileLightScanner.ts:164/185/263。
   5. **WALL_LIGHT 透光墙全表**对照 Main.cs:10487-10503（本仓 14+0 条 vs 原版 16 条含 0）。
   约束（系统提示）：READ-ONLY，禁止任何文件创建/修改/删除/移动，禁止写入重定向，只读搜索分析；最终报告直接以文字返回，不写报告文件；路径用绝对路径；不用 emoji；不要在工具调用前用冒号。

2. Key Technical Concepts:
   - Terraria 1.4.5 (Terarria1456 反编译源) TileLightScanner：GetTileLight 播种顺序 = ApplySurfaceLight(天) → ApplyHellLight(地狱) → ApplyWallLight → ApplyTileLight → ApplyLiquidLight，逐通道 max-raise（lightColor.X < R 则 R）
   - `Main.tileLighted[type]` 门禁：只有该表为 true 的 tile 才进入 ApplyTileLight switch
   - 动态量：`Main.mouseTextColor`（190↔255 步进1/帧，:18066-18074）、`Main.demonTorch`（0↔1 步进0.01/帧，:18090-18099）、`Main.DiscoR/G/B`（6 相步进7，:19440-19500）、`Main.GlobalTimeWrappedHourly`、`Main.demonTorchDir`
   - TorchID._lights 24 条 = 21 ConstantTorchLight + DemonTorchLight(7)/DiscoTorchLight(14)/ShimmerTorchLight(23)；1.4.5 无新增火把色（Count=24 与 1.4.4 相同）
   - ShimmerTorchLight 实际公式：num=clamp(0.9+(270-mouse)/900,0,1) → r=num*0.9, b=num*1.2；num2=clamp(0.9+(270-mouse)/125,0,1) 恒≥1.02→clamp=1 → g=0.55 常量
   - 传送门色 PortalHelper.GetPortalColor(player,portal)：portal0=hslToRgb(0.12,1,0.5)=橙(1,0.47,0)，portal1=hslToRgb(0.52,1,0.6)=青(0.2,0.904,1)；×0.65 后 (0.65,0.306,0)/(0.13,0.588,0.65)
   - 本仓 `vanilla.sheet` 字段 = 原版 TileID（渲染表 id），tile/wall 注册表 TILE_DEFS/WALL_DEFS；liquidType 编码 +1（1=水 2=岩浆 3=蜂蜜 4=微光）
   - lightIsOn(LIGHT_TOGGLE) 接线灯门控：`v % (2*t[1]) < t[1]`（帧翻转 ±offset 语义）

3. Files and Code Sections:
   - **~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs**（3339 行，全读）——原版标杆。关键段落：
     - ApplyLiquidLight :110-152：岩浆 num=0.55+(270-mouseTextColor)/900 → X=num,Y=num*0.6,Z=num*0.2；shimmer :133-151：num2=0.7+(270-mouse)/900、num3=0.7+(270-mouse)/125 → X=num2*0.6, Y=num3*0.25, Z=num2*0.9
     - ApplyWallLight :167-342：21 个墙 case（357:0.15/0.27/0.3+paint flag；182:0.24/0.12/0.09；33:0.09/0.0525/0.24；174:R=0.2975；175:wallColor==0?0.075/0.15/0.4:paint flag；176:0.1/0.1/0.1；137:num4=0.4+(270-mouse)/1500+Next(0,50)*0.0005 → R=num4,G=0.5num4,B=0.1num4；44:Disco×0.15；154:R=0.6,B=0.6；166:R=0.6,G=0.6；165:B=0.6；156:G=0.6；164:R=0.6；155:全 0.6；153:R=0.6,G=0.3；341:0.25/0.1/0；343:0/0.25/0；344:0/0.16/0.34；342:0.3/0/0.17；345:0.3/0/0.35；346:Disco×0.25）。注意 153-166 七个宝石墙 case **无** !LightIsBlocked 门（恒发光），其余有门；末尾 :323-329 墙油漆覆盖（paintColor/765）
     - ApplyTileLight :344-3150（详见第 4 节我整理的完整清单）
     - ApplySurfaceLight :3152-3259（彩色玻璃墙染色 :3190-3242：num=num4 满 sky 光后 switch(wall-88) 乘 0.9/0.15 等；wall 88-93 + 241；条件 tile 不挡阳/halfBrick 且 liquid<255）；`Main.wallLight[wall] || wall==73 || wall==227 || invisibleWall` 门（:3163/:3170）
     - ApplyHellLight :3261-3338：num4=0.55+sin(GlobalTimeWrappedHourly*2)*0.08 → (num4, num4*0.6, num4*0.2)，同 wallLight||73||227 门 + liquid<200
     - GetTileMask :68-87：!lava && liquid>128 → honey?Honey:Water；shimmer(液体4) 落到 Water mask
   - **~/Project/GLM/SandboxWorld/game/src/lighting/TileLightScanner.ts**（278 行，全读）——本仓播种扫描器。specialTileLight(:31-94) 只处理 5 个 sheet：42 灯笼（12 样式表+7/9 demonTorch 动态）、126 迪斯科球、429 导线灯泡、209 传送门炮（硬编码紫/橙）、84 开花药草。主干 exportTo(:156-277)：exposed() 透光判定（wall===0||WALL_LIGHT.has）、WALL_EMISSIVE + 彩玻墙染色 max 合成(:195-210)、tile 光（def.light / MUSHROOM_GLOW_SHEETS 公式 / FLICKER_SHEETS 闪烁叠加 / sheet 4 火把 TORCH_COLORS+额外 flicker :236）、液体光仅岩浆 :262-264、hellV=0.55+sin(performance.now()*0.002)*0.08 :161
   - **~/Project/GLM/SandboxWorld/game/src/lighting/lightTables.ts**（118 行，全读）——TORCH_COLORS(:60-85) 24 条、FLICKER_SHEETS(:87)={33,49,92,93,174,34,149,95,100,126,173,564,215,405,4}、MUSHROOM_GLOW_SHEETS(:90)={70,71,72,190,348,349,528,578}、WALL_EMISSIVE(:93-115) 21 条、WALL_LIGHT(:57)={21,318,106,317,107,138,140,141,139,145,150,152,245,315,168}、MOON_FLOOR=[11,13,15,17,19,17,15,13] 与 Main.cs:63237-63253 月相 minimalLight 一致
   - **~/Project/GLM/SandboxWorld/game/src/data/tiles.ts**（1297 行，全读）——所有带 light 的 def（见第 4 节判定清单）
   - **~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TorchID.cs**（:20-74 providers、:134-161 _lights）——24 条火把色
   - **~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs**——wallLight(:10487-10502 共 16 条含 0)、tileLighted 列表、Disco/demonTorch/mouseTextColor 动画、月相表
   - **~/Project/GLM/SandboxWorld/game/src/lighting/SkyColor.ts** FlickerClock(:93-151)——mouseTextColor/demonTorch/Disco 6 相动画与原版一致；demonTorchColor(:136-139) 与 DemonTorchLight 一致；shimmerTorchColor(:142-146) 错误（用 (mouse-190)/65 线性 0..1，返回 [num*0.9, num2*0.55, num*1.2]，num2=1-num）；discoColor ✓
   - **~/Project/GLM/SandboxWorld/game/src/world/wiring/devices.ts** LIGHT_TOGGLE(:522-529)：4:['x',66], 33/174/49/372:['x',18], 42/92/93:['x',18], 95/100/126/173/564:['x',36], 34/149:['x',54], 215:['y',36]；lightIsOn(:532-537) 用模周期
   - **~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/PortalHelper.cs** GetPortalColor(:382-396)

4. Errors and fixes:
   - TileID 常量 grep 初次失败（`public const short X = id;` 模式不匹配；实际是 `public const ushort X = id;`）→ 改用 `grep -nE "public const ushort [A-Za-z0-9_]+ = (id1|id2|...);$"` 成功解析全部目标 id 名称
   - awk 枚举 switch case 时输出只有行号没有 id（sed -E 分组问题）→ 不影响，因为已完整读过全文，手工转录 case 列表
   - 自我纠偏三处认知：tile 20 = Saplings（非心中臆测）；case 171 = ChristmasTree（frameY&0x3C00>>10 是圣诞树灯串接线色，LogicSensor=423）；用户提示的 "tile 48/137 熔岩块" 是误解——48=Spikes、137=Traps，1.4.5 无此二 case，岩浆发光只在 ApplyLiquidLight :110（用户给的行号 :110 正是该函数位置）

5. Problem Solving:
   已完成全部对账数据采集与逐条判定（尚未落成最终报告）。核心结论数据如下：

   **A. vanilla ApplyTileLight 完整发光清单（:344-3150）与判定**（原版值 → 本仓判定）：
   - 658 ShimmerMonolith :354（!invisibleBlock，TorchColor(23)×frameY/54 档 0.2/0.3/0.1）→ 本仓 v_658 无 light 缺失
   - 356 Sundial :378（sundialCooldown==0 → 0.45/0.25/0）→ v_356 [115,64,0]=0.451/0.251/0 数值一致，cooldown 门缺失
   - 663 Moondial :386（moondialCooldown==0 → 0/0.25/0.45）→ v_663 无 light 缺失
   - 656 GlowTulip :394（0.2/0.55/0.5）→ [255,185,110]=1.0/0.725/0.431 偏差
   - 20 Saplings :399（frameX/18∈30..32 → 0.325/0.15/0.05）→ acorn_sapling(sheet20) 无 light 缺失
   - 634 TreeAsh :410（0.65/0.3/0.1）→ [166,77,26] 一致
   - 633/637/638 AshGrass/Plants/Vines :415-421（0.325/0.15/0.05）→ 三条均 [83,38,13] 一致
   - 463 DefendersForge :422（0.2/0.4/0.8）→ [51,102,204] 一致；491 VoidVault :427（0.5/0.4/0.7）→ [128,102,179] 一致
   - 209 Cannon :432（portal0/portal1×0.65）→ specialTileLight case 209 有实现但色错：本仓 [0.42,0.2,0.65]/[0.65,0.26,0]，应为 portal0 橙 (0.65,0.306,0)、portal1 青 (0.13,0.588,0.65) 偏差(2)
   - 415/416/417/418 月亮碎片块 :448-482（0.7/0.5/0.1；0/0.6/0.7；0.6/0.2/0.6；0.6/0.6/0.9）→ 全部无 light 缺失
   - 500/501/502/503 月砖 :453-487（0.525/0.375/0.075；0/0.45/0.525；0.45/0.15/0.45；0.45/0.45/0.675）→ 全部缺失
   - 390 LavaLamp :488（0.4/0.2/0.1）→ v_390 缺失；597 Pylon :493（8 样式×0.75）→ v_597 [13,204,77]=样式0 未×0.75 偏差
   - 564 PlasmaLamp :541（frameX<36 → 0.05/0.3/0.55）→ [13,77,140] 数值一致，但 frameX<36 门未实现 + FLICKER_SHEETS 额外闪烁（原版无）偏差(2)
   - 568/569/570 仙女罐 :549-563（1/0.61/0.65；0.12/1/0.66；0.57/0.57/1）→ 全缺失
   - 580 HellButterflyJar :564（0.7/0.3/0.2）→ 缺失；391 CageEnchantedNightcrawler :569（0.3/0.1/0.25）→ 缺失
   - 381/517/687 LavaMoss 族 :574-579（0.25/0.1/0）→ v_381 [255,120,30]=1/0.47/0.118 偏差；517/687 缺失
   - 534/535/689 Krypton :581-586（0/0.25/0）→ 全缺失；536/537/690 Xenon :588-593（0/0.16/0.34）→ 536 [0,41,87] 一致、537/690 缺失；539/540/688 Argon :595-600（0.3/0/0.17）→ 539 [77,0,43] 一致、540/688 缺失；625/626/691 Violet :602-607（0.3/0/0.35）→ 625 [77,0,89] 一致、626/691 缺失；627/628/692 Rainbow :609-614（Disco×0.25）→ 全缺失
   - 184 LongMoss :616-653（6 个 frameX 档 110/132/154/176/198/220 → 0.25/0.1/0；0/0.25/0；0/0.16/0.34；0.3/0/0.17；0.3/0/0.35；Disco×0.25）→ v_184 [77,0,89] 仅 198 档值 偏差(5/6 缺)
   - 370 MeteoriteBrick :654（0.32/0.16/0.12）→ 缺失
   - 659/667/708 ShimmerBlock 族 :659-667（GetShimmerBaseColor）→ 全缺失
   - 711 RainbowBoulder :669（0.01/0.01/0.01）→ [3,3,3]=0.0118 ≈一致
   - 27 Sunflower :674（frameY<36 → 0.3/0.27/0）→ v_27 [255,242,166]=1/0.949/0.651 偏差
   - 336 LivingFire :681（0.85/0.5/0.3）→ 缺失
   - 340 LivingCursedFire :686（0.45/1/0.45）→ [115,255,115] 一致
   - 341 LivingDemonFire :691（demonTorch 混合）→ 缺失；342 FrostFire :696（0.5/0.5/1.1）→ 缺失；343 Ichor :701（0.85/0.85/0.3）→ 缺失；344 Ultrabright :706（0.6/1.026/0.96）→ 缺失
   - 327 Lavafall :711（num13=0.5+(270-mouse)/1500+Next(0,50)*0.0005 → R=num13,G=0.5num13,B=0.1num13）→ 缺失
   - 316/317/318 水母罐 :721-777（两态：316 亮0.2/0.3/0.8 暗0.1/0.2/0.5；317 0.2/0.7/0.3|0.05/0.45/0.1；318 0.7/0.2/0.5|0.4/0.1/0.25，按 jellyfishCageMode）→ v_316 [102,26,64]=0.4/0.102/0.251 偏差（两态皆不符）；317/318 缺失
   - 719 RainbowCloud :778（14 相色环）→ 缺失；718 StarCloud :862（夜间且上方非实心 → rand+0.1+Disco/800）→ 缺失；717 LavaCloud :870（num13=0.55+(270-mouse)/800+rand*0.03，×0.5 后 R=1.1n G=0.4n B=0.1n）→ 缺失
   - 429 WireBulb :881-906（frameX/18 位段：bit0→R+0.5, bit1→G+0.5, bit2→B+0.5, bit3→R+0.2/G+0.2）→ specialTileLight case 429 一致
   - 286 GlowingSnailCage / 619 TruffleWormCage :907-912（0.1/0.2/0.7）→ 全缺失
   - 620 EmpressButterflyJar :913（hsl 轮转×0.4）→ 缺失
   - 582 MagmaSnailCage / 598 LavafishBowl :922-927（0.7/0.2/0.1）→ v_598 [255,185,110] 偏差；582 缺失
   - 270 FireflyBottle :928（0.73/1/0.41）、271 LightningBug :933（0.45/0.95/1）、581 Lavafly :938（1/0.75/0.5）、660 Shimmerfly :943（TorchColor(23)）→ 全缺失
   - 572 SoulBottles :946-980（frameY/36 六档 0.9/0.5/0.7 等）→ 缺失
   - 262-268 七色 Gemspark :981-1006（262 R=0.75,B=0.75；263 R=G=0.75；264 B=0.75；265 G=0.75；266 R=0.75；267 全 0.75；268 R=0.75,G=0.375）→ 全缺失
   - 237 LihzahrdAltar :1007（0.1/0.1/0）→ [26,26,0] 一致
   - 238 PlanteraBulb :1011（抬 X/Z 到 0.5）→ 缺失；235 Teleporter :1021（抬 X/Y 到 0.6）→ v_235 缺失
   - 405 Fireplace :1031-1073（frameX<54，样式色+flicker num27=Next(28,42)*0.005+(270-mouse)/700，default 0.9/0.3/0.1）→ [255,185,110]+flicker 偏差
   - 215 Campfire :1074-1164（frameY<36，16 样式 default 0.9/0.3/0.1 + num26 flicker）→ [255,185,110] 偏差
   - 92 Lampposts :1165（frameY<=18 && frameX==0 → 1/1/1）→ [255,255,255] 数值一致但 frameY<=18 门缺失（6 格全亮）偏差(1)
   - 592 BrazierSuspended :1173（frameY>0 → 1.35/0.45/0.15+flicker）→ [255,185,110] 偏差
   - 593/594 Volcano :1186-1201（frameX<18 / <36 → 0.8/0.3/0.1）→ 均 [204,77,26]=0.8/0.302/0.102 数值一致，frameX 门缺失
   - 548 PottedPlants2 :1202（frameX/54>=7 → 0.7/0.3/0.2）→ [179,77,51] 数值一致，门缺失
   - 613/614 PottedLavaPlants :1210-1215（0.7/0.3/0.2）→ 均 [179,77,51] 一致
   - 93 Lamps :1216-1519（frameX==0，frameY/54 样式，default 1/0.97/0.85）→ v_93 [255,185,110] 偏差
   - 96 CookingPots :1520（frameX>=36 → 0.5/0.35/0.1）→ v_96 无 light 缺失
   - 98 SkullLanterns :1528（frameY==0 → 1/0.97/0.85）→ [255,160,70]=1/0.627/0.275 偏差
   - 4 Torch :1536（frameX<66 → TorchColor(frameY/22)）→ 本仓 TORCH_COLORS 表 ✓ 但额外叠加 flicker :236-237（原版无）偏差(1)
   - 372 PeaceCandle :1542（frameX==0 → 0.9/0.1/0.75）→ [230,26,191]=0.902/0.102/0.749 数值一致，门由 LIGHT_TOGGLE 覆盖 ✓
   - 646 ShadowCandle :1550（frameX==0 → 0.2/0.3/0.32）→ 缺失
   - 33 Candles :1558-1851（frameX==0，frameY/22 样式，default 1/0.95/0.65）→ candle [255,185,110]=1/0.725/0.431 偏差
   - 174 PlatinumCandle :1852（frameX==0 → 1/0.95/0.65）→ [255,242,166] 数值一致，门 ✓（LIGHT_TOGGLE）
   - 100/173 Candelabras :1860-2164（frameX<36，frameY/36 样式，default 1/0.95/0.65）→ candelabra [255,185,110] 偏差；v_173 [255,242,166] 数值一致但样式缺失
   - 34 Chandeliers :2165-2471（frameX%108<54，样式=frameY/54+37*(frameX/108)，default 1/1/1）→ chandelier [255,190,120]=1/0.745/0.471 偏差
   - 35 Jackolanterns :2472（frameX<36 → 0.75/0.6/0.3）→ v_35 [179,153,230]=0.702/0.6/0.902 偏差
   - 95 ChineseLanterns :2480（frameX<36 → 1/0.95/0.8）→ [255,160,70]=1/0.627/0.275 偏差，且 FLICKER_SHEETS 含 95 多余闪烁
   - 17/133/302 Furnaces/AdamantiteForge/GlassKiln :2488-2493（0.83/0.6/0.5）→ furnace(17) [255,140,70]=1/0.549/0.275 偏差；v_133 缺失；v_302 [212,153,128]=0.831/0.6/0.502 一致
   - 77 Hellforge :2495（0.75/0.45/0.25）→ v_77 [255,140,70]=1/0.549/0.275 偏差
   - 37 Meteorite :2500（num23=Next(95,106)*0.01 → 0.56n/0.43n/0.15n）→ [143,110,38]=0.561/0.431/0.149 中值一致，闪烁缺失
   - 22/140 Demonite/DemoniteBrick :2508-2515（非漆 26/27 → R=0.12, G=0.07, B=0.32）→ ore_demonite(sheet22) [255,255,153]=1/1/0.6 严重偏差；v_140 缺失
   - 171 ChristmasTree :2517-2575（frameY&0x3C00>>10 十档灯串色 ×0.5）→ v_171 无 light 缺失
   - 204 Crimtane / 347 CrimtaneBrick :2576-2582（非漆 → R=0.35）→ ore_crimtane [89,0,0]=0.349 一致；v_347 缺失
   - 42 HangingLanterns :2583-2912（frameX==0，frameY/36 约 60 样式；0:0.7/0.65/0.55 1:0.9/0.75/0.6 2:0.8/0.6/0.6 3:0.65/0.5/0.2 4:0.5/0.7/0.4 5:0.9/0.4/0.2 7/9:demonTorch 调制 8:0.75/0.6/0.3 11:0.85/0.6/1 14+:1/0.95/0.65 …default **1/1/1**）→ specialTileLight case 42：12 样式值一致、7/9 动态一致，但 default 兜底写成 [0.7,0.65,0.55] 应为 [1,1,1] 偏差，且 style 10/12/13/15-70 大量缺失
   - 49 WaterCandle :2913（frameX==0 → 0/0.35/0.8）→ water_candle [140,180,255]=0.549/0.706/1 偏差，且 FLICKER_SHEETS 含 49 多余闪烁
   - 519 Cattail :2921（frameY==90 → 0.1, 0.2+n12/2, 0.7+n12）→ [26,51,179]=0.102/0.2/0.702 基础值一致，frameY==90 门缺失
   - 70/71/72/190/348/349/528/578 蘑菇组 :2938-2960（R=0,G=0.2+num11/2,B=1；num11=Next(28,42)*0.005+(270-mouse)/1000；349 frameX<36 不发光）→ MUSHROOM_GLOW_SHEETS 公式一致 + 349 门禁一致 ✓（含 519 无关）
   - 739 JellyfishBlock :2962（0.35/0.63/0.7 + paint flag）→ 缺失
   - 350 MartianConduitPlating :2968（-cos 脉动 0..0.2）→ [26,26,26]=0.102 静态近似 偏差(动态缺失)
   - 61/703 JunglePlants :2974-2984（frameX==144 → 0.42*num7/0.81*num6/0.52*num7）→ v_61 [107,207,133]=0.42/0.812/0.522 基础值一致，frameX==144 门与 num6/7 脉动缺失；v_703 缺失
   - 26/31/695/696 DemonAltar/ShadowOrb/复制品 :2985-3003（frameX>=54(26/695) 或 >=36(31/696) → 0.5+n4*2/0.2+n4/0.1；else 0.31+n5/0.1/0.44+n5*2）→ v_26 & v_31 [79,26,112]=0.31/0.102/0.439 else 分支一致，闪烁 n5 缺失 + 第二分支缺失；v_695/v_696 缺失
   - 699 DeadCellsPotionStation :3004（0.4/0.2/0.15）→ 缺失
   - 84 BloomingHerbs :3009-3042（style2/5/6）→ specialTileLight case 84 三档一致 ✓
   - 83 MatureHerbs :3043（frameX==18 且夜间 → 0.1/0.4/0.6；frameX==90 且非雨且 time>40500 → 0.9/0.72/0.18）→ v_83 [230,184,46]=0.902/0.722/0.180 恒亮 偏差（条件全缺）
   - 126 DiscoBall :3057（frameX<36 → Disco RGB）→ specialTileLight case 126 一致 ✓
   - 125 CrystalBall :3065（G=0.3*num,B=0.6*num 直接写 lightColor；num=Next(28,42)*0.01+(270-mouse)/800）→ [0,27,54]=0/0.106/0.212 静态 偏差
   - 129 Crystals :3073-3092（frameX/18%3 → 0/0.05/0.25；0.2/0/0.15；0.1/0/0.2）→ v_129 [0,13,64]=0/0.051/0.251 仅档 0 一致，档 1/2 缺失
   - 149 HolidayLights :3093-3118（frameX<=36，三色档 ×Next(970,1031)*0.001）→ [26,51,128]=0.102/0.2/0.502 仅档 0 基础值，FLICKER 叠加与原版乘性抖动不符 偏差
   - 160 RainbowBrick :3119（Disco×0.25）→ v_160 缺失
   - 354 BewitchingTable :3124（0.65/0.35/0.15）→ [166,89,38]=0.651/0.349/0.149 一致
   - tileLighted 为 true 但 switch 无 case（原版不发光）：19 Platforms、58 Hellstone、76 HellstoneBrick、109 HallowedGrass、346 ChlorophyteBrick、684 AncientHellstoneBrick、701 GlowTulipReplica —— 注意本仓 crystal_heart(sheet12 Heart) light [255,60,90] 与 ore_hellstone(sheet58) light [255,90,40] 属**多加**（原版无此发光）
   - 汇总判定：约 110 个 vanilla 发光 tile 类型；本仓一致 ~20、偏差 ~35、缺失 ~55

   **B. WALL_EMISSIVE 对账（原版 ApplyWallLight :167-342 vs lightTables.ts:93-115）**：21 个墙 id 全部存在，数值偏差集中在宝石墙组：
   - 357 ✓(0.15/0.27/0.3，paint flag 缺)、182 ✓(0.24/0.12/0.09)、33 ✓(0.09/0.0525/0.24)、174 ✓(0.2975/0/0)、175 近似(0.075/0.15/0.4，paint 分支缺)、176 ✓(0.1³)、137 近似(0.5/0.25/0.05 基值，+(270-mouse)/1500+Next(0,50)*0.0005 缺)、44 近似(Disco×0.15 静态化)
   - 153 amber 应 (0.6,0.3,0) → 本仓 [0.6,0.12,0.6] 偏差；154 amethyst 应 (0.6,0,0.6) → [0.6,0.12,0.6] 偏差(G)；155 diamond 应 (0.6,0.6,0.6) → [0.6,0.42,0.06] 偏差；156 emerald 应 (0,0.6,0) → [0.09,0.6,0.24] 偏差；164 ruby 应 (0.6,0,0) → [0.09,0.24,0.6] 偏差；165 sapphire 应 (0,0,0.6) → [0.6,0.06,0.09] 偏差；166 topaz 应 (0.6,0.6,0) → [0.42,0.42,0.6] 偏差（整组错乱）
   - 341/342/343/344/345 ✓（0.25/0.1/0；0.3/0/0.17；0/0.25/0；0/0.16/0.34；0.3/0/0.35）、346 近似(Disco×0.25 静态化)
   - 结构性差异：原版 153-166 无 !LightIsBlocked 门；本仓统一 `wall!==0 && st.type[i]===0` 门；原版墙油漆覆盖分支（:323-329/flag）本仓无

   **C. TORCH_COLORS（TorchID.cs:137-160 vs lightTables.ts:60-85）**：21 条常量全部逐值一致（0:[1,0.95,0.8] 1:[0,0.1,1.3] 2:[1,0.1,0.1] 3:[0,1,0.1] 4:[0.9,0,0.9] 5:[1.4,1.4,1.4] 6:[0.9,0.9,0] 8:[1,1.6,0.5] 9:[0.75,0.85,1.4] 10:[1,0.5,0] 11:[1.4,1.4,0.7] 12:[0.75,1.35,1.5] 13:[0.95,0.75,1.3] 15:[1,0,1] 16:[1.4,0.85,0.55] 17:[0.25,1.3,0.8] 18:[0.95,0.4,1.4] 19:[1.4,0.7,0.5] 20:[1.25,0.6,1.2] 21:[0.75,1.45,0.9] 22:[0.3,0.78,1.2]）；7 DemonTorch 占位 [1,0.3,0.5]（实际走 flicker.demonTorchColor ✓ 与 DemonTorchLight 一致）；14 Disco 占位 [1,1,1]（实际走 discoColor ✓）；23 Shimmer 占位 [1,1,1]（实际走 shimmerTorchColor ✗ 公式错误：应为 r≈0.825-0.89、g=0.55 恒定、b≈1.1-1.187，本仓 0..0.9/0.55..0/0..1.2 摆动）。1.4.5 _lights 长度 24 与注释无新增火把色。另有缺陷：火把 sheet 4 叠加了原版没有的 flicker。

   **D. 液体光源**：岩浆公式一致（本仓 :164 lavaV=0.55+(270-mouse)/900，:262-264 max 合成 R/G=lavaV*0.6/B=lavaV*0.2 ✓ 等价 ApplyLiquidLight :116-132）；**shimmer 液体光完全缺失**（原版 :133-151，本仓无 liquidType===4 分支）；ApplyHellLight 本仓 :161 用 sin(performance.now()*0.002) 替代 sin(GlobalTimeWrappedHourly*2)（近似，周期 ≈1571ms vs 原版游戏小时周期）；原版地狱/天空透光门含 `wall==73(Cloud)||wall==227(Snowfall)` 特例，本仓 WALL_LIGHT 未含 → 云墙/降雪墙天光缺失(2)；彩玻墙染色本仓 max 合成 vs 原版乘法衰减 偏差。

   **E. WALL_LIGHT**：原版 Main.cs:10487-10502 共 16 条（0,21,318,106,317,107,138,140,141,139,145,150,152,245,315,168）；本仓 lightTables.ts:57 15 条 + exposed() 内 `wall===0` 特判 → **全表一致**，0 缺失由调用方处理（符合注释）。

6. All user messages:
   - 唯一实质用户消息（审计任务书）：“你在审计泰拉瑞亚 1:1 移植项目的【发光物光源全量对账】。这是三路代理中的【第一路：tile/墙/液体光源】。光照引擎本体（LightingEngine/LightMap 扫描 Blur）此前已 1:1 移植过，本次只审【光源端】——哪些物体发光、发光条件、发光颜色/强度。本仓实现：game/src/lighting/TileLightScanner.ts（播种扫描器主干 + specialTileLight 动态特例）、game/src/lighting/lightTables.ts（火把色 TORCH_COLORS、发光墙 WALL_EMISSIVE、透光墙 WALL_LIGHT、蘑菇组 MUSHROOM_GLOW_SHEETS、闪烁族 FLICKER_SHEETS、月相地板 MOON_FLOOR、衰减表）、game/src/data/tiles.ts 每个 tile def 的 light?: [r,g,b] 静态字段。原版标杆：Terarria1456/Terraria/Graphics.Light/TileLightScanner.cs + Terraria/Main.cs（wallLight :10487-10503）+ Terraria.ID/TorchID.cs（:134-161 _lights）+ Terraria/TileLoader.cs。审计任务（very thorough）：[五节任务详述，见第 1 节]。输出：五节结构化报告，每条 [原版行号+值, 本仓文件:行号+值, 判定 一致/偏差(N)/缺失]。数值精确到 3 位小数。不要贴大段代码。”
   - 系统提示约束（需持续遵守）：READ-ONLY 严禁创建/修改/删除/移动文件、严禁临时文件、严禁重定向写、只允许只读命令（ls/git status/git log/git diff/find/grep/cat/head/tail）；最终发现直接以文字返回，禁止写报告 .md；路径必须绝对路径；不用 emoji；工具调用前文字不用冒号结尾；快速并行搜索。

7. Pending Tasks:
   - 撰写并输出最终五节结构化审计报告（第一节 静态 tile 光源覆盖率、第二节 WALL_EMISSIVE、第三节 TORCH_COLORS、第四节 液体光源、第五节 WALL_LIGHT），每条 [原版行号+值, 本仓文件:行号+值, 判定]，数值 3 位小数，不贴大段代码。数据已全部采集完毕（见第 5 节），仅需组织成文。

8. Current Work:
   在被要求总结前，我刚完成最后一项数据核对：验证 tileLighted 表中存在但 ApplyTileLight switch 中没有 case 的 tile（确认 19=Platforms、58=Hellstone、76=HellstoneBrick、109=HallowedGrass、346=ChlorophyteBrick、684=AncientHellstoneBrick、701=GlowTulipReplica 在原版不发光），并确认 77=Hellforge 有独立 case（:2495，0.75/0.45/0.25）。此前刚确认 PortalHelper 传送门色计算（portal0 橙 (1,0.47,0)×0.65、portal1 青 (0.2,0.904,1)×0.65），证明本仓 specialTileLight case 209 的紫/橙硬编码两档皆错。所有对账数据齐备，尚未开始写报告正文。

9. Optional Next Step:
   直接撰写最终五节审计报告并作为普通文本消息返回（不调用工具、不写文件）。报告依据第 5 节已采集的完整判定数据，按用户要求格式输出：“五节结构化报告，每条 [原版行号+值, 本仓文件:行号+值, 判定 一致/偏差(N)/缺失]。数值精确到 3 位小数。不要贴大段代码。” 重点突出：第一节需给出 vanilla 全部 ~110 个发光 tile 的 case 清单及逐条判定（含条件门禁缺失标注，如灯笼 default 应为 (1,1,1)、火把多余 flicker、92 路灯 frameY<=18 门、宝石墙 153-166 七条数值错乱、shimmer 液体光缺失、WALL_LIGHT 缺 73/227 特例、shimmerTorchColor 公式错误）。

If you need specific details from before compaction (like exact code snippets, error messages, or content you generated), read the full transcript at: ~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/4a66e745-9d91-4188-8ade-1e2b7775e8b4.jsonl
Continue the conversation from where it left off without asking the user any further questions. Resume directly — do not acknowledge the summary, do not recap what was happening, do not preface with "I'll continue" or similar. Pick up the last task as if the break never happened.
```

---

## 🤖 Assistant · 2026-08-13T06:22:38.141Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
I have all the data. `GlobalTimeWrappedHourly = TotalGameTime.TotalSeconds % 3600` — so it's real-time seconds wrapped at 3600. So `sin(GlobalTimeWrappedHourly * 2)` has period 2π/2 = π seconds ≈ 3.14 real seconds. Repo: `sin(performance.now()*0.002)` — performance.now is ms, ×0.002 → period 2π/0.002 = 3141 ms ≈ 3.14 s. Oh! That's actually equivalent! performance.now()*0.002 = seconds*2. So sin(now_ms * 0.002) = sin(seconds*2). Exactly the same as vanilla since GlobalTimeWrappedHourly = total seconds % 3600 (with wrap at 3600 s which preserves continuity of sin since 3600*2 rad... 7200 rad mod 2π is not 0 but near-continuous jump? 7200/(2π)=1145.9 → discontinuity at wrap. Minor.)

So the hell pulse is actually 1:1 correct. My earlier summary said "period 1571ms vs game-hour" which was wrong. Good catch — I should correct this in the report: ApplyHellLight timing is consistent (sin(seconds*2), period ≈3.142 s), only difference is the 3600 s wrap discontinuity. Let me double check vanilla ApplyHellLight uses `Math.Sin(GlobalTimeWrappedHourly * 2)`.

From summary: "ApplyHellLight :3261-3338：num4=0.55+sin(GlobalTimeWrappedHourly*2)*0.08". And GlobalTimeWrappedHourly = TotalSeconds % 3600. So sin(2*t) where t in seconds. Repo: performance.now() (ms) * 0.002 = 2*t_seconds. Identical. 

But wait — one nuance: vanilla gates ApplyHellLight on `Main.player[Main.myPlayer].position.Y`? No... Let me recheck the hell condition: ApplyHellLight is called in GetTileLight with condition? In vanilla GetTileLight:
```
if (tile.liquid > 0 && tile.liquidType() == LiquidID.Lava) → ApplyLiquidLight
if (y > Main.maxTilesY - 210) → ApplyHellLight  (actually y > UnderworldLayer?)
```
Hmm, from summary: ApplySurfaceLight and ApplyHellLight conditions. Let me quickly verify the GetTileLight call conditions to be precise in the report. Also verify ApplyHellLight gate includes wallLight||73||227.

Actually let me just re-verify the GetTileLight seeding conditions quickly to be accurate.
````

</details>


---

## 🤖 Assistant · 2026-08-13T06:22:38.826Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 89,108p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs; echo ===HELL===; sed -n 3261,3290p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs",
 "description": "Re-read GetTileLight seeding and ApplyHellLight"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:22:38.875Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
	public void GetTileLight(int x, int y, out Vector3 outputColor)
	{
		outputColor = Vector3.Zero;
		Tile tile = Main.tile[x, y];
		FastRandom localRandom = _random.WithModifier(x, y);
		if (y <= (int)Main.worldSurface)
		{
			ApplySurfaceLight(tile, x, y, ref outputColor);
		}
		else if (y > Main.UnderworldLayer)
		{
			ApplyHellLight(tile, x, y, ref outputColor);
		}
		ApplyWallLight(tile, x, y, ref localRandom, ref outputColor);
		if (tile.active())
		{
			ApplyTileLight(tile, x, y, ref localRandom, ref outputColor);
		}
		ApplyLiquidLight(tile, ref outputColor);
	}
(eval):1: ==HELL=== not found

```


---

## 🤖 Assistant · 2026-08-13T06:22:40.848Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The `===HELL===` echo failed because `===HELL===` was interpreted weirdly? "===HELL=== not found" — because `echo ===HELL===` in zsh tries... whatever. Let me just run the second sed separately.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:22:41.157Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '3261,3300p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs",
 "description": "Read ApplyHellLight body"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:22:41.198Z

**📎 ToolResult**

```
	private void ApplyHellLight(Tile tile, int x, int y, ref Vector3 lightColor)
	{
		float num = 0f;
		float num2 = 0f;
		float num3 = 0f;
		float num4 = 0.55f + (float)Math.Sin(Main.GlobalTimeWrappedHourly * 2f) * 0.08f;
		if ((!tile.active() || !Main.tileNoSunLight[tile.type] || ((tile.slope() != 0 || tile.halfBrick()) && Main.tile[x, y - 1].liquid == 0 && Main.tile[x, y + 1].liquid == 0 && Main.tile[x - 1, y].liquid == 0 && Main.tile[x + 1, y].liquid == 0)) && lightColor.X < num4 && (Main.wallLight[tile.wall] || tile.wall == 73 || tile.wall == 227 || (tile.invisibleWall() && !_drawInvisibleWalls)) && tile.liquid < 200 && (!tile.halfBrick() || Main.tile[x, y - 1].liquid < 200))
		{
			num = num4;
			num2 = num4 * 0.6f;
			num3 = num4 * 0.2f;
		}
		if ((!tile.active() || tile.halfBrick() || !Main.tileNoSunLight[tile.type]) && ((tile.wall >= 88 && tile.wall <= 93) || tile.wall == 241) && tile.liquid < byte.MaxValue)
		{
			num = num4;
			num2 = num4 * 0.6f;
			num3 = num4 * 0.2f;
			int num5 = tile.wall - 88;
			if (tile.wall == 241)
			{
				num5 = 6;
			}
			switch (num5)
			{
			case 0:
				num *= 0.9f;
				num2 *= 0.15f;
				num3 *= 0.9f;
				break;
			case 1:
				num *= 0.9f;
				num2 *= 0.9f;
				num3 *= 0.15f;
				break;
			case 2:
				num *= 0.15f;
				num2 *= 0.15f;
				num3 *= 0.9f;
				break;
			case 3:

```


---

## 🤖 Assistant · 2026-08-13T06:22:47.230Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Important discovery: ApplyHellLight ALSO has the stained-glass wall tint branch (walls 88-93/241) that tints the HELL light! The repo only applies the tint in the surface branch... wait, actually repo applies tint unconditionally whenever wall is 88-93/241 and type===0 (with max synthesis). Let me check the repo: in exportTo, the wall tint branch is inside `if (wall !== 0 && st.type[i] === 0)` — applied regardless of surface vs hell depth. So in hell depth, repo also tints (max-synthesis). Vanilla applies tint in both ApplySurfaceLight (:3190-3242) and ApplyHellLight (:3286+). OK so coverage-wise the repo covers both, though with max-synthesis instead of multiply on the sky value. Fine.

Note repo's gate for wall tint requires `st.type[i]===0` (no tile present), but vanilla requires `(!tile.active() || tile.halfBrick() || !tileNoSunLight[type]) && liquid<255` — i.e. tint applies even with non-light-blocking tiles present (e.g., platforms, furniture). Repo's type===0 gate is stricter → deviation (minor).

Also repo applies the emissive wall gate `st.type[i]===0` — vanilla ApplyWallLight gate is `!LightIsBlocked(tile)` where LightIsBlocked checks... let me check LightIsBlocked: probably `(tile.active() && Main.tileBlockLight[tile.type] && tile.type != ... && ...)`. Let me verify, because repo's gate `type===0` may differ for platforms/torches placed on emissive walls.

Let me check LightIsBlocked.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:22:47.822Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"LightIsBlocked\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs | head; sed -n '55,88p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs",
 "description": "Read LightIsBlocked implementation"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:22:47.883Z

**📎 ToolResult**

```
70:		if (LightIsBlocked(tile) && tile.type != 131 && !tile.inActive() && tile.slope() == 0)
154:	private bool LightIsBlocked(Tile tile)
176:			if (!LightIsBlocked(tile))
185:			if (!LightIsBlocked(tile))
193:			if (!LightIsBlocked(tile))
201:			if (!LightIsBlocked(tile))
207:			if (!LightIsBlocked(tile))
222:			if (!LightIsBlocked(tile))
230:			if (!LightIsBlocked(tile))
241:			if (!LightIsBlocked(tile))
		return true;
	}

	public void Update()
	{
		_random.NextSeed();
	}

	public LightMaskMode GetMaskMode(int x, int y)
	{
		return GetTileMask(Main.tile[x, y]);
	}

	private LightMaskMode GetTileMask(Tile tile)
	{
		if (LightIsBlocked(tile) && tile.type != 131 && !tile.inActive() && tile.slope() == 0)
		{
			if (TileID.Sets.CrackedBricks[tile.type])
			{
				return LightMaskMode.CrackedBricks;
			}
			return LightMaskMode.Solid;
		}
		if (!tile.lava() && tile.liquid > 128)
		{
			if (!tile.honey())
			{
				return LightMaskMode.Water;
			}
			return LightMaskMode.Honey;
		}
		return LightMaskMode.None;
	}

```


---

## 🤖 Assistant · 2026-08-13T06:22:49.315Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '154,166p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs",
 "description": "Read LightIsBlocked body"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:22:49.349Z

**📎 ToolResult**

```
	private bool LightIsBlocked(Tile tile)
	{
		if (tile.active() && Main.tileBlockLight[tile.type])
		{
			if (tile.invisibleBlock())
			{
				return _drawInvisibleWalls;
			}
			return true;
		}
		return false;
	}

```


---

## 🤖 Assistant · 2026-08-13T06:23:13.581Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
LightIsBlocked(tile) = tile.active() && Main.tileBlockLight[type] (with echo coating nuance).

So vanilla's ApplyWallLight gate is: wall visible iff NOT (active tile that blocks light). I.e. an emissive wall behind a torch/platform/furniture (non-light-blocking) DOES emit. Repo's gate `st.type[i] === 0` requires air → stricter → deviation: emissive walls (gemspark walls etc.) behind platforms/torches/furniture don't light up in repo.

Also repo's mask gate uses `this.blocksLight[type]` derived from TILE_DEFS (solid && !platform && opacity>=0.9) as approximation of Main.tileBlockLight. Note vanilla tileBlockLight includes many non-solid tiles? Actually tileBlockLight is true for most blocks; for platforms false; for torches false; for trees false, etc. The repo's derivation is roughly right but differs on some (e.g., doors opacity 0.05 → not blocking ✓ matches vanilla tileBlockLight[Door]=false? Actually vanilla tileBlockLight for closed doors is... hmm, TileID sets tileBlockLight[10]=false (doors), fine). Also "invisibleBlock" (echo coating) nuance missing: vanilla echo-coated block does NOT block light (LightIsBlocked returns _drawInvisibleWalls, typically false) but DOES count as mask Solid unless inActive. Repo has no echo-coating handling. Minor note.

Also, the repo's `exposed()` allows AllowLightInWater sheets (54/541/328/459/748/750) — matches vanilla :3161 branch. ✓ Good. But note vanilla :3161 condition: `if (tile.type == 54 || 541 || 328 || 459 || 748 || 750)` inside ApplySurfaceLight — need to verify exact behavior. It's within ApplySurfaceLight. Also vanilla ApplyHellLight does NOT have that AllowLightInWater branch — let me check: ApplyHellLight's first clause is `(!tile.active() || !tileNoSunLight[...] || (slope/half && neighbors liquid==0))` — no AllowLightInWater. Repo's exposed() is used for both sky and hell → repo applies AllowLightInWater to hell too → slight extra light in hell for glass etc. Minor deviation. Actually wait — glass blocks in hell: repo would allow hell light through glass; vanilla wouldn't (glass tileNoSunLight[54]? Actually tileNoSunLight[54]=false for glass, so `!tileNoSunLight[type]` = true → vanilla first clause passes for glass anyway! Since glass doesn't block sunlight, `!Main.tileNoSunLight[tile.type]` is true. So glass gets hell light in vanilla too. Fine, no deviation. Actually the AllowLightInWater branch in ApplySurfaceLight exists precisely because glass in water: condition `tile.liquid >= 200`?? Let me not dig too deep. The repo comment says it mirrors :3161.

OK. I have enough. Also need to double check one thing in section 3: the torch style for tile 4: vanilla `case 4: if (tile.frameX < 66) { TorchColor(tile.frameY/22) }`. Torch frameY/22 ranges 0..23? Actually torch styles: frameY = style*22. Also gate `frameX < 66`?? Hmm, torch frameX < 66 means the top 3 columns? Vanilla torches are 1 tile wide, frameX 0/22/44 for wall variants? Whatever — repo has no frameX gate on torches: it lights all torch tiles. Vanilla gate frameX<66: torches placed on wall have frameX=0? Underwater torch frameX=66? Hmm — actually in 1.4.5 torch frameX encodes the "off" state? Let me quickly check what frameX values torches have. In vanilla, torch tile frameX = 0 normally; the "off" state? Torches can't be toggled off. frameX<66 → 0,22,44 → hmm 3 variants (placed normally, left wall?, right wall?). FrameX 66 would be... The animated frame for torch? Torch tile is 20x20 with TileObjectData; frameX is always 0 for placed torches I think. Actually torch frameX<66 allows 0/22/44 which are the three "wall mount" states? Not important: placed torches always satisfy frameX<66 in practice? Let me verify quickly what sets torch frameX to >=66. WebBulb? No. I recall `torch` frameX used for underwater torch style? There's "torch with biome torches". Hmm.

Let me grep WorldGen/TileObject for torch frameX 66. Actually simpler: check TileData for torch or check `frameX % 66`. I'll do a quick grep in the decompiled source for "frameX = 66" near torch... This may take time; alternatively check `Main.tileFrameImportant[4]`. Torch is frameImportant with TileObjectData newLadder? Let me just grep for "num *= 66" no...

Practical approach: torches on walls vs floor use different frames? In Terraria, torch tile frameX can be 0 (floor), 22 (left wall), 44 (right wall), and 66 would be "underwater"? Not sure. Given the uncertainty, I'll report it as: vanilla gates torch light on `frameX < 66` (TileLightScanner.cs:1536), repo has no such gate — flag as minor conditional deviation (frameX>=66 state doesn't emit). That's accurate as far as the code shows.

Let me check the exact line 1536 text and the lantern default to quote exact values. Let me re-read a few key vanilla segments to make sure my numbers are right for the report: case 4 (:1536), case 42 default & style list, case 92, case 93 default, case 33 default, case 100 default, case 34 default, case 405, case 215, case 98, case 95, case 96, case 17/133/302/77, case 204/347, case 22/140, case 37, case 49, case 519, case 61/703, case 26/31/695/696, case 83, case 125, case 129, case 149, case 160, case 354, case 27, case 356/663, case 658, case 711, case 634, case 633/637/638, case 463, case 491, case 209, case 597, case 564, case 568-570, case 580, case 391, case 381/517/687, case 534/535/689, 536/537/690, 539/540/688, 625/626/691, 627/628/692, case 184, case 370, case 659/667/708, case 336-344, case 327, case 316/317/318, case 719/718/717, case 429, case 286/619, case 620, case 582/598, case 270/271/581/660, case 572, case 262-268, case 237, case 238, case 235, case 592/593/594, case 548, case 613/614, case 96, case 372, case 646, case 171, case 20.

That's a lot of line numbers I already have from the summary. I trust the summary's line numbers (they were collected during full read). But to be safe for a handful of load-bearing quotes (torch case, lantern default, candle default, chandelier default, candelabra default, lamps default), let me grep those specific ones to confirm exact numbers/lines.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:23:14.893Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"TorchColor\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs | head -20; echo ---42default---; sed -n '2890,2915p' ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria.Graphics.Light/TileLightScanner.cs",
 "description": "Confirm torch and lantern default values"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:23:14.960Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
357:					TorchID.TorchColor(23, out R, out G, out B);
944:				TorchID.TorchColor(23, out R, out G, out B);
1152:						TorchID.TorchColor(23, out R, out G, out B);
1539:					TorchID.TorchColor(tile.frameY / 22, out R, out G, out B);
---42default---
sed: ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria.Graphics.Light/TileLightScanner.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-13T06:23:19.689Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The path failed the second time — "No such file or directory"? The first grep worked with that path. Odd — maybe the echo ---42default--- broke zsh parsing (same as before: `---42default---` interpreted?). Yes! zsh treats `---42default---`... no, echo should take it literally. Hmm, but the error came from sed. Maybe the file path got mangled? Actually the error says the file doesn't exist — but grep on the same path worked. Possibly zsh's `echo ---42default---` triggered "not found"? Exit code 1 overall. The issue: `---42default---` starts with `-` and zsh might interpret. Let me just quote it or use a different separator.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:23:20.106Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '2888,2915p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs",
 "description": "Read lantern switch default"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:23:20.160Z

**📎 ToolResult**

```
					G = 0.95f;
					B = 0.65f;
					break;
				case 68:
					R = 47f / 51f;
					G = 0.4117647f;
					B = 1f;
					break;
				case 69:
					R = 38f / 51f;
					G = 38f / 51f;
					B = 1f;
					break;
				case 70:
					R = 43f / 51f;
					G = 35f / 51f;
					B = 49f / 51f;
					break;
				default:
					R = 1f;
					G = 1f;
					B = 1f;
					break;
				}
				break;
			case 49:
				if (tile.frameX == 0)
				{

```


---

## 🤖 Assistant · 2026-08-13T06:23:22.617Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: lantern (42) default = (1,1,1). Repo default [0.7,0.65,0.55] → deviation.

Also note styles 66-70 exist with values. Let me get the full lantern style list to report which styles repo has vs vanilla. Let me dump the case 42 block quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:23:23.782Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "awk 'NR>=2583 && NR<=2912 && (/case [0-9]+:/ || /R = [0-9.\\/f]+;/ || /G = [0-9.\\/f]+;/ || /B = [0-9.\\/f]+;/ || /frameX ==/ || /frameY \\/ 36/)' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs | head -140",
 "description": "Extract lantern case 42 style values"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:23:31.820Z

**📎 ToolResult**

```
			case 42:
				switch (tile.frameY / 36)
				case 0:
					R = 0.7f;
					G = 0.65f;
					B = 0.55f;
				case 1:
					R = 0.9f;
					G = 0.75f;
					B = 0.6f;
				case 2:
					R = 0.8f;
					G = 0.6f;
					B = 0.6f;
				case 3:
					R = 0.65f;
					G = 0.5f;
					B = 0.2f;
				case 4:
					R = 0.5f;
					G = 0.7f;
					B = 0.4f;
				case 5:
					R = 0.9f;
					G = 0.4f;
					B = 0.2f;
				case 6:
					R = 0.7f;
					G = 0.75f;
					B = 0.3f;
				case 7:
				case 8:
					R = 0.75f;
					G = 0.6f;
					B = 0.3f;
				case 9:
					R = 1f;
					G = 0.3f;
					B = 0.5f;
				case 11:
					R = 0.85f;
					G = 0.6f;
					B = 1f;
				case 14:
					R = 1f;
					G = 0.95f;
					B = 0.65f;
				case 15:
				case 16:
					R = 1f;
					G = 0.95f;
					B = 0.65f;
				case 17:
					R = 1f;
					G = 0.97f;
					B = 0.85f;
				case 18:
					R = 0.75f;
					G = 0.85f;
					B = 1f;
				case 21:
					R = 1f;
					G = 0.95f;
					B = 0.65f;
				case 22:
					R = 1f;
					G = 1f;
					B = 0.6f;
				case 23:
					R = 1f;
					G = 0.95f;
					B = 0.65f;
				case 27:
					R = 1f;
					G = 0.95f;
					B = 0.65f;
				case 28:
						R = 0.37f;
						G = 0.8f;
						B = 1f;
				case 29:
					R = 0f;
					G = 0.9f;
					B = 1f;
				case 30:
					R = 0.25f;
					G = 0.7f;
					B = 1f;
				case 32:
					G = 0.3f;
				case 35:
					R = 0.7f;
					G = 0.6f;
					B = 0.9f;
				case 36:
					R = 1f;
					G = 0.95f;
					B = 0.65f;
				case 37:
				case 38:
					R = 1f;
					G = 0.97f;
					B = 0.85f;
				case 39:
					R = 0.55f;
					G = 0.45f;
					B = 0.95f;
				case 40:
					R = 1f;
					G = 0.6f;
					B = 0.1f;
				case 41:
					R = 0.3f;
					G = 0.75f;
					B = 0.55f;
				case 42:
					R = 0.9f;
					G = 0.55f;
					B = 0.7f;
				case 43:
					R = 0.55f;
					G = 0.85f;
					B = 1f;
				case 44:
					R = 1f;
					G = 0.95f;
					B = 0.65f;
				case 45:
					R = 1f;
					G = 0.95f;
					B = 0.65f;
				case 46:
					R = 0.4f;
					G = 0.8f;
					B = 0.9f;
				case 47:
					R = 1f;
					G = 1f;
					B = 1f;
				case 48:

```


---

## 🤖 Assistant · 2026-08-13T06:23:42.853Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Very important: case 9 in the lantern switch is NOT demonTorch! Wait — the summary said styles 7 and 9 use demonTorch modulation. But this dump shows:
- case 7: R=1, G=0.3, B=0.5 (static! — that's the demon torch color-ish? Hmm)

Wait, look at the structure: `case 7:` followed by nothing until `case 8:` — meaning case 7 falls into case 8's code? No — case 7 has no body shown between "case 7:" and "case 8:" except... hmm, the awk filter only kept lines matching patterns; lines like `num14 = Main.demonTorch` wouldn't match. So case 7's body was filtered out (it contains demonTorch lines). Similarly case 9: body filtered out.

So: case 7 body = demonTorch modulation (filtered), case 9 body = demonTorch (filtered). And there's `case 9: R=1, G=0.3, B=0.5` shown after case 8? No wait, look at output again:

```
case 7:
case 8:
   R = 0.75f; G = 0.6f; B = 0.3f;
case 9:
   R = 1f; G = 0.3f; B = 0.5f;
case 11:
```
Hmm — "case 7:" then immediately "case 8:" suggests case 7's body lines were filtered out entirely (demonTorch), OR case 7 is empty and falls through to case 8. And "case 9: R=1,G=0.3,B=0.5" is static. But then what was filtered? Let me check the summary claim: "7/9:demonTorch 调制". The repo implements st===7 → [0.9-d*0.2, 0.9-d*0.2, 0.7+d*0.2] and st===9 → [1-d*0.1, 0.3-d*0.2, 0.5+d*0.2].

Note repo's style 7 values at d=0: (0.9,0.9,0.7) and at d=1: (0.7,0.7,0.9). And style 9: d=0 → (1,0.3,0.5), d=1 → (0.9,0.1,0.7). The static case 9 value (1, 0.3, 0.5) matches the repo's style 9 at d=0! So maybe the actual code is: case 9 has demonTorch lines before setting R=1, G=0.3-0.2d, B=0.5+0.2d? i.e. G = 0.3 - 0.2*demonTorch? But the dump shows `G = 0.3f` literal... unless awk filtered only lines with `G = ` pattern; `G = 0.3f - num * 0.2f` would still match /G = [0-9.\/f]+;/ ? The regex requires the line to end with `;` after digits/dots/slashes/f. "G = 0.3f - num * 0.2f;" ends with "0.2f;" — the pattern `G = [0-9.\/f]+;` requires the whole rest to match [0-9./f]+ then `;`. "0.3f - num * 0.2f" contains spaces/letters → wouldn't match → filtered out. 

So both case 7 and case 9 bodies DO contain demonTorch arithmetic that got filtered. I need to verify exact formulas. Let me read the raw lines around case 7 and 9 in the vanilla source.
````

</details>


---

## 🤖 Assistant · 2026-08-13T06:23:44.881Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"demonTorch\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs; grep -n \"case 42:\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs",
 "description": "Locate demonTorch usage and case 42 line"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:23:45.140Z

**📎 ToolResult**

```
692:				R = 0.4f * Main.demonTorch + 0.6f * (1f - Main.demonTorch);
694:				B = 1f * Main.demonTorch + 0.6f * (1f - Main.demonTorch);
1044:						R = 0.5f * Main.demonTorch + 1f * (1f - Main.demonTorch);
1046:						B = 1f * Main.demonTorch + 0.5f * (1f - Main.demonTorch);
1087:						R = 0.5f * Main.demonTorch + 1f * (1f - Main.demonTorch);
1089:						B = 1f * Main.demonTorch + 0.5f * (1f - Main.demonTorch);
1307:					R = 0.5f * Main.demonTorch + 1f * (1f - Main.demonTorch);
1309:					B = 1f * Main.demonTorch + 0.5f * (1f - Main.demonTorch);
1338:					Vector3 vector10 = Main.hslToRgb(Main.demonTorch * 0.12f + 0.69f, 1f, 0.75f).ToVector3() * 1.2f;
1654:					R = 0.5f * Main.demonTorch + 1f * (1f - Main.demonTorch);
1656:					B = 1f * Main.demonTorch + 0.5f * (1f - Main.demonTorch);
1670:					Vector3 vector8 = Main.hslToRgb(Main.demonTorch * 0.12f + 0.69f, 1f, 0.75f).ToVector3() * 1.2f;
1952:					R = 0.5f * Main.demonTorch + 1f * (1f - Main.demonTorch);
1954:					B = 1f * Main.demonTorch + 0.5f * (1f - Main.demonTorch);
1983:					Vector3 vector6 = Main.hslToRgb(Main.demonTorch * 0.12f + 0.69f, 1f, 0.75f).ToVector3() * 1.2f;
2273:					R = 0.5f * Main.demonTorch + 1f * (1f - Main.demonTorch);
2275:					B = 1f * Main.demonTorch + 0.5f * (1f - Main.demonTorch);
2289:					Vector3 vector4 = Main.hslToRgb(Main.demonTorch * 0.12f + 0.69f, 1f, 0.75f).ToVector3() * 1.2f;
2627:					float num14 = Main.demonTorch * 0.2f;
2642:					B += Main.demonTorch * 0.2f;
2643:					R -= Main.demonTorch * 0.1f;
2644:					G -= Main.demonTorch * 0.2f;
2715:					R = 0.5f * Main.demonTorch + 1f * (1f - Main.demonTorch);
2717:					B = 1f * Main.demonTorch + 0.5f * (1f - Main.demonTorch);
2731:					Vector3 vector2 = Main.hslToRgb(Main.demonTorch * 0.12f + 0.69f, 1f, 0.75f).ToVector3() * 1.2f;
1394:				case 42:
1731:				case 42:
2039:				case 42:
2315:				case 42:
2583:			case 42:
2757:				case 42:

```


---

## 🤖 Assistant · 2026-08-13T06:23:47.107Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read 2615-2660 to get the lantern case 7/9 formulas exactly.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:23:47.501Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '2615,2660p' ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria.Graphics.Light/TileLightScanner.cs",
 "description": "Read lantern style 7 and 9 formulas"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:23:47.631Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
sed: ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria.Graphics.Light/TileLightScanner.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-13T06:23:49.915Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Weird — the file intermittently fails? "No such file or directory" but grep on the same path worked just before. This smells like the sandbox/permission system intermittently denying. Let me retry, maybe with Read tool instead.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:23:50.149Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs",
 "offset": 2615,
 "limit": 50
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:23:50.169Z

**📎 ToolResult**

```
2615					case 5:
2616						R = 0.9f;
2617						G = 0.4f;
2618						B = 0.2f;
2619						break;
2620					case 6:
2621						R = 0.7f;
2622						G = 0.75f;
2623						B = 0.3f;
2624						break;
2625					case 7:
2626					{
2627						float num14 = Main.demonTorch * 0.2f;
2628						R = 0.9f - num14;
2629						G = 0.9f - num14;
2630						B = 0.7f + num14;
2631						break;
2632					}
2633					case 8:
2634						R = 0.75f;
2635						G = 0.6f;
2636						B = 0.3f;
2637						break;
2638					case 9:
2639						R = 1f;
2640						G = 0.3f;
2641						B = 0.5f;
2642						B += Main.demonTorch * 0.2f;
2643						R -= Main.demonTorch * 0.1f;
2644						G -= Main.demonTorch * 0.2f;
2645						break;
2646					case 11:
2647						R = 0.85f;
2648						G = 0.6f;
2649						B = 1f;
2650						break;
2651					case 14:
2652						R = 1f;
2653						G = 0.95f;
2654						B = 0.65f;
2655						break;
2656					case 15:
2657					case 16:
2658						R = 1f;
2659						G = 0.95f;
2660						B = 0.65f;
2661						break;
2662					case 17:
2663						R = 1f;
2664						G = 0.97f;

```


---

## 🤖 Assistant · 2026-08-13T06:23:54.705Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Lantern case 42 styles 7/9 confirmed: repo matches exactly (style 7: R=0.9-d*0.2, G=0.9-d*0.2, B=0.7+d*0.2 ✓; style 9: R=1-d*0.1, G=0.3-d*0.2, B=0.5+d*0.2 ✓). Good — repo's dynamic lantern styles are 1:1.

Now, big correction needed: the summary's claim about lantern styles is fine. But there's a MAJOR correction: the summary claimed case 42 spans "frameX==0, frameY/36 约 60 样式" — confirmed, styles 0..70 with default (1,1,1). Repo only has styles 0-6, 8, 11, 14 + 7/9 dynamic. So styles 10, 12, 13, 15-70 missing → fall back to wrong [0.7,0.65,0.55] instead of their actual values or (1,1,1) default. Confirmed deviation.

Now I also need to double check the lantern case frameX gate. Vanilla case 42 gate: `if (tile.frameX == 0)`? Let me check line 2583-2600.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:23:54.963Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs",
 "limit": 18,
 "offset": 2583
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:23:54.974Z

**📎 ToolResult**

```
2583				case 42:
2584					if (tile.frameX != 0)
2585					{
2586						break;
2587					}
2588					switch (tile.frameY / 36)
2589					{
2590					case 0:
2591						R = 0.7f;
2592						G = 0.65f;
2593						B = 0.55f;
2594						break;
2595					case 1:
2596						R = 0.9f;
2597						G = 0.75f;
2598						B = 0.6f;
2599						break;
2600					case 2:

```


---

## 🤖 Assistant · 2026-08-13T06:24:01.712Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: `if (tile.frameX != 0) break;` — lantern with frameX != 0 emits nothing. Repo: `if (frameX !== 0) return null;` ✓ 1:1.

Now I have enough confidence in the data. One more critical verification for section 1: the candle/lamp/chandelier/candelabra style gates and defaults, since repo has static def.light for candle (33), candelabra (100), chandelier (34), lamp (93). Let me verify:
- case 33 Candles: gate frameX==0, style frameY/22, default (1,0.95,0.65). Also style 6? Let me check what styles have special colors (e.g. demon candle style 6 → demonTorch).
- case 93 Lamps: gate frameX==0, style frameY/54, default (1,0.97,0.85).
- case 100 Candelabras: gate frameX<36, style frameY/36, default (1,0.95,0.65).
- case 34 Chandeliers: gate frameX%108<54, style = frameY/54 + 37*(frameX/108), default (1,1,1).

Let me verify these gates quickly with grep for the enclosing cases. Actually, the demonTorch lines at 1654/1670 (case 33 block is 1558-1851), 1952/1983 (case 100 block 1860-2164), 2273/2289 (case 34 block 2165-2471), 1307/1338 (case 93 block 1216-1519) — so each of candles/lamps/candelabras/chandeliers has a demonTorch style AND an hsl rainbow style (disco? no — hslToRgb(demonTorch*0.12+0.69) is the "cursed/demon" style). So candle style lists are richer than repo's single static color. That confirms deviation for all four families.

Let me confirm the gates and defaults for 33/93/100/34 with a targeted read of the case headers.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:24:02.563Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -nE \"case (33|34|49|92|93|95|96|98|100|174|372|215|405|592|593|594|548|613|614):\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs",
 "description": "Locate lamp family case lines"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:24:02.607Z

**📎 ToolResult**

```
192:		case 33:
200:		case 174:
1031:			case 405:
1074:			case 215:
1165:			case 92:
1173:			case 592:
1186:			case 593:
1194:			case 594:
1202:			case 548:
1210:			case 613:
1211:			case 614:
1216:			case 93:
1349:				case 33:
1354:				case 34:
1432:				case 49:
1520:			case 96:
1528:			case 98:
1542:			case 372:
1558:			case 33:
1686:				case 33:
1691:				case 34:
1769:				case 49:
1852:			case 174:
1860:			case 100:
1994:				case 33:
1999:				case 34:
2077:				case 49:
2165:			case 34:
2350:				case 49:
2480:			case 95:
2792:				case 49:
2913:			case 49:

```


---

## 🤖 Assistant · 2026-08-13T06:24:04.758Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "f=~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs\nsed -n '1558,1575p;1216,1232p;1860,1876p;2165,2185p;1165,1172p;1520,1541p' \"$f\"",
 "description": "Read lamp family case gates and defaults"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:24:04.799Z

**📎 ToolResult**

```
			case 92:
				if (tile.frameY <= 18 && tile.frameX == 0)
				{
					R = 1f;
					G = 1f;
					B = 1f;
				}
				break;
			case 93:
				if (tile.frameX != 0)
				{
					break;
				}
				switch (tile.frameY / 54)
				{
				case 1:
					R = 0.95f;
					G = 0.95f;
					B = 0.5f;
					break;
				case 2:
					R = 0.85f;
					G = 0.6f;
					B = 1f;
					break;
			case 96:
				if (tile.frameX >= 36)
				{
					R = 0.5f;
					G = 0.35f;
					B = 0.1f;
				}
				break;
			case 98:
				if (tile.frameY == 0)
				{
					R = 1f;
					G = 0.97f;
					B = 0.85f;
				}
				break;
			case 4:
				if (tile.frameX < 66)
				{
					TorchID.TorchColor(tile.frameY / 22, out R, out G, out B);
				}
				break;
			case 33:
				if (tile.frameX != 0)
				{
					break;
				}
				switch (tile.frameY / 22)
				{
				case 0:
					R = 1f;
					G = 0.95f;
					B = 0.65f;
					break;
				case 1:
					R = 0.55f;
					G = 0.85f;
					B = 0.35f;
					break;
				case 2:
			case 100:
			case 173:
				if (tile.frameX >= 36)
				{
					break;
				}
				switch (tile.frameY / 36)
				{
				case 1:
					R = 0.95f;
					G = 0.95f;
					B = 0.5f;
					break;
				case 2:
					R = 0.85f;
					G = 0.6f;
					B = 1f;
			case 34:
			{
				if (tile.frameX % 108 >= 54)
				{
					break;
				}
				int num24 = tile.frameY / 54;
				switch (num24 + 37 * (tile.frameX / 108))
				{
				case 7:
					R = 0.95f;
					G = 0.95f;
					B = 0.5f;
					break;
				case 8:
					R = 0.85f;
					G = 0.6f;
					B = 1f;
					break;
				case 9:
					R = 1f;

```


---

## 🤖 Assistant · 2026-08-13T06:24:23.918Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All confirmed:
- case 92: gate `frameY<=18 && frameX==0` → (1,1,1). Repo v_92 light [255,255,255] with LIGHT_TOGGLE gate ['x',18] → lightIsOn(92, frameX, frameY): `v % (2*18) < 18` i.e. frameX%36<18. Vanilla gate is frameX==0 AND frameY<=18. Repo's gate ignores frameY entirely and allows frameX in {0,18} (well frameX%36<18 → frameX==0 for style frames? frameX for lamppost could be 0..108 for styles). Hmm: lamppost styles use frameY/54? Actually lamppost is 1x6 with style in frameY. Vanilla gate frameY<=18 means only the top 1 tile of the 6-tile lamppost emits! Repo applies to all 6 tiles (def.light on every tile of the framed object) → big deviation: repo lamppost glows from all 6 cells vs vanilla only top cell. Good catch to report: gate should be frameY<=18 && frameX==0.

Wait, actually let me double check: lamppost frameY<=18 → the first row. Yes vanilla: only the top cell lights. Repo: every cell of the 1x6 framed object gets def.light → 6 cells lit. Also frameX==0: lamppost has styles via frameX? Whatever — report the two gates missing.

- case 93 (lamps): gate frameX==0 ✓ repo has LIGHT_TOGGLE 93:['x',18] → frameX%36<18 → allows frameX==0 and 18. Vanilla strictly frameX==0. Slight over-glow (frameX==18 = "off" toggled state? LIGHT_TOGGLE semantics flip by ±offset; for a 1-wide lamp, toggling sets frameX=18). So repo's lightIsOn(93, 18) → 18%36=18 <18? No: 18<18 is false → off. So for lamps, lightIsOn(93, frameX=18) = false ✓ correct; frameX=0 → 0<18 true ✓. So the toggle gate is equivalent to frameX==0 for values in {0,18}. But what about other frameX values (e.g. animated)? Lamps don't animate. OK so gate ≈ equivalent. Fine — mark lamp toggle gate as effectively 1:1, but note light style (frameY/54) missing: repo static [255,185,110]=(1,0.725,0.431) vs vanilla style-dependent values (case 0: default? need default value) — case 93 default (1,0.97,0.85) per summary. So repo lamp color wrong + style variants missing (case 1: 0.95/0.95/0.5, case 2: 0.85/0.6/1, demon style, hsl style...).

- case 100/173 candelabra: gate frameX<36 ✓ (LIGHT_TOGGLE 100:['x',18] → frameX%36<18; vanilla frameX<36 allows 0 and 18! Hmm: candelabra is 2 wide (36px); frameX for style columns 0..∞; toggled-off state adds 36? Per devices comment, LIGHT_TOGGLE for 100 is ['x',18]?? That seems odd for a 2-wide object. Vanilla gate frameX>=36 → break (i.e. off state is frameX>=36). Repo lightIsOn(100, frameX, frameY) = frameX % 36 < 18. For a placed candelabra with frameX=0 → 0<18 ✓ on. With frameX=36 (off) → 36%36=0<18 → on ✗ WRONG (should be off). Hmm! Unless the toggle offset for candelabras is 18? Let me check devices.ts LIGHT_TOGGLE: from summary: "100/173:['x',36]"? Summary says: `4:['x',66], 33/174/49/372:['x',18], 42/92/93:['x',18], 95/100/126/173/564:['x',36], 34/149:['x',54], 215:['y',36]`. So 100/173 are ['x',36] → frameX%72<36. For frameX=0: 0<36 ✓ on; frameX=36 (off): 36%72=36 <36 false ✓ off. Correct.

And 42/92/93 ['x',18]: lantern frameX 0 (on) vs 18 (off): 18%36=18<18 false ✓ off. ✓.
And 33/174/49/372 ['x',18]: candle 1-wide: 0 on, 18 off ✓ vanilla gates frameX==0 ✓ equivalent.
And 95 ['x',36]: chinese lantern 2-wide: vanilla gate frameX<36 ✓ equivalent.
And 564 ['x',36]: plasma lamp 2-wide vanilla gate frameX<36 ✓.
And 34/149 ['x',54]: chandelier 3-wide (108px): vanilla gate frameX%108<54 ✓ equivalent. Holiday lights 149: vanilla gate frameX<=36? Summary says 149 frameX<=36. Hmm — 149 is 1x1? Actually holiday lights are 1x1 tiles chained. Vanilla: `if (tile.frameX <= 36)`. Repo ['x',54] → frameX%108<54. For frameX in 0..54 on? Vanilla allows frameX<=36 → 0,18,36; excludes 54+. Repo allows 0..53. Over-glow for frameX in 37..53. Minor deviation. Let me verify 149's gate quickly.
And 215 campfire ['y',36]: vanilla gate frameY<36 (3x2=3 wide 2 tall=54x36); repo gate frameY%72<36 → equivalent for 0/36. ✓
And 4 torch ['x',66]: vanilla frameX<66 ✓ equivalent.

Let me verify case 149 gate and case 126/564/405 gates quickly, plus case 593/594, 548, 613/614, 35 (jackolantern), 95, 49, 372.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:24:25.151Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "f=~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs\nsed -n '3093,3100p;541,548p;3057,3064p;1031,1040p;1074,1082p;2472,2487p;2480,2499p;2913,2927p;1542,1557p' \"$f\"",
 "description": "Read gates for 149, 564, 126, 405, 215, 35, 17, 49, 372"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:24:25.241Z

**📎 ToolResult**

```
			case 564:
				if (tile.frameX < 36)
				{
					R = 0.05f;
					G = 0.3f;
					B = 0.55f;
				}
				break;
			case 405:
				if (tile.frameX < 54)
				{
					float num27 = (float)localRandom.Next(28, 42) * 0.005f;
					num27 += (float)(270 - Main.mouseTextColor) / 700f;
					switch (tile.frameX / 54)
					{
					case 1:
						R = 0.7f;
						G = 1f;
			case 215:
				if (tile.frameY < 36)
				{
					float num26 = (float)localRandom.Next(28, 42) * 0.005f;
					num26 += (float)(270 - Main.mouseTextColor) / 700f;
					switch (tile.frameX / 54)
					{
					case 1:
						R = 0.7f;
			case 372:
				if (tile.frameX == 0)
				{
					R = 0.9f;
					G = 0.1f;
					B = 0.75f;
				}
				break;
			case 646:
				if (tile.frameX == 0)
				{
					R = 0.2f;
					G = 0.3f;
					B = 0.32f;
				}
				break;
			case 35:
				if (tile.frameX < 36)
				{
					R = 0.75f;
					G = 0.6f;
					B = 0.3f;
				}
				break;
			case 95:
			case 95:
				if (tile.frameX < 36)
				if (tile.frameX < 36)
				{
				{
					R = 1f;
					R = 1f;
					G = 0.95f;
					G = 0.95f;
					B = 0.8f;
					B = 0.8f;
				}
				}
				break;
				break;
			case 17:
			case 133:
			case 302:
				R = 0.83f;
				G = 0.6f;
				B = 0.5f;
				break;
			case 77:
				R = 0.75f;
				G = 0.45f;
				B = 0.25f;
				break;
			case 49:
				if (tile.frameX == 0)
				{
					R = 0f;
					G = 0.35f;
					B = 0.8f;
				}
				break;
			case 519:
				if (tile.frameY == 90)
				{
					if (tile.color() == 0)
					{
						float num12 = (float)localRandom.Next(28, 42) * 0.005f;
						num12 += (float)(270 - Main.mouseTextColor) / 1000f;
			case 126:
				if (tile.frameX < 36)
				{
					R = (float)Main.DiscoR / 255f;
					G = (float)Main.DiscoG / 255f;
					B = (float)Main.DiscoB / 255f;
				}
				break;
			case 149:
				if (tile.frameX <= 36)
				{
					switch (tile.frameX / 18)
					{
					case 0:
						R = 0.1f;
						G = 0.2f;

```


---

## 🤖 Assistant · 2026-08-13T06:24:43.443Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All confirmed:
- 564: gate frameX<36 → (0.05, 0.3, 0.55); repo [13,77,140]/255 = (0.051, 0.302, 0.549) ✓ value 1:1; gate via LIGHT_TOGGLE ['x',36] → frameX%72<36 ✓ equivalent; plus FLICKER_SHEETS contains 564 → repo adds flicker (0.14-0.21+...) which vanilla does NOT have for 564 → deviation (extra flicker).
- 405 fireplace: gate frameX<54, flicker num27, styles by frameX/54. Default (0.9,0.3,0.1)? Summary said default 0.9/0.3/0.1. Repo [255,185,110]=(1,0.725,0.431) + flicker → deviation (values + style variants missing).
- 215 campfire: gate frameY<36 ✓ repo ['y',36] ✓; styles frameX/54 (16 variants); default (0.9,0.3,0.1) per summary. Repo (1,0.725,0.431)+flicker → deviation.
- 372 peace candle: gate frameX==0 → (0.9,0.1,0.75); repo [230,26,191]/255=(0.902,0.102,0.749) ✓; gate ['x',18] → frameX%36<18: for 1-wide candle frameX∈{0,18} → 0→on, 18→off ✓ equivalent. But wait: FLICKER_SHEETS includes 372! So repo adds flicker to peace candle → vanilla has none → extra flicker deviation. Let me check FLICKER_SHEETS list: {33,49,92,93,174,34,149,95,100,126,173,564,215,405,4}. 372 not in it. Good — no flicker on 372. ✓ 一致.
- 646 shadow candle: gate frameX==0 → (0.2,0.3,0.32) — repo missing → 缺失.
- 35 jackolantern: gate frameX<36 → (0.75,0.6,0.3). Repo [179,153,230]=(0.702,0.6,0.902) → deviation (R off, B way off). Gate: LIGHT_TOGGLE has 35? Not in list! devices LIGHT_TOGGLE listed: 4,33,174,49,372,42,92,93,95,100,126,173,564,34,149,215. 35 not included → jackolantern "off" state (frameX=36) still glows in repo. Extra deviation.
- 95 chinese lantern: gate frameX<36 → (1,0.95,0.8). Repo [255,160,70]=(1,0.627,0.275) → deviation; gate ['x',36] ✓ equivalent; FLICKER_SHEETS includes 95 → extra flicker (vanilla none) → deviation(2).
- 17/133/302: (0.83,0.6,0.5), no gate. Repo furnace(17) [255,140,70]=(1,0.549,0.275) → deviation; v_133 no light → 缺失; v_302 [212,153,128]=(0.831,0.6,0.502) ✓ 一致.
- 77 hellforge: (0.75,0.45,0.25). Repo [255,140,70]=(1,0.549,0.275) → deviation.
- 49 water candle: gate frameX==0 → (0,0.35,0.8). Repo [140,180,255]=(0.549,0.706,1) → deviation; gate ['x',18] ✓; FLICKER_SHEETS includes 49 → extra flicker → deviation(2).
- 519 cattail: gate frameY==90 && color()==0 → num12 flicker... Repo [26,51,179]=(0.102,0.2,0.702) static, no frameY gate → deviation (gate missing + flicker missing + paint branch missing).
- 126 disco ball: gate frameX<36 → Disco/255. Repo specialTileLight case 126 ✓ gate ✓ discoColor ✓. BUT FLICKER_SHEETS includes 126 → repo ALSO runs the flicker branch? Wait — for 126, def.light is undefined (v_126 has no light), so `d.light || MUSHROOM_GLOW_SHEETS.has(sheet)` is false → the static branch (with FLICKER check) is skipped entirely. So FLICKER_SHEETS containing 126/149/173... only matters for sheets that HAVE def.light. Let me check which sheets have def.light AND are in FLICKER_SHEETS:
  - 4 torch (has light) → flicker applied ✗ vanilla none
  - 33 candle (has light) → flicker ✗
  - 49 water_candle (has light) → flicker ✗
  - 92 lamppost (has light) → flicker ✗
  - 93 lamp (has light) → flicker ✗
  - 174 platinum candle (has light) → flicker ✗
  - 95 chinese lantern (has light) → flicker ✗
  - 100 candelabra (has light) → flicker ✗
  - 173 (has light [255,242,166]) → flicker ✗
  - 564 plasma lamp (has light) → flicker ✗
  - 215 campfire (has light) → flicker ✓ vanilla HAS flicker ✓
  - 405 fireplace (has light) → flicker ✓ vanilla HAS ✓
  - 34 chandelier (has light) → flicker ✗ vanilla none
  - 149 holiday lights (has light [26,51,128]) → flicker ✗ (vanilla has a different multiplicative rand)
  - 126 no def.light → no effect
  So 11 sheets get spurious flicker, and 592 (brazier, vanilla HAS flicker) gets none. Also note the flicker values: vanilla flicker = Next(28,42)*0.005 + (270-mouse)/700 ∈ [0.14+0, 0.21+0.0225] ≈ [0.14, 0.2325] — repo identical formula ✓ for the sheets where it applies.

Also note: repo applies flicker additively to all three channels — matches vanilla (R/G/B += num). ✓.

One more check: v_592 light [255,185,110] vs vanilla (1.35, 0.45, 0.15)? Summary says 592: frameY>0 → 1.35/0.45/0.15 + flicker. Let me verify line 1173.

Also need case 593/594 (volcano), 548, 613/614, 98 skull lantern, 96 cooking pot — verified above:
- 96: frameX>=36 → (0.5,0.35,0.1). Repo cooking_pot def has NO light → 缺失.
- 98: frameY==0 → (1,0.97,0.85). Repo [255,160,70] → deviation; gate: 98 is 2x2, frameY==0 = top row only. Repo applies to all 4 cells; no LIGHT_TOGGLE for 98 → no gate. Deviation(2) (color + row gate).
- 593/594 volcano: verify values.

Let me read 1173-1225.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:24:43.889Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "f=~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs\nsed -n '1173,1215p' \"$f\"",
 "description": "Read brazier, volcano, potted plants values"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:24:43.922Z

**📎 ToolResult**

```
			case 592:
				if (tile.frameY > 0)
				{
					float num25 = (float)localRandom.Next(28, 42) * 0.005f;
					num25 += (float)(270 - Main.mouseTextColor) / 700f;
					R = 1.35f;
					G = 0.45f;
					B = 0.15f;
					R += num25;
					G += num25;
					B += num25;
				}
				break;
			case 593:
				if (tile.frameX < 18)
				{
					R = 0.8f;
					G = 0.3f;
					B = 0.1f;
				}
				break;
			case 594:
				if (tile.frameX < 36)
				{
					R = 0.8f;
					G = 0.3f;
					B = 0.1f;
				}
				break;
			case 548:
				if (tile.frameX / 54 >= 7)
				{
					R = 0.7f;
					G = 0.3f;
					B = 0.2f;
				}
				break;
			case 613:
			case 614:
				R = 0.7f;
				G = 0.3f;
				B = 0.2f;
				break;

```


---

## 🤖 Assistant · 2026-08-13T06:24:49.534Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed:
- 592 brazier: gate frameY>0, (1.35,0.45,0.15)+flicker. Repo [255,185,110]=(1,0.725,0.431) static, no flicker, no gate → deviation(3).
- 593: gate frameX<18 → (0.8,0.3,0.1). Repo [204,77,26]=(0.8,0.302,0.102) ✓ value; gate: no LIGHT_TOGGLE for 593 → repo glows on off-frame too → deviation(1 gate). Vanilla: 593 is 1x1, frameX<18 = on state.
- 594: gate frameX<36 → (0.8,0.3,0.1). Repo [204,77,26] ✓ value; gate missing → deviation(1).
- 548: gate frameX/54>=7 → (0.7,0.3,0.2). Repo [179,77,51]=(0.702,0.302,0.2) ✓ value; gate missing (repo glows for all styles 0-6) → deviation(1).
- 613/614: (0.7,0.3,0.2) no gate. Repo both [179,77,51] ✓ 一致.

Now I'm confident. Let me also verify a handful of section-1 cases I marked "一致" to be safe: 463 (0.2,0.4,0.8), 491 (0.5,0.4,0.7), 634 (0.65,0.3,0.1), 633/637/638 (0.325,0.15,0.05), 354 (0.65,0.35,0.15), 237 (0.1,0.1,0), 340 (0.45,1,0.45), 711 (0.01,0.01,0.01), 356 (0.45,0.25,0), 302. And 656 glow tulip (0.2,0.55,0.5). And 209 portal. And 597 pylon ×0.75.

Let me batch-verify these.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:24:50.822Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "f=~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs\nsed -n '378,398p;410,448p;448,492p;541,548p;574,614p;654,674p;674,712p;1007,1030p;3055,3075p;3119,3130p' \"$f\"",
 "description": "Verify remaining tile case values batch one"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:24:50.856Z

**📎 ToolResult**

```
			case 356:
				if (Main.sundialCooldown == 0)
				{
					R = 0.45f;
					G = 0.25f;
					B = 0f;
				}
				break;
			case 663:
				if (Main.moondialCooldown == 0)
				{
					R = 0f;
					G = 0.25f;
					B = 0.45f;
				}
				break;
			case 656:
				R = 0.2f;
				G = 0.55f;
				B = 0.5f;
				break;
			case 634:
				R = 0.65f;
				G = 0.3f;
				B = 0.1f;
				break;
			case 633:
			case 637:
			case 638:
				R = 0.325f;
				G = 0.15f;
				B = 0.05f;
				break;
			case 463:
				R = 0.2f;
				G = 0.4f;
				B = 0.8f;
				break;
			case 491:
				R = 0.5f;
				G = 0.4f;
				B = 0.7f;
				break;
			case 209:
				if (tile.frameX == 234 || tile.frameX == 252)
				{
					Vector3 vector11 = PortalHelper.GetPortalColor(Main.myPlayer, 0).ToVector3() * 0.65f;
					R = vector11.X;
					G = vector11.Y;
					B = vector11.Z;
				}
				else if (tile.frameX == 306 || tile.frameX == 324)
				{
					Vector3 vector12 = PortalHelper.GetPortalColor(Main.myPlayer, 1).ToVector3() * 0.65f;
					R = vector12.X;
					G = vector12.Y;
					B = vector12.Z;
				}
				break;
			case 415:
			case 415:
				R = 0.7f;
				G = 0.5f;
				B = 0.1f;
				break;
			case 500:
				R = 0.525f;
				G = 0.375f;
				B = 0.075f;
				break;
			case 416:
				R = 0f;
				G = 0.6f;
				B = 0.7f;
				break;
			case 501:
				R = 0f;
				G = 0.45f;
				B = 0.525f;
				break;
			case 417:
				R = 0.6f;
				G = 0.2f;
				B = 0.6f;
				break;
			case 502:
				R = 0.45f;
				G = 0.15f;
				B = 0.45f;
				break;
			case 418:
				R = 0.6f;
				G = 0.6f;
				B = 0.9f;
				break;
			case 503:
				R = 0.45f;
				G = 0.45f;
				B = 0.675f;
				break;
			case 390:
				R = 0.4f;
				G = 0.2f;
				B = 0.1f;
				break;
			case 564:
				if (tile.frameX < 36)
				{
					R = 0.05f;
					G = 0.3f;
					B = 0.55f;
				}
				break;
			case 381:
			case 517:
			case 687:
				R = 0.25f;
				G = 0.1f;
				B = 0f;
				break;
			case 534:
			case 535:
			case 689:
				R = 0f;
				G = 0.25f;
				B = 0f;
				break;
			case 536:
			case 537:
			case 690:
				R = 0f;
				G = 0.16f;
				B = 0.34f;
				break;
			case 539:
			case 540:
			case 688:
				R = 0.3f;
				G = 0f;
				B = 0.17f;
				break;
			case 625:
			case 626:
			case 691:
				R = 0.3f;
				G = 0f;
				B = 0.35f;
				break;
			case 627:
			case 628:
			case 692:
				R = (float)Main.DiscoR / 255f * 0.25f;
				G = (float)Main.DiscoG / 255f * 0.25f;
				B = (float)Main.DiscoB / 255f * 0.25f;
			case 370:
				R = 0.32f;
				G = 0.16f;
				B = 0.12f;
				break;
			case 659:
			case 667:
			case 708:
			{
				Vector4 shimmerBaseColor = LiquidRenderer.GetShimmerBaseColor(x, y);
				R = shimmerBaseColor.X;
				G = shimmerBaseColor.Y;
				B = shimmerBaseColor.Z;
				break;
			}
			case 711:
				R = 0.01f;
				G = 0.01f;
				B = 0.01f;
				break;
			case 27:
			case 27:
				if (tile.frameY < 36)
				{
					R = 0.3f;
					G = 0.27f;
				}
				break;
			case 336:
				R = 0.85f;
				G = 0.5f;
				B = 0.3f;
				break;
			case 340:
				R = 0.45f;
				G = 1f;
				B = 0.45f;
				break;
			case 341:
				R = 0.4f * Main.demonTorch + 0.6f * (1f - Main.demonTorch);
				G = 0.35f;
				B = 1f * Main.demonTorch + 0.6f * (1f - Main.demonTorch);
				break;
			case 342:
				R = 0.5f;
				G = 0.5f;
				B = 1.1f;
				break;
			case 343:
				R = 0.85f;
				G = 0.85f;
				B = 0.3f;
				break;
			case 344:
				R = 0.6f;
				G = 1.026f;
				B = 0.96000004f;
				break;
			case 327:
			{
			case 237:
				R = 0.1f;
				G = 0.1f;
				break;
			case 238:
				if ((double)lightColor.X < 0.5)
				{
					lightColor.X = 0.5f;
				}
				if ((double)lightColor.Z < 0.5)
				{
					lightColor.Z = 0.5f;
				}
				break;
			case 235:
				if ((double)lightColor.X < 0.6)
				{
					lightColor.X = 0.6f;
				}
				if ((double)lightColor.Y < 0.6)
				{
					lightColor.Y = 0.6f;
				}
				break;
				}
				break;
			case 126:
				if (tile.frameX < 36)
				{
					R = (float)Main.DiscoR / 255f;
					G = (float)Main.DiscoG / 255f;
					B = (float)Main.DiscoB / 255f;
				}
				break;
			case 125:
			{
				float num = (float)localRandom.Next(28, 42) * 0.01f;
				num += (float)(270 - Main.mouseTextColor) / 800f;
				G = (lightColor.Y = 0.3f * num);
				B = (lightColor.Z = 0.6f * num);
				break;
			}
			case 129:
				switch (tile.frameX / 18 % 3)
				{
			case 160:
				R = (float)Main.DiscoR / 255f * 0.25f;
				G = (float)Main.DiscoG / 255f * 0.25f;
				B = (float)Main.DiscoB / 255f * 0.25f;
				break;
			case 354:
				R = 0.65f;
				G = 0.35f;
				B = 0.15f;
				break;
			}
		}

```


---

## 🤖 Assistant · 2026-08-13T06:24:58.845Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All confirmed. A few notes refined:

- 237 Lihzahrd Altar: R=0.1, G=0.1, B unset (=0) ✓ repo [26,26,0]=(0.102,0.102,0) ✓ 一致.
- 238 Plantera Bulb: raises X,Z to 0.5 — repo missing → 缺失.
- 235 Teleporter: raises X,Y to 0.6 — repo v_235 has no light → 缺失.
- 656 Glow Tulip: (0.2,0.55,0.5) vs repo [255,185,110]=(1,0.725,0.431) → 偏差.
- 27 Sunflower: gate frameY<36 → R=0.3, G=0.27, B=0. Repo [255,242,166]=(1,0.949,0.651) → 偏差(2) (值+门).
- 711 Rainbow Boulder: (0.01,0.01,0.01) vs repo [3,3,3]=(0.0118,...) → 一致(≈).
- 340: (0.45,1,0.45) vs repo [115,255,115]=(0.451,1,0.451) ✓ 一致.
- 129 Crystals: 3 styles by frameX/18%3: case0 (0,0.05,0.25), case1 (0.2,0,0.15), case2 (0.1,0,0.2) — repo [0,13,64]=(0,0.051,0.251) style 0 only → 偏差(2 档缺).
- 160 Rainbow Brick: Disco×0.25 — repo v_160 no light → 缺失.
- 354: (0.65,0.35,0.15) vs repo [166,89,38]=(0.651,0.349,0.149) ✓ 一致.
- 125 Crystal Ball: G=0.3*num, B=0.6*num where num=Next(28,42)*0.01+(270-mouse)/800 ∈ [0.28+0, 0.42+0.0197] = [0.28, 0.44] → G∈[0.084,0.132], B∈[0.168,0.264]. Repo [0,27,54]=(0,0.106,0.212) static ≈ mid ✓ 近似(动态缺).
- 341 Living Demon Fire: demonTorch blend — repo missing → 缺失.
- 209: confirmed portal colors.
- 370 Meteorite Brick (0.32,0.16,0.12) — repo missing → 缺失.
- 390 Lava Lamp (0.4,0.2,0.1) — repo v_390 no light → 缺失.
- 627/628/692: Disco×0.25 — repo missing → 缺失.

Also I should double-check 597 pylon (line ~493) and 572 soul bottles, 262-268 gemspark, 61/703, 26/31/695/696, 83, 84, 350, 184, 20, 658. Let me grab those.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:24:59.729Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "f=~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs\nsed -n '493,540p;616,656p;778,930p;2962,3056p' \"$f\"",
 "description": "Verify pylon, moss plants, longmoss, clouds, cages"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:24:59.761Z

**📎 ToolResult**

```
			case 597:
				switch (tile.frameX / 54)
				{
				case 0:
					R = 0.05f;
					G = 0.8f;
					B = 0.3f;
					break;
				case 1:
					R = 0.7f;
					G = 0.8f;
					B = 0.05f;
					break;
				case 2:
					R = 0.7f;
					G = 0.5f;
					B = 0.9f;
					break;
				case 3:
					R = 0.6f;
					G = 0.6f;
					B = 0.8f;
					break;
				case 4:
					R = 0.4f;
					G = 0.4f;
					B = 1.15f;
					break;
				case 5:
					R = 0.85f;
					G = 0.45f;
					B = 0.1f;
					break;
				case 6:
					R = 0.8f;
					G = 0.8f;
					B = 1f;
					break;
				case 7:
					R = 0.5f;
					G = 0.8f;
					B = 1.2f;
					break;
				}
				R *= 0.75f;
				G *= 0.75f;
				B *= 0.75f;
				break;
			case 184:
				if (tile.frameX == 110)
				{
					R = 0.25f;
					G = 0.1f;
					B = 0f;
				}
				if (tile.frameX == 132)
				{
					R = 0f;
					G = 0.25f;
					B = 0f;
				}
				if (tile.frameX == 154)
				{
					R = 0f;
					G = 0.16f;
					B = 0.34f;
				}
				if (tile.frameX == 176)
				{
					R = 0.3f;
					G = 0f;
					B = 0.17f;
				}
				if (tile.frameX == 198)
				{
					R = 0.3f;
					G = 0f;
					B = 0.35f;
				}
				if (tile.frameX == 220)
				{
					R = (float)Main.DiscoR / 255f * 0.25f;
					G = (float)Main.DiscoG / 255f * 0.25f;
					B = (float)Main.DiscoB / 255f * 0.25f;
				}
				break;
			case 370:
				R = 0.32f;
				G = 0.16f;
			case 719:
			{
				int num15 = (x + y + (int)(Main.GlobalTimeWrappedHourly * 15f)) % 14;
				float num16 = 0f;
				float num17 = 0f;
				float num18 = 0f;
				switch (num15)
				{
				case 0:
					num16 = 255f;
					num17 = 171f;
					num18 = 183f;
					break;
				case 1:
					num16 = 255f;
					num17 = 170f;
					num18 = 220f;
					break;
				case 2:
					num16 = 252f;
					num17 = 171f;
					num18 = 255f;
					break;
				case 3:
					num16 = 224f;
					num17 = 171f;
					num18 = 255f;
					break;
				case 4:
					num16 = 192f;
					num17 = 171f;
					num18 = 255f;
					break;
				case 5:
					num16 = 174f;
					num17 = 178f;
					num18 = 255f;
					break;
				case 6:
					num16 = 168f;
					num17 = 195f;
					num18 = 255f;
					break;
				case 7:
					num16 = 167f;
					num17 = 224f;
					num18 = 255f;
					break;
				case 8:
					num16 = 168f;
					num17 = 255f;
					num18 = 252f;
					break;
				case 9:
					num16 = 162f;
					num17 = 255f;
					num18 = 233f;
					break;
				case 10:
					num16 = 158f;
					num17 = 255f;
					num18 = 198f;
					break;
				case 11:
					num16 = 207f;
					num17 = 255f;
					num18 = 173f;
					break;
				case 12:
					num16 = 255f;
					num17 = 213f;
					num18 = 186f;
					break;
				case 13:
					num16 = 255f;
					num17 = 192f;
					num18 = 182f;
					break;
				}
				R = num16 / 255f;
				G = num17 / 255f;
				B = num18 / 255f;
				break;
			}
			case 718:
				if (!Main.dayTime && !WorldGen.SolidTile3(x, y - 1))
				{
					R = localRandom.NextFloat() * 0.04f + 0.1f + (float)Main.DiscoR / 800f;
					G = localRandom.NextFloat() * 0.04f + 0.1f + (float)Main.DiscoG / 800f;
					B = localRandom.NextFloat() * 0.04f + 0.1f + (float)Main.DiscoB / 800f;
				}
				break;
			case 717:
			{
				float num13 = 0.55f;
				num13 += (float)(270 - Main.mouseTextColor) / 800f;
				num13 += localRandom.NextFloat() * 0.03f;
				num13 *= 0.5f;
				R = num13 * 1.1f;
				G = num13 * 0.4f;
				B = num13 * 0.1f;
				break;
			}
			case 429:
			{
				int num8 = tile.frameX / 18;
				bool flag2 = num8 % 2 >= 1;
				bool flag3 = num8 % 4 >= 2;
				bool flag4 = num8 % 8 >= 4;
				bool num9 = num8 % 16 >= 8;
				if (flag2)
				{
					R += 0.5f;
				}
				if (flag3)
				{
					G += 0.5f;
				}
				if (flag4)
				{
					B += 0.5f;
				}
				if (num9)
				{
					R += 0.2f;
					G += 0.2f;
				}
				break;
			}
			case 286:
			case 619:
				R = 0.1f;
				G = 0.2f;
				B = 0.7f;
				break;
			case 620:
			{
				Color color = new Color(230, 230, 230, 0).MultiplyRGBA(Main.hslToRgb(Main.GlobalTimeWrappedHourly * 0.5f % 1f, 1f, 0.5f));
				color *= 0.4f;
				R = (float)(int)color.R / 255f;
				G = (float)(int)color.G / 255f;
				B = (float)(int)color.B / 255f;
				break;
			}
			case 582:
			case 598:
				R = 0.7f;
				G = 0.2f;
				B = 0.1f;
				break;
			case 270:
				R = 0.73f;
				G = 1f;
			case 739:
				R = 0.35f;
				G = 0.63f;
				B = 0.7f;
				flag = true;
				break;
			case 350:
			{
				double num10 = Main.timeForVisualEffects * 0.08;
				B = (G = (R = (float)((0.0 - Math.Cos(((int)(num10 / 6.283) % 3 == 1) ? num10 : 0.0)) * 0.1 + 0.1)));
				break;
			}
			case 61:
			case 703:
				if (tile.frameX == 144)
				{
					float num6 = 1f + (float)(270 - Main.mouseTextColor) / 400f;
					float num7 = 0.8f - (float)(270 - Main.mouseTextColor) / 400f;
					R = 0.42f * num7;
					G = 0.81f * num6;
					B = 0.52f * num7;
				}
				break;
			case 26:
			case 31:
			case 695:
			case 696:
				if (((tile.type == 31 || tile.type == 696) && tile.frameX >= 36) || ((tile.type == 26 || tile.type == 695) && tile.frameX >= 54))
				{
					float num4 = (float)localRandom.Next(-5, 6) * 0.0025f;
					R = 0.5f + num4 * 2f;
					G = 0.2f + num4;
					B = 0.1f;
				}
				else
				{
					float num5 = (float)localRandom.Next(-5, 6) * 0.0025f;
					R = 0.31f + num5;
					G = 0.1f;
					B = 0.44f + num5 * 2f;
				}
				break;
			case 699:
				R = 0.4f;
				G = 0.2f;
				B = 0.15f;
				break;
			case 84:
			{
				int num2 = tile.frameX / 18;
				float num3 = 0f;
				switch (num2)
				{
				case 2:
					num3 = (float)(270 - Main.mouseTextColor) / 400f;
					if (num3 > 1f)
					{
						num3 = 1f;
					}
					else if (num3 < 0f)
					{
						num3 = 0f;
					}
					R = num3 * 1.4f;
					G = num3 * 1.2f;
					B = num3 / 2f;
					break;
				case 5:
					num3 = 0.9f;
					R = num3;
					G = num3 * 0.8f;
					B = num3 * 0.2f;
					break;
				case 6:
					num3 = 0.08f;
					G = num3 * 0.8f;
					B = num3;
					break;
				}
				break;
			}
			case 83:
				if (tile.frameX == 18 && !Main.dayTime)
				{
					R = 0.1f;
					G = 0.4f;
					B = 0.6f;
				}
				if (tile.frameX == 90 && !Main.raining && Main.time > 40500.0)
				{
					R = 0.9f;
					G = 0.72f;
					B = 0.18f;
				}
				break;

```


---

## 🤖 Assistant · 2026-08-13T06:25:14.036Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
More refinements:
- 597 pylon: 8 styles ×0.75, style0 = (0.05,0.8,0.3)×0.75 = (0.0375, 0.6, 0.225). Repo [13,204,77]/255 = (0.051, 0.8, 0.302) — that's the UNMULTIPLIED style 0 value. So repo = style0 without ×0.75 and without other 7 styles → 偏差(2): 缺 ×0.75 与 7 个样式.
- 184 longmoss: exact gates frameX==110/132/154/176/198/220 (not ranges!) — repo [77,0,89] static (=0.302,0,0.349 ≈ 198 violet gate) → 偏差: 5/6 档缺 + 静态化.
- 719 rainbow cloud: 14-phase color wheel with time animation (GlobalTimeWrappedHourly*15 %14) → repo missing → 缺失.
- 718 star cloud: gate `!dayTime && !SolidTile3(x,y-1)` → repo missing → 缺失.
- 717 lava cloud: num13=0.55+(270-mouse)/800+rand*0.03, ×0.5 → R=1.1n, G=0.4n, B=0.1n where n∈[0.275,0.293] → R∈[0.3025,0.322] → repo missing → 缺失.
- 429 wire bulb: `R += 0.5` (additive to current light!) — repo computes from 0 and then max-merges. Since vanilla ADDS to existing lightColor and the final is max-raise? Actually ApplyTileLight modifies R/G/B then GetTileLight does... hmm, in vanilla GetTileLight, ApplyTileLight writes to R/G/B which are the output; but there's no max — the switch assigns R directly (overwrites wall/sky light!). Wait: ApplyWallLight/ApplySurfaceLight set lightColor; then ApplyTileLight's switch assigns `R = ...` — in C#, R is a local float in ApplyTileLight? Let me check: ApplyTileLight signature has `ref Vector3 lightColor` and R/G/B are local floats initialized 0. At the end of ApplyTileLight it does lightColor.X = Math.Max(lightColor.X, R) etc. Let me confirm — that's the standard. So the switch R/G/B are separate and merged with max. In that case 429's `R += 0.5` means the switch-internal R accumulates bits (from 0) — equivalent to repo's computation. ✓ 一致.
- 286/619: (0.1,0.2,0.7) — repo missing both → 缺失.
- 620: hsl wheel ×0.4 — repo missing → 缺失.
- 582/598: (0.7,0.2,0.1) — repo v_598 [255,185,110]=(1,0.725,0.431) → 偏差; v_582 缺失.
- 270 firefly: R=0.73, G=1, B=? (cut off) — repo missing → 缺失.
- 739: (0.35,0.63,0.7) + flag(paint branch) — repo missing → 缺失.
- 350: timeForVisualEffects-based pulse (0.1-cos(...)×0.1+0.1) ∈ [0, 0.2]... repo [26,26,26]=0.102 static → 近似/偏差(动态缺失).
- 61/703: gate frameX==144; num6=1+(270-mouse)/400, num7=0.8-(270-mouse)/400 → R=0.42*num7, G=0.81*num6, B=0.52*num7. At mouse=270: num6=1, num7=0.8 → (0.336, 0.81, 0.416). Repo [107,207,133]=(0.42,0.812,0.522) — that's using num6 for... hmm repo = (0.42, 0.81, 0.52) = the un-multiplied coefficients. So repo value ≈ coefficients without num6/num7 modulation, plus gate frameX==144 missing → 偏差(2).
- 26/31/695/696: confirmed two branches.
- 699: (0.4,0.2,0.15) — repo missing → 缺失.
- 84: confirmed. Repo style2 clamp ✓, style5 [0.9,0.72,0.18] ✓ (0.9, 0.72, 0.18) ✓, style6 [0, 0.064, 0.08] = (0, 0.08*0.8, 0.08) ✓. 一致 ✓.
- 83: confirmed.

Also, 658 aether monolith (line 354): TorchColor(23) × frameY/54 tiers. Let me verify quickly + case 20 saplings + 658 + 209 already done + 572 + 262-268 + 96-99 region + 92 done. Let me check 658, 20, 572, 262-268.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:25:14.687Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "f=~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs\nsed -n '354,377p;399,409p;549,573p;922,1006p' \"$f\"",
 "description": "Verify aether monolith, saplings, soul bottles, gemspark"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:25:14.711Z

**📎 ToolResult**

```
			case 658:
				if (!tile.invisibleBlock())
				{
					TorchID.TorchColor(23, out R, out G, out B);
					switch (tile.frameY / 54)
					{
					default:
						R *= 0.2f;
						G *= 0.2f;
						B *= 0.2f;
						break;
					case 1:
						R *= 0.3f;
						G *= 0.3f;
						B *= 0.3f;
						break;
					case 2:
						R *= 0.1f;
						G *= 0.1f;
						B *= 0.1f;
						break;
					}
				}
				break;
			case 20:
			{
				int num28 = tile.frameX / 18;
				if (num28 >= 30 && num28 <= 32)
				{
					R = 0.325f;
					G = 0.15f;
					B = 0.05f;
				}
				break;
			}
			case 568:
				R = 1f;
				G = 0.61f;
				B = 0.65f;
				break;
			case 569:
				R = 0.12f;
				G = 1f;
				B = 0.66f;
				break;
			case 570:
				R = 0.57f;
				G = 0.57f;
				B = 1f;
				break;
			case 580:
				R = 0.7f;
				G = 0.3f;
				B = 0.2f;
				break;
			case 391:
				R = 0.3f;
				G = 0.1f;
				B = 0.25f;
				break;
			case 582:
			case 598:
				R = 0.7f;
				G = 0.2f;
				B = 0.1f;
				break;
			case 270:
				R = 0.73f;
				G = 1f;
				B = 0.41f;
				break;
			case 271:
				R = 0.45f;
				G = 0.95f;
				B = 1f;
				break;
			case 581:
				R = 1f;
				G = 0.75f;
				B = 0.5f;
				break;
			case 660:
				TorchID.TorchColor(23, out R, out G, out B);
				break;
			case 572:
				switch (tile.frameY / 36)
				{
				case 0:
					R = 0.9f;
					G = 0.5f;
					B = 0.7f;
					break;
				case 1:
					R = 0.7f;
					G = 0.55f;
					B = 0.96f;
					break;
				case 2:
					R = 0.45f;
					G = 0.96f;
					B = 0.95f;
					break;
				case 3:
					R = 0.5f;
					G = 0.96f;
					B = 0.62f;
					break;
				case 4:
					R = 0.47f;
					G = 0.69f;
					B = 0.95f;
					break;
				case 5:
					R = 0.92f;
					G = 0.57f;
					B = 0.51f;
					break;
				}
				break;
			case 262:
				R = 0.75f;
				B = 0.75f;
				break;
			case 263:
				R = 0.75f;
				G = 0.75f;
				break;
			case 264:
				B = 0.75f;
				break;
			case 265:
				G = 0.75f;
				break;
			case 266:
				R = 0.75f;
				break;
			case 267:
				R = 0.75f;
				G = 0.75f;
				B = 0.75f;
				break;
			case 268:
				R = 0.75f;
				G = 0.375f;
				break;

```


---

## 🤖 Assistant · 2026-08-13T06:25:17.934Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All confirmed. Now for section 2 (WALL_EMISSIVE), section 3 (TORCH_COLORS), section 4 (liquids), section 5 (WALL_LIGHT) — I have all data from summary. Let me do one final verification of lightTables.ts contents to have exact repo line numbers for each WALL_EMISSIVE entry (21 entries) and TORCH_COLORS (24) and WALL_LIGHT (15), since the report needs 本仓文件:行号. Let me read lightTables.ts fully (118 lines).
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:25:18.140Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/lighting/lightTables.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:25:18.142Z

**📎 ToolResult**

```
Wasted call — file unchanged since your last Read. Refer to that earlier tool_result instead.

```


---

## 🤖 Assistant · 2026-08-13T06:25:20.684Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The system says the file is unchanged since last read — but my context after compaction doesn't include the literal content. I have the summary's line references: TORCH_COLORS(:60-85), FLICKER_SHEETS(:87), MUSHROOM_GLOW_SHEETS(:90), WALL_EMISSIVE(:93-115), WALL_LIGHT(:57), MOON_FLOOR(:?).

I need exact per-entry line numbers for WALL_EMISSIVE 21 entries and TORCH_COLORS 24 entries. Let me grep with line numbers (grep is allowed).
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:25:21.117Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"\" ~/Project/GLM/SandboxWorld/game/src/lighting/lightTables.ts | sed -n '55,118p'",
 "description": "Dump lightTables lines 55-118 with numbers"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:25:21.148Z

**📎 ToolResult**

```
55:export const CRACKED_SHEETS = new Set([481, 482, 483]);
56:/** 透光墙(Main.cs:10487-10503 wallLight 全表)——天空光可穿过的墙(0=无墙含在内由调用方处理) */
57:export const WALL_LIGHT = new Set([21, 318, 106, 317, 107, 138, 140, 141, 139, 145, 150, 152, 245, 315, 168]);
58:
59:// ---- 火把色(TorchID.cs:134-161 _lights 全表;0-1 RGB) ----
60:export const TORCH_COLORS: ReadonlyArray<readonly [number, number, number]> = [
61:  [1, 0.95, 0.8],      // 0 火把
62:  [0, 0.1, 1.3],       // 1 蓝
63:  [1, 0.1, 0.1],       // 2 红
64:  [0, 1, 0.1],         // 3 绿
65:  [0.9, 0, 0.9],       // 4 紫
66:  [1.4, 1.4, 1.4],     // 5 白
67:  [0.9, 0.9, 0],       // 6 黄
68:  [1, 0.3, 0.5],       // 7 恶魔(动态,见 SkyColor.demonTorch 插值)
69:  [1, 1.6, 0.5],       // 8 诅咒
70:  [0.75, 0.85, 1.4],   // 9 冰
71:  [1, 0.5, 0],         // 10 橙
72:  [1.4, 1.4, 0.7],     // 11 圣液
73:  [0.75, 1.35, 1.5],   // 12 超亮
74:  [0.95, 0.75, 1.3],   // 13 骨头
75:  [1, 1, 1],           // 14 彩虹(动态,见 SkyColor.disco)
76:  [1, 0, 1],           // 15 粉
77:  [1.4, 0.85, 0.55],   // 16 沙漠
78:  [0.25, 1.3, 0.8],    // 17 珊瑚
79:  [0.95, 0.4, 1.4],    // 18 腐化
80:  [1.4, 0.7, 0.5],     // 19 猩红
81:  [1.25, 0.6, 1.2],    // 20 神圣
82:  [0.75, 1.45, 0.9],   // 21 丛林
83:  [0.3, 0.78, 1.2],    // 22 蘑菇
84:  [1, 1, 1],           // 23 微光(动态,见 SkyColor)
85:];
86:/** 蜡烛/吊灯/篝火等闪烁幅度来源的 sheet 集(燃烧类光源) */
87:export const FLICKER_SHEETS = new Set([33, 49, 92, 93, 174, 34, 149, 95, 100, 126, 173, 564, 215, 405, 4]);
88:/** 蘑菇组发光 sheet(TileLightScanner.cs:2938 case 70/71/72/190/348/349/528/578；
89: *  R=0 B=1 G=0.2+num11/2 的呼吸蓝光,与 FLICKER_SHEETS 三通道叠加不同) */
90:export const MUSHROOM_GLOW_SHEETS = new Set([70, 71, 72, 190, 348, 349, 528, 578]);
91:
92:// ---- 发光墙(ApplyWallLight:167-342 精选;[wallId] → RGB) ----
93:export const WALL_EMISSIVE: Record<number, readonly [number, number, number]> = {
94:  33: [0.09, 0.0525, 0.24],     // 恶魔砖墙
95:  44: [0.15, 0.15, 0.15],       // 彩虹砖(静态近似;动态 disco 见 phase2)
96:  137: [0.5, 0.25, 0.05],       // 岩浆瀑布墙
97:  153: [0.6, 0.12, 0.6],        // 紫水晶宝石灯墙
98:  154: [0.6, 0.12, 0.6],
99:  155: [0.6, 0.42, 0.06],       // 琥珀
100:  156: [0.09, 0.6, 0.24],       // 祖母绿
101:  164: [0.09, 0.24, 0.6],       // 蓝宝石
102:  165: [0.6, 0.06, 0.09],       // 红宝石
103:  166: [0.42, 0.42, 0.6],       // 钻石
104:  174: [0.2975, 0, 0],          // 猩红砖墙(仅 R)
105:  175: [0.075, 0.15, 0.4],      // 蘑菇护板
106:  176: [0.1, 0.1, 0.1],         // 火星导管
107:  182: [0.24, 0.12, 0.09],      // 陨石砖墙
108:  341: [0.25, 0.1, 0],          // 熔岩苔墙
109:  342: [0, 0.25, 0],
110:  343: [0.3, 0, 0.17],
111:  344: [0, 0.16, 0.34],
112:  345: [0.3, 0, 0.35],
113:  346: [0.25, 0.25, 0.25],      // 彩虹苔砖墙(静态近似)
114:  357: [0.15, 0.27, 0.3],       // 水母墙
115:};
116:
117:// ---- 月相地板(Main.cs:63230-63266;索引 = dayCount%8,相位序 Empty→Full→Empty) ----
118:export const MOON_FLOOR = [11, 13, 15, 17, 19, 17, 15, 13];

```


---

## 🤖 Assistant · 2026-08-13T06:25:23.138Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have exact line numbers for all repo tables. Let me now cross-check the vanilla ApplyWallLight values against these, one final time, since section 2 is the "全表对账". Let me dump vanilla ApplyWallLight :167-342 values with line numbers.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:25:23.548Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "f=~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs\ngrep -n \"\" \"$f\" | sed -n '167,342p'",
 "description": "Dump ApplyWallLight with line numbers"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:25:23.574Z

**📎 ToolResult**

```
167:	private void ApplyWallLight(Tile tile, int x, int y, ref FastRandom localRandom, ref Vector3 lightColor)
168:	{
169:		float num = 0f;
170:		float num2 = 0f;
171:		float num3 = 0f;
172:		bool flag = false;
173:		switch (tile.wall)
174:		{
175:		case 357:
176:			if (!LightIsBlocked(tile))
177:			{
178:				num = 0.15f;
179:				num2 = 0.27f;
180:				num3 = 0.3f;
181:				flag = true;
182:			}
183:			break;
184:		case 182:
185:			if (!LightIsBlocked(tile))
186:			{
187:				num = 0.24f;
188:				num2 = 0.12f;
189:				num3 = 0.089999996f;
190:			}
191:			break;
192:		case 33:
193:			if (!LightIsBlocked(tile))
194:			{
195:				num = 0.089999996f;
196:				num2 = 0.052500002f;
197:				num3 = 0.24f;
198:			}
199:			break;
200:		case 174:
201:			if (!LightIsBlocked(tile))
202:			{
203:				num = 0.2975f;
204:			}
205:			break;
206:		case 175:
207:			if (!LightIsBlocked(tile))
208:			{
209:				if (tile.wallColor() == 0)
210:				{
211:					num = 0.075f;
212:					num2 = 0.15f;
213:					num3 = 0.4f;
214:				}
215:				else
216:				{
217:					flag = true;
218:				}
219:			}
220:			break;
221:		case 176:
222:			if (!LightIsBlocked(tile))
223:			{
224:				num = 0.1f;
225:				num2 = 0.1f;
226:				num3 = 0.1f;
227:			}
228:			break;
229:		case 137:
230:			if (!LightIsBlocked(tile))
231:			{
232:				float num4 = 0.4f;
233:				num4 += (float)(270 - Main.mouseTextColor) / 1500f;
234:				num4 += (float)localRandom.Next(0, 50) * 0.0005f;
235:				num = 1f * num4;
236:				num2 = 0.5f * num4;
237:				num3 = 0.1f * num4;
238:			}
239:			break;
240:		case 44:
241:			if (!LightIsBlocked(tile))
242:			{
243:				num = (float)Main.DiscoR / 255f * 0.15f;
244:				num2 = (float)Main.DiscoG / 255f * 0.15f;
245:				num3 = (float)Main.DiscoB / 255f * 0.15f;
246:			}
247:			break;
248:		case 154:
249:			num = 0.6f;
250:			num3 = 0.6f;
251:			break;
252:		case 166:
253:			num = 0.6f;
254:			num2 = 0.6f;
255:			break;
256:		case 165:
257:			num3 = 0.6f;
258:			break;
259:		case 156:
260:			num2 = 0.6f;
261:			break;
262:		case 164:
263:			num = 0.6f;
264:			break;
265:		case 155:
266:			num = 0.6f;
267:			num2 = 0.6f;
268:			num3 = 0.6f;
269:			break;
270:		case 153:
271:			num = 0.6f;
272:			num2 = 0.3f;
273:			break;
274:		case 341:
275:			if (!LightIsBlocked(tile))
276:			{
277:				num = 0.25f;
278:				num2 = 0.1f;
279:				num3 = 0f;
280:			}
281:			break;
282:		case 343:
283:			if (!LightIsBlocked(tile))
284:			{
285:				num = 0f;
286:				num2 = 0.25f;
287:				num3 = 0f;
288:			}
289:			break;
290:		case 344:
291:			if (!LightIsBlocked(tile))
292:			{
293:				num = 0f;
294:				num2 = 0.16f;
295:				num3 = 0.34f;
296:			}
297:			break;
298:		case 342:
299:			if (!LightIsBlocked(tile))
300:			{
301:				num = 0.3f;
302:				num2 = 0f;
303:				num3 = 0.17f;
304:			}
305:			break;
306:		case 345:
307:			if (!LightIsBlocked(tile))
308:			{
309:				num = 0.3f;
310:				num2 = 0f;
311:				num3 = 0.35f;
312:			}
313:			break;
314:		case 346:
315:			if (!LightIsBlocked(tile))
316:			{
317:				num = (float)Main.DiscoR / 255f * 0.25f;
318:				num2 = (float)Main.DiscoG / 255f * 0.25f;
319:				num3 = (float)Main.DiscoB / 255f * 0.25f;
320:			}
321:			break;
322:		}
323:		if (flag && tile.wallColor() != 0)
324:		{
325:			Color color = WorldGen.paintColor(tile.wallColor());
326:			num = (float)(int)color.R / 765f;
327:			num2 = (float)(int)color.G / 765f;
328:			num3 = (float)(int)color.B / 765f;
329:		}
330:		if (lightColor.X < num)
331:		{
332:			lightColor.X = num;
333:		}
334:		if (lightColor.Y < num2)
335:		{
336:			lightColor.Y = num2;
337:		}
338:		if (lightColor.Z < num3)
339:		{
340:			lightColor.Z = num3;
341:		}
342:	}

```


---

## 🤖 Assistant · 2026-08-13T06:25:36.698Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Perfect — ApplyWallLight fully confirmed with line numbers. Vanilla has 21 wall cases: 357, 182, 33, 174, 175, 176, 137, 44, 154, 166, 165, 156, 164, 155, 153, 341, 343, 344, 342, 345, 346.

Repo WALL_EMISSIVE has 21 keys: 33, 44, 137, 153, 154, 155, 156, 164, 165, 166, 174, 175, 176, 182, 341, 342, 343, 344, 345, 346, 357 → all 21 present ✓.

Now the gem wall mapping (vanilla wall id → gem):
- 153 = AmberGemspark → R=0.6, G=0.3, B=0 (unset=0)
- 154 = AmethystGemspark → R=0.6, B=0.6 (G=0)
- 155 = DiamondGemspark → R=G=B=0.6
- 156 = EmeraldGemspark → G=0.6
- 164 = RubyGemspark → R=0.6
- 165 = SapphireGemspark → B=0.6
- 166 = TopazGemspark → R=0.6, G=0.6

Repo:
- 153: [0.6, 0.12, 0.6] labeled 紫水晶 — wrong: should be (0.6,0.3,0) amber. 偏差(3 通道全错)
- 154: [0.6, 0.12, 0.6] — should be (0.6, 0, 0.6) → G off by 0.12 偏差(1)
- 155: [0.6, 0.42, 0.06] — should be (0.6,0.6,0.6) → G/B wrong 偏差(2)
- 156: [0.09, 0.6, 0.24] — should be (0,0.6,0) → R/B wrong 偏差(2)
- 164: [0.09, 0.24, 0.6] — should be (0.6,0,0) → all wrong 偏差(3)
- 165: [0.6, 0.06, 0.09] — should be (0,0,0.6) → all wrong 偏差(3)
- 166: [0.42, 0.42, 0.6] — should be (0.6,0.6,0) → B wrong 偏差(1)

Also comments mislabeled (153 labeled 紫水晶, 155 琥珀, 156 祖母绿, 164 蓝宝石, 165 红宝石, 166 钻石) — the id→gem comment mapping is shuffled, which explains the wrong values (values appear shifted by one).

Rest:
- 357: vanilla (0.15,0.27,0.3) + paint flag → repo [0.15,0.27,0.3] ✓ 值一致, paint 分支缺失
- 182: (0.24,0.12,0.09) → repo ✓ 一致
- 33: (0.09,0.0525,0.24) → repo ✓ 一致
- 174: (0.2975,0,0) → repo ✓ 一致
- 175: wallColor==0 → (0.075,0.15,0.4); else paint → repo [0.075,0.15,0.4] 基础值 ✓, paint 分支缺失
- 176: (0.1,0.1,0.1) → repo ✓ 一致
- 137: num4=0.4+(270-mouse)/1500+Next(0,50)*0.0005 → (num4, 0.5num4, 0.1num4); mouse∈[190,255] → (270-mouse)/1500 ∈ [0.01, 0.0533]; num4 ∈ [0.41+rand*0.0005, 0.4533+0.0245] → R≈[0.41,0.478] → repo [0.5,0.25,0.05] ≈ mid 基值 (0.4+0.1) 近似 → 偏差(动态项缺, 靺态值略高)
- 44: Disco×0.15 → repo [0.15,0.15,0.15] 静态近似 偏差(动态缺)
- 341: (0.25,0.1,0) ✓
- 342: (0.3,0,0.17) ✓
- 343: (0,0.25,0) ✓
- 344: (0,0.16,0.34) ✓
- 345: (0.3,0,0.35) ✓
- 346: Disco×0.25 → repo [0.25,0.25,0.25] 静态近似 偏差(动态缺)

Structural: vanilla 153-166 seven gem cases have NO !LightIsBlocked gate (emit even behind solid blocks); repo gates all with `st.type[i]===0` → 偏差 (gem walls behind blocks don't emit). Also repo's gate is stricter than LightIsBlocked for all walls (platform/torch in front → vanilla still emits).

Also the paint override :323-329 missing for all flagged cases (357, 175).

Now section 3 TORCH_COLORS. Let me verify the vanilla TorchID._lights values exactly once more (lines 134-161) with line numbers.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:25:37.098Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TorchID.cs | sed -n '100,165p'",
 "description": "Dump TorchID lights table with line numbers"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:25:37.131Z

**📎 ToolResult**

```
100:	public const short Cursed = 8;
101:
102:	public const short Ice = 9;
103:
104:	public const short Orange = 10;
105:
106:	public const short Ichor = 11;
107:
108:	public const short UltraBright = 12;
109:
110:	public const short Bone = 13;
111:
112:	public const short Rainbow = 14;
113:
114:	public const short Pink = 15;
115:
116:	public const short Desert = 16;
117:
118:	public const short Coral = 17;
119:
120:	public const short Corrupt = 18;
121:
122:	public const short Crimson = 19;
123:
124:	public const short Hallowed = 20;
125:
126:	public const short Jungle = 21;
127:
128:	public const short Mushroom = 22;
129:
130:	public const short Shimmer = 23;
131:
132:	public static readonly short Count = 24;
133:
134:	public static void Initialize()
135:	{
136:		ITorchLightProvider[] array = new ITorchLightProvider[Count];
137:		array[0] = new ConstantTorchLight(1f, 0.95f, 0.8f);
138:		array[1] = new ConstantTorchLight(0f, 0.1f, 1.3f);
139:		array[2] = new ConstantTorchLight(1f, 0.1f, 0.1f);
140:		array[3] = new ConstantTorchLight(0f, 1f, 0.1f);
141:		array[4] = new ConstantTorchLight(0.9f, 0f, 0.9f);
142:		array[5] = new ConstantTorchLight(1.4f, 1.4f, 1.4f);
143:		array[6] = new ConstantTorchLight(0.9f, 0.9f, 0f);
144:		array[7] = default(DemonTorchLight);
145:		array[8] = new ConstantTorchLight(1f, 1.6f, 0.5f);
146:		array[9] = new ConstantTorchLight(0.75f, 0.85f, 1.4f);
147:		array[10] = new ConstantTorchLight(1f, 0.5f, 0f);
148:		array[11] = new ConstantTorchLight(1.4f, 1.4f, 0.7f);
149:		array[12] = new ConstantTorchLight(0.75f, 1.3499999f, 1.5f);
150:		array[13] = new ConstantTorchLight(0.95f, 0.75f, 1.3f);
151:		array[14] = default(DiscoTorchLight);
152:		array[15] = new ConstantTorchLight(1f, 0f, 1f);
153:		array[16] = new ConstantTorchLight(1.4f, 0.85f, 0.55f);
154:		array[17] = new ConstantTorchLight(0.25f, 1.3f, 0.8f);
155:		array[18] = new ConstantTorchLight(0.95f, 0.4f, 1.4f);
156:		array[19] = new ConstantTorchLight(1.4f, 0.7f, 0.5f);
157:		array[20] = new ConstantTorchLight(1.25f, 0.6f, 1.2f);
158:		array[21] = new ConstantTorchLight(0.75f, 1.45f, 0.9f);
159:		array[22] = new ConstantTorchLight(0.3f, 0.78f, 1.2f);
160:		array[23] = default(ShimmerTorchLight);
161:		_lights = array;
162:	}
163:
164:	public static void TorchColor(int torchID, out float R, out float G, out float B)
165:	{

```


---

## 🤖 Assistant · 2026-08-13T06:25:38.591Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed all 24 entries. Now verify the ShimmerTorchLight exact formula to quote precisely for the report.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:25:39.275Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"class ShimmerTorchLight\" -A 40 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TorchID.cs | head -50; grep -n \"class DemonTorchLight\" -A 20 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TorchID.cs | head -24",
 "description": "Read ShimmerTorchLight and DemonTorchLight formulas"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:25:39.309Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-13T06:25:40.964Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"ShimmerTorchLight\\|DemonTorchLight\\|DiscoTorchLight\" ~/Project/GLM/SandboxWorld/Terarria1456 --include=*.cs -l",
 "description": "Find torch light provider class files"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:25:40.983Z

**📎 ToolResult**

```
(eval):1: no matches found: --include=*.cs

```


---

## 🤖 Assistant · 2026-08-13T06:25:42.650Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"struct ShimmerTorchLight\" ~/Project/GLM/SandboxWorld/Terarria1456 | head -3",
 "description": "Locate ShimmerTorchLight struct"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:25:42.723Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TorchID.cs:48:	private struct ShimmerTorchLight : ITorchLightProvider

```


---

## 🤖 Assistant · 2026-08-13T06:25:50.166Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TorchID.cs",
 "limit": 54,
 "offset": 20
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:25:50.179Z

**📎 ToolResult**

```
20		private struct ConstantTorchLight(float Red, float Green, float Blue) : ITorchLightProvider
21		{
22			public float R = Red;
23	
24			public float G = Green;
25	
26			public float B = Blue;
27	
28			public void GetRGB(out float r, out float g, out float b)
29			{
30				r = R;
31				g = G;
32				b = B;
33			}
34		}
35	
36		[StructLayout(LayoutKind.Sequential, Size = 1)]
37		private struct DemonTorchLight : ITorchLightProvider
38		{
39			public void GetRGB(out float r, out float g, out float b)
40			{
41				r = 0.5f * Main.demonTorch + (1f - Main.demonTorch);
42				g = 0.3f;
43				b = Main.demonTorch + 0.5f * (1f - Main.demonTorch);
44			}
45		}
46	
47		[StructLayout(LayoutKind.Sequential, Size = 1)]
48		private struct ShimmerTorchLight : ITorchLightProvider
49		{
50			public void GetRGB(out float r, out float g, out float b)
51			{
52				float num = 0.9f;
53				float num2 = 0.9f;
54				num += (float)(270 - Main.mouseTextColor) / 900f;
55				num2 += (float)(270 - Main.mouseTextColor) / 125f;
56				num = MathHelper.Clamp(num, 0f, 1f);
57				num2 = MathHelper.Clamp(num2, 0f, 1f);
58				r = num * 0.9f;
59				g = num2 * 0.55f;
60				b = num * 1.2f;
61			}
62		}
63	
64		[StructLayout(LayoutKind.Sequential, Size = 1)]
65		private struct DiscoTorchLight : ITorchLightProvider
66		{
67			public void GetRGB(out float r, out float g, out float b)
68			{
69				r = (float)Main.DiscoR / 255f;
70				g = (float)Main.DiscoG / 255f;
71				b = (float)Main.DiscoB / 255f;
72			}
73		}

```


---

## 🤖 Assistant · 2026-08-13T06:25:54.818Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
ShimmerTorchLight exact:
- num = clamp(0.9 + (270-mouse)/900, 0, 1); mouse∈[190,255] → (270-mouse)∈[15,80] → num = clamp(0.9+[0.0167,0.0889]) = [0.917, 0.989] (never clamps) → r = num*0.9 ∈ [0.825, 0.890], b = num*1.2 ∈ [1.100, 1.187]
- num2 = clamp(0.9 + (270-mouse)/125, 0, 1) = clamp(0.9+[0.12,0.64]) = [1.02,1.54] → clamps to 1 always → g = 1*0.55 = 0.55 constant

So shimmer torch: r∈[0.825,0.890], g=0.550, b∈[1.100,1.187] — slight R/B breathing driven by mouseTextColor, G fixed.

Repo SkyColor.shimmerTorchColor (per summary): uses (mouse-190)/65 → num 0..1, returns [num*0.9, num2*0.55, num*1.2] with num2=1-num → r∈[0,0.9], g∈[0,0.55], b∈[0,1.2] — full-range swing, G inverted. 偏差(3 通道公式全错).

Let me verify the repo SkyColor code to quote exact lines.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:25:55.023Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"\" ~/Project/GLM/SandboxWorld/game/src/lighting/SkyColor.ts | sed -n '90,152p'",
 "description": "Dump SkyColor FlickerClock dynamic colors"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:25:55.051Z

**📎 ToolResult**

```
90:// 四态全部封装在一个小状态机里,等价原版 Main.CursorColor(51896-51905)+
91:// DoUpdate_AnimateCursorColors(18064-18076)/DoUpdate_AnimateTileGlows(18087-18101)/
92:// DoUpdate_AnimateDiscoRGB(19442-19502)。
93:export class FlickerClock {
94:  /** mouseTextColor:190↔255 步进 1/帧(字节环绕) */
95:  mouseTextColor = 255;
96:  private mouseDir = -1;
97:  /** cursorAlpha(Main.cs:51897-51904):0.6↔1 步进 0.015/帧,驱动光标/心/星呼吸 */
98:  cursorAlpha = 1;
99:  private cursorDir = -1;
100:  /** demonTorch:0↔1 步进 0.01/帧 */
101:  demonTorch = 0;
102:  private demonDir = 1;
103:  /** Disco RGB:6 相循环,每通道步进 7/帧(0-255) */
104:  discoR = 255; discoG = 0; discoB = 0;
105:  private discoStyle = 0;
106:
107:  /** cursorScale(Main.cs:51905):= cursorAlpha*0.3 + 0.8,资源条 flag 心/星缩放脉冲源 */
108:  get cursorScale(): number { return this.cursorAlpha * 0.3 + 0.8; }
109:
110:  tick(): void {
111:    this.cursorAlpha += this.cursorDir * 0.015;
112:    if (this.cursorAlpha >= 1) { this.cursorAlpha = 1; this.cursorDir = -1; }
113:    else if (this.cursorAlpha <= 0.6) { this.cursorAlpha = 0.6; this.cursorDir = 1; }
114:
115:    this.mouseTextColor += this.mouseDir;
116:    if (this.mouseTextColor >= 255) this.mouseDir = -1;
117:    else if (this.mouseTextColor <= 190) this.mouseDir = 1;
118:
119:    this.demonTorch += this.demonDir * 0.01;
120:    if (this.demonTorch > 1) { this.demonTorch = 1; this.demonDir = -1; }
121:    else if (this.demonTorch < 0) { this.demonTorch = 0; this.demonDir = 1; }
122:
123:    // 6 相:G↑ → R↓ → B↑ → G↓ → R↑ → B↓(每帧步进 7,满额切换下一相)
124:    const STEP = 7;
125:    switch (this.discoStyle) {
126:      case 0: this.discoG += STEP; if (this.discoG >= 255) { this.discoG = 255; this.discoStyle = 1; } break;
127:      case 1: this.discoR -= STEP; if (this.discoR <= 0) { this.discoR = 0; this.discoStyle = 2; } break;
128:      case 2: this.discoB += STEP; if (this.discoB >= 255) { this.discoB = 255; this.discoStyle = 3; } break;
129:      case 3: this.discoG -= STEP; if (this.discoG <= 0) { this.discoG = 0; this.discoStyle = 4; } break;
130:      case 4: this.discoR += STEP; if (this.discoR >= 255) { this.discoR = 255; this.discoStyle = 5; } break;
131:      case 5: this.discoB -= STEP; if (this.discoB <= 0) { this.discoB = 0; this.discoStyle = 0; } break;
132:    }
133:  }
134:
135:  /** 恶魔火把色插值(TorchID DemonTorchLight:37-45) */
136:  demonTorchColor(): [number, number, number] {
137:    const d = this.demonTorch;
138:    return [0.5 * d + 1 * (1 - d), 0.3, 1 * d + 0.5 * (1 - d)];
139:  }
140:
141:  /** 微光火把色(TorchID ShimmerTorchLight:48-62;num/num2 由 mouseTextColor 派生钳 0-1) */
142:  shimmerTorchColor(): [number, number, number] {
143:    const num = Math.min(1, Math.max(0, (this.mouseTextColor - 190) / 65));
144:    const num2 = 1 - num;
145:    return [num * 0.9, num2 * 0.55, num * 1.2];
146:  }
147:
148:  discoColor(): [number, number, number] {
149:    return [this.discoR / 255, this.discoG / 255, this.discoB / 255];
150:  }
151:}

```


---

## 🤖 Assistant · 2026-08-13T06:25:57.320Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed repo shimmerTorchColor lines 142-146.

Now let me verify section 4 (liquids) with exact vanilla line numbers (ApplyLiquidLight :110-152) and confirm there's no shimmer branch in repo.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:25:57.640Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs | sed -n '110,153p'",
 "description": "Dump ApplyLiquidLight with line numbers"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:25:57.667Z

**📎 ToolResult**

```
110:	private void ApplyLiquidLight(Tile tile, ref Vector3 lightColor)
111:	{
112:		if (tile.liquid <= 0)
113:		{
114:			return;
115:		}
116:		if (tile.lava())
117:		{
118:			float num = 0.55f;
119:			num += (float)(270 - Main.mouseTextColor) / 900f;
120:			if (lightColor.X < num)
121:			{
122:				lightColor.X = num;
123:			}
124:			if (lightColor.Y < num)
125:			{
126:				lightColor.Y = num * 0.6f;
127:			}
128:			if (lightColor.Z < num)
129:			{
130:				lightColor.Z = num * 0.2f;
131:			}
132:		}
133:		else if (tile.shimmer())
134:		{
135:			float num2 = 0.7f;
136:			float num3 = 0.7f;
137:			num2 += (float)(270 - Main.mouseTextColor) / 900f;
138:			num3 += (float)(270 - Main.mouseTextColor) / 125f;
139:			if (lightColor.X < num2)
140:			{
141:				lightColor.X = num2 * 0.6f;
142:			}
143:			if (lightColor.Y < num3)
144:			{
145:				lightColor.Y = num3 * 0.25f;
146:			}
147:			if (lightColor.Z < num2)
148:			{
149:				lightColor.Z = num2 * 0.9f;
150:			}
151:		}
152:	}
153:

```


---

## 🤖 Assistant · 2026-08-13T06:26:06.085Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Note an important subtlety in vanilla lava light: 
```
if (lightColor.X < num) lightColor.X = num;
if (lightColor.Y < num) lightColor.Y = num*0.6;
```
The Y check is against `num` (not num*0.6) but sets Y to num*0.6. So if Y is between num*0.6 and num, it gets LOWERED to num*0.6! E.g. sky light Y=0.8 > num*0.6 but < num → set to num*0.6 (dimmer!). Interesting quirk. Similarly Z. The repo does `lg = Math.max(lg, lavaV*0.6)` — never lowers. So on the surface, a lava tile in daylight: vanilla R=1 (sky R may exceed num → stays), Y: sky Y (e.g. 1.0 daylight?) — daylight sky light values... At noon sky is (1,1,1)? Then Y=1 > num → not lowered. At dusk sky maybe (0.6,0.3,0.4): Y=0.3, num≈0.62 → 0.3<num → set to 0.372 (raised). Edge case where Y∈(0.372, 0.62): vanilla lowers, repo keeps. This is a real behavioral difference worth a footnote in section 4 (判定: 偏差(1) — 合成语义近似 max-raise, 原版 Y/Z 用 num 作阈值会下调既有光).

Same for shimmer: `if (lightColor.Y < num3) lightColor.Y = num3*0.25` where num3 ≈ 0.82..1.54 clamped? no clamp here — num3 = 0.7+(270-mouse)/125 ∈ [0.82, 1.34]. num2 = 0.7+(270-mouse)/900 ∈ [0.717, 0.789]. So X=num2*0.6∈[0.430,0.473], Y=num3*0.25∈[0.205,0.335], Z=num2*0.9∈[0.645,0.710].

Repo: no shimmer branch at all → 缺失.

Also for section 4, repo lava: `if (st.liquid[i] > 0 && st.liquidType[i] === 2)` — vanilla gate `tile.liquid <= 0 return` + `tile.lava()`. Equivalent (liquidType 2 = lava in repo encoding). ✓

Now section 5 WALL_LIGHT. Vanilla Main.cs:10487-10503. Let me verify exact lines.
````

</details>


---

## 🤖 Assistant · 2026-08-13T06:26:06.438Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | sed -n '10484,10506p'",
 "description": "Dump vanilla wallLight table"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:26:06.475Z

**📎 ToolResult**

```
10484:		wallHouse[309] = true;
10485:		wallHouse[310] = true;
10486:		wallHouse[311] = true;
10487:		wallLight[0] = true;
10488:		wallLight[21] = true;
10489:		wallLight[318] = true;
10490:		wallLight[106] = true;
10491:		wallLight[317] = true;
10492:		wallLight[107] = true;
10493:		wallLight[138] = true;
10494:		wallLight[140] = true;
10495:		wallLight[141] = true;
10496:		wallLight[139] = true;
10497:		wallLight[145] = true;
10498:		wallLight[150] = true;
10499:		wallLight[152] = true;
10500:		wallLight[245] = true;
10501:		wallLight[315] = true;
10502:		wallLight[168] = true;
10503:		for (int num5 = 0; num5 < WallID.Count; num5++)
10504:		{
10505:			wallDungeon[num5] = false;
10506:		}

```


---

## 🤖 Assistant · 2026-08-13T06:26:26.998Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Section 5 fully confirmed: 16 entries (0 + 15). Repo has 15 (0 handled by `wall === 0` in exposed()). ✓ 全表一致.

Additionally, note: vanilla ApplySurfaceLight/ApplyHellLight also accept `tile.wall == 73 || tile.wall == 227` (cloud / snowfall walls) beyond wallLight — repo missing those two → 偏差(2 缺).

Also `tile.invisibleWall() && !_drawInvisibleWalls` (echo-coated wall transmits sky light) — repo missing → minor.

I now have everything verified with exact line numbers on both sides. Time to write the final five-section report.

Let me structure it. It will be long but must be organized. Format per entry: [原版行号+值, 本仓文件:行号+值, 判定]. Values to 3 decimals.

Section 1: 静态 tile 光源覆盖率 — I'll enumerate all vanilla ApplyTileLight cases in switch order, grouped logically, with repo refs. I need repo line numbers for each def.light — I have them from the tiles.ts read (lines given in the file dump above). Let me map:
- torch: tiles.ts:61 [255,225,150] — wait, torch def light [255,225,150]?? Line 61: `def({ key: 'torch', ... light: [255, 225, 150] ...})` and comment line 62 "注：火把光值见下（更亮版本）". Hmm the scanner uses TORCH_COLORS for sheet 4, not def.light. So def.light is unused for torch. Fine.
- furnace: :64 [255,140,70]
- crystal_heart: :140 [255,60,90] (sheet 12 — EXTRA, vanilla tileLighted[12] false)
- candle: :142 [255,185,110]
- chandelier: :143 [255,190,120]
- lantern: :144 no light (specialTileLight case 42)
- candelabra: :146 [255,185,110]
- chinese_lantern: :147 [255,160,70]
- skull_lantern: :148 [255,160,70]
- water_candle: :149 [140,180,255]
- v_463: :155 [51,102,204]
- ore_demonite: :86 [255,255,153]
- ore_meteorite: :87 [143,110,38]
- ore_hellstone: :88 [255,90,40] (sheet 58 — vanilla tileLighted true but no case → EXTRA)
- ore_crimtane: :89 [89,0,0]
- v_633: :178 [83,38,13]
- v_536: :182 [0,41,87]
- v_381: :190 [255,120,30]
- v_190: :207 [0,51,255]
- v_350: :208 [26,26,26]
- v_184: :234 [77,0,89]
- v_637: :247 [83,38,13]
- v_519: :250 [26,51,179]
- v_634: :252 [166,77,26]
- v_26: :254 [79,26,112]
- v_93: :261 [255,185,110]
- v_215: :280 [255,185,110]
- v_597: :282 [13,204,77]
- v_592: :283 [255,185,110]
- v_354: :298 [166,89,38]
- v_349: :302 [0,51,255]
- v_613: :304 [179,77,51]
- v_129: :308 [0,13,64]
- v_302: :321 [212,153,128]
- v_491: :324 [128,102,179]
- v_548: :315 [179,77,51]
- v_614: :316 [179,77,51]
- v_598: :317 [255,185,110]
- v_405: :331 [255,185,110]
- v_356: :334 [115,64,0]
- v_237: :336 [26,26,0]
- v_316: :340 [102,26,64]
- v_125: :341 [0,27,54]
- v_656: :348 [255,185,110]
- v_638: :354 [83,38,13]
- v_528: :355 [0,51,255]
- v_578: :368 [0,51,255]
- v_625: :376 [77,0,89]
- v_539: :393 [77,0,43]
- v_340: :385 [115,255,115]
- v_711: :401 [3,3,3]
- v_31: :408 [79,26,112]
- v_27: :420 [255,242,166]
- v_70: :413 [0,51,255]
- v_71: :417 [0,51,255]
- v_61: :431 [107,207,133]
- v_83: :433 [230,184,46]
- v_72: :435 [0,51,255]
- v_348: :612 [0,51,255]
- v_35: :443 [179,153,230]
- v_92: :444 [255,255,255]
- v_126: :445 (no light; specialTileLight)
- v_149: :450 [26,51,128]
- v_173: :451 [255,242,166]
- v_174: :452 [255,242,166]
- v_209: :453 (specialTileLight)
- v_372: :474 [230,26,191]
- v_564: :500 [13,77,140]
- v_593: :502 [204,77,26]
- v_594: :503 [204,77,26]
- v_77: :510 [255,140,70]
- v_133: :529 (no light)
- v_140: :531 (no light)
- v_347: :611 (no light)
- v_517: :700 (no light)
- v_534/535: :711/712 (no light)
- v_537: :713 (no light)
- v_540: :715 (no light)
- v_626: :767 (no light)
- v_627/628: :768/769 (no light)
- v_687: :819 (no light)
- v_688/689/690/691/692: :820-824 (no light)
- v_659/667/708: :793/800/840 (no light)
- v_370: :623 (no light)
- v_336: :602 (no light)
- v_341: :605 (no light)
- v_342: :606 (no light)
- v_343: :607 (no light)
- v_344: :608 (no light)
- v_327: :596 (no light)
- v_390: :625 (no light)
- v_391: :626 (no light)
- v_160: :541 (no light)
- v_171: :544 (no light)
- v_235: :350 (no light)
- v_238: :557 (no light)
- v_96: :137 (no light) — cooking_pot
- v_317/318: :592/593 (no light)
- v_286: :579 (no light)
- v_619: :762 (no light)
- v_620: :763 (no light)
- v_582: :742 (no light)
- v_270/271/581/660: :566/567/741/794 (no light)
- v_572: :737 (no light)
- v_262-268: :465-471 (no light)
- v_20 (acorn_sapling): :74 (no light)
- v_695/696: :827/828 (no light)
- v_699: :831 (no light)
- v_703: :835 (no light)
- v_717/718/719: :844/845/846 (no light)
- v_739: :866 (no light)
- v_658: :792 (no light)
- v_663: :797 (no light)
- v_415-418: :640-643 (no light)
- v_500-503: :685-688 (no light)
- v_568/569/570: :734/735/736 (no light)
- v_580: :740 (no light)
- v_429: :485 (specialTileLight)
- v_84: :434 (specialTileLight)
- v_646: :781 (no light)
- v_35 (jackolanterns): :443
- v_410/480/509/720/721/455 (monoliths): no light — vanilla? Are monoliths tileLighted? Lunar monolith 410 — is there a case? I didn't see one in my enumeration. Let me check: does ApplyTileLight have cases 410/480/509/658? 658 yes (aether). 410/480/509? Not in my list. Let me verify quickly whether tileLighted includes 410/480/509 and whether there are cases. From my summary's tileLighted list — I should double check whether 410/480/509/720/721/455 are in tileLighted. The summary said tileLighted-but-no-case: 19, 58, 76, 109, 346, 684, 701. So monoliths other than 658 are NOT tileLighted → no light in vanilla → repo no light ✓ 一致(均无光).

Let me verify that 410/480/509 are indeed not tileLighted, plus confirm the exact tileLighted list once more, and check 12 (heart) and 96. Quick grep.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:26:27.769Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"tileLighted\\[\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | sed -n '1,40p'; grep -c \"tileLighted\\[\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "description": "List tileLighted assignments in vanilla Main"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:26:27.803Z

**📎 ToolResult**

```
7015:		tileLighted[517] = true;
7019:		tileLighted[687] = true;
7023:		tileLighted[535] = true;
7027:		tileLighted[689] = true;
7031:		tileLighted[537] = true;
7035:		tileLighted[690] = true;
7039:		tileLighted[540] = true;
7043:		tileLighted[688] = true;
7047:		tileLighted[626] = true;
7051:		tileLighted[691] = true;
7055:		tileLighted[628] = true;
7059:		tileLighted[692] = true;
7060:		tileLighted[592] = true;
7061:		tileLighted[656] = true;
7062:		tileLighted[701] = true;
7063:		tileLighted[356] = true;
7064:		tileLighted[663] = true;
7262:		tileLighted[568] = true;
7266:		tileLighted[569] = true;
7270:		tileLighted[570] = true;
7274:		tileLighted[580] = true;
7277:		tileLighted[582] = true;
7280:		tileLighted[619] = true;
7284:		tileLighted[620] = true;
7288:		tileLighted[572] = true;
7294:		tileLighted[564] = true;
7303:		tileLighted[593] = true;
7307:		tileLighted[594] = true;
7308:		tileLighted[548] = true;
7309:		tileLighted[613] = true;
7310:		tileLighted[614] = true;
7321:		tileLighted[519] = true;
7333:		tileLighted[637] = true;
7342:		tileLighted[215] = true;
7369:		tileLighted[173] = true;
7370:		tileLighted[174] = true;
7372:		tileLighted[160] = true;
7373:		tileLighted[149] = true;
7417:		tileLighted[711] = true;
7499:		tileLighted[699] = true;
147

```


---

## 🤖 Assistant · 2026-08-13T06:26:29.711Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"tileLighted\\[\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | sed -n '41,147p' | grep -oE \"\\[[0-9]+\\]\" | tr -d '[]' | tr '\\n' ' '",
 "description": "Extract all tileLighted ids compact"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:26:29.741Z

**📎 ToolResult**

```
4 17 133 31 696 33 34 35 37 42 49 58 61 703 70 71 72 76 684 77 19 22 26 695 83 84 92 93 95 98 100 109 125 126 129 140 270 271 581 660 578 528 634 20 633 190 316 317 318 405 638 237 27 381 534 536 539 625 627 184 463 491 646 372 415 416 417 418 659 667 391 354 658 327 708 739 336 340 341 342 343 344 349 598 346 347 348 350 429 209 719 717 718 370 500 501 502 503 286 302 171 96 238 204 597 390

```


---

## 🤖 Assistant · 2026-08-13T06:26:39.639Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Full tileLighted list (147 entries incl. the 40 shown earlier). Combined:
4 17 133 31 696 33 34 35 37 42 49 58 61 703 70 71 72 76 684 77 19 22 26 695 83 84 92 93 95 98 100 109 125 126 129 140 270 271 581 660 578 528 634 20 633 190 316 317 318 405 638 237 27 381 534 536 539 625 627 184 463 491 646 372 415 416 417 418 659 667 391 354 658 327 708 739 336 340 341 342 343 344 349 598 346 347 348 350 429 209 719 717 718 370 500 501 502 503 286 302 171 96 238 204 597 390
plus from first 40: 517 687 535 689 537 690 540 688 626 691 628 692 592 656 701 356 663 568 569 570 580 582 619 620 572 564 593 594 548 613 614 519 637 215 173 174 160 149 711 699

Count = 106 + 40 = 146? grep -c said 147 lines (maybe one duplicate). Fine.

Key confirmations:
- 12 (Heart) NOT in tileLighted → crystal_heart light [255,60,90] is EXTRA (非原版).
- 58 (Hellstone) IS tileLighted but has NO case in ApplyTileLight → emits nothing → ore_hellstone [255,90,40] EXTRA.
- 19, 76, 109, 346, 684, 701 tileLighted but no case → no light ✓ repo correct (no light).
- 171, 96, 238, 204 are tileLighted and DO have cases (171 :2517, 96 :1520, 238 :1011, 204 :2576).
- 410/480/509/720/721/455 NOT tileLighted → monoliths no light ✓.

Wait — need to double-check 58: is there a case 58 in ApplyTileLight? From my enumeration: no case 58. Let me confirm by grepping "case 58:" in the switch region.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:26:39.652Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "f=~/Project/GLM/SandboxWorld/Terrarria1456/Terraria.Graphics.Light/TileLightScanner.cs\ngrep -nE \"^\\t\\tcase (12|19|58|76|96|109|171|204|346|684|701):\" \"$f\"",
 "description": "Check cases for ambiguous tile ids"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:26:39.680Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 2
ugrep: warning: ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria.Graphics.Light/TileLightScanner.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-13T06:26:45.199Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The intermittent "No such file or directory" again — this seems to happen when I use a variable `f=` in the command? No — earlier `f=...; grep ... "$f"` worked. It's flaky sandbox behavior. Let me retry with the literal path.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:26:45.809Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -nE \"case (12|19|58|76|96|109|171|204|346|684|701):\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs",
 "description": "Check switch cases for ambiguous ids"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:26:45.854Z

**📎 ToolResult**

```
314:		case 346:
846:				case 12:
1136:					case 12:
1264:				case 12:
1284:				case 19:
1478:				case 58:
1520:			case 96:
1621:				case 19:
1815:				case 58:
1909:				case 12:
1929:				case 19:
2123:				case 58:
2189:				case 12:
2220:				case 19:
2398:				case 58:
2517:			case 171:
2576:			case 204:
2840:				case 58:

```


---

## 🤖 Assistant · 2026-08-13T06:26:50.084Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting: `case 346:` at line 314 is in ApplyWallLight (wall 346). The rest are nested style cases (12/19/58 are style indices in lamp switches).

So in ApplyTileLight's top-level switch: case 96 (:1520), 171 (:2517), 204 (:2576) exist; cases 12, 19, 58, 76, 109, 684, 701, 346 do NOT exist at top level. Confirmed:
- 12 Heart: no tileLighted, no case → vanilla NO light → repo crystal_heart [255,60,90] EXTRA.
- 58 Hellstone: tileLighted, no case → no light → repo ore_hellstone [255,90,40] EXTRA.
- 19/76/109/346/684/701: no case → no light → repo correct.

Now everything is verified. Let me also double-check that ApplyTileLight has cases for all the tileLighted ids I enumerated, to make sure I haven't missed any vanilla glowing tile. Quick check: list top-level case ids in ApplyTileLight region (lines 344-3150) and compare with tileLighted set. Top-level cases are at 2-tab indentation (`\t\tcase`). Let me extract.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:26:50.721Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "awk 'NR>=344 && NR<=3150 && /^\t\tcase [0-9]+:/' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs | grep -oE \"[0-9]+\" | sort -n | tr '\\n' ' '",
 "description": "List all top-level ApplyTileLight case ids"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:27:01.352Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-13T06:27:03.405Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -nE $'^\\t\\tcase [0-9]+:' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs | awk -F: '$1>=344 && $1<=3150' | grep -oE \"case [0-9]+\" | grep -oE \"[0-9]+\" | sort -n | tr '\\n' ' '",
 "description": "Extract top-level case ids in ApplyTileLight"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:27:19.474Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-13T06:27:26.047Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Hmm, no output. Maybe the indentation is different (the file uses 2 tabs for top-level case inside switch inside method? Method body = 1 tab, switch = 1 tab, case = 2 tabs). My earlier grep `^\t\tcase (12|19|...)` matched lines like `		case 346:` at 314 — so 2-tab works. But awk -F: with $1>=344 — the line numbers... let me test without range filter.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:27:33.114Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -cE $'^\\t\\tcase [0-9]+:' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs",
 "description": "Count two-tab case lines"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:27:45.898Z

**📎 ToolResult**

```
21

```


---

## 🤖 Assistant · 2026-08-13T06:27:50.094Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Only 21 matches for `^\t\tcase`?? But earlier the grep for `case (12|...)` matched many lines like 1284, 1621 with leading whitespace. So most case lines have 3 tabs (nested). And 21 two-tab cases: those are in ApplyWallLight (21 wall cases!) — makes sense: ApplyWallLight's switch is at method-body level (1 tab) so cases are 2 tabs. ApplyTileLight's switch must be nested inside `if (Main.tileLighted[tile.type]) { switch ... }` → 3 tabs.

So for ApplyTileLight top-level cases I need `^\t\t\tcase`. Let me extract those in range 344-3150.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:27:50.809Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -nE $'^\\t\\t\\tcase [0-9]+:' ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria.Graphics.Light/TileLightScanner.cs | awk -F: '$1>=344 && $1<=3150 {print $1\" \"$2}' | tr '\\n' '|'",
 "description": "List three-tab case ids in ApplyTileLight"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:28:10.197Z

**📎 ToolResult**

```
ugrep: warning: ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria.Graphics.Light/TileLightScanner.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-13T06:28:13.339Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -nE $'^\\t\\t\\tcase [0-9]+:' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs\" | sed -n '1,200p' | awk -F: '$1>=344 && $1<=3150' | sed 's/\\t//g' | tr '\\n' '|'",
 "description": "List three-tab cases within ApplyTileLight range"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:29:03.025Z

**📎 ToolResult ⚠️ERROR**

```
Permission for this action was denied by the Claude Code auto mode classifier. Reason: Auto mode could not evaluate this action and is blocking it for safety — run with --debug for details. If you have other tasks that don't depend on this action, continue working on those. IMPORTANT: You *may* attempt to accomplish this action using other tools that might naturally be used to accomplish this goal, e.g. using head instead of cat. But you *should not* attempt to work around this denial in malicious ways, e.g. do not use your ability to run tests to execute non-test actions. You should only try to work around this restriction in reasonable ways that do not attempt to bypass the intent behind this denial. If you believe this capability is essential to complete the user's request, STOP and explain to the user what you were trying to do and why you need this permission. Let the user decide how to proceed. To allow this type of action in the future, the user can add a Bash permission rule to their settings.

```


---

## 🤖 Assistant · 2026-08-13T06:29:06.596Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The classifier blocked that command (probably the sed 's/\t//g' + tr combo looked odd). I don't strictly need this — I already have the full case list from my complete read (recorded in the summary) and I've verified the ambiguous ones individually. The tileLighted list vs case list cross-check was done during the earlier session: only 19/58/76/109/346/684/701 lack cases (of which 58 is the notable one).

Actually, let me do one cleaner cross-check with a simple grep + sort to enumerate the ApplyTileLight top-level cases, to be thorough about not missing any glowing tile.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:29:07.335Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -nE $'^\\t\\t\\tcase [0-9]+:' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs | grep -oE \"case [0-9]+\" | grep -oE \"[0-9]+\" | sort -n | uniq | tr '\\n' ' '",
 "description": "Enumerate all three-tab switch cases"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:29:11.344Z

**📎 ToolResult**

```
0 1 2 3 4 5 6 17 20 22 26 27 31 33 34 35 37 42 49 61 70 71 72 77 83 84 92 93 95 96 98 100 125 126 129 133 140 149 160 171 173 174 184 190 204 209 215 235 237 238 262 263 264 265 266 267 268 270 271 286 302 316 317 318 327 336 340 341 342 343 344 347 348 349 350 354 356 370 372 381 390 391 405 415 416 417 418 429 463 491 500 501 502 503 517 519 528 534 535 536 537 539 540 548 564 568 569 570 572 578 580 581 582 592 593 594 597 598 613 614 619 620 625 626 627 628 633 634 637 638 646 656 658 659 660 663 667 687 688 689 690 691 692 695 696 699 703 708 711 717 718 719 739

```


---

## 🤖 Assistant · 2026-08-13T06:29:54.266Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Complete list of ApplyTileLight top-level cases (146 cases; ids 0-6 are nested elsewhere? Wait — 0 1 2 3 4 5 6 appear, but those are probably style cases in OTHER three-tab switches (e.g., inside case 215 campfire's style switch or candle style switches). Hmm, three-tab nesting also occurs in the lamp switches (e.g. case 33's style switch at 3 tabs). So this list includes style indices 0-6 from nested style switches.

Top-level tile cases are those ≥ 17 in this list, plus 4 (torch) — yes 4 is there. So the tile case set is:
4 17 20 22 26 27 31 33 34 35 37 42 49 61 70 71 72 77 83 84 92 93 95 96 98 100 125 126 129 133 140 149 160 171 173 174 184 190 204 209 215 235 237 238 262-268 270 271 286 302 316 317 318 327 336 340 341 342 343 344 347 348 349 350 354 356 370 372 381 390 391 405 415-418 429 463 491 500-503 517 519 528 534 535 536 537 539 540 548 564 568 569 570 572 578 580 581 582 592 593 594 597 598 613 614 619 620 625 626 627 628 633 634 637 638 646 656 658 659 660 663 667 687-692 695 696 699 703 708 711 717 718 719 739

That's the definitive vanilla glowing-tile case list — matches my enumeration exactly (130 tile cases). Great, and it confirms 58/12/19/76/109/346/684/701 have no case.

Count: let me count for the report: I'll say "原版 ApplyTileLight 顶层 case 共 130 个 tile 类型（:344-3150）".

Now let me also confirm case 0-6 are nested style cases (e.g. 6 appears at 1425-ish?). Not needed.

One more: the summary said case 92 "frameY<=18 && frameX==0 → 1/1/1". Confirmed above at 1165-1172.

Also case 96: `if (tile.frameX >= 36)` → (0.5,0.35,0.1) — cooking pot 2x2; gate frameX>=36 (right column!). Repo cooking_pot has no light → 缺失.

Now section 1 counts. Let me categorize my final judgments. I'll write the report with per-entry lines. Given ~130 cases, I'll present them grouped in tables/lists with concise per-entry format. The user asked: 每条 [原版行号+值, 本仓文件:行号+值, 判定]. I'll comply per entry.

Let me also compute the 偏差(N) counts. And include a summary at the end of section 1.

Let me also double check repo line numbers for scanner branches:
- TileLightScanner.ts:31-94 specialTileLight
- case 42: :35-61
- case 126: :62-67
- case 429: :68-76
- case 209: :77-80
- case 84: :81-90
- lavaV: :164
- hell: :161-162
- exposed: :134-153
- wall emissive merge: :190-211
- tile light: :213-253
- torch: :225-237
- mushroom: :238-243
- def.light + flicker: :244-249
- special merge: :254-259
- liquid: :261-264

SkyColor.ts: demonTorchColor :136-139; shimmerTorchColor :142-146; discoColor :148-150; tick :110-133.

devices.ts LIGHT_TOGGLE :522-529, lightIsOn :532-537 (from summary).

lightTables.ts: WALL_LIGHT :57, TORCH_COLORS :60-85, FLICKER_SHEETS :87, MUSHROOM_GLOW_SHEETS :90, WALL_EMISSIVE :93-115, MOON_FLOOR :118.

Now let me think about what "偏差(N)" means: N = number of discrepant aspects. I'll use it consistently.

Also need to note in section 1 the FLICKER_SHEETS systematic issue and the two EXTRA lights (12 heart, 58 hellstone).

Also worth noting: repo applies def.light to ALL cells of a framed multi-cell object (e.g., lamp 1x3 → repo fh:3 but vanilla w:1 h:6; lamppost 6 cells; chandelier 9 cells). Vanilla gates are per-cell frame conditions (e.g. 92 only top cell, 98 only top row, 34/100/93/42 whole object but frameX/Y conditions pick cells). Repo's def.light applies to every cell of the object → over-glow for: 92 lamppost (6 cells vs 1), 98 skull lantern (4 cells vs top row 2), 129 crystal (all styles), 592 brazier (frameY>0 gate missing), 519 cattail (frameY==90 gate missing), 548/593/594 gates, 61/26/31 gates, 83 gates, 27 gate, 93/33/34/100/42/95 toggle gates (handled via LIGHT_TOGGLE where registered).

Actually careful: does the repo apply def.light per-cell for framed objects? The scanner iterates every tile cell; a framed object stores its own def in each cell (all cells have type). def.light is on the def → each cell emits. Yes. So for 6-cell lamppost: 6 cells emit [255,255,255] vs vanilla 1 cell. Worth flagging once as a systemic note rather than per-entry.

Similarly campfire 3x2=6 cells: vanilla gate frameY<36 (top row, 3 cells) → repo 6 cells. Fireplace 3x2: vanilla frameX<54 → 2 cells? frameX<54 means cells at frameX 0,18,36 (3 columns) for all rows? Fireplace frameY also varies... whatever, gate partially handled by LIGHT_TOGGLE? 405 not in LIGHT_TOGGLE. So repo fireplace: 6 cells always; vanilla: cells with frameX<54 → 3 of 6? Fireplace is 3x2 (54x36+padding); frameX per cell: col0=0, col1=54? Hmm, 3-wide object: cell frameX = 0, 54, 108? No — frameX is the pixel offset within the sheet: col0 → 0, col1 → 54, col2 → 108. So frameX<54 → only col0 → 1 cell! Vanilla fireplace emits from 1 cell (left column). Repo: 6 cells. That's a real over-glow. I'll note per entry as gate missing.

Wait, but for campfire the gate is frameY<36: rows: row0 → frameY=0, row1 → frameY=36 → only top row (3 cells). OK.

And for candelabra 100: gate frameX<36 → cols 0 only (frameX 0), col1 → 36 → excluded! So vanilla candelabra emits from left column only (1 cell of 4). Hmm really? Candelabra is 2x2: frameX values 0 and 36; gate frameX<36 → only left column (2 cells). Interesting. Repo: LIGHT_TOGGLE ['x',36] → frameX%72<36 → col0 (0) on, col1 (36) off. So repo emits from left column only too ✓ (2 cells). Good, that matches cell-wise too.

Chandelier 34: gate frameX%108>=54 → break. 3-wide: frameX 0,54,108 → col0 (0%108=0 <54 ✓), col1 (54%108=54 → break ✗), col2 (108%108=0 ✓). So vanilla chandelier emits from cols 0 and 2 (left+right), not middle! Repo LIGHT_TOGGLE ['x',54] → frameX%108<54 → col0 ✓ on, col1 ✗ off, col2 (108%108=0<54 ✓) on. ✓ matches cell-wise too. 

Lamp 93: gate frameX==0 → lamp is 1-wide → single column, all 6 rows emit? frameX==0 for all cells of a 1-wide object (frameY varies). So vanilla lamp emits all 6 cells ✓ repo 6 cells (fh:3 in repo but 6 rows placed? v_93 fh:3 — the def says fw:1 fh:3 but w:1 h:6. Whatever.) ✓.

Chinese lantern 95: gate frameX<36 → 2-wide: col0 (0) ✓, col1 (54)? 2-wide object frameX = 0, 54? Hmm 2-wide = 36px? Objects use 18px cells but frame coords are per-style in the sheet with padding... In Terraria, multi-tile objects' frameX advances by (width*18 + 2). For a 2-wide object: frameX = 0 and 38? No: TileObjectData coordinates — cell (cx,cy) frame = origin + cx*(18+2), cy*(18+2). So col1 frameX = 20. So frameX<36 covers both cols (0,20) ✓. And toggled-off adds 36+2? For 2-wide: +38? Hmm, the LIGHT_TOGGLE offsets in repo: 18 for 1-wide, 36 for 2-wide, 54 for 3-wide. Vanilla gates: frameX==0 (1-wide), frameX<36 (2-wide covers 0,20), frameX<54 (3-wide covers 0,20,40), frameX%108<54 (chandelier 3-wide but 6 styles wide?). These are consistent with repo's toggles. Fine — I'll trust repo's LIGHT_TOGGLE design as functionally equivalent for on/off, and only flag where vanilla's gate is NOT an on/off toggle (92 frameY<=18, 98 frameY==0, 96 frameX>=36 [inverse!], 592 frameY>0 [inverse], 548 frameX/54>=7, 593/594, 129 style, 61/26/31/83/27/20/238/235 state gates).

Note 96 cooking pot: gate frameX>=36 → the RIGHT column emits (not left). Repo missing entirely anyway.

OK. I'm confident. One more small thing for section 4: also mention ApplyLiquidLight's Y/Z threshold quirk (uses num as compare, num*0.6 as value → can lower existing light), repo uses pure max → slight semantic difference. And lava `tile.lava()` = liquidType==Lava.

Also the hell light: repo `performance.now()*0.002` = sin(2*seconds) ≡ vanilla sin(GlobalTimeWrappedHourly*2) since GlobalTimeWrappedHourly = TotalSeconds % 3600 → 一致 (only difference: 3600s wrap discontinuity, negligible). I'll mark hell timing 一致(近似, wrap 差异可忽略) — this corrects my earlier draft note.

Also for section 4: vanilla ApplyHellLight also tints stained glass (88-93/241) with the same multiplier on the hell base — repo's tint branch applies regardless of depth ✓ covered, but via max-synthesis and gated `st.type[i]===0` while vanilla allows halfBrick/non-blocking tiles. Minor deviation noted.

Now, also section 2's gate: repo `st.type[i]===0` vs vanilla `!LightIsBlocked(tile)` (= active && tileBlockLight). For non-solid non-blocking tiles (platforms, torches, furniture), vanilla still emits the wall light; repo doesn't → 偏差 for all 21 walls. I'll note it once as a structural item.

Also the stained-glass tint in repo is at :195-210 — I should judge the tint table itself: repo TINT k=0..6 vs vanilla switch values:
vanilla (from ApplySurfaceLight :3190-3242 and ApplyHellLight :3286+):
- case 0 (wall 88 purple): R*0.9, G*0.15, B*0.9
- case 1 (89 yellow): 0.9,0.9,0.15
- case 2 (90 blue): 0.15,0.15,0.9
- case 3 (91 green): 0.15,0.9,0.15
- case 4 (92 red): 0.9,0.15,0.15
- case 5 (93 rainbow): num*=0.7+DiscoR*0.2/255? per summary "5 彩虹(0.7+Disco×0.2)"
- case 6 (241 orange): 0.9,0.5,0
Repo TINT: [0.9,0.15,0.9],[0.9,0.9,0.15],[0.15,0.15,0.9],[0.15,0.9,0.15],[0.9,0.15,0.15],[0.7+0.2,0.7,0.7],[0.9,0.5,0] ✓ matches (k=5 handled dynamically with disco). So tint multipliers 一致; the deviation is semantics: vanilla multiplies the sky/hell light already present (num4-based) by these factors (reducing it), repo takes max with the factor (raising dark cells to the factor). For a glass wall cell at night: vanilla → sky light 0 → 0*0.9=0 → glass wall dark at night! Repo → max(0, 0.9) = 0.9 → glass wall glows 0.9 at night. HUGE deviation: repo makes stained glass walls self-luminous at night; vanilla only tints existing daylight. Must flag prominently in section 2/4 area. It's part of section 1's scope? The task's five sections: 1 tile, 2 WALL_EMISSIVE, 3 torch, 4 liquid, 5 WALL_LIGHT. Stained glass tint belongs to ApplySurfaceLight — I'll put it in section 2 (walls) as a structural item since it's wall-related.

Let me verify vanilla ApplySurfaceLight tint code to be precise about the multiply semantics.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:29:54.551Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs",
 "limit": 62,
 "offset": 3186
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:29:54.558Z

**📎 ToolResult**

```
3186					}
3187					num3 = num6 * 0.175f * (1f + Main.rand.NextFloat() * 0.13f) * Main.liquidAlpha[13];
3188				}
3189			}
3190			if ((!tile.active() || tile.halfBrick() || !Main.tileNoSunLight[tile.type]) && ((tile.wall >= 88 && tile.wall <= 93) || tile.wall == 241) && tile.liquid < byte.MaxValue)
3191			{
3192				num = num4;
3193				num2 = num5;
3194				num3 = num6;
3195				int num8 = tile.wall - 88;
3196				if (tile.wall == 241)
3197				{
3198					num8 = 6;
3199				}
3200				switch (num8)
3201				{
3202				case 0:
3203					num *= 0.9f;
3204					num2 *= 0.15f;
3205					num3 *= 0.9f;
3206					break;
3207				case 1:
3208					num *= 0.9f;
3209					num2 *= 0.9f;
3210					num3 *= 0.15f;
3211					break;
3212				case 2:
3213					num *= 0.15f;
3214					num2 *= 0.15f;
3215					num3 *= 0.9f;
3216					break;
3217				case 3:
3218					num *= 0.15f;
3219					num2 *= 0.9f;
3220					num3 *= 0.15f;
3221					break;
3222				case 4:
3223					num *= 0.9f;
3224					num2 *= 0.15f;
3225					num3 *= 0.15f;
3226					break;
3227				case 5:
3228				{
3229					float num9 = 0.2f;
3230					float num10 = 0.7f - num9;
3231					num *= num10 + (float)Main.DiscoR / 255f * num9;
3232					num2 *= num10 + (float)Main.DiscoG / 255f * num9;
3233					num3 *= num10 + (float)Main.DiscoB / 255f * num9;
3234					break;
3235				}
3236				case 6:
3237					num *= 0.9f;
3238					num2 *= 0.5f;
3239					num3 *= 0f;
3240					break;
3241				}
3242			}
3243			float num11 = 1f - Main.shimmerDarken;
3244			num *= num11;
3245			num2 *= num11;
3246			num3 *= num11;
3247			if (lightColor.X < num)

```


---

## 🤖 Assistant · 2026-08-13T06:30:04.658Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed:
- The tint branch sets num/num2/num3 = the SKY light (num4/num5/num6) then multiplies by the tint factors. So it's a recolor of existing sky light, NOT an additive emission. Note case 3 (green, wall 91): vanilla multipliers (0.15, 0.9, 0.15) — wait line 3217-3220: case 3: num*=0.15, num2*=0.9, num3*=0.15 ✓ (green keeps G). Repo TINT[3] = [0.15,0.9,0.15] ✓.
- case 6 (orange 241): num*=0.9, num2*=0.5, num3*=0f — B multiplied by 0 (not 0!). Repo TINT[6] = [0.9,0.5,0] — as a max-merge value that's equivalent to 0 for B only in the multiply semantics; as max it forces B=0 which is harmless (max with 0). OK.
- case 5 rainbow: num10 = 0.7-0.2 = 0.5 → factor = 0.5 + Disco/255*0.2 ∈ [0.5, 0.7]. Repo computes [0.7 + disco*0.2, ...] where disco∈[0,1] → [0.7, 0.9] — WRONG: repo uses 0.7+0.2*d instead of 0.5+0.2*d (i.e., repo forgot num10 = 0.7-num9 = 0.5). Repo TINT[5] fallback [0.9,0.7,0.7] (0.7+0.2 hardcoded) and dynamic `0.7 + (dc)*0.2` → range [0.7,0.9] vs vanilla [0.5,0.7]. 偏差(常数错 +0.2 抬高).

Also the shimmerDarken multiplier (:3243-3246) applies to surface sky light — repo? Not seen in scanner; likely handled in skySeed? That's engine/sky side (other agent's scope). I'll note it briefly as out-of-scope/absent.

Also line 3187: the liquid>=200 branch `num3 = num6*0.175*(1+rand*0.13)*liquidAlpha[13]` — this is for shimmer liquid at surface (liquidAlpha[13] is set when shimmer is the "current liquid style"? Actually Main.liquidAlpha[13] relates to liquid type 13?? In 1.4.4 LiquidID.Shimmer=3... liquidAlpha is indexed by "LiquidID + something"? Let me not dig — I'll mention: 表层满液(liquid>=200)格的 B 通道微光分支(:3186-3188, liquidAlpha[13])本仓未实现 — 属地表光细节,归天空光一路。Actually it's in ApplySurfaceLight which is section 4-adjacent (liquid light). I'll include as a section 4 item: 液体表面 B 微光缺失.

Hmm, what is liquidAlpha[13]? In Main.cs, `liquidAlpha[13]` — probably set to 1 when the "water style" is shimmer? Let me check quickly to describe it accurately.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:30:04.976Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"liquidAlpha\\[13\\]\" ~/Project/GLM/SandboxWorld/Terarria1456 | head -5",
 "description": "Find liquidAlpha 13 assignments"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:30:05.038Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs:3181:			else if (Main.liquidAlpha[13] > 0f)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs:3187:				num3 = num6 * 0.175f * (1f + Main.rand.NextFloat() * 0.13f) * Main.liquidAlpha[13];
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Capture/CaptureInterface.cs:1092:					Main.liquidAlpha[13] = 0f;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WaterfallManager.cs:1217:		if (Main.liquidAlpha[13] > 0f)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WaterfallManager.cs:1219:			DrawWaterfall(24, Main.liquidAlpha[13]);

```


---

## 🤖 Assistant · 2026-08-13T06:30:07.412Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"liquidAlpha\\[13\\] = \\|liquidAlpha\\[13\\]=\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head -5; grep -rn \"shimmerAlpha\\|liquidAlpha\\[\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | grep -n \"13\" | head -8",
 "description": "Find where liquidAlpha 13 is set in Main"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:30:07.459Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-13T06:30:09.836Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"liquidAlpha\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head -12",
 "description": "Search liquidAlpha usage in Main"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:30:09.859Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:1162:	public static float[] liquidAlpha = new float[15];
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:56153:		float[] array3 = liquidAlpha.ToArray();
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:56177:				liquidAlpha[i] = ((i == biome.WaterStyle) ? 1f : 0f);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:56554:		liquidAlpha = array3;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:56852:						liquidAlpha[i] = Math.Max(liquidAlpha[i] - 0.2f, 0f);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:56856:						liquidAlpha[i] = Math.Min(liquidAlpha[i] + 0.2f, 1f);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:56870:			if (IsLiquidStyleWater(j) && liquidAlpha[j] > 0f && j != waterStyle)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:56872:				DrawLiquid(isBackground, j, isBackground ? 1f : liquidAlpha[j], waterOnly: true);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:56876:		DrawLiquid(isBackground, waterStyle, flag ? liquidAlpha[waterStyle] : 1f);

```


---

## 🤖 Assistant · 2026-08-13T06:30:14.789Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
liquidAlpha[i] = 1 for i == biome.WaterStyle — it's the water-style crossfade array (index 13 = a specific water style, likely "shimmer" water style id 13). So `liquidAlpha[13] > 0` means the current water style is style 13 (shimmer water). So the :3181-3188 branch: for a surface cell with liquid>=200 (full liquid), if the water style is shimmer (13), B gets `skyB * 0.175 * (1+rand*0.13) * alpha` — a shimmer-water surface tint. Very niche. I'll mention it in one line as missing, noting it's gated on water style 13 (shimmer style) — actually I should double check that water style 13 is shimmer. WaterStyleID: 13 = Shimmer? In Terraria, WaterStyleID.Shimmer = 13? Let me check quickly — grep WaterStyleID for 13.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:30:15.632Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"= 13;\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/WaterStyleID.cs 2>/dev/null | head; grep -rn \"Shimmer\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/WaterStyleID.cs 2>/dev/null | head",
 "description": "Check WaterStyleID 13 meaning"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:30:15.667Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/WaterStyleID.cs:31:	public static readonly int Count = 13;

```


---

## 🤖 Assistant · 2026-08-13T06:30:19.186Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
WaterStyleID.Count = 13, so valid styles are 0..12; index 13 is out of the enum range — liquidAlpha[13] is never set by the biome loop (i ranges over 0..Count-1 presumably). Let me check line 56177's loop bounds. If the loop only goes 0..12, liquidAlpha[13] stays 0 forever → the branch is dead code in vanilla! That would be a fun finding: the :3181 branch never fires (liquidAlpha[13] always 0). Let me verify the loop bounds.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:30:19.407Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "limit": 18,
 "offset": 56165
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:30:19.415Z

**📎 ToolResult**

```
56165			CaptureBiome biome = settings.Biome;
56166			Vector2 vector = screenPosition;
56167			int num2 = screenWidth;
56168			int num3 = screenHeight;
56169			bool captureMech = settings.CaptureMech;
56170			screenWidth = area.Width << 4;
56171			screenHeight = area.Height << 4;
56172			screenPosition = new Vector2(area.X * 16, area.Y * 16);
56173			for (int i = 0; i <= 10; i++)
56174			{
56175				if (i != 1)
56176				{
56177					liquidAlpha[i] = ((i == biome.WaterStyle) ? 1f : 0f);
56178				}
56179			}
56180			float num4 = (biome.TileColor == CaptureBiome.TileColorStyle.Mushroom).ToInt();
56181			SetBackColor(new InfoToSetBackColor
56182			{

```


---

## 🤖 Assistant · 2026-08-13T06:30:22.598Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
That's the CaptureInterface path (only 0..10). The main game path sets liquidAlpha elsewhere. Let me search for where liquidAlpha is assigned during normal gameplay — maybe in Update or in the water style transition code. grep showed :56153 (capture), :56177 (capture), :56852/56856 (transition ±0.2). Who initializes liquidAlpha[waterStyle]=1 in normal play? Maybe via `liquidAlpha[waterStyle] = 1` somewhere. Let me grep for that pattern.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:30:23.541Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"liquidAlpha\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria | grep -v \"Main.cs\" | grep -vE \"WaterfallManager|CaptureInterface|TileLightScanner\" | head -12",
 "description": "Find other liquidAlpha writers"
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:30:23.575Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-13T06:30:26.702Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Only Main.cs (capture + transition decay/grow), WaterfallManager, CaptureInterface, TileLightScanner. The transition code at :56852-56856 raises/lowers by 0.2 — driven presumably when waterStyle changes. So during normal gameplay liquidAlpha[waterStyle] → 1 and others → 0 via that transition. Since WaterStyleID.Count=13 (0..12), index 13 is never a waterStyle → liquidAlpha[13] remains 0 → the :3181 branch in ApplySurfaceLight is dead code in 1.4.5. 

Let me confirm :56840-56860 to see the loop bounds.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:30:26.993Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "limit": 24,
 "offset": 56838
}
```


---

## 👤 User(sidechain) · 2026-08-13T06:30:26.999Z

**📎 ToolResult**

```
56838			{
56839				return;
56840			}
56841			TimeLogger.StartTimestamp fromTimestamp = TimeLogger.Start();
56842			drewLava = false;
56843			if (!isBackground)
56844			{
56845				waterStyle = CalculateWaterStyle();
56846				for (int i = 0; i < 15; i++)
56847				{
56848					if (IsLiquidStyleWater(waterStyle))
56849					{
56850						if (waterStyle != i)
56851						{
56852							liquidAlpha[i] = Math.Max(liquidAlpha[i] - 0.2f, 0f);
56853						}
56854						else
56855						{
56856							liquidAlpha[i] = Math.Min(liquidAlpha[i] + 0.2f, 1f);
56857						}
56858					}
56859				}
56860			}
56861			if (!drawToScreen && !isBackground)

```


---

## 🤖 Assistant · 2026-08-13T06:31:38.926Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The loop goes i < 15, but only index == waterStyle gets raised. waterStyle comes from CalculateWaterStyle() ∈ [0..12]. So liquidAlpha[13] never becomes >0 in normal play → the ApplySurfaceLight :3181 `else if (Main.liquidAlpha[13] > 0f)` branch is dead code in 1.4.5 (only reachable if a mod/water style 13 existed). Great — so it's NOT a repo gap. I'll note it as "原版死代码（liquidAlpha[13] 恒 0），本仓不实现无影响" — nice catch that avoids a false positive.

Now I'm fully done with data collection. Time to write the final report. It must be thorough, structured in 5 sections, with entries formatted [原版行号+值, 本仓文件:行号+值, 判定]. No big code blocks. Absolute paths. No emoji. 3-decimal values.

Let me carefully compose. I'll reference files with short names after defining full paths once, to keep readability: 
- 原版扫描器 = ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs（下称 CS）
- 本仓扫描器 = ~/Project/GLM/SandboxWorld/game/src/lighting/TileLightScanner.ts（下称 TS）
- 表 = ~/Project/GLM/SandboxWorld/game/src/lighting/lightTables.ts（下称 LT）
- tiles = ~/Project/GLM/SandboxWorld/game/src/data/tiles.ts（下称 TD）
- TorchID = ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TorchID.cs
- Main = ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs
- SkyColor = ~/Project/GLM/SandboxWorld/game/src/lighting/SkyColor.ts
- devices = ~/Project/GLM/SandboxWorld/game/src/world/wiring/devices.ts

Format per entry: `id 名称 [CS:行 值 | TD:行 值 | 判定]`. I'll keep each on one line.

Section 1 entries (vanilla case order):
1. 658 AetherMonolith CS:354-377: !invisibleBlock → TorchColor(23)×(frameY/54: default 0.2 / case1 0.3 / case2 0.1) | TD:792 无 light + TS specialTileLight 无 case | 缺失
2. 356 Sundial CS:378-385: sundialCooldown==0 → (0.45,0.25,0) | TD:334 [115,64,0]/255=(0.451,0.251,0) | 偏差(1)：cooldown 门缺失
3. 663 Moondial CS:386-393: moondialCooldown==0 → (0,0.25,0.45) | TD:797 无 | 缺失
4. 656 GlowTulip CS:394-397 (0.2,0.55,0.5) | TD:348 [255,185,110]=(1,0.725,0.431) | 偏差(3)
5. 20 Saplings CS:399-408: frameX/18∈30..32 → (0.325,0.15,0.05) | TD:74 无 | 缺失
6. 634 TreeAsh CS:410 (0.65,0.3,0.1) | TD:252 [166,77,26]=(0.651,0.302,0.102) | 一致
7. 633/637/638 AshGrass/Plants/Vines CS:415-421 (0.325,0.15,0.05) | TD:178/247/354 [83,38,13]=(0.325,0.149,0.051) | 一致×3
8. 463 DefendersForge CS:422 (0.2,0.4,0.8) | TD:155 [51,102,204]=(0.2,0.4,0.8) | 一致
9. 491 VoidVault CS:427 (0.5,0.4,0.7) | TD:324 [128,102,179]=(0.502,0.4,0.702) | 一致
10. 209 Cannon CS:432-447: portal0=GetPortalColor(p,0)*0.65=(0.65,0.3055,0) frameX 234/252; portal1=(0.13,0.5876,0.65) frameX 306/324 | TS:77-80 [0.42,0.2,0.65]/[0.65,0.26,0] | 偏差(2)：两档色值皆错
11. 415-418 Fragment blocks CS:448-482 | TD:640-643 无 | 缺失×4
12. 500-503 Lunar bricks CS:453-487 | TD:685-688 无 | 缺失×4
13. 390 LavaLamp CS:488 (0.4,0.2,0.1) | TD:625 无 | 缺失
14. 597 Pylon CS:493-540: 8 样式 ×0.75, style0=(0.0375,0.6,0.225) | TD:282 [13,204,77]=(0.051,0.8,0.302) | 偏差(2)：未 ×0.75 + 7 样式缺失
15. 564 PlasmaLamp CS:541-547: frameX<36 → (0.05,0.3,0.55) | TD:500 [13,77,140]=(0.051,0.302,0.549); LT:87 FLICKER 含 564 | 偏差(2)：多余 flicker（门由 devices['x',36] ✓ 等效）
16. 568/569/570 FairyJars CS:549-563 | TD:734-736 无 | 缺失×3
17. 580 HellButterflyJar CS:564 (0.7,0.3,0.2) | TD:740 无 | 缺失
18. 391 CageEnchantedNightcrawler CS:569 (0.3,0.1,0.25) | TD:626 无 | 缺失
19. 582/598 MagmaSnailCage/LavafishBowl CS:922-927 (0.7,0.2,0.1) | TD:742 无 / TD:317 [255,185,110]=(1,0.725,0.431) | 缺失 / 偏差(3)
20. 270 FireflyBottle CS:928 (0.73,1,0.41) | TD:566 无 | 缺失
21. 271 LightningBug CS:933 (0.45,0.95,1) | TD:567 无 | 缺失
22. 581 Lavafly CS:938 (1,0.75,0.5) | TD:741 无 | 缺失
23. 660 Faeling CS:943 TorchColor(23) | TD:794 无 | 缺失
24. 572 SoulBottles CS:946-980: 6 档 frameY/36 | TD:737 无 | 缺失
25. 262-268 Gemspark CS:981-1006 | TD:465-471 无 | 缺失×7
26. 237 LihzahrdAltar CS:1007-1009 (0.1,0.1,0) | TD:336 [26,26,0]=(0.102,0.102,0) | 一致
27. 238 PlanteraBulb CS:1011-1019: 抬 X/Z 至 0.5 | TD:557 无 | 缺失
28. 235 Teleporter CS:1021-1028: 抬 X/Y 至 0.6 | TD:350 无 | 缺失
29. 405 Fireplace CS:1031-1073: frameX<54; flicker num27; 样式 frameX/54 | TD:331 [255,185,110]+LT:87 flicker | 偏差(3)：色值错 + frameX<54 门缺 + 样式缺（flicker ✓）
30. 215 Campfire CS:1074-1164: frameY<36; 16 样式; default (0.9,0.3,0.1) + flicker | TD:280 [255,185,110]+flicker; devices ['y',36] ✓ | 偏差(3)：色错 + 样式缺（flicker ✓ 门 ✓）
31. 92 Lampposts CS:1165-1172: frameY<=18 && frameX==0 → (1,1,1) | TD:444 [255,255,255]×6 格 + LT:87 flicker | 偏差(3)：frameY<=18 门缺（6 格全亮）+ 多余 flicker
32. 592 Brazier CS:1173-1185: frameY>0 → (1.35,0.45,0.15)+flicker | TD:283 [255,185,110] 静态 | 偏差(4)：色错 + flicker 缺 + frameY>0 门缺
33. 593/594 Volcano CS:1186-1201: frameX<18 / <36 → (0.8,0.3,0.1) | TD:502/503 [204,77,26]=(0.8,0.302,0.102) | 偏差(1 门)×2
34. 548 PottedTrees2 CS:1202-1208: frameX/54>=7 → (0.7,0.3,0.2) | TD:315 [179,77,51]=(0.702,0.302,0.2) | 偏差(1 门)
35. 613/614 PottedLavaPlants CS:1210-1215 (0.7,0.3,0.2) | TD:304/316 | 一致×2
36. 93 Lamps CS:1216-1519: frameX==0; 样式 frameY/54; default (1,0.97,0.85); 含 demonTorch 档 :1307 与 hsl 档 :1338 | TD:261 [255,185,110]=(1,0.725,0.431)+flicker; devices ['x',18] ✓ | 偏差(4)：色错 + 样式缺 + 多余 flicker
37. 96 CookingPots CS:1520-1527: frameX>=36 → (0.5,0.35,0.1) | TD:137 无 | 缺失
38. 98 SkullLanterns CS:1528-1535: frameY==0 → (1,0.97,0.85) | TD:148 [255,160,70]=(1,0.627,0.275) 全 4 格 | 偏差(3)：色错 + frameY==0 门缺
39. 4 Torch CS:1537-1541: frameX<66 → TorchColor(frameY/22) | TS:225-237 TORCH_COLORS+style 7/14/23 动态 + flicker :236-237; devices ['x',66] ✓ | 偏差(1)：多余 flicker（原版无）
40. 372 PeaceCandle CS:1542-1549: frameX==0 → (0.9,0.1,0.75) | TD:474 [230,26,191]=(0.902,0.102,0.749); devices ['x',18] ✓ | 一致
41. 646 ShadowCandle CS:1550-1557: frameX==0 → (0.2,0.3,0.32) | TD:781 无 | 缺失
42. 33 Candles CS:1558-1851: frameX==0; 样式 frameY/22; default (1,0.95,0.65); demonTorch 档 :1654; hsl 档 :1670 | TD:142 [255,185,110]+flicker | 偏差(4)
43. 174 PlatinumCandle CS:1852-1859: frameX==0 → (1,0.95,0.65) | TD:452 [255,242,166]=(1,0.949,0.651)+flicker | 偏差(1)：多余 flicker
44. 100/173 Candelabras CS:1860-2164: frameX<36; 样式 frameY/36; default (1,0.95,0.65); demon 档 :1952; hsl 档 :1983 | TD:146 [255,185,110]+flicker / TD:451 [255,242,166]+flicker | 偏差(4) / 偏差(3)：173 缺样式但基值 ✓
45. 34 Chandeliers CS:2165-2471: frameX%108<54; 样式 frameY/54+37*(frameX/108); default (1,1,1); demon :2273; hsl :2289 | TD:143 [255,190,120]=(1,0.745,0.471)+flicker | 偏差(4)
46. 35 Jackolanterns CS:2472-2479: frameX<36 → (0.75,0.6,0.3) | TD:443 [179,153,230]=(0.702,0.6,0.902) | 偏差(2)：R/B 错 + frameX<36 门缺（未注册 LIGHT_TOGGLE）
47. 95 ChineseLanterns CS:2480-2487: frameX<36 → (1,0.95,0.8) | TD:147 [255,160,70]=(1,0.627,0.275)+flicker | 偏差(3)：G/B 错 + 多余 flicker（门 ['x',36] ✓）
48. 17 Furnaces CS:2488-2492 (0.83,0.6,0.5) | TD:64 [255,140,70]=(1,0.549,0.275) | 偏差(3)
49. 133 Forges CS:2488 (0.83,0.6,0.5) | TD:529 无 | 缺失
50. 302 GlassKiln CS:2488 (0.83,0.6,0.5) | TD:321 [212,153,128]=(0.831,0.6,0.502) | 一致
51. 77 Hellforge CS:2495-2499 (0.75,0.45,0.25) | TD:510 [255,140,70]=(1,0.549,0.275) | 偏差(3)
52. 37 Meteorite CS:2500-2507: n=Next(95,106)*0.01 → (0.56n,0.43n,0.15n) | TD:87 [143,110,38]=(0.561,0.431,0.149) 静态中值 | 偏差(1)：闪烁动态缺
53. 22/140 Demonite CS:2508-2515: 漆非 26/27 → (0.12,0.07,0.32) | TD:86 [255,255,153]=(1,1,0.6) | 偏差(3) / TD:531 无 → 缺失
54. 171 ChristmasTree CS:2517-2575: (frameY&0x3C00)>>10 十档 ×0.5 | TD:544 无 | 缺失
55. 204 Crimtane CS:2576-2581: 漆非 26/27 → R=0.35 | TD:89 [89,0,0]=(0.349,0,0) | 一致（paint 分支缺，注）
56. 347 CrimtaneBrick CS:2576-2581 R=0.35 | TD:611 无 | 缺失
57. 42 HangingLanterns CS:2583-2912: frameX==0; 样式 frameY/36（0..70）; 7/9 demonTorch :2625-2645; default (1,1,1) :2903-2907 | TS:35-60：12 静态档 + 7/9 动态档 + default [0.7,0.65,0.55] | 偏差(2)：default 错（应为 1,1,1）+ 样式 10/12/13/15-70 缺失
58. 49 WaterCandle CS:2913-2920: frameX==0 → (0,0.35,0.8) | TD:149 [140,180,255]=(0.549,0.706,1)+flicker | 偏差(3)：色错 + 多余 flicker（门 ✓）
59. 519 Cattail CS:2921-2937: frameY==90 && 漆0 → (0.1, 0.2+n12, 0.7+n12) | TD:250 [26,51,179]=(0.102,0.2,0.702) 恒亮 | 偏差(2)：frameY==90 门缺 + n12 动态缺
60. 70/71/72/190/348/349/528/578 Mushroom CS:2938-2960: R=0,G=0.2+n11/2,B=1; 349 frameX<36 不发光 | TS:238-243 公式 + LT:90 + TS:219 门 | 一致×8（349 门 ✓）
61. 739 JellyfishBlock CS:2962-2967 (0.35,0.63,0.7)+paint | TD:866 无 | 缺失
62. 350 MartianConduit CS:2968-2972: timeForVisualEffects 余弦脉动 0..0.2 | TD:208 [26,26,26]=0.102 静态 | 偏差(1)：动态缺
63. 61/703 JunglePlants CS:2974-2984: frameX==144 → (0.42*num7, 0.81*num6, 0.52*num7) | TD:431 [107,207,133]=(0.42,0.812,0.522) 恒亮 / TD:835 无 | 偏差(2)：门缺+脉动缺 / 缺失
64. 26/31/695/696 Altars/Orbs CS:2985-3003: 二分支 | TD:254/408 [79,26,112]=(0.31,0.102,0.439) else 分支静态 / TD:827/828 无 | 偏差(2)：n5 闪烁缺+frameX>=54/36 分支缺 ×2 / 缺失×2
65. 699 DeadCells CS:3004 (0.4,0.2,0.15) | TD:831 无 | 缺失
66. 84 BloomingHerbs CS:3009-3042 | TS:81-90 三档 | 一致（style2 clamp ✓ style5 ✓ style6 ✓）
67. 83 MatureHerbs CS:3043-3055: frameX==18&&夜间→(0.1,0.4,0.6); frameX==90&&!rain&&time>40500→(0.9,0.72,0.18) | TD:433 [230,184,46]=(0.902,0.722,0.18) 恒亮 | 偏差(2)：双门缺
68. 126 DiscoBall CS:3057-3064: frameX<36 → Disco/255 | TS:62-67 ✓ + devices ['x',36] ✓ | 一致
69. 125 CrystalBall CS:3065-3072: G=0.3num,B=0.6num (num=Next(28,42)*0.01+(270-mouse)/800) | TD:341 [0,27,54]=(0,0.106,0.212) 静态 | 偏差(1)：动态缺（量级近似 ✓）
70. 129 Crystals CS:3073-3092: frameX/18%3 三档 | TD:308 [0,13,64]=(0,0.051,0.251) 仅档 0 | 偏差(2)：档 1/2 缺
71. 149 HolidayLights CS:3093-3118: frameX<=36; 三色档 ×Next(970,1031)*0.001 | TD:450 [26,51,128]=(0.102,0.2,0.502)+flicker | 偏差(3)：档缺+乘性抖动改加性+门 36→54
72. 160 RainbowBrick CS:3119-3123: Disco×0.25 | TD:541 无 | 缺失
73. 354 BewitchingTable CS:3124-3128 (0.65,0.35,0.15) | TD:298 [166,89,38]=(0.651,0.349,0.149) | 一致
74. 659/667/708 Shimmer 族 CS:659-667 GetShimmerBaseColor | TD:793/800/840 无 | 缺失×3
75. 370 MeteoriteBrick CS:654-658 (0.32,0.16,0.12) | TD:623 无 | 缺失
76. 381/517/687 LavaMoss CS:574-579 (0.25,0.1,0) | TD:190 [255,120,30]=(1,0.471,0.118) / TD:700 无 / TD:819 无 | 偏差(3) / 缺失×2
77. 534/535/689 Krypton CS:581-586 (0,0.25,0) | TD:711/712/821 无 | 缺失×3
78. 536/537/690 Xenon CS:588-593 (0,0.16,0.34) | TD:182 [0,41,87]=(0,0.161,0.341) / TD:713/822 无 | 一致 / 缺失×2
79. 539/540/688 Argon CS:595-600 (0.3,0,0.17) | TD:393 [77,0,43]=(0.302,0,0.169) / TD:715/820 无 | 一致 / 缺失×2
80. 625/626/691 Violet CS:602-607 (0.3,0,0.35) | TD:376 [77,0,89]=(0.302,0,0.349) / TD:767/823 无 | 一致 / 缺失×2
81. 627/628/692 Rainbow(helium) CS:609-614 Disco×0.25 | TD:768/769/824 无 | 缺失×3
82. 184 LongMoss CS:616-653: 6 档 frameX==110..220 | TD:234 [77,0,89]=(0.302,0,0.349) 恒亮 | 偏差(6)：仅 198 档值近似，5 档缺+静态化
83. 711 RainbowBoulder CS:669-672 (0.01,0.01,0.01) | TD:401 [3,3,3]=(0.0118,…) | 一致（≈）
84. 27 Sunflower CS:674-680: frameY<36 → (0.3,0.27,0) | TD:420 [255,242,166]=(1,0.949,0.651) | 偏差(4)：色错+门缺
85. 336 LivingFire CS:681-685 (0.85,0.5,0.3) | TD:602 无 | 缺失
86. 340 CursedFire CS:686-690 (0.45,1,0.45) | TD:385 [115,255,115]=(0.451,1,0.451) | 一致
87. 341 DemonFire CS:691-695 demonTorch 混合 | TD:605 无 | 缺失
88. 342 FrostFire CS:696-700 (0.5,0.5,1.1) | TD:606 无 | 缺失
89. 343 IchorFire CS:701-705 (0.85,0.85,0.3) | TD:607 无 | 缺失
90. 344 UltrabrightFire CS:706-710 (0.6,1.026,0.96) | TD:608 无 | 缺失
91. 327 Lavafall CS:711-720 | TD:596 无 | 缺失
92. 316/317/318 JellyfishJars CS:721-777 双态 | TD:340 [102,26,64]=(0.4,0.102,0.251) / TD:592/593 无 | 偏差(3)：两态皆不符 / 缺失×2
93. 719 RainbowCloud CS:778-861 14 相 | TD:846 无 | 缺失
94. 718 StarCloud CS:862-869 | TD:845 无 | 缺失
95. 717 LavaCloud CS:870-880 | TD:844 无 | 缺失
96. 429 WireBulb CS:881-906 | TS:68-76 | 一致
97. 286/619 CS:907-912 (0.1,0.2,0.7) | TD:579/762 无 | 缺失×2
98. 620 EmpressLacewing CS:913-921 hsl×0.4 | TD:763 无 | 缺失
99. 22/140 already; 
100. tileLighted 无 case: 19/58/76/109/346/684/701 → 原版不发光
101. 本仓多加: TD:140 crystal_heart [255,60,90]（sheet 12, 原版 tileLighted[12]=false）→ 多加; TD:88 ore_hellstone [255,90,40]（sheet 58 有 tileLighted 但无 case）→ 多加

Counts: let me tally 一致/偏差/缺失.
一致: 634, 633, 637, 638, 463, 491, 302, 613, 614, 372, 174(偏差 flicker→not), hmm let me count at the end. Let me count 一致: 
1. 634 ✓
2. 633 ✓
3. 637 ✓
4. 638 ✓
5. 463 ✓
6. 491 ✓
7. 302 ✓
8. 613 ✓
9. 614 ✓
10. 372 ✓
11. 237 ✓
12. 204 ✓（近似）
13. 蘑菇组 8 ✓
14. 84 ✓
15. 126 ✓
16. 354 ✓
17. 536 ✓
18. 539 ✓
19. 625 ✓
20. 711 ✓
21. 340 ✓
22. 429 ✓
→ 22 条一致（含组内计数：633/637/638 分开算则 +2 = 24? I listed them separately: 633,637,638 are 3 → my list has them as #2,3,4. And 蘑菇组 8 条算 8. Let me just say 约 24 条完全一致.

偏差: 356, 656, 209, 597, 564, 598, 405, 215, 92, 592, 593, 594, 548, 93, 98, 4, 33, 174, 100, 173, 34, 35, 95, 17, 77, 37, 22, 42, 49, 519, 350, 61, 26, 31, 83, 125, 129, 149, 381, 184, 27, 316 → 约 42 条偏差.

缺失: 658, 663, 20, 415, 416, 417, 418, 500, 501, 502, 503, 390, 568, 569, 570, 580, 391, 582, 270, 271, 581, 660, 572, 262-268(7), 238, 235, 96, 646, 171, 140, 347, 703, 695, 696, 699, 659, 667, 708, 370, 517, 687, 534, 535, 689, 537, 690, 540, 688, 626, 691, 627, 628, 692, 336, 341, 342, 343, 344, 327, 317, 318, 719, 718, 717, 286, 619, 620 → 约 66 条缺失.

Total ≈ 24 + 42 + 66 = 132 ≈ 130 case 总数 ✓ good.

Now write the report. I'll keep entries compact. Also add systemic findings subsection at end of section 1:
S1. FLICKER_SHEETS (LT:87) 15 个 sheet 中 11 个属多加闪烁（原版只有 405/215/592 三处加性闪烁）;592 反而漏加。
S2. def.light 逐格应用于 framed 多格物体 → 原版按帧条件逐格门控(92 仅顶格/98 仅顶行/96 仅右列/592 frameY>0 等)。
S3. 多加光源 2 条: TD:140 (sheet 12), TD:88 (sheet 58)。
S4. tileLighted 表未对应: repo 无门禁,靠 def.light 存在性;原版 7 个 tileLighted-but-no-case 的 tile(19/58/76/109/346/684/701)中 repo 只有 58 误发光。
S5. 接线灯 LIGHT_TOGGLE (devices:522-537) 的模周期门对 4/33/42/49/92/93/95/100/126/173/174/215/34/372/564/149 与原版 frameX 门等效 ✓ (但 35/593/594/548/646/96/98/592 未注册)。

Section 2: WALL_EMISSIVE 21 条 + structural:
- 门: CS !LightIsBlocked (= active && tileBlockLight, CS:154-163) vs TS:190 `wall!==0 && st.type[i]===0` → 偏差：宝石墙 153-166 原版无门(CS:248-273 无 LightIsBlocked),恒发光;且所有墙在非挡光 tile(平台/火把/家具)前原版仍发光,本仓不发光。
- paint 覆盖: CS:323-329 (flag 墙 357/175 paintColor/765) 本仓无 → 偏差。
- 彩玻染色: CS:3190-3242 / :3286-3310 乘法改写天光/地狱光 vs TS:195-210 max 合成 + type===0 门 + 彩虹档常数错(0.7+0.2d 应为 0.5+0.2d, CS:3229-3233 num10=0.7-num9=0.5) → 偏差(3): 夜间彩玻墙自发光(原版夜间为 0)、常数错、门严。
- 44/137/346 动态项缺失(静态化)。

Section 3: TORCH_COLORS 24 条逐值 + 7/14/23 动态 + 1.4.5 无新增(Count=24, TorchID.cs:132) + 火把多余 flicker + shimmerTorchColor 公式错。

Section 4: 
- 岩浆: CS:116-132 vs TS:164/262-264 → 公式一致(值域 lavaV∈[0.567,0.639]) 但合成语义偏差: 原版 Y/Z 阈值用 num 而非 num*0.6/0.2 → 可下调既有光;本仓纯 max 只升不降。
- 微光: CS:133-151 → TS 无 → 缺失。给出值域: X=num2*0.6∈[0.430,0.473], Y=num3*0.25∈[0.205,0.335], Z=num2*0.9∈[0.645,0.710]。
- 地狱: CS:3266 num4=0.55+sin(GlobalTimeWrappedHourly*2)*0.08; GlobalTimeWrappedHourly=TotalSeconds%3600 (Main.cs:16777) → sin(2*秒)。TS:161 performance.now()*0.002=2*秒 → 一致(仅 3600s 环绕跳变)。
- 地狱/天光墙门: CS:3170/3286 `wallLight||wall==73||wall==227||invisibleWall` vs TS:152 `wall===0||WALL_LIGHT.has(wall)` → 缺 73(云墙)/227(降雪墙)/回声墙涂层。
- 表层满液 B 微光 CS:3181-3188 liquidAlpha[13] → 原版死代码(liquidAlpha[13] 恒 0, Main.cs:56846-56858 只抬 waterStyle≤12) → 不实现无影响。
- shimmerDarken 乘子 CS:3243-3246 → 归天空光一路(未在本仓扫描器,未见实现)。

Section 5: WALL_LIGHT 16 vs 15+0 特判 → 全表一致;补 73/227 特例缺失(同第四节)。

I think that's complete. Let me write it now. Keep it tight but complete. No code blocks; inline values.

For brevity in section 1, I'll use a compact notation: `CS:394 (0.200,0.550,0.500) | TD:348 (1.000,0.725,0.431) | 偏差(3)`.

Also define abbreviations at top so paths stay absolute once.

One more consideration: the user's task item 1 said "特别核对发光条件（灯笼 frameX!=0 不发光、灯泡 frameX 位段、迪斯科球动态色）" — I'll make sure those three are explicitly called out as 一致.

Let me now write the final answer. It'll be long; that's expected for "very thorough". I'll aim for density.
```

</details>


---

## 🤖 Assistant · 2026-08-13T06:33:30.039Z · glm-x-preview-260804

```
# 发光物光源全量对账 · 第一路：tile / 墙 / 液体光源

文件缩写（均为绝对路径）：
- **CS** = ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Graphics.Light/TileLightScanner.cs
- **TorchID** = ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TorchID.cs
- **Main** = ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs
- **TS** = ~/Project/GLM/SandboxWorld/game/src/lighting/TileLightScanner.ts
- **LT** = ~/Project/GLM/SandboxWorld/game/src/lighting/lightTables.ts
- **TD** = ~/Project/GLM/SandboxWorld/game/src/data/tiles.ts
- **SC** = ~/Project/GLM/SandboxWorld/game/src/lighting/SkyColor.ts
- **DEV** = ~/Project/GLM/SandboxWorld/game/src/world/wiring/devices.ts

前置事实：原版 `ApplyTileLight`（CS:344-3150）顶层 case 共 130 个 tile 类型；`Main.tileLighted[]` 共 147 处置位，其中 19/58/76/109/346/684/701 七项**有 tileLighted 但 switch 无 case**（即原版不发光）。12（Heart）连 tileLighted 都没有。

---

## 第一节 静态 tile 光源覆盖率（CS ApplyTileLight 全量 case）

### 1.1 逐条对账（按原版 switch 顺序）

**A. 特殊/动态组**
| 条目 | 原版 | 本仓 | 判定 |
|---|---|---|---|
| 658 ShimmerMonolith | CS:354-377：!invisibleBlock → TorchColor(23)×(frameY/54 档 0.2/0.3/0.1) | TD:792 无 light，TS specialTileLight 无 case | **缺失** |
| 356 Sundial | CS:378-385：sundialCooldown==0 → (0.450,0.250,0) | TD:334 [115,64,0]=(0.451,0.251,0.000) | **偏差(1)**：cooldown 门缺失 |
| 663 Moondial | CS:386-393：moondialCooldown==0 → (0,0.250,0.450) | TD:797 无 | **缺失** |
| 656 GlowTulip | CS:394-397：(0.200,0.550,0.500) | TD:348 [255,185,110]=(1.000,0.725,0.431) | **偏差(3)** |
| 20 Saplings | CS:399-408：frameX/18∈30..32 → (0.325,0.150,0.050) | TD:74（acorn_sapling，sheet 20）无 | **缺失** |
| 209 Cannon 传送门炮 | CS:432-447：frameX 234/252 → GetPortalColor(p,0)×0.65=(0.650,0.306,0)；frameX 306/324 → portal1×0.65=(0.130,0.588,0.650) | TS:77-80 硬编码 [0.42,0.20,0.65] / [0.65,0.26,0] | **偏差(2)**：两档色值皆错（portal0 应为橙、portal1 应为青，本仓写反色调） |

**B. 灰烬/丛林/杂项**
| 条目 | 原版 | 本仓 | 判定 |
|---|---|---|---|
| 634 TreeAsh | CS:410 (0.650,0.300,0.100) | TD:252 [166,77,26]=(0.651,0.302,0.102) | **一致** |
| 633 AshGrass / 637 AshPlants / 638 AshVines | CS:415-421 (0.325,0.150,0.050) | TD:178 / 247 / 354 均 [83,38,13]=(0.325,0.149,0.051) | **一致 ×3** |
| 463 DefendersForge | CS:422 (0.200,0.400,0.800) | TD:155 [51,102,204]=(0.200,0.400,0.800) | **一致** |
| 491 VoidVault | CS:427 (0.500,0.400,0.700) | TD:324 [128,102,179]=(0.502,0.400,0.702) | **一致** |
| 415-418 四色月亮碎片块 | CS:448-482：(0.700,0.500,0.100)/(0,0.600,0.700)/(0.600,0.200,0.600)/(0.600,0.600,0.900) | TD:640-643 均无 | **缺失 ×4** |
| 500-503 四色月亮砖 | CS:453-487：(0.525,0.375,0.075)/(0,0.450,0.525)/(0.450,0.150,0.450)/(0.450,0.450,0.675) | TD:685-688 均无 | **缺失 ×4** |
| 390 LavaLamp | CS:488 (0.400,0.200,0.100) | TD:625 无 | **缺失** |
| 597 Pylon | CS:493-540：8 样式（frameX/54）末统一 ×0.75；style0=(0.038,0.600,0.225) | TD:282 [13,204,77]=(0.051,0.800,0.302)，未乘 0.75，仅 style0 | **偏差(2)** |
| 564 PlasmaLamp | CS:541-547：frameX<36 → (0.050,0.300,0.550) | TD:500 [13,77,140]=(0.051,0.302,0.549)；LT:87 FLICKER 含 564 | **偏差(2)**：门（DEV ['x',36]）等效 ✓，但多加原版没有的闪烁 |
| 568/569/570 仙女罐 | CS:549-563：(1,0.610,0.650)/(0.120,1,0.660)/(0.570,0.570,1) | TD:734-736 均无 | **缺失 ×3** |
| 580 HellButterflyJar | CS:564 (0.700,0.300,0.200) | TD:740 无 | **缺失** |
| 391 CageEnchantedNightcrawler | CS:569 (0.300,0.100,0.250) | TD:626 无 | **缺失** |
| 582 MagmaSnailCage / 598 LavafishBowl | CS:922-927 (0.700,0.200,0.100) | TD:742 无 / TD:317 [255,185,110]=(1.000,0.725,0.431) | **缺失** / **偏差(3)** |
| 270 FireflyBottle | CS:928 (0.730,1.000,0.410) | TD:566 无 | **缺失** |
| 271 LightningBugBottle | CS:933 (0.450,0.950,1.000) | TD:567 无 | **缺失** |
| 581 LavaflyBottle | CS:938 (1.000,0.750,0.500) | TD:741 无 | **缺失** |
| 660 FaelingBottle | CS:943 TorchColor(23) | TD:794 无 | **缺失** |
| 572 SoulBottles | CS:946-980：frameY/36 六档 (0.900,0.500,0.700)/(0.700,0.550,0.960)/(0.450,0.960,0.950)/(0.500,0.960,0.620)/(0.470,0.690,0.950)/(0.920,0.570,0.510) | TD:737 无 | **缺失** |
| 262-268 Gemspark 七色 | CS:981-1006：262 (0.750,0,0.750)；263 (0.750,0.750,0)；264 (0,0,0.750)；265 (0,0.750,0)；266 (0.750,0,0)；267 (0.750,0.750,0.750)；268 (0.750,0.375,0) | TD:465-471 均无 | **缺失 ×7** |

**C. 灯具大族（本仓问题最集中区域）**

| 条目 | 原版 | 本仓 | 判定 |
|---|---|---|---|
| 237 LihzahrdAltar | CS:1007-1009 (0.100,0.100,0) | TD:336 [26,26,0]=(0.102,0.102,0) | **一致** |
| 238 PlanteraBulb | CS:1011-1019：抬 X/Z 至 0.500（条件合成） | TD:557 无 | **缺失** |
| 235 Teleporter | CS:1021-1028：抬 X/Y 至 0.600 | TD:350 无 | **缺失** |
| 405 Fireplace | CS:1031-1073：门 frameX<54（仅左列 1 格）；闪烁 num27=Next(28,42)×0.005+(270-mouse)/700；样式 frameX/54，default (0.900,0.300,0.100) | TD:331 [255,185,110]=(1.000,0.725,0.431) 全 6 格 + LT:87 闪烁 | **偏差(3)**：色错、frameX<54 门缺、样式缺（闪烁 ✓） |
| 215 Campfire | CS:1074-1164：门 frameY<36（仅顶行 3 格）；16 样式，default (0.900,0.300,0.100)+num26 闪烁 | TD:280 [255,185,110] 全 6 格 + 闪烁；DEV ['y',36] 门 ✓ | **偏差(3)**：色错、样式缺（闪烁 ✓ 门 ✓） |
| 92 Lampposts | CS:1165-1172：门 **frameY<=18 且 frameX==0**（仅顶部 1 格）→ (1,1,1) | TD:444 [255,255,255] 全 6 格 + LT:87 闪烁 | **偏差(3)**：frameY<=18 门缺（6 格全亮 vs 1 格）、多余闪烁 |
| 592 BrazierSuspended | CS:1173-1185：门 frameY>0 → (1.350,0.450,0.150)+num25 闪烁 | TD:283 [255,185,110]=(1.000,0.725,0.431) 静态恒亮 | **偏差(4)**：色错、闪烁缺、frameY>0 门缺 |
| 593 VolcanoSmall / 594 VolcanoLarge | CS:1186-1201：门 frameX<18 / frameX<36 → (0.800,0.300,0.100) | TD:502/503 均 [204,77,26]=(0.800,0.302,0.102)，无门 | **偏差(1) ×2**（仅门缺） |
| 548 PottedTrees2 | CS:1202-1208：门 frameX/54>=7 → (0.700,0.300,0.200) | TD:315 [179,77,51]=(0.702,0.302,0.200) 无门 | **偏差(1)**（样式 0-6 也发光） |
| 613/614 PottedLavaPlants | CS:1210-1215 无门 (0.700,0.300,0.200) | TD:304/316 均 [179,77,51] | **一致 ×2** |
| 93 Lamps | CS:1216-1519：门 frameX==0；样式 frameY/54；default (1.000,0.970,0.850)；含 demonTorch 样式（CS:1307-1309）与 hsl 彩轮样式（CS:1338） | TD:261 [255,185,110]=(1.000,0.725,0.431) + LT:87 闪烁；DEV ['x',18] ✓ | **偏差(4)**：色错、样式缺、多余闪烁 |
| 96 CookingPots | CS:1520-1527：门 **frameX>=36**（仅右列）→ (0.500,0.350,0.100) | TD:137（cooking_pot）无 | **缺失** |
| 98 SkullLanterns | CS:1528-1535：门 frameY==0（仅顶行）→ (1.000,0.970,0.850) | TD:148 [255,160,70]=(1.000,0.627,0.275) 全 4 格 | **偏差(3)**：色错、frameY==0 门缺 |
| 4 Torch | CS:1537-1541：门 frameX<66 → TorchColor(frameY/22)（无闪烁） | TS:225-237 TORCH_COLORS + style 7/14/23 动态 + :236-237 加闪烁；DEV ['x',66] ✓ | **偏差(1)**：色表与门一致，但多加原版没有的闪烁 |
| 372 PeaceCandle | CS:1542-1549：门 frameX==0 → (0.900,0.100,0.750) | TD:474 [230,26,191]=(0.902,0.102,0.749)；DEV ['x',18] ✓ | **一致** |
| 646 ShadowCandle | CS:1550-1557：门 frameX==0 → (0.200,0.300,0.320) | TD:781 无 | **缺失** |
| 33 Candles | CS:1558-1851：门 frameX==0；样式 frameY/22；default (1.000,0.950,0.650)；demonTorch 样式 CS:1654-1656；hsl 彩轮 CS:1670 | TD:142 [255,185,110]=(1.000,0.725,0.431) + LT:87 闪烁；DEV ['x',18] ✓ | **偏差(4)** |
| 174 PlatinumCandle | CS:1852-1859：门 frameX==0 → (1.000,0.950,0.650) | TD:452 [255,242,166]=(1.000,0.949,0.651) + LT:87 闪烁 | **偏差(1)**：值一致，多余闪烁 |
| 100/173 Candelabras | CS:1860-2164：门 frameX<36；样式 frameY/36；default (1.000,0.950,0.650)；demon CS:1952、hsl CS:1983 | TD:146 [255,185,110]=(1.000,0.725,0.431)+闪烁；TD:451 [255,242,166]+闪烁；DEV ['x',36] ✓ | **偏差(4)** / **偏差(3)**（173 基值 ✓ 但样式缺+多余闪烁） |
| 34 Chandeliers | CS:2165-2471：门 frameX%108<54（左+右列发光，中列不发光）；样式 frameY/54+37×(frameX/108)；default (1,1,1)；demon CS:2273、hsl CS:2289 | TD:143 [255,190,120]=(1.000,0.745,0.471)+闪烁；DEV ['x',54] ✓（列级门 ✓） | **偏差(4)** |
| 35 Jackolanterns | CS:2472-2479：门 frameX<36 → (0.750,0.600,0.300) | TD:443 [179,153,230]=(0.702,0.600,0.902)，未注册 LIGHT_TOGGLE | **偏差(3)**：R/B 错、门缺（灭档仍发光） |
| 95 ChineseLanterns | CS:2480-2487：门 frameX<36 → (1.000,0.950,0.800) | TD:147 [255,160,70]=(1.000,0.627,0.275)+LT:87 闪烁；DEV ['x',36] ✓ | **偏差(3)**：G/B 错、多余闪烁 |
| 42 HangingLanterns（重点核对项） | CS:2583-2912：门 **frameX!=0 不发光**（CS:2584-2587）✓；样式 frameY/36 覆盖 0..70；style7 CS:2625-2632 R=G=0.9-0.2d、B=0.7+0.2d；style9 CS:2638-2645 R=1-0.1d、G=0.3-0.2d、B=0.5+0.2d；**default (1,1,1)**（CS:2903-2907） | TS:35-60：frameX!==0→null ✓；12 静态档值逐一相等 ✓；style7/9 动态公式 ✓；**default 兜底 [0.7,0.65,0.55]**；样式 10/12/13/15-70 全缺 | **偏差(2)**：default 应为 (1,1,1)、约 55 个样式档缺失（落进错误兜底） |
| 49 WaterCandle | CS:2913-2920：门 frameX==0 → (0,0.350,0.800) | TD:149 [140,180,255]=(0.549,0.706,1.000)+LT:87 闪烁；DEV ['x',18] ✓ | **偏差(3)**：色错、多余闪烁 |
| 519 Cattail | CS:2921-2937：门 frameY==90 且漆==0 → (0.100, 0.200+n12, 0.700+n12)，n12=Next(28,42)×0.005+(270-mouse)/1000 | TD:250 [26,51,179]=(0.102,0.200,0.702) 恒亮 | **偏差(2)**：frameY==90 门缺、n12 动态缺 |
| 蘑菇组 70/71/72/190/348/349/528/578 | CS:2938-2960：R=0、G=0.2+n11/2、B=1，n11=Next(28,42)×0.005+(270-mouse)/1000；**349 门 frameX<36 不发光**（CS:2940） | TS:238-243 公式 ✓ + LT:90 八表 ✓ + TS:219 的 349 门 ✓（并正确压制 def.light 兜底） | **一致 ×8**（含门禁） |

**D. 矿石/苔藓/火族**
| 条目 | 原版 | 本仓 | 判定 |
|---|---|---|---|
| 17 Furnace | CS:2488-2492 (0.830,0.600,0.500) | TD:64 [255,140,70]=(1.000,0.549,0.275) | **偏差(3)** |
| 133 Forges（精金熔炉） | CS:2488 (0.830,0.600,0.500) | TD:529 无 | **缺失** |
| 302 GlassKiln | CS:2488 (0.830,0.600,0.500) | TD:321 [212,153,128]=(0.831,0.600,0.502) | **一致** |
| 77 Hellforge | CS:2495-2499 (0.750,0.450,0.250) | TD:510 [255,140,70]=(1.000,0.549,0.275) | **偏差(3)** |
| 37 Meteorite | CS:2500-2507：n=Next(95,106)×0.01 → (0.56n,0.43n,0.15n) | TD:87 [143,110,38]=(0.561,0.431,0.149) 静态中值 | **偏差(1)**：闪烁动态缺 |
| 22 Demonite | CS:2508-2515：漆非 26/27 → (0.120,0.070,0.320) | TD:86 [255,255,153]=(1.000,1.000,0.600) | **偏差(3)**（严重：色相完全不同） |
| 140 DemoniteBrick | CS:2508 (0.120,0.070,0.320) | TD:531 无 | **缺失** |
| 171 ChristmasTree | CS:2517-2575：(frameY&0x3C00)>>10 十档灯串色 ×0.5 | TD:544 无 | **缺失** |
| 204 Crimtane | CS:2576-2581：漆非 26/27 → R=0.350 | TD:89 [89,0,0]=(0.349,0,0) | **一致**（paint 分支缺，影响极小） |
| 347 CrimtaneBrick | CS:2576 R=0.350 | TD:611 无 | **缺失** |
| 381/517/687 LavaMoss 族 | CS:574-579 (0.250,0.100,0) | TD:190 [255,120,30]=(1.000,0.471,0.118) / TD:700 无 / TD:819 无 | **偏差(3)** / **缺失 ×2** |
| 534/535/689 KryptonMoss | CS:581-586 (0,0.250,0) | TD:711/712/821 无 | **缺失 ×3** |
| 536/537/690 XenonMoss | CS:588-593 (0,0.160,0.340) | TD:182 [0,41,87]=(0,0.161,0.341) / TD:713、822 无 | **一致** / **缺失 ×2** |
| 539/540/688 ArgonMoss | CS:595-600 (0.300,0,0.170) | TD:393 [77,0,43]=(0.302,0,0.169) / TD:715、820 无 | **一致** / **缺失 ×2** |
| 625/626/691 VioletMoss | CS:602-607 (0.300,0,0.350) | TD:376 [77,0,89]=(0.302,0,0.349) / TD:767、823 无 | **一致** / **缺失 ×2** |
| 627/628/692 Helium(Rainbow)Moss | CS:609-614：Disco×0.25 | TD:768/769/824 无 | **缺失 ×3** |
| 184 LongMoss | CS:616-653：六档 frameX==110/132/154/176/198/220 → (0.25,0.1,0)/(0,0.25,0)/(0,0.16,0.34)/(0.3,0,0.17)/(0.3,0,0.35)/Disco×0.25 | TD:234 [77,0,89]=(0.302,0,0.349) 恒亮 | **偏差(6)**：仅 198 档近似，其余 5 档缺失且静态化 |
| 370 MeteoriteBrick | CS:654-658 (0.320,0.160,0.120) | TD:623 无 | **缺失** |
| 659/667/708 Shimmer 族 | CS:659-667：GetShimmerBaseColor(x,y) | TD:793/800/840 无 | **缺失 ×3** |
| 711 RainbowBoulder | CS:669-672 (0.010,0.010,0.010) | TD:401 [3,3,3]=(0.012,0.012,0.012) | **一致（≈）** |
| 27 Sunflower | CS:674-680：门 frameY<36 → (0.300,0.270,0) | TD:420 [255,242,166]=(1.000,0.949,0.651) 恒亮 | **偏差(4)**：色错、门缺 |
| 336 LivingFire | CS:681-685 (0.850,0.500,0.300) | TD:602 无 | **缺失** |
| 340 LivingCursedFire | CS:686-690 (0.450,1.000,0.450) | TD:385 [115,255,115]=(0.451,1.000,0.451) | **一致** |
| 341 LivingDemonFire | CS:691-695：R=0.4d+0.6(1-d)、G=0.35、B=1d+0.6(1-d) | TD:605 无 | **缺失** |
| 342 LivingFrostFire | CS:696-700 (0.500,0.500,1.100) | TD:606 无 | **缺失** |
| 343 LivingIchorFire | CS:701-705 (0.850,0.850,0.300) | TD:607 无 | **缺失** |
| 344 LivingUltrabrightFire | CS:706-710 (0.600,1.026,0.960) | TD:608 无 | **缺失** |
| 327 Lavafall | CS:711-720：n=0.5+(270-mouse)/1500+Next(0,50)×0.0005 → (n,0.5n,0.1n) | TD:596 无 | **缺失** |

**E. 罐/云/杂项**
| 条目 | 原版 | 本仓 | 判定 |
|---|---|---|---|
| 316/317/318 水母罐 | CS:721-777：双态（jellyfishCageMode）：316 (0.200,0.300,0.800)/(0.100,0.200,0.500)；317 (0.200,0.700,0.300)/(0.050,0.450,0.100)；318 (0.700,0.200,0.500)/(0.400,0.100,0.250) | TD:340 [102,26,64]=(0.400,0.102,0.251)（两态皆不符）；TD:592/593 无 | **偏差(3)** / **缺失 ×2** |
| 719 RainbowCloud | CS:778-861：14 相色轮（(x+y+GlobalTimeWrappedHourly×15)%14） | TD:846 无 | **缺失** |
| 718 StarCloud | CS:862-869：门 !dayTime 且上方非实心 → (0.1+rand×0.04+Disco/800)×3 | TD:845 无 | **缺失** |
| 717 LavaCloud | CS:870-880：n=(0.55+(270-mouse)/800+rand×0.03)×0.5 → (1.1n,0.4n,0.1n) | TD:844 无 | **缺失** |
| 429 WireBulb（重点核对项） | CS:881-906：n=frameX/18；bit0→R+0.5、bit1→G+0.5、bit2→B+0.5、bit3→R+0.2 且 G+0.2 | TS:68-76 逐位一致 | **一致**（位段语义 ✓） |
| 286 GlowingSnailCage / 619 TruffleWormCage | CS:907-912 (0.100,0.200,0.700) | TD:579/762 无 | **缺失 ×2** |
| 620 EmpressLacewingJar | CS:913-921：hsl(GlobalTimeWrappedHourly×0.5%1,1,0.5)×0.4 | TD:763 无 | **缺失** |
| 739 JellyfishBlock | CS:2962-2967 (0.350,0.630,0.700)+paint flag | TD:866 无 | **缺失** |
| 350 MartianConduitPlating | CS:2968-2972：timeForVisualEffects 余弦脉动 0..0.2 | TD:208 [26,26,26]=0.102 静态 | **偏差(1)**：动态缺 |
| 61/703 JunglePlants | CS:2974-2984：门 frameX==144 → (0.42×num7, 0.81×num6, 0.52×num7) | TD:431 [107,207,133]=(0.420,0.812,0.522) 恒亮（未乘 num6/num7）/ TD:835 无 | **偏差(2)** / **缺失** |
| 26/31/695/696 祭坛/暗影珠 | CS:2985-3003：二分支——frameX>=54(26/695) 或 >=36(31/696) → (0.5+2n4,0.2+n4,0.1)；else → (0.31+n5,0.1,0.44+2n5) | TD:254、408 均 [79,26,112]=(0.310,0.102,0.439)（仅 else 分支中值）；TD:827/828 无 | **偏差(2) ×2**：n5 闪烁缺、第二分支缺 |
| 699 DeadCellsPotionStation | CS:3004 (0.400,0.200,0.150) | TD:831 无 | **缺失** |
| 84 BloomingHerbs（重点核对项） | CS:3009-3042：style2 死亡草 num3=clamp((270-mouse)/400,0,1)→(1.4n,1.2n,n/2)；style5 火焰草 (0.900,0.720,0.180)；style6 颤骨草 (0,0.064,0.080) | TS:81-90 三档逐一相等（含 clamp） | **一致** |
| 83 MatureHerbs | CS:3043-3055：frameX==18 且夜间 → (0.100,0.400,0.600)；frameX==90 且非雨且 time>40500 → (0.900,0.720,0.180) | TD:433 [230,184,46]=(0.902,0.722,0.180) 恒亮 | **偏差(2)**：双门禁全缺 |
| 126 DiscoBall（重点核对项） | CS:3057-3064：门 frameX<36 → (DiscoR/255,DiscoG/255,DiscoB/255) | TS:62-67 + SC:148-150 discoColor ✓ + DEV ['x',36] ✓ | **一致**（动态色 ✓ 门 ✓） |
| 125 CrystalBall | CS:3065-3072：G=0.3×num、B=0.6×num，num=Next(28,42)×0.01+(270-mouse)/800 → G∈[0.084,0.132]、B∈[0.168,0.264] | TD:341 [0,27,54]=(0,0.106,0.212) 静态中值 | **偏差(1)**：动态缺（量级近似 ✓） |
| 129 Crystals | CS:3073-3092：frameX/18%3 三档 (0,0.050,0.250)/(0.200,0,0.150)/(0.100,0,0.200) | TD:308 [0,13,64]=(0,0.051,0.251) 仅档 0 | **偏差(2)**：档 1/2 缺 |
| 149 HolidayLights | CS:3093-3118：门 frameX<=36；三色档 ×Next(970,1031)×0.001（乘性抖动） | TD:450 [26,51,128]=(0.102,0.200,0.502) + LT:87 加性闪烁；DEV ['x',54] | **偏差(3)**：档缺、乘性抖动改成加性闪烁、门 36 放宽为 54 |
| 160 RainbowBrick | CS:3119-3123：Disco×0.25 | TD:541 无 | **缺失** |
| 354 BewitchingTable | CS:3124-3128 (0.650,0.350,0.150) | TD:298 [166,89,38]=(0.651,0.349,0.149) | **一致** |

**F. 原版不发光项（tileLighted 但无 case）与本仓多加项**
- 19 Platforms / 58 Hellstone / 76 HellstoneBrick / 109 HallowedGrass / 346 ChlorophyteBrick / 684 AncientHellstoneBrick / 701 GlowTulipReplica：CS 无 case → 原版 0 光。本仓 TD 均无 light → **一致（7/7 正确）**
- **多加 1**：TD:140 `crystal_heart`（sheet 12）light [255,60,90]=(1.000,0.235,0.353)——原版 tileLighted[12]=false 且无 case，生命水晶发光走绘制层 glow mask，不走光照 → **非原版光源，应移除**
- **多加 2**：TD:88 `ore_hellstone`（sheet 58）light [255,90,40]=(1.000,0.353,0.157)——58 有 tileLighted 但 ApplyTileLight 无 case → 原版狱石不发光 → **非原版光源，应移除**

### 1.2 第一节结构性问题（影响面大于单条）
1. **FLICKER_SHEETS（LT:87）系统性错位**：集合含 {4,33,49,92,93,174,34,149,95,100,126,173,564,215,405} 15 项，但原版全文件只有 3 处加性闪烁 `Next(28,42)×0.005+(270-mouse)/700`：405（CS:1032-1033）、215（CS:1075-1076）、592（CS:1174-1175）。本仓对 **11 个不该闪的 sheet**（4/33/49/92/93/174/34/149/95/100/173/564）加了闪烁，**唯独该闪的 592 没加**（592 不在集合且无实现）。闪烁公式本身 TS:236/247 与原版逐字一致。
2. **def.light 逐格播撒 vs 原版逐格帧门控**：framed 多格物体在 TS 中每格都吃同一 def.light（TS:220-251），而原版按帧条件只让部分格发光：92 仅顶格（frameY<=18）、98 仅顶行（frameY==0）、96 仅右列（frameX>=36）、592 仅 frameY>0、129/548/61/26/31/83/27/20/238/235 均有状态门。造成整体光斑偏大。
3. **LIGHT_TOGGLE（DEV:522-537）已覆盖的开关门等效 ✓**：4(frameX<66)/33,174,49,372,42,92,93(frameX==0 等效)/95,100,126,173,564(frameX<36 等效)/34,149(frameX%108<54)/215(frameY<36) 与原版帧门语义一致（含 chandelier 中列不发光的列级效果）。未注册的：35/96/98/592/593/594/548/646/129/61/26/31/83/27/20。
4. **覆盖率统计**（130 个原版发光 tile 类型）：完全一致约 24 条（含蘑菇组 8 条与 42 的门禁/动态档）、偏差约 42 条、缺失约 66 条；另有 2 条多加。一致项集中于：蘑菇组、灰烬组、634/463/491/302/613/614/237/204/354/340/711/536/539/625/372/84/429/126 与灯笼 42 的 12 个静态档+7/9 动态档。

---

## 第二节 发光墙 WALL_EMISSIVE 全表（CS ApplyWallLight :167-342 vs LT:93-115）

原版共 **21** 个墙 case；本仓 WALL_EMISSIVE 也为 21 条，id 全对齐（无缺表项），但数值偏差集中在宝石灯墙组（本仓注释的宝石名与 id 错位一档，导致取值连锁错）。

| 墙 id | 原版（CS 行号 + 值） | 本仓（LT 行号 + 值） | 判定 |
|---|---|---|---|
| 357 水母墙 | CS:175-182 (0.150,0.270,0.300) + paint flag | LT:114 [0.15,0.27,0.3] | 一致（paint 分支缺，见结构 3） |
| 182 陨石砖墙 | CS:184-190 (0.240,0.120,0.090) | LT:107 [0.24,0.12,0.09] | **一致** |
| 33 恶魔砖墙 | CS:192-198 (0.090,0.053,0.240) | LT:94 [0.09,0.0525,0.24] | **一致** |
| 174 猩红砖墙 | CS:200-204 R=0.298（G=B=0） | LT:104 [0.2975,0,0] | **一致** |
| 175 蘑菇护板墙 | CS:206-219：wallColor==0 → (0.075,0.150,0.400)；否则走 paint | LT:105 [0.075,0.15,0.4] | 偏差(1)：paint 分支缺 |
| 176 火星导管墙 | CS:221-227 (0.100,0.100,0.100) | LT:106 [0.1,0.1,0.1] | **一致** |
| 137 岩浆瀑布墙 | CS:229-238：n=0.4+(270-mouse)/1500+Next(0,50)×0.0005 → (n,0.5n,0.1n)，R∈[0.410,0.478] | LT:96 [0.5,0.25,0.05] 静态 | 偏差(2)：动态项缺、基值偏高 |
| 44 彩虹砖墙 | CS:240-246：Disco×0.15 | LT:95 [0.15,0.15,0.15] 静态 | 偏差(1)：动态缺 |
| 153 Amber 宝石灯墙 | CS:270-273 **(0.600,0.300,0)**（无 LightIsBlocked 门） | LT:97 [0.6,0.12,0.6]（注释误标紫水晶） | **偏差(3)** |
| 154 Amethyst 宝石灯墙 | CS:248-251 (0.600,0,0.600) | LT:98 [0.6,0.12,0.6] | **偏差(1)**（G 多 0.12） |
| 155 Diamond 宝石灯墙 | CS:265-268 (0.600,0.600,0.600) | LT:99 [0.6,0.42,0.06]（注释误标琥珀） | **偏差(2)** |
| 156 Emerald 宝石灯墙 | CS:259-261 (0,0.600,0) | LT:100 [0.09,0.6,0.24] | **偏差(2)** |
| 164 Ruby 宝石灯墙 | CS:262-264 (0.600,0,0) | LT:101 [0.09,0.24,0.6]（注释误标蓝宝石） | **偏差(3)** |
| 165 Sapphire 宝石灯墙 | CS:256-258 (0,0,0.600) | LT:102 [0.6,0.06,0.09]（注释误标红宝石） | **偏差(3)** |
| 166 Topaz 宝石灯墙 | CS:252-255 (0.600,0.600,0) | LT:103 [0.42,0.42,0.6]（注释误标钻石） | **偏差(1)**（B 应为 0） |
| 341 熔岩苔墙 | CS:274-280 (0.250,0.100,0) | LT:108 [0.25,0.1,0] | **一致** |
| 342 氩苔墙 | CS:298-304 (0.300,0,0.170) | LT:109 [0.3,0,0.17] | **一致** |
| 343 氪苔墙 | CS:282-288 (0,0.250,0) | LT:110 [0,0.25,0] | **一致** |
| 344 氙苔墙 | CS:290-296 (0,0.160,0.340) | LT:111 [0,0.16,0.34] | **一致** |
| 345 紫罗兰苔墙 | CS:306-312 (0.300,0,0.350) | LT:112 [0.3,0,0.35] | **一致** |
| 346 彩虹苔墙 | CS:314-320：Disco×0.25 | LT:113 [0.25,0.25,0.25] 静态 | 偏差(1)：动态缺 |

**结构判定（全表级）**
1. **门禁偏差**：原版墙发光门为 `!LightIsBlocked(tile)`（CS:154-163 = `tile.active() && Main.tileBlockLight[type]`，回声涂层另有特例），本仓为 TS:190 `wall!==0 && st.type[i]===0`。差异有二：(a) 宝石灯墙 153-166 原版**完全没有** LightIsBlocked 门（CS:248-273），即被实心块盖住也恒发光；本仓统一要求空气格 → 宝石灯墙被方块挡住时熄灭。(b) 所有 21 墙在非挡光 tile（平台/火把/家具/树）后面原版仍发光，本仓不发光。
2. **判分汇总**：21 条中完全一致 10 条（33/44 近似/182/174/176/341-346 组）/ 偏差 11 条；宝石灯墙 7 条数值全错是最重灾区。
3. **墙漆覆盖缺失**：CS:323-329 的 paint 覆盖（`paintColor(wallColor)/765`，作用于 flag 墙 357/175）本仓无实现。
4. **彩玻墙染色语义错**：原版 CS:3190-3242（天光）与 CS:3286-3310（地狱光）都是"先把 num/num2/num3 设为当前天空/地狱光，再乘档位系数"——即**只是给已有光重新着色，夜间彩玻墙不产生任何光**。本仓 TS:195-210 用 `max(lr, tint)` 合成 → 夜间彩玻墙恒自发 0.150-0.900 的光。另有两处细节偏差：彩虹档（wall 93）原版系数 = 0.5+Disco/255×0.2（CS:3229-3233，num10=0.7-num9=0.5），本仓 TS:204-205 用 0.7+Disco×0.2 → 整体抬高 0.2；橙玻墙 241 原版 B 系数为 0（CS:3239），本仓 TINT[6]=[0.9,0.5,0] 在 max 语义下无碍但来源标注不准。门禁上原版允许 halfBrick/非挡阳 tile 存在（CS:3190），本仓要求 type===0，偏严。

---

## 第三节 火把色表 TORCH_COLORS（TorchID.cs:134-161 vs LT:60-85）

1.4.5 `_lights` 共 24 条 = 21 个 ConstantTorchLight + DemonTorchLight(7) + DiscoTorchLight(14) + ShimmerTorchLight(23)（TorchID.cs:132 `Count = 24`，**1.4.5 无新增火把色**）。21 条常量逐值对账：

| id | 原版（TorchID 行号） | 本仓（LT 行号） | 判定 |
|---|---|---|---|
| 0 火把 | :137 (1.000,0.950,0.800) | :61 | **一致** |
| 1 蓝 | :138 (0,0.100,1.300) | :62 | **一致** |
| 2 红 | :139 (1.000,0.100,0.100) | :63 | **一致** |
| 3 绿 | :140 (0,1.000,0.100) | :64 | **一致** |
| 4 紫（恶魔祭坛紫） | :141 (0.900,0,0.900) | :65 | **一致** |
| 5 白 | :142 (1.400,1.400,1.400) | :66 | **一致** |
| 6 黄 | :143 (0.900,0.900,0) | :67 | **一致** |
| 8 诅咒 | :145 (1.000,1.600,0.500) | :69 | **一致** |
| 9 冰 | :146 (0.750,0.850,1.400) | :70 | **一致** |
| 10 橙 | :147 (1.000,0.500,0) | :71 | **一致** |
| 11 圣液 | :148 (1.400,1.400,0.700) | :72 | **一致** |
| 12 超亮 | :149 (0.750,1.350,1.500) | :73 | **一致** |
| 13 骨头 | :150 (0.950,0.750,1.300) | :74 | **一致** |
| 15 粉 | :152 (1.000,0,1.000) | :76 | **一致** |
| 16 沙漠 | :153 (1.400,0.850,0.550) | :77 | **一致** |
| 17 珊瑚 | :154 (0.250,1.300,0.800) | :78 | **一致** |
| 18 腐化 | :155 (0.950,0.400,1.400) | :79 | **一致** |
| 19 猩红 | :156 (1.400,0.700,0.500) | :80 | **一致** |
| 20 神圣 | :157 (1.250,0.600,1.200) | :81 | **一致** |
| 21 丛林 | :158 (0.750,1.450,0.900) | :82 | **一致** |
| 22 蘑菇 | :159 (0.300,0.780,1.200) | :83 | **一致** |

三条动态 provider：
- **7 DemonTorch**：TorchID.cs:39-44 `r=0.5d+(1-d), g=0.3, b=d+0.5(1-d)`，d∈[0,1]（Main.cs 每帧 ±0.01）。SC:136-139 逐字一致 → **一致**（LT:68 占位 [1,0.3,0.5] 未被使用，无害）。
- **14 Disco**：TorchID.cs:67-71 = Disco/255。SC:148-150 + SC:123-132 六相步进 7 与 Main.cs:19442-19502 一致 → **一致**（LT:75 占位 [1,1,1] 未被使用）。
- **23 Shimmer**：TorchID.cs:50-61 `num=clamp(0.9+(270-mouse)/900,0,1)`（实际 [0.917,0.989]）→ r=num×0.9∈[0.825,0.890]、b=num×1.2∈[1.100,1.187]；`num2=clamp(0.9+(270-mouse)/125,0,1)`（实际 [1.020,1.540] 恒被钳到 1）→ **g=0.550 常量**。SC:142-146 用 `(mouse-190)/65` 线性 0..1 的 num，返回 `[num×0.9, (1-num)×0.55, num×1.2]` → r∈[0,0.900]、g∈[0,0.550] 反向摆动、b∈[0,1.200] 全幅摆动 → **偏差(3)**（三通道公式全错；正确形态是 R/B 仅 8% 微幅呼吸、G 恒 0.55）。

附带缺陷：火把（sheet 4）在本仓被叠加了原版没有的闪烁（TS:236-237，见第一节结构 1）；CS:1537-1541 的 `frameX<66` 门由 DEV ['x',66] 等效覆盖 ✓。

---

## 第四节 液体光源（CS ApplyLiquidLight :110-151 / ApplyHellLight :3261-3338 vs TS）

| 项 | 原版 | 本仓 | 判定 |
|---|---|---|---|
| 岩浆光公式 | CS:116-132：num=0.55+(270-mouseTextColor)/900 → R=num、G=num×0.6、B=num×0.2；num∈[0.567,0.639] | TS:164 lavaV=0.55+(270-mouse)/900；TS:262-264 `max(R,lavaV) / max(G,lavaV×0.6) / max(B,lavaV×0.2)` | **公式一致；合成语义偏差(1)**：原版 G/B 的比较阈值是 num 本身（CS:124、128）而非 num×0.6/0.2，故当格内已有光落在 (num×0.6, num) 区间时原版会**下调**该通道，本仓纯 max 只升不降（地表岩浆格黄昏时差异可见） |
| 微光液体光 | CS:133-151：num2=0.7+(270-mouse)/900∈[0.717,0.789]、num3=0.7+(270-mouse)/125∈[0.820,1.340] → R=num2×0.6∈[0.430,0.473]、G=num3×0.25∈[0.205,0.335]、B=num2×0.9∈[0.645,0.710] | TS:261-264 仅 `liquidType===2` 分支，无 `liquidType===4` 分支 | **缺失**（微光液体完全不发光；TS:122 的 mask 处理也把 shimmer 落到 Water mask，与 CS GetTileMask :76-86 一致 ✓） |
| 地狱光 | CS:3266-3271：num4=0.55+sin(GlobalTimeWrappedHourly×2)×0.08 → (num4, num4×0.6, num4×0.2) | TS:161-162 hellV=0.55+sin(performance.now()×0.002)×0.08 → 同构 | **一致（近似）**：Main.cs:16777 `GlobalTimeWrappedHourly = TotalSeconds % 3600`，故 sin(2×秒) 与 performance.now()(ms)×0.002=2×秒 严格同频同幅（周期 3.142 s）；唯一差异是原版 3600 s 环绕处 sin 相位不连续，影响可忽略 |
| 地狱/天光透墙门 | CS:3170（天光）/ CS:3270（地狱）：`wallLight[wall] || wall==73 || wall==227 || (invisibleWall && !drawInvisibleWalls)` | TS:151-152 `wall===0 || WALL_LIGHT.has(wall)` | **偏差(2)**：缺 73（云墙）与 227（降雪墙）特例——云墙/雪墙后无天光与地狱光；另缺回声墙涂层（invisibleWall）透光特例 |
| 地狱光深度门 | CS:3270 `tile.liquid<200 && (!halfBrick || 上邻 liquid<200)` | TS:181 shallowLiquid + TS:134-153 exposed()（slope/half 四邻全干） | **一致**（门同构） |
| 表层满液 B 微光 | CS:3181-3188：liquid>=200 且 liquidAlpha[13]>0 时 B=num6×0.175×(1+rand×0.13)×alpha | 无实现 | **无需实现**：原版死代码——WaterStyleID.Count=13（WaterStyleID.cs:31，合法样式 0..12），Main.cs:56846-56858 只对 `i==waterStyle` 抬 liquidAlpha，liquidAlpha[13] 恒 0，该分支永不触发 |
| shimmerDarken 乘子 | CS:3243-3246：天光三通道 ×(1-shimmerDarken) | TS 扫描器无 | 归"天空光一路"审查范围；本仓播种端未见对应衰减，提示给第三路 |

---

## 第五节 WALL_LIGHT 透光墙全表（Main.cs:10487-10502 vs LT:57 + TS:152）

原版 16 条：`wallLight[0]=true`（Main.cs:10487）+ 15 条非零墙（:10488-10502）。

| 墙 id | 原版行号 | 本仓 | 判定 |
|---|---|---|---|
| 0（空气/无墙） | Main:10487 | TS:152 `wall===0` 特判 | **一致**（由调用方处理，LT:56 注释声明，合理） |
| 21 玻璃墙 | Main:10488 | LT:57 集合成员 | **一致** |
| 318 回声墙 | Main:10489 | LT:57 | **一致** |
| 106 木栅栏 | Main:10490 | LT:57 | **一致** |
| 317 灰烬木栅栏 | Main:10491 | LT:57 | **一致** |
| 107 金属栅栏 | Main:10492 | LT:57 | **一致** |
| 138 黑檀木栅栏 | Main:10493 | LT:57 | **一致** |
| 140 珍珠木栅栏 | Main:10494 | LT:57 | **一致** |
| 141 红木栅栏 | Main:10495 | LT:57 | **一致** |
| 139 红棕木栅栏 | Main:10496 | LT:57 | **一致** |
| 145 铁栅栏 | Main:10497 | LT:57 | **一致** |
| 150 红木矮栏 | Main:10498 | LT:57 | **一致** |
| 152 棕榈木矮栏 | Main:10499 | LT:57 | **一致** |
| 245 熟铁栅栏 | Main:10500 | LT:57 | **一致** |
| 315 竹栅栏 | Main:10501 | LT:57 | **一致** |
| 168 五彩纸屑墙 | Main:10502 | LT:57 | **一致** |

**结论**：WALL_LIGHT 全表 16/16 覆盖一致（15 显式 + 0 特判）。唯一补齐项是第四节指出的 73/227（云墙/降雪墙）**不在** wallLight 表内、而是 ApplySurfaceLight/ApplyHellLight 里的独立特例——若第三路按本表判定"云墙透天光"，本仓确实缺失该特例，建议在 exposed() 内补 `wall===73 || wall===227`。

---

## 总结（按优先级）

1. **P0 数值错误**：宝石灯墙 153-166 七条（LT:97-103，id 与宝石名错位一档）；火把 22 魔矿色（TD:86，应为 0.120/0.070/0.320）；微光火把公式（SC:142-146，G 应恒 0.550）；灯笼 42 default（TS:60，应为 (1,1,1)）；传送门炮 209 双档色（TS:78-79）。
2. **P0 缺失**：微光液体光（TS 无 liquidType===4 分支）；彩玻墙夜间不应自发光（TS:195-210 应改为乘法重着色）；火族 336-344、宝石灯块 262-268、月亮砖 500-503、月球砖 415-418、苔砖族（517/534/535/537/540/626/627/628/687-692）、仙女罐 568-570、灵魂瓶 572、云 717-719 等 66 条 tile 光源。
3. **P1 系统性**：FLICKER_SHEETS 11 项多加闪烁、592 漏加；def.light 逐格播撒替代原版帧级门控（92/98/96/592 最明显）；发光墙统一 `type===0` 门过严（宝石灯墙 153-166 原版无门）；WALL_LIGHT 之外的 73/227 天光/地狱光特例缺失。
4. **P2 清理**：TD:140（sheet 12 心晶）与 TD:88（sheet 58 狱石）两条非原版光源应移除；墙漆覆盖（CS:323-329）未实现。
5. **已达标项**：TORCH_COLORS 21 常量逐值一致、demon/disco 动态一致；岩浆公式与地狱脉动一致；蘑菇组八条含 349 门禁一致；84/126/429/372/237/204/354/340/634/633/637/638/463/491/302/613/614/711/536/539/625/302 与苔墙 341-345/182/33/174/176 一致；WALL_LIGHT 全表一致；原版 7 个"tileLighted 但无 case"项本仓 6/7 正确未发光。
```
