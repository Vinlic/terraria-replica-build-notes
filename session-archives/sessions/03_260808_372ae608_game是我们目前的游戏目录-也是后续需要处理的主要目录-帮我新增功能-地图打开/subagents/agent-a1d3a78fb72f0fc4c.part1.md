# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-09T02:55:02.924Z

```
逐行审计 ~/Project/GLM/SandboxWorld/game/src/world/liquid/LiquidSim.ts（我们的移植）与 ~/Project/GLM/SandboxWorld/Terarria1405/Liquid.cs（原版 1.4.0.5 反编译）的算法一致性。

逐方法对照（我们的方法 → 原版行号）：
- update() → Liquid.Update() L298-674：实心检查、地狱蒸发（UnderworldLayer 我们用 h-200）、岩浆 delay5/蜂蜜 delay10、水唤醒岩浆/蜂蜜邻居的四邻范围、向下流动（L375-397：搬运量公式、flag 边界、skipLiquid 置位、quickSettle 补满）、kill 维护（L652-671）
- sideFlow() → L398-651：flag1-6 的 else-if 链求值顺序、num1=-1 偏置、>250 禁延伸、7/5/4/3/2 格均分公式与中心格例外条件（num3!=6||up.liquid<=0）、类型写入时机、AddWater 条件——**每个分支单独核对**
- lavaCheck()/honeyCheck() → L888-1016 / L1018-1115：情形 A/B 条件、阈值 24/32、方块类型（56/230/229）、生成位置、sum 计算、tileObsidianKill 近似是否引入行为差异
- delWater() → L1117-1213：残量清零/水膜抹除/留在列表的三分支条件、再唤醒、swap-remove
- addWater() → L835-872：边界 [5, w-5)、checkingLiquid、实心拒绝
- updateLiquid() → L691-833：cycles/curMaxLiquid、分片 start/end 计算、quickFall 分支、清扫（kill>=8、254→255）、stuck 检测
- quickWater()/settleWaterAt()/attemptToMoveLiquid() → L85-280：垂直下落条件、蛇形铺开的方向/折返逻辑（num2/num3/num4/num5/flag3/flag4/flag5）、侧下方灌入、AttemptToMoveLava/Honey 的异或语义
- waterCheck() → WorldGen.cs:48955-49009：扫描顺序、AddWater 条件、实心格清液

注意 liquidType 编码差异：我们 1=水 2=岩浆 3=蜂蜜，原版 0=水 1=岩浆 2=蜂蜜——核对类型比较是否翻译正确。

输出：每处偏差一行，格式 `偏差 | 我们代码位置 | 原版行号 | 影响程度（高/中/低）`。不确定的标注"待确认"。不要罗列一致项，只报差异。报告 ≤80 行。
```

---

## 📎 Attachment · skill_listing · 2026-08-09T02:55:02.927Z

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

## 🤖 Assistant · 2026-08-09T02:55:07.460Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The user wants a line-by-line audit comparing two files: our port `LiquidSim.ts` and the original decompiled `Liquid.cs`. Let me read both files first.
```

</details>


---

## 🤖 Assistant · 2026-08-09T02:55:07.462Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/liquid/LiquidSim.ts"
}
```


---

## 🤖 Assistant · 2026-08-09T02:55:07.464Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/Liquid.cs",
 "limit": 400
}
```


---

## 👤 User(sidechain) · 2026-08-09T02:55:07.470Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.Liquid
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using Microsoft.Xna.Framework;
8	using System;
9	using System.Collections.Generic;
10	using Terraria.Audio;
11	using Terraria.GameContent.NetModules;
12	using Terraria.ID;
13	using Terraria.Localization;
14	using Terraria.ObjectData;
15	
16	namespace Terraria
17	{
18	  public class Liquid
19	  {
20	    public static int maxLiquid = 25000;
21	    public static int cycles = 10;
22	    public static int curMaxLiquid = 0;
23	    private static HashSet<int> _netChangeSet = new HashSet<int>();
24	    private static HashSet<int> _swapNetChangeSet = new HashSet<int>();
25	    public const int maxLiquidBuffer = 50000;
26	    public static int skipCount;
27	    public static int stuckCount;
28	    public static int stuckAmount;
29	    public static int numLiquid;
30	    public static bool stuck;
31	    public static bool quickFall;
32	    public static bool quickSettle;
33	    private static int wetCounter;
34	    public static int panicCounter;
35	    public static bool panicMode;
36	    public static int panicY;
37	    public int x;
38	    public int y;
39	    public int kill;
40	    public int delay;
41	
42	    public static void NetSendLiquid(int x, int y)
43	    {
44	      if (WorldGen.gen)
45	        return;
46	      lock (Liquid._netChangeSet)
47	        Liquid._netChangeSet.Add((x & (int) ushort.MaxValue) << 16 | y & (int) ushort.MaxValue);
48	    }
49	
50	    public static void tilesIgnoreWater(bool ignoreSolids)
51	    {
52	      Main.tileSolid[138] = !ignoreSolids;
53	      Main.tileSolid[484] = !ignoreSolids;
54	      Main.tileSolid[546] = !ignoreSolids;
55	    }
56	
57	    public static void worldGenTilesIgnoreWater(bool ignoreSolids)
58	    {
59	      Main.tileSolid[10] = !ignoreSolids;
60	      Main.tileSolid[192] = !ignoreSolids;
61	      Main.tileSolid[191] = !ignoreSolids;
62	      Main.tileSolid[190] = !ignoreSolids;
63	    }
64	
65	    public static void ReInit()
66	    {
67	      Liquid.skipCount = 0;
68	      Liquid.stuckCount = 0;
69	      Liquid.stuckAmount = 0;
70	      Liquid.cycles = 10;
71	      Liquid.curMaxLiquid = Liquid.maxLiquid;
72	      Liquid.numLiquid = 0;
73	      Liquid.stuck = false;
74	      Liquid.quickFall = false;
75	      Liquid.quickSettle = false;
76	      Liquid.wetCounter = 0;
77	      Liquid.panicCounter = 0;
78	      Liquid.panicMode = false;
79	      Liquid.panicY = 0;
80	      if (!Main.Setting_UseReducedMaxLiquids)
81	        return;
82	      Liquid.curMaxLiquid = 5000;
83	    }
84	
85	    public static void QuickWater(int verbose = 0, int minY = -1, int maxY = -1)
86	    {
87	      Main.tileSolid[379] = true;
88	      Liquid.tilesIgnoreWater(true);
89	      if (minY == -1)
90	        minY = 3;
91	      if (maxY == -1)
92	        maxY = Main.maxTilesY - 3;
93	      for (int index = maxY; index >= minY; --index)
94	      {
95	        Liquid.UpdateProgressDisplay(verbose, minY, maxY, index);
96	        for (int originX = 4; originX < Main.maxTilesX - 4; ++originX)
97	        {
98	          if (Main.tile[originX, index].liquid != (byte) 0)
99	            Liquid.SettleWaterAt(originX, index);
100	        }
101	      }
102	      Liquid.tilesIgnoreWater(false);
103	    }
104	
105	    private static void SettleWaterAt(int originX, int originY)
106	    {
107	      Tile tile1 = Main.tile[originX, originY];
108	      Liquid.tilesIgnoreWater(true);
109	      if (tile1.liquid == (byte) 0)
110	        return;
111	      int X = originX;
112	      int Y = originY;
113	      bool tileAtXYHasLava = tile1.lava();
114	      bool tileAtXYHasHoney = tile1.honey();
115	      int liquid = (int) tile1.liquid;
116	      byte num1 = tile1.liquidType();
117	      tile1.liquid = (byte) 0;
118	      bool flag1 = true;
119	      while (true)
120	      {
121	        Tile tile2 = Main.tile[X, Y + 1];
122	        bool flag2 = false;
123	        for (; Y < Main.maxTilesY - 5 && tile2.liquid == (byte) 0 && (!tile2.nactive() || !Main.tileSolid[(int) tile2.type] || Main.tileSolidTop[(int) tile2.type]); tile2 = Main.tile[X, Y + 1])
124	        {
125	          ++Y;
126	          flag2 = true;
127	          flag1 = false;
128	        }
129	        if (flag2 && WorldGen.gen && (!tileAtXYHasHoney && Y > WorldGen.waterLine))
130	          num1 = (byte) 1;
131	        int num2 = -1;
132	        int num3 = 0;
133	        int num4 = -1;
134	        int num5 = 0;
135	        bool flag3 = false;
136	        bool flag4 = false;
137	        bool flag5 = false;
138	        while (true)
139	        {
140	          if (Main.tile[X + num3 * num2, Y].liquid == (byte) 0)
141	          {
142	            num4 = num2;
143	            num5 = num3;
144	          }
145	          if (num2 == -1 && X + num3 * num2 < 5)
146	            flag4 = true;
147	          else if (num2 == 1 && X + num3 * num2 > Main.maxTilesX - 5)
148	            flag3 = true;
149	          Tile tile3 = Main.tile[X + num3 * num2, Y + 1];
150	          if (tile3.liquid != (byte) 0 && tile3.liquid != byte.MaxValue && (int) tile3.liquidType() == (int) num1)
151	          {
152	            int num6 = (int) byte.MaxValue - (int) tile3.liquid;
153	            if (num6 > liquid)
154	              num6 = liquid;
155	            tile3.liquid += (byte) num6;
156	            liquid -= num6;
157	            if (liquid == 0)
158	              goto label_34;
159	          }
160	          if (Y >= Main.maxTilesY - 5 || tile3.liquid != (byte) 0 || tile3.nactive() && Main.tileSolid[(int) tile3.type] && !Main.tileSolidTop[(int) tile3.type])
161	          {
162	            Tile tile4 = Main.tile[X + (num3 + 1) * num2, Y];
163	            if (tile4.liquid != (byte) 0 && (!flag1 || num2 != 1) || tile4.nactive() && Main.tileSolid[(int) tile4.type] && !Main.tileSolidTop[(int) tile4.type])
164	            {
165	              if (num2 == 1)
166	                flag3 = true;
167	              else
168	                flag4 = true;
169	            }
170	            if (!(flag4 & flag3))
171	            {
172	              if (flag3)
173	              {
174	                num2 = -1;
175	                ++num3;
176	              }
177	              else if (flag4)
178	              {
179	                if (num2 == 1)
180	                  ++num3;
181	                num2 = 1;
182	              }
183	              else
184	              {
185	                if (num2 == 1)
186	                  ++num3;
187	                num2 = -num2;
188	              }
189	            }
190	            else
191	              goto label_34;
192	          }
193	          else
194	            break;
195	        }
196	        flag5 = true;
197	label_34:
198	        X += num5 * num4;
199	        if (liquid != 0 && flag5)
200	          ++Y;
201	        else
202	          break;
203	      }
204	      Main.tile[X, Y].liquid = (byte) liquid;
205	      Main.tile[X, Y].liquidType((int) num1);
206	      if (Main.tile[X, Y].liquid > (byte) 0)
207	      {
208	        Liquid.AttemptToMoveLava(X, Y, tileAtXYHasLava);
209	        Liquid.AttemptToMoveHoney(X, Y, tileAtXYHasHoney);
210	      }
211	      Liquid.tilesIgnoreWater(false);
212	    }
213	
214	    private static void AttemptToMoveHoney(int X, int Y, bool tileAtXYHasHoney)
215	    {
216	      if (Main.tile[X - 1, Y].liquid > (byte) 0 && Main.tile[X - 1, Y].honey() != tileAtXYHasHoney)
217	      {
218	        if (tileAtXYHasHoney)
219	          Liquid.HoneyCheck(X, Y);
220	        else
221	          Liquid.HoneyCheck(X - 1, Y);
222	      }
223	      else if (Main.tile[X + 1, Y].liquid > (byte) 0 && Main.tile[X + 1, Y].honey() != tileAtXYHasHoney)
224	      {
225	        if (tileAtXYHasHoney)
226	          Liquid.HoneyCheck(X, Y);
227	        else
228	          Liquid.HoneyCheck(X + 1, Y);
229	      }
230	      else if (Main.tile[X, Y - 1].liquid > (byte) 0 && Main.tile[X, Y - 1].honey() != tileAtXYHasHoney)
231	      {
232	        if (tileAtXYHasHoney)
233	          Liquid.HoneyCheck(X, Y);
234	        else
235	          Liquid.HoneyCheck(X, Y - 1);
236	      }
237	      else
238	      {
239	        if (Main.tile[X, Y + 1].liquid <= (byte) 0 || Main.tile[X, Y + 1].honey() == tileAtXYHasHoney)
240	          return;
241	        if (tileAtXYHasHoney)
242	          Liquid.HoneyCheck(X, Y);
243	        else
244	          Liquid.HoneyCheck(X, Y + 1);
245	      }
246	    }
247	
248	    private static void AttemptToMoveLava(int X, int Y, bool tileAtXYHasLava)
249	    {
250	      if (Main.tile[X - 1, Y].liquid > (byte) 0 && Main.tile[X - 1, Y].lava() != tileAtXYHasLava)
251	      {
252	        if (tileAtXYHasLava)
253	          Liquid.LavaCheck(X, Y);
254	        else
255	          Liquid.LavaCheck(X - 1, Y);
256	      }
257	      else if (Main.tile[X + 1, Y].liquid > (byte) 0 && Main.tile[X + 1, Y].lava() != tileAtXYHasLava)
258	      {
259	        if (tileAtXYHasLava)
260	          Liquid.LavaCheck(X, Y);
261	        else
262	          Liquid.LavaCheck(X + 1, Y);
263	      }
264	      else if (Main.tile[X, Y - 1].liquid > (byte) 0 && Main.tile[X, Y - 1].lava() != tileAtXYHasLava)
265	      {
266	        if (tileAtXYHasLava)
267	          Liquid.LavaCheck(X, Y);
268	        else
269	          Liquid.LavaCheck(X, Y - 1);
270	      }
271	      else
272	      {
273	        if (Main.tile[X, Y + 1].liquid <= (byte) 0 || Main.tile[X, Y + 1].lava() == tileAtXYHasLava)
274	          return;
275	        if (tileAtXYHasLava)
276	          Liquid.LavaCheck(X, Y);
277	        else
278	          Liquid.LavaCheck(X, Y + 1);
279	      }
280	    }
281	
282	    private static void UpdateProgressDisplay(int verbose, int minY, int maxY, int y)
283	    {
284	      if (verbose > 0)
285	      {
286	        float num = (float) (maxY - y) / (float) (maxY - minY + 1) / (float) verbose;
287	        Main.statusText = Lang.gen[27].Value + " " + (object) (int) ((double) num * 100.0 + 1.0) + "%";
288	      }
289	      else
290	      {
291	        if (verbose >= 0)
292	          return;
293	        float num = (float) (maxY - y) / (float) (maxY - minY + 1) / (float) -verbose;
294	        Main.statusText = Lang.gen[18].Value + " " + (object) (int) ((double) num * 100.0 + 1.0) + "%";
295	      }
296	    }
297	
298	    public void Update()
299	    {
300	      Main.tileSolid[379] = true;
301	      Tile tile1 = Main.tile[this.x - 1, this.y];
302	      Tile tile2 = Main.tile[this.x + 1, this.y];
303	      Tile tile3 = Main.tile[this.x, this.y - 1];
304	      Tile tile4 = Main.tile[this.x, this.y + 1];
305	      Tile tile5 = Main.tile[this.x, this.y];
306	      if (tile5.nactive() && Main.tileSolid[(int) tile5.type] && !Main.tileSolidTop[(int) tile5.type])
307	      {
308	        int type = (int) tile5.type;
309	        this.kill = 999;
310	      }
311	      else
312	      {
313	        byte liquid = tile5.liquid;
314	        if (this.y > Main.UnderworldLayer && tile5.liquidType() == (byte) 0 && tile5.liquid > (byte) 0)
315	        {
316	          byte num = 2;
317	          if ((int) tile5.liquid < (int) num)
318	            num = tile5.liquid;
319	          tile5.liquid -= num;
320	        }
321	        if (tile5.liquid == (byte) 0)
322	        {
323	          this.kill = 999;
324	        }
325	        else
326	        {
327	          if (tile5.lava())
328	          {
329	            Liquid.LavaCheck(this.x, this.y);
330	            if (!Liquid.quickFall)
331	            {
332	              if (this.delay < 5)
333	              {
334	                ++this.delay;
335	                return;
336	              }
337	              this.delay = 0;
338	            }
339	          }
340	          else
341	          {
342	            if (tile1.lava())
343	              Liquid.AddWater(this.x - 1, this.y);
344	            if (tile2.lava())
345	              Liquid.AddWater(this.x + 1, this.y);
346	            if (tile3.lava())
347	              Liquid.AddWater(this.x, this.y - 1);
348	            if (tile4.lava())
349	              Liquid.AddWater(this.x, this.y + 1);
350	            if (tile5.honey())
351	            {
352	              Liquid.HoneyCheck(this.x, this.y);
353	              if (!Liquid.quickFall)
354	              {
355	                if (this.delay < 10)
356	                {
357	                  ++this.delay;
358	                  return;
359	                }
360	                this.delay = 0;
361	              }
362	            }
363	            else
364	            {
365	              if (tile1.honey())
366	                Liquid.AddWater(this.x - 1, this.y);
367	              if (tile2.honey())
368	                Liquid.AddWater(this.x + 1, this.y);
369	              if (tile3.honey())
370	                Liquid.AddWater(this.x, this.y - 1);
371	              if (tile4.honey())
372	                Liquid.AddWater(this.x, this.y + 1);
373	            }
374	          }
375	          if ((!tile4.nactive() || !Main.tileSolid[(int) tile4.type] || Main.tileSolidTop[(int) tile4.type]) && ((tile4.liquid <= (byte) 0 || (int) tile4.liquidType() == (int) tile5.liquidType()) && tile4.liquid < byte.MaxValue))
376	          {
377	            bool flag = false;
378	            float num = (float) ((int) byte.MaxValue - (int) tile4.liquid);
379	            if ((double) num > (double) tile5.liquid)
380	              num = (float) tile5.liquid;
381	            if ((double) num == 1.0 && tile5.liquid == byte.MaxValue)
382	              flag = true;
383	            if (!flag)
384	              tile5.liquid -= (byte) num;
385	            tile4.liquid += (byte) num;
386	            tile4.liquidType((int) tile5.liquidType());
387	            Liquid.AddWater(this.x, this.y + 1);
388	            tile4.skipLiquid(true);
389	            tile5.skipLiquid(true);
390	            if (Liquid.quickSettle && tile5.liquid > (byte) 250)
391	              tile5.liquid = byte.MaxValue;
392	            else if (!flag)
393	            {
394	              Liquid.AddWater(this.x - 1, this.y);
395	              Liquid.AddWater(this.x + 1, this.y);
396	            }
397	          }
398	          if (tile5.liquid > (byte) 0)
399	          {
400	            bool flag1 = true;

```


---

## 👤 User(sidechain) · 2026-08-09T02:55:07.646Z

**📎 ToolResult**

```
1	// 液体模拟：Terraria 1.4.0.5 Liquid.cs 一比一移植。
2	// 核心结构（对照原版行号）：
3	//  - 活动液体列表 liquids[{x,y,kill,delay}] + checkingLiquid/skipLiquid 位图（Liquid.cs:37-40）
4	//  - UpdateLiquid() 分片调度 + kill 清扫（Liquid.cs:691-833）
5	//  - Update() 单格流程：实心格/地狱蒸发/岩浆蜂蜜降速与交互/下灌/侧向均流/kill 维护（Liquid.cs:298-674）
6	//  - LavaCheck/HoneyCheck：水+岩浆→黑曜石(56)、岩浆+蜂蜜→脆蜂蜜块(230)、水+蜂蜜→蜂蜜块(229)（Liquid.cs:888-1115）
7	//  - QuickWater/SettleWaterAt 读档沉降搬运（Liquid.cs:85-212）+ WaterCheck 重建列表（WorldGen.cs:48955）
8	// liquidType 编码沿用本仓库 store 约定：1=水 2=岩浆 3=蜂蜜（原版 0/1/2）。
9	// 偏离原版处（无法直译的周边系统）：
10	//  - 无 LiquidBuffer 溢出队列/panic 模式（curMaxLiquid 内直接入列，超限丢弃）
11	//  - PlaceTile 的音效/网络广播省略；tileObsidianKill 近似为 decor 清除
12	//  - AddWater 不做 CheckWaterDeath（火把等不会被水流冲毁）
13	import { TILE_DEFS, TILE_BY_KEY } from '../../data/tiles';
14	import type { World } from '../World';
15	
16	interface LiquidEntry { x: number; y: number; kill: number; delay: number; }
17	
18	const OBSIDIAN = TILE_BY_KEY['obsidian'];
19	const HONEY_BLOCK = TILE_BY_KEY['v_229_honey_block'];
20	const CRISPY_HONEY = TILE_BY_KEY['v_230_crispy_honey_block'];
21	
22	export class LiquidSim {
23	  world: World;
24	  /** 活动液体条目（原版 Main.liquid[]，dense 数组 + swap-remove） */
25	  private liquids: LiquidEntry[] = [];
26	  numLiquid = 0;
27	  /** tile.checkingLiquid / tile.skipLiquid 位图 */
28	  private checking: Uint8Array;
29	  private skip: Uint8Array;
30	  /** 调度参数（单机客户端高质量档：cycles = 17-10*1 = 7；Main.cs:12240-12243） */
31	  private cycles = 7;
32	  private curMaxLiquid = 25000;
33	  private wetCounter = 0;
34	  /** 读档沉降：quickSettle=true 时 cycles=1 全量处理、下灌快速补满（WorldFile.cs:365-389 / Main.cs:12251） */
35	  quickSettle = false;
36	  private quickFall = false;
37	  private stuck = false;
38	  private stuckCount = 0;
39	  private stuckAmount = -99999;
40	  private disposed = false;
41	
42	  constructor(world: World) {
43	    this.world = world;
44	    const st = world.store;
45	    this.checking = new Uint8Array(st.w * st.h);
46	    this.skip = new Uint8Array(st.w * st.h);
47	    // 挖掘/放置唤醒：原版 SquareTileFrame 会对 3×3 内每格 TileFrame→AddWater（WorldGen.cs:49664）
48	    st.onTileChanged((x, y) => {
49	      if (this.disposed) return;
50	      for (let dy = -1; dy <= 1; dy++)
51	        for (let dx = -1; dx <= 1; dx++) this.addWater(x + dx, y + dy);
52	    });
53	    // 液体直接写入（水桶等）：唤醒目标及四邻
54	    st.onLiquidChanged((x, y) => {
55	      if (this.disposed) return;
56	      this.addWater(x, y);
57	      this.addWater(x, y - 1); this.addWater(x, y + 1);
58	      this.addWater(x - 1, y); this.addWater(x + 1, y);
59	    });
60	  }
61	
62	  /** 丢弃模拟器：预沉降临时实例调用，停止响应唤醒 */
63	  dispose() {
64	    this.disposed = true;
65	    this.liquids.length = 0;
66	    this.numLiquid = 0;
67	  }
68	
69	  private idx(x: number, y: number): number { return y * this.world.store.w + x; }
70	
71	  /** 格子是否阻挡液体（原版 nactive() && tileSolid && !tileSolidTop） */
72	  private blocksLiquid(x: number, y: number): boolean {
73	    const st = this.world.store;
74	    if (x < 0 || y < 0 || x >= st.w || y >= st.h) return true;
75	    const t = st.type[this.idx(x, y)];
76	    if (t === 0) return false;
77	    const d = TILE_DEFS[t];
78	    return !!d && d.solid && !d.platform;
79	  }
80	
81	  // ================= AddWater（Liquid.cs:835-872） =================
82	
83	  addWater(x: number, y: number) {
84	    const st = this.world.store;
85	    if (x >= st.w - 5 || y >= st.h - 5 || x < 5 || y < 5) return;
86	    const i = this.idx(x, y);
87	    if (this.checking[i] || st.liquid[i] === 0) return;
88	    const t = st.type[i];
89	    if (t !== 0) {
90	      const d = TILE_DEFS[t];
91	      if (d && d.solid && !d.platform) return;
92	    }
93	    if (this.numLiquid >= this.curMaxLiquid - 1) return; // 无 buffer：超限丢弃（原版走 LiquidBuffer）
94	    this.checking[i] = 1;
95	    this.skip[i] = 0;
96	    this.liquids[this.numLiquid] = { x, y, kill: 0, delay: 0 };
97	    this.numLiquid++;
98	  }
99	
100	  // ================= UpdateLiquid 调度（Liquid.cs:691-833） =================
101	
102	  /** 每 2 个逻辑 tick 调一次（原版 WorldGen.UpdateWorld 内 skipCount 节流） */
103	  step() { this.updateLiquid(); }
104	
105	  updateLiquid() {
106	    const st = this.world.store;
107	    const killThreshold = 8; // 单机 num1（Liquid.cs:693）
108	    const quickSettle = this.quickSettle;
109	    this.quickFall = quickSettle; // 客户端：quickFall = quickSettle（Liquid.cs:752-755）
110	    const cycles = quickSettle ? 1 : this.cycles; // quickSettle 时 cycles=1（Main.cs:12251）
111	    this.wetCounter++;
112	    const slice = Math.floor(this.curMaxLiquid / cycles);
113	    const start = slice * (this.wetCounter - 1);
114	    let end = slice * this.wetCounter;
115	    if (this.wetCounter === cycles) end = this.numLiquid;
116	    if (end > this.numLiquid) { end = this.numLiquid; this.wetCounter = cycles; }
117	    if (this.quickFall) {
118	      for (let l = start; l < end; l++) {
119	        const e = this.liquids[l];
120	        e.delay = 10;
121	        this.update(e);
122	        this.skip[this.idx(e.x, e.y)] = 0;
123	      }
124	    } else {
125	      for (let l = start; l < end; l++) {
126	        const e = this.liquids[l];
127	        const i = this.idx(e.x, e.y);
128	        if (!this.skip[i]) this.update(e);
129	        else this.skip[i] = 0;
130	      }
131	    }
132	    if (this.wetCounter >= cycles) {
133	      this.wetCounter = 0;
134	      // 清扫：kill 累积达标 → 254 补满 255 后出列（Liquid.cs:790-798）
135	      for (let l = this.numLiquid - 1; l >= 0; l--) {
136	        const e = this.liquids[l];
137	        if (e.kill >= killThreshold) {
138	          const i = this.idx(e.x, e.y);
139	          if (st.liquid[i] === 254) st.liquid[i] = 255;
140	          this.delWater(l);
141	        }
142	      }
143	      // 卡死检测：活动量长期不变 → 清空列表靠唤醒自愈（Liquid.cs:808-824）
144	      if (this.numLiquid > 0 && this.numLiquid > this.stuckAmount - 50 && this.numLiquid < this.stuckAmount + 50) {
145	        this.stuckCount++;
146	        if (this.stuckCount >= 10000) {
147	          this.stuck = true;
148	          for (let l = this.numLiquid - 1; l >= 0; l--) this.delWater(l);
149	          this.stuck = false;
150	          this.stuckCount = 0;
151	        }
152	      } else {
153	        this.stuckCount = 0;
154	        this.stuckAmount = this.numLiquid;
155	      }
156	    }
157	  }
158	
159	  // ================= 单格流程 Update（Liquid.cs:298-674） =================
160	
161	  private update(e: LiquidEntry) {
162	    const st = this.world.store;
163	    const w = st.w, h = st.h;
164	    const x = e.x, y = e.y;
165	    const i5 = this.idx(x, y);
166	    // 1) 本格被实心方块占据 → 下轮必删（Liquid.cs:306-310）
167	    if (this.blocksLiquid(x, y)) { e.kill = 999; return; }
168	    const startAmt = st.liquid[i5];
169	    // 2) 地狱蒸发：水每 tick -2（Liquid.cs:314-320；UnderworldLayer ≈ h-200）
170	    if (y > h - 200 && st.liquidType[i5] === 1 && st.liquid[i5] > 0) {
171	      st.liquid[i5] = Math.max(0, st.liquid[i5] - 2);
172	    }
173	    if (st.liquid[i5] === 0) { e.kill = 999; return; }
174	    const myType = st.liquidType[i5];
175	    // 3) 岩浆/蜂蜜：先交互检查，再降速（Liquid.cs:327-373）
176	    if (myType === 2) {
177	      this.lavaCheck(x, y);
178	      if (!this.quickFall) {
179	        if (e.delay < 5) { e.delay++; return; }
180	        e.delay = 0;
181	      }
182	    } else {
183	      // 水格：唤醒岩浆邻居，让对方自己的 Update 处理交互（Liquid.cs:342-349）
184	      for (const [nx, ny] of [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]] as const) {
185	        if (nx < 0 || ny < 0 || nx >= w || ny >= h) continue;
186	        const ni = this.idx(nx, ny);
187	        if (st.liquid[ni] > 0 && st.liquidType[ni] === 2) this.addWater(nx, ny);
188	      }
189	      if (myType === 3) {
190	        this.honeyCheck(x, y);
191	        if (!this.quickFall) {
192	          if (e.delay < 10) { e.delay++; return; }
193	          e.delay = 0;
194	        }
195	      } else {
196	        // 唤醒蜂蜜邻居（Liquid.cs:365-372）
197	        for (const [nx, ny] of [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]] as const) {
198	          if (nx < 0 || ny < 0 || nx >= w || ny >= h) continue;
199	          const ni = this.idx(nx, ny);
200	          if (st.liquid[ni] > 0 && st.liquidType[ni] === 3) this.addWater(nx, ny);
201	        }
202	      }
203	    }
204	    // 4) 向下全量下灌（Liquid.cs:375-397）
205	    {
206	      const bi = this.idx(x, y + 1);
207	      const belowAmt = st.liquid[bi];
208	      const belowType = st.liquidType[bi];
209	      const belowBlocks = y + 1 >= h ? true : this.blocksLiquid(x, y + 1);
210	      if (!belowBlocks && (belowAmt <= 0 || belowType === myType) && belowAmt < 255) {
211	        let t = 255 - belowAmt;
212	        if (t > st.liquid[i5]) t = st.liquid[i5];
213	        // 原版边界特性：缺口 1 且本格满格时不扣源（Liquid.cs:381-384）
214	        const flag = t === 1 && st.liquid[i5] === 255;
215	        if (!flag) st.liquid[i5] -= t;
216	        st.liquid[bi] += t;
217	        st.liquidType[bi] = myType;
218	        this.addWater(x, y + 1);
219	        this.skip[bi] = 1;
220	        this.skip[i5] = 1;
221	        if (this.quickSettle && st.liquid[i5] > 250) st.liquid[i5] = 255;
222	        else if (!flag) { this.addWater(x - 1, y); this.addWater(x + 1, y); }
223	      }
224	    }
225	    // 5) 侧向均流（Liquid.cs:398-651）
226	    if (st.liquid[i5] > 0) this.sideFlow(x, y, i5);
227	    // 6) kill 维护（Liquid.cs:652-671）
228	    if (st.liquid[i5] !== startAmt) {
229	      if (st.liquid[i5] === 254 && startAmt === 255) {
230	        if (this.quickSettle) st.liquid[i5] = 255;
231	        e.kill++;
232	      } else {
233	        this.addWater(x, y - 1);
234	        e.kill = 0;
235	      }
236	    } else {
237	      e.kill++;
238	    }
239	  }
240	
241	  /** 侧向均流：参与格全体写平均值（Liquid.cs:398-651，逐分支照抄） */
242	  private sideFlow(x: number, y: number, i5: number) {
243	    const st = this.world.store;
244	    const myType = st.liquidType[i5];
245	    const il = i5 - 1, ir = i5 + 1, iu = i5 - st.w, im2 = i5 - 2, ip2 = i5 + 2, im3 = i5 - 3, ip3 = i5 + 3;
246	    const lq = st.liquid[il], rq = st.liquid[ir];
247	    // flag1 左可流 / flag2 右可流 / flag3 左 2 格延伸 / flag4 右 2 格延伸
248	    let f1 = true, f2 = true, f3 = true, f4 = true;
249	    if (this.blocksLiquid(x - 1, y)) f1 = false;
250	    else if (lq > 0 && st.liquidType[il] !== myType) f1 = false;
251	    else if (this.blocksLiquid(x - 2, y)) f3 = false;
252	    else if (st.liquid[im2] === 0) f3 = false;
253	    else if (st.liquidType[im2] !== myType) f3 = false;
254	    if (this.blocksLiquid(x + 1, y)) f2 = false;
255	    else if (rq > 0 && st.liquidType[ir] !== myType) f2 = false;
256	    else if (this.blocksLiquid(x + 2, y)) f4 = false;
257	    else if (st.liquid[ip2] === 0) f4 = false;
258	    else if (st.liquidType[ip2] !== myType) f4 = false;
259	    let num1 = 0;
260	    if (st.liquid[i5] < 3) num1 = -1;         // 薄层蒸发偏置（Liquid.cs:424-426）
261	    if (st.liquid[i5] > 250) { f3 = false; f4 = false; }
262	    const setCell = (i: number, ax: number, m: number, centerAmt: number) => {
263	      st.liquidType[i] = myType;
264	      if (st.liquid[i] !== m) { st.liquid[i] = m; this.addWater(ax, y); }
265	    };
266	    if (f1 && f2) {
267	      if (f3 && f4) {
268	        // ±3 延伸判定（Liquid.cs:436-449）
269	        let f5 = true, f6 = true;
270	        if (this.blocksLiquid(x - 3, y)) f5 = false;
271	        else if (st.liquid[im3] === 0) f5 = false;
272	        else if (st.liquidType[im3] !== myType) f5 = false;
273	        if (this.blocksLiquid(x + 3, y)) f6 = false;
274	        else if (st.liquid[ip3] === 0) f6 = false;
275	        else if (st.liquidType[ip3] !== myType) f6 = false;
276	        if (f5 && f6) {
277	          // 7 格均分（Liquid.cs:452-515）
278	          const m = Math.round((lq + rq + st.liquid[im2] + st.liquid[ip2] + st.liquid[im3] + st.liquid[ip3] + st.liquid[i5] + num1) / 7);
279	          let same = 0;
280	          if (lq !== m) { st.liquidType[il] = myType; st.liquid[il] = m; this.addWater(x - 1, y); } else { st.liquidType[il] = myType; same++; }
281	          if (rq !== m) { st.liquidType[ir] = myType; st.liquid[ir] = m; this.addWater(x + 1, y); } else { st.liquidType[ir] = myType; same++; }
282	          if (st.liquid[im2] !== m) { st.liquidType[im2] = myType; st.liquid[im2] = m; this.addWater(x - 2, y); } else { st.liquidType[im2] = myType; same++; }
283	          if (st.liquid[ip2] !== m) { st.liquidType[ip2] = myType; st.liquid[ip2] = m; this.addWater(x + 2, y); } else { st.liquidType[ip2] = myType; same++; }
284	          if (st.liquid[im3] !== m) { st.liquidType[im3] = myType; st.liquid[im3] = m; this.addWater(x - 3, y); } else { st.liquidType[im3] = myType; same++; }
285	          if (st.liquid[ip3] !== m) { st.liquidType[ip3] = myType; st.liquid[ip3] = m; this.addWater(x + 3, y); } else { st.liquidType[ip3] = myType; same++; }
286	          // 中心例外：六邻全等于均值且上方有液 → 保持原值（Liquid.cs:514）
287	          if (same !== 6 || st.liquid[iu] <= 0) st.liquid[i5] = m;
288	        } else {
289	          // 5 格均分（Liquid.cs:519-562）
290	          const m = Math.round((lq + rq + st.liquid[im2] + st.liquid[ip2] + st.liquid[i5] + num1) / 5);
291	          let same = 0;
292	          if (lq !== m) { st.liquidType[il] = myType; st.liquid[il] = m; this.addWater(x - 1, y); } else { st.liquidType[il] = myType; same++; }
293	          if (rq !== m) { st.liquidType[ir] = myType; st.liquid[ir] = m; this.addWater(x + 1, y); } else { st.liquidType[ir] = myType; same++; }
294	          if (st.liquid[im2] !== m) { st.liquidType[im2] = myType; st.liquid[im2] = m; this.addWater(x - 2, y); } else { st.liquidType[im2] = myType; same++; }
295	          if (st.liquid[ip2] !== m) { st.liquidType[ip2] = myType; st.liquid[ip2] = m; this.addWater(x + 2, y); } else { st.liquidType[ip2] = myType; same++; }
296	          if (same !== 4 || st.liquid[iu] <= 0) st.liquid[i5] = m;
297	        }
298	      } else if (f3) {
299	        // 4 格：左延伸（Liquid.cs:567-587）
300	        const m = Math.round((lq + rq + st.liquid[im2] + st.liquid[i5] + num1) / 4);
301	        if (lq !== m || st.liquid[i5] !== m) { st.liquidType[il] = myType; st.liquid[il] = m; this.addWater(x - 1, y); }
302	        if (rq !== m || st.liquid[i5] !== m) { st.liquidType[ir] = myType; st.liquid[ir] = m; this.addWater(x + 1, y); }
303	        if (st.liquid[im2] !== m || st.liquid[i5] !== m) { st.liquidType[im2] = myType; st.liquid[im2] = m; this.addWater(x - 2, y); }
304	        st.liquid[i5] = m;
305	      } else if (f4) {
306	        // 4 格：右延伸（Liquid.cs:590-609）
307	        const m = Math.round((lq + rq + st.liquid[ip2] + st.liquid[i5] + num1) / 4);
308	        if (lq !== m || st.liquid[i5] !== m) { st.liquidType[il] = myType; st.liquid[il] = m; this.addWater(x - 1, y); }
309	        if (rq !== m || st.liquid[i5] !== m) { st.liquidType[ir] = myType; st.liquid[ir] = m; this.addWater(x + 1, y); }
310	        if (st.liquid[ip2] !== m || st.liquid[i5] !== m) { st.liquidType[ip2] = myType; st.liquid[ip2] = m; this.addWater(x + 2, y); }
311	        st.liquid[i5] = m;
312	      } else {
313	        // 3 格均分（Liquid.cs:613-628）：随机 254→255 补满
314	        let m = Math.round((lq + rq + st.liquid[i5] + num1) / 3);
315	        if (m === 254 && Math.random() * 30 < 1) m = 255;
316	        if (lq !== m) { st.liquidType[il] = myType; st.liquid[il] = m; this.addWater(x - 1, y); } else st.liquidType[il] = myType;
317	        if (rq !== m) { st.liquidType[ir] = myType; st.liquid[ir] = m; this.addWater(x + 1, y); } else st.liquidType[ir] = myType;
318	        st.liquid[i5] = m;
319	      }
320	    } else if (f1) {
321	      // 2 格：向左（Liquid.cs:633-639）
322	      const m = Math.round((lq + st.liquid[i5] + num1) / 2);
323	      if (lq !== m) st.liquid[il] = m;
324	      st.liquidType[il] = myType;
325	      if (st.liquid[i5] !== m || st.liquid[il] !== m) this.addWater(x - 1, y);
326	      st.liquid[i5] = m;
327	    } else if (f2) {
328	      // 2 格：向右（Liquid.cs:643-649）
329	      const m = Math.round((rq + st.liquid[i5] + num1) / 2);
330	      if (rq !== m) st.liquid[ir] = m;
331	      st.liquidType[ir] = myType;
332	      if (st.liquid[i5] !== m || st.liquid[ir] !== m) this.addWater(x + 1, y);
333	      st.liquid[i5] = m;
334	    }
335	  }
336	
337	  // ================= 液体交互（Liquid.cs:888-1115） =================
338	
339	  /** 岩浆格与水/蜂蜜接触 → 黑曜石 56 / 脆蜂蜜块 230（阈值 24） */
340	  private lavaCheck(x: number, y: number) {
341	    const st = this.world.store;
342	    if (this.blocksLiquid(x, y)) return;
343	    const i5 = this.idx(x, y);
344	    const il = i5 - 1, ir = i5 + 1, iu = i5 - st.w, id = i5 + st.w;
345	    const lq = st.liquid[il], rq = st.liquid[ir], uq = st.liquid[iu], dq = st.liquid[id];
346	    const lt = st.liquidType[il], rt = st.liquidType[ir], ut = st.liquidType[iu], dt = st.liquidType[id];
347	    if ((lq > 0 && lt !== 2) || (rq > 0 && rt !== 2) || (uq > 0 && ut !== 2)) {
348	      // 情形 A：左右/上方有非岩浆液体 → 生成在岩浆格（Liquid.cs:905-959）
349	      let sum = 0;
350	      let type = OBSIDIAN;
351	      if (lt !== 2) { sum += lq; st.liquid[il] = 0; }
352	      if (rt !== 2) { sum += rq; st.liquid[ir] = 0; }
353	      if (ut !== 2) { sum += uq; st.liquid[iu] = 0; }
354	      if (lt === 3 || rt === 3 || ut === 3) type = CRISPY_HONEY;
355	      if (sum < 24) return;
356	      const t = st.type[i5];
357	      if (t !== 0) {
358	        const d = TILE_DEFS[t];
359	        if (d && d.decor) st.setTile(x, y, 0);  // 近似 tileObsidianKill
360	        else return;                             // 平台等保留方块 → 不生成
361	      }
362	      st.liquid[i5] = 0;
363	      st.liquidType[i5] = 0;
364	      st.setTile(x, y, type);
365	    } else {
366	      if (dq <= 0 || dt === 2) return;
367	      // 情形 B：仅下方有水/蜂蜜 → 生成在下方格（Liquid.cs:961-1014）
368	      const belowT = st.type[id];
369	      if (belowT !== 0) {
370	        const d = TILE_DEFS[belowT];
371	        if (d && d.decor) st.setTile(x, y + 1, 0); // tileCut / obsidianKill 近似
372	        else return;
373	      }
374	      if (st.liquid[i5] < 24) { st.liquid[i5] = 0; st.liquidType[i5] = 0; return; }
375	      const type = dt === 3 ? CRISPY_HONEY : OBSIDIAN;
376	      st.liquid[i5] = 0; st.liquidType[i5] = 0;
377	      st.liquid[id] = 0; st.liquidType[id] = 0;
378	      st.setTile(x, y + 1, type);
379	    }
380	  }
381	
382	  /** 蜂蜜格与水接触 → 蜂蜜块 229（阈值 32） */
383	  private honeyCheck(x: number, y: number) {
384	    const st = this.world.store;
385	    if (this.blocksLiquid(x, y)) return;
386	    const i5 = this.idx(x, y);
387	    const il = i5 - 1, ir = i5 + 1, iu = i5 - st.w, id = i5 + st.w;
388	    const lq = st.liquid[il], rq = st.liquid[ir], uq = st.liquid[iu], dq = st.liquid[id];
389	    const lt = st.liquidType[il], rt = st.liquidType[ir], ut = st.liquidType[iu], dt = st.liquidType[id];
390	    if ((lq > 0 && lt === 1) || (rq > 0 && rt === 1) || (uq > 0 && ut === 1)) {
391	      let sum = 0;
392	      if (lt === 1) { sum += lq; st.liquid[il] = 0; }
393	      if (rt === 1) { sum += rq; st.liquid[ir] = 0; }
394	      if (ut === 1) { sum += uq; st.liquid[iu] = 0; }
395	      if (sum < 32) return;
396	      const t = st.type[i5];
397	      if (t !== 0) {
398	        const d = TILE_DEFS[t];
399	        if (d && d.decor) st.setTile(x, y, 0);
400	        else return;
401	      }
402	      st.liquid[i5] = 0;
403	      st.liquidType[i5] = 0;
404	      st.setTile(x, y, HONEY_BLOCK);
405	    } else {
406	      if (dq <= 0 || dt !== 1) return;
407	      const belowT = st.type[id];
408	      if (belowT !== 0) {
409	        const d = TILE_DEFS[belowT];
410	        if (d && d.decor) st.setTile(x, y + 1, 0);
411	        else return;
412	      }
413	      if (st.liquid[i5] < 32) { st.liquid[i5] = 0; st.liquidType[i5] = 0; return; }
414	      st.liquid[i5] = 0; st.liquidType[i5] = 0;
415	      st.liquid[id] = 0; st.liquidType[id] = 0;
416	      st.setTile(x, y + 1, HONEY_BLOCK);
417	    }
418	  }
419	
420	  // ================= DelWater（Liquid.cs:1117-1213） =================
421	
422	  private delWater(l: number) {
423	    const st = this.world.store;
424	    const e = this.liquids[l];
425	    const x = e.x, y = e.y;
426	    const i5 = this.idx(x, y);
427	    const il = i5 - 1, ir = i5 + 1, id = i5 + st.w;
428	    const amt = st.liquid[i5];
429	    if (amt < 2) {
430	      // 残量清零 + 邻居唤醒（Liquid.cs:1125-1137）
431	      st.liquid[i5] = 0;
432	      if (st.liquid[il] < 2) st.liquid[il] = 0; else this.addWater(x - 1, y);
433	      if (st.liquid[ir] < 2) st.liquid[ir] = 0; else this.addWater(x + 1, y);
434	    } else if (amt < 20) {
435	      // 水膜抹除：邻格更低或下方不满（Liquid.cs:1138-1142）
436	      const lq = st.liquid[il], rq = st.liquid[ir], dq = st.liquid[id];
437	      if ((lq < amt && !this.blocksLiquid(x - 1, y)) ||
438	          (rq < amt && !this.blocksLiquid(x + 1, y)) ||
439	          (dq < 255 && !this.blocksLiquid(x, y + 1))) {
440	        st.liquid[i5] = 0;
441	      }
442	    } else if (st.liquid[id] < 255 && !this.blocksLiquid(x, y + 1) && !this.stuck && !this.blocksLiquid(x, y)) {
443	      e.kill = 0; // 下方未满：留在列表继续流（Liquid.cs:1143-1147）
444	      return;
445	    }
446	    if (st.liquid[i5] < 250 && st.liquid[i5 - st.w] > 0) this.addWater(x, y - 1);
447	    if (st.liquid[i5] === 0) {
448	      st.liquidType[i5] = 0;
449	    } else {
450	      const rq = st.liquid[ir], lq = st.liquid[il];
451	      if (rq > 0 && rq < 250 && !this.blocksLiquid(x + 1, y) && st.liquid[i5] !== rq) this.addWater(x + 1, y);
452	      if (lq > 0 && lq < 250 && !this.blocksLiquid(x - 1, y) && st.liquid[i5] !== lq) this.addWater(x - 1, y);
453	      if (st.liquidType[i5] === 2) {
454	        this.lavaCheck(x, y);
455	        // 3×3 草转泥土近似：岩浆旁 decor 植物清除（Liquid.cs:1160-1187 原版为草方块转换）
456	        for (let dy = -1; dy <= 1; dy++) {
457	          for (let dx = -1; dx <= 1; dx++) {
458	            const nx = x + dx, ny = y + dy;
459	            if (nx < 1 || ny < 1 || nx >= st.w - 1 || ny >= st.h - 1) continue;
460	            const ni = this.idx(nx, ny);
461	            const d = TILE_DEFS[st.type[ni]];
462	            if (d && d.decor && d.attach === 'ground') st.setTile(nx, ny, 0);
463	          }
464	        }
465	      } else if (st.liquidType[i5] === 3) {
466	        this.honeyCheck(x, y);
467	      }
468	    }
469	    // swap-remove（Liquid.cs:1193-1197）
470	    this.numLiquid--;
471	    this.checking[i5] = 0;
472	    this.liquids[l] = this.liquids[this.numLiquid];
473	    this.liquids.length = this.numLiquid;
474	  }
475	
476	  // ================= 读档沉降：QuickWater（Liquid.cs:85-103 / 105-212） =================
477	
478	  /** 自底向上逐湿格直接搬运沉降（原版 QuickWater(verbose, -1, -1)：y 从 h-3 到 3） */
479	  quickWater(minY = 3, maxY = -1) {
480	    const st = this.world.store;
481	    const yMax = maxY < 0 ? st.h - 3 : maxY;
482	    for (let y = yMax; y >= minY; y--) {
483	      for (let x = 4; x < st.w - 4; x++) {
484	        if (st.liquid[this.idx(x, y)] !== 0) this.settleWaterAt(x, y);
485	      }
486	    }
487	  }
488	
489	  /** 单格液体直接搬到最终落点（Liquid.cs:105-212 逐行对照） */
490	  private settleWaterAt(originX: number, originY: number) {
491	    const st = this.world.store;
492	    const oi = this.idx(originX, originY);
493	    if (st.liquid[oi] === 0) return;
494	    let X = originX, Y = originY;
495	    const srcType = st.liquidType[oi];
496	    let liquid = st.liquid[oi];
497	    st.liquid[oi] = 0;
498	    let flag1 = true;
499	    for (;;) {
500	      // 1) 垂直下落：下方空且可通行就一直落（Liquid.cs:121-130）
501	      let flag2 = false;
502	      while (Y < st.h - 5 && st.liquid[this.idx(X, Y + 1)] === 0 && !this.blocksLiquid(X, Y + 1)) {
503	        Y++;
504	        flag2 = true;
505	        flag1 = false;
506	      }
507	      // （Liquid.cs:129-130 的 waterLine 岩浆转换仅世界生成期生效，读档跳过）
508	      // 2) 蛇形横向铺开（Liquid.cs:131-195）
509	      let dir = -1;          // num2：当前行走方向
510	      let step = 0;          // num3：当前行步数
511	      let lastDir = -1;      // num4：最后空位方向
512	      let lastStep = 0;      // num5：最后空位步数
513	      let hitL = false;      // flag4：左边界
514	      let hitR = false;      // flag3：右边界
515	      let dropped = false;   // flag5：本轮发生下落
516	      for (;;) {
517	        const ci = this.idx(X + step * dir, Y);
518	        if (st.liquid[ci] === 0) { lastDir = dir; lastStep = step; }
519	        if (dir === -1 && X + step * dir < 5) hitL = true;
520	        else if (dir === 1 && X + step * dir > st.w - 5) hitR = true;
521	        const bi = this.idx(X + step * dir, Y + 1);
522	        // 侧下方同类型未满 → 直接灌入（Liquid.cs:149-159）
523	        if (st.liquid[bi] !== 0 && st.liquid[bi] !== 255 && st.liquidType[bi] === srcType) {
524	          let t = 255 - st.liquid[bi];
525	          if (t > liquid) t = liquid;
526	          st.liquid[bi] += t;
527	          liquid -= t;
528	          if (liquid === 0) break;
529	        }
530	        if (Y >= st.h - 5 || st.liquid[bi] !== 0 || this.blocksLiquid(X + step * dir, Y + 1)) {
531	          // 下方堵住 → 沿行继续 / 折返（Liquid.cs:162-191）
532	          const ni = this.idx(X + (step + 1) * dir, Y);
533	          const nAmt = st.liquid[ni];
534	          const nSolid = this.blocksLiquid(X + (step + 1) * dir, Y);
535	          if ((nAmt !== 0 && (!flag1 || dir !== 1)) || nSolid) {
536	            if (dir === 1) hitR = true; else hitL = true;
537	          }
538	          if (hitL && hitR) break;
539	          if (hitR) { dir = -1; step++; }
540	          else if (hitL) { if (dir === 1) step++; dir = 1; }
541	          else { if (dir === 1) step++; dir = -dir; }
542	        } else {
543	          dropped = true;
544	          break;
545	        }
546	      }
547	      X += lastStep * lastDir;
548	      if (liquid !== 0 && dropped) Y++;
549	      else break;
550	    }
551	    // 3) 写回落点（Liquid.cs:204-205）
552	    const fi = this.idx(X, Y);
553	    st.liquid[fi] = liquid;
554	    st.liquidType[fi] = srcType;
555	    if (st.liquid[fi] > 0) {
556	      // 落地即交互（Liquid.cs:206-210 / AttemptToMoveLava/Honey 248-280）
557	      this.attemptToMoveLiquid(X, Y, srcType, 2);
558	      this.attemptToMoveLiquid(X, Y, srcType, 3);
559	    }
560	  }
561	
562	  /** 落点与异种液体相邻时触发交互检查（Liquid.cs:248-280 AttemptToMoveLava 同构）。
563	   *  原版语义：邻居的 target 性 != 落点格的 target 性 才算"异种相遇"——
564	   *  水落水旁不算，水落岩浆旁才算（否则整片海洋互相当岩浆转黑曜石） */
565	  private attemptToMoveLiquid(X: number, Y: number, srcType: number, targetType: number) {
566	    const st = this.world.store;
567	    const srcIs = srcType === targetType;
568	    const check = targetType === 2 ? (x: number, y: number) => this.lavaCheck(x, y)
569	      : (x: number, y: number) => this.honeyCheck(x, y);
570	    const diff = (x: number, y: number) => {
571	      const i = this.idx(x, y);
572	      return st.liquid[i] > 0 && (st.liquidType[i] === targetType) !== srcIs;
573	    };
574	    if (diff(X - 1, Y)) { if (srcIs) check(X, Y); else check(X - 1, Y); }
575	    else if (diff(X + 1, Y)) { if (srcIs) check(X, Y); else check(X + 1, Y); }
576	    else if (diff(X, Y - 1)) { if (srcIs) check(X, Y); else check(X, Y - 1); }
577	    else if (diff(X, Y + 1)) { if (srcIs) check(X, Y); else check(X, Y + 1); }
578	  }
579	
580	  // ================= WaterCheck（WorldGen.cs:48955-49009） =================
581	
582	  /** 全图自底向上重建活动列表：能流的/液面不齐的/岩浆旁有异种的都入列 */
583	  waterCheck() {
584	    const st = this.world.store;
585	    this.liquids.length = 0;
586	    this.numLiquid = 0;
587	    this.checking.fill(0);
588	    for (let x = 1; x < st.w - 1; x++) {
589	      for (let y = st.h - 2; y > 0; y--) {
590	        const i = this.idx(x, y);
591	        if (st.liquid[i] === 0) continue;
592	        const t = st.type[i];
593	        if (t !== 0) {
594	          const d = TILE_DEFS[t];
595	          if (d && d.solid && !d.platform) { st.liquid[i] = 0; continue; } // 实心格内液体清零
596	        }
597	        const id = i + st.w;
598	        const dq = st.liquid[id];
599	        if (!this.blocksLiquid(x, y + 1) && dq < 255) {
600	          if (dq > 250) st.liquid[id] = 255;
601	          else this.addWater(x, y);
602	        }
603	        const il = i - 1, ir = i + 1;
604	        if (!this.blocksLiquid(x - 1, y) && st.liquid[il] !== st.liquid[i]) this.addWater(x, y);
605	        else if (!this.blocksLiquid(x + 1, y) && st.liquid[ir] !== st.liquid[i]) this.addWater(x, y);
606	        if (st.liquidType[i] === 2) {
607	          const iu = i - st.w;
608	          if ((st.liquid[il] > 0 && st.liquidType[il] !== 2) ||
609	              (st.liquid[ir] > 0 && st.liquidType[ir] !== 2) ||
610	              (st.liquid[iu] > 0 && st.liquidType[iu] !== 2) ||
611	              (dq > 0 && st.liquidType[id] !== 2)) this.addWater(x, y);
612	        }
613	      }
614	    }
615	  }
616	}
617	

```


---

## 🤖 Assistant · 2026-08-09T02:55:09.711Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me read more of Liquid.cs (L400-1213) and the WorldGen.cs waterCheck part.
```

</details>


---

## 🤖 Assistant · 2026-08-09T02:55:09.713Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/Liquid.cs",
 "limit": 680,
 "offset": 400
}
```


---

## 🤖 Assistant · 2026-08-09T02:55:09.716Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '48940,49020p' ~/Project/GLM/SandboxWorld/Terarria1405/WorldGen.cs",
 "description": "Read WorldGen WaterCheck region"
}
```


---

## 👤 User(sidechain) · 2026-08-09T02:55:09.759Z

**📎 ToolResult**

```
    {
      int num1 = startX;
      int num2 = endX + 1;
      int num3 = startY;
      int num4 = endY + 1;
      for (int i = num1 - 1; i < num2 + 1; ++i)
      {
        for (int j = num3 - 1; j < num4 + 1; ++j)
        {
          WorldGen.TileFrame(i, j, false, false);
          Framing.WallFrame(i, j, false);
        }
      }
    }

    public static void WaterCheck()
    {
      Liquid.tilesIgnoreWater(true);
      Liquid.numLiquid = 0;
      LiquidBuffer.numLiquidBuffer = 0;
      for (int index1 = 1; index1 < Main.maxTilesX - 1; ++index1)
      {
        for (int index2 = Main.maxTilesY - 2; index2 > 0; --index2)
        {
          Tile checkTile = Main.tile[index1, index2];
          checkTile.checkingLiquid(false);
          if (checkTile.liquid > (byte) 0 && checkTile.nactive() && (Main.tileSolid[(int) checkTile.type] && !Main.tileSolidTop[(int) checkTile.type]))
            checkTile.liquid = (byte) 0;
          else if (checkTile.liquid > (byte) 0)
          {
            if (checkTile.active())
            {
              if (checkTile.lava())
              {
                if (TileObjectData.CheckLavaDeath(checkTile))
                  WorldGen.KillTile(index1, index2, false, false, false);
              }
              else if (TileObjectData.CheckWaterDeath(checkTile))
                WorldGen.KillTile(index1, index2, false, false, false);
            }
            Tile tile1 = Main.tile[index1, index2 + 1];
            if ((!tile1.nactive() || !Main.tileSolid[(int) tile1.type] || Main.tileSolidTop[(int) tile1.type]) && tile1.liquid < byte.MaxValue)
            {
              if (tile1.liquid > (byte) 250)
                tile1.liquid = byte.MaxValue;
              else
                Liquid.AddWater(index1, index2);
            }
            Tile tile2 = Main.tile[index1 - 1, index2];
            Tile tile3 = Main.tile[index1 + 1, index2];
            if ((!tile2.nactive() || !Main.tileSolid[(int) tile2.type] || Main.tileSolidTop[(int) tile2.type]) && (int) tile2.liquid != (int) checkTile.liquid)
              Liquid.AddWater(index1, index2);
            else if ((!tile3.nactive() || !Main.tileSolid[(int) tile3.type] || Main.tileSolidTop[(int) tile3.type]) && (int) tile3.liquid != (int) checkTile.liquid)
              Liquid.AddWater(index1, index2);
            if (checkTile.lava())
            {
              if (tile2.liquid > (byte) 0 && !tile2.lava())
                Liquid.AddWater(index1, index2);
              else if (tile3.liquid > (byte) 0 && !tile3.lava())
                Liquid.AddWater(index1, index2);
              else if (Main.tile[index1, index2 - 1].liquid > (byte) 0 && !Main.tile[index1, index2 - 1].lava())
                Liquid.AddWater(index1, index2);
              else if (tile1.liquid > (byte) 0 && !tile1.lava())
                Liquid.AddWater(index1, index2);
            }
          }
        }
      }
      Liquid.tilesIgnoreWater(false);
    }

    public static void EveryTileFrame()
    {
      Stopwatch stopwatch = new Stopwatch();
      stopwatch.Start();
      WorldGen.noLiquidCheck = true;
      WorldGen.noTileActions = true;
      for (int i = 0; i < Main.maxTilesX; ++i)
      {
        float num = (float) i / (float) Main.maxTilesX;
        Main.statusText = Lang.gen[55].Value + " " + (object) (int) ((double) num * 100.0 + 1.0) + "%";

```


---

## 👤 User(sidechain) · 2026-08-09T02:55:09.952Z

**📎 ToolResult**

```
400	            bool flag1 = true;
401	            bool flag2 = true;
402	            bool flag3 = true;
403	            bool flag4 = true;
404	            if (tile1.nactive() && Main.tileSolid[(int) tile1.type] && !Main.tileSolidTop[(int) tile1.type])
405	              flag1 = false;
406	            else if (tile1.liquid > (byte) 0 && (int) tile1.liquidType() != (int) tile5.liquidType())
407	              flag1 = false;
408	            else if (Main.tile[this.x - 2, this.y].nactive() && Main.tileSolid[(int) Main.tile[this.x - 2, this.y].type] && !Main.tileSolidTop[(int) Main.tile[this.x - 2, this.y].type])
409	              flag3 = false;
410	            else if (Main.tile[this.x - 2, this.y].liquid == (byte) 0)
411	              flag3 = false;
412	            else if (Main.tile[this.x - 2, this.y].liquid > (byte) 0 && (int) Main.tile[this.x - 2, this.y].liquidType() != (int) tile5.liquidType())
413	              flag3 = false;
414	            if (tile2.nactive() && Main.tileSolid[(int) tile2.type] && !Main.tileSolidTop[(int) tile2.type])
415	              flag2 = false;
416	            else if (tile2.liquid > (byte) 0 && (int) tile2.liquidType() != (int) tile5.liquidType())
417	              flag2 = false;
418	            else if (Main.tile[this.x + 2, this.y].nactive() && Main.tileSolid[(int) Main.tile[this.x + 2, this.y].type] && !Main.tileSolidTop[(int) Main.tile[this.x + 2, this.y].type])
419	              flag4 = false;
420	            else if (Main.tile[this.x + 2, this.y].liquid == (byte) 0)
421	              flag4 = false;
422	            else if (Main.tile[this.x + 2, this.y].liquid > (byte) 0 && (int) Main.tile[this.x + 2, this.y].liquidType() != (int) tile5.liquidType())
423	              flag4 = false;
424	            int num1 = 0;
425	            if (tile5.liquid < (byte) 3)
426	              num1 = -1;
427	            if (tile5.liquid > (byte) 250)
428	            {
429	              flag3 = false;
430	              flag4 = false;
431	            }
432	            if (flag1 & flag2)
433	            {
434	              if (flag3 & flag4)
435	              {
436	                bool flag5 = true;
437	                bool flag6 = true;
438	                if (Main.tile[this.x - 3, this.y].nactive() && Main.tileSolid[(int) Main.tile[this.x - 3, this.y].type] && !Main.tileSolidTop[(int) Main.tile[this.x - 3, this.y].type])
439	                  flag5 = false;
440	                else if (Main.tile[this.x - 3, this.y].liquid == (byte) 0)
441	                  flag5 = false;
442	                else if ((int) Main.tile[this.x - 3, this.y].liquidType() != (int) tile5.liquidType())
443	                  flag5 = false;
444	                if (Main.tile[this.x + 3, this.y].nactive() && Main.tileSolid[(int) Main.tile[this.x + 3, this.y].type] && !Main.tileSolidTop[(int) Main.tile[this.x + 3, this.y].type])
445	                  flag6 = false;
446	                else if (Main.tile[this.x + 3, this.y].liquid == (byte) 0)
447	                  flag6 = false;
448	                else if ((int) Main.tile[this.x + 3, this.y].liquidType() != (int) tile5.liquidType())
449	                  flag6 = false;
450	                if (flag5 & flag6)
451	                {
452	                  float num2 = (float) Math.Round((double) ((int) tile1.liquid + (int) tile2.liquid + (int) Main.tile[this.x - 2, this.y].liquid + (int) Main.tile[this.x + 2, this.y].liquid + (int) Main.tile[this.x - 3, this.y].liquid + (int) Main.tile[this.x + 3, this.y].liquid + (int) tile5.liquid + num1) / 7.0);
453	                  int num3 = 0;
454	                  tile1.liquidType((int) tile5.liquidType());
455	                  if ((int) tile1.liquid != (int) (byte) num2)
456	                  {
457	                    tile1.liquid = (byte) num2;
458	                    Liquid.AddWater(this.x - 1, this.y);
459	                  }
460	                  else
461	                    ++num3;
462	                  tile2.liquidType((int) tile5.liquidType());
463	                  if ((int) tile2.liquid != (int) (byte) num2)
464	                  {
465	                    tile2.liquid = (byte) num2;
466	                    Liquid.AddWater(this.x + 1, this.y);
467	                  }
468	                  else
469	                    ++num3;
470	                  Main.tile[this.x - 2, this.y].liquidType((int) tile5.liquidType());
471	                  if ((int) Main.tile[this.x - 2, this.y].liquid != (int) (byte) num2)
472	                  {
473	                    Main.tile[this.x - 2, this.y].liquid = (byte) num2;
474	                    Liquid.AddWater(this.x - 2, this.y);
475	                  }
476	                  else
477	                    ++num3;
478	                  Main.tile[this.x + 2, this.y].liquidType((int) tile5.liquidType());
479	                  if ((int) Main.tile[this.x + 2, this.y].liquid != (int) (byte) num2)
480	                  {
481	                    Main.tile[this.x + 2, this.y].liquid = (byte) num2;
482	                    Liquid.AddWater(this.x + 2, this.y);
483	                  }
484	                  else
485	                    ++num3;
486	                  Main.tile[this.x - 3, this.y].liquidType((int) tile5.liquidType());
487	                  if ((int) Main.tile[this.x - 3, this.y].liquid != (int) (byte) num2)
488	                  {
489	                    Main.tile[this.x - 3, this.y].liquid = (byte) num2;
490	                    Liquid.AddWater(this.x - 3, this.y);
491	                  }
492	                  else
493	                    ++num3;
494	                  Main.tile[this.x + 3, this.y].liquidType((int) tile5.liquidType());
495	                  if ((int) Main.tile[this.x + 3, this.y].liquid != (int) (byte) num2)
496	                  {
497	                    Main.tile[this.x + 3, this.y].liquid = (byte) num2;
498	                    Liquid.AddWater(this.x + 3, this.y);
499	                  }
500	                  else
501	                    ++num3;
502	                  if ((int) tile1.liquid != (int) (byte) num2 || (int) tile5.liquid != (int) (byte) num2)
503	                    Liquid.AddWater(this.x - 1, this.y);
504	                  if ((int) tile2.liquid != (int) (byte) num2 || (int) tile5.liquid != (int) (byte) num2)
505	                    Liquid.AddWater(this.x + 1, this.y);
506	                  if ((int) Main.tile[this.x - 2, this.y].liquid != (int) (byte) num2 || (int) tile5.liquid != (int) (byte) num2)
507	                    Liquid.AddWater(this.x - 2, this.y);
508	                  if ((int) Main.tile[this.x + 2, this.y].liquid != (int) (byte) num2 || (int) tile5.liquid != (int) (byte) num2)
509	                    Liquid.AddWater(this.x + 2, this.y);
510	                  if ((int) Main.tile[this.x - 3, this.y].liquid != (int) (byte) num2 || (int) tile5.liquid != (int) (byte) num2)
511	                    Liquid.AddWater(this.x - 3, this.y);
512	                  if ((int) Main.tile[this.x + 3, this.y].liquid != (int) (byte) num2 || (int) tile5.liquid != (int) (byte) num2)
513	                    Liquid.AddWater(this.x + 3, this.y);
514	                  if (num3 != 6 || tile3.liquid <= (byte) 0)
515	                    tile5.liquid = (byte) num2;
516	                }
517	                else
518	                {
519	                  int num2 = 0;
520	                  float num3 = (float) Math.Round((double) ((int) tile1.liquid + (int) tile2.liquid + (int) Main.tile[this.x - 2, this.y].liquid + (int) Main.tile[this.x + 2, this.y].liquid + (int) tile5.liquid + num1) / 5.0);
521	                  tile1.liquidType((int) tile5.liquidType());
522	                  if ((int) tile1.liquid != (int) (byte) num3)
523	                  {
524	                    tile1.liquid = (byte) num3;
525	                    Liquid.AddWater(this.x - 1, this.y);
526	                  }
527	                  else
528	                    ++num2;
529	                  tile2.liquidType((int) tile5.liquidType());
530	                  if ((int) tile2.liquid != (int) (byte) num3)
531	                  {
532	                    tile2.liquid = (byte) num3;
533	                    Liquid.AddWater(this.x + 1, this.y);
534	                  }
535	                  else
536	                    ++num2;
537	                  Main.tile[this.x - 2, this.y].liquidType((int) tile5.liquidType());
538	                  if ((int) Main.tile[this.x - 2, this.y].liquid != (int) (byte) num3)
539	                  {
540	                    Main.tile[this.x - 2, this.y].liquid = (byte) num3;
541	                    Liquid.AddWater(this.x - 2, this.y);
542	                  }
543	                  else
544	                    ++num2;
545	                  Main.tile[this.x + 2, this.y].liquidType((int) tile5.liquidType());
546	                  if ((int) Main.tile[this.x + 2, this.y].liquid != (int) (byte) num3)
547	                  {
548	                    Main.tile[this.x + 2, this.y].liquid = (byte) num3;
549	                    Liquid.AddWater(this.x + 2, this.y);
550	                  }
551	                  else
552	                    ++num2;
553	                  if ((int) tile1.liquid != (int) (byte) num3 || (int) tile5.liquid != (int) (byte) num3)
554	                    Liquid.AddWater(this.x - 1, this.y);
555	                  if ((int) tile2.liquid != (int) (byte) num3 || (int) tile5.liquid != (int) (byte) num3)
556	                    Liquid.AddWater(this.x + 1, this.y);
557	                  if ((int) Main.tile[this.x - 2, this.y].liquid != (int) (byte) num3 || (int) tile5.liquid != (int) (byte) num3)
558	                    Liquid.AddWater(this.x - 2, this.y);
559	                  if ((int) Main.tile[this.x + 2, this.y].liquid != (int) (byte) num3 || (int) tile5.liquid != (int) (byte) num3)
560	                    Liquid.AddWater(this.x + 2, this.y);
561	                  if (num2 != 4 || tile3.liquid <= (byte) 0)
562	                    tile5.liquid = (byte) num3;
563	                }
564	              }
565	              else if (flag3)
566	              {
567	                float num2 = (float) Math.Round((double) ((int) tile1.liquid + (int) tile2.liquid + (int) Main.tile[this.x - 2, this.y].liquid + (int) tile5.liquid + num1) / 4.0);
568	                tile1.liquidType((int) tile5.liquidType());
569	                if ((int) tile1.liquid != (int) (byte) num2 || (int) tile5.liquid != (int) (byte) num2)
570	                {
571	                  tile1.liquid = (byte) num2;
572	                  Liquid.AddWater(this.x - 1, this.y);
573	                }
574	                tile2.liquidType((int) tile5.liquidType());
575	                if ((int) tile2.liquid != (int) (byte) num2 || (int) tile5.liquid != (int) (byte) num2)
576	                {
577	                  tile2.liquid = (byte) num2;
578	                  Liquid.AddWater(this.x + 1, this.y);
579	                }
580	                Main.tile[this.x - 2, this.y].liquidType((int) tile5.liquidType());
581	                if ((int) Main.tile[this.x - 2, this.y].liquid != (int) (byte) num2 || (int) tile5.liquid != (int) (byte) num2)
582	                {
583	                  Main.tile[this.x - 2, this.y].liquid = (byte) num2;
584	                  Liquid.AddWater(this.x - 2, this.y);
585	                }
586	                tile5.liquid = (byte) num2;
587	              }
588	              else if (flag4)
589	              {
590	                float num2 = (float) Math.Round((double) ((int) tile1.liquid + (int) tile2.liquid + (int) Main.tile[this.x + 2, this.y].liquid + (int) tile5.liquid + num1) / 4.0);
591	                tile1.liquidType((int) tile5.liquidType());
592	                if ((int) tile1.liquid != (int) (byte) num2 || (int) tile5.liquid != (int) (byte) num2)
593	                {
594	                  tile1.liquid = (byte) num2;
595	                  Liquid.AddWater(this.x - 1, this.y);
596	                }
597	                tile2.liquidType((int) tile5.liquidType());
598	                if ((int) tile2.liquid != (int) (byte) num2 || (int) tile5.liquid != (int) (byte) num2)
599	                {
600	                  tile2.liquid = (byte) num2;
601	                  Liquid.AddWater(this.x + 1, this.y);
602	                }
603	                Main.tile[this.x + 2, this.y].liquidType((int) tile5.liquidType());
604	                if ((int) Main.tile[this.x + 2, this.y].liquid != (int) (byte) num2 || (int) tile5.liquid != (int) (byte) num2)
605	                {
606	                  Main.tile[this.x + 2, this.y].liquid = (byte) num2;
607	                  Liquid.AddWater(this.x + 2, this.y);
608	                }
609	                tile5.liquid = (byte) num2;
610	              }
611	              else
612	              {
613	                float num2 = (float) Math.Round((double) ((int) tile1.liquid + (int) tile2.liquid + (int) tile5.liquid + num1) / 3.0);
614	                if ((double) num2 == 254.0 && WorldGen.genRand.Next(30) == 0)
615	                  num2 = (float) byte.MaxValue;
616	                tile1.liquidType((int) tile5.liquidType());
617	                if ((int) tile1.liquid != (int) (byte) num2)
618	                {
619	                  tile1.liquid = (byte) num2;
620	                  Liquid.AddWater(this.x - 1, this.y);
621	                }
622	                tile2.liquidType((int) tile5.liquidType());
623	                if ((int) tile2.liquid != (int) (byte) num2)
624	                {
625	                  tile2.liquid = (byte) num2;
626	                  Liquid.AddWater(this.x + 1, this.y);
627	                }
628	                tile5.liquid = (byte) num2;
629	              }
630	            }
631	            else if (flag1)
632	            {
633	              float num2 = (float) Math.Round((double) ((int) tile1.liquid + (int) tile5.liquid + num1) / 2.0);
634	              if ((int) tile1.liquid != (int) (byte) num2)
635	                tile1.liquid = (byte) num2;
636	              tile1.liquidType((int) tile5.liquidType());
637	              if ((int) tile5.liquid != (int) (byte) num2 || (int) tile1.liquid != (int) (byte) num2)
638	                Liquid.AddWater(this.x - 1, this.y);
639	              tile5.liquid = (byte) num2;
640	            }
641	            else if (flag2)
642	            {
643	              float num2 = (float) Math.Round((double) ((int) tile2.liquid + (int) tile5.liquid + num1) / 2.0);
644	              if ((int) tile2.liquid != (int) (byte) num2)
645	                tile2.liquid = (byte) num2;
646	              tile2.liquidType((int) tile5.liquidType());
647	              if ((int) tile5.liquid != (int) (byte) num2 || (int) tile2.liquid != (int) (byte) num2)
648	                Liquid.AddWater(this.x + 1, this.y);
649	              tile5.liquid = (byte) num2;
650	            }
651	          }
652	          if ((int) tile5.liquid != (int) liquid)
653	          {
654	            if (tile5.liquid == (byte) 254 && liquid == byte.MaxValue)
655	            {
656	              if (Liquid.quickSettle)
657	              {
658	                tile5.liquid = byte.MaxValue;
659	                ++this.kill;
660	              }
661	              else
662	                ++this.kill;
663	            }
664	            else
665	            {
666	              Liquid.AddWater(this.x, this.y - 1);
667	              this.kill = 0;
668	            }
669	          }
670	          else
671	            ++this.kill;
672	        }
673	      }
674	    }
675	
676	    public static void StartPanic()
677	    {
678	      if (Liquid.panicMode)
679	        return;
680	      WorldGen.waterLine = Main.maxTilesY;
681	      Liquid.numLiquid = 0;
682	      LiquidBuffer.numLiquidBuffer = 0;
683	      Liquid.panicCounter = 0;
684	      Liquid.panicMode = true;
685	      Liquid.panicY = Main.maxTilesY - 3;
686	      if (!Main.dedServ)
687	        return;
688	      Console.WriteLine(Language.GetTextValue("Misc.ForceWaterSettling"));
689	    }
690	
691	    public static void UpdateLiquid()
692	    {
693	      int num1 = 8;
694	      Liquid.tilesIgnoreWater(true);
695	      if (Main.netMode == 2)
696	      {
697	        int num2 = 0;
698	        for (int index = 0; index < 15; ++index)
699	        {
700	          if (Main.player[index].active)
701	            ++num2;
702	        }
703	        Liquid.cycles = 10 + num2 / 3;
704	        Liquid.curMaxLiquid = Liquid.maxLiquid - num2 * 250;
705	        num1 = 10 + num2 / 3;
706	        if (Main.Setting_UseReducedMaxLiquids)
707	          Liquid.curMaxLiquid = 5000;
708	      }
709	      if (!WorldGen.gen)
710	      {
711	        if (!Liquid.panicMode)
712	        {
713	          if ((double) LiquidBuffer.numLiquidBuffer >= 45000.0)
714	          {
715	            ++Liquid.panicCounter;
716	            if (Liquid.panicCounter > 3600)
717	              Liquid.StartPanic();
718	          }
719	          else
720	            Liquid.panicCounter = 0;
721	        }
722	        if (Liquid.panicMode)
723	        {
724	          int num2 = 0;
725	          while (Liquid.panicY >= 3 && num2 < 5)
726	          {
727	            ++num2;
728	            Liquid.QuickWater(0, Liquid.panicY, Liquid.panicY);
729	            --Liquid.panicY;
730	            if (Liquid.panicY < 3)
731	            {
732	              Console.WriteLine(Language.GetTextValue("Misc.WaterSettled"));
733	              Liquid.panicCounter = 0;
734	              Liquid.panicMode = false;
735	              WorldGen.WaterCheck();
736	              if (Main.netMode == 2)
737	              {
738	                for (int index1 = 0; index1 < (int) byte.MaxValue; ++index1)
739	                {
740	                  for (int index2 = 0; index2 < Main.maxSectionsX; ++index2)
741	                  {
742	                    for (int index3 = 0; index3 < Main.maxSectionsY; ++index3)
743	                      Netplay.Clients[index1].TileSections[index2, index3] = false;
744	                  }
745	                }
746	              }
747	            }
748	          }
749	          return;
750	        }
751	      }
752	      bool quickSettle = Liquid.quickSettle;
753	      if (Main.Setting_UseReducedMaxLiquids)
754	        quickSettle |= Liquid.numLiquid > 2000;
755	      Liquid.quickFall = quickSettle;
756	      ++Liquid.wetCounter;
757	      int num3 = Liquid.curMaxLiquid / Liquid.cycles;
758	      int num4 = num3 * (Liquid.wetCounter - 1);
759	      int num5 = num3 * Liquid.wetCounter;
760	      if (Liquid.wetCounter == Liquid.cycles)
761	        num5 = Liquid.numLiquid;
762	      if (num5 > Liquid.numLiquid)
763	      {
764	        num5 = Liquid.numLiquid;
765	        int netMode = Main.netMode;
766	        Liquid.wetCounter = Liquid.cycles;
767	      }
768	      if (Liquid.quickFall)
769	      {
770	        for (int index = num4; index < num5; ++index)
771	        {
772	          Main.liquid[index].delay = 10;
773	          Main.liquid[index].Update();
774	          Main.tile[Main.liquid[index].x, Main.liquid[index].y].skipLiquid(false);
775	        }
776	      }
777	      else
778	      {
779	        for (int index = num4; index < num5; ++index)
780	        {
781	          if (!Main.tile[Main.liquid[index].x, Main.liquid[index].y].skipLiquid())
782	            Main.liquid[index].Update();
783	          else
784	            Main.tile[Main.liquid[index].x, Main.liquid[index].y].skipLiquid(false);
785	        }
786	      }
787	      if (Liquid.wetCounter >= Liquid.cycles)
788	      {
789	        Liquid.wetCounter = 0;
790	        for (int l = Liquid.numLiquid - 1; l >= 0; --l)
791	        {
792	          if (Main.liquid[l].kill >= num1)
793	          {
794	            if (Main.tile[Main.liquid[l].x, Main.liquid[l].y].liquid == (byte) 254)
795	              Main.tile[Main.liquid[l].x, Main.liquid[l].y].liquid = byte.MaxValue;
796	            Liquid.DelWater(l);
797	          }
798	        }
799	        int num2 = Liquid.curMaxLiquid - (Liquid.curMaxLiquid - Liquid.numLiquid);
800	        if (num2 > LiquidBuffer.numLiquidBuffer)
801	          num2 = LiquidBuffer.numLiquidBuffer;
802	        for (int index = 0; index < num2; ++index)
803	        {
804	          Main.tile[Main.liquidBuffer[0].x, Main.liquidBuffer[0].y].checkingLiquid(false);
805	          Liquid.AddWater(Main.liquidBuffer[0].x, Main.liquidBuffer[0].y);
806	          LiquidBuffer.DelBuffer(0);
807	        }
808	        if (Liquid.numLiquid > 0 && Liquid.numLiquid > Liquid.stuckAmount - 50 && Liquid.numLiquid < Liquid.stuckAmount + 50)
809	        {
810	          ++Liquid.stuckCount;
811	          if (Liquid.stuckCount >= 10000)
812	          {
813	            Liquid.stuck = true;
814	            for (int l = Liquid.numLiquid - 1; l >= 0; --l)
815	              Liquid.DelWater(l);
816	            Liquid.stuck = false;
817	            Liquid.stuckCount = 0;
818	          }
819	        }
820	        else
821	        {
822	          Liquid.stuckCount = 0;
823	          Liquid.stuckAmount = Liquid.numLiquid;
824	        }
825	      }
826	      if (!WorldGen.gen && Main.netMode == 2 && Liquid._netChangeSet.Count > 0)
827	      {
828	        Utils.Swap<HashSet<int>>(ref Liquid._netChangeSet, ref Liquid._swapNetChangeSet);
829	        NetLiquidModule.CreateAndBroadcastByChunk(Liquid._swapNetChangeSet);
830	        Liquid._swapNetChangeSet.Clear();
831	      }
832	      Liquid.tilesIgnoreWater(false);
833	    }
834	
835	    public static void AddWater(int x, int y)
836	    {
837	      Tile checkTile = Main.tile[x, y];
838	      if (Main.tile[x, y] == null || checkTile.checkingLiquid() || (x >= Main.maxTilesX - 5 || y >= Main.maxTilesY - 5) || (x < 5 || y < 5 || checkTile.liquid == (byte) 0) || checkTile.nactive() && Main.tileSolid[(int) checkTile.type] && (checkTile.type != (ushort) 546 && !Main.tileSolidTop[(int) checkTile.type]))
839	        return;
840	      if (Liquid.numLiquid >= Liquid.curMaxLiquid - 1)
841	      {
842	        LiquidBuffer.AddBuffer(x, y);
843	      }
844	      else
845	      {
846	        checkTile.checkingLiquid(true);
847	        checkTile.skipLiquid(false);
848	        Main.liquid[Liquid.numLiquid].kill = 0;
849	        Main.liquid[Liquid.numLiquid].x = x;
850	        Main.liquid[Liquid.numLiquid].y = y;
851	        Main.liquid[Liquid.numLiquid].delay = 0;
852	        ++Liquid.numLiquid;
853	        if (Main.netMode == 2)
854	          Liquid.NetSendLiquid(x, y);
855	        if (!checkTile.active() || WorldGen.gen)
856	          return;
857	        bool flag = false;
858	        if (checkTile.lava())
859	        {
860	          if (TileObjectData.CheckLavaDeath(checkTile))
861	            flag = true;
862	        }
863	        else if (TileObjectData.CheckWaterDeath(checkTile))
864	          flag = true;
865	        if (!flag)
866	          return;
867	        WorldGen.KillTile(x, y, false, false, false);
868	        if (Main.netMode != 2)
869	          return;
870	        NetMessage.SendData(17, -1, -1, (NetworkText) null, 0, (float) x, (float) y, 0.0f, 0, 0, 0);
871	      }
872	    }
873	
874	    private static bool UnderGroundDesertCheck(int x, int y)
875	    {
876	      int num = 3;
877	      for (int x1 = x - num; x1 <= x + num; ++x1)
878	      {
879	        for (int y1 = y - num; y1 <= y + num; ++y1)
880	        {
881	          if (WorldGen.InWorld(x1, y1, 0) && (Main.tile[x1, y1].wall == (ushort) 187 || Main.tile[x1, y1].wall == (ushort) 216))
882	            return true;
883	        }
884	      }
885	      return false;
886	    }
887	
888	    public static void LavaCheck(int x, int y)
889	    {
890	      if (WorldGen.generatingWorld && Liquid.UnderGroundDesertCheck(x, y))
891	      {
892	        for (int index1 = x - 3; index1 <= x + 3; ++index1)
893	        {
894	          for (int index2 = y - 3; index2 <= y + 3; ++index2)
895	            Main.tile[index1, index2].lava(true);
896	        }
897	      }
898	      if (WorldGen.SolidTile(x, y, false))
899	        return;
900	      Tile tile1 = Main.tile[x - 1, y];
901	      Tile tile2 = Main.tile[x + 1, y];
902	      Tile tile3 = Main.tile[x, y - 1];
903	      Tile tile4 = Main.tile[x, y + 1];
904	      Tile tile5 = Main.tile[x, y];
905	      if (tile1.liquid > (byte) 0 && !tile1.lava() || tile2.liquid > (byte) 0 && !tile2.lava() || tile3.liquid > (byte) 0 && !tile3.lava())
906	      {
907	        int num = 0;
908	        int Type = 56;
909	        if (!tile1.lava())
910	        {
911	          num += (int) tile1.liquid;
912	          tile1.liquid = (byte) 0;
913	        }
914	        if (!tile2.lava())
915	        {
916	          num += (int) tile2.liquid;
917	          tile2.liquid = (byte) 0;
918	        }
919	        if (!tile3.lava())
920	        {
921	          num += (int) tile3.liquid;
922	          tile3.liquid = (byte) 0;
923	        }
924	        if (tile1.honey() || tile2.honey() || tile3.honey())
925	          Type = 230;
926	        if (num < 24)
927	          return;
928	        if (tile5.active() && Main.tileObsidianKill[(int) tile5.type])
929	        {
930	          WorldGen.KillTile(x, y, false, false, false);
931	          if (Main.netMode == 2)
932	            NetMessage.SendData(17, -1, -1, (NetworkText) null, 0, (float) x, (float) y, 0.0f, 0, 0, 0);
933	        }
934	        if (WorldGen.getGoodWorldGen)
935	        {
936	          if (!tile1.lava() && !tile2.lava() && !tile3.lava())
937	            tile5.lava(false);
938	          else
939	            tile5.lava(true);
940	        }
941	        else
942	        {
943	          if (tile5.active())
944	            return;
945	          tile5.liquid = (byte) 0;
946	          tile5.lava(false);
947	          if (!WorldGen.gen)
948	          {
949	            if (Type == 56)
950	              SoundEngine.PlaySound(SoundID.LiquidsWaterLava, new Vector2((float) (x * 16 + 8), (float) (y * 16 + 8)));
951	            else
952	              SoundEngine.PlaySound(SoundID.LiquidsHoneyLava, new Vector2((float) (x * 16 + 8), (float) (y * 16 + 8)));
953	          }
954	          WorldGen.PlaceTile(x, y, Type, true, true, -1, 0);
955	          WorldGen.SquareTileFrame(x, y, true);
956	          if (Main.netMode != 2)
957	            return;
958	          NetMessage.SendTileSquare(-1, x - 1, y - 1, 3, Type == 56 ? TileChangeType.LavaWater : TileChangeType.HoneyLava);
959	        }
960	      }
961	      else
962	      {
963	        if (tile4.liquid <= (byte) 0 || tile4.lava())
964	          return;
965	        bool flag = false;
966	        if (tile5.active() && TileID.Sets.IsAContainer[(int) tile5.type] && !TileID.Sets.IsAContainer[(int) tile4.type])
967	          flag = true;
968	        if (Main.tileCut[(int) tile4.type])
969	        {
970	          WorldGen.KillTile(x, y + 1, false, false, false);
971	          if (Main.netMode == 2)
972	            NetMessage.SendData(17, -1, -1, (NetworkText) null, 0, (float) x, (float) (y + 1), 0.0f, 0, 0, 0);
973	        }
974	        else if (tile4.active() && Main.tileObsidianKill[(int) tile4.type])
975	        {
976	          WorldGen.KillTile(x, y + 1, false, false, false);
977	          if (Main.netMode == 2)
978	            NetMessage.SendData(17, -1, -1, (NetworkText) null, 0, (float) x, (float) (y + 1), 0.0f, 0, 0, 0);
979	        }
980	        if (!(!tile4.active() | flag))
981	          return;
982	        if (tile5.liquid < (byte) 24)
983	        {
984	          tile5.liquid = (byte) 0;
985	          tile5.liquidType(0);
986	          if (Main.netMode != 2)
987	            return;
988	          NetMessage.SendTileSquare(-1, x - 1, y, 3, TileChangeType.None);
989	        }
990	        else if (WorldGen.getGoodWorldGen)
991	        {
992	          if (!tile4.lava())
993	            tile5.lava(false);
994	          else
995	            tile5.lava(true);
996	        }
997	        else
998	        {
999	          int Type = 56;
1000	          if (tile4.honey())
1001	            Type = 230;
1002	          tile5.liquid = (byte) 0;
1003	          tile5.lava(false);
1004	          tile4.liquid = (byte) 0;
1005	          if (Type == 56)
1006	            SoundEngine.PlaySound(SoundID.LiquidsWaterLava, new Vector2((float) (x * 16 + 8), (float) (y * 16 + 8)));
1007	          else
1008	            SoundEngine.PlaySound(SoundID.LiquidsHoneyLava, new Vector2((float) (x * 16 + 8), (float) (y * 16 + 8)));
1009	          WorldGen.PlaceTile(x, y + 1, Type, true, true, -1, 0);
1010	          WorldGen.SquareTileFrame(x, y + 1, true);
1011	          if (Main.netMode != 2)
1012	            return;
1013	          NetMessage.SendTileSquare(-1, x - 1, y, 3, Type == 56 ? TileChangeType.LavaWater : TileChangeType.HoneyLava);
1014	        }
1015	      }
1016	    }
1017	
1018	    public static void HoneyCheck(int x, int y)
1019	    {
1020	      if (WorldGen.SolidTile(x, y, false))
1021	        return;
1022	      Tile tile1 = Main.tile[x - 1, y];
1023	      Tile tile2 = Main.tile[x + 1, y];
1024	      Tile tile3 = Main.tile[x, y - 1];
1025	      Tile tile4 = Main.tile[x, y + 1];
1026	      Tile tile5 = Main.tile[x, y];
1027	      bool flag = false;
1028	      if (tile1.liquid > (byte) 0 && tile1.liquidType() == (byte) 0 || tile2.liquid > (byte) 0 && tile2.liquidType() == (byte) 0 || tile3.liquid > (byte) 0 && tile3.liquidType() == (byte) 0)
1029	      {
1030	        int num = 0;
1031	        if (tile1.liquidType() == (byte) 0)
1032	        {
1033	          num += (int) tile1.liquid;
1034	          tile1.liquid = (byte) 0;
1035	        }
1036	        if (tile2.liquidType() == (byte) 0)
1037	        {
1038	          num += (int) tile2.liquid;
1039	          tile2.liquid = (byte) 0;
1040	        }
1041	        if (tile3.liquidType() == (byte) 0)
1042	        {
1043	          num += (int) tile3.liquid;
1044	          tile3.liquid = (byte) 0;
1045	        }
1046	        if (tile1.lava() || tile2.lava() || tile3.lava())
1047	          flag = true;
1048	        if (num < 32)
1049	          return;
1050	        if (tile5.active() && Main.tileObsidianKill[(int) tile5.type])
1051	        {
1052	          WorldGen.KillTile(x, y, false, false, false);
1053	          if (Main.netMode == 2)
1054	            NetMessage.SendData(17, -1, -1, (NetworkText) null, 0, (float) x, (float) y, 0.0f, 0, 0, 0);
1055	        }
1056	        if (tile5.active())
1057	          return;
1058	        tile5.liquid = (byte) 0;
1059	        tile5.liquidType(0);
1060	        WorldGen.PlaceTile(x, y, 229, true, true, -1, 0);
1061	        if (flag)
1062	          SoundEngine.PlaySound(SoundID.LiquidsHoneyLava, new Vector2((float) (x * 16 + 8), (float) (y * 16 + 8)));
1063	        else
1064	          SoundEngine.PlaySound(SoundID.LiquidsHoneyWater, new Vector2((float) (x * 16 + 8), (float) (y * 16 + 8)));
1065	        WorldGen.SquareTileFrame(x, y, true);
1066	        if (Main.netMode != 2)
1067	          return;
1068	        NetMessage.SendTileSquare(-1, x - 1, y - 1, 3, flag ? TileChangeType.HoneyLava : TileChangeType.HoneyWater);
1069	      }
1070	      else
1071	      {
1072	        if (tile4.liquid <= (byte) 0 || tile4.liquidType() != (byte) 0)
1073	          return;
1074	        if (Main.tileCut[(int) tile4.type])
1075	        {
1076	          WorldGen.KillTile(x, y + 1, false, false, false);
1077	          if (Main.netMode == 2)
1078	            NetMessage.SendData(17, -1, -1, (NetworkText) null, 0, (float) x, (float) (y + 1), 0.0f, 0, 0, 0);
1079	        }

```


---

## 🤖 Assistant · 2026-08-09T02:55:11.556Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read the remaining parts: Liquid.cs L1079-1213 (HoneyCheck else branch, DelWater).
```

</details>


---

## 🤖 Assistant · 2026-08-09T02:55:11.558Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/Liquid.cs",
 "limit": 140,
 "offset": 1079
}
```


---

## 👤 User(sidechain) · 2026-08-09T02:55:11.570Z

**📎 ToolResult**

```
1079	        }
1080	        else if (tile4.active() && Main.tileObsidianKill[(int) tile4.type])
1081	        {
1082	          WorldGen.KillTile(x, y + 1, false, false, false);
1083	          if (Main.netMode == 2)
1084	            NetMessage.SendData(17, -1, -1, (NetworkText) null, 0, (float) x, (float) (y + 1), 0.0f, 0, 0, 0);
1085	        }
1086	        if (tile4.active())
1087	          return;
1088	        if (tile5.liquid < (byte) 32)
1089	        {
1090	          tile5.liquid = (byte) 0;
1091	          tile5.liquidType(0);
1092	          if (Main.netMode != 2)
1093	            return;
1094	          NetMessage.SendTileSquare(-1, x - 1, y, 3, TileChangeType.None);
1095	        }
1096	        else
1097	        {
1098	          if (tile4.lava())
1099	            flag = true;
1100	          tile5.liquid = (byte) 0;
1101	          tile5.liquidType(0);
1102	          tile4.liquid = (byte) 0;
1103	          tile4.liquidType(0);
1104	          if (flag)
1105	            SoundEngine.PlaySound(SoundID.LiquidsHoneyLava, new Vector2((float) (x * 16 + 8), (float) (y * 16 + 8)));
1106	          else
1107	            SoundEngine.PlaySound(SoundID.LiquidsHoneyWater, new Vector2((float) (x * 16 + 8), (float) (y * 16 + 8)));
1108	          WorldGen.PlaceTile(x, y + 1, 229, true, true, -1, 0);
1109	          WorldGen.SquareTileFrame(x, y + 1, true);
1110	          if (Main.netMode != 2)
1111	            return;
1112	          NetMessage.SendTileSquare(-1, x - 1, y, 3, flag ? TileChangeType.HoneyLava : TileChangeType.HoneyWater);
1113	        }
1114	      }
1115	    }
1116	
1117	    public static void DelWater(int l)
1118	    {
1119	      int x = Main.liquid[l].x;
1120	      int y = Main.liquid[l].y;
1121	      Tile tile1 = Main.tile[x - 1, y];
1122	      Tile tile2 = Main.tile[x + 1, y];
1123	      Tile tile3 = Main.tile[x, y + 1];
1124	      Tile tile4 = Main.tile[x, y];
1125	      byte num = 2;
1126	      if ((int) tile4.liquid < (int) num)
1127	      {
1128	        tile4.liquid = (byte) 0;
1129	        if ((int) tile1.liquid < (int) num)
1130	          tile1.liquid = (byte) 0;
1131	        else
1132	          Liquid.AddWater(x - 1, y);
1133	        if ((int) tile2.liquid < (int) num)
1134	          tile2.liquid = (byte) 0;
1135	        else
1136	          Liquid.AddWater(x + 1, y);
1137	      }
1138	      else if (tile4.liquid < (byte) 20)
1139	      {
1140	        if ((int) tile1.liquid < (int) tile4.liquid && (!tile1.nactive() || !Main.tileSolid[(int) tile1.type] || Main.tileSolidTop[(int) tile1.type]) || (int) tile2.liquid < (int) tile4.liquid && (!tile2.nactive() || !Main.tileSolid[(int) tile2.type] || Main.tileSolidTop[(int) tile2.type]) || tile3.liquid < byte.MaxValue && (!tile3.nactive() || !Main.tileSolid[(int) tile3.type] || Main.tileSolidTop[(int) tile3.type]))
1141	          tile4.liquid = (byte) 0;
1142	      }
1143	      else if (tile3.liquid < byte.MaxValue && (!tile3.nactive() || !Main.tileSolid[(int) tile3.type] || Main.tileSolidTop[(int) tile3.type]) && (!Liquid.stuck && (!Main.tile[x, y].nactive() || !Main.tileSolid[(int) Main.tile[x, y].type] || Main.tileSolidTop[(int) Main.tile[x, y].type])))
1144	      {
1145	        Main.liquid[l].kill = 0;
1146	        return;
1147	      }
1148	      if (tile4.liquid < (byte) 250 && Main.tile[x, y - 1].liquid > (byte) 0)
1149	        Liquid.AddWater(x, y - 1);
1150	      if (tile4.liquid == (byte) 0)
1151	      {
1152	        tile4.liquidType(0);
1153	      }
1154	      else
1155	      {
1156	        if (tile2.liquid > (byte) 0 && tile2.liquid < (byte) 250 && (!tile2.nactive() || !Main.tileSolid[(int) tile2.type] || Main.tileSolidTop[(int) tile2.type]) && (int) tile4.liquid != (int) tile2.liquid)
1157	          Liquid.AddWater(x + 1, y);
1158	        if (tile1.liquid > (byte) 0 && tile1.liquid < (byte) 250 && (!tile1.nactive() || !Main.tileSolid[(int) tile1.type] || Main.tileSolidTop[(int) tile1.type]) && (int) tile4.liquid != (int) tile1.liquid)
1159	          Liquid.AddWater(x - 1, y);
1160	        if (tile4.lava())
1161	        {
1162	          Liquid.LavaCheck(x, y);
1163	          for (int i = x - 1; i <= x + 1; ++i)
1164	          {
1165	            for (int j = y - 1; j <= y + 1; ++j)
1166	            {
1167	              Tile tile5 = Main.tile[i, j];
1168	              if (tile5.active())
1169	              {
1170	                if (tile5.type == (ushort) 2 || tile5.type == (ushort) 23 || (tile5.type == (ushort) 109 || tile5.type == (ushort) 199) || (tile5.type == (ushort) 477 || tile5.type == (ushort) 492))
1171	                {
1172	                  tile5.type = (ushort) 0;
1173	                  WorldGen.SquareTileFrame(i, j, true);
1174	                  if (Main.netMode == 2)
1175	                    NetMessage.SendTileSquare(-1, x, y, 3, TileChangeType.None);
1176	                }
1177	                else if (tile5.type == (ushort) 60 || tile5.type == (ushort) 70)
1178	                {
1179	                  tile5.type = (ushort) 59;
1180	                  WorldGen.SquareTileFrame(i, j, true);
1181	                  if (Main.netMode == 2)
1182	                    NetMessage.SendTileSquare(-1, x, y, 3, TileChangeType.None);
1183	                }
1184	              }
1185	            }
1186	          }
1187	        }
1188	        else if (tile4.honey())
1189	          Liquid.HoneyCheck(x, y);
1190	      }
1191	      if (Main.netMode == 2)
1192	        Liquid.NetSendLiquid(x, y);
1193	      --Liquid.numLiquid;
1194	      Main.tile[Main.liquid[l].x, Main.liquid[l].y].checkingLiquid(false);
1195	      Main.liquid[l].x = Main.liquid[Liquid.numLiquid].x;
1196	      Main.liquid[l].y = Main.liquid[Liquid.numLiquid].y;
1197	      Main.liquid[l].kill = Main.liquid[Liquid.numLiquid].kill;
1198	      if (Main.tileAlch[(int) tile4.type])
1199	      {
1200	        WorldGen.CheckAlch(x, y);
1201	      }
1202	      else
1203	      {
1204	        if (tile4.type != (ushort) 518)
1205	          return;
1206	        if (Liquid.quickFall)
1207	          WorldGen.CheckLilyPad(x, y);
1208	        else if (Main.tile[x, y + 1].liquid < byte.MaxValue || Main.tile[x, y - 1].liquid > (byte) 0)
1209	          WorldGen.SquareTileFrame(x, y, true);
1210	        else
1211	          WorldGen.CheckLilyPad(x, y);
1212	      }
1213	    }
1214	  }
1215	}
1216	

```


---

## 🤖 Assistant · 2026-08-09T02:57:36.970Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now let me carefully compare each method.

## 1. update() → Liquid.Update() L298-674

L306-310: solid check → kill=999, return. Ours: `if (this.blocksLiquid(x, y)) { e.kill = 999; return; }`. Note original sets `int type = tile5.type` (unused leftover). OK. But note: original `nactive()` requires active() && !inActive(). Our blocksLiquid checks `t===0 return false` then `d.solid && !d.platform`. Reasonable.

Wait — but our blocksLiquid for out of bounds returns true; fine.

L314-320 underworld evaporation: original: `if (this.y > Main.UnderworldLayer && tile5.liquidType() == 0 && tile5.liquid > 0)`. liquidType 0 = water. Ours: `y > h - 200 && liquidType === 1`. Consistent with encoding (1=water). Original subtracts min(2, liquid) — we do `Math.max(0, liquid-2)` — equivalent since liquid>0. OK.

L327-339 lava: lavaCheck then delay. Ours: myType===2 → lavaCheck, delay<5 → delay++, return. Consistent. Note original reads `tile5.lava()` which is liquidType==1 in original (1=lava). Ours uses myType===2 → correct translation.

L342-349: water waking lava neighbors: `tile1.lava()` = original type 1. Ours checks liquidType===2 → correct translation.

Note the order: original checks tile1 (left), tile2 (right), tile3 (up), tile4 (down). Ours: left, right, up, down. Consistent.

L350-362 honey: honeyCheck, delay 10. Ours myType===3. Original honey = liquidType 2. Correct.

L363-373: water waking honey neighbors. Ours liquidType===3. Correct.

BUT: important structural issue. Original L340 `else` — i.e., the lava branch is `if (tile5.lava()) {...} else { wake lava neighbors; if honey {...} else {wake honey neighbors} }`. Ours matches.

However there's a subtle bug in ours: in the water (non-lava) branch, we wake lava neighbors regardless of whether this tile is water or honey. Original: if tile is honey, it still runs the lava-wake block (since it's in the else of lava()). Yes original does that too. OK.

L375-397 downward flow: original condition:
`(!tile4.nactive() || !solid || solidTop) && ((tile4.liquid <= 0 || tile4.liquidType == tile5.liquidType) && tile4.liquid < 255)`

Ours: `!belowBlocks && (belowAmt <= 0 || belowType === myType) && belowAmt < 255`. Consistent.

Amount: num = 255 - belowAmt; if num > cur then cur. flag = num==1 && cur==255. if !flag subtract. add to below. liquidType. AddWater below. skipLiquid both. quickSettle && >250 → 255; else if !flag addWater left/right.

Ours: same. `if (this.quickSettle && st.liquid[i5] > 250) st.liquid[i5] = 255; else if (!flag) {...}`. Consistent.

One difference: original uses `float num` and compares `(double)num == 1.0`. Equivalent.

Note: original at L385 `tile4.liquid += (byte) num;` — potential overflow if belowAmt+num>255? Can't since num=255-belowAmt.

L398: `if (tile5.liquid > 0)` then the big side flow block inline. Ours: `if (st.liquid[i5] > 0) this.sideFlow(...)`. Consistent.

### sideFlow comparison

Original flags:
- flag1: tile1 solid → false; else if tile1.liquid>0 && type diff → false; else if x-2 solid → flag3=false; else if x-2 liquid==0 → flag3=false; else if x-2 liquid>0 && type diff → flag3=false.

Ours:
```
if (this.blocksLiquid(x - 1, y)) f1 = false;
else if (lq > 0 && st.liquidType[il] !== myType) f1 = false;
else if (this.blocksLiquid(x - 2, y)) f3 = false;
else if (st.liquid[im2] === 0) f3 = false;
else if (st.liquidType[im2] !== myType) f3 = false;
```
Consistent. Same for right.

num1: `if (tile5.liquid < 3) num1 = -1;` Ours: `< 3 → -1`. Consistent.

`if (tile5.liquid > 250) { flag3=false; flag4=false; }` Ours: consistent. Note ours reads `st.liquid[i5]` — but at this point liquid[i5] may have been modified by the downward flow; original also reads tile5.liquid at that time. Consistent.

Branch flag1&flag2 → flag3&flag4 → flag5&flag6:

7-cell: `num2 = Round((t1+t2+x-2+x+2+x-3+x+3+t5+num1)/7)`. Ours: `Math.round((lq + rq + im2 + ip2 + im3 + ip3 + i5 + num1)/7)`. Consistent.

Then original: for each neighbor: set liquidType; if liquid != num2 → set liquid & AddWater else num3++.

Ours: for each: `if (lq !== m) {...}` else set type, same++. Consistent — note ours sets liquidType in both branches. Consistent with original.

Then original L502-513: additional AddWater calls: for each of 6 neighbors, `if (neighbor.liquid != num2 || tile5.liquid != num2) AddWater(neighbor)`. Ours DOES NOT have these! Ours only has the initial conditional AddWater. This is a deviation: missing the 6 redundant AddWater calls. Impact: low — they're mostly redundant with the earlier AddWater calls except the case where neighbor==num2 but tile5 != num2 (in which case tile5 will be set to num2 since num3!=6... wait if all six equal num2, num3==6, and if tile3.liquid<=0 then tile5=num2 as well). Hmm, consider: all six neighbors == num2 (num3==6) and tile3.liquid > 0 → tile5 not set. Then original calls AddWater for each of the 6 neighbors (since tile5.liquid != num2). Ours doesn't. Those would add neighbors to the active list. This is a real behavioral difference in wake propagation. Impact: low/medium. Mark as low.

Actually wait, when would all 6 equal m but center differs? E.g. center 255, neighbors... sum+num1 over 7... possible. Impact: liquid above center continues flowing; neighbors get scheduled in original. I'd rate 低.

Same missing block for 5-cell (L553-560). Ours missing those too. Impact 低.

4-cell left (flag3): original condition `tile1.liquid != num2 || tile5.liquid != num2` → set & AddWater. Ours: `if (lq !== m || st.liquid[i5] !== m) {...}`. Consistent. Same for others.

3-cell: original `if (num2 == 254 && WorldGen.genRand.Next(30) == 0) num2 = 255;` Ours: `if (m === 254 && Math.random() * 30 < 1) m = 255;` — equivalent probability. Consistent.

3-cell sets tile1/tile2 liquidType then conditional set; ours same, including `else st.liquidType[il] = myType`. Consistent. And `tile5.liquid = num2` unconditional. Consistent.

2-cell left (flag1 only): original:
```
num2 = Round((t1 + t5 + num1)/2);
if (t1.liquid != num2) t1.liquid = num2;
t1.liquidType(t5 type);
if (t5.liquid != num2 || t1.liquid != num2) AddWater(x-1,y);
t5.liquid = num2;
```
Ours:
```
const m = round((lq + st.liquid[i5] + num1)/2);
if (lq !== m) st.liquid[il] = m;
st.liquidType[il] = myType;
if (st.liquid[i5] !== m || st.liquid[il] !== m) this.addWater(x - 1, y);
st.liquid[i5] = m;
```
Consistent. Same for right.

L652-671 kill maintenance:
```
if (tile5.liquid != liquid /*startAmt*/) {
  if (tile5.liquid == 254 && liquid == 255) {
    if (quickSettle) { tile5.liquid = 255; kill++; }
    else kill++;
  } else { AddWater(x, y-1); kill = 0; }
} else kill++;
```
Ours: identical. Consistent.

Hmm wait: original `startAmt` is `liquid` captured at L313 BEFORE underworld evaporation. Ours: `const startAmt = st.liquid[i5];` captured after solid check, before evaporation. Consistent.

But note: original captured at L313 which is after the solid check at 306. Ours also after solid check. Consistent.

## updateLiquid() → L691-833

Original num1 = 8; single player num1 stays 8. Ours killThreshold=8. Consistent.

Original cycles: default 10, set in Main to 17-10*quality... For single player high quality, per Main.cs:12240 `Liquid.cycles = 17 - 10 * Main.qualityMode`? quality 1 → 7. Ours cycles=7. Consistent (assume).

wetCounter/slice/start/end logic: ours matches, including `if wetCounter === cycles → end = numLiquid` and the clamp. One deviation: original in clamp sets wetCounter = cycles (we do too). Consistent.

quickFall loop: original sets delay=10, Update(), then `skipLiquid(false)`. Ours: same, `this.skip[...] = 0`. Consistent.

Hmm, but original sets `Liquid.quickFall = quickSettle;` and quickSettle may be OR'd with reduced liquids. Ours: `this.quickFall = quickSettle`. Consistent for our setup.

Cleanup: original `for l = numLiquid-1 down to 0: if kill >= num1: if liquid == 254 → 255; DelWater(l)`. Ours same. Consistent.

Buffer flush loop — omitted (documented). Skip.

Stuck detection: consistent.

Note: original `wetCounter >= cycles` gate — ours same.

One deviation: `if (end > this.numLiquid) { end = this.numLiquid; this.wetCounter = cycles; }` — matches original L762-767. Consistent.

Hmm, one subtle thing: original computes `num3 = curMaxLiquid / cycles` using curMaxLiquid (25000), NOT numLiquid. Ours: `Math.floor(this.curMaxLiquid / cycles)`. Consistent.

## delWater() → L1117-1213

Original:
- num = 2. if liquid < 2: set 0; if t1.liquid<2 → t1=0 else AddWater(x-1); same t2.
Ours consistent.

- else if liquid < 20: check neighbors lower and passable → set 0. Ours consistent. Note original compares `(int)tile1.liquid < (int)tile4.liquid`. Ours `lq < amt`. Consistent.

- else if tile3.liquid < 255 && passable && !stuck && center passable → kill=0; return. Ours consistent.

- L1148: if liquid < 250 && tile above liquid > 0 → AddWater(x, y-1). Ours: `if (st.liquid[i5] < 250 && st.liquid[i5 - st.w] > 0) this.addWater(x, y - 1);` Consistent.

- if liquid == 0 → liquidType(0). Ours: sets st.liquidType[i5] = 0. Consistent.

- else: right/left wake with conditions. Ours consistent (order: original checks tile2 (right) first then tile1 (left); ours also right then left at L451-452. Yes consistent).

- if lava: LavaCheck + 3×3 grass/plant conversion (types 2,23,109,199,477,492 → 0; 60,70 → 59). Ours approximates by clearing decor with attach==='ground'. Documented approximation. Report as deviation (低/中). The comment claims 原版为草方块转换 — 60/70→59 is grass conversion. Our approximation clears decor plants only, doesn't convert grass blocks to dirt, and doesn't remove mushrooms(23)/flowers etc unless decor. Impact 低.

- else if honey: HoneyCheck. Ours: `else if (st.liquidType[i5] === 3) this.honeyCheck(x, y);` Consistent.

- swap remove: original L1193-1197: numLiquid--; checkingLiquid(false); liquid[l] = liquid[numLiquid] (x,y,kill — note delay NOT copied). Ours: numLiquid--; checking=0; liquids[l] = liquids[numLiquid]; liquids.length = numLiquid.

Hmm! Important: ours sets `this.liquids.length = this.numLiquid` after swap. That truncates the array. Then `liquids[this.numLiquid] = {...}` on addWater re-adds. That's fine functionally. But one behavioral difference: original does NOT copy delay. Ours copies the whole object including delay. So the swapped-in entry keeps its old delay in ours, whereas original resets delay to stale value of the removed last slot (which original also keeps actually — Main.liquid[l].delay is not overwritten, so it retains the removed entry's delay!). Original: liquid[l].x/y/kill copied but delay NOT → delay keeps old value of the slot l (the removed one), not the last one's. Ours: delay = last entry's delay. This is a subtle difference in lava/honey slowdown after swap-remove. Impact: 低 (delays reset to 0 quickly for lava/honey anyway... actually delay persists and affects timing). Let me think: In original, after swap, slot l keeps the delay value it had (from the entry just deleted). That entry was being deleted after kill>=8 so its delay was likely 0 or small. In ours, the moved entry brings its own delay. Both arbitrary. 低.

Also `liquids.length = numLiquid` — potential issue in the cleanup loop: iterating l from numLiquid-1 down to 0, delWater(l) swaps last into l. Ours truncates array each time; fine.

But there's a real bug risk: in `updateLiquid` quickFall loop and normal loop we iterate `l` from start to end while `update()` calls `addWater` which appends at numLiquid — fine, no removal during update. But `lavaCheck`... doesn't call delWater. OK.

However — `this.liquids.length = this.numLiquid` in delWater while iterating downward: fine.

Another: in delWater, ours does `this.liquids.length = this.numLiquid;` but the entry object at index l is replaced by reference to the last object. OK.

Also original: `Main.tile[Main.liquid[l].x, Main.liquid[l].y].checkingLiquid(false);` uses liquid[l].x BEFORE swap (the entry being removed). Ours: `this.checking[i5] = 0` using e.x,e.y. Consistent.

Wait — actually there's an ordering subtlety: original sets checkingLiquid(false) BEFORE overwriting liquid[l]. Ours sets checking[i5]=0 then swaps. Consistent.

## lavaCheck() → L888-1016

Original start: UndergroundDesertCheck (gen only) — skip; ours skips. Fine.

`if (WorldGen.SolidTile(x, y, false)) return;` Ours: `if (this.blocksLiquid(x, y)) return;`. Consistent-ish. WorldGen.SolidTile checks nactive/solid/!solidTop for the tile itself. blocksLiquid equivalent. OK.

Note ours blocksLiquid returns true for out-of-bounds; SolidTile would be false for OOB. Edge only.

Case A: `if (tile1.liquid > 0 && !tile1.lava() || tile2... || tile3...)`. Ours: `(lq > 0 && lt !== 2) || ...` where 2=lava in our encoding. Correct.

num accumulation: original `if (!tile1.lava()) { num += tile1.liquid; tile1.liquid = 0; }`. Ours: `if (lt !== 2) { sum += lq; st.liquid[il] = 0; }`. Consistent. Note: original's `!tile1.lava()` is true even when tile1.liquid==0 (empty tile is not lava) — adds 0. Ours same (lt would be 0 for empty → !==2 → adds 0). Consistent.

Type: `if (tile1.honey() || tile2.honey() || tile3.honey()) Type = 230;` Ours: `if (lt === 3 || rt === 3 || ut === 3) type = CRISPY_HONEY;`. Hmm: original tile1.honey() is liquidType==2 (honey), independent of liquid>0. For empty tile liquidType may be stale honey → Type 230 even with no honey liquid! Ours: `lt === 3` same semantics — liquidType array value regardless of liquid amount. Consistent actually. OK.

`if (num < 24) return;` Ours: `if (sum < 24) return;` Consistent.

Then: `if (tile5.active() && Main.tileObsidianKill[type]) KillTile`. Ours: if tile non-empty and decor → setTile 0; else return if solid non-decor.

**DEVIATION**: original `if (tile5.active()) return;` at L943 (non-getGoodWorld) — i.e., if there is ANY active tile at the lava cell, return (no obsidian), EXCEPT obsidianKill tiles which were killed. Ours: `if (t !== 0) { if decor → clear; else return; }`. That matches: active tile → unless obsidianKill(decor approx) → return. But approximation: our `d.decor` ≈ tileObsidianKill? tileObsidianKill includes torches, plants, etc. Our decor presumably includes plants/torches. Approximation documented. Then `tile5.liquid = 0; tile5.lava(false); PlaceTile(x,y,Type)`. Ours: liquid=0, liquidType=0, setTile type. Consistent. Note original doesn't clear the water type explicitly — lava(false) → liquidType 0 = water encoding 0. Ours sets liquidType=0 which in OUR encoding means "none/water"? Wait — our encoding 1=water 2=lava 3=honey, and 0 presumably = no liquid. Original 0=water. In ours, water is 1. So `st.liquidType[i5] = 0` means "no type" — consistent with liquid=0. But note: in the case-A else where lava cell becomes obsidian, liquid=0 so type irrelevant. Fine.

Hmm wait, in lavaCheck case A ours sets `st.liquidType[i5] = 0` but our encoding for water is 1. Since liquid[i5]=0 simultaneously, type value is cosmetic. But in `delWater` when lava check kills the cell... fine.

Case B: `if (tile4.liquid <= 0 || tile4.lava()) return;` Ours: `if (dq <= 0 || dt === 2) return;` Correct.

Original: `bool flag=false; if (tile5.active() && IsAContainer[tile5.type] && !IsAContainer[tile4.type]) flag = true;` — container exception. Ours: MISSING the container check. Ours checks `belowT !== 0` and if decor → clear, else return. Original: if tile4.tileCut → KillTile(x,y+1); else if tile4.active && tileObsidianKill → KillTile; then `if (!(!tile4.active() | flag)) return;` — i.e., proceed only if below tile inactive OR container-flag.

**DEVIATION**: ours has no IsAContainer exception → lava inside a container (e.g., placed on top of a table? no—tile4 is below) ... The flag case: tile5 (lava cell) active container and tile4 not container → proceeds even if tile4 active. Ours would `return` if below tile is non-decor non-empty. E.g. lava sitting in a chest?? Impact 低 (our tile set may not have containers).

Then `if (tile5.liquid < 24) { liquid=0; liquidType(0); return; }` Ours: same but note original sets `tile5.liquidType(0)` = water in original encoding. Ours sets 0 = none. Fine.

Else: Type 56 or 230 if tile4.honey(). Ours: `dt === 3 ? CRISPY : OBSIDIAN`. Correct. Then tile5 liquid 0, lava(false), tile4 liquid 0, PlaceTile(x, y+1, Type). Ours: sets liquid[i5]=0, type[i5]=0, liquid[id]=0, liquidType[id]=0, setTile(x, y+1, type). Consistent. Note ours also clears liquidType[id] — original does NOT clear tile4.liquidType in LavaCheck case B (only liquid). Wait L1004: `tile4.liquid = (byte) 0;` — no liquidType reset. Since liquid=0, irrelevant. Low.

**DEVIATION (significant)**: In case B, original checks `tile5.liquid < 24` → clears lava and returns, WITHOUT requiring the sum of anything. Ours matches. But note that in case B, original requires `!tile4.active() | flag` before even the <24 check. Ours returns early if below tile is solid non-decor. Match-ish.

Also **missing getGoodWorldGen branch** (L934-940, L990-996): 10th anniversary seed "remix" where lava/water convert each other instead of obsidian. Impact 低 (special seed only).

Also **PlaceTile(x, y, Type, true, true, -1, 0)** — the `true` for forced + ... PlaceTile with force=true can replace existing tiles. We use setTile. Fine.

Also **SquareTileFrame** omitted → no 3×3 wake of neighbors via framing. Ours does `st.setTile(x,y,type)` which presumably triggers onTileChanged → addWater 3×3. Actually our constructor registers onTileChanged → addWater 3×3 around changed tile. That approximates SquareTileFrame. OK.

## honeyCheck() → L1018-1115

Case A: `if (tile1.liquid > 0 && tile1.liquidType() == 0 || ...)` — original: neighbor liquidType == 0 (water). Ours: `lt === 1` (water). Correct.

Accumulate: `if (tile1.liquidType() == 0) { num += ...; tile1.liquid = 0; }` Ours: `if (lt === 1) {...}`. Consistent.

`if (tile1.lava() || tile2.lava() || tile3.lava()) flag = true;` — flag only used for sound. Ours ignores. Fine.

`if (num < 32) return;` Consistent.

`if (tile5.active() && tileObsidianKill) KillTile; if (tile5.active()) return;` Ours: if t!==0 { if decor clear; else return }. Consistent with approximation.

Then liquid=0, liquidType(0), PlaceTile 229. Ours consistent.

Case B: `if (tile4.liquid <= 0 || tile4.liquidType() != 0) return;` Ours: `dq <= 0 || dt !== 1`. Correct.

`if (tileCut[tile4.type]) KillTile(x,y+1); else if (tile4.active() && tileObsidianKill) KillTile;` `if (tile4.active()) return;` Ours: if belowT!==0 { decor→clear; else return }. Consistent.

`if (tile5.liquid < 32) { liquid=0; type=0; return }` Ours consistent.

Else: `if (tile4.lava()) flag=true;` (sound only). tile5 liquid 0, type 0; tile4 liquid 0, type 0; PlaceTile(x,y+1,229). Ours consistent.

Note honeyCheck type always 229 even if neighbor is lava — consistent with ours (HONEY_BLOCK always).

## attemptToMoveLiquid → L214-280

Original AttemptToMoveLava(X, Y, tileAtXYHasLava): `tileAtXYHasLava` is a bool captured at SettleWaterAt start: `bool tileAtXYHasLava = tile1.lava();` — i.e., whether the ORIGIN tile had lava.

Ours: `attemptToMoveLiquid(X, Y, srcType, 2)` where srcIs = srcType===2. Then `diff(x,y)` = liquid>0 && (liquidType===targetType) !== srcIs. For lava: neighbor.lava() != tileAtXYHasLava. Original checks `Main.tile[X-1,Y].lava()` — lava() is liquidType==1 (original). Hmm, lava() in Terraria's Tile: `public bool lava() => (int) this.liquidType() == 1;`? Actually in Terraria, `lava()` checks `liquidType == 1`? Let me recall: Tile.lava() => this.liquidType() == 1... Hmm, actually there are `lava()`, `honey()` methods that check the liquidType bits. lava() is true when liquidType == 1, honey() when == 2. Yes.

Ours: `st.liquidType[i] === targetType` where targetType=2 for lava in our encoding. Correct translation.

BUT: there's a subtle discrepancy. Original passes `tileAtXYHasLava` = whether the ORIGIN had lava — but note that if the origin had water (not lava), `tileAtXYHasLava=false`, and then any neighbor with lava() == true → `lava() != false` → LavaCheck(X-1, Y) (the neighbor). If origin had lava, tileAtXYHasLava=true, and neighbor NOT lava (i.e., water/honey) → LavaCheck(X, Y) (self). Ours: srcIs = srcType===2; diff = (type===2) !== srcIs; if diff: if srcIs → check(X,Y) else check(neighbor). Consistent. 

Wait — one difference: original `Main.tile[X-1, Y].liquid > 0 && ...lava() != tileAtXYHasLava`. If origin had water and neighbor has HONEY (not lava), then lava()=false == tileAtXYHasLava=false → no check. Ours: `(liquidType===2) !== false` → honey type 3 !== 2 → false !== false → false. Consistent.

OK, consistent. Except: ours calls attemptToMoveLiquid(X, Y, srcType, 2) then (…, 3) — matching original's AttemptToMoveLava then AttemptToMoveHoney. Consistent.

One subtle: original checks `Main.tile[X, Y + 1].liquid <= 0` in the final else. Ours diff handles. Consistent.

## settleWaterAt → L105-212

Original: 
```
if (tile1.liquid == 0) return;   // L109-110
...
bool tileAtXYHasLava = tile1.lava();
bool tileAtXYHasHoney = tile1.honey();
int liquid = tile1.liquid;
byte num1 = tile1.liquidType();
tile1.liquid = 0;
bool flag1 = true;
while(true) {
  Tile tile2 = Main.tile[X, Y+1];
  bool flag2 = false;
  for (; Y < maxTilesY-5 && tile2.liquid == 0 && passable(tile2); tile2 = next) { Y++; flag2=true; flag1=false; }
  if (flag2 && WorldGen.gen && !tileAtXYHasHoney && Y > waterLine) num1 = 1;
  ...
}
```

Ours: vertical loop `while (Y < st.h - 5 && liquid[idx(X,Y+1)]===0 && !blocksLiquid(X,Y+1))`. Consistent. Note ours checks st.liquid at idx(X,Y+1) each iteration (original uses tile2 variable updated in for-increment). Consistent.

We skip the waterLine conversion (gen only) — noted in comment. Fine.

Serpentine: original num2=-1 (dir), num3=0 (step), num4=-1 (lastDir), num5=0 (lastStep), flag3 (right hit), flag4 (left hit), flag5 (dropped).

Ours: dir=-1, step=0, lastDir=-1, lastStep=0, hitR=false (flag3), hitL=false (flag4), dropped=false (flag5). Consistent naming.

Inner loop:
- `if (tile[X+num3*num2, Y].liquid == 0) { num4=num2; num5=num3; }` Ours: `if (st.liquid[ci] === 0) { lastDir = dir; lastStep = step; }`. Consistent.
- `if (num2 == -1 && X + num3*num2 < 5) flag4 = true; else if (num2 == 1 && X+num3*num2 > maxTilesX-5) flag3 = true;` Ours: `if (dir === -1 && X + step*dir < 5) hitL = true; else if (dir === 1 && X + step*dir > st.w - 5) hitR = true;` Consistent.

Hmm wait, original flag4 = left, flag3 = right. And later `if (num2 == 1) flag3 = true; else flag4 = true;` when blocked. And `if (!(flag4 & flag3)) { if (flag3) { num2=-1; ++num3; } else if (flag4) { if (num2==1) ++num3; num2 = 1; } else { if (num2==1) ++num3; num2 = -num2; } } else goto label_34;`

Ours:
```
if ((nAmt !== 0 && (!flag1 || dir !== 1)) || nSolid) {
  if (dir === 1) hitR = true; else hitL = true;
}
if (hitL && hitR) break;
if (hitR) { dir = -1; step++; }
else if (hitL) { if (dir === 1) step++; dir = 1; }
else { if (dir === 1) step++; dir = -dir; }
```
Consistent (flag4=hitL, flag3=hitR). Good.

- tile3 = tile[X+num3*num2, Y+1]; `if (tile3.liquid != 0 && tile3.liquid != 255 && tile3.liquidType() == num1) { num6 = 255 - liquid; if (num6 > liquid) num6 = liquid; tile3.liquid += num6; liquid -= num6; if (liquid==0) goto label_34; }`

Ours: same, `if (liquid === 0) break;` — WAIT. Original `goto label_34` jumps OUT of the inner loop to `label_34:` which is AFTER `flag5 = true;`? Let's look:

```
        flag5 = true;
label_34:
        X += num5 * num4;
        if (liquid != 0 && flag5)
          ++Y;
        else
          break;
```

So `flag5 = true; label_34: X += ...`. If liquid==0 via goto label_34, flag5 is NOT set to true (jump lands after flag5=true). Then `if (liquid != 0 && flag5)` → liquid==0 → break outer. So X is updated by num5*num4 but Y unchanged, then break.

Ours: `if (liquid === 0) break;` inside inner loop — this breaks inner loop, then `X += lastStep * lastDir;` then `if (liquid !== 0 && dropped) Y++; else break;` → break. Same result! Because flag5 stays false → outer break. And X updated. Consistent. 

But hold on — in ours, `dropped` is only set in the else branch (below open → dropped=true; break). Original: `else break;` (L193-194) exits inner while, then `flag5 = true;` at L196. So when below is open, flag5=true, then X += num5*num4, Y++ and continue outer. Ours: dropped=true; break → then X += ..., `if (liquid !== 0 && dropped) Y++` → continue outer. Consistent.

Hmm but subtle: in original, when the below-open break happens at L194, execution flows to L196 flag5=true then label_34: X += num5*num4. Ours same. Good.

- `if (Y >= maxTilesY-5 || tile3.liquid != 0 || tile3.nactive() && solid && !solidTop)` → blocked check. Ours: `if (Y >= st.h - 5 || st.liquid[bi] !== 0 || this.blocksLiquid(...))`. Consistent.

- blocked: tile4 = tile[X+(num3+1)*num2, Y]; `if (tile4.liquid != 0 && (!flag1 || num2 != 1) || tile4.nactive() && solid && !solidTop)`. Ours: `if ((nAmt !== 0 && (!flag1 || dir !== 1)) || nSolid)`. Consistent.

- Final write: `Main.tile[X,Y].liquid = liquid; liquidType(num1); if (liquid > 0) { AttemptToMoveLava; AttemptToMoveHoney; }`. Ours consistent.

Now the boundary: original inner loop accesses `X + num3 * num2` which can go out of [5, maxTilesX-5]... the loop breaks via flag4/flag3 before going too far (bounds 5 and maxTilesX-5). Ours uses idx() directly — could go out of array if X+step*dir goes beyond? The hitL/hitR checks stop stepping beyond, similar to original. Since original relies on array bounds of Main.tile (full world), accessing x=4 etc is fine. Ours: at step where X+step*dir === 5 → not < 5 → hitL not set; then next iteration step increases... wait when dir=-1 and blocked-right path: `if (hitR) { dir = -1; step++; }` — hmm step++ means next cell X + (step+1)*(-1) = previous cell -1 further left. So position moves left one per iteration. It stops when position < 5 → hitL. At position 4, it reads tile[4] then sets flag4 (hitL). Then checks X+(num3+1)*num2 = position-1 = 3 → in original world array valid. In ours idx(3, Y) valid too (x>=0). Fine. But also `bi` at X+step*dir, Y+1 → x=3 fine. OK, no OOB as long as x stays >= 0. Since hitL breaks at x<5... wait: once hitL set, next iteration: `if (hitL && hitR) break` only breaks if both. `else if (hitL) { if (dir===1) step++; dir = 1; }` → reverses to right. So it oscillates. Position range roughly [4, maxTilesX-4]. Our addWater bounds [5, w-5) but that's only for scheduling. Array access fine. Not a deviation per se.

One difference: ours `quickWater` default minY=3, maxY=-1→h-3; loop y from yMax down to minY; x from 4 to w-4. Consistent with original (minY=3, maxY=maxTilesY-3, x from 4 to maxTilesX-4).

Note original QuickWater also sets `Main.tileSolid[379] = true;` (bubbles) and tilesIgnoreWater(true) — meaning during settling, certain non-solid tiles (138 cobweb? 484, 546) are treated solid. Specifically tilesIgnoreWater(true) sets tileSolid[138]=false, [484]=false, [546]=false — i.e., ignoring solids: webs (138), 484, 546 become non-solid so liquid passes. Ours blocksLiquid doesn't consider those; if our tile defs mark those solid, deviation. Uncertain — 待确认. Impact 低.

Also Update() L300 `Main.tileSolid[379] = true;` — bubble solid. Minor.

## addWater → L835-872

Original: `if (tile == null || checkingLiquid() || (x >= maxTilesX-5 || y >= maxTilesY-5) || (x < 5 || y < 5 || liquid == 0) || (nactive && tileSolid && type != 546 && !tileSolidTop)) return;`

Note: `checkTile.type != 546` — type 546 exempt from solid rejection. Ours: rejects solid non-platform regardless. 待确认/低.

Ours: `if (x >= st.w - 5 || y >= st.h - 5 || x < 5 || y < 5) return;` Consistent.

`if (numLiquid >= curMaxLiquid - 1) → LiquidBuffer.AddBuffer(x,y)` (keep checkingLiquid false). Ours: return (drop). Documented. Impact: 中 in extreme cases (liquid activity stalls when at cap vs buffered). Documented so mention briefly.

Then checkingLiquid(true), skipLiquid(false), kill=0, x,y, delay=0, numLiquid++. Then CheckWaterDeath → KillTile. Ours documented omission. 低.

## waterCheck → WorldGen.cs:48955-49009

Original order per tile:
1. checkingLiquid(false)
2. if liquid>0 && nactive && solid && !solidTop → liquid = 0
3. else if liquid > 0: { CheckLavaDeath/CheckWaterDeath KillTile; tile1 = below; if below passable && below.liquid < 255 { if below.liquid > 250 → 255 else AddWater }; tile2 = left, tile3 = right; if left passable && left.liquid != this.liquid → AddWater; else if right passable && right != → AddWater; if lava: left/right/up/down non-lava liquid → AddWater }

Ours:
```
if (st.liquid[i] === 0) continue;   // <-- skips the checkingLiquid(false) and combines
solid → clear, continue
below check → addWater or 255
left/right checks
lava 4-neighbor check
```

Differences:
- Ours `continue` when liquid===0 → equivalent to original's else-if structure (original does nothing when liquid==0 except clear checking flag). But ours does NOT call `checking.fill(0)` per tile... actually ours does `this.checking.fill(0)` at the start. Equivalent.
- **DEVIATION**: original lava wake block uses `else if` chain: left non-lava → AddWater; ELSE IF right; ELSE IF up; ELSE IF down. Ours uses `||` in one condition → AddWater once. Same effect (AddWater idempotent due to checking flag, and it's the same cell). Equivalent. Fine.
- **DEVIATION (real)**: original lava condition: `tile2.liquid > 0 && !tile2.lava()` — checks !lava() i.e., liquidType != 1 (could be water OR honey). Ours: `st.liquidType[il] !== 2` (not lava in our encoding → water or honey). Consistent.
- Ours lava block checks `dq > 0 && st.liquidType[id] !== 2` for below. Original: `tile1.liquid > 0 && !tile1.lava()`. Consistent.

Hmm what about the tileCut/water-death kill (CheckWaterDeath) — omitted, documented.

One more: original checks the below tile using `tile1.nactive() && Main.tileSolid...` i.e. passable check on below. Ours `!this.blocksLiquid(x, y+1)`. Consistent.

Also original: `if (checkTile.liquid > (byte)0 && checkTile.nactive() && ...)` solid → clear. Ours: `if (t !== 0 && d.solid && !d.platform) { st.liquid[i] = 0; continue; }`. Consistent.

Now, waterCheck scan order: original outer x 1..maxTilesX-2, inner y from maxTilesY-2 down to 1. Ours: `for x = 1..w-2 { for y = h-2 down to 1 }`. Consistent.

## update() misc

Underworld: original `Main.UnderworldLayer` — typically maxTilesY - 200. Ours `h - 200`. Consistent approximation.

Now let me check a critical thing in `update()`: the original underworld evaporation happens when `this.y > Main.UnderworldLayer`. Ours `y > h - 200`. OK.

Another critical: in update(), ours calls `this.lavaCheck(x, y)` for lava and then the delay gate. But original: LavaCheck may PLACE OBSIDIAN at (x,y), after which tile5.liquid was set 0 — then `if (!quickFall) { if delay<5 ...}` continues and the downward flow block executes with liquid==0 (no-op) and sideFlow skipped (liquid>0 false), then kill maintenance: liquid != startAmt → 254/255? liquid==0, startAmt==X → else branch AddWater(x, y-1), kill=0. Ours behaves the same since lavaCheck sets liquid 0. Consistent.

Now check `blocksLiquid` vs `nactive() && tileSolid && !tileSolidTop`:
- nactive() = active() && !inActive(). Our t!==0 approximates active.
- tileSolidTop platforms passable. Ours uses `d.platform`. Reasonable.
- Original also has special tiles: during Update, `Main.tileSolid[379] = true` (bubble). Minor.

Now let me look for other files that may reveal TILE defs... not needed.

Let me now check specific numeric issues:

1. `addWater` boundary: original rejects `x >= maxTilesX - 5` i.e. x in [5, maxTilesX-6]. Ours: `x >= st.w - 5` reject → same range. Consistent.

2. In `update()` step 4, original condition `(!tile4.nactive() || ...)` — for y+1 == h (bottom row), tile4 out of range? Main.tile handles via Tile[,] without bounds check? Actually Main.tile[x,y] with y = maxTilesY throws. But liquid can't exist there since addWater excludes y >= h-5. Ours explicitly guards. Fine.

3. cycles: check Main.cs:12240 to verify 17-10*quality.

Let me grep Main.cs.

4. One more potential deviation in updateLiquid: original `Liquid.quickFall = quickSettle;` where quickSettle local possibly OR'd with reduced max liquids. Fine.

5. `stuckAmount` init: original stuckAmount=0; ours -99999. Minor behavioral difference at startup: with numLiquid>0 and numLiquid > -50 and < 50 → stuckCount++ immediately. Original: numLiquid > 0 && numLiquid > -50 && numLiquid < 50 → also true for small values. Actually original stuckAmount=0 gives same behavior for numLiquid<50! So original also increments stuckCount when numLiquid in (0,50). Ours with -99999: numLiquid > -99999-50 && numLiquid < -99999+50 → false → stuckCount=0, stuckAmount=numLiquid. So different init semantics but negligible. 低/可忽略. Maybe worth one line as 低.

6. In `delWater`, original's third branch condition includes `!Liquid.stuck && center passable`. Ours consistent.

7. In `delWater` ours: after the three branches, `if (st.liquid[i5] < 250 && st.liquid[i5 - st.w] > 0) this.addWater(x, y - 1);` — consistent with L1148. But note: original uses tile4.liquid which may have been zeroed in branches 1/2. Ours same.

8. Original DelWater does NOT reset `delay` on swap (as discussed). Also original copies x, y, kill from last slot but delay remains from removed slot. Ours copies whole entry. 低.

Now the notable HIGH deviations I should verify more carefully:

A. **Missing AddWater wake calls in 7-cell and 5-cell sideFlow branches** (L502-513, L553-560). Let me double check ours: in the 7-cell branch ours only does per-cell `if (... !== m) {... addWater ...}` and no extra block. Original additionally calls AddWater for each neighbor when `neighbor != num2 || tile5 != num2`. This matters when neighbor==num2 but tile5 != num2: then neighbor was NOT added in first pass but original adds it. When does that happen with all... e.g., num3 < 6. Example: neighbors (10,10,10,10,10,10), center 255 → sum=310+num1(0 for 255)... (60+255)/7 = 45. Then all neighbors != 45 → added anyway. Hmm. For neighbor==m while center != m: possible when num3<6. E.g., neighbors (50,50,50,50,50,52), center 50: sum = 352+0 /7 = 50.28 → Round=50. num3: five cells equal 50 → num3=5. Center 50==num2 → hmm center equals too. Try center 49, neighbors (50,50,50,50,50,51): sum=350/7=50 → all six neighbors == 50 → num3=6 → extra AddWater calls happen (6 of them) and tile5.liquid!=50 → all six AddWater called. Then `if (num3 != 6 || tile3.liquid <= 0)` → num3==6 and tile3>0 → tile5 NOT updated → center stays 49. So original wakes all six neighbors; ours doesn't. The neighbors then re-run and may re-average. Impact: 低-中. I'd call it 中 for wake propagation correctness in 7/5-cell case. Actually in 5-cell same pattern: num2==4 and tile3>0 → center keeps old value, neighbors all woken in original. I'll rate 中 for combined.

B. **attemptToMoveLiquid target check for honey when origin is water**: original AttemptToMoveHoney uses `honey()`; ours type 3. Consistent.

C. **`liquidType` write in 2-cell and 3-cell branches ordering**: consistent.

D. **lavaCheck/honeyCheck missing `getGoodWorldGen` branch** — 低.

E. **lavaCheck missing IsAContainer exception (L965-967, 980)** — 低.

F. **tileObsidianKill/tileCut approximation via `d.decor`** — documented; the difference: original also kills via KillTile which triggers item drops, frames, etc. And our check `d.decor` may not cover torches if torch isn't decor. 待确认. Also original `Main.tileCut` for plants below in case B. Ours uses decor too. 低.

G. **DelWater lava 3×3: original converts grass (60/70)→dirt(59) and removes specific plants/mushrooms (2,23,109,199,477,492); ours removes decor with attach==='ground'** — approximation, misses grass conversion. 低.

H. **stuckAmount init -99999 vs 0** — 低.

I. **swap-remove delay semantics** — 低.

J. **AddWater drops at cap instead of buffering** — documented; 中 in pathological cases. The user asked to report deviations; this is documented in header but still a deviation. Include as 低/中. I'll say 中 with note.

K. **AddWater type 546 exemption missing** — 低/待确认.

L. **tilesIgnoreWater during Update/QuickWater/WaterCheck (webs 138, 484, 546 treated passable)** — 待确认, 低.

M. **UnderworldLayer = h-200 approximation** — that's given by user, skip.

N. In `update()` water-branch lava-wake: original checks `tile1.lava()` where tile1 is left neighbor *cached at L301-304 BEFORE any modification*. In ours we read fresh. Within this point no modification happened yet. Consistent.

O. **Important**: original L314 evaporation uses `tile5.liquidType() == 0` — water only. Ours `=== 1`. Correct.

P. In update step 4, ours uses `belowType === myType` but original compares `tile4.liquidType() == tile5.liquidType()` — same. Consistent. Note: if belowAmt<=0, belowType may be stale; original same. Consistent.

Q. sideFlow: `if (st.liquid[i5] > 250) { f3 = false; f4 = false; }` — original `tile5.liquid > 250`. Consistent.

R. 4-cell branch: original sets liquidType BEFORE the conditional (L568, 574, 580). Ours sets type inside the if only: `if (lq !== m || center !== m) { type; value; addWater }`. 

**DEVIATION**: In original 4-cell branches, `tile1.liquidType(...)` is called UNCONDITIONALLY, before the if. Ours only writes liquidType when the condition holds. Since f1/f2/f3 gating already ensured neighbor type matches myType (f1 false if type differs... wait f1 requires tile1.liquid>0 && type diff → f1 false. But if tile1.liquid == 0, type may differ (stale), and flag1 stays true). So in the 4-cell branch (f1&f2 true, so tile1 either liquid 0 or same type), if tile1.liquid==0 with stale type, original overwrites type to myType; ours doesn't. Impact: 低 (type of empty cell, will be set when liquid flows in). Also in 7/5-cell branches ours writes type in both branches — consistent there. 3-cell: original unconditional type write before if; ours has else branch writing type. Consistent! Ours: `if (lq !== m) {...} else st.liquidType[il] = myType;` — consistent. 2-cell: ours sets type unconditionally. Consistent.

So deviation only in the two 4-cell branches. 低.

S. In 7-cell, ours computes `same` and then center condition. Original `num3 != 6 || tile3.liquid <= 0` → set. Ours: `if (same !== 6 || st.liquid[iu] <= 0) st.liquid[i5] = m;` Consistent. 5-cell: `num2 != 4 || tile3.liquid <= 0`. Ours: `same !== 4 || ...` Consistent.

T. quickWater: ours iterates `if (st.liquid[this.idx(x, y)] !== 0) this.settleWaterAt(x, y);` — original `!= 0` → SettleWaterAt. Consistent. Note settleWaterAt sets liquid of source to 0 immediately and writes final elsewhere — during the y-descending scan, could write into a row already processed (below) — original same behavior. Consistent.

U. settleWaterAt: ours `if (st.liquid[oi] === 0) return;` — but original also had `Liquid.tilesIgnoreWater(true)` per call. Covered.

V. settleWaterAt — **check the "flag1" semantics**: original `flag1` starts true, set false once any vertical drop occurred. Used in `(!flag1 || num2 != 1)`. Ours same (`flag1` variable). Consistent.

W. settleWaterAt: original inner loop reads `tile3 = Main.tile[X + num3*num2, Y+1]` BEFORE the flag checks? Order in original: (1) record empty cell, (2) boundary flags, (3) tile3 below-current; fill if same type & not full; (4) blocked check on tile3; (5) if blocked, next-cell check. Ours order: (1) ci empty record, (2) boundary flags, (3) bi fill check, (4) blocked check with next cell. Consistent order.

Hmm wait, one subtle thing: in ours, `bi` fill check happens for the CURRENT cell (X + step*dir, Y+1) — original same (tile3). Consistent.

X. **settleWaterAt writes `st.liquidType[fi] = srcType` even when liquid could be... fine.**

Y. Original SettleWaterAt: after writing, `if (Main.tile[X,Y].liquid > 0)` — ours same.

Z. waterCheck: ours `if (dq > 250) st.liquid[id] = 255; else this.addWater(x, y);` Consistent.

AA. waterCheck lava block in original is `if (checkTile.lava())` — i.e., the tile's own liquidType==1. Ours `st.liquidType[i] === 2`. Correct.

BB. **Potential deviation**: waterCheck ours, the left/right AddWater conditions: original `(!tile2.nactive() || ...) && tile2.liquid != checkTile.liquid` → AddWater; `else if` right. Ours: `if (...) addWater else if (...) addWater`? Let me look:

```ts
if (!this.blocksLiquid(x - 1, y) && st.liquid[il] !== st.liquid[i]) this.addWater(x, y);
else if (!this.blocksLiquid(x + 1, y) && st.liquid[ir] !== st.liquid[i]) this.addWater(x, y);
```
Consistent (else-if). Good.

CC. Now the biggest one I should double check: **update() step 4 `addWater(x, y + 1)`** then `skip[bi] = 1`. Original: `Liquid.AddWater(this.x, this.y+1); tile4.skipLiquid(true); tile5.skipLiquid(true);`. Consistent order.

DD. update() kill maintenance — ours reads `st.liquid[i5] !== startAmt` — original compares to `liquid` (captured at L313). Consistent.

EE. **update() when tile becomes solid**: ours `e.kill = 999; return;` — original same. Consistent.

FF. One more: **underworld evaporation for lava/honey** — original only water. Consistent.

GG. **updateLiquid quickFall sets e.delay = 10** then Update; for lava, `!quickFall` false so no delay gate. Consistent.

HH. `step()` being called every 2 ticks — external; original WorldGen.UpdateWorld calls UpdateLiquid every... not our concern.

Now check `cycles` value: let me grep Main.cs line 12240 area to verify `17 - 10 * qualityMode`. Also verify `curMaxLiquid`.

Also check whether `Liquid.cycles` might be `17 - 10 * Main.qualityMode` → quality 1 (high?) Actually Terraria qualityMode: 0=low? Let me check.

Let me also verify Tile.lava()/honey() encoding to confirm 0=water,1=lava,2=honey in liquidType.

Also double-check our `lavaCheck` case A `type` selection: original checks tile1/2/3.honey() → 230. Ours checks lt/rt/ut === 3. But original `honey()` — is it `liquidType()==2`? Need to check Tile.cs.

Also there's one more important thing: In original LavaCheck case A, after `if (tile5.active()) return;` — for the non-getGoodWorld path. But before that, `if (tile5.active() && tileObsidianKill) KillTile`. KillTile sets active false. So flow continues. Ours: decor → setTile(0), then proceeds. Consistent.

But **critical**: ours `st.setTile(x, y, 0)` triggers onTileChanged → addWater 3×3 — original KillTile + SquareTileFrame also wakes. Fine.

Now, in lavaCheck case A, ours sets `st.liquidType[i5] = 0` — but wait, our encoding: 0 = ? If water is 1, then 0 must be "empty". Since liquid=0, fine. BUT in `delWater` and elsewhere, we compare `st.liquidType[i5] === 2` for lava — for an empty cell with stale type 2? e.g., lavaCheck case B clears lava cell: ours sets liquidType=0 (empty) but does NOT reset the BELOW cell's type (`st.liquidType[id] = 0` — actually we DO set it: `st.liquid[id] = 0; st.liquidType[id] = 0;`). Original doesn't reset tile4 type but leaves stale. Since liquid=0, no effect. Consistent enough.

Hmm, but there IS a potential issue: original LavaCheck case A: `tile5.lava(false)` — sets liquidType to 0 = water in original encoding, while ours sets 0 = "none". If elsewhere our code checks `liquidType === 1` for water on a cell with liquid==0... doesn't happen because checks always guard liquid>0. OK.

One more area — `update()`: the water wake-lava loop. Original wakes lava neighbors only for non-lava tiles. Ours loops 4 neighbors and calls addWater for type 2. But note the order: original tile1(left), tile2(right), tile3(up), tile4(down) — ours [x-1],[x+1],[x,y-1],[x,y+1]. Consistent.

And honey wake in the else: same order. Consistent.

Now potential HIGH issue: **In `update()`, ours reads `myType` AFTER the underworld evaporation and zero-check — fine. But the lava/honey branch: ours checks `myType === 2` (lava) → lavaCheck. Original `tile5.lava()`. Same.

Now let me verify `Tile.lava()`/`honey()` definitions and Main.cs cycles to be thorough. Also check whether `checking` array clear in waterCheck should also reset `skip`. Original WaterCheck sets checkingLiquid(false) but not skipLiquid. Ours: checking.fill(0). Consistent.

Let me also check: `updateLiquid` cleanup loop uses `e.kill >= 8`. Consistent.

One more: `updateLiquid` — original processes buffer entries AFTER the kill cleanup: `num2 = curMaxLiquid - (curMaxLiquid - numLiquid)` = numLiquid; capped by buffer count; then re-AddWater from buffer. Omitted (documented).

Let me now grep Tile.cs for lava()/honey() and Main.cs for cycles.
````

</details>


---

## 🤖 Assistant · 2026-08-09T02:57:37.876Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"public bool lava()\\|public bool honey()\\|public byte liquidType()\\|public void liquidType\" ~/Project/GLM/SandboxWorld/Terarria1405/Tile.cs | head; grep -n \"Liquid.cycles\\|Liquid.curMaxLiquid\" ~/Project/GLM/SandboxWorld/Terarria1405/Main.cs | head",
 "description": "Check Tile liquid type helpers and cycles config"
}
```


---

## 👤 User(sidechain) · 2026-08-09T02:57:37.931Z

**📎 ToolResult**

```
152:    public void liquidType(int liquidType)
168:    public byte liquidType()
255:    public bool lava()
268:    public bool honey()
12240:            Terraria.Liquid.cycles = (int) (17.0 - 10.0 * (double) Main.gfxQuality);
12241:            Terraria.Liquid.curMaxLiquid = (int) ((double) Terraria.Liquid.maxLiquid * 0.25 + (double) Terraria.Liquid.maxLiquid * 0.75 * (double) Main.gfxQuality);
12243:              Terraria.Liquid.curMaxLiquid = (int) (2500.0 + 2500.0 * (double) Main.gfxQuality);
12253:            Terraria.Liquid.curMaxLiquid = Terraria.Liquid.maxLiquid;
12255:              Terraria.Liquid.curMaxLiquid = 5000;
12256:            Terraria.Liquid.cycles = 1;

```


---

## 🤖 Assistant · 2026-08-09T02:57:38.136Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '12230,12260p' ~/Project/GLM/SandboxWorld/Terarria1405/Main.cs; grep -n \"lava()\\|honey()\" ~/Project/GLM/SandboxWorld/Terarria1405/Tile.cs | head",
 "description": "Read Main.cs cycles block and Tile lava/honey"
}
```


---

## 👤 User(sidechain) · 2026-08-09T02:57:38.169Z

**📎 ToolResult**

```
              break;
          }
          Main.maxDustToDraw = (int) (6000.0 * ((double) Main.gfxQuality * 0.699999988079071 + 0.300000011920929));
          if ((double) Main.gfxQuality < 0.9)
            Main.maxDustToDraw = (int) ((double) Main.maxDustToDraw * (double) Main.gfxQuality);
          if (Main.maxDustToDraw < 1000)
            Main.maxDustToDraw = 1000;
          Gore.goreTime = (int) (600.0 * (double) Main.gfxQuality);
          if (!WorldGen.gen)
          {
            Terraria.Liquid.cycles = (int) (17.0 - 10.0 * (double) Main.gfxQuality);
            Terraria.Liquid.curMaxLiquid = (int) ((double) Terraria.Liquid.maxLiquid * 0.25 + (double) Terraria.Liquid.maxLiquid * 0.75 * (double) Main.gfxQuality);
            if (Main.Setting_UseReducedMaxLiquids)
              Terraria.Liquid.curMaxLiquid = (int) (2500.0 + 2500.0 * (double) Main.gfxQuality);
          }
          if (Main.superFast)
          {
            Main.graphics.SynchronizeWithVerticalRetrace = false;
            Main.drawSkip = false;
          }
          LegacyLighting.RenderPhases = (double) Main.gfxQuality >= 0.2 ? ((double) Main.gfxQuality >= 0.4 ? ((double) Main.gfxQuality >= 0.6 ? ((double) Main.gfxQuality >= 0.8 ? 4 : 5) : 6) : 7) : 8;
          if (!WorldGen.gen && Terraria.Liquid.quickSettle)
          {
            Terraria.Liquid.curMaxLiquid = Terraria.Liquid.maxLiquid;
            if (Main.Setting_UseReducedMaxLiquids)
              Terraria.Liquid.curMaxLiquid = 5000;
            Terraria.Liquid.cycles = 1;
          }
          if (WorldGen.drunkWorldGen)
          {
            if (!Main.gameMenu)
255:    public bool lava()
268:    public bool honey()

```


---

## 🤖 Assistant · 2026-08-09T02:57:39.960Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Check Tile.cs lava()/honey() definitions.
```

</details>


---

## 🤖 Assistant · 2026-08-09T02:57:39.964Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '140,285p' ~/Project/GLM/SandboxWorld/Terarria1405/Tile.cs",
 "description": "Read Tile.cs liquid type helpers"
}
```


---

## 👤 User(sidechain) · 2026-08-09T02:57:39.986Z

**📎 ToolResult**

```
    }

    public int blockType()
    {
      if (this.halfBrick())
        return 1;
      int num = (int) this.slope();
      if (num > 0)
        ++num;
      return num;
    }

    public void liquidType(int liquidType)
    {
      switch (liquidType)
      {
        case 0:
          this.bTileHeader &= (byte) 159;
          break;
        case 1:
          this.lava(true);
          break;
        case 2:
          this.honey(true);
          break;
      }
    }

    public byte liquidType()
    {
      return (byte) (((int) this.bTileHeader & 96) >> 5);
    }

    public bool nactive()
    {
      return ((int) this.sTileHeader & 96) == 32;
    }

    public void ResetToType(ushort type)
    {
      this.liquid = (byte) 0;
      this.sTileHeader = (short) 32;
      this.bTileHeader = (byte) 0;
      this.bTileHeader2 = (byte) 0;
      this.bTileHeader3 = (byte) 0;
      this.frameX = (short) 0;
      this.frameY = (short) 0;
      this.type = type;
    }

    internal void ClearMetadata()
    {
      this.liquid = (byte) 0;
      this.sTileHeader = (short) 0;
      this.bTileHeader = (byte) 0;
      this.bTileHeader2 = (byte) 0;
      this.bTileHeader3 = (byte) 0;
      this.frameX = (short) 0;
      this.frameY = (short) 0;
    }

    public Color actColor(Color oldColor)
    {
      if (!this.inActive())
        return oldColor;
      double num = 0.4;
      return new Color((int) (byte) (num * (double) oldColor.R), (int) (byte) (num * (double) oldColor.G), (int) (byte) (num * (double) oldColor.B), (int) oldColor.A);
    }

    public void actColor(ref Vector3 oldColor)
    {
      if (!this.inActive())
        return;
      oldColor *= 0.4f;
    }

    public bool topSlope()
    {
      byte num = this.slope();
      return num == (byte) 1 || num == (byte) 2;
    }

    public bool bottomSlope()
    {
      byte num = this.slope();
      return num == (byte) 3 || num == (byte) 4;
    }

    public bool leftSlope()
    {
      byte num = this.slope();
      return num == (byte) 2 || num == (byte) 4;
    }

    public bool rightSlope()
    {
      byte num = this.slope();
      return num == (byte) 1 || num == (byte) 3;
    }

    public bool HasSameSlope(Tile tile)
    {
      return ((int) this.sTileHeader & 29696) == ((int) tile.sTileHeader & 29696);
    }

    public byte wallColor()
    {
      return (byte) ((uint) this.bTileHeader & 31U);
    }

    public void wallColor(byte wallColor)
    {
      this.bTileHeader = (byte) ((uint) this.bTileHeader & 224U | (uint) wallColor);
    }

    public bool lava()
    {
      return ((int) this.bTileHeader & 32) == 32;
    }

    public void lava(bool lava)
    {
      if (lava)
        this.bTileHeader = (byte) ((int) this.bTileHeader & 159 | 32);
      else
        this.bTileHeader &= (byte) 223;
    }

    public bool honey()
    {
      return ((int) this.bTileHeader & 64) == 64;
    }

    public void honey(bool honey)
    {
      if (honey)
        this.bTileHeader = (byte) ((int) this.bTileHeader & 159 | 64);
      else
        this.bTileHeader &= (byte) 191;
    }

    public bool wire4()
    {
      return ((int) this.bTileHeader & 128) == 128;
    }

```


---

## 🤖 Assistant · 2026-08-09T02:57:52.967Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting: `lava()` and `honey()` are INDEPENDENT bits (bit 5 = 32, bit 6 = 64). liquidType() = (header & 96) >> 5. So liquidType 1 = lava bit set, 2 = honey bit set, 3 = BOTH bits set! And `liquidType(int)` with 1 → lava(true), 2 → honey(true), 0 → clears both. Note: `lava(false)` only clears the lava bit; `honey(false)` only clears honey bit.

So in original, `tile.lava()` and `tile.honey()` can BOTH be true (liquidType 3) — an inconsistent state. More importantly: `tile5.liquidType(0)` in delWater L1152 clears both. But `tile5.lava(false)` in LavaCheck only clears the lava bit — leaving honey bit possibly set! And `liquidType()` returns 3 in that case.

This matters for our translation: we treat liquidType as a single value 1/2/3 with no "both" state. In original, after LavaCheck case A: `tile5.liquid = 0; tile5.lava(false);` → honey bit unchanged (would be 0 normally). Fine.

But consider honeyCheck case A L1058-1059: `tile5.liquid = 0; tile5.liquidType(0);` → clears both. Ours sets 0. Fine.

Critical case: original LavaCheck case B L1002-1004: `tile5.liquid = 0; tile5.lava(false); tile4.liquid = 0;` — the lava cell keeps honey bit if set (unlikely). Ours sets liquidType=0. Negligible.

More important: original L984-985: `tile5.liquid = 0; tile5.liquidType(0);` fine.

Now, the KEY encoding issue with `lava()`/`honey()` being independent bits: `tile.lava()` is true iff lava bit set. Our translation `liquidType === 2` is equivalent for well-formed states (1=water neither bit, 2=lava, 3=honey). Only the inconsistent "both bits" state (original liquidType 3) differs — original treats it as both lava AND honey simultaneously. Ours can't represent it. Extremely rare/degenerate. Could note as 待确认/低.

Now check the honey type detection in lavaCheck case A: `tile1.honey() || tile2.honey() || tile3.honey()` → 230. Ours `lt===3 || rt===3 || ut===3`. Consistent for well-formed.

Now let me double-check one potentially HIGH issue I glossed: in `lavaCheck`, ours checks `if (this.blocksLiquid(x, y)) return;`. Original `WorldGen.SolidTile(x, y, false)`:

WorldGen.SolidTile(int x, int y, bool noFonts) — let me check; it might check the tile at x,y being solid. Probably `Main.tile[x,y].nactive() && tileSolid && !tileSolidTop` plus maybe tree checks. Let me verify quickly.

Also I want to verify cycles=7 claim: gfxQuality high = 1 → cycles = 7, curMaxLiquid = 25000. Ours cycles=7, curMaxLiquid=25000. Consistent.

Now let me also double check `updateLiquid` difference: original, after the per-slice loops, cleanup only runs `if wetCounter >= cycles`. Ours same.

One more potential deviation: in our `updateLiquid`, when `quickSettle` is on, `cycles=1`, so `slice = 25000/1 = 25000`, start = 25000*(wetCounter-1) = 0, end = 25000*1 = 25000; wetCounter===cycles(1) → end = numLiquid. Then clamp. Consistent with original (original also has `if wetCounter == cycles → num5 = numLiquid`, and Main sets cycles=1 for quickSettle). Consistent.

Now let me check WorldGen.SolidTile quickly and also check whether `checking` vs original `checkingLiquid` reset in AddWater when full (buffer). Original when full: buffer, checkingLiquid NOT set. Ours: return without setting. Consistent.

Let me check SolidTile.
```

</details>


---

## 🤖 Assistant · 2026-08-09T02:57:52.972Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"public static bool SolidTile\" ~/Project/GLM/SandboxWorld/Terarria1405/WorldGen.cs | head -3",
 "description": "Locate WorldGen.SolidTile definitions"
}
```


---

## 👤 User(sidechain) · 2026-08-09T02:57:52.999Z

**📎 ToolResult**

```
42315:    public static bool SolidTile(Tile testTile)
42365:    public static bool SolidTile(Point p)
42370:    public static bool SolidTile(int i, int j, bool noDoors = false)

```


---

## 🤖 Assistant · 2026-08-09T02:57:54.389Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '42315,42335p;42370,42400p' ~/Project/GLM/SandboxWorld/Terarria1405/WorldGen.cs",
 "description": "Read SolidTile implementations"
}
```


---

## 👤 User(sidechain) · 2026-08-09T02:57:54.418Z

**📎 ToolResult**

```
    public static bool SolidTile(Tile testTile)
    {
      try
      {
        if (testTile == null)
          return true;
        if (testTile.active())
        {
          if (Main.tileSolid[(int) testTile.type])
          {
            if (!Main.tileSolidTop[(int) testTile.type])
            {
              if (!testTile.halfBrick())
              {
                if (testTile.slope() == (byte) 0)
                {
                  if (!testTile.inActive())
                    return true;
                }
              }
            }
    public static bool SolidTile(int i, int j, bool noDoors = false)
    {
      try
      {
        if (Main.tile[i, j] == null)
          return true;
        if (Main.tile[i, j].active())
        {
          if (Main.tileSolid[(int) Main.tile[i, j].type])
          {
            if (!Main.tileSolidTop[(int) Main.tile[i, j].type])
            {
              if (!Main.tile[i, j].halfBrick())
              {
                if (Main.tile[i, j].slope() == (byte) 0)
                {
                  if (!Main.tile[i, j].inActive())
                    return !noDoors || Main.tile[i, j].type != (ushort) 10;
                }
              }
            }
          }
        }
      }
      catch
      {
      }
      return false;
    }

    public static bool SolidTile2(Tile testTile)

```


---

## 🤖 Assistant · 2026-08-09T02:59:06.755Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Important finding: `WorldGen.SolidTile(x, y, false)` used at the start of LavaCheck/HoneyCheck returns true only if the tile is active, solid, !solidTop, NOT halfBrick, slope==0, !inActive. So half-bricks and slopes are NOT solid for lava check! Our `blocksLiquid` returns true for any solid non-platform, ignoring halfBrick/slope. If our game has half-blocks/slopes, deviation. Does our TILE_DEFS have halfBrick/slope? Probably not (2D block world). 待确认/低.

Also note: original in Update() uses `tile.nactive() && Main.tileSolid[...] && !tileSolidTop` — which DOES treat half-bricks/slopes as solid (no halfBrick check). Our blocksLiquid matches that. But for LavaCheck/HoneyCheck entry it's SolidTile (slope/halfBrick aware). Minor inconsistency between the two in original too. Ours uses blocksLiquid for both. 待确认 低.

Now, let me reconsider the biggest candidates for HIGH severity:

1. Missing wake AddWater calls in 7-cell (L502-513) and 5-cell (L553-560) — this changes propagation. Severity: 中.

Actually wait. Let me reconsider. In the 7-cell branch, those extra AddWater calls: `if (tile1.liquid != num2 || tile5.liquid != num2) AddWater(x-1,y)`. The first pass already added tile1 if tile1.liquid != num2. So the extra call only matters when tile1.liquid == num2 && tile5.liquid != num2. In that case num3 was incremented for tile1... The condition `num3 != 6 || tile3.liquid <= 0` decides center write. If num3==6 (all six equal m) and tile3.liquid>0 → center NOT written → center differs from m → all six extra AddWater calls fire. That's the scenario where the surface has liquid above and neighbors equal. This is actually a common scenario? All six neighbors exactly equal to the rounded mean... requires specific values. Moderately rare. And impact is just extra scheduling (the neighbors would re-run and possibly push liquid back). Without it, the center stays unequal to neighbors and the center itself is in the active list (it was just updated). It would continue. I'd call 低.

Hmm, but also there's the 5-cell equivalent (L553-560). Same 低.

2. AddWater drop-at-cap vs buffer — documented, but it's a real behavioral difference when numLiquid approaches 25000: original queues and later processes; ours silently drops → liquid may freeze permanently (no wake). Severity 中.

3. The `checking` bit on swap-remove: ours `this.checking[i5] = 0`. Original clears checking for the removed tile. Consistent.

4. Another important one: **`addWater` while iterating in updateLiquid loop** — original Main.liquid is a preallocated array of size maxLiquid (actually 25000? no, bigger). AddWater writes at index numLiquid which may be >= end of current slice → appended entries processed later slices. Ours appends to `liquids` array → same. Consistent.

BUT: ours `this.liquids[this.numLiquid] = {...}` and `liquids.length = numLiquid` truncation in delWater. During updateLiquid's per-slice loop, no delWater happens. OK.

However!! In `updateLiquid` cleanup loop (l from numLiquid-1 downto 0, delWater), ours truncates `liquids.length = numLiquid` — fine.

But there's a subtle bug: in the stuck branch, `for (l = numLiquid-1 downto 0) delWater(l)` — consistent.

5. **`waterCheck` doesn't handle `LiquidBuffer` reset** — n/a.

6. Now something I should verify: `st.onTileChanged` triggers `addWater` for 3×3 — but `addWater` requires liquid != 0, fine.

7. **settleWaterAt: `st.liquid[fi] = liquid` may overwrite existing liquid at final position!** Original does exactly the same (`Main.tile[X,Y].liquid = (byte) liquid`) — overwrites. Consistent.

Hmm, wait. Actually is that right? If the final position already has liquid of a different amount... Original L204 overwrites unconditionally. Yes consistent.

8. Another check: `settleWaterAt` — ours doesn't handle the case where the loop `while (Y < st.h - 5 ...)` — original `Y < Main.maxTilesY - 5`. Consistent.

9. `settleWaterAt` ours: `if (st.liquid[oi] === 0) return;` but original returns without writing; ours same. But ours doesn't restore tilesIgnoreWater... n/a.

10. **quickWater y loop**: `for (let y = yMax; y >= minY; y--)` with minY=3. Original `index >= minY`. Consistent. x: `4 .. w-4` exclusive → `originX < maxTilesX - 4`. Ours `x < st.w - 4`. Consistent.

Now, let me re-examine one thing in `update()`: the order of "wake lava neighbors" vs "honeyCheck". Original L340-373:

```
else  // not lava
{
  wake lava neighbors (4)
  if (tile5.honey()) { HoneyCheck; delay 10 gate }
  else { wake honey neighbors (4) }
}
```

Ours:
```
} else {
  wake lava neighbors
  if (myType === 3) { honeyCheck; delay }
  else { wake honey neighbors }
}
```
Consistent.

11. **Deviation candidate**: In `update()`, after lava's delay gate `return`, the original returns from Update — meaning no downward flow that tick. Ours `return` too. Consistent.

12. What about `e.kill` not being maintained when delay gate returns? Original same (returns without touching kill). Consistent.

13. `updateLiquid` non-quickFall loop: `if (!skip[i]) update(e) else skip[i]=0`. Consistent.

Now let me quantify the deviations list. Also double-check `honeyCheck` case B: ours requires `dt !== 1` return — original `tile4.liquidType() != 0` return. Correct.

honeyCheck case B: original `if (tile4.active()) return;` after the tileCut/obsidianKill kills. Ours: `if (belowT !== 0) { decor → clear; else return }`. Consistent-ish.

Also honeyCheck case B threshold check `tile5.liquid < 32` → clear lava? no, clear honey and return. Ours consistent.

Now, one more real deviation: **lavaCheck/honeyCheck case A "sum" uses neighbor amounts read BEFORE clearing, but ours reads lq/rq/uq from cached values at function entry — same.** Consistent.

But here's something: ours in lavaCheck case A does NOT check that tile1/2/3 are passable — original doesn't either. Consistent.

Another: original LavaCheck case A does NOT verify `tile5.liquid > 0` (self amount) — the lava check is called from Update when the tile IS lava, so liquid>0. But ours `lavaCheck` is also called from delWater and attemptToMoveLiquid — same as original. Consistent.

Now the last area: `update()` step 4's guard `y + 1 >= h ? true : this.blocksLiquid(...)`. Original would crash; ours defensive. Fine.

Let me also double check the `sideFlow` f3/f4 gating when `st.liquid[i5] > 250`: sets f3=f4=false. Ours consistent.

Also `sideFlow` reads `st.liquid[i5]` for `> 250` check AFTER downward flow. Consistent.

Another deviation: in `sideFlow` 2-cell branch, ours `if (lq !== m) st.liquid[il] = m;` then type, then conditional addWater, then center = m. Original identical order. Consistent.

Now the `num1` (bias) — ours uses `st.liquid[i5] < 3` — consistent.

OK now the third-party items:

- `TILE_BY_KEY['v_229_honey_block']` and `v_230` — assume correct.

Let me also check `d.platform` vs `Main.tileSolidTop`: tileSolidTop includes platforms AND some other tiles? tileSolidTop is set for platforms (19) and... let me think: TileID.Sets.Platforms? Actually Main.tileSolidTop is true for platforms only, I believe. Ours uses `d.platform`. Reasonable.

- `d.solid` vs `Main.tileSolid`: tileSolid is false for many non-solid like torches, trees, doors(open). Ours TILE_DEFS.solid. Reasonable approximation.

One more possible HIGH: **`blocksLiquid` returns false for type 0 (air)** — fine.

Let me also double check `delWater` branch 2 (water film): original condition uses `||` across three clauses. Ours:
```
if ((lq < amt && !blocks(x-1,y)) || (rq < amt && !blocks(x+1,y)) || (dq < 255 && !blocks(x,y+1)))
```
Consistent.

Now — an important one I should double-check: **`delWater` in ours is called from `updateLiquid` cleanup with entries whose `e.kill >= 8`**. But original also calls DelWater from... only UpdateLiquid. Consistent.

Now think about whether there's a HIGH severity deviation I've missed. Let me re-read our `update()` for the water-wake loops: 

```ts
for (const [nx, ny] of [[x-1,y],[x+1,y],[x,y-1],[x,y+1]] as const) {
  if (nx < 0 || ny < 0 || nx >= w || ny >= h) continue;
  ...
}
```
Original calls AddWater unconditionally which is bounds-guarded inside AddWater. Consistent.

Hmm, one thing: our addWater boundary rejects x<5 etc. Original same.

Now — `st.onLiquidChanged` wakes target + 4 neighbors. That's our own API; original handles liquid placement via WorldGen.PlaceLiquid → which calls... let me check PlaceLiquid to see whether it wakes differently. The user didn't ask about that though. But it could matter... The user asked specific methods. I'll skip, or mention 待确认 briefly? The task says report only deviations in listed methods. I'll skip.

Let me now check one more time the 3-cell branch's random: original `WorldGen.genRand.Next(30) == 0` — probability 1/30. Ours `Math.random() * 30 < 1` — probability 1/30 (with floating point edge cases equal). Consistent.

Now the 4-cell type-write deviation (unconditional liquidType in original). Also check: in the 4-cell branch original writes `tile1.liquidType(...)` BEFORE checking `tile1.liquid != num2 || tile5.liquid != num2`. So type always written. Ours writes type only inside the if. Deviation 低.

Wait, also in the 4-cell branch: original AddWater condition includes `|| tile5.liquid != num2`, ours too. Consistent.

Let me also verify the claim about missing extra AddWater in 7/5-cell more carefully by re-reading our code... Yes, our 7-cell branch ends with the center exception; no extra AddWater block. Confirmed deviation.

Now, one more: in the 7-cell branch, original's first-pass AddWater for each cell happens only when value differs. Our `setCell` helper is defined but UNUSED in sideFlow (we inline everything). Wait — `const setCell = (i, ax, m, centerAmt) => {...}` is declared at L262-265 but never called! Dead code. Not a behavior deviation, but worth mentioning? The user wants algorithm deviations. Dead code isn't a deviation. Maybe skip or one line. I'll skip to save lines... Actually it's worth a 低 note since it indicates the intended translation wasn't applied. Hmm, keep report focused. I'll mention briefly as dead code (低).

Now, another potentially important deviation: `update()` — original reads neighbor tiles ONCE at the top (L301-304) and reuses those references throughout, including in the side flow (tile1, tile2, tile3). Since Tile is a reference type, mutations through tile4 etc. reflect. So caching is not stale. Our array reads are live. Consistent.

BUT there's one subtle thing: original `tile3 = Main.tile[this.x, this.y - 1]` is used in side flow's center-exception check `tile3.liquid <= 0`. Ours `st.liquid[iu]` where iu = i5 - st.w. Consistent.

Now, in our sideFlow, if y == 0, iu = i5 - st.w would be negative index → undefined comparison `st.liquid[iu] <= 0` → undefined <= 0 is false → so center gets written. Original: Main.tile[x, -1] → would throw IndexOutOfRange? Main.tile is TileMap with this.unloaded... Actually Terraria's Main.tile indexer for out-of-range returns TileMap.unloaded (a dummy tile), not throw. So liquid 0 → `tile3.liquid <= 0` → true → center not written. DIFFERENT at y=0! But addWater excludes y<5, so liquid at y<5 can't be scheduled... but sideFlow can reference y-1 for y>=5. iu is only for the center cell's up-neighbor; center y >= 5 always (scheduled entries). So y-1 >= 4. Safe. Not a deviation.

Similarly lavaCheck's iu — called on cells that are scheduled (y>=5) or from attemptToMoveLiquid/waterCheck (y>=1). At y=1, iu = idx(x,0) → valid array index (row 0), just world edge. Fine.

OK. Now, another check: `waterCheck` iterates x from 1, y from h-2 down to 1, and reads `st.liquid[id]` = row y+1 up to h-1. Valid. And `i - 1` for x=1 → x=0. Valid.

Original WaterCheck same bounds.

Now compile the deviation list. Let me prioritize:

HIGH: none? Let me think harder about whether anything is truly high.

Hmm, actually let me reconsider the underworld evaporation: original `if (this.y > Main.UnderworldLayer && ...)`. Main.UnderworldLayer set in WorldGen to `Main.maxTilesY - 200`. For a small world (1200 tall), that's 1000. Ours h-200. Consistent as user stated.

Let me reconsider the `update()` step 4 flag logic once more:
Original:
```
if (!flag) tile5.liquid -= (byte)num;
tile4.liquid += (byte)num;
...
if (quickSettle && tile5.liquid > 250) tile5.liquid = 255;
else if (!flag) { AddWater(x-1,y); AddWater(x+1,y); }
```
Ours:
```
if (!flag) st.liquid[i5] -= t;
st.liquid[bi] += t;
st.liquidType[bi] = myType;
addWater(x, y+1);
skip[bi] = 1; skip[i5] = 1;
if (this.quickSettle && st.liquid[i5] > 250) st.liquid[i5] = 255;
else if (!flag) { addWater(x-1,y); addWater(x+1,y); }
```
Consistent.

Hmm wait — there IS something: original `tile4.skipLiquid(true); tile5.skipLiquid(true);` — both set. Ours: `this.skip[bi] = 1; this.skip[i5] = 1;`. Consistent.

OK now let me look at whether the middle branch ordering differs: ours sets skip AFTER addWater; original AddWater first then skipLiquid. AddWater sets skipLiquid(false) — original order: AddWater(x,y+1) [sets skip false], then tile4.skipLiquid(true) → skip true. Ours: addWater (sets skip[i]=0), then skip[bi]=1 → same. Consistent.

Alright. Let me also double check the `honeyCheck` when called for a WATER cell? No, honeyCheck only called when tile is honey. In delWater: `else if (liquidType === 3) honeyCheck`. Original `else if (tile4.honey())`. Consistent.

One more: `delWater` — ours checks `st.liquidType[i5] === 2` for lava branch. Original `tile4.lava()`. Consistent.

Let me now also consider: our `update()` calls `this.lavaCheck(x, y)` which may call `st.setTile` → `onTileChanged` → `addWater` 3×3 — this can APPEND to `liquids` while we're iterating the slice loop. Original: KillTile/PlaceTile/SquareTileFrame → AddWater too. Consistent.

Final: severity assignments.

Deviations list (each one line):

1. 7 格均分分支缺少 L502-513 的 6 次补偿 AddWater（邻格==均值而中心≠均值时不再唤醒） | LiquidSim.ts:278-287 | Liquid.cs:502-513 | 中
2. 5 格均分分支缺少 L553-560 的 4 次补偿 AddWater | LiquidSim.ts:290-296 | Liquid.cs:553-560 | 中
3. 4 格左延伸分支 liquidType 改为条件写入（原版无条件先写类型） | LiquidSim.ts:301 | Liquid.cs:568 | 低
4. 同上右延伸 | LiquidSim.ts:308 | Liquid.cs:591 | 低
5. AddWater 超限直接丢弃，无 LiquidBuffer 缓冲回灌（L799-807 / L840-843） | LiquidSim.ts:93 | Liquid.cs:840-843,799-807 | 中
6. AddWater 缺少 type 546 豁免 | LiquidSim.ts:89-92 | Liquid.cs:838 | 低（待确认：本仓库是否有 546 等价方块）
7. AddWater 缺 CheckWaterDeath/CheckLavaDeath 摧毁火把等 | (documented) 低
8. LavaCheck/HoneyCheck 入口用 blocksLiquid（实心即挡），原版 SolidTile 额外放行半砖/坡度 | LiquidSim.ts:342,385 | Liquid.cs:898,1020 | 低（待确认：仓库是否模拟半砖/坡度）
9. LavaCheck 情形 B 缺 IsAContainer 容器豁免 | LiquidSim.ts:368-373 | Liquid.cs:965-967,980 | 低
10. LavaCheck/HoneyCheck 缺 getGoodWorldGen（十周年种）转液体分支 | LiquidSim.ts:339-379 | Liquid.cs:934-940,990-996 | 低
11. tileObsidianKill/tileCut 近似为 d.decor：原版可杀火把/植物/容器并掉落 | LiquidSim.ts:357-361,369-373,397-401,408-411 | 低（待确认 decor 覆盖范围）
12. DelWater 岩浆 3×3：缺草块 60/70→泥土 59 转换，仅清 ground decor | LiquidSim.ts:456-464 | Liquid.cs:1163-1186 | 低
13. swap-remove 连同 delay 一起搬运；原版 delay 残留被删槽位旧值 | LiquidSim.ts:472 | Liquid.cs:1195-1197 | 低
14. stuckAmount 初值 -99999 vs 0：开局 numLiquid<50 时卡死计数行为不同 | LiquidSim.ts:39 | Liquid.cs:69 (ReInit 69) | 低
15. liquidType 为独立 lava/honey 位，原版可出现"双位皆置"(liquidType==3 同时 lava()&&honey())，我们单值编码无法表示 | 全文件类型比较 | Tile.cs:255-281 | 低（待确认）
16. QuickWater/Update/WaterCheck 的 tilesIgnoreWater(138 蛛网/484/546) 与 379(气泡) 置实心未实现 | LiquidSim.ts:79,83 | Liquid.cs:87-88,102,300,694 | 低（待确认）
17. sideFlow 中 setCell 辅助函数定义后未使用（死代码，非行为差异）
18. updateLiquid 缺 buffer 回灌 L799-807 (同 5)
19. waterCheck 缺 CheckLavaDeath/CheckWaterDeath KillTile（与 AddWater 同源）| 低

Also: settleWaterAt skips waterLine 岩浆转换 (gen only) — intentional, skip.

Also — honeyCheck case B: ours `st.liquidType[id] = 0` additionally clears below type (original L1102-1103 does clear both for honey; for lava L1004 only liquid). Ours lavaCheck case B also clears liquidType[id] (line 377) whereas original LavaCheck case B does NOT clear tile4 type. Impact: none (liquid==0). I'll skip or mark 低. Probably skip; too minor. Actually since type of empty cells is read in several comparisons guarded by liquid>0, no impact. Skip.

One more check on our lavaCheck case A: `if (sum < 24) return;` — but original computes `Type` before this and sets it 230 if honey neighbor. Also original clears neighbor liquids BEFORE the `< 24` check and returns without restoring — meaning small amounts of water get DELETED when touching lava (evaporate) even below threshold. Ours same (clears then returns). Consistent. Good — this is a notable behavior preserved.

Similarly honeyCheck: `if (num < 32) return;` after clearing water neighbors → water deleted touching honey. Consistent.

Now let me reconsider whether item 1/2 deserve 中. The scenario requires the rounded mean to equal neighbor values. Actually wait — re-examine: the extra AddWater condition is `neighbor.liquid != num2 || tile5.liquid != num2`. First pass added neighbor iff `neighbor != num2` (before write). So extra call is non-redundant exactly when `neighbor == num2 && tile5.liquid != num2` (center differs). Given the first pass already wrote all differing neighbors to num2, after the first pass all six neighbors == num2. tile5.liquid is still original (not yet written; written at L515 conditionally). So extra calls fire for ALL SIX whenever `tile5.liquid != num2`, i.e., whenever the center's value differs from the mean AND num3==6 && tile3.liquid>0 (center not updated). Wait no — the extra AddWater calls happen unconditionally in the code path (they're not gated by num3). They run whenever the branch executes! L502-513 run always in the 7-cell branch.

So: extra AddWater fires for neighbor i iff `neighbor_i != num2 || tile5 != num2`. After first pass, all neighbors == num2. So condition reduces to `tile5.liquid != num2`. Therefore: if the center's current amount differs from the mean, ALL SIX neighbors get AddWater (even those already added in pass 1 — redundant for those, but for... hmm, all six were either already added (if they differed) or not (if equal). The ones that equaled num2 (contributing to num3) were NOT added in pass 1, and now DO get added if center != num2.

So concrete impact: whenever the 7-cell average differs from the center's amount (the common case during spreading!), all 6 neighbors are woken. That's substantial for propagation speed/scheduling. Ours only wakes neighbors whose value actually changed. Hmm, but neighbors whose value changed are already woken by pass 1. The only additionally-woken cells are those that already equaled the mean — cells that need no update. Waking them causes them to run Update, do nothing much, and accumulate kill. So impact is mostly wasted work, not wrong final state. But it does matter for the "center not updated" case (num3==6 && tile3>0): original wakes all 6 so they re-run and can re-average with the odd center; ours leaves them asleep with the center also... wait, is the center woken? The center is currently being processed (it's in the list) and after this Update, its kill increments if liquid unchanged. Hmm, the center's liquid: if num3==6 && tile3.liquid>0, center keeps old value. Its kill increments each pass. After 8 kills it's removed. Neighbors asleep. Potential stall where center ≠ neighbors permanently with nothing awake → liquid stops. In original, neighbors are woken each time the center runs, so it keeps churning until kill removes the center... also stalls eventually but re-triggers.

Honestly: 低-中. I'll rate 中 for the pair since it affects wake propagation in the most common spreading branch.

Hmm, let me reconsider. Actually there's a subtlety: in the 7-cell branch, pass-1 AddWater for neighbor i fires iff `neighbor_i != num2` — but this is checked with the ORIGINAL value. Fine.

I'll present them as one combined line (7格/5格) to save lines, rated 中.

Let me also double check one thing about the 4-cell branch: original writes tile1.liquidType unconditionally — but also note original does NOT have the extra AddWater block in 4-cell/3-cell/2-cell branches. Correct, only 7 and 5 have them.

Now also: is there any issue with our `update()` handling of `e.kill = 999` when solid — the entry stays in list until cleanup (kill>=8). Original same.

One more: our `update()` step 1 `blocksLiquid` includes out-of-bounds=true. Fine.

I think I should also verify `delWater` L1148 condition: ours `st.liquid[i5 - st.w]` — for y=0 could be negative index, but delWater only on scheduled cells y>=5. Fine.

Also `waterCheck`: ours doesn't reset `skip` array — original doesn't either. Consistent.

Let me write the report now, ≤80 lines, format: `偏差 | 我们代码位置 | 原版行号 | 影响程度`.

I'll include ~16 lines plus header. Also mention verified-consistent summary briefly? User said don't list consistent items. Just deviations.

Let me finalize with exact line numbers in our file:
- L262-265 setCell dead code
- L278-287 7格 (extra AddWater missing: original 502-513)
- L290-296 5格 (original 553-560)
- L301 / L308 4格 liquidType conditional (original 568 / 591)
- L93 AddWater cap drop (original 840-843 + 799-807)
- L89-92 type 546 exemption (original 838)
- L85 addWater boundary — consistent
- L342/385 lavaCheck/honeyCheck entry SolidTile (original 898/1020)
- L359,371,399,410 decor approximation (original 928-930, 968-979, 1050-1052, 1074-1085)
- L368-373 IsAContainer (original 965-967, 980-981)
- getGoodWorldGen (original 934-940, 990-996)
- L456-464 grass conversion (original 1163-1186)
- L472 delay swap (original 1195-1197)
- L39 stuckAmount init (original ReInit L69)
- Tile.cs independent bits (255-281)
- tilesIgnoreWater (87-88, 102, 300, 694, 832; WaterCheck tilesIgnoreWater WorldGen.cs:48957)
- waterCheck missing CheckWaterDeath (WorldGen.cs:48975-48984)

Also: cycles config verified consistent (gfxQuality=1 → 7).

One more potential: our `update()` underworld uses `y > h - 200` — user said that's intended. Skip.

Write the report.
````

</details>


---

## 🤖 Assistant · 2026-08-09T02:59:20.230Z · glm-x-preview-260804

````
## 审计结果（仅列偏差）

已完整核对 `LiquidSim.ts` 全部方法与 `Liquid.cs` L85-1213、`WorldGen.cs` WaterCheck（L48955-49009），并验证了 `Tile.cs` L255-281 的 `lava()/honey()` 位定义与 `Main.cs:12240-12243` 的 cycles 配置（gfxQuality=1 → cycles=7，与我们的 `cycles=7` 一致）。类型编码 1/2/3 ↔ 0/1/2 的翻译在各比较点均正确。以下为偏差：

```
偏差 | 我们代码位置 | 原版行号 | 影响程度
7格均分分支缺少 6 次"中心≠均值则唤醒全部邻居"的补偿 AddWater（num3==6 且上方有液、中心保持原值时邻居不再被唤醒） | LiquidSim.ts:278-287 | Liquid.cs:502-513 | 中
5格均分分支同样缺少 4 次补偿 AddWater（同上语义） | LiquidSim.ts:290-296 | Liquid.cs:553-560 | 中
AddWater 达到 curMaxLiquid-1 时直接 return 丢弃，原版入 LiquidBuffer 缓冲、UpdateLiquid 末尾回灌（L799-807），极端规模下液体可能永久冻结 | LiquidSim.ts:93 | Liquid.cs:840-843, 799-807 | 中
AddWater 实心拒绝缺少 type 546 豁免（原版 546 不视为阻挡） | LiquidSim.ts:89-92 | Liquid.cs:838 | 低（待确认：本仓库 tile 集是否有对应方块）
AddWater 缺 CheckWaterDeath/CheckLavaDeath（水流冲毁火把/雕像等并 KillTile） | LiquidSim.ts:94-97 | Liquid.cs:855-867 | 低
4格左延伸分支 liquidType 改为条件写入，原版在 if 之前无条件写入（空格残留旧类型时行为不同） | LiquidSim.ts:301 | Liquid.cs:568 | 低
4格右延伸分支同上 | LiquidSim.ts:308 | Liquid.cs:591 | 低
LavaCheck/HoneyCheck 入口用 blocksLiquid（实心非平台即挡），原版 WorldGen.SolidTile 额外放行半砖(halfBrick)与坡度≠0 的方块 | LiquidSim.ts:342, 385 | Liquid.cs:898, 1020（SolidTile 实现见 WorldGen.cs:42370-42395） | 低（待确认：仓库是否模拟半砖/坡度）
LavaCheck 情形 B 缺少 IsAContainer 容器豁免（岩浆格为容器且下方非容器时，原版在下方有方块时仍继续生成） | LiquidSim.ts:366-373 | Liquid.cs:965-967, 980-981 | 低
LavaCheck/HoneyCheck 缺 getGoodWorldGen（十周年种）"互相转液体而非生成块"分支 | LiquidSim.ts:339-379, 383-417 | Liquid.cs:934-940, 990-996 | 低
tileObsidianKill/tileCut 近似为 d.decor 清除：原版按类型表杀火把/植物/容器并触发掉落与 SquareTileFrame，覆盖面与掉落行为不同 | LiquidSim.ts:357-361, 369-373, 397-401, 408-411 | Liquid.cs:928-933, 968-979, 1050-1055, 1074-1085 | 低（待确认：decor 标志是否覆盖火把等）
DelWater 岩浆 3×3：缺草块 60/70→泥土 59 的转换，仅清除 attach==='ground' 的 decor；蘑菇/花(2,23,109,199,477,492)清除范围也可能不一致 | LiquidSim.ts:456-464 | Liquid.cs:1163-1186 | 低
swap-remove 整对象搬运（含 delay），原版只复制 x/y/kill，delay 残留被删槽位的旧值 → 岩浆/蜂蜜降速计数语义不同 | LiquidSim.ts:472 | Liquid.cs:1195-1197 | 低
stuckAmount 初值 -99999（原版 ReInit 为 0）：开局 numLiquid∈(0,50) 时我们走 stuckCount=0 分支、原版走 stuckCount++ 分支 | LiquidSim.ts:39 | Liquid.cs:69（ReInit） | 低
原版 lava()/honey() 是 bTileHeader 两个独立位，可同时置位（liquidType()==3 时 lava()&&honey() 同真）；我们单值编码无法表示该退化态 | 全部 liquidType 比较 | Tile.cs:255-281 | 低（待确认：该态在正常游玩中是否可达）
QuickWater/Update/UpdateLiquid/WaterCheck 的 tilesIgnoreWater（138 蛛网、484、546 置为可穿过）与 Update 入口 tileSolid[379]=true（气泡实心）未实现 | LiquidSim.ts:79, 105 | Liquid.cs:87-88, 102, 300, 694, 832（WorldGen.cs:48957） | 低（待确认：仓库是否建模这些方块）
waterCheck 缺实心格内液体的 CheckLavaDeath/CheckWaterDeath KillTile（与 AddWater 同源省略） | LiquidSim.ts:592-596 | WorldGen.cs:48975-48984 | 低
sideFlow 中 setCell 闭包（L262-265）定义后从未调用，属死代码（非行为差异，但提示部分翻译意图未落地） | LiquidSim.ts:262-265 | — | 低
```

## 逐项确认一致的关键点（不展开）

update() 的实心检查、地狱蒸发（-2 下限截断）、岩浆 delay5/蜂蜜 delay10 门、水唤醒岩浆/蜂蜜邻居的四邻顺序（左/右/上/下）、向下搬运公式与 flag 边界、skipLiquid 双置位、quickSettle 补满与 `!flag` 侧唤醒、kill 维护三分支；sideFlow 的 flag1-6 else-if 求值序、num1=-1 偏置、>250 禁延伸、7/5/4/3/2 格公式、中心格例外条件、3格 254→255 的 1/30 概率、类型写入时机与 AddWater 条件（4/3/2 格分支逐条一致）；lavaCheck/honeyCheck 的情形 A/B 条件、阈值 24/32、块型 56/230/229、生成位置（A 在岩浆格、B 在下方格）、sum 累加与"先清液再判阈值"顺序；delWater 三分支、再唤醒条件与顺序（先右后左）；updateLiquid 的分片 start/end 与钳制、quickFall 的 delay=10、kill>=8 清扫、254→255、stuck 检测阈值（±50/10000）；settleWaterAt 的垂直下落、蛇形 num2-num5/flag3-flag5 与 goto label_34 的 break 等价翻译、侧下方灌入；attemptToMoveLiquid 与 AttemptToMoveLava/Honey 的异或语义逐分支等价；waterCheck 扫描序与 AddWater 条件。
````
