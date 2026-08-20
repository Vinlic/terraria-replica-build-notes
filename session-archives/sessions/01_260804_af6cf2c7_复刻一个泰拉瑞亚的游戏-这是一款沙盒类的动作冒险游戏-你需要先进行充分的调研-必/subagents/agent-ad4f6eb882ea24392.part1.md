# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-08T15:16:27.586Z

```
阅读 ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/ 目录下的反编译源码(DesertBiome.cs 已在 ../DesertBiome.cs,重点是 Desert/ 子目录:SandMound.cs、DesertHive.cs、DesertDescription.cs,以及四个人口 ChambersEntrance/AnthillEntrance/LarvaHoleEntrance/PitEntrance 如果存在)。

用中文输出:
1. SandMound.Place 的精确算法:沙丘表面形状函数(如何从 SurfaceMap 计算沙丘高度)、沙/硬化沙/沙岩的分层规则、每个 tile 的判定条件
2. DesertHive.Place 的精确算法:蜂巢腔室的格阵结构(格子尺寸、腔室/墙判定)、用什么 tile 和 wall id、隧道的生成方式、最大深度限制(hive 是否限制不到地狱)
3. 四种入口的简要结构(每种几行描述即可)
4. 明确列出所有硬编码常量(格子大小、材料 id、深度限制)

只要算法事实,不要建议。
```

---

## 📎 Attachment · skill_listing · 2026-08-08T15:16:27.592Z

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

## 🤖 Assistant · 2026-08-08T15:16:30.397Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me explore the decompiled source files in the Desert directory.
```

</details>


---

## 🤖 Assistant · 2026-08-08T15:16:30.403Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert -type f | sort; ls -la ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/",
 "description": "List files in Desert biome directory"
}
```


---

## 👤 User(sidechain) · 2026-08-08T15:16:30.459Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/AnthillEntrance.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/ChambersEntrance.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/DesertDescription.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/DesertHive.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/LarvaHoleEntrance.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/PitEntrance.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/SandMound.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/SurfaceMap.cs
total 96
drwxr-xr-x@ 10 user  staff    320  8月  7 14:45 .
drwxr-xr-x@ 20 user  staff    640  8月  7 14:45 ..
-rw-r--r--@  1 user  staff   4070  8月  7 14:45 AnthillEntrance.cs
-rw-r--r--@  1 user  staff   4901  8月  7 14:45 ChambersEntrance.cs
-rw-r--r--@  1 user  staff   3067  8月  7 14:45 DesertDescription.cs
-rw-r--r--@  1 user  staff  14120  8月  7 14:45 DesertHive.cs
-rw-r--r--@  1 user  staff   3248  8月  7 14:45 LarvaHoleEntrance.cs
-rw-r--r--@  1 user  staff   3314  8月  7 14:45 PitEntrance.cs
-rw-r--r--@  1 user  staff   2796  8月  7 14:45 SandMound.cs
-rw-r--r--@  1 user  staff   2312  8月  7 14:45 SurfaceMap.cs

```


---

## 🤖 Assistant · 2026-08-08T15:16:33.033Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/SandMound.cs"
}
```


---

## 🤖 Assistant · 2026-08-08T15:16:33.041Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/DesertHive.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-08T15:16:33.065Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.GameContent.Biomes.Desert.DesertHive
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using Microsoft.Xna.Framework;
8	using System;
9	using System.Collections.Generic;
10	using Terraria.Utilities;
11	
12	namespace Terraria.GameContent.Biomes.Desert
13	{
14	  public static class DesertHive
15	  {
16	    public static void Place(DesertDescription description)
17	    {
18	      DesertHive.ClusterGroup clusters = DesertHive.ClusterGroup.FromDescription(description);
19	      DesertHive.PlaceClusters(description, clusters);
20	      DesertHive.AddTileVariance(description);
21	    }
22	
23	    private static void PlaceClusters(
24	      DesertDescription description,
25	      DesertHive.ClusterGroup clusters)
26	    {
27	      Rectangle hive = description.Hive;
28	      hive.Inflate(20, 20);
29	      DesertHive.PostPlacementEffect[,] postEffectMap = new DesertHive.PostPlacementEffect[hive.Width, hive.Height];
30	      DesertHive.PlaceClustersArea(description, clusters, hive, postEffectMap, Point.Zero);
31	      for (int left = hive.Left; left < hive.Right; ++left)
32	      {
33	        for (int top = hive.Top; top < hive.Bottom; ++top)
34	        {
35	          if (postEffectMap[left - hive.Left, top - hive.Top].HasFlag((Enum) DesertHive.PostPlacementEffect.Smooth))
36	            Tile.SmoothSlope(left, top, false, false);
37	        }
38	      }
39	    }
40	
41	    private static void PlaceClustersArea(
42	      DesertDescription description,
43	      DesertHive.ClusterGroup clusters,
44	      Rectangle area,
45	      DesertHive.PostPlacementEffect[,] postEffectMap,
46	      Point postEffectMapOffset)
47	    {
48	      FastRandom fastRandom = new FastRandom(Main.ActiveWorldFileData.Seed).WithModifier(57005UL);
49	      Vector2 vector2_1 = new Vector2((float) description.Hive.Width, (float) description.Hive.Height);
50	      Vector2 vector2_2 = new Vector2((float) clusters.Width, (float) clusters.Height);
51	      Vector2 vector2_3 = description.BlockScale / 2f;
52	      for (int left = area.Left; left < area.Right; ++left)
53	      {
54	        for (int top = area.Top; top < area.Bottom; ++top)
55	        {
56	          if (WorldGen.InWorld(left, top, 1))
57	          {
58	            float num1 = 0.0f;
59	            int num2 = -1;
60	            float num3 = 0.0f;
61	            ushort type = 53;
62	            if (fastRandom.Next(3) == 0)
63	              type = (ushort) 397;
64	            int x = left - description.Hive.X;
65	            int y = top - description.Hive.Y;
66	            Vector2 vector2_4 = (new Vector2((float) x, (float) y) - vector2_3) / vector2_1 * vector2_2;
67	            for (int index = 0; index < clusters.Count; ++index)
68	            {
69	              DesertHive.Cluster cluster = clusters[index];
70	              if ((double) Math.Abs(cluster[0].Position.X - vector2_4.X) <= 10.0 && (double) Math.Abs(cluster[0].Position.Y - vector2_4.Y) <= 10.0)
71	              {
72	                float num4 = 0.0f;
73	                foreach (DesertHive.Block block in (List<DesertHive.Block>) cluster)
74	                  num4 += 1f / Vector2.DistanceSquared(block.Position, vector2_4);
75	                if ((double) num4 > (double) num1)
76	                {
77	                  if ((double) num1 > (double) num3)
78	                    num3 = num1;
79	                  num1 = num4;
80	                  num2 = index;
81	                }
82	                else if ((double) num4 > (double) num3)
83	                  num3 = num4;
84	              }
85	            }
86	            float num5 = num1 + num3;
87	            Tile tile = Main.tile[left, top];
88	            bool flag = (double) ((new Vector2((float) x, (float) y) - vector2_3) / vector2_1 * 2f - Vector2.One).Length() >= 0.800000011920929;
89	            DesertHive.PostPlacementEffect postPlacementEffect = DesertHive.PostPlacementEffect.None;
90	            if ((double) num5 > 3.5)
91	            {
92	              postPlacementEffect = DesertHive.PostPlacementEffect.Smooth;
93	              tile.ClearEverything();
94	              tile.wall = (ushort) 187;
95	              if (num2 % 15 == 2)
96	                tile.ResetToType((ushort) 404);
97	            }
98	            else if ((double) num5 > 1.79999995231628)
99	            {
100	              tile.wall = (ushort) 187;
101	              if ((double) top < Main.worldSurface)
102	                tile.liquid = (byte) 0;
103	              else
104	                tile.lava(true);
105	              if (!flag || tile.active())
106	              {
107	                tile.ResetToType((ushort) 396);
108	                postPlacementEffect = DesertHive.PostPlacementEffect.Smooth;
109	              }
110	            }
111	            else if ((double) num5 > 0.699999988079071 || !flag)
112	            {
113	              tile.wall = (ushort) 216;
114	              tile.liquid = (byte) 0;
115	              if (!flag || tile.active())
116	              {
117	                tile.ResetToType(type);
118	                postPlacementEffect = DesertHive.PostPlacementEffect.Smooth;
119	              }
120	            }
121	            else if ((double) num5 > 0.25 && (double) fastRandom.WithModifier(x, y).NextFloat() < ((double) num5 - 0.25) / 0.449999988079071)
122	            {
123	              tile.wall = (ushort) 187;
124	              if ((double) top < Main.worldSurface)
125	                tile.liquid = (byte) 0;
126	              else
127	                tile.lava(true);
128	              if (tile.active())
129	              {
130	                tile.ResetToType(type);
131	                postPlacementEffect = DesertHive.PostPlacementEffect.Smooth;
132	              }
133	            }
134	            postEffectMap[left - area.X + postEffectMapOffset.X, top - area.Y + postEffectMapOffset.Y] = postPlacementEffect;
135	          }
136	        }
137	      }
138	    }
139	
140	    private static void AddTileVariance(DesertDescription description)
141	    {
142	      for (int index1 = -20; index1 < description.Hive.Width + 20; ++index1)
143	      {
144	        for (int index2 = -20; index2 < description.Hive.Height + 20; ++index2)
145	        {
146	          int x = index1 + description.Hive.X;
147	          int y = index2 + description.Hive.Y;
148	          if (WorldGen.InWorld(x, y, 1))
149	          {
150	            Tile tile = Main.tile[x, y];
151	            Tile testTile1 = Main.tile[x, y + 1];
152	            Tile testTile2 = Main.tile[x, y + 2];
153	            if (tile.type == (ushort) 53 && (!WorldGen.SolidTile(testTile1) || !WorldGen.SolidTile(testTile2)))
154	              tile.type = (ushort) 397;
155	          }
156	        }
157	      }
158	      for (int index1 = -20; index1 < description.Hive.Width + 20; ++index1)
159	      {
160	        for (int index2 = -20; index2 < description.Hive.Height + 20; ++index2)
161	        {
162	          int index3 = index1 + description.Hive.X;
163	          int y = index2 + description.Hive.Y;
164	          if (WorldGen.InWorld(index3, y, 1))
165	          {
166	            Tile tile = Main.tile[index3, y];
167	            if (tile.active() && tile.type == (ushort) 396)
168	            {
169	              bool flag1 = true;
170	              for (int index4 = -1; index4 >= -3; --index4)
171	              {
172	                if (Main.tile[index3, y + index4].active())
173	                {
174	                  flag1 = false;
175	                  break;
176	                }
177	              }
178	              bool flag2 = true;
179	              for (int index4 = 1; index4 <= 3; ++index4)
180	              {
181	                if (Main.tile[index3, y + index4].active())
182	                {
183	                  flag2 = false;
184	                  break;
185	                }
186	              }
187	              if (flag1 && WorldGen.genRand.Next(5) == 0)
188	                WorldGen.PlaceTile(index3, y - 1, 485, true, true, -1, WorldGen.genRand.Next(4));
189	              else if (flag1 && WorldGen.genRand.Next(5) == 0)
190	                WorldGen.PlaceTile(index3, y - 1, 484, true, true, -1, 0);
191	              else if (flag1 ^ flag2 && WorldGen.genRand.Next(5) == 0)
192	                WorldGen.PlaceTile(index3, y + (flag1 ? -1 : 1), 165, true, true, -1, 0);
193	              else if (flag1 && WorldGen.genRand.Next(5) == 0)
194	                WorldGen.PlaceTile(index3, y - 1, 187, true, true, -1, 29 + WorldGen.genRand.Next(6));
195	            }
196	          }
197	        }
198	      }
199	    }
200	
201	    private struct Block
202	    {
203	      public Vector2 Position;
204	
205	      public Block(float x, float y)
206	      {
207	        this.Position = new Vector2(x, y);
208	      }
209	    }
210	
211	    private class Cluster : List<DesertHive.Block>
212	    {
213	    }
214	
215	    private class ClusterGroup : List<DesertHive.Cluster>
216	    {
217	      public readonly int Width;
218	      public readonly int Height;
219	
220	      private ClusterGroup(int width, int height)
221	      {
222	        this.Width = width;
223	        this.Height = height;
224	        this.Generate();
225	      }
226	
227	      public static DesertHive.ClusterGroup FromDescription(DesertDescription description)
228	      {
229	        return new DesertHive.ClusterGroup(description.BlockColumnCount, description.BlockRowCount);
230	      }
231	
232	      private static void SearchForCluster(
233	        bool[,] blockMap,
234	        List<Point> pointCluster,
235	        int x,
236	        int y,
237	        int level = 2)
238	      {
239	        pointCluster.Add(new Point(x, y));
240	        blockMap[x, y] = false;
241	        --level;
242	        if (level == -1)
243	          return;
244	        if (x > 0 && blockMap[x - 1, y])
245	          DesertHive.ClusterGroup.SearchForCluster(blockMap, pointCluster, x - 1, y, level);
246	        if (x < blockMap.GetLength(0) - 1 && blockMap[x + 1, y])
247	          DesertHive.ClusterGroup.SearchForCluster(blockMap, pointCluster, x + 1, y, level);
248	        if (y > 0 && blockMap[x, y - 1])
249	          DesertHive.ClusterGroup.SearchForCluster(blockMap, pointCluster, x, y - 1, level);
250	        if (y >= blockMap.GetLength(1) - 1 || !blockMap[x, y + 1])
251	          return;
252	        DesertHive.ClusterGroup.SearchForCluster(blockMap, pointCluster, x, y + 1, level);
253	      }
254	
255	      private static void AttemptClaim(
256	        int x,
257	        int y,
258	        int[,] clusterIndexMap,
259	        List<List<Point>> pointClusters,
260	        int index)
261	      {
262	        int clusterIndex = clusterIndexMap[x, y];
263	        if (clusterIndex == -1 || clusterIndex == index)
264	          return;
265	        int num = WorldGen.genRand.Next(2) == 0 ? -1 : index;
266	        foreach (Point point in pointClusters[clusterIndex])
267	          clusterIndexMap[point.X, point.Y] = num;
268	      }
269	
270	      private void Generate()
271	      {
272	        this.Clear();
273	        bool[,] blockMap = new bool[this.Width, this.Height];
274	        int num1 = this.Width / 2 - 1;
275	        int y1 = this.Height / 2 - 1;
276	        int num2 = (num1 + 1) * (num1 + 1);
277	        Point point1 = new Point(num1, y1);
278	        for (int index1 = point1.Y - y1; index1 <= point1.Y + y1; ++index1)
279	        {
280	          float num3 = (float) num1 / (float) y1 * (float) (index1 - point1.Y);
281	          int num4 = Math.Min(num1, (int) Math.Sqrt((double) num2 - (double) num3 * (double) num3));
282	          for (int index2 = point1.X - num4; index2 <= point1.X + num4; ++index2)
283	            blockMap[index2, index1] = WorldGen.genRand.Next(2) == 0;
284	        }
285	        List<List<Point>> pointClusters = new List<List<Point>>();
286	        for (int x = 0; x < blockMap.GetLength(0); ++x)
287	        {
288	          for (int y2 = 0; y2 < blockMap.GetLength(1); ++y2)
289	          {
290	            if (blockMap[x, y2] && WorldGen.genRand.Next(2) == 0)
291	            {
292	              List<Point> pointCluster = new List<Point>();
293	              DesertHive.ClusterGroup.SearchForCluster(blockMap, pointCluster, x, y2, 2);
294	              if (pointCluster.Count > 2)
295	                pointClusters.Add(pointCluster);
296	            }
297	          }
298	        }
299	        int[,] clusterIndexMap = new int[blockMap.GetLength(0), blockMap.GetLength(1)];
300	        for (int index1 = 0; index1 < clusterIndexMap.GetLength(0); ++index1)
301	        {
302	          for (int index2 = 0; index2 < clusterIndexMap.GetLength(1); ++index2)
303	            clusterIndexMap[index1, index2] = -1;
304	        }
305	        for (int index = 0; index < pointClusters.Count; ++index)
306	        {
307	          foreach (Point point2 in pointClusters[index])
308	            clusterIndexMap[point2.X, point2.Y] = index;
309	        }
310	        for (int index1 = 0; index1 < pointClusters.Count; ++index1)
311	        {
312	          foreach (Point point2 in pointClusters[index1])
313	          {
314	            int x = point2.X;
315	            int y2 = point2.Y;
316	            if (clusterIndexMap[x, y2] != -1)
317	            {
318	              int index2 = clusterIndexMap[x, y2];
319	              if (x > 0)
320	                DesertHive.ClusterGroup.AttemptClaim(x - 1, y2, clusterIndexMap, pointClusters, index2);
321	              if (x < clusterIndexMap.GetLength(0) - 1)
322	                DesertHive.ClusterGroup.AttemptClaim(x + 1, y2, clusterIndexMap, pointClusters, index2);
323	              if (y2 > 0)
324	                DesertHive.ClusterGroup.AttemptClaim(x, y2 - 1, clusterIndexMap, pointClusters, index2);
325	              if (y2 < clusterIndexMap.GetLength(1) - 1)
326	                DesertHive.ClusterGroup.AttemptClaim(x, y2 + 1, clusterIndexMap, pointClusters, index2);
327	            }
328	            else
329	              break;
330	          }
331	        }
332	        foreach (List<Point> pointList in pointClusters)
333	          pointList.Clear();
334	        for (int x = 0; x < clusterIndexMap.GetLength(0); ++x)
335	        {
336	          for (int y2 = 0; y2 < clusterIndexMap.GetLength(1); ++y2)
337	          {
338	            if (clusterIndexMap[x, y2] != -1)
339	              pointClusters[clusterIndexMap[x, y2]].Add(new Point(x, y2));
340	          }
341	        }
342	        foreach (List<Point> pointList in pointClusters)
343	        {
344	          if (pointList.Count < 4)
345	            pointList.Clear();
346	        }
347	        foreach (List<Point> pointList in pointClusters)
348	        {
349	          DesertHive.Cluster cluster = new DesertHive.Cluster();
350	          if (pointList.Count > 0)
351	          {
352	            foreach (Point point2 in pointList)
353	              cluster.Add(new DesertHive.Block((float) point2.X + (float) (((double) WorldGen.genRand.NextFloat() - 0.5) * 0.5), (float) point2.Y + (float) (((double) WorldGen.genRand.NextFloat() - 0.5) * 0.5)));
354	            this.Add(cluster);
355	          }
356	        }
357	      }
358	    }
359	
360	    [Flags]
361	    private enum PostPlacementEffect : byte
362	    {
363	      None = 0,
364	      Smooth = 1,
365	    }
366	  }
367	}
368	

```


---

## 👤 User(sidechain) · 2026-08-08T15:16:33.066Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.GameContent.Biomes.Desert.SandMound
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using Microsoft.Xna.Framework;
8	using System;
9	
10	namespace Terraria.GameContent.Biomes.Desert
11	{
12	  public static class SandMound
13	  {
14	    public static void Place(DesertDescription description)
15	    {
16	      Rectangle desert1 = description.Desert;
17	      desert1.Height = Math.Min(description.Desert.Height, description.Hive.Height / 2);
18	      Rectangle desert2 = description.Desert;
19	      desert2.Y = desert1.Bottom;
20	      desert2.Height = Math.Max(0, description.Desert.Bottom - desert1.Bottom);
21	      SurfaceMap surface = description.Surface;
22	      int num1 = 0;
23	      int num2 = 0;
24	      for (int index1 = -5; index1 < desert1.Width + 5; ++index1)
25	      {
26	        float num3 = MathHelper.Clamp((float) ((double) Math.Abs((float) (index1 + 5) / (float) (desert1.Width + 10)) * 2.0 - 1.0), -1f, 1f);
27	        if (index1 % 3 == 0)
28	          num1 = Utils.Clamp<int>(num1 + WorldGen.genRand.Next(-1, 2), -10, 10);
29	        num2 = Utils.Clamp<int>(num2 + WorldGen.genRand.Next(-1, 2), -10, 10);
30	        float num4 = (float) Math.Sqrt(1.0 - (double) num3 * (double) num3 * (double) num3 * (double) num3);
31	        int num5 = desert1.Bottom - (int) ((double) num4 * (double) desert1.Height) + num1;
32	        if ((double) Math.Abs(num3) < 1.0)
33	        {
34	          float num6 = Utils.UnclampedSmoothStep(0.5f, 0.8f, Math.Abs(num3));
35	          float num7 = num6 * num6 * num6;
36	          int num8 = Math.Min(10 + (int) ((double) desert1.Top - (double) num7 * 20.0) + num2, num5);
37	          for (int index2 = (int) surface[index1 + desert1.X] - 1; index2 < num8; ++index2)
38	          {
39	            int index3 = index1 + desert1.X;
40	            int index4 = index2;
41	            Main.tile[index3, index4].active(false);
42	            Main.tile[index3, index4].wall = (ushort) 0;
43	          }
44	        }
45	        SandMound.PlaceSandColumn(index1 + desert1.X, num5, desert2.Bottom - num5);
46	      }
47	    }
48	
49	    private static void PlaceSandColumn(int startX, int startY, int height)
50	    {
51	      for (int index = startY + height - 1; index >= startY; --index)
52	      {
53	        int i = startX;
54	        int j = index;
55	        Tile tile1 = Main.tile[i, j];
56	        tile1.liquid = (byte) 0;
57	        Tile tile2 = Main.tile[i, j + 1];
58	        Tile tile3 = Main.tile[i, j + 2];
59	        tile1.type = (ushort) 53;
60	        tile1.slope((byte) 0);
61	        tile1.halfBrick(false);
62	        tile1.active(true);
63	        if (index < startY)
64	          tile1.active(false);
65	        WorldGen.SquareWallFrame(i, j, true);
66	      }
67	    }
68	  }
69	}
70	

```


---

## 🤖 Assistant · 2026-08-08T15:16:33.067Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/DesertDescription.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-08T15:16:33.083Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.GameContent.Biomes.Desert.DesertDescription
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using Microsoft.Xna.Framework;
8	
9	namespace Terraria.GameContent.Biomes.Desert
10	{
11	  public class DesertDescription
12	  {
13	    public static readonly DesertDescription Invalid = new DesertDescription()
14	    {
15	      IsValid = false
16	    };
17	    private static readonly Vector2 DefaultBlockScale = new Vector2(4f, 2f);
18	    private const int SCAN_PADDING = 5;
19	
20	    public Rectangle CombinedArea { get; private set; }
21	
22	    public Rectangle Desert { get; private set; }
23	
24	    public Rectangle Hive { get; private set; }
25	
26	    public Vector2 BlockScale { get; private set; }
27	
28	    public int BlockColumnCount { get; private set; }
29	
30	    public int BlockRowCount { get; private set; }
31	
32	    public bool IsValid { get; private set; }
33	
34	    public SurfaceMap Surface { get; private set; }
35	
36	    private DesertDescription()
37	    {
38	    }
39	
40	    public void UpdateSurfaceMap()
41	    {
42	      this.Surface = SurfaceMap.FromArea(this.CombinedArea.Left - 5, this.CombinedArea.Width + 10);
43	    }
44	
45	    public static DesertDescription CreateFromPlacement(Point origin)
46	    {
47	      Vector2 defaultBlockScale = DesertDescription.DefaultBlockScale;
48	      float num1 = (float) Main.maxTilesX / 4200f;
49	      int num2 = (int) (80.0 * (double) num1);
50	      int num3 = (int) (((double) WorldGen.genRand.NextFloat() + 1.0) * 170.0 * (double) num1);
51	      int width = (int) ((double) defaultBlockScale.X * (double) num2);
52	      int height = (int) ((double) defaultBlockScale.Y * (double) num3);
53	      origin.X -= width / 2;
54	      SurfaceMap surfaceMap = SurfaceMap.FromArea(origin.X - 5, width + 10);
55	      if (DesertDescription.RowHasInvalidTiles(origin.X, surfaceMap.Bottom, width))
56	        return DesertDescription.Invalid;
57	      int y = (int) ((double) surfaceMap.Average + (double) surfaceMap.Bottom) / 2;
58	      origin.Y = y + WorldGen.genRand.Next(40, 60);
59	      return new DesertDescription()
60	      {
61	        CombinedArea = new Rectangle(origin.X, y, width, origin.Y + height - y),
62	        Hive = new Rectangle(origin.X, origin.Y, width, height),
63	        Desert = new Rectangle(origin.X, y, width, origin.Y + height / 2 - y),
64	        BlockScale = defaultBlockScale,
65	        BlockColumnCount = num2,
66	        BlockRowCount = num3,
67	        Surface = surfaceMap,
68	        IsValid = true
69	      };
70	    }
71	
72	    private static bool RowHasInvalidTiles(int startX, int startY, int width)
73	    {
74	      if (WorldGen.skipDesertTileCheck)
75	        return false;
76	      for (int index = startX; index < startX + width; ++index)
77	      {
78	        switch (Main.tile[index, startY].type)
79	        {
80	          case 59:
81	          case 60:
82	            return true;
83	          case 147:
84	          case 161:
85	            return true;
86	          default:
87	            continue;
88	        }
89	      }
90	      return false;
91	    }
92	  }
93	}
94	

```


---

## 🤖 Assistant · 2026-08-08T15:16:35.461Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now read the four entrances and SurfaceMap, and the DesertBiome.cs in ../
```

</details>


---

## 🤖 Assistant · 2026-08-08T15:16:35.465Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/ChambersEntrance.cs"
}
```


---

## 🤖 Assistant · 2026-08-08T15:16:35.470Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/AnthillEntrance.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-08T15:16:35.483Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.GameContent.Biomes.Desert.AnthillEntrance
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using Microsoft.Xna.Framework;
8	using Terraria.WorldBuilding;
9	
10	namespace Terraria.GameContent.Biomes.Desert
11	{
12	  public static class AnthillEntrance
13	  {
14	    public static void Place(DesertDescription description)
15	    {
16	      int num = WorldGen.genRand.Next(2, 4);
17	      for (int index = 0; index < num; ++index)
18	      {
19	        int holeRadius = WorldGen.genRand.Next(15, 18);
20	        int x = (int) ((double) (index + 1) / (double) (num + 1) * (double) description.Surface.Width) + description.Desert.Left;
21	        int y = (int) description.Surface[x];
22	        AnthillEntrance.PlaceAt(description, new Point(x, y), holeRadius);
23	      }
24	    }
25	
26	    private static void PlaceAt(DesertDescription description, Point position, int holeRadius)
27	    {
28	      ShapeData data = new ShapeData();
29	      Point origin = new Point(position.X, position.Y + 6);
30	      WorldUtils.Gen(origin, (GenShape) new Shapes.Tail((float) (holeRadius * 2), new Vector2(0.0f, (float) -holeRadius * 1.5f)), Actions.Chain(new Actions.SetTile((ushort) 53, false, true).Output(data)));
31	      GenShapeActionPair pair1 = new GenShapeActionPair((GenShape) new Shapes.Rectangle(1, 1), Actions.Chain((GenAction) new Modifiers.Blotches(2, 0.3), (GenAction) new Modifiers.IsSolid(), (GenAction) new Actions.Clear(), (GenAction) new Actions.PlaceWall((ushort) 187, true)));
32	      GenShapeActionPair genShapeActionPair = new GenShapeActionPair((GenShape) new Shapes.Rectangle(1, 1), Actions.Chain((GenAction) new Modifiers.IsSolid(), (GenAction) new Actions.Clear(), (GenAction) new Actions.PlaceWall((ushort) 187, true)));
33	      GenShapeActionPair pair2 = new GenShapeActionPair((GenShape) new Shapes.Circle(2, 3), Actions.Chain((GenAction) new Modifiers.IsSolid(), (GenAction) new Actions.SetTile((ushort) 397, false, true), (GenAction) new Actions.PlaceWall((ushort) 187, true)));
34	      GenShapeActionPair pair3 = new GenShapeActionPair((GenShape) new Shapes.Circle(holeRadius, 3), Actions.Chain((GenAction) new Modifiers.SkipWalls(new ushort[1]
35	      {
36	        (ushort) 187
37	      }), (GenAction) new Actions.SetTile((ushort) 53, false, true)));
38	      GenShapeActionPair pair4 = new GenShapeActionPair((GenShape) new Shapes.Circle(holeRadius - 2, 3), Actions.Chain((GenAction) new Actions.PlaceWall((ushort) 187, true)));
39	      int x = position.X;
40	      int y1 = position.Y - holeRadius - 3;
41	      while (true)
42	      {
43	        int num1 = y1;
44	        Microsoft.Xna.Framework.Rectangle rectangle = description.Hive;
45	        int top1 = rectangle.Top;
46	        int y2 = position.Y;
47	        rectangle = description.Desert;
48	        int top2 = rectangle.Top;
49	        int num2 = (y2 - top2) * 2;
50	        int num3 = top1 + num2 + 12;
51	        if (num1 < num3)
52	        {
53	          WorldUtils.Gen(new Point(x, y1), y1 < position.Y ? genShapeActionPair : pair1);
54	          WorldUtils.Gen(new Point(x, y1), pair2);
55	          if (y1 % 3 == 0 && y1 >= position.Y)
56	          {
57	            x += WorldGen.genRand.Next(-1, 2);
58	            WorldUtils.Gen(new Point(x, y1), pair1);
59	            if (y1 >= position.Y + 5)
60	            {
61	              WorldUtils.Gen(new Point(x, y1), pair3);
62	              WorldUtils.Gen(new Point(x, y1), pair4);
63	            }
64	            WorldUtils.Gen(new Point(x, y1), pair2);
65	          }
66	          ++y1;
67	        }
68	        else
69	          break;
70	      }
71	      WorldUtils.Gen(new Point(origin.X, origin.Y - (int) ((double) holeRadius * 1.5) + 3), (GenShape) new Shapes.Circle(holeRadius / 2, holeRadius / 3), Actions.Chain(Actions.Chain((GenAction) new Actions.ClearTile(false), (GenAction) new Modifiers.Expand(1), (GenAction) new Actions.PlaceWall((ushort) 0, true))));
72	      WorldUtils.Gen(origin, (GenShape) new ModShapes.All(data), (GenAction) new Actions.Smooth(false));
73	    }
74	  }
75	}
76	

```


---

## 👤 User(sidechain) · 2026-08-08T15:16:35.485Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.GameContent.Biomes.Desert.ChambersEntrance
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using Microsoft.Xna.Framework;
8	using System;
9	using System.Collections.Generic;
10	using Terraria.Utilities;
11	using Terraria.WorldBuilding;
12	
13	namespace Terraria.GameContent.Biomes.Desert
14	{
15	  public static class ChambersEntrance
16	  {
17	    public static void Place(DesertDescription description)
18	    {
19	      int x = description.Desert.Center.X + WorldGen.genRand.Next(-40, 41);
20	      Point position = new Point(x, (int) description.Surface[x]);
21	      ChambersEntrance.PlaceAt(description, position);
22	    }
23	
24	    private static void PlaceAt(DesertDescription description, Point position)
25	    {
26	      ShapeData shapeData = new ShapeData();
27	      Point origin = new Point(position.X, position.Y + 2);
28	      WorldUtils.Gen(origin, (GenShape) new Shapes.Circle(24, 12), Actions.Chain((GenAction) new Modifiers.Blotches(2, 0.3), new Actions.SetTile((ushort) 53, false, true).Output(shapeData)));
29	      UnifiedRandom genRand = WorldGen.genRand;
30	      ShapeData data = new ShapeData();
31	      int num1 = description.Hive.Top - position.Y;
32	      int direction = genRand.Next(2) == 0 ? -1 : 1;
33	      List<ChambersEntrance.PathConnection> pathConnectionList = new List<ChambersEntrance.PathConnection>()
34	      {
35	        new ChambersEntrance.PathConnection(new Point(position.X + -direction * 26, position.Y - 8), direction)
36	      };
37	      int num2 = genRand.Next(2, 4);
38	      for (int index = 0; index < num2; ++index)
39	      {
40	        int y = (int) ((double) (index + 1) / (double) num2 * (double) num1) + genRand.Next(-8, 9);
41	        int x = direction * genRand.Next(20, 41);
42	        int num3 = genRand.Next(18, 29);
43	        WorldUtils.Gen(position, (GenShape) new Shapes.Circle(num3 / 2, 3), Actions.Chain((GenAction) new Modifiers.Offset(x, y), (GenAction) new Modifiers.Blotches(2, 0.3), new Actions.Clear().Output(data), (GenAction) new Actions.PlaceWall((ushort) 187, true)));
44	        pathConnectionList.Add(new ChambersEntrance.PathConnection(new Point(x + num3 / 2 * -direction + position.X, y + position.Y), -direction));
45	        direction *= -1;
46	      }
47	      WorldUtils.Gen(position, (GenShape) new ModShapes.OuterOutline(data, true, false), Actions.Chain((GenAction) new Modifiers.Expand(1), (GenAction) new Modifiers.OnlyTiles(new ushort[1]
48	      {
49	        (ushort) 53
50	      }), (GenAction) new Actions.SetTile((ushort) 397, false, true), (GenAction) new Actions.PlaceWall((ushort) 187, true)));
51	      GenShapeActionPair pair = new GenShapeActionPair((GenShape) new Shapes.Rectangle(2, 4), Actions.Chain((GenAction) new Modifiers.IsSolid(), (GenAction) new Modifiers.Blotches(2, 0.3), (GenAction) new Actions.Clear(), (GenAction) new Modifiers.Expand(1), (GenAction) new Actions.PlaceWall((ushort) 187, true), (GenAction) new Modifiers.OnlyTiles(new ushort[1]
52	      {
53	        (ushort) 53
54	      }), (GenAction) new Actions.SetTile((ushort) 397, false, true)));
55	      for (int index = 1; index < pathConnectionList.Count; ++index)
56	      {
57	        ChambersEntrance.PathConnection pathConnection1 = pathConnectionList[index - 1];
58	        ChambersEntrance.PathConnection pathConnection2 = pathConnectionList[index];
59	        float num3 = Math.Abs(pathConnection2.Position.X - pathConnection1.Position.X) * 1.5f;
60	        for (float amount = 0.0f; (double) amount <= 1.0; amount += 0.02f)
61	        {
62	          Vector2 vector2_1 = new Vector2(pathConnection1.Position.X + pathConnection1.Direction * num3 * amount, pathConnection1.Position.Y);
63	          Vector2 vector2_2 = new Vector2(pathConnection2.Position.X + (float) ((double) pathConnection2.Direction * (double) num3 * (1.0 - (double) amount)), pathConnection2.Position.Y);
64	          Vector2 vector2_3 = Vector2.Lerp(pathConnection1.Position, pathConnection2.Position, amount);
65	          Vector2 vector2_4 = vector2_3;
66	          double num4 = (double) amount;
67	          WorldUtils.Gen(Vector2.Lerp(Vector2.Lerp(vector2_1, vector2_4, (float) num4), Vector2.Lerp(vector2_3, vector2_2, amount), amount).ToPoint(), pair);
68	        }
69	      }
70	      WorldUtils.Gen(origin, (GenShape) new Shapes.Rectangle(new Microsoft.Xna.Framework.Rectangle(-29, -12, 58, 12)), Actions.Chain((GenAction) new Modifiers.NotInShape(shapeData), (GenAction) new Modifiers.Expand(1), (GenAction) new Actions.PlaceWall((ushort) 0, true)));
71	    }
72	
73	    private struct PathConnection
74	    {
75	      public readonly Vector2 Position;
76	      public readonly float Direction;
77	
78	      public PathConnection(Point position, int direction)
79	      {
80	        this.Position = new Vector2((float) position.X, (float) position.Y);
81	        this.Direction = (float) direction;
82	      }
83	    }
84	  }
85	}
86	

```


---

## 🤖 Assistant · 2026-08-08T15:16:36.041Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/LarvaHoleEntrance.cs"
}
```


---

## 🤖 Assistant · 2026-08-08T15:16:36.048Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/PitEntrance.cs"
}
```


---

## 🤖 Assistant · 2026-08-08T15:16:36.053Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/SurfaceMap.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-08T15:16:36.059Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.GameContent.Biomes.Desert.LarvaHoleEntrance
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using Microsoft.Xna.Framework;
8	using Terraria.WorldBuilding;
9	
10	namespace Terraria.GameContent.Biomes.Desert
11	{
12	  public static class LarvaHoleEntrance
13	  {
14	    public static void Place(DesertDescription description)
15	    {
16	      int num = WorldGen.genRand.Next(2, 4);
17	      for (int index = 0; index < num; ++index)
18	      {
19	        int holeRadius = WorldGen.genRand.Next(13, 16);
20	        int x = (int) ((double) (index + 1) / (double) (num + 1) * (double) description.Surface.Width) + description.Desert.Left;
21	        int y = (int) description.Surface[x];
22	        LarvaHoleEntrance.PlaceAt(description, new Point(x, y), holeRadius);
23	      }
24	    }
25	
26	    private static void PlaceAt(DesertDescription description, Point position, int holeRadius)
27	    {
28	      ShapeData data = new ShapeData();
29	      WorldUtils.Gen(position, (GenShape) new Shapes.Rectangle(new Microsoft.Xna.Framework.Rectangle(-holeRadius, -holeRadius * 2, holeRadius * 2, holeRadius * 2)), new Actions.Clear().Output(data));
30	      WorldUtils.Gen(position, (GenShape) new Shapes.Tail((float) (holeRadius * 2), new Vector2(0.0f, (float) holeRadius * 1.5f)), Actions.Chain(new Actions.Clear().Output(data)));
31	      WorldUtils.Gen(position, (GenShape) new ModShapes.All(data), Actions.Chain((GenAction) new Modifiers.Offset(0, 1), (GenAction) new Modifiers.Expand(1), (GenAction) new Modifiers.IsSolid(), (GenAction) new Actions.Smooth(true)));
32	      GenShapeActionPair pair1 = new GenShapeActionPair((GenShape) new Shapes.Rectangle(1, 1), Actions.Chain((GenAction) new Modifiers.Blotches(2, 0.3), (GenAction) new Modifiers.IsSolid(), (GenAction) new Actions.Clear(), (GenAction) new Actions.PlaceWall((ushort) 187, true)));
33	      GenShapeActionPair pair2 = new GenShapeActionPair((GenShape) new Shapes.Circle(2, 3), Actions.Chain((GenAction) new Modifiers.IsSolid(), (GenAction) new Actions.SetTile((ushort) 397, false, true), (GenAction) new Actions.PlaceWall((ushort) 187, true)));
34	      int x = position.X;
35	      int y1 = position.Y + (int) ((double) holeRadius * 1.5);
36	      while (true)
37	      {
38	        int num1 = y1;
39	        Microsoft.Xna.Framework.Rectangle rectangle = description.Hive;
40	        int top1 = rectangle.Top;
41	        int y2 = position.Y;
42	        rectangle = description.Desert;
43	        int top2 = rectangle.Top;
44	        int num2 = (y2 - top2) * 2;
45	        int num3 = top1 + num2 + 12;
46	        if (num1 < num3)
47	        {
48	          WorldUtils.Gen(new Point(x, y1), pair1);
49	          WorldUtils.Gen(new Point(x, y1), pair2);
50	          if (y1 % 3 == 0)
51	          {
52	            x += WorldGen.genRand.Next(-1, 2);
53	            WorldUtils.Gen(new Point(x, y1), pair1);
54	            WorldUtils.Gen(new Point(x, y1), pair2);
55	          }
56	          ++y1;
57	        }
58	        else
59	          break;
60	      }
61	      WorldUtils.Gen(new Point(position.X, position.Y + 2), (GenShape) new ModShapes.All(data), (GenAction) new Actions.PlaceWall((ushort) 0, true));
62	    }
63	  }
64	}
65	

```


---

## 👤 User(sidechain) · 2026-08-08T15:16:36.070Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.GameContent.Biomes.Desert.SurfaceMap
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using System;
8	
9	namespace Terraria.GameContent.Biomes.Desert
10	{
11	  public class SurfaceMap
12	  {
13	    public readonly float Average;
14	    public readonly int Bottom;
15	    public readonly int Top;
16	    public readonly int X;
17	    private readonly short[] _heights;
18	
19	    public int Width
20	    {
21	      get
22	      {
23	        return this._heights.Length;
24	      }
25	    }
26	
27	    private SurfaceMap(short[] heights, int x)
28	    {
29	      this._heights = heights;
30	      this.X = x;
31	      int val1_1 = 0;
32	      int val1_2 = int.MaxValue;
33	      int num = 0;
34	      for (int index = 0; index < heights.Length; ++index)
35	      {
36	        num += (int) heights[index];
37	        val1_1 = Math.Max(val1_1, (int) heights[index]);
38	        val1_2 = Math.Min(val1_2, (int) heights[index]);
39	      }
40	      if ((double) val1_1 > Main.worldSurface - 10.0)
41	        val1_1 = (int) Main.worldSurface - 10;
42	      this.Bottom = val1_1;
43	      this.Top = val1_2;
44	      this.Average = (float) num / (float) this._heights.Length;
45	    }
46	
47	    public short this[int absoluteX]
48	    {
49	      get
50	      {
51	        return this._heights[absoluteX - this.X];
52	      }
53	    }
54	
55	    public static SurfaceMap FromArea(int startX, int width)
56	    {
57	      int num1 = Main.maxTilesY / 2;
58	      short[] heights = new short[width];
59	      for (int index1 = startX; index1 < startX + width; ++index1)
60	      {
61	        bool flag = false;
62	        int num2 = 0;
63	        for (int index2 = 50; index2 < 50 + num1; ++index2)
64	        {
65	          if (Main.tile[index1, index2].active())
66	          {
67	            if (Main.tile[index1, index2].type == (ushort) 189 || Main.tile[index1, index2].type == (ushort) 196 || Main.tile[index1, index2].type == (ushort) 460)
68	              flag = false;
69	            else if (!flag)
70	            {
71	              num2 = index2;
72	              flag = true;
73	            }
74	          }
75	          if (!flag)
76	            num2 = num1 + 50;
77	        }
78	        heights[index1 - startX] = (short) num2;
79	      }
80	      return new SurfaceMap(heights, startX);
81	    }
82	  }
83	}
84	

```


---

## 👤 User(sidechain) · 2026-08-08T15:16:36.072Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.GameContent.Biomes.Desert.PitEntrance
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using Microsoft.Xna.Framework;
8	using System;
9	
10	namespace Terraria.GameContent.Biomes.Desert
11	{
12	  public static class PitEntrance
13	  {
14	    public static void Place(DesertDescription description)
15	    {
16	      int holeRadius = WorldGen.genRand.Next(6, 9);
17	      Point center = description.CombinedArea.Center;
18	      center.Y = (int) description.Surface[center.X];
19	      PitEntrance.PlaceAt(description, center, holeRadius);
20	    }
21	
22	    private static void PlaceAt(DesertDescription description, Point position, int holeRadius)
23	    {
24	      for (int index = -holeRadius - 3; index < holeRadius + 3; ++index)
25	      {
26	        int j = (int) description.Surface[index + position.X];
27	        while (true)
28	        {
29	          int num1 = j;
30	          Rectangle rectangle = description.Hive;
31	          int num2 = rectangle.Top + 10;
32	          if (num1 <= num2)
33	          {
34	            double num3 = (double) (j - (int) description.Surface[index + position.X]);
35	            rectangle = description.Hive;
36	            int top1 = rectangle.Top;
37	            rectangle = description.Desert;
38	            int top2 = rectangle.Top;
39	            double num4 = (double) (top1 - top2);
40	            float yProgress = MathHelper.Clamp((float) (num3 / num4), 0.0f, 1f);
41	            int num5 = (int) ((double) PitEntrance.GetHoleRadiusScaleAt(yProgress) * (double) holeRadius);
42	            if (Math.Abs(index) < num5)
43	              Main.tile[index + position.X, j].ClearEverything();
44	            else if (Math.Abs(index) < num5 + 3 && (double) yProgress > 0.349999994039536)
45	              Main.tile[index + position.X, j].ResetToType((ushort) 397);
46	            float num6 = Math.Abs((float) index / (float) holeRadius);
47	            float num7 = num6 * num6;
48	            if (Math.Abs(index) < num5 + 3 && (double) (j - position.Y) > 15.0 - 3.0 * (double) num7)
49	            {
50	              Main.tile[index + position.X, j].wall = (ushort) 187;
51	              WorldGen.SquareWallFrame(index + position.X, j - 1, true);
52	              WorldGen.SquareWallFrame(index + position.X, j, true);
53	            }
54	            ++j;
55	          }
56	          else
57	            break;
58	        }
59	      }
60	      holeRadius += 4;
61	      for (int index1 = -holeRadius; index1 < holeRadius; ++index1)
62	      {
63	        int num1 = holeRadius - Math.Abs(index1);
64	        int num2 = Math.Min(10, num1 * num1);
65	        for (int index2 = 0; index2 < num2; ++index2)
66	          Main.tile[index1 + position.X, index2 + (int) description.Surface[index1 + position.X]].ClearEverything();
67	      }
68	    }
69	
70	    private static float GetHoleRadiusScaleAt(float yProgress)
71	    {
72	      return (double) yProgress < 0.600000023841858 ? 1f : (float) ((1.0 - (double) PitEntrance.SmootherStep((float) (((double) yProgress - 0.600000023841858) / 0.400000005960464))) * 0.5 + 0.5);
73	    }
74	
75	    private static float SmootherStep(float delta)
76	    {
77	      delta = MathHelper.Clamp(delta, 0.0f, 1f);
78	      return (float) (1.0 - Math.Cos((double) delta * 3.14159274101257) * 0.5 - 0.5);
79	    }
80	  }
81	}
82	

```


---

## 🤖 Assistant · 2026-08-08T15:16:36.134Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/DesertBiome.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-08T15:16:36.145Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.GameContent.Biomes.DesertBiome
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using Microsoft.Xna.Framework;
8	using Newtonsoft.Json;
9	using Terraria.GameContent.Biomes.Desert;
10	using Terraria.WorldBuilding;
11	
12	namespace Terraria.GameContent.Biomes
13	{
14	  public class DesertBiome : MicroBiome
15	  {
16	    [JsonProperty("ChanceOfEntrance")]
17	    public float ChanceOfEntrance = 0.3333f;
18	
19	    public override bool Place(Point origin, StructureMap structures)
20	    {
21	      DesertDescription fromPlacement = DesertDescription.CreateFromPlacement(origin);
22	      if (!fromPlacement.IsValid)
23	        return false;
24	      DesertBiome.ExportDescriptionToEngine(fromPlacement);
25	      SandMound.Place(fromPlacement);
26	      fromPlacement.UpdateSurfaceMap();
27	      if ((double) GenBase._random.NextFloat() <= (double) this.ChanceOfEntrance)
28	      {
29	        switch (GenBase._random.Next(4))
30	        {
31	          case 0:
32	            ChambersEntrance.Place(fromPlacement);
33	            break;
34	          case 1:
35	            AnthillEntrance.Place(fromPlacement);
36	            break;
37	          case 2:
38	            LarvaHoleEntrance.Place(fromPlacement);
39	            break;
40	          case 3:
41	            PitEntrance.Place(fromPlacement);
42	            break;
43	        }
44	      }
45	      DesertHive.Place(fromPlacement);
46	      DesertBiome.CleanupArea(fromPlacement.Hive);
47	      Microsoft.Xna.Framework.Rectangle area = new Microsoft.Xna.Framework.Rectangle(fromPlacement.CombinedArea.X, 50, fromPlacement.CombinedArea.Width, fromPlacement.CombinedArea.Bottom - 20);
48	      structures.AddStructure(area, 10);
49	      return true;
50	    }
51	
52	    private static void ExportDescriptionToEngine(DesertDescription description)
53	    {
54	      WorldGen.UndergroundDesertLocation = description.CombinedArea;
55	      WorldGen.UndergroundDesertLocation.Inflate(10, 10);
56	      WorldGen.UndergroundDesertHiveLocation = description.Hive;
57	    }
58	
59	    private static void CleanupArea(Microsoft.Xna.Framework.Rectangle area)
60	    {
61	      for (int index1 = area.Left - 20; index1 < area.Right + 20; ++index1)
62	      {
63	        for (int index2 = area.Top - 20; index2 < area.Bottom + 20; ++index2)
64	        {
65	          if (index1 > 0 && index1 < Main.maxTilesX - 1 && (index2 > 0 && index2 < Main.maxTilesY - 1))
66	          {
67	            WorldGen.SquareWallFrame(index1, index2, true);
68	            WorldUtils.TileFrame(index1, index2, true);
69	          }
70	        }
71	      }
72	    }
73	  }
74	}
75	

```


---

## 🤖 Assistant · 2026-08-08T15:16:43.960Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me compile the analysis. Let me verify tile IDs: 53 = Sand, 396 = Hardened Sand, 397 = Sandstone, 404 = "Desert Fossil" (actually 404 is Desert Fossil), 187 = wall 187 is Hardened Sand Wall? Let me recall: WallID 187 = Hardened Sand Wall, 216 = Sandstone Wall. Tile 485 = Oasis plants? Actually 485 = "Blinkroot"? No. Tile 485 is... In 1.4.0.5, 484 = Sea Oats? Hmm. Let me think: 484 = Cactus? No. Small flora: 485 = "Desert foliage" (e.g., 485 = PinkPricklyPear?). Actually tile 485 = Pink Prickly Pear, 484 = Pink Sea Oats? Let me check: tile 483 = Sky Mill... Not needed exactly. 484/485 are desert plants placed on hardened sand. 165 = SmokeBlock? No, 165 = "Smoke Block" is 405. 165 = SolarFlare... Actually 165 is "Smoke Block"? Let me recall: tile 165 = "Lava Lamp"? Hmm. 165 is actually "Smoke Block"? No — tile 165 is "Martian Conduit Plating"? No that's 389. Tile 165 is "Bubble"? No.

Tile 165 = "SmokeBlock"? Let me recall Terraria IDs: 161 = Living Loom? Not important. Actually I believe 165 = "Solar Flare" no... 165 is "Bubble Machine"? Better: I recall tile 165 = "Smoke Block" is not right; Smoke Block is 405? Hmm.

Actually in Terraria, tile 165 is "LavaFall"? There's "LiquidDrip". I recall tile 165 = "SmokeBlock" — no. Let me just check if TileID list is available somewhere in the repo, maybe a TileID file.

Tile 485 in 1.4.0.5: 484 = "BambooBlock"? No. Let me search for a TileID.cs file in the project.

Also wall 187 = Hardened Sand Wall, wall 216 = Sandstone Wall — I'm fairly confident.

Note AddTileVariance: WorldGen.PlaceTile(x, y, 485, ...) — 485 is a random-style plant with style Next(4). 484 style 0. 165 is probably "ItemFrame"? no... 165 could be "WaterDrip"? Let's search for TileID in the repo.
```

</details>


---

## 🤖 Assistant · 2026-08-08T15:16:44.797Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/Terarria1405 -iname \"TileID*.cs\" -o -iname \"WallID*.cs\" 2>/dev/null | head -20",
 "description": "Find TileID and WallID definition files"
}
```


---

## 🤖 Assistant · 2026-08-08T15:16:44.848Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rln \"const ushort Sandstone\\|= 397\\|= 396\\|= 404\" ~/Project/GLM/SandboxWorld/Terarria1405 --include=*.cs | head -10",
 "description": "Search for tile id constant definitions"
}
```


---

## 👤 User(sidechain) · 2026-08-08T15:16:44.864Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1405/Enums/TileIDEnum.cs
~/Project/GLM/SandboxWorld/Terarria1405/ID/TileID.cs
~/Project/GLM/SandboxWorld/Terarria1405/ID/WallID.cs

```


---

## 👤 User(sidechain) · 2026-08-08T15:16:44.867Z

**📎 ToolResult**

```
(eval):1: no matches found: --include=*.cs

```


---

## 🤖 Assistant · 2026-08-08T15:16:46.386Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -nE \"= (53|396|397|404|484|485|165|187|216);\" ~/Project/GLM/SandboxWorld/Terarria1405/ID/TileID.cs ~/Project/GLM/SandboxWorld/Terarria1405/ID/WallID.cs",
 "description": "Look up tile and wall id names"
}
```


---

## 👤 User(sidechain) · 2026-08-08T15:16:46.420Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1405/ID/WallID.cs:64:    public const ushort DiamondUnsafe = 53;
~/Project/GLM/SandboxWorld/Terarria1405/ID/WallID.cs:176:    public const ushort SapphireGemspark = 165;
~/Project/GLM/SandboxWorld/Terarria1405/ID/WallID.cs:198:    public const ushort Sandstone = 187;
~/Project/GLM/SandboxWorld/Terarria1405/ID/WallID.cs:227:    public const ushort HardenedSand = 216;
~/Project/GLM/SandboxWorld/Terarria1405/ID/TileID.cs:67:    public const ushort Sand = 53;
~/Project/GLM/SandboxWorld/Terarria1405/ID/TileID.cs:179:    public const ushort Stalactite = 165;
~/Project/GLM/SandboxWorld/Terarria1405/ID/TileID.cs:201:    public const ushort LargePiles2 = 187;
~/Project/GLM/SandboxWorld/Terarria1405/ID/TileID.cs:230:    public const ushort Firework = 216;
~/Project/GLM/SandboxWorld/Terarria1405/ID/TileID.cs:410:    public const ushort Sandstone = 396;
~/Project/GLM/SandboxWorld/Terarria1405/ID/TileID.cs:411:    public const ushort HardenedSand = 397;
~/Project/GLM/SandboxWorld/Terarria1405/ID/TileID.cs:418:    public const ushort DesertFossil = 404;
~/Project/GLM/SandboxWorld/Terarria1405/ID/TileID.cs:498:    public const ushort RollingCactus = 484;
~/Project/GLM/SandboxWorld/Terarria1405/ID/TileID.cs:499:    public const ushort AntlionLarva = 485;

```


---

## 🤖 Assistant · 2026-08-08T15:17:32.658Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Wall IDs: 187 = Sandstone wall, 216 = HardenedSand wall. So in DesertHive, high density → wall 187 (Sandstone wall), medium → wall 187 too, low → wall 216 (Hardened Sand wall), tunnels → wall 187.

Tile IDs: 53 Sand, 396 Sandstone, 397 HardenedSand, 404 DesertFossil, 484 RollingCactus, 485 AntlionLarva, 165 Stalactite.

Now let me write the analysis in Chinese.

SandMound.Place details:

- desert1 = description.Desert but Height = min(Desert.Height, Hive.Height/2). desert2 = Desert shifted: Y = desert1.Bottom, Height = max(0, Desert.Bottom - desert1.Bottom). So desert1 is the surface dune region (upper half), desert2 is the rest down to desert bottom.
- For each column index1 in [-5, Desert.Width + 5):
  - num3 = clamp(|(index1+5)/(Desert.Width+10)| * 2 - 1, -1, 1) — normalized position from center: -1 at left edge, 1 at right edge, 0 at center. This is a square curve (linear in x).
  - if index1 % 3 == 0: num1 = clamp(num1 + genRand.Next(-1,2), -10, 10) — a slowly-varying noise offset updated every 3 columns (random walk clamped to ±10).
  - num2 = clamp(num2 + genRand.Next(-1,2), -10, 10) — updated every column, separate random walk ±10, used for the surface flattening.
  - num4 = sqrt(1 - num3^4) — mound cross-section height profile: at center num3=0 → 1; at edges |num3|=1 → 0. It's a quartic superellipse profile (flatter than circle).
  - num5 (dune surface Y) = desert1.Bottom - (int)(num4 * desert1.Height) + num1 → the dune surface top for this column.
  - If |num3| < 1 (interior columns): carve air above the dune: num6 = UnclampedSmoothStep(0.5, 0.8, |num3|); num7 = num6^3; num8 = min(10 + (int)(desert1.Top - num7*20) + num2, num5). For index2 from surface[index1+X]-1 up to num8-1: deactivate tile and set wall = 0. So near the center the top of the dune is flattened/cleared up to ~desert1.Top + 10 + noise, blending to higher at edges (num7 up to 1 → top - 20).
  - PlaceSandColumn(index1+X, num5, desert2.Bottom - num5): fills from num5 down to desert2.Bottom with sand.

PlaceSandColumn: iterates from bottom (startY+height-1) up to startY; clears liquid, sets type = 53 (sand), slope 0, halfBrick false, active true; `if (index < startY) tile1.active(false)` — that branch is dead code since loop index >= startY (index starts at startY). Note the decompiler shows index2 references j+1, j+2 (tile2/tile3 unused). Actually the original code likely is: it places sand and checks tile below for hardening — but in this decompiled version tile2/tile3 are assigned but unused, so PlaceSandColumn only sets plain sand (53). So SandMound alone places only sand; hardening (396/397) is done in DesertHive.AddTileVariance and entrances. Important fact: SandMound.PlaceSandColumn sets type 53 for every tile in the column — no layering into hardened sand/sandstone. The layering comes from DesertHive thresholds on field strength.

Wait — but I should double check: the original game code for PlaceSandColumn. In the actual Terraria source (tModPorter/tML), SandMound.PlaceSandColumn:

```csharp
private static void PlaceSandColumn(int i, int j, int height)
{
    for (int num = height - 1; num >= 0; num--) {
        Tile tile = Main.tile[i, j + num];
        Tile tile2 = Main.tile[i, j + num + 1];
        Tile tile3 = Main.tile[i, j + num + 2];
        tile.liquid = 0;
        tile.type = 53;
        ...
    }
}
```
Hmm, the decompiled version has dead code `if (index < startY) tile1.active(false)` which corresponds to nothing. The assignments of tile2/tile3 unused — indeed in original they may be unused too. Fine: state facts as in the code: sand only, type 53, all layers; tile2/tile3 read but unused.

DesertHive.Place:

- ClusterGroup.FromDescription(description): grid Width = BlockColumnCount = num2 = (int)(80 * maxTilesX/4200), Height = BlockRowCount = num3 = (int)((rand+1)*170*maxTilesX/4200). BlockScale = (4,2).
- ClusterGroup.Generate: blockMap of Width×Height. Center point (Width/2-1, Height/2-1). Fills an ellipse: for each row index1 from center.Y - y1 to center.Y + y1 where y1 = Height/2-1: num3 = (num1/y1)*(index1 - centerY) (num1 = Width/2-1), num4 = min(num1, sqrt((num1+1)^2 - num3^2)); for columns within center.X ± num4: blockMap = genRand.Next(2)==0 (50% random). So an elliptical mask filled with 50% noise.
- SearchForCluster: flood fill up to depth level=2 (3 levels, Chebyshev-ish via recursion levels), collecting points; clusters with >2 points kept.
- AttemptClaim / clusterIndexMap merging: neighbors randomly claim/erase clusters (50% chance to set neighbor cluster to -1, i.e., delete).
- Rebuild point lists from clusterIndexMap; drop clusters with < 4 points.
- Each remaining cluster becomes a Cluster of Blocks with position jitter ±0.25.
- PlaceClusters: hive = description.Hive inflated by 20 on each side; postEffectMap sized hive.Width×hive.Height; PlaceClustersArea over the inflated area; then for tiles flagged Smooth → Tile.SmoothSlope.
- PlaceClustersArea: fastRandom = FastRandom(seed).WithModifier(57005UL). Per tile (left, top) in inflated area, in world:
  - type = 53 (Sand); with prob 1/3 → 397 (HardenedSand). This `type` is used for the low-density shell.
  - Map tile coordinate into cluster space: vector2_4 = ((x,y) - BlockScale/2) / HiveSize * ClusterGridSize — note vector2_3 = description.BlockScale/2f = (2,1); vector2_1 = Hive dims (Width, Height) in tiles = BlockScale * grid size; vector2_2 = grid dims. So vector2_4 = ((pos - (2,1)) / (4,2) * ... ) effectively the block-grid coordinate.
  - For each cluster whose first block position is within |dx|<=10 and |dy|<=10 of the mapped point: sum num4 += 1/distSq over blocks in cluster. Track max (num1, num2=index) and second-max (num3).
  - num5 = num1 + num3 (combined field of two strongest clusters).
  - flag = normalized distance from hive center ((pos - center)/halfsize*2 - 1).Length() >= 0.8 → outside the ellipse of ~0.8 radius (edge region).
  - Thresholds on num5:
    - num5 > 3.5: cavity interior (hollow chamber): ClearEverything, wall = 187 (Sandstone wall), and if cluster index num2 % 15 == 2 → tile reset to type 404 (Desert Fossil). Marks Smooth.
    - else num5 > 1.8: tunnel/cave: wall = 187; if top < Main.worldSurface → liquid = 0 else lava(true); if !flag (i.e., inside inner ellipse) OR tile already active → ResetToType(396) (Sandstone) and Smooth. Wait: if (!flag || tile.active()) — flag is true when in outer ring. So when in the outer ring (flag true) and tile not active → keeps the tile clear (tunnel open to cave). Hmm, and note: the else-if doesn't clear the tile — so tiles in this band stay whatever they were unless reset to 396. Careful: `if (!flag || tile.active())` → set sandstone; else leave tile as-is (inactive → open air pocket).
    - else num5 > 0.7 || !flag: shell/hardened sand: wall = 216 (Hardened Sand wall), liquid = 0; if (!flag || tile.active()) → ResetToType(type) where type is 53 or 397 (1/3 chance hardened sand); Smooth. Again in outer ring with inactive tile, nothing set (only wall 216).
    - else num5 > 0.25 and fastRandom.WithModifier(x,y).NextFloat() < (num5 - 0.25)/0.45: sparse tunnel edges: wall = 187; liquid 0 or lava; if tile.active() → ResetToType(type) and Smooth.
  - Record PostPlacementEffect (None/Smooth) into postEffectMap.

Note: no explicit underworld limit in DesertHive itself; depth limits come from DesertDescription: Hive origin.Y = y + genRand.Next(40,60) where y = (surfaceMap.Average + surfaceMap.Bottom)/2; height = BlockScale.Y * BlockRowCount = 2 * num3 where num3 ≈ (1..2)*170*(maxTilesX/4200) → 340..680 tiles tall scaled. So hive bottom = origin.Y + height. Also WorldGen.InWorld(left, top, 1) restricts to world bounds + 1. And SurfaceMap.Bottom is clamped to Main.worldSurface - 10.

Let me compute: num1 factor = maxTilesX/4200 (1.0 small, 1.71 large). num2 = 80*factor → BlockColumnCount 80..137 → Hive.Width = 4*num2 = 320..548. num3 = (rand+1)*170*factor → 170..583 rows; Hive.Height = 2*num3 = 340..1166.

Entrances:

ChambersEntrance:
- x = Desert.Center.X + genRand.Next(-40,41); position = (x, Surface[x]).
- origin = (x, y+2). Circle(24,12) with Blotches(2, 0.3) sets tile 53 (sand), output shapeData — a big sand disc at the surface (the mound).
- num1 = Hive.Top - position.Y (depth to hive top). direction = ±1.
- pathConnectionList starts with (position.X + -direction*26, position.Y - 8).
- num2 = genRand.Next(2,4) chambers (2-3).
- For each: y = (index+1)/num2 * num1 + genRand.Next(-8,9); x offset = direction*genRand.Next(20,41); num3 = genRand.Next(18,29); generate Circle(num3/2, 3) with Offset(x,y) and Blotches(2,0.3), Clear() output to data, PlaceWall(187) — carves chamber and places sandstone wall; record path connection at (x + num3/2*-direction + position.X, y + position.Y) with direction -direction; flip direction.
- Then outer outline of carved data expanded by 1, only sand tiles (53) set to 397 (hardened sand) and wall 187.
- Tunnel between consecutive path connections: rectangle 2x4 shape with IsSolid, Blotches(2,0.3), Clear, Expand(1), PlaceWall(187), OnlyTiles(53), SetTile(397). Path is a bezier-ish: for amount 0..1 step 0.02, cubic lerp between connection points with horizontal extensions of length |ΔX|*1.5 in each direction.
- Finally at origin: Rectangle(-29,-12,58,12) NotInShape(shapeData) → Expand(1) → PlaceWall(0) — clears walls in the area above the mound outside the sand shape (so no floating walls).

AnthillEntrance:
- num = genRand.Next(2,4) hills (2-3); holeRadius = genRand.Next(15,18); x spread evenly: (index+1)/(num+1)*Surface.Width + Desert.Left; y = Surface[x].
- PlaceAt: origin = (x, y+6). Tail(holeRadius*2, (0,-holeRadius*1.5)) sets tile 53 (sand cone), output data.
- pair1: Rect(1,1) Blotches(2,0.3) IsSolid Clear PlaceWall(187); genShapeActionPair (no blotches) same; pair2: Circle(2,3) IsSolid SetTile(397) PlaceWall(187); pair3: Circle(holeRadius,3) SkipWalls(187) SetTile(53); pair4: Circle(holeRadius-2,3) PlaceWall(187).
- Vertical shaft: starts at y1 = position.Y - holeRadius - 3 (above ground, top of the mound) and descends until y1 < Hive.Top + (position.Y - Desert.Top)*2 + 12. Each row: if above surface use no-blotch variant else pair1; pair2 (hardened sand ring). Every 3 rows (y1%3==0) and y1 >= position.Y: x += genRand.Next(-1,2) (wiggle); pair1; if y1 >= position.Y+5: pair3 (sand disc radius holeRadius) and pair4 (wall disc radius holeRadius-2) — forms the winding antlion nest chamber blob; pair2 again.
- Finally: Circle(holeRadius/2, holeRadius/3) at origin.Y - holeRadius*1.5 + 3: ClearTile + Expand(1) + PlaceWall(0) — open the top of the mound.
- Smooth all tiles in the tail data.

LarvaHoleEntrance:
- num = 2..3 holes; holeRadius = genRand.Next(13,16); same spread positions.
- PlaceAt: Rectangle(-r, -2r, 2r, 2r) Clear → data; Tail(2r, (0, r*1.5)) Clear → data; then All(data) Offset(0,1) Expand(1) IsSolid Smooth(true) — smooth the hole edges.
- pair1: Rect(1,1) Blotches IsSolid Clear PlaceWall(187); pair2: Circle(2,3) IsSolid SetTile(397) PlaceWall(187).
- Shaft: starts y1 = position.Y + holeRadius*1.5, descends to same limit Hive.Top + (position.Y - Desert.Top)*2 + 12. Every row pair1 + pair2; every 3 rows x wiggle ±1 and repeat pair1/pair2. (No big chamber discs — narrower than anthill.)
- Finally All(data) at (position.X, position.Y+2): PlaceWall(0) — remove walls in the hole.

PitEntrance:
- holeRadius = genRand.Next(6,9); center = CombinedArea.Center with Y = Surface[center.X].
- For each column index in [-r-3, r+3): j from Surface down to Hive.Top + 10:
  - depth = j - Surface[index+X]; yProgress = clamp(depth / (Hive.Top - Desert.Top), 0, 1);
  - num5 = (int)(GetHoleRadiusScaleAt(yProgress) * holeRadius);
  - if |index| < num5 → ClearEverything (open pit);
  - else if |index| < num5+3 && yProgress > 0.35 → ResetToType(397) (hardened sand ring);
  - wall: num6 = |index|/holeRadius; num7 = num6^2; if |index| < num5+3 && (j - position.Y) > 15 - 3*num7 → wall = 187 + SquareWallFrame for j-1 and j.
- Then holeRadius += 4; for index in [-holeRadius, holeRadius): num1 = holeRadius - |index|; num2 = min(10, num1*num1); for index2 in [0, num2): ClearEverything at (index+X, index2 + Surface) — a shallow parabolic bowl (depth capped at 10) opening the surface.
- GetHoleRadiusScaleAt: yProgress < 0.6 → 1.0; else (1 - SmootherStep((yProgress-0.6)/0.4))*0.5 + 0.5 → tapers to 0.5 at bottom. SmootherStep = clamp then 1 - cos(delta*π)*0.5 - 0.5 (cosine ease).

Depth limit check for hive: Does hive reach hell? Hive.Height = 2 * num3 where num3 = (int)((rand.NextFloat()+1)*170*factor). For large world factor = 8400/4200 = 2.0 → num3 ∈ [340, 680); Hive.Height ∈ [680, 1360). Hive top origin.Y ≈ (Average+Bottom)/2 + 40..60, which is around worldSurface (since Bottom is clamped to worldSurface - 10). For a large world maxTilesY = 2400, hell starts ~ 2400*0.8? Underworld boundary ~ maxTilesY - 200 = 2200. worldSurface ≈ 400 (large world surface line ~ 0.3*maxTilesY? Actually worldSurface large = 350ish). So bottom could be 400+60+1360 = 1820, above hell. So hive doesn't limit to underworld explicitly — no hell check in code. The only constraints: WorldGen.InWorld(x,y,1) and the y computed. And the "tunnel" band uses Main.worldSurface as liquid threshold (above worldSurface → no liquid, below → lava). So answer: no explicit hell limit; depth determined by Hive rect height formula. Also note WorldGen.rockLayer etc not used.

Also DesertDescription.RowHasInvalidTiles rejects if row at surfaceMap.Bottom contains tiles 59 (Sandstone? no 59 = Granite?) Actually 59 = Granite? Tile 59 = Granite? Let me check: 59 = "Granite"? In TileID: 59 = Granite, 60 = Marble? Hmm, 59 = Granite? Actually: 57 = Marble, 58 = Granite? Let me quickly grep. Not essential but nice.

Also 147/161: 147 = SpiderNest? 161 = Marble? Let me grep quickly to be accurate.
````

</details>


---

## 🤖 Assistant · 2026-08-08T15:17:32.680Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -nE \"= (59|60|147|161|189|196|460);\" ~/Project/GLM/SandboxWorld/Terarria1405/ID/TileID.cs",
 "description": "Look up additional tile ids"
}
```


---

## 👤 User(sidechain) · 2026-08-08T15:17:32.724Z

**📎 ToolResult**

```
73:    public const ushort Mud = 59;
74:    public const ushort JungleGrass = 60;
161:    public const ushort SnowBlock = 147;
175:    public const ushort IceBlock = 161;
203:    public const ushort Cloud = 189;
210:    public const ushort RainCloud = 196;
474:    public const ushort SnowCloud = 460;

```


---

## 🤖 Assistant · 2026-08-08T15:17:34.768Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All confirmed. Now write the Chinese report. Include hardcoded constants list.

Structure the answer per request. Keep to facts, with file paths.
```

</details>


---

## 🤖 Assistant · 2026-08-08T15:18:17.328Z · glm-x-preview-260804

```
以下为对反编译源码的算法事实梳理。涉及文件:
- `~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/SandMound.cs`
- `~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/DesertHive.cs`
- `~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/DesertDescription.cs`
- `~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/SurfaceMap.cs`
- `~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/Desert/{ChambersEntrance,AnthillEntrance,LarvaHoleEntrance,PitEntrance}.cs`
- `~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/DesertBiome.cs`

调用顺序(DesertBiome.Place):`SandMound.Place` → `UpdateSurfaceMap` → 以 `ChanceOfEntrance = 0.3333f` 概率从四种入口随机选一种(`GenBase._random.Next(4)`)→ `DesertHive.Place` → `CleanupArea`。

---

## 1. SandMound.Place 精确算法

**区域切分(DesertDescription 提供)**
- `desert1`(沙丘地表区)= `description.Desert`,但 `Height = min(Desert.Height, Hive.Height / 2)`。
- `desert2`(向下余区)= Desert 移到 `desert1.Bottom` 之下,`Height = max(0, Desert.Bottom - desert1.Bottom)`。
- 横向扫描范围:`index1 ∈ [-5, desert1.Width + 5)`(向两侧各外扩 5 列)。

**每列表面形状函数**
1. 归一化位置:`num3 = clamp(|(index1 + 5) / (Width + 10)| * 2 - 1, -1, 1)`。中心为 0,两端 ±5 外处为 ±1,线性。
2. 两个钳制随机游走噪声:
   - `num1`:仅当 `index1 % 3 == 0` 时更新,`num1 = clamp(num1 + genRand.Next(-1, 2), -10, 10)`(粗噪声)。
   - `num2`:每列更新,`num2 = clamp(num2 + genRand.Next(-1, 2), -10, 10)`(细噪声)。
3. 沙丘剖面高度系数:`num4 = sqrt(1 - num3⁴)`(四次超椭圆剖面,比圆更平坦;中心 1、边缘 0)。
4. 沙丘表面 Y 值:`num5 = desert1.Bottom - (int)(num4 * desert1.Height) + num1`。

**表面削平/清空(仅当 `|num3| < 1`)**
- `num6 = UnclampedSmoothStep(0.5, 0.8, |num3|)`,`num7 = num6³`。
- `num8 = min(10 + (int)(desert1.Top - num7 * 20.0) + num2, num5)`。
- 对 `index2` 从 `Surface[index1 + X] - 1` 到 `num8 - 1`:`tile.active(false)` 且 `wall = 0`(中心附近把沙丘顶削平,边缘抬高至多 20 格,用 num2 抖动)。

**沙柱填充(PlaceSandColumn)**
- 从 `startY + height - 1`(即 `desert2.Bottom`)向上填到 `num5`,整列高度 `desert2.Bottom - num5`。
- 每个 tile:`liquid = 0`、`type = 53`(Sand)、`slope = 0`、`halfBrick = false`、`active = true`,并调用 `WorldGen.SquareWallFrame`。
- 代码中读取 `j+1`、`j+2` 两个 tile 但**未使用**;`if (index < startY) active(false)` 分支在该循环条件下不可达(死代码)。
- **事实:SandMound 只放纯沙(53),没有沙/硬化沙/沙岩的分层。硬化沙(397)/沙岩(396)分层完全由 DesertHive 的场强阈值产生,入口结构也会写 397。**

---

## 2. DesertHive.Place 精确算法

### 2.1 腔室格阵(ClusterGroup.Generate)
- 格阵尺寸:`Width = description.BlockColumnCount`、`Height = description.BlockRowCount`(由 DesertDescription 计算,见第 4 节)。
- 在 `blockMap[Width, Height]` 上以中心点 `(Width/2 - 1, Height/2 - 1)` 画椭圆:`num1 = Width/2 - 1`,`y1 = Height/2 - 1`,`num2 = (num1+1)²`;每行 `num3 = (num1/y1) * (row - centerY)`,`num4 = min(num1, sqrt(num2 - num3²))`,椭圆内每格 50% 概率(`genRand.Next(2) == 0`)置 true。
- `SearchForCluster`:递归深度 `level = 2`(即最多 3 层扩散)的四邻接泛洪;`Count > 2` 的簇保留。
- `clusterIndexMap` 邻接合并:`AttemptClaim` 对相邻簇以 50% 概率把它整个改为 -1(删除)或并入。
- 由 map 重建 point 列表,丢弃 `Count < 4` 的簇;每点加 ±0.25 的浮点抖动成为 `Block.Position`。

### 2.2 场强计算(PlaceClustersArea)
- 作用区:`description.Hive` 四边 `Inflate(20, 20)`;postEffectMap 同尺寸。
- 随机源:`new FastRandom(Main.ActiveWorldFileData.Seed).WithModifier(57005UL)`。
- 每 tile(`(left, top)`,需 `WorldGen.InWorld(left, top, 1)`):
  - 局部材质 `type = 53`,1/3 概率改为 `397`。
  - 坐标映射到格阵:`vector2_4 = ((x, y) - BlockScale/2) / HiveSize * ClusterGridSize`,其中 `BlockScale/2 = (2, 1)`。
  - 只考察第一个 Block 位置满足 `|ΔX| ≤ 10 && |ΔY| ≤ 10` 的簇;对每簇求 `num4 = Σ 1/dist²(block, 点)`;记录最大 `num1`(对应簇 `num2`)与次大 `num3`。
  - 合成场强 `num5 = num1 + num3`。
  - 边缘标志:`flag = |((x, y) - BlockScale/2) / HiveSize * 2 - (1,1)| ≥ 0.8`(即落在约 0.8 半径的椭圆带外)。

### 2.3 分层判定阈值(按 num5 从高到低)
| 条件 | 操作 |
|---|---|
| `num5 > 3.5` | 腔室内部:`ClearEverything`,`wall = 187`(Sandstone Wall);若 `num2 % 15 == 2` 则 `ResetToType(404)`(Desert Fossil);标记 Smooth |
| `else num5 > 1.8` | 隧道带:`wall = 187`;`top < Main.worldSurface` → `liquid = 0`,否则 `lava(true)`;若 `!flag || tile.active()` → `ResetToType(396)`(Sandstone)并标记 Smooth |
| `else num5 > 0.7 || !flag` | 硬化沙壳:`wall = 216`(Hardened Sand Wall),`liquid = 0`;若 `!flag || tile.active()` → `ResetToType(type)`(type 为 53 或 397)并标记 Smooth |
| `else num5 > 0.25 && rand < (num5 - 0.25) / 0.45` | 隧道外缘噪声:`wall = 187`;同上 worldSurface/lava 判定;若 `tile.active()` → `ResetToType(type)` 并标记 Smooth |
| 否则 | 不改(仅记录 None) |

`rand` 为 `fastRandom.WithModifier(x, y).NextFloat()`(按坐标确定)。

注:三个分支里 `if (!flag || tile.active())` 意味着在 `flag == true` 的外圈且原本无 tile 时,只改墙不改 tile(保留空腔)。

之后对 postEffectMap 中标记 Smooth 的 tile 统一执行 `Tile.SmoothSlope(left, top, false, false)`。

### 2.4 AddTileVariance
- 范围 `Hive` 四边 ±20。第一遍:凡 `type == 53` 且其下 1~2 格不是 Solid 的 → 改为 `397`(硬化沙,即暴露在洞穴面的沙)。
- 第二遍:凡 active 且 `type == 396`(沙岩)的 tile,检查上方 1~3 格与下方 1~3 格是否有 active tile(`flag1`/`flag2`):
  - `flag1 && genRand.Next(5)==0` → `PlaceTile(x, y-1, 485)`(AntlionLarva,style 0..3)
  - 否则 `flag1 && Next(5)==0` → `PlaceTile(x, y-1, 484)`(RollingCactus,style 0)
  - 否则 `flag1 ^ flag2 && Next(5)==0` → `PlaceTile(x, y + (flag1 ? -1 : 1), 165)`(Stalactite,style 0)
  - 否则 `flag1 && Next(5)==0` → `PlaceTile(x, y-1, 187)`(LargePiles2,style 29..34)

### 2.5 关于"地狱限制"
**DesertHive 代码本身没有任何 underworld/hell 边界检查。** 深度完全由 `DesertDescription` 决定:
- `Hive.Y = y + genRand.Next(40, 60)`,其中 `y = (int)((Surface.Average + Surface.Bottom) / 2)`;
- `Surface.Bottom` 在 SurfaceMap 中被钳到 `Main.worldSurface - 10`;
- `Hive.Height = BlockScale.Y * BlockRowCount = 2 * (int)((rand.NextFloat() + 1) * 170 * maxTilesX / 4200)`(340 ~ 约 1166 格,随世界宽度放大);
- 唯一的空间硬约束是 `WorldGen.InWorld(x, y, 1)`。
- 涉及 `Main.worldSurface` 的只有隧道分支的液体判定(地表以上无液体、以下填熔岩),不是深度限制。

---

## 3. 四种入口结构

**ChambersEntrance(腔室入口)**
- 位置:`Desert.Center.X + genRand.Next(-40, 41)`,`y = Surface[x]`;`origin = (x, y+2)`。
- 地表:`Circle(24, 12)` + `Blotches(2, 0.3)` 设 tile 53(沙盘)。
- 深度目标 `num1 = Hive.Top - position.Y`;`num2 = genRand.Next(2, 4)` 个腔室(2~3 个),每腔:深度 `y = (index+1)/num2 * num1 + genRand.Next(-8, 9)`,水平 `direction * genRand.Next(20, 41)`,尺寸 `Circle(genRand.Next(18,29)/2, 3)` + Blotches → `Clear` + `PlaceWall(187)`;方向交替翻转。
- 腔室轮廓 `OuterOutline(data)` + `Expand(1)` + `OnlyTiles(53)` → `SetTile(397)` + `PlaceWall(187)`。
- 隧道:相邻 PathConnection 之间 `Rectangle(2, 4)` 形状 + `IsSolid` + Blotches + Clear + Expand(1) + PlaceWall(187) + OnlyTiles(53) + SetTile(397);路径为对水平外延 `|ΔX| * 1.5` 的三次 Lerp 插值,`amount` 步长 0.02。
- 顶部 `Rectangle(-29, -12, 58, 12)` 中 `NotInShape(沙盘)` 部分 `Expand(1)` 后 `PlaceWall(0)`(清除空中残留墙)。

**AnthillEntrance(蚁丘入口)**
- `num = genRand.Next(2, 4)` 个丘(2~3),`holeRadius = genRand.Next(15, 18)`;x 均布 `(index+1)/(num+1) * Surface.Width + Desert.Left`。
- 地表:`origin = (x, y+6)`,`Tail(holeRadius * 2, (0, -holeRadius * 1.5))` 设 tile 53 形成锥形丘。
- 竖井从 `y - holeRadius - 3`(丘顶上方)向下,直到 `Hive.Top + (position.Y - Desert.Top) * 2 + 12`;每行用 `Rectangle(1,1)`(+Blotches/无 Blotches 两版)Clear + PlaceWall(187),并用 `Circle(2, 3)` 设 397 + PlaceWall(187) 做硬化圈。
- 每 3 行(`y1 % 3 == 0` 且 `y1 ≥ position.Y`)x 随机 ±1 摆动;`y1 ≥ position.Y + 5` 后追加 `Circle(holeRadius, 3)`(SkipWalls 187 后设 53)与 `Circle(holeRadius - 2, 3)`(PlaceWall 187),形成蜿蜒的膨胀巢室。
- 收尾:`Circle(holeRadius/2, holeRadius/3)` 于丘顶 `ClearTile + Expand(1) + PlaceWall(0)` 开口;对 tail data 全体 `Smooth(false)`。

**LarvaHoleEntrance(幼虫洞入口)**
- `num = genRand.Next(2, 4)` 个洞,`holeRadius = genRand.Next(13, 16)`;x 均布同上。
- 洞体:`Rectangle(-r, -2r, 2r, 2r)` Clear + `Tail(2r, (0, r*1.5))` Clear,输出同一 data;`All(data)` 经 `Offset(0,1) + Expand(1) + IsSolid` 做 `Smooth(true)`。
- 竖井从 `position.Y + r*1.5` 向下,深度上限同上(`Hive.Top + (position.Y - Desert.Top)*2 + 12`);每行 `Rectangle(1,1)` Blotches + IsSolid + Clear + PlaceWall(187),以及 `Circle(2,3)` SetTile(397) + PlaceWall(187);每 3 行 x 随机 ±1。没有 Anthill 那种大圆腔。
- 收尾:`All(data)` 于 `(x, y+2)` `PlaceWall(0)`(移除洞内墙)。

**PitEntrance(竖坑入口)**
- `holeRadius = genRand.Next(6, 9)`;中心 = `CombinedArea.Center`,`y = Surface[x]`。
- 主循环 `index ∈ [-r-3, r+3)`,`j` 从 `Surface` 向下直到 `Hive.Top + 10`:
  - `yProgress = clamp((j - Surface) / (Hive.Top - Desert.Top), 0, 1)`;
  - `num5 = GetHoleRadiusScaleAt(yProgress) * holeRadius`:yProgress < 0.6 时为 1,之后 `(1 - SmootherStep((yProgress-0.6)/0.4)) * 0.5 + 0.5` 渐缩到 0.5(`SmootherStep` 为余弦缓动 `1 - cos(δπ)*0.5 - 0.5`);
  - `|index| < num5` → `ClearEverything`(开口);
  - `|index| < num5 + 3` 且 `yProgress > 0.35` → `ResetToType(397)`(硬化沙衬圈);
  - `|index| < num5 + 3` 且 `(j - position.Y) > 15 - 3*(|index|/r)²` → `wall = 187` 并对 `j-1`、`j` 调 `SquareWallFrame`。
- 收尾地表碗:`holeRadius += 4`,`index ∈ [-holeRadius, holeRadius)`,`depth = min(10, (holeRadius - |index|)²)`,自 `Surface` 起 `ClearEverything` 深度 depth 格(抛物线浅碗,最深 10)。

---

## 4. 全部硬编码常量汇总

**DesertDescription**
- `DefaultBlockScale = (4, 2)`(每格阵格对应 tile 数)
- `SCAN_PADDING = 5`
- 世界缩放因子 `maxTilesX / 4200`
- 列数 `num2 = (int)(80 * factor)` → Hive.Width = `4 * num2`
- 行数 `num3 = (int)((genRand.NextFloat() + 1) * 170 * factor)` → Hive.Height = `2 * num3`
- `origin.Y = y + genRand.Next(40, 60)`;`y = (Surface.Average + Surface.Bottom) / 2`
- 无效地形检查:`RowHasInvalidTiles` 在 `Surface.Bottom` 行扫描,类型 59(Mud)、60(JungleGrass)、147(SnowBlock)、161(IceBlock)判为无效(`WorldGen.skipDesertTileCheck` 可跳过)

**SurfaceMap**
- 起始扫描行 50,扫描深度 `maxTilesY / 2`
- `Bottom` 钳制到 `Main.worldSurface - 10`
- 忽略浮空 tile 类型:189(Cloud)、196(RainCloud)、460(SnowCloud);遇悬浮物把该列高度重置为 `maxTilesY/2 + 50`

**SandMound**
- 列范围外扩 5(两端)
- 噪声钳制 ±10;num1 每 3 列更新一次
- 剖面函数 `sqrt(1 - t⁴)`(t 为 ±1 钳制的归一化位置)
- 表面平滑:`UnclampedSmoothStep(0.5f, 0.8f, |t|)` 立方;抬升幅度 20;基础偏移 10
- tile 材质固定 53(Sand)

**DesertHive**
- 随机种子 modifier:`57005UL`
- Hive 外扩 `Inflate(20, 20)`;AddTileVariance 扫描范围 ±20
- 簇筛选半径 `|ΔX| ≤ 10 && |ΔY| ≤ 10`(相对簇首 Block)
- 场强阈值:3.5(腔室)、1.8(隧道)、0.7(硬化沙壳)、0.25 + 概率 `(num5-0.25)/0.45`(隧道外缘)
- 边缘椭圆半径 0.8
- 化石条件:`clusterIndex % 15 == 2` → tile 404(DesertFossil)
- 外壳材质:type 53(Sand),1/3 概率 397(HardenedSand)
- 液体阈值:`Main.worldSurface`(以上清液体、以下 lava)
- 腔室/隧道墙 187(Sandstone Wall),壳墙 216(HardenedSand Wall)
- ClusterGroup:`SearchForCluster` 递归 level 2(3 层);簇最小点数 2(初筛)→ 重合并后 <4 丢弃;Block 抖动 ±0.25;椭圆掩码 50% 密度
- 装饰(各 1/5 概率,仅 flag1/flag2 满足时):tile 485(AntlionLarva, style 0..3)、484(RollingCactus, style 0)、165(Stalactite, style 0)、187(LargePiles2, style 29..34)
- 沙暴露判定:下方 2 格内非 Solid → 53 改 397

**入口通用**
- 入口出现概率 0.3333f;入口类型 `Next(4)` 均分
- Anthill/LarvaHole 竖井深度上限:`Hive.Top + (position.Y - Desert.Top) * 2 + 12`;Pit 主循环下界 `Hive.Top + 10`
- Chambers:地表圆 `Circle(24,12)`;顶部清墙矩形 `(-29,-12,58,12)`;首连接点偏移 `±26, -8`;腔室水平偏移 20~40、y 抖动 ±8、半径 18~28(用 /2 作 x 半径,y 半径 3);腔室数 2~3;隧道截面 `Rectangle(2,4)`,水平外延系数 1.5,插值步长 0.02;Blotches(2, 0.3)
- Anthill:数量 2~3,holeRadius 15~17,丘 `Tail(2r, -1.5r)`,竖井起点 `y - r - 3`,每 3 行 x 抖动 ±1,大腔起点 `position.Y + 5`,顶部开口 `Circle(r/2, r/3)`
- LarvaHole:数量 2~3,holeRadius 13~15,洞体 `Rectangle(-r,-2r,2r,2r)` + `Tail(2r, 1.5r)`,竖井起点 `y + 1.5r`,每 3 行 x 抖动 ±1
- Pit:holeRadius 6~8;`yProgress` 分界 0.6/0.4;半径缩放下限 0.5;硬化沙圈 `num5+3` 且 yProgress > 0.35;墙条件 `15 - 3*(|index|/r)²`;地表碗 `r+4`、深度 `min(10, (r+4-|i|)²)`

**材质/墙 ID 对照(本项目 ID/TileID.cs、ID/WallID.cs)**
- tile:53 Sand、165 Stalactite、187 LargePiles2、396 Sandstone、397 HardenedSand、404 DesertFossil、484 RollingCactus、485 AntlionLarva
- wall:187 Sandstone、216 HardenedSand、0 无墙
```
