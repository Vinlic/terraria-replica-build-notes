# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-07T07:03:46.541Z

```
Explore two things and report precisely:

**A. Vanilla decompiled source at ~/Project/GLM/SandboxWorld/Terarria1405 (Terraria 1.4.0.5)**:
1. `Framing.cs` — total size, and its overall structure: list the main methods (e.g. AddFrame, FrameNearTile, the tile-specific framing methods for blocks/grass/etc., wall framing). For EACH major method give 1-2 sentences on what it does.
2. Focus on SOLID BLOCK framing (no slopes/half-bricks needed): how does the standard block (dirt/stone) frame itself — is there a lookup table like SelfFrame8Way? Look for `BlockStyle`, `GetBlockStyle`, and how the 47-entry or similar table is built/used in Framing.cs (search for arrays like `blockStyleLookup` or numeric literals like 0x02, 0x04 patterns). Quote the core block framing code.
3. GRASS framing: how grass (tile 2) and the grass family (jungle/corrupt/crimson/mushroom grass) frame — search for "grass" in Framing.cs; grass merges with dirt below (the mud+dirt layers). Quote the essential logic: how grass frames itself and its neighbor dirt tiles (I recall grass sets frames on the dirt AROUND it via AddFrame and uses special merge frames).
4. What happens when a tile is PLACED/REMOVED: `AddFrame` / `FrameNearTile` / `Wiring` — the neighbor re-framing cascade (which neighbors get re-framed).
5. Slope/half-brick handling: just note where it lives (we will skip it).

**B. TEdit at ~/Project/GLM/SandboxWorld/Terraria-Map-Editor**:
6. In `src/TEdit.Terraria/Render/TileFraming.cs` (327 lines): the `BlockStyleLookup` (line ~43) and `GetBlockStyle` (line ~297) — quote them fully. Also `DetermineFrameNumber` modes.
7. How TEdit RENDERER (WorldRenderXna.xaml.cs, the CanBlend path around line 5709+) handles GRASS tiles specifically — the sameStyle/mergeMask logic: which tile types count as "same" for grass, how the merge rows (extra rows in Tiles_2 grass sheet, 110 rows) are selected. Quote the relevant rule-table or mask logic for grass if present. Search for "IsGrass" or grass special-casing.

Report with file paths + line numbers, verbatim code for the block framing lookup, grass framing, BlockStyleLookup, and the re-frame cascade. Very thorough.
```

---

## 📎 Attachment · skill_listing · 2026-08-07T07:03:46.547Z

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

## 🤖 Assistant · 2026-08-07T07:03:48.329Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The user wants a thorough exploration of two codebases: vanilla Terraria decompiled Framing.cs, and TEdit's TileFraming.cs plus renderer grass handling. Let me start by locating the files and getting sizes/structure.

Let me run parallel searches.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:03:48.988Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls -la ~/Project/GLM/SandboxWorld/Terarria1405 2>/dev/null | head -30; echo \"---\"; wc -l ~/Project/GLM/SandboxWorld/Terarria1405/Terraria/Framing.cs 2>/dev/null || find ~/Project/GLM/SandboxWorld/Terarria1405 -name \"Framing.cs\" 2>/dev/null",
 "description": "Locate Framing.cs and get its size"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:03:49.063Z

**📎 ToolResult**

```
total 56800
drwxr-xr-x@ 100 user  staff      3200  8月  7 14:45 .
drwxr-xr-x@  22 user  staff       704  8月  7 14:45 ..
drwxr-xr-x@  12 user  staff       384  8月  7 14:45 .git
-rw-r--r--@   1 user  staff        64  8月  7 14:45 .gitignore
drwxr-xr-x@  12 user  staff       384  8月  7 14:45 Achievements
-rw-r--r--@   1 user  staff      5511  8月  7 14:45 Animation.cs
-rw-r--r--@   1 user  staff       669  8月  7 14:45 AssemblyInfo.cs
drwxr-xr-x@  11 user  staff       352  8月  7 14:45 Audio
-rw-r--r--@   1 user  staff      4622  8月  7 14:45 BitsByte.cs
drwxr-xr-x@   8 user  staff       256  8月  7 14:45 Chat
-rw-r--r--@   1 user  staff    112311  8月  7 14:45 Chest.cs
drwxr-xr-x@   7 user  staff       224  8月  7 14:45 Cinematics
-rw-r--r--@   1 user  staff     11400  8月  7 14:45 Cloud.cs
-rw-r--r--@   1 user  staff    126931  8月  7 14:45 Collision.cs
-rw-r--r--@   1 user  staff      6717  8月  7 14:45 CombatText.cs
drwxr-xr-x@  50 user  staff      1600  8月  7 14:45 DataStructures
-rw-r--r--@   1 user  staff     16926  8月  7 14:45 DelegateMethods.cs
-rw-r--r--@   1 user  staff      5477  8月  7 14:45 DeprecatedClassLeftInForLoading.cs
-rw-r--r--@   1 user  staff     85255  8月  7 14:45 Dust.cs
-rw-r--r--@   1 user  staff      4856  8月  7 14:45 Entity.cs
drwxr-xr-x@  14 user  staff       448  8月  7 14:45 Enums
drwxr-xr-x@   3 user  staff        96  8月  7 14:45 Extensions
-rw-r--r--@   1 user  staff      1727  8月  7 14:45 FrameSkipTest.cs
-rw-r--r--@   1 user  staff     18101  8月  7 14:45 Framing.cs
drwxr-xr-x@  76 user  staff      2432  8月  7 14:45 GameContent
drwxr-xr-x@  12 user  staff       384  8月  7 14:45 GameInput
-rw-r--r--@   1 user  staff      2123  8月  7 14:45 GetItemSettings.cs
-rw-r--r--@   1 user  staff     48304  8月  7 14:45 Gore.cs
drwxr-xr-x@  20 user  staff       640  8月  7 14:45 Graphics
---
~/Project/GLM/SandboxWorld/Terarria1405/Framing.cs

```


---

## 🤖 Assistant · 2026-08-07T07:03:49.232Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls -la ~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria/Render/TileFraming.cs; wc -l ~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria/Render/TileFraming.cs",
 "description": "Check TEdit TileFraming.cs size"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:03:49.263Z

**📎 ToolResult**

```
-rw-r--r--@ 1 user  staff  12312  8月  5 00:32 ~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria/Render/TileFraming.cs
     327 ~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria/Render/TileFraming.cs

```


---

## 🤖 Assistant · 2026-08-07T07:03:54.360Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting — the vanilla Framing.cs is only 18KB. Let me check it. Note there are two possible Framing.cs: ~/Project/GLM/SandboxWorld/Terarria1405/Terraria/Framing.cs (found by find) and ~/Project/GLM/SandboxWorld/Terarria1405/Framing.cs. The wc -l output shows "~/Project/GLM/SandboxWorld/Terarria1405/Framing.cs" — hmm, the wc output actually printed the find result. Let me check both files.

Wait, the ls shows Framing.cs 18101 bytes at the root of Terarria1405. And find returned Terraria/Framing.cs. Let me check both.

Actually 18101 bytes is small for vanilla Framing.cs which is typically ~4000 lines (tile framing in vanilla is in Framing.cs with lots of tile-specific methods... actually no — vanilla 1.4.0.5 has Framing.cs of about 3600 lines? Let me check. Actually vanilla Framing.cs contains the main framing logic; tile-specific framing is in Terraria.GameContent.FramingHelper? No. Let me just read it.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:03:55.034Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls -la ~/Project/GLM/SandboxWorld/Terarria1405/Terraria/Framing.cs 2>/dev/null; wc -l ~/Project/GLM/SandboxWorld/Terarria1405/Terraria/Framing.cs 2>/dev/null; echo \"===\"; ls ~/Project/GLM/SandboxWorld/Terarria1405/ | head; echo \"===\"; find ~/Project/GLM/SandboxWorld/Terarria1405 -name \"*.cs\" -path \"*Framing*\" 2>/dev/null",
 "description": "Check both Framing.cs locations"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:03:55.107Z

**📎 ToolResult**

```
===
Achievements
Animation.cs
AssemblyInfo.cs
Audio
BitsByte.cs
Chat
Chest.cs
Cinematics
Cloud.cs
Collision.cs
===
~/Project/GLM/SandboxWorld/Terarria1405/Framing.cs

```


---

## 🤖 Assistant · 2026-08-07T07:03:55.210Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"BlockStyleLookup\\|GetBlockStyle\\|DetermineFrameNumber\\|IsGrass\" ~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria/Render/TileFraming.cs",
 "description": "Find key methods in TEdit TileFraming.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:03:55.240Z

**📎 ToolResult**

```
43:    private static readonly BlockStyle[] BlockStyleLookup =
147:        BlockStyle centerStyle = GetBlockStyle(centerTile);
157:                upStyle = GetBlockStyle(neighbor);
172:                leftStyle = GetBlockStyle(neighbor);
187:                rightStyle = GetBlockStyle(neighbor);
202:                downStyle = GetBlockStyle(neighbor);
217:                BlockStyle cs = GetBlockStyle(corner);
229:                BlockStyle cs = GetBlockStyle(corner);
241:                BlockStyle cs = GetBlockStyle(corner);
253:                BlockStyle cs = GetBlockStyle(corner);
259:        int frameNumber = DetermineFrameNumber(centerType, x, y);
277:    public static int DetermineFrameNumber(ushort tileType, int x, int y)
297:    private static BlockStyle GetBlockStyle(Tile tile)
300:        if (styleIndex >= 0 && styleIndex < BlockStyleLookup.Length)
301:            return BlockStyleLookup[styleIndex];
302:        return BlockStyleLookup[0]; // Full block default

```


---

## 🤖 Assistant · 2026-08-07T07:04:00.926Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The vanilla Framing.cs is at ~/Project/GLM/SandboxWorld/Terarria1405/Framing.cs (18KB, root level). That's quite small for vanilla — vanilla 1.4.0.5 Framing.cs is actually about 3,600 lines? Hmm, no. Let me check: In decompiled Terraria 1.4.0.5, Framing.cs is indeed large (~4000 lines) containing all the framing logic. But maybe this decompile is partial/stub. Let me read it.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:04:00.930Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/Framing.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:04:00.968Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.Framing
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using Microsoft.Xna.Framework;
8	using Terraria.DataStructures;
9	using Terraria.ID;
10	
11	namespace Terraria
12	{
13	  public class Framing
14	  {
15	    private static Point16[][] selfFrame8WayLookup;
16	    private static Point16[][] wallFrameLookup;
17	    private static Point16 frameSize8Way;
18	    private static Point16 wallFrameSize;
19	    private static Framing.BlockStyle[] blockStyleLookup;
20	    private static int[][] phlebasTileFrameNumberLookup;
21	    private static int[][] lazureTileFrameNumberLookup;
22	    private static int[][] centerWallFrameLookup;
23	
24	    public static void Initialize()
25	    {
26	      Framing.selfFrame8WayLookup = new Point16[256][];
27	      Framing.frameSize8Way = new Point16(18, 18);
28	      Framing.Add8WayLookup(0, (short) 9, (short) 3, (short) 10, (short) 3, (short) 11, (short) 3);
29	      Framing.Add8WayLookup(1, (short) 6, (short) 3, (short) 7, (short) 3, (short) 8, (short) 3);
30	      Framing.Add8WayLookup(2, (short) 12, (short) 0, (short) 12, (short) 1, (short) 12, (short) 2);
31	      Framing.Add8WayLookup(3, (short) 15, (short) 2);
32	      Framing.Add8WayLookup(4, (short) 9, (short) 0, (short) 9, (short) 1, (short) 9, (short) 2);
33	      Framing.Add8WayLookup(5, (short) 13, (short) 2);
34	      Framing.Add8WayLookup(6, (short) 6, (short) 4, (short) 7, (short) 4, (short) 8, (short) 4);
35	      Framing.Add8WayLookup(7, (short) 14, (short) 2);
36	      Framing.Add8WayLookup(8, (short) 6, (short) 0, (short) 7, (short) 0, (short) 8, (short) 0);
37	      Framing.Add8WayLookup(9, (short) 5, (short) 0, (short) 5, (short) 1, (short) 5, (short) 2);
38	      Framing.Add8WayLookup(10, (short) 15, (short) 0);
39	      Framing.Add8WayLookup(11, (short) 15, (short) 1);
40	      Framing.Add8WayLookup(12, (short) 13, (short) 0);
41	      Framing.Add8WayLookup(13, (short) 13, (short) 1);
42	      Framing.Add8WayLookup(14, (short) 14, (short) 0);
43	      Framing.Add8WayLookup(15, (short) 14, (short) 1);
44	      Framing.Add8WayLookup(19, (short) 1, (short) 4, (short) 3, (short) 4, (short) 5, (short) 4);
45	      Framing.Add8WayLookup(23, (short) 16, (short) 3);
46	      Framing.Add8WayLookup(27, (short) 17, (short) 0);
47	      Framing.Add8WayLookup(31, (short) 13, (short) 4);
48	      Framing.Add8WayLookup(37, (short) 0, (short) 4, (short) 2, (short) 4, (short) 4, (short) 4);
49	      Framing.Add8WayLookup(39, (short) 17, (short) 3);
50	      Framing.Add8WayLookup(45, (short) 16, (short) 0);
51	      Framing.Add8WayLookup(47, (short) 12, (short) 4);
52	      Framing.Add8WayLookup(55, (short) 1, (short) 2, (short) 2, (short) 2, (short) 3, (short) 2);
53	      Framing.Add8WayLookup(63, (short) 6, (short) 2, (short) 7, (short) 2, (short) 8, (short) 2);
54	      Framing.Add8WayLookup(74, (short) 1, (short) 3, (short) 3, (short) 3, (short) 5, (short) 3);
55	      Framing.Add8WayLookup(75, (short) 17, (short) 1);
56	      Framing.Add8WayLookup(78, (short) 16, (short) 2);
57	      Framing.Add8WayLookup(79, (short) 13, (short) 3);
58	      Framing.Add8WayLookup(91, (short) 4, (short) 0, (short) 4, (short) 1, (short) 4, (short) 2);
59	      Framing.Add8WayLookup(95, (short) 11, (short) 0, (short) 11, (short) 1, (short) 11, (short) 2);
60	      Framing.Add8WayLookup(111, (short) 17, (short) 4);
61	      Framing.Add8WayLookup((int) sbyte.MaxValue, (short) 14, (short) 3);
62	      Framing.Add8WayLookup(140, (short) 0, (short) 3, (short) 2, (short) 3, (short) 4, (short) 3);
63	      Framing.Add8WayLookup(141, (short) 16, (short) 1);
64	      Framing.Add8WayLookup(142, (short) 17, (short) 2);
65	      Framing.Add8WayLookup(143, (short) 12, (short) 3);
66	      Framing.Add8WayLookup(159, (short) 16, (short) 4);
67	      Framing.Add8WayLookup(173, (short) 0, (short) 0, (short) 0, (short) 1, (short) 0, (short) 2);
68	      Framing.Add8WayLookup(175, (short) 10, (short) 0, (short) 10, (short) 1, (short) 10, (short) 2);
69	      Framing.Add8WayLookup(191, (short) 15, (short) 3);
70	      Framing.Add8WayLookup(206, (short) 1, (short) 0, (short) 2, (short) 0, (short) 3, (short) 0);
71	      Framing.Add8WayLookup(207, (short) 6, (short) 1, (short) 7, (short) 1, (short) 8, (short) 1);
72	      Framing.Add8WayLookup(223, (short) 14, (short) 4);
73	      Framing.Add8WayLookup(239, (short) 15, (short) 4);
74	      Framing.Add8WayLookup((int) byte.MaxValue, (short) 1, (short) 1, (short) 2, (short) 1, (short) 3, (short) 1);
75	      Framing.blockStyleLookup = new Framing.BlockStyle[6];
76	      Framing.blockStyleLookup[0] = new Framing.BlockStyle(true, true, true, true);
77	      Framing.blockStyleLookup[1] = new Framing.BlockStyle(false, true, true, true);
78	      Framing.blockStyleLookup[2] = new Framing.BlockStyle(false, true, true, false);
79	      Framing.blockStyleLookup[3] = new Framing.BlockStyle(false, true, false, true);
80	      Framing.blockStyleLookup[4] = new Framing.BlockStyle(true, false, true, false);
81	      Framing.blockStyleLookup[5] = new Framing.BlockStyle(true, false, false, true);
82	      Framing.phlebasTileFrameNumberLookup = new int[4][]
83	      {
84	        new int[3]{ 2, 4, 2 },
85	        new int[3]{ 1, 3, 1 },
86	        new int[3]{ 2, 2, 4 },
87	        new int[3]{ 1, 1, 3 }
88	      };
89	      Framing.lazureTileFrameNumberLookup = new int[2][]
90	      {
91	        new int[2]{ 1, 3 },
92	        new int[2]{ 2, 4 }
93	      };
94	      Framing.centerWallFrameLookup = new int[3][]
95	      {
96	        new int[3]{ 2, 0, 0 },
97	        new int[3]{ 0, 1, 4 },
98	        new int[3]{ 0, 3, 0 }
99	      };
100	      Framing.wallFrameLookup = new Point16[20][];
101	      Framing.wallFrameSize = new Point16(36, 36);
102	      Framing.AddWallFrameLookup(0, (short) 9, (short) 3, (short) 10, (short) 3, (short) 11, (short) 3, (short) 6, (short) 6);
103	      Framing.AddWallFrameLookup(1, (short) 6, (short) 3, (short) 7, (short) 3, (short) 8, (short) 3, (short) 4, (short) 6);
104	      Framing.AddWallFrameLookup(2, (short) 12, (short) 0, (short) 12, (short) 1, (short) 12, (short) 2, (short) 12, (short) 5);
105	      Framing.AddWallFrameLookup(3, (short) 1, (short) 4, (short) 3, (short) 4, (short) 5, (short) 4, (short) 3, (short) 6);
106	      Framing.AddWallFrameLookup(4, (short) 9, (short) 0, (short) 9, (short) 1, (short) 9, (short) 2, (short) 9, (short) 5);
107	      Framing.AddWallFrameLookup(5, (short) 0, (short) 4, (short) 2, (short) 4, (short) 4, (short) 4, (short) 2, (short) 6);
108	      Framing.AddWallFrameLookup(6, (short) 6, (short) 4, (short) 7, (short) 4, (short) 8, (short) 4, (short) 5, (short) 6);
109	      Framing.AddWallFrameLookup(7, (short) 1, (short) 2, (short) 2, (short) 2, (short) 3, (short) 2, (short) 3, (short) 5);
110	      Framing.AddWallFrameLookup(8, (short) 6, (short) 0, (short) 7, (short) 0, (short) 8, (short) 0, (short) 6, (short) 5);
111	      Framing.AddWallFrameLookup(9, (short) 5, (short) 0, (short) 5, (short) 1, (short) 5, (short) 2, (short) 5, (short) 5);
112	      Framing.AddWallFrameLookup(10, (short) 1, (short) 3, (short) 3, (short) 3, (short) 5, (short) 3, (short) 1, (short) 6);
113	      Framing.AddWallFrameLookup(11, (short) 4, (short) 0, (short) 4, (short) 1, (short) 4, (short) 2, (short) 4, (short) 5);
114	      Framing.AddWallFrameLookup(12, (short) 0, (short) 3, (short) 2, (short) 3, (short) 4, (short) 3, (short) 0, (short) 6);
115	      Framing.AddWallFrameLookup(13, (short) 0, (short) 0, (short) 0, (short) 1, (short) 0, (short) 2, (short) 0, (short) 5);
116	      Framing.AddWallFrameLookup(14, (short) 1, (short) 0, (short) 2, (short) 0, (short) 3, (short) 0, (short) 1, (short) 5);
117	      Framing.AddWallFrameLookup(15, (short) 1, (short) 1, (short) 2, (short) 1, (short) 3, (short) 1, (short) 2, (short) 5);
118	      Framing.AddWallFrameLookup(16, (short) 6, (short) 1, (short) 7, (short) 1, (short) 8, (short) 1, (short) 7, (short) 5);
119	      Framing.AddWallFrameLookup(17, (short) 6, (short) 2, (short) 7, (short) 2, (short) 8, (short) 2, (short) 8, (short) 5);
120	      Framing.AddWallFrameLookup(18, (short) 10, (short) 0, (short) 10, (short) 1, (short) 10, (short) 2, (short) 10, (short) 5);
121	      Framing.AddWallFrameLookup(19, (short) 11, (short) 0, (short) 11, (short) 1, (short) 11, (short) 2, (short) 11, (short) 5);
122	    }
123	
124	    private static Framing.BlockStyle FindBlockStyle(Tile blockTile)
125	    {
126	      return Framing.blockStyleLookup[blockTile.blockType()];
127	    }
128	
129	    public static void Add8WayLookup(
130	      int lookup,
131	      short point1X,
132	      short point1Y,
133	      short point2X,
134	      short point2Y,
135	      short point3X,
136	      short point3Y)
137	    {
138	      Point16[] point16Array = new Point16[3]
139	      {
140	        new Point16((int) point1X * (int) Framing.frameSize8Way.X, (int) point1Y * (int) Framing.frameSize8Way.Y),
141	        new Point16((int) point2X * (int) Framing.frameSize8Way.X, (int) point2Y * (int) Framing.frameSize8Way.Y),
142	        new Point16((int) point3X * (int) Framing.frameSize8Way.X, (int) point3Y * (int) Framing.frameSize8Way.Y)
143	      };
144	      Framing.selfFrame8WayLookup[lookup] = point16Array;
145	    }
146	
147	    public static void Add8WayLookup(int lookup, short x, short y)
148	    {
149	      Point16[] point16Array = new Point16[3]
150	      {
151	        new Point16((int) x * (int) Framing.frameSize8Way.X, (int) y * (int) Framing.frameSize8Way.Y),
152	        new Point16((int) x * (int) Framing.frameSize8Way.X, (int) y * (int) Framing.frameSize8Way.Y),
153	        new Point16((int) x * (int) Framing.frameSize8Way.X, (int) y * (int) Framing.frameSize8Way.Y)
154	      };
155	      Framing.selfFrame8WayLookup[lookup] = point16Array;
156	    }
157	
158	    public static void AddWallFrameLookup(
159	      int lookup,
160	      short point1X,
161	      short point1Y,
162	      short point2X,
163	      short point2Y,
164	      short point3X,
165	      short point3Y,
166	      short point4X,
167	      short point4Y)
168	    {
169	      Point16[] point16Array = new Point16[4]
170	      {
171	        new Point16((int) point1X * (int) Framing.wallFrameSize.X, (int) point1Y * (int) Framing.wallFrameSize.Y),
172	        new Point16((int) point2X * (int) Framing.wallFrameSize.X, (int) point2Y * (int) Framing.wallFrameSize.Y),
173	        new Point16((int) point3X * (int) Framing.wallFrameSize.X, (int) point3Y * (int) Framing.wallFrameSize.Y),
174	        new Point16((int) point4X * (int) Framing.wallFrameSize.X, (int) point4Y * (int) Framing.wallFrameSize.Y)
175	      };
176	      Framing.wallFrameLookup[lookup] = point16Array;
177	    }
178	
179	    private static bool WillItBlend(ushort myType, ushort otherType)
180	    {
181	      return TileID.Sets.ForcedDirtMerging[(int) myType] && otherType == (ushort) 0 || Main.tileBrick[(int) myType] && Main.tileBrick[(int) otherType] || (int) TileID.Sets.GemsparkFramingTypes[(int) otherType] == (int) TileID.Sets.GemsparkFramingTypes[(int) myType];
182	    }
183	
184	    public static void SelfFrame8Way(int i, int j, Tile centerTile, bool resetFrame)
185	    {
186	      if (!centerTile.active())
187	        return;
188	      Framing.BlockStyle blockStyle1 = Framing.FindBlockStyle(centerTile);
189	      int index = 0;
190	      Framing.BlockStyle blockStyle2 = new Framing.BlockStyle();
191	      if (blockStyle1.top)
192	      {
193	        Tile tileSafely = Framing.GetTileSafely(i, j - 1);
194	        if (tileSafely.active() && Framing.WillItBlend(centerTile.type, tileSafely.type))
195	        {
196	          blockStyle2 = Framing.FindBlockStyle(tileSafely);
197	          if (blockStyle2.bottom)
198	            index |= 1;
199	          else
200	            blockStyle2.Clear();
201	        }
202	      }
203	      Framing.BlockStyle blockStyle3 = new Framing.BlockStyle();
204	      if (blockStyle1.left)
205	      {
206	        Tile tileSafely = Framing.GetTileSafely(i - 1, j);
207	        if (tileSafely.active() && Framing.WillItBlend(centerTile.type, tileSafely.type))
208	        {
209	          blockStyle3 = Framing.FindBlockStyle(tileSafely);
210	          if (blockStyle3.right)
211	            index |= 2;
212	          else
213	            blockStyle3.Clear();
214	        }
215	      }
216	      Framing.BlockStyle blockStyle4 = new Framing.BlockStyle();
217	      if (blockStyle1.right)
218	      {
219	        Tile tileSafely = Framing.GetTileSafely(i + 1, j);
220	        if (tileSafely.active() && Framing.WillItBlend(centerTile.type, tileSafely.type))
221	        {
222	          blockStyle4 = Framing.FindBlockStyle(tileSafely);
223	          if (blockStyle4.left)
224	            index |= 4;
225	          else
226	            blockStyle4.Clear();
227	        }
228	      }
229	      Framing.BlockStyle blockStyle5 = new Framing.BlockStyle();
230	      if (blockStyle1.bottom)
231	      {
232	        Tile tileSafely = Framing.GetTileSafely(i, j + 1);
233	        if (tileSafely.active() && Framing.WillItBlend(centerTile.type, tileSafely.type))
234	        {
235	          blockStyle5 = Framing.FindBlockStyle(tileSafely);
236	          if (blockStyle5.top)
237	            index |= 8;
238	          else
239	            blockStyle5.Clear();
240	        }
241	      }
242	      if (blockStyle2.left && blockStyle3.top)
243	      {
244	        Tile tileSafely = Framing.GetTileSafely(i - 1, j - 1);
245	        if (tileSafely.active() && Framing.WillItBlend(centerTile.type, tileSafely.type))
246	        {
247	          Framing.BlockStyle blockStyle6 = Framing.FindBlockStyle(tileSafely);
248	          if (blockStyle6.right && blockStyle6.bottom)
249	            index |= 16;
250	        }
251	      }
252	      if (blockStyle2.right && blockStyle4.top)
253	      {
254	        Tile tileSafely = Framing.GetTileSafely(i + 1, j - 1);
255	        if (tileSafely.active() && Framing.WillItBlend(centerTile.type, tileSafely.type))
256	        {
257	          Framing.BlockStyle blockStyle6 = Framing.FindBlockStyle(tileSafely);
258	          if (blockStyle6.left && blockStyle6.bottom)
259	            index |= 32;
260	        }
261	      }
262	      if (blockStyle5.left && blockStyle3.bottom)
263	      {
264	        Tile tileSafely = Framing.GetTileSafely(i - 1, j + 1);
265	        if (tileSafely.active() && Framing.WillItBlend(centerTile.type, tileSafely.type))
266	        {
267	          Framing.BlockStyle blockStyle6 = Framing.FindBlockStyle(tileSafely);
268	          if (blockStyle6.right && blockStyle6.top)
269	            index |= 64;
270	        }
271	      }
272	      if (blockStyle5.right && blockStyle4.bottom)
273	      {
274	        Tile tileSafely = Framing.GetTileSafely(i + 1, j + 1);
275	        if (tileSafely.active() && Framing.WillItBlend(centerTile.type, tileSafely.type))
276	        {
277	          Framing.BlockStyle blockStyle6 = Framing.FindBlockStyle(tileSafely);
278	          if (blockStyle6.left && blockStyle6.top)
279	            index |= 128;
280	        }
281	      }
282	      if (resetFrame)
283	        centerTile.frameNumber((byte) WorldGen.genRand.Next(0, 3));
284	      Point16 point16 = Framing.selfFrame8WayLookup[index][(int) centerTile.frameNumber()];
285	      centerTile.frameX = point16.X;
286	      centerTile.frameY = point16.Y;
287	    }
288	
289	    public static void WallFrame(int i, int j, bool resetFrame = false)
290	    {
291	      if (WorldGen.SkipFramingBecauseOfGen || i <= 0 || (j <= 0 || i >= Main.maxTilesX - 1) || (j >= Main.maxTilesY - 1 || Main.tile[i, j] == null))
292	        return;
293	      if (Main.tile[i, j].wall >= (ushort) 316)
294	        Main.tile[i, j].wall = (ushort) 0;
295	      WorldGen.UpdateMapTile(i, j, true);
296	      Tile tile1 = Main.tile[i, j];
297	      if (tile1.wall == (ushort) 0)
298	      {
299	        tile1.wallColor((byte) 0);
300	      }
301	      else
302	      {
303	        int index1 = 0;
304	        if (j - 1 >= 0)
305	        {
306	          Tile tile2 = Main.tile[i, j - 1];
307	          if (tile2 != null && (tile2.wall > (ushort) 0 || tile2.active() && tile2.type == (ushort) 54))
308	            index1 = 1;
309	        }
310	        if (i - 1 >= 0)
311	        {
312	          Tile tile2 = Main.tile[i - 1, j];
313	          if (tile2 != null && (tile2.wall > (ushort) 0 || tile2.active() && tile2.type == (ushort) 54))
314	            index1 |= 2;
315	        }
316	        if (i + 1 <= Main.maxTilesX - 1)
317	        {
318	          Tile tile2 = Main.tile[i + 1, j];
319	          if (tile2 != null && (tile2.wall > (ushort) 0 || tile2.active() && tile2.type == (ushort) 54))
320	            index1 |= 4;
321	        }
322	        if (j + 1 <= Main.maxTilesY - 1)
323	        {
324	          Tile tile2 = Main.tile[i, j + 1];
325	          if (tile2 != null && (tile2.wall > (ushort) 0 || tile2.active() && tile2.type == (ushort) 54))
326	            index1 |= 8;
327	        }
328	        int index2;
329	        if (Main.wallLargeFrames[(int) tile1.wall] == (byte) 1)
330	        {
331	          index2 = Framing.phlebasTileFrameNumberLookup[j % 4][i % 3] - 1;
332	          tile1.wallFrameNumber((byte) index2);
333	        }
334	        else if (Main.wallLargeFrames[(int) tile1.wall] == (byte) 2)
335	        {
336	          index2 = Framing.lazureTileFrameNumberLookup[i % 2][j % 2] - 1;
337	          tile1.wallFrameNumber((byte) index2);
338	        }
339	        else if (resetFrame)
340	        {
341	          index2 = WorldGen.genRand.Next(0, 3);
342	          if (tile1.wall == (ushort) 21 && WorldGen.genRand.Next(2) == 0)
343	            index2 = 2;
344	          tile1.wallFrameNumber((byte) index2);
345	        }
346	        else
347	          index2 = (int) tile1.wallFrameNumber();
348	        if (index1 == 15)
349	          index1 += Framing.centerWallFrameLookup[i % 3][j % 3];
350	        Point16 point16 = Framing.wallFrameLookup[index1][index2];
351	        tile1.wallFrameX((int) point16.X);
352	        tile1.wallFrameY((int) point16.Y);
353	      }
354	    }
355	
356	    public static Tile GetTileSafely(Vector2 position)
357	    {
358	      position /= 16f;
359	      return Framing.GetTileSafely((int) position.X, (int) position.Y);
360	    }
361	
362	    public static Tile GetTileSafely(Point pt)
363	    {
364	      return Framing.GetTileSafely(pt.X, pt.Y);
365	    }
366	
367	    public static Tile GetTileSafely(Point16 pt)
368	    {
369	      return Framing.GetTileSafely((int) pt.X, (int) pt.Y);
370	    }
371	
372	    public static Tile GetTileSafely(int i, int j)
373	    {
374	      if (!WorldGen.InWorld(i, j, 0))
375	        return new Tile();
376	      Tile tile = Main.tile[i, j];
377	      if (tile == null)
378	      {
379	        tile = new Tile();
380	        Main.tile[i, j] = tile;
381	      }
382	      return tile;
383	    }
384	
385	    private struct BlockStyle
386	    {
387	      public bool top;
388	      public bool bottom;
389	      public bool left;
390	      public bool right;
391	
392	      public BlockStyle(bool up, bool down, bool left, bool right)
393	      {
394	        this.top = up;
395	        this.bottom = down;
396	        this.left = left;
397	        this.right = right;
398	      }
399	
400	      public void Clear()
401	      {
402	        this.top = this.bottom = this.left = this.right = false;
403	      }
404	    }
405	  }
406	}
407	

```


---

## 🤖 Assistant · 2026-08-07T07:04:06.735Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The Framing.cs in the decompiled source is only 407 lines / 18KB — it's a partial subset. It does NOT contain AddFrame, FrameNearTile, tile-specific framing methods, or grass framing. The caller expected the full vanilla Framing.cs. So I need to find where the rest lives in this decompiled source — maybe in a different class (e.g., WorldGen, or Terraria.GameContent.FramingHelper? No). In vanilla 1.4.0.5, Framing.cs is one file with all framing. But this decompile has a smaller Framing.cs. Let me check the size — vanilla Framing.cs 1.4.0.5 is actually ~6600 lines? Hmm. Let me check the actual Terraria source: 1.4.0.5 Framing.cs has AddFrame, FrameNearTile, all the tile framing... Actually I recall that in 1.4, Framing.cs is quite large (~4500 lines). But maybe this decompile split it. Let me search for "FrameNearTile" and "AddFrame" in the whole repo.

Note: plan mode is active and I'm a read-only search agent anyway. I don't need to write a plan file — my job is exploration and reporting. Actually plan mode says I should create a plan file if needed, but as a search agent I should just return findings. The instruction says I'm allowed to write only that plan file; but writing is prohibited by my role. I'll just answer directly with findings (read-only actions only).

Let me search.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:04:07.452Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"FrameNearTile\" ~/Project/GLM/SandboxWorld/Terarria1405 --include=\"*.cs\" -l | head -20; echo \"===\"; grep -rn \"void AddFrame\" ~/Project/GLM/SandboxWorld/Terarria1405 --include=\"*.cs\" | head -10",
 "description": "Find FrameNearTile and AddFrame in vanilla source"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:04:07.558Z

**📎 ToolResult**

```
===

```


---

## 🤖 Assistant · 2026-08-07T07:04:07.732Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rln \"FrameGrass\\|grass\" ~/Project/GLM/SandboxWorld/Terarria1405 --include=\"*.cs\" -i | head -30",
 "description": "Find grass framing references"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:04:07.773Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1405/WorldGen.cs
~/Project/GLM/SandboxWorld/Terarria1405/Player.cs
~/Project/GLM/SandboxWorld/Terarria1405/Main.cs
~/Project/GLM/SandboxWorld/Terarria1405/Enums/TileIDEnum.cs
~/Project/GLM/SandboxWorld/Terarria1405/Audio/LegacySoundPlayer.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Drawing/TileDrawing.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Biomes/EnchantedSwordBiome.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Generation/ActionGrass.cs
~/Project/GLM/SandboxWorld/Terarria1405/ID/NPCID.cs
~/Project/GLM/SandboxWorld/Terarria1405/ID/ItemID.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Generation/PassLegacy.cs
~/Project/GLM/SandboxWorld/Terarria1405/ID/SoundID.cs
~/Project/GLM/SandboxWorld/Terarria1405/ID/ContentSamples.cs
~/Project/GLM/SandboxWorld/Terarria1405/ID/DustID.cs
~/Project/GLM/SandboxWorld/Terarria1405/ID/TileID.cs
~/Project/GLM/SandboxWorld/Terarria1405/ID/WallID.cs

```


---

## 🤖 Assistant · 2026-08-07T07:04:18.044Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So the vanilla decompiled source is a PARTIAL decompile: Framing.cs contains only the lookup-based framing (SelfFrame8Way, WallFrame, blockStyleLookup). The big file with AddFrame/FrameNearTile/tile-specific framing is NOT present. Also no FrameNearTile anywhere.

So the vanilla Framing.cs here is 407 lines, 18,101 bytes. The main methods present:
- Initialize
- FindBlockStyle
- Add8WayLookup (2 overloads)
- AddWallFrameLookup
- WillItBlend
- SelfFrame8Way
- WallFrame
- GetTileSafely (4 overloads)
- BlockStyle struct

Notably: blockStyleLookup here is only 6 entries (indexed by blockType(), i.e., 0-5 where 5 includes half-brick/slopes), not 47. The 47-entry lookup the caller recalls is TEdit's.

Grass framing: not in this Framing.cs. Grass in vanilla is handled... hmm. Actually in vanilla 1.4.0.5, grass tiles use the standard SelfFrame8Way? No — grass tiles (tile 2) in vanilla are drawn by TileDrawing with special treatment: they use "Tiles_2" sheet with extra rows for merging with dirt. Actually in vanilla, grass is merged via `Main.tileMergeDirt[2] = true` and grass frames via SelfFrame8Way? Hmm, no.

Actually in vanilla Terraria, grass framing: TileID 2 (Grass) has TileID.Sets... Let me check the vanilla TileDrawing.cs and see how grass renders. But the caller asked specifically about Framing.cs grass handling — which doesn't exist in this partial decompile. Important finding to report.

But wait — maybe there's another Framing file in the repo, or maybe the decompile is incomplete. Let me check how large Main.cs is and whether the repo has all classes. Also check whether there's a "Framing.cs" in Terraria namespace under a folder. find earlier only found one Framing.cs.

Let me also check what handles grass rendering in vanilla: TileDrawing.cs — search for "Grass" special handling, and TileID.Sets.GrassSeed, Main.tileMergeDirt.

Let me also check the "Slope" handling — in vanilla it's in WorldGen.SlopeTile / Tile.Slope, and Framing doesn't handle slopes (blockType). Note in SelfFrame8Way the BlockStyle lookup indexed by blockType() handles half-bricks/slopes: blockType() returns 0-5 (0=full, 1=half brick, 2=slope2(right up?), 3,4,5 slopes). The 6-entry table gives which edges exist for each block shape.

Now TEdit side. Let me read TileFraming.cs fully, and search the renderer for grass handling.

Also check WorldGen.cs for framing cascade (WorldGen.FrameTile? "FrameAroundThisTile"?). In vanilla, when a tile is placed, WorldGen calls... Let me search for "Framing." usage in the repo to see what's called (e.g., SelfFrame8Way, WallFrame callers), and for the re-frame cascade: probably `WorldGen.SquareTileFrame` or in TileObject. Let me grep.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:04:18.257Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"Framing\\.\" ~/Project/GLM/SandboxWorld/Terarria1405 --include=\"*.cs\" | grep -v \"Framing.cs\" | head -40; echo \"=== wc WorldGen ===\"; wc -l ~/Project/GLM/SandboxWorld/Terarria1405/WorldGen.cs ~/Project/GLM/SandboxWorld/Terarria1405/Main.cs ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Drawing/TileDrawing.cs",
 "description": "Find Framing callers and file sizes"
}
```


---

## 🤖 Assistant · 2026-08-07T07:04:18.273Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria/Render/TileFraming.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:04:18.288Z

**📎 ToolResult**

```
1	using System.Collections.Generic;
2	using TEdit.Geometry;
3	
4	namespace TEdit.Terraria.Render;
5	
6	/// <summary>
7	/// Terraria-accurate tile framing algorithms, ported from Terraria 1.4.5.4 Framing.SelfFrame8Way().
8	/// Used for gemspark blocks and other tiles that use 8-way neighbor-based framing.
9	/// </summary>
10	public static class TileFraming
11	{
12	    private const int FrameSize8Way = 18; // 16px tile + 2px gap
13	
14	    // Gemspark tile IDs that use SelfFrame8Way framing
15	    private static readonly HashSet<int> GemsparkTileIds =
16	        [255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 385, 446, 447, 448];
17	
18	    // phlebasTileFrameNumberLookup[y%4][x%3] (values are 1-based, subtract 1 for 0-based)
19	    private static readonly int[][] PhlebasLookup =
20	    [
21	        [2, 4, 2],
22	        [1, 3, 1],
23	        [2, 2, 4],
24	        [1, 1, 3]
25	    ];
26	
27	    // lazureTileFrameNumberLookup[x%2][y%2] (values are 1-based, subtract 1 for 0-based)
28	    private static readonly int[][] LazureLookup =
29	    [
30	        [1, 3],
31	        [2, 4]
32	    ];
33	
34	    // selfFrame8WayLookup[index][variant] — grid coordinates (col, row), stored as pixel coords
35	    // 47 defined entries from Framing.cs Add8WayLookup calls; remaining 209 are null (safe default used)
36	    private static readonly Vector2Int32[][] SelfFrame8WayLookup = BuildSelfFrame8WayLookup();
37	
38	    /// <summary>
39	    /// BlockStyle lookup matching Terraria's Framing.blockStyleLookup.
40	    /// Index maps to BrickStyle enum value (0=Full, 1=HalfBrick, 2-5=slopes).
41	    /// Each entry defines which faces are open for neighbor connections.
42	    /// </summary>
43	    private static readonly BlockStyle[] BlockStyleLookup =
44	    [
45	        new(Top: true,  Left: true,  Right: true,  Bottom: true),   // 0: Full block
46	        new(Top: false, Left: true,  Right: true,  Bottom: true),   // 1: HalfBrick
47	        new(Top: false, Left: true,  Right: false, Bottom: true),   // 2: SlopeTopRight
48	        new(Top: false, Left: false, Right: true,  Bottom: true),   // 3: SlopeTopLeft
49	        new(Top: true,  Left: false, Right: true,  Bottom: false),  // 4: SlopeBottomRight
50	        new(Top: true,  Left: false, Right: false, Bottom: true),   // 5: SlopeBottomLeft
51	    ];
52	
53	    // Default frame for undefined lookup entries (center tile, all neighbors = index 255, variant 0)
54	    private static readonly Vector2Int32 DefaultFrame = new(1 * FrameSize8Way, 1 * FrameSize8Way);
55	
56	    private static Vector2Int32[][] BuildSelfFrame8WayLookup()
57	    {
58	        var lookup = new Vector2Int32[256][];
59	
60	        void Add3(int index, int x0, int y0, int x1, int y1, int x2, int y2)
61	        {
62	            lookup[index] =
63	            [
64	                new Vector2Int32(x0 * FrameSize8Way, y0 * FrameSize8Way),
65	                new Vector2Int32(x1 * FrameSize8Way, y1 * FrameSize8Way),
66	                new Vector2Int32(x2 * FrameSize8Way, y2 * FrameSize8Way),
67	            ];
68	        }
69	
70	        void Add1(int index, int x, int y)
71	        {
72	            var pt = new Vector2Int32(x * FrameSize8Way, y * FrameSize8Way);
73	            lookup[index] = [pt, pt, pt];
74	        }
75	
76	        // 47 entries from Framing.cs lines 28-74
77	        Add3(0,   9, 3,  10, 3,  11, 3);
78	        Add3(1,   6, 3,   7, 3,   8, 3);
79	        Add3(2,  12, 0,  12, 1,  12, 2);
80	        Add1(3,  15, 2);
81	        Add3(4,   9, 0,   9, 1,   9, 2);
82	        Add1(5,  13, 2);
83	        Add3(6,   6, 4,   7, 4,   8, 4);
84	        Add1(7,  14, 2);
85	        Add3(8,   6, 0,   7, 0,   8, 0);
86	        Add3(9,   5, 0,   5, 1,   5, 2);
87	        Add1(10, 15, 0);
88	        Add1(11, 15, 1);
89	        Add1(12, 13, 0);
90	        Add1(13, 13, 1);
91	        Add1(14, 14, 0);
92	        Add1(15, 14, 1);
93	        Add3(19,  1, 4,   3, 4,   5, 4);
94	        Add1(23, 16, 3);
95	        Add1(27, 17, 0);
96	        Add1(31, 13, 4);
97	        Add3(37,  0, 4,   2, 4,   4, 4);
98	        Add1(39, 17, 3);
99	        Add1(45, 16, 0);
100	        Add1(47, 12, 4);
101	        Add3(55,  1, 2,   2, 2,   3, 2);
102	        Add3(63,  6, 2,   7, 2,   8, 2);
103	        Add3(74,  1, 3,   3, 3,   5, 3);
104	        Add1(75, 17, 1);
105	        Add1(78, 16, 2);
106	        Add1(79, 13, 3);
107	        Add3(91,  4, 0,   4, 1,   4, 2);
108	        Add3(95, 11, 0,  11, 1,  11, 2);
109	        Add1(111, 17, 4);
110	        Add1(127, 14, 3);
111	        Add3(140,  0, 3,   2, 3,   4, 3);
112	        Add1(141, 16, 1);
113	        Add1(142, 17, 2);
114	        Add1(143, 12, 3);
115	        Add1(159, 16, 4);
116	        Add3(173,  0, 0,   0, 1,   0, 2);
117	        Add3(175, 10, 0,  10, 1,  10, 2);
118	        Add1(191, 15, 3);
119	        Add3(206,  1, 0,   2, 0,   3, 0);
120	        Add3(207,  6, 1,   7, 1,   8, 1);
121	        Add1(223, 14, 4);
122	        Add1(239, 15, 4);
123	        Add3(255,  1, 1,   2, 1,   3, 1);
124	
125	        return lookup;
126	    }
127	
128	    /// <summary>
129	    /// Returns true if the tile type uses SelfFrame8Way framing (gemspark blocks).
130	    /// </summary>
131	    public static bool IsGemSpark(ushort tileType) => GemsparkTileIds.Contains(tileType);
132	
133	    /// <summary>
134	    /// Calculate the tile frame for a gemspark (SelfFrame8Way) tile.
135	    /// Returns grid coordinates (col, row) suitable for uvTileCache encoding.
136	    /// </summary>
137	    public static Vector2Int32 CalculateSelfFrame8Way(World world, int x, int y)
138	    {
139	        if (x < 0 || y < 0 || x >= world.TilesWide || y >= world.TilesHigh)
140	            return new Vector2Int32(0, 0);
141	
142	        Tile centerTile = world.Tiles[x, y];
143	        if (!centerTile.IsActive)
144	            return new Vector2Int32(0, 0);
145	
146	        ushort centerType = centerTile.Type;
147	        BlockStyle centerStyle = GetBlockStyle(centerTile);
148	        int index = 0;
149	
150	        // Check Up neighbor (bit 1)
151	        BlockStyle upStyle = default;
152	        if (centerStyle.Top)
153	        {
154	            Tile neighbor = GetTileSafely(world, x, y - 1);
155	            if (neighbor.IsActive && WillItBlendGemspark(centerType, neighbor.Type))
156	            {
157	                upStyle = GetBlockStyle(neighbor);
158	                if (upStyle.Bottom)
159	                    index |= 1;
160	                else
161	                    upStyle = default;
162	            }
163	        }
164	
165	        // Check Left neighbor (bit 2)
166	        BlockStyle leftStyle = default;
167	        if (centerStyle.Left)
168	        {
169	            Tile neighbor = GetTileSafely(world, x - 1, y);
170	            if (neighbor.IsActive && WillItBlendGemspark(centerType, neighbor.Type))
171	            {
172	                leftStyle = GetBlockStyle(neighbor);
173	                if (leftStyle.Right)
174	                    index |= 2;
175	                else
176	                    leftStyle = default;
177	            }
178	        }
179	
180	        // Check Right neighbor (bit 4)
181	        BlockStyle rightStyle = default;
182	        if (centerStyle.Right)
183	        {
184	            Tile neighbor = GetTileSafely(world, x + 1, y);
185	            if (neighbor.IsActive && WillItBlendGemspark(centerType, neighbor.Type))
186	            {
187	                rightStyle = GetBlockStyle(neighbor);
188	                if (rightStyle.Left)
189	                    index |= 4;
190	                else
191	                    rightStyle = default;
192	            }
193	        }
194	
195	        // Check Down neighbor (bit 8)
196	        BlockStyle downStyle = default;
197	        if (centerStyle.Bottom)
198	        {
199	            Tile neighbor = GetTileSafely(world, x, y + 1);
200	            if (neighbor.IsActive && WillItBlendGemspark(centerType, neighbor.Type))
201	            {
202	                downStyle = GetBlockStyle(neighbor);
203	                if (downStyle.Top)
204	                    index |= 8;
205	                else
206	                    downStyle = default;
207	            }
208	        }
209	
210	        // Corner checks — only when BOTH adjacent cardinals connected AND corner tile's faces align
211	        // UpLeft (bit 16): requires Up.left && Left.top
212	        if (upStyle.Left && leftStyle.Top)
213	        {
214	            Tile corner = GetTileSafely(world, x - 1, y - 1);
215	            if (corner.IsActive && WillItBlendGemspark(centerType, corner.Type))
216	            {
217	                BlockStyle cs = GetBlockStyle(corner);
218	                if (cs.Right && cs.Bottom)
219	                    index |= 16;
220	            }
221	        }
222	
223	        // UpRight (bit 32): requires Up.right && Right.top
224	        if (upStyle.Right && rightStyle.Top)
225	        {
226	            Tile corner = GetTileSafely(world, x + 1, y - 1);
227	            if (corner.IsActive && WillItBlendGemspark(centerType, corner.Type))
228	            {
229	                BlockStyle cs = GetBlockStyle(corner);
230	                if (cs.Left && cs.Bottom)
231	                    index |= 32;
232	            }
233	        }
234	
235	        // DownLeft (bit 64): requires Down.left && Left.bottom
236	        if (downStyle.Left && leftStyle.Bottom)
237	        {
238	            Tile corner = GetTileSafely(world, x - 1, y + 1);
239	            if (corner.IsActive && WillItBlendGemspark(centerType, corner.Type))
240	            {
241	                BlockStyle cs = GetBlockStyle(corner);
242	                if (cs.Right && cs.Top)
243	                    index |= 64;
244	            }
245	        }
246	
247	        // DownRight (bit 128): requires Down.right && Right.bottom
248	        if (downStyle.Right && rightStyle.Bottom)
249	        {
250	            Tile corner = GetTileSafely(world, x + 1, y + 1);
251	            if (corner.IsActive && WillItBlendGemspark(centerType, corner.Type))
252	            {
253	                BlockStyle cs = GetBlockStyle(corner);
254	                if (cs.Left && cs.Top)
255	                    index |= 128;
256	            }
257	        }
258	
259	        int frameNumber = DetermineFrameNumber(centerType, x, y);
260	        Vector2Int32[] entry = SelfFrame8WayLookup[index];
261	        if (entry == null)
262	        {
263	            // Undefined lookup entry — use default (safe fallback)
264	            return new Vector2Int32(DefaultFrame.X / FrameSize8Way, DefaultFrame.Y / FrameSize8Way);
265	        }
266	
267	        Vector2Int32 pixelCoords = entry[frameNumber];
268	        return new Vector2Int32(pixelCoords.X / FrameSize8Way, pixelCoords.Y / FrameSize8Way);
269	    }
270	
271	    /// <summary>
272	    /// Determine the frame number (variant 0-2) for a tile based on its LargeFrameType.
273	    /// Mode 0 (default): deterministic position-based (x*7 + y*11) % 3
274	    /// Mode 1 (phlebas): 4x3 repeating pattern
275	    /// Mode 2 (lazure): 2x2 repeating pattern
276	    /// </summary>
277	    public static int DetermineFrameNumber(ushort tileType, int x, int y)
278	    {
279	        byte largeFrameType = GetLargeFrameType(tileType);
280	
281	        if (largeFrameType == 1)
282	            return PhlebasLookup[y % 4][x % 3] - 1;
283	
284	        if (largeFrameType == 2)
285	            return LazureLookup[x % 2][y % 2] - 1;
286	
287	        // Default: deterministic pseudo-random based on position (0-2)
288	        return ((x * 7) + (y * 11)) % 3;
289	    }
290	
291	    /// <summary>
292	    /// For gemsparks, WillItBlend reduces to same-type check.
293	    /// Each gemspark's GemsparkFramingTypes maps to itself; non-gemsparks map to 0.
294	    /// </summary>
295	    private static bool WillItBlendGemspark(ushort myType, ushort otherType) => myType == otherType;
296	
297	    private static BlockStyle GetBlockStyle(Tile tile)
298	    {
299	        int styleIndex = (int)tile.BrickStyle;
300	        if (styleIndex >= 0 && styleIndex < BlockStyleLookup.Length)
301	            return BlockStyleLookup[styleIndex];
302	        return BlockStyleLookup[0]; // Full block default
303	    }
304	
305	    private static Tile GetTileSafely(World world, int x, int y)
306	    {
307	        if (x < 0 || y < 0 || x >= world.TilesWide || y >= world.TilesHigh)
308	            return default;
309	        return world.Tiles[x, y];
310	    }
311	
312	    private static byte GetLargeFrameType(ushort tileType)
313	    {
314	        var tiles = WorldConfiguration.TileProperties;
315	        if (tiles != null && tileType < tiles.Count)
316	            return tiles[tileType].LargeFrameType;
317	        return 0;
318	    }
319	
320	    // Expose lookup tables for testing
321	    internal static Vector2Int32[][] GetSelfFrame8WayLookup() => SelfFrame8WayLookup;
322	    internal static int[][] GetPhlebasLookup() => PhlebasLookup;
323	    internal static int[][] GetLazureLookup() => LazureLookup;
324	    internal static HashSet<int> GetGemsparkTileIds() => GemsparkTileIds;
325	
326	    private readonly record struct BlockStyle(bool Top, bool Left, bool Right, bool Bottom);
327	}
328	

```


---

## 👤 User(sidechain) · 2026-08-07T07:04:18.329Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1405/Collision.cs:1082:      while (Y > 0 && Framing.GetTileSafely(X, Y).liquid > (byte) 0)
~/Project/GLM/SandboxWorld/Terarria1405/Dust.cs:1682:              if (WorldGen.SolidTile(Framing.GetTileSafely(dust.position)) && (double) dust.fadeIn == 0.0 && !dust.noGravity)
~/Project/GLM/SandboxWorld/Terarria1405/Minecart.cs:1411:      Tile tileSafely = Framing.GetTileSafely(tileCoords);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:16180:          Tile tileSafely = Framing.GetTileSafely(new Point((int) this.ai[0], (int) this.ai[1]));
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:20080:                Tile tileSafely = Framing.GetTileSafely(this.doorX, this.doorY);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:20198:                    Tile tileSafely = Framing.GetTileSafely(num11 + index3, num10 + 1);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:20226:                Tile tileSafely1 = Framing.GetTileSafely(num9, num10);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:20227:                Tile tileSafely2 = Framing.GetTileSafely(num9, num10 - 1);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:20228:                Tile tileSafely3 = Framing.GetTileSafely(num9, num10 - 2);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:21002:                  for (int index4 = 10; index4 > 0 && WorldGen.SolidTile(Framing.GetTileSafely((int) vector2_2.X / 16, (int) vector2_2.Y / 16)); vector2_2 = Main.npc[index3].position - Main.npc[index3].Size * 2f + Main.npc[index3].Size * Utils.RandomVector2(Main.rand, 0.0f, 1f) * 5f)
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:21377:              Tile tileSafely = Framing.GetTileSafely(tileCoordinates.X, tileCoordinates.Y);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:21539:        Tile tileSafely = Framing.GetTileSafely(tileX - this.direction * num, tileY + index);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:21591:          Tile tileSafely = Framing.GetTileSafely(i, j);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:22511:          Tile tileSafely1 = Framing.GetTileSafely(num2, num1);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:22512:          Tile tileSafely2 = Framing.GetTileSafely(num2 + 1, num1);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:22523:          Tile tileSafely1 = Framing.GetTileSafely(num2, num1);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:22524:          Tile tileSafely2 = Framing.GetTileSafely(num2 - 1, num1);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:25732:                Tile tileSafely = Framing.GetTileSafely(i, j);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:27432:          Tile tileSafely1 = Framing.GetTileSafely(index + this.direction, j + 1);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:27433:          Tile tileSafely2 = Framing.GetTileSafely(index, j + 1);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:27434:          Tile tileSafely3 = Framing.GetTileSafely(index, j);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:27435:          Tile tileSafely4 = Framing.GetTileSafely(index, j - 1);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:27436:          Tile tileSafely5 = Framing.GetTileSafely(index, j - 2);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:27437:          Tile tileSafely6 = Framing.GetTileSafely(index, j - 3);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:33346:          Tile tileSafely1 = Framing.GetTileSafely(i1, j1);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:33352:              tileSafely1 = Framing.GetTileSafely(i1, j2);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:35567:          Tile tileSafely2 = Framing.GetTileSafely(i2, j3);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:35573:              tileSafely2 = Framing.GetTileSafely(i2, j2);
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:35592:          if (Framing.GetTileSafely((int) this.ai[0], (int) this.ai[1]).frameX >= (short) 36)
~/Project/GLM/SandboxWorld/Terarria1405/Chest.cs:288:      Tile tileSafely1 = Framing.GetTileSafely(X, Y);
~/Project/GLM/SandboxWorld/Terarria1405/Chest.cs:339:          Tile tileSafely2 = Framing.GetTileSafely(i, j);
~/Project/GLM/SandboxWorld/Terarria1405/Chest.cs:414:          Tile tileSafely = Framing.GetTileSafely(i, j);
~/Project/GLM/SandboxWorld/Terarria1405/TileObject.cs:79:            Tile tileSafely = Framing.GetTileSafely(xCoord + index1, yCoord + index2);
~/Project/GLM/SandboxWorld/Terarria1405/TileObject.cs:94:            Tile tileSafely = Framing.GetTileSafely(xCoord + index1, yCoord + index2);
~/Project/GLM/SandboxWorld/Terarria1405/TileObject.cs:115:            Tile tileSafely = Framing.GetTileSafely(num + index, j);
~/Project/GLM/SandboxWorld/Terarria1405/TileObject.cs:127:            Tile tileSafely = Framing.GetTileSafely(num + index, j);
~/Project/GLM/SandboxWorld/Terarria1405/TileObject.cs:139:            Tile tileSafely = Framing.GetTileSafely(i, num + index);
~/Project/GLM/SandboxWorld/Terarria1405/TileObject.cs:151:            Tile tileSafely = Framing.GetTileSafely(i, num + index);
~/Project/GLM/SandboxWorld/Terarria1405/TileObject.cs:301:              Tile tileSafely = Framing.GetTileSafely(num7 + index1, num8 + index2);
~/Project/GLM/SandboxWorld/Terarria1405/TileObject.cs:336:              Tile tileSafely = Framing.GetTileSafely(num7 + num9, num8 + height);
=== wc WorldGen ===
   54961 ~/Project/GLM/SandboxWorld/Terarria1405/WorldGen.cs
   49938 ~/Project/GLM/SandboxWorld/Terarria1405/Main.cs
    6713 ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Drawing/TileDrawing.cs
  111612 total

```


---

## 🤖 Assistant · 2026-08-07T07:04:24.951Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have the TEdit TileFraming.cs fully. Note: this TileFraming.cs is a LOCAL addition (a port) — "ported from Terraria 1.4.5.4 Framing.SelfFrame8Way()". Interesting: it's for gemspark tiles specifically.

Now the renderer grass logic. Let me search WorldRenderXna.xaml.cs around line 5709 for CanBlend, and grass special-casing.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:04:25.656Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor && grep -rn \"IsGrass\\|grass\" src/TEdit.UI/Render/WorldRenderXna.xaml.cs -i | head -40; echo \"=== file ===\"; wc -l src/TEdit.UI/Render/WorldRenderXna.xaml.cs; ls src/TEdit.UI/Render/ | head -30",
 "description": "Search grass logic in WorldRenderXna"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:04:25.718Z

**📎 ToolResult**

```
ugrep: warning: src/TEdit.UI/Render/WorldRenderXna.xaml.cs: No such file or directory
=== file ===
wc: src/TEdit.UI/Render/WorldRenderXna.xaml.cs: open: No such file or directory
ls: src/TEdit.UI/Render/: No such file or directory

```


---

## 🤖 Assistant · 2026-08-07T07:04:25.912Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor && grep -rn \"CanBlend\" src --include=\"*.cs\" | head -20",
 "description": "Find CanBlend usages in TEdit"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:04:25.976Z

**📎 ToolResult**

```
src/SettingsFileUpdater/TerrariaHost/TerrariaWrapper.cs:814:                    CanBlend = TileID.Sets.Conversion.Stone[i] || TileID.Sets.Conversion.Grass[i] || tileSolid[i],
src/SettingsFileUpdater/TerrariaHost/DataModel/TileDataJson.cs:28:    public bool CanBlend { get; set; }
src/TEdit/View/WorldRenderXna.xaml.cs:5709:                            else if (tileprop.CanBlend || !(tileprop.IsFramed || tileprop.IsAnimated))
src/TEdit.Terraria.Tests/DataModel/TilePropertyTests.cs:23:            CanBlend = true,
src/TEdit.Terraria.Tests/DataModel/TilePropertyTests.cs:44:            CanBlend = true,
src/TEdit.Terraria.Tests/DataModel/TilePropertyTests.cs:59:        restored.CanBlend.ShouldBe(true);
src/TEdit.Terraria/Objects/TileProperty.cs:126:    public bool CanBlend { get; set; }

```


---

## 🤖 Assistant · 2026-08-07T07:04:30.335Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Found renderer at src/TEdit/View/WorldRenderXna.xaml.cs. Let's read around line 5600-5900 for the CanBlend path, and search for grass/sameStyle/mergeMask.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:04:30.735Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor && grep -n \"sameStyle\\|mergeMask\\|IsGrass\\|[Gg]rass\\|Tiles_2\\|Merges\\|merge\" src/TEdit/View/WorldRenderXna.xaml.cs | head -60; echo \"===\"; wc -l src/TEdit/View/WorldRenderXna.xaml.cs",
 "description": "Search sameStyle/mergeMask/grass in renderer"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:04:30.793Z

**📎 ToolResult**

```
137:    // Grass/plant tiles that need horizontal flip on alternating X (includes vines)
317:                case 60:  // Jungle Grass
326:                case 23:  // Corrupt Grass
333:                case 199: // Crimson Grass
334:                case 203: // Crimson Grass (alternate ID)
341:                case 109: // Hallowed Grass
348:                case 70:  // Mushroom Grass
2960:        // zones merge instead of accumulating. Must happen before any other drawing
3098:        // Buff radii pass 2: composite the pre-rendered merge onto the world
4479:                                    int treeType = -1; //Default to normal in case no grass grows beneath the tree
5362:                                    // Grass/plant/vine rendering: horizontal flip on alternating X
5726:                                        int sameStyle = 0x00000000;
5727:                                        int mergeMask = 0x00000000;
5731:                                            sameStyle |= (neighborTile[e]?.IsActive == true) ? 0x0001 : 0x0000;
5732:                                            sameStyle |= (neighborTile[n]?.IsActive == true) ? 0x0010 : 0x0000;
5733:                                            sameStyle |= (neighborTile[w]?.IsActive == true) ? 0x0100 : 0x0000;
5734:                                            sameStyle |= (neighborTile[s]?.IsActive == true) ? 0x1000 : 0x0000;
5738:                                            sameStyle |= (neighborTile[e]?.IsActive == true && WorldConfiguration.GetTileProperties(neighborTile[e].Value.Type).IsStone) ? 0x0001 : 0x0000;
5739:                                            sameStyle |= (neighborTile[n]?.IsActive == true && WorldConfiguration.GetTileProperties(neighborTile[n].Value.Type).IsStone) ? 0x0010 : 0x0000;
5740:                                            sameStyle |= (neighborTile[w]?.IsActive == true && WorldConfiguration.GetTileProperties(neighborTile[w].Value.Type).IsStone) ? 0x0100 : 0x0000;
5741:                                            sameStyle |= (neighborTile[s]?.IsActive == true && WorldConfiguration.GetTileProperties(neighborTile[s].Value.Type).IsStone) ? 0x1000 : 0x0000;
5742:                                            sameStyle |= (neighborTile[ne]?.IsActive == true && WorldConfiguration.GetTileProperties(neighborTile[ne].Value.Type).IsStone) ? 0x00010000 : 0x00000000;
5743:                                            sameStyle |= (neighborTile[nw]?.IsActive == true && WorldConfiguration.GetTileProperties(neighborTile[nw].Value.Type).IsStone) ? 0x00100000 : 0x00000000;
5744:                                            sameStyle |= (neighborTile[sw]?.IsActive == true && WorldConfiguration.GetTileProperties(neighborTile[sw].Value.Type).IsStone) ? 0x01000000 : 0x00000000;
5745:                                            sameStyle |= (neighborTile[se]?.IsActive == true && WorldConfiguration.GetTileProperties(neighborTile[se].Value.Type).IsStone) ? 0x10000000 : 0x00000000;
5749:                                            //Join to nearby tiles if their merge type is this tile's type
5750:                                            sameStyle |= (neighborTile[e]?.IsActive == true && tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[e].Value.Type))) ? 0x0001 : 0x0000;
5751:                                            sameStyle |= (neighborTile[n]?.IsActive == true && tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[n].Value.Type))) ? 0x0010 : 0x0000;
5752:                                            sameStyle |= (neighborTile[w]?.IsActive == true && tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[w].Value.Type))) ? 0x0100 : 0x0000;
5753:                                            sameStyle |= (neighborTile[s]?.IsActive == true && tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[s].Value.Type))) ? 0x1000 : 0x0000;
5754:                                            sameStyle |= (neighborTile[ne]?.IsActive == true && tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[ne].Value.Type))) ? 0x00010000 : 0x00000000;
5755:                                            sameStyle |= (neighborTile[nw]?.IsActive == true && tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[nw].Value.Type))) ? 0x00100000 : 0x00000000;
5756:                                            sameStyle |= (neighborTile[sw]?.IsActive == true && tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[sw].Value.Type))) ? 0x01000000 : 0x00000000;
5757:                                            sameStyle |= (neighborTile[se]?.IsActive == true && tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[se].Value.Type))) ? 0x10000000 : 0x00000000;
5759:                                            sameStyle |= (neighborTile[e]?.IsActive == true && curtile.Type == neighborTile[e].Value.Type) ? 0x0001 : 0x0000;
5760:                                            sameStyle |= (neighborTile[n]?.IsActive == true && curtile.Type == neighborTile[n].Value.Type) ? 0x0010 : 0x0000;
5761:                                            sameStyle |= (neighborTile[w]?.IsActive == true && curtile.Type == neighborTile[w].Value.Type) ? 0x0100 : 0x0000;
5762:                                            sameStyle |= (neighborTile[s]?.IsActive == true && curtile.Type == neighborTile[s].Value.Type) ? 0x1000 : 0x0000;
5763:                                            sameStyle |= (neighborTile[ne]?.IsActive == true && curtile.Type == neighborTile[ne].Value.Type) ? 0x00010000 : 0x00000000;
5764:                                            sameStyle |= (neighborTile[nw]?.IsActive == true && curtile.Type == neighborTile[nw].Value.Type) ? 0x00100000 : 0x00000000;
5765:                                            sameStyle |= (neighborTile[sw]?.IsActive == true && curtile.Type == neighborTile[sw].Value.Type) ? 0x01000000 : 0x00000000;
5766:                                            sameStyle |= (neighborTile[se]?.IsActive == true && curtile.Type == neighborTile[se].Value.Type) ? 0x10000000 : 0x00000000;
5771:                                            lazyCheckReady &= (neighborTile[e] == null || neighborTile[e].Value.IsActive == false || !tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[e].Value.Type))) ? true : (neighborTile[e].Value.lazyMergeId != 0xFF);
5772:                                            lazyCheckReady &= (neighborTile[n] == null || neighborTile[n].Value.IsActive == false || !tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[n].Value.Type))) ? true : (neighborTile[n].Value.lazyMergeId != 0xFF);
5773:                                            lazyCheckReady &= (neighborTile[w] == null || neighborTile[w].Value.IsActive == false || !tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[w].Value.Type))) ? true : (neighborTile[w].Value.lazyMergeId != 0xFF);
5774:                                            lazyCheckReady &= (neighborTile[s] == null || neighborTile[s].Value.IsActive == false || !tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[s].Value.Type))) ? true : (neighborTile[s].Value.lazyMergeId != 0xFF);
5777:                                                sameStyle &= 0x11111110 | ((neighborTile[e] == null || neighborTile[e].Value.IsActive == false || !tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[e].Value.Type))) ? 0x00000001 : ((neighborTile[e].Value.lazyMergeId & 0x04) >> 2));
5778:                                                sameStyle &= 0x11111101 | ((neighborTile[n] == null || neighborTile[n].Value.IsActive == false || !tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[n].Value.Type))) ? 0x00000010 : ((neighborTile[n].Value.lazyMergeId & 0x08) << 1));
5779:                                                sameStyle &= 0x11111011 | ((neighborTile[w] == null || neighborTile[w].Value.IsActive == false || !tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[w].Value.Type))) ? 0x00000100 : ((neighborTile[w].Value.lazyMergeId & 0x01) << 8));
5780:                                                sameStyle &= 0x11110111 | ((neighborTile[s] == null || neighborTile[s].Value.IsActive == false || !tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[s].Value.Type))) ? 0x00001000 : ((neighborTile[s].Value.lazyMergeId & 0x02) << 11));
5784:                                        if (tileprop.MergeWith.HasValue && tileprop.MergeWith.Value > -1) //Merges with a specific type
5786:                                            mergeMask |= (neighborTile[e]?.IsActive == true && neighborTile[e].Value.Type == tileprop.MergeWith.Value) ? 0x0001 : 0x0000;
5787:                                            mergeMask |= (neighborTile[n]?.IsActive == true && neighborTile[n].Value.Type == tileprop.MergeWith.Value) ? 0x0010 : 0x0000;
5788:                                            mergeMask |= (neighborTile[w]?.IsActive == true && neighborTile[w].Value.Type == tileprop.MergeWith.Value) ? 0x0100 : 0x0000;
5789:                                            mergeMask |= (neighborTile[s]?.IsActive == true && neighborTile[s].Value.Type == tileprop.MergeWith.Value) ? 0x1000 : 0x0000;
5790:                                            mergeMask |= (neighborTile[ne]?.IsActive == true && neighborTile[ne].Value.Type == tileprop.MergeWith.Value) ? 0x00010000 : 0x00000000;
5791:                                            mergeMask |= (neighborTile[nw]?.IsActive == true && neighborTile[nw].Value.Type == tileprop.MergeWith.Value) ? 0x00100000 : 0x00000000;
5792:                                            mergeMask |= (neighborTile[sw]?.IsActive == true && neighborTile[sw].Value.Type == tileprop.MergeWith.Value) ? 0x01000000 : 0x00000000;
5793:                                            mergeMask |= (neighborTile[se]?.IsActive == true && neighborTile[se].Value.Type == tileprop.MergeWith.Value) ? 0x10000000 : 0x00000000;
5796:                                        if (tileprop.IsGrass)
===
    8757 src/TEdit/View/WorldRenderXna.xaml.cs

```


---

## 🤖 Assistant · 2026-08-07T07:04:37.886Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
There's an IsGrass at 5796. Let me read lines 5650-6000 of the renderer. Also check TileProperty.IsGrass / Merges / MergeWith definitions. And the grass cases at lines 300-360 (a switch probably for grass rendering rows).
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:04:38.399Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit/View/WorldRenderXna.xaml.cs",
 "offset": 5680,
 "limit": 330
}
```


---

## 🤖 Assistant · 2026-08-07T07:04:38.408Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor && grep -n \"IsGrass\\|Merges\\|MergeWith\\|IsStone\" src/TEdit.Terraria/Objects/TileProperty.cs | head -30",
 "description": "Read TileProperty merge definitions"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:04:38.457Z

**📎 ToolResult**

```
122:    public bool IsGrass { get; set; }
125:    public bool IsStone { get; set; }
127:    public int? MergeWith { get; set; }
162:    public bool Merges(int other)
166:        if (!MergeWith.HasValue) return false;
168:        return MergeWith.Value == other;
171:    public bool Merges(TileProperty other)
173:        if (other.MergeWith.HasValue && other.MergeWith.Value == Id) return true;
174:        if (MergeWith.HasValue && MergeWith.Value == other.Id) return true;
175:        if (MergeWith.HasValue && other.MergeWith.HasValue && MergeWith.Value == other.MergeWith.Value) return true;

```


---

## 👤 User(sidechain) · 2026-08-07T07:04:38.584Z

**📎 ToolResult**

```
5680	                                                break;
5681	                                            }
5682	                                            if (checkTile != null && checkTile.Value.IsActive && checkTile.Value.Type == (int)TileType.EbonsandBlock) //Corruption
5683	                                            {
5684	                                                uv.X += 16;
5685	                                                break;
5686	                                            }
5687	                                            else if (checkTile != null && checkTile.Value.IsActive && checkTile.Value.Type == (int)TileType.PearlsandBlock) //Hallow
5688	                                            {
5689	                                                uv.X += 8;
5690	                                                break;
5691	                                            }
5692	                                        }
5693	                                        curtile.hasLazyChecked = true;
5694	
5695	                                        curtile.uvTileCache = (ushort)((uv.Y << 8) + uv.X);
5696	                                    }
5697	
5698	                                    var texsize = new Vector2Int32(tileprop.TextureGrid.X, tileprop.TextureGrid.Y);
5699	                                    if (texsize.X == 0 || texsize.Y == 0)
5700	                                    {
5701	                                        texsize = new Vector2Int32(16, 16);
5702	                                    }
5703	                                    var source = new Rectangle(((curtile.uvTileCache & 0x00FF) % 8) * (texsize.X + 2), (curtile.uvTileCache >> 8) * (texsize.Y + 2), texsize.X, texsize.Y);
5704	                                    var dest = new Rectangle(1 + (int)((_scrollPosition.X + x) * _zoom), 1 + (int)((_scrollPosition.Y + y) * _zoom), (int)_zoom, (int)_zoom);
5705	
5706	                                    _spriteBatch.Draw(tileTex, dest, source, tilePaintColor, 0f, default, SpriteEffects.None, LayerTileTextures);
5707	                                }
5708	                            }
5709	                            else if (tileprop.CanBlend || !(tileprop.IsFramed || tileprop.IsAnimated))
5710	                            {
5711	                                var tileTex = _textureDictionary.GetTile(curtile.Type);
5712	
5713	                                if (tileTex != null)
5714	                                {
5715	                                    if (curtile.uvTileCache == 0xFFFF || curtile.hasLazyChecked == false)
5716	                                    {
5717	                                        if (TileFraming.IsGemSpark(curtile.Type))
5718	                                        {
5719	                                            var uv = TileFraming.CalculateSelfFrame8Way(_wvm.CurrentWorld, x, y);
5720	                                            curtile.uvTileCache = (ushort)((uv.Y << 8) + uv.X);
5721	                                            curtile.hasLazyChecked = true;
5722	                                        }
5723	                                        else
5724	                                        {
5725	                                        // TODO: Replace BlendRules path with full TileFrameCosmetic port for pixel-perfect accuracy
5726	                                        int sameStyle = 0x00000000;
5727	                                        int mergeMask = 0x00000000;
5728	                                        int strictness = 0;
5729	                                        if (tileprop.MergeWith.HasValue && tileprop.MergeWith.Value == -1) //Basically for cobweb
5730	                                        {
5731	                                            sameStyle |= (neighborTile[e]?.IsActive == true) ? 0x0001 : 0x0000;
5732	                                            sameStyle |= (neighborTile[n]?.IsActive == true) ? 0x0010 : 0x0000;
5733	                                            sameStyle |= (neighborTile[w]?.IsActive == true) ? 0x0100 : 0x0000;
5734	                                            sameStyle |= (neighborTile[s]?.IsActive == true) ? 0x1000 : 0x0000;
5735	                                        }
5736	                                        else if (tileprop.IsStone) //Stone & Gems
5737	                                        {
5738	                                            sameStyle |= (neighborTile[e]?.IsActive == true && WorldConfiguration.GetTileProperties(neighborTile[e].Value.Type).IsStone) ? 0x0001 : 0x0000;
5739	                                            sameStyle |= (neighborTile[n]?.IsActive == true && WorldConfiguration.GetTileProperties(neighborTile[n].Value.Type).IsStone) ? 0x0010 : 0x0000;
5740	                                            sameStyle |= (neighborTile[w]?.IsActive == true && WorldConfiguration.GetTileProperties(neighborTile[w].Value.Type).IsStone) ? 0x0100 : 0x0000;
5741	                                            sameStyle |= (neighborTile[s]?.IsActive == true && WorldConfiguration.GetTileProperties(neighborTile[s].Value.Type).IsStone) ? 0x1000 : 0x0000;
5742	                                            sameStyle |= (neighborTile[ne]?.IsActive == true && WorldConfiguration.GetTileProperties(neighborTile[ne].Value.Type).IsStone) ? 0x00010000 : 0x00000000;
5743	                                            sameStyle |= (neighborTile[nw]?.IsActive == true && WorldConfiguration.GetTileProperties(neighborTile[nw].Value.Type).IsStone) ? 0x00100000 : 0x00000000;
5744	                                            sameStyle |= (neighborTile[sw]?.IsActive == true && WorldConfiguration.GetTileProperties(neighborTile[sw].Value.Type).IsStone) ? 0x01000000 : 0x00000000;
5745	                                            sameStyle |= (neighborTile[se]?.IsActive == true && WorldConfiguration.GetTileProperties(neighborTile[se].Value.Type).IsStone) ? 0x10000000 : 0x00000000;
5746	                                        }
5747	                                        else //Everything else
5748	                                        {
5749	                                            //Join to nearby tiles if their merge type is this tile's type
5750	                                            sameStyle |= (neighborTile[e]?.IsActive == true && tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[e].Value.Type))) ? 0x0001 : 0x0000;
5751	                                            sameStyle |= (neighborTile[n]?.IsActive == true && tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[n].Value.Type))) ? 0x0010 : 0x0000;
5752	                                            sameStyle |= (neighborTile[w]?.IsActive == true && tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[w].Value.Type))) ? 0x0100 : 0x0000;
5753	                                            sameStyle |= (neighborTile[s]?.IsActive == true && tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[s].Value.Type))) ? 0x1000 : 0x0000;
5754	                                            sameStyle |= (neighborTile[ne]?.IsActive == true && tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[ne].Value.Type))) ? 0x00010000 : 0x00000000;
5755	                                            sameStyle |= (neighborTile[nw]?.IsActive == true && tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[nw].Value.Type))) ? 0x00100000 : 0x00000000;
5756	                                            sameStyle |= (neighborTile[sw]?.IsActive == true && tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[sw].Value.Type))) ? 0x01000000 : 0x00000000;
5757	                                            sameStyle |= (neighborTile[se]?.IsActive == true && tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[se].Value.Type))) ? 0x10000000 : 0x00000000;
5758	                                            //Join if nearby tiles have the same type as this tile's type
5759	                                            sameStyle |= (neighborTile[e]?.IsActive == true && curtile.Type == neighborTile[e].Value.Type) ? 0x0001 : 0x0000;
5760	                                            sameStyle |= (neighborTile[n]?.IsActive == true && curtile.Type == neighborTile[n].Value.Type) ? 0x0010 : 0x0000;
5761	                                            sameStyle |= (neighborTile[w]?.IsActive == true && curtile.Type == neighborTile[w].Value.Type) ? 0x0100 : 0x0000;
5762	                                            sameStyle |= (neighborTile[s]?.IsActive == true && curtile.Type == neighborTile[s].Value.Type) ? 0x1000 : 0x0000;
5763	                                            sameStyle |= (neighborTile[ne]?.IsActive == true && curtile.Type == neighborTile[ne].Value.Type) ? 0x00010000 : 0x00000000;
5764	                                            sameStyle |= (neighborTile[nw]?.IsActive == true && curtile.Type == neighborTile[nw].Value.Type) ? 0x00100000 : 0x00000000;
5765	                                            sameStyle |= (neighborTile[sw]?.IsActive == true && curtile.Type == neighborTile[sw].Value.Type) ? 0x01000000 : 0x00000000;
5766	                                            sameStyle |= (neighborTile[se]?.IsActive == true && curtile.Type == neighborTile[se].Value.Type) ? 0x10000000 : 0x00000000;
5767	                                        }
5768	                                        if (curtile.hasLazyChecked == false)
5769	                                        {
5770	                                            bool lazyCheckReady = true;
5771	                                            lazyCheckReady &= (neighborTile[e] == null || neighborTile[e].Value.IsActive == false || !tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[e].Value.Type))) ? true : (neighborTile[e].Value.lazyMergeId != 0xFF);
5772	                                            lazyCheckReady &= (neighborTile[n] == null || neighborTile[n].Value.IsActive == false || !tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[n].Value.Type))) ? true : (neighborTile[n].Value.lazyMergeId != 0xFF);
5773	                                            lazyCheckReady &= (neighborTile[w] == null || neighborTile[w].Value.IsActive == false || !tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[w].Value.Type))) ? true : (neighborTile[w].Value.lazyMergeId != 0xFF);
5774	                                            lazyCheckReady &= (neighborTile[s] == null || neighborTile[s].Value.IsActive == false || !tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[s].Value.Type))) ? true : (neighborTile[s].Value.lazyMergeId != 0xFF);
5775	                                            if (lazyCheckReady)
5776	                                            {
5777	                                                sameStyle &= 0x11111110 | ((neighborTile[e] == null || neighborTile[e].Value.IsActive == false || !tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[e].Value.Type))) ? 0x00000001 : ((neighborTile[e].Value.lazyMergeId & 0x04) >> 2));
5778	                                                sameStyle &= 0x11111101 | ((neighborTile[n] == null || neighborTile[n].Value.IsActive == false || !tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[n].Value.Type))) ? 0x00000010 : ((neighborTile[n].Value.lazyMergeId & 0x08) << 1));
5779	                                                sameStyle &= 0x11111011 | ((neighborTile[w] == null || neighborTile[w].Value.IsActive == false || !tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[w].Value.Type))) ? 0x00000100 : ((neighborTile[w].Value.lazyMergeId & 0x01) << 8));
5780	                                                sameStyle &= 0x11110111 | ((neighborTile[s] == null || neighborTile[s].Value.IsActive == false || !tileprop.Merges(WorldConfiguration.GetTileProperties(neighborTile[s].Value.Type))) ? 0x00001000 : ((neighborTile[s].Value.lazyMergeId & 0x02) << 11));
5781	                                                curtile.hasLazyChecked = true;
5782	                                            }
5783	                                        }
5784	                                        if (tileprop.MergeWith.HasValue && tileprop.MergeWith.Value > -1) //Merges with a specific type
5785	                                        {
5786	                                            mergeMask |= (neighborTile[e]?.IsActive == true && neighborTile[e].Value.Type == tileprop.MergeWith.Value) ? 0x0001 : 0x0000;
5787	                                            mergeMask |= (neighborTile[n]?.IsActive == true && neighborTile[n].Value.Type == tileprop.MergeWith.Value) ? 0x0010 : 0x0000;
5788	                                            mergeMask |= (neighborTile[w]?.IsActive == true && neighborTile[w].Value.Type == tileprop.MergeWith.Value) ? 0x0100 : 0x0000;
5789	                                            mergeMask |= (neighborTile[s]?.IsActive == true && neighborTile[s].Value.Type == tileprop.MergeWith.Value) ? 0x1000 : 0x0000;
5790	                                            mergeMask |= (neighborTile[ne]?.IsActive == true && neighborTile[ne].Value.Type == tileprop.MergeWith.Value) ? 0x00010000 : 0x00000000;
5791	                                            mergeMask |= (neighborTile[nw]?.IsActive == true && neighborTile[nw].Value.Type == tileprop.MergeWith.Value) ? 0x00100000 : 0x00000000;
5792	                                            mergeMask |= (neighborTile[sw]?.IsActive == true && neighborTile[sw].Value.Type == tileprop.MergeWith.Value) ? 0x01000000 : 0x00000000;
5793	                                            mergeMask |= (neighborTile[se]?.IsActive == true && neighborTile[se].Value.Type == tileprop.MergeWith.Value) ? 0x10000000 : 0x00000000;
5794	                                            strictness = 1;
5795	                                        }
5796	                                        if (tileprop.IsGrass)
5797	                                        {
5798	                                            strictness = 2;
5799	                                        }
5800	
5801	                                        int variant = TileFraming.DetermineFrameNumber(curtile.Type, x, y);
5802	                                        Vector2Int32 uvBlend = blendRules.GetUVForMasks((uint)sameStyle, (uint)mergeMask, strictness, variant);
5803	                                        curtile.uvTileCache = (ushort)((uvBlend.Y << 8) + uvBlend.X);
5804	                                        curtile.lazyMergeId = blendRules.lazyMergeValidation[uvBlend.Y, uvBlend.X];
5805	                                        } // end else (non-gemspark BlendRules path)
5806	                                    }
5807	
5808	                                    var texsize = new Vector2Int32(tileprop.TextureGrid.X, tileprop.TextureGrid.Y);
5809	                                    if (texsize.X == 0 || texsize.Y == 0)
5810	                                    {
5811	                                        texsize = new Vector2Int32(16, 16);
5812	                                    }
5813	                                    var source = new Rectangle((curtile.uvTileCache & 0x00FF) * (texsize.X + 2), (curtile.uvTileCache >> 8) * (texsize.Y + 2), texsize.X, texsize.Y);
5814	                                    var dest = new Rectangle(1 + (int)((_scrollPosition.X + x) * _zoom), 1 + (int)((_scrollPosition.Y + y) * _zoom), (int)_zoom, (int)_zoom);
5815	
5816	                                    // Render liquid behind tiles if adjacent tile has liquid
5817	                                    if (_wvm.ShowLiquid)
5818	                                    {
5819	                                        Tile? adjacentLiquidTile = null;
5820	                                        int adjacentX = x, adjacentY = y;
5821	
5822	                                        if (y > 0)
5823	                                        {
5824	                                            var aboveTile = _wvm.CurrentWorld.Tiles[x, y - 1];
5825	                                            if (aboveTile.LiquidAmount > 0)
5826	                                            {
5827	                                                adjacentLiquidTile = aboveTile;
5828	                                                adjacentY = y - 1;
5829	                                            }
5830	                                        }
5831	                                        // For horizontal liquid, render if one side has liquid AND other side has liquid or solid tile (not air/plants)
5832	                                        if (adjacentLiquidTile == null && x > 0 && x < _wvm.CurrentWorld.TilesWide - 1)
5833	                                        {
5834	                                            var leftTile = _wvm.CurrentWorld.Tiles[x - 1, y];
5835	                                            var rightTile = _wvm.CurrentWorld.Tiles[x + 1, y];
5836	                                            bool leftIsSolid = leftTile.IsActive && WorldConfiguration.GetTileProperties(leftTile.Type).IsSolid;
5837	                                            bool rightIsSolid = rightTile.IsActive && WorldConfiguration.GetTileProperties(rightTile.Type).IsSolid;
5838	                                            // Left has liquid, right has liquid or solid tile
5839	                                            if (leftTile.LiquidAmount > 0 && (rightTile.LiquidAmount > 0 || rightIsSolid))
5840	                                            {
5841	                                                adjacentLiquidTile = leftTile;
5842	                                                adjacentX = x - 1;
5843	                                            }
5844	                                            // Right has liquid, left has liquid or solid tile
5845	                                            else if (rightTile.LiquidAmount > 0 && (leftTile.LiquidAmount > 0 || leftIsSolid))
5846	                                            {
5847	                                                adjacentLiquidTile = rightTile;
5848	                                                adjacentX = x + 1;
5849	                                            }
5850	                                        }
5851	
5852	                                        if (adjacentLiquidTile != null)
5853	                                        {
5854	                                            Texture2D liquidTex = null;
5855	                                            var liquidColor = Color.White;
5856	                                            float alpha = 0.5f;
5857	
5858	                                            if (adjacentLiquidTile.Value.LiquidType == LiquidType.Lava)
5859	                                            {
5860	                                                liquidTex = (Texture2D)_textureDictionary.GetLiquid(1);
5861	                                                alpha = 0.85f;
5862	                                            }
5863	                                            else if (adjacentLiquidTile.Value.LiquidType == LiquidType.Honey)
5864	                                            {
5865	                                                liquidTex = (Texture2D)_textureDictionary.GetLiquid(11);
5866	                                            }
5867	                                            else if (adjacentLiquidTile.Value.LiquidType == LiquidType.Shimmer)
5868	                                            {
5869	                                                liquidTex = (Texture2D)_textureDictionary.GetLiquid(14);
5870	                                                liquidColor = new Color(WorldConfiguration.GlobalColors["Shimmer"].PackedValue);
5871	                                            }
5872	                                            else
5873	                                            {
5874	                                                liquidTex = (Texture2D)_textureDictionary.GetLiquid(0);
5875	                                            }
5876	
5877	                                            if (liquidTex != null)
5878	                                            {
5879	                                                // Use same texture as the adjacent tile would use for its own rendering
5880	                                                // Check if adjacent tile has liquid above IT (at adjacentX, adjacentY - 1)
5881	                                                var liquidSource = new Rectangle(0, 8, 16, 8); // Default to body
5882	                                                var liquidDest = dest;
5883	                                                bool adjacentHasLiquidAbove = adjacentY > 0 && _wvm.CurrentWorld.Tiles[adjacentX, adjacentY - 1].LiquidAmount > 0;
5884	
5885	                                                if (!adjacentHasLiquidAbove)
5886	                                                {
5887	                                                    // Adjacent liquid is at the top - use surface texture with variable height
5888	                                                    liquidSource.Y = 0;
5889	                                                    liquidSource.Height = 4 + ((int)Math.Round(adjacentLiquidTile.Value.LiquidAmount * 6f / 255f)) * 2;
5890	                                                    // Also adjust destination height and position like DrawTileLiquid does
5891	                                                    liquidDest.Height = (int)(liquidSource.Height * _zoom / 16f);
5892	                                                    liquidDest.Y = 1 + (int)((_scrollPosition.Y + y) * _zoom + ((16 - liquidSource.Height) * _zoom / 16f));
5893	                                                }
5894	                                                _spriteBatch.Draw(liquidTex, liquidDest, liquidSource, liquidColor * alpha, 0f, default, SpriteEffects.None, LayerTileSlopeLiquid);
5895	                                            }
5896	                                        }
5897	                                    }
5898	
5899	                                    // hack for some slopes
5900	                                    switch (curtile.BrickStyle)
5901	                                    {
5902	
5903	                                        case BrickStyle.HalfBrick:
5904	                                            source.Height /= 2;
5905	                                            dest.Y += (int)(_zoom * 0.5);
5906	                                            dest.Height = (int)(_zoom / 2.0f);
5907	                                            _spriteBatch.Draw(tileTex, dest, source, curtile.InActive ? Color.Gray : tilePaintColor, 0f, default, SpriteEffects.None, LayerTileTextures);
5908	                                            break;
5909	                                        case BrickStyle.SlopeTopRight:
5910	
5911	                                            for (int slice = 0; slice < 8; slice++)
5912	                                            {
5913	                                                Rectangle? sourceSlice = new Rectangle(source.X + slice * 2, source.Y, 2, 16 - slice * 2);
5914	                                                Vector2 destSlice = new Vector2(dest.X + slice * _zoom / 8.0f, dest.Y + slice * _zoom / 8.0f);
5915	
5916	                                                _spriteBatch.Draw(tileTex, destSlice, sourceSlice, curtile.InActive ? Color.Gray : tilePaintColor, 0f, default, _zoom / 16, SpriteEffects.None, LayerTileTextures);
5917	                                            }
5918	
5919	                                            break;
5920	                                        case BrickStyle.SlopeTopLeft:
5921	                                            for (int slice = 0; slice < 8; slice++)
5922	                                            {
5923	                                                Rectangle? sourceSlice = new Rectangle(source.X + slice * 2, source.Y, 2, slice * 2 + 2);
5924	                                                Vector2 destSlice = new Vector2(dest.X + slice * _zoom / 8.0f, dest.Y + (7 - slice) * _zoom / 8.0f);
5925	
5926	                                                _spriteBatch.Draw(tileTex, destSlice, sourceSlice, curtile.InActive ? Color.Gray : tilePaintColor, 0f, default, _zoom / 16, SpriteEffects.None, LayerTileTextures);
5927	                                            }
5928	
5929	                                            break;
5930	                                        case BrickStyle.SlopeBottomRight:
5931	                                            for (int slice = 0; slice < 8; slice++)
5932	                                            {
5933	                                                Rectangle? sourceSlice = new Rectangle(source.X + slice * 2, source.Y + slice * 2, 2, 16 - slice * 2);
5934	                                                Vector2 destSlice = new Vector2(dest.X + slice * _zoom / 8.0f, dest.Y);
5935	
5936	                                                _spriteBatch.Draw(tileTex, destSlice, sourceSlice, curtile.InActive ? Color.Gray : tilePaintColor, 0f, default, _zoom / 16, SpriteEffects.None, LayerTileTextures);
5937	                                            }
5938	
5939	                                            break;
5940	                                        case BrickStyle.SlopeBottomLeft:
5941	                                            for (int slice = 0; slice < 8; slice++)
5942	                                            {
5943	                                                Rectangle? sourceSlice = new Rectangle(source.X + slice * 2, source.Y, 2, slice * 2 + 2);
5944	                                                Vector2 destSlice = new Vector2(dest.X + slice * _zoom / 8.0f, dest.Y);
5945	
5946	                                                _spriteBatch.Draw(tileTex, destSlice, sourceSlice, curtile.InActive ? Color.Gray : tilePaintColor, 0f, default, _zoom / 16, SpriteEffects.None, LayerTileTextures);
5947	                                            }
5948	
5949	                                            break;
5950	                                        case BrickStyle.Full:
5951	                                        default:
5952	                                            _spriteBatch.Draw(tileTex, dest, source, curtile.InActive ? Color.Gray : tilePaintColor, 0f, default, SpriteEffects.None, LayerTileTextures);
5953	                                            break;
5954	                                    }
5955	
5956	
5957	                                    // Actuator Overlay — always draw at standard tile size, not the (possibly modified) dest
5958	                                    if (curtile.Actuator && _wvm.ShowActuators)
5959	                                    {
5960	                                        var actuatorDest = new Rectangle(1 + (int)((_scrollPosition.X + x) * _zoom), 1 + (int)((_scrollPosition.Y + y) * _zoom), (int)_zoom, (int)_zoom);
5961	                                        _spriteBatch.Draw(_textureDictionary.Actuator, actuatorDest, _textureDictionary.ZeroSixteenRectangle, Color.White, 0f, default, SpriteEffects.None, LayerTileActuator);
5962	                                    }
5963	
5964	                                }
5965	                            }
5966	                        }
5967	                    }
5968	                }
5969	                catch (Exception)
5970	                {
5971	                    // failed to render tile? log?
5972	                }
5973	            }
5974	        }
5975	    }
5976	
5977	    /// <summary>
5978	    /// Draws additive glow mask overlays for tiles that have them (meteorite, moss, shimmer, etc.).
5979	    /// Must be called within a SpriteBatch.Begin/End pair using AdditiveGlowBlend.
5980	    /// </summary>
5981	    private void DrawTileGlowMasks()
5982	    {
5983	        Rectangle visibleBounds = GetViewingArea();
5984	        var width = _wvm.CurrentWorld.TilesWide;
5985	        var height = _wvm.CurrentWorld.TilesHigh;
5986	
5987	        for (int y = visibleBounds.Top - 1; y < visibleBounds.Bottom + 2; y++)
5988	        {
5989	            for (int x = visibleBounds.Left - 1; x < visibleBounds.Right + 2; x++)
5990	            {
5991	                try
5992	                {
5993	                    if (x < 0 || y < 0 || x >= width || y >= height) continue;
5994	
5995	                    var curtile = _wvm.CurrentWorld.Tiles[x, y];
5996	                    if (!curtile.IsActive) continue;
5997	
5998	                    // Echo coating (invisible block) — skip unless coatings are visible
5999	                    if (curtile.InvisibleBlock && !_wvm.ShowCoatings) continue;
6000	
6001	                    // Shadow paint suppresses glow
6002	                    if (curtile.TileColor == 29) continue;
6003	
6004	                    // Negative paint — skip glow (undefined visual)
6005	                    if (curtile.TileColor == 30) continue;
6006	
6007	                    // Actuated/inactive tiles — suppress glow
6008	                    if (curtile.InActive) continue;
6009	

```


---

## 🤖 Assistant · 2026-08-07T07:04:55.636Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I need:
- TileProperty.Merges full body (lines ~120-180).
- The blendRules.GetUVForMasks with strictness (grass strictness=2) — need to find the BlendRules class and how strictness 2 selects merge rows (the 110 rows in Tiles_2).
- Grass-specific rule table. Let me find blendRules class.
- Also the TileProperty JSON: where MergeWith for grass is defined (settings files) — probably in the TEdit settings JSON (tiles.json) with "MergeWith": 0 for grasses. Let me check.
- Also line 300-360 switch for grass in renderer (probably tree/grass rendering for vines?) Let me check lines 130-145 and 300-360.

Also vanilla part: I need to report the important finding that Framing.cs is a partial decompile (407 lines) without AddFrame/FrameNearTile/grass. But I should check whether WorldGen has the framing cascade — search WorldGen for "SquareTileFrame" or similar. And check how vanilla frames blocks: SelfFrame8Way is only for gemsparks. Standard blocks (dirt/stone) in vanilla frame via Framing's... hmm, in actual vanilla, standard blocks use `Framing.blockFrame`? Actually in vanilla, solid blocks frame in Framing.cs's big switch? No — vanilla: solid blocks don't use SelfFrame8Way; they use the tile sheet arrangement where each tile type has its own 2x2 frame set per tile type, computed by... Actually vanilla: for normal solid tiles, framing is done by `Framing` main method that iterates: it computes `num5` etc.? Let me recall vanilla 1.4 Framing.cs — it has:
- public static void Initialize()
- private static Framing.BlockStyle FindBlockStyle
- public static void Add8WayLookup
- public static void AddWallFrameLookup
- private static bool WillItBlend
- public static void SelfFrame8Way
- public static void WallFrame
- public static void GetTileSafely
- public static void FrameTreeLeaves / etc? Hmm.

Actually I recall vanilla Framing.cs DOES contain AddFrame, FrameNearTile, and tile-specific frames (frameing for tiles like torches, trees, etc. is in WorldGen and TileDrawing). Let me recall the actual vanilla file... In tModPorter-era decompiles (1.4.4), Framing.cs is ~4600 lines and includes:
- AddFrame(int i, int j)
- FrameNearTile? Hmm, I'm not 100% sure. I believe there is `Framing.AddFrame`, `Framing.Wiring`, `Framing.TileFrame`... Hmm.

Actually I do recall vanilla 1.4 Framing.cs has: `public static void AddFrame(int i, int j)`, `public static void FrameAroundThisTile`? Not sure. There IS `Framing.Wiring(int i, int j, Tile curr)` — no, that's WorldGen?

The key question: does the partial decompile at Terarria1405 contain AddFrame? Grep found nothing ("void AddFrame" empty). Let me verify with a broader grep for "AddFrame" in the whole repo. Also grep "FrameTile" and "SquareTileFrame". And how solid blocks frame in vanilla — that's actually done by Framing in the big per-tile switch? No — for standard solid blocks, vanilla computes frame via... Let me think about vanilla TileDrawing: for normal tiles it uses `Main.tileFrame[type]` positions: `tileFrameX = frameX`, and variants chosen via `frameNumber`. Framing for solid blocks in vanilla happens in `WorldGen.TileFrame`? Actually the classic function is `WorldGen.TileFrame(int i, int j, bool resetFrame)` — yes! In vanilla, per-tile framing logic (including grass merging, dirt, etc.) is in WorldGen.TileFrame, a huge method. And Framing.AddFrame/FrameNearTile... Hmm.

Let me actually check: In Terraria 1.4 source (e.g., ILSpy decompiles on GitHub), Framing.cs contains:
- Initialize, FindBlockStyle, Add8WayLookup, AddWallFrameLookup, WillItBlend, SelfFrame8Way, WallFrame, GetTileSafely, BlockStyle struct... and ALSO at the end:
- `public static void AddFrame(int i, int j)` — I'm fairly confident this exists in Framing.cs in later versions (1.4.4) which calls FrameNearTile etc. Hmm, 1.4.0.5?

Let me just check the local repo: grep "AddFrame", "TileFrame", "SquareTileFrame" in WorldGen.cs and check WorldGen.TileFrame presence and grass handling there. WorldGen.cs is 54,961 lines — likely a full decompile. Let me grep.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:04:56.628Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && grep -rn \"AddFrame\\|FrameNearTile\" --include=\"*.cs\" . | head; echo \"=== WorldGen framing methods ===\"; grep -n \"public static void TileFrame\\|public static bool TileFrame\\|static void SquareTileFrame\\|SlopeTile\\|public static void FrameTile\" WorldGen.cs | head -20",
 "description": "Search framing cascade in vanilla WorldGen"
}
```


---

## 🤖 Assistant · 2026-08-07T07:04:56.652Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && grep -n \"tileMergeDirt\\|MergesWithTile\\|tileBrick\\[\" Main.cs | head -20; echo \"=== TileID Sets for grass ===\"; grep -n \"Grass\\|ForcedDirtMerging\\|GemsparkFramingTypes\" ID/TileID.cs | head -30",
 "description": "Check merge-related data in Main.cs and TileID"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:04:56.711Z

**📎 ToolResult**

```
440:    public static bool[] tileMergeDirt = new bool[623];
5240:      Main.tileBrick[477] = true;
5243:      Main.tileBrick[492] = true;
5246:      Main.tileBrick[1] = true;
5247:      Main.tileBrick[54] = true;
5248:      Main.tileBrick[118] = true;
5249:      Main.tileBrick[119] = true;
5250:      Main.tileBrick[120] = true;
5251:      Main.tileBrick[121] = true;
5252:      Main.tileBrick[122] = true;
5253:      Main.tileBrick[140] = true;
5254:      Main.tileBrick[148] = true;
5255:      Main.tileBrick[150] = true;
5256:      Main.tileBrick[151] = true;
5257:      Main.tileBrick[152] = true;
5258:      Main.tileBrick[30] = true;
5259:      Main.tileBrick[38] = true;
5260:      Main.tileBrick[39] = true;
5261:      Main.tileBrick[41] = true;
5262:      Main.tileBrick[43] = true;
=== TileID Sets for grass ===
16:    public const ushort Grass = 2;
37:    public const ushort CorruptGrass = 23;
74:    public const ushort JungleGrass = 60;
84:    public const ushort MushroomGrass = 70;
123:    public const ushort HallowedGrass = 109;
213:    public const ushort CrimsonGrass = 199;
353:    public const ushort GrasshopperCage = 339;
376:    public const ushort GoldGrasshopperCage = 362;
491:    public const ushort GolfGrass = 477;
506:    public const ushort GolfGrassHallowed = 492;
654:      public static bool[] ForcedDirtMerging = TileID.Sets.Factory.CreateBoolSet(75, 76, 508, 507, 226, 409, 273, 274, 459, 458, 326, 327, 345, 328, 329, 192, 384, 284, 325, 272, 268, 262, 267, 265, 266, 264, 263, 54);
676:      public static ushort[] GemsparkFramingTypes = TileID.Sets.Factory.CreateUshortSet((ushort) 0, (ushort) 265, (ushort) 265, (ushort) 258, (ushort) 258, (ushort) 264, (ushort) 264, (ushort) 257, (ushort) 257, (ushort) 267, (ushort) 267, (ushort) 260, (ushort) 260, (ushort) 266, (ushort) 266, (ushort) 259, (ushort) 259, (ushort) 263, (ushort) 263, (ushort) 256, (ushort) 256, (ushort) 262, (ushort) 262, (ushort) byte.MaxValue, (ushort) byte.MaxValue, (ushort) 268, (ushort) 268, (ushort) 261, (ushort) 261, (ushort) 385, (ushort) 385, (ushort) 446, (ushort) 446, (ushort) 447, (ushort) 447, (ushort) 448, (ushort) 448);
693:      public static bool[] GrassSpecial = TileID.Sets.Factory.CreateBoolSet(70, 60);
712:      public static bool[] NeedsGrassFraming = TileID.Sets.Factory.CreateBoolSet();
713:      public static int[] NeedsGrassFramingDirt = TileID.Sets.Factory.CreateIntSet(0);
738:        public static bool[] Grass = TileID.Sets.Factory.CreateBoolSet(2, 23, 60, 199, 109, 477, 492);
739:        public static bool[] GolfGrass = TileID.Sets.Factory.CreateBoolSet(477, 492);

```


---

## 👤 User(sidechain) · 2026-08-07T07:04:56.733Z

**📎 ToolResult**

```
=== WorldGen framing methods ===
7587:                          WorldGen.SlopeTile(index1, index2, 2, false);
7594:                          WorldGen.SlopeTile(index1, index2, 1, false);
7613:                            WorldGen.SlopeTile(index1, index2, 2, false);
7622:                            WorldGen.SlopeTile(index1, index2, 1, false);
7639:                      WorldGen.SlopeTile(index1, index2, 2, false);
7650:                      WorldGen.SlopeTile(index1, index2, 1, false);
7659:                  WorldGen.SlopeTile(index1, index2, 3, false);
7661:                  WorldGen.SlopeTile(index1, index2, 4, false);
7675:                WorldGen.SlopeTile(i, j, 2, false);
7677:                WorldGen.SlopeTile(i, j, 1, false);
7681:              WorldGen.SlopeTile(i, j, 0, false);
7686:              WorldGen.SlopeTile(i, j, 0, false);
48855:    public static void SquareTileFrame(int i, int j, bool resetFrame = true)
49170:    public static bool SlopeTile(int i, int j, int slope = 0, bool noEffects = false)
49247:          WorldGen.SlopeTile(x, y, slope1, false);
49255:          WorldGen.SlopeTile(x, y, slope2, false);
49263:          WorldGen.SlopeTile(x, y, 0, false);
49639:    public static void TileFrame(int i, int j, bool resetFrame = false, bool noBreak = false)

```


---

## 🤖 Assistant · 2026-08-07T07:05:01.509Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. So the vanilla decompile has:
- Framing.cs (407 lines, lookup-based only)
- WorldGen.SquareTileFrame (line 48855) — the re-frame cascade
- WorldGen.TileFrame (line 49639) — the giant per-tile framing switch (grass handling lives here!)

The caller's assumption that grass framing is in Framing.cs is wrong for this decompile — grass framing is in WorldGen.TileFrame. Let me examine:
1. WorldGen.TileFrame beginning and the grass branch (search "tileMergeDirt" and type==2 / case 2 within TileFrame).
2. WorldGen.SquareTileFrame (cascade).
3. Where does solid block framing happen in vanilla TileFrame? The general case at the end of TileFrame — frameX/frameY computed from neighbor mask using `Main.tileFrame` sheet: it computes a "num" from 8 neighbors then maps via a formula. Let me read TileFrame.

TileFrame is huge (49639 → maybe until ~53000). Let me grep within it for grass-specific handling.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:05:01.512Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && sed -n '48855,48930p' WorldGen.cs",
 "description": "Read SquareTileFrame cascade"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:05:01.557Z

**📎 ToolResult**

```
    public static void SquareTileFrame(int i, int j, bool resetFrame = true)
    {
      WorldGen.TileFrame(i - 1, j - 1, false, false);
      WorldGen.TileFrame(i - 1, j, false, false);
      WorldGen.TileFrame(i - 1, j + 1, false, false);
      WorldGen.TileFrame(i, j - 1, false, false);
      WorldGen.TileFrame(i, j, resetFrame, false);
      WorldGen.TileFrame(i, j + 1, false, false);
      WorldGen.TileFrame(i + 1, j - 1, false, false);
      WorldGen.TileFrame(i + 1, j, false, false);
      WorldGen.TileFrame(i + 1, j + 1, false, false);
    }

    public static void SquareWallFrame(int i, int j, bool resetFrame = true)
    {
      Framing.WallFrame(i - 1, j - 1, false);
      Framing.WallFrame(i - 1, j, false);
      Framing.WallFrame(i - 1, j + 1, false);
      Framing.WallFrame(i, j - 1, false);
      Framing.WallFrame(i, j, resetFrame);
      Framing.WallFrame(i, j + 1, false);
      Framing.WallFrame(i + 1, j - 1, false);
      Framing.WallFrame(i + 1, j, false);
      Framing.WallFrame(i + 1, j + 1, false);
    }

    public static void SectionTileFrameWithCheck(int startX, int startY, int endX, int endY)
    {
      int sectionX1 = Netplay.GetSectionX(startX);
      int sectionY1 = Netplay.GetSectionY(startY);
      int sectionX2 = Netplay.GetSectionX(endX);
      int sectionY2 = Netplay.GetSectionY(endY);
      for (int index1 = sectionX1; index1 <= sectionX2; ++index1)
      {
        for (int index2 = sectionY1; index2 <= sectionY2; ++index2)
        {
          if (Main.sectionManager.SectionLoaded(index1, index2) && !Main.sectionManager.SectionFramed(index1, index2))
          {
            WorldGen.SectionTileFrame(index1, index2, index1, index2);
            if (Main.sectionManager.FrameSectionsLeft == 0)
              return;
          }
        }
      }
    }

    public static void SectionTileFrame(int startX, int startY, int endX, int endY)
    {
      Main.mapTime = Main.mapTimeMax + 10;
      WorldGen.noMapUpdate = true;
      int num1 = startX * 200;
      int num2 = (endX + 1) * 200;
      int num3 = startY * 150;
      int num4 = (endY + 1) * 150;
      if (num1 < 1)
        num1 = 1;
      if (num3 < 1)
        num3 = 1;
      if (num1 > Main.maxTilesX - 2)
        num1 = Main.maxTilesX - 2;
      if (num3 > Main.maxTilesY - 2)
        num3 = Main.maxTilesY - 2;
      if (num2 > Main.maxTilesX - 2)
        num2 = Main.maxTilesX - 2;
      if (num4 > Main.maxTilesY - 2)
        num4 = Main.maxTilesY - 2;
      for (int i = num1 - 1; i < num2 + 1; ++i)
      {
        for (int j = num3 - 1; j < num4 + 1; ++j)
        {
          if (Main.tile[i, j] == null)
            Main.tile[i, j] = new Tile();
          WorldGen.TileFrame(i, j, true, true);
          Framing.WallFrame(i, j, true);
        }
      }

```


---

## 🤖 Assistant · 2026-08-07T07:05:01.665Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && awk 'NR>=49639 && NR<=49639+50' WorldGen.cs; echo \"...\"; grep -n \"tileMergeDirt\" WorldGen.cs | head -20",
 "description": "Read TileFrame start and tileMergeDirt usages"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:05:06.995Z

**📎 ToolResult**

```
    public static void TileFrame(int i, int j, bool resetFrame = false, bool noBreak = false)
    {
      bool addToList = false;
      try
      {
        if (i > 5)
        {
          if (j > 5)
          {
            if (i < Main.maxTilesX - 5)
            {
              if (j < Main.maxTilesY - 5)
              {
                if (Main.tile[i, j] != null)
                {
                  if (WorldGen.SkipFramingBecauseOfGen && !Main.tileFrameImportant[(int) Main.tile[i, j].type])
                    return;
                  addToList = WorldGen.UpdateMapTile(i, j, true);
                  Tile tile1 = Main.tile[i, j];
                  if (!tile1.active())
                  {
                    tile1.halfBrick(false);
                    tile1.color((byte) 0);
                    tile1.slope((byte) 0);
                  }
                  if (tile1.liquid > (byte) 0 && Main.netMode != 1 && !WorldGen.noLiquidCheck)
                    Liquid.AddWater(i, j);
                  if (tile1.active())
                  {
                    if (noBreak && Main.tileFrameImportant[(int) tile1.type] && tile1.type != (ushort) 4)
                      return;
                    int index1 = (int) tile1.type;
                    if (Main.tileStone[index1])
                      index1 = 1;
                    int frameX = (int) tile1.frameX;
                    int frameY = (int) tile1.frameY;
                    Microsoft.Xna.Framework.Rectangle rectangle = new Microsoft.Xna.Framework.Rectangle(-1, -1, 0, 0);
                    if (Main.tileFrameImportant[(int) tile1.type])
                    {
                      switch (index1)
                      {
                        case 4:
                          WorldGen.CheckTorch(i, j);
                          return;
                        case 136:
                          Tile tile2 = Main.tile[i, j - 1];
                          Tile tile3 = Main.tile[i, j + 1];
                          Tile tile4 = Main.tile[i - 1, j];
                          Tile tile5 = Main.tile[i + 1, j];
                          Tile tile6 = Main.tile[i - 1, j + 1];
                          Tile tile7 = Main.tile[i + 1, j + 1];
...
50638:                          if (up > -1 && Main.tileMergeDirt[up])
50650:                          if (down > -1 && Main.tileMergeDirt[down])
50662:                          if (left > -1 && Main.tileMergeDirt[left])
50674:                          if (right > -1 && Main.tileMergeDirt[right])
50695:                          if (upLeft > -1 && Main.tileMergeDirt[upLeft])
50699:                          if (upRight > -1 && Main.tileMergeDirt[upRight])
50703:                          if (downLeft > -1 && Main.tileMergeDirt[downLeft])
50707:                          if (downRight > -1 && Main.tileMergeDirt[downRight])
50767:                      if (Main.tileMergeDirt[index1])
52189:                      if (rectangle.X == -1 && rectangle.Y == -1 && (Main.tileMergeDirt[index1] || index1 > -1 && TileID.Sets.ChecksForMerge[index1]))

```


---

## 🤖 Assistant · 2026-08-07T07:05:10.404Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read TileFrame's general (non-frameImportant) block framing section — around 50600-50800 (the 8-way mask with tileMergeDirt) and 52150-52260 (where frameX/frameY are computed for merge tiles). Also find the grass-specific branch — grass (type 2) is handled where? Grass merges with dirt: In vanilla, when grass is adjacent to dirt, grass uses special frames from its sheet (Tiles_2 has extra rows). Let me search TileFrame for "23" special? Actually grass handling: `if (Main.tileMergeDirt[index1])` at 50767 — grass has tileMergeDirt[2]=true, meaning grass merges INTO dirt? Let me read 50580-50830.

Also the final framing computation: around 52189+. Let me read that region.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:05:10.561Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && sed -n '50580,50800p' WorldGen.cs",
 "description": "Read TileFrame merge-mask section"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:05:10.603Z

**📎 ToolResult**

```
                        num4 = (int) tile1.frameNumber();
                      if (Main.tileLargeFrames[index1] == (byte) 1)
                        num4 = new int[4, 3]
                        {
                          {
                            2,
                            4,
                            2
                          },
                          {
                            1,
                            3,
                            1
                          },
                          {
                            2,
                            2,
                            4
                          },
                          {
                            1,
                            1,
                            3
                          }
                        }[j % 4, i % 3] - 1;
                      if (Main.tileLargeFrames[index1] == (byte) 2)
                        num4 = i % 2 + j % 2 * 2;
                      WorldGen.TileMergeAttempt(index1, Main.tileBlendAll, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                      if (Main.tileBlendAll[index1])
                      {
                        Main.tileSolid[10] = false;
                        Main.tileSolid[387] = false;
                        WorldGen.TileMergeAttempt(index1, Main.tileSolid, Main.tileSolidTop, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                        Main.tileSolid[10] = true;
                        Main.tileSolid[387] = true;
                      }
                      if (TileID.Sets.ForcedDirtMerging[index1])
                      {
                        if (up == 0)
                          up = index1;
                        if (down == 0)
                          down = index1;
                        if (left == 0)
                          left = index1;
                        if (right == 0)
                          right = index1;
                        if (upLeft == 0)
                          upLeft = index1;
                        if (upRight == 0)
                          upRight = index1;
                        if (downLeft == 0)
                          downLeft = index1;
                        if (downRight == 0)
                          downRight = index1;
                      }
                      switch (index1)
                      {
                        case 0:
                          if (up > -1 && Main.tileMergeDirt[up])
                          {
                            WorldGen.TileFrame(i, j - 1, false, false);
                            if (WorldGen.mergeDown)
                              up = index1;
                          }
                          else if (up == 147)
                          {
                            WorldGen.TileFrame(i, j - 1, false, false);
                            if (WorldGen.mergeDown)
                              up = index1;
                          }
                          if (down > -1 && Main.tileMergeDirt[down])
                          {
                            WorldGen.TileFrame(i, j + 1, false, false);
                            if (WorldGen.mergeUp)
                              down = index1;
                          }
                          else if (down == 147)
                          {
                            WorldGen.TileFrame(i, j + 1, false, false);
                            if (WorldGen.mergeUp)
                              down = index1;
                          }
                          if (left > -1 && Main.tileMergeDirt[left])
                          {
                            WorldGen.TileFrame(i - 1, j, false, false);
                            if (WorldGen.mergeRight)
                              left = index1;
                          }
                          else if (left == 147)
                          {
                            WorldGen.TileFrame(i - 1, j, false, false);
                            if (WorldGen.mergeRight)
                              left = index1;
                          }
                          if (right > -1 && Main.tileMergeDirt[right])
                          {
                            WorldGen.TileFrame(i + 1, j, false, false);
                            if (WorldGen.mergeLeft)
                              right = index1;
                          }
                          else if (right == 147)
                          {
                            WorldGen.TileFrame(i + 1, j, false, false);
                            if (WorldGen.mergeLeft)
                              right = index1;
                          }
                          bool[] dirtInAspecialWay = TileID.Sets.Conversion.MergesWithDirtInASpecialWay;
                          if (up > -1 && dirtInAspecialWay[up])
                            up = index1;
                          if (down > -1 && dirtInAspecialWay[down])
                            down = index1;
                          if (left > -1 && dirtInAspecialWay[left])
                            left = index1;
                          if (right > -1 && dirtInAspecialWay[right])
                            right = index1;
                          if (upLeft > -1 && Main.tileMergeDirt[upLeft])
                            upLeft = index1;
                          else if (upLeft > -1 && dirtInAspecialWay[upLeft])
                            upLeft = index1;
                          if (upRight > -1 && Main.tileMergeDirt[upRight])
                            upRight = index1;
                          else if (upRight > -1 && dirtInAspecialWay[upRight])
                            upRight = index1;
                          if (downLeft > -1 && Main.tileMergeDirt[downLeft])
                            downLeft = index1;
                          else if (downLeft > -1 && dirtInAspecialWay[downLeft])
                            downLeft = index1;
                          if (downRight > -1 && Main.tileMergeDirt[downRight])
                            downRight = index1;
                          else if (downRight > -1 && dirtInAspecialWay[downRight])
                            downRight = index1;
                          WorldGen.TileMergeAttempt(-2, 59, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                          WorldGen.TileMergeAttempt(index1, 191, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                          if (up > -1 && TileID.Sets.ForcedDirtMerging[up])
                            up = index1;
                          if (down > -1 && TileID.Sets.ForcedDirtMerging[down])
                            down = index1;
                          if (left > -1 && TileID.Sets.ForcedDirtMerging[left])
                            left = index1;
                          if (right > -1 && TileID.Sets.ForcedDirtMerging[right])
                            right = index1;
                          if (upLeft > -1 && TileID.Sets.ForcedDirtMerging[upLeft])
                            upLeft = index1;
                          if (upRight > -1 && TileID.Sets.ForcedDirtMerging[upRight])
                            upRight = index1;
                          if (downLeft > -1 && TileID.Sets.ForcedDirtMerging[downLeft])
                            downLeft = index1;
                          if (downRight > -1 && TileID.Sets.ForcedDirtMerging[downRight])
                          {
                            downRight = index1;
                            break;
                          }
                          break;
                        case 53:
                          WorldGen.TileMergeAttemptFrametest(i, j, index1, 397, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                          WorldGen.TileMergeAttemptFrametest(i, j, index1, 396, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                          break;
                        case 112:
                          WorldGen.TileMergeAttemptFrametest(i, j, index1, 398, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                          WorldGen.TileMergeAttemptFrametest(i, j, index1, 400, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                          break;
                        case 116:
                          WorldGen.TileMergeAttemptFrametest(i, j, index1, 402, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                          WorldGen.TileMergeAttemptFrametest(i, j, index1, 403, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                          break;
                        case 213:
                          if (up > -1 && Main.tileSolid[up] && !Main.tileSolidTop[up])
                            up = index1;
                          if (down > -1 && Main.tileSolid[down])
                            down = index1;
                          if (up != index1)
                          {
                            if (left > -1 && Main.tileSolid[left])
                              left = index1;
                            if (right > -1 && Main.tileSolid[right])
                            {
                              right = index1;
                              break;
                            }
                            break;
                          }
                          break;
                        case 234:
                          WorldGen.TileMergeAttemptFrametest(i, j, index1, 399, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                          WorldGen.TileMergeAttemptFrametest(i, j, index1, 401, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                          break;
                      }
                      if (Main.tileMergeDirt[index1])
                      {
                        WorldGen.TileMergeAttempt(-2, 0, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                        if (index1 == 1)
                        {
                          if ((double) j > Main.rockLayer)
                            WorldGen.TileMergeAttemptFrametest(i, j, index1, 59, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                          WorldGen.TileMergeAttemptFrametest(i, j, index1, 57, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                        }
                      }
                      else if (index1 == 58 || index1 == 76 || index1 == 75)
                      {
                        WorldGen.TileMergeAttempt(-2, 57, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                      }
                      else
                      {
                        switch (index1)
                        {
                          case 57:
                            WorldGen.TileMergeAttempt(-2, 1, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                            WorldGen.TileMergeAttemptFrametest(i, j, index1, TileID.Sets.HellSpecial, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                            break;
                          case 59:
                            if ((double) j > Main.rockLayer)
                              WorldGen.TileMergeAttempt(-2, 1, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                            WorldGen.TileMergeAttempt(index1, TileID.Sets.GrassSpecial, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                            WorldGen.TileMergeAttemptFrametest(i, j, index1, TileID.Sets.JungleSpecial, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                            if ((double) j < Main.rockLayer)
                            {
                              WorldGen.TileMergeAttemptFrametest(i, j, index1, 0, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                              break;
                            }
                            WorldGen.TileMergeAttempt(index1, 0, ref up, ref down, ref left, ref right);
                            break;

```


---

## 🤖 Assistant · 2026-08-07T07:05:18.106Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This is the key vanilla logic. Note `case 0:` = dirt. Grass (tile 2) has tileMergeDirt[2] = true, so grass goes into `if (Main.tileMergeDirt[index1]) { TileMergeAttempt(-2, 0, ...) }` — meaning grass merges with dirt (type 0).

Wait — but the caller said grass is framed specially. Actually in vanilla: grass is `Main.tileMergeDirt[2] = true`, and grass tiles use the standard framing, but the DIRT side: when dirt (index1==0) has grass neighbors (tileMergeDirt[up] == true since grass has tileMergeDirt set), dirt calls TileFrame on the neighbor and checks WorldGen.mergeUp/mergeDown flags — this is the mutual merge handshake where grass tells dirt "I can merge into you" and dirt sets its neighbor var to 0 (dirt) so dirt draws a merge frame.

Then there's TileMergeAttempt / TileMergeAttemptFrametest which set WorldGen.mergeUp etc. Let me find those methods and the "GrassSpecial" sets. Also need the final frame computation after the mask — around line 52189+ where frameX/frameY computed. Let me read 52100-52320.

Also find where the mask (up/down/left/right as -1/0/type) converts to frame numbers. Let me read.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:05:18.710Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && sed -n '52150,52330p' WorldGen.cs",
 "description": "Read final frame computation in TileFrame"
}
```


---

## 🤖 Assistant · 2026-08-07T07:05:18.727Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && grep -n \"static void TileMergeAttempt\\|static void TileMergeAttemptFrametest\\|mergeUp\\s*=\\|public static bool mergeUp\" WorldGen.cs | head -20",
 "description": "Find TileMergeAttempt definitions"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:05:18.771Z

**📎 ToolResult**

```
49330:    public static void TileMergeAttemptFrametest(
49379:    public static void TileMergeAttemptFrametest(
49428:    public static void TileMergeAttempt(
49447:    public static void TileMergeAttempt(
49478:    public static void TileMergeAttempt(
49509:    public static void TileMergeAttempt(
49541:    public static void TileMergeAttemptWeird(
50569:                      WorldGen.mergeUp = false;
52223:                            WorldGen.mergeUp = true;
52299:                            WorldGen.mergeUp = true;
52319:                            WorldGen.mergeUp = true;
52399:                            WorldGen.mergeUp = true;
52419:                            WorldGen.mergeUp = true;
52461:                            WorldGen.mergeUp = true;
52482:                            WorldGen.mergeUp = true;
52503:                            WorldGen.mergeUp = true;
52624:                              WorldGen.mergeUp = true;
52684:                              WorldGen.mergeUp = true;
52725:                              WorldGen.mergeUp = true;
52848:                              WorldGen.mergeUp = true;

```


---

## 👤 User(sidechain) · 2026-08-07T07:05:18.781Z

**📎 ToolResult**

```
                          {
                            switch (num4)
                            {
                              case 0:
                                rectangle.X = 108;
                                rectangle.Y = 198;
                                break;
                              case 1:
                                rectangle.X = 126;
                                rectangle.Y = 198;
                                break;
                              default:
                                rectangle.X = 144;
                                rectangle.Y = 198;
                                break;
                            }
                          }
                          else
                          {
                            switch (num4)
                            {
                              case 0:
                                rectangle.X = 18;
                                rectangle.Y = 18;
                                break;
                              case 1:
                                rectangle.X = 36;
                                rectangle.Y = 18;
                                break;
                              default:
                                rectangle.X = 54;
                                rectangle.Y = 18;
                                break;
                            }
                          }
                        }
                        WorldGen.TileMergeAttempt(-2, num5, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                      }
                      WorldGen.TileMergeAttempt(index1, Main.tileMerge[index1], ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                      if (rectangle.X == -1 && rectangle.Y == -1 && (Main.tileMergeDirt[index1] || index1 > -1 && TileID.Sets.ChecksForMerge[index1]))
                      {
                        if (!flag1)
                        {
                          flag1 = true;
                          WorldGen.TileMergeAttemptWeird(index1, -1, Main.tileSolid, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                        }
                        if (up > -1 && up != index1)
                          up = -1;
                        if (down > -1 && down != index1)
                          down = -1;
                        if (left > -1 && left != index1)
                          left = -1;
                        if (right > -1 && right != index1)
                          right = -1;
                        if (up != -1 && down != -1 && (left != -1 && right != -1))
                        {
                          if (up == -2 && down == index1 && (left == index1 && right == index1))
                          {
                            switch (num4)
                            {
                              case 0:
                                rectangle.X = 144;
                                rectangle.Y = 108;
                                break;
                              case 1:
                                rectangle.X = 162;
                                rectangle.Y = 108;
                                break;
                              default:
                                rectangle.X = 180;
                                rectangle.Y = 108;
                                break;
                            }
                            WorldGen.mergeUp = true;
                          }
                          else if (up == index1 && down == -2 && (left == index1 && right == index1))
                          {
                            switch (num4)
                            {
                              case 0:
                                rectangle.X = 144;
                                rectangle.Y = 90;
                                break;
                              case 1:
                                rectangle.X = 162;
                                rectangle.Y = 90;
                                break;
                              default:
                                rectangle.X = 180;
                                rectangle.Y = 90;
                                break;
                            }
                            WorldGen.mergeDown = true;
                          }
                          else if (up == index1 && down == index1 && (left == -2 && right == index1))
                          {
                            switch (num4)
                            {
                              case 0:
                                rectangle.X = 162;
                                rectangle.Y = 126;
                                break;
                              case 1:
                                rectangle.X = 162;
                                rectangle.Y = 144;
                                break;
                              default:
                                rectangle.X = 162;
                                rectangle.Y = 162;
                                break;
                            }
                            WorldGen.mergeLeft = true;
                          }
                          else if (up == index1 && down == index1 && (left == index1 && right == -2))
                          {
                            switch (num4)
                            {
                              case 0:
                                rectangle.X = 144;
                                rectangle.Y = 126;
                                break;
                              case 1:
                                rectangle.X = 144;
                                rectangle.Y = 144;
                                break;
                              default:
                                rectangle.X = 144;
                                rectangle.Y = 162;
                                break;
                            }
                            WorldGen.mergeRight = true;
                          }
                          else if (up == -2 && down == index1 && (left == -2 && right == index1))
                          {
                            switch (num4)
                            {
                              case 0:
                                rectangle.X = 36;
                                rectangle.Y = 90;
                                break;
                              case 1:
                                rectangle.X = 36;
                                rectangle.Y = 126;
                                break;
                              default:
                                rectangle.X = 36;
                                rectangle.Y = 162;
                                break;
                            }
                            WorldGen.mergeUp = true;
                            WorldGen.mergeLeft = true;
                          }
                          else if (up == -2 && down == index1 && (left == index1 && right == -2))
                          {
                            switch (num4)
                            {
                              case 0:
                                rectangle.X = 54;
                                rectangle.Y = 90;
                                break;
                              case 1:
                                rectangle.X = 54;
                                rectangle.Y = 126;
                                break;
                              default:
                                rectangle.X = 54;
                                rectangle.Y = 162;
                                break;
                            }
                            WorldGen.mergeUp = true;
                            WorldGen.mergeRight = true;
                          }
                          else if (up == index1 && down == -2 && (left == -2 && right == index1))
                          {
                            switch (num4)
                            {
                              case 0:
                                rectangle.X = 36;
                                rectangle.Y = 108;
                                break;
                              case 1:

```


---

## 🤖 Assistant · 2026-08-07T07:05:29.885Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I need:
- TileMergeAttempt methods (49330-49560) — the merge handshake.
- The merge flags reset at 50569.
- The general (non-merge) framing for standard blocks: where frameX/frameY is computed for non-merge tiles (the "normal" path after the merge block). Let me find the end of the merge block and the default computation.
- Grass (tile 2) specifically: grass's own framing uses `if (Main.tileMergeDirt[index1]) TileMergeAttempt(-2, 0, ...)` — the -2 meaning "special/other type" marker. Then the big mask→frame mapping at 52189+ applies to tiles with tileMergeDirt (which includes grass!) — so grass DOES frame via this mask code, using its own sheet (Tiles_2, with the extra rows). And the "GrassSpecial"/"JungleSpecial" sets handle mud merging (tile 59 = mud).

Wait, I need to double check: grass framing in vanilla actually happens at TileDrawing level? The grass "special" extra rows in Tiles_2 sheet: rows beyond the normal are used when grass merges with dirt. The vanilla approach: the mask code at 52189 sets rectangle coordinates like (144,108), (36,90) etc. — these are pixel coordinates in the 18px grid (col 8 = 144, etc.). Rows 5 (90), 6 (108), 7 (126), 8 (144), 9 (162) — these are the "merge frames" rows used by grass/dirt sheets. For the dirt sheet (Tiles_1?), dirt is at... hmm.

Actually: dirt (type 0) — the `case 0` switch handles dirt: when up/down/left/right neighbor has tileMergeDirt (i.e., is grass family or dirt-merging tiles), dirt calls TileFrame on that neighbor and checks mergeUp/mergeDown/mergeLeft/mergeRight flags, then sets up/down/... = index1 (0) so dirt connects. This is the reverse handshake.

And grass: tileMergeDirt[2] = true → in `if (Main.tileMergeDirt[index1])` grass does TileMergeAttempt(-2, 0, ...) which treats dirt neighbors (type 0) as "-2" (special) rather than same type. Then the mask code with -2 → picks the merge frames from grass's sheet rows 5-9 (the "extra rows"). Wait but Tiles_2 has 110 rows? The user said "extra rows in Tiles_2 grass sheet, 110 rows". Hmm, that's TEdit's blendRules probably.

Also grass "GrassSpecial" = {70, 60} (mushroom, jungle grass) — used for mud (59) merging: `case 59: ... TileMergeAttempt(index1, TileID.Sets.GrassSpecial, ...)` — mud merges with jungle/mushroom grass.

Now let me read TileMergeAttempt (49330-49560) and the section around 50560-50580 (flag resets). Also I need the general normal-block framing (not merge): the part where rectangle stays -1,-1 and frameX/frameY computed from up/down/left/right mask with the standard formula (e.g. `num = ...` using tile's sheet position `Main.tileFrame[type]`). Let me find that — search for "tileFrameCount" or the default after the merge if. Let me look after the merge block ends. The merge block is huge (52189 → maybe 53400). Let me find where the merge if-block ends and default frame assignment happens.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:05:30.098Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && sed -n '49330,49560p' WorldGen.cs",
 "description": "Read TileMergeAttempt overloads"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:05:30.139Z

**📎 ToolResult**

```
    public static void TileMergeAttemptFrametest(
      int i,
      int j,
      int myType,
      int lookfor,
      ref int up,
      ref int down,
      ref int left,
      ref int right,
      ref int upLeft,
      ref int upRight,
      ref int downLeft,
      ref int downRight)
    {
      if (up == lookfor)
      {
        WorldGen.TileFrame(i, j - 1, false, false);
        if (WorldGen.mergeDown)
          up = myType;
      }
      if (down == lookfor)
      {
        WorldGen.TileFrame(i, j + 1, false, false);
        if (WorldGen.mergeUp)
          down = myType;
      }
      if (left == lookfor)
      {
        WorldGen.TileFrame(i - 1, j, false, false);
        if (WorldGen.mergeRight)
          left = myType;
      }
      if (right == lookfor)
      {
        WorldGen.TileFrame(i + 1, j, false, false);
        if (WorldGen.mergeLeft)
          right = myType;
      }
      if (upLeft == lookfor)
        upLeft = myType;
      if (upRight == lookfor)
        upRight = myType;
      if (downLeft == lookfor)
        downLeft = myType;
      if (downRight != lookfor)
        return;
      downRight = myType;
    }

    public static void TileMergeAttemptFrametest(
      int i,
      int j,
      int myType,
      bool[] lookfor,
      ref int up,
      ref int down,
      ref int left,
      ref int right,
      ref int upLeft,
      ref int upRight,
      ref int downLeft,
      ref int downRight)
    {
      if (up > -1 && lookfor[up])
      {
        WorldGen.TileFrame(i, j - 1, false, false);
        if (WorldGen.mergeDown)
          up = myType;
      }
      if (down > -1 && lookfor[down])
      {
        WorldGen.TileFrame(i, j + 1, false, false);
        if (WorldGen.mergeUp)
          down = myType;
      }
      if (left > -1 && lookfor[left])
      {
        WorldGen.TileFrame(i - 1, j, false, false);
        if (WorldGen.mergeRight)
          left = myType;
      }
      if (right > -1 && lookfor[right])
      {
        WorldGen.TileFrame(i + 1, j, false, false);
        if (WorldGen.mergeLeft)
          right = myType;
      }
      if (upLeft > -1 && lookfor[upLeft])
        upLeft = myType;
      if (upRight > -1 && lookfor[upRight])
        upRight = myType;
      if (downLeft > -1 && lookfor[downLeft])
        downLeft = myType;
      if (downRight <= -1 || !lookfor[downRight])
        return;
      downRight = myType;
    }

    public static void TileMergeAttempt(
      int myType,
      int lookfor,
      ref int up,
      ref int down,
      ref int left,
      ref int right)
    {
      if (lookfor == up)
        up = myType;
      if (lookfor == down)
        down = myType;
      if (lookfor == left)
        left = myType;
      if (lookfor != right)
        return;
      right = myType;
    }

    public static void TileMergeAttempt(
      int myType,
      int lookfor,
      ref int up,
      ref int down,
      ref int left,
      ref int right,
      ref int upLeft,
      ref int upRight,
      ref int downLeft,
      ref int downRight)
    {
      if (lookfor == up)
        up = myType;
      if (lookfor == down)
        down = myType;
      if (lookfor == left)
        left = myType;
      if (lookfor == right)
        right = myType;
      if (lookfor == upLeft)
        upLeft = myType;
      if (lookfor == upRight)
        upRight = myType;
      if (lookfor == downLeft)
        downLeft = myType;
      if (lookfor != downRight)
        return;
      downRight = myType;
    }

    public static void TileMergeAttempt(
      int myType,
      bool[] lookfor,
      ref int up,
      ref int down,
      ref int left,
      ref int right,
      ref int upLeft,
      ref int upRight,
      ref int downLeft,
      ref int downRight)
    {
      if (up > -1 && lookfor[up])
        up = myType;
      if (down > -1 && lookfor[down])
        down = myType;
      if (left > -1 && lookfor[left])
        left = myType;
      if (right > -1 && lookfor[right])
        right = myType;
      if (upLeft > -1 && lookfor[upLeft])
        upLeft = myType;
      if (upRight > -1 && lookfor[upRight])
        upRight = myType;
      if (downLeft > -1 && lookfor[downLeft])
        downLeft = myType;
      if (downRight <= -1 || !lookfor[downRight])
        return;
      downRight = myType;
    }

    public static void TileMergeAttempt(
      int myType,
      bool[] lookfor,
      bool[] exclude,
      ref int up,
      ref int down,
      ref int left,
      ref int right,
      ref int upLeft,
      ref int upRight,
      ref int downLeft,
      ref int downRight)
    {
      if (up > -1 && !exclude[up] && lookfor[up])
        up = myType;
      if (down > -1 && !exclude[down] && lookfor[down])
        down = myType;
      if (left > -1 && !exclude[left] && lookfor[left])
        left = myType;
      if (right > -1 && !exclude[right] && lookfor[right])
        right = myType;
      if (upLeft > -1 && !exclude[upLeft] && lookfor[upLeft])
        upLeft = myType;
      if (upRight > -1 && !exclude[upRight] && lookfor[upRight])
        upRight = myType;
      if (downLeft > -1 && !exclude[downLeft] && lookfor[downLeft])
        downLeft = myType;
      if (downRight <= -1 || exclude[downRight] || !lookfor[downRight])
        return;
      downRight = myType;
    }

    public static void TileMergeAttemptWeird(
      int myType,
      int changeTo,
      bool[] exclude,
      ref int up,
      ref int down,
      ref int left,
      ref int right,
      ref int upLeft,
      ref int upRight,
      ref int downLeft,
      ref int downRight)
    {
      if (up > -1 && !exclude[up] && up != myType)
        up = changeTo;
      if (down > -1 && !exclude[down] && down != myType)
        down = changeTo;
      if (left > -1 && !exclude[left] && left != myType)
        left = changeTo;
      if (right > -1 && !exclude[right] && right != myType)

```


---

## 🤖 Assistant · 2026-08-07T07:05:33.924Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now I need the general (non-merge) block framing — where rectangle.X/Y remain -1 and the standard frame is computed from the 8-neighbor mask. Let me find the end of the merge block and the default. Search in the range 52800-53600 for the default. Let me grep for "tileFrameCount" or "num17" etc. Better: find where the merge if-block ends. Search for lines with pattern of the general framing: "if (up == -1)" combos producing 0,1,2 style numbering. In vanilla, the final assignment is:

```
if (rectangle.X == -1 && rectangle.Y == -1) {
  int num = ...;
  tile1.frameX = (short)(Main.tileFrame[type] ... );
}
```

Let me search for "frameX = " within 52000-54000 and "frameY".
````

</details>


---

## 🤖 Assistant · 2026-08-07T07:05:35.332Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && awk 'NR>=53000 && NR<=54200 && (/frameX = /||/frameY = /||/num17 = /||/num = up/||/tileFrame\\[/)' WorldGen.cs | head -30; echo \"=== lines with frameX assignment ===\"; grep -n \"tile1.frameX = \\|tile1.frameY = \\|\\.frameX = (\\|num16 = \\|num17 = \" WorldGen.cs | awk -F: '$1>50400 && $1<55000' | head -30",
 "description": "Locate final frameX/frameY assignment in TileFrame"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:05:39.350Z

**📎 ToolResult**

```
                      tile1.frameX = (short) rectangle.X;
                      tile1.frameY = (short) rectangle.Y;
        tile1.frameX = num;
        tile1.frameX = (short) (22 + (int) num);
        tile1.frameX = (short) (44 + (int) num);
        tile1.frameX = num;
        tile.frameX = (short) 0;
        tile.frameX = (short) 22;
        tile.frameX = (short) 44;
        tile.frameX = (short) 66;
      int frameX = (int) tileCache.frameX;
      int frameY = (int) tileCache.frameY;
      int frameY = (int) tileCache.frameY;
=== lines with frameX assignment ===
53559:                      tile1.frameX = (short) rectangle.X;
53560:                      tile1.frameY = (short) rectangle.Y;
53759:        tile1.frameX = num;
53761:        tile1.frameX = (short) (22 + (int) num);
53763:        tile1.frameX = (short) (44 + (int) num);
53765:        tile1.frameX = num;
53800:        tile.frameX = (short) 0;
53802:        tile.frameX = (short) 22;
53804:        tile.frameX = (short) 44;
53806:        tile.frameX = (short) 66;

```


---

## 🤖 Assistant · 2026-08-07T07:05:43.511Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && sed -n '53370,53575p' WorldGen.cs",
 "description": "Read general block framing mask code"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:05:43.571Z

**📎 ToolResult**

```
                              rectangle.Y = 54;
                              break;
                          }
                        }
                        else if (up == index1 && down != index1 && (left != index1 && right == index1))
                        {
                          switch (num4)
                          {
                            case 0:
                              rectangle.X = 0;
                              rectangle.Y = 72;
                              break;
                            case 1:
                              rectangle.X = 36;
                              rectangle.Y = 72;
                              break;
                            default:
                              rectangle.X = 72;
                              rectangle.Y = 72;
                              break;
                          }
                        }
                        else if (up == index1 && down != index1 && (left == index1 && right != index1))
                        {
                          switch (num4)
                          {
                            case 0:
                              rectangle.X = 18;
                              rectangle.Y = 72;
                              break;
                            case 1:
                              rectangle.X = 54;
                              rectangle.Y = 72;
                              break;
                            default:
                              rectangle.X = 90;
                              rectangle.Y = 72;
                              break;
                          }
                        }
                        else if (up == index1 && down == index1 && (left != index1 && right != index1))
                        {
                          switch (num4)
                          {
                            case 0:
                              rectangle.X = 90;
                              rectangle.Y = 0;
                              break;
                            case 1:
                              rectangle.X = 90;
                              rectangle.Y = 18;
                              break;
                            default:
                              rectangle.X = 90;
                              rectangle.Y = 36;
                              break;
                          }
                        }
                        else if (up != index1 && down != index1 && (left == index1 && right == index1))
                        {
                          switch (num4)
                          {
                            case 0:
                              rectangle.X = 108;
                              rectangle.Y = 72;
                              break;
                            case 1:
                              rectangle.X = 126;
                              rectangle.Y = 72;
                              break;
                            default:
                              rectangle.X = 144;
                              rectangle.Y = 72;
                              break;
                          }
                        }
                        else if (up != index1 && down == index1 && (left != index1 && right != index1))
                        {
                          switch (num4)
                          {
                            case 0:
                              rectangle.X = 108;
                              rectangle.Y = 0;
                              break;
                            case 1:
                              rectangle.X = 126;
                              rectangle.Y = 0;
                              break;
                            default:
                              rectangle.X = 144;
                              rectangle.Y = 0;
                              break;
                          }
                        }
                        else if (up == index1 && down != index1 && (left != index1 && right != index1))
                        {
                          switch (num4)
                          {
                            case 0:
                              rectangle.X = 108;
                              rectangle.Y = 54;
                              break;
                            case 1:
                              rectangle.X = 126;
                              rectangle.Y = 54;
                              break;
                            default:
                              rectangle.X = 144;
                              rectangle.Y = 54;
                              break;
                          }
                        }
                        else if (up != index1 && down != index1 && (left != index1 && right == index1))
                        {
                          switch (num4)
                          {
                            case 0:
                              rectangle.X = 162;
                              rectangle.Y = 0;
                              break;
                            case 1:
                              rectangle.X = 162;
                              rectangle.Y = 18;
                              break;
                            default:
                              rectangle.X = 162;
                              rectangle.Y = 36;
                              break;
                          }
                        }
                        else if (up != index1 && down != index1 && (left == index1 && right != index1))
                        {
                          switch (num4)
                          {
                            case 0:
                              rectangle.X = 216;
                              rectangle.Y = 0;
                              break;
                            case 1:
                              rectangle.X = 216;
                              rectangle.Y = 18;
                              break;
                            default:
                              rectangle.X = 216;
                              rectangle.Y = 36;
                              break;
                          }
                        }
                        else if (up != index1 && down != index1 && (left != index1 && right != index1))
                        {
                          switch (num4)
                          {
                            case 0:
                              rectangle.X = 162;
                              rectangle.Y = 54;
                              break;
                            case 1:
                              rectangle.X = 180;
                              rectangle.Y = 54;
                              break;
                            default:
                              rectangle.X = 198;
                              rectangle.Y = 54;
                              break;
                          }
                        }
                      }
                      if (rectangle.X <= -1 || rectangle.Y <= -1)
                      {
                        if (num4 <= 0)
                        {
                          rectangle.X = 18;
                          rectangle.Y = 18;
                        }
                        else if (num4 == 1)
                        {
                          rectangle.X = 36;
                          rectangle.Y = 18;
                        }
                        if (num4 >= 2)
                        {
                          rectangle.X = 54;
                          rectangle.Y = 18;
                        }
                      }
                      if (Main.tileLargeFrames[index1] == (byte) 1 && num4 == 3)
                        rectangle.Y += 90;
                      if (Main.tileLargeFrames[index1] == (byte) 2 && num4 == 3)
                        rectangle.Y += 90;
                      tile1.frameX = (short) rectangle.X;
                      tile1.frameY = (short) rectangle.Y;
                      if (TileID.Sets.IsVine[index1])
                      {
                        up = tileTopCache == null ? index1 : (tileTopCache.nactive() ? (!tileTopCache.bottomSlope() ? (int) tileTopCache.type : -1) : -1);
                        if (index1 != up)
                        {
                          int num5 = up == 109 ? 1 : (up == 115 ? 1 : 0);
                          bool flag2 = up == 199 || up == 205;
                          bool flag3 = up == 2 || up == 52;
                          bool flag4 = up == 382;
                          int num7 = up == 70 ? 1 : (up == 528 ? 1 : 0);
                          ushort num8 = 0;
                          if (num7 != 0)
                            num8 = (ushort) 528;
                          if (num5 != 0)
                            num8 = (ushort) 115;

```


---

## 🤖 Assistant · 2026-08-07T07:05:51.832Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This is the giant if/else chain mapping the 8-neighbor mask (up/down/left/right equal to index1 or not, plus -2 special) to frame rectangle coordinates in the 18px grid. This is the "standard block framing" — a hard-coded if/else chain, NOT a lookup table (in contrast to SelfFrame8Way which uses a lookup for gemsparks).

Note the frame coords: X values 0,18,36,...,216 and Y 0..72 (rows 0-4) for the normal block framing, plus merge rows (Y=90,108,126,144,162 = rows 5-9) when neighbor == -2.

Now I also need the beginning of the neighbor setup: where up/down/left/right/upLeft/etc. are computed (~50560-50580). Let me read that region: 50500-50580. Also num4 (frame number/variant) and resetFrame handling.

Then the cascade (item 4): when tile placed/removed. In vanilla 1.4.0.5, there's `WorldGen.SquareTileFrame` and also Framing... the caller mentioned AddFrame/FrameNearTile — those don't exist in 1.4.0.5 (they were added in 1.4.4). In 1.4.0.5 the cascade is SquareTileFrame + TileMergeAttemptFrametest recursive calls. Let me verify: does anything call SquareTileFrame from WorldGen.KillTile / PlaceTile? Let me grep calls.

Also "Wiring" — caller asked about Framing.Wiring; check if it exists in this decompile. grep "static void Wiring" or "Wiring(" in WorldGen. Let me check.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:05:51.835Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && sed -n '50500,50580p' WorldGen.cs",
 "description": "Read neighbor setup at TileFrame start"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:05:51.883Z

**📎 ToolResult**

```
                      {
                        if (tileTopCache.frameY == (short) 90)
                          up = index1;
                        else if (tileTopCache.frameY == (short) 54)
                          up = index1;
                      }
                      if (index1 == 225)
                      {
                        if (down == 165)
                          down = index1;
                        if (up == 165)
                          up = index1;
                      }
                      if ((index1 == 200 || index1 == 161 || (index1 == 147 || index1 == 163) || index1 == 164) && down == 165)
                        down = index1;
                      if ((tile1.slope() == (byte) 1 || tile1.slope() == (byte) 2) && (down > -1 && !TileID.Sets.Platforms[down]))
                        down = index1;
                      if (up > -1 && (tileTopCache.slope() == (byte) 1 || tileTopCache.slope() == (byte) 2) && !TileID.Sets.Platforms[up])
                        up = index1;
                      if ((tile1.slope() == (byte) 3 || tile1.slope() == (byte) 4) && (up > -1 && !TileID.Sets.Platforms[up]))
                        up = index1;
                      if (down > -1 && (tile10.slope() == (byte) 3 || tile10.slope() == (byte) 4) && !TileID.Sets.Platforms[down])
                        down = index1;
                      if (index1 == 124)
                      {
                        if (up > -1 && Main.tileSolid[up] && !TileID.Sets.Platforms[up])
                          up = index1;
                        if (down > -1 && Main.tileSolid[down] && !TileID.Sets.Platforms[down])
                          down = index1;
                      }
                      if (up > -1 && tileTopCache.halfBrick() && !TileID.Sets.Platforms[up])
                        up = index1;
                      if (left > -1 && tile11.halfBrick())
                      {
                        if (tile1.halfBrick())
                          left = index1;
                        else if ((int) tile11.type != index1)
                          left = -1;
                      }
                      if (right > -1 && tile12.halfBrick())
                      {
                        if (tile1.halfBrick())
                          right = index1;
                        else if ((int) tile12.type != index1)
                          right = -1;
                      }
                      if (tile1.halfBrick())
                      {
                        if (left != index1)
                          left = -1;
                        if (right != index1)
                          right = -1;
                        up = -1;
                      }
                      if (tile10 != null && tile10.halfBrick())
                        down = -1;
                      if (!Main.tileSolid[index1])
                      {
                        if (index1 == 49)
                        {
                          WorldGen.CheckOnTable1x1(i, j, (int) (byte) index1);
                          return;
                        }
                        if (index1 == 80)
                        {
                          WorldGen.CactusFrame(i, j);
                          return;
                        }
                      }
                      WorldGen.mergeUp = false;
                      WorldGen.mergeDown = false;
                      WorldGen.mergeLeft = false;
                      WorldGen.mergeRight = false;
                      int num4;
                      if (resetFrame)
                      {
                        num4 = WorldGen.genRand.Next(0, 3);
                        tile1.frameNumber((byte) num4);
                      }
                      else
                        num4 = (int) tile1.frameNumber();

```


---

## 🤖 Assistant · 2026-08-07T07:05:52.706Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && grep -rn \"SquareTileFrame(\" WorldGen.cs | grep -v \"public static\" | head -20; echo \"=== Wiring ===\"; grep -rn \"void Wiring\" --include=\"*.cs\" . | head; echo \"=== KillTile/PlaceTile calls ===\"; grep -n \"SquareTileFrame\\|TileFrame(\" WorldGen.cs | grep -n \"KillTile\\|PlaceTile\" | head",
 "description": "Find re-frame cascade callers"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:05:52.805Z

**📎 ToolResult**

```
WorldGen.cs:367:      WorldGen.SquareTileFrame(x, y, false);
WorldGen.cs:391:        WorldGen.SquareTileFrame(x, y, true);
WorldGen.cs:408:      WorldGen.SquareTileFrame(x, y, true);
WorldGen.cs:1633:          WorldGen.SquareTileFrame(i1, j1, true);
WorldGen.cs:1651:              WorldGen.SquareTileFrame(i1, j1, true);
WorldGen.cs:1670:              WorldGen.SquareTileFrame(i1, j1, true);
WorldGen.cs:4235:                WorldGen.SquareTileFrame(i2, j2, true);
WorldGen.cs:4309:                  WorldGen.SquareTileFrame(i2, j2, true);
WorldGen.cs:4318:                  WorldGen.SquareTileFrame(i2, j2, true);
WorldGen.cs:4360:        WorldGen.SquareTileFrame(index1, index4, true);
WorldGen.cs:4372:          WorldGen.SquareTileFrame(index1, index4, true);
WorldGen.cs:4381:            WorldGen.SquareTileFrame(index2, index3, true);
WorldGen.cs:4415:                WorldGen.SquareTileFrame(index2, index3, true);
WorldGen.cs:10751:            WorldGen.SquareTileFrame(WorldGen.lAltarX + index1, WorldGen.lAltarY + index2, true);
WorldGen.cs:10918:                    WorldGen.SquareTileFrame(point.X, point.Y, true);
WorldGen.cs:13498:                  WorldGen.SquareTileFrame(i, j1, true);
WorldGen.cs:13634:            WorldGen.SquareTileFrame(i2, index1, true);
WorldGen.cs:17676:          WorldGen.SquareTileFrame(x, y, true);
WorldGen.cs:25535:      WorldGen.SquareTileFrame(index1, index2, true);
WorldGen.cs:25612:          WorldGen.SquareTileFrame(x, y, true);
=== Wiring ===
=== KillTile/PlaceTile calls ===

```


---

## 🤖 Assistant · 2026-08-07T07:05:56.360Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. Let me check the neighbor initialization (where up/down/left/right are first set from neighbor tiles) — search earlier in TileFrame for "int up = " etc. It's before 50500, probably around 50400-50500. Let me grep.

Also check the initial part of TileFrame where neighbors are read (up = tile above type or -1). And check where grass framing for vines happens (not needed).

For item 4 (cascade on place/remove): lines 367, 391, 408 in WorldGen.cs — probably KillTile / PlaceTile. Let me check context of those lines.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:05:56.572Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && grep -n \"int up = \\|int down = \\|int left = \\|int right = \\|int upLeft = \\|upLeft = \" WorldGen.cs | awk -F: '$1>49639 && $1<50500' | head -12; echo \"=== context 340-420 ===\"; sed -n '340,412p' WorldGen.cs",
 "description": "Find neighbor init and kill/place context"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:06:00.564Z

**📎 ToolResult**

```
50400:                      int upLeft = -1;
50401:                      int up = -1;
50403:                      int left = -1;
50404:                      int right = -1;
50406:                      int down = -1;
50433:                        upLeft = !Main.tileStone[(int) tile25.type] ? (int) tile25.type : 1;
=== context 340-420 ===
        {
          Tile testTile = Main.tile[x + index1, y + index2 + 1];
          Tile tile = Main.tile[x + index1, y + index2];
          if (!tile.active() && WorldGen.SolidTile2(testTile))
          {
            WorldGen.PlaceTile(x + index1, y + index2, 135, true, false, -1, 0);
            if (tile.active() && tile.type == (ushort) 135)
            {
              WorldUtils.WireLine(new Point(x, y), new Point(x + index1, y + index2));
              return;
            }
          }
        }
      }
    }

    public static bool EmptyLiquid(int x, int y)
    {
      if (!WorldGen.InWorld(x, y, 0))
        return false;
      Tile tile = Main.tile[x, y];
      if (tile == null)
        return false;
      int num = (int) tile.liquidType();
      if (tile.nactive() && Main.tileSolid[(int) tile.type] && !Main.tileSolidTop[(int) tile.type])
        return false;
      tile.Clear(TileDataType.Liquid);
      WorldGen.SquareTileFrame(x, y, false);
      if (Main.netMode == 1)
        NetMessage.sendWater(x, y);
      else
        Liquid.AddWater(x, y);
      return true;
    }

    public static bool PlaceLiquid(int x, int y, byte liquidType, byte amount)
    {
      if (!WorldGen.InWorld(x, y, 0))
        return false;
      Tile tile = Main.tile[x, y];
      if (tile == null)
        return false;
      byte num1 = tile.liquidType();
      if (tile.nactive() && Main.tileSolid[(int) tile.type] && !Main.tileSolidTop[(int) tile.type])
        return false;
      if (tile.liquid == (byte) 0 || (int) liquidType == (int) num1)
      {
        tile.liquidType((int) liquidType);
        if ((int) amount + (int) tile.liquid > (int) byte.MaxValue)
          amount = (byte) ((uint) byte.MaxValue - (uint) tile.liquid);
        tile.liquid += amount;
        WorldGen.SquareTileFrame(x, y, true);
        if (Main.netMode != 0)
          NetMessage.sendWater(x, y);
        return true;
      }
      ushort num2 = 0;
      if (liquidType == (byte) 0 && num1 == (byte) 1 || liquidType == (byte) 1 && num1 == (byte) 0)
        num2 = (ushort) 56;
      else if (liquidType == (byte) 0 && num1 == (byte) 2 || liquidType == (byte) 2 && num1 == (byte) 0)
        num2 = (ushort) 229;
      else if (liquidType == (byte) 1 && num1 == (byte) 2 || liquidType == (byte) 2 && num1 == (byte) 1)
        num2 = (ushort) 230;
      if (num2 == (ushort) 0)
        return false;
      tile.liquid = (byte) 0;
      tile.liquidType(0);
      WorldGen.PlaceTile(x, y, (int) num2, true, false, -1, 0);
      WorldGen.SquareTileFrame(x, y, true);
      if (Main.netMode != 0)
        NetMessage.SendTileSquare(-1, x - 1, y - 1, 3, num2 == (ushort) 56 ? TileChangeType.LavaWater : TileChangeType.HoneyLava);
      return true;
    }

```


---

## 🤖 Assistant · 2026-08-07T07:06:01.973Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && sed -n '50395,50500p' WorldGen.cs",
 "description": "Read neighbor mask initialization"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:06:02.019Z

**📎 ToolResult**

```
                      Tile tile12 = Main.tile[i + 1, j];
                      Tile tile13 = Main.tile[i - 1, j + 1];
                      Tile tile24 = Main.tile[i + 1, j + 1];
                      Tile tile25 = Main.tile[i - 1, j - 1];
                      Tile tile26 = Main.tile[i + 1, j - 1];
                      int upLeft = -1;
                      int up = -1;
                      int upRight = -1;
                      int left = -1;
                      int right = -1;
                      int downLeft = -1;
                      int down = -1;
                      int downRight = -1;
                      if (tile11 != null && tile11.active())
                      {
                        left = !Main.tileStone[(int) tile11.type] ? (int) tile11.type : 1;
                        if (tile11.slope() == (byte) 1 || tile11.slope() == (byte) 3)
                          left = -1;
                      }
                      if (tile12 != null && tile12.active())
                      {
                        right = !Main.tileStone[(int) tile12.type] ? (int) tile12.type : 1;
                        if (tile12.slope() == (byte) 2 || tile12.slope() == (byte) 4)
                          right = -1;
                      }
                      if (tileTopCache != null && tileTopCache.active())
                      {
                        up = !Main.tileStone[(int) tileTopCache.type] ? (int) tileTopCache.type : 1;
                        if (tileTopCache.slope() == (byte) 3 || tileTopCache.slope() == (byte) 4)
                          up = -1;
                      }
                      if (tile10 != null && tile10.active())
                      {
                        down = !Main.tileStone[(int) tile10.type] ? (int) tile10.type : 1;
                        if (tile10.slope() == (byte) 1 || tile10.slope() == (byte) 2)
                          down = -1;
                      }
                      if (tile25 != null && tile25.active())
                        upLeft = !Main.tileStone[(int) tile25.type] ? (int) tile25.type : 1;
                      if (tile26 != null && tile26.active())
                        upRight = !Main.tileStone[(int) tile26.type] ? (int) tile26.type : 1;
                      if (tile13 != null && tile13.active())
                        downLeft = !Main.tileStone[(int) tile13.type] ? (int) tile13.type : 1;
                      if (tile24 != null && tile24.active())
                        downRight = !Main.tileStone[(int) tile24.type] ? (int) tile24.type : 1;
                      if (tile1.slope() == (byte) 2)
                      {
                        up = -1;
                        left = -1;
                      }
                      if (tile1.slope() == (byte) 1)
                      {
                        up = -1;
                        right = -1;
                      }
                      if (tile1.slope() == (byte) 4)
                      {
                        down = -1;
                        left = -1;
                      }
                      if (tile1.slope() == (byte) 3)
                      {
                        down = -1;
                        right = -1;
                      }
                      switch (index1)
                      {
                        case 147:
                          WorldGen.TileMergeAttempt(index1, Main.tileBrick, TileID.Sets.Ices, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                          break;
                        case 161:
                        case 163:
                        case 164:
                        case 200:
                          WorldGen.TileMergeAttempt(index1, Main.tileBrick, TileID.Sets.Snow, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                          break;
                        case 162:
                          WorldGen.TileMergeAttempt(index1, Main.tileBrick, TileID.Sets.IcesSnow, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                          break;
                        default:
                          if (Main.tileBrick[index1])
                          {
                            if (index1 == 60 || index1 == 70)
                            {
                              WorldGen.TileMergeAttempt(index1, Main.tileBrick, TileID.Sets.Mud, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                              break;
                            }
                            WorldGen.TileMergeAttempt(index1, Main.tileBrick, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                            break;
                          }
                          if (Main.tilePile[index1])
                          {
                            WorldGen.TileMergeAttempt(index1, Main.tilePile, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
                            break;
                          }
                          break;
                      }
                      if ((index1 == 1 || Main.tileMoss[index1] || (index1 == 117 || index1 == 25) || index1 == 203) && down == 165)
                      {
                        if (tile10.frameY == (short) 72)
                          down = index1;
                        else if (tile10.frameY == (short) 0)
                          down = index1;
                      }
                      if ((index1 == 1 || Main.tileMoss[index1] || (index1 == 117 || index1 == 25) || index1 == 203) && up == 165)
                      {

```


---

## 🤖 Assistant · 2026-08-07T07:06:14.699Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I now have a comprehensive picture of the vanilla side. A few remaining checks for the vanilla report:

1. Where grass (tile 2) is handled: grass is in the "default" tileBrick? No — grass (2) is not tileBrick. Grass has Main.tileMergeDirt[2]=true. Let me verify Main.tileMergeDirt entries in Main.cs. grep "tileMergeDirt[" in Main.cs.

2. The grass framing rows: For grass (index1=2), the mask code at 52189+ handles `Main.tileMergeDirt[index1]` — with TileMergeAttempt(-2, 0, ...) marking dirt neighbors as -2. The mask code then uses -2 to pick merge frames. But wait — where do the grass-specific "extra rows" come from? In Tiles_2, the grass sheet is 22 tiles wide × 110 rows? Hmm, the user says "extra rows in Tiles_2 grass sheet, 110 rows". Actually vanilla: grass frames use `Main.tileFrame[2]` = (0,0) offset... the rectangle coords computed are absolute within the sheet for that type? No — rectangle coords like 0..234, rows 0-4 + merge rows 5-9 are relative and then tile1.frameX = rectangle.X directly?? For grass, the frame coords are used directly as frameX/frameY in the texture with `Main.tileFrame[type]` offsets applied at draw time? Let me check TileDrawing: it uses tileFrameX + Main.tileFrame[type].X? Actually in TileDrawing.DrawSingleTile: `int num = tile.frameX + Main.tileFrame[type]...`. Hmm, actually `Main.tileFrame` stores the sheet offset for animated tiles. For normal tiles the sheet position is determined by... Let me check how frameX/frameY map to texture: In TileDrawing, `Assets` tilesheets are laid out so each tile type occupies a region; for most tiles, frameX 0-234 and frameY 0-234 with type-based offset computed from the "tile frame" structure. Actually vanilla computes texture position via `Main.tileTexture[type]` where each type has its own texture (Textures_2 etc. for a few shared ones). Yes! In 1.4, most tiles each have their own texture file; frameX/frameY are offsets within that texture. The 5x13 grid: 13 columns × ... The frame coords 0..234 X (13 cols) and rows 0..(many). Grass texture (Tiles_2.png) is 13 cols × 110 rows? Hmm — Tiles_2 is 224x2240? Not important; I can note the merge frames occupy rows 5-9 (Y=90..162) in the shared block-framing layout.

Hmm wait, actually for the user's "110 rows" claim: TEdit's blendRules uses a grid; the Tiles_2 texture in TEdit may be padded. Not critical.

3. Where is grass's special "GrassSpecial" used — mud (59) merging with jungle/mushroom grass: `case 59` in the switch at ~50800. And jungle grass (60)/mushroom grass (70) are tileBrick types that merge with Mud set (TileID.Sets.Mud). Let me confirm TileID.Sets.Mud and Sets.Conversion.Grass contents.

4. Item 5: slope/half-brick handling location: WorldGen.TileFrame lines 50458-50510 (mask adjustments), and WorldGen.SlopeTile (49170). Also the slope of the tile itself affects rendering (TileDrawing). Good enough.

5. Check Main.tileMergeDirt entries.

Let me also check TileID.Sets.Mud and Conversion.Grass/MergesWithDirtInASpecialWay.

Then TEdit part:
- TileProperty.cs lines 120-180 (IsGrass, MergeWith, Merges).
- blendRules.GetUVForMasks with strictness — find BlendRules class file. It probably has the rule table with strictness 2 for grass selecting merge rows. Let me find it.

Let me run these searches in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:06:15.534Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && grep -n \"tileMergeDirt\\[\" Main.cs | head -15; echo \"=== Mud set ===\"; grep -n \"Mud\\b\\|MergesWithDirtInASpecialWay\\|ChecksForMerge\" ID/TileID.cs | head -12; echo \"=== Conversion.Grass ===\"; grep -n \"Grass = \\|Stone = \" ID/TileID.cs | head",
 "description": "Check tileMergeDirt and Mud sets in vanilla"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:06:15.588Z

**📎 ToolResult**

```
5293:      Main.tileMergeDirt[202] = true;
5297:      Main.tileMergeDirt[498] = true;
5305:      Main.tileMergeDirt[188] = true;
5374:      Main.tileMergeDirt[177] = true;
5375:      Main.tileMergeDirt[190] = true;
5378:      Main.tileMergeDirt[197] = true;
5398:      Main.tileMergeDirt[175] = true;
5399:      Main.tileMergeDirt[176] = true;
5400:      Main.tileMergeDirt[177] = true;
5401:      Main.tileMergeDirt[208] = true;
5476:      Main.tileMergeDirt[234] = true;
5656:      Main.tileMergeDirt[160] = true;
5661:      Main.tileMergeDirt[145] = true;
5664:      Main.tileMergeDirt[146] = true;
5669:      Main.tileMergeDirt[148] = true;
=== Mud set ===
73:    public const ushort Mud = 59;
688:      public static bool[] Mud = TileID.Sets.Factory.CreateBoolSet(59);
714:      public static bool[] ChecksForMerge = TileID.Sets.Factory.CreateBoolSet(0, 2, 60, 70, 199, 109, 477, 492, 57, 58, 75, 76, 147, 161, 164, 163, 200, 162, 189, 196, 460, 224, 191, 383, 211, 225, 59, 226, 396, 397, 398, 399, 402, 400, 401, 403, 404, 234, 112, 407);
725:      public static bool[] OreMergesWithMud = TileID.Sets.Factory.CreateBoolSet(7, 166, 6, 167, 9, 168, 8, 169, 22, 204, 37, 58, 107, 221, 108, 222, 111, 223);
737:        public static bool[] MergesWithDirtInASpecialWay = TileID.Sets.Factory.CreateBoolSet(2, 23, 109, 199, 477, 492);
=== Conversion.Grass ===
15:    public const ushort Stone = 1;
16:    public const ushort Grass = 2;
37:    public const ushort CorruptGrass = 23;
74:    public const ushort JungleGrass = 60;
84:    public const ushort MushroomGrass = 70;
123:    public const ushort HallowedGrass = 109;
213:    public const ushort CrimsonGrass = 199;
491:    public const ushort GolfGrass = 477;
738:        public static bool[] Grass = TileID.Sets.Factory.CreateBoolSet(2, 23, 60, 199, 109, 477, 492);
739:        public static bool[] GolfGrass = TileID.Sets.Factory.CreateBoolSet(477, 492);

```


---

## 🤖 Assistant · 2026-08-07T07:06:16.056Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor && grep -rn \"GetUVForMasks\" src --include=\"*.cs\" -l; echo \"===\"; grep -rn \"class BlendRules\\|blendRules = \" src --include=\"*.cs\" | head",
 "description": "Find BlendRules class in TEdit"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:06:16.140Z

**📎 ToolResult**

```
src/TEdit/Render/BlendRules.cs
src/TEdit/View/WorldRenderXna.xaml.cs
===
src/TEdit/Render/BlendRules.cs:34:class BlendRules
src/TEdit/Render/BlendRules.cs:39:    private LinkedList<MatchRule>[] blendRules = new LinkedList<MatchRule>[16];
src/TEdit/View/WorldRenderXna.xaml.cs:4200:        BlendRules blendRules = BlendRules.Instance;
src/TEdit/View/WorldRenderXna.xaml.cs:4323:        BlendRules blendRules = BlendRules.Instance;
src/TEdit/View/WorldRenderXna.xaml.cs:6277:        BlendRules blendRules = BlendRules.Instance;

```


---

## 🤖 Assistant · 2026-08-07T07:06:18.180Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting — the tileMergeDirt grep didn't show index [2]. Let me search specifically: "tileMergeDirt[2]". Also BlendRules.cs — read it, particularly GetUVForMasks and strictness handling (grass). Let's do both.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:06:19.089Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && grep -n \"tileMergeDirt\\[(int) \\|tileMergeDirt\\[2\\]\\|tileMergeDirt\\[0\\]\" Main.cs | head -5; grep -n \"tileMergeDirt\" Main.cs | wc -l; echo \"=== find line with just type arg ===\"; sed -n '5285,5300p' Main.cs",
 "description": "Check how tileMergeDirt is filled"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:06:19.146Z

**📎 ToolResult**

```
     109
=== find line with just type arg ===
      Main.tileBrick[154] = true;
      Main.tileBrick[155] = true;
      Main.tileBrick[156] = true;
      Main.tileBrick[157] = true;
      Main.tileBrick[158] = true;
      Main.tileBrick[159] = true;
      Main.tileBrick[273] = true;
      Main.tileBrick[274] = true;
      Main.tileMergeDirt[202] = true;
      Main.tileBrick[202] = true;
      Main.tileSolid[202] = true;
      Main.tileBlockLight[202] = true;
      Main.tileMergeDirt[498] = true;
      Main.tileBrick[161] = true;
      Main.tileBlockLight[161] = true;
      Main.tileBlockLight[163] = true;

```


---

## 🤖 Assistant · 2026-08-07T07:06:19.362Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor && wc -l src/TEdit/Render/BlendRules.cs && grep -n \"strictness\\|GetUVForMasks\\|MatchRule\\|grass\\|Grass\" src/TEdit/Render/BlendRules.cs | head -50",
 "description": "Scan BlendRules.cs structure"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:06:19.399Z

**📎 ToolResult**

```
     511 src/TEdit/Render/BlendRules.cs
38:    private LinkedList<MatchRule>[] baseRules = new LinkedList<MatchRule>[16];
39:    private LinkedList<MatchRule>[] blendRules = new LinkedList<MatchRule>[16];
40:    private LinkedList<MatchRule>[] grassRules = new LinkedList<MatchRule>[16];
83:     * See the "MatchRule" object at the bottom for summaries
90:            baseRules[i] = new LinkedList<MatchRule>();
93:        baseRules[0].AddFirst(new MatchRule(0x0000, "D10", "D12")); //None
94:        baseRules[1].AddFirst(new MatchRule(0x0000, "A10", "C10")); //Right
95:        baseRules[2].AddFirst(new MatchRule(0x0000, "D7", "D9")); //Top
96:        baseRules[3].AddFirst(new MatchRule(0x0000, "E1", "E5")); //Top, Right
97:        baseRules[4].AddFirst(new MatchRule(0x0000, "A13", "C13")); //Left
98:        baseRules[5].AddFirst(new MatchRule(0x0000, "E7", "E9")); //Left, Right
99:        baseRules[6].AddFirst(new MatchRule(0x0000, "E2", "E6")); //Left, Top
100:        baseRules[7].AddFirst(new MatchRule(0x0000, "C2", "C4")); //Left, Top, Right
101:        baseRules[8].AddFirst(new MatchRule(0x0000, "A7", "A9")); //Bottom
102:        baseRules[9].AddFirst(new MatchRule(0x0000, "D1", "D5")); //Bottom, Right
103:        baseRules[10].AddFirst(new MatchRule(0x0000, "A6", "C6")); //Bottom, Top
104:        baseRules[11].AddFirst(new MatchRule(0x0000, "A1", "C1")); //Bottom, Top, Right
105:        baseRules[12].AddFirst(new MatchRule(0x0000, "D2", "D6")); //Bottom, Left
106:        baseRules[13].AddFirst(new MatchRule(0x0000, "A2", "A4")); //Bottom, Left, Right
107:        baseRules[14].AddFirst(new MatchRule(0x0000, "A5", "C5")); //Bottom, Left, Top
108:        baseRules[15].AddFirst(new MatchRule(0x0000, "B2", "B4")); //Bottom, Left, Top, Right
109:        baseRules[15].AddFirst(new MatchRule(0x0110, "A11", "C11")); //Bottom, Left, Top, Right, !TL, !BL
110:        baseRules[15].AddFirst(new MatchRule(0x1001, "A12", "C12")); //Bottom, Left, Top, Right, !TR, !BR
111:        baseRules[15].AddFirst(new MatchRule(0x0011, "B7", "B9")); //Bottom, Left, Top, Right, !TL, !TR
112:        baseRules[15].AddFirst(new MatchRule(0x1100, "C7", "C9")); //Bottom, Left, Top, Right, !BL, !BR
116:            //blendRules[i] = new LinkedList<MatchRule>(baseRules[i]); //These will be added later
117:            blendRules[i] = new LinkedList<MatchRule>();
120:        blendRules[0].AddFirst(new MatchRule(0x0000, 0x00000001, 0x0000, "N4", "N6"));
121:        blendRules[0].AddFirst(new MatchRule(0x0000, 0x00000010, 0x0000, "I7", "K7"));
122:        blendRules[0].AddFirst(new MatchRule(0x0000, 0x00000100, 0x0000, "N1", "N3"));
123:        blendRules[0].AddFirst(new MatchRule(0x0000, 0x00001000, 0x0000, "F7", "H7"));
124:        blendRules[0].AddFirst(new MatchRule(0x0000, 0x00000101, 0x0000, "L10", "L12"));
125:        blendRules[0].AddFirst(new MatchRule(0x0000, 0x00001010, 0x0000, "M7", "O7"));
126:        blendRules[0].AddFirst(new MatchRule(0x0000, 0x00001111, 0x0000, "L7", "L9"));
127:        blendRules[1].AddFirst(new MatchRule(0x0000, 0x00000100, 0x0000, "O1", "O3"));
128:        blendRules[2].AddFirst(new MatchRule(0x0000, 0x00001000, 0x0000, "F8", "H8"));
129:        blendRules[3].AddFirst(new MatchRule(0x0000, 0x00000100, 0x0000, "M1", "M3"));
130:        blendRules[3].AddFirst(new MatchRule(0x0000, 0x00001000, 0x0000, "F5", "H5"));
131:        blendRules[3].AddFirst(new MatchRule(0x0000, 0x00001100, 0x0000, "G3", "K3"));
132:        blendRules[4].AddFirst(new MatchRule(0x0000, 0x00000001, 0x0000, "O4", "O6"));
133:        blendRules[5].AddFirst(new MatchRule(0x0000, 0x00001010, 0x0000, "K9", "K11"));
134:        blendRules[6].AddFirst(new MatchRule(0x0000, 0x00000001, 0x0000, "M4", "M6"));
135:        blendRules[6].AddFirst(new MatchRule(0x0000, 0x00001000, 0x0000, "F6", "H6"));
136:        blendRules[6].AddFirst(new MatchRule(0x0000, 0x00001001, 0x0000, "G4", "K4"));
137:        blendRules[7].AddFirst(new MatchRule(0x0000, 0x00001000, 0x0000, "F9", "F11"));
138:        blendRules[8].AddFirst(new MatchRule(0x0000, 0x00000010, 0x0000, "I8", "K8"));
139:        blendRules[9].AddFirst(new MatchRule(0x0000, 0x00000010, 0x0000, "I5", "K5"));
140:        blendRules[9].AddFirst(new MatchRule(0x0000, 0x00000100, 0x0000, "L1", "L3"));
141:        blendRules[9].AddFirst(new MatchRule(0x0000, 0x00000110, 0x0000, "F3", "J3"));
142:        blendRules[10].AddFirst(new MatchRule(0x0000, 0x00000101, 0x0000, "H11", "J11"));

```


---

## 🤖 Assistant · 2026-08-07T07:06:22.009Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now read BlendRules.cs fully-ish: GetUVForMasks, strictness handling, grassRules, and the row mapping ("A1".."P9" style cell names → row letters). Let me read lines 1-90 and 230-511.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:06:22.010Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit/Render/BlendRules.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:06:22.220Z

**📎 ToolResult**

```
1	using System;
2	using System.Collections.Generic;
3	using System.Linq;
4	using TEdit.Editor;
5	using TEdit.ViewModel;
6	using TEdit.Geometry;
7	using TEdit.Terraria;
8	
9	/* Heathtech */
10	namespace TEdit.Render;
11	
12	public class RenderBlender : INotifyTileChanged
13	{
14	    private readonly World _world;
15	    private readonly TilePicker _tilePicker;
16	
17	    public RenderBlender(World world, TilePicker tilePicker)
18	    {
19	        _world = world;
20	        _tilePicker = tilePicker;
21	    }
22	
23	    public void UpdateTile(int x, int y, int width = 1, int height = 1)
24	    {
25	        BlendRules.ResetUVCache(_world, _tilePicker, x, y, width, height);
26	    }
27	
28	    public void UpdateTiles(IReadOnlyList<Vector2Int32> tiles)
29	    {
30	        BlendRules.ResetUVCache(_world, tiles);
31	    }
32	}
33	
34	class BlendRules
35	{
36	    private static BlendRules instance;
37	
38	    private LinkedList<MatchRule>[] baseRules = new LinkedList<MatchRule>[16];
39	    private LinkedList<MatchRule>[] blendRules = new LinkedList<MatchRule>[16];
40	    private LinkedList<MatchRule>[] grassRules = new LinkedList<MatchRule>[16];
41	    public Random randomVariation = new Random();
42	
43	    //This map is used during lazy merge validation to see whether a given tile is technically merged or not
44	    public byte[,] lazyMergeValidation = new byte[,] {
45	        {11, 13, 13, 13, 14, 10, 8, 8, 8, 1, 15, 15, 4, 13, 13, 13},
46	        {11, 15, 15, 15, 14, 10, 15, 15, 15, 1, 15, 15, 4, 7, 7, 7},
47	        {11, 7, 7, 7, 14, 10, 15, 15, 15, 1, 15, 15, 4, 11, 11, 11},
48	        {9, 12, 9, 12, 9, 12, 2, 2, 2, 0, 0, 0, 0, 14, 14, 14},
49	        {3, 6, 3, 6, 3, 6, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0},
50	        {15, 15, 15, 15, 11, 14, 8, 10, 15, 15, 15, 15, 15, 0, 0, 0},
51	        {15, 15, 15, 15, 11, 14, 8, 10, 15, 15, 15, 15, 15, 0, 0, 0},
52	        {15, 15, 15, 15, 11, 14, 8, 10, 15, 15, 15, 15, 15, 0, 0, 0},
53	        {15, 15, 15, 15, 11, 14, 2, 10, 15, 15, 15, 15, 15, 0, 0, 0},
54	        {15, 15, 15, 15, 11, 14, 2, 10, 15, 15, 15, 15, 15, 0, 0, 0},
55	        {15, 15, 15, 15, 11, 14, 2, 10, 15, 15, 15, 15, 15, 0, 0, 0},
56	        {13, 13, 13, 13, 13, 13, 15, 15, 15, 5, 5, 5, 0, 0, 0, 0},
57	        {7, 7, 7, 7, 7, 7, 10, 9, 13, 12, 9, 13, 12, 9, 13, 12},
58	        {4, 4, 4, 1, 1, 1, 10, 11, 15, 14, 11, 15, 14, 11, 15, 14},
59	        {5, 5, 5, 5, 5, 5, 10, 3, 7, 6, 3, 7, 6, 3, 7, 6},
60	        {11, 14, 13, 13, 13, 9, 9, 9, 12, 12, 12, 15, 15, 15, 0, 0},
61	        {11, 14, 7, 7, 7, 3, 3, 3, 6, 6, 6, 15, 15, 15, 0, 0},
62	        {11, 14, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 0, 0},
63	        {13, 13, 13, 13, 13, 13, 15, 15, 15, 0, 0, 0, 0, 0, 0, 0},
64	        {7, 7, 7, 7, 7, 7, 15, 15, 15, 0, 0, 0, 0, 0, 0, 0},
65	        {11, 11, 11, 11, 11, 11, 15, 15, 15, 0, 0, 0, 0, 0, 0, 0},
66	        {14, 14, 14, 14, 14, 14, 15, 15, 15, 0, 0, 0, 0, 0, 0, 0}
67	    };
68	
69	    //Make this class a singleton
70	    public static BlendRules Instance
71	    {
72	        get
73	        {
74	            if (instance == null)
75	            {
76	                instance = new BlendRules();
77	            }
78	            return instance;
79	        }
80	    }
81	
82	    /* The idea of blend rules is adapted from http://seancode.com/terrafirma/uvs.html which describes the process of determining the UV of a tile via a set of constraints
83	     * See the "MatchRule" object at the bottom for summaries
84	     * The general idea is that the rules are placed into 16 different "buckets" where each bucket is chosen based on what same-type neighbors a tile has
85	     */
86	    public BlendRules()
87	    {
88	        for (int i = 0; i < 16; i++)
89	        {
90	            baseRules[i] = new LinkedList<MatchRule>();
91	        }
92	
93	        baseRules[0].AddFirst(new MatchRule(0x0000, "D10", "D12")); //None
94	        baseRules[1].AddFirst(new MatchRule(0x0000, "A10", "C10")); //Right
95	        baseRules[2].AddFirst(new MatchRule(0x0000, "D7", "D9")); //Top
96	        baseRules[3].AddFirst(new MatchRule(0x0000, "E1", "E5")); //Top, Right
97	        baseRules[4].AddFirst(new MatchRule(0x0000, "A13", "C13")); //Left
98	        baseRules[5].AddFirst(new MatchRule(0x0000, "E7", "E9")); //Left, Right
99	        baseRules[6].AddFirst(new MatchRule(0x0000, "E2", "E6")); //Left, Top
100	        baseRules[7].AddFirst(new MatchRule(0x0000, "C2", "C4")); //Left, Top, Right
101	        baseRules[8].AddFirst(new MatchRule(0x0000, "A7", "A9")); //Bottom
102	        baseRules[9].AddFirst(new MatchRule(0x0000, "D1", "D5")); //Bottom, Right
103	        baseRules[10].AddFirst(new MatchRule(0x0000, "A6", "C6")); //Bottom, Top
104	        baseRules[11].AddFirst(new MatchRule(0x0000, "A1", "C1")); //Bottom, Top, Right
105	        baseRules[12].AddFirst(new MatchRule(0x0000, "D2", "D6")); //Bottom, Left
106	        baseRules[13].AddFirst(new MatchRule(0x0000, "A2", "A4")); //Bottom, Left, Right
107	        baseRules[14].AddFirst(new MatchRule(0x0000, "A5", "C5")); //Bottom, Left, Top
108	        baseRules[15].AddFirst(new MatchRule(0x0000, "B2", "B4")); //Bottom, Left, Top, Right
109	        baseRules[15].AddFirst(new MatchRule(0x0110, "A11", "C11")); //Bottom, Left, Top, Right, !TL, !BL
110	        baseRules[15].AddFirst(new MatchRule(0x1001, "A12", "C12")); //Bottom, Left, Top, Right, !TR, !BR
111	        baseRules[15].AddFirst(new MatchRule(0x0011, "B7", "B9")); //Bottom, Left, Top, Right, !TL, !TR
112	        baseRules[15].AddFirst(new MatchRule(0x1100, "C7", "C9")); //Bottom, Left, Top, Right, !BL, !BR
113	
114	        for (int i = 0; i < 16; i++)
115	        {
116	            //blendRules[i] = new LinkedList<MatchRule>(baseRules[i]); //These will be added later
117	            blendRules[i] = new LinkedList<MatchRule>();
118	        }
119	
120	        blendRules[0].AddFirst(new MatchRule(0x0000, 0x00000001, 0x0000, "N4", "N6"));
121	        blendRules[0].AddFirst(new MatchRule(0x0000, 0x00000010, 0x0000, "I7", "K7"));
122	        blendRules[0].AddFirst(new MatchRule(0x0000, 0x00000100, 0x0000, "N1", "N3"));
123	        blendRules[0].AddFirst(new MatchRule(0x0000, 0x00001000, 0x0000, "F7", "H7"));
124	        blendRules[0].AddFirst(new MatchRule(0x0000, 0x00000101, 0x0000, "L10", "L12"));
125	        blendRules[0].AddFirst(new MatchRule(0x0000, 0x00001010, 0x0000, "M7", "O7"));
126	        blendRules[0].AddFirst(new MatchRule(0x0000, 0x00001111, 0x0000, "L7", "L9"));
127	        blendRules[1].AddFirst(new MatchRule(0x0000, 0x00000100, 0x0000, "O1", "O3"));
128	        blendRules[2].AddFirst(new MatchRule(0x0000, 0x00001000, 0x0000, "F8", "H8"));
129	        blendRules[3].AddFirst(new MatchRule(0x0000, 0x00000100, 0x0000, "M1", "M3"));
130	        blendRules[3].AddFirst(new MatchRule(0x0000, 0x00001000, 0x0000, "F5", "H5"));
131	        blendRules[3].AddFirst(new MatchRule(0x0000, 0x00001100, 0x0000, "G3", "K3"));
132	        blendRules[4].AddFirst(new MatchRule(0x0000, 0x00000001, 0x0000, "O4", "O6"));
133	        blendRules[5].AddFirst(new MatchRule(0x0000, 0x00001010, 0x0000, "K9", "K11"));
134	        blendRules[6].AddFirst(new MatchRule(0x0000, 0x00000001, 0x0000, "M4", "M6"));
135	        blendRules[6].AddFirst(new MatchRule(0x0000, 0x00001000, 0x0000, "F6", "H6"));
136	        blendRules[6].AddFirst(new MatchRule(0x0000, 0x00001001, 0x0000, "G4", "K4"));
137	        blendRules[7].AddFirst(new MatchRule(0x0000, 0x00001000, 0x0000, "F9", "F11"));
138	        blendRules[8].AddFirst(new MatchRule(0x0000, 0x00000010, 0x0000, "I8", "K8"));
139	        blendRules[9].AddFirst(new MatchRule(0x0000, 0x00000010, 0x0000, "I5", "K5"));
140	        blendRules[9].AddFirst(new MatchRule(0x0000, 0x00000100, 0x0000, "L1", "L3"));
141	        blendRules[9].AddFirst(new MatchRule(0x0000, 0x00000110, 0x0000, "F3", "J3"));
142	        blendRules[10].AddFirst(new MatchRule(0x0000, 0x00000101, 0x0000, "H11", "J11"));
143	        blendRules[11].AddFirst(new MatchRule(0x0000, 0x00000100, 0x0000, "H10", "J10"));
144	        blendRules[12].AddFirst(new MatchRule(0x0000, 0x00000001, 0x0000, "L4", "L6"));
145	        blendRules[12].AddFirst(new MatchRule(0x0000, 0x00000010, 0x0000, "I6", "K6"));
146	        blendRules[12].AddFirst(new MatchRule(0x0000, 0x00000011, 0x0000, "F4", "J4"));
147	        blendRules[13].AddFirst(new MatchRule(0x0000, 0x00000010, 0x0000, "G9", "G11"));
148	        blendRules[14].AddFirst(new MatchRule(0x0000, 0x00000001, 0x0000, "H9", "J9"));
149	
150	        for (int i = 0; i < 16; i++)
151	        {
152	            grassRules[i] = new LinkedList<MatchRule>(blendRules[i]);
153	            for (int j = 0; j < baseRules[i].Count; j++)
154	            {
155	                blendRules[i].AddLast(baseRules[i].ElementAt(j));
156	            }
157	        }
158	        //These rules cause conflicts with some of the other rules during grass blending
159	        grassRules[7].RemoveFirst();
160	        grassRules[11].RemoveFirst();
161	        grassRules[13].RemoveFirst();
162	        grassRules[14].RemoveFirst();
163	        grassRules[3].RemoveFirst();
164	        grassRules[6].RemoveFirst();
165	        grassRules[9].RemoveFirst();
166	        grassRules[12].RemoveFirst();
167	
168	        blendRules[1].AddFirst(new MatchRule(0x0000, 0x00001110, 0x0000, "F13", "H13"));
169	        blendRules[2].AddFirst(new MatchRule(0x0000, 0x00001101, 0x0000, "I12", "K12"));
170	        blendRules[4].AddFirst(new MatchRule(0x0000, 0x00001011, 0x0000, "I13", "K13"));
171	        blendRules[5].AddFirst(new MatchRule(0x0000, 0x00000010, 0x0000, "B14", "B16"));
172	        blendRules[5].AddFirst(new MatchRule(0x0000, 0x00001000, 0x0000, "A14", "A16"));
173	        blendRules[8].AddFirst(new MatchRule(0x0000, 0x00000111, 0x0000, "F12", "H12"));
174	        blendRules[10].AddFirst(new MatchRule(0x0000, 0x00000001, 0x0000, "C14", "C16"));
175	        blendRules[10].AddFirst(new MatchRule(0x0000, 0x00000100, 0x0000, "D14", "D16"));
176	        blendRules[15].AddFirst(new MatchRule(0x0000, 0x00010000, 0x0000, "G1", "K1"));
177	        blendRules[15].AddFirst(new MatchRule(0x0000, 0x00100000, 0x0000, "G2", "K2"));
178	        blendRules[15].AddFirst(new MatchRule(0x0000, 0x01000000, 0x0000, "F2", "J2"));
179	        blendRules[15].AddFirst(new MatchRule(0x0000, 0x10000000, 0x0000, "F1", "J1"));
180	
181	        grassRules[1].AddLast(new MatchRule(0x0000, 0x0000, 0x00001010, 0x00000000, "P1", "R1"));
182	        grassRules[1].AddLast(new MatchRule(0x0000, 0x0000, 0x00001110, 0x00000000, "R9", "R11"));
183	        grassRules[2].AddLast(new MatchRule(0x0000, 0x0000, 0x00000101, 0x00000000, "Q3", "Q5"));
184	        grassRules[2].AddLast(new MatchRule(0x0000, 0x0000, 0x00001101, 0x00000000, "Q12", "Q14"));
185	        grassRules[3].AddLast(new MatchRule(0x0000, 0x0001, 0x00000000, 0x00010000, "Q6", "Q8"));
186	        grassRules[4].AddLast(new MatchRule(0x0000, 0x0000, 0x00001010, 0x00000000, "P2", "R2"));
187	        grassRules[4].AddLast(new MatchRule(0x0000, 0x0000, 0x00001011, 0x00000000, "R12", "R14"));
188	        grassRules[6].AddLast(new MatchRule(0x0000, 0x0010, 0x00000000, 0x00100000, "Q9", "Q11"));
189	        grassRules[7].AddLast(new MatchRule(0x0000, 0x0011, 0x00000000, 0x00111000, "O9", "O15"));
190	        grassRules[7].AddLast(new MatchRule(0x0010, 0x0001, 0x00100000, 0x00011000, "T1", "T3"));
191	        grassRules[7].AddLast(new MatchRule(0x0001, 0x0010, 0x00010000, 0x00101000, "T4", "T6"));
192	        grassRules[8].AddLast(new MatchRule(0x0000, 0x0000, 0x00000101, 0x00000000, "P3", "P5"));
193	        grassRules[8].AddLast(new MatchRule(0x0000, 0x0000, 0x00000111, 0x00000000, "P12", "P14"));
194	        grassRules[9].AddLast(new MatchRule(0x0000, 0x1000, 0x00000000, 0x10000000, "P6", "P8"));
195	        grassRules[11].AddLast(new MatchRule(0x0000, 0x1001, 0x00000000, 0x10010100, "N8", "N14"));
196	        grassRules[11].AddLast(new MatchRule(0x1000, 0x0001, 0x10000000, 0x00010100, "U1", "U3"));
197	        grassRules[11].AddLast(new MatchRule(0x0001, 0x1000, 0x00010000, 0x10000100, "U4", "U6"));
198	        grassRules[12].AddLast(new MatchRule(0x0000, 0x0100, 0x00000000, 0x01000000, "P9", "P11"));
199	        grassRules[13].AddLast(new MatchRule(0x0000, 0x1100, 0x00000000, 0x11000010, "M9", "M15"));
200	        grassRules[13].AddLast(new MatchRule(0x0100, 0x1000, 0x01000000, 0x10000010, "S1", "S3"));
201	        grassRules[13].AddLast(new MatchRule(0x1000, 0x0100, 0x10000000, 0x01000010, "S4", "S6"));
202	        grassRules[14].AddLast(new MatchRule(0x0000, 0x0110, 0x00000000, 0x01100001, "N10", "N16"));
203	        grassRules[14].AddLast(new MatchRule(0x0010, 0x0100, 0x00100000, 0x01000001, "V1", "V3"));
204	        grassRules[14].AddLast(new MatchRule(0x0100, 0x0010, 0x01000000, 0x00100001, "V4", "V6"));
205	        grassRules[15].AddLast(new MatchRule(0x0000, 0x1111, 0x00000000, 0x11110000, "N9", "N15"));
206	        grassRules[15].AddLast(new MatchRule(0x0000, 0x0111, 0x10000000, 0x01110000, "S7", "S9"));
207	        grassRules[15].AddLast(new MatchRule(0x0000, 0x1110, 0x00010000, 0x11100000, "T7", "T9"));
208	        grassRules[15].AddLast(new MatchRule(0x0000, 0x1011, 0x01000000, 0x10110000, "U7", "U9"));
209	        grassRules[15].AddLast(new MatchRule(0x0000, 0x1101, 0x00100000, 0x11010000, "V7", "V9"));
210	        grassRules[15].AddLast(new MatchRule(0x0000, 0x1010, 0x00000000, 0x10100000, "R3", "R5"));
211	        grassRules[15].AddLast(new MatchRule(0x0000, 0x0101, 0x00000000, 0x01010000, "R6", "R8"));
212	
213	        //These rules are not listed in the terrafirma guide, but are required for this system to completely work for some reason
214	        grassRules[0].AddFirst(new MatchRule(0x0000, 0x0000, 0x00001110, 0x00000001, "P2", "R2"));
215	        grassRules[0].AddFirst(new MatchRule(0x0000, 0x0000, 0x00001101, 0x00000010, "P3", "P5"));
216	        grassRules[0].AddFirst(new MatchRule(0x0000, 0x0000, 0x00001011, 0x00000100, "P1", "R1"));
217	        grassRules[0].AddFirst(new MatchRule(0x0000, 0x0000, 0x00000111, 0x00001000, "Q3", "Q5"));
218	        grassRules[1].AddFirst(new MatchRule(0x0000, 0x0000, 0x00000110, 0x00001001, "M1", "M3"));
219	        grassRules[1].AddFirst(new MatchRule(0x0000, 0x0000, 0x00001100, 0x00000011, "L1", "L3"));
220	        grassRules[2].AddFirst(new MatchRule(0x0000, 0x0000, 0x00001001, 0x00000110, "F5", "H5"));
221	        grassRules[2].AddFirst(new MatchRule(0x0000, 0x0000, 0x00001100, 0x00000011, "F6", "H6"));
222	        grassRules[3].AddFirst(new MatchRule(0x0000, 0x0001, 0x00001100, 0x00010000, "G3", "K3"));
223	        grassRules[4].AddFirst(new MatchRule(0x0000, 0x0000, 0x00000011, 0x00001100, "M4", "M6"));
224	        grassRules[4].AddFirst(new MatchRule(0x0000, 0x0000, 0x00001001, 0x00000110, "L4", "L6"));
225	        grassRules[6].AddFirst(new MatchRule(0x0000, 0x0010, 0x00001001, 0x00100000, "G4", "K4"));
226	        grassRules[7].AddLast(new MatchRule(0x0000, 0x0011, 0x00001000, 0x00110000, "B7", "B9"));
227	        grassRules[7].AddLast(new MatchRule(0x0000, 0x0001, 0x00001000, 0x00010000, "G3", "K3"));
228	        grassRules[7].AddLast(new MatchRule(0x0000, 0x0010, 0x00001000, 0x00100000, "G4", "K4"));
229	        grassRules[8].AddFirst(new MatchRule(0x0000, 0x0000, 0x00000011, 0x00001100, "I5", "K5"));
230	        grassRules[8].AddFirst(new MatchRule(0x0000, 0x0000, 0x00000110, 0x00001001, "I6", "K6"));
231	        grassRules[9].AddFirst(new MatchRule(0x0000, 0x1000, 0x00000110, 0x10000000, "F3", "J3"));
232	        grassRules[11].AddLast(new MatchRule(0x0000, 0x1001, 0x00000100, 0x10010000, "A12", "C12"));
233	        grassRules[11].AddLast(new MatchRule(0x0000, 0x0001, 0x00000100, 0x00010000, "G3", "K3"));
234	        grassRules[11].AddLast(new MatchRule(0x0000, 0x1000, 0x00000100, 0x10000000, "F3", "J3"));
235	        grassRules[12].AddFirst(new MatchRule(0x0000, 0x0100, 0x00000011, 0x01000000, "F4", "J4"));
236	        grassRules[13].AddLast(new MatchRule(0x0000, 0x1100, 0x00000010, 0x11000000, "C7", "C9"));
237	        grassRules[13].AddLast(new MatchRule(0x0000, 0x0100, 0x00000010, 0x01000000, "F4", "J4"));
238	        grassRules[13].AddLast(new MatchRule(0x0000, 0x1000, 0x00000010, 0x10000000, "F3", "J3"));
239	        grassRules[14].AddLast(new MatchRule(0x0000, 0x0110, 0x00000001, 0x01100000, "A11", "C11"));
240	        grassRules[14].AddLast(new MatchRule(0x0000, 0x0010, 0x00000001, 0x00100000, "G4", "K4"));
241	        grassRules[14].AddLast(new MatchRule(0x0000, 0x0100, 0x00000001, 0x01000000, "F4", "J4"));
242	        grassRules[15].AddLast(new MatchRule(0x0000, 0x0011, 0x00000000, 0x00110000, "B7", "B9"));
243	        grassRules[15].AddLast(new MatchRule(0x0000, 0x1100, 0x00000000, 0x11000000, "C7", "C9"));
244	        grassRules[15].AddLast(new MatchRule(0x0000, 0x0110, 0x00000000, 0x01100000, "A11", "C11"));
245	        grassRules[15].AddLast(new MatchRule(0x0000, 0x1001, 0x00000000, 0x10010000, "A12", "C12"));
246	        grassRules[15].AddLast(new MatchRule(0x0000, 0x0001, 0x00000000, 0x00010000, "G3", "K3"));
247	        grassRules[15].AddLast(new MatchRule(0x0000, 0x0010, 0x00000000, 0x00100000, "G4", "K4"));
248	        grassRules[15].AddLast(new MatchRule(0x0000, 0x0100, 0x00000000, 0x01000000, "F4", "J4"));
249	        grassRules[15].AddLast(new MatchRule(0x0000, 0x1000, 0x00000000, 0x10000000, "F3", "J3"));
250	    }
251	
252	    //Given a set of masks and a strictness, follow the rules until the proper UV is obtained
253	    public Vector2Int32 GetUVForMasks(uint neighborMask, uint blendMask, int ruleStrictness)
254	    {
255	        return GetUVForMasks(neighborMask, blendMask, ruleStrictness, randomVariation.Next(3));
256	    }
257	
258	    //Overload with deterministic variant selection (0-2) instead of random.
259	    //UVPosSet has 3 entries (indices 0-2). Terraria's TileFrameCosmetic uses switch with case 0, case 1,
260	    //and default — so phlebas/lazure values 2 and 3 both map to the third variant (index 2).
261	    public Vector2Int32 GetUVForMasks(uint neighborMask, uint blendMask, int ruleStrictness, int variant)
262	    {
263	        int bucketId = (int)(((neighborMask & 0x00001000) >> 9) + ((neighborMask & 0x00000100) >> 6) + ((neighborMask & 0x00000010) >> 3) + (neighborMask & 0x00000001));
264	        int variationId = Math.Min(variant, 2);
265	        switch (ruleStrictness)
266	        {
267	            case 0:
268	                foreach (MatchRule rule in baseRules[bucketId])
269	                {
270	                    if (rule.Matches(neighborMask, blendMask))
271	                    {
272	                        return rule.UVPosSet[variationId];
273	                    }
274	                }
275	                break;
276	            case 1:
277	                foreach (MatchRule rule in blendRules[bucketId])
278	                {
279	                    if (rule.Matches(neighborMask, blendMask))
280	                    {
281	                        return rule.UVPosSet[variationId];
282	                    }
283	                }
284	                break;
285	            case 2:
286	                foreach (MatchRule rule in grassRules[bucketId])
287	                {
288	                    if (rule.MatchesRelaxed(neighborMask, blendMask)) //Constraints behave slightly differently for grass tiles
289	                    {
290	                        return rule.UVPosSet[variationId];
291	                    }
292	                }
293	                //Only get here if there were no unique grass rules.  As a result, reduce the constraints even more
294	                neighborMask |= blendMask;
295	                bucketId = (int)(((neighborMask & 0x00001000) >> 9) + ((neighborMask & 0x00000100) >> 6) + ((neighborMask & 0x00000010) >> 3) + (neighborMask & 0x00000001));
296	                foreach (MatchRule rule in baseRules[bucketId])
297	                {
298	                    if (rule.Matches(neighborMask, blendMask))
299	                    {
300	                        return rule.UVPosSet[variationId];
301	                    }
302	                }
303	                break;
304	        }
305	        return new Vector2Int32(0, 0);
306	    }
307	
308	    //This function resets the UV state for the specified tile locations (as well as nearby tiles) such that the UV cache must be re-evaluated
309	    public static void ResetUVCache(WorldViewModel _wvm, int tileStartX, int tileStartY, int regionWidth, int regionHeight) =>
310	        ResetUVCache(_wvm.CurrentWorld, _wvm.TilePicker, tileStartX, tileStartY, regionWidth, regionHeight);
311	
312	    public static void ResetUVCache(World world, IReadOnlyList<Vector2Int32> tiles)
313	    {
314	        int tilesWide = world.TilesWide;
315	        int tilesHigh = world.TilesHigh;
316	
317	        // Reset UV cache for each tile and its neighbors
318	        foreach (var tile in tiles)
319	        {
320	            for (int x = tile.X - 1; x <= tile.X + 1; x++)
321	            {
322	                for (int y = tile.Y - 1; y <= tile.Y + 1; y++)
323	                {
324	                    if (x < 0 || y < 0 || x >= tilesWide || y >= tilesHigh)
325	                        continue;
326	
327	                    ref Tile curtile = ref world.Tiles[x, y];
328	                    curtile.uvTileCache = 0xFFFF;
329	                    curtile.lazyMergeId = 0xFF;
330	                    curtile.hasLazyChecked = false;
331	                    curtile.uvWallCache = 0xFFFF;
332	                }
333	            }
334	        }
335	    }
336	
337	    public static void ResetUVCache(
338	        World world,
339	        TilePicker tilePicker,
340	        int tileStartX,
341	        int tileStartY,
342	        int regionWidth,
343	        int regionHeight)
344	    {
345	        // Always reset UV cache when tiles are modified, regardless of paint mode.
346	        // Callers like SpritePlacer, undo/redo, and plugins can modify tiles outside
347	        // TileAndWall mode; skipping the reset causes stale connected texture state.
348	        for (int x = -1; x < regionWidth + 1; x++)
349	        {
350	            int tilex = x + tileStartX;
351	            for (int y = -1; y < regionHeight + 1; y++)
352	            {
353	                int tiley = y + tileStartY;
354	                if (tilex < 0 || tiley < 0 || tilex >= world.TilesWide || tiley >= world.TilesHigh)
355	                {
356	                    continue;
357	                }
358	                ref Tile curtile = ref world.Tiles[tilex, tiley];
359	                curtile.uvTileCache = 0xFFFF;
360	                curtile.lazyMergeId = 0xFF;
361	                curtile.hasLazyChecked = false;
362	                curtile.uvWallCache = 0xFFFF;
363	            }
364	        }
365	    }
366	}
367	
368	class MatchRule
369	{
370	    //Corner order -> 0x0001 = Top Right, 0x0010 = Top Left, 0x0100 = Bottom Left, 0x1000 = Bottom Right
371	    //Edge order -> 0x0001 = Right (East), 0x0010 = Above (North), 0x0100 = Left (West), 0x1000 = Below (South)
372	    private int cornerInclusionMask = 0; //Specifies which corner tiles MUST match a given tile's type using the "corner order" above
373	    private int cornerExclusionMask = 0; //Specifies which corner tile must NOT match a given tile's type using the "corner order" above
374	    private long blendInclusionMask = 0; //When merging a tile to another (e.g. stone and dirt,) these tiles MUST match the merge type - 0xFFFF0000 refers to the "corner order" above, 0x0000FFFF refers to the "edge order" above
375	    private long blendExclusionMask = 0; //When merging a tile to another (e.g. stone and dirt,) these tiles must NOT match the merge type - 0xFFFF0000 refers to the "corner order" above, 0x0000FFFF refers to the "edge order" above
376	    private Vector2Int32[] uvPos; //A set of UV positions, each representing a possible variation of the rule's final position
377	
378	    public MatchRule(int cornerExclusionMask, string tileStart, string tileEnd)
379	    {
380	        this.cornerExclusionMask = cornerExclusionMask;
381	        SetUVsForString(tileStart, tileEnd);
382	    }
383	
384	    public MatchRule(int cornerExclusionMask, long blendInclusionMask, int blendCornerExclusionMask, string tileStart, string tileEnd)
385	    {
386	        this.cornerExclusionMask = cornerExclusionMask;
387	        this.blendInclusionMask = blendInclusionMask;
388	        blendExclusionMask = blendCornerExclusionMask << 16;
389	        SetUVsForString(tileStart, tileEnd);
390	    }
391	
392	    public MatchRule(int cornerInclusionMask, int cornerExclusionMask, long blendInclusionMask, long blendExclusionMask, string tileStart, string tileEnd)
393	    {
394	        this.cornerInclusionMask = cornerInclusionMask;
395	        this.cornerExclusionMask = cornerExclusionMask;
396	        this.blendInclusionMask = blendInclusionMask;
397	        this.blendExclusionMask = blendExclusionMask;
398	        SetUVsForString(tileStart, tileEnd);
399	    }
400	
401	    //tileStart and tileEnd use the "A1" notation based on the pictoral representation of tiles in http://seancode.com/terrafirma/uvs.html
402	    //Note that http://seancode.com/terrafirma/uvs.html does not list "N" as a possible row, but the rules used here do (and have been adjusted accordingly)
403	    private void SetUVsForString(string tileStart, string tileEnd)
404	    {
405	        uvPos = new Vector2Int32[3];
406	        int y1 = tileStart[0] - 'A';
407	        int x1 = Convert.ToInt32(tileStart.Substring(1)) - 1;
408	        int y2 = tileEnd[0] - 'A';
409	        int x2 = Convert.ToInt32(tileEnd.Substring(1)) - 1;
410	        int y3 = y2 - (y2 - y1) / 2;
411	        int x3 = x2 - (x2 - x1) / 2;
412	        uvPos[0] = new Vector2Int32(x1, y1);
413	        uvPos[1] = new Vector2Int32(x3, y3);
414	        uvPos[2] = new Vector2Int32(x2, y2);
415	    }
416	
417	    //Works a "bit" of bit-magic to validate rules
418	    public bool Matches(long neighborMask, long blendMask)
419	    {
420	        long upperCornerInclusionMask = cornerInclusionMask << 16 & 0x11110000;
421	        if ((upperCornerInclusionMask & neighborMask) != upperCornerInclusionMask)
422	        {
423	            return false;
424	        }
425	        long upperCornerExclusionMask = cornerExclusionMask << 16 & 0x11110000;
426	        if (upperCornerExclusionMask != 0 && (upperCornerExclusionMask & neighborMask) != 0x00000000)
427	        {
428	            return false;
429	        }
430	        long lowerBlendInclusionMask = blendInclusionMask & 0x00001111;
431	        if (lowerBlendInclusionMask != 0 && (lowerBlendInclusionMask ^ blendMask & 0x00001111) != 0x00000000)
432	        {
433	            return false;
434	        }
435	        long upperBlendCornerInclusionMask = blendInclusionMask & 0x11110000;
436	        if ((upperBlendCornerInclusionMask & blendMask) != upperBlendCornerInclusionMask)
437	        {
438	            return false;
439	        }
440	        long lowerBlendExclusionMask = blendExclusionMask & 0x00001111;
441	        if ((lowerBlendExclusionMask & blendMask) != 0x00000000)
442	        {
443	            return false;
444	        }
445	        long upperBlendCornerExclusionMask = blendExclusionMask & 0x11110000;
446	        if (upperBlendCornerExclusionMask != 0 && (upperBlendCornerExclusionMask & blendMask) != 0x00000000)
447	        {
448	            return false;
449	        }
450	        return true;
451	    }
452	
453	    //Same as above, inclusion masks are OR'd together on a bit-by-bit basis
454	    public bool MatchesRelaxed(long neighborMask, long blendMask)
455	    {
456	        long column = 0x00010000;
457	        for (int i = 0; i < 4; i++)
458	        {
459	            long upperCornerInclusionMask = cornerInclusionMask << 16 & column;
460	            long upperBlendCornerInclusionMask = blendInclusionMask & column;
461	            if ((upperCornerInclusionMask & upperBlendCornerInclusionMask) == 0x00000000)
462	            {
463	                if (upperCornerInclusionMask != 0 && (upperCornerInclusionMask & neighborMask) == 0)
464	                {
465	                    return false;
466	                }
467	                if (upperBlendCornerInclusionMask != 0 && (upperBlendCornerInclusionMask & blendMask) == 0)
468	                {
469	                    return false;
470	                }
471	            }
472	            else
473	            {
474	                if ((upperCornerInclusionMask & neighborMask) == 0 && (upperBlendCornerInclusionMask & blendMask) == 0)
475	                {
476	                    return false;
477	                }
478	            }
479	            if (i < 3)
480	            {
481	                column <<= 4;
482	            }
483	        }
484	        long upperCornerExclusionMask = cornerExclusionMask << 16 & 0x11110000;
485	        if (upperCornerExclusionMask != 0 && (upperCornerExclusionMask & neighborMask) != 0x00000000)
486	        {
487	            return false;
488	        }
489	        long lowerBlendInclusionMask = blendInclusionMask & 0x00001111;
490	        if (lowerBlendInclusionMask != 0 && (lowerBlendInclusionMask ^ blendMask & 0x00001111) != 0x00000000)
491	        {
492	            return false;
493	        }
494	        long lowerBlendExclusionMask = blendExclusionMask & 0x00001111;
495	        if ((lowerBlendExclusionMask & blendMask) != 0x00000000)
496	        {
497	            return false;
498	        }
499	        long upperBlendCornerExclusionMask = blendExclusionMask & 0x11110000;
500	        if (upperBlendCornerExclusionMask != 0 && (upperBlendCornerExclusionMask & blendMask) != 0x00000000)
501	        {
502	            return false;
503	        }
504	        return true;
505	    }
506	
507	    public Vector2Int32[] UVPosSet
508	    {
509	        get { return uvPos; }
510	    }
511	}
512	

```


---

## 🤖 Assistant · 2026-08-07T07:06:28.668Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Excellent — I have the full BlendRules. Now for the TEdit grass question: which tile types count as "same" for grass. In the renderer, the "Everything else" branch uses tileprop.Merges(...) and same-type. For grass, IsGrass sets strictness=2. And TileProperty.MergeWith defines the merge partner. Let me check the tiles settings JSON for grass entries — what MergeWith values grass types have. Search for settings files with "MergeWith".

Also lines 300-360 in WorldRenderXna.xaml.cs (the switch with grass IDs 60, 23, 199, 203, 109, 70) — what is that? Let me read. Also line 137 comment. Those may be for vine rendering or "grass on trees". Let me check.

Also check TileProperty.cs 100-180 for the full Merges logic.

And how the grass sheet rows map: cell notation "A1".."V9" — rows A-V (22 rows!) — the user said "110 rows in Tiles_2" but the BlendRules grid is 22 rows (A..V) × 16 cols? Actually x1 = number-1 so columns up to 16, rows A-V = 22 rows. Hmm — the UV returned is (col, row) in tile units. For grass tile (Tiles_2), row A=0..V=21. The user's "110 rows" may refer to the actual texture Tiles_2.png height in TEdit? Let me check the texture or any reference to "110". Not critical but let me grep quickly for 110 or "Tiles_2".

Let me do these in parallel:
1. Read renderer lines 120-150 and 290-360.
2. Read TileProperty.cs 100-180.
3. grep MergeWith in settings json files.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:06:29.437Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor && grep -rn \"MergeWith\" --include=\"*.json\" . | head -30; echo \"=== settings dirs ===\"; find . -name \"tiles.json\" -o -name \"*Tiles*.json\" | head",
 "description": "Find MergeWith settings for tiles"
}
```


---

## 🤖 Assistant · 2026-08-07T07:06:29.453Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor && sed -n '120,150p' src/TEdit/View/WorldRenderXna.xaml.cs; echo \"==== 290-360 ====\"; sed -n '290,360p' src/TEdit/View/WorldRenderXna.xaml.cs",
 "description": "Read grass-related switches in renderer"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:06:29.501Z

**📎 ToolResult**

```
    private float _zoom = 1;
    private Size? _exportViewSize;
    private bool _isExporting;
    private float _exportOverallPercent;
    private float _exportLayerPercent;
    private string _exportOverallText = "";
    private string _exportLayerText = "";
    private Texture2D? _exportWhitePixel;
    private CancellationTokenSource? _exportCts;
    private Rectangle _exportCancelButtonRect;
    private float _minNpcScale = 0.75f;

    private Dictionary<int, WriteableBitmap> _spritePreviews = new Dictionary<int, WriteableBitmap>();

    // Vine tile IDs that need -2px Y offset and horizontal flip on alternating X
    private static readonly HashSet<int> _vineTileIds = new HashSet<int> { 52, 62, 115, 205, 382, 528, 636, 638 };

    // Grass/plant tiles that need horizontal flip on alternating X (includes vines)
    // Reference: docs/custom-rendered-tiles.md Section 5
    private static readonly HashSet<int> _spriteFlipTileIds = new HashSet<int>
    {
        3, 20, 24, 52, 61, 62, 71, 73, 74, 81, 82, 83, 84, 110, 113, 115, 127,
        201, 205, 227, 270, 271, 382, 528, 572, 581, 590, 595, 636, 637, 638, 703
    };

    // Selected chest position cache - used to render the selected chest as "open"
    // Set to (-1, -1) when no chest is selected
    private Vector2Int32 _selectedChestPosition = new Vector2Int32(-1, -1);

    // Gem tree tile IDs (583-589): Topaz, Amethyst, Sapphire, Emerald, Ruby, Diamond, Amber
    // These render like normal trees but with fixed texture indices 22-28
==== 290-360 ====
        var world = _wvm.CurrentWorld;

        // Ocean: at world edges (within ~380 tiles)
        int oceanDistance = 380;
        if (x < oceanDistance || x > world.TilesWide - oceanDistance)
        {
            return SurfaceBiome.Ocean;
        }

        // Sample tiles vertically from visible top down to ground level
        int startY = Math.Max(0, visibleBounds.Top);
        int endY = Math.Min(world.TilesHigh - 1, (int)world.GroundLevel + 10);

        for (int checkY = startY; checkY <= endY; checkY++)
        {
            if (x < 0 || x >= world.TilesWide) continue;
            var tile = world.Tiles[x, checkY];
            if (!tile.IsActive) continue;

            switch (tile.Type)
            {
                // Snow biome tiles (check first - ice variants overlap with evil biomes)
                case 147: // Ice
                case 161: // Snow Block
                    return SurfaceBiome.Snow;

                // Jungle biome tiles
                case 60:  // Jungle Grass
                case 226: // Lihzahrd Brick
                    return SurfaceBiome.Jungle;

                // Desert biome tiles
                case 53:  // Sand
                    return SurfaceBiome.Desert;

                // Corruption biome tiles
                case 23:  // Corrupt Grass
                case 25:  // Ebonstone
                case 112: // Ebonsand
                case 163: // Purple Ice
                    return SurfaceBiome.Corruption;

                // Crimson biome tiles
                case 199: // Crimson Grass
                case 203: // Crimson Grass (alternate ID)
                case 200: // Red Ice
                case 208: // Crimstone
                case 234: // Crimsand
                    return SurfaceBiome.Crimson;

                // Hallow biome tiles
                case 109: // Hallowed Grass
                case 117: // Pearlstone
                case 116: // Pearlsand
                case 164: // Pink Ice
                    return SurfaceBiome.Hallow;

                // Mushroom biome tiles
                case 70:  // Mushroom Grass
                case 190: // Glowing Mushroom Block
                    return SurfaceBiome.Mushroom;
            }
        }

        // Default: Forest
        return SurfaceBiome.Forest;
    }

    /// <summary>
    /// Gets the full background style for a detected biome and X position.
    /// </summary>

```


---

## 👤 User(sidechain) · 2026-08-07T07:06:29.517Z

**📎 ToolResult**

```
=== settings dirs ===
./tiles.json
./src/TEdit.Terraria/Data/tiles.json

```


---

## 🤖 Assistant · 2026-08-07T07:06:32.437Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The 290-360 switch is biome detection, not grass framing. Good to note.

Now check tiles.json for grass MergeWith entries, and TileProperty.cs Merges(). Let me grep tiles.json for grass types 2, 23, 60, 70, 109, 199 with MergeWith.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:06:32.777Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor && python3 - <<'EOF'\nimport json\nd=json.load(open('src/TEdit.Terraria/Data/tiles.json'))\nprint(type(d), list(d)[:8] if isinstance(d,dict) else len(d))\nEOF",
 "description": "Inspect tiles.json structure"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:06:40.310Z

**📎 ToolResult**

```
<class 'list'> 753

```


---

## 🤖 Assistant · 2026-08-07T07:06:42.691Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor && python3 - <<'EOF'\nimport json\nd=json.load(open('src/TEdit.Terraria/Data/tiles.json'))\nfor t in d:\n    if t.get('Id') in (0,1,2,23,59,60,70,109,199,477,492,57,58,75,76,147,161,163,164,200,202,191,189,196,226):\n        print({k:t.get(k) for k in ('Id','Name','IsGrass','IsStone','MergeWith','CanBlend','IsSolid','IsFramed')})\nEOF",
 "description": "Dump merge-related tile properties"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:06:47.264Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-07T07:06:51.513Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor && python3 -c \"\nimport json\nd=json.load(open('src/TEdit.Terraria/Data/tiles.json'))\nprint(json.dumps(d[0], indent=1))\nprint(json.dumps(d[2], indent=1))\n\"",
 "description": "Inspect tiles.json entries"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:06:57.436Z

**📎 ToolResult**

```
{
 "id": 0,
 "isSolid": true,
 "canBlend": true,
 "textureGrid": [
  16,
  16
 ],
 "frameGap": [
  2,
  2
 ],
 "frameSize": [
  [
   1,
   1
  ]
 ],
 "name": "Dirt Block",
 "key": "Dirt",
 "color": "#976B4BFF"
}
{
 "id": 2,
 "isSolid": true,
 "isGrass": true,
 "canBlend": true,
 "mergeWith": 0,
 "textureGrid": [
  16,
  16
 ],
 "frameGap": [
  2,
  2
 ],
 "frameSize": [
  [
   1,
   1
  ]
 ],
 "name": "Grass Block",
 "key": "Grass",
 "color": "#1CD85EFF",
 "special": "Grass"
}

```


---

## 🤖 Assistant · 2026-08-07T07:06:59.261Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now dump grass family entries with mergeWith.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:06:59.970Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor && python3 -c \"\nimport json\nd=json.load(open('src/TEdit.Terraria/Data/tiles.json'))\nfor t in d:\n    if t.get('id') in (0,1,2,23,59,60,70,109,199,477,492,57,58,75,76,147,161,163,164,200,202,191,189,196,226,53,112,116,117,199,203,208,234,25,117):\n        print({k:t.get(k) for k in ('id','name','isGrass','isStone','mergeWith','canBlend','special')})\n\"",
 "description": "Dump grass family merge settings"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:07:05.893Z

**📎 ToolResult**

```
{'id': 0, 'name': 'Dirt Block', 'isGrass': None, 'isStone': None, 'mergeWith': None, 'canBlend': True, 'special': None}
{'id': 1, 'name': 'Stone Block', 'isGrass': None, 'isStone': True, 'mergeWith': 0, 'canBlend': True, 'special': None}
{'id': 2, 'name': 'Grass Block', 'isGrass': True, 'isStone': None, 'mergeWith': 0, 'canBlend': True, 'special': 'Grass'}
{'id': 23, 'name': 'Corrupt Grass Block', 'isGrass': True, 'isStone': None, 'mergeWith': 0, 'canBlend': True, 'special': 'Grass'}
{'id': 25, 'name': 'Ebonstone Block', 'isGrass': None, 'isStone': True, 'mergeWith': 0, 'canBlend': True, 'special': None}
{'id': 53, 'name': 'Sand Block', 'isGrass': None, 'isStone': None, 'mergeWith': 0, 'canBlend': True, 'special': None}
{'id': 57, 'name': 'Ash Block', 'isGrass': None, 'isStone': None, 'mergeWith': None, 'canBlend': True, 'special': None}
{'id': 58, 'name': 'Hellstone Ore', 'isGrass': None, 'isStone': None, 'mergeWith': 57, 'canBlend': True, 'special': None}
{'id': 59, 'name': 'Mud Block', 'isGrass': None, 'isStone': None, 'mergeWith': 0, 'canBlend': True, 'special': None}
{'id': 60, 'name': 'Jungle Grass Block', 'isGrass': True, 'isStone': None, 'mergeWith': 59, 'canBlend': True, 'special': 'Grass'}
{'id': 70, 'name': 'Mushroom Grass Block', 'isGrass': True, 'isStone': None, 'mergeWith': 59, 'canBlend': True, 'special': 'Grass'}
{'id': 75, 'name': 'Obsidian Brick', 'isGrass': None, 'isStone': None, 'mergeWith': None, 'canBlend': True, 'special': None}
{'id': 76, 'name': 'Hellstone Brick', 'isGrass': None, 'isStone': None, 'mergeWith': None, 'canBlend': True, 'special': None}
{'id': 109, 'name': 'Hallowed Grass Block', 'isGrass': True, 'isStone': None, 'mergeWith': 0, 'canBlend': True, 'special': 'Grass'}
{'id': 112, 'name': 'Ebonsand Block', 'isGrass': None, 'isStone': None, 'mergeWith': 0, 'canBlend': True, 'special': None}
{'id': 116, 'name': 'Pearlsand Block', 'isGrass': None, 'isStone': None, 'mergeWith': 0, 'canBlend': True, 'special': None}
{'id': 117, 'name': 'Pearlstone Block', 'isGrass': None, 'isStone': True, 'mergeWith': 0, 'canBlend': True, 'special': None}
{'id': 147, 'name': 'Snow Block', 'isGrass': None, 'isStone': None, 'mergeWith': None, 'canBlend': True, 'special': None}
{'id': 161, 'name': 'Ice Block', 'isGrass': None, 'isStone': None, 'mergeWith': None, 'canBlend': True, 'special': None}
{'id': 163, 'name': 'Purple Ice Block', 'isGrass': None, 'isStone': None, 'mergeWith': None, 'canBlend': True, 'special': None}
{'id': 164, 'name': 'Pink Ice Block', 'isGrass': None, 'isStone': None, 'mergeWith': None, 'canBlend': True, 'special': None}
{'id': 189, 'name': 'Cloud Block', 'isGrass': None, 'isStone': None, 'mergeWith': None, 'canBlend': True, 'special': None}
{'id': 191, 'name': 'Living Wood Block', 'isGrass': None, 'isStone': None, 'mergeWith': None, 'canBlend': True, 'special': None}
{'id': 196, 'name': 'Rain Cloud Block', 'isGrass': None, 'isStone': None, 'mergeWith': None, 'canBlend': True, 'special': None}
{'id': 199, 'name': 'Crimson Grass Block', 'isGrass': True, 'isStone': None, 'mergeWith': 0, 'canBlend': True, 'special': 'Grass'}
{'id': 200, 'name': 'Red Ice Block', 'isGrass': None, 'isStone': None, 'mergeWith': None, 'canBlend': True, 'special': None}
{'id': 202, 'name': 'Sunplate Block', 'isGrass': None, 'isStone': None, 'mergeWith': 0, 'canBlend': True, 'special': None}
{'id': 203, 'name': 'Crimstone Block', 'isGrass': None, 'isStone': True, 'mergeWith': 0, 'canBlend': True, 'special': None}
{'id': 208, 'name': 'Shadewood', 'isGrass': None, 'isStone': None, 'mergeWith': 0, 'canBlend': True, 'special': None}
{'id': 226, 'name': 'Lihzahrd Brick', 'isGrass': None, 'isStone': None, 'mergeWith': None, 'canBlend': True, 'special': None}
{'id': 234, 'name': 'Crimsand Block', 'isGrass': None, 'isStone': None, 'mergeWith': 0, 'canBlend': True, 'special': None}
{'id': 477, 'name': 'Mowed Grass Block', 'isGrass': True, 'isStone': None, 'mergeWith': 0, 'canBlend': True, 'special': None}
{'id': 492, 'name': 'Hallowed Mowed Grass Block', 'isGrass': True, 'isStone': None, 'mergeWith': 0, 'canBlend': True, 'special': 'Grass'}

```


---

## 🤖 Assistant · 2026-08-07T07:07:13.564Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have TEdit's grass merge data. Now read TileProperty.cs Merges() fully (lines 115-180), and the docs file docs/custom-rendered-tiles.md maybe mentions grass rows (110 rows). Let me check quickly for "110" in docs and the texture size of Tiles_2. Let me also verify where the grass texture row range comes from: the grassRules cells "P1".."V9" → rows P..V = rows 15..21 (0-based), columns 1..16. Hmm, actually with tileStart "P1", y1 = 'P'-'A' = 15. So grass merge frames live in rows 15-21 of the tile texture grid? But the user says 110 rows. Let me grep for "110" in TEdit src/docs.

Also verify the grass textures in TEdit: maybe Tiles_2 grass texture has 22 rows × 16 cols grid = 22 rows only. The "110" might come from elsewhere (e.g., the actual vanilla Tiles_2.png is 224 x 2240 px → 2240/18 = 124 rows?). Let me grep.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:07:14.041Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor && grep -rn \"110\" docs/*.md 2>/dev/null | head -10; echo \"=== docs list ===\"; ls docs 2>/dev/null | head -30; echo \"=== grass in docs ===\"; grep -rln \"grass\\|Grass\" docs 2>/dev/null | head",
 "description": "Check docs for grass row references"
}
```


---

## 🤖 Assistant · 2026-08-07T07:07:14.058Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor && sed -n '110,185p' src/TEdit.Terraria/Objects/TileProperty.cs",
 "description": "Read TileProperty merge members"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:07:14.088Z

**📎 ToolResult**

```
    public List<FrameProperty>? Frames { get; set; }
    public Vector2Short[]? FrameSize { get; set; } = [new Vector2Short(1, 1)];

    /// <summary>Mod name prefix (before ':') or empty for vanilla tiles.</summary>
    [JsonIgnore]
    public string ModName => Name.Contains(':') ? Name[..Name.IndexOf(':')] : string.Empty;

    /// <summary>Short display name (after ':') or full Name for vanilla tiles.</summary>
    [JsonIgnore]
    public string ShortName => Name.Contains(':') ? Name[(Name.IndexOf(':') + 1)..] : Name;

    public bool IsFramed { get; set; }
    public bool IsGrass { get; set; }
    public bool IsPlatform { get; set; }
    public bool IsCactus { get; set; }
    public bool IsStone { get; set; }
    public bool CanBlend { get; set; }
    public int? MergeWith { get; set; }
    public string? FrameNameSuffix { get; set; }
    public TextureWrap? TextureWrap { get; set; }
    public byte LargeFrameType { get; set; } = 0;

    /// <summary>
    /// Activates code-driven tree rendering pipeline for tree-type tiles.
    /// When set, the preview system uses tree-specific texture assembly (tops, branches, trunks)
    /// instead of standard frame-based preview.
    /// </summary>
    [JsonConverter(typeof(JsonStringEnumConverter))]
    public TreeMode TreeMode { get; set; } = TreeMode.None;

    /// <summary>
    /// Biome variants for tiles that automatically adapt based on biome (e.g., palm trees).
    /// When present, enables biome dropdown in sprite picker for preview selection.
    /// </summary>
    public List<BiomeVariant>? BiomeVariants { get; set; }

    /// <summary>
    /// Half-width and half-height (in tiles) of the buff detection zone centered on this tile.
    /// Null if the tile does not grant a passive buff.
    /// </summary>
    public Vector2Short? BuffRadius { get; set; }

    /// <summary>
    /// Display name of the buff granted by this tile (e.g., "Cozy Fire", "Heart Lamp").
    /// </summary>
    public string? BuffName { get; set; }

    /// <summary>
    /// RGBA overlay color used to render the buff radius visualisation.
    /// </summary>
    public TEditColor? BuffColor { get; set; }

    public bool Merges(int other)
    {
        if (other == this.Id) return true;

        if (!MergeWith.HasValue) return false;

        return MergeWith.Value == other;
    }

    public bool Merges(TileProperty other)
    {
        if (other.MergeWith.HasValue && other.MergeWith.Value == Id) return true;
        if (MergeWith.HasValue && MergeWith.Value == other.Id) return true;
        if (MergeWith.HasValue && other.MergeWith.HasValue && MergeWith.Value == other.MergeWith.Value) return true;

        return false;
    }

    public int GetFrameSizeIndex(short v)
    {
        if (FrameSize == null || FrameSize.Length <= 1)
            return 0;

        int row = v / TextureGrid.Y;

```


---

## 👤 User(sidechain) · 2026-08-07T07:07:14.108Z

**📎 ToolResult**

```
=== docs list ===
architecture
completed
Icons
images
settings.xml
TerrariaVersionTileData.json
todo
world-generation-api.md
=== grass in docs ===
docs/world-generation-api.md
docs/settings.xml
docs/completed/platform-and-connected-texture-rendering.md
docs/completed/todo-render-updates.md
docs/architecture/custom-rendered-tiles.md
docs/architecture/morph-biome-conversion.md
docs/todo/morph-tool.md
docs/architecture/tree-style-mapping.md
docs/todo/biome-tile-catalog.md

```


---

## 🤖 Assistant · 2026-08-07T07:07:19.379Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have nearly everything. A couple of remaining details:

1. The docs/architecture/custom-rendered-tiles.md may describe grass rendering and the "110 rows". Let me grep for grass rows info there.

2. In the renderer, for grass, what about the "sameStyle" branch selection: grass (IsGrass, MergeWith=0) goes to the "Everything else" branch: `sameStyle |= ... tileprop.Merges(neighbor) ...` plus same-type; mergeMask when MergeWith > -1 (grass MergeWith=0) → mergeMask bits where neighbor type == 0 (dirt). strictness=2 for grass. Good.

3. Confirm where neighborTile array is set (e/n/w/s/ne/nw/sw/se) — around line 5640ish? Not crucial, but I can mention. Let me find where neighborTile is populated to give line numbers.

4. Also check whether grass gets a special texture sheet row handling at draw time (the source rectangle uses uvTileCache directly with the texture). For grass the UV from grassRules can be rows up to 'V' (21). The texture must be padded. Let me check _textureDictionary.GetTile and any padding for grass textures. Quick grep for "PaddedTextures" or check where Tiles textures are loaded/padded.

Let me check docs for grass rows and grep neighborTile population.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:07:20.158Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor && grep -n \"grass\\|Grass\" docs/architecture/custom-rendered-tiles.md | head -20; echo \"=== neighborTile population ===\"; grep -n \"neighborTile\\[\" src/TEdit/View/WorldRenderXna.xaml.cs | awk -F: '$1<5700' | head",
 "description": "Check grass docs and neighborTile setup"
}
```


---

## 🤖 Assistant · 2026-08-07T07:07:20.177Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor && grep -rn \"grass\" docs/completed/platform-and-connected-texture-rendering.md | head -20",
 "description": "Check connected texture docs for grass"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:07:39.413Z

**📎 ToolResult**

```
21:| 5 | [Grass & Plant Rendering](#5-grass--plant-rendering) | `BASE TILE` `ANIMATION` |
61:- **TileCounterType**: Special tiles are categorized for batch processing (trees, vines, grass, etc.)
98:   - Level 2: Grass-type strict blending
109:| 2 | Grass Block | `IsGrass=true` |
115:| 23 | Corrupt Grass | |
133:| 60 | Jungle Grass | |
135:| 70 | Mushroom Grass | |
140:| 109 | Hallowed Grass | |
173:| 203 | Crimson Grass | |
201:The tree biome is determined by scanning downward from the tree position to find the controlling grass type:
206:    // Scan downward to find grass beneath tree
207:    // Returns biome style 0-6+ based on grass type found
247:| Biome | Tree_Tops Index | Grass Type Below | Depends On |
249:| Forest | 0/6/7/8/9/10 | Normal Grass (2) | `TreeStyle0-3` (zone-based via `TreeX0-2`) |
250:| Corruption | 1 | Corrupt Grass (23) | Fixed |
251:| Jungle | 2 or 11 | Jungle Grass (60) | `BgJungle` (0→2, 1→11) |
252:| Hallow | 3 | Hallowed Grass (109) | Fixed |
254:| Crimson | 5 | Crimson Grass (199) | Fixed |
255:| Underground Jungle | 13 | Jungle Grass (60, underground) | Fixed |
256:| Mushroom | 14 | Mushroom Grass (70) | Fixed |
=== neighborTile population ===
4230:                    neighborTile[e] = (x + 1) < width ? _wvm.CurrentWorld.Tiles[x + 1, y] : null;
4231:                    neighborTile[n] = (y - 1) >= 0 ? _wvm.CurrentWorld.Tiles[x, y - 1] : null;
4232:                    neighborTile[w] = (x - 1) >= 0 ? _wvm.CurrentWorld.Tiles[x - 1, y] : null;
4233:                    neighborTile[s] = (y + 1) < height ? _wvm.CurrentWorld.Tiles[x, y + 1] : null;
4234:                    neighborTile[ne] = (x + 1) < width && (y - 1) >= 0 ? _wvm.CurrentWorld.Tiles[x + 1, y - 1] : null;
4235:                    neighborTile[nw] = (x - 1) >= 0 && (y - 1) >= 0 ? _wvm.CurrentWorld.Tiles[x - 1, y - 1] : null;
4236:                    neighborTile[sw] = (x - 1) >= 0 && (y + 1) < height ? _wvm.CurrentWorld.Tiles[x - 1, y + 1] : null;
4237:                    neighborTile[se] = (x + 1) < width && (y + 1) < height ? _wvm.CurrentWorld.Tiles[x + 1, y + 1] : null;
4375:                        neighborTile[e] = (x + 1) < width ? ((!FilterManager.TileIsNotAllowed(_wvm.CurrentWorld.Tiles[x + 1, y].Type)) ? _wvm.CurrentWorld.Tiles[x + 1, y] : null) : null;
4376:                        neighborTile[n] = (y - 1) >= 0 ? ((!FilterManager.TileIsNotAllowed(_wvm.CurrentWorld.Tiles[x, y - 1].Type)) ? _wvm.CurrentWorld.Tiles[x, y - 1] : null) : null;

```


---

## 👤 User(sidechain) · 2026-08-07T07:07:39.439Z

**📎 ToolResult**

```
docs/completed/platform-and-connected-texture-rendering.md:116:All solid non-framed tiles (stone, dirt, grass, sand, etc.) and any tile with `CanBlend=true` use this path.
docs/completed/platform-and-connected-texture-rendering.md:160:| `IsGrass == true` | 2 | `grassRules` (relaxed OR-logic for corners) |
docs/completed/platform-and-connected-texture-rendering.md:189:- `grassRules[16]` — grass-specific with relaxed corner matching
docs/completed/platform-and-connected-texture-rendering.md:226:For `strictness == 2`, corner checks use OR logic: a corner is satisfied if EITHER the same-type diagonal bit OR the blend diagonal bit is set. This produces smoother grass-to-dirt transitions.
docs/completed/platform-and-connected-texture-rendering.md:228:When no grass rule matches, masks are merged (`sameStyle |= mergeMask`) and `baseRules` are used as fallback.

```


---

## 🤖 Assistant · 2026-08-07T07:07:44.995Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have everything needed. One more check: the neighborTile population near 5700 (the blend path) — line 4230 is a different draw pass (maybe the "preview" or earlier method). Let me find the population right before 5709 — grep showed only 4230 and 4375 before 5700? That means the blend path at 5709 is inside the same loop that populated neighborTile at ~4375? Actually the draw method containing line 5709 might start around 4323 ("BlendRules blendRules = BlendRules.Instance" at 4323). So neighborTile is set at 4375+ and reused throughout — including at 5726. Good; let me confirm the method containing line 5709 starts where. Let me grep for the method signature between 4300 and 5709, e.g. "private void DrawTiles" etc.

Also confirm the grass texture row range: cell rows A-V = 0-21; docs mention. And "110 rows" for Tiles_2: TEdit textures are padded to a power-of-two maybe. Let me quickly check the actual Tiles_2 grass texture file height. Search textures dir for Tiles_2.png and its size. Let me do a find.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:07:45.844Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor && grep -n \"    private void Draw\\|    public void Draw\\|    private void Render\\|unsafe.*Draw\" src/TEdit/View/WorldRenderXna.xaml.cs | awk -F: '$1>4200 && $1<5760' | head; echo \"=== texture files ===\"; find . -iname \"Tiles_2*\" 2>/dev/null | head; echo \"=== texture padding ===\"; grep -rn \"Tiles_2\\|padding\\|Pad\" src/TEdit.UI/Rendering/TextureDictionary.cs 2>/dev/null | head; find src -name \"TextureDictionary*.cs\" | head",
 "description": "Find draw method and grass texture"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:07:50.201Z

**📎 ToolResult**

```
4320:    public void DrawTileTextures(bool drawInverted = false)
=== texture files ===
=== texture padding ===

```


---

## 🤖 Assistant · 2026-08-07T07:07:53.359Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor && grep -rn \"class TextureDictionary\" src --include=\"*.cs\" | head -3; echo \"===\"; grep -rln \"GetTile(\" src --include=\"*.cs\" | head; echo \"=== grass texture loading/pad ===\"; grep -rn \"Height <\\|PaddingMode\\|ExtendTexture\\|22 rows\\|rows\" src/TEdit/View/WorldRenderXna.xaml.cs | head",
 "description": "Locate texture dictionary implementation"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:07:53.458Z

**📎 ToolResult**

```
===
src/TEdit/Render/Textures.cs
src/TEdit/View/WorldRenderXna.xaml.cs
src/TEdit/Editor/Clipboard/ClipboardTiledPreview.cs
src/TEdit5/Controls/WorldRenderEngine/RasterTileCache.cs
src/TEdit5/Controls/WorldRenderEngine/IRasterTileCache.cs
src/TEdit5/Controls/WorldRenderEngine/Layers/WorldPixelsCustomDrawOp.cs
=== grass texture loading/pad ===
src/TEdit/View/WorldRenderXna.xaml.cs:1422:                    if (xnaRect.Width <= 0 || xnaRect.Height <= 0)
src/TEdit/View/WorldRenderXna.xaml.cs:1567:                                            extraSourceRect.Width <= 0 || extraSourceRect.Height <= 0)
src/TEdit/View/WorldRenderXna.xaml.cs:1571:                                            tileSourceRect.Width <= 0 || tileSourceRect.Height <= 0)
src/TEdit/View/WorldRenderXna.xaml.cs:1612:                            if (source.Height <= 0 || source.Width <= 0)
src/TEdit/View/WorldRenderXna.xaml.cs:1740:                            // 4 biome rows: Normal(0), Crimson(1), Hallowed(2), Corrupt(3)
src/TEdit/View/WorldRenderXna.xaml.cs:1749:                            // 4 biome rows: Normal(0), Crimson(1), Hallowed(2), Corrupt(3)
src/TEdit/View/WorldRenderXna.xaml.cs:1926:                if (source.Height <= 0 || source.Width <= 0)
src/TEdit/View/WorldRenderXna.xaml.cs:2405:                                if (source.Height <= 0 || source.Width <= 0)
src/TEdit/View/WorldRenderXna.xaml.cs:2793:        if (srcRect.Width < bitmap.PixelWidth || srcRect.Height < bitmap.PixelHeight)
src/TEdit/View/WorldRenderXna.xaml.cs:4479:                                    int treeType = -1; //Default to normal in case no grass grows beneath the tree

```


---

## 🤖 Assistant · 2026-08-07T07:07:59.024Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Enough. The "110 rows" detail: I couldn't verify a 110-row count in code; the grass UV grid in BlendRules spans rows A..V (22 rows) × cols 1..16. I'll report that precisely and note I found no "110 rows" literal; the grassRules cells map into rows P..V (15-21) for the merge/blend frames of grass sheets.

Wait — one more useful check: in the renderer blend path, grass textures: `var tileTex = _textureDictionary.GetTile(curtile.Type)` — where does GetTile come from? `src/TEdit/Render/Textures.cs`. Quick grep for GetTile in Textures.cs and any height padding, to see whether grass textures are padded for extra rows. Let me do one quick check, then also verify line numbers for the quote of TileProperty JSON path for grass (src/TEdit.Terraria/Data/tiles.json). Also the git status of TEdit repo? Not needed.

Let me quickly grep Textures.cs for GetTile and padding.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:07:59.634Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor && grep -n \"GetTile\\|pad\\|Pad\\|V ==\\|maxRow\\|110\" src/TEdit/Render/Textures.cs | head -20",
 "description": "Check texture loading for padding"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:07:59.679Z

**📎 ToolResult**

```
161:    public Texture2D GetTile(int num) => GetTextureById(Tiles, num, "Images\\Tiles_{0}");
367:            return GetTile(tileId);
374:            PreviewTextureType.PalmTree => GetTile(323), // Palm tree trunk texture
377:            _ => GetTile(tileId)

```


---

## 🤖 Assistant · 2026-08-07T07:08:11.051Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
No padding logic found in that file; textures come from extracted game assets (Images/Tiles_2) which already contain all rows (the vanilla grass texture is tall). Fine.

I have enough for a thorough report. Let me also double check one thing for part A item 3: the caller believed grass frames the dirt AROUND it via AddFrame. In 1.4.0.5 there is no AddFrame. The mechanism is mutual: when dirt (index1==0) is framed and sees a tileMergeDirt neighbor (grass), dirt calls WorldGen.TileFrame(neighbor) and reads WorldGen.mergeUp/mergeDown/mergeLeft/mergeRight flags that the neighbor set during its own framing (see 52223+ where mergeUp=true is set). And conversely grass, when framed, runs TileMergeAttempt(-2, 0, ...) which marks dirt neighbors as -2 and then the big mask chain picks the grass merge frames (rows with -2 combos), setting mergeUp etc. so the dirt side knows. The recursive TileFrame calls inside TileMergeAttemptFrametest are what "frames the neighbors".

Wait — careful: which direction does grass mark? For grass (index1=2), at line 50767: `if (Main.tileMergeDirt[index1]) { TileMergeAttempt(-2, 0, ref up, ...) }` — so dirt neighbors (type 0) get rewritten to -2 (a special marker meaning "merge-partner present, use merge frame"). Then the mask chain at 52189+ (`Main.tileMergeDirt[index1] || ChecksForMerge`) converts -2 combos into the merge-frame rectangles (rows 5-9, i.e. Y=90..162) and sets WorldGen.mergeUp/mergeDown/mergeLeft/mergeRight = true, which are then read by the adjacent dirt tile's own TileFrame via case 0 / TileMergeAttemptFrametest. Yes — mutual handshake.

Also for grass: which neighbors count as "same"? In vanilla, grass merges with dirt via tileMergeDirt; grass-family-to-grass-family is NOT same-type (2 vs 23 are different types, no merge). Mud (59) merges with jungle (60) and mushroom (70) via Sets.Mud/tileBrick + GrassSpecial; dirt merges with grass family via MergesWithDirtInASpecialWay = {2,23,109,199,477,492} — note 60 and 70 are absent there (they merge with mud instead). 

Let me verify the tileMergeDirt entries include 2,23,60,70,109,199,477,492 — grep showed 109 entries of tileMergeDirt; check a few.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:08:11.154Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && grep -n \"tileMergeDirt\\[2\\]\\|tileMergeDirt\\[23\\]\\|tileMergeDirt\\[60\\]\\|tileMergeDirt\\[70\\]\\|tileMergeDirt\\[109\\]\\|tileMergeDirt\\[199\\]\\|tileMergeDirt\\[477\\]\\|tileMergeDirt\\[492\\]\" Main.cs",
 "description": "Verify grass family tileMergeDirt flags"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:08:11.204Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-07T07:08:14.005Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && grep -rn \"tileMergeDirt\" --include=\"*.cs\" . | grep -v \"Main.cs\" | head -10; echo \"===\"; grep -n \"tileMergeDirt\" Main.cs | sed -n '1,6p'",
 "description": "Find where tileMergeDirt is populated"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:08:14.087Z

**📎 ToolResult**

```
WorldGen.cs:50638:                          if (up > -1 && Main.tileMergeDirt[up])
WorldGen.cs:50650:                          if (down > -1 && Main.tileMergeDirt[down])
WorldGen.cs:50662:                          if (left > -1 && Main.tileMergeDirt[left])
WorldGen.cs:50674:                          if (right > -1 && Main.tileMergeDirt[right])
WorldGen.cs:50695:                          if (upLeft > -1 && Main.tileMergeDirt[upLeft])
WorldGen.cs:50699:                          if (upRight > -1 && Main.tileMergeDirt[upRight])
WorldGen.cs:50703:                          if (downLeft > -1 && Main.tileMergeDirt[downLeft])
WorldGen.cs:50707:                          if (downRight > -1 && Main.tileMergeDirt[downRight])
WorldGen.cs:50767:                      if (Main.tileMergeDirt[index1])
WorldGen.cs:52189:                      if (rectangle.X == -1 && rectangle.Y == -1 && (Main.tileMergeDirt[index1] || index1 > -1 && TileID.Sets.ChecksForMerge[index1]))
===
440:    public static bool[] tileMergeDirt = new bool[623];
5293:      Main.tileMergeDirt[202] = true;
5297:      Main.tileMergeDirt[498] = true;
5305:      Main.tileMergeDirt[188] = true;
5374:      Main.tileMergeDirt[177] = true;
5375:      Main.tileMergeDirt[190] = true;

```


---

## 🤖 Assistant · 2026-08-07T07:08:19.143Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Hmm, so Main.cs populates tileMergeDirt for 202, 498, 188, 177, 190, 197, 175, 176, 208, 234, 160, 145, 146, 148... but not 2/23/60/70/109/199? That's strange — grass must have tileMergeDirt[2]=true. Maybe the decompile's Main.cs is missing some lines, or the assignments happen via a loop. Let me grep Main.cs around where tileMergeDirt assignments cluster, and search for "tileMergeDirt" with a loop like `for`. Search "= true;" near a loop. Let me grep for "MergesWithDirt" in Main.cs or a data-loading path. Actually there might be a file loading from TileData (in 1.4.4+) but in 1.4.0.5 all assignments are in code. Let me grep the whole Main.cs for "tileMergeDirt" and count distinct indices, checking whether 2 exists with different spacing, e.g. "tileMergeDirt[ (int)"]? Let me search for "MergeDirt" case-insensitively.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:08:19.714Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && grep -in \"mergedirt\" Main.cs | grep -i \"\\[2\\]\\|\\[23\\]\\|\\[60\\]\\|\\[70\\]\\|\\[109\\]\\|\\[199\\]\\|loop\\|for\" | head; echo \"=== all mergedirt indices ===\"; grep -o \"tileMergeDirt\\[[0-9]*\\] = true\" Main.cs | grep -o \"\\[[0-9]*\\]\" | tr -d '[]' | sort -n | tr '\\n' ' '",
 "description": "List all tileMergeDirt indices in Main.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:08:19.783Z

**📎 ToolResult**

```
=== all mergedirt indices ===
1 6 7 8 9 22 25 30 37 38 39 40 41 43 44 45 46 47 53 56 107 108 111 112 116 117 118 119 120 121 122 123 140 145 146 148 150 151 152 153 154 155 156 157 158 159 160 166 167 168 169 175 176 177 177 188 190 193 195 197 198 202 203 204 206 208 221 222 223 229 230 234 249 250 251 252 253 311 315 321 322 346 347 348 350 367 368 369 370 371 408 472 473 474 478 479 481 482 483 495 496 498 500 501 502 503 562 563

```


---

## 🤖 Assistant · 2026-08-07T07:08:25.201Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting — the decompiled Main.cs is missing the tileMergeDirt assignments for the grass family (2, 23, 60, 70, 109, 199, 477, 492). This is a gap in the partial decompile (or the decompiler dropped them). I should note this: vanilla Main.cs in the real game sets `Main.tileMergeDirt[2] = true;` etc.; this decompile lacks those lines. Let me double-check with a case-insensitive search for "tileMergeDirt[2" allowing whitespace.

Actually, note that 477/492 don't exist in 1.4.0.5? Golf grass 477/492 are 1.4.4 tiles... but TileID.cs here lists 477/492 (GolfGrass). Hmm, this decompile seems to be a hybrid. Whatever.

Also note: Main.tileMergeDirt assignments missing for grass — I'll flag it as a decompile gap but the logic in WorldGen.TileFrame (case 0 + ChecksForMerge + MergesWithDirtInASpecialWay = {2,23,109,199,477,492}) confirms grass is a dirt-merging tile.

Let me verify the search with flexible whitespace.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:08:25.351Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && grep -rn \"tileMergeDirt\\[ *2 *\\]\\|tileMergeDirt\\[ *23 *\\]\" Main.cs WorldGen.cs | head -5; echo \"---exit $?\"; grep -c \"tileMergeDirt\" Main.cs",
 "description": "Confirm grass tileMergeDirt assignments absent"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:08:33.172Z

**📎 ToolResult**

```
---exit 0
109

```


---

## 🤖 Assistant · 2026-08-07T07:08:40.216Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && grep -rn \"tileMergeDirt\" Main.cs | grep -E \"\\b(2|23|60|70|109|199)\\b\" | head -5; echo \"=== check Main.cs completeness: git log ===\"; git -C . log --oneline -3 2>/dev/null | head",
 "description": "Final check for grass dirt-merge flags"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:08:48.125Z

**📎 ToolResult**

```
=== check Main.cs completeness: git log ===
7a0caff Update README.md
fe3f668 Update project and README to run fresh on Windows 11 today
cd7484a Update README.md

```


---

## 🤖 Assistant · 2026-08-07T07:09:09.200Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: this decompile's Main.cs does NOT contain `tileMergeDirt[2] = true` etc. for the grass family — a decompile gap (the real game sets them). I'll flag it.

Now I have everything. Time to write the final report. It should be thorough, with file paths + line numbers and verbatim quotes for:
- vanilla block framing lookup (blockStyleLookup, SelfFrame8Way) — but note standard blocks (dirt/stone) do NOT use SelfFrame8Way; they use WorldGen.TileFrame's if/else chain. Quote the core.
- grass framing (WorldGen.TileFrame case 0 + tileMergeDirt branch + mask→merge frames).
- re-frame cascade (SquareTileFrame + TileMergeAttemptFrametest).
- TEdit BlockStyleLookup + GetBlockStyle + DetermineFrameNumber.
- Renderer grass sameStyle/mergeMask/strictness.
- BlendRules grassRules.

Structure the report by A and B as requested. Keep it organized. Include line numbers.

Key line numbers:
Vanilla Framing.cs (~/Project/GLM/SandboxWorld/Terarria1405/Framing.cs) — 406/407 lines, 18,101 bytes:
- Initialize: 24-122
- selfFrame8WayLookup Add8WayLookup calls: 28-74 (47 entries)
- blockStyleLookup: 75-81 (6 entries)
- phlebasTileFrameNumberLookup: 82-88; lazure: 89-93; centerWallFrameLookup: 94-99
- wallFrameLookup: 100-121 (20 entries)
- FindBlockStyle: 124-127
- Add8WayLookup(6-arg): 129-145; (2-arg): 147-156
- AddWallFrameLookup: 158-177
- WillItBlend: 179-182
- SelfFrame8Way: 184-287
- WallFrame: 289-354
- GetTileSafely: 356-383
- BlockStyle struct: 385-404

Important: NO AddFrame / FrameNearTile / Wiring / grass / tile-specific methods in this Framing.cs. Those belong to 1.4.4+ Framing; in 1.4.0.5 the equivalent is WorldGen.TileFrame / SquareTileFrame.

WorldGen.cs (~/Project/GLM/SandboxWorld/Terarria1405/WorldGen.cs) — 54,961 lines:
- SquareTileFrame: 48855-48866; SquareWallFrame: 48868-48879
- SlopeTile: 49170
- TileMergeAttemptFrametest (int lookfor): 49330; (bool[] lookfor): 49379
- TileMergeAttempt overloads: 49428 (myType,lookfor,4-dir), 49447 (8-dir), 49478 (bool[]), 49509 (bool[]+exclude), TileMergeAttemptWeird: 49541
- TileFrame: 49639 start
- neighbor init: 50400-50459
- slope mask adjustments: 50461-50477
- tileBrick merge for 60/70 with Mud: 50489-50500
- moss/165 checks: 50500-50540; halfBrick: 50540-50558
- merge flags reset: 50569-50572
- frame number (resetFrame/largeframes): 50573-50593
- TileMergeAttempt(index1, tileBlendAll...) 50594-50606; ForcedDirtMerging 50607-50623
- switch (index1) case 0 (dirt): 50624-50721; case 53/112/116/213/234: 50722-50766
- tileMergeDirt branch: 50767-50783
- index1==1/76/75 branch: 50784-50788; case 57 (ash/hell): 50791+; case 59 (mud): ~50799-50815 (GrassSpecial/JungleSpecial)
- mask→rectangle chain start: 52189 (ChecksForMerge/tileMergeDirt gate), merge frame selection with -2: 52210+ through ~53300; default fallback: 53523-53539; largeFrames adjustments 53540-53544
- assignment: 53559-53560

For grass frames, quote 50767-50783 and 52189-52230ish and one merge-frame case.

TEdit:
- TileFraming.cs ~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria/Render/TileFraming.cs (327 lines)
  - GemsparkTileIds: 15-16
  - SelfFrame8WayLookup builder + 47 entries: 56-126
  - BlockStyleLookup: 43-51
  - CalculateSelfFrame8Way: 137-269
  - DetermineFrameNumber: 277-289
  - WillItBlendGemspark: 295
  - GetBlockStyle: 297-303
  - GetLargeFrameType: 312-318
  - BlockStyle record: 326
- Renderer: ~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit/View/WorldRenderXna.xaml.cs (8757 lines)
  - DrawTileTextures: 4320
  - neighborTile population: 4375-4382 (approx; I saw 4375-4376; e/n/w/s/ne/nw/sw/se presumably 4375-4382)
  - CanBlend branch: 5709
  - gemspark: 5717-5722
  - sameStyle/mergeMask building: 5726-5799
  - grass strictness: 5796-5799
  - DetermineFrameNumber + GetUVForMasks: 5801-5804
  - source rect: 5813
  - slope/halfbrick hack: 5899-5954
  - biome detection switch (not framing): 290-360
- BlendRules: ~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit/Render/BlendRules.cs (511 lines)
  - baseRules: 93-112; blendRules: 120-179; grassRules construction 150-166 + rules 181-249
  - GetUVForMasks: 253-306 (strictness switch: 0 base, 1 blend, 2 grass)
  - MatchRule.Matches: 418-451; MatchesRelaxed: 454-505
  - SetUVsForString: 403-415 (A1..V9 cell notation)
  - ResetUVCache (TEdit's equivalent of the re-frame cascade): 309-365
- TileProperty: src/TEdit.Terraria/Objects/TileProperty.cs — IsGrass 122, IsStone 125, CanBlend 126, MergeWith 127, Merges(int) 162-168, Merges(TileProperty) 171-177
- tiles.json: src/TEdit.Terraria/Data/tiles.json — grass entries with mergeWith.

Also note the renderer's grass mask semantics: bit layout e=0x0001, n=0x0010, w=0x0100, s=0x1000, corners ne=0x00010000, nw=0x00100000, sw=0x01000000, se=0x10000000.

Note on "110 rows": no such constant found; grassRules UV cells range A1..V9 → rows 0..21 (22 rows), columns 1..16; grass-specific frames mostly rows F..V. The grass texture in TEdit is the game's own Images/Tiles_2 texture loaded whole, so extra rows just index into it.

Regarding the re-frame cascade in TEdit (question 4 covers vanilla; but worth mentioning TEdit's ResetUVCache invalidation of 3x3 neighborhood as the equivalent).

Also item 5 (slope/half-brick): vanilla — WorldGen.TileFrame mask adjustments 50433-50477 & 50540-50558, WorldGen.SlopeTile 49170; rendering slope slicing in TEdit renderer 5899-5954. Framing.SelfFrame8Way's BlockStyle lookup includes half-brick/slope entries (blockStyleLookup[1..5]).

One more check I should include for item A.2: "how does the standard block (dirt/stone) frame itself — is there a lookup table like SelfFrame8Way?" Answer: No. SelfFrame8Way is used ONLY by gemspark-type tiles (WillItBlend via GemsparkFramingTypes / ForcedDirtMerging / tileBrick). Standard blocks are framed by WorldGen.TileFrame's hardcoded if/else chain producing a Rectangle in the 18px grid. And FindBlockStyle/blockStyleLookup in Framing.cs is used only by SelfFrame8Way (for gemsparks), with the 6-entry table indexed by blockType() (full/halfbrick/slopes).

Let me verify where SelfFrame8Way is called from (to confirm gemspark-only usage).
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:09:09.241Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && grep -rn \"SelfFrame8Way(\" --include=\"*.cs\" . | grep -v \"Framing.cs\" | head; echo \"=== GemsparkFramingTypes usage ===\"; grep -rn \"GemsparkFramingTypes\" --include=\"*.cs\" . | grep -v TileID.cs | head",
 "description": "Confirm SelfFrame8Way callers"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:09:09.353Z

**📎 ToolResult**

```
WorldGen.cs:50389:                        Framing.SelfFrame8Way(i, j, tile1, resetFrame);
=== GemsparkFramingTypes usage ===
Framing.cs:181:      return TileID.Sets.ForcedDirtMerging[(int) myType] && otherType == (ushort) 0 || Main.tileBrick[(int) myType] && Main.tileBrick[(int) otherType] || (int) TileID.Sets.GemsparkFramingTypes[(int) otherType] == (int) TileID.Sets.GemsparkFramingTypes[(int) myType];

```


---

## 🤖 Assistant · 2026-08-07T07:09:11.618Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && sed -n '50378,50396p' WorldGen.cs",
 "description": "Read SelfFrame8Way call site condition"
}
```


---

## 👤 User(sidechain) · 2026-08-07T07:09:11.656Z

**📎 ToolResult**

```
                                          }
                                      }
                                  }
                              }
                          }
                      }
                    }
                    else
                    {
                      if (index1 >= (int) byte.MaxValue && index1 <= 268 || index1 == 385 || index1 >= 446 && index1 <= 448)
                      {
                        Framing.SelfFrame8Way(i, j, tile1, resetFrame);
                        return;
                      }
                      Tile tileTopCache = Main.tile[i, j - 1];
                      Tile tile10 = Main.tile[i, j + 1];
                      Tile tile11 = Main.tile[i - 1, j];
                      Tile tile12 = Main.tile[i + 1, j];
                      Tile tile13 = Main.tile[i - 1, j + 1];

```


---

## 🤖 Assistant · 2026-08-07T07:09:14.708Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: SelfFrame8Way is only for tile IDs 255-268, 385, 446-448 (gemsparks). Everything else goes through the general TileFrame path.

Now write the comprehensive report.
```

</details>


---

## 🤖 Assistant · 2026-08-07T07:10:30.969Z · glm-x-preview-260804

````
All exploration complete. Here is the full report.

---

# A. Vanilla decompiled source — `~/Project/GLM/SandboxWorld/Terarria1405`

## A.1 `Framing.cs` — size and structure

**Critical discovery first**: the vanilla decompile at this path has a **much smaller `Framing.cs` than you expected** — it is **406 lines / 18,101 bytes** at `~/Project/GLM/SandboxWorld/Terarria1405/Framing.cs`. It contains **only** the lookup-table-driven framing (gemspark SelfFrame8Way + wall framing). **There is no `AddFrame`, no `FrameNearTile`, no `Wiring`, and no grass handling anywhere in this `Framing.cs`** — I grepped the whole repo for `AddFrame`/`FrameNearTile`/`void Wiring`: zero hits. Those methods are a 1.4.4+ Framing.cs design; in **1.4.0.5 the real framing engine is `WorldGen.TileFrame`** (54,961-line `WorldGen.cs`). Everything you asked about in items 2–4 actually lives in `WorldGen.cs`.

### `Framing.cs` contents (all line numbers from that file)

| Method | Lines | What it does |
|---|---|---|
| `Initialize()` | 24–122 | Builds all lookup tables: `selfFrame8WayLookup` (256-entry array, 47 populated via `Add8WayLookup`, lines 28–74), `blockStyleLookup` (6 entries, lines 75–81), `phlebasTileFrameNumberLookup` (82–88), `lazureTileFrameNumberLookup` (89–93), `centerWallFrameLookup` (94–99), `wallFrameLookup` (20 entries, 100–121). Frame size is 18×18 px (16 px tile + 2 px gap). |
| `FindBlockStyle(Tile)` | 124–127 | `return Framing.blockStyleLookup[blockTile.blockType()];` — maps the tile's `blockType()` (0 = full, 1 = half-brick, 2–5 = slopes) to which faces are open for connection. |
| `Add8WayLookup(int, 6 shorts)` | 129–145 | Builds a 3-variant `Point16[3]` entry (variant × 3 random frames), multiplying grid coords by `frameSize8Way` (18,18). |
| `Add8WayLookup(int, short, short)` | 147–156 | Same but all 3 variants identical (used for single-frame cases). |
| `AddWallFrameLookup(...)` | 158–177 | Same idea for walls: 4 frames per mask entry, wall frame size 36×36. |
| `WillItBlend(ushort, ushort)` | 179–182 | The blend predicate for SelfFrame8Way: `ForcedDirtMerging[myType] && otherType == 0 || tileBrick[myType] && tileBrick[otherType] || GemsparkFramingTypes[other] == GemsparkFramingTypes[my]`. |
| `SelfFrame8Way(int i, int j, Tile, bool resetFrame)` | 184–287 | The 8-way bit-mask framer (gemspark-only, see A.2). |
| `WallFrame(int i, int j, bool resetFrame)` | 289–354 | Wall framing: builds a 4-bit neighbor mask from walls (or tile 54, a door), picks wall frame variant (phlebas/lazure/random), and indexes `wallFrameLookup[15 + centerWallFrameLookup[i%3][j%3]]` when fully surrounded. |
| `GetTileSafely` ×4 | 356–383 | Null/in-world-safe tile fetch (used everywhere, incl. NPC/Chest). |
| `struct BlockStyle` | 385–404 | `top/bottom/left/right` bools + `Clear()`. |

There are **no tile-specific framing methods** (no `FrameTree`, torch, etc.) in this file; those are inline in `WorldGen.TileFrame` and helpers in `WorldGen`/`TileDrawing`.

## A.2 SOLID BLOCK framing — no lookup table for dirt/stone

**Answer: there is no lookup table for standard blocks.** `SelfFrame8Way` + `selfFrame8WayLookup` are used **exclusively by gemspark-family tiles**. The gate is in `WorldGen.cs` at lines 50386–50391:

```csharp
// WorldGen.cs:50386-50391
if (index1 >= (int) byte.MaxValue && index1 <= 268 || index1 == 385 || index1 >= 446 && index1 <= 448)
{
  Framing.SelfFrame8Way(i, j, tile1, resetFrame);
  return;
}
```

i.e. only tile IDs 255–268, 385, 446–448 (gemsparks) take that path. Every other solid block (dirt 0, stone 1, grass family, …) falls through to a **hardcoded if/else chain inside `WorldGen.TileFrame`** that writes `rectangle.X` / `rectangle.Y` in an 18 px grid.

### `BlockStyle` / `FindBlockStyle` (the table you half-remembered)

The table is only **6 entries**, indexed by `blockType()`, and it is *only consulted by `SelfFrame8Way`* — it encodes which faces exist for full/half-brick/slope shapes, not frame numbers:

```csharp
// Framing.cs:75-81
Framing.blockStyleLookup = new Framing.BlockStyle[6];
Framing.blockStyleLookup[0] = new Framing.BlockStyle(true, true, true, true);
Framing.blockStyleLookup[1] = new Framing.BlockStyle(false, true, true, true);
Framing.blockStyleLookup[2] = new Framing.BlockStyle(false, true, true, false);
Framing.blockStyleLookup[3] = new Framing.BlockStyle(false, true, false, true);
Framing.blockStyleLookup[4] = new Framing.BlockStyle(true, false, true, false);
Framing.blockStyleLookup[5] = new Framing.BlockStyle(true, false, false, true);

// Framing.cs:124-127
private static Framing.BlockStyle FindBlockStyle(Tile blockTile)
{
  return Framing.blockStyleLookup[blockTile.blockType()];
}
```

### How a standard block actually frames (`WorldGen.TileFrame`, start line 49639)

1. **Neighbor mask init** (`WorldGen.cs:50400–50459`) — 8 ints `up/down/left/right/upLeft/upRight/downLeft/downRight`, each `-1` (empty/air) or the neighbor's type (stone-family types collapse to 1 via `Main.tileStone`). Slopes invalidate the adjacent side (`50461–50477`).

```csharp
// WorldGen.cs:50400-50418
int upLeft = -1;
int up = -1;
int upRight = -1;
int left = -1;
int right = -1;
int downLeft = -1;
int down = -1;
int downRight = -1;
if (tile11 != null && tile11.active())
{
  left = !Main.tileStone[(int) tile11.type] ? (int) tile11.type : 1;
  if (tile11.slope() == (byte) 1 || tile11.slope() == (byte) 3)
    left = -1;
}
...
```

2. **Variant selection** (`WorldGen.cs:50569–50593`) — merge flags cleared, then `num4 = genRand.Next(0,3)` if `resetFrame` else existing `frameNumber()`; phlebas/lazure override via `Main.tileLargeFrames`.

3. **Merge bookkeeping** (`WorldGen.cs:50594–50830`) — a long sequence of `TileMergeAttempt`/`TileMergeAttemptFrametest` calls that rewrite neighbor ints to `index1` (same-type connect) or `-2` (merge-partner connect), plus type-specific switches (dirt `case 0`, sand 53, mud 59, etc.).

4. **Mask → frame rectangle** (`WorldGen.cs:52189–53544`) — a giant `if/else` chain on `up/down/left/right == index1` vs `-2` vs `-1`, writing `rectangle.X/Y` (18 px units: X 0–234, Y rows 0–4 for normal frames; rows 5–9 = Y 90–162 for **merge** frames). Representative branch:

```csharp
// WorldGen.cs:53521-53535 (a "normal" branch — top+right connected, bottom/left not)
else if (up == index1 && down != index1 && (left != index1 && right == index1))
{
  switch (num4)
  {
    case 0:
      rectangle.X = 0;
      rectangle.Y = 72;
      break;
    case 1:
      rectangle.X = 36;
      rectangle.Y = 72;
      break;
    default:
      rectangle.X = 72;
      rectangle.Y = 72;
      break;
  }
}
```

5. **Fallback + write** (`WorldGen.cs:53523–53560`): if nothing matched, use the isolated-tile frames `(18,18)/(36,18)/(54,18)` by variant; large-frame types add 90 to Y for variant 3; then `tile1.frameX = (short)rectangle.X; tile1.frameY = (short)rectangle.Y;` (lines 53559–53560).

### Verbatim `SelfFrame8Way` core (for reference — the gemspark path)

```csharp
// Framing.cs:184-287 (abridged to the essential shape)
public static void SelfFrame8Way(int i, int j, Tile centerTile, bool resetFrame)
{
  if (!centerTile.active())
    return;
  Framing.BlockStyle blockStyle1 = Framing.FindBlockStyle(centerTile);
  int index = 0;
  ...
  if (blockStyle1.top)
  {
    Tile tileSafely = Framing.GetTileSafely(i, j - 1);
    if (tileSafely.active() && Framing.WillItBlend(centerTile.type, tileSafely.type))
    {
      blockStyle2 = Framing.FindBlockStyle(tileSafely);
      if (blockStyle2.bottom)
        index |= 1;
      else
        blockStyle2.Clear();
    }
  }
  // ... left => |2, right => |4, bottom => |8
  // corners (only when both adjacent cardinals connected and the corner's faces align):
  //   upLeft => |16 (requires blockStyle2.left && blockStyle3.top, corner.right && corner.bottom)
  //   upRight => |32, downLeft => |64, downRight => |128
  if (resetFrame)
    centerTile.frameNumber((byte) WorldGen.genRand.Next(0, 3));
  Point16 point16 = Framing.selfFrame8WayLookup[index][(int) centerTile.frameNumber()];
  centerTile.frameX = point16.X;
  centerTile.frameY = point16.Y;
}
```

The 47 populated `selfFrame8WayLookup` entries are `Framing.cs:28–74` (indices 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,19,23,27,31,37,39,45,47,55,63,74,75,78,79,91,95,111,127,140,141,142,143,159,173,175,191,206,207,223,239,255 — that is your "47-entry table"; the numeric literals are `0x01|0x02|0x04...` style masks, e.g. `Add8WayLookup(19, 1, 4, 3, 4, 5, 4)`).

## A.3 GRASS framing

Grass is **not** handled by a dedicated method and there is no "grass" string in `Framing.cs` at all. Grass (2), corrupt (23), hallowed (109), crimson (199), golf (477/492) frame through the **general `TileFrame` path** because they are *dirt-merging* tiles; jungle (60) and mushroom (70) additionally merge with **mud (59)** because they are `Main.tileBrick` types merging against `TileID.Sets.Mud`.

Key data (`~/Project/GLM/SandboxWorld/Terarria1405/ID/TileID.cs`):

```csharp
// TileID.cs:738-739
public static bool[] Grass = TileID.Sets.Factory.CreateBoolSet(2, 23, 60, 199, 109, 477, 492);
// TileID.cs:693  — used by MUD to join to jungle/mushroom grass
public static bool[] GrassSpecial = TileID.Sets.Factory.CreateBoolSet(70, 60);
// TileID.cs:714  — tiles that run the merge-frame code path
public static bool[] ChecksForMerge = TileID.Sets.Factory.CreateBoolSet(0, 2, 60, 70, 199, 109, 477, 492, 57, 58, 75, 76, ...);
// TileID.cs:737  — the dirt side of the handshake
public static bool[] MergesWithDirtInASpecialWay = TileID.Sets.Factory.CreateBoolSet(2, 23, 109, 199, 477, 492);
// TileID.cs:688
public static bool[] Mud = TileID.Sets.Factory.CreateBoolSet(59);
```

⚠️ **Decompile gap warning**: `Main.cs` in this repo populates `Main.tileMergeDirt` for 109 indices (1, 6–9, 22, 25, 30, 37–47, 53, 56, 107–112, 116–123, 140, 145–160, 166–169, 175–177, 188–204, 206, 208, 221–223, 229–230, 234, 249–253, 311, 315, 321–322, 346–348, 350, 367–371, 408, 472–474, 478–479, 481–483, 495–496, 498, 500–503, 562–563) but **the lines for the grass family (2, 23, 60, 70, 109, 199) are missing** from this decompile. In the real game those are set; the code paths below (`WorldGen.cs:50638+`, `50767+`) only make sense with them set. If you port logic from this tree, add them yourself.

### The mutual grass ⇄ dirt handshake (the essential logic)

**Grass side** — when the grass tile itself is framed, dirt neighbors are rewritten to the special marker `-2` (`WorldGen.cs:50767–50783`):

```csharp
// WorldGen.cs:50767-50783
if (Main.tileMergeDirt[index1])
{
  WorldGen.TileMergeAttempt(-2, 0, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
  if (index1 == 1)
  {
    if ((double) j > Main.rockLayer)
      WorldGen.TileMergeAttemptFrametest(i, j, index1, 59, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
    WorldGen.TileMergeAttemptFrametest(i, j, index1, 57, ref up, ref down, ref left, ref right, ref upLeft, ref upRight, ref downLeft, ref downRight);
  }
}
```

`TileMergeAttempt` is a pure mask rewrite (`WorldGen.cs:49447–49466`):

```csharp
// WorldGen.cs:49447-49466 (8-dir overload)
public static void TileMergeAttempt(
  int myType, int lookfor,
  ref int up, ref int down, ref int left, ref int right,
  ref int upLeft, ref int upRight, ref int downLeft, ref int downRight)
{
  if (lookfor == up) up = myType;
  if (lookfor == down) down = myType;
  if (lookfor == left) left = myType;
  if (lookfor == right) right = myType;
  if (lookfor == upLeft) upLeft = myType;
  if (lookfor == upRight) upRight = myType;
  if (lookfor == downLeft) downLeft = myType;
  if (lookfor != downRight) return;
  downRight = myType;
}
```

Then the mask→frame chain **is gated on `tileMergeDirt`/`ChecksForMerge`** and treats `-2` as "merge partner here", selecting the *merge frames* (the extra rows in the grass/dirt sheets, Y = 90–162, i.e. rows 5–9) and **raising the `WorldGen.mergeUp/mergeDown/mergeLeft/mergeRight` flags** (`WorldGen.cs:52189–52240`):

```csharp
// WorldGen.cs:52189-52240
if (rectangle.X == -1 && rectangle.Y == -1 && (Main.tileMergeDirt[index1] || index1 > -1 && TileID.Sets.ChecksForMerge[index1]))
{
  if (!flag1)
  {
    flag1 = true;
    WorldGen.TileMergeAttemptWeird(index1, -1, Main.tileSolid, ref up, ...);
  }
  if (up > -1 && up != index1) up = -1;
  if (down > -1 && down != index1) down = -1;
  if (left > -1 && left != index1) left = -1;
  if (right > -1 && right != index1) right = -1;
  if (up != -1 && down != -1 && (left != -1 && right != -1))
  {
    if (up == -2 && down == index1 && (left == index1 && right == index1))
    {
      switch (num4)
      {
        case 0: rectangle.X = 144; rectangle.Y = 108; break;
        case 1: rectangle.X = 162; rectangle.Y = 108; break;
        default: rectangle.X = 180; rectangle.Y = 108; break;
      }
      WorldGen.mergeUp = true;      // <-- tells the dirt above: "I am merging into you"
    }
    else if (up == index1 && down == -2 && (left == index1 && right == index1))
    {
      switch (num4)
      {
        case 0: rectangle.X = 144; rectangle.Y = 90; break;
        case 1: rectangle.X = 162; rectangle.Y = 90; break;
        default: rectangle.X = 180; rectangle.Y = 90; break;
      }
      WorldGen.mergeDown = true;
    }
    ...
```

**Dirt side** — your recollection is exactly right: *dirt re-frames the grass around it*. It is `case 0` of the type switch (`WorldGen.cs:50624–50721`). Dirt checks each neighbor for `Main.tileMergeDirt[neighbor]` (grass family) or type 147, **recursively calls `WorldGen.TileFrame` on that neighbor**, and only connects (`up = index1`, i.e. treat as dirt) if the neighbor raised the matching merge flag. It then also folds in `MergesWithDirtInASpecialWay` (the grass set above) for all 8 neighbors:

```csharp
// WorldGen.cs:50624-50690 (case 0 == Dirt, abridged)
case 0:
  if (up > -1 && Main.tileMergeDirt[up])
  {
    WorldGen.TileFrame(i, j - 1, false, false);   // <-- frame the grass above
    if (WorldGen.mergeDown) up = index1;           // grass said "I merge down into you"
  }
  else if (up == 147)
  {
    WorldGen.TileFrame(i, j - 1, false, false);
    if (WorldGen.mergeDown) up = index1;
  }
  if (down > -1 && Main.tileMergeDirt[down])
  {
    WorldGen.TileFrame(i, j + 1, false, false);
    if (WorldGen.mergeUp) down = index1;
  }
  ... // same for left / right
  bool[] dirtInAspecialWay = TileID.Sets.Conversion.MergesWithDirtInASpecialWay;
  if (up > -1 && dirtInAspecialWay[up]) up = index1;      // grass counts as dirt on all 8 slots
  if (down > -1 && dirtInAspecialWay[down]) down = index1;
  ... // left, right, then all four corners
```

**Jungle/mushroom grass ⇄ mud** — those two are `Main.tileBrick` types, so at `WorldGen.cs:50487–50493`:

```csharp
// WorldGen.cs:50487-50493
default:
  if (Main.tileBrick[index1])
  {
    if (index1 == 60 || index1 == 70)
    {
      WorldGen.TileMergeAttempt(index1, Main.tileBrick, TileID.Sets.Mud, ref up, ...);
      break;
    }
```

and mud's own `case 59` (`WorldGen.cs:~50800`) does the reverse: `TileMergeAttempt(index1, TileID.Sets.GrassSpecial, ...)` (joins to jungle/mushroom grass) plus `TileMergeAttempt(-2, 1, ...)` for stone below `rockLayer`. (Exact lines 50799–50820 region.)

## A.4 What happens on PLACE / REMOVE — the re-frame cascade

There is **no `AddFrame`/`FrameNearTile`/`Wiring` in 1.4.0.5**. The cascade is two mechanisms:

**1. `WorldGen.SquareTileFrame`** (`WorldGen.cs:48855–48866`) — re-frames the **full 3×3 neighborhood** of (i,j), center with `resetFrame`:

```csharp
// WorldGen.cs:48855-48866
public static void SquareTileFrame(int i, int j, bool resetFrame = true)
{
  WorldGen.TileFrame(i - 1, j - 1, false, false);
  WorldGen.TileFrame(i - 1, j, false, false);
  WorldGen.TileFrame(i - 1, j + 1, false, false);
  WorldGen.TileFrame(i, j - 1, false, false);
  WorldGen.TileFrame(i, j, resetFrame, false);
  WorldGen.TileFrame(i, j + 1, false, false);
  WorldGen.TileFrame(i + 1, j - 1, false, false);
  WorldGen.TileFrame(i + 1, j, false, false);
  WorldGen.TileFrame(i + 1, j + 1, false, false);
}
```

`SquareWallFrame` (48868–48879) is the identical 3×3 loop calling `Framing.WallFrame`. Called from ~40 sites in `WorldGen.cs` (e.g. liquid ops at 367/391/408, altar smashing at 4235–4415, gen passes at 13498/13634, 17676, 25535, 25612…). Region framing is `WorldGen.SectionTileFrame` (48905+) which iterates 200×150 sections calling `TileFrame` + `Framing.WallFrame` per tile.

**2. Recursive handshake re-framing inside `TileFrame` itself** — `TileMergeAttemptFrametest` (`WorldGen.cs:49330–49378` and the `bool[]` overload at 49379–49426) **calls `WorldGen.TileFrame` on the cardinal neighbor** when that neighbor is a candidate merge partner, then reads the flags:

```csharp
// WorldGen.cs:49330-49358 (int lookfor overload)
public static void TileMergeAttemptFrametest(
  int i, int j, int myType, int lookfor,
  ref int up, ref int down, ref int left, ref int right,
  ref int upLeft, ref int upRight, ref int downLeft, ref int downRight)
{
  if (up == lookfor)
  {
    WorldGen.TileFrame(i, j - 1, false, false);
    if (WorldGen.mergeDown) up = myType;
  }
  if (down == lookfor)
  {
    WorldGen.TileFrame(i, j + 1, false, false);
    if (WorldGen.mergeUp) down = myType;
  }
  ... // left (mergeRight), right (mergeLeft); corners are plain rewrites, no recursion
}
```

So: place/remove a tile → `SquareTileFrame` re-frames 3×3 → each of those tiles may recursively `TileFrame` its own cardinal neighbors (one step further) to resolve grass/dirt/brick/mud merges. That is the whole cascade.

## A.5 Slope / half-brick (skip, but note locations)

- `WorldGen.SlopeTile(int i, int j, int slope, bool noEffects)` — `WorldGen.cs:49170`.
- Slope invalidation of the neighbor mask — `WorldGen.cs:50433–50477` (each slope direction zeroes the corresponding neighbor slot) and again 50500–50510.
- Half-brick handling — `WorldGen.cs:50540–50558`.
- `Framing.BlockStyle` table entries 1–5 — `Framing.cs:77–81` (only affect SelfFrame8Way/gemspark).
- TEdit renderer's slope slicing — `WorldRenderXna.xaml.cs:5899–5954`.

---

# B. TEdit — `~/Project/GLM/SandboxWorld/Terraria-Map-Editor`

## B.6 `src/TEdit.Terraria/Render/TileFraming.cs` (327 lines) — a *port of the gemspark-only* `SelfFrame8Way`

Note its own header (lines 6–9): *"Terraria-accurate tile framing algorithms, ported from Terraria 1.4.5.4 Framing.SelfFrame8Way(). Used for gemspark blocks and other tiles that use 8-way neighbor-based framing."* It is **not** the general block framer — TEdit's general framing is `BlendRules` (see B.7).

**`BlockStyleLookup` (lines 43–51)** and **`GetBlockStyle` (lines 297–303)**, verbatim:

```csharp
/// <summary>
/// BlockStyle lookup matching Terraria's Framing.blockStyleLookup.
/// Index maps to BrickStyle enum value (0=Full, 1=HalfBrick, 2-5=slopes).
/// Each entry defines which faces are open for neighbor connections.
/// </summary>
private static readonly BlockStyle[] BlockStyleLookup =
[
    new(Top: true,  Left: true,  Right: true,  Bottom: true),   // 0: Full block
    new(Top: false, Left: true,  Right: true,  Bottom: true),   // 1: HalfBrick
    new(Top: false, Left: true,  Right: false, Bottom: true),   // 2: SlopeTopRight
    new(Top: false, Left: false, Right: true,  Bottom: true),   // 3: SlopeTopLeft
    new(Top: true,  Left: false, Right: true,  Bottom: false),  // 4: SlopeBottomRight
    new(Top: true,  Left: false, Right: false, Bottom: true),   // 5: SlopeBottomLeft
];
```

```csharp
private static BlockStyle GetBlockStyle(Tile tile)
{
    int styleIndex = (int)tile.BrickStyle;
    if (styleIndex >= 0 && styleIndex < BlockStyleLookup.Length)
        return BlockStyleLookup[styleIndex];
    return BlockStyleLookup[0]; // Full block default
}
```

⚠️ Note a subtle divergence from vanilla: TEdit entry **2** is `Top:false, Left:true, Right:false` and **3** is `Top:false, Left:false, Right:true`, while vanilla decompile has `blockStyleLookup[2] = (false, true, true, false)` and `[3] = (false, true, false, true)` (constructor order `up, down, left, right` ⇒ vanilla #2 = top F, bottom T, left T, right F; TEdit #2 = top F, left T, right F, bottom T — same effective faces, different arg order, but vanilla #3 has `right:true, bottom:true` vs TEdit `right:true, bottom:true`... effectively TEdit #2/#3 have bottom open, vanilla #2/#3 also bottom open — consistent, just reordered fields; the record order is `Top, Left, Right, Bottom`).

**`DetermineFrameNumber` modes (lines 271–289)**, verbatim body:

```csharp
public static int DetermineFrameNumber(ushort tileType, int x, int y)
{
    byte largeFrameType = GetLargeFrameType(tileType);

    if (largeFrameType == 1)
        return PhlebasLookup[y % 4][x % 3] - 1;

    if (largeFrameType == 2)
        return LazureLookup[x % 2][y % 2] - 1;

    // Default: deterministic pseudo-random based on position (0-2)
    return ((x * 7) + (y * 11)) % 3;
}
```

- Mode 0 (default): deterministic `(x*7 + y*11) % 3` (vanilla uses `genRand`, TEdit makes it deterministic).
- Mode 1 phlebas: `PhlebasLookup[y%4][x%3] - 1` (table lines 19–25, matches vanilla 1.4.0.5 inline table).
- Mode 2 lazure: `LazureLookup[x%2][y%2] - 1` (lines 28–32).
- `GetLargeFrameType` (312–318) reads `WorldConfiguration.TileProperties[tileType].LargeFrameType`.

Other contents: `GemsparkTileIds = {255..268, 385, 446, 447, 448}` (15–16), `SelfFrame8WayLookup` builder with the same 47 entries (56–126; comment "47 entries from Framing.cs lines 28-74"), `CalculateSelfFrame8Way` (137–269) — a faithful port including the 4 corner checks requiring both adjacent cardinals plus corner face alignment, `WillItBlendGemspark => myType == otherType` (295), `DefaultFrame = (1,1)*18` fallback (54), `BlockStyle` record at 326. Undefined indices return the default (261–265) instead of vanilla's null-crash risk.

## B.7 Renderer grass handling — `src/TEdit/View/WorldRenderXna.xaml.cs` (8,757 lines)

The blend path is in `DrawTileTextures(bool drawInverted = false)` (line 4320). `neighborTile[e/n/w/s/ne/nw/sw/se]` are populated at lines 4375–4382 and reused. The dispatch is at **line 5709**:

```csharp
// WorldRenderXna.xaml.cs:5709
else if (tileprop.CanBlend || !(tileprop.IsFramed || tileprop.IsAnimated))
{
    var tileTex = _textureDictionary.GetTile(curtile.Type);
    if (tileTex != null)
    {
        if (curtile.uvTileCache == 0xFFFF || curtile.hasLazyChecked == false)
        {
            if (TileFraming.IsGemSpark(curtile.Type))
            {
                var uv = TileFraming.CalculateSelfFrame8Way(_wvm.CurrentWorld, x, y);
                curtile.uvTileCache = (ushort)((uv.Y << 8) + uv.X);
                curtile.hasLazyChecked = true;
            }
            else
            {
                // TODO: Replace BlendRules path with full TileFrameCosmetic port for pixel-perfect accuracy
                int sameStyle = 0x00000000;
                int mergeMask = 0x00000000;
                int strictness = 0;
```

**Mask bit layout** (same in `sameStyle` and `mergeMask`): edges — `e`=0x0001, `n`=0x0010, `w`=0x0100, `s`=0x1000; corners — `ne`=0x00010000, `nw`=0x00100000, `sw`=0x01000000, `se`=0x10000000.

**Which tiles count as "same"** — three branches (lines 5729–5766):
1. `MergeWith == -1` (cobweb): any active neighbor (5729–5735).
2. `IsStone` (stone & gems): neighbor's `IsStone` is true (5736–5746).
3. Everything else (grass falls here): `tileprop.Merges(WorldConfiguration.GetTileProperties(neighbor.Type))` **OR** `curtile.Type == neighbor.Type` — both OR'd in for all 8 neighbors (5747–5766).

`TileProperty.Merges` (`src/TEdit.Terraria/Objects/TileProperty.cs:162–177`):

```csharp
public bool Merges(int other)
{
    if (other == this.Id) return true;
    if (!MergeWith.HasValue) return false;
    return MergeWith.Value == other;
}

public bool Merges(TileProperty other)
{
    if (other.MergeWith.HasValue && other.MergeWith.Value == Id) return true;
    if (MergeWith.HasValue && MergeWith.Value == other.Id) return true;
    if (MergeWith.HasValue && other.MergeWith.HasValue && MergeWith.Value == other.MergeWith.Value) return true;
    return false;
}
```

So for grass, "same" = same grass type, OR anything whose `MergeWith` chain reaches it (dirt, since grass `mergeWith: 0`). Concretely from `src/TEdit.Terraria/Data/tiles.json`:

| Id | Name | isGrass | mergeWith |
|---|---|---|---|
| 0 | Dirt | – | – |
| 2 | Grass | true | **0** (dirt) |
| 23 | Corrupt Grass | true | **0** |
| 109 | Hallowed Grass | true | **0** |
| 199 | Crimson Grass | true | **0** |
| 477 | Mowed Grass | true | **0** (note: `special` empty) |
| 492 | Hallowed Mowed Grass | true | **0** (`special: "Grass"`) |
| 60 | Jungle Grass | true | **59** (mud) |
| 70 | Mushroom Grass | true | **59** |
| 59 | Mud | – | **0** |
| 1/25/117/203 | Stone family | isStone | 0 |

**mergeMask + grass strictness** (lines 5784–5799) — verbatim:

```csharp
if (tileprop.MergeWith.HasValue && tileprop.MergeWith.Value > -1) //Merges with a specific type
{
    mergeMask |= (neighborTile[e]?.IsActive == true && neighborTile[e].Value.Type == tileprop.MergeWith.Value) ? 0x0001 : 0x0000;
    mergeMask |= (neighborTile[n]?.IsActive == true && neighborTile[n].Value.Type == tileprop.MergeWith.Value) ? 0x0010 : 0x0000;
    mergeMask |= (neighborTile[w]?.IsActive == true && neighborTile[w].Value.Type == tileprop.MergeWith.Value) ? 0x0100 : 0x0000;
    mergeMask |= (neighborTile[s]?.IsActive == true && neighborTile[s].Value.Type == tileprop.MergeWith.Value) ? 0x1000 : 0x0000;
    mergeMask |= (neighborTile[ne]?.IsActive == true && neighborTile[ne].Value.Type == tileprop.MergeWith.Value) ? 0x00010000 : 0x00000000;
    mergeMask |= (neighborTile[nw]?.IsActive == true && neighborTile[nw].Value.Type == tileprop.MergeWith.Value) ? 0x00100000 : 0x00000000;
    mergeMask |= (neighborTile[sw]?.IsActive == true && neighborTile[sw].Value.Type == tileprop.MergeWith.Value) ? 0x01000000 : 0x00000000;
    mergeMask |= (neighborTile[se]?.IsActive == true && neighborTile[se].Value.Type == tileprop.MergeWith.Value) ? 0x10000000 : 0x00000000;
    strictness = 1;
}
if (tileprop.IsGrass)
{
    strictness = 2;
}

int variant = TileFraming.DetermineFrameNumber(curtile.Type, x, y);
Vector2Int32 uvBlend = blendRules.GetUVForMasks((uint)sameStyle, (uint)mergeMask, strictness, variant);
curtile.uvTileCache = (ushort)((uvBlend.Y << 8) + uvBlend.X);
curtile.lazyMergeId = blendRules.lazyMergeValidation[uvBlend.Y, uvBlend.X];
```

So grass = strictness **2**. (The lazy-merge propagation at 5768–5783 uses `lazyMergeId` to resolve one-tile-deep dependency; `lazyMergeValidation` is the 22×16 table at `BlendRules.cs:44–67`.)

### Where the grass rule table lives: `src/TEdit/Render/BlendRules.cs` (511 lines)

`GetUVForMasks` (lines 261–306) picks the rule list by strictness:

```csharp
// BlendRules.cs:261-306 (switch body verbatim, abridged comments)
int bucketId = (int)(((neighborMask & 0x00001000) >> 9) + ((neighborMask & 0x00000100) >> 6) + ((neighborMask & 0x00000010) >> 3) + (neighborMask & 0x00000001));
int variationId = Math.Min(variant, 2);
switch (ruleStrictness)
{
    case 0:
        foreach (MatchRule rule in baseRules[bucketId])
            if (rule.Matches(neighborMask, blendMask))
                return rule.UVPosSet[variationId];
        break;
    case 1:
        foreach (MatchRule rule in blendRules[bucketId])
            if (rule.Matches(neighborMask, blendMask))
                return rule.UVPosSet[variationId];
        break;
    case 2:
        foreach (MatchRule rule in grassRules[bucketId])
        {
            if (rule.MatchesRelaxed(neighborMask, blendMask)) //Constraints behave slightly differently for grass tiles
            {
                return rule.UVPosSet[variationId];
            }
        }
        //Only get here if there were no unique grass rules.  As a result, reduce the constraints even more
        neighborMask |= blendMask;
        bucketId = (int)(...);
        foreach (MatchRule rule in baseRules[bucketId])
            if (rule.Matches(neighborMask, blendMask))
                return rule.UVPosSet[variationId];
        break;
}
return new Vector2Int32(0, 0);
```

- The 16 "buckets" = the 4 edge bits of `sameStyle` (`s,n,w,e` → bucket index 0–15).
- **`baseRules`** (lines 93–112): plain non-merging frames, terrafirma cells `A1`–`E9`.
- **`blendRules`** (lines 120–179): merge frames with `blendInclusionMask`/`blendExclusionMask` (stones, sand, dirt merges), cells `F1`–`O6`.
- **`grassRules`** = `blendRules` copy minus 8 conflicting `RemoveFirst()` rules (lines 150–166), plus the dedicated grass rules **lines 181–211** (cells `P1`–`V9` — these are the grass→dirt merge frames) and extra fallback rules **lines 213–249**. Representative:

```csharp
// BlendRules.cs:189-191, 196-197 (grass corner transitions into dirt)
grassRules[7].AddLast(new MatchRule(0x0000, 0x0011, 0x00000000, 0x00111000, "O9", "O15"));
grassRules[7].AddLast(new MatchRule(0x0010, 0x0001, 0x00100000, 0x00011000, "T1", "T3"));
grassRules[7].AddLast(new MatchRule(0x0001, 0x0010, 0x00010000, 0x00101000, "T4", "T6"));
...
grassRules[11].AddLast(new MatchRule(0x0000, 0x1001, 0x00000000, 0x10010100, "N8", "N14"));
grassRules[11].AddLast(new MatchRule(0x1000, 0x0001, 0x10000000, 0x00010100, "U1", "U3"));
```

- `MatchRule.Matches` = strict AND-matching (418–451); **`MatchesRelaxed`** = grass-specific OR corner logic (454–505): for each corner column, if the corner-inclusion bit and the blend-corner bit are both set they are OR-satisfied; exclusion still enforced. `SetUVsForString` (403–415) parses `"A1"` notation: row = letter−'A', col = number−1, 3 variants at start / midpoint / end.

**On "110 rows"**: I found **no literal 110** anywhere in TEdit's framing code or docs. The grass UV grid in `BlendRules` spans rows **A..V (0..21, 22 rows)** × cols **1..16**; grass-specific frames occupy rows **F..V**, with the pure grass-merge frames in rows **P..V** (15–21). Textures come straight from the game assets (`Textures.cs:161 GetTile → Images\Tiles_{0}`), so the tall Tiles_2 grass sheet is indexed whole; nothing pads or hard-codes a 110-row count. (The `case 60/23/199/203/109/70` switch at `WorldRenderXna.xaml.cs:313–349` is **biome detection for backgrounds**, not grass framing; grass/vine flip IDs are at 137–145.)

### TEdit's own "re-frame cascade" (equivalent of vanilla's)

`BlendRules.ResetUVCache` (`BlendRules.cs:309–365`) — invalidates `uvTileCache`/`lazyMergeId`/`hasLazyChecked`/`uvWallCache` for a rectangle **expanded by 1 in every direction** (`for x = -1..regionWidth+1`, `y = -1..regionHeight+1`), or a 3×3 block per tile for the list overload (312–335). That is TEdit's analogue of `WorldGen.SquareTileFrame`: dirty the 3×3 neighborhood and let the renderer lazily recompute UVs on next draw.

---

## Summary of the biggest corrections to the premises

1. **`Framing.cs` is only 406 lines** and contains *only* gemspark `SelfFrame8Way` + `WallFrame` + lookups. No `AddFrame`, no `FrameNearTile`, no `Wiring` (those are 1.4.4 concepts). The real block/grass framer is **`WorldGen.TileFrame`** (`WorldGen.cs:49639+`, ~4,000 lines long) with the cascade in **`WorldGen.SquareTileFrame`** (`WorldGen.cs:48855`).
2. **Standard blocks (dirt/stone) do not use a lookup table** — `selfFrame8WayLookup` + the 6-entry `blockStyleLookup` serve only gemsparks (IDs 255–268/385/446–448, gate at `WorldGen.cs:50386`). Dirt/stone/grass use a hardcoded neighbor-mask if/else chain producing an 18 px-grid `Rectangle` (rows 0–4 normal, rows 5–9 merge frames).
3. **Grass framing = the `tileMergeDirt` / `ChecksForMerge` / `MergesWithDirtInASpecialWay` handshake**: grass marks dirt neighbors `-2` and raises `mergeUp/mergeDown/mergeLeft/mergeRight`; dirt (case 0) **recursively `TileFrame`s its grass neighbors** and connects only if the flag is set. Your "grass sets frames on the dirt AROUND it" recollection is realized as those recursive `WorldGen.TileFrame(i±1, j±1, ...)` calls inside `case 0` (`WorldGen.cs:50624–50721`) and `TileMergeAttemptFrametest` (`WorldGen.cs:49330`).
4. In TEdit, `TileFraming.cs` is **gemspark-only**; general (incl. grass) framing is `BlendRules` with `strictness 2` + `MatchesRelaxed` + the `grassRules` table, driven by `IsGrass`/`MergeWith` from `src/TEdit.Terraria/Data/tiles.json`.
````
